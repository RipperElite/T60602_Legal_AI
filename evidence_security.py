"""
Digital Evidence Security Module
================================
Provides SHA-256 fingerprinting, file encryption, and Error Level Analysis (ELA) for digital evidence tampering detection.
"""

import hashlib
import os
from cryptography.fernet import Fernet
from PIL import Image, ImageChops, ImageEnhance
from PIL import ExifTags

def extract_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return {"Status": "No EXIF metadata found (Likely stripped or screenshot)."}
            
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            # Only grab readable text data, skip heavy binary data
            if isinstance(value, (str, int, float)): 
                metadata[tag] = value
        return metadata
    except Exception as e:
        return {"Error": "Could not extract metadata."}

def generate_sha256(file_path):
    """
    Generate a SHA-256 hash fingerprint for a given file.
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

def encrypt_file(file_path, key):
    """
    Encrypt a file using Fernet symmetric encryption and save to 'vault' folder.
    """
    with open(file_path, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    os.makedirs('vault', exist_ok=True)

    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    encrypted_path = os.path.join('vault', name + '.enc')

    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)

def initialize_key(key_path='encryption_key.key'):
    """
    Generate and save a Fernet encryption key.
    """
    key = Fernet.generate_key()

    with open(key_path, 'wb') as key_file:
        key_file.write(key)

    return key

def load_key(key_path='encryption_key.key'):
    """
    Load an existing Fernet key from file.
    """
    with open(key_path, 'rb') as key_file:
        return key_file.read()

def get_ela_image(image_path, quality=90):
    """
    Perform Error Level Analysis (ELA) on an image by comparing it to a JPEG compressed version.
    """
    original = Image.open(image_path).convert('RGB')

    temp_path = 'temp.jpg'
    original.save(temp_path, 'JPEG', quality=quality)

    compressed = Image.open(temp_path)

    ela = ImageChops.difference(original, compressed)
    
    # Enhance the difference so it is visible
    extrema = ela.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    ela = ImageEnhance.Brightness(ela).enhance(scale)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return ela

from PIL import ExifTags

def extract_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return {"Status": "No EXIF metadata found (Likely stripped or screenshot)."}
            
        metadata = {}
        for tag_id, value in exif_data.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            # Only grab readable text data, skip heavy binary data
            if isinstance(value, (str, int, float)): 
                metadata[tag] = value
        return metadata
    except Exception as e:
        return {"Error": "Could not extract metadata."}