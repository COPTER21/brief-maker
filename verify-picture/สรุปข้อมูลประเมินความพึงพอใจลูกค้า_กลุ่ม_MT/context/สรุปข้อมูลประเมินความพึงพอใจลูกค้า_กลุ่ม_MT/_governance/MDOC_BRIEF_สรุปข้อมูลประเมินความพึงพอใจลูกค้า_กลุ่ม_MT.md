# MDOC_BRIEF — MTS สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `MTS` |
| ชื่อ | สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT · MT Customer Satisfaction Summary (per round) |
| หมวด / หน้าที่ | RPT รายงานและการประเมิน · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | SAL · F-TMP-008 |
| หน้าเอกสาร | `#/sales/csat-mt-summary` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-SAL-07 Rev.00 (01/07/2569) |
| แบบพิมพ์ | FM-SAL-07 สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (2 หน้า) |
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
doc_type: MTS
name_th: สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT
name_en: MT Customer Satisfaction Summary (per round)
class_code: RPT
function_code: F01
taxonomy_def_id: null
module: SAL
feature_id: F-TMP-008
route_path: '#/sales/csat-mt-summary'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-SAL-07 Rev.00 (01/07/2569)
prints:
- FM-SAL-07 สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (2 หน้า)
doa: none
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('MTS', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
