# Coverage Report — F-WH-PACK (รอบ 1: HTML)

- วันที่: 2026-08-19
- Artifact: `outputs/03_PACK/f-wh-packing.html`
- Contract basis: PREBRIEF + Function Checklist, Central Plan v2, Picking final contract
- `workflow_graph.json` / NODE_BRIEF: ไม่พบใน workspace; ใช้เอกสารธุรกิจที่ยืนยันแล้วแทนตาม workflow ของโครงการ
- UX gate: `WAIVED-BLOCK` โดยผู้ใช้; finding เดิมยังคงเป็น technical debt

## Verdict: 🟡 WARN

สรุป: UI/function coverage 31/31 · cross-feature contract confirmed 1/3 · NOT-CHECKED 2

## Coverage Matrix

| Item | ประเภท | HTML | Evidence / หมายเหตุ |
|---|---|:---:|---|
| FN-01 คิวจาก Picking `to_pack` | function | ✓ | queue/list seed + PICK state/data block lines 897–919 |
| FN-02 ดูรายการที่หยิบมา | function | ✓ | row/detail modal + start action ใน queue renderer |
| FN-03 wave แตกต่อ SO | function | ✓ | `splitPackJobs`/job key ตาม source ref; Picking contract ส่ง `pack_refs[]` |
| FN-04 งาน Transfer | function | ✓ | mock PICK-0889 และ `srcType` ที่ lines 897, 911; contract ต้นทางยัง NOT-CHECKED |
| FN-05 เริ่มแพ็คและเลข PACK | function | ✓ | start pack/state initialization + stepper/workspace |
| FN-06 เลือกชนิดกล่อง | function | ✓ | box combobox/master + recommendation |
| FN-07 กล่องกำหนดเอง | function | ✓ | custom carton modal + tare/name binding |
| FN-08 scan/type หลายรูปแบบ | function | ✓ | `scanAdd`, `scanKey` lines 1183–1184 |
| FN-09 ใส่ของด้วยแถว/จำนวน/ทั้งหมด | function | ✓ | row actions, quantity input, add-all handlers |
| FN-10 ปรับ/เอาออก/clamp | function | ✓ | quantity mutation + remaining calculation/guard |
| FN-11 undo 10 ขั้น | function | ✓ | snapshot/undo stack + Ctrl+Z handler |
| FN-12 เปลี่ยนกล่องและคำนวณใหม่ | function | ✓ | carton type selection + weight recalc/warning |
| FN-13 ทางลัด 2 แบบ | function | ✓ | one-carton action + `autoPackAll` line 1185 |
| FN-14 น้ำหนักคำนวณและ override | function | ✓ | `calcW` + weight input/action |
| FN-15 ปิดกล่อง/F2/F3 | function | ✓ | close/new carton actions + keyboard handler |
| FN-16 BOXLABEL 150×100 | print | ✓ | print tab + `06_PRINT/BOXLABEL_template.html`/sample |
| FN-17 PACKSLIP A4 | print | ✓ | print tab + generated `06_PRINT/PACKSLIP_template.html`/sample |
| FN-18 finish guard | rule | ✓ | remaining/open-carton condition + packed state |
| FN-19 ออก DN | edge out | ✓ | `toDN`/DN mock + shipped lock; contract DN จริง NOT-CHECKED |
| FN-20 disabled พร้อมเหตุ | exception | ✓ | finish button disabled/reason rendering |
| FN-21 reopen ก่อน DN | exception | ✓ | reopen pack/carton + invalidate/reprint behavior |
| FN-22 free/cold/pickup | exception | ✓ | mock flags `is_free`, `cold`, pickup + print notes |
| FN-23 cancel พร้อมเหตุผล | exception | ✓ | cancel modal/reason + return queue logic |
| FN-24 permission | permission | ✓ | `PERSONAS`/role guard + shipped lock lines 820–822 |
| FN-25 closed-mode summary | state UI | ✓ | workspace renderer branches by `in_progress` |
| FN-90 list/search/filter/export | general | ✓ | two tabs, filters, CSV action, progress |
| FN-91 detail 4 tabs | general | ✓ | box/detail/print/audit panes |
| FN-92 fixed workspace composition | general | ✓ | two-column workspace + closed section + sticky actions |
| FN-93 hotkeys/focus/Esc | general | ✓ | Enter, F2, F3, Ctrl+Z, Escape handlers |
| FN-94 append-only audit | audit | ✓ | `pushAudit` invoked by carton/state/shortcut actions |
| FN-95 responsive/no flicker | non-functional | ✓* | responsive CSS exists; UX render proof waived, จึงถือเป็น acceptance target ไม่ใช่ผลผ่าน production |
| Picking → Packing | edge in | ✓ | locked Picking API `POST /api/v1/picks/:id/send-to-packing`; `picked → to_pack`; `pack_refs[]`; idempotent per source SO |
| Transfer → Packing | edge in | NOT-CHECKED | HTML รองรับ mock แต่ไม่มี locked Transfer artifact; Picking final รองรับ source SO เท่านั้น |
| Packing → Delivery Note | edge out | NOT-CHECKED | HTML มี mock hook แต่ผู้ใช้ยืนยันว่าไม่มี Delivery Note artifact; ห้าม invent API/schema |
| Packing → print docs | edge out | ✓ | PACKSLIP A4 + BOXLABEL 150×100 พร้อม print spec |

## Warnings / Contract Gaps

### COV-W01 · Transfer source contract ยังไม่มีเจ้าของ

- HTML รองรับ Transfer แต่ Picking final contract ระบุ source SO เท่านั้น
- ตีความในรอบนี้: Transfer เป็น alternate intake ในอนาคต ไม่ใช่ payload จาก Picking
- แก้ที่ downstream: FRD ต้องเก็บเป็น `OQ-XT-01` และห้ามประกาศ endpoint/fields จนมี locked Transfer contract

### COV-W02 · Delivery Note มีเพียง UI handoff

- PM/BA ยืนยันว่าไม่มี Delivery Note artifact
- FRD ระบุเฉพาะ outbound intent + idempotency/lock expectations ที่ Packing ต้องรับผิดชอบ และทำเครื่องหมาย contract/schema เป็น OQ
- ห้ามยืนยันว่า SO/Inventory ถูก update สำเร็จโดย Packing เองจน DN owner กำหนด contract

### COV-W03 · UX technical debt ถูก waive

- `FN-95` และคุณภาพ interaction เชิงภาพยังไม่ได้รับการรับรอง เพราะ `_UX_CHECK_REPORT.md` เป็น `WAIVED-BLOCK`
- Test cases ต้องมีเคสตรวจ responsive, tab/overlay และ dead-handler โดยตรง

## Scope Guard

- ไม่รวม picking execution, route/vehicle planning, split shipment, serial scan, photo proof และค่าขนส่ง
- ไม่ใช้ `doccfg-declaration` ตามคำสั่งผู้ใช้ แม้ feature มีเลขเอกสาร; FRD จะอ้าง shared numbering contract เป็น dependency/OQ เท่านั้น
- ไม่ใช้ `doa-declaration`; Packing ไม่มี approval chain ใน scope
- ใช้ `ntf-declaration` หลัง FRD ตาม authorization

## Gate decision

`WARN — proceed` ภายใต้ UX waiver และ contract guards ข้างต้น
