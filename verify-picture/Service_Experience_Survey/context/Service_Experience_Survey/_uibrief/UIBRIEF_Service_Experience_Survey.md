# UI_BRIEF — F-TMP-006 Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)
> AS-BUILT จาก `feature.html` (html-generator-v9.4 · archetype **Q-form** · `window.__QA__`) — ทุกบรรทัด trace กลับหา selector/function/ข้อความจริงได้ · ใช้คู่ FRD_F-TMP-006_Pack

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | feature.html (Q-form · audit FAIL 0 · prune_css แล้ว) |
| FRD | FRD_F-TMP-006_Pack v1.0 (01_UI P-01..03 · 02_API API-01..09 · 05_RULES) |
| มติ | DECISIONS.lock 14 DEC (AI-DEFAULT 10 · VALID 4) |
| Drift | 2 รายการ prototype-only (§11) · ไม่มี business drift |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` / `commitRejected()` จำลอง API error — ระบบจริงลบออก |

## §1 Design Tokens AS-BUILT
CI = CUBE Warm Light (ห้ามแก้) · font: Noto Sans Thai + Satoshi · PDF ใช้ Sarabun (thai-doc)
| CSS var | ค่า |
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

### z-index map (สูง → ต่ำ)
| ค่า | selector |
|---|---|
| var(--z-toast) | .toast |
| var(--z-toast) | #toast |
| var(--z-popover) | เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu ut |
| var(--z-popover) | verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body) /  |
| var(--z-popover) | .row-menu |
| var(--z-modal) | .modal-backdrop |
| var(--z-drawer) | .drawer |
| var(--z-drawer) | #drawer |
| var(--z-backdrop) | .ss-list |
| var(--z-backdrop) | .drawer-backdrop |
| var(--z-backdrop) | รมีปุ่ม action หลัก /  .modal-backdrop |
| var(--z-backdrop) | #drawerBackdrop |
| var(--z-dropdown) | .user-menu |
| var(--z-dropdown) | .info-tip::after |
| var(--z-shell) | .sidebar |
| var(--z-sticky) | .shell-bar |
| var(--z-sticky) | .table-wrap thead th |
| var(--z-sticky) | .wizard-footer |
| 3 | .table-scroll.is-sticky thead th |
| 2 | .stepper-circle |
| 1 | .stepper-item:not(:last-child)::after |
| var(--z-portal) | .bd-pop |

## §2 Route Map
| route | หน้า | handler |
|---|---|---|
| `#/sa-csat-ovs` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/sa-csat-ovs/create` | P-02 สร้าง (drawer wide) | `startWizard()` |
| `#/sa-csat-ovs/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft เท่านั้น) | `startWizard()` |
| `#/sa-csat-ovs/view` · `#/sa-csat-ovs/view/:id` | P-03 ดู (ไม่มีสิทธิ์ = ไม่เปิด drawer) | `openView()` · `canSee()` |
refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go('sa-csat-ovs')`

## §3 Layout Shell
- `.sidebar` (โมดูล Sales · เมนู "ประเมิน Sales Admin ต่างประเทศ" + `#sbBadge` = จำนวนร่างของฉัน) · `.shell-bar` breadcrumb Core › Sales › แบบประเมินความพึงพอใจ Sales Admin ต่างประเทศ · `.user-chip` (คน = วงกลมรูปคน `#ucAv`) → `.user-menu` (สลับผู้ใช้ — prototype)
- `#page-content` (`.content`) · `#drawer` + `#drawerBackdrop` · `#modalBackdrop` > `#modal` · `#toast` · `#overlay-root` (portal)

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (`.ph-title` + `.ph-en` · `.ph-sub` + `.ph-badge` "N รายการ · ร่าง n") · `.ph-actions` [ส่งออก CSV `exportCSV()` · สร้างแบบประเมิน `#btnCreate` → `startWizard()`] → `.seg` segmented tabs (`segTabs()` · `.seg-btn.on` · `.seg-n`) → `.card.list-card` [`.filter-bar`: `#fq` ค้นหา · `searchSelectHTML('fmonth')` · `searchSelectHTML('femp')` · รีเซ็ต `resetFilters()`] → `.table-wrap` > `.table` (`sortTh()` คลิกเรียง) → `pager()` (`.tf-size` 10/25/50 + `.pagination`)
- แถว `.is-clickable` → `rowClick()` → `openView()` · คอลัมน์สุดท้าย `.row-actions-cell` ปุ่ม ⋮ → `openRowMenu()`
### P-02 สร้าง/แก้ — `renderWizard()`
`.dw-head` (eyebrow + `.dw-title` + `stepper()` `.d-stepper` 3 ขั้น) → `.drawer-body.is-soft` → ขั้น 1 `wizMain()`: `.wz-split` = `.wz-main` (`STEPH()` + `.wz-card` ①–③) + `sumCard()` `.wz-sum` · ขั้น 2 `wizAttach()` `.upload-zone` + `#seaFile` · ขั้น 3 `wizReview()` `.review-card` × 4 → `.dw-footer` (ย้อนกลับ `wizBack()` · ยกเลิก `closeDrawer()` · ถัดไป `#btnNext` `wizNext()` / `#btnDraft` `saveDraft()` + `#btnSaveSubmit` `saveAndSubmit()`)
- การ์ด ① "ประจำเดือนและลูกค้า": `#fMonth` (`searchSelectHTML('wmonth')` · ประจำเดือน (Month) · ค่าเริ่มเดือนปัจจุบัน) · `#fCust` (`searchSelectHTML('wcust')` · ชื่อลูกค้า (Company Name)) · `#fContact` (input `contact` · ผู้ติดต่อ (Contact Person) · `setF2()`) — ไม่มีช่องวันที่ (DEC-12)
- การ์ด ②③④ ต่อกลุ่ม (`SECTIONS` 3 กลุ่ม: COMMUNICATION & RESPONSIVENESS · DOCUMENTATION & EXECUTION · PROFESSIONALISM): `.rate-head` ("1 = Very Dissatisfied · 5 = Very Satisfied" + 1 · 2 · 3 · 4 · 5) + `.rate-list` > `rateRow()` `.rate-row#rr-{q_key}` (q1…q10) > `.rate-seg` > `.rate-btn[data-q][data-v]` (ค่า 1–5) → `setScore()` · `#secAns{n}` "ตอบ x/n"
- การ์ด ⑤ Additional Feedback: textarea `comment` → `setF2()`
- `.wz-sum`: `#sumAns` (x/10) · `#sumLow` · `sumSec` + เลขกลุ่ม 1–3 (เฉลี่ยต่อกลุ่ม) · `#sumTotalBox`/`#sumTotal`
### P-03 ดู — `renderViewDrawer()`
`.dw-head` (`.doc-ident` + `.dw-title` เลขที่ + `docPill()` · `.dw-sub` ประจำเดือน · คะแนนเฉลี่ย · `.dw-actions`) → `.drawer-tabs` (`tabBtn()` detail/pdf/sign/history) → `.drawer-body` → `.dw-footer`
- รายละเอียด `renderDetailTab()`: `viewBanner()` · `SEC()` ข้อมูลเอกสาร (เลขที่ · สถานะ · ประจำเดือน · วันที่บันทึก) · ลูกค้า (Company Name · Contact Person · ผู้บันทึก `empChip()`) · 3× `scoreTable()` `.score-tbl` (หัวคอลัมน์ = ชื่อกลุ่ม + 1–5) (`.score-mark` ✓ · `.is-low`) · Additional Feedback `commentBox()` · เอกสารแนบ `fileRow()` · ข้อมูลระบบ
- PDF `renderPdfTab()`: `.pv-bar` + `.a4` > `.pdf-slot` > `iframe.pdf-frame[srcdoc]` (`fitPdf()`) · ดาวน์โหลด/พิมพ์ `genPdf()`
- ลายเซ็น / อนุมัติ `renderSignTab()`: `.review-card` (สาย DOA "ไม่มี · 0 ขั้น" · `renderSignProgress()`) + `.timeline`
- ประวัติ `renderHistoryTab()`: `.timeline` append-only

## §5 Component Inventory
| component | anchor | states |
|---|---|---|
| segmented tabs | `.seg` `.seg-btn` | default · hover · `.on` (dot primary + count primary) |
| search combobox | `searchSelectHTML()` · `initSearchSelect()` · `.ss-list` (portal) | closed · open · filtered · empty · selected · clear |
| ช่องข้อความ | `.input[name=contact]` | ปกติ · `.is-invalid` (VR-03) |
| ปุ่มเลือกคะแนน 1–5 | `.rate-btn` | default · hover · `.is-on` (พื้น #111111) · แถว `.is-bad` (ขาดตอนบันทึกผล) |
| สรุปสด | `.wz-sum` · `.wz-sum-total` | `.is-off` (ยังไม่ตอบ) |
| pill สถานะ | `docPill()` | draft `pill-muted` · recorded `pill-success` · cancelled `pill-danger` |
| คน | `empChip()` `.emp-av` (วงกลมรูปคน) | — |
| ลูกค้า | `custChip()` `.org-ic` | ยังไม่ได้เลือก |
| row menu | `openRowMenu()` `.row-menu` `.rm-item` | `.is-danger` (ยกเลิกเอกสาร) |
| ปุ่ม submit | `busyLabel()` · `loader-2` | ปกติ · disabled+กำลังบันทึก… |
| empty | `emptyStateHTML()` | ไม่มีข้อมูล · ค้นหาไม่พบ |

## §6 Overlay Registry
| overlay | anchor | ขนาด | เปิด | ปิด / dismiss |
|---|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer.drawer-panel.wide` | 1290 | `startWizard()` | X · ยกเลิก · Esc · backdrop **mousedown** `drawerBackdropDown()` — กรอกค้าง (`S.dw.dirty`) → modal ทิ้งข้อมูล |
| drawer ดู | `#drawer.drawer-panel` | 920 | `openView()` | X · ปิด · Esc · backdrop mousedown |
| modal บันทึกผล | `#modal.modal.is-lg` | 680 | `openSubmit()` | ยกเลิก · Esc · backdrop mousedown `modalBackdropDown()` |
| modal ยกเลิก | `#modal` | 520 | `openCancel()` | ไม่ยกเลิก · Esc · backdrop (มีเหตุผลค้าง = ไม่ปิด) |
| modal ทิ้งข้อมูล | `#modal` | 520 | `closeDrawer()` เมื่อ dirty | กลับไปกรอกต่อ / ทิ้งข้อมูล |
| row menu | `.row-menu` (portal `#overlay-root`) | 180 | `openRowMenu()` | คลิกที่อื่น · scroll · `closeRowMenu()` |
| combobox list | `.ss-list` (portal) | ตามช่อง | `ssOpen()` | คลิกที่อื่น · Esc |
| ปฏิทิน | `.bd-pop` (base-kit · ไม่ใช้ในฟอร์มนี้ — ไม่มีช่องวันที่) | 280 | — | — |
| user menu | `.user-menu` | — | `toggleUserMenu()` | คลิกที่อื่น |
| toast | `#toast.toast` | — | `showToast()` | auto ~2.8s |

## §7 Interaction Spec
- Esc chain (ตามลำดับจริง): ปฏิทิน `.bd-pop` (capture · stopPropagation) → combobox `ssOnKey()` → modal (`state.modal.open` → `closeModal()`) → drawer (`closeDrawer()` — wizard dirty เปิด modal ทิ้งข้อมูล)
- backdrop ปิดด้วย mousedown ที่ backdrop เท่านั้น (U25) — ลากจากในออกนอกไม่ปิด
- render รักษา scroll/focus: `preserveRenderState()` / `restoreRenderState()` · พิมพ์ข้อความ/เลือกคะแนน = soft update (`setF2()` · `setScore()`)
- ประจำเดือนค่าเริ่ม = เดือนปัจจุบัน (`blankForm()`) · เลือกเดือน `pickMonth()` · เลือกลูกค้า `pickCust()` · พิมพ์ผู้ติดต่อ `setF2('contact')`
- U15: แก้ไขจาก view = `editFromView()` ปิด view ก่อนเปิด wizard

## §8 State-Driven UI Matrix
| สถานะ | pill | ปุ่ม header (view) | row menu | แก้ไข |
|---|---|---|---|---|
| draft (เจ้าของ) | ร่าง | ยกเลิก · แก้ไข · บันทึกผล | ดูรายละเอียด · แก้ไข · พิมพ์ · ยกเลิกเอกสาร | ✓ |
| draft (role-mgr-sales) | ร่าง | — | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร | ✗ |
| recorded | บันทึกผลแล้ว | ยกเลิกเอกสาร (เจ้าของ/role-mgr-sales) | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร | ✗ (ล็อก) |
| cancelled | ยกเลิก | — | ดูรายละเอียด · พิมพ์ | ✗ |
การมองเห็น: `canSee()` = role-mgr-sales ∨ เจ้าของ (ร่างของคนอื่นไม่เห็น) · `canCancel()` · `isOwner()`

## §9 Microcopy (verbatim)
### toast
| ข้อความ | variant |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | info |
| เลือกคะแนนให้ครบ ${QKEYS.length} ข้อก่อนบันทึกผล (ขาด ${QKEYS.length - answered(r.scores)} ข้อ) | warning |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | warning |
| แก้ไขได้เฉพาะร่างของตัวเอง | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| เลือกคะแนนให้ครบ ${QKEYS.length} ข้อก่อนบันทึกผล | warning |
| บันทึกผลแล้ว · | info |
| ยกเลิกเอกสารแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |

### ปุ่ม
Sales · กลับไปกรอกต่อ · ดาวน์โหลด PDF · ถัดไป · ทิ้งข้อมูล · บันทึกผล · บันทึกแบบร่าง · ปิด · พิมพ์ · ยกเลิก · ยกเลิกเอกสาร · ย้อนกลับ · รีเซ็ต · วันนี้ · สร้างแบบประเมิน · ส่งออก CSV · แก้ไข · ไม่ยกเลิก

### placeholder
ค้นหาเลขที่ / ลูกค้า / ผู้ติดต่อ / ผู้บันทึก · ชื่อผู้ตอบแบบประเมินฝั่งลูกค้า · เหตุผลที่ยกเลิก · ไม่บังคับ

### ถ้อยคำตามแบบฟอร์ม FM-SAL-22 (ภาษาอังกฤษ — ตรงกระดาษ · DEC-14)
- Service Experience Survey
- COMMUNICATION & RESPONSIVENESS
- DOCUMENTATION & EXECUTION
- PROFESSIONALISM
- Communication clarity
- Response time to inquiries
- Follow-up consistency
- Accuracy of documents
- Timeliness of document submission
- Shipment coordination support
- Effectiveness in resolving issues
- Proactive service updates
- Professionalism of our team
- Overall service satisfaction
- Additional Feedback
- 1 = Very Dissatisfied · 5 = Very Satisfied

### ข้อความบนจอ (label + ข้อความระบบ)
- ก.ค.
- ก.พ.
- ก.ย.
- กมลวรรณ ใจเย็น
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นทดสอบ
- ข้อ — จะแจ้งผู้จัดการฝ่ายขาย
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลระบบ
- ข้อมูลหลักแบบประเมิน
- ข้อมูลเอกสาร
- ความคืบหน้า
- คะแนน ≤ 2
- คะแนนเฉลี่ย
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาเลขที่ / ลูกค้า / ผู้ติดต่อ / ผู้บันทึก
- ชนิดไฟล์ไม่รองรับ
- ชื่อผู้ตอบแบบประเมินฝั่งลูกค้า
- ชื่อฟังก์ชัน
- ญี่ปุ่น
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตอบ
- ตอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้อง
- ทั้งหมด
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกเดือน
- ธ.ค.
- ธนพล รอบคอบ
- ธันวาคม
- บันทึกซ้ำ
- บันทึกซ้ำ — ใบที่ถูกต้องคือ SEA-2569-0006
- บันทึกผลเมื่อลูกค้าต่างประเทศตอบแบบประเมิน
- บันทึกผลแบบประเมิน
- บันทึกผลแบบประเมิน?
- บันทึกผลแล้ว
- บันทึกผลแล้ว ·
- บันทึกผลแล้ว ล็อกแก้ไข
- บันทึกผลแล้ว — ยกเลิกแล้วไม่นับในสรุปผล
- บันทึกผลแล้ว — ใช้ในสรุปผลการประเมินความพึงพอใจ
- บันทึกผลแล้วแก้ไขไม่ได้ — ถ้าต้องเปลี่ยน ให้ยกเลิกแล้วสร้างใหม่
- บันทึกผิดลูกค้า
- บันทึกร่างแล้ว ·
- ประจำเดือน
- ประวัติ
- ปิด
- ผู้จัดการฝ่ายขาย
- ผู้บันทึก
- ผู้บันทึกทุกคน
- ฝ่ายขาย
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิจารณาในระบบ
- พิมพ์
- พิมพ์ชื่อหรือรหัสลูกค้าต่างประเทศ
- ฟิลิปปินส์
- ม.ค.
- มกราคม
- มาเลเซีย
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่บันทึกผล
- ยังไม่มีข้อมูล
- ยังไม่มีคะแนนต่ำ
- ยังไม่มีแบบประเมินความพึงพอใจ
- ยังไม่ได้เลือก
- ย้อนกลับ
- รอบันทึกผล
- รายการ
- รายละเอียด
- ร่าง
- ร่างของฉัน
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการบันทึก
- ลูกค้า
- ลูกค้าขอแก้คำตอบ — สร้างใบใหม่
- ล้างตัวกรอง
- วรวุฒิ ทองดี
- วันที่ ........./........./.........
- วันที่บันทึก
- ส.ค.
- สถานะ
- สมศรี ตั้งใจดี
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบประเมิน
- สลับเป็น
- สิงคโปร์
- สิงหาคม
- ส่งออก
- ออสเตรเลีย
- อา
- เดือนถัดไป
- เดือนนี้
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกเดือน
- เวียดนาม
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขเอกสาร
- แก้ไขแบบประเมิน
- แก้ไขได้เฉพาะร่างของตัวเอง
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี · 0 ขั้น
- ไม่มีขั้นอนุมัติ
- ไม่มีข้อเสนอแนะ

## §10 Data Binding & BACKEND anchors
| จุด | mock ใน HTML | API จริง (02_API) |
|---|---|---|
| รายการ + count tabs | `RECS` · `listRows()` · `baseRows()` | API-01 |
| รายละเอียด | `findR()` | API-02 |
| บันทึกร่าง / แก้ร่าง | `persist()` (ENG-DOC-NUM ครั้งแรก) | API-03 / API-04 |
| บันทึกผล | `confirmSubmit()` | API-05 (+ sea_low_score_recorded) |
| ยกเลิก | `confirmReason()` | API-06 (+ sea_cancelled) |
| PDF | `docPrintData()` + `tplRender()` + `SEA_TPL` | API-07 (server render template เดียวกัน) |
| CSV | `exportCSV()` | API-08 |
| แนบไฟล์ | `pickFiles()` · `gateFiles()` | API-09 · Document Center |
| ลูกค้า | `CUSTOMERS` · `custOf()` | Customer master API (อ่าน) |
| DOA | `MOCK_DOA_RESOLVED` (0 ขั้น) · `resolveDoa()` | ไม่มี (DEC-03) |
| สถานะแบบเอกสาร | `DOC.active` | F-DOCCFG status |
markers: ENG-DOC-NUM · ENG-NOTIFY · DOA-ENGINE-HOOK (0 ขั้น)

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/08 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/05 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/06/07 | `renderViewDrawer()` |
| §8 | 05 §5.2/§5.3 | `canSee()` · `canCancel()` |
| §9 คะแนนต่ำ | 05 BR-04 | `lowCount()` · `viewBanner()` |
### ⚠️ Drift Log
| # | ชนิด | รายละเอียด | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only (prototype) | `window.__QA__` · `switchPersona()` · `commitRejected()` | ลบในระบบจริง |
| D-02 | HTML-only (archetype) | `MOCK_DOA_RESOLVED` 0 ขั้น + แท็บ "ลายเซ็น / อนุมัติ" แสดง "ไม่มี · 0 ขั้น" — ตามโครง Q-form (#101/#108) แม้ DEC-03 ไม่มีการอนุมัติ | ยืนยันกับทีม (OQ-07) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ถ้าลูกค้าต้องการให้ผู้จัดการ "รับทราบ" ผลประเมิน · ถ้าต้องการแบบพิมพ์สองภาษา เพิ่ม profile/label ไทยใต้ป้ายอังกฤษ (OQ-08) → ตั้ง DOA กลาง 1 ขั้น (role-mgr-sales) ได้ทันทีเพราะโครง Q-form รองรับ N ขั้นอยู่แล้ว (ต้องทำ DOA_BRIEF + แก้ DEC-03)
