# 05_RULES — F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> **Audience:** BE dev + QA
> ทุก BR ที่นี่สืบทอดหมายเลขจาก BRD §9.1 (BR-01…BR-24) — **ไม่เปลี่ยนเลข** เพื่อให้ trace ข้ามเอกสารได้

## §5.1 Business Rules (BR)

### BR-01 · กระบอกต้องเรียง `0 < min < mid < max`
บล็อกตั้งแต่ร่าง · ชี้แถวที่ผิดแบบเจาะจง · **ตรวจซ้ำหลังปรับเปอร์เซ็นต์ทั้งชุด** (EC-24) · บังคับที่ `assertBandOrder` + CHECK constraint

### BR-02 · เวอร์ชันมีวันมีผลเสมอ · ห้ามแก้เวอร์ชันที่ใช้งานอยู่
แก้ได้เฉพาะ `draft` (`assertVersionEditable`) · การเปลี่ยนค่า = สร้างเวอร์ชันใหม่ · เวอร์ชันที่ 2 ขึ้นไปบังคับ `change_reason` ≥10 ตัวอักษร · **P-2′**

### BR-03 · ช่วงเวลาของ (ระดับ × ขอบเขตบริษัท) ห้ามทับกัน
บังคับ 2 ชั้น: `assertNoOverlap` (logic) + `EXCLUDE USING gist` (DB) · error ระบุ `conflicting_version_id` · **P-3′**

### BR-04 · ห้ามตั้งวันมีผลย้อนเข้างวดที่ปิดแล้ว
นิยาม "งวดปิด" มาจาก **HR Configuration `period_rule`** เท่านั้น (ห้ามเก็บสำเนา) · `assertNotInClosedPeriod` ตรวจ **2 ครั้ง** (ตอน validate + ตอน commit) · error พก `period_code` + `earliest_open_date` · **P-7′**

### BR-05 · ไม่มี hard delete · ประวัติ append-only
ไม่มี DELETE endpoint · trigger ปฏิเสธ UPDATE ค่าเงิน/วันมีผลบนแถวสถานะ `current`/`history`/`ended` · ปิดใช้ = `status='inactive'` (soft archive) · **P-4′**

### BR-06 · ฐานที่ใช้เทียบกระบอก
= ผลรวม component ที่ `include_in_band_base = true` ณ วันที่ · **default = เงินเดือนฐานตัวเดียว** · ไม่มีตัวไหนติดแฟล็ก → เตือน + ใช้ `BASE` · `[ASSUMED]` **OQ-STD-09**

### BR-07 · compa-ratio / range penetration
`compa_ratio = fte_adjusted_base ÷ mid` · `range_penetration = (fte_adjusted_base − min) ÷ (max − min)` · **แสดงผลอย่างเดียว ไม่ใช่เกณฑ์อนุมัติ** · ไม่มีกระบอก ณ วันที่ → คืน `null` (จอแสดง "—")

### BR-08 · อัตรานอกกระบอก = เตือน ไม่บล็อก
ต่ำกว่า min หรือเกิน max → **บังคับ `out_of_range_reason`** แล้วบันทึกได้ · ติดธง + ขึ้นรายงาน · `[AI-DRAFT]` **OQ-SS-01** (ยังไม่เคาะว่าจะเปลี่ยนเป็นบล็อกไหม — **ห้าม implement โหมดบล็อกจนกว่าจะเคาะ**)

### BR-09 · FTE < 1
เทียบกระบอกด้วย `band_base ÷ fte` · แสดงทั้งค่าจริงกับค่าปรับแล้ว · ช่วงที่ยอมรับ 0.01–1.00 · `[ASSUMED]` **OQ-STD-03**

### BR-10 · ข้อมูลควบคุมของทุกเรคคอร์ดอัตรา
ต้องมี ระดับ + เงินเดือนฐาน + วันมีผล + `change_reason` (≥10) · ถ้ามาจากคำสั่งต้องมี `movement_doc_no`

### BR-11 · อัตรา "ปัจจุบัน" มีได้เรคคอร์ดเดียวต่อคนต่อเวลา
บันทึกใหม่ = ปิดช่วงเดิมเป็น `history` อัตโนมัติ (ไม่ลบ) · บังคับด้วย EXCLUDE constraint

### BR-12 · องค์ประกอบแบบเปอร์เซ็นต์ห้ามอ้างตัวเอง/อ้างวน
`detectComponentCycle` เดินกราฟก่อนบันทึก · error คืน `cycle_path[]`

### BR-13 · `payroll_code` เป็นสะพานไป Payroll · **feature นี้ไม่คำนวณภาษี/ปกส./ยอดสุทธิ**
payload ที่มี key เหล่านั้น → `400 ERR_FIELD_NOT_SUPPORTED` · ยอดรวมที่แสดงต้องกำกับ "ไม่ใช่ยอดจ่ายสุทธิ" เสมอ

### BR-14 · เงินหักที่มียอดเป้าหมาย
ปิดเมื่อ `accrued_amount ≥ goal_amount` **หรือ** เลย `effective_to` → `item_status = ended` + `end_trigger` · รายการที่ `ended` **ไม่ถูกส่งออกไปกับ `/resolve`** (EC-15 · D-09)

### BR-15 · ช่วงวันของ (พนักงาน × component) ห้ามทับกัน
`assertNoOverlap` + EXCLUDE constraint · error ระบุ `conflicting_item_id` + ช่วงที่ชน

### BR-16 · ข้อมูลค่าจ้างรายบุคคล = RESTRICTED
ปิดบังที่ **ชั้น API** ทุกช่องทาง (list · detail · รายงาน · export · `/resolve`) ผ่าน **ENG-MASK-01** ของ Policy Center · การเปิดดู detail ถูกบันทึก audit + ยิง E10 · **ห้ามทำ permission logic เอง**

### BR-17 · ค่านโยบายอ่านจาก HR Configuration เสมอ
`resolveHrConfig(date, companyId, group)` — ส่ง `date` เสมอ (C-1) · เก็บ `version_id` (C-2) · cache ภายในวัน + ล้างเมื่อได้ event (C-3) · **ไม่มีค่านโยบายฝังในโค้ด/หน้าจอ**

### BR-18 · ค่าที่ต้นทางปิดใช้
แสดงของเดิมได้ + ป้าย "ปิดใช้แล้ว" · หายจากตัวเลือกใหม่ (`filterActiveOptions`) · **C-5**

### BR-19 · soft reference (LD-4C-02)
เก็บ `id` + snapshot ชื่อ · nullable · **ไม่มี FK ข้าม feature · ไม่มี cascade** · ต้นทางหาย → ยังแสดง snapshot ได้

### BR-20 · การอ่านของ consumer ต้องคืน `version_id` เสมอ
ไม่มีโหมด "ค่าปัจจุบันไม่ระบุวัน" · `date` ไม่ส่ง = `400 ERR_RESOLVE_DATE_REQUIRED` · **P-5′**

### BR-21 · ไม่มี transition อนุมัติในแพ็กนี้
ไม่มี endpoint `/approve` · ไม่มีสถานะ `pending_approval` · ไม่มีสาย DOA · ไม่มีเลขที่เอกสารที่ระบบนี้ออกเอง · การอนุมัติอยู่ที่ **Employee Movement (W3)**

### BR-22 · where-used ก่อนปิดใช้
`countWhereUsed` ต้องถูกเรียกแล้ว client ยืนยันจำนวน (`acknowledged_where_used_count`) ก่อน `deactivate` · ลงทะเบียนการใช้งานกลับไปที่ HR Configuration (C-6)

### BR-23 · ค่าแรงขั้นต่ำตามกฎหมาย
อ่านจาก HR Configuration `group=legal_minimum` ณ `effective_date` · ต่ำกว่า → **เตือน ไม่บล็อก + บังคับเหตุผล** + ติดธง + เก็บ `legal_min_version_id` · ต้นทางยังไม่มีค่า → แสดง "ยังไม่ได้ตั้งค่าขั้นต่ำที่ตั้งค่า HR" · **ห้ามมีตัวเลขขั้นต่ำในโค้ด/หน้าจอ/ตาราง** · **P-8′ · OQ-STD-11**

### BR-24 · ประเภทการเปลี่ยน (enum เป็นข้อมูล)
`change_reason_code` บังคับ · ค่ามาจาก `T_ss_change_reason` (config table + seed 5) — **ห้ามฝัง enum ในโค้ด** · `[ASSUMED]` OQ-BRD-02

## §5.2 State Machine

### A · เวอร์ชันกระบอก / องค์ประกอบ
| จาก | ไป | ใครทำ | เงื่อนไข | event |
|---|---|---|---|---|
| (ใหม่) | `draft` | HR Comp Admin | ผ่าน BR-01 | — |
| `draft` | `scheduled` | HR Comp Admin | BR-02/03/04/23 + เหตุผล | `salstruct.published` |
| `draft` | (ทิ้ง) | HR Comp Admin | ยังไม่ประกาศ | — |
| `scheduled` | `active` | **ระบบ** | ถึงวันมีผล (`advanceEffectiveStates`) | `salstruct.effective` |
| `scheduled` | `cancelled` | HR Comp Admin | บังคับเหตุผล | `salstruct.cancelled` |
| `active` | `superseded` | **ระบบ** | มีเวอร์ชันใหม่มีผล | (รวมใน `salstruct.effective`) |
| `active` | `inactive` | HR Comp Admin / HR Manager | เหตุผล + ยืนยัน where-used | `salstruct.deactivated` |
| `inactive` | `scheduled` (เวอร์ชันใหม่) | HR Comp Admin | สร้างใหม่เท่านั้น | `salstruct.published` |
| `active` | (แก้ค่าตรง) | — | ❌ ไม่มี transition นี้ (P-2′) | — |
| ใด ๆ | (ลบ) | — | ❌ ไม่มี (P-4′) | — |
| ใด ๆ | (รออนุมัติ) | — | ❌ ไม่มี (BR-21) | — |

### B · อัตรารายคน
| จาก | ไป | ใครทำ | เงื่อนไข | event |
|---|---|---|---|---|
| (ไม่มีอัตรา) | `scheduled` | HR Comp Admin **หรือ** API-26 | BR-04/08/10/11/23/24 | — |
| `scheduled` | `current` | **ระบบ** | ถึงวันมีผล | `salcomp.assigned` |
| `scheduled` | `cancelled` | HR Comp Admin | บังคับเหตุผล | `salcomp.cancelled` |
| `current` | `history` | **ระบบ** | มีเรคคอร์ดใหม่มีผล | (รวมใน `salcomp.assigned`) |
| `current` | `ended` | ระบบ / HR Comp Admin | พ้นสภาพ | `salcomp.ended` |
| `history` | (แก้/ลบ) | — | ❌ append-only | — |

### C · รายการประจำ
| จาก | ไป | ใครทำ | เงื่อนไข | event |
|---|---|---|---|---|
| (ใหม่) | `scheduled` | HR Comp Admin | BR-04, BR-15 | — |
| `scheduled` | `active` | **ระบบ** | ถึง `effective_from` | `salrecur.started` |
| `active` | `ended` | **ระบบ** | ครบเป้า หรือ ถึง `effective_to` | `salrecur.ended` |
| `scheduled`/`active` | `cancelled` | HR Comp Admin | บังคับเหตุผล | `salrecur.ended` (`withdrawn`) |

## §5.3 Permission Matrix

| Action | HR Comp Admin | HR Manager | หัวหน้าสายงาน | พนักงานทั่วไป | service (consumer) |
|---|:---:|:---:|:---:|:---:|:---:|
| อ่านระดับ/กระบอก | ✅ | ✅ | ✅ | ✅ | ✅ (API-25) |
| สร้าง/ประกาศ/ถอน เวอร์ชัน | ✅ | ❌ | ❌ | ❌ | ❌ |
| ปิดใช้/เปิดใช้ ระดับ | ✅ | ✅ | ❌ | ❌ | ❌ |
| สร้าง/ปิดใช้ องค์ประกอบ | ✅ | ❌ | ❌ | ❌ | ❌ |
| อ่านตัวเลขอัตรา (ไม่ปิดบัง) | ✅ | ✅ | ✅ เฉพาะลูกทีม (**ABAC**) | ❌ | ✅ ตามสิทธิ์ service |
| ผูก/แก้/ถอน/ปิดช่วง อัตรา | ✅ | ❌ | ❌ | ❌ | ✅ เฉพาะ API-26 (Movement) |
| เพิ่ม/ถอน รายการประจำ | ✅ | ❌ | ❌ | ❌ | ❌ |
| ปรับ Module Linkage | ✅ | ✅ | ❌ | ❌ | ❌ |
| ลบถาวร / ส่งอนุมัติ | ❌ **ไม่มีในระบบ** | ❌ | ❌ | ❌ | ❌ |

## §5.4 Field Validation Rules

### Per-field
| VR | Field | เงื่อนไข | ประเภท | Error code |
|---|---|---|---|---|
| VR-01 | `grade_code` | unique ต่อขอบเขตบริษัท | Error | `ERR_GRADE_CODE_DUPLICATE` |
| VR-02 | `min/mid/max` | `0 < min < mid < max` | Error | `ERR_BAND_ORDER_INVALID` |
| VR-03 | `effective_date` (เวอร์ชัน) | ไม่ทับช่วงเดิม | Error | `ERR_EFFECTIVE_OVERLAP` |
| VR-04 | `effective_date` (ทุกวัตถุ) | ไม่ตกในงวดที่ปิด | Error | `ERR_EFFECTIVE_IN_CLOSED_PERIOD` |
| VR-05 | `change_reason` | ≥10 ตัวอักษร | Error | `ERR_REASON_REQUIRED` |
| VR-06 | `change_reason_code` | ต้องเป็นค่าที่ active | Error | `ERR_CHANGE_REASON_CODE_REQUIRED` |
| VR-07 | `base_amount` | > 0 | Error | `ERR_AMOUNT_INVALID` |
| VR-08 | `base_amount` vs กระบอก | นอกช่วง → ต้องมีเหตุผล | Warning + Prevent | `ERR_OUT_OF_RANGE_REASON_REQUIRED` |
| VR-09 | ค่าเงิน vs ค่าขั้นต่ำตามกฎหมาย | ต่ำกว่า → ต้องมีเหตุผล | Warning + Prevent | `ERR_LEGAL_MIN_REASON_REQUIRED` |
| VR-10 | ค่าขั้นต่ำตามกฎหมาย | ต้นทางไม่มีค่า | Warning | (แสดงข้อความ ไม่ใช่ error) |
| VR-11 | `fte` | 0.01–1.00 | Error | `ERR_FTE_OUT_OF_RANGE` |
| VR-12 | `base_component_code` | ห้ามอ้างวน | Error | `ERR_COMPONENT_CYCLE` |
| VR-13 | `payroll_code` | บังคับ | Error | `ERR_PAYROLL_CODE_REQUIRED` |
| VR-14 | รายการประจำ | ช่วงห้ามทับ | Error | `ERR_RECURRING_OVERLAP` |
| VR-15 | `effective_to` | ≥ `effective_from` | Error | `ERR_END_DATE_BEFORE_EFFECTIVE` |
| VR-16 | `goal_amount` | เฉพาะรายหัก | Error | `ERR_GOAL_ONLY_FOR_DEDUCTION` |
| VR-17 | `grade_code` ที่เลือกใหม่ | ต้อง active ณ วันมีผล | Error | `ERR_GRADE_INACTIVE` |
| VR-18 | `companies[]` | ≥1 เมื่อ `company_scope=specific` | Error | `ERR_COMPANY_REQUIRED` |
| VR-19 | ปิดใช้ | ต้องยืนยัน where-used + เหตุผล | Prevent | `ERR_WHERE_USED_NOT_ACKNOWLEDGED` |
| VR-20 | ทุก POST | กันกดซ้ำ | Prevent | `ERR_IDEMPOTENCY_MISMATCH` |
| VR-21 | การแสดงจำนวนเงิน | คั่นหลักพัน + 2 ตำแหน่ง · THB | Trigger | — |
| VR-22 | ค่า Restricted | ไม่มีสิทธิ์ → `null` + `masked` | Prevent | — |

### Cross-field
- `calc_type = percent_of` ⇒ `base_component_code` ต้องมี
- `amount` XOR `percent` (รายการประจำ) — ต้องมีอย่างใดอย่างหนึ่งเท่านั้น
- `out_of_range_flag = true` ⇒ `out_of_range_reason` ต้องมี
- `below_legal_min_flag = true` ⇒ `below_legal_min_reason` ต้องมี
- `version_status ≠ 'draft'` ⇒ `effective_date` ต้องมี (P-1′)
- `movement_doc_no` มี ⇒ `change_reason_code` ควรเป็น `promotion` หรือ `annual_review` หรือ `transfer_restructure` (**เตือนอย่างเดียว** ไม่บล็อก)

## §5.5 Edge Cases

### ยืนยันแล้ว (☑ · implement Phase 1)
| EC | เคส | พฤติกรรม |
|---|---|---|
| EC-01 | ไม่มีกระบอกของระดับ ณ วันที่ | `band_position = null` · จอแสดง "—" · **ไม่คำนวณมั่ว** |
| EC-02 | ไม่มี component ติดแฟล็กฐานเทียบ | เตือน + ใช้ `BASE` |
| EC-03 | FTE 0.50 | ฐานเทียบเต็มเวลา = 2 เท่า · แสดงทั้งสองค่า |
| EC-04 | `max = min` | บล็อก (BR-01) |
| EC-05 | เวอร์ชันมีผลตรงเที่ยงคืน | ใช้เวอร์ชันใหม่ตั้งแต่ `effective_date` เป็นต้นไป (inclusive) |
| EC-06 | อัตราใหม่วันมีผลเดียวกับเดิม | บล็อก (BR-11 · EXCLUDE) |
| EC-07 | ถอนเวอร์ชันในวันที่มีผลพอดี | ถอนได้เฉพาะก่อนถึงวัน — หลังจากนั้น `ERR_VERSION_NOT_WITHDRAWABLE` |
| EC-08 | พนักงานลาออกแต่มีอัตรารอมีผล | ถอนอัตรารอมีผลพร้อมเหตุผล · ประวัติคงอยู่ |
| EC-09 | ระดับถูกปิดใช้ระหว่างมีอัตรารอมีผลอ้างอยู่ | อัตรารอมีผลยังอ้างระดับเดิมได้ · รายการใหม่เลือกไม่ได้ |
| EC-10 | component ถูกปิดใช้ระหว่างมีรายการใช้อยู่ | รายการเดิมทำงานถึงวันสิ้นสุด · รายการใหม่เลือกไม่ได้ |
| EC-11 | role เปลี่ยนกลางคัน | ปิดบังทันทีรอบโหลดข้อมูลถัดไป |
| EC-12 | export โดย role ที่ไม่มีสิทธิ์ | ไฟล์มีค่าปิดบัง (ผ่าน `maskMoney` เส้นทางเดียวกัน) |
| EC-13 | ค่าขั้นต่ำยังไม่ถูกตั้งที่ต้นทาง | แสดง "ยังไม่ได้ตั้งค่าขั้นต่ำที่ตั้งค่า HR" · ไม่ตั้งธง · **ไม่เดาตัวเลข** |
| EC-14 | ค่า `ot_rate` ที่อ้างถูก deactivate | แสดงของเดิม + ป้ายปิดใช้ · เลือกใหม่ไม่ได้ |
| EC-15 | ยอดสะสมเกินเป้า | ปิดรายการทันทีที่ถึงเป้า · ส่วนเกินเป็นเรื่องของ Payroll |

### AI-suggested (☐ · BA ยืนยันที่ SOW3.7)
| EC | เคส | ข้อเสนอ | tag |
|---|---|---|---|
| EC-16 | บันทึกอัตราของคนเดียวกันพร้อมกัน | optimistic lock ผ่าน `If-Match` → `409 ERR_STALE_VERSION` | `[AI-DEFAULT]` OQ-BRD-03 |
| EC-17 | ประกาศเวอร์ชันวันเดียวกันพร้อมกัน | คนที่สองชน BR-03 แล้วถูกบล็อก | ☐ |
| EC-18 | ระบบเลื่อนสถานะตอนเที่ยงคืนขณะเปิดหน้าค้าง | โหลดรอบถัดไปได้สถานะใหม่ · ไม่เตือนกลางจอ | ☐ |
| EC-19 | HR Configuration ไม่ตอบสนอง | `503 ERR_HRCFG_UNAVAILABLE` + ปิดปุ่มเฉพาะเส้นทางที่ต้องใช้ค่า · **ห้ามใช้ค่าที่จำไว้ข้ามวัน** | `[AI-DEFAULT]` OQ-FRD-06 |
| EC-20 | พลาด event จากต้นทาง (cache ค้าง) | แสดงเวลาที่ดึงล่าสุด + ปุ่มดึงใหม่ (API-23) | `[AI-DEFAULT]` OQ-BRD-04 |
| EC-21 | พนักงานย้ายแผนกกลางช่วงอัตรา | อัตราไม่เปลี่ยน · แผนกที่แสดงเป็น snapshot | ☐ |
| EC-22 | รหัสระดับซ้ำข้ามขอบเขตบริษัท | อนุญาต · แสดงขอบเขตกำกับในตัวเลือกเสมอ | ☐ |
| EC-23 | component ฐานของสูตร % ถูกปิดใช้ | รายการเดิมคำนวณจากค่าเดิม · เตือนในทะเบียนการใช้งาน | ☐ |
| EC-24 | ปัดเศษหลังปรับ % ทำให้ min = mid | ตรวจ BR-01 ซ้ำหลังปัด แล้วบล็อกถ้าผิด | ☐ |
| EC-25 | ยอดสะสมไม่ตรงกับ Payroll (ยังไม่มี Payroll) | `accrued_amount` อ่านอย่างเดียว/กรอกมือ | `[AI-DRAFT]` OQ-SS-02 |
| EC-26 | หัวหน้าดูคนนอกทีม | ABAC ปฏิเสธ → ค่าปิดบัง + บันทึกความพยายามเข้าถึง | `[AI-DEFAULT]` OQ-BRD-05 |
| EC-27 | ปริมาณ event E10 สูงมาก | ให้ Audit Trail รับแทน (ตัดเฉพาะ E10) | ☐ OQ-CSQ-01 |
| EC-28 | เรียก API ตรงโดยไม่ผ่านหน้าจอ | สิทธิ์ตรวจที่ชั้นบริการ ไม่ใช่ที่หน้าจอ | ☐ |
| EC-29 | Movement ส่งอัตราที่ชนงวดปิด | `422` + ไม่สร้างเรคคอร์ดค้าง · ส่งเหตุผลกลับต้นทาง | ☐ |
| EC-30 | Movement ส่งเลขที่คำสั่งซ้ำ | idempotent — คืนผลเดิม ไม่สร้างซ้ำ | ☐ |
| EC-31 | consumer อ่านวันที่ไม่มีข้อมูล | `rate: null` + `reason: NO_RATE_AT_DATE` · **ไม่คืนค่าใกล้เคียง** | ☐ |
| EC-32 | consumer เก็บค่าโดยไม่เก็บ `version_id` | บังคับที่ฝั่งนี้ไม่ได้ — เป็นข้อกำหนดใน SS-2 + ตรวจตอน integration test (CT-05) | ☐ |

## §5.6 Error Catalog

| Code | HTTP | ข้อความที่ผู้ใช้เห็น (ตรงกับจอ) | เกิดที่ |
|---|---|---|---|
| `ERR_GRADE_CODE_DUPLICATE` | 409 | `รหัสระดับนี้มีอยู่แล้ว` | API-02 |
| `ERR_BAND_ORDER_INVALID` | 422 | `ค่ากระบอกต้องเรียง min < mid < max` (+ ชี้แถว) | API-02/03 |
| `ERR_VERSION_NOT_EDITABLE` | 409 | `กระบอกที่มีผลอยู่แก้ค่าตรงไม่ได้ ต้องสร้างเวอร์ชันใหม่พร้อมวันมีผล` | API-03 |
| `ERR_EFFECTIVE_OVERLAP` | 422 | `ช่วงวันมีผลทับกับเวอร์ชันเดิม` | API-04 |
| `ERR_EFFECTIVE_IN_CLOSED_PERIOD` | 422 | `งวด … ปิดแล้ว ตั้งวันมีผลย้อนเข้างวดนี้ไม่ได้ · ตั้งได้ตั้งแต่ …` | API-04/14/19/26 |
| `ERR_REASON_REQUIRED` | 422 | `กรอกเหตุผลอย่างน้อย 10 ตัวอักษร` | API-04/05/06/15/16/20 |
| `ERR_OUT_OF_RANGE_REASON_REQUIRED` | 422 | `… ของกระบอก บันทึกได้แต่ต้องกรอกเหตุผลนอกกระบอก` | API-14 |
| `ERR_LEGAL_MIN_REASON_REQUIRED` | 422 | `ต่ำกว่าค่าแรงขั้นต่ำตามกฎหมายที่อ่านจากตั้งค่า HR ต้องกรอกเหตุผลก่อนบันทึก` | API-04/14 |
| `ERR_CHANGE_REASON_CODE_REQUIRED` | 422 | `เลือกประเภทการเปลี่ยนก่อนบันทึก` | API-14 |
| `ERR_GRADE_INACTIVE` | 422 | `ระดับนี้ปิดใช้แล้ว เลือกระดับอื่น` | API-14 |
| `ERR_COMPONENT_INACTIVE` | 422 | `องค์ประกอบนี้ปิดใช้แล้ว` | API-19 |
| `ERR_COMPONENT_CYCLE` | 422 | `การอ้างอิงวนกลับมาที่ตัวเอง: …` | API-11 |
| `ERR_PAYROLL_CODE_REQUIRED` | 422 | `กรอกรหัสส่งจ่ายเงิน` | API-11 |
| `ERR_RECURRING_OVERLAP` | 409 | `ช่วงวันทับกับรายการเดิมของพนักงานคนนี้ …` | API-19 |
| `ERR_RATE_OVERLAP` | 409 | `ช่วงอัตราทับกับเรคคอร์ดเดิม` | API-14 |
| `ERR_STALE_VERSION` | 409 | `ข้อมูลถูกแก้ไปแล้ว โหลดใหม่แล้วลองอีกครั้ง` | API-14 |
| `ERR_WHERE_USED_NOT_ACKNOWLEDGED` | 409 | (client ต้องแสดงจำนวนผู้ใช้ก่อน) | API-06/12 |
| `ERR_FTE_OUT_OF_RANGE` | 422 | `สัดส่วนเวลาทำงานต้องอยู่ระหว่าง 0.01 ถึง 1.00` | API-14 |
| `ERR_RESOLVE_DATE_REQUIRED` | 400 | (สำหรับ service) `ต้องระบุวันที่ที่ต้องการทราบอัตรา` | API-24/25 |
| `ERR_IDEMPOTENCY_MISMATCH` | 409 | (สำหรับ service) | ทุก POST |
| `ERR_HRCFG_UNAVAILABLE` | 503 | `ยังไม่ได้ค่าจากตั้งค่า HR — ลองใหม่อีกครั้ง` | ทุกเส้นทางที่ต้องใช้ค่านโยบาย |
| `ERR_FIELD_NOT_SUPPORTED` | 400 | (สำหรับ service) `ฟิลด์นี้ไม่อยู่ในขอบเขตของโครงเงินเดือน` | API-11/14 |
| `ERR_FORBIDDEN` | 403 | `บทบาทนี้ดูได้อย่างเดียว ไม่สามารถแก้ไขโครงเงินเดือนได้` | ทุก mutation |

## §5.7 Security Bible Application

### D2 · Authentication & Session
ทุก endpoint ต้องมี token ที่ผ่าน · role มาจาก login เท่านั้น — **ตัวสลับบทบาทบนจอเป็น demo ใน `.demo-strip` ไม่มีผลต่อสิทธิ์จริง** (FN-37) · การเรียก API ตรงโดยไม่ผ่านหน้าจอต้องถูกตรวจสิทธิ์เหมือนกัน (EC-28)

### D7 · PII Protection
`base_amount` · `amount`/`percent` · `goal_amount` · `accrued_amount` · `total_fixed_monthly` · `compa_ratio` (ผูกบุคคล) = **Restricted** → ปิดบังที่ชั้น API · เข้ารหัสตอนเก็บ · ห้ามลง log/trace · ชื่อพนักงานเป็น PII แต่ไม่ปิดบัง (จำเป็นต่อการใช้งาน)

### D-CLASS · Data Classification ⭐
| ระดับ | field ตัวอย่าง | การบังคับ |
|---|---|---|
| Restricted | จำนวนเงินที่ผูกบุคคล + ตัวชี้วัดที่คำนวณจากมัน | mask ที่ API · encrypt at rest · audit ทุกการอ่าน · ห้าม export ดิบ |
| Confidential | min/mid/max · เหตุผล · ธงนอกกระบอก · `movement_doc_no` | เห็นได้เฉพาะผู้มีสิทธิ์เข้าถึง feature |
| Internal | รหัส/ชื่อ/สถานะ/วันที่/ทะเบียนการใช้งาน | เห็นได้ทุก role ที่เข้าถึง feature |
| Public | **ไม่มี** | — |
> ตรวจตอน code review: **ไม่มี field ใดถูกตั้งเป็น Public** · ทุกคอลัมน์ใน `04_DB §4.2` มี Classification + PII flag ครบ

### D9 · Audit Logging
บันทึกทุก create/publish/withdraw/deactivate/reactivate/end + **ทุกการอ่าน detail ของข้อมูล Restricted** · เนื้อหา audit = ใคร · อะไร · เมื่อไร · ที่ไหน · ผล · (สำหรับการอ่าน) ดูของใคร · เก็บที่ **Policy Center** ไม่เก็บเอง · append-only

### D15 · Admin Actions
ปิดใช้/เปิดใช้ระดับ · ปรับ Module Linkage เอง (`manual_override`) → บันทึกผู้ทำ + เวลา + เหตุผล

### D17 · Multi-Tenant Isolation
`tenant_id` ทุกตาราง · ทุก query · ทุก index นำหน้าด้วย `tenant_id` · ห้ามมี endpoint ที่ข้าม tenant

### (ไม่ใช้) D5 · Financial Transactions
feature นี้ **ไม่มีการเคลื่อนไหวเงินจริง** — ไม่มีการตั้งหนี้/จ่าย/ลงบัญชี (เกิดที่ Payroll) จึงไม่บังคับ control ชุด D5 · **แต่ยัง**ยิงท่อ EC ของ 7C เพราะกระทบต้นทุนค่าจ้างคงที่

## §5.8 Compliance & Audit Requirements

| ข้อกำหนด | วิธีพิสูจน์ |
|---|---|
| กฎหมายแรงงาน — ค่าจ้างไม่ต่ำกว่าขั้นต่ำ | รายงาน "ต่ำกว่าขั้นต่ำตามกฎหมาย" ต้องว่างเสมอ หรือทุกแถวมีเหตุผลบันทึกไว้ (BR-23) |
| PDPA | Restricted resource ลงทะเบียนที่ Policy Center · ทุกการเข้าถึงมี audit (OQ-FRD-05) |
| ตรวจสอบย้อนหลัง | ประวัติอัตรา append-only + `version_id` ของค่านโยบายที่ใช้ตัดสิน |
| SoD | Maker (HR Comp Admin) ≠ Checker (HR Manager) · **การอนุมัติอยู่คนละ feature** (Employee Movement) |
| ไม่มี hardcode ค่ากฎหมาย | ตรวจอัตโนมัติทุก release: ไม่มีค่าคงที่เชิงเงินในซอร์สของ feature (KPI-04 · P-8′) |
