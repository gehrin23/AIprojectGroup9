import os
import json
import requests


def generate_documentation(code, model_name="codellama:7b"):
    """Generate documentation for a single code file using CodeLlama model."""
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


def process_single_file(file_path, model="codellama:7b"):
    """Process a single file and generate documentation for it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        print(f"Processing file: {file_path}")
        print(f"File size: {len(code)} characters")
        print(f"Number of lines: {code.count('\n') + 1}")

        documentation = generate_documentation(code, model_name=model)

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
    # Print current working directory to help with debugging
    print("Current working directory:", os.getcwd())

    # Use the direct file path
    target_file = "C:/Users/John/AIproject/repos/python_algorithms/neural_network/back_propagation_neural_network.py"

    # If the file doesn't exist at the above path, try relative path
    if not os.path.exists(target_file):
        # Try a few alternative paths
        alternative_paths = [
            "./repos/python_algorithms/neural_network/back_propagation_neural_network.py",
            "../repos/python_algorithms/neural_network/back_propagation_neural_network.py",
            "./python_algorithms/neural_network/back_propagation_neural_network.py",
            "python_algorithms/neural_network/back_propagation_neural_network.py"
        ]

        for path in alternative_paths:
            print(f"Trying path: {path}")
            if os.path.exists(path):
                target_file = path
                print(f"Found file at: {path}")
                break

    model_to_use = "codellama:7b"

    if not os.path.exists(target_file):
        print(f"File not found: {target_file}")

        # Ask user for the correct path if file still not found
        user_path = input("Please enter the correct path to the file: ")
        if os.path.exists(user_path):
            target_file = user_path
        else:
            print(f"File still not found: {user_path}")
            exit(1)

    success = process_single_file(target_file, model=model_to_use)
    if success:
        print(f"Single file documentation completed successfully using {model_to_use}.")
    else:
        print(f"Failed to generate documentation for the file using {model_to_use}.")