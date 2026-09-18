# CSQ_BRIEF — F-PUR-PR · PR ใบขอซื้อ
> ใบประกาศ event → ท่อ 7C · ระบบ auto-register ตอน deploy · feature ประกาศเท่านั้น ห้าม hardcode การประทับผลรายท่อ

## §1 Identity
| key | value |
|---|---|
| profile_id | `CSQ-PR` |
| feature_code | F-PUR-PR (F072) · module Purchase |
| กลุ่ม | A (feature ใหม่ · ประกาศพร้อมพัฒนา) |
| version | 1.0 (2026-09-10 · Phase A direction) |

## §2 Declared Events
| event_id | trigger point (อ้าง PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|
| `doc.approved` | §2 state machine: PENDING_APPROVAL→APPROVED (ครบทุก slot) | **EC** | ทุกครั้งที่ใบอนุมัติครบ | `pr_no · grand_total · currency · cost_center_id · pr_type · requester_id · approved_at` |
| `doc.cancelled` | §2: APPROVED→CANCELLED (SC-09) | **EC** | ยกเลิกใบที่เคยอนุมัติแล้วเท่านั้น (ยกเลิกจาก DRAFT ไม่ยิง) | `pr_no · grand_total · cancel_reason · cancelled_at` |

### kind ของมูลค่า (เฉพาะ event ที่ยิง EC)
| event | kind | เหตุผล |
|---|---|---|
| `doc.approved` | `estimated` | PR อนุมัติ = ความตั้งใจจะซื้อ · ยังไม่ผูกพันจริง (ผูกพันเกิดที่ PO) · ราคาเป็น "ราคาประมาณ" |
| `doc.cancelled` | `avoided` | หยุดก่อนออก PO = ประหยัดที่เกิดจากการหยุด |
> basis = `declared` (มาจากราคาประมาณที่ผู้ขอกรอก · ไม่ใช่ราคาจริงจากผู้ขาย) — **feature ไม่คำนวณมูลค่าเอง** ENG-CSQ-02 ทำ

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — สำคัญ กันโดน reject 422
| ท่อ | สถานะ | เหตุผล |
|---|---|---|
| **OC** | ❌ ไม่ประกาศ | Operation Process (`sow.*`) เป็นเจ้าของท่อ OC เจ้าเดียว — ประกาศซ้ำ = reject |
| **DC** | ❌ ไม่ประกาศ | DC ระดับเอกสารมาจาก **DOA engine** อัตโนมัติ (การอนุมัติ/เซ็น) · PR ไม่มี terminal decision อื่นนอกจากการอนุมัติ |
| **SC** | ❌ ไม่ประกาศ | สงวนไว้ · `trigger=false` เสมอ (OQ-C3 ยังไม่เคาะ) |
| **SecC** | ❌ no-effect | PR ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย (vendor/ราคา/วงเงินเครดิต ไม่ได้แก้ที่นี่) |
| **AC** | ❌ no-effect | PR ไม่ทำให้เกิดรายการทางบัญชี (ตั้งหนี้เกิดที่ AP Invoice W5) |
| **FC** | ❌ no-effect **รอบนี้** | commitment เกิดที่ PO (W3) · การตรวจงบรอบนี้เป็น **mock** (`TODO: budget-control hook` F117 W7) — ยังไม่ทำให้งบเปลี่ยนจริง ⇒ **ห้ามประกาศ FC ใน Phase A** · ทบทวนอีกครั้งเมื่อ W7 พร้อม |
| **RC** | ❌ no-effect | ไม่เกี่ยวข้อง |

## §4 Payload Contract
| field | type | มาจาก (entity) | Restricted / mask |
|---|---|---|---|
| pr_no | string | pr_header.pr_no | — |
| grand_total | decimal | pr_header.grand_total | — |
| currency | string | pr_header.currency (THB) | — |
| cost_center_id | string (nullable) | pr_header.cost_center_id | — soft-ref |
| pr_type | enum | pr_header.pr_type | — |
| requester_id | string | pr_header.requester_id | — |
| approved_at / cancelled_at | timestamp | pr_header | — |
| cancel_reason | text | pr_header.cancel_reason | — |
> ทุก field มีอยู่จริงใน PREBRIEF §4 Data ✓ ไม่มีการแต่ง field ใหม่ ✓

## §5 Register Checklist
- [ ] event_id ทั้ง 2 ตัวใช้คำใน contract (`doc.approved` / `doc.cancelled`) ไม่คิดคำใหม่ ✓
- [ ] ไม่มี OC / DC / SC ในใบนี้ ✓ (กัน 422)
- [ ] payload ทุก field ตรง 04_DB ตอน Phase B ออก FRD
- [ ] trigger point อ้าง `03_LOGIC §` ได้จริง — Phase B ต้อง map จาก PREBRIEF §2 → FRD 03_LOGIC

## §6 Open Questions
| OQ | เรื่อง | ใครตอบ |
|---|---|---|
| OQ-CSQ-1 | เมื่อ F117 Budget Control (W7) live แล้ว PR ต้องยิง **FC** (soft-commit) ด้วยไหม | เจ้าของ 7C + Budget owner |
| OQ-CSQ-2 | มูลค่า EC ของ PR ควรใช้ราคาประมาณของผู้ขอ หรือรอราคาจาก Compare Vendors | เจ้าของ 7C |
