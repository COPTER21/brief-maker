# _COVERAGE_REPORT — F-PUR-PO · ใบสั่งซื้อ (F078)

**ขั้น:** WF-01 ขั้น 7R · coverage **รอบ 1** (HTML vs contract)
**วันที่:** 2026-09-14
**contract ที่ใช้เป็นเกณฑ์:** `PREBRIEF_F-PUR-PO.md` (OB-1..18 · S-01..S-20 · BR-01..BR-20) + `FUNCTION_CHECKLIST_F-PUR-PO.md` (40 FN)
**หมายเหตุ contract:** repo นี้**ไม่มี** `workflow_graph.json` / `NODE_BRIEF` → ใช้ PREBRIEF + FUNCTION_CHECKLIST เป็น contract แทน (ตาม precedent Mode B: F-PUR-COMPARE · F-PUR-PR)
**ไม่ได้นำ `_COVERAGE_R1.md` ของต้นน้ำมาใช้แทนการตรวจ** — ตรวจใหม่ทั้งชุดบนไฟล์ในแพ็ก

---

## VERDICT: **PASS**

| ด้าน | ผล |
|---|---|
| FN 40 ข้อ | **40/40 มี evidence ชี้บรรทัดได้** |
| BR 20 ข้อ | **20/20** — block rule ทดสอบพฤติกรรมจริงด้วย Playwright ครบ |
| scenario S-01..S-20 | 20/20 มีทางเข้าใน UI |
| declaration 5 ชิป | 5/5 มี surface รองรับ |
| scope creep | **0** (สแกน 9 รายการ "สิ่งที่ไม่รองรับ" — ไม่พบสักตัว) |

> coverage ไม่พบ BLOCK · BLOCK 2 ข้อของรอบนี้อยู่ฝั่ง **UX gate** (`_UX_CHECK_REPORT.md` UX-01/UX-02) ไม่ใช่ความครบของ scope

---

## 1. Function Checklist — 40/40

ทุกแถวชี้บรรทัดจริงในไฟล์ `01_HTML/F-PUR-PO.html`

| FN | เรื่อง | Evidence |
|---|---|---|
| FN-01 | เปิด PO จาก PR | [`:2556`](F-PUR-PO.html#L2556) tile `'pr'` → `ดึงรายการจาก PR ที่อนุมัติแล้ว` |
| FN-02 | เปิดตรงไม่ต้องมี PR | [`:2555`](F-PUR-PO.html#L2555) tile `'new'` · `เปิดตรง (ไม่ผ่าน PR)` — ไม่มีจุดบังคับ (BR-03) |
| FN-03 | เห็นเลข PR ต้นทาง + ย้อนกลับได้ | [`:2727`](F-PUR-PO.html#L2727) `KVR('ใบขอซื้ออ้างอิง', …)` |
| FN-04 | เพิ่ม/แก้/ลบรายการเอง | [`:2249`](F-PUR-PO.html#L2249) `addLine()` · `updateLine()` · `rmLine()` |
| FN-05 | เปิดจากผลเทียบราคา | [`:2023`](F-PUR-PO.html#L2023) `COMPARES[]` + `winner` → ตั้งต้นผู้ขาย/ราคา |
| FN-06 | PR ต้นทางถูกยกเลิก → เตือน (ไม่บล็อก) | [`:2768`](F-PUR-PO.html#L2768) `if (d.pr && PR_BY[d.pr].status !== 'approved') showToast('ใบขอซื้อต้นทางถูกยกเลิก — ตรวจสอบก่อนส่งอนุมัติ','warning')` · **ทดสอบได้จริง** — seed มี `PR-2026-0155` status `cancelled` |
| FN-07 | ตั้ง tolerance % ต่อบรรทัด | [`:2234`](F-PUR-PO.html#L2234) input `รับเกินได้ __%` → [`:2266`](F-PUR-PO.html#L2266) clamp 0–100 · default `CFG.defaultTolerancePct` [`:2116`](F-PUR-PO.html#L2116) · แสดงในแท็บรับของ [`:3027`](F-PUR-PO.html#L3027) · **ดู §4 หมายเหตุขอบเขต** |
| FN-08 | picker ผู้ขาย/สินค้า/หน่วย/คลัง/cc | [`:2408`](F-PUR-PO.html#L2408) `comboItems()` — 4 combobox ตรวจ anatomy แล้วใน UX §6 |
| FN-09 | เตือน PO ซ้ำ | [`:2743`](F-PUR-PO.html#L2743) `similarPOs()` เรียกใช้จริง 4 จุด |
| FN-10 | ชั้นอนุมัติตามยอดสุทธิ | [`:2048`](F-PUR-PO.html#L2048) `resolveDoa(amount)` / `chainOf()` |
| FN-11 | เลือกคนจริงต่อ slot | [`:2870`](F-PUR-PO.html#L2870) `empChip()` — รูปย่อ + ชื่อ + ตำแหน่ง · ยืนยันด้วยภาพ `_shots/08_modal_submit.png` |
| FN-12 | ส่งไม่ได้ถ้า slot ว่าง | [`:1451`](F-PUR-PO.html#L1451) `.slot-row` + `clearSlot()` |
| FN-13 | ส่งกลับแก้/ปฏิเสธ ต้องมีเหตุผล | [`:3243`](F-PUR-PO.html#L3243) `openRejectModal()` → `reasonModal()` บังคับกรอก |
| FN-14 | เห็นผลตรวจงบก่อนส่ง (จำลอง) | [`:2035`](F-PUR-PO.html#L2035) `budgetOf()` · [`:2341`](F-PUR-PO.html#L2341) banner เตือน |
| FN-15 | ส่งให้ผู้ขาย → เปลี่ยนสถานะ + บันทึกเวลา | [`:3298`](F-PUR-PO.html#L3298) `confirmSend()` |
| FN-16 | PDF A4 + ปี ค.ศ. | [`:3042`](F-PUR-PO.html#L3042) `class="a4"` · ภาพ `_shots/05_view_pdf.png` |
| FN-17 | แก้ใบที่อนุมัติ/ส่งแล้ว → Transition Guard | [`:2890`](F-PUR-PO.html#L2890) `isLocked()` + modal ยืนยัน + เหตุผล |
| FN-18 | ยืนยันแก้ → กลับไปรออนุมัติใหม่ | [`:3175`](F-PUR-PO.html#L3175) `s.status = 'pending_approval'` |
| FN-19 | บันทึกร่างได้ทุกขั้น | [`:2812`](F-PUR-PO.html#L2812) `saveDraft()` · ปุ่ม `บันทึกแบบร่าง` อยู่ใน footer step 5 |
| FN-20 | รับครบ → ปิดอัตโนมัติ | [`:2890`](F-PUR-PO.html#L2890) สถานะ `closed` |
| FN-21 | รับบางส่วน → สถานะ + ยอดค้าง | [`:2844`](F-PUR-PO.html#L2844) `partially_received` |
| FN-22 | เห็นยอดสั่ง/รับ/ค้าง · แก้มือไม่ได้ | [`:2851`](F-PUR-PO.html#L2851) · **ทดสอบแล้ว: แท็บรับของมี editable input = 0** (ดู §2 BR-13) |
| FN-23 | short-close จากรับบางส่วน + เหตุผล | [`:3272`](F-PUR-PO.html#L3272) `openShortCloseModal()` → `reasonSelect(REASONS.close)` |
| FN-24 | ยกเลิกใบที่ยังไม่รับของ + เหตุผล | [`:3256`](F-PUR-PO.html#L3256) `openCancelModal()` |
| FN-25 | รับของแล้ว → ปุ่มยกเลิกปิด | [`:2750`](F-PUR-PO.html#L2750) · **ทดสอบแล้ว** — `partially_received` ไม่มีปุ่ม `ยกเลิก` (ดู §2 BR-11) |
| FN-26 | จำนวน 0/ติดลบ ไม่ได้ | [`:2755`](F-PUR-PO.html#L2755) `markErr()` |
| FN-27 | ส่วนลดบรรทัด + ท้ายบิล | [`:2078`](F-PUR-PO.html#L2078) `discount_mode` · `endbill.mode` |
| FN-28 | ภาษีต่อบรรทัด 3 โหมด | [`:2119`](F-PUR-PO.html#L2119) `calcLineVat()` — none/add/included |
| FN-29 | ส่งอนุมัติโดยไม่มีรายการไม่ได้ | [`:2151`](F-PUR-PO.html#L2151) ตรวจ `lines.length` |
| FN-30 | แท็บลายเซ็นแสดงทุก slot | [`:2881`](F-PUR-PO.html#L2881) `renderSignTab()` · ภาพ `_shots/06_view_sign.png` |
| FN-31 | เลข `PO-YYYY-NNNN` อัตโนมัติ | [`:3165`](F-PUR-PO.html#L3165) `nextCode()` |
| FN-32 | แนบไฟล์ + เห็นจากหน้ารายการ | [`:1408`](F-PUR-PO.html#L1408) `.upload-zone` · `mockUpload()` |
| FN-33 | ใบปิด/ยกเลิก = อ่านอย่างเดียว | **ทดสอบแล้ว** — สถานะ `closed` ไม่มีปุ่ม action เลย เหลือแต่แท็บ (ดู §2) |
| FN-34 | หลัง short-close รับต่อไม่ได้ | [`:3279`](F-PUR-PO.html#L3279) `s.status = 'closed'` → `isLocked()` ครอบ `closed` |
| FN-90 | ค้นหา/กรอง + empty state | [`:1807`](F-PUR-PO.html#L1807) `emptyStateHTML()` · `filteredPOs()` |
| FN-91 | ยกเลิก/ทิ้งร่าง ผ่านหน้าต่างยืนยัน | [`:3217`](F-PUR-PO.html#L3217) `reasonModal()` |
| FN-92 | validate + กดซ้ำไม่เกิดใบซ้ำ | [`:2808`](F-PUR-PO.html#L2808) `btnLoading('btn-submit', 'กำลังบันทึก…')` |
| FN-93 | ประวัติครบ + ลบไม่ได้ | [`:2840`](F-PUR-PO.html#L2840) `pushAudit()` — **ตรวจแล้วไม่มี `splice`/`pop`/`delete` บน `audit` เลย** (ตรง L-06) |
| FN-94 | ปี ค.ศ. ทุกจุด | [`:2061`](F-PUR-PO.html#L2061) `formatDate()` · **ทดสอบครบทุกจอ — ดู §2 BR-19** |
| FN-95 | CI Warm Light + เมนูตาม module map | [`:22`](F-PUR-PO.html#L22) token `--c-primary` · sidebar ตรง map |

---

## 2. Business Rules — ทดสอบพฤติกรรมจริง (ไม่ใช่แค่ grep)

รันด้วย Playwright บนไฟล์ในแพ็ก · ทุกผลด้านล่างเป็นค่าที่วัดได้

| BR | เกณฑ์ | วิธีทดสอบ | ผลที่วัดได้ |
|---|---|---|---|
| **BR-19** | ปี ค.ศ. ล้วน ห้ามปน พ.ศ. | เปิด **15 ใบ × 5 แท็บ** + หน้า list แล้ว regex `25[0-9]{2}` บน `innerText` | **0 hit ทุกจอ** · ปี ค.ศ. 26 จุดบนหน้า list ✅ |
| **BR-13** | ยอดรับสะสมแก้มือไม่ได้ | เปิดแท็บ "การรับของ" ของใบ `partially_received` นับ input ที่แก้ได้ | **editable input = 0** (input ทั้งหมด = 0 · เป็น `<td>` ล้วน 21 ช่อง) ✅ |
| **BR-11** | ยกเลิกได้เฉพาะ draft/approved/sent | อ่านปุ่มใน drawer ต่อสถานะ | `sent` → `[ยกเลิก, แก้ไข]` ✅ · `partially_received` → `[ปิดใบก่อนกำหนด]` **ไม่มีปุ่มยกเลิก** ✅ |
| **BR-12** | short-close เฉพาะ partially received | อ่านปุ่มต่อสถานะ | โผล่เฉพาะ `partially_received` ✅ · [`:3276`](F-PUR-PO.html#L3276) ข้อความระบุ "ยอดค้างรับ … จะถูกยกเลิก และเปิดรับของต่อไม่ได้" |
| **BR-16** | audit append-only ไม่มี hard delete | grep `audit.splice|audit.pop|delete …audit` | **0 hit** ✅ ตรง L-06 |
| **BR-10** | แก้ approved/sent = Transition Guard | [`:2890`](F-PUR-PO.html#L2890) `isLocked()` ครอบ 5 สถานะ | `['approved','sent','partially_received','closed','cancelled']` ✅ |
| **BR-01/02/04/05** | hard control ก่อนส่งอนุมัติ | อ่าน `wizardNext()` + `markErr()` | validate ต่อ step + ชี้ field ที่ขาด ✅ |
| **BR-06** | ชั้น DOA ตัดจากยอดสุทธิ | `resolveDoa(amount)` | ยอดเปลี่ยน → ชุด slot เปลี่ยน ✅ |
| **BR-07** | ทุก slot ต้องเป็นคนจริง ห้าม role ID | ภาพ `_shots/08_modal_submit.png` + combobox `buyer` | แสดง `ธว → ธนกฤต วัฒนชัย → เจ้าหน้าที่จัดซื้อ · จัดซื้อ · EMP-0142` — **ไม่มี role id บนจอ** ✅ ตรง L-03 |
| **BR-15 + L-09** | ⚖ **งบ = soft · ยอด PR = hard** | อ่าน `submitForApproval()` + การ render ปุ่ม | **ยืนยันครบทั้งสองฝั่ง:** [`:2548`](F-PUR-PO.html#L2548) ปุ่มได้ attribute `disabled` จริงเมื่อ `_over` (เกินยอด PR) · [`:2825`](F-PUR-PO.html#L2825) มี guard ซ้ำใน handler · ส่วน `_overBudget` **ไม่ถูกใช้ปิดปุ่มเลย** → เตือนอย่างเดียว ✅ **ตรง L-09 เป๊ะ** |
| **BR-17** | master = soft-ref ไม่ FK validate | `comboItems()` ไม่มี required/validate | เลือกค่านอก master ได้ · เตือนอย่างเดียว ✅ ตรง L-08 |
| **BR-18** | เตือน PO ซ้ำ ไม่บล็อก | `similarPOs()` → toast | ไม่มี `return` ที่บล็อก ✅ |
| **BR-20** | เลขจาก doccfg เท่านั้น | `nextCode()` [`:3165`](F-PUR-PO.html#L3165) | ไม่มีช่องให้พิมพ์เลขเอง · [`:2727`](F-PUR-PO.html#L2727) field-help บอกรูปแบบมาจากทะเบียนกลาง ✅ ตรง L-05 |
| BR-03 / BR-08 / BR-09 / BR-14 | ดู §4 (ขอบเขตข้ามฟีเจอร์) | | ✅ |

---

## 3. Scenario S-01..S-20 — ทางเข้าใน UI ครบ

| S | เรื่อง | ทางเข้า |
|---|---|---|
| S-01 | เปิดจาก PR | wizard step 1 tile `จากใบขอซื้อ (PR)` |
| S-02 | เปิดตรง | wizard step 1 tile `เปิดตรง (ไม่ผ่าน PR)` |
| S-03 | เปิดจากผลเทียบราคา | step 1 → `COMPARES` |
| S-04..S-08 | กรอกข้อมูล/รายการ/ภาษี/ส่วนลด | step 2 + step 3 (B2 line editor) |
| S-09..S-12 | สายอนุมัติ · เลือกคน · อนุมัติ/ปฏิเสธ | modal ส่งอนุมัติ + แท็บลายเซ็น |
| S-13 | ส่งให้ผู้ขาย | ปุ่ม `ส่งให้ผู้ขาย` ในสถานะ approved |
| S-14 | ยกเลิก (ก่อนรับของ) | ปุ่ม `ยกเลิก` — ปิดหลังรับของแล้ว ✅ |
| S-15 | แก้หลังอนุมัติ → re-approve | ปุ่ม `แก้ไข` + Transition Guard |
| S-16 | รับเกิน tolerance | แท็บการรับของ + คอลัมน์ `รับเกินได้ %` (**บังคับจริงที่ GRN** — ดู §4) |
| S-17 | รับบางส่วน | สถานะ `partially_received` + ยอดค้างต่อบรรทัด |
| S-18 | ปิดใบก่อนกำหนด | ปุ่ม `ปิดใบก่อนกำหนด` |
| S-19 | Blanket PO | **นอก scope โดยมติ** — ตรวจแล้วไม่มีในไฟล์ ✅ |
| S-20 | Landed cost / FX / drop-ship | **นอก scope โดยมติ** — ตรวจแล้วไม่มีในไฟล์ ✅ |

---

## 4. ขอบเขตข้ามฟีเจอร์ — สิ่งที่ "ไม่ได้ทำในจอนี้" โดยเจตนา (ไม่ใช่ช่องว่าง)

> ส่วนนี้เขียนไว้กันอ่านผิดเป็น gap — ทั้งหมดมีมติรองรับใน PREBRIEF/HANDOFF

| เรื่อง | สถานะในจอนี้ | ใครบังคับจริง | อ้างอิง |
|---|---|---|---|
| **tolerance รับเกิน (FN-07 · BR-08 · S-16)** | **เก็บค่าได้ครบ** — ตั้งต่อบรรทัด · clamp 0–100 · default จาก config · แสดงในแท็บรับของ · seed มีใบที่ตั้ง 5% (`PO-2026-0007`) · **แต่ไม่มีตรรกะเทียบยอดรับกับเพดานในไฟล์นี้** | **F079 GRN** | HANDOFF §7 ระบุตรง ๆ ว่า *"เพดานรับเกิน — GRN เป็นคนบังคับจริง PO เป็นคนเก็บค่า"* · BR-08 *"เกิน = บล็อกที่ GRN"* → **ถูกต้องตาม contract** |
| **ตรวจงบจริง (FN-14 · BR-15)** | ข้อมูลจำลอง แสดงผล ไม่บล็อก | **F117 Budget Control (W7)** | BR-15 · OQ-PO-03 · `CSQ_BRIEF` |
| **ยอดรับสะสมจริง (BR-13)** | seed จำลอง · อ่านอย่างเดียว | **F079 GRN** | BR-13 · HANDOFF §4.2 |
| **ลงบัญชี (JE)** | ไม่มีเลย — PO เป็น commitment ไม่ใช่รายการบัญชี | GRN/Invoice (W5) | `CSQ_BRIEF §3` · LOCK-07 |
| **GRN เปิดจากสถานะไหน (BR-14)** | PO แสดงสถานะถูกต้อง แต่ตัวกรองอยู่ฝั่ง GRN | **F079 GRN** | BR-14/R16 |

> ⚠️ ข้อแรกต่างจากกับดัก "ฟิลด์ config ที่ตั้งได้แต่ไม่มีใครใช้" ของรอบ F-SEC-LOCKOUT
> — รอบนั้น brief อ้างว่าทำงานแล้วแต่ไม่มีโค้ดใช้ · **รอบนี้ brief ระบุชัดว่า PO มีหน้าที่เก็บค่าอย่างเดียว** จึงเป็นไปตามสัญญา ไม่ใช่ของตกหล่น

---

## 5. Declaration coverage — 5/5 ชิป

registry `F078.dec = [doa, ntf, csq, doccfg, pdfdoc]`

| ชิป | surface ในจอ | evidence |
|---|---|---|
| ⚖ `doa` | slot picker เลือกคนจริง + สายตามวงเงิน | [`:1451`](F-PUR-PO.html#L1451) `.slot-row` · `resolveDoa()` · ภาพ `08_modal_submit.png` |
| 🔔 `ntf` | จุด trigger ผูก state transition (ส่งอนุมัติ/อนุมัติ/ส่งผู้ขาย/ปิดใบ) | `confirmSubmit` · `confirmApprove` · `confirmSend` · `openShortCloseModal` |
| ◆ `csq` | ท่อ consequence ตอนอนุมัติ/commitment | `NTF/CSQ_BRIEF` — ไม่มี surface บนจอโดยตั้งใจ (เป็น backend contract) |
| `doccfg` | เลข `PO-YYYY-NNNN` จากทะเบียนกลาง | [`:3165`](F-PUR-PO.html#L3165) `nextCode()` |
| 📄 `pdfdoc` | PDF Preview A4 + 3 ช่องลงนาม | [`:3042`](F-PUR-PO.html#L3042) `class="a4"` · ภาพ `05_view_pdf.png` |

**DIVERGENCE: ไม่มี** — ไม่พบ surface ที่ registry ไม่ได้ประกาศ (รายละเอียดใน `_UX_CHECK_REPORT.md §7`)

---

## 6. Scope guard — creep = 0

สแกนไฟล์ (ตัด comment ออกแล้ว) เทียบกับ 9 รายการใน "สิ่งที่ไม่รองรับ"

| ของที่ห้ามมี | พบ |
|---|---|
| Blanket PO / สัญญาระยะยาว / เรียกของเป็นงวด | 0 |
| Landed cost | 0 |
| FX logic (แปลงค่าเงิน/ตีมูลค่าใหม่) | 0 |
| Drop-ship | 0 |
| Subcontracting | 0 |
| สร้าง PO อัตโนมัติจากจุดสั่งซื้อซ้ำ | 0 |
| ลงบัญชี / GL | 0 |
| PO versioning v1/v2 แยกใบ | 0 |
| ยกเลิกหลังรับของบางส่วน | 0 (ปุ่มถูกปิดจริง — ทดสอบแล้ว §2 BR-11) |

---

## 7. NOT-CHECKED

| หมวด | เหตุผล |
|---|---|
| `workflow_graph.json` edges in/out | ไม่มีไฟล์ graph ใน repo — ใช้ PREBRIEF §9 (inbound/outbound) แทน · **เสนอ:** ถ้ามี mapper ควรออก graph ของ W3P เพื่อให้รอบ 2 ตรวจ edge ได้เชิงกล |
| OB-1..OB-18 รายข้อ | ครอบทางอ้อมผ่าน FN/BR — ยังไม่ได้ทำ matrix แยกราย OB (จะทำในรอบ 2 พร้อม FRD) |
| รอบ 2 (FRD + TC) | ยังไม่ถึงขั้น — จะต่อท้ายไฟล์นี้ |

---
---

# รอบ 2 — FRD Pack + Test Cases vs contract

**วันที่:** 2026-09-14 · **ขั้น:** WF-01 S6.5
**input เพิ่มจากรอบ 1:** `03_FRD/` (FULL 9+INDEX) · `04_QA/testcases-F-PUR-PO-001.md` (72 เคส) · `04_QA/testcase-F-PUR-PO-001.html` (57 เคส)

## VERDICT รอบ 2: **PASS**

ตรวจเชิงกลด้วย set-difference ทุกหมวด — ไม่เดาจากความจำ

| ตรวจ | ผล |
|---|---|
| FN ธุรกิจ 40 ข้อ → มี evidence ใน HTML | **40/40** |
| FN ธุรกิจ 40 ข้อ → ledger ของ testcase อ้างครบ | **40/40** |
| R01–R24 → มีเคสอ้างถึง | **24/24** |
| VR01–VR18 → มีเคสอ้างถึง | **18/18** |
| E01–E11 → มีเคสอ้างถึง | **11/11** |
| Error code 15 ตัว (`02_API §2.10`) → มีเคส | **15/15** |
| LOCK-01..07 → มีเคส verify | **7/7** |
| L-01..L-09 (HANDOFF §3) → มีเคส verify | **9/9** |
| XT-01..15 cross-module → มีเคส | **15/15** |
| S-01..S-20 (PREBRIEF) → ปรากฏใน FRD | **20/20** |
| S-01..S-20 → ปรากฏใน testcase | **20/20** |
| R8 Logic traceability (API ↔ Function) | **26/26 ไม่มี orphan** |
| Data Classification ทุกคอลัมน์ (R10) | ครบ · §4.6 มี 6 หัวข้อย่อย |
| Coverage Manifest (`00_OVERVIEW §0.12`) | ทุกแถวมีที่ลง |

## Gap ที่เจอในรอบนี้ และวิธีปิด

> ตรวจรอบแรกแล้ว **fail ก่อน** แล้วจึงแก้ — ปิดด้วยการ **เพิ่มเคส/เพิ่ม trace** ไม่ใช่ลดจำนวนกติกา

| # | เจออะไร | ปิดอย่างไร |
|---|---|---|
| 1 | `R03` (ช่องบังคับ) ไม่มีเคสตรง | เพิ่ม **AT-33/34/35** (วันที่ก่อนวันเอกสาร · ไม่เลือกเงื่อนไขชำระ · ที่อยู่จัดส่งว่าง) → ฉบับคน **TC-47/48/49** |
| 2 | `VR02` `VR03` ไม่มีเคส | เพิ่ม **AT-33 · AT-34** |
| 3 | `VR06` `VR07` ไม่มีเคส | เพิ่ม **AT-31 · AT-32** → ฉบับคน **TC-50 · TC-51** |
| 4 | `EC-12..14` (`[AI-DEFAULT]`) ไม่มีเคส | เพิ่ม **AT-36/37/38** → ฉบับคน **TC-45** (ที่เหลือเข้า drop ledger เพราะกดจริงไม่ได้) |
| 5 | `E07` `E09` ไม่มีเคสตรง | เพิ่ม **AT-39 · AT-40** |
| 6 | error code 14/15 ตัวไม่ถูกอ้างในเคส | เพิ่ม **§6.13 Error Code → Test map** ครบทั้ง 15 |
| 7 | `S-02/05/14/16/17/18/19/20` ไม่มีใน ledger ของ testcase | เพิ่ม **§G.1 ตาราง S-xx → เคส** ครบทั้ง 20 |
| 8 | `L-04` (CI token + BASE-KIT) ไม่มีเคสอ้าง | ผูกกับ **TC-46** + ชี้ว่าส่วนที่เป็นโค้ด kit ตรวจเชิงกลที่ `_UX_CHECK_REPORT §5` |

## รายการที่ยังไม่มีเคส — **มีเหตุผลรองรับ ไม่ใช่ของตกหล่น**

| รายการ | เหตุผล | เจ้าภาพ |
|---|---|---|
| **R24** เวลาที่ยอมรับได้ต่อขั้นอนุมัติ | ยังไม่มีเกณฑ์ให้ทดสอบ | Q3 — หัวหน้าจัดซื้อ + Strike |
| **E11** บรรทัดประเภทบริการรับของอย่างไร | รอเคาะพร้อมใบรับของ | Q7 — Strike + เจ้าของ F079 |
| **E12–E18** | ยังไม่ confirm (BRD §10.2) — **ไม่ได้เขียนเป็น spec** จึงไม่มีเคส | Strike |
| `DOC_NUMBER_UNAVAILABLE` | ต้องจำลองทะเบียนเอกสารกลางล่ม — ต้นแบบทำไม่ได้ | ตรวจตอนต่อ backend |

## ข้อสังเกตเชิงคุณภาพ

1. **`[AI-DEFAULT]` 3 ข้อถูกกระจายครบ** — `05_RULES §5.3.2` → `02_API §2.9` → เคส AT-36/37/38 → ติดป้ายในฉบับคน (TC-45) ให้ผู้ทดสอบรู้ว่าเกณฑ์นี้ AI ตัดสินแทน BA
2. **คู่ตรงข้าม L-09 ถูกทำเป็นเคสคู่โดยเจตนา** — AT-16/TC-17b (บล็อกจริง) กับ AT-23/TC-18 (เตือนเฉย ๆ) มีหมายเหตุกำกับทั้งสองฝั่งว่าถ้าผลเหมือนกัน = ผิด
3. **ไม่มีการเจือจางกติกา** — ทุก gap ปิดด้วยการเพิ่มเคส จำนวน rule/VR/EC เท่าเดิมทุกตัว
4. **`FN-xx` สองชุดถูกกันสับสนไว้แล้ว** — `00_OVERVIEW §0.12.4` + `07_LOCKED LD-09`

## เอกสารทดสอบ 2 ฉบับ

| ฉบับ | ไฟล์ | เคส | ใครใช้ |
|---|---|---|---|
| สำหรับ AI | `04_QA/testcases-F-PUR-PO-001.md` | **72** | agent ที่รันเทสอัตโนมัติ |
| สำหรับคน | `04_QA/testcase-F-PUR-PO-001.html` | **57** | ผู้ทดสอบที่กดจริงบนจอ |

ส่วนต่าง 15 เคสแจกแจงรายข้อใน `04_QA/_build/DROP_LEDGER.md` — **รหัสเคสคงเดิมทั้งสองฉบับ** ไล่เทียบกันได้ตรง ๆ

**หลักฐานการ build:** `CAPTURE VERIFY OK 27 · SKIP/FAIL 0` (`04_QA/_build/shots.report.json`) · ทุกภาพตรงสถานะที่เคสอ้างถึง
