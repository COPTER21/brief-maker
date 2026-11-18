"""ข้อมูลตัวอย่าง FM-SAL-23 (ข้อมูลสมมติทั้งหมด · โลโก้ placeholder) — 5 สถานะ · ช่องลงชื่อจาก sign_rows.py
data contract: company · doc · period_month_text · blocks[2]{cols[4]{name}, rows[13]{topic, grp, cells[4]{v}}} · conclusion_lines · suggestion_lines · sign_rows · layout"""
import json, sys, os, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ['TD'], 'scripts'))
from sign_rows import build_signs, chunk_signs
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"><rect width="300" height="80" fill="#fff"/><text x="150" y="52" font-size="34" text-anchor="middle" font-family="sans-serif" fill="#888">COMPANY LOGO</text></svg>'.encode()).decode()
GROUPS = [('ด้านการสื่อสารและการตอบสนอง', ['ความชัดเจนในการสื่อสาร', 'ความรวดเร็วในการตอบกลับ', 'การติดตามงานอย่างสม่ำเสมอ']),
          ('ด้านเอกสารและการดำเนินงาน', ['ความถูกต้องของเอกสาร', 'ความรวดเร็วในการส่งเอกสาร', 'การสนับสนุนประสานงานขนส่ง', 'การแก้ปัญหาอย่างมีประสิทธิภาพ', 'การอัปเดตสถานะงาน']),
          ('ด้านความเป็นมืออาชีพ', ['ความเป็นมืออาชีพของทีมงาน', 'ความพึงพอใจในบริการ'])]
NQ = 10
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

def rows_for(cs):
    rows, q = [], 0
    for g, items in GROUPS:
        rows.append({'topic': g, 'grp': True, 'cells': []})
        for t in items:
            rows.append({'topic': t, 'grp': False, 'cells': [{'v': str(c['scores'][q]) if c['scores'][q] else ''} for c in cs]})
            q += 1
    return rows

def blocks(cols):
    """cols: [{name, scores:[10 ints]}] ≤ 8 → 2 ชุด × 4 คอลัมน์ (เติมช่องว่างให้ครบ 8)"""
    cols = list(cols) + [{'name': '', 'scores': [None] * NQ}] * (NCOL - len(cols))
    return [{'cols': [{'name': c['name']} for c in cols[b:b + PER]], 'rows': rows_for(cols[b:b + PER])} for b in range(0, NCOL, PER)]

def build(no, draft, cols, concl, sugg, req, chain_):
    signs = build_signs(req, chain_, PC)
    return {'company': {'name': 'บริษัท ตัวอย่าง จำกัด', 'logo': LOGO},
            'doc': {'title': 'แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ', 'no': no, 'is_draft': draft, 'form_code': 'FM-SAL-23', 'revision': 'Rev.00 : 01/07/2569'},
            'period_month_text': 'กันยายน 2569', 'blocks': blocks(cols),
            'conclusion_lines': lines(concl), 'suggestion_lines': lines(sugg), 'sign_rows': chunk_signs(signs, PC),
            'layout': {'dense': len(cols) > PC['dense_when_rows_over'], 'dense_signs': len(chain_) > PC['sign_layout']['dense_when_steps_over']}}

NAMES = ['Sample Global Trading', 'Demo Ocean Commodities', 'Example Agri Export', 'Mock Pacific Feeds', 'Test Harbor Resources', 'Placeholder Sugar Asia', 'Fictive Molasses Ltd.', 'Dummy Bulk Logistics']
def col(i, sc):
    return {'name': NAMES[i], 'scores': sc}
GOOD = [[5, 4, 5, 5, 4, 5, 4, 5, 5, 5], [4, 5, 4, 4, 5, 4, 5, 4, 5, 4], [5, 5, 4, 5, 5, 4, 4, 4, 4, 5], [4, 4, 5, 4, 4, 5, 5, 5, 4, 4]]
LOWS = [[3, 2, 2, 3, 1, 2, 3, 2, 3, 3], [4, 3, 3, 2, 2, 3, 2, 3, 4, 3]]
REQ = {'role': 'ผู้สรุปผลการประเมิน', 'name': 'สมมติ ใจดี', 'position': 'Sales Administrative Manager', 'date': 'ส่งในระบบ 3 ต.ค. 2569 10:15 น.'}
STEP = [('role-ceo', 'ผู้รับทราบและอนุมัติ', 'ตัวอย่าง บริหารงาน', 'Managing Director')]
def chain(steps, statuses):
    return [{'role_id': r, 'label': l, 'name': n if st != 'waiting' else '', 'position': p, 'status': st,
             'date': f'พิจารณาในระบบ 4 ต.ค. 2569 1{i}:00 น.'} for i, ((r, l, n, p), st) in enumerate(zip(steps, statuses))]
C1 = 'ลูกค้าต่างประเทศทั้ง 4 รายให้คะแนน 4–5 ทุกหัวข้อ โดยเฉพาะความชัดเจนในการสื่อสารและความถูกต้องของเอกสาร'
S1 = 'คงมาตรฐานการตอบกลับภายใน 24 ชั่วโมง และแจ้งสถานะการขนส่งเชิงรุกทุกสัปดาห์'
CL = 'ลูกค้า 2 รายให้คะแนน 1–2 ในหัวข้อความรวดเร็วในการส่งเอกสารและการสนับสนุนประสานงานขนส่ง'
LONG_C = ('ภาพรวมเดือนนี้ลูกค้าต่างประเทศ 8 รายให้คะแนน 4–5 ในหัวข้อความชัดเจนในการสื่อสารและความเป็นมืออาชีพของทีมงาน '
          'ขณะที่หัวข้อความรวดเร็วในการส่งเอกสารยังมีลูกค้าบางรายให้คะแนน 2–3 เนื่องจากเอกสารส่งออกล่าช้ากว่ากำหนดเรือออก\n') * 3
LONG_S = ('กำหนดเวลาส่งเอกสารส่งออกล่วงหน้าอย่างน้อย 2 วันก่อนเรือออก และติดตามสถานะกับ forwarder ทุกวัน '
          'พร้อมทบทวนขั้นตอนประสานงานขนส่งร่วมกับฝ่ายคลังสินค้าทุกเดือน\n') * 3
st = {
 'draft': build('SES-2569-0004', True, [col(i, GOOD[i]) for i in range(2)], '', '', dict(REQ, date=''), chain(STEP, ['waiting'])),
 'approved': build('SES-2569-0004', False, [col(i, GOOD[i]) for i in range(4)], C1, S1, REQ, chain(STEP, ['approved'])),
 'rejected': build('SES-2569-0005', False, [col(i, LOWS[i]) for i in range(2)] + [col(2 + i, GOOD[i]) for i in range(2)], CL, '', REQ, chain(STEP, ['rejected'])),
 'long-8customers': build('SES-2569-0006', False, [col(i, (GOOD + LOWS + GOOD)[i]) for i in range(8)], LONG_C, LONG_S, REQ, chain(STEP, ['approved'])),
}
six = [('role-ceo' if i == 5 else 'role-mgr-sales', f'ขั้นที่ {i + 1}', f'ผู้อนุมัติสมมติ {i + 1}', 'ผู้จัดการ') for i in range(6)]
st['approved-doa6steps'] = build('SES-2569-0007', False, [col(i, GOOD[i]) for i in range(4)], C1, S1, REQ, chain(six, ['approved'] * 6))
for k, v in st.items():
    json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: (len(v['conclusion_lines']), len(v['suggestion_lines']), [len(r['signs']) for r in v['sign_rows']]) for k, v in st.items()})
