# Coverage Report — F-WH-STOCKTAKE (รอบ 1: HTML)

- วันที่: 2026-09-20 · PM/BA feedback re-gate
- Contract: PREBRIEF + FUNCTION_CHECKLIST ที่ผู้ใช้ยืนยัน, `CENTRAL_PLAN_CORE_ERP.md`, `Cube_Feature_List.html`, locked F082 context
- Node: F084 Stocktake · W4-LITE · architecture `master`
- Artifact: `F-WH-STOCKTAKE.html`
- หมายเหตุ: workspace ไม่มี `workflow_graph.json`/NODE_BRIEF จาก mapper สำหรับ node นี้ จึงใช้ confirmed feature brief เป็น node contract ตาม workflow ของ workspace โดยไม่เพิ่มกฎจากความจำ

## Verdict: 🟢 PASS

สรุป: FN ครบ 12/12 · feedback fixes 8/8 · Manual Test fixes 3/3 · E2E 20/20 · BLOCK 0 · WARN 0

## Coverage Matrix

| Item | ประเภท | HTML | Evidence / หมายเหตุ |
|---|---|:---:|---|
| FN-01 กำหนดพื้นที่นับแบบค้นหา | function | ✓ | `#/create` · `.combo` ใน `renderDrawer()` + `choose('คลัง/ตำแหน่ง', …)` |
| FN-02 แสดงสินค้า/ตำแหน่งแบบ soft-reference | function | ✓ | `#/sheets` · `renderSheets()` อ่าน `ITEMS`/`LOCATIONS` โดยไม่สร้าง master |
| FN-03 ล็อกเฉพาะพื้นที่และกันรอบซ้อน | block rule | ✓ | `freezeRound()` + `scopesOverlap()` บล็อก exact/parent/child scope |
| FN-04 เก็บยอดตั้งต้น ณ เวลาล็อก | block rule | ✓ | `freezeRound()` copy `{item, qty}` เข้า `snapshot`; แสดง `freezeAt` |
| FN-05 สร้างใบนับและมอบหมายคนจริง | function | ✓ | `#/sheets` · `openAssign()` + person combobox (ชื่อ/ตำแหน่ง/แผนก) |
| FN-06 blind count / supervisor reveal | permission | ✓ | `canSeeSystem()` คุม column “ยอดตั้งต้น”; counter ไม่เห็น |
| FN-07 ศูนย์ได้; ติดลบ/ว่างไม่ได้ | validation | ✓ | number input `min=0`; `submitCount()` ใช้ `Number.isFinite` และ `<0` block |
| FN-08 ผลต่าง + threshold effective date | rule | ✓ | `submitCount()` ใช้ `abs(diff) > varianceThreshold`; `#/variance` แสดงค่าและวันที่มีผล |
| FN-09 นับซ้ำโดยคนอิสระ | exception | ✓ | status `recount`; `confirmModal()` บล็อกคนเดียวกับ `assignee` |
| ผู้ส่งผลนับต้องเป็นผู้ได้รับมอบหมาย | permission | ✓ | `renderSheets()` ซ่อน controls จากคนอื่น; `submitCount()` guard `currentPersonId===assigned` |
| FN-10 DOA ตามมูลค่า + approve/reject/audit | governance | ✓ | `varianceTotal()` + `MOCK_DOA_ENTRY`; ไม่ prefill; guard status/person; เดินอนุมัติทีละขั้น |
| FN-11 ส่งผลต่างไป F082 แล้วปลดล็อก | edge out | ✓ | `handoff()` guard approved/idempotent; payload lines + ack; ไม่แก้ `ITEMS.qty` |
| FN-12 แยก Stocktake จาก Cycle Count ABC | scope guard | ✓ | routes/tabs มีเฉพาะรอบนับใหญ่; ไม่มี Cycle Count/ABC action ใน rendered DOM |
| Inventory → Stocktake | edge in | ✓ | `snapshot` เก็บยอดอ้างอิง; counter ถูกซ่อนและ supervisor reveal ตามสิทธิ์ |
| Stocktake → Stock Adjustment (F082) | edge out | ✓ | payload `{ref_count_doc,scope,freezeAt,approvedBy,lines[]}` + ack `{adjId,status}` |
| DOA → Stocktake | governance edge | ✓ | เลือกผู้อนุมัติจากคนจริง; pending/approved/rejected แยก state |
| ไม่เป็น Pattern Q/เลขรัน/PDF | scope guard | ✓ | ไม่มี wizard เอกสาร, running number หรือ print/PDF action |
| ไม่แก้ inventory on-hand โดยตรง | golden rule | ✓ | `handoff()` ไม่แก้ `ITEMS`; E2E FN-11 เปรียบเทียบ before/after |
| F086 Cycle Count ABC | deferred feature | N/A-UI | ตั้งใจไม่แสดงใน W4-LITE ตาม PREBRIEF; ไม่ถือเป็น gap |
| F089 → F084 scan data | data edge | ✓ | ปุ่ม “สแกน” display-only แจ้งว่า prototype ใช้คีย์มือ + source anchor |
| CSQ variance approved / handoff | declaration anchor | ✓ | source anchors 2 event + audit event ตอน approved/handoff |
| Movement lock | integration rule | ✓ | `STOCKTAKE_LOCKS`; push ตอน freeze, remove ตอน rejected/closed; chip บน list/sheet |

## Gaps

ไม่มี gap ระดับ BLOCK/WARN ในรอบ 1

## Scope creep

ไม่พบ route/action นอก confirmed scope

## Manual Test layout re-gate

- ปรับเฉพาะ presentation ของ action footer และ handoff summary; route, state transition, edge, rule และ business payload ไม่เปลี่ยน
- Regression: UI-01 ตรวจช่องไฟปุ่มอย่างน้อย 8px · UI-02 ตรวจว่าไม่มี `.card` ซ้อน `.card` ในประวัติ
- Permission regression: SEC-01 ตรวจว่าคนอื่นไม่เห็น controls และเรียก `submitCount()` ตรงก็ไม่เปลี่ยนสถานะ

## รอบ 2: FRD + Test Cases — 2026-09-20

### Verdict: 🟢 PASS

สรุป: FN 12/12 · Rules 10/10 · UI routes 5/5 · Cross-module 5/5 · Lock decisions 5/5 · BLOCK 0 · WARN 0

| Contract | FRD evidence | Test evidence | ผล |
|---|---|---|:---:|
| FN-01–FN-04 รอบนับ/scope/lock/snapshot | `01_UI`, `03_LOGIC`, `05_RULES` BR-ST-01/02 | TC-ST-01–05,26 | ✓ |
| FN-05–FN-09 assign/blind/validate/recount | `01_UI` UI-03, `03_LOGIC`, BR-ST-03/04 | TC-ST-06–13,22 | ✓ |
| FN-10 DOA ตามมูลค่าและลำดับ | `02_API` API-07, BR-ST-05, `DOA_BRIEF_F-WH-STOCKTAKE.md` | TC-ST-14–18,27 | ✓ |
| FN-11 draft-only handoff ไป F082 | `02_API` API-08, `03_LOGIC` ENG-ST-02, BR-ST-06 | TC-ST-19–20,25 | ✓ |
| FN-12 ไม่รวม Cycle Count ABC | `00_OVERVIEW`, LOCK-ST-04 | TC-ST-21 | ✓ |
| F082 contract: source=count/ref/lines/ack | `02_API` integration payload, `03_LOGIC` handoff | TC-ST-19,20,25 | ✓ |
| Movement lock/cut-off/unlock | `03_LOGIC`, BR-ST-02/06 | TC-ST-04,19,25,26 | ✓ |
| Permission/tenant/audit | `04_DB`, `05_RULES`, R10 classification | TC-ST-08,09,14–18,22 | ✓ |
| Optimistic concurrency/idempotency | `02_API` error contract, `03_LOGIC` | TC-ST-23–24 | ✓ |
| Scope locks 5 รายการ | `07_LOCKED_DECISIONS.md` | TC-ST-19,21,25,27 | ✓ |

### Round-2 notes

- ทุก block rule ใน `05_RULES.md` มี negative/permission case ที่ตรวจผลได้
- การส่งต่อ F082 เป็น draft-only; F084 ไม่แก้ on-hand และปิดรอบเมื่อได้ ack สำเร็จเท่านั้น
- DOA declaration ระบุ action `approve_variance` และสูตรฐานมูลค่า แต่ production role/tier mapping ยังเป็น business OQ ไม่ถูก hardcode
- เคส backend/concurrency/adapter ถูกระบุเป็น integration casesอย่างชัดเจน ไม่อ้างว่า single-file prototype พิสูจน์ได้
