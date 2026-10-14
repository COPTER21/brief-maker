# UI BRIEF — F-AGM-004 Crop Management (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `crop-management.html` (v1.0, 2026-07-20 — html-generator-v6, audit FAIL=0 · WARN=1 inherited) |
| FRD Pack | `FRD_F-AGM-004_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-004 APPROVED (LOCK-01..13) |
| Cross-module | **double read-only**: F-AGM-002 Quota (verified,exact) + F-AGM-003 Plot (owner+verified) · ETCD/Survey external fail-soft · **ไม่มี write-back** |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001/002/003 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection = snapshot card + ดูโควตา/ดูแปลง). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (fallback 5s). Thai optical centering (Rule #36). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/crops` (default) | P-01 list | `render()` (getRoute บรรทัด 718 default 'crops' · navigate 719) |
| `#/crops/:crop_id` | P-01 + Landing drawer (P-02) | parse parts[1] → `findCrop()` → `mountViewDrawer()` refresh-safe · `openView(code)=navigate('crops/'+code)` (839) |
Overlay ไม่ผูก route: create/edit drawer + modal 3

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก/โควตา/แปลงที่ดิน (disabled), **จัดการรอบปลูก (is-active)**, การส่งอ้อยเข้าโรงงาน (disabled) + system→Settings · Breadcrumb "เกษตรกรรม › จัดการรอบปลูก" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ทะเบียนรอบปลูก · WKN" · `.content` fluid

## §4 P-01 Crop List (`render()` → `#page-content`)
```
.ph h1 "จัดการรอบปลูก" + count + sub "ทะเบียนรอบปลูกอ้อย · ผูกโควตา→แปลง · ตรวจสอบยืนยันและนำเข้า CSV"
    .ph-actions: [Upload CSV] [ตรวจสอบที่เลือก (N) disabled@0] [สร้างรอบปลูก primary ขวาสุด]
.stats 4: รอบปลูกทั้งหมด(sub "คงเหลือติดลบ N รายการ" ถ้ามี) · รอตรวจสอบ(aging) · ตรวจแล้ว(พร้อมทำสัญญา) · ปฏิเสธ(มีเหตุผลระบุ)
.card
 ├ filter-bar: search (debounce 300ms — crop_id/quota/plot/farmer) + select สถานะ(5) + select ปี(พ.ศ. getYears) + ล้างตัวกรอง
 ├ bulk-bar (waiting selected): "เลือก N (รอตรวจสอบ)" + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ table 10 คอลัมน์: ☑(waiting · cb.is-disabled แถวอื่น) · เลขรอบปลูก(mono แดง link) · ปี(พ.ศ.) · เลขโควตา · เลขแปลง · เกษตรกร · รวมตัน(fmtTons) · **คงเหลือ (ยังไม่จอง) (remainingBadge — แดงถ้า<0)** · สถานะ(pill) · การดำเนินการ(pencil→trash waiting)
 │  row .is-clickable → openView(crop_id) · sortable: crop_id/year_be/total_tons/updated_at
 └ footer: pagination + "X – Y จาก Z"
```
Empty: "ยังไม่มีรอบปลูก" +สร้าง/Upload · filter empty: "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Status pill | `statusPill()`/`statusLabel()` | warning "รอตรวจสอบ"(waiting_for_verify) · success "ตรวจแล้ว"(verified) · danger "ปฏิเสธ"(rejected) · neutral "ยกเลิก"(cancelled) · deleted=ซ่อนจาก list |
| **Remaining badge** ⭐ | `remaining()`/`remainingBadge()`/`sumBookings()` | ปกติ / **แดงเมื่อ < 0** (total_tons − ΣETCD) — list + landing |
| **Quota-search** ⭐ | `initQuotaSearch()/selectQuota()/verifiedQuotas()` | พิมพ์→dropdown quota verified · เลือก→farmer owner snapshot · ไม่พบ/ไม่ verified→"ไม่พบ Quota หรือสถานะไม่เป็น verified" |
| **Plot-search** ⭐ | `initPlotSearch()/selectPlot()/plotsForQuota()` | เปิดใช้หลังเลือก quota · list เฉพาะ plot ของเจ้าของ quota + verified · เลือก→plot snapshot (ที่อยู่+ขนาดไร่) |
| **Field gating** ⭐ | `lockCropFields()` | ล็อกจนครบ quota+plot + note "เลือกโควตาและแปลงก่อนจึงจะกรอกข้อมูลรอบปลูกได้" |
| Month select | `monthField()/monthLabel()` | 1-12 (ม.ค.–ธ.ค.) |
| Field `.field` | `validateField()` | default/is-invalid |
| Snapshot card ⭐ | renderFormDrawer/renderViewDrawer | teal "โควตา [QT] · แปลง [PLT] · [farmer]" + ดูโควตา/ดูแปลง (read-only) |
| ETCD/Survey tab | renderViewDrawer | read-only · fail-soft note "ดึงข้อมูล...ไม่สำเร็จ" |
| Timeline | tab ประวัติ | create/edit/verify/reject/cancel/delete |
| Toast | `showToast` | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Landing drawer (P-02) | 920px | `mountViewDrawer()` 5 tabs (ภาพรวม/รูปภาพ/การจอง ETCD/สำรวจ/ประวัติ) + snapshot card | 50 |
| Create/Edit drawer | 920px | `openForm(mode,id)` — create มี double-binding Section 0; edit = quota/plot read-only banner | 50 |
| Verify/Reject modal | 440px | `openVerifyModal(singleId?)` — bulk ถ้าไม่ส่ง id · radio ยืนยัน/ปฏิเสธ · reject reason บังคับ | 60 |
| Cancel/Delete modal | 440px danger | `openDeleteModal(id)` — radio ยกเลิก/ลบ + reason บังคับ | 60 |
| CSV Upload modal | 680px | `openImportModal()` — Upload→Validate→Confirm→Report · ทุกแถว waiting | 60 |

## §7 Interaction Spec
- **Double-binding cascade ⭐:** (0a) `initQuotaSearch` → `selectQuota` verified เท่านั้น → farmer snapshot · (0b) `initPlotSearch`/`plotsForQuota` เปิดหลังเลือก quota → list เฉพาะ plot ของเจ้าของ + verified → `selectPlot` → plot snapshot · fields ล็อกจนครบทั้งคู่ (`lockCropFields`) · submit ก่อนครบ → "กรุณาเลือกโควตาและแปลงก่อน"
- **Edit verified→waiting ⭐:** `submitForm` edit — ถ้า crop เดิม verified → status กลับ `waiting_for_verify` + toast "บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ" · อื่น → "บันทึกการแก้ไขแล้ว" · quota/plot read-only (LOCK-06) · version++
- **Remaining compute ⭐:** `remaining(crop) = total_tons − sumBookings(ETCD)` · `remainingBadge` แดงเมื่อ < 0 (list + landing tab ภาพรวม + ETCD tab)
- **ETCD/Survey fail-soft:** tab read-only · external down → note ไม่ block landing
- Esc chain · debounce 300ms · Render preservation (preserveState/restoreState) · Row click=view · Double-submit guard · validation verbatim (validateFormAll/validateField)

## §8 State-Driven UI Matrix (canonical 5)
| State | Pill | Checkbox | ปุ่มลบ(list) | Landing actions |
|---|---|---|---|---|
| waiting_for_verify | รอตรวจสอบ(เหลือง) | selectable | มี | แก้ไข + **ตรวจสอบ** + ยกเลิก/ลบ |
| verified | ตรวจแล้ว(เขียว) | disabled | ไม่มี | แก้ไข + ยกเลิก/ลบ (**edit→กลับ waiting**) |
| rejected | ปฏิเสธ(แดง) | disabled | ไม่มี | แก้ไข + ยกเลิก/ลบ · reject_reason box |
| cancelled | ยกเลิก(เทา) | disabled | ไม่มี | (soft — คงใน list) |
| deleted | — (ซ่อน) | — | — | route→navigate กลับ |
verify: ยืนยัน→verified · ปฏิเสธ(+reason บังคับ)→rejected · verified/rejected → verify ซ้ำไม่ได้

## §9 Microcopy (verbatim)
**ปุ่ม:** `สร้างรอบปลูก` · `Upload CSV` · `ตรวจสอบที่เลือก (N)` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `ปิด` · `แก้ไข` · `ตรวจสอบ` · `ยกเลิก/ลบ` · `ยืนยัน` · `ดูโควตา` · `ดูแปลง` · `แนบรูปภาพ`
**Toast:** `สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]` · `บันทึกการแก้ไขแล้ว` · `บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ` (edit verified) · `ยืนยันเรียบร้อย` / `ปฏิเสธเรียบร้อย` · `ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ X ล้มเหลว Y` · `ยกเลิกรอบปลูกแล้ว` / `ลบรอบปลูกแล้ว` · `นำเข้ารอบปลูก X รายการสำเร็จ — ข้าม Y แถว` · `กรุณาเลือกโควตาและแปลงก่อน` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณากรอกเหตุผลในการปฏิเสธ` · `กรุณากรอกเหตุผล` · `เลือกได้เฉพาะรายการที่รอตรวจสอบ` · `ไม่พบข้อมูลรอบปลูกที่เลือก`
**Field errors:** `ไม่พบ Quota หรือสถานะไม่เป็น verified` · `ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600` · `กรุณาเลือกเดือนที่ปลูก` · `ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0`
**Quota search:** placeholder `พิมพ์เลขโควตา หรือ ชื่อเกษตรกร` · help `เลือกได้เฉพาะโควตาที่ตรวจแล้ว (verified) · ระบบจะดึงข้อมูลเจ้าของให้อัตโนมัติ`
**Verify modal:** title `ตรวจสอบรอบปลูก` · radio `ยืนยัน`/`ปฏิเสธ` · reject `กรุณาระบุเหตุผลในการปฏิเสธ...` · verify note `หมายเหตุเพิ่มเติม (ไม่บังคับ)`
**Cancel/Delete:** title `ยกเลิก/ลบรอบปลูก?` · radio `ยกเลิก`/`ลบ` · เหตุผลบังคับ
**ETCD tab:** `การจอง (ETCD) · อ่านอย่างเดียว` · note `ข้อมูลจากระบบ ETCD ภายนอก — แสดงเพื่ออ้างอิงเท่านั้น แก้ไขไม่ได้` · `รวมจองแล้ว (TOTAL_BOOKED_TONS)` · `คงเหลือ (ยังไม่จอง)` · เตือน `ปริมาณจองเกินปริมาณรวม (คงเหลือติดลบ)`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `QUOTAS` const + `verifiedQuotas/findQuotaById` ⭐ | **API-13 quota-search (F-AGM-002 read verified)** + farmer owner snapshot |
| `PLOTS` const + `plotsForQuota/findPlotById` ⭐ | **API-14 plots (F-AGM-003 read owner+verified)** + address/size snapshot |
| ETCD bookings + `sumBookings/remaining` ⭐ | **API-15 etcd (external, fail-soft)** compute remaining |
| Survey tab | API-16 surveys (fail-soft) |
| `state.records` seed | API-01 GET /crops |
| `submitForm()` create | API-02 POST (FN-01) + Idempotency-Key |
| `submitForm()` edit | API-05 PUT (FN-03, verified→waiting) |
| `submitVerify()` | API-07 verify / API-08 bulk |
| `confirmDelete()` | API-11 cancel-delete (soft + reason) |
| `applyImport()` | API-09 upload-csv (partial, waiting) — CSV_COLS `quota_id,plot_id,year_be,planted_month,total_tons` |
| landing tab ประวัติ | API-12 history |
Mock: **8 crops** (CRP-2569-0000001..0008: 4 waiting · 2 verified · 1 rejected · 1 cancelled · deleted ซ่อน) + **5 quotas** (4 verified QT-2569-001..004) + **8 plots** (7 verified) · **negative remaining**: CRP-0000002(−20) + CRP-0000004(−15) · **double-bind**: CRP-001+002 → QT-2569-001

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 (A) | render → #page-content | §4 |
| 01_UI P-02 (C 5-tab) | renderViewDrawer + snapshot | §6 |
| 01_UI OV-01/02 (B) | openForm + double-binding + lockCropFields | §7 |
| 01_UI OV-03 (D) | openVerifyModal + reject reason + bulk | §6 |
| 01_UI OV-04 (D danger) | openDeleteModal cancel/delete | §6 |
| 01_UI OV-05 | openImportModal wizard | §6 |
| 02_API API-13/14 (double read) | initQuotaSearch/initPlotSearch | §7/§10 |
| 02_API API-15/16 (ETCD/Survey fail-soft) | sumBookings/remaining + tabs | §7/§10 |
| 03_LOGIC FN-11/12/13 | selectQuota/selectPlot/remaining | §7 |
| 05_RULES state machine (LOCK-05) | submitForm edit verified→waiting | §8 |
| 06_TESTS XT-01..05 | double-bind/quota/plot/ETCD compute/fail-soft | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด + negative warning | HTML-only | ตรง BRD §18 |
| D-02 | Quota/Plot อ่านจาก QUOTAS/PLOTS mock (read-only) | HTML sim | ระบบจริง = ENG-EXT-QP read F-AGM-002/003 |
| D-03 | ETCD/Survey = mock bookings (fail-soft branch มี) | HTML sim | ระบบจริง = ENG-EXT-ES external read fail-soft |
| D-04 | optimistic CONFLICT (AC-12) ไม่มี demo (single-user) | FRD-only | 409 ที่ server (API-05) |
| D-05 | year range 2500-2600 (code) — checklist 2500-2100 ถูก reject | reverse-resolved | invariants §7 C-01 |
| D-06 | photos = simulated attach | HTML sim | ระบบจริง upload + storage |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (crop-management.zip — Next.js): คงไว้ 100% (LOCK-01) — double-binding, 5-state canonical, remaining compute + negative badge, verify/reject (reject reason บังคับ) เดี่ยว+bulk, CSV, soft cancel/delete, ETCD/Survey read-only · **edit verified→waiting** (LOCK-05) · เปลี่ยน: detail page → Landing drawer 5-tab · CI shadcn → CUBE Warm Light · เพิ่ม stats + snapshot card + audit governance

## §13 💡 ข้อเสนอ
1. snapshot card deep-link ไป Quota/Plot detail จริง (ตอนนี้ mock toast)
2. ETCD/Survey เชื่อม external จริง + retry (ตอนนี้ mock + fail-soft branch)
3. remaining แสดง breakdown ต่อ booking + timeline การจอง
