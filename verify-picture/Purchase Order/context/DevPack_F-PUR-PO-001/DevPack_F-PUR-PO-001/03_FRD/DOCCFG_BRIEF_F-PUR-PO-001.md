# DOCCFG_BRIEF — F-PUR-PO · PO ใบสั่งซื้อ

> Auto-register ลง **Document Configuration (F-DOCCFG)** ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register
> **เลขทุกใบจาก `ENG-DOC-NUM.next()` เท่านั้น · สำเนาทุกใบจาก `ENG-DOC-STORE.store()` เท่านั้น — ห้าม hardcode**

---

## 1. doc_type ที่ประกาศ

| Code | ชื่อไทย | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออกนอกระบบ | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| **PO** | ใบสั่งซื้อ | PUR | `{PREFIX}-{YYYY}-{run:4}` → **`PO-YYYY-NNNN`** | รายปี | global | ✗ | ✓ | ✓ |

**ปี `{YYYY}` = ปี ค.ศ. เท่านั้น** (GOLDEN_RULES §1 · PREBRIEF BR-19) — ห้าม preset ที่ให้ผลเป็น พ.ศ.

**เช็คชนกับ registry เดิม**: code `PO` — ยังไม่มีใน registry ของเลนนี้ · ไม่มีความหมายซ้อนกับ doc_type อื่น (PR = ใบขอซื้อ ของ F072 คนละตัว) → **ประกาศใหม่ได้**

**เหตุผลค่า default**
| ค่า | เหตุผล |
|---|---|
| reset **รายปี** | รูปแบบเลขมีปีอยู่แล้ว (`PO-2026-0001`) — ไม่ reset จะทำให้เลขกระโดดข้ามปีโดยไม่จำเป็น |
| scope **global** | PO เป็นเอกสารจัดซื้อระดับบริษัท ไม่ผูกสาขา (ถ้า tenant ใดต้องแยกสาขา admin เปลี่ยนเป็น branch ได้ที่จอ F-DOCCFG) |
| no-gap **✗** | PO ไม่ใช่เอกสารภาษี (ต่างจาก INV/RV/CN/DN/JE) — ไม่ต้องบังคับเลขไม่ขาดช่วง |
| snapshot **ส่งออกนอกระบบ ✓** | PO ถูกส่งให้ผู้ขายจริง — ต้องเก็บสำเนาใบที่ส่งออกไป |
| snapshot **อนุมัติ+เซ็น ✓** | มีสายอนุมัติ DOA + ช่องลายเซ็นใน PDF — เก็บสำเนา ณ ตอนอนุมัติครบเป็นหลักฐาน |

> ทุกค่าข้างบนเป็น **default ตอน register** — admin แก้ได้ทุกช่องที่จอ F-DOCCFG (มติ 2026-08-11) · ห้ามประกาศค่า "บังคับแก้ไม่ได้"

---

## 2. จุดออกเลข (ENG-DOC-NUM)

| เมื่อไหร่ | อ้าง PREBRIEF | หมายเหตุ |
|---|---|---|
| transition **`draft → approved`** (อนุมัติครบสาย DOA) | §5 · S-04 | **ไม่ออกเลขตอน draft** — กันเปลืองเลขจากร่างที่ถูกทิ้ง (PREBRIEF S-09 ร่างค้างไว้ได้) |

- ร่างที่ยังไม่อนุมัติ แสดงเป็น **"(ยังไม่ออกเลข)"** บนหน้าจอ — ห้าม feature ตั้งเลขชั่วคราวเอง
- **เลขเอกสาร immutable** — ออกแล้วห้ามเปลี่ยน/renumber แม้ config เปลี่ยนภายหลัง
- แก้ใบหลังอนุมัติ → re-approve (S-08) **ใช้เลขเดิม ไม่ออกเลขใหม่** (ไม่ใช่เอกสารใบใหม่)

---

## 3. จุดเก็บสำเนา (ENG-DOC-STORE)

| Event | เมื่อไหร่ | อ้าง PREBRIEF |
|---|---|---|
| `approved_final` | อนุมัติครบทุก slot (`draft → approved`) | §5 · S-04 |
| `sent_external` | กด "ส่งให้ผู้ขาย" (`approved → sent`) | §5 · S-07 · §6.3 |
| `sent_external` (ซ้ำได้) | ส่งใบที่ผ่าน re-approve ให้ผู้ขายอีกครั้ง | S-08 → S-07 |

> engine เป็นคนเช็ค flag เองว่าจะเก็บหรือไม่ — feature แค่เรียก

---

## 4. Dev wiring note (Phase B)

```
po.number = ENG-DOC-NUM.next('PO', company_ctx)   // ที่ transition draft → approved เท่านั้น
ENG-DOC-STORE.store(pdf, 'PO', po_id, 'approved_final')   // ตอนอนุมัติครบ
ENG-DOC-STORE.store(pdf, 'PO', po_id, 'sent_external')    // ตอนกดส่งให้ผู้ขาย
```

- ❌ ห้าม format เลขเอง · ห้าม `+1` เอง · ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
- ❌ ห้ามใส่เงื่อนไข "เก็บสำเนาเมื่อ…" ลง feature — เป็น flag ที่ F-DOCCFG
- ✅ Phase A (HTML) ใช้ mock เลข `PO-2026-NNNN` พร้อมคอมเมนต์ `// TODO: ENG-DOC-NUM`

---

## 5. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| DOC-Q1 | tenant ที่มีหลายสาขาต้องการ scope `branch` + prefix สาขาไหม (รอบนี้ default `global`) | Strike |
| DOC-Q2 | ออกเลขตอน `approved` หรือควรออกตอนกด "ส่งอนุมัติ" — รอบนี้เลือก `approved` (กันเปลืองเลขจากใบที่ถูกปฏิเสธ) | Strike |
