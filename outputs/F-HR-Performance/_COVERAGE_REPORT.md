# _COVERAGE_REPORT — F131 Performance (ประเมินผลงาน)

| | |
|---|---|
| Feature | **F131 Performance** · mod HR · arch **master** · wave **W2** · dec (central plan) `[doa, csq]` |
| Round | **รอบ 1 · HTML vs Contract** (REPORT mode — ไม่แก้ HTML) |
| Artifact ตรวจ | `outputs/F-HR-Performance/performance.html` (2,808 บรรทัด · single-file SPA) |
| Contract | PREBRIEF (master · 12 S · 10 BR) + FUNCTION_CHECKLIST (FN ใน JS PAYLOAD ~ln 215 · 18 FN) + central plan row F131 + BA fix order (`REVIEW_FIX_ORDER_F131`) |
| วันที่ · ผู้ตรวจ | 2026-09-09 · qc-coverage-checker (round 1) |
| บริบทรอบนี้ | **Re-run หลังลง 2 มติ PM/BA** — **(OQ-PERF-01)** อนุญาต re-open ผลที่เผยแพร่แล้ว (authorized HR + เหตุผลบังคับ + audit ผู้แก้) · **(OQ-PERF-03)** narrow scope หัวหน้า → เฉพาะแผนกตัวเอง (staff=SELF · mgr=DEPT · hr=ALL) · comment-only: **OQ-PERF-02** (CSQ per-person publish) + **OQ-PERF-04** (team-calibration คงไว้) mark resolved |
| **VERDICT** | 🟢 **PASS** — FN 18/18 · S 12/12 · Negatives 4/4 absent · Decl doa+ntf+csq hook present · no scope creep · 2 มติ present + guards intact |

---

## 0. สรุปผล 2 มติ PM/BA (จุดโฟกัสรอบนี้)

**มติ A — OQ-PERF-01 · re-open ผลที่เผยแพร่แล้ว (authorized + audited)** ✅ ยืนยันแล้ว · เพิ่ม affordance ใหม่ ไม่ทำ coverage หาย
- **ทางเข้า UI 2 จุด**: ปุ่ม "เปิดแก้ไขผล" ใน `apprView` list (ln 2365 · เงื่อนไข `canReview && !closed`) + ปุ่มใน drawer footer (ln 2476 · `!cycleClosed(a) && a.status==='published' && sec.can('reopen')`)
- **Modal เหตุผลบังคับ**: `m.type==='reopen'` (ln 2665) · `#reopenReason` textarea + `#reopenErr` (ln 2673-2675)
- **Handler + guards ครบชั้น** — `doReopen(id)` (ln 2751):
  - open cycle เท่านั้น: `if(cycleClosed(a)) return` (ln 2753 · FIX-05 ยังคุม)
  - authorized เท่านั้น: `if(!sec.can('reopen'))` → `sec.can` คืน `!!r.manage` = **HR เท่านั้น** (ln 2211) · mgr/staff กดไม่ได้
  - published เท่านั้น: `if(a.status!=='published') return` (ln 2755) — explicit transition
  - เหตุผลบังคับ non-empty: `if(!reason)` block (ln 2757)
  - **audit "ใครแก้"**: `pushAudit(id,'เปิดแก้ไขผลหลังเผยแพร่ · เหตุผล: '+reason)` (ln 2760) → `pushAudit` stamp `who:curRole().name` + `at` (ln 2616 · append-only unshift)
  - **state transition ใหม่ published→mgr**: `a.status='mgr'; a.decision=''; delete a.approvals` (ln 2761) → ส่งกลับขั้นหัวหน้า → แก้ → สอบทาน (DOA เดิม) → เผยแพร่ใหม่ ผ่าน flow เดิม (CSQ 7C ยิงซ้ำ per-person)
- **ไม่กระทบ guard เดิม**: FIX-01/02/03/05 (precondition · no-backward · role · closed-lock) ยังอยู่ — re-open เป็น **ทางที่ตั้งใจ** ผ่านสิทธิ์+เหตุผล+audit ไม่ใช่ bypass

**มติ B — OQ-PERF-03 · narrow scope หัวหน้า → เฉพาะแผนกตัวเอง** ✅ ยืนยันแล้ว · เป็น RESTRICTED tightening (FN-94) ไม่ใช่ coverage loss
- `scopeSelf(list)` (ln 2218): `r.mask` → SELF (`a.emp===r.name`) · `r.id==='mgr'` → **DEPT** (`a.dept===r.dept`, ln 2220) · else → **ALL** (HR manage, ln 2221)
- ใช้ทุกจุดที่ list ผล: `apprView` (ln 2285) · overdue (ln 2288) · calibration team view (ln 2321) · review queue+done (ln 2341-2342)
- **detail-open guard**: mgr เปิดแบบประเมินนอกแผนกไม่ได้ → banner RESTRICTED (ln 2484-2485)
- mock role `mgr` = `dept:'ฝ่ายผลิต'` (ln 2146) → เห็นเฉพาะ A2 (ฝ่ายผลิต) · **HR (manage) ยังเห็น ALL** — FN ทุกข้อยัง reachable เต็มผ่าน role HR

**Comment-only (resolved, ไม่แตะ DOM)**:
- OQ-PERF-02 → CSQ hook comment ปรับเป็น "RESOLVED: per-person publish" (ln 1563) · 7C hook คงทำงาน (ln 2725)
- OQ-PERF-04 → team-calibration view (FIX-08) **คงไว้** — `calibView`/team compare ยังอยู่ (ln 2321) ไม่ถูกตัด

---

## 1. FN Coverage Matrix (18/18) — HTML round 1

| FN | ต้องทำได้ | HTML evidence (route/selector/handler) | ผล |
|---|---|---|:--:|
| FN-01 | สร้างรอบ (ดึงจาก HR Config) → เปิดกรอก | `openDrawer('newCycle')` · อ่าน `PERF.configCycles` (#107 "อ่านมาใช้ ไม่สร้างเอง") · `initSearchSelect('cfgCycle')` ln 2778 · save | ✓ |
| FN-02 | ตั้ง KPI/น้ำหนักรวม 100% | `saveKpi` ln 2565 · guard `sum!==100` block · wsumTag ok/bad | ✓ |
| FN-03 | พนักงานประเมินตนเอง | `saveSelf` ln 2581 · guard status `self` + คะแนน 1–5 ครบ | ✓ |
| FN-04 | หัวหน้าประเมิน + weighted ถูก | `saveMgr` ln 2590 · live weighted `scoreText(a)` · totbox | ✓ |
| FN-05 | สอบทาน (calibration) + decision | `doCalibStage` ln 2704 · `doCalibSend` ln 2683 · decision ผ่าน/ทบทวน(PIP)/ไม่ผ่าน · publish | ✓ |
| FN-06 | ผล → gap → ส่ง Training (hook display-only) | `sendTraining` ln 2768 (toast "ไม่สร้างหลักสูตรในหน้านี้") · ปุ่มใน hookbox ln 2371 | ✓ |
| FN-07 | ผล → event ปรับเงินเดือน/ตำแหน่งให้ Movement (ไม่ปรับเอง) | `sendMovement` ln 2769 (toast "ไม่ปรับเอง") · decouple จาก gap (ln 2367) | ✓ |
| FN-08 | สอบทานผ่าน DOA slot picker ตามตำแหน่ง (ไม่ hardcode) | modal `doaCalib` `.slot-row` doa0/doa1 slot **ว่าง** · `doCalibSend` resolve person จริง ln 2683 (FIX-06 no preset) | ✓ |
| FN-09 | ประเมินไม่ครบ/เกินกำหนด → เตือน | `isOverdue` ln 2203 · banner overdue + `sendReminder` ln 2772 · คอลัมน์ "เกินกำหนด" | ✓ |
| FN-10 | คะแนนต่ำ/ไม่ผ่าน → PIP + decision | ปุ่ม "เปิดแผน PIP" เมื่อ decision includes "ทบทวน" ln 2475 · modal `pip` + `doPip` ln 2739 | ✓ |
| FN-11 | ปิดรอบ (ล็อกแก้) | modal `closeCycle` + `doCloseCycle` ln 2732 set `closed` · **ล็อกจริง**ผ่าน `cycleClosed` guard (ln 2215) | ✓ |
| FN-12 | แจ้งเตือน รอบเปิด/ครบกำหนด/ผล | notif panel (FN-12) · `PERF.notifs` push ตอน publish · head "รอบเปิด · ครบกำหนด · ผล" | ✓ |
| FN-13 | รายงานกระจายคะแนน (distribution) + filter | `reportView` (dispatch ln 2267) · dist A/B/C/D · filter-row "การกระจายคะแนน" | ✓ |
| FN-90 | ค้นหา/filter + empty state | `state.f {search,status}` · `.empty` component + emptyState · ss-empty | ✓ |
| FN-91 | ปิด/ยกเลิกผ่าน confirm + soft archive | modal ยืนยัน "ปิดรอบประเมิน?" · `closeModal`/ghost ยกเลิก · pill-archived + soft archive | ✓ |
| FN-92 | validate + กัน double-submit | `state._busy` guard ต้นทุก mutation (saveKpi/saveSelf/saveMgr/doCalib*/doPip/doCloseCycle/**doReopen** ln 2752) · field validate | ✓ |
| FN-93 | audit ทุก create/แก้/สอบทาน (append-only) | `pushAudit` unshift (append-only ln 2616) · stamp who=`curRole().name` + at · **re-open ก็ audit ผู้แก้** ln 2760 | ✓ |
| FN-94 | ปิดบังผลประเมิน (RESTRICTED) ตาม role | `mask()` ln 2202 · `scopeSelf` ln 2218 (staff=SELF · **mgr=DEPT ใหม่** · hr=ALL) · RESTRICTED banner ln 2482/2485 | ✓ |

**FN: 18/18 ✓** — ทุก FN มี handler เดินได้จริง (ไม่ใช่ปุ่มหลอก) · 2 มติ = **เพิ่ม affordance (re-open) + narrow view (dept)** ไม่ตัด FN ใด · HR (manage) ยัง reach ครบ 18/18

---

## 2. Scenario Coverage (S-01..S-12) — 12/12 reachable

| S | เรื่อง | ทางเดินใน UI | ผล |
|---|---|---|:--:|
| S-01 | สร้างรอบ (จาก HR Config) → เปิดกรอก | tab รอบ → สร้างรอบ (config lookup) | ✓ |
| S-02 | ตั้งเป้า/KPI ต่อคน (น้ำหนัก) | drawer แบบประเมิน → KPI editor → saveKpi | ✓ |
| S-03 | พนักงานประเมินตนเอง | สถานะ self → saveSelf | ✓ |
| S-04 | หัวหน้าประเมิน + คะแนน | สถานะ mgr → saveMgr → weighted | ✓ |
| S-05 | สอบทาน (calibration · DOA · DC decision) | doaCalib 2 ขั้น → doCalibSend/Stage → publish+decision · **+ re-open ผลได้ (HR · เหตุผล · audit) → กลับ mgr → เผยแพร่ใหม่** | ✓ |
| S-06 | ผล → gap → ส่ง Training (hook) | reviewView hookbox → sendTraining | ✓ |
| S-07 | ผล → Movement **event (ไม่ CRUD)** | sendMovement (toast display-only, ไม่ปรับเอง) | ✓ |
| S-08 | ประเมินไม่ครบ/เกินกำหนด → เตือน | isOverdue banner + sendReminder | ✓ |
| S-09 | คะแนนต่ำ/ไม่ผ่าน → PIP/decision | decision "ทบทวน" → เปิดแผน PIP | ✓ |
| S-10 | ปิดรอบ (ล็อกแก้) | doCloseCycle → cycleClosed lock | ✓ |
| S-11 | แจ้งเตือน รอบเปิด/ครบกำหนด/ผล | notif panel + push publish | ✓ |
| S-12 | รายงานการกระจายคะแนน | reportView distribution + filter | ✓ |

**S: 12/12 ✓** — S-05 ได้ transition ใหม่ published→mgr (re-review) เป็น alt path ในตัว scenario เดิม ไม่ใช่ S ใหม่

---

## 3. Negatives / Scope Guard (unsupported 4/4 — ต้อง ABSENT) — ✅ 4/4 absent

| ห้ามมี (FUNCTION_CHECKLIST unsupported) | ตรวจใน HTML | ผล |
|---|---|:--:|
| ปรับเงินเดือน/เลื่อนตำแหน่งเอง | ไม่มี field/ปุ่มแก้เงินเดือน — มีเฉพาะ `sendMovement` = event display-only "(ไม่ปรับเอง)" ln 2769 · sidebar "เงินเดือน" (ln 1527) = nav link ไป feature อื่น ไม่ใช่ CRUD ในหน้านี้ | ✅ absent |
| 360 feedback / competency model / continuous check-in | grep `360`/`competency`/`check-in` = พบเฉพาะ `rotate(360deg)` CSS keyframe (ln 732) ไม่ใช่ feature | ✅ absent |
| สร้าง/แก้รอบประเมิน-แบบฟอร์มกลาง | รอบ**อ่านจาก** `configCycles` (#107) — ไม่มี CRUD master | ✅ absent |
| ทำหลักสูตรอบรม | `sendTraining` toast "ไม่สร้างหลักสูตรในหน้านี้" ln 2768 — display-only hook | ✅ absent |

**Scope creep: ไม่พบ** — re-open (OQ-PERF-01) + dept-scope (OQ-PERF-03) เป็น **มติ PM/BA สั่งลง** ไม่ใช่ของเกิน · `sendSuccession` (ln 2771) เป็น display-only hook สอดคล้อง c[5] (FIX-09) ไม่ใช่ scope creep

---

## 4. Declaration Coverage (Phase 0b) — hook present · brief NOT-CHECKED (step 4)

| ท่อ | เข้าเงื่อนไข? | HTML hook (round 1) | Brief (step 7) | ผล |
|---|---|---|---|:--:|
| **DOA** | ✅ S-05 สอบทานผล (ไม่มีวงเงิน) | `.slot-row` slot picker person จริง (doa0/doa1 **ว่าง** ไม่ preset · FIX-06) · ไม่ hardcode chain · `doCalibSend` ln 2683 | `DOA_BRIEF_F131.md` ยังไม่มี | ✓ hook / brief NOT-CHECKED |
| **NTF** | ✅ S-01 รอบเปิด · S-08 ครบกำหนด · S-05 ผล | notif panel FN-12 · `PERF.notifs` push ตอน publish · sendReminder · map → S-01/S-08/S-11 | `NTF_BRIEF_F131.md` ยังไม่มี | ✓ hook / brief NOT-CHECKED |
| **CSQ** | ✅ S-04/S-05 ผล→SecC · S-05 decision→DC | **7C hook คงอยู่** (FIX-07): audit "บันทึกผลประเมินเข้า 7C" ln 2725 + toast ln 2728 + comment ln 1563 (OQ-PERF-02 RESOLVED per-person publish) · ไม่ประกาศ OC/DC | `CSQ_BRIEF_F131.md` ยังไม่มี | ✓ hook / brief NOT-CHECKED |
| DOCCFG | ❌ ไม่มีเลขรัน | — | — | N/A |
| PDF DOC | ❌ ไม่มีเอกสารคนถือ | — | — | N/A |

> **หมายเหตุ step 4**: `*_BRIEF.md` ทั้ง 3 ท่อ **ยังไม่ต้องมี** — ผลิตหลัง step 7 (frd-generator + companion declaration). รอบ 1 ตรวจแค่ว่า **HTML มี hook จริง** → ครบทั้ง 3. Brief coverage เต็มไปตรวจรอบ 2.

### DIVERGENCE (chip ≠ detect) — resolved
- **central plan row F131 `dec:[doa, csq]`** ไม่มี `ntf` · แต่ PREBRIEF §12 + HTML มี NTF hook จริง (notif/reminder/publish) → detect = **doa + ntf + csq**
- สถานะ: **resolved → declaration รอบนี้ = doa + ntf + csq** (ntf divergence เคาะแล้ว) · ไม่บล็อก (hook มีครบ · brief ผลิต step 7)

---

## 5. Gap list

**ไม่มี gap ระดับ BLOCK/WARN ในรอบ 1** — ทุก FN/S มี hook เดินได้จริง · negatives absent ครบ · declaration hook ครบ 3 ท่อ · 2 มติ PM/BA present + guards intact

**Diff กับรอบก่อน (ก่อนลง 2 มติ):**
- ปิดใหม่: OQ-PERF-01 (re-open flow) + OQ-PERF-03 (dept-scope) — เดิมค้างเป็น OQ ตอนนี้ลงจอแล้ว
- ยังค้าง (ยกไป step ถัดไป · ไม่ใช่ gap ของ HTML):
  1. `DOA/NTF/CSQ_BRIEF_F131.md` — ผลิต + sync read ใน FRD (step 6-7) → ตรวจเต็มรอบ 2
  2. OQ-PERF-02 (CSQ EC valuation detail) — resolved "per-person publish" แล้ว · รายละเอียดมูลค่า EC = architect item (คงรอสถาปนิก ตอน FRD §Integration)

---

## 6. Checker self-gate
- [x] ทุก ✓ มี evidence ระบุตำแหน่ง (route/selector/บรรทัด · line ปรับตามไฟล์ 2,808 บรรทัด)
- [x] ไม่ invent เกณฑ์นอก contract (PREBRIEF + FUNCTION_CHECKLIST + central plan row + BA fix order)
- [x] item ที่ยังตรวจไม่ได้ = NOT-CHECKED (brief 3 ท่อ · รอ step 7) ไม่ mark ✓
- [x] scope creep flag แล้ว: ไม่พบ (2 มติ = PM/BA-mandated ไม่ใช่ creep)
- [x] Declaration coverage (0b) ตรวจครบ · DIVERGENCE (ntf) ลง report + resolved
- [x] re-open affordance ตรวจครบชั้น: entry×2 + modal เหตุผลบังคับ + guard (open/authorized/published) + audit ผู้แก้ + transition published→mgr
- [x] dept-scope ตรวจครบ: scopeSelf (SELF/DEPT/ALL) + detail-open guard · HR ยัง ALL → FN 18/18 reachable
- [x] VERDICT = **PASS** (ไม่มี block-severity ไม่ครอบ)
