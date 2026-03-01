class ExpectancyEngine:
    """
    Converts behavioral distortion into expectancy shifts
    and quantifies financial impact.

    This layer translates psychological inconsistency into economic cost.
    """

    def __init__(self, behavioral_output: dict, declared_risk_per_trade: float, total_trades: int):
        self.behavior = behavioral_output
        self.declared_risk = declared_risk_per_trade
        self.total_trades = total_trades

    # --------------------------------------------------
    # Compute Expectancy
    # --------------------------------------------------
    def compute_expectancy(self):
        """
        Computes expectancy for normal and post-loss states.

        Expectancy (R) = (Win Rate × Avg Win R) + (Loss Rate × Avg Loss R)

        This measures the average R-multiple earned per trade
        under neutral conditions versus emotionally reactive conditions.

        The difference (expectancy_delta) reflects behavioral edge erosion.
        """

        win_rate_normal = self.behavior["win_rate_normal"]
        win_rate_post = self.behavior["win_rate_post"]

        avg_win_normal = self.behavior["avg_win_R_normal"]
        avg_win_post = self.behavior["avg_win_R_post"]

        avg_loss_normal = self.behavior["avg_loss_R_normal"]
        avg_loss_post = self.behavior["avg_loss_R_post"]

        loss_rate_normal = 1 - win_rate_normal
        loss_rate_post = 1 - win_rate_post

        self.expectancy_normal = (
            win_rate_normal * avg_win_normal +
            loss_rate_normal * avg_loss_normal
        )

        self.expectancy_post = (
            win_rate_post * avg_win_post +
            loss_rate_post * avg_loss_post
        )

        self.expectancy_delta = self.expectancy_post - self.expectancy_normal

    # --------------------------------------------------
    # Convert to Financial Impact
    # --------------------------------------------------
    def compute_financial_impact(self):
        """
        Converts expectancy deterioration into estimated monetary impact.

        expectancy_delta (R) x declared_risk_per_trade → rupee change per trade.

        This provides a practical estimate of how much capital
        behavioral distortion costs over the analyzed period.

        The estimate scales by total trades to approximate cumulative impact.
        """

        # Expectancy difference per trade (₹)
        rupee_delta_per_trade = self.expectancy_delta * self.declared_risk

        # Estimate how many trades were post-loss
        # Approximation: use half total trades as post-loss estimate
        estimated_post_trades = self.total_trades * 0.4

        self.economic_impact = rupee_delta_per_trade * estimated_post_trades

    # --------------------------------------------------
    # Simulated Guardrail: Stop After 2 Consecutive Losses
    # --------------------------------------------------
    def simulate_stop_after_2_losses(self):
        """
        Simulates a simple behavioral guardrail intervention:
        stopping trading after two consecutive losses.

        Uses severity score as a proxy for recoverable distortion.

        Estimates how much expectancy and monetary performance
        could improve if emotional escalation were reduced.

        This is a deterministic scenario model, not a prediction.
        """

        severity = self.behavior["severity_score"]

        # Simple deterministic improvement model
        # Higher severity → higher improvement potential
        improvement_factor = min(0.5, severity)

        self.simulated_expectancy_improvement = abs(self.expectancy_delta) * improvement_factor
        self.simulated_rupee_improvement = (
            self.simulated_expectancy_improvement *
            self.declared_risk *
            self.total_trades * 0.4
        )

    # --------------------------------------------------
    # Run Full Engine
    # --------------------------------------------------
    def run(self):
        """
        Executes full financial impact analysis pipeline:

        1. Compute expectancy in normal and post-loss states
        2. Measure expectancy delta (behavioral cost)
        3. Convert R-delta into rupee impact
        4. Simulate guardrail-based improvement

        Returns structured impact metrics used in session summaries
        and downstream reasoning layers.
        """

        self.compute_expectancy()
        self.compute_financial_impact()
        self.simulate_stop_after_2_losses()

        return {
            "expectancy_normal_R": round(self.expectancy_normal, 3),
            "expectancy_post_R": round(self.expectancy_post, 3),
            "expectancy_delta_R": round(self.expectancy_delta, 3),
            "economic_impact_rupees": round(self.economic_impact, 2),
            "simulated_expectancy_improvement_R": round(self.simulated_expectancy_improvement, 3),
            "simulated_rupee_improvement": round(self.simulated_rupee_improvement, 2)
        }