from pathlib import Path
import re


path = Path(__file__).parents[1] / "f-wh-picking.html"
source = path.read_text(encoding="utf-8")

source = source.replace('class="note', 'class="context-box')
source = source.replace('class="tabs"', 'class="drawer-tabs"')
source = source.replace('class="tab ', 'class="drawer-tab ')
source = re.sub(r'\.tabs\b', '.drawer-tabs', source)
source = re.sub(r'\.tab(?!le)\b', '.drawer-tab', source)
source = source.replace('<select onchange=', '<select data-width="bounded" onchange=')
source = source.replace('onclick="event.stopPropagation()" class="tbl-center"', 'onclick="event.cancelBubble=true" class="tbl-center"')
source = source.replace("document.getElementById('cbi-' + key)", "document.querySelector('[id=\"cbi-' + key + '\"]')")
source = source.replace("document.getElementById('combo-pop')", "document.querySelector('#combo-pop')")

old_action = 'style="text-align:left;padding:8px 10px;border-radius:var(--r);cursor:pointer;border:${st.action === a[0] ? \'2px solid var(--c-primary)\' : \'1px solid var(--c-border)\'};background:${st.action === a[0] ? \'var(--c-primary-08)\' : \'#fff\'};display:flex;gap:8px;align-items:center;"'
new_action = 'class="short-action ${st.action === a[0] ? \'is-on\' : \'\'}"'
if old_action not in source:
    raise SystemExit("short-action source pattern not found")
source = source.replace(old_action, new_action)

source, count = re.subn(
    r"if \(!so\) \{ const tr = TR_BY\[code\]; return SECWRAP\(SEC\('arrow-left-right'.*?\); \} const g = gate\(so\);",
    "if (!so) return ''; const g = gate(so);",
    source,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"SO-only detail normalization expected 1 match, got {count}")

path.write_text(source, encoding="utf-8")
print("applied final mechanical normalization")
