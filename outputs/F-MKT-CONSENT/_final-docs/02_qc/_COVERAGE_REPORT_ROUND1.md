# _COVERAGE_REPORT — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> **Step 4 · qc-coverage · รอบ 1 (HTML vs Contract)** — re-run 2026-09-11 หลังเปลี่ยนโมเดลเนื้อหาเป็น **เอกสารอัปโหลด** + เพิ่ม **มุมมองผู้รับ (recipient read+sign view)**
> Artifact: `outputs/F-MKT-CONSENT/consent-pdpa.html` (3086 บรรทัด)
> Contract: `FUNCTION_CHECKLIST_F-MKT-CONSENT.md` (FN-01…20 · FN-40.1…10) + `PREBRIEF_F-MKT-CONSENT.md` (S-01…20 · BR-01…22 · Part C · Part D)
> Declaration: plan `dec=["csq"]`
> ทุก ✓ อ้าง route + selector/function จริง — ไม่มี "น่าจะมี"

## VERDICT: **PASS** ✅

- ครอบ **FN-01…20 = 20/20** มี hook เดินได้จริง
- **FN-40 negatives 10/10 ไม่โผล่บน surface** (ยืนยันระดับ grep + โครง render; การ assert เรนเดอร์จริงเป็นงาน step 5 e2e)
- ไม่มี block rule/scenario ใดไม่ถูกครอบ · ไม่พบ scope creep
- **มุมมองผู้รับ = in-scope** (mock ของลิงก์ภายนอก S-10/S-11) — ไม่ใช่ Part C violation (รายละเอียดด้านล่าง)
- มี **2 divergence ที่ประกาศไว้** (content model = PM/BA-directed · DOA detect = false positive) — ไม่ใช่ failure
- **DECL-CSQ**: hook declare-only ต่อสายแล้วใน HTML · `CSQ_BRIEF` ออกที่ step 7 → ไม่ fail รอบ 1 (ตามกติกา)

---

## FN × Evidence Matrix (รอบ 1 = HTML) — FRD/TC = NOT-CHECKED (รอบ 2)

| FN | HTML | Evidence (route · function · selector) |
|---|:--:|---|
| FN-01 สร้างวัตถุประสงค์ + **อัปโหลด v1** | ✓ | `#/consent/purposes` → `openPurCreate`(2810)/`purCreateDrawer`(2811) · upload zone `uploadBlockHTML('pfDocInput'…)`(2841) + `handleDocUpload(this,'purForm')`(2851) · `submitPurCreate`(2828) บังคับ name+≥1 channel+life 1–120+**doc required** → push `versions:[{v:1,docName,docType,body}]`(2837) |
| FN-02 **อัปโหลดเวอร์ชันใหม่** + เตือน N | ✓ | `openNewVersion`(2993)/`newVersionModal`(2997) upload block `nvDocInput` · `doPublishVersion`(3003) บังคับ doc → push `{v:nv…}` + `currentVer=nv` + `staleCount` → toast "N รายการต้องขอความยินยอมใหม่"(3009) · warn banner affected(2999) |
| FN-03 ตารางวัตถุประสงค์ + สถิติ | ✓ | `purposesBody`(2517) col ความครอบคลุม% · `purposeStats`(2510) granted/withdrawn/expired/coverage · statCards ใน `purViewDrawer`(2869) |
| FN-04 ปิดวัตถุประสงค์ | ✓ | `doClosePurpose`(3016) `status='closed'` · request เลือกได้เฉพาะ `status==='active'`(2621,2638) → ปิดแล้วขอใหม่ไม่ได้ · `closePurposeModal`(3011) ระบุ consent เดิมคงอยู่ (BR-14/17) |
| FN-05 สร้างคำขอ single-screen | ✓ | `openReqCreate`(2618)/`reqCreateDrawer`(2620) = sec blocks ไม่มี stepper (comment "single-screen (no wizard, Part C #10)" 2617) · `submitReqCreate`(2656)→`createRequestRecord`(2666) gen `link`+QR |
| FN-06 ส่งอีเมล → รอตอบ | ✓ | `sendVia`(2713) push `{ch,at}` · draft→`pending` · toast "จำลอง — ไม่ส่งจริง" · ปุ่ม "ส่งทาง…(จำลอง)"(2701) |
| FN-07 ส่งซ้ำช่องทางอื่น = ครั้งที่ N | ✓ | `resendOther`(2715)→`sendVia` ด้วย channel ที่เลือก · append send ไม่สร้างคำขอใหม่ (BR-18) · combo `resendCh`(2699) |
| FN-08 คัดลอกลิงก์ / ดาวน์โหลด QR | ✓ | `copyLink`(3072) + `downloadQR`(3066) → blob SVG + บันทึก send `export-qr` · ปุ่ม 2689/2691 |
| FN-09 **ดาวน์โหลดเอกสาร** | ✓ | `downloadPdfForm`(3069) แสดงชื่อเอกสารเวอร์ชันปัจจุบันของทุกวัตถุประสงค์ (`curDoc`) · ปุ่ม "ดาวน์โหลดเอกสาร"(2692) · *mock toast* (สอดคล้อง FN-40.3) |
| FN-10 เซ็นผ่านมุมมองผู้รับ | ✓ | `openRecipientView`(2758)→`recipientViewHTML`(2779) อ่านเอกสาร+ยืนยันตัวตน · `submitRecipient`(2771) บังคับ verified+เลือกครบ →`applyAnswers`(2723) สร้าง registry row `granted` + `evidence` 5 ฟิลด์ + history + `supersede` |
| FN-11 ยินยอมบางวัตถุประสงค์ (แยกข้อ) | ✓ | `setRecipientChoice(code,grant/decline)`(2768) รายข้อ(2796-97) · `submitRecipient` snapshot choices →`applyAnswers` สร้าง consent แยก granted/declined ต่อ code + `emitConsequence` แยก event(2736/2741) |
| FN-12 ดูหลักฐาน 1 รายการ | ✓ | `consentViewDrawer` evHTML 5×`evItem`(2909-2914): เวลา·ช่องทาง·วิธียืนยันตัวตน·เวอร์ชัน·IP/อุปกรณ์ (BR-15) |
| FN-13 ทะเบียนทั้งหมด + กรองทุกมิติ | ✓ | `registryBody`(2424) + `filteredConsents`(2400) filter search/status/channel/purpose · table subject×purpose×channel+status+expiry(2449) |
| FN-14 Customer 360 | ✓ | `openC360`(2937)/`c360Drawer`(2938) group by purpose ทุกรายการของคน · ปุ่ม "ดูรายคน"(2472) |
| FN-15 ถอนแทนลูกค้า | ✓ | `withdrawModal`(2978) บังคับ reason+via · `doWithdraw`(2984) `status='withdrawn'` ทันที + history reason/via + `emitConsequence(reversal_of)` (BR-09/10) — modal ระบุ "ไม่ต้องผ่านการอนุมัติ" |
| FN-16 ใกล้หมดอายุ ≤30 วัน (เตือน ไม่บล็อก) | ✓ | stat "ใกล้หมดอายุ (≤30 วัน)"(2435) + filter `near`(2440) · `nearExpiry`(2207) 0–30 วัน · near-tag "อีก N วัน" · ต่ออายุจาก consent view (ไม่บล็อก) |
| FN-17 ต่ออายุ = คำขอใหม่อ้างเดิม | ✓ | `openRenew`(2933)→`openReqCreate({refOld})` · `createRequestRecord` set `refOld` · refBanner "ไม่แก้วันหมดอายุของเดิม (BR-13)"(2627) · `reConsent`(2893) batch |
| FN-18 ประวัติ append-only + เหตุผล | ✓ | `consentViewDrawer` hist timeline(2922) `c.history` reverse · เขียนเพิ่มใน `applyAnswers`/`doWithdraw`/`supersede` เท่านั้น (BR-16) |
| FN-19 simulator /consent/resolve | ✓ | `resolveBody`(2537)/`runResolve`(2549)/`resolveConsent`(2554) → ฟิลด์ล็อก + reason + `jsonColor` sample · HTTP 200 chip (BR-19/20) |
| FN-20 never_asked (ไม่ใช่ 404/declined) | ✓ | `resolveConsent` สาขา `!list.length`(2558) → `allowed:false · status:'never_asked' · found:false` + reason (BR-04/08/19) |

**FN ครอบ 20/20** · ทุก S-01…S-20 มีทางเดินจนจบผลทางธุรกิจ (map 1:1 ตาม trace ในตาราง) · `scenarios_without_fn = []` · `fn_without_trace = []`

---

## FN-40 Negatives (ต้องไม่มี) — 10/10 ABSENT

| # | ห้ามมี | ผล | Evidence |
|---|---|:--:|---|
| 40.1 | cookie consent | ✓ ไม่มี | grep `cookie` = 0 hit |
| 40.2 | สายอนุมัติก่อนส่งคำขอ | ✓ ไม่มี | ไม่มี status/ปุ่มอนุมัติในสายส่ง · comment "no approval chain"(2756) · withdraw ระบุ "ไม่ต้องผ่านการอนุมัติ"(2979) |
| 40.3 | ส่งอีเมล/LINE จริง | ✓ ไม่มี | `sendVia` toast "จำลอง — ไม่ส่งจริง"(2714) — mock เท่านั้น |
| 40.4 | คำนวณมูลค่า / คอลัมน์ผลรายท่อ | ✓ ไม่มี | `emitConsequence` "invisible sink · ไม่ตีมูลค่า ไม่ประทับผลรายท่อ"(2321) |
| 40.5 | การ์ดผล 7 ท่อ CSQ | ✓ ไม่มี | grep pipe-card/csq-card render = 0 · "renders NOTHING · no pipe cards"(2310) |
| 40.6 | ประกาศท่อ OC/DC/SC | ✓ ไม่มี | HTML มีแต่ envelope event เดี่ยว(2313) · OC/DC/SC เป็นงาน CSQ_BRIEF step 7 ไม่อยู่ใน HTML |
| 40.7 | ธง opt-out เดียวต่อคน (Odoo) | ✓ ไม่มี | โมเดล triple subject×purpose×channel (`supersede` 2748, BR-01) — ไม่มี flag เดี่ยว |
| 40.8 | "ไม่ตอบ" = "ไม่ยินยอม" | ✓ ไม่มี | `pending`/`expired` แยกจาก `declined` (`effStatus` 2205) · resolve pending reason "การไม่ตอบไม่ใช่การยินยอม"(2571) |
| 40.9 | บล็อกการส่งด้วยตัวเอง | ✓ ไม่มี | resolve = read-only simulator (`runResolve` แค่แสดงผล 2549) ไม่มี action บล็อก |
| 40.10 | wizard Pattern Q 5 ขั้น | ✓ ไม่มี | create request/purpose = single-screen drawer · CSS `.stepper/.d-stepper`(845-1272) เป็น BASE-KIT dormant (DO NOT EDIT) — grep `class="stepper` ในสตริงที่ render = 0 |

> ⚠️ FN-40 ระดับนี้ยืนยันด้วย grep + โครง render string · **การ assert ว่าไม่โผล่ตอนเรนเดอร์จริง = หน้าที่ e2e step 5** (C3.5) — coverage ยืนยันได้แค่ว่า generator ไม่ได้ปล่อยของต้องห้ามลงโค้ด

---

## Declaration Coverage (Phase 0b)

| ท่อ | เข้าเงื่อนไข? | ต้องมี | ผลรอบ 1 |
|---|---|---|---|
| **CSQ** | ✅ (plan `dec=["csq"]` · กระทบข้อมูลอ่อนไหว/ตัดสินใจปลายทาง) | `CSQ_BRIEF` (step 7) + HTML hook declare-only | **N/A-yet (ไม่ fail)** — HTML ต่อ hook `emitConsequence` declare-only แล้ว(2312) · `CSQ_BRIEF` ออก step 7 ตามแผน · surface สะอาด (ไม่ประกาศ OC/DC/SC, ไม่มี pipe card, ไม่ตีมูลค่า) |
| DOA | ❌ ไม่เลือก | — | **DIVERGENCE (false positive)** — `prebrief_checklist.py` ตรวจเจอ `doa:true` เพราะ keyword "อนุมัติ" ไปโดนประโยค **ปฏิเสธ** "ไม่ต้องผ่านการอนุมัติ" (BR-09) · feature ห้าม approval ชัดเจน (Part C#2 · FN-40.2) → **ไม่ต้องมี DOA_BRIEF · ไม่ BLOCK** |
| NTF | ❌ ไม่เลือก | — | N/A — การส่ง (S-06/07) เป็น mock toast ล้วน ไม่มี event "ใครต้องรู้" จริง |
| DOCCFG | ❌ ไม่เลือก | — | N/A — ไม่ใช่เอกสารธุรกรรมที่มีเลขรัน (REQ/CNS = internal id ไม่ hardcode รูปแบบเลขทางการ) |

---

## Declared Divergences (ไม่ใช่ failure — บันทึกเพื่อ Strike/BA)

**DECLARED-01 · โมเดลเนื้อหา = เอกสารอัปโหลด (versioned)** — PM/BA-directed 2026-09-11
- HTML ใช้ file-upload (`type="file"` 2849 · `handleDocUpload` 2851 · `versions[].docName/docType/body`) แทนการพิมพ์ข้อความ
- ขัดกับ `PREBRIEF` **BR-05/06** ที่เขียน "แก้ข้อความ = ออกเวอร์ชันใหม่" (S-01 "แนบข้อความนโยบาย" · S-02 "แก้ข้อความ" · S-09 "PDF ที่มีข้อความฝัง")
- **GOVERNANCE OPEN**: BA ต้องอัปเดต `PREBRIEF` BR-05/06 + S-01/02/09 + FN-01/02/09/10/11 ให้ตรง (FUNCTION_CHECKLIST header ระบุไว้แล้ว) — จนกว่าจะ sync ให้ถือเป็น divergence ที่ประกาศ ไม่นับตก

**DECLARED-02 · DOA keyword false positive** — ดูตาราง Declaration (ตรวจตาม detect แล้วสรุปว่าเป็นสัญญาณหลอก C3.9 · ไม่ไล่แก้)

---

## Part C / Scope Creep Check

| ตรวจ | ผล |
|---|---|
| **มุมมองผู้รับ (recipient read+sign view)** | ✅ **in-scope · ไม่ใช่ Part C violation** — เป็น **mock ของลิงก์ภายนอก** ที่เจ้าของข้อมูลเห็นเมื่อกดลิงก์ (S-10/S-11) · simbar ระบุชัด "จำลอง — ไม่ใช่การส่งจริง"(2782) · surface แยก (ไม่มี ERP sidebar) · `submitRecipient`→`applyAnswers` engine เดิม · **ไม่ใช่** email/LINE จริง (40.3) · **ไม่ใช่** approval chain (40.2, comment 2756) · **ไม่ใช่** การ์ด 7 ท่อ CSQ (40.5) |
| ของเกิน contract อื่น | ไม่พบ — persona strip / `decorativeNav`(3037) = เดโมนอกขอบเขต ระบุ toast ชัด · `exportCsv`(2477 = E4) เป็น utility เสริม ไม่ขัด contract |
| Scope guard (Part C 10 ข้อ) | ผ่านครบ — ดู FN-40 matrix |

---

## Gap List

**ไม่มี gap ระดับ BLOCK/WARN ในรอบ 1** — ทุก FN + S + FN-40 + DECL-CSQ ครอบครบ

รายการติดตาม (ไม่บล็อกรอบ 1):
1. **[GOV] DECLARED-01** — BA sync `PREBRIEF` BR-05/06 + S-01/02/09 + FN ให้เป็นโมเดลเอกสารอัปโหลด (owner: BA)
2. **[step 7] CSQ_BRIEF** — ออก `CSQ_BRIEF_F-MKT-CONSENT.md` (declare-only event → 7C Engine · ห้ามประกาศ OC/DC/SC ซ้ำ)
3. **[รอบ 2] NOT-CHECKED** — Golden rules ใน FRD 05_RULES · FN↔TC ledger · N/A-UI carry (BR-21 caller cache · BR-22 4-step enforcement = OQ) · lock refs — ตรวจที่ step 10

---

## Diff กับผลตรวจก่อนหน้า (หลังเปลี่ยน content model)

- **ปิดแล้ว/เปลี่ยนกลไก**: FN-01/02 textarea → file-upload (upload + version push wired ✓) · FN-09 "ดาวน์โหลดฟอร์ม PDF" → "ดาวน์โหลดเอกสาร" (curDoc) · FN-10/11 ปุ่มจำลอง → **มุมมองผู้รับเต็ม** (`openRecipientView`→`submitRecipient`→`applyAnswers` เขียน registry + 5-evidence + per-purpose split) ✓
- **เกิดใหม่**: recipient view surface (ตรวจแล้ว in-scope) · DECLARED-01 governance divergence
- **ยังค้าง**: CSQ_BRIEF (step 7) · BA PREBRIEF sync

---
*qc-coverage-checker · รอบ 1 (HTML) · 2026-09-11 · ทุก ✓ อ้าง evidence · ไม่แก้ HTML · ไม่ commit*
