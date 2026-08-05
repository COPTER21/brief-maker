# WF-01 Pipeline SkillSet — 2BSimple / CUBE 4.0

ชุด Skill 7 ตัวสำหรับสาย HTML-first pipeline (WF-01) ตั้งแต่สร้าง prototype → ตรวจคุณภาพ → เขียนเอกสาร → ทำ test case ครบวงจร แพ็คไว้ให้ทีมเอาไปติดตั้งใช้ต่อ

---

## 📦 Skill ในแพ็คนี้ (7 ตัว)

| # | Skill | Version | หน้าที่ |
|---|-------|---------|---------|
| 1 | **html-generator-v7** | v7.0 Warm Light | สร้าง Production-Ready HTML Prototype จาก input อะไรก็ได้ (FRD/Brief/BRD/screenshot/text) — Patterns A–O + B2 Line Editor + Iron Rules #1–94 |
| 2 | **qc-ux-html-checker** | v3.13 | Quality Gate — ตรวจ HTML ว่า "ทำถูกมั้ย" เชิง form (iron rules, CI, component, UX heuristics) → `_UX_CHECK_REPORT.md` |
| 3 | **qc-coverage-checker** | v1.0 | Quality Gate — ตรวจ HTML ว่า "ทำครบมั้ย" เชิง business scope เทียบ workflow graph → `_COVERAGE_REPORT.md` |
| 4 | **brd-generator-full** | v2.2 HTML-first | สร้าง BRD ฉบับสมบูรณ์จาก RIF + HTML (Draft→Enrich→Flexibility→Data Entity→VS Impact→Quality Gate) |
| 5 | **frd-generator-v6** | v6.1 HTML-first | สร้าง FRD Pack แยกไฟล์ตาม layer (UI/API/LOGIC/DB/Rules/Tests) — CUBIC 3-layer + traceability |
| 6 | **ai-testcase-md-generator** | v1.2 | เขียน Test Case ละเอียดเป็น Markdown ให้ AI agent (browser-use/vision) รันเอง — anchor ด้วยข้อความบนจอ |
| 7 | **qa-friendly-html-generator** | v2.2 Warm Light | สร้างเอกสารแบบทดสอบฉบับผู้ใช้ (QA-friendly HTML) — end-user ทดสอบตามได้ + บันทึกผล + export PDF |

---

## 🔄 Pipeline Flow (WF-01 HTML-first)

```
RIF (requirement-intake-formatter)
        │
        ▼
[1] html-generator-v7 ──────────────►  HTML Prototype
        │
        ├──►  [2] qc-ux-html-checker      (gate: ทำถูกมั้ย)
        └──►  [3] qc-coverage-checker     (gate: ทำครบมั้ย)
        │            (PASS ทั้งคู่ค่อยไปต่อ)
        ▼
[4] brd-generator-full ─────────────►  BRD (.md + .docx)
        │
        ▼
[5] frd-generator-v6 ───────────────►  FRD Pack (6–9 ไฟล์)
        │
        ▼
[6] ai-testcase-md-generator ───────►  testcases-*.md (AI self-test)
        │
        ▼
[7] qa-friendly-html-generator ─────►  UAT HTML (คนทดสอบ)
```

> **ลำดับตรวจ:** หลัง gen HTML ต้องผ่าน **qc-ux** + **qc-coverage** ก่อนเสมอ ค่อยเข้าเอกสาร
> **Version pin:** อ้างอิง `cube-master-knowledge/knowledge/04_skills/workflow-master-wf01-06.md`

---

## ⚙️ วิธีติดตั้ง (Claude Skills)

1. แตก zip นี้ออกมา — จะได้ 7 โฟลเดอร์ (แต่ละโฟลเดอร์มี `SKILL.md` + resources)
2. วางแต่ละโฟลเดอร์ไว้ใน skills directory ของเครื่อง/บัญชีที่จะใช้
3. แต่ละ skill trigger ด้วยชื่อ skill หรือ keyword ที่ระบุใน `description` ของ `SKILL.md`
4. ไม่ต้องแก้ path — resources ทุกตัวอ้างอิงแบบ relative ในโฟลเดอร์ตัวเอง

---

## 📝 หมายเหตุ

- แพ็คนี้เป็นทรัพย์สินร่วมของทีม 2BSimple (shared knowledge base)
- Skill 1,7 ใช้ CI **CUBE Warm Light** (Ivory #FAF8F5 / Charcoal #111111 / Red #FF3B30 / Orange #FF9A1F)
- BRD/FRD chain รับ HTML จาก html-generator เป็น input ร่วม (HTML-first) — แนะนำให้รันตามลำดับ pipeline

_Exported: 2026-08-04_
