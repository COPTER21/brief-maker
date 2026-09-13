# Pattern L — Collection Views (Card Grid / Kanban / Timeline)

> ใช้เมื่อ requirement ระบุมุมมองที่ไม่ใช่ตาราง — ถ้าไม่ระบุ default = Pattern A (table)
> Anchor: design-system.html `#/list` variants "Card Grid" / "Kanban Board" / "Timeline"
> กติการ่วม: Placement Contract (Rule #46) ใช้เหมือน list view ทุกข้อ — ปุ่มสร้างที่ `.ph-actions`, กด card/แถว = เปิด view drawer, badge ตำแหน่งตายตัว

---

## L1 — Card Grid (browse entities ที่เน้นหน้าตา/identity)

```html
<div class="card-grid">
  <div class="ent-card is-clickable" onclick="openView('${r.id}')">
    <span class="pill pill-info ent-card-status">ใช้งาน</span>   <!-- มุมขวาบน (Rule 46.3) -->
    <div class="ent-card-head">
      <div class="avatar">${initials(r.name)}</div>
      <div><div class="ent-card-title">${r.name}</div>
           <div class="ent-card-meta">${r.code}</div></div>
    </div>
    <div class="ent-card-body"><!-- 2-4 คู่ label:value (--fs-meta) --></div>
  </div>
</div>
```
```css
.card-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(260px,1fr)); gap: var(--sp-lg); }
.ent-card { position:relative; background:#fff; border:1px solid var(--c-line-2); border-radius: var(--r-lg); padding: var(--sp-lg); transition: box-shadow 150ms, border-color 150ms; }
.ent-card:hover { border-color: var(--c-primary); box-shadow: 0 2px 8px rgba(17,17,17,0.05); cursor:pointer; }
.ent-card-status { position:absolute; top: var(--sp-md); right: var(--sp-md); }
```
- filter bar อยู่ใน card แยกเหนือ grid (Rule #9 ใช้เหมือนเดิม) + toggle มุมมอง `list`/`grid` เป็น seg-control ขวาของ filter bar
- ห้าม action buttons บน card (แก้ไข/ลบ ทำจาก view drawer — Rule 46.4)

## L2 — Kanban Board (งานไหลตามสถานะ)

```html
<div class="kanban">
  <div class="kb-col" data-status="draft">
    <div class="kb-col-head"><span class="kb-col-title">ร่าง</span><span class="kb-count">4</span></div>
    <div class="kb-cards">
      <div class="kb-card is-clickable" onclick="openView('${r.id}')">
        <div class="kb-card-title">${r.name}</div>
        <div class="kb-card-meta"><span>${r.code}</span><span class="num">${fmtDate(r.due)}</span></div>
      </div>
    </div>
  </div>
</div>
```
```css
.kanban { display:flex; gap: var(--sp-md); align-items:flex-start; overflow-x:auto; padding-bottom: var(--sp-sm); }
.kb-col { flex: 0 0 280px; background: var(--c-bg-off); border:1px solid var(--c-line-2); border-radius: var(--r-lg); }
.kb-col-head { display:flex; justify-content:space-between; padding: var(--sp-md) var(--sp-lg); font-size: var(--fs-cap); font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color: var(--c-mute); }
.kb-card { background:#fff; border:1px solid var(--c-line-2); border-radius: var(--r-md); padding: var(--sp-md); margin: 0 var(--sp-sm) var(--sp-sm); }
```
- ลำดับคอลัมน์ = ลำดับ status flow จริง (ร่าง → รอ → กำลัง → เสร็จ) ตาม pill vocabulary กลาง
- หัวคอลัมน์ + count เสมอ; คอลัมน์ว่าง → empty state ย่อ (icon+1 บรรทัด)
- Drag-drop = optional; ถ้าทำ ให้เปลี่ยน status + toast; ถ้าไม่ทำ เปลี่ยนสถานะผ่าน view drawer
- Kanban ไม่แทนตาราง — ต้องมี toggle กลับมุมมอง list เสมอ

## L3 — Timeline / Activity Log

```html
<div class="timeline">
  <div class="tl-item">
    <div class="tl-dot is-success"><i data-lucide="check" class="w-3 h-3"></i></div>
    <div class="tl-body">
      <div class="tl-title">อนุมัติใบสั่งซื้อ <b>PO-2026-0042</b></div>
      <div class="tl-meta">สมชาย ใจดี · ${fmtDateTime(t)}</div>
    </div>
  </div>
</div>
```
```css
.timeline { position:relative; padding-left: 34px; }
.timeline::before { content:''; position:absolute; left:12px; top:6px; bottom:6px; width:1.5px; background: var(--c-line-2); }
.tl-item { position:relative; padding-bottom: var(--sp-lg); }
.tl-dot { position:absolute; left:-34px; width:26px; height:26px; border-radius:var(--r-full); background:#fff; border:1.5px solid var(--c-line); display:flex; align-items:center; justify-content:center; color:var(--c-mute-2); }
.tl-dot.is-success { border-color: var(--c-teal); color: var(--c-teal); }
.tl-dot.is-danger { border-color: var(--c-danger); color: var(--c-danger); }
```
- เรียงใหม่→เก่า, คั่นวันด้วย date divider (`--fs-cap` uppercase)
- dot สี = ประเภทเหตุการณ์ (success/danger/default) ตาม semantic tokens เท่านั้น
- ใช้เป็น tab "ประวัติ" ใน view drawer ได้ (โครงเดียวกัน)

## Verification เฉพาะ pattern นี้
- [ ] ปุ่มสร้างอยู่ `.ph-actions` (ไม่อยู่ใน column/card) — Rule 46.1
- [ ] กด card/kb-card เปิด view drawer — Rule #41
- [ ] มี toggle มุมมองกลับ list (L1/L2)
- [ ] status ใช้ pill vocabulary กลาง + ตำแหน่งตาม Rule 46.3
- [ ] คอลัมน์/กลุ่มว่างมี empty state
