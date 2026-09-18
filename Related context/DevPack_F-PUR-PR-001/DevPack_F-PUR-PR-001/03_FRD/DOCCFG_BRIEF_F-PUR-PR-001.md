# DOCCFG_BRIEF — F-PUR-PR · PR ใบขอซื้อ
> Auto-register ลง Document Configuration ตอน deploy · admin ปรับได้ทุกช่องหลัง register
> เลขทุกใบจาก **ENG-DOC-NUM** เท่านั้น · สำเนาทุกใบจาก **ENG-DOC-STORE** เท่านั้น — ห้าม hardcode / ห้าม +1 เอง

## doc_type ที่ประกาศ
| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| `PR` | ใบขอซื้อ | PUR | `{PREFIX}-{YYYY}-{run:4}` → **PR-2026-0001** | รายปี | global | ✗ | ✗ | ✓ |
> ★ `{YYYY}` = **ปี ค.ศ. 4 หลัก** ตาม golden rule ของ lane (TASTE_LOG: ปี ค.ศ. ล้วน) — ไม่ใช้ พ.ศ.
> เช็คชนกับ registry: `PR` ยังไม่มีใน TYPES (PO/GRN/QT/SO/INV มีแล้ว) → ประกาศใหม่ได้ · ความหมายไม่ซ้อนกับ code ใด

## จุดออกเลข (ENG-DOC-NUM)
| เมื่อไหร่ | อ้าง | หมายเหตุ |
|---|---|---|
| S: DRAFT→PENDING_APPROVAL (กด "ส่งอนุมัติ") | PREBRIEF §2 state machine · SC-02 | **ไม่ออกเลขตอน draft** (กันเปลืองเลข + รองรับ no-gap ในอนาคต) · เลข immutable ออกแล้วห้ามเปลี่ยน |

## จุดเก็บสำเนา (ENG-DOC-STORE)
| Event | เมื่อไหร่ | อ้าง |
|---|---|---|
| `approved_final` | อนุมัติครบทุก slot → render PDF ตาม print spec แล้วเก็บสำเนาพร้อมลายเซ็น | PREBRIEF §2 · §3.3 tab PDF/ลายเซ็น |
| `sent_external` | ✗ ไม่ใช้ — PR เป็นใบภายใน ไม่ส่งออกนอกองค์กร | — |

## Dev wiring note
- `pr.pr_no = ENG-DOC-NUM.next('PR', company_ctx)` ที่ transition ส่งอนุมัติ — **ห้าม format เอง ห้าม +1 เอง**
- `ENG-DOC-STORE.store(pdf,'PR',pr_id,'approved_final')` หลังอนุมัติครบ — engine เช็ค flag เองว่าเก็บหรือไม่
- ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
- ทุก default ข้างบน admin แก้ได้ที่จอ F-DOCCFG (มติ 2026-08-11) — ห้ามประกาศค่า "บังคับแก้ไม่ได้"
