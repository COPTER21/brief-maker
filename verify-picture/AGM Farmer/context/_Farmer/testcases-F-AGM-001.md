# AI Test Cases — F-AGM-001 Farmer Member Management (จัดการสมาชิกเกษตรกร)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `farmer-member-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ HTML + UI Brief แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side/role) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-001 (AGM/Farmer — WKN) |
| App entry | เปิดไฟล์ `farmer-member-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/members` (list — default) · `#/members/:member_id` (view drawer, refresh-safe) |
| ที่มา | FRD_F-AGM-001_Pack (7 ไฟล์) · BRD APPROVED · HTML v1.0 (audit FAIL=0) · UI_BRIEF_F-AGM-001 |
| จำนวนเคส | 51 เคส / 10 groups (45 เดิม + 6 recheck 2026-07-22) |
| Scope Lock | LOCK-01..08 (00_OVERVIEW §0.11) — ทุกข้อมีเคส verify (ดู Ledger) |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า = ข้อมูล reset กลับ seed 16 รายการ — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม |

**Seed ตั้งต้น (ใน prototype — หลัง refresh):** 16 รายการ = รอตรวจสอบ 7 (FM-000004/005/006/009/010/013/015) · อนุมัติแล้ว 7 (FM-000001/002/007/008/012/014/016) · ปฏิเสธ 2 (FM-000003 note "เลขบัตรประชาชนไม่ตรงกับสำเนาที่แนบ", FM-000011 note "ที่อยู่ไม่ตรงกับทะเบียนบ้าน") · Pending ค้าง > 7 วัน 4 รายการ · **quota_status = `no_quota` ทุก record** (authoritative — has_quota ถอด seed แล้ว 2026-07-22, เป็น Phase-2)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L — รายการ/ค้นหา/กรอง | TC-L01..L07 (7) | สูง |
| C — สร้างสมาชิก | TC-C01..C09 (9) | สูง |
| I — CSV Import | TC-I01..I08 (8) | สูง |
| V — ตรวจสอบยืนยัน | TC-V01..V06 (6) | สูง |
| E — แก้ไข + State machine | TC-E01..E06 (6) | สูง |
| D — ลบ (soft) | TC-D01..D03 (3) | สูง |
| W — รายละเอียด/ประวัติ | TC-W01..W04 (4) | กลาง |
| P — Permission/SoD | TC-P01 (1 + ledger ข้ามพร้อมเหตุผล) | กลาง |
| K — Concurrency/Idempotency | TC-K01..K02 (2 + C09) | สูง |
| PF — Performance | TC-PF01 (1) | กลาง |
| Recheck additions (2026-07-22) | TC-L08, TC-V07, TC-V08, TC-I09, TC-K02, TC-PF01 (6 — GAP-05/07/09/10/11) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1 ← BRD §7)
| item | cases |
|---|---|
| AC-01/02 สร้าง happy + member_id + pending เสมอ | TC-C01, TC-C02 |
| AC-03 citizen ≠ 13 หลัก | TC-C03 |
| AC-04 cascade reset (EC-08/VR-11) | TC-C07 |
| AC-05 postal auto + validate | TC-C07 (auto) · server-side match → TC-I06 (CSV รายแถว) |
| AC-06/07 citizen ซ้ำ form/CSV (EC-07) | TC-C08, TC-I02 |
| AC-08..11 CSV partial success / guard / all-valid | TC-I02, TC-I03, TC-I07 |
| AC-12/13 ค้นหา debounce + empty state | TC-L02, TC-L03 |
| AC-14..16 verify เดี่ยว approve/reject/not-pending | TC-V01, TC-V02, TC-V03, TC-V06 |
| AC-17/18 bulk verify + selectable (EC-06/12) | TC-L04, TC-V05 |
| AC-19 re-submit อัตโนมัติ (LOCK-06) | TC-E02 |
| AC-20 แก้ approved คงสถานะ (LOCK-07) | TC-E03, TC-E04 |
| AC-21/22 ลบ pending / guard | TC-D01, TC-D02, TC-D03 |
| AC-23/24 detail 3 กลุ่ม + masking | TC-W01, TC-L06 |
| AC-25 optimistic lock CONFLICT | TC-K01 (ต้อง simulate — server-side) |
| AC-26 idempotency double-click | TC-C09 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-AGM-01 member_id FM-%06d ต่อเนื่อง | TC-C02 |
| BR-AGM-02 เริ่ม pending เสมอ | TC-C02, TC-I02 |
| BR-AGM-03 verify เฉพาะ pending | TC-V06 |
| BR-AGM-04 reject ต้องมีเหตุผล | TC-V02 |
| BR-AGM-05 ลบเฉพาะ pending + soft | TC-D01..D03 |
| BR-AGM-06 optimistic lock + idempotency | TC-K01, TC-C09 |
| BR-AGM-07 CSV .csv ≤5MB header 10 คอลัมน์ | TC-I03, TC-I04 |
| BR-AGM-08 partial success + error report | TC-I02 |
| BR-AGM-09 postal auto + match | TC-C07, TC-I06 |
| BR-AGM-10 citizen unique ต่อ tenant | TC-C08, TC-I02 |
| BR-AGM-11 re-submit (LOCK-06) | TC-E02, TC-E06 |
| BR-AGM-12 approved แก้ได้ + Immutable Log | TC-E03, TC-E04 |
| BR-AGM-13 quota_status read-only | TC-W04 |
| BR-AGM-14 DOA placeholder | — ข้าม (backend field placeholder — ไม่มีผลบน UI Phase 1, OQ-01) |

### Validation (05_RULES §5.4 VR-01..11)
| VR | cases |
|---|---|
| VR-01 citizen 13 หลัก | TC-C03 |
| VR-02 phone 9–12 หลัก | TC-C04 |
| VR-03 email required + format (authoritative — LOCK-08 superseded) | TC-C05 |
| VR-04 required set | TC-C06 |
| VR-05 citizen unique | TC-C08 |
| VR-06 ต้องเลือกผลตรวจสอบ | TC-V04 |
| VR-07 note บังคับเมื่อ reject | TC-V02 |
| VR-08 CSV file guard | TC-I03 |
| VR-09 postal match ตำบล | TC-C07 (auto), TC-I06 (mismatch รายแถว) |
| VR-10 optimistic lock message | TC-K01 (ต้อง simulate) |
| VR-11 cascade reset | TC-C07 |

### Edge Cases (05_RULES §5.5 — ☑ บังคับ + ☐ recommended)
| EC | cases / สถานะ |
|---|---|
| EC-01 ☑ verify/edit ชนกัน | TC-K01 (ต้อง simulate) |
| EC-02 ☑ ลบรายการยืนยันแล้ว | TC-D02, TC-D03 |
| EC-03 ☑ reject ไม่ใส่เหตุผล | TC-V02 |
| EC-04 ☑ CSV บางแถวพัง | TC-I02 |
| EC-05 ☑ ค้นหาไม่เจอ | TC-L03 |
| EC-06 ☑ เลือกทั้งหมด = เฉพาะ pending | TC-L04 |
| EC-07 ☑ citizen ซ้ำ | TC-C08, TC-I02 |
| EC-08 ☑ เปลี่ยนจังหวัด reset ลูกโซ่ | TC-C07 |
| EC-09 ☐ encoding ไม่ใช่ UTF-8 | TC-I08 (ต้อง simulate — client mock อ่าน UTF-8; ระบบจริง reject ทั้งไฟล์) |
| EC-10 ☐ header ไม่ตรง | TC-I04 |
| EC-11 ☐ ซ้ำภายในไฟล์ | TC-I05 |
| EC-12 ☐ bulk บางรายการถูก verify ก่อน | TC-V05 (ต้อง simulate) |
| EC-13 ☐ ตำบลสะกดผิด | TC-I06 |
| EC-14 ☐ re-submit วนหลายรอบ | TC-E06 |
| EC-15 ☐ self-verify (SoD) | TC-P01 (ต้อง simulate — feature flag/role) |
| EC-16 ☐ double-click บันทึก | TC-C09 |

### Error catalog (05_RULES §5.6 — ที่มีผลบน UI prototype)
| error | cases |
|---|---|
| ERR_VALIDATION_FAILED (รายช่อง) | TC-C03..C06, TC-V02, TC-V04 |
| BR_CITIZEN_ID_DUPLICATE | TC-C08 |
| BR_POSTAL_CODE_MISMATCH | TC-I06 |
| BR_VERIFY_NOT_PENDING | TC-V06 |
| BR_DELETE_NOT_PENDING | TC-D03 |
| BR_CSV_HEADER_MISMATCH | TC-I04 |
| ERR_CSV_INVALID_FILE | TC-I03 |
| ERR_CSV_ENCODING | TC-I08 (simulate) |
| ERR_STALE_DATA | TC-K01 (simulate) |
| ERR_SOD_SELF_VERIFY | TC-P01 (simulate) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / ERR_NOT_FOUND / ERR_INSUFFICIENT_ROLE / ERR_NOT_AUTHENTICATED / ERR_EMPTY_SELECTION | — ข้าม (server/auth-level — ไม่มีเส้นทางบน prototype; ERR_EMPTY_SELECTION ถูกกันด้วยปุ่ม disabled → TC-L04 ตรวจ) |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases / สถานะ |
|---|---|
| R-01 สร้าง/แก้/ลบ/Import = allow | TC-C01, TC-E01, TC-D01, TC-I02 (prototype user เดียว) |
| R-02 verify เดี่ยว/กลุ่ม = allow | TC-V01, TC-V05 |
| R-01 verify = deny · R-02 สร้าง/แก้/ลบ/Import = deny | — ข้าม (Drift D-04: prototype ไม่มี role switching — ทดสอบที่ระบบจริงผ่าน ENC; UI จริงต้องซ่อนปุ่มตาม §5.3) |
| SoD self-verify block | TC-P01 (simulate) |

### Cross-Module (06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 Quota ผูกได้เฉพาะ approved + มี quota ลบไม่ได้ | Quota | TC-W04 (โครงสร้าง: ลบได้เฉพาะ pending → TC-D02 พิสูจน์ทาง) — module Quota ยังไม่มี (ต้อง simulate ตอน SIT) |
| XT-02 แก้ citizen_id หลัง approved → anomaly | การเงิน | TC-E04 |
| XT-03 quota_status read-only แสดงบน detail | Quota → feature นี้ | TC-W04 |
| XT-04 soft-deleted ไม่นับ list/stats | รายงาน | TC-D01 (step ตรวจ stats) |

### Scope Lock (00_OVERVIEW §0.11)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | capability legacy 100% | ทั้ง suite — ตัวแทน: TC-C01, TC-I02, TC-V01, TC-V05, TC-E01, TC-D01, TC-W01, TC-L02 |
| LOCK-02 | state machine pending→approved/rejected + soft delete | TC-V01, TC-V03, TC-D01, TC-V06 |
| LOCK-03 | optimistic lock + idempotency ทุก mutation | TC-K01, TC-C09 |
| LOCK-04 | CSV 10 คอลัมน์ + partial success + error report | TC-I01, TC-I02, TC-I04 |
| LOCK-05 | governance additions (masking/history) | TC-L06, TC-W02 |
| LOCK-06 | rejected → แก้+บันทึก → pending อัตโนมัติ | TC-E02, TC-E06 |
| LOCK-07 | approved แก้ได้ทุก field สถานะคงเดิม | TC-E03, TC-E04 |
| LOCK-08 | email optional ⚠️ superseded → email **required** (authoritative) | TC-C05 |

### UI States
| item | cases |
|---|---|
| loaded / filtered / filter-empty / all-empty | TC-L02, TC-L03 (all-empty: — ข้าม, seed 16 รายการ ลบหมดไม่ได้ใน prototype — เช็คผ่าน filter-empty แทน) |
| stats widgets (Pending ค้าง >7 วัน) | TC-L01 |
| sort / pagination footer | TC-L05, TC-L07 |
| submitting state (ปุ่ม "กำลัง…") | TC-C01, TC-V01, TC-D01, TC-I02 (step WAIT) |

**Manifest cross-check (FRD §0.12):** Stories 8/8 · Rules R01–R14 14/14 (R14 ข้ามมีเหตุผล) · VR 11/11 · EC ☑ 8/8 + ☐ 8/8 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — สมาชิกใหม่ถูกต้องครบ (happy)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ชื่อ | ทดสอบ |
| นามสกุล | ระบบใหม่ |
| เลขบัตรประชาชน | 1103700123456 |
| เบอร์โทรศัพท์ | 0891234567 |
| อีเมล | test.member@example.com *(required — authoritative, LOCK-08 optional superseded)* |
| ที่อยู่ | 99/1 หมู่ 2 บ้านทดสอบ |
| จังหวัด | กาญจนบุรี |
| อำเภอ | ท่าม่วง |
| ตำบล | วังขนาย *(รหัสไปรษณีย์ต้องเติมอัตโนมัติ = 71110)* |

### ชุด B — ค่าผิดสำหรับ negative
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | เลขบัตรประชาชน | `12345` (5 หลัก) | เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก |
| B2 | เบอร์โทรศัพท์ | `08123` (5 หลัก) | เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก |
| B3 | อีเมล | `invalid-email` | รูปแบบอีเมลไม่ถูกต้อง |
| B4 | เลขบัตรประชาชน | `3710100234561` (ซ้ำกับ FM-000001 สมชาย ใจดี) | เลขบัตรประชาชนนี้มีในระบบแล้ว (FM-000001) |

### ไฟล์ทดสอบ (Files) — runner ต้องเตรียมก่อนรัน (header ตาม LOCK-04)
> header ทุกไฟล์ (ยกเว้นที่ระบุ): `first_name,last_name,citizen_id,phone,email,address,province,district,subdistrict,postal_code` (คอลัมน์ที่ 6 = `address` ตาม authoritative — map DB `address_line`)

| ชื่อไฟล์ | เนื้อหา |
|---|---|
| `members_ok.csv` | 3 แถวถูกทั้งหมด — citizen 4403700000011/22/33 · จังหวัด กาญจนบุรี/ท่าม่วง/วังขนาย (postal เว้นว่าง = ให้ระบบเติม 71110) |
| `members_mixed.csv` | 6 แถว: 4 ถูก (citizen 4403700000101..104, ที่อยู่ กาญจนบุรี/ท่ามะกา/ท่ามะกา) + แถว 3 citizen `999` (12 หลักไม่ครบ) + แถว 5 phone `081` |
| `members_dupfile.csv` | 3 แถว: แถว 2 กับแถว 3 ใช้ citizen เดียวกัน `4403700000201` |
| `members_dupdb.csv` | 2 แถว: แถวแรก citizen `3710100234561` (ซ้ำ FM-000001 ในระบบ) + แถวสอง citizen ใหม่ `4403700000301` |
| `members_badsub.csv` | 2 แถว: แถวแรก subdistrict `วังขนายย` (สะกดผิด) · แถวสอง postal `99999` กับตำบล วังขนาย (mismatch) |
| `members_badheader.csv` | header ขาดคอลัมน์ `email` (เหลือ 9 คอลัมน์) + 1 แถวข้อมูลถูก |
| `members_too_large.csv` | ไฟล์ .csv ขนาด > 5MB (gen แถวซ้ำจนเกิน) |
| `members_tis620.csv` | เนื้อหาถูกแต่ encode TIS-620 (ภาษาไทยไม่ใช่ UTF-8) |
| `notes.xlsx` | ไฟล์ Excel ใด ๆ (ทดสอบ guard นามสกุลไฟล์) |

---

## Test Cases

## Group L — รายการ / ค้นหา / กรอง

### TC-L01 — เปิดหน้า list + stats widgets (happy)
- group: L · ความสำคัญ: สูง · trace: 01_UI P-01 / BRD §18.2 / UI state loaded
- actor (role): R-01
- Setup: role=R-01 (default prototype) · seed=default 16 รายการ (refresh หน้า) · files=—
- Start: OPEN `#/members`
- ผ่านเมื่อ: หน้า list + สถิติ 4 การ์ดแสดงเลขตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/members` | — | หัวข้อ **จัดการสมาชิกเกษตรกร** + badge **16 รายการ** · breadcrumb "เกษตรกรรม / จัดการสมาชิกเกษตรกร" | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **สมาชิกทั้งหมด 16** · **รอตรวจสอบ 7** (meta ส้ม "ค้างเกิน 7 วัน 4 รายการ") · **อนุมัติแล้ว 7** · **ปฏิเสธ 2** | ☐ |
| 3 | VERIFY ปุ่มบน page header (ขวาบน) | — | เรียงซ้าย→ขวา: **Import CSV** · **ตรวจสอบที่เลือก (0)** (disabled) · **สร้างสมาชิก** (ปุ่มแดง ขวาสุด) | ☐ |
| 4 | VERIFY ตาราง | — | 8 คอลัมน์: ☐, MEMBER ID, ชื่อ, นามสกุล, เบอร์โทรศัพท์, เลขบัตรประชาชน, สถานะการยืนยัน, การดำเนินการ | ☐ |
| 5 | VERIFY footer ตาราง | — | ข้อความ **1 – 16 จาก 16 รายการ** | ☐ |

### TC-L02 — ค้นหา (debounce) + กรองสถานะ (happy)
- group: L · ความสำคัญ: สูง · trace: AC-12 / US-03 / LOCK-01
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`
- ผ่านเมื่อ: ค้นได้ทั้ง ชื่อ/นามสกุล/เบอร์/เลขบัตร/Member Id + filter สถานะทำงาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "สมชาย" → ช่องค้นหา (placeholder **ค้นหาชื่อ นามสกุล เบอร์โทร เลขบัตร Member Id**) | สมชาย | รอ ~0.5s ตารางเหลือ 1 แถว: FM-000001 สมชาย ใจดี | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ช่องค้นหาว่าง + ตารางกลับมา 16 รายการ | ☐ |
| 3 | TYPE "0823456789" → ช่องค้นหา | เบอร์ | เหลือแถว FM-000002 สมหญิง รักดี | ☐ |
| 4 | CLICK ปุ่ม **ล้างตัวกรอง** แล้ว TYPE "FM-000011" | Member Id | เหลือแถว FM-000011 มะลิ หอมหวาน (pill แดง **ปฏิเสธ**) | ☐ |
| 5 | CLICK ปุ่ม **ล้างตัวกรอง** → SELECT "รอตรวจสอบ" → dropdown สถานะ | รอตรวจสอบ | เหลือ 7 แถว ทุกแถว pill เหลือง **รอตรวจสอบ** · footer "1 – 7 จาก 7 รายการ" | ☐ |
| 6 | SELECT "ปฏิเสธ" → dropdown สถานะ | ปฏิเสธ | เหลือ 2 แถว (FM-000003, FM-000011) pill แดง | ☐ |

### TC-L03 — ค้นหาไม่เจอ → empty state (edge: EC-05)
- group: L · ความสำคัญ: กลาง · trace: AC-13 / EC-05
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีชื่อนี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state: **ไม่พบรายการที่ค้นหา** + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty state) | — | ตารางกลับมา 16 รายการ | ☐ |

### TC-L04 — เลือกทั้งหมด = เฉพาะแถวรอตรวจสอบ (edge: EC-06)
- group: L · ความสำคัญ: สูง · trace: AC-17 / EC-06 / ERR_EMPTY_SELECTION (กันด้วยปุ่ม disabled)
- Setup: role=R-01 · seed=default (pending 7) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checkbox รายแถว | — | แถวสถานะ **อนุมัติแล้ว/ปฏิเสธ** checkbox จาง กดไม่ได้ · แถว **รอตรวจสอบ** กดได้ | ☐ |
| 2 | VERIFY ปุ่ม **ตรวจสอบที่เลือก (0)** | — | disabled (กดไม่ได้) | ☐ |
| 3 | CLICK checkbox หัวตาราง | — | ติ๊กเฉพาะแถว pending ทั้ง 7 · โผล่แถบเข้ม "**เลือก 7 รายการ (รอตรวจสอบ)**" + ปุ่มหัวเปลี่ยนเป็น **ตรวจสอบที่เลือก (7)** (enabled) | ☐ |
| 4 | CLICK checkbox หัวตารางอีกครั้ง | — | ยกเลิกทั้งหมด → แถบเข้มหาย + ปุ่มกลับเป็น (0) disabled | ☐ |
| 5 | CLICK checkbox แถว FM-000004 | — | เลือก 1 · checkbox หัวตารางเป็นสถานะ partial (ขีดกลาง) | ☐ |

### TC-L05 — Sort คอลัมน์
- group: L · ความสำคัญ: ต่ำ · trace: 01_UI P-01 (sortable) (เพิ่มเติม)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **ชื่อ** | — | แถวเรียงตามชื่อ ก→ฮ | ☐ |
| 2 | CLICK หัวคอลัมน์ **ชื่อ** อีกครั้ง | — | เรียงกลับ ฮ→ก | ☐ |
| 3 | CLICK หัวคอลัมน์ **สถานะการยืนยัน** | — | แถวจัดกลุ่มตามสถานะ | ☐ |

### TC-L06 — Masking เลขบัตรบน list (LOCK-05 / S02-04)
- group: L · ความสำคัญ: สูง · trace: AC-24 / S02-04 / D-CLASS Restricted
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **เลขบัตรประชาชน** ทุกแถวที่เห็น | — | รูปแบบ mask `X-XXXX-XXXX-XX-X` (เห็นเฉพาะหลักแรก+หลักสุดท้าย เช่น `3-XXXX-XXXX-XX-1`) — **ไม่มีแถวไหนโชว์เลขเต็ม 13 หลัก** | ☐ |
| 2 | CLICK แถว FM-000001 | — | view drawer เปิด — ในหัวข้อ **ข้อมูลส่วนตัว** เลขบัตรแสดงเต็มรูปแบบ `3-7101-00234-56-1` (detail ตาม permission) | ☐ |

### TC-L07 — Pagination footer + คลิกแถวเปิด view
- group: L · ความสำคัญ: ต่ำ · trace: 01_UI P-01 / Rule #41 (เพิ่มเติม)
- Setup: role=R-01 · seed=default (16 < 20/หน้า — มีหน้าเดียว) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ pagination | — | ปุ่มหน้า **1** (active สีแดง) · ลูกศรซ้าย/ขวา disabled (หน้าเดียว) | ☐ |
| 2 | CLICK กลางแถว FM-000005 (ไม่โดน checkbox/ไอคอน) | — | view drawer เปิด หัวข้อ **ประยูร ทองแท้** + route เปลี่ยนเป็น `#/members/FM-000005` | ☐ |
| 3 | PRESS Esc | — | drawer ปิด + route กลับ `#/members` | ☐ |

---

## Group C — สร้างสมาชิก (OV-01)

### TC-C01 — สร้างสมาชิกครบถูก (happy — email required)
- group: C · ความสำคัญ: สูง · trace: AC-01 / US-01 / LOCK-01 / VR-04 (email required — authoritative)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`
- ชุดข้อมูล: A
- ผ่านเมื่อ: toast สร้างสำเร็จ + แถวใหม่บนสุดสถานะรอตรวจสอบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างสมาชิก** (แดง ขวาบน) | — | drawer เปิดจากขวา หัวข้อ **สร้างสมาชิกเกษตรกร** · ฟอร์ม 2 กลุ่ม: **ข้อมูลส่วนตัว** / **ที่อยู่** | ☐ |
| 2 | TYPE → ช่อง **ชื่อ** / **นามสกุล** | A | ช่องแสดง "ทดสอบ" / "ระบบใหม่" | ☐ |
| 3 | TYPE → ช่อง **เลขบัตรประชาชน** | A: 1103700123456 | รับเฉพาะตัวเลข แสดงครบ 13 หลัก | ☐ |
| 4 | TYPE → ช่อง **เบอร์โทรศัพท์** | A: 0891234567 | แสดงค่า | ☐ |
| 5 | TYPE → ช่อง **อีเมล** | A: test.member@example.com | แสดงค่า — email เป็น required (authoritative, LOCK-08 superseded) | ☐ |
| 6 | TYPE → ช่อง **ที่อยู่** | A | แสดงค่า | ☐ |
| 7 | CLICK ช่อง **เลือกจังหวัด** → พิมพ์ "กาญ" → CLICK ตัวเลือก **กาญจนบุรี** (มี highlight คำที่พิมพ์) | A | จังหวัด = กาญจนบุรี · ช่องอำเภอเปิดใช้งาน | ☐ |
| 8 | SELECT "ท่าม่วง" → ช่อง **เลือกอำเภอ** · SELECT "วังขนาย" → ช่อง **เลือกตำบล** | A | ตำบลเลือกได้ (แสดงรหัส 71110 ท้ายตัวเลือก) · ช่อง **รหัสไปรษณีย์** เติม **71110** อัตโนมัติ (แก้ไม่ได้ + helper "ระบบกำหนดให้อัตโนมัติจากตำบล") | ☐ |
| 9 | CLICK ปุ่ม **ยืนยันสร้าง** (ล่างขวาของ drawer) | — | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (กดซ้ำไม่ได้) | ☐ |
| 10 | WAIT จน toast ปรากฏ (≤3s) | — | drawer ปิด + toast เขียวขวาล่าง **สร้างสมาชิกสำเร็จ — FM-000017** | ☐ |
| 11 | VERIFY ตาราง | — | แถวบนสุด = ทดสอบ ระบบใหม่ · pill เหลือง **รอตรวจสอบ** · badge นับรายการเป็น **17 รายการ** · การ์ดรอตรวจสอบเพิ่มเป็น 8 | ☐ |

### TC-C02 — member_id ต่อเนื่อง + สถานะเริ่ม pending เสมอ
- group: C · ความสำคัญ: สูง · trace: AC-02 / BR-AGM-01, BR-AGM-02
- Setup: role=R-01 · seed=default (id ล่าสุด FM-000016) · files=—
- Start: OPEN `#/members` (ทำต่อจาก TC-C01 ไม่ได้ — refresh ก่อน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS F5 (refresh) แล้ว OPEN `#/members` | — | seed กลับ 16 รายการ | ☐ |
| 2 | CLICK **สร้างสมาชิก** → กรอกชุด A ครบ → CLICK **ยืนยันสร้าง** → WAIT toast | A | toast ระบุ id = **FM-000017** (running ต่อจาก FM-000016 รูปแบบ FM-%06d) | ☐ |
| 3 | CLICK แถวใหม่บนสุด | — | view drawer: pill **รอตรวจสอบ** · Tab **ประวัติ** มี 1 รายการ "สร้างข้อมูลสมาชิก" | ☐ |

### TC-C03 — เลขบัตร ≠ 13 หลัก (negative — VR-01)
- group: C · ความสำคัญ: สูง · trace: AC-03 / VR-01 / ERR_VALIDATION_FAILED
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "12345" → ช่อง **เลขบัตรประชาชน** แล้ว CLICK ช่องอื่น | B1 | ข้อความแดงใต้ช่อง **เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก** + กรอบช่องแดง | ☐ |
| 2 | TYPE "abc" ต่อในช่องเดิม | — | ตัวอักษรไม่ถูกพิมพ์ลงช่อง (รับเฉพาะตัวเลข) | ☐ |
| 3 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ไม่บันทึก + toast เหลือง **กรุณากรอกข้อมูลให้ครบถ้วน** + error รายช่องอื่นที่ยังว่างแสดงครบ | ☐ |

### TC-C04 — เบอร์โทรผิดรูปแบบ (negative — VR-02)
- group: C · ความสำคัญ: กลาง · trace: VR-02
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "08123" → ช่อง **เบอร์โทรศัพท์** แล้ว CLICK ช่องอื่น | B2 | ข้อความแดง **เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก** | ☐ |
| 2 | TYPE เพิ่มจนเป็น "0812345678" แล้ว CLICK ช่องอื่น | — | ข้อความ error หาย กรอบกลับปกติ | ☐ |

### TC-C05 — email required + validate format (authoritative / VR-03 — LOCK-08 superseded)
- group: C · ความสำคัญ: สูง · trace: VR-03 (email required — authoritative, LOCK-08 optional superseded 2026-07-22)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "invalid-email" → ช่อง **อีเมล** แล้ว CLICK ช่องอื่น | B3 | ข้อความแดง **รูปแบบอีเมลไม่ถูกต้อง** | ☐ |
| 2 | ลบค่าในช่อง **อีเมล** ให้ว่าง แล้ว CLICK ช่องอื่น | — | error แดง **กรุณากรอกอีเมล** (email เป็น required — authoritative, LOCK-08 superseded) | ☐ |
| 3 | แก้ช่อง **อีเมล** เป็น "test.member@example.com" + กรอกชุด A ครบทุกช่องอื่น → CLICK **ยืนยันสร้าง** → WAIT toast | A | บันทึกสำเร็จ toast **สร้างสมาชิกสำเร็จ — FM-000017** (email required ต้องกรอก) | ☐ |

### TC-C06 — required ครบชุด (negative — VR-04)
- group: C · ความสำคัญ: สูง · trace: VR-04
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** ทันที (ไม่กรอกอะไร) | — | ไม่บันทึก + error ครบ: **กรุณากรอกชื่อ / กรุณากรอกนามสกุล / กรุณากรอกเลขบัตรประชาชน / กรุณากรอกเบอร์โทรศัพท์ / กรุณากรอกอีเมล / กรุณากรอกที่อยู่ / กรุณาเลือกจังหวัด / กรุณาเลือกอำเภอ / กรุณาเลือกตำบล** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | VERIFY ช่อง **อีเมล** | — | แสดง error **กรุณากรอกอีเมล** (email เป็น required — authoritative, LOCK-08 superseded) | ☐ |

### TC-C07 — Address cascade + postal auto + reset ลูกโซ่ (edge: EC-08 / VR-09 / VR-11)
- group: C · ความสำคัญ: สูง · trace: AC-04, AC-05 / EC-08 / VR-09, VR-11
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง **เลือกอำเภอ** และ **เลือกตำบล** ก่อนเลือกจังหวัด | — | เป็นสีเทา กดพิมพ์ไม่ได้ (disabled) | ☐ |
| 2 | SELECT "กาญจนบุรี" → **เลือกจังหวัด** | — | ช่องอำเภอเปิดใช้งาน | ☐ |
| 3 | SELECT "ท่าม่วง" → **เลือกอำเภอ** → SELECT "วังขนาย" → **เลือกตำบล** | — | **รหัสไปรษณีย์** = 71110 (อัตโนมัติ, แก้ไม่ได้) | ☐ |
| 4 | SELECT "ราชบุรี" → **เลือกจังหวัด** (เปลี่ยนจังหวัด) | — | ช่อง **อำเภอ / ตำบล / รหัสไปรษณีย์** ถูกเคลียร์ว่างทั้งหมด (reset ลูกโซ่) | ☐ |
| 5 | SELECT "บ้านโป่ง" → อำเภอ → SELECT "ท่าผา" → ตำบล | — | รหัสไปรษณีย์ = 70110 | ☐ |
| 6 | SELECT "โพธาราม" → **เลือกอำเภอ** (เปลี่ยนอำเภอ) | — | **ตำบล + รหัสไปรษณีย์** ถูกเคลียร์ (จังหวัดคงเดิม) | ☐ |

### TC-C08 — เลขบัตรซ้ำในระบบ (negative — EC-07 / VR-05)
- group: C · ความสำคัญ: สูง · trace: AC-06 / EC-07 / BR_CITIZEN_ID_DUPLICATE
- Setup: role=R-01 · seed=default (FM-000001 citizen=3710100234561) · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอกชุด A ครบ แต่ช่อง **เลขบัตรประชาชน** ใช้ค่า B4 | B4: 3710100234561 | — | ☐ |
| 2 | CLICK **ยืนยันสร้าง** | — | ไม่บันทึก + error ใต้ช่องเลขบัตร **เลขบัตรประชาชนนี้มีในระบบแล้ว (FM-000001)** | ☐ |
| 3 | แก้เลขบัตรเป็น 1103700123456 → CLICK **ยืนยันสร้าง** → WAIT toast | — | บันทึกสำเร็จ | ☐ |

### TC-C09 — Double-click กันสร้างซ้ำ (edge: EC-16 / LOCK-03)
- group: C · ความสำคัญ: สูง · trace: AC-26 / EC-16 / BR-AGM-06
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK **สร้างสมาชิก** → กรอกชุด A ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งเร็วที่สุด (double-click) | — | คลิกแรกปุ่มกลายเป็น **กำลังบันทึก…** + disabled — คลิกที่สองไม่มีผล | ☐ |
| 2 | WAIT จน toast ปรากฏ → VERIFY ตาราง | — | มีสมาชิกใหม่ **1 รายการเท่านั้น** (badge = 17 รายการ, ไม่ใช่ 18) | ☐ |

---

## Group I — CSV Import (OV-03 — LOCK-04)

### TC-I01 — ดาวน์โหลดแม่แบบจากใน modal (LOCK-04)
- group: I · ความสำคัญ: สูง · trace: US-02 / API-09 / Rule #32.2
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Import CSV** | — | modal กลางจอ หัวข้อ **นำเข้าสมาชิกจากไฟล์ CSV** + คำอธิบาย ".csv (UTF-8) ไม่เกิน 5MB · คอลัมน์ 10 ช่องตามแม่แบบ · สมาชิกใหม่จะมีสถานะ \"รอตรวจสอบ\" อัตโนมัติ" | ☐ |
| 2 | VERIFY แถบบนใน modal | — | ข้อความ **ดาวน์โหลดแม่แบบ CSV เพื่อดูรูปแบบที่ถูกต้อง** + ปุ่ม **ดาวน์โหลดแม่แบบ** (อยู่ *ใน* modal) | ☐ |
| 3 | CLICK ปุ่ม **ดาวน์โหลดแม่แบบ** | — | ได้ไฟล์ `member-template.csv` — header 10 คอลัมน์: first_name,last_name,citizen_id,phone,email,address,province,district,subdistrict,postal_code + แถวตัวอย่าง 2 แถว (เปิดใน Excel ภาษาไทยไม่เพี้ยน — UTF-8 BOM) | ☐ |
| 4 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ยังไม่ได้เลือกไฟล์) | ☐ |

### TC-I02 — Import แถวผสม → partial success + error report (happy — LOCK-04 / EC-04)
- group: I · ความสำคัญ: สูง · trace: AC-08, AC-09 / EC-04 / BR-AGM-08 / BR-AGM-02
- Setup: role=R-01 · seed=default · files=`members_mixed.csv` (6 แถว: 4 ดี 2 เสีย)
- Start: OPEN `#/members` → CLICK **Import CSV**
- ผ่านเมื่อ: แถวดีสร้างครบ แถวเสียรายงานพร้อม download ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เลือกไฟล์** → UPLOAD members_mixed.csv | — | ชื่อไฟล์ + ขนาดแสดงข้างปุ่ม | ☐ |
| 2 | VERIFY สรุปผลตรวจ (preview — ก่อนเขียนข้อมูล) | — | 3 กล่อง: **แถวทั้งหมด 6** · **ผ่านการตรวจสอบ 4** (เขียว) · **ไม่ผ่าน 2** (แดง) | ☐ |
| 3 | VERIFY ตารางข้อผิดพลาด | — | 2 แถว: ระบุ "แถว N" + ฟิลด์ + ข้อความ (**เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก** / **เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก**) | ☐ |
| 4 | CLICK ปุ่ม **ดาวน์โหลดรายงาน** | — | ได้ไฟล์ `upload-errors.csv` มี 2 แถว error (แถว/ฟิลด์/ข้อผิดพลาด/ข้อมูล) | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันนำเข้า (4 แถว)** | — | ปุ่มเป็น **กำลังนำเข้า…** → สรุปผล: แถวทั้งหมด 6 / **สร้างสำเร็จ 4** / **ล้มเหลว 2** + toast **นำเข้าสมาชิก 4 รายการสำเร็จ — ข้าม 2 แถว** | ☐ |
| 6 | CLICK ปุ่ม **ปิด** → VERIFY ตาราง | — | สมาชิกใหม่ 4 แถวบนสุด ทุกแถว pill เหลือง **รอตรวจสอบ** · badge = **20 รายการ** | ☐ |

### TC-I03 — File guard: นามสกุล + ขนาด (negative — VR-08)
- group: I · ความสำคัญ: สูง · trace: AC-10 / VR-08 / ERR_CSV_INVALID_FILE
- Setup: role=R-01 · seed=default · files=`notes.xlsx`, `members_too_large.csv`
- Start: OPEN `#/members` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD notes.xlsx | — | toast แดง **กรุณาเลือกไฟล์ CSV เท่านั้น** — ไฟล์ไม่ถูกรับ | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD members_too_large.csv | — | toast แดง **ขนาดไฟล์ต้องไม่เกิน 5MB** — ไฟล์ไม่ถูกรับ, ปุ่มยืนยันยัง disabled | ☐ |

### TC-I04 — Header ไม่ตรงแม่แบบ → reject ทั้งไฟล์ (edge: EC-10)
- group: I · ความสำคัญ: สูง · trace: EC-10 / BR_CSV_HEADER_MISMATCH / LOCK-04
- Setup: role=R-01 · seed=default · files=`members_badheader.csv` (ขาดคอลัมน์ email)
- Start: OPEN `#/members` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD members_badheader.csv | — | ไม่ขึ้น preview + error แดงใต้ช่องไฟล์ **คอลัมน์ไฟล์ไม่ตรงแม่แบบ: email** + toast แดง **ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ** | ☐ |
| 2 | VERIFY ตารางหลังปิด modal | — | ไม่มีแถวใดถูกสร้าง (badge ยัง 16 รายการ) | ☐ |

### TC-I05 — เลขบัตรซ้ำภายในไฟล์ (edge: EC-11)
- group: I · ความสำคัญ: กลาง · trace: EC-11
- Setup: role=R-01 · seed=default · files=`members_dupfile.csv` (แถว 2-3 citizen เดียวกัน)
- Start: OPEN `#/members` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD members_dupfile.csv | — | preview: ผ่าน 2 / ไม่ผ่าน 1 — แถวหลังของคู่ซ้ำ error **เลขบัตรประชาชนซ้ำภายในไฟล์ (แถว 3)** (แถวแรกของคู่ผ่าน) | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (2 แถว)** → WAIT | — | สร้างสำเร็จ 2 / ล้มเหลว 1 | ☐ |

### TC-I06 — ตำบลสะกดผิด + postal mismatch (edge: EC-13 / VR-09)
- group: I · ความสำคัญ: กลาง · trace: EC-13 / VR-09 / BR_POSTAL_CODE_MISMATCH · รวม dup-in-DB (B4)
- Setup: role=R-01 · seed=default · files=`members_badsub.csv`, `members_dupdb.csv`
- Start: OPEN `#/members` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD members_badsub.csv | — | ไม่ผ่าน 2: แถวแรก **ไม่พบตำบลในท่าม่วง** (สะกด "วังขนายย") · แถวสอง **รหัสไปรษณีย์ไม่ตรงกับตำบล** (99999 ≠ 71110) | ☐ |
| 2 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ผ่าน 0 แถว) | ☐ |
| 3 | CLICK **เลือกไฟล์** → UPLOAD members_dupdb.csv | — | preview ใหม่: ผ่าน 1 / ไม่ผ่าน 1 — แถวซ้ำ DB error **เลขบัตรประชาชนซ้ำ — มีในระบบแล้ว (FM-000001)** | ☐ |

### TC-I07 — ไฟล์ถูกทั้งหมด + postal เว้นว่างให้ระบบเติม (happy)
- group: I · ความสำคัญ: กลาง · trace: AC-11 / VR-09 (auto)
- Setup: role=R-01 · seed=default · files=`members_ok.csv` (3 แถว postal ว่าง)
- Start: OPEN `#/members` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD members_ok.csv | — | preview: ผ่าน 3 / ไม่ผ่าน 0 + แถบ **ทุกแถวผ่านการตรวจสอบ ไม่มีข้อผิดพลาด** | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (3 แถว)** → WAIT | — | สร้างสำเร็จ 3 + แถบ **อัปโหลดสำเร็จทั้งหมด ไม่มีข้อผิดพลาด** + toast เขียว | ☐ |
| 3 | CLICK **ปิด** → CLICK แถวสมาชิกใหม่คนแรก | — | detail: รหัสไปรษณีย์ = **71110** (ระบบเติมจากตำบลวังขนาย) | ☐ |

### TC-I08 — Encoding ไม่ใช่ UTF-8 (edge: EC-09) (ต้อง simulate)
- group: I · ความสำคัญ: ต่ำ · trace: EC-09 / ERR_CSV_ENCODING
- Setup: role=R-01 · seed=default · files=`members_tis620.csv` · **หมายเหตุ: prototype (client mock) อ่านเป็น UTF-8 — ภาษาไทยจะเพี้ยนและตกที่ validation ตำบลแทน; ระบบจริงต้อง reject ทั้งไฟล์ด้วยข้อความด้านล่าง**
- Start: OPEN `#/members` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD members_tis620.csv | — | **ระบบจริง:** reject ทั้งไฟล์ "ไฟล์ต้องเป็น UTF-8 กรุณาบันทึกไฟล์ใหม่เป็น UTF-8" · **prototype:** ยอมรับได้ว่าแถวตกที่ "ไม่พบตำบล/จังหวัด" (ภาษาไทยเพี้ยน) — mark BLOCKED ถ้าไม่ตรงทั้งสองแบบ | ☐ |

---

## Group V — ตรวจสอบยืนยัน (OV-04)

### TC-V01 — Approve เดี่ยว (happy — LOCK-02)
- group: V · ความสำคัญ: สูง · trace: AC-14 / US-04 / BR-AGM-03
- Setup: role=R-02 (prototype: user เดียวกดได้) · seed=default (FM-000004 pending) · files=—
- Start: OPEN `#/members/FM-000004`
- ผ่านเมื่อ: pill เปลี่ยนเขียว + ประวัติมี event อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer | — | ชื่อ **บุญมี ศรีสุข** + pill เหลือง **รอตรวจสอบ** + ปุ่ม **แก้ไข / ตรวจสอบ / ลบ** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบ** | — | modal **ตรวจสอบสมาชิก** — สรุป ชื่อ + Member Id + เลขบัตร (masked) + radio 2 ตัว | ☐ |
| 3 | CLICK ตัวเลือก **ยืนยัน (อนุมัติ)** | — | ตัวเลือกไฮไลต์เขียว · placeholder หมายเหตุ = "หมายเหตุเพิ่มเติม (ไม่บังคับ)" | ☐ |
| 4 | CLICK ปุ่ม **ยืนยัน** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast เขียว **ยืนยันสมาชิกเรียบร้อย** + pill ใน drawer/ตารางเปลี่ยนเป็นเขียว **อนุมัติแล้ว** | ☐ |
| 6 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — อนุมัติ** โดย ประวิทย์ ตรวจการ | ☐ |

### TC-V02 — Reject โดยไม่กรอกเหตุผล → block (negative — EC-03 / VR-07)
- group: V · ความสำคัญ: สูง · trace: AC-15 / EC-03 / VR-07 / BR-AGM-04
- Setup: role=R-02 · seed=default (FM-000005 pending) · files=—
- Start: OPEN `#/members/FM-000005` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวเลือก **ปฏิเสธ** | — | ไฮไลต์แดง · label หมายเหตุมี * · placeholder = "กรุณาระบุเหตุผลในการปฏิเสธ" | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** (หมายเหตุว่าง) | — | ไม่ดำเนินการ + error แดง **จำเป็นต้องระบุเหตุผลเมื่อปฏิเสธ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V03 — Reject พร้อมเหตุผล → note แสดงใน detail
- group: V · ความสำคัญ: สูง · trace: AC-15 / LOCK-02
- Setup: role=R-02 · seed=default (FM-000005 pending) · files=—
- Start: OPEN `#/members/FM-000005` → CLICK **ตรวจสอบ** → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "เอกสารไม่ครบ ขอสำเนาบัตร" → ช่องหมายเหตุ → CLICK **ยืนยัน** → WAIT | — | toast **ปฏิเสธสมาชิกเรียบร้อย** + pill แดง **ปฏิเสธ** | ☐ |
| 2 | VERIFY กล่องเหตุผลใน Tab ข้อมูล (ส่วนสถานะ) | — | กล่องส้ม **เหตุผลที่ปฏิเสธ: เอกสารไม่ครบ ขอสำเนาบัตร** + คำแนะนำ "แก้ไขข้อมูลแล้วบันทึก รายการจะกลับเข้าคิวรอตรวจสอบอัตโนมัติ" | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ปฏิเสธ** + กล่อง note "เอกสารไม่ครบ ขอสำเนาบัตร" | ☐ |

### TC-V04 — ไม่เลือกผลตรวจสอบ (negative — VR-06)
- group: V · ความสำคัญ: กลาง · trace: VR-06
- Setup: role=R-02 · seed=default (FM-000006 pending) · files=—
- Start: OPEN `#/members/FM-000006` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยัน** ทันที (ยังไม่เลือก radio) | — | ไม่ดำเนินการ + error **กรุณาเลือกผลการตรวจสอบ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V05 — Bulk verify กลุ่ม + รายการถูกตรวจไปก่อน (edge: EC-12) (ต้อง simulate)
- group: V · ความสำคัญ: สูง · trace: AC-17, AC-18 / EC-12 / US-05
- Setup: role=R-02 · seed=default (pending 7) · **simulate EC-12: ระบบจริงต้องมี user ที่สอง verify 1 รายการระหว่าง bulk — prototype ทำไม่ได้ ให้ตรวจเฉพาะเส้น happy แล้ว mark ข้อ EC-12 เป็น SIT case** · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox หัวตาราง (เลือก pending ทั้ง 7) → CLICK ปุ่ม **ตรวจสอบที่เลือก (7)** | — | modal **ตรวจสอบสมาชิกทั้งหมด** + list "รายการที่เลือก (7 รายการ)" แสดง Member Id + ชื่อ + เลขบัตร masked ครบ 7 | ☐ |
| 2 | CLICK **ยืนยัน (อนุมัติ)** → CLICK ปุ่ม **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 7 ล้มเหลว 0** | ☐ |
| 3 | VERIFY ตาราง + stats | — | ไม่มีแถว pill เหลืองเหลือ · การ์ด **รอตรวจสอบ 0** · **อนุมัติแล้ว 14** · ปุ่มหัวกลับเป็น (0) disabled | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | กรณีบางรายการถูก verify ก่อน: toast "สำเร็จ X ล้มเหลว Y (FM-… ถูกตรวจสอบไปแล้ว)" — รายการอื่นต้องสำเร็จตามปกติ (per-record ไม่ล้มทั้งชุด) | ☐ |

### TC-V06 — Verify รายการที่ไม่ใช่ pending (negative — BR-AGM-03) (ต้อง simulate)
- group: V · ความสำคัญ: กลาง · trace: AC-16 / BR_VERIFY_NOT_PENDING
- Setup: role=R-02 · seed=default · **หมายเหตุ: UI ซ่อนปุ่มตรวจสอบสำหรับ approved/rejected อยู่แล้ว — ส่วน 422 server ต้องยิง API ตรง (SIT)** · files=—
- Start: OPEN `#/members/FM-000001` (approved)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบนหัว view drawer | — | มีเฉพาะ **แก้ไข** + X — **ไม่มีปุ่ม ตรวจสอบ / ลบ** (สถานะอนุมัติแล้ว) | ☐ |
| 2 | OPEN `#/members/FM-000003` (rejected) → VERIFY ปุ่ม | — | เช่นเดียวกัน: ไม่มีปุ่ม ตรวจสอบ/ลบ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT) | — | POST verify กับ record approved → 422 "รายการนี้ถูกตรวจสอบไปแล้ว" | ☐ |

---

## Group E — แก้ไข + State machine (OV-02 — LOCK-06/07)

### TC-E01 — แก้ไขสมาชิก pending → สถานะคงเดิม + โหลดค่าเดิม (happy)
- group: E · ความสำคัญ: สูง · trace: US-06 / FN-02 / legacy FN-AT-AGM-102
- Setup: role=R-01 · seed=default (FM-000004 pending) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว FM-000004 | — | drawer **แก้ไขสมาชิก FM-000004** เปิด — ทุกช่องมีค่าเดิม (บุญมี / ศรีสุข / เบอร์ 0845678901 / ราชบุรี / บ้านโป่ง / ท่าผา / 70110) | ☐ |
| 2 | TYPE แก้ช่อง **เบอร์โทรศัพท์** เป็น "0899999999" | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + แถว FM-000004 ยัง pill เหลือง **รอตรวจสอบ** (ไม่เปลี่ยนสถานะ) + เบอร์ในตาราง = 0899999999 | ☐ |
| 4 | OPEN `#/members/FM-000004` → CLICK Tab **ประวัติ** | — | มีรายการ **แก้ไขข้อมูล** เพิ่มบนสุด | ☐ |

### TC-E02 — แก้ Rejected → กลับ Pending อัตโนมัติ + note ย้ายเข้าประวัติ (LOCK-06 ★)
- group: E · ความสำคัญ: สูงสุด · trace: AC-19 / LOCK-06 / BR-AGM-11 / US-06
- Setup: role=R-01 · seed=default (FM-000003 rejected, note "เลขบัตรประชาชนไม่ตรงกับสำเนาที่แนบ") · files=—
- Start: OPEN `#/members/FM-000003`
- ผ่านเมื่อ: บันทึกแล้วสถานะกลับรอตรวจสอบเอง + เหตุผลเดิมอยู่ในประวัติ ไม่อยู่ใน record

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Tab ข้อมูล | — | pill แดง **ปฏิเสธ** + กล่องส้ม **เหตุผลที่ปฏิเสธ: เลขบัตรประชาชนไม่ตรงกับสำเนาที่แนบ** | ☐ |
| 2 | CLICK ปุ่ม **แก้ไข** | — | drawer แก้ไขเปิด + แถบฟ้าแจ้ง **รายการนี้ถูกปฏิเสธ — บันทึกแล้วรายการจะกลับเข้าคิว "รอตรวจสอบ" อีกครั้งโดยอัตโนมัติ (เหตุผลเดิมย้ายไปอยู่ในประวัติ)** | ☐ |
| 3 | TYPE แก้ช่อง **เลขบัตรประชาชน** เป็น "3710100234999" | — | ช่องแสดงค่าใหม่ 13 หลัก | ☐ |
| 4 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกแล้ว — รายการกลับเข้าคิวรอตรวจสอบ** | ☐ |
| 5 | VERIFY แถว FM-000003 ในตาราง | — | pill เปลี่ยนเป็นเหลือง **รอตรวจสอบ** (อัตโนมัติ — ไม่ต้องกดอะไรเพิ่ม) · การ์ดรอตรวจสอบ +1, ปฏิเสธ −1 | ☐ |
| 6 | OPEN `#/members/FM-000003` → VERIFY Tab ข้อมูล | — | **ไม่มี**กล่องเหตุผลที่ปฏิเสธแล้ว (note ถูกเคลียร์จาก record) · ผลตรวจสอบล่าสุด = "— รอการตรวจสอบ" | ☐ |
| 7 | CLICK Tab **ประวัติ** | — | รายการบนสุด **แก้ไขและส่งเข้าคิวตรวจสอบใหม่** + กล่อง note "เหตุผลที่ถูกปฏิเสธเดิม: เลขบัตรประชาชนไม่ตรงกับสำเนาที่แนบ" · รายการ reject เดิมยังอยู่ครบ (history immutable) | ☐ |

### TC-E03 — แก้ Approved → สถานะคงเดิม (LOCK-07 ★)
- group: E · ความสำคัญ: สูง · trace: AC-20 / LOCK-07 / BR-AGM-12
- Setup: role=R-01 · seed=default (FM-000002 approved) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว FM-000002 | — | drawer แก้ไขเปิด + ใต้หัวข้อระบุ "สถานะปัจจุบัน: อนุมัติแล้ว — แก้ไขได้ทุกช่อง สถานะคงเดิม (บันทึกลงประวัติ)" — **ทุกช่องแก้ได้ ไม่มีช่อง lock** | ☐ |
| 2 | TYPE แก้ช่อง **ที่อยู่** เป็น "แก้ไขที่อยู่ใหม่ 111 หมู่ 9" → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + pill ยังเขียว **อนุมัติแล้ว** | ☐ |
| 3 | OPEN `#/members/FM-000002` → Tab **ประวัติ** | — | มีรายการ **แก้ไขข้อมูล** ใหม่ — รายการอนุมัติเดิมยังอยู่ | ☐ |

### TC-E04 — แก้ citizen_id หลัง Approved → anomaly (XT-02 ★)
- group: E · ความสำคัญ: สูง · trace: XT-02 / BR-AGM-12 / BRD §18.5 / RS-02
- Setup: role=R-01 · seed=default (FM-000007 approved) · files=—
- Start: OPEN `#/members` → CLICK ดินสอแถว FM-000007

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE แก้ช่อง **เลขบัตรประชาชน** เป็น "3710100234888" → CLICK **บันทึกการแก้ไข** → WAIT | — | บันทึกได้ (LOCK-07) + pill ยังเขียว | ☐ |
| 2 | OPEN `#/members/FM-000007` → Tab **ประวัติ** | — | รายการ **แก้ไขข้อมูล** บนสุดมี note **"แก้ไขเลขบัตรประชาชนหลังอนุมัติ — บันทึกเข้ารายงานความผิดปกติ (Anomaly Report)"** | ☐ |
| 3 | VERIFY (ระบบจริง — SIT) | — | event `farmer_member_citizen_id_changed_event` ถูก emit + record โผล่ Anomaly Report ให้การเงินตรวจ | ☐ |

### TC-E05 — แก้ไขแล้วชนเลขบัตรซ้ำ (negative — VR-05 exclude ตัวเอง)
- group: E · ความสำคัญ: กลาง · trace: VR-05 / BR_CITIZEN_ID_DUPLICATE (เพิ่มเติม)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members` → CLICK ดินสอแถว FM-000004

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกการแก้ไข** โดยไม่แก้อะไร | — | บันทึกสำเร็จ (เลขบัตรเดิมของตัวเอง **ไม่**นับเป็นซ้ำ) | ☐ |
| 2 | CLICK ดินสอแถว FM-000004 อีกครั้ง → TYPE เลขบัตรเป็น "3710100234561" (ของ FM-000001) → CLICK **บันทึกการแก้ไข** | B4 | ไม่บันทึก + error **เลขบัตรประชาชนนี้มีในระบบแล้ว (FM-000001)** | ☐ |

### TC-E06 — Re-submit วนหลายรอบ (edge: EC-14)
- group: E · ความสำคัญ: กลาง · trace: EC-14 / LOCK-06 / BR-AGM-11
- Setup: role=R-01+R-02 · seed=default (FM-000011 rejected) · files=—
- Start: OPEN `#/members/FM-000011`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** → TYPE แก้ **ที่อยู่** → CLICK **บันทึกการแก้ไข** → WAIT | รอบ 1 | สถานะกลับ **รอตรวจสอบ** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบ** → **ปฏิเสธ** + TYPE "ยังไม่ครบ รอบ 2" → **ยืนยัน** → WAIT | — | pill แดง **ปฏิเสธ** | ☐ |
| 3 | CLICK **แก้ไข** → แก้ **ที่อยู่** อีกครั้ง → **บันทึกการแก้ไข** → WAIT | รอบ 2 | สถานะกลับ **รอตรวจสอบ** (ไม่จำกัดรอบ) | ☐ |
| 4 | OPEN `#/members/FM-000011` → Tab **ประวัติ** | — | timeline ครบทุกรอบเรียงใหม่→เก่า: resubmit(2) / reject "ยังไม่ครบ รอบ 2" / resubmit(1) / reject เดิม / create — ไม่มีรายการหาย | ☐ |
| 5 | VERIFY (ระบบจริง — SIT) | — | re-submit > 3 ครั้ง → flag anomaly (BRD §17.4) โผล่ Anomaly Report | ☐ |

---

## Group D — ลบ (soft — OV-05)

### TC-D01 — ลบสมาชิก pending (happy — LOCK-02) + ไม่นับใน stats (XT-04)
- group: D · ความสำคัญ: สูง · trace: AC-21 / BR-AGM-05 / XT-04 / US-07
- Setup: role=R-01 · seed=default (FM-000009 pending, ทั้งหมด 16) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า การ์ด **สมาชิกทั้งหมด** และ **รอตรวจสอบ** | — | บันทึก: ทั้งหมด=16, รอตรวจสอบ=7 (อ้างใน step 5) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว FM-000009 | — | modal แดง **ลบสมาชิก?** + ข้อความ `ต้องการลบ "อารีย์ จันทร์เพ็ญ (FM-000009)" ใช่หรือไม่ การลบไม่สามารถย้อนกลับได้` + กล่องเตือน soft delete | ☐ |
| 3 | CLICK ปุ่ม **ลบ** (แดง) | — | ปุ่มเป็น **กำลังลบ…** | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast **ลบสมาชิกแล้ว** + แถว FM-000009 หายจากตาราง | ☐ |
| 5 | VERIFY stats อีกครั้ง | — | ทั้งหมด=15 (ลด 1 จากค่าที่จด step 1) · รอตรวจสอบ=6 — soft-deleted ไม่นับ (XT-04) | ☐ |
| 6 | OPEN `#/members/FM-000009` (route ตรง) | — | ไม่เปิด detail — เด้งกลับ `#/members` (รายการถูกลบเข้าไม่ได้) | ☐ |

### TC-D02 — ไม่มีปุ่มลบสำหรับ approved/rejected (negative — EC-02)
- group: D · ความสำคัญ: สูง · trace: AC-22 / EC-02 / BR-AGM-05 / XT-01 (โครงสร้าง: มี quota = approved = ลบไม่ได้)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **การดำเนินการ** แถว FM-000001 (อนุมัติแล้ว) | — | มีเฉพาะไอคอนดินสอ — **ไม่มีถังขยะ** | ☐ |
| 2 | VERIFY แถว FM-000003 (ปฏิเสธ) | — | ไม่มีถังขยะเช่นกัน | ☐ |
| 3 | OPEN `#/members/FM-000001` → VERIFY ปุ่มหัว drawer | — | ไม่มีปุ่ม **ลบ** | ☐ |

### TC-D03 — Guard ลบรายการไม่ใช่ pending (server guard ซ้ำ) (ต้อง simulate)
- group: D · ความสำคัญ: กลาง · trace: EC-02 / BR_DELETE_NOT_PENDING
- Setup: role=R-01 · seed=default · **simulate: prototype ตรวจ guard ที่ function เดียวกัน — ระบบจริงยิง DELETE ตรงกับ record approved (SIT)** · files=—
- Start: —

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — SIT): DELETE /farmer-members/:id ของ record approved | — | 422 + ข้อความ **ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ** — record ไม่ถูกลบ | ☐ |

---

## Group W — รายละเอียด / ประวัติ (P-02)

### TC-W01 — View detail ครบ 3 กลุ่ม + 2 tabs (happy)
- group: W · ความสำคัญ: สูง · trace: AC-23 / US-08 / 01_UI P-02
- Setup: role=R-01 · seed=default (FM-000001) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว FM-000001 | — | view drawer: eyebrow "สมาชิกเกษตรกร · FM-000001" + ชื่อ **สมชาย ใจดี** + pill เขียวหลังชื่อ | ☐ |
| 2 | VERIFY Tab **ข้อมูล** | — | 3 กลุ่ม: **ข้อมูลส่วนตัว** (ชื่อ/เลขบัตรเต็ม/เบอร์/อีเมล) · **ที่อยู่** (ที่อยู่/จังหวัด/อำเภอ/ตำบล/ไปรษณีย์) · **สถานะ** (สถานะการยืนยัน + สถานะโควตา + สร้างเมื่อ + ผลตรวจสอบล่าสุด) | ☐ |
| 3 | VERIFY footer drawer | — | ซ้าย: "อัปเดตล่าสุด …" · ขวา: ปุ่ม **ปิด** (ปุ่มขาว — ไม่ใช่สีแดง) | ☐ |
| 4 | CLICK ปุ่ม **ปิด** | — | drawer ปิด + route กลับ `#/members` | ☐ |

### TC-W02 — Timeline ประวัติครบทุก event (LOCK-05 / S01-07)
- group: W · ความสำคัญ: สูง · trace: AC-23 / S01-07 / FN-09
- Setup: role=R-01 · seed=default (FM-000003 rejected — มี create + reject) · files=—
- Start: OPEN `#/members/FM-000003`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **ประวัติ** | — | timeline เรียงใหม่→เก่า: **ตรวจสอบ — ปฏิเสธ** (จุดแดง + note "เลขบัตรประชาชนไม่ตรงกับสำเนาที่แนบ" + โดย ประวิทย์ ตรวจการ) → **สร้างข้อมูลสมาชิก** (โดย สมพร วงศ์ทะเบียน) — ทุกรายการมีวันเวลา | ☐ |

### TC-W03 — Route refresh-safe `#/members/:id`
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / Rule B routing (เพิ่มเติม)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/members/FM-000012` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/members/FM-000012` | — | หน้า list โหลด + view drawer ของ **คำปอง อินทร์ตา** เปิดเองทันที | ☐ |
| 2 | PRESS F5 (refresh ทั้งหน้า) | — | กลับมาที่เดิม — drawer FM-000012 ยังเปิด (refresh-safe) | ☐ |
| 3 | CLICK พื้นหลังมืดนอก drawer (backdrop) | — | drawer ปิด + route = `#/members` | ☐ |

### TC-W04 — quota_status read-only + คงค่า no_quota เสมอ (XT-03 / BR-AGM-13 / GAP-03)
- group: W · ความสำคัญ: กลาง · trace: XT-01, XT-03 / BR-AGM-13 / GAP-03 (authoritative TC-283 — quota_status คงค่า no_quota)
- Setup: role=R-01 · seed=default (**quota_status = no_quota ทุก record** — authoritative; has_quota = Phase-2) · files=—
- Start: OPEN `#/members/FM-000001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วน **สถานะ** | — | **สถานะโควตา** = pill ขอบเทา **ไม่มีโควตา** (คงค่า `no_quota` เสมอ Phase-1) — เป็น display เท่านั้น ไม่มีปุ่ม/ช่องแก้ที่ใดใน feature นี้ | ☐ |
| 2 | CLICK **แก้ไข** → VERIFY ฟอร์ม | — | ฟอร์มแก้ไข **ไม่มีช่องสถานะโควตา** ให้แก้ (read-only จาก module Quota) | ☐ |
| 3 | OPEN `#/members/FM-000002` → VERIFY | — | สถานะโควตา = **ไม่มีโควตา** เช่นกัน (ทุก record คงค่า no_quota — authoritative TC-283) | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | XT-01: module Quota (Phase-2) ผูกได้เฉพาะสมาชิก **อนุมัติแล้ว** — ผูกกับ pending/rejected ต้องถูกปฏิเสธ · has_quota เขียนโดย Quota module เท่านั้น | ☐ |

---

## Group P — Permission / SoD

### TC-P01 — SoD: ผู้สร้างห้าม verify ตัวเอง (edge: EC-15) (ต้อง simulate)
- group: P · ความสำคัญ: กลาง · trace: EC-15 / ERR_SOD_SELF_VERIFY / S01-04 / OQ-02
- Setup: **simulate — ระบบจริง:** user A (R-01+R-02 สิทธิ์ทั้งคู่ หรือบัญชีที่สร้าง record) สร้างสมาชิก แล้ว login เดิมพยายาม verify record ที่ตัวเองสร้าง · feature flag `sod_self_verify_block` ทดสอบทั้ง on/off · prototype: ไม่มี role switching (Drift D-04) — mark BLOCKED บน prototype
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — flag ON): verify record ที่ตนเองสร้าง | — | ถูก block 403 + ข้อความ **ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง** | ☐ |
| 2 | VERIFY (ระบบจริง — flag OFF) | — | ผ่านได้ แต่ log anomaly (self-verify attempt โผล่ Anomaly Report) | ☐ |

---

## Group K — Concurrency / Idempotency (LOCK-03)

### TC-K01 — Optimistic lock CONFLICT (edge: EC-01) (ต้อง simulate)
- group: K · ความสำคัญ: สูง · trace: AC-25 / EC-01 / VR-10 / ERR_STALE_DATA / BR-AGM-06
- Setup: **simulate — ระบบจริง:** เปิด 2 browser sessions (user A แก้ record + save ก่อน, user B ที่เปิดหน้าเดิมค้างไว้ save ทีหลังด้วย expected_updated_at เก่า) · prototype single-session ทำไม่ได้ — SIT case
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B กด **บันทึกการแก้ไข** หลัง A save ไปแล้ว | — | 409 + toast แดง **ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง** — ข้อมูลของ A **ไม่ถูกทับ** | ☐ |
| 2 | VERIFY (ระบบจริง): scenario เดียวกันกับ verify (A approve ก่อน B) | — | B ได้ 409/422 — สถานะที่ A ตั้งไว้คงเดิม | ☐ |

---

## Recheck Additions (2026-07-22 — align กับ authoritative testcases TC-240..285)

> เคสเพิ่มจาก Refactor-Wave recheck (GAP-05/07/09/10/11) — ต่อ ID scheme เดิมของแต่ละ group. เคส backend/concurrency mark `(ต้อง simulate)` / SIT.

### TC-L08 — Search normalization: whitespace + phone +66/0 (GAP-10 · authoritative TC-271)
- group: L · ความสำคัญ: กลาง · trace: GAP-10 / FN-04 / API-01 (search normalization) / authoritative TC-271
- Setup: role=R-01 · seed=default (FM-000002 phone 0823456789) · files=—
- Start: OPEN `#/members`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "  สมชาย  " (มีช่องว่างหัว/ท้าย) → ช่องค้นหา | — | trim แล้ว match — เหลือแถว FM-000001 สมชาย ใจดี (ช่องว่างไม่ทำให้หาไม่เจอ) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** → TYPE "+66823456789" → ช่องค้นหา | — | phone normalize (+66→0) — เจอ FM-000002 สมหญิง รักดี (เก็บเป็น 0823456789) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT) | — | ค้นด้วยรูปแบบ stored ต่างกัน (มี/ไม่มีขีด, +66/0) ต้อง normalize ทั้งค่า stored และคำค้นก่อน match | ☐ |

### TC-V07 — Verify modal accessibility: focus-trap + aria + focus-return (GAP-09 · authoritative TC-275)
- group: V · ความสำคัญ: กลาง · trace: GAP-09 / 01_UI §1.7 a11y / authoritative TC-275 (focus-trap, aria-labelledby/describedby, focus-return, hook `modal.verify.confirm`)
- Setup: role=R-02 · seed=default (FM-000004 pending) · files=—
- Start: OPEN `#/members/FM-000004` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal **ตรวจสอบสมาชิก** เปิด — โฟกัสเริ่มต้น | — | โฟกัสอยู่ในองค์ประกอบแรกของ modal (radio/ปุ่มปิด) — ไม่ค้างที่ปุ่มเดิมหลัง modal | ☐ |
| 2 | PRESS Tab วนจนสุด modal แล้ว Tab ต่อ | — | **focus-trap:** โฟกัสวนกลับมาต้น modal — ไม่หลุดไปหน้าหลัง (backdrop) | ☐ |
| 3 | VERIFY (a11y — inspect/AT) | — | modal มี `aria-labelledby` (ชี้ title "ตรวจสอบสมาชิก") + `aria-describedby` (สรุปสมาชิก) + `role="dialog"`/`aria-modal="true"` | ☐ |
| 4 | PRESS Esc | — | modal ปิด + **focus-return:** โฟกัสกลับไปที่ปุ่ม **ตรวจสอบ** เดิมที่เปิด modal | ☐ |

### TC-V08 — Bulk-verify per-item Retry สำหรับแถวที่ล้มเหลว (GAP-11 · authoritative TC-264) (ต้อง simulate)
- group: V · ความสำคัญ: กลาง · trace: GAP-11 / 01_UI OV-04 (per-item Retry) / API-06 / authoritative TC-264
- Setup: role=R-02 · **simulate — ระบบจริง:** bulk verify ที่มีบางแถวล้มเหลว (STALE/NOT_PENDING) · prototype แสดง summary รวม — Retry ต่อแถวต้องทดสอบที่ระบบจริง (SIT) · files=—
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): bulk approve 10 รายการ, 2 แถวล้มเหลว | — | ผลสรุป "สำเร็จ 8 ล้มเหลว 2" + แต่ละแถวล้มเหลวมีปุ่ม **ลองใหม่** ต่อรายการ | ☐ |
| 2 | VERIFY (ระบบจริง): CLICK **ลองใหม่** ที่แถวล้มเหลว 1 รายการ | — | เรียก verify เฉพาะรายการนั้นซ้ำ (โหลด expected_updated_at ใหม่) — สำเร็จ → หายจากรายการล้มเหลว, ไม่ต้อง bulk ทั้งชุดใหม่ | ☐ |

### TC-I09 — CSV idempotency rerun: batch_id + file_hash (GAP-05 · authoritative TC-247/279) (ต้อง simulate)
- group: I · ความสำคัญ: สูง · trace: GAP-05 / API-08 §2.3 / FN-08 / authoritative FN-AT-AGM-108/109 + FN-SEQ-AGM-114 / TC-247/279
- Setup: role=R-01 · **simulate — ระบบจริง:** batch idempotency เป็น server-side · prototype (client mock) ไม่มี batch store — SIT · files=`members_ok.csv` (3 แถว)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): upload members_ok.csv ด้วย batch_id=BX + file เดิม | — | สร้าง 3 แถว รายงานผล created 3 | ☐ |
| 2 | VERIFY (ระบบจริง): rerun batch_id=BX + file_hash เดิม (ไฟล์เดิม) | — | **return รายงานผลเดิม** — ไม่สร้างซ้ำ (created ยัง 3, ไม่ใช่ 6) | ☐ |
| 3 | VERIFY (ระบบจริง): batch_id=BX + ไฟล์ **ต่าง** (file_hash ต่าง) | — | **409 ERR_BATCH_CONFLICT** — batch_id นี้ถูกใช้กับไฟล์อื่นแล้ว | ☐ |
| 4 | VERIFY (ระบบจริง): per-row key `{FN-AT-AGM-109}:{batch_id}:{row}:{citizen_id}` | — | resume batch ที่ค้าง — แถวที่สร้างไปแล้วไม่ถูกสร้างซ้ำ | ☐ |

### TC-K02 — member_id generation ภายใต้ concurrency สูง — atomic uniqueness (GAP-07 · authoritative TC-268/243) (ต้อง simulate)
- group: K · ความสำคัญ: สูง · trace: GAP-07 / BR-AGM-01 / FN-01 (Document Numbering กลาง) / authoritative FN-AT-AGM-99 / TC-268, TC-243
- Setup: **simulate — ระบบจริง:** ยิง create หลาย request พร้อมกัน (concurrent) ต่อ tenant เดียว · prototype single-thread ทำไม่ได้ — SIT · files=—
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): create N รายการพร้อมกัน (เช่น 50 concurrent) tenant เดียว | — | member_id ทุกตัว **unique + ต่อเนื่อง** format FM-%06d — ไม่มีเลขซ้ำ/ไม่มีเลขข้าม (atomic sequence/row-lock — FN-AT-AGM-99) | ☐ |
| 2 | VERIFY (ระบบจริง): unique index บน (tenant_id, member_id) | — | ไม่มี collision — DB unique constraint บังคับชั้นสุดท้าย | ☐ |

### TC-PF01 — Performance ที่ authoritative thresholds SER/VAL/CRE-UPT (GAP-04 · authoritative TC-269/270) (ต้อง simulate)
- group: PF · ความสำคัญ: กลาง · trace: GAP-04 / 05_RULES §5.8 / 06_TESTS §6.6 / authoritative TC-269, TC-270
- Setup: **simulate — ระบบจริง:** วัดที่ระบบจริง (load/perf tool) · prototype ไม่วัด latency จริง — SIT · seed=50,000 members/tenant · files=—
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): GET list/detail (reads) | — | **SER ≤ 500ms** | ☐ |
| 2 | VERIFY (ระบบจริง): validation (field/complex validate ก่อน write) | — | **VAL ≤ 300ms** | ☐ |
| 3 | VERIFY (ระบบจริง): POST create / PUT update (writes) | — | **CRE/UPT ≤ 1500ms** | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `farmer-member-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/UPLOAD/PRESS/WAIT/VERIFY)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast อยู่มุมขวาล่าง หายเองใน ~3-4.5s — อ่านทันทีที่โผล่)
5. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` (ข้อความ/สภาพจริงที่เห็น) แล้วไปเคสถัดไป
6. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"
7. ไฟล์ทดสอบทั้งหมดต้องอยู่ในโฟลเดอร์ที่ agent เข้าถึงได้ก่อนเริ่ม (ดู Data Sets → Files)
8. จบทุกเคส → กรอก Result Report ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 26 / 26 |
| Business rules (BR-AGM-01..14) | 13 / 14 (ข้าม 1 มีเหตุผล) |
| Validation (VR-01..11) | 11 / 11 |
| Edge cases (EC-01..16) | 16 / 16 (5 เคส simulate/SIT) |
| Error codes (UI-observable) | 10 / 15 (ข้าม 5 server/auth-level มีเหตุผล) |
| Permission cells | 6 / 10 (ข้าม 4 — Drift D-04 prototype single-role) |
| UI states | 6 / 7 (ข้าม all-empty มีเหตุผล) |

- Cross-Module (XT): **4/4** (XT-01 บางส่วน simulate — module Quota ยังไม่สร้าง)
- Scope Lock (LOCK): **8/8** — ทุก LOCK มีเคส verify
- **Manifest cross-check (FRD §0.12): ✅ 8 Stories + 14 Rules + 11 VR + 16 EC — ทุกแถวมีคู่ใน Ledger**

### ข้าม (พร้อมเหตุผล)
- BR-AGM-14 (DOA placeholder) — backend field + OQ-01, ไม่มีผลบน UI Phase 1
- ERR_DUPLICATE_IDEMPOTENCY_KEY / ERR_NOT_FOUND / ERR_INSUFFICIENT_ROLE / ERR_NOT_AUTHENTICATED / ERR_EMPTY_SELECTION — server/auth-level ไม่มีเส้นทางบน prototype (ERR_EMPTY_SELECTION ถูกกันด้วยปุ่ม disabled — ตรวจใน TC-L04)
- Permission deny cells (R-01 verify / R-02 create-edit-delete-import) — prototype ไม่มี role switching (UI Brief Drift D-04) — ทดสอบที่ระบบจริงผ่าน ENC matrix
- UI state all-empty (list ว่างจริง) — seed 16 รายการ ลบหมดใน prototype ไม่ได้ (ลบได้เฉพาะ pending) — ตรวจ filter-empty แทน (TC-L03)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-001",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 51, "pass": 0, "fail": 0, "blocked": 0 }
}
```
