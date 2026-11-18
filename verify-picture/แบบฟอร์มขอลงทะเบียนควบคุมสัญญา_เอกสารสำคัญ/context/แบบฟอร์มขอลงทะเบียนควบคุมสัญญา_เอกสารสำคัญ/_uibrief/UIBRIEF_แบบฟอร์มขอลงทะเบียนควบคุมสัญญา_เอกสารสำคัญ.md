# UI_BRIEF — F-TMP-009 แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · self_audit PASS · [NO-BROWSER] e2e_standard/render-check ไม่ได้รัน → smoke jsdom 0 error |
| FRD | FRD_F-TMP-009_Pack v1.0 · DECISIONS.lock 14 มติ (DEC-01..14 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS`/`ROLE_HOLDERS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI CUBE Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF แบบพิมพ์)
| Variable | Value |
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
| ค่า | ใช้กับ |
|---|---|
| `1` | .stepper-item:not(:last-child)::after |
| `2` | .stepper-circle |
| `3` | .table-scroll.is-sticky thead th |
| `var(--z-backdrop)` | #drawerBackdrop, .drawer-backdrop, .ss-list, รมีปุ่ม action หลัก */ .modal-bac |
| `var(--z-drawer)` | #drawer, .drawer |
| `var(--z-dropdown)` | .info-tip::after, /* User dropdown menu */ .user-menu |
| `var(--z-modal)` | /* v9.1 Rule #62 — modal เหนือ drawer */ .modal-backdrop |
| `var(--z-popover)` | * เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .menu-fixed, .bd-pop, /* row menu ⋮ (portal ใน #ove |
| `var(--z-portal)` | .bd-pop |
| `var(--z-shell)` | .sidebar |
| `var(--z-sticky)` | .table-wrap thead th, .wizard-footer, .shell-bar |
| `var(--z-toast)` | #toast, .toast |

## §2 Route Map
| Route | หน้าที่ | refresh-safe |
|---|---|---|
| `#/contract-register` | P-01 รายการ (default) | ✓ |
| `#/contract-register/view/:id` | P-03 ดู (เปิด drawer ซ้อนบนรายการ) · ใบที่ไม่มีสิทธิ์ = ไม่เปิด | ✓ |
| `#/contract-register/create` | P-02 สร้าง | ✓ |
| `#/contract-register/edit/:id` | P-02 แก้ร่างของตน | ✓ |
ตัวจัดการ: `applyRoute()` + `go()` (`navigate()` / `getRoute()` ของ skeleton)

## §3 Layout Shell
sidebar `.sidebar` (module บริหารสัญญา › ลงทะเบียนควบคุมสัญญา + badge `#sbBadge` = งานรอฉัน) · topbar `.shell-bar` (breadcrumb Core › บริหารสัญญา › ลงทะเบียนควบคุมสัญญา · bell · user chip `.user-chip` + `.user-menu`) · content `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (title + `.ph-sub` + `.ph-count` badge ≤3 — ไม่มี stat cards) → `.card.list-card` > `.filter-bar` (ค้นหา `#fq` · `searchSelectHTML('fst')` สถานะ · `ftype` ประเภทสัญญา · `funit` หน่วยงาน · รีเซ็ต) → `.table-wrap` ตาราง 10 คอลัมน์ → `pager()` (`.table-footer` + `.pg-size-sel` 10/25/50)
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()` = `.wz-split` (การ์ด ① ประเภท `.opt-grid` · ② จุดประสงค์ `.opt-grid.is-3` + ช่องสาเหตุ · ③ คู่สัญญา/วันที่ `bedateHTML()`/หน่วยงาน `wunit`) + `sumCard()` · ขั้น 2 `wizAttach()` `.upload-zone` · ขั้น 3 `wizReview()`
### P-03 ดู — `renderViewDrawer()`
header (`.doc-ident` เลขที่ + `docPill()` · `.dw-sub` = ประเภท · ระยะสัญญา) · `tabBtn()` 4 แท็บ: `renderDetailTab()` · `renderPdfTab()` (`.pdf-frame` srcdoc จาก `ctrPdfDoc()`) · `renderSignTab()` · `renderHistoryTab()` · footer `.dw-footer`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตัวเลือก (radio card) | `optCard()` · `.track-card.opt-card` | ปกติ · `.is-on` · การ์ดแดง `.wz-card.is-bad` เมื่อยังไม่เลือก |
| ช่องวันที่ พ.ศ. | `bedateHTML()` · `.bedate` · popover `.bd-pop` | ว่าง (placeholder) · มีค่า · disabled วันนอกช่วง min/max |
| combobox | `searchSelectHTML()` / `initSearchSelect()` | ปิด · เปิด · กรอง · เลือกแล้ว |
| คน | `empChip()` · `.person-av` (วงกลม #111 + icon user) | — |
| ลายเซ็น x/y | `renderSignProgress()` · `.sign-prog` | ร่าง = — · ค้าง · ครบ · ยกเลิก `.is-bad` |
| สถานะ | `docPill()` | 6 สถานะ (§8) |
| ไฟล์แนบ | `fileRow()` · `.upload-zone` | ว่าง · มีไฟล์ · ไฟล์ไม่ผ่าน (toast) |
| การ์ดสรุปสด | `sumCard()` · `.wz-sum` | อัปเดตสด (`#sumParty` soft update) |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย | z |
|---|---|---|---|---|
| drawer view | `#drawer` `.drawer-panel` | 920 | ปุ่ม x · Esc · mousedown ที่ `#drawerBackdrop` (`drawerBackdropDown()`) | `var(--z-drawer)` |
| drawer wizard | `.drawer-panel.wide` | 1290 | เหมือนบน · กรอกค้าง → modal ทิ้งข้อมูล | `var(--z-drawer)` |
| modal | `#modal` / `#modalBackdrop` | 520 · `.is-lg` 680 (ส่ง) | ปุ่ม · Esc · mousedown ที่ backdrop (`modalBackdropDown()`) — ไม่ปิดถ้าพิมพ์เหตุผลค้าง | `var(--z-modal)` |
| row-menu ⋮ | `.row-menu` (portal `#overlay-root`) | 180 | คลิกนอก · scroll | `var(--z-dropdown)` |
| ปฏิทิน | `.bd-pop` | 280 | คลิกนอก · Esc (ปิดเฉพาะปฏิทิน) | `var(--z-popover)` |
| combobox list | `.ss-list` | ตามช่อง | คลิกนอก · Esc | `var(--z-portal)` |
| toast | `.toast` | — | อัตโนมัติ 2.8s | `var(--z-toast)` |
| user-menu | `.user-menu` | — | คลิกนอก | `var(--z-dropdown)` |

## §7 Interaction Spec
Esc chain: ปฏิทิน → modal → drawer · backdrop = mousedown เท่านั้น (U25) · แถวคลิกเปิด view (ยกเว้นคอลัมน์ ⋮) · พิมพ์ชื่อคู่สัญญา/สาเหตุ = soft update ไม่ rebuild (`setText()`) · เลือกวันเริ่มหลังวันสิ้นสุด → ล้างวันสิ้นสุด (`pickStart()`) · แก้ไขจาก view = ปิด view ก่อน (`editFromView()`) · ปุ่ม busy แสดง `loader-2`

## §8 State-Driven UI Matrix
| status | pill | ปุ่ม header (ผู้มีสิทธิ์) | ⋮ |
|---|---|---|---|
| draft | ร่าง (pill-muted) | เจ้าของ: ยกเลิก · แก้ไข · ส่งพิจารณา | แก้ไข · พิมพ์ · ยกเลิก |
| pending | รอพิจารณา (pill-warning) | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธ/คำอนุมัติตาม role · เจ้าของ/ผู้ดูแล: ยกเลิกเอกสาร | พิมพ์ · ยกเลิก |
| approved | รอลงทะเบียน (pill-info) | ผู้ดูแล: ลงทะเบียนควบคุม | พิมพ์ · ลงทะเบียนควบคุม |
| registered | ลงทะเบียนแล้ว (pill-success) | ผู้ดูแล: บันทึกรับต้นฉบับ | พิมพ์ · บันทึกรับต้นฉบับ |
| completed | ได้รับต้นฉบับแล้ว (pill-success) | — | พิมพ์ |
| cancelled | ยกเลิก (pill-muted) | — | พิมพ์ |
คำตัดสินตาม role (`wordsOf()`): default อนุมัติ/ไม่อนุมัติ · role-compliance รับทราบ/ส่งกลับแก้ไข

## §9 Microcopy (verbatim)
### toast
- กรุณากรอกข้อมูลให้ครบถ้วน
- บันทึกรับต้นฉบับแล้ว ·
- บันทึกร่างแล้ว ·
- ลงทะเบียนแล้ว ·
- สลับเป็น
- ส่งพิจารณาแล้ว ·
- ส่งออก
- แก้ไขได้เฉพาะร่างของตัวเอง
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- ไม่มีการแจ้งเตือนใหม่
- ส่งกลับเป็นร่างแล้ว · {เลขที่} · ยกเลิกเอกสารแล้ว · {เลขที่} · {คำอนุมัติ}แล้ว · {เลขที่}
### ปุ่ม / placeholder / label
- กลับไปกรอกต่อ
- ค้นหาเลขที่ / ผู้ขอ / คู่สัญญา / ทะเบียน
- ชื่อบริษัท/บุคคลคู่สัญญา
- ดาวน์โหลด PDF
- ถัดไป
- ทิ้งข้อมูล
- บริหารสัญญา
- บันทึกรับต้นฉบับ
- ปิด
- พิมพ์
- ยกเลิก
- ยกเลิกเอกสาร
- ย้อนกลับ
- รีเซ็ต
- ลงทะเบียนควบคุม
- วันนี้
- สร้างคำขอ
- ส่งพิจารณา
- ส่งออก CSV
- แก้ไข
- แก้ไข/เปลี่ยนแปลงเพราะอะไร
- ไม่บังคับ
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- ) — ส่งกลับเป็นร่าง
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]); if (canReceive(r)) items.push(['inbox', 'บันทึกรับต้นฉบับ',
- ]); if (canRegister(r)) items.push(['book-check', 'ลงทะเบียนควบคุม',
- ]]; /* DEC-11: ไม่มีทำซ้ำ */ if (isOwner(r) && r.status === 'draft') items.splice(0, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · ส่งแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กมลวรรณ ทดสอบ
- กรกฎาคม
- กรรมการผู้จัดการ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดตอนส่ง
- กุมภาพันธ์
- ขยายขอบเขตงานติดตั้งเพิ่ม 2 สาขา และปรับงวดชำระเงิน
- ขอร่างสัญญา/เอกสารแนบเพิ่ม
- ขอร่างสัญญาฉบับใหม่แนบมาด้วย
- ขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ
- ขั้น
- ขั้นทดสอบ
- ข้อมูลคู่สัญญาไม่ครบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักคำขอ
- ข้อมูลเอกสาร
- ข้าม
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- คู่สัญญา
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้ขอ / คู่สัญญา / ทะเบียน
- จัดทำสัญญาใหม่
- จุดประสงค์
- จุดประสงค์ร้องขอ
- ชนิดไฟล์ไม่รองรับ
- ชื่อ-สกุล
- ชื่อคู่สัญญา
- ชื่อบริษัท/บุคคลคู่สัญญา
- ชื่อฟังก์ชัน
- ณัฐวุฒิ จำลอง
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ถึง
- ทะเบียนควบคุม
- ทะเบียนควบคุมเลขที่
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกประเภทสัญญา
- ทุกสถานะ
- ทุกหน่วยงาน
- ธ.ค.
- ธนวัฒน์ ตัวอย่าง
- ธันวาคม
- บริษัท การเงินสมมติ จำกัด
- บริษัท ก่อสร้างสมมติ จำกัด
- บริษัท ค้าปลีกสมมติ จำกัด
- บริษัท ตัวอย่าง จำกัด
- บริษัท ตัวแทนจำหน่ายสมมติ จำกัด
- บริษัท ติดตั้งระบบตัวอย่าง จำกัด
- บริษัท ที่ปรึกษาจำลอง จำกัด
- บริษัท บริการทำความสะอาดสมมติ จำกัด
- บริษัท ประกันภัยตัวอย่าง จำกัด
- บริษัท ร่วมทุนพลังงานสมมติ จำกัด
- บริษัท วัตถุดิบตัวอย่าง จำกัด
- บริษัท เช่าเครื่องสำนักงานสมมติ จำกัด
- บันทึกผิด
- บันทึกรับต้นฉบับ/คู่ฉบับ
- บันทึกรับต้นฉบับแล้ว ·
- บันทึกร่างแล้ว ·
- บันทึกแก้ไขสัญญาว่าจ้าง ครั้งที่ 1.pdf
- ประวัติ
- ประวัติ (append-only)
- ประเภท
- ประเภทของสัญญา
- ประเสริฐ สมมุติ
- ปิด
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายจัดซื้อ
- ผู้จัดการฝ่ายบัญชี
- ผู้รับผิดชอบ
- ผู้ส่ง
- ผู้เชี่ยวชาญด้านบริหารสัญญา
- ฝ่ายขาย
- ฝ่ายจัดซื้อ
- ฝ่ายบริหารสัญญา
- ฝ่ายบัญชี
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิจารณาครบ — รอลงทะเบียนควบคุม
- พิมพ์
- พิมพ์ชนก สมมติ
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกฉบับเดิมและทำใหม่ทดแทน
- ยกเลิกสัญญาฉบับเดิมและทำฉบับใหม่ทดแทน
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — ส่งพิจารณาเมื่อข้อมูลครบ
- ยังไม่มีข้อมูล
- ยังไม่มีคำขอลงทะเบียนควบคุมสัญญา
- ยังไม่ส่ง
- ยื่นซ้ำกับใบอื่น
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รอผล
- รอพิจารณา
- รอลงทะเบียน
- ระยะสัญญา
- ระยะเวลา
- ระยะเวลาสัญญาไม่ถูกต้อง
- รับทราบ
- รายการ
- รายละเอียด
- ร่าง
- ลงทะเบียนควบคุม
- ลงทะเบียนควบคุมแล้ว ·
- ลงทะเบียนและได้รับต้นฉบับแล้ว
- ลงทะเบียนแล้ว
- ลงทะเบียนแล้ว ·
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่ขอ
- วันที่สิ้นสุด
- วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มต้น
- วันที่เริ่มต้น
- วันที่เริ่มต้นและสิ้นสุดสัญญา
- วิชัย ตัวอย่างดี
- ศิริพร ลองระบบ
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สร้าง PDF
- สร้างคำขอ
- สร้างคำขอเมื่อมีสัญญาหรือเอกสารสำคัญที่ต้องลงทะเบียน
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สัญญากู้ยืมเงิน
- สัญญาซื้อขาย
- สัญญารักษาความลับ
- สัญญารักษาความลับ (ฉบับลงนาม).pdf
- สัญญาร่วมทุน
- สัญญาว่าจ้าง
- สัญญาเช่าบริการ
- สัญญาแต่งตั้ง
- สายอนุมัติ (DOA)
- สาเหตุ
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- สิ้นสุดสัญญา
- ส่งกลับเป็นร่าง — แก้แล้วส่งใหม่
- ส่งกลับเป็นร่างแล้ว ·
- ส่งกลับแก้ไข
- ส่งพิจารณา
- ส่งพิจารณา?
- ส่งพิจารณาแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับจะกลับเป็นร่างเลขที่เดิม
- ส่งในระบบ
- หน่วยงาน
- หน่วยงานเจ้าของสัญญา
- หัวหน้า/ผู้จัดการ
- อนุมัติ
- อรอุมา ทดลองใช้
- อา
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่จัดซื้อ
- เจ้าหน้าที่บัญชี
- เดือนถัดไป
- เด้งกลับบน
- เบิก/ยืมเอกสาร
- เพิ่มเติม
- เพิ่มเอกสารแนบท้าย
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกจุดประสงค์ร้องขอ
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกประเภทของสัญญา
- เลือกประเภทและจุดประสงค์ แล้วใส่คู่สัญญาและระยะสัญญา — ผู้รับผิดชอบและวันที่ระบบใส่ให้
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกวันที่สิ้นสุด
- เลือกวันที่เริ่มต้น
- เลือกวันที่ได้รับ
- เลือกหน่วยงาน
- เหตุผลที่ยกเลิก
- เอกสารสำคัญอื่นๆ
- เอกสารแนบ
- แก้ไข/เปลี่ยนแปลง
- แก้ไข/เปลี่ยนแปลง ระบุสาเหตุ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้ขอว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แล้ว ·
- ได้รับต้นฉบับวันที่
- ได้รับต้นฉบับแล้ว
- ได้รับวันที่
- ไม่ทำสัญญาแล้ว
- ไม่ทำสัญญาแล้ว — คู่ค้าขอเลื่อนการแต่งตั้ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่ยกเลิก
- ไม่อนุมัติ

## §10 Data Binding & BACKEND anchors
| Prototype (mock) | ระบบจริง | API |
|---|---|---|
| `RECS` + `listRows()` + `canSee()` | GET รายการตามสิทธิ์ | API-01 · FN-11 |
| `findR()` | GET รายละเอียด | API-02 |
| `persist()` (SEQ → เลข CTR) | POST/PUT · ENG-DOC-NUM.next('CTR') | API-03/04 · FN-03 |
| `resolveDoa()` + `MOCK_DOA_RESOLVED` (DOA-ENGINE-HOOK) | GET /doa/resolve?feature_id=F-TMP-009 | API-05 · FN-04 |
| `confirmSubmit()` | POST submit (freeze approval_chain) | API-05 |
| `confirmApprove()` | POST approve | API-06 · FN-05 |
| `confirmReason()` (reject → กลับร่าง / cancel) | POST reject / cancel | API-07/08 · FN-06/07 |
| `confirmRegister()` (REG_SEQ → เลขทะเบียน) | POST register · ENG-DOC-NUM (รูปแบบ OQ-06) | API-09 · FN-08 |
| `confirmReceive()` | POST receive | API-10 · FN-08 |
| `docPrintData()` + `tplRender()` + `CTR_TPL` | server render template เดียวกัน | API-11 · FN-09 |
| `exportCSV()` | GET export.csv | API-12 |
| `pickFiles()` + `gateFiles()` | Document Center | API-13 |
| `DOC.active` | F-DOCCFG status ของ doc_type CTR | FN-03 |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01 §1.1 · API-01/12 | `renderPage()` |
| §4 P-02 | 01 §1.2 · API-03/04 · VR-01..06 | `renderWizard()` · `validateMain()` |
| §4 P-03 | 01 §1.3 · API-02/11 | `renderViewDrawer()` |
| §6 M-01 ส่ง | API-05 · BR-05 | `openSubmit()` · `.slot-row` |
| §6 M-02/03 ตัดสิน | API-06/07 · BR-06/07 | `openApprove()` · `openReject()` |
| §6 M-05/06 ผู้ดูแล | API-09/10 · BR-09/10 | `openRegister()` · `openReceive()` |
| §8 สถานะ | 05 §5.2 | `DOC_ST` |
| PDF | FN-09 · BR-12 | `docPrintData()` · `tplSignRows()` |

| Drift | รายการ | ประเภท |
|---|---|---|
| D-01 | `window.__QA__` · `switchPersona()` · `S.sim` · mock master | prototype-only — ไม่ต้องสร้าง |
| D-02 | ผู้เชี่ยวชาญด้านบริหารสัญญาและผู้ดูแลสัญญาเป็นคนเดียวกันใน mock (E05) | prototype-only — ระบบจริงแยกตามสิทธิ์/DOA (OQ-03) |

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก (v1.0) — ไม่มี diff

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- เพิ่มช่องอ้างอิงทะเบียนเดิมเมื่อจุดประสงค์ = เบิก/ยืม · แก้ไข · ยกเลิกทำใหม่ (รอ OQ-04)
- แจ้งเตือนสัญญาใกล้หมดอายุจาก contract_end (Phase 2)
- คอลัมน์ "ค้างส่งต้นฉบับ (วัน)" สำหรับผู้ดูแลสัญญา
