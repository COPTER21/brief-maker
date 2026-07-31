# Purchase Config Bible — CUBE NATIVE P2P

> **เอกสารนี้คืออะไร:** สรุปนโยบายควบคุมการจัดซื้อ (Purchase Configuration) ทั้งหมดของ CUBE NATIVE — ใช้เป็น **context กลาง** สำหรับ session อื่นที่จะพัฒนา PR / PO / GRN / Invoice / Payment ให้ทุก feature เคารพ setting เดียวกันและทำงานสอดคล้องกัน
>
> **Feature:** `F-PURCHASE-CONFIG-001` · Module: การเงิน/จัดซื้อ (Finance → Procurement) · Value Stream: P2P
> **ขอบเขต:** Company-level **policy gate** — ไม่ใช่ master data, ไม่ใช่ payment term (payment term อยู่ที่ `F-PAYMENT-TERM-001` แยกต่างหาก)
> **Version:** v1.4 · อัปเดตล่าสุด 2026-06-02

---

## 0. หลักการสำคัญ (อ่านก่อนใช้)

1. **Purchase Config = นโยบาย ไม่ใช่ข้อมูล** — เก็บ "กฎ" ที่บังคับใช้กับ flow PR→PO→GRN→Invoice→Payment ทั้งบริษัท (1 ชุดต่อ tenant)
2. **ทุก feature ปลายน้ำต้องอ่าน config นี้ก่อนทำงาน** — PR/PO/GRN/Invoice/Payment ดึงค่า policy ไป enforce ไม่ hardcode กฎเอง
3. **ไม่มี payment term ที่นี่** — เงื่อนไขชำระเงินเป็น master แยก (`F-PAYMENT-TERM-001`) PR/PO ไปดึงจาก master นั้น
4. **Approval ไม่อยู่ที่นี่** — การกำหนดผู้อนุมัติ/วงเงิน ทำที่ **DOA Engine** (Policy Center) — Purchase Config แค่ "เปิด/ปิด" การบังคับ ไม่กำหนดผู้อนุมัติเอง
5. **action 2 แบบ:** `BLOCK` (บล็อกไม่ให้ทำต่อ) vs `WARN` (เตือนแต่ทำต่อได้) — ระบุชัดในแต่ละ policy ด้านล่าง
6. **Config นี้ปรับได้ที่ runtime** — ค่าที่ระบุด้านล่างคือ **default** ผู้ใช้ระดับ Finance Lead ปรับได้ผ่านหน้า Settings

---

## 1. โครงสร้าง Config (12 Policies / 5 หมวด)

| หมวด (Tab) | Policies |
|---|---|
| **A. การควบคุมคำขอซื้อ** | งบประมาณ · เปรียบเทียบราคา · แบ่งแยกหน้าที่ (SoD) · แปลง PR→PO |
| **B. ราคา & จับคู่เอกสาร** | ส่วนต่างราคา · 3-Way Match · ส่วนต่างใบแจ้งหนี้ · ตรวจจับเอกสารซ้ำ |
| **C. การรับของ** | นโยบายการรับของ (GR) |
| **D. ผู้ขาย & แหล่งซื้อ** | นโยบายผู้ขาย · นโยบายแหล่งซื้อ (Catalog) |
| **E. ภาษี** | นโยบายภาษี |

> **หมายเหตุ:** Approval Threshold + Contract Compliance ถูกออกแบบไว้แล้ว (มีใน data model) แต่**ยังไม่เปิดใช้ใน UI** — Approval ไปทำที่ DOA, Contract รอ feature สัญญา/Blanket Agreement (ดู §8)

---

## 2. Config Key Reference (สำหรับ Dev — ใช้ key เหล่านี้)

ทุก feature อ่าน config ผ่าน object เดียว (เสนอ endpoint: `GET /procurement/config`)

```json
{
  "budget_enabled": true,
  "budget_block_over": true,
  "budget_require_ref": true,

  "comparison_enabled": true,
  "comparison_min_quotes": 3,
  "comparison_threshold": 50000,

  "sod_enabled": true,
  "sod_pr_ne_po": true,
  "sod_po_ne_gr": true,
  "sod_gr_ne_pay": true,

  "pr2po_mode": "manual",
  "pr2po_consolidate": true,

  "price_var_enabled": true,
  "price_var_pct": 5,
  "price_var_block": false,

  "match_enabled": true,
  "match_tolerance": 2,
  "match_block": true,

  "inv_var_enabled": true,
  "inv_var_pct": 2,
  "inv_var_amount": 500,

  "dup_pr": true,
  "dup_pr_days": 7,
  "dup_invoice": true,

  "receiving_partial": true,
  "receiving_autoclose": true,
  "receiving_over_pct": 5,
  "receiving_under_pct": 0,

  "vendor_approved_only": true,
  "vendor_require_tax": true,

  "catalog_mode": "flexible",

  "tax_mode": "document"
}
```

---

## 3. หมวด A — การควบคุมคำขอซื้อ (PR Stage)

### A1. นโยบายงบประมาณ (Budget Policy)
**บังคับใช้ที่:** PR (ใบขอซื้อ) — ตอนสร้าง/ส่งอนุมัติ

| Key | Default | ความหมาย |
|---|---|---|
| `budget_enabled` | `true` | เปิดใช้การควบคุมงบประมาณ |
| `budget_block_over` | `true` | **BLOCK** ถ้ายอดซื้อเกินงบที่เหลือ → บล็อกไม่ให้ส่งอนุมัติ |
| `budget_require_ref` | `true` | **BLOCK** PR ต้องระบุเลขปลดอายัดงบก่อนอนุมัติ |

**Logic สำหรับ PR:**
- ถ้า `budget_enabled=false` → ข้ามการเช็คงบทั้งหมด
- ตอน submit PR: ถ้า `budget_block_over=true` และ `ยอดรวม PR > งบคงเหลือของ cost center` → **BLOCK** + error "ยอดเกินงบประมาณคงเหลือ"
- ถ้า `budget_require_ref=true` → field "เลขปลดอายัดงบ" เป็น **required** ก่อน submit

### A2. นโยบายเปรียบเทียบราคา (Comparison Policy)
**บังคับใช้ที่:** PR → PO (ก่อนออกใบสั่งซื้อ)

| Key | Default | ความหมาย |
|---|---|---|
| `comparison_enabled` | `true` | เปิดใช้การบังคับเปรียบเทียบราคา |
| `comparison_min_quotes` | `3` | จำนวนผู้เสนอราคาขั้นต่ำ (เจ้า) |
| `comparison_threshold` | `50000` | บังคับเปรียบเทียบเมื่อยอดซื้อ ≥ ค่านี้ (บาท) |

**Logic สำหรับ PO:**
- ถ้า `comparison_enabled=true` และ `ยอด PO ≥ comparison_threshold` → ต้องแนบใบเปรียบเทียบราคาที่มี **≥ `comparison_min_quotes` เจ้า** ก่อนออก PO
- ยอดต่ำกว่า threshold → ไม่บังคับ
- ไม่ครบเงื่อนไข → **BLOCK** การสร้าง PO

### A3. การแบ่งแยกหน้าที่ (Segregation of Duties — SoD)
**บังคับใช้ที่:** ทุก stage (PR/PO/GR/Payment) — เช็คตัวบุคคล
**มาตรฐาน:** COSO Internal Control · ใช้ร่วมกับ DOA Engine

| Key | Default | ความหมาย | Action |
|---|---|---|---|
| `sod_enabled` | `true` | เปิดใช้การแบ่งแยกหน้าที่ | — |
| `sod_pr_ne_po` | `true` | ผู้จัดทำ PR ต้องไม่ใช่ผู้จัดทำ PO | **BLOCK** สร้าง PO + แจ้งละเมิด |
| `sod_po_ne_gr` | `true` | ผู้จัดทำ PO ต้องไม่ใช่ผู้รับสินค้า (GR) | **BLOCK** บันทึก GR + แจ้งละเมิด |
| `sod_gr_ne_pay` | `true` | ผู้รับสินค้า (GR) ต้องไม่ใช่ผู้อนุมัติจ่ายเงิน | **BLOCK** จ่ายเงิน + แจ้งละเมิด |

**Logic:** ทุก feature ที่สร้างเอกสารขั้นถัดไป ต้องเช็คว่า `created_by` ของเอกสารปัจจุบัน ≠ `created_by` ของเอกสารต้นทาง ตาม rule ที่เปิดอยู่ ถ้าตรงกัน → **BLOCK** + log การละเมิด SoD

### A4. การแปลงใบขอซื้อ → ใบสั่งซื้อ (PR → PO Conversion)
**บังคับใช้ที่:** ตอนแปลง PR (อนุมัติแล้ว) เป็น PO

| Key | Default | ความหมาย |
|---|---|---|
| `pr2po_mode` | `'manual'` | `manual` = จัดซื้อสร้าง PO เอง · `auto` = ระบบสร้าง PO ทันทีหลัง PR อนุมัติ |
| `pr2po_consolidate` | `true` | รวม PR หลายใบจาก vendor เดียวกัน → PO เดียว (consolidation) |

**Logic สำหรับ PO:**
- `pr2po_mode='auto'` → เมื่อ PR เปลี่ยนสถานะเป็น approved → trigger สร้าง PO อัตโนมัติ
- `pr2po_mode='manual'` → PR approved รอจัดซื้อกดสร้าง PO
- `pr2po_consolidate=true` → ตอนสร้าง PO ระบบเสนอรวม PR ที่ vendor เดียวกัน + สกุลเงินเดียวกัน เป็น PO เดียว

---

## 4. หมวด B — ราคา & จับคู่เอกสาร (PO / Invoice Stage)

### B1. ส่วนต่างราคา (Price Variance)
**บังคับใช้ที่:** PO (ตอนสร้าง) — เทียบราคาสั่งซื้อกับราคามาตรฐาน/ราคาตลาด

| Key | Default | ความหมาย |
|---|---|---|
| `price_var_enabled` | `true` | เปิดใช้การเช็คส่วนต่างราคา |
| `price_var_pct` | `5` | ราคาต่างจากมาตรฐานได้ไม่เกิน % |
| `price_var_block` | `false` | `true`=**BLOCK** · `false`=**WARN** (เตือนแต่ผ่านได้) |

**Logic สำหรับ PO:** ถ้าราคาต่อหน่วยใน PO ต่างจากราคามาตรฐาน (material master/last price) เกิน `price_var_pct`% → ถ้า `price_var_block=true` บล็อก, ถ้า `false` เตือนเฉย ๆ

### B2. การจับคู่ 3 ทาง (3-Way Match)
**บังคับใช้ที่:** Payment (ก่อนสร้างใบสำคัญจ่าย) — จับคู่ PO ↔ GRN ↔ Invoice

| Key | Default | ความหมาย |
|---|---|---|
| `match_enabled` | `true` | เปิดใช้ 3-way match |
| `match_tolerance` | `2` | ความคลาดเคลื่อนที่ยอมรับ (ราคา/จำนวน) % |
| `match_block` | `true` | **BLOCK** การจ่ายถ้าจับคู่ไม่ผ่าน |

**Logic สำหรับ Payment:** ก่อนสร้าง Payment Voucher → จับคู่ PO/GRN/Invoice ถ้าจำนวน/ราคาต่างเกิน `match_tolerance`% และ `match_block=true` → **BLOCK** การจ่าย

### B3. ส่วนต่างใบแจ้งหนี้ (Invoice Variance)
**บังคับใช้ที่:** AP Invoice (ตอนตั้งหนี้) — เทียบใบแจ้งหนี้กับ PO/GRN

| Key | Default | ความหมาย |
|---|---|---|
| `inv_var_enabled` | `true` | เปิดใช้การเช็คส่วนต่างใบแจ้งหนี้ |
| `inv_var_pct` | `2` | ยอดต่างเป็น % ไม่เกิน |
| `inv_var_amount` | `500` | **หรือ** ยอดต่างเป็นเงิน ไม่เกิน (บาท) |

**Logic สำหรับ AP Invoice:** เทียบยอดใบแจ้งหนี้กับ PO+GRN → ถ้าต่างเกิน `inv_var_pct`% **หรือ** เกิน `inv_var_amount` บาท (เข้าเงื่อนไขข้อใดข้อหนึ่ง) → **WARN** ให้ตรวจสอบก่อนอนุมัติตั้งหนี้ (กันจ่ายเกิน/ราคาผิด/เรียกเก็บซ้ำ)

### B4. ตรวจจับเอกสารซ้ำ (Duplicate Detection)
**บังคับใช้ที่:** PR (ตอนสร้าง) + AP Invoice (ตอนตั้งหนี้) — **action = WARN เสมอ** (ไม่บล็อก รองรับซื้อซ้ำที่ตั้งใจ)

| Key | Default | ความหมาย |
|---|---|---|
| `dup_pr` | `true` | เตือน PR ซ้ำ |
| `dup_pr_days` | `7` | ช่วงเวลาที่ถือว่าซ้ำ นับจากใบล่าสุด (วัน) |
| `dup_invoice` | `true` | เตือนใบแจ้งหนี้ซ้ำ |

**Logic:**
- **PR ซ้ำ:** ผู้ขอคนเดียวกัน + สินค้ารายการเดียวกัน ภายใน `dup_pr_days` วัน → **WARN**
- **Invoice ซ้ำ:** ผู้ขายเดียวกัน + เลขที่ใบแจ้งหนี้เดียวกัน + ยอดเงินเท่ากัน (ตรงทั้ง 3) → **WARN** (ซ้ำแน่นอน)

---

## 5. หมวด C — การรับของ (GRN Stage)

### C1. นโยบายการรับของ (Receiving / GR)
**บังคับใช้ที่:** GRN (ใบรับสินค้า)

| Key | Default | ความหมาย |
|---|---|---|
| `receiving_partial` | `true` | อนุญาตรับของบางส่วน (รับหลายครั้งจนครบ PO) · `false`=รับครบครั้งเดียว |
| `receiving_autoclose` | `true` | ปิด PO อัตโนมัติเมื่อ**รับของครบ**ตาม tolerance |
| `receiving_over_pct` | `5` | รับเกินจำนวนใน PO ได้ไม่เกิน % |
| `receiving_under_pct` | `0` | รับขาดได้ไม่เกิน % (ถึงถือว่าครบ) |

**Logic สำหรับ GRN:**
- `receiving_partial=true` → รับได้หลายครั้ง ระบบ track ยอดสะสม
- รับเกิน PO: ยอมรับได้ถ้าไม่เกิน `receiving_over_pct`% ของ PO qty (เกินกว่านั้น → BLOCK)
- รับขาด: ถ้ายอดรับ ≥ (100% − `receiving_under_pct`%) → **ถือว่าครบ**
- **`receiving_autoclose` สำคัญ:** ปิด PO พิจารณาจาก**การรับของครบเท่านั้น ไม่เกี่ยวกับการจ่ายเงิน** → รองรับเครดิต (รับของก่อน จ่ายทีหลัง) PO ที่รับครบแล้วแต่ยังไม่จ่าย จะปิดสถานะการรับ แต่ยังค้างชำระอยู่ใน AP

> ⚠️ **สำคัญสำหรับ PO/Payment dev:** สถานะ "ปิด PO" (รับครบ) ≠ "จ่ายครบ" — แยก 2 สถานะ: `receipt_status` (open/closed by GR) กับ `payment_status` (unpaid/paid by Payment)

---

## 6. หมวด D — ผู้ขาย & แหล่งซื้อ (Vendor / Sourcing)

### D1. นโยบายผู้ขาย (Vendor Policy)
**บังคับใช้ที่:** PR/PO (ตอนเลือก vendor)

| Key | Default | ความหมาย |
|---|---|---|
| `vendor_approved_only` | `true` | **BLOCK** PR/PO เลือกได้เฉพาะ vendor สถานะ approved |
| `vendor_require_tax` | `true` | **BLOCK** vendor ต้องมีเลขประจำตัวผู้เสียภาษี 13 หลัก ก่อนใช้ในเอกสาร |

### D2. นโยบายแหล่งซื้อ (Catalog Policy)
**บังคับใช้ที่:** PR (ตอนเพิ่มรายการสินค้า)

| Key | Default | ความหมาย |
|---|---|---|
| `catalog_mode` | `'flexible'` | `catalog_only` = ซื้อจาก catalog ที่อนุมัติเท่านั้น · `flexible` = catalog + พิมพ์เองได้ · `free` = พิมพ์เองทั้งหมด |

**Logic สำหรับ PR:**
- `catalog_only` → รายการสินค้าเลือกจาก catalog เท่านั้น (BLOCK free-text)
- `flexible` → เลือก catalog หรือพิมพ์เอง (free-text item) ได้
- `free` → พิมพ์เองทั้งหมด ไม่บังคับ catalog

### D3. นโยบายภาษี (Tax Policy)
**บังคับใช้ที่:** PR/PO/Invoice (การคำนวณ VAT)

| Key | Default | ความหมาย |
|---|---|---|
| `tax_mode` | `'document'` | `document` = คิด VAT ท้ายเอกสาร · `line` = คิด VAT แยกต่อบรรทัด |

---

## 7. Cross-Feature Integration Map

| Feature ปลายน้ำ | Config ที่ต้องอ่าน/enforce |
|---|---|
| **PR (ใบขอซื้อ)** | budget_* · comparison_* (ตรวจตอนแปลง PO) · sod_pr_ne_po · dup_pr/dup_pr_days · vendor_* · catalog_mode · tax_mode |
| **PO (ใบสั่งซื้อ)** | comparison_* · price_var_* · sod_pr_ne_po · pr2po_* · vendor_* · tax_mode |
| **GRN (ใบรับสินค้า)** | receiving_* · sod_po_ne_gr |
| **AP Invoice (ใบแจ้งหนี้)** | inv_var_* · dup_invoice · tax_mode |
| **Payment (ใบสำคัญจ่าย)** | match_* · sod_gr_ne_pay |

**ลำดับ flow + จุดเช็ค:**
```
PR สร้าง ──► [budget เช็ค + budget ref + dup_pr + vendor + catalog]
   │
   ▼ approved
PR→PO ──────► [comparison เช็ค + price_var + sod_pr_ne_po + pr2po consolidate]
   │
   ▼
PO ส่ง vendor
   │
   ▼
GRN รับของ ─► [receiving over/under + partial + sod_po_ne_gr + autoclose รับครบ]
   │
   ▼
AP Invoice ─► [inv_var + dup_invoice]
   │
   ▼
Payment ────► [3-way match + sod_gr_ne_pay] ──► จ่าย
```

---

## 8. ส่วนที่เกี่ยวข้องแต่อยู่นอก Purchase Config

| เรื่อง | อยู่ที่ไหน | หมายเหตุ |
|---|---|---|
| **เงื่อนไขการชำระเงิน** (payment term) | Master `F-PAYMENT-TERM-001` | PR/PO ดึงจาก master นี้ — ไม่ config ที่ Purchase Config |
| **ผู้อนุมัติ + วงเงินอนุมัติ** | DOA Engine (Policy Center) | Purchase Config ไม่กำหนดผู้อนุมัติ — DOA จัดการ chain + วงเงินทั้งหมด |
| **สัญญา/Blanket Agreement** | (ยังไม่มี feature — backlog) | `contract_required`/`contract_warn_expiry` มีใน data model แล้ว แต่ปิดไว้จนกว่าจะมี feature สัญญา |
| **User Access / สิทธิ์** | Policy Center → User Roles Access | ใครเห็น/แก้ Purchase Config ได้ คุมที่ ENC |

---

## 9. Governance (CUBE 4.0)

- **User Access ENC:** หน้า Purchase Config ต้องผ่าน User Roles Access — แก้ได้เฉพาะ Finance Lead/Admin
- **DOA ENC:** การ "บันทึกการเปลี่ยน config" ควรผ่าน DOA (approval placeholder — wire เมื่อ DOA พร้อม)
- **Data Classification:** ค่า config = **Internal** (default)
- **Audit:** ทุกการเปลี่ยน config บันทึก before/after + ผู้แก้ + เวลา (immutable log)
- **เวอร์ชัน:** config มี version (เช่น v1.4) bump เมื่อบันทึก — feature ปลายน้ำควร log ว่า enforce ด้วย config version ไหน

---

## 10. หมายเหตุการใช้เอกสารนี้ใน session อื่น

เมื่อจะทำ **PR / PO / GRN / Invoice / Payment** ใน session ใหม่:
1. แนบเอกสารนี้เป็น context
2. ระบุว่ากำลังทำ feature อะไร → ดู §7 ว่าต้อง enforce config key ไหนบ้าง
3. ใช้ key name ตาม §2 ตรง ๆ (อย่าตั้งชื่อใหม่)
4. action BLOCK/WARN ตามที่ระบุในแต่ละ policy — อย่าสลับ
5. เรื่องที่อยู่นอก scope (payment term, approval, contract) → อ้างอิง §8 ไปดึงจากที่ถูกต้อง

> **Pipeline เอกสารของ Purchase Config:** HTML ✅ → **Bible (เอกสารนี้)** → BRD → FRD → QA
