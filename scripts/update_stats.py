import os
import json
import urllib.request

def build_stats_svg(repos=4, followers=0, following=1, stars=0):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 180" width="100%" height="100%">
  <defs>
    <linearGradient id="statsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F1720" />
      <stop offset="100%" stop-color="#0B0F14" />
    </linearGradient>

    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F5A0" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#00D9FF" stop-opacity="0.3" />
    </linearGradient>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@600;700&amp;family=Inter:wght@600;800;900&amp;display=swap');
    text {{ font-family: 'Inter', sans-serif; }}
    .mono {{ font-family: 'Fira Code', monospace; }}

    /* Border breathing glow */
    .stat-card-border {{
      animation: statBorderGlow 4s ease-in-out infinite alternate;
    }}
    @keyframes statBorderGlow {{
      0% {{ stroke-opacity: 0.35; }}
      100% {{ stroke-opacity: 0.8; filter: drop-shadow(0 0 5px rgba(0, 245, 160, 0.4)); }}
    }}

    /* Pulsing live sync LED */
    .sync-dot {{
      animation: sDot 1.8s ease-in-out infinite alternate;
    }}
    @keyframes sDot {{
      0% {{ opacity: 0.35; transform: scale(0.85); }}
      100% {{ opacity: 1; transform: scale(1.2); filter: drop-shadow(0 0 4px #00F5A0); }}
    }}
  </style>

  <!-- Card Body -->
  <rect class="stat-card-border" width="678" height="178" x="1" y="1" rx="14" fill="url(#statsBg)" stroke="url(#borderGrad)" stroke-width="1.5" />

  <!-- Header -->
  <text x="24" y="30" font-size="13" font-weight="800" fill="#00F5A0" letter-spacing="1.2">// GITHUB ACTIVITY &amp; METRICS</text>
  <circle cx="515" cy="26" r="3.5" fill="#00F5A0" class="sync-dot" />
  <text x="654" y="30" text-anchor="end" font-size="10.5" font-weight="700" fill="#00D9FF" class="mono">@luxtaic • VERIFIED LIVE</text>
  <line x1="24" y1="42" x2="654" y2="42" stroke="#00F5A0" stroke-width="1" stroke-opacity="0.18" />

  <!-- 4 Real Metric Chips (Pure static coordinates, zero CSS transform collision) -->

  <!-- 1. Public Repositories (x: 24) -->
  <g transform="translate(24, 60)">
    <rect width="145" height="85" rx="10" fill="rgba(0, 245, 160, 0.06)" stroke="#00F5A0" stroke-width="1" stroke-opacity="0.35" />
    <text x="18" y="28" font-size="10" font-weight="700" fill="#8B949E">PUBLIC REPOS</text>
    <text x="18" y="62" font-size="28" font-weight="900" fill="#00F5A0" class="mono">{repos}</text>
  </g>

  <!-- 2. Stars Earned (x: 185) -->
  <g transform="translate(185, 60)">
    <rect width="145" height="85" rx="10" fill="rgba(0, 217, 255, 0.06)" stroke="#00D9FF" stroke-width="1" stroke-opacity="0.35" />
    <text x="18" y="28" font-size="10" font-weight="700" fill="#8B949E">STARS EARNED</text>
    <text x="18" y="62" font-size="28" font-weight="900" fill="#00D9FF" class="mono">{stars}</text>
  </g>

  <!-- 3. Followers (x: 346) -->
  <g transform="translate(346, 60)">
    <rect width="145" height="85" rx="10" fill="rgba(0, 245, 160, 0.06)" stroke="#00F5A0" stroke-width="1" stroke-opacity="0.35" />
    <text x="18" y="28" font-size="10" font-weight="700" fill="#8B949E">FOLLOWERS</text>
    <text x="18" y="62" font-size="28" font-weight="900" fill="#00F5A0" class="mono">{followers}</text>
  </g>

  <!-- 4. Following (x: 507) -->
  <g transform="translate(507, 60)">
    <rect width="147" height="85" rx="10" fill="rgba(0, 217, 255, 0.06)" stroke="#00D9FF" stroke-width="1" stroke-opacity="0.35" />
    <text x="18" y="28" font-size="10" font-weight="700" fill="#8B949E">FOLLOWING</text>
    <text x="18" y="62" font-size="28" font-weight="900" fill="#00D9FF" class="mono">{following}</text>
  </g>

  <!-- Dynamic Footer note -->
  <text x="340" y="162" text-anchor="middle" font-size="9" fill="#8B949E">
    ⚡ GitHub activity updates automatically via GitHub Actions
  </text>
</svg>"""

def main():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {'User-Agent': 'GitHub-Actions'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    public_repos = 4
    followers = 0
    following = 1
    stars = 0

    try:
        req = urllib.request.Request('https://api.github.com/users/luxtaic', headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            user = json.loads(resp.read().decode())
            public_repos = user.get('public_repos', public_repos)
            followers = user.get('followers', followers)
            following = user.get('following', following)
    except Exception as e:
        print(f"Notice: Could not fetch user data ({e}), using fallback values.")

    try:
        req_repos = urllib.request.Request('https://api.github.com/users/luxtaic/repos?per_page=100', headers=headers)
        with urllib.request.urlopen(req_repos, timeout=10) as resp:
            repos = json.loads(resp.read().decode())
            stars = sum(r.get('stargazers_count', 0) for r in repos)
    except Exception as e:
        print(f"Notice: Could not fetch repos ({e}), using fallback values.")

    svg = build_stats_svg(repos=public_repos, followers=followers, following=following, stars=stars)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "stats.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully wrote stats.svg: Repos={public_repos}, Followers={followers}, Following={following}, Stars={stars}")

if __name__ == "__main__":
    main()
