# 02 · API — F-PUR-COMPARE-001

**base:** `/api/purchase/compare` · auth: session ปกติของระบบ · ทุก response เป็น JSON
**หลักการ:** ยอดเงินทุกตัว **คำนวณฝั่ง server เสมอ** (`03_LOGIC §1–2`) — ค่าที่ client ส่งมาใช้แค่ `unit_price` · `discount_pct` · `vat_mode` · `vat_pct` · `available`

## §1 คิวงาน

### `GET /queue`
| query | ชนิด | หมายเหตุ |
| --- | --- | --- |
| `q` | string | ค้นเลขที่ใบขอซื้อ / ชื่อรายการ |
| `status` | enum | `no_round` · `open` · `comparing` · `awarded` |
| `dept` | string | หน่วยงาน |

```jsonc
200 {
  "rows": [{
    "pr_id": "PR-2026-0006", "dept": "ฝ่ายบัญชีและการเงิน",
    "line_count": 2, "est_amount": 13500.00,
    "approved_at": "2026-09-05", "age_days": 5,
    "round": { "round_id": "…", "round_seq": 1, "status": "comparing", "quote_count": 3 }
  }],
  "total": 3
}
```
> `round` เป็น `null` เมื่อยังไม่เปิดรอบ · **คืนเฉพาะใบขอซื้อที่อนุมัติแล้ว** (BR-01 / C-01)

## §2 รอบเทียบราคา

| method | path | ทำอะไร | กติกา |
| --- | --- | --- | --- |
| `POST` | `/rounds` | เปิดรอบจากใบขอซื้อ · body `{pr_id}` | C-01 · สร้าง `pr_snapshot` · ห้ามเปิดซ้อนกับรอบที่ยังไม่ปิด |
| `GET` | `/rounds/{round_id}` | หัวรอบ + ใบเสนอราคา + ตารางเทียบ + ประวัติ | |
| `POST` | `/rounds/{round_id}/award` | ยืนยันผล → ล็อก | BR-04 · BR-05 · LD-06 |
| `POST` | `/rounds/{round_id}/cancel` | ยกเลิกรอบ · body `{reason}` | V-05 |
| `POST` | `/rounds/{round_id}/reopen` | เปิดรอบใหม่จากรอบที่ตัดสินแล้ว | คัดลอกใบเสนอราคาเดิม · `prev_round_id` |

### `POST /rounds/{round_id}/award`
```jsonc
// request
{ "award_mode": "whole",            // หรือ "split"
  "whole_vendor_id": "V-0012",      // เมื่อ whole
  "lines": { "1": "V-0007", "2": "V-0012" },   // เมื่อ split
  "reason": "ส่งมอบเร็วกว่า 6 วัน คุ้มกับส่วนต่างราคา",
  "row_version": 4 }

// 200
{ "round_id": "…", "status": "awarded",
  "awarded_total": 13161.00, "lowest_total": 13011.20, "is_lowest": false,
  "award_lines": [ { "pr_line_no": 1, "winner_vendor_id": "V-0012", "winner_unit_price": 108.50,
                     "line_total": 4643.80, "is_lowest": true } ],
  "awarded_at": "2026-09-13T10:22:41Z" }
```
**server ต้องตรวจซ้ำทุกข้อ ห้ามเชื่อ client:** คำนวณ `bestTotal`/`bestUnit` ใหม่ → สรุป `needReason` เอง → ถ้า `needReason` และ `trim(reason).length < 3` ตอบ `E-CMP-422-REASON`

## §3 ใบเสนอราคา

| method | path | กติกา |
| --- | --- | --- |
| `POST` | `/rounds/{round_id}/quotes` | BR-02 ผู้ขายซ้ำในรอบไม่ได้ · V-01 · V-02 |
| `PUT` | `/quotes/{quote_id}` | เฉพาะรอบที่ยังไม่ `awarded` (BR-05) |
| `DELETE` | `/quotes/{quote_id}` | เฉพาะก่อน `awarded` · ลบใบสุดท้าย → รอบกลับเป็น `open` |

```jsonc
// POST/PUT body
{ "vendor_id": "V-0007", "vendor_quote_no": "OM-6621",
  "quote_date": "2026-09-08", "valid_until": "2026-09-30",
  "payment_term": "เครดิต 30 วัน", "lead_time_days": 5,
  "warranty": "เปลี่ยนสินค้าชำรุดภายใน 7 วัน", "note": "",
  "lines": [ { "pr_line_no": 1, "available": true, "unit_price": 112.00,
               "discount_pct": 0, "vat_mode": "add", "vat_pct": 7 },
             { "pr_line_no": 2, "available": false } ] }
```
response คืนยอดที่ server คำนวณ: `subtotal` · `vat_amount` · `grand_total` · `missing` · `complete` · `is_expired`

## §4 ตารางเทียบ

### `GET /rounds/{round_id}/matrix`
```jsonc
{ "columns": [ { "vendor_id":"V-0007", "vendor_name":"บจก. ออฟฟิศเมท ซัพพลาย",
                 "is_expired": false, "complete": true } ],
  "rows": [ { "pr_line_no":1, "item_name":"กระดาษถ่ายเอกสาร A4 80 แกรม", "qty":40, "uom":"รีม",
              "cells": [ { "vendor_id":"V-0007", "available":true, "unit_price":112.00,
                           "line_total":4793.60, "is_best_unit":false } ],
              "last_purchase_price": 115.00 } ],
  "summary": { "grand_total": {...}, "diff_from_lowest": {...}, "payment_term": {...},
               "lead_time_days": {...}, "warranty": {...}, "valid_until": {...} } }
```
`is_best_unit` / `is_best_*` **server เป็นคนตัดสิน** ด้วย epsilon `0.005` (`03_LOGIC §3`) — หน้าจอแค่ทาสี

## §5 ไฟล์แนบ *(ยังไม่ได้ทำใน HTML — WARN-2 / TD-05)*

| method | path | หมายเหตุ |
| --- | --- | --- |
| `POST` | `/quotes/{quote_id}/attachments` | `multipart/form-data` · ชนิดที่รับ: pdf · jpg · png · xlsx · จำกัด 10 MB/ไฟล์ |
| `DELETE` | `/attachments/{attachment_id}` | เฉพาะก่อน `awarded` |

## §6 จุดเชื่อมใบสั่งซื้อ — `[ASSUMED contract]` (A-01 · LD-09)

### `GET /rounds/{round_id}/po-handoff`
```jsonc
{ "round_id":"…", "pr_id":"PR-2026-0006",
  "groups": [ { "vendor_id":"V-0012", "lead_time_days":9,
                "lines":[{"pr_line_no":1,"item_id":"IT-1001","qty":40,"uom":"รีม",
                          "unit_price":108.50,"discount_pct":0,"vat_mode":"add","vat_pct":7}] } ] }
```
> **อ่านอย่างเดียว** — ฟีเจอร์นี้ไม่สร้างใบสั่งซื้อ ไม่เรียก API ของ W3 (LD-09)
> รูปแบบนี้ยังไม่ได้ตกลงกับเจ้าของ W3 — **A-01 ยังเปิดอยู่**

## §7 Error catalog

| code | HTTP | เมื่อไร | ข้อความบนจอ |
| --- | --- | --- | --- |
| `E-CMP-404-ROUND` | 404 | ไม่พบรอบ | "ไม่พบรอบเทียบราคานี้" |
| `E-CMP-409-LOCKED` | 409 | แก้รอบที่ `awarded`/`cancelled` | "รอบนี้ปิดแล้ว ต้องการเปลี่ยนต้องเปิดรอบใหม่" |
| `E-CMP-409-VERSION` | 409 | `row_version` ไม่ตรง (EC-08) | "มีคนแก้ข้อมูลนี้ไปแล้ว กรุณาโหลดใหม่" |
| `E-CMP-409-DUP-VENDOR` | 409 | BR-02 ผู้ขายซ้ำในรอบ | "ผู้ขายรายนี้มีใบเสนอราคาในรอบนี้แล้ว" |
| `E-CMP-409-OPEN-ROUND` | 409 | เปิดรอบซ้อน | "ใบขอซื้อนี้มีรอบที่ยังไม่ปิดอยู่แล้ว" |
| `E-CMP-422-REASON` | 422 | BR-04 · V-04 | "ต้องระบุเหตุผลอย่างน้อย 3 ตัวอักษร" |
| `E-CMP-422-NO-PRICE` | 422 | V-02 | "ต้องมีอย่างน้อย 1 รายการที่ผู้ขายเสนอราคามากกว่า 0" |
| `E-CMP-422-INCOMPLETE` | 422 | V-03 เลือกผู้ชนะไม่ครบ / ใบไม่ครบในโหมดทั้งใบ | "ยังเลือกผู้ชนะไม่ครบทุกรายการ" |
| `E-CMP-403-ROLE` | 403 | C-09 ไม่มีสิทธิ์ | "คุณมีสิทธิ์ดูอย่างเดียว" |
| `E-CMP-409-PR-CANCELLED` | 409 | SC-15 ใบขอซื้อถูกยกเลิก | "ใบขอซื้อนี้ถูกยกเลิกแล้ว — ยืนยันผลไม่ได้ แนะนำให้ยกเลิกรอบ" |
| `E-CMP-400-PR-NOT-APPROVED` | 400 | BR-01 · C-01 | "เปิดรอบได้เฉพาะใบขอซื้อที่อนุมัติแล้ว" |

## §8 API ที่ **ไม่มี** และเหตุผล
- ❌ `/submit` · `/approve` · `/reject` — ไม่มีสายอนุมัติ (LD-02)
- ❌ `/next-number` — ไม่มีเลขที่เอกสาร (LD-03)
- ❌ `/print` · `/pdf` — ไม่มีแบบพิมพ์ (LD-01)
- ❌ `/notify` — ไม่ประกาศ event แจ้งเตือน
