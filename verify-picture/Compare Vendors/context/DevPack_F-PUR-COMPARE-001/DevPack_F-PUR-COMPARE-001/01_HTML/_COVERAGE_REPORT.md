# _COVERAGE_REPORT — F-PUR-COMPARE · เทียบราคาผู้ขาย

**ขั้น:** WF-01 §7R re-gate · `qc-coverage-checker` **รอบ 1** (HTML เทียบ PREBRIEF + FN-01..20 + SC-01..15)
**target:** `01_HTML/CompareVendors.html`
**contract:** `02_BRD/PREBRIEF_F-PUR-COMPARE.md` · `02_BRD/FUNCTION_CHECKLIST_F-PUR-COMPARE.md` · `02_BRD/BRD_F-PUR-COMPARE.md` (APPROVED) · registry `Cube_Feature_List.html` F073 (`arch: master` · `dec: ["csq"]` · `wave: W2`)
**วันที่:** 2026-09-13

## Verdict รอบ 1: **PASS** · 0 BLOCK · 2 WARN · 0 DIVERGENCE

---

## 1. FN coverage — FN-01..20

| FN | ฟังก์ชัน | หลักฐานในไฟล์ | ภาพ | ผล |
| --- | --- | --- | --- | --- |
| FN-01 | คิวงาน: PR อนุมัติแล้ว + รอบค้าง | `queueRows()` L616 · `renderQueue()` L631 | `01_console_default` | ✅ |
| FN-02 | ค้นหา + กรองสถานะ/หน่วยงาน | `QUEUE={q,status,dept}` L615 · `resetQueue()` | `02_queue_search` · `03_queue_filter_status` · `04_queue_reset` | ✅ |
| FN-03 | ว่าง / กำลังโหลด / ผิดพลาด + ลองใหม่ | `simulateQueueError()` L680 · `retryQueue()` L678 | `05_queue_error` · `06_queue_retry` · `07_queue_empty` | ✅ |
| FN-04 | เปิดรอบเทียบราคาจาก PR | `openRoundConfirm()` L985 | `09_select_row` | ✅ |
| FN-05 | เพิ่มผู้ขาย + หัวใบเสนอราคา | `openQuoteForm()` L1065 · `renderQuoteModal()` L1083 — 11 ฟิลด์ (`vendor_id · vendor_quote_no · quote_date · valid_until · payment_term · lead_time_days · warranty · note · attachments · lines`) | `13_quote_form_new` · `14_quote_form_filled` | ✅ |
| FN-06 | ราคารายรายการ + ส่วนลด% + VAT + ยอดรวม | `lineTotal()` L588 (VAT 3 โหมด) · `quoteTotals()` L598 | `10_tab_quotes` | ✅ |
| FN-07 | ทำเครื่องหมาย "ไม่เสนอ" | `qfl(no,'available',false)` L1077 — ทดสอบจริง: ตั้งค่าแล้ว `lines[0].available === false` | `15_quote_form_notoffer` | ✅ |
| FN-08 | แนบไฟล์ใบเสนอราคา | `addQuoteFile()` L1145 | `16_quote_form_attach` | ⚠️ mock (WARN-A) |
| FN-09 | แก้/ลบเฉพาะก่อนยืนยันผล | `confirmDeleteQuote()` L1007 · ปุ่มซ่อนเมื่อ `locked` L940 — modal จริง: *"ใบเสนอราคาของ บจก. ออฟฟิศเมท ซัพพลาย จะถูกลบออกจากรอบนี้ การกระทำนี้ย้อนกลับไม่ได้"* | `18_confirm_delete_quote` · `27_awarded_quotes_tab` | ✅ |
| FN-10 | เตือนใบเสนอราคาหมดอายุ | `isExpired()` L611 — นับคำว่า "หมดอายุ" บนจอได้ **2 จุด** (pill บนการ์ด + แถว "อายุใบเสนอราคา") | `20_matrix_full` (แดง "หมดอายุ 9 ก.ย. 2026") | ✅ |
| FN-11 | ตารางเทียบ แถว=รายการ คอลัมน์=ผู้ขาย | `renderMatrixTab()` L741 · `.mx` + `.mx-wrap` | `20_matrix_full` | ✅ |
| FN-12 | ไฮไลต์ค่าดีที่สุด (รวมกรณีเท่ากัน) | `bestUnit()` L607 · `bestTotal()` L609 · epsilon `0.005` → นับ `.mx .best` ได้ **4 เซลล์** | `20_matrix_full` | ✅ |
| FN-13 | แถวสรุป 5 แกน + ส่วนต่าง % | tfoot: ยอดสุทธิรวม · ส่วนต่างจากราคาต่ำสุด (`+149.80 (1.2%)`) · เงื่อนไขชำระ · ระยะเวลาส่งมอบ (ไฮไลต์ 3 วัน) · การรับประกัน · อายุใบเสนอราคา | `20_matrix_full` | ✅ |
| FN-14 | ราคาซื้อครั้งก่อน (อ้างอิง) | คอลัมน์ขวาสุด — บนจอ 115.00 / 385.00 | `20_matrix_full` | ✅ |
| FN-15 | สลับโหมด ทั้งใบ / แยกรายรายการ | `AWARD.mode` + `.mode-seg` | `21_award_whole` · `22_award_split` | ✅ |
| FN-16 | เลือกผู้ชนะ + สรุปยอดต่อผู้ขาย | `awardCalc()` L808 · `initAward()` L796 ตั้งค่าเริ่มต้นเป็นผู้ขายราคาต่ำสุด**ที่เสนอครบ** | `12_tab_award` · `40_award_lowest_enabled` | ✅ |
| FN-17 | **บังคับเหตุผลเมื่อไม่ใช่ต่ำสุด / รายเดียว** | ทดสอบ 4 สถานะจริง — ดู §2 ตาราง FN-17 | `40` · `41` · `42` | ✅ |
| FN-18 | ยืนยันผล → ล็อกรอบ + ปุ่มส่งต่อ PO | `doAward()` L1023 → `status='awarded'` · ปุ่มแก้/ลบหาย | `25_confirm_award_modal` · `26_awarded_locked` | ✅ |
| FN-19 | เปิดรอบใหม่จากรอบที่ปิดแล้ว | `confirmReopen()` L995 → `round_seq+1` · toast "เปิดรอบที่ 2 แล้ว" | `28_reopen_confirm` · `29_after_reopen` | ✅ |
| FN-20 | ยกเลิกรอบ (เหตุผลบังคับ) · ประวัติเพิ่มอย่างเดียว | `openReason('cancel')` L1043 · `doCancelRound()` L1057 · `pushHist()` L612 · `renderHistory()` L918 — หัวข้อบนจอ: *"ประวัติ (บันทึกเพิ่มอย่างเดียว · แก้ไข/ลบไม่ได้)"* | `30_cancel_reason_modal` · `31_cancel_reason_typed` · `33_history` | ✅ |

**FN ผ่าน 20/20** (FN-08 ผ่านเชิงหน้าจอ · ติด WARN เรื่อง backend)

---

## 2. ★ FN-17 / BR-04 — จุดควบคุมหลักด้านการกำกับดูแล (ทดสอบเชิงกล 4 สถานะ)

ยอดสุทธิที่วัดได้จริงในรอบ `PR-2026-0006`:
`บจก. ออฟฟิศเมท ซัพพลาย ฿13,011.20 (ครบ)` · `บจก. ไทยเปเปอร์ เทรดดิ้ง ฿13,161.00 (ครบ)` · `บจก. เอ็นเทค ซัพพลายเออร์ ฿4,922.00 (ไม่ครบ)`

| สถานะที่ทดสอบ | ผู้ขายที่เลือก | เหตุผล | ปุ่ม "ยืนยันผลการเลือก" | ถูกต้อง? |
| --- | --- | --- | --- | --- |
| A · ต่ำสุดที่เสนอครบ | ออฟฟิศเมท ฿13,011.20 | ว่าง | **เปิด** · ไม่มีแถบเตือน | ✅ |
| B · ไม่ใช่ต่ำสุด | ไทยเปเปอร์ ฿13,161.00 | ว่าง | **ปิด** · แถบเตือน: *"ต้องระบุเหตุผล \| ผลที่เลือกไม่ใช่ราคาต่ำสุด — ส่วนต่าง ฿149.80 จึงต้องอธิบายเหตุผลให้ตรวจสอบย้อนหลังได้"* | ✅ |
| C · ไม่ใช่ต่ำสุด + เหตุผลสั้น | ไทยเปเปอร์ | `"ส"` (1 ตัวอักษร) | **ปิด** (เกณฑ์ ≥3) | ✅ |
| D · ไม่ใช่ต่ำสุด + เหตุผลครบ | ไทยเปเปอร์ | `"ส่งมอบเร็วกว่า 6 วัน คุ้มกับส่วนต่างราคา"` | **เปิด** | ✅ |

เงื่อนไขในโค้ด: `disabled` เว้นแต่ `c.ok && (!c.needReason || String(a.reason||'').trim().length>=3)`
**ยืนยันว่าราคาต่ำสุดที่ใช้เทียบคือราคาต่ำสุดของใบที่เสนอครบทุกรายการ** — ใบที่ไม่ครบ (฿4,922) ไม่ถูกนับเป็นฐาน และเลือกแบบ "ทั้งใบ" ไม่ได้ (SC-04 ✅)

---

## 3. Scenario / exception path — SC-01..15

| SC | เรื่อง | ผล | หลักฐาน |
| --- | --- | --- | --- |
| SC-01 | เทียบครบวงจร | ✅ | walk 42/42 |
| SC-02 | แยกรายรายการ | ✅ | `22_award_split` |
| SC-03 | เลือกไม่ใช่ต่ำสุด | ✅ | §2 แถว B/D |
| SC-04 | ผู้ขายไม่เสนอบางรายการ | ✅ | `complete:false` ของ ฿4,922 → เลือกทั้งใบไม่ได้ · บนจอขึ้น "ไม่เสนอ" |
| SC-05 | มีผู้เสนอรายเดียว | ✅ | `awardCalc().single` → `needReason` |
| SC-06 | ยังไม่มีใบเสนอราคา | ✅ | state "ยังตัดสินไม่ได้" |
| SC-07 | ใบเสนอราคาหมดอายุ | ✅ | `isExpired()` · `20_matrix_full` |
| SC-08 | ยืนยันแล้วห้ามแก้ | ✅ | `26_awarded_locked` |
| SC-09 | เปิดรอบใหม่ | ✅ | `29_after_reopen` |
| SC-10 | ยกเลิกรอบ | ✅ | `30` · `31` |
| **SC-11** | **ผู้ไม่มีสิทธิ์เปิดดู** | ❌ **ยังไม่ได้ทำ** | ดู WARN-B |
| SC-12 | คิวว่าง / โหลดพัง | ✅ | `05` · `06` · `07` |
| SC-13 | ยอดเท่ากันสองราย | ✅ | epsilon `0.005` ใน `bestUnit`/`bestTotal` (ไม่มี seed ที่เท่ากันพอดี — ตรวจจากตรรกะ) |
| SC-14 | รายการนอกทะเบียน | ✅ | ยึดชื่อรายการจาก PR |
| **SC-15** | **PR ถูกยกเลิกหลังเปิดรอบ** | ❌ **ยังไม่ได้ทำ** | ดู WARN-B |

**SC ผ่าน 13/15**

---

## 4. Declaration coverage เทียบ registry

| chip ใน F073 | ใบประกาศ | hook ในไฟล์ | ผล |
| --- | --- | --- | --- |
| ◆ `csq` | `03_FRD/CSQ_BRIEF_F-PUR-COMPARE-001.md` (จาก `5_DECLARATIONS/`) | คอมเมนต์ `ENG-CSQ master.changed → DC` ที่ `doAward()` · `doc.cancelled → EC(avoided)` ที่ `doCancelRound()` | ✅ |
| ⚖ `doa` · 🔔 `ntf` · `doccfg` · 📄 `pdfdoc` | **ไม่มี — ถูกต้อง** | grep `role\|perm\|approve` = 0 · ไม่มีเลขรัน · ไม่มีแบบพิมพ์ · ไม่มี event แจ้งเตือน | ✅ |

**chip = detect → 0 DIVERGENCE**

---

## 5. Scope creep check

ไม่พบ — ไม่มีจอใบสั่งซื้อ · ไม่มีพอร์ทัลผู้ขาย · ไม่มีคะแนนประเมินผู้ขาย · ไม่มีการต่อรอง
ปุ่ม "ออกใบสั่งซื้อให้ <ผู้ขาย>" เป็น hook ที่แสดง toast เท่านั้น ✅ (แต่ถ้อยคำติด WARN-3 ใน `_UX_CHECK_REPORT.md`)
soft-reference (PR · Vendor · Item · UoM) = ตัวเลือก ไม่ผูกคีย์ ✅

---

## 6. WARN รอบ 1

### WARN-A · FN-08 ไฟล์แนบเป็น mock
`addQuoteFile()` เพิ่มรายการไฟล์ในหน่วยความจำ ไม่มี upload/storage → Phase B ต้องกำหนด contract (ไปอยู่ที่ `03_FRD/02_API.md`)

### WARN-B ★ SC-11 และ SC-15 ยังไม่มีการทำงาน — แก้เกรดจากรายงานต้นน้ำ
`input/09132026-compare-vendors/0_DIRECTION/_COVERAGE_R1.md` ให้ ⚠ และอธิบายว่า *"เป็นข้อกำหนดใน PREBRIEF + **hook ในโค้ด** (`prCancelled` flag)"*
ตรวจซ้ำเชิงกลแล้วคำว่า "hook ในโค้ด" **ไม่ตรงกับไฟล์**:

| เคส | คำสั่งที่ใช้ตรวจ | ผล |
| --- | --- | --- |
| SC-15 | `grep -n prCancelled` | พบครั้งเดียว L939 `const prCancelled=false; /* hook: … mock flag */` → **ไม่มีบรรทัดไหนอ่านค่านี้** · ไม่มีแถบเตือนหัวคอนโซล · ไม่มีการปิดปุ่มยืนยัน |
| SC-11 | `grep -nE 'role\|perm\|canEdit\|readonly\|viewer'` + `['role','perm','canEdit','readonly','viewer'].filter(k=>k in window)` | **0 ทุกคำ / `[]`** — ไม่มีแม้แต่ตัวแปรสิทธิ์ |

→ เกรดใหม่ = ❌ **ยังไม่ได้ทำ** (ไม่ใช่ ⚠ "ทำแล้วแต่ไม่มีข้อมูลตัวอย่าง")
**ไม่ยก BLOCK** เพราะทั้งสองเคสพึ่งสัญญาข้ามฟีเจอร์ที่ Phase B เป็นคนผูก (สิทธิ์จาก Policy Center · สถานะ PR จาก F-PUR-PR) — แต่ **ต้องปรากฏเป็นกฎที่มีเจ้าของใน `03_FRD/05_RULES.md` และมีเคสทดสอบใน `06_TESTS.md`** ไม่ใช่หายไปเงียบ ๆ

---
---

# รอบ 2 — FRD Pack + Test cases

**ขั้น:** `qc-coverage-checker` รอบ 2 — FRD Pack + Test cases เทียบ PREBRIEF/BRD
**วันที่:** 2026-09-13

## Verdict รอบ 2: **PASS** · 0 BLOCK · 3 WARN

## R2.1 ตรวจเชิงกล — ทุกกติกาถูก trace เข้า `06_TESTS.md` จริง

ไม่ได้เช็คจากความจำ · รัน set-difference จริงระหว่างไฟล์:

```python
set(re.findall(r'\bBR-\d\d',      05_RULES))  - set(... 06_TESTS)   → NONE
set(re.findall(r'(?<![A-Z])V-\d\d', 05_RULES))  - set(... 06_TESTS)   → NONE
set(re.findall(r'(?<![A-Z])C-\d\d', 05_RULES))  - set(... 06_TESTS)   → NONE
set(re.findall(r'\bEC-\d\d',      05_RULES))  - set(... 06_TESTS)   → NONE
set(re.findall(r'E-CMP-[0-9]{3}-[A-Z-]+', 02_API)) - set(... 06_TESTS) → NONE
set(re.findall(r'LD-\d\d',  07_LOCKED))        - set(... 06_TESTS)   → NONE
set(re.findall(r'FN-\d\d',  FUNCTION_CHECKLIST)) - set(... 06_TESTS) → NONE
set(re.findall(r'SC-\d\d',  PREBRIEF))          - set(... 06_TESTS)  → NONE
```

| มิติ | จำนวนที่ประกาศ | ถูกอ้างใน `06_TESTS` | ขาด |
| --- | --- | --- | --- |
| BR (กติกาธุรกิจ) | 10 | 10 | — |
| V (ตรวจค่า) | 7 | 7 | — |
| C (จุดควบคุม) | 9 | 9 | — |
| EC (เคสขอบ) | 9 | 9 | — |
| error code (`02_API §7`) | 11 | 11 | — |
| LD (ข้อล็อก) | 12 | 12 | — |
| FN (ฟังก์ชัน) | 20 | 20 | — |
| SC (สถานการณ์) | 15 | 15 | — |

> **รอบแรกของการตรวจนี้ไม่ผ่าน** — ขาด `E-CMP-404-ROUND` · `LD-08` · `LD-10` · `LD-12` · `FN-16` และ SC-01/03/04/06/14
> แก้โดย **เพิ่ม TC-57..60 และเติม trace ในเคสเดิม** แล้วรันซ้ำจนว่างทุกหมวด (ไม่ได้แก้ด้วยการลดจำนวนกติกา)

## R2.2 FRD Pack ครบตามชั้น

| ไฟล์ | มี | ครอบคลุม |
| --- | :--: | --- |
| `00_OVERVIEW.md` | ✅ | ขอบเขต · archetype · **§0.10 สิ่งที่ตั้งใจไม่ทำ** · §0.12 Coverage Manifest |
| `01_UI.md` | ✅ | 8 Layout Decision · 5 ส่วนของจอ · overlay registry · state matrix · responsive |
| `02_API.md` | ✅ | 12 endpoint · 11 error code · §8 API ที่ไม่มีและเหตุผล |
| `03_LOGIC.md` | ✅ | สูตรคำนวณอ้างบรรทัดจริง · state machine · trigger 7C · §7 ตรรกะที่ยังไม่ได้ทำ |
| `04_DB.md` | ✅ | 5 ตาราง · index · append-only enforcement · §7 สิ่งที่ไม่มีในชั้นข้อมูล |
| `05_RULES.md` | ✅ | BR-01..10 · V-01..07 · C-01..09 · EC-01..09 |
| `06_TESTS.md` | ✅ | 60 เคส + traceability |
| `07_LOCKED_DECISIONS.md` | ✅ | LD-01..12 + TD-01..06 + OQ 10 ข้อ |
| `HTML_UI_BRIEF_*.md` | ✅ | tokens · z-index map · anatomy · microcopy verbatim · dead CSS · drift log |
| `CSQ_BRIEF_*.md` | ✅ | ยกจาก Phase A ไม่แก้ |

## R2.3 HANDOFF §3 "ห้ามแตะ" ถูกยกเข้า FRD ครบ

| HANDOFF §3 | → LD | อยู่ใน `07_LOCKED_DECISIONS.md` |
| --- | --- | :--: |
| #1 ห้ามเป็นเอกสารธุรกรรม | LD-01 | ✅ |
| #2 ห้ามใส่ DOA | LD-02 | ✅ |
| #3 โครงตารางเทียบ | LD-04 | ✅ |
| #4 เหตุผลบังคับ | LD-05 | ✅ |
| #5 ยืนยันแล้วล็อก | LD-06 | ✅ |
| #6 ประวัติเพิ่มอย่างเดียว | LD-07 | ✅ |
| #7 อ้างอิงอ่อน 4 ตัว | LD-08 | ✅ |
| #8 ห้ามสร้างจอใบสั่งซื้อ | LD-09 | ✅ |
| #9 ปี ค.ศ. · CI · เมนูข้าง | LD-10 | ✅ |

HANDOFF §5 (OQ/ASSUMED 8 ข้อ) + OQ-CSQ 2 ข้อ → `07_LOCKED_DECISIONS.md` ท้ายไฟล์ ✅ **10/10**

## R2.4 Declaration coverage รอบ 2

| ชิปใน registry | ใบประกาศใน pack | เหตุผลถ้าไม่มี เขียนไว้ที่ไหน |
| --- | --- | --- |
| ◆ `csq` | ✅ `03_FRD/CSQ_BRIEF_F-PUR-COMPARE-001.md` | — |
| ⚖ `doa` | ❌ ตั้งใจไม่ทำ | `00_OVERVIEW §0.10` + `LD-02` + `05_RULES §5` |
| 🔔 `ntf` | ❌ ตั้งใจไม่ทำ | `00_OVERVIEW §0.10` + `INDEX` |
| `doccfg` | ❌ ตั้งใจไม่ทำ | `00_OVERVIEW §0.10` + `LD-03` + `04_DB §7` |
| 📄 `pdfdoc` | ❌ ตั้งใจไม่ทำ | `00_OVERVIEW §0.10` + `02_API §8` |

> เขียนเหตุผลไว้ **4 ที่** ตามบทเรียน F-SEC-TRANS — กันคนอ่านเข้าใจว่าตกหล่น

## R2.5 WARN รอบ 2

### WARN-C · เคส `[Phase B]` 13 เคสยังทดสอบไม่ได้บนต้นแบบ
TC-07 · 08 · 17 · 49 · 50 · 51 · 52 · 53 · 54 · 55 · 57 · 58 และบางส่วนของ TC-16
ทั้งหมดเป็นเคสฝั่ง server / สิทธิ์ / concurrency ที่ต้นแบบ (ไม่มี backend) ทดสอบไม่ได้โดยธรรมชาติ — **ไม่ใช่ช่องว่างของเอกสาร** แต่ต้องไม่หายไปตอน dev รับงาน

### WARN-D · 2 เคสที่ **ไม่ผ่าน** บนต้นแบบ (ไม่ block pack · เป็นงาน Phase B)
| เคส | สิ่งที่วัดได้ | งาน |
| --- | --- | --- |
| TC-48 responsive 768 | `scrollWidth 796 > innerWidth 768` | TD-04 |
| TC-60 ศัพท์ภายในบนจอ | 11 จุด | TD-03 → LD-12 |

### WARN-E · EC-03 (ยอดเท่ากันสองราย) ยังไม่มีข้อมูลตัวอย่าง
ตรรกะถูกต้อง (epsilon `0.005` ใน `bestUnit`/`bestTotal`) แต่ seed ไม่มีคู่ที่เท่ากันพอดี → **ทดสอบได้จากการอ่านโค้ดเท่านั้น**
แนะนำ: Phase B เพิ่มข้อมูลตัวอย่างอีก 1 ใบที่ยอดเท่ากับใบต่ำสุดพอดี เพื่อให้ TC-25 กดเห็นบนจอได้จริง
