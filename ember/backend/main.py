from fastapi import FastAPI
from trust.engine import generate_trust_report
from trust.metadata import check_token_trust
from trust.jupiter import get_token_metadata, is_token_routable
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scan/{mint_address}")
def scan_token(mint_address: str):
    try:
        return generate_trust_report(mint_address)
    except ValueError as ve:
        return {"error": f"Invalid mint or not found: {ve}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}