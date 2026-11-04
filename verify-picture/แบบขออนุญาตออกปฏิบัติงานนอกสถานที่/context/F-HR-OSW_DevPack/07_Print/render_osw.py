#!/usr/bin/env python3
"""render_osw.py — สร้างเอกสาร OSW จาก template + data (logic-less, mustache subset)
usage: python render_osw.py osw_body.tpl.html data.json -o body.html
  แล้ว build_html.py body.html -o X.html && render_pdf.py X.html -o X.pdf  (thai-doc-pdf-generator)
syntax: {{a.b}} escape · {{{a.b}}} raw · {{#list}}…{{/list}} loop/if · {{^x}}…{{/x}} if-not
"""
import argparse, html, json, re, pathlib
SEC = re.compile(r'{{([#^])([\w.]+)}}([\s\S]*?){{/\2}}')
def get(stack, path):
    for ctx in reversed(stack):
        cur = ctx; ok = True
        for k in path.split('.'):
            if isinstance(cur, dict) and k in cur: cur = cur[k]
            else: ok = False; break
        if ok: return cur
    return None
def render(t, stack):
    def sec(m):
        kind, key, inner = m.groups(); v = get(stack, key)
        if kind == '^': return render(inner, stack) if not v else ''
        if isinstance(v, list): return ''.join(render(inner, stack + [x]) for x in v)
        return render(inner, stack + ([v] if isinstance(v, dict) else [])) if v else ''
    t = SEC.sub(sec, t)
    t = re.sub(r'{{{([\w.]+)}}}', lambda m: str(get(stack, m.group(1)) or ''), t)
    return re.sub(r'{{([\w.]+)}}', lambda m: html.escape(str(get(stack, m.group(1)) if get(stack, m.group(1)) is not None else ''), quote=True), t)
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('tpl'); ap.add_argument('data'); ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    out = render(pathlib.Path(a.tpl).read_text(encoding='utf-8'), [json.loads(pathlib.Path(a.data).read_text(encoding='utf-8'))])
    pathlib.Path(a.out).write_text(out, encoding='utf-8'); print('[render_osw] wrote', a.out)
