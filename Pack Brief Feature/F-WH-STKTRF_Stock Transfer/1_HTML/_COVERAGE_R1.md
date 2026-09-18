# _COVERAGE_R1 — F-WH-STKTRF · Stock Transfer

> Stage **S3b** · `qc-coverage-checker` รอบ 1 (HTML vs contract) · 2026-09-10
> Contract ที่เทียบ: `PREBRIEF_F-WH-STKTRF.md` (34 scenario · 34 BR · 15 transition) + `FUNCTION_CHECKLIST_F-WH-STKTRF.md` (**61 FN · 10 หมวด**) + `briefs/W3Q/CHECKLIST.md` + chip declarations
> **ทุก ✓ ต้องมี evidence จริง** (ชื่อฟังก์ชัน / selector / ข้อความบนจอ) — ไม่รับ "น่าจะมี"

---

## VERDICT: **PASS** — FN ครบ 61/61 · scope creep = 0 · exception path มีทางเข้าครบ · DIVERGENCE = 0

| ด้าน | ผล |
|---|---|
| FUNCTION_CHECKLIST (FN) | **61 / 61 มี hook จริง** |
| Scenario (S-01…S-34) | **34 / 34** (รองรับ 25 · "ไม่รองรับ" 9 ตัวมีหลักฐานว่า**ไม่มีจริง**) |
| Business Rule (BR-01…BR-33 + BR-09b) | **34 / 34 บังคับได้จริงบนจอ** |
| Transition (§5.1) | **15 / 15 เดินได้** |
| Declaration coverage (chip `doa,ntf,csq,doccfg,pdfdoc`) | **5 / 5** · detect = chip → **ไม่มี DIVERGENCE** |
| Pattern Q surface coverage | **4 / 4 surface** |
| Scope creep | **0** |

---

## 1. FN Coverage Ledger (61 FN)

### หมวด 1 · หัวใบ + โหมดการย้าย
| FN | Evidence ใน HTML | ✓ |
|---|---|---|
| FN-01 | `openCreateDrawer()` → `renderStep2()` `<select onchange="changeWarehouse('whFrom'…)">` (soft-ref ไม่ FK) | ✓ |
| FN-02 | `docMode(whFrom,whTo)` → `renderStep2()` ชิป `ภายในคลัง — ย้ายจบในจังหวะเดียว` | ✓ |
| FN-03 | เงื่อนไขเดียวกัน → ชิป `ข้ามคลัง/สาขา — ต้องมีขั้นยืนยันรับที่ปลายทาง` (`.route-chip.inter`) | ✓ |
| FN-04 | ไม่มี field คลังใน `createBlankLine()` — คลังอยู่หัวใบตัวเดียว (`d.whFrom/d.whTo`) | ✓ |
| FN-05 | `transitBinFor()` + ช่อง `จุดพักระหว่างทาง (in-transit)` `readonly` + `.route-node.transit` แสดง `TR-BKK-CNX` | ✓ |
| FN-09 | `changeWarehouse()` → `window.confirm('เปลี่ยนคลังจะล้างรายการที่กรอกไว้ N รายการ…และใบนี้จะเปลี่ยนโหมดการย้าย…')` | ✓ |
| FN-10 | `saveDraft()` · หัวใบ/list แสดง `(ร่าง — ยังไม่ออกเลขที่)` (mock `d7` code = `''`) | ✓ |
| FN-11 | `confirmSubmit()` → `if(!s.code) s.code=nextCode()` (รูปแบบ `TRF-2026-NNNN` ปี ค.ศ.) | ✓ |

### หมวด 2 · บรรทัดที่ย้าย (B2 v2)
| FN | Evidence | ✓ |
|---|---|---|
| FN-06 | `renderLineSummary()` → `problems.push('บรรทัด N … ย้าย X เกินยอดคงเหลือที่ BIN (Y)')` + `createWizard._over=true` → ปุ่มส่ง `disabled` · ช่อง qty ขอบแดง | ✓ |
| FN-07 | `wizardNext()` step 3: `if(real.some(l=>(+l.qty||0)<=0)) return showToast('จำนวนที่ย้ายต้องมากกว่า 0 ทุกบรรทัด')` | ✓ |
| FN-08 | `wizardNext()`: `if(real.some(l=>l.binFrom===l.binTo))` + inline `· bin ต้นทางและปลายทางต้องต่างกัน` ในแถว | ✓ |
| FN-12 | `renderLineSummary()` — มูลค่าก่อนภาษี / VAT / ยอดรวมหลังภาษี / **มูลค่ารวมที่ย้าย** จาก `totals()` ตัวเดียว | ✓ |
| FN-44 | grid มี 9 ช่องตาม contract · **ไม่มี** field Lot/Serial (grep `Lot`=0, `Serial`=0) · `.scanbox` "ช่องยิงรหัส (รอบถัดไป)" เผื่อไว้ | ✓ |

### หมวด 3 · กติกาประเภท location
| FN | Evidence | ✓ |
|---|---|---|
| FN-15 | `comboItems()` bin → `dis:locked` → `paintCombo()` render `disabled` + จาง + แสดง `lockReason` ("ล็อกเพื่อตรวจซ่อมชั้นวาง" ที่ `B-03-02-B`) · `setLineBin()` กันซ้ำอีกชั้น | ✓ |
| FN-16 | `comboItems()`: `if(!isFrom && srcType==='quarantine') return b.type==='quarantine'` · `setLineBin()` ล้าง binTo + toast "ของกักกันย้ายได้เฉพาะไปช่องเก็บกักกันด้วยกัน" · mock `TRF-2026-0013` = `QA-01 → CNX-QA-01` | ✓ |
| FN-17 | pool filter: `if(b.type==='in-transit' \|\| b.type==='damage' \|\| b.type==='staging') return false` → `DM-01` ไม่โผล่ทั้ง 2 picker | ✓ |
| FN-18 | filter เดียวกันตัด `staging` (`ST-DOCK-01/02`) ออก — ผู้ใช้เลือกไม่ได้ | ✓ |
| FN-19 | filter เดียวกันตัด `in-transit` → ค้น `TR-BKK-CNX` ใน picker **ไม่เจอ** · แสดงเป็น `readonly` บนหัวใบแทน | ✓ |
| FN-40 | `wizardNext()` step 2: `if(d.mode==='inter' && !transitBinFor(...)) return showToast('คู่คลังนี้ยังไม่มีจุดพักระหว่างทาง — ติดต่อผู้ดูแลผังตำแหน่งให้ตั้งค่าก่อน','error')` + แถบแดงใน `.route-band` + `openSubmitModal()` กันซ้ำ | ✓ |

### หมวด 4 · ★ 2 ขา (หัวใจ)
| FN | Evidence | ✓ |
|---|---|---|
| FN-13 | `doShip()` สาขา `mode==='intra'` → confirm → `l.received=l.qty` → `s.status='moved'` **ไม่แตะ transitBin เลย** · audit "ย้ายภายในคลังสำเร็จ … — ปิดใบ" | ✓ |
| FN-14 | `doShip()` สาขา `inter` → confirm ระบุ "ของจะออกจากช่องเก็บต้นทางไปพักที่ TR-… และยังไม่ถึงปลายทาง" → `s.status='in_transit'` (ยอดปลายทางยังไม่ขยับ) | ✓ |
| FN-20 | header summary line `ค้างระหว่างทาง N` + `renderDetailTab()` กล่อง `.note.warn` "ของที่ยังอยู่ระหว่างทาง N หน่วย · มูลค่า ฿X" + tab `ระหว่างทางและการรับ` | ✓ |
| FN-21 | `renderViewDrawer()`: `mayReceive = canReceive && s.whTo===ME.wh` → ปุ่ม `disabled title="ยืนยันรับได้เฉพาะเจ้าหน้าที่ของคลังปลายทาง (…)"` · `openReceiveModal()` กันซ้ำ + กันคนที่กดส่งออกมารับเอง | ✓ (ภาพ `_shots/03_view_transit.png` ปุ่มจาง) |
| FN-22 | `confirmReceive()` → `inTransitQty(s)===0` → `s.status='closed'` + toast "รับครบแล้ว — ปิดใบ" | ✓ |
| FN-23 | `confirmReceive()` → `s.status='partial'` + audit "ยังค้างระหว่างทาง N หน่วย (รอรับเพิ่ม)" · mock `TRF-2026-0003` (ส่ง 200 รับ 160 ค้าง 40) | ✓ |
| FN-28 | `renderReceiveModal()` inline "รับเกินจำนวนที่ส่งไม่ได้ — ถ้าของงอกจริงต้องใช้ใบปรับยอดสต๊อก" + `confirmReceive()` block | ✓ |
| FN-29 | `doShip()` ตรวจซ้ำ `if((+l.qty||0) > onHandOf(l.binFrom,l.item_code))` → toast แสดงยอดล่าสุด + ทางแก้ 2 ทาง | ✓ |
| FN-45 | คอลัมน์ **"คงค้างระหว่างทาง"** ในแผงรับ (สีส้ม) แสดงก่อนกดยืนยันเสมอ | ✓ |

### หมวด 5 · ★ ส่วนต่างระหว่างทาง
| FN | Evidence | ✓ |
|---|---|---|
| FN-24 | `<select onchange="setDiffAction(...)">` 3 ตัวเลือก `รอรับเพิ่ม (ยังไม่ถึง) / ของหาย-เสียหายระหว่างทาง / ตีกลับคืนต้นทาง` โผล่เมื่อ `diff>0` | ✓ |
| FN-25 | `confirmShortage()` ตรวจ 4 อย่าง: `!modalState.evidence.length` → block · `slots.some(!assignee)` → block · `slots.some(assignee===s.shippedBy)` → block ("ผู้ที่กดส่งออกจากต้นทางเซ็นอนุมัติการตัดส่วนต่างไม่ได้") · `setDiffReason()` บังคับเหตุผล | ✓ |
| FN-26 | `confirmShortage()` → `l.writtenOff+=w` → `s.status='closed_diff'` + audit "…FWD-WIRE: JE posting — ผลขาดทุนสินค้าระหว่างขนส่ง" + banner สีแดงใน detail tab | ✓ |
| FN-27 | `openReturnModal()` → เหตุผลบังคับ → `l.returned+=rem` · `s.status='returned'` · **ไม่เข้า `shortageAmount()`** (นับเฉพาะ `pendingWriteOff`) | ✓ |
| FN-41 | `isAging()` อ่าน `CFG.transitAgingDays` (ประกาศว่ามาจาก NC rules) → ป้ายส้ม "ค้างเกิน N วัน" ใน list + banner ใน detail + KPI การ์ดที่ 3 · mock `TRF-2026-0006` | ✓ |
| FN-46 | `renderTransitTab()` แสดงสมการ "จำนวนที่ส่งออก = รับแล้ว + ตัดหาย + ตีกลับ + ค้างระหว่างทาง" พร้อมตัวเลขจริงทุกคอลัมน์ · `lineRemaining()` เป็นสูตรเดียวที่คำนวณ | ✓ |

### หมวด 6 · อนุมัติ (DOA 2 จุดตัดสินใจ)
| FN | Evidence | ✓ |
|---|---|---|
| FN-30 | `renderSubmitModal()` → `.slot-row` ต่อขั้น + `combo('slot-'+i,…)` → `empChip()` (avatar + ตำแหน่ง + ชื่อ) · `confirmSubmit()` block ถ้ามี slot ว่าง · **ไม่มี role ID บนจอ** (`ROLE_LABEL` map เป็นชื่อไทย) | ✓ |
| FN-31 | `openRejectModal()` → `reasonModal()` เหตุผลบังคับ → `s.status='draft'` · เลขที่เดิมคงอยู่ (ไม่แตะ `s.code`) | ✓ |
| FN-42 | `renderStep5()` การ์ด "สายอนุมัติที่ทะเบียนกลางกำหนด" แสดง `res.why[0]` = "ฐาน = มูลค่ารวมที่ย้าย ฿X · มิติ = …" + `renderLineSummary()` บรรทัดท้าย "หน้านี้ไม่ตัดสินชั้นเอง" · `resolveDoa()` เป็น stub ที่ mark `FWD-WIRE: DOA engine` | ✓ |
| FN-47 | `renderSignTab()` แยก 2 section: "ลำดับการอนุมัติการย้าย" และ "ลำดับการอนุมัติการตัดส่วนต่างระหว่างทาง" (`s.shortage_chain`) · mock `TRF-2026-0004` มีครบ 2 กลุ่ม | ✓ |

### หมวด 7 · สถานะ · ยกเลิก · กลับรายการ
| FN | Evidence | ✓ |
|---|---|---|
| FN-32 | `openCancelModal()` guard `['draft','pending_approval','approved'].indexOf(s.status)===-1` → toast ชี้ทางอื่น · เหตุผลบังคับ · ใบยังอยู่ (`s.status='cancelled'`) | ✓ |
| FN-33 | `renderViewDrawer()` — ปุ่ม `ยกเลิก` มีเฉพาะ 3 สถานะแรก · สาขา `canReceive` ไม่มีปุ่มยกเลิกเลย | ✓ |
| FN-34 | `openReverseModal()` → สร้างใบใหม่ `mkDoc({reversalOf:s.code, whFrom:s.whTo, whTo:s.whFrom, lines:…binFrom↔binTo})` + `s.status='reversed'; s.reversedBy=rev.code` · mock คู่ `0010`/`0011` | ✓ |
| FN-35 | `if(s.reversedBy) return showToast('ใบนี้ถูกกลับรายการไปแล้ว — กลับรายการซ้ำไม่ได้')` + ปุ่มหายจาก header | ✓ |
| FN-36 | `openCreateDrawer(editId)` guard `s.status!=='draft'` → "แก้ไขได้เฉพาะฉบับร่าง" · view tab ทั้งหมด read-only · **ไม่มีปุ่มลบ movement ที่ใดเลย** (grep `ลบรายการเคลื่อนไหว` = 0) | ✓ |
| FN-37 | `KV('การลงบัญชี','<span class="pill draft">รอลงบัญชี</span>','FWD-WIRE: JE posting (W5)')` + audit note ทุก movement · **ไม่มีปุ่มลงบัญชี** | ✓ |
| FN-48 | `renderHistoryTab()` `.tl` จาก `s.audit[]` + note "รายการเคลื่อนไหว…แก้ไม่ได้ ลบไม่ได้" · `pushAudit()` append เท่านั้น | ✓ |

### หมวด 8 · กันงอก (scope creep = 0)
| FN | Evidence (grep ทั้งไฟล์) | ✓ |
|---|---|---|
| FN-38 | `"ยอดที่ถูกต้อง"` = **0** · `"จำนวนที่ปรับ"` = **0** · มี `.note` ใน step 3: "ถ้าต้องการ **แก้ยอดคงเหลือ** … ให้ใช้ **ใบปรับยอดสต๊อก** แทน" + microcopy ตอนรับเกิน | ✓ |
| FN-39 | `"ใบนับ"` = **0** · `"นับรอบ"` = **0** · `"count sheet"` = **0** · `"blind count"` = **0** | ✓ |
| FN-49 | ไม่มีฟังก์ชันสร้าง/แก้ bin — `BINS` เป็น const อ่านอย่างเดียว · ข้อความ S-30 ชี้ให้ผู้ดูแลผังไปตั้งค่า | ✓ |
| FN-50 | `"ค่าขนส่ง"` = **0** · `"tracking"` = 0 · `"pick list"` = 0 | ✓ |

### หมวด 9 · Landing
| FN | Evidence | ✓ |
|---|---|---|
| FN-43 | `kpi()` + `statCard()` 4 ใบ: ของที่อยู่ระหว่างทาง (฿354,400.00 · 2 ใบ) · ใบรออนุมัติ (2) · ค้างเกินเกณฑ์ (1) · รอฉันรับ + มูลค่าส่วนต่างที่ตัดเดือนนี้ — **คลิกแล้ว `setTab()` filter จริง** | ✓ |
| FN-51 | `tabBar()` 4 แท็บ รวม **"รอฉันรับ (ปลายทาง = คลังฉัน)"** (`d.whTo===ME.wh`) และ **"อยู่ระหว่างทาง"** | ✓ |
| FN-52 | `renderFilterBar()` — ค้นหา · คลังต้นทาง · คลังปลายทาง · **โหมด** · สถานะ (11 ค่า) · ล้างตัวกรอง | ✓ |
| FN-53 | `renderDetailTab()` `SEC('paperclip', เอกสารแนบ (N ไฟล์ · Document Center))` เป็น section ใน landing tab | ✓ |
| FN-54 | `renderPdfTab()` `.a4` — เลขที่ · **แถบเส้นทาง + ชิปโหมด** · ตารางบรรทัด (มีคอลัมน์ "รับจริง" เมื่อข้ามคลัง) · totals · ช่องเซ็น **4 ช่องรวมผู้รับปลายทาง** | ✓ |

### หมวด 10 · ทั่วไป
| FN | Evidence | ✓ |
|---|---|---|
| FN-90 | `renderTableHtml()` empty state 2 เคส + ปุ่ม action | ✓ |
| FN-91 | destructive ทุกตัวผ่าน `reasonModal()`/`window.confirm()` + ปุ่มสี danger (ตัดส่วนต่าง · ยกเลิก · กลับรายการ · ตีกลับ) | ✓ |
| FN-92 | ทุก master ใช้ `combo()` ไม่ FK validate · `l.item_name` เก็บข้อความ ณ เวลาที่เลือก → ใบไม่พังเมื่อ master หลุด | ✓ |
| FN-93 | `confirmSubmit/confirmApprove/confirmReceive/confirmShortage` → `btn.disabled=true` + `loader-2 spin` ก่อนทำงาน | ✓ |
| FN-94 | `pushAudit()` เรียกใน 12 จุด (สร้าง/แก้/ส่ง/อนุมัติ/ตีกลับ/ส่งออก/รับ/ตัดส่วนต่าง/ตีกลับคืนต้นทาง/ยกเลิก/กลับรายการ) — append เท่านั้น | ✓ |
| FN-95 | `fdate()/fdt()` ใช้ `d.getFullYear()` → **ค.ศ. ล้วน** ทั้งจอและ PDF (ตรวจภาพ `_shots/01_list.png` = "9 ก.ย. 2026") | ✓ |
| FN-96 | CI tokens + sidebar Warehouse ชุดเดียวกับ GRN/Putaway/StockAdj (F008/F009/F079/F081/F082/**F083**/F040/F042) — ไม่ invent เมนู | ✓ |

---

## 2. Scenario coverage (34) — เน้น exception path ต้องมี "ทางเข้า" จริง

| S | ทางเข้าใน UI | ✓ |
|---|---|---|
| S-01 ข้ามสาขา ส่งครบ/รับครบ | ปุ่มส่งออก → แท็บ "รอฉันรับ" → ปุ่มยืนยันรับ · mock `0001` | ✓ |
| S-02 ภายในคลัง จังหวะเดียว | ปุ่ม "ย้ายสินค้า" · mock `0002` | ✓ |
| S-03 ร่าง | `saveDraft()` · mock `d7` | ✓ |
| S-04 อนุมัติครบ | submit modal → approve modal · mock `0012` (2 ชั้น) `0013` (1 ชั้น) | ✓ |
| S-05 ตีกลับตอนอนุมัติ | ปุ่ม "ไม่อนุมัติ" · mock `0008` (audit มีรอบก่อน) | ✓ |
| **S-06 รับไม่ครบ (รอรับเพิ่ม)** | แผงรับ → `รอรับเพิ่ม` · mock `0003` | ✓ |
| **S-07 ของหาย → ตัดส่วนต่าง** | แผงรับ → `ของหาย/เสียหาย` → `openShortageModal()` (หลักฐาน + DOA จุด 2) · mock `0004` | ✓ |
| **S-08 ตีกลับคืนต้นทาง** | ปุ่ม "ตีกลับคืนต้นทาง" ใน header · mock `0005` | ✓ |
| S-09 ค้างนานเกินเกณฑ์ | ป้ายส้ม + KPI · mock `0006` (ค้าง 16 วัน) | ✓ |
| S-10 ย้ายเกินยอดคงเหลือ | inline แดง + hard-warn + ปุ่มส่ง disabled | ✓ |
| S-11 จำนวน 0/ติดลบ | `wizardNext()` block | ✓ |
| **S-12 รับเกินที่ส่ง** | inline แดง + `confirmReceive()` block + ชี้ไป StockAdj | ✓ |
| S-13 ยกเลิกก่อนส่ง | ปุ่มยกเลิก · mock `0009` | ✓ |
| S-14 ยกเลิกระหว่างทาง (ไม่รองรับ) | **ปุ่มไม่มี** + guard ใน `openCancelModal()` | ✓ |
| S-15 กลับรายการ | ปุ่มกลับรายการ · mock `0010`/`0011` | ✓ |
| S-16 แก้บรรทัดหลังส่ง (ไม่รองรับ) | guard `openCreateDrawer(editId)` + ตาราง read-only | ✓ |
| S-17 quarantine → quarantine | picker กรอง + toast · mock `0013` | ✓ |
| S-18 damage (ไม่รองรับ) | `DM-01` ไม่โผล่ใน picker | ✓ |
| S-19 staging เป็นต้นทาง (บล็อก) | `ST-*` ไม่โผล่ใน picker | ✓ |
| S-20 ผู้ใช้เลือก in-transit เอง | `TR-*` ไม่โผล่ทั้ง 2 picker | ✓ |
| S-21 bin ล็อก | option `disabled` + เหตุผล (`B-03-02-B`) | ✓ |
| S-22 bin ต้นทาง = ปลายทาง | inline + block | ✓ |
| S-23 เปลี่ยนคลังตอนมีบรรทัด | `window.confirm` + เตือนโหมดเปลี่ยน | ✓ |
| S-24 หลายคู่คลังในใบเดียว (ไม่รองรับ) | ไม่มี field คลังระดับบรรทัด | ✓ |
| S-25 ผลบัญชี mock | pill `รอลงบัญชี` + `FWD-WIRE: JE posting` | ✓ |
| **S-26 ปรับยอด (ไม่รองรับ)** | `.note` ชี้ไป StockAdj + grep = 0 | ✓ |
| **S-27 นับสต๊อก (ไม่รองรับ)** | grep = 0 ทุกคำ | ✓ |
| S-28 ยอดต้นทางเปลี่ยนระหว่างรออนุมัติ | `doShip()` ตรวจซ้ำ + toast 2 ยอด + ทางแก้ | ✓ |
| S-29 master หลุด | เก็บ `item_name` ในบรรทัด · picker ไม่ FK | ✓ |
| S-30 ไม่มี in-transit bin ของคู่คลัง | block ที่ `wizardNext()` + `openSubmitModal()` + แถบแดง | ✓ |
| S-31 ผู้ใช้ไม่ใช่คลังปลายทาง | ปุ่มยืนยันรับ `disabled` + tooltip (ภาพ `_shots/03_view_transit.png`) | ✓ |
| S-32 double submit | `btn.disabled` + loader ทุกจุด | ✓ |
| S-33 list ว่าง / ค้นไม่เจอ | empty state 2 เคส | ✓ |
| S-34 Lot/HU/RF/ขนส่ง (ไม่รองรับ) | grep = 0 · มี `.scanbox` เผื่อช่องยิงรหัส | ✓ |

## 3. Transition coverage (§5.1 · 15 เส้น)

`ร่าง→รออนุมัติ` ✓ `รออนุมัติ→รออนุมัติ(ชั้นถัดไป)` ✓ `รออนุมัติ→อนุมัติแล้ว` ✓ `รออนุมัติ→ร่าง` ✓
`อนุมัติแล้ว→ย้ายสำเร็จ` ✓ `อนุมัติแล้ว→ส่งออกแล้ว` ✓ `ส่งออกแล้ว→รับบางส่วน` ✓ `→ปิดใบ (รับครบ)` ✓
`→ปิดใบพร้อมส่วนต่าง` ✓ `→ตีกลับคืนต้นทางแล้ว` ✓ `ร่าง/รออนุมัติ/อนุมัติแล้ว→ยกเลิก` ✓
`ส่งออกแล้ว→ยกเลิก` = **บล็อกจริง** ✓ `ใบปิด→กลับรายการแล้ว` ✓ `กลับรายการแล้ว` ปลายทางสุดท้าย ✓ `ยกเลิก/ตีกลับ` ปลายทางสุดท้าย ✓

## 4. Declaration coverage (chip vs detect)

| chip | detect ใน HTML | evidence | ผล |
|---|---|---|---|
| **doa** | ✅ | `.slot-row` picker คนจริง 2 จุดตัดสินใจ · `resolveDoa()` / `resolveShortageDoa()` อ่านจาก `MOCK_DOA_ENTRY` (รูปของ entry ที่ resolve มา) · **ไม่มี array ชื่อ role hardcode ในโค้ด feature** | ตรง |
| **ntf** | ✅ | marker `FWD-WIRE: ENG-NOTIFY` ที่จุดส่งออก + ส่งอนุมัติ · ไม่มี logic เลือกช่องทางในหน้า | ตรง |
| **csq** | ✅ | event ที่ประกาศ (`ส่งออก / รับ / ตัดส่วนต่าง / ตีกลับ / กลับรายการ`) มีจุดเกิดจริงในโค้ดครบ · ไม่มีการคำนวณผลกระทบเองในหน้า | ตรง |
| **doccfg** | ✅ | `nextCode()` ผลิต `TRF-2026-NNNN` (ปี ค.ศ.) ตอน**ส่งอนุมัติเท่านั้น** + `FWD-WIRE: ENG-DOC-NUM` · ไม่มีช่องกรอกเลขเอง | ตรง |
| **pdfdoc** | ✅ | `renderPdfTab()` `.a4` ตรงโครง `print-spec-trf.md` (แถบเส้นทาง · ข้อความเตือนโหมด B · ช่องเซ็นที่ 4 · ข้อความ "ไม่ใช่เอกสารทางภาษี") | ตรง |

→ **DIVERGENCE = 0** (ไม่ต้องเขียน `_lane/DIVERGENCE.md`)

## 5. Pattern Q surface coverage

| surface | ผล | evidence |
|---|---|---|
| 1 List | ✅ | `.ph` + KPI + tab + filter + ตาราง (docPill + signProgress + ยอด) + footer + ⋮ menu |
| 2 Create/Edit wizard | ✅ | `.drawer-panel.wide` 1290 · 5 steps ชื่อล็อก · footer contract · validate ต่อ step |
| 3 View drawer | ✅ | 920 · header (code/pill/summary/action group/divider/4 icon) · 5 tabs · footer + 🔒 |
| 4 PDF + Sign + Modals | ✅ | `.a4` · `.tl` timeline + `empChip` · submit/approve/reject/cancel/reverse/return/receive/shortage = 8 modal |

## 6. Scope creep check — **0 รายการ**

| ตรวจ | ผล |
|---|---|
| ฟังก์ชันปรับยอด / แก้ยอดคงเหลือ | ไม่มี (คำว่า "ปรับยอด" ปรากฏ 3 ครั้ง: เมนู sidebar ชี้ F082 + microcopy ชี้ทาง 2 จุด) |
| ใบนับ / cycle count | ไม่มี (grep 0 ทุกคำ) |
| สร้าง/แก้ผัง location | ไม่มี |
| ค่าขนส่ง / ผู้ขนส่ง / tracking / pick list | ไม่มี |
| Lot / Serial / Pallet / HU | ไม่มี |
| ปุ่มลงบัญชีที่ทำงานจริง | ไม่มี (สถานะ `รอลงบัญชี` อย่างเดียว) |
| เขียน `damage` / `staging` / `in-transit` โดยผู้ใช้ | ไม่มี (picker กรองออกทั้งหมด) |

## 7. ของที่ยัง mock (ตามแผน — ไม่ใช่ gap)

| รายการ | marker | เจ้าของ |
|---|---|---|
| ลงบัญชีจริง | `FWD-WIRE: JE posting` (19 จุด) | W5 |
| ต้นทุนอ้างอิง/valuation | `FWD-WIRE: valuation engine` (3 จุด) | W5 |
| DOA engine จริง | `FWD-WIRE: DOA engine` (2 จุด) | F-DLG-001 |
| เลขรัน/สำเนาเอกสาร | `FWD-WIRE: ENG-DOC-NUM` (1 จุด) | F-DOCCFG |
| แจ้งเตือน | `FWD-WIRE: ENG-NOTIFY` (2 จุด) | F-NOTIFY |

**ไม่พบ literal `TODO` ในไฟล์** — ตรงตาม convention `_RUNNER_BRIEF §2.11` (audit.sh Rule #24 FAIL = 0) · HANDOFF ผูก `FWD-WIRE:` ↔ `TODO:` เป็นรายการเดียวกัน
