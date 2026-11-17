# MDOC_BRIEF — CSM หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `CSM` |
| ชื่อ | หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade · General Trade Customer Satisfaction Summary (Monthly) |
| หมวด / หน้าที่ | RPT รายงานและการประเมิน · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | SAL · F-TMP-002 |
| หน้าเอกสาร | `#/sales/csat-gt-summary` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-SAL-11 Rev.00 (01/07/2569) |
| แบบพิมพ์ | FM-SAL-11 หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (2 หน้า) |
| การอนุมัติ (DOA) | รอเชื่อม |
| ประกาศ (ค่าเริ่ม) | ไม่ตั้ง (ลูกค้าตั้งเองที่ F185) |


## ผลตรวจ
| กฎ | ระดับ | รายละเอียด |
|---|---|---|
| G04 | WARN | ยังไม่มี taxonomy_def_id — จะเข้าคิว definition ใหม่รออนุมัติ |
| G09 | WARN | doa = pending — ต้องมี DOA_BRIEF และตามปิดก่อนลูกค้าเปิดใช้ |

## Events หลัง register
| Event | ผล |
|---|---|
| `doctype.registered / doctype.version_ready` | F185: แบบใหม่ = `ready` (รอเปิดใช้งาน) · เวอร์ชันใหม่ของแบบเดิม = `update` (มีเวอร์ชันใหม่) |

## Payload
```yaml
doc_type: CSM
name_th: หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade
name_en: General Trade Customer Satisfaction Summary (Monthly)
class_code: RPT
function_code: F01
taxonomy_def_id: null
module: SAL
feature_id: F-TMP-002
route_path: '#/sales/csat-gt-summary'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-SAL-11 Rev.00 (01/07/2569)
prints:
- FM-SAL-11 หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (2 หน้า)
doa: pending
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('CSM', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
