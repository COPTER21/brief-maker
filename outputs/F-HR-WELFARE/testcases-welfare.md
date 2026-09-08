# AI Test Cases — F-HR-WELFARE · Welfare (สวัสดิการ)

> **ผู้บริโภคปลายทาง:** AI agent (browser-use / vision) อ่านไฟล์นี้แล้วลงมือทดสอบบน `welfare.html` จริง แล้วกรอกผลกลับตาม schema ท้ายไฟล์.
> ทุก action ขึ้นต้น verb tag · ทุก anchor = ข้อความที่เห็นบนจอ (verbatim จาก welfare.html) · ทุก Expected เช็คได้ด้วยตา.
> **แหล่ง anchor:** welfare.html (source of truth) > 01_UI > microcopy กลาง html-generator-v9. ไม่พบ HTML–FRD drift.
> **[AI-DEFAULT]** ที่หัวเคส = เกณฑ์ที่ AI ตัดสินแทน BA (Lane Mode probe) — ผล fail อาจแปลว่า "default ผิด" ไม่ใช่ "โค้ดผิด" (ดู OQ-04/05).

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-HR-WELFARE (F102) |
| ชื่อ | Welfare — สวัสดิการ |
| เวอร์ชัน FRD | 1.0 (2026-09-08) · Variant FULL |
| App entry / route default | ว่าง/`#/` → redirect `#/welfare/registry` |
| Routes | `#/welfare/registry` · `#/welfare/requests` · `#/welfare/balance` · `#/welfare/report` |
| Overlays | drawer: benefit-create/edit/view · request-create/view · dependent-create · modal: doa · approve · reject · reverse · cancel · archiveBenefit · removeDep |
| ที่มา | FRD Pack (00/01/05/06/07) · BRD_welfare.md · welfare.html (3,268 บรรทัด) · _DECISION_LOG_OQ.md |
| Roles | `qa_admin`(admin) · `qa_manager`(manager) · `qa_employee`(employee, own scope) |
| ปีสิทธิ์ | พ.ศ. 2569 ทั้งไฟล์ |
| จำนวนเคส | **60** (happy 20 · negative 17 · edge 8 · error/validation 8 · permission 7) |

---

## Coverage

| group | เคส | ความสำคัญ |
|---|---|---|
| G1 ทะเบียนสวัสดิการ (registry / benefit type) | TC-REG-01..07 (7) | สูง |
| G2 ผู้ติดตาม (dependent) | TC-DEP-01..04 (4) | กลาง |
| G3 สร้างคำขอ (request-create) | TC-REQ-01..05 (5) | สูง |
| G4 ส่งอนุมัติ DOA (doa slot picker) | TC-DOA-01..02 (2) | สูง |
| G5 อนุมัติ / one-step advance | TC-APR-01..02, TC-ADV-01 (3) | สูง |
| G6 ไม่อนุมัติ (reject) | TC-REJ-01..02 (2) | สูง |
| G7 ยกเลิก (cancel) | TC-CAN-01..02 (2) | กลาง |
| G8 คงเหลือรายคน (balance) | TC-BAL-01..04 (4) | สูง |
| G9 ดูคำขอ (request-view tabs) | TC-VIEW-01..02 (2) | กลาง |
| G10 รายงาน (report) | TC-RPT-01..02 (2) | กลาง |
| G11 list / filter / empty | TC-LIST-01..02 (2) | กลาง |
| G12 validate / double-submit / audit | TC-VAL-01, TC-AUD-01 (2) | สูง |
| G13 masking per role (FN-94) | TC-MASK-01..03 (3) | สูง |
| G14 กลับรายการ (reversal · OQ-WEL-01) | TC-REV-01..04 (4) | สูง |
| G15 exposure display-only (OQ-WEL-03) | TC-EXP-01 (1) | กลาง |
| G16 concurrent re-check ณ อนุมัติ (FIX-02) | TC-CC-01 (1) | สูง |
| G17 permission / governance guards | TC-PERM-01..04 (4) | สูง |
| G18 negative — 5 not-supported (NS-1..5) | TC-NEG-01..05 (5) | สูง |
| G19 cross-module (XT §6.9) | TC-XT-01..05 (5) | สูง |

---

## Coverage Ledger

### FR / Acceptance (06_TESTS §6.1 · AT-01..27)
| item | cases |
|---|---|
| AT-01 (FN-01) สร้างประเภท | TC-REG-01 |
| AT-02 (FN-02) แก้=เวอร์ชันใหม่ / publish draft | TC-REG-03, TC-REG-04 |
| AT-03 (FN-03/91) ปิดใช้ soft archive + เตือนค้าง | TC-REG-05 |
| AT-04 (FN-04) quota≤0 / effective overlap block | TC-REG-06, TC-REG-07 |
| AT-05 (FN-05) เพิ่มผู้ติดตาม | TC-DEP-01 |
| AT-06 (FN-06) บุตรอายุเกิน / ≥3 warning | TC-DEP-02, TC-DEP-04 |
| AT-07 (FN-07) สร้างคำขอ type มีสิทธิ์ + self/dep + แนบไฟล์ | TC-REQ-01, TC-REQ-02 |
| AT-08 (FN-08) ส่งอนุมัติ DOA slot picker | TC-DOA-01, TC-DOA-02 |
| AT-09 (FN-09) ใช้บางส่วน — คงเหลือถูกต้อง | TC-BAL-02 |
| AT-10 (FN-10) ขอเกินคงเหลือ block | TC-REQ-03 |
| AT-11 (FN-11) type ไม่มีสิทธิ์ block+เหตุ | TC-REQ-04, TC-REQ-05 |
| AT-12 (FN-12) ดูสถานะ + สาย DOA (อ่าน) | TC-VIEW-01 |
| AT-13 (FN-13) อนุมัติ final → ตัดคงเหลือ + 7C EC + hook | TC-APR-01 |
| AT-14 (FN-14) ไม่อนุมัติ → ไม่ตัด + เหตุ + NTF | TC-REJ-01, TC-REJ-02 |
| AT-15 (FN-15) ยกเลิกก่อนอนุมัติ | TC-CAN-01, TC-CAN-02 |
| AT-16 (FN-16) leaver→revoked · null≠ทำงาน | TC-BAL-03 |
| AT-17 (FN-17) สถานะจ่าย display-only | TC-VIEW-02 |
| AT-18 (FN-18) joiner→สิทธิ์เปิดอัตโนมัติ | TC-BAL-04 |
| AT-19 (FN-19) รายงาน + filter จริง | TC-RPT-01, TC-RPT-02 |
| AT-20 (FN-90) ค้นหา/filter + empty | TC-LIST-01, TC-LIST-02 |
| AT-21 (FN-92) validate + กัน double-submit | TC-VAL-01 |
| AT-22 (FN-93) audit append-only | TC-AUD-01 |
| AT-23 (FN-94) RESTRICTED masking ตาม role | TC-MASK-01, TC-MASK-02, TC-MASK-03 |
| AT-24 (OQ-WEL-01) กลับรายการ reversal | TC-REV-01, TC-REV-02, TC-REV-03, TC-REV-04 |
| AT-25 (OQ-WEL-03) exposure display-only | TC-EXP-01 |
| AT-26 (FIX-02/EC-07) re-check ณ อนุมัติ (concurrent) | TC-CC-01 |
| AT-27 (FIX-03) one-step advance | TC-ADV-01 |

### 24 FN cross-check (01_FUNCTION_CHECKLIST)
| FN | cases |
|---|---|
| FN-01 | TC-REG-01, TC-REG-02 |
| FN-02 | TC-REG-03, TC-REG-04 |
| FN-03 | TC-REG-05 |
| FN-04 | TC-REG-06, TC-REG-07 |
| FN-05 | TC-DEP-01, TC-DEP-03 |
| FN-06 | TC-DEP-02, TC-DEP-04 |
| FN-07 | TC-REQ-01, TC-REQ-02 |
| FN-08 | TC-DOA-01, TC-DOA-02 |
| FN-09 | TC-BAL-02 |
| FN-10 | TC-REQ-03 |
| FN-11 | TC-REQ-04, TC-REQ-05 |
| FN-12 | TC-VIEW-01 |
| FN-13 | TC-APR-01, TC-ADV-01 |
| FN-14 | TC-REJ-01, TC-REJ-02 |
| FN-15 | TC-CAN-01, TC-CAN-02 |
| FN-16 | TC-BAL-03 |
| FN-17 | TC-VIEW-02 |
| FN-18 | TC-BAL-04 |
| FN-19 | TC-RPT-01, TC-RPT-02 |
| FN-90 | TC-LIST-01, TC-LIST-02 |
| FN-91 | TC-REG-05, TC-CAN-01 |
| FN-92 | TC-VAL-01, TC-REG-02, TC-REJ-01 |
| FN-93 | TC-AUD-01, TC-REV-01 |
| FN-94 | TC-MASK-01, TC-MASK-02, TC-MASK-03 |

**FN cross-check: 24/24 ✅**

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 eligibility ณ วันยื่น | TC-REQ-01, TC-REQ-04, TC-REQ-05, TC-CC-01 |
| BR-02 quota/remaining + re-check ณ อนุมัติ | TC-REQ-03, TC-BAL-02, TC-CC-01 |
| BR-03 effective_date ช่วงไม่ทับ | TC-REG-03, TC-REG-07 |
| BR-04 ผ่าน DOA ก่อนตัด (resolve, no hardcode) | TC-DOA-01 |
| BR-05 ตัดเฉพาะ approved (reject/cancel/revoke/reversed ไม่ตัด) | TC-APR-01, TC-REJ-02, TC-CAN-01, TC-REV-01 |
| BR-06 employment window · null last-day ≠ ไม่มีวันจบ | TC-BAL-03, TC-BAL-04 |
| BR-07 append-only + soft archive + audit | TC-AUD-01, TC-REG-05 |
| BR-08 RESTRICTED masking per role | TC-MASK-01, TC-MASK-02, TC-MASK-03 |
| BR-09 CSQ EC only (welfare.granted) | TC-XT-01, TC-APR-01 |
| BR-10 snapshot ชื่อ/config ณ บันทึก | TC-REQ-01 (สังเกต snapshot ในคำขอ) |
| BR-11 reversal (approved+canApprove+reason+EC reverse+clawback+append-only) | TC-REV-01..04, TC-XT-03, TC-XT-04 |
| BR-12 exposure display-only (no soft-reserve) | TC-EXP-01, TC-CC-01 |
| BR-DOA-1 approve pending-only (FIX-01) | TC-PERM-03 |
| BR-DOA-2 resolve-at-submit + freeze | TC-DOA-01, TC-VIEW-01 |
| BR-DOA-3 one-step advance | TC-ADV-01 |
| BR-DOA-4 re-check at final approval | TC-APR-01, TC-CC-01 |
| BR-DOA-5 soft-reserve = NONE | TC-EXP-01, TC-CC-01 |
| BR-DOA-6 permission (canApprove/canCancel) enforce | TC-PERM-01, TC-PERM-02, TC-PERM-04 |
| BR-DOA-7 cancel scope (draft/pending only) | TC-CAN-01, TC-CAN-02 |
| BR-DOA-8 archive warns pending | TC-REG-05 |
| BR-BAL-1 balance live compute | TC-BAL-02 |
| BR-BAL-2 no negative-clamp in logic (UI clamp 0) | TC-BAL-02 (สังเกต), TC-CC-01 |
| BR-BAL-3 reversed คืนยอดเอง | TC-REV-01 |

### Field Validation (05_RULES §5.4 · VR-01..12)
| VR | cases |
|---|---|
| VR-01 quota ≤0 → BR_QUOTA_INVALID | TC-REG-06 |
| VR-02 eff_from ≤ เดิม → BR_EFFECTIVE_OVERLAP | TC-REG-07 |
| VR-03 groups ว่าง → BR_GROUPS_REQUIRED | TC-REG-02 |
| VR-04 value > คงเหลือ → BR_OVER_BALANCE | TC-REQ-03 |
| VR-05 eligibility นอกกลุ่ม/พ้นสภาพ → BR_NOT_ELIGIBLE | TC-REQ-04, TC-REQ-05 |
| VR-06 บุตร >20 ปี → BR_DEPENDENT_CHILD_AGE | TC-DEP-02 |
| VR-07 dependent ≥3 → warning | TC-DEP-04 |
| VR-08 reject/reverse reason ว่าง → BR_REASON_REQUIRED | TC-REJ-01, TC-REV-02 |
| VR-09 DOA slot ไม่ครบ → BR_DOA_SLOT_INCOMPLETE | TC-DOA-02 |
| VR-10 cancel status ผิด → BR_CANCEL_NOT_ALLOWED | TC-CAN-02 |
| VR-11 reverse status≠approved/!canApprove → BR_REVERSE_NOT_ALLOWED | TC-REV-03 |
| VR-12 double-submit → is-disabled/"กำลัง…" | TC-VAL-01 |

### Error Catalog (05_RULES §5.6)
| error | cases / สถานะ |
|---|---|
| BR_QUOTA_INVALID | TC-REG-06 |
| BR_EFFECTIVE_OVERLAP | TC-REG-07 |
| BR_GROUPS_REQUIRED | TC-REG-02 |
| BR_NOT_ELIGIBLE | TC-REQ-04, TC-REQ-05 |
| BR_NOT_ELIGIBLE_AT_APPROVAL | TC-CC-01 (สาขา eligibility) |
| BR_OVER_BALANCE | TC-REQ-03 |
| BR_OVER_BALANCE_AT_APPROVAL | TC-CC-01 |
| BR_DEPENDENT_CHILD_AGE | TC-DEP-02 |
| BR_DEPENDENT_COUNT (warn) | TC-DEP-04 |
| BR_REASON_REQUIRED | TC-REJ-01, TC-REV-02 |
| BR_DOA_SLOT_INCOMPLETE | TC-DOA-02 |
| BR_APPROVE_PRECONDITION | TC-PERM-03 |
| BR_CANCEL_NOT_ALLOWED | TC-CAN-02 |
| BR_REVERSE_NOT_ALLOWED | TC-REV-03 |
| ERR_INSUFFICIENT_ROLE | TC-PERM-01, TC-PERM-02, TC-PERM-04 |
| ERR_STALE_DATA (409, optimistic lock) | TC-CC-01 — mark `(ต้อง simulate)` (backend concurrent · OQ-04) |
| ERR_PERMISSION_REVOKED (EC-09) | — ข้าม (backend mid-flight demote · ไม่มีผลสังเกตบน prototype UI · `[AI-DEFAULT]` OQ-05) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY (EC-08) | — ข้าม (backend idempotency-key · prototype ตรวจได้แค่ UI lockBtn = TC-VAL-01) |
| ERR_VALIDATION_FAILED / ERR_NOT_AUTHENTICATED / ERR_NOT_FOUND | — ข้าม (generic HTTP · ไม่มี trigger เฉพาะบน UI) |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases |
|---|---|
| admin: ทะเบียน CRUD = allow | TC-REG-01, TC-REG-03, TC-REG-05 |
| manager/employee: ทะเบียน CRUD = deny | TC-PERM-04 |
| admin/manager: อนุมัติ/ไม่อนุมัติ = allow | TC-APR-01, TC-REJ-02 |
| employee: อนุมัติ = deny (ปุ่มไม่ปรากฏ) | TC-PERM-01 |
| admin/manager: กลับรายการ = allow | TC-REV-01 |
| employee: กลับรายการ = deny | TC-PERM-02, TC-REV-03 |
| owner/admin: cancel = allow · อื่น = deny | TC-CAN-01, TC-CAN-02 |
| canSeeValue/canSeePerson = admin\|manager | TC-MASK-01, TC-MASK-02, TC-MASK-03 |
| canSeeDependent = admin เท่านั้น | TC-MASK-02, TC-MASK-03 |
| รายงาน = admin/manager | TC-RPT-01 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 leaver ระหว่างค้าง · null≠ทำงาน | TC-BAL-03, TC-BAL-04 |
| EC-02 eligibility ผิดกลุ่ม/ช่วง block พร้อมเหตุ | TC-REQ-04, TC-REQ-05 |
| EC-03 ใช้บางส่วน คงเหลือถูก | TC-BAL-02 |
| EC-04 ขอเกินคงเหลือ block+ยอด | TC-REQ-03 |
| EC-05 ปิดใช้ type มีคำขอค้าง → เตือนจำนวน | TC-REG-05 |
| EC-06 กลับรายการหลัง pay=sent → clawback | TC-REV-04, TC-XT-04 |
| EC-07 concurrent over-quota (`[AI-DEFAULT]` OQ-04) | TC-CC-01 (ต้อง simulate) |
| EC-08 idempotency double-click (`[AI-DEFAULT]`) | TC-VAL-01 (UI lock) · backend ข้าม |
| EC-09 permission mid-flight (`[AI-DEFAULT]` OQ-05) | — ข้าม (backend only) |
| EC-10 approver ลาออกกลางสาย | — ข้าม (OQ-02 · re-resolve = OQ) |
| EC-11 reverse ซ้ำ (reversed กลับไม่ได้) | TC-REV-03 (โดยเจตนา) |
| EC-12 fiscal ปีสิทธิ์คร่อมปฏิทิน | — ข้าม (อ้าง HR Config A-WEL-05 · Phase B) |
| EC-13 HR Config company_scope ไม่ตรง | — ข้าม (OQ-03 Phase B contract) |
| EC-14 attachment ชนิด/ขนาด/virus | — ข้าม (mock · deferred to impl §7.5) |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | case |
|---|---|---|
| XT-01 approve → CSQ EC only (welfare.granted) | TC-XT-01 |
| XT-02 approve → Payroll pay=pending display-only | TC-XT-02 |
| XT-03 reverse → CSQ EC reverse (negative offset) | TC-XT-03 |
| XT-04 reverse pay=sent → payroll_clawback=true | TC-XT-04 |
| XT-05 state transitions → 5 NTF events (DOA ไม่ซ้ำ) | TC-XT-05 |

### Scope Lock (07_LOCKED §7.0 · LK-1..6) — ต้องมีเคส verify
| LOCK | ข้อยืนยัน (ย่อ) | case verify |
|---|---|---|
| LK-1 | DOA resolve slot picker · ห้าม hardcode chain | TC-DOA-01 |
| LK-2 | ไม่จ่ายเงินเอง · Welfare = hook display-only | TC-VIEW-02, TC-NEG-01 |
| LK-3 | policy/effective/company_scope = HR Config · ไม่ทำหน้า config | TC-NEG-04 |
| LK-4 | soft reference snapshot (ไม่มี FK cascade) | TC-REQ-01, TC-REG-05 (คำขอเก่ายังอ่านได้) |
| LK-5 | audit append-only · masking · no hard delete | TC-AUD-01, TC-REV-01, TC-MASK-01 |
| LK-6 | CSQ = EC เท่านั้น (ห้าม OC/DC/SC) | TC-XT-01, TC-XT-03 |

### Out of Scope (Scope Lock R11 Exclusions · NS-1..5) — negative verify (ต้องพิสูจน์ว่าไม่มี)
| NS | ของที่ห้ามมี | case |
|---|---|---|
| NS-1 จ่ายเงินจริง/เบิก/หักเงินเดือน | TC-NEG-01 |
| NS-2 จัดการผู้ให้บริการ (รพ./ประกัน) | TC-NEG-02 |
| NS-3 flex credits / แต้ม | TC-NEG-03 |
| NS-4 สร้าง/แก้ค่านโยบาย HR กลาง | TC-NEG-04 |
| NS-5 ออกเอกสารเลขรัน/PDF ทางการ | TC-NEG-05 |

### States (UI)
| state | case |
|---|---|
| empty request list | TC-LIST-02 |
| filtered-empty report | TC-RPT-02 |
| balance empty (ยังไม่เลือกคน) | TC-BAL-01 |
| leaver note | TC-BAL-03 |
| no-eligible group | TC-REQ-04 (สาขา) |
| loaded | ทุกเคส happy |

### Events (business)
| event | case |
|---|---|
| welfare_request_submitted | TC-DOA-01 (toast "แจ้งเตือน HR อัตโนมัติ") |
| welfare_request_result | TC-APR-01, TC-REJ-02 |
| welfare_request_reversed | TC-REV-01 |
| welfare_quota_near_limit / welfare_eligibility_ended | TC-XT-05 (สังเกตเท่าที่ UI เห็น) |

---

## Data Sets

### ชุด A — ประเภทสวัสดิการ (benefit type · admin สร้าง)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อสวัสดิการ | ประกันอุบัติเหตุกลุ่ม |
| หมวด | ประกัน |
| หน่วยนับ | เงิน (บาท/ปี) |
| โควตา/วงเงินต่อปี | 15000 |
| กลุ่มพนักงานที่มีสิทธิ์ | พนักงานประจำ (เลือก ≥1) |
| วันมีผล (effFrom) | 1 ม.ค. 2569 |

### ชุด A-BAD — ชุดผิดสำหรับ negative
| ฟิลด์ | ค่า | ใช้กับ |
|---|---|---|
| โควตา = 0 | 0 | TC-REG-06 (VR-01) |
| กลุ่ม = ไม่เลือกเลย | (ว่าง) | TC-REG-02 (VR-03) |
| effFrom (edit) ≤ เวอร์ชันเดิม | 1 ม.ค. 2568 | TC-REG-07 (VR-02) |

### ชุด B — คำขอใช้สิทธิ์ (self · happy)
| ฟิลด์ | ค่า |
|---|---|
| พนักงานผู้ยื่น | พนักงานประจำที่มีคงเหลือ >0 (seed S-01) |
| ผู้ใช้สิทธิ์ | ตนเอง (self) |
| ประเภทสวัสดิการ | ประกันสุขภาพ (มีสิทธิ์ · โควตา 30,000/ปี) |
| วันที่ใช้สิทธิ์ | 15 มิ.ย. 2569 |
| มูลค่าที่ขอใช้ (บาท) | 5000 |
| เหตุผล / รายละเอียด | ค่ารักษาพยาบาลผู้ป่วยนอก |
| แนบหลักฐาน | receipt_opd.pdf (mock upload) |

### ชุด B-DEP — คำขอสำหรับผู้ติดตาม
| ฟิลด์ | ค่า |
|---|---|
| พนักงานผู้ยื่น | seed S-02 (มีผู้ติดตาม 2 คน) |
| ผู้ใช้สิทธิ์ | ผู้ติดตาม → เลือกบุตร |
| ประเภทสวัสดิการ | ค่าเล่าเรียนบุตร (20,000/ปี) |
| มูลค่าที่ขอใช้ | 8000 |

### ชุด B-OVER — ขอเกินคงเหลือ (negative)
| ฟิลด์ | ค่า |
|---|---|
| ประเภท | ประกันสุขภาพ · คงเหลือ seed = 5,000 |
| มูลค่าที่ขอใช้ | 9000 (> คงเหลือ) |

### ชุด C — ผู้ติดตาม (dependent · admin เพิ่ม)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อ | ด.ช. ก้อง ใจดี |
| ความสัมพันธ์ | บุตร |
| วันเกิด (dob) | 10 พ.ค. 2560 (อายุ ~9 ปี · ผ่าน) |

### ชุด C-BAD — บุตรอายุเกิน (negative)
| ฟิลด์ | ค่า |
|---|---|
| ความสัมพันธ์ | บุตร |
| วันเกิด (dob) | 1 ม.ค. 2545 (อายุ >20 ปี) |

### ชุด D — เหตุผล reject / reverse
| ฟิลด์ | ค่า |
|---|---|
| เหตุผลไม่อนุมัติ | เอกสารหลักฐานไม่ครบ |
| เหตุผลกลับรายการ | อนุมัติผิดคน — ตั้งกลับรายการ |

### ไฟล์ทดสอบ (Files)
| ชื่อไฟล์ | ใช้กับ | หมายเหตุ |
|---|---|---|
| receipt_opd.pdf | TC-REQ-01 | prototype ใช้ `mockUpload()` (คลิก upload-zone = แนบไฟล์ mock อัตโนมัติ · runner ไม่ต้องมีไฟล์จริง) |

### Seed (สรุป · จาก 06_TESTS §6.3)
- **S-01** พนักงานประจำ มีคงเหลือ ประกันสุขภาพ >0 · **S-02** พนักงานมีผู้ติดตาม 2 คน · **S-08** คำขอ approved บางส่วน · **S-09** คำขอ/สิทธิ์เกินวงเงิน · **S-11** คำขอ rejected · **S-13** พนักงานกำลังพ้นสภาพ (last_day set) · **S-14** คำขอ approved + pay=sent · **S-15** joiner (last_day=null) · **3 กลุ่ม:** ประจำ / ทดลองงาน(สิทธิ์จำกัด) / รายวัน(ไม่มีสิทธิ์บางตัว).

---

## Test Cases

### G1 — ทะเบียนสวัสดิการ (registry)

#### TC-REG-01 — สร้างประเภทสวัสดิการครบฟิลด์ (happy)
- group: registry · ความสำคัญ: สูง · trace: FN-01 / AT-01 / BR-03 / event audit
- actor (role): admin
- Setup: role=qa_admin · seed=มี ≥1 กลุ่มพนักงาน (ประจำ) · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: A
- ผ่านเมื่อ: drawer ปิด + toast **"สร้างประเภทสวัสดิการสำเร็จ"** + แถวใหม่ในตาราง สถานะ pill "ใช้งาน/มีผล"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` | — | tab **ทะเบียนสวัสดิการ** active · ตารางหัวคอลัมน์ **ชื่อสวัสดิการ / หมวด / โควตา-วงเงินต่อปี / กลุ่มที่มีสิทธิ์ / วันมีผล / สถานะ / จัดการ** | ☐ |
| 2 | CLICK ปุ่ม **"สร้างประเภทสวัสดิการ"** | — | drawer เปิด หัวข้อ **"สร้างประเภทสวัสดิการ"** | ☐ |
| 3 | TYPE → ช่อง **ชื่อสวัสดิการ** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | SELECT/TYPE → **หมวด** + **หน่วยนับ** | A (ประกัน · เงิน) | ค่าแสดงตามเลือก | ☐ |
| 5 | TYPE → **โควตา/วงเงินต่อปี** | A: 15000 | ช่องแสดง 15000 | ☐ |
| 6 | TOGGLE → **กลุ่มพนักงานที่มีสิทธิ์** (พนักงานประจำ) | A | checkbox กลุ่มถูกติ๊ก | ☐ |
| 7 | SELECT → **วันมีผล** | A: 1 ม.ค. 2569 | ช่องวันที่แสดงค่า | ☐ |
| 8 | CLICK ปุ่มยืนยัน (footer drawer) | — | drawer ปิด + toast **"สร้างประเภทสวัสดิการสำเร็จ"** | ☐ |
| 9 | VERIFY แถวในตาราง | — | เห็นแถว "ประกันอุบัติเหตุกลุ่ม" · โควตา 15,000 · pill สถานะสีเขียว/ฟ้า (ใช้งาน) | ☐ |

#### TC-REG-02 — สร้างประเภทเว้นช่องบังคับ (negative · validation)
- group: registry · ความสำคัญ: สูง · trace: FN-01/FN-92 / VR-03 / BR_GROUPS_REQUIRED
- actor (role): admin
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: A-BAD (กลุ่ม=ว่าง)
- ผ่านเมื่อ: บันทึกไม่ผ่าน + error ใต้ช่องกลุ่ม **"เลือกอย่างน้อย 1 กลุ่ม"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` → CLICK **"สร้างประเภทสวัสดิการ"** | — | drawer เปิด | ☐ |
| 2 | TYPE → **ชื่อสวัสดิการ** + โควตา 15000 | A | ค่าแสดง (แต่ไม่ติ๊กกลุ่มใด ๆ) | ☐ |
| 3 | CLICK ปุ่มยืนยัน | — | drawer **ไม่ปิด** · error ใต้ **กลุ่มพนักงานที่มีสิทธิ์** = **"เลือกอย่างน้อย 1 กลุ่ม"** | ☐ |

#### TC-REG-03 — แก้ประเภท active = ออกเวอร์ชันใหม่ (happy)
- group: registry · ความสำคัญ: สูง · trace: FN-02 / AT-02 / BR-03
- actor (role): admin
- Setup: role=qa_admin · seed=ประเภทหนึ่งมีเวอร์ชัน active (effFrom 1 ม.ค. 2569) · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: effFrom ใหม่ = 1 ก.ค. 2569
- ผ่านเมื่อ: toast **"บันทึกการแก้ไข (ออกเวอร์ชันใหม่) แล้ว"** · เวอร์ชันเก่ากลายเป็น archived/superseded

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` → CLICK แถว/ไอคอน **แก้** ของประเภท active | — | drawer หัวข้อ **"แก้ไขประเภทสวัสดิการ"** เปิด · แสดง "WEL · <code>" | ☐ |
| 2 | SELECT → **วันมีผล** = 1 ก.ค. 2569 (หลังเดิม) | 1 ก.ค. 2569 | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** | — | drawer ปิด + toast **"บันทึกการแก้ไข (ออกเวอร์ชันใหม่) แล้ว"** | ☐ |
| 4 | OPEN drawer **ดู** ประเภทนั้น → tab เวอร์ชัน | — | เห็น 2 เวอร์ชัน: ใหม่ active + เก่า archived (มี effTo = วันก่อนหน้า) | ☐ |

#### TC-REG-04 — เผยแพร่ประเภท draft (draft → มีผล)
- group: registry · ความสำคัญ: กลาง · trace: FN-02 / AT-02
- actor (role): admin
- Setup: role=qa_admin · seed=ประเภทสถานะ draft (ร่าง) ≥1 · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast **"เผยแพร่ประเภทสวัสดิการแล้ว (ร่าง → มีผล)"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` → CLICK **แก้** ของประเภทที่ pill = **ร่าง** (เทา) | — | drawer แก้ไขเปิด | ☐ |
| 2 | CLICK ปุ่ม **บันทึกการแก้ไข** | — | drawer ปิด + toast **"เผยแพร่ประเภทสวัสดิการแล้ว (ร่าง → มีผล)"** | ☐ |
| 3 | VERIFY แถวในตาราง | — | pill เปลี่ยนจาก **ร่าง** → สถานะมีผล | ☐ |

#### TC-REG-05 — ปิดใช้ประเภทที่มีคำขอค้าง — เตือนจำนวน + soft archive (edge: EC-05)
- group: registry · ความสำคัญ: สูง · trace: FN-03/FN-91 / AT-03 / BR-07 / BR-DOA-8 / LK-4/LK-5
- actor (role): admin
- Setup: role=qa_admin · seed=ประเภทที่มีคำขอ pending อ้างอยู่ ≥1 ใบ · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal เตือนจำนวนใบค้าง → ยืนยัน → toast **"ปิดใช้ (เก็บถาวร) แล้ว"** · คำขอเก่ายังเปิดอ่านได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` → CLICK ไอคอน **ปิดใช้ (เก็บถาวร)** (power-off) ท้ายแถวประเภทที่มีคำขอค้าง | — | modal หัวข้อ **"ปิดใช้ประเภทสวัสดิการ?"** เปิด · ข้อความ soft archive "…เก็บถาวร (soft archive) — คำขอเก่ายังอ่านได้ ไม่มีการลบข้อมูล" + **เตือนจำนวนใบค้าง** | ☐ |
| 2 | CLICK ปุ่ม **ปิดใช้** (danger) | — | modal ปิด + toast **"ปิดใช้ (เก็บถาวร) แล้ว"** | ☐ |
| 3 | VERIFY แถวประเภทนั้น | — | pill = **เก็บถาวร** (เทา) · ยังอยู่ในตาราง (ไม่ถูกลบ) | ☐ |
| 4 | OPEN `#/welfare/requests` → CLICK คำขอเก่าที่อ้างประเภทนั้น | — | drawer คำขอเปิดอ่านได้ปกติ (soft ref · LK-4) | ☐ |

#### TC-REG-06 — โควตา ≤ 0 → บล็อก (negative · boundary)
- group: registry · ความสำคัญ: สูง · trace: FN-04 / AT-04 / VR-01 / BR_QUOTA_INVALID
- actor (role): admin
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: A + A-BAD (โควตา=0)
- ผ่านเมื่อ: error **"โควตา/วงเงินต้องมากกว่า 0"** · บันทึกไม่ผ่าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` → CLICK **"สร้างประเภทสวัสดิการ"** | — | drawer เปิด | ☐ |
| 2 | TYPE → ชื่อ + ติ๊กกลุ่ม + หน่วยนับ = เงิน | A | ค่าแสดง | ☐ |
| 3 | TYPE → **โควตา/วงเงินต่อปี** = 0 | A-BAD | ช่องแสดง 0 | ☐ |
| 4 | CLICK ปุ่มยืนยัน | — | drawer ไม่ปิด · error **"โควตา/วงเงินต้องมากกว่า 0"** (BR_QUOTA_INVALID) | ☐ |

#### TC-REG-07 — วันมีผลเวอร์ชันใหม่ ≤ เดิม → ช่วงทับ บล็อก (negative)
- group: registry · ความสำคัญ: สูง · trace: FN-04/FN-02 / AT-04 / VR-02 / BR-03 / BR_EFFECTIVE_OVERLAP
- actor (role): admin
- Setup: role=qa_admin · seed=ประเภท active effFrom 1 ม.ค. 2569 · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: A-BAD (effFrom edit = 1 ม.ค. 2568)
- ผ่านเมื่อ: error **"…ช่วงมีผลทับกันไม่ได้"** · บันทึกไม่ผ่าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` → CLICK **แก้** ประเภท active | — | drawer แก้ไขเปิด | ☐ |
| 2 | SELECT → **วันมีผล** = 1 ม.ค. 2568 (≤ เดิม) | A-BAD | ช่องแสดงค่า | ☐ |
| 3 | CLICK **บันทึกการแก้ไข** | — | drawer ไม่ปิด · error **"วันมีผลของเวอร์ชันใหม่ต้องหลัง … — ช่วงมีผลทับกันไม่ได้"** (BR_EFFECTIVE_OVERLAP) | ☐ |

---

### G2 — ผู้ติดตาม (dependent)

#### TC-DEP-01 — เพิ่มผู้ติดตาม (happy)
- group: dependent · ความสำคัญ: กลาง · trace: FN-05 / AT-05
- actor (role): admin
- Setup: role=qa_admin · seed=พนักงาน 1 คน (S-01) · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: C
- ผ่านเมื่อ: toast **"เพิ่มผู้ติดตามแล้ว"** · ชื่อผู้ติดตามปรากฏใน sub-list

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือกพนักงานใน combobox | S-01 | แสดงตารางสิทธิ์ + sub-list ผู้ติดตาม + ปุ่ม **เพิ่มผู้ติดตาม** | ☐ |
| 2 | CLICK ปุ่ม **เพิ่มผู้ติดตาม** | — | drawer หัวข้อ **"เพิ่มผู้ติดตาม"** (ของ <ชื่อพนักงาน>) เปิด | ☐ |
| 3 | TYPE → **ชื่อ** + SELECT **ความสัมพันธ์** = บุตร | C | ค่าแสดง | ☐ |
| 4 | SELECT → **วันเกิด** = 10 พ.ค. 2560 | C | ช่องแสดงค่า (อายุ ~9 ปี · ผ่าน) | ☐ |
| 5 | CLICK ปุ่มยืนยัน | — | drawer ปิด + toast **"เพิ่มผู้ติดตามแล้ว"** | ☐ |
| 6 | VERIFY sub-list ผู้ติดตาม | — | เห็น "ด.ช. ก้อง ใจดี · บุตร" | ☐ |

#### TC-DEP-02 — บุตรอายุ > 20 ปี → บล็อก (negative)
- group: dependent · ความสำคัญ: กลาง · trace: FN-06 / AT-06 / VR-06 / BR_DEPENDENT_CHILD_AGE
- actor (role): admin
- Setup: role=qa_admin · seed=พนักงาน 1 คน · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: C-BAD (dob 1 ม.ค. 2545)
- ผ่านเมื่อ: error/บล็อก **"บุตรอายุเกิน 20 ปี — เกินเกณฑ์กลุ่ม"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือกพนักงาน → CLICK **เพิ่มผู้ติดตาม** | — | drawer เปิด | ☐ |
| 2 | TYPE ชื่อ + SELECT ความสัมพันธ์ = **บุตร** + วันเกิด 1 ม.ค. 2545 | C-BAD | ค่าแสดง | ☐ |
| 3 | CLICK ปุ่มยืนยัน | — | บันทึกไม่ผ่าน · แสดง **"บุตรอายุเกิน 20 ปี — เกินเกณฑ์กลุ่ม"** (BR_DEPENDENT_CHILD_AGE) | ☐ |

#### TC-DEP-03 — ลบผู้ติดตาม (happy)
- group: dependent · ความสำคัญ: ต่ำ · trace: FN-05 / M-07
- actor (role): admin
- Setup: role=qa_admin · seed=พนักงานมีผู้ติดตาม ≥1 (S-02) · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ยืนยัน → ผู้ติดตามหายจาก sub-list

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือก S-02 | — | sub-list แสดงผู้ติดตาม 2 คน | ☐ |
| 2 | CLICK ไอคอนลบ ท้ายแถวผู้ติดตามคนหนึ่ง | — | modal ยืนยันการลบผู้ติดตามเปิด | ☐ |
| 3 | CLICK ปุ่มยืนยันลบ | — | modal ปิด · sub-list เหลือผู้ติดตาม 1 คน | ☐ |

#### TC-DEP-04 — ผู้ติดตาม ≥ 3 คน → เตือน (non-block · warning)
- group: dependent · ความสำคัญ: ต่ำ · trace: FN-06 / AT-06 / VR-07 / BR_DEPENDENT_COUNT
- actor (role): admin
- Setup: role=qa_admin · seed=พนักงานมีผู้ติดตามอยู่ 2 คน · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: C (เพิ่มเป็นคนที่ 3)
- ผ่านเมื่อ: เพิ่มได้ (non-block) + มี **warning เตือนเกินเกณฑ์** ปรากฏ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือกพนักงานที่มีผู้ติดตาม 2 → CLICK **เพิ่มผู้ติดตาม** | — | drawer เปิด | ☐ |
| 2 | TYPE ผู้ติดตามคนที่ 3 (dob valid) | C | ค่าแสดง | ☐ |
| 3 | CLICK ยืนยัน | — | เพิ่ม**สำเร็จ** (toast "เพิ่มผู้ติดตามแล้ว") + warning เตือนจำนวนผู้ติดตามเกินเกณฑ์ (ไม่บล็อก) | ☐ |

---

### G3 — สร้างคำขอ (request-create)

#### TC-REQ-01 — สร้างคำขอ self + แนบไฟล์ (happy · แสดง "มีสิทธิ์")
- group: request-create · ความสำคัญ: สูง · trace: FN-07 / AT-07 / BR-01 / BR-10 / LK-4
- actor (role): employee
- Setup: role=qa_employee · seed=S-01 มีคงเหลือ ประกันสุขภาพ >0 · files=receipt_opd.pdf (mockUpload)
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: B
- ผ่านเมื่อ: combobox type แสดงป้าย "มีสิทธิ์" + note **"มีสิทธิ์ · คงเหลือ …"** · ส่งได้ (ต่อไป modal doa)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK ปุ่ม **"สร้างคำขอใช้สิทธิ์"** | — | drawer หัวข้อ **"สร้างคำขอใช้สิทธิ์"** เปิด | ☐ |
| 2 | SELECT → **พนักงานผู้ยื่น** (combobox) | B | avatar+ชื่อ+ตำแหน่ง แสดง | ☐ |
| 3 | CLICK segment **ผู้ใช้สิทธิ์** = ตนเอง (self) | B | segment "ตนเอง" active | ☐ |
| 4 | SELECT → **ประเภทสวัสดิการ (เฉพาะที่มีสิทธิ์ ณ วันยื่น)** = ประกันสุขภาพ | B | option แสดงป้าย **"มีสิทธิ์"** · เลือกได้ | ☐ |
| 5 | SELECT **วันที่ใช้สิทธิ์** + TYPE **มูลค่าที่ขอใช้ (บาท)** = 5000 | B | note **"มีสิทธิ์ · คงเหลือ … (ปีสิทธิ์ 2569) — ตัดคงเหลือเมื่ออนุมัติเท่านั้น"** (สีเขียว) | ☐ |
| 6 | CLICK **upload-zone** (คลิกเพื่อแนบไฟล์หลักฐาน) | receipt_opd.pdf | ไฟล์ปรากฏใน req-files (mock) | ☐ |
| 7 | VERIFY ปุ่ม **ส่งอนุมัติ** | — | ปุ่ม enable (ไม่ is-disabled) เพราะ note ไม่ใช่ danger | ☐ |

#### TC-REQ-02 — สร้างคำขอสำหรับผู้ติดตาม (happy)
- group: request-create · ความสำคัญ: สูง · trace: FN-07 / AT-07
- actor (role): employee
- Setup: role=qa_employee · seed=S-02 มีผู้ติดตาม (บุตร) + สิทธิ์ค่าเล่าเรียนบุตร · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: B-DEP
- ผ่านเมื่อ: เลือก "ผู้ติดตาม" → combobox ผู้ติดตามปรากฏ → เลือกบุตร → note มีสิทธิ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK **"สร้างคำขอใช้สิทธิ์"** | — | drawer เปิด | ☐ |
| 2 | SELECT พนักงานผู้ยื่น = S-02 | B-DEP | แสดง | ☐ |
| 3 | CLICK segment **ผู้ใช้สิทธิ์** = ผู้ติดตาม | B-DEP | combobox **เลือกผู้ติดตาม** ปรากฏใต้ segment | ☐ |
| 4 | SELECT → ผู้ติดตาม = บุตร | B-DEP | ค่าแสดง | ☐ |
| 5 | SELECT ประเภท = **ค่าเล่าเรียนบุตร** + TYPE มูลค่า 8000 | B-DEP | note "มีสิทธิ์ · คงเหลือ …" | ☐ |
| 6 | VERIFY ปุ่ม ส่งอนุมัติ | — | enable | ☐ |

#### TC-REQ-03 — ขอเกินคงเหลือ → ปุ่มส่ง disable + note danger (negative · edge: EC-04)
- group: request-create · ความสำคัญ: สูง · trace: FN-10 / AT-10 / VR-04 / BR_OVER_BALANCE
- actor (role): employee
- Setup: role=qa_employee · seed=สิทธิ์ประกันสุขภาพคงเหลือ 5,000 (S-09/บางส่วนใช้แล้ว) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: B-OVER (ขอ 9000 > คงเหลือ 5000)
- ผ่านเมื่อ: note danger **"เกินคงเหลือ: …"** + ปุ่ม ส่งอนุมัติ is-disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK **"สร้างคำขอใช้สิทธิ์"** | — | drawer เปิด | ☐ |
| 2 | SELECT พนักงาน + self + ประเภท ประกันสุขภาพ | B-OVER | note มีสิทธิ์แสดง คงเหลือ 5,000 | ☐ |
| 3 | TYPE **มูลค่าที่ขอใช้** = 9000 | B-OVER | note เปลี่ยนเป็น danger **"เกินคงเหลือ: คงเหลือ 5,000 บาท — ขอใช้เกินสิทธิ์ ตัดคงเหลือไม่ได้"** | ☐ |
| 4 | VERIFY ปุ่ม **ส่งอนุมัติ** | — | ปุ่มมีคลาส **is-disabled** (กดไม่ได้) | ☐ |
| 5 | CLICK ปุ่ม ส่งอนุมัติ (ทดสอบ) | — | ไม่ส่ง / toast **"ยื่นไม่ได้: เกินคงเหลือ"** (ถ้ากดผ่าน guard) | ☐ |

#### TC-REQ-04 — ยื่น type ที่กลุ่มไม่มีสิทธิ์ → บล็อก + เหตุ (negative · edge: EC-02)
- group: request-create · ความสำคัญ: สูง · trace: FN-11 / AT-11 / VR-05 / BR-01 / BR_NOT_ELIGIBLE
- actor (role): employee
- Setup: role=qa_employee · seed=พนักงานกลุ่ม "รายวัน" (ไม่มีสิทธิ์บางตัว) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: note danger **"ยื่นไม่ได้: กลุ่ม … ไม่มีสิทธิ์ในประเภทนี้"** (ไม่บล็อกเงียบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK **"สร้างคำขอใช้สิทธิ์"** | — | drawer เปิด | ☐ |
| 2 | SELECT พนักงานกลุ่มรายวัน + self | — | แสดง | ☐ |
| 3 | SELECT ประเภทที่กลุ่มนั้นไม่มีสิทธิ์ | — | note danger **"ยื่นไม่ได้: กลุ่มพนักงาน "รายวัน …" ไม่มีสิทธิ์ในประเภทนี้"** + ปุ่มส่ง is-disabled | ☐ |

#### TC-REQ-05 — ยื่นเมื่อพ้นสภาพ (leaver) → บล็อก + เหตุ (negative)
- group: request-create · ความสำคัญ: สูง · trace: FN-11 / AT-11 / VR-05 / BR-06 / BR_NOT_ELIGIBLE
- actor (role): employee
- Setup: role=qa_employee · seed=S-13 พนักงานพ้นสภาพ (last_day set) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: note danger เหตุ **"พนักงานพ้นสภาพแล้ว (leaver) — สิทธิ์สิ้นสุด ยื่นคำขอไม่ได้"** (หรือข้อความ eligibility ทำนองเดียวกัน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK **"สร้างคำขอใช้สิทธิ์"** | — | drawer เปิด | ☐ |
| 2 | SELECT พนักงาน = S-13 (leaver) + self + type ใด ๆ | — | note danger **"ยื่นไม่ได้: พนักงานพ้นสภาพ…"** + ปุ่มส่ง is-disabled | ☐ |

---

### G4 — ส่งอนุมัติ DOA (slot picker)

#### TC-DOA-01 — ส่งอนุมัติ เลือกสาย DOA ครบ 2 ขั้น (happy · LK-1)
- group: doa · ความสำคัญ: สูง · trace: FN-08 / AT-08 / BR-04 / BR-DOA-2 / LK-1 / event submitted
- actor (role): employee (ผู้ยื่น)
- Setup: role=qa_employee · seed=คำขอ draft ของตน ≥1 (หรือสร้างต่อจาก TC-REQ-01) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal doa มี 2 slot + note "GET /doa/resolve" → เลือกครบ → toast **"ส่งอนุมัติแล้ว · แจ้งเตือน HR อัตโนมัติ"** · pill เป็น รออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ draft → CLICK ปุ่ม **ส่งอนุมัติ** (หรือส่งจาก drawer create) | — | modal หัวข้อ **"ส่งอนุมัติคำขอ …"** เปิด · subtitle "เลือกผู้อนุมัติแต่ละขั้น (สายจาก DOA · ไม่มีวงเงิน · resolve แล้ว freeze)" | ☐ |
| 2 | VERIFY โครงสร้าง modal | — | มี **2 slot** (ขั้น 1 / ขั้น 2) แต่ละ slot = combobox **"เลือกผู้อนุมัติในตำแหน่งนี้"** + note **"สายอนุมัติมาจาก DOA กลาง (GET /doa/resolve) — เลือก "คน" … ไม่ hardcode"** | ☐ |
| 3 | SELECT → ผู้อนุมัติ ขั้น 1 (หัวหน้า) | — | slot 1 แสดงคนที่เลือก | ☐ |
| 4 | SELECT → ผู้อนุมัติ ขั้น 2 (HR) | — | slot 2 แสดงคนที่เลือก | ☐ |
| 5 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal ปิด + toast **"ส่งอนุมัติแล้ว · แจ้งเตือน HR อัตโนมัติ"** | ☐ |
| 6 | VERIFY แถวคำขอ | — | pill สถานะ = **รออนุมัติ** (เหลือง) | ☐ |

#### TC-DOA-02 — ส่งอนุมัติ เลือก slot ไม่ครบ → บล็อก (negative)
- group: doa · ความสำคัญ: สูง · trace: FN-08 / AT-08 / VR-09 / BR_DOA_SLOT_INCOMPLETE
- actor (role): employee
- Setup: role=qa_employee · seed=คำขอ draft ≥1 · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast/warning **"เลือกผู้อนุมัติให้ครบทุกขั้น"** · ไม่ส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → เปิด modal doa (ส่งอนุมัติ) | — | modal 2 slot เปิด | ☐ |
| 2 | SELECT → ผู้อนุมัติ **เฉพาะขั้น 1** (เว้นขั้น 2) | — | slot 2 ยังว่าง | ☐ |
| 3 | CLICK ปุ่ม **ส่งอนุมัติ** | — | toast warning **"เลือกผู้อนุมัติให้ครบทุกขั้น"** · modal ไม่ปิด | ☐ |

---

### G5 — อนุมัติ / one-step advance

#### TC-APR-01 — อนุมัติขั้นสุดท้าย → ตัดคงเหลือ + 7C EC + pay hook (happy)
- group: approve · ความสำคัญ: สูง · trace: FN-13 / AT-13 / BR-05 / BR-09 / BR-DOA-4 / XT-01/XT-02
- actor (role): admin (HR ขั้นสุดท้าย)
- Setup: role=qa_admin · seed=คำขอ pending อยู่ที่ **ขั้นสุดท้าย** (ขั้น 1 อนุมัติแล้ว) · re-check ผ่าน · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast **"อนุมัติแล้ว · ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC"** · pill = อนุมัติแล้ว · สถานะจ่าย = pending

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ pending (ขั้นสุดท้าย) → CLICK ปุ่ม **อนุมัติ** | — | modal **"อนุมัติคำขอ …?"** เปิด · รายการ "ตัดคงเหลือ …" + "…7C EC" | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** ใน modal | — | ปุ่มขึ้น **"กำลังอนุมัติ…"** (is-disabled) ชั่วขณะ | ☐ |
| 3 | WAIT จน toast ปรากฏ | — | toast **"อนุมัติแล้ว · ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC"** | ☐ |
| 4 | VERIFY pill คำขอ + สถานะจ่าย | — | pill คำขอ = **อนุมัติแล้ว** (เขียว) · สถานะจ่าย = **รอจ่าย/pending** (display) | ☐ |
| 5 | OPEN drawer คำขอ → tab **ประวัติ** | — | เห็นบรรทัด **"ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย"** | ☐ |

#### TC-APR-02 — อนุมัติซ้ำ/สถานะไม่ใช่ pending → ปุ่มอนุมัติไม่ปรากฏ (negative)
- group: approve · ความสำคัญ: กลาง · trace: FN-13 / BR-DOA-1
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ status=approved (S-08 approved) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer คำขอ approved **ไม่มีปุ่ม อนุมัติ / ไม่อนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ **อนุมัติแล้ว** | — | drawer เปิด | ☐ |
| 2 | VERIFY แถบ actions | — | **ไม่มี** ปุ่ม "อนุมัติ" / "ไม่อนุมัติ" (แสดงเฉพาะ pending) · มีปุ่ม "กลับรายการ" แทน (canApprove) | ☐ |

#### TC-ADV-01 — one-step advance: อนุมัติขั้น 1 ไม่ collapse ทั้งสาย (edge · FIX-03)
- group: approve · ความสำคัญ: สูง · trace: FN-13 / AT-27 / BR-DOA-3
- actor (role): manager (ขั้น 1)
- Setup: role=qa_manager · seed=คำขอ pending มีสาย DOA 2 ขั้น · ผู้ล็อกอินเป็นผู้อนุมัติขั้น 1 · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติขั้น 1 → toast **"อนุมัติขั้น 1 แล้ว · ส่งต่อขั้นถัดไป"** · **status ยัง รออนุมัติ** (ไม่ approved)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ pending → tab รายละเอียด | — | timeline สายอนุมัติ: ขั้น 1 = **กำลังพิจารณา** · ขั้น 2 = รอตามคิว | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** → ยืนยันใน modal | — | ปุ่ม "กำลังอนุมัติ…" | ☐ |
| 3 | WAIT จน toast ปรากฏ | — | toast **"อนุมัติขั้น 1 แล้ว · ส่งต่อขั้นถัดไป"** (ไม่ใช่ "อนุมัติแล้ว · ตัดคงเหลือ…") | ☐ |
| 4 | VERIFY pill + timeline | — | pill = **รออนุมัติ** (ยังไม่ approved) · timeline: ขั้น 1 = อนุมัติแล้ว · ขั้น 2 = **กำลังพิจารณา** | ☐ |

---

### G6 — ไม่อนุมัติ (reject)

#### TC-REJ-01 — ไม่อนุมัติ เว้นเหตุผล → บล็อก (negative)
- group: reject · ความสำคัญ: สูง · trace: FN-14 / AT-14 / VR-08 / BR_REASON_REQUIRED
- actor (role): admin/manager
- Setup: role=qa_admin · seed=คำขอ pending ≥1 · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: error **"กรุณาระบุเหตุผล"** · ไม่บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ pending → CLICK ปุ่ม **ไม่อนุมัติ** | — | modal **"ไม่อนุมัติคำขอ …?"** · subtitle "ไม่ตัดคงเหลือ + แจ้งเตือนผู้ยื่น" · ช่อง **เหตุผลที่ไม่อนุมัติ \*** | ☐ |
| 2 | CLICK ปุ่ม **ไม่อนุมัติ** (เว้นเหตุผลว่าง) | — | modal ไม่ปิด · error **"กรุณาระบุเหตุผล"** ใต้ช่อง | ☐ |

#### TC-REJ-02 — ไม่อนุมัติ ระบุเหตุผล → rejected ไม่ตัดคงเหลือ (happy)
- group: reject · ความสำคัญ: สูง · trace: FN-14 / AT-14 / BR-05 / event result
- actor (role): admin/manager
- Setup: role=qa_admin · seed=คำขอ pending ≥1 · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: D (เหตุผลไม่อนุมัติ)
- ผ่านเมื่อ: toast **"บันทึกไม่อนุมัติ · แจ้งเตือนผู้ยื่น"** · pill = ไม่อนุมัติ · คงเหลือไม่ลด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือกเจ้าของสิทธิ์ → VERIFY+จดยอด **คงเหลือ** ของ type นั้น | — | บันทึกค่าคงเหลือตั้งต้น (อ้างใน step 5) | ☐ |
| 2 | OPEN `#/welfare/requests` → CLICK คำขอ pending → CLICK **ไม่อนุมัติ** | — | modal reject เปิด | ☐ |
| 3 | TYPE → **เหตุผลที่ไม่อนุมัติ** | D | ช่องแสดงค่า | ☐ |
| 4 | CLICK ปุ่ม **ไม่อนุมัติ** → WAIT | — | toast **"บันทึกไม่อนุมัติ · แจ้งเตือนผู้ยื่น"** · pill = **ไม่อนุมัติ** (แดง) | ☐ |
| 5 | OPEN `#/welfare/balance` → VERIFY คงเหลืออีกครั้ง | — | คงเหลือ **เท่าค่าที่จดใน step 1** (ไม่ตัด · BR-05) | ☐ |

---

### G7 — ยกเลิก (cancel)

#### TC-CAN-01 — ยกเลิกคำขอ draft/pending (happy)
- group: cancel · ความสำคัญ: กลาง · trace: FN-15/FN-91 / AT-15 / VR-10 / BR-DOA-7 / BR-05
- actor (role): employee (owner) หรือ admin
- Setup: role=qa_employee · seed=คำขอ draft/pending ของตน ≥1 · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast **"ยกเลิกคำขอแล้ว"** · pill = ยกเลิก · ไม่กระทบคงเหลือ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ draft/pending ของตน | — | drawer เปิด · มีปุ่ม **ยกเลิกคำขอ** (canCancelReq) | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิกคำขอ** | — | modal **"ยกเลิกคำขอ?"** · body "…ก่อนอนุมัติ — ไม่กระทบคงเหลือ" | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิกคำขอ** (danger ใน modal) | — | modal ปิด + toast **"ยกเลิกคำขอแล้ว"** · pill = **ยกเลิก** (เทา/แดง) | ☐ |

#### TC-CAN-02 — คำขอ approved ไม่มีปุ่มยกเลิก (negative · BR-DOA-7)
- group: cancel · ความสำคัญ: สูง · trace: FN-15 / AT-15 / VR-10 / BR_CANCEL_NOT_ALLOWED
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved (S-08) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer คำขอ approved **ไม่มีปุ่ม ยกเลิกคำขอ** (ต้องใช้ reversal แทน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ **อนุมัติแล้ว** | — | drawer เปิด | ☐ |
| 2 | VERIFY แถบ actions | — | **ไม่มี** ปุ่ม "ยกเลิกคำขอ" (แสดงเฉพาะ draft/pending) · มีปุ่ม "กลับรายการ" แทน | ☐ |

---

### G8 — คงเหลือรายคน (balance)

#### TC-BAL-01 — empty state ก่อนเลือกคน
- group: balance · ความสำคัญ: ต่ำ · trace: FN-90 / state empty
- actor (role): admin/manager
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น empty state **"เลือกพนักงานเพื่อดูสิทธิ์คงเหลือ"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` | — | combobox ค้นพนักงาน + empty state **"เลือกพนักงานเพื่อดูสิทธิ์คงเหลือ"** + desc "ค้นหาแล้วเลือกพนักงาน 1 คน …" | ☐ |

#### TC-BAL-02 — ใช้บางส่วนแล้ว คงเหลือถูกต้อง (edge: EC-03 · live compute)
- group: balance · ความสำคัญ: สูง · trace: FN-09 / AT-09 / BR-02 / BR-BAL-1
- actor (role): admin/manager
- Setup: role=qa_admin · seed=S-08 มี approved บางส่วนของ type หนึ่ง (เช่น โควตา 30,000 ใช้ไป 10,000) · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตารางสิทธิ์แสดง ใช้ไป + คงเหลือ ถูกต้อง (คงเหลือ = โควตา − ใช้ไป)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → SELECT พนักงาน = S-08 | — | section **"สิทธิ์ · โควตา · คงเหลือ (ปีสิทธิ์ 2569)"** + ตาราง คอลัมน์ ประเภท/โควตา/ปี/ใช้ไป/คงเหลือ/ความคืบหน้า | ☐ |
| 2 | VERIFY แถวของ type ที่ใช้บางส่วน | — | ใช้ไป = ยอด approved สะสม · **คงเหลือ = โควตา − ใช้ไป** ตรงเลข · progress bar สอดคล้อง | ☐ |

#### TC-BAL-03 — leaver → คงเหลือหยุด + note (edge: EC-01)
- group: balance · ความสำคัญ: สูง · trace: FN-16 / AT-16 / BR-06
- actor (role): admin
- Setup: role=qa_admin · seed=S-13 leaver (last_day set) · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: note **"พนักงานพ้นสภาพ (last day …) — สิทธิ์สวัสดิการสิ้นสุด คงเหลือหยุดคำนวณ (leaver signal)"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → SELECT พนักงาน = S-13 | — | note is-warn **"พนักงานพ้นสภาพ (last day …) — สิทธิ์สวัสดิการสิ้นสุด คงเหลือหยุดคำนวณ (leaver signal)"** | ☐ |

#### TC-BAL-04 — joiner (last_day=null) → ยังทำงาน สิทธิ์เปิด (edge · BR-06)
- group: balance · ความสำคัญ: กลาง · trace: FN-18 / AT-18 / BR-06
- actor (role): admin
- Setup: role=qa_admin · seed=S-15 joiner (last_day=null) · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: **ไม่** แสดง leaver note · แสดงสิทธิ์/คงเหลือปกติ (null≠พ้นสภาพ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → SELECT พนักงาน = S-15 (joiner) | — | ตารางสิทธิ์แสดงปกติ (ปีสิทธิ์ 2569) · **ไม่มี** note พ้นสภาพ (null last-day = ยังทำงาน) | ☐ |

---

### G9 — ดูคำขอ (request-view tabs)

#### TC-VIEW-01 — tab รายละเอียด แสดงสาย DOA timeline (อ่าน)
- group: view · ความสำคัญ: กลาง · trace: FN-12 / AT-12 / BR-DOA-2
- actor (role): employee (ผู้ยื่น)
- Setup: role=qa_employee · seed=คำขอ pending ของตน มีสาย DOA freeze แล้ว · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: section **"สายอนุมัติ (จาก DOA กลาง · ไม่กำหนดสายตายตัว)"** + ชั้นปัจจุบัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ pending | — | drawer 4 tab: **รายละเอียด · หลักฐาน · คงเหลือ · ประวัติ** | ☐ |
| 2 | VERIFY tab **รายละเอียด** | — | timeline **"สายอนุมัติ (จาก DOA กลาง · ไม่กำหนดสายตายตัว)"** · ขั้นปัจจุบัน = **กำลังพิจารณา** · แต่ละขั้นแสดง avatar+ชื่อ+ตำแหน่ง | ☐ |

#### TC-VIEW-02 — สถานะจ่าย display-only (ไม่มีปุ่ม CRUD จ่าย · LK-2)
- group: view · ความสำคัญ: สูง · trace: FN-17 / AT-17 / LK-2 / NS-1
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved (S-08/S-14) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดง สถานะจ่าย (pill/text) · **ไม่มีปุ่มจ่าย/บันทึกจ่าย/แก้จ่าย**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ **อนุมัติแล้ว** → tab รายละเอียด | — | เห็น **สถานะจ่าย** (อ่านจาก Payroll/Expense · display) | ☐ |
| 2 | VERIFY ทั่วทั้ง drawer | — | **ไม่มี** ปุ่ม/ฟอร์ม "จ่าย" / "บันทึกการจ่าย" / "แก้สถานะจ่าย" ใด ๆ (Welfare ไม่จ่ายเอง) | ☐ |

---

### G10 — รายงาน (report)

#### TC-RPT-01 — รายงาน filter จริง + agg (happy)
- group: report · ความสำคัญ: กลาง · trace: FN-19 / AT-19 / permission admin/manager
- actor (role): admin
- Setup: role=qa_admin · seed=มีคำขอ approved หลายประเภท/กลุ่ม · files=—
- Start: OPEN `#/welfare/report`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยน filter → ตาราง + agg อัปเดตจริง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/report` | — | stat cards (คำขอทั้งหมด · อนุมัติแล้ว · รออนุมัติ …) + filter **ประเภท/กลุ่ม/from/to** + ตาราง คอลัมน์ ประเภท/หมวด/จำนวนคำขออนุมัติ/มูลค่ารวม | ☐ |
| 2 | VERIFY+จด จำนวนแถวตาราง ก่อน filter | — | บันทึกจำนวนแถวตั้งต้น (อ้าง step 3) | ☐ |
| 3 | SELECT → filter **ประเภท** = ค่าใดค่าหนึ่ง | — | ตาราง + footer "N ประเภท" + มูลค่ารวม **อัปเดตจริง** (ต่างจากค่าที่จด step 2) · footer note "ตัวเลข = เฉพาะคำขอสถานะ "อนุมัติแล้ว"" | ☐ |

#### TC-RPT-02 — รายงาน filter ไม่พบข้อมูล → empty state
- group: report · ความสำคัญ: ต่ำ · trace: FN-19/FN-90 / AT-19/AT-20 / state filtered-empty
- actor (role): admin
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/report`
- ชุดข้อมูล: —
- ผ่านเมื่อ: empty state **"ไม่พบข้อมูลตามตัวกรอง"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/report` → SELECT filter ช่วงวันที่ที่ไม่มีคำขอ (เช่น from/to อนาคต) | — | ตารางแสดง empty state **"ไม่พบข้อมูลตามตัวกรอง"** + desc "ยังไม่มีคำขอที่อนุมัติแล้วตรงกับเงื่อนไข" | ☐ |

---

### G11 — list / filter / empty

#### TC-LIST-01 — filter สถานะคำขอทำงานจริง (ทุกค่า)
- group: list · ความสำคัญ: กลาง · trace: FN-90 / AT-20
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ mix ทุกสถานะ (approved/pending/rejected/cancelled/reversed) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือกแต่ละค่า filter → ตารางเหลือเฉพาะสถานะนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` | — | filter สถานะ dropdown ค่า: **ทุกสถานะ · ร่าง · รออนุมัติ · อนุมัติแล้ว · ไม่อนุมัติ · ยกเลิก · ระงับ · กลับรายการแล้ว** | ☐ |
| 2 | SELECT → filter = **อนุมัติแล้ว** | — | ตารางเหลือเฉพาะแถว pill "อนุมัติแล้ว" | ☐ |
| 3 | SELECT → filter = **รออนุมัติ** | — | ตารางเหลือเฉพาะ pill "รออนุมัติ" | ☐ |
| 4 | SELECT → filter = **กลับรายการแล้ว** | — | ตารางเหลือเฉพาะ pill "กลับรายการแล้ว" (หรือ empty ถ้าไม่มี) | ☐ |

#### TC-LIST-02 — คำขอว่าง → empty state + CTA
- group: list · ความสำคัญ: ต่ำ · trace: FN-90 / AT-20 / state empty
- actor (role): admin
- Setup: role=qa_admin · seed=**ไม่มีคำขอเลย** (tenant สะอาด) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: empty state **"ยังไม่มีคำขอ"** + ปุ่ม CTA "สร้างคำขอใช้สิทธิ์"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` (seed ว่าง) | — | empty state icon inbox · title **"ยังไม่มีคำขอ"** · desc "เริ่มต้นด้วยการสร้างคำขอใช้สิทธิ์แรก" · ปุ่ม **"สร้างคำขอใช้สิทธิ์"** | ☐ |

---

### G12 — validate / double-submit / audit

#### TC-VAL-01 — กัน double-submit (ปุ่ม is-disabled + "กำลัง…") (edge: EC-08)
- group: validate · ความสำคัญ: สูง · trace: FN-92 / AT-21 / VR-12
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ pending ขั้นสุดท้าย · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หลังกดอนุมัติ ปุ่มขึ้น **"กำลังอนุมัติ…"** + is-disabled กันคลิกซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → เปิดคำขอ pending → CLICK **อนุมัติ** → CLICK **อนุมัติ** ใน modal | — | ปุ่มเปลี่ยนเป็น **"กำลังอนุมัติ…"** + คลาส is-disabled ทันที | ☐ |
| 2 | CLICK ปุ่มยืนยันซ้ำระหว่างกำลังส่ง | — | คลิกที่ 2 ไม่มีผล (ปุ่ม disabled) · ไม่เกิดการอนุมัติ/audit ซ้ำ | ☐ |

#### TC-AUD-01 — audit append-only ทุก transition (history timeline)
- group: audit · ความสำคัญ: สูง · trace: FN-93 / AT-22 / BR-07 / LK-5
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอที่ผ่านหลาย transition (สร้าง→ส่ง→อนุมัติ) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: tab ประวัติ แสดงทุกเหตุการณ์เรียงเวลา · ไม่มีปุ่มลบประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ approved → tab **ประวัติ** | — | timeline: **สร้างคำขอ …** → **อนุมัติขั้น N (role)** → **ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย** (เรียงเวลา) | ☐ |
| 2 | VERIFY ทั้ง timeline | — | ทุกรายการเป็น append (อ่านอย่างเดียว) · **ไม่มี** ปุ่มลบ/แก้รายการประวัติ | ☐ |

---

### G13 — masking per role (FN-94)

#### TC-MASK-01 — employee เห็นมูลค่า/บุคคลเป็น ••• (permission)
- group: masking · ความสำคัญ: สูง · trace: FN-94 / AT-23 / BR-08 / LK-5 · [AI-DEFAULT] (OQ-05 backend enforce)
- actor (role): employee
- Setup: role=qa_employee · seed=คำขอ/สิทธิ์ของคนอื่นหรือ scope ที่ต้อง mask · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: คอลัมน์มูลค่า + ข้อมูลบุคคลที่ต้องปกปิด แสดง **•••**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` (role=qa_employee) | — | คอลัมน์ **มูลค่า** ของแถวที่ไม่มีสิทธิ์เห็น = **•••** (masked) | ☐ |
| 2 | OPEN `#/welfare/balance` → เลือกคน (ถ้าเข้าได้) | — | ค่า ใช้ไป/คงเหลือ ที่เป็น RESTRICTED = **•••** | ☐ |

> หมายเหตุ: masking จริง enforce ที่ backend (OQ-05 · [AI-DEFAULT]) — prototype ตรวจได้เฉพาะการแสดง ••• ตาม role ที่ล็อกอิน.

#### TC-MASK-02 — manager เห็นมูลค่า แต่ผู้ติดตาม mask (permission)
- group: masking · ความสำคัญ: สูง · trace: FN-94 / AT-23 / canSeeDependent=admin เท่านั้น
- actor (role): manager
- Setup: role=qa_manager · seed=พนักงานที่มีผู้ติดตาม · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มูลค่า/คงเหลือ **เห็นค่า** · ข้อมูลผู้ติดตาม **mask/ซ่อน**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` (role=qa_manager) → เลือกพนักงานมีผู้ติดตาม | — | ตารางสิทธิ์แสดง **มูลค่า/คงเหลือเป็นตัวเลขจริง** (canSeeValue) | ☐ |
| 2 | VERIFY sub-list ผู้ติดตาม | — | ข้อมูลผู้ติดตาม **ถูก mask/ซ่อน** (canSeeDependent = admin เท่านั้น) · ไม่มีปุ่ม เพิ่มผู้ติดตาม (admin เท่านั้น) | ☐ |

#### TC-MASK-03 — admin เห็นครบ (permission · control)
- group: masking · ความสำคัญ: กลาง · trace: FN-94 / AT-23
- actor (role): admin
- Setup: role=qa_admin · seed=พนักงานมีผู้ติดตาม · files=—
- Start: OPEN `#/welfare/balance`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นมูลค่า + บุคคล + ผู้ติดตาม ครบ ไม่มี •••

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` (role=qa_admin) → เลือกพนักงาน | — | มูลค่า/คงเหลือ = ตัวเลขจริง · ชื่อพนักงานเต็ม · sub-list ผู้ติดตามเห็นครบ · ปุ่ม **เพิ่มผู้ติดตาม** ปรากฏ | ☐ |

---

### G14 — กลับรายการ (reversal · OQ-WEL-01)

#### TC-REV-01 — กลับรายการคำขอ approved → คืนสิทธิ์ + EC reverse (happy · R17 delta)
- group: reversal · ความสำคัญ: สูง · trace: FN-14/AT-24 / BR-11 / BR-BAL-3 / XT-03 / LK-5/LK-6
- actor (role): admin (canApprove)
- Setup: role=qa_admin · seed=คำขอ approved (S-08 · เช่น มูลค่า 5,000 ตัดคงเหลือไปแล้ว) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: D (เหตุผลกลับรายการ)
- ผ่านเมื่อ: toast **"กลับรายการแล้ว · คืนสิทธิ์และมูลค่าให้พนักงาน · แจ้งเตือนผู้ยื่น"** · pill = กลับรายการแล้ว · คงเหลือคืนเท่าเดิมก่อนอนุมัติ · history เพิ่มบรรทัดกลับรายการ (ข้อมูลเดิมคงอยู่)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือกเจ้าของสิทธิ์ → VERIFY+จด **คงเหลือ** ปัจจุบัน (หลังตัด) เช่น 25,000 | — | บันทึกค่าคงเหลือหลังอนุมัติ (อ้าง step 6) | ☐ |
| 2 | OPEN `#/welfare/requests` → CLICK คำขอ **อนุมัติแล้ว** | — | drawer เปิด · มีปุ่ม **กลับรายการ** (undo-2 · แดง) | ☐ |
| 3 | CLICK ปุ่ม **กลับรายการ** | — | modal **"กลับรายการคำขอ …?"** · subtitle "คำขอที่อนุมัติแล้วไม่ถูกลบ — บันทึกการกลับรายการแบบ append-only" · รายการ "คืนสิทธิ์การใช้ …" | ☐ |
| 4 | TYPE → **เหตุผลการกลับรายการ** | D | ช่องแสดงค่า | ☐ |
| 5 | CLICK ปุ่ม **กลับรายการ** (danger) → WAIT | — | modal ปิด + toast **"กลับรายการแล้ว · คืนสิทธิ์และมูลค่าให้พนักงาน · แจ้งเตือนผู้ยื่น"** · pill = **กลับรายการแล้ว** | ☐ |
| 6 | OPEN `#/welfare/balance` → VERIFY คงเหลืออีกครั้ง | — | คงเหลือ **เพิ่มกลับ = ค่าเดิมก่อนอนุมัติ** (25,000 + 5,000 = 30,000 · คืนเท่ามูลค่าคำขอ · เทียบค่าที่จด step 1) | ☐ |
| 7 | OPEN drawer คำขอ → tab ประวัติ + note | — | note danger **"กลับรายการแล้ว: <เหตุผล> — คืนสิทธิ์การใช้ + คืนมูลค่าเข้าเงินได้ (7C · EC) (ข้อมูลเดิมคงไว้ · append-only)"** + history เพิ่ม **"กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)"** · บรรทัดอนุมัติเดิม **ยังอยู่** | ☐ |

#### TC-REV-02 — กลับรายการ เว้นเหตุผล → บล็อก (negative)
- group: reversal · ความสำคัญ: สูง · trace: AT-24 / VR-08 / BR-11 / BR_REASON_REQUIRED
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: error **"กรุณาระบุเหตุผล"** · ไม่กลับรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ approved → CLICK **กลับรายการ** | — | modal reverse เปิด · ช่อง **เหตุผลการกลับรายการ \*** | ☐ |
| 2 | CLICK ปุ่ม **กลับรายการ** (เว้นเหตุผลว่าง) | — | modal ไม่ปิด · error **"กรุณาระบุเหตุผล"** ใต้ช่อง | ☐ |

#### TC-REV-03 — คำขอ pending / non-approved ไม่มีปุ่มกลับรายการ (negative · EC-11)
- group: reversal · ความสำคัญ: สูง · trace: AT-24 / VR-11 / BR_REVERSE_NOT_ALLOWED / EC-11
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ pending + คำขอ reversed แล้ว · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pending/reversed **ไม่มี** ปุ่มกลับรายการ (reverse เฉพาะ approved · reversed กลับซ้ำไม่ได้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ **รออนุมัติ** | — | drawer เปิด · **ไม่มี** ปุ่ม "กลับรายการ" (มีเฉพาะ approved) | ☐ |
| 2 | CLICK คำขอ **กลับรายการแล้ว** (reversed) | — | drawer เปิด · **ไม่มี** ปุ่ม "กลับรายการ" (reversed ≠ approved · EC-11) | ☐ |

#### TC-REV-04 — กลับรายการหลังจ่ายแล้ว (pay=sent) → clawback flag (edge: EC-06 · XT-04)
- group: reversal · ความสำคัญ: สูง · trace: AT-24 / BR-11 / EC-06 / XT-04
- actor (role): admin
- Setup: role=qa_admin · seed=S-14 คำขอ approved + **pay=sent** (ส่งจ่าย Payroll แล้ว) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: D
- ผ่านเมื่อ: หลังกลับรายการ note แสดง **"· แจ้ง Payroll ตั้งเบิกคืน"** (payroll_clawback=true)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ S-14 (approved · pay=sent) → CLICK **กลับรายการ** | — | modal reverse เปิด | ☐ |
| 2 | TYPE เหตุผล → CLICK **กลับรายการ** → WAIT | D | toast กลับรายการแล้ว · pill = กลับรายการแล้ว | ☐ |
| 3 | VERIFY note ใน drawer คำขอ | — | note danger มีข้อความเพิ่ม **"· แจ้ง Payroll ตั้งเบิกคืน"** (clawback flag · Welfare ไม่ clawback เอง) | ☐ |

---

### G15 — exposure display-only (OQ-WEL-03)

#### TC-EXP-01 — แสดง pending demand อื่นบนสิทธิ์เดียวกัน · ไม่ล็อก (display-only)
- group: exposure · ความสำคัญ: กลาง · trace: FN-16/AT-25 / BR-12 / BR-DOA-5
- actor (role): admin/manager
- Setup: role=qa_admin · seed=สิทธิ์หนึ่งมีคำขอ pending อื่น ≥1 ใบบนสิทธิ์เดียวกัน · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: tab คงเหลือ (ใน drawer คำขอ) แสดง note **"คำขอรออนุมัติอื่นของสิทธิ์นี้: N ใบ · รวม {amount}"** · ไม่มีการ reserve/ล็อกโควตา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ pending ที่มีคำขอค้างอื่นบนสิทธิ์เดียวกัน → tab **คงเหลือ** | — | note is-info **"คำขอรออนุมัติอื่นของสิทธิ์นี้: N ใบ · รวม {มูลค่า}"** | ☐ |
| 2 | VERIFY ค่าคงเหลือ | — | คงเหลือ = โควตา − approved (**ไม่หัก pending** · display-only ไม่ soft-reserve) | ☐ |

---

### G16 — concurrent re-check ณ อนุมัติ (FIX-02)

#### TC-CC-01 — 2 คำขอ pending รวมเกินเพดาน → รายที่สองบล็อก ณ อนุมัติ (edge: EC-07 · [AI-DEFAULT])
- group: concurrent · ความสำคัญ: สูง · trace: AT-26 / BR-02 / BR-DOA-4 / BR-DOA-5 / EC-07 / BR_OVER_BALANCE_AT_APPROVAL · **[AI-DEFAULT]** (OQ-04 optimistic lock + backend atomic)
- actor (role): admin (ขั้นสุดท้าย)
- Setup: role=qa_admin · seed=2 คำขอ pending บนสิทธิ์เดียวกัน มูลค่ารวม > คงเหลือ (เช่น คงเหลือ 10,000 · คำขอ A=7,000 · คำขอ B=6,000) · files=— · **(ต้อง simulate concurrent — approve ทั้งสองใกล้กัน; ถ้าทดสอบ sequential ก็ต้องเห็น re-check บล็อกรายที่สอง)**
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: คำขอแรกอนุมัติได้ · คำขอที่สอง ณ อนุมัติ **บล็อก** "คงเหลือไม่พอ ณ วันอนุมัติ" (BR_OVER_BALANCE_AT_APPROVAL) หรือ 409 ERR_STALE_DATA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → VERIFY+จด คงเหลือสิทธิ์ = 10,000 | — | บันทึกคงเหลือตั้งต้น | ☐ |
| 2 | OPEN `#/welfare/requests` → อนุมัติ **คำขอ A** (7,000) จนขั้นสุดท้าย | — | toast "อนุมัติแล้ว · ตัดคงเหลือ + …7C EC" · คงเหลือเหลือ 3,000 | ☐ |
| 3 | CLICK **คำขอ B** (6,000) → CLICK อนุมัติ (ขั้นสุดท้าย) | — | re-check FIX-02 ยิง → บล็อก toast **"คงเหลือไม่พอ ณ วันอนุมัติ"** (B ขอ 6,000 > คงเหลือ 3,000) · คำขอ B ยัง pending | ☐ |
| 4 | VERIFY คงเหลือ | — | คงเหลือยัง 3,000 (ไม่ถูกตัดจาก B) · ไม่ติดลบ (BR-BAL-2 · UI clamp) | ☐ |

> `(ต้อง simulate)`: การชนกันจริงระดับ atomic/optimistic-lock (409 ERR_STALE_DATA) เป็น backend behavior (OQ-04 · [AI-DEFAULT]) — prototype ตรวจได้ระดับ re-check บล็อกรายที่สอง. ถ้า runner จำลอง concurrent จริงไม่ได้ → mark BLOCKED พร้อม note.

---

### G17 — permission / governance guards

#### TC-PERM-01 — employee เปิดคำขอ pending ไม่เห็นปุ่มอนุมัติ (permission · deny)
- group: permission · ความสำคัญ: สูง · trace: BR-DOA-6 / permission matrix / ERR_INSUFFICIENT_ROLE
- actor (role): employee
- Setup: role=qa_employee · seed=คำขอ pending (ที่ employee เห็นได้ใน scope ตน) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer **ไม่มี** ปุ่ม อนุมัติ / ไม่อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` (role=qa_employee) → CLICK คำขอ pending | — | drawer เปิด · **ไม่มี** ปุ่ม "อนุมัติ" / "ไม่อนุมัติ" (canApprove=false) · อาจมีปุ่ม "ยกเลิกคำขอ" ถ้าเป็นเจ้าของ | ☐ |

#### TC-PERM-02 — employee ไม่เห็นปุ่มกลับรายการ (permission · deny)
- group: permission · ความสำคัญ: สูง · trace: BR-DOA-6 / BR-11 / VR-11
- actor (role): employee
- Setup: role=qa_employee · seed=คำขอ approved (ในมุมมองที่ employee เข้าถึงได้) · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer approved **ไม่มี** ปุ่ม กลับรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` (role=qa_employee) → CLICK คำขอ **อนุมัติแล้ว** | — | drawer เปิด · **ไม่มี** ปุ่ม "กลับรายการ" (canApprove=false) | ☐ |

#### TC-PERM-03 — อนุมัติได้เฉพาะ pending (approve precondition · FIX-01)
- group: permission · ความสำคัญ: สูง · trace: BR-DOA-1 / BR_APPROVE_PRECONDITION
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved/rejected แล้ว · files=— · (ต้อง simulate หากต้องกระตุ้น doApprove บนสถานะไม่ใช่ pending)
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มอนุมัติแสดงเฉพาะ pending; หากบังคับเรียกอนุมัติบนสถานะอื่น → toast **"อนุมัติได้เฉพาะคำขอสถานะรออนุมัติ"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → CLICK คำขอ **อนุมัติแล้ว** | — | drawer ไม่มีปุ่มอนุมัติ (precondition กันตั้งแต่ UI) | ☐ |
| 2 | (simulate) กระตุ้น approve บนคำขอที่ไม่ใช่ pending | — | guard ตอบ toast **"อนุมัติได้เฉพาะคำขอสถานะรออนุมัติ"** (BR_APPROVE_PRECONDITION) — ถ้าจำลองไม่ได้ mark BLOCKED | ☐ |

#### TC-PERM-04 — manager/employee สร้าง/ปิดใช้ประเภทไม่ได้ (permission · deny)
- group: permission · ความสำคัญ: สูง · trace: BR-DOA-6 / permission matrix (ทะเบียน = admin เท่านั้น)
- actor (role): manager
- Setup: role=qa_manager · seed=มีประเภทในทะเบียน · files=—
- Start: OPEN `#/welfare/registry`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม สร้างประเภท/แก้/ปิดใช้ (read-only); หากกดปิดใช้ผ่าน guard → toast "สิทธิ์ไม่พอ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/registry` (role=qa_manager) | — | ตารางแสดงอ่านได้ · **ไม่มี** ปุ่ม "สร้างประเภทสวัสดิการ" · ไม่มี row action แก้/ปิดใช้ (admin เท่านั้น) | ☐ |
| 2 | (ถ้ามีปุ่มโผล่) CLICK ปิดใช้ | — | toast **"สิทธิ์ไม่พอ"** (FIX-04 guard) · ไม่เปลี่ยนสถานะ | ☐ |

---

### G18 — negative: 5 not-supported (Scope Lock R11 Exclusions · FN-40 equivalent)

> เคสกลุ่มนี้ **พิสูจน์ว่าของที่อยู่นอก scope ไม่ปรากฏบนจอ** (render จริงแล้ว assert ว่าไม่มี). ทุกเคส role=qa_admin (สิทธิ์สูงสุด — ถ้า admin ยังไม่เห็น = ยืนยันไม่มีจริง).

#### TC-NEG-01 — ไม่มีการจ่ายเงินจริง/เบิก/หักเงินเดือน (NS-1 · LK-2)
- group: negative · ความสำคัญ: สูง · trace: NS-1 / LK-2 / FN-17
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved · files=—
- Start: OPEN `#/welfare/requests`
- ผ่านเมื่อ: ไม่พบปุ่ม/ฟอร์ม จ่ายเงิน/เบิก/หักเงินเดือน ทุกหน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → เปิดคำขอ approved · สำรวจทุก tab | — | สถานะจ่าย = **display-only** · **ไม่มี** ปุ่ม "จ่าย"/"บันทึกการจ่าย"/"หักเงินเดือน"/"เบิกเงิน" | ☐ |
| 2 | VERIFY ทั้ง 4 tab (registry/requests/balance/report) | — | ไม่มีเมนู/action เกี่ยวกับ payout จริงที่ใดเลย | ☐ |

#### TC-NEG-02 — ไม่มีการจัดการผู้ให้บริการ (รพ./ประกัน) (NS-2)
- group: negative · ความสำคัญ: กลาง · trace: NS-2
- actor (role): admin
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/registry`
- ผ่านเมื่อ: ไม่มี tab/เมนู/ฟิลด์ จัดการ provider/รพ./บริษัทประกัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY sidebar + 4 tab | — | มีเพียง ทะเบียนสวัสดิการ/คำขอใช้สิทธิ์/คงเหลือรายคน/รายงาน · **ไม่มี** "ผู้ให้บริการ"/"โรงพยาบาลคู่สัญญา"/"บริษัทประกัน" | ☐ |
| 2 | OPEN drawer สร้างประเภท | — | ไม่มีฟิลด์เลือก provider/รพ. | ☐ |

#### TC-NEG-03 — ไม่มีสวัสดิการยืดหยุ่น/แต้ม (flex credits) (NS-3)
- group: negative · ความสำคัญ: กลาง · trace: NS-3
- actor (role): admin
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/balance`
- ผ่านเมื่อ: ไม่มี "แต้ม"/"เครดิตยืดหยุ่น"/flex points ที่ใด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/balance` → เลือกคน | — | ตารางสิทธิ์เป็น โควตา/ใช้ไป/คงเหลือ ต่อ type เท่านั้น · **ไม่มี** ยอด "แต้ม/เครดิตยืดหยุ่น" ให้เลือกใช้ข้ามประเภท | ☐ |
| 2 | OPEN drawer สร้างประเภท | — | หน่วยนับมีเฉพาะ เงิน/ครั้ง/% · ไม่มี "แต้ม/points" | ☐ |

#### TC-NEG-04 — ไม่มีการสร้าง/แก้ค่านโยบาย HR กลาง (NS-4 · LK-3)
- group: negative · ความสำคัญ: สูง · trace: NS-4 / LK-3
- actor (role): admin
- Setup: role=qa_admin · seed=— · files=—
- Start: OPEN `#/welfare/registry`
- ผ่านเมื่อ: ไม่มีหน้า/ฟอร์ม แก้ ปฏิทิน/กลุ่มบริษัท/effective policy กลาง (อ่านจาก HR Config เท่านั้น)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทั้ง feature | — | **ไม่มี** หน้า/ปุ่ม "ตั้งค่านโยบาย HR"/"กลุ่มบริษัท"/"ปฏิทินสิทธิ์" ให้ CRUD · กลุ่มพนักงานเป็นค่าที่อ่านมาเลือกเท่านั้น (ไม่สร้างกลุ่มใหม่) | ☐ |

#### TC-NEG-05 — ไม่มีเอกสารเลขรัน/PDF ทางการ (NS-5)
- group: negative · ความสำคัญ: สูง · trace: NS-5 / CD-01
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved · files=—
- Start: OPEN `#/welfare/requests`
- ผ่านเมื่อ: ไม่มีปุ่ม พิมพ์/ดาวน์โหลด PDF/ออกเลขเอกสารทางการ · request_no เป็น internal id (REQ-2569-…)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → เปิดคำขอ approved | — | เลขคำขอเป็น **internal display id** (เช่น REQ-2569-xxxx) · **ไม่มี** ปุ่ม "พิมพ์"/"ดาวน์โหลด PDF"/"ออกเอกสาร" | ☐ |
| 2 | OPEN `#/welfare/report` | — | รายงาน view-only · **ไม่มี** ปุ่ม print/Export PDF (NS-5) | ☐ |

---

### G19 — cross-module (XT · 06_TESTS §6.9)

#### TC-XT-01 — approve → ยิง CSQ EC only (welfare.granted) (XT-01 · LK-6)
- group: xt · ความสำคัญ: สูง · trace: XT-01 / BR-09 / LK-6
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ pending ขั้นสุดท้าย · **CSQ = mock** (prototype ไม่มีหน้า CSQ ปลายทาง) · files=—
- Start: OPEN `#/welfare/requests`
- ผ่านเมื่อ: หลังอนุมัติ history/note ยืนยัน "บันทึกมูลค่าเข้า 7C EC" (ท่อ EC เท่านั้น — ไม่มี OC/DC/SC)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → อนุมัติคำขอขั้นสุดท้าย → WAIT | — | toast **"อนุมัติแล้ว · ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC"** | ☐ |
| 2 | OPEN drawer คำขอ → tab ประวัติ | — | บรรทัด **"ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย"** (EC เท่านั้น · ไม่ระบุ OC/DC/SC) | ☐ |

> `(ต้อง simulate)` ฝั่ง CSQ: prototype ยืนยัน event ผ่าน microcopy/history เท่านั้น (ไม่มีหน้า 7C ปลายทาง). payload {ref, employee_id, value_declared, basis=declared} = backend contract.

#### TC-XT-02 — approve → Payroll pay=pending (display-only) (XT-02)
- group: xt · ความสำคัญ: สูง · trace: XT-02 / LK-2 / FN-17
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved · pay hook = mock · files=—
- Start: OPEN `#/welfare/requests`
- ผ่านเมื่อ: หลังอนุมัติ สถานะจ่าย = **รอจ่าย (pending)** อ่านอย่างเดียว · ไม่มี pay action ใน Welfare

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → หลังอนุมัติ VERIFY สถานะจ่าย | — | pill/text สถานะจ่าย = **รอจ่าย/pending** (display-only) | ☐ |
| 2 | VERIFY drawer | — | ไม่มีปุ่มเปลี่ยนสถานะจ่าย (ต่อ TC-NEG-01/VIEW-02) | ☐ |

#### TC-XT-03 — reverse → CSQ EC reverse (negative offset) (XT-03 · LK-6)
- group: xt · ความสำคัญ: สูง · trace: XT-03 / BR-11 / LK-6
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอ approved (มี EC forward แล้ว) · CSQ mock · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: D
- ผ่านเมื่อ: หลังกลับรายการ note/history ยืนยัน **"คืนมูลค่าเข้าเงินได้ (7C · EC)"** (EC reverse คู่กับ forward)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/welfare/requests` → กลับรายการคำขอ approved (ตาม TC-REV-01) → WAIT | D | toast กลับรายการแล้ว | ☐ |
| 2 | OPEN drawer → tab ประวัติ | — | history เพิ่ม **"กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)"** (negative offset · EC เท่านั้น) · บรรทัด EC forward เดิมยังอยู่ (append-only) | ☐ |

#### TC-XT-04 — reverse คำขอ pay=sent → payroll_clawback=true (XT-04)
- group: xt · ความสำคัญ: สูง · trace: XT-04 / EC-06 / BR-11
- actor (role): admin
- Setup: role=qa_admin · seed=S-14 approved + pay=sent · files=—
- Start: OPEN `#/welfare/requests`
- ชุดข้อมูล: D
- ผ่านเมื่อ: note reverse แสดง "· แจ้ง Payroll ตั้งเบิกคืน" (clawback flag · Welfare ไม่ clawback เอง) — เท่ากับ TC-REV-04

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ทำตาม TC-REV-04 (กลับรายการคำขอ pay=sent) | D | toast กลับรายการแล้ว | ☐ |
| 2 | VERIFY note drawer | — | มีข้อความ **"· แจ้ง Payroll ตั้งเบิกคืน"** (payroll_clawback=true flag) | ☐ |

#### TC-XT-05 — state transitions → ยิง NTF events (business · DOA ไม่ซ้ำ) (XT-05)
- group: xt · ความสำคัญ: กลาง · trace: XT-05 / §1.5 events / §6.5
- actor (role): admin
- Setup: role=qa_admin · seed=คำขอครบ lifecycle · NTF = mock (ENG-NOTIFY) · files=— · **(ต้อง simulate — prototype ไม่มี Notification Center; ยืนยันผ่าน toast microcopy ที่ผูก event)**
- Start: OPEN `#/welfare/requests`
- ผ่านเมื่อ: แต่ละ transition มี toast/สัญญาณที่สอดคล้อง event (submitted/result/reversed) · ไม่ยิง DOA event ซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ส่งอนุมัติคำขอ (submit) | — | toast **"ส่งอนุมัติแล้ว · แจ้งเตือน HR อัตโนมัติ"** (= welfare_request_submitted) | ☐ |
| 2 | อนุมัติขั้นสุดท้าย | — | toast อนุมัติแล้ว (= welfare_request_result ยิงถึงผู้ยื่น) | ☐ |
| 3 | กลับรายการ | — | toast กลับรายการแล้ว · แจ้งเตือนผู้ยื่น (= welfare_request_reversed) | ☐ |
| 4 | VERIFY (simulate) NTF payload | — | 5 business events (submitted/result/near_limit/eligibility_ended/reversed) · doa_pending/doa_result มาจาก DOA engine (ไม่ประกาศซ้ำ) — ถ้าจำลอง channel ไม่ได้ mark note (prototype ไม่เช็ค channel เอง) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `outputs/F-HR-WELFARE/welfare.html` ใน browser. ก่อนแต่ละเคส ให้ **refresh** และตั้ง role ตาม `Setup:` (prototype: สลับ role ผ่านตัวสลับ persona/roleของหน้า ถ้ามี — ค่า admin/manager/employee).
2. ทำตาม `Start` route ก่อน (hash route `#/welfare/...`).
3. ทำ step ตามลำดับ. Action ขึ้นต้นด้วย verb tag → map 1:1. Input อ้างชุดข้อมูลใน `## Data Sets`.
4. ตัดสิน Expected จากสิ่งที่ **เห็นบนจอ** (ข้อความ/pill/route/ปุ่ม disable). เคสที่มี **จด/VERIFY ค่าตั้งต้น** ให้บันทึกเลขจริงไว้เทียบ (R17).
5. เคส `(ต้อง simulate)` — ถ้า runner จำลองไม่ได้ (concurrent atomic, backend event, channel) ให้ mark **blocked** พร้อม `evidence` แทน fail.
6. เคส `[AI-DEFAULT]` — fail อาจหมายถึง default (OQ-04/05) ผิด ไม่ใช่โค้ดผิด: ระบุใน note.
7. กรอก `Result ☐` ทุก step + สรุปตาม schema ท้ายไฟล์.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FR / Acceptance (AT-01..27) | 27 / 27 |
| 24 FN (FUNCTION_CHECKLIST) | 24 / 24 |
| Business rules (BR-01..12 + BR-DOA-1..8 + BR-BAL-1..3) | 23 / 23 |
| Field validation (VR-01..12) | 12 / 12 |
| Error codes (ที่ trigger บน UI ได้) | 15 / 19 (4 generic/backend = ข้าม) |
| Permission cells (สำคัญ) | ครบ (create/approve/reject/reverse/cancel/masking/report) |
| Edge cases (EC-01..14) | 8 / 14 (6 backend/Phase B/OQ = ข้าม) |
| Cross-cutting / events / states | ครบ |

- **Cross-Module (XT): 5 / 5** (XT-01..05 · บาง step (ต้อง simulate) — ยืนยันผ่าน microcopy/history)
- **Scope Lock (LK-1..6): 6 / 6** ✅ (ทุก LOCK มีเคส verify)
- **Out of Scope negatives (NS-1..5): 5 / 5** ✅ (FN-40 equivalent — render จริงแล้ว assert ไม่มี)
- **Reversal (OQ-WEL-01): 4 เคส** (happy + reason-block + not-allowed + clawback) ✅
- **Manifest cross-check (FRD §0.12): ✅ 24/24 FN + Stories 17/17 (ผ่าน FN rows) + Rules 12/12 + Edges confirmed 6/6** — ทุกแถว manifest มีคู่ใน Ledger

### ข้าม (พร้อมเหตุผล)
- **ERR_VALIDATION_FAILED / ERR_NOT_AUTHENTICATED / ERR_NOT_FOUND** — generic HTTP ไม่มี trigger เฉพาะบน prototype UI.
- **ERR_PERMISSION_REVOKED (EC-09)** — backend mid-flight role demote · `[AI-DEFAULT]` OQ-05 · ไม่มีผลสังเกตบน prototype.
- **ERR_DUPLICATE_IDEMPOTENCY_KEY (EC-08 backend)** — idempotency-key เป็น backend; UI ตรวจได้แค่ lockBtn (TC-VAL-01).
- **EC-10** approver ลาออกกลางสาย — OQ-02 (re-resolve = OQ กระทบสิทธิ์) · ยังไม่ตัดสิน.
- **EC-12** fiscal ปีสิทธิ์คร่อมปฏิทิน — อ้าง HR Config (A-WEL-05 · Phase B).
- **EC-13** HR Config company_scope ไม่ตรง — OQ-03 Phase B contract.
- **EC-14** attachment ชนิด/ขนาด/virus — mock · deferred to impl (§7.5).
- **ERR_STALE_DATA (409)** — จับได้เฉพาะ (ต้อง simulate) concurrent จริง (OQ-04) → TC-CC-01 mark blocked ถ้าจำลองไม่ได้.
> ของนอกขอบเขตใบเซ็น (NS-1..5) = **สร้างเคส negative verify** (ตามคำสั่ง FN-40 equivalent) ไม่ใช่ข้าม.

### OQ / Gap (ยกให้ BA — ไม่ตัดสินเอง)
- **OQ-03** (Payroll/Expense hook contract · Phase B), **OQ-04** (atomic re-check · [AI-DEFAULT]), **OQ-05** (backend permission enforce · [AI-DEFAULT]) = ยัง blocking ที่ปลายทาง; เคส TC-CC-01/TC-MASK-01 อิง default ปัจจุบัน — ผล fail อาจแปลว่า default ผิด.

---

## Result Report (schema)

```json
{
  "feature_id": "F-HR-WELFARE",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-REG-01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 60, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่เห็นจริงตอน fail/blocked (ข้อความ error จริง · route ที่ค้าง · สิ่งที่แสดงแทน Expected). `note` = หมายเหตุ (เช่น "(ต้อง simulate) จำลอง concurrent ไม่ได้" หรือ "[AI-DEFAULT] อาจเป็น default ผิด").
