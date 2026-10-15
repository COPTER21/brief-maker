# CSQ_BRIEF — F-PUR-COMPARE · เทียบราคาผู้ขาย
> ใบประกาศ event → ท่อ 7C · ระบบ auto-register ตอน deploy · feature ประกาศเท่านั้น ห้าม hardcode การประทับผลรายท่อ

## §1 Identity
| key | value |
|---|---|
| profile_id | `CSQ-CMP` |
| feature_code | F-PUR-COMPARE (F073) · module Purchase |
| กลุ่ม | A (feature ใหม่ · ประกาศพร้อมพัฒนา) |
| version | 1.0 (2026-09-10 · Phase A direction) |

## §2 Declared Events
| event_id | trigger point (อ้าง PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|
| `master.changed` | §2 state machine: COMPARING→**AWARDED** (ยืนยันผลการเลือก · FN-18) | **DC** | ทุกครั้งที่รอบถูกตัดสิน | `round_id · pr_id · award_mode · winner_vendor_ids[] · awarded_total · lowest_total · is_lowest · award_reason · awarded_at` |
| `doc.cancelled` | §2: OPEN/COMPARING→**CANCELLED** (FN-20) | **EC** | ยกเลิกรอบที่เปิดแล้ว | `round_id · pr_id · quote_count · cancel_reason · cancelled_at` |

### เหตุผลที่ `master.changed` ยิง **DC** ได้ (ไม่ชนกฎ G2)
DC ที่ห้ามประกาศคือ DC ที่มาจาก **การอนุมัติ/เซ็นเอกสาร** ซึ่ง DOA engine ยิงให้เอง —
ฟีเจอร์นี้ **ไม่มีสายอนุมัติเลย** (chip มีแค่ `csq`) การ "ตัดสินผู้ชนะ" จึงเป็น **terminal decision ของกระบวนการ**
(Continue/Adjust/Stop) ที่ไม่ใช่การเซ็นอนุมัติ → เข้าเกณฑ์ DC ตาม §Trigger Rule แถว "มีการตัดสินใจปลายทาง"

### kind ของมูลค่า (เฉพาะ event ที่ยิง EC)
| event | kind | เหตุผล |
|---|---|---|
| `doc.cancelled` | `avoided` | ยกเลิกรอบก่อนออกใบสั่งซื้อ = หยุดก่อนผูกพัน |
> basis = `declared` (จากราคาที่บันทึกในใบเสนอราคา) — feature ไม่คำนวณมูลค่าเอง ENG-CSQ-02 ทำ

## §3 ท่อที่ไม่ประกาศ (และเหตุผล)
| ท่อ | สถานะ | เหตุผล |
|---|---|---|
| **OC** | ❌ ไม่ประกาศ | Operation Process (`sow.*`) เป็นเจ้าของท่อ OC เจ้าเดียว |
| **SC** | ❌ ไม่ประกาศ | สงวนไว้ · `trigger=false` เสมอ |
| **SecC** | ❌ no-effect | ไม่แก้ข้อมูลอ่อนไหว ไม่เปลี่ยนสิทธิ์/นโยบาย · ราคาที่บันทึกเป็นของรอบเทียบ ไม่ใช่การแก้ทะเบียนผู้ขาย |
| **AC** | ❌ no-effect | ไม่เกิดรายการทางบัญชี (เกิดที่ AP Invoice W5) |
| **FC** | ❌ no-effect | ยังไม่ผูกพันเงินสด/งบ — ผูกพันเกิดที่ใบสั่งซื้อ (W3) |
| **RC** | ❌ no-effect | ไม่เกี่ยวข้อง |
> **ห้ามประกาศ DC จากการอนุมัติซ้ำ** — ฟีเจอร์นี้ไม่มีการอนุมัติ จึงไม่มีความเสี่ยงชนกับ DOA engine

## §4 Payload Contract
| field | type | มาจาก (entity) | mask |
|---|---|---|---|
| round_id | id | cmp_round.round_id | — |
| pr_id | ref | cmp_round.pr_id (อ้างอิงอ่อน) | — |
| award_mode | enum | cmp_round.award_mode (whole\|split) | — |
| winner_vendor_ids[] | ref[] | cmp_award_line.winner_vendor_id (distinct) | — |
| awarded_total / lowest_total | decimal | คำนวณจาก cmp_award_line + cmp_quote | — |
| is_lowest | bool | cmp_award_line.is_lowest (AND ทุกบรรทัด) | — |
| award_reason / cancel_reason | text | cmp_round | — |
| quote_count | int | นับ cmp_quote ของรอบ | — |
| awarded_at / cancelled_at | timestamp | cmp_round | — |
> ทุก field มีอยู่จริงใน PREBRIEF §4 ✓ ไม่มีการแต่ง field ใหม่ ✓

## §5 Register Checklist
- [ ] event_id ใช้คำใน contract (`master.changed` / `doc.cancelled`) ✓
- [ ] ไม่มี OC / SC ✓ · DC ที่ประกาศไม่ใช่ DC จากการอนุมัติ ✓ (กัน 422)
- [ ] payload map กับ 04_DB ตอน Phase B ออก FRD
- [ ] trigger point อ้าง `03_LOGIC §` ได้จริงตอน Phase B (map จาก PREBRIEF §2)

## §6 Open Questions
| OQ | เรื่อง | ใครตอบ |
|---|---|---|
| OQ-CSQ-1 | ถ้าเลือกผู้ชนะที่ไม่ใช่ราคาต่ำสุด ควรยิง EC เพิ่มเป็น "ส่วนต่างที่ยอมจ่าย" ด้วยไหม | เจ้าของ 7C |
| OQ-CSQ-2 | เปิดรอบใหม่ (revision) ควรถือเป็น event แยกหรือไม่ | เจ้าของ 7C |
