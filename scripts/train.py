import torch
from transformers import (
    LongformerForSequenceClassification,
    LongformerTokenizer,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset

# Load tokenizer and model
tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")
model = LongformerForSequenceClassification.from_pretrained(
    "allenai/longformer-base-4096", num_labels=2
)

# Load dataset
dataset = load_dataset("csv", data_files={"train": "train.csv", "test": "test.csv"})


# Tokenize the dataset
def tokenize_function(example):
    return tokenizer(
        example["policy_text"],
        example["target_text"],
        truncation=True,
        padding="max_length",
        max_length=4096,
    )


tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=1,  # Reduce to 1
    per_device_eval_batch_size=1,  # Reduce to 1
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Fine-tune the model
trainer.train()
