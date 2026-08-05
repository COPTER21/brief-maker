# _COVERAGE_REPORT.md — Format

```markdown
# Coverage Report — F-GRN (รอบ 1: HTML | รอบ 2: FRD+TC)
- วันที่ · graph: P2P-RECEIVING v1.2.0 · node: F-GRN (wave 3)
- Artifacts ที่ตรวจ: grn.html (+ FRD_F-GRN_Pack, testcases-grn.md ถ้ารอบ 2)
- Checklist จาก contract: edges in 2 · out 4 · rules block 5 / warn 3 · exception 3

## Verdict: 🔴 BLOCK | 🟡 WARN | 🟢 PASS
สรุป: ครอบ 11/14 · gap block 2 · gap warn 1 · NOT-CHECKED 0

## Coverage Matrix
| Item | ประเภท | HTML | FRD | TC | Evidence / หมายเหตุ |
|---|---|---|---|---|---|
| E-003 GRN→RTV (reversal) | edge out | ✓ | ✓ | ✗ | #/grn/view ปุ่ม "ส่งคืนผู้ขาย" · API §3.2 · ไม่มีเคสเดิน RTV |
| GR-GRN-02 tolerance block | rule (block) | △ | ✗ | ✗ | UI warn แต่ไม่ block · FRD เขียนเป็น warn (เจือจางจาก rule) |
| GR-GRN-07 posting GR/IR | rule (block) | N/A-UI | ✓ | ✓ | backend-only · 03_LOGIC §5 · TC-28 |
(ครบทุก item — ห้ามตัดแถวที่ผ่าน)

## 🔴 Gaps (เรียงตามความเสี่ยง)
### GAP-01 · GR-GRN-02 ถูกเจือจาง (block → warn)
- หาย: การ block เมื่อรับเกิน tolerance
- แก้ที่: HTML #/grn/create เพิ่ม validate block + microcopy · FRD 05_RULES แก้ข้อความให้ตรง rule
- อ้าง: rule จาก graph v1.2.0 (source: erp-standard, SAP OMC0 pattern)

## 🟡 Warnings / Scope Creep
- พบ route #/grn/print-labels ที่ไม่อยู่ใน contract → ยืนยันว่าตั้งใจเพิ่ม (แล้วไป update graph)
  หรือถอด

## ⬜ NOT-CHECKED
(item + ไฟล์ที่ต้องการเพิ่ม)

## 💡 เสนอเข้า graph (ไม่ใช่ gap — ไม่กระทบ verdict)
- ระหว่างตรวจพบว่า standard มี flow X ที่ graph ยังไม่มี → เสนอรัน mapper update mode

## Diff จากรอบก่อน (ถ้ามี)
ปิดแล้ว: GAP-.. · ค้าง: GAP-.. · ใหม่: GAP-..
```

## กติกาสำคัญ

- Matrix ต้องโชว์**ทุก item** รวมที่ผ่าน — ความมั่นใจว่า "ครบ" มาจากเห็นทั้งตาราง
  ไม่ใช่เห็นแค่รายการที่พัง
- สัญลักษณ์: ✓ ครอบ (มี evidence) · △ partial · ✗ ไม่ครอบ · N/A-UI (rule backend-only
  ในรอบ 1) · NOT-CHECKED
- ทุก gap ต้องมี "แก้ที่:" ระบุ artifact + ตำแหน่ง — report ที่บอกแค่ว่าขาดอะไร
  แต่ไม่บอกว่าไปเติมตรงไหน = ยังไม่เสร็จ
- Verdict: BLOCK ถ้ามี block rule/edge ที่ ✗ หรือ △ ในคอลัมน์ที่รอบนั้นรับผิดชอบ
  (รอบ 1 = HTML, รอบ 2 = FRD+TC) · WARN = warn rule ขาด หรือ scope creep · นอกนั้น PASS
