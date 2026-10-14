# 06_TESTS — F-AGM-001 Farmer Member Management

> **Audience:** QA + ai-testcase-md-generator (SOW3.5)
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + BRD §7 AC
> **Microcopy-aware:** expected text ทุกข้ออ้าง microcopy กลาง html-generator-v6 + ข้อความ error ใน 05_RULES §5.4/§5.6 — testcase จะ match หน้าจอจริง 1:1

---

## §6.1 Acceptance Criteria

### สร้างสมาชิก (US-01)
- **AC-01** Given กรอกครบถูกต้อง When กด `ยืนยันสร้าง` Then ปุ่มเปลี่ยน "กำลังบันทึก…" (disabled) → drawer ปิด → toast "สร้างสมาชิกสำเร็จ" + member_id `FM-NNNNNN` → แถวใหม่ใน list สถานะ pill เหลือง "รอตรวจสอบ"
- **AC-02** Then member_id ต่อเนื่อง format FM-%06d + verify_status = pending_approval เสมอ (แม้ client ส่งค่าอื่น) + history event=create 1 แถว
- **AC-03** Given citizen_id ≠ 13 หลัก When บันทึก Then error รายช่อง "เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก" — ไม่บันทึก
- **AC-04** Given เลือก จังหวัด→อำเภอ→ตำบล แล้วเปลี่ยนจังหวัด Then อำเภอ/ตำบล/รหัสไปรษณีย์ ถูกเคลียร์ (EC-08) + อำเภอ disabled จนเลือกจังหวัดใหม่
- **AC-05** Given เลือกตำบล Then รหัสไปรษณีย์เติมอัตโนมัติ (read-only) · server ตรวจ match — mismatch → 422 "รหัสไปรษณีย์ไม่ตรงกับตำบล"
- **AC-06** Given citizen_id ซ้ำในระบบ (form) When บันทึก Then 422 error รายช่อง "เลขบัตรประชาชนนี้มีในระบบแล้ว"
- **AC-07** Given citizen_id ซ้ำ (CSV แถวใดแถวหนึ่ง) Then แถวนั้น error "เลขบัตรประชาชนซ้ำ" ใน error report — แถวอื่นสร้างปกติ

### CSV Import (US-02 — LOCK-04)
- **AC-08** Given ไฟล์ 150 แถว มี 5 แถวพัง When อัปโหลด Then progress → summary "แถวทั้งหมด 150 / สร้างสำเร็จ 145 / ล้มเหลว 5" + ตาราง error (แถว/ฟิลด์/ข้อผิดพลาด/ข้อมูล) + ปุ่ม `ดาวน์โหลดรายงาน` ได้ไฟล์ .csv ครบ 5 แถว
- **AC-09** Then แถวที่สร้างทุกแถว = pending_approval + history ต่อแถว + batch log (MET-02)
- **AC-10** Given ไฟล์ .xlsx หรือ > 5MB When เลือกไฟล์ Then block ทันที "กรุณาเลือกไฟล์ CSV เท่านั้น" / "ขนาดไฟล์ต้องไม่เกิน 5MB" — ไม่มี request ออก
- **AC-11** Given ทุกแถวผ่าน Then แสดง "อัปโหลดสำเร็จทั้งหมด ไม่มีข้อผิดพลาด" + ปิด → list refresh + toast

### ค้นหา (US-03)
- **AC-12** Given พิมพ์คำค้น When หยุดพิมพ์ 300ms Then กรองด้วย ชื่อ/นามสกุล/เบอร์โทร/เลขบัตร/Member Id (ยิง API ครั้งเดียวหลัง debounce)
- **AC-13** Given ไม่พบ Then empty state "ไม่พบรายการที่ค้นหา" + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม `ล้างตัวกรอง` — กดแล้ว filter reset + list กลับมา

### Verify เดี่ยว (US-04)
- **AC-14** Given สมาชิก pending + role R-02 When เลือก `ยืนยัน (อนุมัติ)` → `ยืนยัน` Then modal ปิด → toast "ยืนยันสมาชิกเรียบร้อย" → pill เขียว "อนุมัติแล้ว" + verified_by/at บันทึก + history event=approve
- **AC-15** Given เลือก `ปฏิเสธ` ไม่กรอกหมายเหตุ When ยืนยัน Then block "จำเป็นต้องระบุเหตุผลเมื่อปฏิเสธ" — กรอกแล้วผ่าน → pill แดง "ปฏิเสธ" + note แสดงใน detail
- **AC-16** Given สมาชิก approved/rejected แล้ว (สถานะเปลี่ยนหลังเปิดหน้า) When verify Then 422 "รายการนี้ถูกตรวจสอบไปแล้ว"

### Verify กลุ่ม (US-05)
- **AC-17** Given list มีแถว pending 3 + approved 2 When กด checkbox หัวตาราง Then เลือกเฉพาะ 3 แถว pending (แถวอื่น checkbox disabled) — เลือก 0 → ปุ่ม `ตรวจสอบที่เลือก (0)` disabled
- **AC-18** Given เลือก 10 รายการ, 2 รายการถูกคนอื่น verify ก่อน When bulk approve Then summary "สำเร็จ 8 ล้มเหลว 2" + เหตุผลรายการที่ข้าม (EC-12) — 8 รายการเปลี่ยนสถานะจริง

### แก้ไข + Re-submit (US-06 — LOCK-06/07)
- **AC-19** Given สมาชิก rejected When แก้ไข + `บันทึกการแก้ไข` สำเร็จ Then สถานะกลับ "รอตรวจสอบ" อัตโนมัติ + toast "บันทึกแล้ว — รายการกลับเข้าคิวรอตรวจสอบ" + verified_note เดิมหายจาก record แต่เห็นใน Tab ประวัติ (event=resubmit) + R-02 เห็นในคิว filter รอตรวจสอบ
- **AC-20** Given สมาชิก approved When แก้ field ใด ๆ + บันทึก Then สำเร็จ สถานะคง "อนุมัติแล้ว" + history diff Before/After · กรณีแก้ citizen_id → anomaly_flag = true (ดู XT-02)

### ลบ (US-07)
- **AC-21** Given สมาชิก pending When กด trash → modal `ลบสมาชิก?` → `ลบ` Then toast "ลบสมาชิกแล้ว" + หายจาก list (soft — DB ยังมี is_deleted=true + history event=delete)
- **AC-22** Given สมาชิก approved/rejected Then ไม่มีปุ่มลบใน list/detail · เรียก API ตรง → 422 "ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ"

### รายละเอียด + ประวัติ (US-08)
- **AC-23** Given เปิด detail (คลิกแถว) Then view drawer แสดง 3 กลุ่ม (ข้อมูลส่วนตัว / ที่อยู่ / สถานะ+โควตา) + Tab ประวัติ timeline ครบทุก event เรียงใหม่→เก่า + ปุ่มตาม role/สถานะ (ตรวจสอบ เฉพาะ R-02+pending)
- **AC-24** Given list Then citizen_id แสดง masked `1-XXXX-XXXX-XX-1` — detail แสดงเต็มเฉพาะ role ที่ผ่าน ACL (ไม่ผ่าน = masked)

### Concurrency + Idempotency (LOCK-03)
- **AC-25** Given 2 users แก้/verify record เดียวกัน When คนหลัง submit ด้วย expected_updated_at เก่า Then 409 + toast "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง" — ข้อมูลคนแรกไม่ถูกทับ
- **AC-26** Given double-click `ยืนยันสร้าง` Then ปุ่ม disabled ตั้งแต่คลิกแรก + Idempotency-Key เดิม → สร้าง 1 record เท่านั้น

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01..07 | Create + validation + cascade + unique | UI/API | AC-01..07 | P0 |
| TC-08..11 | CSV partial success + file guard | UI/API | AC-08..11 | P0 |
| TC-12..13 | Search + empty state | UI | AC-12..13 | P1 |
| TC-14..16 | Verify single (approve/reject/not-pending) | UI/API | AC-14..16 | P0 |
| TC-17..18 | Bulk verify + selectable | UI/API | AC-17..18 | P0 |
| TC-19..20 | Re-submit (LOCK-06) + edit approved (LOCK-07) | UI/API | AC-19..20 | P0 |
| TC-21..22 | Soft delete + guard | UI/API | AC-21..22 | P0 |
| TC-23..24 | Detail + history + masking | UI | AC-23..24 | P0 |
| TC-CC-01 | Optimistic lock conflict | API concurrent | AC-25 | P0 |
| TC-ID-01 | Idempotency double-submit | API | AC-26 | P0 |
| TC-RC-01..06 | Recommended edges (EC-09..15) | API/UI | §6.11 | P2 (recommended) |
| TC-XT-01..04 | Cross-module | Integration | §6.9 | P1 |
| TC-PERF-01 | List 50k members p95 < 3s · CSV 1,000 แถว < 60s | Performance | BRD §17 | P1 |
| TC-PERF-02 | Perf ที่ authoritative thresholds: reads SER≤500ms · validation VAL≤300ms · writes CRE/UPT≤1500ms | Performance | GAP-04 · authoritative TC-269/270 | P1 |
| TC-CC-02 | member_id gen ภายใต้ concurrency สูง — atomic uniqueness (ไม่มีเลขซ้ำ/ข้าม) | API concurrent | GAP-07 · authoritative TC-268/243 | P0 |
| TC-ID-02 | CSV rerun idempotency: batch_id+file_hash เดิม→รายงานเดิม · file ต่าง→ERR_BATCH_CONFLICT | API | GAP-05/07 · authoritative TC-247/279 | P0 |

---

## §6.3 Test Data Setup
- 2 tenants (ตรวจ isolation + citizen_id unique ต่อ tenant — เลขเดียวกันคนละ tenant ต้องสร้างได้)
- Users: `qa_registrar_1`, `qa_registrar_2` (R-01) · `qa_supervisor` (R-02) — registrar 2 คนไว้ทดสอบ SoD/concurrent
- Members seed: 15 รายการ (8 pending / 5 approved / 2 rejected) + 1 soft-deleted (ต้องไม่โผล่ list)
- CSV fixtures: ไฟล์ดี 150 แถว · ไฟล์ 5 แถวพัง (citizen 12 หลัก, phone 6 หลัก, postal mismatch, email ผิด, เลขบัตรซ้ำ) · ไฟล์ header ผิด · ไฟล์ TIS-620 · ไฟล์ซ้ำภายใน

---

## §6.4 Definition of Done
- [ ] AC-01..26 ผ่านครบ (P0 ทั้งหมด + P1)
- [ ] XT-01..04 ผ่าน
- [ ] Recommended RC-01..06 รันแล้ว — ผลรายงานให้ BA confirm (SOW3.7)
- [ ] ไม่ขัด LOCK-01..08 ข้อใด (Scope Lock verify — 00_OVERVIEW §0.11)
- [ ] history append-only verified (พยายาม UPDATE/DELETE ต้อง fail)
- [ ] ENC matrix registered + masking ตรวจทั้ง API และ UI
- [ ] Performance benchmark ผ่าน (§6.2 TC-PERF-01)

---

## §6.5 WebSocket Events
— ไม่มีใน Phase 1 (refresh หลัง action)

---

## §6.6 Performance Benchmarks (BRD §17 + authoritative budget)
| Operation | Target |
|---|---|
| GET list (50,000 members/tenant) | p95 < 3s (business SLA) |
| POST create / PUT update | < 1s (business SLA) |
| CSV import 1,000 แถว | < 60s |
| Bulk verify 200 รายการ | ประมวลผลสำเร็จ ไม่ timeout (chunk ฝั่ง server) |
| **Reads — SER (authoritative, GAP-04)** | **≤ 500ms** |
| **Validation — VAL (authoritative, GAP-04)** | **≤ 300ms** |
| **Writes create/update — CRE/UPT (authoritative, GAP-04)** | **≤ 1500ms** |

> เกณฑ์ authoritative (SER/VAL/CRE-UPT) เป็น technical budget ต่อ operation — เพิ่มเคียงข้าง business SLA ไม่ทดแทน · benchmark ที่ TC-PERF-02 (authoritative TC-269/270).

---

## §6.7 Test Environment Notes
- Document Numbering ใช้ sequence จริงต่อ tenant test (reset ระหว่าง suite)
- M-01 master seed อย่างน้อย 2 จังหวัด × 2 อำเภอ × 2 ตำบล (cascade + mismatch cases)
- Feature flag `sod_self_verify_block`: ทดสอบทั้ง on (block 403) และ off (log anomaly)

---

## §6.8 Trace: AC → Logic Coverage

| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01..07 | API-02 | FN-01, FN-03, FN-09 | ENG-EXT-02 |
| AC-08..11 | API-08/09 | FN-08 (→FN-03, FN-01) | ENG-EXT-01/02 |
| AC-12..13 | API-01 | FN-04 | — |
| AC-14..16 | API-05 | FN-05, FN-09 | — |
| AC-17..18 | API-06 | FN-06 (→FN-05) | — |
| AC-19..20 | API-04 | FN-02, FN-03, FN-09 | ENG-EXT-02 |
| AC-21..22 | API-07 | FN-07, FN-09 | — |
| AC-23..24 | API-03/10 | — (serializer) | — |
| AC-25..26 | API-04/05/02 | FN-02/05/01 | — |

> Coverage: FN-01..09 ✅ ครบ · ENG-EXT-01/02 ✅ ครบ

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1 + 02_API §2.X)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | Quota พยายามผูกกับสมาชิก pending/rejected | Quota | ถูกปฏิเสธ — ผูกได้เฉพาะ approved (invariant module AGM) · สมาชิกมี quota ลบไม่ได้โดยโครงสร้าง (ลบได้เฉพาะ pending) |
| XT-02 | แก้ citizen_id หลัง approved | การเงินชาวไร่ | history diff Before/After + anomaly_flag=true + `farmer_member_citizen_id_changed_event` emitted → โผล่ Anomaly Report (BRD §18.5) |
| XT-03 | Quota อัปเดต quota_status | Feature นี้ | detail แสดงค่าใหม่ (read-only) — ไม่มี endpoint ของ feature นี้เขียน field ได้ (BR-AGM-13) |
| XT-04 | Soft delete แล้วดูรายงาน/นับ active | รายงานทะเบียน | is_deleted ไม่โผล่ list + ไม่นับใน active count + ไม่นับ widget สถานะ |

---

## §6.10 Microcopy-Aware Expected Text (อ้าง microcopy กลาง v6)

| จุด | ข้อความที่ต้อง match เป๊ะ |
|---|---|
| ปุ่มสร้าง (`.ph-actions`) | `สร้างสมาชิก` |
| Drawer create footer | `ยกเลิก` (ghost) · `ยืนยันสร้าง` (primary) — submitting: `กำลังบันทึก…` |
| Drawer edit footer | `ยกเลิก` · `บันทึกการแก้ไข` |
| Toast | `สร้างสมาชิกสำเร็จ` · `บันทึกการแก้ไขแล้ว` · `ลบสมาชิกแล้ว` · error: `เกิดข้อผิดพลาด กรุณาลองใหม่` |
| Confirm ลบ | title `ลบสมาชิก?` · ปุ่ม `ลบ` (danger) — submitting: `กำลังลบ…` |
| Empty | `ยังไม่มีสมาชิกเกษตรกร` / filter: `ไม่พบรายการที่ค้นหา` + `ล้างตัวกรอง` |
| Status pills | `รอตรวจสอบ` (เหลือง) · `อนุมัติแล้ว` (เขียว) · `ปฏิเสธ` (แดง) — คำเดียวกันทุกหน้าจอ |
| Verify modal | title `ตรวจสอบสมาชิก` / bulk `ตรวจสอบสมาชิกทั้งหมด` · radio `ยืนยัน (อนุมัติ)` / `ปฏิเสธ` |
| Error messages | ตาม 05_RULES §5.4/§5.6 ตรงตัว (เช่น "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง") |
| จำนวน | `[N] รายการ` · footer `X – Y จาก Z` · ค่าว่าง `—` |

---

## §6.11 Recommended Cases (EC-09..16 — ☐ BA confirm SOW3.7)

| RC ID | Edge | Expected |
|---|---|---|
| RC-01 | CSV TIS-620 | reject ทั้งไฟล์ "ไฟล์ต้องเป็น UTF-8 กรุณาบันทึกไฟล์ใหม่เป็น UTF-8" |
| RC-02 | header ขาดคอลัมน์ email | reject ทั้งไฟล์ + ระบุ "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: email" — ไม่มีแถวใดถูกสร้าง |
| RC-03 | เลขบัตรซ้ำ 2 แถวในไฟล์ | แถวแรกสร้าง แถวสอง error "เลขบัตรประชาชนซ้ำภายในไฟล์" |
| RC-04 | ตำบลสะกดผิด | error รายแถว "ไม่พบตำบลใน[อำเภอ]" |
| RC-05 | re-submit รอบที่ 4 | สำเร็จ + anomaly_flag + โผล่ Anomaly Report |
| RC-06 | R-01 สร้างแล้ว login เดิม verify เอง | flag on: 403 "ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง" / flag off: ผ่าน + log anomaly |
