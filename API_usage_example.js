   // 1. Generate Keys for a User (one-time setup)
   const generateKeys = async (userId) => {
     const response = await fetch(`/users/${userId}/keys`, {
       method: 'POST'
     });
     return await response.json();
   };

   // 2. Sign a Document
   const signDocument = async (userId, document, signature) => {
     const formData = new FormData();
     formData.append('user_id', userId);
     formData.append('document', document);
     formData.append('signature_base64', signature);

     const response = await fetch('/sign', {
       method: 'POST',
       body: formData
     });
     return await response.json();
   };

   // 3. Verify a Signature
   const verifySignature = async (document, signedPackage, signature) => {
     const formData = new FormData();
     formData.append('document', document);
     formData.append('signed_package', new Blob([JSON.stringify(signedPackage)]));
     formData.append('signature_base64', signature);

     const response = await fetch('/verify', {
       method: 'POST',
       body: formData
     });
     return await response.json();
   };