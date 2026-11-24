"""Run 'python diagrams/draw.py' from the repo to regenerate the SVG figures."""
from html import escape
from pathlib import Path
from policies import DIRECT, AGENTIC, CASE

HERE = Path(__file__).resolve().parent
GROUPS = {"routes": DIRECT, "piper": AGENTIC, "term": CASE}


def local(text, lang):
    zh, en = text.split("|")
    return zh if lang == "zh" else en


def graph(fig, lang):
    columns = [c if isinstance(c, list) else [c] for c in fig.columns]
    paired = any(len(c) > 1 for c in columns)
    top, gap, height = 8, 24, 47
    width = (826 - gap * (len(columns) - 1)) / len(columns)
    ys = [[top, top + 57] if len(c) == 2 else [top + (28 if paired else 0)] for c in columns]
    floor = max(max(y) for y in ys) + height
    canvas = floor + 7 + 37 * len(fig.loops)
    style = """text{font:15px 'Segoe UI','Microsoft YaHei',sans-serif;fill:#17343b;text-anchor:middle}
    .feedback{font-size:13px;fill:#14645c}.wire,.back{fill:none;stroke:#627c81;stroke-width:1.55;stroke-linejoin:round}
    .back{stroke:#287b71}.focus{font-weight:600}"""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{canvas}" viewBox="0 0 860 {canvas}" role="img" aria-labelledby="title desc">',
           f'<title id="title">{escape(fig.name)}</title><desc id="desc">{escape(local(fig.caption,lang))}</desc>',
           '<style>' + style + '</style><defs>']
    for key, color in (("out", "#627c81"), ("in", "#287b71")):
        out.append(f'<marker id="{key}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="{color}"/></marker>')
    out.append('</defs><rect width="100%" height="100%" fill="white"/>')

    def x(col):
        return 19 + col * (width + gap)

    def path(d, back=False):
        css, marker = ("back", "in") if back else ("wire", "out")
        out.append(f'<path class="{css}" d="{d}" marker-end="url(#{marker})"/>')

    for c in range(1, len(columns)):
        prev, after = ys[c - 1], ys[c]
        links = zip(prev, after) if len(prev) == len(after) else [(a, b) for a in prev for b in after]
        for a, b in links:
            path(f'M{x(c)-gap} {a+height/2} H{x(c)-gap/2} V{b+height/2} H{x(c)-3}')
    for level, (start, end, label) in enumerate(fig.loops):
        sx, ex = x(start) + width/2, x(end) + width/2
        row = floor + 26 + level * 37
        if len(columns[end]) == 2 and fig.key == "saycan":
            # New state and updated skill history feed distinct scoring branches.
            for sink in ys[end]:
                path(f'M{sx} {ys[start][-1]+height} V{row} H5 V{sink+height/2} H{x(end)-3}', True)
        else:
            path(f'M{sx} {ys[start][-1]+height} V{row} H{ex} V{ys[end][-1]+height+3}', True)
        out.append(f'<text class="feedback" x="{(sx+ex)/2}" y="{row-5}">{escape(local(label,lang))}</text>')
    for c, nodes in enumerate(columns):
        for raw, y in zip(nodes, ys[c]):
            label = local(raw, lang)
            focus = label.startswith("*")
            lines = label.lstrip("*").split("~")
            fill, stroke = ("#eaf5f2", "#26766d") if focus else ("#ffffff", "#a8bcba")
            out.append(f'<rect x="{x(c)}" y="{y}" width="{width}" height="{height}" rx="4" fill="{fill}" stroke="{stroke}"/>')
            for j, line in enumerate(lines):
                baseline = y + height/2 + 5 + (j - (len(lines)-1)/2)*17
                out.append(f'<text class="{"focus" if focus else "node"}" x="{x(c)+width/2}" y="{baseline}">{escape(line)}</text>')
    return "\n".join(out + ["</svg>"]) + "\n"


def write_figures():
    for lang in ("zh", "en"):
        dest = HERE / lang
        dest.mkdir(exist_ok=True)
        for rows in GROUPS.values():
            for fig in rows:
                (dest / f"{fig.key}.svg").write_text(graph(fig, lang), encoding="utf8")


if __name__ == "__main__":
    write_figures()
