# 06_TESTS — F-AGM-003 Plot Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware · legacy TC-446..501 map

## §6.1 Acceptance Criteria

### สร้างแปลง + quota binding (US-01/02)
- **AC-01** ค้นหา+เลือก quota → farmer snapshot (read-only) แสดง · fields ปลดล็อก
- **AC-02** กรอก 14 fields + Shapefile → ยืนยันสร้าง → toast "สร้างแปลงสำเร็จ — [เลขแปลง]" + status Waiting for verify + audit create
- **AC-02b** quota ไม่พบ → "ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก" + block
- **AC-03** ไม่แนบ Shapefile → "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)"
- **AC-04** lat 95 → "พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90" · long 200 → "…ลองจิจูด…-180 ถึง 180"
- **AC-05** area 0/ติดลบ → "พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0"
- **AC-06** postal ≠ 5 หลัก → "รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก"
- **AC-07** deed ซ้ำ → "เลขที่เอกสารสิทธิ์ซ้ำ"
- **AC-08** เลือกจังหวัด→อำเภอ→ตำบล cascade + postal auto · เปลี่ยนจังหวัด reset

### ค้นหา/กรอง/เรียง/ส่งออก (US-09)
- **AC-09** search (debounce 300ms) กรอง เลขแปลง/โควตา/ชื่อ/เอกสาร/จังหวัด · filter status+province · ไม่พบ → "ไม่พบรายการที่ค้นหา"
- **AC-10** sort plot_code/area/updated_at · export CSV เคารพ filter · pagination

### แก้ไข (US-07)
- **AC-11** แก้ + บันทึก → optimistic version++ · **status คงเดิม** (LOCK-07) + audit
- **AC-12** stale (version เก่า) → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช"
- **AC-13** edit ระเบียน Verified → อนุญาต status คงเดิม (OQ-P1)

### CSV Import (US-03)
- **AC-14** ไฟล์ดี N แถว (แม่แบบ **13 คอลัมน์** incl. `shapefile_url`) → summary total/created/failed + ทุกแถว Waiting for verify
- **AC-15** header ไม่ตรงแม่แบบ 13 คอลัมน์ → reject ทั้งไฟล์ + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]"
- **AC-16** lat/long/postal นอกเกณฑ์ → error รายแถว + error report download
- **AC-16b** แถวไม่มี `shapefile_url` → แถวเสีย "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)" (LOCK-05 · G1) · `postal_code` เติมอัตโนมัติจากตำบล (ไม่ใช่คอลัมน์)
- **AC-17** ไม่ใช่ .csv → "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV"

### Verify (US-05/06)
- **AC-18** waiting + Pass+Confirm → toast "ยืนยันเรียบร้อย" + pill เขียว(Verified) + audit
- **AC-19** Fail ไม่กรอกเหตุผล → "กรุณากรอกเหตุผล" (block)
- **AC-20** Fail + reason → pill แดง(Verification failed) + fail_reason แสดง detail + audit
- **AC-21** Bulk: เลือกทั้งหมด = เฉพาะ waiting · Pass → ทุกรายการ Verified + audit count
- **AC-22** Bulk Fail = เหตุผลเดียวทุกรายการ (บังคับ)
- **AC-23** Bulk partial (บาง verified แล้ว) → summary "สำเร็จ X ล้มเหลว Y" + retry
- **AC-23b** verified/failed → verify ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม)

### Detail/ประวัติ (US-04/10)
- **AC-24** detail 3 tab (ข้อมูล/ไฟล์/ประวัติ) + farmer snapshot card (link ดูโควตา) + download shapefile/doc
- **AC-25** tab ประวัติ = audit timeline create/edit/verify/delete + actor/time
- **AC-25b** deep-link plot ไม่มี/ถูกลบ → "ไม่พบข้อมูลแปลงที่เลือก" + กลับ list

### ลบ (US-08)
- **AC-26** Soft delete + reason → toast "ลบแปลงแล้ว" + ซ่อนจาก list default + audit
- **AC-27** Hard delete + reason → ลบถาวร + กลับ list + audit · idempotent (กดซ้ำ/refresh ไม่ duplicate)

### idempotency
- **AC-28** double-click ยืนยันสร้าง → 1 รายการ (disabled + idempotency)

## §6.9 Cross-Module Test Cases ⭐ (BRD §4)
| XT | Scenario | Upstream | Expected |
|---|---|---|---|
| XT-01 | สร้างแปลง ผูก quota | Quota (read) | plot.quota_id set + farmer snapshot ตรง quota · **quota ไม่ถูกแก้** |
| XT-02 | quota search | Quota (read) | autocomplete คืน verified quota + farmer snapshot read-only |
| XT-03 | 1 quota หลายแปลง | Quota | สร้าง plot ที่ 2 บน quota เดิม → สำเร็จ (1:N, ไม่ block) |
| XT-04 | quota ถูกลบหลังผูก | Quota | plot คง quota_no snapshot + flag (ไม่ error, ไม่ cascade) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| ปุ่มสร้าง | `สร้างแปลง` |
| footer drawer | `ยกเลิก` · `ยืนยันสร้าง` / `บันทึกการแก้ไข` — `กำลังบันทึก…` |
| toast | `สร้างแปลงสำเร็จ` · `บันทึกการแก้ไขแล้ว` · `ลบแปลงแล้ว` · `ยืนยันเรียบร้อย` / `ทำเครื่องหมายไม่ผ่านแล้ว` |
| pills | `รอตรวจสอบ`(เหลือง) · `ตรวจแล้ว`(เขียว) · `ไม่ผ่าน`(แดง) |
| verify modal | `ตรวจสอบแปลง` · radio `ผ่าน` / `ไม่ผ่าน` · `เหตุผลที่ไม่ผ่าน` |
| delete modal | `ลบแปลง?` · radio `ลบชั่วคราว` / `ลบถาวร` · `เหตุผล (ไม่บังคับ)` |
| errors | ตาม §5.6 ตรงตัว |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01/02 | API-02/13 | FN-01,04,11,10,12 |
| AC-03..08 | API-02/03 | FN-04 |
| AC-09/10 | API-01/14 | FN-05 |
| AC-11..13 | API-05 | FN-03,04,10,12 |
| AC-14..17 | API-09 | FN-09 |
| AC-18..20 | API-07 | FN-06,10 |
| AC-21..23 | API-08 | FN-07,10 |
| AC-24/25 | API-04/12 | — |
| AC-26/27 | API-11 | FN-08,10 |
> Coverage FN-01..12 ✅ · XT-01..04 (cross-module read) ✅

## §6.6 Performance
GET list(50k) p95<3s · POST/PUT<1s · CSV 1,000<60s · shapefile ≤50MB · bulk chunk 200
