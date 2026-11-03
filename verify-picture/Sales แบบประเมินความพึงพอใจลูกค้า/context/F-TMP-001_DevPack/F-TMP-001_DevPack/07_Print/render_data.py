"""ข้อมูลตัวอย่าง FM-SAL-06 แบบประเมินความพึงพอใจ (ข้อมูลสมมติทั้งหมด · โลโก้ placeholder · ไม่ใช้ข้อมูลจากไฟล์ลูกค้า)"""
import json, os, sys, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ['TD'], 'scripts'))
from sign_rows import build_signs, chunk_signs
PC = json.load(open(os.path.join(HERE, 'print_config.json'), encoding='utf-8'))
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"><rect width="300" height="80" fill="#fff"/><text x="150" y="52" font-size="34" text-anchor="middle" font-family="sans-serif" fill="#888">COMPANY LOGO</text></svg>'.encode()).decode()
CO = 'บริษัท ตัวอย่างการค้า จำกัด (มหาชน)'
BT = ['hypermarket', 'supermarket', 'wholesales', 'convenience']
RY = [('lt1', 'lt1'), ('1-3', 'y1_3'), ('3-5', 'y3_5'), ('gt5', 'gt5')]
RK = ['quality', 'on_time_delivery', 'stock_replenishment', 'communication', 'trade_terms', 'marketing_support', 'after_sales', 'sales_professionalism', 'overall']
def build(no, draft, store, bt, ry, scores, sug, evaluator, date):
    signs = build_signs({'role': 'ผู้ประเมิน', 'name': evaluator[0], 'position': evaluator[1], 'date': date}, [], PC)
    return {'company': {'name': CO, 'logo': LOGO},
            'doc': {'title': 'แบบฟอร์มประเมินความพึงพอใจของ' + CO.replace('บริษัท ', 'บริษัท', 1), 'no': no, 'is_draft': draft,
                    'form_code': PC['form_code'], 'revision': PC['revision']},
            'store': {'name': store}, 'partner': {'company_name': CO},
            'business_type': {f'{k}_box': '☑' if k == bt else '☐' for k in BT},
            'relationship_years': {f'{k}_box': '☑' if v == ry else '☐' for v, k in RY},
            'rating': {k: (str(s) if s else '') for k, s in zip(RK, scores)},
            'suggestion': sug, 'sign_rows': chunk_signs(signs, PC), 'layout': {'dense': len(sug) > 400}}
SENT = 'ส่งในระบบ 8 ต.ค. 2569 10:15 น.'
EV = ('สมหญิง ตั้งใจงาน', 'เจ้าหน้าที่ขาย')  # ผู้ประเมิน = ผู้บันทึกในระบบ (AI-DEFAULT)
st = {
 'draft': build('CSE-2569-0001', True, 'ร้านตัวอย่างมินิมาร์ท', 'convenience', '', [5, 4, 0, 0, 0, 0, 0, 0, 0], '', EV, ''),
 'submitted': build('CSE-2569-0001', False, 'ห้างสรรพสินค้าสมมติ สาขาตัวอย่าง', 'hypermarket', '3-5', [5, 4, 4, 3, 4, 3, 4, 5, 4],
                    'อยากให้แจ้งรอบส่งสินค้าล่วงหน้าอย่างน้อย 2 วัน', EV, SENT),
 'alt-choices-low': build('CSE-2569-0002', False, 'ร้านค้าส่งตัวอย่าง', 'wholesales', 'lt1', [2, 1, 2, 3, 1, 2, 2, 3, 2],
                    'สินค้าขาดสต็อกบ่อย ควรปรับรอบเติมสินค้า', ('วิชัย ขายดี', 'พนักงานขาย'), SENT),
 'long-suggestion': build('CSE-2569-0003', False, 'ซูเปอร์มาร์เก็ตสมมติ', 'supermarket', 'gt5', [4, 4, 4, 4, 4, 4, 4, 4, 4],
                    ' '.join(['ข้อเสนอแนะยาวสำหรับทดสอบการตัดบรรทัดของกล่องข้อเสนอแนะ ให้พิมพ์ได้ภายในหนึ่งหน้า'] * 8), EV, SENT),
 'blank-print': build('', True, '', '', '', [0] * 9, '', ('', ''), ''),
}
for k, v in st.items():
    json.dump(v, open(os.path.join(HERE, f'{k}.data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: [len(r['signs']) for r in v['sign_rows']] for k, v in st.items()})
