# MDOC_BRIEF — ACR แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `ACR` |
| ชื่อ | แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี · Account Code Add/Change/Cancel Request |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | Accounting · F-TMP-003 |
| หน้าเอกสาร | `#/accounting/account-code-request` |
| เจ้าของแบบ | ฝ่ายบัญชี · role-mgr-acc |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-ACC-01 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี |
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
doc_type: ACR
name_th: แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี
name_en: Account Code Add/Change/Cancel Request
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: Accounting
feature_id: F-TMP-003
route_path: '#/accounting/account-code-request'
owner:
  unit: ฝ่ายบัญชี
  role: role-mgr-acc
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-ACC-01 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี
doa: pending
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('ACR', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
