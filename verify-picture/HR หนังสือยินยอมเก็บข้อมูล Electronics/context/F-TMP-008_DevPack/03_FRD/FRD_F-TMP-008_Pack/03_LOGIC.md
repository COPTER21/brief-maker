# 03_LOGIC — F-TMP-008

## §3.1 Functions (Scope-Local)
### F-TMP-008-FN-01: validateConsent
ตรวจก่อนบันทึก/ยืนยัน — ผู้เรียกต้องเป็นเจ้าของข้อมูล (BR-06) · ทุกข้อในรายการของฉบับต้องมีคำตอบ `consent` หรือ `refuse` ข้อละหนึ่งค่า (BR-01 · DEC-13) · ร่างบันทึกได้โดยยังไม่ครบ แต่ยืนยันไม่ได้ · จำนวนข้อและถ้อยคำอ่านจาก ConsentPurpose master ของ revision ที่ผูกกับใบ **ห้าม hardcode ในโค้ด** (DEC-04)
คืน `CONSENT_INCOMPLETE` พร้อมรายการลำดับข้อที่ยังไม่เลือก

### F-TMP-008-FN-02: lockConsentSnapshot
ตอนยืนยัน — คัดถ้อยคำ `data_label` / `purpose` และธง `is_sensitive` ของทุกข้อจาก master ลงบรรทัดของใบ (snapshot) พร้อม `form_code` + `form_revision` จาก F-DOCCFG และ `header_snapshot` ของ Organization · หลังจุดนี้ใบเป็น immutable (BR-02 · BR-05 · DEC-04)

### F-TMP-008-FN-03: issueNumber
ออกเลขที่เอกสารครั้งแรกตอนบันทึกร่าง — `ENG-DOC-NUM.next('PDC', company_ctx)` (DEC-09 · BR-08) · ก่อนออกเลขตรวจสถานะเปิดใช้ของแบบเอกสารที่ **F-DOCCFG** · ห้าม format เลขเองหรือบวกเลขเอง · เลขที่ออกแล้วเปลี่ยนไม่ได้

### F-TMP-008-FN-04: resolveAndSubmit
ตอนยืนยัน — `DOA-ENGINE-HOOK` resolve สายพิจารณาจาก DOA entry ของ feature ณ เวลายืนยัน แล้ว freeze ลง `approval_chain` (BR-DOA-02) · รอบนี้ DOA ประกาศ 0 ขั้น (DEC-03) ใบจึงเข้าสถานะ `confirmed` ทันที · ถ้าลูกค้าตั้งขั้นเพิ่มที่ DOA กลาง ใบจะเข้าสถานะ `pending` และวนตามขั้นโดยไม่ต้องแก้ feature · บันทึก `consented_at` = เวลาที่เจ้าของข้อมูลยืนยัน

### F-TMP-008-FN-05: decideStep
พิจารณาตามขั้น (ใช้เมื่อ DOA มีขั้น) — ผู้เรียกต้องเป็นผู้พิจารณาขั้นปัจจุบัน (BR-DOA-04 ผู้ให้ความยินยอมพิจารณาใบตัวเองไม่ได้) · ผ่านครบทุกขั้น → `confirmed` · ไม่รับหนังสือ → `rejected` พร้อมเหตุผลบังคับ และขั้นที่เหลือเป็น `skipped`

### F-TMP-008-FN-06: withdrawConsent
ถอนความยินยอม (DEC-14 · BR-03) — รับขอบเขต (รายข้อหรือทั้งฉบับ) + เหตุผลบังคับ · เขียน `pdpa_consent_withdrawal` และตั้งสถานะใบเป็น `withdrawn` · **ไม่ลบและไม่แก้บรรทัดความยินยอมเดิม** — ข้อที่ถอนเพียงไม่ถูกนับว่ามีผล (BR-04) · ถอนซ้ำข้อเดิมไม่สร้างรายการใหม่ (EC-03) · เรียก FN-09 ยิง `pdc_consent_withdrawn`

### F-TMP-008-FN-07: cancelConsent
ยกเลิกเอกสารที่ยังไม่มีผล (ร่าง/รอพิจารณา) โดยเจ้าของข้อมูลหรือผู้ดูแลงานบุคคล — เหตุผลบังคับ · ใบที่ยืนยันแล้วยกเลิกไม่ได้ ต้องใช้การถอนความยินยอมแทน

### F-TMP-008-FN-08: docPrintData + renderPdf
สร้าง data ตาม `print/PDC_data-contract.md` แล้ว render `print/form.tpl.html` (logic-less) เป็น A4 — ช่องลงชื่อ = เจ้าของข้อมูล + หนึ่งช่องต่อขั้นใน `approval_chain` (ไม่ fix จำนวน) · ค่าคงที่ ชื่อบริษัท/ลิงก์นโยบาย อ่านจาก `header_snapshot` ของใบ (BR-07) · ตอนยืนยันเรียก `ENG-DOC-STORE.store(pdf, 'PDC', consent_id, 'approved_final')` เก็บสำเนาเป็นหลักฐานแบบแก้ไขไม่ได้

### F-TMP-008-FN-09: emitEvents
ยิง event ผ่าน `ENG-NOTIFY.emit(...)` เท่านั้น ห้ามเลือกช่องทางเองใน feature:
`pdc_consent_recorded` เมื่อใบเข้าสถานะ `confirmed` · `pdc_consent_withdrawn` เมื่อ FN-06 สำเร็จ (ปิดไม่ได้) · `pdc_sensitive_refused` เมื่อยืนยันแล้วพบข้อที่เป็น `is_sensitive` และตอบ `refuse` อย่างน้อยหนึ่งข้อ
(event ของ DOA — `doa_pending` / `doa_result` — เป็นของ DOA engine ห้ามประกาศซ้ำ)

### F-TMP-008-FN-10: listVisible
กรองรายการตามสิทธิ์ (§5.3) — เจ้าของข้อมูลเห็นของตัวเอง · ผู้พิจารณาเห็นเฉพาะใบที่ส่งแล้วและตนอยู่ในสาย · ผู้ดูแลงานบุคคลเห็นทั้งหมดในหน่วยงาน · ร่างของผู้อื่นไม่ปรากฏในผลลัพธ์ทุกกรณี · ใช้กับทั้งรายการและการส่งออก CSV (CSV ไม่ส่งออกถ้อยคำข้อมูลอ่อนไหวรายข้อ ส่งเฉพาะผลยินยอม/ไม่ยินยอม)

## §3.2 Engines (EXISTING — เรียกใช้)
| Engine | ใช้ทำอะไร |
|---|---|
| `ENG-DOC-NUM` | ออกเลขที่เอกสาร (รหัส PDC) |
| `ENG-DOC-STORE` | เก็บสำเนา PDF เป็นหลักฐาน (`approved_final`) |
| `ENG-NOTIFY` | ส่ง event แจ้งเตือน |
| DOA engine (F-DLG-001) | resolve/บันทึกสายพิจารณา — `DOA-ENGINE-HOOK` |
| Document Center | ไฟล์แนบระดับใบ |

## §3.3 API ↔ Logic Trace
ดู 02_API §2.4 — ทุก mutation API มี FN ปลายทางครบ (R8)
