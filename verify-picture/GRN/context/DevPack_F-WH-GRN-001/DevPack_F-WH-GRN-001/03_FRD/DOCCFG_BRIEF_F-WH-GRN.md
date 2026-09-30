# DOCCFG_BRIEF — F-WH-GRN · GRN รับของ

> Auto-register ลง **Document Configuration (F-DOCCFG)** ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register
> **เลขทุกใบจาก `ENG-DOC-NUM.next()` เท่านั้น · สำเนาทุกใบจาก `ENG-DOC-STORE.store()` เท่านั้น — ห้าม hardcode**

---

## 1. doc_type ที่ประกาศ

| Code | ชื่อไทย | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออกนอกระบบ | Snap: จุดจบสมบูรณ์ (`approved_final`) |
|---|---|---|---|---|---|---|---|---|
| **GRN** | ใบรับของ | WH | `{PREFIX}-{YYYY}-{run:4}` → **`GRN-YYYY-NNNN`** | รายปี | global | ✗ | ✗ | ✓ |

**ปี `{YYYY}` = ปี ค.ศ. เท่านั้น** (GOLDEN_RULES §1 · PREBRIEF BR-19) — ห้าม preset ที่ให้ผลเป็น พ.ศ.

**เช็คชนกับ registry เดิม**: code `GRN` — ยังไม่มีใน registry ของเลนนี้ (มีแต่ `PO` ที่ประกาศไปแล้วโดย F-PUR-PO) · ไม่มีความหมายซ้อนกับ doc_type อื่น (RTV/ADJ/TRF จะประกาศโดย feature ของตัวเองในเลนเดียวกัน) → **ประกาศใหม่ได้**

**เหตุผลค่า default**

| ค่า | เหตุผล |
|---|---|
| reset **รายปี** | รูปแบบเลขมีปีอยู่แล้ว (`GRN-2026-0001`) — ไม่ reset จะทำให้เลขกระโดดข้ามปีโดยไม่จำเป็น |
| scope **global** | รอบนี้ GRN ออกเลขระดับบริษัท · tenant ที่ต้องแยกเลขต่อคลัง/สาขา ให้ admin เปลี่ยนเป็น `branch` ที่จอ F-DOCCFG (ดู DOC-Q1) |
| no-gap **✗** | GRN ไม่ใช่เอกสารภาษี (ต่างจาก INV/RV/CN/DN/JE) — ไม่ต้องบังคับเลขไม่ขาดช่วง |
| snapshot **ส่งออกนอกระบบ ✗** | ใบรับของเป็นเอกสารภายในคลัง ไม่ได้ถูกส่งให้บุคคลภายนอกเป็นทางการ (พิมพ์ให้ผู้ส่งเซ็นได้ แต่ไม่ใช่การส่งออกเชิงระบบ) |
| snapshot **จุดจบสมบูรณ์ ✓** | GRN **ไม่มีสายอนุมัติ** — จุดที่เอกสาร "จบและแก้ไม่ได้อีก" คือ **`post`** (movement เกิดแล้ว · append-only) จึงต้องเก็บสำเนา ณ จุดนั้นเป็นหลักฐานประกอบ 3-way match (ดู DOC-Q2 เรื่องชื่อ flag) |

> ทุกค่าข้างบนเป็น **default ตอน register** — admin แก้ได้ทุกช่องที่จอ F-DOCCFG (มติ 2026-08-11) · ห้ามประกาศค่า "บังคับแก้ไม่ได้"

---

## 2. จุดออกเลข (ENG-DOC-NUM)

| เมื่อไหร่ | อ้าง PREBRIEF | หมายเหตุ |
|---|---|---|
| transition **`draft → posted`** (กด "รับเข้า") | §5.1 · S-07 · BR-20 | **ไม่ออกเลขตอน draft** — กันเปลืองเลขจากร่างที่ถูกทิ้ง (S-06/S-09) |

- ร่างที่ยังไม่ post แสดงเป็น **"(ยังไม่ออกเลข)"** บนหน้าจอ — ห้าม feature ตั้งเลขชั่วคราวเอง
- **เลขเอกสาร immutable** — ออกแล้วห้ามเปลี่ยน/renumber แม้ config เปลี่ยนภายหลัง
- **กลับรายการ (reversal · S-08)** = ใบเดิมยังคงเลขเดิมและสถานะ `reversed` · **ไม่ออกเลขใหม่ให้ใบเดิม** · ถ้าต้องรับใหม่ต้องสร้าง **ใบใหม่** ซึ่งจะได้เลขถัดไปตามปกติ

---

## 3. จุดเก็บสำเนา (ENG-DOC-STORE)

| Event | เมื่อไหร่ | อ้าง PREBRIEF |
|---|---|---|
| `approved_final` (= จุด post ของ GRN) | `draft → posted` สำเร็จ | §5.1 · S-07 |
| `approved_final` (ครั้งที่ 2) | `posted → reversed` — เก็บสำเนาใบ ณ สถานะกลับรายการ เพื่อให้เห็นคู่ก่อน/หลัง | §5.1 · S-08 · BR-15 |

> engine เป็นคนเช็ค flag เองว่าจะเก็บหรือไม่ — feature แค่เรียก

---

## 4. Dev wiring note (Phase B)

```
grn.number = ENG-DOC-NUM.next('GRN', company_ctx)        // ที่ transition draft → posted เท่านั้น
ENG-DOC-STORE.store(pdf, 'GRN', grn_id, 'approved_final') // ตอน post สำเร็จ
ENG-DOC-STORE.store(pdf, 'GRN', grn_id, 'approved_final') // อีกครั้งตอนกลับรายการ (สำเนาสถานะ reversed)
```

- ❌ ห้าม format เลขเอง · ห้าม `+1` เอง · ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
- ❌ ห้ามใส่เงื่อนไข "เก็บสำเนาเมื่อ…" ลง feature — เป็น flag ที่ F-DOCCFG
- ✅ Phase A (HTML) ใช้ mock เลข `GRN-2026-NNNN` พร้อม marker `FWD-WIRE: ENG-DOC-NUM` (ในไฟล์ .md ใช้ `TODO:` ตามปกติ)

---

## 5. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| DOC-Q1 | tenant ที่มีหลายคลัง/หลายสาขาต้องการ scope `branch` + prefix ต่อคลังไหม (รอบนี้ default `global`) | Strike |
| DOC-Q2 | flag `approved_final` ของ F-DOCCFG ตั้งชื่อบนสมมติฐานว่าเอกสารมีการอนุมัติ — **GRN ไม่มี DOA** จึง map เข้ากับจุด `post` · ควรเพิ่มชื่อ flag กลางเป็น "finalized" ไหม | เจ้าของ F-DOCCFG |
| DOC-Q3 | ต้องเก็บสำเนา PDF ตอนกลับรายการจริงไหม หรือให้ดูจาก audit trail พอ (รอบนี้เก็บ เพื่อให้ 3-way match ย้อนตรวจได้) | Strike + บัญชี (W5) |
