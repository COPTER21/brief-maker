# AI DEFAULTS + OPEN QUESTIONS · Payment Term (F-PAY)

> ทุกอย่างที่ไม่ชัดจากต้นทาง = ตั้ง `[AI-DEFAULT]` ที่นี่ ไม่คิด scope เอง · ไม่ปิด OQ เอง
> ยกให้ user เคาะที่ gate · propagate ค่า default เดียวกันข้ามทุก artifact (BRD→FRD→TC)

## Open Questions (สืบทอดจาก PREBRIEF §10 — ยังไม่ปิด)
| # | ประเด็น | เจ้าภาพ | สถานะ |
|---|---------|---------|-------|
| OQ-PAY-01 | full_postpay ≈ credit ที่ due_basis=delivery — คงตาม LD-02 หรือยุบ | Strike | 🔵 pin |
| OQ-PAY-02 | ส่วนลดจ่ายเร็ว 1 ช่วง (SAP ได้ 3) — พอสำหรับ SME? | Strike | 🔵 pin |
| OQ-PAY-03 | Vendor/Customer master ต้องมี field payment_term override default — เพิ่มตอนทำ master คู่ค้า | BA (edge) | 🔵 pin |
| OQ-PAY-04 | มัดจำ: ใบกำกับภาษี ณ จุดรับเงิน + บัญชีมัดจำ — ยืนยัน flow กับ Accounting | Strike/บัญชี | 🔵 pin |
| OQ-PAY-05 | ไม่ล็อกแก้เงื่อนไขเมื่อ used>0 (ต่างจาก Tax) เพราะเอกสาร snapshot แล้ว — ยืนยันหลักการ | Strike | 🔵 pin `[AI-DRAFT]` |
| OQ-PAY-06 | FRD pack v5.1 **stale** → regen จาก HTML + register ENG-PT-01/02 กับ Architect | BA | 🟡 จะแก้ที่ step 6 |
| OQ-PAY-07 | `used` เป็น mock — จริงต้องนับจากเอกสารทุกใบที่อ้าง | FRD | 🟡 spec ที่ step 6 |
| **OQ-PAY-08** | source contradiction: PR ใน use_in (LD-01/FN-40 ตัด vs OB-2/FN-10 มี) | PM/BA | ✅ **CLOSED (2026-08-10): PM/BA = "ถอด PR" — payment term ไม่ผูกที่ PR** · use_in เหลือ 7 |

## [AI-DEFAULT] — ค่าที่ AI ตั้งไว้ (รอ user ยืนยัน)
| # | จุด | ค่า default ที่ตั้ง | เหตุผล |
|---|-----|--------------------|--------|
| AD-01 | หลักการ used>0 | **แก้ไขได้ · ลบไม่ได้** (snapshot ที่เอกสาร) | ตาม OQ-PAY-05 [AI-DRAFT] + BR-08 |
| AD-02 | ส่วนลดจ่ายเร็ว | รองรับ **1 ช่วง** | ตาม HTML as-built (OQ-PAY-02) |
| AD-03 | multi-currency | ไม่รองรับ (THB สมมติ) | ไม่มีใน scope ต้นทาง |

## Step-1 conformance decisions (ตั้งเป็น default — surgical เท่านั้น ไม่เปลี่ยน behavior)
| # | จุด | ตัดสิน | เหตุผล |
|---|-----|--------|--------|
| CF-01 | dead CSV CSS (`.import-drop` / `.mode-opt` / `.modal.is-lg` ฯลฯ) | **ลบทิ้ง** | CSV ถูกตัดออก (มติ 2026-08-09) — CSS ค้างไม่มีคนใช้ |
| CF-02 | comment "6 Payment Types" (บรรทัด ~770) | **แก้เป็น 7** | จริงมี 7 ประเภท — comment stale |
| CF-03 | drawer width 540px | **540 → 680 (.standard)** ✅ แก้แล้ว | ⚠️ default เดิม "คง 540" ถูก **override โดย audit** — v8 Iron Rule #11 hard-FAIL ที่ 540px · 680 (.standard) = ค่าถูกต้องสำหรับฟอร์ม master (920 สงวนให้ B2 line editor) · แก้ทั้ง base + media query |
| CF-04 | body min-width 1180 + #97 media query | ยืนยันคง (responsive 768–1180) | ตรง #97 |

## Step-1 audit result (v8 audit.sh)
- **ก่อนแก้:** FAIL=3 (Rule #25 createIcons · #49 scrollbar · #11 drawer 540) · WARN=4
- **หลังแก้:** **FAIL=0** · WARN=3 (ปล่อยให้ qc-ux step 3 ตัดสิน — cosmetic, ไม่กระทบ behavior)
- WARN ที่เหลือ: (1) Rule #21 sidebar icons ไม่มี class w/h (global CSS คุม size อยู่แล้ว) · (2) Token hardcoded font-size (legacy) · (3) Rule #44 submit ไม่มี loading state (mock submit synchronous — การเพิ่ม loader = แตะ behavior จึงเลื่อนให้ qc-ux ตัดสิน)

> ⚠️ conformance pass = surgical เท่านั้น — **ไม่แตะ** logic/validation/mock/behavior ที่ผ่าน E2E แล้ว (ยืนยัน: แก้เฉพาะ CSS + 1 comment + createIcons→renderIcons wrapper)
