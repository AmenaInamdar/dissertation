from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
import torch

model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# Load model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    load_in_4bit=True, 
    device_map="auto"
)

# PEFT LoRA config
peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, peft_config)

# Load dataset
dataset = load_dataset("json", data_files="data/train_alpaca.jsonl", split="train")

def format(example):
    return tokenizer(
        f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}", 
        truncation=True, padding="max_length", max_length=512
    )

tokenized_dataset = dataset.map(format)

# Training args
args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    output_dir="./output",
    logging_dir="./output/logs",
    logging_steps=10,
    save_strategy="epoch"
)

# Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

# Train!
trainer.train()

# Save model
model.save_pretrained("./output/final_model")
tokenizer.save_pretrained("./output/final_model")
