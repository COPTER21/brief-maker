# Output format — testcases-<feature>.md

ยึดโครงนี้เป๊ะ (เรียงตามลำดับนี้เสมอ). Markdown ล้วน ไม่มีภาพ/base64/HTML.
สองส่วนที่เพิ่มจากเดิมและสำคัญสุด: **Coverage Ledger** (หลัง Coverage) และ **Coverage Audit** (ก่อน schema).

---

## โครงไฟล์ (ลำดับ)
1. `# AI Test Cases — <feature>` + ย่อหน้านำ
2. `## Meta` — ตาราง: Feature ID, ชื่อ, เวอร์ชัน, App entry, Routes, ที่มา (FRD/BRD/HTML), จำนวนเคส/หมวด
3. `## Coverage` — ต่อ group: จำนวนเคส + ความสำคัญ (สูง/กลาง/ต่ำ)
4. `## Coverage Ledger` — ★ ตาราง traceability: ทุก item จาก pack → case IDs (ดูด้านล่าง)
5. `## Data Sets` — ทุกชุด (ฟิลด์ | ค่า) ทั้งชุดถูกและชุดผิด
6. `## Test Cases` — ราย group → ราย case (หัวเคส + ตาราง step)
7. `## วิธีที่ agent รัน (Run protocol)`
8. `## Coverage Audit` — ★ นับ covered/total ต่อหมวด + รายการที่ข้าม (เหตุผล)
9. `## Result Report (schema)` — JSON ให้ agent กรอกผลกลับ

---

## §A — Coverage Ledger (วางหลัง Coverage)
ตารางไล่ทุกสิ่งทดสอบได้ ออกมา map กับเคส. หนึ่งแถวต่อหนึ่ง item. ทุกแถวต้องมี case ≥1
(หรือ mark ข้ามพร้อมเหตุผล). จัดกลุ่มตามชนิด:

```markdown
## Coverage Ledger
### FR (06_TESTS)
| item | cases |
|---|---|
| FR-01 Create Company | TC-C01, TC-C02, TC-V01 |
| FR-04 Convert (atomic) | TC-CNV01..05 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| R-IDN-01 company→legal_name+tax_id required | TC-C01, TC-C03 |
| R-ADR-08 exactly 1 billing | TC-A04 |
| ... (ทุก R-xxx) | ... |
### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-08 timeout retain form | TC-E08 |
| EC-10 concurrent edit | — ข้าม (Phase 2, ไม่มีผลบน UI) |
### Error Codes
| error | cases |
|---|---|
| INVALID_TAX_ID_FORMAT | TC-C03 |
| CASCADE_VIOLATION | TC-A02 |
| ... (ทุกตัวใน catalog) | ... |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| finance edit credit_limit = allow | TC-P03 |
| finance edit legal_name = deny | TC-P04 |
| ... | ... |
### Cross-Module (XT — 06_TESTS §6.9, v6)
| XT | Downstream | Case |
|---|---|---|
| XT-01 | Budget (release on cancel) | TC-X01 |

### Scope Lock (LOCK — 07 §7.0 / 00 §0.11)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | ... | TC-C03 |

### Cross-cutting / Events / States
| item | cases |
|---|---|
| RLS cross-tenant 404 | TC-X01 |
| event customer.created | TC-C01 (สังเกต toast/ผลปลายทางเท่าที่ UI เห็น) |
| empty state (list) | TC-L05 |
```

---

## §B — Test Case (ต่อเคส)
หัวเคส (bullet) + ตาราง step. **ต้องมี `Setup:`** (R14) และ Action ทุกช่อง **ขึ้นต้น verb tag** (R13):

```markdown
### TC-C01 — สร้างลูกค้านิติบุคคลครบฟิลด์ (happy)
- group: สร้างลูกค้า · ความสำคัญ: สูง · trace: FR-01 / R-IDN-01,03,05 / event customer.created
- actor (role): Sales Rep
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` (หรือ OPEN `#/list` แล้ว CLICK ปุ่ม "เพิ่ม Customer")
- ชุดข้อมูล: A
- ผ่านเมื่อ: บันทึกได้ + toast แสดง customer_code รูปแบบ CUST-YYYYMMDD-XXXX + เด้งกลับ list เห็นแถวใหม่บนสุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` | — | drawer เปิด หัวข้อ **เพิ่ม Customer ใหม่**; ประเภท default = **นิติบุคคล** | ☐ |
| 2 | TYPE → ช่อง **ชื่อนิติบุคคล (legal_name)** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 3 | TYPE → ช่อง **เลขผู้เสียภาษี (tax_id)** | A: 0105540012345 | ช่องแสดง 13 หลัก | ☐ |
| 4 | TYPE → **ผู้ติดต่อหลัก** + **อีเมล** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้าง Customer สำเร็จ — CUST-…** + route = `#/list` | ☐ |
| 6 | VERIFY แถวบนสุดของตาราง | — | เห็นชื่อบริษัทที่เพิ่งสร้าง + pill ประเภท **นิติบุคคล** | ☐ |
```

- **Action** = `verb tag` (OPEN/CLICK/TYPE/SELECT/TOGGLE/UPLOAD/PRESS/WAIT/VERIFY) + target ที่เห็น (R13)
- **Input** = อ้างชุดข้อมูล/ค่า หรือ `—` · **Expected** = สิ่งที่เห็นแล้วเช็คได้ · **Result** = `☐`
- 1 step = 1 action

### §B.1 — Expected แบบ delta + WAIT (R17 + R13)
ถ้าผลคือ "ส่วนต่าง/ไม่เปลี่ยน/คืนกลับ" ต้อง **จดค่าตั้งต้นก่อน** แล้วค่อยเทียบ; toast/async ใช้ `WAIT`:

```markdown
- Setup: role=warehouse_staff · seed=ต้นทาง on_hand=24, ปลายทาง on_hand=0 · files=—
| 1 | OPEN `#/stock/WH-01/sku` → VERIFY+จดยอด | — | บันทึก ต้นทาง=24, ปลายทาง=0, รวมฐาน=24 (อ้างใน step ถัดไป) | ☐ |
| 2 | CLICK **ดำเนินการเสร็จ** | — | (ไปทำ action) | ☐ |
| 3 | WAIT จน toast ปรากฏ | — | toast **… ดำเนินการเสร็จ · ย้าย stock + ปลดล็อกแล้ว** | ☐ |
| 4 | OPEN `#/stock/WH-01/sku` → VERIFY ยอดอีกครั้ง | — | ต้นทาง=20 (ลด 4), ปลายทาง=4 (เพิ่ม 4), **รวมฐาน=24 เท่าค่าที่จดใน step 1** | ☐ |
```
> ห้ามเขียน Expected แบบ "ของรวมไม่เปลี่ยน" โดยไม่มี step จดค่าเดิม — agent เช็คไม่ได้ (R17).

---

## §C — Coverage Audit (ก่อน schema)
```markdown
## Coverage Audit
| หมวด | covered / total |
|---|---|
| FR (06_TESTS) | 10 / 10 |
| Business rules (05_RULES) | 46 / 48 |
| Edge cases | 11 / 15 |
| Error codes | 30 / 34 |
| Permission cells (สำคัญ) | 18 / 18 |
| Cross-cutting / events / states | ครบ |

- Cross-Module (XT): N/N
- Scope Lock (LOCK): N/N
- **Manifest cross-check (FRD §0.12): ✅ N/N**

### ข้าม (พร้อมเหตุผล — Phase 2 / OOS / นอกขอบเขตใบเซ็น)
- R-xxx / EC-10 (concurrent) / CONCURRENT_UPDATE — Phase 2 (optimistic lock ยังไม่ทำ)
- ... (ทุกตัวที่ข้ามต้องมีเหตุผล)
```
> ถ้า covered < total และไม่มีเหตุผล "ข้าม" = ไฟล์ยังไม่เสร็จ ให้กลับไปเพิ่มเคส (Iron Rule R11).

---

## §D — Result Report (schema)
```json
{
  "feature_id": "F-XXX",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-C01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 0, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (เช่น ข้อความ error จริง, route ที่ค้าง, สิ่งที่
> แสดงแทนที่จะเป็น Expected) — ช่วย triage โดยไม่ต้องรันซ้ำ. `note` = หมายเหตุเสริม.

## หมายเหตุการเขียน
- **ออก Coverage Ledger + Audit ให้เห็นก่อน** แล้วเช็คครบ ค่อยเขียนเคสจริง (R5 Ledger-first gate)
- ไม่มีคอลัมน์ selector/JS — agent ใช้สิ่งที่เห็น
- anchor ที่ยืนยันกับ UI ไม่ได้ → ติด `⚠ ยืนยัน anchor`
- เคส negative/edge บอกชนิดในชื่อ เช่น `(negative)`, `(boundary)`, `(permission)`, `(edge: EC-08)`
- ถ้าเป็น **regen** ของ pack เดิม: คง TC-id เดิม, เพิ่มเคสใหม่ต่อท้าย, ลบ = mark `(ยกเลิก)` (R16)
- pack ใหญ่ (>~60 เคส): เขียน/append ทีละ group ห้าม truncate (R15)
