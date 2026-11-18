"""ข้อมูลตัวอย่าง FM-SAL-21 (ข้อมูลสมมติทั้งหมด · โลโก้ placeholder) — 5 สถานะ · ช่องลงชื่อจาก sign_rows.py
data contract: company · doc · period_month_text · blocks[2]{cols[6]{name,ref}, rows[5]{topic, cells[6]{v}}} · conclusion_lines · suggestion_lines · sign_rows · layout"""
import json, sys, os, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ['TD'], 'scripts'))
from sign_rows import build_signs, chunk_signs
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"><rect width="300" height="80" fill="#fff"/><text x="150" y="52" font-size="34" text-anchor="middle" font-family="sans-serif" fill="#888">COMPANY LOGO</text></svg>'.encode()).decode()
TOPICS = ['1. ความรวดเร็วในการตอบคำถาม', '2. การให้ข้อมูลสินค้า', '3. การแก้ไขปัญหา (สินค้าเสียหาย)', '4. ความเหมาะสมในการแก้ปัญหา', '5. คุณภาพสินค้า']
SCALE = {5: 'มากที่สุด', 4: 'มาก', 3: 'ปานกลาง', 2: 'น้อย', 1: 'ควรปรับปรุง'}
PER, NCOL, MINL, CPL = PC['cols_per_block'], PC['max_rows'], PC['text_min_lines'], 100

def lines(text):
    out = []
    for para in (text or '').split('\n'):
        while len(para) > CPL:
            cut = para.rfind(' ', 0, CPL); cut = cut if cut > 40 else CPL
            out.append(para[:cut].rstrip()); para = para[cut:].lstrip()
        if para: out.append(para)
    while len(out) < MINL: out.append('')
    return [{'text': t} for t in out]

def blocks(cols):
    """cols: [{name, ref, scores:[5 ints]}] ≤ 12 → 2 ชุด × 6 คอลัมน์ (เติมช่องว่างให้ครบ 12)"""
    cols = list(cols) + [{'name': '', 'ref': '', 'scores': [None] * 5}] * (NCOL - len(cols))
    out = []
    for b in range(0, NCOL, PER):
        cs = cols[b:b + PER]
        out.append({'cols': [{'name': c['name'], 'ref': c['ref']} for c in cs],
                    'rows': [{'topic': t, 'cells': [{'v': SCALE.get(c['scores'][i], '') if c['scores'][i] else ''} for c in cs]} for i, t in enumerate(TOPICS)]})
    return out

def build(no, draft, cols, concl, sugg, req, chain_):
    signs = build_signs(req, chain_, PC)
    return {'company': {'name': 'บริษัท ตัวอย่าง จำกัด', 'logo': LOGO},
            'doc': {'title': 'แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ', 'no': no, 'is_draft': draft, 'form_code': 'FM-SAL-21', 'revision': 'Rev.00 : 01/07/2569'},
            'period_month_text': 'กันยายน 2569', 'blocks': blocks(cols),
            'conclusion_lines': lines(concl), 'suggestion_lines': lines(sugg), 'sign_rows': chunk_signs(signs, PC),
            'layout': {'dense': len(cols) > PC['dense_when_rows_over'], 'dense_signs': len(chain_) > PC['sign_layout']['dense_when_steps_over']}}

def col(i, sc):
    return {'name': f'ลูกค้าตัวอย่าง ในประเทศ {i + 1:02d}', 'ref': f'{(i * 3) % 27 + 2} ก.ย. 69 · SDA-2569-{i + 11:04d}', 'scores': sc}
GOOD = [[5, 4, 4, 5, 5], [4, 4, 5, 4, 5], [5, 5, 4, 4, 4], [4, 5, 5, 5, 4], [5, 4, 4, 4, 5], [4, 4, 4, 5, 5]]
LOWS = [[3, 2, 1, 2, 3], [4, 3, 2, 2, 4], [2, 3, 3, 1, 3]]
REQ = {'role': 'ผู้สรุปผลการประเมิน', 'name': 'สมมติ ใจดี', 'position': 'Sales Administrative Manager', 'date': 'ส่งในระบบ 3 ต.ค. 2569 10:15 น.'}
STEP = [('role-ceo', 'ผู้รับทราบและอนุมัติ', 'ตัวอย่าง บริหารงาน', 'Managing Director')]
def chain(steps, statuses):
    return [{'role_id': r, 'label': l, 'name': n if st != 'waiting' else '', 'position': p, 'status': st,
             'date': f'พิจารณาในระบบ 4 ต.ค. 2569 1{i}:00 น.'} for i, ((r, l, n, p), st) in enumerate(zip(steps, statuses))]
C1 = 'ลูกค้าส่วนใหญ่พึงพอใจระดับมากถึงมากที่สุดทุกหัวข้อ โดยเฉพาะความรวดเร็วในการตอบคำถามและคุณภาพสินค้า'
S1 = 'คงมาตรฐานการตอบกลับภายในวันเดียวกัน และแจ้งข้อมูลสินค้าใหม่ให้ลูกค้าล่วงหน้า'
CL = 'ลูกค้า 3 รายให้ระดับ น้อย ถึง ควรปรับปรุง ในหัวข้อการแก้ไขปัญหาสินค้าเสียหายและความเหมาะสมในการแก้ปัญหา'
LONG_C = ('ภาพรวมเดือนนี้ลูกค้าในประเทศ 12 รายให้ระดับความพึงพอใจมากถึงมากที่สุดในหัวข้อความรวดเร็วในการตอบคำถามและคุณภาพสินค้า '
          'ขณะที่หัวข้อการแก้ไขปัญหากรณีสินค้าเสียหายยังมีลูกค้าบางรายให้ระดับปานกลางถึงน้อย เนื่องจากระยะเวลารอเปลี่ยนสินค้าเกินกว่าที่ตกลง\n') * 3
LONG_S = ('กำหนดขั้นตอนรับเรื่องสินค้าเสียหายให้ชัดเจน ตอบรับภายใน 24 ชั่วโมง และติดตามผลกับลูกค้าจนปิดเรื่อง '
          'พร้อมทบทวนการบรรจุหีบห่อร่วมกับฝ่ายคลังสินค้าทุกเดือน\n') * 3
st = {
 'draft': build('SDS-2569-0004', True, [col(i, GOOD[i]) for i in range(3)], '', '', dict(REQ, date=''), chain(STEP, ['waiting'])),
 'approved': build('SDS-2569-0004', False, [col(i, GOOD[i]) for i in range(6)], C1, S1, REQ, chain(STEP, ['approved'])),
 'rejected': build('SDS-2569-0005', False, [col(i, LOWS[i]) for i in range(3)] + [col(3 + i, GOOD[i]) for i in range(2)], CL, '', REQ, chain(STEP, ['rejected'])),
 'long-12customers': build('SDS-2569-0006', False, [col(i, (GOOD + LOWS + GOOD)[i]) for i in range(12)], LONG_C, LONG_S, REQ, chain(STEP, ['approved'])),
}
six = [('role-ceo' if i == 5 else 'role-mgr-sales', f'ขั้นที่ {i + 1}', f'ผู้อนุมัติสมมติ {i + 1}', 'ผู้จัดการ') for i in range(6)]
st['approved-doa6steps'] = build('SDS-2569-0007', False, [col(i, GOOD[i]) for i in range(6)], C1, S1, REQ, chain(six, ['approved'] * 6))
for k, v in st.items():
    json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: (len(v['conclusion_lines']), len(v['suggestion_lines']), [len(r['signs']) for r in v['sign_rows']]) for k, v in st.items()})
