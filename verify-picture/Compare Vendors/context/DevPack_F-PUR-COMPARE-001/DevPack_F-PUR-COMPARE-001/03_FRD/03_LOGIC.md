# 03 · LOGIC — F-PUR-COMPARE-001

> สูตรทุกข้อสกัดจาก `01_HTML/CompareVendors.html` โดยตรง (HTML-first) — อ้างบรรทัดจริงไว้ให้ตรวจย้อนได้
> **การคำนวณเงินทั้งหมดต้องทำซ้ำฝั่ง server** — client ส่งมาเท่าไรไม่เชื่อ (`04_DB §2`)

## §1 คำนวณยอดรายบรรทัด — `lineTotal()` (HTML L587–L597)

```
ถ้า available = false  →  {net:0, vat:0, total:0}      # BR-03

gross = pr_line.qty × unit_price
net   = gross × (1 − discount_pct/100)
p     = vat_pct / 100

vat_mode = 'none'      →  vat = 0            · total = net
vat_mode = 'add'       →  vat = net × p      · total = net + vat
vat_mode = 'included'  →  vat = net × p/(1+p) · total = net
```

**หมายเหตุสำคัญ:** โหมด `included` — `net` ที่เก็บคือ *ยอดรวมภาษีแล้ว* และ `vat` คือส่วนที่ถอดออกมา ดังนั้น `total = net` (ไม่บวกซ้ำ)
จำนวน (`qty`) มาจาก **ใบขอซื้อ** เสมอ ไม่ใช่จากผู้ขาย — ผู้ขายเสนอได้แค่ราคา/หน่วย

## §2 ยอดรวมทั้งใบ — `quoteTotals()` (L598–L605)

```
สำหรับทุกบรรทัดของ pr:
    ถ้าไม่มีบรรทัดนั้นในใบเสนอราคา หรือ available=false  →  missing += 1 · ข้าม
    ไม่งั้น                                              →  บวก net · vat · total

complete = (missing == 0)
```

`complete` คือหัวใจของ BR-03/BR-04: **ใบที่เสนอไม่ครบทุกรายการ จะไม่ถูกใช้เป็นฐานราคาต่ำสุด และเลือกแบบ "ทั้งใบ" ไม่ได้**

## §3 หาค่าดีที่สุด (L606–L610)

| ฟังก์ชัน | สูตร | ใช้ที่ |
| --- | --- | --- |
| `unitOf(q, no)` | คืน `unit_price` ถ้า `available` ไม่งั้น `null` | ตารางเทียบ |
| `bestUnit(r, no)` | `min(unitOf ของทุกใบ ที่ ≠ null และ > 0)` | ไฮไลต์รายแถว (FN-12) |
| `bestTotal(r)` | `min(total ของทุกใบที่ complete)` | แถวยอดสุทธิรวม + ฐานของ BR-04 |

**เกณฑ์ "เท่ากัน" ใช้ epsilon `0.005`** — `Math.abs(a−b) < 0.005` ถือว่าเท่า (SC-13 ไฮไลต์ทั้งคู่)
เหตุผล: ยอดเงินปัดที่ทศนิยม 2 ตำแหน่ง · epsilon ครึ่งสตางค์กันปัญหา floating point

## §4 ตรรกะการตัดสิน — `awardCalc()` (L808–L827)

```
bt = bestTotal(r)

โหมด whole:
    q = ใบเสนอราคาของ whole_vendor
    ถ้าไม่พบ                       → ok = false
    ถ้า !q.complete                → allLowest = false
    ถ้า |q.total − bt| > 0.005     → allLowest = false
    total = q.total

โหมด split:
    สำหรับทุกบรรทัดของ pr:
        v = ผู้ขายที่เลือกไว้ของบรรทัดนี้
        ถ้าไม่ได้เลือก / ผู้ขายไม่มีบรรทัดนี้ / available=false  → ok = false   # C-04
        total += lineTotal(...)
        ถ้า |unit_price − bestUnit(บรรทัดนี้)| > 0.005           → allLowest = false

single      = (จำนวนใบเสนอราคาในรอบ == 1)
needReason  = (!allLowest) OR single                    # ★ BR-04
isLowest    = allLowest AND !single
```

**ปุ่ม "ยืนยันผลการเลือก" เปิดเมื่อ:** `ok AND (!needReason OR trim(reason).length ≥ 3)` (HTML L865)

### ยืนยันเชิงกล (จาก re-gate 2026-09-13)
| สถานะ | ผู้ขาย | เหตุผล | ปุ่ม |
| --- | --- | --- | --- |
| ต่ำสุดที่เสนอครบ (฿13,011.20) | ออฟฟิศเมท | ว่าง | เปิด |
| ไม่ใช่ต่ำสุด (฿13,161.00) | ไทยเปเปอร์ | ว่าง | **ปิด** + แถบเตือนบอกส่วนต่าง ฿149.80 |
| ไม่ใช่ต่ำสุด | ไทยเปเปอร์ | `"ส"` | **ปิด** |
| ไม่ใช่ต่ำสุด | ไทยเปเปอร์ | ≥3 ตัวอักษร | เปิด |
| ใบไม่ครบ (฿4,922.00) | เอ็นเทค | — | **ปิด** (`ok=false`) |

## §5 State machine + trigger point ของ 7C

```
                ┌──────────── บันทึกใบเสนอราคารายแรก ───────────┐
    [เปิดรอบ open] ──────────────────────────────────────► [กำลังเทียบ comparing]
         │                                                        │
         │                            ┌── ลบใบเสนอราคารายสุดท้าย ──┘
         │                            ▼
         │                       [เปิดรอบ open]
         │                                                        │
         │  ยกเลิกรอบ + เหตุผล                   ยืนยันผล + เหตุผลครบ │
         ▼                                                        ▼
   [ยกเลิก cancelled]                                    [ตัดสินแล้ว awarded]  ← ล็อกถาวร (LD-06)
                                                                  │
                                              เปิดรอบใหม่ (round_seq+1, prev_round_id)
                                                                  ▼
                                                          [กำลังเทียบ comparing]
```

| transition | ผลข้างเคียง | event 7C | ท่อ |
| --- | --- | --- | --- |
| `comparing → awarded` (`doAward()` L1023) | เขียน `cmp_award_line` ทุกบรรทัด · ล็อกรอบ · `pushHist('awarded')` | **`master.changed`** | **DC** |
| `open\|comparing → cancelled` (`doCancelRound()` L1057) | บันทึก `cancel_reason` · `pushHist('cancelled')` · ใบขอซื้อกลับเข้าคิว | **`doc.cancelled`** (kind `avoided`) | **EC** |
| `awarded → (รอบใหม่) comparing` (`confirmReopen()` L995) | สร้างรอบใหม่ `round_seq+1` · คัดลอกใบเสนอราคาเดิม · อ้าง `prev_round_id` | — (OQ-CSQ-2) | — |
| `* → *` ทุกครั้ง | `pushHist()` L612 | — | — |

> **payload ของทั้งสอง event อยู่ที่ `CSQ_BRIEF_F-PUR-COMPARE-001.md §2/§4`** — ห้าม hardcode การประทับผลรายท่อในฟีเจอร์
> ไม่มี event แจ้งเตือน ไม่มี event อนุมัติ (LD-02)

## §6 ประวัติ (append-only) — `pushHist()` (L612)
เขียนทุกเหตุการณ์: `round_opened` · `quote_added` · `quote_updated` · `quote_deleted` · `awarded` · `cancelled` · `reopened`
**ไม่มีเส้นทางลบ** (LD-07) · บนจอหัวข้อเขียนไว้ชัด: *"ประวัติ (บันทึกเพิ่มอย่างเดียว · แก้ไข/ลบไม่ได้)"*

## §7 ตรรกะที่ **ยังไม่ได้ทำ** ใน HTML (ต้องทำจริงใน Phase B)

| # | ตรรกะ | สถานะในไฟล์ | ต้องทำ |
| --- | --- | --- | --- |
| L-1 | **สิทธิ์ตามบทบาท (SC-11)** | ไม่มีตัวแปรเลย (`role` · `perm` · `canEdit` · `readonly` · `viewer` = 0 ทุกคำ) | ตาม `05_RULES` C-09 — ผู้ขอซื้อ/ผู้ตรวจสอบเห็นจอแต่ปุ่มบันทึก/ยืนยัน/ยกเลิกไม่ขึ้น |
| L-2 | **ใบขอซื้อถูกยกเลิกหลังเปิดรอบ (SC-15)** | `const prCancelled=false;` L939 — ประกาศแล้วไม่มีที่ไหนอ่าน | แถบเตือนที่หัวคอนโซล · ปิดปุ่มยืนยันผล · แนะให้ยกเลิกรอบ |
| L-3 | **แก้พร้อมกัน (EC-08)** | ไม่มี | `row_version` optimistic lock — คนแรกชนะ คนที่สองได้ `E-CMP-409` |
| L-4 | **อัปโหลดไฟล์จริง** | `addQuoteFile()` L1145 เพิ่มรายการในหน่วยความจำ | ตาม `02_API §5` |
