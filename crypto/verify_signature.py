import base64
import hashlib
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def verify_signature(document_data: bytes, signature_base64: str, signed_package_data: dict, public_key_path: str) -> bool:
    try:
        # Extract values from the signed package
        timestamp = signed_package_data.get('timestamp')
        signature = base64.b64decode(signed_package_data.get('signature', ''))
        
        # Reconstruct the data that was signed
        data_to_verify = {
            "document": base64.b64encode(document_data).decode(),
            "signature_image": signature_base64,
            "timestamp": timestamp
        }
        
        # Create the same hash that was signed
        json_data = json.dumps(data_to_verify, sort_keys=True).encode()
        hash_digest = hashlib.sha256(json_data).digest()
        
        # Load the public key
        with open(public_key_path, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        
        # Verify the signature
        try:
            public_key.verify(
                signature,
                hash_digest,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("✅ Signature verified successfully!")
            return True
        except Exception as e:
            print(f"❌ Signature verification failed: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        return False
