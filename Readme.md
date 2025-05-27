# Digital Signature App with Timestamp Verification

## Description

This project is a **secure digital signature backend service** built with **FastAPI** in Python. It allows users to sign documents digitally using hand-drawn signatures captured as base64 images. The system includes a timestamp mechanism to prove when documents were signed, and uses cryptographic algorithms to ensure the integrity and authenticity of both the document and the timestamp. The signature package includes the document hash, the drawn signature, and a secure timestamp, all cryptographically signed together.

---

## Features

- **Document Signing**:
  - Upload any document (PDF, DOC, etc.) for signing
  - Include a drawn signature as base64 image
  - Automatic timestamp generation in UTC
  - Cryptographic signing of document + signature + timestamp
  
- **Security Features**:
  - RSA public/private key encryption
  - SHA-256 hashing
  - Timestamp verification
  - Tamper-proof package format
  
- **Verification System**:
  - Verify document authenticity
  - Validate signature integrity
  - Confirm timestamp authenticity
  - Detect any modifications to the signed package

- **API Integration**:
  - RESTful API with FastAPI
  - Swagger UI documentation
  - Easy frontend integration
  - Async request handling

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/digital-signature-app.git
   cd digital-signature-app
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate RSA keys:
   ```bash
   python generate_keys.py
   ```

## Usage

### Starting the Server

1. Start the FastAPI backend:
   ```bash
   python -m uvicorn app:app --reload
   ```

2. Access the interactive API documentation:
   ```
   http://localhost:8000/docs
   ```

### Signing a Document

Use the `/sign` endpoint with:
- A document file (any format)
- A base64-encoded signature image
- The system will automatically add a UTC timestamp

Example using curl:
```bash
curl -X POST "http://localhost:8000/sign" \
  -F "document=@path/to/document.pdf" \
  -F "signature_base64=your_base64_signature_string" \
  --output signed_package.json
```

The response will include:
- Timestamp of signing
- Cryptographic signature
- Hash algorithm used
- Signed data package

### Verifying a Document

Use the `/verify` endpoint with:
- The original document
- The original base64 signature
- The signed package (JSON file from signing process)

Example using curl:
```bash
curl -X POST "http://localhost:8000/verify" \
  -F "document=@path/to/original_document.pdf" \
  -F "signature_base64=original_base64_signature" \
  -F "signed_package=@path/to/signed_package.json"
```

The response will include:
- Verification status (valid/invalid)
- Original timestamp if valid
- Error details if invalid

## Project Structure

```
digital-signature-app/
├── app.py              # FastAPI application
├── crypto/             # Cryptographic operations
│   ├── sign_document.py    # Signing logic
│   └── verify_signature.py # Verification logic
├── keys/              # RSA key storage
├── input/            # Input documents
├── output/           # Signed packages
└── requirements.txt  # Dependencies
```

## Security Notes

- Keep private keys secure and never share them
- Use HTTPS in production
- Regularly backup signed documents and their packages
- Store timestamps in UTC to avoid timezone issues
- Verify both document content and timestamps during verification

## Integration Tips

1. Frontend Integration:
   - Use multipart/form-data for document uploads
   - Convert drawn signatures to base64
   - Store signed packages securely

2. Production Deployment:
   - Use proper SSL/TLS certificates
   - Implement rate limiting
   - Add authentication if needed
   - Use secure key storage

## License

MIT License

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Blockchain Integration

### Data Structure for Blockchain Storage

The system generates a signed package that can be stored on the blockchain. There are two recommended approaches:

#### 1. Full Storage Approach
Store the complete signed package:
```json
{
  "timestamp": "2025-05-27T20:31:32.491975+00:00",
  "signature": "<base64_encoded_cryptographic_signature>",
  "hash_algorithm": "SHA-256",
  "signed_data": {
    "document": "<base64_encoded_document>",
    "signature_image": "<base64_encoded_handwritten_signature>",
    "timestamp": "2025-05-27T20:31:32.491975+00:00"
  }
}
```

#### 2. Essential Storage Approach
Store only the critical verification data:
```json
{
  "document_hash": "<SHA-256_hash_of_original_document>",
  "signature": "<cryptographic_signature>",
  "timestamp": "<UTC_timestamp>",
  "metadata": {
    "hash_algorithm": "SHA-256",
    "signature_type": "RSA-PSS"
  }
}
```

### Storage Considerations

1. **Full Storage**:
   - Advantages:
     - Complete record on-chain
     - Easier verification process
     - Self-contained proof
   - Disadvantages:
     - Higher storage costs
     - Larger blockchain footprint

2. **Essential Storage**:
   - Advantages:
     - Minimal storage requirements
     - Lower blockchain costs
     - Sufficient for verification
   - Disadvantages:
     - Requires off-chain document storage
     - More complex verification process

### Verification Process

1. **With Full Storage**:
   - Extract data from blockchain
   - Use the `/verify` endpoint with the stored data
   - All information is available on-chain

2. **With Essential Storage**:
   - Retrieve document from off-chain storage
   - Calculate document hash
   - Compare with stored hash
   - Verify signature and timestamp