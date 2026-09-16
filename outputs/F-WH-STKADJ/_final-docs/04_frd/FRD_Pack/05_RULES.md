# 05_RULES — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + State Machine + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> **Source of truth:** PREBRIEF §4 (BR-01..BR-27) · §5 (State Machine) · FUNCTION_CHECKLIST 55 FN · BA re-gate 2026-09-15 (FIX-02/03/04)

---

## §5.1 Business Rules (BR)

> **Note:** BR ids ยึดตาม PREBRIEF §4 ตรง ๆ (BR-01..BR-27) — ไม่ rename เพื่อคง traceability กลับ PREBRIEF/BRD/FUNCTION_CHECKLIST
> Constants/thresholds ทั้งหมดที่เป็น "เลข" (วงเงิน DOA, threshold%, อายุใบค้าง) **ไม่ถูก hardcode ใน feature** — อ่านจาก engine กลาง/NC rules (BR-20). ดู §5.9

### BR-01: ห้ามคู่ (bin, สินค้า) ซ้ำในใบเดียว
- **Statement:** 1 ใบ ห้ามมีคู่ **(bin, สินค้า)** ซ้ำกัน
- **Enforced by:** F082-FN-03 updateAdjustmentLines (dup check) + F082-FN-06 validateAdjustmentDocument
- **On violation:** เตือน + ชี้บรรทัดเดิม + เสนอ "รวมบรรทัด" · `ERR_DUPLICATE_BIN_ITEM`
- **Scenario:** S-01..S-03 · **FN:** FN-10

### BR-02: ทุกบรรทัดต้องมีผลต่าง ≠ 0
- **Statement:** ยอดที่ถูกต้อง ≠ ยอดระบบ (ผลต่าง ≠ 0) ทุกบรรทัด
- **Enforced by:** F082-FN-03 + F082-FN-06
- **On violation:** บล็อกตอนบันทึก/ส่ง + ชี้บรรทัด + microcopy "ไม่มีผลต่าง ให้ลบบรรทัดหรือแก้ยอด" · `ERR_ZERO_DELTA`
- **Scenario:** S-04 · **FN:** FN-11

### BR-03: ยอดหลังปรับ ≥ 0
- **Statement:** `ยอดระบบ + จำนวนที่ปรับ ≥ 0` ต่อ (bin, สินค้า) — ห้ามปรับลดจนติดลบ
- **Enforced by:** F082-FN-03 + F082-FN-06 (ใช้ snapshot ยอดคงเหลือจริง)
- **On violation:** บล็อก + แสดงยอดคงเหลือจริง · `ERR_NEGATIVE_STOCK`
- **Scenario:** S-05 · **FN:** FN-12 · `[AI-DRAFT][STD]`

### BR-04: 1 ใบ = 1 คลัง
- **Statement:** ทุกบรรทัดใน 1 ใบต้องอยู่คลังเดียวกับหัวใบ — เพื่อให้ DOA/JE ผูกคลังเดียวชัด
- **Enforced by:** F082-FN-03 (เปลี่ยนคลังหัวใบ = ล้างบรรทัด)
- **On violation:** เปลี่ยนคลังตอนมีบรรทัด → confirm ก่อนล้างบรรทัด
- **Scenario:** S-23 · **FN:** FN-09 · `[AI-DRAFT]`

### BR-05: ห้ามเปลี่ยน/ย้าย location ในใบนี้ (negative)
- **Statement:** ไม่มีช่อง "bin ปลายทาง / ย้ายไป" — การย้าย = Stock Transfer (F083)
- **Enforced by:** โครงหน้าจอ (ไม่มี field) + microcopy ชี้ไป Stock Transfer เมื่อผู้ใช้ค้น "ย้าย"
- **Scenario:** S-25 · **FN:** FN-36 (negative)

### BR-06: เหตุผลบังคับทุกบรรทัด
- **Statement:** ทุกบรรทัดต้องเลือกเหตุผล · เหตุผล "อื่น ๆ" (RS-99) ต้องมีคำอธิบายเพิ่ม
- **Enforced by:** F082-FN-06 (pre-submit) — ส่งอนุมัติไม่ได้ถ้ามีบรรทัดว่างเหตุผล
- **On violation:** ชี้บรรทัดที่ขาด · `ERR_REASON_REQUIRED`
- **Scenario:** S-01..S-03 · **FN:** FN-18, FN-40

### BR-07: เหตุผลต้องตรงทิศกับผลต่าง
- **Statement:** dropdown เหตุผลกรองตามทิศของผลต่าง (บรรทัด + ไม่เห็นเหตุผลกลุ่มลด และกลับกัน) ตาม field "ทิศที่ใช้ได้" ของ master เหตุผล (§8: +/−/ทั้งคู่)
- **Enforced by:** F082-FN-03 (กรอง dropdown) + F082-FN-06 (assert ตรงทิศ)
- **On violation:** เตือน + กรอง dropdown ให้เหลือเฉพาะที่ใช้ได้ · `ERR_REASON_DIRECTION_MISMATCH`
- **Scenario:** S-01/S-02 · **FN:** FN-37 · `[AI-DRAFT]`

### BR-08: ต้องส่งอนุมัติเสมอ — ไม่มีทางลัด post ตรงจากร่าง
- **Statement:** ปุ่ม "ผ่านรายการ" ไม่ enable จนกว่าสถานะ = `อนุมัติแล้ว`
- **Enforced by:** State machine §5.2 + F082-FN-13 postDocument precondition (status must = อนุมัติแล้ว)
- **On violation:** `ERR_INVALID_STATE_TRANSITION`
- **Scenario:** S-07 · **FN:** FN-23

### BR-09: ฐาน DOA = Σ|มูลค่าต่อบรรทัด| (ค่าสัมบูรณ์)
- **Statement:** ชั้นอนุมัติคำนวณจาก **Σ ค่าสัมบูรณ์ของมูลค่าต่อบรรทัด** ไม่ใช่ยอดสุทธิ — ใบ +1,000,000/−1,000,000 (สุทธิ ≈ 0) ยังต้องอนุมัติชั้นสูง
- **Enforced by:** F082-ENG-01 adjustment-valuation-engine (คืน `abs_total`) → ส่งเป็น base ให้ DOA กลาง (F082-API-16)
- **Scenario:** S-03 · S-11/S-12 · **FN:** FN-08, FN-14, FN-43 · gap G-02 · `[AI-DRAFT]` (OQ-ADJ-01 owner Strike)

### BR-10: ทุก DOA slot ต้องเลือกคนจริง — ห้าม role ID
- **Statement:** ทุก slot ต้องเลือก **คนจริง** (avatar + ตำแหน่ง + ชื่อ) · slot ว่างแม้ช่องเดียว ส่งอนุมัติไม่ได้ · **ห้ามใช้ role ID/ชื่อตำแหน่งลอย ๆ**
- **Enforced by:** F082-FN-06 (assert ทุก slot มี person_id) + F082-FN-08
- **On violation:** ส่งอนุมัติไม่ได้ + ชี้ slot ที่ว่าง · `ERR_APPROVER_SLOT_EMPTY`
- **Scenario:** S-13 · **FN:** FN-17, FN-42 · locked 2026-08-17 (LOCK · ดู 07 §7.0)

### BR-11: ตีกลับต้องมีเหตุผล
- **Statement:** ผู้อนุมัติตีกลับต้องกรอกเหตุผลตีกลับ · ใบกลับเป็น `ร่าง` แก้ได้ · ประวัติเก็บรอบที่ถูกตีกลับ
- **Enforced by:** F082-FN-10 rejectDocument (reject_reason required)
- **On violation:** `ERR_REJECT_REASON_REQUIRED`
- **Scenario:** S-08 · **FN:** FN-22

### BR-12: ประเภทการปรับ (หัวใบ) คุมประเภท bin ที่เลือกได้
- **Statement:** `ตัดจำหน่ายของเสีย`→bin `damage` (DM-*) · `ปรับยอดกักกัน`→bin `quarantine` (QA-*) · `ปรับยอดทั่วไป`→`storage`/`staging`
- **Enforced by:** F082-FN-05 filterBinPicker (bin นอกกลุ่มไม่โผล่ใน picker)
- **Scenario:** S-18/S-19 · **FN:** FN-01, FN-02, FN-46 · Putaway §3.0.2

### BR-13: bin ประเภท in-transit ไม่โผล่ใน picker เลย (negative)
- **Statement:** bin `location_type = in-transit` (TR-*) กรองออกตั้งแต่ต้น — ค้นด้วยรหัส `TR-*` ก็ไม่เจอ ทุกกรณี
- **Enforced by:** F082-FN-05 filterBinPicker (exclude in-transit ก่อน query) + F082-API-13 (server-side filter)
- **Scenario:** S-20 · **FN:** FN-32 (negative) · Putaway §3.0.2 ข้อ 2 · OB-6 (LOCK)

### BR-14: bin ล็อก / โซนปิดชั่วคราว = เลือกไม่ได้
- **Statement:** bin สถานะ `ล็อก` หรือโซน `ปิดชั่วคราว` = แสดงใน picker แต่ disabled + บอกเหตุผลที่ล็อก
- **Enforced by:** F082-FN-05 (mark disabled + reason) · F082-API-13 คืน `locked_reason`
- **On violation:** ชี้ให้ติดต่อหัวหน้าคลัง · `ERR_BIN_LOCKED` (ถ้าฝืนเลือกผ่าน API)
- **Scenario:** S-14 · **FN:** FN-03 · Putaway BR-08

### BR-15: ตรวจยอดซ้ำก่อน post (snapshot vs ยอดล่าสุด)
- **Statement:** ตอนกด "ผ่านรายการ" ถ้ายอดระบบต่างจาก snapshot ตอนสร้างบรรทัด → เตือนและแสดง 2 ยอด (เดิม vs ล่าสุด) ให้เลือก "คิดจากยอดล่าสุด" (คำนวณผลต่างใหม่) หรือ "ตีกลับไปแก้"
- **Enforced by:** F082-FN-12 recheckQtyBeforePost (precondition ของ F082-FN-13 postDocument)
- **On violation / mismatch:** `WARN_QTY_CHANGED` (ไม่บล็อกถาวร — บังคับผู้ใช้เลือก)
- **Scenario:** S-15 · **FN:** FN-27 · gap G-04 · `[AI-DRAFT][STD]` (OQ-ADJ-02 owner Strike)

### BR-16: movement append-only
- **Statement:** movement ห้ามลบ ห้ามแก้ — ไม่มีปุ่มลบ/แก้ movement ที่ใดในระบบ
- **Enforced by:** F082-ENG-02 inventory-movement-engine (insert-only) + ไม่มี DELETE/PUT endpoint สำหรับ movement
- **Scenario:** S-10/S-17 · **FN:** FN-45 · OB-11 (LOCK)

### BR-17: ยกเลิกใบที่ post แล้ว = กลับรายการ (reversal) — routes through DOA ★ FIX-03
- **Statement:** ใบสถานะ `ผ่านรายการ` ไม่มีปุ่ม "ยกเลิก" — มีแต่ "กลับรายการ" (บังคับเหตุผล) → **สร้างใบกลับรายการใหม่** (`is_reversal_doc = true`, ทิศ delta ตรงข้าม) ที่ **ต้องผ่านสาย DOA ตามชั้นมูลค่า (ค่าสัมบูรณ์ของตัวเอง) ก่อน post — ไม่ auto-post** (FIX-03) · movement ทิศตรงข้ามเกิดเมื่อใบกลับรายการ post
- **Enforced by:** F082-FN-14 reverseDocument (reason required · สร้าง reversal doc · resolve DOA ตาม abs ของ reversal) → post ผ่าน F082-FN-13 + F082-ENG-02
- **Scenario:** S-10 · **FN:** FN-25 · OB-11 · **FIX-03 · BA re-gate 2026-09-15** (LOCK) · BRD R19/Q13

### BR-17.1: ต้นฉบับ → กลับรายการแล้ว เมื่อใบกลับรายการ post
- **Statement:** ใบต้นฉบับเปลี่ยนเป็น `reversed` เมื่อใบกลับรายการ post สำเร็จ (ไม่ใช่ตอนกดริเริ่ม) · ผูก `reversal_of` ↔ `reversed_by_doc` 2 ทาง
- **Enforced by:** F082-FN-13 postDocument (เมื่อ posted doc เป็น reversal → set ต้นฉบับ = reversed)

### BR-18: ใบกลับรายการผูกคู่ + กลับรายการซ้ำไม่ได้
- **Statement:** ใบกลับรายการผูก soft-link 2 ทางกับใบเดิมเสมอ · ใบที่ `กลับรายการแล้ว` กลับรายการซ้ำอีกไม่ได้ (ปุ่มหาย)
- **Enforced by:** F082-FN-14 (guard: reversed_by is null ก่อนอนุญาต) + state machine ปลายทางสุดท้าย
- **On violation:** `ERR_ALREADY_REVERSED`
- **Scenario:** S-10 · **FN:** FN-44 · `[AI-DRAFT]`

### BR-19: post แล้วไม่ post JE จริง (mock)
- **Statement:** หลัง post ขึ้นสถานะ `รอลงบัญชี` + marker `FWD-WIRE: JE posting` — **ไม่มีปุ่ม "ลงบัญชี" ที่ทำงานจริง** (W5)
- **Enforced by:** F082-FN-13 postDocument (set je_status = รอลงบัญชี เท่านั้น)
- **Scenario:** S-17 · **FN:** FN-30 · OB-10 · forward-wire owner GL/JE · W5

### BR-20: threshold/อายุค้าง ไม่อยู่ใน feature — อ่านจาก NC rules
- **Statement:** เลข threshold ผลต่าง% / อายุใบค้างอนุมัติ ไม่เก็บใน feature — อ่านจาก NC rules มาแสดงป้ายเท่านั้น · **ไม่มีหน้าตั้งค่า threshold ในนี้**
- **Enforced by:** ไม่มี config screen (negative)
- **Scenario:** ทุก S · **FN:** FN-48 (negative) · OB-15

### BR-21: เลขที่เอกสารออกตอนส่งอนุมัติ
- **Statement:** เลข `ADJ-YYYY-NNNN` ออกตอน**ส่งอนุมัติ** ไม่ใช่ตอนสร้างร่าง (กันเลขกระโดดจากร่างที่ถูกทิ้ง) · ร่างแสดง `(ร่าง — ยังไม่ออกเลขที่)`
- **Enforced by:** F082-FN-08 submitForApproval → เรียก ENG-DOC-NUM (F-DOCCFG) · **ห้าม format/+1 เอง**
- **Scenario:** S-06/S-07 · **FN:** FN-19, FN-20 · OB-8 · `[AI-DRAFT][STD]`

### BR-22: soft-reference — master หลุด/archive ไม่ทำให้ใบพัง
- **Statement:** Item/UOM/Warehouse/Zone/Bin/Cost Center/ผู้อนุมัติ = picker ไม่ FK validate nullable · เก็บข้อความ ณ เวลาที่เลือก · master archive → ใบเดิมยังแสดงข้อความเดิม + ป้าย "ข้อมูลอ้างอิงถูกยกเลิก" ไม่บล็อกการดู
- **Enforced by:** DB nullable FK + denormalized snapshot columns (ดู 04_DB §4.2)
- **Scenario:** S-16 · **FN:** FN-31 · LD-4C-02 · OB-12

### BR-23: ประเภท "ตัดจำหน่ายของเสีย" บังคับแนบหลักฐาน ≥ 1 ไฟล์
- **Statement:** ใบประเภท `ตัดจำหน่ายของเสีย` ที่ยังไม่แนบไฟล์ → ส่งอนุมัติไม่ได้
- **Enforced by:** F082-FN-06 (assert attachment_count ≥ 1 เมื่อ type = ตัดจำหน่ายของเสีย)
- **On violation:** `ERR_EVIDENCE_REQUIRED`
- **Scenario:** S-19/S-21 · **FN:** FN-51 · `[AI-DRAFT]`

### BR-24: ห้ามมีฟังก์ชันนับสต๊อก (negative)
- **Statement:** UI ห้ามมีคำว่า "ใบนับ/นับรอบ/count sheet/blind count" หรือหน้า/ปุ่มการนับ — "ยอดที่ถูกต้อง" เป็น input ระดับบรรทัด ไม่ใช่กระบวนการนับ
- **Enforced by:** โครงหน้าจอ (negative) — cycle count = backlog owner Strike
- **Scenario:** S-24 · **FN:** FN-35 (negative) · OB-7

### BR-25: audit append-only ทุกเหตุการณ์
- **Statement:** ทุก create/แก้/ส่ง/อนุมัติ/ตีกลับ/post/กลับรายการ บันทึก audit append-only (ใคร-เมื่อไหร่-ค่าเดิม/ค่าใหม่) · ไม่มีทางลบประวัติ
- **Enforced by:** middleware audit (ดู 04_DB §4.2 T_audit_log) — ทุก mutation API
- **Scenario:** ทุก S · **FN:** FN-39 · OB-11

### BR-26 ★: แหล่งที่มา = "จากใบนับ" → บังคับ ref_count_doc
- **Statement:** หัวใบเลือก `แหล่งที่มา = จากใบนับ` → บังคับเลือก `ref_count_doc` (เลขใบนับ F084/F086) · `ปรับตรง` = ไม่บังคับ · view drawer โชว์ "ใบนับต้นเรื่อง" ลิงก์ trace กลับ **display-only ไม่เปิด/สร้างหน้าใบนับ**
- **Enforced by:** F082-FN-06 (assert ref_count_doc != null เมื่อ source = count) — enforced ใน wizardNext + submitForApproval
- **On violation:** ส่งอนุมัติไม่ได้ · `ERR_COUNT_DOC_REQUIRED`
- **Scenario:** S-26 · **FN:** FN-52 · **FIX-04 · BA re-gate 2026-09-15** (LOCK)

### BR-27 ★: ยกเลิกได้เฉพาะ ร่าง/รออนุมัติ
- **Statement:** ปุ่ม "ยกเลิก" โผล่เฉพาะสถานะ `ร่าง`/`รออนุมัติ` (บังคับเหตุผล · ใบยังอยู่ในระบบ) · **`อนุมัติแล้ว` ยกเลิกไม่ได้** (ไม่มีปุ่ม) · post แล้วกลับรายการเท่านั้น · **ไม่มี transition อนุมัติแล้ว→ยกเลิก**
- **Enforced by:** F082-FN-11 cancelDocument (precondition: status ∈ {ร่าง, รออนุมัติ}) + state machine
- **On violation:** `ERR_CANCEL_NOT_ALLOWED`
- **Scenario:** S-09 · **FN:** FN-24 · **FIX-02 · BA re-gate 2026-09-15** (LOCK)

---

## §5.2 State Machine

### สถานะเอกสาร (6 states)

```
ร่าง ──ส่งอนุมัติ──▶ รออนุมัติ ──อนุมัติครบทุก slot──▶ อนุมัติแล้ว ──ผ่านรายการ──▶ ผ่านรายการ (posted)
 │                    │                                                                │
 │                    └──ตีกลับ+เหตุผล──▶ ร่าง                                          └──กลับรายการ+เหตุผล──▶ กลับรายการแล้ว
 └──ยกเลิก+เหตุผล──▶ ยกเลิก      └──ยกเลิก+เหตุผล──▶ ยกเลิก
```

> ★ **`อนุมัติแล้ว` ไม่มีทางไป `ยกเลิก`** (BR-27 · FIX-02) — post แล้วกลับรายการเท่านั้น
> Status values (snake_case สำหรับ DB/API — ยึดตาม HTML ตัวจริง — label ไทยตามหน้าจอ): `draft` (ร่าง) · `pending` (รออนุมัติ) · `approved` (อนุมัติแล้ว) · `posted` (ผ่านรายการ) · `cancelled` (ยกเลิก) · `reversed` (กลับรายการแล้ว)
> **แยกจาก** `approval_status` (BRD §6.2 #14): draft/pending_approval/approved/rejected/cancelled — เป็น sub-state ของสายอนุมัติ (map กับ status)

| From | To | Action (ปุ่ม) | ใครกด | เงื่อนไข | Function | Scenario |
|---|---|---|---|---|---|---|
| draft | pending | ส่งอนุมัติ | เจ้าหน้าที่คลัง/หัวหน้าคลัง | ≥1 บรรทัด · ทุกบรรทัด BR-02/03/06/07 ผ่าน · ทุก DOA slot มีคนจริง (BR-10) · หลักฐานครบถ้าบังคับ (BR-23) · ref_count_doc ครบถ้า source=count (BR-26) → ออกเลขที่ (BR-21) | F082-FN-08 | S-07 |
| pending | pending (ชั้นถัดไป) | อนุมัติ | ผู้อนุมัติ slot ปัจจุบัน | อนุมัติแล้วยังมี slot เหลือ · SoD (ไม่ใช่ผู้จัดทำ) | F082-FN-09 | S-12 |
| pending | approved | อนุมัติ | ผู้อนุมัติ slot สุดท้าย | ทุก slot อนุมัติครบ | F082-FN-09 | S-07/S-11 |
| pending | draft | ตีกลับ | ผู้อนุมัติ | เหตุผลตีกลับบังคับ (BR-11) | F082-FN-10 | S-08 |
| approved | posted | ผ่านรายการ | หัวหน้าคลัง | ผ่าน BR-15 ตรวจยอดซ้ำ → movement append-only + JE marker | F082-FN-12 → F082-FN-13 | S-07/S-17 |
| draft / pending | cancelled | ยกเลิก | ผู้จัดทำ/หัวหน้าคลัง | เหตุผลยกเลิกบังคับ · **`approved` ยกเลิกไม่ได้** (BR-27) | F082-FN-11 | S-09 |
| posted | reversed | กลับรายการ | หัวหน้าคลัง (ริเริ่ม) + สาย DOA ของใบกลับรายการ | เหตุผลบังคับ → **สร้างใบกลับรายการใหม่ (is_reversal_doc)** → ใบนั้นวิ่ง draft→pending→approved→posted ตามสาย DOA (FIX-03) → เมื่อ post: ต้นฉบับ = reversed + movement ทิศตรงข้าม (BR-17/17.1/18) | F082-FN-14 → F082-FN-08/09/13 | S-10 |
| reversed | — | — | — | ปลายทางสุดท้าย · กลับรายการซ้ำไม่ได้ (BR-18) | — | S-10 |
| cancelled | — | — | — | ปลายทางสุดท้าย · ใบยังอยู่ในระบบ ไม่ลบ | — | S-09 |

### Movement lifecycle (append-only)

```
[post ใบ ADJ]  ──▶  movement "ปรับเพิ่ม/ปรับลด" (แถวถาวร ห้ามแก้ ห้ามลบ)
[กลับรายการ]   ──▶  movement "กลับรายการปรับเพิ่ม/ปรับลด" (แถวใหม่ ทิศตรงข้าม)
                     └── ผูก soft link 2 ทางกับแถวเดิมเสมอ (BR-18)
```

---

## §5.3 Permission Matrix

> สิทธิ์ทั้งหมด `[AI-DRAFT]` — ผูกกับ Security Preset ตอน BRD · การกำหนดจริงเป็นของ Policy Center (ไม่ hardcode ใน feature) · OQ-ADJ-06

| Role | View | Create/แก้ร่าง | ส่งอนุมัติ | อนุมัติ/ตีกลับ | ผ่านรายการ | ยกเลิก | กลับรายการ |
|---|---|---|---|---|---|---|---|
| เจ้าหน้าที่คลัง (warehouse_officer) | ใบตัวเอง + ใบในคลังที่สังกัด | ✅ | ✅ | — | — | ยกเลิกร่างตัวเอง | — |
| หัวหน้าคลัง (warehouse_supervisor) | ทุกใบในคลังที่ดูแล | ✅ | ✅ | — | ✅ | ✅ | ✅ (ขอ) |
| ผู้อนุมัติ (approver — ตาม DOA slot) | ใบที่ส่งมาถึง slot ตัวเอง | — | — | ✅ (เฉพาะ slot ตัวเอง) | — | — | — |
| บัญชี (accounting — อ่านอย่างเดียวรอบนี้) | ใบที่ post แล้ว + มูลค่า + เหตุผล | — | — | — | — | — | — |
| ผู้ตรวจสอบ (auditor) | ทุกใบทุกสถานะ + ประวัติเต็ม | — | — | — | — | — | — |

**SoD (Segregation of Duties):** ผู้อนุมัติ slot ต้องไม่ใช่ผู้จัดทำใบเดียวกัน (can't approve own) — enforced ใน F082-FN-09 (`ERR_SOD_SELF_APPROVAL`).

---

## §5.4 Field Validation Rules (VR)

> Per-field declarative — engine-agnostic

| VR | Field | Rule | Error code |
|---|---|---|---|
| VR-01 | header.warehouse | required, soft-ref (ไม่ FK) | `ERR_WAREHOUSE_REQUIRED` |
| VR-02 | header.effective_date | required, ≤ วันนี้, ย้อนหลังได้เฉพาะงวดที่ยังเปิด (`[AI-DRAFT]` — กติกางวดจริง = W5) | `ERR_INVALID_EFFECTIVE_DATE` |
| VR-03 | header.adjustment_type | required, enum {ปรับยอดทั่วไป, ตัดจำหน่ายของเสีย, ปรับยอดกักกัน} | `ERR_INVALID_ADJ_TYPE` |
| VR-04 | header.source | required, enum {ปรับตรง, จากใบนับ}, default ปรับตรง | `ERR_INVALID_SOURCE` |
| VR-05 | header.ref_count_doc | required **iff** source = จากใบนับ (BR-26) · nullable เมื่อ ปรับตรง · soft-ref display-only | `ERR_COUNT_DOC_REQUIRED` |
| VR-06 | line.bin | required, soft-ref, กรองตาม type+warehouse (BR-12/13/14) | `ERR_BIN_REQUIRED` |
| VR-07 | line.item | required, soft-ref (ไม่ FK), เก็บ snapshot ข้อความ | `ERR_ITEM_REQUIRED` |
| VR-08 | line.correct_qty (โหมด 1) | required (โหมด 1), `≥ 0`, ≠ ยอดระบบ (BR-02) | `ERR_ZERO_DELTA` |
| VR-09 | line.adjust_qty (โหมด 2) | required (โหมด 2), `≠ 0`, ยอดระบบ + adjust_qty ≥ 0 (BR-03) | `ERR_NEGATIVE_STOCK` |
| VR-10 | line.reason_code | required ทุกบรรทัด (BR-06), ตรงทิศ (BR-07) | `ERR_REASON_REQUIRED` / `ERR_REASON_DIRECTION_MISMATCH` |
| VR-11 | line.reason_note | required เมื่อ reason_code = RS-99 (อื่น ๆ) หรือ reason ที่ flag "อธิบายเพิ่ม" | `ERR_REASON_NOTE_REQUIRED` |
| VR-12 | approval.slots[] | ทุก slot มี person_id (คนจริง) ก่อนส่ง (BR-10) | `ERR_APPROVER_SLOT_EMPTY` |
| VR-13 | attachment | ≥1 ไฟล์เมื่อ type = ตัดจำหน่ายของเสีย (BR-23) | `ERR_EVIDENCE_REQUIRED` |
| VR-14 | reject/cancel/reverse.reason | required (BR-11/BR-17/BR-27) | `ERR_ACTION_REASON_REQUIRED` |
| VR-15 | line (bin,item) pair | unique ในใบเดียว (BR-01) | `ERR_DUPLICATE_BIN_ITEM` |

### Cross-field / computed (ไม่ใช่ user input)
- `line.delta = correct_qty − system_qty(snapshot)` (โหมด 2: `= adjust_qty`)
- `line.value = delta × ref_cost` (ref_cost = mock จาก Item Master · `FWD-WIRE: valuation engine` W5)
- `header.abs_total = Σ |line.value|` — **ฐาน DOA** (BR-09)
- `header.net_total = Σ line.value` — แสดงอย่างเดียว
- คำนวณโดย F082-ENG-01 adjustment-valuation-engine (ดู 03_LOGIC §3.2)

---

## §5.5 Edge Cases (Phase 2.5 Probing — Lane Mode / no-ask · conservative default + `[AI-DEFAULT]`)

> Trigger patterns: approval multi-step → PR-1, PR-3 · submit/mutation → PR-4, PR-7 · draft wizard → PR-6 · reverse → PR-8 · inventory counter → PR-9 · stale/real-time → PR-2
> คำตอบส่วนใหญ่ map เข้ากติกาที่ PREBRIEF กำหนดไว้แล้ว (BR-15/17/18/21). ที่เป็น default ใหม่ tag `[AI-DEFAULT]` + ยก Open Question (00_OVERVIEW §0.8)

### EC-01: Concurrent approval (PR-1)
- **Scenario:** ผู้อนุมัติ slot เดียวกัน 2 คน (หรือ retry) กด approve พร้อมกัน
- **Resolution:** optimistic lock ด้วย `version` column — คนแรก commit ได้ คนสอง 409 · `ERR_STALE_DATA` · `[AI-DEFAULT]` (OQ-08)
- **Test:** TC-CC-01 (06_TESTS §6.2)

### EC-02: Idempotency / double-submit (PR-4, PR-7)
- **Scenario:** ผู้ใช้ double-click ส่งอนุมัติ/ผ่านรายการ หรือ network ขาดแล้ว retry
- **Resolution:** ทุก mutation API รับ `Idempotency-Key` header — key เดิม+body เดิม → คืน cached response (ไม่สร้างซ้ำ ไม่ post movement ซ้ำ) · cache 24hr · `[AI-DEFAULT]` (OQ-08). สอดคล้อง FN-92 (กัน double-submit)
- **Test:** TC-ID-01

### EC-03: Permission revoked mid-flight (PR-3)
- **Scenario:** ผู้ใช้เปิดใบตอนมีสิทธิ์ แล้วถูกถอดสิทธิ์ก่อนกดยืนยัน
- **Resolution:** re-check role ตอน mutation (ไม่ใช่แค่ตอน GET) · `ERR_PERMISSION_REVOKED` · `[AI-DEFAULT]` (OQ-08)
- **Test:** TC-PR-01

### EC-04: ยอดระบบเปลี่ยนระหว่างรออนุมัติ (PR-2, PR-9) ★ core edge
- **Scenario:** มี movement อื่น (Putaway/Transfer/เบิก) เข้ามาที่ (bin, สินค้า) เดียวกันหลัง snapshot
- **Resolution:** BR-15 — ตอน post เทียบ snapshot vs ยอดล่าสุด ถ้าต่าง เตือน 2 ยอด ให้เลือก "คิดจากยอดล่าสุด" หรือ "ตีกลับไปแก้" (ไม่ overwrite เงียบ) · **จาก PREBRIEF (ไม่ใช่ AI-DEFAULT)**
- **Test:** TC-QTY-01 · **FN:** FN-27

### EC-05: Draft resume (PR-6)
- **Scenario:** ผู้ใช้กรอก wizard ค้าง ปิด browser กลับมาทีหลัง
- **Resolution:** ร่างบันทึกเป็น record จริง (status=draft, ยังไม่มีเลขที่ · BR-21) — persist ในระบบ ไม่หมดอายุอัตโนมัติรอบนี้ · `[AI-DEFAULT]` (OQ-09: draft expiry policy รอ BA)
- **Test:** TC-DRAFT-01 · **FN:** FN-19

### EC-06: Reversal เป็น compensation (PR-8)
- **Scenario:** ใบ post แล้วต้องแก้
- **Resolution:** ไม่มี refund/undo — สร้างใบกลับรายการ movement ทิศตรงข้าม ผูกคู่ (BR-17/18) · กลับรายการซ้ำไม่ได้ · **จาก PREBRIEF**
- **Test:** TC-REV-01 · **FN:** FN-25, FN-44

### EC-07: สินค้า/หน่วย archive จาก master (soft-ref)
- **Scenario:** Item ถูก archive หลังสร้างใบ
- **Resolution:** BR-22 — แสดงข้อความเดิมที่ snapshot ไว้ + ป้าย "ข้อมูลอ้างอิงถูกยกเลิก" ไม่ FK validate ไม่พัง · **จาก PREBRIEF**
- **Test:** TC-SOFT-01 · **FN:** FN-31

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause / BR |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | Generic field validation |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | No/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | Role mismatch |
| `ERR_PERMISSION_REVOKED` | 403 | error.auth.revoked | EC-03 mid-flight |
| `ERR_SOD_SELF_APPROVAL` | 403 | error.approval.sod | อนุมัติใบตัวเอง (§5.3 SoD) |
| `ERR_NOT_FOUND` | 404 | error.notfound | Resource missing |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | EC-01 version mismatch |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | EC-02 same key diff body |
| `ERR_INVALID_STATE_TRANSITION` | 422 | error.state.transition | BR-08 · state machine §5.2 |
| `ERR_CANCEL_NOT_ALLOWED` | 422 | br.cancel.not_allowed | **BR-27** (approved ยกเลิกไม่ได้) |
| `ERR_ALREADY_REVERSED` | 422 | br.reverse.already | **BR-18** |
| `ERR_DUPLICATE_BIN_ITEM` | 422 | br.line.dup | BR-01 · VR-15 |
| `ERR_ZERO_DELTA` | 422 | br.line.zero_delta | BR-02 · VR-08 |
| `ERR_NEGATIVE_STOCK` | 422 | br.line.negative | BR-03 · VR-09 |
| `ERR_REASON_REQUIRED` | 422 | br.reason.required | BR-06 · VR-10 |
| `ERR_REASON_DIRECTION_MISMATCH` | 422 | br.reason.direction | BR-07 · VR-10 |
| `ERR_REASON_NOTE_REQUIRED` | 422 | br.reason.note | BR-06 · VR-11 |
| `ERR_APPROVER_SLOT_EMPTY` | 422 | br.approver.empty | BR-10 · VR-12 |
| `ERR_EVIDENCE_REQUIRED` | 422 | br.evidence.required | BR-23 · VR-13 |
| `ERR_COUNT_DOC_REQUIRED` | 422 | br.countdoc.required | **BR-26** · VR-05 |
| `ERR_ACTION_REASON_REQUIRED` | 422 | br.action.reason | BR-11/17/27 · VR-14 |
| `ERR_BIN_LOCKED` | 422 | br.bin.locked | BR-14 |
| `ERR_REJECT_REASON_REQUIRED` | 422 | br.reject.reason | BR-11 |
| `WARN_QTY_CHANGED` | 200 (warn) | warn.qty.changed | BR-15 (ไม่บล็อก — บังคับเลือก) |

---

## §5.7 Security Bible Application

> Domains triggered: **D2 (Auth)** · **D5 (Financial — มูลค่าปรับ)** · **D9 (Audit)** · **D15 (Admin/Approval actions)** · **D17 (Multi-tenant)** · **D-CLASS (Data Classification)**

### D2: Authentication & Session
- ทุก endpoint ต้องมี JWT · role-based · SoD ระดับ business (§5.3)

### D5: Financial Transactions
- มูลค่าที่ปรับ (value/abs_total/net_total) = การเงิน → audit log ทุก mutation (BEFORE+AFTER)
- Approval workflow ตามมูลค่า (DOA · BR-08/09) — วงเงินมาจาก F-DLG-001 ไม่ hardcode
- **JE ยังไม่ post จริง (BR-19)** — reconciliation จริงรอ W5

### D9: Audit Logging
- ทุก mutation → T_audit_log (append-only, immutable) · retention 7 ปี (financial 10 ปี) · BR-25 · FN-39

### D15: Admin / Approval Actions
- ทุก state transition logged · ผู้อนุมัติ identity บันทึก (คนจริง BR-10) · เหตุผลบังคับ reject/cancel/reverse

### D17: Multi-Tenant Isolation
- PostgreSQL RLS · API middleware validate `X-Tenant-Id` · cross-tenant queries ห้าม
- Row scope เพิ่มเติม: ใบ scope ตามคลังที่ผู้ใช้สังกัด (§5.3)

### D-CLASS: Data Classification (v5.1)
รายละเอียดต่อ field: 04_DB §4.2 + §4.6. Enforcement summary:

| Layer | Confidential fields (มูลค่า/ต้นทุน/ผู้อนุมัติ-PII) |
|---|---|
| API response | mask/omit ถ้า role ไม่ผ่าน (บัญชี/auditor เห็นมูลค่า · เจ้าหน้าที่เห็นของตัวเอง) |
| UI display | แสดง `***` ถ้าไม่มีสิทธิ์เห็นมูลค่า |
| Export/Print | PDF มูลค่า → เฉพาะ role ที่ผ่าน |
| Audit | log view + mutation |

**Wire points:** Policy Center → Data Classification (master/override) · Policy Center → PDPA consent (ผู้อนุมัติ/ผู้จัดทำ = person data). **ไม่มี field ระดับ Restricted** (ไม่มีเงินเดือน/ข้อมูลบุคคลระดับ ACL) — highest = Confidential.

---

## §5.8 Compliance & Audit Requirements

| Requirement | Implementation |
|---|---|
| ปี ค.ศ. ล้วน ทุก timestamp/วันที่ (จอ + PDF) | OB-14 · FN-38 |
| Audit trail ใคร-เมื่อไหร่-อะไร (append-only) | BR-25 · FN-39 · T_audit_log |
| movement ย้อนรอยได้ + คู่ reversal | BR-16/18 · FN-29 |
| เลขรันควบคุมกลาง (no self-format) | BR-21 · OB-8 · ENG-DOC-NUM (F-DOCCFG) |
| หลักฐานการทำลาย (ตัดจำหน่าย) | BR-23 · FN-51 |

---

## §5.9 Externalized Constants (ไม่ hardcode ใน feature)

> ตัวเลข/เกณฑ์ทั้งหมดที่ "ห้ามอยู่ในโค้ด feature" — อ่านจากแหล่งกลาง (BR-20)

| Constant | เจ้าของ | หมายเหตุ |
|---|---|---|
| วงเงิน DOA (จุดตัด 20,000 / 200,000 / 1,000,000) + จำนวนชั้น | **F-DLG-001 (DOA)** ผ่าน DOA_BRIEF | feature ส่ง `abs_total` ไปให้ resolve · `[DEFAULT — รอยืนยัน]` |
| threshold ผลต่าง % / อายุใบค้างอนุมัติ | **NC rules** | feature แสดงป้ายเท่านั้น · BR-20 · FN-48 |
| รูปแบบเลขรัน `ADJ-YYYY-NNNN` | **F-DOCCFG** ผ่าน DOCCFG_BRIEF | ออกตอนส่งอนุมัติ · ค.ศ. · BR-21 |
| ต้นทุนอ้างอิง/valuation | **W5 (Inventory Valuation)** | mock จาก Item Master · `[ASSUMED contract]` · gap G-01 |
| บัญชีปลายทางต่อเหตุผล (mock) | **W5 (GL/JE)** | master เหตุผลมี field บัญชีปลายทาง mock · gap G-05 |
| ช่องทาง/เงื่อนไขแจ้งเตือน | **F-NOTIFY** ผ่าน NTF_BRIEF | ห้าม hardcode |
