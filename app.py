from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from crypto.sign_document import sign_document
from crypto.verify_signature import verify_signature

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

        signed_hash = sign_document(doc_bytes, signature_base64, PRIVATE_KEY)

        output_path = os.path.join(OUTPUT_DIR, "signed_hash.bin")
        with open(output_path, "wb") as f:
            f.write(signed_hash)

        return FileResponse(output_path, filename="signed_hash.bin")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signing failed: {str(e)}")


@app.post("/verify")
async def verify(
    document: UploadFile = File(...),
    signature_base64: str = Form(...),
    signed_hash: UploadFile = File(...)
):
    try:
        doc_bytes = await document.read()
        signed_hash_bytes = await signed_hash.read()

        is_valid = verify_signature(doc_bytes, signature_base64, signed_hash_bytes, PUBLIC_KEY)

        return JSONResponse(content={"valid": is_valid})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
