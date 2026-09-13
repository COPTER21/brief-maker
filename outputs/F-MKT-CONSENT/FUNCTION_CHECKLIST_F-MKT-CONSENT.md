# FUNCTION_CHECKLIST — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> ⚠️ **สกัดจาก `PREBRIEF_F-MKT-CONSENT.md` เอง** — แพ็กบรีฟไม่มีไฟล์ checklist (ตาม WF-01 Phase 3)
> ใช้เป็น contract ของ step 4 (qc-coverage) + ตัวหารของ step 5 (e2e) · คอลัมน์ `WF` ติ๊กที่ step 4 · `QA` ที่ step 9
> plan row: `F058 · Marketing · W1 · dec=["csq"] · dep=""` (standalone — ไม่ ref feature อื่น)
>
> 🔄 **โมเดลเนื้อหา (แก้ 2026-09-11 per PM/BA — ต้อง sync กลับ PREBRIEF):** เนื้อหา PDPA = **เอกสารอัปโหลด (versioned)** ไม่ใช่ข้อความพิมพ์ → กระทบ **BR-05/06** (เดิม "แก้ข้อความ" → "อัปโหลดเอกสารเวอร์ชันใหม่") · การเซ็น = ผ่าน **มุมมองผู้รับ (หน้าจำลองเต็ม เปิดลิงก์ → อ่านเอกสาร → ยืนยันตัวตน → ยินยอม/ไม่ยินยอมรายวัตถุประสงค์)** แทนปุ่มจำลอง · **GOVERNANCE: BA ต้องอัปเดต PREBRIEF BR-05/06 + FN-01/02/09/10/11 ให้ตรง**

## FN บวก (ต้องทำได้) — 20 ตัว · e2e ต้องครอบ 20/20

| FN | ความสามารถ | ที่มา | WF | QA |
|---|---|---|:--:|:--:|
| FN-01 | สร้างวัตถุประสงค์ใหม่ (ชื่อ · ช่องทางที่ใช้ได้ · อายุ 1–120ด. default 24 · **อัปโหลดเอกสาร PDPA v1** จำลอง — ต้องแนบเอกสาร) | S-01·BR-03/05/11 | ☐ | ☑ |
| FN-02 | **อัปโหลดเอกสารเวอร์ชันใหม่** → ออกเวอร์ชันใหม่ + เตือน consent เวอร์ชันเดิม N รายการไม่ครอบคลุม | S-02·BR-05/06 | ☐ | ☑ |
| FN-03 | ตารางวัตถุประสงค์ + สถิติ (ยินยอม/ถอน/หมดอายุ/%ครอบคลุม) | S-03 | ☐ | ☑ |
| FN-04 | ปิดวัตถุประสงค์ (ห้ามสร้างคำขอใหม่ · consent เดิมคงอยู่เป็นหลักฐาน) | S-04·BR-14 | ☐ | ☑ |
| FN-05 | สร้างคำขอรายเดียว (เจ้าของ + วัตถุประสงค์หลายข้อ + ช่องทาง → ลิงก์ + QR) · single-screen ไม่ใช่ wizard | S-05·BR-01/03 | ☐ | ☑ |
| FN-06 | ส่งคำขอทางอีเมล (บันทึกเวลา/ที่อยู่ · สถานะ→รอตอบ) | S-06·BR-07 | ☐ | ☑ |
| FN-07 | ส่งซ้ำช่องทางอื่น = การส่งครั้งที่ N ในคำขอเดิม (ไม่สร้างคำขอใหม่) | S-07·BR-18 | ☐ | ☑ |
| FN-08 | คัดลอกลิงก์ / **ดาวน์โหลด QR** (บันทึกการนำลิงก์ออก) | S-08 | ☐ | ☑ |
| FN-09 | **ดาวน์โหลดเอกสาร** ของคำขอ (เอกสารเวอร์ชันปัจจุบันของแต่ละวัตถุประสงค์) | S-09 | ☐ | ☑ |
| FN-10 | ลูกค้าเซ็นผ่าน **มุมมองผู้รับ (จำลองลิงก์)** → อ่านเอกสาร + ยืนยันตัวตน + เซ็น → "ตอบแล้ว" + สร้างทะเบียน + หลักฐาน 5 อย่าง | S-10·BR-15 | ☐ | ☑ |
| FN-11 | ยินยอมบางวัตถุประสงค์ ผ่านมุมมองผู้รับ (ยินยอม/ไม่ยินยอม **รายวัตถุประสงค์** บันทึกแยกข้อ) | S-11·BR-01 | ☐ | ☑ |
| FN-12 | ดูหลักฐาน 1 รายการ (เวลา·ช่องทาง·วิธียืนยันตัวตน·เวอร์ชันนโยบาย·IP/อุปกรณ์) | S-12·BR-15 | ☐ | ☑ |
| FN-13 | ทะเบียนทั้งหมด (เจ้าของ×วัตถุประสงค์×ช่องทาง + สถานะ + หมดอายุ · กรองทุกมิติ) | S-13·BR-07 | ☐ | ☑ |
| FN-14 | ดู consent ของลูกค้ารายหนึ่งในที่เดียว (**E1 Customer 360**) | S-14 | ☐ | ☑ |
| FN-15 | ถอนแทนลูกค้า (เหตุผล + ช่องทางที่แจ้ง · มีผลทันที · ไม่ต้องอนุมัติ) | S-15·BR-09/10 | ☐ | ☑ |
| FN-16 | รายการใกล้หมดอายุ ≤30 วัน (เตือน ไม่บล็อก · กดต่ออายุได้) | S-16·BR-12 | ☐ | ☑ |
| FN-17 | ต่ออายุ = คำขอใหม่อ้างรายการเดิม (ไม่แก้วันหมดอายุเดิม) | S-17·BR-13 | ☐ | ☑ |
| FN-18 | ประวัติ 1 รายการ (timeline append-only + เหตุผลทุกครั้ง) | S-18·BR-16 | ☐ | ☑ |
| FN-19 | ตัวจำลอง `/consent/resolve` (เจ้าของ+วัตถุประสงค์+ช่องทาง → allowed + เหตุผล + JSON ล็อกฟิลด์) | S-19·BR-19/20 | ☐ | ☑ |
| FN-20 | ตรวจคนไม่เคยถูกขอ → `allowed:false · status:"never_asked"` (ไม่ใช่ 404 / ไม่ใช่ "ไม่ยินยอม") | S-20·BR-04/08/19 | ☐ | ☑ |

## FN-40 — ต้องไม่มี (จาก Part C 10 ข้อ) · e2e เรนเดอร์จริงแล้ว assert ว่าไม่โผล่

| FN-40.x | ห้ามมี | LOCK | ตรวจได้ที่ |
|---|---|---|---|
| 40.1 | cookie consent บนเว็บ | LOCK-05 | render + grep |
| 40.2 | สายอนุมัติภายในก่อนส่งคำขอ | LOCK-04 | render (ไม่มีปุ่ม/สถานะอนุมัติในสายส่ง) |
| 40.3 | ส่งอีเมล/LINE จริง | — | toast จำลองเท่านั้น |
| 40.4 | คำนวณมูลค่า / คอลัมน์เก็บผลรายท่อ | LOCK-CSQ-04/05 | render + grep |
| 40.5 | การ์ดผล 7 ท่อ CSQ บนหน้าจอ | LOCK-CSQ-06 | render (ไม่มี pipe-card) |
| 40.6 | ประกาศท่อ OC / DC / SC | LOCK-CSQ-01/02/03 | CSQ_BRIEF step 7 |
| 40.7 | ธง opt-out เดียวต่อคน (Odoo) แทนคู่ 3 มิติ | — | โมเดล triple |
| 40.8 | "ไม่ตอบ" นับเป็น "ไม่ยินยอม" | — | render (lapsed ≠ declined) |
| 40.9 | บล็อกการส่งด้วยตัวเอง (ที่นี่ตอบอย่างเดียว) | — | resolve read-only |
| 40.10 | wizard Pattern Q (สร้างคำขอ = single-screen) | LOCK-07 | render (ไม่มี stepper 5 ขั้น) |

## สถานะ pipeline (6→12)
- step6 BRD ✅ (2026-09-13) `BRD_F-MKT-CONSENT.md` + `.docx` — Gate APPROVED, upload model = DECLARED-01, 6 OQ
- step7 FRD ✅ (2026-09-13) `FRD_Pack\` FULL 10 ไฟล์ — gate PASS; OQ-03/OQ-04 BLOCKING (id-verify จริง, ขึ้นทะเบียน F143)
- csq-declaration ✅ (2026-09-13) `CSQ_BRIEF_F-MKT-CONSENT.md` — 7 events, declare-only (no OC/DC/SC), gates pass; OQ-CSQ-01 profile#, OQ-CSQ-02 SecC pipe [DEFAULT รอ BA]
- step8 UI Brief ✅ `UI_BRIEF_ความยินยอม-PDPA.md`
- step9 AI Test case ✅ (2026-09-13) `testcases-consent-pdpa.md` — 72 เคสจริง (สรุปในไฟล์เขียน 68 = stale, reconcile ที่ step12) · QA 20/20 · FN-40 negatives 10/10 · XT 5/5 · LOCK 13/13
- step10 Coverage R2 ✅ (2026-09-13) `_COVERAGE_R2_REPORT.md` — PASS · FRD 20/20 · TC 20/20 · BR 27/27 · FN-40 10/10 · no creep · WARN: DECLARED-01 + microcopy drift + TC-count stale
- step11 UAT ✅ (2026-09-13) `ความยินยอม PDPA HTML Testcase.html` — 62 เคสคนเล่นได้ · 8 กลุ่ม · 0 JS err · capture 20/0 · drop-ledger 10 backend-only
- step11.5 TL;DR ✅ (2026-09-13) `FEATURE_TLDR_F-MKT-CONSENT.html` — gate PASS · แสดง gate results + DECLARED-01 + BLOCKING OQ-03/04
- step12 ปิดงาน ✅ (2026-09-13) `PROPOSALS_outbound.md` · PENDING `MG-01` (combobox meter-gap) · **หยุดรอ commit** (ยังไม่ commit)

## Declaration รอบนี้
- **csq** ✅ (plan `dec=["csq"]`) → `CSQ_BRIEF_F-MKT-CONSENT.md` ออกที่ step 7 (declare-only event → 7C Engine · ห้ามประกาศ OC/DC/SC ซ้ำ)
- doa / doccfg / ntf = ไม่เลือก

## OQ / เลื่อน (→ PROPOSALS_outbound.md ที่ step 12)
- BR-21 caller cache ≤5 นาที + ล้างเมื่อถอน = สัญญาฝั่งผู้เรียก (document ใน FRD API ไม่ทำ UI)
- BR-22 `/consent/*` ขึ้นทะเบียนด่านบังคับใช้สิทธิ์ 4 ขั้น = ผูกฟีเจอร์ Security wave W2 (ยังไม่ทำ) → **OQ**
- E3 consent receipt PDF = scope ใหม่ เลื่อน (ทำได้ที่ step 2 / wave DSAR)
