# BRD — ความยินยอม PDPA (Consent PDPA)

> **โหมด:** brd-generator-full v2.2 · **Fresh Mode (HTML-first)** — HTML ผ่าน ux+coverage gate แล้ว = source of truth ฝั่งหน้าจอ
> **Conflict priority ที่ใช้จริง:** LOCK-XX > PREBRIEF (business intent) > HTML (พฤติกรรมจอ) · ทุก drift ประกาศ ไม่แก้เงียบ

---

## Section 1 · Document Info

| หัวข้อ | ค่า |
|---|---|
| BRD ID | BRD-F-MKT-CONSENT |
| ชื่อ Feature | ความยินยอม PDPA (Consent Management) |
| รหัส Feature | F-MKT-CONSENT (F058) |
| Module | Marketing |
| Wave | W1 |
| Dependency | **standalone — ไม่มี upstream dependency** (plan `dep=""`) |
| ประเภท BRD | New Feature |
| Version | 1.0 |
| Status | **APPROVED** (ผ่าน Quality Gate — ดู §14.7) |
| Owner (BA) | tadswan@2bsimple.com |
| Stakeholders | เจ้าหน้าที่การตลาด · ผู้ดูแลข้อมูลส่วนบุคคล (DPO) · ผู้ตรวจสอบ (Auditor) · ทีมพัฒนา · ทีม Security (เจ้าของ Backend Enforcement Gate F143) |
| Declaration รอบนี้ | **csq เท่านั้น** (`CSQ_BRIEF` ออกที่ step 7) · doa / doccfg / ntf = ไม่เลือก |
| วันที่ | 2026-09-13 |
| Input | `consent-pdpa.html` (3086 บรรทัด, ผ่าน gate) · `PREBRIEF_F-MKT-CONSENT.md` · `FUNCTION_CHECKLIST_F-MKT-CONSENT.md` (20 FN + 10 FN-40) · `_UX_CHECK_REPORT.md` (PASS/4WARN cosmetic) · `_COVERAGE_REPORT.md` (PASS FN 20/20) |

### 1.1 Changelog
- **v1.0 (2026-09-13):** Initial BRD via brd-generator-full (Fresh Mode HTML-first). สกัด Screen Inventory จาก HTML จริง · encode content-model divergence (เอกสารอัปโหลด) เป็น DECLARED DIVERGENCE

### 1.2 ⚠️ Declared Divergence (สำคัญ — อ่านก่อน)
BRD ฉบับนี้สะท้อน **โมเดลที่ระบบสร้างจริง (HTML)** ซึ่งต่างจาก PREBRIEF ที่ยังไม่ sync:

| # | เรื่อง | PREBRIEF เดิม | โมเดลที่สร้างจริง (BRD นี้ยึด) | เจ้าของแก้ |
|---|---|---|---|---|
| **DECLARED-01** | โมเดลเนื้อหา PDPA | ข้อความพิมพ์ (free-text) — BR-05/06 "แก้ข้อความ = ออกเวอร์ชัน" · S-01/02/09 · FN-01/02/09/10/11 | **เอกสารอัปโหลด (versioned per purpose)** — upload → ออกเวอร์ชัน → download เอกสาร | **BA ต้อง sync PREBRIEF BR-05/06 + S-01/02/09 + FN-01/02/09/10/11** (→ §15 OQ-01) |
| **DECLARED-02** | DOA detect | ตัวตรวจ `prebrief_checklist.py` เจอ `doa:true` | **false positive** — keyword "อนุมัติ" ไปโดนประโยคปฏิเสธ "ไม่ต้องผ่านการอนุมัติ" (BR-09) · Part C#2 ห้าม approval chain | ไม่ต้องแก้ (สัญญาณหลอก C3.9) |

> การยึดโมเดลเอกสารอัปโหลด **ไม่ใช่การแต่ง scope เอง** — เป็นมติ PM/BA 2026-09-11 ที่บันทึกไว้ใน FUNCTION_CHECKLIST header + coverage report DECLARED-01 · BRD ประกาศไว้ตรงนี้เพื่อไม่ให้ downstream (FRD/TC) ไหลตาม PREBRIEF ข้อความเดิม

---

## Section 2 · Business Context

### 2.1 ปัญหา / โอกาส
ปัจจุบันการเก็บความยินยอมทำการตลาดกระจัดกระจาย ไม่มีทะเบียนกลางที่ตอบได้ว่า "ลูกค้ารายนี้ยินยอมให้ส่งอะไร ทางช่องทางไหน ภายใต้นโยบายเวอร์ชันไหน" — เสี่ยงส่งข้อความหาคนที่ไม่ยินยอม/ถอนแล้ว/หมดอายุ ซึ่งมีผลทางกฎหมาย PDPA โดยตรง และไม่มีหลักฐานย้อนกลับเมื่อถูกตรวจสอบ

### 2.2 เป้าหมาย business
1. มีทะเบียนความยินยอมกลางแบบ **เจ้าของข้อมูล × วัตถุประสงค์ × ช่องทาง** ที่ default = ไม่อนุญาต
2. ทุกความยินยอมมีหลักฐานครบและแก้ไม่ได้ (audit-ready)
3. ระบบปลายทาง (แคมเปญ/ส่งข้อความ) เรียกตรวจสิทธิ์ผ่าน API เดียวก่อนส่งทุกครั้ง
4. ถอน/ต่ออายุ/ออกเวอร์ชันนโยบายใหม่ ทำได้ครบวงจรและตรวจสอบย้อนได้

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ | คู่ใน §17.3 |
|---|---|---|---|---|---|
| % การส่งการตลาดที่ผ่านการตรวจ `/consent/resolve` ก่อนส่ง | ต้องเก็บ baseline ก่อน launch (action) | ≥ 99% | log ของ Backend Enforcement Gate (F143) นับ call ที่มี resolve นำหน้า | รายเดือน | KPI-Compliance |
| จำนวนการส่งไปยัง subject ที่ status ≠ granted (การส่งผิด) | ต้องเก็บ baseline (action) | 0 | cross-check log การส่ง vs ทะเบียน | รายเดือน | KPI-Quality |
| % ความยินยอมที่มีหลักฐานครบ 5 อย่าง | 0 (ไม่มีระบบ) | 100% | นับ record ที่ evidence ครบใน registry | ต่อเนื่อง | KPI-Compliance |
| เวลาเฉลี่ยในการถอนความยินยอมแทนลูกค้า (รับสาย→มีผล) | ไม่มีข้อมูล | ≤ 2 นาที (มีผลทันทีในระบบ) | timestamp history: requested→withdrawn | รายไตรมาส | SLA-Withdraw |
| % รายการที่ต่ออายุก่อนหมดอายุ (จากรายการ ≤30 วัน) | 0 | ≥ 70% | นับ renew request vs near-expiry list | รายเดือน | KPI-Conversion |

> ⚠️ Baseline หลายตัวยัง = "ต้องเก็บก่อน launch" → เป็น action ก่อน go-live (ไม่ใช่ตัวชี้วัดลอย) → §15 OQ-06

### 2.4 ที่มา
PDPA compliance requirement (Marketing) · plan row `F058 · Marketing · W1 · dec=["csq"] · dep=""` · PREBRIEF S-01…S-20

---

## Section 3 · Scope

### 3.1 In Scope
1. จัดการวัตถุประสงค์ (purpose) + ช่องทางที่ใช้ได้ + อายุความยินยอม + **เอกสารนโยบายแบบ versioned (อัปโหลด)**
2. สร้าง/ส่ง/ส่งซ้ำ/คัดลอกลิงก์+QR/ดาวน์โหลดเอกสาร ของคำขอความยินยอม (ส่งเป็น **mock** เท่านั้น)
3. มุมมองผู้รับ (recipient read+sign view) — จำลองหน้าที่เจ้าของข้อมูลเห็นเมื่อกดลิงก์ (อ่านเอกสาร → ยืนยันตัวตน → ยินยอม/ไม่ยินยอมรายวัตถุประสงค์ → เซ็น)
4. ทะเบียนความยินยอม + สถิติ + กรองทุกมิติ + Customer 360
5. หลักฐาน 5 อย่าง + ประวัติ append-only ต่อรายการ
6. ถอนแทนลูกค้า (เหตุผล+ช่องทาง มีผลทันที) · รายการใกล้หมดอายุ · ต่ออายุ (คำขอใหม่อ้างเดิม)
7. ตัวจำลอง `/consent/resolve` (read-only simulator) + สัญญา JSON ที่ล็อกฟิลด์
8. Declaration: **csq** (declare-only event hook → 7C Engine)

### 3.2 Out of Scope (สำคัญ — 10 Locks จาก Part C)
| # | ไม่ทำ | LOCK |
|---|---|---|
| 1 | ความยินยอมคุกกี้บนเว็บไซต์ | LOCK-05 |
| 2 | สายอนุมัติภายในก่อนส่งคำขอ | LOCK-04 |
| 3 | ส่งอีเมล/SMS/LINE จริง (feature นี้ mock เท่านั้น) | — |
| 4 | คำนวณมูลค่าใด ๆ / คอลัมน์เก็บผลรายท่อ | LOCK-CSQ-04/05 |
| 5 | วาดการ์ดผล 7 ท่อ CSQ บนหน้าจอ | LOCK-CSQ-06 |
| 6 | ประกาศท่อ OC / DC (ระดับเอกสาร) / SC | LOCK-CSQ-01/02/03 |
| 7 | ธง opt-out เดียวต่อคน (แบบ Odoo) — ต้องใช้คู่สามมิติ | — |
| 8 | ให้ "ไม่ตอบ" นับเป็น "ไม่ยินยอม" (lapsed ≠ declined) | — |
| 9 | บล็อกการส่งด้วยตัวเอง — resolve ตอบอย่างเดียว | — |
| 10 | wizard Pattern Q (สร้างคำขอ = single-screen) | LOCK-07 |

### 3.3 Assumptions (จาก PREBRIEF Part D — [ASSUMED])
- อายุความยินยอมเริ่มต้น 24 เดือน (ตั้งได้รายวัตถุประสงค์ 1–120 เดือน)
- กำหนดตอบกลับคำขอ 30 วัน แล้วถือคำขอหมดอายุ · เตือนก่อนหมดอายุ 30 วัน
- ช่องทาง: อีเมล · SMS · LINE · โทรศัพท์ · ไปรษณีย์
- **วิธียืนยันตัวตนในมุมมองผู้รับ = checkbox mock** (ต้นแบบ) · วิธีจริง (ลิงก์/OTP/สแกนกระดาษ) = TBD โดย BA → §15 OQ-03

### 3.4 Scope Lock ⭐
- **LOCK-04, LOCK-05, LOCK-07, LOCK-CSQ-01…06** = สืบทอดจาก Part C · **ห้าม override ตลอด chain** — business rule ใดขัดกับ LOCK → LOCK ชนะ
- **ผลตรวจ scope drift:** ไม่พบ scope เกินใบเซ็น (coverage report `scope creep = ไม่พบ`) · recipient view = in-scope (mock ของลิงก์ภายนอก ไม่ใช่ email/LINE จริง)
- persona/role switcher + `decorativeNav` (เมนูโมดูลอื่น) + `exportCsv` (E4) = utility เดโม ระบุ toast ชัด ไม่ขัด contract

---

## Section 4 · User Roles & Permissions

ระบบมี role switcher เดโม 3 บทบาท (`roleMap` — officer / dpo / auditor):

| Role | ดูทะเบียน/หลักฐาน | สร้าง/แก้วัตถุประสงค์ + อัปโหลดเวอร์ชัน | สร้าง/ส่งคำขอ | ถอนแทนลูกค้า | ปิดวัตถุประสงค์ | ตรวจสิทธิ์ (resolve) |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| เจ้าหน้าที่การตลาด (officer) | ✅ | ✅ | ✅ | ✅ (ระบุเหตุผล+ช่องทาง) | ➖ | ✅ |
| ผู้ดูแลข้อมูล / DPO (dpo) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ผู้ตรวจสอบ (auditor) | ✅ (อ่านอย่างเดียว) | ❌ | ❌ | ❌ | ❌ | ✅ (อ่าน) |

> รายละเอียด permission ระดับ field/route ที่แท้จริง → กำหนดใน FRD + Security Preset (§16) · ⚠️ HTML ปัจจุบันเป็น role switcher เดโม (ไม่บังคับสิทธิ์จริง) → matrix ข้างบนเป็น business intent ที่ FRD ต้อง enforce → §15 OQ-05

---

## Section 5 · User Journey (with COSO)

> Feature นี้ **ไม่มี approval chain** (LOCK-04) — COSO Checker/Approver จึงไม่ปรากฏในสายส่งคำขอ; การควบคุมอยู่ที่ default-deny + evidence + audit trail แทน SoD แบบอนุมัติ

### 5.1 Happy Path — วงจรความยินยอม

| # | Step | route/จุดบนจอ | Maker | Checker | Approver | System |
|--:|---|---|---|---|---|---|
| 1 | ตั้งวัตถุประสงค์ + อัปโหลดเอกสาร v1 | `#/consent/purposes` → drawer สร้าง | เจ้าหน้าที่/DPO | — | — | บังคับ name+≥1 channel+life 1–120+เอกสาร → push `versions:[{v:1}]` |
| 2 | สร้างคำขอ (subject + purposes หลายข้อ + channel) | `#/consent/requests` → drawer single-screen | เจ้าหน้าที่ | — | — | gen link + QR · status = draft |
| 3 | ส่งคำขอ (email/…) | drawer รายละเอียดคำขอ | เจ้าหน้าที่ | — | — | บันทึกการส่ง (mock toast) · status → pending |
| 4 | เจ้าของข้อมูลอ่าน+ยืนยันตัวตน+เลือกยินยอมรายข้อ+เซ็น | recipient view (mock ลิงก์ภายนอก) | เจ้าของข้อมูล | — | — | `applyAnswers` → registry row granted/declined ต่อ purpose + evidence 5 + history + supersede คู่เดิม |
| 5 | ดูทะเบียน/หลักฐาน/ประวัติ | `#/consent/registry` → consent drawer | ทุก role (auditor อ่าน) | — | — | render evidence 5 + timeline append-only |
| 6 | ระบบปลายทางตรวจสิทธิ์ก่อนส่ง | `#/consent/resolve` (จำลอง) / API จริง | ระบบปลายทาง | — | — | ตอบ 200 + allowed + reason + JSON ล็อกฟิลด์ |

### 5.2 Alternative / Exception Paths
- **A1 ยินยอมบางวัตถุประสงค์:** เลือกยินยอม 2 ปฏิเสธ 1 → บันทึกแยกรายข้อ (ไม่ใช่ทั้งก้อน)
- **A2 ออกเวอร์ชันนโยบายใหม่:** อัปโหลดเอกสารใหม่ → v+1 + เตือน consent v เดิม N รายการไม่ครอบคลุม (BR-06)
- **A3 ถอนความยินยอม:** ลูกค้าโทรมา → เจ้าหน้าที่ถอน (เหตุผล+ช่องทาง) มีผลทันที ไม่ต้องอนุมัติ
- **A4 ต่ออายุ:** จากรายการ ≤30 วัน → สร้างคำขอใหม่อ้างรายการเดิม (ไม่แก้วันหมดอายุเดิม)
- **A5 ปิดวัตถุประสงค์:** ห้ามสร้างคำขอใหม่ · consent เดิมยังอยู่เป็นหลักฐาน
- **E1 ตรวจคนไม่เคยถูกขอ:** resolve → `allowed:false · status:"never_asked"` (ไม่ใช่ 404 · ไม่ใช่ declined)
- **E2 คำขอเกินกำหนดตอบ:** → status `expired` (คำขอหมดอายุ) ≠ declined

> ทุก step map กับ route/ปุ่มจริงบนจอ — ไม่มี step ลอย (ตรวจกับ Screen Inventory §14.6)

---

## Section 6 · Data Entity & Fields

### 6.1 Entities (New)
1. **Purpose (วัตถุประสงค์)** — header + `versions[]` (versioned document)
2. **PolicyVersion (เวอร์ชันเอกสารนโยบาย)** — immutable, ฝังใน `purpose.versions[]`
3. **ConsentRequest (คำขอ)** — header + `purposes[]` + `sends[]`
4. **Consent (ความยินยอม — record ในทะเบียน)** — triple key + evidence + history[]
5. **Evidence (หลักฐาน 5 อย่าง)** — ฝังใน consent
6. **HistoryEntry (ประวัติ)** — append-only, ฝังใน consent

### 6.2 Field Tables (สกัดจาก HTML mock)

**Purpose**
| # | Field | Label | Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|--|---|---|---|---|:--:|---|
| 1 | code | รหัสวัตถุประสงค์ | AUTO | PUR-0x | ✅ | |
| 2 | name | ชื่อวัตถุประสงค์ | TEXT | | ✅ | |
| 3 | channels | ช่องทางที่ใช้ได้ | DROPDOWN-MULTI | email/sms/line/phone/post | ✅ (≥1) | BR-03 |
| 4 | lifespan | อายุความยินยอม (เดือน) | NUMBER | 1–120 (default 24) | ✅ | BR-11 |
| 5 | status | สถานะ | AUTO | active / closed | ✅ | BR-14 |
| 6 | currentVer | เวอร์ชันปัจจุบัน | AUTO | int | ✅ | |
| 7 | versions[] | เวอร์ชันเอกสาร | LIST | {v, docName, docType, body} | ✅ | **DECLARED-01: เอกสารอัปโหลด** |

**PolicyVersion (versions[])** — `v` (int), `docName`, `docType` (.pdf/.doc/.docx/.txt), `body` (เนื้อหา/ไฟล์อ้างอิง) · **immutable** (BR-05)

**Consent (record ทะเบียน)**
| # | Field | Label | Type | หมายเหตุ |
|--|---|---|---|---|
| 1 | id | รหัสความยินยอม | AUTO | CNS-xxxx |
| 2 | subject | เจ้าของข้อมูล | LOOKUP | CUS-xxxx |
| 3 | purpose | วัตถุประสงค์ | LOOKUP | PUR-0x |
| 4 | channel | ช่องทาง | DROPDOWN-SINGLE | **triple key ร่วมกับ subject+purpose (BR-01)** |
| 5 | status | สถานะ (เก็บ) | AUTO | pending/granted/declined/withdrawn |
| 6 | policyVersion | เวอร์ชันนโยบายที่เซ็น | AUTO(snapshot) | **BR-06 — bound to version signed** |
| 7 | grantedAt / updated / expiresAt | เวลาให้/แก้ล่าสุด/หมดอายุ | DATETIME | expiresAt = grantedAt + lifespan |
| 8 | evidence | หลักฐาน 5 อย่าง | OBJECT | BR-15 |
| 9 | grantEvent | event id อ้างอิง (สำหรับ reversal) | AUTO | BR-CSQ-04 |
| 10 | history[] | ประวัติ | LIST(append-only) | BR-16 |

**Evidence (5 อย่าง — ยืนยันจาก HTML `ev()`):** `answeredAt` (เวลาที่ตอบ) · `requestChannel` (ช่องทางที่ส่งคำขอ) · `idMethod` (วิธียืนยันตัวตน) · `policyVersion` (เวอร์ชันนโยบาย) · `ipDevice` (IP + อุปกรณ์) — **ครบ 5 ตรง BR-15**

**ConsentRequest** — `id` (REQ-xxxx) · `subject` · `purposes[]` · `channel` · `status` (draft/pending/answered/expired) · `createdAt` · `sends[]` ({ch, at}) · `refOld` (อ้างรายการเดิมเมื่อต่ออายุ, BR-13) · `link` + QR

**HistoryEntry** — `at` · `action` (requested/granted/declined/withdrawn/…) · `label` · `reason` (ถอน) · `via` (ช่องทางที่ลูกค้าแจ้ง)

### 6.3 ER Diagram
```
Purpose ──(1:N contains)──▶ PolicyVersion (versions[], immutable)
Purpose ──(referenced by)──▶ ConsentRequest.purposes[]  (N:M)
Purpose ──(referenced by)──▶ Consent.purpose
ConsentRequest ──(1:N on answer)──▶ Consent           (per-purpose split)
Consent ──(1:1 has)──▶ Evidence
Consent ──(1:N contains)──▶ HistoryEntry (append-only)
Consent.refOld ──(renew ref)──▶ Consent (previous)
Subject(Customer, external ref CUS-xxxx) ──(1:N)──▶ Consent
```
> Snapshot field: `Consent.policyVersion` เก็บค่า ณ เวลาเซ็น (ไม่ตามเวอร์ชันปัจจุบันอัตโนมัติ — BR-06)

---

## Section 7 · User Stories & Acceptance Criteria

(Given-When-Then · map 1:1 กับ FN — 20 stories ตรงกับ FUNCTION_CHECKLIST · แต่ละ story ห้ามมี "และ")

- **US-01 (FN-01):** ตั้งวัตถุประสงค์ใหม่พร้อมอัปโหลดเอกสาร v1
  AC1: ต้องกรอก name + ≥1 channel + อายุ 1–120 + แนบเอกสาร มิฉะนั้นบันทึกไม่ได้ · AC2: บันทึกแล้วได้ `versions:[{v:1}]`
- **US-02 (FN-02):** อัปโหลดเอกสารเวอร์ชันใหม่
  AC1: ออก v+1 · AC2: เตือน consent v เดิม N รายการไม่ครอบคลุม
- **US-03 (FN-03):** ดูตารางวัตถุประสงค์พร้อมสถิติ (ยินยอม/ถอน/หมดอายุ/%ครอบคลุม)
- **US-04 (FN-04):** ปิดวัตถุประสงค์ — AC1: สร้างคำขอใหม่ไม่ได้ · AC2: consent เดิมยังอยู่
- **US-05 (FN-05):** สร้างคำขอรายเดียวแบบ single-screen — AC1: ไม่มี stepper · AC2: ได้ link+QR
- **US-06 (FN-06):** ส่งคำขอทางอีเมล — AC1: บันทึกเวลา/ที่อยู่ · AC2: status → pending
- **US-07 (FN-07):** ส่งซ้ำช่องทางอื่น — AC1: นับเป็นการส่งครั้งที่ N · AC2: ไม่สร้างคำขอใหม่
- **US-08 (FN-08):** คัดลอกลิงก์/ดาวน์โหลด QR — AC: บันทึกการนำลิงก์ออก
- **US-09 (FN-09):** ดาวน์โหลดเอกสารของคำขอ — AC: เป็นเอกสารเวอร์ชันปัจจุบันของแต่ละวัตถุประสงค์
- **US-10 (FN-10):** เซ็นผ่านมุมมองผู้รับ — AC1: ต้องยืนยันตัวตนก่อนส่ง · AC2: สร้างทะเบียน+หลักฐาน 5
- **US-11 (FN-11):** ยินยอมบางวัตถุประสงค์ผ่านมุมมองผู้รับ — AC: บันทึกแยกรายข้อ
- **US-12 (FN-12):** ดูหลักฐาน 1 รายการ — AC: เห็นครบ 5 ฟิลด์
- **US-13 (FN-13):** ดูทะเบียนทั้งหมด — AC: กรองได้ทุกมิติ (search/status/channel/purpose)
- **US-14 (FN-14):** ดู consent รายลูกค้าในที่เดียว (Customer 360)
- **US-15 (FN-15):** ถอนแทนลูกค้า — AC1: ต้องระบุเหตุผล+ช่องทาง · AC2: มีผลทันที ไม่ต้องอนุมัติ
- **US-16 (FN-16):** ดูรายการใกล้หมดอายุ ≤30 วัน — AC: เตือนไม่บล็อก · ต่ออายุได้
- **US-17 (FN-17):** ต่ออายุ — AC: เป็นคำขอใหม่อ้างเดิม ไม่แก้วันหมดอายุเดิม
- **US-18 (FN-18):** ดูประวัติ 1 รายการ — AC: timeline append-only มีเหตุผลทุกครั้ง
- **US-19 (FN-19):** ตัวจำลอง `/consent/resolve` — AC: ตอบ allowed+reason+JSON ฟิลด์ล็อก
- **US-20 (FN-20):** ตรวจคนไม่เคยถูกขอ — AC: `allowed:false · status:"never_asked"` (ไม่ใช่ 404/declined)

---

## Section 8 · Status & Lifecycle

### 8.1 Consent status (เก็บ 4 + คำนวณ 2 + resolve 1)
```
[pending] --เจ้าของยินยอม--> [granted] --daysLeft<0--> (expired*)
[pending] --เจ้าของปฏิเสธ--> [declined]
[pending] --เกินกำหนดตอบ--> (คำขอ expired: lapsed ≠ declined)
[granted] --ถอน--> [withdrawn]
[granted] --policyVer < currentVer--> (stale* : ต้องขอใหม่)
(ไม่มี record) --> never_asked  (เฉพาะผลลัพธ์ resolve)
```
`*` = สถานะคำนวณ (effStatus/policyStale/nearExpiry) ไม่เก็บใน DB

| State | Trigger | Next | หมายเหตุ |
|---|---|---|---|
| pending | สร้าง+ส่งคำขอ | granted/declined/expired | |
| granted | ยินยอมผ่าน recipient view | withdrawn / expired(คำนวณ) | |
| declined | ปฏิเสธรายข้อ | (terminal) | ≠ ไม่ตอบ |
| withdrawn | ถอน (มีผลทันที) | (terminal จนขอใหม่) | ไม่ต้องอนุมัติ |
| expired (คำนวณ) | expiresAt < วันนี้ | ต่ออายุ → คำขอใหม่ | ยังนับเป็นหลักฐาน |
| near-expiry (คำนวณ) | 0 ≤ daysLeft ≤ 30 | เตือน ไม่บล็อก | |
| never_asked | ไม่มี record (resolve) | — | allowed:false |

### 8.2 Request status
`draft → pending → answered` · หรือ `pending → expired` (เกิน 30 วัน)

### 8.3 Purpose status
`active → closed` (ปิดแล้วขอใหม่ไม่ได้ · consent เดิมคงอยู่)

---

## Section 9 · Business Rules + Validation (with Tags)

| Rule | กฎ | Tag | ใครเปลี่ยน + บ่อยแค่ไหน | ที่มา |
|---|---|---|---|---|
| BR-01 | triple key เจ้าของ×วัตถุประสงค์×ช่องทาง ไม่ซ้ำ (มีผลได้รายการเดียว) | **FIXED** | — | ✅ |
| BR-02 | ช่องทางรองรับ 5: email/SMS/LINE/phone/post | **CONFIGURABLE** | Admin · นานๆครั้ง | 🤖 |
| BR-03 | วัตถุประสงค์กำหนดช่องทางที่ใช้ได้เอง — ขอช่องทางนอกรายการไม่ได้ | **FIXED** | — | ✅ |
| BR-04 | default = ไม่อนุญาต (ไม่มี record = ส่งไม่ได้) | **FIXED** | — | ✅ |
| BR-05 | เอกสารนโยบายเป็นเวอร์ชัน · อัปโหลดใหม่ = ออกเวอร์ชันใหม่ · เวอร์ชันเดิมแก้ไม่ได้ | **FIXED** | — | ✅ (DECLARED-01: "อัปโหลด" ไม่ใช่ "แก้ข้อความ") |
| BR-06 | consent ผูกกับเวอร์ชันที่เจ้าของเห็นตอนเซ็น — เวอร์ชันใหม่ไม่ครอบคลุมอัตโนมัติ | **FIXED** | — | ✅ |
| BR-07 | สถานะ 5 ค่า + คำนวณ expired | **FIXED** | — | ✅ |
| BR-08 | ไม่ตอบ ≠ ปฏิเสธ (เกินกำหนด = คำขอหมดอายุ) | **FIXED** | — | ✅ |
| BR-09 | ถอนได้ทุกเมื่อ ไม่ต้องอนุมัติ มีผลทันที | **FIXED** | — | ✅ |
| BR-10 | ถอนต้องระบุเหตุผล + ช่องทางที่ลูกค้าแจ้ง | **FIXED** (บังคับ input) | — | ✅ |
| BR-11 | อายุความยินยอมตามวัตถุประสงค์ (default 24 เดือน) | **CONFIGURABLE** | Admin/DPO รายวัตถุประสงค์ 1–120 | ✅ |
| BR-12 | ใกล้หมดอายุ ≤30 วัน เตือน ไม่บล็อก | **CONFIGURABLE** | Admin · ค่าคงที่วันเตือน | 🤖 |
| BR-13 | ต่ออายุ = คำขอใหม่อ้างเดิม ไม่แก้วันหมดอายุเดิม | **FIXED** | — | ✅ |
| BR-14 | ปิดวัตถุประสงค์ = ห้ามคำขอใหม่ · consent เดิมอยู่ | **FIXED** | — | ✅ |
| BR-15 | หลักฐานครบ 5 อย่างทุก consent ที่ได้รับ | **FIXED** | — | ✅ |
| BR-16 | ประวัติ append-only เขียนในทรานแซกชันเดียวกับเปลี่ยนสถานะ · แก้/ลบไม่ได้ | **FIXED** | — | ✅ |
| BR-17 | ไม่มีการลบถาวร (consent/คำขอ/วัตถุประสงค์) | **FIXED** | — | ✅ |
| BR-18 | คำขอหนึ่งใบส่งซ้ำได้หลายครั้งหลายช่องทาง = รายการส่ง ไม่สร้างคำขอใหม่ | **FIXED** | — | ✅ |
| BR-19 | `/consent/resolve` ตอบ 200 เสมอ · never_asked → allowed:false (ไม่ใช่ 404) | **FIXED** | — | ✅ |
| BR-20 | สัญญาผลลัพธ์ `/consent/resolve` ล็อก — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายเดิม | **FIXED** | — | ✅ |
| BR-21 | ผู้เรียกแคช ≤5 นาที + ล้างทันทีเมื่อถอน | **CONFIGURABLE** (caller-side contract, ไม่ทำ UI) | ทีม integration | ✅ → §15 OQ-02 |
| BR-22 | `/consent/*` ต้องขึ้นทะเบียน Backend Enforcement Gate + ตรวจ 4 ขั้น | **FIXED** (external dependency) | — | ✅ → §15 OQ-04 |
| BR-CSQ-01..05 | event ยิงเข้า 7C Engine ผ่าน envelope · idempotency_key · mask restricted · reversal_of · ไม่ประกาศ OC/DC/SC | **FIXED** | — | ✅ (→ CSQ_BRIEF step 7) |

### 9.1 Validation Rules
| Field/Action | เงื่อนไข | ประเภท | ข้อความ |
|---|---|---|---|
| สร้างวัตถุประสงค์ | ต้องมี name + ≥1 channel + life 1–120 + เอกสาร | Prevent | บันทึกไม่ได้จนกรอกครบ |
| อัปโหลดเวอร์ชันใหม่ | ต้องแนบเอกสาร | Prevent | — |
| ส่ง recipient answer | ต้อง verified ก่อน | Prevent | "กรุณายืนยันตัวตนก่อนส่งคำตอบ" |
| ถอน | ต้องมีเหตุผล + ช่องทาง | Prevent | — |
| สร้างคำขอ | เลือกได้เฉพาะวัตถุประสงค์ status=active | Prevent | ปิดแล้วเลือกไม่ได้ |
| resolve never_asked | ไม่มี record | Trigger | `status:"never_asked"` reason อธิบาย |

### 9.5 สรุประดับความยืดหยุ่น
| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-02 | Admin Panel | รายการ enum ช่องทาง เปลี่ยนนานๆครั้ง | 🤖 AI-inferred → §15 OQ (ระดับ Admin ปล่อยผ่านได้ mark 🤖) |
| BR-11 | Admin Panel (รายวัตถุประสงค์) | อายุตั้งได้ต่อ purpose | ✅ (ตั้งบนฟอร์มจริง) |
| BR-12 | Admin Panel/Config | วันเตือน 30 คงที่ | 🤖 |
| BR-21 | Config (caller-side) | อายุแคช ≤5 นาที | ✅ ระบุใน PREBRIEF |
| ที่เหลือ (FIXED) | Phase 1 seed | logic compliance ห้าม hardcode ค่าที่เดียว | ✅ |
> ไม่มี rule ระดับ DYNAMIC/Engine ที่ AI เดา → ไม่มี escalation บังคับเพิ่มนอกเหนือ OQ ที่ list แล้ว

---

## Section 10 · Edge Cases

### 10.1 Edge Cases ที่ PREBRIEF ระบุ (☑ ยืนยัน)
- ☑ ยินยอมบางวัตถุประสงค์ (S-11) — บันทึกแยกข้อ
- ☑ ไม่ตอบ ≠ ปฏิเสธ (BR-08) — คำขอ expired
- ☑ never_asked (S-20) — ไม่ใช่ 404
- ☑ ออกเวอร์ชันใหม่ทำ consent เดิม stale (BR-06)
- ☑ ปิดวัตถุประสงค์แล้ว consent เดิมคงอยู่ (BR-14)

### 10.2 Edge Cases จาก AI Pattern Matching (☐ ให้ BA/dev ยืนยันที่ FRD/vibe-fix)
- ☐ **[FU]** อัปโหลดเอกสารไฟล์ใหญ่/ชนิดไม่รองรับ — validation ชนิด/ขนาด (ปัจจุบัน mock) — 🔴 กระทบ data → OQ
- ☐ **[CA]** ถอน+ตรวจสิทธิ์พร้อมกัน (race) — แคชผู้เรียกต้องล้างทันที (BR-21) — 🔴 กระทบสิทธิ์ → OQ
- ☐ **[ST]** consent granted แล้วปิด purpose — resolve ต้องตอบ "วัตถุประสงค์ปิด" (HTML จัดการแล้ว: `p.status==='closed'` → allowed:false)
- ☐ **[DI]** subject/purpose ถูกอ้างแต่ถูกลบต้นทาง — BR-17 ห้ามลบถาวร (mitigate)
- ☐ **[CL]** expiresAt คำนวณข้ามเขตเวลา / เดือนไม่เท่ากัน — ยืนยัน timezone rule ที่ FRD
- ☐ **[PM]** auditor พยายามแก้ข้อมูล — ต้องบล็อกจริง (HTML เป็น switcher เดโม) — OQ-05
- ☐ **[PD]** consent receipt PDF (E3) — deferred → §15 OQ-05/§13

---

## Section 11 · Impact / Regression
New Feature standalone — ไม่มี regression กับ feature เดิม (dep="") · Downstream impact ดู §12.1

---

## Section 12.1 · Value Stream & Downstream Impact ⭐

**Value Stream positioning:** Marketing consent gate — เป็น **ต้นน้ำของสิทธิ์การสื่อสาร** ทุกช่องทางการตลาด · standalone แต่เป็น dependency ของ feature ปลายทาง (แคมเปญ/ส่งข้อความ/จดหมายข่าว)

**Upstream:** รับ subject reference (ลูกค้า CUS-xxxx) จากทะเบียนลูกค้า (external ref) · ไม่มี trigger เอกสารต้นทาง

**Downstream Impact Map:**
| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าเปลี่ยน/ถอน |
|---|---|---|---|
| แคมเปญส่งข้อความ / จดหมายข่าว | ผล `/consent/resolve` (allowed + status) | ก่อนส่งทุกครั้ง | ถอน → resolve ตอบ false ทันที · caller ต้องล้างแคช ≤5 นาที (BR-21) |
| Backend Enforcement Gate (F143) | ทะเบียน endpoint `/consent/*` + review 4 ขั้น | deploy | ต้องขึ้นทะเบียนก่อน go-live (BR-22) — **hard dependency** |
| 7C Consequence Engine (F-CSQ-01) | event envelope (granted/declined/withdrawn/version_published/purpose_closed/renew/reconsent) | ทุก state change | reversal ส่ง event `reversal_of` (ถอน) — ไม่ลบผลเดิม |
| DSAR / consent receipt (อนาคต) | evidence + history | (deferred E3) | — |

> ⚠️ Downstream ทุกแถวตอบ "แล้วไงต่อ" ได้ · BR-22 = external dependency ที่ต้อง confirm timeline กับทีม Security → §15 OQ-04

---

## Section 12.3 · Existing System Reference
| Rule/สิ่งที่ต้องพึ่ง | มีอยู่แล้ว? | Reference |
|---|:--:|---|
| Backend Enforcement Gate (BR-22) | ✅ (plan F143 done ตาม prompt) | ต้องลงทะเบียน `/consent/*` + review 4 ขั้น |
| 7C Consequence Engine (CSQ) | ✅ | POST /csq/events (declare-only, CSQ_BRIEF step 7) |
| ทะเบียนลูกค้า (subject ref) | ⚠️ external | ใช้ CUS-xxxx เป็น ref เท่านั้น |
| Document store / running number | ❌ ไม่ใช้ | ไม่ใช่เอกสารธุรกรรม (ไม่มี doccfg) |

---

## Section 13 · Delivery Phases
- **Phase 1 · Feature Launch:** ทุก rule เป็น config/seed (channels, lifespan, warn-days = config table) · state machine consent/request/purpose · triple-key constraint · evidence+history append-only · `/consent/resolve` (contract ล็อก) · recipient view · CSQ hook declare-only · ขึ้นทะเบียน Backend Enforcement Gate
- **Phase 2 · Admin Panel:** จัดการ enum ช่องทาง (BR-02) · วันเตือนหมดอายุ (BR-12) · permission จริงต่อ role (แทน switcher เดโม)
- **Phase 3 · Rule Management:** — (ไม่มี rule DYNAMIC ที่ต้องการ rule engine ในรอบนี้)
- **Phase 4 · Engine Management:** — (n/a)
- **Deferred:** consent receipt PDF (E3) → wave DSAR / step 2

---

## Section 14 · Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation
- Config table: channels enum · default lifespan 24 (1–120) · warn-days 30 · request-timeout 30 วัน · caller cache TTL 5 นาที (ประกาศให้ caller) — **ห้าม hardcode ค่าที่เดียว**
- `/consent/resolve` response schema = **locked contract** (BR-20): `{subject, purpose, channel, allowed, status, found, reason, ...}` — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายเดิม · HTTP 200 เสมอ

### 14.2 ข้อกำหนดจาก Tag
- FIXED ส่วนใหญ่ → seed ตั้งแต่วันแรก · CONFIGURABLE (BR-02/11/12/21) → เตรียม config/admin ไม่ hardcode

### 14.3 Edge Cases สำคัญที่ต้อง handle
- อัปโหลดเอกสาร: validate ชนิด/ขนาดจริง (ตอนนี้ mock) · race ถอน↔resolve + cache invalidation (BR-21) · timezone ของ expiresAt

### 14.4 WARNING รอข้อสรุป
- วิธียืนยันตัวตนจริงในมุมมองผู้รับ (checkbox mock ปัจจุบัน) — **ห้ามเริ่ม implement วิธีจริงจนกว่า BA เคาะ** (§15 OQ-03)
- Permission enforcement จริงต่อ role (switcher เดโม) — OQ-05

### 14.5 Regression Scope
N/A (standalone)

### 14.6 Screen Inventory + UI Signals (หยาบ — ส่งต่อ FRD)

**สถาปัตยกรรม:** โมดูล ERP หน้าเดียว 4 แท็บ (hash route) + surface มุมมองผู้รับแยก + drawers/modals · default route = `#/consent/registry`

| # | หน้า/แท็บ | route (จาก HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) |
|---|---|---|---|---|---|
| P-01 | ทะเบียน | `#/consent/registry` | หน้ารายการ (default) | ทุก role | ตาราง triple + สถิติ + กรองทุกมิติ |
| P-02 | คำขอ | `#/consent/requests` | หน้ารายการ | เจ้าหน้าที่/DPO | ติดตาม/สร้าง/ส่งคำขอ |
| P-03 | วัตถุประสงค์ | `#/consent/purposes` | หน้ารายการ+สถิติ | เจ้าหน้าที่/DPO | จัดการ purpose + เวอร์ชันเอกสาร |
| P-04 | ตรวจสิทธิ์ | `#/consent/resolve` | เครื่องมือ (simulator, read-only) | ทุก role/dev | จำลอง `/consent/resolve` |
| P-05 | มุมมองผู้รับ | recipient view (mock ลิงก์ภายนอก) | หน้ายืนยัน (นอก ERP shell) | เจ้าของข้อมูล | อ่านเอกสาร → ยืนยันตัวตน → ยินยอมรายข้อ → เซ็น |

**Drawers/Modals (ในหน้า):** สร้างวัตถุประสงค์+อัปโหลด · ออกเวอร์ชันใหม่ · สร้างคำขอ (single-screen) · รายละเอียดคำขอ (ส่ง/ส่งซ้ำ/คัดลอกลิงก์/QR/ดาวน์โหลดเอกสาร) · รายละเอียดความยินยอม (หลักฐาน 5 + timeline + ต่ออายุ/ถอน) · Customer 360 · ถอน · ปิดวัตถุประสงค์ · รายละเอียดวัตถุประสงค์ (version list) · document viewer modal (เหนือ drawer, DSP-01)

**สรุปจำนวนหน้า:** ~5 surface หลัก (รายการ 3 + simulator 1 + recipient 1) + ~11 drawer/modal

**UI Signals ส่งต่อ FRD:**
- ❌ ไม่ใช่ Document/Transaction (archetype `is_document=false`) — ไม่มี approver/พิมพ์เอกสารทางการ/เลขรัน
- ❌ ไม่ใช่ wizard (single-screen create — LOCK-07)
- ✅ มี document viewer modal เหนือ drawer (z-tier DSP-01)
- ✅ recipient view = surface แยก (ไม่มี ERP sidebar) — mock ลิงก์ภายนอก
- ⚠️ role switcher = เดโม (FRD ต้องกำหนด permission จริง)
- pattern/CI/spec/px = หน้าที่ FRD 100% (BRD ไม่ตัดสิน)

### 14.7 Functions Cut (จาก FUNCTION_CHECKLIST — "ไม่รองรับ")
10 FN-40 (ต้องไม่มี) = §3.2 Out of Scope · ยืนยัน absent 10/10 (coverage report) · e2e assert เรนเดอร์จริงที่ step 5 (ผ่านแล้ว 32/32 ตาม memory)

---

## Section 15 · Open Questions (→ PROPOSALS_outbound.md step 12)

| # | คำถาม | สถานะ | หมายเหตุ |
|---|---|:--:|---|
| **OQ-01** | **[GOVERNANCE] BA sync PREBRIEF** BR-05/06 + S-01/02/09 + FN-01/02/09/10/11 ให้เป็นโมเดล "เอกสารอัปโหลด" | ⚠️ รอ BA | DECLARED-01 — จนกว่า sync ถือเป็น divergence ที่ประกาศ ไม่นับตก |
| **OQ-02** | BR-21 caller cache ≤5 นาที + ล้างเมื่อถอน — สัญญาฝั่งผู้เรียก (document ใน FRD API ไม่ทำ UI) | ⚠️ รอยืนยันทีม integration | |
| **OQ-03** | วิธียืนยันตัวตนจริงในมุมมองผู้รับ (ปัจจุบัน checkbox mock; PREBRIEF Part D [ASSUMED] ลิงก์/OTP/สแกนกระดาษ) | ⚠️ รอ BA เคาะ | ห้าม dev เดา |
| **OQ-04** | BR-22 `/consent/*` ขึ้นทะเบียน Backend Enforcement Gate (F143 done) + ตรวจ 4 ขั้น — confirm timeline/ขั้นตอนกับทีม Security | ⚠️ รอ Security | hard dependency ก่อน go-live |
| **OQ-05** | Permission enforcement จริงต่อ role (switcher เดโม) + consent receipt PDF (E3) deferred | ⚠️ รอ BA/PM | E3 → wave DSAR |
| **OQ-06** | เก็บ baseline ตัวชี้วัด §2.3 ก่อน launch | ⚠️ action ก่อน go-live | |

---

## Section 16 · Security & Compliance

### 16.1 Preset
**P6 (PII Sensitive — 15 controls)** + overlay compliance (P10 audit) — เหตุผล: feature จัดการข้อมูลส่วนบุคคล + ความยินยอมตาม PDPA ซึ่งต้อง audit-ready

### 16.2 Applicable Standards
PDPA (หลัก) · ISO 27001 (access/audit log) · หลักฐาน/ร่องรอยตามข้อกำหนดกฎหมายไทย

### 16.3 Control Checklist (สำคัญ)
| Control | Required | Note |
|---|:--:|---|
| Field-level access (PII) | ✓Must | subject/evidence เป็น PII |
| Audit trail append-only | ✓Must | BR-16/17 (มีในโมเดลแล้ว) |
| Data masking ก่อนส่ง CSQ | ✓Must | BR-CSQ-03 (mask restricted ที่ผู้ส่ง) |
| Immutable policy version | ✓Must | BR-05/06 |
| API contract lock + gate register | ✓Must | BR-19/20/22 |
| Role-based permission | ✓Must | §4 (ปัจจุบัน switcher เดโม → OQ-05) |
| Cache invalidation on withdraw | ✓Must | BR-21 |

### 16.4 Risk Statement
- **R-A** ส่งการตลาดหาคนที่ถอน/หมดอายุ → mitigate: default-deny (BR-04) + resolve gate (BR-19) + cache ≤5 นาที (BR-21)
- **R-B** consent ผูกเวอร์ชันผิด → mitigate: snapshot policyVersion (BR-06) + immutable version (BR-05)
- **R-C** หลักฐานถูกแก้/ลบ → mitigate: append-only + no hard delete (BR-16/17)
- **R-D** ข้อมูล PII รั่วผ่าน CSQ event → mitigate: mask ก่อนส่ง (BR-CSQ-03)

---

## Section 17 · Health Check

### 17.1 SLA
| Step | เวลาควบคุม | Owner |
|---|---|---|
| SLA-Withdraw | ถอนมีผลทันที (≤2 นาที รับสาย→บันทึก) | เจ้าหน้าที่ |
| resolve response | ตอบ 200 ทุกครั้ง (< X ms — กำหนดที่ FRD) | ระบบ |
| cache TTL | ≤ 5 นาที (BR-21) | caller |

### 17.2 Control Points
map จาก §16: audit log ทุก state change · gate register check · mask check ก่อน emit

### 17.3 KPI
- **KPI-Compliance:** % send ที่ผ่าน resolve ก่อนส่ง (target ≥99%) · % consent หลักฐานครบ (100%)
- **KPI-Quality:** จำนวนส่งผิด (target 0)
- **KPI-Conversion:** % ต่ออายุก่อนหมด (≥70%)
- **KPI-Volume:** จำนวนคำขอ/เดือน · จำนวน consent active

### 17.4 Threshold
| ตัว | Min | Max | Action when breached |
|---|---|---|---|
| ส่งผิด (ส่งหา non-granted) | — | 0 | alert Security + DPO ทันที |
| resolve error rate | — | 0% (ต้อง 200 เสมอ) | เข้าข่ายละเมิด contract → incident |
| consent ไม่มีหลักฐานครบ | — | 0 | บล็อก record |

### 17.5 Throughput
resolve = call ก่อนส่งทุก message → capacity ต้องรองรับ campaign burst (baseline เก็บก่อน launch, stress point กำหนดที่ FRD)

---

## Section 18 · Monitoring

- **18.1 Reports Overview:** Performance (resolve latency/volume) · Compliance/Closing (สรุปสถานะ consent, ใกล้หมดอายุ) · Anomaly (ส่งผิด, resolve non-200) · Transaction (log คำขอ/การส่ง/ถอน)
- **18.2 Dashboard Widgets:** สถิติทะเบียน (ยินยอมอยู่/ถอน/ใกล้หมดอายุ/ทั้งหมด — มีบนจอแล้ว) · %ครอบคลุมต่อวัตถุประสงค์ · rate ผ่าน resolve
- **18.3 Performance:** resolve p95 latency · call volume
- **18.4 Closing/Compliance:** รายเดือน — active/withdrawn/expired/coverage
- **18.5 Anomaly:** ส่งผิด (>0) · resolve error (>0) · consent หลักฐานไม่ครบ
- **18.6 Transaction:** timeline append-only ต่อ consent (มีในโมเดล)

### 18.7 Cross-Section Coverage Check
- ✅ BC ทุกข้อ (BR-01…22) มี edge case/scenario cover (§10 + FN matrix)
- ✅ Control runtime (§16) มี control point (§17.2)
- ✅ Metric (§17.3) มี widget/report (§18)

---

## Section 14.8 · AI Review Report (Quality Gate)

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full
BRD: BRD-F-MKT-CONSENT — ความยินยอม PDPA
ประเภท: New Feature · วันที่: 2026-09-13
═══════════════════════════════════════
✅ C01 Business Objective วัดผลได้ (§2.3 มี baseline/target/แหล่งวัด)
✅ C02 User Roles ครบ (§4)
✅ C05 ไม่มี Story ที่มีคำว่า "และ"
✅ C10 ทุก rule ที่มีตัวเลข/เงื่อนไข ติด Tag (§9)
✅ C13 Edge Cases ครบหมวด (§10.1/10.2)
✅ C18 WARNING ทุกข้อมีแผน (→ §15 OQ)
✅ C19 Section 14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ · ไม่มี scope drift เงียบ
✅ C21 Value Stream §12.1 upstream + downstream map ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 ตัวชี้วัด §2.3 มีคู่ใน §17.3
✅ C23 §9.5 marker 🤖/✅ ครบ · ไม่มี 🤖+DYNAMIC/Engine ค้าง
✅ PE01 COSO ทุก step (§5 — no approval chain by LOCK-04, ระบุเหตุ)
✅ PE02 SoD n/a (ไม่มี approval) — default-deny+evidence แทน
✅ PE03 Security Preset P6 + controls (§16)
✅ PE04 SLA+KPI+Threshold ครบ (§17)
✅ PE05 Cross-section coverage ผ่าน (§18.7)

DIVERGENCES (ประกาศ ไม่นับตก): DECLARED-01 (content model), DECLARED-02 (DOA false positive)
OPEN QUESTIONS: 6 (OQ-01…06) — ยกเข้า PROPOSALS step 12

SUMMARY: ผ่าน 16/16 core + 5/5 PE
สถานะ: ✅ APPROVED — พร้อมเข้า frd-generator-v6
```

**Next step:** BRD APPROVED → step 7 `frd-generator-v6` (+ `csq-declaration` ออก `CSQ_BRIEF` หลัง step 7)
