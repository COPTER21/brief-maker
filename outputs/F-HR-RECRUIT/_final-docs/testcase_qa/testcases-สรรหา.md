# AI Test Cases — สรรหา (F-HR-RECRUIT · F127)

ไฟล์นี้เขียนให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบ `สรรหา.html` บนหน้าจอจริง แล้วรายงานผลกลับ.
ทุก action ขึ้นต้นด้วย **verb tag** (OPEN/CLICK/TYPE/SELECT/TOGGLE/UPLOAD/PRESS/WAIT/VERIFY) + target ที่ **เห็นบนจอ**; ทุก Expected เช็คได้ด้วยตา.
Microcopy ทั้งหมด **คัดตรงตัว (verbatim)** จาก `สรรหา.html` (SoT) + `UI_BRIEF_สรรหา.md §9` + `FRD 06_TESTS §6.10`. ห้าม paraphrase.

> **ที่มา:** `สรรหา.html` (source of truth) · `FRD_F-HR-RECRUIT_Pack/` (00/01/02/05/06/07) · `BRD_สรรหา.md` · `UI_BRIEF_สรรหา.md`
> **หมายเหตุ persona:** prototype นี้สลับบทบาทที่ **แถบล่างซ้าย (demo strip)** — ปุ่ม `เจ้าหน้าที่สรรหา` (recruiter · default) / `ผู้จัดการสายงาน` (manager) / `ผู้ชมทั่วไป` (viewer). Iron #105 — prod จะผูก role master.
> **⚠ state ค้างข้ามเคส:** prototype เก็บข้อมูลใน memory ล้วน — mutation จากเคสก่อนหน้าจะค้างจนกว่าจะ **refresh หน้า (reload ไฟล์)**. ทุกเคสจึงสั่ง reload ที่ Setup เพื่อคืน seed เดิม (refresh-safe · R7).

---

## Meta

| field | value |
|---|---|
| Feature ID | F-HR-RECRUIT (F127) |
| Feature name | สรรหา (Recruit / Candidate Pool) |
| Version / footer | Prototype v1.0.0 · PREFLIGHT v6.4 (2026-09-02) |
| App entry | เปิด `สรรหา.html` → boot ลงแท็บ **ตำแหน่งที่เปิด** เสมอ (`#/recruit/req`) |
| Routes (hash · refresh-safe) | `#/recruit/req` · `#/recruit/pool` · `#/recruit/board` · `#/recruit/report` |
| Overlays | Drawer (ผู้สมัคร 4 แท็บ / อัตรา) · Modal (confirm/reason/interview/doa) · Toast (auto-dismiss ~2.8s) |
| Personas | recruiter (unmask · ไม่อนุมัติ) · manager (mask · อนุมัติได้) · viewer (read-only · mask) |
| Seed | 3 อัตรา (REQ-2569-0001 เปิดรับ · -0002 อนุมัติแล้ว/รอประกาศ · -0003 ปิดแล้ว) · 6 ผู้สมัคร (C1..C6) · 2 ข้อเสนอ |
| จำนวนเคส | 62 (11 group) |
| FN coverage | 21/21 (FN-01..16 + FN-90..94) |

---

## Coverage

| group | หน้า/journey | เคส | ความสำคัญ |
|---|---|---|---|
| G-A · วงจรอัตรา (Requisition) | P-01 · D-02 · M-01 · M-03 | TC-A01..A10 (10) | สูง |
| G-B · ผู้สมัคร + consent + ซ้ำ | P-02 · M-02 · D-01 detail | TC-B01..B06 (6) | สูง |
| G-C · บอร์ดสรรหา (pipeline) | P-03 | TC-C01..C07 (7) | สูง |
| G-D · สัมภาษณ์ + scorecard | D-01 assess · M-04 | TC-D01..D04 (4) | กลาง |
| G-E · ข้อเสนอ + รับเข้าทำงาน | D-01 offer · M-03 · M-06 | TC-E01..E09 (9) | สูง |
| G-F · ไม่ผ่าน/ถอนตัว/talent pool | M-05 | TC-F01..F03 (3) | กลาง |
| G-G · รายงาน funnel | P-04 | TC-G01..G03 (3) | กลาง |
| G-H · กติกากลาง (ค้นหา/validate/audit/mask/viewer) | ทุกหน้า | TC-H01..H09 (9) | สูง |
| G-I · Edge `[AI-DEFAULT]` | concurrency / cancel | TC-I01..I02 (2) | ต่ำ |
| G-X · Cross-module (XT) | handoff / band / NTF / DOA | TC-X01..X04 (4) | กลาง |
| G-N · Negative รวม (ของที่ห้ามมี) | pipeline/offer/req/employee | TC-N01..N05 (5) | สูง |

---

## Coverage Ledger

### FN (FUNCTION_CHECKLIST · 21/21)
| FN | ต้องทำได้ | cases |
|---|---|---|
| FN-01 | เปิดอัตรา | TC-A01, TC-A02 |
| FN-02 | เปิดอัตราไม่มี Manpower → เตือนทำได้ | TC-A03 |
| FN-03 | เพิ่มผู้สมัคร | TC-B01, TC-B02 |
| FN-04 | ผูกผู้สมัครกับอัตรา | TC-B01 |
| FN-05 | consent PDPA gate | TC-B02, TC-B05, TC-C03, TC-D04, TC-N01 |
| FN-06 | เลื่อนสถานะ pipeline | TC-C01, TC-C02 |
| FN-07 | นัดสัมภาษณ์ + แจ้งเตือน | TC-D01, TC-X03 |
| FN-08 | ส่งอนุมัติ (req/offer) DOA slot picker | TC-A05, TC-A06, TC-E04, TC-X04 |
| FN-09 | ประเมิน scorecard | TC-D02, TC-D03 |
| FN-10 | สร้างข้อเสนอ (band freeze) | TC-E01, TC-E02, TC-X02 |
| FN-11 | ตอบรับ → hired → handoff (ไม่สร้าง employee) | TC-E06, TC-X01, TC-N02 |
| FN-12 | ปฏิเสธ/ถอนตัว | TC-F01, TC-F02, TC-E09 |
| FN-13 | ไม่ผ่าน → talent pool | TC-F03 |
| FN-14 | ตรวจซ้ำ email/phone → เตือน | TC-B03 |
| FN-15 | รายงาน funnel/time-to-hire | TC-G01, TC-G02, TC-G03 |
| FN-16 | ปิดอัตรา | TC-A08 |
| FN-90 | ค้นหา/filter + empty state | TC-H01, TC-H02 |
| FN-91 | ปิด/ยกเลิกผ่าน confirm + soft archive | TC-A08, TC-F01 |
| FN-92 | field validate + กัน double-submit | TC-A04, TC-B04, TC-E03, TC-H03 |
| FN-93 | audit append-only | TC-H04 |
| FN-94 | ปิดบังข้อมูลผู้สมัคร RESTRICTED ตาม role | TC-H05, TC-H06, TC-H07 |

**FN cross-check: ✅ 21/21**

### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 req อนุมัติ DOA ครบก่อนประกาศ | TC-A05, TC-A06, TC-A09, TC-N04 |
| BR-02 consent PDPA gate | TC-B02, TC-C03, TC-D04, TC-N01 |
| BR-03 ทุก transition audit | TC-H04, TC-C01 |
| BR-04 offer อนุมัติ DOA + เงินตามระดับ | TC-E04, TC-E05, TC-N03 |
| BR-05 hired → handoff event (ไม่สร้าง employee) | TC-E06, TC-X01, TC-N02 |
| BR-06 ผู้สมัคร RESTRICTED masking | TC-H05, TC-H06, TC-H07 |
| BR-07 audit append-only + soft archive | TC-A08, TC-F01, TC-H04 |
| BR-08 Manpower hook · null ไม่บังคับ | TC-A03 |
| BR-09 snapshot ผู้สัมภาษณ์ + freeze band version | TC-D01, TC-E01, TC-X02 |
| BR-10 duplicate email/phone → เตือน | TC-B03 |

### Validation Rules (VR)
| VR | cases |
|---|---|
| VR-01 required fields (req/cand/offer) | TC-A04, TC-B04, TC-E03 |
| VR-02 double-submit guard (loader) | TC-H03 |
| VR-03 salary in-band / require reason | TC-E02 |
| VR-04 DOA dynamic (slot resolve runtime · ไม่ hardcode) | TC-A05, TC-X04 |
| VR-05 viewer read-only | TC-H08, TC-H09 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 no-consent block เลื่อน | TC-C03, TC-N01 |
| EC-02 duplicate warn | TC-B03 |
| EC-03 no-manpower warn | TC-A03 |
| EC-04 offer นอก band → เตือน+เหตุผล | TC-E02 |
| EC-05 board→hired ข้าม offer.accepted (FIX-01) | TC-C05, TC-N02 |
| EC-06 viewer เรียก mutation ทางอ้อม | TC-H09 |
| EC-07 `[AI-DEFAULT]` concurrent stage move | TC-I01 (ต้อง simulate) |
| EC-08 `[AI-DEFAULT]` cancel req ขณะ pipeline ค้าง | TC-I02 (ต้อง simulate · ⚠ drift DR-01) |
| EC-09 `[AI-DEFAULT]` idempotency/double-submit network | TC-H03 (UI ส่วน · backend simulate) |
| EC-10 `[AI-DEFAULT]` NTF ยิงล้มเหลว queue/retry | — ข้าม (หลังบ้าน · ไม่มีผลบน UI prototype · OQ-D4) |
| EC-11 `[AI-DEFAULT]` band version freeze หลังสร้าง offer | TC-X02 |
| EC-12 HM/interviewer ถูกลบ → ใช้ snapshot | — ข้าม (ต้องลบ record ที่ Employee Master · prototype ไม่มีหน้า · หลังบ้าน) |

### Error Catalog (05_RULES §5.6 — mapped ผ่าน UI observable)
| error | cases (UI-observable proxy) |
|---|---|
| ERR_VALIDATION_FAILED | TC-A04, TC-B04, TC-E03 |
| BR_REQ_NOT_APPROVED | TC-A09, TC-N04 |
| BR_CONSENT_REQUIRED | TC-C03, TC-N01 |
| BR_OFFER_REQUIRED (เข้า offer ไม่มี offer) | TC-C04 |
| BR_OFFER_NOT_APPROVED | TC-N03 |
| BR_OFFER_NOT_ACCEPTED (hire ก่อน accepted) | TC-C05, TC-N02 |
| BR_HIRE_ROUTE_ONLY (move→hired) | TC-C05, TC-N02 |
| BR_OUT_OF_BAND_REASON | TC-E02 |
| BR_REASON_REQUIRED | TC-F02 |
| ERR_INSUFFICIENT_ROLE (viewer) | TC-H08, TC-H09 |
| ERR_STALE_DATA (409 concurrent) | TC-I01 (simulate) |
| ERR_NOT_AUTHENTICATED / ERR_NOT_FOUND / ERR_NOT_IN_SLOT / ERR_DUPLICATE_IDEMPOTENCY_KEY / ERR_INVALID_STATE / BR_DOA_UNRESOLVED / BR_BAND_UNRESOLVED | — ข้าม (backend-only · prototype in-memory ไม่มี async/HTTP path · ดู UI_BRIEF DR-02/DR-03) |

### Permission Matrix (05_RULES §5.3)
| cell | cases |
|---|---|
| recruiter สร้าง req/cand = allow | TC-A01, TC-B01 |
| recruiter unmask PII = allow | TC-H06 |
| manager approve req/offer = allow | TC-A06, TC-E04 |
| manager mask PII = deny full | TC-H05 |
| manager My-Approval hook เห็น | TC-A06 |
| viewer สร้าง = deny (ปุ่มซ่อน) | TC-H08 |
| viewer mutation ทางอ้อม = deny (guard) | TC-H09 |
| viewer PII = mask | TC-H05 (persona=viewer variant) |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | case |
|---|---|---|
| XT-01 hire → emit `recruit.candidate.hired` (ไม่สร้าง employee) | On/Offboard | TC-X01, TC-E06 |
| XT-02 offer band freeze ไม่ re-resolve | Salary Structure | TC-X02 |
| XT-03 NTF ยิงตรง trigger | ENG-NOTIFY | TC-X03 |
| XT-04 DOA resolve slot runtime (ไม่ hardcode) | Policy Center | TC-X04, TC-A05 |

### Scope Lock (07 §7.0 — LOCK ต้องมีเคส verify)
| LOCK | ข้อยืนยัน (ย่อ) | case verify |
|---|---|---|
| LOCK-OB1 | รับ → handoff · ไม่สร้าง employee | TC-N02, TC-X01 |
| LOCK-OB2 | consent + retention PDPA | TC-B02, TC-B06 |
| LOCK-OB3 | offer/req อนุมัติ = DOA slot (ไม่ hardcode) | TC-A05, TC-X04 |
| LOCK-OB4 | Manpower hook · null ไม่บังคับ | TC-A03 |
| LOCK-OB5 | ผู้สมัคร RESTRICTED · audit append-only | TC-H04, TC-H05 |
| LOCK-DOA | DOA ไม่ผูก threshold ยอดเงิน | TC-A05 (VERIFY modal "ไม่มีวงเงิน") |
| LOCK-DOCCFG | ไม่มีเลขรันเอกสาร (offer letter soft-ref) | TC-N05 (VERIFY ไม่มี PDF/เลขรัน offer) |
| unsupported[1..5] (create employee / job board / assessment engine / offer PDF เลขรัน / CRUD band) | นอกขอบเขต | TC-N02/N05 verify absence · **ห้ามสร้างเคสทดสอบฟีเจอร์ที่ไม่มี** |

### Cross-cutting / states / events
| item | cases |
|---|---|
| empty state (req/pool filter 0) | TC-H01, TC-H02 |
| REQ_STATUS pills 5/5 | TC-H01 (VERIFY) · TC-A01/A06/A08 (แต่ละสถานะ) |
| STAGES + TERMINAL pills | TC-C06, TC-F03, TC-G01 |
| consent chip (ยินยอม/รอ) | TC-B05, TC-H07 |
| dup chip "เคยสมัคร" | TC-B03 |
| retention label (FIX-03) | TC-B06 |
| audit timeline append-only | TC-H04 |
| NTF toast (info) | TC-X03, TC-C01 |
| Esc chain (modal→drawer) | TC-A05 (VERIFY Esc) |

---

## Data Sets

### ค่ากรอกจริง
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| **DS-REQ-A** (อัตราถูกครบ) | ตำแหน่ง · แผนก · จำนวนอัตรา · ระดับ · ผู้จัดการสายงาน · Manpower | `Senior Backend Developer` · `เทคโนโลยีสารสนเทศ` · `2` · `G4 · หัวหน้างาน / ชำนาญการ` · `ธีรภัทร วงศ์ไพศาล` · `MP-2569-IT-09` |
| **DS-REQ-NOMP** (ไม่มี Manpower) | เหมือน DS-REQ-A แต่ | Manpower = **เว้นว่าง** |
| **DS-REQ-BAD** (ไม่ครบ) | ตำแหน่ง · แผนก · จำนวนอัตรา | เว้นว่าง · เว้นว่าง · `0` |
| **DS-REQ-NOHM** (ขาดผู้จัดการ) | ตำแหน่ง · แผนก · จำนวน · ผู้จัดการสายงาน | `QA Engineer` · `เทคโนโลยีสารสนเทศ` · `1` · **ไม่เลือก** |
| **DS-CAND-A** (ผู้สมัครถูก + ยินยอม) | ชื่อ-นามสกุล · อีเมล · เบอร์โทร · ตำแหน่งที่สมัคร · ความยินยอม | `วิศรุต ตั้งใจ` · `visarut.t@example.com` · `0801234999` · `REQ-2569-0001` · **เปิด** |
| **DS-CAND-NOCONSENT** | ชื่อ · อีเมล · เบอร์ · ความยินยอม | `ปกรณ์ ใจดี` · `pakorn@example.com` · `0855550000` · **ปิด** |
| **DS-CAND-DUP** (ซ้ำ C1) | ชื่อ · อีเมล · เบอร์ | `ทดสอบ ซ้ำ` · `thanawat.s@example.com` · `0812345678` |
| **DS-CAND-BAD** (ไม่ครบ) | ชื่อ · อีเมล · เบอร์ | เว้นว่างทั้งหมด |
| **DS-OFFER-IN** (ในช่วง band) | ระดับ · วันเริ่มงาน · เงินเดือนที่เสนอ | `G4` · `2026-10-01` · `62000` (band G4 = 45,000–85,000) |
| **DS-OFFER-OUT** (นอกช่วง) | ระดับ · วันเริ่ม · เงินเดือน · เหตุผลนอกช่วง | `G4` · `2026-10-01` · `95000` · `ประสบการณ์ 10 ปี สูงกว่ามาตรฐานระดับ` |
| **DS-OFFER-BAD** | วันเริ่ม · เงินเดือน | เว้นว่าง · เว้นว่าง |
| **DS-INTERVIEW** | วันที่ · เวลา · ผู้สัมภาษณ์ · สถานที่ | `2026-09-20` · `10:30` · `อรรถพล ชัยมงคล` · `ห้องประชุม 2 · Google Meet` |
| **DS-DOA-APPROVERS** (2 slot) | ขั้น 1 (ผู้จัดการสายงาน) · ขั้น 2 (หัวหน้าฝ่ายสรรหา) | `ธีรภัทร วงศ์ไพศาล` · `ปิยะนุช สมานมิตร` |
| **DS-REASON** | เหตุผล terminate | `คุณสมบัติยังไม่ตรงตำแหน่งนี้` |

### ผู้สมัคร seed (อ้างในเคส)
| id | ชื่อ (บนจอ) | รหัส | ระยะ | consent | offer | หมายเหตุ |
|---|---|---|---|---|---|---|
| C1 | ธนวัฒน์ ศรีสมบัติ | APP-2569-0011 | สมัครใหม่ | **ไม่ยินยอม** | — | ใช้ทดสอบ consent gate |
| C2 | สุพิชญา อินทโชติ | APP-2569-0012 | คัดกรอง | ยินยอม | — | มี chip "เคยสมัคร" (dup) |
| C3 | กิตติพงษ์ แซ่ลิ้ม | APP-2569-0009 | สัมภาษณ์ | ยินยอม | — | มี scorecard 4/5 · ใช้สร้าง offer |
| C4 | อารยา พงษ์พิพัฒน์ | APP-2569-0007 | ข้อเสนอ | ยินยอม | **sent** | ใช้ทดสอบ accept→hire + guard |
| C5 | ณัฐพล เจริญสุข | APP-2569-0003 | รับเข้าทำงาน | ยินยอม | accepted | terminal · onboardSent |
| C6 | พีรพล ทองดี | APP-2569-0006 | เก็บ Talent Pool | ยินยอม | — | terminal |

### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ที่ | หมายเหตุ |
|---|---|---|
| — | — | ฟีเจอร์นี้ **ไม่มี CSV import / file upload จริง** — ปุ่มแนบ Resume เป็น mock (สร้างชื่อไฟล์เอง `resume_<ชื่อ>.pdf` เมื่อคลิก · ไม่มี file picker). ไม่ต้องเตรียมไฟล์. |

---

## Test Cases

### G-A · วงจรอัตรา (Requisition)

#### TC-A01 — เปิดอัตราใหม่ครบฟิลด์ (happy)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: FN-01 / BR-08 / AT-01 · actor: recruiter
- Setup: role=recruiter (default) · reload หน้า · seed=default · files=—
- Start: OPEN `#/recruit/req`
- ชุดข้อมูล: DS-REQ-A
- ผ่านเมื่อ: บันทึกได้ + toast "สร้างอัตราแล้ว (ร่าง) — ส่งอนุมัติเปิดได้จากหน้ารายละเอียด" + drawer ปิด + แถวใหม่โผล่ในตาราง (สถานะ **ร่าง**)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` | — | หน้า **ตำแหน่งที่เปิด (Requisition)** · ตาราง 3 แถว · ปุ่ม **เปิดอัตราใหม่** มุมขวาบน | ☐ |
| 2 | CLICK ปุ่ม **เปิดอัตราใหม่** | — | drawer เปิด eyebrow **เปิดอัตราใหม่** หัวข้อ **ใบขออัตรากำลัง (Requisition)** | ☐ |
| 3 | TYPE → ช่อง **ตำแหน่ง** | DS-REQ-A | ช่องแสดง `Senior Backend Developer` | ☐ |
| 4 | TYPE → ช่อง **แผนก** | DS-REQ-A | ช่องแสดง `เทคโนโลยีสารสนเทศ` | ☐ |
| 5 | TYPE → ช่อง **จำนวนอัตรา** | `2` | ช่องแสดง 2 | ☐ |
| 6 | SELECT `G4 · หัวหน้างาน / ชำนาญการ` → **ระดับ (band เงินเดือน)** | DS-REQ-A | การ์ด band อัปเดตช่วง **45,000 – 85,000** · เวอร์ชัน SS-2569-03 | ☐ |
| 7 | CLICK ช่อง **ผู้จัดการสายงาน (Hiring Manager)** → TYPE `ธีรภัทร` → CLICK ตัวเลือก **ธีรภัทร วงศ์ไพศาล** | DS-REQ-A | ช่องแสดงชื่อ **ธีรภัทร วงศ์ไพศาล** ที่เลือก | ☐ |
| 8 | TYPE → ช่อง **อ้างอิงแผนอัตรากำลัง (Manpower)** | `MP-2569-IT-09` | note เตือนสีเหลืองด้านบน (Manpower) **หายไป** | ☐ |
| 9 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawer ปิด · WAIT toast (≤3s) | ☐ |
| 10 | WAIT จน toast ปรากฏ | — | toast success **"สร้างอัตราแล้ว (ร่าง) — ส่งอนุมัติเปิดได้จากหน้ารายละเอียด"** | ☐ |
| 11 | VERIFY ตารางอัตรา | — | มีแถว **Senior Backend Developer** · แผนก เทคโนโลยีสารสนเทศ · pill **ร่าง** (เทา) · ตัวนับแท็บ **ตำแหน่งที่เปิด** = 4 | ☐ |

#### TC-A02 — บันทึกร่างอัตรา (draft path)
- group: วงจรอัตรา · ความสำคัญ: กลาง · trace: FN-01 / DR-06 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/req`
- ชุดข้อมูล: DS-REQ-A
- ผ่านเมื่อ: กด **บันทึกร่าง** → toast "บันทึกร่างแล้ว" · แถวใหม่สถานะ **ร่าง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → CLICK **เปิดอัตราใหม่** | — | drawer ฟอร์มเปิด · มี **2 ปุ่มท้าย**: **บันทึกร่าง** (secondary) + **ยืนยันสร้าง** (primary) | ☐ |
| 2 | TYPE ตำแหน่ง/แผนก/จำนวน + เลือก HM | DS-REQ-A | ฟิลด์ครบ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกร่าง** | — | drawer ปิด · WAIT toast | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast success **"บันทึกร่างแล้ว"** | ☐ |
| 5 | VERIFY แถวใหม่ในตาราง | — | สถานะ pill = **ร่าง** (เหมือน path ยืนยันสร้าง — ทั้งคู่ลง draft ต้องไปกด "ส่งอนุมัติเปิด" ในหน้ารายละเอียด) | ☐ |

#### TC-A03 — เปิดอัตราไม่มี Manpower → เตือน แต่บันทึกได้ (edge: EC-03)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: FN-02 / BR-08 / LOCK-OB4 / AT-02 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/req`
- ชุดข้อมูล: DS-REQ-NOMP
- ผ่านเมื่อ: เว้น Manpower → มี note เตือน แต่บันทึกสำเร็จ (ไม่บล็อก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → CLICK **เปิดอัตราใหม่** | — | drawer ฟอร์มเปิด · **มี note เตือนสีเหลืองด้านบน** "ยังไม่ได้ระบุแผนอัตรากำลัง (Manpower) — เปิดอัตราได้ แต่โปรดตรวจสอบกับแผนกำลังคน (hook · ไม่บังคับ)" (เพราะ Manpower เริ่มว่าง) | ☐ |
| 2 | TYPE ตำแหน่ง/แผนก/จำนวน + เลือก HM · **เว้น Manpower ว่าง** | DS-REQ-NOMP | ฟิลด์ครบ ยกเว้น Manpower · note เตือนยังอยู่ | ☐ |
| 3 | CLICK ปุ่ม **ยืนยันสร้าง** | — | บันทึกได้ (ไม่บล็อก) · WAIT toast | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast success **"สร้างอัตราแล้ว (ร่าง) — ส่งอนุมัติเปิดได้จากหน้ารายละเอียด"** | ☐ |
| 5 | CLICK แถวอัตราที่เพิ่งสร้าง | — | drawer รายละเอียดเปิด · แถว **Manpower** แสดง chip amber **"ไม่มีแผน (เปิดโดยเตือน)"** | ☐ |

#### TC-A04 — validate ฟอร์มอัตราไม่ครบ (negative · VR-01)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: FN-92 / VR-01 / AT-21 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/req`
- ชุดข้อมูล: DS-REQ-BAD, DS-REQ-NOHM
- ผ่านเมื่อ: submit ไม่ครบ → toast เตือน + ฟิลด์ที่ผิดขึ้นกรอบแดง (`.is-invalid`)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → CLICK **เปิดอัตราใหม่** | — | drawer ฟอร์มเปิด (ตำแหน่ง/แผนกว่าง · จำนวน=1) | ☐ |
| 2 | TYPE จำนวนอัตรา = `0` · เว้นตำแหน่ง+แผนก · **เลือก HM** ก่อน | DS-REQ-BAD (แต่เลือก HM) | ฟิลด์ตำแหน่ง/แผนกว่าง | ☐ |
| 3 | CLICK ปุ่ม **ยืนยันสร้าง** | — | toast warning **"กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ"** · ช่อง **ตำแหน่ง**, **แผนก**, **จำนวนอัตรา** ขึ้นกรอบแดง + ข้อความ error ใต้ช่อง ("กรุณากรอกตำแหน่ง" / "กรุณากรอกแผนก" / "อย่างน้อย 1") · drawer **ไม่ปิด** | ☐ |
| 4 | TYPE ตำแหน่ง+แผนก+จำนวน ให้ครบ · แต่ **ล้าง/ไม่เลือก HM** | DS-REQ-NOHM | ฟิลด์ text ครบ · HM ยังว่าง | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันสร้าง** | — | toast warning **"กรุณาเลือกผู้จัดการสายงาน"** (ข้อความต่างจากข้อ 3) · drawer ไม่ปิด | ☐ |

#### TC-A05 — ส่งอนุมัติเปิดอัตรา → DOA slot picker (FN-08 · BR-01)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: FN-08 / BR-01 / VR-04 / XT-04 / LOCK-OB3 / LOCK-DOA / AT-03 · actor: recruiter
- Setup: role=recruiter · reload · seed=สร้างอัตรา draft 1 ตัวก่อน (ทำ TC-A01 ในหน้าเดียวกัน หรือใช้อัตราร่างที่มี) · files=—
- Start: OPEN `#/recruit/req` แล้วเปิดอัตราร่างที่เพิ่งสร้าง
- ชุดข้อมูล: DS-REQ-A (สร้างก่อน) + DS-DOA-APPROVERS
- ผ่านเมื่อ: DOA modal เปิด slot เปล่า → เลือกไม่ครบ toast เตือน → เลือกครบ toast "ส่งอนุมัติแล้ว" · สถานะ → **รออนุมัติเปิด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → CLICK **เปิดอัตราใหม่** → กรอก DS-REQ-A → **ยืนยันสร้าง** | DS-REQ-A | อัตราร่างใหม่ในตาราง (pill ร่าง) | ☐ |
| 2 | CLICK แถวอัตราร่างที่เพิ่งสร้าง | — | drawer รายละเอียด · footer มีปุ่ม **แก้ไข** + **ส่งอนุมัติเปิด** · มี note "อัตรานี้ยังเป็นร่าง — กด …ส่งอนุมัติเปิด…" | ☐ |
| 3 | CLICK ปุ่ม **ส่งอนุมัติเปิด** | — | modal **ส่งอนุมัติ (DOA)** เปิด · subtitle มี **DOA entry DOA-REQ-OPEN-001 · ไม่มีวงเงิน** · มี **2 slot**: "ผู้จัดการสายงาน (Hiring Manager)" และ "หัวหน้าฝ่ายสรรหา" · แต่ละ slot มี combobox **เลือกผู้อนุมัติ...** (ยังว่าง — resolve จาก DOA กลาง ไม่ hardcode คน) | ☐ |
| 4 | CLICK ปุ่ม **ส่งอนุมัติ** (โดยยังไม่เลือก slot) | — | toast warning **"กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น"** · modal ไม่ปิด | ☐ |
| 5 | CLICK slot 1 → เลือก **ธีรภัทร วงศ์ไพศาล** · CLICK slot 2 → เลือก **ปิยะนุช สมานมิตร** | DS-DOA-APPROVERS | ทั้ง 2 slot แสดงชื่อผู้อนุมัติที่เลือก | ☐ |
| 6 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal ปิด · WAIT toast | ☐ |
| 7 | WAIT จน toast ปรากฏ | — | toast success **"ส่งอนุมัติแล้ว"** · แถวอัตราสถานะ pill = **รออนุมัติเปิด** (เหลือง) | ☐ |
| 8 | PRESS Esc (ถ้า drawer ยังเปิด) | — | drawer ปิด (Esc chain — modal ปิดไปแล้วจึงปิด drawer) | ☐ |

#### TC-A06 — manager อนุมัติเปิดอัตรา + My-Approval hook (FN-08 · BR-01)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: FN-08 / BR-01 / permission(manager) · actor: manager
- Setup: role→**ผู้จัดการสายงาน (manager)** · seed=มีอัตราสถานะ "รออนุมัติเปิด" ≥1 (ทำ TC-A05 ต่อเนื่องในหน้าเดียวกัน ก่อนสลับ persona) · files=—
- Start: OPEN `#/recruit/req` (persona=manager)
- ผ่านเมื่อ: manager เห็น My-Approval hook + อนุมัติครบทุก slot → toast "อนุมัติแล้ว" · สถานะ → **อนุมัติแล้ว · รอประกาศ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม persona **ผู้จัดการสายงาน** (แถบล่างซ้าย) | — | user chip มุมขวาบนเปลี่ยนเป็น **ธีรภัทร ว.** | ☐ |
| 2 | VERIFY หัวหน้าตาราง P-01 | — | มี note info **"งานรออนุมัติของฉัน · N รายการ"** (My Approval hook — เห็นเฉพาะ manager ที่มี req pending) · ปุ่ม **เปิดอัตราใหม่** **หายไป** (manager ไม่ใช่ผู้สร้างในหน้านี้? — จริง ๆ manager ยังสร้างได้; ปุ่มยังอยู่) — VERIFY ปุ่มเปิดอัตราใหม่ยังแสดง | ☐ |
| 3 | CLICK แถวอัตราสถานะ **รออนุมัติเปิด** | — | drawer รายละเอียด · footer มีปุ่ม **ไม่อนุมัติ** (แดง) + **อนุมัติ** (primary) — เห็นเพราะ canApprove | ☐ |
| 4 | CLICK ปุ่ม **อนุมัติ** | — | (ขั้น 1/2 อนุมัติ) · timeline DOA ขั้นแรกจุดเขียว · toast success **"อนุมัติแล้ว"** | ☐ |
| 5 | CLICK ปุ่ม **อนุมัติ** อีกครั้ง (ขั้น 2) | — | อนุมัติครบทุก slot · toast **"อนุมัติแล้ว"** · สถานะ pill → **อนุมัติแล้ว · รอประกาศ** (info) · footer เปลี่ยนเป็น **ประกาศรับ** + **ปิดอัตรา** | ☐ |

#### TC-A07 — ไม่อนุมัติเปิดอัตรา (reject → draft, reason required)
- group: วงจรอัตรา · ความสำคัญ: กลาง · trace: FN-08 (reject branch) / BR_REASON_REQUIRED · actor: manager
- Setup: role=manager · seed=อัตราสถานะ "รออนุมัติเปิด" ≥1 · files=—
- Start: OPEN `#/recruit/req` (manager) → เปิดอัตรา pending
- ผ่านเมื่อ: reject ต้องมีเหตุผล → toast "ไม่อนุมัติแล้ว" · สถานะกลับ **ร่าง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer อัตรา pending → CLICK ปุ่ม **ไม่อนุมัติ** | — | modal **ไม่อนุมัติเปิดอัตรา** เปิด · มี textarea เหตุผล (บังคับ) | ☐ |
| 2 | CLICK ปุ่ม **ไม่อนุมัติ** (ในmodal · ยังไม่กรอกเหตุผล) | — | toast warning **"กรุณาระบุเหตุผล"** · modal ไม่ปิด | ☐ |
| 3 | TYPE → textarea เหตุผล | `งบยังไม่อนุมัติรอบนี้` | textarea แสดงข้อความ | ☐ |
| 4 | CLICK ปุ่ม **ไม่อนุมัติ** | — | modal ปิด · WAIT toast **"ไม่อนุมัติแล้ว"** (info) · สถานะ pill กลับ **ร่าง** | ☐ |

#### TC-A08 — ปิดอัตรา (confirm + soft archive · FN-16/FN-91)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: FN-16 / FN-91 / BR-07 / AT-04 · actor: recruiter
- Setup: role=recruiter · reload · seed=REQ-2569-0001 (เปิดรับ) · files=—
- Start: OPEN `#/recruit/req`
- ผ่านเมื่อ: confirm modal "ปิดอัตรานี้?" → toast "ปิดอัตราแล้ว" · สถานะ → **ปิดแล้ว** · ประวัติยังอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → CLICK แถว **Senior Frontend Developer** (REQ-2569-0001 · เปิดรับ) | — | drawer รายละเอียด · footer มีปุ่ม **ปิดอัตรา** (แดง) | ☐ |
| 2 | CLICK ปุ่ม **ปิดอัตรา** | — | confirm modal หัวข้อ **"ปิดอัตรานี้?"** · body "อัตราจะถูกปิด (รับครบ/ยกเลิก) และเก็บถาวรแบบ soft archive — ประวัติยังอยู่ครบ" · ปุ่มยืนยัน **ปิดอัตรา** (แดง) | ☐ |
| 3 | CLICK ปุ่ม **ปิดอัตรา** (ยืนยัน) | — | modal ปิด · WAIT toast success **"ปิดอัตราแล้ว"** | ☐ |
| 4 | VERIFY แถว/สถานะ | — | pill = **ปิดแล้ว** (เทา) | ☐ |
| 5 | CLICK แถวอัตราที่ปิด → VERIFY ส่วน **ประวัติ (append-only)** | — | มี entry "ปิดอัตรา" ล่าสุดบนสุด · entry เก่ายังอยู่ครบ (ไม่ถูกลบ) | ☐ |

#### TC-A09 — อัตราร่างยังประกาศไม่ได้ (negative · BR-01)
- group: วงจรอัตรา · ความสำคัญ: สูง · trace: BR-01 / BR_REQ_NOT_APPROVED / NEG · actor: recruiter
- Setup: role=recruiter · reload · seed=อัตราร่าง (สร้าง DS-REQ-A) · files=—
- Start: OPEN `#/recruit/req` → เปิดอัตราร่าง
- ผ่านเมื่อ: อัตราสถานะร่าง **ไม่มีปุ่ม "ประกาศรับ"** — ประกาศได้ต่อเมื่ออนุมัติครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างอัตราร่าง (DS-REQ-A) → CLICK แถวนั้น | DS-REQ-A | drawer รายละเอียด | ☐ |
| 2 | VERIFY ปุ่มใน footer/header | — | มีเฉพาะ **แก้ไข** + **ส่งอนุมัติเปิด** · **ไม่มีปุ่ม "ประกาศรับ"** และไม่มี "ปิดอัตรา" (ยังร่าง) | ☐ |
| 3 | VERIFY note ในตัว drawer | — | note info "อัตรานี้ยังเป็นร่าง — กด …ส่งอนุมัติเปิด… เพื่อเข้าสายอนุมัติ (DOA)" (ยืนยันว่าต้องผ่าน DOA ก่อน) | ☐ |

#### TC-A10 — ประกาศรับ (approved → open)
- group: วงจรอัตรา · ความสำคัญ: กลาง · trace: FN-06(announce) / AT... · actor: recruiter
- Setup: role=recruiter · reload · seed=REQ-2569-0002 (อนุมัติแล้ว · รอประกาศ) · files=—
- Start: OPEN `#/recruit/req` → เปิด REQ-2569-0002
- ผ่านเมื่อ: กด "ประกาศรับ" → toast "ประกาศรับแล้ว" · สถานะ → **เปิดรับ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → CLICK แถว **นักบัญชี** (REQ-2569-0002 · อนุมัติแล้ว · รอประกาศ) | — | drawer · footer มีปุ่ม **ประกาศรับ** + **ปิดอัตรา** | ☐ |
| 2 | CLICK ปุ่ม **ประกาศรับ** | — | WAIT toast success **"ประกาศรับแล้ว"** · สถานะ pill → **เปิดรับ** (เขียว) | ☐ |
| 3 | VERIFY ประวัติ | — | มี entry "ประกาศรับอัตรา · สถานะ → เปิดรับ" บนสุด | ☐ |

---

### G-B · ผู้สมัคร + consent + ตรวจซ้ำ

#### TC-B01 — เพิ่มผู้สมัคร + ผูกอัตรา (happy · FN-03/04)
- group: ผู้สมัคร · ความสำคัญ: สูง · trace: FN-03 / FN-04 / AT-05 / AT-06 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/pool`
- ชุดข้อมูล: DS-CAND-A
- ผ่านเมื่อ: toast "สร้างผู้สมัครสำเร็จ" · แถวใหม่ในคลัง ระยะ **สมัครใหม่** · ผูกอัตรา REQ-2569-0001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` | — | หน้า **คลังผู้สมัคร** · ตาราง 6 แถว · ปุ่ม **เพิ่มผู้สมัคร** มุมขวาบน | ☐ |
| 2 | CLICK ปุ่ม **เพิ่มผู้สมัคร** | — | drawer eyebrow **เพิ่มผู้สมัครเข้าคลัง** หัวข้อ **ผู้สมัครใหม่** · มี note แดง RESTRICTED/PDPA ด้านบน | ☐ |
| 3 | TYPE → **ชื่อ-นามสกุล** | `วิศรุต ตั้งใจ` | ช่องแสดงค่า | ☐ |
| 4 | TYPE → **อีเมล** + **เบอร์โทร** | `visarut.t@example.com` · `0801234999` | ช่องแสดงค่า | ☐ |
| 5 | CLICK ช่อง **ตำแหน่งที่สมัคร (อัตราที่เปิด)** → TYPE `REQ` → CLICK **REQ-2569-0001** | DS-CAND-A | combobox แสดงอัตราที่เลือก | ☐ |
| 6 | CLICK การ์ด **ความยินยอม PDPA** (สลับเป็นยินยอม) | — | การ์ดเปลี่ยนข้อความเป็น **"ได้รับความยินยอมแล้ว"** · toggle ติ๊ก · note เตือนสีเหลืองหาย | ☐ |
| 7 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawer ปิด · WAIT toast success **"สร้างผู้สมัครสำเร็จ"** | ☐ |
| 8 | VERIFY ตารางคลัง | — | มีแถว **วิศรุต ตั้งใจ** · ตำแหน่งที่สมัคร = **Senior Frontend Developer** · ระยะ **สมัครใหม่** · ความยินยอม chip **ยินยอมแล้ว** (เขียว) · ตัวนับแท็บ คลังผู้สมัคร = 7 | ☐ |

#### TC-B02 — เพิ่มผู้สมัครไม่ยินยอม → บันทึกได้แต่ gate (FN-05 · BR-02)
- group: ผู้สมัคร · ความสำคัญ: สูง · trace: FN-05 / BR-02 / LOCK-OB2 / AT-07 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/pool`
- ชุดข้อมูล: DS-CAND-NOCONSENT
- ผ่านเมื่อ: consent ปิด → note เตือน "ดำเนินการต่อ…ไม่ได้" แต่บันทึกสำเร็จ · ระยะ สมัครใหม่ · chip **รอความยินยอม**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **เพิ่มผู้สมัคร** | — | drawer ฟอร์มเปิด · การ์ดความยินยอม default = **ยังไม่ได้รับความยินยอม** | ☐ |
| 2 | TYPE ชื่อ/อีเมล/เบอร์ · **ไม่แตะการ์ดความยินยอม** | DS-CAND-NOCONSENT | มี note เตือนสีเหลือง "ยังไม่ได้รับความยินยอม — บันทึกเข้าคลังได้ แต่จะ **ดำเนินการต่อ (คัดกรอง / สัมภาษณ์ / ข้อเสนอ) ไม่ได้** จนกว่าจะได้รับความยินยอม" | ☐ |
| 3 | CLICK ปุ่ม **ยืนยันสร้าง** | — | บันทึกได้ (ไม่บล็อก) · toast **"สร้างผู้สมัครสำเร็จ"** | ☐ |
| 4 | VERIFY แถวใหม่ | — | ผู้สมัคร **ปกรณ์ ใจดี** · ความยินยอม chip **รอความยินยอม** (แดง) · ช่องทางติดต่อ = **ต้องได้รับความยินยอมก่อน** (ปิดบัง lock) | ☐ |

#### TC-B03 — ตรวจซ้ำ email/phone → เตือน ไม่บล็อก (FN-14 · EC-02)
- group: ผู้สมัคร · ความสำคัญ: สูง · trace: FN-14 / BR-10 / EC-02 / AT-08 · actor: recruiter
- Setup: role=recruiter · reload · seed=C1 ธนวัฒน์ (email thanawat.s@example.com) มีอยู่ · files=—
- Start: OPEN `#/recruit/pool` → เพิ่มผู้สมัคร
- ชุดข้อมูล: DS-CAND-DUP
- ผ่านเมื่อ: อีเมลตรงผู้สมัครเดิม → live note "พบผู้สมัครซ้ำ/เคยสมัคร" แต่บันทึกต่อได้ · แถวใหม่มี chip "เคยสมัคร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **เพิ่มผู้สมัคร** | — | drawer ฟอร์ม | ☐ |
| 2 | TYPE ชื่อ `ทดสอบ ซ้ำ` · **อีเมล** `thanawat.s@example.com` → คลิกออกจากช่อง (blur) | DS-CAND-DUP | live note เหลือง **"พบผู้สมัครซ้ำ/เคยสมัคร — ธนวัฒน์ ศรีสมบัติ (APP-2569-0011) มีอีเมล/เบอร์ตรงกัน · บันทึกต่อได้ (เตือนไม่บล็อก)"** | ☐ |
| 3 | TYPE เบอร์ + สลับ consent เป็นยินยอม → CLICK **ยืนยันสร้าง** | — | บันทึกได้ · toast **"สร้างผู้สมัครสำเร็จ"** | ☐ |
| 4 | VERIFY แถวใหม่ | — | ชื่อ **ทดสอบ ซ้ำ** มี chip **"เคยสมัคร"** (amber) ต่อท้ายชื่อ | ☐ |

#### TC-B04 — validate ฟอร์มผู้สมัครไม่ครบ (negative · VR-01)
- group: ผู้สมัคร · ความสำคัญ: สูง · trace: FN-92 / VR-01 / AT-21 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/pool` → เพิ่มผู้สมัคร
- ชุดข้อมูล: DS-CAND-BAD
- ผ่านเมื่อ: submit ว่าง → toast + ช่อง ชื่อ/อีเมล/เบอร์ ขึ้นกรอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **เพิ่มผู้สมัคร** | — | drawer ฟอร์ม (ช่องว่าง) | ☐ |
| 2 | CLICK ปุ่ม **ยืนยันสร้าง** (ไม่กรอกอะไร) | — | toast warning **"กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ"** · ช่อง **ชื่อ-นามสกุล**, **อีเมล**, **เบอร์โทร** ขึ้นกรอบแดง + error inline ("กรุณากรอกชื่อ"/"กรุณากรอกอีเมล"/"กรุณากรอกเบอร์โทร") · drawer ไม่ปิด | ☐ |

#### TC-B05 — บันทึกความยินยอมภายหลัง → unmask (FN-05)
- group: ผู้สมัคร · ความสำคัญ: สูง · trace: FN-05 / AT-09 · actor: recruiter
- Setup: role=recruiter · reload · seed=C1 ธนวัฒน์ (ยังไม่ยินยอม) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C1
- ผ่านเมื่อ: กด "บันทึกความยินยอม" → toast "บันทึกความยินยอมแล้ว" · consent → ยินยอม · ติดต่อ unmask (recruiter)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK แถว **ธนวัฒน์ ศรีสมบัติ** | — | drawer ผู้สมัคร แท็บ **รายละเอียด** · banner แดง **"ยังไม่ได้รับความยินยอม PDPA"** + ปุ่ม **บันทึกความยินยอม** · ช่องทางติดต่อ = **ปิดบังจนกว่าจะได้รับความยินยอม** | ☐ |
| 2 | CLICK ปุ่ม **บันทึกความยินยอม** | — | WAIT toast success **"บันทึกความยินยอมแล้ว"** · banner เปลี่ยนเป็น info เขียว "ได้รับความยินยอม PDPA เมื่อ …" | ☐ |
| 3 | VERIFY แถว KV ข้อมูลติดต่อ | — | recruiter (unmask) เห็น **อีเมล** และ **เบอร์โทร เต็ม** (ไม่มี lock) | ☐ |

#### TC-B06 — retention label อ่านจาก Policy Center (FIX-03 · ห้ามระบุ "ไม่มีวันหมดอายุ")
- group: ผู้สมัคร · ความสำคัญ: กลาง · trace: BR-02 / OQ-16 / LOCK-OB2 / FIX-03 · actor: recruiter
- Setup: role=recruiter · reload · seed=ผู้สมัครที่ยินยอมแล้ว (เช่น C2/C3 หรือ C1 หลัง TC-B05) · files=—
- Start: OPEN `#/recruit/pool` → เปิดผู้สมัครที่ยินยอมแล้ว
- ผ่านเมื่อ: banner consent เขียวแสดงระยะเก็บ = **"ตามนโยบาย Policy Center (รอกำหนดระยะ)"** และ **ไม่มี** คำว่า "ไม่มีวันหมดอายุ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK แถว **สุพิชญา อินทโชติ** (C2 · ยินยอมแล้ว) | — | drawer แท็บ รายละเอียด · banner info เขียว | ☐ |
| 2 | VERIFY ข้อความ retention ใน banner | — | มีข้อความ **"ระยะเก็บ (retention): ตามนโยบาย Policy Center (รอกำหนดระยะ)"** · **ไม่พบ** คำว่า "ไม่มีวันหมดอายุ" ที่ใดในจอ | ☐ |

---

### G-C · บอร์ดสรรหา (pipeline)

#### TC-C01 — เลื่อนสถานะไปข้างหน้า (happy · FN-06)
- group: บอร์ด · ความสำคัญ: สูง · trace: FN-06 / BR-03 / AT-10 · actor: recruiter
- Setup: role=recruiter · reload · seed=C2 สุพิชญา (คัดกรอง · ยินยอม) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: กด "ถัดไป" บนการ์ด C2 → ย้ายจากคอลัมน์ **คัดกรอง** ไป **สัมภาษณ์** + toast NTF

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` | — | kanban 5 คอลัมน์: สมัครใหม่/คัดกรอง/สัมภาษณ์/ข้อเสนอ/รับเข้าทำงาน · การ์ด **สุพิชญา อินทโชติ** อยู่คอลัมน์ **คัดกรอง** | ☐ |
| 2 | VERIFY+บันทึก ตัวนับหัวคอลัมน์ | — | จด: คัดกรอง=N1, สัมภาษณ์=N2 (อ้างใน step ถัดไป) | ☐ |
| 3 | CLICK ปุ่ม **ถัดไป** บนการ์ดสุพิชญา | — | การ์ดย้ายไปคอลัมน์ **สัมภาษณ์** · WAIT toast info NTF **"แจ้งเตือน: สุพิชญา อินทโชติ → สัมภาษณ์"** | ☐ |
| 4 | VERIFY ตัวนับหัวคอลัมน์อีกครั้ง | — | คัดกรอง = N1−1 · สัมภาษณ์ = N2+1 (เทียบค่าที่จดใน step 2) | ☐ |

#### TC-C02 — เลื่อนถอยหลัง (←)
- group: บอร์ด · ความสำคัญ: กลาง · trace: FN-06 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ (สัมภาษณ์) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: กดปุ่ม ← บนการ์ดที่ไม่ใช่คอลัมน์แรก → ถอยกลับ 1 คอลัมน์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` · หา การ์ด **กิตติพงษ์ แซ่ลิ้ม** (คอลัมน์ สัมภาษณ์) | — | การ์ดมีปุ่ม **←** (enabled เพราะไม่ใช่คอลัมน์แรก) | ☐ |
| 2 | CLICK ปุ่ม **←** บนการ์ดกิตติพงษ์ | — | การ์ดย้ายกลับคอลัมน์ **คัดกรอง** (ถอย 1 ขั้น · ไม่ต้องเช็ค consent เพราะ dir<0) | ☐ |

#### TC-C03 — เลื่อนไม่ได้เพราะยังไม่ยินยอม (negative · EC-01)
- group: บอร์ด · ความสำคัญ: สูง · trace: FN-05 / EC-01 / BR-02 / BR_CONSENT_REQUIRED / AT-11 · actor: recruiter
- Setup: role=recruiter · reload · seed=C1 ธนวัฒน์ (สมัครใหม่ · **ไม่ยินยอม**) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: กด "ถัดไป" บนการ์ดที่ยังไม่ยินยอม → ปุ่ม disabled หรือ block + toast เตือน (ไม่ย้าย)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` · หา การ์ด **ธนวัฒน์ ศรีสมบัติ** (คอลัมน์ สมัครใหม่) | — | การ์ดมี chip **รอความยินยอม** (แดง) · ปุ่ม **ถัดไป** อยู่ในสถานะ **disabled** (`canFwd` เป็น false เพราะ !consent) | ☐ |
| 2 | VERIFY สถานะปุ่ม ถัดไป | — | ปุ่มจางลง/กดไม่ได้ (disabled) — ระบบกัน dir>0 โดยไม่ยินยอมตั้งแต่ปุ่ม | ☐ |
| 3 | (ถ้าปุ่มกดได้ในบาง build) CLICK **ถัดไป** | — | toast warning **"ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้"** · การ์ดไม่ย้าย | ☐ |

#### TC-C04 — เข้าขั้น "ข้อเสนอ" ต้องมี offer ก่อน (guard)
- group: บอร์ด · ความสำคัญ: สูง · trace: FN-06 / BR_OFFER_REQUIRED · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ (สัมภาษณ์ · ยินยอม · **ยังไม่มี offer**) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: กด "ถัดไป" จากสัมภาษณ์→ข้อเสนอ ที่ยังไม่มี offer → ไม่ย้าย + toast info + เด้งไปแท็บข้อเสนอในลิ้นชัก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` · การ์ด **กิตติพงษ์ แซ่ลิ้ม** (สัมภาษณ์ · ยินยอม) | — | ปุ่ม **ถัดไป** enabled (consent ok) | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | toast info **"ไปขั้น “ข้อเสนอ” ให้สร้างข้อเสนอในลิ้นชักผู้สมัคร"** · drawer ผู้สมัครเปิดที่แท็บ **ข้อเสนอ** พร้อมฟอร์มสร้างข้อเสนอ · การ์ด **ไม่ย้าย**ไปคอลัมน์ข้อเสนอ (ยังคงสัมภาษณ์) | ☐ |

#### TC-C05 — บอร์ดข้ามไป hired ตรง ๆ ไม่ได้ (negative · FIX-01)
- group: บอร์ด · ความสำคัญ: สูง · trace: FN-11 / EC-05 / BR_HIRE_ROUTE_ONLY / BR_OFFER_NOT_ACCEPTED / LD-01 / AT-16 · actor: recruiter
- Setup: role=recruiter · reload · seed=C4 อารยา (ข้อเสนอ · offer.status=**sent** ยังไม่ accepted) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: กด "ถัดไป" จาก ข้อเสนอ→รับเข้าทำงาน ที่ offer ยังไม่ accepted → block + toast (ต้องตอบรับก่อน · route ผ่าน hire เท่านั้น)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` · การ์ด **อารยา พงษ์พิพัฒน์** (คอลัมน์ ข้อเสนอ) | — | ปุ่ม **ถัดไป** enabled (consent ok · ยังไม่ถึงคอลัมน์สุดท้าย) | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | toast info **"ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน"** · การ์ด **ไม่ย้าย**ไป รับเข้าทำงาน · drawer เปิดที่แท็บ **ข้อเสนอ** (ยืนยัน: เข้า hired ผ่าน move-stage ไม่ได้ — FIX-01) | ☐ |

#### TC-C06 — การ์ด hired ไม่มีปุ่ม forward (state)
- group: บอร์ด · ความสำคัญ: กลาง · trace: state machine (hired terminal) · actor: recruiter
- Setup: role=recruiter · reload · seed=C5 ณัฐพล (hired) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: การ์ดคอลัมน์สุดท้ายแสดง "✓ รับเข้าทำงานแล้ว" ไม่มีปุ่มถัดไป

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` · คอลัมน์ **รับเข้าทำงาน** | — | การ์ด **ณัฐพล เจริญสุข** แสดงข้อความ **"✓ รับเข้าทำงานแล้ว"** แทนแถวปุ่ม · **ไม่มีปุ่ม "ถัดไป"** | ☐ |
| 2 | VERIFY note นอกไปป์ไลน์ล่างบอร์ด | — | note info **"นอกไปป์ไลน์ · N รายการ"** ไล่ชื่อ terminal (เช่น พีรพล ทองดี (เก็บ Talent Pool)) | ☐ |

#### TC-C07 — ตัวนับคอลัมน์ตรงกับข้อมูล (VERIFY)
- group: บอร์ด · ความสำคัญ: ต่ำ · trace: FN-06 (display) · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: จำนวนการ์ดต่อคอลัมน์ = ตัวเลข `.kb-count` หัวคอลัมน์ · คอลัมน์ว่างขึ้น "— ว่าง —"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` | — | seed: สมัครใหม่=1 (ธนวัฒน์) · คัดกรอง=1 (สุพิชญา) · สัมภาษณ์=1 (กิตติพงษ์) · ข้อเสนอ=1 (อารยา) · รับเข้าทำงาน=1 (ณัฐพล) — ตัวเลขหัวคอลัมน์ตรงกับจำนวนการ์ด | ☐ |
| 2 | VERIFY คอลัมน์ที่ไม่มีการ์ด | — | แสดง **"— ว่าง —"** (ถ้ามีคอลัมน์ว่าง) | ☐ |

---

### G-D · สัมภาษณ์ + scorecard

#### TC-D01 — นัดสัมภาษณ์ + แจ้งเตือน (FN-07 · BR-09 snapshot)
- group: สัมภาษณ์ · ความสำคัญ: กลาง · trace: FN-07 / BR-09 / XT-03 / AT-12 · actor: recruiter
- Setup: role=recruiter · reload · seed=C2 สุพิชญา (คัดกรอง · ยินยอม) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C2 → แท็บ สัมภาษณ์ / ประเมิน
- ชุดข้อมูล: DS-INTERVIEW
- ผ่านเมื่อ: บันทึกนัด → toast "นัดสัมภาษณ์แล้ว" + snapshot ผู้สัมภาษณ์แสดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK แถว **สุพิชญา อินทโชติ** → CLICK แท็บ **สัมภาษณ์ / ประเมิน** | — | แท็บ assess · แสดง "ยังไม่มีการนัดสัมภาษณ์" + ปุ่ม **นัดสัมภาษณ์** | ☐ |
| 2 | CLICK ปุ่ม **นัดสัมภาษณ์** | — | modal **นัดสัมภาษณ์** เปิด (วันที่/เวลา/ผู้สัมภาษณ์/สถานที่) | ☐ |
| 3 | CLICK ปุ่ม **นัดสัมภาษณ์** (ในmodal · ยังไม่กรอก) | — | toast warning **"กรุณากรอกข้อมูลให้ครบถ้วน"** | ☐ |
| 4 | TYPE วันที่ `2026-09-20` · เวลา `10:30` · เลือกผู้สัมภาษณ์ **อรรถพล ชัยมงคล** · สถานที่ `ห้องประชุม 2 · Google Meet` | DS-INTERVIEW | ฟิลด์ครบ | ☐ |
| 5 | CLICK ปุ่ม **นัดสัมภาษณ์** | — | modal ปิด · WAIT toast success **"นัดสัมภาษณ์แล้ว"** (ก่อนหน้ามี toast info NTF "แจ้งเตือน: นัดสัมภาษณ์ สุพิชญา อินทโชติ") | ☐ |
| 6 | VERIFY แท็บ assess | — | มีบล็อกสัมภาษณ์ · ผู้สัมภาษณ์ snapshot = **อรรถพล ชัยมงคล · Senior Frontend Engineer** · การ์ดผู้สมัครเลื่อนเป็นระยะ **สัมภาษณ์** | ☐ |

#### TC-D02 — ให้คะแนน scorecard (happy · FN-09)
- group: สัมภาษณ์ · ความสำคัญ: กลาง · trace: FN-09 / AT-13 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ มีนัดสัมภาษณ์ IV1 (ยังไม่ให้คะแนนรอบใหม่ — seed มี scorecard แล้ว จึงต้องนัดใหม่ก่อน หรือใช้ผู้สมัครที่มีนัดแต่ยังไม่ score). ⚠ ในseed C3 IV1 มี scorecard แล้ว → ให้ทำ TC-D01 กับ C2 ก่อนเพื่อได้ช่อง scorecard ว่าง · files=—
- Start: OPEN `#/recruit/pool` → เปิดผู้สมัครที่มีนัดสัมภาษณ์ยังไม่ประเมิน → แท็บ assess
- ผ่านเมื่อ: เลือกคะแนน 1–5 + comment → toast "บันทึกผลประเมินแล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (ต่อจาก TC-D01) เปิด **สุพิชญา** แท็บ **สัมภาษณ์ / ประเมิน** | — | มีบล็อกสัมภาษณ์ที่ยังไม่มีผล + แถว **ให้คะแนน (ต่อผู้สัมภาษณ์)** ปุ่ม 1–5 + textarea ความเห็น | ☐ |
| 2 | CLICK ปุ่มคะแนน **4** | — | ปุ่ม 1–4 ติดสถานะ on (ไฮไลต์) | ☐ |
| 3 | TYPE → textarea **ความเห็น** | `สื่อสารดี พื้นฐานแน่น` | textarea แสดงข้อความ | ☐ |
| 4 | CLICK ปุ่ม **บันทึกผลประเมิน** | — | toast success **"บันทึกผลประเมินแล้ว"** · บล็อกแสดง scorecard **4/5** + ความเห็น · คะแนนโผล่ในคอลัมน์คะแนนของคลัง | ☐ |

#### TC-D03 — บันทึก scorecard โดยไม่ให้คะแนน (negative)
- group: สัมภาษณ์ · ความสำคัญ: กลาง · trace: FN-09 / AT-13 (neg) · actor: recruiter
- Setup: role=recruiter · reload · seed=ผู้สมัครมีนัดสัมภาษณ์ยังไม่ประเมิน (เช่นหลัง TC-D01) · files=—
- Start: แท็บ assess ของผู้สมัครนั้น
- ผ่านเมื่อ: กด "บันทึกผลประเมิน" โดยไม่เลือกคะแนน → toast "กรุณาให้คะแนนก่อน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดแท็บ assess ผู้สมัครที่มีบล็อกให้คะแนนว่าง | — | ปุ่ม 1–5 ยังไม่เลือก | ☐ |
| 2 | CLICK ปุ่ม **บันทึกผลประเมิน** (ไม่เลือกคะแนน) | — | toast warning **"กรุณาให้คะแนนก่อน"** · ไม่บันทึก | ☐ |

#### TC-D04 — แท็บสัมภาษณ์ถูก gate เมื่อไม่ยินยอม (negative · BR-02)
- group: สัมภาษณ์ · ความสำคัญ: สูง · trace: FN-05 / BR-02 / EC-01 · actor: recruiter
- Setup: role=recruiter · reload · seed=C1 ธนวัฒน์ (ไม่ยินยอม) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C1 → แท็บ สัมภาษณ์ / ประเมิน
- ผ่านเมื่อ: ไม่ยินยอม → แท็บ assess โชว์ banner block ไม่มีปุ่มนัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK แถว **ธนวัฒน์ ศรีสมบัติ** → CLICK แท็บ **สัมภาษณ์ / ประเมิน** | — | แสดง banner แดง **"ยังไม่ได้รับความยินยอม PDPA — นัดสัมภาษณ์/ประเมินไม่ได้"** · **ไม่มี** ปุ่มนัดสัมภาษณ์ | ☐ |

---

### G-E · ข้อเสนอ + รับเข้าทำงาน

#### TC-E01 — สร้างข้อเสนอในช่วง band → ส่งอนุมัติ (FN-10 · BR-09)
- group: ข้อเสนอ · ความสำคัญ: สูง · trace: FN-10 / BR-04 / BR-09 / XT-04 / AT-14 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ (สัมภาษณ์ · ยินยอม · ยังไม่มี offer) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C3 → แท็บ ข้อเสนอ
- ชุดข้อมูล: DS-OFFER-IN + DS-DOA-APPROVERS
- ผ่านเมื่อ: กรอกในช่วง band → สร้าง offer → DOA modal เปิด → ส่งอนุมัติแล้ว · สถานะข้อเสนอ = รออนุมัติ · freeze version_id

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **กิตติพงษ์ แซ่ลิ้ม** → แท็บ **ข้อเสนอ** | — | ฟอร์ม **สร้างข้อเสนอจ้าง** · การ์ด band แสดงช่วงตาม grade + เวอร์ชัน **SS-2569-03** | ☐ |
| 2 | SELECT `G4` → **ระดับ (band)** · TYPE วันเริ่มงาน `2026-10-01` | DS-OFFER-IN | band card อัปเดตเป็น G4 (45,000–85,000) | ☐ |
| 3 | TYPE → **เงินเดือนที่เสนอ** | `62000` | ไม่มี note นอกช่วง (62,000 อยู่ในช่วง) · ไม่มีช่องเหตุผลบังคับ | ☐ |
| 4 | CLICK ปุ่ม **สร้างข้อเสนอ + ส่งอนุมัติ** | — | modal **ส่งอนุมัติ (DOA)** เปิด · DOA entry **DOA-OFFER-001** · 2 slot | ☐ |
| 5 | เลือกผู้อนุมัติ slot 1=**ธีรภัทร วงศ์ไพศาล** · slot 2=**ปิยะนุช สมานมิตร** → CLICK **ส่งอนุมัติ** | DS-DOA-APPROVERS | modal ปิด · toast success **"ส่งอนุมัติแล้ว"** | ☐ |
| 6 | VERIFY แท็บข้อเสนอ | — | ข้อเสนอสถานะ pill **รออนุมัติ** · KV เงินเดือน **62,000 บาท** · band freeze **(freeze SS-2569-03)** · timeline DOA 2 ขั้น (รอ) | ☐ |

#### TC-E02 — ข้อเสนอนอกช่วง band → บังคับเหตุผล (edge · EC-04 · VR-03)
- group: ข้อเสนอ · ความสำคัญ: สูง · trace: FN-10 / EC-04 / VR-03 / BR_OUT_OF_BAND_REASON / AT-14 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ (ยังไม่มี offer) · files=—
- Start: แท็บ ข้อเสนอ ของ C3
- ชุดข้อมูล: DS-OFFER-OUT
- ผ่านเมื่อ: เงินนอกช่วง → note เตือน + ช่องเหตุผลบังคับ; ไม่กรอกเหตุผล → toast block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดแท็บ **ข้อเสนอ** ของ C3 → SELECT `G4` · วันเริ่ม `2026-10-01` · เงินเดือน `95000` | DS-OFFER-OUT | note เหลือง **"เงินนอกช่วง band (45,000–85,000) — เตือนไม่บล็อก แต่ต้องระบุเหตุผล"** ปรากฏ + ช่อง **เหตุผลนอกช่วง (out_of_range_reason) \*** โผล่ | ☐ |
| 2 | CLICK ปุ่ม **สร้างข้อเสนอ + ส่งอนุมัติ** (ยังไม่กรอกเหตุผล) | — | toast warning **"เงินนอกช่วง band — กรุณาระบุเหตุผล"** · ไม่เปิด DOA modal | ☐ |
| 3 | TYPE → **เหตุผลนอกช่วง** | `ประสบการณ์ 10 ปี สูงกว่ามาตรฐานระดับ` | ช่องแสดงเหตุผล | ☐ |
| 4 | CLICK ปุ่ม **สร้างข้อเสนอ + ส่งอนุมัติ** | — | modal DOA เปิด (ผ่านแล้ว) · ยืนยันว่าต้องมีเหตุผลก่อนจึงไปต่อได้ | ☐ |

#### TC-E03 — validate ข้อเสนอขาดวันเริ่ม/เงินเดือน (negative · VR-01)
- group: ข้อเสนอ · ความสำคัญ: กลาง · trace: FN-92 / VR-01 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 (ยังไม่มี offer) · files=—
- Start: แท็บ ข้อเสนอ ของ C3
- ชุดข้อมูล: DS-OFFER-BAD
- ผ่านเมื่อ: submit โดยไม่มีวันเริ่ม/เงินเดือน → toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดแท็บ **ข้อเสนอ** ของ C3 (ไม่กรอกวันเริ่ม/เงินเดือน) → CLICK **สร้างข้อเสนอ + ส่งอนุมัติ** | DS-OFFER-BAD | toast warning **"กรุณากรอกวันเริ่มงานและเงินเดือน"** · ไม่เปิด DOA modal | ☐ |

#### TC-E04 — manager อนุมัติข้อเสนอ (FN-08 · BR-04)
- group: ข้อเสนอ · ความสำคัญ: สูง · trace: FN-08 / BR-04 / permission(manager) / AT-15 · actor: manager
- Setup: role→manager · seed=ข้อเสนอสถานะ **รออนุมัติ** (ทำ TC-E01 ต่อเนื่องก่อนสลับ persona) · files=—
- Start: OPEN `#/recruit/pool` → เปิดผู้สมัครที่มี offer รออนุมัติ → แท็บ ข้อเสนอ
- ผ่านเมื่อ: manager เห็นปุ่มอนุมัติข้อเสนอ → อนุมัติครบ → toast "อนุมัติแล้ว" · สถานะ → อนุมัติแล้ว · พร้อมส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **ผู้จัดการสายงาน** → เปิดผู้สมัครที่มี offer รออนุมัติ → แท็บ **ข้อเสนอ** | — | มีปุ่ม **ไม่อนุมัติ** + **อนุมัติข้อเสนอ** (เห็นเพราะ canApprove) | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติข้อเสนอ** | — | toast success **"อนุมัติแล้ว"** · สถานะข้อเสนอ pill → **อนุมัติแล้ว · พร้อมส่ง** · ปุ่มเปลี่ยนเป็น **ส่งข้อเสนอให้ผู้สมัคร** | ☐ |

#### TC-E05 — ส่งข้อเสนอให้ผู้สมัคร (approved → sent)
- group: ข้อเสนอ · ความสำคัญ: กลาง · trace: BR-04 / XT-03 · actor: recruiter
- Setup: role=recruiter · seed=ข้อเสนอสถานะ **อนุมัติแล้ว · พร้อมส่ง** (ต่อจาก TC-E04) · files=—
- Start: แท็บ ข้อเสนอ ของผู้สมัครนั้น
- ผ่านเมื่อ: กด "ส่งข้อเสนอให้ผู้สมัคร" → toast "ส่งข้อเสนอแล้ว" · สถานะ → ส่งข้อเสนอแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=recruiter) เปิดแท็บ **ข้อเสนอ** ที่สถานะ อนุมัติแล้ว · พร้อมส่ง → CLICK **ส่งข้อเสนอให้ผู้สมัคร** | — | toast success **"ส่งข้อเสนอแล้ว"** (นำหน้าด้วย toast info NTF "แจ้งเตือน: ส่งข้อเสนอให้ …") · สถานะ pill → **ส่งข้อเสนอแล้ว** · ปุ่มเปลี่ยนเป็น **ผู้สมัครปฏิเสธ** + **ผู้สมัครตอบรับ** | ☐ |

#### TC-E06 — ผู้สมัครตอบรับ → รับเข้าทำงาน → handoff (FN-11 · XT-01)
- group: ข้อเสนอ · ความสำคัญ: สูง · trace: FN-11 / BR-05 / XT-01 / LOCK-OB1 / AT-16 · actor: recruiter
- Setup: role=recruiter · reload · seed=C4 อารยา (offer.status=**sent**) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C4 → แท็บ ข้อเสนอ
- ผ่านเมื่อ: ตอบรับ → hire confirm → toast "ส่งเข้า onboarding แล้ว" · stage=รับเข้าทำงาน · chip onboarding · **ไม่สร้าง employee**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **อารยา พงษ์พิพัฒน์** → แท็บ **ข้อเสนอ** | — | ข้อเสนอสถานะ **ส่งข้อเสนอแล้ว** · ปุ่ม **ผู้สมัครปฏิเสธ** + **ผู้สมัครตอบรับ** | ☐ |
| 2 | CLICK ปุ่ม **ผู้สมัครตอบรับ** | — | toast success **"บันทึกผลข้อเสนอแล้ว"** · สถานะ pill → **ตอบรับ** · ปุ่มใหม่ **รับเข้าทำงาน → ส่ง On/Offboard** | ☐ |
| 3 | CLICK ปุ่ม **รับเข้าทำงาน → ส่ง On/Offboard** | — | confirm modal หัวข้อ **"รับเข้าทำงาน + ส่งเข้า On/Offboard?"** · body มีข้อความ **"…ไม่สร้าง employee และไม่เชื่อมจริงในรอบนี้"** · ปุ่ม **ยืนยันรับเข้าทำงาน** | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันรับเข้าทำงาน** | — | modal ปิด · WAIT toast success **"ส่งเข้า onboarding แล้ว"** (นำหน้าด้วย toast info "แจ้งเตือน: ส่ง อารยา … เข้ากระบวนการ onboarding") | ☐ |
| 5 | VERIFY drawer header ผู้สมัคร | — | มี stage pill **รับเข้าทำงาน** + chip **"ส่งเข้า onboarding แล้ว"** · ไม่มี action อื่นให้กด (terminal) | ☐ |
| 6 | VERIFY (LOCK-OB1) | — | ไม่มี toast/หน้าจอ/ปุ่มใดที่บ่งชี้ว่ามีการ **สร้าง employee record** — ระบบยิง event อย่างเดียว (soft-linkage) | ☐ |

#### TC-E07 — ปุ่มส่งข้อเสนอไม่โผล่ตอนยังไม่อนุมัติ (negative · BR-04)
- group: ข้อเสนอ · ความสำคัญ: สูง · trace: BR-04 / BR_OFFER_NOT_APPROVED / NEG · actor: recruiter
- Setup: role=recruiter · seed=ข้อเสนอสถานะ **รออนุมัติ** (ทำ TC-E01 · ยังไม่ให้ manager อนุมัติ) · files=—
- Start: แท็บ ข้อเสนอ ของผู้สมัครนั้น (recruiter)
- ผ่านเมื่อ: recruiter ที่ไม่มีสิทธิ์อนุมัติ + สถานะยังรออนุมัติ → **ไม่มีปุ่ม "ส่งข้อเสนอให้ผู้สมัคร"** (ส่งก่อนอนุมัติไม่ได้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=recruiter) เปิดแท็บ **ข้อเสนอ** ที่สถานะ **รออนุมัติ** | — | มี timeline DOA (รอ) · **ไม่มีปุ่ม "ส่งข้อเสนอให้ผู้สมัคร"** และ **ไม่มีปุ่ม "อนุมัติข้อเสนอ"** (recruiter ไม่ใช่ผู้อนุมัติ) — ส่งได้ต่อเมื่อสถานะ=อนุมัติแล้ว เท่านั้น | ☐ |

#### TC-E08 — ข้อเสนอปฏิเสธ → ผู้สมัครถอนตัว (offer declined)
- group: ข้อเสนอ · ความสำคัญ: กลาง · trace: FN-12 / offerResult(declined) · actor: recruiter
- Setup: role=recruiter · reload · seed=C4 อารยา (offer sent) · files=—
- Start: เปิด C4 → แท็บ ข้อเสนอ
- ผ่านเมื่อ: กด "ผู้สมัครปฏิเสธ" → toast · สถานะข้อเสนอ ปฏิเสธ · ผู้สมัคร → ถอนตัว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด **อารยา** แท็บ **ข้อเสนอ** → CLICK ปุ่ม **ผู้สมัครปฏิเสธ** | — | toast success **"บันทึกผลข้อเสนอแล้ว"** · สถานะข้อเสนอ pill → **ปฏิเสธข้อเสนอ** (แดง) | ☐ |
| 2 | VERIFY ระยะผู้สมัคร | — | stage pill ของผู้สมัคร → **ถอนตัว** (terminal · candidate.stage=withdrawn) | ☐ |

#### TC-E09 — band freeze ยึด snapshot เดิม (XT-02 · EC-11) → ดู TC-X02
- group: ข้อเสนอ · ความสำคัญ: กลาง · trace: XT-02 / EC-11 / BR-09 · actor: recruiter
- Setup: ดู TC-X02 (cross-module) — เคสนี้ pointer เพื่อ trace FN-10 ↔ band freeze
- Start: — · ผ่านเมื่อ: ดู TC-X02

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ดู **TC-X02** (band freeze cross-module) | — | offer เดิมยึด `version_id` freeze — verify ที่ TC-X02 | ☐ |

---

### G-F · ไม่ผ่าน/ถอนตัว/talent pool

#### TC-F01 — ไม่ผ่าน/ถอนตัว บันทึกเหตุผล (FN-12 · soft archive)
- group: terminate · ความสำคัญ: กลาง · trace: FN-12 / FN-91 / BR-07 / AT-17 · actor: recruiter
- Setup: role=recruiter · reload · seed=C2 สุพิชญา (คัดกรอง · ไม่ terminal) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C2
- ชุดข้อมูล: DS-REASON
- ผ่านเมื่อ: เลือกผล + เหตุผล → toast "บันทึกแล้ว" · ระยะ → terminal · soft archive (record ยังอยู่)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **สุพิชญา อินทโชติ** | — | drawer · header มีปุ่ม **ไม่ผ่าน/ถอนตัว** (แดง) | ☐ |
| 2 | CLICK ปุ่ม **ไม่ผ่าน/ถอนตัว** | — | modal **ไม่ผ่าน / ถอนตัว** · มี select ผลลัพธ์ (default "ไม่ผ่าน → เก็บ Talent Pool") + textarea เหตุผล | ☐ |
| 3 | SELECT **ผู้สมัครถอนตัว** → **ผลลัพธ์** · TYPE เหตุผล `DS-REASON` | DS-REASON | ค่าถูกเลือก | ☐ |
| 4 | CLICK ปุ่ม **บันทึก** | — | modal ปิด · WAIT toast success **"บันทึกแล้ว"** · stage pill ผู้สมัคร → **ถอนตัว** (terminal) | ☐ |
| 5 | VERIFY คลัง/บอร์ด | — | ผู้สมัครยังอยู่ในคลัง (soft archive · ไม่ถูกลบ) · บนบอร์ดออกจากไปป์ไลน์ → note "นอกไปป์ไลน์" | ☐ |

#### TC-F02 — terminate ไม่มีเหตุผล (negative · BR_REASON_REQUIRED)
- group: terminate · ความสำคัญ: กลาง · trace: FN-12 / BR_REASON_REQUIRED / AT-17(neg) · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ (ไม่ terminal) · files=—
- Start: เปิด C3 → ปุ่ม ไม่ผ่าน/ถอนตัว
- ผ่านเมื่อ: ไม่กรอกเหตุผล → toast "กรุณาระบุเหตุผล" (บล็อก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด **กิตติพงษ์** → CLICK **ไม่ผ่าน/ถอนตัว** → CLICK ปุ่ม **บันทึก** (เหตุผลว่าง) | — | toast warning **"กรุณาระบุเหตุผล"** · modal ไม่ปิด · ผู้สมัครไม่เปลี่ยนสถานะ | ☐ |

#### TC-F03 — ไม่ผ่าน → เก็บ Talent Pool (FN-13 · default)
- group: terminate · ความสำคัญ: กลาง · trace: FN-13 / BR-07 / AT-18 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ · files=—
- Start: เปิด C3 → ปุ่ม ไม่ผ่าน/ถอนตัว
- ผ่านเมื่อ: เลือก default "ไม่ผ่าน → เก็บ Talent Pool" + เหตุผล → stage=เก็บ Talent Pool (terminal pill)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด **กิตติพงษ์** → CLICK **ไม่ผ่าน/ถอนตัว** | — | modal เปิด · select ผลลัพธ์ default = **ไม่ผ่าน → เก็บ Talent Pool** | ☐ |
| 2 | TYPE เหตุผล `DS-REASON` → CLICK **บันทึก** | DS-REASON | toast **"บันทึกแล้ว"** · stage pill → **เก็บ Talent Pool** (เทา) | ☐ |
| 3 | OPEN `#/recruit/pool` → filter ระยะ = **เก็บ Talent Pool** | — | ผู้สมัครอยู่ในรายการ terminal (ยังคงเก็บ · soft archive) | ☐ |

---

### G-G · รายงาน funnel

#### TC-G01 — funnel + stats แสดงถูก (FN-15)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-15 / AT-19 · actor: recruiter
- Setup: role=recruiter · reload (seed default) · files=—
- Start: OPEN `#/recruit/report`
- ผ่านเมื่อ: stat cards + funnel bars แสดงตัวเลขตรงกับ seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/report` | — | หน้า **รายงานการสรรหา (Funnel)** · แถบ stat 5 ใบ: ผู้สมัครทั้งหมด · กำลังสัมภาษณ์ · ข้อเสนอ · รับเข้าทำงาน · **Time-to-hire เฉลี่ย = 23 วัน** | ☐ |
| 2 | VERIFY stat "ผู้สมัครทั้งหมด" | — | = จำนวนผู้สมัคร seed ที่ scope=ทุกอัตรา (6) | ☐ |
| 3 | VERIFY funnel bars | — | 5 แถว (สมัครใหม่→…→รับเข้าทำงาน) · แต่ละแถวมี "N คน" · แถบกว้างลดหลั่นตาม cumulative reached | ☐ |
| 4 | VERIFY note สรุป | — | "ผลการคัดเลือก: รับเข้าทำงาน N · ไม่ผ่าน/เก็บ Talent Pool N · ถอนตัว N" | ☐ |

#### TC-G02 — filter รายงานตามอัตรา (FN-15)
- group: รายงาน · ความสำคัญ: กลาง · trace: FN-15 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/report`
- ผ่านเมื่อ: เลือก "กรองตามอัตรา" → stat/funnel อัปเดตเฉพาะผู้สมัครในอัตรานั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/report` → VERIFY+จด "ผู้สมัครทั้งหมด" ตอน ทุกอัตรา | — | จดค่า A (เช่น 6) | ☐ |
| 2 | SELECT `REQ-2569-0001 · Senior Frontend Developer` → **กรองตามอัตรา** | — | stat "ผู้สมัครทั้งหมด" ลดเหลือเฉพาะผู้สมัครที่ผูก REQ-1 (< A) · funnel อัปเดตตาม | ☐ |

#### TC-G03 — Export CSV เป็น stub (FN-15)
- group: รายงาน · ความสำคัญ: ต่ำ · trace: FN-15 / AT-19 (export stub) · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/report`
- ผ่านเมื่อ: กด Export CSV → toast stub (ยังไม่ดาวน์โหลดจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/report` → CLICK ปุ่ม **Export CSV** (มุมขวาบน) | — | toast info **"ส่งออกรายงาน (CSV) — ต่อ dev"** · ไม่มีไฟล์ดาวน์โหลดจริง (stub) | ☐ |

---

### G-H · กติกากลาง (ค้นหา/validate/audit/mask/viewer)

#### TC-H01 — ค้นหา/filter อัตรา + empty state (FN-90)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-90 / AT-20 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/req`
- ผ่านเมื่อ: search/filter จน 0 แถว → empty state + ปุ่มล้างตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → TYPE ในช่องค้นหา (placeholder "ค้นหาตำแหน่ง / เลขที่ / แผนก") | `Frontend` | ตารางกรองเหลือแถวที่ตรง (Senior Frontend Developer) | ☐ |
| 2 | SELECT สถานะ = **ปิดแล้ว** (dropdown) · ล้างคำค้นก่อน | — | เหลือเฉพาะอัตราปิดแล้ว (REQ-2569-0003) | ☐ |
| 3 | TYPE คำค้นที่ไม่มีอยู่ | `zzz` | empty state **"ไม่พบอัตราที่เปิด"** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 4 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ตารางกลับมาครบทุกแถว (คำค้น+สถานะรีเซ็ต) | ☐ |

#### TC-H02 — ค้นหา/filter ผู้สมัคร + empty state (FN-90)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-90 / AT-20 · actor: recruiter
- Setup: role=recruiter · reload · files=—
- Start: OPEN `#/recruit/pool`
- ผ่านเมื่อ: filter ระยะ/ค้นหาจน 0 → "ไม่พบผู้สมัคร" + CTA เพิ่มผู้สมัคร

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → SELECT ระยะ = **สัมภาษณ์** | — | เหลือเฉพาะผู้สมัครระยะสัมภาษณ์ (กิตติพงษ์) | ☐ |
| 2 | TYPE คำค้น (placeholder "ค้นหาชื่อ / รหัส / อีเมล") | `ไม่มีคนนี้` | empty state **"ไม่พบผู้สมัคร"** + ปุ่ม **เพิ่มผู้สมัคร** | ☐ |
| 3 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ตารางกลับครบ 6 แถว | ☐ |

#### TC-H03 — กัน double-submit (VR-02 · loader) — ต้อง simulate
- group: กติกากลาง · ความสำคัญ: กลาง · trace: FN-92 / VR-02 / EC-09 / AT-21 · actor: recruiter
- Setup: role=recruiter · reload · files=— · **(ต้อง simulate)** — ปุ่ม disable+loader มี window ~300ms ก่อน drawer ปิด, จับด้วยสายตายาก; runner ที่กดเร็ว 2 ครั้งควรเห็นเพียง 1 record
- Start: OPEN `#/recruit/pool` → เพิ่มผู้สมัคร
- ผ่านเมื่อ: กดยืนยันสร้างซ้ำเร็ว → สร้างเพียง 1 record (RC.busy กันซ้ำ) · ปุ่มขึ้น loader-2 spin ชั่วขณะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เพิ่มผู้สมัคร DS-CAND-A → CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งติดเร็ว | DS-CAND-A | ระหว่าง submit ปุ่มแสดงไอคอน **loader-2** หมุน + disabled (ชั่วขณะ) · toast **"สร้างผู้สมัครสำเร็จ"** ปรากฏ **ครั้งเดียว** | ☐ |
| 2 | VERIFY ตารางคลัง | — | มีผู้สมัคร "วิศรุต ตั้งใจ" เพิ่ม **เพียง 1 แถว** (ไม่ซ้ำ) | ☐ |

#### TC-H04 — audit append-only (FN-93 · BR-03)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-93 / BR-03 / BR-07 / LOCK-OB5 / AT-22 · actor: recruiter
- Setup: role=recruiter · reload · seed=C3 กิตติพงษ์ (มีประวัติหลาย entry) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C3 → แท็บ ประวัติ
- ผ่านเมื่อ: ทุก action สร้าง entry ใหม่บนสุด · entry เก่าไม่ถูกลบ/แก้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **กิตติพงษ์ แซ่ลิ้ม** → CLICK แท็บ **ประวัติ** | — | timeline "ประวัติ (append-only)" · VERIFY+จด จำนวน entry = N (เช่น 3) | ☐ |
| 2 | CLICK แท็บ **สัมภาษณ์ / ประเมิน** → นัดสัมภาษณ์ใหม่ (DS-INTERVIEW) → บันทึก | DS-INTERVIEW | toast "นัดสัมภาษณ์แล้ว" | ☐ |
| 3 | CLICK แท็บ **ประวัติ** อีกครั้ง | — | มี entry ใหม่ **"นัดสัมภาษณ์ + แจ้งเตือน"** อยู่ **บนสุด** · entry เดิม N รายการ **ยังอยู่ครบด้านล่าง** (จำนวน = N+1) · ไม่มีปุ่มลบ/แก้ประวัติ | ☐ |

#### TC-H05 — masking ตาม role: manager เห็นปิดบัง (FN-94 · BR-06)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-94 / BR-06 / LOCK-OB5 / AT-23 · actor: manager
- Setup: role→manager · reload → สลับ persona · seed=C2 สุพิชญา (ยินยอมแล้ว) · files=—
- Start: OPEN `#/recruit/pool` (manager)
- ผ่านเมื่อ: manager เห็นอีเมล/เบอร์ masked + chip RESTRICTED

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **ผู้จัดการสายงาน** → OPEN `#/recruit/pool` → หา แถว **สุพิชญา** (ยินยอมแล้ว) | — | คอลัมน์ **ช่องทางติดต่อ** แสดงอีเมล masked (เช่น `s•••@example.com`) + เบอร์ `•••-•••-7777` + ไอคอน lock | ☐ |
| 2 | CLICK แถวสุพิชญา → แท็บ **รายละเอียด** | — | KV แสดงอีเมล/เบอร์ masked + chip **"RESTRICTED · ปิดบังตามบทบาท"** ข้างหัวข้อข้อมูลผู้สมัคร | ☐ |
| 3 | (สลับ persona=viewer) VERIFY อีกครั้ง | — | viewer ก็เห็น masked เหมือน manager (unmask=false) | ☐ |

#### TC-H06 — masking ตาม role: recruiter เห็นเต็ม (FN-94)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-94 / BR-06 / AT-23 · actor: recruiter
- Setup: role=recruiter · reload · seed=C2 สุพิชญา (ยินยอม) · files=—
- Start: OPEN `#/recruit/pool` (recruiter)
- ผ่านเมื่อ: recruiter (unmask) เห็นอีเมล/เบอร์เต็ม + ไม่มี chip RESTRICTED

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` (recruiter) → CLICK **สุพิชญา** → แท็บ **รายละเอียด** | — | KV แสดง **อีเมลเต็ม** `supichaya@example.com` + **เบอร์เต็ม** `0898887777` (ไม่มี lock) · **ไม่มี** chip RESTRICTED | ☐ |

#### TC-H07 — ปิดบังเมื่อยังไม่ยินยอม (FN-94 · list)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-94 / BR-06 / BR-02 · actor: recruiter
- Setup: role=recruiter · reload · seed=C1 ธนวัฒน์ (ไม่ยินยอม) · files=—
- Start: OPEN `#/recruit/pool`
- ผ่านเมื่อ: แม้ recruiter (unmask) แต่ผู้สมัครยังไม่ยินยอม → ช่องทางติดต่อปิดบังทั้งหมด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` (recruiter) → หา แถว **ธนวัฒน์ ศรีสมบัติ** (รอความยินยอม) | — | คอลัมน์ **ช่องทางติดต่อ** แสดง **"ต้องได้รับความยินยอมก่อน"** + lock (ไม่แสดงอีเมล/เบอร์เลย แม้ recruiter) | ☐ |

#### TC-H08 — viewer ไม่มีปุ่มสร้าง (VR-05 · permission)
- group: กติกากลาง · ความสำคัญ: สูง · trace: FN-... / VR-05 / EC-06 / AT-24 · actor: viewer
- Setup: role→viewer · reload → สลับ persona · files=—
- Start: OPEN แต่ละหน้า (viewer)
- ผ่านเมื่อ: viewer ไม่เห็นปุ่ม "เปิดอัตราใหม่"/"เพิ่มผู้สมัคร" และปุ่ม action ในบอร์ด/drawer หาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **ผู้ชมทั่วไป** → OPEN `#/recruit/req` | — | **ไม่มีปุ่ม "เปิดอัตราใหม่"** มุมขวาบน | ☐ |
| 2 | OPEN `#/recruit/pool` | — | **ไม่มีปุ่ม "เพิ่มผู้สมัคร"** | ☐ |
| 3 | OPEN `#/recruit/board` | — | การ์ดในบอร์ด: ปุ่ม **ถัดไป** และ **←** อยู่สถานะ disabled ทุกใบ (viewer) | ☐ |
| 4 | CLICK แถวผู้สมัครใด ๆ → VERIFY header drawer | — | **ไม่มีปุ่ม "ไม่ผ่าน/ถอนตัว"** · ในแท็บข้อเสนอไม่มีปุ่ม action | ☐ |

#### TC-H09 — viewer guard mutation ทางอ้อม (EC-06)
- group: กติกากลาง · ความสำคัญ: สูง · trace: VR-05 / EC-06 / ERR_INSUFFICIENT_ROLE / AT-24 · actor: viewer
- Setup: role=viewer · seed=ผู้สมัครที่ยังไม่ยินยอม (C1) · files=— · **(อาจต้อง simulate)** — viewer ปุ่ม mutation ถูกซ่อน; การเรียก guard ทางอ้อมทำได้ผ่าน consof เปิด drawer ตอน recruiter แล้วสลับเป็น viewer (OQ-D3 re-guard mid-drawer)
- Start: เปิด drawer ผู้สมัคร (recruiter) → สลับ persona=viewer → กด mutation
- ผ่านเมื่อ: viewer เรียก mutation → toast "สิทธิ์อ่านอย่างเดียว" (ไม่เปลี่ยนข้อมูล)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (persona=recruiter) OPEN `#/recruit/pool` → เปิด **ธนวัฒน์** (ไม่ยินยอม) → เห็นปุ่ม **บันทึกความยินยอม** ในแท็บรายละเอียด | — | ปุ่มบันทึกความยินยอมแสดง | ☐ |
| 2 | CLICK persona **ผู้ชมทั่วไป** (โดย drawer ยังเปิด) | — | ปุ่ม action ใน drawer หายไป (re-guard OQ-D3) · ถ้ายังกดปุ่ม mutation ใดได้ → toast warning **"สิทธิ์อ่านอย่างเดียว"** · ข้อมูลไม่เปลี่ยน (consent ยัง "รอความยินยอม") | ☐ |

---

### G-I · Edge `[AI-DEFAULT]` (ต้อง simulate)

#### TC-I01 — concurrent stage move → 409 (EC-07 · AI-DEFAULT)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-07 / OQ-D1 / ERR_STALE_DATA / AT-26 · `[AI-DEFAULT]` · actor: recruiter×2
- Setup: **(ต้อง simulate — backend)** — prototype in-memory ไม่มี optimistic lock UI (UI_BRIEF DR-03); ทดสอบจริงต้อง 2 session ยิง move-stage ผู้สมัครคนเดียวพร้อมกัน · role=recruiter · seed=ผู้สมัคร 1 คน (consent ok) · files=—
- Start: 2 client เปิดผู้สมัครคนเดียวกัน
- ผ่านเมื่อ: client แรก 200 · client ที่สอง 409 ERR_STALE_DATA + audit ทั้งคู่ (⚠ ต้องมี backend จริง; prototype จับไม่ได้ → BLOCKED ถ้าไม่มี)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate 2 session) CLICK **ถัดไป** ผู้สมัครคนเดียวกันพร้อมกัน | — | คนแรกเลื่อนสำเร็จ · คนที่สองได้ **409 ERR_STALE_DATA** → UI ควรแสดง toast error + refresh (dev bind · prototype ยังไม่มี → mark BLOCKED) | ☐ |

#### TC-I02 — ปิด/ยกเลิกอัตราขณะมีผู้สมัครค้าง (EC-08 · AI-DEFAULT) — ⚠ drift DR-01
- group: edge · ความสำคัญ: ต่ำ · trace: EC-08 / OQ-17 / AT-25 · `[AI-DEFAULT]` · actor: recruiter
- Setup: role=recruiter · reload · seed=REQ-2569-0001 (เปิดรับ · มีผู้สมัคร C1..C4 ค้างใน pipeline) · files=— · **(ต้อง simulate/verify drift)** — HTML `reqClose()` ปัจจุบัน **ไม่ warn "มีผู้สมัครค้าง"** (UI_BRIEF DR-01); FRD ตั้ง conservative default ว่าต้อง warn. เคสนี้ตรวจว่า candidate ไม่ถูกยกเลิกอัตโนมัติ + บันทึก drift
- Start: OPEN `#/recruit/req` → เปิด REQ-2569-0001 → ปิดอัตรา
- ผ่านเมื่อ: ปิดอัตราแล้ว **ผู้สมัครใน pipeline ยังอยู่/จัดการต่อได้** (ไม่ถูกยกเลิกอัตโนมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/req` → เปิด **REQ-2569-0001** → CLICK **ปิดอัตรา** → ยืนยัน | — | อัตราปิด · toast "ปิดอัตราแล้ว" · **⚠ DR-01:** prototype ไม่แสดง warn "มีผู้สมัครค้างใน pipeline" (FRD คาดว่าควรมี — บันทึก drift ในผล) | ☐ |
| 2 | OPEN `#/recruit/board` → VERIFY ผู้สมัครที่ผูก REQ-1 | — | ผู้สมัคร (C1..C4) **ยังอยู่ในไปป์ไลน์เดิม ไม่ถูกยกเลิก/ลบอัตโนมัติ** (conservative default ถูกต้อง) | ☐ |

---

### G-X · Cross-module (XT)

#### TC-X01 — hire ยิง event handoff · ไม่สร้าง employee (XT-01)
- group: cross-module · ความสำคัญ: สูง · trace: XT-01 / BR-05 / LOCK-OB1 / OQ-15 · actor: recruiter
- Setup: role=recruiter · reload · seed=C4 อารยา (offer sent) · files=— · **(ปลายทาง On/Offboard = simulate)** — prototype ไม่มีหน้า downstream; verify จาก toast/สถานะฝั่งต้นทาง + audit (fire-and-forget · ฝั่งรับไม่ทดสอบ · OQ-15)
- Start: เปิด C4 → ตอบรับ → hire (เหมือน TC-E06)
- ผ่านเมื่อ: hire → toast "ส่งเข้า onboarding แล้ว" + audit "ยิง event เริ่ม onboarding (soft-linkage)" · **ไม่มีการสร้าง employee record**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด **อารยา** → แท็บ ข้อเสนอ → **ผู้สมัครตอบรับ** → **รับเข้าทำงาน → ส่ง On/Offboard** → **ยืนยันรับเข้าทำงาน** | — | toast "ส่งเข้า onboarding แล้ว" | ☐ |
| 2 | CLICK แท็บ **ประวัติ** ของอารยา | — | มี entry **"รับเข้าทำงาน → ส่งเข้า On/Offboard"** detail "ยิง event เริ่ม onboarding (soft-linkage)" — payload ยิงออก (candidate_id/position/grade/start_date/offer_snapshot) แต่ **ไม่มี employee_id · ไม่สร้าง employee** | ☐ |
| 3 | VERIFY ทั้งแอป | — | ไม่มีเมนู/หน้า/ปุ่ม "สร้างพนักงาน" หรือ employee record ใด ๆ ถูกสร้าง (LOCK-OB1 · ฝั่งรับ = OQ-15 ไม่ทดสอบ) | ☐ |

#### TC-X02 — offer ยึด band freeze snapshot (XT-02 · EC-11)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-02 / EC-11 / BR-09 · actor: recruiter
- Setup: role=recruiter · reload · seed=C5 ณัฐพล (offer accepted · band version_id=**SS-2569-02**, ต่างจาก resolve ปัจจุบัน SS-2569-03) · files=—
- Start: OPEN `#/recruit/pool` → เปิด C5 → แท็บ ข้อเสนอ
- ผ่านเมื่อ: offer เดิมแสดง version_id ที่ freeze ไว้ (SS-2569-02) ไม่ re-resolve เป็นเวอร์ชันปัจจุบัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/pool` → CLICK **ณัฐพล เจริญสุข** → แท็บ **ข้อเสนอ** | — | ข้อเสนอแสดง band **(freeze SS-2569-02)** — เป็นเวอร์ชันที่ freeze ณ สร้าง offer | ☐ |
| 2 | VERIFY เทียบกับ resolve ปัจจุบัน | — | ฟอร์มสร้าง offer ใหม่ (ผู้สมัครอื่น) resolve เป็น **SS-2569-03** แต่ offer เก่าของ C5 **ยังคง SS-2569-02** (ไม่เปลี่ยนตาม band ปัจจุบัน · BR-09 freeze) | ☐ |

#### TC-X03 — NTF ยิงตรง trigger (XT-03)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-03 / FN-07 / OQ-D4 · actor: recruiter
- Setup: role=recruiter · reload · seed=C2 สุพิชญา (ยินยอม) · files=— · **(ENG-NOTIFY = simulate)** — prototype `ntf()` = info toast; verify ว่า event ถูก trigger ณ จุดที่ถูกต้อง
- Start: OPEN `#/recruit/board` / เปิด C2 assess
- ผ่านเมื่อ: ทุก trigger (เลื่อนสถานะ / ส่ง offer / นัดสัมภาษณ์) มี toast info NTF ยิงตาม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` → CLICK **ถัดไป** บนการ์ดสุพิชญา | — | toast info NTF **"แจ้งเตือน: สุพิชญา อินทโชติ → สัมภาษณ์"** (trigger = stage changed) | ☐ |
| 2 | เปิด C2 → assess → นัดสัมภาษณ์ (DS-INTERVIEW) → บันทึก | DS-INTERVIEW | toast info **"แจ้งเตือน: นัดสัมภาษณ์ สุพิชญา อินทโชติ"** ก่อน toast success (trigger = interview scheduled) | ☐ |
| 3 | VERIFY (OQ-D4) | — | NTF ล้มเหลว = queue/retry (หลังบ้าน) — ไม่บล็อก business transition (verify เชิงหลักการ · prototype ไม่มี failure path) | ☐ |

#### TC-X04 — DOA resolve slot runtime · ไม่ hardcode คน (XT-04 · VR-04)
- group: cross-module · ความสำคัญ: สูง · trace: XT-04 / VR-04 / LOCK-OB3 / LOCK-DOA · actor: recruiter
- Setup: role=recruiter · reload · seed=อัตราร่าง (DS-REQ-A) · files=— · **(Policy Center = simulate)** — prototype `doaResolve()` คืน slot เปล่า; verify ว่า slot มาจากการ resolve ไม่ใช่ผู้อนุมัติ hardcode
- Start: ส่งอนุมัติเปิดอัตรา (เหมือน TC-A05)
- ผ่านเมื่อ: DOA modal แสดง slot ว่างให้เลือกคนเอง (ไม่มีชื่อ default) + ไม่มีวงเงิน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างอัตราร่าง (DS-REQ-A) → เปิด → **ส่งอนุมัติเปิด** | DS-REQ-A | modal DOA เปิด · แต่ละ slot combobox **ว่าง** (placeholder "เลือกผู้อนุมัติ...") — **ไม่มีชื่อผู้อนุมัติ hardcode** ล่วงหน้า | ☐ |
| 2 | VERIFY subtitle/note ใน modal | — | subtitle "…DOA entry DOA-REQ-OPEN-001 · **ไม่มีวงเงิน**" + note "สายอนุมัติมาจากระบบ DOA กลาง (F-DLG-001) — เลือก "คน" ในแต่ละ slot ที่ระบบ resolve มาให้" (slot มาจาก resolve runtime · LOCK-DOA ไม่ผูก threshold) | ☐ |

---

### G-N · Negative รวม (ของที่ห้ามมี — บังคับเรนเดอร์จริงแล้ว assert ว่าไม่มี)

> feature นี้ **ไม่มี FN-40** — "ของที่ห้ามมี" คือทางลัดที่ FIX-01/Scope Lock บังคับให้หายไป. ทุกเคสต่อไปนี้ **เรนเดอร์จริงแล้ว assert ว่าไม่มีบนจอ**.

#### TC-N01 — ห้ามเลื่อนสถานะ dir>0 โดยไม่มี consent
- group: negative · ความสำคัญ: สูง · trace: BR-02 / EC-01 / BR_CONSENT_REQUIRED · actor: recruiter
- Setup: role=recruiter · reload · seed=C1 ธนวัฒน์ (ไม่ยินยอม) · files=—
- Start: OPEN `#/recruit/board`
- ผ่านเมื่อ: ไม่มีทางเลื่อน C1 ไปข้างหน้าได้จนกว่าจะยินยอม (ปุ่ม disabled/toast block) — ดู TC-C03

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` → พยายามกด **ถัดไป** บน **ธนวัฒน์** (ไม่ยินยอม) | — | ปุ่ม disabled หรือกดแล้ว toast "ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้" · **ไม่มีทางลัด**ให้ข้าม consent gate | ☐ |

#### TC-N02 — ห้ามข้ามไป hired / ห้ามสร้าง employee ตรง ๆ (FIX-01 · LOCK-OB1)
- group: negative · ความสำคัญ: สูง · trace: EC-05 / BR_HIRE_ROUTE_ONLY / LOCK-OB1 / LD-01 · actor: recruiter
- Setup: role=recruiter · reload · seed=C4 อารยา (offer sent · ยังไม่ accepted) · files=—
- Start: OPEN `#/recruit/board` + ทั่วทั้งแอป
- ผ่านเมื่อ: (1) ไม่มีทาง move-stage เข้า hired โดยไม่ผ่าน offer.accepted (2) ไม่มีปุ่ม/เมนู "สร้างพนักงาน/สร้าง employee"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/recruit/board` → CLICK **ถัดไป** บน **อารยา** (offer sent) | — | toast "ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน" · การ์ดไม่เข้า hired (route เดียว = candHireHandoff หลัง accepted) | ☐ |
| 2 | VERIFY ทั่วแอป (sidebar/หน้า/drawer) | — | **ไม่มี** ปุ่ม/เมนู/action ชื่อ "สร้างพนักงาน" / "สร้าง employee" / "ทำสัญญาจ้าง" — hire = ยิง event เท่านั้น (LOCK-OB1 · unsupported[1]) | ☐ |

#### TC-N03 — ห้ามส่ง offer ก่อนอนุมัติ (BR-04)
- group: negative · ความสำคัญ: สูง · trace: BR-04 / BR_OFFER_NOT_APPROVED · actor: recruiter
- Setup: role=recruiter · seed=ข้อเสนอสถานะ รออนุมัติ (ทำ TC-E01) · files=—
- Start: แท็บ ข้อเสนอ
- ผ่านเมื่อ: สถานะยังไม่ "อนุมัติแล้ว" → ไม่มีปุ่ม "ส่งข้อเสนอให้ผู้สมัคร" — ดู TC-E07

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดข้อเสนอสถานะ **รออนุมัติ** (recruiter) | — | **ไม่มีปุ่ม "ส่งข้อเสนอให้ผู้สมัคร"** — ปุ่มส่งโผล่เฉพาะสถานะ "อนุมัติแล้ว · พร้อมส่ง" (BR-04 gate) | ☐ |

#### TC-N04 — ห้ามประกาศ/เปิดรับก่อนอนุมัติ DOA ครบ (BR-01)
- group: negative · ความสำคัญ: สูง · trace: BR-01 / BR_REQ_NOT_APPROVED · actor: recruiter
- Setup: role=recruiter · reload · seed=อัตราร่าง / pending · files=—
- Start: OPEN `#/recruit/req` → เปิดอัตราร่าง/pending
- ผ่านเมื่อ: อัตราที่ยังไม่ approved → ไม่มีปุ่ม "ประกาศรับ" — ดู TC-A09

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดอัตราสถานะ **ร่าง** → VERIFY footer | — | มีเฉพาะ แก้ไข/ส่งอนุมัติเปิด · **ไม่มีปุ่ม "ประกาศรับ"** | ☐ |
| 2 | เปิดอัตราสถานะ **รออนุมัติเปิด** (persona=recruiter) → VERIFY footer | — | **ไม่มีปุ่ม "ประกาศรับ"** และไม่มีปุ่มอนุมัติ (recruiter ไม่ใช่ผู้อนุมัติ) — ประกาศได้เฉพาะหลังสถานะ "อนุมัติแล้ว" | ☐ |

#### TC-N05 — ไม่มีเลขรันเอกสาร/PDF offer letter (LOCK-DOCCFG)
- group: negative · ความสำคัญ: กลาง · trace: LOCK-DOCCFG / unsupported[4] · actor: recruiter
- Setup: role=recruiter · reload · seed=C4/C5 (มี offer) · files=—
- Start: เปิดผู้สมัครที่มี offer → แท็บ ข้อเสนอ
- ผ่านเมื่อ: ข้อเสนอ **ไม่มี** เลขรันเอกสาร/ปุ่มพิมพ์ PDF/ดาวน์โหลด offer letter (soft-ref รอบนี้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดผู้สมัครที่มีข้อเสนอ → แท็บ **ข้อเสนอ** | — | มี KV เงินเดือน/band/วันเริ่ม + timeline อนุมัติ · **ไม่มี** เลขรันเอกสาร (running number), **ไม่มี** ปุ่ม "พิมพ์ PDF"/"ดาวน์โหลด offer letter" (LOCK-DOCCFG · ไม่มี doccfg/pdfdoc) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `สรรหา.html` ในเบราว์เซอร์ (single-file · ไม่ต้อง server). Boot ลงแท็บ **ตำแหน่งที่เปิด** เสมอ.
2. แต่ละเคสเริ่มด้วย **reload หน้า** (คืน seed) แล้วทำตาม `Setup:` — สลับ persona ที่ **แถบล่างซ้าย** (`เจ้าหน้าที่สรรหา`/`ผู้จัดการสายงาน`/`ผู้ชมทั่วไป`) ก่อนเริ่ม.
3. `OPEN #/...` = แก้ hash แล้วรอ render. Overlay (drawer/modal) **ไม่ผูก route** — refresh ขณะเปิดจะปิด overlay กลับ list.
4. Toast หายเองใน ~2.8s — ใช้ `WAIT จน toast ปรากฏ` ก่อน assert; toast **ปิดเองไม่ได้** (ไม่มีปุ่ม X).
5. เคสที่ mark **(ต้อง simulate)** = ต้องมี backend/2 session/หน้า downstream จริง — ถ้า prototype จับไม่ได้ให้รายงาน `blocked` พร้อม evidence.
6. บันทึกผลแต่ละ step (☐ → ✅/❌) แล้วสรุปตาม schema ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST) | **21 / 21** |
| Acceptance AT (06_TESTS §6.1) | 26 / 26 (AT-01..26 map เข้าเคส) |
| Business rules BR (05_RULES §5.1) | 10 / 10 |
| Validation rules VR | 5 / 5 |
| Edge cases EC | 10 / 12 (ข้าม EC-10, EC-12 — หลังบ้านล้วน) |
| Error codes (UI-observable) | 12 / 18 (6 backend-only ข้าม) |
| Permission cells | 8 / 8 (recruiter/manager/viewer × create/approve/mask/mutation) |
| Cross-Module (XT) | **4 / 4** |
| Scope Lock (LOCK) | **7 / 7** (+ unsupported[1..5] verify absence) |
| Negative "ของที่ห้ามมี" (แทน FN-40) | 5 / 5 (TC-N01..N05) |
| Cross-cutting / states / events | ครบ (pills · empty · audit · NTF · Esc · retention) |

- FN cross-check: **✅ 21/21**
- Cross-Module (XT): **4/4**
- Scope Lock (LOCK): **7/7**
- **Manifest cross-check (FRD §0.12): ✅** — ทุกแถว FN table (21) + Story/Rule/Edge ใน Coverage Manifest มีคู่ใน Ledger

### ข้าม (พร้อมเหตุผล)
- **EC-10** (NTF ยิงล้มเหลว queue/retry) — หลังบ้านล้วน (ENG-NOTIFY) · prototype ไม่มี failure path (OQ-D4). แตะเชิงหลักการใน TC-X03.
- **EC-12** (HM/interviewer ถูกลบจาก Employee Master → ใช้ snapshot) — ต้องลบ record ที่ระบบ Employee Master (นอก prototype) · snapshot logic เป็นหลังบ้าน (BR-09).
- **Error codes backend-only** (ERR_NOT_AUTHENTICATED, ERR_NOT_FOUND, ERR_NOT_IN_SLOT, ERR_DUPLICATE_IDEMPOTENCY_KEY, ERR_INVALID_STATE, BR_DOA_UNRESOLVED, BR_BAND_UNRESOLVED) — prototype in-memory ไม่มี HTTP/async path (UI_BRIEF DR-02/DR-03) · dev ทดสอบเมื่อ bind API จริง.
- **Loading/skeleton/500 retry states** — FRD-only (DR-02) · prototype ไม่มี async · ทดสอบตอนต่อ API.
- **นอกขอบเขตใบเซ็น (Scope Lock Exclusions · ห้ามสร้างเคสทดสอบ):** สร้าง employee/สัญญาจ้าง · job board ภายนอก · assessment engine/sourcing agency · offer letter PDF เลขรัน · CRUD band เงินเดือน — ตรวจเฉพาะ **การไม่มีอยู่** (TC-N02/N05) ไม่ทดสอบเป็นฟีเจอร์.

### ⚠ Drift ที่ต้องรายงานเมื่อรัน
- **DR-01** (TC-I02): `reqClose()` ไม่แสดง warn "มีผู้สมัครค้างใน pipeline" ตามที่ FRD EC-08 ตั้งไว้ — prototype scope · dev เพิ่มตอน bind API-08.
- เคส `[AI-DEFAULT]` (TC-I01/I02 + guard OQ-D1..D4): ผล fail อาจแปลว่า "default ที่ AI ตั้งไว้ผิด" ไม่ใช่ "โค้ดผิด" — ยกให้ BA ทบทวน.

---

## Result Report (schema)

```json
{
  "feature_id": "F-HR-RECRUIT",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-A01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 62, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ toast จริง · route ที่ค้าง · สิ่งที่แสดงแทน Expected). `note` = drift/หมายเหตุ (เช่น "DR-01: ไม่มี warn ผู้สมัครค้าง").
