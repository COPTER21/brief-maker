"""ข้อมูลตัวอย่าง FM-WHS-03 ใบตรวจเช็คถังดับเพลิง — ข้อมูลสมมติทั้งหมด (ไม่ใช้ชื่อ/ข้อมูลจริงจากไฟล์ลูกค้า) · โลโก้ placeholder"""
import json, os, base64
HERE = os.path.dirname(os.path.abspath(__file__))
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
MIN = PC['min_rows']; MK = PC['row_marks']
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"><rect width="300" height="80" fill="#fff"/><text x="150" y="52" font-size="34" text-anchor="middle" font-family="sans-serif" fill="#888">COMPANY LOGO</text></svg>'.encode()).decode()
MONTHS = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
INSP = ['สมชาย ตรวจดี', 'สุดา ปลอดภัย']
def row(i, bad=()):
    m = lambda k: MK['abnormal'] if k in bad else MK['normal']
    return {'check_date': f'{5 + (i // 12)} {MONTHS[i % 12]} {69 + (i // 12)}', 'gauge': m('gauge'), 'seal_pin': m('seal_pin'),
            'hose': m('hose'), 'body': m('body'), 'inspector': INSP[i % 2]}
def build(no, rows, cancelled=False):
    rs = list(rows)
    while len(rs) < MIN: rs.append({'check_date': '', 'gauge': '', 'seal_pin': '', 'hose': '', 'body': '', 'inspector': ''})
    return {'company': {'name': 'บริษัท ตัวอย่าง จำกัด (มหาชน)', 'address_line1': '99 อาคารตัวอย่าง ชั้น 9 ถนนตัวอย่าง',
                        'address_line2': 'แขวงตัวอย่าง เขตตัวอย่าง กรุงเทพ 10000', 'logo': LOGO},
            'doc': {'title': 'ใบตรวจเช็คถังดับเพลิง', 'no': no, 'is_cancelled': cancelled, 'form_code': PC['form_code'], 'revision': PC['revision']},
            'location': 'โซน A1 คลังสินค้า', 'checks': rs, 'layout': {'dense': len(rows) > PC['dense_when_rows_over']}}
st = {
    'active-3rows': build('FEC-2569-0001', [row(i) for i in range(3)]),
    'full-12rows': build('FEC-2569-0001', [row(i) for i in range(12)]),
    'abnormal': build('FEC-2569-0002', [row(i, ('gauge',) if i == 4 else ('seal_pin', 'hose') if i == 7 else ()) for i in range(9)]),
    'long-24rows': build('FEC-2569-0003', [row(i, ('body',) if i == 15 else ()) for i in range(24)]),
    'cancelled': build('FEC-2569-0004', [row(i) for i in range(2)], cancelled=True),
}
for k, v in st.items():
    json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: len(v['checks']) for k, v in st.items()})
