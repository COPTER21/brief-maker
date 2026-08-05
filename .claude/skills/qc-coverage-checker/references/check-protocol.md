# Check Protocol — วิธีหา evidence ต่อ artifact

## หลัก: หาให้เจอจริง ไม่ใช่หาให้ครบเร็ว

การตรวจ coverage พังได้ 2 ทาง: (a) ✗ ปลอม — หาไม่ละเอียดแล้วสรุปว่าไม่มี
(b) ✓ ปลอม — เห็นคำใกล้เคียงแล้วนับผ่าน ทั้งคู่ทำลายความเชื่อใจใน gate
→ ทุก item ใช้ลำดับค้นนี้ก่อนตัดสิน ✗:

## รอบ 1 — หา evidence ใน HTML

**Edge out (ทางไป node ปลาย):** ค้นตามลำดับ
1. hash routes ที่ชี้ไป node ปลาย (`#/rtv`, `#/credit-note`)
2. ปุ่ม/action ใน view drawer หรือ row action (ข้อความไทย เช่น "ส่งคืน", "สร้างใบลดหนี้")
3. สถานะ/badge ที่เป็นสะพาน (เช่น สถานะ "รับเกิน" ที่เปิด action ต่อ)
4. เมนู sidebar / tab
เจอที่ชั้นไหนจดชั้นนั้นเป็น evidence — ไม่เจอทั้ง 4 ชั้น = ✗

**Edge in (การอ้าง document ต้นทาง):** ช่องเลือก/ค้นหา document ต้นทาง (search-select PO),
การแสดง fields ตาม `edge.fields` (po_no, qty_ordered...), การ validate เทียบต้นทาง
(qty รับ vs สั่ง) — มีช่องเลือกแต่ไม่โชว์ field สำคัญ = ✓ บางส่วน → ลง matrix เป็น
`△ partial` พร้อมระบุ field ที่ขาด

**Golden rule ใน UI:** ดูที่ mock logic/JS, disabled/enabled ตามเงื่อนไข, error/warning
microcopy, ค่าที่คำนวณโชว์ — rule ที่เป็น calculation/posting ฝั่ง backend ล้วน →
`N/A-UI` พร้อมเหตุผล 1 บรรทัด (ห้ามใช้ N/A-UI เป็นทางหนีของ rule ที่จริง ๆ ควรมีร่องรอยใน UI
เช่น tolerance ควรเห็นเป็น warning ตอนกรอกเกิน)

**Exception path:** ถามตัวเอง "ผู้ใช้เดินเข้าเส้นนี้จากตรงไหน" — ถ้าคำตอบคือ
"ต้องพิมพ์ URL เอง" หรือ "ไม่มีทางเข้า" = ✗ แม้หน้าปลายทางจะมีอยู่

**Scope guard / ของเกิน:** ไล่เมนู + routes ทั้งหมดเทียบ node summary —
อะไรที่อยู่นอก brief → จดเป็นรายการแยก อย่าเหมารวมใน gap

## รอบ 2 — หา evidence ใน FRD + TC

**FRD:** เปิดตามโครง Pack จริงของทีม (05_RULES / 03_LOGIC / API / 06_TESTS —
ชื่อไฟล์ยึดตาม pack ที่ได้รับ ไม่ยึดตามความจำ) — rule ต้อง "เนื้อหาตรง" ไม่ใช่แค่มีคำ
เช่น GR-GRN-02 บอก block เกิน tolerance แต่ FRD เขียนว่า warn เฉย ๆ = ✗ (เจือจาง)
พร้อมชี้ข้อความสองฝั่งให้เห็น

**TC (testcases-*.md):** map ราย rule/path → TC id — เกณฑ์:
- block rule ≥ 1 เคสที่ verify พฤติกรรมตาม rule ตรง ๆ (ไม่ใช่ผ่านทางอ้อม)
- exception path ≥ 1 เคสที่เดินเส้นนั้นจริงตั้งแต่ทางเข้า
- นับเฉพาะเคสที่ expected result ตัดสินได้ — เคส "ตรวจสอบว่าทำงานถูกต้อง" ลอย ๆ ไม่นับ

**Lock refs:** rule ที่มี lock_ref → เปิดเทียบว่า FRD ไม่เขียนขัด LOCK-XX
(ขัด = BLOCK ทันที + ชี้สองข้อความ)

## เคสก้ำกึ่ง — ตัดสินแบบนี้

| สถานการณ์ | ทำยังไง |
|---|---|
| HTML มี hook แต่เป็นปุ่ม dead (ไม่มี handler/route) | `△ partial` — มีเจตนาแต่ยังไม่เดินได้ → gap ระดับ WARN |
| Rule ครอบใน FRD แต่คนละถ้อยคำ | อ่านความหมาย — ตรง = ✓ (จด mapping), เจือจาง/แปลง = ✗ |
| Graph กับ NODE_BRIEF ขัดกัน | หยุดถาม user + แนะนำ sync ที่ mapper — ห้ามเลือกเอง |
| ตรวจแล้วเห็นว่า graph เองน่าจะขาด (เช่น standard มี flow ที่ graph ไม่มี) | ห้ามเพิ่มเกณฑ์เอง — เขียนแยกหมวด "เสนอเข้า graph" ท้าย report |
| ไฟล์ artifact บางตัวไม่ได้แนบ | item ที่พึ่งไฟล์นั้น = NOT-CHECKED ระบุไฟล์ที่ต้องการ |
