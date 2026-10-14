# AI Test Cases — F-AGM-006 Survey Management (จัดการแบบสำรวจ)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `survey-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ HTML + UI Brief §9 แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side / optimistic lock / concurrency / role·SoD / Crop external feed จริง) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-006 (AGM/Survey — WKN) |
| App entry | เปิดไฟล์ `survey-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/surveys` (list — default) · `#/surveys/:survey_id` (detail drawer, refresh-safe) |
| ที่มา | FRD_F-AGM-006_Pack (7 ไฟล์ STANDARD) · BRD APPROVED (LOCK-01..11) · HTML v1.0 (audit FAIL=0) · UI_BRIEF_F-AGM-006 |
| จำนวนเคส | 62 เคส / 10 groups |
| Scope Lock | LOCK-01..11 (00_OVERVIEW §0.11 ← BRD §3.4) — ทุกข้อมีเคส verify (ดู Ledger) |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า = ข้อมูล reset กลับ seed 8 แบบสำรวจ + 4 โควตา + 7 แปลง + 7 รอบปลูก — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh (F5) ก่อนเริ่ม |
| Cascade ⭐⭐⭐ | **TRIPLE 3-level cascade (signature)** — ฟิลด์แบบสำรวจ **ล็อกทั้งหมด** จนกว่าจะเลือกครบ **โควตา (verified) → แปลง (ของโควตา + verified) → รอบปลูก (ของแปลง)** · แต่ละชั้นเปิดหลังชั้นบน · quota→farmer snapshot · READ-ONLY (`QUOTAS`/`PLOTS`/`CROPS` + `verifiedQuotas`/`plotsForQuota`/`cropsForPlot`) · **ไม่มี write-back** |
| Cross-module ⭐ | survey **verified** ป้อนเข้า Crop (F-AGM-004) แท็บ **สำรวจ** (pull-read) · **1 รอบปลูก : N แบบสำรวจ** (SV-0000001 & SV-0000002 ทั้งคู่บน CRP-2569-0000001) · reconcile ไป Crop feature จริง = `(ต้อง simulate)` ที่ SIT |

**Seed ตั้งต้น (หลัง refresh — 8 แบบสำรวจ SV-2569-0000001..0008):**
| เลขสำรวจ | รอบปลูก | โควตา · แปลง | เกษตรกร | ผู้สำรวจ | พันธุ์อ้อย | ผลผลิต(ตัน) | ขนาด(ไร่) | สีดิน/สีใบ/โรค | สถานะ | รูป |
|---|---|---|---|---|---|---|---|---|---|---|
| SV-2569-0000001 | CRP-2569-0000001 | QT-2569-001 · PLT-2569-001 | สมหญิง รักดี | ภาคภูมิ เดินดง | ขอนแก่น 3 | 145.50 | 12.50 | น้ำตาล/ปกติ/ไม่พบ | **รอตรวจสอบ** | 5 (field1 crop2 stalk1 soil1) |
| SV-2569-0000002 | CRP-2569-0000001 | QT-2569-001 · PLT-2569-001 | สมหญิง รักดี | ภาคภูมิ เดินดง | ขอนแก่น 3 | 151.00 | 12.50 | น้ำตาล/เขียวเข้ม/น้อย | **รอตรวจสอบ** | 3 |
| SV-2569-0000003 | CRP-2569-0000003 | QT-2569-002 · PLT-2569-003 | สุรพล เก่งการไร่ | ธีรเดช ไร่กว้าง | LK92-11 | 280.00 | 25.00 | ดำ/ปกติ/ไม่พบ | **ยืนยันแล้ว** | 3 |
| SV-2569-0000004 | CRP-2569-0000004 | QT-2569-003 · PLT-2569-005 | ทองดี พูลผล | อารยา สวนอ้อย | K88-92 | 98.75 | 15.20 | แดง/เหลือง/ปานกลาง | **รอตรวจสอบ** | 3 |
| SV-2569-0000005 | CRP-2569-0000005 | QT-2569-004 · PLT-2569-006 | ประนอม ใจเพชร | ภาคภูมิ เดินดง | ขอนแก่น 3 | 62.40 | 6.00 | น้ำตาล/ปกติ/ไม่พบ | **ยืนยันแล้ว** | 5 |
| SV-2569-0000006 | CRP-2569-0000006 | QT-2569-001 · PLT-2569-002 | สมหญิง รักดี | อารยา สวนอ้อย | LK92-11 | 110.20 | 8.75 | เทา/เขียวเข้ม/น้อย | **รอตรวจสอบ** | 2 |
| SV-2569-0000007 | CRP-2569-0000003 | QT-2569-002 · PLT-2569-003 | สุรพล เก่งการไร่ | ธีรเดช ไร่กว้าง | LK92-11 | 305.00 | 25.00 | ดำ/ปกติ/มาก | **ปฏิเสธ** | 4 |
| SV-2569-0000008 | CRP-2569-0000005 | QT-2569-004 · PLT-2569-006 | ประนอม ใจเพชร | ภาคภูมิ เดินดง | ขอนแก่น 3 | 55.00 | 6.00 | น้ำตาล/ปกติ/ไม่พบ | **ยกเลิก** | 1 |

สรุป: รอตรวจสอบ 4 (SV-001/002/004/006) · ยืนยันแล้ว 2 (SV-003/005) · ปฏิเสธ 1 (SV-007) · ยกเลิก 1 (SV-008) · **แบบสำรวจแสดงทั้งหมด 8** (ไม่มี deleted ใน seed — deleted ถูกซ่อน) · getYears() = [2569] (ทุกแถวปี 2569)
- SV-007 reject_reason = "ประมาณการผลผลิตสูงผิดปกติเมื่อเทียบกับขนาดแปลง และพบโรค/ศัตรูพืชระดับมาก กรุณาสำรวจซ้ำ" · SV-008 cancel_reason = "สำรวจซ้ำซ้อนกับแบบสำรวจอื่นในรอบปลูกเดียวกัน"
- SV-003 verify_note = "ข้อมูลครบถ้วน พิกัดตรงแปลง" · SV-005 verify_note = "ผ่านการตรวจสอบภาคสนาม"
> ⚠ **1 รอบปลูก : N แบบสำรวจ signature:** SV-0000001 + SV-0000002 ผูก **CRP-2569-0000001** เดียวกัน · SV-0000003 + SV-0000007 ผูก CRP-2569-0000003 · SV-0000005 + SV-0000008 ผูก CRP-2569-0000005 → พิสูจน์ 1 crop : N surveys (XT-04) ได้ทันที

**Seed โควตา (4 รายการ — จาก `QUOTAS` const, READ-ONLY · ทุกตัว verified → เลือกได้ทุกตัว):**
| เลขโควตา | สถานะ | เกษตรกร | เบอร์ | เลขบัตร (masked) |
|---|---|---|---|---|
| QT-2569-001 | verified | สมหญิง รักดี | 0823456789 | 3-XXXX-XXXX-XX-2 |
| QT-2569-002 | verified | สุรพล เก่งการไร่ | 0945678901 | 3-XXXX-XXXX-XX-4 |
| QT-2569-003 | verified | ทองดี พูลผล | 0889012345 | 3-XXXX-XXXX-XX-8 |
| QT-2569-004 | verified | ประนอม ใจเพชร | 0833334444 | 4-XXXX-XXXX-XX-3 |
> `verifiedQuotas()` คืนทั้ง 4 · ค้นด้วยเลขโควตาหรือชื่อเกษตรกร (exact) · emptyText = "ไม่พบ Quota หรือสถานะไม่เป็น verified" · **seed ไม่มีโควตา waiting** → การกรอง non-verified เป็น code-path (verify ที่ SIT ด้วย record จริง — ดู TC-X01)

**Seed แปลง (7 รายการ — จาก `PLOTS` const, READ-ONLY · ทุกตัว verified · `plotsForQuota` = ของเจ้าของโควตา + verified):**
| เลขแปลง | โควตา(เจ้าของ) | ขนาด(ไร่) | ที่อยู่ | เลือกได้บนโควตานั้น? |
|---|---|---|---|---|
| PLT-2569-001 | QT-2569-001 | 12.50 | 99 หมู่ 3 · วังขนาย ท่าม่วง กาญจนบุรี | ✅ |
| PLT-2569-002 | QT-2569-001 | 8.75 | 101 หมู่ 3 · ท่าม่วง ท่าม่วง กาญจนบุรี | ✅ |
| PLT-2569-003 | QT-2569-002 | 25.00 | 18 หมู่ 2 · สองพี่น้อง สองพี่น้อง สุพรรณบุรี | ✅ |
| PLT-2569-004 | QT-2569-002 | 30.40 | 20 หมู่ 2 · ต้นตาล สองพี่น้อง สุพรรณบุรี | ✅ |
| PLT-2569-005 | QT-2569-003 | 15.20 | 77 หมู่ 1 · โพธาราม โพธาราม ราชบุรี | ✅ |
| PLT-2569-006 | QT-2569-004 | 6.00 | 5 หมู่ 5 · ท่าผา บ้านโป่ง ราชบุรี | ✅ |
| PLT-2569-007 | QT-2569-004 | 18.90 | 8 หมู่ 5 · บ้านโป่ง บ้านโป่ง ราชบุรี | ✅ |
> `plotsForQuota(qid)`: QT-001→[PLT-001, PLT-002] (2) · QT-002→[PLT-003, PLT-004] (2) · QT-003→[PLT-005] (1) · QT-004→[PLT-006, PLT-007] (2) — **1 โควตา : N verified plots**

**Seed รอบปลูก (7 รายการ — จาก `CROPS` const, READ-ONLY · `cropsForPlot` = ของแปลงนั้น):**
| เลขรอบปลูก | แปลง(เจ้าของ) | ปี(พ.ศ.) | เดือน | บนแปลงนั้น |
|---|---|---|---|---|
| CRP-2569-0000001 | PLT-2569-001 | 2569 | 1 · ม.ค. | ✅ (คู่กับ CRP-0000002) |
| CRP-2569-0000002 | PLT-2569-001 | 2569 | 2 · ก.พ. | ✅ |
| CRP-2569-0000003 | PLT-2569-003 | 2569 | 12 · ธ.ค. | ✅ |
| CRP-2569-0000004 | PLT-2569-005 | 2569 | 3 · มี.ค. | ✅ |
| CRP-2569-0000005 | PLT-2569-006 | 2569 | 5 · พ.ค. | ✅ |
| CRP-2569-0000006 | PLT-2569-002 | 2569 | 4 · เม.ย. | ✅ |
| CRP-2569-0000007 | PLT-2569-004 | 2569 | 6 · มิ.ย. | ✅ |
> `cropsForPlot(pid)`: PLT-001→[CRP-001, CRP-002] (2 — 1 แปลง : N รอบปลูก) · PLT-002→[CRP-006] · PLT-003→[CRP-003] · PLT-004→[CRP-007] · PLT-005→[CRP-004] · PLT-006→[CRP-005] · **PLT-007→[] (0 — cascade ทางตัน → "ไม่พบรอบปลูกของแปลงนี้")**

**Agronomic enums (จาก const, ใช้ verbatim ใน dropdown สร้าง/แก้ไข):**
- พันธุ์อ้อย (`CANE_VARIETIES`): **ขอนแก่น 3 / LK92-11 / K88-92 / อู่ทอง 12 / กำแพงแสน 01** (5 ตัวเลือก)
- สีดิน (`SOIL_COLORS`): **ดำ / น้ำตาล / แดง / เทา / อื่นๆ**
- การตรวจสีใบ (`LEAF_CHECKS`): **ปกติ / เหลือง / เขียวเข้ม / อื่นๆ**
- พบโรค/ศัตรูพืช (`DISEASE_LEVELS`): **ไม่พบ / น้อย / ปานกลาง / มาก**
- รูปภาพ 4 หมวด (`PHOTO_CATS`): **รูปกับแปลง (field) / รูปพืชผล (crop) / รูปลำต้นในกอ (stalk) / รูปสีดิน (soil)**

**Users:** เจ้าหน้าที่สำรวจ = **สมพร วงศ์ทะเบียน** (`CURRENT_USER` · role "เจ้าหน้าที่สำรวจภาคสนาม" · create/edit/csv/cancel/delete) · ผู้ตรวจสอบ = **ธนพล ตรวจสอบ** (`CHECKER` · verify/reject/bulk) — prototype ไม่มี role switching (user เดียวกดได้ทุก action; RBAC/SoD = TC-S04 simulate)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination | TC-L01..L07 (7) | สูง |
| C — สร้าง + cascade 3-level + agronomic + photos + validation | TC-C01..C12 (12) | สูงสุด |
| I — CSV Import (9-col schema · ทุกแถว waiting) | TC-I01..I06 (6) | สูง |
| V — ตรวจสอบ/ปฏิเสธ (เดี่ยว) | TC-V01..V05 (5) | สูง |
| B — Bulk verify/reject | TC-B01..B03 (3) | สูง |
| E — แก้ไข + State machine (verified→waiting ⭐) | TC-E01..E05 (5) | สูงสุด |
| D — ยกเลิก / ลบ (soft) | TC-D01..D04 (4) | สูง |
| W — Detail / 3 tabs / รูปภาพ 4 หมวด / ประวัติ | TC-W01..W05 (5) | สูง |
| **X — Cross-module: cascade read + feeds Crop + 1 crop:N surveys ⭐** | TC-X01..X05 (5) | **สูงสุด** |
| S — System / simulate (optimistic lock, concurrency, SoD, deep-link) | TC-S01..S04 (4) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1 ← BRD §7)
| item | cases |
|---|---|
| AC-01 เลือก quota → farmer snapshot · plot → crop (cascade) · fields ปลดล็อก | TC-C01, TC-C02, TC-X01, TC-X02 |
| AC-02 กรอกพื้นฐาน+พืชผล+รูป 4 หมวด → ยืนยันสร้าง → toast "สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]" + รอตรวจสอบ + audit | TC-C01, TC-X02, TC-X05 |
| AC-02b cascade ไม่ครบ → block ("กรุณากรอกข้อมูลให้ครบถ้วน") | TC-C10, TC-C05 |
| AC-03 ผลผลิต < 0 / ขนาดแปลง ≤ 0 → "กรุณาใส่ค่าที่ถูกต้อง" | TC-C08, TC-C09 |
| AC-04 เลือก สีดิน/การตรวจสีใบ/โรค-ศัตรูพืช จาก dropdown | TC-C07 |
| AC-05 แนบรูปแต่ละหมวด (field/crop/stalk/soil) → preview | TC-C11, TC-W02 |
| AC-06 submit ก่อนครบ cascade → block "กรุณาเลือกโควตา แปลง และรอบปลูกก่อน" | TC-C05, TC-C02 |
| AC-10 search (survey_id/quota/plot/crop/ผู้สำรวจ) + filter status(5)+ปี · ไม่พบ → "ไม่พบรายการที่ค้นหา" | TC-L02, TC-L03, TC-L04 |
| AC-28 sort + export CSV + pagination | TC-L05, TC-L06, TC-L07 |
| AC-11 แก้ survey waiting + save → version++ + audit | TC-E01 |
| AC-11b แก้ survey **verified** + save → **กลับ waiting** (LOCK-07) + toast "บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ" ⭐ | TC-E02 |
| AC-12 stale → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| AC-13 quota/plot/crop บนหน้า edit = read-only | TC-E04 |
| AC-14 CSV ดี N แถว → summary + ทุกแถว waiting | TC-I02, TC-I06 |
| AC-15 header ไม่ตรง → reject ทั้งไฟล์ | TC-I04 |
| AC-16 cascade/field invalid รายแถว → error report | TC-I05, TC-I02 |
| AC-17 ไม่ใช่ .csv → "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" | TC-I03 |
| AC-18 waiting + ยืนยัน → toast "ยืนยันเรียบร้อย" + pill เขียว(ยืนยันแล้ว) + audit | TC-V01 |
| AC-19 ปฏิเสธ ไม่กรอกเหตุผล → "กรุณากรอกเหตุผลในการปฏิเสธ" block | TC-V02 |
| AC-20 ปฏิเสธ + reason → pill แดง(ปฏิเสธ) + reject_reason แสดง + audit | TC-V03, TC-W01 |
| AC-21 Bulk: เลือกทั้งหมด = เฉพาะ waiting · ยืนยันกลุ่ม → summary | TC-B01 |
| AC-22 Bulk reject = เหตุผลบังคับ (ร่วม) · skip non-waiting | TC-B02, TC-B03 |
| AC-23b verified/rejected → verify ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม) | TC-V05, TC-S02 (simulate) |
| AC-24 detail tabs (ข้อมูลสำรวจ/รูปภาพ/ประวัติ) + snapshot card (ดูรอบปลูก) | TC-W01, TC-W02 |
| AC-25 tab รูปภาพ = 4 หมวด · tab ประวัติ = audit | TC-W02, TC-W04 |
| AC-25b deep-link survey ไม่มี/deleted → "ไม่พบข้อมูลแบบสำรวจที่เลือก" + กลับ list | TC-W05, TC-D02 |
| AC-26 ยกเลิก + เหตุผล → toast "ยกเลิกแบบสำรวจแล้ว" + audit · ไม่ใส่เหตุผล → block | TC-D01, TC-D04 |
| AC-27 ลบ + เหตุผล → soft delete + ซ่อน + audit | TC-D02, TC-D03 |

### Cross-Module (06_TESTS §6.9) ⭐
| XT | Scenario | Source | Case |
|---|---|---|---|
| XT-01 | สร้าง survey → quota_id/plot_id/crop_id set + snapshot ตรง · **source ไม่ถูกแก้** | Quota+Plot+Crop (read) | TC-X02, TC-X05 |
| XT-02 | cascade: quota → plots ของโควตา · plot → crops ของแปลง | Quota→Plot→Crop | TC-X01, TC-X03, TC-C01 |
| XT-03 | survey **verified** แสดงในแท็บสำรวจของรอบปลูก | Crop F-AGM-004 | TC-X04 (ต้อง simulate) |
| XT-04 | 1 รอบปลูก : N แบบสำรวจ (สำรวจซ้ำรอบได้) | — | TC-X05, TC-L02 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-AGS-01 cascade โควตา→แปลง(ของโควตา)→รอบปลูก(ของแปลง)→ฟอร์ม | TC-C01, TC-C02, TC-X01, TC-X03 |
| BR-AGS-02 snapshot farmer/plot/crop read-only | TC-C01, TC-X02, TC-W01 |
| BR-AGS-03 create/CSV → waiting_for_verify เสมอ | TC-C01, TC-I06 |
| BR-AGS-04 verify/reject: waiting เท่านั้น · note optional · reject reason บังคับ · เดี่ยว+bulk | TC-V01, TC-V02, TC-B01, TC-B02 |
| BR-AGS-05 **edit survey verified + save → กลับ waiting** ⭐ | TC-E02 |
| BR-AGS-06 photos 4 หมวด (field/crop/stalk/soil) | TC-C11, TC-W02 |
| BR-AGS-07 CSV per-row · ทุกแถว waiting · partial + report | TC-I02, TC-I06 |
| BR-AGS-08 soft cancel/delete + reason + audit | TC-D01, TC-D02, TC-W04 |
| BR-AGS-09 audit ทุก mutation (+ bulk count) | TC-W04, TC-B01 |
| BR-AGS-10 optimistic lock + idempotency | TC-C12, TC-S01, TC-S03 |
| BR-AGS-11 survey verified feeds Crop survey tab | TC-X04 (ต้อง simulate) |

### Validation (05_RULES §5.4 VR-01..06)
| VR | cases |
|---|---|
| VR-01 cascade quota→plot→crop ครบ | TC-C05, TC-C02, TC-I05 |
| VR-02 crop ของ plot ของ quota (cascade filter) | TC-X03, TC-C04, TC-I05 |
| VR-03 พื้นฐาน+พืชผล required (วันที่/ผู้สำรวจ/ปี/พันธุ์/ผลผลิต/ขนาด) → "กรุณากรอกข้อมูลให้ครบถ้วน" | TC-C10, TC-C06, TC-I05 |
| VR-04 yield ≥ 0 · plot_size > 0 → "กรุณาใส่ค่าที่ถูกต้อง" | TC-C08, TC-C09, TC-I05 |
| VR-05 lat/long ช่วง (ถ้ากรอก) | TC-C11 (พิกัด optional) |
| VR-06 reject_reason บังคับเมื่อ reject | TC-V02, TC-B02 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 cascade ไม่ครบ → block | TC-C05, TC-C02, TC-C10 |
| EC-02 crop ไม่ใช่ของ plot → cascade filter | TC-X03, TC-C04, TC-I05 |
| EC-03 yield < 0 / plot_size ≤ 0 | TC-C08, TC-C09 |
| EC-04 reject ไม่ใส่เหตุผล | TC-V02, TC-B02 |
| EC-05 edit survey verified → save → กลับ waiting (BR-05) ⭐ | TC-E02 |
| EC-06 bulk เลือกรวม non-waiting → skip + summary | TC-B03, TC-B01 |
| EC-07 stale edit → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| EC-08 concurrent verify → 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (ต้อง simulate) |
| EC-09 CSV header ไม่ตรง → reject ทั้งไฟล์ + column error | TC-I04 |
| EC-10 CSV row cascade invalid → error รายแถว | TC-I05, TC-I02 |
| EC-11 double-submit → idempotency → 1 รายการ | TC-C12 |
| EC-12 deep-link survey ไม่มี/deleted → "ไม่พบข้อมูลแบบสำรวจที่เลือก" + กลับ list | TC-W05, TC-D02 |

### Error catalog (05_RULES §5.6 — ที่มีผลบน UI prototype)
| error | cases |
|---|---|
| ERR_CASCADE_INVALID "กรุณากรอกข้อมูลให้ครบถ้วน" (required) · (create ก่อนครบ cascade) "กรุณาเลือกโควตา แปลง และรอบปลูกก่อน" | TC-C05, TC-C10, TC-C02 |
| ERR_VALIDATION "กรุณาใส่ค่าที่ถูกต้อง" (yield/size) · "ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600" | TC-C08, TC-C09, TC-C06 |
| ERR_REJECT_NO_REASON "กรุณากรอกเหตุผลในการปฏิเสธ" | TC-V02, TC-B02 |
| (verify no result) "กรุณาเลือกผลการตรวจสอบ" | TC-V04 |
| (cancel/delete no reason) "กรุณากรอกเหตุผล" | TC-D01, TC-D02 |
| (verify non-waiting selected) "เลือกได้เฉพาะรายการที่รอตรวจสอบ" | TC-V05, TC-B01 |
| ERR_CSV_INVALID "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" · (>5MB) "ขนาดไฟล์ต้องไม่เกิน 5MB" | TC-I03 |
| (CSV header) "ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ" + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]" | TC-I04 |
| ERR_STALE(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (simulate) |
| ERR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (simulate) |
| ERR_NOT_FOUND "ไม่พบข้อมูลแบบสำรวจที่เลือก" | TC-W05, TC-D02 |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases / สถานะ |
|---|---|
| เจ้าหน้าที่สำรวจ: create/edit/csv/cancel/delete = allow | TC-C01, TC-E01, TC-D01, TC-I02 (prototype user=สมพร วงศ์ทะเบียน) |
| ผู้ตรวจสอบ: +verify/reject/bulk = allow | TC-V01, TC-B01 (prototype verify actor=ธนพล ตรวจสอบ) |
| ปุ่มซ่อนตาม RBAC + SoD self-verify flag (OQ-SV5) | TC-S04 (ต้อง simulate — prototype ไม่มี role switching) |

### Scope Lock (00_OVERVIEW §0.11 ← BRD §3.4)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | capability legacy 100% (CRUD/CSV/verify/reject/bulk/cancel/delete/search) | ทั้ง suite — ตัวแทน: TC-C01, TC-I02, TC-V01, TC-B01, TC-E01, TC-D01, TC-W01, TC-L02 |
| LOCK-02 | canonical **5-state** machine + soft cancel/delete | TC-V01, TC-V03, TC-D01, TC-D02, TC-L01 |
| LOCK-03 | **cascade (quota→plot→crop) 3-level read-only** ⭐⭐⭐ | TC-C01, TC-C02, TC-X01, TC-X03 |
| LOCK-04 | agronomic fields (พันธุ์/ผลผลิต/ขนาด/สีดิน/สีใบ/โรค/พิกัด) | TC-C07, TC-C08, TC-W01 |
| LOCK-05 | snapshot farmer/plot/crop read-only | TC-C01, TC-X02, TC-W01 |
| LOCK-06 | **photos 4 หมวด** ⭐ | TC-C11, TC-W02 |
| LOCK-07 | **edit verified → waiting_for_verify** ⭐ | TC-E02 |
| LOCK-08 | verify/reject (reject reason บังคับ) เดี่ยว+bulk | TC-V01, TC-V02, TC-B01, TC-B02 |
| LOCK-09 | CSV partial + ทุกแถว waiting | TC-I02, TC-I06 |
| LOCK-10 | soft cancel/delete + reason บังคับ + audit | TC-D01, TC-D02 |
| LOCK-11 | optimistic + idempotency + audit · feeds Crop survey tab | TC-C12, TC-S01, TC-W04, TC-X04 |

### Cross-Module (00_OVERVIEW §0.14)
| item | cases |
|---|---|
| Survey อ่าน Quota→Plot→Crop (cascade, read-only, no write-back) | TC-X01, TC-X02, TC-X03 |
| survey verified feeds Crop F-AGM-004 (แท็บสำรวจ — pull-read) | TC-X04 (ต้อง simulate) |
| 1 crop : N surveys | TC-X05, TC-L02 |

### UI States (§8 State-Driven Matrix — canonical 5)
| item | cases |
|---|---|
| loaded / filtered / filter-empty | TC-L01, TC-L02, TC-L04 |
| stats 4 การ์ด (สำรวจทั้งหมด/รอตรวจสอบ+aging/ยืนยันแล้ว/ปฏิเสธ) | TC-L01 |
| pill 4 สถานะ (รอตรวจสอบ/ยืนยันแล้ว/ปฏิเสธ/ยกเลิก + deleted ซ่อน) | TC-L01, TC-D02, TC-D04 |
| checkbox waiting selectable / อื่น disabled | TC-B01, TC-V05 |
| snapshot card (orange) + ดูรอบปลูก (read-only) | TC-W01, TC-W02 |
| field gating (locked จนครบ quota+plot+crop) ⭐⭐⭐ | TC-C02 |
| detail actions ตามสถานะ (แก้ไข/ตรวจสอบ(waiting)/ยกเลิก-ลบ) | TC-V05, TC-D03 |
| submitting state ("กำลังบันทึก…/กำลังดำเนินการ…/กำลังนำเข้า…") | TC-C01, TC-V01, TC-D01, TC-I02 |
| sort / pagination footer | TC-L05, TC-L06 |

**Manifest cross-check (FRD §0.12):** Stories 10/10 (US-01..10) · Rules BR-AGS-01..11 11/11 · VR-01..06 6/6 · EC-01..12 12/12 · XT-01..04 4/4 · LOCK-01..11 11/11 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — แบบสำรวจถูกต้อง (happy — ผูก QT-2569-001 + PLT-2569-001 + CRP-2569-0000001)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาโควตา (Quota Id · exact) | เลือก **QT-2569-001 · สมหญิง รักดี** *(sub "0823456789 · 3-XXXX-XXXX-XX-2")* |
| เลือกแปลง (ของโควตา · verified) | เลือก **PLT-2569-001 · 99 หมู่ 3** *(sub "วังขนาย ท่าม่วง กาญจนบุรี" · right "12.50 ไร่")* |
| เลือกรอบปลูก (ของแปลง) | เลือก **CRP-2569-0000001 · ปี 2569 · เดือน 1 · ม.ค.** |
| วันที่สำรวจ | 2026-07-15 (วันนี้/ล่าสุด) |
| ผู้สำรวจ | ภาคภูมิ เดินดง |
| ปีผลิต (พ.ศ.) | 2569 |
| พันธุ์อ้อย | ขอนแก่น 3 |
| ประมาณการผลผลิต (ตัน) | 130.00 |
| ขนาดแปลง (ไร่) | 12.50 *( auto-fill จาก plot · แก้ได้)* |
| สีดิน / การตรวจสีใบ / พบโรค/ศัตรูพืช | น้ำตาล / ปกติ / ไม่พบ |
| พิกัด (lat,long) | 14.023145,99.512088 *(ไม่บังคับ)* |
| รูปภาพ | คลิก **แนบรูป** ในหมวด รูปกับแปลง (จำลอง) |

### ชุด B — ค่าผิดสำหรับ negative (ต้องเลือก cascade ชุด A ครบก่อน เพื่อปลดล็อกฟิลด์)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | ปีผลิต (พ.ศ.) | `2400` | ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600 |
| B2 | ประมาณการผลผลิต (ตัน) | `-5` | กรุณาใส่ค่าที่ถูกต้อง |
| B3 | ขนาดแปลง (ไร่) | `0` | กรุณาใส่ค่าที่ถูกต้อง |
| B4 | พันธุ์อ้อย | *(ไม่เลือก — คง "— เลือก —")* | กรุณาเลือกพันธุ์อ้อย |
| B5 | วันที่สำรวจ + ผู้สำรวจ | *(เว้นว่าง)* | กรุณาระบุวันที่สำรวจ / กรุณาระบุผู้สำรวจ |
| B6 | ค้นหาโควตา | พิมพ์ `QT-9999` | ไม่พบ Quota หรือสถานะไม่เป็น verified (emptyText) |
| B7 | cascade | *(ไม่เลือกเลย → submit)* | กรุณาเลือกโควตา แปลง และรอบปลูกก่อน |

### ไฟล์ทดสอบ (Files) — runner ต้องเตรียมก่อนรัน
> header 9 คอลัมน์ (จาก `CSV_COLS`): `quota_id,plot_id,crop_id,survey_date,surveyor,production_year_be,cane_variety,yield_estimate,plot_size_rai`
> *(แม่แบบดาวน์โหลดได้ในModal = `survey_template.csv` · schema = create · UTF-8 BOM · 2 แถวตัวอย่าง)*

| ชื่อไฟล์ | เนื้อหา |
|---|---|
| `survey_ok.csv` | 3 แถวถูกทั้งหมด: `QT-2569-001,PLT-2569-001,CRP-2569-0000001,2026-07-10,ภาคภูมิ เดินดง,2569,ขอนแก่น 3,140.00,12.50` · `QT-2569-002,PLT-2569-003,CRP-2569-0000003,2026-07-11,ธีรเดช ไร่กว้าง,2569,LK92-11,275.00,25.00` · `QT-2569-004,PLT-2569-006,CRP-2569-0000005,2026-07-12,ภาคภูมิ เดินดง,2569,ขอนแก่น 3,60.00,6.00` |
| `survey_mixed.csv` | 5 แถว: 3 ถูก + แถว 4 `production_year_be=2400` (นอกช่วง) + แถว 5 `yield_estimate=-5` |
| `survey_badbind.csv` | 3 แถว: แถว 1 ถูก · แถว 2 `plot_id=PLT-2569-003` กับ `quota_id=QT-2569-001` (plot owner mismatch — PLT-003 เป็นของ QT-002) · แถว 3 `crop_id=CRP-2569-0000003` กับ `plot_id=PLT-2569-001` (crop ไม่ใช่ของ plot ที่ระบุ) |
| `survey_badheader.csv` | header ขาดคอลัมน์ `plot_size_rai` (เหลือ 8 คอลัมน์) + 1 แถวข้อมูลถูก |
| `survey_too_large.csv` | ไฟล์ .csv ขนาด > 5MB (gen แถวซ้ำจนเกิน) |
| `notes.xlsx` | ไฟล์ Excel ใด ๆ (ทดสอบ guard นามสกุลไฟล์) |

---

## Test Cases

## Group L — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination (P-01)

### TC-L01 — เปิดหน้า list + stats widgets (happy)
- group: L · ความสำคัญ: สูง · trace: 01_UI P-01 / UI state loaded / D-01 stats
- Setup: role=เจ้าหน้าที่สำรวจ (default) · seed=default 8 แบบสำรวจ (refresh) · files=—
- Start: OPEN `#/surveys`
- ผ่านเมื่อ: หน้า list + สถิติ 4 การ์ดแสดงเลขตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/surveys` | — | หัวข้อ **จัดการแบบสำรวจ** + count **8 รายการ** · sub "ทะเบียนแบบสำรวจแปลง · ผูกโควตา→แปลง→รอบปลูก · ตรวจสอบยืนยันและนำเข้า CSV" · breadcrumb "เกษตรกรรม › จัดการแบบสำรวจ" · sidebar **จัดการแบบสำรวจ** active · user chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่สำรวจภาคสนาม · WKN" | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **สำรวจทั้งหมด 8** (meta "ไม่รวมที่ยกเลิก/ลบ") · **รอตรวจสอบ 4** (meta "ค้างเกิน 7 วัน N รายการ" หรือ "SLA ตรวจภายใน 3 วันทำการ") · **ยืนยันแล้ว 2** (meta "ป้อนเข้าแท็บสำรวจของรอบปลูก") · **ปฏิเสธ 1** (meta "มีเหตุผลระบุ") | ☐ |
| 3 | VERIFY ปุ่มบน page header (ขวาบน) | — | เรียงซ้าย→ขวา: **Upload CSV** · **ตรวจสอบที่เลือก (0)** (disabled) · **สร้างแบบสำรวจ** (ปุ่มแดง ขวาสุด) | ☐ |
| 4 | VERIFY ตาราง | — | 10 คอลัมน์: ☑, เลขสำรวจ (mono แดง), วันที่สำรวจ, เลขโควตา, เลขแปลง, เลขรอบปลูก, พันธุ์อ้อย, ประมาณการผลผลิต (ตัน), สถานะ, การดำเนินการ · pill 4 สี ครบ (รอตรวจสอบ เหลือง/ยืนยันแล้ว เขียว/ปฏิเสธ แดง/ยกเลิก เทา) | ☐ |
| 5 | VERIFY แถว SV-2569-0000003 | — | pill เขียว **ยืนยันแล้ว** · checkbox จาง กดไม่ได้ · คอลัมน์การดำเนินการมีเฉพาะไอคอนดินสอ (ไม่มีถังขยะ — ลบเฉพาะ waiting) | ☐ |
| 6 | VERIFY footer ตาราง | — | ข้อความ **1 – 8 จาก 8 รายการ** · หน้า 1 active | ☐ |

### TC-L02 — ค้นหา (debounce 300ms, 5 field) (happy — AC-10 / XT-04)
- group: L · ความสำคัญ: สูง · trace: AC-10 / US-10 / 1 crop:N surveys
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys`
- ผ่านเมื่อ: ค้นได้ survey_id/quota/plot/crop/ผู้สำรวจ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "SV-2569-0000007" → ช่องค้นหา | เลขสำรวจ | รอ ~0.3s ตารางเหลือ 1 แถว: SV-2569-0000007 สุรพล เก่งการไร่ (pill แดง **ปฏิเสธ**) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** แล้ว TYPE "CRP-2569-0000001" | เลขรอบปลูก | เหลือ 2 แถว (SV-0000001, SV-0000002 — ผูกรอบปลูกเดียวกัน = 1 crop:N surveys) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** แล้ว TYPE "QT-2569-001" | เลขโควตา | เหลือ 3 แถว (SV-0000001, SV-0000002, SV-0000006 — QT-001) | ☐ |
| 4 | CLICK **ล้างตัวกรอง** แล้ว TYPE "PLT-2569-003" | เลขแปลง | เหลือ 2 แถว (SV-0000003, SV-0000007 — PLT-003) | ☐ |
| 5 | CLICK **ล้างตัวกรอง** แล้ว TYPE "ภาคภูมิ" | ชื่อผู้สำรวจ | เหลือ 4 แถว (SV-0000001, SV-0000002, SV-0000005, SV-0000008 — ผู้สำรวจ ภาคภูมิ เดินดง) | ☐ |

### TC-L03 — กรองสถานะ (5) + ปี (พ.ศ.) (happy — AC-10)
- group: L · ความสำคัญ: สูง · trace: AC-10 / filter status(5)+year
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **รอตรวจสอบ** | — | เหลือ 4 แถว ทุกแถว pill เหลือง · footer "1 – 4 จาก 4 รายการ" | ☐ |
| 2 | SELECT dropdown สถานะ = **ยืนยันแล้ว** | — | เหลือ 2 แถว (SV-0000003, SV-0000005) pill เขียว **ยืนยันแล้ว** | ☐ |
| 3 | SELECT dropdown สถานะ = **ปฏิเสธ** | — | เหลือ 1 แถว (SV-0000007) pill แดง **ปฏิเสธ** | ☐ |
| 4 | SELECT dropdown สถานะ = **ยกเลิก** | — | เหลือ 1 แถว (SV-0000008) pill เทา **ยกเลิก** — ยืนยัน cancelled คงอยู่ในรายการ | ☐ |
| 5 | CLICK **ล้างตัวกรอง** → VERIFY dropdown ปี | — | dropdown ปีมีตัวเลือก "ทุกปี (พ.ศ.)" + **2569** (getYears = ทุกแถวปี 2569) · SELECT 2569 → คง 8 แถว | ☐ |

### TC-L04 — ค้นหาไม่เจอ → empty state (edge — AC-10)
- group: L · ความสำคัญ: กลาง · trace: AC-10 filter-empty
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีแบบสำรวจนี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state: **ไม่พบรายการที่ค้นหา** + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty state) | — | ตารางกลับมา 8 รายการ | ☐ |

### TC-L05 — Sort คอลัมน์ (AC-28)
- group: L · ความสำคัญ: ต่ำ · trace: AC-28 / sortBy survey_id/survey_date/yield_estimate
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **ประมาณการผลผลิต (ตัน)** | — | แถวเรียงน้อย→มาก (55.00 = SV-0000008 บนสุด → 305.00 = SV-0000007 ล่าง) | ☐ |
| 2 | CLICK หัวคอลัมน์ **ประมาณการผลผลิต (ตัน)** อีกครั้ง | — | เรียงกลับ มาก→น้อย (305.00 บนสุด) | ☐ |
| 3 | CLICK หัวคอลัมน์ **เลขสำรวจ** | — | เรียงตาม survey_id (SV-2569-0000001 บนสุด) | ☐ |
| 4 | CLICK หัวคอลัมน์ **วันที่สำรวจ** | — | เรียงตาม survey_date (เก่า→ใหม่) — เปลี่ยนลำดับแถวจาก survey_id | ☐ |

### TC-L06 — Pagination footer + row-click เปิด Detail (AC-28)
- group: L · ความสำคัญ: ต่ำ · trace: AC-28 / row-click = openView
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (8 < 20/หน้า — หน้าเดียว) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ pagination | — | ปุ่มหน้า **1** (active สีแดง) · ลูกศรซ้าย/ขวา disabled (หน้าเดียว) | ☐ |
| 2 | CLICK กลางแถว SV-2569-0000003 (ไม่โดน checkbox/ไอคอน) | — | Detail drawer เปิด eyebrow "แบบสำรวจ · QT-2569-002 · PLT-2569-003 · CRP-2569-0000003" + หัวข้อ **SV-2569-0000003** + route เปลี่ยนเป็น `#/surveys/SV-2569-0000003` | ☐ |
| 3 | PRESS Esc | — | drawer ปิด + route กลับ `#/surveys` | ☐ |

### TC-L07 — Export CSV (AC-28) (ต้อง simulate)
- group: L · ความสำคัญ: กลาง · trace: AC-28 / API-15 · **หมายเหตุ: prototype ไม่มีปุ่ม Export ในหน้า header (มีเฉพาะ Upload CSV) — export = server-side/UI phase ถัดไป**
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default
- Start: — (SIT / UI ระบบจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (prototype): หน้า header | — | มีปุ่ม Upload CSV แต่ **ไม่มีปุ่ม Export** — mark BLOCKED บน prototype (export ยังไม่มี UI) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): filter สถานะ=ยืนยันแล้ว → Export CSV | — | ไฟล์ CSV มีเฉพาะแถวที่ตรง filter · คอลัมน์ตรงตาราง · ชื่อไฟล์ locale ไทย | ☐ |

---

## Group C — สร้างแบบสำรวจ + cascade 3-level + agronomic + photos + validation (OV-01)

### TC-C01 — สร้างแบบสำรวจ happy (cascade QT-001 → PLT-001 → CRP-001) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-02 / BR-AGS-01/02/03 / LOCK-03/05 / XT-02
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys`
- ชุดข้อมูล: A
- ผ่านเมื่อ: cascade ครบ 3 ชั้น + snapshot + toast สร้างสำเร็จ + แถวใหม่ waiting

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างแบบสำรวจ** (แดง ขวาบน) | — | drawer เปิดจากขวา eyebrow **สร้างแบบสำรวจ** + หัวข้อ **สร้างแบบสำรวจ** · section **เลือกโควตา แปลง รอบปลูก (บังคับก่อนกรอกข้อมูล)** · note info lock **เลือกโควตา แปลง และรอบปลูกก่อนจึงจะกรอกข้อมูลแบบสำรวจได้** · ฟิลด์แบบสำรวจล็อกทั้งหมด | ☐ |
| 2 | CLICK ช่อง **ค้นหาโควตา (Quota Id · exact)** → พิมพ์ "QT-2569-001" | A | dropdown แสดง **QT-2569-001 · สมหญิง รักดี** + sub "0823456789 · 3-XXXX-XXXX-XX-2" · help "เลือกได้เฉพาะโควตาที่ยืนยันแล้ว (verified) · ระบบจะดึงข้อมูลเจ้าของให้อัตโนมัติ" | ☐ |
| 3 | CLICK ตัวเลือก **QT-2569-001 · สมหญิง รักดี** | A | ปรากฏ section **เลือกแปลง (ของโควตา · verified)** help "แสดงเฉพาะแปลงที่ยืนยันแล้วของเจ้าของโควตานี้ (2 แปลง)" · ฟิลด์ **ยังล็อก** (ยังไม่ครบ cascade) | ☐ |
| 4 | CLICK ช่องเลือกแปลง → เลือก **PLT-2569-001 · 99 หมู่ 3** | A | การ์ดเขียว **แปลงที่เลือก**: PLT-2569-001 · 99 หมู่ 3 · วังขนาย ท่าม่วง กาญจนบุรี + "ขนาด 12.50 ไร่" + ปุ่ม **เปลี่ยนแปลง** · ปรากฏ section **เลือกรอบปลูก (ของแปลง)** help "แสดงรอบปลูกของแปลงนี้ (2 รอบปลูก)" · ฟิลด์ **ยังล็อก** | ☐ |
| 5 | CLICK ช่องเลือกรอบปลูก → เลือก **CRP-2569-0000001 · ปี 2569 · เดือน 1 · ม.ค.** | A | การ์ดแดงอ่อน **รอบปลูกที่เลือก**: CRP-2569-0000001 · ปี 2569 · เดือน 1 · ม.ค. + note "สำรวจรอบปลูกเดิมได้หลายครั้ง (1 รอบปลูก : หลายแบบสำรวจ)" + ปุ่ม **เปลี่ยนรอบปลูก** · **ฟิลด์แบบสำรวจปลดล็อกทั้งหมด** · note lock หาย · ปีผลิต auto-fill 2569 · ขนาดแปลง auto-fill 12.50 | ☐ |
| 6 | กรอก: วันที่สำรวจ 2026-07-15 · ผู้สำรวจ ภาคภูมิ เดินดง · พันธุ์อ้อย **ขอนแก่น 3** · ผลผลิต 130.00 · สีดิน **น้ำตาล** · สีใบ **ปกติ** · โรค **ไม่พบ** | A | แสดงค่าครบ (section ข้อมูลพื้นฐาน + ข้อมูลพืชผล) | ☐ |
| 7 | CLICK ปุ่ม **แนบรูป** ในหมวด **รูปกับแปลง** | — | toast info **จำลองแนบรูป รูปกับแปลง (JPG/PNG ≤5MB)** · pill นับเลข 1 · รายการไฟล์ survey_field_1_*.jpg ปรากฏ | ☐ |
| 8 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (กดซ้ำไม่ได้) | ☐ |
| 9 | WAIT จน toast ปรากฏ (≤3s) | — | drawer ปิด + toast เขียว **สร้างแบบสำรวจสำเร็จ — SV-2569-0000009** | ☐ |
| 10 | VERIFY ตาราง | — | แถวบนสุด/มี SV-2569-0000009 · pill เหลือง **รอตรวจสอบ** · count = **9 รายการ** · การ์ดรอตรวจสอบ = 5 | ☐ |
| 11 | CLICK แถว SV-2569-0000009 → Tab **ประวัติ** | — | มี 1 event **สร้างแบบสำรวจ** โดย สมพร วงศ์ทะเบียน + note "ผูกโควตา QT-2569-001 · แปลง PLT-2569-001 · รอบปลูก CRP-2569-0000001" | ☐ |

### TC-C02 — Field gating: ฟิลด์ล็อกจนครบ cascade 3-level ★★★ signature
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-06 / BR-AGS-01 / LOCK-03 / triple cascade
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**
- ผ่านเมื่อ: ฟิลด์ล็อกจนกว่าจะเลือก **ครบทั้ง 3** ชั้น (quota → plot → crop)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY block ฟิลด์แบบสำรวจ ก่อนเลือกอะไร | — | โซน `#survey-fields` มี note lock "เลือกโควตา แปลง และรอบปลูกก่อนจึงจะกรอกข้อมูลแบบสำรวจได้" · ทุก input/select/textarea/button ในโซน disabled | ☐ |
| 2 | เลือก **QT-2569-002 · สุรพล เก่งการไร่** (เลือก quota อย่างเดียว) | — | section เลือกแปลงปรากฏ · **ฟิลด์ยัง locked** (ยังไม่เลือก plot+crop) | ☐ |
| 3 | เลือกแปลง **PLT-2569-003** (เลือก plot — ยังไม่เลือก crop) | — | section เลือกรอบปลูกปรากฏ (help "1 รอบปลูก") · **ฟิลด์ยัง locked** (ยังไม่เลือก crop — cascade 3-level บังคับครบทั้ง 3) | ☐ |
| 4 | เลือกรอบปลูก **CRP-2569-0000003** | — | **ฟิลด์ปลดล็อกทันที** (พิมพ์ได้) · note lock หาย | ☐ |
| 5 | CLICK ปุ่ม **เปลี่ยนโควตา** | — | กลับไปโหมดค้นหาโควตา · แปลง+รอบปลูกถูกล้าง (plot+crop reset) · ฟิลด์ล็อกอีกครั้ง (cascade รีเซ็ตทั้งสาย) | ☐ |

### TC-C03 — โควตาค้นไม่พบ → emptyText + section ถัดไปไม่ปรากฏ (negative — AC-06 / VR-01)
- group: C · ความสำคัญ: สูง · trace: AC-06 / VR-01 / ERR_QUOTA (emptyText) / XT-02
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**
- ชุดข้อมูล: B6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ค้นหาโควตา → พิมพ์ "QT-9999" | B6 | dropdown แสดงข้อความว่าง **ไม่พบ Quota หรือสถานะไม่เป็น verified** (emptyText) | ☐ |
| 2 | VERIFY section เลือกแปลง + ฟิลด์แบบสำรวจ | — | section เลือกแปลง **ยังไม่ปรากฏ** (ไม่มี quota ที่เลือก) · ฟิลด์แบบสำรวจ **ยัง locked** | ☐ |
| 3 | ลบคำค้น พิมพ์ "สุรพล" | — | dropdown พบ **QT-2569-002 · สุรพล เก่งการไร่** (ค้นด้วยชื่อได้ · verified) | ☐ |
| 4 | VERIFY (assertion): seed มีแต่โควตา verified 4 ตัว | — | ค้น "QT-2569" → ขึ้นครบ 4 (QT-001..004) · การกรอง non-verified เป็น code-path (`verifiedQuotas`) → ทดสอบ record waiting จริงที่ SIT (ดู TC-X01) | ☐ |

### TC-C04 — แปลง/รอบปลูก cascade เฉพาะของสายบน · dead-end (AC-01 / VR-02 / XT-02)
- group: C · ความสำคัญ: สูงสุด · trace: AC-01 / VR-02 / BR-AGS-01 / LOCK-03 / EC-02
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**
- ผ่านเมื่อ: plot list = ของโควตา · crop list = ของแปลง · แปลงที่ไม่มีรอบปลูก → ทางตัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-002 · สุรพล เก่งการไร่** → CLICK ช่องเลือกแปลง | — | dropdown แสดง **2 แปลง: PLT-2569-003, PLT-2569-004** (เฉพาะของ QT-002) · **ไม่มี** PLT ของโควตาอื่น · help "(2 แปลง)" | ☐ |
| 2 | เลือก **PLT-2569-003** → CLICK ช่องเลือกรอบปลูก | — | dropdown แสดง **CRP-2569-0000003 เท่านั้น (1 รอบปลูก)** (cropsForPlot กรอง plot_id) · help "(1 รอบปลูก)" | ☐ |
| 3 | CLICK **เปลี่ยนแปลง** → เลือก **PLT-2569-004** → CLICK ช่องเลือกรอบปลูก | — | dropdown แสดง **CRP-2569-0000007 เท่านั้น** (ของ PLT-004) | ☐ |
| 4 | CLICK **เปลี่ยนโควตา** → เลือก **QT-2569-004** → เลือกแปลง **PLT-2569-007** → CLICK เลือกรอบปลูก | — | help/empty **ไม่พบรอบปลูกของแปลงนี้** (PLT-007 มี 0 รอบปลูก — cascade ทางตัน) · ฟิลด์ยัง locked | ☐ |

### TC-C05 — Submit ก่อนครบ cascade → block (negative — AC-06 / EC-01)
- group: C · ความสำคัญ: สูง · trace: AC-06 / BR-AGS-01 / VR-01 / "กรุณาเลือกโควตา แปลง และรอบปลูกก่อน"
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**
- ชุดข้อมูล: B7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไม่เลือกอะไร → CLICK ปุ่ม **ยืนยันสร้าง** ทันที | B7 | ไม่บันทึก + toast เตือน **กรุณาเลือกโควตา แปลง และรอบปลูกก่อน** — ไม่มีแบบสำรวจใหม่ | ☐ |
| 2 | เลือก quota QT-2569-001 + plot PLT-2569-001 (ไม่เลือกรอบปลูก) → CLICK **ยืนยันสร้าง** | — | block เดิม **กรุณาเลือกโควตา แปลง และรอบปลูกก่อน** (crop ยังไม่ครบ) | ☐ |
| 3 | VERIFY count ตาราง (หลังปิด drawer) | — | ยัง 8 รายการ | ☐ |

### TC-C06 — ปีผลิต (พ.ศ.) นอกช่วง 2500-2600 (negative — VR-03 / LOCK-04)
- group: C · ความสำคัญ: สูง · trace: VR-03 / EC-03 / "ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600"
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A (QT-001/PLT-001/CRP-001) → กรอกฟิลด์ครบ
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "2400" → ช่อง **ปีผลิต (พ.ศ.)** → CLICK **ยืนยันสร้าง** | B1 | ข้อความแดงใต้ช่องปี **ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600** + กรอบช่องแดง + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | แก้เป็น "2569" → CLICK **ยืนยันสร้าง** → WAIT | — | error หาย → บันทึกสำเร็จ toast **สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]** | ☐ |
| 3 | (ตรวจ empty) เปิดสร้างใหม่ → เลือก cascade → เว้นช่องปีว่าง → ยืนยันสร้าง | — | ข้อความแดง **กรุณากรอกปีผลิต พ.ศ.** | ☐ |

### TC-C07 — Agronomic dropdowns (สีดิน/สีใบ/โรค + พันธุ์) (happy — AC-04 / LOCK-04)
- group: C · ความสำคัญ: สูง · trace: AC-04 / agronomic enums
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown **พันธุ์อ้อย** | — | ตัวเลือก 5 ค่า: **ขอนแก่น 3 / LK92-11 / K88-92 / อู่ทอง 12 / กำแพงแสน 01** | ☐ |
| 2 | CLICK dropdown **สีดิน** | — | ตัวเลือก: **ดำ / น้ำตาล / แดง / เทา / อื่นๆ** → เลือก น้ำตาล | ☐ |
| 3 | CLICK dropdown **การตรวจสีใบ** | — | ตัวเลือก: **ปกติ / เหลือง / เขียวเข้ม / อื่นๆ** → เลือก ปกติ | ☐ |
| 4 | CLICK dropdown **พบโรค/ศัตรูพืช** | — | ตัวเลือก: **ไม่พบ / น้อย / ปานกลาง / มาก** → เลือก ไม่พบ | ☐ |
| 5 | VERIFY: สีดิน/สีใบ/โรค ไม่บังคับ (ไม่มี *) · พันธุ์บังคับ (มี *) | — | เว้น สีดิน/สีใบ/โรค ว่างได้ · เว้นพันธุ์ → error "กรุณาเลือกพันธุ์อ้อย" | ☐ |

### TC-C08 — ประมาณการผลผลิตติดลบ · อนุญาต 0 (negative/edge — AC-03 / VR-04)
- group: C · ความสำคัญ: สูง · trace: AC-03 / VR-04 / EC-03 / "กรุณาใส่ค่าที่ถูกต้อง"
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A → กรอกฟิลด์อื่นครบ
- ชุดข้อมูล: B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "-5" → ช่อง **ประมาณการผลผลิต (ตัน)** → CLICK **ยืนยันสร้าง** | B2 | ข้อความแดง **กรุณาใส่ค่าที่ถูกต้อง** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | แก้เป็น "0" → CLICK **ยืนยันสร้าง** → WAIT | — | **อนุญาต** (yield ≥ 0) → บันทึกสำเร็จ toast **สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]** | ☐ |
| 3 | (ตรวจ empty) เปิดใหม่ → เลือก cascade → เว้นผลผลิตว่าง → ยืนยันสร้าง | — | ข้อความแดง **กรุณากรอกประมาณการผลผลิต** | ☐ |

### TC-C09 — ขนาดแปลง (ไร่) ต้อง > 0 (negative — AC-03 / VR-04)
- group: C · ความสำคัญ: สูง · trace: AC-03 / VR-04 / EC-03 (plot_size ≤ 0)
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A → กรอกฟิลด์อื่นครบ
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "0" → ช่อง **ขนาดแปลง (ไร่)** → CLICK **ยืนยันสร้าง** | B3 | ข้อความแดง **กรุณาใส่ค่าที่ถูกต้อง** (size > 0 · 0 ไม่ผ่าน — ต่างกับ yield ที่ ≥ 0) | ☐ |
| 2 | แก้เป็น "12.50" → CLICK **ยืนยันสร้าง** → WAIT | — | บันทึกสำเร็จ toast **สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]** | ☐ |
| 3 | (ตรวจ empty) เปิดใหม่ → เลือก cascade → ลบขนาดแปลงให้ว่าง → ยืนยันสร้าง | — | ข้อความแดง **กรุณากรอกขนาดแปลง** | ☐ |

### TC-C10 — required ครบชุด (negative — AC-02b / VR-03)
- group: C · ความสำคัญ: สูง · trace: AC-02b / VR-03 / ERR_CASCADE_INVALID
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A (ปลดล็อกฟิลด์) → **ล้างวันที่/ผู้สำรวจ/พันธุ์ให้ว่าง**
- ชุดข้อมูล: B4, B5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ลบ **วันที่สำรวจ** และ **ผู้สำรวจ** ให้ว่าง · ไม่เลือก **พันธุ์อ้อย** → CLICK **ยืนยันสร้าง** ทันที | B4, B5 | ไม่บันทึก + error ครบ: **กรุณาระบุวันที่สำรวจ / กรุณาระบุผู้สำรวจ / กรุณาเลือกพันธุ์อ้อย** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | VERIFY ช่อง **สีดิน / การตรวจสีใบ / พบโรค/ศัตรูพืช / พิกัด** | — | ไม่มี error (optional) | ☐ |

### TC-C11 — แนบรูป 4 หมวด + ลบ (AC-05 / LOCK-06 / BR-AGS-06)
- group: C · ความสำคัญ: กลาง · trace: AC-05 / photos 4 หมวด (field/crop/stalk/soil)
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section **รูปภาพประกอบ (4 หมวด)** | — | 4 การ์ด: **รูปกับแปลง / รูปพืชผล / รูปลำต้นในกอ / รูปสีดิน** แต่ละอันมีปุ่ม **แนบรูป** + pill นับ 0 | ☐ |
| 2 | CLICK **แนบรูป** ในหมวด **รูปพืชผล** 2 ครั้ง | — | toast **จำลองแนบรูป รูปพืชผล (JPG/PNG ≤5MB)** แต่ละครั้ง · pill หมวดรูปพืชผล = 2 · รายการ 2 ไฟล์ survey_crop_1/2_*.jpg | ☐ |
| 3 | CLICK **แนบรูป** ในหมวด **รูปสีดิน** 1 ครั้ง | — | toast **จำลองแนบรูป รูปสีดิน...** · pill หมวดรูปสีดิน = 1 (แยกต่อหมวด) | ☐ |
| 4 | CLICK ปุ่ม X ลบไฟล์แรกในหมวด **รูปพืชผล** | — | เหลือ 1 ไฟล์ในหมวดรูปพืชผล · pill = 1 · หมวดอื่นไม่กระทบ | ☐ |

### TC-C12 — Double-click กันสร้างซ้ำ (edge — EC-11 / BR-AGS-10)
- group: C · ความสำคัญ: สูง · trace: EC-11 / BR-AGS-10 (idempotency + double-submit guard)
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ** → เลือก cascade ชุด A → กรอกฟิลด์ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งเร็วที่สุด (double-click) | — | คลิกแรกปุ่มกลายเป็น **กำลังบันทึก…** + disabled — คลิกที่สองไม่มีผล (f.submitting guard) | ☐ |
| 2 | WAIT จน toast → VERIFY ตาราง | — | มีแบบสำรวจใหม่ **1 รายการเท่านั้น** (count = 9 รายการ, ไม่ใช่ 10) | ☐ |

---
## Group I — CSV Import (OV-05 — 9-col schema · ทุกแถว waiting_for_verify)

### TC-I01 — ดาวน์โหลดแม่แบบ + modal (9 คอลัมน์)
- group: I · ความสำคัญ: สูง · trace: US-03 / schema = create
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Upload CSV** | — | modal หัวข้อ **นำเข้าแบบสำรวจจากไฟล์ CSV** + subtitle ".csv (UTF-8) ≤5MB · ทุกแถวสถานะ \"รอตรวจสอบ\" · โควตา/แปลง/รอบปลูกต้องผูกถูกต้อง" | ☐ |
| 2 | VERIFY แถบดาวน์โหลด + คำแนะนำ | — | แถบ **ดาวน์โหลดแม่แบบ CSV (schema = create)** + ปุ่ม **ดาวน์โหลดแม่แบบ** · คำแนะนำ "header ตรงแม่แบบ 9 คอลัมน์ · UTF-8 · โควตาต้อง verified · แปลงเป็นของเจ้าของโควตา + verified · รอบปลูกเป็นของแปลง" + "วันที่สำรวจ YYYY-MM-DD · ปี พ.ศ. 2500-2600 · ผลผลิต ≥ 0 · ขนาดแปลง > 0" | ☐ |
| 3 | CLICK **ดาวน์โหลดแม่แบบ** | — | ได้ไฟล์ `survey_template.csv` — header 9 คอลัมน์: quota_id,plot_id,crop_id,survey_date,surveyor,production_year_be,cane_variety,yield_estimate,plot_size_rai + 2 แถวตัวอย่าง (UTF-8 BOM — ไทยไม่เพี้ยน) | ☐ |
| 4 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ยังไม่เลือกไฟล์) | ☐ |

### TC-I02 — Import แถวผสม → partial success + error report (happy — AC-14/16 / EC-10)
- group: I · ความสำคัญ: สูง · trace: AC-14, AC-16 / BR-AGS-07 / LOCK-09 · ทุกแถว waiting
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=`survey_mixed.csv` (5 แถว: 3 ดี + ปี 2400 + ผลผลิต -5)
- Start: OPEN `#/surveys` → CLICK **Upload CSV**
- ผ่านเมื่อ: แถวดีสร้างครบ + แถวเสียรายงาน download ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD survey_mixed.csv | — | ชื่อไฟล์ + ขนาด (KB) แสดงข้างปุ่ม | ☐ |
| 2 | VERIFY สรุปผลตรวจ (preview — ก่อนเขียน) | — | 3 chip: **แถวทั้งหมด 5** · **ผ่าน 3** · **ไม่ผ่าน 2** | ☐ |
| 3 | VERIFY ตาราง "รายละเอียดข้อผิดพลาด (แถวเสียจะถูกข้าม)" | — | 2 แถว: "แถว 5" production_year_be **ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600** · "แถว 6" yield_estimate **กรุณาใส่ค่าที่ถูกต้อง (≥ 0)** | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันนำเข้า (3 แถว)** → WAIT | — | ปุ่มเป็น **กำลังนำเข้า…** → phase done: chip แถวทั้งหมด 5 / **สร้างสำเร็จ 3** / **ล้มเหลว 2** + toast **นำเข้าแบบสำรวจ 3 รายการสำเร็จ — ข้าม 2 แถว** | ☐ |
| 5 | CLICK ปุ่ม **ดาวน์โหลดรายงาน** | — | ได้ไฟล์ `survey-upload-errors.csv` มี 2 แถว error (header "แถว,ฟิลด์,ข้อผิดพลาด,ข้อมูล") | ☐ |
| 6 | CLICK **ปิด** → VERIFY ตาราง | — | แบบสำรวจใหม่ 3 แถว ทุกแถว pill เหลือง **รอตรวจสอบ** · count = **11 รายการ** | ☐ |

### TC-I03 — File guard: นามสกุล + ขนาด (negative — AC-17)
- group: I · ความสำคัญ: สูง · trace: AC-17 / ERR_CSV_INVALID
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=`notes.xlsx`, `survey_too_large.csv`
- Start: OPEN `#/surveys` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD notes.xlsx | — | toast แดง **ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV** — ไฟล์ไม่ถูกรับ | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD survey_too_large.csv | — | toast แดง **ขนาดไฟล์ต้องไม่เกิน 5MB** — ไฟล์ไม่ถูกรับ, ปุ่มยืนยันยัง disabled | ☐ |

### TC-I04 — Header ไม่ตรงแม่แบบ → reject ทั้งไฟล์ (edge — AC-15 / EC-09)
- group: I · ความสำคัญ: สูง · trace: AC-15 / EC-09 / LOCK-09
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=`survey_badheader.csv` (ขาดคอลัมน์ plot_size_rai)
- Start: OPEN `#/surveys` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD survey_badheader.csv | — | ไม่ขึ้น preview + ข้อความแดงใต้ช่องไฟล์ **คอลัมน์ไฟล์ไม่ตรงแม่แบบ: plot_size_rai** (หรือ "จำนวนคอลัมน์ไม่ถูกต้อง (8/9)") + toast แดง **ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ** | ☐ |
| 2 | VERIFY ตารางหลังปิด modal | — | ไม่มีแถวใดถูกสร้าง (count ยัง 8 รายการ) | ☐ |

### TC-I05 — แถว cascade invalid รายแถว (edge — AC-16 / EC-10)
- group: I · ความสำคัญ: สูง · trace: AC-16 / VR-01/02/04 / XT-02
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=`survey_badbind.csv`
- Start: OPEN `#/surveys` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD survey_badbind.csv (แถว2 plot owner mismatch · แถว3 crop ไม่ใช่ของ plot) | — | preview: ผ่าน 1 / ไม่ผ่าน 2 — "แถว 3" plot_id **ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ** (PLT-003 เป็นของ QT-002 ไม่ใช่ QT-001) · "แถว 4" crop_id **ไม่พบรอบปลูกของแปลงที่ระบุ** (CRP-003 ไม่ใช่ของ PLT-001) | ☐ |
| 2 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | enabled = **ยืนยันนำเข้า (1 แถว)** (มี validRows 1) | ☐ |
| 3 | CLICK **ยืนยันนำเข้า (1 แถว)** → WAIT | — | phase done: สร้างสำเร็จ 1 / ล้มเหลว 2 + toast **นำเข้าแบบสำรวจ 1 รายการสำเร็จ — ข้าม 2 แถว** | ☐ |

### TC-I06 — ไฟล์ถูกทั้งหมด → ทุกแถว waiting (happy — AC-14 / BR-AGS-03)
- group: I · ความสำคัญ: กลาง · trace: AC-14 / LOCK-09 / ทุกแถว waiting_for_verify
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=`survey_ok.csv` (3 แถวถูก)
- Start: OPEN `#/surveys` → CLICK **Upload CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD survey_ok.csv | — | preview: ผ่าน 3 / ไม่ผ่าน 0 + แถบ **ทุกแถวผ่านการตรวจสอบ ไม่มีข้อผิดพลาด** | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (3 แถว)** → WAIT | — | phase done: สร้างสำเร็จ 3 + แถบ **นำเข้าสำเร็จทั้งหมด ไม่มีข้อผิดพลาด · ทุกแถวสถานะ "รอตรวจสอบ"** + toast เขียว **นำเข้าแบบสำรวจ 3 รายการสำเร็จ** (ไม่มี "ข้าม") | ☐ |
| 3 | CLICK **ปิด** → CLICK แบบสำรวจใหม่ → Tab **ประวัติ** | — | event **สร้างแบบสำรวจ** · pill **รอตรวจสอบ** | ☐ |

---

## Group V — ตรวจสอบ / ปฏิเสธ เดี่ยว (OV-03)

### TC-V01 — Verify (ยืนยัน) เดี่ยว (happy — AC-18 / LOCK-08)
- group: V · ความสำคัญ: สูง · trace: AC-18 / US-05 / BR-AGS-04 / feeds Crop (BR-AGS-11)
- Setup: role=ผู้ตรวจสอบ (prototype: user เดียวกดได้) · seed=default (SV-2569-0000004 waiting) · files=—
- Start: OPEN `#/surveys/SV-2569-0000004`
- ผ่านเมื่อ: pill เปลี่ยนเขียว + ประวัติ event ยืนยัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer + ปุ่ม | — | หัวข้อ **SV-2569-0000004** + pill เหลือง **รอตรวจสอบ** + ปุ่ม **แก้ไข / ตรวจสอบ / ยกเลิก/ลบ** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบ** | — | modal **ตรวจสอบแบบสำรวจ** — subtitle "เลือกผลการตรวจสอบ · หากปฏิเสธต้องระบุเหตุผล" + เลขสำรวจ + ผู้สำรวจ + โควตา/แปลง/รอบปลูก + วันที่/พันธุ์/ผลผลิต + radio 2 (ยืนยัน/ปฏิเสธ) | ☐ |
| 3 | CLICK ตัวเลือก **ยืนยัน** | — | ตัวเลือกไฮไลต์เขียว · ปรากฏช่อง **หมายเหตุ (ไม่บังคับ)** | ☐ |
| 4 | CLICK ปุ่ม **ยืนยัน** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast เขียว **ยืนยันเรียบร้อย** + pill ใน drawer/ตารางเปลี่ยนเป็นเขียว **ยืนยันแล้ว** · การ์ดยืนยันแล้ว = 3 | ☐ |
| 6 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ยืนยัน** (จุดเขียว) โดย ธนพล ตรวจสอบ | ☐ |

### TC-V02 — Reject (ปฏิเสธ) ไม่กรอกเหตุผล → block (negative — AC-19 / VR-06 / EC-04)
- group: V · ความสำคัญ: สูงสุด · trace: AC-19 / BR-AGS-04 / ERR_REJECT_NO_REASON / LOCK-08
- Setup: role=ผู้ตรวจสอบ · seed=default (SV-2569-0000006 waiting) · files=—
- Start: OPEN `#/surveys/SV-2569-0000006` → CLICK **ตรวจสอบ**
- ผ่านเมื่อ: กด ปฏิเสธ + เหตุผลว่าง → block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวเลือก **ปฏิเสธ** | — | ไฮไลต์แดง · ปรากฏช่อง **เหตุผลในการปฏิเสธ** มี * (บังคับ) placeholder "กรุณาระบุเหตุผลในการปฏิเสธ..." | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** โดย **ไม่กรอกเหตุผล** | — | **block** + ข้อความแดงใต้ช่องเหตุผล **กรุณากรอกเหตุผลในการปฏิเสธ** + toast เหลืองข้อความเดียวกัน — ไม่เปลี่ยนสถานะ | ☐ |

### TC-V03 — Reject (ปฏิเสธ) พร้อมเหตุผล (happy — AC-20)
- group: V · ความสำคัญ: สูง · trace: AC-20 / LOCK-02
- Setup: role=ผู้ตรวจสอบ · seed=default (SV-2569-0000006 waiting) · files=—
- Start: OPEN `#/surveys/SV-2569-0000006` → CLICK **ตรวจสอบ** → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "พิกัดไม่ตรงแปลง กรุณาสำรวจซ้ำ" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ปฏิเสธเรียบร้อย** (info) + pill แดง **ปฏิเสธ** | ☐ |
| 2 | VERIFY Tab **ข้อมูลสำรวจ** (ท้าย) | — | กล่องแดง **เหตุผลที่ปฏิเสธ: พิกัดไม่ตรงแปลง กรุณาสำรวจซ้ำ** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ปฏิเสธ** (จุดแดง) + note เหตุผล โดย ธนพล ตรวจสอบ | ☐ |

### TC-V04 — ไม่เลือกผลตรวจสอบ (negative)
- group: V · ความสำคัญ: กลาง · trace: BR-AGS-04 / "กรุณาเลือกผลการตรวจสอบ"
- Setup: role=ผู้ตรวจสอบ · seed=default (SV-2569-0000001 waiting) · files=—
- Start: OPEN `#/surveys/SV-2569-0000001` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยัน** ทันที (ยังไม่เลือก radio) | — | ไม่ดำเนินการ + error ใต้ radio **กรุณาเลือกผลการตรวจสอบ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V05 — ปุ่มตรวจสอบซ่อน + checkbox disabled สำหรับ verified/rejected/cancelled (AC-23b)
- group: V · ความสำคัญ: กลาง · trace: AC-23b / BR-AGS-04 / §8 detail actions
- Setup: role=ผู้ตรวจสอบ · seed=default · files=—
- Start: OPEN `#/surveys/SV-2569-0000003` (verified)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบนหัว Detail drawer (SV-003 ยืนยันแล้ว) | — | มี **แก้ไข + ยกเลิก/ลบ** — **ไม่มีปุ่ม ตรวจสอบ** (verified) | ☐ |
| 2 | OPEN `#/surveys/SV-2569-0000007` (rejected) → VERIFY ปุ่ม | — | เช่นเดียวกัน: มี แก้ไข + ยกเลิก/ลบ · ไม่มี ตรวจสอบ | ☐ |
| 3 | กลับ list → VERIFY checkbox แถว SV-003/005/007/008 | — | checkbox จาง กดไม่ได้ (title "เลือกได้เฉพาะรายการรอตรวจสอบ") — verify ซ้ำผ่าน UI ไม่ได้ · ส่วน 409 server = TC-S02 (simulate) | ☐ |

---

## Group B — Bulk verify / reject (OV-03)

### TC-B01 — Bulk เลือกทั้งหมด = เฉพาะ waiting + ยืนยัน (happy — AC-21 / EC-06)
- group: B · ความสำคัญ: สูง · trace: AC-21 / US-07 / BR-AGS-04/09
- Setup: role=ผู้ตรวจสอบ · seed=default (waiting 4) · files=—
- Start: OPEN `#/surveys`
- ผ่านเมื่อ: เลือกทั้งหมดติ๊กเฉพาะ waiting + summary

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checkbox รายแถว | — | แถว ยืนยันแล้ว/ปฏิเสธ/ยกเลิก (SV-003/005/007/008) checkbox จาง กดไม่ได้ · แถว รอตรวจสอบ (001/002/004/006) กดได้ | ☐ |
| 2 | CLICK checkbox หัวตาราง | — | ติ๊กเฉพาะ 4 แถว waiting · โผล่ bulk-bar + ปุ่มหัวเปลี่ยนเป็น **ตรวจสอบที่เลือก (4)** (enabled) | ☐ |
| 3 | CLICK **ตรวจสอบที่เลือก (4)** | — | modal **ตรวจสอบแบบสำรวจ (4 รายการ)** + list "รายการที่เลือก (4 รายการ)" แสดง เลขสำรวจ + ผู้สำรวจ + รอบปลูก ครบ 4 + help "ใช้เหตุผลเดียวกันทุกรายการ (เมื่อเลือก \"ปฏิเสธ\") · ข้ามรายการที่ไม่ใช่สถานะรอตรวจสอบ" | ☐ |
| 4 | CLICK **ยืนยัน** (radio) → CLICK ปุ่ม **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** | ☐ |
| 5 | VERIFY ตาราง + stats | — | ไม่มีแถว pill เหลืองเหลือ · การ์ด **รอตรวจสอบ 0** · **ยืนยันแล้ว 6** · ปุ่มหัวกลับเป็น (0) disabled | ☐ |

### TC-B02 — Bulk Reject = เหตุผลเดียวทุกรายการ (AC-22 / LOCK-08 / VR-06)
- group: B · ความสำคัญ: สูง · trace: AC-22 / BR-AGS-04
- Setup: role=ผู้ตรวจสอบ · seed=default (waiting 4) · files=—
- Start: OPEN `#/surveys` → เลือกทั้งหมด (4 waiting) → CLICK **ตรวจสอบที่เลือก (4)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ปฏิเสธ** โดยไม่กรอกเหตุผล → CLICK **ยืนยัน** | — | block + **กรุณากรอกเหตุผลในการปฏิเสธ** + note "ใช้เหตุผลเดียวกันนี้กับทุกรายการที่เลือก" | ☐ |
| 2 | TYPE "เอกสารประกอบไม่ครบ" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** · ทุกแถวที่เลือก pill แดง **ปฏิเสธ** | ☐ |
| 3 | OPEN แบบสำรวจหนึ่งใน 4 → Tab ข้อมูลสำรวจ | — | กล่อง **เหตุผลที่ปฏิเสธ: เอกสารประกอบไม่ครบ** (เหตุผลเดียวกันทุกใบ) | ☐ |

### TC-B03 — Bulk skip non-waiting / partial (edge — AC-22 / EC-06) (ต้อง simulate)
- group: B · ความสำคัญ: สูง · trace: AC-22 / EC-06 · **prototype: openVerifyModal กรอง ids ให้เหลือเฉพาะ waiting ก่อนเปิด modal — จึง สำเร็จ=ทั้งหมด; per-record conflict = SIT**
- Setup: role=ผู้ตรวจสอบ · seed=default
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) เลือก waiting ทั้งหมด → ยืนยัน → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ N ล้มเหลว 0** (non-waiting ถูกกรองออกก่อนเปิด modal — checkbox disabled) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): บางใบถูก verify โดยผู้อื่นก่อน submit | — | summary "สำเร็จ X ล้มเหลว Y" — ใบที่ status เปลี่ยนแล้วถูกนับ ล้มเหลว (per-record 409 ERR_STATUS_CONFLICT) | ☐ |

---
## Group E — แก้ไข + State machine (OV-02 — LOCK-07)

### TC-E01 — แก้ไขแบบสำรวจ waiting → status คงเดิม + version++ (happy — AC-11)
- group: E · ความสำคัญ: สูง · trace: AC-11 / US-08 / BR-AGS-10
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000001 waiting, เวอร์ชัน 1) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว SV-2569-0000001 | — | drawer eyebrow **แก้ไขแบบสำรวจ** · หัวข้อ **แก้ไข SV-2569-0000001** · sub "สถานะ: รอตรวจสอบ · เวอร์ชัน 1" · **ไม่มี** ช่องค้นหาโควตา/แปลง/รอบปลูก (cascade read-only) · ฟิลด์มีค่าเดิม (ไม่ล็อก) | ☐ |
| 2 | TYPE แก้ช่อง **ประมาณการผลผลิต (ตัน)** เป็น "150.00" | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + แถว SV-001 ยัง pill เหลือง **รอตรวจสอบ** (status คงเดิม) + ผลผลิตในตาราง = 150.00 | ☐ |
| 4 | OPEN `#/surveys/SV-2569-0000001` → Tab **ประวัติ** | — | มี event **แก้ไขข้อมูล** เพิ่มบนสุด · footer "เวอร์ชัน 2" | ☐ |

### TC-E02 — แก้ไข Verified → **กลับ waiting_for_verify** (AC-11b / EC-05 / LOCK-07) ★★
- group: E · ความสำคัญ: สูงสุด · trace: AC-11b / EC-05 / BR-AGS-05 · **KEY behavior — edit verified → reset waiting**
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000005 verified) · files=—
- Start: OPEN `#/surveys/SV-2569-0000005`
- ผ่านเมื่อ: แก้แล้วบันทึก → สถานะ **กลับ รอตรวจสอบ** (ไม่คงเป็น ยืนยันแล้ว)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **แก้ไข** (verified มีปุ่มแก้ไข) | — | drawer แก้ไข · sub "สถานะ: ยืนยันแล้ว · เวอร์ชัน 2" · note warn **แก้ไขแบบสำรวจที่ยืนยันแล้ว บันทึกจะกลับสู่สถานะรอตรวจสอบ** | ☐ |
| 2 | TYPE แก้ช่อง **ประมาณการผลผลิต (ตัน)** เป็น "70.00" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **สีเหลือง (warning) บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ** | ☐ |
| 3 | VERIFY แถว SV-2569-0000005 ในตาราง | — | pill **เปลี่ยนเป็นเหลือง รอตรวจสอบ** (ไม่คงเป็น ยืนยันแล้ว) · การ์ดรอตรวจสอบ 4→5 · ยืนยันแล้ว 2→1 | ☐ |
| 4 | CLICK แถว → Tab **ประวัติ** | — | event บนสุด **แก้ไขข้อมูล** · verified_by ถูกล้าง (กลับ waiting) | ☐ |

### TC-E03 — แก้ไข Rejected → ยังคง ปฏิเสธ + reject_reason คงอยู่
- group: E · ความสำคัญ: สูง · trace: AC-11 / BR-AGS-05 (rejected ≠ verified — ไม่ reset) / §5.2
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000007 rejected) · files=—
- Start: OPEN `#/surveys/SV-2569-0000007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Tab ข้อมูลสำรวจ | — | pill แดง **ปฏิเสธ** + กล่อง **เหตุผลที่ปฏิเสธ: ประมาณการผลผลิตสูงผิดปกติเมื่อเทียบกับขนาดแปลง และพบโรค/ศัตรูพืชระดับมาก กรุณาสำรวจซ้ำ** | ☐ |
| 2 | CLICK **แก้ไข** → TYPE แก้ **ประมาณการผลผลิต** เป็น "260.00" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** (ไม่ใช่ "กลับสู่สถานะรอตรวจสอบ" — reset เฉพาะ verified) · pill ยังแดง **ปฏิเสธ** | ☐ |
| 3 | OPEN `#/surveys/SV-2569-0000007` → Tab ข้อมูลสำรวจ | — | กล่อง **เหตุผลที่ปฏิเสธ** ยังคงอยู่ (reject_reason ไม่ถูกเคลียร์ตอน edit) | ☐ |

### TC-E04 — cascade read-only บนหน้า edit (AC-13 / LOCK-03)
- group: E · ความสำคัญ: สูง · trace: AC-13 / BR-AGS-01 · quota/plot/crop immutable on edit
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000003) · files=—
- Start: OPEN `#/surveys` → CLICK ดินสอแถว SV-2569-0000003

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Section 0 ของ drawer แก้ไข | — | **ไม่มี** ช่องค้นหาโควตา/เลือกแปลง/เลือกรอบปลูก (ไม่มี cascade UI ตอน edit) — เข้าฟิลด์ข้อมูลพื้นฐาน/พืชผลได้เลย | ☐ |
| 2 | VERIFY ฟิลด์ที่แก้ได้ | — | แก้ได้เฉพาะ วันที่/ผู้สำรวจ/ปี/พันธุ์/ผลผลิต/ขนาด/สีดิน/สีใบ/โรค/พิกัด/รูปภาพ — quota_id/plot_id/crop_id ไม่มี input ให้แก้ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): ยิง PUT เปลี่ยน quota_id/plot_id/crop_id | — | server reject (immutable — BR-AGS-01) แม้ UI ไม่มีช่อง | ☐ |

### TC-E05 — แก้ไขแล้วปีนอกช่วง → block (negative — VR-03 บน edit)
- group: E · ความสำคัญ: กลาง · trace: VR-03 / EC-03 (validate ทำงานบน edit ด้วย)
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000001) · files=—
- Start: OPEN `#/surveys` → CLICK ดินสอแถว SV-2569-0000001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE แก้ **ปีผลิต (พ.ศ.)** เป็น "3000" → CLICK **บันทึกการแก้ไข** | — | ไม่บันทึก + ข้อความแดง **ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | แก้กลับเป็น "2569" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** | ☐ |

---

## Group D — ยกเลิก / ลบ (soft — OV-04 — LOCK-10)

### TC-D01 — ยกเลิก (cancelled) + reason บังคับ (happy — AC-26)
- group: D · ความสำคัญ: สูง · trace: AC-26 / BR-AGS-08 / VR-06 / US-09
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000004 waiting) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า การ์ด **สำรวจทั้งหมด** และ **รอตรวจสอบ** | — | บันทึก: ทั้งหมด=8, รอตรวจสอบ=4 (อ้างใน step 6) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว SV-2569-0000004 | — | modal **ยกเลิก/ลบแบบสำรวจ?** + subtitle `แบบสำรวจ "SV-2569-0000004 — อารยา สวนอ้อย"` + radio **ยกเลิก (cancelled) — ยังคงอยู่ในรายการ สถานะ "ยกเลิก"** (default) / **ลบ (deleted) — ซ่อนจากรายการ (soft delete)** + ช่อง **เหตุผล *** + note info "รายการจะเปลี่ยนเป็นสถานะ \"ยกเลิก\" และยังคงแสดงในรายการ" | ☐ |
| 3 | คง radio **ยกเลิก** → CLICK **ยกเลิกแบบสำรวจ** โดยไม่กรอกเหตุผล | — | **block** + ข้อความแดง **กรุณากรอกเหตุผล** + toast เดียวกัน | ☐ |
| 4 | TYPE "เกษตรกรขอยกเลิกการสำรวจ" → เหตุผล → CLICK **ยกเลิกแบบสำรวจ** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast **ยกเลิกแบบสำรวจแล้ว** + แถว SV-004 **ยังอยู่ในตาราง** pill เทา **ยกเลิก** (soft — คงในรายการ) | ☐ |
| 6 | VERIFY stats | — | สำรวจทั้งหมด=7 (cancelled ไม่รวมใน all — filter status≠deleted แต่ all.length นับ status≠cancelled? ตรวจ: การ์ดสำรวจทั้งหมด = ไม่รวมยกเลิก/ลบ → 7) · รอตรวจสอบ=3 | ☐ |

### TC-D02 — ลบ (deleted) → soft delete ซ่อนจาก list + deep-link (AC-27 / EC-12)
- group: D · ความสำคัญ: สูง · trace: AC-27 / BR-AGS-08 / EC-12 / ERR_NOT_FOUND
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000006 waiting) · files=—
- Start: OPEN `#/surveys` → CLICK ถังขยะ แถว SV-2569-0000006

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK radio **ลบ (deleted)** | — | note เปลี่ยนเป็นแดง **รายการจะถูกซ่อนจากรายการ (soft delete) และบันทึกลงประวัติ** · ปุ่มเปลี่ยนเป็น **ลบแบบสำรวจ** | ☐ |
| 2 | TYPE "ข้อมูลผิด สร้างซ้ำ" → เหตุผล → CLICK **ลบแบบสำรวจ** → WAIT | — | toast **ลบแบบสำรวจแล้ว** + แถว SV-006 **หายจากตาราง** · count = 7 รายการ | ☐ |
| 3 | OPEN `#/surveys/SV-2569-0000006` (route ตรง) | — | ไม่เปิด detail — toast **ไม่พบข้อมูลแบบสำรวจที่เลือก** + เด้งกลับ `#/surveys` (deleted ถูกซ่อน) | ☐ |

### TC-D03 — ยกเลิก/ลบ จาก Detail drawer (ทุกสถานะ) (AC-27)
- group: D · ความสำคัญ: กลาง · trace: AC-27 / BR-AGS-08 · **หมายเหตุ: ในตาราง ถังขยะเฉพาะแถว waiting; ปุ่ม ยกเลิก/ลบ อยู่ใน Detail drawer สำหรับทุกสถานะ**
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000003 verified) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **การดำเนินการ** แถว SV-2569-0000003 (ยืนยันแล้ว) ในตาราง | — | มีเฉพาะไอคอนดินสอ — **ไม่มีถังขยะ** (list ลบเฉพาะ waiting) | ☐ |
| 2 | CLICK แถว SV-2569-0000003 → VERIFY ปุ่มหัว Detail drawer | — | มี **แก้ไข + ยกเลิก/ลบ** (drawer อนุญาตทุกสถานะ · ไม่มี ตรวจสอบ เพราะ verified) | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก/ลบ** → radio **ลบ** → TYPE เหตุผล → CLICK **ลบแบบสำรวจ** → WAIT | — | toast **ลบแบบสำรวจแล้ว** + drawer ปิด + แถว SV-003 หาย · การ์ดยืนยันแล้ว = 1 | ☐ |

### TC-D04 — cancelled คงในรายการ + refresh reset (AC-26)
- group: D · ความสำคัญ: กลาง · trace: AC-26 / §8 (cancelled soft) / mock reset
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000008 cancelled ใน seed) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT filter สถานะ = **ยกเลิก** | — | เหลือ 1 แถว SV-2569-0000008 pill เทา **ยกเลิก** — ยืนยัน cancelled คงแสดงในรายการ (ต่าง deleted ที่ซ่อน) | ☐ |
| 2 | CLICK แถว → Tab ข้อมูลสำรวจ | — | กล่อง **เหตุผลที่ยกเลิก: สำรวจซ้ำซ้อนกับแบบสำรวจอื่นในรอบปลูกเดียวกัน** | ☐ |
| 3 | PRESS F5 (refresh) | — | mock reset → seed กลับมา 8 แบบสำรวจ (in-memory) — ยืนยัน refresh = reset (ทุกเคส independent) | ☐ |

---
## Group W — Detail / 3 tabs / รูปภาพ 4 หมวด / ประวัติ (P-02)

### TC-W01 — Detail ข้อมูลสำรวจ + snapshot card (AC-24 / BR-AGS-02)
- group: W · ความสำคัญ: สูง · trace: AC-24 / US-04 / BR-AGS-02 / LOCK-04/05
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000001) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว SV-2569-0000001 | — | Detail drawer: eyebrow "แบบสำรวจ · QT-2569-001 · PLT-2569-001 · CRP-2569-0000001" + หัวข้อ **SV-2569-0000001** (mono) + pill เหลือง **รอตรวจสอบ** | ☐ |
| 2 | VERIFY snapshot card (ใต้หัว, ส้มอ่อน) | — | "โควตา · แปลง · รอบปลูก · เกษตรกร" → **โควตา QT-2569-001 · แปลง PLT-2569-001 · รอบปลูก CRP-2569-0000001 · สมหญิง รักดี** + ปุ่ม **ดูรอบปลูก** | ☐ |
| 3 | VERIFY Tab **ข้อมูลสำรวจ** | — | กลุ่ม **ข้อมูลพื้นฐาน** (วันที่สำรวจ/ผู้สำรวจ ภาคภูมิ เดินดง/ปีผลิต 2569) · กลุ่ม **ข้อมูลพืชผล** (พันธุ์อ้อย ขอนแก่น 3/ผลผลิต 145.50/ขนาดแปลง 12.50/สีดิน น้ำตาล/สีใบ ปกติ/โรค ไม่พบ/พิกัด 14.023145,99.512088) | ☐ |
| 4 | VERIFY footer drawer | — | "อัปเดตล่าสุด … · เวอร์ชัน N" + ปุ่ม **ปิด** | ☐ |

### TC-W02 — Tab รูปภาพ 4 หมวด + snapshot ดูรอบปลูก (AC-05 / AC-25)
- group: W · ความสำคัญ: กลาง · trace: AC-05, AC-25 / BR-AGS-06 / cross-module read-only (mock toast)
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000001 photos: field1 crop2 stalk1 soil1) · files=—
- Start: OPEN `#/surveys/SV-2569-0000001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **รูปภาพ** | — | หัวข้อ **รูปภาพประกอบ (4 หมวด)** · 4 หมวด: **รูปกับแปลง** (pill 1, sv_001_field_1.jpg) · **รูปพืชผล** (pill 2, sv_001_crop_1/2.jpg) · **รูปลำต้นในกอ** (pill 1) · **รูปสีดิน** (pill 1) — แต่ละไฟล์มี link **ดาวน์โหลด** | ☐ |
| 2 | CLICK link ดาวน์โหลดไฟล์ในหมวด รูปกับแปลง | — | toast info **จำลองดาวน์โหลด sv_001_field_1.jpg** | ☐ |
| 3 | VERIFY หมวดที่ไม่มีรูป (เปิด SV อื่น เช่น SV-0000006 รูปลำต้น/สีดิน = 0) | — | หมวดว่างแสดง **ยังไม่มีรูปในหมวดนี้** (dashed box) | ☐ |
| 4 | CLICK ปุ่ม **ดูรอบปลูก** (snapshot card) | — | toast info **จำลองเปิดหน้ารอบปลูก CRP-2569-0000001** (READ-ONLY — deep-link จริงตอน deploy รวม features) | ☐ |

### TC-W03 — Tab ข้อมูลสำรวจ ของ verified + verify note (AC-24)
- group: W · ความสำคัญ: กลาง · trace: AC-24 / statusLabel verified
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000003 verified) · files=—
- Start: OPEN `#/surveys/SV-2569-0000003`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว + snapshot | — | pill เขียว **ยืนยันแล้ว** · snapshot "โควตา QT-2569-002 · แปลง PLT-2569-003 · รอบปลูก CRP-2569-0000003 · สุรพล เก่งการไร่" | ☐ |
| 2 | VERIFY Tab ข้อมูลสำรวจ | — | พันธุ์อ้อย LK92-11 · ผลผลิต 280.00 · ขนาดแปลง 25.00 · สีดิน ดำ · ไม่มีกล่อง reject/cancel (verified) | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | timeline: **ตรวจสอบ — ยืนยัน** (จุดเขียว · note "ข้อมูลครบถ้วน พิกัดตรงแปลง" · โดย ธนพล ตรวจสอบ) → **สร้างแบบสำรวจ** (โดย สมพร วงศ์ทะเบียน) | ☐ |

### TC-W04 — Tab ประวัติ (audit timeline) เต็มวงจร (AC-25 / BR-AGS-09)
- group: W · ความสำคัญ: สูง · trace: AC-25 / BR-AGS-08/09 / audit append-only
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-2569-0000007 rejected · SV-2569-0000008 cancelled) · files=—
- Start: OPEN `#/surveys/SV-2569-0000007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **ประวัติ** | — | timeline เรียงใหม่→เก่า: **ตรวจสอบ — ปฏิเสธ** (จุดแดง + note reject_reason + โดย ธนพล ตรวจสอบ) → **สร้างแบบสำรวจ** (โดย สมพร วงศ์ทะเบียน + note "ผูกโควตา QT-2569-002 · แปลง PLT-2569-003 · รอบปลูก CRP-2569-0000003") — ทุกรายการมีวันเวลา | ☐ |
| 2 | OPEN `#/surveys/SV-2569-0000008` → CLICK Tab **ประวัติ** | — | timeline: **ยกเลิกแบบสำรวจ** (จุดเหลือง + note cancel_reason) → **สร้างแบบสำรวจ** | ☐ |

### TC-W05 — Deep-link refresh-safe + missing (AC-25b / EC-12)
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / refresh-safe / ERR_NOT_FOUND
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys/SV-2569-0000003` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/surveys/SV-2569-0000003` | — | หน้า list โหลด + Detail drawer **SV-2569-0000003** เปิดเองทันที | ☐ |
| 2 | PRESS F5 (refresh ทั้งหน้า) | — | กลับมาที่เดิม — drawer SV-2569-0000003 ยังเปิด (refresh-safe · mountViewDrawer จาก route) | ☐ |
| 3 | OPEN `#/surveys/SV-2569-9999999` (ไม่มีในระบบ) | — | toast แดง **ไม่พบข้อมูลแบบสำรวจที่เลือก** + เด้งกลับ `#/surveys` (ไม่มี drawer) | ☐ |

---
## Group X — Cross-module: cascade read + feeds Crop + 1 crop:N surveys ⭐ (06_TESTS §6.9)

> Survey อ่าน Quota→Plot→Crop ผ่าน `QUOTAS`/`PLOTS`/`CROPS` + `verifiedQuotas`/`plotsForQuota`/`cropsForPlot` — **ไม่มี write-back** · survey **verified** ป้อนเข้า Crop (F-AGM-004) แท็บสำรวจ (pull-read) · reconcile ไป Crop feature จริง = `(ต้อง simulate)` ที่ SIT

### TC-X01 — Quota search คืนเฉพาะ verified (XT-02)
- group: X · ความสำคัญ: สูงสุด · trace: XT-02 / AC-01 / VR-01 / BR-AGS-01 / LOCK-03
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ค้นหาโควตา → พิมพ์ "QT-2569" | — | dropdown แสดง **4 โควตา** (QT-2569-001..004 — verified ทุกตัว) · option = `[QT] · [ชื่อ]` + sub `[เบอร์] · [เลขบัตร masked]` | ☐ |
| 2 | CLICK **QT-2569-004 · ประนอม ใจเพชร** | — | help "แสดงเฉพาะแปลงที่ยืนยันแล้วของเจ้าของโควตานี้ (2 แปลง)" · farmer snapshot = ประนอม ใจเพชร (0833334444 · 4-XXXX-XXXX-XX-3, read-only) | ☐ |
| 3 | VERIFY (assertion + SIT): seed มีแต่ verified quota | — | `verifiedQuotas()` กรอง status='verified' · seed ไม่มี quota waiting → ทดสอบ record waiting จริง (ควรถูกตัดออก + emptyText "ไม่พบ Quota หรือสถานะไม่เป็น verified") ที่ SIT | ☐ |

### TC-X02 — สร้าง survey ผูก cascade → snapshot ตรง · source ไม่ถูกแก้ (XT-01) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-02 / BR-AGS-02 / §0.14 no write-back
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-004 · ประนอม ใจเพชร** + **PLT-2569-006** + **CRP-2569-0000005** → กรอกฟิลด์ครบ → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]** · แถวใหม่ แสดง QT-2569-004, PLT-2569-006, CRP-2569-0000005 (snapshot จาก cascade) | ☐ |
| 2 | CLICK แถวใหม่ → VERIFY Tab ข้อมูลสำรวจ + snapshot | — | snapshot "โควตา QT-2569-004 · แปลง PLT-2569-006 · รอบปลูก CRP-2569-0000005 · ประนอม ใจเพชร" · ขนาดแปลง auto = 6.00 ไร่ (จาก PLT-006) — ตรงต้นทาง | ☐ |
| 3 | พิสูจน์ READ-ONLY: CLICK **สร้างแบบสำรวจ** อีกครั้ง → เลือก **QT-2569-004** → **PLT-2569-006** → **CRP-2569-0000005** | — | ยังเลือกได้ตามปกติ (ไม่ขึ้น "ถูกใช้แล้ว" — Quota/Plot/Crop array ไม่ถูก mutate · ไม่มี has_survey flag) — 1 crop : N surveys | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | เปิด Quota/Plot/Crop record ก่อน/หลังผูก = **ไม่มี field/สถานะที่เปลี่ยน** (read-only ENG-EXT-AGM GET only) | ☐ |

### TC-X03 — cascade filter: plot ของโควตา · crop ของแปลง (XT-02) ★ signature
- group: X · ความสำคัญ: สูงสุด · trace: XT-02 / AC-01 / VR-02 / BR-AGS-01 / LOCK-03
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default · files=—
- Start: OPEN `#/surveys` → CLICK **สร้างแบบสำรวจ**
- ผ่านเมื่อ: plot list กรอง owner+verified · crop list กรอง plot

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-001 · สมหญิง รักดี** → CLICK เลือกแปลง | — | dropdown = **PLT-2569-001, PLT-2569-002 (2 แปลง)** · **ไม่มี** PLT ของโควตาอื่น (plotsForQuota กรอง quota_id + verified) · help "(2 แปลง)" — 1 quota : N plots | ☐ |
| 2 | เลือก **PLT-2569-001** → CLICK เลือกรอบปลูก | — | dropdown = **CRP-2569-0000001, CRP-2569-0000002 (2 รอบปลูก)** (cropsForPlot กรอง plot_id) — 1 plot : N crops · help "(2 รอบปลูก)" | ☐ |
| 3 | CLICK **เปลี่ยนแปลง** → เลือก **PLT-2569-002** → CLICK เลือกรอบปลูก | — | dropdown = **CRP-2569-0000006 เท่านั้น** (ของ PLT-002) — พิสูจน์ cascade กรองตามแปลง | ☐ |

### TC-X04 — survey verified feeds Crop สำรวจ tab (XT-03 / BR-AGS-11) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-03 / BR-AGS-11 / §0.14 · D-03 Drift · **prototype: feeds Crop = ระบุใน comment (Crop pull-read) — cross-app จริงตอน deploy รวม features → SIT**
- Setup: role=เจ้าหน้าที่สำรวจ · **simulate — ระบบจริง:** F-AGM-004 Crop detail แท็บ สำรวจ
- Start: — (SIT — deploy รวม Survey + Crop)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) OPEN `#/surveys/SV-2569-0000003` (verified) | — | pill **ยืนยันแล้ว** · การ์ด stats "ยืนยันแล้ว" meta "ป้อนเข้าแท็บสำรวจของรอบปลูก" (ระบุ intent) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): เปิด Crop F-AGM-004 `#/crops/CRP-2569-0000003` → Tab **สำรวจ** | — | แสดงแบบสำรวจ **SV-2569-0000003 (verified เท่านั้น)** · read-only (Crop pull-read survey verified) · waiting/rejected ไม่ปรากฏ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): survey ที่ยัง waiting/rejected | — | **ไม่** ป้อนเข้าแท็บสำรวจของ Crop (เฉพาะ verified feeds) | ☐ |

### TC-X05 — 1 รอบปลูก : N แบบสำรวจ (XT-04)
- group: X · ความสำคัญ: สูง · trace: XT-04 / AC-02 / "สำรวจรอบปลูกเดิมได้หลายครั้ง"
- Setup: role=เจ้าหน้าที่สำรวจ · seed=default (SV-0000001 & SV-0000002 บน CRP-2569-0000001) · files=—
- Start: OPEN `#/surveys`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "CRP-2569-0000001" → ช่องค้นหา | — | เหลือ 2 แถว: SV-2569-0000001 + SV-2569-0000002 (ทั้งคู่ผูกรอบปลูกเดียวกัน — 1 crop : N surveys) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** → CLICK **สร้างแบบสำรวจ** → เลือก **QT-001 → PLT-001 → CRP-2569-0000001** (รอบปลูกเดิม) | — | การ์ดรอบปลูกที่เลือก note **สำรวจรอบปลูกเดิมได้หลายครั้ง (1 รอบปลูก : หลายแบบสำรวจ)** · เลือกได้ปกติ (ไม่ block ว่ามีสำรวจแล้ว) | ☐ |
| 3 | กรอกฟิลด์ครบ → CLICK **ยืนยันสร้าง** → WAIT → TYPE "CRP-2569-0000001" ค้นหา | — | toast สร้างสำเร็จ · ค้นรอบปลูกเดิม → เหลือ **3 แถว** (survey ที่ 3 บน CRP-001) — สำรวจซ้ำรอบสำเร็จ | ☐ |

---

## Group S — System / simulate (optimistic lock · concurrency · SoD · deep-link)

### TC-S01 — Optimistic lock stale edit → 409 (edge — AC-12 / EC-07) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-12 / EC-07 / ERR_STALE / BR-AGS-10 · **prototype single-session ทำไม่ได้ (Drift D-04) — SIT case · idempotency double-click ตรวจแล้วใน TC-C12**
- Setup: **simulate — ระบบจริง:** 2 sessions — A แก้ record + save ก่อน, B ที่เปิดค้างไว้ save ทีหลังด้วย expected_version เก่า
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B กด **บันทึกการแก้ไข** หลัง A save ไปแล้ว | — | 409 + toast แดง **ข้อมูลล้าสมัย กรุณารีเฟรช** — ข้อมูลของ A ไม่ถูกทับ | ☐ |

### TC-S02 — Concurrent verify status changed → 409 (edge — AC-23b / EC-08) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-23b / EC-08 / ERR_STATUS_CONFLICT · **prototype UI ซ่อนปุ่มตรวจสอบสำหรับ verified/rejected (TC-V05) — ส่วน 409 server = SIT**
- Setup: **simulate — ระบบจริง:** A verify record ก่อน, B verify record เดิม (status เปลี่ยนแล้ว)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B POST verify กับ record ที่ A เพิ่ง verify | — | 409 + **สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช** — สถานะที่ A ตั้งไว้คงเดิม | ☐ |

### TC-S03 — survey_id sequence race + server-side validation (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: BR-AGS-10 · **survey_id format SV-2569-000000N · nextSurveyCode ฝั่ง client (prototype); atomic sequence + race = server**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): 2 request สร้างแบบสำรวจพร้อมกัน (race) | — | server atomic sequence → survey_id ไม่ชนกัน (SV-2569-000000N unique) · idempotency-key กัน duplicate | ☐ |
| 2 | VERIFY (ระบบจริง): UI ผ่าน แต่ payload year/yield/size ผิด (bypass) | — | server reject validation (ปี 2500-2600 / yield ≥ 0 / size > 0) แม้ UI ปล่อยผ่าน · CSV partial → orphan photo cleanup | ☐ |

### TC-S04 — SoD + RBAC hide (OQ-SV5) (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: §5.3 SoD/permission matrix · **prototype ไม่มี role switching — เจ้าหน้าที่สำรวจ/ผู้ตรวจสอบเป็น user เดียว — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง:** feature flag SoD + RBAC
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — RBAC): login เป็น เจ้าหน้าที่สำรวจ | — | ปุ่ม **ตรวจสอบ / ตรวจสอบที่เลือก** ถูกซ่อน (verify = ผู้ตรวจสอบเท่านั้น) | ☐ |
| 2 | VERIFY (ระบบจริง — SoD flag ON): ผู้ตรวจสอบ verify แบบสำรวจที่ตนเองสร้าง | — | block 403 + ข้อความ SoD (ผู้สร้างไม่ควรตรวจสอบเอง) · flag OFF → ผ่านแต่ log anomaly | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `survey-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed 8 แบบสำรวจ + 4 โควตา + 7 แปลง + 7 รอบปลูก (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/UPLOAD/PRESS/WAIT/VERIFY)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast มุมขวาล่าง · create/edit 0.6s · verify 0.7s · cancel/delete 0.55s · import 0.9s — อ่านทันทีที่โผล่ · toast แสดง 4–4.8s)
5. **cascade 3-level บังคับ:** ทุกเคสสร้าง/negative ที่ต้องกรอกฟิลด์แบบสำรวจ ต้อง **เลือกครบ โควตา (verified) → แปลง (ของโควตา + verified) → รอบปลูก (ของแปลง)** ก่อน (ฟิลด์ล็อกจนครบทั้งสาม) — ยกเว้นเคสที่ทดสอบ gating เอง (TC-C02/C03/C04/C05)
6. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
7. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"
8. ไฟล์ทดสอบทั้งหมด (CSV/xlsx) ต้องอยู่ในโฟลเดอร์ที่ agent เข้าถึงได้ก่อนเริ่ม (ดู Data Sets → Files) · header CSV = 9 คอลัมน์ `quota_id,plot_id,crop_id,survey_date,surveyor,production_year_be,cane_variety,yield_estimate,plot_size_rai`
9. จบทุกเคส → กรอก Result Report ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 28 / 28 (AC-01..28 รวม AC-02b/11b/23b/25b) |
| Cross-Module (XT-01..04) | 4 / 4 (XT-03 feeds Crop = simulate) |
| Business rules (BR-AGS-01..11) | 11 / 11 |
| Validation (VR-01..06) | 6 / 6 |
| Edge cases (EC-01..12) | 12 / 12 (EC-07/08 simulate) |
| Error codes (UI-observable) | 11 / 11 (ERR_STALE / ERR_STATUS_CONFLICT = simulate) |
| Permission cells | เจ้าหน้าที่สำรวจ / ผู้ตรวจสอบ allow ครบ · RBAC deny / SoD = TC-S04 (simulate) |
| Scope Lock (LOCK-01..11) | 11 / 11 — ทุก LOCK มีเคส verify |

- **Manifest cross-check (FRD §0.12): ✅ 10 Stories + 11 Rules + 6 VR + 12 EC + 4 XT + 11 LOCK — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT (6 เคส)
- TC-L07 (export CSV — ไม่มี UI ใน prototype)
- TC-B03 (bulk skip non-waiting per-record conflict)
- TC-X04 (survey verified feeds Crop — cross-app deploy รวม features)
- TC-S01 (optimistic lock 409 — single session)
- TC-S02 (concurrent verify 409)
- TC-S03 (survey_id sequence race + server validation)
- TC-S04 (SoD / RBAC — ไม่มี role switching)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-006",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 56, "pass": 0, "fail": 0, "blocked": 0 }
}
```

---

## v1.1 Recheck Additions (F-AGM-006 · crosscheck กับ FRD/Stage-10/tables/Testcase/AS-BUILT ใหม่)

เพิ่ม 6 เคส หลัง crosscheck พบว่า prototype เดิมขาดพาเนลอากรอนอมิก (agronomic panel) ที่สเปคผู้มีอำนาจ (FRD Create form + AS-BUILT create-survey-drawer) กำหนดไว้ — ได้แก้ prototype ให้ครบแล้ว:

| เคส | กลุ่ม | สิ่งที่ทดสอบ | anchor |
|---|---|---|---|
| TC-C13 | สร้าง | ประเภทอ้อย + เดือนปลูก + อายุอ้อยคำนวณอัตโนมัติ (FN-AT-CROP-192) | create_drawer |
| TC-C14 | สร้าง | การวัดขนาดอ้อย: ระยะร่อง/ความสูง หัว-กลาง-ท้าย/ปล้อง/เส้นผ่าน/ลำต่อกอ/กอ 10ม. | create_drawer |
| TC-C15 | สร้าง | ดิน/สภาพแปลง/โรค: ชนิดดิน · วัชพืช · พบโรค + รายละเอียด | create_drawer |
| TC-E07 | แก้ไข | แก้ฟิลด์การวัดขนาดอ้อยแล้วบันทึก (พาเนลครบเหมือนสร้าง) | edit_drawer |
| TC-W08 | Landing | หน้ารายละเอียดแสดงพาเนลอากรอนอมิกครบ | view_drawer |
| TC-L12 | รายการ | ปุ่ม Export CSV ตามตัวกรอง (ฝั่งหน้าจอ · backend Pending Spec ตาม TC-606) | list_actions |

หมายเหตุ reconciliation:
- prototype เดิมมีเฉพาะ subset (survey_date, surveyor, ปีผลิต, พันธุ์อ้อย, ประมาณการผลผลิต, ขนาดแปลง, สีดิน, สีใบ, ระดับโรค, พิกัด, รูป 4 หมวด) → เพิ่มพาเนลเต็มตาม FRD+AS-BUILT
- ฟิลด์ tonnage ภายในชื่อ yield_estimate เปลี่ยน label เป็น “ปริมาณรวม (ตัน)” map → total_tons (บังคับ ≥0)
- surveyor (ผู้สำรวจ) map → recorder (บังคับ) · relabel “ผู้สำรวจ (ผู้บันทึก)”
- Export backend = Pending Spec (TC-606) — prototype ทำ client-side export
