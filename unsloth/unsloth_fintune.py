# unsloth/unsloth_finetune.py

from unsloth import FastLlamaModel
from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
import torch
import yaml

# 0. Load config
with open("../config.yaml", "r") as f:   # <- Make sure this path points to AIprojectGroup9/config.yaml
    config = yaml.safe_load(f)

# 1. Load the base model (from config)
model, tokenizer = FastLlamaModel.from_pretrained(
    model_name=config["models"][0],    # Use the first model listed (qwen2.5-coder:14b)
    load_in_4bit=True,
    device_map="auto"
)

# 2. Load your training data
training_data_path = config.get("training_data_path", "../TrainingData/py.jsonl")
dataset = load_dataset("json", data_files=training_data_path)["train"]

# 3. Preprocessing
def format_instruction(sample):
    return {
        "input_ids": tokenizer(
            sample["prompt"],
            truncation=True,
            padding="max_length",
            max_length=2048,
            return_tensors="pt"
        ).input_ids[0],
        "labels": tokenizer(
            sample["response"],
            truncation=True,
            padding="max_length",
            max_length=2048,
            return_tensors="pt"
        ).input_ids[0],
    }

dataset = dataset.map(format_instruction, remove_columns=["prompt", "response"])

# 4. Define training arguments
training_args = TrainingArguments(
    output_dir="./unsloth_output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    logging_steps=10,
    learning_rate=2e-4,
    bf16=True,  # Set to False if GPU doesn't support BF16
    save_total_limit=2,
    save_steps=500,
    num_train_epochs=3,
    report_to="none"
)

# 5. Create Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer
)

# 6. Fine-tune
trainer.train()

# 7. Save adapter
trainer.save_model("./unsloth_output")
