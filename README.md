# Compliance Checker Using Longformer, FastAPI

This project uses the **Longformer** transformer model to check whether texts (like website content) comply with specific policies. The project is designed to automate compliance checks, especially for long documents, by splitting texts into smaller chunks, classifying each chunk as compliant or non-compliant, and providing feedback on specific non-compliant terms.

## Key Components

- **FastAPI**: API framework for handling requests and responses.
- **Longformer Model**: A pre-trained transformer model, fine-tuned for sequence classification to detect compliance.
- **Chunking**: Long texts are divided into smaller chunks to be processed within model limitations.
- **Reporting**: Non-compliant terms are identified and chunks are returned.

## How it Works

1. **Policy Text & Target Text**: The model compares policy guidelines with the target text (e.g., content from a website).
2. **Chunking & Tokenization**: Large texts are split into smaller chunks, tokenized, and processed by the model.
3. **Inference**: The model predicts whether each chunk is compliant or non-compliant based on fine-tuned training data.
4. **Reporting**: Non-compliant chunks are returned for easier identification. (currently chunk size is pretty big so not pinpointing the exact mistakes)

## Usage

1. **Train the Model**: Fine-tune the Longformer model with policy text and labeled examples of compliant/non-compliant text.
2. **Inference**: Run compliance checks via the FastAPI app by sending the policy text and target website content.
3. **Result**: Get a boolean `isCompliant` that tells me if its compliant or not and an array of chunks with results.
