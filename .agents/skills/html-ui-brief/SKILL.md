---
name: html-ui-brief
description: >
  สร้าง "HTML UI Brief" (.md) — บรีฟ UI ที่สกัดจาก HTML prototype แบบ 1:1 ใช้คู่กับ HTML
  (source of truth) + FRD Pack ให้ dev สร้างระบบจริงที่ตรงกันทุกจุด หัวใจ: EXTRACTION-BASED —
  ทุกบรรทัดต้อง trace กลับหา selector/function/ข้อความจริงใน HTML ได้ ห้ามแต่งสเปคเอง
  ครอบคลุม design tokens, z-index map, route map, anatomy รายหน้า, component states,
  overlay registry + dismiss rules, Esc chain, state-driven UI matrix, microcopy verbatim,
  BACKEND anchors ↔ FRD API, traceability 3 ทาง (Brief ↔ FRD ↔ HTML) + Drift Log
  ใช้เมื่อ user พูดถึง "html-ui-brief", "HTML UI Brief", "สร้างบรีฟ UI จาก HTML",
  "บรีฟคู่ HTML", "UI brief ให้ dev", "แกะ UI จาก HTML", "สเปค UI เป๊ะ ๆ",
  "บรีฟ UI ตรงกับ FRD", "UI handoff จาก HTML", "ทำบรีฟจากไฟล์ html"
  Input: HTML 1 ไฟล์ + FRD Pack (optional) + HTML เก่า (optional — diff)
  Output: UI_BRIEF_[feature].md ไฟล์เดียว
---

# HTML UI Brief Generator v1.0

**ตำแหน่งใน workflow:** WF-01 · SOP3 · หลัง SOW3.3 (FRD) / SOW3.4 (HTML final) — ก่อน dev handoff
**เป้าหมาย:** dev อ่าน **HTML + FRD Pack + UI Brief** แล้วสร้างระบบจริงได้ตรง prototype โดยไม่ต้องแกะโค้ดเอง และไม่ต้องเดา design intent

**DoD:** 1) ทุก route/หน้า/modal/drawer ใน HTML มี section ในบรีฟ  2) microcopy verbatim 100%  3) ทุก component มี selector anchor  4) Verification Gate ผ่าน (FAIL=0)  5) ถ้ามี FRD → ตาราง traceability ครบทุก P-xx

---

## 🧭 หลักการ (Iron Rules)

| # | Rule |
|---|---|
| R1 | **Extraction-based เท่านั้น** — ห้ามเขียนสเปคที่ไม่มีใน HTML · ทุก claim ต้องชี้ anchor ได้ (CSS class / function name / ข้อความ / บรรทัด) · อยากเสนอเพิ่ม → ใส่หมวด "💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)" แยกท้ายไฟล์เท่านั้น |
| R2 | **Microcopy verbatim** — ปุ่ม/toast/label/placeholder/empty state คัดลอกตรงตัวจากโค้ด ห้าม paraphrase (คำเดียวเพี้ยน = dev สร้าง test ไม่ตรง) |
| R3 | **ทุก component มี anchor** — ระบุ selector หลัก (`.qa-drop`, `#tdrawer .td-foot`) + function ที่ render/handle (`quickAssignOpen()`) เพื่อให้ dev เปิดโค้ดเจอทันที |
| R4 | **State ครบ** — ทุก interactive component ต้องไล่ default / hover / focus / active / disabled / empty / loading / error เท่าที่มีจริงใน HTML — state ไหนไม่มีให้เขียน "ไม่มี (—)" ชัด ๆ กันเดา |
| R5 | **Behavior เชิงระบบต้องเก็บ** — Esc/keyboard chain ตามลำดับจริง, z-index map, positioning strategy (fixed/absolute + เหตุผล), scroll lock, focus management, dismiss rules ของทุก overlay (อันไหน "ห้ามปิด" ต้องตะโกน) |
| R6 | **Pair กับ FRD ถ้ามี** — map ทุกหน้า ↔ 01_UI P-xx, ทุก action ↔ 02_API/BR-xx · เจอของใน HTML ที่ FRD ไม่มี (หรือกลับกัน) → ลง "⚠️ Drift Log" ห้ามเงียบ |
| R7 | **1 HTML = 1 Brief = 1 ไฟล์ .md** — เกินไฟล์เดียว = แตก feature ผิดตั้งแต่ต้นทาง |
| R8 | **Verification Gate ก่อนส่ง** — รัน checklist Phase 4 (mechanical) ให้ FAIL=0 |
| R9 | **ภาษาไทย tone dev-brief** — กระชับ ตาราง > ร้อยแก้ว · ศัพท์ UI ทับศัพท์ได้ (drawer, popover, pill) |
| R10 | **ห้ามลอก CSS ทั้งดุ้น** — สกัดเป็น token/ค่า ไม่ก็ชี้ selector (บรีฟคือแผนที่ ไม่ใช่สำเนาโค้ด) |

---

## 📥 Input

| # | ไฟล์ | Required | ใช้ทำอะไร |
|---|---|---|---|
| 1 | HTML prototype (single-file SPA) | ✅ | source of truth — สกัดทุกอย่าง |
| 2 | FRD Pack (โฟลเดอร์ / อย่างน้อย 01_UI.md + 02_API.md + 05_RULES.md) | optional | traceability + drift check (R6) |
| 3 | HTML เวอร์ชันเก่า | optional | Section 12 Diff |
| 4 | context ในแชท (decision ที่เคาะแล้ว) | optional | อ้างเป็น CH-xx ในคอลัมน์ "ที่มา" |

> ไม่มี FRD → ข้าม Section 11 + Drift Log แล้วระบุใน Document Control ว่า "ยังไม่ pair FRD"

---

## 📐 Workflow

### Phase 0 — Intake (auto, ไม่ถาม user)
1. อ่าน HTML ทั้งไฟล์ · ระบุ feature name จาก `<title>` / header / ชื่อไฟล์
2. รัน `scripts/extract_anchors.py <file.html>` (ถ้าอยู่ใน environment ที่รัน python ได้) → ได้ raw inventory: CSS variables, routes, modal/drawer classes, toast strings, ปุ่มทั้งหมด, z-index, function names — ใช้เป็น checklist กันหล่น **ห้ามใช้แทนการอ่านจริง**
3. มี FRD → อ่าน 01_UI (P-xx + Layout Decision Log), 02_API (endpoint), 05_RULES (BR/EC)
4. มี HTML เก่า → เตรียม diff (Section 12)

### Phase 1 — Deep Extraction (อ่านโค้ดจริง)
ไล่ตามลำดับนี้เสมอ (กันตกหล่น):
1. **Tokens:** `:root` CSS variables ทั้งชุด + font stack + radius/shadow/scrollbar + z-index ทุกตัวที่ประกาศ → จัดเป็นตาราง z-index map เรียงจากสูงลงต่ำ
2. **Routes:** ทุก hash route + hashchange handler + default route + refresh-safety
3. **Pages:** ต่อ route → anatomy (region ใหญ่ → component ย่อย) พร้อม selector
4. **Overlays:** modal / drawer / popover / toast ทุกตัว → ขนาด, backdrop, วิธีเปิด-ปิด, **dismiss rules** (Esc? backdrop? ปุ่ม? หรือห้ามปิด), animation
5. **Interactions:** keyboard (Esc chain ตามลำดับใน handler จริง), click-outside, drag/pan/zoom (threshold, suppression), focus/RAF tricks, positioning (fixed vs absolute + เหตุผลจาก comment/โครง)
6. **State-driven UI:** enum สถานะ → pill class + label + สี + ปุ่ม footer ต่อ state ต่อ type (สกัดจาก mapping objects เช่น `statusPill`, `taskFooter`)
7. **Microcopy:** ปุ่ม, toast (`showToast(...)` ทุก call), placeholder, empty/lock/hint, log templates — verbatim (R2)
8. **Data binding:** `// BACKEND:` anchors, mock structures, จุดที่ FE ต้อง plug API
9. **Assets/ไลบรารี:** icon set + loader, font source, ข้อจำกัด (no CDN ฯลฯ)

### Phase 2 — เขียนบรีฟ
ใช้ `templates/ui-brief.template.md` — โครง 13 sections (ดูใน template) · เขียนไล่ตาม template ห้ามข้าม section (section ที่ไม่มีเนื้อหา = เขียน "— ไม่มีใน HTML นี้" กันคนอ่านสงสัยว่าลืม)

### Phase 3 — Pair + Drift (ถ้ามี FRD)
- Section 11: ตาราง 3 ทาง `Brief §x ↔ FRD (P-xx / API-xx / BR-xx) ↔ HTML anchor`
- Drift Log: ของที่ HTML มีแต่ FRD ไม่มี = `HTML-only` / FRD มีแต่ HTML ไม่มี = `FRD-only` + ข้อเสนอ (แก้ FRD หรือแก้ HTML) — โยงไปสกิล `html-to-frd-sync` ถ้า drift เป็น business

### Phase 4 — Verification Gate (R8 — รายงานในแชทก่อนส่งไฟล์)
```
## 🔍 UI Brief Verification — [feature]
- [ ] ทุก route ใน HTML มี section (นับจาก extractor เทียบบรีฟ)     N/N ✅
- [ ] ทุก modal/drawer/popover มีแถวใน Overlay Registry              N/N ✅
- [ ] ทุก showToast ปรากฏใน Microcopy verbatim                      N/N ✅
- [ ] ทุก component ใน anatomy มี selector anchor                    ✅
- [ ] state matrix ครอบทุกค่า enum ที่เจอในโค้ด                       ✅
- [ ] Esc chain ตรงลำดับ handler จริง (อ้าง function)                 ✅
- [ ] z-index map ครบทุกตัวที่ประกาศ                                  ✅
- [ ] (FRD) ทุก P-xx มีแถว traceability + Drift Log ไม่เงียบ          ✅
- [ ] ไม่มีสเปคที่ trace ไม่ได้ (R1) — sample audit 10 จุด            ✅
Verdict: PASS → ส่งไฟล์ / FAIL → แก้ก่อน
```

### Phase 5 — Deliver
1. เซฟ `UI_BRIEF_[feature].md` → `/mnt/user-data/outputs/` → `present_files`
2. สรุปชุด handoff: **HTML (source of truth) + FRD Pack (ระบบ) + UI Brief (design intent)** + งาน manual (registry/แจ้งทีม) ตามธรรมเนียม

---

## 🗂 โครงไฟล์ output (สรุป — เต็มอยู่ใน template)

| § | Section | หัวใจ |
|---|---|---|
| 0 | Document Control + Pairing | HTML file/version · FRD ref · สถานะ drift |
| 1 | Design Tokens AS-BUILT | CSS vars ทั้งชุด · fonts · radius/shadow · **z-index map** |
| 2 | Route Map | hash routes + refresh-safety + default |
| 3 | Layout Shell | sidebar/topbar/breadcrumb ขนาดจริง |
| 4 | Page Anatomy (ต่อหน้า) | region tree + selector + ภาพรวม behavior |
| 5 | Component Inventory | ต่อ component: anchor + โครง + **states (R4)** + ขนาด |
| 6 | Overlay Registry | modal/drawer/popover/toast: ขนาด + **dismiss rules** + z |
| 7 | Interaction Spec | Esc chain · click-outside · drag/zoom · focus · positioning |
| 8 | State-Driven UI Matrix | enum → pill/label/สี/ปุ่ม footer ต่อ type |
| 9 | Microcopy (verbatim) | ปุ่ม/toast/placeholder/empty/lock/log templates |
| 10 | Data Binding & BACKEND anchors | mock ↔ API mapping จุด plug |
| 11 | Traceability + Drift Log | Brief ↔ FRD ↔ HTML (R6) |
| 12 | Diff จากเวอร์ชันก่อน (optional) | เพิ่ม/แก้/ตัด + ผลกระทบ |
| 13 | 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT) | ที่เดียวที่อนุญาตให้คิดเอง (R1) |

---

## 🔗 ตำแหน่งใน chain + การแบ่งงานกับสกิลข้างเคียง

```
html-generator-v4/v6 ──HTML──┐
frd-generator-v6 ──FRD Pack──┼──► html-ui-brief ──► UI_BRIEF_[feature].md
(optional HTML เก่า) ────────┘         │
                                      ▼
                    Dev handoff = HTML + FRD Pack + UI Brief
```
- ต่างจาก `ui-revision-brief-generator`: ตัวนั้นเน้น "revision/diff ส่ง dev ปรับ UI" — สกิลนี้คือ **full AS-BUILT spec** จับคู่ FRD ทั้ง pack เพื่อสร้างระบบใหม่ทั้ง feature
- ต่างจาก `html-to-feature-brief`: ตัวนั้น reverse เป็น requirement (ต้นน้ำ) — สกิลนี้เป็น design handoff (ปลายน้ำ)
- เจอ business drift ระหว่างทำ → ส่งต่อ `html-to-frd-sync`

## Reference Files
| File | Purpose |
|---|---|
| `templates/ui-brief.template.md` | โครงเอกสาร 13 sections พร้อมตัวอย่างกรอก |
| `references/extraction-checklist.md` | checklist สกัดต่อหมวด + จุดพลาดบ่อย |
| `scripts/extract_anchors.py` | ตัวช่วยดึง inventory (vars/routes/toasts/z-index) ใช้เป็น checklist |
