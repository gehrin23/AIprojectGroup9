import ollama
import time

# List available models
models = ollama.list()
print("Available models:")
for model in models:
    print(f"- {model}")

# Test the Qwen model with a simple prompt
print("\nTesting Qwen model...")
start_time = time.time()

try:
    response = ollama.generate(model="qwen2.5-coder:14b",
                               prompt="Write a simple Python function to calculate the factorial of a number.",
                               options={"num_ctx": 2048})  # Reduced context window

    elapsed = time.time() - start_time
    print(f"Response received in {elapsed:.2f} seconds")
    print("Model output:")
    print(response['response'])
except Exception as e:
    print(f"Error: {e}")

print("Script completed")