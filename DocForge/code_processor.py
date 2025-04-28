import os, json, requests
from RepoSift import repo_loader as rl
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from prompt_builder import *

PROMPT_METHODS = {
    "chain": chain_of_thought_prompt,
    "few": few_shot_prompt,
    "self": self_critique_prompt,
    "rubric": rubric_prompt,
}

# Utility to clean file names
def safe_filename(name):
    return name.replace(":", "_").replace("/", "_").replace("\\", "_")

# Generate documented code
def generate_documentation(code, model, prompt_method):

    print(f"Generating new comments and documentation using {model} with {prompt_method} prompting. . . ")

    prompt = PROMPT_METHODS[prompt_method](code)

    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_ctx": 4096
            }
        }

        response = requests.post(url, json=payload, stream=True)

        print("Receiving documentation...")
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line.decode('utf-8'))
                if 'response' in json_response:
                    chunk = json_response['response']
                    full_response += chunk
                    print(".", end="", flush=True)

                if json_response.get('done', False):
                    break

        print("\nDocumentation generation completed.")
        return full_response

    except Exception as e:
        print(f"Error generating documentation: {e}")
        return None

# Generates an English onboarding summary
def generate_summary_documentation(code, model):
    print(f"Generating onboarding summary using {model}...")

    prompt = f"""
        You are an expert technical writer.
        
        Given the following source code (which already includes clear docstrings and 
        inline comments), write a professional onboarding document in English that 
        explains: 
        
            1. The overall purpose of the file
            2. Key functions/methods/classes and what they do
            3. Important variables and their usage
            4. Design patterns, libraries, or external dependencies used
            5. How this file connects to the larger project
            6. Any special logic, edge cases, or clever design choices
        
        DO NOT output the code.
        
        Write a clear, readable structured explanation in full English paragraphs. 
        
        Here is the code {code}.
        """

    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
            "num_ctx": 4096
            }
        }

        response = requests.post(url, json=payload, stream=True)
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line.decode('utf-8'))
                if 'response' in json_response:
                    chunk = json_response['response']
                    full_response += chunk
                    print(".", end="", flush=True)

                if json_response.get('done', False):
                    break

        print("\nSummary generation completed.")
        return full_response

    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

# Process each repo file
def process_repos(file_path, model_name, prompt_method, summarizer_model):
    """Process a single file and generate documentation for it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        print(f"Processing file: {file_path}")
        print(f"File size: {len(code)} characters")
        print(f"Number of lines: {code.count('\n') + 1}")

        # Step 1: Clean code generation
        documented_code = generate_documentation(code, model_name, prompt_method)

        if documented_code:
            filename = os.path.basename(file_path)
            project_name = os.path.basename(os.path.dirname(file_path))
            output_dir = os.path.join("..", "well_documented_projects", safe_filename(model_name), project_name)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"documented_{filename}")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(documented_code)

            print(f"Documented code saved to {output_file}")

            # Step 2: Summarization pass
            onboarding_summary = generate_summary_documentation(documented_code, summarizer_model)

            if onboarding_summary:
                pdf_name = f"{os.path.splitext(filename)[0]}_summary.pdf"
                pdf_path = os.path.join(output_dir, pdf_name)
                title = f"Onboarding Summary: {filename}"
                pdf(onboarding_summary, pdf_path, title)
                print(f"Onboarding PDF saved to {pdf_path}")
        return True

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


def pdf(summary, out, title):
    can = canvas.Canvas(out, pagesize=LETTER)
    width, height = LETTER
    margin = 0.75 * inch
    line_height = 14

    can.setFont("Helvetica-Bold", 16)
    can.drawString(margin, height - margin, title)

    can.setFont("Courier", 12)
    y = height - margin - 30

    for line in summary.splitlines():
        if y < margin:
            can.showPage()
            can.setFont("Courier", 12)
            y = height - margin
        can.drawString(margin, y, line[:120])
        y -= line_height

    can.save()
    print(f"{title} saved to {out}")

# Main Driver
if __name__ == "__main__":
    config = rl.load_config("../config.yaml")
    source_files = rl.get_source_files(config['repo_paths'], config['file_types'])
    prompt_method = config['prompt_method']
    summarizer_model = config['summarizer_model']

    print(f"\n Found {len(source_files)} files to document.\n")

    for mod in config['models']:
        print(f"\nStarted with model: {safe_filename(mod)}")
        for i, path, in enumerate(source_files):
            print(f"\n[{i + 1}/{len(source_files)}] Documenting: {path}")
            success = process_repos(path, mod, prompt_method, summarizer_model)
            if not success:
                print("Failed to document this file")
