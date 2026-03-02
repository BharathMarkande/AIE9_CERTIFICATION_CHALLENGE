import os
import glob
import traceback

from app.parser import TradeParser
from app.feature_engine import FeatureEngine
from app.behavioral_engine import BehavioralEngine
from app.expectancy_engine import ExpectancyEngine
from app.session_summary_builder import SessionSummaryBuilder
from app.rule_engine import RuleComplianceEngine
from app.config_loader import load_rules_config


from rag.embedder import OpenAIEmbedder
from rag.vector_store import RiskHaloVectorStore
from agents.coach_agent import ask_coach

DECLARED_RISK = 2000
DATA_FOLDER = "data/Weekly_Trade_Data_Uploads"


def process_single_file(file_path, embedder, vector_store):
    """
    Runs full RiskHalo pipeline for a single weekly file
    and stores its summary in ChromaDB.
    """

    print(f"\n Processing file: {file_path}")

    # ----------------------------
    # Analytics Layer
    # ----------------------------
    parser = TradeParser(file_path)
    df = parser.parse()

    feature_df = FeatureEngine(df, DECLARED_RISK).run()
    diagnosis = BehavioralEngine(feature_df).run()

    post_loss_trade_count = int(feature_df["post_loss_flag"].sum())

    impact = ExpectancyEngine(
        diagnosis,
        DECLARED_RISK,
        len(feature_df),
        post_loss_trade_count
    ).run()

    # ==========================================================
    # Rule Compliance Layer
    # ==========================================================
    rules_config = load_rules_config()
    rule_engine = RuleComplianceEngine(feature_df, rules_config)
    rule_results = rule_engine.run()


    # ----------------------------
    # Build Summary Snapshot
    # ----------------------------
    builder = SessionSummaryBuilder(feature_df, diagnosis, impact, rule_results)
    snapshot = builder.run()

    session_id = snapshot["structured_summary"]["session_id"]
    narrative = snapshot["narrative_summary"]
    rule_narrative = snapshot["rule_narrative"]

    full_narrative = narrative.join("\n\n") + "\n\n" + rule_narrative

    print(full_narrative)

    # ----------------------------
    # Embed Narrative
    # ----------------------------
    embedding = embedder.embed_text(full_narrative)

    # ----------------------------
    # Store in ChromaDB with Metadata
    # ----------------------------

    metadata = {
        "behavioral_state": diagnosis["behavioral_state"],
        "severity_score": diagnosis["severity_score"],
        "discipline_score": rule_results["discipline_scores"]["overall_discipline_score"],
        "risk_breach_count": rule_results["violations"]["risk_breach_count"],
        "rr_violation_count": rule_results["violations"]["rr_violation_count"],
        "overtrading_days": rule_results["violations"]["overtrading_days"],
        "daily_loss_breaches": rule_results["violations"]["daily_loss_breaches"],
    }

    vector_store.add_session(
        session_id=session_id,
        embedding=embedding,
        document=full_narrative,
        metadata=metadata
    )

    print(f"Stored session in vector DB: {session_id}")


def run_pipeline():

    # --------------------------------
    # Initialize shared components
    # --------------------------------
    embedder = OpenAIEmbedder()
    vector_store = RiskHaloVectorStore()

    # --------------------------------
    # Find all weekly Excel files (exclude Excel lock files ~$*.xlsx)
    # --------------------------------
    all_xlsx = glob.glob(os.path.join(DATA_FOLDER, "*.xlsx"))
    file_paths = [
        f for f in all_xlsx
        if not os.path.basename(f).startswith("~$")
    ]

    if not file_paths:
        print("No weekly trade files found.")
        return

    print(f"\n Found {len(file_paths)} weekly trade files.")

    # --------------------------------
    # Process each file
    # --------------------------------
    for file_path in file_paths:
        try:
            process_single_file(file_path, embedder, vector_store)
        except Exception as e:
            print(f" Error processing {file_path}: {e}")
            traceback.print_exc()

    print("\n  All weekly files processed successfully.")


# Example coaching queries (optional)
# print(ask_coach("Am I improving over time?"))
# print(ask_coach("Why do traders escalate after losses?"))


if __name__ == "__main__":
    run_pipeline()