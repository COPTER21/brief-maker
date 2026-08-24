# DOCCFG_BRIEF — F-WH-DN Delivery Note

> ตรวจ registry สดจาก `Related context/f-doccfg/f-doccfg.html` แล้วเมื่อ 2026-08-20
> เลขทุกใบจาก ENG-DOC-NUM เท่านั้น · สำเนาจาก ENG-DOC-STORE เท่านั้น · ห้าม hardcode format/+1/snapshot policy

## ผลตรวจ registry

**Reuse entry เดิม — ไม่ประกาศ doc_type ใหม่**

| Code | ชื่อ | Module | Preset ปัจจุบัน | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| `DLV` | ใบส่งของ | WMS | `{PREFIX}-{YYYY}-{run:4}` | รายปี | global | ✗ | ✓ | ✗ |

ห้ามใช้ code `DN` สำหรับใบส่งของ เพราะ registry ปัจจุบันใช้ `DN` กับ “ใบเพิ่มหนี้” ของ Accounting อยู่แล้ว. เลข `DN-...` ใน prototype เป็น mock display; production ต้องขอเลขผ่าน `DLV` entry และแสดงค่าที่ engine คืนมาโดยไม่ประกอบเอง

## จุดออกเลข — ENG-DOC-NUM

| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| Reference: confirm pack selection และ transaction พร้อมสร้าง DN | `03_LOGIC` FN-03 / transaction 1 | ขอเลขครั้งเดียวใน idempotent create; create ล้มเหลวต้องไม่เหลือ DN/pack binding ครึ่งกลาง |
| Manual: confirm Manual create | `03_LOGIC` FN-15 | ใช้ doc type `DLV` เดียวกัน; แยก `creation_mode=manual` ไม่สร้าง running sequence ใหม่ |

เลข immutable หลัง engine ออกแล้ว. แม้ admin เปลี่ยน config ภายหลัง เอกสารเดิมต้องคงเลขเดิม.

## จุดเก็บสำเนา — ENG-DOC-STORE

| Event | เมื่อไหร่ | อ้าง FRD |
|---|---|---|
| `sent_external` | พิมพ์/ส่งใบส่งของออกให้ผู้รับหรือแนบไปกับสินค้า ตาม policy ที่ DLV เปิดไว้ | `02_API` API-17 / XT-06; `01_UI` document tab |

ไม่มี approval chain จึงไม่ใช้ `approved_final` ในรอบนี้. Manual DN ใช้ snapshot policy เดียวกับ DLV เมื่อผู้ใช้ส่งออกเอกสารจริง; การเปลี่ยนสถานะ Manual อย่างเดียวไม่ถือเป็น snapshot trigger.

## Dev wiring note

- `dn.dn_no = ENG-DOC-NUM.next('DLV', company_ctx, idempotency_key)` ใน FN-03/FN-15 เท่านั้น
- renderer ส่งไฟล์ไป `ENG-DOC-STORE.store(pdf,'DLV',dn_id,'sent_external')`; engine ตรวจ flag เอง
- ห้ามอ่าน/เขียนตาราง config โดยตรง และห้ามใช้เลข mock จาก HTML เป็น production value
- admin ปรับ format/reset/scope/no-gap/snapshot flags ได้ที่ F-DOCCFG; feature ไม่ล็อกค่าเหล่านี้

## Open item

- OQ-DOCCFG-01: PM/BA ต้องยืนยันข้อความที่ผู้ใช้คุ้นเคยว่าเลข production จะแสดง prefix ตาม entry `DLV` หรือ admin จะตั้ง prefix display อื่นผ่าน F-DOCCFG; ห้ามเปลี่ยน code เป็น `DN` เพราะชน registry

