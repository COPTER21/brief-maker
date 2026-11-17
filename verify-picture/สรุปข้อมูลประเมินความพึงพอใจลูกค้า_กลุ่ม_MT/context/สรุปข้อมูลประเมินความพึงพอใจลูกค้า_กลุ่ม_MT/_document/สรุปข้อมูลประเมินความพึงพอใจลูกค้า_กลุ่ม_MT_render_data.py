"""ข้อมูลตัวอย่าง FM-SAL-07 (ข้อมูลสมมติทั้งหมด) — 5 สถานะ · ช่องลงชื่อจาก sign_rows.py (ผู้สรุป 1 ช่อง · ไม่มี DOA)"""
import json, sys, os
from decimal import Decimal, ROUND_HALF_UP
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ['TD'], 'scripts'))
from sign_rows import build_signs, chunk_signs
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
TITLE = 'สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT'
CRIT = ['คุณภาพของสินค้า/บริการ', 'ความตรงต่อเวลาในการส่งสินค้า', 'การจัดการสต็อกสินค้าและการเติมสินค้า', 'การสื่อสารและการให้ข้อมูลข่าวสาร',
        'เงื่อนไขทางการค้า (ราคา โปรโมชั่น การชำระเงิน)', 'การสนับสนุนด้านการตลาดและส่งเสริมการขาย', 'การแก้ไขปัญหาและการให้บริการหลังการขาย',
        'ความเป็นมืออาชีพของพนักงานขาย/ทีมงาน', 'ความพึงพอใจโดยรวมต่อบริษัทคู่ค้า']
MAX = [5] * 9
CH = ['บิ๊กซี', 'lotus', 'makro', 'Foodland', 'แมคแวลู่', 'Homepro', '108', 'วิลล่า', 'จิฟฟี่', 'เลม่อนฟาร์ม', 'UFM', 'The mall', 'Tops', 'Do home', 'PT']
STD, LOW = 95, 80
BANDS = [('pass', 'ผ่านมาตรฐาน'), ('below', 'ต่ำกว่ามาตรฐาน'), ('far', 'ค่อนข้างต่ำกว่ามาตรฐาน')]
NOTES = {'pass': 'ควร รักษาคุณภาพ และ สร้างกรณีศึกษา (Best Practice)',
         'below': 'ควร ปรับปรุงบางด้าน เช่น การสื่อสาร หรือความสะดวกในการซื้อสินค้า',
         'far': 'ต้องเร่งแก้ไขอย่างเร่งด่วน'}
pct2 = lambda x: str(Decimal(x).quantize(Decimal('0.01'), ROUND_HALF_UP))
def band(p):
    return 'pass' if p >= STD else ('below' if p >= LOW else 'far')
def group_labels():
    return {'pass': f'ช่องทางที่ ผ่านมาตรฐาน {STD}% ขึ้นไป ได้แก่:', 'below': f'ช่องทางที่ ต่ำกว่ามาตรฐานเล็กน้อย ({LOW}–{STD - 1}%) ได้แก่:', 'far': f'ช่องทางที่ ต่ำกว่า {LOW}% ได้แก่:'}
def legend():
    return [{'label': 'ผ่านมาตรฐาน', 'range': f'% ตั้งแต่ {STD} ขึ้นไป'}, {'label': 'ต่ำกว่ามาตรฐาน', 'range': f'% ตั้งแต่ {LOW} แต่ไม่ถึง {STD}'}, {'label': 'ค่อนข้างต่ำกว่ามาตรฐาน', 'range': f'% ต่ำกว่า {LOW}'}]
def build(no, draft, cancelled, scores, recs, notes=None, req_date='', ass='', summ=''):
    """scores: dict channel_index -> list[9] (int or None) · ไม่มี key = ไม่ได้ประเมิน"""
    maxt = sum(MAX); per = PC['channels_per_block']; blocks = []; status = {}
    for b0 in range(0, len(CH), per):
        idx = list(range(b0, min(b0 + per, len(CH)))); pad = per - len(idx)
        chans = [{'name': CH[i]} for i in idx] + [{'name': ''}] * pad
        rows = []
        for r in range(len(CRIT)):
            vals = []
            for i in idx:
                s = scores.get(i)
                vals.append({'v': '' if not s or s[r] is None else str(s[r])})
            rows.append({'topic': CRIT[r], 'max': str(MAX[r]), 'scores': vals + [{'v': ''}] * pad})
        tots, pcts, sts = [], [], []
        for i in idx:
            s = scores.get(i)
            if s and all(x is not None for x in s):
                t = sum(s); p = Decimal(t) * 100 / Decimal(maxt); bd = band(p); status[i] = bd
                tots.append({'v': str(t)}); pcts.append({'v': pct2(p) + '%'}); sts.append({'v': dict(BANDS)[bd]})
            else:
                tots.append({'v': '' if not s else str(sum(x or 0 for x in s))}); pcts.append({'v': '—'}); sts.append({'v': ''})
        blocks.append({'channels': chans, 'rows': rows, 'max_total': str(maxt), 'totals': tots + [{'v': ''}] * pad,
                       'pcts': pcts + [{'v': ''}] * pad, 'statuses': sts + [{'v': ''}] * pad})
    gl = group_labels(); nt = dict(NOTES, **(notes or {})); groups = []
    for key, _ in BANDS:
        names = [CH[i] for i in range(len(CH)) if status.get(i) == key]
        groups.append({'label': gl[key], 'channels': ', '.join(names) if names else '—', 'note': nt[key], 'is_alert': key == 'far'})
    rr = [{'no': f'{k + 1}.', 'text': t} for k, t in enumerate(recs)]
    while len(rr) < PC['min_rows']: rr.append({'no': f'{len(rr) + 1}.', 'text': ''})
    req = {'role': 'ผู้สรุปการประเมิน', 'name': 'สมมติ ใจดี', 'position': 'Sales Manager', 'date': req_date}
    return {'doc': {'title': TITLE, 'no': no, 'is_draft': draft, 'is_cancelled': cancelled, 'form_code': 'FM-SAL-07', 'revision': 'Rev.00: 01/07/2569'},
            'round_no': '1', 'blocks': blocks, 'policy': {'std_pct': str(STD), 'low_pct': str(LOW)}, 'legend': legend(),
            'summary': {'groups': groups}, 'recommendations': rr, 'sign_rows': chunk_signs(build_signs(req, [], PC), PC),
            'assessment_date': ass, 'summary_date': summ, 'layout': {'dense': len(recs) > PC['dense_when_rows_over']}}
# คะแนนสมมติ 9 หัวข้อ ต่อช่องทาง
P5 = [5, 5, 5, 5, 5, 5, 5, 4, 5]      # 44/45 = 97.78 ผ่าน
P4 = [5, 4, 5, 4, 4, 5, 4, 4, 4]      # 39/45 = 86.67 ต่ำกว่ามาตรฐาน
P3 = [4, 3, 3, 4, 3, 3, 4, 3, 3]      # 30/45 = 66.67 ค่อนข้างต่ำ
MIX = {0: P4, 1: P4, 2: P5, 3: P5, 4: P5, 5: P4, 6: P3, 7: P3, 8: P3, 9: P5, 10: [3, 3, 3, 3, 4, 3, 3, 3, 3], 11: P5, 12: P3, 13: P3, 14: [3, 3, 3, 3, 3, 3, 3, 4, 3]}
RECS = ['วิเคราะห์จุดอ่อนรายช่องทาง จากหัวข้อที่ได้คะแนนต่ำ', 'ปรับกลยุทธ์สนับสนุนช่องทางที่อ่อนแอ เช่น จัดอบรมพนักงานหน้าร้าน ปรับโปรโมชั่น เพิ่มการสื่อสาร',
        'นำช่องทางที่คะแนนสูงมาเป็นต้นแบบ เพื่อพัฒนาอีกช่องทาง', 'ติดตามผลซ้ำทุก 6 เดือน เพื่อดูการเปลี่ยนแปลงอย่างชัดเจน']
D1, D2 = '15 กันยายน 2569', '30 กันยายน 2569'
SENT = 'ยืนยันสรุปในระบบ 30 ก.ย. 2569 16:20 น.'
st = {
 'draft': build('MTS-2569-0001', True, False, {0: P4, 1: [5, 4, None, None, None, None, None, None, None]}, RECS[:1], ass=D1, summ=''),
 'final': build('MTS-2569-0002', False, False, MIX, RECS, req_date=SENT, ass=D1, summ=D2),
 'final-allpass': build('MTS-2569-0003', False, False, {i: P5 for i in range(15)}, RECS[2:4], req_date=SENT, ass=D1, summ=D2),
 'cancelled': build('MTS-2569-0004', False, True, {i: MIX[i] for i in range(0, 15, 2)}, RECS, req_date=SENT, ass=D1, summ=D2),
 'long-12recs': build('MTS-2569-0005', False, False, MIX, RECS + [f'ข้อเสนอแนะเพิ่มเติมตัวอย่างข้อที่ {k} — ติดตามผลกับทีมขายช่องทาง MT ทุกเดือนและรายงานความคืบหน้าต่อผู้บริหารฝ่ายขาย' for k in range(5, 13)],
                     notes={'far': 'ต้องเร่งแก้ไขอย่างเร่งด่วน โดยเฉพาะช่องทางที่ได้คะแนนต่ำกว่า 70% ให้จัดประชุมทบทวนแผนร่วมกับลูกค้าภายใน 30 วัน และกำหนดผู้รับผิดชอบรายช่องทาง'}, req_date=SENT, ass=D1, summ=D2),
}
for k, v in st.items():
    json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: [g['channels'] for g in v['summary']['groups']] for k, v in st.items()})
