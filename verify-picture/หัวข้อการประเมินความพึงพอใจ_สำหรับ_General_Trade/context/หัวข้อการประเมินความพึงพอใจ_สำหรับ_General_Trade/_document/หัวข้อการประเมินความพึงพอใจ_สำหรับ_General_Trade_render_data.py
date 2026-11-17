"""ข้อมูลตัวอย่าง FM-SAL-11 (ข้อมูลสมมติทั้งหมด · โลโก้ placeholder) — 5 สถานะ · ช่องลงชื่อจาก sign_rows.py"""
import json, sys, os, base64
from decimal import Decimal, ROUND_HALF_UP
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ['TD'], 'scripts'))
from sign_rows import build_signs, chunk_signs
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"><rect width="300" height="80" fill="#fff"/><text x="150" y="52" font-size="34" text-anchor="middle" font-family="sans-serif" fill="#888">COMPANY LOGO</text></svg>'.encode()).decode()
LEVELS = [('มากที่สุด', 5), ('มาก', 4), ('ปานกลาง', 3), ('น้อย', 2), ('ต้องปรับปรุง', 1)]
SECTIONS = [('1) ด้านคุณภาพสินค้า/บริการ', 'ด้านคุณภาพสินค้า/บริการ', ['1. คุณภาพของสินค้าโดยรวม', '2. ระดับคุณภาพสินค้าเมื่อเทียบกับบริษัทอื่นๆ', '3. การปรับปรุงคุณภาพสินค้าและบริการให้ดีขึ้นอย่างต่อเนื่อง', '4. ความรวดเร็วในการแก้ไขปัญหาและหาทางป้องกันไม่ให้เกิดซ้ำ']),
            ('2) ด้านการส่งมอบสินค้า', 'ด้านการส่งมอบสินค้า', ['1. การส่งมอบตามเวลาที่ได้นัดหมายไว้', '2. การบรรจุหีบห่อสินค้าอยู่ในสภาพสมบูรณ์', '3. สภาพโดยรวมของพนักงานส่งของและรถขนส่งสินค้า', '4. มาตรฐานการขนส่งสินค้าเมื่อเทียบกับบริษัทอื่นๆ']),
            ('3) ด้านเจ้าหน้าที่ผู้ให้บริการ/พนักงานขาย', 'ด้านเจ้าหน้าที่ผู้ให้บริการ/พนักงานขาย', ['1. พนักงานสนใจไปเยี่ยมเยียน สอบถามความต้องการลูกค้าทั้งก่อนและหลังการขาย', '2. พนักงานมีความรู้ความชำนาญในตัวสินค้า สามารถแนะนำ ตอบข้อซักถามได้ชัดเจน', '3. พนักงานสามารถแก้ปัญหา/อุปสรรคที่เกิดขึ้นได้ อย่างเหมาะสม', '4. พนักงานให้บริการด้วยความรวดเร็ว/เอาใจใส่ และเต็มใจให้บริการ', '5. พนักงานพูดจาสุภาพ อัธยาศัยดี แต่งกายสุภาพ วางตัวเหมาะสม', '6. ความรวดเร็วในการตอบกลับข้อมูลต่างๆ ของพนักงาน', '7. การติดต่อสื่อสารทางโทรศัพท์ และมีประสิทธิภาพ', '8. พนักงานตรงต่อเวลาและปฏิบัติตามเงื่อนไข ที่ให้กับลูกค้า'])]
BANDS = [(80, 'ลูกค้ามีความพึงพอใจสูง'), (60, 'ลูกค้าพึงพอใจในระดับปานกลาง'), (0, 'ลูกค้าอาจมีความไม่พึงพอใจ')]
MIN_ORDERS = 3
pct2 = lambda x: str(Decimal(x).quantize(Decimal('0.01'), ROUND_HALF_UP))
def bands_print():
    return [{'range': '80% – 100%', 'text': BANDS[0][1]}, {'range': '60% – 79%', 'text': BANDS[1][1]}, {'range': 'ต่ำกว่า 60%', 'text': BANDS[2][1]}]
def level(p):
    return next(t for lo, t in BANDS if p >= lo)
def section(si, counts, blank):
    head, col, topics = SECTIONS[si]; items = []; sums = [0] * 5; wsum = 0; tot = 0
    for i, t in enumerate(topics):
        c = counts[i] if not blank else [None] * 5
        rt = sum(x or 0 for x in c)
        for k in range(5): sums[k] += c[k] or 0
        wsum += sum((c[k] or 0) * LEVELS[k][1] for k in range(5)); tot += rt
        items.append({'topic': t, 'counts': [{'v': '' if x is None else str(x)} for x in c], 'total': str(rt), 'pct_cell': None})
    pct = '—' if tot == 0 else pct2(Decimal(wsum) * 100 / (Decimal(5) * tot))
    items[0]['pct_cell'] = {'rowspan': str(len(topics) + 1), 'pct': pct}
    return {'heading': head, 'col_title': col, 'levels': [{'label': l} for l, _ in LEVELS], 'items': items,
            'sums': [{'v': str(s)} for s in sums], 'sum_total': str(tot)}, wsum, tot
def build(no, draft, cnts, customers, req, chain_, blank=False):
    secs, W, T = [], 0, 0
    for si in range(3):
        s, w, t = section(si, cnts[si], blank); secs.append(s); W += w; T += t
    op = None if T == 0 else Decimal(W) * 100 / (Decimal(5) * T)
    rows = [{'name': n, 'order_count': str(o)} for n, o in customers]
    while len(rows) < PC['min_rows']: rows.append({'name': '', 'order_count': ''})
    signs = build_signs(req, chain_, PC)
    return {'company': {'name': 'บริษัท ตัวอย่าง จำกัด', 'logo': LOGO},
            'doc': {'title': 'หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade', 'no': no, 'is_draft': draft, 'form_code': 'FM-SAL-11', 'revision': 'Rev.00: 01/07/2569'},
            'period_month': 'กันยายน 2569', 'sections': secs,
            'overall_pct': '—' if op is None else pct2(op), 'overall_level': '' if op is None else level(op),
            'policy': {'min_orders': str(MIN_ORDERS), 'bands': bands_print()},
            'customers': rows, 'sign_rows': chunk_signs(signs, PC),
            'layout': {'dense': len(customers) > PC['dense_when_rows_over'], 'dense_signs': len(chain_) > PC['sign_layout']['dense_when_steps_over']}}
A = [[6, 4, 2, 0, 0], [5, 5, 2, 0, 0], [4, 6, 1, 1, 0], [5, 4, 3, 0, 0]]
B = [[7, 4, 1, 0, 0], [6, 5, 1, 0, 0], [4, 5, 2, 1, 0], [5, 5, 2, 0, 0]]
C = [[6, 5, 1, 0, 0], [7, 4, 1, 0, 0], [5, 5, 2, 0, 0], [6, 4, 2, 0, 0], [8, 3, 1, 0, 0], [5, 5, 1, 1, 0], [4, 6, 2, 0, 0], [6, 4, 1, 1, 0]]
LOW = [[[1, 2, 4, 3, 2]] * 4, [[1, 3, 3, 3, 2]] * 4, [[2, 2, 3, 3, 2]] * 8]
CUST = [(f'ร้านค้าตัวอย่าง GT {i + 1:02d}', 3 + (i * 7) % 6) for i in range(12)]
REQ = {'role': 'Sales Manager', 'name': 'สมมติ ใจดี', 'position': 'Sales Manager', 'date': 'ส่งในระบบ 3 ต.ค. 2569 10:15 น.'}
STEP = [('role-mgr-bu', 'ผู้อำนวยการสายงานการขาย', 'ตัวอย่าง บริหารงาน', 'ผู้อำนวยการสายงานการขาย')]
def chain(steps, statuses):
    return [{'role_id': r, 'label': l, 'name': n if st != 'waiting' else '', 'position': p if st != 'waiting' else '', 'status': st,
             'date': f'พิจารณาในระบบ 4 ต.ค. 2569 1{i}:00 น.'} for i, ((r, l, n, p), st) in enumerate(zip(steps, statuses))]
st = {
 'draft': build('CSM-2569-0009', True, [A, B, C], CUST[:5], dict(REQ, date=''), chain(STEP, ['waiting']), blank=True),
 'approved': build('CSM-2569-0009', False, [A, B, C], CUST, REQ, chain(STEP, ['approved'])),
 'rejected': build('CSM-2569-0010', False, LOW, CUST[:8], REQ, chain(STEP, ['rejected'])),
 'long-22customers': build('CSM-2569-0011', False, [A, B, C], [(f'ร้านค้าตัวอย่าง GT {i + 1:02d}', 3 + i % 9) for i in range(22)], REQ, chain(STEP, ['approved'])),
}
six = [('role-mgr-bu' if i == 5 else 'role-mgr-sales', f'ขั้นที่ {i + 1}', f'ผู้อนุมัติสมมติ {i + 1}', 'ผู้จัดการ') for i in range(6)]
st['approved-doa6steps'] = build('CSM-2569-0012', False, [A, B, C], CUST, REQ, chain(six, ['approved'] * 6))
for k, v in st.items():
    json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: (v['overall_pct'], v['overall_level'], [len(r['signs']) for r in v['sign_rows']], len(v['customers'])) for k, v in st.items()})
