# HTML_UI_BRIEF — F-PUR-PO · ใบสั่งซื้อ (F078)

> **EXTRACTION-BASED** — ทุกบรรทัดสกัดจาก `01_HTML/F-PUR-PO.html` จริง · trace กลับหา selector / function / ข้อความได้ทุกข้อ
> **ห้ามแต่งสเปคเอง** — ถ้าเห็นว่าควรต่างจากนี้ ให้เปิด Open Question ไม่ใช่เขียนทับ
> **คู่กับ:** `01_UI.md` (Layout Decision Log) · HTML คือ source of truth

---

## 1. Design Tokens (verbatim จาก `:root`)

### 1.1 สี — CUBE Warm Light

| Token | ค่า | ใช้ที่ |
|---|---|---|
| `--c-primary` | `#FF3B30` | ปุ่มหลัก · แถบ active ของ sidebar · เลขเอกสารที่ออกแล้ว |
| `--c-primary-hover` | `#E62E24` | hover ของปุ่มหลัก |
| `--c-primary-08` / `--c-primary-12` | `rgba(255,59,48,0.08 / 0.12)` | พื้นอ่อนของรายการที่ highlight |
| `--c-danger` | `#E62E24` | ปุ่ม/ข้อความอันตราย (ยกเลิก · ไม่อนุมัติ) |
| `--c-danger-08` | `rgba(230,46,36,0.08)` | พื้น banner อันตราย |
| `--c-warning` | `#E8870F` | คำเตือน (เกินงบ · รับเกิน) |
| `--c-warning-08` | `rgba(232,135,15,0.10)` | พื้น banner เตือน |
| `--c-ok` / `--c-success` | `#1F9D55` | สำเร็จ · รับครบ · อนุมัติแล้ว |
| `--c-ok-08` | `rgba(31,157,85,0.10)` | พื้น banner สำเร็จ |
| `--c-teal` / `--c-purple` | `#FF9A1F` | แกนรอง (ส้ม) — สถานะกลางทาง |
| `--c-teal-08` | `rgba(255,154,31,0.10)` | พื้นแกนรอง |
| `--c-teal-light` | `#FFB763` | แถบความคืบหน้าอ่อน |
| `--c-ink` / `--c-text` / `--c-navy` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-text-mute` | `#54565C` | ตัวอักษรรอง |
| `--c-mute-2` / `--c-slate` | `#73757B` | label · หน่วย |
| `--c-mute-3` / `--c-text-soft` | `#9A9CA2` | placeholder · icon จาง |
| `--c-line` / `--c-border` | `#DEDAD4` | เส้นขอบหลัก |
| `--c-line-2` / `--c-border-soft` | `#E9E5E0` | เส้นคั่นภายใน |
| `--c-line-3` | `#F1EEEA` | พื้น hover ของแถว |
| `--c-bg-off` / `--c-off-white` | `#FAF8F5` | พื้นหลังหน้า |
| `--c-white` | `#FFFFFF` | พื้นการ์ด/drawer |

> **ห้าม hardcode hex ในโค้ดหน้า** — ใช้ token เสมอ (Iron Rule #1 · L-04)
> ข้อยกเว้นเดียวที่พบคือ `var(--c-line, #E7E2DB)` ซึ่งเป็น **fallback ของ BASE-KIT เอง** (ยกมา verbatim ห้ามแก้)

### 1.2 z-index registry (ประกาศครบใน `:root`)

| Token | ค่า | ชั้น |
|---|---|---|
| `--z-content` | 1 | เนื้อหาปกติ |
| `--z-sticky` | 10 | หัวตาราง sticky |
| `--z-shell` | 20 | sidebar · shell bar |
| `--z-dropdown` | 30 | เมนูแถว (`.row-menu`) |
| `--z-backdrop` | 50 | ฉากหลัง drawer |
| `--z-drawer` | 51 | `.overlay-wrap` (ตัวถือ drawer) |
| `--z-modal` | 60 | `.modal-overlay` |
| `--z-popover` | 70 | `.combo-pop` · `#item-pop` |
| `--z-toast` | 80 | `.toast` |

> **สำคัญ:** `.drawer-panel` เองเป็น `position:absolute; z-index:auto` — **ชั้นซ้อนเป็นของ `.overlay-wrap`** (#95 Overlay Portal)
> จึงทำให้ modal (60) อยู่เหนือ drawer (51) เสมอ · **ยืนยันด้วย `getComputedStyle` + `elementFromPoint` แล้ว**

### 1.3 รูปทรงและเงา

| Token | ค่า |
|---|---|
| `--r` | `8px` (รัศมีมุมมาตรฐาน) |
| `--sh-md` | `0 6px 20px rgba(17,17,17,0.10)` |
| `--sh-lg` | `0 12px 32px rgba(17,17,17,0.12)` — dropdown · เมนู |
| `--sh-xl` | `0 24px 64px rgba(17,17,17,0.28)` — drawer · modal |

### 1.4 ตัวอักษร

| ใช้กับ | stack |
|---|---|
| ทั่วไป | `'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` |
| ไทยล้วน | `'Noto Sans Thai', sans-serif` |
| ตัวเลข/รหัส (`.tbl-mono`) | `ui-monospace, 'SFMono-Regular', Menlo, monospace` |

> คอลัมน์ตัวเลขใช้ `tabular-nums` + ชิดขวาเสมอ

---

## 2. Geometry

| ส่วน | ค่าจริงที่วัดได้ |
|---|---|
| Sidebar | `var(--sidebar-w)` · เต็มความสูง · พื้นเข้ม |
| Shell bar | สูง `52px` (fallback `var(--shellbar-h, 52px)`) |
| **Drawer ดูรายละเอียด** | **920px** (วัดจริง) |
| **Drawer สร้าง/แก้ (`.wide`)** | **1290px** · responsive `min(1290px, 100vw)` |
| Modal ยืนยัน | 440px |
| Dropdown (`.combo-pop`) | `position:fixed` · `max-height:280px` · `overflow-y:auto` · กว้าง ≥ 340px |
| `.row-menu` | `position:fixed` · `min-width:190px` · z `--z-dropdown` |
| แถวตาราง list | สูง **63px** (2 บรรทัด — เลขที่+วันที่ / ชื่อ+รหัส) |
| Breakpoint | `1180px` (media query #97) |

---

## 3. Route Map

| route | หน้า | ฟังก์ชันเปิด |
|---|---|---|
| `#/` หรือ `#/list` | หน้ารายการ | `renderListPage()` |
| `#/create` | wizard สร้างใหม่ | `openCreateDrawer()` |
| `#/create/:id` | wizard แก้ไข (เริ่มขั้น 2) | `openCreateDrawer(editId)` |
| `#/view/:id` | drawer รายละเอียด | `openViewDrawer(id)` |

`getRoute()` [`:3571`](../01_HTML/F-PUR-PO.html#L3571) แตก hash เป็น `{name, id}` · `navigate(route)` เปลี่ยน hash
**หน้า list เป็นฉากหลังเสมอ** — overlay ทั้งหมดอยู่ใน `#overlay-root`

---

## 4. Anatomy รายหน้า (selector จริง)

### 4.1 หน้ารายการ

| ส่วน | selector / function |
|---|---|
| แถบสรุป 4 ตัว | `.stat` (4 ใบ) |
| แถบกรอง | `.toolbar` → `.search-box` + `<select>` × 3 + ปุ่ม `ล้างตัวกรอง` |
| ตาราง | `.tbl` ใน `.table-wrap` (`overflow-y:auto`) |
| สถานะเอกสาร | `docPill(status)` → `.pill.pill-{muted\|warning\|success\|danger}` |
| ความคืบหน้าลายเซ็น | `renderSignProgress()` → `n/N` + แถบ |
| เมนูแถว | `openRowMenu(id, e)` → `.row-menu` (**flip-up อัตโนมัติ**) |
| empty state | `emptyStateHTML()` → `.empty-icon` |
| เรียงคอลัมน์ | `sortBy(key)` → `renderTableOnly` (ไม่ re-render ทั้งหน้า) |

### 4.2 Wizard (drawer `.wide`)

| ส่วน | selector / function |
|---|---|
| หัว | `.dw-head` → `.dw-eyebrow` + `.dw-title` + ปุ่มปิด `.top-icon-btn` |
| stepper | `.d-stepper` → `renderStepperItem(n, label)` → `.step` · `.step-dot` (`.is-current` / `.is-done`) |
| เนื้อ | `.drawer-body` → `renderStep1()`..`renderStep5()` |
| หัวข้อแต่ละขั้น | `STEPH(icon, title, hint)` |
| footer | `.dw-footer` + `.dw-footer-right` |
| ปุ่มส่ง | `#btn-submit` — **ได้ `disabled` จริงเมื่อ `createWizard._over`** |
| ปุ่มร่าง | `#btn-draft` → `saveDraft()` |
| upload | `.upload-zone` → `mockUpload()` |

### 4.3 B2 Line Editor (ขั้น 3)

| ส่วน | selector / function |
|---|---|
| ตาราง | `table.tbl.line-tbl` |
| แถวขยาย | `.line-expand-panel-anchor` → `.line-expand-panel-inner` |
| toggle | `toggleLineExpand(lineId)` |
| ช่องสินค้า | `#item-input-{lineId}` → `showItemSuggestions()` → `#item-pop` |
| อัปเดตค่า | `updateLine(lineId, field, value)` |
| เพิ่ม/ลบแถว | `addLine()` · `rmLine(lineId)` |
| สูตร | `calcLineVat()` · `migrateLine()` · `totals()` · `taxBadgeV()` |
| สรุปยอด | `renderLineSummary()` · `updateLineSummaryOnly()` |
| ป้ายภาษี | `taxBadgeV(mode, pct)` |

### 4.4 View Drawer

| ส่วน | selector / function |
|---|---|
| หัว | `.dv-head` — เลขเอกสาร + pill สถานะ + ปุ่มตามสถานะ |
| แท็บ | `tabBtn(key, label, icon)` → `setViewTab(key)` |
| section | `SEC(icon, title)` + `SECWRAP()` |
| แถว KV | `KVR(label, value, isWide)` |
| ตารางรายการ read-only | `linesTableView()` |
| PDF | `.a4` + ช่องลงนาม |
| ลายเซ็น | `renderSignTab()` → `.tl` timeline + `empChip()` |
| ประวัติ | `.tl` + `.tl-i` (ต่อท้ายอย่างเดียว) |
| สิทธิ์กดปุ่ม | `canActStep(record)` |
| ล็อกอ่านอย่างเดียว | `isLocked(record)` → `['approved','sent','partially_received','closed','cancelled']` |

### 4.5 Modals

| Modal | function | องค์ประกอบเฉพาะ |
|---|---|---|
| ส่งอนุมัติ | `openSubmitModal(id)` | `.slot-row` ต่อขั้น + combobox เลือกคน + `clearSlot()` |
| อนุมัติ | `openApproveModal(id)` | สรุปยอด + ช่องความเห็น |
| ระบุเหตุผล | `reasonModal(title, icon, color, bg, desc, extraFields, submitLabel, submitCls, onOk)` | `#md-rsel` (`reasonSelect()`) + ช่องข้อความ |
| ส่งผู้ขาย | `openSendModal(id)` | เลือกช่องทาง |
| โครงกลาง | `modalShell(inner)` | `.modal-overlay` z 60 |

---

## 5. Overlay Registry + Dismiss Rules

| Overlay | ตัวถือ | z | ปิดด้วย |
|---|---|---|---|
| `.combo-pop` (ผู้ขาย/ผู้จัดซื้อ/ศูนย์ต้นทุน) | `document.body` | 70 | คลิกนอก · Esc · เลือกค่า · `closePops()` |
| `#item-pop` (สินค้า) | `document.body` | 70 | เหมือนกัน |
| `.row-menu` | `document.body` | 30 | คลิกนอก · `closeRowMenu()` |
| `.overlay-wrap` → `.drawer-panel` | `#overlay-root` | 51 | ปุ่ม X · backdrop · Esc |
| `.modal-overlay` | `#overlay-root` | 60 | ปุ่มยกเลิก · Esc · `closeModal()` |
| `.toast` | `.toast-wrap` | 80 | หมดเวลาเอง |

**flip-up:** ทั้ง 3 popover (`comboOpen` · `showItemSuggestions` · `openRowMenu`) พลิกขึ้นบนเมื่อพื้นที่ด้านล่างไม่พอ
— `openRowMenu` วัดจาก `menu.offsetHeight + 12` หลัง `appendChild` (แก้ในรอบ re-gate นี้)

---

## 6. Esc chain

1. popover/เมนูเปิดอยู่ → ปิดก่อน
2. modal เปิดอยู่ → ปิด modal
3. drawer เปิดอยู่ → ปิด drawer + กลับ `#/list`

---

## 7. State-driven UI Matrix

| สถานะ | pill | ปุ่มใน drawer | แก้ไขได้ |
|---|---|---|---|
| `draft` | `ฉบับร่าง` muted | ยกเลิก · แก้ไข · ส่งอนุมัติ | ✅ |
| `pending_approval` | `รออนุมัติ` warning | ไม่อนุมัติ · อนุมัติ (`canActStep`) | ✗ |
| `approved` | `อนุมัติแล้ว` success | ยกเลิก · แก้ไข · ส่งให้ผู้ขาย | ⚠️ ผ่าน Transition Guard |
| `sent` | `ส่งผู้ขายแล้ว` info | ยกเลิก · แก้ไข | ⚠️ ผ่าน Transition Guard |
| `partially_received` | `รับบางส่วน` | **ปิดใบก่อนกำหนด** (ไม่มียกเลิก) | ✗ |
| `closed` | `ปิดแล้ว` | **ไม่มีปุ่มเลย** | ✗ |
| `cancelled` | `ยกเลิก` danger | **ไม่มีปุ่มเลย** | ✗ |

---

## 8. Microcopy verbatim

ดู `01_UI §1.10` — ข้อความทั้งหมดสกัดจากจอจริง **ห้ามแปลใหม่หรือย่อ**

---

## 9. BACKEND anchors ↔ FRD API

| จุดในหน้า (mock) | ต้องต่อกับ |
|---|---|
| `POS` array (seed) | `GET /purchase-orders` (API-01) |
| `findPO(id)` | `GET /purchase-orders/:id` (API-03) |
| `persist()` ใน `submitForApproval()` | `POST /purchase-orders` (API-02) / `PUT` (API-04) |
| `submitForApproval()` → `openSubmitModal()` | `POST /:id/submit` (API-05) |
| `confirmApprove()` | `POST /:id/approve` (API-06) |
| `openRejectModal()` → `reasonModal` | `POST /:id/reject` (API-07) |
| `confirmSend()` | `POST /:id/send` (API-08) |
| `openCancelModal()` | `POST /:id/cancel` (API-09) |
| `openShortCloseModal()` | `POST /:id/short-close` (API-10) |
| `.a4` render | `GET /:id/document` (API-11) |
| `pushAudit()` / แท็บประวัติ | `GET /:id/audit` (API-12) |
| `mockUpload()` | `POST /:id/attachments` (API-13) |
| `similarPOs()` | `GET /duplicate-check` (API-14) |
| `resolveDoa()` / `chainOf()` | `GET /:id/doa-preview` (API-15) + ทะเบียน DOA |
| `nextCode()` | `ENG-DOC-NUM.next('PO')` |
| `budgetOf(cc)` | F117 (W7) — **ยังไม่มีจริง** ปัจจุบันเป็นข้อมูลจำลอง |
| `l.received` / `qty_open` | เขียนโดยใบรับของ (F079) เท่านั้น |

---

## 10. Traceability 3 ทาง

| Brief (ไฟล์นี้) | FRD | HTML |
|---|---|---|
| §1 tokens | `01_UI §1.1` | `:root` |
| §2 geometry | `01_UI §1.1` | `.drawer-panel` · `.wide` |
| §3 routes | `01_UI §1.0` | `getRoute()` |
| §4.3 line editor | `01_UI §1.4` · `03_LOGIC ENG-PO-CALC` | `.line-tbl` |
| §5 overlays | `01_UI §1.8` | `#overlay-root` · `.combo-pop` |
| §7 state matrix | `05_RULES §5.1.1` | `isLocked()` · `docPill()` |
| §9 anchors | `02_API §2.1` | function ที่ระบุ |

---

## 11. Drift Log

| # | จุด | เกิดอะไร | สถานะ |
|---|---|---|---|
| D-01 | `openRowMenu()` | ต้นแบบเดิม**ไม่มี flip-up** → เมนูจมใต้จอ 104.5px | ✅ **แก้แล้วในรอบ re-gate** (ผู้ใช้อนุมัติ) — ไม่กระทบสัญญา UI อื่น |
| D-02 | banner งบ · field-help งบ · note แท็บรับของ | มี marker ภายใน `FWD-WIRE` + รหัส wave `W7`/`W3P` บนจอ (Iron Rule #81) | ✅ **แก้ถ้อยคำแล้ว** — ความหมายเดิมคงอยู่ · สัญญา forward-wire ย้ายไป `07_LOCKED` + `CSQ_BRIEF` + code comment |
| D-03 | `.note.warn` แท็บรับของ | ยาว 121 ตัวอักษร (เพดาน 120) | ⏸ **ยังไม่แก้** — WARN นอกขอบเขตที่ตกลง |
| D-04 | `ss-caret` · `empty-icon` | `<i data-lucide>` ไม่มี class `w-/h-` | ⏸ ยังไม่แก้ — WARN |
| D-05 | `.table-wrap` หน้ารายการ | ขอบล่างล้น fold 130.5px (#96) | ⏸ ยังไม่แก้ — ไม่บล็อก มี `overflow-y:auto` แล้ว |

> Drift ทั้งหมดบันทึกเต็มใน `01_HTML/_UX_CHECK_REPORT.md`
