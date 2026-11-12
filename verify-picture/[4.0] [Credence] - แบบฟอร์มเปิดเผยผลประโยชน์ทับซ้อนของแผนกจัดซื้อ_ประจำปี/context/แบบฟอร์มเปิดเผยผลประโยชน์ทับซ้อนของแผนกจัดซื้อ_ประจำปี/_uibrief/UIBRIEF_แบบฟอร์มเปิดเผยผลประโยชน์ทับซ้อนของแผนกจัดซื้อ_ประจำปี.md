# UI BRIEF — F-TMP-006 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) · audit FAIL 0 · jsdom smoke 39/39 · [NO-BROWSER] e2e/screenshot ยังไม่รัน |
| FRD | FRD_F-TMP-006_Pack (00–07 · frd_lint BLOCK 0 WARN 0) |
| DECISIONS | DECISIONS.lock REQ-TMP-006 — 18 มติ (AI-DEFAULT 11 · VALID 7) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` (`commitRejected()`) · seed `RECS` (`mkRec()` ชื่อสมมติ) — ไม่ทำในระบบจริง (Drift Log) |
| Data Classification | Confidential — รายละเอียด/ข้อคิดเห็นไม่อยู่ใน list/CSV/notification |
| Drift | 3 รายการ (ดู §11) |

## §1 Design Tokens AS-BUILT
CI CUBE Warm Light (BASE-KIT ห้ามแก้) · font Noto Sans Thai + Satoshi · icon Lucide 0.469.0 (multi-CDN loader) · scrollbar 5px
| CSS variable | ค่า |
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

### z-index map
| ค่า | selector |
|---|---|
| `var(--z-shell)` | /* ============== SIDEBAR ============== */ .sidebar |
| `var(--z-sticky)` | /* ============== SHELL BAR ============== */ .shell-bar |
| `var(--z-dropdown)` | /* User dropdown menu */ .user-menu |
| `var(--z-sticky)` | .table-wrap thead th |
| `var(--z-popover)` | * เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .menu-fixed |
| `var(--z-backdrop)` | .ss-list |
| `var(--z-popover)` | verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body) */ .ss-list.menu-fixed |
| `3` | .table-scroll.is-sticky thead th |
| `2` | .stepper-circle |
| `1` | .stepper-item:not(:last-child)::after |
| `var(--z-backdrop)` | .drawer-backdrop |
| `var(--z-drawer)` | .drawer |
| `var(--z-backdrop)` | รมีปุ่ม action หลัก */ /* ============== MODAL ============== */ .modal-backdrop |
| `var(--z-toast)` | /* ============== TOAST ============== */ .toast |
| `var(--z-sticky)` | .wizard-footer |
| `var(--z-dropdown)` | .info-tip::after |
| `var(--z-modal)` | /* v9.1 Rule #62 — modal เหนือ drawer */ .modal-backdrop |
| `var(--z-drawer)` | #drawer |
| `var(--z-backdrop)` | #drawerBackdrop |
| `var(--z-toast)` | #toast |
| `var(--z-popover)` | /* row menu ⋮ (portal ใน #overlay-root) */ .row-menu |

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/coi-disclosure` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/coi-disclosure/create` · `#/coi-disclosure/create/change-:id` | P-02 ยื่นใหม่ / แจ้งเปลี่ยนแปลง (อ้างใบเดิม) | `startWizard()` |
| `#/coi-disclosure/edit/:id` | P-02 แก้ไข | `startWizard()` (เฉพาะเจ้าของ · draft/returned) |
| `#/coi-disclosure/view` · `#/coi-disclosure/view/:id` | P-03 ดู | `openView()` · `showDrawer()` (ไม่มีสิทธิ์ = ไม่เปิด) |
refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go('coi-disclosure')`

## §3 Layout Shell
sidebar `#sidebar` (โมดูล "จัดซื้อ" → "เปิดเผยผลประโยชน์ทับซ้อน" + `#sbBadge` = จำนวนใบรอฉันพิจารณา) · shell-bar (breadcrumb Core › จัดซื้อ › เปิดเผยผลประโยชน์ทับซ้อน · กระดิ่ง · ชิปผู้ใช้ + `.user-menu` สลับผู้ใช้เดโม) · `#page-content` · `#drawer` + `#drawerBackdrop` · `#modal` + `#modalBackdrop` · `#toast` · `#overlay-root`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-count` + `.ph-sub` "รอบปี {current_year} · เอกสารลับ…" · ปุ่ม `exportCSV()` · `#btnCreate` "ยื่นแบบเปิดเผย") → แถบแดงเมื่อ `DOC.active` = false → `.seg` (`segTabs()` · `.seg-btn` ทั้งหมด/รอฉันพิจารณา) → `.card` filter (ค้นหา `#fq` · search-select `fst` สถานะ · `fch` ผลการเปิดเผย · ล้างตัวกรอง) → ตาราง 9 คอลัมน์ (เลขที่ · ประจำปี · วันที่ยื่น · ผู้เปิดเผย `personInline()` · ตำแหน่ง · ผลประโยชน์ทับซ้อน `choicePill()` · สถานะ `docPill()` (+ ถูกแทนที่) · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()`) → `pager()` 25/หน้า · ไม่มีคอลัมน์รายละเอียด (ข้อมูลลับ)
### P-02 ยื่น/แก้ไข — `renderWizard()` (drawer `.wide`)
หัว + `stepper()` 3 ขั้น → ขั้น 1 `wizMain()`: `dupAlert()` (มีใบปีนี้แล้ว → แทนฉบับ) · `.wz-split` = ซ้าย การ์ด ① ข้าพเจ้า/ตำแหน่ง/ปี + `.stmt` ถ้อยคำรับรอง (`COI_CONFIG`) · การ์ด ② `choiceCard()` ×2 (`.track-card` ไม่มี/มี · `setChoice()`) + `#in-detail` (เฉพาะ มี · `setDetail()` · `secretNote()`) · การ์ด ③ `.stmt` ถ้อยคำท้าย + `#cfConfirm` `.cf-row` (`toggleConfirm()`) · ขวา `#wzSum` `sumCard()` → ขั้น 2 `wizAttach()` upload zone → ขั้น 3 `wizReview()` review cards → footer (`wizBack()` · ยกเลิก · `saveDraft()` · `wizNext()` / `#btnSaveSubmit` `saveAndSubmit()`)
### P-03 ดู — `renderViewDrawer()` (drawer 920)
หัว lean (เลขที่ + pill สถานะ + pill ไม่มี/มี · sub ผู้เปิดเผย · ประจำปี) + ปุ่มตามสถานะ → `.drawer-tabs` (`tabBtn()`) → `renderDetailTab()` (`viewBanner()` · ข้อมูลเอกสาร · ผู้เปิดเผย · ถ้อยคำรับรอง · การมีผลประโยชน์ทับซ้อน + `secretNote()` · `commentView()` ข้อคิดเห็นของผู้บังคับบัญชา · เอกสารแนบ · ข้อมูลระบบ) / `renderPdfTab()` (iframe `.pdf-frame` `fitPdf()`) / `renderSignTab()` / `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| segmented tabs | `.seg-btn` · `setStat()` | default · `.on` (dot primary + count) · hover |
| ตัวเลือก ไม่มี/มี | `.track-card` · `.tc-check` · `setChoice()` | default · `.is-on` (เลือกได้ 1) · `.track-grid.is-bad` (ยังไม่เลือก) |
| รายละเอียด | `#fw-detail` · `#in-detail` · `setDetail()` | ซ่อน (ไม่มี) · แสดง (มี) · `.field.is-invalid` < 10 ตัวอักษร · ล้าง error เมื่อพิมพ์ครบ |
| ยืนยันถ้อยคำ | `#cfConfirm` · `.cf-row` · `toggleConfirm()` | default · `.is-on` · `.is-bad` (ยังไม่ยืนยัน) |
| ถ้อยคำรับรอง | `.stmt` | อ่านอย่างเดียว (config / snapshot) |
| ป้ายข้อมูลลับ | `.secret-note` · `secretNote()` | แสดงใต้รายละเอียดทุกจุด |
| สรุปขวา | `#wzSum` · `sumCard()` | `.wz-sum-total` `.is-off` (ยังไม่เลือก) / `.is-ok` (ไม่มี) / `.is-bad` (มี) · แทนฉบับ · อัปเดต soft `softSum()` |
| ปุ่มบันทึก | `#btnSaveSubmit` · `busyLabel()` | default · disabled + "กำลังบันทึก…" (`S.busy`) |
| คน | `personInline()` · `empChip()` | วงกลม icon `user` mono (ไม่มี initials) |
| เมนูแถว | `.row-menu` · `openRowMenu()` · `canChange()` | portal ใน `#overlay-root` · ปิดเมื่อคลิกนอก/scroll · "แจ้งเปลี่ยนแปลง" เฉพาะใบรับทราบแล้วของตนปีนี้ |

## §6 Overlay Registry
| Overlay | ขนาด | เปิด | ปิด | ห้ามปิด |
|---|---|---|---|---|
| drawer view | 920 | `openView()` | ปุ่ม X · Esc · mousedown ที่ `#drawerBackdrop` | — |
| drawer wizard `.wide` | 1290 | `startWizard()` | ปุ่ม X/ยกเลิก · Esc · backdrop → ถ้ากรอกค้าง (`S.dw.dirty`) เปิด modal ทิ้งข้อมูล | dirty |
| modal (`#modalBackdrop`) | 520 / `.is-lg` 680 (ส่ง) | `openModalCfg()` | ปุ่ม · mousedown ที่ backdrop (`modalBackdropClick()`) | มีข้อความเหตุผล/ข้อคิดเห็นค้าง |
| `.row-menu` | 230 | ⋮ | คลิกนอก · scroll | — |
| `.toast` (`#toast`) | — | `showToast()` | อัตโนมัติ | — |
| `.user-menu` | — | `toggleUserMenu()` | คลิกนอก | — |
| `.ss-list` (search-select) | ตามช่อง | `initSearchSelect()` | คลิกนอก · Esc | — |
| iframe พิมพ์ `.pdf-gen` | ซ่อน | `genPdf()` | — | ตรวจ `canSee()` ก่อน |

## §7 Interaction Spec
- Esc chain (kit): ปิด search-select → modal → drawer ตามลำดับ handler
- backdrop ปิดด้วย `onmousedown` เมื่อ target = backdrop เท่านั้น (U25) — ลากจากในออกนอกไม่ปิด
- `render()` เก็บ/คืน scroll + focus (`preserveRenderState()`/`restoreRenderState()`) · พิมพ์รายละเอียดไม่เรียก `render()` (focus ไม่หลุด)
- เลือก ไม่มี = ล้างรายละเอียดและซ่อนช่อง (DEC-15) · เลือกได้ทีละ 1 (DEC-14)
- ส่งจากหน้าดูขณะยังไม่ครบ (เลือก/รายละเอียด/ยืนยัน) → toast + เปิดแก้ไข (`openSubmit()`)
- รับทราบขั้นสุดท้ายของใบที่อ้างใบเดิม → ใบเดิมได้ pill "ถูกแทนที่" + audit (`confirmApprove()`)
- PDF: `genPdf()` เปิดหน้าต่างพิมพ์จาก iframe ซ่อน `.pdf-gen` (ชื่อ = เลขที่) · ไม่มีสิทธิ์ = ไม่ทำงาน

## §8 State-Driven UI Matrix
| สถานะ | pill | ปุ่มหัว drawer (ตามผู้ใช้) |
|---|---|---|
| draft ร่าง | `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งพิจารณา |
| pending รอพิจารณา | `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำตาม role จาก `wordsOf()` (ส่งกลับแก้ไข · รับทราบ) · เจ้าของ/compliance: ยกเลิกเอกสาร |
| returned ส่งกลับแก้ไข | `pill-danger` | เหมือนร่าง + แถบแดงเหตุผล |
| approved รับทราบแล้ว | `pill-success` | เจ้าของ (ปีปัจจุบัน · ยังไม่ถูกแทนที่): แจ้งเปลี่ยนแปลง · ล็อกแก้ไข |
| cancelled ยกเลิก | `pill-muted` | — |
| (ถูกแทนที่) | `pill-muted` เพิ่มข้าง pill สถานะ | แถบ "ใบนี้ถูกแทนที่ด้วย …" |
ผลการเปิดเผย (`CHOICE`): none `pill-success` "ไม่มี" · has `pill-danger` "มี" · blank `pill-muted` "ยังไม่เลือก"

## §9 Microcopy (verbatim)
### Toast
| variant | ข้อความ |
|---|---|
| info | `ไม่มีการแจ้งเตือนใหม่` |
| warning | `แบบเอกสารนี้ยังไม่เปิดใช้งาน` |
| warning | `แก้ไขได้เฉพาะร่างของตัวเอง` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| info | `บันทึกร่างแล้ว ·` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| warning | `เลือก ไม่มี/มี กรอกรายละเอียด และยืนยันถ้อยคำรับรองก่อนส่ง` |
| info | `ส่งพิจารณาแล้ว ·` |
| info | `ส่งออก` |
| info | `สลับเป็น` |
| error | `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง` |
toast แบบประกอบ: "บันทึกร่างแล้ว · {เลขที่}" · "ส่งพิจารณาแล้ว · {เลขที่}" · "รับทราบ · {เลขที่}" · "ส่งกลับแก้ไขแล้ว · {เลขที่}" · "ยกเลิกเอกสารแล้ว · {เลขที่}" · "ส่งออก n รายการ (ไม่มีช่องรายละเอียด — ข้อมูลลับ)" · "สลับเป็น {ชื่อ}"
### Placeholder
`${rej ? 'แจ้งผู้เปิดเผยว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}` · `' + ph + '` · `ค้นหาเลขที่ / ชื่อผู้เปิดเผย / ตำแหน่ง / ปี` · `เช่น พี่ชายเป็นหุ้นส่วนผู้จัดการ หจก. ... ซึ่งเป็นผู้ขายของบริษัท` · `ไม่บังคับ — พิมพ์ลงกรอบข้อคิดเห็นในแบบพิมพ์`
### ข้อความในจอ (สกัดจาก HTML)
- (ขั้น
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]); if (canChange(r)) items.push(['file-pen-line', 'แจ้งเปลี่ยนแปลง (ยื่นใบใหม่)',
- ]]; if (isOwner(r) && isEditable(r)) items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · รับทราบแล้ว ล็อกแก้ไข
- · เปิดอยู่
- · เมื่อรับทราบ ใบนี้จะแทนฉบับ
- ก.ค.
- ก.พ.
- ก.ย.
- กฎหมาย
- กรอกผิดปี
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณายืนยันถ้อยคำรับรองก่อนส่ง
- กรุณาเลือก ไม่มี หรือ มี
- กำลังเปิดหน้าต่างพิมพ์ ·
- ขั้น
- ขาดเอกสารประกอบ
- ข้อความแจ้งเตือนไม่มีรายละเอียด (ข้อมูลลับ)
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักแบบเปิดเผย
- ข้อมูลเอกสาร
- ข้าพเจ้า นาย/นาง/นางสาว
- ข้าม
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- คู่สมรส (ชื่อสมมติ) ดำรงตำแหน่งผู้จัดการ บริษัท สมมติขนส่ง จำกัด ผู้ให้บริการขนส่งของบริษัท
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง)
- ค้นหา...
- ค้นหาเลขที่ / ชื่อผู้เปิดเผย / ตำแหน่ง / ปี
- จัดซื้อ
- จำลอง คัดสรร
- ชนิดไฟล์ไม่รองรับ
- ญาติทำงานบริษัทผู้ขาย
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวอย่าง ซื้อดี
- ตัวอย่าง บริหารซื้อ
- ตำแหน่ง
- ต้อง
- ถึง
- ถูกแทนที่
- ถูกแทนที่ด้วย
- ทดสอบ กำกับงาน
- ทดสอบ หาของ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกผลการเปิดเผย
- ทุกสถานะ
- ธ.ค.
- นาง
- นางสาว
- นาย
- บริษัท ตัวอย่าง จำกัด
- บริหาร
- บันทึกร่างแล้ว ·
- บันทึกแบบร่าง
- บันทึกแบบร่างได้ · ส่งพิจารณาแล้วแก้ไขไม่ได้จนกว่าถูกส่งกลับ
- บุตร (ชื่อสมมติ) ถือหุ้นและเป็นกรรมการผู้มีอำนาจลงนาม บริษัท ทดสอบบรรจุภัณฑ์ จำกัด
- ประจำปี
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ผล
- ผล:
- ผลประโยชน์ทับซ้อน
- ผู้จัดการทั่วไป
- ผู้จัดการฝ่ายจัดซื้อ
- ผู้บังคับบัญชา
- ผู้บังคับบัญชาให้ข้อคิดเห็นตอนพิจารณา
- ผู้พิจารณา
- ผู้ส่ง
- ผู้เปิดเผย
- ผู้เปิดเผย (ลงชื่อ)
- ผู้เปิดเผยยืนยันถ้อยคำรับรองแล้ว
- ฝ่ายกฎหมาย
- พ.ค.
- พ.ย.
- พิมพ์
- พี่ชาย (ชื่อสมมติ) เป็นหุ้นส่วนผู้จัดการ ห้างหุ้นส่วนจำกัด ตัวอย่างการค้า ซึ่งเป็นผู้ขายวัสดุสิ้นเปลืองในทะเบียนผู้ขาย
- ม.ค.
- มิ.ย.
- มี
- มี (กรุณาระบุรายละเอียดด้านล่าง)
- มี.ค.
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อคิดเห็น
- ยังไม่มีข้อมูล
- ยังไม่มีแบบเปิดเผยผลประโยชน์ทับซ้อน
- ยังไม่ยืนยันถ้อยคำรับรอง
- ยังไม่ส่ง
- ยังไม่เลือก
- ยื่นซ้ำโดยไม่ได้ตั้งใจ
- ยื่นผิดคน
- ยื่นแบบเปิดเผย
- ยื่นแบบเปิดเผยประจำปี
- ยื่นแบบเปิดเผยผลประโยชน์ทับซ้อน ประจำปี
- ย้อนกลับ
- รอผล
- รอพิจารณา
- ระบบ
- ระบุชื่อบุคคล ความสัมพันธ์ ชื่อกิจการ และตำแหน่ง
- รับทราบ
- รับทราบ ให้งดร่วมพิจารณาจัดจ้างขนส่งรายนี้
- รับทราบ ไม่พบผลประโยชน์ทับซ้อน
- รับทราบแล้ว
- รับทราบแล้ว — มีผลเป็นแบบเปิดเผยประจำปี
- รายการ
- รายการ (ไม่มีช่องรายละเอียด — ข้อมูลลับ)
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการพิจารณา
- ล้างตัวกรอง
- วันที่ ........./........./.........
- วันที่ยื่น
- ส.ค.
- สถานะ
- สมมติ ผู้บริหาร
- สมมติ ใจตรง
- สมมุติ ดูแลดี
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- ส่งกลับแก้ไข
- ส่งกลับแก้ไขแล้ว ·
- ส่งกลับให้ผู้เปิดเผยแก้ไข
- ส่งพิจารณา
- ส่งพิจารณา?
- ส่งพิจารณาแล้ว ·
- ส่งออก
- ส่งในระบบ
- หนังสือรับรองบริษัท (สำเนา).pdf
- หัวหน้าแผนกจัดซื้อ
- อนุมัติ
- อ่านถ้อยคำรับรอง เลือก ไม่มี/มี แล้วยืนยัน — บันทึกร่างได้ก่อนส่ง
- เจ้าหน้าที่กำกับดูแล (ฝ่ายกฎหมาย)
- เจ้าหน้าที่จัดซื้อ
- เจ้าหน้าที่จัดซื้อต่างประเทศ
- เจ้าหน้าที่จัดซื้ออาวุโส
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือก ไม่มี/มี กรอกรายละเอียด และยืนยันถ้อยคำรับรองก่อนส่ง
- เลือกตัวเลือกไม่ตรงกับข้อมูลที่ทราบ
- เลือกประเทศ
- เลือกผู้พิจารณา
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขแบบเปิดเผย
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้เปิดเผยว่าต้องแก้อะไร
- แจ้งฝ่ายกฎหมาย/กำกับดูแล (coi_conflict_declared)
- แจ้งเปลี่ยนแปลงระหว่างปี
- แทนฉบับ
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ
- แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนก
- แล้วส่งให้ผู้บังคับบัญชารับทราบ
- โปรดระบุชื่อบุคคล/กิจการ และความสัมพันธ์ให้ครบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีบุคคลในครอบครัว/เครือญาติเป็นผู้จัดการหรือหุ้นส่วนในกิจการที่เกี่ยวข้อง
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้พิจารณาขั้นนี้

## §10 Data Binding & BACKEND anchors
| จุดใน prototype | ระบบจริง |
|---|---|
| `RECS` / `mkRec()` | API-01/02 |
| `COI_CONFIG` | API-12 CoiDisclosureConfig (current_year · statement_text · closing_text · detail_min — snapshot ลงใบ) |
| `persist()` | API-03/04 (ENG-DOC-NUM ตอนบันทึกครั้งแรก · snapshot ผู้เปิดเผย/ปี) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (DOA-ENGINE-HOOK) | API-05/06 `GET /doa/resolve?feature_id=F-TMP-006` (role-line-manager · TODO: DOA engine) |
| `confirmSubmit()` | API-06 (+ coi_conflict_declared เมื่อตอบ มี) |
| `confirmApprove()` · `confirmReason()` | API-07/08 (supersede ใบเดิมตอนรับทราบขั้นสุดท้าย) |
| `docPrintData()` + `COI_TPL` + `tplRender()` | API-09 render ฝั่ง server (data contract เดียวกัน · ตรวจ canSee) |
| `exportCSV()` · `csvRow()` | API-10 (ไม่มีรายละเอียด/ข้อคิดเห็น) |
| `dupOf()` | API-03/06 warning DUPLICATE_YEAR + supersedes_no |
| `canSee()` | row policy (05 §5.3) |
| `DOC.active` | F-DOCCFG status |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 · FN-11 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/12 · FN-01..04 · BR-01..07 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 · FN-05..09 | `renderViewDrawer()` |
| §6 modal ส่ง/ตัดสิน/ยกเลิก | 05 §5.2 · BR-DOA-01..04 | `renderModal()` |
**Drift Log**
| # | ชนิด | รายการ | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only (prototype) | `window.__QA__` · สลับผู้ใช้ · `S.sim` | ไม่ทำในระบบจริง |
| D-02 | HTML mock | `MOCK_DOA_RESOLVED` 1 ขั้น · ขั้นฝ่ายกฎหมายทดสอบผ่าน `__QA__.doa.push` | ระบบจริงมาจาก DOA กลาง (OQ-03) |
| D-03 | HTML-only | ป้าย "เอกสารลับ" + view log ยังไม่มีใน prototype | ระบบจริงบันทึก audit การเปิดดู (เสนอ · 04 §4.2) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- แยกรายละเอียดเป็นรายการ (ความสัมพันธ์ · ชื่อบุคคล · กิจการ · ตำแหน่ง) เมื่อลูกค้ายืนยัน (OQ-07)
- หน้าตั้งค่า CoiDisclosureConfig (ปีรอบ · ถ้อยคำ · เวอร์ชัน) แบบ B Setting Rows (U26–U28) — OQ-06
- แดชบอร์ด % ยื่นแล้วต่อรอบปี สำหรับ role-compliance (ไม่มีรายละเอียด)
