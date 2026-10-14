# UI BRIEF — F-AGM-009 Area & Permission Management (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `area-permission-management.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=3 inherited: font-size + submit-loading + stepper) |
| FRD Pack | `FRD_F-AGM-009_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-009 APPROVED (LOCK-01..11) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (T3 code-only, AS-BUILT จาก React/Vite shadcn) |
| Cross-module | read ERP HR (employees) + Geography masters · **Areas scope** Farmer (F-AGM-001)/Quota (F-AGM-002) · **Roles gate** AGM chain (RBAC) |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..008 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (`loadLucide`/`bootIfReady` fallback 5s). Thai optical centering (Rule #36). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/areas` (default) | P-01 Areas List (topTab=areas) | `render()` (`getRoute()` บรรทัด 213 default 'areas' · `topTabBar` · `navigate`) |
| `#/areas/:area_id` | P-01 + Area Detail drawer (P-02, 4 tabs) | parse `parts[1]` → `findArea()` → `mountViewDrawer()` refresh-safe · `openView(id)` · ไม่พบ → toast "ไม่พบพื้นที่นี้" + กลับ |
| `#/roles` | P-03 Roles (topTab=roles · SA/Director เท่านั้น) | `navigate('roles')` → `renderRolesPage()` · ถ้าไม่ canWrite → redirect areas |
Overlay ไม่ผูก route: create-area drawer (`openForm('area')`) · add-head modal (`openModalBox('addhead')`) · create-code modal (`openModalBox('createcode')`) · add-director modal (`openModalBox('adddirector')`) · confirm modal (`openConfirm`)

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก..หนี้ลูกหนี้ (disabled), **พื้นที่และการกำหนดสิทธิ์ (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › การบริหาร › พื้นที่และการกำหนดสิทธิ์" · User chip "สมพร วงศ์ทะเบียน / ผู้ดูแลระบบ (System Admin) · WKN" · **top tab-bar** (`topTabBar`): Areas + Roles (Roles ซ่อนถ้า !canWrite)

## §4 P-01 Areas List (`renderAreasPage()` → `#page-content`, topTab=areas)
```
.ph h2 "พื้นที่ (Areas)" + count + sub "จัดการพื้นที่ปฏิบัติการ, สถานะ และหัวหน้าพื้นที่"
    .ph-actions: [Export CSV] [สร้างพื้นที่ primary — canWrite]
.stats 4: พื้นที่ทั้งหมด(ทุกสถานะ) · เปิดใช้งาน(Active) · Extension Codes รวม(`totalCodes`) · Area Heads รวม(`totalHeads`)
.card
 ├ filter-bar: search (debounce — ชื่อพื้นที่/รหัส · `onSearchInput`) + select จังหวัด(ทุกจังหวัด + provinces) + select สถานะ(ทุกสถานะ/เปิดใช้งาน/ปิดใช้งาน) + ล้างตัวกรอง
 ├ bulk-bar (selected): "เลือกแล้ว N รายการ" (`toggleSelect/toggleSelectAll`)
 ├ table: ☑ · ชื่อพื้นที่(mono แดง link) · จังหวัด · #Heads(`countBadge` center) · #Codes(center) · สถานะ(`statusPill`) · การกระทำ(เปิด/แก้ไข/toggle)
 │  row → openView(area_id) · toggle → `toggleAreaStatus` (deactivate guard)
 └ footer: "แสดง X-Y จาก Z รายการ" + pagination (25/หน้า · `getPaged/goToPage`)
```
Empty: "ยังไม่มีพื้นที่" +สร้างพื้นที่ใหม่ · filter empty: "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Area status pill | `statusPill()` | success เปิดใช้งาน(Active) · neutral ปิดใช้งาน(Inactive) |
| **Code status pill ⭐** | `codeStatusPill()` | neutral ว่าง(EMPTY) · success ใช้งานอยู่(OCCUPIED) |
| Count badge | `countBadge()` | #Heads / #Codes (info) |
| **Geography cascade ×3 ⭐** | `setAreaProvince/setAreaDistrict/setAreaSub` · `districtsOf/subdistrictsOf/findSub` | จังหวัด → อำเภอ(enable หลังเลือกจังหวัด) → ตำบล(หลังอำเภอ) → postal auto-fill (read-only) |
| **ERP employee search ⭐** | `initSearchSelect`/`empOptions`/`empStatusTag`/`updateEmpPreview` | ค้น ชื่อ/รหัส/email · tag inactive · active-only guard |
| Action badge (audit) | `actionBadge()` | area.created/updated/head.added/code.created |
| Confirm modal | `openConfirm`/`renderConfirmModal`/`confirmYes` | remove head/director |
| RBAC gate | `canWrite = ['System Admin','Director'].includes(CURRENT_ROLE)` | hide/disable write + Roles tab |
| Toast | `showToast` (+desc line) | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Area Detail drawer (P-02, 4 tabs) | 920px | `mountViewDrawer()`/`renderViewDrawer()` — header + `setViewTab` (overview/heads/codes/audit via `avOverviewTab`/`avHeadsTab`/`avCodesTab`/`avAuditTab`) | 50 |
| Create-area drawer | 680px | `openForm('area')`/`renderAreaForm()` — geography cascade + postal auto | 50 |
| Add-head modal | 560px | `openModalBox('addhead')`/`renderAddHeadModal()` — ERP search + active guard | 60 |
| Create-code modal | 560px | `openModalBox('createcode')`/`renderCreateCodeModal()` — Active-area select + 4-digit | 60 |
| Add-director modal | 560px | `openModalBox('adddirector')`/`renderAddDirectorModal()` — ERP search + active guard | 60 |
| Confirm modal | 460px | `openConfirm`/`renderConfirmModal` — remove head/director | 60 |

## §7 Interaction Spec
- **Deactivate guard ⭐:** `toggleAreaStatus(id)` — Active & `areaCodes(id).length>0` → toast.error "ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" (desc "กรุณาย้ายหรือลบโค้ดที่ใช้งานอยู่ก่อน") + ไม่เปลี่ยนสถานะ · Inactive→Active เสมอได้ · Active→Inactive (codes=0) → "เปลี่ยนสถานะสำเร็จ" (BR-01)
- **Geography cascade ⭐:** `setAreaProvince` → reset+populate อำเภอ · `setAreaDistrict` → reset+populate ตำบล · `setAreaSub` → postal auto-fill (getPostalCode) · child disabled จนเลือก parent ("กรุณาเลือกจังหวัดก่อน"/"กรุณาเลือกอำเภอก่อน") (BR-02)
- **4-digit code ⭐:** `submitCreateCode` — `^\d{4}$` (ไม่ผ่าน "รูปแบบหมายเลขโค้ดไม่ถูกต้อง" desc "กรอกตัวเลข 4 หลัก เช่น 0123") · area select = Active เท่านั้น · no area "กรุณาเลือกพื้นที่" · success "สร้างโค้ดสำเร็จ"
- **Active-employee guard ⭐:** `submitAddHead`/`submitAddDirector` — no selection "กรุณาเลือกพนักงาน" · status≠active "พนักงานไม่active" (desc "ไม่สามารถเพิ่มพนักงานที่ไม่ได้ใช้งาน…") · success "เพิ่มหัวหน้าพื้นที่สำเร็จ"/"เพิ่ม Director สำเร็จ" (BR-06)
- **RBAC write-gate ⭐:** `canWrite` ซ่อน/disable ปุ่ม write + Roles tab · CURRENT_ROLE='System Admin' (demo) → เห็นทั้งหมด (BR-07)
- **Remove confirm:** `askRemoveHead/askRemoveDirector` → `openConfirm` → `confirmYes` → "ลบหัวหน้าพื้นที่สำเร็จ"/"ลบ Director สำเร็จ"
- **Audit append:** `pushAudit` (ทุก mutation) · Esc chain (`closeTopDrawer`) · Render preservation (`preserveState/restoreState`) · Row click=view

## §8 State-Driven UI Matrix
| Entity | State | Pill | พฤติกรรม |
|---|---|---|---|
| Area | Active | เปิดใช้งาน(เขียว) | toggle→Inactive (guard codes>0) · edit |
| Area | Inactive | ปิดใช้งาน(เทา) | toggle→Active (เสมอ) · code create ไม่เลือกได้ |
| Code | EMPTY | ว่าง(เทา) | assign → OCCUPIED |
| Code | OCCUPIED | ใช้งานอยู่(เขียว) | มี assigned employee · unassign → EMPTY |
| Role gate | SA/Director | — | write + Roles tab visible |
| Role gate | Head/Officer/Audit | — | read-only · Roles tab ซ่อน |

## §9 Microcopy (verbatim)
**Top tabs:** `Areas` · `Roles` · **Detail tabs:** `Overview`/`ภาพรวม` · `Area Heads` · `Extension Codes` · `Audit` · **Roles sub-tabs:** `Directors` · `Area Heads` · `Extension Officers`
**ปุ่ม:** `สร้างพื้นที่` · `Export CSV` · `แก้ไข` · `เปิดใช้งาน`/`ปิดใช้งาน` · `เพิ่มหัวหน้าพื้นที่` · `Create Code`/`สร้าง Extension Code` · `เพิ่ม Director` · `เพิ่ม` · `ลบ` · `ยืนยัน` · `ยกเลิก` · `ปิด` · `เปิด`
**Area status:** `เปิดใช้งาน`(Active) · `ปิดใช้งาน`(Inactive) · **Code status:** `ว่าง`(EMPTY) · `ใช้งานอยู่`(OCCUPIED)
**Toast success:** `เปลี่ยนสถานะสำเร็จ` · `สร้างพื้นที่สำเร็จ` · `เพิ่มหัวหน้าพื้นที่สำเร็จ` · `ลบหัวหน้าพื้นที่สำเร็จ` · `สร้างโค้ดสำเร็จ` · `เพิ่ม Director สำเร็จ` · `ลบ Director สำเร็จ` · `กำลังเตรียมไฟล์ CSV`
**Guard/validation:** `ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้` (desc `กรุณาย้ายหรือลบโค้ดที่ใช้งานอยู่ก่อน`) · `รูปแบบหมายเลขโค้ดไม่ถูกต้อง` (desc `กรอกตัวเลข 4 หลัก เช่น 0123`) · `กรุณาเลือกพื้นที่` · `กรุณาเลือกพนักงาน` · `พนักงานไม่active` (desc `ไม่สามารถเพิ่มพนักงานที่ไม่ได้ใช้งานเป็นหัวหน้าพื้นที่`)
**Empty:** `ยังไม่มีพื้นที่` · `ยังไม่มีหัวหน้าพื้นที่` · `ยังไม่มี Extension Codes ในพื้นที่นี้`
**Create-area cascade:** `— เลือกจังหวัด —`/`— เลือกอำเภอ/เขต —`/`— เลือกตำบล/แขวง —` · help `กรุณาเลือกจังหวัดก่อน`/`กรุณาเลือกอำเภอก่อน` · postal `เติมอัตโนมัติจากตำบล`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `state.areas` seed | API-01 GET /areas |
| `submitArea()` | API-02 POST (FN-02, geography) |
| `toggleAreaStatus()` ⭐ | API-05 toggle (FN-04 deactivate guard) |
| `submitAddHead()`/`removeHead()` | API-H1/H2 (FN-H, active-employee) |
| `submitCreateCode()` ⭐ | API-C1 (FN-C, 4-digit + Active area) |
| `submitAddDirector()`/`removeDirector()` | API-D1/D2 (FN-D) |
| `empOptions/findEmp` (ERP search) ⭐ | API-ERP (ENG-EXT-ERP read) |
| `provinceName/districtsOf/subdistrictsOf/findSub` | API-GEO (ENG-GEO cascade) |
| `pushAudit()`/`avAuditTab` | API-A1 (FN-AUDIT append) |
| `canWrite` gate | FN-RBAC (server enforce) |
| **Areas scope** | area_id → Farmer/Quota (F-AGM-001/002) |
Mock: **5 areas** AR-0001..0005 (4 Active/1 Inactive · จังหวัด กทม/เชียงใหม่/เชียงราย) · **7 extension codes** (EMPTY/OCCUPIED) · **3 area heads** · **1 director** · **7 ERP employees** (1 inactive) · **4 audit** (AR-0001)

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 list | renderAreasPage → #page-content | §4 |
| 01_UI P-02 detail 4-tab | renderViewDrawer + setViewTab + av*Tab | §6 |
| 01_UI P-03 roles 3-tab | renderRolesPage + setRoleTab + rolesDirectors/Heads/OfficersView | §6 |
| 01_UI OV create-area | openForm('area') + geography cascade | §6/§7 |
| 01_UI OV add-head/create-code/add-director | openModalBox + submit* | §6/§7 |
| 02_API A05 (guard) | toggleAreaStatus | §7/§10 |
| 02_API C1 (4-digit) | submitCreateCode | §7/§10 |
| 02_API H1/D1 (active) | submitAddHead/Director | §7/§10 |
| 03_LOGIC FN-RBAC | canWrite gate | §7 |
| 03_LOGIC FN-GEO | cascade | §7 |
| 05_RULES BR-01 guard | toggleAreaStatus | §8 |
| 06_TESTS AC-01..27 / XT-01..05 | ครบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | ERP employees + geography อ่านจาก mock | HTML sim | ระบบจริง = ENG-EXT-ERP + ENG-GEO |
| D-03 | RBAC = hide/disable UI (CURRENT_ROLE demo) | HTML sim | ระบบจริง = server enforce 403 (OQ-03) |
| D-04 | edit area / assign-unassign-reassign officer | stub/no-op | ระบบจริง = full workflow (OQ-01) |
| D-05 | heads_count/codes_count = snapshot field | design | ระบบจริง = derived reconcile (C-04) |
| D-06 | audit before/after snapshot | HTML minimal | ระบบจริง = diff view (OQ-02) |
| D-07 | T3 code-only reverse — labels ตาม code | reverse-note | invariants §7 C-01 |
| D-08 | Extension Officer = code assignment (ไม่มี role table) | AS-BUILT | invariants §7 C-02 (BR-05) |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (React/Vite shadcn prototype): คงไว้ 100% (LOCK-01) — 2-tab (Areas/Roles), area detail 4 tabs, geography cascade + postal auto, deactivate guard, 4-digit code + Active-area, EMPTY/OCCUPIED, RBAC write-gate SA/Director, active-employee-only, audit trail, optimistic+idempotent · เปลี่ยน: in-page tab-switch detail → CUBE drawer 920px + route · dialogs modal → CUBE modal · CI shadcn slate → CUBE Warm Light · เพิ่ม stats + audit governance

## §13 💡 ข้อเสนอ
1. Edit area + assign/unassign/reassign officer เต็มรูป (OQ-01)
2. RBAC role-switcher (demo) + server 403 enforcement (OQ-03)
3. Audit before/after snapshot diff view (OQ-02)
4. Area deep-link → Farmer/Quota ที่ scope ด้วย area_id (OQ-04)
5. Bulk activate/deactivate + bulk code-move (แก้ deactivate guard workflow)
