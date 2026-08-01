import sys
import os

ROWS = [
    ("user", "arnav-jain700"),
    ("role", "Software Engineer"),
    ("focus", "Full-Stack Development · AI Systems"),
    ("stack", "Python · JavaScript/TypeScript · React · C++"),
    ("now", "Building a Living Terminal GitHub Profile"),
    ("status", "⚡ Active & Building"),
]

def render_panel(output_path="sysinfo.svg", is_preview=False):
    width = 460
    header_height = 36
    row_height = 26
    padding_y = 20
    padding_x = 24
    
    total_height = header_height + (len(ROWS) * row_height) + padding_y * 2
    
    accent_color = "#38bdf8"
    label_color = "#8b949e"
    value_color = "#c9d1d9"
    bg_color = "#0d1117"
    header_bg = "#161b22"
    border_color = "#30363d"
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_height}" width="{width}" height="{total_height}">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 10px; }}')
    svg.append(f'    .header-bg {{ fill: {header_bg}; rx: 10px; }}')
    svg.append('    .btn-red { fill: #ff5f56; }')
    svg.append('    .btn-yellow { fill: #ffbd2e; }')
    svg.append('    .btn-green { fill: #27c93f; }')
    svg.append(f'    .title {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: #8b949e; font-weight: 600; }}')
    svg.append(f'    .label {{ font-family: "Fira Code", monospace, sans-serif; font-size: 13px; fill: {label_color}; font-weight: 500; }}')
    svg.append(f'    .value {{ font-family: "Fira Code", monospace, sans-serif; font-size: 13px; fill: {value_color}; font-weight: 400; }}')
    svg.append(f'    .prompt {{ font-family: "Fira Code", monospace, sans-serif; font-size: 13px; fill: {accent_color}; font-weight: 600; }}')
    
    if not is_preview:
        svg.append('    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }')
        svg.append('    .anim-row { animation: fadeIn 0.4s ease-out forwards; opacity: 0; }')
    
    svg.append('  </style>')
    
    # Outer box & header
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')
    svg.append(f'  <path d="M 0,10 A 10,10 0 0 1 10,0 L {width-10},0 A 10,10 0 0 1 {width},10 L {width},{header_height} L 0,{header_height} Z" class="header-bg"/>')
    
    # Window controls (Traffic lights)
    svg.append('  <circle cx="20" cy="18" r="6" class="btn-red"/>')
    svg.append('  <circle cx="38" cy="18" r="6" class="btn-yellow"/>')
    svg.append('  <circle cx="56" cy="18" r="6" class="btn-green"/>')
    
    # Window title
    title_text = "arnav-jain700@terminal:~ (sysinfo)"
    svg.append(f'  <text x="{width/2}" y="22" text-anchor="middle" class="title">{title_text}</text>')
    
    # Rows
    y_start = header_height + padding_y + 10
    for idx, (label, val) in enumerate(ROWS):
        y = y_start + (idx * row_height)
        delay = (idx * 0.15) + 0.1
        style_attr = f' style="animation-delay: {delay:.2f}s;"' if not is_preview else ''
        anim_class = ' class="anim-row"' if not is_preview else ''
        
        svg.append(f'  <g{anim_class}{style_attr}>')
        svg.append(f'    <text x="{padding_x}" y="{y}" class="prompt">❯</text>')
        svg.append(f'    <text x="{padding_x + 18}" y="{y}" class="label">{label}:</text>')
        # Offset value depending on label length
        val_x = padding_x + 95
        svg.append(f'    <text x="{val_x}" y="{y}" class="value">{val}</text>')
        svg.append('  </g>')
        
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Generated sysinfo panel SVG successfully: {output_path}")

if __name__ == "__main__":
    is_preview = os.environ.get("PREVIEW") == "1"
    out_file = sys.argv[1] if len(sys.argv) > 1 else "sysinfo.svg"
    render_panel(out_file, is_preview=is_preview)
