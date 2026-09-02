# Iron Rules — ai-testcase-md-generator

กฎที่ห้ามฝ่าฝืนเวลาเขียนไฟล์ test case. ผู้บริโภคปลายทางคือ **AI agent (browser-use / vision)**
ที่อ่าน MD แล้วลงมือทดสอบบนหน้าจอจริง. กฎสองชุดสำคัญสุดคือ **R5 (ไล่ให้ครบ)** กับ
**R11 (audit เชิงตัวเลข)** — สองตัวนี้คือสิ่งที่กันไม่ให้ "เคสขาด".

## R1 — คงรายละเอียดให้ agent (กลับขั้วจาก qa-friendly-html-generator)
qa-friendly *ตัด* ศัพท์เทคนิคเพราะคนอ่าน. ที่นี่ **คง** สิ่งที่ agent ใช้นำทาง:
- **route ที่ต้องไป** (hash route จริง เช่น `#/create`, `#/edit/:id`) ระบุเป็น `Start` ของทุกเคส
- **anchor = ข้อความ/ป้ายที่เห็นบนจอจริง** (ปุ่มเขียนว่าอะไร, ป้ายฟิลด์, หัวข้อ tab, toast)
- error/validation อ้าง **ข้อความจริงที่ระบบแสดง** + (ในวงเล็บ) error code จาก catalog เพื่อ trace

## R2 — anchor ด้วยสิ่งที่เห็น ไม่ใช่ selector ดิบ
agent อ่านหน้าจอ จึงผูกกับ **label/text/บทบาทที่มองเห็น** ("คลิกปุ่ม **เพิ่ม Customer**",
"ช่อง **เลขประจำตัวผู้เสียภาษี**"). ห้าม CSS selector / XPath / JS. element ที่ไม่มีข้อความให้บรรยาย
ตำแหน่งที่มองเห็น ("ไอคอนถังขยะมุมขวาของการ์ดที่อยู่ใบที่ 2").

## R3 — anchor อ่านจากแหล่งจริง ห้ามเดา
ทุกข้อความปุ่ม/ป้าย/หัวข้อ/route/toast ต้องมาจากแหล่งตามลำดับ: **HTML ต้นทาง** → **01_UI** →
**microcopy กลางของ html-generator-v9** (อ่านสดจาก `html-generator-v9/knowledge/microcopy.md`
ทุก session — ห้ามใช้ความจำ; v6 ไม่มี → หา `html-generator-v*` สูงสุด + log) (ข้อความมาตรฐาน:
toast/ปุ่ม/confirm/empty/pill — ไม่ต้องติดธง เพราะเป็น standard ที่ทุก HTML v6 ต้อง comply).
01_UI ขัดกับ HTML → **HTML ชนะ + note drift**. ถ้าทั้ง 3 แหล่งไม่ยืนยัน **อย่าประดิษฐ์** — เขียนเท่าที่
spec บอกแล้วติดธง `⚠ ยืนยัน anchor` ที่ step นั้น เพื่อให้คนตามเช็คกับ UI จริง.

## R4 — Expected ต้องเช็คได้ด้วยตา (machine-verifiable)
ทุก step มี Expected ที่ตัดสิน pass/fail จากสิ่งที่ปรากฏ: ข้อความปรากฏ/หาย, route เปลี่ยนเป็น `#/...`,
ป้ายสถานะ/pill กลายเป็น X, จำนวนแถว, ปุ่ม disable/enable, toast ข้อความ Y, badge ปรากฏ. ห้ามเขียน
ผลลอย ๆ แบบ "บันทึกสำเร็จ" โดยไม่บอกว่า *เห็นอะไร*.

## R5 — ★ ไล่ให้ครบทุก item (Exhaustive Enumeration) — กันเคสขาด
**ก่อนเขียนเคสใด ๆ** ต้องทำ **Coverage Ledger** (ตาราง traceability ใน output) ที่ไล่ทุกสิ่งทดสอบได้
จาก pack ออกมาเป็นรายการ แล้ว map แต่ละรายการเข้ากับ case+step. รายการที่ต้องไล่ให้ครบ — **ทุกตัว**:
- ทุก **FR** ใน 06_TESTS (FR-01..FR-NN) และทุกแถว acceptance (UI/API/DB/Event/Engine/Contract) ในนั้น
- ทุก **business rule** ใน 05_RULES (ทุก R-xxx ทุกหมวด)
- ทุก **edge case** (EC-01..EC-NN)
- ทุก **error code** ใน error catalog
- ทุก **field** ใน validation schema (required / format / length / range / enum / FK / unique / encrypt/mask)
- ทุก **cell** ใน permission matrix (role × field/action → allowed + denied)
- ทุก **cross-cutting acceptance** (RLS/multi-tenant, code-gen, encryption, cascade, masking, ...)
- ทุก **integration event** + payload
- ทุก **state transition** (ถูก + ผิด) จาก state machine
- ทุก **UI state** (loading / empty / filtered-empty / error / loaded / selection)
- ทุก **XT (cross-module test)** ใน 06_TESTS §6.9 (v6) — เคสข้าม module ต้องมี Setup seed ปลายทาง
- ทุก **LOCK (Scope Lock)** จาก 07_LOCKED §7.0 / 00 §0.11 — ทุกข้อยืนยันลูกค้าต้องมีเคส verify

วิธี "แตก 1 รายการ → หลายเคส" ให้ใช้ `references/derivation-playbook.md`. รายการที่ **ไม่ทำเคส**
(เพราะ Out of Scope / Phase 2 / ไม่มีผลที่สังเกตได้บน UI) ต้อง **ยังอยู่ใน Ledger** พร้อมเหตุผล —
ห้ามหายเงียบ.

**★ Ledger-first gate:** ให้ **ออก Coverage Ledger + Coverage Audit (โครงนับ covered/total) ให้เห็นก่อน**
แล้วตรวจว่าครบ *ก่อน* ลงมือเขียนเคสจริงทั้งชุด. ถ้า Ledger ยังมีแถวที่ไม่มี case และไม่มีเหตุผลข้าม
= ยังไม่ผ่าน gate ห้ามเขียนเคสต่อ. การทำแบบนี้ทำให้ "เคสขาด" ถูกจับตั้งแต่ตอนวาง ไม่ใช่ตอนเขียนจบแล้ว.

> หนึ่งเคสครอบได้หลายรายการ (เช่นเคสสร้างบริษัทครอบ R-IDN-01/03 + MISSING_REQUIRED_FIELD ในคนละ step).
> Ledger คือสิ่งที่การันตีว่าไม่มีรายการไหนถูกลืม แม้เคสจะถูกยุบรวม.

## R6 — traceability ในหัวเคส
แต่ละเคส map กลับ FR / rule ID / EC / error code ที่หัวเคส (field `trace:`). เคสที่เพิ่มเองนอก
06_TESTS ให้ทำเครื่องหมาย `(เพิ่มเติม)`.

## R7 — step atomic + เคส independent
1 step = 1 action ที่ agent ทำได้ทันที (เปิด route / คลิก / พิมพ์ / เลือก / toggle / ยืนยัน / สังเกตผล).
ทุกเคสเริ่มด้วย `Start` route ของตัวเอง + Preconditions ชัด — ห้ามพึ่งสถานะค้างจากเคสก่อน (refresh-safe).

## R8 — Data Sets แยก ใช้ค่าจริงกรอกได้ + ไฟล์ทดสอบมีชื่อจริง
ค่าตัวอย่างรวมที่ `## Data Sets` (ฟิลด์ | ค่า) เป็นค่าที่ **กรอกได้จริง** (ทั้งชุดถูก + ชุดผิดสำหรับ
negative). ใน step คอลัมน์ Input อ้างชื่อชุด/ค่าตรง ๆ. อย่าใส่ placeholder ลอย เช่น `<ชื่อ>`.
**ถ้าเคสต้องอัปโหลดไฟล์** (CSV import ฯลฯ) ห้ามเขียนแค่ "ไฟล์ใหญ่เกิน" — ต้องระบุ **ชื่อไฟล์จริง**
(เช่น `too_large.csv`, `with_errors.csv` จาก 06_TESTS §6.6) ในส่วน `### ไฟล์ทดสอบ (Files)` ของ
Data Sets + ใน `Setup:` ของเคส. agent อัปโหลดไฟล์เองไม่ได้ — runner ต้องเตรียมไฟล์ตามชื่อ.

## R9 — pure Markdown ล้วน
ห้ามมีภาพ, base64, HTML, หรือ `<script>`. ไฟล์เดียว เปิดอ่านได้ทุกที่ ไม่มี dependency.

## R10 — มีตารางผล + สคีมารายงานกลับ
ทุก step มีคอลัมน์ `Result` = `☐`. ท้ายไฟล์มี **Result Report (schema)** เป็น JSON compact ให้ agent
กรอกผลกลับ machine-readable (ต่อเคส: id/status/failed_step/note + summary).

## R11 — ★ Coverage Audit gate (เชิงตัวเลข) — ปิดท้ายทุกไฟล์
ก่อนส่ง ต้องมี section `## Coverage Audit` สรุป **นับจริง**: ต่อหมวด (FR / rules / edge cases /
error codes / permission cells / cross-cutting / events / states) = `covered / total` + รายการที่
ข้าม (พร้อมเหตุผล Phase 2/OOS). เป้าหมาย **100%** ของรายการที่อยู่ใน scope. ถ้ายังไม่ครบ = ไฟล์ยัง
ไม่เสร็จ ให้กลับไปเพิ่มเคส. นี่คือด่านกัน"ไม่คลุม".

## R12 — Depth bar (กันไม่ละเอียด)
เคสต้องลึกพอ: happy-flow ที่มีหลาย section (เช่น สร้างลูกค้า) ต้องมี **step ต่อ section/ฟิลด์สำคัญ**
ไม่ยุบเหลือ 2 step. ทุกเคสมี Preconditions + actor/role + "ผ่านเมื่อ" ที่ผูกกับ acceptance ต้นทาง.
negative/edge ระบุชนิดในชื่อเคส เช่น `(negative)`, `(boundary)`, `(permission)`, `(edge: EC-08)`.

## R13 — ★ ทุก Action ขึ้นต้นด้วย verb tag (agent map 1:1 ไม่ต้องตีความ)
คอลัมน์ Action ทุกช่อง **ขึ้นต้นด้วยกริยาแท็กตัวพิมพ์ใหญ่** จากชุดมาตรฐานนี้เท่านั้น แล้วตามด้วย
target ที่เป็น **ข้อความ/ป้ายที่เห็นบนจอ**:
| verb | ความหมาย | รูปแบบ |
|---|---|---|
| `OPEN` | ไปที่ route/หน้า | `OPEN #/create` |
| `CLICK` | คลิกปุ่ม/ลิงก์/ไอคอน/แถว | `CLICK ปุ่ม "เพิ่ม Customer"` |
| `TYPE` | พิมพ์ลงช่อง | `TYPE "0105540012345" → ช่อง "เลขผู้เสียภาษี"` |
| `SELECT` | เลือกค่าใน dropdown | `SELECT "Enterprise" → "customer_group"` |
| `TOGGLE` | สลับ toggle/checkbox | `TOGGLE "ตั้งเป็นจัดส่งหลัก" (การ์ดที่ 2)` |
| `UPLOAD` | เลือกไฟล์ใน file picker | `UPLOAD too_large.csv` |
| `PRESS` | คีย์ลัด | `PRESS Esc` · `PRESS Ctrl+S` |
| `WAIT` | รอ async/anim ก่อนเช็ค (toast/โหลด) | `WAIT จน toast ปรากฏ (≤3s)` |
| `VERIFY` | step สังเกตล้วน (ไม่มี interaction) | `VERIFY แถบ Stats ด้านบน` |
ห้ามเขียน Action ที่ไม่ขึ้นต้นด้วย verb เหล่านี้. ถ้า target ไม่มีข้อความ ให้บรรยายตำแหน่งที่เห็นต่อท้าย
verb ("CLICK ไอคอนถังขยะ ท้ายแถวที่เลือก"). Expected ยังเป็น "สิ่งที่เห็นแล้วเช็คได้" เหมือนเดิม (R4).

## R14 — ★ ทุกเคสมีบรรทัด Setup (role + seed + files) — บอก runner ต้องเตรียมอะไร
หัวเคสต้องมี field **`Setup:`** ระบุเป๊ะว่าก่อนรันต้องเตรียมอะไร เพราะ agent เสกเองไม่ได้:
- **role** = login เป็นบทบาทไหน (เช่น `role=finance`)
- **seed** = ข้อมูลที่ต้องมีอยู่ก่อน (เช่น `ลูกค้า 1 รายมี ≥2 ที่อยู่`, `prospect ที่ convert แล้ว 1 ราย`, `id ของ tenant อื่น`)
- **files** = ไฟล์ทดสอบที่ต้องมี (ชื่อจริง) หรือ `—`
รูปแบบ: `- Setup: role=sales_mgr · seed=ลูกค้า suspended ≥1 · files=—`
ถ้าเคสต้อง simulate สภาพที่กดมือไม่ได้ (network timeout, โมดูลปลายทาง down) ให้ระบุใน Setup ว่า
**ต้อง inject อย่างไร** + mark เคสนั้นว่า `(ต้อง simulate)` เพื่อ runner รู้ว่าอาจ BLOCKED ถ้าทำไม่ได้.

## R15 — ห้าม truncate / pack ใหญ่เขียนทีละ group
output ต้องครบทุกเคสที่ Ledger ระบุ — **ห้ามตัดท้าย, ห้ามใส่ "... (เพิ่มเติมในลักษณะเดียวกัน)"**,
ห้ามลดความละเอียดช่วงท้ายไฟล์ (โมเดลมักหละหลวมตอนใกล้จบ — อย่า). ถ้า Ledger ออกมา **เกิน ~60 เคส**
หรือยาวเกินจะ generate รอบเดียวจบสวย ให้เขียน **ทีละ group ต่อรอบ** (เช่น append ทีละกลุ่ม) จนครบทุก
group ใน Ledger แล้วค่อยปิดด้วย Coverage Audit. เคสกลุ่มท้าย ๆ ต้องลึกเท่ากลุ่มแรก (depth bar R12).

## R16 — ID เสถียรข้ามรอบ (regen ไม่ทำผลเทสเก่าเพี้ยน)
ถ้าเป็นการ **regen จาก pack ที่เคยทำ test case แล้ว** ให้ **คง TC-id เดิมไว้กับเคสเดิม** (อย่าเลื่อนเลข)
เพิ่มเคสใหม่ต่อท้าย id ของ group นั้น (เช่นมี TC-C01..C11 อยู่แล้ว เคสใหม่ = TC-C12). ถ้าจำเป็นต้องลบ
เคส ให้คง id ไว้แล้ว mark `(ยกเลิก — เหตุผล)` แทนการรีนัมเบอร์ เพื่อให้ผลรันเก่าที่ track ด้วย id ยัง
อ้างอิงได้. ใส่หมายเหตุนี้ใน Meta ถ้าเป็น regen.

## R17 — ★ Expected แบบ delta ต้อง capture ค่าตั้งต้นก่อน (กัน "เช็คไม่ได้จริง")
ถ้า Expected เป็นการ **เปรียบเทียบ/ส่วนต่าง** — มีคำว่า *ไม่เปลี่ยน · คืนกลับ · เพิ่ม/ลด · เท่ากับเดิม ·
conserved · ไม่ลดเป็น 0 · มากกว่า/น้อยกว่าก่อนหน้า* — agent ที่อ่านหน้าจอ **ไม่รู้ค่าเดิม** ถ้าไม่ได้จดไว้
ก่อน. ดังนั้นเคสแบบนี้ **ต้องมี step VERIFY ที่ "อ่าน + บันทึกค่าตั้งต้น" มาก่อน** แล้ว Expected ของ step
หลังจึงอ้าง "เทียบกับค่าที่บันทึกไว้ใน step N".

รูปแบบ:
```
| 1 | OPEN … → VERIFY+บันทึก ยอดต้นทาง/ปลายทาง (เช่น ต้นทาง=24, ปลายทาง=0) | — | จดค่าไว้อ้างใน step ถัดไป | ☐ |
| ... | (ทำ action ที่ทำให้ค่าเปลี่ยน) | … | … | ☐ |
| n | VERIFY ยอดอีกครั้ง | — | ต้นทางลดลง = จำนวนที่ย้าย, ปลายทางเพิ่ม = เท่ากัน, **ผลรวม = ค่ารวมที่จดใน step 1** | ☐ |
```
ถ้าค่าตั้งต้นมาจาก seed ให้ระบุค่าที่คาดไว้ใน `Setup:` (เช่น `seed=ต้นทาง on_hand=24`) เพื่อให้ Expected
อ้างเลขจริงได้ — ไม่ใช่ "ไม่เปลี่ยน" ลอย ๆ ที่ตรวจไม่ได้.

## R18 — ★ Scope Lock + Manifest cross-check (v1.1)
- **LOCK ทุกข้อ = ต้องมีเคส verify** (ข้อยืนยันในใบเซ็นคือสัญญา — ถ้าเทสไม่คลุม แปลว่าส่งมอบโดยไม่พิสูจน์)
- **ของนอกขอบเขตใบเซ็น (Exclusions) = ห้ามสร้างเคส** — ลง Ledger เป็นข้าม เหตุผล "นอกขอบเขตใบเซ็น"
  (กันทีม test/dev หลงไปทำสิ่งที่ไม่ได้ขาย)
- **Manifest cross-check:** ก่อนปิด Coverage Audit เทียบ Ledger กับ FRD `00_OVERVIEW §0.12` —
  ทุกแถว manifest ต้องมีคู่ใน Ledger; ไม่มี = Ledger ไม่ครบ ห้ามส่ง. รายงานผลเป็นบรรทัด
  `Manifest cross-check: ✅ N/N` ใน Coverage Audit.
