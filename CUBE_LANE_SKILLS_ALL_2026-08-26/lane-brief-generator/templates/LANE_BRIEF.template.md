# LANE_BRIEF — {FEATURE_ID} · {FEATURE_NAME}

> ใบสั่งเข้าเลน 1 feature (S0) — brief = เจตนา+ตัวชี้ · ความรู้อยู่ที่ knowledge/plan (เลน slice สดเอง)
> ออกโดย lane-brief-generator v2.0 · {DATE} · pool_version: {POOL_VERSION} · plan_version: {GRAPH_VERSION|—} · knowledge: current-state v{X} / catalog v{Y}

| | |
|---|---|
| **Feature** | `{FEATURE_ID}` — {NAME_EN} · {NAME_TH} |
| **Module / Wave** | {MODULE} · {WAVE} |
| **ประเภทงาน** | new / ENH ต่อ artifact เดิม: {…} |
| **Archetype (html-generator-v9)** | {Q-document / master / P-planner / J-dashboard / console} → reference: {path} |
| **Dependency** | {dep list + สถานะ done/ba-done} |

## Scope รอบนี้ (จาก catalog + scope note)
- ทำ: {…}
- hook ที่ต้องมี (edge out / เอกสารต้นทาง-ปลายทาง): {ปุ่ม/สถานะ/ช่องอ้างอิง — ไม่ทำ feature ปลายทาง}
- scope note จากคนเลือก: {ข้อความจาก WAVE_CHECKLIST — verbatim}

## ไม่ทำรอบนี้ ← ห้ามว่าง
- {ของ feature ปลายทาง / สิ่งที่ตัด}
- **เรียกใช้ baseline ไม่ทำเอง:** {DOA engine · DOCCFG · NOTIFY · Roles/Employee · OP/Planner … ตามที่เกี่ยว}

## Declarations ที่ต้องรัน (S1.8 — ตั้งต้นจาก chip · S1.8 detect ซ้ำ)
| ท่อ | chip | skill | หมายเหตุ |
|---|---|---|---|
| DOA | {✓/—} | doa-declaration | {มีวงเงิน? สายเดียว/หลายสาย — จาก scope note} |
| NTF | {✓/—} | ntf-declaration | {event ธุรกิจที่คาด} |
| CSQ | {✓/—} | csq-declaration | {ท่อที่คาด EC/SecC/AC/FC/DC — ห้าม OC/DC-doc/SC} |
| DOCCFG | {✓/—} | doccfg-declaration | {doc_type ที่คาด} |
| PDF DOC | {✓/—} | thai-doc-pdf-generator | {ชื่อเอกสาร/แบบฟอร์ม · ต้องมีเลขผู้เสียภาษี/สาขา? ช่องเซ็นกี่ช่อง} |

## LOCK / มติ (อ้าง id — ศักดิ์เท่าใบเซ็น)
- {DOA iron rule · มติ 2026-08-17 slot picker · LD-4C-02 · HR-1 · audit append-only · 7C forbidden pipes · LD-xx/AC-xx/OQ-Gxx จาก graph}

## OQ
- ตอบแล้ว (จาก scope note): {…}
- ให้เลนใช้ default + `[ASSUMED]`: {…}
- Hard Stop (ไม่มีคำตอบ + critical): {— หรือรายการ → validate ตก}

## Skill ที่เลนจะเรียก (ตามลำดับ)
feature-prebrief → feature-review-standard(quick) → [declarations ข้างบน] → html-generator-v9 → audit/qc-ux/qc-coverage/render/taste → RIF/brd-generator-full → frd-generator-v6 → ai-testcase-md → qa-friendly-html → qa-html-to-ai-testset → qc-coverage R2 → html-ui-brief → output-checker → NF-SO

---
## Context Preview (FYI คนตรวจ — เลนไม่ใช้)
- feature ข้างเคียงใน module: {…} · edges in {I} / out {O} (ถ้ามี graph) · artifacts เดิม: {…} · TASTE_LOG: {path}
