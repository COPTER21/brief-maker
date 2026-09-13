# Pattern P — Day Planner / Team Scheduler (CUBE Warm Light) ⭐ v9

> **Reference (verbatim source):**
> - `references/planner/_SOURCE_op-action-plan.html` — F-95D "แผนงานประจำวันของฉัน" (my plan)
> - `references/planner/_SOURCE_team-plan.html` — "แผนงานของทีม" (หัวหน้าดู/จัดแผนให้ลูกทีม)
>
> ทั้งสองไฟล์ผ่าน PREFLIGHT v6.4 + vibe จาก user แล้ว — ใช้เป็น golden reference สำหรับ
> feature ประเภท **"หยิบงานจากคลัง → วางลงวัน/เวลา → ดูโหลด/ความคืบหน้า"** (Operation Process, งาน dispatch,
> ตารางกะ, maintenance schedule, planner ของ PM)

---

## 🎯 When to Use

✅ มี **คลังงาน (pool)** ที่ยังไม่ถูกจัด + **แผนรายวัน** ที่มีลำดับ/เวลาเริ่ม/ระยะเวลา + โควตาต่อวัน (capacity)
✅ ต้องเห็นภาพรวมเป็น **ปฏิทินเดือน** (โหลดต่อวัน) และ **timeline/Gantt รายวัน**
✅ มีมิติ "ของฉัน" vs "ของทีม" (หัวหน้าจัดให้ลูกทีม)

❌ Kanban ล้วน (Pattern L) · Runner ติ๊กขั้นตอน (Pattern O) · Dashboard (J)

---

## 🗺️ Route / Page map (ล็อก)

### P1 — My plan (`_SOURCE_op-action-plan.html`)
| Route | Page fn | เนื้อหา |
|---|---|---|
| `#/plan` | `pageList()` | ปฏิทินเดือน (`.cal-grid` 7 col) ↔ list (`seg-control` สลับ) · stats row · legend |
| `#/plan/day/:date` | `pageDay()` | header + `.stats` 6 ตัว (คลิกกรอง `setGf`) → `.dayswitch` seg [แผน | Gantt | บันทึกงาน] → ตาราง/`.gt-*` Gantt/`.daylog` |
| `#/plan/build` | `pageBuild()` | `.split` 2 pane: ซ้าย **คลังงานที่รอจัด** (seg ทั้งหมด/Operation/Ticket + filter + `.pool-card` draggable + ปุ่ม `จัดงานโดย AI` `.btn-ai`) · ขวา **แผนวันนี้** (`.plan-row` draggable เรียงลำดับ · เวลาเริ่ม `.time-input` · ระยะเวลา `.dur-*` · `.cap-track` โควตา) |

### P2 — Team plan (`_SOURCE_team-plan.html`) = P1 + ชั้นทีม
| Route | Page fn | เนื้อหา |
|---|---|---|
| `#/team` | `pageTeam()` | stats ทีม (คน / SOW วันนี้ / โหลดเกิน / ยังไม่มีแผน / งานครบกำหนดยังไม่ลงแผน) → `.wk-table` ตารางสมาชิก × 7 วัน (`.wk-load` bar ต่อ cell) · `.daynav` เลื่อนวัน |
| `#/team/:uid` | `pageMember()` | = P1 `#/plan` ของคนนั้น + **`.mbar` member bar** บนสุด (avatar · ชื่อ · role · tag "แก้ไขในฐานะหัวหน้า") |
| `#/team/:uid/day/:date` | `pageDay()` | = P1 day + `.mbar` |
| `#/team/:uid/build` | `pageBuild()` | = P1 build + `.mbar` |

**`.mbar` ต้องอยู่ทุกหน้าที่อยู่ในบริบทลูกทีม** — กันหัวหน้าแก้แผนผิดคน (audit ในชื่อหัวหน้า)

---

## 🧱 Components เฉพาะ pattern (CSS อยู่ในไฟล์ reference — ลอก class + ค่า)

| Component | class | สาระ |
|---|---|---|
| Calendar month | `.cal .cal-top .cal-dow .cal-grid .cal-cell(.is-today/.is-weekend/.is-blank/.is-empty) .cal-num .cal-sow .cal-load .cal-load-fill .cal-risk .cal-legend` | cell = `<button>` ทั้งก้อน · min-height 96 · โหลด bar + จุดเสี่ยง · `min-width:720` scroll |
| Day nav | `.daynav .daynav-date .daynav-label .daynav-dow .dateinput` | ‹ [calendar วันที่ · dow · relative] › + `<input type=date>` + `วันนี้` |
| Stats (คลิกได้) | `.stats > button.stat(.is-on) .stat-label .stat-value .stat-meta(.is-ok/.is-warn)` | ≥4 ตัว · กด = ตั้ง filter (Rule #70) |
| Segmented | `.seg-control > .seg-item(.is-active)` | สลับ view/tab ในหน้า (ไม่ใช่ `.tabs` ของ drawer) |
| Pool card | `.pool-card(.is-soon) .pool-head .pool-code .pool-parent .pool-due(.is-late/.is-soon/.is-none) .pool-add .pool-name` | `<button draggable>` · click = `addOne(id)` · drag = `dragPoolStart` · ข้อมูลรองไป `title` |
| Plan row | `.plan-row(.is-over/.is-dragging/.is-locked) .plan-ord .plan-main .plan-name .plan-sub .plan-src .plan-tools` | grid `28px 1fr` · drag reorder (`dragItemStart/dragOverRow/dropOnRow`) · locked = งานปิดแล้ว dashed |
| Duration/time | `.time-box .time-input .time-end .dur-box .dur-select .dur-val .dur-fixed` | `setStart/setDur/bumpDur/resetDurToSla/restackFrom` |
| Capacity | `.cap .cap-top .cap-track .cap-fill(.is-warn/.is-over) .cap-main .cap-strong` | โควตา นาที/วัน (`CFG.capacity_min_per_day`) · >80% warn · >100% over |
| Gantt day | `.gt-wrap .gt-head .gt-hours .gt-hour .gt-rows .gt-row .gt-lbl(.gt-lbl-name/.gt-lbl-sub) .gt-track .gt-bar(.is-p0..p3/.is-done/.is-late) .gt-now .gt-legend` | แกนชั่วโมง · bar ต่อ item · เส้น now |
| Day log | `.daylog .dl-row .dl-time .dl-ico .dl-main .dl-act .dl-ref .dl-detail` | timeline การกระทำ (`logAct`) |
| Team week | `.wk-table .wk-h .wk-cell .wk-c .wk-d .wk-load(.is-over/.is-warn/.is-none)` | คน × 7 วัน · cell = ปุ่มเปิด day ของคนนั้น |
| Member bar | `.mbar .mbar-av .mbar-txt .mbar-name .mbar-role .mbar-tag` | บริบท "กำลังแก้แผนของใคร" |
| AI button | `.btn.btn-ai` | `aiPlanDay()` — เรียงจาก เลยกำหนด → ครบวันนี้ → priority → SLA สั้น · ไม่เกินโควตา · ต้องผ่าน confirm modal |
| Kind/priority badges | `.kind-badge.kind-CL/.kind-SOP/.kind-TK .prio.is-p0..p3 .type-tag.type-*` | vocabulary ตาม microcopy.md |

---

## ⚙️ Behavior contract

- **Drag & drop** ใช้ HTML5 DnD + `.drag-float` ghost (`paintFloat/queueFloat`) · drop บนแถว = แทรกก่อนแถวนั้น · drop บน list ว่าง = ต่อท้าย · `dragEndAny()` ล้าง mark เสมอ
- **Auto-save** ใน build page (pill `บันทึกอัตโนมัติ`) — `markDirty()` แล้ว `finishBuild()` กลับ day view · `cancelBuild()` ถามยืนยันถ้า dirty
- **Locked items** (งานปิดแล้ว/ทำแล้ว) ย้ายไม่ได้ ลบไม่ได้ — `guardLocked()`
- **Overlap** (`overlapCount`) และ **over/under SLA** (`deltaBadge`) แสดงเป็น badge ในแถว + stat
- **Accuracy** ของแผน (`dayAccuracy`) = เวลาจริง/เวลาแผน — โชว์เมื่อมี actual
- render ใช้ `preserveRenderState/restoreRenderState` (Rule #29) + `applyGeom()` หลัง render (Gantt วัดความกว้างจริง)
- Drawer: view item (`renderViewDrawer` tabs: รายละเอียด / ประวัติ) + edit (`renderEditDrawer` เวลา/ระยะ/memo) — ใช้ kit drawer 920 มาตรฐาน · source drawer (`openSourceDrawer`) เปิดงานต้นทาง (SOW/Ticket)

---

## ✅ Self-check เพิ่ม

- [ ] มี 3 มุมมอง: ปฏิทินเดือน · วัน (แผน/Gantt/log) · build (pool+plan)
- [ ] pool card = button draggable + click add · plan row reorder ได้
- [ ] capacity bar + over/under badge + overlap
- [ ] stats ≥4 กดกรองได้ · seg-control ไม่ใช่ `.tabs`
- [ ] (team) `.mbar` ทุกหน้าลูกทีม · `.wk-table` คน×7วัน
- [ ] AI plan ผ่าน confirm modal · เคารพโควตา
