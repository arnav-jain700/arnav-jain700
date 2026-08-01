import sys
import os
import json
import urllib.request
import html

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GitHubStatsBot/1.0"

def fetch_github_stats(username="arnav-jain700"):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    
    headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github.v3+json"}
    
    public_repos = 0
    followers = 0
    stars = 0
    languages = {}
    
    try:
        req = urllib.request.Request(user_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            public_repos = data.get("public_repos", 0)
            followers = data.get("followers", 0)
    except Exception as e:
        print(f"Notice: User API fetch fallback ({e})")

    try:
        req = urllib.request.Request(repos_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            repos = json.loads(resp.read().decode("utf-8"))
            for r in repos:
                stars += r.get("stargazers_count", 0)
                lang = r.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
    except Exception as e:
        print(f"Notice: Repos API fetch fallback ({e})")

    return {
        "public_repos": public_repos,
        "followers": followers,
        "stars": stars,
        "languages": languages
    }

def render_stats_svg(stats, output_path="stats.svg"):
    width = 540
    height = 200
    bg_color = "#0d1117"
    border_color = "#30363d"
    header_bg = "#161b22"
    
    cyan = "#7dcfff"
    orange = "#ff9e64"
    val_color = "#c0caf5"
    text_color = "#8b949e"
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 10px; }}')
    svg.append(f'    .header-bg {{ fill: {header_bg}; rx: 10px; }}')
    svg.append('    .btn-red { fill: #ff5f56; }')
    svg.append('    .btn-yellow { fill: #ffbd2e; }')
    svg.append('    .btn-green { fill: #27c93f; }')
    svg.append(f'    .title {{ font-family: "Fira Code", monospace, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }}')
    svg.append(f'    .stat-label {{ font-family: "Fira Code", monospace, sans-serif; font-size: 12px; fill: {orange}; font-weight: 600; }}')
    svg.append(f'    .stat-val {{ font-family: "Fira Code", monospace, sans-serif; font-size: 13px; fill: {val_color}; font-weight: 700; }}')
    svg.append(f'    .lang-name {{ font-family: "Fira Code", monospace, sans-serif; font-size: 11px; fill: {cyan}; font-weight: 600; }}')
    svg.append('  </style>')
    
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')
    svg.append(f'  <path d="M 0,10 A 10,10 0 0 1 10,0 L {width-10},0 A 10,10 0 0 1 {width},10 L {width},32 L 0,32 Z" class="header-bg"/>')
    svg.append('  <circle cx="18" cy="16" r="5" class="btn-red"/>')
    svg.append('  <circle cx="32" cy="16" r="5" class="btn-yellow"/>')
    svg.append('  <circle cx="46" cy="16" r="5" class="btn-green"/>')
    svg.append(f'  <text x="{width/2}" y="20" text-anchor="middle" class="title">arnav-jain700:~$ neofetch --stats</text>')
    
    # Left column: Stats
    svg.append(f'  <text x="24" y="65" class="stat-label">Public Repositories:</text>')
    svg.append(f'  <text x="200" y="65" class="stat-val">{stats["public_repos"]}</text>')
    
    svg.append(f'  <text x="24" y="95" class="stat-label">Total Stars Earned:</text>')
    svg.append(f'  <text x="200" y="95" class="stat-val">{stats["stars"]}</text>')
    
    svg.append(f'  <text x="24" y="125" class="stat-label">Followers:</text>')
    svg.append(f'  <text x="200" y="125" class="stat-val">{stats["followers"]}</text>')
    
    # Vertical divider line
    svg.append(f'  <line x1="260" y1="45" x2="260" y2="180" stroke="{border_color}" stroke-width="1"/>')
    
    # Right column: Top Languages
    svg.append(f'  <text x="280" y="65" class="stat-label">Top Languages:</text>')
    
    top_langs = sorted(stats["languages"].items(), key=lambda x: x[1], reverse=True)[:5]
    if not top_langs:
        top_langs = [("Python", 5), ("TypeScript", 4), ("JavaScript", 4), ("C++", 3), ("HTML/CSS", 2)]
        
    total_l_count = sum(c for _, c in top_langs)
    
    y_pos = 92
    for lang, count in top_langs:
        pct = (count / total_l_count) * 100 if total_l_count > 0 else 20
        svg.append(f'  <text x="280" y="{y_pos}" class="lang-name">{html.escape(lang)}</text>')
        svg.append(f'  <rect x="380" y="{y_pos - 9}" width="{int(pct * 1.2)}" height="8" rx="3" fill="{cyan}"/>')
        svg.append(f'  <text x="{385 + int(pct * 1.2)}" y="{y_pos}" class="stat-val" font-size="10">{pct:.0f}%</text>')
        y_pos += 22
        
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated stats SVG successfully: {output_path}")

if __name__ == "__main__":
    st = fetch_github_stats("arnav-jain700")
    render_stats_svg(st, "stats.svg")
