#!/usr/bin/env python3
"""
Generates tech-stack.svg matching the dark terminal theme of the profile README.
"""
import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "tech-stack.svg")

CANVAS_W = 860
CANVAS_H = 310
PAD = 24
TITLEBAR_H = 32
BORDER = "#30363d"
MUTED = "#7d8590"
TEXT_MAIN = "#c9d1d9"

# Colors for sections
BLUE = "#38bdf8"
GREEN = "#4ade80"
PURPLE = "#c084fc"
ORANGE = "#fb923c"

def generate_svg():
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">')
    parts.append('<defs><linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>')
    
    # Outer box
    parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#tbg)"/>')
    parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{BORDER}" stroke-width="1"/>')
    
    # Titlebar
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>')
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">stdygit@github: ~/skills --tech-stack</text>')

    sections = [
        ("BACKEND", BLUE, ["[Python]", "[Flask]", "[REST API]"]),
        ("FRONTEND", GREEN, ["[Vue.js]", "[JavaScript]", "[HTML5]", "[CSS3]"]),
        ("DATABASE", PURPLE, ["[PostgreSQL]", "[Neon DB]"]),
        ("DEVOPS & CLOUD", ORANGE, ["[Docker]", "[AWS EC2]", "[Netlify]", "[Render]", "[Railway]"]),
    ]

    curr_y = 60
    line_h = 18

    all_rows = []
    
    for title, color, items in sections:
        hdr = f"// {title}"
        all_rows.append((hdr, color, True))
        
        boxes = "   ".join(items)
        all_rows.append((boxes, TEXT_MAIN, False))

    for idx, (line_str, color, is_hdr) in enumerate(all_rows):
        y = curr_y
        clip_id = f"tc{idx}"
        delay = idx * 0.05
        
        parts.append(f'<clipPath id="{clip_id}"><rect x="{PAD}" y="{y-14}" height="20" width="0"><animate attributeName="width" from="0" to="{CANVAS_W - 2*PAD}" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/></rect></clipPath>')
        
        font_weight = 'font-weight="bold"' if is_hdr else ''
        font_size = "13" if is_hdr else "12"
        indent = "" if is_hdr else "  "
        
        escaped_str = html.escape(indent + line_str)
        parts.append(f'<g clip-path="url(#{clip_id})"><text xml:space="preserve" x="{PAD}" y="{y}" fill="{color}" font-size="{font_size}" {font_weight}>{escaped_str}</text></g>')
        
        if is_hdr:
            curr_y += line_h + 2
        else:
            curr_y += line_h + 10

    # Bottom status line
    parts.append(f'<line x1="0" y1="{CANVAS_H - 35}" x2="{CANVAS_W}" y2="{CANVAS_H - 35}" stroke="{BORDER}"/>')
    parts.append(f'<text x="{PAD}" y="{CANVAS_H - 14}" fill="{MUTED}" font-size="12">stdygit@github:~$ <tspan fill="{TEXT_MAIN}">echo &quot;Skills loaded successfully.&quot;</tspan></text>')
    parts.append(f'<rect x="{PAD + 242}" y="{CANVAS_H - 24}" width="7" height="13" fill="{TEXT_MAIN}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')

    parts.append('</svg>')
    
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"wrote {OUT_PATH}")

if __name__ == "__main__":
    generate_svg()
