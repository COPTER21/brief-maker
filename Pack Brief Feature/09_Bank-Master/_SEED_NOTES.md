# _SEED_NOTES · F-BNK Bank Master
> W1-09 · FIN · prior: reg · seed 2026-08-04 · state → done

## ทำอะไรไป
HTML v7 หัวเชื้อ — `BankMaster.html` (141 KB). master 2 ระดับ (ธนาคาร + บัญชีบริษัท) FN ครบ:
- FN-01 เพิ่มบัญชี: ธนาคาร = search combobox (Rule #94, preset ไทย ~22) + validate เลข 10-15 หลัก + ผูก GL จาก CoA (combobox)
- FN-02 สลับบริษัท (2) + default จ่าย/รับ อย่างละ 1 (toggle บังคับ unique) · FN-03 เลขซ้ำในบริษัท = บล็อก
- FN-04 inactive → หายจาก mock picker เอกสารใหม่ ของเดิมโชว์ปกติ · FN-05 masking 4 ตัวท้าย + "ดูเต็ม" ตามสิทธิ์ + log
- FN-06 ใช้แล้วลบไม่ได้ → soft archive + audit · FN-90 audit + validation ครบ
- 2 แท็บ: บัญชีบริษัท + ธนาคาร (preset BOT code/SWIFT + เพิ่มธนาคารต่างประเทศ + SWIFT)
Patterns: A · B (drawer 680) · C (view tabbed) · D (archive/deactivate/picker) · Rule #94 ทั้ง bank + GL.
Mock: 2 บริษัท · 5 บัญชี (KBank กระแส=default จ่าย, SCB ออม=default รับ, BBL, inactive 1, บริษัท2 1). Gate: FAIL=0 (WARN=3 base-kit) · script 5/5 OK · Playwright PASS.

## OQ ค้าง (เจ้าภาพ)
- OQ-1 masking เลขบัญชี + สิทธิ์ดูเต็ม — ทำ reveal-on-permission + audit (Strike/Policy: ยืนยัน tier ใครได้ canRevealFull)
- OQ-2 รองรับสกุลอื่นเมื่อไหร่ — ล็อก THB เฟสนี้ (Strike — โยง multi-currency)

## [AI-DRAFT] ที่หัวหน้าควรดูก่อน
- เลขบัญชี = ตัวเลข 10-15 หลัก (ไม่มีตาราง format ต่อธนาคาร) · SWIFT ต่างประเทศ = 8/11 ตัวอักษร-ตัวเลข
- THB-only บังคับ · ผู้ใช้ mock ได้สิทธิ์ reveal

## คำสั่งเลนถัดไป (ทีมทำต่อ)
1) เปิด BankMaster.html vibe ต่อ /html-generator-v7 · 2) /qc-ux + /qc-coverage
3) /frd-generator-v6 → UI Brief → TC → QA · 4) ติ๊ก checklist DEV/QA · ไม่รองรับ: bank API/statement (S-06), multi-currency
