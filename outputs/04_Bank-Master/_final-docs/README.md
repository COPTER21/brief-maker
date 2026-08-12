# 📦 Bank Master (F-BNK) — Dev Handoff Pack

> Feature: **บัญชีธนาคาร** · module Finance Foundation · master/registry (ใช้ร่วมฝั่งรับ Receipt + จ่าย PV)
> WF-01 pipeline COMPLETE · 2026-08-11 · **HTML = source of truth** (BRD/FRD/TC/UAT derive จาก HTML)
> รหัส: F-BNK (node F-0.21) · ปิด chain การเงิน: ผังบัญชี (COA) → กลุ่มบัญชี (Posting Group) → **บัญชีธนาคาร** → วิธีชำระเงิน

## 🚀 เริ่มยังไง (dev)
1. เปิด **`01_prototype/f-bank.html`** ใน browser — เล่นได้จริง = spec ที่มีชีวิต (source of truth)
2. อยากเข้าใจเร็วใน 2 นาที → เปิด **`08_tldr/FEATURE_TLDR_bank-master.html`** (ภาษาคน ไม่มีศัพท์ระบบ)
3. อ่าน **`03_brd/BRD_F-BNK.md`** ภาพรวมธุรกิจ + scope + rules + §14.6 Functions Cut
4. Implement ตาม **`04_frd/FRD_F-BNK_Pack/`** (แยก layer: UI/API/DB/LOGIC/RULES/TESTS)
5. ยึด **`05_ui-brief/`** สร้าง UI ให้ตรง prototype 1:1
6. ทดสอบด้วย **`06_testcases/`** (AI/browser-use) หรือ **`07_uat/`** (คนเปิดทำตามได้)

## 📂 มีอะไรบ้าง — ใครใช้
| โฟลเดอร์ | ไฟล์ | ใครใช้ |
|---|---|---|
| `00_context/` | PREBRIEF · FUNCTION_CHECKLIST | BA/PM/Dev — scope + scenarios + FN trace |
| `01_prototype/` | f-bank.html (single-file SPA) | **ทุกคน — source of truth** |
| `02_qc/` | UX · Coverage · E2E (R1/R2) reports | QA/Lead — หลักฐานคุณภาพ |
| `03_brd/` | BRD_F-BNK.md | PM/BA — ภาพรวมธุรกิจ |
| `04_frd/` | FRD Pack 9 ไฟล์ (FULL) | **Dev — สเปคพัฒนา** |
| `05_ui-brief/` | UI_BRIEF (extraction-based, as-built) | Dev (Frontend) — UI 1:1 |
| `06_testcases/` | testcases-F-BNK.md (96 เคส) | QA / AI test runner |
| `07_uat/` | UAT_bank-master.html (3.7MB, 76 เคส Lite) | End-user/ลูกค้า — ทดสอบเอง + พิมพ์ผล |
| `08_tldr/` | FEATURE_TLDR_bank-master.html | ทุกคน — หน้าปกสรุป 2 นาที (ELI5) |

## ✅ สถานะคุณภาพ
- html-generator-v8 conformance + token retrofit — **audit.sh FAIL=0** (self_audit residuals = documented, ไม่ zero-tolerance)
- qc-ux — PASS · qc-coverage — FN **25/25 + FN-40** · BR **07/07**
- **E2E playwright 2 รอบ — 36/36 · 0 JS error** (ยืนยัน 3 business rule + latent base-kit bug ครบ)
- **Manual test (user + PM/BA) — ผ่าน** (แก้ 4 จุด UX: CSV file picker จริง, status menu จัด layout+disable ค่าปัจจุบัน, header actions ชิดขวาบน, ลบบรรทัด "ลองด้วยไฟล์ตัวอย่าง")
- BRD Quality Gate 28/28 · FRD Coverage (Stories 8/8, Rules 10/10, Edges 13+10) · TC 96 เคส trace FRD ครบ · UAT 76 Lite (คง TC id เดิม, drop 20 = back-end/redundant)

## 🔑 Decisions สำคัญ (Strike 2026-08-11 — ดู FRD `07_LOCKED_DECISIONS` + BRD §15)
- **OQ-BNK-01 = NO** → เส้น Bank Master → Payment Method **ตัดทิ้ง** (PM คง COA-direct) — ไม่ต้อง expose ให้ PM
- **OQ-BNK-02 = binding OPTIONAL** → ไม่ผูกกลุ่ม GL ก็บันทึกได้ (view เตือน "GL post ไม่ได้") · picker เห็นเฉพาะ active + คงกลุ่มที่ผูกไว้เดิมแม้ draft
- **OQ-BNK-03 = CONFIRMED (IR-BNK-01)** → used>0 ล็อกเฉพาะ **ธนาคาร + เลขที่บัญชี** (field อื่นแก้ได้) · used = count เอกสาร Receipt/PV · ไม่โชว์ used บนจอ
- **OQ-BNK-04 = CONFIRMED** → Receipt/PV เลือกบัญชี active+ฝั่งตรง · ★ pre-select · snapshot ตอนบันทึก
- **GL Contract:** soft-ref → GL Posting Group (F-PG kind=bank) · resolve บัญชีเงินฝากผ่านกลุ่ม · master ไม่เก็บ COA ตรง · `GET /api/v1/gl/posting-groups?kind=bank&status=active` (generic F-PG-API-01)
- THB-only (สกุลเงิน disabled) · ไม่มีสายอนุมัติ (DOA null) · นำเข้า merge-only · ไม่มีลบเดี่ยว · FRD variant = FULL · CI = v8 CUBE Warm Light

## ❓ Open Questions (ต้องเคาะบางส่วนก่อน dev — ดู FRD `00_OVERVIEW` §0.8 + `07_LOCKED_DECISIONS`)
| # | ประเด็น | สถานะ |
|---|---|---|
| OQ-BNK-06 | GL posting_group source: mock ≠ f-postgrp as-built (3 drifts) → DEV ใช้ generic API-01 `?kind=bank&status=active` | 🔴 ก่อน dev integration GL |
| OQ-BNK-07 | นิยาม `used` ที่แม่นยำ (count เอกสาร Receipt/PV) → delete/lock guard · ผูกกับ Receipt/PV ที่ยังไม่สร้าง | 🔴 ก่อน dev guard จริง |
| OQ-BNK-08 | ระดับการ mask เลขบัญชี (view header mask แล้ว · table/def-grid?) | 🔵 P3 |
| [AI-DEFAULT] | optimistic-lock (AD-BNK-02) · idempotency = Phase-2.5 conservative default (ไม่มีใน HTML mock) | รอ confirm |

## ⚠️ Drift / อย่า implement ตาม mock (ดู UI_BRIEF §11 + FRD 02_API §2.6)
- **GL param:** ใช้ `?kind=bank` (ไม่ใช่ `?type=bank`) · active-only จริงคืน **KBANK เท่านั้น** (SCB=draft ถูกกรอง) — mock local list โชว์ทั้งคู่ผิด · ห้ามลอก `BANK_POSTING_GROUPS` seed
- **Validation drift (HTML wins):** import row KBANK-01 ในความจริงตอบ **`CODE_DUPLICATE`** (ไม่ใช่ `ACCT_DUPLICATE` ตาม FRD §6.10) เพราะ account_no ของ sample ต่างจากทะเบียน → ผ่านด่านเลขซ้ำ ไปโดน code ซ้ำ · TC anchor ไว้ที่ HTML-actual แล้ว (product ตัดสินว่าจะแก้ mock ให้เลขซ้ำจริงหรือปล่อย)
- **Dead code (ไม่ต้องพอร์ต):** `bulkPickDemo()` / `BULK_SAMPLE` (ปุ่ม "ลองด้วยไฟล์ตัวอย่าง" ที่ถอดออกแล้ว) · duplicate `.type-pill` CSS · hint-card CSS ที่ไม่ถูกใช้
- **as-built notes:** drawer = 680px (920 เฉพาะ ≤1180) · toast = bottom-right 3500ms · status menu = z-dropdown (ไม่ยกเป็น portal #95) · GL picker = native `<select>`
- optimistic lock/idempotency/RBAC/audit/multi-tenant = production (HTML เป็น mock client-side)
