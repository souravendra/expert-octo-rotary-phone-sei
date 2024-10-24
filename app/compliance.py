import asyncio
from app.scraper import scrape_text
import torch
from transformers import (
    LongformerForSequenceClassification,
    LongformerTokenizer,
)


class ComplianceChecker:
    def __init__(self) -> None:
        self.tokenizer: LongformerTokenizer = LongformerTokenizer.from_pretrained(
            "allenai/longformer-base-4096"
        )
        self.model: LongformerForSequenceClassification = (
            LongformerForSequenceClassification.from_pretrained(
                "allenai/longformer-base-4096"
            )
        )

    async def check_compliance(self, policy_url: str, target_url: str) -> str:
        """Asynchronously checks compliance between the policy and target website."""
        # Asynchronously scrape text from both URLs
        policy_text: str
        target_text: str
        policy_text, target_text = await asyncio.gather(
            scrape_text(policy_url), scrape_text(target_url)
        )

        # Compare and check for compliance
        return await self._compare_compliance(policy_text, target_text)

    async def _compare_compliance(self, policy_text: str, target_text: str) -> dict:
        """Performs compliance check by comparing policy and target texts using the trained model."""

        chunk_size = 4096
        mistakes = []
        is_compliant = True

        summarized_policy = []
        for i in range(0, len(policy_text), chunk_size):
            policy_chunk = policy_text[i : i + chunk_size]
            summarized_policy.append(policy_chunk)

        summarized_policy_text = " ".join(summarized_policy)

        # Iterate through target text in chunks
        for i in range(0, len(target_text), chunk_size):
            chunk = target_text[i : i + chunk_size]

            # Tokenize the input, concatenating the summarized policy and target chunk
            inputs = self.tokenizer(
                summarized_policy_text,
                chunk,
                truncation=True,
                padding="max_length",
                max_length=4096,
                return_tensors="pt",
            )

            # Move inputs to the appropriate device (CPU/GPU)
            inputs = {key: value.to(self.model.device) for key, value in inputs.items()}

            # Perform inference with the trained model
            outputs = self.model(**inputs)

            # Get the logits from the output and perform classification
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=-1).item()

            # If the predicted class is 0 (non-compliant), append to mistakes
            if predicted_class == 0:
                is_compliant = False
                mistakes.append(
                    {"chunk": chunk, "error": "Non-compliant content found"}
                )

        return {
            "isCompliant": is_compliant,
            "mistakes": mistakes,
        }
