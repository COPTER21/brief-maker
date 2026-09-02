---
file_id: KB-04-03
title: Workflow Master — WF-01..WF-06 (2bsimple Master Process)
version: 2.10.0
last_updated: 2026-07-25
status: stable
source: Google Sheet "2bsimple Master Process" + WF-01 v2 Skeleton session (2026-07-24/25)
---

# Workflow Master — ระบบปฏิบัติการงาน CUBE (WF-01..WF-06)

> **นี่คือ operating model ปัจจุบันของทีม + version pin กลาง**
> ทุก skill ที่ sync read เวอร์ชัน generator/gate ต้องอ่านจากไฟล์นี้ — **ห้ามจำเวอร์ชันกันเอง**
> (บทเรียน 2026-07: 7 skill จำเวอร์ชันเองแล้ว drift — v4/v5/-25 ปนกันจน CI ชนกันเอง)

## 6 Workflows

| WF | ชื่อ | ใช้เมื่อ |
|---|---|---|
| WF-01 | New Feature (Full Loop) | สร้าง feature ใหม่ทั้งวง |
| WF-02 | Enhancement | ปรับ feature เดิม |
| WF-03 | New Requirement (Draft) | requirement ใหม่ระดับ discovery |
| WF-04/05/06 | Report (Informative/CSV/Dashboard) | รายงาน 3 แบบ |

จุดตัดสินใจ WF-04/05/06 อยู่ที่ SOP2 Field Mapping — **GAP: `report-field-mapping-checker` ยังไม่สร้าง**

---

## ⭐ Version Pin (source of truth เดียว)

| บทบาท | Skill ที่ pin | ห้ามใช้ |
|---|---|---|
| HTML generator | `html-generator-v9` **v6.2** (Warm Light, iron rules 49 + Layout Integrity #50-62 + Component Contracts #63-68 + Kit Integrity #69 + Anatomy #70-73 + Contracts #74-77 + ERP UX Ref + Blocks-First (templates/blocks/) #78-80 + audit v4) | ~~v3 / v4 / -25~~ (Navy — ปนแล้ว UX gate BLOCK) |
| BRD | `brd-generator-full` v2.1 (+ HTML input, HTML-first) | — |
| FRD | `frd-generator-v6` Design Authority (Sync Read → **v6**) | ~~v5 / -25~~ |
| RIF | `requirement-intake-formatter` v2.1 | — |
| Testcase | `ai-testcase-md-generator` v1.1 (microcopy → **v6**) + `qa-friendly-html-generator` (CI Warm Light) | — |
| UX gate | `qc-ux-html-checker` (3 pass: rules + Geometry + **Render Gate บังคับหลักฐานภาพ — ไม่มีภาพ = BLOCK**) | — |
| Coverage gate | `qc-coverage-checker` (เทียบ graph เท่านั้น) | — |
| UI brief | `html-ui-brief` (extraction-based 1:1) | `dev-brief-generator` (ตัดออกจาก WF-01 v2) |
| Drift check | `html-to-frd-sync` | — |
| Orchestrator | `feature-lane-runner` v0.3 | — |
| Brief ตั้งต้น (SOW1 — งานคน) | `lane-brief-generator` v1.0 | — |

**ตัดออกจาก WF-01 v2 โดยตั้งใจ:** `uba-taxonomy-register` (ไม่ใช้), `dev-brief-generator` (ใช้ `html-ui-brief` แทน), **`output-checker` (ตัด 2026-07-25 — เกณฑ์ผูก -25/Navy; งาน final check กระจายเข้า gate ในตัว: BRD C01-C23, FRD Phase 3.5 A-M, Coverage Manifest R13, Coverage R2, TC Ledger cross-check)**, OP adapter (รอ endpoint — dry-run ผ่าน `_OP_MANIFEST.json`)

---

## WF-01 v2 — HTML-First Lane (แทน pipeline เดิม §SOP3)

> เปลี่ยนจาก doc-first (BRD→FRD→HTML) เป็น **HTML-first** — เอกสารเขียนโดยเห็นหน้าจอจริง
> รันอัตโนมัติ one-shot โดย `feature-lane-runner` — ไม่มี human gate ในเลน
> รายละเอียด gate policy/retry อยู่ที่ `feature-lane-runner/references/`

**เหนือเลน (มีก่อน):** `plan-module-workflow-mapper` (ต่อ module) → graph/NODE_BRIEF/BUILD_ORDER · `newfeature-signoff-generator` (ต่อ feature) → LOCK-XX

| Step | งาน | Skill | หมายเหตุ |
|---|---|---|---|
| S0 | Pull Brief → RIF | `requirement-intake-formatter` | input = **Central Plan ทั้งก้อน + LANE_BRIEF** (ไม่ตัด slice) · self-slice ตามกติกาใน feature-lane-runner · conf ≥80% + LOCK ครบ (ใบเซ็น หรือ LD/AC/OQ-G สำหรับงาน internal) |
| S1 | HTML | `html-generator-v9` | อ่าน NODE_BRIEF+GOLDEN_RULES เสมอ |
| S2 | Check HTML (ถูกมั้ย) | `qc-ux-html-checker` | UX ก่อน Coverage — **ล็อกแล้ว** |
| S3 | Check Logic (ครบมั้ย) | `qc-coverage-checker` R1 | เทียบ graph, evidence ทุก ✓ |
| S4 | BRD | `brd-generator-full` v2.2 | **อ่าน HTML เป็น input ร่วม** · gate = Quality Gate C01-C23 ในตัว (APPROVED) |
| S5 | FRD Pack | `frd-generator-v6` v6.1 | Design Authority (Recognize & Validate) · gate = Phase 3.5 A-M ในตัว |
| S6 | TC + UAT doc | `ai-testcase-md-generator` → `qa-friendly-html-generator` | 1:1 ห้าม drop เคส |
| S6.5 | Coverage R2 | `qc-coverage-checker` R2 | rules ใน 05_RULES + TC ครอบ |
| S6.75 | Drift check (conditional) | `html-to-frd-sync` | **รันเมื่อ HTML ถูกแก้หลัง S5** (fix loop แตะ HTML) — UX drift auto-sync FRD · Business drift = Hard Stop |
| S7.5 | UI Brief | `html-ui-brief` | สกัดจาก HTML final + FRD → เข้า DevPack ให้ dev |
| S8 | Pack | runner | DevPack.zip + `_OP_MANIFEST.json` |
| S9 | OP Sync | adapter (dry-run) | แขวนไฟล์+สถานะราย SOW ผ่าน `op-binding.json` |

**Gate policy ย่อ:** PASS/WARN ไหลต่อ · BLOCK วนแก้ (cap 3/gate, 8/feature, issue ซ้ำ 2 รอบ = หยุด) · NOT-CHECKED = BLOCK · Hard Stop 5 ข้อ (LOCK/sign-off/graph/graph ขาด/governance) ห้าม auto-fix · **"Check ?" = built-in gates ของแต่ละ skill ไม่มีตัวตรวจอิสระ (ตัด output-checker แล้ว)**

**Post-lane rule:** vibe HTML หลังได้ DevPack → **ต้องผ่าน `html-to-frd-sync` เสมอ** ก่อนถือว่าเอกสารยัง valid

## Run List ปัจจุบัน
ลำดับรันทั้งโปรเจกต์ (41 features · 9 waves + สถานะรายตัว): ดู `wf01-run-list.md` — อัพเดตทุกครั้งที่ feature จบเลน

## OP Mapping (pattern CL-0003)

SOP1 = คน (intake+sign-off) · SOP2 = 12 SOW: SOW1 Feature Brief ตั้งต้น (คน — lane-brief-generator) → SOW2-12 AI ทั้งหมด (RIF → HTML → ตรวจUX → ตรวจครบจอ → BRD → FRD → TC → UAT → ตรวจครบเอกสาร → UI Brief → Final Dev Doc) · SOP3-4 = dev+test หยิบ DevPack ต่อ
Binding อยู่ที่ `op-binding.json` ต่อ CL — **ห้าม hardcode SOW ใน skill**

## Document Chain (Scope Lock ตลอดสาย — ไม่เปลี่ยน)

```
ใบเซ็น Sign-off [LOCK-XX] → RIF §16.3 → BRD §3.4 → FRD 07_LOCKED → TC → DevPack
```
- Scope Lock ห้าม override ตลอดสาย — ขัดเมื่อไหร่ = Hard Stop
- Design Authority อยู่ที่ **FRD** — HTML มาก่อนเชิงเวลา ไม่ใช่เชิงอำนาจ
- LOCK ชนะทุกอย่าง · RIF ชนะ HTML (ยกเว้น layout — HTML ชนะ)

## Change Log
- **2.10.0** (2026-07-28): One-Shot Hardening — reference strip JS ทั้ง 4 (#82 Behavior-from-Kit) + audit v7 (undefined_handlers/missing_ids) + render เดิน tab/overlay ครบ
- **2.9.1** (2026-07-28): #81 jargon leak · #68.1 overlay ระบบเดียว · #73.1 All-Tabs Test
- **2.9.0** (2026-07-28): reference ครบ 4 archetype (product-drawer/fac-fullpage/operation-console/bom-general) + #78.7-78.8 + #62.2 + audit menu_no_bg_z
- **2.8.1** (2026-07-27): defect F-UOM thead ทะลุ drawer → #62.1 Overlay Layering (overlay ต้องประกาศ z + เป็นลูก body + map class กลับ kit) + audit overlay_no_z + Render: Sticky-vs-Overlay Test
- **2.8.0** (2026-07-27): Reference-First — ไฟล์ vibe user = Golden Reference (healed) ใน templates/reference/ · master-data features ให้ mirror ทั้งโครง
- **2.7.1** (2026-07-27): #78 ขยายเป็น Filter Zone Spec 6 ข้อวัดได้ (1 แถว 36px/select 140-240/นับที่เดียว) + audit v5 จับ fullwidth_select · duplicate_counts
- **2.7.0** (2026-07-27): v6.6 audit ผ่านแต่ตายังไม่ผ่าน → เปลี่ยนกลยุทธ์เป็น Block-First: templates/blocks/ (toolbar-filter/uom-editor/avatar-cell กลั่นจาก vibe) + #78 toolbar row · #79 progressive create · #80 avatar initial
- **2.6.0** (2026-07-27): visual review รอบ 2 → #74 tab contract · #75 form composition · #76 no h-overflow · #77 mock completeness+compound widget · Phase 0.5 ERP UX Reference (erp-ux-patterns.md ชั้น offline + search สดชั้น online) · audit v3 จับ banner ยาว+tab เถื่อน
- **2.5.0** (2026-07-26): Greenfield run สำเร็จ (audit=0) แต่ user เทียบกับ vibe แล้วชี้ gap ใหม่ = composition — เพิ่ม Page Anatomy #70-73 (stat row/chip counts/sortable/identity drawer/summary step) — "ความถูกจบแล้ว เกมถัดไปคือความรวย" 
- **2.4.3** (2026-07-26): วินิจฉัย root cause — skeleton ป่วยเอง (56 spacing/14 fonts) → heal จน audit=0 + Rule #69 Kit Integrity (BASE-KIT verbatim + #page-late escape) + Checkpoint ทุก Phase
- **2.4.2** (2026-07-26): Component Contracts #63-68 (density/breathing/dropdown contract/flip-up/hint→tooltip/overlay discipline) จาก defect จริง + self_audit v2 + Render Gate เพิ่ม Bottom-Edge & Dropdown Anatomy Test
- **2.4.1** (2026-07-26): เพิ่ม #61 Type Scale + #62 Z-Index Registry + Self-Review Protocol (stamp ต้องมีตัวเลข, checker นับซ้ำเทียบ) 
- **2.4.0** (2026-07-26): บทเรียน F-PRODUCT "HTML ผ่าน gate แต่เบี้ยว" → v6.2 Layout Integrity #50-60 + Pre-flight stamp + checker 3 pass (Geometry static + Render Gate หลักฐานภาพบังคับ) — เลนต้องรันใน env ที่มี browser
- **2.3.0** (2026-07-26): เพิ่ม lane-brief-generator (SOW1 งานคน) + ล็อกโครง SOP2 = 12 SOW
- **2.2.0** (2026-07-25): Pre-RIF = Central Plan ทั้งก้อน + LANE_BRIEF ต่อ feature (ยกเลิกแนวคิด NODE_BRIEF slice — กัน artifact stale) + Self-Slice Rules 5 ข้อใน feature-lane-runner
- **2.1.0** (2026-07-25): ตัด output-checker ออกจากเลน (S7) — final check กระจายเข้า built-in gates · pin BRD v2.2 / FRD v6.1 / TC v1.2 / qa-friendly v2.2
- **2.0.0** (2026-07-25): WF-01 v2 HTML-first lane + Version Pin กลาง + เพิ่ม S6.75 drift check / S7.5 html-ui-brief + ตัด uba-taxonomy/dev-brief + OP dry-run
- **1.0.0** (2026-07-06): Initial snapshot
