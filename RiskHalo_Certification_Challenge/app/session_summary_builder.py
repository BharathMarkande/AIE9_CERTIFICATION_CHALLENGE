# riskhalo/app/session_summary_builder.py

from datetime import datetime
import uuid


class SessionSummaryBuilder:
    """
    Creates a structured behavioral snapshot for a given analysis session.

    Combines behavioral diagnosis and financial impact into:
    - Structured JSON (machine-readable)
    - Narrative summary (embedding-ready text)
    - Metadata (retrieval filtering)

    It represents a single time-stamped behavioral checkpoint
    in the trader’s performance evolution.
    """

    def __init__(self, behavioral_output: dict, expectancy_output: dict, total_trades: int):
        self.behavior = behavioral_output
        self.expectancy = expectancy_output
        self.total_trades = total_trades

    # --------------------------------------------------
    # Generate Unique Session ID
    # --------------------------------------------------
    def generate_session_id(self):
        """
        Generates a unique identifier for the current analysis session.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_suffix = str(uuid.uuid4())[:8]
        return f"session_{timestamp}_{unique_suffix}"

    # --------------------------------------------------
    # Build Structured Snapshot (JSON)
    # --------------------------------------------------
    def build_structured_summary(self):
        """
        Creates a structured JSON snapshot of the session.

        Combines behavioral classification, distortion metrics,
        expectancy shifts, and financial impact into a single
        machine-readable record.

        This snapshot represents the trader’s behavioral state
        at a specific point in time.
        """

        self.session_id = self.generate_session_id()
        self.timestamp = datetime.now().isoformat()

        self.structured_summary = {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "total_trades": self.total_trades,

            "behavioral_state": self.behavior["behavioral_state"],
            "severity_score": self.behavior["severity_score"],

            "avg_R_normal": self.behavior["avg_R_normal"],
            "avg_R_post": self.behavior["avg_R_post"],

            "R_drop_percent": self.behavior["R_drop_percent"],
            "win_shrink_percent": self.behavior["win_shrink_percent"],
            "loss_expansion_percent": self.behavior["loss_expansion_percent"],

            "expectancy_normal_R": self.expectancy["expectancy_normal_R"],
            "expectancy_post_R": self.expectancy["expectancy_post_R"],
            "expectancy_delta_R": self.expectancy["expectancy_delta_R"],

            "economic_impact_rupees": self.expectancy["economic_impact_rupees"],
            "simulated_rupee_improvement": self.expectancy["simulated_rupee_improvement"]
        }

        return self.structured_summary

    # --------------------------------------------------
    # Convert Snapshot to Narrative Text
    # --------------------------------------------------
    def build_narrative_summary(self):
        """
        Converts structured session metrics into a concise narrative summary.

        The narrative explains:
        - Behavioral state classification
        - Expectancy shift magnitude
        - Financial impact of distortion

        This text is designed for semantic embedding and
        downstream retrieval in the RAG system.
        """
        state = self.behavior["behavioral_state"]
        severity = self.behavior["severity_score"]
        expectancy_delta = self.expectancy["expectancy_delta_R"]
        economic_cost = self.expectancy["economic_impact_rupees"]

        narrative = (
            f"In this session of {self.total_trades} trades, "
            f"the trader was classified as {state} with a severity score of {severity}. "
            f"Expectancy shifted from {self.expectancy['expectancy_normal_R']}R "
            f"under normal conditions to {self.expectancy['expectancy_post_R']}R "
            f"after losses, resulting in a delta of {expectancy_delta}R per trade. "
            f"This behavioral distortion corresponds to an estimated financial impact "
            f"of ₹{economic_cost} over the analyzed period."
        )

        self.narrative_summary = narrative
        return narrative

    # --------------------------------------------------
    # Metadata for Vector DB
    # --------------------------------------------------
    def build_metadata(self):
        """
        Generates metadata for vector database storage.

        Includes key retrieval fields such as:
        - session_id
        - timestamp
        - behavioral_state
        - severity_score
        - total_trades

        Metadata enables hybrid retrieval and filtering
        across historical behavioral snapshots.
        """

        metadata = {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "behavioral_state": self.behavior["behavioral_state"],
            "severity_score": self.behavior["severity_score"],
            "total_trades": self.total_trades
        }

        return metadata

    # --------------------------------------------------
    # Run Full Builder
    # --------------------------------------------------
    def run(self):
        """
        Executes the full session snapshot construction pipeline:

        1. Generate unique session identifier
        2. Build structured summary (JSON)
        3. Generate narrative behavioral summary
        4. Prepare retrieval metadata

        Returns a complete snapshot object ready for
        embedding and vector database storage.
        """

        structured = self.build_structured_summary()
        narrative = self.build_narrative_summary()
        metadata = self.build_metadata()

        return {
            "structured_summary": structured,
            "narrative_summary": narrative,
            "metadata": metadata
        }