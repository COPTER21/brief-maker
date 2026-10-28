# MDOC_BRIEF — LOA หนังสือสัญญายืม

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `LOA` |
| ชื่อ | หนังสือสัญญายืม · Box Loan Agreement |
| หมวด / หน้าที่ | AGR สัญญาและข้อตกลง · F31 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | SALES · F-TMP-006 |
| หน้าเอกสาร | `#/sales/box-loan-agreement` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-SAL-14 หนังสือสัญญายืม (ต้นฉบับ)_Rev.00 · FM-SAL-14 หนังสือสัญญายืม (สำเนา)_Rev.00 (เอกสารชุด · เลขที่เดียว) |
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
doc_type: LOA
name_th: หนังสือสัญญายืม
name_en: Box Loan Agreement
class_code: AGR
function_code: F31
taxonomy_def_id: null
module: SALES
feature_id: F-TMP-006
route_path: '#/sales/box-loan-agreement'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-SAL-14 หนังสือสัญญายืม (ต้นฉบับ)_Rev.00
- FM-SAL-14 หนังสือสัญญายืม (สำเนา)_Rev.00
doa: pending
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('LOA', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
