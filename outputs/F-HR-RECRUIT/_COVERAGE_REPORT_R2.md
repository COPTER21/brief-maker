# _COVERAGE_REPORT_R2 — F-HR-RECRUIT (สรรหา / F127)

**Skill:** qc-coverage-checker · **จังหวะ:** **รอบ 2** (FRD Pack + Test Cases vs contract) · **โหมด:** feature-prebrief (F127 · ไม่มี workflow_graph)
**Subjects:** `FRD_F-HR-RECRUIT_Pack/` (00–07 + INDEX) · `testcases-สรรหา.md` (62 TC)
**Contract:** `FUNCTION_CHECKLIST.html` (21 FN + unsupported[] 5) + `05_RULES.md` (BR/VR/EC/Error/State) + `07_LOCKED §7.0`
**Declarations:** `DOA_BRIEF` · `NTF_BRIEF` · `CSQ_BRIEF` (DOCCFG/PDFDOC = NOT-NEEDED)
**วันที่:** 2026-09-03 · **ไม่แตะ** `_COVERAGE_REPORT.md` (รอบ 1)

---

## VERDICT: ⚠️ WARN (advisory · ไม่บล็อก · ไปต่อ step 11 ได้)

- **ไม่มี BLOCK** — ทุก block-severity rule/edge + ทุก XT + ทุก LOCK มี TC ≥1 พร้อม trace · ไม่มี declaration ท่อไหนเข้าเงื่อนไขแล้วขาด brief
- **FN↔TC: 21/21** · **BR: 10/10** · **VR: 5/5** · **XT: 4/4** · **LOCK: 7/7** · **Negative (แทน FN-40): 5/5** — uncovered block rules = **0**
- WARN = ของที่ **carry มาก่อนด่านนี้** (OQ ที่ tracked แล้ว) + ของที่ **ตรวจไม่ได้ที่ step 10** (R15 tri-parity รอ step 11) — **ไม่ใช่ gap ใหม่** ทั้งหมด

---

## 1 · FN ↔ TC Ledger (21/21 · ledger-first)

ทุก FN จาก FUNCTION_CHECKLIST มี TC ≥1 · cross-check 3 ชั้นตรงกัน (TC ledger · 06_TESTS §6.1 AT · 00_OVERVIEW §0.12 Manifest)

| FN | ต้องทำได้ | TC (testcases-สรรหา.md) | FRD trace |
|---|---|---|:--:|
| FN-01 | เปิดอัตรา | TC-A01, A02 | AT-01 · §0.12 ✓ |
| FN-02 | เปิดอัตราไม่มี Manpower → เตือน | TC-A03 | AT-02 ✓ |
| FN-03 | เพิ่มผู้สมัคร | TC-B01, B02 | AT-05 ✓ |
| FN-04 | ผูกผู้สมัครกับอัตรา | TC-B01 | AT-06 ✓ |
| FN-05 | consent PDPA gate | TC-B02, B05, C03, D04, N01 | AT-07/11 ✓ |
| FN-06 | เลื่อนสถานะ pipeline | TC-C01, C02 | AT-10 ✓ |
| FN-07 | นัดสัมภาษณ์ + แจ้งเตือน | TC-D01, X03 | AT-12 ✓ |
| FN-08 | ส่งอนุมัติ (req/offer) DOA slot | TC-A05, A06, E04, X04 | AT-03/15 ✓ |
| FN-09 | ประเมิน scorecard | TC-D02, D03 | AT-13 ✓ |
| FN-10 | สร้างข้อเสนอ (band freeze) | TC-E01, E02, X02 | AT-14 ✓ |
| FN-11 | ตอบรับ → hired → handoff (ไม่สร้าง employee) | TC-E06, X01, N02 | AT-16 · XT-01 ✓ |
| FN-12 | ปฏิเสธ/ถอนตัว | TC-F01, F02, E09 | AT-17 ✓ |
| FN-13 | ไม่ผ่าน → talent pool | TC-F03 | AT-18 ✓ |
| FN-14 | ตรวจซ้ำ email/phone → เตือน | TC-B03 | AT-08 ✓ |
| FN-15 | รายงาน funnel/time-to-hire | TC-G01, G02, G03 | AT-19 ✓ |
| FN-16 | ปิดอัตรา | TC-A08 | AT-04 ✓ |
| FN-90 | ค้นหา/filter + empty state | TC-H01, H02 | AT-20 ✓ |
| FN-91 | ปิด/ยกเลิก confirm + soft archive | TC-A08, F01 | AT-04/17 ✓ |
| FN-92 | field validate + double-submit | TC-A04, B04, E03, H03 | AT-21 ✓ |
| FN-93 | audit append-only | TC-H04 | AT-22 ✓ |
| FN-94 | ปิดบัง RESTRICTED ตาม role | TC-H05, H06, H07 | AT-23 ✓ |

**FN↔TC = 21/21 ✅** (FN ที่ขาด TC = 0)

> **หมายเหตุ 2 numbering scheme (ไม่ใช่ gap):** contract = FUNCTION_CHECKLIST **21 FN** (FN-01..16 + FN-90..94) · FRD ภายในใช้ **F127-FN-01..26** (implementation-level เช่น createCandidate=FN-08 ภายใน). ทั้งสอง reconcile ครบใน `00_OVERVIEW §0.12` (คอลัมน์ "อยู่ที่ใน Pack") — TC ผูกกับ scheme contract ถูกต้อง.

---

## 2 · Business Rules 05_RULES ↔ TC (Rule Coverage)

| Rule | severity | TC | ผล |
|---|---|---|:--:|
| BR-01 req DOA ครบก่อนประกาศ | **block** | TC-A05, A06, A09, N04 | ✅ |
| BR-02 consent PDPA gate | **block** | TC-B02, C03, D04, N01 | ✅ |
| BR-03 ทุก transition audit | fixed | TC-H04, C01 | ✅ |
| BR-04 offer DOA + เงินตามระดับ | **block** | TC-E04, E05, N03 | ✅ |
| BR-05 hired → handoff event (ไม่สร้าง employee) | **block** | TC-E06, X01, N02 | ✅ |
| BR-06 ผู้สมัคร RESTRICTED masking | fixed | TC-H05, H06, H07 | ✅ |
| BR-07 audit append-only + soft archive | fixed | TC-A08, F01, H04 | ✅ |
| BR-08 Manpower hook · null ไม่บังคับ | warn | TC-A03 | ✅ |
| BR-09 snapshot ผู้สัมภาษณ์ + freeze band | fixed | TC-D01, E01, X02 | ✅ |
| BR-10 duplicate → เตือน | warn | TC-B03 | ✅ |
| VR-01..05 (required/double-submit/band/DOA-dynamic/viewer) | — | A04·B04·E03 / H03 / E02 / A05·X04 / H08·H09 | ✅ 5/5 |

**BR block-severity ที่ขาด TC = 0** · **BR 10/10 · VR 5/5**

### Edge Cases + Error Catalog (uncovered = documented skips เท่านั้น)

| หมวด | covered | ข้ามพร้อมเหตุผล (NOT-CHECKED · ไม่ใช่ silent) |
|---|---|---|
| EC (05_RULES §5.5) | **10/12** | **EC-10** NTF fail queue/retry — หลังบ้าน ENG-NOTIFY (OQ-D4) · **EC-12** HM/interviewer ถูกลบ→snapshot — ต้องลบที่ Employee Master (นอก prototype · BR-09) |
| Error codes (§5.6) | **12/18** UI-observable | 6 backend-only: ERR_NOT_AUTHENTICATED/NOT_FOUND/NOT_IN_SLOT/DUPLICATE_IDEMPOTENCY_KEY/INVALID_STATE/BR_DOA_UNRESOLVED/BR_BAND_UNRESOLVED — prototype in-memory ไม่มี HTTP/async path (UI_BRIEF DR-02/03) · dev ทดสอบตอน bind API |

การข้ามทั้งหมดมีเหตุผลกำกับใน `testcases §Coverage Audit → ข้าม (พร้อมเหตุผล)` + DoD §6.4 (`retention/handoff jobs = feature flag OFF จนกว่า OQ-15/16 เคาะ`). **ไม่มี block/warn rule ที่ควรมี TC แล้วหายเงียบ.**

---

## 3 · Declaration ↔ FRD (Phase 0b · รอบ 2)

| ท่อ | เข้าเงื่อนไข | Brief | FRD sync read (evidence) | hardcode? | TC verify | ผล |
|---|:--:|:--:|---|:--:|---|:--:|
| **DOA** | ✅ (approve req+offer · status pending) | ✅ `DOA_BRIEF` | 03_LOGIC FN-03/FN-16 → `resolveDoaChain` (FN-26 · L32,111,165) · 02_API-05/06/18 · 07 LOCK-OB3 | **ไม่มี** (G7 ✅ · resolve runtime) | TC-A05, A06, E04, X04 (VERIFY "ไม่มีวงเงิน" + slot เปล่า) | ✅ |
| **NTF** | ✅ (interview/stage/offer×2) | ✅ `NTF_BRIEF` (4 event) | 02_API-14/15/20/21 · 03_LOGIC §3.1 emit · 01_UI §ntf · DOA events ไม่ประกาศซ้ำ (§2) | **ไม่มี** (channel = PREFS กลาง) | TC-X03, C01, C03, E05, E06, E08 | ✅ |
| **CSQ** | ✅ (PDPA SecC + hire EC) | ⚠️ `CSQ_BRIEF` **carried verbatim** | ยกจากแพ็กบรีฟ — **WF-01 ไม่มี csq-declaration skill** · ไม่ผ่าน quality-gate · รอ BA ทวน | — | consent/mask ครอบใน TC-B02/B06/H05-07 | ⚠️ carry |
| **DOCCFG** | ❌ (soft-ref · LOCK-DOCCFG) | N/A NOT-NEEDED | 07 LOCK-DOCCFG ✅ · ไม่มีเลขรัน/PDF | — | TC-N05 (VERIFY absence) | ✅ N/A |
| **PDFDOC** | ❌ (offer letter soft-ref) | N/A NOT-NEEDED | ไม่มี PDF gen | — | TC-N05 | ✅ N/A |

- **chip vs detect:** รอบ 1 ยืนยัน 0 DIVERGENCE · รอบ 2 brief สอดคล้อง chip ทุกท่อ — **ไม่มี DIVERGENCE ใหม่**
- **event ⊆ brief:** NTF FRD emit 4 = brief 4 · DOA chain ไม่มี array role hardcode ในไฟล์ feature/FRD ✅
- **DR-04 (tracked · ไม่ใช่ FRD gap):** HTML `candTerminate` ยิง `ntf('อัปเดตผลผู้สมัคร…')` แต่ NTF_BRIEF ไม่ประกาศ event terminate → **HTML-only mock drift**, บันทึกที่ `UI_BRIEF §11.2 DR-04` + OQ ให้ BA ("terminate ต้องแจ้งผู้สมัครไหม → ถ้าไม่ เอา ntf ออกตอน wire"). FRD/NTF_BRIEF **ไม่ได้ประกาศ event ที่ไม่ทดสอบ** — เป็น extra ฝั่ง HTML ที่ flag ไว้ถูกต้อง.

---

## 4 · Scope Lock + Negative (แทน FN-40)

| LOCK / unsupported | TC verify | ผล |
|---|---|:--:|
| LOCK-OB1 รับ→handoff ไม่สร้าง employee | TC-N02, X01 | ✅ |
| LOCK-OB2 consent + retention PDPA | TC-B02, B06 | ✅ |
| LOCK-OB3 DOA slot ไม่ hardcode | TC-A05, X04 | ✅ |
| LOCK-OB4 Manpower hook null | TC-A03 | ✅ |
| LOCK-OB5 RESTRICTED + audit append-only | TC-H04, H05 | ✅ |
| LOCK-DOA ไม่ผูก threshold เงิน | TC-A05 (VERIFY "ไม่มีวงเงิน") | ✅ |
| LOCK-DOCCFG ไม่มีเลขรัน offer | TC-N05 | ✅ |
| unsupported[1..5] (create employee/job board/assessment/PDF เลขรัน/CRUD band) | TC-N02, N05 (assert ไม่มีบนจอ) | ✅ |

**Negative "ของที่ห้ามมี" (feature ไม่มี FN-40): TC-N01..N05 = 5/5** — เรนเดอร์จริงแล้ว assert absence · **scope creep = 0** (ยืนยันต่อจากรอบ 1)

---

## 5 · Diff vs รอบ 1

| สถานะ | รายการ |
|---|---|
| **ปิดแล้ว (รอบ 1 ค้างไว้ตรวจรอบ 2)** | rules ใน FRD 05_RULES ✅ · FN↔TC ledger ✅ · Declaration↔FRD sync read (brief จริงมีแล้ว: DOA/NTF/CSQ) ✅ |
| **ยังค้าง (carry · tracked)** | OQ-15 · OQ-16 · OQ-17 · OQ-DOA · OQ-D1..D4 · OQ-R1 — ทุกตัวอยู่ใน `07 §7.3` + brief · ไม่มีตัวใหม่ |
| **เกิดใหม่** | **ไม่มี gap ใหม่** |

---

## 6 · WARN list (ไม่บล็อก · เรียงตามความเสี่ยง)

1. **W1 · OQ-DOA (carry · G1 ยืนยันเชิงบวกไม่ได้)** — `doa-contract.md` master ไม่มีในการติดตั้งนี้ → role id (`role-hiring-manager` · `role-hr-recruit-head`) ทุกตัวติด `[DEFAULT — รอยืนยัน]`. **ไม่บล็อก HTML/FRD/TC** (สาย resolve runtime) แต่ **บล็อกการ wire DOA จริง** — BA/พี่เบิร์ดต้องเคาะ role id ก่อน dev ตั้งค่า. (DOA_BRIEF §7 · 07 §7.5)
2. **W2 · R15 tri-parity = NOT-CHECKED (expected ที่ step 10)** — parity นับเคส MD ↔ QA HTML ↔ AI Testset ตรวจครบไม่ได้เพราะ QA-friendly HTML + AI Testset เป็น **step 11 (หลังด่านนี้)**. ฝั่ง MD self-manifest สอดคล้องภายใน (62 TC · 21/21 FN · Manifest cross-check §0.12 ✅). ให้ verify parity อีกครั้งหลัง step 11.
3. **W3 · CSQ_BRIEF carried (ไม่ผ่าน skill)** — WF-01 ไม่มี `csq-declaration` skill · ใบยกมา verbatim จากแพ็กบรีฟ · **รอ BA ทวนก่อนใช้จริง** (ระบุในหัวใบเอง). retention_until ผูก OQ-16.
4. **W4 · DR-04 terminate NTF (HTML-only mock)** — ดู §3 · flag ให้ BA แล้วใน UI_BRIEF · ไม่กระทบ coverage TC/FRD.
5. **W5 · EC-10/EC-12 + 6 backend error codes = NOT-CHECKED** — หลังบ้านล้วน (prototype in-memory) · deferred ให้ dev ทดสอบตอน bind API (DoD §6.4 · UI_BRIEF DR-02/03). มีเหตุผลกำกับครบ.

---

## 7 · OQ ที่ยืนยัน (เป็นตัวเดียวที่ค้าง · ไม่มีตัวใหม่)

| OQ | เรื่อง | owner | บล็อก? |
|---|---|---|---|
| OQ-15 | inbound handoff On/Offboard undesigned (fire-and-forget เท่านั้น) | Strike | ไม่บล็อกฝั่งเรา (BR-05) |
| OQ-16 | PDPA retention period + withdraw → Policy Center (Phase 4) | Strike/พี่เบิร์ด | ไม่บล็อก (display-only · LD-05) |
| OQ-17 | req cancelled ขณะ pipeline ค้าง (conservative default EC-08) | BA/HR | ไม่บล็อก (= DR-01) |
| OQ-DOA | ยืนยัน role id + slot 3 exec? (master หาย) | BA/พี่เบิร์ด | บล็อก **การ wire DOA จริง** เท่านั้น |
| OQ-D1..D4 | `[AI-DEFAULT]` concurrency/idempotency/permission/ntf-retry | BA confirm | ไม่บล็อก (TC-I01/I02 simulate) |
| OQ-R1 | Restricted Resources per-person ACL (Phase 2) | Security | ไม่บล็อก (รอบนี้ role masking) |

**NEW gap = ไม่มี** — OQ ข้างบนคือชุดเดิมที่ tracked แล้วทั้งหมด.

---

## สรุปสำหรับ WF-01

- **WARN (ไม่บล็อก)** → ผ่านด่าน coverage รอบ 2 · ไปต่อ **step 11 (UAT) + 11.5 (TL;DR)** ได้
- uncovered block rule/edge/XT/LOCK = **0** · declaration ท่อที่เข้าเงื่อนไขมี brief ครบ (DOCCFG/PDFDOC = N/A) · ไม่มี DIVERGENCE · ไม่มี scope creep · ไม่มี hardcoded chain
- WARN 5 ข้อ = carry ที่ tracked (OQ-DOA/CSQ/DR-04) + NOT-CHECKED ตามธรรมชาติของ step (R15 รอ step 11 · backend-only รอ bind API) — **ไม่มีอันไหนเป็น gap ใหม่**
- **ถึงคน:** BA เคาะ OQ-DOA (role id) + ทวน CSQ_BRIEF ก่อน dev wire · ยืนยัน DR-04 (terminate ต้องมี NTF ไหม) — ทั้งหมดไม่ขวาง handoff เอกสารรอบนี้
