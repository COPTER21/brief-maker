# 07_LOCKED_DECISIONS — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Audience:** All roles
> **Purpose:** บันทึกมติที่เคาะแล้ว — ห้ามเปิดอภิปรายซ้ำ
> **Scope:** FULL variant

---

## §7.0 Scope Lock (Imported จาก BRD §3.4) ⭐ — IMMUTABLE

> ข้อยืนยันที่ล็อกแล้ว — ห้าม override ตลอด pack และ chain ปลายน้ำ (HTML/Test/Dev) · spec ใดขัด LOCK → LOCK ชนะ
> **Scope Lock Ref:** N/A — **standalone** (เข้า lane ผ่าน Central Plan CUBE-LANE-W3-LITE + CHECKLIST W3Q + BA re-gate 2026-09-15 — ไม่ใช่ chain ใบเซ็นลูกค้า)

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | arch = Q-document — Pattern Q เต็ม 4 surface (list + wizard 5 steps + view drawer 4 tabs + เอกสารแนบ landing) + B2 v2 line editor | CONTEXT_PACK §2.1 · FEATURE_LIST F082 | ✅ 01_UI §1.0/§1.1 |
| LOCK-02 | เหตุผลบังคับทุกบรรทัด + DOA ตามมูลค่า · cycle count = backlog | OQ-STK-01 · CHECKLIST W3Q | ✅ 05 BR-06/08/09/24 |
| LOCK-03 | เพิ่ม/ลดเท่านั้น — เปลี่ยน location ไม่อยู่ feature นี้ · movement single-bin (ไม่มี from→to) | CHECKLIST W3Q | ✅ 04 T_inventory_movement · 05 BR-05 |
| LOCK-04 | DOA slot picker คนจริง (avatar+ตำแหน่ง+ชื่อ) — **ห้าม role ID** | locked 2026-08-17 · GOLDEN §3 | ✅ 05 BR-10 · 01 P-04 |
| LOCK-05 | เลขรัน `ADJ-YYYY-NNNN` ประกาศผ่าน doccfg — ห้าม hardcode/format เอง · ออกตอนส่งอนุมัติ | CONTEXT_PACK §2.3 | ✅ 05 BR-21 · 02 API-05 |
| LOCK-06 | movement append-only — ยกเลิกหลัง post = reversal เท่านั้น | CONTEXT_PACK §2.8 · GOLDEN §4 | ✅ 05 BR-16/17 · 04 append-only |
| LOCK-07 | location model จาก Putaway §3.0 — ห้ามนิยามใหม่ · `in-transit` ห้ามแตะ | BUILD_ORDER PUTAWAY→STKADJ | ✅ 04 §4.9 · 05 BR-13 · read-only |
| LOCK-08 | JE = mock + `FWD-WIRE: JE posting` (W5) — ห้าม post จริง | CONTEXT_PACK §2.6 | ✅ 05 BR-19 |
| LOCK-09 | soft-reference LD-4C-02 — master = picker ไม่ FK validate nullable | GOLDEN §4 | ✅ 05 BR-22 · 04 soft-ref |
| LOCK-10 | CI CUBE Warm Light · ปี ค.ศ. ล้วน · sidebar module map | TASTE_LOG | ✅ 01 §1.0/§1.7 |

- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี (BRD §3.4 Scope Drift = none)

---

## §7.1 Locked Decisions (LD)

### LD-01: Optimistic locking (version) + serialize post ที่ (bin,item)
- **Date:** 2026-09-16 · **Context:** EC-01 concurrent approve/post + race condition inventory (PR-1/PR-9)
- **Decision:** optimistic lock ด้วย `version` column (If-Match) + serialize post ต่อ (bin,item)
- **Rationale:** contention หายาก · pessimistic lock ทำร้าย 99% · ตรงกับ BRD §14.3
- **Implications:** 04_DB `version` · 02_API If-Match approve/post/reverse · 06 TC-CC-01
- **Reversibility:** MEDIUM · **Note:** ค่า/นโยบายรอ BA ยืนยัน (OQ-08 `[AI-DEFAULT]`)

### LD-02: F082-ENG-01 (adjustment-valuation-engine) register CUBIC ตอน dev hand-off
- **Decision:** scope-local ก่อน (DRAFT) → register เมื่อ F083 Stock Transfer ยืนยัน reuse
- **Rationale:** หลีก premature abstraction · confirm reuse pattern (OB-16)
- **Implications:** 03_LOGIC §3.2 status=DRAFT

### LD-03: F082-ENG-02 (inventory-movement-engine) = shared ledger engine
- **Decision:** movement engine เป็น shared candidate ของ Warehouse lane — register ตอน F083 reuse
- **Rationale:** movement schema + reversal linking ใช้ร่วม (OB-16)
- **Implications:** 03_LOGIC §3.2 · 04_DB T_inventory_movement (shared)

### LD-04 (BR-09 · OQ-ADJ-01): ฐาน DOA = Σ ค่าสัมบูรณ์ ไม่ใช่ยอดสุทธิ
- **Date:** ยืนยัน BA re-gate · **Context:** ใบผสม +/− สุทธิ≈0 แต่เคลื่อนสินทรัพย์จริง
- **Decision:** `abs_adjustment_amount = Σ|line_amount|` เป็นฐาน DOA · frozen at submit · `net_adjustment_amount` แสดงอย่างเดียว (ห้ามใช้เป็นฐาน)
- **Rationale:** กันใบผสมหลุดอนุมัติ (gap G-02 · DOA_BRIEF BR-DOA-07)
- **Implications:** 03 ENG-01 · 05 BR-09/FN-43 · 04 abs/net fields · **load-bearing ทั้ง DOA/JE/PDF/NTF/CSQ**
- **Reversibility:** HARD (สัญญาข้ามเอกสาร)

### LD-05 (FIX-03 · BA re-gate 2026-09-15): reversal ผ่าน DOA ตามมูลค่า — ไม่ auto-post
- **Context:** BRD Risk R-09 (กลับรายการมูลค่าสูงไม่ถ่วงดุล)
- **Decision:** กลับรายการ = **สร้างใบใหม่** (`is_reversal_doc`) วิ่ง draft→pending→approved→posted ตามสาย DOA (ค่าสัมบูรณ์ของตัวเอง) · ต้นฉบับ → reversed เมื่อใบกลับรายการ post · ผูก 2 ทาง
- **Implications:** 02 API-10 · 03 FN-14 · 05 BR-17/17.1/18 · 01 P-07 journey
- **Reversibility:** HARD (BA locked)

### LD-06 (FIX-02 · BA re-gate 2026-09-15): ยกเลิกเฉพาะ ร่าง/รออนุมัติ — ไม่มี Approved→Cancelled
- **Context:** BRD Risk R-10 (ยกเลิกใบอนุมัติแล้วเลี่ยงร่องรอย post)
- **Decision:** ปุ่มยกเลิกโผล่เฉพาะ draft/pending · `approved` ยกเลิกไม่ได้ (post แล้วกลับรายการเท่านั้น) · ไม่มี transition approved→cancelled
- **Implications:** 02 API-08 guard · 03 FN-11 · 05 BR-27/VR-16 · state machine §5.2
- **Reversibility:** HARD (BA locked)

### LD-07 (FIX-04 · BA re-gate 2026-09-15): count-doc trace = display-only
- **Decision:** `adj_source` (ปรับตรง/จากใบนับ) + `ref_count_doc` (F084/F086 soft-ref) · source=count → ref บังคับ (enforced ใน wizardNext + submitForApproval) · **ไม่เปิด/สร้างหน้าใบนับ**
- **Implications:** 02 API-18 · 03 FN-06 · 04 CHECK constraint · 05 BR-26/VR-05 · 01 P-02 s1/P-03
- **Reversibility:** HARD

### LD-08 (OQ-ADJ-02): ยอดเปลี่ยนระหว่างรออนุมัติ → เตือน 2 ยอดก่อน post
- **Decision:** BR-15 recheck — snapshot vs ยอดล่าสุด ต่าง → เตือน + เลือก "คิดจากยอดล่าสุด"/"ตีกลับไปแก้" (ไม่ overwrite เงียบ)
- **Implications:** 03 FN-12 · 05 BR-15/EC-04 · 01 P-06

---

## §7.2 Convention Deviations

### CD-01: ID prefix = `F082` (fid) แทน `F-WH-STKADJ`
- **Convention default:** `F-XX-API-NN`
- **Deviation:** ใช้ `F082-API-NN`/`F082-FN-NN`/`F082-ENG-NN` (fid สั้น อ่านง่าย ตรง MEMORY/HANDOFF)
- **Approved:** BA lane convention · apply ทั้ง pack consistently

### CD-02: BR ids ยึด PREBRIEF (BR-01..BR-27) ไม่ใช่ BRD R-series
- **Reason:** คง traceability กลับ PREBRIEF/FUNCTION_CHECKLIST (source of truth) · map R01–R28 ระบุใน 05 §5.1 header
- **Approved:** WF-01 rule C3.1 (PREBRIEF = business content)

---

## §7.3 Open Questions Promoted → LD
ยังไม่มี (OQ ทั้งหมด non-blocking · รอ owner ภายนอก — ดู 00 §0.8)

## §7.4 Architecture Tradeoffs Acknowledged
- **AT-01:** PostgreSQL RLS + row scope ตามคลัง (perf ~5% vs security) — accepted (CUBE standard)
- **AT-02:** JE = mock รอบนี้ (W5 post จริง) — accepted · CSQ ไม่ประกาศ AC กันนับซ้ำ
- **AT-03:** ต้นทุน = mock Item Master (valuation engine W5) — accepted · engine รับ input ต้นทุน ไม่ตัดสินเอง

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| วงเงิน DOA จริง + จำนวนชั้น | Strike + F-DLG-001 | ตั้ง entry DOA-WH-ADJ-01 |
| เกณฑ์ NC (มูลค่าสูง/อายุค้าง) | Strike + NC rules | pre-deploy |
| valuation engine contract | W5 | Wave W5 |
| no-gap เลขรัน (ถ้าบัญชีต้องการ) | F-DOCCFG | pre-deploy |
| draft expiry policy | BA | sprint |

## §7.6 References
- Convention: `knowledge/conventions.md` · CUBIC: `references/cubic-schema-templates.md`
- Related: F081 Putaway (location §3.0) · F083 Stock Transfer (reuse ENG-01/02) · F-DLG-001/F-DOCCFG/F-NOTIFY/F-CSQ-01
- Declarations: `5_DECLARATIONS/` (DOA/NTF/CSQ/DOCCFG/print-spec)
