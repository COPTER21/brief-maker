# 02_API — F-AGM-012 Cane Payment Setting

> REST `/api/cane-payment/settings` · headers: X-Idempotency-Key, If-Match(ETag), X-Trace-Id · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /cane-payment/settings?seasonId= | อ่าน setting ตามรอบหีบ (+ green/white schedules) |
| API-02 | GET | /cane-payment/settings/:id | detail |
| **API-03** | PUT | /cane-payment/settings/:id | บันทึก setting (If-Match) → คำนวณ dailyRate + save |
| API-04 | POST | /cane-payment/settings | สร้าง (season+product) |
| API-05 | POST | /cane-payment/settings/:id:duplicate | คัดลอก (Idempotency-Key) |
| API-06 | POST | /cane-payment/settings/:id:deactivate | ปิดใช้งาน (If-Match) |
| API-CH | GET/POST/PUT/DELETE | /settings/:id/charges | รายการหักเพิ่มเติม |
| API-GS | GET/POST/PUT/DELETE | /settings/:id/green-schedules | ตารางบิลเขียว |
| API-WS | GET/POST/PUT/DELETE | /settings/:id/white-schedules | ตารางบิลขาว |
| **API-EXT** | GET | /payment-settings/active?season=&product= ⭐ | (Cane Payment อ่าน active setting) |
| API-SEASON/PROD/PRICE | GET | /crushing-seasons · /products?type=cane · /price-lists/:productId | masters (Base @10CCS) |
| API-AUDIT | POST | /audit-logs | audit (create/update/duplicate/deactivate) |

## §2.X Contracts ⭐
- **API-03 (save):** If-Match(ETag) optimistic · payload มี interest{rateYear, baseDays} + bankFee{mainProvinceCode, inProvinceFee, outProvinceFee} + kValue + vat + greenSchedules[] + whiteSchedules[] · **BE คำนวณ dailyRate = roundUp(rateYear/baseDays, 7)** ก่อนเก็บ · validate: no-overlap ต่อ (setting, month_year); FIXED_DATE ⇒ payDate; WITH_CANE ⇒ payDate null; rate_year>0; base_days>0; unique Active per season×product
- **API-EXT (Cane Payment read):** คืน active setting เท่านั้น (status=Active) — kValue, base, interest, bankFee, charges[], greenSchedules[], whiteSchedules[], vat
- **API-05 (duplicate):** target season/product · month-adjust payout · unique Active (409 ถ้าซ้ำ)
- **All mutations:** audit log (before/after) + optimistic lock

## §2.2 ตัวอย่าง
```
PUT /api/cane-payment/settings/1   (If-Match: "etag-x")
{ "productId":10,"basePriceCcs10":900.0,
  "interest":{"rateYear":7.0,"baseDays":365},
  "bankFee":{"mainProvinceCode":"44","inProvinceFee":5.0,"outProvinceFee":15.0},
  "greenSchedules":[{"monthYear":"2025-12-01","fromDay":1,"toDay":15,"payDateInst1":"2025-12-22","payDateInst2":"2026-01-22"}],
  "whiteSchedules":[{"monthYear":"2025-12-01","fromDay":1,"toDay":7,"payType":"FIXED_DATE","payDate":"2025-12-12"},
                    {"monthYear":"2025-12-01","fromDay":15,"toDay":15,"payType":"WITH_CANE","payDate":null}] }
→ 200 { ...same shape, "interest":{"rateYear":7.0,"baseDays":365,"dailyRate":0.0191781} }
```
Events: `payment_settings.created|updated|duplicated|deactivated`

## §2.3 Errors → 05_RULES §5.6
VALIDATION_FAILED · SCHEDULE_OVERLAP · INVALID_PAY_TYPE · CONFLICT(409 unique Active) · CONFLICT_UPDATE_STALE(412 ETag) · FORBIDDEN(403 RBAC)
