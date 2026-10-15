# CSQ_BRIEF — F-PUR-PO · PO ใบสั่งซื้อ

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
| profile key | `CSQ-PUR-PO` |
| feature_id | `F-PUR-PO` (fid F078) |
| ชื่อ | PO ใบสั่งซื้อ |
| module | Purchase (PUR) |
| register status | `pending` |

---

## 2. Event ที่ประกาศ (เฉพาะ transition ที่ "จบแล้วมีผล")

> ❌ ไม่ประกาศ `draft → pending_approval` — ไม่มีผลทางธุรกิจ
> ❌ ไม่ประกาศ event การอนุมัติ/ปฏิเสธเอง — DOA engine เป็นเจ้าของ (DC ระดับเอกสาร)

| # | event_id | Trigger (อ้าง PREBRIEF) | ท่อที่กระทบ | kind / basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | `po_approved` | `draft → approved` (§5 · S-04) | **FC** (เงินสด/งบ) · **EC** (ต้นทุน/มูลค่า) | `estimated` — ผูกพันแล้วแต่ยังไม่จ่ายจริง | ทุกใบที่อนุมัติครบสาย |
| 2 | `po_commitment_released_cancel` | `→ cancelled` (§5 · S-13) | **FC** · **EC** | `avoided` — ปลดภาระผูกพันเพราะหยุด | เฉพาะใบที่เคย `approved` แล้ว (ใบ `draft` ไม่เคยผูกพัน → ไม่ยิง) |
| 3 | `po_commitment_released_shortclose` | `partially received → closed` โดยคน (§5 · S-12) | **FC** · **EC** | `avoided` — ปลดเฉพาะ**ส่วนค้างรับ**ที่ถูกยกเลิก | เฉพาะใบ short-close · มูลค่า = Σ (คงเหลือรับ × ราคาสุทธิ) |
| 4 | `po_commitment_adjusted` | แก้ใบหลังอนุมัติแล้ว re-approve สำเร็จ (§5 · S-08) | **FC** · **EC** | `estimated` — ปรับยอดผูกพัน (delta ใหม่ − เดิม) | เฉพาะกรณียอดสุทธิเปลี่ยน |
| 5 | `po_commitment_consumed` | `sent/partially received → closed` จากการรับครบ (§5 · S-10) | **FC** | `estimated` → ปิดยอดผูกพัน | ภาระผูกพันแปลงเป็นของจริงฝั่ง GRN/Invoice — **PO แค่ปิดยอด** |

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (ต้องเขียนชัด กันประกาศซ้ำ)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — PO ไม่ใช่ต้นทาง OC |
| **DC** (Decision) | ❌ ไม่ | การอนุมัติ/ปฏิเสธ PO = **DC ระดับเอกสาร** ที่ DOA engine ยิงเองอยู่แล้ว · PO ไม่มี terminal decision นอกเหนือการเซ็นอนุมัติ |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ |
| **SecC** (Security) | ❌ ไม่ | PO ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย — Vendor Master เป็นคนละ feature (เจ้าของท่อ SecC ของข้อมูลผู้ขาย) |
| **AC** (Accounting) | ❌ ไม่ | **PO ไม่ post บัญชี** — commitment ≠ actual · รายการบัญชีเกิดที่ GRN/AP Invoice (W5) · `TODO: JE posting` ไม่ใช่ของ PO |

---

## 4. Payload contract (field ที่ต้องมีจริงใน entity — ตรวจกับ PREBRIEF §3)

| field | ที่มา | หมายเหตุ |
|---|---|---|
| `ref` = `po_id` | header | soft-reference ทุก event |
| `po_no` | doccfg `PO-YYYY-NNNN` | ปี **ค.ศ.** |
| `vendor_ref` | ผู้ขาย (soft-ref LD-4C-02) | nullable-safe |
| `net_amount` | ยอดสุทธิ (§3.3) | หน่วยบาท |
| `open_commitment_amount` | `Σ (คงเหลือรับ × ราคาต่อหน่วยสุทธิ)` (§3.3) | ใช้กับ event 3 และ 5 |
| `delta_amount` | ยอดใหม่ − ยอดเดิม | เฉพาะ event 4 |
| `cost_center_ref` · `budget_ref` | soft-ref / **mock** | `TODO: budget-control hook` |
| `occurred_at` | timestamp (**ค.ศ.**) | ทุก event |
| `actor` | ผู้กดทำ transition | ทุก event |

> ⚠️ ทุกค่ามูลค่าเป็น `basis: computed` จาก field ที่มีจริงในใบ — **feature ห้ามตีมูลค่าเพิ่มเอง** ENG-CSQ-02 เป็นคนประเมิน

---

## 5. HTML/FRD Injection note

- HTML **ไม่ต้องวาด UI ประเมินผลกระทบ** — Engine เป็นคนประทับ · feature แค่รู้ว่า emit ตอนไหน
- จุด emit = transition ตาม §2 เท่านั้น (ตรงกับ state machine PREBRIEF §5)
- ในโค้ด Phase A ใส่เป็น mock + คอมเมนต์ `// TODO: ENG-CSQ emit` ที่ transition ที่เกี่ยว
- FRD Phase B: `05_RULES.md` เพิ่มหัวข้อ "ผลกระทบ 7C" ชี้มาที่ไฟล์นี้

---

## 6. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| CSQ-Q1 | `po_commitment_adjusted` — ควรยิงเป็น delta หรือยิงยอดเต็มใหม่แล้วให้ engine หักเอง | เจ้าของ F-CSQ-01 |
| CSQ-Q2 | ตอน `po_approved` ควรแยก FC (กันงบ) ออกจาก EC (ต้นทุนคาดการณ์) เป็นคนละ event ไหม | เจ้าของ F-CSQ-01 + Strike |
| CSQ-Q3 | ถ้า Budget Control (W7) มาแล้ว FC จะถูกยิงจาก PO หรือจาก Budget Control — กันนับซ้ำ | เจ้าของ F117 + F-CSQ-01 |
