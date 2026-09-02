# _UX_CHECK_REPORT.md — Format

```markdown
# UX Check Report — [feature/ไฟล์]
- วันที่: YYYY-MM-DD · Iteration: N
- Generator spec: html-generator-v9 (iron-rules #1–#49, #94–#103 · Pattern Q/B2 v2/P)  ← จดจากไฟล์ที่ Sync Read จริง
- Passes run: audit.sh · static_scan · G · D (ถ้าเอกสาร) · R (shots ใน _shots/) · golden compare
- ไฟล์ที่ตรวจ: xxx.html (NNN บรรทัด)

## Verdict: 🔴 BLOCK | 🟡 WARN | 🟢 PASS (with N warnings)
| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 3 | 5 | 2 | 2 |
ประเมินเวลาแก้: ~XX นาที

## 🔴 BLOCK — ต้องแก้ก่อนผ่าน gate
### UX-01 · Rule #1 CI Tokens · route #/grn/list · line 214
- **พบ:** hex `#0B5CFF` ใช้ 12 ครั้ง (สี Navy เก่า) ที่ `.btn-primary`, `.link`
- **แก้:** แทนด้วย `var(--c-primary)` (#FF3B30) — ห้าม hardcode
  `.btn-primary { background: var(--c-primary); }`

## 🟡 WARN
### UX-04 · H-Consistency · ทั้งไฟล์
- **พบ:** badge สถานะ "รออนุมัติ" มี 2 แบบ (line 340 pill เหลือง / line 512 outline)
- **แก้:** ยึดแบบ pill ตาม component-catalog → แก้ line 512 ใช้ class เดียวกัน

## ℹ️ INFO
(ข้อเสนอปรับที่ไม่บังคับ)

## ⬜ NOT-CHECKED
- Contrast บนจอจริง — เปิดไฟล์แล้วกวาดตาโซน stats (เหตุผล: ต้องเห็น rendering)

## Loop Diff (iteration ≥ 2 เท่านั้น)
| สถานะ | รายการ |
|---|---|
| ✓ แก้แล้ว | UX-02, UX-03 |
| ⏳ ค้าง (รอบที่ 2) | UX-01 ← เกิน 2 รอบเมื่อไหร่จะเสนอแก้ให้เลย |
| 🆕 ใหม่ | UX-07 (เกิดจากการแก้ UX-05) |
```

## Finding ที่ดี vs แย่

✅ ดี: ระบุ rule + route + line + สิ่งที่พบเชิงตัวเลข + โค้ด/ค่าที่ถูกต้อง
❌ แย่: "ปุ่มดูไม่ค่อยเรียบร้อย ควรปรับให้สวยขึ้น" — ไม่มีตำแหน่ง ไม่มีเกณฑ์ ไม่มีวิธีแก้
❌ แย่: report ว่า "ผ่าน Rule #38 Thai rhythm" ทั้งที่ไม่ได้ไล่อ่านข้อความจริง

## ลำดับใน report

BLOCK เรียงตาม: แก้แล้วปลดหลายที่ (token/class กลาง) มาก่อน one-off
— ให้ user แก้จุด leverage สูงสุดก่อน
