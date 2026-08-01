import sys
import os
import numpy as np
from PIL import Image

# Density ramp matching classic ASCII terminal style
GLYPHS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def image_to_ascii(image_path, width=54, aspect_ratio=0.52):
    img = Image.open(image_path).convert("L")
    w_orig, h_orig = img.size
    height = int(width * (h_orig / w_orig) * aspect_ratio)
    
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.array(img_resized)
    
    p_min, p_max = pixels.min(), pixels.max()
    if p_max > p_min:
        pixels = ((pixels - p_min) / (p_max - p_min) * 255).astype(np.uint8)

    lines = []
    ramp_len = len(GLYPHS)
    for y in range(height):
        row_chars = []
        for x in range(width):
            val = pixels[y, x]
            idx = int(val / 255 * (ramp_len - 1))
            idx = max(0, min(ramp_len - 1, idx))
            char = GLYPHS[idx]
            
            if char == " ":
                row_chars.append("&#160;")
            elif char == "<":
                row_chars.append("&lt;")
            elif char == ">":
                row_chars.append("&gt;")
            elif char == "&":
                row_chars.append("&amp;")
            elif char == '"':
                row_chars.append("&quot;")
            elif char == "'":
                row_chars.append("&apos;")
            else:
                row_chars.append(char)
        lines.append("".join(row_chars))
    return lines

def generate_svg(ascii_lines, output_path="portrait.svg", accent_color="#7dcfff", bg_color="#0d1117", border_color="#30363d"):
    font_size = 9.0
    line_height = 10.2
    padding_x = 16
    padding_y = 14
    header_h = 32
    footer_h = 28
    
    width = 440
    height = 460
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 10px; }}')
    svg.append(f'    .header-bg {{ fill: #161b22; rx: 10px; }}')
    svg.append('    .btn-red { fill: #ff5f56; }')
    svg.append('    .btn-yellow { fill: #ffbd2e; }')
    svg.append('    .btn-green { fill: #27c93f; }')
    svg.append(f'    .title {{ font-family: "Fira Code", monospace, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }}')
    svg.append(f'    .ascii-text {{ font-family: "Fira Code", "Courier New", monospace; font-size: {font_size}px; fill: {accent_color}; font-weight: 500; xml:space: preserve; }}')
    svg.append(f'    .prompt {{ font-family: "Fira Code", monospace, sans-serif; font-size: 11px; fill: #7dcfff; font-weight: 600; }}')
    svg.append(f'    .cursor {{ fill: #7dcfff; }}')
    svg.append('  </style>')
    
    # Background & Header
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')
    svg.append(f'  <path d="M 0,10 A 10,10 0 0 1 10,0 L {width-10},0 A 10,10 0 0 1 {width},10 L {width},{header_h} L 0,{header_h} Z" class="header-bg"/>')
    
    # Traffic lights
    svg.append('  <circle cx="18" cy="16" r="5" class="btn-red"/>')
    svg.append('  <circle cx="32" cy="16" r="5" class="btn-yellow"/>')
    svg.append('  <circle cx="46" cy="16" r="5" class="btn-green"/>')
    svg.append(f'  <text x="{width/2}" y="20" text-anchor="middle" class="title">arnav-jain700:~$ cat portrait.asc</text>')
    
    # ASCII lines (Static rendering for 100% GitHub proxy compatibility)
    svg.append('  <g class="ascii-text">')
    y_start = header_h + padding_y
    for i, line in enumerate(ascii_lines):
        y_pos = y_start + (i + 1) * line_height - 2
        if y_pos > height - footer_h - 10:
            break
        svg.append(f'    <text x="{padding_x}" y="{y_pos:.1f}">{line}</text>')
    svg.append('  </g>')
    
    # Bottom prompt line with cursor
    prompt_y = height - 12
    svg.append(f'  <text x="{padding_x}" y="{prompt_y}" class="prompt">arnav-jain700:~$ whoami</text>')
    svg.append(f'  <rect x="{padding_x + 165}" y="{prompt_y - 9}" width="7" height="11" class="cursor"/>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Generated portrait SVG successfully: {output_path}")

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "assets/photo-ready.png"
    out_svg = sys.argv[2] if len(sys.argv) > 2 else "portrait.svg"
    
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found. Running clean_photo.py first...")
        from clean_photo import clean_photo
        clean_photo("assets/my-photo.png", img_path)
        
    ascii_art = image_to_ascii(img_path, width=64)
    generate_svg(ascii_art, output_path=out_svg)
