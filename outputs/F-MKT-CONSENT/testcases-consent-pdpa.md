# AI Test Cases — ความยินยอม PDPA (F-MKT-CONSENT · F058)

เอกสารนี้เขียนสำหรับ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบน `consent-pdpa.html` (prototype) จริง แล้วรายงานผลกลับแบบ machine-readable. ทุก action ผูกกับ **ข้อความ/ป้ายที่เห็นบนจอ** (verbatim จาก HTML) + route จริง (`#/consent/...`) และทุก Expected ตรวจได้ด้วยตา.

> **Consumer = AI** (กลับขั้วจาก qa-friendly) — คงรายละเอียด route/label/toast ที่ agent ใช้นำทาง.
> **Anchor source order:** HTML ต้นทาง (verbatim) > 01_UI > microcopy กลาง html-generator-v9.

## ⚠️ Drift note (HTML ชนะ — FRD กับจอหลุดกันเล็กน้อย ให้คนไป sync)
1. **resolve เลือกไม่ครบ:** จอจริงแสดง toast **"เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสิทธิ์"** (05_RULES/06_TESTS เขียน "…ก่อนตรวจสอบ") → ยึดจอ
2. **สร้างคำขอ purpose ไม่รองรับ:** จอจริง **"เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ"** (05_RULES เขียนย่อ) → ยึดจอ
3. **Customer 360:** ปุ่มบนแถวทะเบียนเขียนว่า **"ดูรายคน"** (01_UI เรียก "Customer 360"/D-c360) → anchor = "ดูรายคน"
4. **role switch:** prototype ใช้ **persona switcher (demo-strip #105)** ปุ่ม `Officer / DPO / Auditor` — ไม่ใช่ login จริง (OQ-05 enforce จริงภายหลัง)

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-MKT-CONSENT (plan F058) |
| ชื่อ | ความยินยอม PDPA (Consent Management) |
| เวอร์ชัน pack | FRD v1.0 (2026-09-13) FULL · BRD APPROVED |
| App entry | เปิด `consent-pdpa.html` → default route `#/consent/registry` |
| Routes | `#/consent/registry` (default) · `#/consent/requests` · `#/consent/purposes` · `#/consent/resolve` · recipient view (full-screen overlay z=--z-recipient เปิดจากปุ่มในคำขอ) |
| ที่มา | FRD Pack (00/01/05/06/07) + BRD_F-MKT-CONSENT.md + consent-pdpa.html (source of truth หน้าจอ · e2e 32/32 · FN 20/20) |
| role switch | persona strip: `Officer` / `DPO` / `Auditor` (มุมบน demo-strip) |
| จำนวนเคส | **68** เคส · 10 group |

## Coverage

| group | เคส | ความสำคัญ |
|---|:--:|---|
| G1 วัตถุประสงค์ (Purposes) | 10 | สูง |
| G2 คำขอ (Requests) | 9 | สูง |
| G3 มุมมองผู้รับ (Recipient sign) | 5 | สูง |
| G4 ทะเบียน/หลักฐาน/ถอน/ต่ออายุ | 12 | สูง |
| G5 Resolve simulator | 8 | สูง |
| G6 FN-40 Negative Locks | 10 | สูง |
| G7 Edge cases + Cross-Module (XT) | 9 | กลาง |
| G8 Permission matrix | 5 | สูง |
| G9 UX / interaction | 4 | กลาง |

---

## Coverage Ledger

### FN บวก (FUNCTION_CHECKLIST · 20 ตัว)
| FN | S / BR | cases |
|---|---|---|
| FN-01 สร้าง purpose + upload v1 | S-01·BR-03/05/11 | TC-PUR-01, TC-PUR-02, TC-PUR-03, TC-PUR-04, TC-PUR-05 |
| FN-02 อัปโหลดเวอร์ชันใหม่ + เตือน stale | S-02·BR-05/06 | TC-PUR-07, TC-PUR-08 |
| FN-03 ตาราง purpose + สถิติ | S-03 | TC-PUR-06 |
| FN-04 ปิด purpose (consent เดิมอยู่) | S-04·BR-14 | TC-PUR-09 |
| FN-05 สร้างคำขอ single-screen | S-05·BR-01/03 | TC-REQ-01, TC-REQ-02, TC-REQ-03, TC-REQ-04 |
| FN-06 ส่งทางอีเมล (mock) | S-06·BR-07 | TC-REQ-05 |
| FN-07 ส่งซ้ำช่องทางอื่น = ส่งครั้งที่ N | S-07·BR-18 | TC-REQ-06 |
| FN-08 คัดลอกลิงก์ / ดาวน์โหลด QR | S-08 | TC-REQ-07, TC-REQ-08 |
| FN-09 ดาวน์โหลดเอกสารของคำขอ | S-09 | TC-REQ-09 |
| FN-10 เซ็นผ่าน recipient view + evidence 5 | S-10·BR-15 | TC-RCP-01, TC-RCP-02, TC-RCP-05 |
| FN-11 ยินยอมรายวัตถุประสงค์ | S-11·BR-01 | TC-RCP-03, TC-RCP-04 |
| FN-12 ดูหลักฐาน 1 รายการ (5 ฟิลด์) | S-12·BR-15 | TC-REG-05 |
| FN-13 ทะเบียน + กรองทุกมิติ | S-13·BR-07 | TC-REG-01, TC-REG-02, TC-REG-03 |
| FN-14 Customer 360 | S-14 | TC-REG-07 |
| FN-15 ถอนแทนลูกค้า (ทันที) | S-15·BR-09/10 | TC-REG-08, TC-REG-09, TC-REG-10 |
| FN-16 ใกล้หมดอายุ ≤30 วัน | S-16·BR-12 | TC-REG-04 |
| FN-17 ต่ออายุ = คำขอใหม่อ้างเดิม | S-17·BR-13 | TC-REG-11 |
| FN-18 ประวัติ append-only | S-18·BR-16 | TC-REG-06 |
| FN-19 resolve simulator | S-19·BR-19/20 | TC-RES-01, TC-RES-03, TC-RES-04, TC-RES-05, TC-RES-06, TC-RES-07 |
| FN-20 never_asked (ไม่ 404/declined) | S-20·BR-04/08/19 | TC-RES-02, TC-RES-08 |

**FN cross-check: ✅ 20/20**

### FN-40 Negative Locks (10 ข้อ — ต้องไม่มี)
| NEG | ต้องไม่มี | LOCK | case |
|---|---|---|---|
| NEG-40.1 | cookie consent บนเว็บ | LOCK-05 | TC-NEG-01 |
| NEG-40.2 | สายอนุมัติก่อนส่งคำขอ | LOCK-04 | TC-NEG-02 |
| NEG-40.3 | ส่งอีเมล/LINE จริง | — | TC-NEG-03 |
| NEG-40.4 | คำนวณมูลค่า/คอลัมน์ผลรายท่อ | LOCK-CSQ-04/05 | TC-NEG-04 |
| NEG-40.5 | การ์ดผล 7 ท่อ CSQ บนจอ | LOCK-CSQ-06 | TC-NEG-05 |
| NEG-40.6 | ประกาศท่อ OC/DC/SC | LOCK-CSQ-01/02/03 | TC-NEG-06, TC-XT-04 |
| NEG-40.7 | ธง opt-out เดียวต่อคน | — | TC-NEG-07 |
| NEG-40.8 | "ไม่ตอบ" = "ไม่ยินยอม" | — | TC-NEG-08, TC-RES-08 |
| NEG-40.9 | บล็อกการส่งเอง (resolve read-only) | — | TC-NEG-09 |
| NEG-40.10 | wizard สร้างคำขอ (stepper 5 ขั้น) | LOCK-07 | TC-NEG-10, TC-REQ-01 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 triple key ไม่ซ้ำ (active รายการเดียว) | TC-RCP-01, TC-REG-01, TC-RES-01 |
| BR-02 ช่องทาง 5 (config) | TC-REQ-04 (verify enum ช่องทาง), TC-PUR-01 |
| BR-03 purpose กำหนดช่องทางเอง (ขอนอกไม่ได้) | TC-REQ-04 |
| BR-04 default-deny (never_asked) | TC-RES-02, TC-XT-02 |
| BR-05 เอกสาร versioned · upload = เวอร์ชันใหม่ | TC-PUR-01, TC-PUR-05, TC-PUR-07, TC-PUR-08 |
| BR-06 consent ผูกเวอร์ชันที่เซ็น (stale) | TC-PUR-07, TC-RES-04 |
| BR-07 5 สถานะ + คำนวณ expired | TC-REG-01, TC-RES-05 |
| BR-08 ไม่ตอบ ≠ ปฏิเสธ | TC-RES-08, TC-NEG-08 |
| BR-09 ถอนทันที ไม่ต้องอนุมัติ | TC-REG-08, TC-NEG-02 |
| BR-10 ถอนต้องมีเหตุผล + ช่องทาง | TC-REG-08, TC-REG-09, TC-REG-10 |
| BR-11 อายุ default 24 (1–120) | TC-PUR-01, TC-PUR-04 |
| BR-12 ใกล้หมดอายุ ≤30 เตือน ไม่บล็อก | TC-REG-04 |
| BR-13 ต่ออายุ = คำขอใหม่อ้างเดิม | TC-REG-11 |
| BR-14 ปิด purpose = ห้ามคำขอใหม่ · consent เดิมอยู่ | TC-PUR-09, TC-REQ-04(purpose closed ไม่ pickable) |
| BR-15 หลักฐานครบ 5 | TC-RCP-01, TC-REG-05 |
| BR-16 ประวัติ append-only | TC-REG-06 |
| BR-17 ไม่มีการลบถาวร | TC-PUR-09, TC-REG-08 |
| BR-18 ส่งซ้ำ = รายการส่ง ไม่สร้างคำขอใหม่ | TC-REQ-06 |
| BR-19 resolve ตอบ 200 เสมอ · never_asked→false | TC-RES-02, TC-RES-07 |
| BR-20 resolve contract lock (ฟิลด์) | TC-RES-07 |
| BR-21 caller cache ≤5 นาที + ล้างเมื่อถอน | TC-XT-03 (ต้อง simulate · OQ-02) |
| BR-22 register Backend Enforcement Gate | TC-XT-05 (ต้อง simulate · OQ-04) |
| BR-CSQ-01 ทุก event ยิง 7C (ไม่เก็บผลรายท่อ) | TC-XT-04, TC-NEG-04 |
| BR-CSQ-02 idempotency_key unique | TC-XT-04, TC-EC-04 |
| BR-CSQ-03 payload mask restricted | TC-XT-04 (ต้อง simulate) |
| BR-CSQ-04 reversal_of ตอนถอน (ไม่ลบผลเดิม) | TC-XT-04, TC-REG-08 |
| BR-CSQ-05 ไม่ประกาศ/คำนวณ OC/DC/SC | TC-NEG-06, TC-XT-04 |

### Edge Cases (05_RULES §5.5)
| EC | case / สถานะ |
|---|---|
| EC-01 never_asked | TC-RES-02 |
| EC-02 ถอน↔resolve race + caller cache `[AI-DEFAULT]` | TC-XT-03 (ต้อง simulate) |
| EC-03 version stale | TC-RES-04, TC-PUR-07 |
| EC-04 double-submit / idempotency `[AI-DEFAULT]` | TC-EC-04 (ต้อง simulate — API header) |
| EC-05 lapsed ≠ declined | TC-RES-08 |
| EC-06 ยินยอมบางข้อ | TC-RCP-04 |
| EC-07 ปิด purpose → consent เดิมอยู่ | TC-PUR-09 |
| EC-08 withdraw = compensation (reversal_of) | TC-REG-08, TC-XT-04 |
| EC-09 upload ชนิด/ขนาด `[AI-DEFAULT]` | TC-EC-09 (partial — mock ไม่ validate size · OQ-07) |
| EC-10 timezone expires_at `[AI-DEFAULT]` | TC-EC-10 (ต้อง simulate · OQ-08) |
| EC-11 optimistic lock (2 dpo) | TC-EC-11 (ต้อง simulate — API 409) |

### Error Catalog (05_RULES §5.6)
| error | case |
|---|---|
| BR_DOCUMENT_REQUIRED (422) | TC-PUR-05, TC-PUR-08 |
| BR_CHANNEL_NOT_SUPPORTED (422) | TC-REQ-04 |
| BR_PURPOSE_CLOSED (422) | TC-PUR-09 (verify closed → ขอใหม่ไม่ได้) |
| BR_IDENTITY_NOT_VERIFIED (422) | TC-RCP-02 |
| BR_ANSWERS_INCOMPLETE (422) | TC-RCP-03 |
| BR_WITHDRAW_REASON_REQUIRED (422) | TC-REG-09 |
| BR_WITHDRAW_CHANNEL_REQUIRED (422) | TC-REG-10 |
| ERR_VALIDATION_FAILED (400) | TC-PUR-02/03/04, TC-REQ-02/03, TC-RES-06 |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / CSQ_ERR_DUPLICATE_ENVELOPE | TC-EC-04 (ต้อง simulate) |
| ERR_STALE_DATA (409) | TC-EC-11 (ต้อง simulate) |
| ERR_INSUFFICIENT_ROLE (403) | TC-PERM-01, TC-PERM-04 (UI: ปุ่มหาย/chip — enforce จริง OQ-05) |
| resolve = ไม่มี error business (200 เสมอ) | TC-RES-02, TC-RES-07, TC-NEG-09 |

### Field Validation (05_RULES §5.4)
| field/action | cases |
|---|---|
| สร้าง purpose: name required | TC-PUR-02 |
| สร้าง purpose: ≥1 channel | TC-PUR-03 |
| สร้าง purpose: life 1–120 (boundary) | TC-PUR-04 |
| สร้าง purpose: แนบเอกสาร | TC-PUR-05 |
| ออกเวอร์ชัน: แนบเอกสาร | TC-PUR-08 |
| recipient: verified ก่อนส่ง | TC-RCP-02 |
| recipient: ตอบครบทุก purpose | TC-RCP-03 |
| ถอน: เหตุผล + ช่องทาง | TC-REG-09, TC-REG-10 |
| สร้างคำขอ: subject/channel/purpose รองรับ | TC-REQ-02/03/04 |
| resolve: ครบ 3 ช่อง | TC-RES-06 |

### Permission Matrix (05_RULES §5.3 — HTML `PERM()` persona)
| cell | case |
|---|---|
| officer สร้าง/แก้ purpose = deny (read + chip) | TC-PERM-01 |
| officer สร้างคำขอ/ถอน/resolve = allow | TC-PERM-02 |
| dpo purpose CRUD + ปิด + upload = allow | TC-PERM-03 |
| auditor สร้างคำขอ/ถอน/purpose = deny (ปุ่มหาย) | TC-PERM-04 |
| auditor ดูทะเบียน/หลักฐาน + resolve(read) = allow | TC-PERM-05 |

### Cross-Module (06_TESTS §6.9 — XT)
| XT | Downstream | case |
|---|---|---|
| XT-01 resolve granted → ส่งได้ | แคมเปญ | TC-XT-01 |
| XT-02 resolve never_asked/withdrawn/expired → ไม่ส่ง (default-deny) | แคมเปญ | TC-XT-02 |
| XT-03 ถอน → caller cache invalidation ≤5 นาที | caller | TC-XT-03 (ต้อง simulate) |
| XT-04 state change → CSQ envelope ถูก (idempotency/reversal · ไม่มี OC/DC/SC) | 7C | TC-XT-04 (ต้อง simulate) |
| XT-05 register `/consent/*` Enforcement Gate | F143 | TC-XT-05 (ต้อง simulate) |

### Scope Lock (07_LOCKED §7.0 — ทุกข้อต้องมีเคส verify)
| LOCK | ข้อยืนยัน (ย่อ) | case verify |
|---|---|---|
| LOCK-04 | ไม่มีสายอนุมัติ · ถอนทันที | TC-NEG-02, TC-REG-08 |
| LOCK-05 | ไม่ทำ cookie consent | TC-NEG-01 |
| LOCK-07 | สร้างคำขอ single-screen | TC-NEG-10, TC-REQ-01 |
| LOCK-CSQ-01/02/03 | ไม่ประกาศ OC/DC/SC | TC-NEG-06, TC-XT-04 |
| LOCK-CSQ-04 | ไม่คำนวณมูลค่า | TC-NEG-04 |
| LOCK-CSQ-05 | ไม่มีคอลัมน์ผลรายท่อ | TC-NEG-04 |
| LOCK-CSQ-06 | ไม่วาดการ์ด 7 ท่อบนจอ | TC-NEG-05 |
| lock#7 | triple (ไม่ใช่ธงเดียว) | TC-NEG-07 |
| lock#8 | "ไม่ตอบ" ≠ "ไม่ยินยอม" | TC-NEG-08, TC-RES-08 |
| lock#9 | resolve ตอบอย่างเดียว (ไม่ส่งเอง) | TC-NEG-09 |
| lock#3 | ไม่ส่งอีเมล/LINE จริง (mock toast) | TC-NEG-03, TC-REQ-05 |

### Cross-cutting / Events / States / UI states
| item | case |
|---|---|
| Empty state ทะเบียน (filtered-empty) | TC-REG-03 |
| Stat cards toggle filter | TC-REG-04 |
| DSP-01 document viewer เหนือ drawer (z-pop) | TC-PUR-10 |
| Esc chain / 3-way close overlay | TC-UX-02 |
| Tab navigation 4 แท็บ + default route | TC-UX-01 |
| CSV export (client-side utility) | TC-REG-12 |
| decorativeNav toast (โมดูลอื่น) | TC-UX-03 |
| toast auto-dismiss | TC-UX-04 |
| event consent.granted/withdrawn/... → CSQ | TC-XT-04 (envelope) |

### ข้าม (นอก scope / ไม่มีผลบน UI)
- **ทั้ง Out-of-Scope 10 Locks** = ห้ามสร้างเคส "ทำได้" — verify **ไม่มี** แทน (TC-NEG-01..10) ✅ ครบ
- **sort คอลัมน์** — ไม่มี sortable column ใน registry table (observed) → ไม่มีเคส
- **pagination** — prototype seed ไม่ถึง 1 หน้า → ไม่มีเคส (Phase: จริงต้องมี · ปัจจุบันไม่สังเกตบน UI)
- **D7 encryption-at-rest / RLS multi-tenant** — backend-only, single-user demo → ข้าม (05_RULES §5.7 · ไม่มีผลบน prototype UI)

---

## Data Sets

> prototype `consent-pdpa.html` มี **seed ในตัว** (subjects CUS-1001..1008 · purposes PUR-01..04 · consents CNS-5001..5009 · requests REQ-2601..2604). Setup ของแต่ละเคสอ้าง seed ที่มีอยู่แล้วนี้.

### Seed reference (มีในตัว prototype)
| ชนิด | id | รายละเอียด (สำหรับ assert) |
|---|---|---|
| subject | CUS-1001 | นายสมชาย รักดี (บจก. สยามเทรด) |
| subject | CUS-1002 | นางสาวมาลี ศรีสุข |
| subject | CUS-1004 | นายวิชัย ตั้งใจ |
| subject | CUS-1008 | นายกิตติ วัฒนา (ไม่มี consent record) |
| purpose | PUR-01 | ส่งโปรโมชันสินค้า · ช่องทาง email/sms/line · อายุ 24 ด. · **currentVer=2** |
| purpose | PUR-02 | แจ้งข่าวสารและกิจกรรม · email/line/post · v1 |
| purpose | PUR-03 | สำรวจความพึงพอใจทางโทรศัพท์ · phone · v1 |
| purpose | PUR-04 | ส่งใบเสร็จอิเล็กทรอนิกส์ · email · **status=closed** |
| consent | CNS-5001 | CUS-1001×PUR-01×email · **granted v2 · ยังไม่หมดอายุ** (resolve→ส่งได้) |
| consent | CNS-5002 | CUS-1001×PUR-01×sms · granted **v1 (stale)** (resolve→ส่งไม่ได้ stale) |
| consent | CNS-5003 | CUS-1002×PUR-02×email · granted · **ใกล้หมดอายุ ~20 วัน** |
| consent | CNS-5004 | CUS-1002×PUR-01×line · **withdrawn** |
| consent | CNS-5006 | CUS-1004×PUR-03×phone · **declined** |
| consent | CNS-5007 | CUS-1004×PUR-01×email · granted **หมดอายุแล้ว (expired)** |
| consent | CNS-5008 | CUS-1005×PUR-02×post · granted · **ใกล้หมดอายุ ~10 วัน** |
| request | REQ-2601 | CUS-1007 · PUR-01+PUR-02 · email · **pending** (มีลิงก์ · ใช้ทดสอบ recipient/ส่งซ้ำ) |
| request | REQ-2602 | CUS-1008 · PUR-01 · line · **draft** |

### ชุด A — สร้าง purpose (ถูก)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อวัตถุประสงค์ | ทดสอบส่งข้อเสนอสมาชิก |
| ช่องทาง | email, line (ติ๊ก ≥1) |
| อายุ (เดือน) | 24 |
| แนบเอกสาร | `policy-test-v1.pdf` |

### ชุด A-bad — สร้าง purpose (ผิด สำหรับ negative)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อ (เว้นว่าง) | (ปล่อยว่าง) |
| อายุนอกช่วง | 0 หรือ 121 |

### ชุด B — สร้างคำขอ (ถูก)
| ฟิลด์ | ค่า |
|---|---|
| เจ้าของข้อมูล | CUS-1003 (บริษัท กรีนฟู้ด จำกัด) |
| ช่องทาง | email |
| วัตถุประสงค์ | PUR-02 (แจ้งข่าวสารและกิจกรรม · รองรับ email) |

### ชุด C — resolve (ตรวจสิทธิ์)
| กรณี | subject | purpose | channel | ผลคาด |
|---|---|---|---|---|
| granted | CUS-1001 | ส่งโปรโมชันสินค้า (PUR-01) | email | ส่งได้ |
| stale | CUS-1001 | ส่งโปรโมชันสินค้า (PUR-01) | sms | ส่งไม่ได้ (เวอร์ชันเก่า) |
| withdrawn | CUS-1002 | ส่งโปรโมชันสินค้า (PUR-01) | line | ส่งไม่ได้ (ถอนแล้ว) |
| expired | CUS-1004 | ส่งโปรโมชันสินค้า (PUR-01) | email | ส่งไม่ได้ (หมดอายุ) |
| never_asked | CUS-1008 | สำรวจความพึงพอใจฯ (PUR-03) | phone | ส่งไม่ได้ (never_asked) |

### ไฟล์ทดสอบ (Files)
| ชื่อไฟล์ | ใช้ที่ | หมายเหตุ |
|---|---|---|
| `policy-test-v1.pdf` | TC-PUR-01 / TC-PUR-05(ตรงข้าม) | เอกสาร PDPA v1 (.pdf) |
| `policy-test-v2.pdf` | TC-PUR-07 | เอกสารเวอร์ชันใหม่ |
| `too_large.pdf` | TC-EC-09 | ไฟล์เกินขนาด (mock ไม่ validate → OQ-07) |
| `bad_type.exe` | TC-EC-09 | ชนิดนอก `.pdf/.doc/.docx/.txt` |

> prototype อัปโหลดเป็น mock (file picker) — runner ต้องเตรียมไฟล์ชื่อตามนี้ให้ file input.

---

## Test Cases

## G1 — วัตถุประสงค์ (Purposes)

### TC-PUR-01 — สร้างวัตถุประสงค์ครบ + แนบเอกสาร v1 (happy)
- group: วัตถุประสงค์ · ความสำคัญ: สูง · trace: FN-01 / AT-01 / BR-03,05,11
- actor (role): DPO
- Setup: role=dpo (คลิก persona "DPO") · seed=prototype default · files=`policy-test-v1.pdf`
- Start: OPEN `#/consent/purposes`
- ชุดข้อมูล: A
- ผ่านเมื่อ: drawer ปิด + toast **"สร้างวัตถุประสงค์ PUR-0x แล้ว"** + เด้งไปแท็บวัตถุประสงค์ เห็นแถวใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **DPO** (demo-strip มุมบน) | — | โหมด DPO (มีปุ่มสร้างวัตถุประสงค์) | ☐ |
| 2 | OPEN `#/consent/purposes` | — | แท็บ **วัตถุประสงค์** active + ปุ่ม **"สร้างวัตถุประสงค์"** | ☐ |
| 3 | CLICK ปุ่ม **"สร้างวัตถุประสงค์"** | — | drawer เปิด หัวข้อ **"วัตถุประสงค์ใหม่"** + บล็อกแนบเอกสาร | ☐ |
| 4 | TYPE → ช่อง **ชื่อวัตถุประสงค์** | A: ทดสอบส่งข้อเสนอสมาชิก | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | TOGGLE ช่องทาง **email** และ **line** | A | 2 ช่องทางถูกเลือก | ☐ |
| 6 | TYPE → ช่อง **อายุ (เดือน)** | A: 24 | ช่องแสดง 24 | ☐ |
| 7 | UPLOAD `policy-test-v1.pdf` → บล็อกแนบเอกสาร | A | เห็นชื่อไฟล์ที่แนบ | ☐ |
| 8 | CLICK ปุ่ม **"สร้างวัตถุประสงค์"** (ใน drawer) | — | drawer ปิด + toast success **"สร้างวัตถุประสงค์ PUR-0x แล้ว"** + route = `#/consent/purposes` | ☐ |
| 9 | VERIFY ตารางวัตถุประสงค์ | — | เห็นแถวใหม่ชื่อ "ทดสอบส่งข้อเสนอสมาชิก" + ป้ายเวอร์ชัน **v1** | ☐ |

### TC-PUR-02 — สร้าง purpose ไม่กรอกชื่อ (negative: required)
- group: วัตถุประสงค์ · ความสำคัญ: กลาง · trace: FN-01 / validation / ERR_VALIDATION_FAILED
- actor: DPO · Setup: role=dpo · seed=default · files=—
- Start: OPEN `#/consent/purposes` → CLICK **"สร้างวัตถุประสงค์"**
- ผ่านเมื่อ: toast warning **"กรอกชื่อวัตถุประสงค์"** + drawer ยังเปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **DPO** → OPEN `#/consent/purposes` → CLICK **"สร้างวัตถุประสงค์"** | — | drawer เปิด | ☐ |
| 2 | (เว้นช่องชื่อว่าง) CLICK ปุ่ม **"สร้างวัตถุประสงค์"** | A-bad | toast warning **"กรอกชื่อวัตถุประสงค์"** · drawer ยังเปิด · ไม่มีแถวใหม่ | ☐ |

### TC-PUR-03 — สร้าง purpose ไม่เลือกช่องทาง (negative)
- group: วัตถุประสงค์ · ความสำคัญ: กลาง · trace: FN-01 / validation ≥1 channel
- actor: DPO · Setup: role=dpo · seed=default · files=—
- Start: drawer สร้างวัตถุประสงค์
- ผ่านเมื่อ: toast warning **"เลือกช่องทางอย่างน้อย 1"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer สร้างวัตถุประสงค์ | — | drawer เปิด | ☐ |
| 2 | TYPE ช่องชื่อ = "ทดสอบ" (ไม่ติ๊กช่องทางใด) | — | ชื่อกรอกแล้ว · ช่องทางว่าง | ☐ |
| 3 | CLICK **"สร้างวัตถุประสงค์"** | — | toast warning **"เลือกช่องทางอย่างน้อย 1"** | ☐ |

### TC-PUR-04 — สร้าง purpose อายุนอกช่วง 1–120 (boundary/negative)
- group: วัตถุประสงค์ · ความสำคัญ: กลาง · trace: FN-01 / BR-11 boundary
- actor: DPO · Setup: role=dpo · seed=default · files=—
- Start: drawer สร้างวัตถุประสงค์
- ผ่านเมื่อ: toast warning **"อายุต้องอยู่ระหว่าง 1–120 เดือน"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer · TYPE ชื่อ + TOGGLE email | — | ชื่อ+ช่องทาง valid | ☐ |
| 2 | TYPE ช่อง **อายุ** = 121 (เกิน max) | A-bad: 121 | ช่องแสดง 121 | ☐ |
| 3 | CLICK **"สร้างวัตถุประสงค์"** | — | toast warning **"อายุต้องอยู่ระหว่าง 1–120 เดือน"** | ☐ |
| 4 | TYPE ช่อง **อายุ** = 0 (ต่ำกว่า min) → CLICK สร้าง | A-bad: 0 | toast warning เดิม (ยังบล็อก) | ☐ |

### TC-PUR-05 — สร้าง purpose ไม่แนบเอกสาร (negative: BR_DOCUMENT_REQUIRED)
- group: วัตถุประสงค์ · ความสำคัญ: สูง · trace: FN-01 / BR-05 / BR_DOCUMENT_REQUIRED
- actor: DPO · Setup: role=dpo · seed=default · files=—
- Start: drawer สร้างวัตถุประสงค์
- ผ่านเมื่อ: toast warning **"ต้องแนบเอกสาร PDPA"** (บังคับแนบตามโมเดล upload DECLARED-01)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer · TYPE ชื่อ + TOGGLE email + TYPE อายุ 24 (ไม่แนบไฟล์) | A (ยกเว้นไฟล์) | ทุกช่อง valid ยกเว้นเอกสาร | ☐ |
| 2 | CLICK **"สร้างวัตถุประสงค์"** | — | toast warning **"ต้องแนบเอกสาร PDPA"** · ไม่บันทึก | ☐ |

### TC-PUR-06 — ตารางวัตถุประสงค์ + สถิติ (VERIFY)
- group: วัตถุประสงค์ · ความสำคัญ: กลาง · trace: FN-03 / AT-03
- actor: DPO/officer · Setup: role=dpo · seed=default (PUR-01..04) · files=—
- Start: OPEN `#/consent/purposes`
- ผ่านเมื่อ: เห็นทุก purpose พร้อมสถิติ (ยินยอม/ถอน/หมดอายุ/%ครอบคลุม) ต่อแถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/purposes` | — | ตารางวัตถุประสงค์แสดง PUR-01..04 | ☐ |
| 2 | VERIFY แถว **PUR-01 ส่งโปรโมชันสินค้า** | — | เห็นป้าย **v2** + สถิติต่อ purpose + ป้าย "N รายการผูกเวอร์ชันเก่า" (มี stale) | ☐ |
| 3 | VERIFY แถว **PUR-04** | — | ป้ายสถานะ **ปิด/closed** (ปิดใช้งาน) | ☐ |
| 4 | VERIFY footer ตาราง | — | ข้อความ "4 วัตถุประสงค์" | ☐ |

### TC-PUR-07 — ออกเวอร์ชันเอกสารใหม่ → v+1 + เตือน stale N (FN-02)
- group: วัตถุประสงค์ · ความสำคัญ: สูง · trace: FN-02 / AT-02 / BR-05,06 / EC-03 / event policy.version_published
- actor: DPO · Setup: role=dpo · seed=PUR-01 (currentVer=2 · มี consent v1 stale) · files=`policy-test-v2.pdf`
- Start: OPEN `#/consent/purposes` → CLICK แถว **PUR-01** → เปิด purView drawer
- ผ่านเมื่อ: toast **"ออกเอกสาร vN แล้ว · M รายการต้องขอความยินยอมใหม่"** + currentVer เพิ่ม 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/purposes` → CLICK แถว **PUR-01** | — | drawer รายละเอียด + รายการเวอร์ชัน (v1, v2) | ☐ |
| 2 | VERIFY+บันทึก **currentVer ปัจจุบัน** ของ PUR-01 | — | จดค่า = v2 (อ้างใน step 5) | ☐ |
| 3 | CLICK ปุ่ม **"ออกเวอร์ชันใหม่"** | — | modal ออกเวอร์ชันใหม่ (z สูงกว่า drawer) + คำเตือน "ความยินยอม N รายการจะไม่ครอบคลุมเวอร์ชันใหม่" | ☐ |
| 4 | UPLOAD `policy-test-v2.pdf` → CLICK ยืนยันออกเวอร์ชัน | `policy-test-v2.pdf` | modal ปิด + toast success **"ออกเอกสาร v3 แล้ว · M รายการต้องขอความยินยอมใหม่"** | ☐ |
| 5 | VERIFY แถว PUR-01 อีกครั้ง | — | ป้ายเวอร์ชัน = **v3** (เพิ่ม 1 จากค่าที่จด step 2) | ☐ |

### TC-PUR-08 — ออกเวอร์ชันใหม่ ไม่แนบเอกสาร (negative)
- group: วัตถุประสงค์ · ความสำคัญ: กลาง · trace: FN-02 / BR-05 / BR_DOCUMENT_REQUIRED
- actor: DPO · Setup: role=dpo · seed=PUR-01 · files=—
- Start: purView PUR-01 → modal ออกเวอร์ชันใหม่
- ผ่านเมื่อ: toast warning **"ต้องแนบเอกสาร PDPA"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/purposes` → CLICK PUR-01 → CLICK **"ออกเวอร์ชันใหม่"** | — | modal เปิด | ☐ |
| 2 | (ไม่แนบไฟล์) CLICK ยืนยันออกเวอร์ชัน | — | toast warning **"ต้องแนบเอกสาร PDPA"** · เวอร์ชันไม่เพิ่ม | ☐ |

### TC-PUR-09 — ปิดวัตถุประสงค์ → closed + consent เดิมอยู่ (FN-04 · EC-07)
- group: วัตถุประสงค์ · ความสำคัญ: สูง · trace: FN-04 / AT-04 / BR-14,17 / EC-07 / BR_PURPOSE_CLOSED
- actor: DPO · Setup: role=dpo · seed=PUR-02 (active มี consent granted) · files=—
- Start: OPEN `#/consent/purposes` → CLICK แถว **PUR-02**
- ผ่านเมื่อ: toast **"ปิดวัตถุประสงค์ PUR-0x แล้ว"** + สถานะ closed + consent เดิมยังเห็นในทะเบียน + ขอใหม่ไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/purposes` → CLICK แถว **PUR-02** | — | drawer รายละเอียด PUR-02 (active) | ☐ |
| 2 | CLICK ปุ่ม **"ปิดวัตถุประสงค์"** | — | modal confirm ปิด | ☐ |
| 3 | CLICK ยืนยันปิด | — | toast **"ปิดวัตถุประสงค์ PUR-02 แล้ว"** · แถว PUR-02 = closed | ☐ |
| 4 | OPEN `#/consent/registry` → กรอง/ค้นหา consent ของ PUR-02 | — | consent เดิม (เช่น CNS-5003/5005/5008) **ยังอยู่** เป็นหลักฐาน (ไม่ถูกลบ · BR-17) | ☐ |
| 5 | OPEN `#/consent/requests` → CLICK **"สร้างคำขอ"** → เลือก subject + email | — | PUR-02 (closed) **ไม่ปรากฏ**ให้เลือก (ขอใหม่กับ purpose closed ไม่ได้ · BR-14) | ☐ |

### TC-PUR-10 — เปิด document viewer (DSP-01 · modal เหนือ drawer)
- group: วัตถุประสงค์ · ความสำคัญ: กลาง · trace: FN-03 / DSP-01 z=--z-pop (behavioral contract) · `.doc-link`
- actor: DPO · Setup: role=dpo · seed=PUR-01 (มีเอกสาร) · files=—
- Start: OPEN `#/consent/purposes` → CLICK แถว **PUR-01**
- ผ่านเมื่อ: คลิกชื่อเอกสาร → modal เนื้อเอกสารลอย **เหนือ** drawer (ไม่ถูก drawer บัง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/purposes` → CLICK แถว **PUR-01** | — | drawer เปิด เห็นรายการเวอร์ชัน + ชื่อเอกสาร (`นโยบาย-PUR-01-v2.pdf`) เป็นลิงก์ | ☐ |
| 2 | CLICK ชื่อเอกสาร **"นโยบาย-PUR-01-v2.pdf"** (`.doc-link`) | — | modal document viewer เปิด **ทับ/เหนือ drawer** เห็นเนื้อเอกสาร (`.doc-frame`) ครบ ไม่โดน drawer บัง (DSP-01) | ☐ |
| 3 | PRESS Esc | — | ปิด modal เอกสารก่อน (กลับมาเห็น drawer — Esc chain) | ☐ |

## G2 — คำขอ (Requests)

### TC-REQ-01 — สร้างคำขอ single-screen (happy · LOCK-07)
- group: คำขอ · ความสำคัญ: สูง · trace: FN-05 / AT-05 / BR-01,03 / LOCK-07 (single-screen)
- actor: officer · Setup: role=officer (persona "Officer") · seed=default · files=—
- Start: OPEN `#/consent/requests` → CLICK **"สร้างคำขอ"**
- ชุดข้อมูล: B
- ผ่านเมื่อ: toast **"สร้างคำขอ REQ-xxxx พร้อมลิงก์และ QR แล้ว"** + คำขอครบในจอเดียว (ไม่มี stepper)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **Officer** → OPEN `#/consent/requests` | — | แท็บ **คำขอ** active + ปุ่ม **"สร้างคำขอ"** | ☐ |
| 2 | CLICK ปุ่ม **"สร้างคำขอ"** | — | drawer **"คำขอความยินยอมใหม่"** เปิด — **จอเดียว** (เลือก subject + ช่องทาง + วัตถุประสงค์พร้อมกัน · ไม่มี tab/stepper 5 ขั้น) | ☐ |
| 3 | SELECT เจ้าของข้อมูล = **CUS-1003 (บริษัท กรีนฟู้ด จำกัด)** | B | ช่องเจ้าของข้อมูลแสดงค่าที่เลือก | ☐ |
| 4 | SELECT ช่องทาง = **email** | B | ช่องทาง = email | ☐ |
| 5 | TOGGLE วัตถุประสงค์ **PUR-02 (แจ้งข่าวสารและกิจกรรม)** | B | PUR-02 ถูกเลือก (รองรับ email) | ☐ |
| 6 | CLICK ปุ่ม **"สร้างคำขอ + ลิงก์/QR"** | — | drawer ปิด + toast **"สร้างคำขอ REQ-xxxx พร้อมลิงก์และ QR แล้ว"** + route = `#/consent/requests` | ☐ |
| 7 | VERIFY ตารางคำขอ | — | เห็นคำขอใหม่ของ CUS-1003 | ☐ |

### TC-REQ-02 — สร้างคำขอ ไม่เลือกเจ้าของข้อมูล (negative)
- group: คำขอ · ความสำคัญ: กลาง · trace: FN-05 / validation
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: drawer สร้างคำขอ
- ผ่านเมื่อ: toast warning **"เลือกเจ้าของข้อมูลก่อน"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK **"สร้างคำขอ"** | — | drawer เปิด | ☐ |
| 2 | (ไม่เลือก subject) CLICK **"สร้างคำขอ + ลิงก์/QR"** | — | toast warning **"เลือกเจ้าของข้อมูลก่อน"** | ☐ |

### TC-REQ-03 — สร้างคำขอ ไม่เลือกช่องทาง (negative)
- group: คำขอ · ความสำคัญ: กลาง · trace: FN-05 / validation
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: drawer สร้างคำขอ
- ผ่านเมื่อ: toast warning **"เลือกช่องทางก่อน"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer สร้างคำขอ · SELECT subject = CUS-1003 (ไม่เลือกช่องทาง) | — | subject เลือกแล้ว · ช่องทางว่าง | ☐ |
| 2 | CLICK **"สร้างคำขอ + ลิงก์/QR"** | — | toast warning **"เลือกช่องทางก่อน"** | ☐ |

### TC-REQ-04 — สร้างคำขอ ไม่เลือก purpose ที่รองรับช่องทาง (negative · BR-03)
- group: คำขอ · ความสำคัญ: สูง · trace: FN-05 / BR-03 / BR_CHANNEL_NOT_SUPPORTED
- actor: officer · Setup: role=officer · seed=default (PUR-03 รองรับเฉพาะ phone) · files=—
- Start: drawer สร้างคำขอ
- ผ่านเมื่อ: toast warning **"เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ"** + PUR ที่ไม่รองรับช่องทางแสดงเป็นเลือกไม่ได้/แจ้ง "ไม่รองรับช่องทางที่เลือก"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer สร้างคำขอ · SELECT subject = CUS-1003 · SELECT ช่องทาง = **email** | — | subject+ช่องทางเลือกแล้ว | ☐ |
| 2 | VERIFY รายการวัตถุประสงค์ | — | **PUR-03 (phone)** แสดงเป็น **"— ไม่รองรับช่องทางที่เลือก"** (เลือกไม่ได้) | ☐ |
| 3 | (ไม่ติ๊ก purpose ใด) CLICK **"สร้างคำขอ + ลิงก์/QR"** | — | toast warning **"เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ"** | ☐ |

### TC-REQ-05 — ส่งคำขอทางอีเมล → pending (mock · ไม่ส่งจริง)
- group: คำขอ · ความสำคัญ: สูง · trace: FN-06 / AT-06 / BR-07 / lock#3
- actor: officer · Setup: role=officer · seed=REQ-2602 (draft, CUS-1008, line) หรือคำขอที่เพิ่งสร้าง · files=—
- Start: OPEN `#/consent/requests` → CLICK แถวคำขอ draft
- ผ่านเมื่อ: toast **"บันทึกการส่งทาง&lt;ช่องทาง&gt; (จำลอง — ไม่ส่งจริง)"** + สถานะ → รอตอบ (pending)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK แถว **REQ-2602** (draft) | — | drawer รายละเอียดคำขอ (ลิงก์ + ช่องทางส่ง) | ☐ |
| 2 | CLICK ปุ่มส่งทางช่องทางของคำขอ (เช่น **LINE**) | — | toast success **"บันทึกการส่งทางLINE (จำลอง — ไม่ส่งจริง)"** — ไม่มีการส่งจริง | ☐ |
| 3 | VERIFY สถานะคำขอ | — | ป้ายสถานะ → **รอตอบ** (pending) | ☐ |

### TC-REQ-06 — ส่งซ้ำช่องทางอื่น = ส่งครั้งที่ N (ไม่สร้างคำขอใหม่)
- group: คำขอ · ความสำคัญ: สูง · trace: FN-07 / AT-07 / BR-18
- actor: officer · Setup: role=officer · seed=REQ-2601 (pending · CUS-1007 · มี 1 send email แล้ว) · files=—
- Start: OPEN `#/consent/requests` → CLICK แถว **REQ-2601**
- ผ่านเมื่อ: จำนวน "คำขอ" ใน footer ไม่เพิ่ม + มีรายการส่งครั้งที่ 2 ในคำขอเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → VERIFY+บันทึก footer "N คำขอ" | — | จดจำนวนคำขอฐาน (อ้าง step 4) | ☐ |
| 2 | CLICK แถว **REQ-2601** | — | drawer เห็นประวัติการส่ง (email 1 ครั้ง) | ☐ |
| 3 | SELECT ช่องทางอื่น (เช่น **LINE**) → CLICK ส่งซ้ำ | — | toast **"บันทึกการส่งทางLINE (จำลอง — ไม่ส่งจริง)"** + รายการส่งเพิ่มเป็น 2 ครั้งในคำขอ REQ-2601 เดิม | ☐ |
| 4 | ปิด drawer → VERIFY footer "N คำขอ" | — | จำนวนคำขอ **เท่าเดิม** (ไม่สร้างคำขอใหม่ · BR-18) | ☐ |

### TC-REQ-07 — คัดลอกลิงก์ (FN-08)
- group: คำขอ · ความสำคัญ: กลาง · trace: FN-08 / AT-08
- actor: officer · Setup: role=officer · seed=REQ-2601 · files=—
- Start: OPEN `#/consent/requests` → CLICK แถว REQ-2601
- ผ่านเมื่อ: toast **"คัดลอกลิงก์แล้ว"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK แถว **REQ-2601** | — | drawer เห็นลิงก์คำขอ + ปุ่มคัดลอกลิงก์ | ☐ |
| 2 | CLICK ปุ่ม **คัดลอกลิงก์** | — | toast success **"คัดลอกลิงก์แล้ว"** | ☐ |

### TC-REQ-08 — ดาวน์โหลด QR (FN-08 · log การนำลิงก์ออก)
- group: คำขอ · ความสำคัญ: กลาง · trace: FN-08 / AT-08
- actor: officer · Setup: role=officer · seed=REQ-2601 · files=—
- Start: drawer คำขอ REQ-2601
- ผ่านเมื่อ: toast **"ดาวน์โหลด QR ของ REQ-2601 แล้ว (บันทึกการนำลิงก์ออก)"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK แถว **REQ-2601** | — | drawer เห็นปุ่ม **"ดาวน์โหลด QR"** | ☐ |
| 2 | CLICK ปุ่ม **"ดาวน์โหลด QR"** | — | toast **"ดาวน์โหลด QR ของ REQ-2601 แล้ว (บันทึกการนำลิงก์ออก)"** (หรือ toast error env ถ้าดาวน์โหลดใน sandbox ไม่ได้ — ยังถือว่ามี hook) | ☐ |

### TC-REQ-09 — ดาวน์โหลดเอกสารของคำขอ (เวอร์ชันปัจจุบันของแต่ละ purpose)
- group: คำขอ · ความสำคัญ: กลาง · trace: FN-09 / AT-09
- actor: officer · Setup: role=officer · seed=REQ-2601 (PUR-01+PUR-02) · files=—
- Start: drawer คำขอ REQ-2601
- ผ่านเมื่อ: toast **"ดาวน์โหลดเอกสาร (ต้นแบบ): &lt;ชื่อเอกสาร&gt;"** ระบุเอกสารเวอร์ชันปัจจุบันของแต่ละ purpose

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK แถว **REQ-2601** | — | drawer เห็นปุ่มดาวน์โหลดเอกสาร | ☐ |
| 2 | CLICK ปุ่ม **ดาวน์โหลดเอกสาร** | — | toast **"ดาวน์โหลดเอกสาร (ต้นแบบ): นโยบาย-PUR-01-v2… · นโยบาย-PUR-02-v1…"** (เวอร์ชันปัจจุบันของแต่ละ purpose) | ☐ |

## G3 — มุมมองผู้รับ (Recipient read + sign)

### TC-RCP-01 — เซ็นครบผ่าน recipient view → granted + evidence 5 (FN-10)
- group: มุมมองผู้รับ · ความสำคัญ: สูง · trace: FN-10 / AT-10 / BR-15 / event consent.granted
- actor: เจ้าของข้อมูล (ผ่าน mock link) · Setup: role=officer (เปิดลิงก์จากคำขอ) · seed=REQ-2601 (pending · PUR-01+PUR-02) · files=—
- Start: OPEN `#/consent/requests` → CLICK REQ-2601 → CLICK **"เปิดมุมมองผู้รับ (จำลองลิงก์)"**
- ผ่านเมื่อ: toast **"บันทึกคำตอบแล้ว · ยินยอม N · ปฏิเสธ M (เก็บหลักฐานครบ 5 อย่าง)"** + ทะเบียนมีแถว granted + หลักฐาน 5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK **REQ-2601** → CLICK **"เปิดมุมมองผู้รับ (จำลองลิงก์)"** | — | หน้าเต็มจอ recipient view เปิด (เหนือ ERP shell) · หัวข้อ + รายวัตถุประสงค์ 2 ข้อ | ☐ |
| 2 | CLICK **"อ่านเอกสาร · &lt;docName&gt;"** ของ PUR-01 | — | เนื้อเอกสารของ PUR-01 แสดง | ☐ |
| 3 | CLICK **"ยินยอม"** ของ PUR-01 และ PUR-02 | — | ทั้ง 2 ข้อเลือก "ยินยอม" (is-on) | ☐ |
| 4 | TOGGLE checkbox **"ฉันคือเจ้าของข้อมูลและได้อ่านเอกสารแล้ว"** | — | checkbox verified (is-on) | ☐ |
| 5 | CLICK ปุ่ม **ส่งคำตอบ** | — | toast success **"บันทึกคำตอบแล้ว · ยินยอม 2 · ปฏิเสธ 0 (เก็บหลักฐานครบ 5 อย่าง)"** + ปิด recipient view | ☐ |
| 6 | OPEN `#/consent/registry` → ค้นหา CUS-1007 → CLICK แถว | — | consent ใหม่ pill **ยินยอม** + drawer แสดงหลักฐานครบ 5 (เวลา·ช่องทาง·วิธียืนยันตัวตน·เวอร์ชันนโยบาย·IP/อุปกรณ์) | ☐ |

### TC-RCP-02 — ไม่ยืนยันตัวตนก่อนส่ง (negative · BR_IDENTITY_NOT_VERIFIED)
- group: มุมมองผู้รับ · ความสำคัญ: สูง · trace: FN-10 / AT-10 neg / BR-15
- actor: เจ้าของข้อมูล · Setup: role=officer · seed=REQ-2601 · files=—
- Start: recipient view ของ REQ-2601
- ผ่านเมื่อ: toast warning **"กรุณายืนยันตัวตนก่อนส่งคำตอบ"** + ไม่บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด recipient view REQ-2601 · CLICK **"ยินยอม"** ทั้ง 2 ข้อ (ไม่ติ๊ก verify) | — | เลือกยินยอมแล้ว · verify ยังไม่ติ๊ก | ☐ |
| 2 | CLICK ปุ่ม **ส่งคำตอบ** | — | toast warning **"กรุณายืนยันตัวตนก่อนส่งคำตอบ"** · ไม่มีแถว granted ใหม่ในทะเบียน | ☐ |

### TC-RCP-03 — ตอบไม่ครบทุก purpose (negative · BR_ANSWERS_INCOMPLETE)
- group: มุมมองผู้รับ · ความสำคัญ: สูง · trace: FN-11 / validation ตอบครบ
- actor: เจ้าของข้อมูล · Setup: role=officer · seed=REQ-2601 (2 purpose) · files=—
- Start: recipient view REQ-2601
- ผ่านเมื่อ: toast warning **"กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบทุกวัตถุประสงค์"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด recipient view REQ-2601 · TOGGLE verify · CLICK **"ยินยอม"** เฉพาะ PUR-01 (เว้น PUR-02) | — | verified + ตอบแค่ 1 ข้อ | ☐ |
| 2 | CLICK ปุ่ม **ส่งคำตอบ** | — | toast warning **"กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบทุกวัตถุประสงค์"** | ☐ |

### TC-RCP-04 — ยินยอมบางข้อ (2 grant + 1 decline) บันทึกแยกข้อ (FN-11 · EC-06)
- group: มุมมองผู้รับ · ความสำคัญ: สูง · trace: FN-11 / AT-11 / EC-06 / BR-01
- actor: เจ้าของข้อมูล · Setup: role=officer · seed=คำขอที่มี ≥3 purpose (ถ้า seed มีไม่ถึง 3 → **สร้างคำขอ 3 purpose ก่อน** เช่น CUS-1003 email + PUR-01,PUR-02 และเพิ่ม 1) · files=—
- Start: recipient view ของคำขอหลาย purpose
- ผ่านเมื่อ: registry บันทึก granted และ declined **แยกรายข้อ** (ไม่ใช่ทั้งก้อน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด recipient view ของคำขอที่มีหลายวัตถุประสงค์ | — | เห็นทุก purpose ให้เลือกแยกข้อ | ☐ |
| 2 | CLICK **"ยินยอม"** 2 ข้อ · CLICK **"ไม่ยินยอม"** 1 ข้อ · TOGGLE verify | — | 2 grant + 1 decline · verified | ☐ |
| 3 | CLICK **ส่งคำตอบ** | — | toast **"บันทึกคำตอบแล้ว · ยินยอม 2 · ปฏิเสธ 1 …"** | ☐ |
| 4 | OPEN `#/consent/registry` → ค้นหา subject นั้น | — | เห็น **แถวแยกต่อ purpose**: 2 แถว pill **ยินยอม** + 1 แถว pill **ไม่ยินยอม** (แยกข้อ ไม่ใช่รวมก้อน) | ☐ |

### TC-RCP-05 — อ่านเอกสารใน recipient view (verify การอ่าน)
- group: มุมมองผู้รับ · ความสำคัญ: กลาง · trace: FN-10 / S-10
- actor: เจ้าของข้อมูล · Setup: role=officer · seed=REQ-2601 · files=—
- Start: recipient view REQ-2601
- ผ่านเมื่อ: กด "อ่านเอกสาร" แล้วเห็นเนื้อนโยบายของ purpose นั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด recipient view REQ-2601 | — | เห็นข้อความนำ "โปรดอ่านเอกสารแต่ละวัตถุประสงค์…" | ☐ |
| 2 | CLICK **"อ่านเอกสาร · &lt;docName&gt;"** ของ PUR-01 | — | เนื้อเอกสารนโยบาย PUR-01 (เวอร์ชันที่ผูกคำขอ) แสดงในหน้า | ☐ |

## G4 — ทะเบียน / หลักฐาน / ถอน / ต่ออายุ

### TC-REG-01 — ทะเบียน + กรองสถานะ (FN-13)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-13 / AT-13 / BR-07
- actor: officer · Setup: role=officer · seed=default (CNS-5001..5009 หลายสถานะ) · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: ตาราง triple แสดง + กรองสถานะแล้วเหลือเฉพาะที่ตรง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` | — | ตาราง triple (เจ้าของ × วัตถุประสงค์ × ช่องทาง + pill สถานะ + วันหมดอายุ) | ☐ |
| 2 | VERIFY+บันทึก จำนวนแถวทั้งหมด | — | จดจำนวนฐาน | ☐ |
| 3 | SELECT ตัวกรองสถานะ = **ถอนแล้ว** | — | เหลือเฉพาะแถว pill **ถอนแล้ว** (เช่น CNS-5004) · น้อยกว่าฐาน | ☐ |
| 4 | SELECT ตัวกรองสถานะ = **ยินยอม** | — | เหลือเฉพาะแถว pill **ยินยอม** | ☐ |

### TC-REG-02 — กรอง channel + purpose + search (FN-13)
- group: ทะเบียน · ความสำคัญ: กลาง · trace: FN-13
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: แต่ละมิติกรองแล้วตารางถูกกรองถูกต้อง + reset คืนทั้งหมด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` · SELECT ตัวกรองช่องทาง = **email** | — | เหลือเฉพาะแถวช่องทาง email | ☐ |
| 2 | SELECT ตัวกรองวัตถุประสงค์ = **ส่งโปรโมชันสินค้า (PUR-01)** | — | เหลือเฉพาะ PUR-01 + email | ☐ |
| 3 | TYPE ช่องค้นหา = "สมชาย" | — | เหลือเฉพาะแถวของ CUS-1001 | ☐ |
| 4 | CLICK ล้างตัวกรอง (reset) | — | ตารางกลับมาแสดงทุกแถว | ☐ |

### TC-REG-03 — filtered-empty state (FN-13 · UI state)
- group: ทะเบียน · ความสำคัญ: กลาง · trace: FN-13 / empty state
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: กรองจนไม่มีผล → เห็น empty state **"ไม่พบความยินยอม"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` · TYPE ช่องค้นหา = "zzzzไม่มีจริง" | — | ตารางว่าง → empty state title **"ไม่พบความยินยอม"** + คำแนะนำ "ลองล้างตัวกรอง…" | ☐ |

### TC-REG-04 — stat card toggle: ใกล้หมดอายุ ≤30 วัน (FN-16 · BR-12)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-16 / AT-16 / BR-12
- actor: officer · Setup: role=officer · seed=CNS-5003(~20วัน) + CNS-5008(~10วัน) near-expiry · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: กด stat card "ใกล้หมดอายุ" → เหลือเฉพาะรายการ daysLeft 0–30 + มี near-tag แสดง (เตือน ไม่บล็อก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` · VERIFY stat cards | — | เห็นการ์ด **"ใกล้หมดอายุ (≤30 วัน)"** พร้อมตัวเลข ≥1 | ☐ |
| 2 | CLICK stat card **"ใกล้หมดอายุ (≤30 วัน)"** | — | ตารางเหลือเฉพาะแถว near-expiry (เช่น CNS-5003, CNS-5008) + near-tag "N วัน" · การ์ด is-on | ☐ |
| 3 | VERIFY แถว near-expiry | — | ยังคลิกเปิด/ใช้งานได้ (เตือน ไม่บล็อก) | ☐ |
| 4 | CLICK stat card เดิมซ้ำ | — | ยกเลิกกรอง (toggle off) กลับมาทั้งหมด | ☐ |

### TC-REG-05 — ดูหลักฐาน 5 อย่าง (FN-12)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-12 / AT-12 / BR-15
- actor: officer/auditor · Setup: role=officer · seed=CNS-5001 (granted มี evidence) · files=—
- Start: OPEN `#/consent/registry` → CLICK แถว granted
- ผ่านเมื่อ: เห็นหลักฐานครบ 5: เวลา · ช่องทาง · วิธียืนยันตัวตน · เวอร์ชันนโยบาย · IP/อุปกรณ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → CLICK แถวของ **CUS-1001 · PUR-01 · email** (granted) | — | drawer รายละเอียดความยินยอม | ☐ |
| 2 | VERIFY บล็อกหลักฐาน | — | เห็นครบ 5 ฟิลด์: เวลาตอบ · ช่องทางคำขอ · **วิธียืนยันตัวตน** · เวอร์ชันนโยบาย · IP/อุปกรณ์ | ☐ |

### TC-REG-06 — ประวัติ timeline append-only (FN-18)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-18 / AT-18 / BR-16
- actor: officer · Setup: role=officer · seed=CNS-5004 (withdrawn — มี history ขอ→ยินยอม→ถอน) · files=—
- Start: OPEN `#/consent/registry` → CLICK แถว withdrawn
- ผ่านเมื่อ: timeline เรียงเวลา + มีเหตุผลทุกครั้ง + เป็น append-only (ถอนแล้วยังเห็นทั้งสาย)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` · SELECT กรองสถานะ **ถอนแล้ว** → CLICK แถว CUS-1002 × PUR-01 × line | — | drawer เห็น timeline | ☐ |
| 2 | VERIFY timeline | — | ลำดับ: ขอ (LINE) → ยินยอม (นโยบาย v2) → **ถอนความยินยอม** พร้อมเหตุผล "ลูกค้าไม่ประสงค์รับข้อความส่งเสริมการขาย" · เรียงเวลา · ไม่มีการลบรายการเดิม | ☐ |

### TC-REG-07 — Customer 360 "ดูรายคน" (FN-14)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-14 / AT-14
- actor: officer · Setup: role=officer · seed=CUS-1002 (มีหลาย consent) · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: กด "ดูรายคน" ของลูกค้า → drawer แสดง consent ทุกอันของคนนั้นในที่เดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → หาแถวของ **CUS-1002** → CLICK ปุ่ม **"ดูรายคน"** (ท้ายแถว) | — | drawer Customer 360 ของ CUS-1002 | ☐ |
| 2 | VERIFY เนื้อหา drawer | — | เห็น consent ทั้งหมดของ CUS-1002 (PUR-02 granted + PUR-01 withdrawn) รวมในที่เดียว | ☐ |

### TC-REG-08 — ถอนแทนลูกค้า (happy · ทันที ไม่อนุมัติ · FN-15)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-15 / AT-15 / BR-09,10,17 / EC-08 / LOCK-04
- actor: officer · Setup: role=officer · seed=CNS-5001 (granted) · files=—
- Start: OPEN `#/consent/registry` → CLICK แถว granted → CLICK "ถอนความยินยอม"
- ผ่านเมื่อ: toast **"ถอนความยินยอมแล้ว — มีผลทันทีในคำขอถัดไป"** + สถานะ → ถอนแล้ว **ทันที** (ไม่มีขั้นอนุมัติ) + record เดิมไม่ถูกลบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → CLICK แถว **CUS-1001 · PUR-01 · email** (granted) | — | drawer รายละเอียด + ปุ่ม **"ถอนความยินยอม"** (สีอันตราย) | ☐ |
| 2 | CLICK ปุ่ม **"ถอนความยินยอม"** | — | modal **"ถอนความยินยอมแทนลูกค้า"** subtitle "มีผลทันที ไม่ต้องผ่านการอนุมัติ (BR-09)" — **ไม่มีปุ่ม/ขั้นอนุมัติ** | ☐ |
| 3 | TYPE ช่องเหตุผล = "ลูกค้าแจ้งขอถอนทางโทรศัพท์" · SELECT ช่องทางที่ลูกค้าแจ้ง = phone | — | ช่องกรอกครบ | ☐ |
| 4 | CLICK ยืนยันถอน | — | modal ปิด + toast **"ถอนความยินยอมแล้ว — มีผลทันทีในคำขอถัดไป"** | ☐ |
| 5 | VERIFY แถวเดิมในทะเบียน | — | pill → **ถอนแล้ว** ทันที (ไม่มีสถานะ "รออนุมัติ") · แถวยังอยู่ (ไม่ลบ) · timeline เพิ่มรายการถอน + เหตุผล | ☐ |

### TC-REG-09 — ถอน ไม่กรอกเหตุผล (negative · BR_WITHDRAW_REASON_REQUIRED)
- group: ทะเบียน · ความสำคัญ: กลาง · trace: FN-15 / BR-10
- actor: officer · Setup: role=officer · seed=granted consent · files=—
- Start: modal ถอนความยินยอม
- ผ่านเมื่อ: toast warning **"กรอกเหตุผล"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ถอน (จาก consent granted) · (เว้นเหตุผล) SELECT ช่องทาง = phone | — | ช่องทางเลือกแล้ว เหตุผลว่าง | ☐ |
| 2 | CLICK ยืนยันถอน | — | toast warning **"กรอกเหตุผล"** · ไม่ถอน | ☐ |

### TC-REG-10 — ถอน ไม่เลือกช่องทาง (negative · BR_WITHDRAW_CHANNEL_REQUIRED)
- group: ทะเบียน · ความสำคัญ: กลาง · trace: FN-15 / BR-10
- actor: officer · Setup: role=officer · seed=granted consent · files=—
- Start: modal ถอนความยินยอม
- ผ่านเมื่อ: toast warning **"เลือกช่องทางที่ลูกค้าแจ้งมา"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด modal ถอน · TYPE เหตุผล = "ทดสอบ" (ไม่เลือกช่องทาง) | — | เหตุผลกรอกแล้ว ช่องทางว่าง | ☐ |
| 2 | CLICK ยืนยันถอน | — | toast warning **"เลือกช่องทางที่ลูกค้าแจ้งมา"** | ☐ |

### TC-REG-11 — ต่ออายุ = คำขอใหม่อ้างเดิม (FN-17 · BR-13)
- group: ทะเบียน · ความสำคัญ: สูง · trace: FN-17 / AT-17 / BR-13
- actor: officer · Setup: role=officer · seed=CNS-5007 (expired) หรือ CNS-5003 (near-expiry) · files=—
- Start: OPEN `#/consent/registry` → CLICK แถว near/expired → CLICK "สร้างคำขอต่ออายุ"
- ผ่านเมื่อ: เกิดคำขอใหม่ที่อ้างรายการเดิม (refOld) + **ไม่แก้วันหมดอายุเดิม**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` · SELECT กรอง **หมดอายุ** → CLICK แถว **CUS-1004 · PUR-01** (expired) | — | drawer + ปุ่ม **"สร้างคำขอต่ออายุ"** | ☐ |
| 2 | VERIFY+บันทึก **วันหมดอายุเดิม** | — | จดค่า (อ้าง step 5) | ☐ |
| 3 | CLICK **"สร้างคำขอต่ออายุ"** | — | drawer สร้างคำขอ แสดง warn-banner "คำขอนี้เป็น**การต่ออายุ** อ้างรายการเดิม … (สร้างเป็นคำขอใหม่ ไม่แก้วันหมดอายุของเดิม — BR-13)" | ☐ |
| 4 | CLICK **"สร้างคำขอ + ลิงก์/QR"** | — | toast สร้างคำขอสำเร็จ + ไปแท็บคำขอ · คำขอใหม่มี near-tag **"ต่ออายุ"** (refOld) | ☐ |
| 5 | OPEN `#/consent/registry` → VERIFY consent เดิม | — | **วันหมดอายุเดิมไม่เปลี่ยน** (เท่าค่าที่จด step 2) | ☐ |

### TC-REG-12 — ส่งออก CSV (utility)
- group: ทะเบียน · ความสำคัญ: ต่ำ · trace: FN-13 (toolbar) / client-side
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: toast **"ส่งออก N รายการเป็น CSV แล้ว"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → CLICK ปุ่ม **"ส่งออก CSV"** | — | toast success **"ส่งออก N รายการเป็น CSV แล้ว"** (N = จำนวนแถวที่กรองอยู่) | ☐ |

## G5 — Resolve simulator (`/consent/resolve`)

### TC-RES-01 — resolve granted → ส่งได้ (FN-19)
- group: resolve · ความสำคัญ: สูง · trace: FN-19 / AT-19 / BR-19
- actor: ทุก role · Setup: role=officer · seed=CNS-5001 (granted current) · files=—
- Start: OPEN `#/consent/resolve`
- ชุดข้อมูล: C (granted)
- ผ่านเมื่อ: result card verdict **"ส่งได้"** + allowed:true ใน JSON

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` | — | หน้า simulator 3 ช่อง + empty card "เลือกเจ้าของข้อมูล · วัตถุประสงค์ · ช่องทาง แล้วกดตรวจสิทธิ์" | ☐ |
| 2 | SELECT เจ้าของข้อมูล = CUS-1001 · วัตถุประสงค์ = ส่งโปรโมชันสินค้า (PUR-01) · ช่องทาง = email | C | 3 ช่องเลือกครบ | ☐ |
| 3 | CLICK ปุ่ม **"ตรวจสิทธิ์การส่ง"** | — | result card verdict **"ส่งได้"** (is-allow) + JSON `allowed:true, status:"granted"` | ☐ |

### TC-RES-02 — resolve never_asked → ส่งไม่ได้ (ไม่ใช่ 404/declined · FN-20 · EC-01)
- group: resolve · ความสำคัญ: สูง · trace: FN-20 / AT-20 / EC-01 / BR-04,19
- actor: ทุก role · Setup: role=officer · seed=CUS-1008 ไม่มี consent PUR-03 · files=—
- Start: OPEN `#/consent/resolve`
- ชุดข้อมูล: C (never_asked)
- ผ่านเมื่อ: verdict **"ส่งไม่ได้"** + status `never_asked` + reason "ยังไม่เคยขอความยินยอมสำหรับคู่นี้ — ค่าเริ่มต้นคือส่งไม่ได้" — **ไม่มี error/404 · ไม่ใช่ "ไม่ยินยอม"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT CUS-1008 · สำรวจความพึงพอใจฯ (PUR-03) · phone | C | 3 ช่องครบ | ☐ |
| 2 | CLICK **"ตรวจสิทธิ์การส่ง"** | — | verdict **"ส่งไม่ได้"** + reason **"ยังไม่เคยขอความยินยอมสำหรับคู่นี้ — ค่าเริ่มต้นคือส่งไม่ได้"** + JSON `allowed:false, status:"never_asked", found:false` · หน้าไม่ error (ตอบ 200) | ☐ |

### TC-RES-03 — resolve withdrawn → ส่งไม่ได้ (AT-19b)
- group: resolve · ความสำคัญ: สูง · trace: FN-19 / AT-19b / EC-02
- actor: ทุก role · Setup: role=officer · seed=CNS-5004 (withdrawn) · files=—
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: verdict "ส่งไม่ได้" + reason "ถอนความยินยอมแล้วเมื่อ … — ห้ามส่งจนกว่าจะได้รับความยินยอมใหม่"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT CUS-1002 · ส่งโปรโมชันสินค้า (PUR-01) · line | — | 3 ช่องครบ | ☐ |
| 2 | CLICK **"ตรวจสิทธิ์การส่ง"** | — | verdict **"ส่งไม่ได้"** + reason ขึ้นต้น **"ถอนความยินยอมแล้วเมื่อ …"** + JSON `allowed:false, status:"withdrawn"` | ☐ |

### TC-RES-04 — resolve version stale (v1 < v2) → ส่งไม่ได้ (EC-03 · AT-19c)
- group: resolve · ความสำคัญ: สูง · trace: FN-19 / AT-19c / EC-03 / BR-06
- actor: ทุก role · Setup: role=officer · seed=CNS-5002 (CUS-1001×PUR-01×sms · granted v1 · PUR-01 currentVer=2) · files=—
- Start: OPEN `#/consent/resolve`
- ชุดข้อมูล: C (stale)
- ผ่านเมื่อ: verdict "ส่งไม่ได้" + reason "ยินยอมไว้กับนโยบายเวอร์ชัน 1 แต่เวอร์ชันปัจจุบันคือ 2 — ต้องขอความยินยอมใหม่"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT CUS-1001 · ส่งโปรโมชันสินค้า (PUR-01) · **sms** | C | 3 ช่องครบ | ☐ |
| 2 | CLICK **"ตรวจสิทธิ์การส่ง"** | — | verdict **"ส่งไม่ได้"** + reason **"ยินยอมไว้กับนโยบายเวอร์ชัน 1 แต่เวอร์ชันปัจจุบันคือ 2 — ต้องขอความยินยอมใหม่"** | ☐ |

### TC-RES-05 — resolve expired → ส่งไม่ได้
- group: resolve · ความสำคัญ: กลาง · trace: FN-19 / BR-07
- actor: ทุก role · Setup: role=officer · seed=CNS-5007 (expired · CUS-1004×PUR-01×email) · files=—
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: verdict "ส่งไม่ได้" + reason "เคยยินยอมแต่หมดอายุแล้วเมื่อ … — ต้องต่ออายุก่อนจึงจะส่งได้"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT CUS-1004 · ส่งโปรโมชันสินค้า (PUR-01) · email | C | 3 ช่องครบ | ☐ |
| 2 | CLICK **"ตรวจสิทธิ์การส่ง"** | — | verdict **"ส่งไม่ได้"** + reason ขึ้นต้น **"เคยยินยอมแต่หมดอายุแล้วเมื่อ …"** + status `expired` | ☐ |

### TC-RES-06 — resolve เลือกไม่ครบ 3 ช่อง (negative)
- group: resolve · ความสำคัญ: กลาง · trace: FN-19 / validation
- actor: ทุก role · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: toast warning **"เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสิทธิ์"** (ดู Drift note #1)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT เฉพาะเจ้าของข้อมูล (เว้น purpose+channel) | — | เลือกไม่ครบ | ☐ |
| 2 | CLICK **"ตรวจสิทธิ์การส่ง"** | — | toast warning **"เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสิทธิ์"** · ไม่มี result card | ☐ |

### TC-RES-07 — resolve JSON contract ล็อกฟิลด์ (BR-19/20)
- group: resolve · ความสำคัญ: สูง · trace: FN-19 / BR-19,20 / LD-02
- actor: dev/ทุก role · Setup: role=officer · seed=CNS-5001 (granted) · files=—
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: JSON ตัวอย่างมีฟิลด์ล็อกครบ: subject, purpose, channel, allowed, status, policy_version, granted_at, expires_at, found, reason + ตอบ 200 เสมอ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT CUS-1001 · PUR-01 · email → CLICK ตรวจสิทธิ์ | C | result card + บล็อก JSON ตัวอย่าง | ☐ |
| 2 | VERIFY บล็อก JSON | — | มีคีย์ครบ: `subject, purpose, channel, allowed, status, policy_version, granted_at, expires_at, found, reason` (ชื่อ/ความหมายตรงสัญญา — เพิ่มได้ ห้ามเปลี่ยนชื่อ) | ☐ |
| 3 | VERIFY ข้อความใต้หัว simulator | — | ระบุ "ตอบ HTTP 200 เสมอ" (ไม่มี error path) | ☐ |

### TC-RES-08 — lapsed ≠ declined (ไม่ตอบ ไม่ใช่ปฏิเสธ · EC-05 · AT-20b)
- group: resolve · ความสำคัญ: สูง · trace: FN-20 / EC-05 / BR-08 / lock#8
- actor: ทุก role · Setup: role=officer · seed=คำขอ pending เกิน 30 วัน (REQ-2604 expired) · consent ของ triple นั้นยัง never/pending · files=— · **(ต้อง simulate ถ้า seed ไม่มี pending>30วันที่ resolve ได้ตรง — ใช้ triple ของคำขอ expired ที่ยังไม่มี consent record)**
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: verdict ส่งไม่ได้ แต่สถานะ **ไม่ใช่ "declined/ไม่ยินยอม"** — เป็น never_asked/lapsed (การไม่ตอบ ≠ การปฏิเสธ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT subject+purpose+channel ของคำขอที่ส่งไปแต่ยังไม่ตอบ (เช่น CUS-1002 × PUR-02 × email จาก REQ-2604 expired) | — | 3 ช่องครบ | ☐ |
| 2 | CLICK **"ตรวจสิทธิ์การส่ง"** | — | verdict **"ส่งไม่ได้"** แต่ status = **never_asked** (ไม่ใช่ `declined`) · reason สื่อ "ยังไม่ได้รับคำตอบ/ยังไม่เคยขอ" ไม่ใช่ "ปฏิเสธ" (lapsed ≠ declined) | ☐ |

## G6 — FN-40 Negative Locks (ต้องไม่มี — render จริงแล้ว assert absent)

### TC-NEG-01 — ไม่มี cookie consent banner (NEG-40.1 · LOCK-05)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.1 / LOCK-05
- actor: ทุก role · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/registry` (และไล่ทุกแท็บ)
- ผ่านเมื่อ: ไม่พบแบนเนอร์/ป๊อปอัป cookie consent บนหน้าเว็บใด ๆ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → เยี่ยมทุกแท็บ (คำขอ/วัตถุประสงค์/ตรวจสิทธิ์) | — | **ไม่มี** cookie consent banner/ปุ่ม "ยอมรับคุกกี้" ที่ใดเลย (feature นี้คือ consent แบบ triple ไม่ใช่ cookie) | ☐ |

### TC-NEG-02 — ไม่มีสายอนุมัติก่อนส่งคำขอ (NEG-40.2 · LOCK-04)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.2 / LOCK-04
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/requests` → drawer สร้าง/ส่งคำขอ + ถอน
- ผ่านเมื่อ: ไม่มีปุ่ม/สถานะ "อนุมัติ/รออนุมัติ/Approve/Checker" ในสายส่งคำขอและการถอน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK "สร้างคำขอ" → ดูสายสร้าง+ส่ง | — | สร้าง→ส่งได้ทันที · **ไม่มี**ปุ่ม/ป้าย "ส่งอนุมัติ/รออนุมัติ/Approve" | ☐ |
| 2 | เปิด consent granted → modal ถอน | — | subtitle ระบุ "มีผลทันที ไม่ต้องผ่านการอนุมัติ" · **ไม่มี**ขั้นอนุมัติ | ☐ |

### TC-NEG-03 — ไม่ส่งอีเมล/LINE จริง (mock toast เท่านั้น · NEG-40.3 · lock#3)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.3 / lock#3
- actor: officer · Setup: role=officer · seed=REQ-2602 · files=—
- Start: drawer คำขอ → ส่ง
- ผ่านเมื่อ: toast ระบุคำว่า **"(จำลอง — ไม่ส่งจริง)"** ทุกครั้งที่ส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK REQ-2602 → CLICK ส่งทางช่องทาง | — | toast มีวลี **"(จำลอง — ไม่ส่งจริง)"** — ยืนยันว่าไม่มีการส่งอีเมล/LINE จริง | ☐ |

### TC-NEG-04 — ไม่มีคำนวณมูลค่า / คอลัมน์ผลรายท่อ (NEG-40.4 · LOCK-CSQ-04/05)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.4 / LOCK-CSQ-04,05 / BR-CSQ-01
- actor: ทุก role · Setup: role=dpo · seed=default · files=—
- Start: ไล่ทุกหน้า (ทะเบียน/คำขอ/วัตถุประสงค์/resolve)
- ผ่านเมื่อ: ไม่มีคอลัมน์/ฟิลด์ที่เป็นจำนวนเงิน/มูลค่า หรือ "ผลรายท่อ" (pipe result)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → VERIFY หัวตาราง | — | ไม่มีคอลัมน์ amount/มูลค่า/ยอดเงิน/ผลรายท่อ | ☐ |
| 2 | เยี่ยมแท็บวัตถุประสงค์ + resolve | — | ไม่มีตัวเลขมูลค่า/การคำนวณเงินที่ใด | ☐ |

### TC-NEG-05 — ไม่มีการ์ดผล 7 ท่อ CSQ บนจอ (NEG-40.5 · LOCK-CSQ-06)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.5 / LOCK-CSQ-06
- actor: ทุก role · Setup: role=dpo · seed=default · files=—
- Start: ไล่ทุกหน้า
- ผ่านเมื่อ: ไม่พบการ์ด/แผง "7 ท่อ (7C)" หรือ pipe-card แสดงผลรายท่อบนหน้าจอ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เยี่ยมทุกแท็บ + drawer consent | — | **ไม่มี** pipe-card / การ์ด "7C/7 ท่อ" / แผงผล consequence บนจอ (CSQ เป็น declare-only หลังบ้าน) | ☐ |

### TC-NEG-06 — ไม่ประกาศท่อ OC/DC/SC (NEG-40.6 · LOCK-CSQ-01/02/03)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.6 / LOCK-CSQ-01,02,03 / BR-CSQ-05
- actor: dev · Setup: role=dpo · seed=default · files=— · **(ต้อง simulate/inspect — ตรวจ envelope CSQ ที่ระบบยิงเมื่อมี state change)**
- Start: ทำ action ที่ยิง event (เช่น ถอน) แล้ว inspect envelope (console/network mock)
- ผ่านเมื่อ: envelope declare-only — **ไม่มี** field/ประกาศ OC, DC, SC

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) ทำ action ถอน consent → ตรวจ envelope 7C ที่ระบบสร้าง | — | envelope มี event/idempotency_key/reversal_of เท่านั้น · **ไม่มี** OC/DC/SC declaration (declare-only) | ☐ |

### TC-NEG-07 — ใช้ triple (ไม่ใช่ธง opt-out เดียวต่อคน · NEG-40.7 · lock#7)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.7 / lock#7 / BR-01
- actor: officer · Setup: role=officer · seed=CUS-1001 (มีหลาย consent ต่าง purpose/channel) · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: ลูกค้าคนเดียวมีหลายรายการแยกตาม (purpose × channel) — ไม่ใช่ธง opt-out เดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` · TYPE ค้นหา "สมชาย" (CUS-1001) | — | เห็น **หลายแถว** ของ CUS-1001 แยกตาม purpose/channel (PUR-01×email, PUR-01×sms) — ไม่ใช่ธงเดียวต่อคน | ☐ |

### TC-NEG-08 — "ไม่ตอบ" ≠ "ไม่ยินยอม" (NEG-40.8 · lock#8)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.8 / BR-08 (ดู TC-RES-08)
- actor: ทุก role · Setup: role=officer · seed=REQ-2604 (expired/lapsed) · files=—
- Start: OPEN `#/consent/requests`
- ผ่านเมื่อ: คำขอที่หมดเวลาตอบแสดงสถานะ **หมดอายุ (lapsed)** ไม่ใช่ "ไม่ยินยอม/declined"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → หา REQ-2604 | — | สถานะคำขอ = **หมดอายุ (expired/lapsed)** — **ไม่ถูก**ตีความเป็น "ไม่ยินยอม/declined" | ☐ |

### TC-NEG-09 — resolve read-only (ไม่บล็อกการส่งเอง · NEG-40.9 · lock#9)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.9 / lock#9 / API-20 read-only
- actor: ทุก role · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: หน้า resolve ตอบผลอย่างเดียว — **ไม่มี**ปุ่ม "ส่งข้อความ/บล็อก/ระงับ" ใด ๆ (ไม่ mutate)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` → ตรวจสิทธิ์ 1 ครั้ง | — | result card มีแค่ verdict/reason/JSON · **ไม่มี**ปุ่มส่ง/บล็อก/ระงับ · resolve ไม่แก้ข้อมูลใด | ☐ |
| 2 | OPEN `#/consent/registry` → VERIFY ไม่มีอะไรเปลี่ยนจากการ resolve | — | ทะเบียนไม่เปลี่ยน (resolve = read-only) | ☐ |

### TC-NEG-10 — สร้างคำขอเป็น single-screen (ไม่มี wizard 5 ขั้น · NEG-40.10 · LOCK-07)
- group: FN-40 · ความสำคัญ: สูง · trace: NEG-40.10 / LOCK-07 (ดู TC-REQ-01)
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/requests` → CLICK "สร้างคำขอ"
- ผ่านเมื่อ: drawer สร้างคำขอ **ไม่มี** stepper/แท็บ 5 ขั้น — เลือกครบในจอเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK "สร้างคำขอ" | — | drawer **ไม่มี** ตัวบอกขั้น "1/5, 2/5…" หรือปุ่ม ถัดไป/ย้อนกลับ · ทุกฟิลด์ (subject/ช่องทาง/วัตถุประสงค์) อยู่ในจอเดียว | ☐ |

## G7 — Edge cases + Cross-Module (XT)

### TC-EC-04 — double-submit / idempotency (EC-04 · `[AI-DEFAULT]`)
- group: edge · ความสำคัญ: กลาง · trace: EC-04 / BR-CSQ-02 / ERR_DUPLICATE_IDEMPOTENCY_KEY · **(ต้อง simulate — API header 24 ชม.)**
- actor: officer · Setup: role=officer · seed=REQ-2601 · files=— · inject: กด "ส่งคำตอบ/สร้างคำขอ" ซ้ำเร็ว ๆ 2 ครั้ง (double-click) หรือ replay request เดิม
- Start: recipient view หรือ drawer สร้างคำขอ
- ผ่านเมื่อ: การกดซ้ำ → เกิด record **1 รายการ** (ไม่ซ้ำ) · envelope idempotency_key ซ้ำถูกกัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) กด **ส่งคำตอบ** 2 ครั้งเร็ว ๆ ใน recipient view | — | สร้าง consent **ครั้งเดียว** (ไม่เกิดซ้ำ) · ระดับ API = Idempotency-Key กัน · CSQ envelope key ซ้ำ reject | ☐ |

### TC-EC-09 — อัปโหลดชนิด/ขนาดไม่รองรับ (EC-09 · `[AI-DEFAULT]` · OQ-07)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-09 [AI-DEFAULT] / OQ-07 · **(partial — prototype mock ไม่ validate size)**
- actor: dpo · Setup: role=dpo · seed=default · files=`bad_type.exe`, `too_large.pdf`
- Start: drawer สร้างวัตถุประสงค์ → upload
- ผ่านเมื่อ: default accept `.pdf/.doc/.docx/.txt` · ขนาดจริง = TBD (mock ยังไม่ validate — บันทึกผลเป็น [AI-DEFAULT])

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer สร้างวัตถุประสงค์ → UPLOAD `bad_type.exe` | `bad_type.exe` | (default) ชนิดนอก 4 แบบ **ไม่ควรรับ** — บันทึกพฤติกรรมจริง (prototype อาจรับ mock → flag OQ-07) `[AI-DEFAULT]` | ☐ |
| 2 | UPLOAD `too_large.pdf` | `too_large.pdf` | mock ปัจจุบัน **ไม่ validate size** — บันทึกว่าเป็น TBD (OQ-07) `[AI-DEFAULT]` | ☐ |

### TC-EC-10 — timezone ของ expires_at (EC-10 · `[AI-DEFAULT]` · OQ-08)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-10 [AI-DEFAULT] / OQ-08 · **(ต้อง simulate — backend UTC vs tenant TZ)**
- actor: dpo · Setup: role=dpo · seed=consent ใกล้ข้ามวัน/ข้ามเดือน · files=—
- Start: N/A (backend-level)
- ผ่านเมื่อ: default = เก็บ/คำนวณ UTC · display tenant TZ (บันทึกเป็น [AI-DEFAULT] · ตรวจจริงที่ backend)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) ตรวจ expires_at ของ consent ข้ามเขตเวลา | — | default: UTC internal + display TZ ของ tenant · `[AI-DEFAULT]` (fail = default อาจผิด ไม่ใช่โค้ดผิด) | ☐ |

### TC-EC-11 — optimistic lock: 2 dpo ออกเวอร์ชันพร้อมกัน (EC-11 · ERR_STALE_DATA)
- group: edge · ความสำคัญ: กลาง · trace: EC-11 / AT-VER-lock / ERR_STALE_DATA (409) · **(ต้อง simulate — 2 session)**
- actor: dpo · Setup: role=dpo (2 session พร้อมกัน) · seed=PUR-01 · files=`policy-test-v2.pdf` · inject: session A + session B โหลด PUR-01 เวอร์ชันเดียวกัน
- Start: 2 หน้าจอ purView PUR-01
- ผ่านเมื่อ: session ที่ commit ทีหลัง → 409 ERR_STALE_DATA (version mismatch)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) session A + B ออกเวอร์ชันใหม่ PUR-01 พร้อมกัน | — | A สำเร็จ · **B ได้ 409 ERR_STALE_DATA** (version column mismatch) — ไม่เขียนทับเงียบ | ☐ |

### TC-XT-01 — campaign resolve granted → allowed:true → ส่งได้ (XT-01)
- group: cross-module · ความสำคัญ: สูง · trace: XT-01 / BR-19
- actor: campaign (caller) · Setup: role=officer (จำลอง caller ผ่านหน้า resolve) · seed=CNS-5001 · files=—
- Start: OPEN `#/consent/resolve` (จำลอง call ของ campaign)
- ผ่านเมื่อ: resolve granted → allowed:true → campaign ส่งได้ (verify ผ่านผล resolve เพราะ prototype ไม่มีหน้า campaign)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/resolve` · SELECT CUS-1001 · PUR-01 · email → ตรวจสิทธิ์ | C | verdict **ส่งได้** allowed:true → (downstream) campaign ส่งได้ | ☐ |

### TC-XT-02 — campaign resolve never_asked/withdrawn/expired → ไม่ส่ง (default-deny · XT-02)
- group: cross-module · ความสำคัญ: สูง · trace: XT-02 / BR-04,19
- actor: campaign · Setup: role=officer · seed=CUS-1008(never), CNS-5004(withdrawn), CNS-5007(expired) · files=—
- Start: OPEN `#/consent/resolve`
- ผ่านเมื่อ: ทั้ง 3 กรณีตอบ allowed:false + reason → campaign **ไม่ส่ง** (default-deny)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | resolve CUS-1008 × PUR-03 × phone | C(never_asked) | allowed:false status never_asked → ไม่ส่ง | ☐ |
| 2 | resolve CUS-1002 × PUR-01 × line | C(withdrawn) | allowed:false status withdrawn → ไม่ส่ง | ☐ |
| 3 | resolve CUS-1004 × PUR-01 × email | C(expired) | allowed:false status expired → ไม่ส่ง | ☐ |

### TC-XT-03 — ถอน → caller cache invalidation ≤5 นาที (XT-03 · BR-21 · OQ-02)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-03 / BR-21 / EC-02 · **(ต้อง simulate — caller-side cache, ไม่มี server push)**
- actor: caller + officer · Setup: role=officer · seed=CNS-5001 (granted · campaign cache ผล granted แล้ว) · files=— · inject: caller cache ผล granted
- Start: ถอน CNS-5001 → resolve ซ้ำทันที
- ผ่านเมื่อ: ทะเบียนถอนทันที · resolve ตอบ allowed:false ทันที · caller ต้องล้าง cache ≤5 นาที (สัญญาฝั่งผู้เรียก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | resolve CUS-1001 × PUR-01 × email → บันทึกผล = ส่งได้ (baseline) | — | allowed:true (จดไว้) | ☐ |
| 2 | ถอน consent เดียวกัน (TC-REG-08) → resolve ซ้ำทันที | — | resolve ตอบ **allowed:false** ทันที (server ไม่แคช) · caller-side cache ≤5 นาที = สัญญา OQ-02 `[AI-DEFAULT]` | ☐ |

### TC-XT-04 — CSQ envelope shape ทุก state change (XT-04 · declare-only)
- group: cross-module · ความสำคัญ: สูง · trace: XT-04 / BR-CSQ-01..05 / EC-08 · **(ต้อง simulate — inspect envelope)**
- actor: dev · Setup: role=officer/dpo · seed=default · files=— · inject: ทำ action granted/withdrawn/version_published แล้ว inspect envelope
- Start: ทำ action ที่ยิง event
- ผ่านเมื่อ: envelope มี idempotency_key `F-MKT-CONSENT:<ref>:<event>` unique · ถอนมี reversal_of ชี้ grant event · **ไม่มี OC/DC/SC** · payload masked

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เซ็น consent → inspect envelope `consent.granted` | — | idempotency_key = `F-MKT-CONSENT:<consent>:consent.granted` unique · ไม่มี OC/DC/SC | ☐ |
| 2 | (simulate) ถอน consent → inspect envelope `consent.withdrawn` | — | มี **reversal_of** = grant event id (ไม่ลบผลเดิม · BR-CSQ-04) | ☐ |
| 3 | (simulate) ออกเวอร์ชันใหม่ → envelope `policy.version_published` | — | envelope declare-only · payload ไม่มี restricted ดิบ (mask · BR-CSQ-03) | ☐ |

### TC-XT-05 — register `/consent/*` Backend Enforcement Gate F143 (XT-05 · BR-22 · OQ-04)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-05 / BR-22 / OQ-04 · **(ต้อง simulate — external dependency, ก่อน go-live)**
- actor: ทีม Security · Setup: role=— · seed=— · files=— · inject: deployment gate
- Start: N/A (deployment/registry)
- ผ่านเมื่อ: endpoint `/consent/*` ขึ้นทะเบียน Enforcement Gate + ผ่าน review 4 ขั้น ก่อน go-live (hard dependency)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) ตรวจ deployment checklist | — | `/consent/*` register + 4-step review pass — **BLOCKED go-live ถ้ายังไม่ครบ** (OQ-04) | ☐ |

## G8 — Permission matrix (persona switcher)

### TC-PERM-01 — officer: แก้ purpose ไม่ได้ (deny · read + chip)
- group: permission · ความสำคัญ: สูง · trace: PERM officer×purpose=deny / ERR_INSUFFICIENT_ROLE (OQ-05)
- actor: officer · Setup: role=officer (persona "Officer") · seed=default · files=—
- Start: OPEN `#/consent/purposes`
- ผ่านเมื่อ: ไม่มีปุ่ม "สร้างวัตถุประสงค์" · เห็น chip **"เฉพาะ DPO แก้ไขได้"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **Officer** → OPEN `#/consent/purposes` | — | **ไม่มี**ปุ่ม "สร้างวัตถุประสงค์" · เห็น chip **"เฉพาะ DPO แก้ไขได้"** (มี icon lock) | ☐ |
| 2 | CLICK แถว purpose | — | ดูได้ (read) · ไม่มีปุ่มปิด/ออกเวอร์ชัน (แก้ไม่ได้) | ☐ |

### TC-PERM-02 — officer: สร้างคำขอ/ถอน/resolve ได้ (allow)
- group: permission · ความสำคัญ: สูง · trace: PERM officer allow reqCreate/withdraw/resolve
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: OPEN `#/consent/requests`
- ผ่านเมื่อ: มีปุ่มสร้างคำขอ + ถอนได้ + resolve ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | persona Officer → OPEN `#/consent/requests` | — | เห็นปุ่ม **"สร้างคำขอ"** | ☐ |
| 2 | OPEN `#/consent/registry` → CLICK consent granted | — | เห็นปุ่ม **"ถอนความยินยอม"** | ☐ |
| 3 | OPEN `#/consent/resolve` → ตรวจสิทธิ์ | — | ใช้งาน resolve ได้ | ☐ |

### TC-PERM-03 — dpo: purpose CRUD + ปิด + upload (allow)
- group: permission · ความสำคัญ: สูง · trace: PERM dpo×purpose=allow
- actor: dpo · Setup: role=dpo (persona "DPO") · seed=default · files=—
- Start: OPEN `#/consent/purposes`
- ผ่านเมื่อ: มีปุ่มสร้างวัตถุประสงค์ + ออกเวอร์ชัน + ปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **DPO** → OPEN `#/consent/purposes` | — | เห็นปุ่ม **"สร้างวัตถุประสงค์"** (ไม่มี chip lock) | ☐ |
| 2 | CLICK แถว purpose | — | เห็นปุ่ม **"ออกเวอร์ชันใหม่"** + **"ปิดวัตถุประสงค์"** | ☐ |

### TC-PERM-04 — auditor: read-only (deny mutation)
- group: permission · ความสำคัญ: สูง · trace: PERM auditor×(reqCreate/withdraw/purpose)=deny
- actor: auditor · Setup: role=auditor (persona "Auditor") · seed=default · files=—
- Start: OPEN `#/consent/requests` + registry + purposes
- ผ่านเมื่อ: ไม่มีปุ่มสร้างคำขอ/ถอน/สร้างวัตถุประสงค์ (ปุ่ม mutation หายทั้งหมด)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK persona **Auditor** → OPEN `#/consent/requests` | — | **ไม่มี**ปุ่ม "สร้างคำขอ" | ☐ |
| 2 | OPEN `#/consent/registry` → CLICK consent granted | — | **ไม่มี**ปุ่ม "ถอนความยินยอม" (read-only) | ☐ |
| 3 | OPEN `#/consent/purposes` | — | ไม่มีปุ่มสร้าง/แก้ purpose | ☐ |

### TC-PERM-05 — auditor: ดูทะเบียน/หลักฐาน + resolve (read) ได้
- group: permission · ความสำคัญ: กลาง · trace: PERM auditor allow view+resolve(read)
- actor: auditor · Setup: role=auditor · seed=CNS-5001 · files=—
- Start: OPEN `#/consent/registry`
- ผ่านเมื่อ: เปิดดูหลักฐาน 5 + timeline + resolve ได้ (อ่าน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | persona Auditor → OPEN `#/consent/registry` → CLICK แถว granted | — | เห็นหลักฐาน 5 + timeline (อ่านได้) | ☐ |
| 2 | OPEN `#/consent/resolve` → ตรวจสิทธิ์ | — | resolve แสดงผลได้ (อ่าน) | ☐ |

## G9 — UX / interaction

### TC-UX-01 — tab navigation 4 แท็บ + default route
- group: ux · ความสำคัญ: กลาง · trace: 01_UI §1.1 routes / default `#/consent/registry`
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: เปิดไฟล์ (fresh)
- ผ่านเมื่อ: default = ทะเบียน · คลิกแต่ละแท็บเปลี่ยน route + breadcrumb ถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด `consent-pdpa.html` (fresh) | — | route = `#/consent/registry` · แท็บ **ทะเบียน** active | ☐ |
| 2 | CLICK แท็บ **คำขอ** | — | route `#/consent/requests` · breadcrumb "คำขอ" | ☐ |
| 3 | CLICK แท็บ **วัตถุประสงค์** | — | route `#/consent/purposes` | ☐ |
| 4 | CLICK แท็บ **ตรวจสิทธิ์** | — | route `#/consent/resolve` | ☐ |

### TC-UX-02 — Esc chain / 3-way close overlay
- group: ux · ความสำคัญ: กลาง · trace: 01_UI §1.8 Esc chain / closeOverlay
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: เปิด drawer ใด ๆ
- ผ่านเมื่อ: ปิด drawer ได้ 3 ทาง (Esc / backdrop / ปุ่ม X หรือ ยกเลิก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/requests` → CLICK "สร้างคำขอ" → PRESS Esc | — | drawer ปิด | ☐ |
| 2 | เปิด drawer อีกครั้ง → CLICK backdrop (พื้นที่มืดนอก drawer) | — | drawer ปิด | ☐ |
| 3 | เปิด drawer อีกครั้ง → CLICK ปุ่ม **ยกเลิก** / X | — | drawer ปิด | ☐ |

### TC-UX-03 — decorativeNav toast (เมนูโมดูลอื่น)
- group: ux · ความสำคัญ: ต่ำ · trace: 01_UI §1.7 decorativeNav
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: shell sidebar
- ผ่านเมื่อ: คลิกเมนูโมดูลอื่น (เดโม) → toast **"เมนูนี้เป็นบริบทของโมดูลอื่น (เดโมไม่รวมขอบเขต)"**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เมนู sidebar โมดูลอื่น (ไม่ใช่ "ความยินยอม PDPA") | — | toast info **"เมนูนี้เป็นบริบทของโมดูลอื่น (เดโมไม่รวมขอบเขต)"** — ไม่ navigate ออก | ☐ |

### TC-UX-04 — toast auto-dismiss
- group: ux · ความสำคัญ: ต่ำ · trace: microcopy กลาง / showToast duration
- actor: officer · Setup: role=officer · seed=default · files=—
- Start: ทำ action ที่มี toast (เช่น ส่งออก CSV)
- ผ่านเมื่อ: toast แสดงแล้วหายเองภายในไม่กี่วินาที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/consent/registry` → CLICK "ส่งออก CSV" | — | toast ปรากฏ | ☐ |
| 2 | WAIT ~3 วินาที | — | toast หายเอง (auto-dismiss) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)
1. เปิด `consent-pdpa.html` ในเบราว์เซอร์ (prototype มี seed ในตัว — ไม่ต้อง login จริง)
2. **สลับ role ผ่าน persona strip** (`Officer / DPO / Auditor`) ตามที่ `Setup:` ระบุ ก่อนเริ่มทุกเคส
3. ทุกเคส refresh-safe: เริ่มจาก `Start` route ของตัวเอง (reload หน้าถ้าจำเป็นเพื่อรีเซ็ตสถานะ seed)
4. เดินตามตาราง step (Action verb → Input → Expected) แล้วติ๊ก Result (☐→✅/❌/⊘)
5. เคส `(ต้อง simulate)` = ต้อง inject สภาพที่กดมือไม่ได้ (2 session / API replay / inspect envelope) — ทำไม่ได้ = `blocked`
6. เคส `[AI-DEFAULT]` = เกณฑ์ที่ AI ตัดสินแทน BA — fail อาจแปลว่า "default ผิด" ไม่ใช่ "โค้ดผิด" → ระบุใน note
7. กรอกผลใน Result Report (schema) ด้านล่าง

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN บวก (FUNCTION_CHECKLIST) | **20 / 20** |
| FN-40 Negative Locks | **10 / 10** |
| FR / AT (06_TESTS AT-01..20 + AT-ID/VER) | 22 / 22 |
| Business rules (05_RULES §5.1) | 27 / 27 (BR-21/22 = ต้อง simulate) |
| Edge cases (EC-01..11) | 11 / 11 (EC-04/10/11 simulate · EC-09 partial) |
| Error codes (catalog) | 12 / 12 (idempotency/stale = simulate) |
| Field validation | 10 / 10 |
| Permission cells (สำคัญ) | 5 / 5 (enforce จริง = OQ-05) |
| Cross-cutting / events / states / UI states | ครบ |

- Cross-Module (XT): **5 / 5** (XT-03/04/05 = ต้อง simulate)
- Scope Lock (LOCK): **13 / 13** (ทุกข้อมีเคส verify — ส่วนใหญ่เป็น NEG verify "ไม่มี")
- **Manifest cross-check (FRD §0.12): ✅ 20/20 stories + 22 rules + 5 edges** — ทุกแถว manifest มีคู่ใน Ledger

### ข้าม (พร้อมเหตุผล)
- **Out-of-Scope 10 Locks** — ห้ามสร้างเคส "ทำได้"; แทนด้วยเคส verify **ไม่มี** (TC-NEG-01..10) — ตามใบเซ็น/LOCK
- **sort คอลัมน์** — ไม่มี sortable column ใน registry table (observed จาก HTML) → ไม่มีเคส
- **pagination** — seed prototype ไม่ถึง 1 หน้า (ไม่มี pagination control สังเกตได้บน UI) → ข้าม (จริงต้องมีตอน dev)
- **D7 encryption-at-rest · D17 RLS multi-tenant** — backend-only, single-user demo ไม่มีผลบน prototype UI → ข้าม (05_RULES §5.7)
- **BR-21/22 · XT-03/04/05 · EC-04/10/11** — ต้อง simulate (caller cache / F143 register / API idempotency / optimistic lock / timezone) — มีเคสใน Ledger แต่ mark `(ต้อง simulate)` — runner อาจ `blocked` ถ้า inject ไม่ได้

> **Note:** resolve toast/label ในเคสยึด **verbatim จาก HTML** (มี drift เล็กน้อยกับ 05_RULES/06_TESTS — ดู Drift note หัวไฟล์ · HTML ชนะ). Permission เป็น persona switcher เดโม (OQ-05 enforce จริง).

---

## Result Report (schema)

```json
{
  "feature_id": "F-MKT-CONSENT",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-PUR-01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 68, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ toast จริง, route ที่ค้าง, verdict/JSON ที่ได้แทน Expected). `note` = สำหรับ `(ต้อง simulate)` ระบุว่า inject ได้/ไม่ได้ · สำหรับ `[AI-DEFAULT]` ระบุว่าพฤติกรรมตรง default หรือไม่.
</content>
</invoke>
