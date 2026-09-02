# Output format — testset .md

โครงไฟล์ที่ `html_to_md.py` สร้าง (เรียงตามนี้เสมอ):

1. `# Test Suite — <title>` + ย่อหน้านำ (บอกว่าเป็นชุดสำหรับ AI self-test)
2. ตาราง **Meta** — Feature ID, ชื่อ, เวอร์ชัน, จำนวนเคส/หมวด, URL, โหมดที่รองรับ
3. `## Coverage Matrix` — ต่อหมวด: จำนวนเคส + นับตามความสำคัญ (High/Med/Low)
4. `## Data Sets` — ทุกชุดข้อมูล เป็นตาราง `ฟิลด์ | data sample`
5. `## Test Cases` — ต่อเคส:
   - bullet: หมวด / ความสำคัญ / ทดสอบเพื่อ / ผู้ทดสอบ / Preconditions / ชุดข้อมูล / Pass criteria
   - ตารางขั้นตอน:
     - โหมด vision: `# | Action | Input | Expected | Screenshot | Result`
     - โหมด automated (มี --spec): `# | Action | Input | Expected | Setup/Locator | Screenshot | Result`
   - `Result` เป็น `☐` ให้ AI กา; `Screenshot` เป็น `` `regionKey` `` หรือรูป (ถ้า --with-images) หรือ `—`
   - `Setup/Locator` = `setup: <JS>` + `el: <selector|text>` (จาก shot-spec)
6. `## AI Self-Test Protocol` — ขั้นตอน + เกณฑ์ PASS/FAIL
7. `### รูปแบบผลลัพธ์ที่ AI ต้องส่งกลับ` — บล็อก JSON เทมเพลต (summary + results[])
8. `## Appendix — Structured Suite (JSON)` — ทั้ง suite (meta/groups/data/cases) แบบ machine-readable

## หมายเหตุ
- คอลัมน์ `Input` มาจาก `step[1]` (dataText). ถ้าเคสมีชุดข้อมูล ดูค่าจริงเต็มชุดได้ที่ Data Sets
- `Screenshot` regionKey ใช้จับคู่กับภาพในไฟล์ HTML เดิม (หรือไฟล์ที่ export ด้วย --with-images)
- ไม่มี base64 ในไฟล์ .md เด็ดขาด
