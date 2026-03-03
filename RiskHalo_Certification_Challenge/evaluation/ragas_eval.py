from ragas import evaluate, RunConfig
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    LLMContextRecall,
    Faithfulness,
    FactualCorrectness,
    ResponseRelevancy,
    ContextEntityRecall,
    ContextPrecision,
)
from datasets import Dataset
from evaluation.generate_testset import RiskHaloTestsetGenerator
from rag.retriever import RiskHaloRetriever


class RiskHaloRagasEvaluator:
    """
    Simplified RAGAS Evaluation for MVP.

    Uses:
    - Single concatenated raw document
    - 10 persona-driven questions
    - Full metric set
    """

    def __init__(self):
        self.llm = LangchainLLMWrapper(
            ChatOpenAI(model="gpt-4o-mini", temperature=0)
        )

        self.embedding_model = OpenAIEmbeddings()

        self.testset_generator = RiskHaloTestsetGenerator()
        self.retriever = RiskHaloRetriever()

    # --------------------------------------------------
    # Prepare RAGAS Dataset
    # --------------------------------------------------
    def prepare_ragas_dataset(self):
        """
        1. Generate dataset (10 Qs, single raw_doc)
        2. Run full RAG pipeline per question
        3. Build RAGAS-compatible dataset
        """

        dataset = self.testset_generator.generate_dataset()

        ragas_rows = []

        for row in dataset:
            question = row["question"]

            # Run full RAG pipeline
            rag_result = self.retriever.generate(question)
            answer = rag_result["answer"]
            retrieved_contexts = rag_result["retrieved_contexts"]

            ragas_rows.append(
                {
                    "question": question,
                    "contexts": retrieved_contexts,
                    "ground_truth": row["context"],
                    "response": answer,
                }
            )

        ds = Dataset.from_list(ragas_rows)

        # Pretty print with truncation
        df = ds.to_pandas()[["question", "contexts", "ground_truth", "response"]]
        print("\nRagas dataset :: preview")
        print(df)

        return ds

    # --------------------------------------------------
    # Run Evaluation
    # --------------------------------------------------
    def evaluate(self):

        ragas_data = self.prepare_ragas_dataset()

        custom_run_config = RunConfig(timeout=360)

        print(f"Start RAGAS evaluation")
        print(f"evaluate::ragas_data length: {len(ragas_data)}")
        results = evaluate(
            ragas_data,
            metrics=[
                LLMContextRecall(),
                ContextPrecision(),
                ContextEntityRecall(),
                Faithfulness(),
                FactualCorrectness(),
                ResponseRelevancy()
            ],
            llm=self.llm,
            run_config=custom_run_config,
        )

        return results