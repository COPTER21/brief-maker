# PROPOSALS / OQ ส่งออก — ความยินยอม PDPA (F-MKT-CONSENT · F058)

> ปิดงาน WF-01 ครบ 12 step วันที่ 2026-09-13 · feature **ความยินยอม PDPA** · standalone (dep="") · module การตลาด · wave W1 · declaration = **csq เท่านั้น** (declare-only)
> ไฟล์นี้รวม **ข้อเสนอถึงเจ้าของฟีเจอร์อื่น / design system** + **OQ ที่ BA ต้องเคาะ** — ยังไม่ commit (รอผู้ใช้สั่ง)

---

## A. 🔴 OQ ที่บล็อกก่อนเปิดใช้จริง (dev ห้ามเดา — BA/เจ้าของระบบต้องเคาะ)

| # | เรื่อง | ทำไมบล็อก | อ้างอิง |
|---|---|---|---|
| OQ-03 | **วิธียืนยันตัวตนจริงในมุมมองผู้รับ** — ตอนนี้เป็น checkbox จำลอง ("ยืนยันว่าเป็นเจ้าของข้อมูล") ต้องแทนด้วยของจริง (OTP / ลิงก์เฉพาะบุคคล / อื่น ๆ) | หลักฐานการยินยอมต้องพิสูจน์ตัวตนได้จริงตามกฎหมาย — เดาผิดมีคนเอาไปตั้งค่าจริง + หลักฐานใช้ไม่ได้ | FRD OQ-03 · recipient view · Part D [ASSUMED] |
| OQ-04 | **ขึ้นทะเบียน `/consent/*` กับด่านบังคับใช้สิทธิ์ (Backend Enforcement Gate / F143)** + รีวิว 4 ขั้น | ทุก endpoint ที่ตอบ allowed/deny ต้องผ่านด่านนี้ก่อน go-live — เป็น dependency ข้ามฟีเจอร์ | FRD OQ-04 · BR-22 |

## B. 🟠 OQ / งานประสาน (ไม่บล็อก gate นี้ แต่ต้องเคลียร์ก่อนส่ง dev / ก่อน launch)

| # | เรื่อง | รายละเอียด | อ้างอิง |
|---|---|---|---|
| OQ-01 | **Governance: sync PREBRIEF กับโมเดลเนื้อหาที่ทำจริง** | เนื้อหา PDPA เปลี่ยนจาก "พิมพ์ข้อความ" → **"อัปโหลดเอกสาร (versioned ต่อวัตถุประสงค์)"** ตามที่ PM/BA สั่ง (DECLARED-01) → BA ต้องแก้ **PREBRIEF BR-05/06 + S-01/02/09 + FN-01/02/09/10/11** ให้ตรง (FUNCTION_CHECKLIST อัปเดตแล้ว มีหมายเหตุ) | DECLARED-01 · LD-01 |
| OQ-02 | **BR-21 caller cache** ≤5 นาที + ล้างทันทีเมื่อถอน | เป็นสัญญาฝั่งผู้เรียก (`/consent/resolve`) — document ใน FRD API แล้ว ไม่ทำ UI | BR-21 |
| OQ-05 | **บังคับสิทธิ์ตามบทบาทจริง** | prototype ใช้ demo persona switch (เจ้าหน้าที่/DPO/ผู้ตรวจสอบ) แทน login จริง — ต้อง map เป็น role จริงตอน dev | FRD OQ-05 |
| OQ-06 | เก็บ baseline ตัวชี้วัด §2.3 ก่อน launch | เพื่อวัดผลหลังใช้งานจริง | BRD §2.3 |
| OQ-07 | **[AI-DEFAULT] validate ไฟล์อัปโหลด** (ขนาด/ชนิด) | ตอนนี้ mock — ยังไม่กำหนดเพดานขนาด/ชนิดไฟล์จริง | FRD Phase 2.5 |
| OQ-08 | **[AI-DEFAULT] timezone ของ `expires_at`** | ต้องยืนยัน tz ที่ใช้คำนวณหมดอายุ | FRD Phase 2.5 |
| OQ-CSQ-01 | **เลขโปรไฟล์ 7C จริง `CSQ-NN`** | ตอนนี้ใช้ placeholder `CSQ-F058` — เลขจริงออกโดย 7C Profile Registry | CSQ_BRIEF |
| OQ-CSQ-02 | **ยืนยันท่อ `SecC`** ถูกต้องไหม | ประกาศ SecC แบบ `[DEFAULT — รอยืนยัน]` เพราะ master contract `references/csq-contract.md` **ไม่มีในเครื่องนี้** (skill ติดตั้งแบบ flat) → ตรวจ enum กับ catalog จริงไม่ได้ | CSQ_BRIEF · skill flat |
| OQ-CSQ-03 | consent ควรนับเป็น **DC** (data-subject terminal decision) เพิ่มไหม | ที่นี่ไม่ประกาศตาม lock (declare-only, no OC/DC/SC) — BA เคาะว่าต้องเพิ่มปลายทางไหม | CSQ_BRIEF · LOCK-CSQ-02 |

## C. 📤 ข้อเสนอถึงเจ้าของฟีเจอร์อื่น / design system

| ถึง | เรื่อง |
|---|---|
| เจ้าของ **Backend Enforcement Gate (F143)** | รับ `/consent/*` ขึ้นทะเบียน + รีวิว 4 ขั้น (= OQ-04) · สัญญา `/consent/resolve` = HTTP 200 เสมอ · never-asked → `allowed:false, status:"never_asked"` (ไม่ใช่ 404 / ไม่ใช่ "ไม่ยินยอม") |
| เจ้าของ **DSAR (F157)** | Consent PDPA เป็น dependency ของ DSAR — feed ประวัติ consent + Customer-360 (E1) ให้ · ทะเบียน consent เป็นแหล่งหลักฐาน |
| เจ้าของ **design system / uikit** | **MG-01** (ลงทะเบียน PENDING แล้ว): generalize DSP-02 combobox check ให้รับ combobox ที่ไม่ใช่ `ss-*` (feature นี้ใช้ `.combo`/`cx_*` เอง) |
| เจ้าของ **skill pack** | ⚠️ 2026-09-11 PM/BA สั่ง replace `html-generator-v9` + `qc-ux-html-checker` จาก `update/` = **snapshot เก่ากว่า** (61 iron rules vs 64) → หาย #104/#105/#40.1 + DSP skeleton hardening + qc v3 geometry gate · run นี้ **บังคับ #104 + pre-wire DSP-01..04 ด้วยมือทั้งหมด** · backup ที่ `.claude/_skills_backup_2026-09-11/` · ราย detail [[skill-replace-2026-09-11]] |

## D. 📝 รายการ reconcile ภายใน (ไม่บล็อก · ให้ QA/BA เก็บ)

- **Microcopy drift FRD↔หน้าจอ** (HTML เป็นตัวจริง · TC anchor ถูกแล้ว): resolve toast "…ก่อนตรวจสิทธิ์" (จอ) vs "…ก่อนตรวจสอบ" (FRD) · ปุ่ม Customer-360 บนจอ = "ดูรายคน" (FRD เรียก Customer 360) · ข้อความช่องทางไม่รองรับ → sync FRD 05_RULES §5.4 / 06 §6.10 / 01_UI
- **TC-count stale**: `testcases-consent-pdpa.md` สรุปเขียน "68 เคส" แต่มีจริง **72** `### TC-` (coverage ไม่ลด เพราะมากกว่า) → reconcile เลขสรุป
- **PREFLIGHT stamp** ใน HTML ยังเป็น template ว่าง (audit ไม่ gate)

## E. 🔧 ส่วนขยายที่ทำเพิ่ม (นอกหัวเชื้อ) + ที่เลื่อน

- ✅ **E1 Customer-360** ("ดูรายคน") — เสริม S-14 · feed DSAR
- ✅ **E2 re-consent** หลังออกเวอร์ชันใหม่ — ปิด dead-end S-02
- ✅ **E4 QR download + CSV**
- ⏸ **E3 consent-receipt PDF** — เลื่อน (scope ใหม่ · ทำได้ที่ step 2 thai-doc หรือ wave DSAR)

## F. Declaration รอบนี้
- **csq** ✅ → `CSQ_BRIEF_F-MKT-CONSENT.md` (7 events · declare-only · ไม่ประกาศ OC/DC/SC · idempotency_key + reversal_of)
- doa / doccfg / ntf = **ไม่เลือก**

## G. หมายเหตุแผนกลาง (Cube_Feature_List)
- แถว Consent PDPA (F058) ถูก PM mark `st="done" · "FULL automation"` **ล่วงหน้า** — **ไม่มี auto-pack แยก** · ชุดเอกสารจริง = งาน WF-01 ชุดนี้ที่ `outputs/F-MKT-CONSENT/` (source of truth)
- ไม่ต้องแตะ dep ของ feature อื่น (feature นี้ standalone)
