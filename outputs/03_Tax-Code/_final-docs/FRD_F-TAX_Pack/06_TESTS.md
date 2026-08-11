# 06_TESTS — F-TAX ทะเบียนรหัสภาษี (Tax Code Master)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + DoD + Cross-Module cases
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + `f-taxcode.html` (as-built)
> **🚨 Expected text:** ยึด **ข้อความจริงบนจอ (verbatim)** เป็นอันดับแรก (R14 HTML Fidelity) แล้ว fallback microcopy กลาง v8 — ห้ามแต่งคำเอง.

---

## §6.1 Acceptance Criteria (AC)

### AC-01: สร้างรหัสภาษี — happy (S-01)
**Given** บัญชีอยู่หน้า `#/tax-codes`, กด "สร้างรหัสภาษี"
**When** กรอก ชื่อไทย "ภาษีมูลค่าเพิ่ม 7%" + ประเภท VAT + อัตรา 7 (รหัสเว้นว่าง) → "ยืนยันสร้าง"
**Then** ปุ่มขึ้น loader "กำลังบันทึก…" · drawer ปิด · toast **"สร้างรหัสภาษี "ภาษีมูลค่าเพิ่ม 7%" สำเร็จ"** (success)
**And** record ใหม่โผล่บนสุด (page=1) · code = auto "VAT01" (ถ้าเว้นว่าง) · used=0 · status=active

### AC-02: auto-code ตามประเภท ไม่ชนของเดิม (S-01 · FN-02)
**Given** สร้างโดยเว้นรหัส, ประเภท=WHT
**Then** code = "WHT" + เลข 2 หลัก ที่ยังไม่มีในทะเบียน (case-insensitive)

### AC-03: สร้างยกเว้นภาษี → rate ล็อก 0 (S-02 · BR-03)
**Given** ฟอร์มสร้าง
**When** เลือกประเภท "ยกเว้นภาษี"
**Then** ช่องอัตรา = "0" + disabled + tag **"ยกเว้นภาษี = อัตรา 0"**
**And** สลับกลับ VAT/WHT → ช่องอัตราปลดล็อก (tag หาย)

### AC-04: แก้ตัว used=0 แก้ได้ทุก field (S-03)
**Given** record VAT10 (draft, used=0), กด "แก้ไข"
**Then** code/rate/category ไม่ disabled · แก้แล้ว "บันทึกการแก้ไข" → toast **"บันทึกการแก้ไข "{name}" แล้ว"**

### AC-05: แก้ตัว used>0 — ล็อก 3 field (S-04 · BR-04)
**Given** record VAT7 (used=214), กด "แก้ไข"
**Then** code/rate/category **disabled** + lock-tag **"ล็อก — ถูกใช้งานแล้ว"** · name_th/name_en/status แก้ได้

### AC-06: IR-TAX-01 server guard (S-04 · EC-07)
**Given** used>0, client ฝืนส่ง PUT พร้อม code/rate/category ใหม่ (bypass UI)
**When** F-TAX-API-04 ประมวลผล
**Then** server **คงค่า code/rate/category เดิม** (persist เฉพาะ name/status) · response record = ค่าเดิม 3 field · **KPI-02 = 0 persist violation**

### AC-07: เปลี่ยนสถานะอิสระ (S-05 · BR-06)
**Given** view drawer, เมนู "เปลี่ยนสถานะ"
**Then** 3 ค่าเลือกได้ทุกทิศ · ค่าปัจจุบัน disabled + mark "ปัจจุบัน" · เปลี่ยนแล้ว toast **"เปลี่ยนสถานะ "{name}" เป็น {สถานะ} แล้ว"** · ไม่มีขั้นอนุมัติ

### AC-08: bulk เปลี่ยนสถานะ (S-05 · FN-10)
**Given** เลือก ≥2 แถว, bulk bar "ตั้งเป็น ใช้งาน"
**Then** ทุกตัวเปลี่ยนเป็น active · toast **"เปลี่ยนสถานะ {n} รายการ เป็น ใช้งาน แล้ว"**

### AC-09: bulk delete confirm (S-06 · FN-12)
**Given** เลือกหลายแถว, "ลบ"
**Then** modal title **"ลบรหัสภาษี {n} รายการ?"** · ถ้ามี used>0 desc **"มี {u} รายการถูกอ้างอิงในสินค้า/เอกสาร — จะถูกข้าม ไม่ลบ"** · ปุ่ม **"ลบ {n-u} รายการ"**

### AC-10: bulk delete ผสม used>0/used=0 (S-06 · EC-06 · BR-05)
**Given** เลือก VAT7(used>0) + VAT10(used=0), ยืนยันลบ
**Then** VAT10 หาย · VAT7 อยู่ · toast **"ลบแล้ว 1 รายการ · ข้าม 1 (ถูกใช้ในสินค้า/เอกสาร)"** (warning)

### AC-11: รหัสซ้ำ case-insensitive (S-07 · EC-01 · BR-01)
**Given** มี VAT7 อยู่แล้ว, สร้างใหม่ code "vat7"
**Then** field has-err + **"รหัส vat7 ถูกใช้แล้ว"** · ไม่บันทึก (production: 409 ERR_CODE_DUPLICATE)

### AC-12: อัตราผิด (S-07 · BR-02)
**Given** สร้าง, อัตรา = ว่าง / -1 / 120
**Then** field has-err + **"กรุณากรอกอัตรา 0–100"** · ไม่บันทึก

### AC-13: import จอแรก (S-08 · FN-16 · EC-08)
**Given** กด "นำเข้า CSV"
**Then** modal title **"นำเข้ารหัสภาษีจากไฟล์"** · desc "CSV / Excel — ระบุสถานะได้ในไฟล์" · จอแรกมีแค่ upload-box "เลือกไฟล์ CSV / Excel" + ปุ่ม **"ดาวน์โหลด template ตัวอย่าง"** · **ไม่มีข้อความอธิบายคอลัมน์** · ยังไม่เลือกไฟล์ → ไม่ preview

### AC-14: import preview + status ว่าง=ร่าง (S-08 · EC-05 · BR-08)
**Given** เลือกไฟล์ (BULK_SAMPLE 5 แถว)
**Then** summary **"ตรวจแล้ว 5 แถว — นำเข้าได้ {ok} · ติดปัญหา {err} (แถวผิดจะถูกข้าม)"** · แถว VAT9 (status ว่าง) preview pill = "ร่าง"

### AC-15: import ทศนิยม + ผ่าน (S-08 · EC-04)
**Given** แถว WHT075 rate 0.75 status "ใช้งาน"
**Then** ผลตรวจ = **"พร้อมนำเข้า"** · commit → record rate 0.75 status active

### AC-16: import 6 error codes (S-08 · FN-17 · EC-02/03)
**Given** BULK_SAMPLE: VAT7(ซ้ำ), WHT99(rate 120)
**Then** VAT7 → **"รหัสซ้ำ (CODE_DUPLICATE)"** · WHT99 → **"อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)"** · แถวผิดข้าม ไม่ล้มไฟล์ · done toast **"นำเข้าแล้ว {ok} รายการ · ข้าม {err} แถว (IMPORT_ERROR)"**

### AC-17: export CSV filter + BOM (S-09 · FN-20)
**Given** filter ปัจจุบัน, กด "ส่งออก CSV"
**Then** ดาวน์โหลด `taxcode_export_YYYY-MM-DD.csv` · 7 คอลัมน์ `code,name_th,name_en,type,rate,status,used_in` · BOM (เปิด Excel ไม่เพี้ยน) · toast **"ส่งออก {n} รายการเป็น CSV แล้ว"**

### AC-18: view tabs — usage + history (S-11 · FN-23/93)
**Given** เปิด view drawer
**Then** tab "การใช้งาน" badge={used}, แสดง "จำนวนที่ถูกอ้างอิง {used} รายการ" **ไม่มีแถวลบ** · tab "ประวัติ" timeline: แก้ไขล่าสุด {updated_by·date} / สร้างรายการ {created_by·date}

### AC-19: ไม่มี GL / ลบเดี่ยว / อนุมัติ (LOCK absence — FN-40)
**Then** list แถวมีแค่ปุ่ม "แก้ไข" (ไม่มีลบเดี่ยว) · ไม่มี field เลขบัญชี GL · ไม่มีปุ่มส่งอนุมัติ · ไม่มี icon หน้ารหัส

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to AC | Priority |
|---|---|---|---|---|
| TC-01 | สร้าง happy + auto-code | UI/API | AC-01, AC-02 | P0 |
| TC-02 | exempt lock 0 | UI | AC-03 | P0 |
| TC-03 | แก้ used=0 | UI/API | AC-04 | P1 |
| TC-04 | แก้ used>0 UI lock | UI | AC-05 | P0 |
| TC-05 | IR-TAX-01 server guard (bypass UI) | API | AC-06 | **P0** |
| TC-06 | เปลี่ยนสถานะ เดี่ยว/bulk | UI/API | AC-07, AC-08 | P1 |
| TC-07 | bulk delete confirm + skip used>0 | UI/API | AC-09, AC-10 | P0 |
| TC-08 | รหัสซ้ำ case-insensitive | UI/API | AC-11 | P0 |
| TC-09 | rate invalid | UI/API | AC-12 | P1 |
| TC-10 | import 3-step + status ว่าง | UI | AC-13, AC-14, AC-15 | P0 |
| TC-11 | import 6 error codes | UI/API | AC-16 | P0 |
| TC-12 | export CSV BOM 7 cols | UI | AC-17 | P1 |
| TC-13 | view tabs usage/history | UI | AC-18 | P2 |
| TC-14 | LOCK absence (no GL/single-delete/approval) | UI | AC-19 | P1 |
| TC-CC-01 | concurrent create same code | API stress | EC-A3 | P1 |
| TC-XT-01 | lookup เห็นเฉพาะ active | Integration | XT-01 | P1 |
| TC-XT-02 | เอกสารเดิมคงค่าหลัง inactive | Integration | XT-02 | P1 |

---

## §6.3 Test Data Setup

- Seed 10 records (จาก HTML mock §8): VAT7(used 214, prove IR-TAX-01), VAT0, NONVAT(exempt), WHT1/2/3/5/10/15, VAT10(draft, used 0)
- BULK_SAMPLE 5 แถว (import): WHT075(0.75, ผ่าน), VAT9(status ว่าง→ร่าง), TAXOLD(inactive, ผ่าน), VAT7(ซ้ำ→CODE_DUPLICATE), WHT99(rate 120→RATE_INVALID)
- Role: `qa_tax_admin` (mock เปิดหมด — RBAC deferred OQ-TAX-06)

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] ทุก AC implemented + unit tests (FN-01..FN-11)
- [ ] IR-TAX-01 server guard test (TC-05) ผ่าน — **bypass UI ยัง persist ค่าเดิม**
- [ ] unique constraint case-insensitive (DB) + concurrent test (TC-CC-01)
- [ ] import row isolation (แถวผิดไม่ล้มไฟล์)

### Documentation
- [ ] API docs จาก 02_API · Scope Lock (00 §0.11) reflected
- [ ] OQ ที่ blocking (OQ-TAX-04) resolved ก่อน enable production hard-delete/used-dependent

### QA
- [ ] P0 + P1 ผ่านทั้งหมด · ไม่มี P0/P1 bug open
- [ ] verbatim microcopy ตรงจอ (spot-check toast/error/empty)

### Deployment
- [ ] Migration + seed (10 อัตราไทยมาตรฐาน) tested staging
- [ ] DOA placeholder = null · ไม่มี NOTIF emit

---

## §6.5 WebSocket Events
**ไม่มี** — LOCK-NO-NOTIF (feature ไม่ emit event).

---

## §6.6 Performance Benchmarks

| Action | Target |
|---|---|
| บันทึกสร้าง/แก้ | < 1s (mock 600ms loader) |
| List/filter/sort | < 500ms (volume สิบ–ร้อยแถว) |
| Import preview | ตามขนาดไฟล์ — threshold นิยามเพิ่ม (EC-A2, พันแถว) |

---

## §6.7 Test Environment Notes
- prototype = client mock (`state.records`) — production ทดสอบกับ API จริง + RLS tenant
- `used_count` = mock → TC-07/TC-XT ต้อง note dependency บน OQ-TAX-04 (guard พึ่งตัวเลขจริง)

---

## §6.8 Trace: AC → Logic Coverage

| AC | API tested | Functions tested |
|---|---|---|
| AC-01/02 | F-TAX-API-02 | FN-01, FN-02, FN-04 |
| AC-03 | (UI) + F-TAX-FN-04 | FN-04 (exempt force 0) |
| AC-04 | F-TAX-API-04 | FN-03 (used=0), FN-04 |
| AC-05/06 | F-TAX-API-04 | FN-03 (guard used>0) |
| AC-07/08 | F-TAX-API-05/06 | FN-06 |
| AC-09/10 | F-TAX-API-07 | FN-07 |
| AC-11/12 | F-TAX-API-02 | FN-04 |
| AC-13..16 | F-TAX-API-08 | FN-08, FN-09 |
| AC-17 | F-TAX-API-09 | FN-10 |
| AC-18 | F-TAX-API-03 | FN-11 |

> **Coverage check:** FN-01..FN-11 ทุกตัวถูก trace ≥1 AC ✅ · ไม่มี engine.

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1 Downstream Impact)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | Item Master/เอกสาร เปิด combobox กลุ่มภาษี | Item Master, docs | F-TAX-API-10 lookup คืน **เฉพาะ status=active** · draft/inactive ไม่โผล่ (BR-07) |
| XT-02 | เปลี่ยนรหัสที่ถูกอ้างเป็น inactive ภายหลัง | เอกสารเดิม | เอกสาร/สินค้าเดิม **คงค่า code+rate เดิม** (soft ref, ไม่มี cascade) · เลือกใหม่ไม่ได้ (EC-A4/A6) |
| XT-03 | แก้ไข rate ของตัวที่ used>0 (พยายาม) | เอกสารซื้อ-ขาย (VAT/WHT) | ถูก IR-TAX-01 guard บล็อก → บิลเก่าคำนวณ VAT/WHT ถูกตลอด (BR-04) |
| XT-04 | GL Posting Setup อ่านรหัส | GL (Accounting) | อ่าน `code` ได้ · ทะเบียนนี้ไม่ถือเลขบัญชี GL (LOCK-NO-GL) |

> ไม่มี compensating event (pull model, LOCK-NO-NOTIF) — downstream sync ผ่าน lookup ตอน query.

---

## §6.10 Microcopy-Aware Expected Text (verbatim จาก HTML)

| เหตุการณ์ | ข้อความจริงบนจอ |
|---|---|
| สร้างสำเร็จ | `สร้างรหัสภาษี "{name}" สำเร็จ` |
| แก้ไขสำเร็จ | `บันทึกการแก้ไข "{name}" แล้ว` |
| เปลี่ยนสถานะเดี่ยว | `เปลี่ยนสถานะ "{name}" เป็น {สถานะ} แล้ว` |
| เปลี่ยนสถานะ bulk | `เปลี่ยนสถานะ {n} รายการ เป็น {สถานะ} แล้ว` |
| ลบ bulk | `ลบแล้ว {n} รายการ · ข้าม {n} (ถูกใช้ในสินค้า/เอกสาร)` |
| ส่งออก | `ส่งออก {n} รายการเป็น CSV แล้ว` |
| import done | `นำเข้าแล้ว {n} รายการ · ข้าม {n} แถว (IMPORT_ERROR)` |
| template | `ดาวน์โหลด template ตัวอย่างแล้ว` |
| ปุ่ม create/edit | `ยืนยันสร้าง` / `บันทึกการแก้ไข` · loader `กำลังบันทึก…` |
| lock-tag / exempt-tag | `ล็อก — ถูกใช้งานแล้ว` / `ยกเว้นภาษี = อัตรา 0` |
| empty (no data / filtered) | `ยังไม่มีรหัสภาษีในระบบ` / `ไม่พบรหัสภาษีที่ตรงกับตัวกรอง` |

> ผลลัพธ์: testcase ที่ ai-testcase-md-generator สร้างต่อจะ match หน้าจอจริง 1:1.
