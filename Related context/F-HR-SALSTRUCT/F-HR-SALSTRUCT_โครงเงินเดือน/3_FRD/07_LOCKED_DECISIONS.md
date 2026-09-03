# 07_LOCKED_DECISIONS — F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> **Audience:** ทุกบทบาท · **§7.0 คือส่วนที่แก้ไม่ได้** — spec ใดในแพ็กขัดกับ §7.0 ให้ถือว่า §7.0 ชนะ แล้วแจ้ง drift

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ — **IMMUTABLE**

| LOCK id | สาระ | ผลผูกพันในแพ็กนี้ |
|---|---|---|
| **HR-1** | legal/policy parameter ทุกตัวมี `effective_date` · มาจาก HR Configuration · ห้าม hardcode | BR-17 · BR-23 · `resolveHrConfig` · `resolveLegalMinimum` |
| **C-1…C-6** | ส่ง `date` เสมอ · เก็บ `version_id` · ห้าม cache ข้ามวัน · ห้าม CRUD ของ HR Config · ค่า inactive ยังแสดงได้ · ลงทะเบียน where-used | `00_OVERVIEW §0.14.2` · `T_ss_cfg_ref` · API-21/23/27 |
| **P-1…P-9** | invariant ของ HR Configuration ที่แพ็กนี้ต้องเคารพ **และ** บังคับใช้ซ้ำกับข้อมูลตัวเอง (P-1′…P-9′) | `00_OVERVIEW §0.14.1` |
| **#107** | ห้ามสร้างหน้า config ของ HR เอง — อ้างด้วยลิงก์เท่านั้น | FN-39 · `01_UI` ทุกหน้า · ไม่มี endpoint เขียนของ HR Config |
| **LD-4C-02** | soft reference ทุกเส้นข้าม feature: snapshot/display-only · nullable · ไม่มี FK cascade · ห้าม CRUD ของ feature อื่น | `04_DB §4.3` · `00_OVERVIEW §0.15` |
| **DOA iron rule** | ไม่มี hardcoded approval chain — feature นี้ไม่มี approval เลย | BR-21 · ไม่มี endpoint/สถานะอนุมัติ |
| **Audit append-only · ไม่มี hard delete** | ประวัติลบไม่ได้ · ปิดใช้ = soft archive | BR-05 · ไม่มี DELETE ทั้งแพ็ก · trigger ที่ DB |
| **7C ท่อต้องห้าม** | ห้ามประกาศ OC · DC ระดับเอกสาร · SC (register 422) | `CSQ_BRIEF.md §3` · 10 event เป็น EC/SecC เท่านั้น |
| **Data Masking (Policy Center)** | RESTRICTED · masking ตาม role · ห้ามทำ permission เอง | BR-16 · ENG-MASK-01 · OQ-FRD-05 |
| **UI standard** | #102 combobox · #103 lean list · #104 1 feature = 1 เมนู · #105 demo strip · #106 ห้าม hint banner · #40.1 แถว ≤52px · CI Warm Light | `01_UI §1.0.1` (ผ่าน render จริงแล้ว) |

**SCOPE DRIFT ที่พบในแพ็กนี้: ไม่มี**

## §7.1 Locked Decisions (LD)

### LD-01 · การเปลี่ยนสถานะตามวันมีผลใช้ทั้ง as-of read และ scheduler
- **ตัดสิน:** ความจริงตอนอ่านมาจากการคำนวณ as-of (`resolveBandAt` · `resolveCurrentRate`) · scheduler (`advanceEffectiveStates`) เขียนคอลัมน์สถานะเพื่อให้รายงาน/ตัวกรองเร็ว และต้อง **idempotent**
- **ทำไม:** ถ้าพึ่ง scheduler อย่างเดียว การอ่านย้อนวัน/ล่วงหน้าจะผิดทันทีที่งานเบื้องหลังพลาด · ถ้าพึ่ง as-of อย่างเดียว การกรองตามสถานะจะช้าที่ข้อมูลหลักหมื่นแถว
- **ผลถ้าเปลี่ยน:** ต้องแก้ `03_LOGIC` E5 + ดัชนีที่ `04_DB §4.8` · อ้าง OQ-FRD-02

### LD-02 · masking ทำที่ชั้น API ไม่ใช่ UI
- **ตัดสิน:** ค่าที่ผู้เรียกไม่มีสิทธิ์ถูกแทนด้วย `null` + `masked: true` **ก่อนออกจากเซิร์ฟเวอร์** ทุก endpoint รวม `/resolve` และ export
- **ทำไม:** RESTRICTED — ถ้าส่งตัวเลขจริงลงไปที่ browser แล้วค่อยซ่อน ถือว่ารั่วแล้ว · และ consumer ที่เรียก API ตรงจะเลี่ยง UI ได้
- **ผลถ้าเปลี่ยน:** ผิด BR-16 (LOCK) — เปลี่ยนไม่ได้

### LD-03 · ใช้ `null` แทนสตริงอำพราง
- **ตัดสิน:** ค่าที่ปิดบังคืน `null` ไม่ใช่ `"••••"` หรือค่าที่มีความยาวสัมพันธ์กับของจริง
- **ทำไม:** ความยาวของค่าอำพรางเป็นช่องรั่วเชิงอนุมาน · UI เป็นผู้เรนเดอร์จุดปิดบังเอง (ความกว้างคงที่ · Hotspot #35)

### LD-04 · เลข `version_id` ที่คืนให้ consumer เป็น **ก้อน** ไม่ใช่ค่าเดียว
- **ตัดสิน:** `version_id = { band, hr_config: { period_rule, legal_minimum } }`
- **ทำไม:** คำตอบหนึ่งครั้งใช้หลายเวอร์ชันตัดสิน — ถ้าคืนค่าเดียว ปลายทางพิสูจน์ย้อนหลังไม่ครบ (SS-2)
- **ผลถ้าเปลี่ยน:** กระทบสัญญา §0.13.2 → ต้องแจ้ง consumer ทั้ง 4 ตัว

### LD-05 · การเขียนกลับมีทางเข้าเดียว (`POST /rates/from-movement`) และ idempotent ตามเลขที่คำสั่ง
- **ตัดสิน:** Employee Movement เป็น service เดียวที่เขียนได้ · ใช้ `movement_doc_no` เป็น `Idempotency-Key`
- **ทำไม:** กันการสร้างอัตราซ้ำจากการส่งซ้ำ · กันไม่ให้ feature อื่นแอบเขียน (LD-4C-02)

### LD-06 · ค่าแรงขั้นต่ำอ่านอย่างเดียว — ไม่มีที่เก็บ ไม่มีค่าสำรอง
- **ตัดสิน:** ไม่มีคอลัมน์/ไฟล์/ค่าคงที่ใดในแพ็กนี้ที่เก็บตัวเลขขั้นต่ำ · ต้นทางไม่มีค่า = แสดงข้อความ ไม่เดา
- **ทำไม:** **P-8** เป็น LOCK · การมีค่าสำรองคือการ hardcode กฎหมายโดยอ้อม
- **หมายเหตุ:** ทำให้ AT-53 เป็นเคสที่ต้องผ่านเสมอ

## §7.2 Convention Deviations

| CD | รายการ | สถานะ |
|---|---|---|
| CD-01 | naming · API path · error code · function/engine convention | **ไม่มี deviation** — ตรงมาตรฐานทั้งหมด |
| CD-02 | ใช้ `POST /grades/{id}/versions/{vid}/publish` แทน `PATCH` | **ตั้งใจ** — เป็น state transition ไม่ใช่การแก้ field (แพทเทิร์นเดียวกับ HR Configuration) |
| CD-03 | ตาราง P-03 กว้าง 1120px แล้ว scroll ภายใน `.table-wrap` | **ตั้งใจ** — เพื่อรักษาแถว ≤52px ที่ viewport 1024 (บันทึกใน `01_UI §1.0` · UX Pass G-b) |

## §7.3 Open Questions Promoted from 00_OVERVIEW

| # | คำถาม | default | เจ้าภาพ | ต้องเคาะก่อน |
|---|---|---|---|---|
| OQ-SS-01 | นอกกระบอก เตือนหรือบล็อก | เตือน + บังคับเหตุผล | HR / Strike | SOW3.7 — **ห้าม implement โหมดบล็อกก่อน** |
| OQ-STD-11 | group `legal_minimum` ยังไม่เผยแพร่จาก HR Configuration | เรียก `group=legal_minimum` · ไม่มีค่า = แสดงข้อความ | BA / Architect (F-HR-CONFIG) | ปิด Phase 1 |
| OQ-SS-02 | ที่มาของยอดสะสมของเงินหัก | อ่านอย่างเดียว/กรอกมือ | BA | ปิด Phase 1 |
| OQ-SS-03 | HR Manager แก้กระบอกเองได้ไหม | ไม่ได้ (HR Comp Admin เท่านั้น) | HR | SOW3.7 |
| OQ-CSQ-01 | E10 เป็น SecC หรือให้ Audit Trail รับ | ประกาศ SecC ไว้ก่อน (ปิดได้ด้วยสวิตช์) | Architect / Policy Center | ก่อนลงทะเบียน event |
| OQ-STD-01…10 · 12 · 13 | ขอบเขตที่ standard มีแต่รอบนี้ไม่ทำ | ตาม BRD §15 | Strike / HR / BA | ก่อนวางแผน wave ถัดไป |
| OQ-HR-01 · OQ-HR-05 | Payroll สร้างเองเต็ม · multi-company | ตาม BRD §15 | Strike | — |
| OQ-BRD-01 | baseline ของตัวชี้วัด M-01 · M-02 | เก็บก่อน go-live | BA | go-live |
| OQ-BRD-02 | ชุด enum ประเภทการเปลี่ยนอยู่ที่ไหน | config table ที่ feature นี้ | Strike / BA | ก่อน Employee Movement ส่งมอบ |
| OQ-BRD-03 | วิธีจัดการการบันทึกชนกัน | optimistic lock (`If-Match`) | Tech Lead | เริ่ม dev API-14 |
| OQ-BRD-04 | รู้ได้อย่างไรว่าพลาด event | แสดงเวลาที่ดึงล่าสุด + ปุ่มดึงใหม่ | Tech Lead | — |
| OQ-BRD-05 | บันทึกความพยายามเข้าถึงที่ถูกปฏิเสธ | บันทึกที่ Policy Center | Policy Center | — |
| OQ-FRD-01…06 | รายละเอียดเชิงเทคนิค (scope=company · scheduler · version_id · masking layer · restricted resource · config ล่ม) | ดู `00_OVERVIEW §0.8` | Architect / Tech Lead / Security | ตามที่ระบุในตาราง |

**รวม Open Questions ที่ยังเปิดอยู่: 30 ข้อ — ไม่มีข้อใดบล็อกการเริ่ม Phase 1**

## §7.4 Architecture Tradeoffs Acknowledged

| AT | ทางเลือกที่เลือก | ที่แลกไป |
|---|---|---|
| AT-A | EXCLUDE constraint ที่ DB คู่กับการตรวจใน logic | เขียนกติกา 2 ที่ (ต้อง sync ข้อความ error) แลกกับความมั่นใจว่าไม่มีช่วงทับหลุดผ่าน race |
| AT-B | เก็บ snapshot ชื่อพนักงานทุกเรคคอร์ด | ข้อมูลซ้ำ + ชื่อเก่าไม่อัปเดตตามต้นทาง — แลกกับการที่ประวัติอ่านได้ตลอดไป (LD-4C-02) |
| AT-C | อ่านค่านโยบายผ่าน HTTP ทุกครั้ง (cache ภายในวัน) | latency เพิ่ม + พึ่งพา HR Configuration — แลกกับการไม่มีค่ากฎหมายซ้ำในระบบนี้ (P-8) |
| AT-D | ไม่มี WebSocket | ผู้ใช้เห็นสถานะใหม่ตอนโหลดหน้าถัดไป — ยอมรับได้เพราะการเปลี่ยนเกิดวันละครั้ง |
| AT-E | ไม่ทำ mass import ในรอบแรก | ตอน onboarding ต้องกรอกมือหรือใช้สคริปต์ครั้งเดียว — แลกกับการไม่เปิดช่องเขียนข้อมูลที่เลี่ยง validation (NS-06) |

## §7.5 Decisions Deferred to Implementation

| # | เรื่อง | หมายเหตุ |
|---|---|---|
| DI-01 | รูปแบบการเก็บ `companies[]` (jsonb vs ตารางลูก) | เลือกได้ตอน implement — เงื่อนไขเดียวคือต้องเก็บ snapshot ชื่อ |
| DI-02 | กลไก scheduler (cron ในแอป vs job runner กลาง) | ต้อง idempotent + รันซ้ำได้ (LD-01) |
| DI-03 | วิธี cache ค่าจาก HR Config (in-memory vs shared) | เงื่อนไข: ไม่ข้ามวัน + ล้างได้ด้วย event (C-3) |
| DI-04 | รูปแบบ ETag ของอัตราปัจจุบัน | ใช้กับ `If-Match` (OQ-BRD-03) |
| DI-05 | โครงสร้างการเพจของ `scope=company` (cursor vs offset) | เกณฑ์: ต้องอ่าน 5,000 คนจบใน 30 วินาที (§6.6) |

## §7.6 References
BRD §3.4 · `00_OVERVIEW §0.8` `§0.13` `§0.14` `§0.15` · `02_API §2.3` · `03_LOGIC §3.2` · `04_DB §4.6` · `05_RULES §5.7` · `5_DECLARATIONS/CSQ_BRIEF.md` · `5_DECLARATIONS/NOT_NEEDED.md` · `output/2026-08-28/F-HR-CONFIG_ตั้งค่าHR/3_FRD/00_OVERVIEW.md §0.13–§0.15`
