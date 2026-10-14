# 05_RULES — F-AGM-002 Quota Management

> **Audience:** BE + QA · Declarative · Map 1:1 จาก BRD §9 (R01–R13, VR-01..11) + §10 Edge

---

## §5.1 Business Rules

### BR-AGQ-01: quota_number user-entered + unique — FIXED (LOCK-03)
ผู้ใช้กรอกเอง · unique ต่อ tenant (exclude self ตอน edit) · Error `BR_QUOTA_NUMBER_DUPLICATE` → 422 "เลขโควต้านี้ถูกใช้แล้ว" · Enforced: FN-04 + DB unique

### BR-AGQ-02: 2 create modes — FIXED (LOCK-04)
From-Member (API-02, FN-01): ผูก member + write has_quota · No-Member (API-03, FN-02): standalone

### BR-AGQ-03: 1:0..1 + Approved — FIXED (contract)
สมาชิก 1 คน ≤ 1 โควตา active (BR_MEMBER_HAS_QUOTA "สมาชิกนี้มีโควต้าอยู่แล้ว") · ผูกได้เฉพาะ Approved (BR_MEMBER_NOT_APPROVED "ผูกได้เฉพาะสมาชิกที่อนุมัติแล้ว") · Enforced: FN-11 + DB partial unique

### BR-AGQ-04: verify เฉพาะ unverified — FIXED
Error `BR_VERIFY_NOT_UNVERIFIED` → 422 · FN-06

### BR-AGQ-05: verify note optional — FIXED (LOCK-09, OQ-Q1)
แม้ reject ก็ไม่บังคับ note (ตาม legacy) — ⚠ ต่างจาก Farmer (align รอ Strike)

### BR-AGQ-06: ลบเฉพาะ unverified + soft — FIXED (LOCK-08)
Error `BR_DELETE_NOT_UNVERIFIED` → 422 "ลบได้เฉพาะรายการที่รออนุมัติ" · FN-08

### BR-AGQ-07: Cross-module write-back — FIXED (LOCK-05) ⭐ (keep-quota + async idempotent retry)
create From-Member → member.quota_status=has_quota · reject/delete (linked) → no_quota · **quota mutation commit ก่อน — write-back เป็น step แยก idempotent (ไม่ rollback quota เมื่อ write-back fail)** · member หาย → skip+log (EC-17) · fail (TIMEOUT/502/503) → keep mutation + schedule async idempotent retry + `member_update_status=scheduled_retry` + non-blocking banner "กำลังอัปเดตสถานะสมาชิก (จะ retry อัตโนมัติ)" (OQ-F03 / FN-AT-AGQ-127) · FN-12

### BR-AGQ-08: (ดู BR-AGQ-03 — รวม approved + 1:0..1)

### BR-AGQ-09: optimistic lock + idempotency — FIXED (LOCK-06)
ทุก mutation `expected_version` + `Idempotency-Key` · Error `ERR_STALE_DATA` → 409

### BR-AGQ-10: CSV No-Member partial success + per-row idempotency — FIXED (LOCK-07)
No-Member only · แถวดีสร้าง แถวเสียรายงาน + error report · file-level error (header/encoding/size) → reject ทั้งไฟล์ · **per-row idempotency key `FN-AT-AGQ-126:{source_file_hash}:{row_index}` — rerun ไฟล์เดิม (hash เดิม) → คืนผลเดิม (ไม่สร้าง duplicate) · same batch_id + ไฟล์เนื้อหาต่าง (hash ต่าง) → 409 CONFLICT** (FN-AT-AGQ-126/132)

### BR-AGQ-11: postal auto ×2 + validate — FIXED
current + id_card แยกกัน · auto จากตำบล · server validate match · Error `BR_POSTAL_CODE_MISMATCH`

### BR-AGQ-12: file limits — CONFIGURABLE
PDF/JPG/PNG ≤ 5MB (Admin config — ห้าม hardcode)

### BR-AGQ-13: DOA placeholder — WARNING
approver fields + `// TODO: wire DOA ENC` (OQ-Q5) — ห้าม hardcode approval

---

## §5.2 State Machine (LOCK-02)

```
[*] ──create(From/No-Member)/CSV──▶ unverified ──approve(R-02)──▶ verified
                                      │  └──reject(R-02)──▶ rejected [linked→no_quota]
                                      └──delete(R-01)──▶ deleted(soft) [linked→no_quota]
```
| From | Action | To | เงื่อนไข | ผู้ทำ | Cross-module |
|---|---|---|---|---|---|
| — | Create From-Member | unverified | validation + eligible | R-01 | →has_quota |
| — | Create No-Member / CSV | unverified | validation | R-01 | — |
| unverified | Approve | verified | — | R-02 | — |
| unverified | Reject | rejected | note optional | R-02 | linked→no_quota |
| unverified | Delete | deleted | soft | R-01 | linked→no_quota |
| verified/rejected | Delete/Verify | ❌ | — | — | — |

> OQ-Q3: rejected → edit → unverified (re-submit) — legacy ไม่มี → คงตาม legacy (edit ไม่เปลี่ยนสถานะ)

> **Canonical status mapping (BE) ⭐ (G11):** stored `unverified` ↔ authoritative canonical **Pending Approval** · `verified` ↔ **Approved** · `rejected` ↔ **Rejected** — UI labels (รออนุมัติ/อนุมัติ/ไม่อนุมัติ) ตรงกับ authoritative แล้ว; BE ต้อง map ชื่อ canonical นี้ให้ชัดตอน integrate

---

## §5.3 Permission Matrix (→ ENC)
| Role | ดู | สร้าง | แก้ | ลบ (unverified) | CSV | Verify เดี่ยว | Verify กลุ่ม |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| R-01 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| R-02 | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ (unverified) | ✅ (unverified) |
**SoD:** R-01 ≠ R-02 · self-verify → EC-15 (flag OQ-Q6)

---

## §5.4 Field Validation (map BRD VR-01..11)
| ID | Field | เงื่อนไข | Error | ข้อความ |
|---|---|---|---|---|
| VR-01 | citizen_id | 13 หลัก (strip) | ERR_VALIDATION_FAILED | "เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก" |
| VR-02 | phone | 9–12 หลัก | ERR_VALIDATION_FAILED | "เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก" |
| VR-03 | email (optional) | format | ERR_VALIDATION_FAILED | "รูปแบบอีเมลไม่ถูกต้อง" |
| VR-04 | required | quota_number, ชื่อ, นามสกุล, เลขบัตร, เบอร์, จ/อ/ต ×2 | ERR_VALIDATION_FAILED | "กรุณากรอก/เลือก[ฟิลด์]" |
| VR-05 | quota_number unique | exclude self | BR_QUOTA_NUMBER_DUPLICATE | "เลขโควต้านี้ถูกใช้แล้ว" |
| VR-06 | 1:0..1 | ก่อนผูก | BR_MEMBER_HAS_QUOTA | "สมาชิกนี้มีโควต้าอยู่แล้ว" |
| VR-07 | member Approved | ก่อนผูก | BR_MEMBER_NOT_APPROVED | "ผูกได้เฉพาะสมาชิกที่อนุมัติแล้ว" |
| VR-08 | CSV file | .csv + ≤5MB | ERR_CSV_INVALID_FILE | "กรุณาเลือกไฟล์ CSV เท่านั้น" / "ขนาดไฟล์ต้องไม่เกิน 5MB" |
| VR-09 | verify result | ต้องเลือก | ERR_VALIDATION_FAILED | "กรุณาเลือกผลการตรวจสอบ" |
| VR-10 | postal ×2 | match ตำบล | BR_POSTAL_CODE_MISMATCH | "รหัสไปรษณีย์ไม่ตรงกับตำบล" |
| VR-11 | optimistic lock | version | ERR_STALE_DATA | "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง" |
| VR-12 | cascade reset ×2 | เปลี่ยนจังหวัด/อำเภอ | — (UI) | — |

---

## §5.5 Edge Cases

### §5.5.1 Confirmed ☑ (BRD §10.1)
| ID | กรณี | Resolution | Test |
|---|---|---|---|
| EC-01 | สมาชิกมีโควตาแล้ว | block BR_MEMBER_HAS_QUOTA | AC-02 |
| EC-02 | quota_number ซ้ำ | BR_QUOTA_NUMBER_DUPLICATE | AC-05 |
| EC-03 | ลบ verified/rejected | ไม่มีปุ่ม / 422 guard | AC-27 |
| EC-04 | CSV บางแถวพัง | partial success + report | AC-14 |
| EC-05 | ค้นหาไม่เจอ | empty state + CTA | AC-19 |
| EC-06 | เลือกทั้งหมด | เฉพาะ unverified | AC-23 |
| EC-07 | แก้ชนกัน | 409 ERR_STALE_DATA | AC-25 |
| EC-08 | reject/delete linked → no_quota | write-back สำเร็จ | XT-01/02 |

### §5.5.2 Recommended ☐ (BRD §10.2 — BA confirm SOW3.7)
| ID | กรณี | Resolution | Test |
|---|---|---|---|
| EC-09 | CSV ไม่ใช่ UTF-8 | reject + แนะนำ UTF-8 | RC-01 |
| EC-10 | CSV header ผิด | reject ทั้งไฟล์ + บอกคอลัมน์ | RC-02 |
| EC-11 | quota_number ซ้ำในไฟล์ | แถวแรกผ่าน แถวหลัง error | RC-03 |
| EC-12 | Bulk verify บางรายการถูก verify ก่อน | ข้าม นับ failed + เหตุผล | AC-23 |
| EC-13 | ตำบล CSV สะกดผิด | error รายแถว | RC-04 |
| EC-14 | สร้าง No-Member แล้วอยากผูก member ภายหลัง | Phase 2 (ยังไม่มี re-link) | — ข้าม (OOS) |
| EC-15 | self-verify (SoD) | block ERR_SOD_SELF_VERIFY (flag) | RC-05 |
| EC-16 | Double-click บันทึก | idempotency + ปุ่ม disabled | AC-26 |
| EC-17 | reject/delete แต่ member ถูกลบไปแล้ว | write-back skip + log anomaly (ไม่ error) | RC-06 |

---

## §5.6 Error Catalog
| Code | HTTP | Message (UI) | Cause |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | รายช่องตาม §5.4 | validation |
| ERR_INSUFFICIENT_ROLE | 403 | "คุณไม่มีสิทธิ์เข้าถึงส่วนนี้" | ENC |
| ERR_SOD_SELF_VERIFY | 403 | "ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง" | EC-15 (flag) |
| ERR_NOT_FOUND | 404 | "ไม่พบข้อมูลโควตา" | — |
| ERR_STALE_DATA | 409 | "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง" | version |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | "เกิดข้อผิดพลาด กรุณาลองใหม่" | key ซ้ำ body ต่าง |
| BR_QUOTA_NUMBER_DUPLICATE | 422 | "เลขโควต้านี้ถูกใช้แล้ว" | BR-AGQ-01 |
| BR_MEMBER_HAS_QUOTA | 422 | "สมาชิกนี้มีโควต้าอยู่แล้ว" | BR-AGQ-03 |
| BR_MEMBER_NOT_APPROVED | 422 | "ผูกได้เฉพาะสมาชิกที่อนุมัติแล้ว" | BR-AGQ-03 |
| BR_VERIFY_NOT_UNVERIFIED | 422 | "รายการนี้ถูกตรวจสอบไปแล้ว" | BR-AGQ-04 |
| BR_DELETE_NOT_UNVERIFIED | 422 | "ลบได้เฉพาะรายการที่รออนุมัติ" | BR-AGQ-06 |
| BR_POSTAL_CODE_MISMATCH | 422 | "รหัสไปรษณีย์ไม่ตรงกับตำบล" | BR-AGQ-11 |
| BR_CSV_HEADER_MISMATCH | 422 | "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [รายการ]" | EC-10 |
| ERR_CSV_ENCODING | 422 | "ไฟล์ต้องเป็น UTF-8 กรุณาบันทึกไฟล์ใหม่เป็น UTF-8" | EC-09 |
| ERR_CSV_INVALID_FILE | 400 | "กรุณาเลือกไฟล์ CSV เท่านั้น" / "ขนาดไฟล์ต้องไม่เกิน 5MB" | VR-08 |

---

## §5.7 Security — Preset P3 + Document Access
| Control | Implementation |
|---|---|
| S01-04 SoD | §5.3 + EC-15 (FN-06 created_by != userId) |
| S01-07 Immutable Log | FN-10 + T_quota_history append-only |
| S02-04 Data Masking | citizen_id mask list · bank/BAAC mask ตาม permission |
| S02-05 Classification | 04_DB §4.2 per-column |
| S04-05 Master Mapping | M-01 + farmer_member FK (ENG-EXT-03) |
| S05-02 Audit Fields | created/updated by/at |
| S06-03 Soft Delete | BR-AGQ-06 |
| S07-01 Export Control | error report เท่านั้น Phase 1 |
| S08-02 Document Access | เอกสารแนบเข้าถึงตาม permission + audit |

### D-CLASS Enforcement
| Layer | Confidential (phone/email/addr/bank/BAAC/docs) | Restricted (citizen_id) |
|---|---|---|
| API | ตาม ENC role | masked list · เต็ม ACL (audit) |
| UI | ตาม role | mask list เสมอ |
| Export | — | excluded |
**Wire:** Policy Center → Data Classification / Restricted Resources (OQ-F02) / Document Access / ENC (§4)

---

## §5.8 Compliance & Health
| Requirement | Implementation |
|---|---|
| PDPA | encrypt citizen_id + masking + ไม่ log PII |
| Cross-module integrity | write-back = step แยก idempotent (keep-quota, ไม่ rollback) + async retry + reconcile report (MET-03) |
| SLA (BRD §17 — business) | verify 3 วัน · list p95<3s · CSV 1,000<60s · write-back<500ms |
| **NFR technical budget (authoritative) ⭐** | **reads SER ≤ 500ms · validation VAL ≤ 300ms · writes CRE/UPT ≤ 1500ms · debounce search 300ms · skeleton loader เมื่อ page/list load > 200ms** (authoritative technical budget — คงเพิ่มจาก SLA ธุรกิจข้างบน) |
| Threshold | CSV failed >20% → banner · write-back fail → alert+retry (ห้ามเงียบ) · unverified >7 วัน → widget |
