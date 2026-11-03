# MDOC_BRIEF — CSE แบบประเมินความพึงพอใจลูกค้า

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `CSE` |
| ชื่อ | แบบประเมินความพึงพอใจลูกค้า · Customer Satisfaction Evaluation |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | Sales · F-TMP-001 |
| หน้าเอกสาร | `#/customer-satisfaction` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก — จากแบบฟอร์มลูกค้า FM-SAL-06 Rev.00 (คำขอชั่วคราว REQ-TMP-001 · เปลี่ยน source เป็น request เมื่อได้เลขคำขอจริง) · function_code F01 รอ librarian ยืนยัน taxonomy |
| แบบพิมพ์ | FM-SAL-06 แบบฟอร์มประเมินความพึงพอใจ |
| การอนุมัติ (DOA) | ไม่ใช้สายอนุมัติ |
| ประกาศ (ค่าเริ่ม) | ไม่ตั้ง (ลูกค้าตั้งเองที่ F185) |


## ผลตรวจ
| กฎ | ระดับ | รายละเอียด |
|---|---|---|
| G04 | WARN | ยังไม่มี taxonomy_def_id — จะเข้าคิว definition ใหม่รออนุมัติ |

## Events หลัง register
| Event | ผล |
|---|---|
| `doctype.registered / doctype.version_ready` | F185: แบบใหม่ = `ready` (รอเปิดใช้งาน) · เวอร์ชันใหม่ของแบบเดิม = `update` (มีเวอร์ชันใหม่) |

## Payload
```yaml
doc_type: CSE
name_th: แบบประเมินความพึงพอใจลูกค้า
name_en: Customer Satisfaction Evaluation
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: Sales
feature_id: F-TMP-001
route_path: '#/customer-satisfaction'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก — จากแบบฟอร์มลูกค้า FM-SAL-06 Rev.00 (คำขอชั่วคราว REQ-TMP-001
  · เปลี่ยน source เป็น request เมื่อได้เลขคำขอจริง) · function_code F01 รอ librarian
  ยืนยัน taxonomy
prints:
- FM-SAL-06 แบบฟอร์มประเมินความพึงพอใจ
doa: none
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('CSE', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
