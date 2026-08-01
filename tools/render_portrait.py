import sys
import os
import numpy as np
from PIL import Image

GLYPHS = " '.,:;~+*xXO#"

def image_to_ascii(image_path, width=64, aspect_ratio=0.55):
    img = Image.open(image_path).convert("L")
    w_orig, h_orig = img.size
    height = int(width * (h_orig / w_orig) * aspect_ratio)
    
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.array(img_resized).flatten()
    
    lines = []
    ramp_len = len(GLYPHS)
    for y in range(height):
        row_chars = []
        for x in range(width):
            val = pixels[y * width + x]
            idx = int((255 - val) / 255 * (ramp_len - 1))
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

def generate_svg(ascii_lines, output_path="portrait.svg", accent_color="#38bdf8", bg_color="#0d1117"):
    num_rows = len(ascii_lines)
    num_cols = len(ascii_lines[0]) if num_rows > 0 else 0
    
    font_size = 10
    char_width = 6.0
    line_height = 11.5
    padding = 16
    
    svg_width = int(num_cols * char_width + padding * 2)
    svg_height = int(num_rows * line_height + padding * 2)
    
    row_delay_ms = 35
    anim_duration_sec = 0.4
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_parts.append('  <style>')
    svg_parts.append(f'    .bg {{ fill: {bg_color}; rx: 8px; }}')
    svg_parts.append(f'    .ascii-text {{ font-family: "Fira Code", "Courier New", monospace; font-size: {font_size}px; fill: {accent_color}; font-weight: 500; xml:space: preserve; }}')
    svg_parts.append('  </style>')
    
    svg_parts.append(f'  <rect width="100%" height="100%" class="bg"/>')
    
    svg_parts.append('  <defs>')
    for i in range(num_rows):
        clip_id = f"row-clip-{i}"
        start_time = (i * row_delay_ms) / 1000.0
        svg_parts.append(f'    <clipPath id="{clip_id}">')
        svg_parts.append(f'      <rect x="0" y="0" width="0" height="{svg_height}">')
        svg_parts.append(f'        <animate attributeName="width" from="0" to="{svg_width}" begin="{start_time:.3f}s" dur="{anim_duration_sec}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>')
        svg_parts.append(f'      </rect>')
        svg_parts.append(f'    </clipPath>')
    svg_parts.append('  </defs>')
    
    svg_parts.append('  <g class="ascii-text">')
    for i, line in enumerate(ascii_lines):
        y_pos = padding + (i + 1) * line_height - 2
        clip_id = f"row-clip-{i}"
        svg_parts.append(f'    <text x="{padding}" y="{y_pos:.1f}" clip-path="url(#{clip_id})">{line}</text>')
    svg_parts.append('  </g>')
    svg_parts.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
        
    print(f"Generated portrait SVG successfully: {output_path}")

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "assets/photo-ready.png"
    out_svg = sys.argv[2] if len(sys.argv) > 2 else "portrait.svg"
    
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found. Please run clean_photo.py first.")
        sys.exit(1)
        
    ascii_art = image_to_ascii(img_path, width=54)
    generate_svg(ascii_art, output_path=out_svg)
