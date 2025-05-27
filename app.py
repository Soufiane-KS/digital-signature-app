from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from crypto.sign_document import sign_document
from crypto.verify_signature import verify_signature
import json

app = FastAPI()

KEYS_DIR = "keys"
PRIVATE_KEY = os.path.join(KEYS_DIR, "private_key.pem")
PUBLIC_KEY = os.path.join(KEYS_DIR, "public_key.pem")

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/sign")
async def sign(
    document: UploadFile = File(...),
    signature_base64: str = Form(...)
):
    try:
        doc_bytes = await document.read()
        output_path = os.path.join(OUTPUT_DIR, "signed_document.json")
        
        signed_package = sign_document(doc_bytes, signature_base64, PRIVATE_KEY, output_path)
        return JSONResponse(content=signed_package)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signing failed: {str(e)}")


@app.post("/verify")
async def verify(
    document: UploadFile = File(...),
    signature_base64: str = Form(...),
    signed_package: UploadFile = File(...)
):
    try:
        doc_bytes = await document.read()
        signed_package_json = await signed_package.read()
        signed_package_data = json.loads(signed_package_json)

        is_valid = verify_signature(doc_bytes, signature_base64, signed_package_data, PUBLIC_KEY)

        result = {
            "valid": is_valid,
            "timestamp": signed_package_data["timestamp"] if is_valid else None
        }

        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
