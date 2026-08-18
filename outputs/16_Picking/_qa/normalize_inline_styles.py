from pathlib import Path
import re


path = Path(__file__).parents[1] / "f-wh-picking.html"
source = path.read_text(encoding="utf-8")
rules = []
seen = {}


def replace(match):
    style = match.group(1).strip()
    dynamic_width = re.fullmatch(r"width:\s*\$\{([^}]+)\}%\s*;?", style)
    if dynamic_width:
        return f'data-progress="${{{dynamic_width.group(1)}}}"'
    if "${" in style:
        return match.group(0)
    key = re.sub(r"\s+", " ", style)
    token = seen.get(key)
    if token is None:
        token = f"u{len(seen) + 1:03d}"
        seen[key] = token
        rules.append(f'[data-u="{token}"]{{{style}}}')
    return f'data-u="{token}"'


source = re.sub(r'style="([^"]*)"', replace, source)
late_css = '<style id="late-utilities">\n' + "\n".join(rules) + "\n</style>"
source = source.replace("</head>", late_css + "\n</head>", 1)
path.write_text(source, encoding="utf-8")
print(f"normalized {len(seen)} reusable inline declarations")
