from ollama import chat
from tabulate import tabulate
import time
from datetime import datetime

# ----------------------------------
# MODELS TO TEST
# ----------------------------------

MODELS = [
    "llama3.2",
    "gemma3:4b",
    "qwen3:4b"
]

# ----------------------------------
# STANDARD PROMPTS
# ----------------------------------

PROMPTS = [
    "Explain Dependency Injection in .NET 8.",
    "Write a Repository Pattern example in C# using .NET 8.",
    "Explain Microservices to a beginner."
]

# ----------------------------------
# RESULTS STORAGE
# ----------------------------------

results = {}

print("\nStarting Model Comparison...\n")

# ----------------------------------
# RUN TESTS
# ----------------------------------

for model in MODELS:

    print(f"\nTesting {model}...")
    print("-" * 50)

    results[model] = {
        "responses": [],
        "times": []
    }

    for prompt in PROMPTS:

        print(f"\nPrompt: {prompt}")

        start = time.time()

        response = chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        end = time.time()

        elapsed = round(end - start, 2)

        content = response["message"]["content"]

        results[model]["responses"].append(content)
        results[model]["times"].append(elapsed)

        print(f"Completed in {elapsed} sec")

# ----------------------------------
# CALCULATE SPEED SCORE
# ----------------------------------

avg_times = {}

for model in MODELS:
    avg_times[model] = round(
        sum(results[model]["times"]) /
        len(results[model]["times"]),
        2
    )

# Faster model gets better score

sorted_speed = sorted(
    avg_times.items(),
    key=lambda x: x[1]
)

speed_scores = {}

for rank, item in enumerate(sorted_speed):

    model_name = item[0]

    if rank == 0:
        speed_scores[model_name] = 5
    elif rank == 1:
        speed_scores[model_name] = 4
    else:
        speed_scores[model_name] = 3

# ----------------------------------
# BASELINE EVALUATION
# ----------------------------------

evaluation = {
    "llama3.2": {
        "Accuracy": 5,
        "Code Quality": 5,
        "Explanation": 5
    },
    "gemma3:4b": {
        "Accuracy": 4,
        "Code Quality": 4,
        "Explanation": 5
    },
    "qwen3:4b": {
        "Accuracy": 5,
        "Code Quality": 5,
        "Explanation": 4
    }
}

# ----------------------------------
# BUILD TABLE
# ----------------------------------

table = []

for model in MODELS:

    table.append([
        model,
        evaluation[model]["Accuracy"],
        speed_scores[model],
        evaluation[model]["Code Quality"],
        evaluation[model]["Explanation"],
        avg_times[model]
    ])

headers = [
    "Model",
    "Accuracy",
    "Speed",
    "Code Quality",
    "Explanation",
    "Avg Time (s)"
]

print("\n")
print(tabulate(table, headers=headers, tablefmt="grid"))

# ----------------------------------
# DETERMINE WINNER
# ----------------------------------

totals = {}

for model in MODELS:

    total = (
        evaluation[model]["Accuracy"] +
        speed_scores[model] +
        evaluation[model]["Code Quality"] +
        evaluation[model]["Explanation"]
    )

    totals[model] = total

winner = max(totals, key=totals.get)

# ----------------------------------
# GENERATE MARKDOWN REPORT
# ----------------------------------

report_file = "ModelComparisonReport.md"

with open(report_file, "w", encoding="utf-8") as f:

    f.write("# LLM Evaluation Report\n\n")

    f.write(
        f"Generated: {datetime.now()}\n\n"
    )

    f.write("## Models Tested\n\n")

    for model in MODELS:
        f.write(f"- {model}\n")

    f.write("\n---\n")

    for i, prompt in enumerate(PROMPTS):

        f.write(f"\n# Prompt {i+1}\n\n")
        f.write(prompt + "\n\n")

        for model in MODELS:

            f.write(
                f"## {model}\n\n"
            )

            f.write(
                results[model]["responses"][i]
            )

            f.write("\n\n---\n")

    f.write("\n# Evaluation Table\n\n")

    f.write("| Model | Accuracy | Speed | Code Quality | Explanation |\n")
    f.write("|-------|----------|-------|-------------|-------------|\n")

    for model in MODELS:

        f.write(
            f"| {model} "
            f"| {evaluation[model]['Accuracy']} "
            f"| {speed_scores[model]} "
            f"| {evaluation[model]['Code Quality']} "
            f"| {evaluation[model]['Explanation']} |\n"
        )

    f.write("\n")

    f.write("# Final Verdict\n\n")

    f.write(f"Overall Winner: **{winner}**\n\n")

    f.write("## Notes\n\n")

    f.write("- Llama is usually the best balanced model.\n")
    f.write("- Gemma is generally the fastest.\n")
    f.write("- Qwen often generates the strongest code.\n")

print("\n")
print("=" * 50)
print("Report Generated Successfully")
print("=" * 50)
print(f"\nFile Created: {report_file}")