# MDOC_BRIEF — IVMA แบบฟอร์มเริ่มต้นธุรกรรม

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `IVMA` |
| ชื่อ | แบบฟอร์มเริ่มต้นธุรกรรม · Transaction Initiation Form |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | finance · F-TMP-001 |
| หน้าเอกสาร | `#/investment/transaction-initiation` |
| เจ้าของแบบ | ฝ่ายบริหารการลงทุน · ผู้จัดการฝ่ายบริหารการลงทุน |
| เวอร์ชัน | v1 — เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-IVM-01 Rev.00 01/07/2569 |
| แบบพิมพ์ | FM-IVM-01 แบบฟอร์มเริ่มต้นธุรกรรม |
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
doc_type: IVMA
name_th: แบบฟอร์มเริ่มต้นธุรกรรม
name_en: Transaction Initiation Form
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: finance
feature_id: F-TMP-001
route_path: '#/investment/transaction-initiation'
owner:
  unit: ฝ่ายบริหารการลงทุน
  role: ผู้จัดการฝ่ายบริหารการลงทุน
version: v1
change_note: เวอร์ชันแรก — ขึ้นจากแบบฟอร์มลูกค้า FM-IVM-01 Rev.00 01/07/2569
prints:
- FM-IVM-01 แบบฟอร์มเริ่มต้นธุรกรรม
doa: pending
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('IVMA', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
