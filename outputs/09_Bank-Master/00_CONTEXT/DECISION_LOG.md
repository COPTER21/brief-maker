# DECISION LOG · F-BNK Bank Master
> pipeline run · started 2026-08-05 · pack: `Pack Brief Feature/09_Bank-Master/`

Feature = Shared Foundation master (Finance · W1) · **no tier** (Lite/Full ไม่เกี่ยว) · master 2 ระดับ: ธนาคาร (preset ธปท. 22) + บัญชีบริษัท.

## Pipeline scope decisions (locked with user, 2026-08-05)

| # | Decision | Rationale |
|---|---|---|
| D1 | **skill 1 html-generator-v7 = adopt `BankMaster.html` เดิมเป็น source of truth** (ไม่ re-gen) | HTML หัวเชื้อเสร็จแล้ว FN-01..06+90 wired, gate FAIL=0, Playwright PASS. Phase A จึงเริ่มจริงที่ skill 3. |
| D2 | **skill 2 thai-doc-pdf-generator = SKIP** | Bank Master เป็น master ไม่มีเอกสารธุรกรรม A4 พิมพ์ออก (ต่างจาก PO/PR/Invoice). |
| D3 | **skill 4 qc-coverage-checker baseline = PREBRIEF + Central Plan edges** | pack ไม่มี `workflow_graph.json`/`NODE_BRIEF` (ไม่ผ่าน plan-module-workflow-mapper). Baseline = FN-01..06+90 · BR-01..05 · S-01..06 · edges §9 (→Payment Voucher, →Bank Reconciliation, ←CoA). **ห้ามรัน plan-module-workflow-mapper หรือ skill นอกลิสต์ 9 ตัว.** |
| D4 | **OQ-1 / OQ-2 = `[AI-DEFAULT]` ตาม seed** | ยกไว้ตลอดสาย + flag ในทุกเอกสาร ไม่ประดิษฐ์ scope. ดู AI_DEFAULTS.md. |
| D5 | **กลุ่ม B scope additions = ไม่เพิ่มตอนนี้** (คงของเดิม) | เคารพ scope PREBRIEF + no-invented-scope. PromptPay = recommended future field (บันทึก flag ใน BRD/FRD, ตัดสินตอนทำ Payment/Receipt Voucher). purpose-tag + per-bank number-format = [AI-DEFAULT] ไม่ทำ. |

## Group A — conformance fixes (ให้ QC loop skill 3/4 จับ+แก้ ไม่ขยาย scope)
- **A1 Audit ฝั่ง bank preset** — เพิ่ม/ลบธนาคารต่างประเทศ ยังไม่ถูก log (FN-90 audit เฉพาะบัญชีบริษัท) → ขัด Global Contract #7 (append-only audit ทุก module).
- **A2 archived = terminal** — ยืนยัน archive แล้ว reactivate ไม่ได้ (ต่างจาก inactive ที่ active⇄inactive).
- **A3 doc-usage รับรู้ Bank Reconciliation** — archive-lock/used-in-doc ปัจจุบัน mock เฉพาะ Payment Voucher (`PV-2025-014`); Bank Recon ที่อ้างบัญชีก็ควรนับ.

## Phase A results (2026-08-05)
- **skill 3 qc-ux → 🟢 PASS** (BLOCK=0). แก้ 8 items + I-06 (list refresh หลัง create/edit — เพิ่ม `setTimeout(render,300)`). self_audit real hits=0. JS/render clean. Report: `02_QC/_UX_CHECK_REPORT.md`.
- **skill 4 qc-coverage → 🟡 WARN** (24/25, 0 block, no scope creep). Group A (A1/A2/A3) ยืนยันปิดครบ. Report: `02_QC/_COVERAGE_REPORT.md`.
- **W1 → ✅ RESOLVED (user เลือก guard used=0, 2026-08-05):** `removeBank` guard = ลบ custom bank ได้เฉพาะเมื่อ `used=0` (ไม่มีบัญชีอ้าง `bankCode`), ไม่งั้น block + warning toast · ปุ่มลบ disable เมื่อ used>0 (title บอกจำนวนบัญชีอ้าง). กัน soft-ref พัง + สอดคล้อง Contract #7. **ยังไม่ re-run Playwright รอบนี้** — spot-check ตอนเปิดไฟล์.
- **W2 (→ FRD):** Payroll OUT edge (§9) ยังไม่ถูกตั้งชื่อชัดใน UI (มีแต่ generic picker + CoA payroll GL). ไม่ block — ให้ FRD list Payroll เป็น named downstream consumer. doc-only, ไม่แก้ HTML.

## E2E test (pre-manual, 3 rounds · 2026-08-05)
- Round 1: ทุก flow PASS 3/3 + I-06a/b/c + W1 PASS 3/3 · console-app-err=0 · page-err=0 — **ยกเว้น Flow 8 (FN-02 default toggle) FAIL 3/3** จาก **Bug A**.
- **Bug A (SEVERE, fixed):** `renderDrawerEl` reset `className='drawer standard'` ทุก render → drop `is-open` → drawer ไถลออกนอกจอ (`translateX(100%)`) ตอน re-render ระหว่างเปิด (setViewTab/toggle/validate) → FN-02 เข้าไม่ถึง + error inline ไม่โชว์. Fix: preserve `is-open` (`wasOpen`).
- **Bug B (minor, fixed):** toast บัง submit button → `.toast { pointer-events:none }`.
- Re-test: 4 scenario ที่เคยพัง PASS หมด (ยืนยันด้วยภาพ `_e2e/retest/`). Verdict → 🟢 GREEN. (agent ไม่ได้ emit ตัวเลข 3-round ใหม่ — round 1 พิสูจน์ flow อื่นสะอาด 3/3 แล้ว + fix เป็น isolated drawer/CSS). Report: `02_QC/_E2E_TEST_REPORT.md`.
- **Bug C (SEVERE, fixed):** fix Bug A (drawer อยู่กับที่) เปิดโปง latent bug — `.modal-backdrop` z-index = `--z-backdrop`(50) < `.drawer`(51) → confirm modal จากใน drawer อยู่ใต้ drawer คลิกไม่ได้ → บล็อก deactivate (FN-04) + archive (FN-06). Fix: `.modal-backdrop` → `--z-modal`(60). RE-TEST 2 ยืนยัน 13/13 + ภาพ `_e2e/retest2/modal-over-drawer.png` (modal เหนือ drawer, ปุ่มคลิกได้). → **🟢 GREEN**.
- HTML edits หลัง QC ทั้งหมด (I-06×2, W1×2, Bug A, Bug B, Bug C) อยู่ใน `01_HTML/BankMaster.html` — input เดิมไม่แตะ. Bugs A/B/C fixed & verified; I-06/W1 verified 3/3 round 1.

## Manual test round 1 — feedback + corrections (2026-08-05)
PM/user แจ้ง 3 จุด. **AI ตีความผิดรอบแรก** (ลบ lucide icon ทั้งแอป + แก้ padding ผิดจุด) → user แก้ให้ → ตีความถูก + แก้ใหม่:
- **#3 "icon ไม่มีที่มา (เอา icon ออก)"** = ลบ **`.bank-logo`** (สี่เหลี่ยมสีตัวย่อ KBAN/SCB — โลโก้กุขึ้นเอง) เท่านั้น **ไม่ใช่** lucide icon ทั้งแอป. → ลบ `.bank-logo` ทุกที่ (2 tab + doc picker), restore lucide icon กลับครบ (data-lucide 109).
- **#1 "ประวัติการเปลี่ยนแปลงรายชื่อธนาคารเบี้ยว"** = section `.bank-audit-sec` **ชิดขอบเกิน** (padding) **ไม่ใช่** กล่อง icon ว่าง. → `.bank-audit-sec { padding:18px 18px 20px; border-top }` align กับ card content.
- **#2 "CRUD หาย"** = แค่ **tab ธนาคาร** (scope ถูกแล้ว). → view ทุกแถว + edit/delete custom + preset read-only. คงไว้.
- **บทเรียน:** ก่อนแก้ HTML รอบใหญ่ให้ยืนยัน scope กับ user + **backup ไฟล์ก่อนแก้ destructive** (รอบนี้ไม่มี backup ตอนลบ icon → กู้จาก input). backup อยู่ `02_QC/_bak/`.
- **Offline caveat (ยังคงอยู่):** lucide icon + ฟอนต์ Satoshi โหลดจาก CDN → offline จะ blank (ไม่ใช่ข้อ complaint ของ user รอบนี้). อนาคตถ้าต้อง offline-safe = inline icons/font.
- verify: data-lucide 109, 0 `.bank-logo`, padding ok, CRUD + Bug A/B/C/I-06/W1 regression pass, 0 error. ภาพ `02_QC/_fix3/`. build ~149KB.

## EC-14 resolution (2026-08-06) — post-Phase-B, user-approved
UI Brief จับ divergence: FRD [AI-DEFAULT] เขียน deactivate/archive = "เตือน+คง flag" แต่ HTML เคลียร์ทันที. user เลือก **"เตือน + เคลียร์"** (AI แนะนำ — clear ถูกต้องกัน dangling default ที่ชี้บัญชีซึ่งหายจาก picker; เพิ่ม warning ตามเจตนา FRD).
- HTML: `deactivateModalHTML`/`archiveModalHTML` เพิ่ม `.note.is-warn` (defNote) เมื่อ `defaultPay||defaultReceive`; confirm ยังเคลียร์ flag เหมือนเดิม. Playwright verify: warn โผล่เฉพาะ default (deactivate+archive), non-default ไม่โผล่, flag เคลียร์, 0 error, Bug A/C ไม่ regress. ภาพ `02_QC/_fix4/`.
- Docs sync: FRD (LD-06 + 05_RULES EC-14 + 03_LOGIC + 06_TESTS AC-05c + 00/01/02/07/INDEX), TC (E03/E06 คง cleared + เพิ่ม expected warning, ลบ divergence banner), UI Brief (D-6 + §9.6/§11.5), BRD (§14.4/§15 OQ-5). retag [AI-DEFAULT]→RESOLVED. TC id/count คงเดิม 76.
- UAT regen จาก TC ใหม่. _final-docs re-copy. **divergence ปิดแล้ว.**

## Effective pipeline
Phase A: ~~1 html-gen~~ (adopt) · ~~2 pdf~~ (skip) · **3 qc-ux** · **4 qc-coverage** → ⏸ STOP for user review
Phase B: 5 brd-generator-full · 6 frd-generator-v6 · 7 html-ui-brief · 8 ai-testcase-md-generator · 9 qa-friendly-html-generator (stop before each)

## Output
`outputs/09_Bank-Master/` staged: `00_CONTEXT` · `01_HTML` · `02_QC` · `03_BRD` · `04_FRD` · `05_UI_BRIEF` · `06_TESTCASES` · `07_UAT` · `_final-docs`.
Inputs under `Pack Brief Feature/` และ `Central Plan v2/` = **read-only ห้ามแก้**.
