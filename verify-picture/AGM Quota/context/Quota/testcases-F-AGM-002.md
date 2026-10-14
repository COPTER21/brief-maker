# AI Test Cases — F-AGM-002 Quota Management (จัดการโควตา)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `quota-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ HTML + UI Brief §9 แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side / role / cross-module Farmer API จริง) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-002 (AGM/Quota — WKN) |
| App entry | เปิดไฟล์ `quota-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/quotas` (list — default) · `#/quotas/:quota_number` (view drawer, refresh-safe) |
| ที่มา | FRD_F-AGM-002_Pack (7 ไฟล์) · BRD APPROVED (LOCK-01..11) · HTML v1.0 (audit FAIL=0) · UI_BRIEF_F-AGM-002 |
| จำนวนเคส | 60 เคส / 10 groups (recheck 2026-07-22: +9 — retry-UX/NFR/idempotency/a11y) |
| Scope Lock | LOCK-01..11 (00_OVERVIEW §0.11) — ทุกข้อมีเคส verify (ดู Ledger) |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า = ข้อมูล reset กลับ seed 8 โควตา + 6 สมาชิก — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh (F5) ก่อนเริ่ม |
| Cross-module | write-back `member.quota_status` จำลองในหน่วยความจำผ่าน `writeMemberQuotaStatus()` + history event `quota_status_written` + toast — Farmer API จริง (ENG-EXT-03) ทดสอบตอน SIT |

**Seed ตั้งต้น (หลัง refresh — 8 โควตา):**
| เลขโควต้า | ชื่อ | สถานะ | โหมด | หมายเหตุ |
|---|---|---|---|---|
| Q-2569-001 | สมหญิง รักดี | **อนุมัติ** | From-Member (FM-000002) | linked |
| Q-2569-002 | สุรพล เก่งการไร่ | **อนุมัติ** | From-Member (FM-000014) | linked |
| Q-2569-003 | บุญมา ทุ่งกว้าง | **รออนุมัติ** | No-Member | ค้างเกิน 7 วัน |
| Q-2569-004 | ทองคำ ไร่งาม | **รออนุมัติ** | No-Member | — |
| Q-2569-005 | ประนอม ใจเพชร | **รออนุมัติ** | No-Member | — |
| Q-2569-006 | วิรัช มั่งมี | **ไม่อนุมัติ** | No-Member | note "สำเนาบัตรไม่ชัด" |
| Q-2569-007 | สมพงษ์ ทองแท้ | **รออนุมัติ** | No-Member | ค้างเกิน 7 วัน |
| Q-2569-008 | จันทร์ แจ่มใส | **รออนุมัติ** | No-Member | — |

สรุป: รออนุมัติ 5 (ค้างเกิน 7 วัน 2) · อนุมัติ 2 · ไม่อนุมัติ 1
> ⚠ **สำคัญ:** โควตาที่ **ผูกสมาชิก (From-Member)** ทั้ง 2 รายในseed เป็นสถานะ **อนุมัติแล้ว** ทั้งคู่ · โควตา **รออนุมัติ** ทั้งหมดเป็น **No-Member** → เคส cross-module reject/delete-linked (X02/X03) ต้อง **สร้างโควตา From-Member ใหม่ก่อน** (จะได้ unverified + linked) แล้วค่อย reject/ลบ

**Seed สมาชิก (6 คน Approved — จาก Farmer):**
| FM-id | ชื่อ | quota_status | ใช้ทดสอบ |
|---|---|---|---|
| FM-000001 | สมชาย ใจดี | no_quota | From-Member happy (ชุด A1) |
| FM-000002 | สมหญิง รักดี | **has_quota** | 1:0..1 block (ชุด B5) |
| FM-000007 | สายชล น้ำใจงาม | no_quota | — |
| FM-000008 | ทองดี พูลผล | no_quota | — |
| FM-000012 | คำปอง อินทร์ตา | no_quota | — |
| FM-000014 | สุรพล เก่งการไร่ | **has_quota** | 1:0..1 block (สำรอง) |

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| Q — รายการ / ค้นหา / กรอง / masking | TC-Q01..Q08 (8) | สูง |
| C — สร้าง (From/No-Member) + validation | TC-C01..C14 (14) | สูง |
| I — CSV Import (No-Member) | TC-I01..I09 (9) | สูง |
| V — ตรวจสอบยืนยัน | TC-V01..V08 (8) | สูง |
| E — แก้ไข + State machine | TC-E01..E04 (4) | สูง |
| D — ลบ (soft) | TC-D01..D03 (3) | สูง |
| W — รายละเอียด / ประวัติ | TC-W01..W05 (5) | กลาง |
| **X — Cross-module write-back ⭐** | TC-X01..X07 (7) | **สูงสุด** |
| P — Permission / SoD | TC-P01 (1) | กลาง |
| K — Concurrency / Idempotency | TC-K01 (1 + C11) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1 ← BRD §7)
| item | cases |
|---|---|
| AC-01 From-Member happy + toast + unverified + has_quota | TC-C01, TC-X01 |
| AC-02 สมาชิกมีโควตาแล้ว → block | TC-C04 |
| AC-03 เริ่ม unverified เสมอ + history=create | TC-C03 |
| AC-03b ผูกได้เฉพาะ Approved (member-search แสดงเฉพาะ Approved) | TC-C01 (step verify), TC-C04 |
| AC-04 No-Member happy + ไม่เขียน quota_status | TC-C02 |
| AC-05 quota_number ซ้ำ → "เลขโควต้านี้ถูกใช้แล้ว" | TC-C05 |
| AC-06 citizen ≠ 13 | TC-C06 |
| AC-07 phone ≠ 9-12 | TC-C07 |
| AC-08 postal auto ×2 + cascade reset แยกที่อยู่ | TC-C10 |
| AC-09 email format + optional | TC-C08 |
| AC-10 required ครบ | TC-C09 |
| AC-11 prefill จากสมาชิก + member summary card | TC-C01 |
| AC-13 เอกสารแนบ guard (>5MB / ไม่ใช่ PDF/JPG/PNG) | TC-C12 (prototype mock — SIT ตรวจ guard จริง) |
| AC-14 CSV partial success + error report + unverified/No-Member | TC-I02 |
| AC-15 ไม่ใช่ .csv | TC-I03 |
| AC-16 ทุกแถวผ่าน + toast | TC-I07 |
| AC-17 modal title ระบุ No-Member | TC-I01 |
| AC-18 ค้นหา debounce 6 field | TC-Q02 |
| AC-19 ไม่พบ → empty state | TC-Q03 |
| AC-20 approve เดี่ยว | TC-V01 |
| AC-21 reject **ไม่กรอก note ผ่านได้** (LOCK-09 ★) | TC-V02 |
| AC-21b reject linked → warning + no_quota | TC-X02 |
| AC-22 verify verified/rejected → 422 (UI ซ่อนปุ่ม) | TC-V06 |
| AC-23 bulk เฉพาะ unverified + summary | TC-Q04, TC-V05 |
| AC-24 edit optimistic ผ่าน + **ไม่เปลี่ยนสถานะ** (OQ-Q3 ★) | TC-E01, TC-E02, TC-E03 |
| AC-25 optimistic conflict 409 | TC-K01 (ต้อง simulate) |
| AC-26 double-click idempotency | TC-C11 |
| AC-27 ลบ unverified + soft + linked no_quota + guard | TC-D01, TC-D02, TC-X03 |
| AC-28 detail 3 tabs + member card | TC-W01, TC-W02, TC-W03 |
| AC-29 citizen mask list / detail เต็ม + bank/BAAC mask | TC-Q06, TC-W01 |

### Cross-Module (06_TESTS §6.9) ⭐
| XT | Scenario | Downstream | Case |
|---|---|---|---|
| XT-01 | reject โควตา linked → no_quota | Farmer | TC-X02 |
| XT-02 | ลบ โควตา linked → no_quota | Farmer | TC-X03 |
| XT-03 | สร้าง From-Member → has_quota | Farmer | TC-X01 |
| XT-04 | reject/delete แต่ member ถูกลบก่อน → skip + log (EC-17) | Farmer | TC-X04 (ต้อง simulate) |
| — | reconcile Farmer detail แสดง มี/ไม่มีโควตา | Farmer | TC-X05 (ต้อง simulate — Farmer feature แยกไฟล์) |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-AGQ-01 quota_number user-entered + unique | TC-C05, TC-E04 |
| BR-AGQ-02 2 create modes (From/No-Member) | TC-C01, TC-C02 |
| BR-AGQ-03 1:0..1 + Approved | TC-C04, TC-C01 |
| BR-AGQ-04 verify เฉพาะ unverified | TC-V06 |
| BR-AGQ-05 verify note optional (LOCK-09 ★) | TC-V02 |
| BR-AGQ-06 ลบเฉพาะ unverified + soft | TC-D01, TC-D02, TC-D03 |
| BR-AGQ-07 cross-module write-back | TC-X01, TC-X02, TC-X03, TC-X04 |
| BR-AGQ-09 optimistic lock + idempotency | TC-K01, TC-C11 |
| BR-AGQ-10 CSV No-Member partial success | TC-I02, TC-I04 |
| BR-AGQ-11 postal auto ×2 + validate | TC-C10, TC-I06 |
| BR-AGQ-12 file limits (config) | TC-C12 |
| BR-AGQ-13 DOA placeholder | — ข้าม (backend placeholder OQ-Q5 — ไม่มีผลบน UI Phase 1) |

### Validation (05_RULES §5.4 VR-01..12)
| VR | cases |
|---|---|
| VR-01 citizen 13 หลัก | TC-C06 |
| VR-02 phone 9–12 หลัก | TC-C07 |
| VR-03 email optional + format (LOCK-11) | TC-C08 |
| VR-04 required set | TC-C09 |
| VR-05 quota_number unique (exclude self) | TC-C05, TC-E04 |
| VR-06 1:0..1 ก่อนผูก | TC-C04 |
| VR-07 member Approved ก่อนผูก | TC-C01, TC-C04 |
| VR-08 CSV file guard | TC-I03 |
| VR-09 ต้องเลือกผลตรวจสอบ | TC-V04 |
| VR-10 postal ×2 match | TC-C10, TC-I06 |
| VR-11 optimistic lock message | TC-K01 (ต้อง simulate) |
| VR-12 cascade reset ×2 | TC-C10 |

### Edge Cases (05_RULES §5.5 — ☑ บังคับ + ☐ recommended)
| EC | cases / สถานะ |
|---|---|
| EC-01 ☑ สมาชิกมีโควตาแล้ว | TC-C04 |
| EC-02 ☑ quota_number ซ้ำ | TC-C05 |
| EC-03 ☑ ลบ verified/rejected | TC-D02, TC-D03 |
| EC-04 ☑ CSV บางแถวพัง | TC-I02 |
| EC-05 ☑ ค้นหาไม่เจอ | TC-Q03 |
| EC-06 ☑ เลือกทั้งหมด = เฉพาะ unverified | TC-Q04 |
| EC-07 ☑ แก้ชนกัน (optimistic) | TC-K01 (ต้อง simulate) |
| EC-08 ☑ reject/delete linked → no_quota | TC-X02, TC-X03 |
| EC-09 ☐ CSV ไม่ใช่ UTF-8 | TC-I08 (ต้อง simulate — RC-01) |
| EC-10 ☐ CSV header ผิด | TC-I04 (RC-02) |
| EC-11 ☐ quota_number ซ้ำในไฟล์ | TC-I05 (RC-03) |
| EC-12 ☐ bulk บางรายการถูก verify ก่อน | TC-V05 (ต้อง simulate ส่วน per-record) |
| EC-13 ☐ ตำบล CSV สะกดผิด | TC-I06 (RC-04) |
| EC-14 ☐ No-Member ผูก member ภายหลัง | — ข้าม (OOS — Phase 2, ไม่มี re-link) |
| EC-15 ☐ self-verify (SoD) | TC-P01 (ต้อง simulate — RC-05) |
| EC-16 ☐ double-click บันทึก | TC-C11 |
| EC-17 ☐ member ถูกลบก่อน write-back | TC-X04 (ต้อง simulate — RC-06) |

### Recommended Cases (06_TESTS §6.11)
| RC | cases / สถานะ |
|---|---|
| RC-01 CSV TIS-620 | TC-I08 ☐ (ต้อง simulate) |
| RC-02 header ขาดคอลัมน์ | TC-I04 ☐ |
| RC-03 quota_number ซ้ำในไฟล์ | TC-I05 ☐ |
| RC-04 ตำบลสะกดผิด | TC-I06 ☐ |
| RC-05 self-verify (SoD) | TC-P01 ☐ (ต้อง simulate) |
| RC-06 member ถูกลบก่อน write-back | TC-X04 ☐ (ต้อง simulate) |

### Error catalog (05_RULES §5.6 — ที่มีผลบน UI prototype)
| error | cases |
|---|---|
| ERR_VALIDATION_FAILED (รายช่อง) | TC-C06..C09, TC-V04 |
| BR_QUOTA_NUMBER_DUPLICATE | TC-C05, TC-E04, TC-I05 |
| BR_MEMBER_HAS_QUOTA | TC-C04 |
| BR_MEMBER_NOT_APPROVED | TC-C01, TC-C04 (member-search แสดงเฉพาะ Approved) |
| BR_VERIFY_NOT_UNVERIFIED | TC-V06 (ต้อง simulate ส่วน 422) |
| BR_DELETE_NOT_UNVERIFIED | TC-D02, TC-D03 |
| BR_CSV_HEADER_MISMATCH | TC-I04 |
| ERR_CSV_INVALID_FILE | TC-I03 |
| ERR_CSV_ENCODING | TC-I08 (simulate) |
| ERR_STALE_DATA | TC-K01 (simulate) |
| ERR_SOD_SELF_VERIFY | TC-P01 (simulate) |
| ERR_INSUFFICIENT_ROLE / ERR_NOT_FOUND / ERR_DUPLICATE_IDEMPOTENCY_KEY | — ข้าม (server/auth-level — ไม่มีเส้นทางบน prototype single-user) |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases / สถานะ |
|---|---|
| R-01 สร้าง/แก้/ลบ/CSV = allow | TC-C01, TC-E01, TC-D01, TC-I02 (prototype user เดียว) |
| R-02 verify เดี่ยว/กลุ่ม = allow | TC-V01, TC-V05 |
| R-01 verify = deny · R-02 create/edit/delete/CSV = deny | — ข้าม (Drift D-04: prototype ไม่มี role switching — ทดสอบที่ระบบจริงผ่าน ENC; UI จริงต้องซ่อนปุ่มตาม §5.3) |
| SoD self-verify block | TC-P01 (simulate) |

### Scope Lock (00_OVERVIEW §0.11)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | capability legacy 100% | ทั้ง suite — ตัวแทน: TC-C01, TC-C02, TC-I02, TC-V01, TC-V05, TC-E01, TC-D01, TC-W01, TC-Q02 |
| LOCK-02 | state machine unverified→verified/rejected + soft delete | TC-V01, TC-V02, TC-D01, TC-V06 |
| LOCK-03 | quota_number user-entered + unique | TC-C05, TC-E04 |
| LOCK-04 | 2 create modes (From/No-Member, 1:0..1, approved) | TC-C01, TC-C02, TC-C04 |
| LOCK-05 | cross-module write-back has/no_quota ⭐ | TC-X01, TC-X02, TC-X03, TC-X04 |
| LOCK-06 | optimistic lock + idempotency | TC-K01, TC-C11 |
| LOCK-07 | CSV No-Member + partial success + error report | TC-I01, TC-I02, TC-I04 |
| LOCK-08 | ลบเฉพาะ unverified + soft | TC-D01, TC-D02 |
| LOCK-09 | verify note optional (★ ตรงข้าม Farmer) | TC-V02 |
| LOCK-10 | governance additions (masking / warning / stats) | TC-Q06, TC-W03, TC-X02 |
| LOCK-11 | email optional | TC-C08 |

### UI States (§8 State-Driven Matrix)
| item | cases |
|---|---|
| loaded / filtered / filter-empty | TC-Q01, TC-Q02, TC-Q03 |
| all-empty ("ยังไม่มีโควตา") | — ข้าม (seed 8, ลบได้เฉพาะ unverified — ลบหมดไม่ได้ใน prototype; ตรวจ filter-empty แทน TC-Q03) |
| stats widgets (ค้างเกิน 7 วัน 2 รายการ / คืนสถานะโควตาสมาชิกแล้ว) | TC-Q01 |
| pill 3 สถานะ (รออนุมัติ/อนุมัติ/ไม่อนุมัติ) | TC-Q01, TC-Q02 |
| checkbox unverified selectable / อื่น disabled | TC-Q04 |
| member card linked / No-Member | TC-W01, TC-W02 |
| submitting state (ปุ่ม "กำลัง…") | TC-C01, TC-V01, TC-D01, TC-I02 (step WAIT) |
| sort / pagination footer | TC-Q05, TC-Q07 |

**Manifest cross-check (FRD §0.12):** Stories 10/10 · Rules R01–R13 12/13 (R13 DOA ข้ามมีเหตุผล) · VR 12/12 · EC ☑ 8/8 + ☐ 9/9 (EC-14 ข้าม OOS มีเหตุผล) · XT 4/4 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A1 — From-Member ถูกต้อง (happy — เลือกสมาชิก FM-000001)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาสมาชิกที่อนุมัติแล้ว | เลือก **สมชาย ใจดี (FM-000001)** *(no_quota — prefill อัตโนมัติ: ชื่อ/เลขบัตร/เบอร์/ที่อยู่ปัจจุบัน)* |
| เลขโควต้า | Q-2569-101 |
| ที่อยู่ตามบัตรประชาชน | 123 หมู่ 1 · กาญจนบุรี / ท่าม่วง / วังขนาย *(postal auto 71110)* |

### ชุด A2 — No-Member ถูกต้อง (happy — กรอกเอง ข้ามค้นหาสมาชิก)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาสมาชิก | *(ข้าม — No-Member)* |
| เลขโควต้า | Q-2569-102 |
| ชื่อ / นามสกุล | ทดสอบ / ระบบใหม่ |
| เลขบัตรประชาชน | 1103700123456 |
| เบอร์โทรศัพท์ | 0891234567 |
| อีเมล | *(เว้นว่าง — LOCK-11)* |
| ที่อยู่ปัจจุบัน | 99/1 หมู่ 2 · กาญจนบุรี / ท่าม่วง / วังขนาย *(postal auto 71110)* |
| ที่อยู่ตามบัตรประชาชน | 99/1 หมู่ 2 · ราชบุรี / บ้านโป่ง / ท่าผา *(postal auto 70110)* |

### ชุด B — ค่าผิดสำหรับ negative
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | เลขบัตรประชาชน | `12345` (5 หลัก) | เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก |
| B2 | เบอร์โทรศัพท์ | `08123` (5 หลัก) | เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก |
| B3 | อีเมล | `invalid-email` | รูปแบบอีเมลไม่ถูกต้อง |
| B4 | เลขโควต้า | `Q-2569-001` (ซ้ำ seed) | เลขโควต้านี้ถูกใช้แล้ว |
| B5 | ค้นหาสมาชิก | เลือก **สมหญิง รักดี (FM-000002)** (has_quota) | สมาชิกนี้มีโควต้าอยู่แล้ว |

### ไฟล์ทดสอบ (Files) — runner ต้องเตรียมก่อนรัน (No-Member เท่านั้น — LOCK-07)
> header 12 คอลัมน์ (จาก `CSV_COLS` ใน HTML): `quota_number,first_name,last_name,citizen_id,phone,address,province,district,subdistrict,birth_date,marital_status,number_of_children`
> *(ไปรษณีย์ไม่มีในคอลัมน์ — ระบบเติมจากตำบลอัตโนมัติ)*

| ชื่อไฟล์ | เนื้อหา |
|---|---|
| `quota_ok.csv` | 3 แถวถูกทั้งหมด — quota_number Q-2569-201/202/203 · citizen 13 หลัก · จังหวัด กาญจนบุรี/ท่าม่วง/วังขนาย |
| `quota_mixed.csv` | 6 แถว: 4 ถูก (Q-2569-211..214) + แถว 3 citizen `999` (ไม่ครบ 13) + แถว 5 phone `081` |
| `quota_dupfile.csv` | 3 แถว: แถว 2 กับแถว 3 ใช้ quota_number เดียวกัน `Q-2569-221` |
| `quota_dupdb.csv` | 2 แถว: แถวแรก quota_number `Q-2569-001` (ซ้ำ seed ในระบบ) + แถวสอง `Q-2569-231` ใหม่ |
| `quota_badsub.csv` | 2 แถว: แถวแรก subdistrict `วังขนายย` (สะกดผิด ในท่าม่วง) · แถวสอง province `นครปฐม` (ไม่มีในระบบ) |
| `quota_badheader.csv` | header ขาดคอลัมน์ `number_of_children` (เหลือ 11 คอลัมน์) + 1 แถวข้อมูลถูก |
| `quota_too_large.csv` | ไฟล์ .csv ขนาด > 5MB (gen แถวซ้ำจนเกิน) |
| `quota_tis620.csv` | เนื้อหาถูกแต่ encode TIS-620 (ภาษาไทยไม่ใช่ UTF-8) |
| `notes.xlsx` | ไฟล์ Excel ใด ๆ (ทดสอบ guard นามสกุลไฟล์) |

---

## Test Cases

## Group Q — รายการ / ค้นหา / กรอง / masking (P-01)

### TC-Q01 — เปิดหน้า list + stats widgets (happy)
- group: Q · ความสำคัญ: สูง · trace: 01_UI P-01 / UI state loaded / D-01 stats
- Setup: role=R-01 (default prototype) · seed=default 8 โควตา (refresh หน้า) · files=—
- Start: OPEN `#/quotas`
- ผ่านเมื่อ: หน้า list + สถิติ 4 การ์ดแสดงเลขตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/quotas` | — | หัวข้อ **จัดการโควตา** + count **8 รายการ** · breadcrumb "เกษตรกรรม › จัดการโควตา" · sidebar **จัดการโควตา** active | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **โควตาทั้งหมด 8** (sub "ไม่รวมที่ถูกลบ") · **รออนุมัติ 5** (meta ส้ม "ค้างเกิน 7 วัน 2 รายการ") · **อนุมัติ 2** (sub "พร้อมทำสัญญา") · **ไม่อนุมัติ 1** (sub "คืนสถานะโควตาสมาชิกแล้ว") | ☐ |
| 3 | VERIFY ปุ่มบน page header (ขวาบน) | — | เรียงซ้าย→ขวา: **Import CSV** · **ตรวจสอบที่เลือก (0)** (disabled) · **สร้างโควตา** (ปุ่มแดง ขวาสุด) | ☐ |
| 4 | VERIFY ตาราง | — | 8 คอลัมน์: ☐, เลขโควต้า (mono แดง), ชื่อ, นามสกุล, เบอร์โทรศัพท์, เลขบัตรประชาชน, สถานะ, การดำเนินการ · แถว From-Member (Q-2569-001/002) มีไอคอน link 🔗 | ☐ |
| 5 | VERIFY footer ตาราง | — | ข้อความ **1 – 8 จาก 8 รายการ** | ☐ |

### TC-Q02 — ค้นหา (debounce 300ms, 6 field) + กรองสถานะ (happy)
- group: Q · ความสำคัญ: สูง · trace: AC-18 / US-05 / LOCK-01
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`
- ผ่านเมื่อ: ค้นได้ทั้ง เลขโควตา/ชื่อ/นามสกุล/เบอร์/เลขบัตร/อีเมล + filter สถานะทำงาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "Q-2569-006" → ช่องค้นหา | เลขโควตา | รอ ~0.3s ตารางเหลือ 1 แถว: Q-2569-006 วิรัช มั่งมี (pill แดง **ไม่อนุมัติ**) | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ช่องค้นหาว่าง + ตารางกลับมา 8 รายการ | ☐ |
| 3 | TYPE "0823456789" → ช่องค้นหา | เบอร์ | เหลือแถว Q-2569-001 สมหญิง รักดี | ☐ |
| 4 | CLICK **ล้างตัวกรอง** แล้ว TYPE "jan@example.com" | อีเมล | เหลือแถว Q-2569-008 จันทร์ แจ่มใส | ☐ |
| 5 | CLICK **ล้างตัวกรอง** → SELECT "รออนุมัติ" → dropdown สถานะ | รออนุมัติ | เหลือ 5 แถว ทุกแถว pill เหลือง **รออนุมัติ** · footer "1 – 5 จาก 5 รายการ" | ☐ |
| 6 | SELECT "อนุมัติ" → dropdown สถานะ | อนุมัติ | เหลือ 2 แถว (Q-2569-001, Q-2569-002) pill เขียว **อนุมัติ** | ☐ |

### TC-Q03 — ค้นหาไม่เจอ → empty state (edge: EC-05)
- group: Q · ความสำคัญ: กลาง · trace: AC-19 / EC-05
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีโควตานี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state: **ไม่พบรายการที่ค้นหา** + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty state) | — | ตารางกลับมา 8 รายการ | ☐ |

### TC-Q04 — เลือกทั้งหมด = เฉพาะแถวรออนุมัติ (edge: EC-06)
- group: Q · ความสำคัญ: สูง · trace: AC-23 / EC-06
- Setup: role=R-01 · seed=default (unverified 5) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checkbox รายแถว | — | แถว **อนุมัติ/ไม่อนุมัติ** (Q-001/002/006) checkbox จาง กดไม่ได้ (title "เลือกได้เฉพาะรายการรออนุมัติ") · แถว **รออนุมัติ** กดได้ | ☐ |
| 2 | VERIFY ปุ่ม **ตรวจสอบที่เลือก (0)** | — | disabled (กดไม่ได้) | ☐ |
| 3 | CLICK checkbox หัวตาราง | — | ติ๊กเฉพาะ 5 แถว unverified · โผล่แถบ "**เลือก 5 รายการ (รออนุมัติ)**" + ปุ่มหัวเปลี่ยนเป็น **ตรวจสอบที่เลือก (5)** (enabled) | ☐ |
| 4 | CLICK **ยกเลิกการเลือก** (ในแถบ) | — | ยกเลิกทั้งหมด → แถบหาย + ปุ่มกลับเป็น (0) disabled | ☐ |
| 5 | CLICK checkbox แถว Q-2569-004 | — | เลือก 1 · checkbox หัวตารางเป็นสถานะ partial (ขีดกลาง) | ☐ |

### TC-Q05 — Sort คอลัมน์
- group: Q · ความสำคัญ: ต่ำ · trace: 01_UI P-01 (sortBy: quota_number/first_name/last_name/verify_status)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **ชื่อ** | — | แถวเรียงตามชื่อ ก→ฮ | ☐ |
| 2 | CLICK หัวคอลัมน์ **ชื่อ** อีกครั้ง | — | เรียงกลับ ฮ→ก | ☐ |
| 3 | CLICK หัวคอลัมน์ **สถานะ** | — | แถวจัดกลุ่มตามสถานะ (verify_status) | ☐ |

### TC-Q06 — Masking เลขบัตรบน list (LOCK-10 / S02-04)
- group: Q · ความสำคัญ: สูง · trace: AC-29 / S02-04 / D-CLASS Restricted
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **เลขบัตรประชาชน** ทุกแถวที่เห็น | — | รูปแบบ mask `X-XXXX-XXXX-XX-X` (เห็นเฉพาะหลักแรก+หลักสุดท้าย เช่น `3-XXXX-XXXX-XX-2`) — **ไม่มีแถวไหนโชว์เลขเต็ม 13 หลัก** | ☐ |
| 2 | CLICK แถว Q-2569-001 | — | view drawer เปิด — Tab **ข้อมูลทั่วไป** → กลุ่ม **ข้อมูลส่วนบุคคล** เลขบัตรแสดงเต็มรูปแบบ `3-7101-00234-57-2` (detail ตาม permission) · เลขบัญชี/ธ.ก.ส. masked (`maskAcct`) | ☐ |

### TC-Q07 — Pagination footer + คลิกแถวเปิด view
- group: Q · ความสำคัญ: ต่ำ · trace: 01_UI P-01 / Rule #41 (row-click = view)
- Setup: role=R-01 · seed=default (8 < 20/หน้า — หน้าเดียว) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ pagination | — | ปุ่มหน้า **1** (active สีแดง) · ลูกศรซ้าย/ขวา disabled (หน้าเดียว) | ☐ |
| 2 | CLICK กลางแถว Q-2569-005 (ไม่โดน checkbox/ไอคอน) | — | view drawer เปิด หัวข้อ **ประนอม ใจเพชร** + route เปลี่ยนเป็น `#/quotas/Q-2569-005` | ☐ |
| 3 | PRESS Esc | — | drawer ปิด + route กลับ `#/quotas` | ☐ |

---

### TC-Q08 — เลือกแถวข้ามหน้า pagination คงอยู่ (edge: TC-307 / AC-37) (ต้อง simulate)
- group: Q · ความสำคัญ: กลาง · trace: TC-307 / AC-37 / FN-SEQ-AGQ-131 · **prototype seed 8 แถวหน้าเดียว — SIT case เมื่อข้อมูลหลายหน้า**
- Setup: **simulate — ระบบจริง:** list มีหลายหน้า (page_size < จำนวน unverified) · role=R-01+R-02
- Start: — (SIT) / prototype: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) เลือก checkbox แถว unverified 2 แถว → ดู `ตรวจสอบที่เลือก (N)` | — | N นับตามที่เลือก · bulk-bar "เลือก N รายการ (รออนุมัติ)" | ☐ |
| 2 | VERIFY (ระบบจริง): หน้า 1 เลือก 2 แถว → ไปหน้า 2 (ไม่ล้าง) → เลือกอีก 3 แถว | — | total selected = 5 (คงการเลือกข้ามหน้า) | ☐ |
| 3 | VERIFY (ระบบจริง): CLICK **ตรวจสอบที่เลือก (5)** → ยืนยัน | — | payload FN-SEQ-AGQ-131 มี quota_id ครบทั้ง 5 (ทุกหน้า) → FN-AT-AGQ-124 ประมวลผลครบ + refresh | ☐ |

## Group C — สร้างโควตา (OV-01 — 2 modes)

### TC-C01 — สร้าง From-Member (happy — เลือก FM-000001) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-11, AC-03b / BR-AGQ-02/03 / LOCK-04 / VR-07
- Setup: role=R-01 · seed=default (FM-000001 no_quota) · files=—
- Start: OPEN `#/quotas`
- ชุดข้อมูล: A1
- ผ่านเมื่อ: prefill จากสมาชิก + toast สร้างสำเร็จ + แถวใหม่ unverified + link icon

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างโควตา** (แดง ขวาบน) | — | drawer เปิดจากขวา eyebrow **สร้างโควตาชาวไร่** + หัวข้อ **สร้างโควตา** · section แรก **ค้นหาสมาชิก (ผูกโควตา — ข้ามได้ถ้าเป็น No-Member)** | ☐ |
| 2 | CLICK ช่อง **ค้นหาสมาชิกที่อนุมัติแล้ว** → พิมพ์ "สมชาย" | — | dropdown แสดง **สมชาย ใจดี (FM-000001)** + sub เบอร์ 0812345678 · help "แสดงเฉพาะสมาชิกที่อนุมัติแล้ว · เลือกแล้วระบบจะกรอกข้อมูลให้อัตโนมัติ" | ☐ |
| 3 | CLICK ตัวเลือก **สมชาย ใจดี (FM-000001)** | A1 | แถบฟ้า **เลือกสมาชิก FM-000001 · สมชาย ใจดี — กรอกข้อมูลส่วนตัวและที่อยู่ให้อัตโนมัติแล้ว** · ช่อง ชื่อ/นามสกุล/เลขบัตร/เบอร์/ที่อยู่ปัจจุบัน ถูก prefill | ☐ |
| 4 | TYPE → ช่อง **เลขโควต้า** | A1: Q-2569-101 | แสดงค่า | ☐ |
| 5 | เลือกที่อยู่ตามบัตรประชาชน: SELECT กาญจนบุรี / ท่าม่วง / วังขนาย | A1 | รหัสไปรษณีย์ (id_card) เติม **71110** อัตโนมัติ (แก้ไม่ได้) | ☐ |
| 6 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (กดซ้ำไม่ได้) | ☐ |
| 7 | WAIT จน toast ปรากฏ (≤3s) | — | drawer ปิด + toast เขียว **สร้างโควตาสำเร็จ — Q-2569-101 (สมาชิก FM-000001 → มีโควตา)** | ☐ |
| 8 | VERIFY ตาราง | — | แถวบนสุด = Q-2569-101 สมชาย ใจดี · pill เหลือง **รออนุมัติ** · มีไอคอน link 🔗 · count = **9 รายการ** · การ์ดรออนุมัติ = 6 | ☐ |

### TC-C02 — สร้าง No-Member (happy — ข้ามค้นหาสมาชิก) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-04 / BR-AGQ-02 / LOCK-04
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**
- ชุดข้อมูล: A2
- ผ่านเมื่อ: สร้างได้โดยไม่ผูกสมาชิก + ไม่มี link icon + ไม่เขียน quota_status

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ข้าม section ค้นหาสมาชิก (ไม่เลือกใคร) → TYPE ช่อง **เลขโควต้า** | A2: Q-2569-102 | แสดงค่า | ☐ |
| 2 | TYPE ช่อง **ชื่อ / นามสกุล** | A2 | ทดสอบ / ระบบใหม่ | ☐ |
| 3 | TYPE **เลขบัตรประชาชน** / **เบอร์โทรศัพท์** | A2 | 1103700123456 / 0891234567 (รับเฉพาะตัวเลข) | ☐ |
| 4 | เลือก **ที่อยู่ปัจจุบัน** กาญจนบุรี/ท่าม่วง/วังขนาย · **ที่อยู่ตามบัตรประชาชน** ราชบุรี/บ้านโป่ง/ท่าผา | A2 | postal current=**71110**, id_card=**70110** (แต่ละที่อยู่แยกกัน) | ☐ |
| 5 | CLICK **ยืนยันสร้าง** → WAIT toast | — | toast เขียว **สร้างโควตาสำเร็จ — Q-2569-102 (No-Member)** | ☐ |
| 6 | CLICK แถวใหม่ Q-2569-102 | — | view drawer: member card สีเทา **โควตาแบบไม่ผูกสมาชิก (No-Member)** — ไม่มี link icon · ไม่มีปุ่ม ดูสมาชิก | ☐ |

### TC-C03 — สถานะเริ่ม unverified เสมอ + history=create
- group: C · ความสำคัญ: สูง · trace: AC-03 / BR-AGQ-02 / §5.2 state machine
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างโควตา** → กรอกชุด A2 ครบ → CLICK **ยืนยันสร้าง** → WAIT | A2 | toast สร้างสำเร็จ · แถวใหม่ pill เหลือง **รออนุมัติ** (ไม่มีทางสร้างเป็น approved/rejected) | ☐ |
| 2 | CLICK แถวใหม่ → CLICK Tab **ประวัติ** | — | มี 1 รายการ **สร้างโควตา** โดย สมพร วงศ์ทะเบียน + note "ไม่ผูกสมาชิก (No-Member)" | ☐ |

### TC-C04 — เลือกสมาชิกที่มีโควตาแล้ว → block (negative — EC-01 / VR-06) ★ signature
- group: C · ความสำคัญ: สูงสุด · trace: AC-02 / EC-01 / BR_MEMBER_HAS_QUOTA / 1:0..1
- Setup: role=R-01 · seed=default (FM-000002 has_quota) · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**
- ชุดข้อมูล: B5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **ค้นหาสมาชิกที่อนุมัติแล้ว** → พิมพ์ "สมหญิง" | — | dropdown แสดง **สมหญิง รักดี (FM-000002)** + sub เบอร์ **· มีโควตาแล้ว** (ต่อท้ายเบอร์) | ☐ |
| 2 | CLICK ตัวเลือก **สมหญิง รักดี (FM-000002)** | B5 | แถบแดงในกล่องสถานะสมาชิก **สมาชิกนี้มีโควต้าอยู่แล้ว — ผูกโควตาซ้ำไม่ได้ (1 สมาชิก 1 โควตา)** · ช่องฟอร์ม **ไม่ถูก prefill** (block) | ☐ |
| 3 | TYPE เลขโควต้า Q-2569-199 + กรอกช่องที่เหลือ → CLICK **ยืนยันสร้าง** | — | ไม่บันทึก + toast เหลือง **สมาชิกนี้มีโควต้าอยู่แล้ว** | ☐ |
| 4 | VERIFY dropdown ค้นหาสมาชิก (ทั้งลิสต์) | — | แสดงเฉพาะสมาชิก **อนุมัติแล้ว** เท่านั้น (ไม่มี pending/rejected — ป้องกัน BR_MEMBER_NOT_APPROVED ที่ต้นทาง) | ☐ |

### TC-C05 — เลขโควต้าซ้ำ (negative — EC-02 / VR-05)
- group: C · ความสำคัญ: สูง · trace: AC-05 / EC-02 / BR_QUOTA_NUMBER_DUPLICATE / LOCK-03
- Setup: role=R-01 · seed=default (Q-2569-001 มีอยู่) · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**
- ชุดข้อมูล: B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "Q-2569-001" → ช่อง **เลขโควต้า** แล้ว CLICK ช่องอื่น (blur) | B4 | ข้อความแดงใต้ช่อง **เลขโควต้านี้ถูกใช้แล้ว** + กรอบช่องแดง (checkQuotaNumber on-blur) | ☐ |
| 2 | กรอกช่องที่เหลือ (ชุด A2) → CLICK **ยืนยันสร้าง** | — | ไม่บันทึก + error ใต้ช่องเลขโควต้าคงเดิม + toast เหลือง **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 3 | แก้เลขโควต้าเป็น Q-2569-102 → CLICK **ยืนยันสร้าง** → WAIT | — | บันทึกสำเร็จ toast **สร้างโควตาสำเร็จ — Q-2569-102 (No-Member)** | ☐ |

### TC-C06 — เลขบัตร ≠ 13 หลัก (negative — VR-01)
- group: C · ความสำคัญ: สูง · trace: AC-06 / VR-01 / ERR_VALIDATION_FAILED
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "12345" → ช่อง **เลขบัตรประชาชน** แล้ว CLICK **ยืนยันสร้าง** | B1 | ข้อความแดงใต้ช่อง **เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก** + กรอบช่องแดง | ☐ |
| 2 | TYPE "abc" ต่อในช่องเดิม | — | ตัวอักษรไม่ถูกพิมพ์ลงช่อง (รับเฉพาะตัวเลข — oninput strip) | ☐ |

### TC-C07 — เบอร์โทรผิดรูปแบบ (negative — VR-02)
- group: C · ความสำคัญ: กลาง · trace: AC-07 / VR-02
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "08123" → ช่อง **เบอร์โทรศัพท์** แล้ว CLICK **ยืนยันสร้าง** | B2 | ข้อความแดง **เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก** | ☐ |
| 2 | TYPE เพิ่มจนเป็น "0812345678" | — | *(หลังกรอกครบและ submit จะไม่ error ช่องนี้ — ยืนยันเฉพาะข้อความ error หายเมื่อ validate ซ้ำ)* | ☐ |

### TC-C08 — email optional + validate เมื่อกรอก (LOCK-11 / VR-03)
- group: C · ความสำคัญ: สูง · trace: AC-09 / LOCK-11 / VR-03
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "invalid-email" → ช่อง **อีเมล** แล้ว CLICK **ยืนยันสร้าง** | B3 | ข้อความแดง **รูปแบบอีเมลไม่ถูกต้อง** | ☐ |
| 2 | ลบค่าในช่อง **อีเมล** ให้ว่าง (helper "ไม่บังคับ") + กรอกชุด A2 ครบช่องอื่น → CLICK **ยืนยันสร้าง** → WAIT | A2 (email ว่าง) | บันทึกสำเร็จ toast **สร้างโควตาสำเร็จ — Q-2569-102 (No-Member)** — email ว่างไม่ block | ☐ |

### TC-C09 — required ครบชุด (negative — VR-04)
- group: C · ความสำคัญ: สูง · trace: AC-10 / VR-04
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** ทันที (ไม่กรอกอะไร) | — | ไม่บันทึก + error ครบ: **กรุณากรอกเลขโควต้า / กรุณากรอกชื่อ / กรุณากรอกนามสกุล / เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก / เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก / กรุณาเลือกจังหวัด / กรุณาเลือกอำเภอ / กรุณาเลือกตำบล** (×2 ชุดที่อยู่) + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | VERIFY ช่อง **อีเมล** | — | ไม่มี error (ไม่ใช่ required) | ☐ |

### TC-C10 — Dual address cascade + postal auto ×2 + reset แยกที่อยู่ (edge: VR-10 / VR-12)
- group: C · ความสำคัญ: สูง · trace: AC-08 / VR-10, VR-12 / cascade ×2 (current + id_card อิสระ)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง **อำเภอ/ตำบล** ของ **ที่อยู่ปัจจุบัน** ก่อนเลือกจังหวัด | — | เป็นสีเทา กดพิมพ์ไม่ได้ (disabled) | ☐ |
| 2 | ที่อยู่ปัจจุบัน: SELECT กาญจนบุรี → ท่าม่วง → วังขนาย | — | รหัสไปรษณีย์ (current) = **71110** (อัตโนมัติ, แก้ไม่ได้) | ☐ |
| 3 | ที่อยู่ตามบัตรประชาชน: SELECT ราชบุรี → บ้านโป่ง → ท่าผา | — | รหัสไปรษณีย์ (id_card) = **70110** · **ที่อยู่ปัจจุบันไม่ถูกกระทบ** (ยัง 71110 กาญจนบุรี) | ☐ |
| 4 | ที่อยู่ปัจจุบัน: SELECT จังหวัดใหม่ **สุพรรณบุรี** | — | ช่อง อำเภอ/ตำบล/ไปรษณีย์ ของ **ที่อยู่ปัจจุบัน** ถูกเคลียร์ (reset ลูกโซ่) · **ที่อยู่ตามบัตรประชาชนคงเดิม** (ราชบุรี/บ้านโป่ง/ท่าผา/70110) | ☐ |
| 5 | ที่อยู่ตามบัตรประชาชน: เปลี่ยน **อำเภอ** เป็น โพธาราม | — | ตำบล + ไปรษณีย์ ของ id_card ถูกเคลียร์ (จังหวัดคงเดิม ราชบุรี) · ที่อยู่ปัจจุบันไม่กระทบ | ☐ |

### TC-C11 — Double-click กันสร้างซ้ำ (edge: EC-16 / LOCK-06)
- group: C · ความสำคัญ: สูง · trace: AC-26 / EC-16 / BR-AGQ-09 (idempotency)
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา** → กรอกชุด A2 ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งเร็วที่สุด (double-click) | — | คลิกแรกปุ่มกลายเป็น **กำลังบันทึก…** + disabled — คลิกที่สองไม่มีผล | ☐ |
| 2 | WAIT จน toast ปรากฏ → VERIFY ตาราง | — | มีโควตาใหม่ **1 รายการเท่านั้น** (count = 9 รายการ, ไม่ใช่ 10) | ☐ |

### TC-C12 — เอกสารแนบ guard >5MB / ไม่ใช่ PDF/JPG/PNG (AC-13) (prototype mock)
- group: C · ความสำคัญ: กลาง · trace: AC-13 / BR-AGQ-12 · **หมายเหตุ: prototype เป็น mock (คลิกโซนแนบ = toast จำลอง) — guard ขนาด/ชนิดจริงทดสอบที่ระบบจริง (Document Storage) ตอน SIT**
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK โซน **เอกสารแนบ** (สำเนาบัตรประชาชน / สำเนาทะเบียนบ้าน) | — | toast info **จำลองแนบไฟล์ (PDF/JPG/PNG ≤5MB)** + helper "คลิกเพื่อแนบไฟล์ · รองรับ PDF/JPG/PNG ขนาดไม่เกิน 5MB" | ☐ |
| 2 | VERIFY (ระบบจริง — SIT) | — | แนบไฟล์ >5MB หรือชนิดอื่น (เช่น .exe) → block + ข้อความปฏิเสธ (config limit — ห้าม hardcode) | ☐ |

---

### TC-C13 — ค้นหาสมาชิก 0 match → ข้อความมาตรฐานสีแดง + email เป็น key (TC-287 / G2)
- group: C · ความสำคัญ: สูง · trace: TC-287 / FN-AT-AGQ-115 / API-13 · **prototype fixed แล้ว (email key + standard 0-match message)**
- Setup: role=R-01 · seed=default
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ที่ช่องค้นหาสมาชิก TYPE ค่าที่ไม่มีในระบบ (เช่น zzz-ไม่มีจริง) | — | ข้อความมาตรฐานสีแดง **ไม่พบข้อมูลสมาชิกที่ตรงกับคำค้นหา** · ฟอร์มไม่ prefill · **ยืนยันสร้าง** ยัง disabled/ไม่ผูก member | ☐ |
| 2 | ล้าง → TYPE **email** ของสมาชิก Approved จาก seed (email เป็น search key) | — | dropdown แสดงสมาชิกที่ email ตรง — พิสูจน์ว่า email ค้นได้ | ☐ |
| 3 | เลือกสมาชิกจากผล email | — | prefill ชื่อ/เลขบัตร/เบอร์/email/ที่อยู่ + member card | ☐ |

### TC-C14 — ค้นหาสมาชิก timeout → Retry (ไม่ prefill/Save) (TC-322 / G5) (ต้อง simulate)
- group: C · ความสำคัญ: สูง · trace: TC-322 / FN-AT-AGQ-115 / TIMEOUT · **prototype ไม่มี network — SIT case**
- Setup: **simulate — ระบบจริง:** FN-AT-AGQ-115 ตอบ TIMEOUT/DEPENDENCY ชั่วคราว · Create Drawer เปิด
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): ค้นหาสมาชิก แล้ว service ตอบ TIMEOUT (>500ms) | — | spinner → toast/banner ข้อความ TIMEOUT (ไทย) + ปุ่ม **Retry** | ☐ |
| 2 | VERIFY: กด **Retry** เมื่อ service กลับมา | — | เรียก FN-AT-AGQ-115 ใหม่ → คืน matches → prefill ตามปกติ | ☐ |
| 3 | VERIFY: การค้นที่ fail | — | **ไม่ prefill / Save ยัง disabled** + log attempt/retry telemetry | ☐ |

## Group I — CSV Import (OV-05 — No-Member เท่านั้น — LOCK-07)

### TC-I01 — ดาวน์โหลดแม่แบบ + modal ระบุ No-Member (AC-17 / LOCK-07)
- group: I · ความสำคัญ: สูง · trace: AC-17 / US-04 / 12 คอลัมน์
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Import CSV** | — | modal กลางจอ หัวข้อ **นำเข้าโควตาจากไฟล์ CSV (No-Member only)** + subtitle ".csv (UTF-8) ≤5MB · ทุกแถวสถานะ \"รออนุมัติ\" · เลขโควต้าไม่ซ้ำ · เลขบัตร 13 หลัก เบอร์ 9-12" | ☐ |
| 2 | VERIFY แถบบนใน modal | — | ข้อความ **ดาวน์โหลดแม่แบบ CSV** + ปุ่ม **ดาวน์โหลดแม่แบบ** (อยู่ *ใน* modal) | ☐ |
| 3 | CLICK ปุ่ม **ดาวน์โหลดแม่แบบ** | — | ได้ไฟล์ `quota_template.csv` — header 12 คอลัมน์: quota_number,first_name,last_name,citizen_id,phone,address,province,district,subdistrict,birth_date,marital_status,number_of_children + แถวตัวอย่าง 2 แถว (UTF-8 BOM — ไทยไม่เพี้ยน) | ☐ |
| 4 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ยังไม่ได้เลือกไฟล์) | ☐ |

### TC-I02 — Import แถวผสม → partial success + error report (happy — EC-04)
- group: I · ความสำคัญ: สูง · trace: AC-14 / EC-04 / BR-AGQ-10 · ทุกแถว unverified + No-Member
- Setup: role=R-01 · seed=default · files=`quota_mixed.csv` (6 แถว: 4 ดี 2 เสีย)
- Start: OPEN `#/quotas` → CLICK **Import CSV**
- ผ่านเมื่อ: แถวดีสร้างครบ แถวเสียรายงานพร้อม download ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เลือกไฟล์** → UPLOAD quota_mixed.csv | — | ชื่อไฟล์ + ขนาด (KB) แสดงข้างปุ่ม | ☐ |
| 2 | VERIFY สรุปผลตรวจ (preview — ก่อนเขียน) | — | 3 กล่อง: **แถวทั้งหมด 6** · **ผ่าน 4** · **ไม่ผ่าน 2** | ☐ |
| 3 | VERIFY ตารางข้อผิดพลาด | — | 2 แถว: ระบุ "แถว N" + ฟิลด์ + ข้อความ (**เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก** / **เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก**) | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันนำเข้า (4 แถว)** → WAIT | — | ปุ่มเป็น **กำลังนำเข้า…** → phase done: แถวทั้งหมด 6 / **สร้างสำเร็จ 4** / **ล้มเหลว 2** + toast **นำเข้าโควตา 4 รายการสำเร็จ — ข้าม 2 แถว** | ☐ |
| 5 | CLICK ปุ่ม **ดาวน์โหลดรายงาน** | — | ได้ไฟล์ `quota-upload-errors.csv` มี 2 แถว error | ☐ |
| 6 | CLICK **ปิด** → VERIFY ตาราง | — | โควตาใหม่ 4 แถวบนสุด ทุกแถว pill เหลือง **รออนุมัติ** + **ไม่มี link icon** (No-Member) · count = **12 รายการ** | ☐ |

### TC-I03 — File guard: นามสกุล + ขนาด (negative — VR-08)
- group: I · ความสำคัญ: สูง · trace: AC-15 / VR-08 / ERR_CSV_INVALID_FILE
- Setup: role=R-01 · seed=default · files=`notes.xlsx`, `quota_too_large.csv`
- Start: OPEN `#/quotas` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD notes.xlsx | — | toast แดง **กรุณาเลือกไฟล์ CSV เท่านั้น** — ไฟล์ไม่ถูกรับ | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD quota_too_large.csv | — | toast แดง **ขนาดไฟล์ต้องไม่เกิน 5MB** — ไฟล์ไม่ถูกรับ, ปุ่มยืนยันยัง disabled | ☐ |

### TC-I04 — Header ไม่ตรงแม่แบบ → reject ทั้งไฟล์ (edge: EC-10 / RC-02)
- group: I · ความสำคัญ: สูง · trace: EC-10 / BR_CSV_HEADER_MISMATCH / LOCK-07 / RC-02
- Setup: role=R-01 · seed=default · files=`quota_badheader.csv` (ขาดคอลัมน์ number_of_children)
- Start: OPEN `#/quotas` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD quota_badheader.csv | — | ไม่ขึ้น preview + toast แดง **ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ** (คอลัมน์ที่ขาด: number_of_children) | ☐ |
| 2 | VERIFY ตารางหลังปิด modal | — | ไม่มีแถวใดถูกสร้าง (count ยัง 8 รายการ) | ☐ |

### TC-I05 — เลขโควต้าซ้ำภายในไฟล์ + ซ้ำในระบบ (edge: EC-11 / RC-03)
- group: I · ความสำคัญ: กลาง · trace: EC-11 / BR_QUOTA_NUMBER_DUPLICATE / RC-03
- Setup: role=R-01 · seed=default · files=`quota_dupfile.csv`, `quota_dupdb.csv`
- Start: OPEN `#/quotas` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD quota_dupfile.csv | — | preview: ผ่าน 2 / ไม่ผ่าน 1 — แถวหลังของคู่ซ้ำ error **เลขโควต้าซ้ำภายในไฟล์ (แถว 2)** (แถวแรกของคู่ผ่าน) | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD quota_dupdb.csv | — | preview ใหม่: ผ่าน 1 / ไม่ผ่าน 1 — แถวซ้ำระบบ error **เลขโควต้าซ้ำ — มีในระบบแล้ว** | ☐ |

### TC-I06 — ตำบล/จังหวัด CSV สะกดผิด (edge: EC-13 / RC-04)
- group: I · ความสำคัญ: กลาง · trace: EC-13 / VR-10 / RC-04
- Setup: role=R-01 · seed=default · files=`quota_badsub.csv`
- Start: OPEN `#/quotas` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD quota_badsub.csv | — | ไม่ผ่าน 2: แถวแรก **ไม่พบตำบลในท่าม่วง** (สะกด "วังขนายย") · แถวสอง **ไม่พบจังหวัดในระบบ** (province "นครปฐม") | ☐ |
| 2 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ผ่าน 0 แถว) | ☐ |

### TC-I07 — ไฟล์ถูกทั้งหมด + postal เว้นว่างให้ระบบเติม (happy — AC-16)
- group: I · ความสำคัญ: กลาง · trace: AC-16 / VR-10 (auto)
- Setup: role=R-01 · seed=default · files=`quota_ok.csv` (3 แถว ไม่มีคอลัมน์ postal)
- Start: OPEN `#/quotas` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD quota_ok.csv | — | preview: ผ่าน 3 / ไม่ผ่าน 0 + แถบ **ทุกแถวผ่านการตรวจสอบ ไม่มีข้อผิดพลาด** | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (3 แถว)** → WAIT | — | phase done: สร้างสำเร็จ 3 + แถบ **อัปโหลดสำเร็จทั้งหมด ไม่มีข้อผิดพลาด** + toast เขียว | ☐ |
| 3 | CLICK **ปิด** → CLICK แถวโควตาใหม่คนแรก | — | detail: ที่อยู่ปัจจุบัน รหัสไปรษณีย์ = **71110** (ระบบเติมจากตำบลวังขนาย) | ☐ |

### TC-I08 — Encoding ไม่ใช่ UTF-8 (edge: EC-09 / RC-01) (ต้อง simulate)
- group: I · ความสำคัญ: ต่ำ · trace: EC-09 / ERR_CSV_ENCODING / RC-01 · **หมายเหตุ: prototype (client mock) อ่านเป็น UTF-8 — ภาษาไทยเพี้ยนแล้วตกที่ validation จังหวัด/ตำบลแทน; ระบบจริง reject ทั้งไฟล์**
- Setup: role=R-01 · seed=default · files=`quota_tis620.csv`
- Start: OPEN `#/quotas` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD quota_tis620.csv | — | **ระบบจริง:** reject ทั้งไฟล์ "ไฟล์ต้องเป็น UTF-8 กรุณาบันทึกไฟล์ใหม่เป็น UTF-8" · **prototype:** ยอมรับได้ว่าแถวตกที่ "ไม่พบจังหวัด/ตำบล" (ไทยเพี้ยน) — mark BLOCKED ถ้าไม่ตรงทั้งสองแบบ | ☐ |

---

### TC-I09 — CSV per-row idempotency: rerun ไฟล์เดิม → คืนผลเดิม · batch เดิม+ไฟล์ต่าง → CONFLICT (TC-304 / G3) (ต้อง simulate)
- group: I · ความสำคัญ: สูง · trace: TC-304 / FN-AT-AGQ-126 / FN-SEQ-AGQ-132 / BR-AGQ-10 · **prototype validate ฝั่ง client — idempotency เป็น server semantics = SIT**
- Setup: **simulate — ระบบจริง:** key `FN-AT-AGQ-126:{source_file_hash}:{row_index}`
- Start: — (SIT) / prototype: ตรวจ per-row validate ปกติ (TC-I02)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): upload ไฟล์ CSV (file_hash H1) ครั้งแรก | — | ได้ report + per-row quota_ids (created) | ☐ |
| 2 | VERIFY: upload ไฟล์เดิม (source_file_hash H1) ซ้ำ | — | per-row idempotency hit → **คืนผลเดิม ไม่สร้าง duplicate** + message **ไฟล์นี้ถูกประมวลผลแล้ว — คืนผลเดิม** | ☐ |
| 3 | VERIFY: rerun ด้วย **same batch_id แต่ไฟล์เนื้อหาต่าง (hash ต่าง)** | — | **409 CONFLICT** + UI อธิบายชัดเจน | ☐ |

## Group V — ตรวจสอบยืนยัน (OV-03)

### TC-V01 — Approve เดี่ยว (happy — LOCK-02)
- group: V · ความสำคัญ: สูง · trace: AC-20 / US-06 / BR-AGQ-04
- Setup: role=R-02 (prototype: user เดียวกดได้) · seed=default (Q-2569-004 unverified, No-Member) · files=—
- Start: OPEN `#/quotas/Q-2569-004`
- ผ่านเมื่อ: pill เปลี่ยนเขียว + ประวัติมี event อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer | — | ชื่อ **ทองคำ ไร่งาม** + pill เหลือง **รออนุมัติ** + ปุ่ม **แก้ไข / ตรวจสอบ / ลบ** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบ** | — | modal **ตรวจสอบโควตา** — subtitle "เลือกผลการตรวจสอบ (หมายเหตุไม่บังคับ)" + เลขโควต้า + ชื่อ + "โควตาแบบไม่ผูกสมาชิก" + radio 2 ตัว (อนุมัติ/ปฏิเสธ) | ☐ |
| 3 | CLICK ตัวเลือก **อนุมัติ** | — | ตัวเลือกไฮไลต์เขียว · ช่องหมายเหตุ label "หมายเหตุ (ไม่บังคับ)" | ☐ |
| 4 | CLICK ปุ่ม **ยืนยัน** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast เขียว **อนุมัติเรียบร้อย** + pill ใน drawer/ตารางเปลี่ยนเป็นเขียว **อนุมัติ** | ☐ |
| 6 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — อนุมัติ** โดย ประวิทย์ ตรวจการ | ☐ |

### TC-V02 — Reject **ไม่กรอกเหตุผล → ผ่านได้** (LOCK-09 ★ ตรงข้าม Farmer)
- group: V · ความสำคัญ: สูงสุด · trace: AC-21 / BR-AGQ-05 / LOCK-09 / OQ-Q1
- Setup: role=R-02 · seed=default (Q-2569-005 unverified, No-Member) · files=—
- Start: OPEN `#/quotas/Q-2569-005` → CLICK **ตรวจสอบ**
- ผ่านเมื่อ: กด ปฏิเสธ + note ว่าง → ยืนยันผ่าน (ไม่ block) — ยืนยันว่าต่างจาก Farmer ที่บังคับ note

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวเลือก **ปฏิเสธ** | — | ไฮไลต์แดง · ช่องหมายเหตุ label ยังเป็น **หมายเหตุ (ไม่บังคับ)** — **ไม่มี * บังคับ** | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** โดย **ไม่กรอกหมายเหตุ** → WAIT | — | **ผ่านได้** (ไม่ block) + toast เขียว **ปฏิเสธเรียบร้อย** + pill แดง **ไม่อนุมัติ** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ไม่อนุมัติ** โดย ประวิทย์ ตรวจการ (ไม่มีกล่อง note — เว้นว่างได้) | ☐ |

### TC-V03 — Reject พร้อมเหตุผล → note แสดงใน detail
- group: V · ความสำคัญ: สูง · trace: AC-21 / LOCK-02
- Setup: role=R-02 · seed=default (Q-2569-007 unverified) · files=—
- Start: OPEN `#/quotas/Q-2569-007` → CLICK **ตรวจสอบ** → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "เอกสารไม่ครบ ขอสำเนาบัตร" → ช่องหมายเหตุ → CLICK **ยืนยัน** → WAIT | — | toast **ปฏิเสธเรียบร้อย** + pill แดง **ไม่อนุมัติ** | ☐ |
| 2 | VERIFY Tab **ข้อมูลทั่วไป** (ท้ายกลุ่ม) | — | กล่อง **เหตุผลที่ไม่อนุมัติ: เอกสารไม่ครบ ขอสำเนาบัตร** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ไม่อนุมัติ** + กล่อง note "เอกสารไม่ครบ ขอสำเนาบัตร" | ☐ |

### TC-V04 — ไม่เลือกผลตรวจสอบ (negative — VR-09)
- group: V · ความสำคัญ: กลาง · trace: VR-09 / ERR_VALIDATION_FAILED
- Setup: role=R-02 · seed=default (Q-2569-008 unverified) · files=—
- Start: OPEN `#/quotas/Q-2569-008` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยัน** ทันที (ยังไม่เลือก radio) | — | ไม่ดำเนินการ + error ใต้ radio **กรุณาเลือกผลการตรวจสอบ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V05 — Bulk verify กลุ่ม + รายการถูกตรวจก่อน (edge: EC-12 / AC-23)
- group: V · ความสำคัญ: สูง · trace: AC-23 / EC-12 / US-07 · **EC-12 per-record (มีคนที่สอง verify ก่อน) = SIT — prototype ตรวจเส้น happy**
- Setup: role=R-02 · seed=default (unverified 5) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox หัวตาราง (เลือก unverified ทั้ง 5) → CLICK ปุ่ม **ตรวจสอบที่เลือก (5)** | — | modal **ตรวจสอบโควตาทั้งหมด** + list "รายการที่เลือก (5 รายการ)" แสดงเลขโควต้า + ชื่อ ครบ 5 | ☐ |
| 2 | CLICK **อนุมัติ** → CLICK ปุ่ม **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 5 ล้มเหลว 0** | ☐ |
| 3 | VERIFY ตาราง + stats | — | ไม่มีแถว pill เหลืองเหลือ · การ์ด **รออนุมัติ 0** · **อนุมัติ 7** · ปุ่มหัวกลับเป็น (0) disabled | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | กรณีบางรายการถูก verify ก่อน: toast "สำเร็จ X ล้มเหลว Y ([Q] ถูกตรวจสอบไปแล้ว)" — รายการอื่นสำเร็จตามปกติ (per-record) | ☐ |

### TC-V06 — Verify รายการที่ไม่ใช่ unverified (negative — BR-AGQ-04) (ต้อง simulate ส่วน 422)
- group: V · ความสำคัญ: กลาง · trace: AC-22 / BR_VERIFY_NOT_UNVERIFIED
- Setup: role=R-02 · seed=default · **UI ซ่อนปุ่มตรวจสอบสำหรับ verified/rejected — ส่วน 422 server ต้องยิง API ตรง (SIT)**
- Start: OPEN `#/quotas/Q-2569-001` (verified)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบนหัว view drawer | — | มีเฉพาะ **แก้ไข** + X — **ไม่มีปุ่ม ตรวจสอบ / ลบ** (สถานะอนุมัติ) | ☐ |
| 2 | OPEN `#/quotas/Q-2569-006` (rejected) → VERIFY ปุ่ม | — | เช่นเดียวกัน: ไม่มีปุ่ม ตรวจสอบ/ลบ | ☐ |
| 3 | VERIFY (ระบบจริง — SIT) | — | POST verify กับ record verified → 422 **รายการนี้ถูกตรวจสอบไปแล้ว** | ☐ |

---

### TC-V07 — Verify modal a11y: focus-trap + aria-modal + aria-live (TC-316 / G8) (ต้อง simulate a11y)
- group: V · ความสำคัญ: กลาง · trace: TC-316 / AC-36 · **โครงสร้าง modal ตรวจบน prototype ได้บางส่วน (focus/Esc) · aria/screen-reader = SIT**
- Setup: role=R-02 · seed=default (มี unverified)
- Start: OPEN `#/quotas` → เลือกแถวรออนุมัติ → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด Verify modal → ดู focus แรก | — | focus เลื่อนไป radio ผลการตรวจสอบ (อนุมัติ/ปฏิเสธ) | ☐ |
| 2 | กด Tab วนใน modal | — | focus **วนอยู่ใน modal (focus-trap)** ออกไปนอก modal ไม่ได้ · กด Esc → ปิด (หรือ confirm ถ้า dirty) | ☐ |
| 3 | VERIFY (a11y — SIT): ตรวจ attribute | — | modal มี `aria-modal="true"` + `aria-labelledby`(title "ตรวจสอบโควตา") + `aria-live` ประกาศ success/fail · reject danger-variant อ่านคำเตือนคืนสถานะ | ☐ |

### TC-V08 — Bulk verify large set: throughput + progress + summary (TC-312 / G10) (ต้อง simulate)
- group: V · ความสำคัญ: สูง · trace: TC-312 / AC-34 / FN-AT-AGQ-124 · **prototype seed เล็ก — NFR large-set = SIT**
- Setup: **simulate — ระบบจริง:** dataset 1,000 Pending Approval · FN-AT-AGQ-124 batched
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): เลือก 1,000 รายการ unverified → bulk verify | — | batched writes + per-row optimistic retry ≤3 บน CONFLICT | ☐ |
| 2 | VERIFY: วัด elapsed / per-row avg / error rate | — | คืน summary ภายใน operational timeout (บันทึกค่าที่วัดได้ / SLA) | ☐ |
| 3 | VERIFY: UI | — | แสดง **progress ระหว่างทำงาน** + final summary สำเร็จ X/ล้มเหลว Y + เหตุผลรายรายการ | ☐ |

## Group E — แก้ไข + State machine (OV-02 — OQ-Q3 ★)

### TC-E01 — แก้ไขโควตา unverified → สถานะคงเดิม + โหลดค่าเดิม (happy)
- group: E · ความสำคัญ: สูง · trace: AC-24 / US-08 / FN-03
- Setup: role=R-01 · seed=default (Q-2569-004 unverified, No-Member) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว Q-2569-004 | — | drawer **แก้ไขโควตา Q-2569-004** เปิด — sub "สถานะ: รออนุมัติ · เวอร์ชัน 1" · แถบเตือน **โควตาแบบไม่ผูกสมาชิก (No-Member)** · ทุกช่องมีค่าเดิม (ทองคำ / ไร่งาม / 0822223333) | ☐ |
| 2 | TYPE แก้ช่อง **เบอร์โทรศัพท์** เป็น "0899999999" | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + แถว Q-2569-004 ยัง pill เหลือง **รออนุมัติ** (ไม่เปลี่ยนสถานะ) + เบอร์ในตาราง = 0899999999 | ☐ |
| 4 | OPEN `#/quotas/Q-2569-004` → CLICK Tab **ประวัติ** | — | มีรายการ **แก้ไขข้อมูล** เพิ่มบนสุด · เวอร์ชันใน footer = 2 | ☐ |

### TC-E02 — แก้ไข Rejected → **ยังคง rejected** (OQ-Q3 ★ ตรงข้าม Farmer LOCK-06)
- group: E · ความสำคัญ: สูงสุด · trace: AC-24 / OQ-Q3 / §5.2 (edit ไม่เปลี่ยนสถานะ)
- Setup: role=R-01 · seed=default (Q-2569-006 rejected, note "สำเนาบัตรไม่ชัด") · files=—
- Start: OPEN `#/quotas/Q-2569-006`
- ผ่านเมื่อ: แก้แล้วบันทึก → สถานะยัง **ไม่อนุมัติ** (ไม่กลับ pending อัตโนมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Tab **ข้อมูลทั่วไป** | — | pill แดง **ไม่อนุมัติ** + กล่อง **เหตุผลที่ไม่อนุมัติ: สำเนาบัตรไม่ชัด** | ☐ |
| 2 | CLICK ปุ่ม **แก้ไข** → sub ของ drawer | — | "สถานะ: ไม่อนุมัติ · เวอร์ชัน N" — **ไม่มีแถบแจ้งว่าจะกลับเข้าคิว** (ต่างจาก Farmer) | ☐ |
| 3 | TYPE แก้ช่อง **ที่อยู่ปัจจุบัน** → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** | ☐ |
| 4 | VERIFY แถว Q-2569-006 ในตาราง | — | pill **ยังเป็นแดง ไม่อนุมัติ** (ไม่กลับ รออนุมัติ) · การ์ดไม่อนุมัติยัง 1, รออนุมัติไม่เพิ่ม | ☐ |
| 5 | OPEN `#/quotas/Q-2569-006` → Tab **ข้อมูลทั่วไป** | — | กล่อง **เหตุผลที่ไม่อนุมัติ** ยังคงอยู่ (note ไม่ถูกเคลียร์) | ☐ |

### TC-E03 — แก้ Verified → สถานะคงเดิม
- group: E · ความสำคัญ: สูง · trace: AC-24 / §5.2
- Setup: role=R-01 · seed=default (Q-2569-002 verified, From-Member FM-000014) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว Q-2569-002 | — | drawer แก้ไขเปิด · sub "สถานะ: อนุมัติ · เวอร์ชัน N" · แถบฟ้า **โควตานี้ผูกกับสมาชิก FM-000014 (แก้ไขการผูกไม่ได้ในหน้านี้)** | ☐ |
| 2 | TYPE แก้ช่อง **ผู้รับผลประโยชน์** → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + pill ยังเขียว **อนุมัติ** | ☐ |
| 3 | OPEN `#/quotas/Q-2569-002` → Tab **ประวัติ** | — | มีรายการ **แก้ไขข้อมูล** ใหม่ — รายการอนุมัติเดิมยังอยู่ (history immutable) | ☐ |

### TC-E04 — แก้แล้วชนเลขโควต้าซ้ำ (negative — VR-05 exclude self)
- group: E · ความสำคัญ: กลาง · trace: VR-05 / BR_QUOTA_NUMBER_DUPLICATE / LOCK-03
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas` → CLICK ดินสอแถว Q-2569-004

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกการแก้ไข** โดยไม่แก้อะไร | — | บันทึกสำเร็จ (เลขโควต้าเดิมของตัวเอง **ไม่**นับเป็นซ้ำ — exclude self) | ☐ |
| 2 | CLICK ดินสอแถว Q-2569-004 อีกครั้ง → TYPE เลขโควต้าเป็น "Q-2569-001" (ของแถวอื่น) แล้ว blur → CLICK **บันทึกการแก้ไข** | — | ไม่บันทึก + error ใต้ช่องเลขโควต้า **เลขโควต้านี้ถูกใช้แล้ว** | ☐ |

---

## Group D — ลบ (soft — OV-04 — LOCK-08)

### TC-D01 — ลบโควตา unverified No-Member (happy — LOCK-08)
- group: D · ความสำคัญ: สูง · trace: AC-27 / BR-AGQ-06 / US-09
- Setup: role=R-01 · seed=default (Q-2569-005 unverified, No-Member) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า การ์ด **โควตาทั้งหมด** และ **รออนุมัติ** | — | บันทึก: ทั้งหมด=8, รออนุมัติ=5 (อ้างใน step 5) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว Q-2569-005 | — | modal แดง **ลบโควตา?** + ข้อความ `ต้องการลบ "Q-2569-005 — ประนอม ใจเพชร" ใช่หรือไม่ การลบไม่สามารถย้อนกลับได้` + กล่องเตือน soft delete (No-Member ไม่มีข้อความคืนสถานะ) | ☐ |
| 3 | CLICK ปุ่ม **ลบ** (แดง) | — | ปุ่มเป็น **กำลังลบ…** | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast **ลบโควตาแล้ว** (No-Member — ไม่มีคำท้าย "คืนสถานะ...") + แถว Q-2569-005 หายจากตาราง | ☐ |
| 5 | VERIFY stats | — | ทั้งหมด=7 · รออนุมัติ=4 — soft-deleted ไม่นับ | ☐ |
| 6 | OPEN `#/quotas/Q-2569-005` (route ตรง) | — | ไม่เปิด detail — เด้งกลับ `#/quotas` (รายการถูกลบ) | ☐ |

### TC-D02 — ไม่มีปุ่มลบสำหรับ verified/rejected + guard toast (negative — EC-03)
- group: D · ความสำคัญ: สูง · trace: AC-27 / EC-03 / BR_DELETE_NOT_UNVERIFIED
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **การดำเนินการ** แถว Q-2569-001 (อนุมัติ) | — | มีเฉพาะไอคอนดินสอ — **ไม่มีถังขยะ** | ☐ |
| 2 | VERIFY แถว Q-2569-006 (ไม่อนุมัติ) | — | ไม่มีถังขยะเช่นกัน | ☐ |
| 3 | OPEN `#/quotas/Q-2569-001` → VERIFY ปุ่มหัว drawer | — | มีเฉพาะ **แก้ไข** — ไม่มีปุ่ม **ลบ** | ☐ |

### TC-D03 — Guard ลบรายการไม่ใช่ unverified (server guard) (ต้อง simulate)
- group: D · ความสำคัญ: กลาง · trace: EC-03 / BR_DELETE_NOT_UNVERIFIED · **UI ไม่มีปุ่มลบให้อยู่แล้ว; ถ้ามีเส้นทางเรียก openDeleteModal กับ record ที่ verified → toast "ลบได้เฉพาะรายการที่รออนุมัติ" (client guard) · ส่วน 422 server = SIT**
- Setup: role=R-01 · seed=default
- Start: — (SIT / client guard)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (client guard) เรียก openDeleteModal กับ Q-2569-001 (verified) | — | modal **ไม่เปิด** + toast แดง **ลบได้เฉพาะรายการที่รออนุมัติ** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): DELETE /quotas/:id ของ record verified | — | 422 **ลบได้เฉพาะรายการที่รออนุมัติ** — record ไม่ถูกลบ | ☐ |

---

## Group W — รายละเอียด / ประวัติ (P-02 — 3 tabs)

### TC-W01 — View detail ครบ 3 tabs + member card (linked)
- group: W · ความสำคัญ: สูง · trace: AC-28, AC-29 / US-10
- Setup: role=R-01 · seed=default (Q-2569-001 From-Member FM-000002) · files=—
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว Q-2569-001 | — | view drawer: eyebrow "โควตาชาวไร่ · Q-2569-001" + ชื่อ **สมหญิง รักดี** + pill เขียว **อนุมัติ** หลังชื่อ | ☐ |
| 2 | VERIFY member card (บนสุด ใต้หัว) | — | การ์ดสีส้มอ่อน **ผูกกับสมาชิก FM-000002 · สมหญิง รักดี · 0823456789** + ปุ่ม **ดูสมาชิก** (teal) | ☐ |
| 3 | VERIFY Tab **ข้อมูลทั่วไป** | — | กลุ่ม **ข้อมูลส่วนบุคคล** (เลขบัตรเต็ม) · **ที่อยู่ปัจจุบัน** · **ที่อยู่ตามบัตรประชาชน** · **ข้อมูลธนาคาร** (เลขบัญชี/ธ.ก.ส. masked) | ☐ |
| 4 | CLICK Tab **ไฟล์ที่อัปโหลด** / Tab **ประวัติ** | — | ไฟล์: "ยังไม่มีไฟล์อัปโหลด" (seed ว่าง) · ประวัติ: timeline · footer "อัปเดตล่าสุด … · เวอร์ชัน N" + ปุ่ม **ปิด** | ☐ |
| 5 | CLICK ปุ่ม **ดูสมาชิก** | — | toast info **จำลองเปิดหน้าสมาชิก FM-000002** (prototype standalone — deep-link จริงตอน deploy รวม 2 features) | ☐ |

### TC-W02 — member card No-Member
- group: W · ความสำคัญ: กลาง · trace: AC-28 / member card No-Member state
- Setup: role=R-01 · seed=default (Q-2569-004 No-Member) · files=—
- Start: OPEN `#/quotas/Q-2569-004`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY member card | — | กล่องเทา **โควตาแบบไม่ผูกสมาชิก (No-Member)** — **ไม่มี**ปุ่ม ดูสมาชิก | ☐ |

### TC-W03 — Timeline ประวัติครบทุก event (LOCK-10)
- group: W · ความสำคัญ: สูง · trace: AC-28 / S01-07 append-only
- Setup: role=R-01 · seed=default (Q-2569-006 rejected — create + reject) · files=—
- Start: OPEN `#/quotas/Q-2569-006` → CLICK Tab **ประวัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY timeline | — | เรียงใหม่→เก่า: **ตรวจสอบ — ไม่อนุมัติ** (จุดแดง + note "สำเนาบัตรไม่ชัด" + โดย ประวิทย์ ตรวจการ) → **สร้างโควตา** (โดย สมพร วงศ์ทะเบียน) — ทุกรายการมีวันเวลา | ☐ |

### TC-W04 — Route refresh-safe `#/quotas/:quota_number`
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / refresh-safe
- Setup: role=R-01 · seed=default · files=—
- Start: OPEN `#/quotas/Q-2569-003` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/quotas/Q-2569-003` | — | หน้า list โหลด + view drawer ของ **บุญมา ทุ่งกว้าง** เปิดเองทันที | ☐ |
| 2 | PRESS F5 (refresh ทั้งหน้า) | — | กลับมาที่เดิม — drawer Q-2569-003 ยังเปิด (refresh-safe) | ☐ |
| 3 | CLICK พื้นหลังมืดนอก drawer (backdrop) | — | drawer ปิด + route = `#/quotas` | ☐ |

---

### TC-W05 — Attachment in-app preview + btn-open-original fallback (TC-313 / G7) (ต้อง simulate)
- group: W · ความสำคัญ: กลาง · trace: TC-313 / AC-35 · **prototype Attachments tab เป็น download-link — preview/signed-URL = SIT**
- Setup: **simulate — ระบบจริง:** quota มีไฟล์แนบ · storage คืน signed URL
- Start: — (SIT) / prototype: OPEN detail → Tab **ไฟล์ที่อัปโหลด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): คลิก thumbnail ไฟล์แนบ | — | client fetch signed URL → เปิด **preview modal (iframe/pdf viewer)** + แสดง name/size/mime (UTF-8 filename) | ☐ |
| 2 | VERIFY: preview fail (CSP/format block) | — | แสดงปุ่ม **`btn-open-original`** (fallback) | ☐ |
| 3 | VERIFY: คลิก `btn-open-original` | — | เปิด signed URL ใน tab ใหม่ + ดาวน์โหลดไฟล์ได้ | ☐ |

## Group X — Cross-module write-back ⭐ (06_TESTS §6.9 — the highlight)

> prototype จำลอง write-back ในหน่วยความจำผ่าน `writeMemberQuotaStatus()` — พิสูจน์ได้บนจอผ่าน (ก) toast คำท้าย "— คืนสถานะโควตาสมาชิกแล้ว" (ข) history event **อัปเดตสถานะโควตาของสมาชิก** (จุดส้ม) note "สมาชิก [FM]: สถานะโควตา → มี/ไม่มีโควตา" · การ reconcile ไปยัง Farmer feature จริง = `(ต้อง simulate)` ที่ SIT

### TC-X01 — สร้าง From-Member → member.quota_status = has_quota (XT-03)
- group: X · ความสำคัญ: สูงสุด · trace: XT-03 / AC-01 / BR-AGQ-07 / LOCK-05
- Setup: role=R-01 · seed=default (FM-000007 no_quota) · files=—
- Start: OPEN `#/quotas` → CLICK **สร้างโควตา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ค้นหาสมาชิก → เลือก **สายชล น้ำใจงาม (FM-000007)** → TYPE เลขโควต้า Q-2569-107 → กรอกที่อยู่ตามบัตร → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างโควตาสำเร็จ — Q-2569-107 (สมาชิก FM-000007 → มีโควตา)** | ☐ |
| 2 | CLICK แถว Q-2569-107 → Tab **ประวัติ** | — | มี event **อัปเดตสถานะโควตาของสมาชิก** (จุดส้ม) note **สมาชิก FM-000007: สถานะโควตา → มีโควตา** + event สร้างโควตา | ☐ |
| 3 | ทดสอบ 1:0..1 ต่อเนื่อง: CLICK **สร้างโควตา** → ค้นหา → เลือก FM-000007 อีกครั้ง | — | แถบแดง **สมาชิกนี้มีโควต้าอยู่แล้ว** (เพราะเพิ่งถูกเขียน has_quota) — พิสูจน์ว่า write-back สะท้อนกลับใน memberQuota แล้ว | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | Farmer detail FM-000007 แสดง "มีโควตา" (ENG-EXT-03 PATCH เป็น step แยก idempotent หลัง quota commit — keep-quota, ไม่ rollback) | ☐ |

### TC-X02 — Reject โควตา linked → member.quota_status = no_quota (XT-01) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-21b / EC-08 / BR-AGQ-07 / LOCK-05
- Setup: role=R-01+R-02 · seed=default · files=— · **ต้องสร้างโควตา From-Member ก่อน (seed ไม่มี unverified+linked)**
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้าง From-Member: CLICK **สร้างโควตา** → เลือก **ทองดี พูลผล (FM-000008)** → เลขโควต้า Q-2569-108 → กรอกที่อยู่ → **ยืนยันสร้าง** → WAIT | — | สร้างสำเร็จ (FM-000008 → มีโควตา) · แถว Q-2569-108 unverified + link icon | ☐ |
| 2 | OPEN `#/quotas/Q-2569-108` → CLICK **ตรวจสอบ** → CLICK **ปฏิเสธ** | — | modal แสดง warning **การปฏิเสธจะคืนค่าสถานะโควตาของสมาชิกที่ผูกไว้กลับเป็น ไม่มีโควตา** | ☐ |
| 3 | CLICK **ยืนยัน** (note เว้นว่างได้) → WAIT | — | toast เขียว **ปฏิเสธเรียบร้อย — คืนสถานะโควตาสมาชิกแล้ว** + pill แดง **ไม่อนุมัติ** | ☐ |
| 4 | CLICK Tab **ประวัติ** | — | event **อัปเดตสถานะโควตาของสมาชิก** note **สมาชิก FM-000008: สถานะโควตา → ไม่มีโควตา** + event ตรวจสอบ — ไม่อนุมัติ | ☐ |
| 5 | พิสูจน์ reconcile: CLICK **สร้างโควตา** → ค้นหา → เลือก **ทองดี พูลผล (FM-000008)** | — | **prefill ได้ตามปกติ** (ไม่ขึ้น block มีโควตาแล้ว) — พิสูจน์ว่า write-back คืน no_quota แล้ว | ☐ |
| 6 | VERIFY (ระบบจริง — SIT) | — | Farmer detail FM-000008 แสดง "ไม่มีโควตา" + history event=quota_status_written | ☐ |

### TC-X03 — ลบโควตา linked → member.quota_status = no_quota (XT-02) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-02 / AC-27 / EC-08 / BR-AGQ-07 / LOCK-05
- Setup: role=R-01 · seed=default · files=— · **สร้าง From-Member ก่อน**
- Start: OPEN `#/quotas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้าง From-Member: CLICK **สร้างโควตา** → เลือก **คำปอง อินทร์ตา (FM-000012)** → เลขโควต้า Q-2569-112 → กรอกที่อยู่ → **ยืนยันสร้าง** → WAIT | — | สร้างสำเร็จ (FM-000012 → มีโควตา) · แถว unverified + link icon | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว Q-2569-112 | — | modal **ลบโควตา?** + กล่องเตือน **... จะคืนค่าสถานะโควตาของสมาชิก FM-000012 เป็น ไม่มีโควตา** | ☐ |
| 3 | CLICK **ลบ** → WAIT | — | toast **ลบโควตาแล้ว — คืนสถานะโควตาสมาชิกแล้ว** + แถวหายจากตาราง | ☐ |
| 4 | พิสูจน์ reconcile: CLICK **สร้างโควตา** → ค้นหา → เลือก **คำปอง อินทร์ตา (FM-000012)** | — | prefill ได้ตามปกติ (ไม่ block) — write-back คืน no_quota แล้ว | ☐ |
| 5 | VERIFY (ระบบจริง — SIT) | — | Farmer detail FM-000012 = "ไม่มีโควตา" (write-back เป็น step แยก idempotent หลัง soft delete — ไม่ rollback) | ☐ |

### TC-X04 — reject/delete แต่ member ถูกลบก่อน → skip + log (XT-04 / EC-17 / RC-06) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-04 / EC-17 / RC-06 / OQ-F03 · **prototype: MEMBERS เป็น const ลบสมาชิกไม่ได้ — SIT case**
- Setup: role=R-01 · **simulate — ระบบจริง:** โควตา linked กับ member ที่ถูก soft-delete ไปแล้ว จากนั้น reject/delete โควตา
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): reject/delete โควตา linked ที่ member หายไปแล้ว | — | quota mutation **สำเร็จ** (ไม่ error) + write-back **skip** + log anomaly (คู่ quota↔member ไม่ตรง) — ไม่ปล่อยเงียบ (retry queue OQ-F03) | ☐ |
| 2 | VERIFY reconcile report | — | MET-03 จับคู่ quota_status ระหว่าง Quota↔Farmer — รายการ skip ถูก flag | ☐ |

### TC-X05 — Reconcile Farmer detail แสดงสถานะโควตา (ต้อง simulate)
- group: X · ความสำคัญ: กลาง · trace: BR-AGQ-07 / MET-03 · **Farmer เป็นคนละ feature/ไฟล์ — cross-check ที่ SIT (รวม 2 features)**
- Setup: **simulate** · Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): หลัง create From-Member / reject-linked / delete-linked | — | เปิด Farmer feature `#/members/:id` → **สถานะโควตา** ตรงกับที่ Quota เขียน (มีโควตา / ไม่มีโควตา) ทุกเคส | ☐ |

---

### TC-X06 — Reject linked แต่ member-API fail → schedule retry + banner, ไม่ rollback (TC-297 / G1/G5) (ต้อง simulate)
- group: X · ความสำคัญ: สูงสุด · trace: TC-297 / AC-31 / XT-05 / BR-AGQ-07 / FN-AT-AGQ-127 · **prototype write-back mock สำเร็จเสมอ — failure path = SIT**
- Setup: **simulate — ระบบจริง:** FN-AT-AGQ-127 ตอบ timeout/502 ตอน reject linked quota
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): Reject quota ที่ linked_member_id != null แต่ member service ตอบ timeout/502 | — | quota.verify_status = **Rejected** ยังคงถูก set + บันทึก verified_by/at/note (**ไม่ rollback**) | ☐ |
| 2 | VERIFY: state ของ revert | — | emit `quota.member_revert_needed` หรือบันทึก pending_revert flag เพื่อ worker retry (idempotent) | ☐ |
| 3 | VERIFY: UI หลังปิด modal | — | non-blocking banner **การคืนสถานะสมาชิกล้มเหลว จะทำการ retry อัตโนมัติ** + ลิงก์ดูสถานะ retry | ☐ |

### TC-X07 — FN-AT-AGQ-127 idempotent + retry (create has_quota scheduled_retry) (TC-323 / G1/G5) (ต้อง simulate)
- group: X · ความสำคัญ: สูงสุด · trace: TC-323 / AC-30 / XT-05 / FN-SEQ-AGQ-128 / FN-AT-AGQ-127 · **SIT — failure + retry-worker path**
- Setup: **simulate — ระบบจริง:** create-from-member; external member service fail ชั่วคราวแล้วกลับมา
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): create From-Member สำเร็จ + member service สำเร็จ | — | member.quota_status = has_quota + emit `member.quota_status.changed` | ☐ |
| 2 | VERIFY: member service fail (502/timeout) ตอนเขียน has_quota | — | **quota create สำเร็จ (ไม่ rollback)** + response `member_update_status=scheduled_retry` + UI non-blocking banner + persist retry task | ☐ |
| 3 | VERIFY: retry worker เรียก FN-AT-AGQ-127 อีกครั้งแล้วสำเร็จ | — | member.quota_status → has_quota + event emitted + audit นับ attempt | ☐ |
| 4 | VERIFY: re-run ด้วย idempotency_key เดิม | — | external treat idempotent — **ไม่มี duplicate side-effect** | ☐ |

## Group P — Permission / SoD

### TC-P01 — SoD: ผู้สร้างห้าม verify ตัวเอง (edge: EC-15 / RC-05) (ต้อง simulate)
- group: P · ความสำคัญ: กลาง · trace: EC-15 / RC-05 / ERR_SOD_SELF_VERIFY / OQ-Q6 · **prototype ไม่มี role switching (Drift D-04) — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง:** feature flag `sod_self_verify_block` ทดสอบทั้ง on/off
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — flag ON): verify โควตาที่ตนเองสร้าง | — | block 403 + **ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง** | ☐ |
| 2 | VERIFY (ระบบจริง — flag OFF) | — | ผ่านได้ แต่ log anomaly (self-verify attempt) | ☐ |

---

## Group K — Concurrency / Idempotency (LOCK-06)

### TC-K01 — Optimistic lock CONFLICT (edge: EC-07 / AC-25) (ต้อง simulate)
- group: K · ความสำคัญ: สูง · trace: AC-25 / EC-07 / VR-11 / ERR_STALE_DATA / BR-AGQ-09 · **prototype single-session ทำไม่ได้ (Drift D-03) — SIT case · idempotency double-click ตรวจแล้วใน TC-C11**
- Setup: **simulate — ระบบจริง:** 2 sessions — A แก้ record + save ก่อน, B ที่เปิดค้างไว้ save ทีหลังด้วย expected_version เก่า
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B กด **บันทึกการแก้ไข** หลัง A save ไปแล้ว | — | 409 + toast แดง **ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง** — ข้อมูลของ A ไม่ถูกทับ | ☐ |
| 2 | VERIFY (ระบบจริง): scenario เดียวกันกับ verify (A approve ก่อน B) | — | B ได้ 409/422 — สถานะที่ A ตั้งไว้คงเดิม | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `quota-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/UPLOAD/PRESS/WAIT/VERIFY)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast มุมขวาล่าง, cross-module/import 4–4.8s — อ่านทันทีที่โผล่)
5. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
6. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"
7. เคสกลุ่ม X (cross-module reject/delete-linked) ต้อง **สร้าง From-Member ใหม่ก่อน** ในเคสเดียวกัน (seed ไม่มี unverified+linked)
8. ไฟล์ทดสอบทั้งหมดต้องอยู่ในโฟลเดอร์ที่ agent เข้าถึงได้ก่อนเริ่ม (ดู Data Sets → Files)
9. จบทุกเคส → กรอก Result Report ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 28 / 28 (AC-01..11, AC-13..29 + AC-03b/AC-21b — ต้นฉบับข้าม AC-12) |
| Cross-Module (XT-01..04) | 4 / 4 (XT-04 simulate) |
| Business rules (BR-AGQ-01..13) | 12 / 13 (ข้าม BR-AGQ-13 DOA มีเหตุผล) |
| Validation (VR-01..12) | 12 / 12 |
| Edge cases (EC-01..17) | 16 / 17 (ข้าม EC-14 OOS; 5 เคส simulate/SIT) |
| Recommended (RC-01..06) | 6 / 6 (มี ☐ / simulate ตามเหมาะสม) |
| Error codes (UI-observable) | 10 / 13 (ข้าม 3 server/auth-level มีเหตุผล) |
| Permission cells | R-01/R-02 allow ครบ · deny cells ข้าม (Drift D-04) |
| Scope Lock (LOCK-01..11) | 11 / 11 — ทุก LOCK มีเคส verify |

- **Manifest cross-check (FRD §0.12): ✅ 10 Stories + 13 Rules + 12 VR + 17 EC — ทุกแถวมีคู่ใน Ledger** (ยกเว้นที่ mark ข้ามพร้อมเหตุผล)

### Recheck 2026-07-22 (authoritative) — new cases mapping
- TC-287 → **TC-C13** (member-search 0-match มาตรฐาน + email key) · TC-322 → **TC-C14** (member-search timeout/Retry)
- TC-304 → **TC-I09** (CSV per-row idempotency rerun/CONFLICT) · TC-307 → **TC-Q08** (cross-page selection)
- TC-316 → **TC-V07** (verify-modal focus-trap/aria) · TC-312 → **TC-V08** (bulk-verify throughput/progress)
- TC-313 → **TC-W05** (attachment preview + open-original fallback)
- TC-297 → **TC-X06** (reject external fail → schedule retry, banner, no rollback) · TC-323 → **TC-X07** (FN-AT-AGQ-127 idempotent + retry)
- ครอบคลุม G1 (write-back keep+retry, ไม่ rollback) · G2 (member-search) · G3 (CSV per-row idempotency) · G4 (NFR budgets) · G5–G10

### ข้าม (พร้อมเหตุผล)
- BR-AGQ-13 (DOA placeholder) — backend field + OQ-Q5, ไม่มีผลบน UI Phase 1
- EC-14 (No-Member ผูก member ภายหลัง) — OOS Phase 2 (ไม่มี re-link)
- ERR_INSUFFICIENT_ROLE / ERR_NOT_FOUND / ERR_DUPLICATE_IDEMPOTENCY_KEY — server/auth-level ไม่มีเส้นทางบน prototype single-user
- Permission deny cells (R-01 verify / R-02 create-edit-delete-import) — prototype ไม่มี role switching (Drift D-04) — ทดสอบที่ระบบจริงผ่าน ENC matrix
- UI state all-empty (list ว่างจริง) — ลบได้เฉพาะ unverified — ตรวจ filter-empty แทน (TC-Q03)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-002",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-Q01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 60, "pass": 0, "fail": 0, "blocked": 0 }
}
```
