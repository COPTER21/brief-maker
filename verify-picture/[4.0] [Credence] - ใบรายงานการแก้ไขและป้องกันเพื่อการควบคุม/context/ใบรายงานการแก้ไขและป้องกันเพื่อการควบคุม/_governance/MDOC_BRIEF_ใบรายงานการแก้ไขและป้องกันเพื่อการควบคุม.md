# MDOC_BRIEF — CAR ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `CAR` |
| ชื่อ | ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม · Corrective Action Request (CAR) |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | เอกสารทั่วไป · F-TMP-008 |
| หน้าเอกสาร | `#/governance/car` |
| เจ้าของแบบ | แผนกบริหารองค์กร และกำกับดูแล · role-ic-officer |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-CCC-04 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม Corrective Action Request (CAR) |
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
doc_type: CAR
name_th: ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม
name_en: Corrective Action Request (CAR)
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: เอกสารทั่วไป
feature_id: F-TMP-008
route_path: '#/governance/car'
owner:
  unit: แผนกบริหารองค์กร และกำกับดูแล
  role: role-ic-officer
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-CCC-04 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม Corrective Action Request (CAR)
doa: pending
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('CAR', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
