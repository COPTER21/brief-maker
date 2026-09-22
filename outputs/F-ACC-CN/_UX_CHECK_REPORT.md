# _UX_CHECK_REPORT — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

| | |
|---|---|
| ไฟล์ | `outputs/F-ACC-CN/F-ACC-CN_credit-note.html` |
| Generator (Sync Read) | `html-generator-v9` (`.claude/skills/html-generator-v9`, v9.1) — Pattern Q + B2 v2 |
| รอบ | **Re-gate หลัง BA เคาะ 2 กฎบัญชี "ส่วนลดท้ายบิล"** (surgical) · WF-01 C3.2 (แตะ `.html` หลัง step 5 → ตรวจ 3·4·5 ใหม่) |
| วันที่ | 2026-09-22 (Windows · venv playwright 1360×900) |
| **Verdict** | 🟢 **PASS with 1 warning** — BLOCK = 0 · audit.sh **FAIL=0 · WARN=1** (baseline sidebar font-size) |

---

## บริบทการเปลี่ยน (BA เคาะ 2 กฎ)

รอบก่อน = restore ส่วนลดท้ายบิล B2 v2 (segmented ฿/%) โดย end-bill หัก"หลัง VAT". รอบนี้ BA เคาะ **2 กฎบัญชี** ให้ถูกต้องตามกฎหมาย:

- **Rule 1 (จำกัด):** ส่วนลดท้ายบิลต้องไม่ทำให้ยอดสุทธิ (grand) ติดลบ — เพดาน = ยอดหลัง VAT (`ebCap = after − coupon`) · เกิน = clamp + hard-warn + block submit + hint "ลดได้สูงสุด ฿X"
- **Rule 2 (ม.86/10):** ส่วนลดท้ายบิล **ลดฐานภาษี** → VAT คิดใหม่จากฐานที่ลดแล้ว (ภ.พ.30 / JE / PDF ต้องโชว์ VAT ที่ลดลง ไม่ใช่ VAT เต็มบรรทัด)

การแก้เป็น **CN-level totals adjustment** — ไม่แตะ per-line B2 v2 VAT engine (`calcLineVat`/`migrateLine`).

---

## Phase 1 — Mechanical (audit.sh = gate)

`bash .claude/skills/html-generator-v9/scripts/audit.sh <file>` → **FAIL = 0 · WARN = 1** · doc_archetype: ไม่มี FAIL

| WARN | สถานะ | เหตุผล |
|---|---|---|
| Token — hardcoded `font-size` (sidebar BASE-KIT) | คงไว้ (baseline) | WARN เดียวกันยิงบน golden `file-skeleton.template.html` — ไม่ใช่ regression · ไม่ได้เกิดจากรอบนี้ |

### self_audit.py (เครื่องนับเสริม — non-zero-tolerance · **ไม่ใช่ gate** ตาม memory `html-v8-self-audit-not-zero-tolerance`)
`RESULT: FAIL` — residual: `inline_layout=248 · stopprop_blanket=6 · long_banners=1 · missing_ids=4 · custom_tabs=2`
ทุก counter ≤ Q-archetype golden `_SOURCE_so-reference.html`. `inline_layout` 239→248 จาก inline-style ของแถวสรุปที่แทรกเพิ่ม (ฐานหลังหักส่วนลด / VAT คิดใหม่) — ฟอร์แมตเดียวกับแถวสรุปเดิมใน Pattern Q ไม่ใช่ regression. **gate = audit.sh FAIL=0 → ผ่าน.**

---

## Pass D — Document Archetype (Q)

- audit ส่วน `doc_archetype`: **ไม่มี FAIL**
- **VAT/discount per-line engine** (`calcLineVat` / `migrateLine`) — **ไม่แตะ** (diff = verbatim B2 v2)
- **totals order (#99):**
  - เมื่อ **ไม่มี** ส่วนลดท้ายบิล → canonical เดิมทุกตัว: ก่อน VAT → VAT → หลัง VAT → สุทธิ
  - เมื่อ **มี** ส่วนลดท้ายบิล → **BA-approved divergence (C3.4 · เนื้อธุรกิจ override display convention):** ก่อน VAT → ส่วนลดท้ายบิล (ลดฐาน) → ฐานภาษีหลังหักส่วนลด → **VAT คิดจากฐานใหม่ (ม.86/10)** → สุทธิ
  - เหตุผลที่ลำดับต่าง #99 canonical: กฎ ม.86/10 บังคับให้ end-bill เกิดผล **ก่อน** VAT (ลดฐาน) การโชว์ "VAT เต็ม แล้วค่อยหักท้ายบิลหลัง VAT" จะรายงานภาษีขายผิด — ลำดับใหม่คือการแสดงกฎที่ BA เคาะอย่างซื่อสัตย์ (สอดคล้องทั้ง `renderLineSummary` · `linesTableView` tfoot · `renderPdfTab`)
- B2 v2 grid / line editor / VAT segmented 3 โหมด / wizard 5 steps / view tabs order — **ไม่แตะ**
- ส่วนลดท้ายบิล segmented control (`.toggle` + ฿/% + value bound `createWizard.data.endbill`) — โครงเดิม

## จุดแก้ (surgical · CN-level เท่านั้น)

| จุด | ฟังก์ชัน | ทำอะไร |
|---|---|---|
| 1 | `totals()` | เพิ่ม `ebCap`/`ebOver` (Rule 1 clamp · grand≥0) + `ebVat`/`ebBase`/`netBefore`/`netVat` (Rule 2 แบ่งส่วนลดตามสัดส่วน VAT-inclusive) · `vat`/`before` เดิม (gross รายบรรทัด) คงไว้ |
| 2 | `step3Block` | เพิ่ม hint "ลดได้สูงสุด ฿X" ใต้ input (แดงเมื่อเกิน) |
| 3 | `lineSummaryWarn`/`blockReason`/`submitGuard` | hard-warn + block submit เมื่อ `ebOver` (Rule 1) |
| 4 | `renderLineSummary`/`linesTableView`/`renderPdfTab` | เมื่อ end-bill on → โชว์ ลดฐาน → ฐานใหม่ → VAT คิดใหม่ (Rule 2) |
| 5 | `renderRefTab` (ภ.พ.30 + JE) · detail · submit modal · list stat/row · csv · onFinalApprove audit · pdfParts | ตัวเลข "ภาษีขายที่ลด" ทุกจุด → `netVat` (VAT ที่ลดจริง) · JE บาลานซ์ (`netBefore + netVat = grand`) |

**ไม่แตะของอื่น:** FIX-01/02/03 status guards · FIX-04 legal_basis · FIX-05 anchors · FIX-06 ออกเอกสารแก้ไข · FIX-08 busyGate · FIX-09 demo-only · modal-z / line-cap / real-upload · per-line VAT engine · ไม่เพิ่ม dependency/CDN · ไม่แตะ BASE-KIT

---

## Pass R — Render Gate (browser · venv playwright 1360×900 · `pageerror=0 · console=0`)

หลักฐานภาพ (INV-2026-0141 · ฐาน 360,000):

| ภาพ | ตรวจ | ผล |
|---|---|---|
| `_shots/08_endbill_vat_step3.png` | สรุปยอด end-bill 10% | ✅ ก่อน VAT 360,000 → ลดฐาน −36,000 → ฐานใหม่ 324,000 → VAT(ม.86/10) +22,680 → สุทธิ 346,680 · ภ.พ.30 −22,680 |
| `_shots/09_endbill_cap_warn.png` | ส่วนลดเกินเพดาน (Rule 1) | ✅ hint "ลดได้สูงสุด ฿385,200" (แดง) + hard-warn banner · clamp → ฐาน 0 · VAT 0 · **สุทธิ ฿0.00 (ไม่ติดลบ)** |
| `_shots/10_endbill_ref_je.png` | ภ.พ.30 + JE (R2+10%) | ✅ ฐานภาษีที่ลด 1,800 · ภาษีขายที่ลด **126.00** (ลดจาก 140) · JE 4120=1,800 · 2150=126 · บาลานซ์กับ AR 1,926 |
| `_shots/11_endbill_pdf.png` | PDF preview | ✅ ก่อนภาษี → ลดฐาน → มูลค่าหลังหักส่วนลด → VAT (ลดแล้ว) → รวมทั้งสิ้น |

หมายเหตุ: `resolveDoa` อ่าน `totals().grand` → grand ≥ 0 เสมอหลัง clamp → tier DOA ทำงานปกติ (ยืนยันใน e2e E09b)

---

## NEW issues จากการแก้
**ไม่มี.** audit.sh FAIL=0 คงเดิม · self_audit residual ≤ golden · pageerror/console=0 · guards/FIX เดิมไม่ถูกแตะ · per-line VAT engine verbatim

## NOT-CHECKED
- `static_scan.py` — ไม่มีใน generator เวอร์ชันนี้ → audit.sh เป็น mechanical gate หลัก
- Golden Compare รายพิกเซล — โครง archetype ไม่ถูกแตะ (แก้เฉพาะแถวสรุป/ตัวเลข VAT · เทียบเชิงโครงจาก render แล้วตรง)
- e2e (step 5) = ขอบเขต qc-coverage/e2e (รายงานแยก: FN 21/21 · 33/33 PASS · +2 เคสใหม่ end-bill VAT/cap)
