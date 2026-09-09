# NTF_BRIEF — F131 Performance / ประเมินผลงาน (F-HR-PERF)

> **ยิงผ่าน ENG-NOTIFY (F-NOTIFY) เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature**
> **doa_pending / doa_result มาจาก ENG-DOA อัตโนมัติ — ❌ ไม่ประกาศซ้ำในใบนี้** (ประกาศซ้ำ = BLOCK)
> Source of truth: FRD Pack (03_LOGIC §3.1 FN-01/FN-07/FN-13 · §3.2 ENG-NOTIFY · 02_API §API-02/12/15 · §2.X · 05_RULES BR-08/EC-09)
> รันหลัง step 7 (FRD) · WF-01 declaration · 2026-09-09

---

## Declared Business Events (feature ของตัวเอง)

| Event ID | Trigger (state transition · อ้าง FRD) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|:--:|
| `perf.cycle.opened` | **S-01** · `createCycleFromConfig` → cycle.status `draft→open` (03_LOGIC FN-01 · API-02 side-effect) | พนักงาน + หัวหน้าในรอบ | รอบประเมิน **{cycle}** เปิดให้กรอกแล้ว | in-app + email | ✓ |
| `perf.deadline.overdue` | **S-08** · `sendReminder` — `isOverdue` = `status≠published && due<today` (03_LOGIC FN-13 · API-15 · EC-09) | ผู้ที่ยังไม่กรอก/ยังไม่ครบขั้น | แบบประเมิน **{cycle}** ครบกำหนด {date} — กรุณาดำเนินการ | in-app + email | ✗ (บังคับ) |
| `perf.result.published` | **S-05** · `recordCalibrationStage` ขั้นสุดท้าย → appraisal.status `calibration→published` (03_LOGIC FN-07 · API-12 isLast) — **per-person publish** | พนักงานเจ้าของผล | ผลประเมินรอบ **{cycle}** เผยแพร่แล้ว | in-app | ✗ |

- ทุก event ยิงผ่าน `ENG-NOTIFY.emit(event_id, { ref, vars })` ที่จุด transition — **feature ไม่เช็ค user preference/channel เอง** (config กลาง).
- `ref` (soft-reference): `perf.cycle.opened` → `cycle_id` · `perf.deadline.overdue` → `appraisal_id`/`cycle_id` · `perf.result.published` → `appraisal_id` + `employee_ref`.
- ข้อความ template อยู่ในใบประกาศนี้ **ไม่ฝังใน code feature**.

---

## Re-publish (ไม่ใช่ event ใหม่)

- **re-open → re-publish** (`reopenPublished` · FN-09 · API-14) — ผลกลับขั้น mgr แล้วเดินขั้นเผยแพร่ใหม่ → **`perf.result.published` ยิงซ้ำ per-person** (notif ใหม่ตอน re-publish · 02_API §2.X).
- **ไม่มี event แยกสำหรับ re-open** — re-open เองไม่ notify (FRD ระบุ notify เฉพาะ 3 event ข้างบน · S-05 ครอบ re-publish). ถ้าภายหลังต้องการแจ้ง "ผลถูกเปิดแก้" → เป็น event ใหม่ที่ต้องเคาะ (ไม่อยู่ในขอบเขตรอบนี้).

---

## ❌ ไม่ประกาศในใบนี้ (มาจาก engine อื่น)

| ท่อ | เหตุผล |
|---|---|
| `doa_pending` / `doa_result` | มาจาก **ENG-DOA** อัตโนมัติ (staged calibration) — ประกาศซ้ำ = BLOCK · ดู DOA_BRIEF |
| `perf.result.published` (7C queue side) | เป็น **ENG-CSQ** event (SecC/DC) — คนละท่อกับ notify · ดู CSQ_BRIEF |
| dispatch events (`perf.gap.training_requested` · `perf.result.movement_requested` · `perf.result.succession_candidate`) | เป็น **cross-module event/hook** (02_API §2.X) ไม่ใช่ user notification |

---

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

- กลุ่มใหม่ **"ประเมินผลงาน (Performance)"** → เพิ่ม 3 event: `perf.cycle.opened` · `perf.deadline.overdue` · `perf.result.published`.
- ตรวจชนกับ catalog เดิม: ไม่มีชื่อซ้ำ/ความหมายซ้อน (feature-scoped prefix `perf.*`).

## Dev wiring note

- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref, vars })` ที่ transition ตาม trigger ข้างบน — **ห้ามเช็ค preference/channel เอง**.
- `perf.result.published` ผูกจุดเดียวกับ ENG-CSQ emit (API-12 isLast) แต่ **คนละ engine** — ยิงทั้งคู่ต่อ 1 publish รายคน.
