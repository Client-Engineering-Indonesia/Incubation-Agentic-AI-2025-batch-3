from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Set your IBM Cloud API Key and Deployment ID here (or from env vars for security)
API_KEY = "xxx"
URL = "xxx"


class QueryRequest(BaseModel):
    message: str


def get_ibm_token() -> str:
    """Fetch IAM bearer token from IBM Cloud"""
    try:
        token_response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        )
        token_response.raise_for_status()
        return token_response.json()["access_token"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get IAM token: {str(e)}")


@app.post("/ask_watsonx")
def ask_watsonx(req: QueryRequest):
    token = get_ibm_token()

    payload_scoring = {
        "messages": [
            {"role": "user", "content": req.message}
        ]
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(URL, json=payload_scoring, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Watsonx request failed: {str(e)}")
