# HANDOFF — F-ACC-DN · Debit Note (ใบลดหนี้ผู้ขาย · ฝั่งซื้อ) · Phase A → ba-done
> Lane W5Q#2 · 2026-09-20 · dep AP Invoice = ba-done ✓ · **รอทีม vibe — Phase B ออกเอกสารหลัง HTML นิ่ง + ผ่าน re-gate html-review-fix-order**

## ทำอะไรไปแล้ว
S0 RIF 82% → S0.5 baseline (7 Must ✅ · 2 ⏭) → S1 PREBRIEF (S-01..16 · BR-01..10) + CHECKLIST FN 21 (.md/.html) → S1.5 → S1.8 (doa 3 ช่วง/ntf/csq/doccfg/pdfdoc) → S2 HTML v9 (อ่าน SKILL.md ใหม่) → S3a WARN (BLOCK 0) → S3b PASS → S3c Playwright 30/30 → S4 BRD APPROVED

## ส่งมอบ
0_DIRECTION: RIF_v2 · BASELINE_ACC_DN · PREBRIEF · FUNCTION_CHECKLIST .md/.html · 1_HTML: F-ACC-DN_debit-note.html + _UX_CHECK_REPORT · _COVERAGE_R1 · _TECH_CHECK_S3c · 2_BRD: BRD_F-ACC-DN .md/.docx (§12.1 dn_applied_amount → ap_open_item · input_vat_line ติดลบ) · 5_DECLARATIONS: DOA_BRIEF · NTF · CSQ · DOCCFG (DN) · DN_print-spec · DECLARATION_INDEX · build: output/2026-09-20/_qdoc_build/f-acc-dn.js (+kernel.js · pw_dn.py)

## ห้ามแตะ
โครง Pattern Q · B2 v2 engine · DOA slot picker · hint/info-banner (#67.1) · ปุ่มสลับ view ขวาบน (#104) · DEMO badge (#105) · class toolbar (#106) · เปิดลดหนี้ลอย · ทำหน้า RTV/PV/JE จริง
✅ vibe ได้: layout/microcopy/mock · ลำดับ field step 2 · ตาราง ref tab
**Phase B ต้องมี section "Demo-only elements":** `[data-demo="persona-switch"]` · `[data-demo="pv-simulate"]`

## ASSUMED / OQ + owner
OQ-DN-01 ลดลอยปิด [ASSUMED ตาม OQ-CN-01] (Strike) · OQ-DN-02 tier 50k/300k [DEFAULT] (Policy Center) · OQ-DN-03 เรียกเงินคืน (Strike+Finance) · OQ-DN-04 ยกเลิกหลังอนุมัติ (Strike) · OQ-DN-05 เดือนภาษีซื้อ [ASSUMED เดือนวันที่ใบลดหนี้] (Tax) · OQ-AP-06 role id (Admin) · [ASSUMED contract] RTV {rtv_no, api_no, line, qty_returned} (W3-LITE) · DN reason master (config) · forward-wire JE F093

## DIVERGENCE / WARN
DIVERGENCE: ไม่มี · WARN S3a W-1..4 สืบทอด canonical · pdfdoc template/pdf = Phase B · kernel ไม่แก้

## คำสั่ง Phase B
html-review-fix-order → `run_state.py phase briefs/W5Q/F-ACC-DN docs` → FRD (Sync Read DOA/NTF/CSQ/DOCCFG + Demo-only elements) → TC → UI Brief
