# UX Check Report — GL Posting Group (f-postgrp.html)
- วันที่: 2026-08-10 · Iteration: 3 (LOOP MODE — post coverage-gate fix pass)
- Generator spec synced: `html-generator-v7/knowledge/` — iron-rules.md + layout-integrity.md + component-contracts.md + page-anatomy.md + ci-tokens.md (Warm Light) + microcopy.md + component-catalog-ref.md
- ไฟล์ที่ตรวจ: f-postgrp.html (1,751 บรรทัด — เดิม 1,762 ที่ iter2, -11 บรรทัด net จากการลบ CSV mode step ที่หักลบกับโค้ด lock-tag/validation ที่เพิ่ม)
- Mechanical scan: `static_scan.py` + `html-generator-v7/scripts/self_audit.py` รันซ้ำอิสระ
- Stamp พบที่ line 609-626: `<!-- PREFLIGHT v6.3 — coverage-gate fix pass for _COVERAGE_REPORT.md (GAP-01 BLOCK, GAP-02/GAP-03 WARN), 2026-08-10 ... round3 (coverage gate): GAP-01 reverted / GAP-02 fixed / GAP-03 fixed -->` — **ยืนยันตัวเลขในสแตมป์ตรงกับ self_audit.py อิสระ 100%**

## Verdict: 🟢 PASS (with 8 warnings) — ไม่เปลี่ยนจาก iteration 2, ไม่มี regression จาก coverage-gate fix pass
| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 8 | 2 | 3 |

---

## Focus Check — 3 การแก้จาก coverage-gate pass

### 1. ลบ CSV Import Replace/Merge mode step (GAP-01 reverted)
- **ตรวจ:** grep `mode-opt`/`mode-radio`/`setImportMode`/`importModeNext` ทั้งไฟล์ = 0 ผลลัพธ์ (เหลือแค่ในข้อความ stamp ที่บรรยายการแก้) — ไม่มี dead CSS/orphan JS reference หลงเหลือ
- **`renderImportModal()`** (line 1673) เหลือ 3 step: pick → preview → done, merge-only ล้วน; subtitle บอกชัด "เพิ่มรายการใหม่เท่านั้น ทะเบียนเดิมไม่ถูกแตะ"
- **`applyImport()`** (line 1646) มี comment อธิบาย BR-07/FN-18 ตรงกับ behavior จริง (push เข้า state.groups/state.setup เท่านั้น ไม่มี replace logic เหลือค้าง)
- **สรุป: ไม่มี regression** — ลบสะอาด ไม่มีชิ้นส่วนตกค้าง

### 2. Block + toast validation ใน submitSetup() สำหรับ bus/prod ที่ used>0 (GAP-02 fixed)
- **ตรวจโค้ด** line 1501-1522: เพิ่ม branch `if(state.drawer.mode==='edit-setup'){ const t=sById(...); if((t.used||0)>0 && (f.bus!==t.bus || f.prod!==t.prod)){ ...add is-invalid...; showToast(...,'error'); return; } }`
- Pattern ตรงกับ tab 1 (`submitGroup` มี guard คล้ายกันสำหรับ code field ที่ used>0) — consistency ดี
- ไม่มี `style=` inline layout เพิ่มจากจุดนี้, ไม่แตะ flow ของ busy/guard เดิม (`if(state.busy.setup) return;` ยังอยู่บรรทัดแรกของฟังก์ชัน)
- **สรุป: ไม่มี regression** — logic เพิ่มตรงจุด ไม่กระทบ mechanical count ใด ๆ

### 3. `.lock-tag` static indicator บน code (tab1) และ bus/prod (tab2) เมื่อ used>0 (GAP-03 fixed)
- **CSS** line 271-272: `.lock-tag{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:600;color:var(--c-warning-fg);background:var(--c-warning-bg);border-radius:6px;padding:2px 8px;margin-left:8px;vertical-align:middle;}` — ใช้ CSS var tokens ทั้งหมด (`--c-warning-fg/-bg`) **ไม่มี raw hex ใหม่** → ตรงกับ `hex_off=0` ที่ self_audit ยืนยัน
- padding `2px 8px` / gap `4px` / border-radius `6px` อยู่ใน spacing scale ที่ยอมรับ (`spacing_off=0` คงที่)
- **Markup**: 3 จุดที่ใช้ (`fieldBlock` label + `.sdd-trigger` locked div) ที่ line 1211-1212 (code), 1254-1255 (bus), 1257-1258 (prod) — รูปแบบเดียวกับ kind field เดิม (line 1205) ที่ล็อกอยู่แล้ว ("mirroring kind field's existing lock treatment" ตามที่ stamp ระบุ) — **component consistency ดี ไม่สร้าง pattern ใหม่ซ้ำซ้อน**
- inline `style="cursor:not-allowed; opacity:0.7;"` ที่ locked div ทั้ง 3 จุดใหม่ — เป็น cursor/opacity เท่านั้น **ไม่ใช่ layout property (margin/padding/width/height)** จึงไม่ติด `inline_layout` regex ของ self_audit และไม่ถือเป็น violation ของ Rule inline-layout — ยืนยันด้วย `self_audit: inline_layout=0` (คงที่จาก iter2)
- `static_scan.inline_style_attr_count` ขยับ 18→21 (+3) ตรงกับ 3 locked-div ใหม่พอดี ไม่มีจุดผิดคาด
- **สรุป: ไม่มี regression** — icon `lock` เป็น lucide icon มาตรฐาน, ใช้ token สี ไม่ใช่ hex ดิบ

---

## เทียบ self_audit ตัวเลข Iteration 2 → 3 (ยืนยัน PREFLIGHT stamp ตรงกับนับจริง)

| Metric | Iter 2 (stamp+report) | Iter 3 (นับจริงซ้ำ) | สถานะ |
|---|---|---|---|
| spacing_off | 0 | 0 | ✅ คงที่ |
| font_off | 0 | 0 | ✅ คงที่ |
| font_count | 7 (limit 8) | 7 (limit 8) | ✅ คงที่ |
| inline_layout | 0 | 0 | ✅ คงที่ (ไม่ regress แม้เพิ่ม 3 locked-div) |
| z_adhoc | 0 | 0 | ✅ คงที่ |
| hex_off | 0 | 0 | ✅ คงที่ (lock-tag ใช้ var tokens) |
| preflight | 0 (stamped) | 0 (stamped v6.3) | ✅ คงที่ — stamp อัปเดตแล้ว |
| flex_noalign | 7 | 7 | ✅ คงที่ (WARN เดิม UX-12 ไม่เปลี่ยน) |
| stopprop_blanket | 8 | 8 | ✅ คงที่ (false-positive เดิม) |
| long_banners | 1 | 1 | ✅ คงที่ (WARN เดิม UX-14 ไม่เปลี่ยน) |
| missing_ids | 5 | 5 | ✅ คงที่ (false-positive เดิม — dynamic runtime ids) |
| fullwidth_select | 2 | 2 | ✅ คงที่ (false-positive เดิม) |
| custom_tabs | 4 | 4 | ✅ คงที่ (pre-existing pattern) |

**ไม่มี metric ใดขยับผิดคาดจาก 3 การแก้ — เฉพาะ `inline_style_attr_count` (static_scan, ไม่ใช่ self_audit BLOCK metric) ขยับ 18→21 ตามที่คาด และไม่กระทบ verdict**

---

## 🔴 BLOCK — ไม่มี (0)

## 🟡 WARN (8 — เหมือน iteration 2 ทุกข้อ ไม่มีข้อใดถูกแก้หรือเกิดใหม่ในรอบนี้)

ตามคำสั่งงาน scope ของ iteration 3 คือตรวจ regression จาก coverage-gate fix pass เท่านั้น — WARN เดิม UX-12 ถึง UX-19 (flex align-items, `.stats` ประกาศซ้ำ, hint banner, inline validation on blur, sortable headers, confirm modal ก่อน inactivate, empty state branch, font loading cleanup) **ไม่ถูกแตะโดย 3 การแก้ และยังคงสภาพเดิมทุกข้อ** ดูรายละเอียดเต็มที่ report iteration 2 (เนื้อหาไม่เปลี่ยน จึงไม่ลอกซ้ำที่นี่)

## ℹ️ INFO (2 — เหมือน iteration 2)
- UX-20 Dead code ternary — ไม่เปลี่ยน
- UX-21 ไม่มี per-row delete — ไม่เปลี่ยน (business scope, ไม่ใช่งานของ checker นี้)

## ⬜ NOT-CHECKED (3 — เหมือน iteration 2)
- Rule #38 Thai Vertical Rhythm — ต้อง render จริง
- Pass R (Render Gate) — **RENDER: UNAVAILABLE** ทั้ง 3 รอบ — โดยเฉพาะ `.lock-tag` ใหม่ยังไม่เห็นภาพจริงว่าวางตำแหน่งข้าง field-label แล้วตัดคำ/ล้นบรรทัดหรือไม่ในหน้าจอแคบ
- stopprop_blanket=8 — false positive ตรวจแล้ว (เดิม)

---

## Loop Diff — Iteration 2 → 3

| ID/หัวข้อ | Iter 2 | Iter 3 | หลักฐาน |
|---|---|---|---|
| CSV Replace/Merge mode | มีอยู่ (UX-09 ของ iter1 ที่เคยแก้เป็น mode selector) | ถูกลบทั้งหมดตาม coverage-gate GAP-01 | grep `mode-opt/mode-radio/setImportMode` = 0; `renderImportModal` เหลือ pick→preview→done merge-only |
| submitSetup() validation | validate เฉพาะ required fields + dup combination | เพิ่ม block+toast เมื่อ used>0 และเปลี่ยน bus/prod | code line 1508-1514: is-invalid + showToast('error') + return |
| lock indicator (code/bus/prod) | ไม่มี (มีแค่ kind field ที่ล็อกอยู่ก่อน) | เพิ่ม `.lock-tag` badge + locked div ที่ code(tab1), bus/prod(tab2) | CSS line 271-272 (var tokens), markup line 1211-1212, 1254-1255, 1257-1258 |
| self_audit BLOCK metrics ทั้งหมด | 0 ทุกตัว | 0 ทุกตัว (คงที่) | ตารางเทียบด้านบน |
| WARN 8 ข้อเดิม | ค้าง 8 | ค้าง 8 (ไม่เปลี่ยน) | ไม่อยู่ใน scope ของ 3 การแก้รอบนี้ |

**สรุป: 3 การแก้จาก coverage-gate fix pass ไม่สร้าง BLOCK ใหม่ ไม่สร้าง WARN ใหม่ ไม่ทำ mechanical metric ใดขยับผิดคาด — regression-free**

## เกณฑ์ผ่าน Gate
BLOCK = 0 → **ผ่าน mechanical/heuristic gate ต่อเนื่อง** — เหลือ WARN 8 ข้อเดิมให้ user ตัดสินใจ — Render Gate ยังเป็น UNAVAILABLE (3 รอบติด) โดยเฉพาะ `.lock-tag` ที่เพิ่มใหม่ยังไม่เห็นภาพจริง
