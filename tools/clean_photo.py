import sys
import os
import cv2
import numpy as np
from PIL import Image

def clean_photo(input_path="assets/my-photo.png", output_path="assets/photo-ready.png"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    print(f"Loading image from {input_path}...")
    img = Image.open(input_path).convert("RGB")
    w, h = img.size

    # Crop tightly around face and upper body (center crop)
    # The photo is a selfie: face is in upper-center
    crop_left = int(w * 0.22)
    crop_top = int(h * 0.25)
    crop_right = int(w * 0.85)
    crop_bottom = int(h * 0.90)
    
    cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Convert to OpenCV image (BGR)
    cv_img = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR)

    # Convert to Grayscale
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)

    # Convert back to PIL Image
    final_pil = Image.fromarray(equalized)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final_pil.save(output_path)
    print(f"Cleaned photo successfully saved to {output_path}!")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "assets/my-photo.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/photo-ready.png"
    clean_photo(src, out)
