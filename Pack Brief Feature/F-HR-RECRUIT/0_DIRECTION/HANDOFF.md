# HANDOFF — F-HR-RECRUIT · Recruit (สรรหา) · Phase A จบ 2026-08-31 · runner v2.4
> อ่านก่อนแตะ HTML · 0_DIRECTION/PREBRIEF.md · FUNCTION_CHECKLIST.html (21 FN) · STANDARD_BASELINE.md (MUST 12)
## 1. feature นี้ทำอะไร
สรรหา — เปิดอัตรา → คลังผู้สมัคร (PDPA) → pipeline board → ข้อเสนอจ้าง (DOA) → รับ → ส่งเข้า "เข้า-ออกงาน" (onboarding). ผู้ใช้: HR สรรหา · Hiring Manager · ผู้สมัคร. ไม่จ้างจริง/ไม่สร้าง employee เอง.
## 2. ส่งมอบ: 0_DIRECTION · 1_HTML(recruit.html master+pipeline) audit FAIL=0 · qc-ux BLOCK=0 · coverage FN 21/21 · 2_BRD(md/docx APPROVED) · 5_DECLARATIONS(DOA/NTF/CSQ + NOT_NEEDED doccfg/pdfdoc) · 3_FRD/4_TC ⏳Phase B
## 3. LOCK: DOA(req+offer · 17ส.ค.) · hired→Onboard handoff (ไม่สร้าง employee) · PDPA consent gate (SecC) · band อ่าน HR Config(#107) · ผู้สมัคร RESTRICTED · audit append-only · CSQ SecC/EC
## 4. [ASSUMED]/OQ: A-REC-01 เปิดอัตราไม่มี MP=hook (Strike) · A-REC-02 offer DOA ตามระดับ (พี่เบิร์ด) · A-REC-03 handoff Onboard=event (Strike) · A-REC-04 PDPA consent+retention (Strike) · DIVERGENCE: —
## 5. vibe อิสระ: layout/microcopy/mock · **คงไว้:** FN ทุกข้อ · consent gate · pipeline board stages · #104/#105/#106 · พ.ศ. · feature :root --z-* tokens
## 6. Phase B:
```
python3 .claude/skills/feature-lane-runner/scripts/run_state.py phase briefs/W5/F-HR-RECRUIT docs
ใช้ skill feature-lane-runner v2.4 → lane docs "Recruit / Candidate Pool"
```
