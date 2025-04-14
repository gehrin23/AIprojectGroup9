import os, json, requests
from RepoSift import repo_loader as rl

def generate_documentation(code, model_name="qwen2.5-coder:14b"):
    """Generate documentation for a single code file using Qwen model."""
    print(f"Generating documentation using {model_name}...")

    prompt = f"""
    I need comprehensive documentation for the following source code:

    ```
    {code}
    ```
    Please provide:
    1. A general description of what the code does
    2. Inline comments explaining key parts and logic to help clarify actions and variables
    3. Function/method/class/interface/enum documentation in proper format (docstring). Ensure to add parameters required, parameters variable name and their types, side effects of 
    method/function, and what the method/function returns (if it returns anything)
    4. Provide any import notes about usage, edge cases, side effects, limitations, or any other import documentation
    5. Do not alter any existing functional code
    6. If a comment already exists, read over it, and determine if it accurately portrays what the method/function/variable is or is doing. 
    7. If comment is inaccurate, adjust the pre-existing comment so that it properly reflects what is happening
    8. A comment can be deemed inaccurate if it being to broad, or using incorrect terminology/jargon. 
    
    Format the output as the original code with added documentation.
    """

    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model_name,
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


def process_repos(file_path):
    """Process a single file and generate documentation for it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        print(f"Processing file: {file_path}")
        print(f"File size: {len(code)} characters")
        print(f"Number of lines: {code.count('\n') + 1}")

        documentation = generate_documentation(code)

        if documentation:
            # Create output filename
            filename = os.path.basename(file_path)
            ext = os.path.split(filename)[1].lstrip('.')
            repo_root = os.path.basename(os.path.dirname(file_path))
            output_dir = os.path.join("..", "well_documented_code", repo_root, ext)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"documented_{filename}")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(documentation)

            print(f"Documentation saved to {output_file}")

            # Display a preview
            print("\nDocumentation Preview:")
            print("-" * 80)
            preview = documentation[:500] + "..." if len(documentation) > 500 else documentation
            print(preview)
            print("-" * 80)

        return True

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


if __name__ == "__main__":
<<<<<<<< HEAD:code_processorQWEN.py
    # Replace with path to a single Python file you want to document
    target_file = "./repos/python_algorithms/neural_network/back_propagation_neural_network.py"
========
    config = rl.load_config()
    source_files = rl.get_source_files(config['repo_paths'], config['file_types'])
>>>>>>>> c7fa8334a1828ca60cfcd66afcec507a73658d26:DocForge/code_processor.py

    print(f"\n Found {len(source_files)} files to document.\n")

    for i, path, in enumerate(source_files):
        print(f"\n[{i+1}/{len(source_files)}] Documenting: {path}")
        success = process_repos(path)
        if not success:
            print("Failed to document this file")