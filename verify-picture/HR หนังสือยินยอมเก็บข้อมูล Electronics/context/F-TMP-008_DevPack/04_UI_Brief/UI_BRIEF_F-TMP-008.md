# UI BRIEF — F-TMP-008 หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล

## §0 Document Control + Pairing
| | |
|---|---|
| Source of truth | `feature.html` (single-file SPA · archetype `Q-form` · มี `window.__QA__`) |
| Pair FRD | `FRD_F-TMP-008_Pack/` (01_UI P-01..P-03 · 02_API · 05_RULES) |
| แบบพิมพ์ | `print/form.tpl.html` + `print/PDC_print-spec.md` + `print/PDC_data-contract.md` |
| มติที่คุมหน้าจอ | DECISIONS.lock 15 ข้อ (AI-DEFAULT 10 · VALID 5) |
| prototype-only (ห้ามพาไป production) | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` จำลอง API ล้ม · seed `RECS` |
| ไอคอน | Lucide 0.469.0 multi-CDN fallback · เรียกผ่าน `renderIcons()` เท่านั้น |

## §1 Design Tokens AS-BUILT
CSS variables ที่ประกาศใน `:root` (ครบตาม BASE-KIT v6.4):
- สี: `--c-navy` `--c-navy-2` `--c-primary` `--c-primary-hover` `--c-teal` `--c-teal-light` `--c-ink` `--c-mute` `--c-mute-2` `--c-mute-3` `--c-placeholder` `--c-line` `--c-line-2` `--c-line-3` `--c-bg-off` `--c-success` `--c-warning` `--c-danger`
- โครง: `--sidebar-w` `--shell-h`
- ตัวอักษร: `--fs-h1` `--fs-h2` `--fs-h3` `--fs-body` `--fs-sub` `--fs-meta` `--fs-cap` `--fs-kpi`
- ระยะ: `--sp-xs` `--sp-sm` `--sp-md` `--sp-lg` `--sp-xl` · มุม: `--r-xs` `--r-sm` `--r-md` `--r-lg` `--r-full`
- ชั้นซ้อน: `--z-content` `--z-sticky` `--z-shell` `--z-dropdown` `--z-backdrop` `--z-drawer` `--z-modal` `--z-popover` `--z-toast`

**z-index map (สูง → ต่ำ)**: `var(--z-toast)` › `var(--z-popover)` › `var(--z-modal)` › `var(--z-drawer)` › `var(--z-backdrop)` › `var(--z-dropdown)` › `var(--z-shell)` › `var(--z-sticky)` · ค่าเฉพาะที่ใช้ภายใน component: `3` `2` `1`
> ห้ามใส่ z-index ลอย — ต้องประกาศใน registry เดียวกันนี้

ฟอนต์: Satoshi (Fontshare) + Noto Sans Thai (Google Fonts) · scrollbar แบบบาง (`::-webkit-scrollbar` 5px + `scrollbar-width`)

## §2 Route Map
| route | หน้าจอ | refresh-safe |
|---|---|---|
| `#/pdpa-consent` | รายการหนังสือยินยอม (P-01) | ✓ |
| `#/pdpa-consent/create` | wizard สร้างใหม่ | ✓ |
| `#/pdpa-consent/create/copy-:id` | wizard อ้างอิงใบเดิม (ต้องเลือกความยินยอมใหม่ทุกข้อ) | ✓ |
| `#/pdpa-consent/edit/:id` | wizard แก้ไขร่างของตัวเอง | ✓ |
| `#/pdpa-consent/view/:id` | drawer ดูเอกสาร (P-03) | ✓ |

route ประกอบจากค่าคงที่ `ROOT` ใน JS → `applyRoute()` อ่าน hash ตอนโหลด/`hashchange` · ปิด drawer = กลับ route รายการ

## §3 Layout Shell
`#sidebar` (เมนู HR › หนังสือยินยอม PDPA + badge จำนวนงานค้าง `#sbBadge`) · shell bar (breadcrumb Core › HR › หนังสือยินยอม PDPA + ปุ่มแจ้งเตือน + user chip `#userMenu` / `#personaList`) · เนื้อหา `#page-content` · overlay root `#overlay-root`
- ผู้ใช้ปัจจุบันอัปเดตโดย `updateShell()` · สลับผู้ใช้ (เดโมเท่านั้น) `switchPersona()`
- responsive ≥1180 เต็ม · 768–1180 sidebar off-canvas ผ่าน `toggleSidebar()`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
`.ph` หัวเรื่อง + `.ph-actions` (ปุ่ม `ส่งออก CSV` → `exportCSV()` · ปุ่ม `#btnCreate` `สร้างหนังสือยินยอม` → `startWizard()`) › `.stats` 3 ใบ (`statCard()`) › `.filter-bar` (ค้นหา `#fq` → `onQ()` · ตัวกรองสถานะ/ผลความยินยอม/ฝ่าย สร้างโดย `initSelects()`) › `.table-wrap > .table` (เรียงด้วย `sortBy()`) › `.table-foot` แบ่งหน้า (`goPage()`)
- แถวทั้งแถวคลิกเปิด view (`rowClick()`) · ปุ่ม ⋮ `openRowMenu()` วาง `.row-menu` ใน `#overlay-root` ด้วยตำแหน่ง fixed
- คอลัมน์: เลขที่ (`.code-strong`) · วันที่ให้ความยินยอม · เจ้าของข้อมูล · ฝ่าย · ยินยอม n/N · ข้อมูลอ่อนไหว · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()` + `.sp-bar` `.sp-fill`)

### P-02 สร้าง/แก้ไข (`renderWizard()` ใน `#drawer` class `.drawer-panel` + `wide`)
`.dw-head` + `.d-stepper` (`.stepper-item` / `.stepper-circle`) › `.drawer-body` › `.dw-footer`
- ขั้น 1 `wizMain()` = `.wz-split` [ `.wz-main` : `.wz-card` ① ความยินยอมรายข้อ (`.att-ctl` ปุ่มช่วย → `setAllAns()` · `.trips` > `.trip` ต่อข้อ โดย `itemCard()` มี `.track-grid` > `.track-card` สองทาง → `setAns()` และคำอธิบายวัตถุประสงค์ใน `.pd-hint`) · `.wz-card` ② ข้อความที่ท่านรับทราบ (ถ้อยคำกฎหมาย อ่านอย่างเดียว) ] + `.wz-sum` การ์ดสรุปสด (`#sumDone` `#sumYes`) · ตัวนับในหัวการ์ด `#itDone`
- ขั้น 2 `wizAttach()` = `.upload-zone` + `#pdcFile` + `.file-row` ต่อไฟล์ (`pickFiles()` → `gateFiles()`)
- ขั้น 3 `wizReview()` = `.review-card` 3 ใบ (ข้อมูลหนังสือยินยอม · ความยินยอมรายข้อ · เอกสารแนบ)
- footer: `#btnNext` / `#btnDraft` (`saveDraft()`) / `#btnSaveSubmit` (`saveAndSubmit()`)

### P-03 ดู (`renderViewDrawer()`)
`.dw-head` (เลขที่ + `.pill` สถานะ + ยินยอม n/N) + `.dw-actions` › `.drawer-tabs` (`.drawer-tab` × 4 · `setTab()`) › `.drawer-body` › `.dw-footer`
- แท็บ `renderDetailTab()` ใช้ `.drawer-section` + `.drawer-fields`; แท็บ `renderPdfTab()` = `.a4 > .pdf-slot > .pdf-frame` (srcdoc) ปรับสูงด้วย `fitPdf()`; แท็บ `renderSignTab()` = `.timeline` (`.tl-item` `.tl-dot`); แท็บ `renderHistoryTab()` = ประวัติ append-only

## §5 Component Inventory
| component | anchor | หมายเหตุ |
|---|---|---|
| สถานะเอกสาร | `docPill()` → `.pill` | ร่าง · รอพิจารณา · ยินยอมแล้ว · ถอนความยินยอม · ไม่รับหนังสือ · ยกเลิก |
| ความคืบหน้าลายเซ็น | `renderSignProgress()` → `.sp-bar` `.sp-fill` | ร่างแสดง `—` |
| การ์ดความยินยอม 1 ข้อ | `itemCard()` → `.trip` + `.track-card` + `.tc-radio` | ป้าย `ข้อมูลอ่อนไหว (ม.26)` เมื่อข้อนั้นเป็นข้อมูลอ่อนไหว |
| การ์ดสรุปสด | `sumCard()` → `.wz-sum` | ข้อมูลจากระบบ ไม่ใช่ช่องกรอก |
| เมนูแถว | `openRowMenu()` → `.row-menu` `.rm-item` | portal ไป `#overlay-root` · ปิดด้วย `closeRowMenu()` |
| ตัวกรอง search-select | `initSelects()` → `.menu-fixed` | ใช้ helper กลางของ BASE-KIT |
| ปุ่มสถานะ busy | `.btn` + ไอคอน loader | ปุ่ม submit ถูก disable ระหว่างบันทึก |

## §6 Overlay Registry
| overlay | เปิดโดย | ปิดโดย | dismiss |
|---|---|---|---|
| `drawer` (`#drawer` + `#drawerBackdrop`) | `showDrawer()` | `closeDrawer()` · ปุ่มปิด · คลิก backdrop | wizard ที่แก้ค้างจะถาม `ทิ้งข้อมูลที่กรอกไว้?` ก่อน |
| `modal` (`#modal` + `#modalBackdrop` · `.modal-header-icon`) | `openModalCfg()` | `closeModal()` | คลิก backdrop ไม่ปิดถ้ากรอกเหตุผล/ความเห็นไว้ (`modalBackdropClick()`) |
| `row-menu` | `openRowMenu()` | คลิกที่อื่น / scroll | ปิดอัตโนมัติเมื่อ scroll |
| `user-menu` | `toggleUserMenu()` | คลิกนอกเมนู | prototype-only |
| `toast` (`#toast`) | `showToast()` | หมดเวลาเอง | — |

## §7 Interaction Spec
- คลิกแถว = เปิด view (ยกเว้นคลิกในคอลัมน์ปุ่ม ⋮)
- เลือกความยินยอมซ้ำค่าเดิม = ยกเลิกการเลือกข้อนั้น (`setAns()`)
- ปุ่ม `เลือกยินยอมทั้งหมด` / `ล้างที่เลือก` ทำงานกับทุกข้อพร้อมกัน
- ปิด drawer ระหว่างกรอก → modal ยืนยันทิ้งข้อมูล (`#btnDiscard`)
- หลังบันทึกร่างแล้วกดยืนยัน ระบบเปิด modal ยืนยันความยินยอมต่อให้อัตโนมัติ
- การถอนความยินยอม: เลือกข้อด้วย `.chip-row` > `.chip` (`toggleWdItem()` / `toggleWdAll()`) + เหตุผลบังคับที่ `#fReason`
- ทุก mutation มีสถานะ busy และกัน double-submit

## §8 State-Driven UI Matrix
| สถานะ | แบนเนอร์ | ปุ่มในหัว drawer | เมนูแถว |
|---|---|---|---|
| ร่าง | ยังเป็นร่าง — เลือกความยินยอมให้ครบ | ยกเลิก · แก้ไข · `#btnSubmitView` ยืนยันความยินยอม | แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| รอพิจารณา | รอ … พิจารณา | ไม่รับหนังสือ · รับหนังสือยินยอม (เฉพาะผู้พิจารณาขั้นปัจจุบัน) | พิมพ์ · ยกเลิกเอกสาร |
| ยินยอมแล้ว | (เตือนเมื่อไม่ยินยอมข้อมูลอ่อนไหว) | `#btnWithdrawView` ถอนความยินยอม | พิมพ์ · ถอนความยินยอม |
| ถอนความยินยอม | ถอนความยินยอม ข้อ … + เหตุผล | — | พิมพ์ |
| ยกเลิก / ไม่รับหนังสือ | แถบแดงพร้อมเหตุผล | — | พิมพ์ |
| แบบเอกสารปิดใช้งาน | `.alert-row` แดงบนหน้า list | ปุ่มสร้างถูก disable | — |

## §9 Microcopy (verbatim)
**ปุ่ม/ป้าย:** `สร้างหนังสือยินยอม` · `ส่งออก CSV` · `บันทึกแบบร่าง` · `ยืนยันความยินยอม` · `ถอนความยินยอม` · `ยกเลิกเอกสาร` · `ดาวน์โหลด PDF` · `พิมพ์` · `รายละเอียด` · `ลบไฟล์` · `ครบทุกข้อ` · `ยังไม่เลือก` · `ยินยอมครบ` · `มีข้อที่ไม่ยินยอม` · `ทุกสถานะ` · `ค้นหา...` · `เลขที่เอกสาร` · `วันที่ให้ความยินยอม` · `ฉบับของหนังสือ` · `สถานะ/ตำแหน่ง` · `สร้างโดย` · `เจ้าของข้อมูลส่วนบุคคล` · `ข้อมูลอ่อนไหว (ม.26)` · `รอฉันพิจารณา` · `รอเจ้าของข้อมูลยืนยัน` · `ที่คุณเกี่ยวข้อง` · `ลำดับการลงนาม` · `ความยินยอมมีผล` · `ถอนความยินยอมบางส่วน/ทั้งฉบับแล้ว` · `· ยืนยันแล้ว แก้ไขไม่ได้` · `ยังไม่มีข้อมูล`
**toast (คงที่):** `ไม่มีการแจ้งเตือนใหม่` · `แบบเอกสารนี้ยังไม่เปิดใช้งาน` · `แก้ไขได้เฉพาะร่างของตัวเอง — ใบที่ยืนยันแล้วแก้ไม่ได้` · `ต้องเลือกความยินยอมให้ครบทุกข้อ` · `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง` · `ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่` · `คุณไม่มีสิทธิ์ทำรายการนี้` · `ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
**toast (ประกอบกับเลขที่):** `บันทึกร่างแล้ว ·` · `บันทึกความยินยอมแล้ว ·` · `บันทึกผลแล้ว ·` · `บันทึกการถอนความยินยอมแล้ว ·` · `บันทึกว่าไม่รับหนังสือ ·` · `ยกเลิกเอกสารแล้ว ·` · `กำลังเปิดหน้าต่างพิมพ์ ·` · `ส่งออก` · `สลับเป็น`
**ข้อความเตือนในฟอร์ม:** `ต้องเลือกยินยอมหรือไม่ยินยอมข้อนี้` · `กรุณาระบุเหตุผล` · `กรุณาเลือกผู้พิจารณา` · `กรุณากรอกข้อมูลให้ครบถ้วน`
**ชุดเหตุผลสำเร็จรูป:** `เลือกความยินยอมไม่ครบทุกข้อ` · `ออกหนังสือฉบับใหม่แทน` · `ผู้สมัครยกเลิกการสมัครงาน` · `เปลี่ยนใจเฉพาะข้อมูลอ่อนไหว` · `เหตุผลที่ยกเลิก`
**ถ้อยคำจากแบบฟอร์ม (ห้ามแก้):** `หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล` · `ผลตรวจทางการแพทย์และผลตรวจสารเสพติด` · `ประวัติอาชญากรรม` · `ข้อมูลส่วนบุคคลตามข้อ 1-7`
**ค่าเดโม (prototype-only):** ชื่อสมมติ เช่น `เมธี จันทรสาร` · `ศิรประภา วงศ์วรรณ` · หน่วยงาน `ทรัพยากรบุคคล` · `บัญชี` · `ผู้สมัครงาน` · ตำแหน่ง `เจ้าหน้าที่ขาย` · คำตัดสินตาม role `ตรวจแล้ว` · ขั้นทดสอบจาก QA hook `ขั้นทดสอบ`
**เดือนไทยในแบบพิมพ์:** `กันยายน` · `ตุลาคม` · `พฤษภาคม` · `สิงหาคม` · `ธันวาคม` · ตัวย่อ `ก.พ.` · `พ.ค.` · `มิ.ย.`

## §10 Data Binding & BACKEND anchors
| จุดต่อ | anchor | API ปลายทาง (02_API) |
|---|---|---|
| รายการ + ตัวกรอง | `listRows()` · `canSee()` | `GET /pdpa-consent` |
| บันทึกร่าง / แก้ไข | `persist()` | `POST` / `PUT /pdpa-consent` |
| ยืนยันความยินยอม | `confirmSubmit()` · `resolveDoa()` (marker `DOA-ENGINE-HOOK`) | `POST /{id}/confirm` |
| พิจารณาตามขั้น | `confirmApprove()` · `confirmReason()` | `POST /{id}/decide` |
| ถอนความยินยอม | `confirmWithdraw()` · `isActiveConsent()` | `POST /{id}/withdraw` |
| แบบพิมพ์ | `pdcPrintData()` → `tplRender()` + `tplSignRows()` → `pdcPdfDoc()` · พิมพ์ด้วย `genPdf()` (`.pdf-gen`) | `GET /{id}/pdf` |
| ส่งออก | `exportCSV()` | `GET /pdpa-consent/export` |
| จำลอง API ล้ม (prototype) | `commitRejected()` | — |

## §11 Traceability + Drift Log
| หน้า/จุด | FRD |
|---|---|
| P-01 รายการ | 01_UI §1.2 P-01 · FN-10 |
| P-02 wizard | 01_UI §1.2 P-02 · FN-01/FN-02/FN-03 · BR-01 |
| P-03 ดู + 4 แท็บ | 01_UI §1.2 P-03 · FN-08 |
| ถอนความยินยอม | FN-06 · BR-03 · DEC-14 |
| เลือกผู้พิจารณาต่อขั้น (`.slot-row` + `.slot-help`) | FN-04 · DOA contract |

**⚠️ Drift Log**
| # | สิ่งที่ต่าง | สถานะ |
|---|---|---|
| D-01 | prototype มีตัวสลับผู้ใช้และ `window.__QA__` ซึ่งระบบจริงไม่มี | ตั้งใจ (prototype-only) |
| D-02 | prototype ยังไม่เรียก API จริง ใช้ seed ในหน่วยความจำ | ตั้งใจ |
| D-03 | แบบพิมพ์ในแท็บ PDF render ฝั่ง FE ส่วนระบบจริง render ฝั่ง server จาก template เดียวกัน | ตั้งใจ (print-spec §5) |
| D-04 | ยังไม่ได้ทดสอบด้วย browser จริง (โหมด NO-BROWSER) — ใช้ stub DOM smoke test แทน | ต้องรันรอบเต็มก่อนส่งลูกค้า |

## §12 Diff จากเวอร์ชันก่อน
ไม่มี — ฉบับแรกของ feature นี้

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. เพิ่มมุมมอง "ความยินยอมที่ยังมีผลของบุคคลหนึ่งคน" รวมทุกฉบับ เพื่อให้ module ปลายทางเรียกใช้ง่าย (รอบถัดไป · DEC-02)
2. ปุ่มดาวน์โหลดหลักฐานความยินยอมเป็นชุด (zip) สำหรับผู้ตรวจ
3. แจ้งเตือนเจ้าของข้อมูลเมื่อมีการออกฉบับใหม่ของหนังสือ เพื่อขอความยินยอมอีกครั้ง
