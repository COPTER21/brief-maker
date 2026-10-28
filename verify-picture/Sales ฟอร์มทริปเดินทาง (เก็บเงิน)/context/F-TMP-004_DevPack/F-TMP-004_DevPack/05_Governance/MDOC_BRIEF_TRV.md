# MDOC_BRIEF — TRV ใบเดินทาง : เขตการขาย General Trade

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `TRV` |
| ชื่อ | ใบเดินทาง : เขตการขาย General Trade · Sales Territory Travel Sheet |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F31 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | SALES · F-TMP-004 |
| หน้าเอกสาร | `#/sales/travel-sheet` |
| เจ้าของแบบ | ฝ่ายขาย · role-mgr-sales |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | ใบเดินทาง เขตการขาย General Trade (เก็บเงิน)_v1 |
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
doc_type: TRV
name_th: 'ใบเดินทาง : เขตการขาย General Trade'
name_en: Sales Territory Travel Sheet
class_code: FRM
function_code: F31
taxonomy_def_id: null
module: SALES
feature_id: F-TMP-004
route_path: '#/sales/travel-sheet'
owner:
  unit: ฝ่ายขาย
  role: role-mgr-sales
version: v1
change_note: เวอร์ชันแรก
prints:
- ใบเดินทาง เขตการขาย General Trade (เก็บเงิน)_v1
doa: pending
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('TRV', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
