# 05_RULES — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machine + Permission + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด · ทุก rule trace กลับ FN/HTML

---

## §5.1 Business Rules (BR)

### BR-01: เลือกใบตั้งหนี้ได้เฉพาะ approved/posted ที่ dnRoom>0
- **Statement:** picker แสดงเฉพาะใบ **approved/posted และ dnRoom>0** (ใบที่ลดเต็มมูลค่าแล้วไม่โผล่ · **ใบจ่ายครบยังโผล่** ถ้า dnRoom>0 — คืนของหลังจ่าย)
- **Enforced by:** API-11 + FN-04 · ENG ap-open-item (`invList()` filter `dnRoom>0.005`) · **Type:** Prevent (FIXED) · **FN:** FN-01, FN-04 · **LOCK-04**

### BR-02: ยอด DN สุทธิ ≤ dnRoom ใบอ้างอิง (ตรวจ 2 จังหวะ)
- **Statement:** ตอนส่ง (grand ≤ **dnRoom**) และตอน**อนุมัติขั้นสุดท้าย** (grand ≤ **dnRoom** re-check)
- **Enforced by:** FN-05 submitGuard + FN-07 approveGuard · ENG ap-open-item (`dnOver`) · **Type:** Error/Prevent (FIXED) · **FN:** FN-09, FN-17 · **LOCK-04**
- **Note:** draft ที่เกิน dnRoom **บันทึกร่างได้** แต่ส่งอนุมัติไม่ได้ (blockReason "ยอดลดหนี้เกินมูลค่าที่ลดได้ (บันทึกร่างได้)" vs submitGuard)

### BR-03: จำนวนลดต่อบรรทัด ≤ (จำนวนใบเดิม − ลดแล้วทุกใบรวมกัน)
- **Statement:** qty ≤ qtyLeft (mode qty) · line net ≤ netLeft. credited นับข้ามทุกใบ ยกเว้น cancelled
- **Enforced by:** FN-05 + FN-14 (lineRoom) · `extraLineValidate`/`lineOver`/`overMsg` · **Type:** Error (FIXED) · **FN:** FN-07, FN-08

### BR-04: ราคาลดต่อหน่วย ≤ ราคาเดิม (mode price)
- **Statement:** OVERPRICE — unit_price ≤ orig_price (`extraLineValidate` block) · **Type:** Error (FIXED) · **FN:** FN-06

### BR-05: เหตุผลจาก master + คำอธิบาย ≥ 10 ตัวอักษร
- **Statement:** reason ∈ master · reason_text.trim().length ≥ 10
- **Type:** Error (FIXED ข้อความ) / CONFIGURABLE (master รายการเหตุผล) · **FN:** FN-05, FN-10

### BR-06: เหตุผล "คืนของ" (RTV) ต้องอ้างใบคืนสินค้าของใบเดียวกัน · จำนวนไม่เกินที่คืน
- **Statement:** reason.need_rtv=true → ต้องเลือก RTV ของ inv เดียวกัน · line.max = min(qtyLeft, RTV.qty) (`pickRTV` cap)
- **Type:** Error (FIXED · [ASSUMED contract W3-LITE mock]) · **FN:** FN-05

### BR-07: DOA resolve ตามมูลค่า ณ กดส่ง (freeze) · ผู้ขอไม่อนุมัติเอง (SoD)
- **Statement:** resolveDoa ตาม `grand` (ยอดสุทธิหลัง end-bill — **LD-05**) → snapshot chain freeze · **canActStep:** submitted_by === actor ⇒ ไม่มีสิทธิ์ (ซ่อนปุ่มอนุมัติ)
- **Type:** Trigger/Prevent (CONFIGURABLE ผ่าน DOA กลาง) · **FN:** FN-11, FN-14 · **LOCK-05**

### BR-08: เลข DN ออกเมื่ออนุมัติครบสาย (no-gap running number)
- **Statement:** `code = ENG-DOC-NUM.next('DN')` (`nextCode()` · `DOC.prefix='DN'`) ตอน final approve เท่านั้น — ไม่ออกตอน draft/ส่งอนุมัติ (DOCCFG Iron 4)
- **Type:** Trigger (CONFIGURABLE doccfg) · **FN:** FN-12 · **LOCK-06**

### BR-09: อนุมัติครบ → dn_applied ใบเดิม + JE (จำลอง)
- **Statement:** ap_open_item.dn_applied += applyToAp · JE: **Dr 2110 เจ้าหนี้ = applyToAp** · **Cr 5xxx รับคืน/ส่วนลด = netBefore** · **Cr 1150 ภาษีซื้อ = netVat** · input_vat_line negative = netVat (⚠️ ลง ภ.พ.30 เมื่อมี vendorCn — ดู BR-14)
- **Type:** Trigger (FIXED logic) · **FN:** FN-11, FN-18

### BR-10: ร่าง/รออนุมัติกันยอด (dn_held) ชั่วคราว
- **Statement:** dnRoom = invGrand − dn_applied − dn_held(draft/pending). ยกเลิก → คืน held
- **Type:** Trigger (FIXED) · **FN:** FN-08

### ⭐ BR-11: ส่วนลดท้ายบิล — เพดาน ยอดสุทธิ ≥0 และ ≤ dnRoom  (FN-19)
- **Statement:** end-bill (฿ หรือ %) หักเพิ่มจากยอดรวม. **เพดาน ebCap = max(0, after − couponAmt)** — เกิน (`ebOver = ebRaw > ebCap + 0.005`) → **บล็อก submit + เตือนสูงสุด** ("ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)"). grand ต้อง ≥0. รวมกับ BR-02/dnOver → net ≤ dnRoom
- **Enforced by:** ENG dn-totals (ebOver) → FN-05 blockReason/submitGuard · **Type:** Error/Prevent (CONFIGURABLE เพดาน% Admin) · **FN:** FN-19 · **[BA 2026-09-23]**

### ⭐ BR-12: ส่วนลดท้ายบิลลดฐานภาษี → input VAT คำนวณใหม่ตามสัดส่วน (ม.86/10)  (FN-19)
- **Statement:** `ebVat = ebAmt × (vat/after)` (แบ่งตามสัดส่วน VAT ในยอดรวม — รองรับหลายอัตรา/VAT-inclusive) · `ebBase = ebAmt − ebVat` · **netBefore = before − ebBase** · **netVat = vat − ebVat**. ภ.พ.30 + JE + PDF สะท้อน netVat (**ภาษีซื้อที่ลดจริง**)
- **Enforced by:** ENG dn-totals (verbatim `totals()`) · **Type:** Trigger (FIXED logic) · **FN:** FN-19 · **[BA 2026-09-23 · legal basis ฝั่งซื้อรอ BA รับรอง OQ-DN-05]**

### ⭐ BR-13: เพดานลดหนี้ = dnRoom (ไม่หัก paid) · vendor credit split  (FN-04/FN-20)
- **Statement:** `dnRoom = invGrand − ลดหนี้แล้ว(approved/sent) − กันยอด(draft/pending)` **ไม่หัก paid** → **ใบจ่ายครบยังออก DN ได้** (คืนของหลังจ่าย) · `dnSplit(grand)`: `applyToAp = min(grand, outstanding)` (หักจากหนี้ค้าง) · `vendorCredit = max(0, grand − applyToAp)` (**เครดิตคงเหลือกับผู้ขาย**) · ใบที่ลดเต็มมูลค่าแล้ว (dnRoom=0) ไม่โผล่
- **Enforced by:** ENG ap-open-item (dnRoom/dnSplit) · FN-11 (set apply_to_ap/vendor_credit) · FN-17 (buildVendorCreditLedger display) · **Type:** Trigger/Prevent (FIXED logic) · **FN:** FN-04, FN-20 · **[BA FIX-01 2026-09-23]** · **LOCK-04 (ปรับความหมาย)**
- **Note:** vendor credit = **display-only** รอบนี้ · flow ใช้/ตัดยอด = OQ-DN-06

### ⭐ BR-14: กลับภาษีซื้อ (ภ.พ.30) gated by vendorCn (ม.82/10)  (FN-21)
- **Statement:** input_vat_line (negative = netVat) ลง ภ.พ.30 **ได้เมื่อมีเลขที่+วันที่ใบลดหนี้จากผู้ขาย (vendorCn)** · **เดือนภาษี = เดือนของ vendorCnDate** · ไม่มี vendorCn → note.warn **"รอใบลดหนี้ผู้ขาย"** (ลด AP ได้แต่ยังไม่ลดภาษีซื้อ) · ปุ่มบันทึกภายหลัง (`openVendorCn`) บนใบ approved/sent
- **Enforced by:** FN-16 recordVendorCn (API-16) · DB CHECK (input_vat_applied ⇒ vendor_cn NOT NULL) · **Type:** Trigger/Prevent (FIXED logic) · **FN:** FN-21 · **[BA FIX-02 2026-09-23 · ยืนยัน OQ-DN-05]** · **LOCK-07**
- **Edge CA-01:** vendorCn ซ้ำ / เดือนภาษีปิดงวด → **ยก OQ** (flag warn, ไม่ block รอบนี้)

### BR-15: ประวัติ append-only · ไม่มี hard delete · วันที่ ค.ศ.
- **Statement:** ทุกการกระทำ → T_dn_audit (`pushAudit` insert/unshift-only). ยกเลิก = status cancelled (ไม่ลบ). approval_history append-only. date = ค.ศ. (`formatThaiDate`)
- **Type:** Trigger (FIXED) · **FN:** FN-91 · **LOCK-10**

### BR-16: ลดหนี้ไม่อ้างใบ = ปิด (tile "ปิดไว้")
- **Statement:** tile "ลดหนี้ไม่อ้างใบ" disabled (`cursor:not-allowed`) — คลิก → toast · ไม่ผูก `setSource`. ต้องอ้าง inv เสมอ
- **Type:** Prevent (FIXED) · **FN:** FN-02 · **OQ-DN-01**

### BR-17: เหตุผลแต่ละตัวพก `legal_basis` (ม.86/10 ฝั่งซื้อ)
- **Statement:** แต่ละ reason มี legal_basis. legal_basis พิมพ์ลง PDF (FN-92). **legal basis ฝั่งซื้อ = [ASSUMED mirror CN]** รอ BA รับรอง (OQ-DN-05)
- **Type:** Warning (CONFIGURABLE master) · **OQ-DN-05**
- **legal_basis (จาก master seed [ASSUMED]):** RTV="รับคืนสินค้า/คืนของให้ผู้ขาย" · OVERPRICE="ผู้ขายคำนวณราคาสูงกว่าที่ตกลง/ผิดราคา" · SHORT="จัดส่งสินค้าขาดจำนวน/ไม่ครบตามใบกำกับ"

### DOA Tier Matrix (BR-07 · entry `DOA-ACC-DN` sequential · คิดจาก `grand` หลัง end-bill — LD-05)
| Tier | ช่วง (ยอดสุทธิ grand) | สายอนุมัติ |
|:--:|---|---|
| 1 | 0 – 50,000 | ผจก.จัดซื้อ |
| 2 | 50,000.01 – 300,000 | ผจก.จัดซื้อ → ผจก.บัญชี |
| 3 | > 300,000 | ผจก.จัดซื้อ → ผจก.บัญชี → CFO |
> ช่วง 50k/300k = **[ASSUMED — mirror CN]** รอ `DOA-ACC-DN` ยืนยัน (OQ-AP-06).

---

## §5.2 State Machine (has-state)

```
        A-02 save        A-04 submit          A-05 approve(ครบสาย)      A-07 send
   (—) ─────────▶ draft ──────────▶ pending_approval ──────────────▶ approved ──────────▶ sent
                    ▲                    │                              │  │
                    │ A-06 reject(เหตุผล) │                              │  │ (display-only / vendorCn)
                    └────────────────────┘                              └──┴─▶ ออกเอกสารแก้ไข · บันทึก vendorCn (ไม่เปลี่ยน state)
        draft/pending ──── A-08 cancel(เหตุผล) ────▶ cancelled
```

| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| — | draft | create/save | officer-ap | — |
| draft | pending_approval | submit | officer-ap (owner) | !ebOver · grand ≤ dnRoom · reason_text≥10 · slot ครบ (BR-11,02,05,07) |
| pending_approval | approved | approve (ครบสาย) | approver ขั้นสุดท้าย | re-check grand ≤ dnRoom → ออกเลข DN + dnSplit (BR-02,08,13) |
| pending_approval | draft | reject | approver (current step) | reason required · append history |
| draft/pending_approval | cancelled | cancel | officer-ap (owner) | reason required · คืน held |
| approved | sent | send | officer-ap | — (sent→resend, ไม่เปลี่ยน state) |
| approved/sent | (คงเดิม) | บันทึก vendorCn | officer-ap / mgr-acc | กลับภาษีซื้อเดือน vendorCnDate (BR-14) |
| approved/sent | (คงเดิม) | ~~ออกเอกสารแก้ไข~~ | officer-ap | ⚠️ **forward — ไม่มีใน prototype v1** · display-only · ไม่ถอนยอด (OQ-DN-04 · D-3) |

> **Status guards (จาก HTML — บังคับที่ 03_LOGIC + API precondition):**
> - **cancel** เฉพาะ draft/pending_approval (double-guard `openCancelDN`) — อื่น → verbatim HTML: "ยกเลิกได้เฉพาะฉบับร่าง / รออนุมัติ — ใบที่อนุมัติแล้วยกเลิกไม่ได้ (OQ-DN-04)"
> - **send** เฉพาะ approved (sent = ส่งสำเนาซ้ำ) — อื่น → "ต้องอนุมัติครบก่อนส่ง"
> - **submit** เฉพาะ draft — อื่น → "ส่งอนุมัติได้เฉพาะฉบับร่าง"
> - **edit** เฉพาะ draft — อื่น → "แก้ไขได้เฉพาะฉบับร่าง"
> - **vendorCn** เฉพาะ approved/sent (บันทึกได้แม้ locked แก้ไข)
> - **approved/sent = locked** แก้ไขไม่ได้ (`lockedStatuses:['approved','sent']`) ยกเว้น vendorCn

---

## §5.3 Permission Matrix (SoD)

| Role | View | Create | Edit(draft) | Submit | Approve/Reject | Cancel(draft/pending) | Send | vendorCn |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| เจ้าหน้าที่เจ้าหนี้ (officer-ap) | ✅ | ✅ | own | ✅ | — | ✅ | ✅ | ✅ |
| ผจก.จัดซื้อ (mgr-purchase) | ✅ | — | — | — | ✅ ขั้น 1 | — | — | — |
| ผจก.บัญชี (mgr-acc) | ✅ | — | — | — | ✅ ขั้น 2 (tier2+) | — | — | ✅ |
| CFO (cfo) | ✅ | — | — | — | ✅ ขั้น 3 (tier3) | — | — | — |

> **SoD (BR-07 · FN-14):** `canActStep` = ต้องเป็นผู้มีสิทธิ์ขั้นปัจจุบัน (assignee ตรง หรือ role ตรง) **และ** `submittedBy !== ME`. ผู้ส่งเห็นได้แค่ "ยกเลิก" ตอน pending. role-ids [ASSUMED] (OQ-AP-06).

---

## §5.4 Field Validation Rules

| Field | Rule | Error code |
|---|---|---|
| inv | required · approved/posted · dnRoom>0 | BR_INVALID_INVOICE |
| dn_date | required · ≥ ap_invoice.vdate | BR_DN_DATE_BEFORE_INVOICE ("ต้องไม่ก่อนวันที่ใบกำกับเดิม") |
| reason | required · ∈ master | BR_REASON_REQUIRED ("เลือกเหตุผล") |
| rtv | required เมื่อ reason=RTV · ของใบเดียวกัน | BR_RTV_NEEDS_RTV ("เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า" / "เลือกใบคืนสินค้าของใบตั้งหนี้นี้") |
| reason_text | required · ≥10 | BR_REASON_TEXT_TOO_SHORT ("ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร") |
| line.qty | ≤ qtyLeft (และ ≤ RTV qty ถ้า RTV) | BR_LINE_QTY_EXCEEDED |
| line.unit_price | ≤ orig_price (mode price) | BR_PRICE_EXCEEDS_ORIG |
| line net | ≤ netLeft | BR_LINE_NET_EXCEEDED |
| endbill | !ebOver (≤ ebCap) | BR_ENDBILL_EXCEEDS_CAP |
| grand (submit) | ≤ dnRoom | BR_DN_EXCEEDS_ROOM |
| vendor_cn / vendor_cn_date | ทั้งคู่ต้องมีก่อนกลับภาษีซื้อ | (gate — ไม่มี = "รอเอกสาร") |

**Cross-field:** grand = max(0, after − ebAmt − couponAmt) · netVat = vat − ebVat · applyToAp = min(grand, outstanding) · vendorCredit = max(0, grand − applyToAp) · dnRoom = invGrand − dn_applied − dn_held (ไม่หัก paid) — คำนวณ ENG dn-totals/ap-open-item

---

## §5.5 Edge Cases (BRD §10.1 confirmed + Phase 2.5 probes)

### EC-01: ใบเดิมถูกลดหนี้เพิ่มระหว่างรออนุมัติ (EDGE-01 · S-11 · FN-17)
- **Scenario:** dnRoom ลดลงหลัง submit ก่อน approve ขั้นสุดท้าย (ใบอื่น approved เพิ่ม)
- **Resolution:** approveGuard re-check grand ≤ dnRoom — ไม่พอ → block "อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ {inv} เหลือ ฿Y น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้"
- **Note:** การจ่ายเงินไม่กระทบเพดานอีกต่อไป (dnRoom ไม่หัก paid) · **Test:** AT-17 (DEMO harness `demoPay`)

### EC-02: ลดหลายรอบบนใบเดียว (EDGE-02 · S-04) → บรรทัดแสดง จำนวนเดิม/ลดแล้ว/ลดได้อีก ถูกต้อง (dn_applied + dn_held) · **Test:** AT-08
### EC-03: ใบตั้งหนี้จ่ายครบ (EDGE-03 · S-13) → **ยังออก DN ได้** (dnRoom ไม่หัก paid) · ส่วนเกินคงค้าง = vendorCredit · **Test:** AT-20
### EC-04: ใบที่ลดเต็มมูลค่าแล้ว (EDGE-04) → dnRoom=0 → ไม่โผล่ใน picker · **Test:** AT-13
### EC-05: ยกเลิก draft/pending (EDGE-05 · S-09) → คืนยอด held · **Test:** AT-15
### EC-06: ไม่อนุมัติ (EDGE-06 · S-07) → approval_history + badge "ถูกตีกลับ N ครั้ง" · **Test:** AT-13b
### EC-07: ยังไม่ได้รับใบลดหนี้จากผู้ขาย (EDGE-07 · FN-21) → ภ.พ.30 "รอเอกสาร" (ลด AP แล้วแต่ยังไม่ลดภาษีซื้อ) · **Test:** AT-21

### EC-CC-01: Concurrent approval 2 คนขั้นเดียว (PR-1 · `[AI-DEFAULT]`)
- **Resolution:** optimistic lock `version` — first commit wins, second 409 ERR_STALE_DATA · **Test:** TC-CC-01 · **OQ:** OQ-CC-01
### EC-ID-01: double-submit (PR-7 · busyGate) → Idempotency-Key, cached response · **Test:** TC-ID-01
### EC-CALC-01: ปัดเศษ ebVat แบ่งตามสัดส่วน (PR-calc · `[AI-DEFAULT]`) → ปัด 2 ตำแหน่งตาม HTML `totals()` · **OQ:** OQ-EB-01
### EC-FU-01: ชนิด/ขนาดไฟล์แนบ (`[AI-DEFAULT]`) → jpg/png/pdf ≤10MB · **OQ:** OQ-FU-01
### EC-CA-01: vendorCn กรอกซ้ำ / เดือนภาษีปิดงวดแล้ว (⚠️ กระทบภาษี) → **OQ ทันที** (flag warn) · **OQ:** CA-01

---

## §5.6 Error Catalog

| Code | HTTP | Message (verbatim/i18n) | Cause |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | "กรุณากรอกข้อมูลให้ครบถ้วน" | generic |
| ERR_NOT_AUTHENTICATED | 401 | error.auth.unauth | no token |
| ERR_INSUFFICIENT_ROLE | 403 | error.auth.role | role mismatch |
| ERR_NOT_CURRENT_APPROVER | 403 | "ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน" | SoD/step (BR-07) |
| ERR_NOT_FOUND | 404 | error.notfound | missing |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | error.idempotency.dup | same key diff body |
| ERR_STALE_DATA | 409 | error.concurrency.stale | version mismatch (EC-CC-01) |
| BR_DN_EXCEEDS_ROOM | 422 | "ยอดลดหนี้เกินมูลค่าที่ลดได้ของใบตั้งหนี้ (ลดได้ ฿X) — แก้ไขร่างก่อน" | BR-02/BR-13 |
| BR_APPROVE_EXCEEDS_ROOM | 422 | "อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ {inv} เหลือ ฿Y น้อยกว่ายอดลดหนี้ (มีใบลดหนี้อื่นได้รับอนุมัติเพิ่มระหว่างรออนุมัติ) · ให้ไม่อนุมัติกลับไปแก้" | BR-02 (last step) |
| BR_ENDBILL_EXCEEDS_CAP | 422 | "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)" | BR-11 |
| BR_LINE_QTY_EXCEEDED | 422 | "จำนวนลดเกินที่ลดได้: {item} (ลดได้อีก N)" | BR-03 |
| BR_PRICE_EXCEEDS_ORIG | 422 | "ราคาลดต่อหน่วยเกินราคาเดิม: {item}" | BR-04 |
| BR_LINE_NET_EXCEEDED | 422 | "มูลค่าลดเกินมูลค่าที่ลดได้ของบรรทัด: {item}" | BR-03 |
| BR_REASON_TEXT_TOO_SHORT | 422 | "ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร" | BR-05 |
| BR_RTV_NEEDS_RTV | 422 | "เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า" | BR-06 |
| BR_SUBMIT_DRAFT_ONLY | 422 | "ส่งอนุมัติได้เฉพาะฉบับร่าง" | §5.2 |
| BR_EDIT_DRAFT_ONLY | 422 | "แก้ไขได้เฉพาะฉบับร่าง" | §5.2 |
| BR_CANCEL_STATE_INVALID | 422 | "ยกเลิกได้เฉพาะฉบับร่าง / รออนุมัติ — ใบที่อนุมัติแล้วยกเลิกไม่ได้ (OQ-DN-04)" | §5.2 (verbatim HTML) |
| BR_SEND_STATE_INVALID | 422 | "ต้องอนุมัติครบก่อนส่ง" | §5.2 |
| BR_VENDORCN_STATE_INVALID | 422 | "บันทึกใบลดหนี้ผู้ขายได้เฉพาะใบที่อนุมัติแล้ว" | BR-14 / §5.2 |
| BR_SLOT_INCOMPLETE | 422 | "เลือกผู้อนุมัติให้ครบทุกขั้น" | BR-07 |
| BR_REASON_REQUIRED | 422 | (reject/cancel reason ว่าง) | §5.2 |

---

## §5.7 Security Bible Application
> Domains: **D2, D5, D7, D9, D15, D17**

### D2 Auth: JWT ทุก endpoint · role-based · DOA slot binding per step
### D5 Financial: ทุก amount change → audit (before/after) · approval-by-value (DOA 3-tier) · reconciliation (netVat รายเดือน ภ.พ.30 · เฉพาะที่มี vendorCn) · **amount ceiling BR-02/BR-13 (dnRoom) ทั้งส่ง+อนุมัติ** · input-VAT reversal gated (BR-14)
### D7 PII/PDPA: vendor name/taxId/billTo/rep encrypt at rest · บุคคลธรรมดา taxId → mask ใน CSQ payload · logs ใช้ ID ref
### D-CLASS (Data Classification):
| Layer | Confidential fields (amount/vendor PII/reason_text/vendorCn/applyToAp/vendorCredit) |
|---|---|
| API response | mask ถ้า role ไม่ผ่าน |
| UI | แสดง `***` |
| Export/Print | excluded ถ้า role ไม่ผ่าน |
| Audit | log view + mutation |
> ไม่มี field ระดับ Restricted → ไม่ต้อง wire Restricted Resources. Wire: Policy Center → Data Classification.
### D9 Audit: ทุก mutation → T_dn_audit (append-only, 7 ปี, immutable) · no hard delete (BR-15)
### D15 Admin/Approval: ทุก transition logged · approver identity + timestamp · reason บังคับ reject/cancel · vendorCn บันทึก by/at
### D17 Multi-tenant: PostgreSQL RLS (scope company) · X-Tenant-Id middleware · cross-tenant forbidden

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| ม.86/10 (ออกใบลดหนี้อ้างใบกำกับเดิม) | BR-06/BR-08/BR-12/BR-17 · PDF อ้างเลข+วันที่ใบกำกับเดิม+เดิม/ถูกต้อง/ผลต่าง/เหตุผล (FN-92) |
| ม.82/10 (เดือนภาษี ฝั่งซื้อ) | input VAT ลง ภ.พ.30 เดือน **vendorCnDate** — gated by vendorCn (BR-14) · **[ASSUMED mirror CN — OQ-DN-05]** |
| COSO Maker/Checker/Approver + SoD | BR-07 · §5.3 |
| PDPA | D7 · mask · retention |
| Audit trail | T_dn_audit append-only |
