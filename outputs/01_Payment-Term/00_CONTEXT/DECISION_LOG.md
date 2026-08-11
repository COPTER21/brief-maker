# DECISION LOG · Payment Term (F-PAY)

## 2026-08-10 — Pipeline kickoff
| # | Decision | ผู้ตัดสิน | เหตุผล |
|---|----------|-----------|--------|
| D-01 | Step 1 = **Adopt seed + v8 conformance pass** (ไม่ full re-gen) | user | seed ผ่าน E2E + FN wired แล้ว — รักษาของที่ gate-passed ไว้ |
| D-02 | **ข้าม Step 2** (thai-doc-pdf-generator) | user | Payment Term เป็น master ไม่มีเอกสารธุรกรรม/PDF (PREBRIEF OB-2) |
| D-03 | FRD variant = **FULL** | user | cross-module edges (PO/AR/AP) + 2 ENG + VAT-มัดจำ hook → dev ต้องการรายละเอียดครบ |
| D-04 | ใช้เฉพาะ 9 skills ที่ระบุ — ห้าม skill นอกลิสต์ | user | ข้อตกลง workflow |
| D-05 | หยุดทุก step ให้ user รีวิว | user | gating convention |
| D-06 | output = `outputs/01_Payment-Term/` (feature #1 ใน Pack Brief) | AI (confirmed) | repo นี้ยังไม่มี feature อื่นวิ่ง pipeline · outputs/ ว่าง |

| D-07 | Token retrofit (step 3) แทนการ waiver/re-gen | user | qc-ux BLOCK เป็น token/โครงสร้างล้วน — retrofit เก็บ behavior + แก้ root cause |

## GATE decisions (2026-08-10)
| # | Decision | ผู้ตัดสิน | เหตุผล |
|---|----------|-----------|--------|
| D-08 | **ถอด PR ออกจาก use_in** (OQ-PAY-08) | PM/BA | PR ไม่ผูก payment term (LD-01/FN-40 LOCK + ERP standard) — เจรจาเทอมที่ PO · use_in 8→7 · propagate BRD/FRD/TC |
| D-09 | แก้ G2 (dropdown desc) + G3 (hamburger) ทันที | user | minor UI, surgical, ไม่กระทบ behavior |

## E2E gate (2026-08-10)
- 2 รอบ · 23/23 · 0 JS error · **เจอ+แก้ BUG-E2E-01** drawer scroll jump-to-top (stale `_formScroll` — onTypeChange/close paths ไม่ล้าง) — ดู `02_QC/_E2E_REPORT.md`
- confirm class เดียวกับ [[html-v7-basekit-latent-bugs]] — E2E จับได้ที่ audit/qc-ux มองไม่เห็น

## Retrofit outcome (2026-08-10)
- เพิ่ม v8 token blocks (--fs/--sp/--r/--z) ใน :root · font_off 16→0 · z_adhoc 13→0 · Navy/blue ค้าง remap → warm (hex 41→24, rgba 19) · dead overlay markup ลบ · PREFLIGHT stamped · audit.sh FAIL=0
- **หลักฐานสำคัญ:** v8 gold reference เอง self_audit FAIL 6 counters → self_audit ≠ zero-tolerance gate
- Accepted residuals: spacing_off=86 (snap=destructive), hex 24 (semantic tints), stopprop 6 (behavior), missing_ids 8 (JS runtime IDs) — ดู _UX_CHECK_REPORT.md Fix Round 1
- backup: `01_HTML/f-payterm.PRE-RETROFIT.bak.html`

## สืบทอด (locked ก่อนหน้า — ดู SCOPE_LOCK.md)
- ตัด CSV import/export (มติ 2026-08-09)
- CI rebrand Navy v3.9 → v8 Warm Light (2026-08-09)
- Iron Rule #29 scroll preservation (fix 2026-08-09)
