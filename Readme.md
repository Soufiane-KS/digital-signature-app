# Digital Signature App

## Description

This project is a **secure digital signature backend service** built with **FastAPI** in Python. It allows users to sign documents digitally using hand-drawn signatures captured as base64 images. The system hashes and signs the combined document and signature data using cryptographic algorithms to ensure integrity and authenticity. It also supports verifying signed documents.

---

## Features

- User uploads a document (PDF, DOC, etc.) and a drawn signature (base64 image) via API.
- Generates a cryptographic hash of the document and signature.
- Signs the hash with a private RSA key.
- Verifies the authenticity of the signed document.
- Provides a REST API for signing and verifying documents.
- Easy integration with frontend applications.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/digital-signature-app.git
   cd digital-signature-app

2. Create and activate a Python virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate      # On Windows: venv\Scripts\activate

3. Install dependencies:

    ```bash
    pip install -r requirements.txt

## Usage
1. Start the FastAPI backend:

    ```bash
    uvicorn app:app --reload

2. Access the interactive API docs at:

    ```bash
    http://localhost:8000/docs

Use the /sign endpoint to upload a document and a signature (base64 string) to get a signed hash.

Use the /verify endpoint to verify a signed document.

## Testing
You can test the endpoints with curl, Postman, or directly via the Swagger UI.

1. Example with curl to sign:

    ```bash
    curl -X POST "http://localhost:8000/sign" \
    -F "document=@path/to/document.pdf" \
    -F "signature_base64=your_signature_base64_string_here" \
    --output signed_hash.bin
    
## Notes
Make sure to place your RSA private and public keys inside the keys/ directory.

Signed hashes are saved in the output/ folder.

This backend is ready to be integrated with a frontend that captures the user's drawn signature and uploads the document.

## License
MIT License .