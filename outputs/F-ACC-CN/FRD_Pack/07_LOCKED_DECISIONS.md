# 07_LOCKED_DECISIONS — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions — ห้ามเปิดอภิปรายซ้ำ

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ — IMMUTABLE

> ข้อยืนยันจาก CONTEXT_PACK W5-LITE + GOLDEN_RULES — ห้าม override ตลอด pack + chain ปลายน้ำ (HTML/Test/Dev). spec ใดขัด → LOCK ชนะ.

| LOCK-ID | ข้อยืนยัน | อ้าง | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | Pattern Q-document + B2 v2 line editor | CONTEXT_PACK §2.2 | ✅ 01_UI §1.0/§1.2 |
| LOCK-02 | อ้าง AR Invoice (ในเลน · หลัง AR ba-done) | workflow_graph | ✅ 02_API-11 · §2.X |
| LOCK-03 | เหตุผล master config: รับคืน(SR mock)/ส่วนลดภายหลัง/ผิดราคา | §2.2 | ✅ 04_DB T_cn_reason_master · 05_RULES BR-05/15 |
| LOCK-04 | ลดไม่เกินยอดคงเหลือใบอ้างอิง (OQ-CN-01) | OQ-CN-01 | ✅ 05_RULES BR-02 |
| LOCK-05 | DOA slot picker ตามมูลค่า | §2.2 | ✅ 05_RULES BR-07 · 01_UI submit modal |
| LOCK-06 | doccfg CN-YYYY-NNNN + pdfdoc อ้างเลขใบเดิม+เหตุผล (สรรพากร) | §2.2 | ✅ 05_RULES BR-08 · 03_FN-11/15 |
| LOCK-07 | ระบุผลกระทบ VAT ขายใน pack | §2.2 | ✅ 05_RULES BR-12 · 02_API §2.X · ref tab |
| LOCK-08 | dep ข้ามเลน (Sales Return/JE) = mock [ASSUMED contract] | §2.2 | ✅ 00_OVERVIEW §0.5 · 02_API §2.X |
| LOCK-09 | UI #67.1/#104/#105/#106 = enforce | GOLDEN_RULES | ✅ 01_UI §1.6 (#67.1) · Design Authority html-generator-v9 |
| LOCK-10 | ค.ศ. · append-only | GR | ✅ 04_DB (date ค.ศ.) · 05_RULES BR-13 |

- **Scope Lock Ref:** CONTEXT_PACK W5-LITE §2.2 + §3 (OQ-CN-01) + GOLDEN_RULES 1–12
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี. End-bill discount (FN-19) = การขยายภายใต้ LOCK-04/LOCK-07 ที่ BA เคาะเพิ่ม 2026-09-22 (คุมยอดสุทธิ ≤ คงค้าง + สะท้อน VAT) — ไม่ชน exclusion.

---

## §7.1 Locked Decisions (LD)

### LD-01: approval_chain = jsonb snapshot บน header (freeze ณ ส่ง)
- **Context:** DOA field contract + HTML `confirmSubmit` freeze chain
- **Decision:** เก็บ approval_chain + approval_history เป็น jsonb บน T_credit_note (ไม่แยกตาราง step)
- **Rationale:** snapshot ณ ส่ง = immutable · history append-only · ตรง HTML/DOA brief
- **Implications:** 04_DB header jsonb · **Reversibility:** MEDIUM

### LD-02: Optimistic lock (`version`) สำหรับ concurrent approval
- **Context:** EC-CC-01 (2 คนอนุมัติขั้นเดียวพร้อมกัน — Phase 2.5 PR-1 `[AI-DEFAULT]`)
- **Decision:** version column + If-Match → 409 ERR_STALE_DATA (first wins)
- **OQ:** OQ-CC-01 (BA confirm) · **Reversibility:** MEDIUM

### LD-03: ENG cn-totals + ar-open-item register CUBIC ตอน hand-off
- **Decision:** สร้าง scope-local ก่อน (status DRAFT) · register เมื่อ AR family (Invoice/DN) ยืนยัน reuse
- **Rationale:** เลี่ยง premature abstraction · **Reversibility:** EASY

### LD-04: "ออกเอกสารแก้ไข" = display-only (ไม่ถอนยอด/ไม่ลบใบ)
- **Context:** approved/sent ยกเลิกไม่ได้ (ม.86/10 — เอกสารภาษีออกแล้ว)
- **Decision:** mark รอเอกสารทดแทน เท่านั้น (revise_marked) — เส้นทางจริง (Debit Note vs CN ใหม่) รอ **OQ-CN-02**
- **Reversibility:** EASY (เพิ่มเส้นทางเมื่อเคาะ)

### LD-05: DOA tier คิดจาก `grand` (ยอดสุทธิหลังหักส่วนลดท้ายบิล) ⭐ (OQ-b RESOLVED)
- **Date:** 2026-09-22 · **Context:** BR-07 + BR-11 — end-bill ลด grand ก่อนเข้า DOA
- **Options:** A) tier บนยอดก่อนส่วนลด · B) tier บนยอดสุทธิหลังส่วนลด
- **Decision:** **B** — `resolveDoa()` ใช้ `totals(s).grand` (ตรง HTML) · **BA-confirmed 2026-09-22**
- **Rationale:** วงเงินอนุมัติควรสะท้อนภาระจริงหลังส่วนลด · **Reversibility:** MEDIUM (กระทบ DOA matrix wire)
- **Implications:** 03_LOGIC ENG-DOA input = grand · 05_RULES BR-07/tier matrix · 06 TC-19c

### LD-06: เลข CN / VAT / DOA / NTF / CSQ / PDF store = engine กลาง (declare-only)
- **Decision:** feature ประกาศ event/doc_type/slot เท่านั้น — ห้าม hardcode เลขรัน/สายอนุมัติ/ช่องทาง/logic ประทับผล 7C
- **Rationale:** DOCCFG/DOA/NOTIFY/CSQ engine กลาง · ประกาศซ้ำ (เช่น DC จาก DOA, OC จาก OP) = register reject 422
- **Reversibility:** N/A (สถาปัตย์)

---

## §7.2 Convention Deviations
### CD-01: POST custom action endpoints (submit/approve/reject/cancel/send/revise-doc) แทน PATCH state
- **Reason:** semantic clarity — action ไม่ใช่ property update (ตรง HTML handler + DOA/COSO). Apply: API-05..09, API-14

---

## §7.3 Open Questions (ยังไม่ resolve — ดู 00_OVERVIEW §0.8)
- OQ-CN-01 (เหตุผล master ฉบับสุดท้าย + trade_discount_warn) · OQ-CN-02 (revise-doc path) · OQ-CN-03 (refund/FC) · OQ-CN-04 (tax month + DOA cut) · OQ-AR-06 (role-ids) · AR contract F094 [ASSUMED] · CSQ-OQ-CN-1 (EC DISC/PRICE) · OQ-EB-01/OQ-CC-01/OQ-FU-01 ([AI-DEFAULT] confirm)
> **RESOLVED → LD:** OQ-b → LD-05.

---

## §7.4 Architecture Tradeoffs
- **AT-01:** PostgreSQL RLS (scope company) over app-level filter — accepted (CUBE standard)
- **AT-02:** JE/VAT/RV/SR/DOA = mock/forward-wire ใน W5-LITE — accepted (LOCK-08) · re-evaluate Phase 4 wire จริง

## §7.5 Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| ปัดเศษ ebVat (2 ตำแหน่ง per HTML) ยืนยัน | BA/Finance | sprint |
| ไฟล์แนบ type/size (jpg/png/pdf ≤10MB) | Tech Lead | pre-dev |
| DOA cut 50k/300k + role-mgr-acc master | Policy Center | pre-dev (OQ-AR-06/CN-04) |

## §7.6 References
- BRD §3.4 (Scope Lock) · declaration briefs (DOA/NTF/CSQ/DOCCFG/pdfdoc) · conventions.md · HTML source of truth
