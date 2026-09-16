# 06_TESTS — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + DoD + Cross-Module + Negative + Microcopy-aware expected text
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + FUNCTION_CHECKLIST 55 FN
> **⭐ Expected text:** ยึด **ข้อความจริงบนจอ (verbatim จาก HTML)** ก่อน — ดู §6.10 · ปี ค.ศ. ล้วน

---

## §6.1 Acceptance Criteria (AC)

### AC-01: List + filter + KPI (FN-26, FN-90)
**Given** ผู้ใช้ role หัวหน้าคลัง มีใบหลายสถานะ **When** GET list + filter สถานะ=รออนุมัติ **Then** 200 คืนเฉพาะ pending + KPI 4 การ์ด · empty filtered แสดง "ไม่พบรายการที่ค้นหา"

### AC-02: สร้าง + บันทึกร่าง (FN-19)
**Given** เลือกคลัง+วันที่+ประเภท **When** บันทึกร่าง **Then** status=draft · **adj_no = null** · แสดง "(ร่าง — ยังไม่ออกเลขที่)" · ไม่กระทบสต๊อก · toast "บันทึกร่างแล้ว"

### AC-03: ผลต่าง + / − + มูลค่า (FN-04, FN-05, FN-06)
**Given** ยอดระบบ 180 **When** กรอกยอดที่ถูกต้อง 195 **Then** ผลต่าง = +15 (ชิปเขียว) · มูลค่า = +97.50 (15×6.50) · กรอก 156 → −24 (ชิปแดง)

### AC-04: สลับโหมดกรอก (FN-07)
**When** สลับ "ระบุยอดที่ถูกต้อง" ↔ "ระบุจำนวนที่ปรับ" **Then** ตัวเลขแปลงกลับไปมาถูกต้อง (migrateLine)

### AC-05: totals Σ ค่าสัมบูรณ์ vs สุทธิ (FN-08, FN-43)
**Given** ใบผสม + และ − (เช่น +4,600 · −1,275 · −15,600 · +2,100) **Then** footer แสดง Σ ค่าสัมบูรณ์ = 23,575 (ฐาน DOA) และ สุทธิ = −10,175 แยกกันชัด · ใบสุทธิ≈0 ยังต้องอนุมัติชั้นตามค่าสัมบูรณ์

### AC-06: ผลต่าง = 0 บล็อก (FN-11)
**When** กรอกยอดที่ถูกต้อง = ยอดระบบ **Then** ส่งไม่ได้ · toast "บรรทัด <bin> ผลต่าง = 0 — ให้ลบบรรทัดหรือแก้ยอด (BR-02)"

### AC-07: ปรับลดติดลบ บล็อก (FN-12)
**When** ปรับลด > ยอดคงเหลือ **Then** บล็อก · toast "บรรทัด <bin> ยอดหลังปรับติดลบ — คงเหลือ <n> (BR-03)" · inline "ยอดหลังปรับติดลบ (คงเหลือ <n>)"

### AC-08: คู่ (bin,สินค้า) ซ้ำ (FN-10)
**When** ใส่คู่ซ้ำ **Then** toast "คู่ (bin, สินค้า) ซ้ำ: <bin> · <ชื่อสินค้า> (BR-01)" + ชี้บรรทัดเดิม

### AC-09: เหตุผลบังคับ + ตรงทิศ + อื่นๆ (FN-18, FN-37, FN-40)
**When** ส่งโดยมีบรรทัดว่างเหตุผล **Then** toast "บรรทัด <bin> ยังไม่เลือกเหตุผล (BR-06)" · dropdown เหตุผลกรองตามทิศ (บรรทัด + ไม่เห็นกลุ่มลด) · เลือก "อื่น ๆ" ไม่พิมพ์คำอธิบาย → "เหตุผล \"<name>\" ต้องพิมพ์คำอธิบายเพิ่ม (BR-06)"

### AC-10: เหตุผลรวมของใบ (FN-41)
**When** เลือกเหตุผลรวม + กด "เติมทุกบรรทัดที่ว่าง" **Then** เติมบรรทัดว่าง · toast "เติมเหตุผลให้บรรทัดที่ยังว่างแล้ว" · แก้รายบรรทัดต่อได้

### AC-11: DOA ตามมูลค่า + ชั้น (FN-14, FN-15, FN-16)
**Given** Σ|มูลค่า| = 15,000 **Then** 1 ชั้น (หัวหน้าคลัง) · =150,000 → 2 ชั้น (+ผจก.คลัง) · =500,000 → 3 ชั้น (+ผจก.บัญชี) · >1,000,000 → 4 ชั้น (+ผอ.สายงาน) — จุดตัด 20,000/200,000/1,000,000

### AC-12: slot ต้องคนจริง (FN-17, FN-42)
**When** ส่งอนุมัติโดยมี slot ว่าง **Then** ส่งไม่ได้ · toast "เลือกผู้อนุมัติให้ครบทุกขั้น (BR-10)" · inline "เลือกผู้อนุมัติขั้นนี้" · ไม่มีที่ไหนใช้ role ID แทนคน

### AC-13: ส่งอนุมัติ ออกเลขที่ (FN-20)
**When** ส่งอนุมัติสำเร็จ **Then** adj_no = ADJ-YYYY-NNNN (ค.ศ.) จาก ENG-DOC-NUM · status pending · toast "ส่ง <code> เพื่ออนุมัติแล้ว" · แจ้ง slot แรก

### AC-14: อนุมัติหลายชั้น + SoD (FN-21, FN-28)
**When** ผู้อนุมัติ slot กดอนุมัติ **Then** ไป slot ถัดไป (toast "อนุมัติขั้น <n> แล้ว — ส่งต่อ <assignee>") · ครบ → "อนุมัติครบทุกขั้น — สถานะ \"อนุมัติแล้ว\" · กด \"ผ่านรายการ\" เพื่อโพสต์" · **ผู้จัดทำอนุมัติใบตัวเองไม่ได้** (ERR_SOD_SELF_APPROVAL) · tab ลายเซ็นแสดงการ์ดผู้อนุมัติจริง เรียงตามชั้น

### AC-15: ตีกลับ (FN-22)
**When** ตีกลับ + เหตุผล **Then** status draft (returned) · toast "ตีกลับ <code> เพื่อแก้ไข" · ประวัติเก็บรอบตีกลับ · ว่างเหตุผล → "กรุณาระบุเหตุผล"

### AC-16: ผ่านรายการเฉพาะ approved (FN-23)
**When** กด "ผ่านรายการ" ตอน draft **Then** "ผ่านรายการได้เฉพาะสถานะ \"อนุมัติแล้ว\" (BR-08)" · approved → post สำเร็จ · toast "ผ่านรายการ <code> — movement เกิดแล้ว · JE รอลงบัญชี"

### AC-17: ยกเลิกเฉพาะ ร่าง/รออนุมัติ (FN-24 · BR-27/FIX-02)
**When** กดยกเลิกใบ approved **Then** ไม่มีปุ่มยกเลิก (ปุ่มโผล่เฉพาะ draft/pending) · ถ้าฝืน API → "ยกเลิกได้เฉพาะใบร่าง/รออนุมัติเท่านั้น" (ERR_CANCEL_NOT_ALLOWED) · ยกเลิก draft/pending → เหตุผลบังคับ → toast "ยกเลิก <code> แล้ว" · ใบยังอยู่

### AC-18: กลับรายการ (FN-25, FN-44 · FIX-03)
**Given** ใบ posted **When** กลับรายการ + เหตุผล **Then** สร้างใบกลับรายการใหม่ status pending · toast "สร้างใบกลับรายการ <code> — รออนุมัติตามมูลค่าก่อนผ่านรายการ" · **ไม่ auto-post** · กลับรายการซ้ำ → "กลับรายการซ้ำไม่ได้ (BR-18)" · post ใบกลับ → movement ทิศตรงข้าม + ต้นฉบับ reversed

### AC-19: BR-15 ตรวจยอดซ้ำก่อน post (FN-27)
**Given** ยอดระบบเปลี่ยนหลัง snapshot **When** กด post **Then** dialog "ยอดระบบเปลี่ยนหลังสร้างบรรทัด" แสดง 2 ยอด (bin·สินค้า / ยอด ณ ตอนสร้าง / ยอดล่าสุด / ผลต่างใหม่) + ปุ่ม "ตีกลับไปแก้" / "คิดจากยอดล่าสุด"

### AC-20: post ผลกระทบครบวง (FN-29, FN-30, FN-45)
**When** post **Then** movement append-only เกิด (tab ประวัติ) · ป้าย `รอลงบัญชี` + `FWD-WIRE: JE posting` (ไม่มีปุ่มลงบัญชีจริง) · **ไม่มีปุ่มลบ/แก้ movement** · คู่ reversal ผูก 2 ทาง

### AC-21: bin picker filter (FN-01, FN-02, FN-03, FN-46)
**When** ประเภท=ปรับยอดกักกัน **Then** picker เหลือ QA-* · ตัดจำหน่าย → DM-* · bin ล็อก → disabled + เหตุผล (เช่น "ล็อกเพื่อตรวจซ่อมชั้นวาง") · quarantine ปรับได้แต่ไม่มีทางย้ายออก storage

### AC-22: PDF + ลายเซ็น (FN-28, FN-34, FN-38)
**When** เปิด tab PDF **Then** A4 portrait: เลขที่ · วันที่ (ค.ศ.) · คลัง · ตาราง 10 cols · totals headline Σ ค่าสัมบูรณ์ · **3 ช่องลายเซ็น** (ผู้จัดทำ/ผู้อนุมัติ/ผู้ผ่านรายการ) · พิมพ์ได้ · ทุกวันที่ ค.ศ.

### AC-23: soft-ref archive (FN-31)
**Given** สินค้าถูก archive หลังสร้างใบ **Then** ใบแสดงข้อความเดิม (snapshot) + ป้าย "ข้อมูลอ้างอิงถูกยกเลิก" ไม่พัง

### AC-24: count-doc trace (FN-52 · BR-26/FIX-04)
**When** แหล่งที่มา="จากใบนับ" ไม่เลือกใบนับ → ส่งไม่ได้ · toast "เลือกใบนับต้นเรื่อง (F084/F086) ก่อน (BR-26)" · เลือกแล้ว → view drawer โชว์ "ใบนับต้นเรื่อง" · คลิก → "อ้างอิงใบนับ <code> — แสดงผล ไม่เปิดหน้าใบนับ" (display-only) · "ปรับตรง" = ไม่บังคับ

### AC-25: เปลี่ยนคลัง/ประเภท ล้างบรรทัด (FN-09)
**When** เปลี่ยนคลัง/ประเภทตอนมีบรรทัด **Then** confirm "เปลี่ยนคลัง"/"เปลี่ยนประเภทการปรับ" body "จะล้าง...บรรทัด ต่อหรือไม่?" ปุ่ม "ล้างและเปลี่ยน" (danger)

### AC-26: แนบหลักฐาน + บังคับ damage (FN-33, FN-51)
**When** ประเภท=ตัดจำหน่ายของเสีย ไม่แนบไฟล์ → ส่งไม่ได้ · toast "ประเภทตัดจำหน่ายของเสีย ต้องแนบหลักฐานอย่างน้อย 1 ไฟล์ (BR-23)" · ไฟล์โผล่ใน "เอกสารแนบ" ที่ landing

---

## §6.2 Test Case Inventory (edge/probe)

| TC | Name | Type | Maps | Priority |
|---|---|---|---|---|
| TC-CC-01 | อนุมัติพร้อมกัน (EC-01) | API stress | AC-14 | P1 |
| TC-ID-01 | Idempotency double-submit (EC-02) | API | AC-13/AC-16 | P0 |
| TC-PR-01 | Permission revoked mid-flight (EC-03) | API | §5.3 | P2 |
| TC-QTY-01 | ยอดเปลี่ยนก่อน post (EC-04/BR-15) | API+UI | AC-19 | P0 |
| TC-DRAFT-01 | Draft resume (EC-05) | UI | AC-02 | P2 |
| TC-REV-01 | Reversal ผ่าน DOA (EC-06/FIX-03) | API | AC-18 | P0 |
| TC-SOFT-01 | soft-ref archive (EC-07) | UI | AC-23 | P2 |
| TC-SOD-01 | ผู้จัดทำอนุมัติเองไม่ได้ | API | AC-14 | P1 |

---

## §6.3 Test Data Setup
ใช้ mock ชุด PREBRIEF §8 / HTML: ADJ-2026-0001..0011 (ครอบทุก scenario) · reason RS-01..RS-99 · warehouses WH-BKK-01/WH-CNX-01/WH-TRN(virtual excluded) · count docs CNT-2026-0012, CNT-2026-0018 (F084), CYC-2026-0031 (F086) · roles: WH_STAFF/WH_LEAD/WH_MGR/FIN_MGR/DIR (ผู้ทดสอบตาม §5.3). Bin ล็อก: B-03-02-B ("ล็อกเพื่อตรวจซ่อมชั้นวาง"). in-transit: TR-BKK-CNX (ต้องไม่โผล่).

---

## §6.4 Definition of Done (DoD)
**Code:** ทุก AC + unit tests · integration (API+DB+Engine) · E2E happy + edge · review approved · security (D-domains) · coverage ≥80% logic
**Docs:** API docs (auto 02_API) · FRD 07 reflects final · CUBIC: ENG-01/02 register (dev hand-off)
**QA:** P0/P1 ผ่าน · ไม่มี P0/P1 bug เปิด · performance §6.6 · **negative FN §6.7 ผ่าน (พิสูจน์ว่า "ไม่มี")**
**Deploy:** migration staging · declarations register (DOA/NTF/CSQ/DOCCFG) · rollback plan

---

## §6.5 WebSocket / Realtime events
| Event | Trigger | Channel | Test |
|---|---|---|---|
| `adj_posted` | post | tenant:approvers/บัญชี | ปรากฏโดยไม่ refresh |
| `adj_qty_drift_on_post` | BR-15 drift | ผู้ post + maker | แจ้งเตือน drift |
> events wire ผ่าน ENG-NOTIFY (NTF_BRIEF) · `doa_pending`/`doa_result` มาจาก DOA engine

## §6.6 Performance (BRD §17.5)
capacity 200 ใบ/วัน · 2,000 บรรทัด/วัน · list < 500ms · post < 1s. SLA: ส่ง→อนุมัติขั้น1 4 ชม.ทำการ · อนุมัติครบ→post 4 ชม.

## §6.7 Negative Test Cases (พิสูจน์ว่า "ไม่มี" — หมวด 7 FUNCTION_CHECKLIST)

| TC | ต้องพิสูจน์ | FN | Expected |
|---|---|---|---|
| NEG-01 | in-transit ไม่โผล่ | FN-32 | ค้น `TR-BKK-CNX`/`TR-` → ไม่เจอ + hint "bin ระหว่างทาง...ไม่แสดงในใบปรับยอด" |
| NEG-02 | ไม่มีนับสต๊อก | FN-35 | ทั้งระบบไม่มีคำ/หน้า/ปุ่ม "ใบนับ/นับรอบ/cycle count/count sheet" (การอ้าง ref_count_doc เป็น display-only ไม่ใช่การนับ) |
| NEG-03 | ไม่มี bin ปลายทาง/ย้าย | FN-36 | ไม่มีช่อง "ย้ายไป" · ค้น "ย้าย" → hint ชี้ Stock Transfer |
| NEG-04 | quarantine ปรับได้ ย้ายออกไม่ได้ | FN-46 | picker quarantine ไม่มี storage เป็นปลายทาง |
| NEG-05 | ไม่มีช่องกรอกเลขเอง/ตั้งเลขรัน | FN-47 | เลขที่ disabled · ไม่มีหน้าตั้งค่าเลขรัน |
| NEG-06 | ไม่มีช่อง threshold/% | FN-48 | ไม่มีหน้าตั้ง threshold (อยู่ NC rules) |
| NEG-07 | ไม่มีคอลัมน์ VAT/ส่วนลด | FN-49 | grid ไม่มีคอลัมน์ VAT (segmented = โหมดกรอก) |
| NEG-08 | ไม่มีปุ่มลบ/แก้ movement | FN-45 | tab ประวัติ append-only ไม่มีปุ่มลบ |
| NEG-09 | sidebar module map | FN-50 | เมนู Warehouse ตาม module map — ไม่มีเมนูที่ feature คิดเอง |

> render จริงแล้ว assert ว่าไม่มีบนจอ (ตาม WF-01 C3.5 — negative หมวด 7 ไม่ใช่ FN-40 แต่กลไกเดียวกัน)

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-02 | API-03 | FN-02, FN-04 | — |
| AC-03/05 | API-04 | FN-03 | ENG-01 |
| AC-09 | API-05 | FN-06 | — |
| AC-13 | API-05 | FN-08 | ENG-01, ENG-DOC-NUM* |
| AC-14 | API-06 | FN-09 | — |
| AC-16/20 | API-09 | FN-12, FN-13 | ENG-02, ENG-CSQ* |
| AC-18 | API-10 | FN-14 | ENG-01, DOA* |
| AC-21 | API-13 | FN-05 | — |
| AC-22 | API-19 | FN-17 | ENG-01 |
> ทุก Function/Engine ใน 03_LOGIC ถูก trace ≥1 AC

## §6.9 Cross-Module Test Cases (จาก BRD §12.1 · PREBRIEF §9)

| XT | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | post ใบ + | Inventory ledger | movement ปรับเพิ่มเกิด · ยอดคงเหลือ bin เพิ่ม · เห็นในช่องยอดระบบใบถัดไป |
| XT-02 | post ใบ | GL/JE (W5) | je_status=`รอลงบัญชี` + `FWD-WIRE: JE posting` · **ไม่ post จริง** |
| XT-03 | post | ENG-NOTIFY | `adj_posted` ยิงถึงผู้จัดทำ+หน.คลัง+บัญชี |
| XT-04 | post type=damage | NOTIFY + CSQ | `adj_writeoff_posted` (NTF) + CSQ EC `adj_writeoff_posted` |
| XT-05 | post ใบผสม | 7C CSQ | `adj_posted_increase` + `adj_posted_decrease` (EC actual, basis computed) |
| XT-06 | กลับรายการ (post ใบกลับ) | ledger + CSQ | movement ทิศตรงข้าม + CSQ `adj_reversed` (avoided) · ต้นฉบับ reversed |
| XT-07 | ยกเลิก (ร่าง/รออนุมัติ) | NOTIFY + CSQ | `adj_cancelled` (NTF) + CSQ no-effect · **ไม่มี movement** |
| XT-08 | submit abs สูง | NOTIFY | `adj_high_value_submitted` ถึงบัญชี+ผจก.คลัง (FYI ไม่ใช่ approval) |
| XT-09 | submit | DOA (F-DLG-001) | resolve steps ตาม abs → doa_pending (engine) — feature ไม่ประกาศซ้ำ |
| XT-10 | submit | ENG-DOC-NUM | ออกเลข ADJ-YYYY-NNNN (ค.ศ.) · immutable · ใบกลับรายการได้เลขใหม่ |
| XT-11 | อ้างใบนับ | Count Doc F084/F086 | ref_count_doc display-only · ไม่เปิดหน้าใบนับ |

## §6.10 Microcopy-Aware Expected Text (verbatim จาก HTML — ห้ามแต่งคำเอง)

**Toasts (สำเร็จ):** "บันทึกร่างแล้ว" · "ส่ง <code> เพื่ออนุมัติแล้ว" · "อนุมัติขั้น <n> แล้ว — ส่งต่อ <assignee>" · "อนุมัติครบทุกขั้น — สถานะ \"อนุมัติแล้ว\" · กด \"ผ่านรายการ\" เพื่อโพสต์" · "ผ่านรายการ <code> — movement เกิดแล้ว · JE รอลงบัญชี" · "ตีกลับ <code> เพื่อแก้ไข" · "ยกเลิก <code> แล้ว" · "สร้างใบกลับรายการ <code> — รออนุมัติตามมูลค่าก่อนผ่านรายการ" · "เติมเหตุผลให้บรรทัดที่ยังว่างแล้ว"
**Toasts (เตือน/บล็อก):** "บรรทัด <bin> ผลต่าง = 0 — ให้ลบบรรทัดหรือแก้ยอด (BR-02)" · "บรรทัด <bin> ยอดหลังปรับติดลบ — คงเหลือ <n> (BR-03)" · "คู่ (bin, สินค้า) ซ้ำ: <bin> · <ชื่อสินค้า> (BR-01)" · "บรรทัด <bin> ยังไม่เลือกเหตุผล (BR-06)" · "เหตุผล <name> ไม่ตรงทิศผลต่าง (BR-07)" · "เหตุผล \"<name>\" ต้องพิมพ์คำอธิบายเพิ่ม (BR-06)" · "ประเภทตัดจำหน่ายของเสีย ต้องแนบหลักฐานอย่างน้อย 1 ไฟล์ (BR-23)" · "เลือกผู้อนุมัติให้ครบทุกขั้น (BR-10)" · "เลือกใบนับต้นเรื่อง (F084/F086) ก่อน (BR-26)" · "ผ่านรายการได้เฉพาะสถานะ \"อนุมัติแล้ว\" (BR-08)" · "ยกเลิกได้เฉพาะใบร่าง/รออนุมัติเท่านั้น" · "กลับรายการซ้ำไม่ได้ (BR-18)" · "กรุณาระบุเหตุผล" · "แก้ไขได้เฉพาะฉบับร่าง"
**ปุ่ม:** `สร้างใบปรับยอด` · `บันทึกร่าง` · `ส่งอนุมัติ` (spinner "กำลังส่ง…") · `ถัดไป` · `กลับ` · `ยกเลิก` · `เพิ่มบรรทัด` · `เติมทุกบรรทัดที่ว่าง` · `แนบเพิ่ม` · `อนุมัติ` · `ตีกลับ` · `ผ่านรายการ` · `กลับรายการ` · `พิมพ์` · `ดาวน์โหลด` · `ปิด` · `ล้างตัวกรอง`
**Confirm/reason dialogs:** cancel title "ยกเลิกใบปรับยอด <code>?" ปุ่ม "ยืนยันยกเลิก" · reverse title "กลับรายการ <code>" ปุ่ม "ยืนยันกลับรายการ" · reject title "ตีกลับ <code> เป็นร่าง" ปุ่ม "ตีกลับ" · post drift title "ยอดระบบเปลี่ยนหลังสร้างบรรทัด" ปุ่ม "ตีกลับไปแก้"/"คิดจากยอดล่าสุด" · post title "ผ่านรายการ <code>?" · เปลี่ยนคลัง "เปลี่ยนคลัง" ปุ่ม "ล้างและเปลี่ยน"
**Status badge:** ร่าง · รออนุมัติ · อนุมัติแล้ว · ผ่านรายการ · ยกเลิก · กลับรายการแล้ว · JE `รอลงบัญชี` · movement `ปรับเพิ่ม`/`ปรับลด`/`กลับรายการปรับเพิ่ม`/`กลับรายการปรับลด`
**Empty:** "ยังไม่มีใบปรับยอด" · "ไม่พบรายการที่ค้นหา" · "ไม่พบ bin ที่ตรงประเภท/คลัง" · "ยังไม่มีเอกสารแนบ"
> ผลลัพธ์: testcase ที่ ai-testcase-md-generator สร้างต่อจะ match หน้าจอจริง 1:1
