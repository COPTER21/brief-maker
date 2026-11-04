# MDOC_BRIEF — ACL ใบเคลียร์เงินทดรองจ่าย

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `request` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `ACL` |
| ชื่อ | ใบเคลียร์เงินทดรองจ่าย · Advance Clearing |
| หมวด / หน้าที่ | TXN เอกสารธุรกรรม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | Finance · F-FIN-ACL |
| หน้าเอกสาร | `#/advance-clearing` |
| เจ้าของแบบ | ฝ่ายการเงิน · role-finance-manager |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-FIN-02 ใบเคลียร์เงินทดรองจ่าย |
| การอนุมัติ (DOA) | รอเชื่อม |
| ประกาศ (ค่าเริ่ม) | ไม่ตั้ง (ลูกค้าตั้งเองที่ F185) |
| คำขอ | REQ-2569-0000 |

## ผลตรวจ
| กฎ | ระดับ | รายละเอียด |
|---|---|---|
| G01 | INFO | ไม่ได้ให้รายการ F-DOCCFG — ตรวจรูปแบบอย่างเดียว (ต้องเช็คว่ามี code ใน F-DOCCFG ก่อน register) |
| G04 | WARN | ยังไม่มี taxonomy_def_id — จะเข้าคิว definition ใหม่รออนุมัติ |
| G09 | WARN | doa = pending — ต้องมี DOA_BRIEF และตามปิดก่อนลูกค้าเปิดใช้ |

## Events หลัง register
| Event | ผล |
|---|---|
| `doctype.registered / doctype.version_ready` | F185: แบบใหม่ = `ready` (รอเปิดใช้งาน) · เวอร์ชันใหม่ของแบบเดิม = `update` (มีเวอร์ชันใหม่) |
| `doctype.registered → F186` | คำขอ REQ-2569-0000 → `deployed` (พร้อมเปิดใช้) |

## Payload
```yaml
doc_type: ACL
name_th: ใบเคลียร์เงินทดรองจ่าย
name_en: Advance Clearing
class_code: TXN
function_code: F01
taxonomy_def_id: null
module: Finance
feature_id: F-FIN-ACL
route_path: '#/advance-clearing'
owner:
  unit: ฝ่ายการเงิน
  role: role-finance-manager
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-FIN-02 ใบเคลียร์เงินทดรองจ่าย
doa: pending
request_no: REQ-2569-0000
announcement_default: {}
source: request
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('ACL', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
