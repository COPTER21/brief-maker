# _COVERAGE_REPORT — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> **Step 4 · qc-coverage-checker · ROUND 1 (HTML vs contract)** — re-run หลัง BA-gate surgical edits
> วันที่: 2026-09-14 · Artifact: `outputs/F-MKT-CONSENT/consent-pdpa.html` (205.2K)
> Contract: `PREBRIEF_F-MKT-CONSENT.md` (S-01..20 · BR-01..22 + CSQ) + `FUNCTION_CHECKLIST_F-MKT-CONSENT.md` (20 FN บวก · 10 FN-40)
> ขอบเขตรอบนี้: รอบ 1 เท่านั้น (UI มีทาง/ช่อง/สถานะ/handler รองรับครบมั้ย · FN-40 absence · scope creep) — **ไม่ใช่รอบ 2** (FRD/TC = `_COVERAGE_R2_REPORT.md`)

---

## VERDICT: ✅ **PASS** (มี WARN 2 ข้อ · ไม่มี block-severity gap)

| ตัวชี้วัด | ผล |
|---|---|
| FN บวก wired ใน HTML | **20 / 20** ✓ (handler เดินได้จริง ไม่ใช่ปุ่มหลอก) |
| FN-40 (ต้องไม่มี) absent | **10 / 10** ✓ |
| Scope creep | **ไม่พบ** (Part C 1–10 ไม่โผล่บนจอ) |
| Declaration coverage | CSQ ✓ · DOA/NTF/DOCCFG = N/A (ดู DIVERGENCE) |
| Contract anchors F136 / F031 / F157 | **present · display-only** — ไม่มีจอ feature อื่นถูก mock |

**WARN (ไม่บล็อก · ยกเป็น governance/บันทึก):**
1. **DECLARED-01** — content model = เอกสารอัปโหลด versioned ต่อวัตถุประสงค์ (HTML+CHECKLIST) ต่างจาก PREBRIEF ที่เขียน "แก้ข้อความ" (free-text) → **governance OQ (BA อัปเดต PREBRIEF BR-05/06 + FN-01/02/09/10/11)** — ไม่ใช่ coverage failure, ทั้ง contract ปัจจุบัน (checklist) กับ HTML ตรงกันแล้ว
2. **DIVERGENCE (chip≠detect) DECL-DOA** — `prebrief_checklist.py` detect `doa=true` แต่ plan chip = `dec=["csq"]` เท่านั้น → เป็น **false-positive จากคำ "อนุมัติ" ในบริบทปฏิเสธ** (BR-09 "ไม่ต้องผ่านการอนุมัติ" · Part C/LOCK-04 "ห้ามใส่สายอนุมัติ" · FN-40.2). ไม่มี action อนุมัติ/สถานะ pending_approval/slot-row ใน HTML → **DOA out-of-scope โดยเจตนา (N/A)** ไม่ใช่ missing brief · Strike ตัดสิน

---

## Declaration Coverage (Phase 0b)

| ท่อ | เข้าเงื่อนไข? | Evidence | ผล |
|---|---|---|---|
| **CSQ** | ✅ (กระทบข้อมูลอ่อนไหว/ตัดสินใจปลายทาง · plan dec=csq) | `emitConsequence()` declare-only sink (L2332) — "renders NOTHING · no pipe cards · no value calc" · envelope มี `idempotency_key` (BR-CSQ-02) + `reversal_of` บน withdraw (BR-CSQ-04, L3041) · ไม่ประกาศ OC/DC/SC · `CSQ_BRIEF_F-MKT-CONSENT.md` มีจริง | ✓ |
| **DOA** | ❌ (ห้ามมี — FN-40.2/LOCK-04) | ไม่มี approval UI · comment L2797 "ไม่มี approval chain" | N/A (DIVERGENCE — ดูข้างบน) |
| **NTF** | ❌ (chip ไม่เลือก · ส่งจริง = forbidden 40.3) | toast จำลองเท่านั้น | N/A |
| **DOCCFG** | ❌ (ไม่ใช่เอกสารธุรกรรมมีเลขรัน) | — | N/A |

---

## Coverage Matrix — FN บวก (ROUND 1 · HTML)

| FN | ความสามารถ | HTML evidence (route/selector/handler) | WF |
|---|---|---|:--:|
| FN-01 | สร้างวัตถุประสงค์ + อัปโหลดเอกสาร v1 | tab purposes · MOCK UPLOAD control (L1376) · `versions[]`+`currentVer` (L2185) · guard `PERM().purpose` DPO (L3055) | ☑ |
| FN-02 | อัปโหลดเวอร์ชันใหม่ + เตือน N เดิมไม่ครอบคลุม | `publishVersion` → warn-banner "affected รายการจะไม่ครอบคลุมเวอร์ชันใหม่" (L3050) · `emitConsequence('policy.version_published')` (L3062) · S-02/BR-06 | ☑ |
| FN-03 | ตารางวัตถุประสงค์ + สถิติ | tab purposes · `purStatusPill` (L2540) · ver-tag/coverage · stats (L2535) | ☑ |
| FN-04 | ปิดวัตถุประสงค์ (ห้ามสร้างคำขอใหม่ · consent เดิมคงอยู่) | `closePurpose` guard `PERM().purpose` (L3071) · `emitConsequence('purpose.closed')` · status='closed' (PUR-04) กัน reqCreate | ☑ |
| FN-05 | สร้างคำขอรายเดียว (single-screen drawer) → ลิงก์+QR | `openReqCreate`→`reqCreateDrawer` (L2648) form เดียว · submit "สร้างคำขอ + ลิงก์/QR" (L2662) · **ไม่ใช่ page wizard** | ☑ |
| FN-06 | ส่งคำขอทางอีเมล (บันทึกเวลา/ที่อยู่ · →รอตอบ) | `sendVia` guard `PERM().send` (L2750) · status→pending · SIM_NOTE (L2155) | ☑ |
| FN-07 | ส่งซ้ำช่องทางอื่น = ส่งครั้งที่ N ในคำขอเดิม | `resendOther`→`sendVia` (L2754) push `sends[]` · FIX-05 เฉพาะ draft/pending (L2751) · BR-18 | ☑ |
| FN-08 | คัดลอกลิงก์ / ดาวน์โหลด QR (บันทึกการนำออก) | `downloadQR` (L3123) push `sends[{ch:'export-qr'}]` · copy link | ☑ |
| FN-09 | ดาวน์โหลดเอกสารของคำขอ (เวอร์ชันปัจจุบันต่อ purpose) | `downloadPdfForm` (L3126) ปุ่ม "ดาวน์โหลดเอกสาร" (L2725) | ☑ |
| FN-10 | เซ็นผ่านมุมมองผู้รับ → ทะเบียน + หลักฐาน 5 | `recipientViewHTML`/`submitRecipient` (L2812) verify+choices→`applyAnswers` → registry+5-evidence+history · guard `PERM().sign` (L2763) | ☑ |
| FN-11 | ยินยอมบางวัตถุประสงค์ (รายข้อ แยกบันทึก) | `setRecipientChoice` grant/decline ต่อ code (L2809) · applyAnswers push consent ต่อ purpose (L2777/2782) | ☑ |
| FN-12 | ดูหลักฐาน 5 อย่าง | evidence grid BR-15 (L1541) · `evItem` เวลา·ช่องทาง·วิธียืนยัน·เวอร์ชัน·IP/อุปกรณ์ (L2958+) | ☑ |
| FN-13 | ทะเบียนทั้งหมด + กรองทุกมิติ | tab registry `#/consent/registry` · `filteredConsents` (L2497) · statusPill · filters | ☑ |
| FN-14 | consent ลูกค้ารายเดียว (Customer 360) | c360 view · `c360-row`+statusPill (L2993) | ☑ |
| FN-15 | ถอนแทนลูกค้า (เหตุผล+ช่องทาง · ทันที · ไม่อนุมัติ) | `withdraw` guard `PERM().withdraw` (L3033) · reason+channel modal · `emitConsequence('consent.withdrawn', reversal_of)` (L3041) · BR-09/10 | ☑ |
| FN-16 | รายการใกล้หมด ≤30 วัน (เตือน ไม่บล็อก · ต่ออายุได้) | `daysLeft` (L2144) · near-tag (L1588) · filter 'near' (L2462) · ปุ่มต่ออายุ | ☑ |
| FN-17 | ต่ออายุ = คำขอใหม่อ้างรายการเดิม | `openReqCreate({refOld})` refBanner BR-13 (L2655) · `emitConsequence('consent.renew_requested')` (L2691) | ☑ |
| FN-18 | ประวัติ 1 รายการ (timeline append-only) | `.timeline` (L1007) · `history[]` render เรียงเวลา (L2206+) | ☑ |
| FN-19 | ตัวจำลอง /consent/resolve (allowed+เหตุผล+JSON) | tab resolve `#/consent/resolve` · `runResolve`/`resolveResultHTML` (L2565+) · read-only · HTTP 200 เสมอ · BR-19/20 | ☑ |
| FN-20 | never_asked (allowed:false · ไม่ 404 · ไม่ "ไม่ยินยอม") | `resolveConsent` return `allowed:false, status:'never_asked'` (L2587) · statusPill แยก never_asked/declined/expired (L2246) | ☑ |

**FN wired = 20 / 20** — ทุกตัวมี handler เดินได้ ผูก state จริง

---

## FN-40 — ต้องไม่มี (ROUND 1 · render/grep evidence)

| FN-40.x | ห้ามมี | ผลตรวจ | Evidence |
|---|---|:--:|---|
| 40.1 | cookie consent บนเว็บ | ✅ absent | grep `cookie` = 0 hit |
| 40.2 | สายอนุมัติก่อนส่งคำขอ | ✅ absent | ไม่มี slot-row/approve/pending_approval · comment L2797 "ไม่มี approval chain" |
| 40.3 | ส่งอีเมล/LINE จริง | ✅ absent | `SIM_NOTE=' (จำลอง — ไม่ส่งจริง)'` (L2155) · toast เท่านั้น |
| 40.4 | คำนวณมูลค่า / คอลัมน์เก็บผลรายท่อ | ✅ absent | `emitConsequence` "no value calc" (L2331) · ไม่มีคอลัมน์ผลท่อ |
| 40.5 | การ์ดผล 7 ท่อ CSQ บนจอ | ✅ absent | ไม่มี `pipe-card` · sink "renders NOTHING · no pipe cards" (L2331) |
| 40.6 | ประกาศท่อ OC/DC/SC | ✅ absent | HTML emit event เท่านั้น · declare OC/DC/SC ไม่มี (CSQ_BRIEF declare-only) |
| 40.7 | ธง opt-out เดียวต่อคน (Odoo) | ✅ absent | โมเดล triple: consent มี subject×purpose×channel (L2205+) · BR-01 |
| 40.8 | "ไม่ตอบ" นับเป็น "ไม่ยินยอม" | ✅ absent | `effStatus` แยก expired (L2225) · pill 'คำขอหมดอายุ'/'หมดอายุ' ≠ 'ไม่ยินยอม' (L2243/2247) |
| 40.9 | บล็อกการส่งด้วยตัวเอง | ✅ absent | resolve read-only (ปุ่มเดียว "ตรวจสิทธิ์" `runResolve` ไม่ mutate/ไม่ block) | 
| 40.10 | wizard Pattern Q (5 ขั้น) | ✅ absent | create request = drawer single-screen · `.wizard-stepper-band` = BASE-KIT CSS ไม่ถูกใช้สร้างคำขอ · LOCK-07 | 

**FN-40 absent = 10 / 10**

---

## Contract Anchors (การยืนยันตามคำสั่ง)

| Code | บทบาท | Evidence | display-only? |
|---|---|---|:--:|
| **F136** Broadcast | consume `resolveConsent` (ctl ตรวจ opt-in ก่อนส่ง) | comment L7/2561 · resolve simulator (FN-19) | ✅ ไม่ mock จอ F136 |
| **F031** Customer 360 | consume consent status (data) | comment L7/2561 · FN-14 c360 view (จอของ **feature นี้** ไม่ใช่ F031) | ✅ ไม่ mock จอ F031 |
| **F157** DSAR | ทะเบียน consent+evidence+history = ฐานข้อมูลให้ DSAR | comment L7/2419 · registry/history (จอ feature นี้) | ✅ ไม่ mock จอ F157 |

ทั้ง 3 เป็น **contract anchor comment** ("อ้างเป็น contract anchor — ไม่ใช่การอ้างจอ", L10) — ไม่มีหน้าจอ feature อื่นถูกวาด/จำลอง → **ไม่ใช่ scope creep**

---

## Scope Guard (Part C · S-01..20)

- Part C 1–10 ทั้งหมด absent (ตรงกับ FN-40 ข้างบน)
- ทุก S-01..20 มี FN รองรับ · ไม่มี flow เกิน contract ใน HTML

## Gap list

- ไม่มี block/warn-severity coverage gap ในรอบ 1
- WARN carry (governance, ไม่บล็อก): DECLARED-01 (BA sync PREBRIEF BR-05/06 + FN-01/02/09/10/11) · DECL-DOA divergence (detector false-positive → Strike ยืนยัน N/A)

## หมายเหตุการ re-run (C3.2)

- รอบนี้เป็นการรัน step 4 ซ้ำหลังแตะ `.html` (BA-gate surgical edits) — การแก้ทั้งหมดเป็น **guards/anchors** (answered-once, recipient closed-page, `_busy`, persona, version-snapshot+stale near-tag, contract-anchor comments, demo-only, purStatusPill) → **ไม่มี FN ใหม่ · ไม่มี FN-40 ใหม่ · ไม่มี scope เปลี่ยน** — coverage เดิม 20/20 คงอยู่
