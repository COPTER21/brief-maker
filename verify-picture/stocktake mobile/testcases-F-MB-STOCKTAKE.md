# AI Test Cases — F-MB-STOCKTAKE

## 0. Document Control

| Field | Value |
|---|---|
| Feature ID | F-MB-STOCKTAKE (เสนอ; อ้างอิง F084 / F-WH-STOCKTAKE) |
| Feature | Stocktake ตรวจนับใหญ่บนมือถือ — CUBE Mobile · Warehouse / Inventory |
| Version | 0.1 |
| สถานะ | DRAFT — แผนทดสอบ (planned) ยังไม่มีการรันหรือผลทดสอบใด ๆ |
| Owner | เตชินท์ เสยกระโทก (BA) |
| วันที่ | 2026-11-04 |
| Workflow task | 2.1 Spec Pack — ใช้รันใน 4.2 (agent บน RC) และ 4.3 (UAT) |
| Source | `FACTS.md` · `1_discovery/prebrief/PREBRIEF_F-MB-STOCKTAKE.md` · `1_discovery/prebrief/MOBILE_SPEC_NOTES.md` (seed TC-MB-01..11) · `1_discovery/prototype-qc/02_qc/_BROWSER_QC_CHECKLIST.md` (B-01..B-07, DEF/UX) · web baseline `feature-brief/stockable/testcase_qa/testcases-F-WH-STOCKTAKE.md` + `04_frd/FRD_Pack/02_API.md` + `09_declarations/DOA_BRIEF_F-WH-STOCKTAKE.md` |
| Checklist page (UAT) | `testcase-F-MB-STOCKTAKE.html` (หน้าเดียว, บันทึกผลในเครื่อง, export MD/CSV) |

> ผลทดสอบเว็บ (F-WH-STOCKTAKE) และผล Browser QC ของ prototype **ไม่นับ** เป็นผลของมือถือ — B-01..B-07 ถูกนำมาเป็น regression check เท่านั้น ทุกเคสต้องรันใหม่บนแอปจริงที่ต่อ BFF sandbox

## 1. Meta

| Field | Value |
|---|---|
| Run target | mobile-app RC build (preview / `cube-mobile-release`) ต่อ BFF **sandbox** — ไม่ใช่ HTML prototype และไม่ใช่ mock `store.ts` |
| Screens | S-01 รายการรอบ · S-02 สร้างรอบ · S-03 รายละเอียดรอบ · S-04 ใบนับ/ใบนับซ้ำ · S-05 ผลต่าง/อนุมัติ/F082 · S-06 ประวัติ · SH-02 Assign · SH-03 Approval chain |
| Endpoints | API-01..API-13 (`/m/v1/stocktake-rounds…`, `/m/v1/locations`, `/m/v1/people`) — path/field สุดท้าย lock ใน 3.1 Tech Plan |
| Automation | Maestro `mobile-app/.maestro/` — flow เดิม `07_stocktake.yaml` ใช้ข้อมูล mock (ST-2026-00x) ต้องปรับให้ใช้ DS ด้านล่าง + flow ใหม่ `10_stocktake_live.yaml` (ดู Additions) ; การตรวจ response/BFF log ทำโดย agent ผ่าน HTTP client ด้วย token ของบัญชี sandbox |
| Priority rule | **High** = ทุกเคสที่แตะ blind data, lock/snapshot, self-approval/segregation, F082 ack, idempotency/timeout (ตาม FACTS) ; Medium = flow/validation/state ทั่วไป |
| Run location | `4.2` = agent บน RC + sandbox (UI ผ่าน Maestro + ตรวจ API/BFF log/core audit) · `4.3` = UAT คนจริงตาม role บนเครื่องจริง |

> ทุกเคสเริ่มด้วย `subflows/start.yaml` (clearState + login บัญชี sandbox ตาม role) เว้นแต่ระบุให้ทำต่อเนื่อง ข้อมูลต้อง seed บน sandbox ตาม Data Sets ก่อนรัน ตัวเลขใน Expected อ้างจาก DS ไม่ใช่ค่า mock ใน `data.ts`
>
> **ปุ่มลอย MOCK / BLANK:** build จาก `develop` อาจยังมีปุ่มลอยตัวอย่าง (`applyStocktakeSample`) — ต้องตั้งเป็น **BLANK** หรือใช้ build ที่ถอดปุ่มแล้ว ถ้าหน้าจอตรวจนับเปลี่ยนตามปุ่ม หรือเห็นรอบ `ST-2026-00x` จาก mock = FAIL. Production ต้องไม่มี persona switcher (web LD-06) — ตัวตนมาจาก `GET /m/v1/me`

## 2. Sandbox Accounts

ข้อมูลบัญชีจริง (email/password) อยู่ใน env ของ `.maestro/run.sh` (`E2E_*`) และ vault ของ QA เท่านั้น **ห้ามเขียนลงเอกสารนี้** — การจัดเตรียมรอ OQ-MB-07

| Key | Role | บุคคล (ตาม prototype) | ใช้ทำอะไร |
|---|---|---|---|
| ACC-CNT | counter | กิตติพงษ์ ใจดี · ผู้นับ | นับรอบ 1 แบบ blind |
| ACC-RCN | recounter | พิมพ์ดาว ศรีสุข · ผู้นับซ้ำ | นับรอบ 2 แบบ blind (ต้องไม่ใช่ ACC-CNT) |
| ACC-SUP | supervisor | นลิน วัฒนา · หัวหน้าคลัง (ผู้จัดการคลัง) | สร้าง/freeze/assign, ดูผลต่าง, ส่งอนุมัติ, F082 draft; ถูกเลือกเป็น DOA slot 1 ได้ (ดู Contradictions C-03) |
| ACC-APR | approver | อรทัย ตั้งมั่น · ผู้อนุมัติ (ผู้อำนวยการคลัง) | DOA slot 2 อนุมัติ/ไม่อนุมัติ |
| ACC-AUD | auditor | — (รอ OQ-MB-07) | อ่านประวัติอย่างเดียว |
| ACC-OUT | counter (ไม่ได้รับมอบหมาย) | ผู้ใช้คลังอีกคน — รอ OQ-MB-07 | negative: ไม่ใช่ assignee, ไม่มีงาน |
| ACC-NOP | ไม่มีสิทธิ์ stocktake | — | negative: 403 / ไม่เห็นเมนู |

## 3. Data Sets (sandbox)

ทุก DS ใช้คลังทดสอบของตัวเอง (`WH-T*`) เพื่อไม่ให้ lock ของเคสหนึ่งชนอีกเคส แต่ seed สินค้าเหมือนกันเพื่อให้ตัวเลข expected คงที่: **ITM-001 ปั๊มน้ำ** (เครื่อง) on-hand 12, unit cost 25,000 บาท · **ITM-002 วาล์ว** (ชิ้น) on-hand 20, unit cost 1,200 บาท. Threshold policy version ปัจจุบัน = **2** (effective 2026-09-01). DOA matrix sandbox ตาม `DOA_BRIEF_F-WH-STOCKTAKE.md` §3: 0–19,999 = 1 ขั้น (ผู้จัดการคลัง) · 20,000–199,999 = 2 ขั้น (ผู้จัดการคลัง → ผู้อำนวยการคลัง) · ≥200,000 = 3 ขั้น — `[DEFAULT — รอยืนยัน]`

| Set | Values | ใช้ใน |
|---|---|---|
| DS-A | รอบ **ร่าง** `ST-MB-A01` ชื่อ “ตรวจนับ WH-T1 โซน A พ.ย.” scope `WH-T1-A` 2 บรรทัด (ITM-001, ITM-002) supervisor ACC-SUP ; รอบร่าง `ST-MB-A02` scope `WH-T3E` (ตำแหน่งที่ไม่มีสินค้า) ; คลัง/โซน/ตำแหน่งใน `/m/v1/locations` ≥ 10 รายการให้ค้นหาได้ | TC-MST-01–05, 07, 27 |
| DS-B | **scope ซ้อน**: รอบ `ST-MB-B01` สถานะ counting (lock active) scope `WH-T1-B` ; รอบร่าง `ST-MB-B02` scope `WH-T1` (แม่ของ WH-T1-B) ; รอบร่าง `ST-MB-B03` scope `WH-T1-B` (ซ้ำตรง) ; รอบร่าง `ST-MB-B04` scope `WH-T2` (ไม่ซ้อน — control) | TC-MST-06, 22 |
| DS-C | **นับรอบ 1 เกิน threshold**: รอบ `ST-MB-C01` frozen + assign รอบ 1 = ACC-CNT (counting) scope `WH-T3` snapshot 12 / 20 ; ผลนับที่จะกรอก ITM-001 = **9**, ITM-002 = **20** → abs(diff) = 3 > 2 → recount ; ผลนับซ้ำ (ACC-RCN) = **11**, **20** ; รอบ `ST-MB-C02` (scope `WH-T4`, counting, ACC-CNT) สำหรับ **boundary** กรอก **10**, 20 → abs(diff) = 2 = threshold → ไม่ recount | TC-MST-08–18 |
| DS-D | **DOA 2 ขั้น**: ผลจาก DS-C (count1 9/20, count2 11/20 → final diff −1 / 0, มูลค่า abs = 1 × 25,000 = **25,000 บาท** → set 2) ; รอบ `ST-MB-D01` สถานะ review (ยังไม่ส่งอนุมัติ) ; รอบ `ST-MB-D02` และ `ST-MB-D03` สถานะ pending chain ถูก freeze แล้ว slot 1 = ACC-SUP, slot 2 = ACC-APR, step ปัจจุบัน = 1 ; counter = ACC-CNT, recounter = ACC-RCN ทุกรอบ | TC-MST-15, 19–23 |
| DS-E | **F082 ใช้ไม่ได้**: รอบ `ST-MB-E01` สถานะ approved (lock active, scope `WH-T7`) + sandbox fault flag F082 = `unavailable` (BFF คืน 502 `ERR_F082_UNAVAILABLE`) และโหมด `timeout` (F082 ack ช้ากว่า client timeout แต่สำเร็จฝั่ง core) | TC-MST-25 |
| DS-F | **F082 ปกติ**: รอบ `ST-MB-F01` approved (scope `WH-T8`) ; รอบ `ST-MB-F02` closed แล้ว มี adj draft (`adj_id` จาก sandbox F082) ; รอบ `ST-MB-F03` สถานะ review (ยังไม่ approved) | TC-MST-24, 26 |
| DS-G | **ประวัติ/ขอบเขต**: `ST-MB-F02` มี audit ครบ ≥ 10 event (สร้าง → freeze → assign → submit ×2 → submit-approval → approve ×2 → F082 ack → closed) ; ในบริษัทเดียวกันมีงาน Cycle Count/ABC ใน core อย่างน้อย 1 รายการ | TC-MST-27, 28 |
| DS-H | **ว่าง**: ACC-OUT ไม่มีรอบที่ได้รับมอบหมาย ; ACC-NOP ไม่มีสิทธิ์ stocktake ; บริษัทที่ไม่มีรอบใด ๆ เลย (สำหรับ “ไม่มีงาน”) | TC-MST-03, 29, 33 |
| DS-I | **ทศนิยม/จำนวนมาก**: รอบ `ST-MB-I01` counting ACC-CNT มี ITM-008 เม็ดพลาสติก PP (กก.) on-hand 1,250 + บรรทัดรวม N บรรทัด (N = ค่าสูงสุดตาม OQ-MB-05; ก่อนปิด OQ ใช้ 60) | TC-MST-12, 36 |
| DS-J | **Fault / config toggles ของ sandbox** (รอ OQ-MB-06/07): (1) หน่วง response API-05/08/09 เกิน client timeout แต่ commit สำเร็จ, (2) หน่วงแล้ว **ไม่** commit, (3) revoke session → 401, (4) บังคับ `426 APP_UPDATE_REQUIRED` (min app version), (5) เปลี่ยน threshold policy เป็น version ใหม่ = 5 หลัง freeze, (6) DOA config ที่ไม่มี tier ครอบมูลค่า → `BR_DOA_NO_TIER`, (7) ช่องทางสร้าง stock movement ใน core sandbox (ใช้ทดสอบ lock/snapshot) | TC-MST-05, 07, 15, 19, 25, 31–34 |

## 4. Coverage Manifest

| FN | Function | TC |
|---|---|---|
| FN-01 | ค้นหา/กรองรอบ + เลือกพื้นที่ (picker) | TC-MST-01–03 |
| FN-02 | รายการ Item/Location soft-reference | TC-MST-04 |
| FN-03 | freeze lock เฉพาะ scope + กันรอบซ้อน | TC-MST-05–06 |
| FN-04 | snapshot ณ freeze time immutable | TC-MST-07 |
| FN-05 | มอบหมายผู้นับ / ผู้นับซ้ำ (คนจริง) | TC-MST-08–09 |
| FN-06 | blind count ทั้ง UI และ response | TC-MST-10–11 |
| FN-07 | กรอกจำนวน + ส่งเฉพาะ assignee | TC-MST-12–14 |
| FN-08 | server คำนวณผลต่างด้วย threshold version (`>`) | TC-MST-15–16 |
| FN-09 | recount คนละคน, ผลรอบ 2 = final | TC-MST-17–18 |
| FN-10 | DOA submit / decide / reject reason / no self-approval | TC-MST-19–23 |
| FN-11 | F082 draft ครั้งเดียว, ปิดรอบเมื่อได้ ack | TC-MST-24–26 |
| FN-12 | ขอบเขตรอบนับใหญ่ + ประวัติตามสิทธิ์ | TC-MST-27–28 |
| FN-13 | สถานะหน้าจอ/เครือข่าย/401/403/409/426/timeout/ร่าง session | TC-MST-29–36 |

## 5. Test Cases

### TC-MST-01 — รายการรอบ: ค้นหา กรองสถานะ และล้างตัวกรอง

- Priority: Medium
- FN: FN-01
- Trace: S-01, API-01, BR-01
- Role/Account: ACC-SUP
- Precondition: DS-A, DS-B seed แล้ว
- Steps:
  1. เปิดเมนู “ตรวจนับใหญ่” → S-01 ตรวจ KPI 4 ช่อง และกลุ่ม “รอคุณ”
  2. พิมพ์ค้นหา `ST-MB` แล้ว **แตะ chip “ปิดรอบแล้ว” ครั้งเดียวทันที** (ไม่ปิดคีย์บอร์ดก่อน)
  3. แตะ “ล้างตัวกรอง”
- Expected: ขั้น 1 รายการ/KPI ตรงกับ API-01 (`my_action` ต่อแถว — รอบที่ต้องลงมือขึ้นกลุ่ม “รอคุณ”); ขั้น 2 chip ติดตั้งแต่แตะครั้งแรกและยังอยู่ในจอ (regression **UX-B01**), ผลว่างแสดง “ไม่พบรอบที่ตรงกับตัวกรอง” + ปุ่มล้าง (ต่างจาก empty “ไม่มีงาน”); ขั้น 3 คำค้นและ chip ถูกล้าง รายการกลับมาครบ; ไม่มีรอบ mock `ST-2026-00x`
- Runs in: 4.2 (Maestro `10_stocktake_live.yaml`) · 4.3
- Seed/QC: TC-MB-01, B-01, UX-B01

### TC-MST-02 — สร้างรอบ: เลือกคลัง/โซน/ตำแหน่งแบบค้นหาและกดสร้างซ้ำไม่เกิดรอบซ้ำ

- Priority: High
- FN: FN-01
- Trace: S-02, API-02, API-11, BR-01, BR-08
- Role/Account: ACC-SUP
- Precondition: DS-A (locations ค้นหาได้)
- Steps:
  1. S-01 แตะ “สร้างรอบ” → S-02 กรอกชื่อรอบ
  2. ในช่องพื้นที่ พิมพ์ `WH-T2` เลือกผลจาก picker (API-11 `type=stock_scope`)
  3. ตรวจสรุป scope ก่อนยืนยัน แล้วแตะ “สร้าง” 3 ครั้งติดกันเร็ว ๆ
  4. ตรวจ BFF log / core
- Expected: picker แสดงผลจาก API-11 จริง (ไม่ใช่ `LOCATIONS` ใน `data.ts`); สรุป scope แสดงคลัง/โซน/ตำแหน่งชัดก่อนยืนยัน; ปุ่ม disable ระหว่างส่ง; core มีรอบใหม่ **1** รอบ สถานะ “แบบร่าง” (`draft`); request ทุกครั้งใช้ `Idempotency-Key` เดียวกัน (ถ้ามี retry) ; toast สำเร็จ 1 ครั้ง; รอบใหม่ขึ้นใน S-01
- Runs in: 4.2 (UI + BFF log) · 4.3 (ขั้น 1–3)
- Seed/QC: TC-MB-01

### TC-MST-03 — สร้างรอบ: ข้อมูลไม่ครบ, picker ไม่พบผล และผู้ไม่มีสิทธิ์

- Priority: Medium
- FN: FN-01
- Trace: S-02, API-02, API-11, BR-01
- Role/Account: ACC-SUP, ACC-CNT
- Precondition: DS-A, DS-H
- Steps:
  1. ACC-SUP เปิด S-02 เว้นชื่อรอบหรือพื้นที่ แล้วกด “สร้าง”
  2. พิมพ์คำค้นพื้นที่ที่ไม่มีอยู่ `ZZZ-999`
  3. login ACC-CNT เปิด S-01 ; agent เรียก API-02 ด้วย token ACC-CNT
- Expected: ขั้น 1 ไม่สร้างรอบ ระบุช่องที่ขาด (`ERR_REQUIRED_FIELD` → “กรุณาระบุชื่อรอบนับและพื้นที่นับ”), sheet ยังเปิด ค่าที่กรอกยังอยู่; ขั้น 2 empty “ไม่พบพื้นที่ที่ตรงกับคำค้น”; ขั้น 3 ACC-CNT ไม่เห็นปุ่มสร้าง และ API ตอบ 403 `ERR_INSUFFICIENT_ROLE`
- Runs in: 4.2 · 4.3 (ขั้น 1–2)
- Seed/QC: —

### TC-MST-04 — รายการ Item/Location ของรอบแบบ soft-reference

- Priority: Medium
- FN: FN-02
- Trace: S-03, S-04, API-06, BR-01
- Role/Account: ACC-SUP
- Precondition: DS-C (`ST-MB-C01` frozen) ; sandbox เปลี่ยนชื่อ ITM-002 ใน master หลัง freeze เป็น “วาล์ว (รุ่นใหม่)”
- Steps:
  1. เปิด `ST-MB-C01` tab “ใบนับ”
  2. ตรวจการจัดกลุ่มตามตำแหน่ง และข้อมูลต่อบรรทัด
- Expected: แสดงแนวตั้งกลุ่มตามตำแหน่ง แต่ละบรรทัดมี รหัส / ชื่อสินค้า / UoM / ตำแหน่ง ครบ 2 บรรทัดตาม snapshot; บรรทัดอ้าง item/location แบบ soft-reference (รหัสคงเดิม) การเปลี่ยน master ภายหลังไม่ทำให้บรรทัดหาย/เปลี่ยนจำนวน (การแสดงชื่อเดิมหรือใหม่ตาม 3.1 Tech Plan); ไม่มีตารางกว้างที่ต้อง scroll แนวนอน
- Runs in: 4.2 · 4.3
- Seed/QC: TC-MB-01

### TC-MST-05 — Freeze สำเร็จ: lock เฉพาะ scope ของรอบ

- Priority: High
- FN: FN-03
- Trace: S-03, API-03, BR-01, BR-02
- Role/Account: ACC-SUP
- Precondition: DS-A (`ST-MB-A01` draft, scope `WH-T1-A`) ; DS-J(7) สร้าง movement ได้
- Steps:
  1. เปิด `ST-MB-A01` กด “ล็อกพื้นที่” → กล่องยืนยันแสดง scope → ยืนยัน
  2. agent สร้าง movement ใน core ที่ `WH-T1-A` (ITM-001) และที่ `WH-T2`
  3. แตะปุ่มล็อกซ้ำ / ส่ง API-03 ซ้ำด้วย key เดิม
- Expected: ขั้น 1 สถานะ “ล็อกแล้ว” + เวลา freeze; request มี `expected_version` + `Idempotency-Key`; ขั้น 2 movement ใน `WH-T1-A` ถูกปฏิเสธ (lock), movement ใน `WH-T2` สำเร็จ (lock เฉพาะ scope); ขั้น 3 ไม่เกิด freeze/snapshot ซ้ำ ได้ผลเดิม; audit มี event freeze 1 ครั้ง
- Runs in: 4.2 (ต้องใช้ core sandbox) · 4.3 (ขั้น 1)
- Seed/QC: TC-MB-02

### TC-MST-06 — Freeze ถูกปฏิเสธ: scope ซ้อน, scope ว่าง และ version เก่า

- Priority: High
- FN: FN-03
- Trace: S-03, API-03, BR-01, BR-08
- Role/Account: ACC-SUP (2 เครื่อง/2 session)
- Precondition: DS-B, DS-A (`ST-MB-A02` scope ไม่มีสินค้า)
- Steps:
  1. freeze `ST-MB-B02` (scope แม่ `WH-T1`) แล้ว `ST-MB-B03` (scope เดียวกัน `WH-T1-B`)
  2. freeze `ST-MB-B04` (`WH-T2`)
  3. freeze `ST-MB-A02`
  4. เปิด `ST-MB-B04` อีกรอบบน session A และ B (version เดียวกัน) — A แก้ไข/freeze สำเร็จก่อน แล้ว B กด freeze
- Expected: ขั้น 1 ทั้งสองถูกปฏิเสธ `ERR_SCOPE_OVERLAP` (“พื้นที่นี้ทับซ้อนกับรอบนับที่กำลังใช้งาน”) สถานะยังเป็นร่าง ไม่มี snapshot; ขั้น 2 สำเร็จ; ขั้น 3 `ERR_SCOPE_EMPTY` ไม่ lock; ขั้น 4 B ได้ 409 `ERR_STALE_DATA` → แอปแสดง “ข้อมูลเปลี่ยนแล้ว กรุณาโหลดใหม่” + refresh, ไม่แสดงสำเร็จ; ไม่มี lock ค้างจากคำขอที่ล้มเหลว
- Runs in: 4.2 · 4.3 (ขั้น 1–3)
- Seed/QC: TC-MB-02

### TC-MST-07 — Snapshot ณ เวลา freeze เดียว และแก้ย้อนหลังไม่ได้

- Priority: High
- FN: FN-04
- Trace: S-03, API-03, API-06, BR-02, BR-04
- Role/Account: ACC-SUP
- Precondition: ต่อจาก TC-MST-05 (`ST-MB-A01` frozen) ; DS-J(7) มี movement ก่อน freeze 1 รายการ และพยายามสร้างหลัง freeze
- Steps:
  1. agent เรียก API-06 (+`/variance`) ด้วย token ACC-SUP ตรวจ snapshot
  2. เปลี่ยน on-hand/cost ใน core sandbox (ผ่านทางที่ไม่ติด lock เช่น revaluation ถ้ามี) แล้วเรียกซ้ำ
  3. agent พยายามแก้ snapshot ผ่าน API ใด ๆ (เช่น freeze ซ้ำ / PATCH ถ้ามี)
- Expected: snapshot ทุกบรรทัดมี watermark/เวลาเดียวกัน = freeze_at, ค่า 12 / 20, unit cost 25,000 / 1,200, threshold version = 2 (eff 2026-09-01) ผูกกับรอบ; movement ก่อน freeze ถูกนับใน snapshot, หลัง freeze ไม่ปน; ขั้น 2 snapshot ไม่เปลี่ยน; ขั้น 3 ถูกปฏิเสธ snapshot immutable; แอปไม่คำนวณ/เก็บ snapshot เอง
- Runs in: 4.2 เท่านั้น (API/core)
- Seed/QC: TC-MB-02

### TC-MST-08 — มอบหมายผู้นับรอบ 1 จากรายชื่อคนจริง

- Priority: Medium
- FN: FN-05
- Trace: S-03, SH-02, API-04, API-12, BR-03
- Role/Account: ACC-SUP
- Precondition: รอบ frozen ที่ยังไม่มี assignee (เช่น `ST-MB-B04` หลัง TC-MST-06 ขั้น 2)
- Steps:
  1. เปิดรอบ แตะ “มอบหมาย” → SH-02
  2. ค้นหาชื่อ “กิตติ” ; ลองกดยืนยันโดยยังไม่เลือกใคร
  3. เลือก ACC-CNT → ยืนยัน
- Expected: SH-02 แสดงรายชื่อจาก API-12 (`for=stocktake_counter&round_id=`) พร้อมชื่อ/ตำแหน่ง ไม่รวมคนไม่มีสิทธิ์ (ACC-NOP ไม่อยู่ในรายการ); ไม่เลือกใคร → ปุ่มยืนยัน disabled หรือแจ้งให้เลือก; ยืนยันแล้วรอบเป็น “กำลังนับ” แสดงผู้รับงาน = กิตติพงษ์; ACC-CNT เห็นรอบนี้ในกลุ่ม “รอคุณ”
- Runs in: 4.2 · 4.3
- Seed/QC: TC-MB-03

### TC-MST-09 — มอบหมายผู้นับซ้ำ: ตัดผู้นับรอบ 1 ออก และ server ปฏิเสธคนเดิม

- Priority: High
- FN: FN-05
- Trace: S-03, SH-02, API-04, API-12, BR-03, BR-04
- Role/Account: ACC-SUP, ACC-CNT
- Precondition: `ST-MB-C01` หลัง TC-MST-17 ขั้น 1 (สถานะ “รอนับซ้ำ” ก่อนมอบหมาย, count1 โดย ACC-CNT)
- Steps:
  1. ACC-SUP เปิด SH-02 สำหรับรอบ 2
  2. agent เรียก API-04 `{count_round:2, person_id: ACC-CNT}`
  3. agent เรียก API-04 ด้วย token ACC-CNT
- Expected: ขั้น 1 รายชื่อไม่มีกิตติพงษ์ (regression B-03); ขั้น 2 422 `BR_RECOUNT_SAME_PERSON` (“ผู้นับซ้ำต้องเป็นคนละคนกับผู้นับครั้งแรก”); ขั้น 3 403 `ERR_INSUFFICIENT_ROLE`; สถานะรอบไม่เปลี่ยน
- Runs in: 4.2 · 4.3 (ขั้น 1)
- Seed/QC: B-03

### TC-MST-10 — Blind count บนหน้าจอ: ผู้นับไม่เห็นยอดระบบ/ต้นทุน/ผลต่าง

- Priority: High
- FN: FN-06
- Trace: S-04, S-05, API-06 (blind DTO), BR-03
- Role/Account: ACC-CNT
- Precondition: DS-C (`ST-MB-C01` counting, ACC-CNT)
- Steps:
  1. เปิด `ST-MB-C01` → S-04 ตรวจทุกบรรทัด
  2. แตะ tab “ผลต่าง” และ “ประวัติ”
  3. กรอก 9 / 20 ส่ง (ยืนยัน) แล้วดูหน้ารอบ, S-01 และ toast
- Expected: ขั้น 1 เห็นเฉพาะ รหัส/ชื่อ/UoM/ตำแหน่ง/ช่องกรอก **ไม่มี** ยอดตั้งต้น, จำนวนระบบ, ต้นทุน, มูลค่า, ผลต่าง, threshold (regression B-02); ขั้น 2 ผลต่างแสดง “ไม่มีสิทธิ์ดูผลต่าง” ไม่มีตัวเลข, ประวัติไม่มีตัวเลขยอด/ผลต่าง; ขั้น 3 หลังส่งเห็นเพียง “ส่งผลนับ … แล้ว” และสถานะงานของตนเสร็จ — **ต้องไม่**เห็นว่าเกินเกณฑ์/ต้องนับซ้ำ หรือผลต่างใด ๆ (ดู Contradictions C-01)
- Runs in: 4.2 (Maestro `assertNotVisible`) · 4.3
- Seed/QC: TC-MB-03, B-02

### TC-MST-11 — Blind DTO: response ของผู้นับ/ผู้นับซ้ำไม่มีข้อมูลต้องห้าม

- Priority: High
- FN: FN-06
- Trace: API-06 (blind DTO), API-01, API-10, BR-03, BR-07
- Role/Account: ACC-CNT, ACC-RCN
- Precondition: DS-C ก่อนและหลังส่งรอบ 1 ; หลัง assign recount ให้ ACC-RCN
- Steps:
  1. agent เรียก API-06 `GET /m/v1/stocktake-rounds/{C01}` ด้วย token ACC-CNT ; เก็บ raw JSON (รวม `meta`, headers)
  2. เรียก `/variance` ด้วย token ACC-CNT และ ACC-RCN
  3. เรียก API-01 และ API-10 ด้วย token ACC-CNT
  4. ทำซ้ำขั้น 1 ด้วย ACC-RCN (รอบ 2) และเรียกซ้ำแบบ `If-None-Match` (ETag/304)
  5. ค้น app log / crash breadcrumb ของ RC ในช่วงทดสอบ
- Expected: ขั้น 1, 3, 4 สำเร็จด้วย blind DTO; ขั้น 2 403 ไม่มี body ข้อมูลตัวเลข
- Must NOT appear (ทุก response ของ counter/recounter, ทุกระดับ nested, ใน `data` และ `meta`): `system_qty` / `on_hand` / snapshot qty, `unit_cost` / ราคา / มูลค่า, `diff` / `variance` / `value_diff`, `absolute_variance_value`, `threshold` / `threshold_version` / threshold result / `recount_required`, ค่าตัวเลข 12 หรือ 25,000 ที่ผูกกับบรรทัด ; สำหรับ ACC-RCN ต้องไม่มี `count1` / ผลนับรอบ 1 (ข้อเสนอ — ยืนยันใน OQ-MB-04) ; app log ไม่มีค่าเหล่านี้
- Runs in: 4.2 เท่านั้น
- Seed/QC: TC-MB-03

### TC-MST-12 — กรอกจำนวน: 0 ได้, ว่าง/ติดลบไม่ได้, ชี้บรรทัดผิด

- Priority: Medium
- FN: FN-07
- Trace: S-04, API-05, BR-03
- Role/Account: ACC-CNT
- Precondition: DS-C (`ST-MB-C02`) ; DS-I สำหรับขั้น 5
- Steps:
  1. เปิดใบนับ กด “ส่งผลนับ” ตอนทุกช่องว่าง
  2. กรอก ITM-001 = `0` ช่องเดียว แล้วกดส่ง ; จากนั้นกรอก ITM-002 = `-1`
  3. แก้เป็น `0` / `20` — ตรวจแถบเตือนและสถานะช่อง ; กดส่งแล้ว **ยกเลิก**กล่องยืนยัน
  4. agent ส่ง API-05 ตรงโดยขาด 1 บรรทัด และมีค่า −1
  5. (DS-I) กรอก `12.5` ที่ ITM-008 (กก.)
- Expected: ขั้น 1 ส่งไม่ได้ ข้อความ “กรุณากรอกผลนับทุกสินค้าเป็นศูนย์หรือมากกว่า” โฟกัส/เลื่อนไปช่องแรกที่ผิด ช่องผิดมี `aria-invalid`/a11y error ไม่พึ่งสีอย่างเดียว; ขั้น 2 `0` ถือว่าถูก, `-1` ถูกปฏิเสธที่บรรทัด; ขั้น 3 แถบเตือนหายเมื่อแก้ครบ (regression **UX-B02**), ยกเลิกแล้วค่า 0 / 20 คงอยู่ (B-02); ขั้น 4 422 `BR_COUNT_INCOMPLETE` / `BR_COUNT_NEGATIVE` ไม่บันทึก; ขั้น 5 **BLOCKED จนปิด OQ-MB-05** (ทศนิยมตาม UoM) — keyboard ต้องตรง UoM ที่ตกลง
- Runs in: 4.2 · 4.3 (ขั้น 1–3)
- Seed/QC: TC-MB-04, TC-MB-11, B-02, UX-B02

### TC-MST-13 — ส่งผลนับได้เฉพาะ assignee ปัจจุบัน

- Priority: High
- FN: FN-07
- Trace: S-04, API-05, BR-03
- Role/Account: ACC-OUT, ACC-SUP, ACC-CNT
- Precondition: DS-C (`ST-MB-C01` counting, assignee ACC-CNT)
- Steps:
  1. login ACC-OUT เปิดรอบ (ผ่าน deep link/ค้นหา)
  2. agent ส่ง API-05 ด้วย token ACC-OUT และ ACC-SUP
  3. ACC-SUP reassign รอบ 1 เป็นคนอื่น (ถ้า 3.1 อนุญาต) แล้ว ACC-CNT ส่งผลจากหน้าจอที่เปิดค้าง
- Expected: ขั้น 1 ไม่มีช่องกรอก/ปุ่มส่ง (อ่านอย่างเดียวหรือ 403 ตามสิทธิ์) ไม่เห็นข้อมูลต้องห้าม; ขั้น 2 403 `ERR_NOT_ASSIGNED_COUNTER` (“ไม่ใช่ผู้ได้รับมอบหมายให้นับในขั้นนี้”); ขั้น 3 ถูกปฏิเสธ (`ERR_NOT_ASSIGNED_COUNTER` หรือ 409 `ERR_STALE_DATA`) และแอป refresh ไม่แสดงสำเร็จ
- Runs in: 4.2 · 4.3 (ขั้น 1)
- Seed/QC: TC-MB-03

### TC-MST-14 — ส่งผลนับ: กดซ้ำ / ส่งซ้ำไม่เกิด submission ซ้ำ

- Priority: High
- FN: FN-07
- Trace: S-04, API-05, BR-08
- Role/Account: ACC-CNT
- Precondition: DS-C (`ST-MB-C02` counting)
- Steps:
  1. กรอก 10 / 20 แล้วแตะ “ส่งผลนับ” → “ยืนยัน” 3 ครั้งติดกันเร็ว ๆ
  2. agent replay request เดิม (key + body เดิม)
  3. agent ส่ง key เดิมแต่ body ต่าง (11 / 20)
  4. agent ส่ง key ใหม่ด้วย `expected_version` เก่า
- Expected: ขั้น 1 ปุ่ม disable ระหว่างส่ง, request ออก 1 ครั้ง (หรือ retry ด้วย `Idempotency-Key` เดิม), core มี submission 1 รายการ, toast 1 ครั้ง; ขั้น 2 ได้ผลเดิม ไม่เพิ่ม event; ขั้น 3 409 `ERR_IDEMPOTENCY_CONFLICT`; ขั้น 4 409 `ERR_STALE_DATA`
- Runs in: 4.2 เท่านั้น (ขั้น 1 ทำใน 4.3 ได้แต่ตรวจผลผ่าน audit)
- Seed/QC: TC-MB-09

### TC-MST-15 — Server คำนวณผลต่างด้วย threshold version ของรอบ

- Priority: High
- FN: FN-08
- Trace: S-05, API-05, API-06, BR-04
- Role/Account: ACC-SUP
- Precondition: DS-C รอบ 1 ส่งแล้ว ; DS-J(5) เปลี่ยน threshold policy เป็น 5 หลัง freeze
- Steps:
  1. ACC-SUP เปิด S-05 ของ `ST-MB-C01`
  2. agent เรียก API-06 `/variance`
  3. ตรวจ request ของแอป (BFF log) ว่าไม่มีการส่งค่าผลต่างที่คำนวณจาก client
- Expected: ผลต่าง ITM-001 = 9 − 12 = −3, ITM-002 = 0; threshold ที่ใช้ = 2 (version ของรอบ, eff 2026-09-01) **ไม่ใช่ 5** → ต้อง recount; ข้อมูลเหล่านี้มาจาก server; `computeVariance` ใน client ไม่ถูกใช้ตัดสินสถานะ; ป้ายกำกับเป็นภาษาไทย
- Runs in: 4.2 · 4.3 (ขั้น 1)
- Seed/QC: TC-MB-05, B-04

### TC-MST-16 — Boundary: ผลต่างเท่ากับ threshold ไม่ต้องนับซ้ำ

- Priority: High
- FN: FN-08
- Trace: S-05, API-05, API-06, BR-04
- Role/Account: ACC-CNT → ACC-SUP
- Precondition: DS-C (`ST-MB-C02`) — ใช้ผลจาก TC-MST-14 (10 / 20) หรือ seed ใหม่
- Steps:
  1. ACC-CNT ส่ง 10 / 20
  2. ACC-SUP เปิดรอบ
- Expected: abs(10 − 12) = 2 ไม่ `>` 2 → สถานะ “รอตรวจผลต่าง” (`review`) ทันที ไม่มีขั้นนับซ้ำ; S-05 แสดงผลต่าง −2 / 0 และมูลค่า 50,000 บาท (เฉพาะ supervisor); (variant seed 9 / 20 → recount ตาม TC-MST-17)
- Runs in: 4.2 · 4.3
- Seed/QC: TC-MB-05

### TC-MST-17 — นับซ้ำโดยคนละคน และใช้ผลรอบ 2 เป็นผลสุดท้าย

- Priority: High
- FN: FN-09
- Trace: S-03, S-04, S-05, API-04, API-05, BR-04
- Role/Account: ACC-CNT → ACC-SUP → ACC-RCN → ACC-SUP
- Precondition: DS-C (`ST-MB-C01`)
- Steps:
  1. ACC-CNT ส่ง 9 / 20
  2. ACC-SUP เปิดรอบ → มอบหมายนับซ้ำให้ ACC-RCN
  3. ACC-RCN เปิดใบนับซ้ำ กรอก 11 / 20 ส่ง
  4. ACC-SUP เปิด S-05
- Expected: ขั้น 1 → สถานะ “รอนับซ้ำ” ก่อนมอบหมาย; ขั้น 2 → ยังเป็น “รอนับซ้ำ” พร้อมข้อความ “กำลังนับซ้ำ” และ assignee = พิมพ์ดาว; ขั้น 3 → “ตรวจผลต่าง”; ขั้น 4 แสดง ยอดตั้งต้น 12 / นับครั้งที่ 1 = 9 / นับซ้ำ = 11 / ผลต่างสุดท้าย −1 / มูลค่า 25,000 บาท; ITM-002 20 / 20 / 20 / 0; ผลรอบ 1 ยังเก็บเป็นหลักฐาน (เห็นใน S-05 และ S-06) (regression B-03, B-04)
- Runs in: 4.2 · 4.3
- Seed/QC: TC-MB-05, B-03, B-04

### TC-MST-18 — สิทธิ์ใบนับซ้ำ: ผู้นับรอบ 1 ส่ง/แก้ไม่ได้ และใบนับซ้ำยัง blind

- Priority: High
- FN: FN-09
- Trace: S-04, API-05, API-06, BR-03, BR-04
- Role/Account: ACC-CNT, ACC-RCN
- Precondition: `ST-MB-C01` สถานะกำลังนับซ้ำ (หลัง TC-MST-17 ขั้น 2)
- Steps:
  1. ACC-CNT เปิดรอบ ; agent ส่ง API-05 `count_round:2` และ `count_round:1` (ส่งซ้ำ) ด้วย token ACC-CNT
  2. ACC-RCN เปิดใบนับซ้ำ ตรวจหน้าจอ
- Expected: ขั้น 1 ไม่มีช่องกรอก; API ตอบ `ERR_NOT_ASSIGNED_COUNTER` (หรือ 409 สถานะไม่รองรับ) — ผลรอบ 1 แก้ย้อนหลังไม่ได้; ขั้น 2 ใบนับซ้ำ blind เหมือน S-04: ไม่มียอดระบบ/ต้นทุน/ผลต่าง/threshold และไม่มีผลนับรอบ 1 (ดู TC-MST-11)
- Runs in: 4.2 · 4.3 (ขั้น 2)
- Seed/QC: TC-MB-03, TC-MB-05

### TC-MST-19 — ส่งอนุมัติ: DOA preview, เลือกคนต่อ slot และ freeze chain

- Priority: High
- FN: FN-10
- Trace: S-05, SH-03, API-07, API-13, BR-05
- Role/Account: ACC-SUP
- Precondition: DS-D (`ST-MB-D01` review, มูลค่า abs 25,000) ; DS-J(6) สำหรับขั้น 5
- Steps:
  1. เปิด S-05 ตรวจ “ฐานอนุมัติ” และกด “ส่งอนุมัติ” → SH-03
  2. ตรวจ slot จาก API-13 `doa-preview`
  3. เลือก slot 1 = นลิน, slot 2 = อรทัย → ยืนยัน
  4. หลังส่ง ให้ admin เปลี่ยน DOA matrix sandbox แล้วเปิดรอบอีกครั้ง
  5. (variant) รอบที่ไม่มี tier ครอบ → ส่งอนุมัติ
- Expected: ขั้น 1 ป้าย “ฐานอนุมัติ” 25,000 บาท เป็นภาษาไทย ไม่มี “APPROVAL BASIS” (regression **UX-B04**); ขั้น 2 2 slot (ผู้จัดการคลัง → ผู้อำนวยการคลัง) มาจาก server ไม่ hardcode; ขั้น 3 สถานะ “รออนุมัติ” step ปัจจุบัน = 1, request มี `selected_people[{slot_no, person_id}]` + `expected_version`; ขั้น 4 chain ของรอบไม่เปลี่ยน (frozen); ขั้น 5 `BR_DOA_NO_TIER` “ไม่พบสายอนุมัติสำหรับมูลค่านี้” ไม่ส่ง
- Runs in: 4.2 · 4.3 (ขั้น 1–3)
- Seed/QC: B-04, UX-B04

### TC-MST-20 — กันผู้อนุมัติต้องห้าม: ขาด slot, เป็นผู้นับ, ซ้ำคน (ห้าม self-approval)

- Priority: High
- FN: FN-10
- Trace: SH-03, API-07, API-12, BR-05
- Role/Account: ACC-SUP
- Precondition: DS-D (`ST-MB-D01` review; counter ACC-CNT, recounter ACC-RCN)
- Steps:
  1. SH-03 เว้น slot 2 แล้วกดส่ง
  2. ตรวจว่ามีกิตติพงษ์/พิมพ์ดาวให้เลือกหรือไม่ ; agent ส่ง API-07 โดย slot 1 = ACC-CNT
  3. agent ส่ง API-07 slot 1 = slot 2 = ACC-APR
  4. agent ส่ง API-07 slot 2 = ACC-RCN
- Expected: ขั้น 1 `BR_APPROVAL_SLOT_MISSING` “กรุณาเลือกผู้อนุมัติทุกขั้น”; ขั้น 2 UI ตัดหรือ disable ผู้นับ/ผู้นับซ้ำ (ถ้าแสดงต้องปฏิเสธ) และ API 422 `BR_APPROVER_IS_COUNTER` “ผู้อนุมัติต้องไม่ใช่ผู้นับ”; ขั้น 3 `BR_APPROVER_DUPLICATE`; ขั้น 4 `BR_APPROVER_IS_COUNTER`; ทุกกรณีสถานะยัง review ไม่มี chain
- Runs in: 4.2 · 4.3 (ขั้น 1–2 UI)
- Seed/QC: TC-MB-06

### TC-MST-21 — ตัดสินตามลำดับ: เฉพาะผู้อนุมัติ step ปัจจุบัน

- Priority: High
- FN: FN-10
- Trace: S-05, API-08, BR-05
- Role/Account: ACC-APR, ACC-SUP, ACC-CNT
- Precondition: `ST-MB-D01` หลัง TC-MST-19 (pending step 1 = นลิน) หรือ DS-D `ST-MB-D02`
- Steps:
  1. ACC-APR เปิดรอบ ; agent ส่ง API-08 approve ด้วย token ACC-APR
  2. ACC-CNT เปิดรอบ / ส่ง API-08
  3. ACC-SUP กด “อนุมัติขั้นนี้” → ยืนยัน
  4. ACC-APR กด “อนุมัติขั้นนี้” → ยืนยัน
- Expected: ขั้น 1 ACC-APR ไม่เห็นปุ่มตัดสิน (เห็น progress “รอขั้นที่ 1”), API 403 `ERR_NOT_CURRENT_APPROVER`; ขั้น 2 ไม่มีปุ่ม, API `ERR_NOT_CURRENT_APPROVER`/`ERR_INSUFFICIENT_ROLE`; ขั้น 3 step → 2; ขั้น 4 กล่องยืนยันบอก “ครบทุกขั้น → อนุมัติแล้ว” สถานะ “อนุมัติแล้ว”; audit มีผู้ทำ/เวลาแต่ละขั้น
- Runs in: 4.2 · 4.3
- Seed/QC: TC-MB-06, B-04

### TC-MST-22 — ไม่อนุมัติต้องมีเหตุผล และปล่อย lock เฉพาะรอบนั้น

- Priority: High
- FN: FN-10
- Trace: S-05, API-08, BR-05, BR-01
- Role/Account: ACC-SUP (step 1 ของ `ST-MB-D02`)
- Precondition: DS-D (`ST-MB-D02` pending) ; DS-B (`ST-MB-B01` lock active)
- Steps:
  1. กด “ไม่อนุมัติ” เว้นเหตุผล → ยืนยัน
  2. agent ส่ง API-08 `{decision:"rejected"}` ไม่มี reason
  3. กรอกเหตุผล “นับไม่ครบโซน” → ยืนยัน
  4. ตรวจ lock ของ scope `ST-MB-D02` และ `ST-MB-B01`, และประวัติ
- Expected: ขั้น 1 กล่องไม่ปิด และ**มีข้อความ** “กรุณาระบุเหตุผล” ที่ช่อง + a11y (regression **UX-B04**); ขั้น 2 422 `BR_REJECT_REASON_REQUIRED`; ขั้น 3 สถานะ “ไม่อนุมัติ” (`rejected`); ขั้น 4 lock ของ D02 ถูกปล่อย แต่ lock ของ B01 ยังอยู่; ประวัติมีเหตุผล + ผู้ทำ + เวลา
- Runs in: 4.2 · 4.3 (ขั้น 1, 3)
- Seed/QC: TC-MB-06, B-04, UX-B04

### TC-MST-23 — ตัดสินพร้อมกัน / กดซ้ำ: first commit wins ไม่มีการตัดสินซ้ำ

- Priority: High
- FN: FN-10
- Trace: S-05, API-08, BR-05, BR-08
- Role/Account: ACC-SUP บน 2 เครื่อง
- Precondition: DS-D (`ST-MB-D03` pending step 1)
- Steps:
  1. เปิดรอบบนเครื่อง A และ B ; A กด “อนุมัติขั้นนี้” ยืนยันสำเร็จ
  2. B (หน้าจอเก่า) กด “ไม่อนุมัติ” พร้อมเหตุผล → ยืนยัน
  3. agent replay request ของ A ด้วย key เดิม ; ส่ง request พร้อมกัน 2 ตัว key ต่างกัน
- Expected: ขั้น 1 step → 2; ขั้น 2 B ได้ 409 `ERR_STALE_DATA` (หรือ `ERR_NOT_CURRENT_APPROVER`) → แอป refresh แสดงสถานะจริง ไม่แสดงว่าไม่อนุมัติสำเร็จ; ขั้น 3 replay ได้ผลเดิม; คำขอพร้อมกันสำเร็จเพียง 1; audit มี decision step 1 เพียงรายการเดียว
- Runs in: 4.2 เท่านั้น
- Seed/QC: TC-MB-06

### TC-MST-24 — สร้างร่างใบปรับยอด F082: ปิดรอบและปล่อย lock เมื่อได้ ack

- Priority: High
- FN: FN-11
- Trace: S-05, S-06, API-09, BR-06
- Role/Account: ACC-SUP
- Precondition: DS-F (`ST-MB-F01` approved) ; จด on-hand ของ ITM-001/002 ใน core ก่อนเริ่ม
- Steps:
  1. กด “สร้างร่างใบปรับยอด” → ยืนยัน
  2. เปิด tab ประวัติ
  3. agent ตรวจ core: on-hand, movement, lock ของ scope, F082 draft
- Expected: ขั้น 1 สำเร็จเมื่อได้ ack เท่านั้น: “สร้างร่างใบปรับยอดและปิดรอบนับแล้ว” สถานะ “ปิดรอบแล้ว”; ขั้น 2 มี event ack พร้อม `adj_id` จาก F082 + เวลา (regression B-05); ขั้น 3 F082 มี draft 1 ใบอ้างรอบ, **on-hand ไม่เปลี่ยน และไม่มี movement ที่ post จาก stocktake**, lock ถูกปล่อย
- Runs in: 4.2 · 4.3 (ขั้น 1–2)
- Seed/QC: TC-MB-07, B-05

### TC-MST-25 — F082 ใช้ไม่ได้ / timeout: ไม่ปิดรอบ ไม่ปล่อย lock และ retry ไม่สร้างซ้ำ

- Priority: High
- FN: FN-11
- Trace: S-05, API-09, BR-06, BR-08
- Role/Account: ACC-SUP
- Precondition: DS-E (`ST-MB-E01` approved) ; fault = `unavailable` แล้วเปลี่ยนเป็น `timeout`
- Steps:
  1. (unavailable) กด “สร้างร่างใบปรับยอด” → ยืนยัน
  2. (timeout) กดอีกครั้ง — response ไม่กลับภายใน client timeout แต่ core/F082 สร้างสำเร็จ
  3. ปิด fault แล้วกดลองใหม่ตามที่แอปเสนอ
  4. (offline) ปิดเน็ตบนรอบ approved อื่น แล้วดูปุ่ม
- Expected: ขั้น 1 502 `ERR_F082_UNAVAILABLE` → “สร้างร่างใบปรับยอดไม่สำเร็จ รอบยังไม่ปิดและพื้นที่ยังล็อก” สถานะยัง “อนุมัติแล้ว”, lock ยังอยู่, ไม่มี draft ครึ่งเดียว; ขั้น 2 แอปแสดง “ยังยืนยันผลไม่ได้” ปุ่ม disabled แล้ว GET สถานะก่อน — เมื่อพบว่าปิดแล้วให้แสดงสถานะจริงโดยไม่ส่งซ้ำ; ขั้น 3 retry ใช้ `Idempotency-Key` + payload เดิม → F082 มี draft **1** ใบ; ขั้น 4 ปุ่ม disabled “ต้องออนไลน์” ไม่มีการเข้าคิว
- Runs in: 4.2 เท่านั้น (ต้องใช้ fault flag) — 4.3 ดูเฉพาะข้อความขั้น 1 ถ้า sandbox เปิด fault ให้
- Seed/QC: TC-MB-07, OQ-MB-06

### TC-MST-26 — F082 draft ได้ครั้งเดียว และเฉพาะหลัง approved โดย supervisor

- Priority: High
- FN: FN-11
- Trace: S-05, API-09, BR-06
- Role/Account: ACC-SUP, ACC-APR
- Precondition: DS-F (`ST-MB-F02` closed, `ST-MB-F03` review)
- Steps:
  1. เปิด `ST-MB-F03` ตรวจว่ามีปุ่มสร้างร่างหรือไม่ ; agent ส่ง API-09
  2. agent ส่ง API-09 ของ `ST-MB-F02` (key ใหม่) และ replay key เดิมของ F02
  3. agent ส่ง API-09 ด้วย token ACC-APR บนรอบ approved
- Expected: ขั้น 1 ไม่มีปุ่ม; API ถูกปฏิเสธ (409 `ERR_HANDOFF_ALREADY_EXISTS` “ต้องอนุมัติผลต่างก่อน และสร้างใบปรับได้ครั้งเดียว” — ดู Contradictions C-02); ขั้น 2 key ใหม่ → 409 `ERR_HANDOFF_ALREADY_EXISTS`, key เดิม → ผลเดิม (`adj_id` เดิม) ไม่มี draft ใหม่และไม่มี event ใหม่; ขั้น 3 403 `ERR_INSUFFICIENT_ROLE`
- Runs in: 4.2 เท่านั้น
- Seed/QC: TC-MB-07

### TC-MST-27 — ขอบเขตรอบนับใหญ่: ไม่มี Cycle Count/ABC บนมือถือ

- Priority: Medium
- FN: FN-12
- Trace: S-01, S-02, API-01, BR-01
- Role/Account: ACC-SUP
- Precondition: DS-G (มีงาน Cycle Count/ABC ใน core)
- Steps:
  1. ตรวจชื่อหน้า คำอธิบาย ตัวเลือกใน S-02 และ chip สถานะ
  2. agent เรียก API-01 ทุก `status`
- Expected: ระบุ “ตรวจนับใหญ่ / Stocktake”; ไม่มีตัวเลือก ABC, schedule, Cycle Count; API-01 ไม่คืนงาน Cycle Count; ไม่มีการตั้งค่า DOA/threshold บนมือถือ (out of scope)
- Runs in: 4.2 · 4.3
- Seed/QC: TC-MB-08

### TC-MST-28 — ประวัติรอบ: actor + เวลา + action ตามสิทธิ์ ไม่เปิดตัวเลขลับ

- Priority: High
- FN: FN-12
- Trace: S-06, API-10, BR-07
- Role/Account: ACC-AUD, ACC-SUP, ACC-CNT
- Precondition: DS-G (`ST-MB-F02` closed)
- Steps:
  1. ACC-AUD เปิดรอบ → tab ประวัติ
  2. ACC-SUP เปิดประวัติเดียวกัน
  3. ACC-CNT เปิดประวัติ ; agent เรียก API-10 ด้วย token ACC-CNT
- Expected: ขั้น 1 ทุก event มี **ผู้ทำ + วันเวลา** + action + ผล (regression **UX-B05**) เรียงตามเวลา, มี F082 ack + `adj_id`; ACC-AUD อ่านอย่างเดียว ไม่มีปุ่ม action; ขั้น 2 เห็นตามสิทธิ์ supervisor; ขั้น 3 event ไม่มีตัวเลขยอดระบบ/ผลต่าง/มูลค่า (เช่น “ส่งผลนับรอบ 1” โดยไม่มีจำนวน) ทั้งบนจอและใน response (ขอบเขตการเห็นของ auditor รอ OQ-MB-04)
- Runs in: 4.2 · 4.3 (ขั้น 1–2)
- Seed/QC: TC-MB-08, B-05, UX-B05

### TC-MST-29 — Loading, empty (ไม่มีงาน vs ไม่พบผลกรอง) และ error พร้อมลองใหม่

- Priority: Medium
- FN: FN-13
- Trace: S-01..S-06, ทุก API, BR-08
- Role/Account: ACC-OUT, ACC-SUP
- Precondition: DS-H ; network throttle (slow 3G) ; sandbox fault 500 ที่ API-06
- Steps:
  1. login ACC-OUT เปิด S-01 ขณะ throttle
  2. ดูหลังโหลดเสร็จ (ไม่มีรอบ)
  3. ACC-SUP เปิดรอบที่ API-06 ตอบ 500 → กด “ลองใหม่” หลังปิด fault
  4. เปิดรอบที่ไม่มีเหตุการณ์ (ประวัติว่าง) และ S-05 ที่ไม่มีรายการต้องตัดสินใจ
- Expected: ขั้น 1 skeleton ไม่มีตัวเลข 0 ปลอม; ขั้น 2 “ไม่มีงาน…” (ต่างข้อความจาก “ไม่พบรอบที่ตรงกับตัวกรอง”); ขั้น 3 แสดงสาเหตุที่แสดงได้ + ปุ่มลองใหม่ แล้วโหลดสำเร็จ; ขั้น 4 empty ตาม state matrix (“ยังไม่มีเหตุการณ์”, “ไม่มีรายการที่ต้องตัดสินใจ”); ใบนับที่ไม่มีบรรทัดแสดง “ติดต่อหัวหน้า” และส่งผลว่างไม่ได้
- Runs in: 4.2 · 4.3 (ขั้น 1–2)
- Seed/QC: MOBILE_SPEC_NOTES state matrix

### TC-MST-30 — Offline: ปิด mutation ทั้งหมด ไม่มี offline queue และค่าร่างคงอยู่ใน session

- Priority: High
- FN: FN-13
- Trace: S-01..S-05, API-02..API-09, BR-08
- Role/Account: ACC-CNT, ACC-SUP
- Precondition: DS-C (`ST-MB-C01` counting) ; อุปกรณ์สลับ airplane mode ได้
- Steps:
  1. ACC-CNT กรอก 5 / 7 แล้วเปิด airplane mode กด “ส่งผลนับ”
  2. ACC-SUP (offline) ลองสร้างรอบ, freeze, assign, ส่งอนุมัติ, อนุมัติ, สร้างร่าง F082
  3. กลับออนไลน์ รอ 30 วินาที ; agent ตรวจ BFF log
- Expected: ขั้น 1 banner “ออฟไลน์ · เชื่อมต่อเพื่อส่งข้อมูล” ปุ่มส่ง disabled ไม่มี request; ขั้น 2 ทุก action disabled / ไม่ส่ง และไม่แสดงสำเร็จ; ขั้น 3 ค่า 5 / 7 ยังอยู่ (session เดิม) แต่**ไม่มีการส่งอัตโนมัติ** (ไม่มี queue) — ต้องกดส่งเอง; BFF ไม่มี mutation ช่วง offline (regression B-06)
- Runs in: 4.2 (airplane ทำมือได้) · 4.3
- Seed/QC: TC-MB-09, B-06

### TC-MST-31 — Timeout หลังส่ง: “ยังยืนยันผลไม่ได้” → reconcile ก่อน retry ด้วย key เดิม

- Priority: High
- FN: FN-13
- Trace: S-04, S-05, API-05, API-06, API-08, BR-08
- Role/Account: ACC-CNT, ACC-SUP
- Precondition: DS-C (`ST-MB-C02` หรือรอบ counting ใหม่) ; DS-J(1) และ DS-J(2)
- Steps:
  1. เปิด fault (1) หน่วงแต่ commit ; ACC-CNT ส่งผลนับ
  2. ดูหน้าจอระหว่าง/หลัง timeout ; agent ดู BFF log
  3. เปิด fault (2) หน่วงไม่ commit ; ส่งอีกรอบ → กด “ลองใหม่” ที่แอปเสนอ
  4. ทำซ้ำขั้น 1–2 กับ API-08 (อนุมัติ) บน DS-D
- Expected: ขั้น 2 แสดง “ยังยืนยันผลไม่ได้” ไม่แสดงสำเร็จหรือล้มเหลวเท็จ ปุ่ม disabled; แอป GET สถานะ (API-06) ก่อน → พบว่าส่งแล้ว แสดงสถานะจริง ไม่ส่งซ้ำ; ขั้น 3 GET พบว่ายังไม่ส่ง → retry ด้วย `Idempotency-Key` และ payload **เดิม** (ห้ามสร้าง key ใหม่ก่อน reconcile); core มี submission/decision รายการเดียวทุกกรณี
- Runs in: 4.2 เท่านั้น
- Seed/QC: TC-MB-09, OQ-MB-06

### TC-MST-32 — 401 session หมดอายุ / สลับผู้ใช้: กลับหน้า login และไม่เห็นข้อมูลของคนก่อน

- Priority: High
- FN: FN-13
- Trace: ทุกหน้า, `GET /m/v1/me`, BR-03, BR-08
- Role/Account: ACC-CNT → ACC-OUT
- Precondition: DS-C ; DS-J(3)
- Steps:
  1. ACC-CNT กรอก 9 / 20 (ยังไม่ส่ง) ; revoke session แล้ว pull-to-refresh / กดส่ง
  2. login กลับด้วย ACC-CNT
  3. logout แล้ว login ACC-OUT บนเครื่องเดียวกัน เปิดรอบเดียวกันผ่าน deep link
  4. ตรวจ build ว่าไม่มีตัวเลือกสลับ persona
- Expected: ขั้น 1 401 → ไปหน้าเข้าสู่ระบบทั้งหน้า ไม่ค้าง section, ไม่แสดงสำเร็จ; ขั้น 2 แอปตรวจสิทธิ์และโหลดสถานะใหม่จาก server; ขั้น 3 ACC-OUT ไม่เห็นค่าร่าง 9 / 20 หรือข้อมูลรอบเกินสิทธิ์ (cache ของผู้ใช้ก่อนถูกล้าง); ขั้น 4 ตัวตนจาก `/me` เท่านั้น ไม่มี persona switcher
- Runs in: 4.2 · 4.3 (ขั้น 1–3)
- Seed/QC: TC-MB-10

### TC-MST-33 — 403 และ 409: ซ่อนข้อมูล/ปิด input และ refresh ให้ทบทวน

- Priority: Medium
- FN: FN-13
- Trace: S-03, S-04, S-05, API-04..API-08, BR-08
- Role/Account: ACC-NOP, ACC-SUP
- Precondition: DS-H ; DS-D
- Steps:
  1. ACC-NOP เปิด deep link ไปรอบ `ST-MB-D01`
  2. ACC-SUP เปิด S-05 `ST-MB-D01` ค้างไว้ ; อีก session เปลี่ยนสถานะรอบ (เช่น ส่งอนุมัติ) ; กลับมากดส่งอนุมัติบนหน้าจอเดิม
  3. ตรวจ GET ซ้ำด้วย ETag (304) หลังสถานะเปลี่ยน
- Expected: ขั้น 1 403 `ERR_INSUFFICIENT_ROLE` → หน้าจอไม่แสดงข้อมูลรอบ ไม่มี input/action (ไม่ใช่ 401 ทั้งหน้า); ขั้น 2 409 `ERR_STALE_DATA` → “ข้อมูลเปลี่ยนแล้ว กรุณาโหลดใหม่” refresh แสดงสถานะล่าสุด ข้อมูลที่ผู้ใช้กรอกไม่หายเงียบ ๆ (แจ้งให้ทบทวน); ขั้น 3 หลังเปลี่ยนสถานะได้ 200 ใหม่ ไม่ได้ 304 ค้างค่าเก่า
- Runs in: 4.2 · 4.3 (ขั้น 1–2)
- Seed/QC: MOBILE_SPEC_NOTES state matrix

### TC-MST-34 — 426 APP_UPDATE_REQUIRED: บล็อกและไม่ส่ง mutation

- Priority: Medium
- FN: FN-13
- Trace: ทุก API, BR-08
- Role/Account: ACC-CNT
- Precondition: DS-C ; DS-J(4)
- Steps:
  1. เปิด fault 426 แล้วเปิด S-01 / กดส่งผลนับ
- Expected: แสดงหน้าขอให้อัปเดตแอป (ข้อความไทย + ปุ่มไปร้านค้า) ไม่แสดงข้อมูลรอบเก่าเป็นปัจจุบัน; ไม่มี mutation ถูก commit; ไม่ใช่ error ทั่วไป/ไม่ใช่ logout
- Runs in: 4.2 เท่านั้น
- Seed/QC: BFF rule 426

### TC-MST-35 — ร่างผลนับเก็บใน memory ของ session เท่านั้น

- Priority: High
- FN: FN-13
- Trace: S-04, BR-08, OQ-MB-02
- Role/Account: ACC-CNT
- Precondition: DS-C (`ST-MB-C01` counting)
- Steps:
  1. กรอก 9 / 20 แล้วกดย้อนกลับ
  2. กลับเข้าใบนับเดิม (app ยังเปิด) ; ส่งแอปไป background 1 นาทีแล้วกลับมา
  3. kill แอปแล้วเปิดใหม่
  4. กรอกใหม่ แล้ว logout → login ACC-CNT อีกครั้ง
  5. agent ตรวจ storage ของแอป (AsyncStorage / MMKV / ไฟล์) หลังขั้น 1
- Expected: ขั้น 1 มีกล่องยืนยันการออกเพราะมีข้อมูลที่ยังไม่ส่ง; ขั้น 2 ค่าคงอยู่; ขั้น 3 ค่าหาย (ไม่รับปากว่าเก็บถาวร); ขั้น 4 ค่าถูกล้าง; ขั้น 5 ไม่มีค่าผลนับเขียนลงดิสก์; ร่างไม่ถือว่าเป็นผลที่ server รับ — **ผลตามข้อเสนอ OQ-MB-02 (อนุมัติใน 1.3) รอ Security ยืนยัน ถ้า policy เปลี่ยนต้องแก้เคสนี้**
- Runs in: 4.2 · 4.3 (ขั้น 1–4)
- Seed/QC: TC-MB-10, B-06

### TC-MST-36 — Accessibility และจอเล็ก: font scale, dark mode, keyboard, focus

- Priority: Medium
- FN: FN-13
- Trace: S-01..S-05, SH-02, SH-03
- Role/Account: ACC-CNT, ACC-SUP
- Precondition: DS-C, DS-I ; อุปกรณ์จอแคบ (≈ 320–360 pt) ; OS font scale สูงสุด ; dark mode ; screen reader (TalkBack/VoiceOver)
- Steps:
  1. ตั้ง OS font scale สูงสุด เปิด S-01, S-04, S-05
  2. ใน S-04 เปิด numeric keyboard ที่บรรทัดล่างสุด (DS-I หลายบรรทัด) แล้วเลื่อนไปช่องที่ผิด
  3. เปิดกล่องยืนยัน / SH-02 / SH-03 หลังเลื่อนหน้าจอ
  4. เปิด dark mode และ screen reader เดินโฟกัสรายการ → ใบนับ → ปุ่มส่ง → กล่องยืนยัน
- Expected: ขั้น 1 ตัวอักษรขยายตาม OS (regression **DEF-P02** — ห้าม fixed px) ข้อความไทยไม่ตัด ไม่มี scroll แนวนอน; ขั้น 2 keyboard ไม่บังช่อง/ปุ่มส่ง, เลื่อนไปบรรทัดผิดพร้อมข้อความ; ขั้น 3 กล่อง/sheet อยู่ในจอทั้งหมด ปุ่มกดได้ (เทียบ DEF-P01 ของ prototype); ขั้น 4 อ่านได้ทุกโหมด, ปุ่ม/ช่องมี label ไทย (เช่น “ผลนับ ปั๊มน้ำ”), ลำดับโฟกัสถูก, ปิดกล่องยืนยันได้และค่าคงอยู่, touch target ≥ 44 pt; performance ของ N บรรทัดรอ OQ-MB-05
- Runs in: 4.2 (ขั้น 1, 3) · 4.3 (ทั้งหมดบนเครื่องจริง)
- Seed/QC: TC-MB-11, B-07, DEF-P01, DEF-P02

## 6. Seed & QC Mapping

### 6.1 Seed TC-MB (MOBILE_SPEC_NOTES) → TC-MST

| Seed | FN | สถานการณ์ | TC-MST |
|---|---|---|---|
| TC-MB-01 | FN-01,02 | ค้นหา/เลือกพื้นที่, empty | 01, 02, 04 |
| TC-MB-02 | FN-03,04 | freeze ซ้อนถูกปฏิเสธ, snapshot เดียว | 05, 06, 07 |
| TC-MB-03 | FN-05,06 | non-assignee ส่งไม่ได้, blind UI + response | 08, 10, 11, 13, 18 |
| TC-MB-04 | FN-07 | 0 ผ่าน, ว่าง/ติดลบไม่ผ่าน, ทศนิยม | 12 |
| TC-MB-05 | FN-08,09 | เท่ากับ threshold ไม่ recount, เกิน recount คนอื่น | 15, 16, 17, 18 |
| TC-MB-06 | FN-10 | self-approval/ข้ามขั้น, reject reason, stale | 20, 21, 22, 23 |
| TC-MB-07 | FN-11 | handoff ก่อน approved, F082 fail/timeout, ไม่ซ้ำ | 24, 25, 26 |
| TC-MB-08 | FN-12 | ไม่มี Cycle Count/ABC, history ตามสิทธิ์ | 27, 28 |
| TC-MB-09 | FN-05,07 | offline / timeout ไม่สำเร็จเท็จ, ไม่ซ้ำ | 14, 30, 31 |
| TC-MB-10 | FN-01,06,10 | session หมดอายุ / สลับ user | 32, 35 |
| TC-MB-11 | FN-07 | keyboard, จอเล็ก, font scale | 12, 36 |

### 6.2 Prototype Browser QC → regression ใน TC-MST

| QC | ผลใน 1.2 (prototype) | ตรวจซ้ำบนแอปจริงใน |
|---|---|---|
| B-01 ค้นหา/กรอง/ล้าง | PASS | TC-MST-01 |
| B-02 blind + ช่องว่าง + ยกเลิกยืนยัน | PASS | TC-MST-10, 12 |
| B-03 นับซ้ำคนละคน | PASS | TC-MST-09, 17 |
| B-04 ผลต่าง + reject reason + approve | PASS | TC-MST-15, 17, 19, 21, 22 |
| B-05 F082 + ประวัติ | PASS | TC-MST-24, 28 |
| B-06 offline + ค่าคงอยู่ | PASS | TC-MST-30, 35 |
| B-07 จอแคบ/dark/font/focus | PARTIAL | TC-MST-36 |
| DEF-P01 dialog 320px (prototype only) | S3 | TC-MST-36 ขั้น 3 (ยืนยันว่าแอปไม่มีปัญหาเดียวกัน) |
| DEF-P02 fixed px font | S3 | TC-MST-36 ขั้น 1 |
| UX-B01 chip แตะครั้งแรกไม่ติด | ต่ำ | TC-MST-01 ขั้น 2 |
| UX-B02 แถบเตือนค้าง + ไม่มี aria-invalid | ต่ำ | TC-MST-12 ขั้น 1, 3 |
| UX-B04 reject ไม่มีข้อความ + “APPROVAL BASIS” | ต่ำ | TC-MST-19 ขั้น 1, TC-MST-22 ขั้น 1 |
| UX-B05 ประวัติไม่มีเวลา/ผู้ทำ | ต่ำ | TC-MST-28 ขั้น 1 |

## 7. Coverage Audit

| Source | Coverage |
|---|---|
| 13 FN (FN-01..13) | 13/13 — ตาม allocation ใน FACTS (36 TC) |
| 8 Business Rules | BR-01: 01–06, 22, 27 · BR-02: 05, 07 · BR-03: 08–14, 18, 32 · BR-04: 09, 15–18 · BR-05: 19–23 · BR-06: 24–26 · BR-07: 11, 28 · BR-08: 02, 06, 14, 23, 25, 29–35 → 8/8 |
| Endpoints API-01..13 | API-01: 01, 11, 27 · API-02: 02, 03 · API-03: 05–07 · API-04: 08, 09, 17 · API-05: 12–18, 31 · API-06: 04, 07, 10, 11, 15, 31 · API-07: 19, 20 · API-08: 21–23, 31 · API-09: 24–26 · API-10: 11, 28 · API-11: 02, 03 · API-12: 08, 09, 20 · API-13: 19 → 13/13 |
| Screens S-01..S-06, SH-02, SH-03 | 8/8 |
| Error codes (FACTS) | ERR_REQUIRED_FIELD 03 · ERR_INSUFFICIENT_ROLE 03, 09, 26, 33 · ERR_IDEMPOTENCY_CONFLICT 14 · ERR_SCOPE_OVERLAP 06 · ERR_STALE_DATA 06, 14, 23, 33 · ERR_SCOPE_EMPTY 06 · BR_RECOUNT_SAME_PERSON 09 · ERR_NOT_ASSIGNED_COUNTER 13, 18 · BR_COUNT_INCOMPLETE / BR_COUNT_NEGATIVE 12 · BR_APPROVAL_SLOT_MISSING / BR_APPROVER_IS_COUNTER / BR_APPROVER_DUPLICATE 20 · BR_DOA_NO_TIER 19 · ERR_NOT_CURRENT_APPROVER 21 · BR_REJECT_REASON_REQUIRED 22 · ERR_HANDOFF_ALREADY_EXISTS 26 · ERR_F082_UNAVAILABLE 25 · 401 32 · 426 34 |
| Priority | High 26 · Medium 10 · Low 0 |
| Run location | 4.2: 36/36 · 4.3 (UAT ทั้งเคสหรือบางขั้น): 29 — 4.2 เท่านั้น: 07, 11, 23, 25 (4.3 ดูข้อความได้ถ้าเปิด fault), 26, 31, 34 |

## 8. Run Protocol & Exit Rule

1. Seed sandbox ตาม DS-A..J และบัญชี ACC-* (OQ-MB-07); ตั้ง `E2E_*` ของแต่ละ role ใน `.maestro/run.sh`
2. ติดตั้ง RC build (preview `cube-mobile-release`) ต่อ BFF sandbox; ตั้งปุ่มลอยเป็น BLANK หรือใช้ build ที่ถอดแล้ว
3. **4.2 (agent บน RC):** รันครบ 36 เคส — UI ผ่าน Maestro (`07_stocktake.yaml` ปรับเป็น DS + `10_stocktake_live.yaml`), ตรวจ response/BFF log/core audit ด้วย HTTP client ต่อ token ของแต่ละ role; offline/airplane/font scale ทำมือได้
4. **4.3 (UAT):** ผู้ใช้จริงตาม role รันเคส/ขั้นที่ระบุ “4.3” บนเครื่องจริง บันทึกผลใน `testcase-F-MB-STOCKTAKE.html` แล้ว export MD/CSV แนบใน core
5. เก็บหลักฐาน: screenshot + build version + บัญชี (key ACC-*) + เวลา + เลขรอบ; สำหรับ blind test เก็บ raw JSON response (ลบ token ออก)
6. ผลต่างจาก Expected → `FAIL` + defect (S1–S4); ถูก block โดย OQ/fault ที่ sandbox ไม่มี → `BLOCKED` + อ้าง OQ — ห้ามตีความแทนระบบ

**Severity:** S1 = ข้อมูลต้องห้ามรั่วถึง counter/recounter, self-approval ผ่าน, ปิดรอบ/ปล่อย lock โดยไม่มี ack, เกิด submission/decision/draft ซ้ำ, แสดงสำเร็จเท็จ · S2 = กฎธุรกิจผิดหรือ flow หลักใช้ไม่ได้โดยไม่มีทางเลี่ยง · S3 = ใช้ได้แต่มีปัญหา UX/ข้อความ/a11y · S4 = เล็กน้อย

**Exit rule 4.2 → 4.3:** เคส **High ผ่าน 100%** (26/26 — `BLOCKED` ไม่นับว่าผ่าน) **และ ไม่มี defect S1/S2 ค้าง**; เคส Medium ที่ FAIL ต้องมี defect S3/S4 ที่ PO รับทราบ. ผลขั้นที่ BLOCKED จาก OQ-MB-05 (ทศนิยม/จำนวนบรรทัด) อยู่ใน TC Medium (12, 36) จึงไม่ block exit แต่ต้องปิดก่อน release

## 9. Additions (ไม่มีใน FACTS — เสนอในเอกสารนี้)

| Item | รายละเอียด |
|---|---|
| ACC-CNT / ACC-RCN / ACC-SUP / ACC-APR / ACC-AUD / ACC-OUT / ACC-NOP | key บัญชี sandbox ตาม role (เพิ่ม ACC-OUT, ACC-NOP สำหรับ negative) — รอ OQ-MB-07 |
| DS-A..DS-J, รอบ `ST-MB-*`, คลัง `WH-T*` | ข้อมูล sandbox ที่ต้อง seed; ITM-001/002 ค่าเดียวกับ prototype |
| Maestro `10_stocktake_live.yaml` | flow ใหม่ต่อข้อมูลจริง (ชื่อเสนอ); `07_stocktake.yaml` เดิมอิง mock |
| Severity S1–S4 นิยามตามข้างบน | ใช้กับ exit rule |
| Must-NOT-appear list ของ blind DTO รวม `count1` สำหรับ recounter | ข้อเสนอ — ยืนยันใน OQ-MB-04 / 3.1 |

## 10. Contradictions / ข้อสังเกตที่ต้องให้ owner ตัดสิน

| ID | ประเด็น | ผลต่อเคส |
|---|---|---|
| C-01 | Web TC-ST-11 ให้ผู้ตรวจเห็นสถานะ “รอนับซ้ำ” หลังส่ง แต่ BR-03 ห้ามให้ counter รู้ threshold result — สถานะ recount ที่ counter เห็นเท่ากับบอกว่าเกินเกณฑ์ | TC-MST-10 ขั้น 3 คาดหวังว่าไม่เห็น; ยืนยันใน OQ-MB-04 |
| C-02 | ส่ง F082 ก่อน approved: web FRD API-09 ระบุ precondition approved แต่ error ที่มีคือ `ERR_HANDOFF_ALREADY_EXISTS` (ข้อความใน `engine.ts` ครอบทั้งสองกรณี) ; `store.ts` ยังใช้ `BR_INVALID_STATE` ซึ่งไม่อยู่ในรายการ error ของ FACTS | TC-MST-26 ขั้น 1 ยอมรับ `ERR_HANDOFF_ALREADY_EXISTS`; ให้ 3.1 กำหนด code สถานะไม่รองรับ |
| C-03 | DOA set 2 slot 1 = ผู้จัดการคลัง ซึ่งคือ supervisor ผู้ส่งอนุมัติ (นลิน) — BR-05 ห้ามเฉพาะ counter/recounter ไม่ได้ห้าม submitter | TC-MST-19/21 ใช้ ACC-SUP เป็น slot 1 ตาม web; ถ้า OQ-ST-02 ห้าม ต้องใช้ผู้จัดการคลังคนอื่น |
| C-04 | Browser QC B-04 ให้อรทัยอนุมัติโดยตรง (1 ขั้น) แต่ข้อมูล prototype/DOA ให้ 25,000 บาท = 2 ขั้น | ใช้ DOA brief (2 ขั้น) ใน DS-D |
| C-05 | `engine.ts` ใช้ข้อความเดียวกันสำหรับ `BR_COUNT_INCOMPLETE` และ `BR_COUNT_NEGATIVE` — ไม่ระบุว่าบรรทัดใดผิดเพราะอะไร | TC-MST-12 ต้องชี้บรรทัด; ข้อความแยกให้ UI Brief ตัดสิน |
