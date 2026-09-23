# AI Test Cases — ใบลดหนี้ผู้ขาย (Debit Note · F-ACC-DN / F097)

ไฟล์นี้เขียนสำหรับ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype
`F-ACC-DN_debit-note.html` (vanilla JS SPA · hash routing). ทุก action/expected ผูกกับ **ข้อความที่เห็นบนจอ**
(verbatim จาก HTML / 01_UI / microcopy กลาง) + **route จริง**. Expected เช็คได้ด้วยตา. ทุก step มีช่อง Result `☐`.
Trace กลับ FRD Pack (`06_TESTS` AC/§6.9 XT · `05_RULES` BR/EC/error/permission · `01_UI`) + `FUNCTION_CHECKLIST` 24 FN.

> **แหล่ง anchor:** HTML ต้นทาง (verbatim) > 01_UI > microcopy กลาง html-generator-v9. ไม่พบ drift ระหว่าง 01_UI ↔ HTML.
> **DEMO harness:** persona switcher / `demoPay` / `.demo-only` เป็นของทดสอบใน prototype (prod strip) — ใช้เพื่อ setup role และพิสูจน์ S-11 เท่านั้น.
> **DN vs CN (สำคัญ — semantic reversal จาก sibling CN):**
> - **FN-04/FN-20:** เพดานการออก DN = **มูลค่าที่ลดได้ (dnRoom) ไม่หัก paid** → **ใบจ่ายครบยังออก DN ได้** (คืนของหลังจ่าย) · ส่วนเกินคงค้าง = **เครดิตคงเหลือกับผู้ขาย (vendorCredit)** · ใบที่ **ลดเต็มมูลค่าแล้ว (dnRoom=0)** เท่านั้นที่ไม่โผล่.
> - **FN-17:** re-check ตอนอนุมัติขั้นสุดท้าย บล็อกเมื่อมี **ใบลดหนี้อื่น approved เพิ่ม** จน grand > dnRoom — **การจ่ายเงินไม่บล็อก** (ต่างจาก CN).
> - **FN-21:** กลับ **ภาษีซื้อ** (input VAT) ลง ภ.พ.30 ได้เมื่อกรอก **vendorCn** (เลขที่+วันที่ใบลดหนี้จากผู้ขาย) · เดือนภาษี = vendorCnDate (ม.82/10) · ไม่มี → "รอใบลดหนี้ผู้ขาย".

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-ACC-DN (F097) |
| Feature Name | ใบลดหนี้ผู้ขาย — Debit Note (mirror ฝั่งซื้อ ของ Credit Note) |
| FRD Version | 1.0 (2026-09-23) · Variant FULL · HTML-first (หลัง BA FIX-01/02) |
| App entry | เปิด `F-ACC-DN_debit-note.html` · Sidebar (กลุ่ม AP/บัญชี) active = **ใบลดหนี้ผู้ขาย** |
| Routes | `#/list` (P-01) · `#/create` (P-02 wizard 5 ขั้น) · `#/create/dup-<id>` (ทำสำเนา) · `#/edit/<id>` (P-03 draft) · `#/view/<id>` (P-04 view drawer 5 tabs) |
| ที่มา | FRD_Pack (00,01,05,06,07) · BRD_F-ACC-DN.md · HTML `F-ACC-DN_debit-note.html` (source of truth) · FUNCTION_CHECKLIST (24 FN) |
| จำนวนเคส | 102 เคส · 14 group |
| Roles | เจ้าหน้าที่เจ้าหนี้ (officer-ap · Maker) · ผจก.จัดซื้อ (mgr-purchase · ขั้น1) · ผจก.บัญชี (mgr-acc · ขั้น2) · CFO (cfo · ขั้น3) — สลับด้วย persona switcher (DEMO) |
| Negatives | ไม่มี FN-40 เดี่ยว — negatives = tile ปิด (FN-02) · SoD ไม่มีปุ่มอนุมัติ (FN-14) · no hard delete (BR-15) · no refund · no RTV CRUD · ใบ dnRoom=0 ไม่โผล่ |

---

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| G1 · รายการ/ค้นหา/กรอง/สถิติ/CSV + credit card (P-01 · FN-90/20) | 11 | กลาง/สูง |
| G2 · เลือกแหล่งที่มา s1 (FN-01/02/03/04) | 7 | สูง |
| G3 · เหตุผล + ยอดลด s2/s3 (FN-05/06/07/08/09/10) | 17 | สูง |
| G4 · ส่วนลดท้ายบิล s3 (FN-19 · BR-11/12 · LD-05) | 7 | สูง |
| G5 · ส่งอนุมัติ + DOA (FN-11) | 5 | สูง |
| G6 · อนุมัติ/ไม่อนุมัติ/re-check/SoD (FN-12/13/17/14) | 8 | สูง |
| G7 · ยกเลิก/ส่งผู้ขาย/ออกเอกสารแก้ไข (FN-15/16) | 6 | กลาง |
| G8 · เครดิตคงเหลือกับผู้ขาย + ภาษีซื้อกลับ (FN-20/21) | 5 | สูง |
| G9 · View tabs: ref/history/pdf (FN-18/91/92) | 5 | กลาง |
| G10 · Status guards + Negatives | 10 | สูง |
| G11 · Permission matrix (SoD) | 7 | สูง |
| G12 · Cross-module (XT-01..07) | 7 | สูง |
| G13 · Scope Lock verify (LOCK) | 3 | กลาง |
| G14 · Edge cases (EC) | 4 | กลาง/ต่ำ |

---

## Coverage Ledger

### FN (FUNCTION_CHECKLIST 24/24)
| FN | S / BR | cases |
|---|---|---|
| FN-01 เลือกใบตั้งหนี้คงค้าง + เห็นสุทธิ/จ่ายแล้ว/ลดแล้ว/คงค้าง | S-01 · BR-01 | TC-S01, TC-S02, TC-01 |
| FN-02 tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ | S-12 · BR-16 · OQ-DN-01 | TC-S03, TC-14a |
| FN-03 เลือกใบ→ดึงผู้ขาย/เลขใบกำกับเดิม/บรรทัด | S-01 | TC-S02, TC-01 |
| FN-04 ใบ dnRoom=0 ไม่โผล่ · **ใบจ่ายครบยังออกได้** | S-13 · BR-13 · FIX-01 | TC-S04, TC-13c, TC-20a |
| FN-05 RTV → เลือกใบคืนสินค้า · จำนวนจาก RTV | S-01 · BR-06 | TC-R01, TC-R02, TC-R03, TC-01, TC-X06 |
| FN-06 OVERPRICE ราคาลด ≤ ราคาเดิม | S-02 · BR-04 | TC-06, TC-06b |
| FN-07 SHORT ลดเฉพาะบรรทัด · ลบ/readd | S-03 · BR-03 | TC-07, TC-07b |
| FN-08 ลดหลายรอบ meta ถูกต้อง | S-04 · BR-03/10 | TC-08 |
| FN-09 ยอด/จำนวนเกิน → บล็อก+บอกยอด | S-05 · BR-02 | TC-09, TC-09b, TC-09c |
| FN-10 คำอธิบาย ≥10 | BR-05 | TC-10 |
| FN-11 ส่งอนุมัติ: สายตามมูลค่า + เลือกครบ | S-06 · BR-07 | TC-11a, TC-11b, TC-11c, TC-11d, TC-11e |
| FN-12 อนุมัติครบสาย → เลข DN | S-06 · BR-08 | TC-12, TC-12b |
| FN-13 ไม่อนุมัติ + เหตุผล → ร่าง + รอบก่อน | S-07 | TC-13, TC-13b |
| FN-14 ผู้ส่งไม่เห็นปุ่มอนุมัติ (SoD) | S-08 · BR-07 | TC-14b, TC-P05 |
| FN-15 ยกเลิก draft/pending + เหตุผล → คืน held | S-09 | TC-15, TC-15b |
| FN-16 ส่งผู้ขาย → "ส่งผู้ขายแล้ว" · resend | S-10 | TC-16, TC-16b |
| FN-17 dnRoom ลดระหว่างรอ (ใบอื่น approved) → อนุมัติไม่ได้ | S-11 · BR-02/13 · FIX-01 | TC-17, TC-17b |
| FN-18 ref tab คงค้างก่อน/หลัง + ภาษีซื้อ + JE + split | S-14 · BR-09 | TC-18, TC-18b |
| FN-19 ส่วนลดท้ายบิล ฿/% · ≥0 ≤dnRoom · ลด input VAT | S-05/S-14 · BR-11/12 | TC-19a..TC-19g |
| FN-20 เครดิตคงเหลือกับผู้ขาย (dnSplit · card+modal) | S-13/S-14 · BR-13 | TC-20a, TC-20b, TC-X07 |
| FN-21 ภาษีซื้อกลับตาม vendorCn (รอเอกสาร/เดือนภาษี) | S-14 · BR-14 · FIX-02 | TC-21a, TC-21b, TC-21c, TC-X02 |
| FN-90 ค้นหา/กรอง/สถิติ/CSV + empty | กติกากลาง | TC-L01..TC-L10 |
| FN-91 ประวัติ append-only | GR-4 · BR-15 | TC-91, TC-91b |
| FN-92 PDF ม.86/10 (เลข/วันที่ใบกำกับเดิม·เดิม/ถูกต้อง/ผลต่าง·เหตุผล·ค.ศ.) | OB-6 | TC-92 |

**FN cross-check: ✅ 24/24** (ทุก FN มี ≥1 เคส)

### Business Rules (05_RULES §5.1 · BR-01..17)
| BR | cases |
|---|---|
| BR-01 picker เฉพาะ approved/posted · dnRoom>0 | TC-S01, TC-S04, TC-13c |
| BR-02 grand ≤ dnRoom (ส่ง + อนุมัติขั้นสุดท้าย) | TC-09, TC-09b, TC-17, TC-X01 |
| BR-03 qty/net ≤ ที่ลดได้ (ข้ามทุกใบ) | TC-07, TC-08, TC-09c |
| BR-04 price ≤ ราคาเดิม (mode price) | TC-06, TC-06b |
| BR-05 reason ∈ master · text ≥10 | TC-10, TC-R04 |
| BR-06 RTV ต้องอ้างใบคืนสินค้า · qty ≤ RTV | TC-R01, TC-R02, TC-R03 |
| BR-07 DOA resolve ตาม grand · SoD | TC-11c, TC-14b, TC-19c, TC-P05 |
| BR-08 เลข DN no-gap ตอน final approve | TC-12, TC-12b |
| BR-09 approved → dn_applied + JE + ลดภาษีซื้อ | TC-18, TC-X01, TC-X03 |
| BR-10 held ชั่วคราว · ยกเลิกคืน held | TC-08, TC-15, TC-X04 |
| BR-11 end-bill cap · net ≥0 ≤dnRoom | TC-19b, TC-19e |
| BR-12 end-bill ลดฐานภาษี · input VAT ม.86/10 | TC-19a, TC-19d, TC-18b, TC-X02 |
| BR-13 dnRoom ไม่หัก paid · vendorCredit split | TC-20a, TC-20b, TC-S04, TC-X07 |
| BR-14 input VAT gated by vendorCn (ม.82/10) | TC-21a, TC-21b, TC-21c, TC-X02 |
| BR-15 append-only · no hard delete · ค.ศ. | TC-91, TC-91b, TC-NEG-04 |
| BR-16 tile ลดลอย ปิดไว้ | TC-S03, TC-14a |
| BR-17 legal_basis ต่อ reason (PDF) | TC-R05, TC-92 |

### State Machine / Status Guards (05_RULES §5.2)
| transition/guard | cases |
|---|---|
| draft→pending (submit) | TC-11a |
| pending→approved (approve ครบสาย) | TC-12 |
| pending→draft (reject) | TC-13 |
| draft/pending→cancelled (cancel) | TC-15, TC-15b |
| approved→sent (send) · sent→resend | TC-16, TC-16b |
| approved/sent → บันทึก vendorCn (ไม่เปลี่ยน state) | TC-21b, TC-21c |
| approved/sent → ออกเอกสารแก้ไข (display-only) | TC-NEG-05 |
| submit เฉพาะ draft (guard) | TC-GRD-01 |
| edit เฉพาะ draft (guard) | TC-GRD-02 |
| cancel เฉพาะ draft/pending (guard) | TC-GRD-03 |
| send เฉพาะ approved (guard) | TC-GRD-04 |
| vendorCn เฉพาะ approved/sent (guard) | TC-GRD-05 |

### Field Validation / Error Catalog (05_RULES §5.4/§5.6)
| error code | cases |
|---|---|
| BR_DN_DATE_BEFORE_INVOICE ("ต้องไม่ก่อนวันที่ใบกำกับเดิม") | TC-R06 |
| BR_REASON_REQUIRED ("เลือกเหตุผล") | TC-R04 |
| BR_RTV_NEEDS_RTV ("เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า") | TC-R02 |
| BR_REASON_TEXT_TOO_SHORT ("ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร") | TC-10 |
| BR_LINE_QTY_EXCEEDED | TC-09c, TC-R03 |
| BR_PRICE_EXCEEDS_ORIG | TC-06 |
| BR_LINE_NET_EXCEEDED | TC-09c |
| BR_ENDBILL_EXCEEDS_CAP | TC-19b |
| BR_DN_EXCEEDS_ROOM | TC-09, TC-09b |
| BR_APPROVE_EXCEEDS_ROOM | TC-17 |
| BR_SUBMIT_DRAFT_ONLY | TC-GRD-01 |
| BR_EDIT_DRAFT_ONLY | TC-GRD-02 |
| BR_CANCEL_STATE_INVALID | TC-GRD-03 |
| BR_SEND_STATE_INVALID | TC-GRD-04 |
| BR_VENDORCN_STATE_INVALID | TC-GRD-05 |
| BR_SLOT_INCOMPLETE ("เลือกผู้อนุมัติให้ครบทุกขั้น") | TC-11b |
| ERR_NOT_CURRENT_APPROVER ("ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน") | TC-P07 |
| ERR_STALE_DATA (409 concurrent) | TC-CC-01 |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / double-submit | TC-ID-01 |

### Permission Matrix (05_RULES §5.3 · role × action)
| cell | cases |
|---|---|
| officer-ap create/edit/submit/cancel/send/vendorCn = allow | TC-P01 |
| mgr-purchase create = deny (ไม่มีปุ่มสร้าง) | TC-P02 |
| mgr-purchase approve ขั้น1 = allow | TC-P03 |
| mgr-acc approve ขั้น2 (tier2+) + vendorCn = allow | TC-P04 |
| cfo approve ขั้น3 (tier3) = allow | TC-P06 |
| ผู้ส่ง (owner) approve ใบตัวเอง = deny (SoD) | TC-P05, TC-14b |
| ไม่ใช่ผู้มีสิทธิ์ขั้นปัจจุบัน = deny | TC-P07 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 dnRoom ลดระหว่างรอ (ใบอื่น approved · S-11) | TC-17 |
| EC-02 ลดหลายรอบ (S-04) | TC-08 |
| EC-03 ใบจ่ายครบยังออก DN ได้ (S-13) | TC-20a, TC-S04 |
| EC-04 ใบ dnRoom=0 ไม่โผล่ | TC-13c |
| EC-05 ยกเลิก draft/pending คืน held (S-09) | TC-15, TC-X04 |
| EC-06 reject → history + badge (S-07) | TC-13, TC-13b |
| EC-07 ยังไม่ได้ใบลดหนี้ผู้ขาย → "รอเอกสาร" (FN-21) | TC-21a |
| EC-CC-01 concurrent approval → 409 `[AI-DEFAULT]` | TC-CC-01 (ต้อง simulate) |
| EC-ID-01 double-submit idempotency | TC-ID-01 (ต้อง simulate) |
| EC-CALC-01 ปัดเศษ ebVat 2 ตำแหน่ง `[AI-DEFAULT]` | TC-CALC-01 |
| EC-FU-01 ชนิด/ขนาดไฟล์แนบ `[AI-DEFAULT]` | TC-FU-01 |
| EC-CA-01 vendorCn ซ้ำ/เดือนปิดงวด → OQ | TC-CA-01 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 approve → ap_open_item dn_applied↑ | AP F-ACC-APINV | TC-X01 |
| XT-02 บันทึก vendorCn → ภ.พ.30 input VAT เดือน vendorCnDate | VAT F105 | TC-X02 |
| XT-03 approve → JE (Dr 2110 · Cr 5xxx · Cr 1150) | JE F093 mock | TC-X03 |
| XT-04 ยกเลิก (draft/pending) → held คืน | AP F-ACC-APINV | TC-X04 |
| XT-05 ยกเลิกหลังอนุมัติ (ไม่รองรับ) → "ออกเอกสารแก้ไข" | — | TC-X05 (= TC-NEG-05) |
| XT-06 RTV → ใบเดียวกัน · qty ≤ คืน | RTV W3-LITE mock | TC-X06 (= TC-R01/R03) |
| XT-07 ใบจ่ายครบ → vendorCredit | Vendor Credit Ledger F097 | TC-X07 (= TC-20a/20b) |

### Scope Lock (07_LOCKED §7.0)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 Pattern Q + B2 v2 | TC-LK-01, TC-07 |
| LOCK-02 อ้าง AP Invoice เสมอ | TC-S03, TC-S01 |
| LOCK-03 เหตุผล master (RTV/OVERPRICE/SHORT) | TC-R05 |
| LOCK-04 ลดไม่เกิน dnRoom (ปรับความหมาย FIX-01) | TC-09, TC-17, TC-20a |
| LOCK-05 DOA slot picker ตามมูลค่า | TC-11c |
| LOCK-06 doccfg DN-YYYY-NNNN + PDF อ้างเลขเดิม | TC-12, TC-92 |
| LOCK-07 ระบุผลกระทบ VAT ซื้อ (gated vendorCn) | TC-18, TC-21a, TC-X02 |
| LOCK-08 dep ข้ามเลน = mock | TC-X03, TC-X06 |
| LOCK-09 UI #67.1 (เฉพาะ hard-warn/field-error/danger/note.warn) | TC-LK-09 |
| LOCK-10 ค.ศ. · append-only | TC-91, TC-92, TC-LK-10 |

### Out of Scope (Exclusions — ห้ามสร้างเคสทดสอบ "ให้ทำได้")
- ลดหนี้ไม่อ้างใบ (ลดลอย) → ตรวจ **ต้องปิด** ที่ TC-S03/TC-14a (นอกขอบเขต = ทดสอบว่าปิด ไม่ใช่ทำได้)
- เรียกเงินคืนเมื่อจ่ายครบ (refund) → นอกขอบเขต (OQ-DN-03) → TC-NEG-03 (ตรวจว่าไม่มี refund · ใบจ่ายครบใช้ vendorCredit แทน)
- ยกเลิก DN หลังอนุมัติ → นอกขอบเขต (OQ-DN-04) → TC-NEG-05 (ตรวจว่าใช้ revise-doc display-only)
- หน้าจอคืนสินค้า (RTV) จริง → นอกขอบเขต (W3-LITE mock) → seed อย่างเดียว ไม่ทดสอบหน้าจอ RTV
- flow ใช้/ตัดยอดเครดิตคงเหลือกับผู้ขาย → OQ-DN-06 (display-only รอบนี้) → TC-20b ตรวจว่า **display-only**

---

## Data Sets

> ค่าจาก 06_TESTS §6.3 (mock ใน HTML — พิสูจน์ scenario) + master. ปุ่ม "จำลอง" ใน prototype ใช้ seed ได้ทันที.

### ชุดใบตั้งหนี้ซื้อ (ref AP invoice)
| ชุด | ใบตั้งหนี้ | ลักษณะ | ใช้กับ scenario |
|---|---|---|---|
| API-A | API-2026-0041 | จ่ายบางส่วน · DN-0011 คืน 1 เครื่อง (ลดแล้ว) · ร่างคืน 2 กล่อง · มี RTV-2026-0007/0010 | S-01/S-04 (RTV, ลดหลายรอบ) |
| API-B | API-2026-0043 | ราคา 4,100 (mode price) | S-02/S-07 (OVERPRICE, ตีกลับ) |
| API-C | API-2026-0046 | 60 ใบ · 526,440 · มี RTV-2026-0009 · DN รอ ขั้น1(tier2)+ขั้น2(tier3) | S-03/S-06/S-11 (SHORT, tier, re-check) |
| API-PAID | API-2026-0038 | **จ่ายครบ (outstanding=0)** · dnRoom>0 | S-13 (ยังออก DN ได้ → vendorCredit) |
| API-FULL | (ใบที่ลดเต็มมูลค่าแล้ว · dnRoom=0) | ลด DN จนเต็ม invGrand | ต้องไม่โผล่ใน picker (seed หรือเดินสถานะให้ถึง) |

### ชุดเหตุผล (DN_REASONS master · verbatim จาก HTML)
| ชุด | เหตุผลบนจอ | mode | needRTV | legal_basis [ASSUMED · OQ-DN-05] |
|---|---|---|---|---|
| RS-RTV | คืนสินค้า (อ้างใบคืนสินค้า RTV) | qty | ✅ | รับคืนสินค้า/คืนของให้ผู้ขาย |
| RS-OVERPRICE | ผู้ขายคิดราคาเกิน | price | — | ผู้ขายคำนวณราคาสูงกว่าที่ตกลง/ผิดราคา |
| RS-SHORT | ของขาด/ไม่ครบตามใบกำกับ | qty | — | จัดส่งสินค้าขาดจำนวน/ไม่ครบตามใบกำกับ |

### ชุดคำอธิบายเหตุผล (reason_text)
| ชุด | ค่า | ผล |
|---|---|---|
| RT-OK | "คืนสินค้าให้ผู้ขาย 2 กล่องเนื่องจากชำรุด" (>10 ตัว) | ผ่าน |
| RT-SHORT | "ชำรุด" (<10 ตัว) | field-error |

### ชุดส่วนลดท้ายบิล (end-bill)
| ชุด | mode | value | คาดผล |
|---|---|---|---|
| EB-OK-AMT | ฿ (amount) | ค่าที่ ≤ ebCap | ลดฐานภาษี + input VAT คิดใหม่ · grand ลดลง |
| EB-OK-PCT | % (percent) | 5% | ebBase/netVat คำนวณตามสัดส่วน |
| EB-OVER | ฿ (amount) | ค่าที่ > ebCap | hard-warn + block submit |

### ชุด DOA tier (ยอดสุทธิ grand · หลัง end-bill · [ASSUMED cut · OQ-AP-06])
| ชุด | grand | tier | สายอนุมัติ |
|---|---|---|---|
| DOA-T1 | ≤ 50,000 | 1 | ผจก.จัดซื้อ |
| DOA-T2 | 50,000.01–300,000 | 2 | ผจก.จัดซื้อ → ผจก.บัญชี |
| DOA-T3 | > 300,000 | 3 | ผจก.จัดซื้อ → ผจก.บัญชี → CFO |

### ชุด vendorCn (ใบลดหนี้จากผู้ขาย)
| ชุด | เลขที่ | วันที่ได้รับ | ผล |
|---|---|---|---|
| VCN-OK | เช่น TFS-6650 | เดือนปัจจุบัน | input VAT ลง ภ.พ.30 เดือน = วันที่ได้รับ (ม.82/10) |
| VCN-NONE | (เว้นว่าง) | — | note.warn "รอใบลดหนี้ผู้ขาย" · ยังไม่ลง ภ.พ.30 |

### Personas (DEMO switcher)
| ชุด | ชื่อบนจอ | role | ใช้ |
|---|---|---|---|
| U-AP | สุภาพร เจ้าหนี้ดี | เจ้าหน้าที่เจ้าหนี้ (officer-ap) | Maker |
| U-PUR | สมศักดิ์ จัดซื้อ | ผจก.จัดซื้อ (mgr-purchase) | อนุมัติขั้น 1 |
| U-ACC | ประเสริฐ | ผจก.บัญชี (mgr-acc) | อนุมัติขั้น 2 · vendorCn |
| U-CFO | อรุณี | CFO (cfo) | อนุมัติขั้น 3 |

### ไฟล์ทดสอบ (Files)
| ชื่อไฟล์ | ใช้กับ | หมายเหตุ |
|---|---|---|
| `dn-attach-ok.pdf` | TC-FU-01 (แนบ s4) | jpg/png/pdf ≤10MB → ผ่าน (`[AI-DEFAULT]`) |
| `dn-attach-big.pdf` | TC-FU-01 (>10MB) | เกินขนาด → ปฏิเสธ (ต้อง simulate ถ้า UI ไม่บังคับ) |

---

## Test Cases

## G1 · รายการ / ค้นหา / กรอง / สถิติ / CSV + credit card (P-01 · FN-90 · FN-20 · AC-90)

### TC-L01 — เปิดหน้ารายการ เห็นตาราง + stat 4 tile + credit card (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / AC-90 / 01_UI P-01
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=officer-ap (U-AP) · seed=มีใบลดหนี้หลายสถานะ (DN 8 ใบ) · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: เห็นตาราง 10 คอลัมน์ + stat 4 tile ครบ + KPI card เครดิตคงเหลือกับผู้ขาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | Breadcrumb Accounting > AP > ใบลดหนี้ผู้ขาย · Sidebar active = **ใบลดหนี้ผู้ขาย** | ☐ |
| 2 | VERIFY แถบ stat ด้านบน | — | 4 tile: **รออนุมัติ** · **ลดหนี้เดือนนี้** · **ฉบับร่าง** · **ภาษีซื้อที่ลดเดือนนี้** (sub "ภ.พ.30 เดือน MM/YYYY") | ☐ |
| 3 | VERIFY KPI card เพิ่มเติม | — | เห็นการ์ด **เครดิตคงเหลือกับผู้ขาย** (รวม vendorCredit ของ approved/sent) | ☐ |
| 4 | VERIFY หัวตาราง | — | คอลัมน์: เลขที่ · วันที่ · ผู้ขาย · ใบตั้งหนี้อ้างอิง · เหตุผล · สถานะเอกสาร · ลายเซ็น · ยอดลดหนี้ · ภาษีซื้อที่ลด · ⋮ | ☐ |
| 5 | VERIFY ปุ่มมุมขวาบน | — | เห็นปุ่ม **ส่งออก CSV** + **สร้างใบลดหนี้ผู้ขาย** | ☐ |

### TC-L02 — ค้นหาเจอ (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / onSearchInput
- Setup: role=officer-ap · seed=มีใบของผู้ขายที่ค้นได้ · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | เลข DN หรือชื่อผู้ขายที่มีจริง | ตารางเหลือเฉพาะแถวที่ตรง | ☐ |
| 2 | VERIFY จำนวนแถว | — | ทุกแถวที่เหลือมีคำค้นในคอลัมน์ เลขที่/ผู้ขาย/ใบอ้างอิง (code/ผู้ขาย/inv/rtv/vendorCn/vinv) | ☐ |

### TC-L03 — ค้นหาไม่เจอ → empty (edge)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / states
- Setup: role=officer-ap · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | "zzzzzz" | ตารางว่าง · แสดง **ไม่พบรายการ** (ไม่มีแถว) | ☐ |
| 2 | CLICK ล้างคำค้น | — | ตารางกลับมามีข้อมูลเดิม | ☐ |

### TC-L04 — กรองสถานะเอกสาร ครบทุกค่า (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / filterSelects
- Setup: role=officer-ap · seed=มีใบ draft/pending/approved/sent/cancelled อย่างละ ≥1 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → ตัวกรอง **สถานะเอกสาร** | "ฉบับร่าง" | เหลือเฉพาะแถว pill = ฉบับร่าง | ☐ |
| 2 | SELECT → **สถานะเอกสาร** | "รออนุมัติ" | เหลือเฉพาะ pill รออนุมัติ | ☐ |
| 3 | SELECT → **สถานะเอกสาร** | "อนุมัติแล้ว · รอส่ง" | เหลือเฉพาะ pill อนุมัติแล้ว · รอส่ง | ☐ |
| 4 | SELECT → **สถานะเอกสาร** | "ส่งผู้ขายแล้ว" | เหลือเฉพาะ pill ส่งผู้ขายแล้ว | ☐ |
| 5 | SELECT → **สถานะเอกสาร** | "ยกเลิก" | เหลือเฉพาะ pill ยกเลิก | ☐ |
| 6 | SELECT → **สถานะเอกสาร** | "ทั้งหมด" | กลับมาเห็นทุกแถว | ☐ |

### TC-L05 — กรองเหตุผล (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90
- Setup: role=officer-ap · seed=มีใบหลายเหตุผล · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → ตัวกรอง **เหตุผล** | "คืนสินค้า (อ้างใบคืนสินค้า RTV)" | เหลือเฉพาะแถวเหตุผลคืนสินค้า | ☐ |
| 2 | SELECT → **เหตุผล** | "ทั้งหมด" | กลับมาเห็นทุกแถว | ☐ |

### TC-L06 — กรองผู้ขาย (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90
- Setup: role=officer-ap · seed=มีใบ ≥2 ผู้ขาย · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → ตัวกรอง **ผู้ขาย** | ผู้ขายรายหนึ่ง | เหลือเฉพาะแถวของผู้ขายนั้น | ☐ |

### TC-L07 — sort คอลัมน์ (happy)
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-90 / sortBy (code/date/total)
- Setup: role=officer-ap · seed=≥3 แถว · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **เลขที่** | — | ลำดับแถวเปลี่ยน (เรียงตามเลขที่) | ☐ |
| 2 | CLICK หัวคอลัมน์ **วันที่** | — | เรียงตามวันที่ | ☐ |
| 3 | CLICK หัวคอลัมน์ **ยอดลดหนี้** | — | เรียงตามยอด grand | ☐ |

### TC-L08 — คลิก stat tile = filter (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-90 / f.stat
- Setup: role=officer-ap · seed=มี pending + draft + approved เดือนนี้ · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tile **รออนุมัติ** | — | ตารางกรองเหลือเฉพาะ pending | ☐ |
| 2 | CLICK tile **ฉบับร่าง** | — | ตารางเหลือเฉพาะ draft | ☐ |
| 3 | CLICK tile **ลดหนี้เดือนนี้** | — | ตารางเหลือเฉพาะ approved/sent เดือนปัจจุบัน | ☐ |
| 4 | CLICK tile **ภาษีซื้อที่ลดเดือนนี้** | — | ตารางกรองตาม vat เดือนนี้ | ☐ |

### TC-L09 — ส่งออก CSV (happy)
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-90 / API-10 / csvHead
- Setup: role=officer-ap · seed=≥1 แถว · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | ไฟล์ CSV ถูกดาวน์โหลด · toast **ส่งออก CSV {n} รายการ** | ☐ |

### TC-L10 — empty state ไม่มีข้อมูลเลย (edge)
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-90 / states / 01_UI §1.6
- Setup: role=officer-ap · seed=ไม่มีใบลดหนี้เลย · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY กลางตาราง | — | ข้อความ **ยังไม่มีใบลดหนี้ผู้ขาย** + ปุ่ม CTA สร้าง | ☐ |

### TC-20b — เครดิตคงเหลือกับผู้ขาย: card เปิด modal รายผู้ขาย (display-only) (UI · FN-20)
- group: รายการ · ความสำคัญ: สูง · trace: FN-20 / AC-20(4) / BR-13 / API-17 / OQ-DN-06 / XT-07
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=officer-ap (U-AP) · seed=มี DN approved/sent ที่ vendorCredit>0 (จาก API-PAID) · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: card แสดงยอดรวม · คลิกเปิด modal รายผู้ขาย · เป็น display-only (ปิดได้อย่างเดียว)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY KPI card **เครดิตคงเหลือกับผู้ขาย** | — | แสดงยอด ฿รวม vendorCredit ของ DN approved/sent | ☐ |
| 2 | CLICK card **เครดิตคงเหลือกับผู้ขาย** | — | เปิด modal รายผู้ขาย (vendorCreditLedger) · แต่ละแถว = ผู้ขาย + ฿เครดิตคงเหลือ | ☐ |
| 3 | VERIFY modal เป็น display-only | — | **ไม่มีปุ่มใช้/ตัดยอด/refund** — มีแค่ปุ่มปิด (flow ใช้ยอด = OQ-DN-06) | ☐ |
| 4 | CLICK ปุ่ม **ปิด** | — | modal ปิด กลับหน้ารายการ | ☐ |

---

## G2 · เลือกแหล่งที่มา s1 (FN-01/02/03/04)

### TC-S01 — s1 เห็นตารางใบตั้งหนี้คงค้าง (สุทธิ/จ่ายแล้ว/ลดแล้ว/คงค้าง) (happy)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-01 / AC-01 / BR-01 / LOCK-02
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=officer-ap (U-AP) · seed=API-A มี dnRoom>0 · files=—
- Start: OPEN `#/list` → CLICK ปุ่ม **สร้างใบลดหนี้ผู้ขาย**
- ชุดข้อมูล: API-A
- ผ่านเมื่อ: s1 แสดงตารางใบที่มี dnRoom>0 พร้อมคอลัมน์ ยอดสุทธิ/จ่ายแล้ว/ลดหนี้แล้ว/คงค้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบลดหนี้ผู้ขาย** | — | drawer สร้างเปิด · route=`#/create` · Stepper ขั้น 1 = **เลือกแหล่งที่มาของใบลดหนี้** | ☐ |
| 2 | VERIFY 2 tile บนสุด | — | tile **จากใบตั้งหนี้** (active) · tile **ลดหนี้ไม่อ้างใบ** (มี pill "ปิดไว้") | ☐ |
| 3 | VERIFY ตารางใบตั้งหนี้ (srcPickerCard) | — | คอลัมน์ ใบตั้งหนี้ · ผู้ขาย · วันที่ · ยอดสุทธิ · **จ่ายแล้ว** · **ลดหนี้แล้ว** · **คงค้าง** | ☐ |
| 4 | VERIFY แถว API-A | API-A | คอลัมน์ ลดหนี้แล้ว > 0 (DN-0011) · คงค้าง = สุทธิ − จ่าย − ลดแล้ว | ☐ |

### TC-S02 — เลือกใบ → ดึงผู้ขาย/เลขใบกำกับเดิม/บรรทัด (happy)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-03 / AC-01 / pickInv
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create`
- ชุดข้อมูล: API-A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **API-A** ในตารางใบตั้งหนี้ | API-A | แถวถูกเลือก (highlight) | ☐ |
| 2 | CLICK **ถัดไป** | — | ไปขั้น 2 = **ข้อมูลหลักใบลดหนี้** | ☐ |
| 3 | VERIFY ช่องใบอ้างอิง + ผู้ขาย | — | ใบอ้างอิง = "no · ใบกำกับ vinv ลงวันที่..." (disabled) · ผู้ขาย disabled แสดงชื่อ · เห็นเลขภาษี/ที่อยู่ | ☐ |
| 4 | VERIFY ช่องเลขที่ DN | — | readonly = **(ออกเลขเมื่ออนุมัติครบ)** | ☐ |
| 5 | CLICK **ถัดไป** ผ่าน s2 (กรอกครบ) แล้วดู s3 | — | ขั้น 3 มีบรรทัดสินค้าจากใบเดิม (สินค้าถูกล็อก readonly) | ☐ |

### TC-S03 — tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ (negative · FN-02)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-02 / AC-14 / BR-16 / LOCK-02 / OQ-DN-01
- Setup: role=officer-ap · seed=— · files=—
- Start: OPEN `#/create`
- ผ่านเมื่อ: tile disabled + คลิกแล้ว toast ปิดไว้ · ไม่มีทางเข้าสร้างแบบไม่อ้างใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tile **ลดหนี้ไม่อ้างใบ** | — | มี pill **ปิดไว้** · เคอร์เซอร์ not-allowed (ดูจาง/ปิด) | ☐ |
| 2 | CLICK tile **ลดหนี้ไม่อ้างใบ** | — | toast **ลดหนี้ไม่อ้างใบตั้งหนี้ถูกปิดไว้ (OQ-DN-01)** · ไม่เปลี่ยน tile · ไม่มีฟอร์มสร้างแบบลอย (ไม่ผูก setSource) | ☐ |
| 3 | VERIFY ไม่มีทางไปต่อโดยไม่เลือกใบ | — | tile "จากใบตั้งหนี้" คงเป็นทางเดียว | ☐ |

### TC-S04 — ใบ dnRoom=0 ไม่โผล่ · ใบจ่ายครบยังโผล่ (negative+positive · FN-04 · FIX-01)
- group: สร้าง-s1 · ความสำคัญ: สูง · trace: FN-04 / AC-13/AC-20 / BR-01/BR-13 / EC-03/04
- Setup: role=officer-ap · seed=API-FULL (dnRoom=0) + API-PAID (จ่ายครบ · dnRoom>0) มีอยู่ในระบบ · files=—
- Start: OPEN `#/create`
- ชุดข้อมูล: API-FULL, API-PAID
- ผ่านเมื่อ: ใบลดเต็มไม่โผล่ · **ใบจ่ายครบยังโผล่** (ต่างจาก CN)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตารางใบตั้งหนี้ | — | **ไม่มี** แถว API-FULL (ลดเต็มมูลค่าแล้ว dnRoom=0) | ☐ |
| 2 | VERIFY ตารางใบตั้งหนี้ | — | **ยังมี** แถว **API-2026-0038 (จ่ายครบ)** เพราะ dnRoom ไม่หัก paid — คอลัมน์ คงค้าง=0 แต่ยังเลือกได้ | ☐ |
| 3 | TYPE ค้นหาในตาราง | "0038" | พบแถว API-PAID (ยืนยันไม่ถูกกรองออกเพราะจ่ายครบ) | ☐ |

### TC-S05 — s1 ไม่เลือกใบ → บล็อกไปต่อ (negative)
- group: สร้าง-s1 · ความสำคัญ: กลาง · trace: FN-01 / step1Validate
- Setup: role=officer-ap · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** โดยยังไม่เลือกใบ | — | บล็อก · ข้อความให้เลือกใบตั้งหนี้ก่อน · ยังอยู่ขั้น 1 | ☐ |

### TC-S06 — ทำสำเนา (dup) จาก row menu (happy)
- group: สร้าง-s1 · ความสำคัญ: ต่ำ · trace: FN-90 / prefillDup
- Setup: role=officer-ap · seed=มีใบ ≥1 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน ⋮ ท้ายแถวหนึ่ง | — | เมนูเปิด: ดูรายละเอียด · (แก้ไข ถ้า draft) · **ทำสำเนา** · (ยกเลิก ถ้า draft/pending) | ☐ |
| 2 | CLICK **ทำสำเนา** | — | route=`#/create/dup-<id>` · wizard เปิดพร้อมค่าจากใบต้นทาง | ☐ |

### TC-S07 — เข้าสร้างจากปุ่มหลัก (happy)
- group: สร้าง-s1 · ความสำคัญ: ต่ำ · trace: FN-90 / navigate('create')
- Setup: role=officer-ap · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบลดหนี้ผู้ขาย** | — | route=`#/create` · Stepper ขั้น 1 | ☐ |

---

## G3 · เหตุผล + ยอดลด s2/s3 (FN-05/06/07/08/09/10)

### TC-01 — สร้าง DN RTV ครบ flow ถึงส่งอนุมัติ (happy · E2E)
- group: เหตุผล-RTV · ความสำคัญ: สูง · trace: FN-01/03/05/11/12 / AC-01,02,11,12 / LOCK-01
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=officer-ap (U-AP) · seed=API-A + RTV-2026-0007 (2 กล่อง) · files=—
- Start: OPEN `#/create`
- ชุดข้อมูล: API-A · RS-RTV · RT-OK
- ผ่านเมื่อ: บันทึกร่าง + เปิด submit modal ได้ (สายอนุมัติ resolve)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **API-A** → **ถัดไป** | API-A | ไปขั้น 2 · ใบอ้างอิง=API-A | ☐ |
| 2 | SELECT → ช่อง **เหตุผล** | RS-RTV (คืนสินค้า (อ้างใบคืนสินค้า RTV)) | แสดง legal_basis hint + ช่อง **ใบคืนสินค้า** โผล่ | ☐ |
| 3 | SELECT → ช่อง **ใบคืนสินค้า** | RTV-2026-0007 | จำนวนบรรทัดถูกจำกัดตามใบคืนสินค้า (line.max = RTV qty = 2) | ☐ |
| 4 | SELECT → ช่อง **พนักงาน/ผู้จัดทำ** | ผู้จัดทำที่มี | ช่องแสดงชื่อที่เลือก | ☐ |
| 5 | TYPE → ช่อง **คำอธิบายเหตุผล** | RT-OK | ผ่าน (>10 ตัว) | ☐ |
| 6 | CLICK **ถัดไป** → s3 | — | เห็นบรรทัดสินค้า mode qty · จำนวนสูงสุด = 2 | ☐ |
| 7 | CLICK **ถัดไป** ผ่าน s4 → s5 | — | ขั้น 5 = **ตรวจสอบและยืนยัน** · เห็น DOA preview (tier + สายอนุมัติ) | ☐ |
| 8 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกแบบร่างใบลดหนี้ผู้ขายเรียบร้อย** · route=`#/view/<id>` · pill=ฉบับร่าง | ☐ |

### TC-R01 — RTV เลือกใบคืนสินค้า → จำนวนจากใบคืนสินค้า (happy · FN-05)
- group: เหตุผล-RTV · ความสำคัญ: สูง · trace: FN-05 / AC-02 / BR-06 / XT-06
- Setup: role=officer-ap · seed=API-A + RTV-2026-0007 (2 กล่อง) · files=—
- Start: OPEN `#/create` → เลือก API-A → ถัดไป (s2)
- ชุดข้อมูล: API-A · RS-RTV

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → **เหตุผล** | RS-RTV | ช่อง **ใบคืนสินค้า** ปรากฏ (required) | ☐ |
| 2 | SELECT → **ใบคืนสินค้า** | RTV-2026-0007 | จำนวนบรรทัดในใบ = จำนวนจาก RTV (2 กล่อง) | ☐ |
| 3 | OPEN s3 → VERIFY จำนวนสูงสุดต่อบรรทัด | — | max = min(qtyLeft, RTV.qty) | ☐ |

### TC-R02 — RTV ไม่เลือกใบคืนสินค้า → บล็อก (negative · FN-05)
- group: เหตุผล-RTV · ความสำคัญ: สูง · trace: FN-05 / AC-02 / BR-06 / BR_RTV_NEEDS_RTV
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → เลือก API-A → ถัดไป (s2)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → **เหตุผล** | RS-RTV | ช่องใบคืนสินค้าปรากฏ (ยังว่าง) | ☐ |
| 2 | CLICK **ถัดไป** โดยไม่เลือก RTV | — | บล็อก · field-error **เลือกใบคืนสินค้าของใบตั้งหนี้นี้** / block **เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า** · ยังอยู่ s2 | ☐ |

### TC-R03 — RTV จำนวนเกินที่คืน → บล็อก (negative · boundary · BR-06)
- group: เหตุผล-RTV · ความสำคัญ: สูง · trace: FN-05 / BR-06 / BR_LINE_QTY_EXCEEDED / XT-06
- Setup: role=officer-ap · seed=API-A + RTV-2026-0007 (2 กล่อง) · files=—
- Start: OPEN `#/create` → API-A → RTV → RTV-2026-0007 → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **จำนวน** ของบรรทัด | 3 (เกิน RTV qty=2) | ช่องจำนวนขึ้นสถานะ over (แดง) · ยอดผิด | ☐ |
| 2 | CLICK **ถัดไป**/ทบทวน แล้วดูปุ่มส่ง | — | ถูกบล็อก · ข้อความ **จำนวนลดเกินที่ลดได้: {item} (ลดได้อีก N)** | ☐ |
| 3 | TYPE → **จำนวน** | 2 | สถานะ over หาย · ไปต่อได้ | ☐ |

### TC-R04 — ไม่เลือกเหตุผล → บล็อก (negative · BR-05)
- group: เหตุผล · ความสำคัญ: กลาง · trace: FN-05 / BR_REASON_REQUIRED
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** โดยไม่เลือกเหตุผล | — | field-error **เลือกเหตุผล** · ยังอยู่ s2 | ☐ |

### TC-R05 — legal_basis ต่อ reason (happy · BR-17 · LOCK-03)
- group: เหตุผล · ความสำคัญ: กลาง · trace: BR-17 / LOCK-03 / FN-92
- Setup: role=officer-ap · seed=API-B · files=—
- Start: OPEN `#/create` → API-B → s2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT → **เหตุผล** | RS-OVERPRICE (ผู้ขายคิดราคาเกิน) | แสดง legal_basis hint "ผู้ขายคำนวณราคาสูงกว่าที่ตกลง/ผิดราคา" `[ASSUMED · OQ-DN-05]` | ☐ |
| 2 | SELECT → **เหตุผล** | RS-RTV (คืนสินค้า (อ้างใบคืนสินค้า RTV)) | legal_basis hint เปลี่ยนเป็น "รับคืนสินค้า/คืนของให้ผู้ขาย" · ช่อง RTV โผล่ | ☐ |
| 3 | SELECT → **เหตุผล** | RS-SHORT (ของขาด/ไม่ครบตามใบกำกับ) | legal_basis hint = "จัดส่งสินค้าขาดจำนวน/ไม่ครบตามใบกำกับ" | ☐ |

### TC-R06 — dn_date ก่อนวันที่ใบกำกับเดิม → บล็อก (negative · boundary)
- group: เหตุผล · ความสำคัญ: กลาง · trace: FN-05 / BR_DN_DATE_BEFORE_INVOICE
- Setup: role=officer-ap · seed=API-A (มีวันที่ใบกำกับเดิม vdate) · files=—
- Start: OPEN `#/create` → API-A → s2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **วันที่ใบลดหนี้** | วันที่ก่อน vdate | field-error **ต้องไม่ก่อนวันที่ใบกำกับเดิม** · บล็อกไปต่อ | ☐ |
| 2 | TYPE → **วันที่ใบลดหนี้** | วันที่ ≥ vdate | error หาย · ไปต่อได้ | ☐ |

### TC-R07 — ไม่ระบุผู้จัดทำ → บล็อก (negative)
- group: เหตุผล · ความสำคัญ: ต่ำ · trace: FN-05 / step2Validate
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s2 (เลือกเหตุผล + คำอธิบายครบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** โดยเว้นผู้จัดทำ | — | บล็อก/field-error ให้ระบุผู้จัดทำ · ยังอยู่ s2 (ถ้า prototype ไม่บังคับ → mark blocked พร้อม evidence) | ☐ |

### TC-06 — OVERPRICE ราคาลดต่อหน่วย ≤ ราคาเดิม (negative · FN-06 · BR-04)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-06 / AC-06 / BR-04 / BR_PRICE_EXCEEDS_ORIG
- Setup: role=officer-ap · seed=API-B (mode price · ราคา 4,100) · files=—
- Start: OPEN `#/create` → API-B → s2 (RS-OVERPRICE + คำอธิบาย) → s3
- ชุดข้อมูล: API-B · RS-OVERPRICE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัด s3 | — | ช่อง **ราคา/หน่วย** แก้ได้ (mode price) | ☐ |
| 2 | TYPE → **ราคา/หน่วย** | ค่าที่ > orig_price | meta บรรทัด "— ราคาลดเกินราคาเดิม" · บรรทัด over | ☐ |
| 3 | CLICK ทบทวน/ส่ง | — | บล็อก · ข้อความ **ราคาลดต่อหน่วยเกินราคาเดิม: {item}** | ☐ |
| 4 | TYPE → **ราคา/หน่วย** | ค่าที่ ≤ orig_price | over หาย · ไปต่อได้ | ☐ |

### TC-06b — OVERPRICE ราคาลดเท่าราคาเดิม (boundary · ผ่าน)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-06 / BR-04 (boundary)
- Setup: role=officer-ap · seed=API-B · files=—
- Start: OPEN `#/create` → API-B → s2 (RS-OVERPRICE) → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **ราคา/หน่วย** | = orig_price พอดี | ไม่ over · ผ่าน (boundary ≤) | ☐ |

### TC-07 — SHORT ลบบรรทัดอื่น + readd (happy · FN-07 · LOCK-01)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-07 / AC-07 / BR-03 / LOCK-01
- Setup: role=officer-ap · seed=API-C (หลายบรรทัด) · files=—
- Start: OPEN `#/create` → API-C → s2 (RS-SHORT) → s3
- ชุดข้อมูล: API-C · RS-SHORT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัด s3 | — | มีหลายบรรทัดจากใบเดิม · สินค้าล็อก (readonly) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายบรรทัดที่ 2 | — | บรรทัดหายไป · โผล่ chip "บรรทัดจากใบเดิมที่ไม่ได้ลด" (readd ได้) | ☐ |
| 3 | CLICK chip readd บรรทัดที่ลบ | — | บรรทัดกลับมาในตาราง | ☐ |
| 4 | VERIFY ลดเฉพาะบรรทัดที่เหลือ | — | สรุปยอดคิดจากบรรทัดที่มีอยู่เท่านั้น | ☐ |

### TC-07b — ลดจำนวนเฉพาะบรรทัดที่เลือก (happy · FN-07)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-07 / BR-03
- Setup: role=officer-ap · seed=API-C · files=—
- Start: OPEN `#/create` → API-C → RS-SHORT → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **จำนวน** บรรทัดที่ 1 | ค่าที่ ≤ qtyLeft | จำนวนเงินบรรทัด 1 อัปเดต · บรรทัดอื่นไม่เปลี่ยน | ☐ |
| 2 | VERIFY สรุปยอด | — | ยอดรวมสะท้อนเฉพาะบรรทัดที่ปรับ | ☐ |

### TC-08 — ลดหลายรอบ meta ถูกต้อง (edge · FN-08 · EC-02)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-08 / AC-08 / BR-03/10 / EC-02
- Setup: role=officer-ap · seed=API-A มี DN-0011 อนุมัติแล้ว (ลดแล้ว 1 เครื่อง) · files=—
- Start: OPEN `#/create` → API-A → s2 → s3
- ชุดข้อมูล: API-A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN s3 → VERIFY+จด meta บรรทัด | — | จด "ใบเดิม N × ฿P · ลดแล้ว ฿X · ลดจำนวนได้อีก M · ลดมูลค่าได้อีก ฿Y" (อ้าง step ถัดไป) | ☐ |
| 2 | VERIFY ค่า "ลดจำนวนได้อีก" | — | = จำนวนเดิม − ลดแล้วรวมทุกใบ (dn_applied + dn_held) | ☐ |
| 3 | TYPE → **จำนวน** เกิน M | M+1 | บรรทัด over + ถูกบล็อก (นับรวมข้ามทุกใบ) | ☐ |

### TC-09 — ยอด DN เกิน dnRoom → บล็อกส่ง + บอกยอด (negative · FN-09 · BR-02 · LOCK-04)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-09 / AC-09 / BR-02 / BR_DN_EXCEEDS_ROOM / LOCK-04
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s2 → s3
- ผ่านเมื่อ: draft บันทึกได้ แต่ส่งอนุมัติถูกบล็อก + แสดงยอด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ปรับจำนวน/ราคา ให้ grand > dnRoom | ค่าที่เกิน | hard-warn: **ยอดลดหนี้เกินมูลค่าที่ลดได้ (บันทึกร่างได้)** | ☐ |
| 2 | CLICK **บันทึกแบบร่าง** | — | บันทึกได้ (draft) · toast บันทึกแบบร่างใบลดหนี้ผู้ขายเรียบร้อย | ☐ |
| 3 | OPEN `#/view/<id>` → CLICK **ส่งอนุมัติ** | — | ถูกบล็อก · ข้อความ **ยอดลดหนี้เกินมูลค่าที่ลดได้ของใบตั้งหนี้ (ลดได้ ฿X) — แก้ไขร่างก่อน** | ☐ |

### TC-09b — grand เท่ากับ dnRoom พอดี (boundary · ผ่าน)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-09 / BR-02 (boundary ≤)
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ปรับให้ grand = dnRoom พอดี | = dnRoom | ไม่มี hard-warn · ส่งอนุมัติได้ (boundary ≤) | ☐ |

### TC-09c — บรรทัด net เกิน netLeft → บล็อก (negative · BR-03)
- group: ยอดลด · ความสำคัญ: กลาง · trace: FN-07/09 / BR-03 / BR_LINE_NET_EXCEEDED
- Setup: role=officer-ap · seed=API-A (มี DN ลดแล้วบางส่วน) · files=—
- Start: OPEN `#/create` → API-A → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ปรับมูลค่าบรรทัด > netLeft | เกิน netLeft | บรรทัด over · ข้อความ **มูลค่าลดเกินมูลค่าที่ลดได้ของบรรทัด: {item}** · บล็อก | ☐ |

### TC-10 — คำอธิบายเหตุผล <10 → บล็อก (negative · FN-10 · BR-05)
- group: ยอดลด · ความสำคัญ: สูง · trace: FN-10 / AC-10 / BR-05 / BR_REASON_TEXT_TOO_SHORT
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s2
- ชุดข้อมูล: RT-SHORT / RT-OK

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **คำอธิบายเหตุผล** | RT-SHORT ("ชำรุด") | field-error **ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร** · บล็อกไปต่อ/ส่ง | ☐ |
| 2 | TYPE → **คำอธิบายเหตุผล** | RT-OK | error หาย · ไปต่อได้ | ☐ |

---

## G4 · ส่วนลดท้ายบิล (FN-19 · BR-11/12 · LD-05 · AC-19)

### TC-19a — end-bill (฿) ลด input VAT ถูกต้อง ม.86/10 (happy · calc · BR-12)
- group: end-bill · ความสำคัญ: สูง · trace: FN-19 / AC-19(a) / BR-12 / ENG dn-totals
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=officer-ap · seed=API-A (มีบรรทัดคิด VAT ภาษีซื้อ) · files=—
- Start: OPEN `#/create` → API-A → s2 (ครบ) → s3
- ชุดข้อมูล: EB-OK-AMT
- ผ่านเมื่อ: summary แสดงฐานภาษีหลังหัก + input VAT คิดจากฐานใหม่ + grand ลดลง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN s3 → VERIFY+จดสรุปยอด (ก่อนเปิด end-bill) | — | จด: ราคาก่อน VAT=before · ภาษีซื้อ=vat · ยอดรวมหลัง VAT=after (อ้าง step ถัดไป) | ☐ |
| 2 | TOGGLE เปิด **ส่วนลดท้ายบิล** (การ์ด FN-19) | — | ช่อง mode ฿/% + value + ข้อความ **ลดได้สูงสุด ฿X** ปรากฏ | ☐ |
| 3 | SELECT mode = **฿** · TYPE value | EB-OK-AMT (≤ ebCap) | summary เพิ่มแถว "ยอดลดก่อน VAT" (netBefore ลดลง) | ☐ |
| 4 | VERIFY แถว **ภาษีซื้อที่ลด · คิดจากฐานใหม่ (ม.86/10)** | — | = vat − ebVat โดย ebVat = ebAmt×(vat/after) · **น้อยกว่า vat เดิม** ที่จดใน step 1 | ☐ |
| 5 | VERIFY แถว **ยอดลดหนี้สุทธิ** | — | = max(0, after − ebAmt) · น้อยกว่ายอดที่จดใน step 1 | ☐ |

### TC-19b — end-bill เกิน cap → block submit (negative · BR-11)
- group: end-bill · ความสำคัญ: สูง · trace: FN-19 / AC-19(b) / BR-11 / BR_ENDBILL_EXCEEDS_CAP
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s3
- ชุดข้อมูล: EB-OVER
- ผ่านเมื่อ: hard-warn + block submit · net ไม่ติดลบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE เปิด **ส่วนลดท้ายบิล** | — | card เปิด | ☐ |
| 2 | TYPE value เกิน ebCap | EB-OVER (สูงกว่ายอด after) | hard-warn **ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)** | ☐ |
| 3 | VERIFY แถว **ยอดลดหนี้สุทธิ** | — | grand = 0 (ไม่ติดลบ — clamp) | ☐ |
| 4 | OPEN s5 → CLICK **บันทึกและส่งอนุมัติ** | — | ถูกบล็อก · ข้อความ "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)" · ไม่เปิด submit modal | ☐ |
| 5 | TYPE value ลดให้ ≤ ebCap | ≤ ebCap | hard-warn หาย · ส่งได้ | ☐ |

### TC-19c — DOA tier คิดจาก grand หลัง end-bill (E2E · LD-05)
- group: end-bill · ความสำคัญ: สูง · trace: FN-19 / AC-19(c) / AC-11 / BR-07 / LD-05 / LOCK-05
- Setup: role=officer-ap · seed=API-C (ยอดสูง 526,440) · files=—
- Start: OPEN `#/create` → API-C → s2 (ครบ) → s3
- ผ่านเมื่อ: ปรับ end-bill ให้ grand ข้าม tier แล้วสายอนุมัติเปลี่ยนตาม grand หลังหัก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN s3 → ตั้งยอดให้ grand > 300,000 (ยังไม่เปิด end-bill) | — | จด grand (อ้าง step ถัดไป) | ☐ |
| 2 | OPEN s5 → VERIFY DOA preview | — | tier 3 · สาย ผจก.จัดซื้อ → ผจก.บัญชี → CFO | ☐ |
| 3 | กลับ s3 → TOGGLE end-bill → TYPE ให้ grand ลดมาอยู่ 50,000.01–300,000 | ค่าที่ทำให้ grand เข้า tier 2 | grand ลดลงตามที่ตั้ง | ☐ |
| 4 | OPEN s5 → VERIFY DOA preview อีกครั้ง | — | tier **เปลี่ยนเป็น 2** · สาย ผจก.จัดซื้อ → ผจก.บัญชี (ไม่มี CFO) — พิสูจน์คิดจาก grand หลัง end-bill | ☐ |

### TC-19d — end-bill mode % (happy · calc)
- group: end-bill · ความสำคัญ: กลาง · trace: FN-19 / BR-12
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s3
- ชุดข้อมูล: EB-OK-PCT (5%)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE เปิด end-bill → SELECT mode **%** → TYPE | 5 | ebRaw = after × 5% · summary แถว "ส่วนลดท้ายบิล (5%)" | ☐ |
| 2 | VERIFY netVat/netBefore | — | คำนวณตามสัดส่วน (ปัด 2 ตำแหน่ง) เหมือน mode ฿ | ☐ |

### TC-19e — end-bill + คงค้าง (net ≤ dnRoom) (boundary · BR-11+BR-02)
- group: end-bill · ความสำคัญ: กลาง · trace: FN-19 / BR-11 / BR-02
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ตั้งบรรทัด + end-bill ให้ grand = dnRoom พอดี | — | ไม่มี hard-warn ยอดเกิน · ส่งได้ (net ≤ dnRoom) | ☐ |

### TC-19f — ปิด end-bill กลับ → input VAT กลับเป็นปกติ (happy · toggle off)
- group: end-bill · ความสำคัญ: กลาง · trace: FN-19 / BR-12
- Setup: role=officer-ap · seed=API-A · files=—
- Start: OPEN `#/create` → API-A → s3 (เปิด end-bill แล้ว)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด netVat ขณะ end-bill เปิด | — | จดค่า netVat (ลดแล้ว) | ☐ |
| 2 | TOGGLE ปิด **ส่วนลดท้ายบิล** | — | summary กลับเป็น "ภาษีซื้อที่ลด" (ไม่มี "คิดจากฐานใหม่") · VAT = vat เดิม > netVat ที่จด | ☐ |

### TC-19g — end-bill VAT หลายอัตรา แบ่งตามสัดส่วน (edge · EC-CALC-01)
- group: end-bill · ความสำคัญ: ต่ำ · trace: FN-19 / BR-12 / EC-CALC-01 `[AI-DEFAULT]`
- Setup: role=officer-ap · seed=ใบที่มีบรรทัด VAT คละอัตรา/inclusive ปน · files=—
- Start: OPEN `#/create` → เลือกใบ → s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ตั้งบรรทัดคละ VAT (add/included/none) → เปิด end-bill | — | ebVat = ebAmt × (vat/after) แบ่งตามสัดส่วน VAT ในยอดรวม (ปัด 2 ตำแหน่ง) `[AI-DEFAULT]` | ☐ |

---

## G5 · ส่งอนุมัติ + DOA (FN-11 · AC-11)

### TC-11a — เลือกผู้อนุมัติครบ → pending (happy · FN-11)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-11 / AC-11 / BR-07 / LOCK-05
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=officer-ap (U-AP) · seed=draft ที่ valid (grand tier 1) · files=—
- Start: OPEN `#/view/<draftId>` → CLICK **ส่งอนุมัติ**
- ผ่านเมื่อ: chain freeze → pending_approval

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด · หัวข้อสาย "สายอนุมัติ (DOA-ACC-DN · tier X) — เลือกผู้อนุมัติแต่ละขั้น" | ☐ |
| 2 | VERIFY slot ตาม tier | — | tier 1 → 1 slot (ผจก.จัดซื้อ · ขั้นสุดท้าย) | ☐ |
| 3 | SELECT ผู้อนุมัติในแต่ละ slot | U-PUR (สมศักดิ์ จัดซื้อ) | slot แสดง chip ชื่อผู้อนุมัติ + ปุ่มเปลี่ยน | ☐ |
| 4 | CLICK **ส่งอนุมัติ** (ปุ่ม modal) | — | toast ส่งอนุมัติแล้ว · pill=รออนุมัติ | ☐ |
| 5 | VERIFY view หลังส่ง | — | สถานะ N/N ขั้น · ปุ่ม (สำหรับ owner) เหลือ **ยกเลิก** | ☐ |

### TC-11b — slot ไม่ครบ → บล็อก (negative · FN-11)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-11 / AC-11 / BR_SLOT_INCOMPLETE
- Setup: role=officer-ap · seed=draft valid tier 2 (2 slot) · files=—
- Start: OPEN `#/view/<draftId>` → CLICK **ส่งอนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด 2 slot | ☐ |
| 2 | SELECT เฉพาะ slot 1 (เว้น slot 2) | U-PUR | slot 2 ยังว่าง | ☐ |
| 3 | CLICK **ส่งอนุมัติ** | — | บล็อก · toast **เลือกผู้อนุมัติให้ครบทุกขั้น** · slot 2 ขึ้นเตือน | ☐ |

### TC-11c — สายอนุมัติเปลี่ยนตามมูลค่า (tier 1/2/3) (happy · BR-07 · LOCK-05)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-11 / BR-07 / DOA tier matrix / LOCK-05
- Setup: role=officer-ap · seed=draft 3 ใบ grand tier1/tier2/tier3 · files=—
- Start: OPEN `#/view/<id>` แต่ละใบ → CLICK **ส่งอนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด submit modal ใบ tier 1 (grand ≤50,000) | DOA-T1 | 1 slot: ผจก.จัดซื้อ | ☐ |
| 2 | เปิด submit modal ใบ tier 2 (50,000.01–300,000) | DOA-T2 | 2 slot: ผจก.จัดซื้อ → ผจก.บัญชี | ☐ |
| 3 | เปิด submit modal ใบ tier 3 (>300,000) | DOA-T3 | 3 slot: ผจก.จัดซื้อ → ผจก.บัญชี → CFO (ขั้นสุดท้าย) | ☐ |

### TC-11d — DOA preview ที่ s5 ตรงกับ submit modal (happy)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: FN-11 / step5Extra resolveDoa
- Setup: role=officer-ap · seed=API-C → grand tier 3 · files=—
- Start: OPEN `#/create` → API-C → ... → s5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY DOA preview ที่ s5 | — | แสดง tier + สายอนุมัติตาม grand | ☐ |
| 2 | บันทึกร่าง → เปิด submit modal | — | จำนวน slot ตรงกับ preview | ☐ |

### TC-11e — tier boundary 50,000.00 vs 50,000.01 (boundary)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: FN-11 / DOA tier matrix (boundary)
- Setup: role=officer-ap · seed=draft grand=50,000.00 และอีกใบ grand=50,000.01 · files=—
- Start: OPEN `#/view/<id>` → **ส่งอนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด submit modal ใบ grand=50,000.00 | — | tier 1 (1 slot) | ☐ |
| 2 | เปิด submit modal ใบ grand=50,000.01 | — | tier 2 (2 slot) | ☐ |

---

## G6 · อนุมัติ / ไม่อนุมัติ / re-check / SoD (FN-12/13/17/14)

### TC-12 — อนุมัติครบสาย → เลข DN no-gap (E2E · FN-12)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-12 / AC-12 / BR-08 / LOCK-06 / XT-01
- actor: ผู้อนุมัติ (ตามขั้น)
- Setup: role สลับตามขั้น (U-PUR→U-ACC→U-CFO ตาม tier) · seed=ใบ pending tier ที่ต้องการ · files=—
- Start: OPEN `#/view/<pendingId>` (login ผู้อนุมัติขั้นปัจจุบัน)
- ผ่านเมื่อ: อนุมัติขั้นสุดท้าย → ออกเลข DN-YYYY-NNNN

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สลับ persona เป็นผู้อนุมัติขั้น 1 (U-PUR) → OPEN view | — | เห็นปุ่ม **อนุมัติ** + **ไม่อนุมัติ** | ☐ |
| 2 | CLICK **อนุมัติ** (ขั้นกลาง) | — | toast **อนุมัติขั้น {n} แล้ว — ส่งต่อ {assignee}** · ขั้นถัดไป pending | ☐ |
| 3 | สลับ persona เป็นผู้อนุมัติขั้นสุดท้าย → CLICK **อนุมัติ** | — | toast **อนุมัติครบสาย — ออกใบลดหนี้ {code} · ลดยอดคงค้าง {inv}** | ☐ |
| 4 | VERIFY สถานะ + เลข | — | pill = **อนุมัติแล้ว · รอส่ง** · ช่องเลขที่ = DN-YYYY-NNNN (ไม่ใช่ "(ออกเลขเมื่ออนุมัติครบ)") | ☐ |

### TC-12b — เลข DN ออกเฉพาะ final approve (no-gap · negative timing)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-12 / BR-08 / LOCK-06
- Setup: role=officer-ap · seed=ใบ draft และใบ pending · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เลขที่ใบ draft | — | "(ออกเลขเมื่ออนุมัติครบ)" — ยังไม่มีเลข | ☐ |
| 2 | VERIFY เลขที่ใบ pending (ยังไม่ครบสาย) | — | ยังไม่มีเลข DN (ออกเมื่อ final approve เท่านั้น) | ☐ |

### TC-13 — ไม่อนุมัติ + เหตุผล → กลับร่าง + badge (E2E · FN-13)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-13 / AC-13 / EC-06 / FN-91
- actor: ผู้อนุมัติ
- Setup: role=U-PUR (ผู้อนุมัติขั้นปัจจุบัน) · seed=ใบ pending · files=—
- Start: OPEN `#/view/<pendingId>` (login ผู้อนุมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** | — | modal ใส่เหตุผล (บังคับ) | ☐ |
| 2 | CLICK ยืนยันโดยเว้นเหตุผล | — | บล็อก (เหตุผลบังคับ) | ☐ |
| 3 | TYPE เหตุผล → ยืนยัน | "จำนวนไม่ตรงกับใบคืนสินค้า" | toast ตีกลับเพื่อแก้ไข · pill กลับเป็น **ฉบับร่าง** | ☐ |
| 4 | VERIFY badge บน view (owner) | — | badge **ถูกตีกลับ 1 ครั้ง** | ☐ |
| 5 | OPEN tab **ลายเซ็น / อนุมัติ** | — | เห็น approval_history รอบที่ถูกตีกลับ + เหตุผล | ☐ |

### TC-13b — ตีกลับหลายรอบ → นับสะสม (edge · EC-06)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-13 / EC-06 / FN-91
- Setup: role สลับ maker/approver · seed=ใบเคยถูกตีกลับ 1 ครั้ง (API-B) · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ส่งอนุมัติใหม่ → ผู้อนุมัติ **ไม่อนุมัติ** อีกครั้ง (มีเหตุผล) | — | badge **ถูกตีกลับ 2 ครั้ง** | ☐ |
| 2 | OPEN tab ประวัติ/ลายเซ็น | — | เห็นทั้ง 2 รอบ (append-only ไม่ทับ) | ☐ |

### TC-14b — SoD: ผู้ส่งไม่เห็นปุ่มอนุมัติใบตัวเอง (permission · FN-14)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-14 / AC-14 / BR-07 / §5.3 SoD
- actor: เจ้าหน้าที่เจ้าหนี้ (ผู้ส่ง)
- Setup: role=U-AP (ผู้ส่งใบนี้เอง) · seed=ใบ pending ที่ U-AP เป็นผู้ส่ง · files=—
- Start: OPEN `#/view/<pendingId>` (login เป็นผู้ส่ง)
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ · เห็นแค่ยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบปุ่ม view (pending · เป็นผู้ส่งเอง) | — | **ไม่มีปุ่ม "อนุมัติ"** และ **ไม่มี "ไม่อนุมัติ"** (canActStep=false เพราะ submittedBy===ME) | ☐ |
| 2 | VERIFY ปุ่มที่มี | — | เห็นเฉพาะ **ยกเลิก** (ถอนจากรออนุมัติ) | ☐ |

### TC-17 — dnRoom ลดระหว่างรอ (ใบอื่น approved) → อนุมัติไม่ได้ (E2E · FN-17 · EC-01)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-17 / AC-17 / BR-02/BR-13 / EC-01 / BR_APPROVE_EXCEEDS_ROOM / LOCK-04 / FIX-01
- actor: ผู้อนุมัติขั้นสุดท้าย
- Setup: role สลับ · seed=ใบ pending ขั้นสุดท้าย (API-C) + มีอีกใบ DN ของ API-C ที่รอ approve · files=—
- Start: OPEN `#/view/<pendingId>`
- ผ่านเมื่อ: อนุมัติใบอื่นจน dnRoom ไม่พอ → ใบนี้อนุมัติขั้นสุดท้ายไม่ได้ (การจ่ายเงินไม่บล็อก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN tab **ใบตั้งหนี้อ้างอิง · ภาษีซื้อ** → VERIFY+จด มูลค่าที่ลดได้ (dnRoom) | — | จด dnRoom ก่อน (อ้าง step ถัดไป) | ☐ |
| 2 | อนุมัติ **ใบ DN อื่น** ของ API-C ให้ครบสาย (สลับ persona) จน dnRoom < grand ของใบนี้ | — | dnRoom ของ API-C ลดลงต่ำกว่ายอดลดหนี้ของใบที่รออยู่ | ☐ |
| 3 | สลับ persona ผู้อนุมัติขั้นสุดท้าย ใบเดิม → CLICK **อนุมัติ** | — | ถูกบล็อก · ข้อความ **อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ {inv} เหลือ ฿Y น้อยกว่ายอดลดหนี้ (มีใบลดหนี้อื่นได้รับอนุมัติเพิ่มระหว่างรออนุมัติ) · ให้ไม่อนุมัติกลับไปแก้** | ☐ |
| 4 | VERIFY สถานะ | — | ยังเป็น pending (ไม่ออกเลข DN) | ☐ |

### TC-17b — การจ่ายเงินไม่บล็อกการอนุมัติ (negative-of-CN · FIX-01 reversal · S-11)
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-17 / BR-13 / LD-07 / demoPay
- actor: ผู้อนุมัติขั้นสุดท้าย
- Setup: role สลับ · seed=ใบ pending ขั้นสุดท้าย · files=— · (ต้อง simulate ผ่าน demoPay ในหน้า ref tab)
- Start: OPEN `#/view/<pendingId>`
- ผ่านเมื่อ: จ่ายครบระหว่างรอ **ไม่บล็อก** อนุมัติ (grand ส่วนเกิน → vendorCredit)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ref tab → CLICK **จำลองรับชำระ** (demoPay) จน outstanding < grand | — | คงค้างของใบเดิมลดลงต่ำกว่ายอดลดหนี้ (แต่ dnRoom ไม่เปลี่ยน) | ☐ |
| 2 | สลับ persona ผู้อนุมัติขั้นสุดท้าย → CLICK **อนุมัติ** | — | **อนุมัติได้** (dnRoom ไม่หัก paid) · ออกเลข DN · ส่วนเกิน outstanding → vendorCredit | ☐ |

### TC-P07 — ไม่ใช่ผู้มีสิทธิ์ขั้นปัจจุบัน → อนุมัติไม่ได้ (permission)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-14 / §5.3 / ERR_NOT_CURRENT_APPROVER
- Setup: role=U-CFO (ขั้น 3) · seed=ใบ pending ที่ยังอยู่ขั้น 1 · files=—
- Start: OPEN `#/view/<pendingId>` (login CFO)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | CFO ยังไม่ถึงคิว → ไม่มีปุ่มอนุมัติ (ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน) | ☐ |

---

## G7 · ยกเลิก / ส่งผู้ขาย / ออกเอกสารแก้ไข (FN-15/16)

### TC-15 — ยกเลิก draft/pending + เหตุผล → คืน held (E2E · FN-15 · EC-05)
- group: ยกเลิก · ความสำคัญ: สูง · trace: FN-15 / AC-15 / EC-05 / BR-10 / XT-04
- actor: เจ้าหน้าที่เจ้าหนี้ (owner)
- Setup: role=U-AP · seed=ใบ draft/pending ที่มี dn_held · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ref tab → VERIFY+จด กันยอด (held) + มูลค่าที่ลดได้ | — | จด held และ dnRoom (อ้าง step ถัดไป) | ☐ |
| 2 | CLICK **ยกเลิก** | — | modal ใส่เหตุผล (บังคับ) | ☐ |
| 3 | CLICK ยืนยันเว้นเหตุผล | — | บล็อก (เหตุผลบังคับ) | ☐ |
| 4 | TYPE เหตุผล → ยืนยัน | "ผู้ขายขอยกเลิกคำขอ" | toast ยกเลิกเรียบร้อย · pill=ยกเลิก | ☐ |
| 5 | VERIFY banner บน view | — | note.danger **ยกเลิก โดย {ชื่อ} · {เหตุผล}** | ☐ |
| 6 | OPEN ใบเดิม/ref → VERIFY held คืน | — | held ลดลง = ยอดใบนี้ · dnRoom เพิ่มกลับเท่าที่จดใน step 1 | ☐ |

### TC-15b — ยกเลิก pending (ผู้ส่ง) (happy)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: FN-15 / §5.2
- Setup: role=U-AP (ผู้ส่ง) · seed=ใบ pending · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → TYPE เหตุผล → ยืนยัน | "ถอนคำขอ" | pill=ยกเลิก · toast ยกเลิกเรียบร้อย | ☐ |

### TC-16 — ส่งให้ผู้ขาย (approved→sent) (E2E · FN-16)
- group: ส่งผู้ขาย · ความสำคัญ: กลาง · trace: FN-16 / AC-16 / DOC-STORE
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=U-AP · seed=ใบ approved (มีเลข DN) · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม (approved) | — | **ออกเอกสารแก้ไข** + **บันทึกใบลดหนี้ผู้ขาย** + **ส่งให้ผู้ขาย** | ☐ |
| 2 | CLICK **ส่งให้ผู้ขาย** → ยืนยัน | — | toast ส่ง {code} ให้ผู้ขายแล้ว · pill=**ส่งผู้ขายแล้ว** | ☐ |

### TC-16b — ส่งสำเนาซ้ำ (resend) ไม่เปลี่ยนวันที่ส่งเดิม (edge · FN-16)
- group: ส่งผู้ขาย · ความสำคัญ: กลาง · trace: FN-16 / AC-16
- Setup: role=U-AP · seed=ใบ sent · files=—
- Start: OPEN `#/view/<sentId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม (sent) | — | **ออกเอกสารแก้ไข** + **บันทึกใบลดหนี้ผู้ขาย** + **ส่งสำเนาซ้ำ** | ☐ |
| 2 | OPEN detail → VERIFY+จด วันที่ส่งเดิม | — | จดวันที่ส่ง (อ้าง step ถัดไป) | ☐ |
| 3 | CLICK **ส่งสำเนาซ้ำ** → ยืนยัน | — | toast ส่งสำเนาซ้ำแล้ว · สถานะยังเป็น ส่งผู้ขายแล้ว | ☐ |
| 4 | VERIFY วันที่ส่ง | — | = วันที่ส่งเดิมที่จดใน step 2 (ไม่เปลี่ยน) | ☐ |

### TC-NEG-05 — ออกเอกสารแก้ไข = display-only (negative · XT-05 · LD-04)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: XT-05 / LD-04 / OQ-DN-04
- Setup: role=U-AP · seed=ใบ approved · files=—
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
| 2 | CLICK **อนุมัติ** | — | ออกเลข DN · pill=อนุมัติแล้ว · รอส่ง | ☐ |

---

## G8 · เครดิตคงเหลือกับผู้ขาย + ภาษีซื้อกลับ (FN-20/21)

### TC-20a — ใบจ่ายครบยังออก DN ได้ → vendorCredit split (E2E · FN-20 · BR-13 · FIX-01)
- group: vendor-credit · ความสำคัญ: สูง · trace: FN-04/FN-20 / AC-20 / BR-13 / LOCK-04 / XT-07 / LD-07
- actor: เจ้าหน้าที่เจ้าหนี้ → ผู้อนุมัติ
- Setup: role=U-AP → สลับผู้อนุมัติ · seed=API-PAID (API-2026-0038 · จ่ายครบ · dnRoom>0) + RTV ของใบนี้ · files=—
- Start: OPEN `#/create` → เลือก API-PAID
- ชุดข้อมูล: API-PAID · RS-RTV
- ผ่านเมื่อ: ออก DN บนใบจ่ายครบได้ · grand > outstanding → applyToAp=min(grand,outstanding) · vendorCredit=grand−applyToAp>0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY picker | — | API-2026-0038 (จ่ายครบ) **ยังโผล่** (dnRoom ไม่หัก paid) | ☐ |
| 2 | เลือก API-PAID → RTV → กรอกครบ → บันทึกและส่งอนุมัติ → อนุมัติครบสาย | grand > outstanding | ออกเลข DN · audit **หักหนี้ค้าง ฿Y · เครดิตคงเหลือกับผู้ขาย ฿Z** | ☐ |
| 3 | OPEN ref tab | — | แยกยอด **หักจากหนี้ค้าง (applyToAp)** = min(grand, outstanding) · **เครดิตคงเหลือกับผู้ขาย (vendorCredit)** = grand − applyToAp > 0 | ☐ |
| 4 | OPEN `#/list` → VERIFY KPI card | — | ยอด "เครดิตคงเหลือกับผู้ขาย" เพิ่มขึ้นตาม vendorCredit ของใบนี้ | ☐ |

> **TC-20b** (card เปิด modal รายผู้ขาย display-only · FN-20 / AC-20(4) / OQ-DN-06) อยู่ในกลุ่ม **G1** ด้านบน — วางไว้ที่หน้ารายการ (P-01) ตามตำแหน่งจริงบนจอ.

### TC-21a — DN approved ไม่มี vendorCn → "รอใบลดหนี้ผู้ขาย" (UI · FN-21 · BR-14)
- group: vat-reversal · ความสำคัญ: สูง · trace: FN-21 / AC-21(1) / BR-14 / EC-07 / LOCK-07
- actor: เจ้าหน้าที่เจ้าหนี้
- Setup: role=U-AP · seed=ใบ approved ที่ **ยังไม่กรอก vendorCn** (VCN-NONE) · files=—
- Start: OPEN `#/view/<approvedId>` → CLICK tab **ใบตั้งหนี้อ้างอิง · ภาษีซื้อ**
- ผ่านเมื่อ: ลด AP แล้วแต่ยังไม่ลดภาษีซื้อ · note.warn รอเอกสาร · มีปุ่มบันทึกภายหลัง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วนผลกระทบภาษีซื้อ (ภ.พ.30) | — | note.warn **รอใบลดหนี้ผู้ขาย** (read-only) · input VAT ยังไม่ลง ภ.พ.30 (สถานะ "รอเอกสาร") | ☐ |
| 2 | VERIFY dn_applied ใบเดิม | — | คงค้างลดแล้ว (AP ลดทันที) แม้ยังไม่ลดภาษีซื้อ | ☐ |
| 3 | VERIFY ปุ่ม | — | มีปุ่ม **บันทึกใบลดหนี้ผู้ขาย** (openVendorCn) บนใบ approved | ☐ |

### TC-21b — บันทึก vendorCn → input VAT เดือน vendorCnDate (E2E · FN-21 · ม.82/10)
- group: vat-reversal · ความสำคัญ: สูง · trace: FN-21 / AC-21(2,3) / BR-14 / XT-02 / API-16 / LD-08
- actor: เจ้าหน้าที่เจ้าหนี้ (หรือ ผจก.บัญชี)
- Setup: role=U-AP · seed=ใบ approved ยังไม่มี vendorCn · files=—
- Start: OPEN `#/view/<approvedId>` → ref tab → CLICK **บันทึกใบลดหนี้ผู้ขาย**
- ชุดข้อมูล: VCN-OK (เช่น TFS-6650)
- ผ่านเมื่อ: input VAT ลง ภ.พ.30 เดือน = vendorCnDate · audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกใบลดหนี้ผู้ขาย** | — | modal เปิด · field label **เลขที่ใบลดหนี้จากผู้ขาย (ถ้าได้รับแล้ว)** placeholder "เช่น TFS-6650" + **วันที่ได้รับใบลดหนี้ผู้ขาย** + helper "ใช้กำหนดเดือนภาษีที่ลดภาษีซื้อใน ภ.พ.30" | ☐ |
| 2 | TYPE เลขที่ + วันที่ (VCN-OK) → ยืนยัน | TFS-6650 · วันที่เดือนปัจจุบัน | toast **บันทึกใบลดหนี้ผู้ขายแล้ว — ลดภาษี...** · สถานะเอกสารไม่เปลี่ยน (ยัง approved) | ☐ |
| 3 | OPEN ref tab → VERIFY ภาษีซื้อ | — | note.warn "รอใบลดหนี้ผู้ขาย" หาย · input_vat_line (ค่าลบ) = netVat · **เดือนภาษี = เดือนของ vendorCnDate** (ม.82/10) | ☐ |
| 4 | OPEN tab ประวัติ | — | เห็น audit **บันทึกใบลดหนี้ผู้ขาย {vendor_cn} ({vendor_cn_date})** | ☐ |

### TC-21c — openVendorCn บันทึกภายหลังบนใบ sent (edge · FN-21)
- group: vat-reversal · ความสำคัญ: กลาง · trace: FN-21 / BR-14 / §5.2 (approved/sent locked ยกเว้น vendorCn)
- Setup: role=U-AP · seed=ใบ sent ที่ยังไม่มี vendorCn · files=—
- Start: OPEN `#/view/<sentId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม (sent) | — | มีปุ่ม **บันทึกใบลดหนี้ผู้ขาย** (บันทึกได้แม้ locked แก้ไข) | ☐ |
| 2 | CLICK **บันทึกใบลดหนี้ผู้ขาย** → กรอก VCN-OK → ยืนยัน | TFS-xxxx · วันที่ | input VAT ลง ภ.พ.30 เดือน vendorCnDate · state ยังเป็น ส่งผู้ขายแล้ว | ☐ |

### TC-CA-01 — vendorCn ซ้ำ / เดือนภาษีปิดงวด (edge · OQ)
- group: vat-reversal · ความสำคัญ: ต่ำ · trace: EC-CA-01 / BR-14 / OQ CA-01
- Setup: role=U-AP · seed=ใบ approved + มีใบอื่นใช้ vendorCn เดียวกัน / วันที่อยู่เดือนที่ปิดงวดแล้ว · files=— · **(ต้อง simulate — flag warn ไม่ block รอบนี้)**
- Start: OPEN `#/view/<approvedId>` → openVendorCn

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE vendorCn ซ้ำ / วันที่เดือนปิดงวด → ยืนยัน | — | flag warn (ยก OQ CA-01) · **ไม่ block** รอบนี้ (ถ้า prototype ไม่ทำ → mark blocked พร้อม evidence) | ☐ |

---

## G9 · View tabs: ref / history / pdf (FN-18/91/92)

### TC-18 — ref tab: คงค้างก่อน/หลัง + ภาษีซื้อ + JE + split (UI · FN-18)
- group: view-ref · ความสำคัญ: กลาง · trace: FN-18 / AC-18 / BR-09 / BR-13 / LOCK-07 / XT-01/03
- Setup: role=U-AP · seed=ใบ approved (มี vendorCn แล้ว) · files=—
- Start: OPEN `#/view/<approvedId>` → CLICK tab **ใบตั้งหนี้อ้างอิง · ภาษีซื้อ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วนใบเดิม | — | ยอดสุทธิใบเดิม · จ่ายแล้ว · ลดแล้ว · **คงค้างก่อน** · **คงค้างหลังใบนี้** · กันยอด | ☐ |
| 2 | VERIFY แยกยอด | — | **หักจากหนี้ค้าง (applyToAp)** + **เครดิตคงเหลือกับผู้ขาย (vendorCredit)** | ☐ |
| 3 | VERIFY ส่วน **ผลกระทบภาษีซื้อ (VAT Report ภ.พ.30)** | — | input_vat_line (ค่าลบ) = netVat · เดือน = vendorCnDate (ม.82/10) | ☐ |
| 4 | VERIFY ส่วน **รายการบัญชี (จำลอง)** JE | — | Dr 2110 เจ้าหนี้ = applyToAp · Cr 5xxx รับคืน/ส่วนลด = netBefore · Cr 1150 ภาษีซื้อ = netVat | ☐ |

### TC-18b — JE ภาษีซื้อสะท้อน netVat หลัง end-bill (UI · BR-09/BR-12)
- group: view-ref · ความสำคัญ: ต่ำ · trace: FN-18 / BR-09 / BR-12
- Setup: role=U-AP · seed=ใบ approved ที่มี end-bill · files=—
- Start: OPEN `#/view/<id>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY JE Cr 1150 ภาษีซื้อ | — | = netVat (หลังหัก ebVat) ไม่ใช่ vat เต็ม | ☐ |

### TC-91 — ประวัติ append-only ทุกการกระทำ (E2E · FN-91)
- group: view-history · ความสำคัญ: กลาง · trace: FN-91 / AC-91 / BR-15 / LOCK-10
- Setup: role สลับ · seed=ใบที่ผ่าน สร้าง→ส่ง→อนุมัติ→บันทึก vendorCn→ส่งผู้ขาย · files=—
- Start: OPEN `#/view/<sentId>` → CLICK tab **ประวัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รายการประวัติ | — | เห็น: สร้าง · ส่งอนุมัติ · อนุมัติแต่ละขั้น · ออกเลข · บันทึก vendorCn · ส่งผู้ขาย (เรียงตามเวลา) | ☐ |
| 2 | VERIFY วันที่ | — | ทุกวันที่เป็น **ค.ศ.** | ☐ |
| 3 | VERIFY ไม่มีปุ่มลบ/แก้ประวัติ | — | ไม่มีปุ่ม ลบ/แก้ไข รายการประวัติ (append-only · unshift-only) | ☐ |

### TC-91b — ประวัติเก็บรอบตีกลับ (append-only · FN-91)
- group: view-history · ความสำคัญ: ต่ำ · trace: FN-91 / EC-06
- Setup: role สลับ · seed=ใบเคยถูกตีกลับ · files=—
- Start: OPEN `#/view/<id>` → tab ประวัติ / ลายเซ็น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รอบตีกลับ | — | รอบก่อนหน้ายังอยู่ (ไม่ถูกทับ) | ☐ |

### TC-92 — PDF ครบตาม ม.86/10 (UI · FN-92)
- group: view-pdf · ความสำคัญ: กลาง · trace: FN-92 / AC-92 / BR-17 / LOCK-06/10
- Setup: role=U-AP · seed=ใบ approved (มีเลข DN) · files=—
- Start: OPEN `#/view/<approvedId>` → CLICK tab **PDF Preview**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว PDF | — | เลข DN-YYYY-NNNN · **อ้างเลข + วันที่ใบกำกับเดิม** | ☐ |
| 2 | VERIFY ตารางมูลค่า | — | **มูลค่าเดิม · มูลค่าที่ถูกต้อง · ผลต่าง** · ภาษีซื้อ (netVat) | ☐ |
| 3 | VERIFY เหตุผล + legal_basis | — | เหตุผล + legal_basis (ม.86/10) พิมพ์ลง PDF · 3 ช่องเซ็น | ☐ |
| 4 | VERIFY วันที่ | — | วันที่บน PDF เป็น **ค.ศ.** | ☐ |
| 5 | CLICK ปุ่มดาวน์โหลด PDF | — | ดาวน์โหลดไฟล์ PDF (mock toast) | ☐ |

---

## G10 · Status guards + Negatives

### TC-GRD-01 — submit เฉพาะ draft (negative · guard)
- group: guards · ความสำคัญ: สูง · trace: §5.2 / BR_SUBMIT_DRAFT_ONLY
- Setup: role=U-AP · seed=ใบ pending/approved · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มส่งอนุมัติในใบ pending | — | ไม่มีปุ่ม "ส่งอนุมัติ" (ไม่ใช่ draft) | ☐ |
| 2 | (ถ้ามีทางลัด) พยายาม submit ใบ non-draft | — | toast **ส่งอนุมัติได้เฉพาะฉบับร่าง** | ☐ |

### TC-GRD-02 — edit เฉพาะ draft (negative · guard)
- group: guards · ความสำคัญ: สูง · trace: §5.2 / BR_EDIT_DRAFT_ONLY
- Setup: role=U-AP · seed=ใบ approved (id ทราบ) · files=—
- Start: OPEN `#/edit/<approvedId>` (พิมพ์ route ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/<approvedId>` | — | toast **แก้ไขได้เฉพาะฉบับร่าง** · เด้งไป `#/view/<id>` | ☐ |

### TC-GRD-03 — cancel เฉพาะ draft/pending (negative · guard)
- group: guards · ความสำคัญ: สูง · trace: §5.2 / BR_CANCEL_STATE_INVALID
- Setup: role=U-AP · seed=ใบ approved/sent · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มยกเลิกในใบ approved | — | ไม่มีปุ่ม "ยกเลิก" (มีแต่ ออกเอกสารแก้ไข/บันทึก vendorCn/ส่งให้ผู้ขาย) | ☐ |
| 2 | (ถ้ามีทางลัด row menu) พยายามยกเลิก | — | toast **ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ "ออกเอกสารแก้ไข"** | ☐ |

### TC-GRD-04 — send เฉพาะ approved (negative · guard)
- group: guards · ความสำคัญ: กลาง · trace: §5.2 / BR_SEND_STATE_INVALID
- Setup: role=U-AP · seed=ใบ draft/pending · files=—
- Start: OPEN `#/view/<draftId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มส่งให้ผู้ขายในใบ draft/pending | — | ไม่มีปุ่ม "ส่งให้ผู้ขาย" (ต้องอนุมัติครบก่อน · "ต้องอนุมัติครบก่อนส่ง") | ☐ |

### TC-GRD-05 — vendorCn เฉพาะ approved/sent (negative · guard)
- group: guards · ความสำคัญ: กลาง · trace: §5.2 / BR-14 / BR_VENDORCN_STATE_INVALID
- Setup: role=U-AP · seed=ใบ draft/pending · files=—
- Start: OPEN `#/view/<draftId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบันทึกใบลดหนี้ผู้ขายในใบ draft/pending | — | ไม่มีปุ่ม "บันทึกใบลดหนี้ผู้ขาย" (บันทึกได้เฉพาะใบที่อนุมัติแล้ว) | ☐ |

### TC-14a — tile ลดลอยปิด (negative · = FN-02 confirm)
- group: negatives · ความสำคัญ: สูง · trace: FN-02 / BR-16 / AC-14
- Setup: role=U-AP · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tile **ลดหนี้ไม่อ้างใบ** | — | toast **ลดหนี้ไม่อ้างใบตั้งหนี้ถูกปิดไว้ (OQ-DN-01)** · tile ยัง disabled | ☐ |

### TC-13c — ใบ dnRoom=0 ไม่โผล่ (negative · FN-04 · EC-04)
- group: negatives · ความสำคัญ: กลาง · trace: FN-04 / AC-13 / BR-01 / EC-04
- Setup: role=U-AP · seed=API-FULL (ลดเต็มมูลค่าแล้ว dnRoom=0) · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY picker | — | ไม่มีใบที่ dnRoom=0 (ลดเต็มมูลค่าแล้ว) | ☐ |

### TC-NEG-03 — refund เมื่อจ่ายครบ ไม่รองรับ (negative · out of scope)
- group: negatives · ความสำคัญ: กลาง · trace: OOS / OQ-DN-03
- Setup: role=U-AP · seed=API-PAID · files=—
- Start: OPEN `#/create` / `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไม่มีทางเรียกเงินคืน | — | ไม่มีปุ่ม refund/คืนเงิน · ใบจ่ายครบใช้ **vendorCredit** แทน (ไม่ใช่ refund) | ☐ |

### TC-NEG-04 — no hard delete (negative · BR-15)
- group: negatives · ความสำคัญ: สูง · trace: BR-15 / FN-91 / LOCK-10
- Setup: role=U-AP · seed=ใบหลายสถานะ · files=—
- Start: OPEN `#/list` และ `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY row menu ⋮ | — | ไม่มีเมนู "ลบ" (มีแค่ ดูรายละเอียด/แก้ไข(draft)/ทำสำเนา/ยกเลิก) | ☐ |
| 2 | VERIFY ใน view | — | ไม่มีปุ่มลบเอกสาร · ยกเลิก = เปลี่ยนสถานะ cancelled (ไม่หายจาก list) | ☐ |

### TC-LK-09 — UI #67.1: อนุญาตเฉพาะ hard-warn/field-error/danger/note.warn (LOCK-09)
- group: negatives · ความสำคัญ: ต่ำ · trace: LOCK-09 / 01_UI §1.6
- Setup: role=U-AP · seed=API-A · files=—
- Start: OPEN `#/create` → s3 · และ view ref tab (approved ไม่มี vendorCn)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ข้อความช่วยเหลือบนฟอร์ม | — | มีเฉพาะ ① hard-warn ยอดเกิน · ② field-error/บรรทัดเกิน · ③ note.danger ยกเลิก · ④ hard-warn ส่วนลดท้ายบิลเกิน + helper max-cap · ⑤ note.warn "รอใบลดหนี้ผู้ขาย" — **ไม่มี hint/info banner อื่น** | ☐ |

---

## G11 · Permission matrix (SoD · §5.3)

### TC-P01 — officer-ap ทำ create/edit/submit/cancel/send/vendorCn ได้ (permission · allow)
- group: permission · ความสำคัญ: สูง · trace: §5.3 (officer-ap allow)
- Setup: role=U-AP · seed=ใบ draft/approved ของ officer · files=—
- Start: OPEN `#/list` / `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มสร้าง | — | เห็นปุ่ม **สร้างใบลดหนี้ผู้ขาย** | ☐ |
| 2 | VERIFY view ใบ draft | — | เห็น ยกเลิก/แก้ไข/ส่งอนุมัติ | ☐ |
| 3 | VERIFY view ใบ approved | — | เห็น ออกเอกสารแก้ไข/บันทึก vendorCn/ส่งให้ผู้ขาย | ☐ |

### TC-P02 — mgr-purchase สร้างไม่ได้ (permission · deny)
- group: permission · ความสำคัญ: สูง · trace: §5.3 (mgr create = —)
- Setup: role=U-PUR · seed=— · files=—
- Start: OPEN `#/list` (login ผจก.จัดซื้อ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มสร้าง | — | ผจก.จัดซื้อไม่ควรสร้างได้ (create = officer-ap เท่านั้น) — ปุ่มสร้างไม่ทำงาน/ไม่มีสิทธิ์สร้าง | ☐ |

### TC-P03 — mgr-purchase อนุมัติขั้น 1 ได้ (permission · allow)
- group: permission · ความสำคัญ: สูง · trace: §5.3 (mgr-purchase approve ขั้น1)
- Setup: role=U-PUR · seed=ใบ pending อยู่ขั้น 1 · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | เห็น **อนุมัติ** + **ไม่อนุมัติ** (ขั้น 1) | ☐ |

### TC-P04 — mgr-acc อนุมัติขั้น 2 (tier2+) + vendorCn ได้ (permission · allow)
- group: permission · ความสำคัญ: กลาง · trace: §5.3 (mgr-acc approve ขั้น2 + vendorCn)
- Setup: role=U-ACC · seed=ใบ pending tier2 ถึงขั้น 2 + ใบ approved ไม่มี vendorCn · files=—
- Start: OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มอนุมัติ (ใบ pending ขั้น 2) | — | ผจก.บัญชีเห็น **อนุมัติ** (ขั้น 2) | ☐ |
| 2 | VERIFY ปุ่ม vendorCn (ใบ approved) | — | ผจก.บัญชีเห็น **บันทึกใบลดหนี้ผู้ขาย** (มีสิทธิ์ vendorCn) | ☐ |

### TC-P05 — owner อนุมัติใบตัวเองไม่ได้ (permission · deny · SoD)
- group: permission · ความสำคัญ: สูง · trace: §5.3 / BR-07 / FN-14
- Setup: role=U-AP (ผู้ส่งเอง มีบทบาทซ้อน) · seed=ใบ pending ที่ตัวเองส่ง · files=—
- Start: OPEN `#/view/<pendingId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม | — | ไม่มีปุ่มอนุมัติ (submittedBy === ME → canActStep false) · เห็นแค่ ยกเลิก | ☐ |

### TC-P08 — ทุก role ดูรายละเอียดได้ (permission · view allow)
- group: permission · ความสำคัญ: ต่ำ · trace: §5.3 (View = ทุก role)
- Setup: role=U-PUR/U-ACC/U-CFO · seed=ใบใด ๆ · files=—
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

## G12 · Cross-module (XT-01..07 · §6.9)

### TC-X01 — approve → ap_open_item dn_applied↑ / outstanding ลด (XT-01)
- group: cross-module · ความสำคัญ: สูง · trace: XT-01 / BR-02/09 / FN-18
- Setup: role สลับ · seed=ใบ pending + ใบเดิม API-A มี outstanding · files=— · (prototype: ตรวจผลที่ ref tab แทนหน้า AP จริง)
- Start: OPEN `#/view/<pendingId>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ref tab → VERIFY+จด คงค้างก่อน | — | จดคงค้างก่อน (อ้าง step ถัดไป) | ☐ |
| 2 | อนุมัติครบสาย (สลับ persona) | — | toast อนุมัติครบสาย · ออกเลข DN | ☐ |
| 3 | OPEN ref tab อีกครั้ง | — | **คงค้างหลังใบนี้** = คงค้างก่อน − applyToAp (ปิดเมื่อ = 0) · dn_applied += applyToAp | ☐ |

### TC-X02 — บันทึก vendorCn → ภ.พ.30 input VAT เดือน vendorCnDate (XT-02)
- group: cross-module · ความสำคัญ: สูง · trace: XT-02 / BR-14 / ม.82/10 / LOCK-07
- Setup: role=U-AP · seed=ใบ approved มี vendorCn แล้ว · files=—
- Start: OPEN `#/view/<approvedId>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ผลกระทบภาษีซื้อ | — | input_vat_line (ค่าลบ) = netVat · เดือน = **vendorCnDate** (ม.82/10) | ☐ |
| 2 | VERIFY stat tile P-01 "ภาษีซื้อที่ลดเดือนนี้" | — | รวม netVat ของใบที่มี vendorCn เดือนนี้ (ไม่รวมใบที่ "รอเอกสาร") | ☐ |

### TC-X03 — approve → JE mock (XT-03)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-03 / BR-09 / LOCK-08
- Setup: role=U-AP · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รายการบัญชี (จำลอง) | — | Dr 2110 เจ้าหนี้ applyToAp · Cr 5xxx รับคืน/ส่วนลด netBefore · Cr 1150 ภาษีซื้อ netVat · ป้าย "จำลอง" (demo) | ☐ |

### TC-X04 — cancel → held คืน (XT-04)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-04 / BR-10 / EC-05
- Setup: role=U-AP · seed=ใบ draft/pending มี held · files=—
- Start: OPEN `#/view/<id>` → ref tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด กันยอด (held) | — | จด held ปัจจุบัน | ☐ |
| 2 | CLICK ยกเลิก + เหตุผล → ยืนยัน | "ยกเลิก" | pill=ยกเลิก | ☐ |
| 3 | OPEN ref/ใบเดิม → VERIFY dnRoom | — | held คืน · dnRoom เพิ่มกลับ = held ที่จด | ☐ |

### TC-X05 — ยกเลิกหลังอนุมัติไม่รองรับ → revise-doc (XT-05)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-05 / LD-04 (= TC-NEG-05)
- Setup: role=U-AP · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไม่มีปุ่มยกเลิก · มี "ออกเอกสารแก้ไข" | — | ยกเลิกหลังอนุมัติปิด · revise-doc display-only ไม่ถอนยอด | ☐ |

### TC-X06 — RTV ผูกใบเดียวกัน qty ≤ คืน (XT-06)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-06 / BR-06 (= TC-R01/R03)
- Setup: role=U-AP · seed=API-A + RTV-2026-0007 (ของใบเดียวกัน) · files=—
- Start: OPEN `#/create` → API-A → RTV

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตัวเลือกใบคืนสินค้า | — | เฉพาะ RTV ของ API-A (ใบเดียวกัน) · qty ปิดที่จำนวนที่คืน | ☐ |

### TC-X07 — ใบจ่ายครบ → vendorCredit ledger (XT-07)
- group: cross-module · ความสำคัญ: สูง · trace: XT-07 / BR-13 / FN-20 (= TC-20a/20b)
- Setup: role สลับ · seed=API-PAID → DN approved มี vendorCredit>0 · files=—
- Start: OPEN `#/list` → KPI card

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY KPI card + modal | — | vendorCredit ของ DN ใบจ่ายครบ ปรากฏใน ledger รายผู้ขาย (display-only · flow OQ-DN-06) | ☐ |

---

## G13 · Scope Lock verify (LOCK)

### TC-LK-01 — Pattern Q document + B2 v2 line editor (LOCK-01)
- group: scope-lock · ความสำคัญ: ต่ำ · trace: LOCK-01
- Setup: role=U-AP · seed=API-A + ใบ approved · files=—
- Start: OPEN `#/create` → s3 และ OPEN `#/view/<id>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY s3 line editor | — | ตารางบรรทัด B2 v2 (สินค้า/จำนวน/หน่วย/ราคา/ส่วนลด%/ภาษี VAT7 ภาษีซื้อ/จำนวนเงิน) · สินค้า lock | ☐ |
| 2 | VERIFY view drawer | — | 5 tabs (รายละเอียด/ใบตั้งหนี้อ้างอิง·ภาษีซื้อ/PDF Preview/ลายเซ็น·อนุมัติ/ประวัติ) | ☐ |

### TC-LK-10 — ค.ศ. ทุกที่ + append-only (LOCK-10)
- group: scope-lock · ความสำคัญ: ต่ำ · trace: LOCK-10 / BR-15
- Setup: role=U-AP · seed=ใบ sent (ผ่านหลาย action) · files=—
- Start: OPEN `#/view/<sentId>`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY วันที่ทุก tab (detail/history/pdf) | — | เป็น ค.ศ. ทั้งหมด (ไม่มี พ.ศ.) | ☐ |
| 2 | VERIFY ประวัติ | — | append-only (ไม่มีลบ/แก้) | ☐ |

### TC-LK-06 — doccfg DN-YYYY-NNNN + PDF อ้างเลขใบเดิม (LOCK-06)
- group: scope-lock · ความสำคัญ: ต่ำ · trace: LOCK-06 / BR-08 / FN-92
- Setup: role=U-AP · seed=ใบ approved · files=—
- Start: OPEN `#/view/<approvedId>` → tab PDF

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รูปแบบเลข | — | DN-YYYY-NNNN (ออกตอน final approve · no-gap) | ☐ |
| 2 | VERIFY PDF | — | อ้างเลข + วันที่ใบกำกับเดิม | ☐ |

---

## G14 · Edge cases (EC)

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
- Setup: role=U-AP · seed=draft valid · files=— · **(ต้อง simulate: กดส่ง/บันทึกซ้ำเร็ว ๆ)**
- Start: OPEN `#/view/<draftId>` → submit modal

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** (ปุ่ม modal) ซ้ำเร็ว ๆ 2 ครั้ง | — | busyGate กันซ้ำ · ไม่เกิด 2 ใบ/2 pending (cached response) | ☐ |

### TC-CALC-01 — ปัดเศษ ebVat 2 ตำแหน่ง (edge · `[AI-DEFAULT]`)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-CALC-01 / BR-12 / OQ-EB-01 `[AI-DEFAULT]`
- Setup: role=U-AP · seed=ใบที่ทำให้ ebVat มีเศษ · files=—
- Start: OPEN `#/create` → s3 → เปิด end-bill

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY netVat/ebBase | — | แสดงปัด 2 ตำแหน่ง (formatMoney) ตาม HTML totals() `[AI-DEFAULT]` | ☐ |

### TC-FU-01 — ไฟล์แนบ type/size (edge · `[AI-DEFAULT]`)
- group: edge · ความสำคัญ: ต่ำ · trace: EC-FU-01 / OQ-FU-01 `[AI-DEFAULT]`
- Setup: role=U-AP · seed=draft · files=`dn-attach-ok.pdf`, `dn-attach-big.pdf`
- Start: OPEN `#/create` → s4 (เอกสารแนบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `dn-attach-ok.pdf` | jpg/png/pdf ≤10MB | แนบสำเร็จ `[AI-DEFAULT]` | ☐ |
| 2 | UPLOAD `dn-attach-big.pdf` (>10MB) | เกินขนาด | ถูกปฏิเสธ (ต้อง simulate ถ้า prototype ไม่บังคับ size) `[AI-DEFAULT]` | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `F-ACC-DN_debit-note.html` ใน browser. หน้าเริ่มที่ `#/list`.
2. **ตั้ง role** ผ่าน persona switcher (DEMO): เลือกบุคคลตาม `Setup: role=` ก่อนเริ่มเคส (U-AP/U-PUR/U-ACC/U-CFO).
3. แต่ละเคส **เริ่มที่ `Start` route ของตัวเอง** (refresh-safe) — ห้ามพึ่งสถานะค้างจากเคสก่อน. สำหรับเคสที่ต้องมี seed (draft/pending/approved) ให้สร้าง/เดินสถานะให้ถึงก่อน หรือใช้ข้อมูล mock ที่มากับ prototype.
4. เดินทีละ step: ทำ Action (ตาม verb tag) → ตรวจ Expected ด้วยตา → ติ๊ก Result ☐→✔/✘.
5. เคสที่มี **Expected แบบส่วนต่าง** ให้จดค่าตั้งต้นใน step แรก แล้วเทียบ (ระบุไว้ในตารางแล้ว).
6. เคส `(ต้อง simulate)` (TC-17b demoPay, TC-CC-01, TC-ID-01, TC-FU-01 big file, TC-CA-01) — ถ้า prototype ทำไม่ได้ ให้ mark **blocked** พร้อม evidence.
7. บันทึกผลตาม `Result Report (schema)` ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST) | 24 / 24 |
| Business Rules (BR-01..17) | 17 / 17 |
| Status guards / transitions (§5.2) | 11 / 11 |
| Error codes (§5.6) | 17 / 19 |
| Field validation (§5.4) | 11 / 11 |
| Permission cells (§5.3 สำคัญ) | 7 / 7 |
| Edge cases (§5.5) | 12 / 12 |
| Cross-Module (XT-01..07) | 7 / 7 |
| Scope Lock (LOCK-01..10) | 10 / 10 |

- **FN cross-check: ✅ 24/24** (FN-01..21 + FN-90/91/92 · รวม FN-20 vendor credit + FN-21 vendorCn input-VAT reversal ที่ต่างจาก CN)
- **Cross-Module (XT): 7/7** (เพิ่ม XT-07 vendorCredit จาก CN)
- **Scope Lock (LOCK): 10/10** (LOCK-02→TC-S03/S01 · LOCK-03→TC-R05 · LOCK-04→TC-09/17/20a · LOCK-05→TC-11c · LOCK-07→TC-18/21a/X02 · LOCK-08→TC-X03/X06 อื่น ๆ มีเคส verify เฉพาะ)
- **Manifest cross-check (FRD §0.12): ✅ 24/24** — ทุกแถว FN Coverage Manifest มีคู่ใน Ledger + เคส.

### ข้าม (พร้อมเหตุผล)
- **ERR_VALIDATION_FAILED / ERR_NOT_AUTHENTICATED / ERR_INSUFFICIENT_ROLE / ERR_NOT_FOUND (400/401/403/404 generic):** ข้าม — auth/infra layer ไม่สังเกตได้บน prototype UI (ทดสอบระดับ API). นับ error catalog 17/19 (BR_* + ERR_NOT_CURRENT_APPROVER + concurrency/idempotency ครอบ; generic auth = API test).
- **หน้าจอคืนสินค้า RTV จริง (W3-LITE mock):** ข้าม — นอกขอบเขต — ตรวจเฉพาะการผูก RTV ที่ฝั่ง DN (TC-R01/R03/X06).
- **หน้า AP / VAT Report / JE / Vendor Credit flow จริง (F-ACC-APINV/F105/F093/F097 use):** ข้าม module ปลายทาง — prototype ไม่มีหน้าจริง → ตรวจผลผ่าน ref tab / stat tile / credit card ฝั่ง DN (TC-X01/X02/X03/X07).
- **ลดหนี้ไม่อ้างใบ / refund / ยกเลิกหลังอนุมัติ:** นอกขอบเขต (Exclusions) — ทดสอบว่า **ปิด/ไม่รองรับ** (TC-S03/14a, TC-NEG-03, TC-NEG-05/X05) ไม่ทดสอบให้ทำได้.
- **flow ใช้/ตัดยอดเครดิตคงเหลือกับผู้ขาย (OQ-DN-06):** display-only รอบนี้ — ทดสอบว่าเป็น display-only (TC-20b) ไม่ทดสอบ flow ใช้ยอด.
- **DEMO artifacts (persona switcher/demoPay/.demo-only):** เป็น harness ทดสอบ — ใช้ตั้ง role/simulate เท่านั้น (prod strip). ไม่มีเคสยืนยัน "ต้องมีบนจอ prod".

---

## Result Report (schema)

```json
{
  "feature_id": "F-ACC-DN",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 102, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent เห็นจริงตอน fail/blocked (ข้อความ error จริง · route ที่ค้าง · ค่าที่แสดงแทน Expected). `note` = หมายเหตุเสริม เช่น `(ต้อง simulate)` ทำไม่ได้บน prototype.
