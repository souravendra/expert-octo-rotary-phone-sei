# Compliance Checker Using Longformer, FastAPI

This project uses the **Longformer** transformer model to check whether texts (like website content) comply with specific policies. The project is designed to automate compliance checks, especially for long documents, by splitting texts into smaller chunks, classifying each chunk as compliant or non-compliant, and providing feedback on specific non-compliant terms.

## Why Longformer

We chose Longformer for this project because it is specifically designed to handle long documents more efficiently than standard transformer models. It uses a sliding window attention mechanism, allowing it to process long sequences (up to 4096 tokens or more) without the memory and computational overhead typical of full self-attention models like BERT. This makes it ideal for tasks involving large text inputs, such as compliance checking across extensive documents or website content, where understanding the broader context is crucial. Also it can be run locally on my system without issue.

## Brief Summary

- First scrape the target website urls and retrieve the text content
- Divide both into chunks, starting by summarizing the policy
- Now against the summarized policy, start validating every chunk of target website text
- if any chunk is found to be non-compliant, consider the whole website to be non-compliant
- Selected Longformer because I can run it locally and also it has a decent context window


## Corners Cut

- Didn't scan all subdomains
- Didn't train a cloud model (didnt want to exceed an API limit), ran Longformer locally
- Didn't train on a larger dataset which would perhaps catch more nuances
- Didn't optimise the report so it would highlight the exact term that was causing the problem

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


## Actual Request & Response

```json
{
    "policy_website_url": "https://docs.stripe.com/treasury/marketing-treasury",
    "target_website_url": "https://mercury.com"
}
```

```json
{
    "result": {
        "isCompliant": false,
        "mistakes": [
            {
                "chunk": "Online Business Banking For Startups | Simplified Financial Workflows Products Resources About Pricing Log In Log In Open Account Log In Log In Open Account Open Menu Products Resources About Pricing  
                 --- truncated ----
                achieving PMF from AMAs. I highly recommend it. Ch",
                "error": "Non-compliant content found"
            },
            {
                "chunk": "arles Meyer Founder , My Better AI Building trust as a finance leader Read the Story Carolynn Levy, inventor of the SAFE Read the Story Sending international wires through SWIFT Read the Story Pricing 
                 --- truncated ---
                FDIC-insured bank . Banking services provided by Choice Financial Group , Column N.A. , and Evolve Bank & Trust , Members FDIC. Deposit insurance covers the failure of an insured bank.",
                "error": "Non-compliant content found"
            }
        ]
    }
}
```