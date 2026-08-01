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
    img = Image.open(input_path).convert("RGBA")

    # Step 1: Crop center/subject region if image is large
    w, h = img.size
    # Focus on upper torso / face area
    crop_box = (int(w * 0.1), int(h * 0.05), int(w * 0.9), int(h * 0.95))
    cropped = img.crop(crop_box)

    # Step 2: Composite onto white background
    white_bg = Image.new("RGBA", cropped.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, cropped).convert("RGB")

    # Step 3: OpenCV LAB CLAHE contrast enhancement
    cv_img = cv2.cvtColor(np.array(composite), cv2.COLOR_RGB2BGR)

    # Equalize L channel
    lab = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    enhanced_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)

    final_pil = Image.fromarray(enhanced_rgb)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final_pil.save(output_path)
    print(f"Cleaned photo successfully saved to {output_path}!")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "assets/my-photo.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/photo-ready.png"
    clean_photo(src, out)
