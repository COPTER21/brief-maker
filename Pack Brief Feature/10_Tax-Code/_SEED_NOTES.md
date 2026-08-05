# _SEED_NOTES · F-TAX Tax Code
> W1-10 · ACC · prior: reg · seed 2026-08-04 · state → done

## ทำอะไรไป
HTML v7 หัวเชื้อ — `TaxCode.html` (131 KB). 2 ตระกูล VAT + WHT (แท็บ) FN ครบ:
- FN-01 preset ไทย 7 code พร้อม GL ตั้งแต่ mock แรก: VAT7(ขาย/ซื้อ), VAT0(ส่งออก), VAT-EX(ยกเว้น), WHT1%(ขนส่ง), WHT2%(โฆษณา), WHT3%(บริการ), WHT5%(เช่า)
- FN-02 เพิ่ม code + GL บังคับก่อน active (BR-04, GL combobox Rule #94) · FN-03 อัตราของ code ที่ใช้แล้ว = read-only + flow "สร้างตัวแทน + วันมีผล"
- FN-04 WHT บังคับประเภทเงินได้ (ภงด.3/53) · FN-05 inactive/หมดผล → หายจาก picker ใหม่ ของเดิมปกติ
- FN-06 ใช้แล้วลบไม่ได้ + badge "ใช้แล้ว N เอกสาร" · FN-90 audit + soft archive
Patterns: A (แท็บ VAT/WHT) · B (drawer 680) · D ×4 · Rule #94 GL + income-type combobox.
Mock: 7 preset + inactive 1 + demo delete-block. Gate: FAIL=0 (WARN=3 base-kit) · script 0 err · Playwright 0 err.

## OQ ค้าง (เจ้าภาพ)
- OQ-1 default code ต่อเอกสาร (SO default VAT7?) เก็บที่ config module ไหน — นอก feature นี้ (Strike)
- OQ-2 WHT ฝั่งถูกหัก (ลูกค้าหักเรา) เฟสนี้ไหม — ยังไม่ทำ (Strike)

## [AI-DRAFT] ที่หัวหน้าควรดูก่อน
- โมเดล VAT ผ่าน vatKind (standard 7% / zero 0% / exempt) เพื่อครอบ 7%/0%/ยกเว้น
- VAT "both" โชว์ GL 2 ช่อง (ภาษีขาย + ภาษีซื้อ) · VAT-EX ให้ memo GL แทนช่องว่างเพื่อ BR-04 uniform
- list ≤ 8 คอลัมน์ (ย้าย GL ไป view drawer) · ไม่รองรับ: ภาษีต่างประเทศ (S-06), ฝั่งถูกหัก

## คำสั่งเลนถัดไป (ทีมทำต่อ)
1) เปิด TaxCode.html vibe ต่อ /html-generator-v7 · 2) /qc-ux + /qc-coverage
3) /frd-generator-v6 → UI Brief → TC → QA · 4) ติ๊ก checklist DEV/QA
