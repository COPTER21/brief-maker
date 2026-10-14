# UI BRIEF — F-AGM-005 Contract Management (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `contract-management.html` (v1.0, 2026-07-20 — html-generator-v6, audit FAIL=0 · WARN=1 inherited) |
| FRD Pack | `FRD_F-AGM-005_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-005 APPROVED (LOCK-01..10) |
| Cross-module | read Quota/Plot/Crop (verified) + **WRITE-BACK crop.license_status (contracted/none)** ⭐ |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..004 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection = snapshot card + ดูโควตา). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (fallback 5s). Thai optical centering (Rule #36). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/contracts` (default) | P-01 list | `render()` (getRoute บรรทัด 746 default 'contracts' · navigate 747) |
| `#/contracts/:contract_id` | P-01 + detail drawer (P-02) | parse parts[1] → `findContract()` → `mountViewDrawer()` refresh-safe · `openView(code)=navigate('contracts/'+code)` (861) |
Overlay ไม่ผูก route: create/edit drawer + modal 2

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก/โควตา/แปลงที่ดิน/รอบปลูก (disabled), **จัดการสัญญาส่งอ้อย (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › จัดการสัญญาส่งอ้อย" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ทะเบียนสัญญา · WKN" · `.content` fluid

## §4 P-01 Contract List (`render()` → `#page-content`)
```
.ph h1 "จัดการสัญญาส่งอ้อย" + count + sub "ทะเบียนสัญญาส่งอ้อย · รวมรอบปลูกที่ตรวจแล้ว · อนุมัติเดี่ยว/กลุ่ม"
    .ph-actions: [ตรวจสอบที่เลือก (N) disabled@0] [สร้างสัญญา primary ขวาสุด]
.stats 4: สัญญาทั้งหมด(sub ไม่รวมที่ลบ) · รอการตรวจสอบ(aging) · อนุมัติแล้ว(สัญญามีผล) · ปฏิเสธ(คืนสิทธิ์รอบปลูกแล้ว)
.card
 ├ filter-bar: search (debounce 300ms — contract_id/quota/farmer) + select สถานะ(3) + select ประเภทสัญญา(5) + ล้างตัวกรอง
 ├ bulk-bar (waiting selected): "เลือก N (รอการตรวจสอบ)" + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ table 9 คอลัมน์: ☑(waiting · cb.is-disabled แถวอื่น) · เลขสัญญา(mono แดง link) · เลขโควตา · เกษตรกร · ประเภทสัญญา(typeLabel) · รวมตัน(fmtTons) · แปลง/รอบปลูก ("N แปลง · M รอบ") · สถานะ(pill) · การดำเนินการ(pencil→trash)
 │  row .is-clickable → openView(contract_id) · sortable: contract_id/total_tons/updated_at
 └ footer: pagination + "X – Y จาก Z"
```
Empty: "ยังไม่มีสัญญา" +สร้าง · filter empty: "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Status pill | `statusPill()`/`statusLabel()` | warning "รอการตรวจสอบ"(waiting_for_verify) · success "อนุมัติแล้ว"(verified) · danger "ปฏิเสธ"(reject) |
| Contract type | `typeLabel()` (TYPES) | ตันสูญเปล่า(price-per-ton) · ส่งเสริม(support) · โปรโมชั่น โปร 7 วัน(promotion-7) · โปรโมชั่นเครน(promotion-crane) · ตกเขียว(early-purchase) |
| **Quota-search** ⭐ | `initQuotaSearch()/selectQuota()/clearQuota()` | พิมพ์→dropdown quota · เลือก→เจ้าของโควตา snapshot (read-only) + ปุ่มเปลี่ยนโควตา |
| **Plot checklist** ⭐ | `plotsForQuota()/toggleFormPlot()` | multi-select plots ของโควตา (≥1) · "เลือกแล้ว N แปลง" |
| **Crop checklist** ⭐ | `cropsForQuota()/toggleFormCrop()` | multi-select crops verified ของโควตา (≥1) · **crop license=contracted → greyed + "· ทำสัญญาแล้ว" + disabled** (guard toast "รอบปลูกนี้ทำสัญญาแล้ว") · เลือก→รวม total_tons (sumCrops) |
| **Field gating** ⭐ | `lockContractFields()` | ล็อกจนครบ quota+≥1 plot+≥1 crop + note "เลือกโควตา · แปลง (≥1) · รอบปลูก (≥1) ก่อน…" |
| **Type-specific** ⭐ | `onTypeChange()/typeSpecificSummary()` | support→support_items repeater (addSupportItem/removeSupportItem) · promotion-7→เลือกช่วง · promotion-crane→เลือกเครน · price-per-ton/early-purchase→ไม่มี |
| Snapshot card | renderFormDrawer/renderViewDrawer | teal "โควตา [QT] · [farmer] · ประเภท [type]" + ดูโควตา |
| License label | `licenseLabel()` | crop สิทธิ์: ทำสัญญาแล้ว(contracted) / ไม่มีสัญญา(none) |
| Timeline | tab ประวัติ | create/approve/reject/delete + **license-write/license-revert** events |
| Toast | `showToast` | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Detail drawer (P-02) | 920px | `mountViewDrawer()` 5 tabs (ข้อมูลทั่วไป/แปลง/รอบปลูก/เอกสาร/ประวัติ) + snapshot card | 50 |
| Create/Edit drawer | 920px | `openForm(mode,id)` — create มี build-path Section 0; edit = quota/plots/crops read-only banner | 50 |
| Approve/Reject modal | 440px | `openVerifyModal(singleId?)` — bulk ถ้าไม่ส่ง id · radio อนุมัติ/ปฏิเสธ · reject reason บังคับ | 60 |
| Delete modal | 440px danger | `openDeleteModal(id)` — confirm ลบ + attachments | 60 |

## §7 Interaction Spec
- **Build-path cascade ⭐:** (0a) `initQuotaSearch`→`selectQuota` → เจ้าของโควตา snapshot · (0b) plot checklist `plotsForQuota`/`toggleFormPlot` ≥1 · (0c) crop checklist `cropsForQuota`/`toggleFormCrop` verified ≥1 · **crop license=contracted กันเลือกซ้ำ** (greyed + toast "รอบปลูกนี้ทำสัญญาแล้ว") · รวม total_tons `sumCrops` live · fields ล็อกจนครบ (`lockContractFields`) · submit ก่อนครบ → "กรุณาตรวจสอบข้อมูลให้ครบถ้วน"
- **Type-specific ⭐:** `onTypeChange` render field ตาม 5 types · required → "เลือกช่วงโปรโมชั่น"/"เลือกเครน"/"เลือกรายการส่งเสริม"/"เลือกประเภทสัญญา"
- **Cross-module WRITE-BACK ⭐:** create → `setCropsLicense(crops,'contracted')` + history "ตั้งสถานะสิทธิ์รอบปลูก → ทำสัญญาแล้ว" · reject → `setCropsLicense(crops,'none')` + history "คืนสถานะสิทธิ์รอบปลูก → ไม่มีสัญญา" · delete → revert none · approve → keep contracted
- Esc chain · debounce 300ms · Render preservation · Row click=view · Double-submit guard

## §8 State-Driven UI Matrix (3-state)
| State | Pill | Checkbox | ปุ่มลบ(list) | Detail actions | Cross-module |
|---|---|---|---|---|---|
| waiting_for_verify | รอการตรวจสอบ(เหลือง) | selectable | มี | แก้ไข + **อนุมัติ** + **ปฏิเสธ** + ลบ | (crop=contracted จาก create) |
| verified | อนุมัติแล้ว(เขียว) | disabled | ไม่มี | แก้ไข + ลบ | crop คง contracted |
| reject | ปฏิเสธ(แดง) | disabled | ไม่มี | แก้ไข + ลบ · reject_reason box | **crop → none (revert)** |
approve/reject: อนุมัติ (ไม่ต้องมีเหตุผล)→verified · ปฏิเสธ(+reason บังคับ)→reject · verified/reject → ซ้ำไม่ได้

## §9 Microcopy (verbatim)
**ปุ่ม:** `สร้างสัญญา` · `ตรวจสอบที่เลือก (N)` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `ปิด` · `แก้ไข` · `อนุมัติ` · `ปฏิเสธ` · `ลบ` · `ยืนยัน` · `ดูโควตา` · `เปลี่ยนโควตา` · `แนบเอกสาร`
**Toast:** `สร้างสัญญาสำเร็จ — [เลขสัญญา]` · `บันทึกการแก้ไขแล้ว` · `อนุมัติเรียบร้อย` · `ปฏิเสธเรียบร้อย — คืนสถานะสิทธิ์รอบปลูกแล้ว` · `ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ X ล้มเหลว Y` · `ลบสัญญาแล้ว` · `กรุณาตรวจสอบข้อมูลให้ครบถ้วน` · `กรุณากรอกเหตุผลในการปฏิเสธ` · `กรุณาเลือกผลการตรวจสอบ` · `รอบปลูกนี้ทำสัญญาแล้ว` · `เลือกประเภทสัญญา` · `เลือกช่วงโปรโมชั่น` · `เลือกเครน` · `เลือกรายการส่งเสริม` · `เลือกได้เฉพาะรายการที่รอการตรวจสอบ` · `ไม่พบข้อมูลสัญญาที่เลือก`
**History (write-back):** `ตั้งสถานะสิทธิ์รอบปลูก → ทำสัญญาแล้ว` · `คืนสถานะสิทธิ์รอบปลูก → ไม่มีสัญญา`
**Quota search:** placeholder `พิมพ์เลขโควตา หรือ ชื่อเกษตรกร` · help `ระบบจะดึงข้อมูลเจ้าของโควตาให้อัตโนมัติ (F-AGM-002)`
**Build-path note:** `เลือกโควตา · แปลง (≥1) · รอบปลูก (≥1) ก่อน จึงจะเลือกประเภทสัญญาและกรอกข้อมูลได้` · crop `รอบปลูกที่ทำสัญญาแล้วจะถูกปิดไม่ให้เลือกซ้ำ`
**Approve/Reject modal:** title `ตรวจสอบสัญญา` · radio `อนุมัติ`/`ปฏิเสธ` · reject `กรุณาระบุเหตุผลในการปฏิเสธ...` · อนุมัติ note optional
**Delete:** title `ยืนยันการลบสัญญา` · warn `ข้อมูลสัญญาและไฟล์เอกสารที่แนบจะถูกลบ`
**Contract types:** `สัญญาตันสูญเปล่า` · `สัญญาส่งเสริม` · `สัญญาโปรโมชั่น โปร 7 วัน` · `สัญญาโปรโมชั่นเครน` · `สัญญาตกเขียว`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `QUOTAS` const + `findQuota` ⭐ | **API-13 quota-search (F-AGM-002 read)** + farmer snapshot |
| `PLOTS/CROPS` const + `plotsForQuota/cropsForQuota` ⭐ | **API-14 available-items (F-AGM-003/004 read verified, license≠contracted)** |
| `setCropsLicense()` ⭐ | **API-02/08/11 write crop.license_status (contracted/none) + sync (FN-12)** |
| `state.records` seed | API-01 GET /contracts |
| `submitForm()` create | API-02 POST (FN-01) + Idempotency-Key + write license contracted |
| `submitForm()` edit | API-05 PUT (FN-03) |
| `submitVerify()` | API-07 approve (no reason) / API-08 reject (reason + revert license) / API-09 bulk |
| `confirmDelete()` | API-11 DELETE + attachments + revert license |
| detail tab ประวัติ | API-12 history |
Mock: **8 contracts** (CT-2569-001..008: 4 waiting · 2 verified · 2 reject) ครบ 5 types · **4 quotas** · **8 plots** · **14 crops** (7 contracted / 7 none) · crop license contracted กันเลือกซ้ำใน create

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 (A) | render → #page-content | §4 |
| 01_UI P-02 (C 5-tab) | renderViewDrawer + snapshot | §6 |
| 01_UI OV-01/02 (B) | openForm + build-path + lockContractFields | §7 |
| 01_UI OV-03 (D) | openVerifyModal + reject reason + bulk | §6 |
| 01_UI OV-04 (D danger) | openDeleteModal | §6 |
| 02_API API-13/14 (read) | initQuotaSearch/plotsForQuota/cropsForQuota | §7/§10 |
| 02_API API-02/08/11 (WRITE license) | setCropsLicense | §7/§10 |
| 03_LOGIC FN-11/12 | selectQuota+checklists / setCropsLicense | §7 |
| 04_DB write crop.license_status | setCropsLicense (contracted/none) | §8 |
| 05_RULES state machine (LOCK-06/07) | submitVerify + write-back | §8 |
| 06_TESTS XT-01..05 | create→contracted / reject→none / delete→none / available read / กันซ้ำ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | Quota/Plot/Crop อ่านจาก mock (read) | HTML sim | ระบบจริง = ENG-EXT-AGM read F-AGM-002/003/004 |
| D-03 | **write-back crop license จำลองใน memory** (setCropsLicense) | HTML sim | ระบบจริง = ENG-EXT-AGM PATCH crop.license_status ใน transaction + retry (LOCK-07) |
| D-04 | optimistic CONFLICT (EC-09) ไม่มี demo (single-user) | FRD-only | 409 ที่ server (API-05) |
| D-05 | attachments = simulated | HTML sim | ระบบจริง upload + storage |
| D-06 | T3 code-only reverse (ไม่มี FRD/testcase แยก) — status label ตาม statusThai (อนุมัติแล้ว/ปฏิเสธ/รอการตรวจสอบ) | reverse-note | invariants §7 C-01 |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (contractmanagement.zip — Next.js + REST API): คงไว้ 100% (LOCK-01) — build-path (quota→plots→crops), 5 contract types + type-specific, aggregate tons, approve/reject (reject reason บังคับ) เดี่ยว+bulk, **write-back crop license (contracted/none)**, delete + attachments · เปลี่ยน: detail page → drawer 5-tab · CI shadcn → CUBE Warm Light · เพิ่ม stats + snapshot card + license-write history events + audit governance

## §13 💡 ข้อเสนอ
1. snapshot/crop deep-link ไป Quota/Crop detail จริง (ตอนนี้ mock)
2. write-back retry indicator เมื่อ sync crop license ล้มเหลว (LOCK-07 retry queue)
3. ราคา/มูลค่าสัญญาต่อ type (ตอนนี้เก็บ type-specific เชิงโครงสร้าง — ยังไม่คิดเงิน)
