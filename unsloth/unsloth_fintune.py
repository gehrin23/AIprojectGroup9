# unsloth/unsloth_finetune.py

from unsloth import FastLanguageModel  # or FastLlamaModel if you prefer
from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from peft import get_peft_model, LoraConfig
import torch
import yaml

# Load config
with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=config["models"][0],
    load_in_4bit=True,
    device_map="auto"
)

# Add LoRA adapter (required for 4bit fine-tuning)
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # adjust if needed
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Load dataset
training_data_path = config.get("training_data_path", "../TrainingData/py.jsonl")
dataset = load_dataset("json", data_files=training_data_path)["train"]

# Tokenize
def format_instruction(sample):
    return {
        "input_ids": tokenizer(sample["prompt"], truncation=True, padding="max_length", max_length=2048).input_ids,
        "labels": tokenizer(sample["response"], truncation=True, padding="max_length", max_length=2048).input_ids
    }

dataset = dataset.map(format_instruction, remove_columns=["prompt", "response"])

# Training arguments
training_args = TrainingArguments(
    output_dir="./unsloth_output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    logging_steps=10,
    learning_rate=2e-4,
    bf16=True,
    save_total_limit=2,
    save_steps=500,
    num_train_epochs=3,
    report_to="none",
    remove_unused_columns=False  # <- important!
)

# Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer
)

# Train
trainer.train()

# Save
trainer.save_model("./unsloth_output")
