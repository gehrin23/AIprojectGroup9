# unsloth/unsloth_finetune.py

from unsloth import FastLlamaModel
from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
import torch
import yaml
import os

# Load config.yaml
config_path = os.path.join(os.path.dirname(__file__), "../config.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Load model
model, tokenizer = FastLlamaModel.from_pretrained(
    model_name=config["models"][0],
    load_in_4bit=False,  # CPU => don't quantize
    device_map="cpu"     # explicitly force CPU for Colab CPU
)

# Resolve training data path
training_data_path = config.get("training_data_path", "py_training.jsonl")
print(f"Loading dataset from: {training_data_path}")

# Load dataset
dataset = load_dataset("json", data_files=training_data_path)["train"]

# Tokenization function
def format_instruction(sample):
    return {
        "input_ids": tokenizer(
            sample["prompt"],
            truncation=True,
            padding="max_length",
            max_length=1024,  # lower max length for CPU
            return_tensors="pt"
        ).input_ids[0],
        "labels": tokenizer(
            sample["response"],
            truncation=True,
            padding="max_length",
            max_length=1024,
            return_tensors="pt"
        ).input_ids[0],
    }

# Tokenize dataset
dataset = dataset.map(format_instruction, remove_columns=["prompt", "response"])

# Training args
training_args = TrainingArguments(
    output_dir="./unsloth_output",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=2,
    warmup_steps=10,
    logging_steps=5,
    learning_rate=1e-4,
    bf16=False,   # CPU: disable bfloat16
    save_total_limit=2,
    save_steps=50,
    num_train_epochs=1,
    report_to="none"
)

# Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer
)

# Start training
trainer.train()

# Save model
trainer.save_model("./unsloth_output")
