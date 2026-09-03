# Coverage Report (รอบ 1 · HTML vs Contract) — F-HR-TRAIN (อบรม / Training) — **RE-GATE รอบ 2 หลังแก้ BUG-03 + BUG-04**

- วันที่: 2026-09-03 · WF-01 step 4 (re-gate รอบ 2) · skill `qc-coverage-checker`
- Artifact: `outputs/F-HR-TRAIN/อบรม.html` (archetype = master · แก้ 7 FIX + BUG-03 + BUG-04 แล้ว)
- Contract: `PREBRIEF.md` (12 S · 10 BR · §12 declarations) + `FUNCTION_CHECKLIST.html` (18 FN + unsupported 5)
- Declarations pack: DOA_BRIEF · NTF_BRIEF · CSQ_BRIEF · NOT_NEEDED (DOCCFG/PDF)
- Global (Cube_Feature_List F133): dec = [doa, csq] + ntf · dep = Rate Card (ยังไม่สร้าง → EC placeholder display-only) · locked: DOA gate เมื่อ has_cost · EC ไม่มี AC · 3 hook display-only · cert soft ref

## Verdict: 🟢 PASS (คงเดิม — ไม่มีอะไรหลุด)

| Metric | ผล |
|---|---|
| FN ครอบ | **18 / 18** (ทุกข้อมี handler จริง เดินได้ · ไม่มีตัวไหนหายจากการแก้บั๊ก) |
| Scenario S-01..S-12 | 12 / 12 เดินจบผลลัพธ์ได้ใน UI |
| capability จาก 7 FIX (spec c[]) | **5 / 5 ยังปรากฏบนจอ** (FIX-01..05 ครบ · FIX-03/04/05 ยืนยันด้านล่าง) |
| unsupported (ของห้ามมี) | 5 / 5 ยัง **ไม่มีทางทำบนจอ** — bug fix ไม่ได้เพิ่มความสามารถต้องห้าม |
| Declaration surface (0b) | DOA ✓ · NTF ✓ · CSQ ✓ · DOCCFG N/A (ถูกต้อง) — brief ครบ 3+1 |
| ขัด contract | 0 |
| Scope creep | 0 |
| BLOCK / WARN | 0 / 0 (1 NOTE ระดับ INFO — FN-10 framing, ยกมาจากรอบก่อน) |

> รอบนี้เปลี่ยนแค่ 2 จุด UI-affordance (BUG-03 · BUG-04) — ไม่แตะ FN/business/scope · การ assert เชิงลบจริง (unsupported ห้าม render) = งาน step 5 E2E · brief coverage เนื้อ FRD = งานรอบ 2 (step 10)

---

## Δ รอบ 2 — 2 บั๊กที่แก้ (ตรวจว่าไม่กระทบ coverage)

| BUG | อาการ | การแก้ | HTML surface | กระทบ FN? |
|---|---|---|---|:--:|
| BUG-03 | tooltip ปุ่ม "บันทึกผล" ตอน disabled ไม่ขึ้น (native title ไม่ยิงบน `disabled`) | หุ้มปุ่มด้วย `<span class="tt-wrap" title="…" style="display:inline-block">` | L2445 (ยังไม่ปิดรอบ) · L2446/L2714 (ยังไม่เช็คชื่อ) · L2718 | ไม่ — FN-06 `recordResult` guard เดิมครบ (closed L2778 · attended L2781/2791) · แค่เพิ่ม affordance บอกเหตุผล disabled |
| BUG-04 | combobox ใน modal ไม่กาง dropdown เองเมื่อโฟกัส | input มี `onfocus="ssOpen(key)"` (L1809) + `initSearchSelect` ตอน render modal | `enr_emp` L2910/2959 · `slot_i` L2934/2961 | ไม่ — FN-03 (เลือกผู้เรียน) + FN-08 (DOA slot picker) ยังเลือกคนได้จริง · combobox anatomy (#102) คงเดิม |

ทั้งสองเป็นการเพิ่ม/แก้ affordance ล้วน (span หุ้ม + onfocus open) — ไม่มีการแตะ handler ธุรกิจ · ไม่มี FN/S/BR/unsupported เปลี่ยน

---

## Coverage Matrix — 18 FN (ยังครบเหมือนรอบก่อน · verify ซ้ำหลังแก้บั๊ก)

| FN | ต้องทำได้ | HTML | Evidence (route/handler) |
|---|---|:--:|---|
| FN-01 | สร้างหลักสูตร (has_cost·งบ) | ✓ | `openCourseCreate()` L2520 → `submitCourse()` L2563 (budget เฉพาะ has_cost) |
| FN-02 | สร้างรอบอบรม (จำนวนรับ) | ✓ | `openSessionCreate()` L2523 → `submitSession()` L2649 · `coursePublish` L2884 |
| FN-03 | ลงทะเบียน (gap/เลือกเอง · เกินรับบล็อก) | ✓ | `openEnrollModal()` L2754 (guard `>=capacity`) · combo `enr_emp` L2910 (**BUG-04 ok**) → `submitEnroll()` L2758 · full → btn disabled L2699 |
| FN-04 | has_cost → DOA ก่อนยืนยัน | ✓ | `submitEnroll`: has_cost→`pending_doa` L2764/2767 |
| FN-05 | no-cost → ยืนยันเลย (ข้าม DOA) | ✓ | `submitEnroll` else → confirmed + audit "ข้าม DOA" L2771 |
| FN-06 | บันทึกผล ผ่าน/ไม่ผ่าน | ✓ | `openResultModal` L2776 → `recordResult()` L2795 · guard closed+attended L2778/2790 · ปุ่ม disabled หุ้ม tooltip (**BUG-03 ok**) |
| FN-07 | ออกใบรับรอง soft ref | ✓ | `issueCert()` L2799 → "ไม่มีเลขรัน / ไม่ออก PDF" L2804 |
| FN-08 | อนุมัติผ่าน DOA slot picker (ไม่ hardcode) | ✓ | modal doa `slot_i` combo L2934 (**BUG-04 ok**) · `empOpts()` L2165 · `enrollApprove()` L2815 |
| FN-09 | ค่าอบรม → EC display-only + ยิงมูลค่า | ✓ | EC block "อ้างอิง Rate Card" display-only L2604/2739 · sendEC L2843 (ไม่ post เอง) |
| FN-10 | gap → แนะนำ (hook display-only) | ✓* | `GAPS` mock อ่านอย่างเดียว L2185 `gapsForCourse()` · modal gap section L2908 — ดู NOTE-1 |
| FN-11 | ยกเลิกการลงทะเบียน | ✓ | `cancelEnroll()` L2808 → status='cancelled' (soft archive · คืนที่ว่าง) |
| FN-12 | แจ้งเตือน (เปิดรับ/ยืนยัน/ผล) | ✓ | `audit`+ntf: ยืนยัน L2771 · อนุมัติ L2822 · ผล L2795 |
| FN-13 | รายงาน completion rate + filter | ✓ | `renderReportTab()` L2466 · per-course completion L2483 · filter |
| FN-90 | ค้นหา/filter + empty | ✓ | filter-bar ทุก tab + `emptyStateHTML` (L2408 ฯลฯ) |
| FN-91 | ปิด/ยกเลิก confirm + soft archive | ✓ | `courseClose()` L2885 · `sessionClose` · `cancelEnroll` — ผ่าน `openConfirm()` |
| FN-92 | field validate + กัน double-submit | ✓ | `validateField` L1922 · `TC.busy` guard + btn disabled L2561/2647 |
| FN-93 | audit append-only | ✓ | `audit()` L2278 (unshift) · เรียกทุก create/approve/result/cancel/เช็คชื่อ |
| FN-94 | ปิดบังข้อมูลตาม role | ✓ | `maskMoney()` L2283 (viewer → `••••••`) · `viewerRO()` ซ่อนปุ่มสร้าง |

`*` = ✓ พร้อม NOTE (ไม่ลด verdict)

## Scenario trace (S-01..S-12)
S-01→FN-01 · S-02→FN-02 · S-03→FN-03 · S-04→FN-04/08 · S-05→FN-05 · S-06→FN-06 · S-07→FN-07 · S-08→FN-09 · S-09→FN-10 · S-10→FN-11 · S-11→FN-12 · S-12→FN-13 — เดินครบทุกเส้น

## Capability จาก FIX (spec c[]) — ยืนยันยังอยู่หลังแก้บั๊ก
| FIX | capability | HTML | Evidence |
|---|---|:--:|---|
| FIX-01 | บันทึกผลเฉพาะรอบ closed | ✓ | `isClosedResult()` L2272 · guard L2778/2790 · completion นับเฉพาะ closed L2470 |
| FIX-02 | function guards (canApprove/published) | ✓ | `canApprove` L2705 · session เฉพาะ published · `courseOpts` filter |
| FIX-03 | เช็คชื่อ + ประเมิน 1-5 | ✓ | `markAttendance` L2847-2853 · ต้อง attended ก่อนบันทึกผล L2781/2791 · evalScore ในผล L2795 |
| FIX-04 | ประวัติรายคน + ชั่วโมงสะสม | ✓ | `openEmpHistory()` L2858 (คลิกชื่อ L2725) → drawer + totalHours |
| FIX-05 | ต้นทุนต่อหัว (EC) ในรายงาน | ✓ | `costCourses` L2485 → cph-grid L2506 = งบ ÷ ผู้ผ่าน · mask ตาม role · "EC ไม่ลงบัญชี" |

## Declaration surface (Phase 0b)
| ท่อ | เงื่อนไข | HTML | brief | สรุป |
|---|---|:--:|:--:|---|
| DOA | has_cost → อนุมัติ | ✓ slot picker `slot_i` L2934 (ไม่ hardcode สาย) | DOA_BRIEF | ตรง §12 |
| NTF | เปิดรับ/ยืนยัน/ผล | ✓ 3 event + bell (ENG-NOTIFY dev-wire) | NTF_BRIEF | ตรง §12 |
| CSQ | มูลค่าอบรม → EC (ไม่มี AC) | ✓ EC display-only · ไม่มี AC บนจอ | CSQ_BRIEF | ตรง §12 + locked |
| DOCCFG | เลขรัน | — ไม่มีเลขรัน · cert soft ref · ไม่ Pattern Q | NOT_NEEDED | ตรง §12 (no) |

## ของห้ามมี (unsupported 5) — ยังไม่มีทางทำ (bug fix ไม่ได้เพิ่ม)
| # | ห้ามมี | ผล | หลักฐาน |
|---|---|:--:|---|
| 1 | จ่ายเงินค่าอบรมจริง/ลงบัญชี | ไม่มี | EC display-only · "EC ไม่ลงบัญชี" · ไม่มีปุ่ม post/จ่าย |
| 2 | ประเมินผลงาน/สร้าง gap เอง | ไม่มี | `GAPS` อ่านอย่างเดียว L2185 · ไม่มีปุ่มสร้าง gap (FIX-03 = ประเมิน**ผลอบรม** คนละเรื่อง) |
| 3 | eLearning/SCORM · competency mapping | ไม่มี | โผล่เฉพาะ oos list |
| 4 | ใบรับรองเลขรัน PDF | ไม่มี | `issueCert` "ไม่มีเลขรัน / ไม่ออก PDF" |
| 5 | สร้าง/แก้ config หมวดหลักสูตรกลาง | ไม่มี | `CATEGORIES` อ่านอย่างเดียว · `ctxStub('ตั้งค่า HR')` |

---

## NOTE (INFO · ไม่ลด verdict)
- **NOTE-1 · FN-10 framing (ยกมาจากรอบก่อน):** checklist = "gap → แนะนำ**หลักสูตร**" แต่ HTML gap hook = "แนะนำ**ผู้เรียน**ที่มี gap ตรงหลักสูตร/รอบนี้". ทิศกลับด้าน แต่ underlying hook (อ่าน Performance gap · display-only · ไม่สร้าง gap) ครบตาม OB-2/BR-07/S-09 → นับ **ครอบ** · ยกให้ BA ยืนยัน framing

## Diff จากรอบก่อน (re-gate รอบ 1 → รอบ 2)
- **ปิดแล้ว:** ไม่มี gap ค้าง (รอบ 1 = PASS)
- **เปลี่ยน:** BUG-03 (disabled result btn หุ้ม `tt-wrap` span → tooltip ขึ้น) · BUG-04 (modal combobox `onfocus→ssOpen` กาง dropdown) — ทั้งคู่ UI-affordance ล้วน
- **coverage:** FN 18/18 · FIX 5/5 · unsupported 5/5 · declaration 3+1 — **ไม่มีอะไรหาย ไม่มีอะไรเกิน**
- **ยังค้าง (INFO):** NOTE-1 (FN-10 framing) — ไม่บล็อก

## Quality gate ของ checker
- [x] ทุก ✓ มี evidence ระบุตำแหน่ง (route/function/บรรทัด)
- [x] ไม่ invent เกณฑ์นอก contract
- [x] scope creep flag แล้ว (= 0 · BUG-03/04 = affordance ไม่ใช่ feature ใหม่)
- [x] BLOCK เมื่อ block-severity ไม่ครอบ — ไม่มี
- [x] Declaration coverage (0b) ครบ 4 ท่อ
- [x] 18 FN ยังครบหลัง BUG-03/04 · unsupported 5/5 ยังไม่มีทางทำบนจอ
