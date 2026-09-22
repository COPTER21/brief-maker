# CSQ_BRIEF — F-ACC-CN / F096 ใบลดหนี้ลูกค้า (Credit Note)

> feature **ประกาศ** event → ท่อ (7C) เท่านั้น · ยิงเข้า **ENG-CSQ** (F-CSQ-01) ผ่าน `POST /csq/events` (Event Envelope)
> **ห้าม** เขียนผลรายท่อลง table ของ feature · **ห้าม** คำนวณมูลค่าเอง (ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า)
> Source of truth: FRD_Pack/03_LOGIC FN-11 (step 6 emit CSQ) + §3.2 External Engines + 05_RULES BR-09/BR-12 · align HTML `onFinalApprove` (FIX-05)

## §1 Identity
- profile_id: **CSQ-ACC-CN** `[DEFAULT — รอยืนยัน]` · feature_code: F-ACC-CN / F096 · module: Accounting / AR · กลุ่ม B · v1.1

## §2 Declared Events

| event_id | (ชื่อลัด) | trigger point (อ้าง FRD) | ท่อ | kind | เงื่อนไข | payload fields |
|---|---|---|---|---|---|---|
| `ar_cn.approved` | **cn.issued** | pending_approval → approved ครบสาย · 03_LOGIC FN-11 step 3–6 · 05_RULES BR-09 | **AC** (Accounting) | — | ทุกใบที่อนุมัติครบสาย | cn_id, cn_no, inv_no, customer_code, reason_code, base_amount (netBefore), vat_amount (netVat), grand_total, cn_date |
| `ar_cn.approved` | (เดียวกัน) | FN-11 step 6 "+EC ถ้า DISC/PRICE" · 05_RULES BR-15 | **EC** (Economic) | `actual` | reason ∈ {DISC, PRICE} — รายได้ที่ลดจริงจากการให้ส่วนลด/แก้ราคา `[ASSUMED — CSQ-OQ-CN-1]` | reason_code, base_amount |

**AC — สิ่งที่ท่อบัญชีรับไปประเมิน (feature ประกาศ ไม่คำนวณผลเอง):**
- **ลด AR (ลูกหนี้)** — `ar_open_item.cn_applied += grand_total` (Cr 1130 ลูกหนี้ = grand)
- **กลับภาษีขาย (reverse output VAT)** — `output_vat_line` ค่าลบ = `net_vat` เดือน `cn_date` (ภ.พ.30 · Dr 2150 ภาษีขาย)
- **ฐานรายได้/ส่วนลด** — Dr 4110 (RET/QTY) หรือ 4120 (DISC/PRICE) = `net_before`
- **end-bill (ส่วนลดท้ายบิล):** VAT คำนวณใหม่บนฐานที่ลดจริงตาม **ม.86/10** (BR-12) — `net_vat = vat − ebVat` (ENG cn-totals) · payload ส่งค่า **หลัง** recompute แล้ว (Engine ไม่คำนวณ VAT ซ้ำ)

## §3 ท่อที่ **ไม่** ประกาศ (และเหตุผล) — ประกาศซ้ำ = register **reject 422**
| ท่อ | สถานะ | เหตุผล |
|---|---|---|
| **OC** (Operation) | ไม่ประกาศ | OP เป็นเจ้าของท่อเดียว — event มาจาก Operation Process (`sow.*`) · CN ไม่ใช่ operation event |
| **DC** (Decision) | ไม่ประกาศ | มาจาก **DOA engine** อัตโนมัติ (decision ระดับเอกสาร = การอนุมัติ) · CN ไม่มี terminal decision นอกเหนือการเซ็นอนุมัติ |
| **SC** | ไม่ประกาศ | สงวนไว้ (trigger=false เสมอ · OQ-C3 ยังไม่เคาะ) |
| **SecC** (Security) | no-effect | ไม่มี field ระดับ Restricted (05_RULES §5.7 D-CLASS = Confidential เท่านั้น · mask ที่ producer) — ไม่เข้าเงื่อนไข SecC |
| **FC** (Financial) | **OQ — ยังไม่ประกาศ** | FRD LD-06/§3.2 = "FC ไม่ประกาศ" (ลดหนี้ไม่ทำให้เงินสดเปลี่ยน) · แต่ **refund กรณีชำระครบ → RV/PV** ยัง open = **OQ-CN-03** (Strike + Finance) `[ASSUMED default = ไม่ยิง FC — รอเคาะ]` |

## §4 Payload Contract
- ทุก field มาจาก entity `credit_note` (04_DB · BRD §6) · `base_amount`/`vat_amount`/`grand_total` = output ของ ENG cn-totals (netBefore/netVat/grand)
- **PII:** `customer_code` = ref ID · taxId ลูกค้า**บุคคลธรรมดา** → **mask ที่ producer ก่อนส่ง** (BR-CSQ-03 · D7 §5.7) — ห้ามส่ง Restricted ดิบ
- envelope ต้องมี `idempotency_key` unique ต่อ (feature, ref, action) กันยิงซ้ำตอน retry (BR-CSQ-02)
- reversal (ถ้ามีในอนาคต) ต้องส่ง event ที่มี `reversal_of` — ห้ามลบ/แก้ผลเดิม (BR-CSQ-04) · ปัจจุบัน CN ที่ออกเลขแล้ว **ยกเลิกไม่ได้** (ใช้ "ออกเอกสารแก้ไข" display-only — LD-04)

## §5 Register Checklist (ก่อน deploy จะ register สำเร็จ)
- [ ] payload fields มีจริงใน 04_DB `T_credit_note` (+_line)
- [ ] emit ที่ transition อนุมัติครบสายเท่านั้น (FN-11 · API-06 last step) — ไม่ emit ตอน draft/submit
- [ ] ไม่มี column ผลรายท่อใน table feature · ไม่มีการคำนวณมูลค่าใน feature
- [ ] G1–G3 ผ่าน (ไม่มี oc / dc-อนุมัติ / sc)
- [ ] Profile Registry ของ 7C Engine แถว CSQ-ACC-CN เปลี่ยนเป็น "เชื่อมแล้ว" หลัง event แรกเข้า

## §6 Open Questions
- **OQ-CN-03** — CSQ **FC** profile / กรณีชำระครบแล้วต้องการลด (refund → RV/PV path) · **NO (ยังไม่เคาะ)** · เจ้าของ: Strike + Finance · default ปัจจุบัน = **ไม่ยิง FC** `[ASSUMED]`
- **CSQ-OQ-CN-1** — EC สำหรับ reason DISC/PRICE ควรนับเป็น consequence เชิงเศรษฐกิจไหม (kind=actual) · default = ประกาศตาม FN-11 · `[ASSUMED — รอ BA ยืนยัน]`
- **OQ-CN-04** — เดือนภาษี (cn_date · ม.82/10) ยืนยัน — กระทบ payload `cn_date`/AC เดือนที่ลง (แต่ไม่เปลี่ยนท่อ)
