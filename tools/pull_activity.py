import sys
import os
import json
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GitHubActivityBot/1.0"

def fetch_recent_activity(username="arnav-jain700", max_items=5):
    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github.v3+json"})
    
    print(f"Fetching recent activity for '{username}'...")
    events = []
    try:
        with urllib.request.urlopen(req, timeout=10.0) as response:
            if response.status == 200:
                events = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Notice: GitHub API fetch fallback triggered ({e})")

    activity_lines = []
    seen = set()

    for ev in events:
        if len(activity_lines) >= max_items:
            break

        ev_type = ev.get("type")
        repo_name = ev.get("repo", {}).get("name", "")
        repo_url = f"https://github.com/{repo_name}" if repo_name else "#"

        if ev_type == "PushEvent":
            commits = ev.get("payload", {}).get("commits", [])
            for c in commits:
                msg = c.get("message", "").split("\n")[0]
                sha = c.get("sha", "")[:7]
                key = f"push-{repo_name}-{sha}"
                if key not in seen:
                    seen.add(key)
                    commit_url = f"{repo_url}/commit/{c.get('sha')}"
                    activity_lines.append(f"- 🔨 Pushed [`{sha}`]({commit_url}) to [{repo_name}]({repo_url}): *{msg}*")
                    if len(activity_lines) >= max_items:
                        break

        elif ev_type == "PullRequestEvent":
            action = ev.get("payload", {}).get("action", "")
            pr = ev.get("payload", {}).get("pull_request", {})
            title = pr.get("title", "")
            pr_url = pr.get("html_url", repo_url)
            number = pr.get("number", "")
            key = f"pr-{repo_name}-{number}"
            if key not in seen:
                seen.add(key)
                activity_lines.append(f"- 🔀 {action.capitalize()} PR [#{number} {title}]({pr_url}) in [{repo_name}]({repo_url})")

        elif ev_type == "CreateEvent":
            ref_type = ev.get("payload", {}).get("ref_type", "repository")
            ref_name = ev.get("payload", {}).get("ref", "")
            key = f"create-{repo_name}-{ref_name}"
            if key not in seen:
                seen.add(key)
                if ref_type == "repository":
                    activity_lines.append(f"- 📦 Created repository [{repo_name}]({repo_url})")
                else:
                    activity_lines.append(f"- 🚀 Created {ref_type} `{ref_name}` in [{repo_name}]({repo_url})")

        elif ev_type == "WatchEvent":
            key = f"star-{repo_name}"
            if key not in seen:
                seen.add(key)
                activity_lines.append(f"- ⭐ Starred repository [{repo_name}]({repo_url})")

    if not activity_lines:
        activity_lines = [
            "- 🚀 Building full-stack web applications & AI agent systems",
            "- 🔨 Created `live_github_terminal` dynamic SVG contribution engine",
            "- ⭐ Contributing to open-source developer tooling & modern web apps",
            "- ⚡ Automating GitHub stats, graphs, & profile workflows with GitHub Actions"
        ]

    return "\n".join(activity_lines)

def update_readme_activity(readme_path="README.md", activity_markdown=""):
    if not os.path.exists(readme_path):
        print(f"{readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!--START_SECTION:activity-->"
    end_tag = "<!--END_SECTION:activity-->"

    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = f"{before}{start_tag}\n{activity_markdown}\n{end_tag}{after}"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated README.md activity section successfully!")
    else:
        print("Activity tags not found in README.md; skipping inline replacement.")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "arnav-jain700"
    readme = sys.argv[2] if len(sys.argv) > 2 else "README.md"
    act_md = fetch_recent_activity(uname)
    print("Fetched Activity:")
    print(act_md)
    update_readme_activity(readme, act_md)
