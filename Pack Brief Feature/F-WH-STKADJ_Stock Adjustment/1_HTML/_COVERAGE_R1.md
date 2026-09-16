# _COVERAGE_R1 — F-WH-STKADJ (S3b · qc-coverage-checker รอบ 1 · HTML)

วันที่ 2026-09-10 · contract = `PREBRIEF_F-WH-STKADJ.md` (S-01..S-25 · BR-01..BR-25 · OB-1..OB-17) + `FUNCTION_CHECKLIST_F-WH-STKADJ.md` (54 FN / 8 หมวด) + `briefs/W3Q/CHECKLIST.md` + chip declarations
artifact = `1_HTML/F-WH-STKADJ.html` · ทุก ✓ มี evidence (ฟังก์ชัน/selector/ข้อความจริงในไฟล์)

---

## 1. FN Coverage (54/54)

### หมวด 1 · การสร้างใบ + เลือกช่องเก็บ
| FN | ผล | Evidence |
|---|---|---|
| FN-01 | ✅ | `comboItems('bin:*')` กรอง `ADJ_TYPES.quar.bins = ['quarantine']` → เลือก "ปรับยอดกักกัน" เหลือเฉพาะ `QA-*` |
| FN-02 | ✅ | `ADJ_TYPES.writeoff.bins = ['damage']` → เหลือเฉพาะ `DM-*` |
| FN-03 | ✅ | `BIN_BY['B-03-02-B'].locked` → option `disabled` + pill "ล็อก" + บรรทัดรองบอกเหตุ (`paintCombo` `it.disabled`) |
| FN-09 | ✅ | `setWarehouse()` → `window.confirm('เปลี่ยนคลังจะล้างรายการที่เลือกไว้ N รายการ…')` |

### หมวด 2 · กรอกรายการปรับยอด (B2 v2)
| FN | ผล | Evidence |
|---|---|---|
| FN-04 | ✅ | `applyItemToLine()`/`applyBinToLine()` → `l.system_qty = stockOf(bin,item)` · คอลัมน์ "ยอดระบบ" + ชิป `delta-up` |
| FN-05 | ✅ | `signed(l.qty)` + class `delta-down` (แดง) เมื่อผลต่างเป็นลบ |
| FN-06 | ✅ | `calcLineVat()` → `netAmount = qty × unit_price` แสดงที่คอลัมน์ "มูลค่าที่ปรับ" (`signedMoney`) |
| FN-07 | ✅ | segmented `setLineMode('correct'/'delta')` → `updateLine(...,'correct_qty'/'delta')` แปลงกลับไปมาผ่าน `migrateLine()` |
| FN-08 | ✅ | `renderLineSummary()` แสดง "มูลค่าสุทธิ (+/−)" และ "มูลค่าที่ปรับรวม (ค่าสัมบูรณ์)" แยกบรรทัด (`absTotal` vs `netTotal`) |
| FN-10 | ✅ | `wizardNext()` step 3: `dup[bin+'|'+item]` → toast "ช่องเก็บ + สินค้า ซ้ำกัน: …" |
| FN-11 | ✅ | `wizardNext()` step 3: `l.qty === 0` → toast "มีบรรทัดที่ยอดไม่ต่างจากยอดระบบ — แก้ยอดหรือลบแถวก่อน" |
| FN-12 | ✅ | `renderLineSummary()` `.hard-warn` "ยอดหลังปรับติดลบ N รายการ … (คงเหลือ X)" + `createWizard._over` → ปุ่มส่ง `disabled` (Render Gate ช็อต 27) |
| FN-13 | ✅ | แถวขยาย: `ต้นทุนอ้างอิง ${formatMoney(l.unit_price)} / หน่วย` + pill "ทะเบียนสินค้า" (อ่านอย่างเดียว) · `CFG.allowCostOverride=false` + `FWD-WIRE: valuation engine (W5)` |

### หมวด 3 · เหตุผล + หลักฐาน
| FN | ผล | Evidence |
|---|---|---|
| FN-18 | ✅ | `validateAll()` + `wizardNext()` step 3 → toast "ระบุเหตุผลให้ครบทุกบรรทัด — <ชื่อสินค้า>" · คอลัมน์ 7 แสดง pill แดง "ต้องระบุ" (`reasonBadge`) |
| FN-37 | ✅ | `comboItems('lreason:<id>')` กรองตามทิศ (`r.dir === '+'/'-'/'both'` เทียบ `l.qty`) |
| FN-40 | ✅ | `REASON_BY[code].note === true` → `validateAll()`/`wizardNext()` บังคับ `l.note` (RS-03/RS-06/RS-07/RS-99) |
| FN-41 | ✅ | `comboPick('reason')` → เติมทุกบรรทัดที่ `!l.reason_code` แล้วยังแก้รายบรรทัดได้ในแถวขยาย |
| FN-33 | ✅ | `mockUpload()` + `.upload-zone` (step 4) · ไฟล์โผล่ที่ view tab รายละเอียด `SEC('paperclip', 'เอกสารแนบ (N ไฟล์ · Document Center)')` |
| FN-51 | ✅ | `ADJ_TYPES.writeoff.needFile` → `.hard-warn` ใน step 4 + `wizardNext()` step 4 บล็อก + `validateAll()` |

### หมวด 4 · สายอนุมัติ (DOA)
| FN | ผล | Evidence |
|---|---|---|
| FN-14 | ✅ | `renderSubmitModal()` header แสดง "มูลค่าที่ปรับ X บาท (สุทธิ …)" + บรรทัด `resolveDoa(s).why[0]` = "ฐานวงเงิน = ผลรวมค่าสัมบูรณ์…" |
| FN-15 | ✅ | `MOCK_DOA_ENTRY.matrix[0]` (0–20,000) → 1 slot · mock `ADJ-2026-0001` (97.50) |
| FN-16 | ✅ | matrix set 2 (20,001–200,000) → 2 slots เรียงลำดับ · mock `ADJ-2026-0003` (23,575) |
| FN-17 | ✅ | `confirmSubmit()` → `modalState.err = true` + `.slot-row.is-err` + toast "เลือกผู้อนุมัติให้ครบทุกขั้น" (Render Gate ช็อต 18) |
| FN-42 | ✅ | ทุกจุดใช้ `empChip(name, roleId)` = avatar + ตำแหน่ง·แผนก + ชื่อ · ไม่มี role id ดิบบนจอ (`ROLE_LABEL` map เป็นชื่อไทยเสมอ) |
| FN-43 | ✅ | `resolveDoa()` ใช้ `absTotal(doc)` — mock `ADJ-2026-0003` สุทธิ −10,175 แต่ค่าสัมบูรณ์ 23,575 → ได้ 2 ขั้น |

### หมวด 5 · สถานะเอกสาร + ผ่านรายการ + กลับรายการ
| FN | ผล | Evidence |
|---|---|---|
| FN-19 | ✅ | `saveDraft()` → `persist(false)` (ไม่ออกเลข) · list แสดง "ร่าง — ยังไม่ออกเลขที่" · ไม่แตะ `STOCK` |
| FN-20 | ✅ | `confirmSubmit()` → `s.code = nextCode()` (`ADJ-2026-NNNN` ปี ค.ศ.) + comment `FWD-WIRE: ENG-DOC-NUM` |
| FN-21 | ✅ | `confirmApprove()` → `cur.status='approved'` → มี `next` ⇒ ส่งต่อ · ไม่มี ⇒ `s.status='approved'` |
| FN-22 | ✅ | `openRejectModal()` → `reasonModal` บังคับเหตุผล → `s.status='draft'` + `approval_history` เก็บรอบเดิม |
| FN-23 | ✅ | `headerActions()` ปุ่ม "ผ่านรายการ" โผล่เฉพาะ `status==='approved'` · `openPostModal()` ตรวจซ้ำ `if (s.status !== 'approved') return` |
| FN-24 | ✅ | `openCancelModal()` = `reasonModal` + select ประเภทเหตุผล → `s.status='cancelled'` (ใบยังอยู่ใน `DOCS`) |
| FN-25 | ✅ | `headerActions()` `status==='posted'` → เหลือปุ่ม "กลับรายการ" เท่านั้น (ไม่มี "ยกเลิก") |
| FN-26 | ✅ | filter สถานะครบ 6 ค่า + "ทุกสถานะ" ใน `renderFilterBar()` |
| FN-27 | ✅ | `qtyDrift(s)` → banner ใน tab รายละเอียด + `openPostModal()` แสดง 2 ยอด + `<select id="md-base">` (ยอดที่บันทึกไว้ / ยอดล่าสุด) |
| FN-44 | ✅ | `openReverseModal()` → `if (s.status !== 'posted' \|\| s.reversal) return` · ใบที่กลับรายการแล้ว `status='reversed'` ไม่มีปุ่ม |

### หมวด 6 · ผลปลายทาง
| FN | ผล | Evidence |
|---|---|---|
| FN-29 | ✅ | tab "ผลต่อสต๊อก" → `renderStockTab()` ตาราง `s.movements` · ใบกลับรายการมี `reversalOf` + ใบเดิมมี `s.reversal.doc` (ผูก 2 ทาง) |
| FN-30 | ✅ | คอลัมน์ "การลงบัญชี" = pill "รอลงบัญชี" · KV "การลงบัญชี" ใน tab รายละเอียด + ข้อความ `FWD-WIRE: JE posting (W5)` · ไม่มีปุ่มลงบัญชี |
| FN-45 | ✅ | ไม่มี handler ลบ/แก้ movement ทั้งไฟล์ (`s.movements` ถูกเขียนครั้งเดียวตอน post; กลับรายการ = สร้างใบใหม่) + note "append-only" |
| FN-34 | ✅ | `renderPdfTab()` = toolbar + `.a4` (หัวบริษัท · เลขที่ · วันที่ ค.ศ. · คลัง · ตาราง 8 คอลัมน์ · totals 4 บรรทัด · 3 ช่องเซ็น) + ปุ่มพิมพ์ `window.print()` |
| FN-28 | ✅ | `renderSignTab()` = KV 4 ช่อง + `pgl()` + `.tl` timeline ต่อขั้นพร้อม `empChip` + เวลา ค.ศ. |
| FN-31 | ✅ | บรรทัดเก็บ `item_name`/`uom`/`bin` เป็นข้อความในตัว record — ไม่ resolve จาก master ตอนแสดง (`linesTableView` ใช้ `l.item_name`) |

### หมวด 7 · ขอบเขต — พิสูจน์ว่า "ไม่มี" (negative)
| FN | ผล | Evidence |
|---|---|---|
| FN-32 | ✅ | `comboItems('bin:*')`: `if (b.type === 'in-transit') return false` · Render Gate พิมพ์ `TR-` → เมนูแสดง **"ไม่พบรายการ"** (ช็อต 28) |
| FN-35 | ✅ | grep ทั้งไฟล์: `นับสต๊อก`=0 · `ใบนับ`=0 · `นับรอบ`=0 · `count sheet`=0 · `cycle count`=0 |
| FN-36 | ✅ | grid มี 9 ช่องตาม contract ไม่มีคอลัมน์ปลายทาง · grep `bin ปลายทาง`=0 · `ย้ายไป`=0 · step 1 มี note ชี้ไป "ย้ายคลัง / สาขา" |
| FN-46 | ✅ | ประเภท `quar` เลือกได้เฉพาะ bin `quarantine` — ไม่มีทางระบุปลายทาง storage (ไม่มีช่องปลายทางเลย) |
| FN-47 | ✅ | ช่อง "เลขที่" ใน step 2 เป็น `disabled` · ไม่มีหน้าตั้งค่าเลขรัน · `nextCode()` มี comment ชี้ ENG-DOC-NUM |
| FN-48 | ✅ | grep `threshold`=0 · ไม่มี input % เตือนใด ๆ ในฟอร์ม |
| FN-49 | ✅ | หัวตาราง `line-tbl` = # · สินค้า · ยอดระบบ · ช่องเก็บ · ยอดที่ถูกต้อง · ผลต่าง · เหตุผล · มูลค่าที่ปรับ · (action) — ไม่มี VAT/ส่วนลด |

### หมวด 8 · ทั่วไป
| FN | ผล | Evidence |
|---|---|---|
| FN-90 | ✅ | `renderTableOnly()` + `emptyStateHTML()` 2 เคส (ยังไม่มีข้อมูล / filter ไม่เจอ) |
| FN-91 | ✅ | ยกเลิก/กลับรายการผ่าน modal เสมอ · ไม่มีปุ่มลบใด ๆ ในไฟล์ |
| FN-92 | ✅ | `markErr()`+`wizardNext()`+`validateAll()` · ปุ่ม submit/post `disabled` + `loader-2` กัน double-submit |
| FN-38 | ✅ | `fdate()/fdt()` ใช้ `d.getFullYear()` (ค.ศ.) ทุกจุด รวม PDF และ footer · ไม่มี `toLocaleDateString('th-TH')` ในโค้ด feature |
| FN-39 | ✅ | `pushAudit()` ทุก transition → `renderHistoryTab()` append-only + note "ลบหรือแก้ไม่ได้" |
| FN-50 | ✅ | sidebar = module map กลาง (คลังสินค้า 8 รายการ / จัดซื้อ 3 / นโยบายและเอกสาร 2) — ไม่มีเมนูที่ feature คิดเอง |

**สรุป: 54/54 FN มี hook จริง — ไม่มี FN ที่ไม่มีที่ยืนบนจอ**

---

## 2. Scenario coverage (S-01..S-25)

| S | ทางเข้าใน HTML |
|---|---|
| S-01 / S-02 | wizard step 3 กรอกยอดสูง/ต่ำกว่ายอดระบบ · mock `ADJ-2026-0001` (+15) / `ADJ-2026-0002` (−24) |
| S-03 | mock `ADJ-2026-0003` ใบผสม 4 บรรทัด (+/−) · summary แยกเพิ่ม/ลด/สุทธิ/ค่าสัมบูรณ์ |
| S-04 | `wizardNext()` บล็อกผลต่าง 0 |
| S-05 | `.hard-warn` + ปุ่มส่งอนุมัติ disabled (ช็อต 27) |
| S-06 | `saveDraft()` → mock `DRAFT-0004` (ไม่มีเลขที่) |
| S-07 | submit → approve → post (Render Gate เดินครบ) |
| S-08 | `openRejectModal()` · mock `ADJ-2026-0005` มี `approval_history` รอบที่ถูกตีกลับ |
| S-09 | `openCancelModal()` · mock `ADJ-2026-0006` |
| S-10 | `openReverseModal()` → สร้างใบใหม่ + ผูกคู่ · mock `ADJ-2026-0007` ↔ `ADJ-2026-0008` |
| S-11 / S-12 | `resolveDoa()` matrix 4 set — 1 ขั้น vs 2 ขั้น (mock 0001 vs 0003) |
| S-13 | `confirmSubmit()` slot ว่าง → `.slot-row.is-err` |
| S-14 | bin `B-03-02-B` locked → option disabled + เหตุผลที่ล็อก |
| S-15 | `qtyDrift()` banner + `openPostModal()` ให้เลือกฐาน |
| S-16 | บรรทัดเก็บข้อความสินค้าไว้เอง (ไม่ FK) |
| S-17 | `confirmPost()` → movement + `STOCK` ขยับ + สถานะ "รอลงบัญชี" |
| S-18 | ประเภท "ปรับยอดกักกัน" · mock `ADJ-2026-0009` (QA-01) |
| S-19 | ประเภท "ตัดจำหน่ายของเสีย" · mock `DRAFT-0010` (DM-01 + หลักฐานบังคับ) |
| S-20 | bin `in-transit` ถูกกรองออกทั้งหมด (negative — พิสูจน์แล้ว) |
| S-21 | `.upload-zone` + section เอกสารแนบใน landing tab |
| S-22 | tab PDF Preview + tab ลายเซ็น + ปุ่มพิมพ์ |
| S-23 | `setWarehouse()` confirm ก่อนล้างบรรทัด (1 ใบ = 1 คลัง) |
| S-24 | **ไม่รองรับ** — ไม่มีคำ/หน้า/ปุ่มใด ๆ (grep = 0) |
| S-25 | **ไม่รองรับ** — ไม่มีช่องปลายทาง + microcopy ชี้ไป "ย้ายคลัง / สาขา" |

---

## 3. Business Rules coverage (BR-01..BR-25)

ครบ 25/25 — จุดที่เป็นหัวใจของ feature:

| BR | จุดในโค้ด |
|---|---|
| BR-01 | `wizardNext()` dup key `bin|item` |
| BR-02 | `wizardNext()` + `validateAll()` `qty === 0` |
| BR-03 | `renderLineSummary()` hard-warn + `_over` → footer disable |
| BR-04 | `setWarehouse()` confirm ล้างบรรทัด |
| BR-05 | ไม่มีช่องปลายทางในโครงสร้างข้อมูลและ UI + note ใน step 1 |
| BR-06 | `reasonBadge()` "ต้องระบุ" + `validateAll()` |
| BR-07 | `comboItems('lreason:*')` กรองตามทิศ |
| BR-08 | `headerActions()` ปุ่มผ่านรายการเฉพาะ `approved` |
| BR-09 | `resolveDoa()` ใช้ `absTotal()` |
| BR-10 | `confirmSubmit()` ตรวจทุก slot มี `assignee` |
| BR-11 | `openRejectModal()` เหตุผลบังคับ |
| BR-12 | `ADJ_TYPES[t].bins` กรอง picker |
| BR-13 | `if (b.type === 'in-transit') return false` |
| BR-14 | `b.locked` → option `disabled` |
| BR-15 | `qtyDrift()` + `md-base` |
| BR-16 | ไม่มี delete/update movement |
| BR-17 | `openReverseModal()` เหตุผลบังคับ + ใบทิศตรงข้าม |
| BR-18 | `s.reversal` guard + ผูก `reversalOf` 2 ทาง |
| BR-19 | pill "รอลงบัญชี" + `FWD-WIRE: JE posting` |
| BR-20 | ไม่มี field threshold ในไฟล์ |
| BR-21 | `persist(issueCode)` — ออกเลขตอนส่งอนุมัติเท่านั้น |
| BR-22 | บรรทัดเก็บข้อความ master ไว้เอง |
| BR-23 | `needFile` บังคับแนบไฟล์ |
| BR-24 | grep คำนับสต๊อก = 0 |
| BR-25 | `pushAudit()` ทุก transition |

---

## 4. Declaration coverage (chip = `doa, ntf, csq, doccfg, pdfdoc`)

| chip | เจอในไฟล์? | Evidence | ตรง chip |
|---|---|---|---|
| `doa` | ✅ | `MOCK_DOA_ENTRY` + `resolveDoa()` + `.slot-row` slot picker คนจริง + `FWD-WIRE: DOA engine` | ✅ |
| `ntf` | ✅ | `FWD-WIRE: ENG-NOTIFY emit` ที่จุดส่งอนุมัติ/post + note ใน submit modal | ✅ |
| `csq` | ✅ | `FWD-WIRE: ENG-CSQ emit (adj_posted_increase / adj_posted_decrease)` ที่ `confirmPost()` | ✅ |
| `doccfg` | ✅ | `CFG.docPrefix='ADJ'` + `nextCode()` + `FWD-WIRE: ENG-DOC-NUM` (ห้าม format เอง) | ✅ |
| `pdfdoc` | ✅ | tab PDF Preview `.a4` ตาม `print-spec-adj.md` + 3 ช่องเซ็น | ✅ |

**detect = chip เป๊ะ — ไม่มี DIVERGENCE** (ไม่มี declaration ส่วนเกิน เช่น ไม่มีสายอนุมัติ hardcode, ไม่มี channel แจ้งเตือนใน feature)

---

## 5. Pattern Q surface coverage

| surface | ผล |
|---|---|
| List (สถานะเอกสาร + ลายเซ็น n/N + ยอด + ⋮) | ✅ |
| Create wizard 5 steps ชื่อล็อก | ✅ |
| View drawer tabs ล็อก + เอกสารแนบใน landing | ✅ |
| PDF `.a4` + 3 ช่องเซ็น | ✅ |
| DOA slot picker คนจริง | ✅ |
| B2 v2 line editor (grid 9 ช่อง widths ตรง contract) | ✅ |

---

## 6. Scope creep check

| ตรวจ | ผล |
|---|---|
| cycle count / ใบนับ / นับรอบ / count sheet | **0 ครั้งทั้งไฟล์** ✅ |
| ย้าย location (bin ปลายทาง / ย้ายไป / transfer) | **ไม่มีช่อง ไม่มีปุ่ม** ✅ (มีเฉพาะ microcopy ชี้ทางไป feature อื่น) |
| เขียน `in-transit` | **กรองออกจาก picker ทุกกรณี** ✅ |
| สร้าง/แก้ Location Master | ไม่มี ✅ (bin เป็น picker อ่านอย่างเดียว) |
| ตั้งค่าสายอนุมัติ / เลขรัน / threshold ในหน้า feature | ไม่มี ✅ |
| Lot/Serial · CSV import · revaluation | ไม่มี ✅ |

---

## 7. Gap / ของที่ตั้งใจไม่ทำในรอบนี้ (log ไว้ ไม่เงียบ)

| # | เรื่อง | เหตุผล |
|---|---|---|
| G1 | ต้นทุนอ้างอิงเป็น mock จากทะเบียนสินค้า | valuation engine = W5 (`[ASSUMED contract]` · PREBRIEF gap G-01) — มีป้าย/คอมเมนต์ `FWD-WIRE: valuation engine` |
| G2 | JE ไม่ post จริง | W5 (BR-19) — สถานะค้างที่ "รอลงบัญชี" |
| G3 | สิทธิ์ใช้เหตุผลรายตำแหน่ง (OQ-ADJ-06) | ยกไป Security Preset ตอน BRD — รอบนี้ไม่จำกัดใน UI |
| G4 | KPI/report แยกหน้า | ไม่อยู่ scope — มีเฉพาะ stat row 4 ใบบน list |

---

**VERDICT: PASS** — FN 54/54 · S-01..S-25 มีทางเข้าครบ (รวม negative 3 ตัว) · BR 25/25 · declaration ตรง chip · Pattern Q ครบ 6 surface · scope creep = 0
