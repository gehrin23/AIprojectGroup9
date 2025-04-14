from collections import defaultdict
import yaml
import os

def load_config(filename="config.yaml"):
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, filename)

    if not os.path.exists(config_path):
        raise FileNotFoundError("Could not find file")

    with open(config_path, "r") as files:
        return yaml.safe_load(files)


def get_source_files(repos, ftypes):
    all_files = []
    for repo in repos:
        for root, dirs, files, in os.walk(repo):
            for file in files:
                if any(file.endswith(ext) for ext in ftypes):
                    all_files.append(os.path.join(root, file))
    return all_files

#run the repo_loader file. This run will create a text document of the number of identified code files that are specified in the
#config.yaml file
if __name__ == "__main__":
    config = load_config()
    source_files = get_source_files(
        config['repo_paths'],
        config.get('file_types'),
    )

    ext_counts = defaultdict(int)
    for f in source_files:
        ext = os.path.splitext(f)[1]
        ext_counts[ext] += 1

    print(f"\nFound {len(source_files)} total source files\n")

    print(" Breakdown by file type: ")
    for ext, count in ext_counts.items():
        print(f" {ext}: {count}")

    with open("found_files.txt", "w") as out_file:
        for f in source_files:
            out_file.write(f + "\n")