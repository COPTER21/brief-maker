# HANDOFF — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย) · Phase A จบ 2026-08-31 · runner v2.4
> อ่านก่อนแตะ HTML · ทิศทางใน 0_DIRECTION/PREBRIEF.md · FUNCTION_CHECKLIST.html (22 FN) · STANDARD_BASELINE.md (MUST 11)

## 1. feature นี้ทำอะไร (3 บรรทัด)
ใบเบิกค่าใช้จ่ายพนักงาน (Pattern Q + line editor) → ตรวจเพดานหมวด → อนุมัติตามวงเงิน (DOA threshold) → ออกเลข EXP-YYYY-NNNN + PDF → เลือกช่องทางจ่าย → hook GL/Payroll.
ผู้ใช้: พนักงาน (ยื่น) · ผู้อนุมัติตามวงเงิน (หัวหน้า/ผจก./ผอ.) · Finance (ติดตาม).
จบที่: ใบอนุมัติ ออกเลข+PDF ยิง 7C (FC/EC) และส่งสถานะจ่ายให้ปลายทาง (ไม่จ่ายเงิน/ไม่ post บัญชีเอง).

## 2. ของที่ส่งมอบ (Phase A)
| โฟลเดอร์ | ไฟล์ | สถานะ |
|---|---|---|
| 0_DIRECTION | HANDOFF · PREBRIEF · FUNCTION_CHECKLIST.html · STANDARD_BASELINE | ✅ |
| 1_HTML | expense.html (Q-document · wizard 5 ขั้น · view 4 tabs · a4 PDF) | ✅ audit FAIL=0(doc_archetype PASS) · qc-ux BLOCK=0 · coverage FN 22/22 |
| 2_BRD | BRD_expense.md/.docx | ✅ APPROVED |
| 5_DECLARATIONS | DOA(3-tier) · NTF(4) · CSQ(FC/AC/EC) · DOCCFG(EXP) · PDFDOC(template+sample.pdf+print-spec) | ✅ |
| 3_FRD · 4_TC | — | ⏳ Phase B |

## 3. ห้ามแตะ (LOCK)
- LK-1 DOA threshold (ยอด→สาย · resolve · ไม่ hardcode) · LK-2 ไม่จ่าย/ไม่ post เอง (hook) · LK-3 เพดานหมวด/legal จาก HR Config (#107) · LK-4 เลข EXP+สำเนา = ENG-DOC-NUM/STORE · LK-5 CSQ FC/AC/EC เท่านั้น · LK-6 soft ref·audit append-only·RESTRICTED
- ความสามารถ feature อื่น = soft reference (HR_DONE_CONTRACTS)

## 4. [ASSUMED] · OQ ค้าง — Strike/พี่เบิร์ด เคาะ
| # | เรื่อง | default | owner |
|---|---|---|---|
| A-EXP-01 | ช่องทางจ่ายเลือกต่อใบ | ผ่านเงินเดือน/โอนตรง | Strike |
| A-EXP-02 | จ่ายจริง/GL = hook display-only | [ASSUMED contract รอ FRD Phase B] | Strike |
| A-EXP-03 | DOA threshold 3-tier | <5k / 5k–50k / >50k [DEFAULT] | พี่เบิร์ด |
| A-EXP-04 | เพดานหมวด group ใน HR Config | mock · โครงอ้าง resolve | Strike |
| A-EXP-05 | เกินเพดาน warn vs block | warn + ต้องเหตุผล (ไม่ hard block) | Strike |
> DIVERGENCE: — (chip = detect ทุกท่อ)

## 5. จุดที่ vibe ได้อิสระ
layout/microcopy/ตัวอย่างข้อมูล · state ว่าง/โหลด/ผิดพลาด · **แต่คงไว้:** FN ทุกข้อ · wizard 5 ขั้นชื่อล็อก (Pattern Q #100) · view tabs detail/pdf/sign/history · line-tbl/VAT engine (calcLineVat/totals) · a4 · ปี พ.ศ. · feature :root --z-* tokens (อย่าลบ)

## 6. ขั้นถัดไป (Phase B)
```
python3 .claude/skills/feature-lane-runner/scripts/run_state.py phase briefs/W4/F-HR-EXPENSE docs
ใช้ skill feature-lane-runner v2.4 → lane docs "Expense Claim"
python3 .claude/skills/feature-lane-runner/scripts/pool.py set "Expense Claim" done --run W4
```
