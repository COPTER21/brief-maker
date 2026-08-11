# E2E TEST REPORT · Payment Term (F-PAY)

> Playwright interaction harness (คลิกจริงทุก flow + ดัก JS console/page error) · 2026-08-10
> harness: `scratchpad/e2e_payterm.py` · shots: `02_QC/_e2e_shots/`

## ผลสุดท้าย: 🟢 **PASS — 23/23 checks · 0 JS errors** (ยืนยัน 2 passes ติดกัน stable)

## 🐞 Bug ที่เจอ + แก้ (จับได้เฉพาะ E2E — audit/qc-ux มองไม่เห็น)
**BUG-E2E-01 · Drawer scroll jump-to-top** (Iron Rule #29 latent, class เดียวกับ base-kit bug เดิม)
- **อาการ:** เปิด create drawer → เลือกประเภทจาก dropdown (เช่น installment) → scroll ลง → toggle checkbox use_in → **drawer เด้งกลับขึ้นบนสุด** (300→0)
- **Root cause:** `toggleSdd` set `state._formScroll` ทุกครั้งที่เปิด dropdown · แต่ `onTypeChange` ใช้ `render()` ตรง ๆ ไม่ได้ consume/clear `_formScroll` → การ interact ครั้งถัดไป (`renderFormKeepScroll`) หยิบค่า scroll เก่า (0 = ตอนเปิด dropdown บนสุด) มา restore → เด้ง
- **Fix (surgical):** clear `state._formScroll=null` ในทุก path ที่ปิด dropdown โดยไม่ผ่าน renderFormKeepScroll — `onTypeChange`, `closeDrawer`, Esc handler (sdd branch), outside-click handler
- **หลัง fix:** 300→308 (preserved, ไม่เด้ง) · ยืนยัน 2 passes

## Coverage ที่เทสต์ (23 checks)
list render · stat filter + toggle · search · create drawer open · **use_in = 7 (ไม่มี PR)** · **type dropdown 2-line desc (G2)** · type switch (installment) · installment live % total + add row · validation block + toast · drawer stays open on invalid · Esc chain · **scroll preservation (Rule #29) + no jump-to-top** · row→view drawer · status menu · bulk select + bulk bar · bulk delete confirm · edit prefill · **hamburger @1024 + toggle sidebar (G3)**

## หมายเหตุ (พฤติกรรม by-design ไม่ใช่ bug)
- validation error highlights หายเมื่อ interact ฟอร์มต่อ (re-render จาก state) — error กลับมาเมื่อกด submit อีกครั้ง · ปกติของ re-render SPA

**พร้อมให้ user ทดสอบมือจริง** — ไม่พบ JS error / broken flow / z-index จม / scroll เด้ง เหลืออยู่

## 🐞 BUG-E2E-02 · Toast แทบมองไม่เห็น + ทับปุ่มบันทึก (พบตอน user manual test)
- **อาการ:** toast โผล่ ~200ms แล้ว**จางหายเอง** (อ่านไม่ทัน) + อยู่มุมขวาล่างทับปุ่ม "บันทึก" ใน drawer
- **Root cause:** บล็อก `.toast` เก่า (legacy) ตั้ง base `opacity:0` + `position:fixed;bottom;right` · ตัว toast จริงใช้ `animation:toastIn` (ไม่มี fill-mode) → หลัง animation จบ revert กลับ `opacity:0` = หาย · และ position:fixed มุมขวาล่างทับ footer
- **Fix:** ลบ base `opacity:0`/`position:fixed`/`transform` ออกจาก legacy block · ย้าย `.toast-host` เป็น **top-center** · error/warning อยู่ **5s** (success 2.8s) · animation slide จากบน
- **หลัง fix (verified):** opacity=1 · y=16 (top-center) · ไม่ทับปุ่ม · E2E 23/23 · audit FAIL=0

## 🔧 MANUAL-TEST FIX ROUND (user ทดสอบมือ — 7 จุด, 2026-08-10)
| # | จุดที่ user เจอ | แก้ | verify |
|---|---|---|---|
| 1 | เมนูซ้าย (ผังบัญชี/GL Posting Group) ลิงก์ไปไฟล์ที่ยังไม่มี | `is-disabled` + ตัด href | coa disabled=True, href=None |
| 2 | ช่องค้นหา พิมพ์ได้ทีละตัว focus หลุด (re-render ทำ input หาย) | onSearch refocus + คืน caret ท้าย | พิมพ์ "NET6" ได้ครบ + ยัง focus |
| 3 | filter dropdown ยังบรรทัดเดียว (sub เพิ่มแค่ฟอร์ม) | เพิ่ม `sub:v.hint` ให้ filter typeOpts | 7 sub-lines (ภาพยืนยัน 2 บรรทัด) |
| 4 | bulk bar ดำ | ขาว + charcoal text + line border + danger แดง (contrast) | bg=rgb(255,255,255) |
| 5 | grn-trigger note ชิด input ล่างเกิน | +`margin-bottom:16px` | — |
| 6 | ปุ่มเพิ่มงวด + badge % ไม่ align | wrap `.inst-actions` flex space-between + align-center | inst-actions=1 |
| 7 | รหัสซ้ำ (NET30) inline message ไม่สื่อ | set field-error = "รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น" | — |
| 8 | use_in toast เร็ว+ทับปุ่ม | (แก้แล้ว BUG-E2E-02: top-center + 5s) | opacity=1, y=16 |

**หลังแก้:** audit.sh FAIL=0 · E2E 23/23 · 0 JS error · visual verified
