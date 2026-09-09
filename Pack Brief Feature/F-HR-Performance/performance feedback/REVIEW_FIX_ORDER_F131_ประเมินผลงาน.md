# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
HR — F131 Performance (ประเมินผลงาน) · performance.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F131 Performance (ประเมินผลงาน) · mod HR · arch master · dec: doa + csq |
| ไฟล์ที่ตรวจ | performance.html (2,637 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-09 · BA gate (html-review-fix-order) |
| ขอบเขต | Re-gate ก่อนเข้า Phase B (FRD/TC) — เทียบ spec F131 + governance + interaction จริง |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK ทุก block · audit **FAIL=0** WARN=2 (kit residuals) · Playwright **pageerror=0** |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 5 · HIGH 4 · MINOR 2 → แก้แล้วส่ง re-gate เต็มรอบ |

## 1. สรุปผลตรวจ (Executive Summary)

ส่วนที่ทำถูก: state machine รายแบบประเมินออกแบบครบ (goal → self → mgr → calibration → published) · KPI editor บังคับน้ำหนักรวม 100% (พิสูจน์แล้ว — sum 90 ถูก block) · double submit กันด้วย `_busy` (audit เกิด entry เดียว) · empty submit รอบใหม่ถูก block · รอบประเมินอ้าง config จากตั้งค่า HR (ไม่ hardcode — สอดคล้อง HR-1) · UI ฝั่ง edit gate ตาม role บางส่วน (KPI แก้ได้เฉพาะ goal+manage · คะแนนหัวหน้าแก้ได้เฉพาะ mgr role/manage) · sendMovement/sendTraining เป็น display-only hook ไม่ mock หน้าจอ feature อื่น ✓ · Esc/overlay/pageerror สะอาด

ประเด็นที่ต้อง **BLOCK**: ชั้น function ของทุก transition ไม่มี guard — พิสูจน์จากการรันจริง: (1) สอบทาน+เผยแพร่ผลแบบประเมินที่ยังอยู่ขั้น "ตั้งเป้า" (คะแนนหัวหน้า null ทั้งหมด) ได้ decision "ผ่าน" (2) แบบประเมินที่เผยแพร่ผลแล้วถูกดันสถานะถอยกลับและแก้คะแนนได้ (3) persona พนักงานเรียกบันทึกผลหัวหน้าเองสำเร็จ — audit บันทึกชื่อพนักงานเป็นผู้ประเมิน (4) persona พนักงานเห็น decision + Gap ของเพื่อนร่วมงานทุกคน (ขัด "เกรดเป็นความลับต่อคน") พร้อมปุ่มสอบทาน/เปิด PIP กดได้ (5) ปิดรอบแล้ว "ล็อกการแก้ไข" เป็นแค่ toast — ยัง mutate ได้จริง นอกจากนี้ dec `csq` ถูกประกาศไว้แต่ **ไม่มี CSQ hook แม้แต่จุดเดียวในไฟล์** และ c[5] ขาด hook ฝั่ง Succession

### 1.1 ความครบถ้วนเทียบ Spec F131

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| ตั้งเป้ารายคน + น้ำหนัก | ✅ | KPI editor + add/del + guard น้ำหนักรวม=100 (P6 ผ่าน) |
| ประเมินตนเอง/หัวหน้า + คอมเมนต์ | ✅ กลไก / ⚠️ guard | ฟอร์มคะแนน 1–5 + note ครบ แต่ transition เรียกข้าม/ย้อนได้ (FIX-02) |
| calibrate เกรดระดับทีม/บริษัท | ⚠️ บางส่วน | มี "สอบทานรายคน" (DOA) แต่ไม่มีมุม calibrate ระดับทีม/บริษัท — ไม่มี view เทียบ distribution ก่อนเคาะ (FIX-08) |
| อนุมัติผล + แจ้งรายบุคคล | ⚠️ บางส่วน | มี modal สอบทาน + notif เผยแพร่ผล แต่คลิกเดียวจบ 2 ขั้น + slot ผู้สอบทาน auto-preset (FIX-01/06) |
| ส่งผลเข้า Movement/Succession/Training | ⚠️ บางส่วน | sendMovement ✓ sendTraining ✓ (display-only) — **Succession = 0 ทั้งไฟล์** (FIX-09) |
| dec: doa | ⚠️ | มี slot picker ตามตำแหน่ง + ข้อความ "ไม่ hardcode" แต่ค่า default ถูก preset ให้ (P1/P2) — เจตนา "เลือกคนจริง" ตามมติ 2026-08-17 หายไป (FIX-06) |
| dec: csq | ❌ | grep CSQ/7C/csq = 0 — chip ประกาศแต่ไม่มี hook (FIX-07) |
| d: เกรดเป็นความลับต่อคน | ❌ | คะแนน mask แต่ decision + Gap เปิดให้ persona พนักงานเห็นของทุกคน (FIX-04, screenshot) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] doCalib ไม่มี precondition guard — เผยแพร่ผลข้ามขั้นได้ทั้ง flow

| ช่อง | รายละเอียด |
|---|---|
| อาการ | สอบทาน+เผยแพร่ record ที่ยังอยู่ขั้นตั้งเป้า (ไม่มีคะแนนหัวหน้าเลย) สำเร็จ |
| หลักฐาน | Bypass P2: record status `goal` · mgr scores `[null,null]` → `doCalib()` → `{status:'published', decision:'ผ่าน'}` |
| ผลกระทบ | คนที่ยังไม่ถูกประเมินเลยได้ผล "ผ่าน" เข้า Movement/เงินเดือนได้ — data integrity เพี้ยนทั้งสาย |
| ตำแหน่ง | `function doCalib(id)` |
| วิธีแก้ | guard ต้น function: status ต้องเป็น `calibration` และ `rawScore(a)!=null` (ทุก KPI มีคะแนนหัวหน้า) — ไม่ผ่าน toast + return |

เกณฑ์ตรวจรับ: doCalib กับ record goal/self/mgr/published → ไม่เปลี่ยน + toast · record calibration ที่คะแนนครบ → published ได้

### FIX-02 · [CRITICAL] Transition ย้อนหลัง — record เผยแพร่แล้วถูกดันกลับ/แก้คะแนนได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `saveSelf`/`saveKpi`/`saveMgr` ไม่เช็คสถานะปัจจุบัน — เรียกกับ record published ได้ สถานะถอยกลับและคะแนนถูกแก้หลังประกาศผล |
| หลักฐาน | Bypass P1: A5 `{status:'published', decision:'ผ่าน'}` → `saveSelf()` → status `mgr` |
| ผลกระทบ | ผลประเมินที่ประกาศแล้ว (ฐานปรับเงินเดือน) แก้ย้อนได้เงียบ ๆ — ขัด append-only + terminal state |
| ตำแหน่ง | `saveKpi` · `saveSelf` · `saveMgr` |
| วิธีแก้ | guard ตามขั้น: saveKpi เฉพาะ `goal` · saveSelf เฉพาะ `self` · saveMgr เฉพาะ `mgr` — สถานะอื่น toast + return · การแก้หลังเผยแพร่แขวน OQ-PERF-01 |

เกณฑ์ตรวจรับ: เรียกทั้งสาม function กับ record ทุกสถานะที่ไม่ตรงขั้นตัวเอง → ไม่เปลี่ยน · flow ปกติเดินครบ goal→…→published

### FIX-03 · [CRITICAL] Role guard หลุด — พนักงานประเมินแทนหัวหน้า/สอบทานเองได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | function ไม่เช็ค role: persona พนักงานเรียก `saveMgr` สำเร็จ — audit บันทึก who = ชื่อพนักงานเอง · ฝั่ง UI แท็บสอบทานยังโชว์ปุ่ม "สอบทาน (DOA)" / "เปิดแผน PIP" / "ส่งเรื่องปรับตำแหน่ง" ให้ persona พนักงานกด |
| หลักฐาน | Bypass P3: role `staff` → `saveMgr(A3)` → `mgr→calibration` · audit `who:'สมชาย ใจดี'` · Screenshot staff_review (ปุ่มครบทุกตัวใน persona พนักงาน) |
| ผลกระทบ | permission หลุดทั้ง UI และ function — พนักงานเดินผลตัวเอง/เพื่อนจนถึงเผยแพร่ได้ |
| ตำแหน่ง | `saveMgr` · `doCalib` · `doPip` · `doCloseCycle` · `sendMovement/sendTraining` · `reviewView` (render ปุ่ม) |
| วิธีแก้ | ใช้ flag ที่มีอยู่: `curRole().manage` (HR) / `curRole().id==='mgr'` — (a) function: saveMgr ต้อง mgr/manage · doCalib/doPip/doCloseCycle/send* ต้อง manage (b) UI: reviewView ไม่ render ปุ่ม mutation ให้ role ที่ไม่ผ่าน — mirror sec.can() |

เกณฑ์ตรวจรับ: role staff เรียกทุก mutation ข้างต้นตรง → state ไม่เปลี่ยน · staff ไม่เห็นปุ่มเหล่านี้ · hr/mgr ทำงานตามสิทธิ์เดิม

### FIX-04 · [CRITICAL] RESTRICTED leak — พนักงานเห็น decision + Gap ของทุกคน

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `mask()` ปิดเฉพาะตัวเลขคะแนน — persona พนักงานเปิดแท็บ "สอบทาน + ผล & Gap" เห็นรายชื่อทุกคนพร้อม decision (ผ่าน/ทบทวน PIP/ไม่ผ่าน) และ Gap ("ทักษะการนำเสนอ", "ความถูกต้องในงาน") แบบไม่ปิดบัง |
| หลักฐาน | Screenshot staff_review + evaluate `{hasDecision:true}` ใน persona staff |
| ผลกระทบ | decision+Gap = เกรดโดยพฤตินัย — ขัด design constraint "เกรดเป็นความลับต่อคน" (RESTRICTED) ตรง ๆ |
| ตำแหน่ง | `reviewView` · `apprView` (คอลัมน์ผลการตัดสิน) · `tabDetail` |
| วิธีแก้ | scope SELF สำหรับ role staff: เห็นเฉพาะแบบประเมิน/ผลของตนเอง — แท็บสอบทานซ่อนทั้งแท็บ (หรือกรองเหลือของตน) · decision/gap ของคนอื่นใช้ `mask()` เดียวกับคะแนน · ระบุ scope_type ใน SEC_BRIEF ตอน FRD |

เกณฑ์ตรวจรับ: role staff เห็นเฉพาะข้อมูลตนเอง — ไม่มีชื่อ/decision/gap คนอื่นใน DOM · hr/mgr เห็นตาม scope เดิม

### FIX-05 · [CRITICAL] ปิดรอบไม่ล็อกจริง — "ล็อกการแก้ไข" เป็นแค่ toast

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `doCloseCycle` set `closed` แล้วจบ — แบบประเมินในรอบที่ปิดยังถูก mutate ได้ทุก function |
| หลักฐาน | Bypass P4: CY1 → closed → `saveSelf(A2)` → `self→mgr` สำเร็จ |
| ผลกระทบ | ขัด microcopy ตัวเอง + รอบที่ปิด (ฐานข้อมูลส่งต่อ Movement) แก้ย้อนได้ |
| ตำแหน่ง | ทุก mutation ที่แตะ appraisal (`saveKpi/saveSelf/saveMgr/doCalib/doPip`) |
| วิธีแก้ | guard ร่วม: `if(cyc(a.cycle).status==='closed') return showToast('รอบนี้ปิดแล้ว — แก้ไขไม่ได้','warning')` ต้นทุก function |

เกณฑ์ตรวจรับ: รอบ closed → ทุก mutation ถูก block · รอบ open ทำงานปกติ

### FIX-06 · [HIGH] DOA slot auto-preset + คลิกเดียวจบ 2 ขั้นสอบทาน

| ช่อง | รายละเอียด |
|---|---|
| อาการ | slot ผู้สอบทานถูก preset `value:'P1'/'P2'` อัตโนมัติ (modal เปิดมาขั้น 2 มีชื่อ "สุนิสา คำแก้ว" แล้ว) และปุ่มเดียว "สอบทาน + เผยแพร่ผล" ทำทั้งเลือกผู้สอบทาน 2 ขั้น + decision + publish ใน action เดียว โดยผู้สอบทานตัวจริงไม่ได้กระทำ |
| หลักฐาน | evaluate `ssGet('doa0').value='P1'`, `ssGet('doa1').value='P2'` ทันทีที่ modal เปิด · Screenshot modal_doacalib |
| ผลกระทบ | ขัดเจตนามติ 2026-08-17 (ผู้ส่งต้องค้นหา/เลือก "คน" จริงต่อตำแหน่ง) และขัด DOA chain — ซ้ำ class เดียวกับ F102 FIX-03 |
| ตำแหน่ง | `initFeatureSelects` (doa0/doa1 `value:'P1'/'P2'`) · `doCalib` · `modalHTML` doaCalib |
| วิธีแก้ | (a) `value:null` ทั้งสอง slot — บังคับเลือกจริง (validation มีอยู่แล้ว) (b) แยกจังหวะ: ส่งสอบทาน = resolve+freeze รายชื่อ (สถานะคง calibration) → ผู้สอบทานแต่ละขั้นบันทึกผลของตน → ขั้นสุดท้ายค่อย publish — ขั้นต่ำต้องเป็น 2 action แยกกัน + timeline บันทึก at/ผู้กระทำต่อขั้น |

เกณฑ์ตรวจรับ: modal เปิดมา slot ว่างทั้งคู่ · กดโดยไม่เลือก → block · publish เกิดหลังขั้นสุดท้ายบันทึกผลแล้วเท่านั้น + ทุกขั้นมี at

### FIX-07 · [HIGH] dec csq ประกาศแต่ไม่มี CSQ hook ในไฟล์

| ช่อง | รายละเอียด |
|---|---|
| อาการ | Feature List ประกาศ chip ◆csq แต่ grep `CSQ`/`csq`/`7C` = 0 ทั้งไฟล์ — ไม่มี stamp/comment/toast ใด ๆ |
| หลักฐาน | grep count: CSQ 0 · csq 0 · 7C 0 (เทียบ F102 มี EC stamp 6 จุด) |
| ผลกระทบ | chip มีแต่ hook ไม่มี = spec/HTML แตกกัน — decl_rule.py จะ DIVERGENCE ตอน S1.8 |
| ตำแหน่ง | `doCalib` (จุด publish) + drawer/audit |
| วิธีแก้ | เพิ่ม CSQ hook ตาม pattern F102: audit line + toast "บันทึกผลประเมินเข้า 7C" ตอน publish + comment `<!-- CSQ: perf.result.published → ท่อตาม CSQ_BRIEF -->` — event/ท่อจริงรอเคาะ OQ-PERF-02 |

เกณฑ์ตรวจรับ: publish แล้วมีร่องรอย CSQ ใน audit/toast/comment · ไม่ประกาศท่อ OC/DC (สงวนของ engine)

### FIX-08 · [HIGH] c[3] calibrate ระดับทีม/บริษัท — ไม่มี view

| ช่อง | รายละเอียด |
|---|---|
| อาการ | มีเฉพาะสอบทาน "รายคน" — ไม่มีมุมเทียบคะแนน/เกรดทั้งทีมหรือ distribution ก่อนเคาะ ตามที่ c[3] ระบุ "calibrate เกรดระดับทีม/บริษัท" |
| หลักฐาน | reviewView = ตารางรายคน + modal รายคนเท่านั้น (screenshot tab_review) |
| ผลกระทบ | coverage หลักไม่ครบ — FRD จะเขียน calibration process ไม่ได้ |
| ตำแหน่ง | `reviewView` |
| วิธีแก้ | เพิ่ม section "Calibration ระดับทีม" (mock): ตารางเทียบทุกคนในทีม/รอบ — คะแนน · เกรดเสนอ · ปรับเกรดใน session เดียว (display + mock adjust) — หรือถ้า Strike เคาะว่ารอบนี้ตัด scope ให้ยุบเป็น OQ ปิด |

เกณฑ์ตรวจรับ: มี view เทียบทั้งทีมก่อนเคาะเกรด (หรือมีมติ OQ ตัด scope เป็นลายลักษณ์อักษร)

### FIX-09 · [HIGH] c[5] hook ส่งผลเข้า Succession หาย

| ช่อง | รายละเอียด |
|---|---|
| อาการ | sendMovement/sendTraining มีครบ แต่ Succession = 0 ทั้งไฟล์ ทั้งที่ c[5] ระบุ "ส่งผลเข้า Movement/Succession/Training" และ F134 (Succession) ba-done แล้ว |
| หลักฐาน | grep Succession 0 |
| ผลกระทบ | contract ปลายทาง F134 ไม่มีหลักฐานบนหน้าจอ |
| ตำแหน่ง | `reviewView` hookbox |
| วิธีแก้ | เพิ่มปุ่ม display-only `sendSuccession(id)` แบบเดียวกับ sendMovement (toast ส่งต่อ ไม่แก้ที่นี่) — โชว์เมื่อ decision ผ่าน/top performer |

เกณฑ์ตรวจรับ: ผลที่เผยแพร่มีปุ่มส่งเข้า Succession (display-only) เคียง Movement/Training

### FIX-10 · [MINOR] ปุ่มปิด drawer icon ไม่ render (กล่องเปล่า)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `.icon-btn` ปิด drawer มี `<i data-lucide>` ค้าง ไม่ถูกแปลงเป็น svg → เห็นเป็นกรอบเปล่า |
| หลักฐาน | Screenshot dr_appr มุมขวาบน · evaluate `{hasSvg:false, hasI:true}` หลังเปิด drawer |
| ตำแหน่ง | `render()` ส่วน drawer / `renderIcons` timing |
| วิธีแก้ | เรียก `renderIcons()` หลังเติม drawer innerHTML ทุกครั้ง (หรือท้าย render() รวม) |

เกณฑ์ตรวจรับ: เปิด drawer แล้วปุ่มปิดมี svg เสมอ

### FIX-11 · [MINOR] placeholder slot DOA ถูกตัดคำ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | ช่อง slot แคบจน placeholder "เลือกผู้สอบทานตามตำแหน่ง…" เห็นเป็น "เลือกผู้สอบทานตา" |
| หลักฐาน | Screenshot modal_doacalib slot 1 |
| วิธีแก้ | ขยาย `.slot-pick` หรือย่อ placeholder ("เลือกผู้สอบทาน…") + text-overflow ellipsis |

เกณฑ์ตรวจรับ: placeholder อ่านจบคำหรือ ellipsis สวยงาม ไม่ตัดกลางคำ

## 3. WARN จาก audit (แก้ตามสะดวก · ไม่บล็อก)

- Rule #21 icon ไม่มี w-/h- 1 จุด (comment ใน loader)
- hardcoded font-size ใน base-kit residual

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ (ส่วน FRD) |
|---|---|---|---|
| OQ-PERF-01 | แก้ผลหลังเผยแพร่ — ต้องมี flow re-open (อำนาจสูง + เหตุผล + audit) หรือ published = final จนปิดรอบ | Strike | 03_LOGIC state machine · 05_RULES |
| OQ-PERF-02 | CSQ profile ของ F131 — event ไหนยิงท่อไหน (publish ผลรายคน? ปิดรอบ?) มูลค่า EC คิดยังไง | Strike + Architect | CSQ_BRIEF · §Integration |
| OQ-PERF-03 | scope การเห็นของหัวหน้าสายงาน — ปัจจุบันเห็นทุกแผนก ควรจำกัด DEPT/สายบังคับบัญชาไหม | Strike | SEC_BRIEF scope_type |
| OQ-PERF-04 | ถ้าตัด scope calibration ระดับทีมออกจากรอบนี้ (FIX-08) ให้บันทึกมติ + แผน wave ถัดไป | Strike | Coverage Manifest |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ทุก script block ผ่าน
- [ ] audit.sh FAIL=0
- [ ] Playwright pageerror=0 ทุก route/drawer/modal
- [ ] รันเคส Acceptance ของ FIX-01..05 (CRITICAL) และ FIX-06..09 (HIGH) ซ้ำทั้งชุด — โดยเฉพาะ P1/P2/P3/P4 + slot preset
- [ ] ส่งไฟล์กลับ re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (BA status F131) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → เข้า Phase B (FRD/TC)
