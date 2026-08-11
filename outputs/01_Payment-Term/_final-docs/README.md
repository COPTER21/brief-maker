# 📦 Payment Term (F-PAY) — Dev Handoff Pack

> Feature: **เงื่อนไขการชำระเงิน** · module Accounting · master/config (ใช้ร่วม P2P + S2C)
> WF-01 pipeline COMPLETE · 2026-08-10 · **HTML = source of truth** (BRD/FRD/TC derive จาก HTML)
> รหัส: F-PAY (เดิม F-PAYMENT-TERM-001)

## 🚀 เริ่มยังไง (dev)
1. เปิด **`01_prototype/f-payterm.html`** ใน browser — เล่นได้จริง = spec ที่มีชีวิต (source of truth)
2. อ่าน **`03_brd/BRD_F-PAY.md`** ภาพรวมธุรกิจ + scope + rules
3. Implement ตาม **`04_frd/FRD_F-PAY_Pack/`** (แยก layer: UI/API/DB/LOGIC/RULES/TESTS)
4. ยึด **`05_ui-brief/`** สร้าง UI ให้ตรง prototype 1:1
5. ทดสอบด้วย **`06_testcases/`** (AI/browser-use) หรือ **`07_uat/`** (คนเปิดทำตามได้)

## 📂 มีอะไรบ้าง — ใครใช้
| โฟลเดอร์ | ไฟล์ | ใครใช้ |
|---|---|---|
| `00_context/` | AI_DEFAULTS · DECISION_LOG · SCOPE_LOCK | BA/PM/Dev — decisions + locks + open questions |
| `01_prototype/` | f-payterm.html (single-file SPA) | **ทุกคน — source of truth** |
| `02_qc/` | UX · Coverage · E2E reports | QA/Lead — หลักฐานคุณภาพ |
| `03_brd/` | BRD_F-PAY.md + .docx | PM/BA — ภาพรวมธุรกิจ |
| `04_frd/` | FRD Pack 9 ไฟล์ (FULL) | **Dev — สเปคพัฒนา** |
| `05_ui-brief/` | UI_BRIEF (extraction-based) | Dev (Frontend) — UI 1:1 |
| `06_testcases/` | testcases-F-PAY.md (89 เคส) | QA / AI test runner |
| `07_uat/` | UAT_payment-term.html (2.9MB) | End-user/ลูกค้า — ทดสอบเอง + พิมพ์ผล |

## ✅ สถานะคุณภาพ
- html-generator-v8 conformance + token retrofit — **audit.sh FAIL=0**
- qc-ux — PASS with documented residuals · qc-coverage — FN **26/26** · BR **13/13**
- **E2E playwright 2 รอบ — 23/23 · 0 JS error** (เจอ+แก้ 2 bug: scroll jump-to-top, toast opacity/position)
- **Manual test (user + PM/BA) — ผ่าน** (แก้ 8 จุด UX)
- BRD Quality Gate 28/28 · FRD Coverage Manifest 8/8 stories · TC 89 เคส trace FRD ครบ · UAT 89=89 (1:1)

## 🔑 Decisions สำคัญ (ดู 00_context/DECISION_LOG)
- **D-08 (PM/BA): payment term ไม่ผูกที่ PR** → use_in = **7 เอกสาร** (PO/AP Inv/PV · SO/QUO/AR Inv/Receipt)
- ไม่มีสายอนุมัติ (DOA null) · ไม่มี CSV import/export · ไม่มีลบเดี่ยว · Credit trigger ล็อก=ทันที
- แก้ไขได้แม้ used>0 (เอกสาร snapshot) — ต่างจาก Tax Code
- FRD variant = FULL · CI = v8 CUBE Warm Light

## ❓ Open Questions (ต้องเคาะก่อน dev บางส่วน — ดู FRD 00_OVERVIEW §0.8 + AI_DEFAULTS)
| # | ประเด็น | สถานะ |
|---|---|---|
| OQ-PAY-07 | นิยาม `used` ที่แม่นยำ → delete guard | 🔴 ก่อน dev delete |
| OQ-PAY-04 | Deposit VAT flow (ใบกำกับภาษี ณ จุดรับเงิน + Tax Code Hook-2) | 🔴 ก่อน dev deposit GL |
| OQ-PAY-02 | ส่วนลดจ่ายเร็ว 1 ช่วง (SAP ได้ 3) | 🔵 future |
| OQ-ENG-REG | register **ENG-PT-01 (installment-validator)** + **ENG-PT-02 (payment-trigger-resolver)** กับ Architect | 🔴 ก่อน Phase 4 |
| [AI-DEFAULT] | AD-01 edit-yes/delete-no · AD-02 1 discount tier · AD-03 no multi-currency | รอ confirm |

## ⚠️ Drift / อย่า implement (ดู UI_BRIEF §11.2)
- HTML มี dead code `archived` status + askArchive/doArchive/reactivate + confirm-archive modal — **สถานะจริง = 3 ค่า (ร่าง/ใช้งาน/ไม่ใช้งาน)** ห้าม implement archive
- dead CSS (legacy toast/CSV stubs) — ไม่ต้องพอร์ต
- optimistic lock/idempotency/RBAC/audit/multi-tenant = production (HTML เป็น mock client-side)
