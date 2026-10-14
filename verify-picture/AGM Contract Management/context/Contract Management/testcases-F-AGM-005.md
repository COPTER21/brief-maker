# AI Test Cases — F-AGM-005 Contract Management (จัดการสัญญาส่งอ้อย)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `contract-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ HTML + UI Brief §9 แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side / optimistic lock / concurrency / SoD / RBAC / license-write rollback จริง) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-005 (AGM/Contract — WKN) |
| App entry | เปิดไฟล์ `contract-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/contracts` (list — default) · `#/contracts/:contract_id` (Detail drawer, refresh-safe · ใช้ contract_id เช่น `CT-2569-001`) |
| ที่มา | FRD_F-AGM-005_Pack (7 ไฟล์ STANDARD) · BRD APPROVED (LOCK-01..10) · HTML v1.0 (audit FAIL=0) · UI_BRIEF_F-AGM-005 |
| จำนวนเคส | 56 เคส / 9 groups (ไม่มี I group — feature นี้ไม่มี CSV import; legacy ไม่มี) |
| Scope Lock | LOCK-01..10 (00_OVERVIEW §0.11 ← BRD §3.4) — ทุกข้อมีเคส verify (ดู Ledger) |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า = ข้อมูล reset กลับ seed 8 สัญญา + 4 โควตา + 8 แปลง + 14 รอบปลูก — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh (F5) ก่อนเริ่ม |
| Cross-module ⭐⭐ | **READ + WRITE-BACK** — Contract อ่าน Quota (`QUOTAS`/`findQuota`) + Plot (`PLOTS`/`plotsForQuota`) + Crop verified (`CROPS`/`cropsForQuota`) **และเขียนกลับ** `crop.license_status` ผ่าน `setCropsLicense()`: create→`'contracted'` · reject/delete→`'none'` · approve→keep · simulate in-memory (D-03) · ระบบจริง = ENG-EXT-AGM PATCH + retry ที่ SIT |

**Seed ตั้งต้น (หลัง refresh — 8 สัญญา CT-2569-001..008):**
| เลขสัญญา | โควตา | เกษตรกร | ประเภทสัญญา | รวมตัน | แปลง/รอบ | สถานะ | อายุ(วัน) | รอบปลูก · type-specific |
|---|---|---|---|---|---|---|---|---|
| CT-2569-001 | QT-2569-001 | สมหญิง รักดี | สัญญาตันสูญเปล่า | 80.00 | 1 แปลง · 1 รอบ | **รอการตรวจสอบ** | 2 | CRP-…0003 · แนบ contract_ct001_scan.pdf |
| CT-2569-002 | QT-2569-002 | สุรพล เก่งการไร่ | สัญญาส่งเสริม | 350.00 | 1 · 2 | **อนุมัติแล้ว** | 20 | CRP-…0004/0005 · support[ปุ๋ยเคมี สูตร 15-15-15, ยากำจัดวัชพืช] · note "เอกสารครบถ้วน" · แนบ 2 |
| CT-2569-003 | QT-2569-003 | ทองดี พูลผล | สัญญาโปรโมชั่น โปร 7 วัน | 60.00 | 1 · 1 | **ปฏิเสธ** | 12 | CRP-…0007 · promo "1-7 ม.ค. 2569" |
| CT-2569-004 | QT-2569-004 | ประนอม ใจเพชร | สัญญาโปรโมชั่นเครน | 150.00 | 1 · 1 | **รอการตรวจสอบ** | 1 | CRP-…0009 · crane "เครน B (20 ตัน)" |
| CT-2569-005 | QT-2569-004 | ประนอม ใจเพชร | สัญญาตกเขียว | 110.00 | 2 · 1 | **รอการตรวจสอบ** | 9 (ค้าง) | CRP-…0011 · plots[PLT-…007,008] · แนบ green_purchase_agreement.pdf |
| CT-2569-006 | QT-2569-003 | ทองดี พูลผล | สัญญาโปรโมชั่นเครน | 95.00 | 1 · 1 | **ปฏิเสธ** | 15 | CRP-…0013 · crane "เครน A (10 ตัน)" |
| CT-2569-007 | QT-2569-001 | สมหญิง รักดี | สัญญาส่งเสริม | 60.00 | 1 · 1 | **อนุมัติแล้ว** | 25 | CRP-…0012 · support[ค่าเตรียมดิน] |
| CT-2569-008 | QT-2569-002 | สุรพล เก่งการไร่ | สัญญาตกเขียว | 130.00 | 1 · 1 | **รอการตรวจสอบ** | 5 | CRP-…0014 · plots[PLT-…004] |

สรุป: **รอการตรวจสอบ 4** (CT-001/004/005/008 · ค้างเกิน 7 วัน **1 รายการ** = CT-005 age9) · **อนุมัติแล้ว 2** (CT-002/007) · **ปฏิเสธ 2** (CT-003/006) · สัญญาทั้งหมด **8** (deleted ซ่อน) · ครบ 5 ประเภทสัญญา
- CT-003 reject_reason = "เอกสารสิทธิ์แปลงไม่ครบถ้วน กรุณาแนบเพิ่มเติมแล้วยื่นใหม่" · CT-006 reject_reason = "ปริมาณตันไม่สอดคล้องกับรอบปลูกที่ตรวจสอบ"
- ลำดับในตาราง (ไม่ sort) = CT-001 → CT-008 · สร้างใหม่ `unshift` ขึ้นบนสุด · `nextContractCode()` ตัวถัดไป = **CT-2569-009**
> ⚠ **Write-back signature:** crops ของสัญญา active (waiting/verified) ถูกตั้ง `license_status='contracted'` ตอน seed → **contracted 7 รอบ** (CRP-…0003/0004/0005/0009/0011/0012/0014) · **none 7 รอบ** (CRP-…0001/0002/0006/0008/0010/0013 + 0007 คืนแล้วจาก reject) — พิสูจน์ 1 crop : 1 active contract + กันเลือกซ้ำได้ทันที

**Seed โควตา (4 รายการ — `QUOTAS` const, READ-ONLY · verified ทุกตัว):**
| เลขโควตา | เกษตรกร | เบอร์ | เลขบัตร (masked) | แปลงของโควตา | รอบปลูกที่เลือกได้ (license=none) | รอบปลูก greyed (contracted) |
|---|---|---|---|---|---|---|
| QT-2569-001 | สมหญิง รักดี | 0823456789 | 3-XXXX-XXXX-XX-2 | PLT-…001, PLT-…002 | CRP-…0001 (120), CRP-…0002 (90) | CRP-…0003, CRP-…0012 |
| QT-2569-002 | สุรพล เก่งการไร่ | 0945678901 | 3-XXXX-XXXX-XX-4 | PLT-…003, PLT-…004 | CRP-…0006 (100) | CRP-…0004, CRP-…0005, CRP-…0014 |
| QT-2569-003 | ทองดี พูลผล | 0889012345 | 3-XXXX-XXXX-XX-8 | PLT-…005, PLT-…006 | CRP-…0007 (60), CRP-…0008 (75), CRP-…0013 (95) | — (ไม่มี contracted) |
| QT-2569-004 | ประนอม ใจเพชร | 0833334444 | 4-XXXX-XXXX-XX-3 | PLT-…007, PLT-…008 | CRP-…0010 (90) | CRP-…0009, CRP-…0011 |
> `cropsForQuota(qid)` คืน verified crops ของโควตา (ทุก crop = verified) · contracted จะถูก grey + " · ทำสัญญาแล้ว" ใน checklist (กันเลือกซ้ำ) · `plotsForQuota(qid)` คืนแปลงทุกแปลงของโควตา

**Users:** เจ้าหน้าที่สัญญา = **สมพร วงศ์ทะเบียน** (`CURRENT_USER` — create/edit/delete) · ผู้อนุมัติ = **ธนพล อนุมัติ** (`CHECKER` — approve/reject/bulk). prototype เป็น user เดียว (ไม่มี role switching — RBAC/SoD = SIT)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L — รายการ / ค้นหา / กรอง(สถานะ+ประเภท) / เรียง / ส่งออก / pagination | TC-L01..L08 (8) | สูง |
| C — สร้างสัญญา + build-path cascade + 5 ประเภทสัญญา + validation | TC-C01..C12 (12) | สูงสุด |
| V — อนุมัติ / ปฏิเสธ (เดี่ยว) | TC-V01..V05 (5) | สูง |
| B — Bulk อนุมัติ/ปฏิเสธ | TC-B01..B03 (3) | สูง |
| E — แก้ไข (type-specific/เอกสาร · quota/plots/crops read-only) | TC-E01..E04 (4) | สูง |
| D — ลบ (soft delete + attachments + revert license) | TC-D01..D03 (3) | สูง |
| W — Detail / 5 tabs / snapshot / ประวัติ (audit + license events) | TC-W01..W05 (5) | สูง |
| **X — Cross-module WRITE-BACK ⭐⭐ (contracted/none + available read + 1 crop:1 contract)** | TC-X01..X06 (6) | **สูงสุด** |
| S — System / simulate (optimistic lock · concurrency · SoD · license-write rollback) | TC-S01..S04 (4) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1 ← BRD §7)
| item | cases |
|---|---|
| AC-01 เลือก quota → farmer snapshot | TC-C01, TC-C03, TC-X05 |
| AC-02 เลือกแปลง(≥1) + รอบปลูก verified(≥1) → รวม total_tons auto · fields ปลดล็อก | TC-C01, TC-C02, TC-C03 |
| AC-02b quota/plots/crops ไม่ครบ → "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" block | TC-C08, TC-C02 |
| AC-03 เลือกประเภทสัญญา 1 ใน 5 → type-specific field ปรากฏ | TC-C04, TC-C05, TC-C06, TC-C07 |
| AC-04 type=support → support_items repeater | TC-C04, TC-E03 |
| AC-05 type=promotion-7 → เลือกช่วงโปรโมชั่น (บังคับ) | TC-C05 |
| AC-06 type=promotion-crane → เลือกเครน (บังคับ) | TC-C06 |
| AC-07 crop license=contracted → กันเลือกซ้ำ "รอบปลูกนี้ทำสัญญาแล้ว" | TC-X06 |
| AC-08 ยืนยันสร้าง → toast "สร้างสัญญาสำเร็จ — [เลขสัญญา]" + status รอการตรวจสอบ + crop license → contracted + audit | TC-C01, TC-X01 |
| AC-09 upload attachments → preview | TC-C11 |
| AC-10 search(contract_id/quota/farmer) + filter status(3)+type(5) · ไม่พบ → "ไม่พบรายการที่ค้นหา" | TC-L02, TC-L03, TC-L04, TC-L08 |
| AC-11 แก้ type-specific/attachments + save → version++ + audit (status คงเดิม) | TC-E01, TC-E03 |
| AC-12 quota/plots/crops บนหน้า edit = read-only | TC-E02 |
| AC-13 waiting + อนุมัติ (ไม่ต้องมีเหตุผล) + Confirm → toast "อนุมัติเรียบร้อย" + pill เขียว + approved_by/at + audit | TC-V01 |
| AC-14 อนุมัติ → crop license คง contracted | TC-V01, TC-X04 |
| AC-15 ปฏิเสธ ไม่กรอกเหตุผล → "กรุณากรอกเหตุผลในการปฏิเสธ" block | TC-V02 |
| AC-16 ปฏิเสธ + reason → pill แดง + reject_reason แสดง + crop license → none + audit | TC-V03, TC-X02 |
| AC-17 Bulk: เลือกทั้งหมด = เฉพาะ waiting · อนุมัติกลุ่ม → summary | TC-B01 |
| AC-18 Bulk reject = เหตุผลบังคับ (ใช้ร่วม) · skip non-waiting | TC-B02, TC-B03 |
| AC-18b verified/reject → approve ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม) | TC-V05, TC-S02 (simulate) |
| AC-19 detail tabs (5) + snapshot card | TC-W01 |
| AC-20 tab รอบปลูก = crop list + tons · tab ประวัติ = audit + license write events | TC-W02, TC-W03 |
| AC-20b deep-link contract ไม่มี/deleted → "ไม่พบข้อมูลสัญญาที่เลือก" + กลับ list | TC-W04, TC-D02 |
| AC-21 ลบ + confirm → toast "ลบสัญญาแล้ว" + ลบ attachments + audit | TC-D01, TC-D03 |
| AC-22 ลบสัญญา → crop license revert none | TC-D01, TC-X03 |
| AC-23 sort + export CSV + pagination | TC-L05, TC-L06, TC-L07 (export simulate) |

### Cross-Module (06_TESTS §6.9) ⭐⭐ READ + WRITE-BACK
| XT | Scenario | Module | Case |
|---|---|---|---|
| XT-01 | สร้างสัญญา → crop.license_status → contracted ทุก crop ที่ผูก + history | Crop (write) | TC-X01, TC-C01 |
| XT-02 | ปฏิเสธสัญญา → crop.license_status → none (revert) ทุก crop | Crop (write) | TC-X02, TC-V03 |
| XT-03 | ลบสัญญา → crop.license_status → none | Crop (write) | TC-X03, TC-D01 |
| XT-04 | available-items → คืนเฉพาะ plot/crop verified ของโควตา + crop license≠contracted | Plot+Crop (read) | TC-X05, TC-C03 |
| XT-05 | crop ผูกสัญญาแล้ว → กันเลือกซ้ำ (1 crop : 1 active contract) | Crop | TC-X06 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-AGT-01 build path: โควตา → แปลง(≥1) → รอบปลูก verified(≥1) → ประเภทสัญญา | TC-C01, TC-C02, TC-C03, TC-X05 |
| BR-AGT-02 total_tons รวมจาก crops · plot_count/crop_count นับ | TC-C03, TC-C01, TC-W02 |
| BR-AGT-03 create → Waiting for verify เสมอ | TC-C01, TC-X01 |
| BR-AGT-04 approve/reject: waiting เท่านั้น · approve ไม่ต้องมีเหตุผล · reject reason บังคับ · เดี่ยว+bulk | TC-V01, TC-V02, TC-B01, TC-B02 |
| BR-AGT-05 **write-back**: create→contracted · reject→none · approve→keep | TC-X01, TC-X02, TC-X04 |
| BR-AGT-06 5 contract types + type-specific fields (เก็บเฉพาะ type ที่ตรง) | TC-C04, TC-C05, TC-C06, TC-C07, TC-E03 |
| BR-AGT-07 1 crop : 1 active contract (กัน crop license=contracted เลือกซ้ำ) | TC-X06 |
| BR-AGT-08 delete + ลบ attachments + audit | TC-D01, TC-D03 |
| BR-AGT-09 audit ทุก mutation (+ bulk count + license write) | TC-W03, TC-B01, TC-X01 |
| BR-AGT-10 optimistic lock + idempotency | TC-C12, TC-S01 (simulate) |

### Validation (05_RULES §5.4 VR-01..05)
| VR | cases |
|---|---|
| VR-01 quota+plots+crops+type required (plots≥1, crops≥1) → "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" | TC-C08, TC-C02 |
| VR-02 crops verified + ของโควตา → "เลือกรอบปลูกที่ตรวจสอบแล้ว" | TC-X05, TC-C03 (mock ทุก crop verified — server enforce) |
| VR-03 crop license ≠ contracted → "รอบปลูกนี้ทำสัญญาแล้ว" | TC-X06 |
| VR-04 reject_reason บังคับเมื่อ reject → "กรุณากรอกเหตุผลในการปฏิเสธ" | TC-V02, TC-B02 |
| VR-05 type-specific required → "เลือกช่วงโปรโมชั่น"/"เลือกเครน"/"เลือกรายการส่งเสริม" | TC-C05, TC-C06, TC-C10 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 quota/plots/crops ไม่ครบ → block | TC-C08, TC-C02 |
| EC-02 crop ไม่ verified → excluded จาก available-items | TC-X05 (mock ทุก crop verified → server, ต้อง simulate ฝั่ง reject) |
| EC-03 crop license=contracted → กันเลือกซ้ำ | TC-X06 |
| EC-04 type-specific field ไม่ครบ → VR-05 block | TC-C05, TC-C06, TC-C10 |
| EC-05 approve → ไม่ต้องมีเหตุผล → Verified | TC-V01 |
| EC-06 reject ไม่ใส่เหตุผล → block | TC-V02, TC-B02 |
| EC-07 reject → crop license revert none | TC-X02, TC-V03 |
| EC-08 bulk เลือกรวม non-waiting → skip + summary | TC-B03, TC-B01 |
| EC-09 stale edit → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| EC-10 concurrent approve (status เปลี่ยน) → 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (ต้อง simulate) |
| EC-11 license write fail → rollback + retry queue | TC-S04 (ต้อง simulate) |
| EC-12 delete → crop license revert none (เหมือน reject) | TC-X03, TC-D01 |
| EC-13 double-submit create → idempotency → 1 รายการ | TC-C12 |
| EC-14 deep-link contract ไม่มี/deleted → "ไม่พบข้อมูลสัญญาที่เลือก" + กลับ list | TC-D02, TC-W04 |

### Error catalog (05_RULES §5.6 — ที่มีผลบน UI prototype)
| error | cases |
|---|---|
| ERR_MISSING_FIELDS "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" | TC-C08, TC-C02 |
| ERR_CROP_NOT_VERIFIED "เลือกรอบปลูกที่ตรวจสอบแล้ว" | TC-X05, TC-S04 (server-enforced — simulate) |
| ERR_CROP_ALREADY_CONTRACTED "รอบปลูกนี้ทำสัญญาแล้ว" | TC-X06 |
| (type ไม่เลือก) "เลือกประเภทสัญญา" | TC-C09 |
| (type-specific) "เลือกช่วงโปรโมชั่น" / "เลือกเครน" / "เลือกรายการส่งเสริม" | TC-C05, TC-C06, TC-C10 |
| ERR_REJECT_NO_REASON "กรุณากรอกเหตุผลในการปฏิเสธ" | TC-V02, TC-B02 |
| (verify no result) "กรุณาเลือกผลการตรวจสอบ" | TC-V04 |
| (verify no waiting selected) "เลือกได้เฉพาะรายการที่รอการตรวจสอบ" | TC-V05, TC-B01 |
| ERR_STALE(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (simulate) |
| ERR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (simulate) |
| ERR_NOT_FOUND "ไม่พบข้อมูลสัญญาที่เลือก" | TC-D02, TC-W04 |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases / สถานะ |
|---|---|
| เจ้าหน้าที่สัญญา: create/edit/delete = allow | TC-C01, TC-E01, TC-D01 (prototype user=สมพร วงศ์ทะเบียน) |
| ผู้อนุมัติ: +approve/reject/bulk = allow | TC-V01, TC-B01 (prototype verify actor=ธนพล อนุมัติ) |
| ปุ่มซ่อนตาม RBAC (เจ้าหน้าที่สัญญาไม่เห็น อนุมัติ/ปฏิเสธ) | TC-S03 (ต้อง simulate — prototype ไม่มี role switching) |
| SoD self-approve block (OQ-CT6) | TC-S03 (ต้อง simulate) |

### Scope Lock (00_OVERVIEW §0.11 ← BRD §3.4)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | capability legacy 100% (create/edit/approve/reject/bulk/delete/search) | ทั้ง suite — ตัวแทน: TC-C01, TC-V01, TC-B01, TC-E01, TC-D01, TC-W01, TC-L02 |
| LOCK-02 | canonical **3-state** machine (รอการตรวจสอบ/อนุมัติแล้ว/ปฏิเสธ) | TC-V01, TC-V03, TC-W01, TC-L01 |
| LOCK-03 | **build path (quota→plots≥1→crops verified≥1→type) + field gating** ⭐⭐ | TC-C01, TC-C02, TC-C03 |
| LOCK-04 | **5 contract types + type-specific** ⭐ | TC-C04, TC-C05, TC-C06, TC-C07 |
| LOCK-05 | aggregate tons auto จาก crops | TC-C03, TC-C01 |
| LOCK-06 | approve/reject (reject reason บังคับ) เดี่ยว+bulk | TC-V01, TC-V02, TC-B01, TC-B02 |
| LOCK-07 | **write-back crop license (contracted/none)** ⭐⭐ | TC-X01, TC-X02, TC-X03, TC-X04 |
| LOCK-08 | **1 crop : 1 active contract** ⭐ | TC-X06 |
| LOCK-09 | delete + ลบ attachments | TC-D01, TC-D03 |
| LOCK-10 | optimistic + idempotency + audit | TC-C12, TC-S01, TC-W03 |

### UI States (§8 State-Driven Matrix — canonical 3)
| item | cases |
|---|---|
| loaded / filtered / filter-empty | TC-L01, TC-L02, TC-L04 |
| stats 4 การ์ด (ค้างเกิน 7 วัน 1) | TC-L01 |
| pill 3 สถานะ (รอการตรวจสอบ/อนุมัติแล้ว/ปฏิเสธ) | TC-L01, TC-V01, TC-V03 |
| checkbox waiting selectable / อื่น disabled | TC-B01, TC-V05 |
| snapshot card (orange) + ดูโควตา | TC-W01 |
| **field gating (locked จนครบ quota+plot+crop)** ⭐⭐ | TC-C02 |
| **type-specific dynamic block (support repeater / promo / crane)** ⭐ | TC-C04, TC-C05, TC-C06 |
| detail actions ตามสถานะ (อนุมัติ/ปฏิเสธ เฉพาะ waiting) | TC-V05, TC-W01 |
| submitting state ("กำลังบันทึก…"/"กำลังดำเนินการ…") | TC-C01, TC-V01, TC-D01 |
| sort / pagination footer | TC-L05, TC-L06 |

**Manifest cross-check (FRD §0.12):** Stories 9/9 (US-01..09) · Rules BR-AGT-01..10 10/10 · VR-01..05 5/5 · EC-01..14 14/14 · XT-01..05 5/5 · LOCK-01..10 10/10 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — สัญญาถูกต้อง (happy — ผูก QT-2569-001 + PLT-2569-001 + CRP-2569-0000001 + ตันสูญเปล่า)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาโควตา (Quota Id) | เลือก **QT-2569-001 · สมหญิง รักดี** *(sub "0823456789 · 3-XXXX-XXXX-XX-2")* |
| เลือกแปลง (ของโควตา) | ติ๊ก **PLT-2569-001** *(sub "99 หมู่ 3 · วังขนาย ท่าม่วง กาญจนบุรี 71110")* |
| เลือกรอบปลูก (ตรวจแล้ว ของโควตา) | ติ๊ก **CRP-2569-0000001** *(sub "PLT-2569-001 · 120.00 ตัน" · license none — เลือกได้)* |
| เลือกประเภทสัญญา | **สัญญาตันสูญเปล่า** (price-per-ton — ไม่มี type-specific field) |
| รวม (auto) | **120.00 ตัน · 1 รอบปลูก** (จาก sumCrops) |
| เอกสารแนบ | คลิก **แนบเอกสาร** (จำลอง) |

### ชุด B — ค่าผิดสำหรับ negative (ต้องผ่าน build-path ก่อนตามเคสระบุ)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | เลือกประเภทสัญญา | *(คง "— เลือกประเภทสัญญา —")* → ยืนยันสร้าง | เลือกประเภทสัญญา |
| B2 | เลือกช่วงโปรโมชั่น (promotion-7) | *(คง "— เลือกช่วงโปรโมชั่น —")* → ยืนยันสร้าง | เลือกช่วงโปรโมชั่น |
| B3 | เครน (promotion-crane) | *(คง "— เลือกเครน —")* → ยืนยันสร้าง | เลือกเครน |
| B4 | รายการส่งเสริม (support) | *(0 รายการ)* → ยืนยันสร้าง | เลือกรายการส่งเสริม |
| B5 | quota+plots+crops | *(ไม่เลือกเลย → ยืนยันสร้าง)* | กรุณาตรวจสอบข้อมูลให้ครบถ้วน |
| B6 | เหตุผลในการปฏิเสธ | *(เว้นว่าง → ยืนยัน)* | กรุณากรอกเหตุผลในการปฏิเสธ |
| B7 | ผลตรวจสอบ | *(ไม่เลือก radio → ยืนยัน)* | กรุณาเลือกผลการตรวจสอบ |

### ไฟล์ทดสอบ (Attachments)
> attachments เป็น **simulated** (ปุ่ม **แนบเอกสาร** สร้างชื่อไฟล์ `contract_doc_N_[ts].pdf` เอง · D-05) — ไม่ต้องเตรียมไฟล์จริง
| จุด | ค่า seed |
|---|---|
| CT-2569-001 เอกสารแนบ | `contract_ct001_scan.pdf` (1) |
| CT-2569-002 เอกสารแนบ | `support_plan.pdf`, `id_card.jpg` (2) |
| CT-2569-005 เอกสารแนบ | `green_purchase_agreement.pdf` (1) |
| create แนบใหม่ | `contract_doc_1_[timestamp].pdf` (toast "จำลองแนบเอกสาร (PDF/JPG ≤5MB)") |

---

## Test Cases

## Group L — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination (P-01)

### TC-L01 — เปิดหน้า list + stats widgets (happy)
- group: L · ความสำคัญ: สูง · trace: 01_UI P-01 / UI state loaded / D-01 stats
- Setup: role=เจ้าหน้าที่สัญญา (default) · seed=default 8 สัญญา (refresh)
- Start: OPEN `#/contracts`
- ผ่านเมื่อ: หน้า list + สถิติ 4 การ์ดแสดงเลขตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/contracts` | — | หัวข้อ **จัดการสัญญาส่งอ้อย** + count **8 รายการ** · sub "ทะเบียนสัญญาส่งอ้อย · รวมรอบปลูกที่ตรวจแล้ว · อนุมัติเดี่ยว/กลุ่ม" · breadcrumb "เกษตรกรรม › จัดการสัญญาส่งอ้อย" · sidebar **จัดการสัญญาส่งอ้อย** active · user chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ทะเบียนสัญญา · WKN" | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **สัญญาทั้งหมด 8** (meta "ไม่รวมที่ลบ") · **รอการตรวจสอบ 4** (meta ส้ม "ค้างเกิน 7 วัน 1 รายการ") · **อนุมัติแล้ว 2** (meta "สัญญามีผล") · **ปฏิเสธ 2** (meta "คืนสิทธิ์รอบปลูกแล้ว") | ☐ |
| 3 | VERIFY ปุ่มบน page header (ขวาบน) | — | เรียงซ้าย→ขวา: **ตรวจสอบที่เลือก (0)** (disabled) · **สร้างสัญญา** (ปุ่มแดง primary ขวาสุด) | ☐ |
| 4 | VERIFY ตาราง | — | 9 คอลัมน์: ☑, เลขสัญญา (mono แดง), เลขโควตา, เกษตรกร, ประเภทสัญญา, รวมตัน, **แปลง / รอบปลูก**, สถานะ, การดำเนินการ · pill 3 สี ครบ (รอการตรวจสอบ เหลือง / อนุมัติแล้ว เขียว / ปฏิเสธ แดง) | ☐ |
| 5 | VERIFY แถว CT-2569-001 | — | เลขโควตา QT-2569-001 · สมหญิง รักดี · **สัญญาตันสูญเปล่า** · รวมตัน **80.00** · **1 แปลง · 1 รอบ** · pill เหลือง **รอการตรวจสอบ** · คอลัมน์การดำเนินการมีไอคอน **ดินสอ + ถังขยะ** | ☐ |
| 6 | VERIFY footer ตาราง | — | ข้อความ **1 – 8 จาก 8 รายการ** · หน้า 1 active | ☐ |

### TC-L02 — ค้นหา (debounce 300ms, 3 field) (happy — AC-10)
- group: L · ความสำคัญ: สูง · trace: AC-10 / US-09 / search contract_id/quota/farmer
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`
- ผ่านเมื่อ: ค้นได้ contract_id/quota/farmer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "CT-2569-003" → ช่องค้นหา (placeholder "ค้นหา เลขสัญญา / โควตา / เกษตรกร") | เลขสัญญา | รอ ~0.3s ตารางเหลือ 1 แถว: CT-2569-003 ทองดี พูลผล (pill แดง **ปฏิเสธ**) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** แล้ว TYPE "QT-2569-002" | เลขโควตา | เหลือ 2 แถว (CT-2569-002, CT-2569-008 — ผูกโควตา QT-2569-002) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** แล้ว TYPE "ทองดี" | ชื่อเกษตรกร | เหลือ 2 แถว (CT-2569-003, CT-2569-006 ทองดี พูลผล) | ☐ |
| 4 | CLICK **ล้างตัวกรอง** แล้ว TYPE "สมหญิง" | ชื่อเกษตรกร | เหลือ 2 แถว (CT-2569-001, CT-2569-007 สมหญิง รักดี) | ☐ |

### TC-L03 — กรองสถานะ(3) + ประเภทสัญญา(5) (happy — AC-10)
- group: L · ความสำคัญ: สูง · trace: AC-10 / filter status(3)+type(5)
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **รอการตรวจสอบ** | — | เหลือ 4 แถว ทุกแถว pill เหลือง (CT-001/004/005/008) · footer "1 – 4 จาก 4 รายการ" | ☐ |
| 2 | SELECT dropdown สถานะ = **อนุมัติแล้ว** | — | เหลือ 2 แถว (CT-002, CT-007) pill เขียว **อนุมัติแล้ว** | ☐ |
| 3 | SELECT dropdown สถานะ = **ปฏิเสธ** | — | เหลือ 2 แถว (CT-003, CT-006) pill แดง **ปฏิเสธ** | ☐ |
| 4 | CLICK **ล้างตัวกรอง** → SELECT dropdown ประเภทสัญญา = **สัญญาโปรโมชั่นเครน** | — | เหลือ 2 แถว (CT-004, CT-006) · dropdown ประเภทมี "ทุกประเภทสัญญา" + 5 ตัวเลือก (สัญญาตันสูญเปล่า/ส่งเสริม/โปรโมชั่น โปร 7 วัน/โปรโมชั่นเครน/ตกเขียว) | ☐ |
| 5 | SELECT ประเภทสัญญา = **สัญญาตกเขียว** | — | เหลือ 2 แถว (CT-005, CT-008) ประเภท **สัญญาตกเขียว** | ☐ |

### TC-L04 — ค้นหาไม่เจอ → empty state (edge — AC-10)
- group: L · ความสำคัญ: กลาง · trace: AC-10 filter-empty
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีสัญญานี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state: **ไม่พบรายการที่ค้นหา** + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty state) | — | ตารางกลับมา 8 รายการ | ☐ |

### TC-L05 — Sort คอลัมน์ (AC-23)
- group: L · ความสำคัญ: ต่ำ · trace: AC-23 / sortBy contract_id/total_tons
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **รวมตัน** | — | แถวเรียงน้อย→มาก (60.00 = CT-003/CT-007 บนสุด → 350.00 = CT-002 ล่างสุด) | ☐ |
| 2 | CLICK หัวคอลัมน์ **รวมตัน** อีกครั้ง | — | เรียงกลับ มาก→น้อย (350.00 CT-002 บนสุด) | ☐ |
| 3 | CLICK หัวคอลัมน์ **เลขสัญญา** | — | เรียงตาม contract_id (CT-2569-001 บนสุด) | ☐ |
| 4 | VERIFY คอลัมน์อื่น | — | เลขโควตา/เกษตรกร/ประเภทสัญญา/แปลง·รอบ/สถานะ **ไม่มี** cursor sortable (มีเฉพาะ เลขสัญญา + รวมตัน) | ☐ |

### TC-L06 — Pagination footer + row-click เปิด Detail (AC-23)
- group: L · ความสำคัญ: ต่ำ · trace: AC-23 / row-click = openView(contract_id)
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (8 < 20/หน้า — หน้าเดียว)
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ pagination | — | ปุ่มหน้า **1** (active สีแดง) · ลูกศรซ้าย/ขวา disabled (หน้าเดียว) | ☐ |
| 2 | CLICK กลางแถว CT-2569-002 (ไม่โดน checkbox/ไอคอน) | — | Detail drawer เปิด eyebrow "สัญญาส่งอ้อย · QT-2569-002" + หัวข้อ mono **CT-2569-002** + route เปลี่ยนเป็น `#/contracts/CT-2569-002` | ☐ |
| 3 | PRESS Esc | — | drawer ปิด + route กลับ `#/contracts` | ☐ |

### TC-L07 — Export CSV เคารพ filter (AC-23) (ต้อง simulate)
- group: L · ความสำคัญ: กลาง · trace: AC-23 / API-15 · **หมายเหตุ: prototype ไม่มีปุ่ม Export ในหน้า header (มีเฉพาะ ตรวจสอบที่เลือก + สร้างสัญญา) — export = server-side/UI phase ถัดไป**
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: — (SIT / UI ระบบจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (prototype): หน้า header | — | **ไม่มีปุ่ม Export** — mark BLOCKED บน prototype (export ยังไม่มี UI) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): filter สถานะ=อนุมัติแล้ว → Export CSV | — | ไฟล์ CSV มีเฉพาะแถวที่ตรง filter · คอลัมน์ตรงตาราง · ชื่อไฟล์ locale ไทย | ☐ |

### TC-L08 — กรองสถานะ + ประเภท พร้อมกัน (edge — AC-10)
- group: L · ความสำคัญ: กลาง · trace: AC-10 / combined filter (status ∧ type)
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT สถานะ = **รอการตรวจสอบ** + SELECT ประเภทสัญญา = **สัญญาตกเขียว** | — | เหลือ 2 แถว (CT-005, CT-008 — waiting ∧ ตกเขียว) · footer "1 – 2 จาก 2 รายการ" | ☐ |
| 2 | SELECT ประเภทสัญญา = **สัญญาส่งเสริม** (คงสถานะ รอการตรวจสอบ) | — | ตารางว่าง + empty **ไม่พบรายการที่ค้นหา** (support ทั้งหมดเป็น อนุมัติแล้ว — ไม่มี waiting) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** | — | กลับ 8 รายการ · dropdown สถานะ="ทุกสถานะ" ประเภท="ทุกประเภทสัญญา" | ☐ |

---

## Group C — สร้างสัญญา + build-path cascade + 5 ประเภทสัญญา + validation (OV-01)

### TC-C01 — สร้างสัญญา happy (build-path QT-001 + PLT-001 + CRP-0001 + ตันสูญเปล่า) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-02, AC-03, AC-08 / BR-AGT-01/02/03 / LOCK-03/04/05 / XT-01
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`
- ชุดข้อมูล: A
- ผ่านเมื่อ: quota+plot+crop snapshot + toast สร้างสำเร็จ + แถวใหม่ waiting

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างสัญญา** (แดง ขวาบน) | — | drawer เปิดจากขวา eyebrow **สร้างสัญญา** + หัวข้อ **สร้างสัญญาส่งอ้อย** · form-section **เลือกโควตา แปลง และรอบปลูก (บังคับก่อน)** · โซนล่าง (ประเภทสัญญา) ล็อก + note lock **เลือกโควตา · แปลง (≥1) · รอบปลูก (≥1) ก่อน จึงจะเลือกประเภทสัญญาและกรอกข้อมูลได้** | ☐ |
| 2 | CLICK ช่อง **ค้นหาโควตา (Quota Id)** → พิมพ์ "QT-2569-001" | A | dropdown แสดง **QT-2569-001 · สมหญิง รักดี** + sub "0823456789 · 3-XXXX-XXXX-XX-2" · help "ระบบจะดึงข้อมูลเจ้าของโควตาให้อัตโนมัติ (F-AGM-002)" | ☐ |
| 3 | CLICK ตัวเลือก **QT-2569-001 · สมหญิง รักดี** | A | การ์ด **เจ้าของโควตา (อ่านอย่างเดียว)** (ส้ม/teal): QT-2569-001 · สมหญิง รักดี · 0823456789 + "เลขบัตร 3-XXXX-XXXX-XX-2" + ปุ่ม **เปลี่ยนโควตา** · ปรากฏ **เลือกแปลง (ของโควตา)** (2 แปลง) + **เลือกรอบปลูก (ตรวจแล้ว ของโควตา)** | ☐ |
| 4 | CLICK checkbox **PLT-2569-001** | A | cb ติ๊ก · help "เลือกอย่างน้อย 1 แปลง · เลือกแล้ว **1** แปลง" · ฟิลด์ยัง locked (ยังไม่เลือก crop) | ☐ |
| 5 | CLICK checkbox **CRP-2569-0000001** (sub "PLT-2569-001 · 120.00 ตัน") | A | cb ติ๊ก · กล่องรวม **รวม: 120.00 ตัน · 1 รอบปลูก** · **ฟิลด์ปลดล็อกทันที** (โซนประเภทสัญญา opacity เต็ม) · note lock หาย | ☐ |
| 6 | SELECT **เลือกประเภทสัญญา** = **สัญญาตันสูญเปล่า** | A | dropdown แสดงค่า · ไม่มี type-specific block (ตันสูญเปล่าไม่มีฟิลด์เพิ่ม) · สรุปสัญญา: ประเภทสัญญา=สัญญาตันสูญเปล่า / รวมตัน 120.00 / จำนวนแปลง 1 / จำนวนรอบปลูก 1 | ☐ |
| 7 | CLICK ปุ่ม **แนบเอกสาร** | — | toast info **จำลองแนบเอกสาร (PDF/JPG ≤5MB)** · ไฟล์ `contract_doc_1_*.pdf` ปรากฏใต้ปุ่ม | ☐ |
| 8 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (กดซ้ำไม่ได้) | ☐ |
| 9 | WAIT จน toast ปรากฏ (≤3s) | — | drawer ปิด + toast เขียว **สร้างสัญญาสำเร็จ — CT-2569-009** | ☐ |
| 10 | VERIFY ตาราง | — | แถวบนสุด = CT-2569-009 สมหญิง รักดี · สัญญาตันสูญเปล่า · 120.00 · pill เหลือง **รอการตรวจสอบ** · count = **9 รายการ** · การ์ดรอการตรวจสอบ = 5 | ☐ |
| 11 | CLICK แถว CT-2569-009 → Tab **ประวัติ** | — | timeline (ใหม่→เก่า): **เขียนสิทธิ์รอบปลูก (write-back)** (จุดเขียว · note "ตั้งสถานะสิทธิ์รอบปลูก → ทำสัญญาแล้ว · CRP-2569-0000001" · โดย ระบบ (write-back)) → **สร้างสัญญา** (โดย สมพร วงศ์ทะเบียน · note "ผูกโควตา QT-2569-001 · 1 แปลง · 1 รอบปลูก") | ☐ |

### TC-C02 — Field gating: ล็อกจนครบ quota + ≥1 plot + ≥1 crop ★★ signature
- group: C · ความสำคัญ: สูงสุด · trace: AC-02, AC-02b / BR-AGT-01 / LOCK-03 / VR-01
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา**
- ผ่านเมื่อ: ฟิลด์ล็อกจนกว่าจะครบทั้ง quota + ≥1 plot + ≥1 crop

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY โซนล่าง (ประเภทสัญญา/สรุป/เอกสาร) ก่อนเลือกอะไร | — | โซน `#contract-fields` จางลง (opacity ~0.55, pointer-events none) · note lock **เลือกโควตา · แปลง (≥1) · รอบปลูก (≥1) ก่อน จึงจะเลือกประเภทสัญญาและกรอกข้อมูลได้** · input/select disabled | ☐ |
| 2 | เลือกโควตา **QT-2569-003 · ทองดี พูลผล** (เลือก quota อย่างเดียว) | — | การ์ดเจ้าของโควตา + เลือกแปลง (2 แปลง) + เลือกรอบปลูก (3 รอบ) ปรากฏ · **ฟิลด์ยัง locked** (ยังไม่เลือกแปลง/รอบ) | ☐ |
| 3 | CLICK checkbox **PLT-2569-005** (แปลงอย่างเดียว) | — | help "เลือกแล้ว 1 แปลง" · **ฟิลด์ยัง locked** (ยังไม่เลือกรอบปลูก — build path บังคับครบทั้งสาม) | ☐ |
| 4 | CLICK checkbox **CRP-2569-0000007** | — | กล่องรวม "รวม: 60.00 ตัน · 1 รอบปลูก" · **ฟิลด์ปลดล็อกทันที** · note lock หาย | ☐ |
| 5 | เอาออก: CLICK checkbox **CRP-2569-0000007** ซ้ำ (uncheck) | — | crop_ids=0 · **ฟิลด์ล็อกอีกครั้ง** (ต้อง ≥1 crop) | ☐ |
| 6 | CLICK ปุ่ม **เปลี่ยนโควตา** | — | กลับโหมดค้นหาโควตา · แปลง+รอบปลูกถูกล้าง (reset) · ฟิลด์ล็อก | ☐ |

### TC-C03 — Build-path cascade: quota→plots→crops + auto-sum tons (AC-01/02 · XT-04)
- group: C · ความสำคัญ: สูง · trace: AC-01, AC-02 / BR-AGT-01/02 / LOCK-05 / XT-04 / available-items read
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา**
- ผ่านเมื่อ: checklist กรองตามโควตา + total_tons รวม auto จากหลาย crop

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกโควตา **QT-2569-003 · ทองดี พูลผล** → VERIFY เลือกแปลง | — | แสดง 2 แปลง: **PLT-2569-005, PLT-2569-006** (แปลงของ QT-003) · ไม่มีแปลงโควตาอื่น | ☐ |
| 2 | VERIFY เลือกรอบปลูก (ตรวจแล้ว ของโควตา) | — | แสดง 3 รอบ: **CRP-2569-0000007 (60.00), CRP-2569-0000008 (75.00), CRP-2569-0000013 (95.00)** — ทั้งหมด license none (เลือกได้) · ไม่มี " · ทำสัญญาแล้ว" | ☐ |
| 3 | CLICK checkbox **CRP-2569-0000007** + **CRP-2569-0000008** | — | กล่องรวม **รวม: 135.00 ตัน · 2 รอบปลูก** (60+75 auto) | ☐ |
| 4 | CLICK checkbox **CRP-2569-0000013** เพิ่ม | — | กล่องรวม **รวม: 230.00 ตัน · 3 รอบปลูก** (135+95) · สรุปสัญญา จำนวนรอบปลูก 3 | ☐ |
| 5 | CLICK checkbox **PLT-2569-005** + **PLT-2569-006** | — | help "เลือกแล้ว 2 แปลง" · สรุปสัญญา จำนวนแปลง 2 | ☐ |

### TC-C04 — ประเภท support → support_items repeater (AC-03/04 / LOCK-04)
- group: C · ความสำคัญ: สูง · trace: AC-03, AC-04 / BR-AGT-06 / LOCK-04
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-003 + PLT-2569-005 + CRP-2569-0000008
- ผ่านเมื่อ: เลือก support → repeater เพิ่ม/ลบรายการ + สร้างสำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **เลือกประเภทสัญญา** = **สัญญาส่งเสริม** | — | ปรากฏ form-section **รายการส่งเสริม** + help "ยังไม่มีรายการ · กดปุ่มด้านล่างเพื่อเพิ่ม" + ปุ่ม **เพิ่มรายการส่งเสริม** | ☐ |
| 2 | CLICK **เพิ่มรายการส่งเสริม** → TYPE "ปุ๋ยเคมี สูตร 15-15-15" (placeholder "เช่น ปุ๋ยเคมี สูตร 15-15-15") | — | input แถวแรกปรากฏ + มีปุ่ม X ท้ายแถว | ☐ |
| 3 | CLICK **เพิ่มรายการส่งเสริม** อีกครั้ง → TYPE "ยากำจัดวัชพืช" | — | มี 2 แถว input | ☐ |
| 4 | CLICK ปุ่ม X ท้ายแถวที่ 2 | — | เหลือ 1 แถว ("ปุ๋ยเคมี สูตร 15-15-15") | ☐ |
| 5 | CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างสัญญาสำเร็จ — CT-2569-009** · แถวใหม่ ประเภท **สัญญาส่งเสริม** | ☐ |
| 6 | CLICK แถวใหม่ → Tab **ข้อมูลทั่วไป** | — | section **รายการส่งเสริม** แสดง 1 รายการ "ปุ๋ยเคมี สูตร 15-15-15" (มีไอคอนติ๊กเขียว) | ☐ |

### TC-C05 — ประเภท promotion-7 → เลือกช่วงโปรโมชั่น บังคับ (AC-05 / VR-05 / EC-04)
- group: C · ความสำคัญ: สูง · trace: AC-05 / VR-05 / EC-04 / "เลือกช่วงโปรโมชั่น"
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-003 + PLT-2569-005 + CRP-2569-0000007
- ชุดข้อมูล: B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **เลือกประเภทสัญญา** = **สัญญาโปรโมชั่น โปร 7 วัน** | — | ปรากฏ section **ช่วงโปรโมชั่น (โปร 7 วัน)** + label "เลือกช่วงโปรโมชั่น *" + select default "— เลือกช่วงโปรโมชั่น —" (ตัวเลือก: 1-7 ม.ค. 2569 / 8-14 ม.ค. 2569 / 15-21 ม.ค. 2569) | ☐ |
| 2 | คง select ที่ "— เลือกช่วงโปรโมชั่น —" → CLICK **ยืนยันสร้าง** | B2 | **block** + toast เหลือง **เลือกช่วงโปรโมชั่น** — ไม่สร้าง | ☐ |
| 3 | SELECT ช่วง = **1-7 ม.ค. 2569** → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างสัญญาสำเร็จ — CT-2569-009** · แถวใหม่ ประเภท **สัญญาโปรโมชั่น โปร 7 วัน** | ☐ |
| 4 | CLICK แถวใหม่ → Tab **ข้อมูลทั่วไป** | — | section **ช่วงโปรโมชั่น (โปร 7 วัน)** → "ช่วงที่เลือก 1-7 ม.ค. 2569" | ☐ |

### TC-C06 — ประเภท promotion-crane → เลือกเครน บังคับ (AC-06 / VR-05 / EC-04)
- group: C · ความสำคัญ: สูง · trace: AC-06 / VR-05 / EC-04 / "เลือกเครน"
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-003 + PLT-2569-006 + CRP-2569-0000013
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **เลือกประเภทสัญญา** = **สัญญาโปรโมชั่นเครน** | — | ปรากฏ section **เลือกเครน** + label "เครน *" + select default "— เลือกเครน —" (ตัวเลือก: เครน A (10 ตัน) / เครน B (20 ตัน) / เครน C (30 ตัน)) | ☐ |
| 2 | คง select ที่ "— เลือกเครน —" → CLICK **ยืนยันสร้าง** | B3 | **block** + toast เหลือง **เลือกเครน** | ☐ |
| 3 | SELECT เครน = **เครน C (30 ตัน)** → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างสัญญาสำเร็จ — CT-2569-009** · ประเภท **สัญญาโปรโมชั่นเครน** | ☐ |
| 4 | CLICK แถวใหม่ → Tab **ข้อมูลทั่วไป** | — | section **เครน** → "เครนที่เลือก เครน C (30 ตัน)" | ☐ |

### TC-C07 — ประเภท early-purchase (ตกเขียว — ไม่มี type-specific) create happy (AC-03)
- group: C · ความสำคัญ: กลาง · trace: AC-03 / BR-AGT-06 / type ไม่มีฟิลด์เพิ่ม
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-001 + PLT-2569-002 + CRP-2569-0000002 (90.00)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **เลือกประเภทสัญญา** = **สัญญาตกเขียว** | — | **ไม่มี** type-specific block (ตกเขียวเหมือนตันสูญเปล่า — ไม่มีฟิลด์เพิ่ม) · สรุปสัญญา รวมตัน 90.00 | ☐ |
| 2 | CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างสัญญาสำเร็จ — CT-2569-009** · ประเภท **สัญญาตกเขียว** · pill **รอการตรวจสอบ** | ☐ |

### TC-C08 — Submit ก่อนครบ quota+plots+crops → block (negative — AC-02b / VR-01)
- group: C · ความสำคัญ: สูง · trace: AC-02b / VR-01 / EC-01 / ERR_MISSING_FIELDS
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา**
- ชุดข้อมูล: B5
- หมายเหตุ: ปุ่ม **ยืนยันสร้าง** อยู่นอกโซนที่ล็อก (footer) — กดได้เสมอ · validate เด้งใน submitForm

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไม่เลือกอะไร → CLICK ปุ่ม **ยืนยันสร้าง** ทันที | B5 | ไม่บันทึก + toast เตือน **กรุณาตรวจสอบข้อมูลให้ครบถ้วน** (quota/plots/crops ยังไม่ครบ) | ☐ |
| 2 | เลือก quota QT-2569-001 + plot PLT-2569-001 (ยังไม่เลือกรอบปลูก) → CLICK **ยืนยันสร้าง** | — | block เดิม **กรุณาตรวจสอบข้อมูลให้ครบถ้วน** (crop ยัง 0) | ☐ |
| 3 | ปิด drawer → VERIFY count ตาราง | — | ยัง 8 รายการ | ☐ |

### TC-C09 — ไม่เลือกประเภทสัญญา → block (negative — AC-03)
- group: C · ความสำคัญ: สูง · trace: AC-03 / "เลือกประเภทสัญญา"
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-001 + PLT-2569-001 + CRP-2569-0000001 (ปลดล็อก)
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | คง dropdown **เลือกประเภทสัญญา** ที่ "— เลือกประเภทสัญญา —" → CLICK **ยืนยันสร้าง** | B1 | **block** + toast เหลือง **เลือกประเภทสัญญา** — ไม่สร้าง | ☐ |
| 2 | SELECT ประเภทสัญญา = **สัญญาตันสูญเปล่า** → CLICK **ยืนยันสร้าง** → WAIT | — | ผ่าน → toast **สร้างสัญญาสำเร็จ — CT-2569-009** | ☐ |

### TC-C10 — ประเภท support แต่ 0 รายการส่งเสริม → block (negative — VR-05 / EC-04)
- group: C · ความสำคัญ: กลาง · trace: VR-05 / EC-04 / "เลือกรายการส่งเสริม"
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-003 + PLT-2569-005 + CRP-2569-0000007
- ชุดข้อมูล: B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภทสัญญา = **สัญญาส่งเสริม** → **ไม่กด** เพิ่มรายการ → CLICK **ยืนยันสร้าง** | B4 | **block** + toast เหลือง **เลือกรายการส่งเสริม** (support_items = 0) | ☐ |
| 2 | CLICK **เพิ่มรายการส่งเสริม** → TYPE "ค่าเตรียมดิน" → CLICK **ยืนยันสร้าง** → WAIT | — | ผ่าน → toast **สร้างสัญญาสำเร็จ — CT-2569-009** | ☐ |
| 3 | (ตรวจ whitespace) เปิดใหม่ → เพิ่มรายการ พิมพ์ช่องว่างล้วน "   " → ยืนยันสร้าง | — | ยัง block **เลือกรายการส่งเสริม** (trim แล้ว 0 รายการ) | ☐ |

### TC-C11 — แนบเอกสารหลายไฟล์ + ลบ (AC-09)
- group: C · ความสำคัญ: กลาง · trace: AC-09 / attachments simulated (D-05)
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-001 + PLT-2569-001 + CRP-2569-0000001 + ตันสูญเปล่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แนบเอกสาร** 3 ครั้ง | — | toast **จำลองแนบเอกสาร (PDF/JPG ≤5MB)** แต่ละครั้ง · รายการ 3 ไฟล์ (contract_doc_1/2/3_*.pdf) ปรากฏใต้ปุ่ม | ☐ |
| 2 | CLICK ปุ่ม X ลบไฟล์แรก | — | เหลือ 2 ไฟล์ในรายการ | ☐ |
| 3 | CLICK **ยืนยันสร้าง** → WAIT → CLICK แถวใหม่ → Tab **เอกสาร** | — | Tab เอกสาร แสดง **เอกสารแนบ (2)** + ลิงก์ **ดาวน์โหลด** ต่อไฟล์ | ☐ |

### TC-C12 — Double-click กันสร้างซ้ำ (edge — EC-13 / BR-AGT-10)
- group: C · ความสำคัญ: สูง · trace: EC-13 / BR-AGT-10 (double-submit guard f.submitting) / LOCK-10
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-001 + PLT-2569-001 + CRP-2569-0000001 + ตันสูญเปล่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งเร็วที่สุด (double-click) | — | คลิกแรกปุ่มกลายเป็น **กำลังบันทึก…** + disabled — คลิกที่สองไม่มีผล (f.submitting guard) | ☐ |
| 2 | WAIT จน toast → VERIFY ตาราง | — | มีสัญญาใหม่ **1 รายการเท่านั้น** (count = 9, ไม่ใช่ 10) | ☐ |

---

## Group V — อนุมัติ / ปฏิเสธ เดี่ยว (OV-03)

### TC-V01 — อนุมัติ (approve) เดี่ยว — ไม่ต้องมีเหตุผล (happy — AC-13/14 / LOCK-06)
- group: V · ความสำคัญ: สูง · trace: AC-13, AC-14 / US-04 / BR-AGT-04 / EC-05 / XT (keep contracted)
- Setup: role=ผู้อนุมัติ (prototype: user เดียวกดได้) · seed=default (CT-2569-004 waiting)
- Start: OPEN `#/contracts/CT-2569-004`
- ผ่านเมื่อ: pill เปลี่ยนเขียว + toast อนุมัติเรียบร้อย + crop คง contracted

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer + ปุ่ม | — | หัวข้อ mono **CT-2569-004** + pill เหลือง **รอการตรวจสอบ** + ปุ่ม **แก้ไข / อนุมัติ / ปฏิเสธ / ลบ** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** | — | modal **ตรวจสอบสัญญา** — subtitle "เลือกผลการตรวจสอบ · หากปฏิเสธต้องระบุเหตุผล" + info "เลขสัญญา: CT-2569-004 · ประนอม ใจเพชร · โควตา QT-2569-004 · สัญญาโปรโมชั่นเครน · รวม 150.00 ตัน · 1 แปลง · 1 รอบปลูก" + radio **อนุมัติ** (preselect) / **ปฏิเสธ** | ☐ |
| 3 | VERIFY radio อนุมัติ ถูกเลือก (preset) | — | ตัวเลือก **อนุมัติ** ไฮไลต์เขียว · ปรากฏช่อง **หมายเหตุ (ไม่บังคับ)** (ไม่ต้องกรอก) · ไม่มีช่องเหตุผลบังคับ | ☐ |
| 4 | CLICK ปุ่ม **ยืนยัน** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast เขียว **อนุมัติเรียบร้อย** + pill ใน drawer/ตารางเปลี่ยนเป็นเขียว **อนุมัติแล้ว** · การ์ดอนุมัติแล้ว = 3 | ☐ |
| 6 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — อนุมัติ** (จุดเขียว) โดย ธนพล อนุมัติ · **ไม่มี** event license (approve → crop คง contracted) | ☐ |

### TC-V02 — ปฏิเสธ (reject) ไม่กรอกเหตุผล → block (negative — AC-15 / VR-04 / EC-06)
- group: V · ความสำคัญ: สูงสุด · trace: AC-15 / BR-AGT-04 / ERR_REJECT_NO_REASON / LOCK-06
- Setup: role=ผู้อนุมัติ · seed=default (CT-2569-005 waiting)
- Start: OPEN `#/contracts/CT-2569-005` → CLICK **ปฏิเสธ**
- ชุดข้อมูล: B6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หลังกด **ปฏิเสธ** (modal เปิดด้วย preset reject) | — | radio **ปฏิเสธ** ไฮไลต์แดง · ปรากฏช่อง **เหตุผลในการปฏิเสธ *** placeholder "กรุณาระบุเหตุผลในการปฏิเสธ..." + note warn "เมื่อปฏิเสธ ระบบจะคืนสถานะสิทธิ์รอบปลูกที่ผูกไว้ (→ ไม่มีสัญญา)" | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** โดย **ไม่กรอกเหตุผล** | B6 | **block** + ข้อความแดงใต้ช่องเหตุผล **กรุณากรอกเหตุผลในการปฏิเสธ** + toast เหลืองข้อความเดียวกัน — ไม่เปลี่ยนสถานะ | ☐ |

### TC-V03 — ปฏิเสธ (reject) พร้อมเหตุผล → revert license (happy — AC-16 / XT-02)
- group: V · ความสำคัญ: สูง · trace: AC-16 / LOCK-02/07 / EC-07 / XT-02
- Setup: role=ผู้อนุมัติ · seed=default (CT-2569-005 waiting · crop CRP-2569-0000011 = contracted)
- Start: OPEN `#/contracts/CT-2569-005` → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "เอกสารตกเขียวไม่ครบ ขอยื่นใหม่" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ปฏิเสธเรียบร้อย — คืนสถานะสิทธิ์รอบปลูกแล้ว** (info) + pill แดง **ปฏิเสธ** | ☐ |
| 2 | VERIFY Tab **ข้อมูลทั่วไป** (ท้าย) | — | กล่องแดง **เหตุผลที่ปฏิเสธ: เอกสารตกเขียวไม่ครบ ขอยื่นใหม่** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | timeline บนสุด: **คืนสิทธิ์รอบปลูก (write-back)** (จุดเหลือง · note "คืนสถานะสิทธิ์รอบปลูก → ไม่มีสัญญา · CRP-2569-0000011") → **ตรวจสอบ — ปฏิเสธ** (จุดแดง · โดย ธนพล อนุมัติ · note เหตุผล) | ☐ |
| 4 | CLICK Tab **รอบปลูก** | — | CRP-2569-0000011 · "สิทธิ์: **คืนแล้ว**" (pill เทา — license กลับ none จาก write-back) | ☐ |

### TC-V04 — ไม่เลือกผลตรวจสอบ (negative)
- group: V · ความสำคัญ: กลาง · trace: BR-AGT-04 / "กรุณาเลือกผลการตรวจสอบ"
- Setup: role=ผู้อนุมัติ · seed=default (CT-2569-001 waiting)
- Start: OPEN `#/contracts` → CLICK แถว CT-2569-001 → **แต่เปิด modal ผ่านปุ่มหัว: กด อนุมัติ แล้วสลับ radio ให้ไม่ถูกเลือก**
- ชุดข้อมูล: B7
- หมายเหตุ: เปิด modal แบบ bulk (ไม่ preset) เพื่อให้ radio ว่าง — เลือก CT-001 บน list แล้วกด **ตรวจสอบที่เลือก (1)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | บน list: CLICK checkbox แถว CT-2569-001 → CLICK ปุ่มหัว **ตรวจสอบที่เลือก (1)** | — | modal **ตรวจสอบสัญญา** เปิด · radio **ยังไม่มีตัวใดถูกเลือก** (result ว่าง) | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** ทันที (ยังไม่เลือก radio) | B7 | ไม่ดำเนินการ + error ใต้ radio **กรุณาเลือกผลการตรวจสอบ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V05 — ปุ่มอนุมัติ/ปฏิเสธ ซ่อน + checkbox disabled สำหรับ verified/reject (AC-18b / §8)
- group: V · ความสำคัญ: กลาง · trace: AC-18b / BR-AGT-04 / §8 detail actions
- Setup: role=ผู้อนุมัติ · seed=default
- Start: OPEN `#/contracts/CT-2569-002` (verified)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบนหัว Detail drawer (CT-002 อนุมัติแล้ว) | — | มี **แก้ไข + ลบ** — **ไม่มีปุ่ม อนุมัติ/ปฏิเสธ** (ไม่ใช่ waiting) | ☐ |
| 2 | OPEN `#/contracts/CT-2569-003` (reject) → VERIFY ปุ่ม | — | เช่นเดียวกัน: มี แก้ไข + ลบ · ไม่มี อนุมัติ/ปฏิเสธ | ☐ |
| 3 | กลับ list → VERIFY checkbox แถว CT-002/003/006/007 | — | checkbox จาง กดไม่ได้ (title "เลือกได้เฉพาะรายการรอการตรวจสอบ") · ส่วน 409 server (concurrent) = TC-S02 (simulate) | ☐ |

---

## Group B — Bulk อนุมัติ / ปฏิเสธ (OV-03)

### TC-B01 — Bulk เลือกทั้งหมด = เฉพาะ waiting + อนุมัติ (happy — AC-17 / EC-08)
- group: B · ความสำคัญ: สูง · trace: AC-17 / US-06 / BR-AGT-04/09 / LOCK-06
- Setup: role=ผู้อนุมัติ · seed=default (waiting 4)
- Start: OPEN `#/contracts`
- ผ่านเมื่อ: เลือกทั้งหมดติ๊กเฉพาะ waiting + summary

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checkbox รายแถว | — | แถว อนุมัติแล้ว/ปฏิเสธ (CT-002/003/006/007) checkbox จาง กดไม่ได้ · แถว รอการตรวจสอบ (CT-001/004/005/008) กดได้ | ☐ |
| 2 | CLICK checkbox หัวตาราง (title "เลือกทั้งหมด (เฉพาะรอการตรวจสอบ)") | — | ติ๊กเฉพาะ 4 แถว waiting · โผล่ bulk-bar **เลือก 4 รายการ (รอการตรวจสอบ)** + ปุ่มหัวเปลี่ยนเป็น **ตรวจสอบที่เลือก (4)** (enabled) | ☐ |
| 3 | CLICK ปุ่มหัว **ตรวจสอบที่เลือก (4)** | — | modal **ตรวจสอบสัญญา (4 รายการ)** + list "รายการที่เลือก (4 รายการ)" แสดง เลขสัญญา + ชื่อ + โควตา · ประเภท ครบ 4 + help "ใช้เหตุผลเดียวกันทุกรายการ (เมื่อเลือก "ปฏิเสธ") · ข้ามรายการที่ไม่ใช่สถานะรอการตรวจสอบ" | ☐ |
| 4 | CLICK radio **อนุมัติ** → CLICK ปุ่ม **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** | ☐ |
| 5 | VERIFY ตาราง + stats | — | ไม่มีแถว pill เหลืองเหลือ · การ์ด **รอการตรวจสอบ 0** · **อนุมัติแล้ว 6** · ปุ่มหัวกลับเป็น (0) disabled | ☐ |

### TC-B02 — Bulk Reject = เหตุผลเดียวทุกรายการ (AC-18 / VR-04 / LOCK-06)
- group: B · ความสำคัญ: สูง · trace: AC-18 / BR-AGT-04 / VR-04
- Setup: role=ผู้อนุมัติ · seed=default (waiting 4)
- Start: OPEN `#/contracts` → เลือกทั้งหมด (4 waiting) → CLICK **ตรวจสอบที่เลือก (4)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK radio **ปฏิเสธ** โดยไม่กรอกเหตุผล → CLICK **ยืนยัน** | — | block + **กรุณากรอกเหตุผลในการปฏิเสธ** + note warn "...ใช้เหตุผลเดียวกันนี้กับทุกรายการที่เลือก" | ☐ |
| 2 | TYPE "เอกสารประกอบไม่ครบ" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** · ทุกแถวที่เลือก pill แดง **ปฏิเสธ** · การ์ด ปฏิเสธ = 6 | ☐ |
| 3 | OPEN สัญญาหนึ่งใน 4 → Tab ข้อมูลทั่วไป | — | กล่อง **เหตุผลที่ปฏิเสธ: เอกสารประกอบไม่ครบ** (เหตุผลเดียวกันทุกใบ) · Tab รอบปลูก → crop license "คืนแล้ว" | ☐ |

### TC-B03 — Bulk skip non-waiting / partial (edge — AC-18 / EC-08) (ต้อง simulate)
- group: B · ความสำคัญ: สูง · trace: AC-18 / EC-08 · **prototype: openVerifyModal กรอง ids ให้เหลือเฉพาะ waiting ก่อนเปิด modal — จึง สำเร็จ=ทั้งหมด; per-record conflict (คนที่สอง approve ก่อน submit) = SIT**
- Setup: role=ผู้อนุมัติ · seed=default
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) เลือก waiting ทั้งหมด → อนุมัติ → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** (ทุกใบ waiting จริง — non-waiting ถูกกรองออกก่อนเปิด modal) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): บางใบถูก approve โดยผู้อื่นก่อน submit | — | summary "สำเร็จ X ล้มเหลว Y" — ใบที่ status เปลี่ยนแล้วถูกนับ ล้มเหลว (per-record 409 ERR_STATUS_CONFLICT) | ☐ |

---

## Group E — แก้ไข (OV-02 — quota/plots/crops read-only)

### TC-E01 — แก้ไข type-specific/เอกสาร → version++ + audit (status คงเดิม) (happy — AC-11)
- group: E · ความสำคัญ: สูง · trace: AC-11 / US-07 / BR-AGT-10 · **หมายเหตุ: แก้ไขไม่ reset สถานะ (ต่างจาก Crop F-AGM-004)**
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-001 waiting, เวอร์ชัน 1)
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว CT-2569-001 | — | drawer eyebrow **แก้ไขสัญญา** + หัวข้อ **แก้ไข CT-2569-001** · sub "สถานะ: รอการตรวจสอบ · เวอร์ชัน 1" · note info **โควตา QT-2569-001 · 1 แปลง · 1 รอบปลูก — แก้ไม่ได้** · ประเภทสัญญา = สัญญาตันสูญเปล่า (แก้ได้) | ☐ |
| 2 | SELECT เปลี่ยนประเภทสัญญา = **สัญญาโปรโมชั่นเครน** → SELECT เครน = **เครน B (20 ตัน)** | — | ปรากฏ section เลือกเครน + เลือกได้ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + แถว CT-001 ยัง pill เหลือง **รอการตรวจสอบ** (status คงเดิม) + ประเภท = **สัญญาโปรโมชั่นเครน** | ☐ |
| 4 | OPEN `#/contracts/CT-2569-001` → Tab **ประวัติ** | — | มี event **แก้ไขข้อมูลสัญญา** เพิ่มบนสุด (note "แก้ไขประเภทสัญญา/เอกสารแนบ") · footer "เวอร์ชัน 2" | ☐ |

### TC-E02 — quota/plots/crops read-only บนหน้า edit (AC-12 / LOCK-03)
- group: E · ความสำคัญ: สูง · trace: AC-12 / BR-AGT-01 / immutable binding
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-002 verified, 2 crops)
- Start: OPEN `#/contracts` → CLICK ดินสอแถว CT-2569-002

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Section 0 ของ drawer แก้ไข | — | **ไม่มี** ช่องค้นหาโควตา/checklist แปลง/รอบปลูก (ไม่มี build-path UI) · แสดงเฉพาะ note info **โควตา QT-2569-002 · 1 แปลง · 2 รอบปลูก — แก้ไม่ได้** (read-only banner) | ☐ |
| 2 | VERIFY ฟิลด์ที่แก้ได้ | — | แก้ได้เฉพาะ ประเภทสัญญา/type-specific/เอกสารแนบ — quota_id/plot_ids/crop_ids ไม่มี input ให้แก้ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): ยิง PUT เปลี่ยน quota_id/plot_ids/crop_ids | — | server reject (immutable — BR-AGT-01) แม้ UI ไม่มีช่อง | ☐ |

### TC-E03 — แก้ไข support: เพิ่ม/ลบรายการส่งเสริม + save (AC-11 / AC-04)
- group: E · ความสำคัญ: กลาง · trace: AC-11, AC-04 / BR-AGT-06
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-007 support, support_items[ค่าเตรียมดิน])
- Start: OPEN `#/contracts` → CLICK ดินสอแถว CT-2569-007

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section **รายการส่งเสริม** | — | มี 1 แถว input ค่าเดิม "ค่าเตรียมดิน" | ☐ |
| 2 | CLICK **เพิ่มรายการส่งเสริม** → TYPE "ค่าขนส่ง" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** · status ยัง **อนุมัติแล้ว** (edit ไม่ reset) | ☐ |
| 3 | OPEN `#/contracts/CT-2569-007` → Tab ข้อมูลทั่วไป | — | section รายการส่งเสริม แสดง 2 รายการ (ค่าเตรียมดิน, ค่าขนส่ง) · เวอร์ชัน 3 | ☐ |

### TC-E04 — แก้ไข verified ไม่ reset สถานะ (contrast — AC-11)
- group: E · ความสำคัญ: กลาง · trace: AC-11 / §5.2 (Contract edit ≠ reset · ต่างจาก Crop)
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-002 verified)
- Start: OPEN `#/contracts/CT-2569-002`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** → เปลี่ยนประเภท support → เพิ่มรายการ "ยาปราบศัตรูพืช" → **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** (ไม่มี "กลับสู่สถานะรอตรวจสอบ") | ☐ |
| 2 | VERIFY แถว CT-2569-002 | — | pill **ยังเขียว อนุมัติแล้ว** (status คงเดิม — Contract edit ไม่ reset) · การ์ดอนุมัติแล้ว ยัง 2 | ☐ |

---

## Group D — ลบ (soft delete + attachments + revert license — OV-04 — LOCK-09)

### TC-D01 — ลบสัญญา waiting + confirm → soft delete + revert license (happy — AC-21/22 / XT-03)
- group: D · ความสำคัญ: สูง · trace: AC-21, AC-22 / BR-AGT-08 / EC-12 / XT-03 / LOCK-09
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-004 waiting · crop CRP-2569-0000009 = contracted)
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า การ์ด **สัญญาทั้งหมด** และ **รอการตรวจสอบ** | — | บันทึก: ทั้งหมด=8, รอการตรวจสอบ=4 (อ้างใน step 5) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว CT-2569-004 | — | modal **ยืนยันการลบสัญญา** + subtitle `สัญญา "CT-2569-004 — ประนอม ใจเพชร"` + warn แดง **ข้อมูลสัญญาและไฟล์เอกสารที่แนบจะถูกลบ และระบบจะคืนสถานะสิทธิ์รอบปลูกที่ผูกไว้ (→ ไม่มีสัญญา)** + ปุ่ม **ลบสัญญา** | ☐ |
| 3 | CLICK ปุ่ม **ลบสัญญา** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast **ลบสัญญาแล้ว** + แถว CT-004 **หายจากตาราง** (soft delete ซ่อน) · count = 7 รายการ | ☐ |
| 5 | VERIFY stats | — | สัญญาทั้งหมด=7 (is_deleted ไม่นับ) · รอการตรวจสอบ=3 | ☐ |
| 6 | VERIFY (crop write-back): OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก QT-2569-004 → VERIFY checklist รอบปลูก | — | **CRP-2569-0000009 กลับมาเลือกได้** (license revert → none, ไม่ grey) — พิสูจน์ delete → revert none | ☐ |

### TC-D02 — ลบแล้ว deep-link → ไม่พบข้อมูลสัญญาที่เลือก (AC-20b / EC-14)
- group: D · ความสำคัญ: สูง · trace: AC-20b / EC-14 / ERR_NOT_FOUND
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-008 waiting)
- Start: OPEN `#/contracts` → CLICK ถังขยะ แถว CT-2569-008 → **ลบสัญญา** → WAIT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หลังลบ | — | toast **ลบสัญญาแล้ว** · แถว CT-008 หาย · count = 7 | ☐ |
| 2 | OPEN `#/contracts/CT-2569-008` (route ตรง) | — | ไม่เปิด detail — toast แดง **ไม่พบข้อมูลสัญญาที่เลือก** + เด้งกลับ `#/contracts` (deleted ถูกซ่อน) | ☐ |

### TC-D03 — ลบจาก Detail drawer + attachments เคลียร์ (AC-21 / LOCK-09)
- group: D · ความสำคัญ: กลาง · trace: AC-21 / BR-AGT-08 · **ปุ่ม ลบ อยู่ทั้งในตาราง (ทุกแถว) และหัว Detail drawer**
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-005 waiting · attachments[green_purchase_agreement.pdf])
- Start: OPEN `#/contracts/CT-2569-005`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **เอกสาร** | — | **เอกสารแนบ (1)** = green_purchase_agreement.pdf | ☐ |
| 2 | CLICK ปุ่มหัว **ลบ** → modal **ยืนยันการลบสัญญา** → CLICK **ลบสัญญา** → WAIT | — | toast **ลบสัญญาแล้ว** + drawer ปิด + แถว CT-005 หาย · count = 7 | ☐ |
| 3 | CLICK แถว CT-2569-005? (ไม่มีแล้ว) — VERIFY ผ่าน ประวัติ ก่อนลบ (ยิงซ้ำ seed) | — | (ก่อนลบ) Tab ประวัติจะบันทึก event **ลบสัญญา** (note "ลบสัญญา + ลบไฟล์เอกสารแนบ") + **คืนสิทธิ์รอบปลูก (write-back)** — attachments ถูกเคลียร์ (BR-AGT-08) | ☐ |

---

## Group W — Detail / 5 tabs / snapshot / ประวัติ (P-02)

### TC-W01 — Detail ภาพรวม 5 tabs + snapshot card (AC-19)
- group: W · ความสำคัญ: สูง · trace: AC-19 / US-03 / BR-AGT-02 / LOCK-02
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-002 verified support)
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว CT-2569-002 | — | Detail drawer: eyebrow "สัญญาส่งอ้อย · QT-2569-002" + หัวข้อ mono **CT-2569-002** + pill เขียว **อนุมัติแล้ว** | ☐ |
| 2 | VERIFY snapshot card (ใต้หัว) | — | การ์ดส้มอ่อน "โควตา · เกษตรกร · ประเภท" → **โควตา QT-2569-002 · สุรพล เก่งการไร่ · สัญญาส่งเสริม** + ปุ่ม **ดูโควตา** | ☐ |
| 3 | VERIFY แถบ tabs (5) | — | **ข้อมูลทั่วไป · แปลง · รอบปลูก · เอกสาร · ประวัติ** | ☐ |
| 4 | VERIFY Tab **ข้อมูลทั่วไป** | — | section **ข้อมูลสัญญา**: ประเภทสัญญา สัญญาส่งเสริม / รวมตัน **350.00** ตัน / จำนวนแปลง 1 / จำนวนรอบปลูก 2 · section **รายการส่งเสริม** 2 รายการ (ปุ๋ยเคมี สูตร 15-15-15, ยากำจัดวัชพืช) | ☐ |
| 5 | VERIFY footer drawer + ปุ่มหัว | — | "อัปเดตล่าสุด … · เวอร์ชัน N" + ปุ่ม **ปิด** · ปุ่มหัว = **แก้ไข + ลบ** (ไม่มี อนุมัติ/ปฏิเสธ — verified) | ☐ |

### TC-W02 — Tab แปลง + รอบปลูก (crop list + tons + license pill) (AC-20)
- group: W · ความสำคัญ: กลาง · trace: AC-20 / BR-AGT-02 / license label
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-002 verified, 2 crops contracted)
- Start: OPEN `#/contracts/CT-2569-002`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **แปลง** | — | **แปลงที่ผูกกับสัญญา (1)**: PLT-2569-003 + ที่อยู่ "18 หมู่ 2 · สองพี่น้อง สองพี่น้อง สุพรรณบุรี 72110" | ☐ |
| 2 | CLICK Tab **รอบปลูก** | — | **รอบปลูกที่ผูกกับสัญญา (2)**: CRP-2569-0000004 (200.00 ตัน · สิทธิ์ **ทำสัญญาแล้ว** pill เขียว) + CRP-2569-0000005 (150.00 ตัน · ทำสัญญาแล้ว) · **รวมตันทั้งหมด 350.00 ตัน** | ☐ |
| 3 | OPEN `#/contracts/CT-2569-003` (reject) → Tab **รอบปลูก** | — | CRP-2569-0000007 · สิทธิ์ **คืนแล้ว** (pill เทา — reject คืน license none) | ☐ |

### TC-W03 — Tab เอกสาร + ประวัติ (audit + license write events) (AC-20 / BR-AGT-09)
- group: W · ความสำคัญ: สูง · trace: AC-20 / BR-AGT-08/09 / audit + write-back events
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-002 create+approve · CT-2569-003 create+reject)
- Start: OPEN `#/contracts/CT-2569-002`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **เอกสาร** | — | **เอกสารแนบ (2)**: support_plan.pdf + id_card.jpg + ลิงก์ **ดาวน์โหลด** ต่อไฟล์ | ☐ |
| 2 | CLICK ลิงก์ ดาวน์โหลด ไฟล์แรก | — | toast info **จำลองดาวน์โหลด support_plan.pdf** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | timeline (ใหม่→เก่า): **ตรวจสอบ — อนุมัติ** (จุดเขียว · note "เอกสารครบถ้วน" · โดย ธนพล อนุมัติ) → **เขียนสิทธิ์รอบปลูก (write-back)** (note "ตั้งสถานะสิทธิ์รอบปลูก → ทำสัญญาแล้ว · CRP-2569-0000004, CRP-2569-0000005") → **สร้างสัญญา** (โดย สมพร วงศ์ทะเบียน) | ☐ |
| 4 | OPEN `#/contracts/CT-2569-003` → Tab **ประวัติ** | — | timeline: **คืนสิทธิ์รอบปลูก (write-back)** (จุดเหลือง · note "คืนสถานะสิทธิ์รอบปลูก → ไม่มีสัญญา · CRP-2569-0000007") → **ตรวจสอบ — ปฏิเสธ** (จุดแดง · note "เอกสารสิทธิ์แปลงไม่ครบถ้วน กรุณาแนบเพิ่มเติมแล้วยื่นใหม่") → เขียนสิทธิ์ → สร้างสัญญา | ☐ |

### TC-W04 — Deep-link refresh-safe + missing (AC-20b / EC-14)
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / refresh-safe / ERR_NOT_FOUND
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts/CT-2569-006` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/contracts/CT-2569-006` | — | หน้า list โหลด + Detail drawer **CT-2569-006** เปิดเองทันที (pill แดง ปฏิเสธ) | ☐ |
| 2 | PRESS F5 (refresh ทั้งหน้า) | — | กลับมาที่เดิม — drawer CT-2569-006 ยังเปิด (refresh-safe · mountViewDrawer จาก route) | ☐ |
| 3 | OPEN `#/contracts/CT-2569-999` (ไม่มีในระบบ) | — | toast แดง **ไม่พบข้อมูลสัญญาที่เลือก** + เด้งกลับ `#/contracts` (ไม่มี drawer) | ☐ |

### TC-W05 — type-specific ในหน้า detail ครบทุกประเภท (AC-19/20)
- group: W · ความสำคัญ: กลาง · trace: AC-19 / BR-AGT-06 / typeSpecificSummary
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/contracts/CT-2569-003` → Tab ข้อมูลทั่วไป | — | section **ช่วงโปรโมชั่น (โปร 7 วัน)** → "ช่วงที่เลือก 1-7 ม.ค. 2569" | ☐ |
| 2 | OPEN `#/contracts/CT-2569-006` → Tab ข้อมูลทั่วไป | — | section **เครน** → "เครนที่เลือก เครน A (10 ตัน)" + กล่องแดง **เหตุผลที่ปฏิเสธ: ปริมาณตันไม่สอดคล้องกับรอบปลูกที่ตรวจสอบ** | ☐ |
| 3 | OPEN `#/contracts/CT-2569-001` → Tab ข้อมูลทั่วไป | — | ประเภท สัญญาตันสูญเปล่า · **ไม่มี** section type-specific (ตันสูญเปล่าไม่มีฟิลด์เพิ่ม) | ☐ |

---

## Group X — Cross-module WRITE-BACK ⭐⭐ (06_TESTS §6.9 — contracted/none + available read + 1 crop:1 contract)

> Contract อ่าน Quota/Plot/Crop (`findQuota`/`plotsForQuota`/`cropsForQuota`) **และเขียนกลับ** `crop.license_status` ผ่าน `setCropsLicense()`: create→`contracted` · reject→`none` · delete→`none` · approve→keep. จำลอง in-memory (D-03) · reconcile ไป Crop feature จริง (ENG-EXT-AGM PATCH + retry) = `(ต้อง simulate)` ที่ SIT

### TC-X01 — สร้างสัญญา → crop license → contracted + history (XT-01) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-08 / BR-AGT-05/09 / LOCK-07
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CRP-2569-0000010 license none — เลือกได้)
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา**
- ผ่านเมื่อ: crop ที่ผูก license → contracted + history "ตั้งสถานะสิทธิ์รอบปลูก → ทำสัญญาแล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-004** → VERIFY checklist รอบปลูก | — | **CRP-2569-0000010 เลือกได้** (license none) · CRP-2569-0000009 + CRP-2569-0000011 grey " · ทำสัญญาแล้ว" | ☐ |
| 2 | ติ๊ก **PLT-2569-008** + **CRP-2569-0000010** → SELECT ตันสูญเปล่า → **ยืนยันสร้าง** → WAIT | — | toast **สร้างสัญญาสำเร็จ — CT-2569-009** | ☐ |
| 3 | CLICK แถวใหม่ CT-2569-009 → Tab **รอบปลูก** | — | CRP-2569-0000010 · สิทธิ์ **ทำสัญญาแล้ว** (pill เขียว — license → contracted จาก write-back) | ☐ |
| 4 | Tab **ประวัติ** | — | event **เขียนสิทธิ์รอบปลูก (write-back)** (note "ตั้งสถานะสิทธิ์รอบปลูก → ทำสัญญาแล้ว · CRP-2569-0000010" · โดย ระบบ (write-back)) | ☐ |
| 5 | (พิสูจน์กันซ้ำ) CLICK **สร้างสัญญา** → เลือก QT-2569-004 → VERIFY checklist | — | **CRP-2569-0000010 ตอนนี้ grey " · ทำสัญญาแล้ว"** (contracted แล้ว — กันเลือกซ้ำทันที) | ☐ |

### TC-X02 — ปฏิเสธสัญญา → crop license → none (revert) (XT-02)
- group: X · ความสำคัญ: สูงสุด · trace: XT-02 / AC-16 / BR-AGT-05 / EC-07 / LOCK-07
- Setup: role=ผู้อนุมัติ · seed=default (CT-2569-001 waiting · crop CRP-2569-0000003 = contracted)
- Start: OPEN `#/contracts/CT-2569-001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (ก่อนปฏิเสธ) CLICK Tab **รอบปลูก** | — | CRP-2569-0000003 · สิทธิ์ **ทำสัญญาแล้ว** (contracted) | ☐ |
| 2 | CLICK **ปฏิเสธ** → TYPE "ข้อมูลไม่ครบ" → **ยืนยัน** → WAIT | — | toast **ปฏิเสธเรียบร้อย — คืนสถานะสิทธิ์รอบปลูกแล้ว** · pill แดง ปฏิเสธ | ☐ |
| 3 | CLICK Tab **รอบปลูก** อีกครั้ง | — | CRP-2569-0000003 · สิทธิ์ **คืนแล้ว** (pill เทา — license → none) | ☐ |
| 4 | (พิสูจน์เลือกได้ใหม่) CLICK **สร้างสัญญา** → เลือก QT-2569-001 → VERIFY checklist | — | **CRP-2569-0000003 กลับมาเลือกได้** (ไม่ grey — license revert none) | ☐ |

### TC-X03 — ลบสัญญา → crop license → none (XT-03 / EC-12)
- group: X · ความสำคัญ: สูง · trace: XT-03 / AC-22 / EC-12 / BR-AGT-05
- Setup: role=เจ้าหน้าที่สัญญา · seed=default (CT-2569-005 waiting · crop CRP-2569-0000011 = contracted)
- Start: OPEN `#/contracts`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ถังขยะ แถว CT-2569-005 → **ลบสัญญา** → WAIT | — | toast **ลบสัญญาแล้ว** · แถวหาย | ☐ |
| 2 | CLICK **สร้างสัญญา** → เลือก **QT-2569-004** → VERIFY checklist รอบปลูก | — | **CRP-2569-0000011 กลับมาเลือกได้** (ไม่ grey — delete → revert none เหมือน reject) | ☐ |

### TC-X04 — อนุมัติ → crop license คง contracted (XT keep / AC-14)
- group: X · ความสำคัญ: สูง · trace: AC-14 / BR-AGT-05 / LOCK-07 (approve keeps)
- Setup: role=ผู้อนุมัติ · seed=default (CT-2569-004 waiting · crop CRP-2569-0000009 = contracted)
- Start: OPEN `#/contracts/CT-2569-004`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → radio อนุมัติ → **ยืนยัน** → WAIT | — | toast **อนุมัติเรียบร้อย** · pill เขียว อนุมัติแล้ว | ☐ |
| 2 | CLICK Tab **รอบปลูก** | — | CRP-2569-0000009 · สิทธิ์ **ทำสัญญาแล้ว** (คง contracted — approve ไม่คืน) | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | มี **ตรวจสอบ — อนุมัติ** · **ไม่มี** event license-revert (approve keep) | ☐ |

### TC-X05 — available-items read: เฉพาะ verified ของโควตา + license≠contracted (XT-04)
- group: X · ความสำคัญ: สูงสุด · trace: XT-04 / AC-01/02 / VR-02/03 / BR-AGT-01
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-002 · สุรพล เก่งการไร่** → VERIFY checklist รอบปลูก | — | 4 รอบ verified: **CRP-2569-0000006 เลือกได้** (none) · **CRP-2569-0000004, 0000005, 0000014 grey " · ทำสัญญาแล้ว"** (contracted — กันเลือกซ้ำ) | ☐ |
| 2 | VERIFY checklist แปลง | — | 2 แปลงของ QT-002: **PLT-2569-003, PLT-2569-004** เท่านั้น (ไม่มีแปลงโควตาอื่น) | ☐ |
| 3 | CLICK ปุ่ม **เปลี่ยนโควตา** → เลือก **QT-2569-003** → VERIFY | — | รอบปลูก 3 รอบ (CRP-0007/0008/0013 ทั้งหมดเลือกได้) · แปลง PLT-005/006 — พิสูจน์ available-items กรองตามโควตา | ☐ |

### TC-X06 — 1 crop : 1 active contract — contracted grey + กันเลือกซ้ำ (XT-05 / AC-07 / VR-03)
- group: X · ความสำคัญ: สูงสุด · trace: XT-05 / AC-07 / VR-03 / EC-03 / BR-AGT-07 / LOCK-08
- Setup: role=เจ้าหน้าที่สัญญา · seed=default
- Start: OPEN `#/contracts` → CLICK **สร้างสัญญา** → เลือก **QT-2569-001**
- ผ่านเมื่อ: crop contracted ถูก grey + disabled + ไม่ให้ติ๊ก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checklist รอบปลูก ของ QT-2569-001 | — | 4 รอบ: **CRP-2569-0000001 (120.00) + CRP-2569-0000002 (90.00) เลือกได้** (text แดง mono) · **CRP-2569-0000003 + CRP-2569-0000012 grey** (opacity ต่ำ) + ต่อท้าย " · ทำสัญญาแล้ว" | ☐ |
| 2 | HOVER checkbox ของ **CRP-2569-0000003** (contracted) | — | cb แบบ disabled + tooltip title **รอบปลูกนี้ทำสัญญาแล้ว** · cursor not-allowed | ☐ |
| 3 | CLICK checkbox **CRP-2569-0000003** (contracted) | — | **ไม่มีการติ๊ก** (cb ไม่มี onclick — disabled) · crop_ids ไม่เปลี่ยน · (guard `toggleFormCrop` มี toast "รอบปลูกนี้ทำสัญญาแล้ว" เป็น defensive path) | ☐ |
| 4 | CLICK checkbox **CRP-2569-0000001** (none) | — | ติ๊กได้ปกติ · กล่องรวม "รวม: 120.00 ตัน · 1 รอบปลูก" — พิสูจน์เฉพาะ license≠contracted เลือกได้ | ☐ |

---

## Group S — System / simulate (optimistic lock · concurrency · SoD · license-write rollback)

### TC-S01 — Optimistic lock stale edit → 409 (edge — EC-09 / BR-AGT-10) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: EC-09 / ERR_STALE / API-05 · **prototype single-session ทำไม่ได้ (Drift D-04) — SIT case · double-submit guard ตรวจแล้วใน TC-C12**
- Setup: **simulate — ระบบจริง:** 2 sessions — A แก้ record + save ก่อน, B ที่เปิดค้างไว้ save ทีหลังด้วย expected_version เก่า
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B กด **บันทึกการแก้ไข** หลัง A save ไปแล้ว | — | 409 + toast แดง **ข้อมูลล้าสมัย กรุณารีเฟรช** — ข้อมูลของ A ไม่ถูกทับ | ☐ |

### TC-S02 — Concurrent approve status changed → 409 (edge — AC-18b / EC-10) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-18b / EC-10 / ERR_STATUS_CONFLICT · **prototype UI ซ่อนปุ่มอนุมัติ/ปฏิเสธ สำหรับ verified/reject (TC-V05) — ส่วน 409 server = SIT**
- Setup: **simulate — ระบบจริง:** A approve record ก่อน, B approve record เดิม (status เปลี่ยนแล้ว)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B POST approve กับ record ที่ A เพิ่ง approve | — | 409 + **สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช** — สถานะที่ A ตั้งไว้คงเดิม | ☐ |

### TC-S03 — SoD + RBAC hide (OQ-CT6) (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: §5.3 SoD/permission matrix · **prototype ไม่มี role switching — เจ้าหน้าที่/ผู้อนุมัติเป็น user เดียว — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง:** feature flag SoD + RBAC
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — RBAC): login เป็น เจ้าหน้าที่สัญญา | — | ปุ่ม **อนุมัติ / ปฏิเสธ / ตรวจสอบที่เลือก** ถูกซ่อน (approve = ผู้อนุมัติเท่านั้น) | ☐ |
| 2 | VERIFY (ระบบจริง — SoD flag ON): ผู้อนุมัติ approve สัญญาที่ตนเองสร้าง | — | block 403 + ข้อความ SoD (ผู้สร้างไม่ควรอนุมัติเอง) · flag OFF → ผ่านแต่ log anomaly | ☐ |

### TC-S04 — license-write rollback + retry + server crop-verified enforce (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: EC-11 / BR-AGT-05/10 / ERR_CROP_NOT_VERIFIED · **prototype write-back เป็น in-memory sync (D-03) — rollback/retry + crop verified guard = server**
- Setup: **simulate — ระบบจริง:** setCropsLicense ผ่าน ENG-EXT-AGM PATCH (transaction)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): create สำเร็จ แต่ crop-license PATCH ล้มเหลว | — | rollback contract insert + เข้า retry queue (EC-11 · LOCK-07) — ไม่มีสัญญาค้างที่ crop ยัง none | ☐ |
| 2 | VERIFY (ระบบจริง): payload ผูก crop ที่ไม่ verified (bypass UI) | — | server reject **เลือกรอบปลูกที่ตรวจสอบแล้ว** (ERR_CROP_NOT_VERIFIED · VR-02) แม้ mock ทุก crop verified | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `contract-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed 8 สัญญา + 4 โควตา + 8 แปลง + 14 รอบปลูก (license write-back reset กลับ contracted 7/none 7) — ทำให้เคส independent
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/PRESS/WAIT/VERIFY/HOVER)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast มุมขวาล่าง · create/edit 0.6s · approve/reject 0.7s · delete 0.55s — อ่านทันทีที่โผล่ · toast แสดง ~4s)
5. **build-path บังคับ:** ทุกเคสสร้าง/negative ที่ต้องเลือกประเภทสัญญา ต้อง **เลือกโควตา + ≥1 แปลง + ≥1 รอบปลูก (license none) ก่อน** (ฟิลด์ล็อกจนครบทั้งสาม) — ยกเว้นเคสที่ทดสอบ gating เอง (TC-C02/C08)
6. **crop id ที่ contracted (grey) เลือกไม่ได้** — ใช้เฉพาะ crop license=none ตามตาราง seed (ดู Data Sets → Seed โควตา)
7. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
8. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"
9. จบทุกเคส → กรอก Result Report ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 26 / 26 (AC-01..23 + AC-02b/18b/20b) |
| Cross-Module (XT-01..05) | 5 / 5 (write-back contracted/none + available read + กันซ้ำ) |
| Business rules (BR-AGT-01..10) | 10 / 10 |
| Validation (VR-01..05) | 5 / 5 (VR-02 server-enforce → TC-S04 simulate) |
| Edge cases (EC-01..14) | 14 / 14 (EC-09/10/11 simulate/SIT) |
| Error codes (UI-observable) | 11 / 11 (ERR_STALE / ERR_STATUS_CONFLICT / ERR_CROP_NOT_VERIFIED = simulate) |
| Permission cells | เจ้าหน้าที่สัญญา / ผู้อนุมัติ allow ครบ · RBAC deny / SoD = TC-S03 (simulate) |
| Scope Lock (LOCK-01..10) | 10 / 10 — ทุก LOCK มีเคส verify |

- **Manifest cross-check (FRD §0.12): ✅ 9 Stories + 10 Rules + 5 VR + 14 EC + 5 XT + 10 LOCK — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT (6 เคส)
- TC-L07 (export CSV — ไม่มี UI ใน prototype)
- TC-B03 (bulk skip non-waiting per-record conflict)
- TC-S01 (optimistic lock 409 — single session)
- TC-S02 (concurrent approve 409)
- TC-S03 (SoD / RBAC — ไม่มี role switching)
- TC-S04 (license-write rollback/retry + server crop-verified enforce)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-005",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 50, "pass": 0, "fail": 0, "blocked": 0 }
}
```

---

## v1.1 Recheck Additions (F-AGM-005 · crosscheck กับ FRD/Stage-10/Testcase/AS-BUILT ใหม่)

เพิ่ม 6 เคส หลัง crosscheck พบว่า prototype เดิมยังไม่ตรงสเปคผู้มีอำนาจในบางจุด — ได้แก้แล้ว:

| เคส | กลุ่ม | สิ่งที่ทดสอบ | anchor |
|---|---|---|---|
| TC-C13 | สร้าง | รายการส่งเสริมแบบมีโครงสร้าง (ประเภท 5 มาสเตอร์ + ราคา + วันที่รับ) แทนข้อความอิสระ | create_type |
| TC-C14 | สร้าง | จำนวนตันที่ทำสัญญา = ช่องกรอกเอง บังคับ >0 ทุกประเภท + ปุ่ม “ใช้ค่านี้” | create_drawer |
| TC-C15 | สร้าง | ช่วงโปร 7 วัน (4 ค่า) + เครน (กุดโดน/ชื่นชม2/หนองกุงสวรรค์/โนนสำราญ) ตรงมาสเตอร์ | create_type |
| TC-C16 | สร้าง | สัญญาตกเขียว (early-purchase) ไม่มีส่วนเอกสารแนบ | create_type |
| TC-W07 | Landing | หน้ารายละเอียดแสดงรายการส่งเสริมพร้อมประเภท/ราคา/วันที่ | view_drawer |
| TC-L11 | รายการ | ปุ่ม Export CSV ตามตัวกรอง (ฝั่งหน้าจอ · backend Pending Spec ตาม TC-522) | list_actions |

หมายเหตุ reconciliation:
- total_tons เดิม prototype คำนวณอัตโนมัติจากผลรวมรอบปลูก → แก้เป็นช่องกรอกเอง (บังคับ >0) ตาม FRD Create §4 + AS-BUILT โดยคงผลรวมรอบปลูกเป็นตัวช่วย (“ใช้ค่านี้”)
- support_items เดิมเป็นข้อความอิสระ → แก้เป็นโครงสร้าง {ประเภทส่งเสริม (5 มาสเตอร์), ราคา, วันที่รับ}
- ค่ามาสเตอร์ ช่วงโปร 7 วัน / เครน แก้ให้ตรงสเปค (เดิมเป็นช่วงวันที่/เครน A-B-C)
- Export backend = Pending Spec (TC-522) — prototype ทำ client-side export
