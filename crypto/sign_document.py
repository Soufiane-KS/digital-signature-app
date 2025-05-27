import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def sign_document(document_bytes: bytes, signature_base64: str, private_key_path: str) -> bytes:
    signature_bytes = base64.b64decode(signature_base64)
    
    hasher = hashlib.sha256()
    hasher.update(document_bytes)
    hasher.update(signature_bytes)
    digest = hasher.digest()
    
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
    
    signed_hash = private_key.sign(
        digest,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signed_hash
