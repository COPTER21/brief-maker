"""FM-SAL-16 ฟอร์มแจ้งงานขนส่งนอก — data ตัวอย่างทุกสถานะ (ข้อมูลสมมติทั้งหมด · โลโก้ placeholder · ไม่ใช้ข้อมูลจริงลูกค้า)
data contract: ทุกค่าแสดงเป็น string จัดรูปแล้ว · lines เติมแถวว่างจนครบ min_rows · sign_rows จาก sign_rows.py (ผู้จัดทำ + ขั้น DOA ถ้ามี)"""
import json, os, sys, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ.get('SKILLS_ROOT', ''), 'pack', 'thai-doc-pdf-generator', 'scripts'))
from sign_rows import build_signs, chunk_signs
SPEC = json.load(open(os.path.join(HERE, '..', 'FORM_SPEC.json'), encoding='utf-8'))
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"><rect width="300" height="80" fill="#fff"/><text x="150" y="52" font-size="34" text-anchor="middle" font-family="sans-serif" fill="#888">COMPANY LOGO</text></svg>'.encode()).decode()
MIN = PC['min_rows']; WRAP = 30   # ตัวอักษรต่อบรรทัดในช่องแคบสุดโดยประมาณ → เกินแล้ว dense

def fmt_qty(n): return f'{n:,}'

def lines(rows):
    out = [{'origin': o, 'destination': d, 'po_no': p, 'qty': fmt_qty(q), 'delivery_date': dt} for o, d, p, q, dt in rows]
    while len(out) < MIN: out.append({'origin': '', 'destination': '', 'po_no': '', 'qty': '', 'delivery_date': ''})
    return out

def build(no, *, draft=False, cancelled=False, carrier='', round_date='', rows=(), preparer='', sent='', chain=()):
    L = lines(list(rows))
    req = {'role': 'ผู้จัดทำ', 'name': preparer, 'date': sent}
    signs = build_signs(req, list(chain), PC)
    long_text = any(len(r['origin']) > WRAP or len(r['destination']) > WRAP for r in L)
    return {'company': {'name': 'บริษัท ตัวอย่าง จำกัด', 'logo': LOGO},
            'doc': {'title': SPEC['form']['title'], 'no': no, 'is_draft': draft, 'is_cancelled': cancelled,
                    'form_code': PC['form_code'], 'revision': PC['revision']},
            'carrier_name': carrier, 'round_date_text': round_date,
            'lines': L,
            # TODO: DOA engine — ไม่มีการอนุมัติ (DEC-03) · approval_chain ว่าง → sign_rows = ผู้จัดทำ 1 ช่อง
            'approver_role': '', 'approved_by': '', 'approval_chain': list(chain),
            'sign_rows': chunk_signs(signs, PC),
            'layout': {'dense': len(L) > PC['dense_when_rows_over'] or long_text or len(chain) > PC['sign_layout']['dense_when_steps_over']}}

R = [('คลังสินค้า บางนา', 'ร้านสมใจการค้า (ชลบุรี)', 'PO-6903-0141', 120, '16/03/2569'),
     ('คลังสินค้า บางนา', 'หจก. รุ่งเรืองพาณิชย์ (ระยอง)', 'PO-6903-0142', 80, '16/03/2569'),
     ('โรงงาน วังน้อย', 'บริษัท มั่นคงค้าส่ง จำกัด (สระบุรี)', 'PO-6903-0150', 1500, '17/03/2569'),
     ('คลังสินค้า บางนา', 'ร้านเจริญดีมาร์ท (ฉะเชิงเทรา)', 'PO-6903-0153', 45, '17/03/2569'),
     ('โรงงาน วังน้อย', 'ร้านทองดีค้าปลีก (อยุธยา)', 'PO-6903-0155', 300, '18/03/2569'),
     ('คลังสินค้า บางนา', 'บริษัท สยามสโตร์ จำกัด (นนทบุรี)', 'PO-6903-0158', 600, '18/03/2569'),
     ('โรงงาน วังน้อย', 'ร้านใจดีพาณิชย์ (ลพบุรี)', 'PO-6903-0160', 75, '19/03/2569'),
     ('คลังสินค้า บางนา', 'หจก. ศรีสุขค้าส่ง (ปราจีนบุรี)', 'PO-6903-0161', 240, '19/03/2569')]
LONG = [('คลังสินค้า บางนา' if i % 2 else 'โรงงาน วังน้อย', ('บริษัท มั่นคงค้าส่งทั่วไทย จำกัด สาขาหนองแค จ.สระบุรี' if i % 4 == 0 else R[i % 8][1]), f'PO-6904-{200+i:04d}', 100 + 37 * i, f'{(i % 9) + 21:02d}/04/2569') for i in range(MIN)]   # 20 แถวเต็ม · ทุก 4 แถวมีปลายทางยาว 2 บรรทัด
ST = {
 'draft': build('OTN-2569-0007', draft=True, carrier='บริษัท ขนส่งตัวอย่าง จำกัด', round_date='15 มีนาคม 2569', rows=R[:3]),
 'submitted': build('OTN-2569-0007', carrier='บริษัท ขนส่งตัวอย่าง จำกัด', round_date='15 มีนาคม 2569', rows=R,
                    preparer='นางสาวตัวอย่าง ใจดี', sent='ส่งในระบบ 15/03/2569 10:42'),
 'cancelled': build('OTN-2569-0005', cancelled=True, carrier='หจก. รถร่วมตัวอย่าง', round_date='14 มีนาคม 2569', rows=R[:2],
                    preparer='นางสาวตัวอย่าง ใจดี', sent='ส่งในระบบ 14/03/2569 16:05'),
 'long-20rows': build('OTN-2569-0021', carrier='บริษัท ขนส่งตัวอย่างทั่วไทย โลจิสติกส์ จำกัด', round_date='20 เมษายน 2569', rows=LONG,
                      preparer='นายสมมติ ทดสอบระบบ', sent='ส่งในระบบ 20/04/2569 09:15'),
 'blank': build('', draft=True),
}
if __name__ == '__main__':
    for k, v in ST.items():
        json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print({k: (sum(1 for r in v['lines'] if r['po_no']), len(v['lines']), v['layout']['dense'], [len(r['signs']) for r in v['sign_rows']]) for k, v in ST.items()})
