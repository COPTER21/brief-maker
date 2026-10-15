# _COVERAGE_REPORT — F-PUR-PR · PR ใบขอซื้อ
skill `qc-coverage-checker` · contract: `PREBRIEF_F-PUR-PR.md` + `FUNCTION_CHECKLIST` FN-01..FN-24 + registry F072

---

# รอบ 1 — HTML (ขั้น 7R · re-gate หลัง vibe) · 2026-09-13

## Verdict: **PASS** (0 BLOCK · 2 WARN · 0 DIVERGENCE)

> รันใหม่บนไฟล์หลัง vibe ตาม §7R ข้อ 3 — **ไม่ได้ยก `0_DIRECTION/_COVERAGE_R1.md` มาใช้แทน**
> ทุก ✅ ด้านล่างยืนยันด้วยชื่อฟังก์ชัน/ตัวแปรจริงที่ `grep` เจอในไฟล์ แล้วเปิดอ่านโค้ดว่า **ถูกเรียกใช้จริง ไม่ใช่ const ตาย**

## 1. FN coverage — FN-01..FN-24

| FN | ฟังก์ชัน | หลักฐานในไฟล์ (ตรวจแล้วว่าถูกเรียกจริง) | ผล |
|---|---|---|:--:|
| FN-01 | List + คอลัมน์ครบ lean | `renderList()` · `<th>` 10 คอลัมน์ 1 บรรทัด/เซลล์ · `sortBy()` ผูก 4 คอลัมน์ | ✅ |
| FN-02 | ค้นหา + filter | `LIST.q/status/dept/requester` + `resetF()` · `MOCK_DEPT`/`MOCK_EMP` ป้อน `<select>` | ✅ |
| FN-03 | แถบเอกสารแนบใน landing | การ์ด `เอกสารแนบล่าสุด` ท้าย list รวมไฟล์ข้ามใบ | ✅ |
| FN-04 | empty / loading / error | `LIST.loading` (skeleton) · `LIST.error` + `retryLoad()` + ปุ่ม `ลองใหม่` · empty แยก 2 แบบ (ยังไม่มีข้อมูล / กรองแล้วไม่เจอ) — **ยืนยันด้วยภาพ** `_shots/06_empty_filtered.png` · `07_error_state.png` | ✅ |
| FN-05 | wizard 5 ขั้น | `renderCreateDrawer()` + `STEP_NAMES` (ชื่อตรง LOCK หลังแก้ B1) + `stepItem()` (done คลิกย้อนได้ · active/future คลิกไม่ได้) | ✅ |
| FN-06 | header ครบ + validate วันที่ | `wizardNext()` step 2 → `markErr()` 4 ช่อง + เงื่อนไข `d.requiredDate < d.docDate` | ✅ |
| FN-07 | Cost center picker nullable | `<select>` จาก `MOCK_CC` มี option ว่าง `— ไม่ระบุ —` · ไม่มี `required` | ✅ |
| FN-08 | B2 v2 grid 9 ช่อง | `<th>` width 26/auto/64/92/92/78/72/104/54 · `.line-tbl` 12.5px | ✅ |
| FN-09 | Item combobox + free-text | `.item-combo` · `applyItemToLine()` · `useFreeText()` · `focusCombo()`/`scheduleCloseCombo()` กัน focus หลุด | ✅ |
| FN-10 | ส่วนลดรายบรรทัด | คอลัมน์ `ส่วนลด %` + `discount_mode` รองรับ amt/pct ใน engine | ✅ |
| FN-11 | VAT segmented 3 โหมด | segmented ในแถวขยาย + `taxBadgeV()` · โหมด none/add/included คำนวณย้อนได้ | ✅ |
| FN-12 | Totals ครบตามลำดับ | `renderLineSummary()` — ก่อน VAT → VAT → หลัง VAT → ส่วนลดท้ายบิล → ยอดสุทธิ **ยืนยันด้วยภาพ** `_shots/05_wizard_step3.png` | ✅ |
| FN-13 | เพิ่ม/ลบแถว + กันแถวว่าง | `addLine()`/`removeLine()` · `wizardNext()` step 3 มี **3 ด่าน**: ต้องมี ≥1 แถวสมบูรณ์ · กันแถวว่าง · กันสินค้า+หน่วยซ้ำ — **อ่านโค้ดยืนยันว่าอยู่นอก `return` ไม่ใช่ dead code** | ✅ |
| FN-14 | ผู้ขายแนะนำ soft-ref | `addVendor()`/`removeVendor()` · อยู่ในขั้น 2 ตาม DIVERGENCE-0 | ✅ |
| FN-15 | แนบไฟล์ + validate | `.upload-zone` · `mockUpload()` · `mockUploadBad()` แสดง error inline ไม่ล้มฟอร์ม | ✅ |
| FN-16 | Step 5 read-only | `renderStep5()` — ไม่มี input ที่แก้ได้ | ✅ |
| FN-17 | ตรวจงบ mock ไม่ block | `budgetCheckMock()` คืน `{ok,remaining,budget_code,mock:true}` · แสดง `hard-warn` + pill `งบไม่พอ (จำลอง)` · **ยังกดส่งอนุมัติได้** · มี `// TODO: budget-control hook` | ✅ |
| FN-18 | DOA slot picker คนจริง | `renderSubmitModal()` `.slot-row` + `empChip()` = avatar + ชื่อ + ตำแหน่ง · `SLOT_CANDIDATES` map role→คน | ✅ |
| FN-19 | บันทึกร่าง / ส่งอนุมัติ | `saveDraft()` · `doSubmit()` — เลขที่ออกตอน submit เท่านั้น (`nextDocNo()`) | ✅ |
| FN-20 | View รายละเอียด + ปุ่มตามสถานะ | `renderDetailTab()` + `canActStep()` | ✅ |
| FN-21 | View PDF A4 | `renderPdfTab()` `.a4` + `bahtText()` (จำนวนเงินตัวอักษร) + 3 ช่องเซ็น · **ภาพ** `_shots/04_tab_pdf.png` | ✅ |
| FN-22 | View ลายเซ็น ต่อ slot | `renderSignTab()` การ์ดต่อ slot + สถานะ + วันเวลา + เหตุผล · **ภาพ** `_shots/04_tab_sign.png` | ✅ |
| FN-23 | View ประวัติ append-only | `renderHistoryTab()` อ่าน `d.audit` · เขียนผ่าน `pushAudit()` 10 จุด · **ไม่มีฟังก์ชันลบ** · **ภาพ** `_shots/04_tab_history.png` | ✅ |
| FN-24 | อนุมัติ/ไม่อนุมัติ/เรียกคืน/ยกเลิก/คัดลอก | `doApprove()` · `openReasonModal('reject')` · `doRecall()` · `openReasonModal('cancel')` · `duplicateDoc()` | ✅ |

**FN ครบ 24/24**

## 2. Scenario coverage — SC-01..SC-15

| SC | ผล | หลักฐาน |
|---|:--:|---|
| SC-01 happy path | ✅ | เดินครบ wizard 5 ขั้น → submit → approve · walk ผ่าน Playwright |
| SC-02 บันทึกร่างแล้วกลับมาแก้ | ✅ | `saveDraft()` · เลขที่ยังไม่ออกจนกว่าจะ submit |
| SC-03 free-text ไม่มีใน master | ✅ | `useFreeText()` · soft-ref ไม่ block |
| SC-04 ไม่อนุมัติ + เหตุผล | ✅ | `openReasonModal('reject')` บังคับเหตุผล ≥3 ตัวอักษร · slot ที่เหลือไม่ต้องตัดสิน |
| SC-05 เรียกคืนระหว่างรออนุมัติ | ✅ | `doRecall()` → กลับ DRAFT · ลายเซ็นเดิมถูก void แต่คงอยู่ในประวัติ |
| **SC-06 ยอดเกินวงเงิน slot** | ⚠ | **ทำคนละแบบกับที่ PREBRIEF เขียนไว้** — ดู WARN W1 |
| SC-07 ตรวจงบไม่ผ่าน | ✅ | เตือนอย่างเดียว ไม่ block (ตรง LOCK §3 ข้อ 6) |
| SC-08 แก้หลังส่งอนุมัติ | ✅ | route `#/edit` เด้งกลับ view + note-box อธิบายให้เรียกคืนก่อน |
| SC-09 ยกเลิกใบที่อนุมัติแล้ว | ✅ | `openReasonModal('cancel')` บังคับเหตุผล + destructive confirm + append ประวัติ |
| SC-10 ไม่มีสิทธิ์อนุมัติ | ✅ | `canActStep()` เทียบ `ACT_AS` (ตัวตนผู้ใช้ปัจจุบัน) กับ `assignee` ของ slot ที่ pending → คืน -1 → **ไม่ render ปุ่มอนุมัติ** · **เป็นการผูกสิทธิ์จริง ไม่ใช่ flag ตาย** |
| SC-11 ไฟล์เกินขนาด/ผิดชนิด | ✅ | `mockUploadBad()` → error inline ระบุชนิดและขนาดที่รองรับ · ไฟล์อื่นยังอยู่ครบ |
| SC-12 คัดลอกใบเดิม | ✅ | `duplicateDoc()` + ขั้น 1 tile `จากใบขอซื้อเดิม` — ไม่คัดลอกเลขที่/ลายเซ็น/ประวัติ |
| SC-13 รายการว่างแล้วส่ง | ✅ | `wizardNext()` step 3 ด่านที่ 1 |
| SC-14 วันที่ต้องการใช้ < วันที่เอกสาร | ✅ | `markErr('requiredDate', …)` |
| SC-15 list ว่าง / โหลดพัง | ✅ | empty 2 แบบ + error + `retryLoad()` |

## 3. Declaration coverage — ชิปครบ 5 ใบ (registry F072)

| ชิป | ใบประกาศใน `5_DECLARATIONS/` | hook ในจอ | ผล |
|---|---|---|:--:|
| ⚖ `doa` | `DOA_BRIEF_F-PUR-PR.md` | `MOCK_DOA_TIERS` (3 tier · `doa_entry_ref`) + `resolveDoa()` + slot picker | ✅ |
| 🔔 `ntf` | `NTF_BRIEF_F-PUR-PR.md` | comment `ENG-NOTIFY.emit(...)` ที่ transition จริง 5 จุด (submitted/approved/rejected/recalled/cancelled) | ✅ |
| ◆ `csq` | `CSQ_BRIEF_F-PUR-PR.md` | comment `ENG-CSQ doc.approved (EC/estimated)` · `doc.cancelled (EC/avoided)` | ✅ |
| `doccfg` | `DOCCFG_BRIEF_F-PUR-PR.md` | `nextDocNo()` + comment `ENG-DOC-NUM.next('PR')` · ออกเลขตอน submit เท่านั้น | ✅ |
| 📄 `pdfdoc` | `PRINT_SPEC_PR.md` | แท็บ PDF `.a4` ตาม field mapping ของ print spec | ✅ |

**ชิปที่ประกาศ = surface ที่มีบนจอ → ไม่มี DIVERGENCE ทั้งสองทิศ** (ไม่มีชิปที่ไม่มีของ · ไม่มีของที่ไม่มีชิป)

## 4. Scope creep

ไม่พบ · `grep -c 'renderPoDrawer|renderGrnDrawer|renderCompare|renderBudget'` = **0**
ปุ่มปลายทาง (ส่งไปเทียบราคา · ออกใบสั่งซื้อ) เป็น hook ที่ขึ้น toast เท่านั้น ✅
soft-reference 4 ตัว (ผู้ขาย / สินค้า / ศูนย์ต้นทุน / หน่วยนับ) เป็น picker ไม่ FK ไม่ validate ✅

## 5. WARN รอบ 1

- **W1 · SC-06 ทำคนละแบบกับ PREBRIEF** — PREBRIEF เขียนว่า *"ยอดสุทธิเกินวงเงิน slot ที่เลือก → **เตือนที่ step 5** · ต้องเลือกผู้อนุมัติระดับที่ครอบวงเงิน"*
  แต่ไฟล์จริงใช้ `resolveDoa(amount)` **เลือกชั้นอนุมัติจากยอดให้อัตโนมัติ** → โดยโครงสร้างแล้ว "เกินวงเงินของ slot ที่เลือก" เกิดขึ้นไม่ได้ จึงไม่มีข้อความเตือนใด ๆ
  `grep -oE 'เกินวงเงิน'` = **0 จุด**
  → **ผลลัพธ์เชิงธุรกิจถูก** (ได้ผู้อนุมัติระดับที่ครอบยอดเสมอ) แต่ **ถ้อยคำใน PREBRIEF ไม่ตรงกับพฤติกรรมจริง**
  → ต้องบันทึกใน `03_FRD/07_LOCKED_DECISIONS.md` + เปิด OQ ให้ BA แก้ถ้อยคำ SC-06 · **ห้ามปล่อยเงียบ**
  (ต้นน้ำติ๊ก SC-06 ✅ โดยอ้าง `resolveDoa` 3 tier — ซึ่งอธิบายกลไกถูก แต่ไม่ได้บอกว่ามันไม่ตรงกับข้อความ "เตือน" ใน PREBRIEF)
- **W2 · `budgetCheckMock` ใช้ตัวเลขงบสมมติต่อศูนย์ต้นทุน** (`MOCK_BUDGET`) — Phase B ต้องแทนด้วย contract จริงของ F117 (W7)
  ค่า `[ASSUMED contract]` = `{ok, remaining, budget_code}` (A-01) ยังรอเจ้าของ W7 ยืนยัน

---
<!-- รอบ 2 (FRD + Testcases vs brief) จะถูกต่อท้ายไฟล์นี้หลัง Phase B -->

# รอบ 2 — FRD Pack + Testcases (ขั้น 13 · ก่อนปิด pack) · 2026-09-13

## Verdict: **PASS** (0 BLOCK · 3 WARN) — หลังปิดช่องว่าง 3 จุดที่ตรวจเจอในรอบนี้

ตรวจเชิงกล (set-difference) ไม่ใช่การเช็คจากความจำ — สคริปต์เทียบชุดรหัสระหว่างไฟล์

## 1. ผลตรวจ traceability (รันซ้ำหลังแก้)

| # | ตรวจอะไร | ผล |
|---|---|:--:|
| 1 | `FN-01..FN-24` (FUNCTION_CHECKLIST) → FRD Pack | ✅ 24/24 |
| 2 | `SC-01..SC-15` (PREBRIEF §5) → FRD Pack | ✅ 15/15 |
| 3 | `AC-01..AC-14` (BRD §7) → FRD Pack | ✅ 14/14 |
| 4 | `BR-01..BR-12` (05_RULES) → 06_TESTS | ✅ 12/12 |
| 5 | `V-01..V-09` (05_RULES) → 06_TESTS | ✅ 9/9 |
| 6 | `EC-01..EC-07` (05_RULES) → 06_TESTS | ✅ 7/7 |
| 7 | `C-01..C-08` COSO (05_RULES) → 06_TESTS | ✅ 8/8 |
| 8 | error code (02_API §2.10) → 06_TESTS | ✅ 17/17 |
| 9 | `XT-01..XT-06` cross-module (02_API §2.9) → 06_TESTS | ✅ 6/6 |
| 10 | `AT-01..AT-40` (06_TESTS) → testcases(AI) + DROP_LEDGER | ✅ ครบ |
| 11 | `AI-01..AI-45` (testcases) → DROP_LEDGER | ✅ ครบ |
| 12 | `LOCK-*` (BRD §3.4) → 07_LOCKED_DECISIONS | ✅ 7/7 |
| 13 | mutation API → Function/Engine (R8) | ✅ 10/10 · ไม่มี orphan |

## 2. ★ ช่องว่างที่ตรวจเจอในรอบนี้ และวิธีปิด

รอบแรกที่รันสคริปต์ **ไม่ผ่าน 3 จุด** — บันทึกไว้เพราะเป็นของจริงที่ gate จับได้ ไม่ใช่เขียนให้ผ่าน

| # | ช่องว่างที่เจอ | สาเหตุ | วิธีปิด |
|---|---|---|---|
| G1 | `FN-17..FN-24` ของ **FUNCTION_CHECKLIST** ไม่ปรากฏใน FRD เลย | **รหัสชนกัน** — `FN-xx` ของ checklist (ฟังก์ชันเชิงธุรกิจ 24 ตัว) ไปชนกับ `FN-xx` ที่ `03_LOGIC` ใช้เรียกฟังก์ชันชั้น logic (16 ตัว) · คนอ่านแยกไม่ออก และ FN-17..24 ของ checklist ไม่มีที่ลงจริง | เพิ่ม **`00_OVERVIEW §0.12.1`** ตาราง map `FN-01..FN-24` ของ checklist → ที่อยู่ใน pack + test · พร้อมคำเตือนว่าเป็นคนละชุดรหัสกับ `F-PUR-PR-FN-xx` |
| G2 | `SC-01..SC-15` ของ PREBRIEF ขาดหายไป 10 ข้อจาก FRD | FRD อ้างด้วย `AC-xx`/`EC-xx`/`BR-xx` แทน ทำให้ไล่จาก PREBRIEF กลับมาไม่เจอ | เพิ่ม **`00_OVERVIEW §0.12.2`** ตาราง scenario coverage ครบ 15 ข้อ · ระบุชัดว่า **SC-06 เป็นข้อเดียวที่ระบบทำคนละแบบกับ brief** (LD-10 · OQ-07) |
| G3 | `AT-14` · `AT-24` · `AT-27` ไม่มีเคสฝั่ง AI รองรับ | BR-06 (ราคาประมาณ) และ BR-12 (ผู้ขายที่แนะนำ) ประกาศไว้ใน `05_RULES` ครบ แต่ไม่มีเคสไหนอ้างถึง — **ตรงกับบทเรียนรอบ F-SEC-LOCKOUT ข้อ 5** | เติม trace `AT-14` เข้า AI-38 · เพิ่มขั้นตอนตรวจข้อความ **"ราคาประมาณจากผู้ขอ — ราคาจริงตัดสินที่ขั้นเทียบราคาผู้ขาย"** เข้า AI-18 (AT-24) · **เพิ่มเคสใหม่ AI-45** สำหรับผู้ขายที่แนะนำ (AT-27) แล้วยุบเข้าเคสฝั่งคน TC-10 |

> **วิธีปิดคือเพิ่มเคสและเติม trace — ไม่ใช่ลดจำนวนกติกาลงให้ตัวเลขสวย**

## 3. Testcase coverage

| ฝั่ง | ไฟล์ | จำนวน |
|---|---|---|
| FRD (ครบทุกชั้น รวมที่ต้องมี backend) | `03_FRD/06_TESTS.md` | **AT-01..AT-40** |
| AI agent (รันบนต้นแบบได้) | `04_QA/testcases-F-PUR-PR-001.md` | **AI-01..AI-45** |
| ผู้ทดสอบที่เป็นคน (Lite) | `04_QA/testcase-F-PUR-PR-001.html` | **TC-01..TC-36** · 6 กลุ่ม · 112 ขั้นตอน |
| บัญชีการแปลง | `04_QA/_build/DROP_LEDGER.md` | **ตัดทิ้งทั้งเคส 0** · ยุบรวม 9 |

**ภาพประกอบ:** `CAPTURE VERIFY` = **OK 26 · SKIP/FAIL 0** (ยืนยัน selector ทุกตัวด้วย `querySelectorAll` ก่อนเขียน shot-spec)

## 4. WARN รอบ 2

- **W3 · รหัส `FN-xx` ถูกใช้ 2 ความหมายในเลนนี้** — checklist (ธุรกิจ) กับ `03_LOGIC` (โค้ด)
  รอบนี้แก้ด้วยตาราง map + คำเตือน แต่ **ควรแก้ที่ต้นทาง** ให้ checklist กับ FRD ใช้ prefix ต่างกันตั้งแต่แรก (เสนอให้ BA พิจารณา)
- **W4 · คำว่า `Document Center` ปรากฏบนจอ 2 จุด** (การ์ดเอกสารแนบใน landing และหัวข้อเอกสารแนบในลิ้นชัก)
  เป็น **ชื่อโมดูลกลางของ CUBE** ไม่ใช่ศัพท์ภายในแบบ `ENG-*` จึงไม่ถือว่าละเมิด #81 เต็มตัว
  แต่ผู้ใช้ทั่วไปอาจไม่รู้จัก → **เสนอให้ BA เคาะว่าจะใช้ชื่อไทยแทนหรือไม่** (ไม่แก้เองในเลนนี้ เพราะเป็นชื่อโมดูลข้ามฟีเจอร์)
- **W5 · CSS `.line-collapse-panel` + keyframes `line-collapse-slide` ไม่ถูกใช้งาน**
  ตรวจแล้วเชื่อถือได้ (ไฟล์ **ไม่มี `classList.*` เลย** และไม่มีการต่อชื่อคลาสแบบ `'x-'+v`)
  → animation ตอนยุบแถวไม่ได้ถูกต่อ · **ไม่กระทบการใช้งาน** (ยุบแถวได้ปกติ) · ให้ dev เลือกว่าจะต่อ animation หรือลบ CSS

## 5. สิ่งที่ยังไม่ได้ตรวจในเลนนี้ (ตรวจไม่ได้จนกว่าจะมี backend)

ยอดเงินคำนวณฝั่งเซิร์ฟเวอร์ · optimistic lock ของ slot · idempotency ตอนส่งอนุมัติ · version conflict ·
เลขเอกสารต่อเนื่องจากทะเบียนจริง · การตรวจว่ามี PO อ้างถึงก่อนยกเลิก
→ ทั้งหมดมี test รออยู่แล้วใน `06_TESTS` (AT-20 · AT-22 · AT-23 · AT-25 · AT-30..AT-36)
