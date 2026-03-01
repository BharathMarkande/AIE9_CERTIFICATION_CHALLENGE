# riskhalo/app/behavioral_engine.py

import numpy as np


class BehavioralEngine:
    """
    Diagnoses behavioral distortion by comparing performance
    in emotionally neutral trades versus post-loss trades.

    It quantifies expectancy shifts, win-size shrinkage,
    loss-size expansion, and classifies the trader's
    behavioral state using deterministic thresholds.
    """

    def __init__(self, df):
        self.df = df.copy()

        if "post_loss_flag" not in self.df.columns:
            raise ValueError("FeatureEngine must be run before BehavioralEngine.")

    # --------------------------------------------------
    # Split Groups
    # --------------------------------------------------
    def split_groups(self):
        """
        Segments trades into two behavioral contexts:

        - Normal state: trades not immediately following a loss
        - Post-loss state: trades occurring immediately after a loss

        This separation enables conditional performance comparison,
        which is the foundation of distortion detection.
        """

        self.normal_df = self.df[self.df["post_loss_flag"] == 0]
        self.post_df = self.df[self.df["post_loss_flag"] == 1]

        if len(self.normal_df) < 3 or len(self.post_df) < 3:
            raise ValueError("Not enough trades in one of the groups for reliable analysis.")

    # --------------------------------------------------
    # Compute Group Metrics
    # --------------------------------------------------
    def compute_metrics(self):
        """
        Computes core performance statistics for both groups:

        - Average R (risk-normalized performance)
        - Average winning R
        - Average losing R
        - Win rate

        These metrics allow us to compare whether behavior
        changes after emotional triggers (loss events).
        """

        def group_stats(group):

            avg_R = group["R_proxy"].mean()

            wins = group[group["R_proxy"] > 0]
            losses = group[group["R_proxy"] < 0]

            avg_win_R = wins["R_proxy"].mean() if len(wins) > 0 else 0
            avg_loss_R = losses["R_proxy"].mean() if len(losses) > 0 else 0

            win_rate = len(wins) / len(group) if len(group) > 0 else 0

            return avg_R, avg_win_R, avg_loss_R, win_rate

        (
            self.avg_R_normal,
            self.avg_win_R_normal,
            self.avg_loss_R_normal,
            self.win_rate_normal,
        ) = group_stats(self.normal_df)

        (
            self.avg_R_post,
            self.avg_win_R_post,
            self.avg_loss_R_post,
            self.win_rate_post,
        ) = group_stats(self.post_df)

    # --------------------------------------------------
    # Compute Distortion Metrics
    # --------------------------------------------------
    def compute_distortions(self):
        """
        Calculates percentage change in performance between
        normal trades and post-loss trades.

        Measures:
        - R_drop_percent: overall performance deterioration
        - win_shrink_percent: reduction in average win size
        - loss_expansion_percent: increase in average loss size

        These metrics quantify behavioral distortion magnitude.
        """

        # Avoid division by zero
        self.R_drop_percent = (
            (self.avg_R_normal - self.avg_R_post) / abs(self.avg_R_normal)
            if self.avg_R_normal != 0 else 0
        )

        self.win_shrink_percent = (
            (self.avg_win_R_normal - self.avg_win_R_post) / abs(self.avg_win_R_normal)
            if self.avg_win_R_normal != 0 else 0
        )

        self.loss_expansion_percent = (
            (abs(self.avg_loss_R_post) - abs(self.avg_loss_R_normal)) / abs(self.avg_loss_R_normal)
            if self.avg_loss_R_normal != 0 else 0
        )

    # --------------------------------------------------
    # Classify Behavioral State
    # --------------------------------------------------
    def classify_behavior(self):
        """
        Classifies the trader's behavioral state using
        deterministic thresholds (default 25%).
        
        Possible states:
        - STABLE: No meaningful distortion detected
        - CONFIDENCE_CONTRACTION: Wins shrink after losses
        - LOSS_ESCALATION: Losses expand after losses
        - ADAPTIVE_RECOVERY: Performance improves post-loss
        
        This converts statistical shifts into interpretable states.
        """

        threshold = 0.25  # 25% distortion threshold

        if self.avg_R_post > self.avg_R_normal:
            self.behavioral_state = "ADAPTIVE_RECOVERY"

        elif self.loss_expansion_percent > threshold:
            self.behavioral_state = "LOSS_ESCALATION"

        elif self.win_shrink_percent > threshold:
            self.behavioral_state = "CONFIDENCE_CONTRACTION"

        else:
            self.behavioral_state = "STABLE"

    # --------------------------------------------------
    # Compute Severity Score
    # --------------------------------------------------
    def compute_severity(self):
        """
        Computes a normalized severity score (0-1) representing
        the magnitude of behavioral distortion.

        averages positive distortion components while
        ignoring improvements.

        Higher severity indicates stronger emotional impact
        on execution quality.
        """

        components = [
            max(0, self.R_drop_percent),
            max(0, self.win_shrink_percent),
            max(0, self.loss_expansion_percent),
        ]

        self.severity_score = min(1, np.mean(components))

    # --------------------------------------------------
    # Run Full Diagnosis
    # --------------------------------------------------
    def run(self):
        """
        Executes the full behavioral diagnosis pipeline:
        1. Segment trades by emotional state
        2. Compute group performance metrics
        3. Quantify distortion percentages
        4. Classify behavioral state
        5. Compute severity score
        
        Returns a structured diagnosis dictionary used
        by the Expectancy Engine and downstream agents.
        """

        self.split_groups()
        self.compute_metrics()
        self.compute_distortions()
        self.classify_behavior()
        self.compute_severity()

        return {
            "behavioral_state": self.behavioral_state,
            "severity_score": round(self.severity_score, 3),

            "avg_R_normal": round(self.avg_R_normal, 3),
            "avg_R_post": round(self.avg_R_post, 3),

            "avg_win_R_normal": round(self.avg_win_R_normal, 3),
            "avg_win_R_post": round(self.avg_win_R_post, 3),

            "avg_loss_R_normal": round(self.avg_loss_R_normal, 3),
            "avg_loss_R_post": round(self.avg_loss_R_post, 3),

            "win_rate_normal": round(self.win_rate_normal, 3),
            "win_rate_post": round(self.win_rate_post, 3),

            "R_drop_percent": round(self.R_drop_percent, 3),
            "win_shrink_percent": round(self.win_shrink_percent, 3),
            "loss_expansion_percent": round(self.loss_expansion_percent, 3),
        }