# UI BRIEF — F-TMP-008 สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (AS-BUILT)

> ใช้คู่: **HTML `feature.html` (source of truth)** + **FRD_F-TMP-008_Pack** + บรีฟนี้ (design intent + แผนที่โค้ด)
> ทุกบรรทัดสกัดจาก HTML — anchor = selector / function / ข้อความจริง · ข้อเสนอที่ไม่ใช่ของจริงอยู่ §13 เท่านั้น

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` รอบ 1 (kit html-generator-v9.4 · archetype `Q-form` · `__QA__` มี) |
| Gate ของ HTML | audit.sh FAIL 0 (WARN 4 จาก kit/ไม่มีผู้อนุมัติ) · self_audit PASS · e2e_standard **ยังไม่รัน (NO-BROWSER)** · smoke node vm error 0 |
| FRD | `FRD_F-TMP-008_Pack` v1.0 — paired ✅ (frd_lint BLOCK 0 · WARN 0) |
| มติ | DECISIONS.lock 20 ข้อ (AI-DEFAULT 12 · VALID 8) · ไม่มีการอนุมัติ (DEC-03) |
| Print | `print/form.tpl.html` + `FM-SAL-07_print-spec.md` (thai-doc v2.2 · Replica R9 + R10 2 หน้า) |
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

**Font:** Noto Sans Thai + Satoshi · **Icons:** Lucide (multi-CDN loader · `renderIcons()`) · **PDF:** Sarabun · สี % ต่อช่องทางใช้ token `--c-success` / `--c-warning` / `--c-danger` ผ่าน `BAND_CLS`

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
| `var(--z-portal)` | `.bd-pop` |

## §2 Route Map
| Route | หน้าที่ | เปิดด้วย | Refresh-safe |
|---|---|---|---|
| `#/csat-mt` | P-01 รายการ | sidebar `.sb-item` · `closeDrawer()` | ✓ `applyRoute()` |
| `#/csat-mt/view/:id` | P-03 ดูเอกสาร | `rowClick()` · `openView()` | ✓ เปิด drawer ถ้า `canSee()` — ไม่มีสิทธิ์ = ไม่เปิด |
| `#/csat-mt/create` | P-02 สร้าง | `startWizard()` | ✓ |
| `#/csat-mt/edit/:id` | P-02 แก้ร่าง | `startWizard('id')` | ✓ เฉพาะร่างของตน |
route ประกอบจากค่าคงที่ `BASE = 'csat-mt'` + `ROUTES` ผ่าน `go()` · `navigate()` · `getRoute()` · `hashchange → applyRoute()`

## §3 Layout Shell
| ส่วน | Anchor | AS-BUILT |
|---|---|---|
| Sidebar | `.sidebar` · `.sb-module[data-module="sales"]` · `.sb-item` | Sales › สรุปความพึงพอใจ MT · badge `#sbBadge` = จำนวนร่างของฉันที่ยืนยันได้ |
| Topbar | `.shell-bar` · `.breadcrumb` | Core › Sales › สรุปความพึงพอใจ MT |
| User chip | `.user-chip` · `#ucAv` (วงกลม icon `.avatar.pc`) · `#userMenu` · `#personaList` | สลับผู้ใช้เดโม `switchPersona()` (prototype-only) |
| Content | `#page-content` | `renderPage()` |

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
```
.page-fill
 ├ .ph  (.ph-title · .ph-sub + .ph-badge ≤2: "n รายการ" · "ร่าง n" — ค่า 0 ซ่อน)
 │  └ .ph-actions: ส่งออก CSV (`exportCSV()`) · สร้างสรุปผล `#btnCreate` (`startWizard()` · disabled เมื่อ DOC.active=false)
 └ .card.list-card
    ├ .filter-bar: `#fq` ค้นหา (`onQ()`) · search-select `fst` สถานะ · `fyr` ปี · รีเซ็ต (`resetFilters()`)
    ├ .table-wrap > table.table  (sort `sortTh()`/`sortBy()` · แถว `rowClick()` · ⋮ `openRowMenu()` · ลายเซ็น `renderSignProgress()`)
    └ .table-footer (`pager()` · page-size 10/25/50 `setPs()` · `goPage()`)
```
### P-02 Wizard (`renderWizard()` · `.drawer-panel.wide`)
```
.dw-head (eyebrow · .dw-title · `stepper()` 4 ขั้น)
.drawer-body
 ├ ขั้น 1 `wizMain()`
 │   ├ .wz-card ① `#fRound` ครั้งที่ (`setF1()`) · `#fAssess` / `#fSumm` วันที่ `bedateHTML()` → `pickAssess()` / `pickSumm()` · เตือนครั้งที่ซ้ำ `dupRound()`
 │   └ .wz-card ② `scoreEditor()` → `#mxEdit` table.mx-tbl (input.mx-in → `setScore()` soft update `#mt-n` `#mp-n`) · .mx-legend · `sumLine()` (`#sumLine`)
 ├ ขั้น 2 `wizSummary()` (.grp ×3 รายชื่อกลุ่ม + textarea → `setNote()` · `#recList` .rec-row → `setRec()` · `addRec()` · `removeRec()`)
 ├ ขั้น 3 `wizAttach()` (.upload-zone · `#mtsFile` · `pickFiles()` · `removeFile()`)
 └ ขั้น 4 `wizReview()` (.review-card ×5 · `matrixView()` · `groupsView()` · `recsView()`)
.dw-footer: ย้อนกลับ (`wizBack()`) · ยกเลิก · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและยืนยันสรุป `#btnSaveFinal` (`saveAndFinalize()`)
```
### P-03 View (`renderViewDrawer()` · drawer 920)
```
.dw-head: .doc-ident (eyebrow "สรุปความพึงพอใจลูกค้า MT" · .dw-title.mono เลขที่ · `docPill()` · .dw-sub ครั้งที่ + ผ่านมาตรฐาน x/y) · .dw-actions ตามสถานะ · พิมพ์/ดาวน์โหลด (`genPdf()`) · ปิด
.drawer-tabs (`tabBtn()`): รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
.dw-footer: แก้ไขล่าสุด … · ปิด
```

## §5 Component Inventory
| Component | Anchor | States |
|---|---|---|
| Score matrix (แก้ได้) | `scoreEditor()` · `.mx-tbl` · `.mx-in` | default · focus · invalid `.is-bad` (ไม่ใช่ 1–5 / ช่องทางกรอกไม่ครบตอนยืนยัน) |
| Score matrix (อ่าน) | `matrixView()` | ค่าว่างแสดง "—" · แถวรวม + % สีตามผล |
| คำนวณช่องทาง | `chCalc()` · `allCalc()` · `pctTxt()` · `groupsOf()` · `bandPill()` | none "ไม่ได้ประเมิน" · partial "ยังไม่ครบ" · done % + pill |
| ภาพรวมโดยสรุป | `groupsView()` · `.grp` · `.grp-txt` | กลุ่มต่ำกว่า 80% `.is-alert` (ตัวหนาแดง) · ไม่มีช่องทาง "—" |
| ข้อเสนอแนะ | `recsView()` · `.rec-row` | ว่าง → `.empty-mini` "ยังไม่มีข้อเสนอแนะ" |
| วันที่ พ.ศ. | `bedateHTML()` · `.bedate` | เลือก · วันนี้ · min/max |
| Search select | `searchSelectHTML()` · `initSearchSelect()` | เปิด/ปิด · ค้นหา · ล้าง · keyboard |
| Person chip | `empChip()` · `.avatar.pc` | วงกลม icon + role + ชื่อ |
| Sign progress | `renderSignProgress()` · `.sign-prog` · `.sp-bar` | ร่าง "—" · 1/1 |
| Status pill | `docPill()` | ร่าง · สรุปแล้ว · ยกเลิก |
| Empty | `emptyStateHTML()` · `.empty-mini` | list: ไม่มีข้อมูล / ไม่พบรายการที่ค้นหา |
| Loading | `busyLabel()` · `.spin` | "กำลังบันทึก…" ปุ่ม disabled |

## §6 Overlay Registry
| Overlay | Anchor | ขนาด | เปิด | ปิด / dismiss |
|---|---|---|---|---|
| drawer (view) | `#drawer.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · backdrop **mousedown** (`drawerBackdropDown()`) |
| drawer (wizard) | `#drawer.drawer-panel.wide` | 1290 | `startWizard()` | dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" ก่อนปิด |
| modal | `#modalBackdrop` · `#modal` (`.is-lg` สำหรับยืนยันสรุป) | 520 / lg | `openModalCfg()` | ปุ่ม · Esc · backdrop mousedown (`modalBackdropDown()` — มีเหตุผลค้าง = ไม่ปิด) |
| row-menu | `.row-menu` (portal `#overlay-root`) | 180 | `openRowMenu()` | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| ปฏิทิน | `.bd-pop` (portal) | 280 | `bdToggle()` | เลือกวัน · Esc · คลิกนอก |
| user-menu | `#userMenu` | — | `toggleUserMenu()` | คลิกนอก |
| toast | `showToast()` | — | `showToast()` | หายเอง |

## §7 Interaction Spec
- Esc chain: ปฏิทิน/search-select → modal → drawer · drawer wizard dirty → modal ทิ้งข้อมูล
- Soft update: `setScore()` อัปเดตรวม/% ของคอลัมน์นั้น + `sumLine()` โดยไม่ render ใหม่ (focus ไม่หลุด)
- Render preservation: `render()` ใช้ `preserveRenderState()` / `restoreRenderState()`
- Validate: `validateMain(false)` ตอนถัดไป/บันทึกร่าง · `validateMain(true)` + `validateRecs()` ตอนบันทึกและยืนยันสรุป
- PDF: iframe `.pdf-frame` srcdoc · `fitPdf()` · ดาวน์โหลด/พิมพ์ผ่าน iframe ซ่อน `.pdf-gen`

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว drawer (ผู้ใช้) | เมนู ⋮ |
|---|---|---|---|
| draft | ร่าง (pill-muted) | เจ้าของ: ยกเลิก · แก้ไข · ยืนยันสรุป `#btnFinalizeView` | ดูรายละเอียด · แก้ไข (เจ้าของ) · พิมพ์ · ยกเลิกเอกสาร (เจ้าของ/admin) |
| final | สรุปแล้ว (pill-success) | เจ้าของ/admin: ยกเลิกเอกสาร | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร |
| cancelled | ยกเลิก (pill-muted) | — | ดูรายละเอียด · พิมพ์ |
แบนเนอร์ (`viewBanner()`): ร่าง / ยกเลิก + เหตุผล / สรุปแล้วและมีช่องทางต่ำกว่า 80%

## §9 Microcopy (verbatim)
### Toast
| ข้อความ | ชนิด |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | toast |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | toast |
| แก้ไขได้เฉพาะร่างของตัวเอง | toast |
| กรุณากรอกข้อมูลให้ครบถ้วน | toast |
| บันทึกร่างแล้ว · | toast |
| ยืนยันสรุปแล้ว · | toast |
| ยกเลิกเอกสารแล้ว · | toast |
| ส่งออก | toast |
| สลับเป็น | toast |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | toast |
### ข้อความอื่นในหน้าจอ (สกัดจาก HTML)
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · สรุปแล้ว ล็อกแก้ไข
- · เอกสารสรุปแล้วจะถูกปิด ต้องสร้างใบใหม่แทน
- · แจ้งช่องทางต่ำกว่า
- · แจ้งผู้สรุปแล้ว
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรอกคะแนนครบทุกหัวข้ออย่างน้อย 1 ช่องทาง
- กรอกคะแนนผิดช่องทาง
- กรอกคะแนนให้ครบทุกหัวข้อของช่องทางที่ประเมิน (หรือเว้นว่างทั้งคอลัมน์)
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณาระบุครั้งที่
- กรุณาเลือกวันที่
- กันยายน
- การจัดการสต็อกสินค้าและการเติมสินค้า
- การสนับสนุนด้านการตลาดและส่งเสริมการขาย
- การสื่อสารและการให้ข้อมูลข่าวสาร
- การแก้ไขปัญหาและการให้บริการหลังการขาย
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขาย MT
- ขาย MT ภูมิภาค
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลเอกสาร
- ข้อเสนอแนะ
- ครั้งที่
- ครั้งที่ต้องเป็นจำนวนเต็มตั้งแต่ 1
- ครั้งที่นี้ของปีเดียวกันมีอยู่แล้ว — ตรวจอีกครั้ง
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ควร ปรับปรุงบางด้าน เช่น การสื่อสาร หรือความสะดวกในการซื้อสินค้า
- ควร รักษาคุณภาพ และ สร้างกรณีศึกษา (Best Practice)
- ความตรงต่อเวลาในการส่งสินค้า
- ความพึงพอใจโดยรวมต่อบริษัทคู่ค้า
- ความเป็นมืออาชีพของพนักงานขาย/ทีมงาน
- คะแนนต้องเป็นจำนวนเต็ม 1–5
- คะแนนรายช่องทาง
- คุณภาพของสินค้า/บริการ
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่อนข้างต่ำกว่ามาตรฐาน
- ค้นหา...
- ค้นหาเลขที่ / ผู้สรุป / ครั้งที่
- จำลอง ดูแลดี
- จิฟฟี่
- ชนิดไฟล์ไม่รองรับ
- ชื่อฟังก์ชัน
- ช่องทาง
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวอย่าง บริหารงาน
- ติดตามผลซ้ำทุก 6 เดือน เพื่อดูการเปลี่ยนแปลงอย่างชัดเจน
- ตุลาคม
- ต่ำกว่า
- ต่ำกว่ามาตรฐาน
- ต้อง
- ต้องเร่งแก้ไขอย่างเร่งด่วน
- ทดสอบ รักงาน
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกปี
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธุรการขาย
- นำช่องทางที่คะแนนสูงมาเป็นต้นแบบ เพื่อพัฒนาอีกช่องทาง
- บริษัท ตัวอย่าง จำกัด
- บันทึกร่างแล้ว ·
- บิ๊กซี
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ปี
- ผู้สรุป
- ผู้สรุปการประเมิน
- ผ่านมาตรฐาน
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ภาพรวมและข้อเสนอแนะ
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีช่องทางที่กรอกคะแนนไม่ครบ — แก้ไขร่างก่อน
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — ยืนยันสรุปเมื่อกรอกคะแนนครบ (ยืนยันแล้วแก้ไขไม่ได้)
- ยังไม่มีข้อมูล
- ยังไม่มีข้อเสนอแนะ
- ยังไม่มีข้อเสนอแนะ — แก้ไขร่างก่อน
- ยังไม่มีช่องทางที่กรอกคะแนนครบ — แก้ไขร่างก่อน
- ยังไม่ยืนยัน
- ยืนยันสรุป
- ยืนยันสรุปผลประเมิน?
- ยืนยันสรุปเมื่อ
- ยืนยันสรุปแล้ว ·
- ยืนยันสรุปแล้วแก้ไขไม่ได้ — ถ้าผิดต้องยกเลิกแล้วสร้างใบใหม่
- ยืนยันแล้ว
- ย้อนกลับ
- ระบบ
- รายการ
- รายชื่อช่องทางแต่ละกลุ่มมาจากคะแนน (แก้ไม่ได้) · ข้อความแนะนำแก้ได้
- รายละเอียด
- รีเซ็ต
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือรีเซ็ตตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการลงนาม
- วันที่ ........./........./.........
- วิลล่า
- วิเคราะห์จุดอ่อนรายช่องทาง จากหัวข้อที่ได้คะแนนต่ำ
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมมติ ใจดี
- สรุปข้อมูล วันที่
- สรุปข้อมูล วันที่ ต้องไม่ก่อนเอกสารประเมิน วันที่
- สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT
- สรุปความพึงพอใจลูกค้า MT
- สรุปแล้ว
- สรุปแล้ว — ล็อกแก้ไข
- สร้าง PDF
- สร้างซ้ำครั้งเดียวกัน
- สร้างซ้ำครั้งเดียวกัน — ใช้ MTS-2569-0004
- สร้างสรุปผล
- สร้างสรุปผลประเมินความพึงพอใจลูกค้า MT ครั้งแรก
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สายงานการขาย
- สายอนุมัติ (DOA)
- สิงหาคม
- ส่งออก
- หัวหน้าหน่วยธุรกิจ
- อา
- เงื่อนไขทางการค้า (ราคา โปรโมชั่น การชำระเงิน)
- เช่น 1
- เช่น แบบประเมินที่ลูกค้า MT ตอบ หรือไฟล์สรุปคะแนน
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลม่อนฟาร์ม
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกวันที่
- เอกสารประเมิน วันที่
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งเตือน: ช่องทางต่ำกว่า
- แนบเอกสารประกอบ (ถ้ามี)
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบประเมินลูกค้า MT ครั้งที่ 2-2569.xlsx
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แมคแวลู่
- ใส่ข้อเสนอแนะอย่างน้อย 1 ข้อ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีขั้นอนุมัติ ตามแบบฟอร์ม (DEC-03)
- ไม่มีข้อมูล
- ไม่ใช้เอกสารนี้แล้ว

## §10 Data Binding & BACKEND anchors
| Prototype | API (02_API) | หมายเหตุ |
|---|---|---|
| `RECS` · `listRows()` · `canSee()` | API-01/02/08 | FN-09 |
| `persist()` (ENG-DOC-NUM ตอนบันทึกครั้งแรก) | API-03/04 | FN-01..03 |
| `openFinalize()` · `confirmFinalize()` | API-05 | FN-04 · ENG-NOTIFY mts_low_channel |
| `openCancel()` · `confirmReason()` | API-06 | FN-05 · ENG-NOTIFY mts_cancelled |
| `docPrintData()` · `tplRender()` · `tplSignRows()` · `DOC_TPL` | API-07 | FN-07 · parity กับ render_doc.py |
| `pickFiles()` · `gateFiles()` | API-09 | FN-06 |
| `CFG` (criteria · channels · std · low · bands) | SalesConfig (อ่าน) | ห้าม hardcode ในระบบจริง |
| `MOCK_DOA_RESOLVED` (steps ว่าง) · `resolveDoa()` · `DOA_FIELDS` | 02 §2.3 | DOA hook 0 ขั้น (DEC-03) · TODO: DOA engine |
| `DOC.active` | F-DOCCFG status | |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/08 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/09 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/05/06/07 | `renderViewDrawer()` |
| §6 modal | 01_UI M-01..03 · 05 VR-04..06 | `renderModal()` |
| §5 % | 05 BR-01..05 | `chCalc()` · `groupsOf()` |
**Drift Log:** business 0 · HTML-only (prototype-only ไม่ต้องสร้าง): `window.__QA__` · `switchPersona()` สลับผู้ใช้ · `S.sim` / `commitRejected()` จำลอง API ล้ม · บันทึกแจ้งเตือนในประวัติ (ระบบจริงยิง ENG-NOTIFY)

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (รอบแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ผู้รับรองรายงานผ่าน DOA กลาง ถ้าลูกค้าต้องการ (OQ-03) · ดึงคะแนนจากแบบประเมินลูกค้า MT อัตโนมัติ (OQ-05) · กราฟแนวโน้ม % รายช่องทางข้ามครั้ง
