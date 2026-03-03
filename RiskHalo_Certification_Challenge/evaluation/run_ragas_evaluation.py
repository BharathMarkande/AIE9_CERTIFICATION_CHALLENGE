from evaluation.ragas_eval import RiskHaloRagasEvaluator


def print_results(title, results):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    try:
        for metric, value in results.items():
            print(f"{metric}: {round(value, 4)}")
    except Exception:
        print(results)


def main():

    print("\nStarting Simplified RiskHalo RAGAS Evaluation...\n")

    evaluator = RiskHaloRagasEvaluator()

    results = evaluator.evaluate()

    print_results("RAGAS Evaluation Results", results)

    print("\nEvaluation Completed.\n")


if __name__ == "__main__":
    main()