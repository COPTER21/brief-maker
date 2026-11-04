# MDOC_BRIEF — DSR คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `DSR` |
| ชื่อ | คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature) · Digital Signature Request Form |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F31 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | HR · F-TMP-003 |
| หน้าเอกสาร | `#/hr/digital-signature-request` |
| เจ้าของแบบ | ฝ่ายทรัพยากรบุคคล · role-mgr-hr |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-HRM-23 คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)_Rev.00 |
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
doc_type: DSR
name_th: คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)
name_en: Digital Signature Request Form
class_code: FRM
function_code: F31
taxonomy_def_id: null
module: HR
feature_id: F-TMP-003
route_path: '#/hr/digital-signature-request'
owner:
  unit: ฝ่ายทรัพยากรบุคคล
  role: role-mgr-hr
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-HRM-23 คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)_Rev.00
doa: pending
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('DSR', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
