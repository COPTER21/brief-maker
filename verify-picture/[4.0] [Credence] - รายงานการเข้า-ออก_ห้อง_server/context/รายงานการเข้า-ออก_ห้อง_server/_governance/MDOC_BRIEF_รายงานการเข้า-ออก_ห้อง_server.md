# MDOC_BRIEF — SRAL รายงานการเข้า-ออก ห้อง server

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `SRAL` |
| ชื่อ | รายงานการเข้า-ออก ห้อง server · Server Room Access Log |
| หมวด / หน้าที่ | REC หลักฐานและบันทึก · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | IT Support · F-TMP-006 |
| หน้าเอกสาร | `#/it/server-room-access` |
| เจ้าของแบบ | ฝ่ายเทคโนโลยีสารสนเทศ · admin_role (เจ้าหน้าที่/ผู้ดูแลห้อง server ฝ่าย IT — ยังไม่มี role ใน DOA contract) |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-ITS-09 รายงานการเข้า-ออก ห้อง server |
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
doc_type: SRAL
name_th: รายงานการเข้า-ออก ห้อง server
name_en: Server Room Access Log
class_code: REC
function_code: F01
taxonomy_def_id: null
module: IT Support
feature_id: F-TMP-006
route_path: '#/it/server-room-access'
owner:
  unit: ฝ่ายเทคโนโลยีสารสนเทศ
  role: admin_role (เจ้าหน้าที่/ผู้ดูแลห้อง server ฝ่าย IT — ยังไม่มี role ใน DOA
    contract)
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-ITS-09 รายงานการเข้า-ออก ห้อง server
doa: none
request_no: null
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('SRAL', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
