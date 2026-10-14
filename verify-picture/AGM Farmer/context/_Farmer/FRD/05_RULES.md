# 05_RULES — F-AGM-001 Farmer Member Management

> **Audience:** Backend developer + QA
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> Map 1:1 จาก BRD §9 (R01–R14, VR-01..11) + §10 Edge Cases — Tag (FIXED/CONFIGURABLE/WARNING) คงตาม BRD

---

## §5.1 Business Rules (BR)

### BR-AGM-01: Member ID auto-gen `FM-%06d` — Tag: CONFIGURABLE
- **Statement:** member_id gen อัตโนมัติ format `FM-%06d` running ต่อ tenant — ห้ามแก้หลังสร้าง
- **Enforced by:** FN-01 ผ่าน Document Numbering กลาง (**ห้ามเขียน gen เอง**)
- **Configurable:** prefix/format ที่ CUBE Admin → Document Numbering (มีแล้ว — seed ค่า FM)

### BR-AGM-02: เริ่ม Pending เสมอ — Tag: FIXED
- **Statement:** สมาชิกใหม่ (form + CSV) เริ่ม `pending_approval` เสมอ
- **Enforced by:** FN-01 (hard-set, ไม่รับจาก input)

### BR-AGM-03: Verify เฉพาะ Pending — Tag: FIXED
- **Statement:** Verify (เดี่ยว/กลุ่ม) ทำได้เฉพาะ `pending_approval`
- **Error:** `BR_VERIFY_NOT_PENDING` → 422 · **Enforced by:** FN-05

### BR-AGM-04: Reject ต้องมีเหตุผล — Tag: FIXED
- **Statement:** verify_status=rejected ต้องมี verified_note
- **Error:** `ERR_VALIDATION_FAILED` (VR-07) → 400 · UI: "จำเป็นต้องระบุเหตุผลเมื่อปฏิเสธ"

### BR-AGM-05: ลบเฉพาะ Pending + soft only — Tag: FIXED
- **Statement:** ลบได้เฉพาะ `pending_approval` และเป็น soft delete เท่านั้น (ไม่มี hard delete — S06-03)
- **Error:** `BR_DELETE_NOT_PENDING` → 422 · UI: "ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ"
- **ผลพลอยได้:** สมาชิกที่มี quota (= approved) ลบไม่ได้โดยโครงสร้าง — protect downstream (02_API §2.X)

### BR-AGM-06: Optimistic lock + Idempotency ทุก mutation — Tag: FIXED (LOCK-03)
- **Statement:** ทุก mutation ใช้ `expected_updated_at` + `Idempotency-Key` = `{Legacy FN}:{id}:{user}`
- **Error:** `ERR_STALE_DATA` → 409 · `ERR_DUPLICATE_IDEMPOTENCY_KEY` → 409

### BR-AGM-07: CSV file constraints — Tag: CONFIGURABLE
- **Statement:** .csv เท่านั้น · ≤ 5MB · header 10 คอลัมน์ตรง template เป๊ะ · UTF-8
- **Config:** T_import_config (Admin Panel Phase 2) — **ห้าม hardcode 5MB ในโค้ด**
- **หมายเหตุ:** จำนวน/ชื่อ 10 คอลัมน์ = LOCK-04 ห้ามเปลี่ยน (ที่ configurable คือ limit ขนาด/แถว)

### BR-AGM-08: CSV partial success — Tag: FIXED (LOCK-04)
- **Statement:** แถวดีสร้าง แถวเสียรายงาน (row/field/message/data) + error report download — ห้าม fail ทั้งไฟล์เพราะบางแถวพัง (ยกเว้น file-level error: header/encoding/size)

### BR-AGM-09: postal_code auto + validate — Tag: FIXED
- **Statement:** postal_code กำหนดอัตโนมัติจากตำบล · ถ้าผู้ใช้/CSV ระบุมา server ต้อง validate match ตำบล
- **Error:** `BR_POSTAL_CODE_MISMATCH` → 422 · "รหัสไปรษณีย์ไม่ตรงกับตำบล"

### BR-AGM-10: citizen_id unique ต่อ tenant — Tag: FIXED
- **Statement:** ซ้ำ → reject (form: error รายช่อง / CSV: error รายแถว)
- **Error:** `BR_CITIZEN_ID_DUPLICATE` → 422 · "เลขบัตรประชาชนนี้มีในระบบแล้ว"

### BR-AGM-11: Re-submit อัตโนมัติ — Tag: FIXED (LOCK-06)
- **Statement:** `rejected` → แก้ไข+บันทึกสำเร็จ → กลับ `pending_approval` อัตโนมัติ ใน transaction เดียว · verified_note เดิมย้ายเข้า history แล้วเคลียร์จาก record · ไม่จำกัดรอบ (EC-14)
- **Enforced by:** FN-02 step 3

### BR-AGM-12: Approved แก้ได้ทุก field — Tag: FIXED (LOCK-07)
- **Statement:** `approved` แก้ได้ทุก field สถานะคงเดิม — ทุกการแก้ลง Immutable Log (Before/After) · แก้ citizen_id หลัง approved → anomaly flag + event แจ้งการเงิน (BRD §18.5)

### BR-AGM-13: quota_status read-only — Tag: FIXED
- **Statement:** quota_status เขียนโดย module Quota เท่านั้น — feature นี้อ่านอย่างเดียว (ไม่มี API เขียน field นี้)

### BR-AGM-14: DOA placeholder — Tag: WARNING
- **Statement:** Verify เป็น pre-DOA placeholder — fields `approver_role/approved_by/approval_chain` + `// TODO: wire DOA ENC` · **ห้าม hardcode approval rule** · Phase 4 wire DOA engine (OQ-01)

---

## §5.2 State Machine (LOCK-02 + LOCK-06/07)

```
   [*] ──create/CSV──▶ pending_approval ──approve (R-02)──▶ approved ──edit (R-01)──▶ approved (คงเดิม — LOCK-07)
                        │        ▲
                        │        └──edit+save (R-01, อัตโนมัติ — LOCK-06)── rejected ◀──reject+note (R-02)──┘
                        └──delete (R-01)──▶ deleted (soft)
```

| From | Action | To | เงื่อนไข | ผู้ทำ | Enforced by |
|---|---|---|---|---|---|
| — | Create / CSV import | pending_approval | ผ่าน validation | R-01 | FN-01 |
| pending_approval | Approve | approved | — | R-02 | FN-05 |
| pending_approval | Reject | rejected | verified_note required | R-02 | FN-05 |
| rejected | Edit + Save | pending_approval | บันทึกสำเร็จ (อัตโนมัติ) | R-01 | FN-02 |
| pending_approval | Edit + Save | pending_approval | สถานะคงเดิม | R-01 | FN-02 |
| approved | Edit + Save | approved | สถานะคงเดิม + Immutable Log | R-01 | FN-02 |
| pending_approval | Delete | deleted (soft) | — | R-01 | FN-07 |
| approved / rejected | Delete | ❌ ไม่อนุญาต | BR_DELETE_NOT_PENDING | — | FN-07 |
| approved / rejected / deleted | Verify | ❌ ไม่อนุญาต | BR_VERIFY_NOT_PENDING | — | FN-05 |

> ⚠️ **Recheck note — GAP-12 (2026-07-22):** authoritative FRD ระบุ verify_status เปลี่ยน **ผ่าน Verify Modal (single/bulk) เท่านั้น**. LOCK-06 (rejected → edit+save → pending อัตโนมัติ) และ LOCK-07 (approved edit คงสถานะ) เป็นเส้น transition **additive เกิน authoritative** — คงไว้แต่ **ต้องขอ owner sign-off** ก่อนถือเป็น final.
> **GAP-08 verify_status mapping:** wire value = `pending_approval`/`approved`/`rejected`; authoritative canonical ↔ domain = unverified↔Pending Approval / verified↔Approved / rejected↔Rejected (ตารางเต็มที่ 04_DB §4.2).

---

## §5.3 Permission Matrix (→ register เป็น User Access ENC — ห้าม hardcode)

| Role | ดูรายการ/detail | สร้าง | แก้ไข | ลบ (Pending) | CSV Import | Verify เดี่ยว | Verify กลุ่ม |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| R-01 Farmer Registrar (Maker) | ✅ | ✅ | ✅ ทุกสถานะ (LOCK-07) | ✅ | ✅ | ❌ | ❌ |
| R-02 Registrar Supervisor (Checker) | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ เฉพาะ Pending | ✅ เฉพาะ Pending |

**SoD:** R-01 ≠ R-02 คนละบัญชี · self-verify → EC-15 (feature flag — OQ-02)

---

## §5.4 Field Validation Rules (map BRD VR-01..11 ครบ)

| ID | Field/Action | เงื่อนไข | Error code | ข้อความ |
|---|---|---|---|---|
| VR-01 | citizen_id | ตัวเลข 13 หลักเป๊ะ (strip non-digit, maxLength 13) | ERR_VALIDATION_FAILED | "เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก" |
| VR-02 | phone | ตัวเลข 9–12 หลัก (strip non-digit) | ERR_VALIDATION_FAILED | "เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก" |
| VR-03 | email | **required** + email format (blank → error) — authoritative (LOCK-08 optional superseded 2026-07-22) | ERR_VALIDATION_FAILED | "กรุณากรอกอีเมล" / "รูปแบบอีเมลไม่ถูกต้อง" |
| VR-04 | required set | first_name, last_name, citizen_id, phone, **email**, address_line, province, district, subdistrict | ERR_VALIDATION_FAILED | "กรุณากรอก[ชื่อฟิลด์]" / dropdown: "กรุณาเลือก[จังหวัด/อำเภอ/ตำบล]" |
| VR-05 | citizen_id unique | ต่อ tenant (exclude ตัวเองตอน edit) | BR_CITIZEN_ID_DUPLICATE | "เลขบัตรประชาชนนี้มีในระบบแล้ว" |
| VR-06 | verify result | ต้องเลือก approved/rejected | ERR_VALIDATION_FAILED | "กรุณาเลือกผลการตรวจสอบ" |
| VR-07 | verified_note เมื่อ Reject | บังคับกรอก | ERR_VALIDATION_FAILED | "จำเป็นต้องระบุเหตุผลเมื่อปฏิเสธ" |
| VR-08 | CSV file | .csv + ≤ limit (config) | ERR_CSV_INVALID_FILE | "กรุณาเลือกไฟล์ CSV เท่านั้น" / "ขนาดไฟล์ต้องไม่เกิน 5MB" |
| VR-09 | postal_code | ต้อง match ตำบล (form + CSV รายแถว) | BR_POSTAL_CODE_MISMATCH | "รหัสไปรษณีย์ไม่ตรงกับตำบล" |
| VR-10 | optimistic lock | expected_updated_at ไม่ตรง | ERR_STALE_DATA | "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง" |
| VR-11 | cascade reset | เปลี่ยนจังหวัด → เคลียร์อำเภอ/ตำบล/ไปรษณีย์ · เปลี่ยนอำเภอ → เคลียร์ตำบล/ไปรษณีย์ | — (UI trigger) | — |

---

## §5.5 Edge Cases

### §5.5.1 Confirmed ☑ (BRD §10.1 — บังคับ implement + test)

| ID | กรณี | Resolution | Test |
|---|---|---|---|
| EC-01 | Verify/Edit ชนกัน | Optimistic lock — คนหลัง 409 ERR_STALE_DATA แจ้งรีเฟรช ไม่ทับข้อมูล | AC-25 |
| EC-02 | ลบรายการยืนยันแล้ว | block BR_DELETE_NOT_PENDING + "ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ" (UI ซ่อนปุ่มอยู่แล้ว — server ต้อง guard ซ้ำ) | AC-22 |
| EC-03 | Reject ไม่ใส่เหตุผล | block VR-07 | AC-15 |
| EC-04 | CSV บางแถวพัง | partial success + error report ครบทุกแถวเสีย (LOCK-04) | AC-08 |
| EC-05 | ค้นหาไม่เจอ | empty state "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง + CTA | AC-13 |
| EC-06 | เลือกทั้งหมด | checkbox หัวตารางเลือกเฉพาะแถว selectable (pending) | AC-17 |
| EC-07 | citizen_id ซ้ำ | form: error รายช่อง / CSV: error รายแถว "เลขบัตรประชาชนซ้ำ" | AC-06/07 |
| EC-08 | เปลี่ยนจังหวัดหลังเลือกตำบล | cascade reset (VR-11) | AC-04 |

### §5.5.2 Recommended ☐ (BRD §10.2 — implement แนะนำ, BA confirm ที่ SOW3.7)

| ID | กรณี | Resolution แนะนำ | Test |
|---|---|---|---|
| EC-09 | CSV encoding ไม่ใช่ UTF-8 | reject ทั้งไฟล์ ERR_CSV_ENCODING + แนะนำ save เป็น UTF-8 | RC-01 |
| EC-10 | CSV header ไม่ตรง/ขาด-เกิน | reject ทั้งไฟล์ก่อน process BR_CSV_HEADER_MISMATCH + บอกคอลัมน์ผิด | RC-02 |
| EC-11 | citizen_id ซ้ำกันเองในไฟล์ | แถวแรกผ่าน แถวถัดไป error "เลขบัตรประชาชนซ้ำภายในไฟล์" | RC-03 |
| EC-12 | Bulk verify — บางรายการถูก verify ก่อน | ข้าม นับ failed + เหตุผลใน summary (ไม่ล้มทั้ง batch) | AC-18 |
| EC-13 | ตำบลใน CSV สะกดไม่ตรง master | error รายแถว "ไม่พบตำบลใน[อำเภอ]" | RC-04 |
| EC-14 | Re-submit วนหลายรอบ | อนุญาตไม่จำกัด · history ครบทุกรอบ · > 3 ครั้ง → anomaly flag | RC-05 |
| EC-15 | Self-verify (SoD) | block ERR_SOD_SELF_VERIFY "ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง" — หลัง feature flag (OQ-02; flag ปิด = log anomaly) | RC-06 |
| EC-16 | Double-click บันทึก | Idempotency key กันสร้างซ้ำ (BR-AGM-06) + ปุ่ม disabled ระหว่างส่ง (Rule #44) | AC-26 |

---

## §5.6 Error Catalog

| Code | HTTP | Message (UI) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | ข้อความรายช่องตาม §5.4 | validation ไม่ผ่าน |
| `ERR_NOT_AUTHENTICATED` | 401 | — (redirect login) | token หมด/ไม่มี |
| `ERR_INSUFFICIENT_ROLE` | 403 | "คุณไม่มีสิทธิ์เข้าถึงส่วนนี้" | ENC role ไม่ผ่าน |
| `ERR_SOD_SELF_VERIFY` | 403 | "ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง" | EC-15 (หลัง flag) |
| `ERR_NOT_FOUND` | 404 | "ไม่พบข้อมูลสมาชิก" | ไม่มี/ถูกลบ |
| `ERR_STALE_DATA` | 409 | "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง" | optimistic lock (VR-10) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | "เกิดข้อผิดพลาด กรุณาลองใหม่" | key เดิม body ต่าง |
| `BR_CITIZEN_ID_DUPLICATE` | 422 | "เลขบัตรประชาชนนี้มีในระบบแล้ว" | BR-AGM-10 |
| `BR_POSTAL_CODE_MISMATCH` | 422 | "รหัสไปรษณีย์ไม่ตรงกับตำบล" | BR-AGM-09 |
| `BR_VERIFY_NOT_PENDING` | 422 | "รายการนี้ถูกตรวจสอบไปแล้ว" | BR-AGM-03 |
| `BR_DELETE_NOT_PENDING` | 422 | "ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ" | BR-AGM-05 |
| `BR_CSV_HEADER_MISMATCH` | 422 | "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [รายการ]" | EC-10 |
| `ERR_CSV_ENCODING` | 422 | "ไฟล์ต้องเป็น UTF-8 กรุณาบันทึกไฟล์ใหม่เป็น UTF-8" | EC-09 |
| `ERR_CSV_INVALID_FILE` | 400 | "กรุณาเลือกไฟล์ CSV เท่านั้น" / "ขนาดไฟล์ต้องไม่เกิน 5MB" | VR-08 |
| `ERR_EMPTY_SELECTION` | 422 | — (UI กัน: ปุ่ม disabled เมื่อเลือก 0) | bulk items ว่าง |

---

## §5.7 Security — Preset P3 Master Data (BRD §16.3, 10 controls)

| Control | Implementation ใน pack |
|---|---|
| S01-04 SoD Conflict Matrix | §5.3 + EC-15 (FN-05 check `created_by != userId`) |
| S01-07 Immutable Master Data Log | FN-09 + T_farmer_member_history append-only — เขียน fail = block transaction |
| S02-01 Password Policy | CUBE platform standard (นอก scope feature) |
| S02-04 Data Masking | citizen_id `1-XXXX-XXXX-XX-1` บน list (API-01 serializer) — เต็มเฉพาะ detail + ACL |
| S02-05 Data Classification Tags | 04_DB §4.2 per-column (Restricted/Confidential/Internal) |
| S03-02 Policy Versioning | ENC matrix version ที่ Policy Center |
| S04-05 Standard Master Data Mapping | M-01 address master กลาง + field naming CUBE convention |
| S05-02 Audit Fields | created/updated by/at ทุก entity |
| S06-03 Soft Delete Only | BR-AGM-05 — REVOKE hard delete |
| S07-01 Export Control | Phase 1: export เฉพาะ CSV error report (แถวเสีย) — ไม่มี export ทะเบียนทั้งชุด |

### D-CLASS: Enforcement summary
| Layer | Confidential (phone/email/address) | Restricted (citizen_id) |
|---|---|---|
| API response | ตาม ENC role | masked ใน list · เต็มเฉพาะ ACL ผ่าน (audit ทุกครั้ง) |
| UI | แสดงสำหรับ R-01/R-02 | mask บน list เสมอ |
| Export | — (ไม่มี export Phase 1) | excluded — Restricted Resources approval |
| Audit | view + mutation | view + mutation + full-value access |

**Wire points:** Policy Center → Data Classification / Restricted Resources (OQ-F02) / User Access ENC (BRD §4)

---

## §5.8 Compliance & Health

| Requirement | Implementation |
|---|---|
| PDPA | D7: PII encrypt (citizen_id) + masking + ไม่ log PII |
| ISO 27001 / COSO | Maker-Checker (§5.3) + Immutable Log + ENC |
| SLA (BRD §17.1) | Verify ภายใน 3 วันทำการ (widget เตือน > 7 วัน) · list p95 < 3s · save < 1s · CSV 1,000 แถว < 60s |
| Performance budget (authoritative — GAP-04, 2026-07-22) | reads **SER ≤ 500ms** · validation **VAL ≤ 300ms** · writes (create/update) **CRE/UPT ≤ 1500ms** — เกณฑ์เทคนิคต่อ operation (เพิ่มเคียงข้าง business SLA; benchmark ที่ 06_TESTS §6.6) |
| Threshold (BRD §17.4) | CSV failed > 20%/ไฟล์ → banner แนะนำตรวจ template/encoding · re-submit > 3 → anomaly · Pending > 7 วัน → widget |
