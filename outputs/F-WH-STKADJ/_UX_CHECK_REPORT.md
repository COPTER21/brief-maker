# UX Check Report — F-WH-STKADJ · ใบปรับยอดสต๊อก (Stock Adjustment)
- วันที่: 2026-09-16 · Iteration: RE-GATE (final) — post 2 user-found UI-bug fixes (BUG-1 scroll-lock · BUG-2 combobox-behind-modal)
- Generator spec: html-generator-v9 (Sync Read: iron-rules #1–#49 · #94–#103 · Pattern Q + B2 v2)
- Passes run: `audit.sh` (SSOT counter) · `static_scan.py` · Pass D (Document Archetype Q/B2 v2) · Pass R (fresh Playwright render + overflow measure @1280/1024 + z-occlusion probe บน submit modal)
- ไฟล์ที่ตรวจ: `outputs/F-WH-STKADJ/F-WH-STKADJ.html` (**1,160 บรรทัด · 171,467 bytes · mtime 2026-09-16 00:45 = final bytes** หลัง BUG-1 + BUG-2 fixes)
- ⚠️ Skill downgrade 2026-09-11: v3 geometry gate หาย → Pass G ระดับ v3 = NOT-CHECKED (ดูหมวด NOT-CHECKED)
- 🔁 Report เก่า (mtime ก่อนหน้า · อ้าง 171,222 bytes @ 22:36) = **STALE** → ไฟล์นี้เขียนทับด้วยผลจาก final bytes (2 UI-bug fixes)

## Verdict: 🟢 PASS (with 5 warnings — ทั้งหมด documented residual / BA-accepted / user-requested)
| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| **0** | 5 | 1 | 2 |

**Mechanical SSOT gate (`audit.sh`): FAIL=0 · WARN=2** → ไม่มี iron-rule violation ที่บล็อก · verdict = PASS
WARN 5 = 2 จาก audit.sh (font-size px · endbill #99) + 3 documented/exception (VAT shim · #106 filter · #16 9-คอลัมน์) — ไม่มีตัวใดเป็น failure

---

## ✅ ยืนยัน 2 UI-bug fixes บน final bytes (render + runtime จริง)

### BUG-1 · scroll-lock ค้างหลัง "กลับรายการ" (trap-stack imbalance) → 🟢 FIXED
| ตรวจ | ผล | หลักฐาน |
|---|---|---|
| `openViewDrawer` release trap เดิมก่อนแทน view drawer | 🟢 **มี** | บรรทัด 988: `if(_ovState.type==='view') releaseFocus();` (คอมเมนต์ DSP-01 บรรทัด 987) — pop trap ของ drawer เดิมก่อน push trap ใหม่ (บรรทัด 992) |
| reverse reason-modal callback ปิด modal ก่อน doReverse | 🟢 **มี** | บรรทัด 1111 `openReverse`: callback = `r=>{ closeModal(); doReverse(d,r); }` — `closeModal()` **ก่อน** `doReverse()` |
| trap-stack สมดุล (in=out) → `body.is-overlay-open` ไม่ค้าง | 🟢 **ยืนยันเชิงกล** | `releaseFocus()` (บรรทัด 330–334) เอา `is-overlay-open` ออกเมื่อ `_trapStack` ว่างเท่านั้น · flow reverse: modal trap ปิด (closeModal) → navigate('view/'+rev.id) → openViewDrawer เห็น `_ovState.type==='view'` → releaseFocus() pop trap view เดิม → trapFocus view ใหม่ = 1-in/1-out ทุกขั้น |

### BUG-2 · combobox ผู้อนุมัติจมใต้ submit-approval modal ("ไม่มีคนใน dropdown") → 🟢 FIXED
| ตรวจ | ผล | หลักฐาน |
|---|---|---|
| เพิ่ม token `--z-combopop:75` | 🟢 **มี** | บรรทัด 34: `--z-combopop:75` (ระหว่าง modal70 กับ toast80) |
| `.combo-pop,.menu-fixed` ใช้ `--z-combopop` | 🟢 **มี** | บรรทัด 188: `.combo-pop,.menu-fixed{position:fixed;…z-index:var(--z-combopop)}` |
| append target ไม่สร้าง stacking context กด z ลง | 🟢 **ปลอดภัย** | `.combo-pop` append เข้า `#ss-overlay-root` (บรรทัด 956) ซึ่ง**ไม่มี CSS** (ไม่มี position/z-index) → child position:fixed z75 ร่วม root stacking context |
| **runtime: dropdown อยู่เหนือ modal จริง (ไม่ถูกบัง)** | 🟢 **ยืนยัน (render)** | เปิด submit modal ของใบร่าง `d4` → focus `cbi-slot-0` → `#ss-combo-pop` computed **z-index=75** vs `#ss-modal` **z-index=70** · `elementFromPoint` กลาง option → element อยู่ **ใน** `.combo-pop` (`occluded=false`, `topInPop=true`) — ตัวเลือกผู้อนุมัติโผล่เหนือ modal ไม่ถูกบัง |

---

## ✅ ยืนยันตามที่ร้องขอ (จาก final bytes · render + runtime @1280/1024)
| ตรวจ | ผล | หลักฐาน |
|---|---|---|
| native `confirm/alert/prompt` | 🟢 **0** | grep word-boundary `(confirm\|alert\|prompt)(` = ไม่พบ native · มีแต่ custom `confirmModal`/`reasonModal`/`confirmSubmit`/`confirmApprove` (modalShell) |
| `mockUpload` | 🟢 **0** | grep count = 0 |
| horizontal overflow @1280 | 🟢 **ไม่มี** | list: sw 1270 vs cw 1280 (−10) · create-drawer: 1270 vs 1280 (−10) |
| horizontal overflow @1024 | 🟢 **ไม่มี** | list: 1014 vs 1024 (−10) · create-drawer: 1014 vs 1024 (−10) |
| z-scale coherent (strict ladder) | 🟢 **ยืนยัน** | `--z-dropdown:40 < --z-drawer:50 < --z-portal:60 < --z-modal:70 < --z-combopop:75 < --z-toast:80` (บรรทัด 34) — เรียงขึ้นไม่มีชนกัน |
| submit-modal dropdown เหนือ modal (ไม่บัง) | 🟢 **ยืนยัน** | ดู BUG-2 ข้างบน (z75 > z70 · elementFromPoint อยู่ใน combo-pop) |
| **WARN #47 (stepper)** | 🟢 **CLEARED** | `.step-dot` มีจริง (`stepper-circle step-dot`) · `audit.sh` ไม่ flag #47 |

---

## 🔴 BLOCK — ไม่มี
`audit.sh` FAIL=0 · Pass D `doc_archetype` ผ่าน (view tabs = detail › pdf › sign › history · ไม่มี attachments tab #101 · docPill+signProgress ✓ · a4+slot_row+vat_segmented_3 ✓ · calcLineVat+totals ✓) · lane BLOCK-list: **#104** ไม่พบ (view-tabs เป็น tab bar ในลิ้นชัก ไม่ใช่ dropdown switch หน้า header) · **#105** ไม่พบ (ไม่มี persona/role switcher เปลือย) · **#106** (2-row filter toolbar) = BA-accepted WARN residual (ดู UX-04) · **#67.1** ไม่พบ hint/banner ที่ไม่มีแหล่ง

## 🟡 WARN — Documented residuals / exceptions (ไม่ใช่ failure)
### UX-01 · Token · body/sidebar · line 37,56,57,60,61
- **พบ:** hardcoded `font-size` px ที่ไม่ใช่ `var(--fs-*)` (13px/10px…) — `audit.sh` WARN
- **สถานะ:** documented residual · ยึด BASE-KIT ตามเดิม ไม่แตะ (gold ref ก็เกิน counter เดียวกัน)

### UX-02 · Rule #99 · endbill segmented · view drawer
- **พบ:** ส่วนลดท้ายบิล segmented ฿/% (`endbill.mode`) — `audit.sh` WARN #99
- **สถานะ:** shim documented · เอกสารปรับยอดไม่ใช้ discount จริง คงโครง B2 v2 ไว้

### UX-03 · VAT shim (tax-inert)
- **พบ:** UI VAT segmented 3 ปุ่ม แต่ปรับยอดสต๊อกไม่คิดภาษี → shim เฉื่อย
- **สถานะ:** documented residual · คงไว้เพื่อ B2 v2 archetype compliance (doc_archetype ผ่าน)

### UX-04 · Rule #106 · 2-row filter toolbar · line ~680
- **พบ:** toolbar filter 2 แถว + `<select class="select">`
- **สถานะ:** SKILL default lane = BLOCK · **แต่ BA-accepted เป็น WARN residual** (ระบุใน re-gate brief) → คง WARN

### UX-05 · Rule #16 exception · list table · line ~690
- **พบ:** ตาราง list 9 คอลัมน์ (เลขที่·คลัง·ประเภท·มูลค่าปรับ·สถานะ·ลายเซ็น·วันที่มีผล·ผู้จัดทำ·[chevron])
- **สถานะ:** user-requested exception · cell atomicity OK (ไม่มี pill ≥2/เซลล์) → WARN documented

## ✅ RESOLVED เทียบ report เก่า
- **UX-06 เดิม (BR-26 markErr no-op cosmetic):** report STALE ระบุ guard เรียก `markErr('f-countdoc',true)` ที่ไม่มี element → no-op. **final bytes บรรทัด 898 เปลี่ยนเป็น `markErr('f-source',true)`** ซึ่ง target element จริง (`<div class="field full" id="f-source">` บรรทัด 790 = field แหล่งที่มา ครอบ combo ใบนับ) → field-highlight ทำงานจริงแล้ว · **finding นี้ไม่มีในรอบนี้** (WARN 6→5)

## ℹ️ INFO — advisory
- **Comment drift (บรรทัด 1155):** คอมเมนต์ z-scale ยังเขียน `dropdown40/drawer50/portal60/modal70/toast80 · .menu-fixed=--z-portal` ซึ่ง**ล้าสมัย** — CSS จริง (บรรทัด 188) ตั้ง `.menu-fixed`/`.combo-pop` เป็น `--z-combopop`(75) แล้ว · เป็น comment-only drift ไม่กระทบพฤติกรรม/verdict · แนะนำ sync คอมเมนต์เมื่อแตะไฟล์รอบหน้า (ไม่แก้ในรอบนี้ตาม brief)
- `self_audit.py` เป็น advisory (non-zero-tolerance · gold reference ก็ FAIL counters เดียวกัน) — gate จริงคือ `audit.sh` FAIL=0

## ⬜ NOT-CHECKED
- **Pass G v3 geometry gate** — skill downgrade 2026-09-11 (สูญ geometry gate v3) · ตรวจได้เฉพาะ counters พื้นฐานผ่าน `audit.sh`
- **Golden Compare (Taste)** — ไม่ได้วางเทียบ golden `_SOURCE_so-reference.html` แบบ pixel side-by-side · overflow/structure checks ผ่านทั้งหมด

## Render / Runtime Gate (Pass R) — fresh @ final bytes (mtime 00:45)
| viewport | route/state | overflow | ผล |
|---|---|---|---|
| 1280 | #/list | −10px | 🟢 ไม่ล้น |
| 1280 | #/create (drawer) | −10px | 🟢 ไม่ล้น |
| 1024 | #/list | −10px | 🟢 ไม่ล้น |
| 1024 | #/create (drawer) | −10px | 🟢 ไม่ล้น |
| 1280 | submit modal (d4) + approver combo เปิด | — | 🟢 combo z75 > modal z70 · elementFromPoint อยู่ใน combo-pop (ไม่บัง) |

หลักฐานภาพ: `_shots/regate_create_1280.png` · `_shots/regate_submitmodal_combo.png`

---
**สรุป:** ทำถูกเชิง form · BLOCK=0 · WARN 5 = documented/BA-accepted/user-requested ทั้งหมด · #47 CLEARED · **BUG-1 (scroll-lock/trap-stack) + BUG-2 (combobox z-order) ยืนยันแก้แล้วบน final bytes** (render + runtime จริง) · UX-06 เดิม RESOLVED — ผ่าน UX gate (PASS with 5 warnings) · verdict คำนวณจาก final bytes (mtime 2026-09-16 00:45 · 171,467 bytes)
