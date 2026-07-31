# CUBE Skill Bundle — HTML/FRD/QA/Doc Chain

Export date: 30 July 2026
Source: 2BSimple internal skill library (`/mnt/skills/user/`)

## Contents (6 skills)

| # | Skill | Version | บทบาทใน chain |
|---|-------|---------|----------------|
| 1 | `html-generator-v6` | v6.0 Warm Light | สร้าง HTML prototype (Patterns A–O, 49 iron rules, CI Warm Light) |
| 2 | `frd-generator-v6` | v6 Design Authority | FRD Pack แยก layer (UI/API/LOGIC/DB/Rules/Tests) — HTML-first |
| 3 | `html-ui-brief` | v1.0 | UI Brief สกัด 1:1 จาก HTML คู่กับ FRD Pack ส่ง dev |
| 4 | `ai-testcase-md-generator` | v1.1 Workflow | Test case markdown ให้ AI agent รันเอง |
| 5 | `qa-friendly-html-generator` | v2.2 Warm Light | เอกสารแบบทดสอบฉบับผู้ใช้ (UAT HTML ไฟล์เดียว) |
| 6 | `thai-doc-pdf-generator` | — | เอกสารธุรกรรม/จดหมายทางการไทย PDF A4 (Sarabun ฝังไฟล์) |

## Pipeline order (WF-01, HTML-first)

```
HTML (1) → FRD Pack (2) → UI Brief (3) → Test Cases (4) → UAT Doc (5)
                                   └── (6) ใช้แนบ FRD เมื่อ feature มีเอกสารพิมพ์
```

## Install

วางทั้งโฟลเดอร์ `skills/*` ลงใน skill directory ของปลายทาง เช่น

```
~/.claude/skills/
  html-generator-v6/
  frd-generator-v6/
  ...
```

แต่ละโฟลเดอร์มี `SKILL.md` เป็น entry point — ไม่ต้อง config เพิ่ม

## Dependencies / หมายเหตุ

- **CI**: skill 1, 5 ใช้ CUBE Warm Light (Charcoal `#111111`, Red `#FF3B30`, Orange `#FF9A1F`, Ivory `#FAF8F5`) + Satoshi/Noto Sans Thai
  skill 6 ใช้ CUBE NATIVE (Navy `#0B1D3A`, Primary `#0B5CFF`, Teal `#00A88E`) + Sarabun
- **Sync Read**: `frd-generator-v6`, `ai-testcase-md-generator`, `qc-*` อ่าน iron rules/microcopy จาก `html-generator-v6/knowledge/` แบบ live — ห้าม hardcode ถ้าย้าย ให้เก็บทั้ง 6 ตัวไว้ระดับเดียวกัน
- **Version pin**: `frd-generator-v6` อ้าง `cube-master-knowledge/knowledge/04_skills/workflow-master-wf01-06.md` — ไม่รวมมาในชุดนี้ ปลายทางที่ไม่มี cube-master-knowledge จะรันได้แต่ไม่มี version pin
- **Python deps**: `thai-doc-pdf-generator/scripts/render_pdf.py` และ `qa-friendly-html-generator/scripts/` ต้องมี playwright/weasyprint ตามที่ระบุใน SKILL.md ของแต่ละตัว
- **Assets**: ฟอนต์ Sarabun (.ttf) และ inter/noto (.woff2) ฝังมาในชุดแล้ว — ไม่ต้องโหลดเพิ่ม
