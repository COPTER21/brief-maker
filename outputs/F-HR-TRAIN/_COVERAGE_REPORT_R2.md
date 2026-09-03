# Coverage Report (รอบ 2 · FRD Pack + Test Cases vs Contract) — F-HR-TRAIN (อบรม / Training · F133)

- วันที่: 2026-09-03 · WF-01 **step 10** (ตรวจ *ทำครบมั้ย* รอบ 2 · ก่อนส่ง dev) · skill `qc-coverage-checker`
- คำถามรอบนี้: **spec (FRD) และ test (TC) ผูกทุก FN/BR/edge/permission ครบมั้ย** — ไม่ซ้ำรอบ 1 (HTML vs PREBRIEF, PASS)
- Artifacts ตรวจ:
  - FRD Pack: `FRD_F-HR-TRAIN_Pack/` (00_OVERVIEW Coverage Manifest · 05_RULES · 06_TESTS · 02_API · 03_LOGIC)
  - Test cases: `testcases-อบรม.md` (**84 เคส** / 11 group · มี Coverage Ledger + Coverage Audit)
  - Contract: `FUNCTION_CHECKLIST.html` (18 FN + unsupported 5) · `PREBRIEF.md` (12 S · 10 BR · §12 declarations)
  - Declaration briefs: DOA_BRIEF · NTF_BRIEF · CSQ_BRIEF (DOCCFG/PDF = N/A)
- อ้างอิงร่วม: `อบรม.html` · `BRD_อบรม.md` · `_COVERAGE_REPORT.md` (รอบ 1)

## Verdict: 🟢 PASS

| Metric | ผล |
|---|---|
| **FN ↔ TC** | **18 / 18** ทุก FN มี TC ≥1 (trace กลับ FN/S/BR ครบใน Ledger) |
| **BR ↔ TC** (05_RULES §5.1) | **18 / 18** (BR-01..18 มีเคส · block rule ไม่มีตัวไหนหาย) |
| **AC ↔ TC** (06_TESTS) | **29 / 29** (AC-01..25 happy/main + AC-26..29 edge ผ่าน TC-EC01/PR01/ID01/RACE01) |
| **Edge cases** (05_RULES §5.5) | **8 / 8** (EC-01..08) |
| **Negatives "ห้ามมี"** (แทน FN-40) | **5 / 5** (TC-N01..N05 = unsupported 1–5) |
| **Permission** | 3 persona (hr/manager/viewer) + SoD (hr approve=deny) + mask money ครบ |
| **Cross-Module (XT)** | **4 / 4** (+XT-01b/02) |
| **Scope Lock (LOCK-01..07)** | **7 / 7** ทุกข้อมีเคส verify |
| **Capability ใหม่ FIX-01..07** | **7 / 7** (FIX-06/07 = DOA gate+slot · Rate Card display-only) |
| **Declaration ↔ FRD** (DOA/NTF/CSQ) | sync-read ครบ · ไม่มี hardcoded chain/event/เลขรัน |
| **uncovered BLOCK** | **0** |
| ขัด contract / scope creep | 0 / 0 |

> เทียบรอบ 1: gap ที่ปิดแล้ว = ไม่มีค้าง (รอบ 1 PASS อยู่แล้ว) · **เกิดใหม่ = 0** · รอบ 2 เพิ่มชั้นตรวจ spec/test ที่รอบ 1 ยังไม่แตะ (FRD rule เนื้อตรง + FN↔TC ledger + error catalog + XT)

---

## Matrix — 18 FN ↔ TC (evidence จาก Coverage Ledger)

| FN | ความสามารถ | FRD (05_RULES/06) | TC (evidence) | ✓ |
|---|---|---|---|:--:|
| FN-01 | สร้างหลักสูตร (has_cost/งบ) | BR-01 · AC-01..03 | TC-C01/C02/C03/C04/C05/C09 | ✓ |
| FN-02 | สร้างรอบ (guard published) | BR-11 · AC-05 | TC-S01/S02/S03/S04 | ✓ |
| FN-03 | ลงทะเบียน (gap/manual · เกิน→บล็อก) | BR-02/03 · AC-07/08 | TC-E01/E02/E03/E10/RACE01 | ✓ |
| FN-04 | has_cost → DOA ก่อนยืนยัน | BR-04 · AC-09 | TC-E04/E05/E06 | ✓ |
| FN-05 | ฟรี → ยืนยันทันที ข้าม DOA | BR-04 · AC-10 | TC-E07 | ✓ |
| FN-06 | บันทึกผล (closed+attended)+eval | BR-05/05b · AC-13/14 | TC-R04/R05/R06/R07 | ✓ |
| FN-07 | ออกใบรับรอง (soft ref) | BR-07C · AC-15 | TC-R08/R09 | ✓ |
| FN-08 | DOA slot picker (ไม่ hardcode) | BR-13/14 · AC-11 | TC-E05/E06/E08/E09/PR01 | ✓ |
| FN-09 | ค่าอบรม → Expense hook + EC | BR-06/09/12 · AC-16 · XT-01 | TC-X01/X02/X03/XT01/XT02 | ✓ |
| FN-10 | gap → แนะนำผู้เรียน (hook read) | BR-07 · AC-08 · OQ-01 | TC-E02/N02/XT04 | ✓ |
| FN-11 | ยกเลิกการลงทะเบียน (soft archive) | BR-08 · AC-17 | TC-X05/X06/CANEC01 | ✓ |
| FN-12 | แจ้งเตือน 3 event | NTF_BRIEF · AC-19 | TC-S05/E07/R06/NTF01 | ✓ |
| FN-13 | รายงาน completion + ต้นทุนต่อหัว | BR-16 · AC-18 | TC-RP01/RP02/RP03/RP04 | ✓ |
| FN-90 | ค้นหา/filter + empty | AC-20 | TC-G01/G02/G03 | ✓ |
| FN-91 | ปิด/ยกเลิก confirm + soft archive | BR-08 · AC-17/21 | TC-C07/S06/X05/G04 | ✓ |
| FN-92 | validate + กัน double-submit | EC-04/07 · AC-22 | TC-C02/G05/ID01 | ✓ |
| FN-93 | audit append-only | §5.7 D9 · AC-23 | TC-G06/G07 | ✓ |
| FN-94 | masking ตาม role | §5.7 D-CLASS · AC-24 | TC-P05/P06/MASK01 | ✓ |

**Coverage Manifest (FRD §0.12) cross-check:** 20/20 แถว (FN-01..13 + FN-90..94 + FIX-04/05) มีคู่ใน Ledger ✅

## Matrix — Declaration ↔ FRD (Phase 0b/Phase 2)

| ท่อ | เข้าเงื่อนไข | brief | FRD sync-read | TC | ✓ |
|---|---|---|---|---|:--:|
| DOA | has_cost → approval (BR-04) | DOA_BRIEF ✓ | 02_API §DOA อ้าง brief + `role-line-manager` เป็น [DEFAULT] · "ห้าม hardcode" ×3 | TC-E05/E08 (slot picker · ไม่ hardcode) | ✓ |
| NTF | 3 event (เปิดรับ/ยืนยัน/ผล) | NTF_BRIEF ✓ | event ⊆ brief · `train_session_opened`/`train_enroll_confirmed`/`train_result` · doa_* ไม่ประกาศเอง | TC-NTF01 | ✓ |
| CSQ | มูลค่าอบรม → EC (ไม่มี AC) | CSQ_BRIEF ✓ | BR-09 · `train.enrolled_paid` (EC) ×2 | TC-XT01/N01 | ✓ |
| DOCCFG | — (cert=soft ref · ไม่มีเลขรัน) | N/A ✓ | LOCK-07 · ไม่ใช้ doccfg | TC-N04 (negative) | N/A |

> หมายเหตุ: `prebrief_checklist.py` รายงาน `doccfg:true` เป็น **keyword false-positive** — PREBRIEF §12 + รอบ 1 ยืนยัน DOCCFG **ไม่ต้องมี** (cert soft ref, ไม่มีเลขรัน) · ไม่ใช่ DIVERGENCE

---

## OQ / WARN ที่ track (ไม่บล็อก — ต้องอยู่ในรายงาน)

| ID | เรื่อง | สถานะรอบ 2 |
|---|---|---|
| OQ-01 | FN-10 framing (checklist "แนะนำหลักสูตร" vs HTML/จอ "แนะนำผู้เรียน") | hook เนื้อในครบ · TC-E02 ติด `⚠ ยืนยัน anchor` (gap header) — ถ้อยคำ ไม่กระทบ logic |
| OQ-03 | Rate Card (F060) ยังไม่ dev → มูลค่า EC/ต้นทุนต่อหัว display-only | TC-XT04 verify display-only · BR-17 DYNAMIC ห้าม hardcode |
| OQ-04 | สาย DOA role-id + drift `role-hr-ld-head` vs `role-hr-dev-head` | TC verify **ไม่ hardcode** (TC-E05/E08) · role-id ปลายทาง = งาน DOA declaration (นอกขอบเขต TC coverage) |
| OQ-05 | RBAC (หัวหน้า สร้างได้/อนุมัติอย่างเดียว) | TC-C08 (manager create allow · precedent) + TC-P04 (SoD) — เคาะ RBAC จริงก่อน deploy |
| OQ-06 | ยกเลิกหลังส่ง EC → reverse policy | TC-CANEC01 verify **ไม่ auto-reverse** (conservative) · flag Finance |
| OQ-NTF-01 | event code จริง | TC-NTF01 ยืนยัน 3 event feature + doa_* ไม่ประกาศเอง · code ปลายทาง = NTF declaration |

### WARN — track (ไม่บล็อก · มีเหตุผลบันทึกแล้วใน Coverage Audit)

| # | เรื่อง | เหตุผลที่ไม่บล็อก |
|---|---|---|
| W1 | **error code 3 ตัวไม่มี TC ตรงที่ UI** — `ERR_NOT_AUTHENTICATED` (401) · `ERR_NOT_FOUND` (404) · `BR_NO_PENDING_STEP` (422) | backend guard ล้วน · ไม่มีทางเข้าที่ UI prototype (401 ไม่มี login flow · 404 hidden path · BR_NO_PENDING ครอบทางอ้อมใน TC-EC01) → ตรวจที่ backend integration |
| W2 | **edge/downstream 6 เคส mark `(ต้อง simulate)`** — TC-EC01/PR01/RACE01/EC06 + XT downstream | concurrent/lock/cross-module ต้อง mock/backend จริง · บน prototype = partial → ระบุใน Setup + Result schema (`blocked` + ระบุ mock ที่ต้องใช้) |

> W1/W2 = ของ backend-only ที่ตรวจที่ UI ไม่ได้ — บันทึกครบใน `testcases-อบรม.md` §Coverage Audit → "ข้าม (พร้อมเหตุผล)" · ไม่ใช่ gap ที่หาย

---

## Quality Gates ของ checker (self)
- [x] ทุก ✓ มี evidence (FN→TC id · BR→TC id · declaration→FRD section)
- [x] ไม่ invent เกณฑ์นอก contract (FUNCTION_CHECKLIST + FRD + PREBRIEF เท่านั้น)
- [x] item ตรวจไม่ได้ = ระบุเหตุผล (W1/W2 backend-only) ไม่ใช่ ✓ ลอย
- [x] scope creep = 0 (ไม่มี TC ทำสิ่ง unsupported "ได้" · G9 เป็น negative ยืนยัน "ทำไม่ได้")
- [x] BLOCK เฉพาะเมื่อ block-rule ไม่ครอบ — รอบนี้ไม่มี → PASS
- [x] Declaration coverage ครบ 3+1 (DOA/NTF/CSQ + DOCCFG N/A) · chip=detect (ไม่มี DIVERGENCE)

**สรุป:** FRD ↔ TC ไม่มี gap ที่บล็อก · ทุก FN/BR/AC/edge/permission/XT/LOCK มี TC · negatives 5/5 · uncovered BLOCK = 0 → **พร้อมส่ง dev** (เหลือ OQ ที่ BA/SEC/Finance เคาะปลายทาง ไม่บล็อก launch)
