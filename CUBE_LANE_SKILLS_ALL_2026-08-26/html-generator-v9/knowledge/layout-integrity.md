# Layout Integrity Rules (#50–#60) — v6.2

> หมวดกฎใหม่ (2026-07-26) เกิดจาก defect จริงของเลน F-PRODUCT: HTML ผ่าน gate ทุกข้อแต่ "เบี้ยว"
> เพราะกฎ 49 ข้อเดิมคุมสี/พฤติกรรม/คำ — **ไม่มีข้อไหนคุมเรขาคณิต** หมวดนี้ปิดช่องนั้น
> ทุกข้อออกแบบให้ **ตรวจได้เชิงกล** (grep/นับ) — คู่กับ Geometry Check ใน qc-ux-html-checker

---

## Rule #50 — Spacing Scale เดียวทั้งไฟล์ (แกนของหมวดนี้)
ระยะทุกชนิด (padding / margin / gap) ใช้ค่าจาก scale เท่านั้น:
```
4 · 6 · 8 · 10 · 12 · 16 · 18 · 20 · 24 · 32 · 40 (px)
```
- ❌ ห้ามค่านอก scale (13px, 15px, 22px, 27px…) — ที่มาหลักของ "ช่องไฟไม่สม่ำเสมอ"
- ค่าเดียวที่ยกเว้น: 1–3px สำหรับ border/offset เชิง optical (เช่น `margin-bottom:-1px` ของ tab)
- แนะนำประกาศ `--sp-1..--sp-8` ใน `:root` แล้วอ้าง var — แต่ค่าดิบใน scale ก็ผ่าน

## Rule #51 — Form Grid มาตรฐาน
ฟอร์มทุกฟอร์มวางบน grid ประกาศชัด — ห้ามไล่ margin ทีละ field:
- 2 คอลัมน์: `display:grid; grid-template-columns:repeat(2,1fr); gap:16px 20px`
- field เต็มแถว (หมายเหตุ/ที่อยู่/upload): `grid-column:1/-1` — ห้ามปล่อยลอยครึ่งแถวโดยไม่ตั้งใจ
- label อยู่บน field เสมอ (แนวตั้ง) ระยะ label→input = 6px ทุกจุด
- ห้ามผสม grid กับ float/inline-block ในฟอร์มเดียว

## Rule #52 — Row Consistency (ปุ่ม/ควบคุมร่วมแถว)
ทุก element ที่อยู่แถว action เดียวกัน:
- สูงเท่ากันหมด — ปุ่ม/input/select ใช้ height เดียว (มาตรฐาน 36px, ปุ่มเล็กในตาราง 30px)
- container ต้องเป็น flex + `align-items:center` + `gap` จาก scale — ห้ามดัน align ด้วย margin-top รายตัว
- ปุ่มชุดเดียวกัน (เช่น footer drawer) ใช้ class ระบบเดียวกัน — ห้ามตัวหนึ่ง `.btn` อีกตัวเขียน style สด

## Rule #53 — Table Alignment
- คอลัมน์ตัวเลข/จำนวนเงิน: `text-align:right` + `font-variant-numeric:tabular-nums`
- ข้อความ: ชิดซ้าย · สถานะ/pill: กึ่งกลาง หรือซ้ายทั้งคอลัมน์ — เลือกแล้วคงที่ทั้งตาราง
- th กับ td คอลัมน์เดียวกัน align ตรงกันเสมอ
- คอลัมน์ action ท้ายตาราง: ความกว้างคงที่ + ชิดขวา

## Rule #54 — Container Padding ค่าเดียวต่อชนิด
ประกาศครั้งเดียวใช้ทั้งไฟล์: `.card` = 20px · `.drawer-body` = 24px · `.modal-body` = 24px ·
section ใน page = 18px จากกัน — ห้ามไฟล์เดียวมี card 3 padding

## Rule #55 — Flex/Grid ต้องประกาศ align ครบ
- ทุก `display:flex` ที่มีลูก >1 ต้องมี `align-items` ระบุชัด (ห้ามพึ่ง default stretch โดยไม่ตั้งใจ)
- ทุก `display:grid` ต้องมี `gap` — ห้ามเว้นระยะด้วย margin ของลูกแทน gap

## Rule #56 — ห้าม inline layout style
`style="margin:… / padding:… / width:…"` ใน markup = FAIL — layout อยู่ใน class เท่านั้น
(inline อนุญาตเฉพาะค่า dynamic จาก JS เช่น progress width)

## Rule #57 — Overflow Discipline
- ลูก flex ที่มีข้อความยาว: `min-width:0` + ellipsis — กันกล่องพี่น้องโดนดันเบี้ยว
- เซลล์ตารางข้อความยาว: `.cell-truncate` — ห้ามปล่อยดันความกว้างตาราง
- container แนวนอนทุกตัวตอบคำถาม "ถ้าเนื้อหายาวสุดจะเกิดอะไร" ได้ (truncate/scroll/wrap — เลือกชัด)

## Rule #58 — Vertical Rhythm
ระยะแนวตั้งระหว่าง section ระดับเดียวกัน = ค่าเดียวตลอดหน้า (18 หรือ 24px — เลือกแล้วคงที่)
หัว section → เนื้อ = 12px ทุกจุด · ห้ามหน้าเดียวมีจังหวะ 14/18/22/26 ปน

## Rule #59 — Wizard/Stepper Geometry
- step indicator: ทุก step กว้างเท่ากัน (`flex:1`) เส้นเชื่อมอยู่กึ่งกลางแนวตั้งของ dot เป๊ะ
- เนื้อหาทุก step อยู่ใน container กว้างเดียวกัน — เปลี่ยน step แล้วขอบซ้ายขวาห้ามขยับ
- footer ปุ่ม (กลับ | ถัดไป) ตำแหน่งตายตัวทุก step

## Rule #61 — Type Scale (จาก audit จริง: ไฟล์เดียวมี 14 ขนาด)
font-size ใช้ได้เฉพาะ scale นี้:
```
11 · 12 · 12.5 · 13 (base) · 14 · 16 · 20 · 26 (px)
```
- 12.5 = ค่าเดียวที่มีเศษ อนุญาตเฉพาะ table density — ประกาศเป็น `--fs-table` ใน `:root` แล้วอ้าง var
- ❌ ห้ามขั้นเศษอื่น (9.5 / 10.5 / 11.5 / 15.5) — ต้นตอ "ลำดับสายตาไม่นิ่ง"
- caption/uppercase label เล็กสุด = 11px — ห้ามต่ำกว่า (อ่านไม่ออกบนจอจริง)
- บทบาทมาตรฐาน: 26 page-title · 20 section-title · 16 drawer/modal-title · 14 emphasis ·
  13 body · 12.5 table · 12 secondary · 11 caption/label

## Rule #62 — Z-Index Registry (จาก audit จริง: 11 ค่า ad-hoc)
ประกาศชั้นใน `:root` แล้วอ้าง var เท่านั้น — ห้ามเลขลอย:
```css
--z-content: 1;      /* in-flow decoration 1-9 */
--z-sticky: 10;      /* sticky header/column */
--z-dropdown: 30;    /* select list, user menu, tooltip */
--z-backdrop: 50;    /* ฉากหลัง overlay ทุกชนิด */
--z-drawer: 51;
--z-modal: 60;       /* modal อยู่เหนือ drawer เสมอ (confirm จาก drawer) */
--z-toast: 80;       /* บนสุดตลอด */
```
- element ใหม่ต้องเลือกจาก registry — อยากได้ชั้นใหม่ = แก้ registry ก่อน (ที่เดียว)
- ❌ `z-index: 999` / เลขสุ่ม = FAIL ทันที
**62.1 Overlay Layering (บังคับ — จาก defect F-UOM: thead ทะลุ drawer):**
- overlay ทุกตัว (backdrop/drawer/modal/toast/เมนู) **ต้องประกาศ** `z-index: var(--z-…)` ของชั้นตัวเอง
  — overlay ไร้ z-index = FAIL (sticky ชนะแล้วทะลุ)
- drawer/modal/backdrop ต้องเป็น**ลูกตรงของ `<body>`** (markup อยู่ท้ายไฟล์ก่อน script)
  — ห้ามฝังใน content container (ติด stacking context เดียวกับตาราง)
- `position:sticky` ใช้ได้เฉพาะ `--z-sticky`/`--z-shell` — ห้าม ancestor ของตารางมี transform/filter
  ที่สร้าง context ใหม่คร่อม overlay
- mirror จาก reference: **class ระบบ overlay ต้อง map กลับเป็นของ kit เสมอ** (.drawer/.modal/.backdrop)
- **62.2 เมนูลอยทุกตัว** (dropdown/autocomplete/menu): พื้นทึบ + border + shadow + `var(--z-dropdown)`
  — เมนูโปร่งให้เห็น thead ทะลุ = FAIL (defect F-UOM รอบ 2)

## Rule #60 — Pre-flight Self-Check (บังคับก่อนส่งไฟล์)
ก่อนถือว่า gen เสร็จ ต้องไล่ตรวจไฟล์ตัวเองแล้วแก้ให้จบ:
1. grep hex ทั้งหมด → ทุกตัวอยู่ใน ci-tokens whitelist (Rule #1)
2. grep px ของ padding/margin/gap → ทุกค่าอยู่ใน scale #50
3. grep `style="` → ไม่มี inline layout (#56)
4. grep `display:flex` → มี align-items (#55) · `display:grid` → มี gap
5. ไล่ปุ่มร่วมแถว → class ระบบเดียว สูงเท่ากัน (#52)
6. grep `font-size` ทั้งหมด → ทุกค่าอยู่ใน type scale #61 (นับจำนวนขนาด — เกิน 8 = สอบตก)
7. grep `z-index` ทั้งหมด → ทุกค่าอ้าง `var(--z-*)` จาก registry #62
8. ไล่ microcopy ปุ่มหลัก เทียบ `knowledge/microcopy.md` (กลับ/ถัดไป/ยืนยัน…)
9. toast/submitting/disabled ตาม #44/#45/#46.5

**ผลการตรวจต้องรายงานเป็นตัวเลข ไม่ใช่คำว่า "ผ่าน"** — ดู Self-Review Protocol ด้านล่าง

---

## ⭐ Self-Review Protocol (v6.2 — บังคับ 2 รอบก่อนส่งทุกไฟล์)

> หลักคิด: การ "gen แล้วเช็คไปด้วย" เชื่อไม่ได้ — ตอน gen โมเดลโฟกัสที่เนื้อหา ไม่ใช่กติกา
> ต้องแยกเป็น **รอบเขียน → รอบตรวจแบบเปลี่ยนหมวก** โดยรอบตรวจห้ามแก้เนื้อหา แก้ได้เฉพาะ compliance

### รอบที่ 1 — Mechanical Sweep (ตรวจเชิงตัวเลข)
รัน `scripts/self_audit.py <file.html>` (หรือไล่มือตาม logic เดียวกันถ้า env ไม่มี python):
สคริปต์คืนตัวเลขจริง — off-scale spacing / จำนวน font sizes / flex ไม่มี align /
inline layout / z-index นอก registry / hex นอก whitelist / ปุ่มร่วมแถวต่าง height
**เกณฑ์ผ่าน: ทุกตัวนับ = 0** (ยกเว้น whitelist ที่กฎอนุญาต) — ไม่เป็นศูนย์ → แก้ → รันซ้ำ จนศูนย์

### รอบที่ 2 — Role Sweep (ตรวจเชิงบทบาท — สิ่งที่ script นับไม่ได้)
เปลี่ยนหมวกเป็น reviewer ไล่ checklist โดย **อ้างหลักฐานทุกข้อ (บรรทัด/selector) ห้ามติ๊กจากความจำ:**
- [ ] ทุกหน้าตอบได้ว่าใช้ Pattern ไหน (A-N) และ element ครบตาม pattern นั้น
- [ ] ปุ่มทุกปุ่มสีตรงบทบาท (#31.1/#46.4): primary=ไปหน้า · danger=ทำลาย · ghost=รอง
- [ ] state ครบทุก view: empty / loading / error / disabled (#44/#45)
- [ ] ทุก flow เดินจบ: สร้าง→toast→กลับ list · ลบ→confirm→หาย · Esc chain ปิดถูกลำดับ
- [ ] microcopy ตรงไฟล์กลาง (สุ่ม 10 ปุ่ม/toast เทียบ verbatim)
- [ ] ทุก edge-out hook จาก brief มีที่ยืนบนจอ (ปุ่ม/สถานะ/ช่องอ้างอิง)
- [ ] wizard: ขอบ container นิ่งทุก step · footer ตำแหน่งเดิม

### ตราประทับ (แทน comment เดิม — ต้องมีตัวเลข)
```html
<!-- PREFLIGHT v6.2
  round1: spacing-off=0 · font-sizes=7 · flex-noalign=0 · inline-layout=0
          z-adhoc=0 · hex-off=0 · btn-height-mix=0
  round2: 7/7 checked (evidence in gen log)
  date: YYYY-MM-DD -->
```
**checker เจอตราที่ไม่มีตัวเลข หรือตัวเลขไม่เป็นศูนย์โดยไม่มีเหตุ whitelist = BLOCK**
(ตรา "ผ่าน" เปล่า ๆ ปลอมง่าย — ตัวเลขปลอมยาก เพราะ Pass G ของ checker นับซ้ำแล้วต้องตรงกัน)

## Rule #69 — Kit Integrity + Late-Style Escape (v6.4 — จากการวินิจฉัย 2 กลไก)
**วินิจฉัย:** violation ใน CSS = สืบทอดจาก skeleton (ไม่ใช่โมเดลมั่ว) · inline ท้ายไฟล์ = single-pass
ย้อนกลับไปแก้ CSS ข้างบนไม่ได้ inline เลย "ถูกกว่า" เสมอ — กฎนี้ปิดทั้งสองทาง:
1. **BASE-KIT ห้ามแตะ** — CSS ระหว่าง marker `/* ===== BASE-KIT ===== */` … `/* ===== END BASE-KIT ===== */`
   ต้อง verbatim จาก skeleton — checker เทียบกับ template ต้นทาง แก้แม้บรรทัดเดียว = BLOCK
   (skeleton ผ่าน self_audit = 0 แล้ว — ลอกทั้งก้อน = สะอาดอัตโนมัติ ไม่ต้องออกแบบ CSS เอง)
2. **page CSS** เขียนใต้ END marker เท่านั้น — ใช้ค่าจาก scale/#61/#62 เหมือนกัน
3. **Late-Style Escape:** ตอนเขียน markup แล้วต้องการ style ใหม่ → เขียนลง `<style id="page-late">`
   ท้ายไฟล์ (มีให้ใน skeleton แล้ว) — **inline จึงไม่มีข้ออ้างว่า "จำเป็น" อีกต่อไป** (#56 เด็ดขาด 100%)
4. utils (#66/#68: positionMenu / openOverlay / global click) มากับ skeleton — **ห้ามเขียนเวอร์ชันตัวเอง**

## Checkpoint Protocol (กัน "ทำนานจนหลุด")
audit ครั้งเดียวท้ายไฟล์ = เจอ 50 จุดพร้อมกันตอนสายเกินแก้ — เปลี่ยนเป็นตรวจเป็นด่านระหว่างทาง:
| หลังจบ | ตรวจ | เกณฑ์ |
|---|---|---|
| Phase 2 วาง skeleton | `self_audit.py` ทั้งไฟล์ | **ต้อง 0 ทันที** (พิสูจน์ kit ไม่ถูกแตะ) |
| Phase 3 จบ**แต่ละ**หน้า | สแกนเฉพาะ chunk ที่เพิ่งเขียน: inline / class นอก kit ที่ไม่ได้ประกาศ / hint เปลือย | 0 ก่อนไปหน้าถัดไป |
| Phase 4 จบ JS | grep stopPropagation / เมนูใช้ openOverlay ครบ | 0 |
| Phase 5 | `self_audit.py` เต็ม + Role Sweep + ประทับตรา | 0 ทุกตัวนับ |

---

### Checklist ต่อท้าย (สำหรับ generator ติ๊กใน pre-flight)
- [ ] #50 spacing ทุกค่าใน scale
- [ ] #51 ฟอร์มบน grid ประกาศชัด + full-width ตั้งใจ
- [ ] #52 แถว action สูงเท่า/class เดียว/align center
- [ ] #53 ตาราง: เลขขวา tabular-nums, th=td align
- [ ] #54 padding ค่าเดียวต่อชนิด container
- [ ] #55 flex มี align-items / grid มี gap
- [ ] #56 ไม่มี inline layout style
- [ ] #57 ทุกจุด overflow มีคำตอบ
- [ ] #58 จังหวะแนวตั้งค่าเดียว
- [ ] #59 wizard ขอบนิ่งทุก step
- [ ] #61 font-size ≤8 ขนาด ทุกค่าใน type scale
- [ ] #62 z-index อ้าง var(--z-*) ทั้งหมด
- [ ] #69 BASE-KIT verbatim · page CSS ใต้ END marker · late style ใน #page-late
- [ ] #60 PREFLIGHT stamp แบบมีตัวเลข + ผ่าน Self-Review 2 รอบ (checkpoint ทุกด่าน)
