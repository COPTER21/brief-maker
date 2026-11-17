# MDOC_BRIEF — FEC ใบตรวจเช็คถังดับเพลิง

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `FEC` |
| ชื่อ | ใบตรวจเช็คถังดับเพลิง · Fire Extinguisher Inspection Card |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | Inventory / Warehouse · F-TMP-001 |
| หน้าเอกสาร | `#/fire-extinguisher-check` |
| เจ้าของแบบ | แผนกคลังสินค้า · role-mgr-wh |
| เวอร์ชัน | v1 — เวอร์ชันแรก (function_code F01 = ค่าชั่วคราว รอยืนยัน Taxonomy) |
| แบบพิมพ์ | FM-WHS-03 ใบตรวจเช็คถังดับเพลิง |
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
doc_type: FEC
name_th: ใบตรวจเช็คถังดับเพลิง
name_en: Fire Extinguisher Inspection Card
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: Inventory / Warehouse
feature_id: F-TMP-001
route_path: '#/fire-extinguisher-check'
owner:
  unit: แผนกคลังสินค้า
  role: role-mgr-wh
version: v1
change_note: เวอร์ชันแรก (function_code F01 = ค่าชั่วคราว รอยืนยัน Taxonomy)
prints:
- FM-WHS-03 ใบตรวจเช็คถังดับเพลิง
doa: none
request_no: null
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('FEC', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
