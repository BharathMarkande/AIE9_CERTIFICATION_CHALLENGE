# AIE09 Certification Challenge - RiskHalo - A Behavioral Risk Intelligence Engine for Intraday Traders

##✅ Deliverables

### Task 1: Problem, Audience and Scope

1. Write a succinct 1-sentence description of the problem
Retail intraday traders frequently underperform not due to flawed strategies, but because emotional decision-making disrupts disciplined risk management - leading to overtrading, revenge trading, premature profit-taking and failure to cut losses according to predefined rules.

2. Write 1-2 paragraphs on why this is a problem for your specific user
**RiskHalo** targets **Indian F&O intraday retail traders** - a segment where regulatory data from SEBI ((Securities and Exchange Board of India)) indicates that nearly 95% of participants incur losses, with approximately ₹1.8 lakh crore ($2.2 trillion USD) lost over the past three years. This reflects a structural execution problem rather than isolated trading mistakes.

A significant portion of retail traders struggle to consistently follow predefined risk rules. Despite consuming large amounts of market content and strategy material, they lack structured feedback on their execution behavior. Emotional responses such as overtrading, revenge trading, fear of missing out and premature profit-taking frequently override disciplined risk management. Without a systematic trading journal or visibility into recurring loss patterns, traders are unable to diagnose **behavioral distortions** and end up repeating the same execution errors, **leading to rapid drawdowns and eventual capital erosion**.

Beyond financial loss, the psychological impact is substantial. Repeated intraday losses increase stress and impulsivity, often pushing traders to trade more aggressively in an attempt to recover losses, further compounding risk. In an environment where most retail participants lose money, the absence of tools focused on behavioral discipline, risk containment and downside control creates a structural disadvantage. This makes emotional execution failure, rather than strategy selection - one of the primary drivers of trader attrition.

This is a problem worth solving because capital loss driven by emotional and undisciplined execution is the leading cause of retail trader churn in the F&O market.

![Behavioral Pattern](deliverables/images/behavioral_pattern.png)

3. Create a list of questions or input-output pairs that you can use to evaluate your application
**Evaluation questions** - this will later form the RAGAS evaluation dataset
| Input | Expecte Output |
|-------|----------------|
|Why do my losses increase after a losing trade?|ystem identifies whether LOSS_ESCALATION exists, references post-loss loss expansion metrics, and explains if risk increases conditionally after losses.|
|Is my behavior unstable after red days?|System evaluates behavioral_state and severity score, determines whether execution degrades post-loss, and states if instability is statistically supported.|
|Am I cutting profits too early?|System evaluates behavioral_state and severity score, determines whether execution degrades post-loss, and states if instability is statistically supported.|
|How is my R:R affecting long-term results?|System explains relationship between average R, expectancy, and win/loss size balance; highlights if low R on winners is suppressing profitability.|
|I follow rules but still lose. Why?|System distinguishes between behavioral stability and structural negative expectancy; clarifies that discipline does not guarantee profitability if edge is weak.|
|Are my winners too small?|System analyzes average win R and minimum R:R compliance; identifies whether profit compression exists.|
|Am I improving over time?|System compares severity, expectancy, and discipline scores across sessions and determines if trends show improvement, deterioration, or stability.|
|Is my recovery behavior healthy?|System evaluates ADAPTIVE_RECOVERY vs LOSS_ESCALATION and determines whether performance improves or deteriorates after losses.|
|When was my severity highest?|System identifies the session with the maximum severity_score and reports the corresponding behavioral_state.|
|When did expectancy drop most?|System compares expectancy_delta across sessions and identifies the session with the largest negative shift.|
|Am I improving compared to previous sessions?|System compares expectancy_delta across sessions and identifies the session with the largest negative shift.|
|Are wins shrinking after losses?|Win shrink %|
|Is trader stable under pressure?|STABLE/ADAPTIVE/CONTRACTION|



