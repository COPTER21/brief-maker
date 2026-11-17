# UI_BRIEF — F-TMP-001 ใบตรวจเช็คถังดับเพลิง (Fire Extinguisher Inspection Card)

> AS-BUILT จาก `feature.html` (source of truth) · คู่กับ FRD_F-TMP-001_Pack · html-ui-brief v1.1

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | feature.html · html-generator-v9 (Golden Skeleton v9.4) · archetype `Q-form-noapproval` · `window.__QA__` มี |
| FRD | FRD_F-TMP-001_Pack v1.0 (STANDARD) · 01_UI P-01..03 · 02_API API-01..09 · 05_RULES BR-01..13 |
| มติ | DECISIONS.lock 13 ข้อ (AI-DEFAULT 10 · VALID 3) — รอใบเซ็นลูกค้า |
| สถานะ drift | ไม่มี business drift · prototype-only: `__QA__` · `switchPersona()` · `S.sim` (ดู §11) |
| Gate | audit FAIL 0 · self_audit PASS · jsdom smoke 27/27 · [NO-BROWSER] ยังไม่รัน e2e_standard / render-check |

## §1 Design Tokens AS-BUILT
CI = CUBE Warm Light (base-kit v6.4 — ห้ามแก้) · font: Noto Sans Thai / Satoshi · icon: Lucide 0.469.0 (mono currentColor)

| CSS variable | ค่า |
|---|---|
| `--c-navy` | #111111 |
| `--c-navy-2` | #111111 |
| `--c-primary` | #FF3B30 |
| `--c-primary-hover` | #E62E24 |
| `--c-teal` | #FF9A1F |
| `--c-teal-light` | #FFB763 |
| `--c-ink` | #111111 |
| `--c-mute` | #54565C |
| `--c-mute-2` | #73757B |
| `--c-mute-3` | #9A9CA2 |
| `--c-placeholder` | rgb(180,182,188) |
| `--z-content` | 1 |
| `--z-sticky` | 10 |
| `--z-shell` | 10 |
| `--z-dropdown` | 30 |
| `--z-backdrop` | 50 |
| `--z-drawer` | 51 |
| `--z-modal` | 60 |
| `--z-popover` | 70 |
| `--z-toast` | 80 |
| `--c-line` | #DEDAD4 |
| `--c-line-2` | #E9E5E0 |
| `--c-line-3` | #F1EEEA |
| `--c-bg-off` | #FAF8F5 |
| `--c-success` | #1F9D55 |
| `--c-warning` | #E8870F |
| `--c-danger` | #E62E24 |
| `--sidebar-w` | 232px |
| `--shell-h` | 52px |
| `--fs-h1` | 22px |
| `--fs-h2` | 17px |
| `--fs-h3` | 15px |
| `--fs-body` | 14px |
| `--fs-sub` | 13px |
| `--fs-meta` | 12px |
| `--fs-cap` | 11px |
| `--fs-kpi` | 28px |
| `--sp-xs` | 4px |
| `--sp-sm` | 8px |
| `--sp-md` | 12px |
| `--sp-lg` | 20px |
| `--sp-xl` | 28px |
| `--r-xs` | 4px |
| `--r-sm` | 6px |
| `--r-md` | 8px |
| `--r-lg` | 12px |
| `--r-full` | 999px |

### z-index map
| ค่า | ใช้ที่ |
|---|---|
| 1 | .stepper-item:not(:last-child)::after |
| 2 | .stepper-circle |
| 3 | .table-scroll.is-sticky thead th |
| var(--z-backdrop) | #drawerBackdrop, .drawer-backdrop, .ss-list, รมีปุ่ม action หลัก */  .modal-backdrop |
| var(--z-drawer) | #drawer, .drawer |
| var(--z-dropdown) | .info-tip::after, .user-menu |
| var(--z-modal) | .modal-backdrop |
| var(--z-popover) | * เมนูที่ portal ออกจาก scroll container (ใช้คู่ p, .row-menu, verlay-root ตอนเปิด (หลุด overflow ของ modal/drawe |
| var(--z-portal) | .bd-pop |
| var(--z-shell) | .sidebar |
| var(--z-sticky) | .shell-bar, .table-wrap thead th, .wizard-footer |
| var(--z-toast) | #toast, .toast |

## §2 Route Map
| Route | หน้า | refresh-safe |
|---|---|---|
| `#/fire-extinguisher-check` | P-01 รายการ | ✓ (`applyRoute()`) |
| `#/fire-extinguisher-check/create` | P-02 สร้าง (drawer wide) | ✓ |
| `#/fire-extinguisher-check/view/:id` | P-03 ดู (drawer 920) — ใบที่ไม่มีสิทธิ์ไม่เปิด | ✓ |
hashchange → `applyRoute()` · route ใช้ `go()` → `navigate()` (base-kit)

## §3 Layout Shell
sidebar 232px (`.sidebar` · โมดูล "คลังสินค้า" › "ตรวจเช็คถังดับเพลิง" + `#sbBadge` = จำนวนใบที่ผลล่าสุดผิดปกติ) · shell-bar 52px (`.shell-bar` · breadcrumb Core › คลังสินค้า › ใบตรวจเช็คถังดับเพลิง · `#notifBtn` · `.user-chip` → `#userMenu` สลับ persona) · เนื้อหา `#page-content`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph` → `.ph-title` "ใบตรวจเช็คถังดับเพลิง" + `.ph-sub` + `.ph-badge` (จำนวน) + `.ph-badge.is-bad` (ผิดปกติ N · ซ่อนเมื่อ 0) · `.ph-actions`: ส่งออก CSV (`exportCSV()`) · `#btnCreate` สร้างใบตรวจ (`startWizard()`)
- `.filter-card` → `.input-search` `#fq` (`onQ()`) · `searchSelectHTML()` 3 ตัว: fst สถานะ · fres ผลตรวจ · fzone โซน (`initSelects()`) · รีเซ็ต (`resetFilters()`)
- `.list-card` → `.table` คอลัมน์ เลขที่ · สถานที่ · ตรวจล่าสุด · ผลล่าสุด · ผู้ตรวจล่าสุด · จำนวนครั้ง · สถานะเอกสาร · ⋮ (`sortTh()` sortable 4 คอลัมน์) · แถวคลิก `rowClick()` → `openView()` · ⋮ `openRowMenu()` → `.row-menu`
- footer `pager()` → `.pg-size` (10/25/50 · `setSize()`) + "x – y จาก N รายการ" + `.pagination`
### P-02 สร้าง (`renderWizard()` · `.drawer-panel.wide`)
- `stepper()` 3 ขั้น `STEPS` · ขั้น 1 `wizMain()` = `.wz-split`: การ์ด ① สถานที่ (`searchSelectHTML()` loc + แจ้งใบซ้ำ + `openExisting()`) · ② ผลตรวจครั้งนี้ (`bedateHTML()` ckdate + `marksBlock()` + `toggleWithCheck()`) · ขวา `sumCard()`
- ขั้น 2 `wizAttach()` `.upload-zone` → `#fecFile` (`pickFiles()` · `gateFiles()`) · ขั้น 3 `wizReview()` `.review-card` ×3
- footer: ย้อนกลับ (`wizBack()`) · ยกเลิก · ถัดไป `#btnNext` (`wizNext()`) / บันทึกใบตรวจ `#btnSave` (`saveCard()`)
### P-03 ดู (`renderViewDrawer()` · drawer 920)
- `.dw-head` lean: kicker · เลขที่ + `docPill()` · `.dw-sub` สถานที่ · ตรวจล่าสุด · actions ยกเลิกใบตรวจ (link แดง) · `#btnCheckView` บันทึกผลตรวจ · พิมพ์/ดาวน์โหลด (`genPdf()`) · ปิด
- `.drawer-tabs.dt-full` (`tabBtn()`): รายละเอียด (`renderDetailTab()` · `viewBanner()` · `checksTable()`) · PDF Preview (`renderPdfTab()` · `.pdf-frame`) · ประวัติ (`renderHistoryTab()` · `.tl`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตัวเลือกเครื่องหมาย | `markSeg()` `.mk-seg` `.mk-opt` | ว่าง · / ปกติ (`.is-on` เขียว) · x ผิดปกติ (`.is-x.is-on` แดง) · error `.mk-row.is-invalid` · ไม่มี disabled |
| ปกติทุกข้อ | `allNormal()` `.link-btn` | — |
| วันที่ พ.ศ. | `bedateHTML()` `.bedate` | ว่าง · มีค่า · max = วันนี้ (วันอนาคต disabled) · error `.field.is-invalid` |
| สถานที่ | `searchSelectHTML()` `.search-select` | ว่าง · เลือก · ใบซ้ำ (alert + ลิงก์) · error |
| การ์ดสรุป | `sumCard()` `.wz-sum` `.wz-sum-total` | is-off (ไม่ต้องแจ้ง) · is-bad (จะแจ้งทันที) |
| ตารางผลตรวจ | `checksTable()` `.fec-checks` | ว่าง `.empty-sub` · แถวผิดปกติ `.is-bad-row` · ปุ่มแก้เฉพาะ `canEditCheck()` |
| คน | `empChip()` `.emp-chip` `.emp-av` · `personInline()` `.person-inline` | วงกลมพื้น #111111 + icon คน SVG |
| pill | `docPill()` `resPill()` `markPill()` | ใช้งาน/ยกเลิก · ปกติ/ผิดปกติ/ยังไม่ตรวจ · / ปกติ / x ผิดปกติ |
| ปุ่ม loading | `busyLabel()` | loader-2 "กำลังบันทึก…" |

## §6 Overlay Registry
| Overlay | ขนาด | เปิด | ปิด (dismiss) | z |
|---|---|---|---|---|
| drawer view | 920 | `openView()` / route | ปุ่ม x · ปิด · Esc · backdrop **mousedown** (`drawerBackdropDown()`) | var(--z-drawer) / var(--z-backdrop) |
| drawer wizard `.drawer-panel.wide` | 1290 | `startWizard()` | เหมือน view แต่กรอกค้าง → modal ทิ้งข้อมูล (`closeDrawer()`) | var(--z-drawer) |
| modal บันทึก/แก้ผลตรวจ (`.modal.is-lg`) | 680 | `openCheck()` | ยกเลิก · Esc · **backdrop ไม่ปิด** (`modalBackdropDown()`) | var(--z-modal) |
| modal ยกเลิกใบตรวจ | 520 | `openCancel()` | ไม่ยกเลิก · Esc · backdrop ไม่ปิดเมื่อพิมพ์เหตุผลแล้ว | var(--z-modal) |
| modal ทิ้งข้อมูล | 520 | `closeDrawer()` ตอน dirty | กลับไปกรอกต่อ / ทิ้งข้อมูล | var(--z-modal) |
| row-menu ⋮ | 180 | `openRowMenu()` | คลิกที่อื่น · scroll (`closeRowMenu()`) | var(--z-popover) |
| user-menu | — | `toggleUserMenu()` | คลิกที่อื่น | var(--z-dropdown) |
| ปฏิทิน bd-pop · ss-list | — | `bdToggle()` · search-select | Esc ปิดเฉพาะตัวเอง · คลิกที่อื่น | var(--z-portal) |
| toast | — | `showToast()` | อัตโนมัติ 2.8s | var(--z-toast) |

## §7 Interaction Spec
- Esc chain: ปฏิทิน/combobox (จัดการในตัว · stopPropagation) → modal (`closeModal()`) → drawer (`closeDrawer()`)
- backdrop: ปิดด้วย mousedown ที่ backdrop เท่านั้น (ลากจากข้างในไปปล่อยนอก = ไม่ปิด)
- `render()` เก็บ/คืน focus + scroll (`preserveRenderState()` / `restoreRenderState()`) · ปิดปฏิทินก่อน render (`bdClose()`)
- จำลอง API: บันทึก 500ms · `commitRejected()` ตาม `S.sim` (stale/denied/error/upload_fail)

## §8 State-Driven UI Matrix
| สถานะใบ | pill | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| active | ใช้งาน (pill-success) | ยกเลิกใบตรวจ (เจ้าของ/role-mgr-wh) · บันทึกผลตรวจ (ผู้เห็น) | ดูรายละเอียด · บันทึกผลตรวจ · พิมพ์ · ยกเลิกใบตรวจ |
| cancelled | ยกเลิก (pill-muted) | — (footer "ยกเลิกแล้ว ล็อกการบันทึก") | ดูรายละเอียด · พิมพ์ |
| ผลล่าสุด | ปกติ (pill-success) · ผิดปกติ (pill-danger + แถบแดง) · ยังไม่ตรวจ (pill-muted + แถบแนะนำ) | | |

## §9 Microcopy (verbatim)
### Toast
- [info] ไม่มีการแจ้งเตือนใหม่
- [warning] แบบเอกสารนี้ยังไม่เปิดใช้งาน
- [warning] กรุณากรอกข้อมูลให้ครบถ้วน
- [warning] แจ้งผู้จัดการคลังสินค้าแล้ว — ${r.code} พบผิดปกติ (${badList(c)})
- [info] บันทึกใบตรวจแล้ว ·
- [warning] บันทึกผลตรวจได้เฉพาะใบที่ใช้งาน
- [warning] แก้ไขได้เฉพาะแถวที่คุณบันทึกวันนี้
- [info] บันทึกผลตรวจแล้ว ·
- [info] ยกเลิกใบตรวจแล้ว ·
- [info] ส่งออก
- [info] สลับเป็น
- [error] แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
### ข้อความบนจอ (สกัดจาก HTML)
- / ปกติ
- 99 อาคารตัวอย่าง ชั้น 9 ถนนตัวอย่าง
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกใบตรวจ',
- ], ['printer', 'พิมพ์',
- ]]; if (canRecord(r)) items.splice(1, 0, ['clipboard-check', 'บันทึกผลตรวจ',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- x ผิดปกติ
- · ตรวจล่าสุด
- · ยกเลิกแล้ว ล็อกการบันทึก
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณาเลือกสถานที่
- กันยายน
- กานดา ขายเก่ง
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักใบตรวจ
- คลังสินค้า
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาสถานที่ / โซน
- ค้นหาเลขที่ / สถานที่ / ผู้สร้าง
- จะแจ้งทันที
- จะแจ้งผู้จัดการคลังสินค้า
- จำนวนครั้ง
- ชนิดไฟล์ไม่รองรับ
- ชื่อฟังก์ชัน
- ซีล/สลัก
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจล่าสุด
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้อง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกผลตรวจ
- ทุกสถานะ
- ทุกโซน
- ธ.ค.
- ธันวาคม
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บันทึกผลตรวจ
- บันทึกผลตรวจด้วย
- บันทึกผลตรวจแล้ว ·
- บันทึกผลตรวจได้เฉพาะใบที่ใช้งาน
- บันทึกผิดสถานที่
- บันทึกแล้วระบบออกเลขที่เอกสาร · ใบตรวจใช้บันทึกผลตรวจครั้งต่อไปได้เรื่อย ๆ
- บันทึกใบตรวจแล้ว ·
- ปกติ
- ปกติทุกข้อ
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ผล
- ผลตรวจล่าสุด
- ผลล่าสุด
- ผิดปกติ
- ผิดปกติ:
- ผู้จัดการคลังสินค้า
- ผู้ตรวจ
- ผู้ตรวจล่าสุด
- ผู้สร้าง
- ฝ่ายขาย
- พ.ค.
- พ.ย.
- พบผิดปกติ — บันทึกแล้วระบบแจ้งผู้จัดการคลังสินค้าให้ติดต่อผู้จำหน่ายเพื่อแก้ไข
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ม.ค.
- มกราคม
- มาตรวัด
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีใบใช้งาน
- ยกเลิก
- ยกเลิกใบตรวจ
- ยกเลิกใบตรวจแล้ว ·
- ยังไม่ตรวจ
- ยังไม่ตรวจ (ใบเปล่า)
- ยังไม่ตรวจ — สร้างใบเปล่า
- ยังไม่มีข้อมูล
- ยังไม่มีผลตรวจ
- ยังไม่มีใบตรวจเช็คถังดับเพลิง
- ย้อนกลับ
- ย้ายจุดติดตั้งถัง
- ย้ายจุดติดตั้งถัง — ไปติดที่โซน A3
- รายการ
- รายการตรวจ
- รายละเอียด
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ล้างตัวกรอง
- วันที่ตรวจห้ามเป็นวันในอนาคต
- วันที่นี้บันทึกผลตรวจแล้ว
- วันที่สร้าง
- วิชัย คลังดี
- ส.ค.
- สถานที่
- สถานที่นี้มีใบตรวจที่ใช้งานอยู่แล้ว
- สถานะ
- สถานะเอกสาร
- สภาพถัง
- สมชาย ตรวจดี
- สร้าง PDF
- สร้างโดย
- สร้างใบซ้ำ
- สร้างใบตรวจ
- สร้างใบตรวจ 1 ใบต่อ 1 จุดติดตั้งถังดับเพลิง
- สลับเป็น
- สายฉีด
- สิงหาคม
- สุดา ปลอดภัย
- ส่งออก
- ห้องเก็บสารเคมี
- อา
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่คลังสินค้า
- เช่น ใบรับรองการเติมสารดับเพลิง หรือรูปถ่ายถังที่ผิดปกติ
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกจุดติดตั้งถังดับเพลิง แล้วบันทึกผลตรวจครั้งนี้ — 1 ใบต่อ 1 จุดติดตั้ง
- เลือกประเทศ
- เลือกผลให้ครบทั้ง 4 หัวข้อ
- เลือกวันที่
- เอกสารแนบ
- แก้ไขผลตรวจ
- แก้ไขล่าสุด
- แก้ไขแถวนี้
- แก้ไขได้เฉพาะแถวที่คุณบันทึกวันนี้
- แขวงตัวอย่าง เขตตัวอย่าง กรุงเทพ 10000
- แนบเอกสารประกอบ (ถ้ามี)
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบพิมพ์
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- โซน
- โซน A1 คลังสินค้า
- โซน A4 คลังสินค้า
- โซน B2 คลังสินค้า
- ใช้งาน
- ใบตรวจเช็คถังดับเพลิง
- ใบรับรองการเติมสารดับเพลิง 2569.pdf
- ไม่ต้องแจ้ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา

## §10 Data Binding & BACKEND anchors
| จุด | mock | API (02_API) |
|---|---|---|
| รายการ/ดู | `RECS` · `listRows()` · `canSee()` | API-01 · API-02 |
| สร้างใบ + ออกเลข | `saveCard()` (SEQ → FEC-2569-NNNN) | API-03 · ENG-DOC-NUM |
| บันทึก/แก้ผลตรวจ | `confirmCheck()` | API-04 · API-05 |
| ยกเลิก | `confirmCancel()` | API-06 |
| PDF | `docPrintData()` → `tplRender()` → `fecPdfDoc()` | API-07 (server render template เดียวกัน) |
| แจ้งผิดปกติ | `notifyAbnormal()` (toast จำลอง) | ENG-NOTIFY fec_abnormal_found |
| master | `EMP` · `LOCS` | F-EMP-001 · Warehouse Location |
| สิทธิ์ | `isAdmin()` role-mgr-wh · `canRecord()` · `canCancel()` · `canEditCheck()` | 05 §5.3 |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/08 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03 · BR-01/04/05 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/04/05/06/07 | `renderViewDrawer()` |
| §6 modal บันทึกผลตรวจ | M-01 · BR-02/03/05/06/07 | `openCheck()` |
| §6 modal ยกเลิก | M-02 · BR-12 | `openCancel()` |
**Drift Log:** ไม่มี business drift · prototype-only (ไม่ต้องสร้างในระบบจริง): `window.__QA__` · `switchPersona()` (ตัวสลับผู้ใช้) · `S.sim` · ชื่อบริษัท/โลโก้ใน PDF เป็น placeholder (ระบบจริงใช้ header_snapshot)

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- เตือนจุดที่เลยรอบตรวจ (ต้องมีรอบตรวจใน master) · ปุ่มเปิดงานซ่อมจากแถวผิดปกติ (Phase 2 · OQ-05) · สแกน QR ที่ถังเพื่อเปิดใบ
