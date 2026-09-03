# _COVERAGE_REPORT — F-HR-RECRUIT (สรรหา)

**Skill:** qc-coverage-checker · **จังหวะ:** รอบ 1 (HTML vs contract) · **โหมด:** feature-prebrief (F127 · ไม่มี workflow_graph)
**Target:** `outputs/F-HR-RECRUIT/สรรหา.html` (2,830 บรรทัด)
**Contract:** `Pack Brief Feature/F-HR-RECRUIT/0_DIRECTION/PREBRIEF.md` + `FUNCTION_CHECKLIST.html` (21 FN + unsupported[] 5)
**วันที่:** 2026-09-02

---

## VERDICT: ✅ PASS

- **FN coverage: 21/21** — ทุก FN มี hook/ทางเข้าจริง + handler เดินได้ (ไม่ใช่ปุ่มหลอก) พร้อม evidence
- **Exception/edge paths: ครบ** — consent gate · duplicate เตือน · Manpower เตือน · offer นอก band เตือน · hired→handoff
- **unsupported[] 5 ข้อ: ไม่พบบนจอทั้งหมด** (0 scope creep)
- **Declaration hooks (round 1): ครบ** — DOA slot picker + timeline · NTF `ntf()` events · CSQ consent+mask+RESTRICTED · chip = detect (ไม่มี DIVERGENCE)

> หมายเหตุ archetype = **master** (requisition/candidate + pipeline board · **ไม่ใช่ Q-document**) ตาม PREBRIEF §2 → **Phase 0c Pattern Q surface coverage = N/A** (ตรวจ list/wizard/view/pdf/modals แบบ Q ไม่ใช้)

---

## Matrix — FN (21/21) · ติ๊กคอลัมน์ WF

| FN | ต้องทำอะไรได้ | WF | Evidence (route/selector/handler) |
|---|---|:--:|---|
| FN-01 | เปิดอัตรา (ตำแหน่ง·จำนวน·ระดับ·ช่วงเงินเดือน·hiring manager) | ✅ | `#recruit/req` → ปุ่ม "เปิดอัตราใหม่" `openReqCreate()` → `reqFormDrawer()` มี field ครบ (ตำแหน่ง/แผนก/จำนวน/band select/HM combobox) → `submitReq()` |
| FN-02 | เปิดอัตราแม้ไม่มี Manpower → เตือนทำได้ (hook display-only) | ✅ | `reqFormDrawer` L2497 note is-warn "ยังไม่ได้ระบุแผนอัตรากำลัง … เปิดอัตราได้"; list/view chip "ไม่มีแผน"; `manpower_ref` nullable, help "F124 ยังไม่มี · hook display-only" — **mock ที่ถูกต้อง [A-REC-01]** |
| FN-08 | ส่งอนุมัติ (req/offer) ผ่าน DOA slot picker ตามตำแหน่ง — ไม่ hardcode | ✅ | `openDoaModal()` → `renderModal()` t==='doa' render `.slot` + `searchSelectHTML('slot_N')` เลือกคน; `doaResolve()` คืน **slot เปล่า** (ไม่ hardcode คน); `submitDoa()` บังคับเลือกครบทุกขั้น |
| FN-16 | ปิดอัตรา (รับครบ/ยกเลิก) | ✅ | `reqViewDrawer` acts L2541-42 ปุ่ม "ปิดอัตรา" `reqClose()` → `openConfirm()` soft archive; auto-close เมื่อ `filled>=count` (L2741) |
| FN-03 | เพิ่มผู้สมัครเข้าคลัง (ชื่อ·ติดต่อ·resume·ตำแหน่ง) | ✅ | `#recruit/pool` → "เพิ่มผู้สมัคร" `openCandCreate()` → `candFormDrawer()` field ครบ + upload-zone resume → `submitCand()` |
| FN-04 | ผูกผู้สมัครกับอัตรา (application) | ✅ | `candFormDrawer` L2589 combobox `cand_req` "ตำแหน่งที่สมัคร" → `RC.draft.reqId`; `reqViewDrawer` แสดง "ผู้สมัครในอัตรานี้" (linked) |
| FN-05 | ยินยอม PDPA — ไม่ยินยอม = ดำเนินต่อไม่ได้ | ✅ | consent toggle L2593; gate: `candMoveStage` L2726 บล็อก, `candAssess` L2656 / `candOffer` L2671 บล็อกเมื่อ `!consent.ok`; banner + ปุ่ม "บันทึกความยินยอม" `candSetConsent()` |
| FN-14 | ตรวจซ้ำ/เคยสมัคร (email/เบอร์) → เตือน | ✅ | `findDuplicate()` L2602; note is-warn ใน form L2582 (live) + chip "เคยสมัคร" ใน pool/board/detail — **เตือนไม่บล็อก** |
| FN-06 | เลื่อนสถานะใน pipeline board | ✅ | `#recruit/board` → `renderBoardTab()` kanban 5 คอลัมน์ + `kbCard` ปุ่ม "ถัดไป/←" `candMoveStage()`; guard consent + viewer |
| FN-07 | นัดสัมภาษณ์ + แจ้งเตือน | ✅ | `candAssess` ปุ่ม "นัดสัมภาษณ์" `openInterviewModal()` → modal (วันที่/เวลา/ผู้สัมภาษณ์ combobox/สถานที่) → `saveInterview()` + `ntf()` |
| FN-09 | ประเมิน (scorecard ต่อผู้สัมภาษณ์) | ✅ | `candAssess` score-pick 1-5 + comment `pickScore/saveScore` L2668-69; snapshot ผู้สัมภาษณ์ชื่อ+ตำแหน่ง |
| FN-10 | สร้างข้อเสนอ (ตำแหน่ง·เงินตามระดับ·วันเริ่ม) → ส่งอนุมัติ | ✅ | tab ข้อเสนอ `candOffer()` create form (grade/start/salary + band scale) → `submitOffer()` → `openDoaModal('offer')`; band freeze `version_id` |
| FN-11 | ตอบรับ → hired → ส่ง On/Offboard (ไม่ทำเอง) | ✅ | `candHireHandoff()` L2739 `openConfirm` "ยิง event … soft-linkage · ไม่สร้าง employee"; chip "ส่งเข้า onboarding แล้ว" — **event stub ที่ถูกต้อง [OQ-15]** |
| FN-12 | ปฏิเสธ/ถอนตัว (บันทึกเหตุ) | ✅ | ปุ่ม "ไม่ผ่าน/ถอนตัว" `candTerminate()` → reason modal (select rejected/withdrawn/talent_pool + เหตุผลบังคับ) L2732; offer declined → withdrawn L2762 |
| FN-13 | ไม่ผ่าน (เหตุ) → เก็บ talent pool | ✅ | reason modal option "ไม่ผ่าน → เก็บ Talent Pool" (default) → `c.stage='talent_pool'` + reason; TERMINAL pill |
| FN-15 | รายงาน funnel/time-to-hire + filter | ✅ | `#recruit/report` `renderReportTab()` funnel bars + stat "Time-to-hire เฉลี่ย" + filter select "กรองตามอัตรา" (real `RC.f.report.req`) |
| FN-90 | ค้นหา/filter list + empty state | ✅ | `renderReqTab`/`renderPoolTab` input-search + status/stage select + ล้างตัวกรอง; `emptyStateHTML()` เมื่อ 0 แถว (L2342/2379) |
| FN-91 | ปิด/ยกเลิกผ่าน confirm + soft archive | ✅ | `reqClose` openConfirm soft archive; `candTerminate` reason modal; ทุก destructive มี confirm/reason |
| FN-92 | field validate + กัน double-submit | ✅ | `submitReq`/`submitCand`/`submitOffer` ตรวจ required + toast; `RC.busy` guard กันกดซ้ำ; `validateField()` component |
| FN-93 | audit ทุก create/แก้/เลื่อน/อนุมัติ (append-only) | ✅ | `audit()` L2263 `history.unshift`; `historySection()` "ประวัติ (append-only)"; เรียกในทุก action (create/edit/move/approve/reject/hire/close) |
| FN-94 | ปิดบังข้อมูลผู้สมัคร (RESTRICTED) ตาม role | ✅ | `maskEmail`/`maskPhone` + `PERSONAS.unmask`; `contactCell` ปิดบังเมื่อ !consent; chip "RESTRICTED · ปิดบังตามบทบาท"; persona switch (recruiter unmask / manager+viewer mask) |

---

## Matrix — Edge / Exception paths (PREBRIEF §9)

| Path | มีทางเข้าใน UI | Evidence |
|---|:--:|---|
| no-consent → บล็อกดำเนินต่อ | ✅ | `candMoveStage` L2726, `candAssess`/`candOffer` บล็อก; board `canFwd` require `consent.ok`; mask contact |
| duplicate → เตือน (ไม่บล็อก) | ✅ | `findDuplicate` live note ใน form + chip ทุกจอ |
| เปิดอัตราไม่มี Manpower → เตือน (ทำได้) | ✅ | note is-warn ใน form + chip list/view; `submitReq` audit kind='warn' |
| offer เงินนอก band → เตือน + บังคับเหตุผล | ✅ | `candOffer` L2705 note + field `out_of_range_reason` บังคับ; `submitOffer` L2714 บล็อกถ้าไม่มีเหตุผล; freeze band snapshot |
| hired → handoff On/Offboard (event) | ✅ | `candHireHandoff` ยิง event stub · ไม่สร้าง employee [OQ-15 · mock ถูกต้อง] |

---

## Matrix — unsupported[] 5 (ต้อง **ไม่มี** บนจอ)

| unsupported | สถานะบนจอ | Evidence |
|---|:--:|---|
| จ้างจริง/สร้าง employee record/สัญญาจ้าง | ✅ ไม่มี | `candHireHandoff` ระบุชัด "ไม่สร้าง employee และไม่เชื่อมจริง" — มีแค่ event ออก |
| ประกาศงานบน job board ภายนอก | ✅ ไม่มี | `reqAnnounce` = เปลี่ยนสถานะ→เปิดรับ (internal) เท่านั้น · ไม่มี integration job board |
| แบบทดสอบ/assessment · sourcing agency | ✅ ไม่มี | มีแค่ scorecard (=FN-09 ประเมิน) · ไม่มีหน้า assessment test / agency |
| offer letter PDF เลขรัน | ✅ ไม่มี | offer ไม่มี doc number/PDF gen · `DOCCFG chip —` สอดคล้อง |
| สร้าง/แก้ระดับ-band เงินเดือน | ✅ ไม่มี | BANDS อ่านอย่างเดียว (select) · help "อ่านจาก HR Configuration (ไม่แก้ในหน้านี้)" [#107] |

**Scope creep:** ไม่พบ (grep unsupported keywords = 0 hit)

---

## Matrix — Declaration coverage (round 1 = HTML hook · chip vs detect)

| ท่อ | chip §12 | detect ใน HTML | ผล | Evidence hook |
|---|:--:|:--:|:--:|---|
| DOA | ✓ | ✅ YES | match | `openDoaModal`/`submitDoa` slot picker เลือกคน + `approvalSection()` timeline + ปุ่มอนุมัติ/ไม่อนุมัติ (`reqApprove`/`offerApprove`) · **ไม่ hardcode chain** (`doaResolve` = slot เปล่า) |
| NTF | ✓ | ✅ YES | match | `ntf()` L2265 (comment "wire ENG-NOTIFY") ยิงที่ นัดสัมภาษณ์/offer sent/offer result/stage changed/ประกาศ/อนุมัติ |
| CSQ | ✓ | ✅ YES | match | PDPA consent gate + `maskEmail/maskPhone` + RESTRICTED chip + note is-danger "ชั้นความลับ" (SecC data-sensitivity) |
| DOCCFG | — | ❌ NO | match | ไม่มีเลขรัน/doc number บนจอ |
| PDF DOC | — | ❌ NO | match | offer letter = soft ref (ไม่มี PDF gen) |

**DIVERGENCE: — (ไม่มี)** · chip ตรงกับ detect ทุกท่อ

> **หมายเหตุ (ไม่ใช่ gap):** ไฟล์ `DOA_BRIEF` / `NTF_BRIEF` / `CSQ_BRIEF` **ยังไม่มี** ในโฟลเดอร์ — ถูกต้องตาม WF-01 C3.10: `*-declaration` รัน**หลัง step 7** และผู้ใช้เลือกเอง ไม่ใช่ deliverable ของ round 1 HTML → ไม่ BLOCK ที่ด่านนี้ · ตรวจ brief จริง = round 2 (Declaration ↔ FRD)

---

## ข้อสังเกตเล็กน้อย (ไม่กระทบ verdict)

1. **FN-15** "Time-to-hire เฉลี่ย: 23 วัน" เป็นค่า hardcoded และ "Export CSV" เป็น stub (`showToast … ต่อ dev`) — เป็น mock ที่ยอมรับได้สำหรับ prototype (funnel + filter เป็น handler จริง) · ให้ dev ผูกค่าจริงตอนทำระบบ
2. Manpower (FN-02) และ handoff On/Offboard (FN-11) เป็น **[AI-DEFAULT] ที่ตัดสินแล้ว** (F124/On-Offboard ยังไม่มี inbound) — hook/event stub ถูกต้องตามโจทย์ ไม่ใช่ของขาด

---

## สรุปสำหรับ WF-01

- **ผ่าน (PASS)** → ไปต่อ step 5 (e2e) ได้ · ทุก FN มี WF ✅ พร้อม evidence
- ไม่มี BLOCK · ไม่มี OQ ค้างใหม่ · ไม่มี scope creep · ไม่มี DIVERGENCE
- (round 2 ค้างไว้ตรวจ: rules ใน FRD 05_RULES · FN↔TC ledger · Declaration↔FRD sync read เมื่อมี brief จริง)
