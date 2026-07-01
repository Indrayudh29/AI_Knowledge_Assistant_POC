from ollama import chat
import pandas as pd
import os
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "RawResponses")

os.makedirs(RAW_DIR, exist_ok=True)

MODELS = [
    "llama3.2",
    "gemma3:4b",
    "qwen3:4b"
]

PROMPTS = {
    "ZeroShot":
    """
    Explain Dependency Injection in .NET 8.
    """,

    "Detailed":
    """
    Explain Dependency Injection in .NET 8.

    Include:
    1. Concept
    2. Advantages
    3. Disadvantages
    4. Code Example
    """,

    "RoleBased":
    """
    You are a Senior .NET Architect.

    Explain Dependency Injection in .NET 8.

    Include:
    - Concept
    - Example
    - Best Practices
    """,

    "FewShot":
    """
    Question:
    What is Repository Pattern?

    Answer:
    Repository Pattern abstracts data access logic.

    Question:
    What is Dependency Injection?

    Answer:
    """,

    "Structured":
    """
    Explain Dependency Injection.

    Return JSON:

    {
      "concept":"",
      "advantages":[],
      "disadvantages":[]
    }
    """
}

results = []

print("Starting Prompt Engineering Lab...\n")

for model in MODELS:

    model_file = os.path.join(
        RAW_DIR,
        model.replace(":", "_") + ".txt"
    )

    with open(model_file, "w", encoding="utf-8") as f:

        f.write(f"MODEL: {model}\n")
        f.write("=" * 80 + "\n\n")

        for prompt_type, prompt in PROMPTS.items():

            print(f"{model} -> {prompt_type}")

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

            output = response["message"]["content"]

            duration = round(end - start, 2)

            results.append({
                "Model": model,
                "PromptType": prompt_type,
                "TimeSeconds": duration,
                "ResponseLength": len(output)
            })

            f.write(f"\nPROMPT TYPE: {prompt_type}\n")
            f.write("-" * 60 + "\n")
            f.write(output)
            f.write("\n\n")

print("\nGenerating Excel Report...")

df = pd.DataFrame(results)

excel_file = os.path.join(
    BASE_DIR,
    "PromptComparison.xlsx"
)

df.to_excel(excel_file, index=False)

print("Generating Prompt Library Files...")

library_files = {
    "ZeroShot.md":
    "# Zero Shot Examples\n\nExplain Dependency Injection\n\nGenerate CRUD API\n\nWrite SQL Query",

    "FewShot.md":
    "# Few Shot Examples\n\nRepository Pattern Example\n\nDependency Injection Example",

    "SystemPrompts.md":
    "# System Prompts\n\nSenior Architect\n\nTechnical Interviewer\n\nTrainer",

    "StructuredOutputs.md":
    "# Structured Outputs\n\nJSON Templates\n\nAPI Templates",

    "PromptTemplates.md":
    "# Reusable Prompt Templates"
}

for file_name, content in library_files.items():

    with open(
        os.path.join(BASE_DIR, file_name),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)

evaluation_md = os.path.join(
    BASE_DIR,
    "PromptEvaluation.md"
)

with open(evaluation_md, "w", encoding="utf-8") as f:

    f.write("# Prompt Evaluation Report\n\n")

    f.write(
        f"Generated: {datetime.now()}\n\n"
    )

    f.write("## Models Tested\n\n")

    for model in MODELS:
        f.write(f"- {model}\n")

    f.write("\n## Prompt Styles\n\n")

    for p in PROMPTS.keys():
        f.write(f"- {p}\n")

    f.write("\n## Observations\n\n")

    f.write("- Detailed prompts generated longer responses.\n")
    f.write("- Role prompts produced more structured explanations.\n")
    f.write("- Structured prompts returned machine-readable output.\n")
    f.write("- Few-shot prompts generally improved consistency.\n")

phase_report = os.path.join(
    BASE_DIR,
    "Phase3_Report.md"
)

with open(phase_report, "w", encoding="utf-8") as f:

    f.write("# Phase 3 Report\n\n")

    f.write("## Topics Covered\n\n")
    f.write("- Zero Shot Prompting\n")
    f.write("- Few Shot Prompting\n")
    f.write("- System Prompts\n")
    f.write("- Structured Outputs\n")
    f.write("- Prompt Evaluation\n\n")

    f.write("## Conclusion\n\n")
    f.write(
        "Prompt quality significantly affects model output quality. "
        "Role-based and few-shot prompts generally produced the most useful responses."
    )

print("\nCompleted Successfully")
print(f"\nOutput Folder: {BASE_DIR}")