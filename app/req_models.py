from pydantic import BaseModel


class ComplianceCheckRequest(BaseModel):
    policy_website_url: str
    target_website_url: str
