# UI BRIEF — F-TMP-002 หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (AS-BUILT)

> ใช้คู่: **HTML `feature.html` (source of truth)** + **FRD_F-TMP-002_Pack** + บรีฟนี้ (design intent + แผนที่โค้ด)
> ทุกบรรทัดสกัดจาก HTML — anchor = selector / function / ข้อความจริง · ข้อเสนอที่ไม่ใช่ของจริงอยู่ §13 เท่านั้น

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` รอบ 1 (kit html-generator-v9.4 · archetype `Q-form` · `__QA__` มี) |
| Gate ของ HTML | audit.sh FAIL 0 (WARN 3 จาก kit) · self_audit PASS · e2e_standard **ยังไม่รัน (NO-BROWSER)** · smoke node vm error 0 |
| FRD | `FRD_F-TMP-002_Pack` v1.0 — paired ✅ (frd_lint BLOCK 0 · WARN 0) |
| มติ | DECISIONS.lock 20 ข้อ (AI-DEFAULT 14 · VALID 6) |
| Print | `print/form.tpl.html` + `print-spec §2` (thai-doc v2.2 · Replica R9 + R10 2 หน้า) |
| Drift | business drift 0 · HTML-only (prototype) 4 — §11 |
| วันที่ | 2026-10-10 |

## §1 Design Tokens AS-BUILT
| ตัวแปร | ค่า |
|---|---|
| `--c-navy` | `#111111` |
| `--c-navy-2` | `#111111` |
| `--c-primary` | `#FF3B30` |
| `--c-primary-hover` | `#E62E24` |
| `--c-teal` | `#FF9A1F` |
| `--c-teal-light` | `#FFB763` |
| `--c-ink` | `#111111` |
| `--c-mute` | `#54565C` |
| `--c-mute-2` | `#73757B` |
| `--c-mute-3` | `#9A9CA2` |
| `--c-placeholder` | `rgb(180,182,188)` |
| `--z-content` | `1` |
| `--z-sticky` | `10` |
| `--z-shell` | `10` |
| `--z-dropdown` | `30` |
| `--z-backdrop` | `50` |
| `--z-drawer` | `51` |
| `--z-modal` | `60` |
| `--z-popover` | `70` |
| `--z-toast` | `80` |
| `--c-line` | `#DEDAD4` |
| `--c-line-2` | `#E9E5E0` |
| `--c-line-3` | `#F1EEEA` |
| `--c-bg-off` | `#FAF8F5` |
| `--c-success` | `#1F9D55` |
| `--c-warning` | `#E8870F` |
| `--c-danger` | `#E62E24` |
| `--sidebar-w` | `232px` |
| `--shell-h` | `52px` |
| `--fs-h1` | `22px` |
| `--fs-h2` | `17px` |
| `--fs-h3` | `15px` |
| `--fs-body` | `14px` |
| `--fs-sub` | `13px` |
| `--fs-meta` | `12px` |
| `--fs-cap` | `11px` |
| `--fs-kpi` | `28px` |
| `--sp-xs` | `4px` |
| `--sp-sm` | `8px` |
| `--sp-md` | `12px` |
| `--sp-lg` | `20px` |
| `--sp-xl` | `28px` |
| `--r-xs` | `4px` |
| `--r-sm` | `6px` |
| `--r-md` | `8px` |
| `--r-lg` | `12px` |
| `--r-full` | `999px` |

**Font:** Noto Sans Thai + Satoshi (Google Fonts / Fontshare) · **Icons:** Lucide 0.469.0 (multi-CDN loader · `renderIcons()`) · **PDF:** Sarabun

**z-index map (ตามที่ประกาศ):**
| z | ใช้กับ |
|---|---|
| `var(--z-shell)` | `.sidebar` |
| `var(--z-sticky)` | `.shell-bar` |
| `var(--z-dropdown)` | `.user-menu` |
| `var(--z-sticky)` | `.table-wrap thead th` |
| `var(--z-popover)` | `* เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .` |
| `var(--z-backdrop)` | `.ss-list` |
| `var(--z-popover)` | `verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body) */ .ss-list.` |
| `3` | `.table-scroll.is-sticky thead th` |
| `2` | `.stepper-circle` |
| `1` | `.stepper-item:not(:last-child)::after` |
| `var(--z-backdrop)` | `.drawer-backdrop` |
| `var(--z-drawer)` | `.drawer` |
| `var(--z-backdrop)` | `รมีปุ่ม action หลัก */  .modal-backdrop` |
| `var(--z-toast)` | `.toast` |
| `var(--z-sticky)` | `.wizard-footer` |
| `var(--z-dropdown)` | `.info-tip::after` |
| `var(--z-modal)` | `.modal-backdrop` |
| `var(--z-drawer)` | `#drawer` |
| `var(--z-backdrop)` | `#drawerBackdrop` |
| `var(--z-toast)` | `#toast` |
| `var(--z-popover)` | `.row-menu` |

## §2 Route Map
| Route | หน้าที่ | เปิดด้วย | Refresh-safe |
|---|---|---|---|
| `#/csat-gt` | P-01 รายการ | sidebar `.sb-item` · `closeDrawer()` | ✓ `applyRoute()` |
| `#/csat-gt/view/:id` | P-03 ดูเอกสาร | `rowClick()` · `openView()` | ✓ เปิด drawer ถ้า `canSee()` — ไม่มีสิทธิ์ = ไม่เปิด |
| `#/csat-gt/create` | P-02 สร้าง | `startWizard()` | ✓ |
| `#/csat-gt/edit/:id` | P-02 แก้ร่าง | `startWizard('id')` | ✓ เฉพาะร่างของตน |
route ประกอบจากค่าคงที่ `BASE = 'csat-gt'` ผ่าน `go()` · `navigate()` · `getRoute()` · `hashchange → applyRoute()`

## §3 Layout Shell
| ส่วน | Anchor | AS-BUILT |
|---|---|---|
| Sidebar | `.sidebar` · `.sb-module[data-module="sales"]` · `.sb-item` | Sales › สรุปความพึงพอใจ GT · badge `#sbBadge` = จำนวนรอฉันพิจารณา |
| Topbar | `.shell-bar` · `.breadcrumb` | Core › Sales › สรุปความพึงพอใจ GT · กระดิ่ง `#notifBtn` |
| User chip | `.user-chip` · `#ucAv` (วงกลม icon `.avatar.pc`) · `#userMenu` · `#personaList` | สลับผู้ใช้เดโม `switchPersona()` (prototype-only) |
| Content | `#page-content` | `renderPage()` |

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
```
.page-fill
 ├ .ph  (.ph-title · .ph-sub + .ph-badge ≤3: "n รายการ" · "รออนุมัติ n" · "รอฉันพิจารณา n" — ค่า 0 ซ่อน)
 │  └ .ph-actions: ส่งออก CSV (`exportCSV()`) · สร้างแบบสรุป `#btnCreate` (`startWizard()` · disabled เมื่อ DOC.active=false)
 └ .card.list-card
    ├ .filter-bar: `#fq` ค้นหา (`onQ()`) · search-select `fst` สถานะ · `fper` เดือน · รีเซ็ต (`resetFilters()`)
    ├ .table-wrap > table.table  (sort `sortTh()`/`sortBy()` · แถว `rowClick()` · ⋮ `openRowMenu()`)
    └ .table-footer (`pager()` · page-size 10/25/50 `setPs()` · `goPage()`)
```
### P-02 Wizard (`renderWizard()` · `.drawer-panel.wide`)
```
.dw-head (eyebrow · .dw-title · `stepper()` 3 ขั้น)
.drawer-body
 ├ ขั้น 1 `wizMain()`: .wz-split
 │   ├ .wz-card ① ประจำเดือน (search-select `wper` → `setPeriod()`)
 │   ├ .wz-card ② `scoreEditor()` ×3 → table.sc-tbl (input.sc-in inputmode=numeric → `setCnt()` soft update) + .sc-foot %
 │   ├ .wz-card ③ ลูกค้า: ปุ่ม `pullCustomers()` · `custRows()` (.cu-row + search-select `cu{i}` → `setCust()`) · `addCust()` · `removeCust()`
 │   └ `sumCard()` (.wz-sum sticky: ผู้จัดทำ · ผู้รับรอง DOA · เดือน · % 3 ด้าน · `#sumTotal` · `#sumLevel`)
 ├ ขั้น 2 `wizAttach()` (.upload-zone · `pickFiles()` · `removeFile()`)
 └ ขั้น 3 `wizReview()` (.review-card ×4 · `csatBox()` · `custTable()`)
.dw-footer: ย้อนกลับ (`wizBack()`) · ยกเลิก · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งอนุมัติ `#btnSaveSubmit` (`saveAndSubmit()`)
```
### P-03 View (`renderViewDrawer()` · drawer 920)
```
.dw-head: .doc-ident (eyebrow "แบบสรุปความพึงพอใจ GT (CSAT)" · .dw-title.mono เลขที่ · `docPill()` · .dw-sub เดือน + % โดยรวม) · .dw-actions ตามสถานะ · พิมพ์/ดาวน์โหลด (`genPdf()`) · ปิด
.drawer-tabs (`tabBtn()`): รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
.dw-footer: แก้ไขล่าสุด … · ปิด
```

## §5 Component Inventory
| Component | Anchor | States |
|---|---|---|
| Score table (แก้ได้) | `scoreEditor()` · `.sc-tbl` · `.sc-in` | default · focus · invalid `.is-bad` (ไม่ใช่จำนวนเต็ม ≥ 0 / ทั้งเอกสารว่าง) · disabled — ไม่มี |
| Score table (อ่าน) | `scoreTableView()` | ค่าว่างแสดง "—" |
| % ต่อด้าน / โดยรวม | `secCalc()` · `overall()` · `pctTxt()` · `bandOf()` · `levelPill()` | null → "—" · pill สีตามช่วง (success/warning/danger) |
| Customer row | `.cu-row` · `custRows()` | ปกติ · `.is-bad` + `.field-error` (เลือกลูกค้า / ลูกค้าซ้ำกับแถวที่ n) · ป้าย "ต่ำกว่าเกณฑ์" |
| Search select | `searchSelectHTML()` · `initSearchSelect()` | เปิด/ปิด · ค้นหา · ล้าง · keyboard |
| Person chip | `empChip()` · `.avatar.pc` | วงกลม icon + role + ชื่อ |
| Sign progress | `renderSignProgress()` · `.sign-prog` · `.sp-bar` | ร่าง "—" · x/y |
| Status pill | `docPill()` | ร่าง · รออนุมัติ · อนุมัติแล้ว · ยกเลิก |
| Empty | `emptyStateHTML()` · `.empty-mini` | list: ไม่มีข้อมูล / ไม่พบรายการที่ค้นหา · sub-table: ยังไม่มีรายชื่อลูกค้า |
| Loading | `busyLabel()` · `.spin` | "กำลังบันทึก…" ปุ่ม disabled |

## §6 Overlay Registry
| Overlay | Anchor | ขนาด | เปิด | ปิด / dismiss |
|---|---|---|---|---|
| drawer (view) | `#drawer.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · backdrop **mousedown** (`drawerBackdropDown()`) |
| drawer (wizard) | `#drawer.drawer-panel.wide` | 1290 | `startWizard()` | dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" ก่อนปิด |
| modal | `#modalBackdrop` · `#modal` (`.is-lg` สำหรับส่ง) | 520 / lg | `openModalCfg()` | ปุ่ม · Esc · backdrop mousedown (`modalBackdropDown()` — มีเหตุผล/ความเห็นค้าง = ไม่ปิด) |
| row-menu | `.row-menu` (portal `#overlay-root`) | 180 | `openRowMenu()` | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| user-menu | `#userMenu` | — | `toggleUserMenu()` | คลิกนอก |
| ss-list | search-select list (portal) | ตาม input | focus | เลือก · คลิกนอก · Esc |
| toast | `#toast` | — | `showToast()` | หายเองราว 2.8 วินาที |

## §7 Interaction Spec
- Esc chain (handler ใน BASE-KIT `keydown`): modal → drawer (search-select ปิดก่อนใน `ssOnKey`) · drawer wizard dirty → modal ทิ้งข้อมูล
- Soft update: `setCnt()` อัปเดต `#rt-…` `#cs-…` `#ct-…` `#sp-…` `#sum-…` `#sumTotal` `#sumLevel` โดยไม่ render ใหม่ (focus ไม่หลุด)
- Render preservation: `render()` ใช้ `preserveRenderState()` / `restoreRenderState()`
- Row menu render icon เฉพาะในเมนู (`data-rmic`) กันคลิกทะลุ
- PDF: iframe `.pdf-frame` srcdoc · `fitPdf()` สูงขั้นต่ำ 2 หน้า · ดาวน์โหลด/พิมพ์ผ่าน iframe ซ่อน `.pdf-gen`

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว drawer (ผู้ใช้) | เมนู ⋮ |
|---|---|---|---|
| draft | ร่าง (pill-muted) | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ | ดูรายละเอียด · แก้ไข (เจ้าของ) · พิมพ์ · ยกเลิกเอกสาร (เจ้าของ/admin) |
| pending | รออนุมัติ (pill-warning) | ผู้พิจารณาขั้นปัจจุบัน: ไม่อนุมัติ · อนุมัติ (`.btn-success`) · เจ้าของ/admin: ยกเลิกเอกสาร | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว (pill-success) | — (ล็อก) | ดูรายละเอียด · พิมพ์ |
| cancelled | ยกเลิก (pill-muted) | — | ดูรายละเอียด · พิมพ์ |
draft ที่ถูกไม่อนุมัติ: แบนเนอร์ "ไม่อนุมัติ — กลับเป็นร่าง (เลขเดิม): เหตุผล" (`viewBanner()`)

## §9 Microcopy (verbatim)
### Toast
| ข้อความ | ชนิด |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | toast |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | toast |
| แก้ไขได้เฉพาะร่างของตัวเอง | toast |
| กรุณากรอกข้อมูลให้ครบถ้วน | toast |
| บันทึกร่างแล้ว · | toast |
| ส่งอนุมัติแล้ว · | toast |
| อนุมัติแล้ว · | toast |
| ส่งออก | toast |
| สลับเป็น | toast |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | toast |
### ข้อความอื่นในหน้าจอ (สกัดจาก HTML)
- % โดยรวม
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · สั่งซื้อ
- · อนุมัติแล้ว ล็อกแก้ไข
- · เอกสารจะกลับเป็นร่าง (เลขเดิม) ให้ผู้จัดทำแก้แล้วส่งใหม่
- · แจ้งฝ่ายขาย: ผลต่ำกว่า
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรอกคะแนนอย่างน้อย 1 ด้าน
- กรอกคะแนนเพื่อดูผลการแปลผล
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลับเป็นร่าง (เลขเดิม)
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขอข้อมูลเพิ่มเติม
- ขั้นทดสอบ
- ขาย GT ภาคกลาง
- ขาย GT ภาคเหนือ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลระบบ
- ข้อมูลหลักแบบสรุป
- ข้าม
- ครั้ง
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
- ค้นหา...
- ค้นหาลูกค้า GT
- ค้นหาเลขที่ / ผู้จัดทำ / เดือน / ลูกค้า
- จำนวนการสั่งซื้อ —
- จำลอง ดูแลดี
- ชนิดไฟล์ไม่รองรับ
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวอย่าง บริหารงาน
- ตัวเลขไม่ตรงกับแบบสำรวจ
- ตุลาคม
- ต่ำกว่า 60%
- ต้อง
- ต้องปรับปรุง
- ถึง
- ทดสอบ รักงาน
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกสถานะ
- ทุกเดือน
- ธ.ค.
- ธันวาคม
- ธุรการขาย
- น้อย
- บริษัท ตัวอย่าง จำกัด
- บริหาร
- บันทึกร่างแล้ว ·
- ประกอบ ตั้งใจ
- ประจำเดือน
- ประวัติ
- ประวัติ (append-only)
- ปานกลาง
- ปิด
- ผลการแปลผล
- ผู้จัดการทั่วไป
- ผู้จัดทำ
- ผู้รับรอง (ค่าเริ่ม)
- ผู้ส่ง
- ผู้อำนวยการสายงานการขาย
- พ.ค.
- พ.ย.
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ภาคกลาง
- ภาคเหนือ
- มกราคม
- มาก
- มากที่สุด
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีคำตอบในด้านนี้
- ยังไม่มีรายชื่อลูกค้า
- ยังไม่ส่ง
- ย้อนกลับ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบบ
- รายการ
- รายชื่อลูกค้าไม่ครบ
- รายชื่อลูกค้าไม่ครบ — ขาดร้านที่สั่งซื้อปลายเดือน
- รายละเอียด
- รีเซ็ต
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือรีเซ็ตตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ลูกค้าซ้ำกับแถวที่
- ลูกค้าที่ประเมิน
- ลูกค้าพึงพอใจในระดับปานกลาง
- ลูกค้ามีความพึงพอใจสูง
- ลูกค้าอาจมีความไม่พึงพอใจ
- วันที่ ........./........./.........
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมมติ ใจดี
- สรุปผลการประเมิน
- สรุปแบบสำรวจ FM-SAL-10 ก.ค. 2569.xlsx
- สร้าง PDF
- สร้างซ้ำเดือนเดียวกัน
- สร้างซ้ำเดือนเดียวกัน — ใช้ CSM-2569-0006
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบสรุป
- สร้างแบบสรุปผลการประเมินความพึงพอใจของเดือนแรก
- สลับเป็น
- สาธิต มั่นคง
- สายงานการขาย
- สิงหาคม
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่อนุมัติ เอกสารจะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หน่วยงาน
- หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade
- อนุมัติ
- อนุมัติ (ขั้น
- อนุมัติแล้ว
- อนุมัติแล้ว ·
- เดือนปัจจุบัน
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกตอนส่งอนุมัติ
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกลูกค้า
- เลือกลูกค้าที่ประเมินอย่างน้อย 1 ราย
- เลือกเดือน
- เลือกเดือนก่อน
- เลือกเดือนผิด
- เหตุผลที่ยกเลิก
- เหนือ
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบสรุปความพึงพอใจ General Trade
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- ใส่เป็นจำนวนเต็ม 0 ขึ้นไป (จำนวนลูกค้า)
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อมูล
- ไม่มีลูกค้าเพิ่ม
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ — กลับเป็นร่าง ·
- ไม่ใช้เอกสารนี้แล้ว
- — คุณเป็นผู้พิจารณาเอกสารนี้

## §10 Data Binding & BACKEND anchors
| Prototype | API (02_API) | หมายเหตุ |
|---|---|---|
| `RECS` · `listRows()` · `canSee()` | API-01/02/10 | FN-10 |
| `persist()` (ENG-DOC-NUM ตอนบันทึกครั้งแรก) | API-03/04 | FN-01..03 |
| `pullCustomers()` · `orderCount()` | API-05 | FN-04 · เกณฑ์จาก `CFG.min_orders` (SalesConfig) |
| `openSubmit()` · `confirmSubmit()` · `resolveDoa()` · `MOCK_DOA_RESOLVED` (DOA-ENGINE-HOOK) | API-06 | FN-05 |
| `confirmApprove()` · `confirmReason()` | API-07/08 | FN-06/07 · ENG-NOTIFY |
| `docPrintData()` · `tplRender()` · `tplSignRows()` · `DOC_TPL` | API-09 | FN-08 · parity กับ render_doc.py |
| `CFG` (scale · bands · sections · min_orders) | SalesConfig (อ่าน) | ห้าม hardcode ในระบบจริง |
| `DOC.active` | F-DOCCFG status | |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/05 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/06..09 | `renderViewDrawer()` |
| §6 modal | 01_UI M-01..05 · 05 VR-05/06 | `renderModal()` |
| §5 % | 05 BR-01..05 | `secCalc()` · `overall()` |
**Drift Log:** business 0 · HTML-only (prototype-only ไม่ต้องสร้าง): `window.__QA__` · `switchPersona()` สลับผู้ใช้ · `S.sim` / `commitRejected()` จำลอง API ล้ม · `orderCount()` mock (ระบบจริงใช้ API-05)

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (รอบแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- กันสร้างซ้ำเดือน/หน่วยงาน (OQ-06) · ดึงคะแนนจากแบบสำรวจ FM-SAL-10 อัตโนมัติ (OQ-05) · กราฟแนวโน้ม CSAT 12 เดือนใน Report area
