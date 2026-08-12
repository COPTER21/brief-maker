# 05_RULES — F-ORG-001 Organization Management

> Business Rules + Validation + Edge Cases + Error Catalog + Security/Data-Classification. Source: BRD §9/§10/§16.

## §5.1 Business Rules (Tagged)
| ID | Rule | Tag | Enforce |
|---|---|---|---|
| BR-01 | branch code 5 หลัก, 00000=HQ, unique | FIXED | DB CHECK + FN-05 |
| BR-02 | code unique ต่อ entity | FIXED | UNIQUE + FN-05 |
| BR-03 | department.division_id nullable (สังกัด/ไม่สังกัดสายงาน) | FIXED | schema |
| BR-04 | position ผูก dept หรือ division หรือไม่ผูก (ทั้งคู่ nullable; แสดง dept ก่อน) | CONFIGURABLE | FN-09 (precedence — OQ-2) |
| BR-05 | tier ∈ ชุดของ track (M1-7/S1-6/E1-5) | CONFIGURABLE | FN-05 + config tier_set |
| BR-06 | parent ≠ self/descendant (no cycle) — dept & position | FIXED | FN-05 + DB trigger |
| BR-07 | ลบ division → null child refs | FIXED | ENG-ORG-03 |
| BR-08 | ลบ dept/position → reparent children | FIXED | ENG-ORG-03 |
| BR-09 | inactive ถูกซ่อนจาก dropdown ระบบอื่น | FIXED | FN-08 filter |
| BR-10 | CSV import: Replace/Merge; ref by code; cross-entity ต้องมีก่อน; same-entity parent ∈ batch(Replace)/batch∪existing(Merge); no self-ref | FIXED | ENG-ORG-02 |
| BR-11 | code auto-gen pattern | CONFIGURABLE | FN-06 (Document Numbering) |
| BR-12 | headcount/salary ≥ 0; salary_min ≤ salary_max | WARNING | FN-05 (OQ-4) |
| BR-13 | required ขั้นต่ำ = name_th | FIXED | FN-05 |
| BR-14 | โลโก้บริษัท: image (PNG/JPG/SVG) + ≤2MB; optional; 1 โลโก้/บริษัท; ลบได้ | CONFIGURABLE | FN-13/FN-14 + config `logo.allowed_mime`/`logo.max_size` |
| BR-GOV | create/edit/inactivate/delete เตรียม approval_chain + audit; enforce ผ่าน DOA | DYNAMIC | Pre-DOA fields (R-GOV) |

## §5.2 Validation Rules
| Field/Action | เงื่อนไข | ประเภท | ข้อความ |
|---|---|---|---|
| name_th | ว่าง | Error | "กรุณาระบุชื่อ (ไทย)" |
| code | ซ้ำ | Error | "รหัสนี้มีอยู่แล้ว" |
| parent | = self/descendant | Error | กรอง dropdown + "เลือกแผนก/ตำแหน่งนี้ไม่ได้" |
| tier | ไม่อยู่ใน track | Error | "ระดับไม่อยู่ในสายอาชีพนี้" |
| FK (division/branch/dept) | ไม่มีจริง | Error | "ไม่พบ[entity] ที่อ้างถึง" |
| salary | min>max | Warning | "เงินเดือนต่ำสุดมากกว่าสูงสุด" |
| logo (อัปโหลด) | ชนิดไม่ใช่ image | Error | "ไฟล์ต้องเป็นรูปภาพ (PNG/JPG/SVG)" |
| logo (อัปโหลด) | ขนาด > 2MB | Error | "ไฟล์ใหญ่เกิน 2MB" |

## §5.3 Edge Cases (จาก BRD §10 + QC)
- EC-01 ลบ division มีแผนก/ตำแหน่งสังกัด → null refs (ทดสอบผ่าน)
- EC-02 ลบ dept มีแผนกย่อย → ย่อยเลื่อนขึ้น parent
- EC-03 chart มี cycle/orphan/self-parent → coverage-pass ไม่ loop ไม่หล่น (ENG-ORG-01)
- EC-04 dept.division_id ชี้สายงานไม่มีจริง → แสดงใต้บริษัทโดยตรง
- EC-05 position ผูกสายงานไม่มีแผนก (CFO/CTO) → tag "สายงาน"
- EC-06 CSV ref code ไม่มี → row error (ข้าม), ไม่ fail ทั้งไฟล์
- EC-07 CSV Replace parent_code ไม่อยู่ใน batch → row error
- EC-08 CSV ไม่มีคอลัมน์ code/name_th → reject ทั้งไฟล์
- EC-09 concurrent edit → optimistic lock ด้วย version (OQ-5)
- EC-10 toggle inactive record ที่ระบบอื่นอ้างถึง → ซ่อนจาก dropdown แต่ snapshot เดิมยังอ้างได้
- EC-11 อัปโหลดโลโก้ผิดชนิด/ใหญ่เกิน → ERR_LOGO_TYPE/ERR_LOGO_SIZE (ไม่บันทึก)
- EC-12 ลบโลโก้ → hero กลับเป็นไอคอนเริ่มต้น; ไม่กระทบเอกสาร/รายงานที่ออกไปแล้ว
- EC-13 เลือกไฟล์โลโก้แล้วปิด drawer ก่อนบันทึก → draft ถูกยกเลิก (ของจริงไม่เปลี่ยน)

## §5.4 Error Catalog
| Code | HTTP | ความหมาย |
|---|---|---|
| ERR_VALIDATION_FAILED | 400 | validate ไม่ผ่าน |
| ERR_DUPLICATE_CODE | 409 | code ซ้ำ |
| ERR_CYCLE_DETECTED | 422 | parent เป็น self/descendant |
| ERR_TIER_TRACK_MISMATCH | 422 | tier ไม่ตรง track |
| ERR_FK_NOT_FOUND | 422 | FK ref ไม่มี |
| ERR_IMPORT_MISSING_COLUMN | 400 | CSV ขาด code/name_th |
| ERR_LOGO_TYPE | 400 | โลโก้ชนิดไฟล์ไม่รองรับ |
| ERR_LOGO_SIZE | 400 | โลโก้ใหญ่เกิน 2MB |
| ERR_INSUFFICIENT_ROLE | 403 | สิทธิ์ไม่พอ (IAM) |
| ERR_VERSION_CONFLICT | 409 | optimistic lock (OQ-5) |

## §5.7 Security & Data Classification Enforcement

### Security (Preset P3 — Master Data, 10 controls)
S01-04 SoD (Maker≠Approver, ผู้ลบ≠ผู้สร้าง) · S01-07 Immutable Master Data Log (before/after ทุก mutation — ห้ามลบ) · S02-05 Classification Tags · S03-02 Versioning · S04-05 Naming convention (code) · S06-03 Audit content (Who/What/When/Where/Result) · S07-06 PII Tagging/Masking · S11-02 Ticket Enforcement.
**Governance checkpoints:** User Access (F-IAM-02) + DOA (F-PC-DOA-01, Pre-DOA).

### §5.7-D-CLASS Data Classification Enforcement
- **Restricted** (position.salary_min/max): UI ซ่อนเว้นมี ACL · API omit เว้น role + log access · Export excluded + require approval · register Restricted Resources (OQ-1).
- **Confidential** (tax_id, reg_no, head/deputy/manager/contact, email, phone): mask `***` ถ้า role ไม่ผ่าน · excluded column ใน export ถ้า role ไม่ผ่าน.
- **Public** (company name/website): แสดง/export ได้ทุก role.
- **Internal** (default — org structure/status/audit): authenticated user เห็นได้.
- Default = Internal (ห้าม default Public). Enforce ที่ DB(§4.6.2)/API(§4.6.3)/UI(§4.6.4)/Export(§4.6.5).
