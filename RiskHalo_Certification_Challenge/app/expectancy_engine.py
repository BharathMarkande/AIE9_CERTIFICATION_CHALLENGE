class ExpectancyEngine:
    """
    Converts behavioral distortion into expectancy shifts
    and quantifies financial impact.

    This layer translates psychological inconsistency into economic cost.
    """

    def __init__(self, behavioral_output: dict, declared_risk_per_trade: float, total_trades: int, post_loss_trade_count: int):
        self.behavior = behavioral_output
        self.declared_risk = declared_risk_per_trade
        self.total_trades = total_trades
        self.post_loss_trade_count = post_loss_trade_count

    # --------------------------------------------------
    # Compute Expectancy
    # --------------------------------------------------
    def compute_expectancy(self):
        """
        Computes expectancy for normal and post-loss states.

        Expectancy (R) = (Win Rate x Avg Win R) + (Loss Rate x Avg Loss R)

        This measures the average R-multiple earned per trade
        under neutral conditions versus emotionally reactive conditions.

        The difference (expectancy_delta) reflects behavioral edge erosion.
        """

        # --- Normal Expectancy ---
        win_rate_normal = self.behavior["win_rate_normal"]
        avg_win_normal = self.behavior["avg_win_R_normal"]
        avg_loss_normal = self.behavior["avg_loss_R_normal"]

        # --- Post-Loss Expectancy ---
        win_rate_post = self.behavior["win_rate_post"]
        avg_win_post = self.behavior["avg_win_R_post"]
        avg_loss_post = self.behavior["avg_loss_R_post"]

        # --- Calculate Rates ---
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
        return self.expectancy_normal, self.expectancy_post, self.expectancy_delta

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

        # Apply Delta Only to Post-Loss Trades, Expectancy shift only applies to post-loss trades
        self.economic_impact = rupee_delta_per_trade * self.post_loss_trade_count


    # --------------------------------------------------
    # Run Full Expectancy Analysi
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

        return {
            "expectancy_normal_R": round(self.expectancy_normal, 2),
            "expectancy_post_R": round(self.expectancy_post, 2),
            "expectancy_delta_R": round(self.expectancy_delta, 2),
            "economic_impact_rupees": round(self.economic_impact, 2),
            "risk_per_trade": self.declared_risk,
            "post_loss_trade_count": self.post_loss_trade_count
        }

# --------------------------------------------------
# Human-Friendly Readable Formatter
# --------------------------------------------------
def format_expectancy_summary(
    expectancy_normal_R: float,
    expectancy_post_R: float,
    expectancy_delta_R: float,
    economic_impact_rupees: float,
    risk_per_trade: float = None
) -> str:
    """
    Formats expectancy metrics into a clean, human-readable summary.
    """

    # Round values for display
    normal_R = round(expectancy_normal_R, 2)
    post_R = round(expectancy_post_R, 2)
    delta_R = round(expectancy_delta_R, 2)
    impact_rupees = round(economic_impact_rupees)

    # Optional rupee conversion per trade
    if risk_per_trade:
        normal_rupees = round(normal_R * risk_per_trade)
        post_rupees = round(post_R * risk_per_trade)

        summary = (
            "Performance Impact\n\n"
            f"Normal trades: {normal_R}R (~₹{normal_rupees} per trade)\n"
            f"After losses: {post_R}R (~₹{post_rupees} per trade)\n"
            f"Behavioral shift: {delta_R}R per trade\n"
            f"Estimated impact over period: ₹{impact_rupees}"
        )
    else:
        summary = (
            "Performance Impact\n\n"
            f"Normal trades: {normal_R}R per trade\n"
            f"After losses: {post_R}R per trade\n"
            f"Behavioral shift: {delta_R}R per trade\n"
            f"Estimated impact over period: ₹{impact_rupees}"
        )

    return summary