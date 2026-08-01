import sys
import os
import json
from datetime import datetime

LEVELS = ["#161a2e", "#16537e", "#1c7ed6", "#4dabf7", "#a5d8ff"]

def render_graph(json_path="assets/contributions.json", output_path="graph.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Please run pull_contributions.py first.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    busiest_day = data.get("busiest_day", "N/A")
    username = data.get("username", "arnav-jain700")

    cell_size = 11.5
    cell_gap = 3.5
    cell_step = cell_size + cell_gap
    padding_x = 24
    header_height = 42
    footer_height = 34
    
    num_weeks = (len(days) + 6) // 7
    width = int(padding_x * 2 + num_weeks * cell_step)
    height = int(header_height + 7 * cell_step + footer_height)
    
    bg_color = "#0d1117"
    border_color = "#30363d"
    text_color = "#8b949e"
    accent_color = "#38bdf8"
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 10px; }}')
    svg.append(f'    .title {{ font-family: "Fira Code", monospace, sans-serif; font-size: 13px; fill: {accent_color}; font-weight: 600; }}')
    svg.append(f'    .meta {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: {text_color}; font-weight: 400; }}')
    svg.append('  </style>')
    
    # Background
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')
    
    # Header
    header_text = f"$ cat contributions.log --user={username}"
    svg.append(f'  <text x="{padding_x}" y="26" class="title">❯ {header_text}</text>')
    
    # Grid cells
    grid_y_start = header_height + 5
    
    for i, d in enumerate(days):
        week_idx = i // 7
        day_idx = i % 7
        
        x = padding_x + week_idx * cell_step
        y = grid_y_start + day_idx * cell_step
        
        level = d.get("level", 0)
        level = max(0, min(4, level))
        color = LEVELS[level]
        
        date_str = d.get("date", "")
        count = d.get("count", 0)
        tooltip = f"{count} contributions on {date_str}"
        delay = week_idx * 0.015
        
        svg.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}">')
        svg.append(f'    <animate attributeName="opacity" values="0;1" dur="0.2s" begin="{delay:.3f}s" fill="freeze"/>')
        svg.append(f'    <title>{tooltip}</title>')
        svg.append(f'  </rect>')
        
    # Footer Stats Summary
    footer_y = height - 14
    stats_str = f"Total: {total_contribs}  |  Current Streak: {current_streak} days  |  Longest: {longest_streak} days  |  Peak: {busiest_day}s"
    svg.append(f'  <text x="{padding_x}" y="{footer_y}" class="meta">{stats_str}</text>')
    
    # Legend at bottom right
    legend_x_end = width - padding_x
    svg.append(f'  <text x="{legend_x_end - 90}" y="{footer_y}" class="meta">Less</text>')
    for l_idx, lvl_color in enumerate(LEVELS):
        lx = legend_x_end - 55 + (l_idx * 10)
        svg.append(f'  <rect x="{lx}" y="{footer_y - 8}" width="8" height="8" rx="1.5" fill="{lvl_color}"/>')
    svg.append(f'  <text x="{legend_x_end - 2}" y="{footer_y}" class="meta">More</text>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Generated contribution graph SVG successfully: {output_path}")

if __name__ == "__main__":
    jpath = sys.argv[1] if len(sys.argv) > 1 else "assets/contributions.json"
    opath = sys.argv[2] if len(sys.argv) > 2 else "graph.svg"
    render_graph(jpath, opath)
