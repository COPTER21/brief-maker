# Coverage Report — F-CUST-CL-001 (รอบ 2: HTML)

- วันที่: 2026-08-14 · node: Customer Credit Limit · Wave S2 · Iteration: 3
- Contract ที่ใช้: `PREBRIEF_F-CUST-CL-001_CustomerCreditLimit.md`, `FUNCTION_CHECKLIST_F-CUST-CL-001_CustomerCreditLimit.md`, `Central Plan v2` และ Customer Master ref
- Artifact ที่ตรวจ: `f-credit-limit.html`
- หมายเหตุ: ไม่พบ `workflow_graph.json`/`NODE_BRIEF` ใน input ที่ผู้ใช้กำหนด จึงใช้ PREBRIEF + Function Checklist เป็น contract รอบนี้ โดยไม่เรียก skill อื่นเพิ่ม

## Verdict: 🟡 WARN — no Credit Limit scope gap

สรุป: ครบ 19/23 · partial 4 · gap block 0 · gap warn 4 · NOT-CHECKED (FRD/TC) ทั้งรอบ 2

## Recheck result

- HTML implementation was re-rendered after the UX repair; the customer-credit workflows and evidence in the matrix remain available.
- The credit-limit request now explicitly covers the pre-submission state (`รอส่งอนุมัติ`) and the transition to DOA pending approval (`รออนุมัติ`).
- No new scope gap or block-severity gap was found.
- The four partial items are external, deferred integration contracts (My Profile, Sales Order, AR Invoice/SO read model and Customer Master create event), not missing UI work in Customer Credit Limit. Per PM/BA confirmation, SO, Invoice and Notification do not yet exist and must remain placeholders until their own feature packs are created.

## Coverage Matrix

| Item | ประเภท | HTML | FRD | TC | Evidence / หมายเหตุ |
|---|---|---:|---:|---:|---|
| FN-01 ตั้งวงเงินครั้งแรก | flow | ✓ | — | — | ลูกค้าเงินสดอยู่ใน `CREDITS`; `openChange()` line 804 + `submitChange()` line 961 |
| FN-02 เพิ่มวงเงิน | flow | ✓ | — | — | Change Drawer line 920; approve ครบสายแล้วเปลี่ยน limit line 974 |
| FN-03 ลดวงเงิน | flow | ✓ | — | — | amount ใหม่รับค่าต่ำกว่าเดิมและแสดง delta; ใช้ `submitChange()` ชุดเดียวกับเพิ่ม |
| FN-04 resolve DOA ตามจำนวน | rule | ✓ | — | — | `MOCK_DOA_SETS` line 630, `resolveDoa()` line 636, tier chips ใน Change Drawer |
| FN-05 fail-closed เมื่อไม่มี tier | exception | ✓ | — | — | `resolveChain()` คืน null; Change Drawer disable เมื่อ `!tier`; `submitChange()` block + toast |
| FN-06 เหตุผลว่าง/จำนวนเดิม disabled | validation | ✓ | — | — | `valid` ใน `changeDrawer()` line 920 และ `refreshChgFoot()` |
| FN-07 ไม่ hardcode สายจริง | integration | ✓ mock | — | — | `DOA_FEATURE_ID='F-CL-001'` line 627; mock แยกชัดและ UI ระบุว่าของจริง resolve จาก DOA |
| FN-08 ชื่อผู้เซ็นจาก My Profile | integration | △ | — | — | timeline แสดงผู้เซ็น/เวลา แต่ prototype ใช้ mock `ME`; ต้องยืนยัน integration จริงใน FRD |
| FN-09 อนุมัติทีละขั้น/เปลี่ยนเมื่อครบ | rule | ✓ | — | — | `approveStep()` line 974 advance step และเปลี่ยน limit เฉพาะขั้นสุดท้าย |
| FN-10 timeline อนุมัติ | UI state | ✓ | — | — | tab “คำขอ & อนุมัติ”; ภาพ `_ux_shots/04-view-approval.png` |
| FN-11 reject บังคับเหตุผล/วงเงินคงเดิม | exception | ✓ | — | — | `renderModal()` line 994 disabled จนมีเหตุผล; `doReject()` line 1031 ไม่แก้ limit |
| FN-18 สถานะกลาง ไม่มี My Approval | scope rule | ✓ | — | — | คำขอและปุ่มอนุมัติอยู่ใน View Drawer กลาง; ไม่มี route/menu My Approval |
| FN-12 hold + เหตุผล | exception | △ | — | — | Hold Modal + `doHold()` line 1038 ครบ; การ block ที่ SO เป็นข้อความ placeholder เพราะ SO ยังไม่มี |
| FN-13 unhold + เหตุผล | exception | ✓ | — | — | modal เดิมเปลี่ยนเป็น “ปลดระงับ”; `doHold()` toggle สถานะและ audit |
| FN-14 review credit + audit | action | ✓ | — | — | ปุ่ม “ทบทวน”; `reviewCredit()` line 992 อัปเดตวันที่และ audit |
| FN-15 limit/used/available/util | calculation | ✓ | — | — | `creditUsed/creditAvail/creditPct` lines 658–660; list + overview progress bar |
| FN-16 ปกติ/ใกล้เต็ม/เกิน + filter | state | ✓ | — | — | `creditState()` line 663; filter/KPI “ใกล้เต็มวงเงิน” และสีสถานะ |
| FN-17 AR + aging + DSO | integration | △ | — | — | tab AR และ KPI aging/DSO ครบ (`03-view-ar.png`) แต่ข้อมูลเป็น `TXNS` mock รอ AR Invoice/SO |
| FN-20 เงินสด limit 0 | state | ✓ | — | — | row `CUST-2026-0056` แสดง “เงินสด”; overview ไม่แสดง credit bar |
| FN-19 1 customer = 1 profile/ใหม่=0 | edge in | △ | — | — | sample key ใช้ customer code และมี cash profile; auto-create event ต้องยืนยันใน FRD/implementation |
| FN-21 search/filter/sort/empty | list | ✓ | — | — | `filtered()` line 730 + `listBody()` line 752; empty CTA และ sortable headers |
| FN-91 audit append-only | rule | ✓ mock | — | — | `pushAudit()` line 696 prepend event; ทุก action หลักเรียกใช้ |
| FN-92 Esc chain | interaction | ✓ | — | — | keydown handler lines 1055–1059: modal → change → view → close |

## 🟡 Gaps / Warnings

### GAP-01 · My Profile signer integration (FN-08)

- หาย: contract ว่าดึงชื่อ/ลายเซ็นจาก profile ณ ตอนกดอนุมัติ ไม่ใช่จาก DOA payload
- แก้ที่: FRD รอบ 2 — API/LOGIC ของ approve action และ rule ห้ามเก็บชื่อใน DOA

### GAP-02 · SO enforcement ยังเป็น placeholder (FN-12 / OB-9)

- หาย: integration จริงที่ Sales Order สำหรับ block/warn credit check
- แก้ที่: FRD รอบ 2 — XT cross-module contract ไป SO; ตอนนี้ UI ระบุจุด enforce แล้วตามคำยืนยันว่า SO ยังไม่เกิด

### GAP-03 · AR/SO source ยังเป็น mock (FN-17 / OB-7)

- หาย: source contract และ freshness/error behavior เมื่อ AR Invoice หรือ SO unavailable
- แก้ที่: FRD รอบ 2 — integration/read model; ตอนนี้ prototype ใช้ข้อมูล mock และบอกผู้ใช้ชัด

### GAP-04 · Auto-create profile ยังพิสูจน์จาก UI ไม่ได้ (FN-19 / OB-6)

- หาย: event/handler ตอน Customer Master สร้างลูกค้าใหม่แล้วสร้าง profile limit=0 อัตโนมัติ
- แก้ที่: FRD รอบ 2 — LOGIC/DB/event contract; HTML แสดงผลปลายทางได้แต่ไม่ใช่หลักฐาน backend event

## Notification obligation

- OB-10 (แจ้งเมื่อส่งคำขอ/อนุมัติ/ไม่อนุมัติ): HTML มี toast feedback แต่ยังไม่ประกาศ notification integration เพราะ Notification feature ยังไม่มีตามคำยืนยันของ PM/BA
- สถานะรอบนี้: `N/A-UI / deferred` — ต้องตรวจในรอบ `ntf-declaration` หลังผู้ใช้อนุมัติ Phase 1

## Scope Guard

- ✓ ไม่มี direct set ข้าม DOA
- ✓ ไม่มีการแก้วงเงินที่ Customer Master
- ✓ ไม่มี delete credit profile
- ✓ ไม่มี My Approval รายบุคคล
- ✓ SO/AR/Notification ถูกใช้เป็น mock/placeholder ไม่ถูกสร้างเป็น feature แทรก

## ⬜ NOT-CHECKED

- FRD Pack และ test cases ยังไม่ถูกสร้างตาม workflow จึงไม่ตรวจรอบ 2 และไม่นับเป็นผ่าน
- Formal `workflow_graph.json`/`NODE_BRIEF` ไม่อยู่ใน input; รายงานนี้ไม่อ้างว่าผ่าน graph contract
