# 06_TESTS — F-AGM-002 Quota Management

> **Audience:** QA + ai-testcase-md-generator · **Microcopy-aware:** expected อ้าง microcopy กลาง v6 + error §5.6

---

## §6.1 Acceptance Criteria

### สร้าง From-Member (US-01)
- **AC-01** Given ค้นหาสมาชิก Approved ที่ยังไม่มีโควตา → เลือก → prefill When กรอกเลขโควตา+ยืนยันสร้าง Then toast "สร้างโควตาสำเร็จ — [เลขโควต้า]" + แถวใหม่ unverified + **member.quota_status→has_quota**
- **AC-02** Given เลือกสมาชิกที่มีโควตาแล้ว Then banner แดง "สมาชิกนี้มีโควต้าอยู่แล้ว" + block บันทึก
- **AC-03** Then สถานะเริ่ม unverified เสมอ + history event=create
- **AC-03b** Given เลือกสมาชิกที่ยัง**ไม่ Approved** (ถ้ามีในผลค้น) Then "ผูกได้เฉพาะสมาชิกที่อนุมัติแล้ว" — (member-search แสดงเฉพาะ Approved อยู่แล้ว)

### สร้าง No-Member (US-02)
- **AC-04** Given ข้ามการค้นหาสมาชิก กรอกเอง When ยืนยันสร้าง Then quota unverified ไม่ผูก member (linked_member_id=—) + **ไม่เขียน quota_status**

### quota_number unique (US-03)
- **AC-05** Given quota_number ซ้ำ When บันทึก/blur Then "เลขโควต้านี้ถูกใช้แล้ว" — ไม่บันทึก

### Validation
- **AC-06** citizen ≠ 13 → "เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก"
- **AC-07** phone ≠ 9-12 → "เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก"
- **AC-08** เลือกตำบล (current+id_card) → postal auto · เปลี่ยนจังหวัด → reset cascade (แต่ละที่อยู่แยก)
- **AC-09** email ผิดรูปแบบ → "รูปแบบอีเมลไม่ถูกต้อง" · เว้นว่างได้
- **AC-10** required ครบ → กด "ยืนยันสร้าง" ว่าง → error ครบ + "กรุณากรอกข้อมูลให้ครบถ้วน"
- **AC-11** Given เลือกสมาชิก Then prefill ชื่อ/เลขบัตร/เบอร์/ที่อยู่จากสมาชิก + member summary card
- **AC-13** เอกสารแนบ: เลือกไฟล์ >5MB หรือไม่ใช่ PDF/JPG/PNG → block

### CSV No-Member (US-04)
- **AC-14** Given ไฟล์ 6 แถว (ดี 4 เสีย 2) When upload Then summary total/created/failed + error report download + ทุกแถว unverified + No-Member
- **AC-15** Given ไฟล์ไม่ใช่ .csv Then "กรุณาเลือกไฟล์ CSV เท่านั้น"
- **AC-16** Given ทุกแถวผ่าน Then "อัปโหลดสำเร็จ..." + toast
- **AC-17** Then modal title ระบุ "No-Member"

### ค้นหา (US-05)
- **AC-18** พิมพ์ (debounce 300ms) → กรอง เลขโควตา/ชื่อ/นามสกุล/เบอร์/เลขบัตร/อีเมล
- **AC-19** ไม่พบ → "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

### Verify (US-06/07)
- **AC-20** Given unverified + R-02 When Approve+ยืนยัน Then toast "ยืนยันเรียบร้อย" + pill เขียว + history
- **AC-21** Given Reject **ไม่กรอก note** When ยืนยัน Then **ผ่านได้** (note optional — LOCK-09) + pill แดง
- **AC-21b** Given Reject (linked) Then modal แสดง warning "จะคืนค่าสถานะโควตาของสมาชิก [FM] เป็น ไม่มีโควตา" + หลังยืนยัน → **member.quota_status→no_quota** (XT-01)
- **AC-22** Given verified/rejected Then verify → 422 "รายการนี้ถูกตรวจสอบไปแล้ว" (UI ซ่อนปุ่ม)
- **AC-23** Bulk: เลือกทั้งหมด = เฉพาะ unverified · summary "สำเร็จ X ล้มเหลว Y"

### แก้ไข (US-08)
- **AC-24** Given แก้+บันทึก Then optimistic lock ผ่าน (version++) · **ไม่เปลี่ยนสถานะ** (rejected คงเป็น rejected — OQ-Q3)
- **AC-25** Given มีคนแก้ก่อน (version เก่า) Then 409 "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรชและลองใหม่อีกครั้ง"
- **AC-26** Double-click ยืนยันสร้าง → 1 รายการเท่านั้น (idempotency + disabled)

### ลบ (US-09)
- **AC-27** Given unverified When ลบ+confirm Then toast "ลบโควตาแล้ว" + soft delete · **linked → member.quota_status→no_quota** (XT-02) · verified/rejected ไม่มีปุ่มลบ

### Detail (US-10)
- **AC-28** เปิด detail Then meta + member card (ถ้า linked, link ไป Farmer) + 3 tabs (ข้อมูลทั่วไป/ไฟล์/ประวัติ)
- **AC-29** citizen_id list masked · detail เต็มตาม permission · bank/BAAC mask ตาม permission

### Retry-UX / NFR / Idempotency / A11y (authoritative recheck 2026-07-22)
- **AC-30** (G1) Given create-from-member สำเร็จ แต่ member write-back fail (TIMEOUT/502) Then **quota ยัง commit (unverified) — ไม่ rollback** + `member_update_status=scheduled_retry` + non-blocking banner "กำลังอัปเดตสถานะสมาชิก (จะ retry อัตโนมัติ)" + async retry idempotent (FN-AT-AGQ-127 / TC-323)
- **AC-31** (G5) Given Reject โควตา linked แต่ external member-API fail Then verify_status ยังเป็น rejected (บันทึก verified_by/at/note) + schedule retry การ revert (pending flag/event) + non-blocking banner — **ไม่ rollback** (TC-297)
- **AC-32** (G5) Given member-search timeout/DEPENDENCY Then spinner → toast/banner + ปุ่ม Retry · Retry สำเร็จ → prefill · ล้มเหลว → **ไม่ prefill / Save disabled** (TC-322)
- **AC-33** (G3) Given upload ไฟล์ CSV เดิม (source_file_hash เดิม) ซ้ำ Then per-row idempotency hit → คืนผลเดิม ไม่สร้าง duplicate + "ไฟล์นี้ถูกประมวลผลแล้ว — คืนผลเดิม" · same batch_id + ไฟล์ต่าง → 409 CONFLICT (TC-304)
- **AC-34** (G10) Given bulk verify 1,000 รายการ unverified Then batched writes + per-row optimistic retry ≤3 + UI progress + final summary สำเร็จ X/ล้มเหลว Y (TC-312)
- **AC-35** (G7) Given attachment บน detail Then คลิก thumbnail → in-app preview (signed URL) · preview fail → ปุ่ม `btn-open-original` เปิด tab ใหม่ (TC-313)
- **AC-36** (G8) Given เปิด Verify modal Then focus ไป radio ผล + focus-trap + `aria-modal=true` + `aria-labelledby` + `aria-live` ประกาศผล (TC-316)
- **AC-37** (G6) Given เลือกแถวข้ามหน้า pagination Then total selected รวมทุกหน้า + bulk verify ส่ง id ครบทุกหน้า (TC-307)

---

## §6.2 Test Case Inventory (สรุป)
| กลุ่ม | เคส |
|---|---|
| สร้าง From/No-Member + validation | AC-01..13 |
| CSV | AC-14..17 |
| ค้นหา | AC-18/19 |
| Verify | AC-20..23 |
| แก้ไข/idempotency | AC-24..26 |
| ลบ | AC-27 |
| Detail/masking | AC-28/29 |
| Cross-module | XT-01..05 |
| Retry-UX / NFR / Idempotency / A11y | AC-30..37 |
| Recommended | RC-01..06 |

---

## §6.4 Definition of Done
- [ ] AC-01..29 ผ่าน (P0/P1) · AC-30..37 (retry-UX / NFR / a11y — บางส่วน SIT)
- [ ] XT-01..05 ผ่าน (cross-module write-back + keep-quota async retry)
- [ ] ไม่ขัด LOCK-01..11
- [ ] history append-only verified
- [ ] ENC + masking ตรวจ API + UI
- [ ] **Reconcile: quota_status ระหว่าง Quota↔Farmer ตรงกันทุกเคส (MET-03)**
- [ ] write-back failure → retry queue (ไม่ปล่อยเงียบ)
- [ ] Performance (list/CSV/write-back) ผ่าน

---

## §6.6 Performance (BRD §17 + authoritative NFR)
GET list (50k) p95<3s · POST/PUT <1s · CSV 1,000<60s · write-back <500ms · bulk 200 chunk
**Authoritative technical budget ⭐:** reads SER ≤ 500ms · validation VAL ≤ 300ms · writes CRE/UPT ≤ 1500ms · debounce search 300ms · **skeleton loader เมื่อ load > 200ms** · bulk verify 1,000 → batched + progress + summary (TC-312)

---

## §6.8 Trace: AC → Logic
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01..03/11 | API-02/13 | FN-01,04,11,12,10 | ENG-EXT-02/03 |
| AC-04 | API-03 | FN-02,04,10 | ENG-EXT-02 |
| AC-05..10/13 | API-02/03/06 | FN-04 | ENG-EXT-02 |
| AC-14..17 | API-09/10 | FN-09(→04,02) | ENG-EXT-01/02 |
| AC-18/19 | API-01 | FN-05 | — |
| AC-20..23 | API-07/08 | FN-06/07,12,10 | ENG-EXT-03 |
| AC-24..26 | API-05 | FN-03,04,10 | ENG-EXT-02 |
| AC-27 | API-11 | FN-08,12,10 | ENG-EXT-03 |
| AC-28/29 | API-04/12 | — | — |
> Coverage: FN-01..12 ✅ · ENG-EXT-01/02/03 ✅

---

## §6.9 Cross-Module Test Cases ⭐ (BRD §12.1 + 02_API §2.X)
| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | Reject โควตา linked | Farmer | member.quota_status → no_quota + Farmer detail แสดง "ไม่มีโควตา" + history event=quota_status_written |
| XT-02 | ลบโควตา linked | Farmer | member.quota_status → no_quota (เหมือน XT-01) |
| XT-03 | สร้าง From-Member | Farmer | member.quota_status → has_quota + Farmer detail แสดง "มีโควตา" |
| XT-04 | reject/delete แต่ member ถูกลบไปแล้ว (EC-17) | Farmer | write-back skip + log anomaly (quota mutation สำเร็จ ไม่ error) |
| XT-05 ⭐ | write-back fail (member service down) — create/reject/delete linked | Farmer | quota mutation **commit ไว้ ไม่ rollback** + schedule async idempotent retry + `member_update_status=scheduled_retry` + non-blocking banner (FN-AT-AGQ-127 / AC-30/31 / TC-297/323) |

---

## §6.10 Microcopy-Aware Expected Text
| จุด | ข้อความ |
|---|---|
| ปุ่มสร้าง | `สร้างโควตา` |
| Drawer footer | `ยกเลิก` · `ยืนยันสร้าง` / `บันทึกการแก้ไข` — submitting `กำลังบันทึก…` |
| Toast | `สร้างโควตาสำเร็จ` · `บันทึกการแก้ไขแล้ว` · `ลบโควตาแล้ว` · `ยืนยันเรียบร้อย` / `ปฏิเสธเรียบร้อย` |
| Confirm ลบ | `ลบโควตา?` · ปุ่ม `ลบ` (danger) |
| Empty | `ยังไม่มีโควตา` / `ไม่พบรายการที่ค้นหา` + `ล้างตัวกรอง` |
| Pills | `รออนุมัติ`(เหลือง) · `อนุมัติ`(เขียว) · `ไม่อนุมัติ`(แดง) |
| Verify modal | `ตรวจสอบโควตา` · radio `อนุมัติ` / `ปฏิเสธ` · warning "จะคืนค่าสถานะโควตาของสมาชิก [FM] เป็น ไม่มีโควตา" |
| Cross-module block | `สมาชิกนี้มีโควต้าอยู่แล้ว` · `ผูกได้เฉพาะสมาชิกที่อนุมัติแล้ว` |
| Errors | ตาม §5.6 ตรงตัว |

---

## §6.11 Recommended Cases (EC-09..17 — ☐ BA confirm SOW3.7)
| RC | Edge | Expected |
|---|---|---|
| RC-01 | CSV TIS-620 | reject "ไฟล์ต้องเป็น UTF-8..." |
| RC-02 | header ขาดคอลัมน์ | reject ทั้งไฟล์ + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]" |
| RC-03 | quota_number ซ้ำในไฟล์ | แถวแรกผ่าน แถวหลัง error |
| RC-04 | ตำบลสะกดผิด | error รายแถว |
| RC-05 | self-verify (SoD) | flag on → 403 "ผู้สร้างไม่สามารถตรวจสอบรายการของตนเอง" / off → log |
| RC-06 | member ถูกลบก่อน write-back (EC-17) | quota mutation สำเร็จ + write-back skip + log |
