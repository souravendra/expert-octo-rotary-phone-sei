import torch.multiprocessing as mp
from fastapi import FastAPI, HTTPException
from typing import AsyncGenerator
from app.compliance import ComplianceChecker
from app.req_models import ComplianceCheckRequest


async def lifespan(app: FastAPI) -> AsyncGenerator:
    mp.set_start_method("fork", force=True)

    yield


app = FastAPI(lifespan=lifespan)


# instantiating this outside the endpoint loads the model once and and re-uses it
# on subsequent requests so keeping it here
compliance_checker = ComplianceChecker()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/check_compliance/")
async def check_compliance(request: ComplianceCheckRequest):
    policy_website_url = request.policy_website_url.strip()
    target_website_url = request.target_website_url.strip()

    # return {"received": {policy_website_url, target_website_url}}

    if not policy_website_url or not target_website_url:
        raise HTTPException(status_code=400, detail="Both URLs must be provided")

    try:
        answer = await compliance_checker.check_compliance(
            policy_website_url, target_website_url
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during compliance check: {str(e)}"
        )

    return {"result": answer}
