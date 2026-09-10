# Coverage Report (รอบ 2 · FRD Pack + Test Cases vs Contract) — F-HR-EXPENSE (เบิกค่าใช้จ่าย / Expense Claim · F101)

- วันที่: 2026-09-10 · WF-01 **step 10** (ตรวจ *ทำครบมั้ย* รอบ 2 · ก่อนส่ง dev) · skill `qc-coverage-checker`
- คำถามรอบนี้: **spec (FRD) และ test (TC) ผูกทุก FN/BR/EC/LOCK/XT/permission ครบมั้ย + declaration ตรง FRD มั้ย** — ไม่ซ้ำรอบ 1 (HTML vs PREBRIEF, PASS)
- Artifacts ตรวจ:
  - FRD Pack: `FRD_F-HR-EXPENSE_Pack/` (00_OVERVIEW §0.12 Coverage Manifest · 05_RULES · 06_TESTS · 07_LOCKED · 02_API · 03_LOGIC)
  - Test cases: `testcases-เบิกค่าใช้จ่าย.md` (**76 เคส** / 13 group · มี Coverage Ledger + Business Rules/EC/Error/Permission/LOCK/XT tables)
  - Contract: `FUNCTION_CHECKLIST.html` (22 FN) + **FN-18/19/20 (3 PM/BA additions 2026-09-10)** = FRD §0.12 (25 FN) · `PREBRIEF.md` (S-01..15 · declarations)
  - Declaration briefs: DOA_BRIEF · DOCCFG_BRIEF · NTF_BRIEF (**ผู้ใช้เลือก doccfg+doa+ntf** · OQ-06)
- อ้างอิงร่วม: `expense.html` · `BRD_เบิกค่าใช้จ่าย.md` · `_COVERAGE_REPORT.md` (รอบ 1)

## Verdict: 🟢 PASS

| Metric | ผล |
|---|---|
| **FN ↔ TC** | **25 / 25** ทุก FN มี TC ≥1 (FN-01..17 + FN-90..94 + FN-18/19/20 · trace กลับ FN/AC/BR ใน Ledger) |
| **BR ↔ TC** (05_RULES §5.1) | **16 / 16** (BR-01..15 + BR-18 · ไม่มี BR-16/17 ในฟีเจอร์นี้ · block rule ไม่มีตัวไหนหาย) |
| **AC ↔ TC** (06_TESTS §6.1) | **18 / 18** (AC-01..16 + AC-17/18 edge → TC-CC/PR ครบใน §6.8 Trace) |
| **Edge cases** (05_RULES §5.5) | **8 / 8** (EC-01..08 · EC-05 = negative "ไม่มี path" OQ-05) |
| **Scope Lock** (07_LOCKED §7.0) | **10 / 10** (LOCK-01..10 ทุกข้อมีเคส verify) |
| **Cross-Module (XT)** (06_TESTS §6.9) | **5 / 5** (XT-01..05) |
| **Negatives "ห้ามมี"** (unsupported 7 + FN-40 style) | **9 / 9** (TC-N01..N09 = เรนเดอร์จริง verify absent) |
| **Error Catalog** (05_RULES §5.6) | 14 code → TC (บาง backend-only = simulate · ระบุใน W1) |
| **Permission** (05_RULES §5.3) | 3 role (maker/approver/officer) + SoD (self-approve=deny · officer=deny) + mask money ครบ |
| **Declaration ↔ FRD** (DOA/DOCCFG/NTF) | sync-read ครบ · ไม่มี hardcoded chain/รูปแบบเลข/ช่องทางแจ้งเตือน · **CSQ อ้างใน FRD แต่ไม่ได้ produce → W3** |
| **3 PM/BA touchpoints** (FN-18/19/20) | ครบทั้ง FRD + TC (ดูตารางล่าง) |
| **uncovered BLOCK** | **0** |
| ขัด contract / scope creep | 0 / 0 |

> เทียบรอบ 1: gap ที่ปิดแล้ว = ไม่มีค้าง (รอบ 1 PASS · NOT-CHECKED = declaration briefs → รอบนี้ตรวจแล้ว) · **เกิดใหม่ = 0** · รอบ 2 เพิ่มชั้นตรวจ spec/test ที่รอบ 1 ยังไม่แตะ (FRD rule เนื้อตรง + FN↔TC ledger + EC/LOCK/XT/error + declaration↔FRD)

---

## Matrix — 25 FN ↔ TC (evidence จาก Coverage Ledger · testcases §Coverage Ledger)

| FN | ความสามารถ | FRD (BR/AC) | TC (evidence) | ✓ |
|---|---|---|---|:--:|
| FN-01 | wizard 5 ขั้น | BR-14 · AC-01 | TC-W01/W02/WL01 | ✓ |
| FN-02 | หัวเอกสาร ผู้เบิก/วันที่/ช่องทางจ่าย | AC-01 | TC-W01/W03 | ✓ |
| FN-03 | line editor + VAT none/add/included + totals | BR-01 · AC-02 | TC-L01..L05 | ✓ |
| FN-04 | เกินเพดาน → เตือน + บังคับเหตุผล (ไม่ block) | BR-02 · AC-03 | TC-OC01..OC04 | ✓ |
| FN-05 | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ | BR-03 · AC-04 | TC-V01/V02/WL01 | ✓ |
| FN-06 | ตำแหน่ง/cc snapshot Movement ณ วันเบิก | BR-08 · AC-01 | TC-W03/DI01 | ✓ |
| FN-07 | ส่งอนุมัติจาก wizard/ใบเบิก | BR-04 · AC-05 | TC-S01/S02 | ✓ |
| FN-08 | DOA slot picker ตามวงเงิน (ไม่ hardcode) | BR-04 · AC-05 | TC-S01/S03/S04/S05 | ✓ |
| FN-09 | อนุมัติครบสาย → เลข EXP + PDF + 7C | BR-06/07 · AC-06 | TC-AP01/AP02/AP03 | ✓ |
| FN-10 | เลือกช่องทางจ่าย → ส่งจ่าย (hook) | BR-09 · AC-07 | TC-PAY01/TP01 | ✓ |
| FN-11 | แก้ยอดข้ามช่วง → re-resolve DOA | BR-05 · AC-05b | TC-RR01 | ✓ |
| FN-12 | แนบใบเสร็จตามนโยบายหมวด | BR-03 · AC-04 | TC-RC01/RC02 | ✓ |
| FN-13 | ตีกลับ → แก้แล้วยื่นใหม่ (reopen) | BR-18 · AC-08 | TC-RJ01/RJ02/RJ03 | ✓ |
| FN-14 | ยกเลิกก่อนอนุมัติ (soft archive) | BR-10 · AC-09 | TC-CX01/CX02 | ✓ |
| FN-15 | PDF tab a4 + tab ลายเซ็น | BR-06 · AC-10 | TC-VW03/VW04 | ✓ |
| FN-16 | "จ่ายแล้ว" อ่านจากปลายทาง display-only | BR-09 · AC-07 | TC-PAY02 | ✓ |
| FN-17 | view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + แนบ | AC-10 | TC-VW01/VW02 | ✓ |
| **FN-18** | touchpoint PV/petty (F091) + หักลบทดรอง (F103 display-only) | BR-11 · AC-11 · XT-03 | TC-TP01/TP02/TP03/ADV01 | ✓ |
| **FN-19** | 7C = FC/EC เท่านั้น (ไม่มี AC) | BR-07 · XT-01 | TC-AP03/XT01/N06 | ✓ |
| **FN-20** | scope self/all + role เจ้าหน้าที่ HR/Finance ไม่อนุมัติ | BR-12 · AC-12 | TC-P01/P02/P04/P05 | ✓ |
| FN-90 | list docPill + signprog + filter + empty | AC-13 | TC-G01/G02/G03 | ✓ |
| FN-91 | ตีกลับ/ยกเลิก confirm + soft archive | AC-08/09 | TC-RJ01/CX01/G04 | ✓ |
| FN-92 | validate + กัน double-submit + wizard ล็อก | AC-14 | TC-V01/WL01/ID01 | ✓ |
| FN-93 | audit append-only | AC-15 | TC-AU01/AU02 | ✓ |
| FN-94 | masking ตัวเงิน RESTRICTED ตาม role | AC-16 | TC-P02/P03/MASK01 | ✓ |

**Coverage Manifest (FRD §0.12) cross-check:** 25/25 แถวมีคู่ใน Ledger ✅ · **ทุก TC ที่นิยาม (76) trace กลับ requirement — ไม่มี orphan TC**

## Matrix — 3 PM/BA Touchpoints (FN-18/19/20) — ครบทั้ง FRD + TC

| FN | FRD (spec) | TC (test) | ✓ |
|---|---|---|:--:|
| **FN-18** touchpoint F091/F103 | §0.3(12) · BR-11 · AC-11 · XT-03 · 03_FN-16 + ENG-EXP-02 · LOCK-09 | TC-TP01 (PV/petty) · TC-TP03 (หักลบทดรอง display-only) · TC-ADV01 (EC-06 ทดรอง>ยอด) | ✓ |
| **FN-19** 7C = FC/EC (ไม่มี AC) | §0.3(13) · BR-07 · XT-01 · 03_FN-22 · LOCK-04 | TC-AP03 (emit ตอนอนุมัติ) · TC-XT01 (FC+EC) · TC-N06 (negative: ไม่มี AC) | ✓ |
| **FN-20** visibility scope + officer | §0.3(14) · BR-12 · AC-12 · §5.3 · 03_FN-19/20 · LOCK-10 | TC-P01 (self) · TC-P04 (officer เห็นทุกใบ+unmask แต่ approve deny) · TC-P05 (scope:all unmask) | ✓ |

## Matrix — Declaration ↔ FRD (Phase 0b · ผู้ใช้เลือก 3 ท่อ)

| ท่อ | เข้าเงื่อนไข | brief | FRD sync-read | TC | ✓ |
|---|---|---|---|---|:--:|
| DOA | อนุมัติตามวงเงิน (BR-04) | DOA_BRIEF ✓ | FREE ranges · resolve `doc_total` ผ่าน API-12 · ไม่ hardcode สาย/3-tier · role ทุกตัว `[DEFAULT — รอยืนยัน]` (master หาย) → OQ-01 | TC-S01/S03/S04/S05 (slot picker · ไม่ hardcode) · TC-RR01 (re-resolve) | ✓ |
| DOCCFG | เอกสาร EXP มีเลขรัน | DOCCFG_BRIEF ✓ | `EXP-<พ.ศ.>-NNNN` · ออกตอน approved-final (FN-11/23 · BR-06) · ตัวนับ global monotonic · no-gap · ไม่ hardcode รูปแบบ | TC-AP03 (เลข+PDF immutable) | ✓ |
| NTF | ยื่น/ผล-ตีกลับ/จ่าย/เกินเพดาน | NTF_BRIEF ✓ | 5 event (`exp.submitted/approved/rejected/paid/overcap`) map กลับ transition + HTML anchor · doa_*/FC/EC/pay_hook/advance_offset **ไม่ประกาศซ้ำ** | TC-S01/AP03/RJ01/OC04 (สังเกต toast · doa_* ไม่ประกาศเอง) | ✓ |
| CSQ | กระทบ ต้นทุน/มูลค่า/งบ (FC/EC) | **ไม่ produce** (ผู้ใช้เลือก 3 ท่อ · OQ-06) | FRD/HTML/NTF อ้าง `CSQ_BRIEF_F101` (7C emit) — **ดู W3** | 7C ครอบด้วย TC-AP03/XT01/N06 (FN-19) | ⚠ W3 |
| PDFDOC | print-spec | N/A (ผู้ใช้ไม่เลือก) | 07_LOCKED §7.6 ref เท่านั้น | — | N/A |

> chip DOCCFG/DOA/NTF (PREBRIEF §12) = ✓ · detect = need → **ตรงกัน ไม่มี DIVERGENCE ระดับ chip** (divergence ที่พบเป็น config detail: DOCCFG scope global-vs-branch → OQ-DOCCFG-04)

---

## OQ / WARN ที่ track (ไม่บล็อก — ต้องอยู่ในรายงาน)

> ทั้งหมดเป็น **open policy question** (BA/SEC/Finance/Strike เคาะปลายทาง) — ไม่ใช่ missing-TC ของ requirement ที่ spec แล้ว → **ไม่บล็อก launch** (ตามคำสั่งงาน)

| ID | เรื่อง | สถานะรอบ 2 |
|---|---|---|
| OQ-01 (A-EXP-03) | DOA ช่วงวงเงินจริง + role-id master + **CL-0013 แขวน** | TC verify **ไม่ hardcode** (TC-S01/S03/RR01) · role-id/ช่วงจริง = งาน DOA declaration (นอกขอบเขต TC coverage · CL-0013 blocker ระดับ config) |
| OQ-02 (A-EXP-04) | เพดานหมวด (group HR Config #107 ยังไม่มี → mock) | TC-N08 verify อ่าน-only (ไม่ CRUD) · ตัวเลขเพดาน = mock resolve · ไม่บล็อก launch |
| OQ-03 (A-EXP-02) | pay/GL hook contract (Phase B) | TC-PAY01/PAY02/N01 verify display-only (F101 ไม่จ่าย/ไม่ post) · contract ปลายทาง = Phase B |
| OQ-04 (RBAC) | mapping role→login + "ธุรการสร้างแทนผู้เบิก" | TC-P03/P04/PM01..03 verify SoD ปัจจุบัน · RBAC จริงเคาะก่อน deploy |
| OQ-05 | reverse-EC / release-FC on cancel-after-approval | TC-N09 + TC-EC05 verify **ไม่มี path** (cancel เฉพาะ draft · reopen เฉพาะ rejected) — conservative · ถ้า BA เปิด path ต้องนิยาม compensating FC/EC |
| OQ-EXP-04 | F117 Budget / F102 Welfare hook (Central-Plan edges) | TC-HK01/HK02 verify display-only mock (เตือน ไม่ block) · คงไว้ตาม Central Plan |
| OQ-DOCCFG-02/04 | doc-number พ.ศ. vs ค.ศ. + ตัวนับ global-vs-branch (DIVERGENCE) | ประกาศ default (พ.ศ. · global บนจอ vs branch ในบรีฟ) + ยก OQ ให้ BA/Finance · ไม่กระทบ FN-coverage |
| OQ-NTF-01b | event naming reconcile (`exp.*` 5 แยกผล vs `expense_*` 4 รวมผล) | ใบยึด FRD/HTML anchor (5 · dotted) · BA เคาะ registry แบบเดียว · ไม่กระทบ transition coverage |

### WARN — track (ไม่บล็อก · เหตุผลบันทึกแล้ว)

| # | เรื่อง | เหตุผลที่ไม่บล็อก |
|---|---|---|
| W1 | **error code backend-only ไม่มี anchor UI** — `ERR_NOT_AUTHENTICATED` (401) · `ERR_NOT_FOUND` (404) · `ERR_STALE_DATA`/`ERR_PERMISSION_REVOKED` (409/403 concurrent) | ไม่มีทางเข้าที่ prototype (401 ไม่มี login flow · 404 hidden path · concurrent ต้อง 2-session) → TC-EC01/EC02/DI01 mark **(ต้อง simulate)** · ตรวจที่ backend integration |
| W2 | **edge 3 เคส mark `(ต้อง simulate)`** — TC-EC01 (concurrent) · TC-EC02 (permission mid-flight) · TC-DI01 (cc=null seed) | ต้อง mock/backend จริง · บน prototype = partial → ระบุใน Setup + Result schema (`blocked` + ระบุ mock) |
| W3 | **FRD/HTML/NTF อ้าง `CSQ_BRIEF_F101` แต่ไม่ได้ produce** (ผู้ใช้เลือก doccfg+doa+ntf · OQ-06) | requirement เนื้อ (FN-19 · 7C=FC/EC) **spec ครบ + TC ครบ** (TC-AP03/XT01/N06) — ไม่ใช่ missing-TC · การ**เลือกรัน declaration เป็นสิทธิ์ผู้ใช้** (C3.10 · ไม่เลือก=ไม่รัน) → **reconcile item ให้ผู้ใช้เคาะ:** รัน `csq-declaration` เพิ่ม **หรือ** ผ่อนถ้อยคำ "ตาม CSQ_BRIEF_F101" ใน FRD/HTML · ไม่บล็อก verdict |

> W1/W2 = backend-only ที่ตรวจที่ UI ไม่ได้ (บันทึกใน testcases §Setup/Result schema) · W3 = declaration reference reconcile (ผู้ใช้ตัดสิน) — ทั้งหมด**ไม่ใช่ gap ที่หายเงียบ**

---

## Diff กับรอบ 1

| จุด | รอบ 1 (HTML) | รอบ 2 (FRD + TC) |
|---|---|---|
| gap ที่ปิดแล้ว | NOT-CHECKED: declaration briefs | ✅ ตรวจแล้ว DOA/DOCCFG/NTF sync-read ครบ (W3 = CSQ reconcile) |
| ยังค้าง | — | OQ-01..05 + OQ-EXP-04 + declaration-level OQ (ปลายทาง BA/SEC/Finance · ไม่บล็อก) |
| เกิดใหม่ | — | **0 BLOCK** · W3 (CSQ reference) เป็น reconcile ไม่ใช่ gap |

## Quality Gates ของ checker (self)
- [x] ทุก ✓ มี evidence (FN→TC id · BR→TC id · declaration→FRD section)
- [x] ไม่ invent เกณฑ์นอก contract (FRD §0.12 + 05_RULES + 07_LOCKED + PREBRIEF เท่านั้น)
- [x] item ตรวจไม่ได้ = ระบุเหตุผล (W1/W2 backend-only · W3 declaration scope) ไม่ใช่ ✓ ลอย
- [x] scope creep = 0 (negatives TC-N01..N09 ยืนยัน unsupported "ทำไม่ได้" · เรนเดอร์จริง)
- [x] BLOCK เฉพาะเมื่อ block-rule/requirement ที่ spec แล้วไม่มี TC — รอบนี้ไม่มี → PASS
- [x] Declaration coverage: DOA/DOCCFG/NTF ครบ (ผู้ใช้เลือก 3) · CSQ อ้างแต่ไม่ produce = W3 reconcile (ผู้ใช้ตัดสิน · ไม่ auto-BLOCK ตาม C3.10) · chip=detect (ไม่มี DIVERGENCE ระดับ chip)

**สรุป:** FRD ↔ TC ไม่มี gap ที่บล็อก · ทุก FN(25)/BR(16)/AC(18)/EC(8)/LOCK(10)/XT(5)/permission/negatives(9) มี TC · 3 PM/BA touchpoints (FN-18/19/20) ครบทั้ง spec+test · declaration DOA/DOCCFG/NTF sync ตรง FRD · **uncovered BLOCK = 0 → พร้อมส่ง dev** (เหลือ OQ ที่ BA/SEC/Finance เคาะปลายทาง + W3 CSQ reconcile ที่ผู้ใช้ตัดสิน — ไม่บล็อก launch)
