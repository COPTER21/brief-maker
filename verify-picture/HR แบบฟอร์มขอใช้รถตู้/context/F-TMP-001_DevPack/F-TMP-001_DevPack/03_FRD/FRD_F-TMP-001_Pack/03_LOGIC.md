# 03_LOGIC — F-TMP-001 แบบฟอร์มขอใช้รถตู้

## 1. State machine
```
(ใหม่) ──FN-04──> draft ──FN-06──> pending ──FN-07(ขั้นสุดท้าย)──> approved
                   ^  │                │
          FN-08 ───┘  └──FN-09──> cancelled <──FN-09── (จาก pending)
          (ไม่อนุมัติ = กลับเป็นร่างเลขเดิม)
```

---

### FN-01 — เติมข้อมูลผู้ขอจากระบบ (snapshot)
**เมื่อ:** เปิดหน้าสร้าง และตอนบันทึก (A3/A4)
**ทำ:** อ่าน `Employee.full_name` · `Employee.code` · `Employee.position` (F-EMP-001) และ `OrgUnit` ฝ่าย/แผนก (F-ORG-001) ของผู้ใช้ที่ login
แล้ว snapshot ลง `requester_name` · `requester_code` · `requester_position` · `requester_division` · `requester_department`
**หมายเหตุ:** ค่าเหล่านี้ไม่รับจาก client · เปลี่ยนตำแหน่งภายหลังไม่กระทบใบเดิม

### FN-02 — คำนวณจำนวนวัน
**เมื่อ:** `use_date_from` หรือ `use_date_to` เปลี่ยน (ฝั่งจอ) และทุกครั้งก่อนบันทึก (ฝั่ง server)
**ทำ:** `total_days = (use_date_to − use_date_from) + 1` นับรวมวันเริ่มและวันสิ้นสุด
**บล็อก:** ถ้า `use_date_to < use_date_from` → `VALIDATION_FAILED` ("ถึงวันที่ต้องไม่ก่อนวันที่เริ่ม")
**เตือน:** `total_days > 30` → เตือนให้ผู้พิจารณาตรวจก่อนอนุมัติ (ไม่บล็อก)

### FN-03 — บังคับความสอดคล้องของลักษณะการเดินทาง
**เมื่อ:** บันทึกร่าง และก่อนส่งอนุมัติ
**ทำ:**
| `trip_mode` | บล็อกที่บังคับกรอกครบ 4 ช่อง | บล็อกที่ถูกล้างเป็นค่าว่าง |
|---|---|---|
| `outbound_only` | ขาไป | ขากลับ |
| `return_only` | ขากลับ | ขาไป |
| `round_trip` | ทั้งขาไปและขากลับ | — |
**เตือน:** เวลาส่ง < เวลารับ ในเที่ยวเดียวกัน → เตือน ไม่บล็อก

### FN-04 — บันทึกร่างและออกเลขที่เอกสาร
**เมื่อ:** `POST /api/hr/van-requests` ครั้งแรก
**ทำ:**
1. เรียก **F-DOCCFG** เช็คสถานะเปิดใช้ของ doc_type `VAN` — ยังไม่เปิดใช้ → `DOCTYPE_INACTIVE` (ห้ามออกเลข)
2. ตรวจ validation (ดู 05_RULES §2)
3. เรียก **ENG-DOC-NUM** `next('VAN')` → ได้ `doc_no` รูปแบบ `VAN-{พ.ศ.}-{run:4}` · reset รายปี · ไม่ต้อง no-gap
4. snapshot หัวกระดาษจาก Organization ลง `header_snapshot` (`organization_snapshot_at_numbering`)
5. สถานะ `draft` · `approval_status = draft` · เขียนประวัติ "สร้างเอกสาร"

### FN-05 — แก้ไขร่าง
**เมื่อ:** `PUT …/{id}` · อนุญาตเฉพาะเจ้าของและสถานะ `draft` (ไม่ใช่ → `NOT_OWNER` / `INVALID_STATE`)
**ทำ:** อัปเดตช่อง · เรียก FN-02 + FN-03 ซ้ำ · **ไม่ออกเลขใหม่** · เขียนประวัติ "แก้ไขร่าง"

### FN-06 — ส่งอนุมัติ (resolve + freeze สายอนุมัติ)
**เมื่อ:** `POST …/{id}/submit`
**ทำ:**
1. ตรวจสถานะต้องเป็น `draft` (BR-DOA-01) และผู้เรียกเป็นเจ้าของ
2. `// TODO: DOA engine` — เรียก `GET /doa/resolve` ด้วย `doa_entry_ref = DOA-VAN-01` + ผู้ขอ → ได้รายการขั้น (จำนวนขั้นและ role ตามที่ตั้งที่ DOA กลาง **ห้าม hardcode**)
3. รับ `assignees[]` ที่ผู้ขอเลือกต่อขั้น — ต้องครบทุกขั้น และต้องไม่ใช่ผู้ขอเอง (BR-DOA-04 → `SELF_APPROVAL_DENIED`)
4. **freeze** ลง `approval_chain` (BR-DOA-02) · ขั้น 1 = `pending` · ขั้นที่เหลือ = `waiting`
5. สถานะ `pending` · `approval_status = pending_approval` · `approver_role` = role ของขั้นปัจจุบัน · `submitted_at = now`
6. DOA engine ยิง `doa_pending` เอง — **feature ไม่ยิงซ้ำ**

### FN-07 — อนุมัติขั้นปัจจุบัน
**เมื่อ:** `POST …/{id}/approve`
**ทำ:**
1. ผู้เรียกต้องเป็น `assignee_id` ของขั้นที่ `decision = pending` (ไม่ใช่ → `NOT_CURRENT_APPROVER`)
2. ขั้นนั้น `decision = approved` · `decided_at = now` · เก็บความเห็น
3. มีขั้นถัดไป → ขั้นถัดไป `pending` · `approver_role` เปลี่ยนตาม · สถานะคงเป็น `pending`
4. ไม่มีขั้นถัดไป → สถานะ `approved` · `approval_status = approved` · `approved_by` · `approved_at`
   แล้วเรียก **ENG-DOC-STORE** เก็บ snapshot PDF ของใบ
5. คำที่บันทึกในประวัติใช้คำตัดสินของ **role** นั้น (`อนุมัติ` สำหรับ `role-line-manager` · `เห็นควร` สำหรับ `role-mgr-hr`)

### FN-08 — ไม่อนุมัติ (กลับเป็นร่างเลขเดิม)
**เมื่อ:** `POST …/{id}/reject` · `reason` บังคับ (ว่าง → `REASON_REQUIRED`)
**ทำ:**
1. ขั้นปัจจุบัน `decision = rejected` · `reject_reason = reason` · `decided_at = now`
2. เขียนประวัติด้วยคำตัดสินของ role (`ไม่อนุมัติ` / `ไม่เห็นควร`)
3. **คืนใบเป็นร่าง:** สถานะ `draft` · `approval_status = draft` · `submitted_at = null` · `approved_by/at = null`
   **เลขที่เอกสารคงเดิม** · `approval_chain` รอบที่ถูกปฏิเสธถูกเก็บไว้แบบ append-only แล้ว resolve ใหม่ตอนส่งรอบถัดไป
4. DOA engine ยิง `doa_result` เอง — feature ไม่ยิงซ้ำ

### FN-09 — ยกเลิกเอกสาร
**เมื่อ:** `POST …/{id}/cancel` · `reason` บังคับ
**ทำ:**
1. อนุญาตเฉพาะสถานะ `draft` หรือ `pending` และผู้เรียกเป็นเจ้าของหรือ admin role (`role-mgr-hr`) — ไม่ใช่ → `INVALID_STATE` / `NOT_OWNER`
2. สถานะ `cancelled` · `cancel_reason` · `cancelled_at` · ขั้นที่ยังไม่ตัดสิน → `skipped`
3. ถ้าเดิมเป็น `pending` → ยิง **`van_cancelled`** ผ่าน `ENG-NOTIFY.emit('van_cancelled', { ref: doc_no, vars: { actor, reason } })` ถึงผู้พิจารณาขั้นปัจจุบัน

### FN-10 — การมองเห็น (query filter)
**เมื่อ:** ทุก endpoint ที่อ่านใบ
**ทำ:** คืนเฉพาะใบที่ `is_admin_role OR requester_id = me OR (status <> 'draft' AND me ∈ approval_chain[].assignee_id)`
ใบที่ไม่เข้าเงื่อนไข → `NOT_FOUND` (ไม่เปิดเผยว่ามีใบอยู่)

### FN-11 — แบบพิมพ์ PDF
**เมื่อ:** `GET …/{id}/pdf` และแท็บ PDF Preview
**ทำ:** สร้าง data ตาม `VAN_data-contract.md` แล้ว render `form.tpl.html` (logic-less) ฝั่ง server
- รายชื่อผู้เดินทางเติมแถวว่างจนครบ `print_config.min_rows` (5)
- ช่องลงชื่อ = ผู้ขอ + 1 ช่องต่อขั้นใน `approval_chain` · แบ่งแถวละ ≤ `sign_layout.max_per_row` (4)
- คำตัดสินต่อช่องอ่านจาก `print_config.decision_words.by_role[role_id]` (ไม่ผูกลำดับขั้น)
- `header_snapshot` ใช้เป็นหัวกระดาษ (ไม่ดึงสดหลังออกเลข)

### FN-12 — ส่งออก CSV
**เมื่อ:** `GET …/export` · ใช้ตัวกรองและสิทธิ์เดียวกับ FN-10
**ทำ:** คืนไฟล์ UTF-8 BOM หัวคอลัมน์ภาษาไทย: เลขที่ · วันที่ขอ · ผู้ขอ · ฝ่าย · ตั้งแต่วันที่ · ถึงวันที่ · จำนวนวัน · ลักษณะการเดินทาง · วัตถุประสงค์ · จำนวนผู้เดินทาง · สถานะ

---

## 2. สิ่งที่ feature **ไม่** ทำ
- ไม่เขียนค่าตั้งค่าใด ๆ ในระบบเมื่ออนุมัติ (DEC-01)
- ไม่ส่งข้อมูลต่อระบบเวลาทำงาน / เบิกจ่าย / เงินเดือน (DEC-02)
- ไม่ตรวจว่ารถตู้ว่างหรือชนกับใบอื่น (BRD §15 OQ-02)
- ไม่ประกาศ `doa_pending` / `doa_result` / `doa_escalate` ซ้ำ
