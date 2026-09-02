---
name: qa-html-to-ai-testset
description: >-
  แปลงเอกสารแบบทดสอบ QA-friendly HTML (ผลของ qa-friendly-html-generator) ให้เป็น
  Markdown test set แบบละเอียด ที่ AI อ่านแล้ว "ทดสอบเอง (self-test)" ได้ — ดึง PAYLOAD
  (meta/groups/data/cases) ที่ฝังใน HTML ออกมาเป็น: ตารางทุกเคส (Step | Action | Input |
  Expected | Screenshot | Result), Coverage matrix, Data Sets, AI Self-Test Protocol,
  เทมเพลตผลลัพธ์ JSON ให้ AI กรอก, และ Structured Suite (JSON) ให้ AI parse ตรง ๆ.
  ถ้าแนบ shot-spec.json จะเพิ่มคอลัมน์ Setup(JS)+Locator ให้ AI รัน Playwright อัตโนมัติได้
  (โหมด automated); ถ้าไม่แนบก็เป็นโหมด vision/manual ทำตาม step + ภาพ. ใช้เมื่อ user พูดถึง
  "แปลง html เป็น md test case", "ทำ test case ให้ AI อ่าน", "AI self test", "ให้ AI รันเทสเอง",
  "md ตาราง testcase ละเอียด", "qa-html-to-ai-testset", "เอา html testcase ไปทำ markdown",
  "สร้าง test set ให้ AI", "automated test จาก html". Input: ไฟล์ HTML (ที่มี PAYLOAD).
  Output: ไฟล์ .md เดียว.
---

# qa-html-to-ai-testset

เปลี่ยน "เอกสารทดสอบสำหรับคน" (HTML) → "ชุดทดสอบสำหรับ AI" (Markdown ละเอียด) ที่ AI
อ่านแล้วลงมือทดสอบเอง + รายงานผลกลับมาในรูปแบบมาตรฐานได้.

> สกิลคู่กับ `qa-friendly-html-generator` (ตัวนั้นสร้าง HTML; ตัวนี้ถอดออกมาเป็น MD ให้ AI)

## Input
- **ไฟล์ HTML** ที่สร้างจาก `qa-friendly-html-generator` (มี `const PAYLOAD={...}` ฝังอยู่) — จำเป็น
- **shot-spec.json** (ออปชั่น) — ของฟีเจอร์เดียวกัน เพื่อเติม Setup(JS)+Locator → ปลดล็อกโหมด automated
- รูป base64 ใน HTML ไม่ถูกอ่านเข้า context (อ้างเป็น regionKey; export เป็นไฟล์ได้ด้วย `--with-images`)

## Output — Markdown เดียว ประกอบด้วย
1. **Meta + Coverage Matrix** (หมวด × จำนวนเคส × ระดับความสำคัญ)
2. **Data Sets** — ทุกชุด (ฟิลด์/ค่า)
3. **Test Cases** รายเคส:
   - Preconditions / Why / Who / Pass criteria / ชุดข้อมูล
   - ตาราง `# | Action | Input | Expected | [Setup/Locator] | Screenshot | Result`
4. **AI Self-Test Protocol** — ขั้นตอนให้ AI ทำ + เกณฑ์ตัดสิน PASS/FAIL
5. **เทมเพลตผลลัพธ์ (JSON)** — โครงให้ AI กรอกผลกลับ
6. **Appendix: Structured Suite (JSON)** — ทั้ง suite แบบ machine-readable (ไม่รวม base64)

## วิธีใช้
```bash
# โหมด vision/manual (HTML อย่างเดียว)
python scripts/html_to_md.py --html testcase-F-91.html --out testset-F-91.md

# โหมด automated (เติม locator/JS จาก shot-spec ของฟีเจอร์เดียวกัน)
python scripts/html_to_md.py --html testcase-F-91.html --out testset-F-91.md \
  --spec shot-spec.json --app-url "opproc-sow.html#/sow"

# ส่งออกรูปประกอบให้ vision AI ดูด้วย
python scripts/html_to_md.py --html testcase-F-91.html --out testset-F-91.md --with-images
```

## โหมดการทดสอบของ AI
- **Vision / Manual** — AI เปิดแอปจริง อ่าน *Action* ทำตามทีละขั้น (ดู Screenshot ประกอบ) เทียบ *Expected*
- **Automated** — มี `--spec`: ตารางจะมี `setup` (JS ไปยังหน้าจอ) + `el` (selector/ข้อความ)
  AI ที่มี Playwright/computer-use รันได้ตรง ๆ

## หลักการ (สำคัญ)
- เอกสารนี้ "ใส่รายละเอียดเทคนิคกลับ" (locator/JS/regionKey) ตรงข้ามกับ HTML ฉบับคนที่ตัดออก —
  เพราะผู้บริโภคคือ **AI** ไม่ใช่ผู้ใช้ทั่วไป
- engine แค่ **ถอด+จัดรูป** จาก PAYLOAD ไม่แต่งเนื้อหาเพิ่ม (เนื้อหามาจาก cases.json เดิม)
- **ห้ามอ่านไฟล์ HTML ดิบทั้งไฟล์เข้า context** (มี base64 ใหญ่) — ใช้ `html_to_md.py` ถอดให้
  แล้วอ่าน **เฉพาะ .md** ที่ได้ (ไม่มี base64)

## ไฟล์ในสกิล
```
scripts/html_to_md.py     # engine: extract PAYLOAD -> MD (+ optional spec/images)
references/output-format.md  ai-runner-guide.md
examples/testset-F-91.md  # ตัวอย่าง MD ที่ได้จาก F-91 (โหมด automated)
```
