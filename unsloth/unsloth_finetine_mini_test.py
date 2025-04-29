# unsloth/unsloth_finetune_mini_test.py

from unsloth import FastLlamaModel
from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
import yaml

# Load config
with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load the base model
model, tokenizer = FastLlamaModel.from_pretrained(
    model_name=config["models"][0],  # qwen2.5-coder:14b
    load_in_4bit=True,
    device_map="auto"
)

# Load your training data
training_data_path = config.get("training_data_path", "../TrainingData/py.jsonl")
dataset = load_dataset("json", data_files=training_data_path)["train"]

# Use only a very small subset for mini test
small_dataset = dataset.select(range(3))  # Only 3 samples!

# Preprocessing
def format_instruction(sample):
    return {
        "input_ids": tokenizer(
            sample["prompt"],
            truncation=True,
            padding="max_length",
            max_length=512,
            return_tensors="pt"
        ).input_ids[0],
        "labels": tokenizer(
            sample["response"],
            truncation=True,
            padding="max_length",
            max_length=512,
            return_tensors="pt"
        ).input_ids[0],
    }

small_dataset = small_dataset.map(format_instruction, remove_columns=["prompt", "response"])

# Training arguments
training_args = TrainingArguments(
    output_dir="./unsloth_mini_output",
    per_device_train_batch_size=1,      # VERY small batch size
    gradient_accumulation_steps=1,
    learning_rate=2e-4,
    warmup_steps=5,
    logging_steps=1,
    save_steps=5,
    num_train_epochs=1,                 # ONLY 1 epoch
    bf16=False,                         # Safe choice
    report_to="none"
)

# Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=small_dataset,
    args=training_args,
    tokenizer=tokenizer
)

# Fine-tune
trainer.train()

# Save mini output
trainer.save_model("./unsloth_mini_output")

print("✅ Mini fine-tune test completed successfully!")
