# 03_LOGIC — F-TMP-008
> ไม่มีตัวเลขค่าคงที่ใน logic — หัวข้อ · คะแนนเต็ม · รายชื่อช่องทาง · เกณฑ์มาตรฐาน/เกณฑ์ต่ำ · ป้าย · ข้อความแนะนำค่าเริ่ม อ่านจาก SalesConfig (config) เท่านั้น (DEC-04)

## Functions (Scope-Local)
### F-TMP-008-FN-01: validateSummary
- Input `{round_no, assessment_date, summary_date, scores[], notes, recommendations[]}` → errors VR-01..03 (05 §5.4) · scores ต้องอ้าง criterion_id/channel_id ที่อยู่ใน config snapshot ของเอกสาร · คืน warning DUP_ROUND เมื่อมีใบอื่น (status ≠ cancelled) ครั้งที่เดียวกันในปีเดียวกันของ assessment_date
### F-TMP-008-FN-02: computeChannels
- ต่อช่องทาง: n = จำนวนหัวข้อที่มีคะแนน · n = 0 → state none · n < จำนวนหัวข้อ → partial · ครบ → total = Σ score · max_total = Σ max_score (จาก config snapshot) · pct = total ÷ max_total × 100 (แสดงปัด 2 ตำแหน่ง ROUND_HALF_UP) · status เทียบค่าก่อนปัด: pct ≥ mt_csat_standard_pct (config) → pass · ≥ mt_csat_low_pct (config) → below · อื่น → far · ป้ายจาก mt_csat_bands (config)
- รายชื่อกลุ่ม pass_channels / below_channels / far_channels = ชื่อช่องทาง snapshot ตามลำดับคอลัมน์ · คำนวณฝั่ง server เสมอ (ไม่เชื่อค่าจาก FE)
### F-TMP-008-FN-03: issueNumber
- เรียกตอนบันทึกครั้งแรก (DEC-11): ตรวจ F-DOCCFG status ของ doc_type MTS (ปิด → 409 DOC_TYPE_INACTIVE) → `ENG-DOC-NUM.next('MTS', company_ctx)` → snapshot ผู้สรุป (ชื่อ/ตำแหน่ง) + `header_snapshot` (Organization) + config snapshot (หัวข้อ · คะแนนเต็ม · ช่องทาง · เกณฑ์ · ป้าย) + ค่าเริ่มข้อความแนะนำ · ตั้ง field DOA ตาม 02 §2.3 (approval_required=false · ที่เหลือ null · TODO: DOA engine) · ห้าม format/+1 เอง
### F-TMP-008-FN-04: finalizeSummary
- เฉพาะเจ้าของ · status = draft · ตรวจ VR-04/05 (ช่องทางที่เริ่มกรอกต้องครบ · ≥ 1 ช่องทางครบ · ข้อเสนอแนะ ≥ 1) → status = final · finalized_at · snapshot total/pct/status ต่อช่องทาง → FN-07 render + `ENG-DOC-STORE.store(pdf,'MTS',id,'approved_final')` (event มาตรฐาน = ฉบับสุดท้าย · เอกสารนี้ = ยืนยันสรุป) → FN-08 (mts_low_channel ถ้ามีช่องทาง far) · ไม่มีขั้นอนุมัติ (DEC-03)
### F-TMP-008-FN-05: cancelSummary
- owner หรือ Sales admin · status ∈ {draft, final} · เหตุผลบังคับ → cancelled + cancelled_* · ถ้าเดิม final และผู้ยกเลิกไม่ใช่เจ้าของ → FN-08 mts_cancelled · ใบ final ที่ยกเลิกแล้วต้องสร้างใบใหม่แทน (ไม่มีแก้หลังสรุป)
### F-TMP-008-FN-06: attachFiles
- Document Center (ref_type='MTS') · file_policy กลาง (ชนิด/ขนาด) · เฉพาะเจ้าของใบร่าง
### F-TMP-008-FN-07: docPrintData + renderPdf
- สร้าง data contract ตรงคีย์ `print/form.tpl.html` (print-spec §2): doc (title · no · is_draft · is_cancelled · form_code · revision) · round_no · blocks[] (แบ่งช่องทาง snapshot เป็นช่วงละ print_config.channels_per_block · ช่วงสุดท้ายเติมคอลัมน์ว่าง · rows[topic · max · scores[]] · max_total · totals[] · pcts[] ("—" เมื่อไม่ครบ) · statuses[]) · policy (std_pct · low_pct จาก config) · legend[] · summary.groups[] (label · channels หรือ "—" · note · is_alert) · recommendations[] (เติมแถวว่างถึง print_config.min_rows) · sign_rows[] (ผู้สรุป 1 ช่อง · ข้อความ "ยืนยันสรุปในระบบ" — จำนวนตาม DOA ซึ่งเป็น 0 ขั้น) · assessment_date · summary_date (วันที่ไทย พ.ศ.) · layout.dense → render logic-less (parity กับ tpl_render.js) · 2 หน้า (R10)
### F-TMP-008-FN-08: emitEvents
- `ENG-NOTIFY.emit`: **mts_low_channel** (draft→final และมีช่องทาง status far → role-mgr-bu + Sales admin · vars doc_no, round_no, far_channels) · **mts_cancelled** (final→cancelled โดย admin → owner) · `mts.finalized` ประกาศไม่ยิง (DEC-02) · ไม่มี doa_* (ไม่มี DOA)
### F-TMP-008-FN-09: listVisible
- canSee = sales_admin ∨ owner · ใบไม่มีสิทธิ์ → 404 · CSV ใช้ชุดเดียวกัน (คอลัมน์ % ต่อช่องทาง + จำนวนต่อกลุ่ม)

## Engines (EXISTING — เรียกใช้)
ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · Document Center — ไม่มี engine ใหม่ · DOA engine ไม่ถูกเรียก (DEC-03)

## API ↔ Logic Trace
| API | FN |
|---|---|
| 01,02,08 | FN-09 |
| 03 | FN-01, FN-02, FN-03 |
| 04 | FN-01, FN-02 |
| 05 | FN-04 (+FN-07, FN-08) |
| 06 | FN-05 (+FN-08) |
| 07 | FN-07 |
| 09 | FN-06 |
ทุก FN มี API ผูก ✓
