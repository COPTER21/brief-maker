# UX Check Report — F-WH-PACK Packing

- วันที่: 2026-08-19 · Iteration: 1
- Generator spec ที่ Sync Read: `html-generator-v8` (Iron Rules #1–#97 และเอกสาร CI/Component/Layout ที่เกี่ยวข้อง)
- ไฟล์ที่ตรวจ: `outputs/03_PACK/f-wh-packing.html` (1,190 บรรทัด)
- โหมด: read-only ตามคำสั่ง PM/BA — รายงานนี้ไม่ได้แก้ HTML

## Verdict: 🔴 BLOCK

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 7 | 3 | 2 | 2 |

ไม่ผ่าน UX gate จึงยังไม่อนุญาตให้ใช้ไฟล์นี้เป็นฐานสร้าง BRD/FRD ตาม workflow ที่กำหนด

## 🔴 BLOCK — ต้องแก้ก่อนผ่าน gate

### UX-01 · Rule #60 · PREFLIGHT stamp ไม่ใช่รูปแบบที่ตรวจสอบย้อนกลับได้ · line 105

- พบ: comment ระบุเพียง `PREFLIGHT v8` และคำอธิบายเชิงข้อความ แต่ไม่มีตัวเลขผล Mechanical Sweep และไม่มีหลักฐาน Role Sweep ตาม format บังคับ
- หลักฐานเครื่องมือ: `self_audit.py` ยอมรับว่ามี stamp แต่ผล audit จริงเป็น `FAIL`
- แก้: สร้าง stamp ใหม่หลังแก้ข้อบกพร่องและรัน self-audit จนค่าบังคับเป็นศูนย์ โดยระบุตัวเลขจริงทุกช่อง

### UX-02 · Rules #1, #50, #61 · token/spacing/type scale ไม่ตรงมาตรฐาน

- พบ: spacing นอก scale 28 จุด; font-size นอก scale 9 ค่า (`10`, `10.5`, `11.5`, `15`, `18`, `21` เป็นต้น); ใช้ font-size 13 ขนาด เกินเพดาน 8 ขนาด
- พบ fallback สี UI เก่า `#0B5CFF` ที่ line 20 และ `#0B1D3A` ที่ line 23
- หมายเหตุ: สีภายในพื้นที่จำลองเอกสารพิมพ์ `.pdoc` ไม่ถูกนับเป็นเหตุ BLOCK ข้อนี้ เพราะกฎอนุญาต print/PDF sheet แยกต่างหาก
- แก้: ย้ายค่าหน้าจอทั้งหมดเข้า token v8, ใช้ spacing/type scale กลาง และตัด fallback สี legacy ใน UI chrome

### UX-03 · Rules #55–#56 · layout ไม่ผ่าน mechanical contract

- พบ: flex ที่ไม่มี `align-items` 9 selector, grid ที่ไม่มี `gap` 2 selector
- พบ inline layout 129 จุดจาก self-audit (static scan พบ `style` attribute ทั้งหมด 258 จุด) ซึ่งหลายจุดกำหนด position/width/height/padding/margin โดยตรง ไม่ใช่เฉพาะค่าคำนวณแบบ dynamic
- ตัวอย่าง: `#toast-root` line 798 กำหนด position, spacing และ z-index แบบ inline
- แก้: ย้าย layout คงที่เข้า class; inline อนุญาตเฉพาะค่าที่เกิดจาก runtime เช่น progress width

### UX-04 · Rules #49, #62 · scrollbar และ z-index ไม่ผ่าน registry

- พบ: scrollbar หลักกว้าง 8px ที่ lines 159–162 แทนมาตรฐาน 5px
- พบ z-index แบบเลขลอย เช่น `60` ที่ lines 23, 448, 571 และ `90` ที่ line 705 แทน `var(--z-*)`
- แก้: ใช้ scrollbar block มาตรฐาน และ map overlay/dropdown/tooltip ทุกตัวเข้ากับ z-index registry

### UX-05 · Rule #82 · static interaction integrity ไม่ผ่าน

- พบจาก self-audit: `undefined_handlers = ['if']` และ `missing_ids = ['bcb-', 'bcb-act', 'bcb-new', 'combo-pop']`
- ถึงแม้บางรายการอาจเป็น false positive จาก template string แต่ gate กำหนดให้ต้องพิสูจน์ทีละจุดก่อนผ่าน ไม่สามารถถือว่าผ่านจากความจำได้
- แก้: ตรวจ handler/ID ที่ runtime สร้างขึ้นและปรับ markup/สคริปต์หรือ whitelist ที่ authoritative checker รองรับ พร้อมหลักฐาน render

### UX-06 · Rules #68, #74 · overlay/tab contract ไม่เป็นรูปแบบ kit

- พบ `stopPropagation()` เกิน allowance ของ checker 1 จุด
- พบ custom tab classes 4 รูปแบบ (`tabs`, template class `tab ...`) แทน `.drawer-tabs > .drawer-tab`
- แก้: ใช้ overlay discipline และ drawer tab component จาก BASE-KIT เท่านั้น

### UX-07 · Rules #67, #69 · late-layout/long banner ไม่ผ่าน

- พบ long banner 2 จุดจาก self-audit และไม่พบหลักฐาน trace ว่าเป็นข้อความที่ PREBRIEF กำหนดให้แสดงตรง ๆ
- พบ BASE-KIT/late-style compliance ไม่สามารถยืนยันได้จาก stamp ปัจจุบัน ขณะที่ mechanical audit มีข้อผิดพลาดหลายหมวด
- แก้: ตรวจข้อความกับ requirement; ข้อความช่วยที่ไม่ได้ระบุ explicit ต้องตัดออกหรือใช้ pattern ที่กฎอนุญาต และพิสูจน์ kit integrity ใหม่

## 🟡 WARN

### UX-08 · Empty state coverage

- static scan พบ table 8 จุด แต่ไม่พบ marker empty-state
- ต้อง render ทุก list/filter state เพื่อพิสูจน์ว่ามี empty/no-result state ที่ผู้ใช้เห็นได้จริง

### UX-09 · Accessibility anchors

- static scan ไม่พบ `aria-*` attribute แม้มี interaction จำนวนมาก
- ควรตรวจชื่อ accessible ของปุ่ม icon-only, dialog/drawer และ combobox หลังแก้ mechanical BLOCK

### UX-10 · Font stack order

- stack ปัจจุบันเริ่มด้วย `Noto Sans Thai` ก่อน `Satoshi` และบางจุดไม่มี `system-ui` ไม่ตรง stack กลางแบบ verbatim
- ให้ใช้ `'Satoshi', 'Noto Sans Thai', system-ui, -apple-system, sans-serif` สำหรับ UI

## ℹ️ INFO

- ผ่านเบื้องต้น: ไม่ใช้ `localStorage`/`sessionStorage`, มี hash route และ `hashchange`, มี Escape handler, มี Lucide icon และไม่พบ Font Awesome
- ฟังก์ชัน `scanKey` ปิดครบที่ line 1184; ไม่พบหลักฐาน syntax error จาก brace ที่สงสัยด้วยการอ่านตำแหน่งนี้

## ⬜ NOT-CHECKED

- Render/visual sweep ทุก route, drawer, modal, tab และ responsive viewport — ยุติทันทีเมื่อ mechanical gate ให้ผล BLOCK
- Business coverage round 1 — ไม่รันต่อ เพราะลำดับ workflow กำหนดให้ UX gate ผ่านก่อน

## หลักฐานคำสั่งตรวจ

- `qc-ux-html-checker/scripts/static_scan.py`: พบ 1,190 lines, scrollbar 8px, inline style 258, empty marker 0, aria marker 0
- `html-generator-v8/scripts/self_audit.py`: `RESULT: FAIL` พร้อม violation ตามรายการด้านบน

## Gate decision

`WAIVED-BLOCK` — ผู้ใช้ยืนยันเมื่อ 2026-08-19 ว่า “waive UX gate และใช้ HTML ตามสภาพ” จึงอนุญาตให้เดิน pipeline ต่อโดย:

1. ไม่แก้ `f-wh-packing.html`
2. คง finding ทั้งหมดไว้เป็น technical debt
3. ไม่ตีความ waiver ว่า finding ผ่านหรือหายไป
4. ให้ BRD/FRD อ้างพฤติกรรมธุรกิจจาก HTML แต่ไม่สืบทอดรายละเอียด UI ที่ขัดกับมาตรฐานกลางเป็นข้อกำหนดใหม่
