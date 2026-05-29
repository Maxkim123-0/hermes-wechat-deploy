#!/usr/bin/env python3
"""GitHub trending repos — fetches repos from last 3 days, filters spam, outputs for briefing agent."""
import json, urllib.request, ssl, time

ctx = ssl.create_default_context()
UA = "Mozilla/5.0"
SPAM_KW = ['cheat', 'aimbot', 'executor', 'esp ', 'overlay', 'exploit', 'hack ', 'bypass', 'spoofer', 'mod menu', 'crack', 'keygen', 'external tool',
    # 2026-05 实战新增: polymarket 交易机器人刷屏、壁纸引擎/Lossless Scaling 仿冒、Jenny Mod/minecraft 色情模组、赌场推广
    'polymarket trading bot', 'polymarket copy trading', 'polymarket-trading-bot', 'polymarket-copy-trading',
    'wallpaper engine', 'lossless scaling', 'jenny mod', 'jenny-mod',
    'casino bonus', 'no deposit', 'crypto casino', 'cashback system',
    'tomodachi life', # 游戏ROM推广，非技术项目
]

since = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400 * 3))
out = []

try:
    url = f"https://api.github.com/search/repositories?q=stars:>30+created:>={since}&sort=stars&order=desc&per_page=20"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        data = json.loads(r.read())

    seen = set()
    for item in data.get("items", []):
        name = item["full_name"]
        desc = (item.get("description") or "")[:150]
        stars = item["stargazers_count"]
        lang = item.get("language") or ""

        if any(kw in desc.lower() for kw in SPAM_KW):
            continue
        if name in seen:
            continue
        seen.add(name)

        out.append(f"⭐{stars} | {name} | {lang}")
        out.append(f"  {desc}")
        out.append(f"  {item['html_url']}")
        out.append("")

    for line in out:
        print(line)

except Exception as e:
    print(f"# GitHub fetch error: {e}")
