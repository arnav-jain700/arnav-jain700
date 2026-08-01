import sys
import os

SECTIONS = [
    {"type": "kv", "key": "Now", "val": "Software Engineer & Builder"},
    {"type": "kv", "key": "Prev", "val": "Full-Stack Engineer"},
    {"type": "kv", "key": "Also", "val": "Open-Source Contributor"},
    {"type": "kv", "key": "Edu", "val": "B.Tech Computer Science"},
    {"type": "header", "title": "- Stack"},
    {"type": "kv", "key": "Frontend", "val": "React, Next.js, TypeScript, Tailwind"},
    {"type": "kv", "key": "Backend", "val": "Node.js, Python, FastAPI, Postgres"},
    {"type": "kv", "key": "AI / ML", "val": "OpenAI API, LangChain, PyTorch"},
    {"type": "kv", "key": "Cloud", "val": "AWS, Docker, Vercel, Linux"},
    {"type": "header", "title": "- Highlights"},
    {"type": "bullet", "text": "• Built Living Terminal GitHub Profile README"},
    {"type": "bullet", "text": "• Active developer & open-source contributor"},
]

def render_panel(output_path="sysinfo.svg", is_preview=False):
    width = 480
    height = 460
    header_height = 32
    padding_x = 22
    
    bg_color = "#0d1117"
    header_bg = "#161b22"
    border_color = "#30363d"
    
    cyan_color = "#7dcfff"
    orange_color = "#ff9e64"
    val_color = "#c0caf5"
    muted_color = "#565f89"
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 10px; }}')
    svg.append(f'    .header-bg {{ fill: {header_bg}; rx: 10px; }}')
    svg.append('    .btn-red { fill: #ff5f56; }')
    svg.append('    .btn-yellow { fill: #ffbd2e; }')
    svg.append('    .btn-green { fill: #27c93f; }')
    svg.append(f'    .title {{ font-family: "Fira Code", monospace, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }}')
    svg.append(f'    .user-prompt {{ font-family: "Fira Code", monospace, sans-serif; font-size: 13px; fill: {cyan_color}; font-weight: 700; }}')
    svg.append(f'    .section-title {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: {cyan_color}; font-weight: 600; }}')
    svg.append(f'    .key {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: {orange_color}; font-weight: 600; }}')
    svg.append(f'    .val {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: {val_color}; font-weight: 400; }}')
    svg.append(f'    .bullet-text {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: #73daca; font-weight: 400; }}')
    svg.append(f'    .divider {{ stroke: {muted_color}; stroke-width: 1px; stroke-dasharray: 4 2; }}')
    svg.append('  </style>')
    
    # Outer box & header
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')
    svg.append(f'  <path d="M 0,10 A 10,10 0 0 1 10,0 L {width-10},0 A 10,10 0 0 1 {width},10 L {width},{header_height} L 0,{header_height} Z" class="header-bg"/>')
    
    # Traffic lights
    svg.append('  <circle cx="18" cy="16" r="5" class="btn-red"/>')
    svg.append('  <circle cx="32" cy="16" r="5" class="btn-yellow"/>')
    svg.append('  <circle cx="46" cy="16" r="5" class="btn-green"/>')
    svg.append(f'  <text x="{width/2}" y="20" text-anchor="middle" class="title">arnav-jain700:~$ neofetch</text>')
    
    # Top User Prompt
    y_curr = header_height + 26
    svg.append(f'  <text x="{padding_x}" y="{y_curr}" class="user-prompt">arnav@github</text>')
    
    # Divider line under prompt
    y_curr += 12
    svg.append(f'  <line x1="{padding_x}" y1="{y_curr}" x2="{width - padding_x}" y2="{y_curr}" stroke="{border_color}" stroke-width="1"/>')
    
    y_curr += 20
    for idx, item in enumerate(SECTIONS):
        svg.append('  <g>')
        if item["type"] == "kv":
            svg.append(f'    <text x="{padding_x}" y="{y_curr}" class="key">{item["key"]}</text>')
            svg.append(f'    <text x="{padding_x + 95}" y="{y_curr}" class="val">{item["val"]}</text>')
            y_curr += 22
        elif item["type"] == "header":
            y_curr += 6
            svg.append(f'    <text x="{padding_x}" y="{y_curr}" class="section-title">{item["title"]}</text>')
            # Dash divider extending to right edge
            title_len = len(item["title"]) * 7.5
            svg.append(f'    <line x1="{padding_x + title_len + 8}" y1="{y_curr - 4}" x2="{width - padding_x}" y2="{y_curr - 4}" class="divider"/>')
            y_curr += 20
        elif item["type"] == "bullet":
            svg.append(f'    <text x="{padding_x}" y="{y_curr}" class="bullet-text">{item["text"]}</text>')
            y_curr += 20
            
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
