# PREBRIEF · Payment Term — เงื่อนไขชำระเงิน
> Sales lane · F-0.17 · จาก HTML as-built (vibe + CI rebrand v8 — 2026-08-09) + BRD/FRD pack เดิม (v5.1 — **stale**) + standard review (SAP/Odoo)
> Reverse Mode: HTML คือของจริง · Finance Foundation master ใช้ร่วม **P2P + S2C** · [AI-DRAFT] รอเคาะ
> รหัสเดิม: F-PAYMENT-TERM-001 (F-PAY)

## 0. Obligations — พันธะจากต้นทาง
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | **LD สืบทอดจาก pack (ห้ามฝืน)**: LD-01 payment term ที่ PO/SO เท่านั้น (PR ไม่มี · Quotation ฝั่งขาย = proposal) · LD-02 GRN/Ship trigger ตามประเภท (Prepay/Deposit รอชำระ · ที่เหลือทันที) · LD-05 เปลี่ยน type หลัง approve เอกสารไม่ได้ · LD-08 deposit % inherit+ปรับได้ที่ PO/SO · LD-08b Credit trigger = ทันที (locked) · LD-09 installment inherit+ปรับได้ รวม 100% · LD-10 Partial: GRN กำหนดยอดจ่ายต่อรอบ · LD-15 Installment ≠ Partial | FRD 07_LOCKED | §2, §4 |
| OB-2 | **DD สืบทอด**: 1 master ร่วม 2 ฝั่ง (trigger ตีความตามฝั่ง: P2P=GRN · S2C=Warehouse/Ship) · use_in 8 เอกสาร (PR/PO/AP Inv/PV ฝั่งซื้อ · QUO/SO/AR Inv/Receipt ฝั่งขาย) · view = drawer generic ไม่มี approver/PDF | FRD 07 DD-01..06 | §3, §9 |
| OB-3 | **Standard hooks (review 2026-08-09 — SAP/Odoo)**: ① installment → บัญชีแตก journal item ต่องวด ② มัดจำ → **ใบกำกับภาษี ณ จุดรับเงิน (VAT ไทย)** + บัญชีมัดจำ clearing ③ ส่วนลดจ่ายเร็ว → บัญชีส่วนลดรับ/จ่าย ④ default term ระดับคู่ค้า (Vendor/Customer master override) ⑤ due_basis = baseline date | BACKEND comment ในไฟล์ | §7, §9, §10 |
| OB-4 | DOA: ไม่มีสายอนุมัติ — placeholder 4 fields = null (FRD §7.5 กำหนดไว้เอง) · NOTIF: ไม่ emit | Ledger + FRD | §3.3 |
| OB-5 | ENG candidates 2 ตัว รอ register CUBIC: `installment-validator` (ENG-PT-01) · `payment-trigger-resolver` (ENG-PT-02) — **แจ้ง Architect ตอน handoff** | FRD §7.4 | §10 |
| OB-6 | Pattern เลน (VD-PDM): สถานะ 3 ค่าอิสระ · bulk · ไม่มีลบเดี่ยว · ตัด hint/field-help/panelInfo · ★ ยกเว้นของเลน: **ไม่มีนำเข้า/ส่งออก CSV** (มติ 2026-08-09 — จัดการผ่านฟอร์มเท่านั้น) | มติเลน | §2, §6 |
| OB-7 | v8 + **CI Warm Light** (ไฟล์เดิมเป็น Navy v3.9 — rebrand แล้ว): #96 full-height (.tbl-scroll) · #97 responsive 768 · #95 · Esc chain · **Iron Rule #29 scroll preservation** (_keepScroll 3 ชั้น) | มติ v8 + fix 2026-08-09 | §6 |

## 1. สรุป + ผู้ใช้
Master กลางกำหนด "เงื่อนไขการชำระเงิน" ครั้งเดียวใช้ทั้งระบบ — 7 ประเภทครอบทุกรูปแบบการค้า พร้อมกำหนด trigger คลัง (ของออก/รับเมื่อไหร่) และรายการเอกสารที่ใช้ได้ ระบบปลายทางคำนวณวันครบกำหนด + ส่วนลด + งวด อัตโนมัติ
| ประเภท | ใจความ | trigger คลัง |
|---|---|---|
| Full Prepay | จ่ายครบ 100% ก่อนส่ง | หลังชำระเต็ม |
| Full Postpay | รับของก่อน จ่ายเต็มภายใน N วันหลังรับ | ทันที |
| Deposit | มัดจำ (%/บาท/กำหนดตอนทำเอกสาร) + ส่วนเหลือ | หลังชำระมัดจำ |
| Installment | ส่งรอบเดียว แบ่งจ่าย ≥2 งวด รวม 100% | ทันที |
| Partial Delivery | ส่งหลายรอบ จ่ายตามรับจริง (invoice ต่อรอบ) | ทันที |
| Credit | N วัน + ส่วนลดจ่ายเร็ว (เช่น 2/10 Net 30) + EOM | ทันที (LD-08b locked) |
| Direct Payment | จ่ายตรงเข้า GL ไม่ผ่าน PO/SO (ค่าน้ำไฟ/สัญญา) | ไม่มี |

## 2. Scenarios (derive: D1→S-06,S-07 · D2→S-08 · D3→S-05,S-07 · D4→— master ต้นน้ำ (N/A) · D5→§9 (ปลายทางเลือกเฉพาะ active) · D6[STD]→S-09)
| S | ประเภท | ชื่อ | เกิดอะไร | ข้อมูลที่ต้องมี | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | สร้างเงื่อนไข Credit | form ปรับ field ตามประเภท: N วัน\* + ส่วนลด (%,วัน) + due basis (ใบแจ้งหนี้/ส่งมอบ/สิ้นเดือน) | code\* ชื่อ\* use_in ≥1 | เอกสารที่เลือกเห็นเงื่อนไขนี้ |
| S-02 | Happy | สร้าง Deposit | วิธีมัดจำ 3 แบบ (% / บาทคงที่ / กำหนดตอนสร้างเอกสาร) + เวลาชำระส่วนเหลือ + trigger หลังมัดจำ | มัดจำ % > 0 และ ≤ 100 | มัดจำ inherit ไปปรับต่อได้ที่ PO/SO (LD-08) |
| S-03 | Happy | สร้าง Installment | เพิ่ม/ลบงวด (≥2) กำหนด % + due_type ต่องวด · แถบรวม % สด | รวม = 100% เท่านั้น | ปลายทางแตก journal item ต่องวด (OB-3①) |
| S-04 | Happy | สร้าง Prepay / Postpay / Partial / Direct | field เฉพาะประเภท (Direct: หมวดค่าใช้จ่าย + ไม่มี trigger/ไม่ผ่าน PO) | — | — |
| S-05 | Alt | ตั้งค่า Default | toggle ต่อประเภท — ตัวเก่าประเภทเดียวกันหลุดอัตโนมัติ (radio) · **ตั้งได้เฉพาะสถานะใช้งาน** | สถานะ = ใช้งาน | เอกสารใหม่เลือกให้อัตโนมัติ |
| S-06 | Exception | ข้อมูลผิด | code ซ้ำ · เครดิต ≤0 วัน · มัดจำ % 0/เกิน 100 · งวด <2 หรือรวม ≠100 · use_in ว่าง · **ส่วนลด: วันลด ≥ วันเครดิต** | — | บล็อกพร้อมชี้ช่อง + toast |
| S-07 | Alt | แก้ไข | แก้ได้ทุก field (เอกสารเก่า snapshot เงื่อนไขแล้ว — ต่างจาก Tax Code) · used>0 ลบไม่ได้ | — | กระทบเฉพาะเอกสารใหม่ |
| S-08 | Alt | เปลี่ยนสถานะอิสระ (เมนู view / bulk 3 ค่า) | ทุกทิศ ไม่มีอนุมัติ | — | ไม่ "ใช้งาน" หายจากตัวเลือกเอกสารใหม่ |
| S-09 | Exception | bulk ลบ | confirm บอกยอดข้ามเพราะถูกใช้ — `used>0` ไม่ลบ | เลือก ≥1 | — |
| S-10 | **ไม่รองรับ** (ตัดสินแล้ว) | ① **นำเข้า/ส่งออก CSV ทั้งคู่ — ตัดออกจาก feature นี้ (มติ 2026-08-09)**: เงื่อนไขชำระเงินมีจำนวนน้อยและโครงซับซ้อนต่อแถว (งวด/มัดจำ) — จัดการผ่านฟอร์มเท่านั้น ② payment term ที่ PR (LD-01) ③ เปลี่ยน trigger ของ Credit (LD-08b locked) ④ ส่วนลดหลายช่วง (SAP ได้ 3 ช่วง — เรา 1) → OQ-PAY-02 ⑤ ลบเดี่ยว/ลบตัวที่ถูกใช้ ⑥ สายอนุมัติ ⑦ ล็อกแก้เงื่อนไขเมื่อ used>0 (ไม่ล็อกแบบ Tax เพราะเอกสาร snapshot แล้ว — [AI-DRAFT] ดู §10) | | | |

## 3. Data — full data dict
### 3.1 Fields (form เดียว ปรับตามประเภท)
| Field | ใช้กับประเภท | บังคับ | กติกา |
|---|---|---|---|
| code | ทุกประเภท | ✅ | unique · uppercase ตอนนำเข้า |
| ชื่อ (TH) / ชื่อ (EN) | ทุกประเภท | TH ✅ | — |
| ประเภท (7 ค่า) | — | ✅ | fix · sub อธิบายใน dropdown (2 บรรทัด) |
| trigger คลัง (ทันที/หลังมัดจำ/หลังชำระเต็ม) | ยกเว้น Direct | ✅ | ค่า default ต่อประเภท · Credit locked=ทันที (LD-08b) · หลังมัดจำ = deposit เท่านั้น |
| due_basis (ใบแจ้งหนี้/ส่งมอบ/สิ้นเดือน) | ทุกประเภท | ✅ | = baseline date (OB-3⑤) |
| net_days | Postpay(≥0) · Credit(>0) · Deposit (ส่วนเหลือ) | ตามประเภท | เครดิตต้อง >0 |
| discount_pct + discount_days | Credit | ⬜ | ถ้ามี % → วันลด >0 และ **< net_days** |
| deposit_method (%/บาท/กำหนดเอง) + deposit_value | Deposit | ✅ | % → >0 และ ≤100 · กำหนดเอง → value ว่าง |
| remaining_timing (หลังส่ง/หลังรับ/ตามสัญญา) | Deposit | ✅ | — |
| installments[] {pct, days, due_type, desc} | Installment | ✅ | ≥2 งวด · รวม 100% · due_type 3 ค่า (เมื่อสร้างเอกสาร/N วันหลังส่งมอบ/กำหนดเอง) |
| expense_category (สาธารณูปโภค/สัญญา/อื่น) | Direct | ✅ | — |
| use_in[] (8 เอกสาร แยกฝั่ง) | ทุกประเภท | ✅ ≥1 | Quotation ฝั่งขายเท่านั้น (LD-01) |
| is_default | ทุกประเภท | — | 1 ตัว/ประเภท (radio) · ต้องสถานะใช้งาน |
| สถานะ (3 ค่า) | ทุกประเภท | — | อิสระ |
### 3.2 ระบบ: `used` (เอกสารที่อ้าง — guard ลบ · mock) · created/updated
### 3.3 DOA placeholder 4 fields = null (OB-4)

## 4. Business Rules
| BR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01 | code unique (form + ในไฟล์นำเข้า + กับทะเบียน) | S-06, S-10 | [แผน] |
| BR-02 | เครดิต net_days > 0 · Postpay ≥ 0 (0 = ทันทีหลังรับ) | S-06 | FRD BR-ENH-10 |
| BR-03 | มัดจำ %: > 0 และ ≤ 100 | S-06 | FRD BR-ENH-05 + standard |
| BR-04 | งวด ≥ 2 + รวม 100% เท่านั้น | S-03, S-06 | FRD BR-ENH-02/03 |
| BR-05 | ส่วนลดจ่ายเร็ว: discount_days > 0 และ < net_days | S-06 | standard (2/10 Net 30) |
| BR-06 | use_in ≥ 1 · Quotation เฉพาะฝั่งขาย | S-06 | LD-01 |
| BR-07 | Default: 1 ตัวต่อประเภท (ตัวเก่าหลุดอัตโนมัติ) + ตั้งได้เฉพาะสถานะใช้งาน | S-05 | FRD BR-ENH-02 + standard |
| BR-08 | `used > 0` ลบไม่ได้ — bulk ข้ามพร้อมแจ้ง · **แก้ไขยังได้** (เอกสารเก่า snapshot เงื่อนไขแล้ว) | S-07, S-09 | [แผน + AI-DRAFT] |
| BR-09 | ไม่มีนำเข้า/ส่งออก CSV — สร้าง/แก้ผ่านฟอร์มเท่านั้น | S-10① | มติ 2026-08-09 |
| BR-10 | ปลายทางเลือกได้เฉพาะสถานะ "ใช้งาน" · Credit trigger = ทันทีเสมอ | S-08 | LD-08b |

## 5. State Machine — 3 สถานะอิสระ (ร่าง ⇄ ใช้งาน ⇄ ไม่ใช้งาน ทุกทิศ) — จาก เมนู view / bulk / ฟอร์ม / ไฟล์นำเข้า

## 6. Actions ต่อหน้า
| หน้า | Action |
|---|---|
| List | ค้นหา (รหัส/ชื่อ) · filter ประเภท (sdd combobox) + สถานะ · stat 4 ใบกดกรอง · checkbox + bulk (3 สถานะ + ลบ) · เพิ่มเงื่อนไข · แถว: แก้ไขเดี่ยว · ★ ตารางใน `.tbl-scroll` (thead sticky) — **scroll ไม่เด้งทุก interaction (Iron Rule #29)** |
| Drawer form | field ปรับตามประเภท · แถบรวม % งวดสด · validate ครบ + toast · สถานะ + default toggle |
| Drawer view | สรุปเงื่อนไขต่อประเภท · เมนูเปลี่ยนสถานะ 3 ค่า · แก้ไข · Esc chain |
| Modal | confirm ลบ bulk (บอกยอดข้าม) |

## 7. Data behaviour
เอกสารปลายทาง **snapshot เงื่อนไข** ตอนสร้าง (แก้ master กระทบเฉพาะเอกสารใหม่) · soft ref เก็บ code · `used` จริง sync จากเอกสารทุกใบ (OQ) · hooks บัญชี 5 ข้อ (OB-3) รอ FRD

## 8. Mock Data Spec (12 ตัวครอบ 7 ประเภท)
PREPAY / POSTPAY / NET30 (default · used 186 — prove guard ลบ) / NET60 (ไม่ใช้งาน) / 2-10N30 (ส่วนลด) / EOM30 / DEP50 / DEP30 / INST3 (3 งวด 40-30-30) / PARTIAL / DIRECT-UTIL / NET45 (ร่าง used 0)

## 9. Edges + ผลปลายทาง
| ทิศ | คู่ | ผ่านอะไร |
|---|---|---|
| ออก | → PO / SO (+ QUO ฝั่งขาย) | เงื่อนไข inherit ไปปรับต่อ (LD-08/09) · เลือกเฉพาะใช้งาน |
| ออก | → AP/AR Invoice · Payment Voucher / Receipt | คำนวณ due date (baseline) + งวด + ส่วนลด |
| ออก | → **Warehouse/GRN/Ship** | trigger ต่อประเภท (LD-02) — engine `payment-trigger-resolver` (ENG-PT-02) |
| ออก | → **Accounting/GL** | journal item ต่องวด · บัญชีมัดจำ clearing + **ใบกำกับภาษีมัดจำ (Tax Code)** · บัญชีส่วนลดรับ/จ่าย (OB-3) |
| ออก | → Customer / Vendor master | field payment_term default ระดับคู่ค้า (OQ-PAY-03 — edge ประกาศไว้ ยังไม่ทำ) |
| — | DOA / NOTIF | ไม่มี (OB-4) |

## 10. OQ + [AI-DRAFT] register
| # | ประเด็น | เจ้าภาพ | สถานะ |
|---|---|---|---|
| OQ-PAY-01 | full_postpay ≈ credit ที่ due_basis=delivery (มาตรฐานใช้ประเภทเดียว + baseline) — คงตาม LD-02 หรือยุบ | Strike | pin |
| OQ-PAY-02 | ส่วนลดจ่ายเร็ว 1 ช่วง (SAP ได้ 3 ช่วง) — พอสำหรับ SME มั้ย | Strike | pin |
| OQ-PAY-03 | Vendor/Customer master ต้องมี field payment_term override default ระบบ — เพิ่มตอนทำ master คู่ค้า | BA (edge) | pin |
| OQ-PAY-04 | มัดจำ: ใบกำกับภาษี ณ จุดรับเงิน + บัญชีมัดจำ — ยืนยัน flow กับ Accounting | Strike/บัญชี | pin |
| OQ-PAY-05 | ไม่ล็อกแก้เงื่อนไขเมื่อ used>0 (ต่างจาก IR-TAX-01) เพราะเอกสาร snapshot แล้ว — ยืนยันหลักการ [AI-DRAFT] | Strike | pin |
| OQ-PAY-06 | FRD pack (v5.1) **stale** — regen จาก HTML ใหม่ + register ENG-PT-01/02 กับ Architect | BA | เปิด |
| OQ-PAY-07 | `used` mock — จริงนับจากเอกสารทุกใบที่อ้าง | FRD | เปิด |

## 11. Coverage Matrix
| S | BR | transition | UI | FN |
|---|---|---|---|---|
| S-01..S-04 | BR-01..06,10 | สร้าง | form ต่อประเภท | FN-01..FN-12 |
| S-05 | BR-07 | — | default toggle | FN-13 |
| S-06 | BR-01..06 | — | validate + toast | FN-14..FN-16 |
| S-07 | BR-08 | amend | แก้ไข | FN-17 |
| S-08 | BR-10 | ทุกทิศ | เมนู view + bulk | FN-18, FN-19 |
| S-09 | BR-08 | ลบ | bulk + confirm ข้าม | FN-20 |
| S-10 | BR-09 | — | (ตรวจว่าไม่มี) | FN-40 |
ผ่าน: BR ครบ ✓ · state ครบ ✓ · S↔UI↔FN ครบ ✓ · OB-1..7 อ้างครบ ✓ · LD-01..15 ไม่ถูกฝืน ✓
