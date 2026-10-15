# CSQ_BRIEF — F-PUR-RTV · RTV คืนผู้ขาย

> ใบประกาศ 7C Consequence → **ENG-CSQ (F-CSQ-01)** · deploy pipeline อ่านไฟล์นี้แล้ว auto-register
> feature **ประกาศ event เท่านั้น** — ห้าม hardcode การประทับผลรายท่อ ห้ามคำนวณมูลค่าเอง (ENG-CSQ-02 ทำ)
> ⛔ **ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ** (register จะถูก reject 422):
> - **OC** — เจ้าของคือ Operation Process (`sow.*`) เท่านั้น → **ไม่ประกาศ**
> - **DC ระดับเอกสาร** — DOA engine ยิงให้ตอนอนุมัติ/ปฏิเสธแล้ว → **ไม่ประกาศ**
> - **SC** — สงวนไว้ `trigger = false` เสมอ (OQ-C3 ยังไม่เคาะ) → **ไม่ประกาศ**

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| profile key | `CSQ-PUR-RTV` |
| feature_id | `F-PUR-RTV` (fid F080) |
| ชื่อ | RTV คืนผู้ขาย |
| module | Purchase (PUR) |
| register status | `pending` |

---

## 2. Event ที่ประกาศ (เฉพาะ transition ที่ "จบแล้วมีผล")

> ❌ ไม่ประกาศ `ร่าง → รออนุมัติ` — ยังไม่มีผลทางธุรกิจ (ของยังไม่ออก)
> ❌ ไม่ประกาศ `รออนุมัติ → อนุมัติแล้ว` และการปฏิเสธ/ส่งกลับแก้ — **DC ระดับเอกสาร** DOA engine เป็นเจ้าของ

| # | event_id | Trigger (อ้าง PREBRIEF) | ท่อที่กระทบ | kind / basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | `rtv_returned` | `อนุมัติแล้ว → ส่งคืนแล้ว` (§5.1 · S-11 · BR-13/BR-14) | **EC** (มูลค่าคงคลังลด) | `actual` — ของออกจากคลังจริงแล้ว มีเอกสารรองรับ (`basis: computed` จากมูลค่าที่คืน) | ทุกใบที่บันทึกส่งคืนสำเร็จ · มูลค่า = `Σ (จำนวนคืน × ราคาสุทธิจาก GRN)` |
| 2 | `rtv_credit_expected` | `อนุมัติแล้ว → ส่งคืนแล้ว` (§5.1 · S-30) | **FC** (เงินสด/ภาระกับผู้ขาย) | `estimated` — สิทธิเรียกเครดิตเกิดแล้ว แต่ยังไม่ได้รับจริง | ยิงพร้อม event 1 แต่แยกท่อ · **ไม่ใช่รายการบัญชี** (AC ยังไม่เกิด) |
| 3 | `rtv_credited` | `ส่งคืนแล้ว → ปิดใบ` (§5.1 · S-12 · BR-18) | **FC** | `actual` — ได้รับเครดิตจริงตามเลขเอกสารของผู้ขาย | มูลค่า = `มูลค่าเครดิตที่ได้รับจริง` (อาจ ≠ มูลค่าที่คืน — `OQ-RTV-06`) |
| 4 | `rtv_reversed` | `ส่งคืนแล้ว → กลับรายการ` (§5.1 · S-14 · BR-16) | **EC** · **FC** | `avoided` → กลับรายการ: หักผลของ event 1/2 ออก | เฉพาะใบที่เคย `ส่งคืนแล้ว` · ของกลับเข้าคลัง มูลค่าคงคลังกลับคืน |
| 5 | `rtv_cancelled` | `ร่าง/รออนุมัติ/อนุมัติแล้ว → ยกเลิก` (§5.1 · S-10, S-13) | — **no-effect** | — | **ประกาศเป็น no-effect โดยเจตนา** — ของยังไม่เคยออก ไม่มีท่อไหนถูกกระทบ (บันทึกไว้กันคนมาเติมท่อทีหลัง) |

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (ต้องเขียนชัด กันประกาศซ้ำ)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — RTV ไม่ใช่ต้นทาง OC |
| **DC** (Decision) | ❌ ไม่ | การอนุมัติ/ส่งกลับ/ปฏิเสธใบคืน = **DC ระดับเอกสาร** ที่ DOA engine ยิงเองแล้ว · RTV ไม่มี terminal decision นอกเหนือการเซ็นอนุมัติ (การตัดสินใจ "คืนหรือไม่คืน" จบในตัวเอกสารเอง) |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ |
| **SecC** (Security) | ❌ ไม่ | RTV ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย — ข้อมูลผู้ขายเป็นของ Vendor Master (คนละ feature) |
| **AC** (Accounting) | ❌ ไม่ | **RTV ไม่ post บัญชีเองในรอบนี้** — รายการบัญชีจริง (ใบลดหนี้ / ล้าง GR-IR) เกิดฝั่ง **AP/GL ใน W5** · รอบนี้เป็น mock + `TODO: JE posting` · เมื่อ W5 มาแล้วให้ **AP เป็นเจ้าของท่อ AC** กันนับซ้ำ (`CSQ-Q2`) |

---

## 4. Payload contract (field ที่ต้องมีจริงใน entity — ตรวจกับ PREBRIEF §3)

| field | ที่มา | หมายเหตุ |
|---|---|---|
| `ref` = `rtv_id` | header | soft-reference ทุก event |
| `rtv_no` | doccfg `RTV-YYYY-NNNN` (§3.1) | ปี **ค.ศ.** |
| `grn_ref` · `po_ref` | header (soft-ref ผ่าน GRN) | เอกสารต้นทาง — **RTV ไม่เขียนกลับ PO** (`OQ-RTV-01`) |
| `vendor_ref` | ผู้ขาย (soft-ref LD-4C-02) | nullable-safe |
| `return_amount` | มูลค่าที่คืนรวม (§3.3) | หน่วยบาท · ใช้กับ event 1, 2, 4 |
| `return_amount_ex_vat` | ยอดรวมก่อนภาษี (§3.3) | ให้ engine เลือกฐานได้ |
| `credit_amount_actual` | มูลค่าเครดิตที่ได้รับจริง (§3.1) | เฉพาะ event 3 |
| `credit_doc_no` | เลขเอกสารเครดิตของผู้ขาย (§3.1 · mock) | เฉพาะ event 3 |
| `qty_returned_by_line[]` | จำนวนคืนต่อบรรทัด (§3.2) | ให้ engine ผูกกับสินค้า/มูลค่าคงคลัง |
| `source_location_ref[]` | location ต้นทางต่อบรรทัด (quarantine/ปกติ · §3.2) | soft-ref |
| `return_reason[]` | เหตุผลคืนต่อบรรทัด (§3.2) | ใช้จัดกลุ่มผลกระทบ/คุณภาพผู้ขาย |
| `cost_center_ref` | soft-ref (§3.1) | nullable |
| `occurred_at` | timestamp (**ค.ศ.**) | ทุก event |
| `actor` | ผู้กดทำ transition | ทุก event |

> ⚠️ ทุกค่ามูลค่าเป็น `basis: computed` จาก field ที่มีจริงในใบ — **feature ห้ามตีมูลค่าเพิ่มเอง** ENG-CSQ-02 เป็นคนประเมิน
> ⚠️ ต้นทุนจริงของของที่ตัดออก (FIFO/เฉลี่ย) เป็นของ **Inventory Valuation (F070 · W4)** — รอบนี้ใช้ราคาจาก GRN/PO ตรง ๆ (`CSQ-Q3`)

---

## 5. HTML/FRD Injection note

- HTML **ไม่ต้องวาด UI ประเมินผลกระทบ** — Engine เป็นคนประทับ · feature แค่รู้ว่า emit ตอนไหน
- จุด emit = transition ตาม §2 เท่านั้น (ตรงกับ state machine PREBRIEF §5.1)
- ในโค้ด Phase A ใส่เป็น mock + marker **`FWD-WIRE: ENG-CSQ emit`** ที่ transition ที่เกี่ยว (ใน .md ใช้ `TODO: ENG-CSQ emit` ตามปกติ)
- FRD Phase B: `05_RULES.md` เพิ่มหัวข้อ "ผลกระทบ 7C" ชี้มาที่ไฟล์นี้

---

## 6. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| CSQ-Q1 | `rtv_returned` (EC) กับ `rtv_credit_expected` (FC) ควรเป็น 2 event แยก หรือ 1 event ที่ยิง 2 ท่อ | เจ้าของ F-CSQ-01 |
| CSQ-Q2 | เมื่อ W5 (AP/CN) มาแล้ว ท่อ **AC** และ `rtv_credited` (FC) จะยิงจาก RTV หรือจาก AP — **กันนับซ้ำ** | เจ้าของ F-CSQ-01 + เจ้าของ AP (W5) |
| CSQ-Q3 | มูลค่าที่ใช้ตัดของออกควรเป็นราคาจาก GRN หรือ **ต้นทุนเฉลี่ย/FIFO** จาก Inventory Valuation (F070 · W4) | เจ้าของ F070 + F-CSQ-01 |
| CSQ-Q4 | `rtv_cancelled` ประกาศเป็น no-effect — ต้อง register แถวเปล่าไว้ หรือไม่ต้องส่งเข้า registry เลย | เจ้าของ F-CSQ-01 |
