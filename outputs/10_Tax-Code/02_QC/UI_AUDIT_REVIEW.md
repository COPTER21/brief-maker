# Human-reviewed UI Audit — Tax Code

วันที่ตรวจ: 5 สิงหาคม 2026  
ต้นฉบับผลอัตโนมัติ: `UI_AUDIT_RESULT.json`  
ขอบเขต: Chromium · 1280 / 1440 / 1920 / 2560 · 7 ฉากต่อ viewport · ภาพ 2 pass

## บทสรุป

- เปิดดูภาพครบ 56/56 ภาพแล้ว
- ไม่พบ clipping, horizontal scroll, ตารางล้นคอลัมน์, input เหลื่อมแนว หรือ dropdown หลุดออกจาก drawer ด้วยตา
- Behavior checks ผ่าน 13/14; จุดที่ตกเป็น defect จริงของ Esc chain
- Runtime ภายใน 0 รายการ
- External CDN failures 66 events ทำให้ Lucide icons ไม่แสดงใน sandbox แต่ไม่เกิด JavaScript page error
- ภาพเหมือนกันทุกไบต์ 27/28 คู่; คู่ที่ต่างมีเพียง 7 พิกเซลจาก 1,152,000 พิกเซล (0.000608%) และแต่ละช่องสีต่างสูงสุด 1 ระดับ

ผลอัตโนมัติ `33 errors + 1 warning` ต้องอ่านร่วมกับการจำแนกด้านล่าง เพราะประกอบด้วย contrast selector 22 ตำแหน่งและ false positive ของตัวตรวจ

## Defect จริงใน TaxCode.html

### UI-01 — กด Esc ติดกันสองครั้งแล้ว drawer ไม่ปิด

- วิธีทำซ้ำ: เปิด view drawer → เปิด confirmation modal → กด Esc สองครั้งติดกัน
- วัดได้หลัง 350ms: `modal=false`, `modalClass=false`, `drawer=true`, `drawerClass=true`
- สาเหตุเชิงพฤติกรรม: modal class ถูกถอดทันที แต่ `state.modal.open` ค้างต่อ 200ms ทำให้ Esc ครั้งที่สองยังถูกส่งไปปิด modal ซ้ำแทน drawer
- ผลกระทบ: ขัดกับ overlay Esc chain; ผู้ใช้ต้องรอหรือกด Esc ครั้งที่สาม

### UI-02 — Clickable cards และ user menu ใช้คีย์บอร์ดไม่ได้

- `.user-chip`: `tabIndex=-1`, handler `toggleUserMenu`
- KPI `.stat.is-clickable` 3 ใบ: `tabIndex=-1`, handler `setStatusFilter`
- ไม่มี focusable child ที่เรียก handler เดียวกัน
- ผลกระทบ: ผู้ใช้ keyboard-only เข้าเมนูผู้ใช้และใช้ KPI filter ไม่ได้

### UI-03 — ปุ่มแจ้งเตือนไม่มี accessible name

- Selector: `#notifBtn`
- ไม่มี `aria-label`, `title` หรือข้อความที่ screen reader อ่านเป็นชื่อปุ่ม
- เมื่อ CDN ถูกบล็อก ปุ่มยังกลายเป็นพื้นที่ว่างที่ไม่มี icon ให้ผู้ใช้เห็นด้วย

### UI-04 — ไม่มี focus-visible treatment กลาง

- สแกน CSS แล้วไม่พบ `:focus-visible`
- control บางชนิดมี `:focus` เฉพาะตัว แต่ไม่มีหลักประกันว่าทุก interactive element จะแสดงกรอบโฟกัสจาก keyboard

## Design-system / accessibility findings

### UI-05 — Contrast ต่ำกว่า WCAG AA

พบ 22 selectors แต่ยุบเป็น 5 คู่สี:

| Foreground / Background | Ratio | เกณฑ์ | ตัวอย่าง |
|---|---:|---:|---|
| `#FFFFFF` / `#FF3B30` | 3.55 | 4.5 | primary button, active sidebar |
| `#73757B` / `#F1EEEA` | 3.98 | 4.5 | muted pills/counts |
| `#73757B` / `#FAF8F5` | 4.34 | 4.5 | drawer footer metadata |
| `#9A9CA2` / `#FFFFFF` | 2.74 | 4.5 | unused/secondary text |
| `#E62E24` / `#FFFFFF` | 4.39 | 4.5 | required marks and danger text |

สีเหล่านี้มาจาก base-kit/shared tokens จึงไม่ควรแก้เฉพาะ Tax Code ต้องให้เจ้าของ design system เลือก token ใหม่หรือปรับขนาด/น้ำหนักข้อความแล้ว sync กลับทุก feature

### UI-06 — Modal ไม่มีปุ่มปิดใน header

- Modal มีปุ่ม “ปิด/ยกเลิก” ที่ footer และปิดด้วย Esc ได้
- แต่ prompt กำหนดให้ปุ่มปิดอยู่ขวาสุดในแถวหัวข้อ จึงถือว่าไม่ผ่าน contract นี้
- เป็น pattern กลางของ modal ควรตัดสินและแก้ที่ base-kit ไม่ควร patch เฉพาะหน้า

## ตัวตรวจกลางที่แก้แล้ว แต่ยังไม่ได้รันยืนยันรอบที่สาม

แก้ `uikit.py` 2 จุดหลังพิสูจน์ว่าเป็น false positive:

1. Overlay occlusion เคยนับ drawer ว่าถูก modal ทับ ทั้งที่ modal เป็น top layer โดยตั้งใจ — เปลี่ยนให้ยิง 8 จุดเฉพาะ overlay ชั้นบนสุด
2. Close-button detector เคยจับปุ่ม “ปิดใช้งาน” เป็นปุ่มปิดเพราะค้นข้อความที่มีคำว่า “ปิด” — เปลี่ยนให้ใช้ `aria-label/title` ที่เท่ากับ “ปิด/close” เท่านั้น

ไม่รัน Playwright รอบที่สามตามกติกาใน `check_ui_prompt.md`; การแก้ตัวตรวจสองจุดนี้จึงผ่าน syntax checkได้ แต่ยังรอรอบถัดไปเพื่อยืนยันเชิง runtime

## Finding ที่ไม่ใช่ defect ปัจจุบัน

- `.notif-wrap` ไม่มี CSS rule แต่มี `position:relative` แบบ inlineและใช้เป็น JavaScript hook
- `.width-filter` ไม่มี CSS rule แต่ element เดียวกันมี `.filter-status { max-width:200px; }` ทำงานอยู่แล้ว
- ภาพ 1280 VAT list ต่าง 7 พิกเซลบริเวณขอบ/เงาการ์ดที่พิกัด x=1244–1245, y=156–159 โดยต่างสูงสุด 1 ระดับสี มองด้วยตาไม่เห็น แต่ยังคงระบุเป็น visual-stability deviation เพราะข้อกำหนดต้องเหมือนกันทุกไบต์

## การเปลี่ยนแปลงรอบนี้

- แก้ไฟล์ feature (`TaxCode.html`): **0 จุด**
- แก้ตัวตรวจ/feature walker: **5 จุดเชิงสาเหตุ**
  - Playwright argument signature
  - deduplicate finding ข้าม viewport/pass
  - correlate Lucide warning กับ external request URL
  - topmost-overlay occlusion
  - exact close-button identification
- แก้แม่แบบ/shared CSS: **0 จุด**
- รอเจ้าของ design system ตัดสิน: **2 กลุ่ม** — contrast tokens และ modal header close contract

## สิ่งที่ตัวตรวจอัตโนมัติยังยืนยันแทนคนไม่ได้

- ความสวยงามและจังหวะ whitespace โดยรวม
- ลำดับงานและ microcopy เข้าใจง่ายกับผู้ใช้จริงหรือไม่
- ประสบการณ์ screen reader เชิงความหมายแบบ end-to-end
- native browser tooltip

