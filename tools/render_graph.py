import sys
import os
import json
from datetime import datetime

# GitHub classic green palette
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render_graph(json_path="assets/contributions.json", output_path="graph.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Please run pull_contributions.py first.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    username = data.get("username", "arnav-jain700")

    cell_size = 11.5
    cell_gap = 3.5
    cell_step = cell_size + cell_gap
    
    padding_left = 42
    padding_top = 32
    padding_right = 24
    footer_height = 36
    
    num_weeks = (len(days) + 6) // 7
    width = int(padding_left + num_weeks * cell_step + padding_right)
    height = int(padding_top + 7 * cell_step + footer_height)
    
    bg_color = "#0d1117"
    border_color = "#30363d"
    text_color = "#8b949e"
    white_text = "#ffffff"
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 10px; }}')
    svg.append(f'    .axis-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; fill: {text_color}; font-weight: 500; }}')
    svg.append(f'    .total-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; fill: {white_text}; font-weight: 700; }}')
    svg.append('  </style>')
    
    # Background
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')
    
    # Day axis labels on left (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for label, day_idx in day_labels:
        y_pos = padding_top + day_idx * cell_step + 9
        svg.append(f'  <text x="{padding_left - 10}" y="{y_pos:.1f}" text-anchor="end" class="axis-text">{label}</text>')

    # Month axis labels on top
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = None
    
    for i in range(0, len(days), 7):
        week_idx = i // 7
        date_str = days[i].get("date", "")
        if date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            m_name = month_names[dt.month - 1]
            if m_name != last_month:
                x_pos = padding_left + week_idx * cell_step
                svg.append(f'  <text x="{x_pos:.1f}" y="{padding_top - 10}" class="axis-text">{m_name}</text>')
                last_month = m_name

    # Render grid cells (Static 100% visible on GitHub)
    for i, d in enumerate(days):
        week_idx = i // 7
        day_idx = i % 7
        
        x = padding_left + week_idx * cell_step
        y = padding_top + day_idx * cell_step
        
        level = d.get("level", 0)
        level = max(0, min(4, level))
        color = LEVELS[level]
        
        date_str = d.get("date", "")
        count = d.get("count", 0)
        tooltip = f"{count} contributions on {date_str}"
        
        svg.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}">')
        svg.append(f'    <title>{tooltip}</title>')
        svg.append(f'  </rect>')
        
    # Footer Stats Line
    footer_y = height - 12
    total_str = f"{total_contribs:,} contributions in the last year"
    svg.append(f'  <text x="{padding_left}" y="{footer_y}" class="total-text">{total_str}</text>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Generated contribution graph SVG successfully: {output_path}")

if __name__ == "__main__":
    jpath = sys.argv[1] if len(sys.argv) > 1 else "assets/contributions.json"
    opath = sys.argv[2] if len(sys.argv) > 2 else "graph.svg"
    render_graph(jpath, opath)
