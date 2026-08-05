# Pattern M — Landing / Home Page (Rule #48)

> ใช้กับ: หน้าแรกของระบบ, หน้า home ของ module, workspace ของ user
> Anchor: design-system.html `#/landing` — เลือกจาก **3 variants เท่านั้น** ห้ามออกแบบ landing ใหม่เอง
> นี่คือ internal tool — ❌ carousel, banner รูป stock, marketing copy

---

## เลือก Variant

| Variant | ใช้เมื่อ | ส่วนประกอบ |
|---|---|---|
| **M1 Hero + Tiles** | หน้าแรกทั้งระบบ / module ใหญ่หลาย feature | hero band + tiles grid |
| **M2 Workspace Grid** | หน้าแรกรายผู้ใช้ (task-oriented) | greeting + งานค้าง + shortcuts + รายการล่าสุด |
| **M3 KPI Home** | หน้าแรกเชิง monitoring | greeting + stats + chart ย่อ + รายการล่าสุด (= Pattern J3 ย่อ) |

## M1 — Hero + Tiles

```html
<div class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">[ชื่อระบบ/module]</h1>
    <p class="hero-sub">[อธิบาย 1-2 บรรทัด ว่าที่นี่ทำอะไรได้]</p>
    <div class="hero-actions"><button class="btn btn-primary">…CTA หลัก 1 ปุ่ม…</button></div>
  </div>
</div>
<div class="tiles">
  <a class="tile" href="#/[route]">
    <div class="tile-icon"><i data-lucide="[icon]" class="w-5 h-5"></i></div>
    <div class="tile-text">
      <div class="tile-title">[Feature]</div>
      <div class="tile-desc">[1 บรรทัด]</div>
    </div>
    <i data-lucide="chevron-right" class="w-4 h-4 tile-chev"></i>
  </a>
</div>
```
```css
.hero { background: linear-gradient(135deg, var(--c-navy) 0%, var(--c-navy-2) 100%); border-radius: var(--r-lg); padding: 40px; margin-bottom: var(--sp-xl); }
.hero-title { color:#fff; font-size: 26px; font-weight: 700; }
.hero-sub { color: rgba(255,255,255,0.75); font-size: var(--fs-body); margin-top: var(--sp-sm); max-width: 640px; }
.hero-actions { margin-top: var(--sp-lg); }
.tiles { display:grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: var(--sp-lg); }
.tile { display:flex; align-items:center; gap: var(--sp-md); background:#fff; border:1px solid var(--c-line-2); border-radius: var(--r-lg); padding: var(--sp-lg); transition: border-color 150ms, box-shadow 150ms; }
.tile:hover { border-color: var(--c-primary); box-shadow: 0 2px 8px rgba(17,17,17,0.05); }
.tile-icon { width:40px; height:40px; border-radius: var(--r-md); background: linear-gradient(135deg, var(--c-primary), var(--c-teal)); color:#fff; display:flex; align-items:center; justify-content:center; flex:0 0 auto; }
.tile-title { font-size: var(--fs-h3); font-weight:600; color: var(--c-ink); }
.tile-desc { font-size: var(--fs-meta); color: var(--c-mute-2); }
.tile-chev { margin-left:auto; color: var(--c-mute-3); }
```
- hero มี CTA primary ได้ **1 ปุ่มเดียว** (secondary เพิ่มได้ 1)
- tile กดได้ทั้งการ์ด, icon อยู่ใน gradient circle Primary→Teal เท่านั้น
- จำนวน tiles ตาม feature จริง — ห้ามยัด tile หลอก/coming soon เกิน 1

## M2 — Workspace Grid

```html
<div class="ws-greet">
  <h1 class="ph-title">สวัสดี, [ชื่อ user]</h1>
  <p class="ph-sub">[วันที่วันนี้ fmtDate] · คุณมีงานค้าง [N] รายการ</p>
</div>
<div class="ws-grid">
  <div class="card ws-span2"><!-- งานของฉัน: list ย่องานค้าง 5 แถว + "ดูทั้งหมด" --></div>
  <div class="card"><!-- Shortcuts: tile ย่อ 4-6 อัน (โครง .tile แบบ compact) --></div>
  <div class="card ws-span3"><!-- รายการล่าสุด / กิจกรรม (Pattern L3 timeline ย่อ) --></div>
</div>
```
```css
.ws-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: var(--sp-lg); }
.ws-span2 { grid-column: span 2; } .ws-span3 { grid-column: span 3; }
```
- งานค้างกดแถว → ไปหน้างานนั้น (Rule #41)
- จำนวนงานค้าง badge สี Warning ถ้า >0

## M3 — KPI Home

โครง = greeting (แบบ M2) → `.stats` row (≤4 cards) → chart 1 ตัว (Pattern J helper) → รายการล่าสุด
ใช้เมื่อ home ต้อง "เห็นสุขภาพระบบ" ตั้งแต่เข้า — ถ้าเนื้อหาเชิงวิเคราะห์มากกว่านี้ = แยกเป็นหน้า Dashboard จริง (Pattern J) แล้ว home ใช้ M1/M2

## Verification เฉพาะ pattern นี้
- [ ] ใช้ M1/M2/M3 ตรง variant — ไม่มี carousel/banner/รูป stock
- [ ] hero: CTA primary 1 ปุ่ม, gradient navy ตาม token
- [ ] tile icon = gradient circle Primary→Teal, กดได้ทั้งการ์ด
- [ ] greeting ใช้ fmtDate + จำนวนงานจริงจาก mock state
