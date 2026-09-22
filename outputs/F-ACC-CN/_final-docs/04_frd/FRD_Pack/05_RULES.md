# 05_RULES — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machine + Permission + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด · ทุก rule trace กลับ FN/HTML

---

## §5.1 Business Rules (BR)

### BR-01: เลือกใบแจ้งหนี้ได้เฉพาะ issued/sent ที่ outstanding>0
- **Statement:** picker แสดงเฉพาะใบ **ไม่ void และ outstanding>0** (void/ชำระครบ ไม่โผล่)
- **Enforced by:** API-11 + FN-04 · ENG ar-open-item · **Type:** Prevent (FIXED) · **FN:** FN-01, FN-04

### BR-02: ยอด CN สุทธิ ≤ outstanding ใบอ้างอิง (ตรวจ 2 จังหวะ)
- **Statement:** ตอนส่ง (grand ≤ **available** = outstanding − held) และตอน**อนุมัติขั้นสุดท้าย** (grand ≤ **outstanding** re-check)
- **Enforced by:** FN-05 submitGuard + FN-07 approveGuard · **Type:** Error/Prevent (FIXED) · **FN:** FN-09, FN-17 · **LOCK-04**
- **Note:** draft ที่เกิน available **บันทึกร่างได้** แต่ส่งอนุมัติไม่ได้ (ยึด HTML blockReason vs submitGuard)

### BR-03: จำนวนลดต่อบรรทัด ≤ (จำนวนใบเดิม − ลดแล้วทุกใบรวมกัน)
- **Statement:** qty ≤ qtyLeft (mode qty) · line net ≤ netLeft. credited นับข้ามทุกใบ ยกเว้น cancelled
- **Enforced by:** FN-05 + FN-14 (lineRoom) · **Type:** Error (FIXED) · **FN:** FN-07, FN-08

### BR-04: ราคาลดต่อหน่วย ≤ ราคาเดิม (mode price)
- **Statement:** DISC/PRICE — unit_price ≤ orig_price · **Type:** Error (FIXED) · **FN:** FN-06

### BR-05: เหตุผลจาก master + คำอธิบาย ≥ 10 ตัวอักษร
- **Statement:** reason ∈ master · reason_text.trim().length ≥ 10
- **Type:** Error (FIXED ข้อความ) / CONFIGURABLE (master รายการเหตุผล) · **FN:** FN-05, FN-10

### BR-06: เหตุผล "รับคืน" (RET) ต้องอ้างใบรับคืนของใบเดียวกัน · จำนวนไม่เกินที่รับคืน
- **Statement:** reason.need_sr=true → ต้องเลือก SR ของ ref_invoice เดียวกัน · line.max = min(qtyLeft, SR.qty)
- **Type:** Error (FIXED · [ASSUMED contract F090 mock]) · **FN:** FN-05

### BR-07: DOA resolve ตามมูลค่า ณ กดส่ง (freeze) · ผู้ขอไม่อนุมัติเอง (SoD)
- **Statement:** resolveDoa ตาม `grand` (ยอดสุทธิหลัง end-bill — **LD-05**) → snapshot chain freeze · **canActStep:** submitted_by === actor ⇒ ไม่มีสิทธิ์ (ซ่อนปุ่มอนุมัติ)
- **Type:** Trigger/Prevent (CONFIGURABLE ผ่าน DOA กลาง) · **FN:** FN-06, FN-07 · **LOCK-05**

### BR-08: เลข CN ออกเมื่ออนุมัติครบสาย (no-gap running number)
- **Statement:** `code = ENG-DOC-NUM.next('CN')` ตอน final approve เท่านั้น — ไม่ออกตอน draft/ส่งอนุมัติ (DOCCFG Iron 4)
- **Type:** Trigger (CONFIGURABLE doccfg) · **FN:** FN-11 · **LOCK-06**

### BR-09: อนุมัติครบ → cn_applied ใบเดิม + JE (จำลอง) + ลดภาษีขายเดือนที่ออก
- **Statement:** ar_open_item.cn_applied += grand · JE: Dr 4110 รับคืน/ลดรายได้ (RET/QTY) หรือ 4120 ส่วนลดจ่าย (DISC/PRICE) = netBefore · Dr 2150 ภาษีขาย = netVat · Cr 1130 ลูกหนี้ = grand · output_vat_line negative = netVat เดือน cnDate
- **Type:** Trigger (FIXED logic) · **FN:** FN-11, FN-18

### BR-10: ร่าง/รออนุมัติกันยอด (cn_held) ชั่วคราว
- **Statement:** available = outstanding − cn_held(draft/pending). ยกเลิก → คืน held
- **Type:** Trigger (FIXED) · **FN:** FN-08

### ⭐ BR-11: ส่วนลดท้ายบิล — เพดาน ยอดสุทธิ ≥0 และ ≤ ยอดคงค้าง  (FN-19)
- **Statement:** end-bill (฿ หรือ %) หักเพิ่มจากยอดรวม. **เพดาน ebCap = max(0, after − coupon)** — เกิน (`ebOver = ebRaw > ebCap + 0.005`) → **บล็อก submit + เตือนสูงสุด** ("ยอดสุทธิห้ามติดลบ"). grand ต้อง ≥0. รวมกับ BR-02 → net ≤ outstanding
- **Enforced by:** ENG cn-totals (ebOver) → FN-05 blockReason/submitGuard · **Type:** Error/Prevent (CONFIGURABLE เพดาน% Admin) · **FN:** FN-19 · **[BA 2026-09-22]**

### ⭐ BR-12: ส่วนลดท้ายบิลลดฐานภาษี → VAT คำนวณใหม่ตามสัดส่วน (ม.86/10)  (FN-19)
- **Statement:** `ebVat = ebAmt × (vat/after)` (แบ่งตามสัดส่วน VAT ในยอดรวม — รองรับหลายอัตรา/VAT-inclusive) · `ebBase = ebAmt − ebVat` · **netBefore = before − ebBase** · **netVat = vat − ebVat**. ภ.พ.30 + JE + PDF สะท้อน netVat (ภาษีขายที่ลดจริง)
- **Enforced by:** ENG cn-totals (verbatim `totals()`) · **Type:** Trigger (FIXED logic) · **FN:** FN-19 · **[BA 2026-09-22]**

### BR-13: ประวัติ append-only · ไม่มี hard delete · วันที่ ค.ศ.
- **Statement:** ทุกการกระทำ → T_cn_audit (insert-only). ยกเลิก = status cancelled (ไม่ลบ). approval_history append-only. date = ค.ศ.
- **Type:** Trigger (FIXED) · **FN:** FN-91 · **LOCK-10**

### BR-14: ลดหนี้ไม่อ้างใบ = ปิด (tile "ปิดไว้")
- **Statement:** tile "ลดหนี้ไม่อ้างใบ" disabled (`cursor:not-allowed`) — คลิก → toast "ลดหนี้ไม่อ้างใบแจ้งหนี้ถูกปิดไว้ (OQ-CN-01)". ต้องอ้าง ref_invoice เสมอ
- **Type:** Prevent (FIXED) · **FN:** FN-02 · **OQ-CN-01**

### BR-15: เหตุผลแต่ละตัวพก `legal_basis` (ม.86/10) · DISC มี trade_discount_warn
- **Statement:** แต่ละ reason มี legal_basis (ประกาศอธิบดีฯ / ม.86/10). DISC → แสดงเตือน "ส่วนลดทางการค้าล้วนไม่ใช่เหตุออกใบลดหนี้ภาษี (รอเคาะ OQ-CN-01)". legal_basis พิมพ์ลง PDF (FN-92)
- **Type:** Warning (CONFIGURABLE master) · **OQ-CN-01**
- **legal_basis (จาก master seed):** RET="รับคืนสินค้า/ยกเลิกบริการ" · DISC="ลดราคาเพราะสินค้าผิดข้อกำหนด/ชำรุด" (+warn) · PRICE="คำนวณราคาสินค้าผิดพลาดสูงกว่าที่เป็นจริง" · QTY="จัดส่งสินค้าขาดจำนวน/คิดเกินที่ส่งจริง"

### DOA Tier Matrix (BR-07 · entry `DOA-ACC-CN` sequential · คิดจาก `grand` หลัง end-bill — LD-05)
| Tier | ช่วง (ยอดสุทธิ grand) | สายอนุมัติ |
|:--:|---|---|
| 1 | 0 – 50,000 | ผจก.ขาย |
| 2 | 50,000.01 – 300,000 | ผจก.ขาย → ผจก.บัญชี |
| 3 | > 300,000 | ผจก.ขาย → ผจก.บัญชี → CFO |

---

## §5.2 State Machine (has-state)

```
        A-02 save        A-05 submit          A-06 approve(ครบสาย)      A-09 send
   (—) ─────────▶ draft ──────────▶ pending_approval ──────────────▶ approved ──────────▶ sent
                    ▲                    │                              │  │
                    │ A-07 reject(เหตุผล) │                              │  │ (display-only)
                    └────────────────────┘                              └──┴─▶ ออกเอกสารแก้ไข (ไม่เปลี่ยน state)
        draft/pending ──── A-08 cancel(เหตุผล) ────▶ cancelled
```

| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| — | draft | create/save | officer-ar | — |
| draft | pending_approval | submit | officer-ar (owner) | !ebOver · grand ≤ available · reason_text≥10 · slot ครบ (BR-11,02,05,07) |
| pending_approval | approved | approve (ครบสาย) | approver ขั้นสุดท้าย | re-check grand ≤ outstanding → ออกเลข CN (BR-02,08) |
| pending_approval | draft | reject | approver (current step) | reason required · append history |
| draft/pending_approval | cancelled | cancel | officer-ar (owner) | reason required · คืน held |
| approved | sent | send | officer-ar | — (sent→resend, ไม่เปลี่ยน state) |
| approved/sent | (คงเดิม) | ออกเอกสารแก้ไข | officer-ar | display-only · ไม่ถอนยอด (OQ-CN-02) |

> **Status guards (จาก HTML — บังคับที่ 03_LOGIC + API precondition):**
> - **cancel** เฉพาะ draft/pending_approval — อื่น → "ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ \"ออกเอกสารแก้ไข\""
> - **send** เฉพาะ approved (sent = ส่งสำเนาซ้ำ) — อื่น → "ต้องอนุมัติครบก่อนส่ง"
> - **submit** เฉพาะ draft — อื่น → "ส่งอนุมัติได้เฉพาะฉบับร่าง"
> - **edit** เฉพาะ draft — อื่น → "แก้ไขได้เฉพาะฉบับร่าง"
> - **approved/sent = locked** แก้ไขไม่ได้ (`lockedStatuses:['approved','sent']`)

---

## §5.3 Permission Matrix (SoD)

| Role | View | Create | Edit(draft) | Submit | Approve/Reject | Cancel(draft/pending) | Send |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| เจ้าหน้าที่ลูกหนี้ (officer-ar) | ✅ | ✅ | own | ✅ | — | ✅ | ✅ |
| ผจก.ขาย (mgr-sales) | ✅ | — | — | — | ✅ ขั้น 1 | — | — |
| ผจก.บัญชี (mgr-acc) | ✅ | — | — | — | ✅ ขั้น 2 (tier2+) | — | — |
| CFO (cfo) | ✅ | — | — | — | ✅ ขั้น 3 (tier3) | — | — |

> **SoD (BR-07 · FN-14):** `canActStep` = ต้องเป็นผู้มีสิทธิ์ขั้นปัจจุบัน (assignee ตรง หรือ role ตรง) **และ** `submitted_by !== actor`. ผู้ส่งเห็นได้แค่ "ยกเลิก" ตอน pending. role-ids [ASSUMED] (OQ-AR-06).

---

## §5.4 Field Validation Rules

| Field | Rule | Error code |
|---|---|---|
| ref_invoice | required · issued/sent · outstanding>0 | BR_INVALID_INVOICE |
| cn_date | required · ≥ ref_invoice.date | BR_CN_DATE_BEFORE_INVOICE ("ต้องไม่ก่อนวันที่ใบแจ้งหนี้") |
| reason | required · ∈ master | BR_REASON_REQUIRED ("เลือกเหตุผล") |
| sales_return_ref | required เมื่อ reason=RET · ของใบเดียวกัน | BR_RET_NEEDS_SR ("เลือกใบรับคืนของใบแจ้งหนี้นี้") |
| reason_text | required · ≥10 | BR_REASON_TEXT_TOO_SHORT ("ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร") |
| sales_rep | required | BR_REP_REQUIRED ("ระบุพนักงานขาย") |
| line.qty | ≤ qtyLeft (และ ≤ SR qty ถ้า RET) | BR_LINE_QTY_EXCEEDED |
| line.unit_price | ≤ orig_price (mode price) | BR_PRICE_EXCEEDS_ORIG |
| line net | ≤ netLeft | BR_LINE_NET_EXCEEDED |
| endbill | !ebOver (≤ ebCap) | BR_ENDBILL_EXCEEDS_CAP |
| grand (submit) | ≤ available | BR_CN_EXCEEDS_OUTSTANDING |

**Cross-field:** grand = max(0, after − ebAmt − coupon) · netVat = vat − ebVat · outstanding after = outstanding − grand (คำนวณ ENG cn-totals/ar-open-item)

---

## §5.5 Edge Cases (BRD §10.1 confirmed + Phase 2.5 probes)

### EC-01: ใบเดิมชำระ/ลดเพิ่มระหว่างรออนุมัติ (EDGE-01 · S-11 · FN-17)
- **Scenario:** outstanding ลดลงหลัง submit ก่อน approve ขั้นสุดท้าย
- **Resolution:** approveGuard re-check grand ≤ outstanding — ไม่พอ → block "อนุมัติไม่ได้ — ยอดคงค้าง {inv} เหลือ ฿X น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้"
- **Test:** AT-17 (พิสูจน์ด้วย DEMO harness demoPay ใน prototype)

### EC-02: ลดหลายรอบบนใบเดียว (EDGE-02 · S-04)
- บรรทัดแสดง จำนวนเดิม/ลดแล้ว/ลดได้อีก ถูกต้อง (cn_applied + cn_held) · **Test:** AT-08

### EC-03: ใบเดิม void (EDGE-03 · S-13) → ไม่โผล่ใน picker · CN ร่างที่อ้างไม่ได้ · **Test:** AT-13
### EC-04: ใบชำระครบ (EDGE-04) → ไม่โผล่ (refund ไม่รองรับ LITE) · **Test:** AT-13
### EC-05: ยกเลิก draft/pending (EDGE-05 · S-09) → คืนยอด held · **Test:** AT-15
### EC-06: ไม่อนุมัติ (EDGE-06 · S-07) → approval_history + badge "ถูกตีกลับ N ครั้ง" · **Test:** AT-13b

### EC-CC-01: Concurrent approval 2 คนขั้นเดียว (PR-1 · `[AI-DEFAULT]`)
- **Resolution:** optimistic lock `version` — first commit wins, second 409 ERR_STALE_DATA · **Test:** TC-CC-01 · **OQ:** OQ-CC-01
### EC-ID-01: double-submit (PR-7 · FIX-08 busyGate) → Idempotency-Key, cached response · **Test:** TC-ID-01
### EC-CALC-01: ปัดเศษ ebVat แบ่งตามสัดส่วน (PR-calc · `[AI-DEFAULT]`) → ปัด 2 ตำแหน่งตาม HTML `totals()` · **OQ:** OQ-EB-01
### EC-FU-01: ชนิด/ขนาดไฟล์แนบ (`[AI-DEFAULT]`) → jpg/png/pdf ≤10MB · **OQ:** OQ-FU-01

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
| BR_CN_EXCEEDS_OUTSTANDING | 422 | "ยอดลดหนี้เกินยอดคงเหลือของใบแจ้งหนี้อ้างอิง — ลดได้ ฿X · ใบนี้ ฿Y · เกิน ฿Z" | BR-02 |
| BR_APPROVE_EXCEEDS_OUTSTANDING | 422 | "อนุมัติไม่ได้ — ยอดคงค้าง {inv} เหลือ ฿X น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้" | BR-02 (last step) |
| BR_ENDBILL_EXCEEDS_CAP | 422 | "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X) — ยอดสุทธิห้ามติดลบ" | BR-11 |
| BR_LINE_QTY_EXCEEDED | 422 | "จำนวนลดเกินที่ลดได้: {item} (ลดได้อีก N)" | BR-03 |
| BR_PRICE_EXCEEDS_ORIG | 422 | "ราคาลดต่อหน่วยเกินราคาเดิม: {item}" | BR-04 |
| BR_LINE_NET_EXCEEDED | 422 | "มูลค่าลดเกินมูลค่าที่ลดได้ของบรรทัด: {item}" | BR-03 |
| BR_REASON_TEXT_TOO_SHORT | 422 | "ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร" | BR-05 |
| BR_RET_NEEDS_SR | 422 | "เหตุผลรับคืนต้องอ้างใบรับคืน" | BR-06 |
| BR_SUBMIT_DRAFT_ONLY | 422 | "ส่งอนุมัติได้เฉพาะฉบับร่าง" | §5.2 |
| BR_EDIT_DRAFT_ONLY | 422 | "แก้ไขได้เฉพาะฉบับร่าง" | §5.2 |
| BR_CANCEL_STATE_INVALID | 422 | "ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ \"ออกเอกสารแก้ไข\"" | §5.2 |
| BR_SEND_STATE_INVALID | 422 | "ต้องอนุมัติครบก่อนส่ง" | §5.2 |
| BR_SLOT_INCOMPLETE | 422 | "เลือกผู้อนุมัติให้ครบทุกขั้น" | BR-07 |
| BR_REASON_REQUIRED | 422 | (reject/cancel reason ว่าง) | §5.2 |

---

## §5.7 Security Bible Application
> Domains: **D2, D5, D7, D9, D15, D17**

### D2 Auth: JWT ทุก endpoint · role-based · DOA slot binding per step
### D5 Financial: ทุก amount change → audit (before/after) · approval-by-value (DOA 3-tier) · reconciliation (netVat รายเดือน ภ.พ.30) · **amount ceiling BR-02 ทั้งส่ง+อนุมัติ**
### D7 PII/PDPA: customer name/taxId/billTo/rep encrypt at rest · บุคคลธรรมดา taxId → mask ใน CSQ payload · logs ใช้ ID ref
### D-CLASS (Data Classification):
| Layer | Confidential fields (amount/customer PII/reason_text) |
|---|---|
| API response | mask ถ้า role ไม่ผ่าน |
| UI | แสดง `***` |
| Export/Print | excluded ถ้า role ไม่ผ่าน |
| Audit | log view + mutation |
> ไม่มี field ระดับ Restricted → ไม่ต้อง wire Restricted Resources. Wire: Policy Center → Data Classification.
### D9 Audit: ทุก mutation → T_cn_audit (append-only, 7 ปี, immutable) · no hard delete (BR-13)
### D15 Admin/Approval: ทุก transition logged · approver identity + timestamp · reason บังคับ reject/cancel
### D17 Multi-tenant: PostgreSQL RLS (scope company) · X-Tenant-Id middleware · cross-tenant forbidden

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| ม.86/10 (ออกใบลดหนี้อ้างใบกำกับเดิม) | BR-06/BR-08/BR-12/BR-15 · PDF อ้างเลข+วันที่ใบเดิม+เดิม/ถูกต้อง/ผลต่าง/เหตุผล (FN-92) |
| ม.82/10 (เดือนภาษี) | netVat ลง ภ.พ.30 เดือน cnDate (OQ-CN-04 ยืนยัน) |
| COSO Maker/Checker/Approver + SoD | BR-07 · §5.3 |
| PDPA | D7 · mask · retention |
| Audit trail | T_cn_audit append-only |
