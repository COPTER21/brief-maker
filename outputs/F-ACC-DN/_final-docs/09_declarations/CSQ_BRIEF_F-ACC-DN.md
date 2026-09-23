# CSQ_BRIEF — F-ACC-DN / F097 ใบลดหนี้ผู้ขาย (Debit Note)

> feature **ประกาศ** event → ท่อ (7C) เท่านั้น · ยิงเข้า **ENG-CSQ** (F-CSQ-01) ผ่าน `POST /csq/events` (Event Envelope)
> **ห้าม** เขียนผลรายท่อลง table ของ feature · **ห้าม** คำนวณมูลค่าเอง (ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า)
> Source of truth: FRD_Pack/03_LOGIC FN-12 (step emit CSQ) + §3.2 External Engines + 05_RULES BR-09/BR-12/BR-14 · align HTML `onFinalApprove`
> **Mirror ของ F-ACC-CN** ฝั่ง AR → re-domain เป็น AP: **ลดเจ้าหนี้ + กลับภาษีซื้อ (input VAT ค่าลบ)**

## §1 Identity
- profile_id: **CSQ-ACC-DN** `[DEFAULT — รอยืนยัน]` · feature_code: F-ACC-DN / F097 · module: Accounting / AP · กลุ่ม B · v1.0

## §2 Declared Events

| event_id | (ชื่อลัด) | trigger point (อ้าง FRD) | ท่อ | kind | เงื่อนไข | payload fields |
|---|---|---|---|---|---|---|
| `ap_dn.approved` | **dn.issued** | pending_approval → approved ครบสาย · 03_LOGIC FN-12 · 05_RULES BR-09 | **AC** (Accounting) | — | ทุกใบที่อนุมัติครบสาย | dn_id, dn_no, api_no, vendor_code, reason_code, base_amount (netBefore), vat_amount (netVat · input), grand_total, apply_to_ap, vendor_credit, dn_date, **vendor_cn_date** |
| `ap_dn.approved` | (เดียวกัน) | FN-12 "+EC ถ้า DISC/PRICE / no-PO expense" · 05_RULES BR-15 | **EC** (Economic) | `actual` | reason ∈ {DISC, PRICE} หรือ api เป็นเส้นค่าใช้จ่าย (no_po) — ค่าใช้จ่ายที่ลดจริง `[ASSUMED — CSQ-OQ-DN-1]` | reason_code, base_amount (**ติดลบ** = ค่าใช้จ่ายลดลง) |

**AC — สิ่งที่ท่อบัญชีรับไปประเมิน (feature ประกาศ ไม่คำนวณผลเอง):**
- **ลด AP (เจ้าหนี้)** — `ap_open_item.dn_applied += apply_to_ap` (Dr 2110 เจ้าหนี้ = apply_to_ap) · ส่วนเกินหนี้ค้าง = `vendor_credit` (เครดิตคงเหลือกับผู้ขาย — **ไม่ใช่เงินสด**, FN-20 · BR-13)
- **กลับภาษีซื้อ (reverse input VAT)** — `input_vat_line` **ค่าลบ** = `net_vat` · **เดือนภาษี = `vendor_cn_date`** (เดือนที่ได้รับใบลดหนี้จากผู้ขาย · ภ.พ.30 · Dr/Cr 1150 ภาษีซื้อ ค่าลบ) — **ม.82/10** (FN-21 · BR-14)
- **ฐานค่าใช้จ่าย/ส่วนลด** — Cr 5xxx (ค่าใช้จ่าย/RTV) หรือกลับต้นทุนรับเข้า = `net_before`
- **end-bill (ส่วนลดท้ายบิล):** VAT คำนวณใหม่บนฐานที่ลดจริงตาม **ม.86/10** (BR-12) — `net_vat = vat − ebVat` (ENG dn-totals) · payload ส่งค่า **หลัง** recompute แล้ว (Engine ไม่คำนวณ VAT ซ้ำ)

> **★ ต่างจาก CN (สำคัญ):** ฝั่งซื้อ input VAT ลดใน**เดือนที่ได้รับใบลดหนี้ผู้ขาย** (`vendor_cn_date`) ตาม ม.82/10 — **ไม่ใช่เดือน `dn_date`** ที่ออกเอกสาร. ถ้ายังไม่กรอก vendorCn → **ยังไม่ยิงผล input-VAT** (ภ.พ.30 = "รอเอกสาร") · เมื่อกรอก vendorCn ภายหลัง (openVendorCn บนใบ approved/sent) → payload อัปเดต `vendor_cn_date` แล้วท่อ AC ค่อยลงเดือนนั้น. legal basis ม.82/10 = **[ASSUMED — mirror CN, รอ BA ยืนยัน · OQ-DN-05]**

## §3 ท่อที่ **ไม่** ประกาศ (และเหตุผล) — ประกาศซ้ำ = register **reject 422**
| ท่อ | สถานะ | เหตุผล |
|---|---|---|
| **OC** (Operation) | ไม่ประกาศ | OP เป็นเจ้าของท่อเดียว — event มาจาก Operation Process (`sow.*`) · DN ไม่ใช่ operation event |
| **DC** (Decision) | ไม่ประกาศ | มาจาก **DOA engine** อัตโนมัติ (decision ระดับเอกสาร = การอนุมัติ) · DN ไม่มี terminal decision นอกเหนือการเซ็นอนุมัติ |
| **SC** | ไม่ประกาศ | สงวนไว้ (trigger=false เสมอ) |
| **SecC** (Security) | no-effect | ไม่มี field ระดับ Restricted (05_RULES §5.7 D-CLASS = Confidential เท่านั้น · mask ที่ producer) — ไม่เข้าเงื่อนไข SecC |
| **FC** (Financial) | **OQ — ยังไม่ประกาศ** | ลดหนี้ไม่ทำให้เงินสดเปลี่ยน · แต่ **กรณีจ่ายครบแล้ว → เครดิตคงเหลือ/เรียกเงินคืน (refund path)** ยัง open = **OQ-DN-03/OQ-DN-06** (Strike + Finance) `[ASSUMED default = ไม่ยิง FC — รอเคาะ]` |

## §4 Payload Contract
- ทุก field มาจาก entity `debit_note` (04_DB · BRD §6) · `base_amount`/`vat_amount`/`grand_total` = output ของ ENG dn-totals (netBefore/netVat/grand) · `apply_to_ap`/`vendor_credit` = output ของ `dnSplit()` (FN-20)
- **PII:** `vendor_code` = ref ID · taxId ผู้ขาย**บุคคลธรรมดา** → **mask ที่ producer ก่อนส่ง** (BR-CSQ-03 · D7 §5.7) — ห้ามส่ง Restricted ดิบ
- envelope ต้องมี `idempotency_key` unique ต่อ (feature, ref, action) กันยิงซ้ำตอน retry (BR-CSQ-02)
- reversal (ถ้ามีในอนาคต) ต้องส่ง event ที่มี `reversal_of` — ห้ามลบ/แก้ผลเดิม (BR-CSQ-04) · ปัจจุบัน DN ที่ออกเลขแล้ว **ยกเลิกไม่ได้** (ใช้ "ออกเอกสารแก้ไข" display-only — OQ-DN-04)
- **vendor_cn late-fill:** เมื่อกรอก `vendor_cn_date` ภายหลัง (FN-21 · openVendorCn) → ยิง event เดิมซ้ำด้วย idempotency_key เดิม + field ใหม่ (หรือ patch event ตามที่ ENG-CSQ รองรับ) — ท่อ AC ปรับเดือน input-VAT ตามนั้น · **ห้าม**สร้างผลใหม่ทับของเก่า

## §5 Register Checklist (ก่อน deploy จะ register สำเร็จ)
- [ ] payload fields มีจริงใน 04_DB `T_debit_note` (+_line) รวม `apply_to_ap`/`vendor_credit`/`vendor_cn_date`
- [ ] emit ที่ transition อนุมัติครบสายเท่านั้น (FN-12 · API-06 last step) — ไม่ emit ตอน draft/submit
- [ ] ไม่มี column ผลรายท่อใน table feature · ไม่มีการคำนวณมูลค่าใน feature
- [ ] G1–G3 ผ่าน (ไม่มี oc / dc-อนุมัติ / sc)
- [ ] Profile Registry ของ 7C Engine แถว CSQ-ACC-DN เปลี่ยนเป็น "เชื่อมแล้ว" หลัง event แรกเข้า

## §6 Open Questions
- **OQ-DN-05** — legal basis input-VAT reduction ฝั่งซื้อ **ม.82/10** (เดือนที่ได้รับใบลดหนี้ผู้ขาย) · `[ASSUMED — mirror CN]` · เจ้าของ: BA + Finance (ภาษี) — กระทบ payload `vendor_cn_date`/AC เดือนที่ลง
- **OQ-DN-03 / OQ-DN-06** — CSQ **FC** profile / กรณีจ่ายครบแล้วต้องการลด (เครดิตคงเหลือ → settlement/refund path) · **NO (ยังไม่เคาะ)** · เจ้าของ: Strike + Finance · default ปัจจุบัน = **ไม่ยิง FC** `[ASSUMED]`
- **CSQ-OQ-DN-1** — EC สำหรับ reason DISC/PRICE / no-PO expense ควรนับเป็น consequence เชิงเศรษฐกิจไหม (kind=actual, base ติดลบ) · default = ประกาศตาม FN-12 · `[ASSUMED — รอ BA ยืนยัน]`
- **OQ-DN-07** — CSQ profile-id `CSQ-ACC-DN` + event id `ap_dn.approved` vs `ap_dn.vat_applied` (แยก event ตอน late-fill vendorCn ไหม) ยืนยันกับ 7C Engine registry
