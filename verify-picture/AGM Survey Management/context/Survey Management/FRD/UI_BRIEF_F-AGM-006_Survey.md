# UI BRIEF — F-AGM-006 Survey Management (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `survey-management.html` (v1.0, 2026-07-20 — html-generator-v6, audit FAIL=0 · WARN=1 inherited) |
| FRD Pack | `FRD_F-AGM-006_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-006 APPROVED (LOCK-01..11) |
| Cross-module | read Quota→Plot→Crop (cascade) · survey verified feeds Crop "สำรวจ" tab (F-AGM-004 pull-read) |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..005 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection = snapshot card + ดูรอบปลูก). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (fallback 5s). Thai optical centering (Rule #36). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/surveys` (default) | P-01 list | `render()` (getRoute บรรทัด 750 default 'surveys' · navigate) |
| `#/surveys/:survey_id` | P-01 + detail drawer (P-02) | parse parts[1] → `findSurvey()` → `mountViewDrawer()` refresh-safe · `openView(code)=navigate('surveys/'+code)` (869) |
Overlay ไม่ผูก route: create/edit drawer + modal 3

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก/โควตา/แปลงที่ดิน/รอบปลูก/สัญญาส่งอ้อย (disabled), **จัดการแบบสำรวจ (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › จัดการแบบสำรวจ" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่สำรวจภาคสนาม · WKN" · `.content` fluid

## §4 P-01 Survey List (`render()` → `#page-content`)
```
.ph h1 "จัดการแบบสำรวจ" + count + sub "ทะเบียนแบบสำรวจแปลง · ผูกโควตา→แปลง→รอบปลูก · ตรวจสอบยืนยันและนำเข้า CSV"
    .ph-actions: [Upload CSV] [ตรวจสอบที่เลือก (N) disabled@0] [สร้างแบบสำรวจ primary ขวาสุด]
.stats 4: สำรวจทั้งหมด(sub ไม่รวมยกเลิก/ลบ) · รอตรวจสอบ(aging) · ยืนยันแล้ว(ป้อนเข้าแท็บสำรวจของรอบปลูก) · ปฏิเสธ(มีเหตุผลระบุ)
.card
 ├ filter-bar: search (debounce 300ms — survey_id/quota/plot/crop/ผู้สำรวจ) + select สถานะ(5) + select ปี(พ.ศ. getYears) + ล้างตัวกรอง
 ├ bulk-bar (waiting selected): "เลือก N (รอตรวจสอบ)" + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ table 10 คอลัมน์: ☑(waiting) · เลขสำรวจ(mono แดง link) · วันที่สำรวจ(fmtDate) · เลขโควตา · เลขแปลง · เลขรอบปลูก · พันธุ์อ้อย · ประมาณการผลผลิต(ตัน · fmtTons) · สถานะ(pill) · การดำเนินการ(pencil→trash)
 │  row .is-clickable → openView(survey_id) · sortable: survey_id/survey_date/yield/updated_at
 └ footer: pagination + "X – Y จาก Z"
```
Empty: "ยังไม่มีแบบสำรวจ" +สร้าง/Upload · filter empty: "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Status pill | `statusPill()`/`statusLabel()` | warning "รอตรวจสอบ"(waiting_for_verify) · success "ยืนยันแล้ว"(verified) · danger "ปฏิเสธ"(rejected) · neutral "ยกเลิก"(cancelled) · deleted=ซ่อน |
| **Cascade search ×3** ⭐ | `initQuotaSearch/selectQuota` · `initPlotSearch/plotsForQuota/selectPlot` · `initCropSearch/cropsForPlot/selectCrop` | quota→farmer snapshot · plot ของโควตา · crop ของแปลง (แต่ละชั้นเปิดหลังชั้นบน) |
| **Field gating** ⭐ | `lockSurveyFields()` | ล็อกจนครบ quota+plot+crop + note "เลือกโควตา แปลง และรอบปลูกก่อน…" |
| Agronomic selects | `selectField()` | สีดิน(ดำ/น้ำตาล/แดง/เทา/อื่นๆ) · การตรวจสีใบ(ปกติ/เหลือง/เขียวเข้ม/อื่นๆ) · พบโรค/ศัตรูพืช(ไม่พบ/น้อย/ปานกลาง/มาก) · พันธุ์อ้อย |
| Field `.field` | `validateField()` | default/is-invalid (yield≥0 · size>0) |
| **Photo grid 4 หมวด** ⭐ | `attachSurveyPhoto()/removeSurveyPhoto()/photoCount()` | รูปกับแปลง(field)/รูปพืชผล(crop)/รูปลำต้นในกอ(stalk)/รูปสีดิน(soil) — simulated attach |
| Snapshot card | renderFormDrawer/renderViewDrawer | teal "โควตา [QT] · แปลง [PLT] · รอบปลูก [CRP] · [farmer]" + ดูรอบปลูก |
| Timeline | tab ประวัติ | create/verify/reject/cancel/delete |
| Toast | `showToast` | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Detail drawer (P-02) | 920px | `mountViewDrawer()` 3 tabs (ข้อมูลสำรวจ/รูปภาพ/ประวัติ) + snapshot | 50 |
| Create/Edit drawer | 920px | `openForm(mode,id)` — create มี cascade Section 0; edit = cascade read-only banner | 50 |
| Verify/Reject modal | 440px | `openVerifyModal(singleId?)` — bulk ถ้าไม่ส่ง id · radio ยืนยัน/ปฏิเสธ · reject reason บังคับ | 60 |
| Cancel/Delete modal | 440px danger | `openDeleteModal(id)` — radio ยกเลิก/ลบ + reason บังคับ | 60 |
| CSV Upload modal | 680px | `openImportModal()` — Upload→Validate→Confirm→Report · ทุกแถว waiting | 60 |

## §7 Interaction Spec
- **Cascade 3-level ⭐:** quota (`initQuotaSearch/selectQuota`) → plot (`plotsForQuota/selectPlot`) → crop (`cropsForPlot/selectCrop`) · แต่ละชั้นเปิดหลังชั้นบน · fields ล็อกจนครบ (`lockSurveyFields`) · submit ก่อนครบ → "กรุณาเลือกโควตา แปลง และรอบปลูกก่อน"
- **Edit verified→waiting ⭐:** `submitForm` edit — verified → status กลับ waiting + toast "บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ" · อื่น → "บันทึกการแก้ไขแล้ว" · cascade read-only (LOCK-13) · version++
- **Photo 4 หมวด ⭐:** `attachSurveyPhoto(cat)` เพิ่มไฟล์ต่อหมวด (field/crop/stalk/soil) · `photoCount` นับ
- validation: yield≥0 · size>0 ("กรุณาใส่ค่าที่ถูกต้อง") · required ("กรุณากรอกข้อมูลให้ครบถ้วน")
- Esc chain · debounce 300ms · Render preservation · Row click=view · Double-submit guard

## §8 State-Driven UI Matrix (canonical 5)
| State | Pill | Checkbox | ปุ่มลบ(list) | Detail actions |
|---|---|---|---|---|
| waiting_for_verify | รอตรวจสอบ(เหลือง) | selectable | มี | แก้ไข + **ตรวจสอบ** + ยกเลิก/ลบ |
| verified | ยืนยันแล้ว(เขียว) | disabled | ไม่มี | แก้ไข + ยกเลิก/ลบ (**edit→กลับ waiting**) |
| rejected | ปฏิเสธ(แดง) | disabled | ไม่มี | แก้ไข + ยกเลิก/ลบ · reject_reason box |
| cancelled | ยกเลิก(เทา) | disabled | ไม่มี | (soft) |
| deleted | — (ซ่อน) | — | — | route→navigate กลับ |
verify: ยืนยัน→verified (note optional) · ปฏิเสธ(+reason บังคับ)→rejected · verified/rejected → ซ้ำไม่ได้

## §9 Microcopy (verbatim)
**ปุ่ม:** `สร้างแบบสำรวจ` · `Upload CSV` · `ตรวจสอบที่เลือก (N)` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `ปิด` · `แก้ไข` · `ตรวจสอบ` · `ยกเลิก/ลบ` · `ยืนยัน` · `ดูรอบปลูก`
**Toast:** `สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]` · `บันทึกการแก้ไขแล้ว` · `บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ` (edit verified) · `ยืนยันเรียบร้อย` / `ปฏิเสธเรียบร้อย` · `ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ X ล้มเหลว Y` · `ยกเลิกแบบสำรวจแล้ว` / `ลบแบบสำรวจแล้ว` · `นำเข้าแบบสำรวจ X รายการสำเร็จ — ข้าม Y แถว` · `กรุณาเลือกโควตา แปลง และรอบปลูกก่อน` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณากรอกเหตุผลในการปฏิเสธ` · `กรุณากรอกเหตุผล` · `เลือกได้เฉพาะรายการที่รอตรวจสอบ` · `ไม่พบข้อมูลแบบสำรวจที่เลือก`
**Field errors:** yield/size = "กรุณาใส่ค่าที่ถูกต้อง" · required = "กรุณากรอกข้อมูลให้ครบถ้วน"
**Quota search:** placeholder `พิมพ์เลขโควตา หรือ ชื่อเกษตรกร` · help `เลือกได้เฉพาะโควตาที่ยืนยันแล้ว (verified) · ระบบจะดึงข้อมูลเจ้าของให้อัตโนมัติ`
**Verify modal:** title `ตรวจสอบแบบสำรวจ` · radio `ยืนยัน`/`ปฏิเสธ` · reject `กรุณาระบุเหตุผลในการปฏิเสธ...`
**Cancel/Delete:** title `ยกเลิก/ลบแบบสำรวจ?` · radio `ยกเลิก`/`ลบ` · เหตุผลบังคับ
**Photo หมวด:** `รูปกับแปลง` · `รูปพืชผล` · `รูปลำต้นในกอ` · `รูปสีดิน` · attach `จำลองแนบรูป [หมวด] (JPG/PNG ≤5MB)`
**Agronomic:** สีดิน `ดำ/น้ำตาล/แดง/เทา/อื่นๆ` · การตรวจสีใบ `ปกติ/เหลือง/เขียวเข้ม/อื่นๆ` · พบโรค/ศัตรูพืช `ไม่พบ/น้อย/ปานกลาง/มาก`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `QUOTAS/PLOTS/CROPS` const + `verifiedQuotas/plotsForQuota/cropsForPlot` ⭐ | **API-13 quota-search + API-14 cascade (F-AGM-002/003/004 read)** |
| `state.records` seed | API-01 GET /surveys |
| `submitForm()` create | API-02 POST (FN-01) + Idempotency-Key |
| `submitForm()` edit | API-05 PUT (FN-03, verified→waiting) |
| `submitVerify()` | API-07 verify / API-08 bulk |
| `confirmDelete()` | API-11 cancel-delete (soft + reason) |
| `attachSurveyPhoto()` | API-16 photos (4 categories) |
| `applyImport()` | API-09 upload-csv (partial, waiting) |
| detail tab ประวัติ | API-12 history |
| **feeds Crop** | survey verified → Crop F-AGM-004 อ่าน (แท็บสำรวจ — pull-read) |
Mock: **8 surveys** (SV-2569-0000001..0008: 4 waiting · 2 verified · 1 rejected · 1 cancelled) · **4 quotas · 7 plots · 7 crops** · **1 crop:N surveys**: SV-0000001+0000002 → CRP-2569-0000001 · varieties ขอนแก่น 3/LK92-11/K88-92 · photos 4 หมวด/รายการ

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 (A) | render → #page-content | §4 |
| 01_UI P-02 (C 3-tab) | renderViewDrawer + snapshot | §6 |
| 01_UI OV-01/02 (B) | openForm + cascade + lockSurveyFields | §7 |
| 01_UI OV-03 (D) | openVerifyModal + reject reason + bulk | §6 |
| 01_UI OV-04 (D danger) | openDeleteModal | §6 |
| 01_UI OV-05 | openImportModal wizard | §6 |
| 02_API API-13/14 (cascade read) | initQuotaSearch/plotsForQuota/cropsForPlot | §7/§10 |
| 03_LOGIC FN-11 (cascade) | selectQuota/selectPlot/selectCrop | §7 |
| 05_RULES state machine (LOCK-07) | submitForm edit verified→waiting | §8 |
| 06_TESTS XT-01..04 | cascade read / feeds Crop / 1 crop:N | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | Quota/Plot/Crop อ่านจาก mock (cascade read) | HTML sim | ระบบจริง = ENG-EXT-AGM read F-AGM-002/003/004 |
| D-03 | survey verified feeds Crop = ระบุใน comment (Crop pull-read) | design | ระบบจริง = Crop F-AGM-004 อ่าน survey verified (แท็บสำรวจ) |
| D-04 | optimistic CONFLICT (EC-07) ไม่มี demo (single-user) | FRD-only | 409 ที่ server (API-05) |
| D-05 | photos 4 หมวด = simulated attach | HTML sim | ระบบจริง upload + storage |
| D-06 | T3 code-only reverse — status label ตาม code (verified="ยืนยันแล้ว") | reverse-note | invariants §7 C-01 |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (surveymanagement.zip — Next.js): คงไว้ 100% (LOCK-01) — cascade (quota→plot→crop), agronomic fields (พันธุ์/ผลผลิต/ขนาด/สีดิน/สีใบ/โรค-ศัตรูพืช/พิกัด), photos 4 หมวด, verify/reject (reject reason บังคับ) เดี่ยว+bulk, CSV, soft cancel/delete, edit verified→waiting · เปลี่ยน: detail page → drawer 3-tab · CI shadcn → CUBE Warm Light · เพิ่ม stats + snapshot card + audit governance

## §13 💡 ข้อเสนอ
1. snapshot deep-link ไป Crop detail จริง (ตอนนี้ mock)
2. รูปภาพ 4 หมวด แสดง thumbnail จริง + lightbox (ตอนนี้ list ชื่อไฟล์)
3. แสดงประวัติการสำรวจย้อนหลังของรอบปลูกเดียวกัน (1 crop:N surveys) ในหน้า detail
