# MDOC_BRIEF — SES แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `SES` |
| ชื่อ | แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ · Sale Admin Satisfaction Summary (Overseas Customer) |
| หมวด / หน้าที่ | RPT รายงานและการประเมิน · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | Sales · F-TMP-007 |
| หน้าเอกสาร | `#/sales-admin-csat-overseas-summary` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-SAL-23 Rev.00 (01/07/2569) |
| แบบพิมพ์ | FM-SAL-23 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ (2 หน้า) |
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
doc_type: SES
name_th: แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ
name_en: Sale Admin Satisfaction Summary (Overseas Customer)
class_code: RPT
function_code: F01
taxonomy_def_id: null
module: Sales
feature_id: F-TMP-007
route_path: '#/sales-admin-csat-overseas-summary'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-SAL-23 Rev.00 (01/07/2569)
prints:
- FM-SAL-23 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ (2
  หน้า)
doa: pending
request_no: null
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('SES', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
