# AI Test Cases — ใบปรับยอดสต๊อก (Stock Adjustment · F082 / F-WH-STKADJ)

> ไฟล์นี้เขียนให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype แล้วรายงานผลกลับ.
> ทุก action ผูกกับ **ข้อความ/ป้ายที่เห็นบนจอ** (verbatim จาก HTML) + **route จริง (hash)** · ทุก Expected เช็คได้ด้วยตา.
> Microcopy ทั้งหมด Sync-Read จาก `F-WH-STKADJ.html` (source of truth) + `UI_BRIEF` + FRD `06_TESTS §6.10`.

---

## ⚠️ ข้อจำกัด prototype (อ่านก่อนรัน — กำหนด Setup ของหลายเคส)

- **ผู้ใช้ตายตัว 1 คน:** `ปวีณา สุขทวี` · ตำแหน่ง **หัวหน้าคลัง (WH_LEAD)** · WH-BKK-01 · EMP-1002 (มุมขวาบน). **สลับ role/login ไม่ได้** — เคส permission/SoD ที่ต้องเป็นคนอื่นให้ทำเท่าที่ UI เปิด (ปุ่มโผล่/ไม่โผล่, คนถูกกันออกจาก picker) และ mark `(ต้อง simulate)` เมื่อกดมือไม่ได้.
- **canActStep:** ปุ่ม *อนุมัติ/ตีกลับ* โผล่เฉพาะเมื่อ ใบมีขั้น pending **และ** ผู้ใช้ไม่ใช่ผู้ส่ง **และ** (assignee = ปวีณา หรือ role ของ slot = WH_LEAD). → ใบที่ **ปวีณาสร้าง+ส่งเอง อนุมัติเองไม่ได้** (SoD ระดับใบ).
- **SoD ใน slot picker:** รายชื่อผู้อนุมัติ **ตัด ปวีณา (ME) ออกเสมอ** — เลือกตัวเองเป็นผู้อนุมัติไม่ได้.
- **ไม่มี backend:** ทุกอย่างเป็น state ในหน่วยความจำ · refresh หน้าคืน seed เดิม (mock DOCS). ปิด drawer/รีเฟรชเพื่อรีเซ็ตสถานะเคส.
- **เลขที่เอกสาร** ออกจริงตอน "ส่งอนุมัติ" (mock `nextCode()` = `ADJ-2026-NNNN` เดินเลขต่อจาก seed).
- **FWD-WIRE chip** (`.demo-only`) แสดงใน prototype (เช่น "FWD-WIRE: JE posting") — เป็น demo marker, production ซ่อน. ในเทสถือเป็น "เห็นได้" บนจอ prototype.
- **วันนี้ (TODAY)** = 2026-09-16 (วันที่มีผลต้อง ≤ วันนี้).

---

## Meta

| หัวข้อ | ค่า |
|---|---|
| Feature ID | F-WH-STKADJ (fid F082) |
| ชื่อ | ใบปรับยอดสต๊อก (Stock Adjustment) |
| เวอร์ชัน | FRD 1.0 (2026-09-16) · HTML `F-WH-STKADJ.html` (`<title>` "ใบปรับยอดสต๊อก (Stock Adjustment) · CUBE 4.0") |
| App entry | เปิดไฟล์ `outputs/F-WH-STKADJ/F-WH-STKADJ.html` → default route `#/list` |
| Routes (hash) | `#/list` (default) · `#/create` · `#/edit/:id` (เฉพาะ draft) · `#/view/:id` (4 tabs) |
| Overlays | wizard drawer (5 steps) · view drawer (4 tabs) · modals: submit / approve / reject / cancel / reverse / post(+drift) |
| ที่มา | FRD Pack (00–07) · BRD `BRD_F-WH-STKADJ.md` · HTML (source of truth) · UI_BRIEF · FUNCTION_CHECKLIST (55 FN) · PREBRIEF |
| จำนวนเคส | 116 (จัดกลุ่ม 17 group) |

---

## Coverage

| group | ขอบเขต | เคส | ความสำคัญ |
|---|---|---|---|
| L — List / KPI / Filter / Document Center | TC-L01..L09 | 9 | สูง |
| W1 — Wizard Step 1 (ข้อมูลใบปรับยอด) | TC-W101..W108 | 8 | สูง |
| W2 — Step 2 (line editor B2 v2) | TC-W201..W214 | 14 | สูง |
| W3 — Step 3 (เหตุผล + หลักฐาน) | TC-W301..W307 | 7 | สูง |
| W4 — Step 4 (ผู้อนุมัติ DOA) | TC-W401..W406 | 6 | สูง |
| W5 — Step 5 (ตรวจทาน + ร่าง/ส่ง) | TC-W501..W504 | 4 | สูง |
| V — View drawer (detail / count-doc / soft-ref) | TC-V01..V06 | 6 | กลาง |
| AP — Approve / Reject | TC-AP01..AP05 | 5 | สูง |
| PO — Post + drift (BR-15) | TC-PO01..PO05 | 5 | สูง |
| CX — Cancel (BR-27 / FIX-02) | TC-CX01..CX03 | 3 | สูง |
| RV — Reverse (FIX-03) | TC-RV01..RV04 | 4 | สูง |
| PD — PDF / Sign tabs | TC-PD01..PD04 | 4 | กลาง |
| HS — History / movement append-only | TC-HS01..HS03 | 3 | กลาง |
| NG — Negative "พิสูจน์ว่าไม่มี" (หมวด 7) | TC-NG01..NG10 | 10 | สูง |
| GN — General / edge / permission | TC-GN01..GN08 | 8 | กลาง |
| XT — Cross-module (§6.9) | TC-XT01..XT11 | 11 | กลาง |
| SL — Scope Lock verify (LOCK-01..10) | TC-SL01..SL10 | 10 | กลาง |

---

## Coverage Ledger

### FN (FUNCTION_CHECKLIST · 55 FN)
| FN | ย่อ | cases |
|---|---|---|
| FN-01 | ปรับกักกัน→picker QA-* | TC-W203, TC-W205 |
| FN-02 | ตัดจำหน่าย→picker DM-* | TC-W206 |
| FN-03 | bin ล็อก disabled+เหตุผล | TC-W207 |
| FN-04 | ผลต่าง + ชิปเขียว | TC-W201 |
| FN-05 | ผลต่าง − ชิปแดง | TC-W202 |
| FN-06 | มูลค่า = ผลต่าง×ต้นทุน | TC-W201, TC-W204 |
| FN-07 | สลับโหมดกรอก | TC-W208 |
| FN-08 | totals Σabs vs สุทธิ | TC-W209 |
| FN-09 | เปลี่ยนคลัง→confirm ล้างบรรทัด | TC-W105 |
| FN-10 | คู่ (bin,สินค้า) ซ้ำ | TC-W210 |
| FN-11 | ผลต่าง=0 บล็อก | TC-W211 |
| FN-12 | ปรับลดติดลบ บล็อก | TC-W212 |
| FN-13 | ป้ายต้นทุน mock | TC-W213 |
| FN-14 | Σabs + ชั้นที่ step4 | TC-W401 |
| FN-15 | มูลค่าต่ำ 1 ชั้น | TC-W402 |
| FN-16 | มูลค่าสูง หลายชั้น | TC-W403 |
| FN-17 | ทุก slot คนจริง (บล็อกถ้าว่าง) | TC-W404, TC-W503 |
| FN-18 | บรรทัดไม่มีเหตุผล ส่งไม่ได้ | TC-W301 |
| FN-19 | บันทึกร่าง ไม่มีเลขจริง | TC-W501 |
| FN-20 | ส่งอนุมัติ→ออกเลข ADJ-YYYY-NNNN | TC-W502 |
| FN-21 | อนุมัติ→slot ถัดไป/ครบ | TC-AP01, TC-AP02 |
| FN-22 | ตีกลับ+เหตุผล→ร่าง | TC-AP03, TC-AP04 |
| FN-23 | ผ่านรายการเฉพาะ approved | TC-PO01, TC-PO02 |
| FN-24 | ยกเลิกเฉพาะ ร่าง/รออนุมัติ ★ | TC-CX01, TC-CX02, TC-CX03 |
| FN-25 | posted ไม่มียกเลิก มีแต่กลับรายการ | TC-RV01 |
| FN-26 | list กรองครบทุกสถานะ | TC-L02 |
| FN-27 | ยอดเปลี่ยน→เตือน 2 ยอด ★ | TC-PO03, TC-PO04 |
| FN-28 | tab ลายเซ็น การ์ดผู้อนุมัติจริง | TC-PD03 |
| FN-29 | tab ประวัติ movement + คู่ reversal | TC-HS01, TC-HS02 |
| FN-30 | ป้ายรอลงบัญชี + JE marker (ไม่มีปุ่มจริง) | TC-V04, TC-HS01 |
| FN-31 | สินค้า archive ยังแสดงข้อความเดิม | TC-V05 |
| FN-32 | in-transit ไม่เจอ picker (neg) | TC-NG01 |
| FN-33 | แนบไฟล์→เอกสารแนบ landing | TC-W305, TC-L08 |
| FN-34 | tab PDF A4 + พิมพ์ | TC-PD01, TC-PD02 |
| FN-35 | ไม่มีนับสต๊อก (neg) | TC-NG02 |
| FN-36 | ไม่มี bin ปลายทาง/ย้าย (neg) | TC-NG03 |
| FN-37 | dropdown เหตุผลกรองตามทิศ | TC-W302 |
| FN-38 | ปี ค.ศ. ทุกจุด | TC-GN01 |
| FN-39 | audit append-only ทุก event | TC-HS03 |
| FN-40 | เหตุผล "อื่น ๆ" บังคับคำอธิบาย | TC-W303 |
| FN-41 | เหตุผลรวมของใบ เติมบรรทัดว่าง | TC-W304 |
| FN-42 | ไม่ใช้ role ID แทนคน | TC-W405 |
| FN-43 | ใบผสมสุทธิ≈0 ยังต้องอนุมัติตาม abs | TC-W406 |
| FN-44 | กลับรายการซ้ำไม่ได้ | TC-RV03 |
| FN-45 | ไม่มีปุ่มลบ/แก้ movement (neg) | TC-NG08 |
| FN-46 | quarantine ปรับได้ ย้ายออกไม่ได้ | TC-NG04 |
| FN-47 | ไม่มีช่องเลขเอง/ตั้งเลขรัน (neg) | TC-NG05 |
| FN-48 | ไม่มีช่อง threshold/% (neg) | TC-NG06 |
| FN-49 | ไม่มีคอลัมน์ VAT (neg) | TC-NG07 |
| FN-50 | sidebar module map | TC-NG09 |
| FN-51 | damage บังคับแนบหลักฐาน | TC-W306 |
| FN-52 | count-doc trace ★ | TC-W107, TC-V02 |
| FN-90 | ค้นหา/filter + empty state | TC-L03, TC-L04 |
| FN-91 | ยกเลิก/กลับรายการผ่าน confirm · ไม่มี hard delete | TC-GN05 |
| FN-92 | field validate + กัน double-submit | TC-W504, TC-GN06 |

**FN cross-check: ✅ 55/55** (ทุก FN มี ≥1 TC · หมวด 7 negative = พิสูจน์ "ไม่มี" ที่ TC-NG01..NG09)

### Business Rules (05_RULES §5.1 · BR-01..BR-27)
| BR | cases |
|---|---|
| BR-01 คู่ซ้ำ | TC-W210 |
| BR-02 ผลต่าง≠0 | TC-W211 |
| BR-03 ยอดหลังปรับ≥0 | TC-W212 |
| BR-04 1 ใบ 1 คลัง | TC-W105 |
| BR-05 ห้ามย้าย location (neg) | TC-NG03 |
| BR-06 เหตุผลบังคับ + note | TC-W301, TC-W303 |
| BR-07 เหตุผลตรงทิศ | TC-W302, TC-W307 |
| BR-08 ต้องอนุมัติก่อน post | TC-PO02 |
| BR-09 ฐาน DOA = Σ|abs| | TC-W209, TC-W406 |
| BR-10 slot คนจริง | TC-W404, TC-W503 |
| BR-11 ตีกลับมีเหตุผล | TC-AP04 |
| BR-12 ประเภทคุมชนิด bin | TC-W205, TC-W206, TC-NG04 |
| BR-13 in-transit ไม่โผล่ | TC-NG01 |
| BR-14 bin ล็อก disabled | TC-W207 |
| BR-15 ตรวจยอดซ้ำก่อน post | TC-PO03, TC-PO04 |
| BR-16 movement append-only | TC-NG08, TC-HS01 |
| BR-17 ยกเลิก posted = reversal ผ่าน DOA | TC-RV01, TC-RV02 |
| BR-17.1 ต้นฉบับ→reversed เมื่อใบกลับ post | TC-RV04 |
| BR-18 กลับรายการซ้ำไม่ได้ | TC-RV03 |
| BR-19 post ไม่ post JE จริง | TC-V04, TC-NG08 |
| BR-20 threshold ไม่อยู่ feature | TC-NG06 |
| BR-21 เลขออกตอนส่ง | TC-W501, TC-W502 |
| BR-22 soft-ref archive | TC-V05 |
| BR-23 damage บังคับแนบ | TC-W306 |
| BR-24 ไม่มีนับสต๊อก | TC-NG02 |
| BR-25 audit append-only | TC-HS03 |
| BR-26 count-doc บังคับ | TC-W106, TC-W107 |
| BR-27 ยกเลิกเฉพาะ ร่าง/รออนุมัติ | TC-CX01, TC-CX02, TC-CX03 |

### Field Validation (05_RULES §5.4 · VR-01..VR-15)
| VR | cases |
|---|---|
| VR-01 warehouse required | TC-W101 |
| VR-02 effective_date required ≤วันนี้ | TC-W102 |
| VR-03 adjustment_type required | TC-W103 |
| VR-04 source enum default ปรับตรง | TC-W104 |
| VR-05 ref_count_doc required iff count | TC-W106 |
| VR-06 bin required + filter | TC-W205 |
| VR-07 item required | TC-W214 |
| VR-08 correct_qty ≠ system | TC-W211 |
| VR-09 adjust_qty ≥0 after | TC-W212 |
| VR-10 reason required + direction | TC-W301, TC-W302 |
| VR-11 reason_note when RS-99 | TC-W303 |
| VR-12 all slots person | TC-W404 |
| VR-13 attachment ≥1 damage | TC-W306 |
| VR-14 reject/cancel/reverse reason | TC-AP04, TC-CX03, TC-RV02 |
| VR-15 (bin,item) unique | TC-W210 |

### Edge Cases (05_RULES §5.5 · EC-01..EC-07)
| EC | cases / สถานะ |
|---|---|
| EC-01 concurrent approval (409) | TC-GN07 — `(ต้อง simulate)` API stress; UI single-user → mark BLOCKED ถ้าทำไม่ได้ |
| EC-02 idempotency / double-submit | TC-GN06 (กันกดรัว ปุ่ม disable ระหว่างส่ง) |
| EC-03 permission revoked mid-flight | TC-GN08 — `(ต้อง simulate)` re-check role ตอน mutation (ไม่มี UI ถอดสิทธิ์ใน prototype → BLOCKED) |
| EC-04 ยอดเปลี่ยนก่อน post (BR-15) | TC-PO03, TC-PO04 |
| EC-05 draft resume | TC-W501 (ร่าง persist เป็น record จริง ไม่มีเลข) |
| EC-06 reversal เป็น compensation | TC-RV01, TC-RV02 |
| EC-07 item archive soft-ref | TC-V05 |

### Error Catalog (05_RULES §5.6) — ที่สังเกตบน UI ได้
| error (โยงข้อความจอ) | cases |
|---|---|
| ERR_DUPLICATE_BIN_ITEM (BR-01) | TC-W210 |
| ERR_ZERO_DELTA (BR-02) | TC-W211 |
| ERR_NEGATIVE_STOCK (BR-03) | TC-W212 |
| ERR_REASON_REQUIRED (BR-06) | TC-W301 |
| ERR_REASON_DIRECTION_MISMATCH (BR-07) | TC-W307 |
| ERR_REASON_NOTE_REQUIRED (BR-06) | TC-W303 |
| ERR_APPROVER_SLOT_EMPTY (BR-10) | TC-W404, TC-W503 |
| ERR_EVIDENCE_REQUIRED (BR-23) | TC-W306 |
| ERR_COUNT_DOC_REQUIRED (BR-26) | TC-W106, TC-W107 |
| ERR_BIN_LOCKED (BR-14) | TC-W207 (UI: disabled — กดไม่ได้) |
| ERR_INVALID_STATE_TRANSITION / post-before-approve (BR-08) | TC-PO02 |
| ERR_CANCEL_NOT_ALLOWED (BR-27) | TC-CX02, TC-RV01 |
| ERR_ALREADY_REVERSED (BR-18) | TC-RV03 |
| ERR_ACTION_REASON_REQUIRED (BR-11/17/27) | TC-AP04, TC-CX03, TC-RV02 |
| ERR_SOD_SELF_APPROVAL (SoD) | TC-W405, TC-AP05 |
| WARN_QTY_CHANGED (BR-15) | TC-PO03 |
| ERR_STALE_DATA (EC-01) | TC-GN07 `(simulate)` |
| ERR_PERMISSION_REVOKED (EC-03) | TC-GN08 `(simulate)` |
| ERR_VALIDATION_FAILED (generic required) | TC-W101 |

### Permission Matrix (05_RULES §5.3) — เท่าที่ UI single-user ตรวจได้
| cell | cases |
|---|---|
| หัวหน้าคลัง สร้าง/ส่งอนุมัติ = allow | TC-W502 |
| หัวหน้าคลัง ผ่านรายการ = allow | TC-PO01 |
| หัวหน้าคลัง กลับรายการ = allow | TC-RV02 |
| ผู้อนุมัติ อนุมัติเฉพาะ slot ตัวเอง (role/assignee ตรง) = allow | TC-AP01 |
| SoD ผู้จัดทำอนุมัติใบตัวเองไม่ได้ = deny | TC-AP05, TC-W405 |
| role อื่น (บัญชี/auditor) read-only | `(ต้อง simulate)` — ไม่มีใน prototype → ข้าม (ดู Audit) |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 post ใบ + → Inventory ledger | TC-XT01 |
| XT-02 post → GL/JE รอลงบัญชี | TC-XT02 |
| XT-03 post → ENG-NOTIFY adj_posted | TC-XT03 |
| XT-04 post damage → NOTIFY+CSQ writeoff | TC-XT04 |
| XT-05 post ใบผสม → 7C CSQ +/− | TC-XT05 |
| XT-06 กลับรายการ → ledger + CSQ reversed | TC-XT06 |
| XT-07 ยกเลิก → NOTIFY + no movement | TC-XT07 |
| XT-08 submit abs สูง → NOTIFY FYI | TC-XT08 |
| XT-09 submit → DOA resolve | TC-XT09 |
| XT-10 submit → ENG-DOC-NUM immutable | TC-XT10 |
| XT-11 อ้างใบนับ → Count Doc display-only | TC-XT11 |

### Scope Lock (07_LOCKED §7.0 · LOCK-01..10)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | Pattern Q 4 surface + B2 v2 | TC-SL01 |
| LOCK-02 | เหตุผลบังคับ + DOA ตามมูลค่า · no cycle count | TC-SL02 |
| LOCK-03 | +/− เท่านั้น · movement single-bin (ไม่มี from→to) | TC-SL03 |
| LOCK-04 | DOA slot คนจริง ห้าม role ID | TC-SL04 |
| LOCK-05 | เลข ADJ-YYYY-NNNN ออกตอนส่ง ห้าม format เอง | TC-SL05 |
| LOCK-06 | movement append-only · post แล้ว reversal เท่านั้น | TC-SL06 |
| LOCK-07 | location จาก Putaway · in-transit ห้ามแตะ | TC-SL07 |
| LOCK-08 | JE mock FWD-WIRE ห้าม post จริง | TC-SL08 |
| LOCK-09 | soft-ref nullable ไม่ FK | TC-SL09 |
| LOCK-10 | CI Warm Light · ปี ค.ศ. · sidebar module map | TC-SL10 |

### Cross-cutting / States / Events
| item | cases |
|---|---|
| list loading/loaded | TC-L01 |
| empty unfiltered "ยังไม่มีใบปรับยอด" | TC-L04 (obs) |
| empty filtered "ไม่พบรายการที่ค้นหา" | TC-L03 |
| KPI cross-filter | TC-L05 |
| refresh-safe deep link `#/view/:id` | TC-GN02 |
| Esc chain (combo→modal→drawer) | TC-GN03 |
| dirty-check ปิด wizard | TC-GN04 |
| event adj_posted / audit "บันทึกเข้า 7C" | TC-XT03, TC-XT05, TC-HS03 |

---

## Data Sets

### ผู้ใช้ (ตายตัว)
| field | ค่า |
|---|---|
| ผู้ใช้ปัจจุบัน | ปวีณา สุขทวี · หัวหน้าคลัง (WH_LEAD) · WH-BKK-01 · EMP-1002 |

### รายชื่อผู้อนุมัติที่เลือกได้ (EMPLOYEES · ปวีณาถูกกันออก = SoD)
| ชื่อ | ตำแหน่ง (role) | dept · code |
|---|---|---|
| สมชาย ใจดี | เจ้าหน้าที่คลัง (WH_STAFF) | คลัง WH-BKK-01 · EMP-1005 |
| อารีย์ พงษ์ทอง | เจ้าหน้าที่คลัง (WH_STAFF) | คลัง WH-BKK-01 · EMP-1008 |
| วิชัย มั่นคง | หัวหน้าคลัง (WH_LEAD) | คลัง WH-CNX-01 · EMP-1011 |
| สุนีย์ เจริญสุข | ผู้จัดการคลัง (WH_MGR) | ฝ่ายคลังสินค้า · EMP-2003 |
| ธนพล รัตนชัย | ผู้จัดการคลัง (WH_MGR) | ฝ่ายคลังสินค้า · EMP-2007 |
| กมลวรรณ ศรีทอง | ผู้จัดการบัญชี (FIN_MGR) | ฝ่ายบัญชีและการเงิน · EMP-3001 |
| ประเสริฐ วัฒนกุล | ผู้อำนวยการฝ่าย (DIR) | สายงานปฏิบัติการ · EMP-4001 |

### สินค้า (ITEMS · ต้นทุนอ้างอิง)
| code | ชื่อ | หน่วย | ต้นทุน |
|---|---|---|---|
| STA-0012 | ปากกาลูกลื่น น้ำเงิน 0.5 มม. | ด้าม | 6.50 |
| STA-0031 | กระดาษ A4 80 แกรม | รีม | 115.00 |
| STA-0044 | แฟ้มสันกว้าง 3 นิ้ว | เล่ม | 85.00 |

### bin (WH-BKK-01)
| code | โซน · ชนิด |
|---|---|
| A-01-01-A, A-01-02-C, A-02-01-C, A-02-03-B, B-01-01-A, B-02-01-A, C-01, C-02 | storage (ช่องเก็บปกติ) |
| B-03-02-B | storage · **ล็อก** ("ล็อกเพื่อตรวจซ่อมชั้นวาง") |
| ST-DOCK-01, ST-DOCK-02 | staging (พักรับเข้า) |
| QA-01 | quarantine (กักกัน) |
| DM-01 | damage (ของเสีย) |

### ประเภทการปรับ (คุมชนิด bin)
| ประเภท | bin ที่เลือกได้ | บังคับแนบ |
|---|---|---|
| ปรับยอดทั่วไป | storage, staging | ไม่ |
| ตัดจำหน่ายของเสีย | damage (DM-*) | **ใช่ (BR-23)** |
| ปรับยอดกักกัน | quarantine (QA-*) | ไม่ |

### เหตุผล (REASONS · ทิศ + ต้องอธิบายเพิ่ม)
| code | ชื่อ | ทิศ | ต้องอธิบาย |
|---|---|---|---|
| RS-01 | ของเจอเกินยอดระบบ | + (plus) | ไม่ |
| RS-02 | รับเข้าบันทึกขาด | + (plus) | ไม่ |
| RS-03 | ของสูญหาย | − (minus) | ใช่ |
| RS-04 | แตก/ชำรุดระหว่างจัดเก็บ | − (minus) | ไม่ |
| RS-05 | จ่ายออกบันทึกขาด | − (minus) | ไม่ |
| RS-06 | ตัดจำหน่าย/ทำลาย | − (minus) | ใช่ |
| RS-07 | ปรับยอดกักกันหลังตรวจซ้ำ | ± (both) | ใช่ |
| RS-99 | อื่น ๆ | ± (both) | ใช่ |

### ใบนับต้นเรื่อง (COUNT_DOCS · display-only)
| code | ที่มา |
|---|---|
| CNT-2026-0012 | F084 ตรวจนับใหญ่ |
| CYC-2026-0031 | F086 นับหมุนเวียน |
| CNT-2026-0018 | F084 ตรวจนับใหญ่ |

### เอกสาร seed (สำหรับเคสที่ต้องมีใบอยู่ก่อน)
| เลขที่ | สถานะ | หมายเหตุ (ใช้ในเคส) |
|---|---|---|
| ADJ-2026-0001 | ผ่านรายการ (posted) | general · reverse ได้ (ไม่ใช่ใบกลับ/ยังไม่ถูกกลับ) |
| ADJ-2026-0002 | ผ่านรายการ (posted) | general · reverse ได้ |
| ADJ-2026-0003 | รออนุมัติ (pending) | source=จากใบนับ CNT-2026-0012 · ผู้ส่ง สมชาย · **slot 1 = ปวีณา(ME) pending** → อนุมัติได้ · 2 ชั้น (slot2 = สุนีย์ WH_MGR) |
| ADJ-2026-0009 | รออนุมัติ (pending) | ประเภท ปรับยอดกักกัน · slot 1 = ปวีณา pending → อนุมัติได้ |
| ADJ-2026-0011 | อนุมัติแล้ว (approved) | general · **มี drift** (บรรทัด A-01-02-C ยอด ณ สร้าง 180 → ยอดล่าสุด 186) → ใช้ทดสอบ post drift |
| (ร่าง — ยังไม่ออกเลขที่) | ร่าง (draft) | general · ผู้สร้าง ปวีณา · note ว่าง → edit/cancel/submit |
| ADJ-2026-0005 | ร่าง (draft · returned) | general · banner "เคยถูกตีกลับ" |
| ADJ-2026-0006 | ยกเลิก (cancelled) | WH-CNX-01 · ดูอย่างเดียว |
| ADJ-2026-0007 | กลับรายการแล้ว (reversed) | reversedBy ADJ-2026-0008 → กลับรายการซ้ำไม่ได้ |
| ADJ-2026-0008 | ผ่านรายการ (posted · ใบกลับรายการของ 0007) | isReversal → ไม่มีปุ่มกลับรายการ |
| (ร่าง — ยังไม่ออกเลขที่) | ร่าง (draft · damage) | ประเภทตัดจำหน่ายของเสีย · note "ตัดจำหน่ายกระเบื้องแตก" → ทดสอบบังคับแนบ |

### ชุดกรอก wizard (ใช้ในเคสสร้าง)
| ชุด | ค่า |
|---|---|
| A (happy +) | คลัง=คลังกรุงเทพ (WH-BKK-01) · วันที่มีผล=2026-09-15 · ประเภท=ปรับยอดทั่วไป · แหล่งที่มา=ปรับตรง · บรรทัด1: bin=A-01-02-C · สินค้า=STA-0012 · ยอดที่ถูกต้อง=195 (ยอดระบบ 180 → +15 · มูลค่า +97.50) · เหตุผล=RS-01 |
| B (mixed +/−) | บรรทัด1: A-01-01-A · STA-0031 · ยอดที่ถูกต้อง=240 (ระบบ 200 → +40 · +4,600) เหตุผล RS-02 · บรรทัด2: A-02-03-B · STA-0044 · ยอดที่ถูกต้อง=75 (ระบบ 90 → −15 · −1,275) เหตุผล RS-04 |
| C (high value → 2 ชั้น) | บรรทัด: A-01-01-A · STA-0031 · ยอดที่ถูกต้อง=400 (ระบบ 200 → +200 · +23,000 ≥20,000) เหตุผล RS-02 |
| D (zero delta) | bin=A-01-02-C · STA-0012 · ยอดที่ถูกต้อง=180 (= ยอดระบบ → ผลต่าง 0) |
| E (negative) | bin=A-01-02-C · STA-0012 · โหมด "ระบุจำนวนที่ปรับ" · จำนวน=−999 (ติดลบเกินคงเหลือ) |
| F (damage) | ประเภท=ตัดจำหน่ายของเสีย · bin=DM-01 · สินค้า=STA-0044 · ยอดที่ถูกต้อง=0 (ระบบ>0) เหตุผล RS-06 + คำอธิบาย "ทำลายตามใบบันทึก" |

### ไฟล์ทดสอบ (Files)
| ชื่อไฟล์ | ใช้ที่ | หมายเหตุ |
|---|---|---|
| `evidence-damage-01.pdf` | TC-W305, TC-W306 | ไฟล์หลักฐานสำหรับแนบใน step 3 (ชนิดใดก็ได้ · runner เตรียมไฟล์จริงให้ file picker) |

---

## Test Cases

### กลุ่ม L — List / KPI / Filter / Document Center

#### TC-L01 — เปิด list เห็น KPI + ตาราง + Document Center (happy)
- group: List · ความสำคัญ: สูง · trace: FN-26, FN-90 / AC-01 · actor: หัวหน้าคลัง
- Setup: role=หัวหน้าคลัง(ME) · seed=ใบ seed 11 ใบ · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: เห็นหัวข้อ ตาราง KPI 4 การ์ด และการ์ดเอกสารแนบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | หัวข้อหน้า **"ใบปรับยอดสต๊อก"** + ปุ่ม **"สร้างใบปรับยอด"** มุมขวา · sidebar active "ใบปรับยอดสต๊อก" · breadcrumb "คลังสินค้า › ใบปรับยอดสต๊อก" | ☐ |
| 2 | VERIFY แถว KPI (4 การ์ด) | — | เห็น 4 การ์ด: **"ใบรออนุมัติ"**, **"ใบเกินเกณฑ์อายุ"** (meta "ตามเกณฑ์ NC rules"), **"มูลค่าปรับสะสมเดือนนี้"** (meta "จากใบที่ผ่านรายการ"), **"ใบที่กลับรายการ"** (meta "reversal (append-only)") | ☐ |
| 3 | VERIFY หัวตาราง | — | คอลัมน์: เลขที่ · คลัง · ประเภท · **มูลค่าปรับ (Σ\|฿\|)** · สถานะเอกสาร · ลายเซ็น · วันที่มีผล · ผู้จัดทำ · (⋮) | ☐ |
| 4 | VERIFY แถวข้อมูล + foot | — | มีหลายแถว (เช่น ADJ-2026-0001 ป้าย **ผ่านรายการ**) · foot ล่าง "แสดง N จาก N ใบ" + "ปี ค.ศ. · มูลค่าอ้างอิงจาก Item Master (mock)" | ☐ |
| 5 | VERIFY การ์ดเอกสารแนบ (Document Center) | — | มีการ์ด "เอกสารแนบ" ท้ายหน้า (landing) | ☐ |

#### TC-L02 — กรองสถานะครบทุกค่า (FN-26)
- group: List · ความสำคัญ: สูง · trace: FN-26 / AC-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบครบ 6 สถานะ · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: dropdown สถานะเลือกได้ครบ 6 ค่า และตารางกรองตาม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY dropdown "ทุกสถานะ" | — | มีตัวเลือก: ร่าง · รออนุมัติ · อนุมัติแล้ว · ผ่านรายการ · ยกเลิก · กลับรายการแล้ว (ครบ 6) | ☐ |
| 2 | SELECT "รออนุมัติ" → dropdown สถานะ | รออนุมัติ | ตารางเหลือเฉพาะแถวป้าย **รออนุมัติ** (เช่น ADJ-2026-0003, ADJ-2026-0009) | ☐ |
| 3 | SELECT "ผ่านรายการ" → dropdown สถานะ | ผ่านรายการ | ตารางเหลือเฉพาะป้าย **ผ่านรายการ** | ☐ |
| 4 | SELECT "กลับรายการแล้ว" → dropdown สถานะ | กลับรายการแล้ว | ตารางเหลือ ADJ-2026-0007 ป้าย **กลับรายการแล้ว** | ☐ |
| 5 | CLICK ปุ่ม **"ล้างตัวกรอง"** | — | ตารางกลับมาแสดงทุกแถว | ☐ |

#### TC-L03 — ค้นหาไม่เจอ → empty filtered (FN-90 · negative)
- group: List · ความสำคัญ: กลาง · trace: FN-90 / AC-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ZZZ-ไม่มีจริง" → ช่องค้นหา (placeholder "ค้นหา เลขที่ / สินค้า / bin / ผู้จัดทำ…") | ZZZ-ไม่มีจริง | ตารางว่าง แสดง empty: title **"ไม่พบรายการที่ค้นหา"** + desc **"ลองปรับคำค้นหรือล้างตัวกรอง"** | ☐ |
| 2 | CLICK ปุ่ม **"ล้างตัวกรอง"** | — | ตารางกลับมามีแถว | ☐ |

#### TC-L04 — ค้นหาเจอ + empty state ว่างเปล่า (FN-90)
- group: List · ความสำคัญ: กลาง · trace: FN-90 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "0003" → ช่องค้นหา | 0003 | ตารางเหลือแถว ADJ-2026-0003 (ค้นด้วยเลขที่ทำงาน) | ☐ |
| 2 | TYPE "ปากกา" → ช่องค้นหา (ล้างก่อน) | ปากกา | เหลือใบที่มีสินค้า STA-0012 (ค้นด้วยชื่อสินค้าทำงาน) | ☐ |
| 3 | VERIFY empty ว่างเปล่า | (อ้างอิง) เมื่อไม่มีใบเลย `(ต้อง simulate)` — seed มีใบเสมอ | title **"ยังไม่มีใบปรับยอด"** + desc **"เริ่มต้นด้วยการสร้างใบปรับยอดใบแรก"** — mark BLOCKED ถ้า seed ล้างไม่ได้ | ☐ |

#### TC-L05 — KPI คลิกเพื่อ cross-filter
- group: List · ความสำคัญ: กลาง · trace: FN-26 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=มีใบ pending ≥1 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด KPI **"ใบรออนุมัติ"** | — | การ์ดขึ้น state active (เน้นกรอบ) · ตารางเหลือเฉพาะใบ **รออนุมัติ** | ☐ |
| 2 | CLICK การ์ด **"ใบรออนุมัติ"** ซ้ำ | — | ปลด filter · ตารางกลับมาครบ | ☐ |
| 3 | CLICK การ์ด **"ใบที่กลับรายการ"** | — | ตารางเหลือใบสถานะ **กลับรายการแล้ว** (ADJ-2026-0007) | ☐ |

#### TC-L06 — คลิกแถวเปิด view drawer
- group: List · ความสำคัญ: สูง · trace: FN-26 / AC-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว ADJ-2026-0001 | — | route → `#/view/d1` · เปิด view drawer หัวข้อ **"ใบปรับยอดสต๊อก"** + เลขที่ **ADJ-2026-0001** + ป้าย **ผ่านรายการ** | ☐ |
| 2 | VERIFY 4 tabs | — | เห็น tab: **รายละเอียด** · **PDF Preview** · **ลายเซ็น / อนุมัติ** · **ประวัติ** | ☐ |
| 3 | CLICK ปุ่ม **ปิด** (มุมล่าง) | — | drawer ปิด · route กลับ `#/list` | ☐ |

#### TC-L07 — ปุ่มแถว ⋮ ไม่ทำให้เปิด view (click-through guard)
- group: List · ความสำคัญ: กลาง · trace: FN-26 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **⋮** ท้ายแถว ADJ-2026-0001 | — | เมนู row เปิดขึ้น (ลอยเหนือแถว) · **ไม่** เด้งเข้า view drawer | ☐ |
| 2 | VERIFY เมนู posted | — | มีรายการ "กลับรายการ" (ใบ posted ที่ยังไม่ถูกกลับ) · ไม่มี "ยกเลิก" | ☐ |
| 3 | PRESS Esc | — | เมนูปิด · ยังอยู่หน้า list | ☐ |

#### TC-L08 — เอกสารแนบโผล่ที่ Document Center landing (FN-33)
- group: List · ความสำคัญ: กลาง · trace: FN-33 / AC-26 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 (มีไฟล์แนบ "ใบตรวจนับ-Q3.pdf") · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY การ์ด "เอกสารแนบ" ท้ายหน้า | — | มีรายการไฟล์รวมจากใบต่าง ๆ (เช่น **ใบตรวจนับ-Q3.pdf** จาก ADJ-2026-0003) พร้อมผู้แนบ/วันที่ (ค.ศ.) | ☐ |

#### TC-L09 — กรองคลัง + ช่วงวันที่
- group: List · ความสำคัญ: ต่ำ · trace: FN-90 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบทั้ง WH-BKK-01 และ WH-CNX-01 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "คลังกรุงเทพ (WH-BKK-01)" → dropdown คลัง | WH-BKK-01 | ตารางเหลือใบคลัง BKK · ADJ-2026-0006 (WH-CNX-01) หาย | ☐ |
| 2 | TYPE ช่วงวันที่ "ตั้งแต่" = 2026-09-10 | 2026-09-10 | ตารางเหลือใบวันที่มีผล ≥ 2026-09-10 | ☐ |
| 3 | CLICK **"ล้างตัวกรอง"** | — | ตารางกลับมาครบ | ☐ |

### กลุ่ม W1 — Wizard Step 1 (ข้อมูลใบปรับยอด)

#### TC-W101 — บันทึกไม่ได้เมื่อไม่ครบ required (VR-01/03)
- group: Wizard S1 · ความสำคัญ: สูง · trace: VR-01, VR-03 / FN-92 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` | — | drawer wizard เปิด หัวข้อ **"สร้างใบปรับยอดสต๊อก"** · stepper 5 จุด · step 1 = **"ข้อมูลใบปรับยอด"** | ☐ |
| 2 | CLICK ปุ่ม **"ถัดไป"** (โดยยังไม่กรอกคลัง) | — | ไม่ไป step 2 · toast **"กรุณากรอกข้อมูลให้ครบถ้วน"** · ช่องคลัง/ประเภทติดกรอบ error | ☐ |

#### TC-W102 — วันที่มีผลห้ามอนาคต (VR-02 · boundary)
- group: Wizard S1 · ความสำคัญ: กลาง · trace: VR-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT คลัง = คลังกรุงเทพ (WH-BKK-01) | — | ช่องคลังแสดงค่าที่เลือก | ☐ |
| 2 | TYPE วันที่มีผล = 2026-12-31 (อนาคต) → ช่อง "วันที่มีผล" | 2026-12-31 | CLICK "ถัดไป" → ไม่ไปต่อ · toast **"กรุณากรอกข้อมูลให้ครบถ้วน"** · ช่องวันที่ติด error (>วันนี้) | ☐ |
| 3 | TYPE วันที่มีผล = 2026-09-15 (อดีต/วันนี้) | 2026-09-15 | ช่องวันที่ไม่ติด error | ☐ |

#### TC-W103 — ประเภทการปรับ required enum (VR-03)
- group: Wizard S1 · ความสำคัญ: กลาง · trace: VR-03 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY dropdown ประเภทการปรับ | — | มี 3 ค่า: **ปรับยอดทั่วไป · ตัดจำหน่ายของเสีย · ปรับยอดกักกัน** | ☐ |
| 2 | SELECT "ตัดจำหน่ายของเสีย" | — | field-help ใต้ช่องเปลี่ยนเป็น **"bin ของเสีย (DM-*) · บังคับแนบหลักฐาน"** | ☐ |
| 3 | SELECT "ปรับยอดกักกัน" | — | field-help เปลี่ยนเป็น **"bin กักกัน (QA-*) · ปรับในบิ๊นเดิม"** | ☐ |

#### TC-W104 — แหล่งที่มา default ปรับตรง (VR-04)
- group: Wizard S1 · ความสำคัญ: กลาง · trace: VR-04, FN-52 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY segmented "แหล่งที่มา" | — | มี 2 ปุ่ม **ปรับตรง** / **จากใบนับ** · **ปรับตรง** ถูกเลือก (on) เป็น default · ไม่มีช่องเลือกใบนับ | ☐ |
| 2 | VERIFY field-help | — | ข้อความ "\"ปรับตรง\" = ปรับยอดเอง · \"จากใบนับ\" = อ้างอิงใบนับต้นเรื่อง (F084/F086) แบบแสดงผล — ไม่เปิด/ไม่สร้างหน้าจอใบนับ" | ☐ |

#### TC-W105 — เปลี่ยนคลังตอนมีบรรทัด → confirm ล้าง (FN-09 · BR-04)
- group: Wizard S1 · ความสำคัญ: สูง · trace: FN-09 / BR-04 / AC-25 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT คลัง=คลังกรุงเทพ · วันที่=2026-09-15 · ประเภท=ปรับยอดทั่วไป → CLICK "ถัดไป" | ชุด A (หัว) | เข้า step 2 | ☐ |
| 2 | CLICK ช่อง bin บรรทัดแรก → เลือก **A-01-02-C** | A-01-02-C | บรรทัดมี bin | ☐ |
| 3 | CLICK "กลับ" ไป step 1 → เปลี่ยนคลังเป็นคลังอื่น (พิมพ์ในช่องคลัง แล้วเลือกใบใหม่) | คลังอื่น | modal confirm หัวข้อ **"เปลี่ยนคลัง"** + body "จะล้าง bin ในรายการที่เลือกไว้ ต่อหรือไม่?" + ปุ่ม **"ล้างและเปลี่ยน"** (danger) | ☐ |
| 4 | CLICK **"ล้างและเปลี่ยน"** | — | modal ปิด · คลังเปลี่ยน · กลับไป step 2 บรรทัด bin ถูกล้าง | ☐ |

#### TC-W106 — source=จากใบนับ ไม่เลือกใบนับ → ส่งไม่ได้ (BR-26 · VR-05)
- group: Wizard S1 · ความสำคัญ: สูง · trace: FN-52 / BR-26 / VR-05 / AC-24 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT คลัง=คลังกรุงเทพ · วันที่=2026-09-15 · ประเภท=ปรับยอดทั่วไป | — | หัวใบครบ | ☐ |
| 2 | CLICK segmented **"จากใบนับ"** | — | โผล่ช่องเลือกใบนับ (placeholder "เลือกใบนับต้นเรื่อง (CNT/CYC · F084/F086)…") | ☐ |
| 3 | CLICK ปุ่ม **"ถัดไป"** (ยังไม่เลือกใบนับ) | — | ไม่ไปต่อ · toast **"เลือกใบนับต้นเรื่อง (F084/F086) ก่อน (BR-26)"** · ช่องแหล่งที่มาติด error | ☐ |

#### TC-W107 — source=จากใบนับ เลือกใบนับ → ผ่าน (FN-52)
- group: Wizard S1 · ความสำคัญ: สูง · trace: FN-52 / BR-26 / AC-24 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT หัวใบครบ + CLICK "จากใบนับ" | — | ช่องเลือกใบนับปรากฏ | ☐ |
| 2 | CLICK ช่องเลือกใบนับ → เลือก **CNT-2026-0012** | CNT-2026-0012 | ช่องแสดง "CNT-2026-0012 · F084 ตรวจนับใหญ่" | ☐ |
| 3 | CLICK **"ถัดไป"** | — | ไปที่ step 2 ได้ (ไม่มี toast บล็อก) | ☐ |

#### TC-W108 — เลขที่เอกสารเป็น disabled placeholder (BR-21 · FN-47)
- group: Wizard S1 · ความสำคัญ: กลาง · trace: FN-19, FN-47 / BR-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "เลขที่เอกสาร" | — | ช่อง **disabled** แสดง **"(ร่าง — ยังไม่ออกเลขที่)"** + field-help "ออกเลขอัตโนมัติเมื่อส่งอนุมัติ" · แก้ไม่ได้ (พิสูจน์ FN-47) | ☐ |

### กลุ่ม W2 — Wizard Step 2 (line editor B2 v2)

> ก่อนทุกเคส W2: OPEN `#/create` → SELECT คลัง=คลังกรุงเทพ · วันที่=2026-09-15 · ประเภท=ปรับยอดทั่วไป → CLICK "ถัดไป" เข้า step **"รายการปรับยอด"**.

#### TC-W201 — ผลต่าง + ชิปเขียว + มูลค่าถูกต้อง (FN-04, FN-06 · happy)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-04, FN-06 / AC-03 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ยอดระบบ bin A-01-02-C × STA-0012 = 180 · files=—
- Start: OPEN `#/create` → step 2
- ผ่านเมื่อ: ยอดระบบขึ้นเอง 180 · ผลต่าง +15 ชิปเขียว · มูลค่า +97.50

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin บรรทัดแรก → เลือก **A-01-02-C** | A-01-02-C | บรรทัดมี bin + meta โซน/คลังใต้ช่อง | ☐ |
| 2 | CLICK ช่องสินค้า → เลือก **STA-0012** (ปากกาลูกลื่น น้ำเงิน 0.5 มม.) | STA-0012 | ช่อง **ยอดระบบ** ขึ้นเป็น **180** อัตโนมัติ · หน่วย "ด้าม" · ต้นทุน 6.50 | ☐ |
| 3 | TYPE "195" → ช่อง **ยอดที่ถูกต้อง** | 195 | ช่อง **ผลต่าง** แสดง **+15** ชิป**เขียว** (มีเครื่องหมาย +) | ☐ |
| 4 | VERIFY ช่อง **มูลค่าที่ปรับ** | — | แสดง **+97.50** (15 × 6.50) ทิศเป็นบวก | ☐ |

#### TC-W202 — ผลต่าง − ชิปแดง (FN-05)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-05 / AC-03 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=A-02-03-B × STA-0044 = 90 · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK bin → **A-02-03-B** · CLICK สินค้า → **STA-0044** | A-02-03-B / STA-0044 | ยอดระบบขึ้น **90** · หน่วย "เล่ม" · ต้นทุน 85.00 | ☐ |
| 2 | TYPE "75" → ยอดที่ถูกต้อง | 75 | ผลต่าง **−15** ชิป**แดง** (มีเครื่องหมาย −) | ☐ |
| 3 | VERIFY มูลค่าที่ปรับ | — | แสดง **−1,275.00** (−15 × 85) | ☐ |

#### TC-W203 — bin picker เหลือเฉพาะประเภทที่เลือก (FN-01 · storage)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-01 / BR-12 / AC-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ประเภท=ปรับยอดทั่วไป · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin บรรทัดแรก (ไม่พิมพ์) | — | dropdown bin แสดงเฉพาะ storage/staging (A-*, B-*, C-*, ST-DOCK-*) · **ไม่มี** QA-01 หรือ DM-01 | ☐ |
| 2 | TYPE "QA" → ช่อง bin | QA | ไม่พบ QA-01 (นอกประเภท) · แสดง "ไม่พบ bin ที่ตรงประเภท/คลัง" | ☐ |

#### TC-W205 — ปรับยอดกักกัน → picker เหลือ QA-* (FN-01 · BR-12)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-01 / BR-12 / VR-06 / AC-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภท=**ปรับยอดกักกัน** → CLICK "ถัดไป" | — | เข้า step 2 | ☐ |
| 2 | CLICK ช่อง bin บรรทัดแรก | — | dropdown เหลือเฉพาะ **QA-01** (โซนกักกัน) · ไม่มี storage/damage | ☐ |

#### TC-W206 — ตัดจำหน่ายของเสีย → picker เหลือ DM-* (FN-02 · BR-12)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-02 / BR-12 / AC-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภท=**ตัดจำหน่ายของเสีย** → CLICK "ถัดไป" | — | เข้า step 2 | ☐ |
| 2 | CLICK ช่อง bin บรรทัดแรก | — | dropdown เหลือเฉพาะ **DM-01** (โซนของเสีย) | ☐ |

#### TC-W207 — bin ล็อก แสดงแต่เลือกไม่ได้ + เหตุผล (FN-03 · BR-14)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-03 / BR-14 / AC-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=bin B-03-02-B ล็อก ("ล็อกเพื่อตรวจซ่อมชั้นวาง") · files=—
- Start: OPEN `#/create` → step 2 (ประเภททั่วไป)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin → TYPE "B-03" | B-03 | รายการ **B-03-02-B** ปรากฏแต่ **disabled** (กดไม่ได้) · แสดงป้าย **ล็อก** + เหตุผล **"ล็อกเพื่อตรวจซ่อมชั้นวาง"** | ☐ |
| 2 | CLICK รายการ B-03-02-B | — | เลือกไม่ได้ (ไม่ถูกใส่ในบรรทัด) | ☐ |

#### TC-W208 — สลับโหมดกรอก แปลงค่ากลับไปมา (FN-07)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-07 / AC-04 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=A-01-02-C × STA-0012 = 180 · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก bin A-01-02-C + สินค้า STA-0012 · TYPE ยอดที่ถูกต้อง = 195 | 195 | ผลต่าง +15 (โหมด "ระบุยอดที่ถูกต้อง") | ☐ |
| 2 | CLICK segmented **"ระบุจำนวนที่ปรับ"** | — | คอลัมน์เปลี่ยนเป็นช่องจำนวนที่ปรับ · ค่าแสดง **+15** (แปลงจากยอดถูกต้อง 195 − ระบบ 180) | ☐ |
| 3 | CLICK segmented **"ระบุยอดที่ถูกต้อง"** กลับ | — | ช่องยอดที่ถูกต้องกลับเป็น **195** · ผลต่างยัง +15 | ☐ |

#### TC-W209 — totals Σ ค่าสัมบูรณ์ vs สุทธิ (FN-08 · BR-09)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-08 / BR-09 / AC-05 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ยอดระบบ A-01-01-A×STA-0031=200, A-02-03-B×STA-0044=90 · files=—
- Start: OPEN `#/create` → step 2 · ชุด B (mixed)
- ผ่านเมื่อ: footer แยก Σ ค่าสัมบูรณ์ (5,875) กับ สุทธิ (+3,325) ชัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | บรรทัด1: bin A-01-01-A · STA-0031 · ยอดที่ถูกต้อง=240 | +40 | ผลต่าง +40 · มูลค่า +4,600.00 (40×115) | ☐ |
| 2 | CLICK **"เพิ่มบรรทัด"** → บรรทัด2: bin A-02-03-B · STA-0044 · ยอดที่ถูกต้อง=75 | −15 | ผลต่าง −15 · มูลค่า −1,275.00 (15×85) | ☐ |
| 3 | VERIFY footer totals | — | **มูลค่าสุทธิ** = +3,325.00 (4,600−1,275) · **Σ มูลค่าค่าสัมบูรณ์ (ฐาน DOA)** = 5,875.00 (4,600+1,275) — แยกกันคนละบรรทัด | ☐ |

#### TC-W210 — คู่ (bin, สินค้า) ซ้ำ (FN-10 · BR-01 · negative)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-10 / BR-01 / VR-15 / AC-08 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | บรรทัด1: bin A-01-02-C · STA-0012 · ยอดที่ถูกต้อง=195 | — | บรรทัด1 ครบ | ☐ |
| 2 | CLICK "เพิ่มบรรทัด" → บรรทัด2: bin **A-01-02-C** · STA-0012 (คู่เดิม) · ยอดที่ถูกต้อง=170 | คู่ซ้ำ | บรรทัด2 กรอกได้ | ☐ |
| 3 | CLICK ปุ่ม **"ถัดไป"** | — | ไม่ไปต่อ · toast **"คู่ (bin, สินค้า) ซ้ำ: A-01-02-C · ปากกาลูกลื่น น้ำเงิน 0.5 มม. (BR-01)"** | ☐ |

#### TC-W211 — ผลต่าง = 0 บล็อก (FN-11 · BR-02 · negative)
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-11 / BR-02 / VR-08 / AC-06 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=A-01-02-C × STA-0012 = 180 · files=—
- Start: OPEN `#/create` → step 2 · ชุด D

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | bin A-01-02-C · STA-0012 · TYPE ยอดที่ถูกต้อง = **180** (= ยอดระบบ) | 180 | ผลต่างชิปแสดง **0** | ☐ |
| 2 | CLICK **"ถัดไป"** | — | ไม่ไปต่อ · toast **"บรรทัด A-01-02-C ผลต่าง = 0 — ให้ลบบรรทัดหรือแก้ยอด (BR-02)"** | ☐ |

#### TC-W212 — ปรับลดจนติดลบ บล็อก (FN-12 · BR-03 · negative) [AI-DEFAULT]
- group: Wizard S2 · ความสำคัญ: สูง · trace: FN-12 / BR-03 / VR-09 / AC-07 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=A-01-02-C × STA-0012 = 180 · files=—
- Start: OPEN `#/create` → step 2 · ชุด E
- หมายเหตุ: BR-03 tag `[AI-DRAFT][STD]` — เกณฑ์นี้ AI ร่างไว้; fail อาจแปลว่า default ผิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | bin A-01-02-C · STA-0012 · CLICK segmented "ระบุจำนวนที่ปรับ" · TYPE จำนวน = **−999** | −999 | ช่องจำนวนแสดง −999 · ใต้ bin ขึ้น note "ยอดหลังปรับติดลบ (คงเหลือ 180)" | ☐ |
| 2 | CLICK **"ถัดไป"** | — | ไม่ไปต่อ · toast (error) **"บรรทัด A-01-02-C ยอดหลังปรับติดลบ — คงเหลือ 180 (BR-03)"** | ☐ |

#### TC-W213 — ต้นทุนอ้างอิงมีป้าย mock แก้ไม่ได้ (FN-13)
- group: Wizard S2 · ความสำคัญ: กลาง · trace: FN-13 / gap G-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY note บนหัว step 2 | — | มีข้อความ "ต้นทุนอ้างอิงมาจาก Item Master (mock)" + chip **"FWD-WIRE: valuation engine (W5)"** + "แก้ไม่ได้" | ☐ |
| 2 | CLICK ช่อง **ต้นทุนอ้างอิง** / **มูลค่าที่ปรับ** ของบรรทัด | — | เป็น read-only (คลิกแก้ค่าไม่ได้) | ☐ |

#### TC-W214 — bin/สินค้า ไม่ครบคู่ → ส่งไม่ได้ (VR-07 · negative)
- group: Wizard S2 · ความสำคัญ: กลาง · trace: VR-06, VR-07 / FN-92 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก bin A-01-02-C แต่ **ไม่เลือกสินค้า** | — | บรรทัดมี bin แต่สินค้าว่าง | ☐ |
| 2 | CLICK **"ถัดไป"** | — | ไม่ไปต่อ · toast **"มีบรรทัดที่เลือก bin หรือสินค้าไม่ครบ"** | ☐ |
| 3 | ลบบรรทัด/เคลียร์ทั้งหมด → CLICK "ถัดไป" (ไม่มีบรรทัดจริง) | — | toast **"กรุณาเพิ่มรายการปรับยอดอย่างน้อย 1 บรรทัด"** | ☐ |

### กลุ่ม W3 — Wizard Step 3 (เหตุผล + หลักฐาน)

> ก่อนทุกเคส W3: สร้างหัวใบ + ≥1 บรรทัดที่มีผลต่าง (เช่น A-01-02-C·STA-0012·195 = +15) → เข้า step **"เหตุผล + หลักฐาน"**.

#### TC-W301 — บรรทัดไม่มีเหตุผล ส่งไม่ได้ (FN-18 · BR-06)
- group: Wizard S3 · ความสำคัญ: สูง · trace: FN-18 / BR-06 / VR-10 / AC-09 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=1 บรรทัด +15 · files=—
- Start: step 3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัดเหตุผล | — | มี combo เหตุผลต่อบรรทัด (ยังว่าง) | ☐ |
| 2 | CLICK **"ถัดไป"** (โดยยังไม่เลือกเหตุผล) | — | ไม่ไปต่อ · toast **"บรรทัด A-01-02-C ยังไม่เลือกเหตุผล (BR-06)"** | ☐ |

#### TC-W302 — dropdown เหตุผลกรองตามทิศ + (FN-37 · BR-07)
- group: Wizard S3 · ความสำคัญ: สูง · trace: FN-37 / BR-07 / AC-09 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=บรรทัดผลต่าง **+15** (bin A-01-02-C · STA-0012 · 195) · files=—
- Start: step 3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK combo เหตุผลของบรรทัด (ผลต่าง +) | — | dropdown แสดงเฉพาะเหตุผลทิศ + และ both: **RS-01, RS-02, RS-07, RS-99** · **ไม่เห็น** RS-03/04/05/06 (กลุ่มลด) | ☐ |
| 2 | SELECT **RS-01 · ของเจอเกินยอดระบบ** | RS-01 | ช่องแสดง RS-01 · ไม่มี error | ☐ |

#### TC-W303 — เหตุผล "อื่น ๆ" บังคับคำอธิบาย (FN-40 · BR-06 · VR-11)
- group: Wizard S3 · ความสำคัญ: สูง · trace: FN-40 / BR-06 / VR-11 / AC-09 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=บรรทัดผลต่าง +15 · files=—
- Start: step 3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT เหตุผล = **RS-99 · อื่น ๆ** | RS-99 | โผล่ช่อง "คำอธิบายเพิ่ม" (needNote) | ☐ |
| 2 | CLICK **"ถัดไป"** (ไม่พิมพ์คำอธิบาย) | — | ไม่ไปต่อ · toast **"เหตุผล \"อื่น ๆ\" ต้องพิมพ์คำอธิบายเพิ่ม (BR-06)"** | ☐ |
| 3 | TYPE "ปรับตามผลตรวจ" → ช่องคำอธิบายเพิ่ม → CLICK "ถัดไป" | ปรับตามผลตรวจ | ไปต่อได้ | ☐ |

#### TC-W304 — เหตุผลรวมของใบ เติมบรรทัดว่าง (FN-41)
- group: Wizard S3/S1 · ความสำคัญ: กลาง · trace: FN-41 / AC-10 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=≥2 บรรทัด (ทิศ + ทั้งคู่) ยังไม่เลือกเหตุผล · files=—
- Start: step 1 (มีช่อง "เหตุผลรวมของใบ")

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ที่ step 1 CLICK ช่อง **"เหตุผลรวมของใบ"** → เลือก RS-01 | RS-01 | ช่องแสดง RS-01 | ☐ |
| 2 | CLICK ปุ่ม **"เติมทุกบรรทัดที่ว่าง"** | — | toast **"เติมเหตุผลให้บรรทัดที่ยังว่างแล้ว"** | ☐ |
| 3 | ไปที่ step 3 VERIFY | — | ทุกบรรทัดที่ว่างถูกเติม RS-01 · ยังแก้รายบรรทัดต่อได้ | ☐ |

#### TC-W305 — แนบไฟล์หลักฐาน (FN-33)
- group: Wizard S3 · ความสำคัญ: กลาง · trace: FN-33 / AC-26 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=1 บรรทัดครบเหตุผล · files=`evidence-damage-01.pdf`
- Start: step 3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY โซนแนบไฟล์ | — | เห็นส่วน "เอกสารแนบหลักฐาน (ถ้ามี)" + upload zone | ☐ |
| 2 | UPLOAD evidence-damage-01.pdf → upload zone | evidence-damage-01.pdf | ไฟล์โผล่ในรายการแนบ + ปุ่ม **"แนบเพิ่ม"** | ☐ |

#### TC-W306 — damage ไม่แนบไฟล์ ส่งไม่ได้ (FN-51 · BR-23)
- group: Wizard S3 · ความสำคัญ: สูง · trace: FN-51 / BR-23 / VR-13 / AC-26 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ประเภท=ตัดจำหน่ายของเสีย · bin DM-01 · สินค้า STA-0044 · ยอดที่ถูกต้อง=0 · เหตุผล RS-06 + คำอธิบาย · files=— (ตั้งใจไม่แนบ)
- Start: OPEN `#/create` (ประเภท damage) → step 3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกเหตุผล RS-06 + พิมพ์คำอธิบาย "ทำลายตามใบบันทึก" (ไม่แนบไฟล์) | — | บรรทัดครบเหตุผล | ☐ |
| 2 | CLICK **"ถัดไป"** | — | ไม่ไปต่อ · toast **"ประเภทตัดจำหน่ายของเสีย ต้องแนบหลักฐานอย่างน้อย 1 ไฟล์ (BR-23)"** | ☐ |
| 3 | UPLOAD evidence-damage-01.pdf → CLICK "ถัดไป" | evidence-damage-01.pdf | ไปต่อได้ | ☐ |

#### TC-W307 — เหตุผลผิดทิศ บล็อก (BR-07 · negative)
- group: Wizard S3 · ความสำคัญ: กลาง · trace: BR-07 / VR-10 / FN-37 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=บรรทัดผลต่าง **−15** (bin A-02-03-B·STA-0044·75) · files=—
- Start: step 3
- หมายเหตุ: dropdown กรองทิศอยู่แล้ว — เคสนี้พิสูจน์ว่า assert ทิศทำงาน (เลือกทิศตรงกับผลต่างได้เท่านั้น)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK combo เหตุผลของบรรทัด (ผลต่าง −) | — | dropdown แสดงเฉพาะทิศ − และ both (RS-03,04,05,06,07,99) · ไม่เห็น RS-01/02 | ☐ |
| 2 | SELECT RS-04 (แตก/ชำรุด) → CLICK "ถัดไป" | RS-04 | ผ่าน (ทิศตรง) · ถ้าระบบยอมให้ RS-01 (ผิดทิศ) จะได้ toast "เหตุผล ของเจอเกินยอดระบบ ไม่ตรงทิศผลต่าง (BR-07)" — ปัจจุบัน dropdown กันไว้แล้ว | ☐ |

### กลุ่ม W4 — Wizard Step 4 (ผู้อนุมัติ · DOA slot)

> ก่อนทุกเคส W4: สร้างใบ (หัว + บรรทัด + เหตุผล) ครบถึง step 3 → CLICK "ถัดไป" เข้า step **"ผู้อนุมัติ"**.

#### TC-W401 — แสดง Σ|มูลค่า| + จำนวนชั้นตามมูลค่า (FN-14)
- group: Wizard S4 · ความสำคัญ: สูง · trace: FN-14 / BR-09 / AC-11 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบ Σ|มูลค่า| < 20,000 (เช่น 1 บรรทัด +15 = 97.50) · files=—
- Start: step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว step 4 | — | แสดง Σ|มูลค่า| ของใบ + จำนวนชั้น DOA (chip "FWD-WIRE: DOA engine") | ☐ |
| 2 | VERIFY slot | — | มี slot การ์ด ตามชั้น (มูลค่าต่ำ = 1 slot ตำแหน่ง **หัวหน้าคลัง**) | ☐ |

#### TC-W402 — ใบมูลค่าต่ำ → 1 ชั้น (FN-15 · boundary <20,000)
- group: Wizard S4 · ความสำคัญ: สูง · trace: FN-15 / AC-11 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=Σ|มูลค่า| = 97.50 (< 20,000) · files=—
- Start: step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY จำนวน slot | — | **1 ชั้น** เท่านั้น — ขั้นที่ 1 ตำแหน่ง **หัวหน้าคลัง** · ป้าย "ขั้นสุดท้าย" | ☐ |

#### TC-W403 — ใบมูลค่าสูง → หลายชั้น (FN-16 · boundary ≥20,000)
- group: Wizard S4 · ความสำคัญ: สูง · trace: FN-16 / AC-11 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ชุด C: A-01-01-A·STA-0031·ยอดที่ถูกต้อง=400 (+200×115 = +23,000 ≥ 20,000) · files=—
- Start: step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY จำนวน slot | — | **2 ชั้น** — ขั้น 1 **หัวหน้าคลัง**, ขั้น 2 **ผู้จัดการคลัง** เรียงลำดับชัดเจน (Σ|มูลค่า| 23,000 อยู่ช่วง 20,000–200,000) | ☐ |

#### TC-W404 — slot ว่าง ส่งอนุมัติไม่ได้ (FN-17 · BR-10 · VR-12)
- group: Wizard S4 · ความสำคัญ: สูง · trace: FN-17 / BR-10 / VR-12 / AC-12 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบ ≥1 บรรทัด · files=—
- Start: step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **"ถัดไป"** (โดยไม่เลือกคนใน slot) | — | ไม่ไปต่อ · toast **"เลือกผู้อนุมัติให้ครบทุกขั้น (BR-10)"** · slot ที่ว่างขึ้นกรอบ error + ข้อความ **"เลือกผู้อนุมัติขั้นนี้"** | ☐ |

#### TC-W405 — slot picker เป็น "คนจริง" ไม่ใช่ role ID + กันเลือกตัวเอง (FN-17, FN-42 · SoD)
- group: Wizard S4 · ความสำคัญ: สูง · trace: FN-17, FN-42 / BR-10 / SoD / AC-12 · actor: หัวหน้าคลัง
- Setup: role=ME(ปวีณา) · seed=ใบ 1 ชั้น (หัวหน้าคลัง) · files=—
- Start: step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องเลือกคนใน slot 1 (placeholder "ค้นหาคนในตำแหน่ง หัวหน้าคลัง…") | — | dropdown แสดง **คนจริง** (avatar + ชื่อ + ตำแหน่ง + dept + code) เช่น **วิชัย มั่นคง · หัวหน้าคลัง · คลัง WH-CNX-01 · EMP-1011** · **ไม่มี** "ปวีณา สุขทวี" (ME ถูกกันออก = SoD) · ไม่มี role ID ลอย ๆ | ☐ |
| 2 | SELECT **วิชัย มั่นคง** | วิชัย มั่นคง | slot 1 แสดงการ์ดคน (avatar+ชื่อ+ตำแหน่ง) + ปุ่ม **"เปลี่ยน"** | ☐ |

#### TC-W406 — ใบผสมสุทธิ≈0 ยังต้องอนุมัติตามค่าสัมบูรณ์ (FN-43 · BR-09)
- group: Wizard S4 · ความสำคัญ: สูง · trace: FN-43 / BR-09 / AC-05 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=บรรทัด +200×115=+23,000 และ −200×115=−23,000 (สุทธิ 0, Σ|มูลค่า|=46,000) · files=—
- Start: step 2 → step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ที่ step 2 VERIFY footer | — | มูลค่าสุทธิ ≈ **0.00** แต่ **Σ มูลค่าค่าสัมบูรณ์ (ฐาน DOA)** = **46,000.00** | ☐ |
| 2 | ไป step 4 VERIFY | — | ยังต้องอนุมัติ **2 ชั้น** (ตาม Σ|มูลค่า| 46,000 ≥ 20,000) — ไม่หลุดเพราะสุทธิ 0 | ☐ |

### กลุ่ม W5 — Wizard Step 5 (ตรวจทาน + บันทึกร่าง/ส่งอนุมัติ)

#### TC-W501 — บันทึกร่าง ไม่มีเลขจริง (FN-19 · BR-21 · EC-05)
- group: Wizard S5 · ความสำคัญ: สูง · trace: FN-19 / BR-21 / EC-05 / AC-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบครบถึง step 5 (บรรทัด +15 · เหตุผล RS-01) · files=—
- Start: step 5 (ตรวจทานและส่ง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY สรุป step 5 | — | ป้าย **"ร่าง — ยังไม่ออกเลขที่"** · สรุปหัวใบ + บรรทัด + totals + สาย + แนบ | ☐ |
| 2 | CLICK ปุ่ม **"บันทึกร่าง"** | — | drawer ปิด · toast **"บันทึกร่างแล้ว"** · เด้งไป `#/view/<id>` | ☐ |
| 3 | VERIFY view drawer | — | เลขที่แสดง **"(ร่าง — ยังไม่ออกเลขที่)"** · ป้าย **ร่าง** · ไม่กระทบสต๊อก (ยังไม่มี movement) | ☐ |

#### TC-W502 — ส่งอนุมัติ → ออกเลข ADJ-YYYY-NNNN (FN-20 · BR-21 · happy)
- group: Wizard S5 · ความสำคัญ: สูง · trace: FN-20 / BR-21 / AC-13 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบครบถึง step 5 · เลือกผู้อนุมัติครบ (วิชัย มั่นคง) · files=—
- Start: step 5
- ผ่านเมื่อ: ออกเลข ADJ-2026-NNNN (ค.ศ.) · status pending · toast ส่งสำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY slot ครบคน + CLICK ปุ่ม **"ส่งอนุมัติ"** | — | ปุ่มขึ้น spinner **"กำลังส่ง…"** ชั่วครู่ | ☐ |
| 2 | WAIT จน toast ปรากฏ (≤3s) | — | toast (success) **"ส่ง ADJ-2026-NNNN เพื่ออนุมัติแล้ว"** (เลขจริงเดินต่อจาก seed สูงสุด เช่น ADJ-2026-0012) · เด้งไป view | ☐ |
| 3 | VERIFY view drawer | — | เลขที่เป็น **ADJ-2026-NNNN** (ค.ศ. รูปแบบ ADJ-YYYY-NNNN) · ป้าย **รออนุมัติ** | ☐ |

#### TC-W503 — ส่งอนุมัติจาก step 5 ทั้งที่ slot ว่าง (FN-17 · BR-10 · negative)
- group: Wizard S5 · ความสำคัญ: สูง · trace: FN-17 / BR-10 / VR-12 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบครบบรรทัด/เหตุผล แต่ **ยังไม่เลือกคนใน slot** · files=—
- Start: step 5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **"ส่งอนุมัติ"** | — | ไม่ส่ง · เด้งกลับ step 4 · toast **"เลือกผู้อนุมัติให้ครบทุกขั้น (BR-10)"** | ☐ |

#### TC-W504 — กันกดส่งรัว (double-submit guard · FN-92 · EC-02)
- group: Wizard S5 · ความสำคัญ: กลาง · trace: FN-92 / EC-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบครบพร้อมส่ง (slot ครบ) · files=—
- Start: step 5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **"ส่งอนุมัติ"** แล้วรีบ CLICK ซ้ำทันที 2–3 ครั้ง | — | ปุ่ม disable ทันทีหลังคลิกแรก (spinner "กำลังส่ง…") · เกิดใบเดียว (ไม่มีเลขซ้ำ/ใบซ้ำ) | ☐ |

### กลุ่ม V — View drawer (รายละเอียด / count-doc / soft-ref)

#### TC-V01 — view detail แสดงหัวใบ + สรุปมูลค่า + บรรทัด RO
- group: View · ความสำคัญ: สูง · trace: FN-30 / AC-20 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab "รายละเอียด" (default) | — | section "ข้อมูลเอกสาร" (เลขที่/คลัง/ประเภท/วันที่มีผล ค.ศ./สถานะ) + "สรุปมูลค่า" (Σ ค่าสัมบูรณ์ ฐาน DOA + สุทธิ) + ตารางบรรทัด (อ่านอย่างเดียว) | ☐ |
| 2 | VERIFY ตารางบรรทัด | — | มีคอลัมน์ ยอดระบบ/ยอดที่ถูกต้อง/ผลต่าง/ต้นทุน/มูลค่า/เหตุผล · แก้ไม่ได้ | ☐ |

#### TC-V02 — count-doc trace เป็น display-only (FN-52 · BR-26 · FIX-04)
- group: View · ความสำคัญ: สูง · trace: FN-52 / BR-26 / AC-24 / XT-11 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 (source=count · ref CNT-2026-0012) · files=—
- Start: OPEN `#/view/d3`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section ข้อมูลเอกสาร | — | มีแถว **"ใบนับต้นเรื่อง (F084/F086)"** แสดงลิงก์ **CNT-2026-0012** + "F084 ตรวจนับใหญ่" | ☐ |
| 2 | CLICK ลิงก์ **CNT-2026-0012** | — | toast **"อ้างอิงใบนับ CNT-2026-0012 — แสดงผล ไม่เปิดหน้าใบนับ"** · **ไม่** เปิด/นำทางไปหน้าใบนับใด ๆ (display-only) | ☐ |

#### TC-V03 — banner ตามสถานะ (returned / cancel / reversed / isReversal)
- group: View · ความสำคัญ: กลาง · trace: FN-22, FN-25 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0005 (returned), ADJ-2026-0006 (cancelled), ADJ-2026-0007 (reversed), ADJ-2026-0008 (isReversal) · files=—
- Start: OPEN `#/view/:id` ราย doc

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN view ADJ-2026-0005 | — | banner **"เคยถูกตีกลับ"** (warn) + เหตุผล + "กลับเป็นร่าง แก้ไขแล้วส่งใหม่ได้" | ☐ |
| 2 | OPEN view ADJ-2026-0006 | — | banner **"ยกเลิก"** (danger) + ผู้ยกเลิก + เหตุผล | ☐ |
| 3 | OPEN view ADJ-2026-0007 | — | banner **"ถูกกลับรายการ"** + ลิงก์ใบกลับ **ADJ-2026-0008** | ☐ |
| 4 | OPEN view ADJ-2026-0008 | — | banner **"ใบกลับรายการของ ADJ-2026-0007 — movement ทิศตรงข้าม"** + ลิงก์กลับต้นฉบับ | ☐ |

#### TC-V04 — JE รอลงบัญชี + marker ไม่มีปุ่มลงบัญชีจริง (FN-30 · BR-19)
- group: View · ความสำคัญ: สูง · trace: FN-30 / BR-19 / XT-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "สรุปมูลค่า" แถว "สถานะลงบัญชี (JE)" | — | ป้าย **"รอลงบัญชี"** + chip **"FWD-WIRE: JE posting"** | ☐ |
| 2 | VERIFY ทั้งหน้า | — | **ไม่มี** ปุ่ม "ลงบัญชี"/"Post JE" ที่ทำงานจริง | ☐ |

#### TC-V05 — สินค้า archive ยังแสดงข้อความเดิม (FN-31 · BR-22 · EC-07 · soft-ref)
- group: View · ความสำคัญ: กลาง · trace: FN-31 / BR-22 / EC-07 / AC-23 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบที่มีสินค้าถูก archive (สินค้าไม่อยู่ใน master แล้ว) · files=— · `(ต้อง simulate: ต้อง seed สินค้าที่ไม่มีใน ITEMS)`
- Start: OPEN `#/view/:id`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัดที่สินค้าถูก archive | — | บรรทัดยังแสดงรหัสสินค้าเดิม (snapshot) + ป้าย **"อ้างอิงถูกยกเลิก"** · ใบเปิดดูได้ไม่พัง | ☐ |

> หมายเหตุ TC-V05: seed default อาจไม่มีสินค้า archive — ถ้า runner สร้าง seed ไม่ได้ให้ mark **BLOCKED** (โค้ดรองรับผ่าน `ITEM_BY[l.item]` เป็น undefined → แสดง pill "อ้างอิงถูกยกเลิก").

#### TC-V06 — deep link view refresh-safe
- group: View · ความสำคัญ: กลาง · trace: (cross-cutting) · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/view/d1`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/d1` ตรง ๆ (พิมพ์ hash) แล้ว refresh หน้า | — | หลัง refresh ยังเปิด view drawer ADJ-2026-0001 หน้าเดิม (ไม่หลุดไป list) | ☐ |
| 2 | OPEN `#/edit/d1` (d1 = posted ไม่ใช่ร่าง) | — | toast **"แก้ไขได้เฉพาะฉบับร่าง"** · เด้งไป view (ไม่เปิด wizard แก้) | ☐ |

### กลุ่ม AP — Approve / Reject

#### TC-AP01 — อนุมัติ slot ตัวเอง → ส่งต่อขั้นถัดไป (FN-21 · happy)
- group: Approve · ความสำคัญ: สูง · trace: FN-21 / AC-14 · actor: ผู้อนุมัติ (ปวีณา = slot1 ของ ADJ-2026-0003)
- Setup: role=ME(ปวีณา) · seed=ADJ-2026-0003 (pending · ผู้ส่ง สมชาย · slot1=ปวีณา WH_LEAD, slot2=สุนีย์ WH_MGR) · files=—
- Start: OPEN `#/view/d3`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions | — | มีปุ่ม **อนุมัติ** + **ตีกลับ** + **ยกเลิก** (canActStep true: ปวีณาเป็น slot1, ไม่ใช่ผู้ส่ง) | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** | — | modal "อนุมัติ ADJ-2026-0003 — ขั้น 1/2" เปิด · note "ยังมีขั้นถัดไป — ส่งต่อผู้อนุมัติคนถัดไป" | ☐ |
| 3 | CLICK ปุ่ม **อนุมัติ** ใน modal | — | toast (success) **"อนุมัติขั้น 1 แล้ว — ส่งต่อ สุนีย์ เจริญสุข"** · ใบยัง **รออนุมัติ** (เหลือขั้น 2) | ☐ |

#### TC-AP02 — อนุมัติครบทุกขั้น → อนุมัติแล้ว (FN-21)
- group: Approve · ความสำคัญ: สูง · trace: FN-21 / AC-14 · actor: ผู้อนุมัติ
- Setup: role=ME · seed=ใบ pending ที่ ปวีณาเป็นผู้อนุมัติ **ขั้นสุดท้าย** · `(ต้อง simulate)` — prototype single-user: ขั้น 2 ของ seed = สุนีย์(WH_MGR) ที่ ปวีณากดแทนไม่ได้ (role mismatch)
- Start: OPEN `#/view/:id`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เป็นผู้อนุมัติขั้นสุดท้าย CLICK **อนุมัติ** | — | modal note "ขั้นสุดท้าย — เอกสารเป็น \"อนุมัติแล้ว\" · หัวหน้าคลังกด \"ผ่านรายการ\" เพื่อสร้าง movement" · หลังยืนยัน → toast **"อนุมัติครบทุกขั้น — สถานะ \"อนุมัติแล้ว\" · กด \"ผ่านรายการ\" เพื่อโพสต์"** · ป้าย **อนุมัติแล้ว** | ☐ |

> TC-AP02: prototype ทำครบสายด้วยผู้ใช้เดียวไม่ได้ (ขั้น 2 = WH_MGR) → mark **BLOCKED** พร้อม evidence ปุ่มอนุมัติขั้น 2 ไม่โผล่. หลักฐานสถานะ "อนุมัติแล้ว" ใช้ seed ADJ-2026-0011 แทน (ดู TC-PO03).

#### TC-AP03 — ตีกลับ → กลับเป็นร่าง (FN-22 · happy)
- group: Reject · ความสำคัญ: สูง · trace: FN-22 / BR-11 / AC-15 · actor: ผู้อนุมัติ (ปวีณา slot1 ของ d3)
- Setup: role=ME · seed=ADJ-2026-0003 (pending) · files=—
- Start: OPEN `#/view/d3`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ตีกลับ** | — | modal reason หัวข้อ **"ตีกลับ ADJ-2026-0003 เป็นร่าง"** + ช่องเหตุผล (บังคับ *) | ☐ |
| 2 | TYPE "ยอดไม่ตรงเอกสารแนบ" → ช่องเหตุผล → CLICK ปุ่ม **ตีกลับ** | ยอดไม่ตรงเอกสารแนบ | modal ปิด · toast (info) **"ตีกลับ ADJ-2026-0003 เพื่อแก้ไข"** · ป้ายใบเปลี่ยนเป็น **ร่าง** + banner "เคยถูกตีกลับ" | ☐ |

#### TC-AP04 — ตีกลับไม่กรอกเหตุผล บล็อก (BR-11 · VR-14 · negative)
- group: Reject · ความสำคัญ: สูง · trace: FN-22 / BR-11 / VR-14 · actor: ผู้อนุมัติ
- Setup: role=ME · seed=ADJ-2026-0009 (pending · ปวีณา slot1) · files=—
- Start: OPEN `#/view/d9`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ตีกลับ** → CLICK ปุ่ม **ตีกลับ** ใน modal (ไม่กรอกเหตุผล) | — | ไม่ทำงาน · toast **"กรุณาระบุเหตุผล"** · ใบยัง **รออนุมัติ** | ☐ |

#### TC-AP05 — ผู้จัดทำอนุมัติใบตัวเองไม่ได้ (SoD · ERR_SOD_SELF_APPROVAL)
- group: Approve · ความสำคัญ: สูง · trace: SoD §5.3 / AC-14 / TC-SOD-01 · actor: หัวหน้าคลัง
- Setup: role=ME(ปวีณา) · seed=สร้าง+ส่งอนุมัติใบใหม่เอง (ผู้ส่ง=ปวีณา, slot=วิชัย) · files=—
- Start: สร้างใบ → ส่งอนุมัติ (TC-W502) → OPEN view ใบนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | หลังส่งอนุมัติใบที่ ปวีณาเป็นผู้ส่ง OPEN `#/view/<id>` (pending) | — | **ไม่มี** ปุ่ม อนุมัติ/ตีกลับ (canActStep false เพราะผู้ใช้ = ผู้ส่ง) · มีแต่ปุ่ม **ยกเลิก** — พิสูจน์ SoD ระดับใบ | ☐ |

### กลุ่ม PO — Post + drift (BR-15)

#### TC-PO01 — ผ่านรายการใบ approved (ไม่มี drift) → posted (FN-23 · happy)
- group: Post · ความสำคัญ: สูง · trace: FN-23 / AC-16, AC-20 / XT-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบ approved ไม่มี drift · `(ต้อง simulate: seed ADJ-2026-0011 มี drift)` — ใช้ใบ approved อื่นที่ curSys ตรง หรือรับ drift dialog ก่อน
- Start: OPEN view ใบ approved

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions (approved) | — | มีปุ่มเดียว **ผ่านรายการ** (ไม่มี ยกเลิก — FIX-02) | ☐ |
| 2 | CLICK **ผ่านรายการ** | — | modal "ผ่านรายการ <code>?" (กรณีไม่มี drift) + ปุ่ม **ผ่านรายการ** | ☐ |
| 3 | CLICK **ผ่านรายการ** ใน modal | — | toast (success) **"ผ่านรายการ <code> — movement เกิดแล้ว · JE รอลงบัญชี"** · ป้ายใบ **ผ่านรายการ** | ☐ |

#### TC-PO02 — post ทางลัดจากร่าง/ก่อน approved บล็อก (FN-23 · BR-08 · negative)
- group: Post · ความสำคัญ: สูง · trace: FN-23 / BR-08 / AC-16 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบร่าง หรือ pending · files=—
- Start: OPEN view ใบ pending (ADJ-2026-0003)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions (pending) | — | **ไม่มี** ปุ่ม "ผ่านรายการ" (โผล่เฉพาะ approved) — พิสูจน์ไม่มีทางลัด post จากร่าง/pending | ☐ |

#### TC-PO03 — ยอดเปลี่ยนก่อน post → เตือน 2 ยอด (FN-27 · BR-15 · EC-04) [AI-DEFAULT]
- group: Post · ความสำคัญ: สูง · trace: FN-27 / BR-15 / EC-04 / AC-19 / TC-QTY-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved · บรรทัด A-01-02-C ยอด ณ สร้าง 180 → ยอดล่าสุด 186) · files=—
- Start: OPEN `#/view/d11`
- หมายเหตุ: BR-15 มาจาก PREBRIEF (ไม่ใช่ AI-DEFAULT) แต่ปุ่ม/นโยบายค่า default อื่นเป็น [AI-DEFAULT]

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ผ่านรายการ** | — | modal เตือน หัวข้อ **"ยอดระบบเปลี่ยนหลังสร้างบรรทัด"** + ตาราง 2 ยอด (bin·สินค้า / **ยอด ณ ตอนสร้าง** 180 / **ยอดล่าสุด** 186 / ผลต่างใหม่) | ☐ |
| 2 | VERIFY ปุ่มใน modal | — | มี 2 ปุ่ม: **"ตีกลับไปแก้"** และ **"คิดจากยอดล่าสุด"** | ☐ |
| 3 | CLICK **"คิดจากยอดล่าสุด"** | — | modal ปิด · toast **"ผ่านรายการ ADJ-2026-0011 — movement เกิดแล้ว · JE รอลงบัญชี"** · ป้าย **ผ่านรายการ** | ☐ |

#### TC-PO04 — drift dialog เลือก "ตีกลับไปแก้" (FN-27 · BR-15)
- group: Post · ความสำคัญ: กลาง · trace: FN-27 / BR-15 / AC-19 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved · มี drift) · files=—
- Start: OPEN `#/view/d11`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ผ่านรายการ** → ใน drift modal CLICK **"ตีกลับไปแก้"** | — | เปิด modal ตีกลับ (reason) — ต่อเป็น flow ตีกลับ · ไม่ post · ใบไม่กลายเป็น posted | ☐ |

#### TC-PO05 — capture baseline ยอดคงเหลือ ก่อน/หลัง post (R17 · XT-01)
- group: Post · ความสำคัญ: กลาง · trace: FN-23, FN-29 / XT-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved) · files=—
- Start: OPEN `#/view/d11`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด ยอด ณ ตอนสร้าง/ล่าสุด จาก drift dialog | — | บันทึกค่า: บรรทัด A-01-02-C ยอด ณ สร้าง=180, ล่าสุด=186 (อ้างใน step ถัดไป) | ☐ |
| 2 | CLICK "คิดจากยอดล่าสุด" → post → เปิด tab **ประวัติ** | — | เกิด movement "ปรับเพิ่ม/ปรับลด" ที่ bin เดิม จำนวน = ผลต่างที่คิดจากยอดล่าสุด 186 (ไม่ใช่ 180) — สอดคล้องค่าที่จดใน step 1 | ☐ |

### กลุ่ม CX — Cancel (BR-27 / FIX-02)

#### TC-CX01 — ยกเลิกใบร่าง (FN-24 · happy)
- group: Cancel · ความสำคัญ: สูง · trace: FN-24 / BR-27 / AC-17 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบร่าง (draft) · files=—
- Start: OPEN view ใบร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions (draft) | — | มีปุ่ม แก้ไข · ส่งอนุมัติ · **ยกเลิก** | ☐ |
| 2 | CLICK **ยกเลิก** → TYPE เหตุผล "สร้างผิด" → CLICK **"ยืนยันยกเลิก"** | สร้างผิด | toast (success) **"ยกเลิก <code> แล้ว"** · ป้าย **ยกเลิก** · ใบยังอยู่ในระบบ (ไม่ถูกลบ) | ☐ |

#### TC-CX02 — ใบ approved ไม่มีปุ่มยกเลิก (FN-24 · BR-27 · FIX-02 · negative) ★
- group: Cancel · ความสำคัญ: สูง · trace: FN-24 / BR-27 / FIX-02 / AC-17 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved) · files=—
- Start: OPEN `#/view/d11`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions (approved) | — | มีปุ่มเดียว **ผ่านรายการ** · **ไม่มี** ปุ่มยกเลิก (พิสูจน์ approved ยกเลิกไม่ได้) | ☐ |
| 2 | VERIFY ใบ posted (ADJ-2026-0001) header | — | มีปุ่ม **กลับรายการ** · **ไม่มี** ยกเลิก | ☐ |

#### TC-CX03 — ยกเลิกไม่กรอกเหตุผล บล็อก (BR-27 · VR-14 · negative)
- group: Cancel · ความสำคัญ: กลาง · trace: FN-24 / VR-14 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบร่าง หรือ pending · files=—
- Start: OPEN view ใบร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → CLICK **"ยืนยันยกเลิก"** (ไม่กรอกเหตุผล) | — | toast **"กรุณาระบุเหตุผล"** · ใบไม่ถูกยกเลิก | ☐ |

### กลุ่ม RV — Reverse (FIX-03)

#### TC-RV01 — ใบ posted มีปุ่มกลับรายการ ไม่มียกเลิก (FN-25 · BR-17)
- group: Reverse · ความสำคัญ: สูง · trace: FN-25 / BR-17 / AC-18 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted · ยังไม่ถูกกลับ) · files=—
- Start: OPEN `#/view/d1`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions (posted) | — | มีปุ่ม **กลับรายการ** เท่านั้น · **ไม่มี** ยกเลิก | ☐ |

#### TC-RV02 — กลับรายการ → สร้างใบใหม่ pending เข้าสาย DOA (FN-25 · FIX-03 · happy)
- group: Reverse · ความสำคัญ: สูง · trace: FN-25 / BR-17 / VR-14 / AC-18 / XT-06 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1`
- ผ่านเมื่อ: สร้างใบกลับรายการใหม่ status pending · ไม่ auto-post · ต้นฉบับ = กลับรายการแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **กลับรายการ** | — | modal reason หัวข้อ **"กลับรายการ ADJ-2026-0001"** + desc "สร้าง movement ทิศตรงข้าม + ผูกคู่ใบ 2 ทาง · กลับรายการซ้ำไม่ได้..." + ช่องเหตุผล | ☐ |
| 2 | TYPE "ลงผิด bin" → CLICK **"ยืนยันกลับรายการ"** | ลงผิด bin | toast (success) **"สร้างใบกลับรายการ ADJ-2026-NNNN — รออนุมัติตามมูลค่าก่อนผ่านรายการ"** · เด้งไป view ใบกลับรายการใหม่ | ☐ |
| 3 | VERIFY ใบกลับรายการใหม่ | — | ป้าย **รออนุมัติ** (ไม่ auto-post) · banner "ใบกลับรายการของ ADJ-2026-0001" · มีสายอนุมัติ DOA ตาม Σ|มูลค่า| ของตัวเอง | ☐ |
| 4 | OPEN view ADJ-2026-0001 (ต้นฉบับ) | — | ป้าย **กลับรายการแล้ว** + banner "ถูกกลับรายการ" + ลิงก์ใบกลับ | ☐ |

#### TC-RV03 — กลับรายการซ้ำไม่ได้ (FN-44 · BR-18 · negative)
- group: Reverse · ความสำคัญ: สูง · trace: FN-44 / BR-18 / AC-18 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0007 (reversed · reversedBy 0008) + ADJ-2026-0008 (isReversal) · files=—
- Start: OPEN `#/view/d7` และ `#/view/d8`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ADJ-2026-0007 (reversed) header | — | **ไม่มี** ปุ่มกลับรายการ (ป้าย กลับรายการแล้ว) | ☐ |
| 2 | VERIFY ADJ-2026-0008 (posted · isReversal) header | — | **ไม่มี** ปุ่มกลับรายการ (ใบกลับรายการเอง reverse ซ้ำไม่ได้) | ☐ |
| 3 | (ถ้ามีทางกด) CLICK กลับรายการ ใบที่ถูกกลับแล้ว | — | toast **"กลับรายการซ้ำไม่ได้ (BR-18)"** | ☐ |

#### TC-RV04 — post ใบกลับรายการ → ต้นฉบับ reversed + movement ทิศตรงข้าม (BR-17.1)
- group: Reverse · ความสำคัญ: กลาง · trace: FN-25, FN-29 / BR-17.1 / XT-06 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0008 (posted · isReversal ของ 0007) · files=—
- Start: OPEN `#/view/d8` → tab ประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด tab **ประวัติ** ของ ADJ-2026-0008 | — | Movement table แสดง **"กลับรายการปรับเพิ่ม/ปรับลด"** (ทิศตรงข้ามต้นฉบับ) + note "ผูกคู่กับ ADJ-2026-0007 (2 ทาง)" | ☐ |
| 2 | OPEN ADJ-2026-0007 → VERIFY | — | ป้าย **กลับรายการแล้ว** (ต้นฉบับถูกตั้ง reversed เมื่อใบกลับ post) | ☐ |

### กลุ่ม PD — PDF Preview / ลายเซ็น·อนุมัติ (view drawer tabs)

#### TC-PD01 — tab PDF Preview เรนเดอร์ A4 ครบองค์ (FN-34, FN-38 · AC-22)
- group: PDF · ความสำคัญ: กลาง · trace: FN-34, FN-38 / AC-22 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted · หลายบรรทัด) · files=—
- Start: OPEN `#/view/d1`
- ผ่านเมื่อ: A4 preview แสดงหัวกระดาษ + ตาราง 8 คอลัมน์ + totals + ช่องลายเซ็น · ทุกวันที่ ค.ศ.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **PDF Preview** | — | แถบเครื่องมือบน: **"ตัวอย่าง PDF · A4 · 1/1 · template ตาม thai-doc-pdf-generator"** + ปุ่ม **ดาวน์โหลด** / **พิมพ์** · ด้านล่างเป็นกระดาษ `.a4` | ☐ |
| 2 | VERIFY หัวกระดาษ | — | **"บริษัท 2BSimple จำกัด"** + "เลขผู้เสียภาษี 0105560000001 (สำนักงานใหญ่)" · หัวเอกสาร **"ใบปรับยอดสต๊อก / STOCK ADJUSTMENT"** + เลขที่ **ADJ-2026-0001** + "วันที่มีผล \<วันที่ ค.ศ.\>" | ☐ |
| 3 | VERIFY หัวตาราง PDF | — | คอลัมน์: **# · bin · สินค้า · ยอดระบบ · ที่ถูกต้อง · ผลต่าง · มูลค่า · เหตุผล** (8 คอลัมน์ · **ไม่มี VAT**) | ☐ |
| 4 | VERIFY totals ท้ายตาราง | — | แถว **"มูลค่าสุทธิ (+/−)"** + แถวหนา **"Σ มูลค่าค่าสัมบูรณ์"** | ☐ |
| 5 | VERIFY แถวช่องลายเซ็น | — | มีช่อง **ผู้จัดทำ** (ชื่อผู้สร้าง) + **ผู้อนุมัติขั้น 1..N** ตามชั้น DOA (เส้นลายเซ็น + ชื่อ/ตำแหน่งใต้เส้น) | ☐ |
| 6 | VERIFY รูปแบบปี | — | ทุกวันที่บนกระดาษเป็น **ค.ศ.** (เช่น 2026) · ไม่มี พ.ศ. 25xx ที่ใดเลย | ☐ |

#### TC-PD02 — ปุ่มพิมพ์ / ดาวน์โหลดบน PDF tab (FN-34)
- group: PDF · ความสำคัญ: ต่ำ · trace: FN-34 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/view/d1` → tab **PDF Preview**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **พิมพ์** | — | เปิด print dialog ของ browser (`window.print()`) — mark BLOCKED ถ้า runner กัน dialog | ☐ |
| 2 | CLICK ปุ่ม **ดาวน์โหลด** | — | toast **"ดาวน์โหลด PDF (mock)"** (ยังไม่มี backend ดาวน์โหลดจริง) | ☐ |

#### TC-PD03 — tab ลายเซ็น / อนุมัติ แสดงการ์ดผู้อนุมัติ "คนจริง" (FN-28 · AC-14)
- group: Sign · ความสำคัญ: สูง · trace: FN-28, FN-42 / AC-14 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 (pending · 2 ชั้น · slot1=ปวีณา(ME) pending) · files=—
- Start: OPEN `#/view/d3`
- ผ่านเมื่อ: timeline แสดงคนจริงเรียงตามชั้น + ทะเบียน DOA + ปุ่มอนุมัติ/ตีกลับที่ slot ของ ME

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **ลายเซ็น / อนุมัติ** | — | section **"สายอนุมัติ (DOA)"** + การ์ด: **"ทะเบียน DOA"** = `DOA-WH-STKADJ` + ป้าย **"FWD-WIRE: DOA engine"** · **"สถานะ · ความคืบหน้า"** = pill สถานะ + `done/total` · **"ฐานคำนวณ (Σ\|มูลค่า\|)"** = ฿… · N ชั้น · **"ผู้ส่งอนุมัติ"** = สมชาย ใจดี + วันเวลา (ค.ศ.) | ☐ |
| 2 | VERIFY timeline สายอนุมัติ | — | แต่ละขั้นเป็น **การ์ดคนจริง** (ชื่อ + ตำแหน่ง เช่น "หัวหน้าคลัง · …") · ป้าย **"ขั้นที่ 1"**, **"ขั้นที่ 2 · ขั้นสุดท้าย"** · ไม่มีที่ไหนโชว์ role ID (WH_LEAD/WH_MGR) แทนคน | ☐ |
| 3 | VERIFY ปุ่มบน slot รออนุมัติ (ME) | — | ขั้นที่ ปวีณา (ME) เป็น pending → มีปุ่ม **อนุมัติ** + **ตีกลับ** (canActStep เพราะ ME ไม่ใช่ผู้ส่ง) | ☐ |

#### TC-PD04 — sign tab สะท้อนชั้น DOA ตามมูลค่า + SoD ผู้ส่ง≠ผู้อนุมัติ (FN-14, FN-17 · doaTiers 20k/200k/1M)
- group: Sign · ความสำคัญ: กลาง · trace: FN-14, FN-17, FN-42 / AC-11, AC-12 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved · general · Σ|มูลค่า| ต่ำ) + ADJ-2026-0003 (pending · 2 ชั้น) · files=—
- Start: OPEN `#/view/d11` → tab **ลายเซ็น / อนุมัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY "ฐานคำนวณ (Σ\|มูลค่า\|)" + จำนวนชั้น (ADJ-2026-0011) | — | แสดง `฿<Σabs> · N ชั้น` โดย N ตรงกับจุดตัด mock **20,000 / 200,000 / 1,000,000** (ต่ำกว่า 20,000 = 1 ชั้น) | ☐ |
| 2 | OPEN `#/view/d3` → sign tab → VERIFY 2 ชั้น | — | ใบ ADJ-2026-0003 (Σ|มูลค่า| ≥20,000) แสดง **2 ชั้น** (หัวหน้าคลัง + ผู้จัดการคลัง) | ☐ |
| 3 | VERIFY SoD ผู้ส่ง≠ผู้อนุมัติ | — | **"ผู้ส่งอนุมัติ" = สมชาย ใจดี** (ผู้สร้าง) ไม่ปรากฏเป็นการ์ดผู้อนุมัติในสายเดียวกัน (ผู้จัดทำ/ผู้ส่งอนุมัติใบตัวเองไม่ได้) | ☐ |

### กลุ่ม HS — ประวัติ / Movement (append-only)

#### TC-HS01 — tab ประวัติ: audit timeline + Movement table + JE marker (FN-29, FN-30 · BR-16/BR-19 · AC-20)
- group: History · ความสำคัญ: กลาง · trace: FN-29, FN-30 / BR-16, BR-19 / AC-20 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted · มี movements) · files=—
- Start: OPEN `#/view/d1`
- ผ่านเมื่อ: เห็น timeline ประวัติ + ตาราง Movement + JE "รอลงบัญชี" · ไม่มีปุ่มลบ/แก้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **ประวัติ** | — | section **"ประวัติ (append-only)"** · timeline เหตุการณ์ (act) แต่ละอันมี ผู้ทำ · วันเวลา (ค.ศ.) | ☐ |
| 2 | VERIFY ตาราง Movement | — | section **"Movement ที่เกิด (append-only · ไม่มีปุ่มลบ/แก้)"** · หัวตาราง: **ประเภท · สินค้า · bin · จำนวน · มูลค่า · JE** | ☐ |
| 3 | VERIFY แถว movement + JE | — | pill **ปรับเพิ่ม** (เขียว) / **ปรับลด** (แดง) ตามทิศ · คอลัมน์ JE = pill **"รอลงบัญชี"** + ป้าย **"FWD-WIRE: JE posting"** | ☐ |
| 4 | VERIFY ไม่มี affordance แก้ movement | — | ในตาราง movement **ไม่มี** ปุ่มลบ/แก้/ยกเลิกรายบรรทัด (พิสูจน์ append-only) | ☐ |

#### TC-HS02 — reversal ผูกคู่ movement ทิศตรงข้าม + ลิงก์ 2 ทาง (FN-29)
- group: History · ความสำคัญ: กลาง · trace: FN-29 / BR-17.1 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0008 (posted · isReversal ของ ADJ-2026-0007) · files=—
- Start: OPEN `#/view/d8`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **ประวัติ** → VERIFY movement type | — | pill movement เป็น **"กลับรายการปรับเพิ่ม"** หรือ **"กลับรายการปรับลด"** (ทิศตรงข้ามต้นฉบับ) | ☐ |
| 2 | VERIFY note ผูกคู่ | — | มี note **"ผูกคู่กับ ADJ-2026-0007 (2 ทาง)"** + ลิงก์คลิกได้ (`gotoByCode`) | ☐ |
| 3 | CLICK ลิงก์ **ADJ-2026-0007** | — | เด้งไปเปิดใบ ADJ-2026-0007 (ต้นฉบับ · สถานะ กลับรายการแล้ว) | ☐ |

#### TC-HS03 — audit append-only ครบทุก event (FN-39 · BR-25)
- group: History · ความสำคัญ: กลาง · trace: FN-39 / BR-25 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0005 (draft · returned · ผ่านรอบตีกลับ) · files=—
- Start: OPEN view ของ ADJ-2026-0005

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **ประวัติ** | — | timeline แสดงเหตุการณ์ตามลำดับเวลา เช่น **สร้าง / ส่งอนุมัติ / ตีกลับ** — แต่ละอันมี ผู้ทำ + วันเวลา ค.ศ. + note (ถ้ามี) | ☐ |
| 2 | VERIFY append-only | — | ทุกเหตุการณ์เป็น log ต่อท้าย · **ไม่มี** ปุ่มลบ/แก้ประวัติ · เหตุการณ์ตีกลับยังคงอยู่ (ไม่ถูกลบเมื่อกลับเป็นร่าง) | ☐ |

### กลุ่ม NG — Negative "พิสูจน์ว่าไม่มี" (§6.7 หมวด 7 · render-and-assert-absent)

#### TC-NG01 — in-transit (TR-*) ไม่โผล่ใน picker (FN-32 · BR-13 · NEG-01)
- group: Negative · ความสำคัญ: สูง · trace: FN-32 / BR-13 / NEG-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → กรอกหัวใบ → ถัดไป → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin บรรทัดแรก → TYPE "TR-" | TR- | หัว dropdown mute **"bin ระหว่างทาง (in-transit · TR-*) สงวนให้โอนย้ายสต๊อก — ไม่แสดงในใบปรับยอด"** · ไม่มี option TR-* ให้เลือก | ☐ |
| 2 | TYPE "TR-BKK-CNX" ต่อ | TR-BKK-CNX | ไม่มีผลลัพธ์ bin ระหว่างทางในรายการ (พิสูจน์ FN-32) | ☐ |

#### TC-NG02 — ไม่มีฟังก์ชันนับสต๊อก/cycle count (FN-35 · BR-24 · NEG-02)
- group: Negative · ความสำคัญ: สูง · trace: FN-35 / BR-24 / NEG-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทั้งหน้า list + sidebar | — | **ไม่มี** ปุ่ม/เมนู/คำว่า "ตรวจนับ / นับสต๊อก / นับรอบ / cycle count / count sheet" ที่ใดบนจอ | ☐ |
| 2 | OPEN `#/create` → เดินทุก step | — | ไม่มี step/ปุ่ม "นับสต๊อก" · "จากใบนับ" เป็นเพียง **การอ้างอิงแบบแสดงผล** ไม่ใช่การเปิด/ทำการนับ | ☐ |

#### TC-NG03 — ไม่มี bin ปลายทาง / ช่องย้าย (FN-36 · BR-05 · NEG-03)
- group: Negative · ความสำคัญ: สูง · trace: FN-36 / BR-05 / NEG-03 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin → TYPE "ย้าย" | ย้าย | หัว dropdown warn **"การย้ายของระหว่าง bin/คลัง ไม่อยู่ในใบปรับยอด — ใช้ \"โอนย้ายสต๊อก\" (Stock Transfer)"** | ☐ |
| 2 | VERIFY โครงสร้างบรรทัด | — | แต่ละบรรทัดมี **bin เดียว** (single-bin movement) · **ไม่มี** ช่อง "ย้ายไป / bin ปลายทาง / to-bin" | ☐ |

#### TC-NG04 — quarantine ปรับในบิ๊นเดิม ย้ายออกไม่ได้ (FN-46 · BR-12 · NEG-04)
- group: Negative · ความสำคัญ: กลาง · trace: FN-46 / BR-12 / NEG-04 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → หัวใบ ประเภท=**ปรับยอดกักกัน** → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin → VERIFY picker | — | เหลือเฉพาะ bin **QA-*** (กักกัน) · ไม่มี storage bin | ☐ |
| 2 | VERIFY ไม่มีทางย้ายออก | — | ปรับได้เฉพาะยอดใน QA-01 เดิม · **ไม่มี** ตัวเลือก/ช่องกำหนดปลายทางไป storage (ปรับได้ ย้ายออกไม่ได้) | ☐ |

#### TC-NG05 — ไม่มีช่องกรอกเลขเอง / ตั้งเลขรัน (FN-47 · NEG-05)
- group: Negative · ความสำคัญ: กลาง · trace: FN-47 / BR-21 / NEG-05 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "เลขที่เอกสาร" | — | **disabled** แสดง **"(ร่าง — ยังไม่ออกเลขที่)"** · พิมพ์/แก้ไม่ได้ | ☐ |
| 2 | VERIFY ไม่มีหน้าตั้งค่าเลขรัน | — | ไม่มีปุ่ม/หน้า "ตั้งค่าเลขรัน / running number / รูปแบบเลขเอกสาร" ใน feature (เลขมาจาก ENG-DOC-NUM) | ☐ |

#### TC-NG06 — ไม่มีช่อง threshold / % (FN-48 · BR-20 · NEG-06)
- group: Negative · ความสำคัญ: กลาง · trace: FN-48 / BR-20 / NEG-06 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/list` → แล้ว OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทั่วทั้ง wizard + view | — | **ไม่มี** ช่องตั้ง threshold / เปอร์เซ็นต์ / เกณฑ์ NC ให้กรอกในใบ | ☐ |
| 2 | VERIFY การ์ด KPI "ใบเกินเกณฑ์อายุ" | — | meta **"ตามเกณฑ์ NC rules"** เป็นข้อความอ้างอิงแบบ read-only · ไม่ใช่ที่ตั้งค่า threshold | ☐ |

#### TC-NG07 — ไม่มีคอลัมน์ VAT / ส่วนลด (FN-49 · NEG-07)
- group: Negative · ความสำคัญ: สูง · trace: FN-49 / NEG-07 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวตาราง line editor (step 2) | — | **ไม่มี** คอลัมน์ VAT / ภาษี / ส่วนลด · ตำแหน่งนั้นถูกแทนด้วย segmented **"โหมดกรอก: ระบุยอดที่ถูกต้อง / ระบุจำนวนที่ปรับ"** | ☐ |
| 2 | OPEN `#/view/d1` → tab **PDF Preview** → VERIFY | — | ตารางบนกระดาษ A4 ก็ **ไม่มี** คอลัมน์ VAT | ☐ |

#### TC-NG08 — ไม่มีปุ่มลบ/แก้ movement + ไม่มีปุ่มลงบัญชีจริง (FN-45 · BR-16/BR-19 · NEG-08)
- group: Negative · ความสำคัญ: สูง · trace: FN-45 / BR-16, BR-19 / NEG-08 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1` → tab **ประวัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง Movement | — | แต่ละแถว **ไม่มี** ปุ่มลบ/แก้/ยกเลิก (append-only · แก้ผิดใช้ "กลับรายการ" เท่านั้น) | ☐ |
| 2 | VERIFY JE | — | JE เป็น pill **"รอลงบัญชี"** อ่านอย่างเดียว · **ไม่มี** ปุ่ม "ลงบัญชี / post JE จริง" (BR-19 · post ไม่ post JE จริง) | ☐ |

#### TC-NG09 — sidebar ตาม module map ไม่มีเมนูที่คิดเอง (FN-50 · NEG-09)
- group: Negative · ความสำคัญ: กลาง · trace: FN-50 / NEG-09 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY sidebar กลุ่ม "คลังสินค้า" | — | มี 4 เมนู: **รับเข้า-จัดเก็บ · ใบปรับยอดสต๊อก** (active) **· โอนย้ายสต๊อก · คืนผู้ขาย (RTV)** — ไม่มีเมนูนอก module map (เช่น "ตรวจนับ") | ☐ |
| 2 | CLICK เมนูอื่น (เช่น "โอนย้ายสต๊อก") | — | toast **"เปิด โอนย้ายสต๊อก (mock)"** (ไม่ใช่ route จริง — one-feature-one-menu) | ☐ |

#### TC-NG10 — "จากใบนับ" เป็น display-only ไม่เปิด/สร้างหน้าใบนับ (FN-52 · BR-26/FIX-04 · NEG · LOCK-02 no cycle count)
- group: Negative · ความสำคัญ: กลาง · trace: FN-52 / BR-26 / XT-11 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 (source=count · ref CNT-2026-0012) · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอกหัวใบ → CLICK segmented **"จากใบนับ"** → เลือก **CNT-2026-0012** | CNT-2026-0012 | ช่องแสดง **"CNT-2026-0012 · F084 ตรวจนับใหญ่"** แบบอ่านอย่างเดียว | ☐ |
| 2 | VERIFY ไม่มี affordance เปิด/สร้างใบนับ | — | **ไม่มี** ปุ่ม "เปิดใบนับ / สร้างใบนับ / ไปหน้านับ" — เป็นเพียง ref (feature นี้ไม่ทำการนับ) | ☐ |
| 3 | OPEN `#/view/d3` → CLICK "ใบนับต้นเรื่อง" | — | ข้อความ **"อ้างอิงใบนับ CNT-2026-0012 — แสดงผล ไม่เปิดหน้าใบนับ"** (display-only) | ☐ |

### กลุ่ม GN — General / edge / permission

#### TC-GN01 — ปี ค.ศ. ทุกจุด (FN-38)
- group: General · ความสำคัญ: กลาง · trace: FN-38 / AC-22 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY list foot + คอลัมน์วันที่ | — | foot มี **"ปี ค.ศ. · มูลค่าอ้างอิงจาก Item Master (mock)"** · วันที่ในตารางเป็น ค.ศ. | ☐ |
| 2 | OPEN `#/view/d1` → ไล่ tab รายละเอียด / PDF / ประวัติ | — | ทุกวันที่/วันเวลาเป็น **ค.ศ.** (เช่น 2026) · **ไม่มี** พ.ศ. 25xx ที่ใดเลย | ☐ |

#### TC-GN02 — deep link `#/view/:id` refresh-safe
- group: General · ความสำคัญ: กลาง · trace: cross-cutting (refresh-safe) · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/view/d1` ตรง ๆ (จำลอง refresh ที่ deep link)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/d1` (โหลดตรง) | — | view drawer เปิดที่ **ADJ-2026-0001** ทันที (ไม่ตกกลับ `#/list` เปล่า) · 4 tabs ครบ | ☐ |

#### TC-GN03 — Esc chain (combo → modal → drawer)
- group: General · ความสำคัญ: กลาง · trace: cross-cutting (Esc chain · DSP) · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง bin (เปิด combo) → PRESS **Esc** | — | combo ปิด · drawer wizard ยังเปิดอยู่ (ปิดชั้นในสุดก่อน) | ☐ |
| 2 | กลับ step 1 → เปลี่ยนคลัง (เปิด modal "เปลี่ยนคลัง") → PRESS **Esc** | — | modal ปิด · drawer ยังเปิด · คลังไม่ถูกล้าง | ☐ |
| 3 | PRESS **Esc** อีกครั้ง (ที่ drawer) | — | ถ้ามีการแก้ค้าง → modal ยืนยันปิด (dirty-check) ปรากฏ; ถ้าไม่มี → drawer ปิดกลับ list `⚠ ยืนยัน anchor` | ☐ |

#### TC-GN04 — dirty-check ปิด wizard ทั้งที่มีข้อมูลค้าง
- group: General · ความสำคัญ: กลาง · trace: UX dirty-check · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT คลัง + TYPE วันที่ (กรอกบางช่อง) → CLICK **ปิด** / ไอคอนปิด | ชุด A (หัว) | มี modal ยืนยันปิดโดยยังไม่บันทึกร่างปรากฏ (กันข้อมูลหาย) `⚠ ยืนยัน anchor` | ☐ |
| 2 | CLICK ยกเลิกการปิด (อยู่ต่อ) | — | drawer ยังเปิด ข้อมูลที่กรอกยังอยู่ | ☐ |

#### TC-GN05 — ยกเลิก/กลับรายการผ่าน confirm · ไม่มี hard delete (FN-91)
- group: General · ความสำคัญ: สูง · trace: FN-91 / BR-16, BR-27 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ร่าง (ปวีณาสร้าง) + ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **⋮** ท้ายแถวใบร่าง / ใบ posted | — | เมนูมี **ยกเลิก** (ร่าง/รออนุมัติ) หรือ **กลับรายการ** (posted) — **ไม่มี** "ลบถาวร / Delete" | ☐ |
| 2 | CLICK **ยกเลิก** (ใบร่าง) → กรอกเหตุผล → ยืนยัน | เหตุผลใด ๆ | confirm **"ยกเลิกใบปรับยอด \<code\>?"** → toast **"ยกเลิก \<code\> แล้ว"** · ใบยัง**อยู่ในระบบ** สถานะ **ยกเลิก** (ไม่หาย · append-only) | ☐ |

#### TC-GN06 — กันกดส่งรัว (double-submit guard · FN-92 · EC-02)
- group: General · ความสำคัญ: กลาง · trace: FN-92 / EC-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=— (กรอกใบครบพร้อมส่ง)
- Start: OPEN `#/create` → กรอกครบทุก step → step 5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** (แล้วรีบกดซ้ำทันที) | — | ปุ่มขึ้น spinner **"กำลังส่ง…"** + **disabled** ระหว่างส่ง → กดซ้ำไม่ทำงาน (ส่งครั้งเดียว · ออกเลขใบเดียว) | ☐ |

#### TC-GN07 — อนุมัติพร้อมกัน (EC-01 · concurrent) `(ต้อง simulate)`
- group: General · ความสำคัญ: ต่ำ · trace: EC-01 / ERR_STALE_DATA · actor: ผู้อนุมัติ (2 คน)
- Setup: role=ME · seed=ADJ-2026-0003 · files=—
- Start: OPEN `#/view/d3` → tab ลายเซ็น / อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อนุมัติ slot เดียวกันพร้อมกัน 2 session | — | prototype single-user จำลองไม่ได้ → คาดหวังฝั่ง API: คนที่ 2 ได้ 409 ERR_STALE_DATA · **mark BLOCKED** ถ้ากดจริงไม่ได้ | ☐ |

#### TC-GN08 — สิทธิ์ถูกถอนกลางคัน (EC-03) `(ต้อง simulate)`
- group: General · ความสำคัญ: ต่ำ · trace: EC-03 / ERR_PERMISSION_REVOKED · actor: ผู้อนุมัติ
- Setup: role=ME · seed=ADJ-2026-0003 · files=—
- Start: OPEN `#/view/d3` → tab ลายเซ็น / อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ถอนสิทธิ์ระหว่างค้างหน้าอนุมัติ แล้วกดอนุมัติ | — | prototype ไม่มี UI ถอดสิทธิ์ → คาดหวัง re-check ตอน mutation คืน ERR_PERMISSION_REVOKED · **mark BLOCKED** | ☐ |

### กลุ่ม XT — Cross-module (§6.9)

#### TC-XT01 — post ใบ + → Inventory ledger ยอดเพิ่ม (XT-01 · R17)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-01 / AC-20 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved · มีบรรทัดปรับเพิ่ม) · files=— · seed ปลายทาง=ยอดคงเหลือ bin ก่อน post `(ต้อง simulate downstream)`
- Start: OPEN `#/view/d11`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดยอด ผลต่างบรรทัดปรับเพิ่ม | — | บันทึกยอด ณ สร้าง + ผลต่าง (อ้างใน step ถัดไป) | ☐ |
| 2 | CLICK **ผ่านรายการ** → ยืนยัน | — | toast **"ผ่านรายการ \<code\> — movement เกิดแล้ว · JE รอลงบัญชี"** · tab ประวัติมี movement **ปรับเพิ่ม** | ☐ |
| 3 | VERIFY ledger ปลายทาง | — | ยอดคงเหลือ bin เพิ่มตามผลต่าง (เห็นในช่องยอดระบบใบถัดไป) — ถ้า prototype ไม่มีหน้า Inventory → **mark (ต้อง simulate)** เช็คจาก movement แทน | ☐ |

#### TC-XT02 — post → GL/JE รอลงบัญชี ไม่ post จริง (XT-02 · BR-19)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-02 / BR-19 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1` → tab ประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY JE บน movement | — | `je_status` = pill **"รอลงบัญชี"** + ป้าย **"FWD-WIRE: JE posting"** · **ไม่มี** การ post GL จริง (mock) | ☐ |

#### TC-XT03 — post → ENG-NOTIFY adj_posted (XT-03) `(ต้อง simulate)`
- group: Cross-module · ความสำคัญ: ต่ำ · trace: XT-03 / §6.5 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0011 (approved) · files=—
- Start: OPEN `#/view/d11`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ผ่านรายการ** → ยืนยัน | — | ต้นทาง: toast **"ผ่านรายการ \<code\> — movement เกิดแล้ว · JE รอลงบัญชี"** · event `adj_posted` ยิงถึงผู้จัดทำ+หน.คลัง+บัญชี — **(ต้อง simulate)** ไม่มี Notification Center ใน prototype | ☐ |

#### TC-XT04 — post damage → NOTIFY + CSQ writeoff (XT-04) `(ต้อง simulate)`
- group: Cross-module · ความสำคัญ: ต่ำ · trace: XT-04 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบ damage approved (ประเภทตัดจำหน่ายของเสีย · แนบหลักฐานแล้ว) · files=`evidence-damage-01.pdf`
- Start: OPEN view ของใบ damage

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ผ่านรายการ** → ยืนยัน | — | ต้นทาง post สำเร็จ (movement ปรับลด) · event `adj_writeoff_posted` (NTF) + CSQ EC `adj_writeoff_posted` — **(ต้อง simulate)** เช็คจาก movement + ประเภทใบ | ☐ |

#### TC-XT05 — post ใบผสม → 7C CSQ +/− (XT-05) `(ต้อง simulate)`
- group: Cross-module · ความสำคัญ: ต่ำ · trace: XT-05 / AC-05 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบผสม + และ − (approved) · files=—
- Start: OPEN view ใบผสม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ผ่านรายการ** → tab ประวัติ | — | มี movement ทั้ง **ปรับเพิ่ม** และ **ปรับลด** · event `adj_posted_increase` + `adj_posted_decrease` (EC actual, basis computed) — **(ต้อง simulate)** ฝั่ง 7C | ☐ |

#### TC-XT06 — กลับรายการ (post ใบกลับ) → ledger + CSQ reversed (XT-06)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-06 / BR-17.1 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0008 (posted · isReversal ของ 0007) · files=—
- Start: OPEN `#/view/d8` → tab ประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY movement ใบกลับ | — | movement **ทิศตรงข้าม** ต้นฉบับ (กลับรายการปรับเพิ่ม/ปรับลด) · ต้นฉบับ ADJ-2026-0007 = **กลับรายการแล้ว** · CSQ `adj_reversed` (avoided) — **(ต้อง simulate)** ฝั่ง CSQ | ☐ |

#### TC-XT07 — ยกเลิก → NOTIFY + ไม่มี movement (XT-07)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-07 / BR-27 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0006 (cancelled) · files=—
- Start: OPEN view ของ ADJ-2026-0006

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **ประวัติ** → VERIFY | — | ใบยกเลิก **ไม่มี** ตาราง Movement (ยกเลิกก่อน post = ไม่กระทบสต๊อก) · event `adj_cancelled` (NTF) + CSQ no-effect — **(ต้อง simulate)** ฝั่ง NOTIFY | ☐ |

#### TC-XT08 — submit abs สูง → NOTIFY FYI (XT-08) `(ต้อง simulate)`
- group: Cross-module · ความสำคัญ: ต่ำ · trace: XT-08 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=— (สร้างใบ Σ|มูลค่า| สูง)
- Start: OPEN `#/create` → กรอกชุด C (สูง ≥20,000) → ส่งอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ส่งอนุมัติใบมูลค่าสูง | ชุด C | event `adj_high_value_submitted` ถึงบัญชี+ผจก.คลัง (FYI ไม่ใช่ approval) — **(ต้อง simulate)** · ต้นทางเช็คจาก toast "ส่ง \<code\> เพื่ออนุมัติแล้ว" | ☐ |

#### TC-XT09 — submit → DOA resolve steps ตาม abs (XT-09)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-09 / AC-11 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY จำนวน slot ตาม Σ|มูลค่า| | ชุด A vs C | จำนวนชั้นเปลี่ยนตามมูลค่า (จุดตัด 20,000/200,000/1,000,000) · slot มาจาก DOA engine (`doaTiers`) — feature ไม่ประกาศซ้ำ | ☐ |

#### TC-XT10 — submit → ENG-DOC-NUM ออกเลข immutable (XT-10 · BR-21)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-10 / BR-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → กรอกครบ → step 5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | ชุด A | ออกเลข **ADJ-2026-NNNN** (ค.ศ.) · toast "ส่ง \<code\> เพื่ออนุมัติแล้ว" | ☐ |
| 2 | OPEN ใบที่เพิ่งส่ง → VERIFY เลข | — | เลขที่คงที่ (immutable) · แก้ไม่ได้ · ใบกลับรายการจะได้เลขใหม่ (ไม่ซ้ำ) | ☐ |

#### TC-XT11 — อ้างใบนับ → Count Doc display-only (XT-11 · FN-52)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-11 / BR-26 / AC-24 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 (source=count · ref CNT-2026-0012) · files=—
- Start: OPEN `#/view/d3`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY "ใบนับต้นเรื่อง" ในหน้ารายละเอียด | — | แสดง **CNT-2026-0012** (F084) · CLICK → **"อ้างอิงใบนับ CNT-2026-0012 — แสดงผล ไม่เปิดหน้าใบนับ"** (display-only · ไม่เปิดหน้า F084/F086) | ☐ |

### กลุ่ม SL — Scope Lock verify (07_LOCKED §7.0 · LOCK-01..10)

#### TC-SL01 — Pattern Q 4 surface + B2 v2 (LOCK-01)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-01 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไล่ surface | — | มีครบ 4 surface: **list** (`#/list`) · **wizard create** (`#/create` · 5 steps) · **view drawer** (`#/view/:id` · 4 tabs) · line editor **B2 v2** (step 2) | ☐ |

#### TC-SL02 — เหตุผลบังคับ + DOA ตามมูลค่า · ไม่มี cycle count (LOCK-02)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-02 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เหตุผล + DOA + ไม่มีนับ | — | step 3 บังคับเลือกเหตุผลทุกบรรทัด · step 4 ชั้น DOA ตาม Σ|มูลค่า| · **ไม่มี** ฟังก์ชันนับสต๊อก/cycle count (ดู TC-NG02) | ☐ |

#### TC-SL03 — +/− เท่านั้น · movement single-bin (LOCK-03)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-03 / BR-05 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทิศ + โครงบรรทัด | — | ผลต่างเป็น **+ (ปรับเพิ่ม)** หรือ **− (ปรับลด)** เท่านั้น · แต่ละบรรทัด **1 bin** (ไม่มี from→to · ดู TC-NG03) | ☐ |

#### TC-SL04 — DOA slot คนจริง ห้าม role ID (LOCK-04)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-04 / FN-42 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0003 · files=—
- Start: OPEN `#/create` → step 4 · และ OPEN `#/view/d3` → tab ลายเซ็น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY slot picker (step 4) + sign tab | — | ทุก slot เป็น **การ์ดคนจริง** (ชื่อ + ตำแหน่ง) · picker ตัด ปวีณา (ME · SoD) ออก · ไม่มีที่ไหนใช้ role ID (WH_LEAD ฯลฯ) แทนคน | ☐ |

#### TC-SL05 — เลข ADJ-YYYY-NNNN ออกตอนส่ง ห้าม format เอง (LOCK-05)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-05 / BR-21 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เลขก่อน/หลังส่ง | — | ร่าง = **"(ร่าง — ยังไม่ออกเลขที่)"** disabled · ส่งอนุมัติ → **ADJ-2026-NNNN** (ค.ศ.) จาก ENG-DOC-NUM · ไม่มีช่องให้ผู้ใช้ตั้ง format เอง (ดู TC-NG05) | ☐ |

#### TC-SL06 — movement append-only · post แล้ว reversal เท่านั้น (LOCK-06)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-06 / BR-16, BR-17 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แก้ใบ posted | — | ใบ posted **ไม่มี** ปุ่มแก้/ยกเลิก · มีแต่ **กลับรายการ** · movement ในประวัติ append-only (ดู TC-NG08) | ☐ |

#### TC-SL07 — location จาก Putaway · in-transit ห้ามแตะ (LOCK-07)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-07 / BR-13 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/create` → step 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY bin source | — | bin ที่เลือกได้เป็น location จาก Putaway (storage/staging/QA/DM) · in-transit **TR-*** ถูกกันออกจาก picker (ดู TC-NG01) | ☐ |

#### TC-SL08 — JE mock FWD-WIRE ห้าม post จริง (LOCK-08)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-08 / BR-19 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ADJ-2026-0001 (posted) · files=—
- Start: OPEN `#/view/d1` → tab ประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY JE marker | — | JE = pill **"รอลงบัญชี"** + ป้าย **"FWD-WIRE: JE posting"** (demo marker) · ไม่มีการ post GL จริง · ไม่มีปุ่มลงบัญชี | ☐ |

#### TC-SL09 — soft-ref nullable ไม่ FK (LOCK-09)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-09 / BR-22, EC-07 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=ใบที่สินค้าถูก archive หลังสร้าง · files=—
- Start: OPEN view ใบนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY สินค้า archive | — | ใบยังแสดง **ข้อความ/ชื่อสินค้าเดิม (snapshot)** + ป้าย "ข้อมูลอ้างอิงถูกยกเลิก" · ไม่พัง (soft-ref nullable ไม่ hard FK · ดู TC-V05) | ☐ |

#### TC-SL10 — CI Warm Light · ปี ค.ศ. · sidebar module map (LOCK-10)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK-10 / FN-38, FN-50 · actor: หัวหน้าคลัง
- Setup: role=ME · seed=— · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY CI + วันที่ + sidebar | — | ธีม Warm Light (พื้นสว่าง) · ทุกวันที่ ค.ศ. (ดู TC-GN01) · sidebar 4 เมนูตาม module map เมนูเดียว active (ดู TC-NG09) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิดไฟล์ `outputs/F-WH-STKADJ/F-WH-STKADJ.html` ใน browser → route เริ่มที่ `#/list`.
2. รันเคสตามลำดับ group (L → W1..W5 → V → AP → PO → CX → RV → PD → HS → NG → GN → XT → SL). ก่อนเคสใหม่ที่ต้อง seed สะอาด: **refresh หน้า** เพื่อคืน seed เดิม (mock in-memory ไม่มี backend).
3. ทุก Start route เป็น hash เปิดตรงได้ (refresh-safe). ยึด **ข้อความบนจอ verbatim** ตาม Expected.
4. ผู้ใช้ตายตัว = ปวีณา สุขทวี (หัวหน้าคลัง · ME). เคส permission/SoD/concurrent ที่ต้องเป็นคนอื่น → ทำเท่าที่ UI เปิด แล้ว **mark `(ต้อง simulate)` / BLOCKED**.
5. กรอกผล `☐` → pass/fail/blocked ต่อ step; เก็บ `evidence` ตอน fail/blocked (ข้อความจริงที่เห็น). สรุปลง Result Report schema ท้ายไฟล์.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST) | **55 / 55** |
| Acceptance Criteria (AC-01..26) | 26 / 26 |
| Business Rules (BR-01..27 · +BR-17.1) | 28 / 28 |
| Field Validation (VR-01..15) | 15 / 15 |
| Edge Cases (EC-01..07) | 7 / 7 (EC-01/03 = simulate → BLOCKED บน prototype) |
| Error Catalog (ที่สังเกตบน UI ได้) | ครบ (2 ตัว simulate) |
| Permission cells (single-user ตรวจได้) | ครบเท่าที่ UI เปิด (role อื่น = simulate) |
| Cross-Module (XT-01..11) | **11 / 11** (downstream หลายตัว = simulate) |
| Scope Lock (LOCK-01..10) | **10 / 10** |
| Negative หมวด 7 (NEG-01..09) | **9 / 9** (+ NG10 เสริม) |
| Cross-cutting / states / events | ครบ |

- Cross-Module (XT): **11 / 11**
- Scope Lock (LOCK): **10 / 10**
- FN cross-check: **✅ 55 / 55** (ทุก FN มี ≥1 TC · หมวด 7 negative render-and-assert-absent ที่ TC-NG01..NG10)
- **Manifest cross-check (FRD §0.12 / 06_TESTS): ✅** — ทุก AC/XT/NEG/LOCK มีคู่ในเคส
- **จำนวนเคสรวม: 116 เคส** (17 group)

### ข้าม / จำกัดด้วย prototype (พร้อมเหตุผล)
- **EC-01 concurrent (TC-GN07)** · **EC-03 permission revoked (TC-GN08)** — prototype single-user ไม่มี multi-session/ถอดสิทธิ์ → `(ต้อง simulate)` · mark **BLOCKED** เมื่อกดจริงไม่ได้ (ต้องทดสอบชั้น API).
- **role อื่น read-only (บัญชี/auditor)** — สลับ login ไม่ได้ → ข้าม UI · ยืนยันผ่าน Audit/§5.3.
- **XT downstream (Inventory ledger / GL / NOTIFY / CSQ / DOA engine)** — prototype ไม่มีหน้า module ปลายทาง → เช็คจาก event/toast/สถานะฝั่งต้นทาง + `(ต้อง simulate)`.
- **empty state "ยังไม่มีใบปรับยอด" (TC-L04 step 3)** — seed มีใบเสมอ → BLOCKED ถ้าล้าง seed ไม่ได้.
- ไม่มีรายการที่ "นอกขอบเขตใบเซ็น" ถูกสร้างเป็นเคส (Exclusions ถูกพิสูจน์เป็น negative หมวด NG แทน).

---

## Result Report (schema)

```json
{
  "feature_id": "F-WH-STKADJ",
  "run_at": "<iso datetime · ค.ศ.>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 116, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ error จริง, route ที่ค้าง, สิ่งที่แสดงแทน Expected) — ช่วย triage โดยไม่ต้องรันซ้ำ. เคส `(ต้อง simulate)` / BLOCKED ให้ note ว่าติดข้อจำกัด prototype ข้อใด.
