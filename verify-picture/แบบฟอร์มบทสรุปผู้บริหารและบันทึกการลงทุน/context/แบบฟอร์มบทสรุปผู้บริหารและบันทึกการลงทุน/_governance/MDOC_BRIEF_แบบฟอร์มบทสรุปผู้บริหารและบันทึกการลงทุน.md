# MDOC_BRIEF — IVM แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน

> ใบประกาศแบบเอกสารเข้าทะเบียน F185 · ระบบ register ตอน deploy · F185 เก็บแบบ ไม่เก็บฉบับ (LD-DM-01)
> Verdict: **WARN** · source: `declaration` · สร้างโดย mdoc-declaration

## แบบเอกสาร
| หัวข้อ | ค่า |
|---|---|
| รหัส (จาก F-DOCCFG) | `IVM` |
| ชื่อ | แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน · Executive Summary and Investment Memo Form |
| หมวด / หน้าที่ | FRM แบบฟอร์ม · F01 |
| Taxonomy definition | — (รออนุมัติ definition ใหม่) |
| Module · Feature | Business Development · F-TMP-005 |
| หน้าเอกสาร | `#/investment-memo` |
| เจ้าของแบบ | ฝ่ายพัฒนาธุรกิจ · role-mgr-bu |
| เวอร์ชัน | v1 — เวอร์ชันแรก |
| แบบพิมพ์ | FM-BDM-05 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน |
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
doc_type: IVM
name_th: แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน
name_en: Executive Summary and Investment Memo Form
class_code: FRM
function_code: F01
taxonomy_def_id: null
module: Business Development
feature_id: F-TMP-005
route_path: '#/investment-memo'
owner:
  unit: ฝ่ายพัฒนาธุรกิจ
  role: role-mgr-bu
version: v1
change_note: เวอร์ชันแรก
prints:
- FM-BDM-05 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน
doa: pending
request_no: null
announcement_default: {}
source: declaration
```

## Dev wiring note
- register ผ่าน F185 register API ตอน deploy (pipeline) — feature ห้ามเขียนตาราง `doc_type` / `doc_type_version` เอง
- เลขที่เอกสารของฉบับ = `ENG-DOC-NUM.next('IVM', ctx)` (doccfg) · สายอนุมัติ = DOA engine (doa) · แจ้งเตือน = ENG-NOTIFY (ntf) — ไม่อยู่ในใบนี้
- เปลี่ยนแบบพิมพ์/หน้าเอกสาร = ประกาศเวอร์ชันใหม่ (v+1) พร้อม change_note — ห้ามแก้เวอร์ชันที่ register แล้ว
