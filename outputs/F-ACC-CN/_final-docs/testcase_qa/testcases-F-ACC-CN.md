# AI Test Cases — ใบลดหนี้ลูกค้า (Credit Note · F-ACC-CN / F096)

ไฟล์นี้เขียนสำหรับ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype
`F-ACC-CN_credit-note.html` (vanilla JS SPA · hash routing). ทุก action/expected ผูกกับ **ข้อความที่เห็นบนจอ**
(verbatim จาก HTML / 01_UI / microcopy กลาง) + **route จริง**. Expected เช็คได้ด้วยตา. ทุก step มีช่อง Result `☐`.
Trace กลับ FRD Pack (`06_TESTS` AC/§6.9 XT · `05_RULES` BR/EC/error/permission · `01_UI`) + `FUNCTION_CHECKLIST` 22 FN.

> **แหล่ง anchor:** HTML ต้นทาง (verbatim) > 01_UI > microcopy กลาง html-generator-v9. ไม่พบ drift ระหว่าง 01_UI ↔ HTML.
> **DEMO harness:** persona switcher / `demoPay` / `.demo-only` เป็นของทดสอบใน prototype (prod strip) — ใช้เพื่อ setup role และพิสูจน์ S-11 เท่านั้น.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-ACC-CN (F096) |
| Feature Name | ใบลดหนี้ลูกค้า — Credit Note |
| FRD Version | 1.0 (2026-09-22) · Variant FULL |
| App entry | เปิด `F-ACC-CN_credit-note.html` · Sidebar (กลุ่ม AR) active = **ใบลดหนี้ลูกค้า** |
| Routes | `#/list` (P-01) · `#/create` (P-02 wizard 5 ขั้น) · `#/create/dup-<id>` (ทำสำเนา) · `#/edit/<id>` (P-03 draft) · `#/view/<id>` (P-04 view drawer 5 tabs) |
| ที่มา | FRD_Pack (00,01,05,06,07) · BRD_F-ACC-CN.md · HTML `F-ACC-CN_credit-note.html` (source of truth) · FUNCTION_CHECKLIST (22 FN) |
| จำนวนเคส | 88 เคส · 13 group |
| Roles | เจ้าหน้าที่ลูกหนี้ (officer-ar · Maker) · ผจก.ขาย (mgr-sales · ขั้น1) · ผจก.บัญชี (mgr-acc · ขั้น2) · CFO (cfo · ขั้น3) — สลับด้วย persona switcher (DEMO) |
| Negatives | ไม่มี FN-40 เดี่ยว — negatives = tile ปิด (FN-02) · SoD ไม่มีปุ่มอนุมัติ (FN-14) · no hard delete (BR-13) · void/paid ไม่โผล่ · refund/revise-only |

---

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| G1 · รายการ/ค้นหา/กรอง/สถิติ/CSV (P-01 · FN-90) | 10 | กลาง |
| G2 · เลือกแหล่งที่มา s1 (FN-01/02/03/04) | 7 | สูง |
| G3 · เหตุผล + ยอดลด s2/s3 (FN-05/06/07/08/09/10) | 13 | สูง |
| G4 · ส่วนลดท้ายบิล s3 (FN-19 · BR-11/12 · LD-05) | 7 | สูง |
| G5 · ส่งอนุมัติ + DOA (FN-11) | 6 | สูง |
| G6 · อนุมัติ/ไม่อนุมัติ/re-check/SoD (FN-12/13/17/14) | 8 | สูง |
| G7 · ยกเลิก/ส่งลูกค้า/ออกเอกสารแก้ไข (FN-15/16) | 6 | กลาง |
| G8 · View tabs: ref/history/pdf (FN-18/91/92) | 6 | กลาง |
| G9 · Status guards + Negatives | 9 | สูง |
| G10 · Permission matrix (SoD) | 7 | สูง |
| G11 · Cross-module (XT-01..06) | 6 | สูง |
| G12 · Scope Lock verify (LOCK) | 3 | กลาง |
| G13 · Edge cases (EC) | 4 | กลาง/ต่ำ |

---

## Coverage Ledger

### FN (FUNCTION_CHECKLIST 22/22)
| FN | S / BR | cases |
|---|---|---|
| FN-01 เลือกใบคงค้าง + เห็นสุทธิ/ลดแล้ว/คงค้าง | S-01 · BR-01 | TC-S01, TC-S02, TC-01 |
| FN-02 tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ | S-12 · BR-14 | TC-S03 |
| FN-03 เลือกใบ→ดึงลูกค้า/ที่อยู่/เลขภาษี/บรรทัด | S-01 | TC-S02, TC-01 |
| FN-04 ใบชำระครบ/void ไม่โผล่ | S-13 · BR-01 | TC-S04, TC-13c |
| FN-05 RET → เลือกใบรับคืน · จำนวนจาก SR | S-01 · BR-06 | TC-R01, TC-R02, TC-R03, TC-01 |
| FN-06 DISC ราคาลด ≤ ราคาเดิม | S-02 · BR-04 | TC-06, TC-06b |
| FN-07 PRICE/QTY ลดเฉพาะบรรทัด · ลบ/readd | S-03 · BR-03 | TC-07, TC-07b |
| FN-08 ลดหลายรอบ meta ถูกต้อง | S-04 · BR-03/10 | TC-08 |
| FN-09 ยอด/จำนวนเกิน → บล็อก+บอกยอด | S-05 · BR-02 | TC-09, TC-09b, TC-09c |
| FN-10 คำอธิบาย ≥10 | BR-05 | TC-10 |
| FN-11 ส่งอนุมัติ: สายตามมูลค่า + เลือกครบ | S-06 · BR-07 | TC-11a, TC-11b, TC-11c, TC-11d, TC-11e |
| FN-12 อนุมัติครบสาย → เลข CN | S-06 · BR-08 | TC-12, TC-12b |
| FN-13 ไม่อนุมัติ + เหตุผล → ร่าง + รอบก่อน | S-07 | TC-13, TC-13b |
| FN-14 ผู้ส่งไม่เห็นปุ่มอนุมัติ (SoD) | S-08 · BR-07 | TC-14b, TC-P05 |
| FN-15 ยกเลิก draft/pending + เหตุผล → คืน held | S-09 | TC-15, TC-15b |
| FN-16 ส่งลูกค้า → "ส่งลูกค้าแล้ว" · resend | S-10 | TC-16, TC-16b |
| FN-17 outstanding ลดระหว่างรอ → อนุมัติไม่ได้ | S-11 · BR-02 | TC-17 |
| FN-18 ref tab คงค้างก่อน/หลัง + VAT + JE | S-14 · BR-09 | TC-18, TC-18b |
| FN-19 ส่วนลดท้ายบิล ฿/% · ≥0 ≤คงค้าง · ลด VAT | S-14 · BR-11/12 | TC-19a, TC-19b, TC-19c, TC-19d, TC-19e, TC-19f, TC-19g |
| FN-90 ค้นหา/กรอง/สถิติ/CSV + empty | กติกากลาง | TC-L01..TC-L10 |
| FN-91 ประวัติ append-only | GR-4 · BR-13 | TC-91, TC-91b |
| FN-92 PDF ม.86/10 (เลข/วันที่ใบเดิม·เดิม/ถูกต้อง/ผลต่าง·เหตุผล·ค.ศ.) | OB-6 | TC-92 |

**FN cross-check: ✅ 22/22** (ทุก FN มี ≥1 เคส)

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-01 picker เฉพาะ issued/sent outstanding>0 | TC-S01, TC-S04, TC-13c |
| BR-02 grand ≤ available (ส่ง) + ≤ outstanding (อนุมัติ) | TC-09, TC-09b, TC-17, TC-X01 |
| BR-03 qty/net ≤ ที่ลดได้ (ข้ามทุกใบ) | TC-07, TC-08, TC-09c |
| BR-04 price ≤ ราคาเดิม (mode price) | TC-06, TC-06b |
| BR-05 reason ∈ master · text ≥10 | TC-10, TC-R04 |
| BR-06 RET ต้องอ้าง SR · qty ≤ SR | TC-R01, TC-R02, TC-R03 |
| BR-07 DOA resolve ตาม grand · SoD | TC-11c, TC-14b, TC-19c, TC-P05 |
| BR-08 เลข CN no-gap ตอน final approve | TC-12, TC-12b |
| BR-09 approved → cn_applied + JE + ลดภาษีขาย | TC-18, TC-X01, TC-X03 |
| BR-10 held ชั่วคราว · ยกเลิกคืน held | TC-08, TC-15, TC-X04 |
| BR-11 end-bill cap · net ≥0 ≤คงค้าง | TC-19b, TC-19e |
| BR-12 end-bill ลดฐานภาษี · VAT ม.86/10 | TC-19a, TC-19d, TC-18b, TC-X02 |
| BR-13 append-only · no hard delete · ค.ศ. | TC-91, TC-91b, TC-NEG-04 |
| BR-14 tile ลดลอย ปิดไว้ | TC-S03 |
| BR-15 legal_basis ต่อ reason · DISC warn | TC-R05, TC-06, TC-92 |

### State Machine / Status Guards (05_RULES §5.2)
| transition/guard | cases |
|---|---|
| draft→pending (submit) | TC-11a |
| pending→approved (approve ครบสาย) | TC-12 |
| pending→draft (reject) | TC-13 |
| draft/pending→cancelled (cancel) | TC-15, TC-15b |
| approved→sent (send) · sent→resend | TC-16, TC-16b |
| approved/sent → ออกเอกสารแก้ไข (display-only) | TC-NEG-05 |
| submit เฉพาะ draft (guard) | TC-GRD-01 |
| edit เฉพาะ draft (guard) | TC-GRD-02 |
| cancel เฉพาะ draft/pending (guard) | TC-GRD-03 |
| send เฉพาะ approved (guard) | TC-GRD-04 |

### Field Validation / Error Catalog (05_RULES §5.4/§5.6)
| error code | cases |
|---|---|
| BR_CN_DATE_BEFORE_INVOICE ("ต้องไม่ก่อนวันที่ใบแจ้งหนี้") | TC-R06 |
| BR_REASON_REQUIRED ("เลือกเหตุผล") | TC-R04 |
| BR_RET_NEEDS_SR ("เลือกใบรับคืนของใบแจ้งหนี้นี้") | TC-R02 |
| BR_REASON_TEXT_TOO_SHORT ("ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร") | TC-10 |
| BR_REP_REQUIRED ("ระบุพนักงานขาย") | TC-R07 |
| BR_LINE_QTY_EXCEEDED | TC-09c, TC-R03 |
| BR_PRICE_EXCEEDS_ORIG | TC-06 |
| BR_LINE_NET_EXCEEDED | TC-09c |
| BR_ENDBILL_EXCEEDS_CAP | TC-19b |
| BR_CN_EXCEEDS_OUTSTANDING | TC-09, TC-09b |
| BR_APPROVE_EXCEEDS_OUTSTANDING | TC-17 |
| BR_SUBMIT_DRAFT_ONLY | TC-GRD-01 |
| BR_EDIT_DRAFT_ONLY | TC-GRD-02 |
| BR_CANCEL_STATE_INVALID | TC-GRD-03 |
| BR_SEND_STATE_INVALID | TC-GRD-04 |
| BR_SLOT_INCOMPLETE ("เลือกผู้อนุมัติให้ครบทุกขั้น") | TC-11b |
| ERR_STALE_DATA (409 concurrent) | TC-CC-01 |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / double-submit | TC-ID-01 |

### Permission Matrix (05_RULES §5.3 · role × action)
| cell | cases |
|---|---|
| officer-ar create/edit/submit/cancel/send = allow | TC-P01 |
| mgr-sales create = deny (ไม่มีปุ่มสร้าง) | TC-P02 |
| mgr-sales approve ขั้น1 = allow | TC-P03 |
| mgr-acc approve ขั้น2 (tier2+) = allow | TC-P04 |
| cfo approve ขั้น3 (tier3) = allow | TC-P06 |
| ผู้ส่ง (owner) approve ใบตัวเอง = deny (SoD) | TC-P05, TC-14b |
| ไม่ใช่ผู้มีสิทธิ์ขั้นปัจจุบัน = deny | TC-P07 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 outstanding ลดระหว่างรอ (S-11) | TC-17 |
| EC-02 ลดหลายรอบ (S-04) | TC-08 |
| EC-03 ใบ void ไม่โผล่ (S-13) | TC-13c |
| EC-04 ใบชำระครบ ไม่โผล่ | TC-S04, TC-13c |
| EC-05 ยกเลิก draft/pending คืน held (S-09) | TC-15, TC-X04 |
| EC-06 reject → history + badge (S-07) | TC-13, TC-13b |
| EC-CC-01 concurrent approval → 409 `[AI-DEFAULT]` | TC-CC-01 (ต้อง simulate) |
| EC-ID-01 double-submit idempotency | TC-ID-01 (ต้อง simulate) |
| EC-CALC-01 ปัดเศษ ebVat 2 ตำแหน่ง `[AI-DEFAULT]` | TC-CALC-01 |
| EC-FU-01 ชนิด/ขนาดไฟล์แนบ `[AI-DEFAULT]` | TC-FU-01 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 approve → ar_open_item cn_applied↑ | AR F094 | TC-X01 |
| XT-02 approve → ภ.พ.30 netVat เดือน cnDate | VAT F105 | TC-X02 |
| XT-03 approve → JE (Dr 4110/4120 · Dr 2150 · Cr 1130) | JE F093 mock | TC-X03 |
| XT-04 ยกเลิก (draft/pending) → held คืน | AR F094 | TC-X04 |
| XT-05 ยกเลิกหลังอนุมัติ (ไม่รองรับ) → "ออกเอกสารแก้ไข" | — | TC-X05 (= TC-NEG-05) |
| XT-06 RET → SR ใบเดียวกัน · qty ≤ รับคืน | SR F090 mock | TC-X06 (= TC-R01/R03) |

### Scope Lock (07_LOCKED §7.0)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 Pattern Q + B2 v2 | TC-01, TC-07 |
| LOCK-02 อ้าง AR Invoice เสมอ | TC-S03, TC-S01 |
| LOCK-03 เหตุผล master (RET/DISC/PRICE/QTY) | TC-R05 |
| LOCK-04 ลดไม่เกินคงเหลือ | TC-09, TC-17 |
| LOCK-05 DOA slot picker ตามมูลค่า | TC-11c |
| LOCK-06 doccfg CN-YYYY-NNNN + PDF อ้างเลขเดิม | TC-12, TC-92 |
| LOCK-07 ระบุผลกระทบ VAT ขาย | TC-18, TC-X02 |
| LOCK-08 dep ข้ามเลน = mock | TC-X03, TC-X06 |
| LOCK-09 UI #67.1 (เฉพาะ hard-warn/field-error/danger) | TC-LK-09 |
| LOCK-10 ค.ศ. · append-only | TC-91, TC-92, TC-LK-10 |

### Out of Scope (Exclusions — ห้ามสร้างเคสทดสอบ "ให้ทำได้")
- ลดหนี้ไม่อ้างใบ (ลดลอย) → ตรวจ **ต้องปิด** ที่ TC-S03 (นอกขอบเขต = ทดสอบว่าปิด ไม่ใช่ทำได้)
- คืนเงิน refund เมื่อชำระครบ → นอกขอบเขตใบเซ็น (LITE) → TC-NEG-03 (ตรวจว่าใบชำระครบไม่โผล่)
- ยกเลิกหลังอนุมัติ → นอกขอบเขต → TC-NEG-05 (ตรวจว่าใช้ revise-doc display-only)
- หน้าจอ Sales Return จริง → นอกขอบเขต (F090 mock) → seed อย่างเดียว ไม่ทดสอบหน้าจอ SR

---

## Data Sets

> ค่าจาก 06_TESTS §6.3 (mock ใน HTML — พิสูจน์ scenario) + master. ปุ่ม "จำลอง" ใน prototype ใช้ seed ได้ทันที.

### ชุดใบแจ้งหนี้ (ref invoice)
| ชุด | ใบแจ้งหนี้ | ลักษณะ | ใช้กับ scenario |
|---|---|---|---|
| INV-A | INV-2026-0140 | 10 กล่อง · CN-0021 ลดแล้ว 1 กล่อง · มี SR-2026-0016 (2 กล่อง) | S-01/S-04 (RET, ลดหลายรอบ) |
| INV-B | INV-2026-0137 | ใบบริการ | S-02 (DISC ส่วนลดภายหลัง) |
| INV-C | INV-2026-0135 | สินค้าหลายบรรทัด | S-03 (PRICE/QTY ลบ/readd บรรทัด) |
| INV-D | INV-2026-0141 | ยอด 770,400 · มี SR-2026-0014 | tier 2/3 DOA |
| INV-PAID | INV-2026-0136 | ชำระครบ (outstanding=0) | ต้องไม่โผล่ใน picker |
| INV-VOID | INV-2026-0143 | void | ต้องไม่โผล่ใน picker |

### ชุดเหตุผล (CN_REASONS master · verbatim)
| ชุด | เหตุผลบนจอ | mode | legal_basis | หมายเหตุ |
|---|---|---|---|---|
| RS-RET | รับคืนสินค้า (อ้างใบรับคืน) | qty | รับคืนสินค้า/ยกเลิกบริการ | ต้องเลือกใบรับคืน (needSR) |
| RS-DISC | ส่วนลดภายหลังการขาย | price | ลดราคาเพราะสินค้าผิดข้อกำหนด/ชำรุด | มี trade_discount_warn |
| RS-PRICE | คิดราคาสูงเกิน (ผิดราคา) | price | คำนวณราคาสินค้าผิดพลาดสูงกว่าที่เป็นจริง | — |
| RS-QTY | คิดจำนวนเกินที่ส่งจริง | qty | จัดส่งสินค้าขาดจำนวน/คิดเกินที่ส่งจริง | — |

### ชุดคำอธิบายเหตุผล (reason_text)
| ชุด | ค่า | ผล |
|---|---|---|
| RT-OK | "ลูกค้าคืนสินค้า 2 กล่องเนื่องจากชำรุด" (>10 ตัว) | ผ่าน |
| RT-SHORT | "ชำรุด" (<10 ตัว) | field-error |

### ชุดส่วนลดท้ายบิล (end-bill)
| ชุด | mode | value | คาดผล (บน INV-A after=X) |
|---|---|---|---|
| EB-OK-AMT | ฿ (amount) | ค่าที่ ≤ ebCap | ลดฐานภาษี + VAT คิดใหม่ · grand ลดลง |
| EB-OK-PCT | % (percent) | 5% | ebBase/netVat คำนวณตามสัดส่วน |
| EB-OVER | ฿ (amount) | ค่าที่ > ebCap (เช่น สูงกว่ายอด after) | hard-warn + block submit |

### ชุด DOA tier (ยอดสุทธิ grand)
| ชุด | grand | tier | สายอนุมัติ |
|---|---|---|---|
| DOA-T1 | ≤ 50,000 | 1 | ผจก.ขาย |
| DOA-T2 | 50,000.01–300,000 | 2 | ผจก.ขาย → ผจก.บัญชี |
| DOA-T3 | > 300,000 | 3 | ผจก.ขาย → ผจก.บัญชี → CFO |

### Personas (DEMO switcher)
| ชุด | ชื่อบนจอ | role | ใช้ |
|---|---|---|---|
| U-AR | วราภรณ์ | เจ้าหน้าที่ลูกหนี้ (officer-ar) | Maker |
| U-SALES | มานพ | ผจก.ขาย (mgr-sales) | อนุมัติขั้น 1 |
| U-ACC | ประเสริฐ | ผจก.บัญชี (mgr-acc) | อนุมัติขั้น 2 |
| U-CFO | อรุณี | CFO (cfo) | อนุมัติขั้น 3 |

### ไฟล์ทดสอบ (Files)
| ชื่อไฟล์ | ใช้กับ | หมายเหตุ |
|---|---|---|
| `cn-attach-ok.pdf` | TC-FU-01 (แนบ s4) | jpg/png/pdf ≤10MB → ผ่าน (`[AI-DEFAULT]`) |
| `cn-attach-big.pdf` | TC-FU-01 (>10MB) | เกินขนาด → ปฏิเสธ (ต้อง simulate ถ้า UI ไม่บังคับ) |

---

## Test Cases

## G1 · รายการ / ค้นหา / กรอง / สถิติ / CSV (P-01 · FN-90 · AC-90)

### TC-L01 — เปิดหน้ารายการ เห็นตาราง + stat 4 tile (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / AC-90 / 01_UI P-01
- actor: เจ้าหน้าที่ลูกหนี้
- Setup: role=officer-ar (U-AR) · seed=มีใบลดหนี้หลายสถานะ · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: เห็นตาราง 10 คอลัมน์ + stat 4 tile ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | Breadcrumb Accounting > AR > ใบลดหนี้ลูกค้า · Sidebar active = **ใบลดหนี้ลูกค้า** | ☐ |
| 2 | VERIFY แถบ stat ด้านบน | — | 4 tile: **รออนุมัติ** · **ลดหนี้เดือนนี้** · **ฉบับร่าง** · **ภาษีขายที่ลดเดือนนี้** (sub "ภ.พ.30 เดือน MM/YYYY") | ☐ |
| 3 | VERIFY หัวตาราง | — | คอลัมน์: เลขที่ · วันที่ · ลูกค้า · ใบแจ้งหนี้อ้างอิง · เหตุผล · สถานะเอกสาร · ลายเซ็น · ยอดลดหนี้ · ภาษีขายที่ลด · ⋮ | ☐ |
| 4 | VERIFY ปุ่มมุมขวาบน | — | เห็นปุ่ม **ส่งออก CSV** + **สร้างใบลดหนี้** | ☐ |

### TC-L02 — ค้นหาเจอ (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / searchText
- Setup: role=officer-ar · seed=มีใบของลูกค้าที่ค้นได้ · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | เลข CN หรือชื่อลูกค้าที่มีจริง | ตารางเหลือเฉพาะแถวที่ตรง | ☐ |
| 2 | VERIFY จำนวนแถว | — | ทุกแถวที่เหลือมีคำค้นในคอลัมน์ เลขที่/ลูกค้า/ใบอ้างอิง | ☐ |

### TC-L03 — ค้นหาไม่เจอ → empty (edge)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / states
- Setup: role=officer-ar · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | "zzzzzz" | ตารางว่าง · แสดงสถานะไม่พบข้อมูล (ไม่มีแถว) | ☐ |
| 2 | CLICK ล้างคำค้น | — | ตารางกลับมามีข้อมูลเดิม | ☐ |

### TC-L04 — กรองสถานะเอกสาร ครบทุกค่า (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / filterSelects
- Setup: role=officer-ar · seed=มีใบ draft/pending/approved/sent/cancelled อย่างละ ≥1 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → ตัวกรอง **สถานะเอกสาร** | "ฉบับร่าง" | เหลือเฉพาะแถว pill = ฉบับร่าง | ☐ |
| 2 | SELECT → **สถานะเอกสาร** | "รออนุมัติ" | เหลือเฉพาะ pill รออนุมัติ | ☐ |
| 3 | SELECT → **สถานะเอกสาร** | "อนุมัติแล้ว" | เหลือเฉพาะ pill อนุมัติแล้ว | ☐ |
| 4 | SELECT → **สถานะเอกสาร** | "ส่งลูกค้าแล้ว" | เหลือเฉพาะ pill ส่งลูกค้าแล้ว | ☐ |
| 5 | SELECT → **สถานะเอกสาร** | "ยกเลิก" | เหลือเฉพาะ pill ยกเลิก | ☐ |
| 6 | SELECT → **สถานะเอกสาร** | "ทั้งหมด" | กลับมาเห็นทุกแถว | ☐ |

### TC-L05 — กรองเหตุผล (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90
- Setup: role=officer-ar · seed=มีใบหลายเหตุผล · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → ตัวกรอง **เหตุผล** | "รับคืนสินค้า (อ้างใบรับคืน)" | เหลือเฉพาะแถวเหตุผลรับคืน | ☐ |
| 2 | SELECT → **เหตุผล** | "ทั้งหมด" | กลับมาเห็นทุกแถว | ☐ |

### TC-L06 — กรองลูกค้า (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90
- Setup: role=officer-ar · seed=มีใบ ≥2 ลูกค้า · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → ตัวกรอง **ลูกค้า** | ลูกค้ารายหนึ่ง | เหลือเฉพาะแถวของลูกค้านั้น | ☐ |

### TC-L07 — sort คอลัมน์ (happy)
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-90 / sortBy
- Setup: role=officer-ar · seed=≥3 แถว · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **เลขที่** | — | ลำดับแถวเปลี่ยน (เรียงตามเลขที่) | ☐ |
| 2 | CLICK หัวคอลัมน์ **วันที่** | — | เรียงตามวันที่ | ☐ |
| 3 | CLICK หัวคอลัมน์ **ยอดลดหนี้** | — | เรียงตามยอด grand | ☐ |

### TC-L08 — คลิก stat tile = filter (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / f.stat
- Setup: role=officer-ar · seed=มี pending + draft + approved เดือนนี้ · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tile **รออนุมัติ** | — | ตารางกรองเหลือเฉพาะ pending | ☐ |
| 2 | CLICK tile **ฉบับร่าง** | — | ตารางเหลือเฉพาะ draft | ☐ |
| 3 | CLICK tile **ลดหนี้เดือนนี้** | — | ตารางเหลือเฉพาะ approved/sent เดือนปัจจุบัน | ☐ |
| 4 | CLICK tile **ภาษีขายที่ลดเดือนนี้** | — | ตารางกรองตาม vat เดือนนี้ | ☐ |

### TC-L09 — ส่งออก CSV (happy)
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-90 / API-10 / csvHead
- Setup: role=officer-ar · seed=≥1 แถว · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | ไฟล์ CSV ถูกดาวน์โหลด (มีหัวคอลัมน์ csvHead) | ☐ |

### TC-L10 — empty state ไม่มีข้อมูลเลย (edge)
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-90 / states / 01_UI §1.6
- Setup: role=officer-ar · seed=ไม่มีใบลดหนี้เลย · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY กลางตาราง | — | ข้อความ **ยังไม่มีใบลดหนี้** + ปุ่ม CTA สร้าง | ☐ |

---

## G2 · เลือกแหล่งที่มา s1 (FN-01/02/03/04)

### TC-S01 — s1 เห็นตารางใบคงค้าง (สุทธิ/ลดแล้ว/คงค้าง) (happy)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-01 / AC-01 / BR-01 / LOCK-02
- actor: เจ้าหน้าที่ลูกหนี้
- Setup: role=officer-ar (U-AR) · seed=INV-A มีคงค้าง>0 · files=—
- Start: OPEN `#/list` → CLICK ปุ่ม **สร้างใบลดหนี้**
- ชุดข้อมูล: INV-A
- ผ่านเมื่อ: s1 แสดงตารางใบคงค้างพร้อมคอลัมน์ ยอดสุทธิ/ลดหนี้แล้ว/คงค้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบลดหนี้** | — | drawer สร้างเปิด · route=`#/create` · Stepper ขั้น 1 = **เลือกแหล่งที่มาของใบลดหนี้** | ☐ |
| 2 | VERIFY 2 tile บนสุด | — | tile **จากใบแจ้งหนี้** (active) · tile **ลดหนี้ไม่อ้างใบ** (มี pill "ปิดไว้") | ☐ |
| 3 | VERIFY ตารางใบคงค้าง | — | คอลัมน์ ใบแจ้งหนี้ · ลูกค้า · วันที่ · ยอดสุทธิ · **ลดหนี้แล้ว** · **คงค้าง** | ☐ |
| 4 | VERIFY แถว INV-A | INV-A | คอลัมน์ ลดหนี้แล้ว > 0 (CN-0021) · คงค้าง = สุทธิ − ลดแล้ว | ☐ |

### TC-S02 — เลือกใบ → ดึงลูกค้า/ที่อยู่/เลขภาษี/บรรทัด (happy)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-03 / AC-01 / pickInvoice
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create`
- ชุดข้อมูล: INV-A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **INV-A** ในตารางใบคงค้าง | INV-A | แถวถูกเลือก (highlight) | ☐ |
| 2 | CLICK **ถัดไป** | — | ไปขั้น 2 = **ข้อมูลหลักใบลดหนี้** | ☐ |
| 3 | VERIFY ช่องใบอ้างอิง + ลูกค้า | — | ใบอ้างอิง = INV-A (disabled) · ลูกค้า disabled แสดงชื่อ · เห็นเลขภาษี/ที่อยู่ | ☐ |
| 4 | VERIFY ช่องเลขที่ CN | — | readonly = **(ออกเลขเมื่ออนุมัติครบ)** | ☐ |
| 5 | CLICK **ถัดไป** ผ่าน s2 (กรอกครบ) แล้วดู s3 | — | ขั้น 3 มีบรรทัดสินค้าจากใบเดิม (สินค้าถูกล็อก readonly) | ☐ |

### TC-S03 — tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ (negative · FN-02)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-02 / AC-14 / BR-14 / LOCK-02 / OQ-CN-01
- Setup: role=officer-ar · seed=— · files=—
- Start: OPEN `#/create`
- ผ่านเมื่อ: tile disabled + คลิกแล้ว toast ปิดไว้ · ไม่มีทางเข้าสร้างแบบไม่อ้างใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tile **ลดหนี้ไม่อ้างใบ** | — | มี pill **ปิดไว้** · เคอร์เซอร์ not-allowed (ดูจาง/ปิด) | ☐ |
| 2 | CLICK tile **ลดหนี้ไม่อ้างใบ** | — | toast **ลดหนี้ไม่อ้างใบแจ้งหนี้ถูกปิดไว้ (OQ-CN-01)** · ไม่เปลี่ยน tile · ไม่มีฟอร์มสร้างแบบลอย | ☐ |
| 3 | VERIFY ไม่มีทางไปต่อโดยไม่เลือกใบ | — | tile "จากใบแจ้งหนี้" คงเป็นทางเดียว | ☐ |

### TC-S04 — ใบชำระครบ/void ไม่โผล่ใน picker (negative · FN-04)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-04 / AC-13 / BR-01 / EC-03/04
- Setup: role=officer-ar · seed=INV-PAID (ชำระครบ) + INV-VOID (void) มีอยู่ในระบบ · files=—
- Start: OPEN `#/create`
- ชุดข้อมูล: INV-PAID, INV-VOID

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตารางใบคงค้าง | — | ไม่มีแถว **INV-2026-0136** (ชำระครบ) | ☐ |
| 2 | VERIFY ตารางใบคงค้าง | — | ไม่มีแถว **INV-2026-0143** (void) | ☐ |
| 3 | TYPE ค้นหาในตาราง | "0136" | ไม่พบแถว (ยืนยันถูกกรองออก ไม่ใช่แค่ scroll) | ☐ |

### TC-S05 — s1 ไม่เลือกใบ → บล็อกไปต่อ (negative)
- group: สร้าง-s1 · ความสำคัญ: กลาง · trace: FN-01 / step1Validate
- Setup: role=officer-ar · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** โดยยังไม่เลือกใบ | — | บล็อก · ข้อความ **กรุณาเลือกใบแจ้งหนี้ที่จะลดหนี้** · ยังอยู่ขั้น 1 | ☐ |

### TC-S06 — ทำสำเนา (dup) จาก row menu (happy)
- group: สร้าง-s1 · ความสำคัญ: ต่ำ · trace: FN-90 / dupRec / prefillDup
- Setup: role=officer-ar · seed=มีใบ ≥1 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน ⋮ ท้ายแถวหนึ่ง | — | เมนูเปิด: ดูรายละเอียด · (แก้ไข ถ้า draft) · **ทำสำเนา** · พิมพ์ | ☐ |
| 2 | CLICK **ทำสำเนา** | — | route=`#/create/dup-<id>` · wizard เปิดพร้อมค่าจากใบต้นทาง | ☐ |

### TC-S07 — เข้าสร้างจากปุ่มหลัก (happy)
- group: สร้าง-s1 · ความสำคัญ: ต่ำ · trace: FN-90 / navigate('create')
- Setup: role=officer-ar · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบลดหนี้** | — | route=`#/create` · Stepper ขั้น 1 | ☐ |

---

## G3 · เหตุผล + ยอดลด s2/s3 (FN-05/06/07/08/09/10)

### TC-01 — สร้าง CN RET ครบ flow ถึงส่งอนุมัติ (happy · E2E)
- group: เหตุผล-RET · ความสำคัญ: สูง · trace: FN-01/03/05/11/12 / AC-01,02,11,12 / LOCK-01
- actor: เจ้าหน้าที่ลูกหนี้
- Setup: role=officer-ar (U-AR) · seed=INV-A + SR-2026-0016 (2 กล่อง) · files=—
- Start: OPEN `#/create`
- ชุดข้อมูล: INV-A · RS-RET · RT-OK
- ผ่านเมื่อ: บันทึกร่าง + เปิด submit modal ได้ (สายอนุมัติ resolve)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **INV-A** → **ถัดไป** | INV-A | ไปขั้น 2 · ใบอ้างอิง=INV-A | ☐ |
| 2 | SELECT → ช่อง **เหตุผล** | RS-RET (รับคืนสินค้า (อ้างใบรับคืน)) | แสดง legal_basis hint + ช่อง **ใบรับคืน** โผล่ | ☐ |
| 3 | SELECT → ช่อง **ใบรับคืน** | SR-2026-0016 | จำนวนบรรทัดถูกจำกัดตามใบรับคืน (line.max = SR qty = 2) | ☐ |
| 4 | SELECT → ช่อง **พนักงานขาย** | พนักงานขายที่มี | ช่องแสดงชื่อที่เลือก | ☐ |
| 5 | TYPE → ช่อง **คำอธิบายเหตุผล** | RT-OK | ผ่าน (>10 ตัว) | ☐ |
| 6 | CLICK **ถัดไป** → s3 | — | เห็นบรรทัดสินค้า mode qty · จำนวนสูงสุด = 2 | ☐ |
| 7 | CLICK **ถัดไป** ผ่าน s4 → s5 | — | ขั้น 5 = **ตรวจสอบและยืนยัน** · เห็น DOA preview (tier + สายอนุมัติ) | ☐ |
| 8 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกแบบร่างใบลดหนี้เรียบร้อย** · route=`#/view/<id>` · pill=ฉบับร่าง | ☐ |

### TC-R01 — RET เลือก SR → จำนวนจากใบรับคืน (happy · FN-05)
- group: เหตุผล-RET · ความสำคัญ: สูง · trace: FN-05 / AC-02 / BR-06 / XT-06
- Setup: role=officer-ar · seed=INV-A + SR-2026-0016 (2 กล่อง) · files=—
- Start: OPEN `#/create` → เลือก INV-A → ถัดไป (s2)
- ชุดข้อมูล: INV-A · RS-RET

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → **เหตุผล** | RS-RET | ช่อง **ใบรับคืน** ปรากฏ (required) | ☐ |
| 2 | SELECT → **ใบรับคืน** | SR-2026-0016 | จำนวนบรรทัดในใบ = จำนวนจาก SR (2 กล่อง) | ☐ |
| 3 | OPEN s3 → VERIFY จำนวนสูงสุดต่อบรรทัด | — | max = min(qtyLeft, SR.qty) | ☐ |

### TC-R02 — RET ไม่เลือก SR → บล็อก (negative · FN-05)
- group: เหตุผล-RET · ความสำคัญ: สูง · trace: FN-05 / AC-02 / BR-06 / BR_RET_NEEDS_SR
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → เลือก INV-A → ถัดไป (s2)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → **เหตุผล** | RS-RET | ช่องใบรับคืนปรากฏ (ยังว่าง) | ☐ |
| 2 | CLICK **ถัดไป** โดยไม่เลือก SR | — | บล็อก · field-error **เลือกใบรับคืนของใบแจ้งหนี้นี้** · ยังอยู่ s2 | ☐ |

### TC-R03 — RET จำนวนเกินที่รับคืน → บล็อก (negative · boundary · BR-06)
- group: เหตุผล-RET · ความสำคัญ: สูง · trace: FN-05 / BR-06 / BR_LINE_QTY_EXCEEDED / XT-06
- Setup: role=officer-ar · seed=INV-A + SR-2026-0016 (2 กล่อง) · files=—
- Start: OPEN `#/create` → INV-A → RET → SR-2026-0016 → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **จำนวน** ของบรรทัด | 3 (เกิน SR qty=2) | ช่องจำนวนขึ้นสถานะ over (แดง) · ยอดผิด | ☐ |
| 2 | CLICK **ถัดไป**/ทบทวน แล้วดูปุ่มส่ง | — | ถูกบล็อก · ข้อความบรรทัดเกิน "จำนวนลดเกินที่ลดได้: {item}" | ☐ |
| 3 | TYPE → **จำนวน** | 2 | สถานะ over หาย · ไปต่อได้ | ☐ |

### TC-R04 — ไม่เลือกเหตุผล → บล็อก (negative · BR-05)
- group: เหตุผล · ความสำคัญ: กลาง · trace: FN-05 / BR_REASON_REQUIRED
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** โดยไม่เลือกเหตุผล | — | field-error **เลือกเหตุผล** · ยังอยู่ s2 | ☐ |

### TC-R05 — legal_basis + trade_discount_warn ต่อ reason (happy · BR-15 · LOCK-03)
- group: เหตุผล · ความสำคัญ: กลาง · trace: BR-15 / LOCK-03 / FN-92
- Setup: role=officer-ar · seed=INV-B (บริการ) · files=—
- Start: OPEN `#/create` → INV-B → s2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → **เหตุผล** | RS-DISC (ส่วนลดภายหลังการขาย) | แสดง legal_basis hint "ลดราคาเพราะสินค้าผิดข้อกำหนด/ชำรุด" | ☐ |
| 2 | VERIFY เตือนใต้เหตุผล DISC | — | คำเตือน "ส่วนลดทางการค้าล้วนไม่ใช่เหตุออกใบลดหนี้ภาษี (รอเคาะ OQ-CN-01)" | ☐ |
| 3 | SELECT → **เหตุผล** | RS-PRICE (คิดราคาสูงเกิน (ผิดราคา)) | legal_basis hint เปลี่ยนเป็น "คำนวณราคาสินค้าผิดพลาดสูงกว่าที่เป็นจริง" · ไม่มี warn | ☐ |
| 4 | SELECT → **เหตุผล** | RS-QTY (คิดจำนวนเกินที่ส่งจริง) | legal_basis hint = "จัดส่งสินค้าขาดจำนวน/คิดเกินที่ส่งจริง" | ☐ |

### TC-R06 — cn_date ก่อนวันที่ใบเดิม → บล็อก (negative · boundary)
- group: เหตุผล · ความสำคัญ: กลาง · trace: FN-05 / BR_CN_DATE_BEFORE_INVOICE
- Setup: role=officer-ar · seed=INV-A (มีวันที่ใบเดิม) · files=—
- Start: OPEN `#/create` → INV-A → s2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **วันที่ใบลดหนี้** | วันที่ก่อนวันที่ใบเดิม | field-error **ต้องไม่ก่อนวันที่ใบแจ้งหนี้** · บล็อกไปต่อ | ☐ |
| 2 | TYPE → **วันที่ใบลดหนี้** | วันที่ ≥ วันที่ใบเดิม | error หาย · ไปต่อได้ | ☐ |

### TC-R07 — ไม่ระบุพนักงานขาย → บล็อก (negative)
- group: เหตุผล · ความสำคัญ: ต่ำ · trace: FN-05 / BR_REP_REQUIRED
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s2 (เลือกเหตุผล + คำอธิบายครบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** โดยเว้นพนักงานขาย | — | field-error **ระบุพนักงานขาย** · ยังอยู่ s2 | ☐ |

### TC-06 — DISC ราคาลดต่อหน่วย ≤ ราคาเดิม (negative · FN-06 · BR-04)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-06 / AC-06 / BR-04 / BR_PRICE_EXCEEDS_ORIG
- Setup: role=officer-ar · seed=INV-B (บริการ · mode price) · files=—
- Start: OPEN `#/create` → INV-B → s2 (RS-DISC + คำอธิบาย) → s3
- ชุดข้อมูล: INV-B · RS-DISC

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัด s3 | — | ช่อง **ราคา/หน่วย** แก้ได้ (mode price) | ☐ |
| 2 | TYPE → **ราคา/หน่วย** | ค่าที่ > orig_price | meta บรรทัด "— ราคาลดเกินราคาเดิม" · บรรทัด over | ☐ |
| 3 | CLICK ทบทวน/ส่ง | — | บล็อก · ข้อความ "ราคาลดต่อหน่วยเกินราคาเดิม: {item}" | ☐ |
| 4 | TYPE → **ราคา/หน่วย** | ค่าที่ ≤ orig_price | over หาย · ไปต่อได้ | ☐ |

### TC-06b — DISC ราคาลดเท่าราคาเดิม (boundary · ผ่าน)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-06 / BR-04 (boundary)
- Setup: role=officer-ar · seed=INV-B · files=—
- Start: OPEN `#/create` → INV-B → s2 (RS-DISC) → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **ราคา/หน่วย** | = orig_price พอดี | ไม่ over · ผ่าน (boundary ≤) | ☐ |

### TC-07 — PRICE/QTY ลบบรรทัดอื่น + readd (happy · FN-07 · LOCK-01)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-07 / AC-07 / BR-03 / LOCK-01
- Setup: role=officer-ar · seed=INV-C (หลายบรรทัด) · files=—
- Start: OPEN `#/create` → INV-C → s2 (RS-QTY) → s3
- ชุดข้อมูล: INV-C · RS-QTY

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัด s3 | — | มีหลายบรรทัดจากใบเดิม · สินค้าล็อก (readonly) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายบรรทัดที่ 2 | — | บรรทัดหายไป · โผล่ chip "บรรทัดจากใบเดิมที่ไม่ได้ลด" (readd ได้) | ☐ |
| 3 | CLICK chip readd บรรทัดที่ลบ | — | บรรทัดกลับมาในตาราง | ☐ |
| 4 | VERIFY ลดเฉพาะบรรทัดที่เหลือ | — | สรุปยอดคิดจากบรรทัดที่มีอยู่เท่านั้น | ☐ |

### TC-07b — ลดจำนวนเฉพาะบรรทัดที่เลือก (happy · FN-07)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-07 / BR-03
- Setup: role=officer-ar · seed=INV-C · files=—
- Start: OPEN `#/create` → INV-C → RS-QTY → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **จำนวน** บรรทัดที่ 1 | ค่าที่ ≤ qtyLeft | จำนวนเงินบรรทัด 1 อัปเดต · บรรทัดอื่นไม่เปลี่ยน | ☐ |
| 2 | VERIFY สรุปยอด | — | ยอดรวมสะท้อนเฉพาะบรรทัดที่ปรับ | ☐ |

### TC-08 — ลดหลายรอบ meta ถูกต้อง (edge · FN-08 · EC-02)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-08 / AC-08 / BR-03/10 / EC-02
- Setup: role=officer-ar · seed=INV-A มี CN-0021 อนุมัติแล้ว (ลดแล้ว 1 กล่อง) · files=—
- Start: OPEN `#/create` → INV-A → s2 → s3
- ชุดข้อมูล: INV-A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN s3 → VERIFY+จด meta บรรทัด | — | จด "ใบเดิม N × ฿P · ลดแล้ว ฿X · ลดจำนวนได้อีก M · ลดมูลค่าได้อีก ฿Y" (อ้าง step ถัดไป) | ☐ |
| 2 | VERIFY ค่า "ลดจำนวนได้อีก" | — | = จำนวนเดิม − ลดแล้วรวมทุกใบ (cn_applied + cn_held) เช่น 10 − 1 = 9 | ☐ |
| 3 | TYPE → **จำนวน** เกิน M | M+1 | บรรทัด over + ถูกบล็อก (นับรวมข้ามทุกใบ) | ☐ |

### TC-09 — ยอด CN เกินคงเหลือ → บล็อกส่ง + บอกยอด (negative · FN-09 · BR-02 · LOCK-04)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-09 / AC-09 / BR-02 / BR_CN_EXCEEDS_OUTSTANDING / LOCK-04
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s2 → s3
- ผ่านเมื่อ: draft บันทึกได้ แต่ส่งอนุมัติถูกบล็อก + แสดงยอด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ปรับจำนวน/ราคา ให้ grand > available | ค่าที่เกิน | hard-warn: "ยอดลดหนี้เกินยอดคงเหลือของใบแจ้งหนี้อ้างอิง — ลดได้ ฿X · ใบนี้ ฿Y · เกิน ฿Z ..." | ☐ |
| 2 | CLICK **บันทึกแบบร่าง** | — | บันทึกได้ (draft) · toast บันทึกแบบร่าง | ☐ |
| 3 | OPEN `#/view/<id>` → CLICK **ส่งอนุมัติ** | — | ถูกบล็อก · ข้อความ "ยอดลดหนี้เกินยอดคงเหลือใบแจ้งหนี้ (ลดได้ ฿X) — แก้ไขร่างก่อน" | ☐ |

### TC-09b — grand เท่ากับ available พอดี (boundary · ผ่าน)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-09 / BR-02 (boundary ≤)
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ปรับให้ grand = available พอดี | = available | ไม่มี hard-warn · ส่งอนุมัติได้ (boundary ≤) | ☐ |

### TC-09c — บรรทัด net เกิน netLeft → บล็อก (negative · BR-03)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-07/09 / BR-03 / BR_LINE_NET_EXCEEDED
- Setup: role=officer-ar · seed=INV-A (มี CN ลดแล้วบางส่วน) · files=—
- Start: OPEN `#/create` → INV-A → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ปรับมูลค่าบรรทัด > netLeft | เกิน netLeft | บรรทัด over · ข้อความ "มูลค่าลดเกินมูลค่าที่ลดได้ของบรรทัด: {item}" · บล็อก | ☐ |

### TC-10 — คำอธิบายเหตุผล <10 → บล็อก (negative · FN-10 · BR-05)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-10 / AC-10 / BR-05 / BR_REASON_TEXT_TOO_SHORT
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s2
- ชุดข้อมูล: RT-SHORT / RT-OK

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **คำอธิบายเหตุผล** | RT-SHORT ("ชำรุด") | field-error **ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร** · บล็อกไปต่อ/ส่ง | ☐ |
| 2 | TYPE → **คำอธิบายเหตุผล** | RT-OK | error หาย · ไปต่อได้ | ☐ |

---

## G4 · ส่วนลดท้ายบิล (FN-19 · BR-11/12 · LD-05 · AC-19)

### TC-19a — end-bill (฿) ลด VAT ถูกต้อง ม.86/10 (happy · calc · BR-12)
- group: end-bill · ความสำคัญ: สูง · trace: FN-19 / AC-19(a) / BR-12 / ENG cn-totals
- actor: เจ้าหน้าที่ลูกหนี้
- Setup: role=officer-ar · seed=INV-A (มีบรรทัดคิด VAT) · files=—
- Start: OPEN `#/create` → INV-A → s2 (ครบ) → s3
- ชุดข้อมูล: EB-OK-AMT
- ผ่านเมื่อ: summary แสดงฐานภาษีหลังหัก + VAT คิดจากฐานใหม่ + grand ลดลง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN s3 → VERIFY+จดสรุปยอด (ก่อนเปิด end-bill) | — | จด: ราคาก่อน VAT=before · ภาษีมูลค่าเพิ่ม (VAT)=vat · ยอดรวมหลัง VAT=after · ยอดสุทธิทั้งหมด=after (อ้าง step ถัดไป) | ☐ |
| 2 | TOGGLE เปิด **ส่วนลดท้ายบิล** (การ์ด FN-19) | — | ช่อง mode ฿/% + value + ข้อความ "ลดได้สูงสุด ฿X" ปรากฏ | ☐ |
| 3 | SELECT mode = **฿** · TYPE value | EB-OK-AMT (≤ ebCap) | summary เพิ่มแถว "ส่วนลดท้ายบิล · ลดฐานภาษี −฿ebBase" | ☐ |
| 4 | VERIFY แถว **ฐานภาษีหลังหักส่วนลด** | — | = before − ebBase (น้อยกว่า before ที่จดใน step 1) | ☐ |
| 5 | VERIFY แถว **ภาษีมูลค่าเพิ่ม (VAT) · คิดจากฐานใหม่ (ม.86/10)** | — | = vat − ebVat โดย ebVat = ebAmt×(vat/after) · **น้อยกว่า vat เดิม** | ☐ |
| 6 | VERIFY แถว **ยอดสุทธิทั้งหมด** | — | = max(0, after − ebAmt) · น้อยกว่ายอดสุทธิที่จดใน step 1 | ☐ |

### TC-19b — end-bill เกิน cap → block submit (negative · BR-11)
- group: end-bill · ความสำคัญ: สูง · trace: FN-19 / AC-19(b) / BR-11 / BR_ENDBILL_EXCEEDS_CAP
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s3
- ชุดข้อมูล: EB-OVER
- ผ่านเมื่อ: hard-warn + block submit · net ไม่ติดลบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE เปิด **ส่วนลดท้ายบิล** | — | card เปิด | ☐ |
| 2 | TYPE value เกิน ebCap | EB-OVER (สูงกว่ายอด after) | hard-warn "ส่วนลดท้ายบิลเกินยอดที่ลดได้ — สูงสุด ฿X · ที่กรอก ฿Y ... (ยอดสุทธิห้ามติดลบ)" | ☐ |
| 3 | VERIFY แถว **ยอดสุทธิทั้งหมด** | — | grand = 0 (ไม่ติดลบ — clamp) | ☐ |
| 4 | OPEN s5 → CLICK **บันทึกและส่งอนุมัติ** | — | ถูกบล็อก · ข้อความ "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)" · ไม่เปิด submit modal | ☐ |
| 5 | TYPE value ลดให้ ≤ ebCap | ≤ ebCap | hard-warn หาย · ส่งได้ | ☐ |

### TC-19c — DOA tier คิดจาก grand หลัง end-bill (E2E · LD-05)
- group: end-bill · ความสำคัญ: สูง · trace: FN-19 / AC-19(c) / AC-11 / BR-07 / LD-05 / LOCK-05
- Setup: role=officer-ar · seed=INV-D (ยอดสูง 770,400) · files=—
- Start: OPEN `#/create` → INV-D → s2 (ครบ) → s3
- ผ่านเมื่อ: ปรับ end-bill ให้ grand ข้าม tier แล้วสายอนุมัติเปลี่ยนตาม grand หลังหัก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN s3 → ตั้งยอดให้ grand > 300,000 (ยังไม่เปิด end-bill) | — | จด grand (อ้าง step ถัดไป) | ☐ |
| 2 | OPEN s5 → VERIFY DOA preview | — | tier 3 · สาย ผจก.ขาย → ผจก.บัญชี → CFO | ☐ |
| 3 | กลับ s3 → TOGGLE end-bill → TYPE ให้ grand ลดมาอยู่ 50,000.01–300,000 | ค่าที่ทำให้ grand เข้า tier 2 | grand ลดลงตามที่ตั้ง | ☐ |
| 4 | OPEN s5 → VERIFY DOA preview อีกครั้ง | — | tier **เปลี่ยนเป็น 2** · สาย ผจก.ขาย → ผจก.บัญชี (ไม่มี CFO) — พิสูจน์คิดจาก grand หลัง end-bill | ☐ |

### TC-19d — end-bill mode % (happy · calc)
- group: end-bill · ความสำคัญ: กลาง · trace: FN-19 / BR-12
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s3
- ชุดข้อมูล: EB-OK-PCT (5%)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE เปิด end-bill → SELECT mode **%** → TYPE | 5 | ebRaw = after × 5% · summary แถว "ส่วนลดท้ายบิล (5%) · ลดฐานภาษี" | ☐ |
| 2 | VERIFY netVat/netBefore | — | คำนวณตามสัดส่วน (ปัด 2 ตำแหน่ง) เหมือน mode ฿ | ☐ |

### TC-19e — end-bill + คงค้าง (net ≤ outstanding) (boundary · BR-11+BR-02)
- group: end-bill · ความสำคัญ: กลาง · trace: FN-19 / BR-11 / BR-02
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ตั้งบรรทัด + end-bill ให้ grand = available พอดี | — | ไม่มี hard-warn ยอดเกิน · ส่งได้ (net ≤ คงค้าง) | ☐ |

### TC-19f — ปิด end-bill กลับ → VAT กลับเป็นปกติ (happy · toggle off)
- group: end-bill · ความสำคัญ: กลาง · trace: FN-19 / BR-12
- Setup: role=officer-ar · seed=INV-A · files=—
- Start: OPEN `#/create` → INV-A → s3 (เปิด end-bill แล้ว)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด netVat ขณะ end-bill เปิด | — | จดค่า netVat (ลดแล้ว) | ☐ |
| 2 | TOGGLE ปิด **ส่วนลดท้ายบิล** | — | summary กลับเป็น "ภาษีมูลค่าเพิ่ม (VAT)" (ไม่มี "คิดจากฐานใหม่") + "ยอดรวมหลัง VAT" · VAT = vat เดิม > netVat ที่จด | ☐ |

### TC-19g — end-bill VAT-inclusive/หลายอัตรา แบ่งตามสัดส่วน (edge · EC-CALC-01)
- group: end-bill · ความสำคัญ: ต่ำ · trace: FN-19 / BR-12 / EC-CALC-01 `[AI-DEFAULT]`
- Setup: role=officer-ar · seed=INV ที่มีบรรทัด VAT-inclusive (NET) ปน · files=—
- Start: OPEN `#/create` → เลือกใบ → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ตั้งบรรทัดคละ VAT (add/included/none) → เปิด end-bill | — | ebVat = ebAmt × (vat/after) แบ่งตามสัดส่วน VAT ในยอดรวม (ปัด 2 ตำแหน่ง) `[AI-DEFAULT]` | ☐ |

---

## G5 · ส่งอนุมัติ + DOA (FN-11 · AC-11)

### TC-11a — เลือกผู้อนุมัติครบ → pending (happy · FN-11)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-11 / AC-11 / BR-07 / LOCK-05
- actor: เจ้าหน้าที่ลูกหนี้
- Setup: role=officer-ar (U-AR) · seed=draft ที่ valid (grand tier 1) · files=—
- Start: OPEN `#/view/<draftId>` → CLICK **ส่งอนุมัติ**
- ผ่านเมื่อ: chain freeze → pending_approval

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด หัวข้อ "ส่งอนุมัติใบลดหนี้ (ร่าง)" · หัวข้อสาย "สายอนุมัติ (DOA-ACC-CN · tier X) — เลือกผู้อนุมัติแต่ละขั้น *" | ☐ |
| 2 | VERIFY slot ตาม tier | — | tier 1 → 1 slot (ผจก.ขาย · ขั้นสุดท้าย) | ☐ |
| 3 | SELECT ผู้อนุมัติในแต่ละ slot | U-SALES (มานพ) | slot แสดง chip ชื่อผู้อนุมัติ + ปุ่มเปลี่ยน | ☐ |
| 4 | CLICK **ส่งอนุมัติ** (ปุ่ม modal) | — | toast "ส่งเพื่ออนุมัติแล้ว — My Approval ของ มานพ" · pill=รออนุมัติ | ☐ |
| 5 | VERIFY view หลังส่ง | — | สถานะ N/N ขั้น · ปุ่ม (สำหรับ owner) เหลือ **ยกเลิก** | ☐ |

### TC-11b — slot ไม่ครบ → บล็อก (negative · FN-11)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-11 / AC-11 / BR_SLOT_INCOMPLETE
- Setup: role=officer-ar · seed=draft valid tier 2 (2 slot) · files=—
- Start: OPEN `#/view/<draftId>` → CLICK **ส่งอนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด 2 slot | ☐ |
| 2 | SELECT เฉพาะ slot 1 (เว้น slot 2) | U-SALES | slot 2 ยังว่าง | ☐ |
| 3 | CLICK **ส่งอนุมัติ** | — | บล็อก · toast **เลือกผู้อนุมัติให้ครบทุกขั้น** · slot 2 ขึ้น "เลือกผู้อนุมัติขั้นนี้" | ☐ |

### TC-11c — สายอนุมัติเปลี่ยนตามมูลค่า (tier 1/2/3) (happy · BR-07 · LOCK-05)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-11 / BR-07 / DOA tier matrix / LOCK-05
- Setup: role=officer-ar · seed=draft 3 ใบ grand tier1/tier2/tier3 · files=—
- Start: OPEN `#/view/<id>` แต่ละใบ → CLICK **ส่งอนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด submit modal ใบ tier 1 (grand ≤50,000) | DOA-T1 | 1 slot: ผจก.ขาย | ☐ |
| 2 | เปิด submit modal ใบ tier 2 (50,000.01–300,000) | DOA-T2 | 2 slot: ผจก.ขาย → ผจก.บัญชี | ☐ |
| 3 | เปิด submit modal ใบ tier 3 (>300,000) | DOA-T3 | 3 slot: ผจก.ขาย → ผจก.บัญชี → CFO (ขั้นสุดท้าย) | ☐ |

### TC-11d — DOA preview ที่ s5 ตรงกับ submit modal (happy)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: FN-11 / step5Extra resolveDoa
- Setup: role=officer-ar · seed=INV-D → grand tier 3 · files=—
- Start: OPEN `#/create` → INV-D → ... → s5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY DOA preview ที่ s5 | — | แสดง tier + สายอนุมัติตาม grand | ☐ |
| 2 | บันทึกร่าง → เปิด submit modal | — | จำนวน slot ตรงกับ preview | ☐ |

### TC-11e — tier boundary 50,000.00 vs 50,000.01 (boundary)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: FN-11 / DOA tier matrix (boundary)
- Setup: role=officer-ar · seed=draft grand=50,000.00 และอีกใบ grand=50,000.01 · files=—
- Start: OPEN `#/view/<id>` → **ส่งอนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด submit modal ใบ grand=50,000.00 | — | tier 1 (1 slot) | ☐ |
| 2 | เปิด submit modal ใบ grand=50,000.01 | — | tier 2 (2 slot) | ☐ |

---

## G6 · อนุมัติ / ไม่อนุมัติ / re-check / SoD (FN-12/13/17/14)

### TC-12 — อนุมัติครบสาย → เลข CN no-gap (E2E · FN-12)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-12 / AC-12 / BR-08 / LOCK-06 / XT-01
- actor: ผู้อนุมัติ (ตามขั้น)
- Setup: role สลับตามขั้น (U-SALES→U-ACC→U-CFO ตาม tier) · seed=ใบ pending tier ที่ต้องการ · files=—
- Start: OPEN `#/view/<pendingId>` (login ผู้อนุมัติขั้นปัจจุบัน)
- ผ่านเมื่อ: อนุมัติขั้นสุดท้าย → ออกเลข CN-YYYY-NNNN

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สลับ persona เป็นผู้อนุมัติขั้น 1 (U-SALES) → OPEN view | — | เห็นปุ่ม **อนุมัติ** + **ไม่อนุมัติ** | ☐ |
| 2 | CLICK **อนุมัติ** (ขั้นกลาง) | — | toast "อนุมัติขั้น 1 แล้ว — ส่งต่อ {ชื่อ}" · ขั้นถัดไป pending | ☐ |
| 3 | สลับ persona เป็นผู้อนุมัติขั้นสุดท้าย → CLICK **อนุมัติ** | — | toast **อนุมัติครบสาย — ออกใบลดหนี้ CN-YYYY-NNNN · ลดยอดคงค้าง {inv}** | ☐ |
| 4 | VERIFY สถานะ + เลข | — | pill = **อนุมัติแล้ว · รอส่ง** · ช่องเลขที่ = CN-YYYY-NNNN (ไม่ใช่ "(ออกเลขเมื่ออนุมัติครบ)") | ☐ |

### TC-12b — เลข CN ออกเฉพาะ final approve (no-gap · negative timing)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-12 / BR-08 / LOCK-06
- Setup: role=officer-ar · seed=ใบ draft และใบ pending · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เลขที่ใบ draft | — | "(ออกเลขเมื่ออนุมัติครบ)" — ยังไม่มีเลข | ☐ |
| 2 | VERIFY เลขที่ใบ pending (ยังไม่ครบสาย) | — | ยังไม่มีเลข CN (ออกเมื่อ final approve เท่านั้น) | ☐ |

### TC-13 — ไม่อนุมัติ + เหตุผล → กลับร่าง + badge (E2E · FN-13)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-13 / AC-13 / EC-06 / FN-91
- actor: ผู้อนุมัติ
- Setup: role=U-SALES (ผู้อนุมัติขั้นปัจจุบัน) · seed=ใบ pending · files=—
- Start: OPEN `#/view/<pendingId>` (login ผู้อนุมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** | — | modal ใส่เหตุผล (บังคับ) | ☐ |
| 2 | CLICK ยืนยันโดยเว้นเหตุผล | — | บล็อก (เหตุผลบังคับ) | ☐ |
| 3 | TYPE เหตุผล → ยืนยัน | "จำนวนไม่ตรงกับใบรับคืน" | toast **ตีกลับเพื่อแก้ไข** · pill กลับเป็น **ฉบับร่าง** | ☐ |
| 4 | VERIFY badge บน view (owner) | — | badge **ถูกตีกลับ 1 ครั้ง** | ☐ |
| 5 | OPEN tab **ลายเซ็น · อนุมัติ** | — | เห็น approval_history รอบที่ถูกตีกลับ + เหตุผล | ☐ |

### TC-13b — ตีกลับหลายรอบ → นับสะสม (edge · EC-06)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-13 / EC-06 / FN-91
- Setup: role สลับ maker/approver · seed=ใบเคยถูกตีกลับ 1 ครั้ง · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ส่งอนุมัติใหม่ → ผู้อนุมัติ **ไม่อนุมัติ** อีกครั้ง (มีเหตุผล) | — | badge **ถูกตีกลับ 2 ครั้ง** | ☐ |
| 2 | OPEN tab ประวัติ/ลายเซ็น | — | เห็นทั้ง 2 รอบ (append-only ไม่ทับ) | ☐ |

### TC-14b — SoD: ผู้ส่งไม่เห็นปุ่มอนุมัติใบตัวเอง (permission · FN-14)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-14 / AC-14 / BR-07 / §5.3 SoD
- actor: เจ้าหน้าที่ลูกหนี้ (ผู้ส่ง)
- Setup: role=U-AR (ผู้ส่งใบนี้เอง) · seed=ใบ pending ที่ U-AR เป็นผู้ส่ง · files=—
- Start: OPEN `#/view/<pendingId>` (login เป็นผู้ส่ง)
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ · เห็นแค่ยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบปุ่ม view (pending · เป็นผู้ส่งเอง) | — | **ไม่มีปุ่ม "อนุมัติ"** และ **ไม่มี "ไม่อนุมัติ"** | ☐ |
| 2 | VERIFY ปุ่มที่มี | — | เห็นเฉพาะ **ยกเลิก** (ถอนจากรออนุมัติ) | ☐ |

### TC-17 — outstanding ลดระหว่างรอ → อนุมัติไม่ได้ (E2E · FN-17 · EC-01)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-17 / AC-17 / BR-02 / EC-01 / BR_APPROVE_EXCEEDS_OUTSTANDING / LOCK-04
- actor: ผู้อนุมัติขั้นสุดท้าย
- Setup: role สลับ · seed=ใบ pending ขั้นสุดท้าย · files=— · (ต้อง simulate ผ่าน demoPay ในหน้า ref tab)
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN tab **ใบแจ้งหนี้อ้างอิง · ภาษีขาย** → VERIFY+จด คงค้าง | — | จดยอดคงค้างก่อน (อ้าง step ถัดไป) | ☐ |
| 2 | CLICK **จำลองรับชำระ** (demoPay · เฉพาะ pending) จนคงค้าง < grand | — | คงค้างของใบเดิมลดลงต่ำกว่ายอดลดหนี้ | ☐ |
| 3 | สลับ persona ผู้อนุมัติขั้นสุดท้าย → CLICK **อนุมัติ** | — | ถูกบล็อก · ข้อความ "อนุมัติไม่ได้ — ยอดคงค้าง {inv} เหลือ ฿X น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้" | ☐ |
| 4 | VERIFY สถานะ | — | ยังเป็น pending (ไม่ออกเลข CN) | ☐ |

### TC-P07 — ไม่ใช่ผู้มีสิทธิ์ขั้นปัจจุบัน → อนุมัติไม่ได้ (permission)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-14 / §5.3 / ERR_NOT_CURRENT_APPROVER
- Setup: role=U-CFO (ขั้น 3) · seed=ใบ pending ที่ยังอยู่ขั้น 1 · files=—
- Start: OPEN `#/view/<pendingId>` (login CFO)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | CFO ยังไม่ถึงคิว → ไม่มีปุ่มอนุมัติ (ไม่ใช่ผู้มีสิทธิ์ขั้นปัจจุบัน) | ☐ |

---

## G7 · ยกเลิก / ส่งลูกค้า / ออกเอกสารแก้ไข (FN-15/16)

### TC-15 — ยกเลิก draft/pending + เหตุผล → คืน held (E2E · FN-15 · EC-05)
- group: ยกเลิก · ความสำคัญ: สูง · trace: FN-15 / AC-15 / EC-05 / BR-10 / XT-04
- actor: เจ้าหน้าที่ลูกหนี้ (owner)
- Setup: role=U-AR · seed=ใบ draft/pending ที่มี cn_held · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ref tab → VERIFY+จด กันยอด (held) + คงค้าง | — | จด held และ available (อ้าง step ถัดไป) | ☐ |
| 2 | CLICK **ยกเลิก** | — | modal ใส่เหตุผล (บังคับ) | ☐ |
| 3 | CLICK ยืนยันเว้นเหตุผล | — | บล็อก (เหตุผลบังคับ) | ☐ |
| 4 | TYPE เหตุผล → ยืนยัน | "ลูกค้าขอยกเลิกคำขอ" | toast **ยกเลิกเรียบร้อย** · pill=ยกเลิก | ☐ |
| 5 | VERIFY banner บน view | — | note.danger "ยกเลิก โดย {ชื่อ} · {เหตุผล}" | ☐ |
| 6 | OPEN ใบเดิม/ref → VERIFY held คืน | — | held ลดลง = ยอดใบนี้ · available เพิ่มกลับเท่าที่จดใน step 1 | ☐ |

### TC-15b — ยกเลิก pending (ผู้ส่ง) (happy)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: FN-15 / §5.2
- Setup: role=U-AR (ผู้ส่ง) · seed=ใบ pending · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → TYPE เหตุผล → ยืนยัน | "ถอนคำขอ" | pill=ยกเลิก · toast ยกเลิกเรียบร้อย | ☐ |

### TC-16 — ส่งให้ลูกค้า (approved→sent) (E2E · FN-16)
- group: ส่งลูกค้า · ความสำคัญ: กลาง · trace: FN-16 / AC-16 / DOC-STORE
- actor: เจ้าหน้าที่ลูกหนี้
- Setup: role=U-AR · seed=ใบ approved (มีเลข CN) · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม (approved) | — | **ออกเอกสารแก้ไข** + **ส่งให้ลูกค้า** | ☐ |
| 2 | CLICK **ส่งให้ลูกค้า** → ยืนยัน | — | toast "ส่ง CN-YYYY-NNNN ให้ลูกค้าแล้ว" · pill=**ส่งลูกค้าแล้ว** | ☐ |

### TC-16b — ส่งสำเนาซ้ำ (resend) ไม่เปลี่ยนวันที่ส่งเดิม (edge · FN-16)
- group: ส่งลูกค้า · ความสำคัญ: กลาง · trace: FN-16 / AC-16
- Setup: role=U-AR · seed=ใบ sent · files=—
- Start: OPEN `#/view/<sentId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม (sent) | — | **ออกเอกสารแก้ไข** + **ส่งสำเนาซ้ำ** | ☐ |
| 2 | OPEN detail → VERIFY+จด วันที่ส่งเดิม | — | จดวันที่ส่ง (อ้าง step ถัดไป) | ☐ |
| 3 | CLICK **ส่งสำเนาซ้ำ** → ยืนยัน | — | toast "ส่งสำเนา CN-YYYY-NNNN ซ้ำแล้ว" · สถานะยังเป็น ส่งลูกค้าแล้ว | ☐ |
| 4 | VERIFY วันที่ส่ง | — | = วันที่ส่งเดิมที่จดใน step 2 (ไม่เปลี่ยน) | ☐ |

### TC-NEG-05 — ออกเอกสารแก้ไข = display-only (negative · XT-05 · LD-04)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: XT-05 / LD-04 / OQ-CN-02
- Setup: role=U-AR · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ref tab → VERIFY+จด คงค้างหลังใบนี้ | — | จดยอด (อ้าง step ถัดไป) | ☐ |
| 2 | CLICK **ออกเอกสารแก้ไข** → ยืนยัน | — | เป็น display-only (mark เท่านั้น) · **ไม่เปลี่ยนสถานะ** (ยังเป็น approved/sent) | ☐ |
| 3 | VERIFY ref tab คงค้าง | — | คงค้าง = ค่าที่จดใน step 1 (ไม่ถอนยอด) | ☐ |

### TC-P06 — CFO อนุมัติขั้น 3 (tier 3) (permission · happy)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-12 / §5.3 (cfo approve tier3)
- Setup: role=U-CFO · seed=ใบ pending tier3 อยู่ขั้น 3 · files=—
- Start: OPEN `#/view/<id>` (login CFO)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | CFO เห็นปุ่ม **อนุมัติ** (ขั้นสุดท้าย) | ☐ |
| 2 | CLICK **อนุมัติ** | — | ออกเลข CN · pill=อนุมัติแล้ว | ☐ |

---

## G8 · View tabs: ref / history / pdf (FN-18/91/92)

### TC-18 — ref tab: คงค้างก่อน/หลัง + ภาษีขาย + JE (UI · FN-18)
- group: view-ref · ความสำคัญ: กลาง · trace: FN-18 / AC-18 / BR-09 / LOCK-07 / XT-01/03
- Setup: role=U-AR · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>` → CLICK tab **ใบแจ้งหนี้อ้างอิง · ภาษีขาย**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วนใบเดิม | — | ยอดสุทธิใบเดิม · รับชำระ · ลดแล้ว · **คงค้างก่อน** · **คงค้างหลังใบนี้** · กันยอด | ☐ |
| 2 | VERIFY คงค้างหลังใบนี้ | — | = คงค้างก่อน − grand ของใบนี้ | ☐ |
| 3 | VERIFY ส่วน **ผลกระทบภาษีขาย (VAT Report ภ.พ.30)** | — | เดือนภาษีที่ลด = เดือน cnDate (ม.82/10) · ฐานภาษีที่ลด = netBefore · ภาษีขายที่ลด = netVat | ☐ |
| 4 | VERIFY ส่วน **รายการบัญชี (จำลอง)** JE | — | Dr 4110/4120 = netBefore · Dr 2150 = netVat · Cr 1130 = grand | ☐ |

### TC-18b — JE บัญชีตาม reason (RET/QTY=4110 · DISC/PRICE=4120) (UI · BR-09)
- group: view-ref · ความสำคัญ: ต่ำ · trace: FN-18 / BR-09 / BR-12
- Setup: role=U-AR · seed=ใบ approved 2 ใบ (reason RET และ DISC) · files=—
- Start: OPEN `#/view/<id>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY JE ใบ reason RET/QTY | — | บัญชี Dr = **4110** (รับคืน/ลดรายได้) | ☐ |
| 2 | VERIFY JE ใบ reason DISC/PRICE | — | บัญชี Dr = **4120** (ส่วนลดจ่าย) | ☐ |

### TC-91 — ประวัติ append-only ทุกการกระทำ (E2E · FN-91)
- group: view-history · ความสำคัญ: กลาง · trace: FN-91 / AC-91 / BR-13 / LOCK-10
- Setup: role สลับ · seed=ใบที่ผ่าน สร้าง→ส่ง→อนุมัติ→ส่งลูกค้า · files=—
- Start: OPEN `#/view/<sentId>` → CLICK tab **ประวัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รายการประวัติ | — | เห็น: สร้าง · ส่งอนุมัติ · อนุมัติแต่ละขั้น · ออกเลข · ส่งลูกค้า (เรียงตามเวลา) | ☐ |
| 2 | VERIFY วันที่ | — | ทุกวันที่เป็น **ค.ศ.** | ☐ |
| 3 | VERIFY ไม่มีปุ่มลบ/แก้ประวัติ | — | ไม่มีปุ่ม ลบ/แก้ไข รายการประวัติ (append-only) | ☐ |

### TC-91b — ประวัติเก็บรอบตีกลับ (append-only · FN-91)
- group: view-history · ความสำคัญ: ต่ำ · trace: FN-91 / EC-06
- Setup: role สลับ · seed=ใบเคยถูกตีกลับ · files=—
- Start: OPEN `#/view/<id>` → tab ประวัติ / ลายเซ็น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รอบตีกลับ | — | รอบก่อนหน้ายังอยู่ (ไม่ถูกทับ) | ☐ |

### TC-92 — PDF ครบตาม ม.86/10 (UI · FN-92)
- group: view-pdf · ความสำคัญ: กลาง · trace: FN-92 / AC-92 / BR-15 / LOCK-06/10
- Setup: role=U-AR · seed=ใบ approved (มีเลข CN) · files=—
- Start: OPEN `#/view/<approvedId>` → CLICK tab **PDF Preview**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว PDF | — | เลข CN-YYYY-NNNN · **อ้างเลข + วันที่ใบแจ้งหนี้เดิม** | ☐ |
| 2 | VERIFY ตารางมูลค่า | — | **มูลค่าเดิม · มูลค่าที่ถูกต้อง · ผลต่าง** · ภาษี (netVat) | ☐ |
| 3 | VERIFY เหตุผล + legal_basis | — | เหตุผล + legal_basis (ม.86/10) พิมพ์ลง PDF | ☐ |
| 4 | VERIFY วันที่ | — | วันที่บน PDF เป็น **ค.ศ.** | ☐ |
| 5 | CLICK ปุ่มดาวน์โหลด PDF | — | ดาวน์โหลดไฟล์ PDF | ☐ |

---

## G9 · Status guards + Negatives

### TC-GRD-01 — submit เฉพาะ draft (negative · guard)
- group: guards · ความสำคัญ: สูง · trace: §5.2 / BR_SUBMIT_DRAFT_ONLY
- Setup: role=U-AR · seed=ใบ pending/approved · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มส่งอนุมัติในใบ pending | — | ไม่มีปุ่ม "ส่งอนุมัติ" (ไม่ใช่ draft) | ☐ |
| 2 | (ถ้ามีทางลัด) พยายาม submit ใบ non-draft | — | toast **ส่งอนุมัติได้เฉพาะฉบับร่าง** | ☐ |

### TC-GRD-02 — edit เฉพาะ draft (negative · guard)
- group: guards · ความสำคัญ: สูง · trace: §5.2 / BR_EDIT_DRAFT_ONLY
- Setup: role=U-AR · seed=ใบ approved (id ทราบ) · files=—
- Start: OPEN `#/edit/<approvedId>` (พิมพ์ route ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/<approvedId>` | — | toast **แก้ไขได้เฉพาะฉบับร่าง** · เด้งไป `#/view/<id>` | ☐ |

### TC-GRD-03 — cancel เฉพาะ draft/pending (negative · guard)
- group: guards · ความสำคัญ: สูง · trace: §5.2 / BR_CANCEL_STATE_INVALID
- Setup: role=U-AR · seed=ใบ approved/sent · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มยกเลิกในใบ approved | — | ไม่มีปุ่ม "ยกเลิก" (มีแต่ ออกเอกสารแก้ไข/ส่งให้ลูกค้า) | ☐ |
| 2 | (ถ้ามีทางลัด row menu) พยายามยกเลิก | — | toast **ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ "ออกเอกสารแก้ไข"** | ☐ |

### TC-GRD-04 — send เฉพาะ approved (negative · guard)
- group: guards · ความสำคัญ: กลาง · trace: §5.2 / BR_SEND_STATE_INVALID
- Setup: role=U-AR · seed=ใบ draft/pending · files=—
- Start: OPEN `#/view/<draftId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มส่งให้ลูกค้าในใบ draft/pending | — | ไม่มีปุ่ม "ส่งให้ลูกค้า" (ต้องอนุมัติครบก่อน) | ☐ |

### TC-14a — tile ลดลอยปิด (negative · = FN-02 confirm)
- group: negatives · ความสำคัญ: สูง · trace: FN-02 / BR-14 / AC-14
- Setup: role=U-AR · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tile **ลดหนี้ไม่อ้างใบ** | — | toast **ลดหนี้ไม่อ้างใบแจ้งหนี้ถูกปิดไว้ (OQ-CN-01)** · tile ยัง disabled | ☐ |

### TC-13c — ใบ void/ชำระครบ ไม่โผล่ (negative · FN-04 · EC-03/04)
- group: negatives · ความสำคัญ: กลาง · trace: FN-04 / AC-13 / BR-01 / EC-03/04
- Setup: role=U-AR · seed=INV-VOID + INV-PAID · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY picker | — | ไม่มี INV-2026-0143 (void) และ INV-2026-0136 (ชำระครบ) | ☐ |

### TC-NEG-03 — refund เมื่อชำระครบ ไม่รองรับ (negative · out of scope)
- group: negatives · ความสำคัญ: กลาง · trace: OOS (§0.3) / OQ-CN-03
- Setup: role=U-AR · seed=INV-PAID · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไม่มีทางเลือกใบชำระครบเพื่อลด/คืนเงิน | — | ใบชำระครบไม่โผล่ · ไม่มีปุ่ม refund/คืนเงิน ในทั้ง flow | ☐ |

### TC-NEG-04 — no hard delete (negative · BR-13)
- group: negatives · ความสำคัญ: สูง · trace: BR-13 / FN-91 / LOCK-10
- Setup: role=U-AR · seed=ใบหลายสถานะ · files=—
- Start: OPEN `#/list` และ `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY row menu ⋮ | — | ไม่มีเมนู "ลบ" (มีแค่ ดูรายละเอียด/แก้ไข(draft)/ทำสำเนา/พิมพ์/ยกเลิก) | ☐ |
| 2 | VERIFY ใน view | — | ไม่มีปุ่มลบเอกสาร · ยกเลิก = เปลี่ยนสถานะ cancelled (ไม่หายจาก list) | ☐ |

### TC-LK-09 — UI #67.1: อนุญาตเฉพาะ hard-warn/field-error/danger (LOCK-09)
- group: negatives · ความสำคัญ: ต่ำ · trace: LOCK-09 / 01_UI §1.6
- Setup: role=U-AR · seed=INV-A · files=—
- Start: OPEN `#/create` → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ข้อความช่วยเหลือบนฟอร์ม | — | มีเฉพาะ hard-warn (ยอดเกิน) · field-error/บรรทัดเกิน · note.danger (ยกเลิก) — **ไม่มี hint/info banner อื่น** | ☐ |

---

## G10 · Permission matrix (SoD · §5.3)

### TC-P01 — officer-ar ทำ create/edit/submit/cancel/send ได้ (permission · allow)
- group: permission · ความสำคัญ: สูง · trace: §5.3 (officer-ar allow)
- Setup: role=U-AR · seed=ใบ draft/approved ของ officer · files=—
- Start: OPEN `#/list` / `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มสร้าง | — | เห็นปุ่ม **สร้างใบลดหนี้** | ☐ |
| 2 | VERIFY view ใบ draft | — | เห็น ยกเลิก/แก้ไข/ส่งอนุมัติ | ☐ |
| 3 | VERIFY view ใบ approved | — | เห็น ส่งให้ลูกค้า | ☐ |

### TC-P02 — mgr-sales สร้างไม่ได้ (permission · deny)
- group: permission · ความสำคัญ: สูง · trace: §5.3 (mgr create = —)
- Setup: role=U-SALES · seed=— · files=—
- Start: OPEN `#/list` (login ผจก.ขาย)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มสร้าง | — | ผจก.ขายไม่ควรสร้างได้ (create = officer-ar เท่านั้น) — ปุ่มสร้างไม่ทำงาน/ไม่มีสิทธิ์สร้าง | ☐ |

### TC-P03 — mgr-sales อนุมัติขั้น 1 ได้ (permission · allow)
- group: permission · ความสำคัญ: สูง · trace: §5.3 (mgr-sales approve ขั้น1)
- Setup: role=U-SALES · seed=ใบ pending อยู่ขั้น 1 · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | เห็น **อนุมัติ** + **ไม่อนุมัติ** (ขั้น 1) | ☐ |

### TC-P04 — mgr-acc อนุมัติขั้น 2 (tier2+) ได้ (permission · allow)
- group: permission · ความสำคัญ: กลาง · trace: §5.3 (mgr-acc approve ขั้น2)
- Setup: role=U-ACC · seed=ใบ pending tier2 ถึงขั้น 2 · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | ผจก.บัญชีเห็น **อนุมัติ** (ขั้น 2) | ☐ |

### TC-P05 — owner อนุมัติใบตัวเองไม่ได้ (permission · deny · SoD)
- group: permission · ความสำคัญ: สูง · trace: §5.3 / BR-07 / FN-14
- Setup: role=U-AR (ผู้ส่งเอง มีบทบาทซ้อน) · seed=ใบ pending ที่ตัวเองส่ง · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | ไม่มีปุ่มอนุมัติ (submitted_by === actor → canActStep false) · เห็นแค่ ยกเลิก | ☐ |

### TC-P08 — ทุก role ดูรายละเอียดได้ (permission · view allow)
- group: permission · ความสำคัญ: ต่ำ · trace: §5.3 (View = ทุก role)
- Setup: role=U-SALES/U-ACC/U-CFO · seed=ใบใด ๆ · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เปิด view ได้ทุก role | — | ทุก role เปิดดูรายละเอียด/tabs ได้ (action ต่างกันตามสิทธิ์) | ☐ |

### TC-P09 — cfo อนุมัติเฉพาะ tier3 (permission · scope)
- group: permission · ความสำคัญ: ต่ำ · trace: §5.3 (cfo ขั้น3 tier3)
- Setup: role=U-CFO · seed=ใบ pending tier1/tier2 (ไม่มีขั้น CFO) · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มในใบ tier1/tier2 | — | CFO ไม่มีปุ่มอนุมัติ (สายไม่มีขั้น CFO) | ☐ |

---

## G11 · Cross-module (XT-01..06 · §6.9)

### TC-X01 — approve → ar_open_item cn_applied↑ / outstanding ลด (XT-01)
- group: cross-module · ความสำคัญ: สูง · trace: XT-01 / BR-02/09 / FN-18
- Setup: role สลับ · seed=ใบ pending + ใบเดิม INV-A มี outstanding · files=— · (prototype: ตรวจผลที่ ref tab แทนหน้า AR จริง)
- Start: OPEN `#/view/<pendingId>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ref tab → VERIFY+จด คงค้างก่อน | — | จดคงค้างก่อน (อ้าง step ถัดไป) | ☐ |
| 2 | อนุมัติครบสาย (สลับ persona) | — | toast อนุมัติครบสาย · ออกเลข CN | ☐ |
| 3 | OPEN ref tab อีกครั้ง | — | **คงค้างหลังใบนี้** = คงค้างก่อน − grand (ปิดเมื่อ = 0) | ☐ |

### TC-X02 — approve → ภ.พ.30 netVat เดือน cnDate (XT-02)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-02 / BR-12 / ม.82/10 / LOCK-07
- Setup: role=U-AR · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ผลกระทบภาษีขาย | — | output_vat_line (ค่าลบ) = netVat · เดือน = cnDate (ม.82/10) | ☐ |
| 2 | VERIFY stat tile P-01 "ภาษีขายที่ลดเดือนนี้" | — | รวม netVat ของ approved/sent เดือนนี้ | ☐ |

### TC-X03 — approve → JE mock (XT-03)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-03 / BR-09 / LOCK-08
- Setup: role=U-AR · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รายการบัญชี (จำลอง) | — | Dr 4110/4120 netBefore · Dr 2150 netVat · Cr 1130 grand · ป้าย "จำลอง" (demo) | ☐ |

### TC-X04 — cancel → held คืน (XT-04)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-04 / BR-10 / EC-05
- Setup: role=U-AR · seed=ใบ draft/pending มี held · files=—
- Start: OPEN `#/view/<id>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด กันยอด (held) | — | จด held ปัจจุบัน | ☐ |
| 2 | CLICK ยกเลิก + เหตุผล → ยืนยัน | "ยกเลิก" | pill=ยกเลิก | ☐ |
| 3 | OPEN ref/ใบเดิม → VERIFY available | — | held คืน · available เพิ่มกลับ = held ที่จด | ☐ |

### TC-X05 — ยกเลิกหลังอนุมัติไม่รองรับ → revise-doc (XT-05)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-05 / LD-04 (= TC-NEG-05)
- Setup: role=U-AR · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไม่มีปุ่มยกเลิก · มี "ออกเอกสารแก้ไข" | — | ยกเลิกหลังอนุมัติปิด · revise-doc display-only ไม่ถอนยอด | ☐ |

### TC-X06 — RET ผูก SR ใบเดียวกัน qty ≤ รับคืน (XT-06)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-06 / BR-06 (= TC-R01/R03)
- Setup: role=U-AR · seed=INV-A + SR-2026-0016 (ของใบเดียวกัน) · files=—
- Start: OPEN `#/create` → INV-A → RET

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตัวเลือกใบรับคืน | — | เฉพาะ SR ของ INV-A (ใบเดียวกัน) · qty ปิดที่จำนวนที่รับคืน | ☐ |

---

## G12 · Scope Lock verify (LOCK)

### TC-LK-01 — Pattern Q document + B2 v2 line editor (LOCK-01)
- group: scope-lock · ความสำคัญ: ต่ำ · trace: LOCK-01
- Setup: role=U-AR · seed=INV-A + ใบ approved · files=—
- Start: OPEN `#/create` → s3 และ OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY s3 line editor | — | ตารางบรรทัด B2 v2 (สินค้า/จำนวน/หน่วย/ราคา/ส่วนลด%/ภาษี/จำนวนเงิน) · สินค้า lock | ☐ |
| 2 | VERIFY view drawer | — | 5 tabs (รายละเอียด/ใบแจ้งหนี้อ้างอิง·ภาษีขาย/PDF Preview/ลายเซ็น·อนุมัติ/ประวัติ) | ☐ |

### TC-LK-10 — ค.ศ. ทุกที่ + append-only (LOCK-10)
- group: scope-lock · ความสำคัญ: ต่ำ · trace: LOCK-10 / BR-13
- Setup: role=U-AR · seed=ใบ sent (ผ่านหลาย action) · files=—
- Start: OPEN `#/view/<sentId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY วันที่ทุก tab (detail/history/pdf) | — | เป็น ค.ศ. ทั้งหมด (ไม่มี พ.ศ.) | ☐ |
| 2 | VERIFY ประวัติ | — | append-only (ไม่มีลบ/แก้) | ☐ |

### TC-LK-06 — doccfg CN-YYYY-NNNN + PDF อ้างเลขใบเดิม (LOCK-06)
- group: scope-lock · ความสำคัญ: ต่ำ · trace: LOCK-06 / BR-08 / FN-92
- Setup: role=U-AR · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>` → tab PDF

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รูปแบบเลข | — | CN-YYYY-NNNN (ออกตอน final approve · no-gap) | ☐ |
| 2 | VERIFY PDF | — | อ้างเลข + วันที่ใบแจ้งหนี้เดิม | ☐ |

---

## G13 · Edge cases (EC)

### TC-CC-01 — concurrent approval → 409 (edge · ต้อง simulate)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-CC-01 / LD-02 / ERR_STALE_DATA / `[AI-DEFAULT]`
- Setup: role=ผู้อนุมัติ 2 session ขั้นเดียวกัน · seed=ใบ pending · files=— · **(ต้อง simulate: 2 client อนุมัติพร้อมกัน — API-level)**
- Start: OPEN `#/view/<pendingId>` 2 session

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อนุมัติจาก session A | — | สำเร็จ (first commit wins) | ☐ |
| 2 | อนุมัติจาก session B (version เก่า) | — | 409 ERR_STALE_DATA (version mismatch) `[AI-DEFAULT]` | ☐ |

### TC-ID-01 — double-submit idempotency (edge · ต้อง simulate)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-ID-01 / busyGate / ERR_DUPLICATE_IDEMPOTENCY_KEY
- Setup: role=U-AR · seed=draft valid · files=— · **(ต้อง simulate: กดส่ง/บันทึกซ้ำเร็ว ๆ)**
- Start: OPEN `#/view/<draftId>` → submit modal

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** (ปุ่ม modal) ซ้ำเร็ว ๆ 2 ครั้ง | — | busyGate กันซ้ำ · ไม่เกิด 2 ใบ/2 pending (cached response) | ☐ |

### TC-CALC-01 — ปัดเศษ ebVat 2 ตำแหน่ง (edge · `[AI-DEFAULT]`)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-CALC-01 / BR-12 / OQ-EB-01 `[AI-DEFAULT]`
- Setup: role=U-AR · seed=INV ที่ทำให้ ebVat มีเศษ · files=—
- Start: OPEN `#/create` → s3 → เปิด end-bill

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY netVat/ebBase | — | แสดงปัด 2 ตำแหน่ง (formatMoney) ตาม HTML totals() `[AI-DEFAULT]` | ☐ |

### TC-FU-01 — ไฟล์แนบ type/size (edge · `[AI-DEFAULT]`)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-FU-01 / OQ-FU-01 `[AI-DEFAULT]`
- Setup: role=U-AR · seed=draft · files=`cn-attach-ok.pdf`, `cn-attach-big.pdf`
- Start: OPEN `#/create` → s4 (เอกสารแนบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `cn-attach-ok.pdf` | jpg/png/pdf ≤10MB | แนบสำเร็จ `[AI-DEFAULT]` | ☐ |
| 2 | UPLOAD `cn-attach-big.pdf` (>10MB) | เกินขนาด | ถูกปฏิเสธ (ต้อง simulate ถ้า prototype ไม่บังคับ size) `[AI-DEFAULT]` | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `F-ACC-CN_credit-note.html` ใน browser. หน้าเริ่มที่ `#/list`.
2. **ตั้ง role** ผ่าน persona switcher (DEMO): เลือกบุคคลตาม `Setup: role=` ก่อนเริ่มเคส (U-AR/U-SALES/U-ACC/U-CFO).
3. แต่ละเคส **เริ่มที่ `Start` route ของตัวเอง** (refresh-safe) — ห้ามพึ่งสถานะค้างจากเคสก่อน. สำหรับเคสที่ต้องมี seed (draft/pending/approved) ให้สร้าง/เดินสถานะให้ถึงก่อน หรือใช้ข้อมูล mock ที่มากับ prototype.
4. เดินทีละ step: ทำ Action (ตาม verb tag) → ตรวจ Expected ด้วยตา → ติ๊ก Result ☐→✔/�’.
5. เคสที่มี **Expected แบบส่วนต่าง** ให้จดค่าตั้งต้นใน step แรก แล้วเทียบ (ระบุไว้ในตารางแล้ว).
6. เคส `(ต้อง simulate)` (TC-17 demoPay, TC-CC-01, TC-ID-01, TC-FU-01 big file) — ถ้า prototype ทำไม่ได้ ให้ mark **blocked** พร้อม evidence.
7. บันทึกผลตาม `Result Report (schema)` ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST) | 22 / 22 |
| Business Rules (BR-01..15) | 15 / 15 |
| Status guards / transitions (§5.2) | 10 / 10 |
| Error codes (§5.6) | 17 / 18 |
| Field validation (§5.4) | 11 / 11 |
| Permission cells (§5.3 สำคัญ) | 7 / 7 |
| Edge cases (§5.5) | 10 / 10 |
| Cross-Module (XT-01..06) | 6 / 6 |
| Scope Lock (LOCK-01..10) | 10 / 10 |

- **FN cross-check: ✅ 22/22**
- **Cross-Module (XT): 6/6**
- **Scope Lock (LOCK): 10/10** (LOCK-02→TC-S03/S01 · LOCK-03→TC-R05 · LOCK-04→TC-09/17 · LOCK-05→TC-11c · LOCK-07→TC-18/X02 · LOCK-08→TC-X03/X06 อื่น ๆ มีเคส verify เฉพาะ)
- **Manifest cross-check (FRD §0.12): ✅ 22/22** — ทุกแถว FN Coverage Manifest มีคู่ใน Ledger + เคส.

### ข้าม (พร้อมเหตุผล)
- **ERR_VALIDATION_FAILED / ERR_NOT_AUTHENTICATED / ERR_NOT_FOUND (401/404 generic):** ข้าม — เป็น auth/infra layer ไม่สังเกตได้บน prototype UI (ทดสอบระดับ API). นับ error catalog 17/18 (BR_* + concurrency/idempotency ครอบหมด; generic auth = API test).
- **หน้าจอ Sales Return จริง (F090):** ข้าม — นอกขอบเขตใบเซ็น (mock [ASSUMED contract]) — ตรวจเฉพาะการผูก SR ที่ฝั่ง CN (TC-R01/R03/X06).
- **หน้า AR / VAT Report / JE จริง (F094/F105/F093):** ข้าม module ปลายทาง — prototype ไม่มีหน้าจริง → ตรวจผลผ่าน ref tab / stat tile ฝั่ง CN (TC-X01/X02/X03).
- **ลดหนี้ไม่อ้างใบ / refund / ยกเลิกหลังอนุมัติ:** นอกขอบเขตใบเซ็น (Exclusions) — ทดสอบว่า **ปิด/ไม่รองรับ** (TC-S03/14a, TC-NEG-03, TC-NEG-05/X05) ไม่ทดสอบให้ทำได้.
- **DEMO artifacts (persona switcher/demoPay/.demo-only):** เป็น harness ทดสอบ — ใช้ตั้ง role/simulate เท่านั้น (prod strip). ไม่มีเคสยืนยัน "ต้องมีบนจอ prod".

---

## Result Report (schema)

```json
{
  "feature_id": "F-ACC-CN",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 88, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent เห็นจริงตอน fail/blocked (ข้อความ error จริง · route ที่ค้าง · ค่าที่แสดงแทน Expected). `note` = หมายเหตุเสริม เช่น `(ต้อง simulate)` ทำไม่ได้บน prototype.
