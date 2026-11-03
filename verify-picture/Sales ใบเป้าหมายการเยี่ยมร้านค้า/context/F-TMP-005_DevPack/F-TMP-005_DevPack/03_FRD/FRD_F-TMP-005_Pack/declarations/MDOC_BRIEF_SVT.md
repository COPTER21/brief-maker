# MDOC_BRIEF — SVT ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `SVT` |
| ชื่อ | ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade · Store Visit Target (General Trade) |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | SAL · F-TMP-005 |
| หน้าเอกสาร | `#/sales/visit-target` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-SAL-09 ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade |
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
doc_type: SVT
name_th: 'ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade'
name_en: Store Visit Target (General Trade)
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: SAL
feature_id: F-TMP-005
route_path: '#/sales/visit-target'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก
prints:
- 'FM-SAL-09 ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade'
doa: pending
request_no: null
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('SVT', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
