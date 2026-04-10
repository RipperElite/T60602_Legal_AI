import hashlib
import os
from cryptography.fernet import Fernet


# ==========================================================
# 1. DIGITAL FINGERPRINT (SHA-256 HASH)
# ==========================================================
image_path="/image/image.jpg"
def generate_fingerprint(image_path):
    """
    Generate a SHA-256 hash fingerprint for the given image file.

    Args:
        image_path (str): Path to the image file

    Returns:
        str: Hexadecimal SHA-256 hash (digital fingerprint)
    """
    with open(image_path, 'rb') as file:
        file_data = file.read()

    fingerprint = hashlib.sha256(file_data).hexdigest()
    return fingerprint


# ==========================================================
# 2. KEY GENERATION (FERNET SYMMETRIC KEY)
# ==========================================================
def generate_key(key_path='encryption_key.key'):
    """
    Generate and save a Fernet encryption key.

    Args:
        key_path (str): File path to save the key

    Returns:
        bytes: Generated encryption key
    """
    key = Fernet.generate_key()

    with open(key_path, 'wb') as key_file:
        key_file.write(key)

    return key


def load_key(key_path='encryption_key.key'):
    """
    Load an existing Fernet key from file.

    Args:
        key_path (str): Path to the saved key

    Returns:
        bytes: Loaded encryption key
    """
    with open(key_path, 'rb') as key_file:
        return key_file.read()


# ==========================================================
# 3. SECURE STORAGE (ENCRYPT & STORE)
# ==========================================================
def secure_store(image_path, key):
    """
    Encrypt an image file and store it securely.

    Args:
        image_path (str): Path to image
        key (bytes): Fernet encryption key

    Returns:
        str: Path of encrypted file
    """
    # Read image data
    with open(image_path, 'rb') as file:
        data = file.read()

    # Encrypt data
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    # Ensure secure vault exists
    os.makedirs('secure_vault', exist_ok=True)

    # Create output file name
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    encrypted_path = os.path.join('secure_vault', name + '.bin')

    # Save encrypted file
    with open(encrypted_path, 'wb') as file:
        file.write(encrypted_data)

    return encrypted_path


# ==========================================================
# 4. LIVE DEMO BLOCK (FOR HACKATHON)
# ==========================================================

def find_first_uploaded_image(search_dirs, extensions=None):
    """
    Find the first image file in the supplied directories.

    Args:
        search_dirs (list[str]): Directories to scan for image files
        extensions (list[str], optional): Valid image file extensions

    Returns:
        str | None: Path to the first matching image, or None if not found
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

    for directory in search_dirs:
        if not os.path.isdir(directory):
            continue

        for file_name in os.listdir(directory):
            _, ext = os.path.splitext(file_name)
            if ext.lower() in extensions:
                return os.path.join(directory, file_name)
    return None


if __name__ == "__main__":
    print("\n=== DIGITAL EVIDENCE SECURITY DEMO ===\n")

    dataset_directories = [
        os.path.join(os.getcwd(), 'CASIA2', 'Au'),
        os.path.join(os.getcwd(), 'CASIA2', 'Tp'),
        os.path.join(os.getcwd(), 'image'),
    ]

    test_image_path = find_first_uploaded_image(dataset_directories)

    if test_image_path is None:
        raise FileNotFoundError(
            "No uploaded image found in CASIA2/Au, CASIA2/Tp, or image/. "
            "Please place a test image in one of those folders."
        )

    print("[✔] Using uploaded image for test:", test_image_path)

    fingerprint = generate_fingerprint(test_image_path)
    print(f"[✔] Digital Fingerprint (SHA-256):\n{fingerprint}\n")

    key = generate_key()
    print("[✔] Encryption key generated and saved")

    encrypted_file_path = secure_store(test_image_path, key)
    print(f"[✔] Encrypted evidence stored at: {encrypted_file_path}")