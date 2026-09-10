# 06_TESTS — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Audience:** QA
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + HTML (ข้อความจริงบนจอ verbatim)
> **Chain:** ไฟล์นี้เป็น input ให้ ai-testcase-md-generator + qa-friendly-html-generator

---

## §6.1 Acceptance Criteria (AC)

### AC-01: สร้างใบเบิก + header snapshot (FN-01/02/06)
**Given** role=ผู้เบิก, cat ∈ HR Config **When** wizard step2 เลือกผู้เบิก → แสดง hookbox "ตำแหน่ง … (ดึงจากตำแหน่ง ณ วันเบิก · Movement)" **And** step3 เพิ่มรายการ **When** POST /expenses
**Then** 201, status='draft', doc_no=null **And** emp_snapshot (position/cc) เก็บ ณ วันเบิก **And** audit entry "สร้างใบเบิก"

### AC-02: line editor VAT none/add/included + totals (FN-03)
**Given** 3 รายการ vat_mode ต่างกัน **When** คำนวณ **Then** badge (ไม่คิด / VAT 7% / NET 7%) ถูก · `add` → +VAT · `included` → NET (ฐานแยก) · totbox รวมเป็นเงิน/VAT/รวมทั้งสิ้นถูกต้อง (ENG-EXP-01)

### AC-03: เกินเพดานหมวด → เตือน + บังคับเหตุผล (ไม่ hard block · FN-04/BR-02)
**Given** unit_price > cat.cap **When** ขั้น3 **Then** panel เตือน "เกินเพดานหมวด {หมวด} ({เพดาน}) — เตือน แต่ยังส่งได้ · ต้องระบุเหตุผล:" + input `เหตุผลการเบิกเกินเพดาน (จำเป็น)`
**And** ไม่กรอกเหตุผล → ปุ่มส่ง disabled (title "ต้องระบุเหตุผลรายการที่เกินเพดานก่อนส่ง") · API 422 BR_OVERCAP_REASON_REQUIRED **And** กรอกครบ → ส่งได้ (ไม่ block)

### AC-04: ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ + ใบเสร็จหมวดบังคับ (FN-05/12/BR-03)
**Given** 0 รายการ หรือ grand=0 **When** ขั้น5 **Then** ปุ่ม "บันทึกและส่งอนุมัติ" disabled (title "ต้องมีรายการและยอด > 0")
**And** step-advance gate: ขั้น3 ไม่มีรายการ/ยอด=0 → กด "ถัดไป" ไม่ได้ (BUG-4) **And** หมวดบังคับใบเสร็จ (travel/lodge/ent) → step4 เตือน + submit 422 BR_RECEIPT_REQUIRED

### AC-05: ส่งอนุมัติ DOA slot picker ตามวงเงิน (FN-07/08/BR-04)
**Given** draft grand>0 **When** "ส่งอนุมัติ" → modal "ส่งอนุมัติ — เลือกผู้อนุมัติแต่ละ slot" (note "resolve ตามวงเงิน {ยอด} → ช่วง {label} (ตัวอย่าง/mock)")
**Then** slot ต่อขั้นตามช่วงวงเงิน · เลือกครบทุก slot → ปุ่ม "ส่งอนุมัติ" enabled → status='pending_approval' · toast "ส่งคำขออนุมัติแล้ว — resolve สายตามวงเงิน + แจ้งผู้อนุมัติ"
**And** เลือกไม่ครบ → ปุ่ม disabled (BR_DOA_SLOTS_INCOMPLETE) **And** สาย/slot **ไม่ hardcode** — มาจาก DOA กลาง (CL-0013 แขวน · OQ-01)

### AC-05b: แก้ยอดข้ามช่วง → re-resolve DOA (FN-11/BR-05)
**Given** ยอดเดิมช่วง A **When** แก้ยอดข้ามไปช่วง B แล้วส่งใหม่ **Then** สายอนุมัติ resolve ใหม่ตามช่วง B (resolveDoa เรียกซ้ำ · จำนวนขั้นเปลี่ยน)

### AC-06: อนุมัติครบสาย → เลข EXP + PDF + 7C (FC/EC) (FN-09/19/BR-06/07)
**Given** approver=canApprove, pending_approval **When** approve modal "อนุมัติใบเบิก?" (desc "…ออกเลข EXP-YYYY-NNNN + PDF + บันทึกเข้า 7C ตาม CSQ_BRIEF_F101…") → approve
**Then (ยังไม่ครบ)** toast "อนุมัติขั้น N แล้ว — รอขั้นถัดไป" (คง pending_approval)
**Then (ครบสาย)** status='approved' · doc_no=`EXP-2569-NNNN` (ตัวนับ global) · PDF snapshot · **emit 7C FC+EC (ไม่มี AC)** · toast "อนุมัติครบสาย · ออกเลข EXP-2569-XXXX · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · ส่งสถานะจ่าย (hook)"
**And** ผิดสิทธิ์ → toast "สิทธิ์ไม่พอ — เฉพาะผู้อนุมัติ (DOA) อนุมัติได้" · ผิดสถานะ → "อนุมัติไม่ได้ — ใบนี้ไม่ได้อยู่สถานะรออนุมัติ"

### AC-07: เลือกช่องทางจ่าย + สถานะจ่าย hook display-only (FN-10/16/BR-09)
**Given** approved **When** เลือกช่องทางจ่าย (payroll/transfer/PV/petty) **Then** ส่งจ่าย hook (payDownstream) · **ไม่จ่าย/ไม่ post** · แท็บรายละเอียด "สถานะการจ่าย" แสดง "อ่านจากปลายทาง: {payDownstream} · display-only — Expense ไม่จ่าย/ไม่ลงบัญชีเอง" · สถานะ paid อ่านจากปลายทาง

### AC-08: ตีกลับ → แก้แล้วยื่นใหม่ (FN-13/BR-18/91)
**Given** pending_approval, approver **When** "ไม่อนุมัติ" → modal "ไม่อนุมัติ (ตีกลับ)" → กรอกเหตุผล (ปุ่ม "ยืนยันตีกลับ" disabled จนกรอก) **Then** status='rejected' + reason · toast "ตีกลับ + แจ้งผู้เบิกแล้ว (แก้แล้วยื่นใหม่ได้)"
**And** ผู้เบิก "แก้ไขและยื่นใหม่" (reopen) → status='draft' · toast "เปิดแก้ไขใบเบิก — แก้แล้วส่งอนุมัติใหม่ได้" **And** reopen ใบที่ไม่ถูกตีกลับ → toast "เปิดแก้ไขไม่ได้ — ทำได้เฉพาะใบที่ถูกตีกลับ"

### AC-09: ยกเลิกก่อนอนุมัติ soft archive (FN-14/91)
**Given** draft **When** "ยกเลิก" → modal "ยกเลิกใบเบิก?" / "ใบเบิกจะถูกยกเลิก (soft archive)" → "ยกเลิกใบเบิก" **Then** status='cancelled' · toast "ยกเลิกใบเบิกแล้ว (soft archive)"
**And** ยกเลิกใบที่ไม่ใช่ฉบับร่าง → toast "ยกเลิกไม่ได้ — ทำได้เฉพาะใบฉบับร่าง" (BR_CANCEL_ONLY_DRAFT)

### AC-10: view drawer 4 tabs + PDF + ลายเซ็น (FN-15/17)
**Given** ใบเบิก **When** เปิด view **Then** tabs รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ · เอกสารแนบใน tab รายละเอียด · PDF a4 (ช่องลายเซ็น ผู้เบิก/ผู้อนุมัติ DOA/การเงิน) · tab ลายเซ็น = DOA timeline + range label · ประวัติ = audit append-only

### AC-11: หักลบเงินทดรอง display-only (FN-18/BR-11)
**Given** ผู้เบิกมีทดรองค้าง (F103 mock · เช่น E03=15,000) **When** เปิด view/step5 **Then** section "เคลียร์เงินทดรอง (F103 · soft-ref · display-only)" · "ยอดจ่ายสุทธิ = grand − offset" · ทดรองคงค้างแสดง (ถ้ามี) · note "(F101 ไม่ปรับยอดทดรองเอง · ส่งค่าหักลบให้ F103 · display-only)"
**And (EC-06)** ทดรอง > grand → net_pay=0 + ทดรองคงค้าง = adv − grand

### AC-12: visibility scope + role เจ้าหน้าที่ HR/Finance (FN-20/94/BR-12)
**Given** role=ผู้เบิก/ธุรการ (scope:self) **Then** เห็นเฉพาะใบของตน + ยอดใบคนอื่น mask `฿ •••••`
**And** role=เจ้าหน้าที่ HR/Finance (scope:all) **Then** เห็นทุกใบ + เงินเต็ม (unmask) · **ไม่มีสิทธิ์อนุมัติ DOA** (ปุ่มอนุมัติไม่ render · note "รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้")
**And** role=ผู้อนุมัติ (all) **Then** เห็นทุกใบ + เงินเต็ม + อนุมัติได้

### AC-13: list docPill + signprog + filter + empty (FN-90)
**When** list **Then** docPill 7 สถานะ + signprog (done/total) + filter (ค้นหา/สถานะ/ล้างตัวกรอง) · row over-cap = chip "เกินเพดาน"
**And** filter ไม่เจอ/ว่าง → empty "ยังไม่มีใบเบิก" + "สร้างใบเบิกใหม่ ระบบจะตรวจเพดานหมวดและ resolve สายอนุมัติตามวงเงินให้" + ปุ่ม "สร้างใบเบิก"

### AC-14: validate + กัน double-submit + wizard ล็อก (FN-92)
**When** double-click submit/approve/reject/cancel **Then** `state._busy` กัน action ซ้ำ + Idempotency-Key กัน INSERT ซ้ำ (200 cached) **And** wizard STEP_KEYS ล็อกลำดับ + step-advance gate

### AC-15: audit append-only (FN-93)
ทุก create/แก้/อนุมัติ/ตีกลับ/ยกเลิก/ส่งจ่าย → T_expense_audit_log entry · tab ประวัติ "(audit · append-only)" · **UPDATE/DELETE ถูกปฏิเสธ**

### AC-16: masking ตัวเงิน RESTRICTED (FN-94)
role mask:true → ยอด "ใบของคนอื่น" mask `฿ •••••` ทั้ง list · view · PDF/export · ใบของตน/ผู้อนุมัติ/เจ้าหน้าที่ เห็นเต็ม

### AC-17..AC-18 (Edge · Phase 2.5) — ดู §6.2 TC-CC/PR

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | สร้างใบเบิก + snapshot cc | API/E2E | AC-01 | P0 |
| TC-02 | VAT none/add/included + totals | unit/E2E | AC-02 | P0 |
| TC-03 | เกินเพดาน → เตือน+เหตุผล (ไม่ block) | negative/E2E | AC-03 | P0 |
| TC-04 | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ + ใบเสร็จบังคับ | negative | AC-04 | P0 |
| TC-05 | ส่งอนุมัติ DOA slot picker ตามวงเงิน | E2E | AC-05 | P0 |
| TC-06 | แก้ยอดข้ามช่วง → re-resolve | E2E | AC-05b | P1 |
| TC-07 | อนุมัติหลายขั้น → เลข+PDF+7C (FC/EC) | E2E | AC-06 | P0 |
| TC-08 | เลือกจ่าย hook display-only | API/E2E | AC-07 | P0 |
| TC-09 | ตีกลับ + reopen | E2E | AC-08 | P0 |
| TC-10 | ยกเลิกฉบับร่าง (guard) | API | AC-09 | P1 |
| TC-11 | view 4 tabs + PDF + ลายเซ็น | E2E | AC-10 | P1 |
| TC-12 | หักลบทดรอง display-only | API/E2E | AC-11 | P1 |
| TC-13 | scope self/all + officer ไม่อนุมัติ | E2E | AC-12 | P0 |
| TC-14 | list docPill/signprog/filter/empty | E2E | AC-13 | P1 |
| TC-CC-01 | concurrent approve (EC-01) | stress | AC-17 | P1 |
| TC-PR-01 | permission mid-flight (EC-02) | API | AC-18 | P2 |
| TC-ID-01 | idempotency double-submit (EC-03) | API | AC-14 | P0 |
| TC-DI-01 | cc=null (EC-04) | API | — | P2 |
| TC-CANCEL-EC-01 | ยกเลิกหลังอนุมัติ (EC-05/OQ-05) | integration | XT-04 | P1 |
| TC-ADV-01 | ทดรอง > ยอดใบ (EC-06) | unit | AC-11 | P2 |
| TC-MASK-01 | mask money + export (EC-07) | API/E2E | AC-12/16 | P1 |
| TC-HOOK-01 | budget/welfare display-only (EC-08) | E2E | — | P2 |

---

## §6.3 Test Data Setup
- 2 tenant (isolated) · 4 employees (ต่างศูนย์ต้นทุน: E01 ผลิต · E02 การเงิน · E03 ขาย · E04 คลัง) · 3 roles: `qa_maker` (ผู้เบิก/ธุรการ · mask · self=E01) · `qa_manager` (ผู้อนุมัติ DOA · unmask · approver) · `qa_officer` (เจ้าหน้าที่ HR/Finance · unmask · approver:false)
- 5 หมวด: เดินทาง(cap 5,000/ครั้ง·ใบเสร็จบังคับ) · ที่พัก(2,000/คืน·บังคับ) · รับรอง(3,000·บังคับ) · วัสดุ(ไม่จำกัด) · อื่นๆ
- ใบเบิก 6 สถานะ: ร่าง(d1) · อนุมัติแล้ว+เลข(d2) · รออนุมัติ 1 ขั้น(d3) · รออนุมัติ 3 ขั้น ต่างวงเงิน(d4 · 62,000) · ตีกลับ(d5) · จ่ายแล้ว(d6)
- F103 ทดรองค้าง mock: E03=15,000 · F117 งบ mock=100,000 · F102 สิทธิ์สวัสดิการ mock=5,000 (หมวด ent)
- VAT 7% · วันที่ พ.ศ. (2569)

## §6.4 Definition of Done (DoD)
### Code
- [ ] ทุก AC (01–18) implement + unit tests pass · guard (over-cap/receipt/submit/cancel/reopen) ครบ
- [ ] Integration (API+DB+Engine) · E2E happy + edge (EC-01..08)
- [ ] test coverage ≥ 80% logic layer
### Documentation
- [ ] API docs (จาก 02_API) · FRD 07_LOCKED สะท้อน final · CUBIC: ENG-EXP-01/02 registered (Phase 2)
### QA
- [ ] P0+P1 pass · ไม่มี P0/P1 bug เปิด · security (D2/D5/D7/D9/D15/D17) verified · masking (FN-94) ตรวจ export/PDF
### Deployment
- [ ] migration staging · **ไม่ผูกเพดานหมวด/สายDOA/รูปแบบเลข เป็นค่าคงที่** (OQ-01/02) · **ไม่ผูก reverse EC/FC จน BA เคาะ** (OQ-05) · monitoring DOA compliance · rollback plan

---

## §6.5 WebSocket Events (optional)
- `exp.submitted` → channel `tenant:<id>:approver:<id>`
- `exp.approved` / `exp.rejected` / `exp.paid` → channel `tenant:<id>:user:<emp_id>`
> ปกติ in-app/email ผ่าน ENG-NOTIFY — WS optional สำหรับ inbox ผู้อนุมัติ · **doa_* ไม่ประกาศเอง** (DOA engine)

---

## §6.6 Performance Benchmarks
| Endpoint | P95 | Throughput |
|---|---|---|
| GET /expenses (list · scope) | < 500ms | 200/s |
| POST /expenses | < 1000ms | 50/s |
| POST /expenses/:id/approve | < 800ms | 100/s |
| GET /expenses/:id (view + hooks) | < 800ms | 100/s |

---

## §6.7 Test Environment Notes
- staging tenant `tenant-test-001` · DOA engine (F-DLG-001) = **mock resolve ตามวงเงิน** (DOA_RANGES mock <5k/5k–50k/>50k) — **role-id/ช่วงจริงรอ OQ-01 · CL-0013 แขวน**
- ENG-NOTIFY mock (assert emit event ธุรกิจ · ไม่นับ doa_*) · ENG-DOC-NUM/STORE mock (assert เลข global unique + PDF snapshot) · F103/F117/F102 mock hook (assert display-only · ไม่ post/ไม่ปรับ ledger)

---

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-02 | FN-01, FN-15, FN-21 | ENG-EXP-01 |
| AC-02 | API-02/03 | FN-03, FN-04 | ENG-EXP-01 |
| AC-03 | API-02/05 | FN-13 | — |
| AC-04 | API-05 | FN-05, FN-06, FN-14 | — |
| AC-05/05b | API-05/12 | FN-05, FN-06 | — |
| AC-06 | API-06 | FN-07, FN-11, FN-22, FN-23 | — |
| AC-07 | API-10/11 | FN-12, FN-16 | ENG-EXP-02 |
| AC-08 | API-07/09 | FN-08, FN-10 | — |
| AC-09 | API-08 | FN-09 | — |
| AC-10 | API-03/20 | FN-23, FN-18 | ENG-EXP-01 |
| AC-11 | API-16 | FN-16 | ENG-EXP-02 |
| AC-12/16 | API-01/03 | FN-19, FN-18, FN-20 | — |
| AC-13 | API-01 | FN-19, FN-04 | — |
| AC-14 | ทุก mutation | FN-06/07/08/09 (busy) | — |
| AC-15 | ทุก mutation | FN-21 | — |

> **Coverage check:** ทุก Function (FN-01..23) + Engine (ENG-EXP-01/02) ถูก trace ≥1 AC ✅

---

## §6.9 Cross-Module Test Cases (จาก BRD §12.1)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | อนุมัติครบสาย | CSQ / 7C | emit `exp.approved` (**FC + EC** · **ไม่มี AC**) · GL ไม่กระทบ (Accounting ปลายทาง post เอง) |
| XT-02 | เลือกช่องทางจ่าย (approved) | Payroll/Finance/F091/F109 | รับ hook display-only · **ไม่ auto-post/ไม่ auto-จ่าย** · status paid อ่านกลับ |
| XT-03 | หักลบเงินทดรอง | F103 (Advance) | อ่านทดรองค้าง · ส่งค่าหักลบ display-only · **F101 ไม่ปรับ ledger F103** |
| XT-04 | ยกเลิก/แก้หลังอนุมัติ (EC-05) | CSQ/Finance | **ไม่มี path ในระบบปัจจุบัน** (cancel เฉพาะ draft · reopen เฉพาะ rejected) → ถ้าเปิด = ต้อง reverse EC/release FC → **OQ-05** (ยืนยัน policy) |
| XT-05 | ตรวจงบ/สิทธิ์สวัสดิการ | F117 (งบ) / F102 (Welfare) | display-only mock · เตือนเฉย ไม่ block · **ไม่มีตัวเลข hardcode** (OQ-EXP-04) |

---

## §6.10 Microcopy-Aware Expected Text
> ยึด **ข้อความจริงบนจอ (verbatim)** จาก expense.html ก่อน fallback microcopy กลาง v9
- toast: "ส่งคำขออนุมัติแล้ว — resolve สายตามวงเงิน + แจ้งผู้อนุมัติ" · "อนุมัติขั้น {N} แล้ว — รอขั้นถัดไป" · "อนุมัติครบสาย · ออกเลข {code} · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · ส่งสถานะจ่าย (hook)" · "ตีกลับ + แจ้งผู้เบิกแล้ว (แก้แล้วยื่นใหม่ได้)" · "ยกเลิกใบเบิกแล้ว (soft archive)" · "เปิดแก้ไขใบเบิก — แก้แล้วส่งอนุมัติใหม่ได้"
- toast (guard/warn): "สิทธิ์ไม่พอ — เฉพาะผู้อนุมัติ (DOA) อนุมัติได้" · "อนุมัติไม่ได้ — ใบนี้ไม่ได้อยู่สถานะรออนุมัติ" · "ยกเลิกไม่ได้ — ทำได้เฉพาะใบฉบับร่าง" · "เปิดแก้ไขไม่ได้ — ทำได้เฉพาะใบที่ถูกตีกลับ" · "สิทธิ์ไม่พอ — เฉพาะผู้อนุมัติ (DOA) ตีกลับได้"
- ปุ่ม: "สร้างใบเบิก" · "บันทึกและส่งอนุมัติ" · "ถัดไป" / "ย้อนกลับ" · "ส่งอนุมัติ" · "อนุมัติ" / "ไม่อนุมัติ" · "ยืนยันตีกลับ" · "ยกเลิกใบเบิก" · "แก้ไขและยื่นใหม่" · "เพิ่มรายการ" · "ล้างตัวกรอง"
- modal: "ส่งอนุมัติ — เลือกผู้อนุมัติแต่ละ slot" · "อนุมัติใบเบิก?" · "ไม่อนุมัติ (ตีกลับ)" · "ยกเลิกใบเบิก?"
- placeholder: "ค้นหาเลขที่ / ชื่อผู้เบิก…" · "เหตุผลการเบิกเกินเพดาน (จำเป็น)" · "เหตุผลการตีกลับ (จำเป็น)" · "เลือกผู้อนุมัติ…"
- empty: "ยังไม่มีใบเบิก" · "ยังไม่มีรายการ — กด "เพิ่มรายการ""
- title disabled: "ต้องมีรายการและยอด > 0" · "ต้องระบุเหตุผลรายการที่เกินเพดานก่อนส่ง"
