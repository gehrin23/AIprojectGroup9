import os
import json
from RepoSift import repo_loader as rl
from collections import defaultdict

PROMPT_TEMPLATES = {
    "py": "Read and learn from this professionally documented Python code on how to properly add docstrings and inline comments.",
    "java": "Read and learn from this professionally documented Java code on how to properly add docstrings and inline comments.",
    "js": "Read and learn from this professionally documented JavaScript code on how to properly add docstrings and inline comments.",
    "html": "Read and learn from this professionally documented HTML code on how to properly add docstrings and inline comments.",
    "css": "Read and learn from this professionally documented CSS code on how to properly add docstrings and inline comments.",
    "ipynb": "Read and learn from this professionally documented Jupyter Notebook code on how to properly add docstrings and inline comments.",
}

def create_training_data(output_dir="./TrainingData/"):
    config = rl.load_config("../config.yaml")
    files = rl.get_source_files(config['repo_paths'], config['file_types'])

    training_data = defaultdict(list)

    for i, filepath in enumerate(files):
        ext = os.path.splitext(filepath)[1].lstrip(".").lower()
        if ext not in PROMPT_TEMPLATES:
            continue

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()

        except Exception:
            continue

        if not content:
            continue

        prompt = PROMPT_TEMPLATES[ext]
        training_data[ext].append({
            "prompt": prompt,
            "response": content
        })

        if i % 500 == 0:
            print(f"Processed {i} of {len(files)} files...")

    os.makedirs(output_dir,exist_ok=True)

    for ext, entries in training_data.items():
        out_file = os.path.join(output_dir, f"{ext}_training.jsonl")
        with open(out_file, "w", encoding="utf-8") as out:
            for entry in entries:
                out.write(json.dumps(entry) + "\n")

        print(f"Saved {len(entries)} entries to {out_file}")


if __name__ == "__main__":
    create_training_data()










