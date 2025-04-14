import json, os, ast, re, nbformat
from repo_loader import load_config, get_source_files

def extract_snippets(path, ext):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as files:
            content = files.read()
    except:
        return []

    snippets = []

    if ext == '.py':
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    snippet = ast.get_source_segment(content, node)
                    if snippet:
                        snippets.append(snippet.strip())
        except Exception:
            pass

    elif ext == ".java":
        pattern = r"(public|private|protected|abstract)?\s*(class|interface|enum|void|static|[\w<>]+)\s+\w+\s*\([^)]*\)\s*\{"
        matches = re.finditer(pattern, content)
        for match in matches:
            start = match.start()
            snippet = content[start:start+500]
            snippets.append(snippet.strip())

    elif ext == ".css":
        pattern = r"[^{]+\{[^}]+\}"
        matches = re.findall(pattern, content)
        snippets.extend(matches)

    elif ext == ".html":
        tags = re.findall(r"<(script|syle|div|section)[^>]*>.*?</\1>", content, re.DOTALL)
        snippets.extend(tags)

    elif ext == ".ipynb":
        try:
            nb = nbformat.reads(content, as_version=4)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    snippets.append(cell.source)
        except Exception:
            pass

    return snippets

def create_jsonl(output_path="training_data.jsonl"):
    config = load_config()
    files = get_source_files(config['repo_paths'], config['file_types'])

    entries = []

    for file in files:
        ext = os.path.splitext(file)[1]
        snippets = extract_snippets(file, ext)

        for snippet in snippets:
            entry = {
                "prompt": f" Improve comments and clarity in this {ext} code:\n" + snippet,
                "response": snippet
            }
            entries.append(entry)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as files:
            for entry in entries:
                files.write(json.dumps(entry) + "\n")

#this will run the create_jsonl.py file. This file will is used for training purposes. When ran, Ollama will need to
#be running as well. This file trains the Ollama LLM using a .jsonl file since it provides easy formatting and parsing
if __name__ == "__main__":
    create_jsonl()