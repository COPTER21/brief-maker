# _COVERAGE_REPORT_R2 — F-HR-ESS · ESS Portal (พนักงานทำเอง · F059)

> **Round 2** (FRD Pack + Test Cases · ก่อนส่ง dev) — แยกจากรอบ 1 (`_COVERAGE_REPORT.md` = HTML hook, verdict PASS)
> **Skill:** qc-coverage-checker · **Question:** "spec + test ผูกเรื่องครบมั้ย" (ไม่ตรวจ HTML hook ซ้ำ · ไม่ตรวจ CI/iron rules)
> **Date:** 2026-09-11 · **Archetype:** portal(aggregate) display-only + deep-link — **ไม่ใช่ Pattern Q** → Phase 0c surface coverage ข้าม (ไม่มี list/wizard/view/pdf/modals ของตัวเอง)
> **Contract:** `PREBRIEF.md` + `FUNCTION_CHECKLIST.html` (FN-01..11 + FN-90/92/93/94 = **15 FN** · unsupported NS-1..6) · FRD Pack v1.0 (STANDARD · 7 files) · `testcases-ess.md` (40 cases) · `BRD_ess.md`
> **Declaration briefs:** `NTF_BRIEF_F-HR-ESS.md` · `CSQ_BRIEF_F-HR-ESS.md` (doa/doccfg/pdf = NOT_NEEDED)

---

## VERDICT: **PASS** 🟢

FN↔TC ledger **15/15** (ทุก FN → TC ≥1) · rules ครบ (**BR-01..08 = 8/8** + **VR-1..5 = 5/5** + **LK-1..6 = 6/6** มี TC verify) · declaration coverage **ntf+csq ครบ · chip = detect · NO DIVERGENCE** (doa/doccfg/pdf = N/A justified) · display-only lock สะท้อนใน FRD (GET-only · ไม่มี mutation API) · scope creep **0** · **gap block 0**.

**Advisory (non-block · ไม่ใช่ coverage gap · ยกให้ owner team):**
1. **R15 cross-artifact parity** — เทียบได้แค่ MD testset ตอนนี้ (40 cases, internal manifest 15/15); QA-friendly HTML = **step 11 ยังไม่ทำ** → parity check เลื่อนไป post-step-11.
2. **OQ ปลายทาง blocking-at-wire** (owner-team resolve · ไม่บล็อก doc gate): **OQ-ESS-01** (CSQ event id) · **OQ-ESS-02** (5 deep-link routes) · **OQ-ESS-05** (backend self-enforce) · **OQ-ESS-NTF-01** (ENG-NOTIFY read-contract). ทุกจุด flag `[ASSUMED]`/OQ สม่ำเสมอทั้ง FRD+TC — ไม่ invent.
3. **FRD note stale (cosmetic):** 05_RULES §5.7 + 00_OVERVIEW §0.1/§0.12 เขียน "Declarations (NOTE only — ไม่ generate ใน pack นี้)" แต่ briefs (NTF+CSQ) **มีอยู่จริงแล้ว** (operator สร้างแยกตาม PREBRIEF §12 · CSQ_BRIEF header ยืนยัน "คัดมาไว้ในแพ็ก output ตามมติผู้ใช้"). Phase 0b requirement = **satisfied** (brief มีเมื่อเข้าเงื่อนไข chip) — เป็นแค่ถ้อยคำ FRD ล้าหลัง ไม่ใช่ช่องโหว่ coverage.

---

## §1 · FN ↔ TC Ledger (15/15) + Rule presence + Manifest anchor

| FN | สรุป | FRD anchor (§0.12) | TC (testcases-ess.md) | ✓ |
|---|---|---|---|:--:|
| FN-01 | หน้ารวมของฉัน (5 การ์ด read + launcher) | 01_UI P-01 · 06 AT-01 | TC-H01, TC-H02, TC-H03 | ✓ |
| FN-02 | สลิป + ประวัติ + YTD (self · all-or-nothing) | 02_API-02 · 05 BR-02 · 06 AT-02 | TC-P01, TC-P02, TC-P03, TC-P04 | ✓ |
| FN-03 | วันลา/โควตา (read) + "ยื่นลา" navigate-out | 03 FN-08 resolveDeepLink · 06 AT-03 | TC-L01, TC-L02, TC-L03 | ✓ |
| FN-04 | OT/เวลา/สแกน + ตารางกะ (read-only) | 05 BR-01 · 06 AT-04 | TC-D01, TC-D02 | ✓ |
| FN-05 | ใบเบิก (read) + "ยื่นเบิก" navigate-out | 05 BR-03 · 06 AT-05 | TC-E01, TC-E02 | ✓ |
| FN-06 | หนังสือรับรอง (read) + "ขอหนังสือ" navigate-out | 05 BR-01/BR-03 · 06 AT-06 | TC-E03, TC-E04 | ✓ |
| FN-07 | สวัสดิการ/อบรม/ใบรับรอง (read) | 05 BR-01 · 06 AT-07 | TC-E05 | ✓ |
| FN-08 | โปรไฟล์ (read · masked) + "ขอแก้ข้อมูล" navigate-out | 03 FN-05 maskRestricted · 05 VR-2 · 06 AT-08 | TC-E06, TC-E07, TC-E08 | ✓ |
| FN-09 | แจ้งเตือนของฉัน (consume ENG-NOTIFY feed) | 03 FN-06 consumeNotifyFeed · 06 AT-09 | TC-N01, TC-N05 | ✓ |
| FN-10 | เข้าถึงคนอื่น → 403 (self-access SecC) | 03 FN-04 enforceSelfScope · 05 BR-06/VR-3 · 06 AT-10 | TC-SEC01, TC-SEC02 | ✓ |
| FN-11 | surface ba-done → display-only + [ASSUMED] chip | 05 BR-07 · 06 AT-11 | TC-X05 | ✓ |
| FN-90 | ค้นหา/กรอง notif + empty state | 05 §5.4 VR-4 · 06 AT-12 | TC-N02, TC-N03, TC-N04, TC-N06 | ✓ |
| FN-92 | responsive (มือถือ) | 05 BR-05 · 06 AT-13 | TC-X03 | ✓ |
| FN-93 | audit การเข้าถึงข้อมูลตัวเอง (append-only) | 03 FN-07 appendAccessAudit · 05 BR-08 · 06 AT-14 | TC-E08, TC-SEC05 | ✓ |
| FN-94 | ปิดบัง/ไม่แสดงข้อมูลนอกขอบเขต self | 03 FN-04/FN-05 · 05 BR-06 · 06 AT-15 | TC-SEC03, TC-SEC04, TC-H04 | ✓ |

**Ledger result: 15/15 — ทุก FN มี TC ≥1, trace กลับ FN/AT/BR ได้** · Manifest cross-check (FRD §0.12) = 15/15 · S-01..S-11 mapped ผ่าน FN rows.

---

## §2 · Rules ↔ TC (Business / Validation / Scope-Lock)

### §2.1 Business Rules (05_RULES §5.1 · 8/8 present + TC)
| BR | present ใน 05_RULES | severity | TC | ✓ |
|---|:--:|---|---|:--:|
| BR-01 ห้าม CRUD surface อื่น (display-only) | ✓ §5.1 | FIXED/Prevent | TC-P03, TC-D02, TC-E05, TC-SEC03 | ✓ |
| BR-02 สลิป self · all-or-nothing | ✓ §5.1 | FIXED/Prevent | TC-P01, TC-P04, TC-SEC03 | ✓ |
| BR-03 ยื่นคำขอ = navigate (ไม่ทำ form) | ✓ §5.1 | FIXED/Trigger | TC-L03, TC-E02, TC-E04, TC-E07, TC-X01 | ✓ |
| BR-04 dashboard = สรุป read | ✓ §5.1 | CONFIGURABLE | TC-H01 | ✓ |
| BR-05 responsive | ✓ §5.1 | FIXED | TC-X03 | ✓ |
| BR-06 self-access เท่านั้น · คนอื่น=403 | ✓ §5.1 | FIXED/Error | TC-SEC01, TC-SEC02, TC-SEC03 | ✓ |
| BR-07 surface ba-done = [ASSUMED] soft ref | ✓ §5.1 | WARNING | TC-X05 | ✓ |
| BR-08 audit อ่าน append-only · masking self | ✓ §5.1 | FIXED | TC-E08, TC-SEC04, TC-SEC05 | ✓ |

ไม่มี block rule หาย/เจือจางใน FRD · CONFIGURABLE (BR-04) + WARNING (BR-07) ระบุ tag ชัด.

### §2.2 Validation Rules (05_RULES §5.4 · 5/5)
| VR | TC | ✓ |
|---|---|:--:|
| VR-1 deep-link ไม่ยืนยัน → [ASSUMED] chip + fallback | TC-X05, TC-X02 | ✓ |
| VR-2 RESTRICTED masking ตาม self · reveal → log | TC-E08, TC-SEC04 | ✓ |
| VR-3 employee_id ≠ self → 403 backend · ไม่ leak | TC-SEC01, TC-SEC02 | ✓ |
| VR-4 search/filter ไม่พบ → empty (ไม่ใช่ error) | TC-N03, TC-N06 | ✓ |
| VR-5 payslip all-or-nothing | TC-P01, TC-P04 | ✓ |

### §2.3 Scope Lock (00_OVERVIEW §0.11 · LK-1..6 · verify-by-TC)
| LK | เนื้อหา | TC verify | ✓ |
|---|---|---|:--:|
| LK-1 display-only · ห้าม CRUD feature อื่น | TC-P03, TC-D02, TC-E05, TC-SEC03 | ✓ |
| LK-2 ยื่นคำขอ = navigate ไป owner | TC-L03, TC-X01 | ✓ |
| LK-3 สลิป PS-1 · self · all-or-nothing | TC-P01, TC-P04 | ✓ |
| LK-4 self-access เท่านั้น · คนอื่น=403 | TC-SEC01, TC-SEC02 | ✓ |
| LK-5 surface ba-done = [ASSUMED contract] | TC-X05 | ✓ |
| LK-6 CSQ=SecC + NTF=อ่าน feed · ไม่มี doa/doccfg/pdf · audit append-only | TC-N01, TC-E08, TC-X04 | ✓ |

**Negative/verify-by-absence** (NS-1..6 ตัดโดยมติ) ครอบด้วย TC-P03/D02/E05/SEC03/X04 — ไม่มีการทดสอบ scope ที่ตัดออกเป็น feature (ถูกต้อง).

---

## §3 · Declaration Coverage (Phase 0b) — chip vs detect

Chip ประกาศ (PREBRIEF §12): **NTF ✓need · CSQ ✓need** · DOA/DOCCFG/PDF = no.

| ท่อ | เข้าเงื่อนไข? | detect | brief | chip=detect? | ✓ |
|---|---|---|---|:--:|:--:|
| **NTF** | ✅ consume ENG-NOTIFY feed (FN-09 · S-09) | consumer-only · **0 emit event** | `NTF_BRIEF_F-HR-ESS.md` ✓ (consume-only · ไม่มี doa_*) | ✅ | ✓ |
| **CSQ** | ✅ self-access PII → SecC (S-10/BR-06) | `ess.self_access` → ท่อ **SecC** | `CSQ_BRIEF_F-HR-ESS.md` ✓ (declared 1 event · ไม่ประกาศ OC/DC/AC/FC/SC) | ✅ | ✓ |
| **DOA** | ❌ ไม่มี action อนุมัติ/slot picker (portal อ่านอย่างเดียว) | absent (grep approval/mutation=0 รอบ1) | N/A (NOT_NEEDED) | ✅ | ✓ |
| **DOCCFG** | ❌ ไม่ออกเอกสาร/เลขรันเอง | absent (ไม่มี running-number pattern) | N/A (NOT_NEEDED) | ✅ | ✓ |
| **PDF** | ❌ สลิป/หนังสือ PDF จาก owner ต้นทาง | absent | N/A | ✅ | ✓ |

**→ NO DIVERGENCE.** chip ตรงกับ detect ทุกท่อ.

### §3.1 Declaration ↔ FRD sync (Phase 2)
- **CSQ:** FRD 05_RULES §5.7 sync-read `CSQ_BRIEF` · event `ess.self_access` flag **[ASSUMED · OQ-ESS-01]** (HTML anchors `ess.restricted_view` L2534 + `ess.access_denied` L2657 = 1↔2 reconcile ยังค้าง). FRD **ไม่ invent event id** · ไม่ประกาศ OC/DC ซ้ำ → event ใน FRD ⊆ brief ✓. TC-SEC05 mark PENDING จนกว่า OQ-ESS-01 ปิด (ถูกต้อง).
- **NTF:** FRD 03_LOGIC FN-06 `consumeNotifyFeed` · **ไม่มี `ENG-NOTIFY.emit(...)`** · ไม่ hardcode channel/email/LINE · read-contract `ENG-NOTIFY.list(employee_id, self)` flag [ASSUMED · OQ-ESS-NTF-01]. consume-only ตรง brief ✓.
- **ไม่มี hardcoded chain/ช่องทางแจ้งเตือน/รูปแบบเลขรัน ใน FRD** ✓.

---

## §4 · Display-only lock reflected in FRD (no mutation API)

| ตรวจ | Evidence | ✓ |
|---|---|:--:|
| API = GET-only (ไม่มี mutation endpoint) | 00_OVERVIEW §0.6 "API — GET only (aggregate read)" · §0.10 "02_API GET-only" · 02_API §2.4 navigate/consume เท่านั้น | ✓ |
| 03_LOGIC = read/aggregate/guard เท่านั้น (ไม่มี engine/mutation) | §0.1 "read/aggregate/guard functions เท่านั้น · ไม่มี engine · ไม่มี mutation API (R8 vacuously satisfied)" | ✓ |
| ไม่มี table mutation ของตัวเอง | 04_DB = read-model view refs + append-only `T_ess_access_audit` เท่านั้น | ✓ |
| LK-1..6 immutable ประกาศใน §0.11 · compliance check ผ่าน | §0.11 "ทุก API เป็น GET · ทุกปุ่มยื่น=navigate · ไม่มี table mutation" | ✓ |
| ยื่นคำขอ = navigate-out (ทุก TC negative ยืนยัน) | TC-L03/E02/E04/E07/X01 toast · TC-P03/X04 verify-no-write | ✓ |

Display-only / no-mutation lock **สะท้อนครบใน FRD** และผูก TC negative — สอดคล้องรอบ 1 (grep mutation/form/submit = 0).

---

## §5 · Scope Creep

**0 creep.** testcases-ess.md ระบุ Out-of-Scope NS-1..6 ชัด · ไม่มี FN เกิน 15 · ไม่สร้างเคสทดสอบ scope ที่ตัดออก (form ยื่น/ออกสลิป-PDF เอง/Manager self-service/อนุมัติ/config เมนู/เลขรัน) — ครอบด้วย negative verify-by-absence เท่านั้น. FUNCTION_CHECKLIST payload = 15 FN + unsupported NS-1..6 ตรงกับ FRD §0.3 + testcases §Out-of-Scope.

---

## §6 · Diff จากรอบ 1 (HTML → FRD+TC)

| สถานะ | รายการ |
|---|---|
| **ปิดต่อเนื่อง (รอบ1 ปิด · รอบ2 ยืนยันใน spec+TC)** | 3 BA gap (cert deep-link c[1] · ตารางกะ c[4] · CSQ anchor DIVERGENCE) — FRD encode ครบ (FN-06/FN-04/§5.7) · TC ครอบ (TC-E04/D02/SEC05) |
| **ยังค้าง (carry OPEN · non-block doc gate)** | OQ-ESS-01 (CSQ event id) · OQ-ESS-02 (deep-link routes) · OQ-ESS-05 (backend self-enforce) · OQ-ESS-NTF-01 (NTF read-contract) — owner-team resolve at wire |
| **เกิดใหม่** | — (ไม่มี gap/creep ใหม่) |

---

## §7 · Quality Gate (checker self-check)
- [x] ทุก ✓ มี evidence (FRD file/§ + TC id) — ไม่มีช่องเดา
- [x] ไม่ invent เกณฑ์นอก contract (PREBRIEF/FUNCTION_CHECKLIST/FRD §0.12)
- [x] item ที่ตรวจไม่ได้ = ระบุชัด (R15 QA-HTML parity = post-step-11 · ไม่ mark ✓ ลอย)
- [x] scope creep flag = 0 (ยืนยันแล้ว ไม่ตัดสินแทน user)
- [x] block rule ครอบครบ → verdict PASS
- [x] Declaration 0b ตรวจครบ 5 ท่อ · chip=detect · NO DIVERGENCE

**หมายเหตุ tension ที่ทราบแล้ว (ไม่ยกเป็น gap):** BR-05 mobile vs iron rule #97 = accepted tension.
