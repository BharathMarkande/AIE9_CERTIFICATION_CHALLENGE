from app.parser import TradeParser
from app.feature_engine import FeatureEngine
from app.behavioral_engine import BehavioralEngine
from app.expectancy_engine import ExpectancyEngine
from app.session_summary_builder import SessionSummaryBuilder

from rag.embedder import OpenAIEmbedder
from rag.vector_store import RiskHaloVectorStore

DECLARED_RISK = 2000
FILE_PATH = "data/trade_data.xlsx"


def run_pipeline():

    #Analytics Layer
    parser = TradeParser(FILE_PATH)
    df = parser.parse()

    feature_df = FeatureEngine(df, DECLARED_RISK).run()
    diagnosis = BehavioralEngine(feature_df).run()
    impact = ExpectancyEngine(diagnosis, DECLARED_RISK, len(feature_df)).run()

    #Build Snapshot
    builder = SessionSummaryBuilder(diagnosis, impact, len(feature_df))
    snapshot = builder.run()

    #Embed Narrative
    embedder = OpenAIEmbedder()
    embedding = embedder.embed_text(snapshot["narrative_summary"])

    #Store in Chroma
    vector_store = RiskHaloVectorStore()
    session_id = snapshot["structured_summary"]["session_id"]
    vector_store.add_session(
        session_id=session_id,
        embedding=embedding,
        document=snapshot["narrative_summary"]
    )

    print(f"✅ Session stored successfully in vector database. (session_id: {session_id})")

    # Fetch directly from ChromaDB and print
    fetched = vector_store.collection.get(ids=[session_id])
    print("\n📥 Fetched from ChromaDB:")
    print(f"  Session ID: {fetched['ids'][0]}")
    print(f"  Document:\n  {fetched['documents'][0]}")


if __name__ == "__main__":
    run_pipeline()