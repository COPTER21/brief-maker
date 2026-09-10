# AI Test Cases — Expense Claim / เบิกค่าใช้จ่าย (F-HR-EXPENSE · F101)

เอกสารนี้เป็น **Test Case สำหรับ AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบน HTML prototype `expense.html` จริง แล้วรายงานผลกลับ. ทุก action ผูกกับ **ข้อความ/ป้ายที่เห็นบนจอ (verbatim)** จาก HTML ต้นทาง + route จริง. Expected เช็คได้ด้วยตา.

> **ที่มา anchor:** expense.html (source of truth · verbatim) > FRD 01_UI > microcopy กลาง html-generator-v9.
> **Prototype demo model:** สลับบทบาทที่แถบ **"มุมมองสาธิต"** (บนสุดของหน้า) — ปุ่ม `ผู้เบิก/ธุรการ` (=admin · mask · self=E01 · ไม่อนุมัติ) · `ผู้อนุมัติ (DOA)` (=mgr · unmask · approver) · `เจ้าหน้าที่ (HR/Finance)` (=officer · unmask · scope:all · **ไม่อนุมัติ**). ข้อมูลเป็น seed ในเครื่อง (DB คงที่ · refresh คืนค่าเริ่มต้น).
> **หมายเหตุ QA column (WF-01 step 9):** คอลัมน์ `QA` ของ FUNCTION_CHECKLIST เป็นผลติ๊ก localStorage runtime — tester ติ๊กตอนรัน browser (แก้ไฟล์ไม่ได้). **Coverage Ledger FN↔TC ด้านล่างคือหลักฐาน "ติ๊ก QA" (ครบทุก FN มี TC).**
> **Scope note:** FUNCTION_CHECKLIST.html มี 22 FN (FN-01..17 + FN-90..94) · **FN-18/19/20 = 3 PM/BA additions (2026-09-10)** เพิ่มหลัง checklist → อยู่ใน FRD §0.12 Coverage Manifest (25 FN) · Ledger นี้ยึด **25 FN**.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-HR-EXPENSE (F101) |
| ชื่อ | Expense Claim / เบิกค่าใช้จ่าย (ใบเบิกค่าใช้จ่ายพนักงาน) |
| เวอร์ชัน | TC v1.0 (2026-09-10) · จาก FRD 1.0 (FULL · Q-document) |
| App entry | เปิด `expense.html` → sidebar "เบิกค่าใช้จ่าย" → หน้ารายการใบเบิก (list · default `state.tab='list'`) |
| Routes | `#/expense` (list default) · overlay = drawer (wizard สร้าง / view 4 tabs) + modal (submit/approve/reject/cancel) — **ไม่มี route แยกต่อ overlay** · ปิดด้วย Esc / backdrop / ปุ่มปิด |
| ที่มา | FRD_F-HR-EXPENSE_Pack (00/01/02/03/04/05/06/07) · BRD_เบิกค่าใช้จ่าย.md · expense.html · FUNCTION_CHECKLIST (22 FN + 3 add) |
| จำนวนเคส | **76 เคส** / 13 group |
| Persona seed (มุมมองสาธิต) | `ผู้เบิก/ธุรการ` (admin · mask:true · self=E01 · approver:false · scope:self) · `ผู้อนุมัติ (DOA)` (mgr · unmask · approver:true · scope:all) · `เจ้าหน้าที่ (HR/Finance)` (officer · unmask · approver:false · scope:all) · **default = ผู้เบิก/ธุรการ** |
| Seed employees | E01 สมชาย ใจดี (ผลิต · CC-PROD-01) · E02 อรทัย แสนสุข (การเงิน · CC-FIN-01) · E03 ธนากร พูนผล (ขาย · CC-SALES-01) · E04 มะลิ ดอกไม้ (คลัง · CC-WH-01) |
| Seed หมวด (cap · ใบเสร็จบังคับ) | เดินทาง(cap 5,000/ครั้ง · **บังคับ**) · ที่พัก(2,000/คืน · **บังคับ**) · รับรอง(3,000 · **บังคับ**) · วัสดุสำนักงาน(ไม่จำกัด) · อื่นๆ(ไม่จำกัด) |
| Seed docs (6 สถานะ) | d1 `(ร่าง)` E01 · d2 `EXP-2569-0001` approved E01 · d3 `(รออนุมัติ)` E02 1 ขั้น · d4 `(รออนุมัติ)` E03 **3 ขั้น 66,340 (over-cap)** · d5 `(ตีกลับ)` E04 · d6 `EXP-2569-0002` paid E02 |
| DOA ranges (mock) | <5,000 = 1 ขั้น (หัวหน้าสายงาน) · 5,000–50,000 = 2 ขั้น (+ผู้จัดการแผนก) · >50,000 = 3 ขั้น (+ผู้อำนวยการ) · **ห้าม hardcode ในระบบจริง (OQ-01 · CL-0013 แขวน)** |
| Approver pool (slot picker) | A1 สมพงษ์ อินทร์ · A2 วิไล ประสงค์ · A3 อนันต์ ทวี · A4 ปรีชา วัฒน์ · A5 ก้อง มีชัย |
| ทดรอง F103 (mock) | E03 = 15,000 (soft-ref · display-only) |
| งบ/สวัสดิการ mock | F117 งบคงเหลือ = 100,000 · F102 สิทธิ์สวัสดิการ (หมวด รับรอง/ent) = 5,000 |

---

## Coverage

| group | เคส | ความสำคัญ |
|---|---|---|
| G1 สร้างใบเบิก wizard 5 ขั้น (FN-01/02/06) | 3 | สูง |
| G2 line editor + VAT + over-cap + ใบเสร็จ (FN-03/04/05/12) | 13 | สูง |
| G3 ส่งอนุมัติ DOA slot picker + re-resolve (FN-07/08/11) | 6 | สูง |
| G4 อนุมัติ → เลข+PDF+7C(FC/EC) + จ่าย hook (FN-09/10/16/19) | 6 | สูง |
| G5 ตีกลับ / reopen / ยกเลิก (FN-13/14/91) | 5 | สูง |
| G6 view drawer 4 tabs + PDF a4 + ลายเซ็น (FN-15/17) | 4 | กลาง |
| G7 touchpoint: PV/petty + หักลบทดรอง F103 (FN-18) | 4 | สูง |
| G8 visibility scope + role เจ้าหน้าที่ ไม่อนุมัติ (FN-20/94) | 5 | สูง |
| G9 กติกากลาง (FN-90/91/92/93) | 8 | กลาง |
| G10 Negatives — "ห้ามมี" (unsupported 7 + FN-40 style) | 9 | สูง |
| G11 Permission matrix (3 role × action) | 3 | สูง |
| G12 Edge cases (EC-01..08) | 7 | กลาง |
| G13 Cross-module (XT-01..05) | 3 | กลาง |

---

## Coverage Ledger

> ★ FN cross-check (FRD §0.12 Coverage Manifest · 25 FN): ทุก FN มี TC ≥1 = **หลักฐานติ๊กคอลัมน์ QA** · unsupported 7 มีเคสเชิงลบ (verify absent) · LOCK 10/10 มีเคส verify · XT 5/5.

### FN — Coverage Manifest (25/25) — QA column evidence
| FN | AC / BR | Requirement (ย่อ) | TC ids |
|---|---|---|---|
| FN-01 | AC-01 · BR-14 | wizard 5 ขั้น | TC-W01, TC-W02, TC-WL01 |
| FN-02 | AC-01 | หัวเอกสาร: ผู้เบิก/วันที่/ช่องทางจ่าย | TC-W01, TC-W03 |
| FN-03 | AC-02 · BR-01 | line editor + VAT none/add/included + totals | TC-L01, TC-L02, TC-L03, TC-L04, TC-L05 |
| FN-04 | AC-03 · BR-02 | เกินเพดาน → เตือน + บังคับเหตุผล (ไม่ block) | TC-OC01, TC-OC02, TC-OC03, TC-OC04 |
| FN-05 | AC-04 · BR-03 | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ | TC-V01, TC-V02, TC-WL01 |
| FN-06 | AC-01 · BR-08 | ตำแหน่ง/cc snapshot Movement ณ วันเบิก | TC-W03, TC-DI01 |
| FN-07 | AC-05 · BR-04 | ส่งอนุมัติจาก wizard/ใบเบิก | TC-S01, TC-S02 |
| FN-08 | AC-05 · BR-04 | DOA slot picker ตามวงเงิน (ไม่ hardcode) | TC-S01, TC-S03, TC-S04, TC-S05 |
| FN-09 | AC-06 · BR-06/07 | อนุมัติครบสาย → เลข EXP + PDF + 7C | TC-AP01, TC-AP02, TC-AP03 |
| FN-10 | AC-07 · BR-09 | เลือกช่องทางจ่าย → ส่งจ่าย (hook) | TC-PAY01, TC-TP01 |
| FN-11 | AC-05b · BR-05 | แก้ยอดข้ามช่วง → re-resolve DOA | TC-RR01 |
| FN-12 | AC-04 · BR-03 | แนบใบเสร็จตามนโยบายหมวด | TC-RC01, TC-RC02 |
| FN-13 | AC-08 · BR-18 | ตีกลับ → แก้แล้วยื่นใหม่ (reopen) | TC-RJ01, TC-RJ02, TC-RJ03 |
| FN-14 | AC-09 · BR-10 | ยกเลิกก่อนอนุมัติ (soft archive) | TC-CX01, TC-CX02 |
| FN-15 | AC-10 · BR-06 | PDF tab a4 + tab ลายเซ็น | TC-VW03, TC-VW04 |
| FN-16 | AC-07 · BR-09 | "จ่ายแล้ว" อ่านจากปลายทาง display-only | TC-PAY02 |
| FN-17 | AC-10 | view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + แนบ | TC-VW01, TC-VW02 |
| **FN-18** | AC-11 · BR-11 | touchpoint PV/petty (F091) + หักลบทดรอง (F103 display-only) | TC-TP01, TC-TP02, TC-TP03, TC-ADV01 |
| **FN-19** | AC-06 · BR-07 | 7C = FC/EC เท่านั้น (ไม่มี AC) | TC-AP03, TC-XT01, TC-N06 |
| **FN-20** | AC-12 · BR-12 | scope self/all + role เจ้าหน้าที่ HR/Finance ไม่อนุมัติ | TC-P01, TC-P02, TC-P04, TC-P05 |
| FN-90 | AC-13 | list docPill + signprog + filter + empty | TC-G01, TC-G02, TC-G03 |
| FN-91 | AC-08/09 | ตีกลับ/ยกเลิก confirm + soft archive | TC-RJ01, TC-CX01, TC-G04 |
| FN-92 | AC-14 | validate + กัน double-submit + wizard ล็อก | TC-V01, TC-WL01, TC-ID01 |
| FN-93 | AC-15 | audit append-only | TC-AU01, TC-AU02 |
| FN-94 | AC-16 | masking ตัวเงิน RESTRICTED ตาม role | TC-P02, TC-P03, TC-MASK01 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 line amount>0 + cat HR Config + VAT | TC-L01, TC-L05 |
| BR-02 (LOCK-05/08) เพดานหมวด warn+reason (ไม่ block) | TC-OC01, TC-OC02, TC-OC03 |
| BR-03 ≥1 line + ยอด>0 + ใบเสร็จหมวดบังคับ | TC-V01, TC-V02, TC-RC01 |
| BR-04 (LOCK-01) DOA resolve ตามยอด · slot ครบ | TC-S01, TC-S04, TC-S05 |
| BR-05 (FN-11) แก้ยอดข้ามช่วง re-resolve | TC-RR01 |
| BR-06 (LOCK-02) เลข EXP + PDF = ENG-DOC ตอนอนุมัติ (immutable) | TC-AP03 |
| BR-07 (LOCK-04) 7C = FC+EC (ไม่มี AC) | TC-AP03, TC-XT01, TC-N06 |
| BR-08 (LOCK-06) cc snapshot Movement ณ วันเบิก (null≠ไม่มี) | TC-W03, TC-DI01 |
| BR-09 (LOCK-03) จ่าย/post = hook display-only | TC-PAY01, TC-PAY02, TC-N01 |
| BR-10 (LOCK-07) audit append-only + mask + soft archive | TC-AU01, TC-CX01, TC-MASK01 |
| BR-11 (FN-18 · LOCK-09) หักลบทดรอง soft-ref F103 display-only | TC-TP03, TC-ADV01 |
| BR-12 (FN-20 · LOCK-10) scope self/all + officer ไม่อนุมัติ | TC-P01, TC-P04, TC-P05 |
| BR-13 (SoD) approve/reject เฉพาะ approver · กัน self-approve | TC-P03, TC-P04, TC-EC02 |
| BR-14 (FN-92) wizard ล็อกลำดับ + step-advance gate + กัน double-submit | TC-WL01, TC-ID01 |
| BR-15 (OQ-EXP-04) งบ F117 + สวัสดิการ F102 = hook warn display-only | TC-HK01, TC-HK02 |
| BR-18 (reject reason) ไม่อนุมัติต้องระบุเหตุผล | TC-RJ01 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 concurrent approval (409 ERR_STALE_DATA) | TC-EC01 (ต้อง simulate) |
| EC-02 permission mid-flight (403 ERR_NOT_APPROVER/REVOKED) | TC-EC02 |
| EC-03 double-submit idempotency (state._busy) | TC-ID01 |
| EC-04 cc=null (Movement ไม่มี assignment) | TC-DI01 (ต้อง simulate seed) |
| EC-05 cancel/แก้ หลังอนุมัติ → **ไม่มี path** (OQ-05) | TC-EC05 (verify absent) |
| EC-06 ทดรอง > ยอดใบ → net_pay=0 + ทดรองคงค้าง | TC-ADV01 |
| EC-07 mask export/PDF ตาม scope | TC-MASK01 |
| EC-08 ยอด>งบ (F117)/เกินสิทธิ์สวัสดิการ (F102) → warn display-only | TC-HK01, TC-HK02 |

### Error Catalog (05_RULES §5.6) → เคสที่แสดงผลบนจอ
| error | cases |
|---|---|
| BR_LINE_AMOUNT_REQUIRED (422) | TC-L05 |
| BR_SUBMIT_NO_LINES (422) | TC-V01, TC-V02 |
| BR_OVERCAP_REASON_REQUIRED (422) | TC-OC02, TC-OC03 |
| BR_RECEIPT_REQUIRED (422) | TC-RC01 |
| BR_DOA_SLOTS_INCOMPLETE (422) | TC-S05 |
| BR_CANCEL_ONLY_DRAFT (422) | TC-CX02 |
| BR_REOPEN_ONLY_REJECTED (422) | TC-RJ03 |
| BR_NOT_PENDING_APPROVAL (422) | TC-AP04 |
| ERR_NOT_APPROVER (403) | TC-P03, TC-P04 |
| ERR_REASON_REQUIRED (400) | TC-RJ01 |
| ERR_STALE_DATA (409) | TC-EC01 (simulate) |
| ERR_PERMISSION_REVOKED (403) | TC-EC02 (simulate) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY (409) | TC-ID01 |
| ERR_VALIDATION_FAILED (400) | TC-V01, TC-L05 |

### Permission Matrix (05_RULES §5.3 · role × action)
| cell | cases |
|---|---|
| ผู้เบิก/ธุรการ view = self only | TC-P01 |
| ผู้เบิก/ธุรการ ยอดใบคนอื่น = mask `฿ •••••` | TC-P02 (deny-view-money) |
| ผู้เบิก/ธุรการ create/submit = allow | TC-W01, TC-S01 |
| ผู้เบิก/ธุรการ approve = **deny** (ไม่มีปุ่ม) | TC-P03 |
| ผู้อนุมัติ (DOA) approve/reject = allow | TC-AP01, TC-RJ01 |
| ผู้อนุมัติ (DOA) view all + unmask | TC-P02 |
| เจ้าหน้าที่ (HR/Finance) view all + unmask | TC-P05 |
| เจ้าหน้าที่ (HR/Finance) approve = **deny** (ไม่ render ปุ่ม + note) | TC-P04 |
| เลือกช่องทางจ่าย (hook) = allow (ผู้เบิก/เจ้าหน้าที่) | TC-PAY01 |

### Scope Lock (07_LOCKED §7.0 · LOCK 10/10)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | DOA threshold ตามวงเงิน · ไม่ hardcode 3-tier | TC-S01, TC-S03, TC-RR01 |
| LOCK-02 | เลข EXP + PDF = ENG-DOC ออกตอนอนุมัติ immutable | TC-AP03 |
| LOCK-03 | จ่าย/post = hook display-only | TC-PAY01, TC-PAY02, TC-N01 |
| LOCK-04 | 7C = FC/EC เท่านั้น (ไม่มี AC) | TC-AP03, TC-XT01, TC-N06 |
| LOCK-05 | เพดานหมวด = อ่าน HR Config #107 (ไม่ CRUD) | TC-N08 |
| LOCK-06 | ตำแหน่ง/cc = snapshot Movement ณ วันเบิก | TC-W03, TC-DI01 |
| LOCK-07 | audit append-only + RESTRICTED mask + soft archive | TC-AU01, TC-MASK01, TC-CX01 |
| LOCK-08 | over-cap = warn + บังคับเหตุผล (ไม่ hard block) | TC-OC01, TC-OC02 |
| LOCK-09 | touchpoint PV/petty (F091) + หักลบทดรอง (F103) display-only | TC-TP01, TC-TP03 |
| LOCK-10 | scope self/all · เจ้าหน้าที่ = all+unmask+ไม่อนุมัติ | TC-P01, TC-P04, TC-P05 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 | CSQ / 7C (FC+EC · ไม่มี AC) | TC-XT01 |
| XT-02 | Payroll/Finance/F091/F109 (จ่าย hook display-only) | TC-PAY01, TC-PAY02 |
| XT-03 | F103 Advance (หักลบ display-only) | TC-TP03, TC-ADV01 |
| XT-04 | ยกเลิก/แก้หลังอนุมัติ = ไม่มี path (OQ-05) | TC-EC05 |
| XT-05 | F117 Budget / F102 Welfare (warn display-only) | TC-HK01, TC-HK02 |

### Cross-cutting / Events / States
| item | cases |
|---|---|
| empty state (list ว่าง/filter ไม่เจอ) | TC-G03 |
| docPill 7 สถานะ + signprog (done/total) | TC-G01 |
| event exp.submitted / approved / rejected / paid / overcap (NTF) | TC-S01, TC-AP03, TC-RJ01, TC-OC04 (สังเกต toast · doa_* ไม่ประกาศเอง) |
| state machine transition ถูก (draft→pending→approved / →rejected→draft / →cancelled) | TC-S01, TC-AP03, TC-RJ01/RJ02, TC-CX01 |
| state machine transition ต้องห้าม (cancel non-draft · reopen non-rejected · approve non-pending) | TC-CX02, TC-RJ03, TC-AP04 |

---

## Data Sets

### ชุดข้อมูลใบเบิก (กรอกในผู้เบิก/ธุรการ)
| ชุด | ผู้เบิก | วันที่ | ช่องทางจ่าย | รายการ |
|---|---|---|---|---|
| **A** (2 ขั้น · in-cap) | สมชาย ใจดี (E01) | 2569-08-31 | ผ่านรอบเงินเดือน | 1: เดินทาง · "ค่าแท็กซี่" · 4,500 · VAT 7% (add) |
| **B** (over-cap · ต้องเหตุผล) | สมชาย ใจดี | 2569-08-31 | โอนตรง | 1: เดินทาง · "เหมารถตู้ต่างจังหวัด" · 8,000 · VAT 7% (add) → เกินเพดาน 5,000 |
| **C** (VAT 3 โหมด) | สมชาย ใจดี | 2569-08-31 | ผ่านรอบเงินเดือน | L1 วัสดุ · "กระดาษ" · 1,000 · **ไม่คิด** · L2 วัสดุ · "หมึก" · 1,000 · **VAT 7%** · L3 วัสดุ · "ปากกา" · 1,070 · **รวมแล้ว NET 7%** |
| **D** (>50k · 3 ขั้น) | สมชาย ใจดี | 2569-08-31 | โอนตรง | 1: อื่นๆ · "เหมางานอีเวนต์" · 60,000 · ไม่คิด |
| **E** (ใบเสร็จบังคับ) | สมชาย ใจดี | 2569-08-31 | โอนตรง | 1: ที่พัก · "โรงแรม 1 คืน" · 1,800 · VAT 7% (add) → หมวดบังคับใบเสร็จ |
| **F** (ยอด 0 · negative) | สมชาย ใจดี | 2569-08-31 | ผ่านรอบเงินเดือน | 1: วัสดุ · "ของแถม" · **0** |
| **G** (amount ≤ 0 · negative line) | สมชาย ใจดี | 2569-08-31 | ผ่านรอบเงินเดือน | 1: วัสดุ · "ทดสอบ" · **-50** |
| **H** (หมวดสวัสดิการเกินสิทธิ์) | สมชาย ใจดี | 2569-08-31 | โอนตรง | 1: รับรอง · "เลี้ยงรับรอง" · 6,000 · VAT 7% → เกินสิทธิ์ F102 (5,000) + เกินเพดาน 3,000 |

### ค่าเหตุผล (over-cap / reject)
| ชื่อ | ค่า |
|---|---|
| over_reason | `ลูกค้าต่างจังหวัด ต้องเหมารถ ไม่มีขนส่งสาธารณะ` |
| reject_reason | `แนบใบเสร็จไม่ครบ กรุณาแนบเพิ่ม` |

### ไฟล์ทดสอบ (Files)
| ชื่อไฟล์ | ใช้ที่ | หมายเหตุ |
|---|---|---|
| `receipt_hotel.pdf` | TC-RC02 (step4 upload-zone) | ใบเสร็จ PDF ตัวอย่าง (หมวดที่พัก) — runner เตรียมไฟล์ · prototype upload = mock UI |

> **หมายเหตุ prototype:** ทุกใบเบิกใหม่จะขึ้นบนสุดของ list เป็นสถานะ `(รออนุมัติ)` (submit สร้าง pending ทันที · ไม่มี draft-save แยกใน wizard) · refresh หน้าคืน seed เดิม (ล้างใบที่สร้างระหว่างเทส).

---

## Test Cases

### G1 — สร้างใบเบิก wizard 5 ขั้น (FN-01/02/06)

#### TC-W01 — สร้างใบเบิกครบ 5 ขั้น + ส่งอนุมัติ (happy · in-cap 2 ขั้น)
- group: G1 · ความสำคัญ: สูง · trace: FN-01/02/06/07 · AC-01/05 · event exp.submitted
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ (default) · seed=— · files=—
- Start: OPEN `expense.html` → หน้ารายการใบเบิก
- ชุดข้อมูล: A
- ผ่านเมื่อ: เดินครบ 5 ขั้น → เปิด modal ส่งอนุมัติ → ส่งได้ → toast "ส่งคำขออนุมัติแล้ว — …" + ใบใหม่ขึ้น list สถานะ **รออนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ "มุมมองสาธิต" ด้านบน | — | ปุ่มบทบาท active = **ผู้เบิก/ธุรการ** | ☐ |
| 2 | CLICK ปุ่ม **สร้างใบเบิก** | — | drawer เปิด · stepper 5 ขั้น · ขั้น 1 = **เลือกแหล่งที่มา** | ☐ |
| 3 | VERIFY ขั้น 1 radio | — | "สร้างใหม่ (สำรองจ่ายเอง)" ถูกเลือก · "จากใบขออนุมัติเดินทาง" **disabled** | ☐ |
| 4 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น 2 **ข้อมูลหลัก** | ☐ |
| 5 | SELECT ผู้เบิก → ช่อง **ผู้เบิก** (combobox) | A: สมชาย ใจดี | เลือกได้ + แสดง hookbox ตำแหน่ง/แผนก/ศูนย์ต้นทุน (ดึงจากตำแหน่ง ณ วันเบิก · Movement) | ☐ |
| 6 | VERIFY ช่อง วันที่ + ช่องทางจ่าย | A | วันที่ (พ.ศ.) = 2569-08-31 · ช่องทางจ่าย = ผ่านรอบเงินเดือน | ☐ |
| 7 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น 3 **รายการค่าใช้จ่าย** | ☐ |
| 8 | CLICK ปุ่ม **เพิ่มรายการ** → กรอกบรรทัด | A: เดินทาง · ค่าแท็กซี่ · 4,500 · VAT 7% | แถวรายการปรากฏ · totbox รวมทั้งสิ้น > 0 | ☐ |
| 9 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น 4 **เอกสารแนบ** (ไม่มีหมวดบังคับ → ผ่านได้) | ☐ |
| 10 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น 5 **ตรวจสอบและยืนยัน** · เห็นสรุป ผู้เบิก/วันที่/ยอดรวม + สายอนุมัติ (ช่วง 5,000–50,000 · 2 ขั้น) | ☐ |
| 11 | CLICK ปุ่ม **บันทึกและส่งอนุมัติ** | — | เปิด modal **ส่งอนุมัติ — เลือกผู้อนุมัติแต่ละ slot** | ☐ |
| 12 | SELECT ผู้อนุมัติครบทุก slot | A1 สมพงษ์, A2 วิไล | ปุ่ม **ส่งอนุมัติ** เปลี่ยนเป็น enabled | ☐ |
| 13 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal+drawer ปิด · toast **ส่งคำขออนุมัติแล้ว — resolve สายตามวงเงิน + แจ้งผู้อนุมัติ** | ☐ |
| 14 | VERIFY แถวบนสุดของ list | — | ใบใหม่ ผู้เบิก สมชาย ใจดี · pill **รออนุมัติ** | ☐ |

#### TC-W02 — stepper แสดง 5 ขั้นชื่อถูกต้อง + ปุ่มย้อนกลับคงค่า
- group: G1 · ความสำคัญ: กลาง · trace: FN-01 · AC-01
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html`
- ชุดข้อมูล: A
- ผ่านเมื่อ: 5 ขั้นชื่อ = เลือกแหล่งที่มา › ข้อมูลหลัก › รายการค่าใช้จ่าย › เอกสารแนบ › ตรวจสอบและยืนยัน + back คงค่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบเบิก** | — | stepper 5 ขั้น ชื่อครบตามลำดับ | ☐ |
| 2 | CLICK **ถัดไป** → เลือกผู้เบิก → **ถัดไป** | A | อยู่ขั้น 3 | ☐ |
| 3 | CLICK ปุ่ม **ย้อนกลับ** | — | กลับขั้น 2 · ผู้เบิกที่เลือกไว้ยังอยู่ (คงค่า) | ☐ |
| 4 | PRESS Esc | — | drawer ปิด (ไม่มีการบันทึก) | ☐ |

#### TC-W03 — snapshot ตำแหน่ง/ศูนย์ต้นทุน ณ วันเบิก (FN-06 · Movement)
- group: G1 · ความสำคัญ: สูง · trace: FN-06 · BR-08 · LOCK-06 · AC-01
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=E03 มีตำแหน่ง ผู้จัดการขาย/CC-SALES-01 · files=—
- Start: OPEN `expense.html` → CLICK **สร้างใบเบิก** → ขั้น 2
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือกผู้เบิกต่างคน → hookbox ตำแหน่ง/ศูนย์ต้นทุนเปลี่ยนตามคน (ดึง ณ วันเบิก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ผู้เบิก | ธนากร พูนผล (E03) | hookbox แสดง ผู้จัดการขาย · ขาย · CC-SALES-01 + ข้อความ "ดึงจากตำแหน่ง ณ วันเบิก · Movement" | ☐ |
| 2 | SELECT ผู้เบิก เปลี่ยนเป็น | สมชาย ใจดี (E01) | hookbox เปลี่ยนเป็น วิศวกร · ผลิต · CC-PROD-01 | ☐ |
| 3 | VERIFY note snapshot | — | ระบุที่มา Movement ณ วันเบิก (soft ref) | ☐ |

### G2 — line editor + VAT + over-cap + ใบเสร็จ (FN-03/04/05/12)

#### TC-L01 — VAT "ไม่คิด" (none) — ยอดไม่บวก VAT
- group: G2 · ความสำคัญ: สูง · trace: FN-03 · BR-01 · AC-02
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → CLICK **สร้างใบเบิก** → เดินถึงขั้น 3 (เลือกผู้เบิกก่อน)
- ชุดข้อมูล: C (L1)
- ผ่านเมื่อ: badge = **ไม่คิด** · รวมบรรทัด = 1,000 (ไม่มี VAT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → กรอก | C L1: วัสดุ · กระดาษ · 1,000 · VAT segmented = **ไม่คิด** | badge บรรทัด = **ไม่คิด** · รวม = 1,000 | ☐ |
| 2 | VERIFY totbox | — | รวมเป็นเงิน 1,000 · VAT 0 · รวมทั้งสิ้น 1,000 | ☐ |

#### TC-L02 — VAT "VAT 7%" (add) — บวก VAT บนยอด
- group: G2 · ความสำคัญ: สูง · trace: FN-03 · BR-01 · AC-02
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: (ต่อจากขั้น 3 · หรือใบใหม่)
- ชุดข้อมูล: C (L2)
- ผ่านเมื่อ: badge = **VAT 7%** · รวมบรรทัด = 1,070

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → กรอก | C L2: วัสดุ · หมึก · 1,000 · VAT = **VAT 7%** | badge = **VAT 7%** · รวม = 1,070 | ☐ |
| 2 | VERIFY totbox VAT | — | VAT = 70 · รวมทั้งสิ้นรวม VAT | ☐ |

#### TC-L03 — VAT "รวมแล้ว NET 7%" (included) — แยกฐาน
- group: G2 · ความสำคัญ: สูง · trace: FN-03 · BR-01 · AC-02
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: (ขั้น 3)
- ชุดข้อมูล: C (L3)
- ผ่านเมื่อ: badge = **NET 7%** · รวมบรรทัด = 1,070 (VAT ถอดจากฐาน · ไม่บวกเพิ่ม)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → กรอก | C L3: วัสดุ · ปากกา · 1,070 · VAT = **รวมแล้ว NET 7%** | badge = **NET 7%** · รวม = 1,070 (ไม่บวก VAT ซ้ำ) | ☐ |
| 2 | VERIFY totbox | — | VAT ส่วนนี้ถอดจาก 1,070 (≈70) · รวมทั้งสิ้นไม่เกินผลบวกรายการ | ☐ |

#### TC-L04 — 3 รายการ 3 VAT mode รวม totals ถูกต้อง
- group: G2 · ความสำคัญ: สูง · trace: FN-03 · AC-02 · ENG-EXP-01
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (ผู้เบิก A)
- ชุดข้อมูล: C (L1+L2+L3)
- ผ่านเมื่อ: totbox รวม 3 บรรทัดครบ (รวมเป็นเงิน + VAT + รวมทั้งสิ้น) สอดคล้อง badge แต่ละบรรทัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เพิ่ม 3 รายการ | C L1(none) + L2(add) + L3(included) | 3 แถว badge = ไม่คิด / VAT 7% / NET 7% | ☐ |
| 2 | VERIFY+จด totbox | — | จดค่า รวมเป็นเงิน/VAT/รวมทั้งสิ้น (อ้างใน step ถัดไป) | ☐ |
| 3 | CLICK ไอคอนลบ ท้ายแถวที่ 2 (VAT 7%) | — | เหลือ 2 แถว · totbox ลดลง = ยอดบรรทัด VAT 7% ที่จดไว้ (1,070 + VAT 70) | ☐ |

#### TC-L05 — จำนวนเงิน ≤ 0 → ส่ง/ถัดไปไม่ได้ (negative · BR_LINE_AMOUNT_REQUIRED)
- group: G2 · ความสำคัญ: สูง · trace: FN-03 · BR-01 · error BR_LINE_AMOUNT_REQUIRED/ERR_VALIDATION_FAILED
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (ผู้เบิก A)
- ชุดข้อมูล: G
- ผ่านเมื่อ: ยอดรวม ≤ 0 → กด "ถัดไป" ขั้น 3 ไม่ได้ (gate) — ไม่นับเป็นยอดที่ส่งได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → กรอกจำนวนเงิน | G: -50 | ยอดรวม (grand) = 0 (Math.max) · รายการไม่ทำให้ยอด>0 | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | กดไม่ได้ (disabled · gate ต้องมียอด>0) — อยู่ขั้น 3 | ☐ |

#### TC-OC01 — เกินเพดานหมวด → panel เตือน + input เหตุผล (FN-04 · warn ไม่ block)
- group: G2 · ความสำคัญ: สูง · trace: FN-04 · BR-02 · LOCK-08 · AC-03
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (ผู้เบิก A)
- ชุดข้อมูล: B
- ผ่านเมื่อ: unit_price>cap → panel เตือน "เกินเพดานหมวด …" + input "เหตุผลการเบิกเกินเพดาน (จำเป็น)" ปรากฏ · **แถวไม่ถูกลบ (ยังส่งได้)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → กรอก | B: เดินทาง · เหมารถตู้ · 8,000 · VAT 7% | panel เตือน **เกินเพดานหมวด เดินทาง (5,000) — เตือน แต่ยังส่งได้ · ต้องระบุเหตุผล:** | ☐ |
| 2 | VERIFY input เหตุผล | — | มีช่อง **เหตุผลการเบิกเกินเพดาน (จำเป็น)** | ☐ |
| 3 | VERIFY แถวรายการ | — | แถวยังอยู่ (ไม่ถูก hard block) · totbox รวม 8,000+VAT | ☐ |

#### TC-OC02 — เกินเพดานไม่กรอกเหตุผล → ปุ่มส่งอนุมัติ disabled + title (BR_OVERCAP_REASON_REQUIRED)
- group: G2 · ความสำคัญ: สูง · trace: FN-04 · BR-02 · AC-03 · error BR_OVERCAP_REASON_REQUIRED
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ถึงขั้น 5 (ใบ over-cap ยังไม่กรอกเหตุผล)
- ชุดข้อมูล: B
- ผ่านเมื่อ: เหตุผลว่าง → ปุ่ม "บันทึกและส่งอนุมัติ" disabled + title "ต้องระบุเหตุผลรายการที่เกินเพดานก่อนส่ง"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบ over-cap ถึงขั้น 5 | B (ไม่กรอกเหตุผล) | ขั้น 5 มี over-cap summary | ☐ |
| 2 | VERIFY ปุ่ม **บันทึกและส่งอนุมัติ** | — | disabled · hover เห็น title **ต้องระบุเหตุผลรายการที่เกินเพดานก่อนส่ง** | ☐ |

#### TC-OC03 — กรอกเหตุผลครบ → ส่งได้ (over-cap ไม่ block · AC-03)
- group: G2 · ความสำคัญ: สูง · trace: FN-04 · BR-02 · LOCK-08 · AC-03
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: (ต่อจาก TC-OC02 หรือใบ over-cap ขั้น 3)
- ชุดข้อมูล: B + over_reason
- ผ่านเมื่อ: กรอกเหตุผล → ปุ่มส่งเปิดใช้ได้ → ส่งอนุมัติสำเร็จ (ไม่ถูก block)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **เหตุผลการเบิกเกินเพดาน (จำเป็น)** | over_reason | ช่องแสดงข้อความ · panel เตือนยังอยู่ (informational) | ☐ |
| 2 | ไปขั้น 5 → VERIFY ปุ่ม **บันทึกและส่งอนุมัติ** | — | enabled (ไม่ disabled) | ☐ |
| 3 | CLICK **บันทึกและส่งอนุมัติ** → เลือก slot ครบ → **ส่งอนุมัติ** | A1 | toast **ส่งคำขออนุมัติแล้ว — …** (ส่งได้แม้เกินเพดาน) | ☐ |

#### TC-OC04 — ใบ over-cap ใน list ขึ้น chip "เกินเพดาน" (FN-90 · event exp.overcap)
- group: G2 · ความสำคัญ: กลาง · trace: FN-04/90 · AC-13
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d4 (E03 · 66,340 over-cap) · files=—
- Start: OPEN `expense.html` → สลับบทบาท **ผู้อนุมัติ (DOA)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: แถว d4 (ธนากร) แสดง chip **เกินเพดาน** (warning)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ผู้อนุมัติ (DOA)** (มุมมองสาธิต) | — | list แสดงทุกใบ (scope:all) | ☐ |
| 2 | VERIFY แถว ธนากร พูนผล (รออนุมัติ · 66,340) | — | มี chip **เกินเพดาน** ในแถว | ☐ |

#### TC-V01 — ไม่มีรายการ → กด "ถัดไป" ขั้น 3 ไม่ได้ (FN-05 · BR_SUBMIT_NO_LINES)
- group: G2 · ความสำคัญ: สูง · trace: FN-05/92 · BR-03 · AC-04 · error BR_SUBMIT_NO_LINES
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (ผู้เบิก A · ไม่มีรายการ)
- ชุดข้อมูล: —
- ผ่านเมื่อ: 0 รายการ → empty "ยังไม่มีรายการ — กด …" + ปุ่ม "ถัดไป" กดไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 3 (ไม่กดเพิ่มรายการ) | — | empty **ยังไม่มีรายการ — กด "เพิ่มรายการ"** | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | กดไม่ได้ (disabled · gate ≥1 รายการ + ยอด>0) | ☐ |

#### TC-V02 — ยอดรวม = 0 → ปุ่มส่งอนุมัติ disabled + title (FN-05 · AC-04)
- group: G2 · ความสำคัญ: สูง · trace: FN-05 · BR-03 · AC-04
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (ผู้เบิก A)
- ชุดข้อมูล: F
- ผ่านเมื่อ: มีรายการแต่ยอด=0 → ปุ่ม "บันทึกและส่งอนุมัติ" disabled + title "ต้องมีรายการและยอด > 0"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → กรอกจำนวนเงิน 0 | F | totbox รวมทั้งสิ้น = 0 | ☐ |
| 2 | (ถ้า gate ปล่อยถึงขั้น 5) VERIFY ปุ่ม **บันทึกและส่งอนุมัติ** | — | disabled + title **ต้องมีรายการและยอด > 0** | ☐ |

#### TC-RC01 — หมวดบังคับใบเสร็จ ไม่แนบ → ขั้น 4 เตือน (FN-12 · BR_RECEIPT_REQUIRED)
- group: G2 · ความสำคัญ: สูง · trace: FN-12 · BR-03 · AC-04 · error BR_RECEIPT_REQUIRED
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 4 (ใบหมวด ที่พัก)
- ชุดข้อมูล: E
- ผ่านเมื่อ: ขั้น 4 hookbox แสดงหมวดที่บังคับแนบใบเสร็จ (ที่พัก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบหมวด ที่พัก ถึงขั้น 4 | E | ขั้น 4 hookbox ระบุ **หมวดที่นโยบายบังคับแนบใบเสร็จ** = ที่พัก | ☐ |
| 2 | VERIFY upload-zone | — | มี upload-zone (PDF/JPG/PNG · OCR ไม่รองรับ) | ☐ |

#### TC-RC02 — แนบใบเสร็จ PDF → ผ่านขั้น 4 (FN-12)
- group: G2 · ความสำคัญ: กลาง · trace: FN-12 · AC-04
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=`receipt_hotel.pdf`
- Start: (ต่อจาก TC-RC01 ขั้น 4)
- ชุดข้อมูล: E
- ผ่านเมื่อ: อัปโหลดไฟล์ → ไปขั้น 5 ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD receipt_hotel.pdf → upload-zone | receipt_hotel.pdf | ไฟล์แสดงใน zone (mock) | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น 5 ตรวจสอบและยืนยัน | ☐ |

### G3 — ส่งอนุมัติ DOA slot picker + re-resolve (FN-07/08/11)

#### TC-S01 — ส่งอนุมัติ ช่วง 5,000–50,000 → 2 slot (FN-07/08 · AC-05)
- group: G3 · ความสำคัญ: สูง · trace: FN-07/08 · BR-04 · LOCK-01 · AC-05 · event exp.submitted
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → สร้างใบ A ถึงขั้น 5 → CLICK **บันทึกและส่งอนุมัติ**
- ชุดข้อมูล: A (4,500 + VAT = 4,815 → หรือใช้ยอด 4,500×? ; ปรับให้เข้า 5,000–50,000: ใช้ 8,000) · **หมายเหตุ:** ใช้ยอดที่ตกช่วง 5,000–50,000
- ผ่านเมื่อ: modal มี note "resolve ตามวงเงิน … ช่วง 5,000 – 50,000" + **2 slot** (หัวหน้าสายงาน + ผู้จัดการแผนก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบยอดในช่วง 5,000–50,000 → เปิด modal ส่งอนุมัติ | ยอด ≈ 8,560 | modal **ส่งอนุมัติ — เลือกผู้อนุมัติแต่ละ slot** | ☐ |
| 2 | VERIFY note ช่วงวงเงิน | — | note ระบุ **ช่วง 5,000 – 50,000 (ตัวอย่าง/mock)** + "ไม่ hardcode · ตั้งค่าจริงที่ DOA กลาง" | ☐ |
| 3 | VERIFY จำนวน slot-row | — | **2 slot** (หัวหน้าสายงาน · ผู้จัดการแผนก) | ☐ |
| 4 | SELECT ผู้อนุมัติ slot 1 + slot 2 | A1 สมพงษ์, A2 วิไล | 2 slot มีคน · ปุ่ม **ส่งอนุมัติ** enabled | ☐ |
| 5 | CLICK **ส่งอนุมัติ** | — | toast **ส่งคำขออนุมัติแล้ว — resolve สายตามวงเงิน + แจ้งผู้อนุมัติ** · ใบใหม่ pill รออนุมัติ | ☐ |

#### TC-S03 — ช่วง <5,000 → 1 slot เท่านั้น (FN-08 · LOCK-01)
- group: G3 · ความสำคัญ: สูง · trace: FN-08 · BR-04 · LOCK-01 · AC-05
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → สร้างใบยอด < 5,000 → เปิด modal ส่งอนุมัติ
- ชุดข้อมูล: (วัสดุ 1,000 · ไม่คิด → grand 1,000)
- ผ่านเมื่อ: modal มี **1 slot** (หัวหน้าสายงาน) + note ช่วง 0 – 5,000

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบยอด 1,000 → เปิด modal ส่งอนุมัติ | — | note ช่วง **0 – 5,000** · **1 slot** | ☐ |
| 2 | SELECT ผู้อนุมัติ slot 1 | A1 สมพงษ์ | ปุ่ม **ส่งอนุมัติ** enabled | ☐ |

#### TC-S04 — ช่วง >50,000 → 3 slot (FN-08 · LOCK-01)
- group: G3 · ความสำคัญ: สูง · trace: FN-08 · BR-04 · LOCK-01 · AC-05
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → สร้างใบ D → เปิด modal ส่งอนุมัติ
- ชุดข้อมูล: D (60,000)
- ผ่านเมื่อ: modal มี **3 slot** (หัวหน้าสายงาน · ผู้จัดการแผนก · ผู้อำนวยการ) + note ช่วง มากกว่า 50,000

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบ D → เปิด modal ส่งอนุมัติ | D: 60,000 | note ช่วง **มากกว่า 50,000** · **3 slot** | ☐ |
| 2 | VERIFY slot labels | — | หัวหน้าสายงาน · ผู้จัดการแผนก · ผู้อำนวยการ | ☐ |

#### TC-S05 — เลือก slot ไม่ครบ → ปุ่มส่งอนุมัติ disabled (BR_DOA_SLOTS_INCOMPLETE)
- group: G3 · ความสำคัญ: สูง · trace: FN-08 · BR-04 · AC-05 · error BR_DOA_SLOTS_INCOMPLETE
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → สร้างใบ D (3 slot) → เปิด modal ส่งอนุมัติ
- ชุดข้อมูล: D
- ผ่านเมื่อ: เลือกไม่ครบทุก slot → ปุ่ม "ส่งอนุมัติ" disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT เฉพาะ slot 1 (เว้น slot 2/3) | A1 | ปุ่ม **ส่งอนุมัติ** ยัง disabled | ☐ |
| 2 | SELECT slot 2 + slot 3 ครบ | A2, A3 | ปุ่ม **ส่งอนุมัติ** enabled | ☐ |

#### TC-S02 — ส่งอนุมัติจากใบฉบับร่าง (openSubmitDraft · FN-07)
- group: G3 · ความสำคัญ: กลาง · trace: FN-07 · AC-05
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=d1 (ร่าง · E01) · files=—
- Start: OPEN `expense.html` → CLICK แถว d1 `(ร่าง)` → view drawer
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer ใบ draft มีปุ่ม "ส่งอนุมัติ" → เปิด modal slot picker

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **(ร่าง)** ของ สมชาย ใจดี | — | view drawer เปิด · สถานะ ฉบับร่าง | ☐ |
| 2 | VERIFY footer | — | มีปุ่ม **ยกเลิก** + **ส่งอนุมัติ** | ☐ |
| 3 | CLICK ปุ่ม **ส่งอนุมัติ** | — | เปิด modal **ส่งอนุมัติ — เลือกผู้อนุมัติแต่ละ slot** (resolve ตามยอด d1) | ☐ |

#### TC-RR01 — แก้ยอดข้ามช่วง → re-resolve สาย DOA (FN-11 · BR-05)
- group: G3 · ความสำคัญ: สูง · trace: FN-11 · BR-05 · AC-05b
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard สร้างใบ · ขั้น 3 → ขั้น 5 → เปิด modal ส่งอนุมัติ
- ชุดข้อมูล: เริ่ม 3,000 (1 slot) → แก้เป็น 60,000 (3 slot)
- ผ่านเมื่อ: จำนวน slot เปลี่ยนตามยอด (1 → 3) เมื่อกลับไปแก้ยอดแล้วเปิด modal ใหม่ (resolveDoa เรียกซ้ำ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบยอด 3,000 → เปิด modal ส่งอนุมัติ → VERIFY+จด slot | 3,000 | จด: **1 slot** (ช่วง 0–5,000) | ☐ |
| 2 | ปิด modal → ย้อนกลับขั้น 3 แก้จำนวนเงินเป็น 60,000 | 60,000 | totbox รวม > 50,000 | ☐ |
| 3 | ไปขั้น 5 → เปิด modal ส่งอนุมัติอีกครั้ง | — | slot กลายเป็น **3 slot** (ช่วง >50,000) — ต่างจากค่าที่จดใน step 1 = re-resolve | ☐ |

### G4 — อนุมัติ → เลข+PDF+7C(FC/EC) + จ่าย hook (FN-09/10/16/19)

#### TC-AP01 — อนุมัติขั้นแรก (ยังไม่ครบสาย) → toast "อนุมัติขั้น N แล้ว — รอขั้นถัดไป"
- group: G4 · ความสำคัญ: สูง · trace: FN-09 · AC-06 · state pending_approval คงอยู่
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=ใบ 2 ขั้น pending (สร้างจาก TC-S01 · ยังไม่มี approve) · files=—
- Start: OPEN `expense.html` → สร้างใบ 2 ขั้นแล้วส่งอนุมัติ (ผู้เบิก) → สลับ **ผู้อนุมัติ (DOA)** → CLICK ใบนั้น
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติ 1 ครั้ง (ยังเหลือขั้น 2) → toast "อนุมัติขั้น 2 แล้ว — รอขั้นถัดไป" · ใบยังสถานะ **รออนุมัติ** (ไม่ออกเลข)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สลับบทบาท **ผู้อนุมัติ (DOA)** → CLICK ใบ 2 ขั้น (รออนุมัติ) | — | view drawer · footer มีปุ่ม **ไม่อนุมัติ** + **อนุมัติ** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** | — | modal **อนุมัติใบเบิก?** (desc ระบุออกเลข+PDF+7C ตอนครบสาย) | ☐ |
| 3 | CLICK ปุ่ม **อนุมัติ** (ใน modal) | — | toast **อนุมัติขั้น 2 แล้ว — รอขั้นถัดไป** · ใบคง pill **รออนุมัติ** (ยังไม่มีเลข EXP) | ☐ |

#### TC-AP02 — อนุมัติขั้นสุดท้าย → ครบสาย (ต่อจาก AP01)
- group: G4 · ความสำคัญ: สูง · trace: FN-09 · AC-06
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=ใบจาก AP01 (เหลือ 1 ขั้น) · files=—
- Start: (ต่อจาก TC-AP01) CLICK ใบเดิม
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติขั้นสุดท้าย → toast ครบสาย + ออกเลข EXP + สถานะ อนุมัติแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ใบเดิม → CLICK **อนุมัติ** → **อนุมัติ** (modal) | — | toast **อนุมัติครบสาย · ออกเลข EXP-2569-XXXX · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · ส่งสถานะจ่าย (hook)** | ☐ |
| 2 | VERIFY pill ใบ | — | pill **อนุมัติแล้ว** · code = EXP-2569-XXXX (ไม่ใช่ "(รออนุมัติ)") | ☐ |

#### TC-AP03 — อนุมัติใบ d3 (1 ขั้น) → เลข+PDF+7C ครบทีเดียว (FN-09/19 · LOCK-02/04)
- group: G4 · ความสำคัญ: สูง · trace: FN-09/19 · BR-06/07 · LOCK-02/04 · AC-06 · XT-01
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 (E02 · รออนุมัติ 1 ขั้น · ปรีชา วัฒน์ pending) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK แถว อรทัย แสนสุข (รออนุมัติ)
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติ → toast ครบสาย + เลข EXP + desc modal ระบุ **7C (บันทึกเข้า 7C ตาม CSQ_BRIEF_F101)** — ไม่มีคำว่า AC/ลงบัญชี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **อรทัย แสนสุข** (รออนุมัติ · d3) | — | view drawer · footer มี **ไม่อนุมัติ** + **อนุมัติ** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** | — | modal desc = **อนุมัติแล้วระบบจะออกเลข EXP-YYYY-NNNN + PDF + บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 + ส่งสถานะจ่ายให้ปลายทาง** (ไม่มีคำว่า AC/ลงบัญชี) | ☐ |
| 3 | CLICK **อนุมัติ** (modal) | — | toast **อนุมัติครบสาย · ออกเลข EXP-2569-XXXX · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · ส่งสถานะจ่าย (hook)** | ☐ |
| 4 | VERIFY ใบ | — | pill **อนุมัติแล้ว** · เลข EXP-2569-XXXX (immutable) | ☐ |

#### TC-AP04 — อนุมัติใบที่ไม่ได้รออนุมัติ → guard (BR_NOT_PENDING_APPROVAL)
- group: G4 · ความสำคัญ: กลาง · trace: FN-09 · AC-06 · error BR_NOT_PENDING_APPROVAL
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (approved · E01) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK แถว EXP-2569-0001 (อนุมัติแล้ว)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบ approved ไม่มีปุ่มอนุมัติ (footer edge-out ตามสถานะ) — ไม่มีทางกดอนุมัติซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **EXP-2569-0001** (อนุมัติแล้ว) | — | view drawer · สถานะ อนุมัติแล้ว | ☐ |
| 2 | VERIFY footer | — | **ไม่มีปุ่ม อนุมัติ/ไม่อนุมัติ** (ใบไม่ได้อยู่สถานะรออนุมัติ) | ☐ |

#### TC-PAY01 — เลือกช่องทางจ่าย → ส่งจ่าย hook display-only (FN-10 · LOCK-03 · XT-02)
- group: G4 · ความสำคัญ: สูง · trace: FN-10 · BR-09 · LOCK-03 · AC-07 · XT-02
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=d2 (approved · pay=payroll) · files=—
- Start: OPEN `expense.html` → สลับ **เจ้าหน้าที่ (HR/Finance)** → CLICK แถว EXP-2569-0001 → tab รายละเอียด
- ชุดข้อมูล: —
- ผ่านเมื่อ: hookbox "สถานะการจ่าย" แสดง "อ่านจากปลายทาง … display-only — Expense ไม่จ่าย/ไม่ลงบัญชีเอง"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **EXP-2569-0001** → tab **รายละเอียด** | — | เห็น section **สถานะการจ่าย** (hookbox) | ☐ |
| 2 | VERIFY hookbox จ่าย | — | ข้อความระบุ **อ่านจากปลายทาง … display-only — Expense ไม่จ่าย/ไม่ลงบัญชีเอง** (payHook = ส่งจ่ายผ่านเงินเดือน · รอบ ก.ย. 2569) | ☐ |

#### TC-PAY02 — สถานะ "จ่ายแล้ว" อ่านจากปลายทาง (FN-16 · display-only)
- group: G4 · ความสำคัญ: กลาง · trace: FN-16 · BR-09 · AC-07
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=d6 (paid · E02) · files=—
- Start: OPEN `expense.html` → สลับ **เจ้าหน้าที่ (HR/Finance)** → CLICK แถว EXP-2569-0002 (จ่ายแล้ว)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบ paid แสดง payHook "โอนแล้ว · 2569-08-28" + note display-only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว EXP-2569-0002 | — | pill **จ่ายแล้ว** | ☐ |
| 2 | CLICK แถว → tab รายละเอียด → VERIFY hookbox จ่าย | — | payHook **โอนแล้ว · 2569-08-28** + display-only (อ่านจากปลายทาง Finance) | ☐ |

### G5 — ตีกลับ / reopen / ยกเลิก (FN-13/14/91)

#### TC-RJ01 — ตีกลับต้องมีเหตุผล (FN-13/91 · BR-18 · ERR_REASON_REQUIRED)
- group: G5 · ความสำคัญ: สูง · trace: FN-13/91 · BR-18 · AC-08 · error ERR_REASON_REQUIRED · event exp.rejected
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 (รออนุมัติ · E02) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK แถว อรทัย แสนสุข (รออนุมัติ)
- ชุดข้อมูล: reject_reason
- ผ่านเมื่อ: ปุ่ม "ยืนยันตีกลับ" disabled จนกรอกเหตุผล → กรอกแล้วตีกลับได้ → toast + สถานะ ตีกลับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ไม่อนุมัติ** | — | modal **ไม่อนุมัติ (ตีกลับ)** · textarea เหตุผล · ปุ่ม **ยืนยันตีกลับ** disabled | ☐ |
| 2 | VERIFY ปุ่มยืนยัน (ยังไม่กรอก) | — | **ยืนยันตีกลับ** disabled | ☐ |
| 3 | TYPE → textarea เหตุผล | reject_reason | ปุ่ม **ยืนยันตีกลับ** enabled | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันตีกลับ** | — | toast **ตีกลับ + แจ้งผู้เบิกแล้ว (แก้แล้วยื่นใหม่ได้)** · ใบ pill **ตีกลับ** | ☐ |

#### TC-RJ02 — reopen ใบที่ถูกตีกลับ → กลับเป็น draft (FN-13 · AC-08)
- group: G5 · ความสำคัญ: สูง · trace: FN-13 · AC-08 · state rejected→draft
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=d5 (ตีกลับ · E04) — **หมายเหตุ:** d5 emp=E04 (ไม่ใช่ self E01) → mask; ใช้ใบที่ตีกลับจาก TC-RJ01 (E02) ก็ mask เช่นกัน · เพื่อทดสอบ reopen ใช้บทบาทที่เห็นใบ (mgr/officer เห็นทุกใบ แต่ reopen เป็นสิทธิ์ผู้เบิก) — **ในโปรโตไทป์ reopen guard = สถานะเท่านั้น**; ทดสอบผ่านใบ rejected ใดก็ได้ที่เปิดดูได้ · files=—
- Start: OPEN `expense.html` → CLICK ใบสถานะ **ตีกลับ**
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer ใบ rejected มีปุ่ม "แก้ไขและยื่นใหม่" → กด → toast reopen + สถานะกลับ ฉบับร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ใบสถานะ **ตีกลับ** (เช่น มะลิ ดอกไม้ · d5) | — | view drawer · แสดงเหตุผลตีกลับ · footer มีปุ่ม **แก้ไขและยื่นใหม่** | ☐ |
| 2 | CLICK ปุ่ม **แก้ไขและยื่นใหม่** | — | toast **เปิดแก้ไขใบเบิก — แก้แล้วส่งอนุมัติใหม่ได้** · ใบเปลี่ยนเป็น pill **ฉบับร่าง** | ☐ |

#### TC-RJ03 — reopen ใบที่ไม่ถูกตีกลับ → guard toast (BR_REOPEN_ONLY_REJECTED)
- group: G5 · ความสำคัญ: กลาง · trace: FN-13 · AC-08 · error BR_REOPEN_ONLY_REJECTED
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (approved) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ใบ approved
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบ approved ไม่มีปุ่ม "แก้ไขและยื่นใหม่" (guard) — footer แสดงเฉพาะ action ตามสถานะ; ถ้ามีทางเรียก reopen → toast "เปิดแก้ไขไม่ได้ — ทำได้เฉพาะใบที่ถูกตีกลับ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ใบ **EXP-2569-0001** (อนุมัติแล้ว) | — | view drawer · **ไม่มีปุ่ม แก้ไขและยื่นใหม่** ใน footer | ☐ |
| 2 | VERIFY (guard) | — | ไม่มีทาง reopen ใบ approved (ถ้าถูกเรียก → toast **เปิดแก้ไขไม่ได้ — ทำได้เฉพาะใบที่ถูกตีกลับ**) | ☐ |

#### TC-CX01 — ยกเลิกฉบับร่าง (confirm + soft archive · FN-14/91)
- group: G5 · ความสำคัญ: สูง · trace: FN-14/91 · BR-10 · LOCK-07 · AC-09
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=d1 (ร่าง · E01) · files=—
- Start: OPEN `expense.html` → CLICK แถว (ร่าง) สมชาย ใจดี
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ยืนยัน "ยกเลิกใบเบิก?" / "ใบเบิกจะถูกยกเลิก (soft archive)" → ยกเลิก → toast + สถานะ ยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **(ร่าง)** → CLICK ปุ่ม **ยกเลิก** (footer) | — | modal **ยกเลิกใบเบิก?** · body **ใบเบิกจะถูกยกเลิก (soft archive)** · ปุ่ม **ยกเลิกใบเบิก** (danger) | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิกใบเบิก** | — | toast **ยกเลิกใบเบิกแล้ว (soft archive)** · ใบ pill **ยกเลิก** | ☐ |

#### TC-CX02 — ยกเลิกใบที่ไม่ใช่ฉบับร่าง → guard (BR_CANCEL_ONLY_DRAFT)
- group: G5 · ความสำคัญ: สูง · trace: FN-14 · AC-09 · error BR_CANCEL_ONLY_DRAFT
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 (รออนุมัติ) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ใบ รออนุมัติ
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบที่ไม่ใช่ draft ไม่มีปุ่มยกเลิก (footer edge-out) — ถ้าเรียก doCancel → toast "ยกเลิกไม่ได้ — ทำได้เฉพาะใบฉบับร่าง"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ใบ **รออนุมัติ** (อรทัย · d3) | — | footer แสดง action ตามสถานะ pending (อนุมัติ/ไม่อนุมัติ) · **ไม่มีปุ่มยกเลิก** | ☐ |
| 2 | VERIFY guard | — | ไม่มีทางยกเลิกใบ non-draft (ถ้าถูกเรียก → toast **ยกเลิกไม่ได้ — ทำได้เฉพาะใบฉบับร่าง**) | ☐ |

### G6 — view drawer 4 tabs + PDF a4 + ลายเซ็น (FN-15/17)

#### TC-VW01 — view drawer 4 tabs ครบ (FN-17 · AC-10)
- group: G6 · ความสำคัญ: กลาง · trace: FN-17 · AC-10
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (approved · E01) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK แถว EXP-2569-0001
- ชุดข้อมูล: —
- ผ่านเมื่อ: 4 tabs = รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **EXP-2569-0001** | — | view drawer เปิด · 4 tab: **รายละเอียด · PDF Preview · ลายเซ็น / อนุมัติ · ประวัติ** | ☐ |
| 2 | CLICK tab **รายละเอียด** | — | kv (เลขที่/ผู้เบิก/ศูนย์ต้นทุน ณ วันเบิก/วันที่/ช่องทางจ่าย/สถานะ) + ตารางรายการ + **เอกสารแนบ** section | ☐ |

#### TC-VW02 — tab ประวัติ = audit append-only (FN-17/93)
- group: G6 · ความสำคัญ: กลาง · trace: FN-17/93 · AC-15
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (มี audit: ยื่น + อนุมัติออกเลข) · files=—
- Start: (ต่อจาก TC-VW01)
- ชุดข้อมูล: —
- ผ่านเมื่อ: tab ประวัติ = timeline "(audit · append-only)" มี entry อนุมัติ+ยื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **ประวัติ** | — | timeline audit มี entry **อนุมัติ · ออกเลข EXP-2569-0001** (วิไล ประสงค์) + **ยื่นคำขอ** (สมชาย ใจดี) + ป้าย **(audit · append-only)** | ☐ |

#### TC-VW03 — tab PDF Preview a4 + ช่องลายเซ็น 3 ช่อง (FN-15)
- group: G6 · ความสำคัญ: กลาง · trace: FN-15 · AC-10
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 · files=—
- Start: (view drawer EXP-2569-0001)
- ชุดข้อมูล: —
- ผ่านเมื่อ: tab PDF = a4 doc + ช่องลายเซ็น 3 ช่อง (ผู้เบิก / ผู้อนุมัติ DOA / การเงิน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **PDF Preview** | — | a4 doc: หัวบริษัท + เลขที่/วันที่ + ผู้เบิก/ตำแหน่ง/ศูนย์ต้นทุน + ตารางรายการ + ยอดรวม/VAT/รวมทั้งสิ้น | ☐ |
| 2 | VERIFY ช่องลายเซ็น | — | **3 ช่อง**: ผู้เบิก · ผู้อนุมัติ (DOA) · การเงิน | ☐ |

#### TC-VW04 — tab ลายเซ็น/อนุมัติ = DOA timeline + range label (FN-15)
- group: G6 · ความสำคัญ: กลาง · trace: FN-15 · AC-10 · LOCK-01
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d4 (3 ขั้น · 2 approved 1 pending) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK แถว ธนากร (รออนุมัติ 66,340)
- ชุดข้อมูล: —
- ผ่านเมื่อ: tab ลายเซ็น = DOA timeline 3 ขั้น (approved/approved/pending) + note ช่วงวงเงิน mock

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **ธนากร** → tab **ลายเซ็น / อนุมัติ** | — | timeline 3 ขั้น: หัวหน้าสายงาน (✓) · ผู้จัดการแผนก (✓) · ผู้อำนวยการ (รอ) | ☐ |
| 2 | VERIFY note range | — | note ช่วงวงเงินเป็นตัวอย่าง (mock) — ตั้งค่าจริงที่ DOA กลาง · re-resolve อัตโนมัติ | ☐ |

### G7 — touchpoint: PV/petty + หักลบทดรอง F103 (FN-18)

#### TC-TP01 — ช่องทางจ่ายมี PV + เงินสดย่อย (F091) (FN-18 · PM/BA add)
- group: G7 · ความสำคัญ: สูง · trace: FN-18 · LOCK-09 · AC-11
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → CLICK **สร้างใบเบิก** → ขั้น 2 (เลือกผู้เบิก)
- ชุดข้อมูล: —
- ผ่านเมื่อ: dropdown ช่องทางจ่ายมี 4 ตัวเลือกรวม **ใบสำคัญจ่าย (PV)** + **เงินสดย่อย (F091)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องทางจ่าย (dropdown) | — | 4 ตัวเลือก: ผ่านรอบเงินเดือน · โอนตรง · **ใบสำคัญจ่าย (PV)** · **เงินสดย่อย (F091)** | ☐ |
| 2 | SELECT **เงินสดย่อย (F091)** | — | ช่องทางจ่าย = เงินสดย่อย (F091) (hook display-only ปลายทาง Finance) | ☐ |

#### TC-TP02 — หมวดสวัสดิการ (รับรอง) hook F102 display-only (FN-18/BR-15)
- group: G7 · ความสำคัญ: กลาง · trace: FN-18 · BR-15 · AC-11 · XT-05
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard สร้างใบหมวด รับรอง (ent) ถึงขั้น 5
- ชุดข้อมูล: H (รับรอง 6,000)
- ผ่านเมื่อ: ขั้น 5 budgetHookHTML แสดง F102 สวัสดิการ (สิทธิ์ 5,000) + warn display-only (ไม่ block)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบหมวด รับรอง 6,000 → ไปขั้น 5 | H | budgetHookHTML แสดง F117 งบ + **F102 สวัสดิการ** (สิทธิ์คงเหลือ mock 5,000) | ☐ |
| 2 | VERIFY warn (เกินสิทธิ์) | — | เตือน display-only (6,000 > 5,000) · **ไม่ block การส่ง** | ☐ |

#### TC-TP03 — หักลบเงินทดรอง display-only (FN-18 · BR-11 · XT-03)
- group: G7 · ความสำคัญ: สูง · trace: FN-18 · BR-11 · LOCK-09 · AC-11 · XT-03
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=ใบของ E03 ธนากร (มีทดรองค้าง 15,000 · d4) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK แถว ธนากร (d4) → tab รายละเอียด
- ชุดข้อมูล: —
- ผ่านเมื่อ: section "เคลียร์เงินทดรอง (F103 · soft-ref · display-only)" แสดง ทดรองค้าง 15,000 + ยอดจ่ายสุทธิ = grand − offset + note F101 ไม่ปรับ ledger

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **ธนากร** (d4) → tab **รายละเอียด** → scroll | — | section **เคลียร์เงินทดรอง (F103 · soft-ref · display-only)** | ☐ |
| 2 | VERIFY ทดรอง + สุทธิ | — | เงินทดรองค้างของผู้เบิก **15,000** (mock · อ่านจาก F103) · **ยอดจ่ายสุทธิ = ยอดใบเบิก − 15,000** | ☐ |
| 3 | VERIFY note display-only | — | note ระบุ F101 ไม่ปรับยอดทดรองเอง · ส่งค่าหักลบให้ F103 · display-only | ☐ |

#### TC-ADV01 — ทดรอง > ยอดใบ → net_pay=0 + ทดรองคงค้าง (EC-06 · FN-18)
- group: G7 · ความสำคัญ: กลาง · trace: FN-18 · BR-11 · EC-06 · AC-11
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=E03 ทดรอง 15,000 · ใบยอด < 15,000 (เช่น 5,000) · files=—
- Start: OPEN `expense.html` → wizard สร้างใบผู้เบิก **ธนากร (E03)** ยอด 5,000 → ขั้น 5
- ชุดข้อมูล: (ผู้เบิก E03 · ยอด 5,000)
- ผ่านเมื่อ: advance offset = min(15,000, 5,000) = 5,000 → net_pay=0 + ทดรองคงค้าง = 10,000

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบผู้เบิก ธนากร (E03) ยอด 5,000 → ขั้น 5 → VERIFY+จด | — | จด: ทดรองค้าง 15,000 · ยอดใบ 5,000 | ☐ |
| 2 | VERIFY ยอดจ่ายสุทธิ | — | **ยอดจ่ายสุทธิ = 0** (max(0, 5,000 − 5,000)) · **ทดรองคงค้าง 10,000** (15,000 − 5,000) | ☐ |

### G8 — visibility scope + role เจ้าหน้าที่ ไม่อนุมัติ (FN-20/94)

#### TC-P01 — ผู้เบิก/ธุรการ เห็นเฉพาะใบของตน (scope:self · FN-20)
- group: G8 · ความสำคัญ: สูง · trace: FN-20 · BR-12 · LOCK-10 · AC-12
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ (self=E01 สมชาย) · seed=6 docs (E01 มี d1,d2) · files=—
- Start: OPEN `expense.html` (default role)
- ชุดข้อมูล: —
- ผ่านเมื่อ: list แสดงเฉพาะใบของ E01 (สมชาย ใจดี) — ไม่เห็นใบ E02/E03/E04

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY list (บทบาท ผู้เบิก/ธุรการ) | — | เห็นเฉพาะแถว **สมชาย ใจดี** (d1 ร่าง + d2 EXP-2569-0001) · ไม่เห็น อรทัย/ธนากร/มะลิ | ☐ |

#### TC-P02 — ผู้เบิก mask ยอดใบคนอื่น · ผู้อนุมัติ unmask (FN-94)
- group: G8 · ความสำคัญ: สูง · trace: FN-94/20 · BR-12 · AC-16
- actor (role): ผู้เบิก/ธุรการ → ผู้อนุมัติ (DOA)
- Setup: role สลับ · seed=6 docs · files=—
- Start: OPEN `expense.html`
- ชุดข้อมูล: —
- ผ่านเมื่อ: (self scope ทำให้ผู้เบิกไม่เห็นใบคนอื่นอยู่แล้ว) สลับเป็น ผู้อนุมัติ → เห็นทุกใบ + ยอดเต็ม (unmask)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (ผู้เบิก/ธุรการ) VERIFY ยอดใบของตน | — | ยอด d2 แสดงเต็ม (ใบของตน · ไม่ mask) | ☐ |
| 2 | CLICK ปุ่ม **ผู้อนุมัติ (DOA)** | — | list แสดงทุกใบ · ยอดทุกใบ **แสดงเต็ม (unmask)** — ไม่มี `฿ •••••` | ☐ |

#### TC-P03 — ผู้เบิก/ธุรการ อนุมัติไม่ได้ (ไม่มีปุ่ม · SoD · ERR_NOT_APPROVER)
- group: G8 · ความสำคัญ: สูง · trace: FN-20/94 · BR-13 · AC-12 · error ERR_NOT_APPROVER
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=ใบ pending ที่ผู้เบิกเห็น (ต้องเป็นใบของตน — ผู้เบิก self scope; ใช้ใบ pending ที่สร้างเอง) · files=—
- Start: OPEN `expense.html` → สร้าง+ส่งใบ (สถานะ รออนุมัติ) → CLICK ใบนั้น
- ชุดข้อมูล: A
- ผ่านเมื่อ: ใบ pending ใต้บทบาทผู้เบิก → footer note "รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้" (ไม่มีปุ่มอนุมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้าง+ส่งใบ → CLICK ใบสถานะ **รออนุมัติ** (บทบาท ผู้เบิก) | A | view drawer · footer **ไม่มีปุ่ม อนุมัติ/ไม่อนุมัติ** | ☐ |
| 2 | VERIFY note | — | footer แสดง **รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้** | ☐ |

#### TC-P04 — เจ้าหน้าที่ (HR/Finance) เห็นทุกใบ + unmask แต่ **อนุมัติไม่ได้** (FN-20 · LOCK-10)
- group: G8 · ความสำคัญ: สูง · trace: FN-20 · BR-12/13 · LOCK-10 · AC-12 · error ERR_NOT_APPROVER
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=d3/d4 (รออนุมัติ) · files=—
- Start: OPEN `expense.html` → CLICK ปุ่ม **เจ้าหน้าที่ (HR/Finance)** → CLICK ใบ รออนุมัติ
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นทุกใบ + ยอดเต็ม แต่ใบ pending **ไม่มีปุ่มอนุมัติ** + note "รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เจ้าหน้าที่ (HR/Finance)** (มุมมองสาธิต) | — | list แสดงทุกใบ (scope:all) · ยอดเต็ม (unmask) | ☐ |
| 2 | CLICK ใบ **รออนุมัติ** (ธนากร · d4) | — | view drawer · **ไม่มีปุ่ม อนุมัติ/ไม่อนุมัติ** (approver:false) | ☐ |
| 3 | VERIFY note | — | **รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้** | ☐ |

#### TC-P05 — เจ้าหน้าที่ (HR/Finance) scope:all unmask ยอดใบคนอื่น (FN-20)
- group: G8 · ความสำคัญ: กลาง · trace: FN-20/94 · BR-12 · AC-12
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=6 docs · files=—
- Start: OPEN `expense.html` → CLICK **เจ้าหน้าที่ (HR/Finance)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยอดทุกใบ (รวมใบคนอื่น) แสดงเต็ม ไม่มี `฿ •••••`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ยอดรวมทุกแถว | — | ทุกยอดเป็นตัวเลขเต็ม (เช่น d4 = 66,340) · ไม่มี `฿ •••••` | ☐ |

### G9 — กติกากลาง (FN-90/91/92/93)

#### TC-G01 — list docPill 7 สถานะ + signprog (FN-90)
- group: G9 · ความสำคัญ: กลาง · trace: FN-90 · AC-13
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=6 docs (6 สถานะ) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น docPill หลากสถานะ (ฉบับร่าง/รออนุมัติ/อนุมัติแล้ว/ตีกลับ/จ่ายแล้ว) + คอลัมน์ลายเซ็น signprog (done/total)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์สถานะ | — | pill: ฉบับร่าง · รออนุมัติ · อนุมัติแล้ว · ตีกลับ · จ่ายแล้ว | ☐ |
| 2 | VERIFY คอลัมน์ลายเซ็น (signprog) | — | แสดง done/total เช่น d4 = 2/3 · มี progress bar | ☐ |

#### TC-G02 — ค้นหา/filter สถานะ (FN-90)
- group: G9 · ความสำคัญ: กลาง · trace: FN-90 · AC-13
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=6 docs · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: filter สถานะ = รออนุมัติ → เหลือเฉพาะใบ pending · ค้นหาชื่อ → กรองแถว · ล้างตัวกรอง → คืนทุกแถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT filter สถานะ → **รออนุมัติ** | — | เหลือเฉพาะแถว pending (อรทัย d3 · ธนากร d4) | ☐ |
| 2 | TYPE → ช่องค้นหา | ธนากร | เหลือเฉพาะแถว ธนากร | ☐ |
| 3 | CLICK ปุ่ม **ล้างตัวกรอง** | — | คืนทุกแถว (6 ใบ) · ช่องค้นหาว่าง · สถานะ = ทุกสถานะ | ☐ |

#### TC-G03 — filter ไม่เจอ → empty state (FN-90)
- group: G9 · ความสำคัญ: กลาง · trace: FN-90 · AC-13
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=6 docs · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค้นหาคำที่ไม่มี → empty "ยังไม่มีใบเบิก" + ข้อความแนะนำ + ปุ่ม "สร้างใบเบิก"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | zzzไม่มีจริง | ตารางว่าง | ☐ |
| 2 | VERIFY empty | — | **ยังไม่มีใบเบิก** + **สร้างใบเบิกใหม่ ระบบจะตรวจเพดานหมวดและ resolve สายอนุมัติตามวงเงินให้** + ปุ่ม **สร้างใบเบิก** | ☐ |

#### TC-G04 — ทุก destructive action ผ่าน confirm (FN-91)
- group: G9 · ความสำคัญ: กลาง · trace: FN-91 · AC-08/09
- actor (role): ผู้เบิก/ธุรการ + ผู้อนุมัติ (DOA)
- Setup: role=ตามขั้น · seed=d1 (ร่าง) + d3 (รออนุมัติ) · files=—
- Start: OPEN `expense.html`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิก + ตีกลับ ต้องผ่าน modal confirm ก่อนเสมอ (ไม่มี action ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (ผู้เบิก) CLICK ใบ (ร่าง) → **ยกเลิก** | — | เปิด modal confirm ก่อน (ไม่ยกเลิกทันที) | ☐ |
| 2 | PRESS Esc | — | modal ปิด · ใบยังเป็น ฉบับร่าง (ไม่ถูกยกเลิก) | ☐ |
| 3 | (ผู้อนุมัติ) CLICK ใบ รออนุมัติ → **ไม่อนุมัติ** | — | เปิด modal ตีกลับ (ต้องกรอกเหตุผล) ก่อน | ☐ |

#### TC-WL01 — wizard ล็อกลำดับ + step-advance gate (FN-92 · BR-14)
- group: G9 · ความสำคัญ: สูง · trace: FN-92 · BR-14 · AC-14
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → CLICK **สร้างใบเบิก**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ขั้น 2 ไม่เลือกผู้เบิก → "ถัดไป" กดไม่ได้ · ขั้น 3 ไม่มีรายการ → "ถัดไป" กดไม่ได้ (gate ตามลำดับ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** (ขั้น 1 → 2) → **ถัดไป** โดยไม่เลือกผู้เบิก | — | ขั้น 2 ปุ่ม **ถัดไป** disabled (ต้องเลือกผู้เบิกก่อน) | ☐ |
| 2 | SELECT ผู้เบิก → **ถัดไป** → (ขั้น 3 ไม่มีรายการ) CLICK **ถัดไป** | สมชาย ใจดี | ขั้น 3 ปุ่ม **ถัดไป** disabled (ต้องมี ≥1 รายการ + ยอด>0) | ☐ |

#### TC-ID01 — กัน double-submit (state._busy · FN-92 · EC-03)
- group: G9 · ความสำคัญ: สูง · trace: FN-92 · BR-14 · EC-03 · AC-14 · error ERR_DUPLICATE_IDEMPOTENCY_KEY
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 (รออนุมัติ 1 ขั้น) · files=— · **(ต้อง simulate double-click เร็ว)**
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ใบ รออนุมัติ → **อนุมัติ**
- ชุดข้อมูล: —
- ผ่านเมื่อ: กดปุ่ม "อนุมัติ" ใน modal ซ้ำเร็ว ๆ → เกิด side-effect ครั้งเดียว (ออกเลขใบเดียว · ไม่ซ้ำ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → ใน modal CLICK ปุ่ม **อนุมัติ** สองครั้งเร็ว | — | toast ครบสายปรากฏครั้งเดียว · ออกเลข EXP เดียว (state._busy กันซ้ำ) | ☐ |
| 2 | VERIFY list | — | ใบเปลี่ยนเป็น อนุมัติแล้ว 1 ใบ (ไม่มีการอนุมัติ/ออกเลขซ้ำ) | ☐ |

#### TC-AU01 — audit บันทึกทุก action (append-only · FN-93)
- group: G9 · ความสำคัญ: กลาง · trace: FN-93 · AC-15 · LOCK-07
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → อนุมัติ d3 → เปิด view tab ประวัติ
- ชุดข้อมูล: —
- ผ่านเมื่อ: หลังอนุมัติ → tab ประวัติมี entry ใหม่ (อนุมัติ/ออกเลข) ต่อท้าย (append-only · ของเก่าไม่หาย)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อนุมัติ d3 (ครบสาย) → CLICK ใบเดิม → tab **ประวัติ** | — | มี entry **อนุมัติ · ออกเลข EXP-…** เพิ่ม + entry **ยื่นคำขอ** เดิมยังอยู่ | ☐ |
| 2 | VERIFY ป้าย append-only | — | ป้าย **(audit · append-only)** ปรากฏ | ☐ |

#### TC-AU02 — audit มี entry create/แก้/อนุมัติ ครบสาย (FN-93)
- group: G9 · ความสำคัญ: กลาง · trace: FN-93 · AC-15
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (approved · audit 2 entry) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK EXP-2569-0001 → tab ประวัติ
- ชุดข้อมูล: —
- ผ่านเมื่อ: timeline มี 2 entry เรียงเวลา (ยื่นคำขอ 09:05 → อนุมัติออกเลข 10:20)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK EXP-2569-0001 → tab **ประวัติ** | — | timeline: **ยื่นคำขอ** (สมชาย ใจดี · 2569-08-31 09:05) → **อนุมัติ · ออกเลข EXP-2569-0001** (วิไล ประสงค์ · 10:20) | ☐ |

### G10 — Negatives "ห้ามมี" (unsupported 7 + guardrails · แทน FN-40)

#### TC-N01 — ไม่มีการจ่ายเงินจริง/ตัดจ่าย/GL post ในระบบ
- group: G10 · ความสำคัญ: สูง · trace: unsupported #1 · LOCK-03 · BR-09
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=d2 (approved) · files=—
- Start: OPEN `expense.html` → สลับ **เจ้าหน้าที่ (HR/Finance)** → CLICK EXP-2569-0001 → tab รายละเอียด
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม "จ่ายเงิน"/"ตัดจ่าย"/"ลงบัญชี/post GL" ที่ทำจริง — มีแค่ hookbox display-only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab รายละเอียด (ใบ approved) | — | **ไม่มี** ปุ่มจ่ายเงินจริง/โอน/ตัดจ่าย/post GL · มีเพียง hookbox "สถานะการจ่าย" display-only + note "Expense ไม่จ่าย/ไม่ลงบัญชีเอง" | ☐ |

#### TC-N02 — ไม่มี per diem / ค่าเดินทางต่อกิโลเมตร (mileage)
- group: G10 · ความสำคัญ: กลาง · trace: unsupported #3 (mileage)
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (line editor)
- ชุดข้อมูล: —
- ผ่านเมื่อ: dropdown หมวด มีแค่ 5 หมวด (เดินทาง/ที่พัก/รับรอง/วัสดุสำนักงาน/อื่นๆ) — **ไม่มี** per diem / mileage / ต่อกิโลเมตร

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** → เปิด dropdown หมวด | — | 5 ตัวเลือกเท่านั้น: เดินทาง · ที่พัก · รับรอง · วัสดุสำนักงาน · อื่นๆ | ☐ |
| 2 | VERIFY absence | — | **ไม่มี** ตัวเลือก per diem / mileage / ต่อกิโลเมตร · ไม่มีช่องระยะทาง | ☐ |

#### TC-N03 — ไม่มีคำขออนุมัติเดินทางล่วงหน้า (option ขั้น 1 disabled)
- group: G10 · ความสำคัญ: กลาง · trace: unsupported #4 (travel request)
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → CLICK **สร้างใบเบิก** → ขั้น 1
- ชุดข้อมูล: —
- ผ่านเมื่อ: radio "จากใบขออนุมัติเดินทาง" อยู่แต่ **disabled** (เลือกไม่ได้ · ไม่รองรับรอบนี้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 1 radio | — | "สร้างใหม่ (สำรองจ่ายเอง)" เลือกได้ · **"จากใบขออนุมัติเดินทาง" disabled** | ☐ |
| 2 | CLICK radio "จากใบขออนุมัติเดินทาง" | — | เลือกไม่ได้ (ยังอยู่ที่ "สร้างใหม่") | ☐ |

#### TC-N04 — ไม่มีระบบออกเงินทดรองเต็มรูป (แค่ touchpoint หักลบ)
- group: G10 · ความสำคัญ: กลาง · trace: unsupported #2/cash-advance · LOCK-09
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d4 (ผู้เบิก E03 มีทดรอง) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ธนากร → tab รายละเอียด
- ชุดข้อมูล: —
- ผ่านเมื่อ: section ทดรองเป็น **display-only** (แสดงยอด+หักลบ) — ไม่มีปุ่ม "ออกเงินทดรอง"/"เคลียร์ทดรอง"/แก้ ledger F103

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section เคลียร์เงินทดรอง | — | แสดงยอด+หักลบ display-only · **ไม่มี** ปุ่มออก/ปรับ/เคลียร์ทดรองจริง · note "F101 ไม่ปรับ ledger F103" | ☐ |

#### TC-N05 — ไม่มีหลายสกุลเงิน (THB only)
- group: G10 · ความสำคัญ: กลาง · trace: unsupported #5 (multi-currency)
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 3 (line editor)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีตัวเลือกสกุลเงิน — ทุกยอดเป็นบาท (฿) เท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY line editor + totbox | — | **ไม่มี** dropdown สกุลเงิน · ยอดทุกช่องเป็น ฿ (THB) เท่านั้น | ☐ |

#### TC-N06 — 7C มีแค่ FC/EC ไม่มี AC (FN-19 · LOCK-04)
- group: G10 · ความสำคัญ: สูง · trace: FN-19 · LOCK-04 · BR-07 · XT-01
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 (รออนุมัติ) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK d3 → **อนุมัติ**
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal desc + toast ระบุ **7C (FC/EC · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101)** — **ไม่มีคำว่า AC / ลงบัญชี / accounting post**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → อ่าน desc modal | — | desc = "…ออกเลข EXP-YYYY-NNNN + PDF + **บันทึกเข้า 7C ตาม CSQ_BRIEF_F101**…" · **ไม่มี** คำว่า AC/ลงบัญชี | ☐ |
| 2 | CLICK **อนุมัติ** → อ่าน toast | — | toast ระบุ **บันทึกเข้า 7C ตาม CSQ_BRIEF_F101** · **ไม่มี** AC posting | ☐ |

#### TC-N07 — ไม่มี OCR อ่านใบเสร็จอัตโนมัติ
- group: G10 · ความสำคัญ: ต่ำ · trace: unsupported #6 (OCR)
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=— · files=—
- Start: OPEN `expense.html` → wizard ขั้น 4 (เอกสารแนบ)
- ชุดข้อมูล: —
- ผ่านเมื่อ: upload-zone = แนบไฟล์ธรรมดา — ไม่มีปุ่ม/ข้อความ "อ่านใบเสร็จอัตโนมัติ (OCR)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY upload-zone ขั้น 4 | — | รองรับ PDF/JPG/PNG (แนบเฉย ๆ) · **ไม่มี** OCR / อ่านใบเสร็จอัตโนมัติ | ☐ |

#### TC-N08 — ไม่สามารถสร้าง/แก้เพดานหมวด/นโยบายเอง (อ่าน HR Config · LOCK-05)
- group: G10 · ความสำคัญ: กลาง · trace: unsupported #7 · LOCK-05 · BR-02
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=— · files=—
- Start: OPEN `expense.html` → สำรวจทั้งหน้า (list + wizard)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีหน้า/ปุ่ม "ตั้งค่าเพดานหมวด"/"แก้ HR Config" — เพดานเป็น read-only (มาจาก HR Config #107)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY sidebar + หน้าเบิกค่าใช้จ่าย | — | **ไม่มี** เมนู/ปุ่มตั้งค่าเพดานหมวด/แก้ HR Config · 1 เมนู = เบิกค่าใช้จ่าย เท่านั้น | ☐ |
| 2 | VERIFY over-cap panel (ขั้น 3) | — | เพดานแสดงเป็นค่าอ้างอิง (เช่น เดินทาง 5,000) · แก้ไม่ได้ในหน้านี้ | ☐ |

#### TC-N09 — ไม่มี path ยกเลิก/แก้หลังอนุมัติ (EC-05 · OQ-05 · XT-04)
- group: G10 · ความสำคัญ: สูง · trace: EC-05 · XT-04 · LD-06 · OQ-05
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (approved) + d6 (paid) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ใบ approved/paid
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบ approved/paid **ไม่มี** ปุ่มยกเลิก/แก้/reopen — ยืนยันไม่มี transition หลังอนุมัติ (conservative · รอ OQ-05)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ใบ **EXP-2569-0001** (อนุมัติแล้ว) | — | footer **ไม่มี** ปุ่มยกเลิก/แก้ไข/reopen | ☐ |
| 2 | CLICK ใบ **EXP-2569-0002** (จ่ายแล้ว) | — | footer **ไม่มี** ปุ่มยกเลิก/แก้/ถอน — ไม่มี path reverse EC/release FC | ☐ |

### G11 — Permission matrix รวบ (3 role × action)

#### TC-PM01 — ผู้เบิก/ธุรการ: create/submit allow · approve deny
- group: G11 · ความสำคัญ: สูง · trace: FN-20 · BR-13 · §5.3
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=6 docs · files=—
- Start: OPEN `expense.html`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มีปุ่ม "สร้างใบเบิก" (allow) · ใบ pending ของตน = ไม่มีปุ่มอนุมัติ (deny)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY topbar | — | ปุ่ม **สร้างใบเบิก** ปรากฏ (create allow) | ☐ |
| 2 | VERIFY ใบ pending (ของตน) footer | — | ไม่มีปุ่มอนุมัติ · note "รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้" (approve deny) | ☐ |

#### TC-PM02 — ผู้อนุมัติ (DOA): approve/reject allow · view all unmask
- group: G11 · ความสำคัญ: สูง · trace: FN-20 · BR-13 · §5.3
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3/d4 (pending) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบ pending มีปุ่มอนุมัติ+ไม่อนุมัติ (allow) · เห็นทุกใบ ยอดเต็ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ใบ pending (ธนากร d4) | — | footer มีปุ่ม **ไม่อนุมัติ** + **อนุมัติ** (approve/reject allow) | ☐ |
| 2 | VERIFY list scope | — | เห็นทุกใบ (6 ใบ) · ยอดเต็มทุกใบ (unmask) | ☐ |

#### TC-PM03 — เจ้าหน้าที่ (HR/Finance): view all + จ่าย hook allow · approve deny
- group: G11 · ความสำคัญ: สูง · trace: FN-20 · BR-12/13 · §5.3
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=d2 (approved) + d4 (pending) · files=—
- Start: OPEN `expense.html` → สลับ **เจ้าหน้าที่ (HR/Finance)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นทุกใบ+unmask · ใบ approved เข้าถึงช่องทางจ่าย hook · ใบ pending ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY list | — | เห็นทุกใบ · ยอดเต็ม (unmask) | ☐ |
| 2 | CLICK ใบ pending (d4) | — | ไม่มีปุ่มอนุมัติ (deny) + note "เฉพาะผู้อนุมัติ (DOA)" | ☐ |
| 3 | CLICK ใบ approved (d2) → tab รายละเอียด | — | เห็น hookbox สถานะการจ่าย (จ่าย hook allow · display-only) | ☐ |

### G12 — Edge cases (EC-01..08)

#### TC-EC01 — concurrent approval (EC-01 · ต้อง simulate)
- group: G12 · ความสำคัญ: กลาง · trace: EC-01 · error ERR_STALE_DATA (409)
- actor (role): ผู้อนุมัติ (DOA) × 2
- Setup: role=ผู้อนุมัติ (DOA) · seed=ใบ pending 1 ใบ · files=— · **(ต้อง simulate 2 approver อนุมัติขั้นเดียวกันพร้อมกัน · prototype เป็น single-session → BLOCKED ถ้าจำลองไม่ได้)**
- Start: (backend/2 session)
- ชุดข้อมูล: —
- ผ่านเมื่อ: 2 คน approve พร้อมกัน → first commit สำเร็จ, second → 409 ERR_STALE_DATA (optimistic version)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) 2 approver approve ใบเดียวกันขั้นเดียวกันพร้อมกัน | — | คนแรกสำเร็จ · คนที่สอง error **ERR_STALE_DATA (409)** (version mismatch) — prototype อาจ BLOCKED | ☐ |

#### TC-EC02 — permission mid-flight (EC-02 · ต้อง simulate)
- group: G12 · ความสำคัญ: กลาง · trace: EC-02 · BR-13 · error ERR_NOT_APPROVER/ERR_PERMISSION_REVOKED (403)
- actor (role): ผู้อนุมัติ (DOA) → ถูก demote
- Setup: role=ผู้อนุมัติ (DOA) เปิดใบ pending · **จากนั้นสลับเป็น ผู้เบิก/ธุรการ (จำลอง demote)** · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ใบ pending
- ชุดข้อมูล: —
- ผ่านเมื่อ: re-check canApprove ตอน mutation → หลัง demote กด approve ไม่ได้ (403)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (ผู้อนุมัติ) CLICK ใบ pending | — | footer มีปุ่มอนุมัติ | ☐ |
| 2 | สลับบทบาทเป็น **ผู้เบิก/ธุรการ** (จำลอง demote) แล้ว re-render | — | ปุ่มอนุมัติหายไป · note "เฉพาะผู้อนุมัติ (DOA)" (canApprove re-check · ในระบบจริง = 403 ERR_NOT_APPROVER) | ☐ |

#### TC-EC05 — cancel/แก้ หลังอนุมัติ → ไม่มี path (EC-05 · OQ-05)
- group: G12 · ความสำคัญ: สูง · trace: EC-05 · XT-04 · LD-06 · OQ-05
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d2 (approved) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK EXP-2569-0001
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยืนยัน "ไม่มี" ปุ่ม/transition ยกเลิกหรือแก้หลังอนุมัติ (conservative · reverse EC/release FC ยังไม่ทำ · รอ OQ-05)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY footer ใบ approved | — | ไม่มีปุ่มยกเลิก/แก้/ถอนอนุมัติ (path ไม่มีในระบบ) | ☐ |

#### TC-DI01 — cc = null (Movement ไม่มี assignment · EC-04 · ต้อง simulate)
- group: G12 · ความสำคัญ: ต่ำ · trace: EC-04 · BR-08 · LOCK-06
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=ผู้เบิกที่ไม่มี Movement assignment ณ วันเบิก (cc=null) · files=— · **(ต้อง simulate seed cc=null)**
- Start: OPEN `expense.html` → wizard ขั้น 2 เลือกผู้เบิกที่ cc=null
- ชุดข้อมูล: —
- ผ่านเมื่อ: cc=null → แสดง "—" (ไม่ block · null≠ไม่มี)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate cc=null) SELECT ผู้เบิกที่ไม่มี assignment | — | hookbox ศูนย์ต้นทุนแสดง **—** (dash) · ไม่มี error · ไปต่อได้ | ☐ |

#### TC-HK01 — ยอด > งบ F117 → warn display-only (EC-08 · BR-15 · XT-05)
- group: G12 · ความสำคัญ: กลาง · trace: EC-08 · BR-15 · XT-05 · OQ-EXP-04
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=งบ mock 100,000 · files=—
- Start: OPEN `expense.html` → wizard สร้างใบยอด > 100,000 → ขั้น 5
- ชุดข้อมูล: (อื่นๆ 120,000)
- ผ่านเมื่อ: ขั้น 5 budgetHookHTML เตือนยอดเกินงบ (display-only · ไม่ block ส่ง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบยอด 120,000 → ขั้น 5 | — | budgetHookHTML แสดงงบ F117 mock (100,000) + เตือนเกินงบ | ☐ |
| 2 | VERIFY ไม่ block | — | ยังกด "บันทึกและส่งอนุมัติ" ได้ (warn display-only · ไม่ hard block) | ☐ |

#### TC-HK02 — หมวดสวัสดิการเกินสิทธิ์ F102 → warn display-only (EC-08 · BR-15)
- group: G12 · ความสำคัญ: กลาง · trace: EC-08 · BR-15 · XT-05
- actor (role): ผู้เบิก/ธุรการ
- Setup: role=ผู้เบิก/ธุรการ · seed=สิทธิ์สวัสดิการ mock 5,000 (หมวด รับรอง) · files=—
- Start: OPEN `expense.html` → wizard สร้างใบหมวด รับรอง 6,000 → ขั้น 5
- ชุดข้อมูล: H
- ผ่านเมื่อ: hook F102 เตือนเกินสิทธิ์ (5,000) display-only · ไม่ block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างใบหมวด รับรอง 6,000 → ขั้น 5 | H | hook F102 แสดงสิทธิ์คงเหลือ 5,000 + เตือนเกินสิทธิ์ (display-only) | ☐ |
| 2 | VERIFY ไม่ block | — | ส่งอนุมัติได้ (warn เท่านั้น) | ☐ |

#### TC-MASK01 — mask ยอดใน list + PDF/export ตาม scope (EC-07 · FN-94)
- group: G12 · ความสำคัญ: สูง · trace: EC-07 · FN-94 · AC-16 · LOCK-07
- actor (role): ผู้เบิก/ธุรการ (self=E01)
- Setup: role=ผู้เบิก/ธุรการ · seed=6 docs · files=—
- Start: OPEN `expense.html` (default)
- ชุดข้อมูล: —
- ผ่านเมื่อ: (scope:self ทำให้ผู้เบิกไม่เห็นใบคนอื่น) — ยืนยัน ใบของตน (E01) เห็นเต็ม · เมื่อสลับเป็น mgr/officer ยอดทุกใบ unmask (mask logic ยึด role.mask + isSelf)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (ผู้เบิก/ธุรการ) VERIFY ยอด d2 (ใบของตน E01) | — | ยอดแสดงเต็ม (isSelf → ไม่ mask) | ☐ |
| 2 | CLICK EXP-2569-0001 → tab PDF | — | ตัวเลขในเอกสาร a4 แสดงเต็ม (ใบของตน) | ☐ |
| 3 | สลับ **ผู้อนุมัติ (DOA)** → VERIFY ยอดใบคนอื่น (d4 ธนากร) | — | ยอดเต็ม 66,340 (mgr unmask) — ไม่มี `฿ •••••` | ☐ |

### G13 — Cross-module (XT-01..05)

#### TC-XT01 — อนุมัติครบ → emit 7C FC+EC (ไม่มี AC · XT-01)
- group: G13 · ความสำคัญ: กลาง · trace: XT-01 · FN-19 · BR-07 · LOCK-04
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d3 (รออนุมัติ) · files=— · (7C ปลายทาง = mock · assert จาก toast)
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → อนุมัติ d3
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast ระบุ "บันทึกเข้า 7C ตาม CSQ_BRIEF_F101" (FC+EC) — prototype ไม่มีหน้า 7C → assert จาก toast/สถานะฝั่งต้นทาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อนุมัติ d3 ครบสาย | — | toast **อนุมัติครบสาย · ออกเลข EXP-… · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · ส่งสถานะจ่าย (hook)** (= FC+EC · ไม่มี AC) | ☐ |

#### TC-XT02 — เลือกช่องทางจ่าย → hook display-only ปลายทาง (XT-02)
- group: G13 · ความสำคัญ: กลาง · trace: XT-02 · FN-10/16 · BR-09
- actor (role): เจ้าหน้าที่ (HR/Finance)
- Setup: role=เจ้าหน้าที่ (HR/Finance) · seed=d2 (approved · payroll) + d6 (paid · transfer) · files=—
- Start: OPEN `expense.html` → สลับ **เจ้าหน้าที่ (HR/Finance)**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องทางจ่าย → payDownstream label ต่างตามชนิด (payroll/transfer/PV/petty) · status paid อ่านกลับ · ไม่ auto จ่าย/post

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK d2 (payroll) → tab รายละเอียด | — | hookbox = รอบเงินเดือน (Payroll HK-1) · display-only | ☐ |
| 2 | CLICK d6 (transfer · paid) → tab รายละเอียด | — | hookbox = โอนตรง (Finance) · payHook "โอนแล้ว · 2569-08-28" (อ่านกลับ · ไม่ auto) | ☐ |

#### TC-XT03 — หักลบทดรอง F103 ส่งค่าให้ปลายทาง ไม่ปรับ ledger (XT-03)
- group: G13 · ความสำคัญ: กลาง · trace: XT-03 · FN-18 · BR-11 · LOCK-09
- actor (role): ผู้อนุมัติ (DOA)
- Setup: role=ผู้อนุมัติ (DOA) · seed=d4 (ผู้เบิก E03 · ทดรอง 15,000) · files=—
- Start: OPEN `expense.html` → สลับ **ผู้อนุมัติ (DOA)** → CLICK ธนากร (d4) → tab รายละเอียด
- ชุดข้อมูล: —
- ผ่านเมื่อ: section ทดรองแสดง หักลบ display-only + note ชัดว่า F101 ส่งค่าหักลบให้ F103 (ไม่ปรับ ledger เอง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section เคลียร์เงินทดรอง (d4) | — | ทดรองค้าง 15,000 · ยอดจ่ายสุทธิ = grand − 15,000 · note **F101 ไม่ปรับยอดทดรองเอง · ส่งค่าหักลบให้ F103 · display-only** | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิดไฟล์ `expense.html` ใน browser (prototype client-side · seed DB คงที่ · refresh = คืนค่าเริ่มต้น).
2. **สลับบทบาท** ที่แถบ **"มุมมองสาธิต"** บนสุด: `ผู้เบิก/ธุรการ` · `ผู้อนุมัติ (DOA)` · `เจ้าหน้าที่ (HR/Finance)` — ตาม `Setup: role=` ของแต่ละเคส (default = ผู้เบิก/ธุรการ).
3. ทำตามตาราง step เรียงจากบน — ทุก Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/UPLOAD/PRESS/WAIT/VERIFY).
4. เทียบ **Expected** กับสิ่งที่เห็นจริง → ติ๊ก `☐` (pass) / mark fail + จด evidence (ข้อความจริงที่เห็น).
5. เคสที่ mark **(ต้อง simulate)** (EC-01/EC-02/EC-04/ID01) = prototype single-session อาจทำไม่ได้ → mark `blocked` + note.
6. **overlay ปิดด้วย** Esc / คลิก backdrop / ปุ่มปิด. ทุกเคส refresh-safe — เริ่มจาก Start ใหม่เสมอ (อย่าพึ่งสถานะค้าง; ใบที่สร้างระหว่างเทสหายเมื่อ refresh).
7. ส่งผลกลับตาม **Result Report (schema)** ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (Coverage Manifest · รวม FN-18/19/20) | 25 / 25 |
| Business rules (05_RULES §5.1) | 16 / 16 (BR-01..15 + BR-18 · ไม่มี BR-16/17 ใน pack นี้) |
| Edge cases (EC-01..08) | 8 / 8 |
| Error codes (catalog) | 14 / 17 (ที่เหลือ = auth infra: ERR_NOT_AUTHENTICATED/ERR_INSUFFICIENT_ROLE/ERR_NOT_FOUND — ดูข้าม) |
| Permission cells (สำคัญ · 3 role) | 9 / 9 |
| Cross-cutting / events / states | ครบ (docPill · signprog · empty · 5 event · state transition ถูก+ผิด) |

- Cross-Module (XT): **5 / 5** (XT-01..05)
- Scope Lock (LOCK): **10 / 10** (LOCK-01..10)
- Negatives "ห้ามมี" (unsupported 7 + FN-19 no-AC + no-cancel-after-approval): **9 / 9** (TC-N01..N09)
- **Manifest cross-check (FRD §0.12): ✅ 25/25** (ทุกแถว manifest มีคู่ใน Ledger)

### ข้าม (พร้อมเหตุผล)
- **ERR_NOT_AUTHENTICATED (401)** — prototype ไม่มี login/token (RBAC จริงจาก login · scaffolding demo-strip) → ไม่มีผลสังเกตบน UI.
- **ERR_INSUFFICIENT_ROLE (403 · ผู้เบิกสร้างใบคนอื่น)** — prototype ผูก self=E01 คงที่ · "ธุรการสร้างแทนผู้เบิก" = OQ-04 (รอ RBAC จริง) → ข้าม (ยังไม่มี path).
- **ERR_NOT_FOUND (404)** — record หาย = backend infra · ไม่มีผลบน prototype (seed คงที่).
- **BR-16 / BR-17** — ไม่มีใน 05_RULES ของ F-HR-EXPENSE (เลข BR ข้ามไป BR-18) → ไม่ใช่การหล่น.
- **EC-01 / EC-02 / EC-04 / ID01 (simulate)** — prototype single-session client-side จำลอง concurrent/demote/cc-null/idempotency จริงไม่ได้ครบ → mark `(ต้อง simulate)` · runner backend เป็นผู้ยืนยัน · UI-level ครอบเท่าที่เห็นได้แล้ว.
- **OQ-01 (DOA role-id/ช่วงจริง · CL-0013) · OQ-02 (เพดาน group) · OQ-03 (pay contract) · OQ-04 (RBAC) · OQ-05 (reverse EC)** — config/policy รอ BA/SEC/Finance เคาะ · เทสยึด mock ที่มี + verify "ไม่ hardcode/ไม่มี path" (TC-S01/S03/S04 · TC-N08 · TC-N09/EC05).

---

## Result Report (schema)

```json
{
  "feature_id": "F-HR-EXPENSE",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-W01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 76, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ toast จริง · route/สถานะที่ค้าง · สิ่งที่แสดงแทน Expected) เพื่อ triage โดยไม่ต้องรันซ้ำ. `note` = หมายเหตุเสริม (เช่น "prototype single-session — simulate ไม่ได้").
