from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# -------------------------------
# CONFIG: Output Paths
# -------------------------------
KEY_DIR = "secrets"
PRIVATE_KEY_FILE = os.path.join(KEY_DIR, "private_key.pem")
PUBLIC_KEY_FILE = os.path.join(KEY_DIR, "public_key.pem")

# -------------------------------
# Step 1: Create Key Directory
# -------------------------------
os.makedirs(KEY_DIR, exist_ok=True)

# -------------------------------
# Step 2: Generate RSA Key Pair
# -------------------------------
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# -------------------------------
# Step 3: Save Private Key
# -------------------------------
with open(PRIVATE_KEY_FILE, "wb") as priv_file:
    priv_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# -------------------------------
# Step 4: Save Public Key
# -------------------------------
public_key = private_key.public_key()
with open(PUBLIC_KEY_FILE, "wb") as pub_file:
    pub_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print(f" RSA Key Pair Generated:")
print(f" Private Key: {PRIVATE_KEY_FILE}")
print(f" Public Key : {PUBLIC_KEY_FILE}")