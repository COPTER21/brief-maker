# UI BRIEF — F-AGM-003 Plot Management (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `plot-management.html` (v1.0, 2026-07-20 — html-generator-v6, audit FAIL=0 · WARN=1 inherited) |
| FRD Pack | `FRD_F-AGM-003_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-003 APPROVED (LOCK-01..12) |
| Cross-module | F-AGM-002 Quota (READ-ONLY: search quota + farmer snapshot; **ไม่มี write-back**) |
| Drift status | ดู §11 Drift Log |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001/002 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F **connection = farmer snapshot card + ดูโควตา link**). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 multi-CDN loader (fallback 5s). Thai optical centering `.btn{padding:2px 14px 0}` · `.pill{4px 10px 3px}` (Rule #36).
Z-index: Toast 80 · ss-list 70 · modal-backdrop 60 · drawer 50 · user-menu 30 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/plots` (default) | P-01 list | `render()` (getRoute บรรทัด 700 → default 'plots' · navigate 701) |
| `#/plots/:plot_code` | P-01 + view drawer (P-02) | parse `parts[1]` → `findPlot()` → `mountViewDrawer()` — refresh-safe · `openView(code)=navigate('plots/'+code)` (816) · id ถูกลบ → navigate กลับ |
Overlay ไม่ผูก route: create/edit drawer + modal 3 (state-driven)

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → จัดการสมาชิกเกษตรกร(disabled), จัดการโควตา(disabled), **จัดการแปลงที่ดิน(is-active)**, การส่งอ้อยเข้าโรงงาน(disabled) + system→Settings · Breadcrumb "เกษตรกรรม › จัดการแปลงที่ดิน" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ทะเบียนแปลง · WKN" · `.content` fluid (Rule #30)

## §4 P-01 Plot List (`render()` → `#page-content`)
```
.ph h1 "จัดการแปลงที่ดิน" + count "[N] รายการ" + sub "ทะเบียนแปลงชาวไร่ · ผูกกับโควตา · ตรวจสอบยืนยันและนำเข้า CSV"
    .ph-actions: [Import CSV] [ตรวจสอบที่เลือก (N) disabled@0] [สร้างแปลง primary ขวาสุด]
.stats 4: แปลงทั้งหมด(sub ไม่รวมที่ถูกลบ) · รอตรวจสอบ(warn "ค้างเกิน 7 วัน N รายการ") · ตรวจแล้ว(พร้อมทำสัญญา) · ไม่ผ่าน(มีเหตุผลระบุ)
.card
 ├ filter-bar: search (debounce 300ms — onSearchInput: เลขแปลง/โควตา/ชื่อ/เอกสาร/จังหวัด) + select สถานะ + select จังหวัด + ล้างตัวกรอง(resetFilters)
 ├ bulk-bar (selectedIds>0): "เลือก N รายการ (รอตรวจสอบ)" + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ table 9 คอลัมน์: ☑(เฉพาะ waiting · cb.is-disabled แถวอื่น title "เลือกได้เฉพาะรายการที่รอตรวจสอบ") · เลขแปลง(mono แดง link) · เลขโควตา · ชื่อเกษตรกร · จังหวัด · พื้นที่(ไร่ · fmtArea) · เลขที่เอกสาร · สถานะ(pill) · การดำเนินการ(pencil→trash เฉพาะ waiting)
 │  row .is-clickable → openView(plot_code) · sortable: plot_code/area_rai/updated_at/deed_number (sortBy)
 └ footer: pagination + "X – Y จาก Z รายการ"
```
Empty: "ยังไม่มีแปลงที่ดิน" +สร้าง/Import · filter empty: "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| ปุ่ม `.btn` | CSS | default/hover/disabled/submitting (loader-2 + "กำลังบันทึก…") |
| Status pill | `statusPill()`/`statusLabel()` | pill-warning "รอตรวจสอบ" / pill-success "ตรวจแล้ว" / pill-danger "ไม่ผ่าน" |
| **Quota-search select** ⭐ | `initQuotaSearch()/selectQuota()/clearQuota()` | พิมพ์→dropdown quota verified (QT + ชื่อ + เบอร์ + citizen masked) / เลือก→farmer snapshot card + unlock fields / ไม่พบ→"ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก" · **ทุก verified quota เลือกได้ (1:N, ไม่มี block)** |
| **Field gating** ⭐ | `lockPlotFields()` | ก่อนเลือก quota → fields disabled (opacity+pointer-events) + note "เลือกโควตาก่อนจึงจะกรอกข้อมูลแปลงได้" |
| Address search-select ×3 | `searchSelectHTML()/initSearchSelect()` (`initPlotAddr/refreshPlotAddr`) | cascade จังหวัด→อำเภอ→ตำบล + postal auto readonly · เปลี่ยนจังหวัด reset |
| Field `.field` | `validateField()` on-blur | default/is-invalid(.field-error)/readonly(postal) |
| Deed check | `checkDeed()` on-blur | "เลขที่เอกสารสิทธิ์ซ้ำ" (VR-07) |
| File attach | `attachFile()` | Shapefile (บังคับ) / Document (optional) — simulated toast |
| Farmer snapshot card ⭐ | renderFormDrawer/renderViewDrawer | teal card "ผูกกับโควตา [QT] · [farmer] · [phone]" + citizen masked + ปุ่ม ดูโควตา (read-only) |
| Timeline | renderViewDrawer tab ประวัติ | create/edit/verify_pass(success)/verify_fail(danger)/delete(danger) |
| Toast | `showToast(msg,variant,ms)` | success/info/warning/error · ขวาล่าง |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| View drawer (P-02) | 920px | `mountViewDrawer()` 3 tabs (ข้อมูลทั่วไป/ไฟล์ที่อัปโหลด/ประวัติ) + farmer card · route `#/plots/:code` | 50 |
| Create/Edit drawer | 920px | `openForm(mode,id)` — create มี quota-binding Section 0; edit ไม่มี (read-only banner) · block submitting | 50 |
| Verify modal | 440px | `openVerifyModal(singleId?)` — ไม่ส่ง id = bulk · radio ผ่าน/ไม่ผ่าน · ไม่ผ่าน→reason บังคับ | 60 |
| Delete modal | 440px danger | `openDeleteModal(id)` — soft/hard radio + reason | 60 |
| CSV Import modal | 680px | `openImportModal()` — pick→preview→done · ทุกแถว Waiting for verify | 60 |

## §7 Interaction Spec
- **Quota binding sub-flow ⭐:** พิมพ์→`initQuotaSearch` dropdown (findQuotaByNo) · เลือก→`selectQuota` set form.quota_no/farmer + farmer card + `lockPlotFields(false)` unlock · ข้ามไม่ได้ (บังคับ LOCK-03) · **ไม่มี 1:0..1 block (1:N)** — ต่างจาก Quota→Farmer
- **Field gating:** ก่อนเลือก quota fields disabled (`lockPlotFields`) — submit ก่อนเลือก → "กรุณาค้นหาและเลือกโควตาก่อน"
- Esc chain: modal→closeModal → form→closeForm → view→closeView
- Search debounce 300ms (onSearchInput) · Render preservation (Rule #29 preserveState/restoreState)
- Row click = view (Rule #41) · checkbox/actions stopPropagation
- Double-submit guard (Rule #44) ทุก submit
- Cascade reset (VR-12): เปลี่ยนจังหวัด→เคลียร์อำเภอ/ตำบล/postal (initPlotAddr/refreshPlotAddr)
- validation verbatim: lat/long/postal/area/shapefile/deed (validateFormAll/validateField)

## §8 State-Driven UI Matrix
| State | Pill | Checkbox | ปุ่มลบ(list) | View actions |
|---|---|---|---|---|
| Waiting for verify | รอตรวจสอบ(เหลือง) | selectable | มี | แก้ไข + **ตรวจสอบ** + ลบ |
| Verified | ตรวจแล้ว(เขียว) | disabled | ไม่มี | แก้ไข + ลบ (ตรวจสอบซ่อน) |
| Verification failed | ไม่ผ่าน(แดง) | disabled | ไม่มี | แก้ไข + ลบ · detail แสดง fail_reason (note is-danger) |
| is_deleted | — (หายจาก list) | — | — | route→navigate กลับ |
**edit ทุก state → status ไม่เปลี่ยน (LOCK-07)** · verify: Pass→Verified · Fail→Verification failed + reason
History → timeline: create/edit(ปกติ) · verify_pass(success) · verify_fail/delete(danger)

## §9 Microcopy (verbatim)
**ปุ่ม:** `สร้างแปลง` · `Import CSV` · `ตรวจสอบที่เลือก (N)` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `ปิด` · `แก้ไข` · `ตรวจสอบ` · `ลบ` · `ยืนยัน` · `ดูโควตา` · `ล้างตัวกรอง`
**Toast:** `สร้างแปลงสำเร็จ — [เลขแปลง]` · `บันทึกการแก้ไขแล้ว` · `ยืนยันเรียบร้อย` / `ทำเครื่องหมายไม่ผ่านแล้ว` · `ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ X ล้มเหลว Y` · `ลบแปลงแล้ว` · `นำเข้าแปลง X รายการสำเร็จ — ข้าม Y แถว` · `กรุณาค้นหาและเลือกโควตาก่อน` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณากรอกเหตุผล` · `กรุณาเลือกผลการตรวจสอบ` · `เลือกได้เฉพาะรายการที่รอตรวจสอบ` · `ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV` · `ไม่พบข้อมูลแปลงที่เลือก`
**Field errors (.field-error):** `พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90` · `พิกัดลองจิจูดต้องอยู่ระหว่าง -180 ถึง 180` · `รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก` · `พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0` · `กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)` · `เลขที่เอกสารสิทธิ์ซ้ำ` · required "กรุณา…" ต่อ field
**Quota search:** placeholder `ค้นหาเลขโควตา หรือ ชื่อเกษตรกร` · help `เลือกโควตาที่ตรวจแล้ว · เลือกได้หลายแปลงต่อ 1 โควตา (1:N) · ระบบจะดึงข้อมูลเกษตรกรให้อัตโนมัติ` · ไม่พบ `ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก`
**Verify modal:** title `ตรวจสอบแปลง` · radio `ผ่าน`/`ไม่ผ่าน` · `เหตุผลที่ไม่ผ่าน` · bulk note `ใช้เหตุผลเดียวกันทุกรายการ`
**Delete modal:** title `ลบแปลง?` · radio `ลบชั่วคราว`/`ลบถาวร` · `เหตุผล (ไม่บังคับ)` · warn `การลบถาวรไม่สามารถกู้คืนได้`
**Attach:** `จำลองแนบไฟล์ลักษณะแปลง (Shapefile .zip ≤50MB)` · `จำลองแนบเอกสารสิทธิ์ (PDF/JPG ≤5MB)`
**Masking:** farmer snapshot citizen = maskCitizen `3-XXXX-XXXX-XX-N`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `ADDRESS` const | M-01 hierarchy |
| `QUOTAS` const + `findQuotaByNo` ⭐ | **API-13 quota-search (F-AGM-002 read-only)** + farmer snapshot |
| `state.records` seed | API-01 GET /plots |
| `checkDeed()` | API-06 check-deed unique |
| `submitForm()` create | API-02 POST /plots (FN-01) + Idempotency-Key |
| `submitForm()` edit | API-05 PUT /:id (FN-03, version, status คงเดิม) |
| `submitVerify()` | API-07 verify / API-08 bulk (shared reason, partial) |
| `confirmDelete()` | API-11 DELETE ?mode=soft\|hard |
| `applyImport()` | API-09 import (partial, Waiting for verify) |
| view tab ประวัติ | API-12 history |
Mock: **8 plots** (PLT-2569-001..008: 4 waiting · 2 verified · 2 verification failed) + **5 verified quotas** (QT-2569-001..005) · **1:N**: QT-2569-001 → PLT-001+002 · ADDRESS 3 จังหวัด

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 (A) | render → #page-content | §4 |
| 01_UI P-02 (C 3-tab) | renderViewDrawer + farmer card | §5/§6 |
| 01_UI OV-01/02 (B) | openForm + quota sub-flow + lockPlotFields | §7 |
| 01_UI OV-03 (D) | openVerifyModal + fail reason + bulk | §6 |
| 01_UI OV-05 | openImportModal 3-phase | §6 |
| 02_API API-13 (cross-module read) | initQuotaSearch/findQuotaByNo | §7/§10 |
| 03_LOGIC FN-11 (quota binding read-only) | selectQuota | §7 |
| 04_DB 1:N (ไม่มี unique quota_id) | เลือก quota ซ้ำได้ | §5/§8 |
| 05_RULES state machine (LOCK-02/07) | submitVerify · submitForm(status คงเดิม) | §8 |
| 06_TESTS XT-01..04 | quota bind/search/1:N/quota-ลบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats row 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | Cross-module quota อ่านจาก QUOTAS mock (read-only) | HTML sim | ระบบจริง = ENG-EXT-Q01 read F-AGM-002 (ไม่มี write-back) |
| D-03 | optimistic CONFLICT (AC-12) ไม่มี demo (single-user) | FRD-only | 409 ที่ server จริง (API-05) — copy พร้อม |
| D-04 | Shapefile/Document = simulated attach (ไม่ upload จริง) | HTML sim | ระบบจริง = upload API + storage; mandatory validate ที่ client + server |
| D-05 | Address = single line + province (code truth) — Stage10 line1/line2+plot_name ถูก reject | reverse-resolved | invariants §7 C-01/C-03 |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy v0 (agriculturalplotmanagement.zip — Next.js): คงไว้ 100% (LOCK-01) CRUD/CSV/verify/bulk/delete/search/export · quota binding · 5-field address+province · shapefile mandatory · lat/long/area validation (verbatim) · 3-state · เปลี่ยน: detail full-page → view drawer 3-tab · CI shadcn → CUBE Warm Light · เพิ่ม stats + farmer snapshot card + optimistic + audit governance

## §13 💡 ข้อเสนอ
1. farmer snapshot deep-link ไป Quota detail (`#/quotas/:qn`) จริง (ตอนนี้ mock toast)
2. GIS preview จาก lat/long + shapefile (ตอนนี้ "เปิดแผนที่" link เฉย)
3. tab ประวัติ: diff before/after ต่อ event (มีใน 04_DB history.diff)
