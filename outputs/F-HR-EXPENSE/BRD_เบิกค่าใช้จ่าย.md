# BRD — Expense Claim / เบิกค่าใช้จ่าย (F-HR-EXPENSE · F101)

> เอกสาร Business Requirement ฉบับสมบูรณ์ · WF-01 · SOW3.2 (Actor: BA)
> Mode: **Fresh (HTML-first)** — สกัด Screen Inventory + behaviour จาก HTML ที่ผ่าน re-gate แล้ว (`outputs/F-HR-EXPENSE/expense.html`)
> Conflict Priority ที่ใช้: **LOCK > PREBRIEF (business intent) > HTML (หน้าจอจริง)**

---

## Section 1 · Document Info

| หัวข้อ | ค่า |
|---|---|
| BRD ID | BRD-F-HR-EXPENSE |
| Feature | Expense Claim / เบิกค่าใช้จ่าย (ใบเบิกค่าใช้จ่ายพนักงาน) |
| Feature Code | F101 · F-HR-EXPENSE |
| Archetype | **Q-document** (เอกสารธุรกรรมมีเลขรัน EXP-YYYY-NNNN + PDF + line editor B2 v2 · Iron Rules #98–101) |
| ประเภท BRD | **New Feature** |
| Wave | W5 |
| Version | 1.0 |
| Status | **APPROVED** (ผ่าน Quality Gate ในตัว — ดู §14.7 · ทุก issue เปิดเป็น Open Question ไม่บล็อกเอกสาร) |
| Owner | BA — ทีม Human Capital (2BSimple) |
| Stakeholders | พนักงาน (ผู้เบิก/ยื่น) · ผู้อนุมัติตามวงเงิน (หัวหน้า/ผจก./ผอ. ตาม DOA) · เจ้าหน้าที่ HR/Finance (ติดตามสถานะ) · Finance/Payroll (ปลายทางจ่าย · hook) · SEC/PM |
| วันที่ | 2026-09-10 |
| Source of truth | HTML `expense.html` (2512 บรรทัด · audit FAIL=0 · qc-ux BLOCK=0 · coverage FN 22/22 · S 15/15) + PREBRIEF + FUNCTION_CHECKLIST (22 FN) + Central Plan row F101 + PM/BA additions 2026-09-10 (OQ-EXP-01/02/03) |

### 1.1 Changelog
- v1.0 (2026-09-10): Initial BRD via brd-generator-full (Fresh Mode, HTML-first) — สะท้อน scope PREBRIEF + FUNCTION_CHECKLIST (FN-01..17 + FN-90..94) + **3 PM/BA-approved additions 2026-09-10 formalized เป็น FN-18/19/20** (OQ-EXP-01 cross-feature touchpoints · OQ-EXP-02 7C=FC/EC · OQ-EXP-03 visibility scope + role ใหม่)

---

## Section 2 · Business Context

### 2.1 ปัญหา / โอกาส
การเบิกค่าใช้จ่ายพนักงานปัจจุบันทำนอกระบบ (กระดาษ/อีเมล/ไฟล์แยก) — ไม่มีใบเบิกกลางที่มีเลขรันตรวจสอบได้, สายอนุมัติตามวงเงินไม่บังคับ (เสี่ยงอนุมัติข้ามอำนาจ), เพดานค่าใช้จ่ายต่อหมวดไม่ถูกคุมอัตโนมัติ, และการจ่าย/ลงบัญชีทำแยกจากการอนุมัติทำให้ตรวจสอบย้อนหลังยากและคุมงบไม่ได้ อีกทั้งเงินทดรองที่ค้างของพนักงานไม่ถูกหักลบกับใบเบิกจริง ทำให้ยอดจ่ายซ้ำซ้อน

### 2.2 เป้าหมาย Business
1. มีใบเบิกค่าใช้จ่ายกลาง (หลายรายการ/หลายหมวด) พร้อมเลขรัน EXP-YYYY-NNNN + PDF + ลายเซ็นอนุมัติ
2. ตรวจเพดานหมวด (อ่านจาก HR Configuration) — เกินเพดาน = เตือน + บังคับเหตุผล (ไม่ hard block)
3. บังคับสายอนุมัติตามวงเงิน (DOA threshold · ช่วงวงเงินตั้งค่าอิสระที่ DOA กลาง) — ยอดต่างช่วง = สายต่างกัน
4. ออกเลข + สำเนา PDF ตอนอนุมัติ (immutable snapshot) + ยิงมูลค่าเข้า 7C (FC งบ / EC มูลค่า)
5. เลือกช่องทางจ่ายเป็น **hook display-only** (ผ่านเงินเดือน/โอนตรง/ใบสำคัญจ่าย PV/เงินสดย่อย) + หักลบเงินทดรองค้าง (soft-ref F103) — **F101 ไม่จ่ายเงิน/ไม่ post บัญชีเอง**

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง / จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| สัดส่วนใบเบิกที่ผ่านสายอนุมัติตามวงเงินครบ (DOA compliant) | ไม่มีระบบวัด — **เก็บ baseline ก่อน launch** | 100% ของใบที่อนุมัติ | audit ขั้นอนุมัติ (FN-07/08) เทียบ DOA resolve | รายเดือน |
| เวลาเฉลี่ยจากยื่น → อนุมัติครบ | ไม่มีข้อมูล — เก็บ baseline หลัง launch | ≤ 3 วันทำการ | timestamp audit trail ขั้นอนุมัติ (FN-08/09) | รายเดือน |
| สัดส่วนใบเบิกที่มีรายการเกินเพดานหมวด (ควบคุมงบ) | ไม่เคยวัดรวมศูนย์ | ติดตามแนวโน้ม (ลดลง) + ต้องมีเหตุผลครบ 100% | flag over-cap (FN-04) + over_reason | รายไตรมาส |
| ยอดหักลบเงินทดรองสำเร็จ (ลดจ่ายซ้ำ) | 0% (ไม่มี hook เดิม) | ติดตามแนวโน้ม (display-only จน F103 พร้อม) | advanceClear net payable (FN-18) | รายไตรมาส |

> คู่กับ §17.3 KPI ทุกตัว (C22)

### 2.4 ที่มา
- Central Plan row F101: archetype `Q-document` · wave `W5` · dec `[doa, ntf, csq, doccfg, pdfdoc]` · dep `OP✓ · CL-0013 ผู้บริหาร (แขวน 31 ส.ค.)`
- LANE_BRIEF + STANDARD_BASELINE (MUST 11 · lifecycle 8 state) · dep CONFIG/MOVE/PAYROLL
- Central Plan edges (dep contract): F102→F101 (ctl สิทธิ์สวัสดิการกำกับวงเงินเบิก) · F103→F101 (flow เคลียร์เงินทดรองด้วยใบเบิกจริง) · F059→F101 (flow พนักงานยื่นเบิกเอง) · F101→F109 (flow อนุมัติเบิก→จ่ายคืน) · F101→F091 (flow เบิกย่อยจ่ายผ่านเงินสดย่อย) · F101→F117 (ctl ใบเบิกตรวจงบก่อนอนุมัติ)
- **PM/BA 2026-09-10:** 3 มติเพิ่ม (OQ-EXP-01/02/03) เคาะแล้ว อยู่ใน HTML แต่ยังไม่อยู่ใน PREBRIEF/FUNCTION_CHECKLIST → formalize เป็น FN-18/19/20 ในเอกสารนี้

---

## Section 3 · Scope

### 3.1 In Scope
1. สร้างใบเบิกผ่าน **wizard 5 ขั้น** (เลือกแหล่งที่มา › ข้อมูลหลัก › รายการค่าใช้จ่าย › เอกสารแนบ › ตรวจสอบและยืนยัน) (FN-01)
2. หัวเอกสาร: ผู้เบิก (combobox) · วันที่ (พ.ศ.) · ช่องทางจ่าย · ตำแหน่ง/ศูนย์ต้นทุน snapshot ณ วันเบิก (FN-02, FN-06)
3. รายการค่าใช้จ่าย (line editor B2 v2): วันที่ · หมวด · รายละเอียด · จำนวนเงิน · VAT none/add/included + ยอดรวม/VAT/สุทธิ (FN-03)
4. เพดานหมวด (อ่านจาก HR Config) — เกิน = เตือน + บังคับเหตุผล (ไม่ hard block · A-EXP-05) (FN-04)
5. Validation ก่อนส่ง: ต้องมี ≥1 รายการ + ยอด > 0 + แนบใบเสร็จตามนโยบายหมวด (FN-05, FN-12)
6. ส่งอนุมัติ → **DOA slot picker ตามวงเงิน** (ช่วงวงเงินตั้งค่าอิสระที่ DOA กลาง · ไม่ hardcode สาย) (FN-07, FN-08)
7. แก้ยอดหลังส่ง → re-resolve สาย DOA ถ้าข้ามช่วงวงเงิน (FN-11)
8. ตีกลับ (ระบุเหตุผล) → แก้แล้วยื่นใหม่ · ยกเลิกก่อนอนุมัติ (soft archive) (FN-13, FN-14)
9. อนุมัติครบสาย → ออกเลข EXP-YYYY-NNNN + เก็บสำเนา PDF + ยิง **7C (FC งบ / EC มูลค่า)** (FN-09)
10. มุมมองเอกสาร: tabs รายละเอียด › PDF Preview (a4) › ลายเซ็น/อนุมัติ (DOA timeline) › ประวัติ (audit) + เอกสารแนบใน tab รายละเอียด (FN-15, FN-17)
11. เลือกช่องทางจ่าย → ส่งจ่าย (**hook display-only**) + สถานะ "จ่ายแล้ว" อ่านจากปลายทาง (Payroll/Finance) (FN-10, FN-16)
12. **[FN-18 · PM/BA 2026-09-10 · OQ-EXP-01]** จุดเชื่อมข้ามฟีเจอร์ (touchpoint · ไม่ใช่ระบบเต็ม):
    - (a) ช่องทางจ่ายเพิ่ม "ใบสำคัญจ่าย (PV)" + "เงินสดย่อย (F091)" เป็น hook display-only
    - (b) "เคลียร์เงินทดรอง หักลบอัตโนมัติ" = soft-ref F103 · ยอดจ่ายสุทธิ = ยอดใบเบิก − เงินทดรองค้าง (display-only) — F101 **ไม่ออก/ไม่ปรับยอดทดรองเอง** ส่งค่าหักลบให้ F103
13. **[FN-19 · PM/BA 2026-09-10 · OQ-EXP-02]** 7C = **FC/EC เท่านั้น (ไม่มี AC)** — สะท้อนใน events/CSQ (§12.1)
14. **[FN-20 · PM/BA 2026-09-10 · OQ-EXP-03]** ขอบเขตการมองเห็น: ผู้เบิก/ธุรการ `scope:self` เห็นเฉพาะใบของตน · **role ใหม่ "เจ้าหน้าที่ (HR/Finance)"** `scope:all` เห็นทุกใบ + เงินเต็ม (ไม่มาสก์) แต่ **ไม่ใช่ผู้อนุมัติ DOA**
15. กติกากลาง: list docPill + signprog + filter + empty (FN-90) · ตีกลับ/ยกเลิก confirm + soft archive (FN-91) · validate + กัน double-submit + wizard ล็อกลำดับ (FN-92) · audit append-only (FN-93) · masking ตัวเงิน RESTRICTED ตาม role (FN-94)

### 3.2 Out of Scope (ดู §14.6 · unsupported 7 — ตัดโดยมติ)
1. **จ่ายเงินจริง / โอน / ตัดจ่าย & GL posting** — hook display-only เท่านั้น (A-EXP-02 · ไปที่ Finance/Payroll/Accounting)
2. **ระบบเงินสดย่อย / ออกเงินทดรองเต็มรูป** — อยู่ที่ F091 (Petty Cash) / F103 (Advance) · F101 ต่อ**แค่จุดเชื่อม** (touchpoint) (OQ-EXP-01)
3. **เบี้ยเลี้ยง / ค่าน้ำมันต่อกิโลเมตร (mileage)** — NICE ไม่รองรับรอบนี้
4. **คำขออนุมัติเดินทางล่วงหน้า (travel request/authorization)** — NICE
5. **หลายสกุลเงิน** — THB only รอบนี้
6. **อ่านใบเสร็จอัตโนมัติ (OCR)** — ไม่รองรับ
7. **สร้าง/แก้เพดานหมวด/นโยบายเอง** — อ่านจาก HR Configuration (#107) เท่านั้น

### 3.3 Assumptions
- Employee Master · HR Configuration (F164 · #107) · Movement (assignment/resolve) พร้อมใช้งาน
- เพดานหมวด/รายการหมวด **[A-EXP-04]** ยังไม่มี group นี้ใน HR Config → mock · โครงอ้าง `resolve(date, company_id)` (ห้าม hardcode ในโค้ด)
- สายอนุมัติจริงมาจาก DOA กลาง (F-DLG-001 · Policy Center) — feature ประกาศเท่านั้น · **CL-0013 (สายอนุมัติผู้บริหาร) แขวน 31 ส.ค.** → OQ
- ปลายทางจ่าย (Payroll HK-1 / Finance / F091 / F109) + เงินทดรอง (F103) + งบ (F117) + สิทธิ์สวัสดิการ (F102) = อ่าน/ส่ง hook เท่านั้น (display-only) — ของจริงอ่านตอน dev
- วันที่แสดงเป็น พ.ศ. (2569) · VAT 7%

### 3.4 Scope Lock ⭐

**scope_lock_ref:** LANE_BRIEF + STANDARD_BASELINE (MUST 11 · lifecycle 8 state) + Central Plan row F101 (dec/dep) + PM/BA 2026-09-10 (OQ-EXP-01/02/03)

| LOCK-ID | มติที่ล็อก | ผลต่อ scope |
|---|---|---|
| LOCK-01 | อนุมัติ = **DOA threshold ตามวงเงิน** · ช่วงวงเงิน FREE ตั้งค่าอิสระที่ DOA กลาง · **ไม่ hardcode สาย/ไม่ใช่ 3-tier ตายตัว** | FN-07/08/11 · BR-04/05 |
| LOCK-02 | เลข EXP-YYYY-NNNN + สำเนา = ENG-DOC-NUM/STORE (doccfg) · ออกตอนอนุมัติ (immutable) | FN-09/15 · BR-06 |
| LOCK-03 | จ่ายจริง/post = **hook display-only** (Payroll/โอน/PV/petty/Accounting) — F101 ไม่ทำเอง | FN-10/16/18 · BR-09 · Out #1/#2 |
| LOCK-04 | 7C = **FC + EC เท่านั้น (ไม่มี AC)** — Accounting/Expense ปลายทางเป็นตัวลงบัญชี | FN-09/19 · BR-07 · §12 (OQ-EXP-02) |
| LOCK-05 | เพดานหมวด/นโยบาย = **อ่านจาก HR Config** (#107 · effective_date) — ไม่ CRUD | FN-04/12 · BR-02 · Out #7 |
| LOCK-06 | ตำแหน่ง/ศูนย์ต้นทุน = **snapshot Movement ณ วันเบิก** (soft ref · null≠ไม่มี) | FN-06 · BR-08 |
| LOCK-07 | audit **append-only** + เงิน **RESTRICTED masking** + ไม่มี hard delete | FN-93/94 · BR-10 |
| LOCK-08 | over-cap = **warn + บังคับเหตุผล (ไม่ hard block)** (A-EXP-05) | FN-04 · BR-02 |
| LOCK-09 | **[OQ-EXP-01]** cross-feature = touchpoint display-only (PV/petty F091 · หักลบทดรอง F103) — F101 ไม่ออก/ปรับ ledger ปลายทาง | FN-18 · Out #2 |
| LOCK-10 | **[OQ-EXP-03]** visibility scope: ผู้เบิก/ธุรการ=self · เจ้าหน้าที่ HR/Finance=all+unmask+ไม่อนุมัติ | FN-20 · §4 · §16 |

**SCOPE DRIFT:** — (ไม่พบ In-Scope ที่เกินมติ) · HTML สอดคล้อง LOCK ทุกข้อ
- HTML มี hook display-only เสริม 2 จุดที่**ไม่อยู่ใน PREBRIEF เดิม** แต่มาจาก Central Plan edges: **F117 Budget Control** (LK edge `F101→F117 ctl`) + **F102 Welfare สิทธิ์คงเหลือ** (LK edge `F102→F101 ctl`) — ทั้งคู่ mock/display-only มีป้ายกำกับชัด → บันทึกเป็น In-Scope §3.1(11)/§12.1 (ยืนยัน scope กับ BA · **OQ-EXP-04**) ไม่ตัด/ไม่รับรองเงียบ

---

## Section 4 · User Roles & Permissions

> HTML มี persona demo 3 ตัว (admin/mgr/officer) เป็น scaffolding ทดสอบสิทธิ์ (`.demo-strip` #105) — RBAC + scope จริงตั้งที่ระบบสิทธิ์กลาง/login

| Role | เห็นใบ (scope) | สร้าง/ยื่น/แก้ | ยกเลิก (ร่าง) | อนุมัติ/ตีกลับ (DOA) | เห็นตัวเงิน (unmask) |
|---|:--:|:--:|:--:|:--:|:--:|
| ผู้เบิก / ธุรการ (`admin`) | **เฉพาะใบของตน** (scope:self) | ✅ (ใบของตน) | ✅ | ❌ | ✅ ใบของตน · ❌ ใบคนอื่น (mask ••••) |
| ผู้อนุมัติ (DOA · `mgr`) | ทั้งหมด (scope:all) | ✅ | ✅ | ✅ | ✅ (ต้องเห็นเต็มเพื่ออนุมัติตามวงเงิน) |
| **เจ้าหน้าที่ (HR/Finance) (`officer`) [FN-20 · OQ-EXP-03 ใหม่]** | ทั้งหมด (scope:all) | ✅ ติดตาม | — | **❌ ไม่ใช่ผู้อนุมัติ** | ✅ (unmask · ติดตาม/กระทบยอด) |

- **Scope guard (FN-20):** `visibleDocs()` — scope:self กรองเฉพาะ `d.emp===self`; scope:all เห็นทุกใบ (HTML L2170-2173)
- **Approval guard:** อนุมัติ/ตีกลับได้เฉพาะ role ที่ `approver:true` (`canApprove()` L2169) — เจ้าหน้าที่ HR/Finance เห็นทุกใบแต่กดอนุมัติไม่ได้ (OQ-EXP-03 เจตนา)
- **Masking (FN-94 · BR-10):** ตัวเงิน RESTRICTED · mask ยอด "ใบของคนอื่น" สำหรับ role ที่ `mask:true` · ใบของตน/ผู้อนุมัติ/เจ้าหน้าที่ เห็นเต็ม (`maskM()` L2171)
- **OQ-04 (RBAC):** mapping role→login จริง + สิทธิ์ "ธุรการสร้างแทนผู้เบิก" ต้องให้ SEC/BA เคาะ

---

## Section 5 · User Journey (with COSO)

### 5.1 Happy Path — ใบเบิกยอดเข้าสาย DOA (มีวงเงิน)

| # | Step | Route/Overlay จริง | Maker | Checker | Approver | System |
|:--:|---|---|---|---|---|---|
| 1 | สร้างใบเบิก (wizard step 1-2: แหล่งที่มา + หัวเอกสาร) | list → `openCreate()` wizard | ผู้เบิก | — | — | ผู้เบิก combobox · ตำแหน่ง/cc snapshot Movement (FN-02/06) |
| 2 | เพิ่มรายการค่าใช้จ่าย (step 3 · B2 line editor) | wizard step3 `lineEditor()` | ผู้เบิก | — | — | totals()/VAT · flag over-cap (FN-03/04) |
| 3 | แนบเอกสาร (step 4) + ตรวจสอบยืนยัน (step 5) | wizard step4-5 | ผู้เบิก | — | — | guard receiptRequired + canSubmit grand>0 (FN-05/12) |
| 4 | ส่งอนุมัติ — DOA slot picker (เลือกคนตามตำแหน่งแต่ละขั้น) | modal DOA slot picker | ผู้เบิก | — | — | resolveDoa(total) → สายตามช่วงวงเงิน · **NTF: ยื่น** (FN-07/08) |
| 5 | อนุมัติแต่ละขั้น (1-3 ขั้น ตามวงเงิน) | view › ลายเซ็น/อนุมัติ | — | หัวหน้าสายงาน | ผจก./ผอ. | ครบสาย → approved (FN-08) |
| 6 | ระบบออกเลข + PDF + 7C | (auto ตอนอนุมัติครบ) | — | — | — | EXP-2569-NNNN + สำเนา PDF + **FC/EC (ไม่มี AC)** · **NTF: ผล** (FN-09/19) |
| 7 | เลือก/ยืนยันช่องทางจ่าย → ส่งจ่าย (hook) | view › รายละเอียด (pay) | เจ้าหน้าที่/ผู้เบิก | — | — | payDownstream hook display-only + หักลบทดรอง F103 (FN-10/18) |
| 8 | สถานะ "จ่ายแล้ว" อ่านจากปลายทาง | view › รายละเอียด (payHook) | — | — | — | display-only จาก Payroll/Finance (FN-16) |

**SoD:** Maker (ผู้เบิก · สร้าง/ยื่น) ≠ Approver (หัวหน้า/ผจก./ผอ. · อนุมัติ DOA) — ผ่าน ✅ · เจ้าหน้าที่ HR/Finance = ติดตาม (ไม่อนุมัติ · OQ-EXP-03)

### 5.2 Alternative / Exception Paths
- **A1 หลายรายการหลายหมวด (S-02/S-12):** VAT none/add/included ต่อบรรทัด · totals ถูกต้อง (FN-03)
- **A2 เกินเพดานหมวด (S-03):** เตือน + บังคับ over_reason ก่อนส่ง (ไม่ hard block · LOCK-08) (FN-04)
- **A3 ไม่มีรายการ/ยอด=0 (S-04):** ปุ่มส่งถูก disable + submitTitle เตือน (FN-05)
- **A4 ตีกลับ (S-06):** ผู้อนุมัติระบุเหตุผล → rejected → ผู้เบิกแก้แล้วยื่นใหม่ (FN-13)
- **A5 ยกเลิกก่อนอนุมัติ (S-07):** confirm → cancelled (soft archive · เฉพาะฉบับร่าง) (FN-14)
- **A6 แก้ยอดข้ามช่วง DOA (S-11):** re-resolve สายอนุมัติอัตโนมัติ (BR-05) (FN-11)
- **A7 หักลบเงินทดรอง (FN-18):** ผู้เบิกมีทดรองค้าง (F103) → ยอดจ่ายสุทธิ = ยอดใบเบิก − หักลบ (display-only) — ทดรองคงค้างที่เหลือ (advanceClear)
- **A8 PDF + ลายเซ็น (S-15):** tab PDF Preview (a4) + tab ลายเซ็น (DOA timeline) (FN-15)

> ทุก step map กับ route/overlay จริงบนจอ — ไม่มี step ลอย

---

## Section 6 · Data Entity & Fields

### 6.1 Entities
- **ExpenseClaim** (ใบเบิก · header)
- **ExpenseLine** (รายการค่าใช้จ่าย · 1 Claim : N Line · grid B2 v2)
- **ApprovalChain** (สาย DOA · embedded ใน Claim เมื่อยื่น · steps ตามช่วงวงเงิน)
- Reference (อ่านอย่างเดียว/hook): Employee (ผู้เบิก) · Movement (ตำแหน่ง/cc snapshot) · HR Config (หมวด/เพดาน #107) · DOA กลาง (F-DLG-001) · F103 (เงินทดรองค้าง) · F117 (งบ) · F102 (สิทธิ์สวัสดิการ) · Payroll/Finance/F091/F109 (ปลายทางจ่าย)

### 6.2 ExpenseClaim (Header) — fields

| # | Field | Label UI | Type | จำเป็น | ที่มา / หมายเหตุ |
|:--:|---|---|---|:--:|---|
| 1 | doc_no | เลขที่เอกสาร | AUTO | auto (ตอนอนุมัติ) | EXP-YYYY-NNNN · ENG-DOC-NUM (doccfg · LOCK-02) |
| 2 | emp | ผู้เบิก | LOOKUP (snapshot) | ✅ | Employee Master (combobox #102) |
| 3 | position / dept / cost_center | ตำแหน่ง·แผนก·ศูนย์ต้นทุน | SNAPSHOT | ✅ | Movement resolve(as_of=วันเบิก) · null≠ไม่มี (BR-08 · LOCK-06) |
| 4 | date | วันที่เอกสาร | DATE (พ.ศ.) | ✅ | — |
| 5 | pay | ช่องทางจ่าย | ENUM | ✅ | payroll / transfer / **pv** / **petty** — hook display-only [A-EXP-01 · FN-18] |
| 6 | status | สถานะ | ENUM | auto | state machine §8 |
| 7 | grand (computed) | ยอดรวมสุทธิ | MONEY | auto | totals() · single source |
| 8 | advance_offset (computed) | หักลบเงินทดรอง | MONEY | auto (display-only) | soft-ref F103 · advanceClear (FN-18) |
| 9 | payHook | สถานะการจ่าย | TEXT | auto (hook) | อ่านจากปลายทาง display-only (FN-16) |
| 10 | config_version_id | เวอร์ชัน config | SNAPSHOT | auto | HR Config resolve |
| 11 | reason (reject) | เหตุผลตีกลับ | TEXT | เมื่อ rejected | บังคับเมื่อตีกลับ (FN-13) |
| 12 | history | ประวัติ | AUDIT | auto | append-only (FN-93) |

### 6.3 ExpenseLine (grid B2 v2) — fields

| # | Field | Label UI | Type | จำเป็น | หมายเหตุ |
|:--:|---|---|---|:--:|---|
| 1 | date | วันที่ | DATE (พ.ศ.) | ✅ | ต่อรายการ |
| 2 | cat | หมวดค่าใช้จ่าย | LOOKUP | ✅ | จาก HR Config (เพดานหมวด · combobox) |
| 3 | desc | รายละเอียด | TEXT | ✅ | — |
| 4 | unit_price / qty | จำนวนเงิน | NUMBER (>0) | ✅ | BR-01 |
| 5 | vat_mode | VAT | SEGMENTED | ✅ | none / add / included · calcLineVat |
| 6 | receipt | แนบใบเสร็จ | FILE | ตามนโยบายหมวด | receiptRequired (BR-03 · FN-12) |
| 7 | over_reason | เหตุผลเกินเพดาน | TEXT | เมื่อ over-cap | บังคับเมื่อเกินเพดาน (FN-04 · LOCK-08) |
| 8 | computed: net/vat/line_total | (คำนวณ) | MONEY | auto | migrateLine/calcLineVat |

### 6.4 ApprovalChain (embedded) — fields
- `steps[]`: `{ order, role (จากตำแหน่ง), name/approver_id (slot pick), status(pending/approved/rejected), at }`
- `range_label`: ช่วงวงเงินที่ resolve (mock · จริงจาก DOA กลาง) · re-resolve เมื่อยอดข้ามช่วง (BR-05 · FN-11)

### 6.5 Entity Relationship
```
ExpenseClaim ──(1:N)──▶ ExpenseLine
ExpenseClaim ──(embeds)──▶ ApprovalChain(DOA steps)
Employee ──(referenced · snapshot)──▶ ExpenseClaim.emp
Movement ──(resolve as_of=วันเบิก · snapshot)──▶ ExpenseClaim.position/cost_center
HR Config(หมวด/เพดาน #107) ──(referenced · read-only)──▶ ExpenseLine.cat / cap
DOA กลาง(F-DLG-001) ──(resolve ตามวงเงิน)──▶ ApprovalChain.steps
F103(เงินทดรอง) ──(hook soft-ref · display-only)──▶ ExpenseClaim.advance_offset   [FN-18]
F117(งบ) / F102(สวัสดิการ) ──(hook ctl · display-only)──▶ ตรวจก่อนอนุมัติ            [§3.4 OQ-EXP-04]
Payroll/Finance/F091/F109 ◀──(hook จ่าย · display-only)── ExpenseClaim.pay/payHook
7C(FC งบ + EC มูลค่า · ไม่มี AC) ◀──(emit ตอนอนุมัติ)── ExpenseClaim               [FN-19]
```

---

## Section 7 · User Stories & Acceptance Criteria

| ID | Story (As a … I want … so that …) | AC |
|---|---|---|
| US-01 | ในฐานะผู้เบิก ฉันต้องการสร้างใบเบิกหลายรายการผ่าน wizard | AC1 wizard 5 ขั้นตามลำดับล็อก · AC2 หัวเอกสารครบ (ผู้เบิก/วันที่/ช่องทางจ่าย) · AC3 ตำแหน่ง/cc ดึง snapshot ณ วันเบิก |
| US-02 | ในฐานะผู้เบิก ฉันต้องการเพิ่มรายการค่าใช้จ่ายพร้อม VAT | AC1 เงิน>0 · หมวดจาก HR Config · AC2 VAT none/add/included คำนวณกลาง · AC3 ยอดรวม/VAT/สุทธิถูกต้อง |
| US-03 | ในฐานะผู้เบิก ฉันต้องการรู้เมื่อรายการเกินเพดานหมวด | AC1 flag เตือนเมื่อเกินเพดาน (HR Config) · AC2 บังคับกรอกเหตุผลก่อนส่ง · AC3 ยังส่งได้ (ไม่ hard block) |
| US-04 | ในฐานะผู้เบิก ฉันต้องการส่งอนุมัติตามวงเงิน | AC1 ยอดต่างช่วง = สายอนุมัติต่างกัน (resolve) · AC2 เลือกผู้อนุมัติจริงครบทุก slot จึงส่งได้ · AC3 แก้ยอดข้ามช่วง → re-resolve |
| US-05 | ในฐานะผู้อนุมัติ ฉันต้องการอนุมัติ/ตีกลับใบเบิก | AC1 เฉพาะ role approver:true · AC2 อนุมัติครบสาย → approved + เลข+PDF+7C · AC3 ตีกลับต้องระบุเหตุผล → rejected |
| US-06 | ในฐานะระบบ ฉันต้องออกเลข+PDF+7C ตอนอนุมัติ | AC1 EXP-YYYY-NNNN (ENG-DOC-NUM · ไม่ซ้ำ) · AC2 สำเนา PDF immutable · AC3 ยิง **FC/EC เท่านั้น (ไม่มี AC)** |
| US-07 | ในฐานะผู้เบิก ฉันต้องการเลือกช่องทางจ่าย | AC1 payroll/transfer/PV/petty · AC2 เป็น hook display-only ไม่จ่าย/ไม่ post · AC3 สถานะ "จ่ายแล้ว" อ่านจากปลายทาง |
| US-08 | ในฐานะผู้เบิก ฉันต้องการเห็นยอดจ่ายสุทธิหลังหักเงินทดรอง | AC1 แสดงทดรองค้าง (soft-ref F103) · AC2 ยอดจ่ายสุทธิ = ยอดใบ − หักลบ (display-only) · AC3 F101 ไม่ปรับ ledger F103 |
| US-09 | ในฐานะเจ้าหน้าที่ HR/Finance ฉันต้องการติดตามใบเบิกทั้งหมด | AC1 เห็นทุกใบ (scope:all) + เงินเต็ม (unmask) · AC2 **ไม่มีสิทธิ์อนุมัติ DOA** · AC3 ผู้เบิก/ธุรการเห็นเฉพาะใบของตน |
| US-10 | ในฐานะผู้ใช้ ฉันต้องการดูเอกสารครบทุกมุม | AC1 tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ · AC2 เอกสารแนบใน tab รายละเอียด · AC3 ตัวเงิน mask ตาม role |

---

## Section 8 · Status & Lifecycle

```
[ร่าง draft] ──ยื่น──▶ [รออนุมัติ pending_approval (DOA)]
      │                        │
      │                        ├──อนุมัติครบสาย──▶ [อนุมัติ approved (เลข+PDF+7C)] ──ส่งจ่าย(hook)──▶ [ส่งจ่าย sent_to_pay] ──▶ [จ่ายแล้ว paid (hook)] ──▶ [ปิด closed]
      │                        └──ตีกลับ──▶ [ตีกลับ rejected] ──แก้/ยื่นใหม่──▶ [ร่าง]
      └──ยกเลิก(ฉบับร่าง)──▶ [ยกเลิก cancelled (soft archive)]
```

| State | Trigger | Next | ผู้กด |
|---|---|---|---|
| draft | ยื่น (canSubmit: grand>0 + reason ครบ) | pending_approval | ผู้เบิก |
| draft | ยกเลิก | cancelled | ผู้เบิก (เฉพาะฉบับร่าง · FN-14) |
| pending_approval | อนุมัติครบสาย | approved (auto: เลข+PDF+FC/EC) | ผู้อนุมัติ DOA |
| pending_approval | ตีกลับ (+ เหตุผล) | rejected | ผู้อนุมัติ DOA |
| rejected | แก้แล้วยื่นใหม่ | draft → pending_approval | ผู้เบิก |
| approved | เลือก/ส่งช่องทางจ่าย (hook) | sent_to_pay | เจ้าหน้าที่/ผู้เบิก |
| sent_to_pay | ปลายทางจ่ายจริง (hook อ่านกลับ) | paid | ระบบ (display-only จาก Payroll/Finance) |
| paid | ปิดงาน | closed | ระบบ |

- เลข/PDF/7C ออกครั้งเดียวตอนอนุมัติครบ (immutable snapshot) · แก้ยอดหลังส่ง (ก่อนอนุมัติ) = re-resolve DOA (FN-11)

---

## Section 9 · Business Rules + Validation (with Tags)

| ID | Rule | Type | Tag | ใครเปลี่ยน + บ่อยแค่ไหน |
|---|---|---|---|---|
| R01 (BR-01) | line: จำนวนเงิน > 0 · หมวดจาก HR Config · VAT คำนวณกลาง (calcLineVat) | Prevent | **FIXED** | — (กติกาโครงสร้าง) |
| R02 (BR-02 · LOCK-05/08) | เพดานหมวด (HR Config resolve) — เกิน = **เตือน + บังคับเหตุผล** (ไม่ hard block) | Warning | **CONFIGURABLE** 🤖 | เพดาน = HR Config (#107 · Admin เปลี่ยนเป็นระยะ) |
| R03 (BR-03) | ≥1 รายการ + ยอด>0 + แนบใบเสร็จตามนโยบายหมวด ก่อนส่ง | Prevent | FIXED | — |
| R04 (BR-04 · LOCK-01) | ส่งอนุมัติ = DOA resolve **ตามยอดรวม (threshold)** · ช่วงวงเงิน FREE · ไม่ hardcode สาย | Prevent | **CONFIGURABLE** 🤖 | DOA กลาง F-DLG-001 (ผู้บริหาร · เป็นระยะ) |
| R05 (BR-05) | แก้ยอดหลังส่ง → re-resolve DOA ถ้าข้ามช่วงวงเงิน | Trigger | FIXED | — |
| R06 (BR-06 · LOCK-02) | เลข EXP-YYYY-NNNN + สำเนา = ENG-DOC-NUM/STORE · ออกตอนอนุมัติ (ไม่ซ้ำ · pad 4) | Trigger | **CONFIGURABLE** 🤖 | รูปแบบเลข = DOCCFG (Document Config) |
| R07 (BR-07 · LOCK-04) | อนุมัติ → **FC (commit งบ) + EC (มูลค่า) เท่านั้น — ไม่มี AC** | Trigger | FIXED (มติล็อก) | ผู้บริหาร (มติ · OQ-EXP-02) |
| R08 (BR-08 · LOCK-06) | ตำแหน่ง/ศูนย์ต้นทุน = snapshot Movement ณ วันเบิก (soft ref · null≠ไม่มี) | Trigger | FIXED | — |
| R09 (BR-09 · LOCK-03) | จ่ายจริง/post = **hook display-only** (Payroll/โอน/PV/petty/Accounting) — F101 ไม่ทำเอง | Trigger | FIXED | — |
| R10 (BR-10 · LOCK-07) | audit append-only · เงิน RESTRICTED masking · ไม่มี hard delete | Prevent | FIXED | — |
| R11 (FN-18 · LOCK-09) | หักลบเงินทดรอง = soft-ref F103 · ยอดจ่ายสุทธิ = ยอด − หักลบ (**display-only** · F101 ไม่ปรับ ledger) | Calc | FIXED | — (touchpoint · OQ-EXP-01) |
| R12 (FN-20 · LOCK-10) | visibility scope: self (ผู้เบิก/ธุรการ) / all (ผู้อนุมัติ, เจ้าหน้าที่ HR/Finance) · เจ้าหน้าที่ = ไม่อนุมัติ | Prevent | FIXED | SEC (RBAC · OQ-04) |
| R13 | อนุมัติ/ตีกลับได้เฉพาะ role approver:true (canApprove) | Prevent | FIXED | SEC (RBAC · OQ-04) |
| R14 | กัน double-submit (state._busy) + wizard ล็อกลำดับ (STEP_KEYS) | Prevent | FIXED | — |
| R15 (§3.4 OQ-EXP-04) | ตรวจงบ F117 + เพดานสิทธิ์สวัสดิการ F102 = **hook display-only** (mock · อ่านตอน dev) | Warning | **DYNAMIC** 🤖 | F117/F102 (ยังไม่ dev · ctl edge) |

### 9.5 สรุประดับความยืดหยุ่น

| Rule | ระดับ Flexibility | เหตุผล | ที่มา |
|---|---|---|---|
| R04 (สาย DOA ตามวงเงิน) | Rule Management (DOA กลาง F-DLG-001) | ช่วงวงเงิน/สายเปลี่ยนตามองค์กร · FREE ranges | 🤖 AI-inferred → **OQ-01** (CL-0013 แขวน · role-id เคาะ) |
| R02 (เพดานหมวด) | Admin Panel (HR Config #107) | เพดานหมวดเปลี่ยนตามนโยบาย | 🤖 AI-inferred → **OQ-02** (group ยังไม่มี · A-EXP-04 mock) |
| R06 (รูปแบบเลข EXP) | Admin Panel (Document Config) | เลขรัน/รูปแบบตั้งที่ doccfg | 🤖 AI-inferred → declaration doccfg (หลัง step 7) |
| R15 (งบ F117 / สวัสดิการ F102) | Engine/Integration (Budget/Welfare) | อ่านจากปลายทางเมื่อพร้อม · display-only | 🤖 AI-inferred → **OQ-03/OQ-EXP-04** (F117 W7 ยังไม่ dev) |
| R01, R03, R05, R07–R14 | FIXED (โครงสร้าง/มติล็อก) | flow + มติ (LOCK-01..10) | ✅ LOCK / STANDARD_BASELINE |

> Escalation: R04/R15 (🤖 DYNAMIC/Rule-Engine) → ยกเข้า §15 Open Questions ให้ยืนยันก่อนพัฒนา (C23)

---

## Section 10 · Edge Cases

### 10.1 Edge Cases ที่ PREBRIEF/BA ระบุ (☑ ยืนยันแล้ว)
- ☑ รายการเกินเพดานหมวด → เตือน + บังคับเหตุผล (ไม่ hard block · S-03 · LOCK-08)
- ☑ ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ (S-04)
- ☑ ยอดต่างช่วงวงเงิน → สาย DOA ต่างกัน (S-08)
- ☑ แก้ยอดข้ามช่วง → re-resolve DOA (S-11)
- ☑ ตำแหน่ง/cost_center = null (ไม่มี assignment) → null≠ไม่มี (S-05 · BR-08)
- ☑ แนบใบเสร็จไม่ครบตามนโยบายหมวด → เตือนก่อนส่ง (S-13)
- ☑ ตีกลับ → แก้ยื่นใหม่ (S-06) · ยกเลิกเฉพาะฉบับร่าง (S-07)
- ☑ **[FN-18]** ผู้เบิกมีทดรองค้าง (F103) → ยอดจ่ายสุทธิหักลบ display-only · ทดรองคงค้างที่เหลือแสดง

### 10.2 Edge Cases จาก AI Pattern Matching (☐ = แนะนำ · BA/dev ยืนยันที่ SOW3.7)
- ☐ [CA] ผู้อนุมัติ 2 คนกดขั้นเดียวกันพร้อมกัน → กันสถานะซ้อน (concurrent)
- ☐ [DI] ผู้เบิก/หมวด/ผู้อนุมัติถูกปิดใช้งานใน master ระหว่างค้างในสาย → นโยบายจัดการ
- ☐ [ST] แก้/ยกเลิกหลังออกเลข EXP + ยิง FC/EC แล้ว → นโยบาย reverse EC/release FC commit (⚠️ กระทบเงิน → **OQ-05**)
- ☐ [CL] หักลบทดรอง (FN-18) เมื่อทดรอง > ยอดใบเบิก → ยอดจ่ายสุทธิ=0 + ทดรองคงค้าง (fallback มีแล้ว · advanceClear Math.max)
- ☐ [PM] เจ้าหน้าที่ HR/Finance เห็นทุกใบ unmask — ตรวจว่า export/PDF ก็เคารพ scope/mask ตาม role (FN-94 · OQ-EXP-03)
- ☐ [EN] F117 Budget (W7) / F103 Advance พร้อมภายหลัง → migrate hook display-only เป็นตัวเลข/ledger จริง

---

## Section 11 · Impact / Regression
New Feature — ไม่มี regression กับของเดิม แต่มี integration points (ดู §12.1):
- HR Config (F164 · #107): เพิ่มการ "อ่าน" หมวด/เพดาน — ไม่ CRUD
- Movement: เพิ่มการ resolve ตำแหน่ง/cc (snapshot) — ไม่แก้ข้อมูล Movement
- DOA กลาง (F-DLG-001): เพิ่ม entry ตามวงเงิน (มีวงเงิน) — feature ประกาศเท่านั้น
- Payroll/Finance/F091/F109/F103/F117/F102: hook display-only — ต้องไม่ auto-จ่าย/auto-post/auto-ปรับ ledger

---

## Section 12 · System Context

### 12.1 Value Stream & Downstream Impact ⭐

**Value Stream:** Human Capital (H2R) → เบิกจ่ายพนักงาน · ตัดขวาง วงจรงบประมาณ (ตั้งงบ→ควบคุม→เทียบจริง)
**Upstream:** Employee (ผู้เบิก) · Movement (ตำแหน่ง/cc snapshot) · HR Config (หมวด/เพดาน #107) · ESS (F059 · flow "พนักงานยื่นเบิกเอง") · F103 (เงินทดรองค้าง · flow "เคลียร์เงินทดรองด้วยใบเบิกจริง") · F102 (สิทธิ์สวัสดิการกำกับวงเงิน · ctl)

**Downstream Impact Map:**

| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าเปลี่ยน/ยกเลิกกลางทาง |
|---|---|---|---|
| DOA กลาง (F-DLG-001) | คำขออนุมัติ + ยอด (มีวงเงิน) | ยื่นอนุมัติ | สาย/ช่วงวงเงินเปลี่ยนที่ DOA กลาง · CL-0013 แขวน (OQ-01) |
| 7C / โครงสร้างต้นทุน | **FC (commit งบ) + EC (มูลค่า) — ไม่มี AC** | อนุมัติครบสาย | reverse EC/release FC เมื่อยกเลิกหลังอนุมัติ (OQ-05) · **Accounting เป็นตัว post บัญชี ไม่ใช่ F101** (OQ-EXP-02) |
| Payroll (HK-1) / Finance / โอนตรง | สั่งจ่าย (hook display-only) | ส่งจ่าย (เลือกช่องทาง) | ปลายทางจ่ายจริง · F101 อ่านสถานะกลับ (paid) |
| **ใบสำคัญจ่าย PV / เงินสดย่อย F091** [FN-18] | ช่องทางจ่าย (hook display-only) | เลือก pay=pv/petty | touchpoint · F091 เป็นระบบเงินสดย่อยเต็มรูป (OQ-EXP-01) |
| **F103 เงินทดรอง** [FN-18] | ค่าหักลบ (offset) — display-only | หน้ารายละเอียด/จ่าย | **F101 ไม่ปรับ ledger F103** ส่งค่าหักลบให้ F103 (OQ-EXP-01) |
| F109 (Payment) | อนุมัติเบิก → จ่ายคืนพนักงาน (flow) | approved | ปลายทางจ่ายจริง (นอก scope จ่าย) |
| F117 Budget Control | ยอดใบเบิกตรวจงบก่อนอนุมัติ (ctl · display-only mock) | ก่อนอนุมัติ | F117 W7 ยังไม่ dev → hook display-only (OQ-EXP-04) |
| ENG-NOTIFY | event: ยื่น / ผล-ตีกลับ / จ่ายแล้ว / เกินเพดาน (ไม่นับ doa_*) | state transition | ไม่มี event = ผู้เบิกไม่รู้สถานะ |
| ประวัติ/audit | append-only ทุก mutation | ทุก action | ตรวจสอบย้อนหลัง (append-only · ไม่มี hard delete) |

**ผลกระทบแนวขวาง:** งบประมาณ (FC commit · F117 ctl) · บัญชี/GL = **ไม่ post โดย F101** (Accounting ปลายทาง · ไม่มี AC) · เงินทดรอง = หักลบ display-only (F103 เป็นเจ้าของ ledger) · รายงาน = DOA compliance + เกินเพดาน + ยอดหักลบ

### 12.3 Existing System Reference

| Rule/องค์ประกอบ | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| สายอนุมัติตามวงเงิน (R04) | DOA กลาง | ✅ | F-DLG-001 Policy Center (feature ประกาศ · doa-declaration · CL-0013 แขวน) |
| แจ้งเตือน (NTF) | ENG-NOTIFY | ✅ | F-NOTIFY (ntf-declaration) |
| เลขรัน EXP + สำเนา (R06) | Document Config | ✅ | ENG-DOC-NUM/STORE (doccfg-declaration) |
| หมวด/เพดาน (R02) | HR Config | ⚠️ บางส่วน | F164 #107 (อ่านอย่างเดียว · **group เพดานยังไม่มี** · A-EXP-04 mock) |
| ตำแหน่ง/cc snapshot (R08) | Movement | ✅ | F-HR-MOVE assignment/resolve |
| จ่าย (R09) | Payroll/Finance/F091/F109 | ✅ | hook display-only |
| หักลบเงินทดรอง (R11 · FN-18) | Advance | ⚠️ | F103 (soft-ref · display-only · F101 ไม่ปรับ ledger) |
| ตรวจงบ (R15) | Budget Control | ❌ | F117 (W7 **ยังไม่ dev**) → hook display-only |
| สิทธิ์สวัสดิการ (R15) | Welfare | ✅ | F102 (ctl edge · hook display-only) |
| 7C มูลค่า/งบ (R07) | CSQ | ✅ | csq-declaration (FC/EC · **ไม่มี AC**) |

---

## Section 13 · Delivery Phases

**Phase 1 — Feature Launch (ไม่ hardcode ตั้งแต่วันแรก):**
- ExpenseClaim/Line/ApprovalChain entity + state machine (8 state)
- wizard 5 ขั้น · line editor B2 v2 (VAT/totals) · over-cap warn+reason (LOCK-08)
- DOA slot picker resolve ตามวงเงิน (ไม่ hardcode สาย) · re-resolve ข้ามช่วง
- เลข EXP + PDF (ตอนอนุมัติ) · ยิง FC/EC (ไม่มี AC)
- ช่องทางจ่าย hook display-only (payroll/transfer/PV/petty) · หักลบทดรอง F103 (display-only) · สถานะ paid อ่าน hook
- visibility scope self/all + role เจ้าหน้าที่ HR/Finance (FN-20) · masking · audit append-only
- **Declarations** (รันหลัง step 7 โดยผู้ใช้สั่ง): DOA · NTF · CSQ (FC/EC) · DOCCFG · PDF DOC

**Phase 2 — เมื่อ F117 Budget (W7) / F103 Advance พร้อม:**
- ผูกตรวจงบ + หักลบทดรองจาก display-only → ledger/ตัวเลขจริง (R15/R11)

**Phase 3 — Rule Management / DOA finalize:**
- CL-0013 (สายผู้บริหาร) resolve + ช่วงวงเงินจริง (OQ-01) · เพดานหมวด group ใน HR Config (OQ-02) · RBAC finalize (OQ-04)

---

## Section 14 · Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation ที่ต้องเตรียม
- DOA entry (มีวงเงิน · threshold ranges) — สายจริงจาก F-DLG-001 (ห้าม hardcode สาย/ช่วงในโค้ด · DOA_RANGES = mock)
- Document type `EXP-YYYY-NNNN` — เลขจาก ENG-DOC-NUM.next() · สำเนาผ่าน ENG-DOC-STORE (doccfg · ห้ามรันเลขเอง)
- 7C (CSQ) — โครงสร้างรับ **FC (งบ) + EC (มูลค่า) เท่านั้น (ไม่มี AC)**
- HR Config resolve หมวด/เพดาน (#107 · effective_date) — read-only (group ยังไม่มี → mock resolve · A-EXP-04)

### 14.2 ข้อกำหนดจาก Tag
- R04 (CONFIGURABLE): สาย DOA + ช่วงวงเงินอ่านจาก DOA กลาง — FREE ranges ไม่ผูกโค้ด
- R02 (CONFIGURABLE): เพดานหมวดอ่านจาก HR Config — render mock + note "resolve จาก HR Config" ห้ามฝังตัวเลข
- R06 (CONFIGURABLE): เลข EXP รูปแบบจาก DOCCFG — ตัวนับ global เดินหน้าอย่างเดียว (ไม่อิง count สถานะ)
- R15 (DYNAMIC): งบ F117 / สวัสดิการ F102 — render display-only "อ่านจาก F117/F102 ตอน dev" ห้ามใส่ตัวเลขคงที่จริง

### 14.3 ข้อกำหนดจาก Edge Cases / Validation (ต้อง handle เป็นพิเศษ)
- over-cap: warn + บังคับ over_reason ทั้ง UI + submit (defense-in-depth · ไม่ hard block)
- re-resolve DOA เมื่อยอดข้ามช่วง (BR-05) — ต้องทำก่อนอนุมัติ
- เลข/PDF/7C ออกครั้งเดียวตอนอนุมัติครบ (immutable · กันซ้ำด้วยตัวนับ global)
- **FN-18 หักลบทดรอง:** display-only เท่านั้น — ห้ามเขียน/ปรับ ledger F103 (ส่งค่าหักลบให้ F103)
- **FN-19:** ยิง 7C = FC/EC เท่านั้น — **ห้ามยิง AC** (Accounting ปลายทาง post เอง)
- **FN-20:** scope guard ทั้ง list + PDF/export — เจ้าหน้าที่ HR/Finance unmask แต่กดอนุมัติไม่ได้ (approver:false)

### 14.4 WARNING ที่รอข้อสรุป
- ดู §15 Open Questions (OQ-01..05 + OQ-EXP-04 + OQ-04 RBAC)

### 14.6 Screen Inventory + UI Signals (หยาบ — ส่งต่อ FRD)

**Iron Rule #104:** 1 feature = 1 เมนู "เบิกค่าใช้จ่าย" · Pattern Q Transaction Document (list + wizard 5 steps + view tabs)

| # | ชื่อหน้า/overlay | route/trigger จริง | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) |
|---|---|---|---|---|---|
| P-01 | รายการใบเบิก | list view (default) | หน้ารายการ | ทุก role (scope self/all) | ค้นหา/filter สถานะ + docPill + signprog + empty + สร้างใบเบิก + เอกสารแนบใน landing |
| P-02 | สร้างใบเบิก (wizard 5 ขั้น) | `openCreate()` wizard | ฟอร์มสร้าง (หลายขั้น) | ผู้เบิก | แหล่งที่มา › ข้อมูลหลัก › รายการค่าใช้จ่าย › เอกสารแนบ › ตรวจสอบยืนยัน |
| P-03 | รายละเอียดใบเบิก | view drawer (tabs) | หน้ารายละเอียด | ทุก role | tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + เอกสารแนบ + hook จ่าย/หักลบทดรอง/งบ |
| P-04 | ส่งอนุมัติ (DOA slot picker) | modal (slot picker) | หน้ายืนยัน | ผู้เบิก | เลือกผู้อนุมัติจริงตามตำแหน่งแต่ละขั้น (ตามวงเงิน) |
| P-05 | ตีกลับ (เหตุผลบังคับ) | modal (reason) | หน้ายืนยัน | ผู้อนุมัติ | ระบุเหตุผลตีกลับ |
| P-06 | ยกเลิก (confirm) | modal (confirm) | หน้ายืนยัน | ผู้เบิก | ยกเลิกฉบับร่าง (soft archive) |
| P-07 | PDF Preview (a4) | view tab `pdf` | หน้ารายละเอียด (พิมพ์) | ทุก role | ใบเบิก a4 + ลายเซ็นอนุมัติ |

**สรุป:** ~1 หน้าหลัก (list) + wizard 5 ขั้น + view drawer 4 tabs + 3 modal = 1 เมนูเดียว

**UI Signals ส่งต่อ FRD:**
- Archetype = **Q-document** — มีเลขรัน + PDF + ลายเซ็น + DOA + line editor B2 v2
- print/PDF: ✅ (a4 ใบเบิก · thai-doc-pdf-generator · dec chip pdfdoc)
- NON-STANDARD: — (ตาม html-generator-v9 Pattern Q มาตรฐาน)
- **demo-strip role switcher (#105):** admin/mgr/officer — scaffolding ทดสอบ scope/mask/approver (RBAC จริงจาก login)

---

## Section 15 · Open Questions

| ID | คำถาม | สถานะ | หมายเหตุ |
|---|---|:--:|---|
| OQ-01 (A-EXP-03) | สาย DOA — ช่วงวงเงินจริง + role-id + **CL-0013 (สายผู้บริหาร) แขวน 31 ส.ค.** | ⚠️ รอ SEC/BA เคาะ | ช่วง [DEFAULT] <5k หัวหน้า · 5k–50k ผจก. · >50k ผอ. — ห้าม skill เดารหัสสาย |
| OQ-02 (A-EXP-04) | เพดานหมวด — ยังไม่มี group ใน HR Config → mock · โครงอ้าง resolve | ⚠️ รอ HR Config group | R02 CONFIGURABLE 🤖 |
| OQ-03 (A-EXP-02) | จ่ายจริง/GL = hook display-only — ยืนยัน contract ปลายทาง (Payroll/Finance/Accounting) | ⚠️ รอ FRD Phase B | [ASSUMED] hook only |
| OQ-05 | ยกเลิก/แก้หลังออกเลข+ยิง FC/EC → นโยบาย reverse EC / release FC commit | ⚠️ รอ BA/Finance | กระทบเงิน — ยกทันที (§10.2) |
| OQ-EXP-01 (FN-18) | cross-feature touchpoint (PV/petty F091 · หักลบทดรอง F103) = display-only — **ยืนยัน F101 ไม่ออก/ปรับ ledger ปลายทาง** | ✅ เคาะแล้ว (PM/BA 2026-09-10) | formalize เป็น FN-18 · touchpoint ไม่ใช่ระบบเต็ม |
| OQ-EXP-02 (FN-19) | 7C = FC/EC เท่านั้น (ไม่มี AC) | ✅ เคาะแล้ว (PM/BA 2026-09-10) | formalize เป็น FN-19 · Accounting ปลายทาง post |
| OQ-EXP-03 (FN-20) | visibility scope self/all + role เจ้าหน้าที่ HR/Finance (unmask · ไม่อนุมัติ) | ✅ เคาะแล้ว (PM/BA 2026-09-10) | formalize เป็น FN-20 |
| OQ-EXP-04 | hook เสริมใน HTML: **F117 Budget** (edge F101→F117 ctl) + **F102 Welfare** (edge F102→F101 ctl) — ยืนยันตั้งใจคงไว้ (display-only) หรือถอด | ⚠️ รอ BA ยืนยัน | มาจาก Central Plan edges · scope note §3.4 |
| OQ-04 | RBAC mapping role→login + สิทธิ์ "ธุรการสร้างแทนผู้เบิก" | ⚠️ รอ SEC/BA เคาะ | §4 |
| OQ-UX | ศัพท์ระบบบนจอ (hook / 7C / FC/EC / soft-ref) | ⚠️ รอ BA | UX judgment |

---

## Section 16 · Security & Compliance

### 16.1 Security Preset
**P6 (HR / PII Sensitive · 15 controls)** — feature จัดการข้อมูลบุคคล (ผู้เบิก/ผู้อนุมัติ) + ตัวเงิน (ยอดเบิก/เพดาน/ทดรอง) + สายอนุมัติตามวงเงิน

### 16.2 Applicable Standards (ย่อ)
- PDPA (ข้อมูลพนักงาน) ✅ · SoD/COSO (Maker≠Approver · เจ้าหน้าที่ไม่อนุมัติ) ✅ · Audit trail (append-only · ไม่มี hard delete) ✅ · Access control (RBAC + scope self/all) ✅ · Segregation of money visibility (RESTRICTED masking) ✅

### 16.3 Control Checklist (สำคัญ)
| Control | Required | Implementation |
|---|:--:|---|
| RBAC ตาม role (admin/mgr/officer) + scope self/all | ✓Must | canApprove/visibleDocs/mask (FN-20/94) |
| Data masking ตัวเงิน (RESTRICTED) | ✓Must | maskM() mask ใบคนอื่นสำหรับ mask:true role (FN-94) |
| Audit append-only ทุก mutation | ✓Must | EXP.audit tab ประวัติ · ไม่มี hard delete (FN-93) |
| SoD DOA (Maker≠Approver) + เจ้าหน้าที่ไม่อนุมัติ | ✓Must | ผู้เบิกยื่น · ผู้อนุมัติ approve · officer approver:false (FN-20) |
| Snapshot ตำแหน่ง/cc + ผู้เบิก (กันข้อมูลเปลี่ยนย้อนหลัง) | ✓Must | Movement resolve as_of=วันเบิก (BR-08) |
| กัน double-submit + slot ครบก่อนส่ง | ○Should | state._busy + submitReady (FN-92) |
| เลข/PDF immutable ตอนอนุมัติ | ✓Must | ตัวนับ global + snapshot PDF (BR-06) |

### 16.4 Risk Statement
- Risk-1: ตัวเงิน (ยอด/เพดาน/ทดรอง) รั่วถึง role ที่ไม่ควรเห็น → mitigated by masking + scope (FN-20/94)
- Risk-2: อนุมัติข้ามอำนาจ/ข้ามวงเงิน → mitigated by DOA resolve ตามยอด + canApprove guard (R04/R13)
- Risk-3: F101 เผลอ post บัญชี/จ่าย/ปรับ ledger ทดรอง โดยไม่ตั้งใจ → mitigated by hook display-only (LOCK-03/09) + 7C = FC/EC ไม่มี AC (LOCK-04)

---

## Section 17 · Health Check

### 17.1 SLA
- ยื่น → อนุมัติครบสาย ≤ 3 วันทำการ (owner: ผู้อนุมัติ DOA)
- อนุมัติ → ส่งจ่าย (hook) ≤ 2 วันทำการ (owner: เจ้าหน้าที่ HR/Finance)

### 17.2 Control Points
- ทุกการยื่น/อนุมัติ/ตีกลับ/ยกเลิก/ออกเลข/ส่งจ่าย ผ่าน audit append-only (map จาก §16.3)

### 17.3 KPI (คู่กับ §2.3)
- DOA compliance = 100% ของใบที่อนุมัติผ่านสายตามวงเงิน
- เวลาอนุมัติเฉลี่ย ≤ 3 วันทำการ
- ใบเบิกเกินเพดานที่มีเหตุผลครบ = 100% (ควบคุมงบ)
- ยอดหักลบเงินทดรองสำเร็จ (ติดตามแนวโน้ม · display-only จน F103 พร้อม)

### 17.4 Threshold
- ยอดใบ > งบคงเหลือ (F117 mock) → เตือน (display-only · OQ-EXP-04)
- รายการ > เพดานหมวด → เตือน + บังคับเหตุผล (Max soft · ไม่ block)
- ทดรองค้าง ≥ ยอดใบ → ยอดจ่ายสุทธิ = 0 (กันติดลบ · advanceClear)

### 17.5 Throughput
- รายการต่อใบ = ไม่จำกัด (line editor B2 v2) · ต่อยอดด้วยการสร้างใบเพิ่ม

---

## Section 18 · Monitoring

### 18.1 Reports Overview
- **Performance report:** DOA compliance + เวลาอนุมัติเฉลี่ย
- **Cost/Budget report:** ยอดเบิกรวม vs งบ (F117 hook) · ต่อหมวด/ศูนย์ต้นทุน
- **Transaction report:** รายการใบเบิก (filter สถานะ/ผู้เบิก · scope-aware) + Export (mask ตาม role)
- **Anomaly:** ใบเกินเพดานที่ไม่มีเหตุผล · ทดรองค้างสูงผิดปกติ · ยอดเกินงบ

### 18.2 Dashboard Widgets (หน้า Report)
- stat cards: ใบเบิกทั้งหมด / รออนุมัติ / อนุมัติ / จ่ายแล้ว / ยอดรวม (mask ตาม role)
- funnel สถานะใบเบิก (draft→pending→approved→paid)
- การ์ดยอดเกินเพดาน + ยอดหักลบทดรอง (display-only)
- ขอบเขตที่ไม่รองรับ (unsupported 7 · แสดงเตือน)

---

## Cross-Section Coverage Check
- ✅ ทุก Business Condition (§9) มี Edge Case cover (§10)
- ✅ ทุก Control runtime (§16) มี Control Point (§17.2)
- ✅ ทุก KPI/Threshold (§17) มี Widget/Report (§18)
- ✅ FN 25/25 map เข้า §5/§7/§9 (FN-01..17 + FN-90..94 + **FN-18/19/20 ใหม่**) · S-01..15 cover ครบ

---

## Section 14.7 · AI Review Report (Quality Gate)

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full
BRD: BRD-F-HR-EXPENSE — Expense Claim / เบิกค่าใช้จ่าย
ประเภท: New Feature · วันที่: 2026-09-10
───────────────────────────────────────
✅ C01 Business Objective วัดผลได้ (§2.3 มีตัวเลข/แหล่งวัด)
✅ C02 User Roles ครบ (§4 · 3 role รวม officer ใหม่)
✅ C05 Story ไม่มีคำว่า "และ" ที่ทำให้ควรแยก
✅ C10 ทุก rule มีตัวเลข/เงื่อนไขติด Tag (§9 · R01-R15)
✅ C13 Edge Cases ครบหมวด (§10.1/10.2)
✅ C18 WARNING ทุกข้อมีแผน (§15 OQ)
✅ C19 Section 14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ (LOCK-01..10) · SCOPE DRIFT = none (hook เสริม flag เป็น OQ-EXP-04)
✅ C21 Value Stream §12.1 ทุกแถวตอบ "แล้วไงต่อ"
✅ C22 ตัวชี้วัด §2.3 มี baseline/target/วิธีวัด + คู่ใน §17.3
✅ C23 §9.5 marker 🤖/✅ ครบ — R04/R15 (🤖) ลง OQ แล้ว
✅ PE01 COSO Roles ครบทุก step (§5.1)
✅ PE02 SoD ผ่าน (ผู้เบิก Maker ≠ ผู้อนุมัติ Approver · officer ไม่อนุมัติ)
✅ PE03 Security Preset P6 + controls (§16)
✅ PE04 SLA/KPI/Threshold ครบ (§17)
✅ PE05 Cross-section coverage ผ่าน
───────────────────────────────────────
ผ่าน: 16/16 · สถานะ: ✅ APPROVED
Note: 3 PM/BA additions (OQ-EXP-01/02/03) formalized เป็น FN-18/19/20 ✅
      Open Questions (OQ-01/02/03/05 + OQ-EXP-04 + OQ-04) เป็น decision ของ BA/SEC/Finance
      ไม่บล็อกเอกสาร — dev ห้ามเริ่มส่วนที่ผูก OQ-01/05 (DOA/reverse) จนกว่า resolve
═══════════════════════════════════════
```

**Declaration รอบนี้ (บันทึกไว้ · รันหลัง step 7 โดยผู้ใช้สั่งเท่านั้น · Central Plan dec chip):** DOA ✓ · NTF ✓ · CSQ (FC/EC · **ไม่มี AC**) ✓ · DOCCFG ✓ · PDF DOC ✓ — **BA/ผู้ใช้เป็นผู้สั่ง AI ไม่เรียกเอง (C3.10)**

---
*BRD นี้สร้างจาก HTML source of truth (`expense.html`) + PREBRIEF + FUNCTION_CHECKLIST (22 FN) + Central Plan row F101 + PM/BA additions 2026-09-10 (FN-18/19/20) · Conflict Priority: LOCK > PREBRIEF > HTML · ถัดไป: frd-generator-v6*
