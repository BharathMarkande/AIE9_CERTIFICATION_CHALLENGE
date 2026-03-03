"""
Implements the Retrieval + Generation layer for RiskHalo.

This module:
1. Retrieves relevant session summaries from ChromaDB
2. Injects retrieved context into a structured prompt
3. Generates grounded coaching responses
4. Enforces strict 4-section output format

Architecture
------------
User Question
      ↓
Vector Retrieval (ChromaDB)
      ↓
Context Injection
      ↓
LLM Generation
      ↓
Structured Coaching Response
"""

import chromadb
from openai import OpenAI
from dotenv import load_dotenv

from rag.embedder import OpenAIEmbedder

load_dotenv()

class RiskHaloRetriever:
    """
    Retrieval-Augmented Generation (RAG) layer for RiskHalo.

    Responsibilities:
    - Perform semantic similarity search
    - Inject grounded context
    - Generate structured coaching output
    """

    def __init__(
        self,
        collection_name="riskhalo_sessions",
        top_k=4,
        model="gpt-4o-mini",
        persist_directory: str = "./chroma_db"
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_collection(collection_name)

        self.top_k = top_k
        self.llm = OpenAI()
        self.model = model
        # Use same embedder as when indexing (OpenAI 1536-dim); Chroma default is 384-dim.
        self.embedder = OpenAIEmbedder()

    # --------------------------------------------------
    # Retrieve Relevant Sessions
    # --------------------------------------------------
    def retrieve(self, query: str):
        """
        Performs vector similarity search against stored
        session summaries.

        Parameters
        ----------
        query : str
            User coaching question.

        Returns
        -------
        list[str]
            Top-k retrieved session summaries.
        """

        query_embedding = self.embedder.embed_text(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
        )

        documents = results.get("documents", [[]])[0]
        return documents

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------
    def build_prompt(self, question: str, contexts: list[str]):
        """
        Constructs structured grounding prompt.

        Enforces:
        - No hallucination
        - Context-only reasoning
        - Strict 4-section output format
        """

        joined_context = "\n\n---\n\n".join(contexts)

        system_prompt = """
            You are RiskHalo, a performance-focused trading execution coach.

            Your role is to analyze behavioral trading patterns strictly using retrieved session summaries.

            ---------------------------------------
            CORE OPERATING RULES
            ---------------------------------------

            1. Use ONLY the retrieved session context.
            2. Do NOT invent metrics, trends, or assumptions.
            3. Do NOT infer psychological states beyond what metrics support.
            4. Do NOT predict markets or discuss price direction.
            5. If data is insufficient, explicitly state that the evidence is limited.

            ---------------------------------------
            ANALYTICAL FOCUS
            ---------------------------------------

            You must focus strictly on:
            - Behavioral state classification
            - Severity score interpretation
            - Expectancy shifts
            - Discipline score and rule compliance
            - Risk management consistency
            - Performance trends across sessions (if multiple sessions are retrieved)

            When multiple sessions are provided:
            - Identify whether performance is improving, deteriorating, or stable.
            - Reference metric changes explicitly.

            ---------------------------------------
            STRICT RESPONSE STRUCTURE (MANDATORY)
            ---------------------------------------

            Your response must follow this exact 4-section format:

            1. Direct Conclusion  
            - Clear, concise answer to the user's question.

            2. Evidence From Sessions  
            - Reference specific metrics or session patterns.
            - Mention severity, expectancy delta, discipline score when relevant.

            3. Behavioral Interpretation  
            - Explain what the metrics imply about execution quality.
            - Avoid emotional language.

            4. Actionable Adjustment  
            - Provide 1-3 practical, execution-focused improvements.

            ---------------------------------------

            Maintain a professional, performance-oriented tone.
            Avoid exaggeration.
            Avoid motivational language.
            Avoid generic advice.
            Stay data-grounded at all times.

            Your objective is to improve execution discipline and behavioral stability.
            """

        user_prompt = f"""
            User Question:
            {question}

            Retrieved Session Context:
            {joined_context}
            """

        return system_prompt, user_prompt

    # --------------------------------------------------
    # Generate Answer
    # --------------------------------------------------
    def generate(self, question: str):
        """
        Executes full RAG pipeline:
        - Retrieve
        - Build prompt
        - Generate structured response

        Returns
        -------
        dict:
            {
                "question": str,
                "retrieved_contexts": list[str],
                "answer": str
            }
        """

        contexts = self.retrieve(question)

        if not contexts:
            return {
                "question": question,
                "retrieved_contexts": [],
                "answer": "No relevant session data found."
            }

        system_prompt, user_prompt = self.build_prompt(
            question,
            contexts
        )

        response = self.llm.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        answer = response.choices[0].message.content

        return {
            "question": question,
            "retrieved_contexts": contexts,
            "answer": answer,
        }