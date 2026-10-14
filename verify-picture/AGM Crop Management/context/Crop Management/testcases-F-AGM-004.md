# AI Test Cases — F-AGM-004 Crop Management (จัดการรอบปลูก)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `crop-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ HTML + UI Brief §9 แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side / optimistic lock / concurrency / role / ETCD·Survey external จริง) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-004 (AGM/Crop — WKN) |
| App entry | เปิดไฟล์ `crop-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/crops` (list — default) · `#/crops/:crop_id` (Landing drawer, refresh-safe) |
| ที่มา | FRD_F-AGM-004_Pack (7 ไฟล์) · BRD APPROVED (LOCK-01..13) · HTML v1.0 (audit FAIL=0) · UI_BRIEF_F-AGM-004 |
| จำนวนเคส | 65 เคส / 10 groups (v1.1 — +7 เคสจาก recheck: ลักษณะอ้อย/อายุอ้อยคำนวณ/Export/CSV 8 คอลัมน์) |
| Scope Lock | LOCK-01..13 (00_OVERVIEW §0.11 ← BRD §3.4) — ทุกข้อมีเคส verify (ดู Ledger) |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า = ข้อมูล reset กลับ seed 8 รอบปลูก + 5 โควตา + 8 แปลง — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh (F5) ก่อนเริ่ม |
| Cross-module ⭐⭐ | **DOUBLE READ-ONLY** — Crop อ่าน Quota (verified,exact ผ่าน `QUOTAS`+`verifiedQuotas/findQuotaById`) **และ** Plot (owner+verified ผ่าน `PLOTS`+`plotsForQuota/findPlotById`) · อ่าน ETCD/Survey (external, fail-soft) · store `quota_id/plot_id`+snapshot · **ไม่มี write-back ไป Quota/Plot** · Quota/Plot/ETCD/Survey feature จริง ทดสอบตอน SIT |

**Seed ตั้งต้น (หลัง refresh — 8 รอบปลูก CRP-2569-0000001..0008):**
| เลขรอบปลูก | ปี(พ.ศ.) | โควตา | แปลง | เกษตรกร | รวมตัน | ΣETCD | คงเหลือ | สถานะ | อายุ(วัน) |
|---|---|---|---|---|---|---|---|---|---|
| CRP-2569-0000001 | 2569 | QT-2569-001 | PLT-2569-001 | สมหญิง รักดี | 120.00 | 80 | **40.00** | **รอตรวจสอบ** | 14 (ค้าง) |
| CRP-2569-0000002 | 2569 | QT-2569-001 | PLT-2569-002 | สมหญิง รักดี | 90.00 | 110 | **−20.00** 🔴 | **รอตรวจสอบ** | 11 (ค้าง) |
| CRP-2569-0000003 | 2568 | QT-2569-002 | PLT-2569-003 | สุรพล เก่งการไร่ | 200.00 | 150 | **50.00** | **ตรวจแล้ว** | 26 |
| CRP-2569-0000004 | 2569 | QT-2569-003 | PLT-2569-005 | ทองดี พูลผล | 60.00 | 75 | **−15.00** 🔴 | **รอตรวจสอบ** | 8 (ค้าง) |
| CRP-2569-0000005 | 2569 | QT-2569-004 | PLT-2569-006 | ประนอม ใจเพชร | 150.00 | 0 | **150.00** | **รอตรวจสอบ** | 6 |
| CRP-2569-0000006 | 2569 | QT-2569-002 | PLT-2569-003 | สุรพล เก่งการไร่ | 300.00 | 120 | **180.00** | **ตรวจแล้ว** | 18 |
| CRP-2569-0000007 | 2568 | QT-2569-003 | PLT-2569-005 | ทองดี พูลผล | 80.00 | 30 | **50.00** | **ปฏิเสธ** | 24 |
| CRP-2569-0000008 | 2569 | QT-2569-004 | PLT-2569-007 | ประนอม ใจเพชร | 100.00 | 20 | **80.00** | **ยกเลิก** | 16 |

สรุป: รอตรวจสอบ 4 (ค้างเกิน 7 วัน 3 รายการ = CRP-001/002/004) · ตรวจแล้ว 2 · ปฏิเสธ 1 · ยกเลิก 1 · **คงเหลือติดลบ 2 รายการ** (CRP-002 −20 · CRP-004 −15) · รอบปลูกทั้งหมด 8 (ไม่มี deleted ใน seed — deleted ถูกซ่อน)
- CRP-007 reject_reason = "ปริมาณรวมไม่สอดคล้องกับขนาดแปลง กรุณาตรวจสอบและแก้ไข" · CRP-008 cancel_reason = "เกษตรกรขอยกเลิกรอบปลูกนี้"
- CRP-003 verify note = "ข้อมูลครบถ้วน" · CRP-001 photos 2 (crop_001_a.jpg, crop_001_b.jpg) + survey 1 (ทีมสำรวจ A · ต้นอ้อยสมบูรณ์) · CRP-005 photos 3 · CRP-003 survey 1 (ทีมสำรวจ B)
> ⚠ **Double-binding signature:** CRP-001 + CRP-002 ผูกโควตาเดียวกัน **QT-2569-001** (แปลงต่างกัน) · CRP-003 + CRP-006 ผูก QT-2569-002 → พิสูจน์ 1 quota : N crops ได้ทันที

**Seed โควตา (5 รายการ — จาก `QUOTAS` const, READ-ONLY · เลือกได้เฉพาะ verified 4 ตัว):**
| เลขโควตา | สถานะ | เกษตรกร | เบอร์ | เลขบัตร (masked) | เลือกได้? |
|---|---|---|---|---|---|
| QT-2569-001 | verified | สมหญิง รักดี | 0823456789 | 3-XXXX-XXXX-XX-2 | ✅ |
| QT-2569-002 | verified | สุรพล เก่งการไร่ | 0945678901 | 3-XXXX-XXXX-XX-4 | ✅ |
| QT-2569-003 | verified | ทองดี พูลผล | 0889012345 | 3-XXXX-XXXX-XX-8 | ✅ |
| QT-2569-004 | verified | ประนอม ใจเพชร | 0833334444 | 4-XXXX-XXXX-XX-3 | ✅ |
| QT-2569-005 | **waiting_for_verify** | สมพงษ์ ทองแท้ | 0855556666 | 4-XXXX-XXXX-XX-5 | ❌ (ไม่ verified — ไม่ขึ้น dropdown) |
> `verifiedQuotas()` คืนเฉพาะ 4 ตัวแรก · QT-2569-005 **ไม่แสดง** ในค้นหา (พิสูจน์ XT-02 ได้ทันที)

**Seed แปลง (8 รายการ — จาก `PLOTS` const, READ-ONLY · `plotsForQuota` = ของเจ้าของโควตา + verified):**
| เลขแปลง | โควตา(เจ้าของ) | verify_status | ขนาด(ไร่) | ที่อยู่ | เลือกได้บนโควตานั้น? |
|---|---|---|---|---|---|
| PLT-2569-001 | QT-2569-001 | verified | 12.50 | 99 หมู่ 3 · วังขนาย ท่าม่วง กาญจนบุรี | ✅ |
| PLT-2569-002 | QT-2569-001 | verified | 8.75 | 101 หมู่ 3 · ท่าม่วง ท่าม่วง กาญจนบุรี | ✅ |
| PLT-2569-003 | QT-2569-002 | verified | 25.00 | 18 หมู่ 2 · สองพี่น้อง สองพี่น้อง สุพรรณบุรี | ✅ |
| PLT-2569-004 | QT-2569-002 | **waiting** | 30.40 | 20 หมู่ 2 · ต้นตาล สองพี่น้อง สุพรรณบุรี | ❌ (ยังไม่ verified — ถูกตัดออก) |
| PLT-2569-005 | QT-2569-003 | verified | 15.20 | 77 หมู่ 1 · โพธาราม โพธาราม ราชบุรี | ✅ |
| PLT-2569-006 | QT-2569-004 | verified | 6.00 | 5 หมู่ 5 · ท่าผา บ้านโป่ง ราชบุรี | ✅ |
| PLT-2569-007 | QT-2569-004 | verified | 18.90 | 8 หมู่ 5 · บ้านโป่ง บ้านโป่ง ราชบุรี | ✅ |
| PLT-2569-008 | QT-2569-005 | verified | 9.30 | 80 หมู่ 1 · คลองตาคต โพธาราม ราชบุรี | ✅* (แต่ QT-005 ไม่ verified → เข้าไม่ถึงผ่าน create) |
> `plotsForQuota(qid)`: QT-001→[PLT-001, PLT-002] (2) · QT-002→[PLT-003] (1, PLT-004 waiting ถูกตัด) · QT-003→[PLT-005] (1) · QT-004→[PLT-006, PLT-007] (2). **owner mismatch / ไม่ verified → excluded** (XT-03)

**Users:** เจ้าหน้าที่รอบปลูก = **สมพร วงศ์ทะเบียน** (`CURRENT_USER` — create/edit/csv/cancel/delete) · ผู้ตรวจสอบ = **ธนพล ตรวจสอบ** (`CHECKER` — verify/reject/bulk)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination / remaining badge | TC-L01..L08 (8) | สูง |
| C — สร้างรอบปลูก + double-binding + validation | TC-C01..C12 (12) | สูงสุด |
| I — CSV Import (5-col schema) | TC-I01..I06 (6) | สูง |
| V — ตรวจสอบ/ปฏิเสธ (เดี่ยว) | TC-V01..V05 (5) | สูง |
| B — Bulk verify/reject | TC-B01..B03 (3) | สูง |
| E — แก้ไข + State machine (verified→waiting ⭐) | TC-E01..E05 (5) | สูงสุด |
| D — ยกเลิก / ลบ (soft) | TC-D01..D04 (4) | สูง |
| W — Landing / 5 tabs / ETCD / Survey / ประวัติ | TC-W01..W05 (5) | สูง |
| **X — Cross-module DOUBLE read-only ⭐⭐ + ETCD compute + fail-soft** | TC-X01..X06 (6) | **สูงสุด** |
| S — System / simulate (optimistic lock, concurrency, SoD, deep-link) | TC-S01..S04 (4) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1 ← BRD §7)
| item | cases |
|---|---|
| AC-01 ค้นหา quota (exact, verified) → farmer owner snapshot | TC-C01, TC-C02, TC-X01, TC-X02 |
| AC-02 เลือก plot (ของเจ้าของ quota + verified) → plot snapshot + fields ปลดล็อก | TC-C01, TC-C04, TC-X03 |
| AC-02b quota ไม่พบ/ไม่ verified → "ไม่พบ Quota หรือสถานะไม่เป็น verified" block | TC-C03, TC-I05 |
| AC-02c plot owner mismatch/ไม่ verified → block | TC-C04, TC-X03, TC-I05 |
| AC-03 create happy + toast "สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]" + waiting_for_verify + audit | TC-C01, TC-X02 |
| AC-04 year นอก 2500-2600 → "ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600" | TC-C06, TC-E05 |
| AC-05 month ไม่เลือก → "กรุณาเลือกเดือนที่ปลูก" | TC-C07 |
| AC-06 total_tons < 0 → "ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0" | TC-C08 |
| AC-07 submit ก่อนครบ quota+plot → block "กรุณาเลือกโควตาและแปลงก่อน" | TC-C05, TC-C02 |
| AC-08 upload photos หลายไฟล์ → preview ชื่อไฟล์ | TC-C09, TC-W02 |
| AC-09 search (crop_id/quota/plot/farmer) + filter status(5)+ปี · ไม่พบ → "ไม่พบรายการที่ค้นหา" | TC-L02, TC-L03, TC-L04 |
| AC-10 sort crop_id/year/total_tons · export CSV เคารพ filter · pagination | TC-L05, TC-L06, TC-L07 |
| AC-29 remaining ติดลบ → badge แดง (list + landing) | TC-L08, TC-W01, TC-X04 |
| AC-11 แก้ crop waiting + save → version++ · status คงเดิม + audit | TC-E01 |
| AC-11b แก้ crop **verified** + save → **กลับ waiting_for_verify** (LOCK-05) + toast "บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ" ⭐ | TC-E02 |
| AC-12 stale (version เก่า) → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| AC-13 quota/plot บนหน้า edit = read-only (แก้ไม่ได้) | TC-E04 |
| AC-14 CSV ดี N แถว → summary total/created/failed + ทุกแถว waiting_for_verify | TC-I02, TC-I06 |
| AC-15 header ไม่ตรง → reject ทั้งไฟล์ + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]" | TC-I04 |
| AC-16 แถว quota/plot invalid → error รายแถว + report | TC-I05, TC-I02 |
| AC-17 ไม่ใช่ .csv → "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" | TC-I03 |
| AC-18 waiting + ยืนยัน → toast "ยืนยันเรียบร้อย" + pill เขียว + verified_by + audit | TC-V01 |
| AC-19 ปฏิเสธ ไม่กรอกเหตุผล → "กรุณากรอกเหตุผลในการปฏิเสธ" block | TC-V02 |
| AC-20 ปฏิเสธ + reason → pill แดง + reject_reason แสดง landing + audit | TC-V03, TC-W01 |
| AC-21 Bulk: เลือกทั้งหมด = เฉพาะ waiting · ยืนยันกลุ่ม → summary | TC-B01 |
| AC-22 Bulk reject = เหตุผลบังคับ (ใช้ร่วม) · skip non-waiting | TC-B02, TC-B03 |
| AC-23b verified/rejected → verify ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม) | TC-V05, TC-S02 (simulate) |
| AC-24 Landing tabs + snapshot card (ดูโควตา/ดูแปลง) | TC-W01, TC-W02 |
| AC-25 ETCD tab bookings + total_booked + remaining (read-only) · Survey read-only | TC-W03, TC-W04 |
| AC-25b ETCD/Survey external down → fail-soft (landing ยังเปิดได้) | TC-X06 (ต้อง simulate) |
| AC-26 ประวัติ = audit timeline | TC-W04 |
| AC-26b deep-link crop ไม่มี/deleted → "ไม่พบข้อมูลรอบปลูกที่เลือก" + กลับ list | TC-W05, TC-D02 |
| AC-27 ยกเลิก(cancelled) + เหตุผล → toast "ยกเลิกรอบปลูกแล้ว" + audit · ไม่ใส่เหตุผล → block | TC-D01, TC-D04 |
| AC-28 ลบ(deleted) + เหตุผล → soft delete + ซ่อนจาก list + audit | TC-D02, TC-D03 |

### Cross-Module (06_TESTS §6.9) ⭐⭐ DOUBLE READ-ONLY
| XT | Scenario | Source | Case |
|---|---|---|---|
| XT-01 | สร้าง crop → crop.quota_id/plot_id set + snapshot ตรง · **quota/plot ไม่ถูกแก้** | Quota+Plot (read) | TC-X02, TC-X05 |
| XT-02 | quota search exact verified → คืน verified quota + farmer owner · ไม่ verified → block/excluded | Quota | TC-X01, TC-C03 |
| XT-03 | plot load ของเจ้าของ quota + verified · owner อื่น/ไม่ verified → excluded | Plot | TC-X03, TC-C04 |
| XT-04 | ETCD compute remaining = total − ΣETCD · ติดลบ → badge | ETCD external | TC-X04, TC-L08, TC-W03 |
| XT-05 | ETCD/Survey down → fail-soft (crop mutation/landing ยังทำงาน) | external | TC-X06 (ต้อง simulate) |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-AGC-01 double-binding บังคับ (Quota verified,exact → Plot owner+verified → form) | TC-C01, TC-C02, TC-X01, TC-X03 |
| BR-AGC-02 snapshot farmer/address/size read-only | TC-C01, TC-X02, TC-W01 |
| BR-AGC-03 create/CSV → waiting_for_verify เสมอ | TC-C01, TC-I06 |
| BR-AGC-04 **edit crop verified + save → กลับ waiting_for_verify** ⭐ | TC-E02 |
| BR-AGC-05 quota_id/plot_id แก้ไม่ได้ตอน edit | TC-E04 |
| BR-AGC-06 verify/reject: waiting เท่านั้น · reject reason บังคับ · เดี่ยว+bulk (skip non-eligible) | TC-V01, TC-V02, TC-B01, TC-B02 |
| BR-AGC-07 remaining = total_tons − ΣETCD · negative allowed + badge | TC-L08, TC-W03, TC-X04 |
| BR-AGC-08 ETCD/Survey read-only + fail-soft | TC-W03, TC-W04, TC-X06 |
| BR-AGC-09 soft cancel/delete + reason บังคับ + audit | TC-D01, TC-D02, TC-W04 |
| BR-AGC-10 CSV per-row idempotent · ทุกแถว waiting · partial + report | TC-I02, TC-I06 |
| BR-AGC-11 optimistic lock + idempotency ทุก mutation | TC-C12, TC-S01, TC-S03 |
| BR-AGC-12 audit ทุก mutation (+ bulk count) | TC-W04, TC-B01 |

### Validation (05_RULES §5.4 VR-01..09)
| VR | cases |
|---|---|
| VR-01 quota_id กรอก+verified → "ไม่พบ Quota หรือสถานะไม่เป็น verified" | TC-C03, TC-X01, TC-I05 |
| VR-02 plot_id ของ owner + verified → "ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ" | TC-C04, TC-X03, TC-I05 |
| VR-03 production_year_be 2500-2600 | TC-C06, TC-E05, TC-I02 |
| VR-04 planted_month 1-12 | TC-C07, TC-I05 |
| VR-05 total_tons ≥ 0 (อนุญาต 0) | TC-C08, TC-I02 |
| VR-06 reject_reason บังคับเมื่อ reject | TC-V02, TC-B02 |
| VR-07 postal_code 5 หลัก (ถ้ากรอก) | TC-C11 |
| VR-08 photos ชนิด/ขนาด policy | TC-C09 (ต้อง simulate — policy server) |
| VR-09 cancel/delete reason บังคับ | TC-D01, TC-D02 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 quota ไม่พบ/ไม่ verified → block | TC-C03, TC-X01, TC-I05 |
| EC-02 plot ไม่ใช่ของเจ้าของ quota / ไม่ verified → block owner mismatch | TC-C04, TC-X03, TC-I05 |
| EC-03 year นอก 2500-2600 | TC-C06, TC-E05 |
| EC-04 month นอก 1-12 | TC-C07, TC-I05 |
| EC-05 total_tons < 0 / ไม่ใช่ตัวเลข | TC-C08 |
| EC-06 reject ไม่ใส่เหตุผล | TC-V02, TC-B02 |
| EC-07 edit crop verified → save → กลับ waiting (BR-04) ⭐ | TC-E02 |
| EC-08 แก้ quota/plot ตอน edit → อ่านอย่างเดียว (block) | TC-E04 |
| EC-09 bulk เลือกรวม non-waiting → skip + summary | TC-B03 (ต้อง simulate per-record) |
| EC-10 remaining ติดลบ → badge แดง (ไม่ block verify — OQ-C5) | TC-L08, TC-V01, TC-X04 |
| EC-11 ETCD/Survey down → fail-soft "ดึงข้อมูล...ไม่สำเร็จ" (ไม่ block landing) | TC-X06 (ต้อง simulate) |
| EC-12 stale edit → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| EC-13 concurrent verify (status เปลี่ยน) → 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (ต้อง simulate) |
| EC-14 CSV header ไม่ตรง → reject ทั้งไฟล์ + column error | TC-I04 |
| EC-15 CSV row quota/plot invalid → error รายแถว | TC-I05, TC-I02 |
| EC-16 double-submit create → idempotency → 1 รายการ | TC-C12 |
| EC-17 deep-link crop ไม่มี/deleted → "ไม่พบข้อมูลรอบปลูกที่เลือก" + กลับ list | TC-W05, TC-D02 |
| EC-18 cancel/delete ไม่ใส่เหตุผล → VR-09 block | TC-D01, TC-D02 |

### Legacy carry-over (TC-547..586 → AS-BUILT anchors)
| Legacy TC | Scenario | Case |
|---|---|---|
| TC-547 create เดี่ยว ครบขั้น + navigate landing | TC-C01 · TC-548 quota ไม่พบ/ไม่ verified TC-C03 |
| TC-549 plot ไม่ใช่ของ quota/ไม่ verified → ปฏิเสธก่อนเปิดฟอร์ม | TC-C04 · TC-550 validate year/month/tons TC-C06/C07/C08 |
| TC-551 generate crop_id format/sequence | TC-C01 (format CRP-2569-000000N) · TC-S03 (race) |
| TC-552 insert idempotency same-key | TC-C12 · TC-553 photo upload dedupe TC-C09 |
| TC-554 edit load + save reset status→waiting | TC-E02 · TC-555 edit เปลี่ยน quota/plot ถูกปฏิเสธ TC-E04 |
| TC-556 optimistic lock conflict + retry | TC-S01 (ต้อง simulate) |
| TC-557 list search/filter/sort/pagination + negative badge | TC-L02/L03/L05/L06/L08 |
| TC-558 bulk verify/reject + partial failure | TC-B01/B02 · TC-559 bulk skip non-eligible TC-B03 |
| TC-560 landing overview + etcd/survey tabs | TC-W01/W03/W04 · TC-561 etcd fail-soft TC-X06 |
| TC-562 compute remaining allow negative + badge | TC-L08/TC-X04 · TC-564 etcd bookings + total_booked TC-W03 |
| TC-565 surveys + latest synced | TC-W04 · TC-566 csv header mismatch TC-I04 |
| TC-567 csv per-row validation | TC-I05 · TC-568 csv commit idempotent + report TC-I02/I06 |
| TC-569 soft delete/cancel + reason + audit | TC-D01/D02 · TC-570 soft delete idempotent + double confirm TC-D03/S03 |
| TC-571 verify single waiting→verified | TC-V01 · TC-572 verify state error not-waiting TC-V05/S02 |
| TC-573 bulk verify atomic + summary + idempotency | TC-B01 · TC-574 negative badge list+landing warn TC-L08/W01 |
| TC-575 crop_id sequence concurrency race | TC-S03 · TC-576 double-submit protection TC-C12 |
| TC-577/578 nfr latency/write SLA + orphan photo | TC-S03 (ต้อง simulate) |
| TC-580 view/download photos | TC-W02 · TC-581 search trim/unicode/debounce TC-L02 |
| TC-582 export list csv (pending-spec) | TC-L07 (ต้อง simulate) · TC-583 deeplink landing + recovery TC-W05 |
| TC-585 total_tons allow zero reject negative | TC-C08 · TC-586 audit every state change TC-W04 |

### Error catalog (05_RULES §5.6 — ที่มีผลบน UI prototype)
| error | cases |
|---|---|
| ERR_QUOTA_NOT_VERIFIED "ไม่พบ Quota หรือสถานะไม่เป็น verified" | TC-C03, TC-X01, TC-I05 |
| ERR_PLOT_OWNER_MISMATCH "ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ" | TC-C04, TC-X03, TC-I05 |
| ERR_VALIDATION (รายช่อง year/month/tons/postal) | TC-C06..C08, TC-C11, TC-I05 |
| (submit ก่อนครบ) "กรุณาเลือกโควตาและแปลงก่อน" | TC-C05, TC-C02 |
| (submit incomplete) "กรุณากรอกข้อมูลให้ครบถ้วน" | TC-C10 |
| ERR_REJECT_NO_REASON "กรุณากรอกเหตุผลในการปฏิเสธ" | TC-V02, TC-B02 |
| (verify no result) "กรุณาเลือกผลการตรวจสอบ" | TC-V04 |
| (cancel/delete no reason) "กรุณากรอกเหตุผล" | TC-D01, TC-D02 |
| (verify non-waiting selected) "เลือกได้เฉพาะรายการที่รอตรวจสอบ" | TC-V05, TC-B01 |
| ERR_CSV_INVALID "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" · (>5MB) "ขนาดไฟล์ต้องไม่เกิน 5MB" | TC-I03 |
| (CSV header) "ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ" + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]" | TC-I04 |
| ERR_STALE(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (simulate) |
| ERR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (simulate) |
| ERR_NOT_FOUND "ไม่พบข้อมูลรอบปลูกที่เลือก" | TC-W05, TC-D02 |
| ERR_ETCD_UNAVAILABLE (fail-soft) "ดึงข้อมูล...ไม่สำเร็จ" | TC-X06 (simulate) |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases / สถานะ |
|---|---|
| เจ้าหน้าที่ crop: create/edit/csv/cancel/delete = allow | TC-C01, TC-E01, TC-D01, TC-I02 (prototype user=สมพร วงศ์ทะเบียน) |
| ผู้ตรวจสอบ: +verify/reject/bulk = allow | TC-V01, TC-B01 (prototype verify actor=ธนพล ตรวจสอบ) |
| ปุ่มซ่อนตาม RBAC (เจ้าหน้าที่ crop เห็น verify ไม่ได้) | — ข้าม (prototype ไม่มี role switching — ทดสอบระบบจริงผ่าน RBAC; UI จริงต้องซ่อนปุ่ม §5.3) |
| SoD self-verify block (OQ-C4) | TC-S04 (ต้อง simulate) |

### Scope Lock (00_OVERVIEW §0.11 ← BRD §3.4)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | capability legacy 100% (CRUD/CSV/verify/reject/bulk/cancel/delete/search/export) | ทั้ง suite — ตัวแทน: TC-C01, TC-I02, TC-V01, TC-B01, TC-E01, TC-D01, TC-W01, TC-L02 |
| LOCK-02 | canonical **5-state** machine + soft cancel/delete | TC-V01, TC-V03, TC-D01, TC-D02, TC-L01 |
| LOCK-03 | **double-binding (quota→plot) read-only** ⭐⭐ | TC-C01, TC-C02, TC-X01, TC-X03 |
| LOCK-04 | snapshot farmer/address/size read-only | TC-C01, TC-X02, TC-W01 |
| LOCK-05 | **edit verified → waiting_for_verify** ⭐ | TC-E02 |
| LOCK-06 | quota/plot immutable on edit | TC-E04 |
| LOCK-07 | verify/reject (reject reason บังคับ) เดี่ยว+bulk | TC-V01, TC-V02, TC-B01, TC-B02 |
| LOCK-08 | **remaining = total − ΣETCD ติดลบได้ + badge** ⭐ | TC-L08, TC-W03, TC-X04 |
| LOCK-09 | ETCD/Survey read-only fail-soft | TC-W03, TC-W04, TC-X06 |
| LOCK-10 | CSV partial + ทุกแถว waiting | TC-I02, TC-I06 |
| LOCK-11 | soft cancel/delete + reason บังคับ | TC-D01, TC-D02 |
| LOCK-12 | optimistic + idempotency + audit | TC-C12, TC-S01, TC-W04 |
| LOCK-13 | year 2500-2600 / month 1-12 / tons ≥ 0 | TC-C06, TC-C07, TC-C08 |

### UI States (§8 State-Driven Matrix — canonical 5)
| item | cases |
|---|---|
| loaded / filtered / filter-empty | TC-L01, TC-L02, TC-L04 |
| stats 4 การ์ด (คงเหลือติดลบ 2 · ค้างเกิน 7 วัน 3) | TC-L01 |
| pill 5 สถานะ (รอตรวจสอบ/ตรวจแล้ว/ปฏิเสธ/ยกเลิก + deleted ซ่อน) | TC-L01, TC-D02, TC-D04 |
| remaining badge (แดงเมื่อ < 0) ⭐ | TC-L08, TC-X04 |
| checkbox waiting selectable / อื่น disabled | TC-B01, TC-V05 |
| snapshot card (orange) + ดูโควตา/ดูแปลง (read-only) | TC-W01, TC-W02 |
| field gating (locked จนครบ quota+plot) ⭐⭐ | TC-C02 |
| landing actions ตามสถานะ (แก้ไข/ตรวจสอบ/ยกเลิก-ลบ) | TC-V05, TC-D03 |
| submitting state ("กำลังบันทึก…/กำลังดำเนินการ…/กำลังนำเข้า…") | TC-C01, TC-V01, TC-D01, TC-I02 |
| sort / pagination footer | TC-L05, TC-L06 |

**Manifest cross-check (FRD §0.12):** Stories 10/10 (US-01..10) · Rules BR-AGC-01..12 12/12 · VR-01..09 9/9 · EC-01..18 18/18 · XT-01..05 5/5 · LOCK-01..13 13/13 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — รอบปลูกถูกต้อง (happy — ผูก QT-2569-001 + PLT-2569-001)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาโควตา (Quota Id · exact) | เลือก **QT-2569-001 · สมหญิง รักดี** *(verified — sub "0823456789 · 3-XXXX-XXXX-XX-2")* |
| เลือกแปลง (ของเจ้าของโควตา · verified) | เลือก **PLT-2569-001 · 99 หมู่ 3** *(sub "วังขนาย ท่าม่วง กาญจนบุรี" · right "12.50 ไร่")* |
| ปีผลิต (พ.ศ.) | 2569 |
| เดือนที่ปลูก | 7 · ก.ค. |
| ปริมาณรวม (ตัน) | 100 |
| ละติจูด (lat) / ลองจิจูด (long) | 14.023145 / 99.512088 *(ไม่บังคับ)* |
| รหัสไปรษณีย์ | *(เว้นว่าง — ไม่บังคับ)* |
| รูปภาพ | คลิก **แนบรูปภาพ** (จำลอง) |

### ชุด B — ค่าผิดสำหรับ negative (ต้องเลือกโควตา+แปลง ชุด A ก่อน เพื่อปลดล็อกฟิลด์)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | ปีผลิต (พ.ศ.) | `2400` | ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600 |
| B2 | เดือนที่ปลูก | *(ไม่เลือก — คง "— เลือกเดือน —")* | กรุณาเลือกเดือนที่ปลูก |
| B3 | ปริมาณรวม (ตัน) | `-5` | ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0 |
| B4 | รหัสไปรษณีย์ | `123` | รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก |
| B5 | ค้นหาโควตา | พิมพ์ `QT-9999` | ไม่พบ Quota หรือสถานะไม่เป็น verified (emptyText) |
| B6 | ค้นหาโควตา | พิมพ์ `สมพงษ์` (เจ้าของ QT-2569-005 waiting) | ไม่พบ Quota หรือสถานะไม่เป็น verified (ไม่ขึ้น dropdown — ไม่ verified) |
| B7 | quota+plot | *(ไม่เลือกเลย → submit)* | กรุณาเลือกโควตาและแปลงก่อน |

### ไฟล์ทดสอบ (Files) — runner ต้องเตรียมก่อนรัน
> header 5 คอลัมน์ (จาก `CSV_COLS`): `quota_id,plot_id,year_be,planted_month,total_tons`
> *(แม่แบบดาวน์โหลดได้ในModal = `crop_template.csv` · schema = create)*

| ชื่อไฟล์ | เนื้อหา |
|---|---|
| `crop_ok.csv` | 3 แถวถูกทั้งหมด: `QT-2569-001,PLT-2569-001,2569,1,120.00` · `QT-2569-002,PLT-2569-003,2568,12,200.00` · `QT-2569-004,PLT-2569-006,2569,5,150.00` |
| `crop_mixed.csv` | 5 แถว: 3 ถูก + แถว 4 `year_be=2400` (นอกช่วง) + แถว 5 `total_tons=-5` |
| `crop_badbind.csv` | 3 แถว: แถว 1 ถูก · แถว 2 `quota_id=QT-2569-005` (ไม่ verified) · แถว 3 `QT-2569-001,PLT-2569-003` (plot owner mismatch — PLT-003 เป็นของ QT-002) |
| `crop_badheader.csv` | header ขาดคอลัมน์ `total_tons` (เหลือ 4 คอลัมน์) + 1 แถวข้อมูลถูก |
| `crop_badmonth.csv` | 2 แถว: แถว 1 `planted_month=13` (นอก 1-12) · แถว 2 `plot_id=PLT-2569-004` (waiting, owner QT-002) กับ quota QT-002 |
| `crop_too_large.csv` | ไฟล์ .csv ขนาด > 5MB (gen แถวซ้ำจนเกิน) |
| `notes.xlsx` | ไฟล์ Excel ใด ๆ (ทดสอบ guard นามสกุลไฟล์) |

---

## Test Cases

## Group L — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination / remaining badge (P-01)

### TC-L01 — เปิดหน้า list + stats widgets (happy)
- group: L · ความสำคัญ: สูง · trace: 01_UI P-01 / UI state loaded / D-01 stats
- Setup: role=เจ้าหน้าที่รอบปลูก (default) · seed=default 8 รอบปลูก (refresh) · files=—
- Start: OPEN `#/crops`
- ผ่านเมื่อ: หน้า list + สถิติ 4 การ์ดแสดงเลขตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/crops` | — | หัวข้อ **จัดการรอบปลูก** + count **8 รายการ** · sub "ทะเบียนรอบปลูกอ้อย · ผูกโควตา→แปลง · ตรวจสอบยืนยันและนำเข้า CSV" · breadcrumb "เกษตรกรรม › จัดการรอบปลูก" · sidebar **จัดการรอบปลูก** active | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **รอบปลูกทั้งหมด 8** (meta ส้ม "คงเหลือติดลบ 2 รายการ") · **รอตรวจสอบ 4** (meta ส้ม "ค้างเกิน 7 วัน 3 รายการ") · **ตรวจแล้ว 2** (sub "พร้อมทำสัญญา") · **ปฏิเสธ 1** (sub "มีเหตุผลระบุ") | ☐ |
| 3 | VERIFY ปุ่มบน page header (ขวาบน) | — | เรียงซ้าย→ขวา: **Upload CSV** · **ตรวจสอบที่เลือก (0)** (disabled) · **สร้างรอบปลูก** (ปุ่มแดง ขวาสุด) | ☐ |
| 4 | VERIFY ตาราง | — | 10 คอลัมน์: ☑, เลขรอบปลูก (mono แดง), ปี (พ.ศ.), เลขโควตา, เลขแปลง, เกษตรกร, รวมตัน, **คงเหลือ (ยังไม่จอง)**, สถานะ, การดำเนินการ · pill 4 สี ครบ (รอตรวจสอบ/ตรวจแล้ว/ปฏิเสธ/ยกเลิก) | ☐ |
| 5 | VERIFY แถว CRP-2569-0000002 คอลัมน์ คงเหลือ | — | badge **แดง −20.00** (pill-danger) · แถว CRP-0000001 badge เทา **40.00** | ☐ |
| 6 | VERIFY footer ตาราง | — | ข้อความ **1 – 8 จาก 8 รายการ** | ☐ |

### TC-L02 — ค้นหา (debounce 300ms, 4 field) (happy — AC-09)
- group: L · ความสำคัญ: สูง · trace: AC-09 / US-10 / legacy TC-557/581
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`
- ผ่านเมื่อ: ค้นได้ crop_id/quota/plot/farmer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "CRP-2569-0000007" → ช่องค้นหา | เลขรอบปลูก | รอ ~0.3s ตารางเหลือ 1 แถว: CRP-2569-0000007 ทองดี พูลผล (pill แดง **ปฏิเสธ**) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** แล้ว TYPE "QT-2569-001" | เลขโควตา | เหลือ 2 แถว (CRP-0000001, CRP-0000002 — ผูกโควตาเดียวกัน) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** แล้ว TYPE "PLT-2569-003" | เลขแปลง | เหลือ 2 แถว (CRP-0000003, CRP-0000006 — ผูกแปลงเดียวกัน) | ☐ |
| 4 | CLICK **ล้างตัวกรอง** แล้ว TYPE "สุรพล" | ชื่อเกษตรกร | เหลือ 2 แถว (CRP-0000003, CRP-0000006 สุรพล เก่งการไร่) | ☐ |
| 5 | CLICK **ล้างตัวกรอง** แล้ว TYPE "ประนอม" | ชื่อเกษตรกร | เหลือ 2 แถว (CRP-0000005, CRP-0000008 ประนอม ใจเพชร) | ☐ |

### TC-L03 — กรองสถานะ (5) + ปี (พ.ศ.) (happy — AC-09)
- group: L · ความสำคัญ: สูง · trace: AC-09 / filter status(5)+year
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **รอตรวจสอบ** | — | เหลือ 4 แถว ทุกแถว pill เหลือง · footer "1 – 4 จาก 4 รายการ" | ☐ |
| 2 | SELECT dropdown สถานะ = **ตรวจแล้ว** | — | เหลือ 2 แถว (CRP-0000003, CRP-0000006) pill เขียว **ตรวจแล้ว** | ☐ |
| 3 | SELECT dropdown สถานะ = **ปฏิเสธ** | — | เหลือ 1 แถว (CRP-0000007) pill แดง **ปฏิเสธ** | ☐ |
| 4 | SELECT dropdown สถานะ = **ยกเลิก** | — | เหลือ 1 แถว (CRP-0000008) pill เทา **ยกเลิก** — ยืนยัน cancelled คงอยู่ในรายการ | ☐ |
| 5 | CLICK **ล้างตัวกรอง** → SELECT dropdown ปี = **2568** | — | เหลือ 2 แถว (CRP-0000003, CRP-0000007 ปี 2568) · dropdown ปีมีตัวเลือก "ทุกปี (พ.ศ.)" + 2569 + 2568 | ☐ |

### TC-L04 — ค้นหาไม่เจอ → empty state (edge — AC-09)
- group: L · ความสำคัญ: กลาง · trace: AC-09 filter-empty
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีรอบปลูกนี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state: **ไม่พบรายการที่ค้นหา** + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty state) | — | ตารางกลับมา 8 รายการ | ☐ |

### TC-L05 — Sort คอลัมน์ (AC-10)
- group: L · ความสำคัญ: ต่ำ · trace: AC-10 / sortBy crop_id/year_be/total_tons / legacy TC-557
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **รวมตัน** | — | แถวเรียงน้อย→มาก (60.00 = CRP-0000004 บนสุด → 300.00 = CRP-0000006 ล่าง) | ☐ |
| 2 | CLICK หัวคอลัมน์ **รวมตัน** อีกครั้ง | — | เรียงกลับ มาก→น้อย (300.00 บนสุด) | ☐ |
| 3 | CLICK หัวคอลัมน์ **เลขรอบปลูก** | — | เรียงตาม crop_id (CRP-2569-0000001 บนสุด) | ☐ |
| 4 | CLICK หัวคอลัมน์ **ปี (พ.ศ.)** | — | เรียงตาม year_be (2568 บนสุด: CRP-0000003, CRP-0000007) | ☐ |

### TC-L06 — Pagination footer + row-click เปิด Landing (AC-10)
- group: L · ความสำคัญ: ต่ำ · trace: AC-10 / row-click = openView
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (8 < 20/หน้า — หน้าเดียว) · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ pagination | — | ปุ่มหน้า **1** (active สีแดง) · ลูกศรซ้าย/ขวา disabled (หน้าเดียว) | ☐ |
| 2 | CLICK กลางแถว CRP-2569-0000003 (ไม่โดน checkbox/ไอคอน) | — | Landing drawer เปิด eyebrow "รอบปลูก · QT-2569-002 · PLT-2569-003" + หัวข้อ **CRP-2569-0000003** + route เปลี่ยนเป็น `#/crops/CRP-2569-0000003` | ☐ |
| 3 | PRESS Esc | — | drawer ปิด + route กลับ `#/crops` | ☐ |

### TC-L07 — Export CSV เคารพ filter (AC-10) (ต้อง simulate)
- group: L · ความสำคัญ: กลาง · trace: AC-10 / API-17 / legacy TC-582 · **หมายเหตุ: prototype ไม่มีปุ่ม Export ในหน้า header (มีเฉพาะ Upload CSV) — export = server-side/UI phase ถัดไป**
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default
- Start: — (SIT / UI ระบบจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (prototype): หน้า header | — | มีปุ่ม Upload CSV แต่ **ไม่มีปุ่ม Export** — mark BLOCKED บน prototype (export ยังไม่มี UI) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): filter สถานะ=ตรวจแล้ว → Export CSV | — | ไฟล์ CSV มีเฉพาะแถวที่ตรง filter · คอลัมน์ตรงตาราง · ชื่อไฟล์ locale ไทย | ☐ |

### TC-L08 — Remaining badge ติดลบ (แดง) บน list ⭐ (AC-29 / EC-10 / LOCK-08)
- group: L · ความสำคัญ: สูง · trace: AC-29 / BR-AGC-07 / XT-04 / legacy TC-574
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`
- ผ่านเมื่อ: badge แดงเฉพาะรายการ remaining < 0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY การ์ด **รอบปลูกทั้งหมด** meta | — | ข้อความส้ม **คงเหลือติดลบ 2 รายการ** (negCount = CRP-0000002 + CRP-0000004) | ☐ |
| 2 | TYPE "QT-2569-001" → ช่องค้นหา | — | 2 แถว: CRP-0000001 badge เทา **40.00** · CRP-0000002 badge **แดง −20.00** (120−80=40 · 90−110=−20) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** → TYPE "QT-2569-003" | — | 2 แถว: CRP-0000004 badge **แดง −15.00** (60−75) · CRP-0000007 badge เทา 50.00 (80−30) | ☐ |
| 4 | VERIFY แถวอื่น (เช่น CRP-0000005) | — | badge เทา **150.00** (ไม่มี ETCD จอง — 150−0) | ☐ |

---

## Group C — สร้างรอบปลูก + double-binding + validation (OV-01)

### TC-C01 — สร้างรอบปลูก happy (double-bind QT-2569-001 + PLT-2569-001) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-02, AC-03 / BR-AGC-01/02/03 / LOCK-03/04 / XT-01
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`
- ชุดข้อมูล: A
- ผ่านเมื่อ: quota+plot snapshot + toast สร้างสำเร็จ + แถวใหม่ waiting_for_verify

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างรอบปลูก** (แดง ขวาบน) | — | drawer เปิดจากขวา eyebrow **สร้างรอบปลูก** + หัวข้อ **สร้างรอบปลูก** · section **เลือกโควตาและแปลง (บังคับก่อนกรอกข้อมูล)** · ฟิลด์รอบปลูกล็อก + note "เลือกโควตาและแปลงก่อนจึงจะกรอกข้อมูลรอบปลูกได้" | ☐ |
| 2 | CLICK ช่อง **ค้นหาโควตา (Quota Id · exact)** → พิมพ์ "QT-2569-001" | A | dropdown แสดง **QT-2569-001 · สมหญิง รักดี** + sub "0823456789 · 3-XXXX-XXXX-XX-2" · help "เลือกได้เฉพาะโควตาที่ตรวจแล้ว (verified) · ระบบจะดึงข้อมูลเจ้าของให้อัตโนมัติ" | ☐ |
| 3 | CLICK ตัวเลือก **QT-2569-001 · สมหญิง รักดี** | A | การ์ด **เจ้าของโควตา** (teal/ส้ม): QT-2569-001 · สมหญิง รักดี · 0823456789 + "เลขบัตร 3-XXXX-XXXX-XX-2" + ปุ่ม **เปลี่ยนโควตา** · ปรากฏ section **เลือกแปลง (ของเจ้าของโควตา · verified)** help "แสดงเฉพาะแปลงที่ตรวจแล้วของเจ้าของโควตานี้ (2 แปลง)" | ☐ |
| 4 | CLICK ช่องเลือกแปลง → เลือก **PLT-2569-001 · 99 หมู่ 3** | A | การ์ดเขียว **แปลงที่เลือก**: PLT-2569-001 · 99 หมู่ 3 · วังขนาย ท่าม่วง กาญจนบุรี + "ขนาด 12.50 ไร่" + ปุ่ม **เปลี่ยนแปลง** · **ฟิลด์รอบปลูกปลดล็อก** (opacity เต็ม) · note lock หาย | ☐ |
| 5 | กรอก: ปีผลิต (พ.ศ.) 2569 · เดือนที่ปลูก **7 · ก.ค.** · ปริมาณรวม (ตัน) 100 | A | แสดงค่าครบ (year inputmode numeric, tons decimal) | ☐ |
| 6 | (ไม่บังคับ) TYPE ละติจูด 14.023145 · ลองจิจูด 99.512088 | A | แสดงค่า | ☐ |
| 7 | CLICK ปุ่ม **แนบรูปภาพ** | — | toast info **จำลองแนบรูป (JPG/PNG ≤5MB)** · รายการไฟล์ crop_photo_1_*.jpg ปรากฏใต้ปุ่ม | ☐ |
| 8 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (กดซ้ำไม่ได้) | ☐ |
| 9 | WAIT จน toast ปรากฏ (≤3s) | — | drawer ปิด + toast เขียว **สร้างรอบปลูกสำเร็จ — CRP-2569-0000009** | ☐ |
| 10 | VERIFY ตาราง | — | แถวบนสุด = CRP-2569-0000009 สมหญิง รักดี · pill เหลือง **รอตรวจสอบ** · count = **9 รายการ** · การ์ดรอตรวจสอบ = 5 | ☐ |
| 11 | CLICK แถว CRP-2569-0000009 → Tab **ประวัติ** | — | มี 1 event **สร้างรอบปลูก** โดย สมพร วงศ์ทะเบียน + note "ผูกโควตา QT-2569-001 · แปลง PLT-2569-001 · สมหญิง รักดี" | ☐ |

### TC-C02 — Field gating: ฟิลด์ล็อกจนครบ quota+plot ★★ signature
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-07 / BR-AGC-01 / LOCK-03 / double-binding
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**
- ผ่านเมื่อ: ฟิลด์ล็อกจนกว่าจะเลือก **ทั้ง** quota และ plot (double-binding)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY block ฟิลด์รอบปลูก ก่อนเลือกอะไร | — | โซน `#crop-fields` จางลง (opacity ~0.55, pointer-events none) · note มีไอคอน lock "เลือกโควตาและแปลงก่อนจึงจะกรอกข้อมูลรอบปลูกได้" · ทุก input/select disabled | ☐ |
| 2 | CLICK ค้นหาโควตา → เลือก **QT-2569-002 · สุรพล เก่งการไร่** (เลือก quota อย่างเดียว) | — | การ์ดเจ้าของโควตาปรากฏ + section เลือกแปลง · **ฟิลด์ยัง locked** (ยังไม่เลือกแปลง — double-binding บังคับทั้งคู่) | ☐ |
| 3 | CLICK เลือกแปลง → เลือก **PLT-2569-003** | — | การ์ดแปลงปรากฏ · **ฟิลด์ปลดล็อกทันที** (opacity เต็ม, พิมพ์ได้) · note lock หาย | ☐ |
| 4 | CLICK ปุ่ม **เปลี่ยนโควตา** | — | กลับไปโหมดค้นหาโควตา · แปลงถูกล้าง (plot reset) · ฟิลด์ล็อกอีกครั้ง (double-binding รีเซ็ต) | ☐ |

### TC-C03 — โควตาไม่พบ / ไม่ verified → block (negative — AC-02b / EC-01 / XT-02)
- group: C · ความสำคัญ: สูง · trace: AC-02b / VR-01 / ERR_QUOTA_NOT_VERIFIED / legacy TC-548
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**
- ชุดข้อมูล: B5, B6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ค้นหาโควตา → พิมพ์ "QT-9999" | B5 | dropdown แสดงข้อความว่าง **ไม่พบ Quota หรือสถานะไม่เป็น verified** (emptyText) | ☐ |
| 2 | ลบคำค้น พิมพ์ "สมพงษ์" (เจ้าของ QT-2569-005 ที่ waiting) | B6 | **ไม่ขึ้น** QT-2569-005 ใน dropdown (verifiedQuotas ตัดออก — ยังไม่ verified) → emptyText เดิม | ☐ |
| 3 | VERIFY section เลือกแปลง + ฟิลด์รอบปลูก | — | section เลือกแปลง **ยังไม่ปรากฏ** (ไม่มี quota ที่เลือก) · ฟิลด์รอบปลูก **ยัง locked** | ☐ |
| 4 | ลบคำค้น พิมพ์ "สมหญิง" | — | dropdown พบ **QT-2569-001 · สมหญิง รักดี** (ค้นด้วยชื่อได้ · verified) | ☐ |

### TC-C04 — แปลง: แสดงเฉพาะ owner+verified · owner mismatch/ไม่ verified ถูกตัด (AC-02/02c / XT-03)
- group: C · ความสำคัญ: สูงสุด · trace: AC-02, AC-02c / VR-02 / BR-AGC-01 / LOCK-03 / EC-02 / legacy TC-549
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**
- ผ่านเมื่อ: plot list ของโควตา = เฉพาะแปลงของเจ้าของ + verified

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกโควตา **QT-2569-002 · สุรพล เก่งการไร่** → CLICK ช่องเลือกแปลง | — | dropdown แสดง **1 แปลงเท่านั้น: PLT-2569-003** (PLT-2569-004 owner เดียวกันแต่ **waiting** ถูกตัดออก) · help "แสดงเฉพาะแปลงที่ตรวจแล้วของเจ้าของโควตานี้ (1 แปลง)" | ☐ |
| 2 | CLICK ปุ่ม **เปลี่ยนโควตา** → เลือก **QT-2569-004 · ประนอม ใจเพชร** → CLICK เลือกแปลง | — | dropdown แสดง **2 แปลง: PLT-2569-006, PLT-2569-007** (เฉพาะของ QT-004 + verified) · **ไม่มี** PLT ของโควตาอื่น (owner mismatch excluded) | ☐ |
| 3 | เลือก **PLT-2569-006** | — | การ์ดแปลง PLT-2569-006 · 5 หมู่ 5 · ท่าผา บ้านโป่ง ราชบุรี + "6.00 ไร่" · ฟิลด์ปลดล็อก | ☐ |

### TC-C05 — Submit ก่อนครบ quota+plot → block (negative — AC-07)
- group: C · ความสำคัญ: สูง · trace: AC-07 / BR-AGC-01 / "กรุณาเลือกโควตาและแปลงก่อน"
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**
- ชุดข้อมูล: B7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไม่เลือกอะไร → CLICK ปุ่ม **ยืนยันสร้าง** ทันที | B7 | ไม่บันทึก + toast เตือน **กรุณาเลือกโควตาและแปลงก่อน** (validateFormAll เด้งก่อน — ข้อความสุดท้ายบนจออาจตามด้วย "กรุณากรอกข้อมูลให้ครบถ้วน") — ไม่มีรอบปลูกใหม่ | ☐ |
| 2 | เลือก quota QT-2569-001 อย่างเดียว (ไม่เลือกแปลง) → CLICK **ยืนยันสร้าง** | — | block เดิม **กรุณาเลือกโควตาและแปลงก่อน** (plot ยังไม่ครบ) | ☐ |
| 3 | VERIFY count ตาราง (หลังปิด drawer) | — | ยัง 8 รายการ | ☐ |

### TC-C06 — ปีผลิต (พ.ศ.) นอกช่วง 2500-2600 (negative — AC-04 / VR-03 / LOCK-13)
- group: C · ความสำคัญ: สูง · trace: AC-04 / VR-03 / EC-03 / D-05 (checklist 2500-2100 ถูก reject · code = 2500-2600)
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "2400" → ช่อง **ปีผลิต (พ.ศ.)** → กรอก month/tons ครบ → CLICK **ยืนยันสร้าง** | B1 | ข้อความแดงใต้ช่องปี **ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600** + กรอบช่องแดง + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | แก้เป็น "2569" → CLICK **ยืนยันสร้าง** → WAIT | — | error หาย → บันทึกสำเร็จ toast **สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]** | ☐ |
| 3 | (ตรวจ empty) เปิดสร้างใหม่ → เว้นช่องปีว่าง → ยืนยันสร้าง | — | ข้อความแดง **กรุณากรอกปีผลผลิต พ.ศ.** | ☐ |

### TC-C07 — เดือนที่ปลูกไม่เลือก (negative — AC-05 / VR-04)
- group: C · ความสำคัญ: สูง · trace: AC-05 / VR-04 / EC-04
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001
- ชุดข้อมูล: B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | คง dropdown **เดือนที่ปลูก** ที่ "— เลือกเดือน —" → กรอก ปี 2569 + ตัน 100 → CLICK **ยืนยันสร้าง** | B2 | ข้อความแดงใต้ dropdown **กรุณาเลือกเดือนที่ปลูก** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | SELECT เดือน **5 · พ.ค.** → CLICK **ยืนยันสร้าง** → WAIT | — | บันทึกสำเร็จ toast **สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]** | ☐ |

### TC-C08 — ปริมาณรวมติดลบ · อนุญาต 0 (negative/edge — AC-06 / VR-05 / LOCK-13)
- group: C · ความสำคัญ: สูง · trace: AC-06 / VR-05 / EC-05 / legacy TC-585
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "-5" → ช่อง **ปริมาณรวม (ตัน)** → กรอก ปี/เดือน ครบ → CLICK **ยืนยันสร้าง** | B3 | ข้อความแดง **ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0** | ☐ |
| 2 | แก้เป็น "0" → CLICK **ยืนยันสร้าง** → WAIT | — | **อนุญาต** (≥ 0) → บันทึกสำเร็จ toast **สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]** (0.00 ตัน ถูกต้อง) | ☐ |
| 3 | (ตรวจ empty) เปิดใหม่ → เว้นตันว่าง → ยืนยันสร้าง | — | ข้อความแดง **กรุณากรอกปริมาณรวม** | ☐ |

### TC-C09 — แนบรูปภาพหลายไฟล์ + ลบ (AC-08 / VR-08)
- group: C · ความสำคัญ: กลาง · trace: AC-08 / VR-08 (policy ชนิด/ขนาด = simulate server) / legacy TC-553
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แนบรูปภาพ** 3 ครั้ง | — | toast **จำลองแนบรูป (JPG/PNG ≤5MB)** แต่ละครั้ง · รายการ 3 ไฟล์ (crop_photo_1/2/3_*.jpg) ปรากฏ | ☐ |
| 2 | CLICK ปุ่ม X ลบไฟล์แรก | — | เหลือ 2 ไฟล์ในรายการ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): แนบไฟล์ชนิด/ขนาดผิด policy | — | server reject "ไฟล์รูปไม่ถูกต้อง (ชนิด/ขนาด)" (VR-08 · prototype จำลอง attach เท่านั้น — D-06) | ☐ |

### TC-C10 — required ครบชุด (negative — VR-01..05)
- group: C · ความสำคัญ: สูง · trace: VR-03/04/05 / ERR_VALIDATION
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001 (ปลดล็อกฟิลด์) → **ไม่กรอกอะไรต่อ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** ทันที (ฟิลด์ว่าง) | — | ไม่บันทึก + error ครบ: **กรุณากรอกปีผลผลิต พ.ศ. / กรุณาเลือกเดือนที่ปลูก / กรุณากรอกปริมาณรวม** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | VERIFY ช่อง **ตำแหน่ง (ไม่บังคับ)** lat/long/postal | — | ไม่มี error (optional) | ☐ |

### TC-C11 — รหัสไปรษณีย์ 5 หลัก (optional) (negative — VR-07)
- group: C · ความสำคัญ: กลาง · trace: VR-07 / "รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก"
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001 → กรอก ปี/เดือน/ตัน ครบ
- ชุดข้อมูล: B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "123" → ช่อง **รหัสไปรษณีย์** → CLICK **ยืนยันสร้าง** | B4 | ข้อความแดง **รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก** (validate เฉพาะเมื่อกรอก) | ☐ |
| 2 | ลบให้ว่าง → CLICK **ยืนยันสร้าง** → WAIT | — | ผ่าน (postal ว่างได้ — optional) → toast **สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]** | ☐ |

### TC-C12 — Double-click กันสร้างซ้ำ (edge — EC-16 / BR-AGC-11)
- group: C · ความสำคัญ: สูง · trace: EC-16 / BR-AGC-11 (idempotency + double-submit guard) / legacy TC-552/576
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก** → เลือก QT-2569-001 + PLT-2569-001 → กรอกชุด A ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งเร็วที่สุด (double-click) | — | คลิกแรกปุ่มกลายเป็น **กำลังบันทึก…** + disabled — คลิกที่สองไม่มีผล (f.submitting guard) | ☐ |
| 2 | WAIT จน toast → VERIFY ตาราง | — | มีรอบปลูกใหม่ **1 รายการเท่านั้น** (count = 9 รายการ, ไม่ใช่ 10) | ☐ |

---
## Group I — CSV Import (OV-05 — 5-col schema · ทุกแถว waiting_for_verify)

### TC-I01 — ดาวน์โหลดแม่แบบ + modal (5 คอลัมน์)
- group: I · ความสำคัญ: สูง · trace: US-03 / legacy TC-566 / schema = create
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Upload CSV** | — | modal หัวข้อ **นำเข้ารอบปลูกจากไฟล์ CSV** + subtitle ".csv (UTF-8) ≤5MB · ทุกแถวสถานะ \"รอตรวจสอบ\" · โควตา/แปลงต้อง verified" | ☐ |
| 2 | VERIFY แถบดาวน์โหลด + คำแนะนำ | — | แถบ **ดาวน์โหลดแม่แบบ CSV (schema = create)** + ปุ่ม **ดาวน์โหลดแม่แบบ** · คำแนะนำ "header ตรงแม่แบบ 5 คอลัมน์ · UTF-8 · โควตาต้อง verified · แปลงต้องเป็นของเจ้าของโควตา + verified" + "ปี พ.ศ. 2500-2600 · เดือน 1-12 · ปริมาณรวม ≥ 0" | ☐ |
| 3 | CLICK **ดาวน์โหลดแม่แบบ** | — | ได้ไฟล์ `crop_template.csv` — header 5 คอลัมน์: quota_id,plot_id,year_be,planted_month,total_tons + 2 แถวตัวอย่าง (UTF-8 BOM — ไทยไม่เพี้ยน) | ☐ |
| 4 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ยังไม่เลือกไฟล์) | ☐ |

### TC-I02 — Import แถวผสม → partial success + error report (happy — AC-14/16 / EC-15)
- group: I · ความสำคัญ: สูง · trace: AC-14, AC-16 / BR-AGC-10 / LOCK-10 · ทุกแถว waiting_for_verify
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=`crop_mixed.csv` (5 แถว: 3 ดี + year 2400 + tons -5)
- Start: OPEN `#/crops` → CLICK **Upload CSV**
- ผ่านเมื่อ: แถวดีสร้างครบ + แถวเสียรายงาน download ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD crop_mixed.csv | — | ชื่อไฟล์ + ขนาด (KB) แสดงข้างปุ่ม | ☐ |
| 2 | VERIFY สรุปผลตรวจ (preview — ก่อนเขียน) | — | 3 chip: **แถวทั้งหมด 5** · **ผ่าน 3** · **ไม่ผ่าน 2** | ☐ |
| 3 | VERIFY ตารางข้อผิดพลาด "รายละเอียดข้อผิดพลาด (แถวเสียจะถูกข้าม)" | — | 2 แถว: "แถว 5" year_be **ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600** · "แถว 6" total_tons **ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0** | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันนำเข้า (3 แถว)** → WAIT | — | ปุ่มเป็น **กำลังนำเข้า…** → phase done: chip แถวทั้งหมด 5 / **สร้างสำเร็จ 3** / **ล้มเหลว 2** + toast **นำเข้ารอบปลูก 3 รายการสำเร็จ — ข้าม 2 แถว** | ☐ |
| 5 | CLICK ปุ่ม **ดาวน์โหลดรายงาน** | — | ได้ไฟล์ `crop-upload-errors.csv` มี 2 แถว error | ☐ |
| 6 | CLICK **ปิด** → VERIFY ตาราง | — | รอบปลูกใหม่ 3 แถวบนสุด ทุกแถว pill เหลือง **รอตรวจสอบ** · count = **11 รายการ** | ☐ |

### TC-I03 — File guard: นามสกุล + ขนาด (negative — AC-17)
- group: I · ความสำคัญ: สูง · trace: AC-17 / ERR_CSV_INVALID
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=`notes.xlsx`, `crop_too_large.csv`
- Start: OPEN `#/crops` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD notes.xlsx | — | toast แดง **ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV** — ไฟล์ไม่ถูกรับ | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD crop_too_large.csv | — | toast แดง **ขนาดไฟล์ต้องไม่เกิน 5MB** — ไฟล์ไม่ถูกรับ, ปุ่มยืนยันยัง disabled | ☐ |

### TC-I04 — Header ไม่ตรงแม่แบบ → reject ทั้งไฟล์ (edge — AC-15 / EC-14)
- group: I · ความสำคัญ: สูง · trace: AC-15 / EC-14 / LOCK-10 / legacy TC-566
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=`crop_badheader.csv` (ขาดคอลัมน์ total_tons)
- Start: OPEN `#/crops` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD crop_badheader.csv | — | ไม่ขึ้น preview + ข้อความแดงใต้ช่องไฟล์ **คอลัมน์ไฟล์ไม่ตรงแม่แบบ: total_tons** (หรือ "จำนวนคอลัมน์ไม่ถูกต้อง (4/5)") + toast แดง **ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ** | ☐ |
| 2 | VERIFY ตารางหลังปิด modal | — | ไม่มีแถวใดถูกสร้าง (count ยัง 8 รายการ) | ☐ |

### TC-I05 — แถว quota/plot invalid รายแถว (edge — AC-16 / AC-02b/02c / EC-15)
- group: I · ความสำคัญ: สูง · trace: AC-16 / VR-01/02/04 / XT-02/03 / legacy TC-567
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=`crop_badbind.csv`, `crop_badmonth.csv`
- Start: OPEN `#/crops` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD crop_badbind.csv (แถว2 quota QT-005 · แถว3 owner mismatch) | — | preview: ผ่าน 1 / ไม่ผ่าน 2 — "แถว 3" quota_id **ไม่พบ Quota หรือสถานะไม่เป็น verified** · "แถว 4" plot_id **ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ** | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD crop_badmonth.csv | — | preview ใหม่: "แถว 2" planted_month **เดือนที่ปลูกต้องอยู่ระหว่าง 1-12** · "แถว 3" plot_id **ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ** (PLT-2569-004 = waiting) | ☐ |
| 3 | VERIFY ปุ่ม **ยืนยันนำเข้า** เมื่อผ่าน 0 | — | disabled (ถ้าทุกแถวเสีย validRows=0) | ☐ |

### TC-I06 — ไฟล์ถูกทั้งหมด → ทุกแถว waiting (happy — AC-14 / BR-AGC-03)
- group: I · ความสำคัญ: กลาง · trace: AC-14 / LOCK-10 / ทุกแถว waiting_for_verify
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=`crop_ok.csv` (3 แถวถูก)
- Start: OPEN `#/crops` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD crop_ok.csv | — | preview: ผ่าน 3 / ไม่ผ่าน 0 + แถบ **ทุกแถวผ่านการตรวจสอบ ไม่มีข้อผิดพลาด** | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (3 แถว)** → WAIT | — | phase done: สร้างสำเร็จ 3 + แถบ **นำเข้าสำเร็จทั้งหมด ไม่มีข้อผิดพลาด · ทุกแถวสถานะ "รอตรวจสอบ"** + toast เขียว **นำเข้ารอบปลูก 3 รายการสำเร็จ** (ไม่มี "ข้าม") | ☐ |
| 3 | CLICK **ปิด** → CLICK แถวรอบปลูกใหม่คนแรก → Tab **ประวัติ** | — | event **สร้างรอบปลูก** โดย "สมพร วงศ์ทะเบียน (CSV import)" + note "นำเข้าจาก CSV · ผูกโควตา..." · pill **รอตรวจสอบ** | ☐ |

---

## Group V — ตรวจสอบ / ปฏิเสธ เดี่ยว (OV-03)

### TC-V01 — Verify (ยืนยัน) เดี่ยว (happy — AC-18 / LOCK-07)
- group: V · ความสำคัญ: สูง · trace: AC-18 / US-05 / BR-AGC-06 / EC-10 (remaining ติดลบ ไม่ block verify)
- Setup: role=ผู้ตรวจสอบ (prototype: user เดียวกดได้) · seed=default (CRP-2569-0000005 waiting, คงเหลือ 150) · files=—
- Start: OPEN `#/crops/CRP-2569-0000005`
- ผ่านเมื่อ: pill เปลี่ยนเขียว + ประวัติ event ยืนยัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer + ปุ่ม | — | หัวข้อ **CRP-2569-0000005** + pill เหลือง **รอตรวจสอบ** + ปุ่ม **แก้ไข / ตรวจสอบ / ยกเลิก-ลบ** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบ** | — | modal **ตรวจสอบรอบปลูก** — subtitle "เลือกผลการตรวจสอบ · หากปฏิเสธต้องระบุเหตุผล" + เลขรอบปลูก + เกษตรกร + โควตา + แปลง + ปี/เดือน/รวมตัน + radio 2 (ยืนยัน/ปฏิเสธ) | ☐ |
| 3 | CLICK ตัวเลือก **ยืนยัน** | — | ตัวเลือกไฮไลต์เขียว · ปรากฏช่อง **หมายเหตุ (ไม่บังคับ)** (ไม่ต้องกรอก) | ☐ |
| 4 | CLICK ปุ่ม **ยืนยัน** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast เขียว **ยืนยันเรียบร้อย** + pill ใน drawer/ตารางเปลี่ยนเป็นเขียว **ตรวจแล้ว** · การ์ดตรวจแล้ว = 3 | ☐ |
| 6 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ยืนยัน** (จุดเขียว) โดย ธนพล ตรวจสอบ | ☐ |

### TC-V02 — Reject (ปฏิเสธ) ไม่กรอกเหตุผล → block (negative — AC-19 / VR-06 / EC-06)
- group: V · ความสำคัญ: สูงสุด · trace: AC-19 / BR-AGC-06 / ERR_REJECT_NO_REASON / LOCK-07
- Setup: role=ผู้ตรวจสอบ · seed=default (CRP-2569-0000004 waiting) · files=—
- Start: OPEN `#/crops/CRP-2569-0000004` → CLICK **ตรวจสอบ**
- ผ่านเมื่อ: กด ปฏิเสธ + เหตุผลว่าง → block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวเลือก **ปฏิเสธ** | — | ไฮไลต์แดง · ปรากฏช่อง **เหตุผลในการปฏิเสธ** มี * (บังคับ) placeholder "กรุณาระบุเหตุผลในการปฏิเสธ..." | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** โดย **ไม่กรอกเหตุผล** | — | **block** + ข้อความแดงใต้ช่องเหตุผล **กรุณากรอกเหตุผลในการปฏิเสธ** + toast เหลืองข้อความเดียวกัน — ไม่เปลี่ยนสถานะ | ☐ |

### TC-V03 — Reject (ปฏิเสธ) พร้อมเหตุผล (happy — AC-20)
- group: V · ความสำคัญ: สูง · trace: AC-20 / LOCK-02 / legacy TC-571
- Setup: role=ผู้ตรวจสอบ · seed=default (CRP-2569-0000004 waiting) · files=—
- Start: OPEN `#/crops/CRP-2569-0000004` → CLICK **ตรวจสอบ** → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ปริมาณไม่สอดคล้องกับขนาดแปลง ขอตรวจสอบใหม่" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ปฏิเสธเรียบร้อย** (info) + pill แดง **ปฏิเสธ** | ☐ |
| 2 | VERIFY Tab **ภาพรวม** (ท้าย) | — | กล่องแดง **เหตุผลที่ปฏิเสธ: ปริมาณไม่สอดคล้องกับขนาดแปลง ขอตรวจสอบใหม่** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ปฏิเสธ** (จุดแดง) + note เหตุผล โดย ธนพล ตรวจสอบ | ☐ |

### TC-V04 — ไม่เลือกผลตรวจสอบ (negative)
- group: V · ความสำคัญ: กลาง · trace: BR-AGC-06 / "กรุณาเลือกผลการตรวจสอบ"
- Setup: role=ผู้ตรวจสอบ · seed=default (CRP-2569-0000001 waiting) · files=—
- Start: OPEN `#/crops/CRP-2569-0000001` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยัน** ทันที (ยังไม่เลือก radio) | — | ไม่ดำเนินการ + error ใต้ radio **กรุณาเลือกผลการตรวจสอบ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V05 — ปุ่มตรวจสอบซ่อน + checkbox disabled สำหรับ verified/rejected/cancelled (AC-23b)
- group: V · ความสำคัญ: กลาง · trace: AC-23b / BR-AGC-06 / §8 landing actions
- Setup: role=ผู้ตรวจสอบ · seed=default · files=—
- Start: OPEN `#/crops/CRP-2569-0000003` (verified)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบนหัว Landing drawer (CRP-003 ตรวจแล้ว) | — | มี **แก้ไข + ยกเลิก/ลบ** — **ไม่มีปุ่ม ตรวจสอบ** (verified) | ☐ |
| 2 | OPEN `#/crops/CRP-2569-0000007` (rejected) → VERIFY ปุ่ม | — | เช่นเดียวกัน: มี แก้ไข + ยกเลิก/ลบ · ไม่มี ตรวจสอบ | ☐ |
| 3 | กลับ list → VERIFY checkbox แถว CRP-003/006/007/008 | — | checkbox จาง กดไม่ได้ (title "เลือกได้เฉพาะรายการรอตรวจสอบ") — verify ซ้ำผ่าน UI ไม่ได้ · ส่วน 409 server = TC-S02 (simulate) | ☐ |

---

## Group B — Bulk verify / reject (OV-03)

### TC-B01 — Bulk เลือกทั้งหมด = เฉพาะ waiting + ยืนยัน (happy — AC-21 / EC-09)
- group: B · ความสำคัญ: สูง · trace: AC-21 / US-07 / BR-AGC-06/12 / legacy TC-558/573
- Setup: role=ผู้ตรวจสอบ · seed=default (waiting 4) · files=—
- Start: OPEN `#/crops`
- ผ่านเมื่อ: เลือกทั้งหมดติ๊กเฉพาะ waiting + summary

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checkbox รายแถว | — | แถว ตรวจแล้ว/ปฏิเสธ/ยกเลิก (CRP-003/006/007/008) checkbox จาง กดไม่ได้ · แถว รอตรวจสอบ (001/002/004/005) กดได้ | ☐ |
| 2 | CLICK checkbox หัวตาราง | — | ติ๊กเฉพาะ 4 แถว waiting · โผล่ bulk-bar "**เลือก 4 รายการ (รอตรวจสอบ)**" + ปุ่มหัวเปลี่ยนเป็น **ตรวจสอบที่เลือก (4)** (enabled) | ☐ |
| 3 | CLICK **ตรวจสอบที่เลือก (4)** | — | modal **ตรวจสอบรอบปลูก (4 รายการ)** + list "รายการที่เลือก (4 รายการ)" แสดง เลขรอบปลูก + ชื่อ + โควตา · แปลง ครบ 4 + help "ใช้เหตุผลเดียวกันทุกรายการ (เมื่อเลือก \"ปฏิเสธ\") · ข้ามรายการที่ไม่ใช่สถานะรอตรวจสอบ" | ☐ |
| 4 | CLICK **ยืนยัน** (radio) → CLICK ปุ่ม **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** | ☐ |
| 5 | VERIFY ตาราง + stats | — | ไม่มีแถว pill เหลืองเหลือ · การ์ด **รอตรวจสอบ 0** · **ตรวจแล้ว 6** · ปุ่มหัวกลับเป็น (0) disabled | ☐ |

### TC-B02 — Bulk Reject = เหตุผลเดียวทุกรายการ (AC-22 / LOCK-07 / VR-06)
- group: B · ความสำคัญ: สูง · trace: AC-22 / BR-AGC-06 / legacy TC-558
- Setup: role=ผู้ตรวจสอบ · seed=default (waiting 4) · files=—
- Start: OPEN `#/crops` → เลือกทั้งหมด (4 waiting) → CLICK **ตรวจสอบที่เลือก (4)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ปฏิเสธ** โดยไม่กรอกเหตุผล → CLICK **ยืนยัน** | — | block + **กรุณากรอกเหตุผลในการปฏิเสธ** + note "ใช้เหตุผลเดียวกันนี้กับทุกรายการที่เลือก" | ☐ |
| 2 | TYPE "เอกสารประกอบไม่ครบ" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** · ทุกแถวที่เลือก pill แดง **ปฏิเสธ** | ☐ |
| 3 | OPEN รอบปลูกหนึ่งใน 4 → Tab ภาพรวม | — | กล่อง **เหตุผลที่ปฏิเสธ: เอกสารประกอบไม่ครบ** (เหตุผลเดียวกันทุกใบ) | ☐ |

### TC-B03 — Bulk skip non-waiting / partial (edge — AC-22 / EC-09) (ต้อง simulate)
- group: B · ความสำคัญ: สูง · trace: AC-22 / EC-09 · **prototype: openVerifyModal กรอง ids ให้เหลือเฉพาะ waiting ก่อนเปิด modal — จึง สำเร็จ=ทั้งหมด; per-record conflict (คนที่สอง verify ก่อน submit) = SIT**
- Setup: role=ผู้ตรวจสอบ · seed=default
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) เลือก waiting ทั้งหมด → ยืนยัน → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ N ล้มเหลว 0** (ทุกใบ waiting จริง — non-waiting ถูกกรองออกก่อนเปิด modal) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): บางใบถูก verify โดยผู้อื่นก่อน submit | — | summary "สำเร็จ X ล้มเหลว Y" — ใบที่ status เปลี่ยนแล้วถูกนับ ล้มเหลว (per-record 409 ERR_STATUS_CONFLICT) | ☐ |

---
## Group E — แก้ไข + State machine (OV-02 — LOCK-05/06)

### TC-E01 — แก้ไขรอบปลูก waiting → status คงเดิม + version++ (happy — AC-11)
- group: E · ความสำคัญ: สูง · trace: AC-11 / US-08 / BR-AGC-11 / legacy TC-554
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000001 waiting, เวอร์ชัน 1) · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว CRP-2569-0000001 | — | drawer **แก้ไข CRP-2569-0000001** · sub "สถานะ: รอตรวจสอบ · เวอร์ชัน 1" · note info **โควตา QT-2569-001 · แปลง PLT-2569-001 — แก้ไม่ได้** + note warn **ถ้ารอบปลูกนี้ตรวจแล้ว บันทึกการแก้ไขจะกลับสู่สถานะรอตรวจสอบ** · ฟิลด์มีค่าเดิม (ไม่ล็อก) | ☐ |
| 2 | TYPE แก้ช่อง **ปริมาณรวม (ตัน)** เป็น "130" | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + แถว CRP-001 ยัง pill เหลือง **รอตรวจสอบ** (status คงเดิม) + รวมตันในตาราง = 130.00 | ☐ |
| 4 | OPEN `#/crops/CRP-2569-0000001` → Tab **ประวัติ** | — | มี event **แก้ไขข้อมูล** เพิ่มบนสุด · footer "เวอร์ชัน 2" | ☐ |

### TC-E02 — แก้ไข Verified → **กลับ waiting_for_verify** (AC-11b / EC-07 / LOCK-05) ★★
- group: E · ความสำคัญ: สูงสุด · trace: AC-11b / EC-07 / BR-AGC-04 / legacy TC-554 · **KEY behavior — ตรงข้ามกับ Plot (F-AGM-003) ที่ status คงเดิม**
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000006 verified) · files=—
- Start: OPEN `#/crops/CRP-2569-0000006`
- ผ่านเมื่อ: แก้แล้วบันทึก → สถานะ **กลับ รอตรวจสอบ** (ไม่คงเป็น ตรวจแล้ว)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **แก้ไข** (verified มีปุ่มแก้ไข) | — | drawer แก้ไข · sub "สถานะ: ตรวจแล้ว · เวอร์ชัน 2" · note warn "ถ้ารอบปลูกนี้ตรวจแล้ว บันทึกการแก้ไขจะกลับสู่สถานะรอตรวจสอบ" | ☐ |
| 2 | TYPE แก้ช่อง **ปริมาณรวม (ตัน)** เป็น "320" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **สีเหลือง (warning) บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ** | ☐ |
| 3 | VERIFY แถว CRP-2569-0000006 ในตาราง | — | pill **เปลี่ยนเป็นเหลือง รอตรวจสอบ** (ไม่คงเป็น ตรวจแล้ว) · การ์ดรอตรวจสอบ 4→5 · ตรวจแล้ว 2→1 | ☐ |
| 4 | CLICK แถว → Tab **ประวัติ** | — | event บนสุด **แก้ไขข้อมูล** + note "แก้ไขหลังตรวจแล้ว — กลับสู่สถานะรอตรวจสอบ" · verified_by ถูกล้าง | ☐ |

### TC-E03 — แก้ไข Rejected → ยังคง ปฏิเสธ + reject_reason คงอยู่
- group: E · ความสำคัญ: สูง · trace: AC-11 / BR-AGC-04 (rejected ≠ verified — ไม่ reset) / §5.2
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000007 rejected, reason "ปริมาณรวมไม่สอดคล้องกับขนาดแปลง กรุณาตรวจสอบและแก้ไข") · files=—
- Start: OPEN `#/crops/CRP-2569-0000007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Tab ภาพรวม | — | pill แดง **ปฏิเสธ** + กล่อง **เหตุผลที่ปฏิเสธ: ปริมาณรวมไม่สอดคล้องกับขนาดแปลง กรุณาตรวจสอบและแก้ไข** | ☐ |
| 2 | CLICK **แก้ไข** → TYPE แก้ **ปริมาณรวม** เป็น "85" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** (ไม่ใช่ "กลับสู่สถานะรอตรวจสอบ" — reset เฉพาะ verified) · pill ยังแดง **ปฏิเสธ** | ☐ |
| 3 | OPEN `#/crops/CRP-2569-0000007` → Tab ภาพรวม | — | กล่อง **เหตุผลที่ปฏิเสธ** ยังคงอยู่ (reject_reason ไม่ถูกเคลียร์ตอน edit) | ☐ |

### TC-E04 — quota/plot read-only บนหน้า edit (AC-13 / EC-08 / LOCK-06)
- group: E · ความสำคัญ: สูง · trace: AC-13 / EC-08 / BR-AGC-05 / legacy TC-555
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000003) · files=—
- Start: OPEN `#/crops` → CLICK ดินสอแถว CRP-2569-0000003

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Section 0 ของ drawer แก้ไข | — | **ไม่มี** ช่องค้นหาโควตา/เลือกแปลง (ไม่มี double-binding UI) · แสดงเฉพาะ note info **โควตา QT-2569-002 · แปลง PLT-2569-003 — แก้ไม่ได้** (read-only banner) | ☐ |
| 2 | VERIFY ฟิลด์ที่แก้ได้ | — | แก้ได้เฉพาะ ปีผลิต/เดือน/ปริมาณรวม/lat/long/postal/รูปภาพ — quota_id/plot_id ไม่มี input ให้แก้ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): ยิง PUT เปลี่ยน quota_id/plot_id | — | server reject (immutable — BR-AGC-05) แม้ UI ไม่มีช่อง | ☐ |

### TC-E05 — แก้ไขแล้วปีนอกช่วง → block (negative — AC-04 บน edit)
- group: E · ความสำคัญ: กลาง · trace: VR-03 / EC-03 (validate ทำงานบน edit ด้วย)
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000001) · files=—
- Start: OPEN `#/crops` → CLICK ดินสอแถว CRP-2569-0000001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE แก้ **ปีผลิต (พ.ศ.)** เป็น "3000" → CLICK **บันทึกการแก้ไข** | — | ไม่บันทึก + ข้อความแดง **ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | แก้กลับเป็น "2569" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** | ☐ |

---

## Group D — ยกเลิก / ลบ (soft — OV-04 — LOCK-11)

### TC-D01 — ยกเลิก (cancelled) + reason บังคับ (happy — AC-27 / EC-18)
- group: D · ความสำคัญ: สูง · trace: AC-27 / BR-AGC-09 / VR-09 / US-09 / legacy TC-569
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000004 waiting) · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า การ์ด **รอบปลูกทั้งหมด** และ **รอตรวจสอบ** | — | บันทึก: ทั้งหมด=8, รอตรวจสอบ=4 (อ้างใน step 6) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว CRP-2569-0000004 | — | modal **ยกเลิก/ลบรอบปลูก?** + subtitle `รอบปลูก "CRP-2569-0000004 — ทองดี พูลผล"` + radio **ยกเลิก (cancelled) — ยังคงอยู่ในรายการ** (default) / **ลบ (deleted) — ซ่อนจากรายการ** + ช่อง **เหตุผล *** + note info "รายการจะเปลี่ยนเป็นสถานะ \"ยกเลิก\" และยังคงแสดงในรายการ" | ☐ |
| 3 | คง radio **ยกเลิก** → CLICK **ยกเลิกรอบปลูก** โดยไม่กรอกเหตุผล | — | **block** + ข้อความแดง **กรุณากรอกเหตุผล** + toast เดียวกัน | ☐ |
| 4 | TYPE "เกษตรกรขอยกเลิก" → เหตุผล → CLICK **ยกเลิกรอบปลูก** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast **ยกเลิกรอบปลูกแล้ว** + แถว CRP-004 **ยังอยู่ในตาราง** pill เทา **ยกเลิก** (soft — คงในรายการ) | ☐ |
| 6 | VERIFY stats | — | ทั้งหมด=8 (cancelled ยังนับใน list · all.length นับ status≠deleted) · รอตรวจสอบ=3 | ☐ |

### TC-D02 — ลบ (deleted) → soft delete ซ่อนจาก list + deep-link (AC-28 / EC-17)
- group: D · ความสำคัญ: สูง · trace: AC-28 / BR-AGC-09 / EC-17 / ERR_NOT_FOUND / legacy TC-569
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000005 waiting) · files=—
- Start: OPEN `#/crops` → CLICK ถังขยะ แถว CRP-2569-0000005

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK radio **ลบ (deleted)** | — | note เปลี่ยนเป็นแดง **รายการจะถูกซ่อนจากรายการ (soft delete) และบันทึกลงประวัติ** · ปุ่มเปลี่ยนเป็น **ลบรอบปลูก** | ☐ |
| 2 | TYPE "ข้อมูลผิด สร้างซ้ำ" → เหตุผล → CLICK **ลบรอบปลูก** → WAIT | — | toast **ลบรอบปลูกแล้ว** + แถว CRP-005 **หายจากตาราง** · count = 7 รายการ | ☐ |
| 3 | OPEN `#/crops/CRP-2569-0000005` (route ตรง) | — | ไม่เปิด detail — toast **ไม่พบข้อมูลรอบปลูกที่เลือก** + เด้งกลับ `#/crops` (deleted ถูกซ่อน) | ☐ |

### TC-D03 — ยกเลิก/ลบ จาก Landing drawer (ทุกสถานะ) (AC-28)
- group: D · ความสำคัญ: กลาง · trace: AC-28 / BR-AGC-09 · **หมายเหตุ: ในตาราง ถังขยะเฉพาะแถว waiting; ปุ่ม ยกเลิก/ลบ อยู่ใน Landing drawer สำหรับทุกสถานะ**
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000003 verified) · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **การดำเนินการ** แถว CRP-2569-0000003 (ตรวจแล้ว) ในตาราง | — | มีเฉพาะไอคอนดินสอ — **ไม่มีถังขยะ** (list ลบเฉพาะ waiting) | ☐ |
| 2 | CLICK แถว CRP-2569-0000003 → VERIFY ปุ่มหัว Landing drawer | — | มี **แก้ไข + ยกเลิก/ลบ** (drawer อนุญาตทุกสถานะ) | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก/ลบ** → radio **ลบ** → TYPE เหตุผล → CLICK **ลบรอบปลูก** → WAIT | — | toast **ลบรอบปลูกแล้ว** + drawer ปิด + แถว CRP-003 หาย · การ์ดตรวจแล้ว = 1 | ☐ |

### TC-D04 — cancelled คงในรายการ + refresh reset (AC-27)
- group: D · ความสำคัญ: กลาง · trace: AC-27 / §8 (cancelled soft) / mock reset
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000008 cancelled ใน seed) · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT filter สถานะ = **ยกเลิก** | — | เหลือ 1 แถว CRP-2569-0000008 pill เทา **ยกเลิก** — ยืนยัน cancelled คงแสดงในรายการ (ต่าง deleted ที่ซ่อน) | ☐ |
| 2 | CLICK แถว → Tab ภาพรวม | — | กล่อง **เหตุผลที่ยกเลิก: เกษตรกรขอยกเลิกรอบปลูกนี้** | ☐ |
| 3 | PRESS F5 (refresh) | — | mock reset → seed กลับมา 8 รอบปลูก (in-memory) — ยืนยัน refresh = reset (ทุกเคส independent) | ☐ |

---

## Group W — Landing / 5 tabs / ETCD / Survey / ประวัติ (P-02)

### TC-W01 — Landing ภาพรวม + snapshot card + negative warn (AC-24 / AC-29 / AC-20)
- group: W · ความสำคัญ: สูง · trace: AC-24, AC-29 / US-04 / BR-AGC-02/07 / LOCK-04/08
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000002 → remaining −20) · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว CRP-2569-0000002 | — | Landing drawer: eyebrow "รอบปลูก · QT-2569-001 · PLT-2569-002" + หัวข้อ **CRP-2569-0000002** (mono) + pill เหลือง **รอตรวจสอบ** | ☐ |
| 2 | VERIFY snapshot card (ใต้หัว) | — | การ์ดส้มอ่อน "โควตา · แปลง · เกษตรกร" → **โควตา QT-2569-001 · แปลง PLT-2569-002 · สมหญิง รักดี** + ปุ่ม **ดูโควตา** + **ดูแปลง** | ☐ |
| 3 | VERIFY Tab **ภาพรวม** | — | กลุ่ม **การผูกโควตา · แปลง · เกษตรกร** (เลขโควตา/เลขแปลง/เกษตรกร/โทรศัพท์/ที่อยู่แปลง snapshot/ขนาดแปลง 8.75 ไร่) · กลุ่ม **ข้อมูลรอบปลูก** (ปีผลิต 2569/เดือน 2 · ก.พ./ปริมาณรวม 90.00/จองแล้ว (ETCD) 110.00/**คงเหลือ badge แดง −20.00**) | ☐ |
| 4 | VERIFY กล่องเตือน (ท้าย ภาพรวม) | — | กล่องแดง **คงเหลือติดลบ: ปริมาณจอง (ETCD) มากกว่าปริมาณรวมของรอบปลูกนี้** | ☐ |
| 5 | VERIFY footer drawer | — | "อัปเดตล่าสุด … · เวอร์ชัน N" + ปุ่ม **ปิด** | ☐ |

### TC-W02 — Tab รูปภาพ + snapshot links ดูโควตา/ดูแปลง (AC-08 / AC-24)
- group: W · ความสำคัญ: กลาง · trace: AC-08, AC-24 / cross-module read-only (mock toast) / legacy TC-580
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000001 photos 2) · files=—
- Start: OPEN `#/crops/CRP-2569-0000001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **รูปภาพ** | — | การ์ด 2 ไฟล์: **crop_001_a.jpg**, **crop_001_b.jpg** + link **ดาวน์โหลด** ต่อไฟล์ | ☐ |
| 2 | CLICK link ดาวน์โหลดไฟล์แรก | — | toast info **จำลองดาวน์โหลด crop_001_a.jpg** | ☐ |
| 3 | CLICK ปุ่ม **ดูโควตา** (snapshot card) | — | toast info **จำลองเปิดหน้าโควตา QT-2569-001** (READ-ONLY — deep-link จริงตอน deploy รวม features) | ☐ |
| 4 | CLICK ปุ่ม **ดูแปลง** | — | toast info **จำลองเปิดหน้าแปลง PLT-2569-001** (READ-ONLY) | ☐ |

### TC-W03 — Tab การจอง (ETCD): bookings + total_booked + remaining ⭐ (AC-25 / XT-04)
- group: W · ความสำคัญ: สูง · trace: AC-25 / BR-AGC-07/08 / LOCK-08 / legacy TC-564
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000001: total 120, ΣETCD 80, remaining 40) · files=—
- Start: OPEN `#/crops/CRP-2569-0000001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **การจอง (ETCD)** | — | หัวข้อ **การจอง (ETCD) · อ่านอย่างเดียว** + note info **ข้อมูลจากระบบ ETCD ภายนอก — แสดงเพื่ออ้างอิงเท่านั้น แก้ไขไม่ได้** | ☐ |
| 2 | VERIFY ตารางการจอง | — | 2 แถว (วันที่จอง / ปริมาณ (ตัน)) รวม 50.00 + 30.00 | ☐ |
| 3 | VERIFY สรุปตัวเลข | — | **รวมจองแล้ว (total_booked_tons) 80.00** · **ปริมาณรวม (ตัน) 120.00** · **คงเหลือ (ยังไม่จอง)** badge เทา **40.00** (ไม่มี warn — บวก) | ☐ |
| 4 | OPEN `#/crops/CRP-2569-0000002` → Tab **การจอง (ETCD)** | — | รวมจองแล้ว 110.00 · คงเหลือ badge **แดง −20.00** + กล่องเตือน **ปริมาณจองเกินปริมาณรวม (คงเหลือติดลบ)** | ☐ |

### TC-W04 — Tab สำรวจ + ประวัติ (audit timeline) (AC-25 / AC-26 / BR-AGC-12)
- group: W · ความสำคัญ: สูง · trace: AC-25, AC-26 / BR-AGC-08/09/12 / audit append-only / legacy TC-565/586
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000007 rejected — create+reject · CRP-001 มี survey) · files=—
- Start: OPEN `#/crops/CRP-2569-0000001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **สำรวจ** | — | หัวข้อ **สำรวจ (Survey) · อ่านอย่างเดียว** + note info "ข้อมูลจากระบบสำรวจภายนอก · ซิงก์ล่าสุด [date]" + การ์ด **ทีมสำรวจ A** + note "ต้นอ้อยสมบูรณ์" | ☐ |
| 2 | OPEN `#/crops/CRP-2569-0000007` → CLICK Tab **ประวัติ** | — | timeline เรียงใหม่→เก่า: **ตรวจสอบ — ปฏิเสธ** (จุดแดง + note "ปริมาณรวมไม่สอดคล้องกับขนาดแปลง กรุณาตรวจสอบและแก้ไข" + โดย ธนพล ตรวจสอบ) → **สร้างรอบปลูก** (โดย สมพร วงศ์ทะเบียน + note "ผูกโควตา QT-2569-003 · แปลง PLT-2569-005 · ทองดี พูลผล") — ทุกรายการมีวันเวลา | ☐ |
| 3 | VERIFY (empty survey) OPEN `#/crops/CRP-2569-0000002` → Tab **สำรวจ** | — | "ยังไม่มีข้อมูลสำรวจ" (CRP-002 ไม่มี survey) | ☐ |

### TC-W05 — Deep-link refresh-safe + missing (AC-26b / EC-17)
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / refresh-safe / ERR_NOT_FOUND / legacy TC-583
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops/CRP-2569-0000003` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/crops/CRP-2569-0000003` | — | หน้า list โหลด + Landing drawer **CRP-2569-0000003** เปิดเองทันที | ☐ |
| 2 | PRESS F5 (refresh ทั้งหน้า) | — | กลับมาที่เดิม — drawer CRP-2569-0000003 ยังเปิด (refresh-safe · mountViewDrawer จาก route) | ☐ |
| 3 | OPEN `#/crops/CRP-2569-9999999` (ไม่มีในระบบ) | — | toast แดง **ไม่พบข้อมูลรอบปลูกที่เลือก** + เด้งกลับ `#/crops` (ไม่มี drawer) | ☐ |

---
## Group X — Cross-module DOUBLE read-only ⭐⭐ (06_TESTS §6.9 — Quota + Plot + ETCD/Survey)

> Crop อ่าน Quota ผ่าน `QUOTAS`/`verifiedQuotas`/`findQuotaById` **และ** Plot ผ่าน `PLOTS`/`plotsForQuota`/`findPlotById` — **ไม่มี write-back** · อ่าน ETCD/Survey (external, fail-soft) · พิสูจน์บนจอผ่าน (ก) verified quota เท่านั้น (QT-005 waiting ถูกตัด) (ข) plot ของเจ้าของ+verified เท่านั้น (PLT-004 waiting ถูกตัด) (ค) `QUOTAS`/`PLOTS` array ไม่ถูก mutate · reconcile ไป Quota/Plot/ETCD/Survey feature จริง = `(ต้อง simulate)` ที่ SIT

### TC-X01 — Quota search คืนเฉพาะ verified · ไม่ verified ถูกตัด (XT-02)
- group: X · ความสำคัญ: สูงสุด · trace: XT-02 / AC-01 / VR-01 / BR-AGC-01 / LOCK-03
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ค้นหาโควตา → พิมพ์ "QT-2569" | — | dropdown แสดง **4 โควตา** (QT-2569-001..004 — verified ทุกตัว) · option = `[QT] · [ชื่อ]` + sub `[เบอร์] · [เลขบัตร masked]` · **ไม่มี QT-2569-005** (waiting_for_verify — verifiedQuotas ตัดออก) | ☐ |
| 2 | CLICK **QT-2569-004 · ประนอม ใจเพชร** | — | การ์ดเจ้าของโควตา: QT-2569-004 · ประนอม ใจเพชร · 0833334444 · เลขบัตร 4-XXXX-XXXX-XX-3 (masked, read-only) | ☐ |
| 3 | VERIFY การ์ดเจ้าของโควตา | — | ข้อมูลเกษตรกร **แก้ไม่ได้** (แสดงอย่างเดียว) — ปุ่ม **เปลี่ยนโควตา** เท่านั้น | ☐ |

### TC-X02 — สร้าง crop ผูก quota+plot → snapshot ตรง · quota/plot ไม่ถูกแก้ (XT-01) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-03 / BR-AGC-02 / §0.14 no write-back
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-004 · ประนอม ใจเพชร** + **PLT-2569-006** → กรอก ปี 2569 · เดือน 5 · ตัน 100 → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]** · แถวใหม่ แสดง QT-2569-004, PLT-2569-006, ประนอม ใจเพชร (snapshot จาก quota+plot) | ☐ |
| 2 | CLICK แถวใหม่ → VERIFY Tab ภาพรวม | — | ที่อยู่แปลง = 5 หมู่ 5 · ท่าผา บ้านโป่ง ราชบุรี 70110 · ขนาดแปลง 6.00 ไร่ (snapshot จาก PLT-2569-006) · โทรศัพท์ 0833334444 (จาก quota) — ตรงต้นทาง | ☐ |
| 3 | พิสูจน์ READ-ONLY: CLICK **สร้างรอบปลูก** อีกครั้ง → เลือก **QT-2569-004** → เลือกแปลง | — | ยังเลือก **PLT-2569-006 ได้ตามปกติ** (ไม่ขึ้น "แปลงถูกใช้แล้ว" — Plot ไม่ถูก mutate) · quota ยังเลือกได้ (ไม่มี has_crop flag) | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | เปิด Quota `#/quotas/QT-2569-004` + Plot `#/plots/PLT-2569-006` → **ไม่มี field/สถานะที่เปลี่ยน** จากการผูกรอบปลูก (read-only ENG-EXT-QP GET only) | ☐ |

### TC-X03 — Plot list = owner + verified เท่านั้น (XT-03) ★ signature
- group: X · ความสำคัญ: สูงสุด · trace: XT-03 / AC-02c / VR-02 / BR-AGC-01 / LOCK-03
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops` → CLICK **สร้างรอบปลูก**
- ผ่านเมื่อ: plot list กรอง owner + verified (PLT-004 waiting ถูกตัด · owner อื่นไม่ขึ้น)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-002 · สุรพล เก่งการไร่** → CLICK เลือกแปลง | — | dropdown = **PLT-2569-003 เท่านั้น (1 แปลง)** · **ไม่มี PLT-2569-004** (owner เดียวกันแต่ verify_status=waiting → ตัดออก) · help "(1 แปลง)" | ☐ |
| 2 | VERIFY: ไม่มีแปลงของโควตาอื่น | — | dropdown ไม่แสดง PLT-2569-001/005/006/007 (owner mismatch — plotsForQuota กรอง quota_id) | ☐ |
| 3 | CLICK ปุ่ม **เปลี่ยนโควตา** → เลือก **QT-2569-001** → เลือกแปลง | — | dropdown = **PLT-2569-001, PLT-2569-002 (2 แปลง)** — พิสูจน์ 1 quota : N verified plots | ☐ |

### TC-X04 — ETCD compute remaining ติดลบ → badge (XT-04 / AC-29 / LOCK-08)
- group: X · ความสำคัญ: สูง · trace: XT-04 / BR-AGC-07 / EC-10
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default (CRP-2569-0000004: total 60, ΣETCD 75) · files=—
- Start: OPEN `#/crops/CRP-2569-0000004`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **การจอง (ETCD)** | — | ตาราง 2 การจอง (45.00 + 30.00) · รวมจองแล้ว **75.00** · ปริมาณรวม **60.00** · คงเหลือ badge **แดง −15.00** (60 − 75) | ☐ |
| 2 | VERIFY กล่องเตือน | — | **ปริมาณจองเกินปริมาณรวม (คงเหลือติดลบ)** | ☐ |
| 3 | VERIFY Tab **ภาพรวม** คงเหลือ | — | badge แดง −15.00 (compute เดียวกันทั้ง 2 tab) — remaining อ่านจาก ETCD (read-only) ไม่ block การ verify (OQ-C5) | ☐ |

### TC-X05 — Assert ไม่มี write-back ไป Quota/Plot (READ-ONLY invariant)
- group: X · ความสำคัญ: สูง · trace: §0.14 / XT-01 / D-02 Drift
- Setup: role=เจ้าหน้าที่รอบปลูก · seed=default · files=—
- Start: OPEN `#/crops`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างรอบปลูกผูก QT-2569-001 + PLT-2569-002 (ตามชุด A) → WAIT toast | — | สร้างสำเร็จ · **ไม่มี toast/history event ประเภท "อัปเดตสถานะโควตา/แปลง"** (Crop อ่านอย่างเดียว) | ☐ |
| 2 | CLICK รอบปลูกใหม่ → Tab **ประวัติ** | — | มีเฉพาะ event **สร้างรอบปลูก** — ไม่มี cross-module write event | ☐ |
| 3 | VERIFY (ระบบจริง — SIT) | — | ตรวจ Quota + Plot record ก่อน/หลังผูก = **ไม่เปลี่ยน** (ENG-EXT-QP GET only, ไม่มี PATCH) | ☐ |

### TC-X06 — ETCD/Survey down → fail-soft (XT-05 / AC-25b / EC-11) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-05 / AC-25b / EC-11 / BR-AGC-08 / D-03 · **prototype: seed etcd_fail/survey_fail=false เสมอ — ไม่มี UI toggle · code path fail-soft มี (branch c.etcd_fail / c.survey_fail) → SIT case**
- Setup: role=เจ้าหน้าที่รอบปลูก · **simulate — ระบบจริง:** ETCD/Survey external ไม่พร้อม
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): เปิด Landing → Tab การจอง (ETCD) เมื่อ external down | — | note warn **ดึงข้อมูลการจองไม่สำเร็จ (ระบบภายนอกไม่พร้อมใช้งาน) — แสดงเฉพาะข้อมูลที่มี** · **landing ยังเปิดได้** (ไม่ crash) · tab อื่นทำงานปกติ | ☐ |
| 2 | VERIFY (ระบบจริง): Tab สำรวจ เมื่อ external down | — | note warn **ดึงข้อมูลสำรวจไม่สำเร็จ (ระบบภายนอกไม่พร้อมใช้งาน)** — fail-soft, crop mutation (สร้าง/แก้/verify) ยังทำงาน | ☐ |

---

## Group S — System / simulate (optimistic lock · concurrency · SoD · deep-link)

### TC-S01 — Optimistic lock stale edit → 409 (edge — AC-12 / EC-12) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-12 / EC-12 / ERR_STALE / BR-AGC-11 / legacy TC-556 · **prototype single-session ทำไม่ได้ (Drift D-04) — SIT case · idempotency double-click ตรวจแล้วใน TC-C12**
- Setup: **simulate — ระบบจริง:** 2 sessions — A แก้ record + save ก่อน, B ที่เปิดค้างไว้ save ทีหลังด้วย expected_version เก่า
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B กด **บันทึกการแก้ไข** หลัง A save ไปแล้ว | — | 409 + toast แดง **ข้อมูลล้าสมัย กรุณารีเฟรช** — ข้อมูลของ A ไม่ถูกทับ | ☐ |

### TC-S02 — Concurrent verify status changed → 409 (edge — AC-23b / EC-13) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-23b / EC-13 / ERR_STATUS_CONFLICT / legacy TC-572 · **prototype UI ซ่อนปุ่มตรวจสอบสำหรับ verified/rejected (TC-V05) — ส่วน 409 server = SIT**
- Setup: **simulate — ระบบจริง:** A verify record ก่อน, B verify record เดิม (status เปลี่ยนแล้ว)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B POST verify กับ record ที่ A เพิ่ง verify | — | 409 + **สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช** — สถานะที่ A ตั้งไว้คงเดิม | ☐ |

### TC-S03 — crop_id sequence race + server-side validation + orphan photo (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: BR-AGC-11 / legacy TC-551/575/577/578 · **crop_id format CRP-2569-000000N · nextCropCode ฝั่ง client (prototype); atomic sequence + race = server**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): 2 request สร้างรอบปลูกพร้อมกัน (race) | — | server atomic sequence → crop_id ไม่ชนกัน (CRP-2569-000000N unique) · idempotency-key กัน duplicate | ☐ |
| 2 | VERIFY (ระบบจริง): UI ผ่าน แต่ payload year/tons ผิด (bypass) | — | server reject validation (ปี 2500-2600 / tons ≥ 0) แม้ UI ปล่อยผ่าน · CSV partial → orphan photo cleanup (TC-578) | ☐ |

### TC-S04 — SoD + RBAC hide (OQ-C4) (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: §5.3 SoD/permission matrix · **prototype ไม่มี role switching — เจ้าหน้าที่/ผู้ตรวจสอบเป็น user เดียว — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง:** feature flag SoD + RBAC
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — RBAC): login เป็น เจ้าหน้าที่รอบปลูก | — | ปุ่ม **ตรวจสอบ / ตรวจสอบที่เลือก** ถูกซ่อน (verify = ผู้ตรวจสอบเท่านั้น) | ☐ |
| 2 | VERIFY (ระบบจริง — SoD flag ON): ผู้ตรวจสอบ verify รอบปลูกที่ตนเองสร้าง | — | block 403 + ข้อความ SoD (ผู้สร้างไม่ควรตรวจสอบเอง) · flag OFF → ผ่านแต่ log anomaly | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `crop-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed 8 รอบปลูก + 5 โควตา + 8 แปลง (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/UPLOAD/PRESS/WAIT/VERIFY)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast มุมขวาล่าง · create/edit 0.6s · verify 0.7s · cancel/delete 0.55s · import 0.9s — อ่านทันทีที่โผล่ · toast แสดง 4–4.8s)
5. **double-binding บังคับ:** ทุกเคสสร้าง/negative ที่ต้องกรอกฟิลด์รอบปลูก ต้อง **เลือกทั้งโควตา (verified) และแปลง (owner+verified) ก่อน** (ฟิลด์ล็อกจนครบทั้งคู่) — ยกเว้นเคสที่ทดสอบ gating เอง (TC-C02/C03/C04/C05)
6. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
7. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"
8. ไฟล์ทดสอบทั้งหมด (CSV/xlsx) ต้องอยู่ในโฟลเดอร์ที่ agent เข้าถึงได้ก่อนเริ่ม (ดู Data Sets → Files) · header CSV = 5 คอลัมน์ `quota_id,plot_id,year_be,planted_month,total_tons`
9. จบทุกเคส → กรอก Result Report ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 34 / 34 (AC-01..29 + AC-02b/02c/11b/23b/25b/26b) |
| Cross-Module (XT-01..05) | 5 / 5 (XT-05 simulate) + X05 read-only assertion |
| Business rules (BR-AGC-01..12) | 12 / 12 |
| Validation (VR-01..09) | 9 / 9 (VR-08 photo policy simulate) |
| Edge cases (EC-01..18) | 18 / 18 (EC-09/11/12/13 simulate/SIT) |
| Error codes (UI-observable) | 14 / 14 (ERR_STALE / ERR_STATUS_CONFLICT / ERR_ETCD = simulate) |
| Permission cells | เจ้าหน้าที่ / ผู้ตรวจสอบ allow ครบ · RBAC deny / SoD = TC-S04 (simulate) |
| Scope Lock (LOCK-01..13) | 13 / 13 — ทุก LOCK มีเคส verify |
| Legacy TC-547..586 (40 เคส) | mapped 100% (server-only/pending-spec → simulate group S) |

- **Manifest cross-check (FRD §0.12): ✅ 10 Stories + 12 Rules + 9 VR + 18 EC + 5 XT + 13 LOCK — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT (7 เคส)
- TC-L07 (export CSV — ไม่มี UI ใน prototype)
- TC-B03 (bulk skip non-waiting per-record conflict)
- TC-X06 (ETCD/Survey fail-soft — seed etcd_fail=false เสมอ, ไม่มี toggle)
- TC-S01 (optimistic lock 409 — single session)
- TC-S02 (concurrent verify 409)
- TC-S03 (crop_id sequence race + server validation + orphan photo)
- TC-S04 (SoD / RBAC — ไม่มี role switching)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-004",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 58, "pass": 0, "fail": 0, "blocked": 0 }
}
```

---

## v1.1 Recheck Additions (F-AGM-004 · crosscheck กับ FRD/Stage-10/Testcase/AS-BUILT ใหม่)

เพิ่ม 7 เคส หลัง crosscheck พบว่า prototype เดิมขาดฟิลด์ที่สเปคผู้มีอำนาจ (FRD §2 create-form + AS-BUILT create-crop-drawer) กำหนดไว้ — ได้แก้ prototype ให้ครบแล้ว:

| เคส | กลุ่ม | สิ่งที่ทดสอบ | anchor สำคัญ |
|---|---|---|---|
| TC-C13 | สร้าง | ฟอร์มสร้างมี สายพันธุ์ (ขอนแก่น 3/LK 92-11/UT 8) · ประเภทอ้อย (อ้อยใหม่/อ้อยตอ) · รหัสแปลง · อายุอ้อยคำนวณอัตโนมัติ | create_drawer / create_details |
| TC-C14 | สร้าง | เลือกพบโรค/ศัตรูพืช + กรอกรายละเอียด | create_details |
| TC-C15 | สร้าง | อายุอ้อย = 0 เมื่อปี+เดือนปลูก = ปัจจุบัน (สูตร FN-AT-CROP-192: พ.ศ.−543 แล้วนับเดือน floor ≥0) | create_details |
| TC-E05 | แก้ไข | แก้สายพันธุ์/ประเภทอ้อยแล้วบันทึก (โควตา/แปลงยังแก้ไม่ได้) | edit_drawer |
| TC-W06 | Landing | แท็บภาพรวมแสดง สายพันธุ์/ประเภท/อายุอ้อย/สถานะโรค แบบอ่านอย่างเดียว | view_drawer |
| TC-L09 | รายการ | ปุ่ม Export CSV ส่งออกตามตัวกรอง (ฝั่งหน้าจอ · backend Pending Spec ตาม TC-581) | list_actions |
| TC-I07 | CSV | แม่แบบ CSV 8 คอลัมน์: quota_id, plot_id, production_year_be, plot_code, variety, cane_type, planted_month, total_tons + ตรวจ header | import_modal |

หมายเหตุ reconciliation:
- prototype คง latitude+longitude เป็น 2 ช่อง (ละเอียดกว่า) แทน geo_coordinate เดี่ยว — เทียบเท่ากันเชิงสัญญา API (map → geo_coordinate)
- CSV คง plot_id ไว้เพื่อผูกแปลง (AS-BUILT expectedHeaders 9 ช่องละ plot_id เป็น mock simplification) · เปลี่ยนชื่อ year_be → production_year_be ตามสเปคใหม่
- Export backend = Pending Spec (TC-581) — prototype ทำ client-side export ไว้ก่อน
