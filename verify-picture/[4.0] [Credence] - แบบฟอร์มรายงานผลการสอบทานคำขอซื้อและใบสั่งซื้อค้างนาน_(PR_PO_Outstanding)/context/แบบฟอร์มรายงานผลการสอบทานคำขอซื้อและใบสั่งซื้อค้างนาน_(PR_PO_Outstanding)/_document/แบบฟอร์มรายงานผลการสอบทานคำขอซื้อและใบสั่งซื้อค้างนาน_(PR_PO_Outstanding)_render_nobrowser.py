"""[NO-BROWSER] แทน render_states.py: render body + build_html ทุกสถานะ (ไม่ทำ PDF) + ตรวจ {{}} หลง/key หาย/จำนวนหน้า"""
import sys, os, json, pathlib, subprocess, re
TD = os.environ['TD']; sys.path.insert(0, TD + '/scripts')
import render_doc
tpl, out, title = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
datas = sys.argv[4:]
out.mkdir(exist_ok=True)
build = [sys.executable, TD + '/scripts/build_html.py']
subprocess.run(build + [tpl, '--title', title, '--mode', 'replica', '--profile', 'profile.json', '-o', 'FM-PUR-03_template.html'], check=True, capture_output=True)
for d in sorted(datas):
    stem = pathlib.Path(d).name.replace('.data.json', '')
    render_doc.MISSING.clear()
    body = render_doc.render_file(tpl, json.loads(pathlib.Path(d).read_text(encoding='utf-8')))
    bp = out / f'_{stem}.body.html'; bp.write_text(body, encoding='utf-8')
    subprocess.run(build + [str(bp), '--title', title, '--mode', 'replica', '--profile', 'profile.json', '-o', str(out / f'{stem}.html')], check=True, capture_output=True)
    html = (out / f'{stem}.html').read_text(encoding='utf-8')
    pages = body.count('class="doc-page'); stray = len(re.findall(r'{{', body)); miss = sorted(set(render_doc.MISSING))
    print(stem, 'pages=', pages, 'stray=', stray, 'missing=', miss)
