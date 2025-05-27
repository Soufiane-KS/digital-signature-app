import base64
import hashlib
import json
from datetime import datetime, timezone
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path

def sign_document(document_data: bytes, signature_base64: str, private_key_path: str, output_path: str):
    timestamp = datetime.now(timezone.utc).isoformat()

    data_to_sign = {
        "document": base64.b64encode(document_data).decode(),
        "signature_image": signature_base64,
        "timestamp": timestamp
    }

    json_data = json.dumps(data_to_sign, sort_keys=True).encode()
    hash_digest = hashlib.sha256(json_data).digest()

    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    signature = private_key.sign(
        hash_digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    signed_package = {
        "timestamp": timestamp,
        "signature": base64.b64encode(signature).decode(),
        "hash_algorithm": "SHA-256",
        "signed_data": data_to_sign
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(signed_package, f, indent=2)

    print("Document signed and saved with timestamp.")
    return signed_package
