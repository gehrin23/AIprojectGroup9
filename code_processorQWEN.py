import os
import json
import requests


def generate_documentation(code, model_name="qwen2.5-coder:14b"):
    """Generate documentation for a single code file using Qwen model."""
    print(f"Generating documentation using {model_name}...")

    prompt = f"""
    I need comprehensive documentation for the following Python code:

    ```python
    {code}
    ```

    Please provide:
    1. A general description of what the code does
    2. Inline comments explaining key parts and logic
    3. Function/method documentation in proper format (docstrings)
    4. Any important notes about usage, edge cases, or limitations

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


def process_single_file(file_path):
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
            output_dir = "./documented_code"
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
    # Replace with path to a single Python file you want to document
    target_file = "./repos/python_algorithms/neural_network/back_propagation_neural_network.py"

    if not os.path.exists(target_file):
        print(f"File not found: {target_file}")
    else:
        success = process_single_file(target_file)
        if success:
            print("Single file documentation completed successfully.")
        else:
            print("Failed to generate documentation for the file.")