#!/usr/bin/env python3
"""Draws the SVG images used in README.md, in a light and a dark version.

Run from the repo root:   python tools/make_assets.py
Edit the text below and re-run it; don't hand-edit the files in assets/.
Standard library only.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        bg1="#0B1020", bg2="#131C33", grid="#1B2640", frame="#1F2B47",
        card="#0E1528", text="#E6EDF3", muted="#9AA8BB", faint="#5F6E86",
        cyan="#22D3EE", violet="#A78BFA", green="#34D399",
        node="#101A2F", node_stroke="#2A3A5E", chip="#152038", chip_stroke="#24345A",
    ),
    "light": dict(
        bg1="#FFFFFF", bg2="#F0F4FA", grid="#E1E7F0", frame="#D6DEEA",
        card="#FFFFFF", text="#0F172A", muted="#475569", faint="#94A3B8",
        cyan="#0891B2", violet="#7C3AED", green="#059669",
        node="#FFFFFF", node_stroke="#CBD5E1", chip="#F1F5F9", chip_stroke="#D5DEEA",
    ),
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Ubuntu, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace"


def e(s):
    return escape(s, quote=True)


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}">\n'
            f'<title>{e(title)}</title>\n{body}\n</svg>\n')


# ----------------------------------------------------------------------------- banner
def banner(t):
    W, H = 1200, 300
    labels = ["alert", "triage", "ATT&CK", "critic", "playbook"]
    xs = [240, 420, 600, 780, 960]
    y, nw, nh = 222, 124, 38
    dur, travel = 6, 0.75          # seconds per loop, share of it spent moving

    out = [f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/>
  </linearGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{t['grid']}"/>
  </pattern>
  <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['cyan']}"/><stop offset="1" stop-color="{t['violet']}"/>
  </linearGradient>
  <linearGradient id="inkline" gradientUnits="userSpaceOnUse" x1="{xs[0]}" y1="0" x2="{xs[-1]}" y2="0">
    <stop offset="0" stop-color="{t['cyan']}"/><stop offset="1" stop-color="{t['violet']}"/>
  </linearGradient>
  <radialGradient id="halo">
    <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="frame"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>
</defs>
<style>
  .flow {{ stroke-dasharray: 5 9; animation: flow 1.1s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -14; }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <circle cx="1080" cy="40" r="180" fill="url(#halo)" opacity="0.35">
    <animate attributeName="cx" values="1080;1010;1080" dur="14s" repeatCount="indefinite"/>
  </circle>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="{t['frame']}"/>
<g fill="{t['faint']}"><circle cx="30" cy="28" r="5"/><circle cx="48" cy="28" r="5"/><circle cx="66" cy="28" r="5"/></g>
<text x="{W-30}" y="33" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t['faint']}">rawalpindi, pk</text>

<text x="{W/2}" y="112" text-anchor="middle" font-family="{SANS}" font-size="54" font-weight="700" fill="{t['text']}" letter-spacing="0.5">Muhammad Abubakar Nadeem</text>
<text x="{W/2}" y="156" text-anchor="middle" font-family="{MONO}" font-size="21" fill="url(#ink)">Agentic AI + Full-Stack Engineer</text>

<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{t['node_stroke']}" stroke-width="2"/>
<line class="flow" x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="url(#inkline)" stroke-width="2"/>''']

    # chevrons between the nodes
    for a, b in zip(xs, xs[1:]):
        m = (a + b) / 2 + 3
        out.append(f'<path d="M{m-5},{y-6} L{m+1},{y} L{m-5},{y+6}" fill="none" '
                   f'stroke="{t["muted"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

    # the packet that travels the pipeline (drawn before the nodes, so it passes behind them)
    span = xs[-1] - xs[0]
    out.append(f'''<g opacity="0">
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.04;{travel};{travel+0.08};1" dur="{dur}s" repeatCount="indefinite"/>
  <circle cx="{xs[0]}" cy="{y}" r="14" fill="url(#halo)"/>
  <circle cx="{xs[0]}" cy="{y}" r="5" fill="{t['cyan']}"/>
  <animateMotion path="M0,0 H{span}" keyPoints="0;1;1" keyTimes="0;{travel};1" calcMode="linear" dur="{dur}s" repeatCount="indefinite"/>
</g>''')

    # nodes light up as the packet reaches them
    for i, (label, x) in enumerate(zip(labels, xs)):
        k = round(travel * (x - xs[0]) / span, 3)
        last = i == len(xs) - 1
        hot = t["green"] if last else t["cyan"]
        base = t["node_stroke"]
        if k == 0:
            vals, times = f"{hot};{base};{base}", "0;0.12;1"
        elif last:
            vals, times = f"{base};{base};{hot};{hot};{base}", f"0;{k-0.02};{k};0.96;1"
        else:
            vals, times = f"{base};{base};{hot};{base};{base}", f"0;{k-0.02};{k};{k+0.1};1"
        out.append(f'''<g>
  <rect x="{x-nw/2}" y="{y-nh/2}" width="{nw}" height="{nh}" rx="10" fill="{t['node']}" stroke="{base}" stroke-width="1.6">
    <animate attributeName="stroke" values="{vals}" keyTimes="{times}" dur="{dur}s" repeatCount="indefinite"/>
  </rect>
  <text x="{x}" y="{y+5}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{t['text']}">{e(label)}</text>
</g>''')

    # a check mark on the playbook once the packet arrives
    cx, cy = xs[-1] + nw / 2 - 2, y - nh / 2 + 2
    out.append(f'''<g opacity="0">
  <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{travel};{travel+0.02};0.96;1" dur="{dur}s" repeatCount="indefinite"/>
  <circle cx="{cx}" cy="{cy}" r="10" fill="{t['green']}"/>
  <path d="M{cx-4.5},{cy} L{cx-1},{cy+3.5} L{cx+5},{cy-3.5}" fill="none" stroke="{t['bg1']}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
</g>''')

    out.append(f'<text x="{W/2}" y="280" text-anchor="middle" font-family="{MONO}" font-size="13.5" '
               f'fill="{t["muted"]}">agents that act, and the guardrails that keep them in check</text>')
    return svg(W, H, "Muhammad Abubakar Nadeem, Agentic AI + Full-Stack Engineer", "\n".join(out))


# ----------------------------------------------------------------------------- project cards
CARDS = {
    "alert2playbook": dict(
        kicker="MULTI-AGENT  /  SECURITY",
        title="Alert2Playbook",
        lines=["A security alert goes in. A MITRE ATT&CK mapping and a",
               "reviewed response playbook come out, in about 7 seconds."],
        chips=["83.3% recall", "810 techniques", "85 tests"],
        tags="LangGraph · Pinecone · BM25 · A2A · MCP",
        footer="live demo and code on GitHub  →",
        live=True,
    ),
    "unisphere": dict(
        kicker="FINAL YEAR PROJECT  /  TEAM LEAD",
        title="UniSphere",
        lines=["One profile to apply to 10+ Pakistani universities,",
               "plus an AI tutor for 14 university entry tests."],
        chips=["graded A+ and A", "RAG tutor", "team of 3"],
        tags="React · FastAPI · pgvector · Mistral",
        footer="unisphere.me  →",
    ),
    "wellmaster": dict(
        kicker="CLIENT WORK  /  MOBILE",
        title="WellMaster App",
        lines=["Customer, rider and admin apps for an organic food",
               "brand, from one React codebase for Android and iOS."],
        chips=["488 tests", "3 apps", "live order chat"],
        tags="React · Capacitor · FastAPI · PostgreSQL · Celery",
        footer="private client code",
    ),
    "data-warehouse": dict(
        kicker="DATA ENGINEERING",
        title="Near-Real-Time Data Warehouse",
        lines=["Streams about 550,000 retail transactions through",
               "a HYBRIDJOIN into a MySQL star schema."],
        chips=["5 dimensions", "20 OLAP queries", "2 threads"],
        tags="Python · MySQL · pandas",
        footer="code on GitHub  →",
    ),
}


def chip_w(text, size):
    return len(text) * size * 0.58 + 22


def card(t, kicker, title, lines, chips, tags, footer, live=False):
    W, H = 500, 236
    out = [f'''<defs>
  <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['cyan']}"/><stop offset="1" stop-color="{t['violet']}"/>
  </linearGradient>
  <clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath>
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{t['card']}" stroke="{t['frame']}"/>
<rect clip-path="url(#c)" x="0" y="0" width="{W}" height="3" fill="url(#ink)"/>
<text x="24" y="36" font-family="{MONO}" font-size="11.5" letter-spacing="1.2" fill="{t['cyan']}">{e(kicker)}</text>
<text x="24" y="68" font-family="{SANS}" font-size="23" font-weight="700" fill="{t['text']}">{e(title)}</text>''']
    for i, line in enumerate(lines):
        out.append(f'<text x="24" y="{96 + i*21}" font-family="{SANS}" font-size="14.5" fill="{t["muted"]}">{e(line)}</text>')
    x = 24
    for c in chips:
        w = chip_w(c, 12.5)
        out.append(f'<rect x="{x}" y="138" width="{w:.0f}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["chip_stroke"]}"/>'
                   f'<text x="{x + w/2:.0f}" y="155.5" text-anchor="middle" font-family="{SANS}" font-size="12.5" '
                   f'font-weight="600" fill="{t["text"]}">{e(c)}</text>')
        x += w + 8
    out.append(f'<text x="24" y="190" font-family="{MONO}" font-size="12" fill="{t["faint"]}">{e(tags)}</text>')
    out.append(f'<text x="24" y="216" font-family="{SANS}" font-size="13" font-weight="600" fill="{t["violet"]}">{e(footer)}</text>')
    if live:
        out.append(f'''<g>
  <circle cx="{W-62}" cy="32" r="9" fill="{t['green']}" opacity="0.25">
    <animate attributeName="r" values="4;10;4" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.45;0;0.45" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{W-62}" cy="32" r="4" fill="{t['green']}"/>
  <text x="{W-50}" y="36.5" font-family="{MONO}" font-size="12" fill="{t['green']}">live</text>
</g>''')
    return svg(W, H, f"{title}: {' '.join(lines)}", "\n".join(out))


# ----------------------------------------------------------------------------- tech stack
STACK = [
    ("agents", ["LangGraph", "LangChain", "LangSmith", "CrewAI", "MCP", "A2A", "Tool calling"]),
    ("retrieval", ["RAG", "Pinecone", "pgvector", "FAISS", "BM25 + RRF", "Reranking", "Knowledge graphs"]),
    ("models", ["OpenAI", "Claude", "Gemini", "Groq", "Mistral", "Hugging Face"]),
    ("apps", ["FastAPI", "React", "TypeScript", "Capacitor", "PostgreSQL", "Redis", "Celery", "Docker", "GitHub Actions"]),
    ("data", ["Python", "SQL", "MySQL", "pandas", "ETL", "OLAP"]),
]


def stack(t):
    W, row, top = 1000, 46, 26
    H = top + row * len(STACK) + 12
    out = [f'''<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{t['card']}" stroke="{t['frame']}"/>''']
    for r, (label, items) in enumerate(STACK):
        y = top + r * row
        out.append(f'<text x="28" y="{y+19}" font-family="{MONO}" font-size="14" fill="{t["cyan"]}">{e(label)}/</text>')
        x = 150
        for it in items:
            w = chip_w(it, 13)
            out.append(f'<g>'
                       f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="28" rx="8" fill="{t["chip"]}" stroke="{t["chip_stroke"]}"/>'
                       f'<text x="{x + w/2:.0f}" y="{y+18.5}" text-anchor="middle" font-family="{SANS}" font-size="13" '
                       f'fill="{t["text"]}">{e(it)}</text></g>')
            x += w + 8
    return svg(W, H, "Tech stack: " + "; ".join(f"{l}: {', '.join(i)}" for l, i in STACK), "\n".join(out))


def main():
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"banner-{name}.svg").write_text(banner(t), encoding="utf-8")
        (OUT / f"stack-{name}.svg").write_text(stack(t), encoding="utf-8")
        for slug, c in CARDS.items():
            (OUT / f"card-{slug}-{name}.svg").write_text(card(t, **c), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)


if __name__ == "__main__":
    main()
