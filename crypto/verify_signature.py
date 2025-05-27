import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

def verify_signature(document_bytes: bytes, signature_base64: str, signed_hash: bytes, public_key_path: str) -> bool:
    signature_bytes = base64.b64decode(signature_base64)
    
    hasher = hashlib.sha256()
    hasher.update(document_bytes)
    hasher.update(signature_bytes)
    digest = hasher.digest()
    
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
    
    try:
        public_key.verify(
            signed_hash,
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
