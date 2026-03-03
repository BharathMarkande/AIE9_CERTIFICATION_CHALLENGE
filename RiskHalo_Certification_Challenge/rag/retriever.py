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
from rag.prompts import RISKHALO_SYSTEM_PROMPT

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
        print(f"Retrieved top {self.top_k} documents from ChromaDB :: documents length: {len(documents)}")
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

        system_prompt = RISKHALO_SYSTEM_PROMPT

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