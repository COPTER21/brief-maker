# 07_LOCKED_DECISIONS — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions — ห้ามเปิดอภิปรายซ้ำ

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ — IMMUTABLE

> ข้อยืนยันจาก PREBRIEF §0 Obligations (OB-1..OB-9) + CONTEXT_PACK §2 ข้อ 4 + GOLDEN_RULES — ห้าม override ตลอด pack + chain ปลายน้ำ (HTML/Test/Dev). spec ใดขัด → LOCK ชนะ.

| LOCK-ID | ข้อยืนยัน | อ้าง | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | Pattern Q-document + B2 v2 line editor (UI #67.1/#104/#105/#106) | OB-9 | ✅ 01_UI §1.0/§1.2 |
| LOCK-02 | อ้าง AP Invoice (ในเลน · หลัง APINV ba-done) | OB-1 · workflow_graph | ✅ 02_API-11 · §2.X |
| LOCK-03 | เหตุผล master config: คืนของ RTV/ราคาเกิน/ของขาด | OB-3 | ✅ 04_DB T_dn_reason_master · 05_RULES BR-05/17 |
| LOCK-04 | ลดไม่เกินมูลค่าที่ลดได้ (dnRoom) ของใบอ้างอิง | OB-2 | ✅ 05_RULES BR-02/BR-13 |
| LOCK-05 | DOA slot picker ตามมูลค่า | OB-5 | ✅ 05_RULES BR-07 · 01_UI submit modal |
| LOCK-06 | doccfg DN-YYYY-NNNN + pdfdoc อ้างเลขใบเดิม+เหตุผล (สรรพากร) | OB-6 | ✅ 05_RULES BR-08 · 03_FN-11/15 |
| LOCK-07 | ระบุผลกระทบ VAT ซื้อใน pack (input VAT · gated vendorCn) | OB-7 | ✅ 05_RULES BR-12/BR-14 · 02_API §2.X · ref tab |
| LOCK-08 | dep ข้ามเลน (RTV/JE/PV) = mock [ASSUMED contract] | OB-4 | ✅ 00_OVERVIEW §0.5 · 02_API §2.X |
| LOCK-09 | UI #67.1/#104/#105/#106 = enforce | OB-9 · GOLDEN_RULES | ✅ 01_UI §1.6 (#67.1) · Design Authority html-generator-v9 |
| LOCK-10 | ค.ศ. · append-only | OB-9 · GR | ✅ 04_DB (date ค.ศ.) · 05_RULES BR-15 |

- **Scope Lock Ref:** PREBRIEF §0 (OB-1..OB-9) + CONTEXT_PACK W5-LITE §2 ข้อ 4 + GOLDEN_RULES
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี.
  - End-bill discount (FN-19) = การขยายภายใต้ LOCK-04/LOCK-07 ที่ BA เคาะเพิ่ม 2026-09-23 (คุมยอดสุทธิ ≤ dnRoom + สะท้อน input VAT) — ไม่ชน exclusion.
  - เครดิตคงเหลือกับผู้ขาย (FN-20/BR-13) = **ปรับความหมาย LOCK-04** ตามมติ BA FIX-01 (เพดาน = dnRoom ไม่หัก paid; ส่วนเกินคงค้าง = vendor credit) — ไม่ชน exclusion (refund ยังปิด).
  - vendorCn input-VAT gating (FN-21/BR-14) = การขยายภายใต้ LOCK-07 ตามมติ BA FIX-02.

---

## §7.1 Locked Decisions (LD)

### LD-01: approval_chain = jsonb snapshot บน header (freeze ณ ส่ง)
- **Context:** DOA field contract + HTML `confirmSubmit` freeze chain
- **Decision:** เก็บ approval_chain + approval_history เป็น jsonb บน T_debit_note (ไม่แยกตาราง step)
- **Rationale:** snapshot ณ ส่ง = immutable · history append-only · ตรง HTML/DOA brief
- **Implications:** 04_DB header jsonb · **Reversibility:** MEDIUM

### LD-02: Optimistic lock (`version`) สำหรับ concurrent approval
- **Context:** EC-CC-01 (2 คนอนุมัติขั้นเดียวพร้อมกัน — Phase 2.5 PR-1 `[AI-DEFAULT]`)
- **Decision:** version column + If-Match → 409 ERR_STALE_DATA (first wins)
- **OQ:** OQ-CC-01 (BA confirm) · **Reversibility:** MEDIUM

### LD-03: ENG dn-totals + ap-open-item register CUBIC ตอน hand-off
- **Decision:** สร้าง scope-local ก่อน (status DRAFT) · register เมื่อ AP family (Invoice/CN kernel) ยืนยัน reuse
- **Rationale:** เลี่ยง premature abstraction · **Reversibility:** EASY

### LD-04: "ออกเอกสารแก้ไข" = display-only (ไม่ถอนยอด/ไม่ลบใบ)
- **Context:** approved/sent ยกเลิกไม่ได้ (ม.86/10 — เอกสารภาษีออกแล้ว)
- **Decision:** mark รอเอกสารทดแทน เท่านั้น (revise_marked) — เส้นทางจริงรอ **OQ-DN-04**
- **Reversibility:** EASY

### LD-05: DOA tier คิดจาก `grand` (ยอดสุทธิหลังหักส่วนลดท้ายบิล) ⭐
- **Context:** BR-07 + BR-11 — end-bill ลด grand ก่อนเข้า DOA
- **Decision:** `resolveDoa()` ใช้ `totals(s).grand` (ตรง HTML `step5Extra`)
- **Rationale:** วงเงินอนุมัติควรสะท้อนภาระจริงหลังส่วนลด · **Reversibility:** MEDIUM (กระทบ DOA matrix wire)
- **Implications:** 03_LOGIC ENG-DOA input = grand · 05_RULES BR-07/tier matrix · 06 TC-19c

### LD-06: เลข DN / input VAT / DOA / NTF / CSQ / PDF store = engine กลาง (declare-only)
- **Decision:** feature ประกาศ event/doc_type/slot เท่านั้น — ห้าม hardcode เลขรัน/สายอนุมัติ/ช่องทาง/logic ประทับผล 7C
- **Rationale:** DOCCFG/DOA/NOTIFY/CSQ engine กลาง · ประกาศซ้ำ (เช่น DC จาก DOA, OC จาก OP) = register reject 422
- **Reversibility:** N/A (สถาปัตย์)

### LD-07: dnRoom = เพดานการออก DN **ไม่หัก paid** · vendor credit split ⭐ (FIX-01)
- **Date:** 2026-09-23 (BA FIX-01) · **Context:** คืนของหลังจ่ายครบ → ต้องออก DN ได้
- **Options:** A) เพดาน = outstanding (mirror CN ตรง ๆ — จ่ายครบออกไม่ได้) · B) เพดาน = dnRoom (ไม่หัก paid) + แยก vendorCredit
- **Decision:** **B** — `dnRoom = invGrand − dn_applied − dn_held` · `dnSplit`: applyToAp = min(grand, outstanding) · vendorCredit = ส่วนเกิน · **BA-confirmed 2026-09-23**
- **Rationale:** สะท้อนของจริง (คืนของหลังจ่าย = เจ้าหนี้มีเครดิตคงเหลือกับผู้ขาย ไม่ใช่ลดไม่ได้) · **Reversibility:** MEDIUM
- **Implications:** 03_LOGIC ENG ap-open-item dnRoom/dnSplit · FN-11/FN-17 · 04_DB apply_to_ap/vendor_credit + V_vendor_credit_ledger · 05_RULES BR-13 · 06 AT-20
- **หมายเหตุ semantic reversal:** FN-04/S-13/S-11 **กลับด้านจาก mirror CN** — การจ่ายเงินไม่บล็อกเพดานอีกต่อไป. vendor credit flow (ใช้/ตัดยอด) = **display-only รอบนี้ · OQ-DN-06**

### LD-08: input-VAT reversal gated by vendorCn ⭐ (FIX-02)
- **Date:** 2026-09-23 (BA FIX-02) · **Context:** ม.82/10 ฝั่งซื้อ — กลับภาษีซื้อต้องมีใบลดหนี้จากผู้ขาย
- **Decision:** input_vat_line ลง ภ.พ.30 เมื่อกรอก vendorCn+วันที่ (API-16/FN-16) · เดือนภาษี = vendorCnDate · ไม่มี = "รอเอกสาร" · ปุ่มบันทึกภายหลังบน approved/sent
- **Rationale:** กันกลับภาษีซื้อก่อนมีเอกสาร (KPI-C2 = 0) · **Reversibility:** MEDIUM
- **Implications:** 03_LOGIC FN-16 · 04_DB vendor_cn/date + input_vat_applied/month + CHECK · 05_RULES BR-14 · 06 AT-21 · 02_API-16
- **legal basis:** **[ASSUMED — mirror CN ฝั่ง AR]** → **OQ-DN-05** (BA รับรองก่อน dev ตั้งค่า)

---

## §7.2 Convention Deviations
### CD-01: POST custom action endpoints (submit/approve/reject/cancel/send/revise-doc/vendor-cn) แทน PATCH state
- **Reason:** semantic clarity — action ไม่ใช่ property update (ตรง HTML handler + DOA/COSO). Apply: API-05..09, API-14, API-16

---

## §7.3 Open Questions (ยังไม่ resolve — ดู 00_OVERVIEW §0.8)
- OQ-DN-01 (เหตุผล master ฉบับสุดท้าย + ลดลอย) · OQ-DN-03 (refund) · OQ-DN-04 (revise-doc path) · OQ-DN-05 ⭐ (legal basis ภาษีซื้อ ม.82/10 ฝั่งซื้อ [ASSUMED mirror CN]) · OQ-DN-06 ⭐ (flow เครดิตคงเหลือกับผู้ขาย) · OQ-DN-07 (CSQ profile dn.issued vs dn.vat_applied) · OQ-AP-06 (role-ids + DOA tier boundaries) · AP contract [ASSUMED] · CA-01 (vendorCn ซ้ำ/เดือนปิดงวด) · OQ-CC-01/OQ-EB-01/OQ-FU-01 ([AI-DEFAULT] confirm)
> **RESOLVED → LD:** FIX-01 → LD-07 · FIX-02 → LD-08.

---

## §7.4 Architecture Tradeoffs
- **AT-01:** PostgreSQL RLS (scope company) over app-level filter — accepted (CUBE standard)
- **AT-02:** RTV/JE/VAT/PV/DOA = mock/forward-wire ใน W5-LITE — accepted (LOCK-08) · re-evaluate Phase 4 wire จริง
- **AT-03:** vendor credit ledger = display-only (view) — accepted · flow ใช้/ตัดยอด รอ OQ-DN-06

## §7.5 Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| legal basis ภาษีซื้อ ม.82/10 ฝั่งซื้อ (BR-12/BR-14) ยืนยัน | BA/Finance | pre-dev (OQ-DN-05) |
| ปัดเศษ ebVat (2 ตำแหน่ง per HTML) ยืนยัน | BA/Finance | sprint (OQ-EB-01) |
| ไฟล์แนบ type/size (jpg/png/pdf ≤10MB) | Tech Lead | pre-dev (OQ-FU-01) |
| DOA cut 50k/300k + role ids master | Policy Center | pre-dev (OQ-AP-06) |
| flow ใช้/ตัดยอดเครดิตคงเหลือกับผู้ขาย | AP/F097 | Phase 4 (OQ-DN-06) |
| CSQ profile dn.issued vs dn.vat_applied | Strike/Finance | pre-dev (OQ-DN-07) |

## §7.6 References
- BRD §3.4 (Scope Lock) · declaration briefs (DOA/NTF/CSQ/DOCCFG/pdfdoc) · conventions.md · HTML source of truth · sibling FRD F-ACC-CN (structural template)
