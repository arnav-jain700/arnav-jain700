import sys
import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def clean_photo(input_path="assets/my-photo.png", output_path="assets/photo-ready.png"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    print(f"Loading image from {input_path}...")
    img = Image.open(input_path).convert("RGB")
    w, h = img.size

    # Auto crop bounds focusing on the central subject
    crop_left = int(w * 0.10)
    crop_top = int(h * 0.05)
    crop_right = int(w * 0.90)
    crop_bottom = int(h * 0.95)
    cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Convert to numpy array
    arr = np.array(cropped, dtype=np.float32)

    # 1. Background removal / thresholding to white background
    # Estimate background color from outer border samples
    top_border = arr[:int(h*0.1), :]
    bottom_border = arr[-int(h*0.1):, :]
    left_border = arr[:, :int(w*0.1)]
    right_border = arr[:, -int(w*0.1):]
    border_pixels = np.vstack([
        top_border.reshape(-1, 3),
        bottom_border.reshape(-1, 3),
        left_border.reshape(-1, 3),
        right_border.reshape(-1, 3)
    ])
    bg_color = np.median(border_pixels, axis=0)

    # Compute Euclidean distance of each pixel to estimated background color
    dist = np.linalg.norm(arr - bg_color, axis=2)
    
    # Also evaluate lightness for bright backgrounds
    gray_arr = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    
    # Create background mask (true for background)
    bg_threshold = np.percentile(dist, 40)
    bg_mask = (dist < bg_threshold) | (gray_arr > 220)

    # Set background pixels to solid white (255, 255, 255)
    arr[bg_mask] = [255.0, 255.0, 255.0]

    # 2. Convert to PIL Grayscale & Even out lighting
    pil_img = Image.fromarray(arr.astype(np.uint8)).convert("L")
    
    # Equalize subject lighting
    # Mask out pure white background for contrast calculation
    np_gray = np.array(pil_img)
    subject_pixels = np_gray[np_gray < 250]
    
    if len(subject_pixels) > 0:
        p_low, p_high = np.percentile(subject_pixels, 5), np.percentile(subject_pixels, 95)
        if p_high > p_low:
            # Stretch contrast on subject
            stretched = np.clip((np_gray - p_low) * (255.0 / (p_high - p_low)), 0, 255).astype(np.uint8)
            # Re-apply pure white background
            stretched[np_gray >= 250] = 255
            pil_img = Image.fromarray(stretched)

    # Mild contrast & sharpness enhancement
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.25)
    pil_img = ImageEnhance.Sharpness(pil_img).enhance(1.3)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    pil_img.save(output_path)
    print(f"Cleaned photo with even lighting and white background saved to {output_path}!")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "assets/my-photo.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/photo-ready.png"
    clean_photo(src, out)
