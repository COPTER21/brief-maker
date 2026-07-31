# 06_TESTS — F-PRODUCT-MASTER-001 Product Master

> **Audience:** QA · Coverage: 02_API + 03_LOGIC + 05_RULES · Expected text = **verbatim จากจอจริง** (§6.10)
> Prototype E2E ปัจจุบัน: Playwright 46/46 PASS (อ้างเป็น baseline พฤติกรรมจอ)

---

## §6.1 Acceptance Criteria

### AC-01 List + filter + sort
**Given** tenant มีสินค้าหลายสถานะ **When** GET /products?status=active **Then** 200 เฉพาะ active · stats ตรง (`inactive` = obsolete+discontinued) · sort ทำงานทุกคอลัมน์ sortable
### AC-02 Empty state 2 เคส
ไม่มีข้อมูล → "ยังไม่มีสินค้าในทะเบียน" + ปุ่มเพิ่มสินค้า · filter ไม่เจอ → "ไม่พบสินค้าตามเงื่อนไข" + ปุ่ม `ล้างตัวกรอง` (กดแล้ว filter reset + toast `ล้างตัวกรองแล้ว`)
### AC-03 Create draft
wizard ผ่าน step gates → `บันทึกแบบร่าง` → 201 status=draft · code = `{TYPE}-{running}` · audit `สร้างรายการ (v1)` · toast `บันทึกร่างแล้ว`
### AC-04 Create + activate (happy)
กรอกครบ (cost>0, price, posting group) → `บันทึกและเปิดใช้งาน` → ปุ่มเข้า loading `กำลังบันทึก…` → active · audit +`เปิดใช้งาน` · toast `บันทึกและเปิดใช้งานแล้ว`
### AC-05 Activate gate (NOT_READY)
draft ไม่มี posting group (stocked) → เปิดใช้งาน → 422 BR_NOT_READY · จอ: toast `ข้อมูลไม่พร้อมใช้งาน: Posting Group (NOT_READY)` (wizard: เด้ง step 3)
### AC-06 Amend active (ปุ่ม "บันทึก")
edit active แก้ชื่อ → submit label = `บันทึก` → 200 version+1 · **สถานะคง active** · toast `บันทึกการแก้ไขแล้ว` · audit `แก้ไข (vN)`
### AC-07 Edit guard
PUT ที่ archived/discontinued → 422 BR_INVALID_STATE · จอ: hash edit → เด้ง view
### AC-08 UOM rules
เพิ่มหน่วยแปลงข้ามหมวด → block toast คนละหมวด · factor 0 → block ≥1 · ซ้ำ base → block (VR-04)
### AC-09 IR-02 lock
record `has_txn` → step 2 disabled ทั้งชุด + `สูตรหน่วยแปลงถูกล็อก — มี transaction แล้ว (IR-02)` · API PUT แตะ uom → 422 BR_UOM_LOCKED
### AC-10 VR-MM
min 50 / max 10 → step3 block toast `สต็อกสูงสุด (Max) ต้องไม่ต่ำกว่าขั้นต่ำ (Min) — MINMAX_INVALID` · แก้ max 500 → ผ่าน · view แสดง `— ไม่เตือน` เมื่อ null
### AC-11 Pricing gate
role นอก canSeePricing → list header `— จำกัด —` + cell `•••` + tab ราคา empty "ข้อมูลจำกัด (Confidential)" · **API payload ไม่มี pricing fields**
### AC-12 เลิกผลิต
active → modal เลิกผลิต → confirm → pill `เลิกผลิต` · toast `เปลี่ยนสถานะเป็น เลิกผลิต แล้ว` · header actions เปลี่ยนเป็น แก้ไข/ใช้งานอีกครั้ง/ยกเลิกถาวร
### AC-13 Reactivate
obsolete (ข้อมูลครบ) → `ใช้งานอีกครั้ง` → pill `ใช้งาน` · toast `สินค้ากลับมาสถานะ ใช้งาน แล้ว` · ข้อมูลไม่ครบ → BR_NOT_READY (EC-08)
### AC-14 ยกเลิกถาวร
obsolete → modal → confirm → pill `ยกเลิก` · เหลือ action จัดเก็บเท่านั้น
### AC-15 จัดเก็บ (soft)
active/discontinued → modal (has_txn → warning BR-002) → confirm → archived · toast `จัดเก็บสินค้าแล้ว (soft delete)` · record ไม่หาย (soft) · archived ไม่มี action
### AC-16 Bulk preview validate
เลือกไฟล์ (5 แถว mock) → preview 5 แถว: 3 ✓ `พร้อมนำเข้า` + `CODE_DUPLICATE` 1 + `MINMAX_INVALID` 1 · ปุ่ม `นำเข้า 3 แถว`
### AC-17 Bulk partial import
confirm → summary `นำเข้าเสร็จ — สร้างร่าง 3 แถว · ข้าม 2 แถว (IMPORT_ERROR)` + ตารางสาเหตุ · RAW +3 (draft) · toast `นำเข้าแล้ว 3 แถว · ข้าม 2 แถว (IMPORT_ERROR)`
### AC-18 Audit & version
ทุก mutation ปรากฏใน tab ประวัติ เรียงเวลา + dot สีตาม variant · footer `version N · สร้าง <วันที่>`
### AC-19 Routing/Esc/context
Esc: modal→drawer→list · modal จาก view: ยกเลิก/ยืนยัน → กลับ view เดิม **คง tab** · refresh ที่ทุก hash → state เดิม
### AC-20 Concurrency + idempotency `[AI-DEFAULT]`
PUT ซ้อน → คนหลัง 409 ERR_STALE_DATA · POST retry key เดิม → response cached ไม่ INSERT ซ้ำ

---

## §6.2 Test Case Inventory

| TC | Name | Type | AC | Pri |
|---|---|---|---|---|
| TC-01..02 | list/filter/sort/paginate + empty 2 เคส | UI+API | AC-01/02 | P0 |
| TC-03..04 | create draft / create+activate | E2E | AC-03/04 | P0 |
| TC-05 | NOT_READY gate | negative | AC-05 | P0 |
| TC-06..07 | amend active / edit guard | E2E | AC-06/07 | P0 |
| TC-08..09 | UOM VR + IR-02 lock | negative | AC-08/09 | P0 |
| TC-10 | VR-MM block + null=ไม่เตือน | negative | AC-10 | P0 |
| TC-11 | pricing role gate (2 roles) | security | AC-11 | P0 |
| TC-12..15 | transitions ครบ loop + INVALID_STATE guards | E2E | AC-12..15 | P0 |
| TC-BK-01..02 | bulk preview / partial import | E2E | AC-16/17 | P0 |
| TC-18 | audit+version | E2E | AC-18 | P1 |
| TC-19 | routing/Esc/context/tab preserve | E2E | AC-19 | P1 |
| TC-CC-01 / TC-ID-01 / TC-RC-01 | stale / idempotent / genCode race | API | AC-20, EC-06 | P1 |
| TC-GD-01 | hash-hack guards | E2E | EC-03 | P2 |
| TC-TY-01 | เปลี่ยน type regen code | UI | EC-04 | P2 |

## §6.3 Test Data
- 2 tenants · seed 13+ products ครบ 5 สถานะ + `has_txn=true` อย่างน้อย 1 (FG-1001 pattern) + draft ที่ไม่มี posting group (FG-1010 pattern — ใช้ทดสอบ AC-05/13)
- Roles: qa_clerk (master_data_clerk), qa_pm (product_manager), qa_finance, qa_viewer (no pricing)

## §6.4 Definition of Done
- [ ] AC-01..20 ผ่าน + unit ≥80% บน logic layer (FN-01..12)
- [ ] Negative ทุก BR_* code ตอบ HTTP ตรงตาราง 05 §5.6
- [ ] Pricing exclusion ตรวจที่ **payload** ไม่ใช่แค่จอ
- [ ] Migration v3.5→2.0 ทดสอบ (pending→draft, drop 4CODE cols)
- [ ] `[AI-DEFAULT]` rules (OQ-07) ได้รับ confirm ก่อนปิด
- [ ] Cross-module XT-01..03 ผ่าน

## §6.5 WebSocket Events — ไม่มีใน scope · `product_threshold_changed_event` = server-side event bus (ดู 02 §2.X)

## §6.6 Performance
| Endpoint | P95 |
|---|---|
| GET /products (list) | < 500ms |
| GET /products/:id | < 200ms |
| POST /products | < 800ms |
| POST /bulk-import (100 แถว) | < 3s |

## §6.8 Trace: AC → Logic
| AC | API | Functions |
|---|---|---|
| 01/02 | API-01 | FN-01 |
| 03/04 | API-03 | FN-02, FN-09, FN-10 (+FN-06/07/08) |
| 05 | API-05 | FN-04→FN-06 |
| 06/07 | API-04 | FN-03 |
| 08/09 | API-03/04 | FN-08 |
| 10 | API-03/04/05 | FN-07 |
| 12..15 | API-06 | FN-05 (+FN-06) |
| 16/17 | API-07 | FN-12→FN-11 |
| 20 | API-03/04 | (middleware) + FN-09 race |
> FN ทุกตัวถูก trace ≥1 AC ✅

## §6.9 Cross-Module Test Cases ⭐
| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | set/แก้ min-max แล้ว activate/amend | Inventory Monitoring | ได้ `product_threshold_changed_event` payload `{product_id,min,max,uom_base}` ครบ · null side ไม่ trigger เตือนด้านนั้น |
| XT-02 | product → obsolete/discontinued | Sales/Purchase picker + BOM | picker ไม่แสดง (status≠active) · BOM add component ที่ไม่ active → gate fail |
| XT-03 | archive product ที่มี transaction | เอกสารเก่า | FK ยังอ้างได้ (soft) — ไม่มี orphan/ลบจริง |

## §6.10 Microcopy-Aware Expected Text (verbatim จากจอ)
ปุ่ม: `เพิ่มสินค้า` `นำเข้าจำนวนมาก` `ถัดไป` `ย้อนกลับ` `ยกเลิก` `บันทึกแบบร่าง` `บันทึกและเปิดใช้งาน` `บันทึก` `แก้ไข` `เปิดใช้งาน` `เลิกผลิต` `ใช้งานอีกครั้ง` `ยกเลิกถาวร` `จัดเก็บ` `ปิด` `ล้างตัวกรอง` · loading: `กำลังบันทึก…`
Toast: `บันทึกร่างแล้ว` `บันทึกการแก้ไขแล้ว` `บันทึกและเปิดใช้งานแล้ว` `เปิดใช้งานแล้ว` `เปลี่ยนสถานะเป็น เลิกผลิต แล้ว` `เปลี่ยนสถานะเป็น ยกเลิก แล้ว` `สินค้ากลับมาสถานะ ใช้งาน แล้ว` `จัดเก็บสินค้าแล้ว (soft delete)` `ล้างตัวกรองแล้ว` `ตั้งเป็นรูปปกแล้ว` `นำเข้าแล้ว N แถว · ข้าม M แถว (IMPORT_ERROR)` `ศูนย์แจ้งเตือนจะเชื่อมกับ Notification Center (F-NT) ภายหลัง`
สถานะ (pill): `ร่าง` `ใช้งาน` `เลิกผลิต` `ยกเลิก` `จัดเก็บ` · Empty: `ยังไม่มีสินค้าในทะเบียน` / `ไม่พบสินค้าตามเงื่อนไข` / `ข้อมูลจำกัด (Confidential)` / `ยังไม่มีเอกสารแนบ`
