# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
**CUBE 4.0 · HR Module — F127 สรรหา (Recruit / Candidate Pool) · `สรรหา.html`**

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F127 สรรหา (W9 · master) |
| ไฟล์ที่ตรวจ | `สรรหา.html` (Phase A · หลัง vibe) |
| วันที่ตรวจ | 2 ก.ย. 2569 · ผู้ตรวจ: BA (AI-assisted review) |
| ขอบเขต | Spec F127 + UX walkthrough ทุก flow |
| เครื่องมือ | audit.sh v9 · node --check · Playwright |
| ผล Quality Gate | node OK · audit **FAIL=0** (WARN=4) · **pageerror=0** |
| **Verdict** | **ผ่านเชิงเทคนิค · ติด 2 บั๊ก logic + 1 ประเด็น PDPA — แก้ก่อน re-gate เข้า FRD** |

---

## 1. สรุปผลตรวจ (Executive Summary)

ตัว prototype เดินครบทุก flow หลักของ F127 และผ่าน quality gate เชิงเทคนิคทั้งหมด (syntax / iron rules FAIL=0 / ไม่มี pageerror ทั้ง 4 แท็บ) โครง UX แข็งแรง: consent gate PDPA ทำงานจริง, DOA แสดง avatar + ตำแหน่ง + ชื่อคน ตรง decision 2026-08-17, band freeze snapshot คู่ข้อเสนอ, บอร์ดบังคับสร้างข้อเสนอก่อนเข้าขั้น "ข้อเสนอ"

อย่างไรก็ตาม พบช่องโหว่ logic 2 จุดที่ทำให้ข้อมูลไม่สอดคล้องกัน (FIX-01, FIX-02) และ microcopy PDPA 1 จุดที่ขัดกับ spec โดยตรง (FIX-03) — ทั้ง 3 จุดต้องแก้ในรอบ vibe นี้ก่อนส่งเข้า Phase B (FRD/TC) เพราะ dev จะ implement ตาม prototype

### 1.1 ความครบถ้วนเทียบ Spec F127

| Capability ตามแผน | ผล | หมายเหตุ |
|---|---|---|
| เปิด requisition อ้างอัตราว่าง + อนุมัติ | ✅ ผ่าน | ผูก manpower_ref · DOA-REQ-OPEN · state ครบ draft→ปิด |
| Pipeline ผู้สมัคร (screen/interview/offer/hire) | ✅ ผ่าน | 5 stage + terminal (ไม่ผ่าน/ถอนตัว/Talent Pool) + บอร์ด Kanban |
| นัดสัมภาษณ์ + บันทึกผลผู้สัมภาษณ์ | ✅ ผ่าน | modal นัด + person picker + scorecard + NTF สองฝ่าย |
| ออก offer + อนุมัติเงื่อนไข | ✅ ผ่าน | state ครบ · DOA-OFFER แยก entry · เช็คเงินเดือนในช่วง band |
| แปลง hire → Employee + เปิด onboard | ⚠️ บางส่วน | soft-linkage ยิง event เท่านั้น (OQ-15 · จงใจค้าง — ดูข้อ 4) |
| PDPA (เก็บตามระยะที่ประกาศ) | ❌ ไม่ผ่าน | microcopy ระบุ "เก็บแบบไม่มีวันหมดอายุ" — FIX-03 |

---

## 2. รายการสั่งแก้ (Fix Order)

> เรียงตามความรุนแรง · แก้เสร็จให้รัน re-gate ตามข้อ 5 ทุกครั้ง

### FIX-01 · [CRITICAL] บอร์ด "ถัดไป" ข้ามขั้น ข้อเสนอ → รับเข้าทำงาน โดยไม่ผ่านการตอบรับ offer

| | |
|---|---|
| **อาการ** | ผู้สมัครที่ offer ยังสถานะ "ส่งข้อเสนอแล้ว" (sent) กดปุ่มถัดไปบนบอร์ด → stage เปลี่ยนเป็น hired ทันที |
| **หลักฐาน** | ทดสอบจริง: อารยา (offer=sent) → hired ได้ · filled ค้าง 0/2 · req ไม่ปิด · ไม่ยิง event onboarding · onboardSent=false |
| **ผลกระทบ** | มี 2 เส้นทางไป hired ที่พฤติกรรมต่างกัน — เส้นบอร์ดข้าม business rule ทั้งหมด (ตอบรับ offer, นับอัตรา, ปิด req, ส่ง onboard) ถ้า dev ทำตามจะได้ข้อมูลเพี้ยนใน production |
| **ตำแหน่ง** | `candMoveStage()` — guard มีเฉพาะขั้น offer (ต้องมี offer ก่อน) แต่ไม่มี guard ขั้น hired |
| **วิธีแก้** | เพิ่ม guard: ถ้า `STAGES[ni].id==='hired'` และ `offer.status!=='accepted'` → toast "ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน" + เปิด drawer แท็บข้อเสนอ (pattern เดียวกับ guard ขั้น offer) · ถ้า accepted แล้ว → เรียก `candHireHandoff()` แทนการ set stage ตรง ๆ ให้เป็นเส้นทางเดียวกันทั้งระบบ |

**เกณฑ์ตรวจรับ:**
- กดถัดไปจากขั้นข้อเสนอขณะ offer ยังไม่ accepted → ถูกบล็อกพร้อมคำอธิบาย และพาไปแท็บข้อเสนอ
- เมื่อ offer=accepted กดถัดไป → ผ่าน flow เดียวกับปุ่มรับเข้าทำงาน: filled+1, req ปิดอัตโนมัติเมื่อครบ, ยิง event onboarding, audit log ครบ
- ไม่มีเส้นทางใดตั้ง stage=hired โดยไม่ผ่าน `candHireHandoff()`

### FIX-02 · [CRITICAL] Persona "ผู้ชมทั่วไป" (read-only) ยังสร้าง/แก้ข้อมูลได้

| | |
|---|---|
| **อาการ** | สลับเป็นผู้ชมทั่วไป → ปุ่ม "เพิ่มผู้สมัคร" และ "เปิดอัตราใหม่" ยังแสดง กดเปิดฟอร์มและยืนยันสร้างได้จริง |
| **หลักฐาน** | ทดสอบจริง: viewer เปิด drawer ผู้สมัครใหม่ได้ · `submitCand()`/`submitReq()` ไม่เช็ค persona (guard viewer มี 8 จุดเฉพาะ action ใน drawer/บอร์ด) |
| **ผลกระทบ** | ขัด label "สิทธิ์อ่านอย่างเดียว" — demo ให้ลูกค้าดูแล้วสิทธิ์ไม่จริง และ dev จะเข้าใจ permission model ผิด |
| **ตำแหน่ง** | ปุ่ม primary บน page header ทั้ง 2 แท็บ (req/pool) + `submitCand()` + `submitReq()` + `candSetConsent()` + entry `openCandCreate()`/`reqFormDrawer` |
| **วิธีแก้** | (1) ซ่อนปุ่ม เพิ่มผู้สมัคร/เปิดอัตราใหม่ เมื่อ `persona==='viewer'` (2) เพิ่ม guard ต้นทุก mutation function: `if(RC.persona==='viewer'){showToast('สิทธิ์อ่านอย่างเดียว','warning');return;}` กันเส้นทางอ้อม |

**เกณฑ์ตรวจรับ:**
- persona ผู้ชมทั่วไป: ไม่เห็นปุ่มสร้าง/แก้/บันทึกความยินยอม/เลื่อนสถานะ ทุกแท็บ
- เรียก mutation ทางอ้อม (เช่น console) → ถูกบล็อกด้วย toast ไม่มี state เปลี่ยน
- recruiter/manager ใช้งานได้ครบเท่าเดิม (manager เท่านั้นที่อนุมัติได้ ตาม canApprove)

### FIX-03 · [HIGH · PDPA] Microcopy "เก็บข้อมูลแบบไม่มีวันหมดอายุตามนโยบาย" — ขัด spec F127

| | |
|---|---|
| **อาการ** | banner ใน drawer ผู้สมัคร และ banner ฟอร์มเพิ่มผู้สมัคร ระบุการเก็บข้อมูลแบบไม่มีวันหมดอายุ |
| **หลักฐาน** | spec F127 กำหนด "ข้อมูลผู้สมัครอยู่ใต้ PDPA — เก็บตามระยะที่ประกาศ" · การเก็บไม่มีกำหนดขัดหลัก storage limitation ของ PDPA |
| **ผลกระทบ** | ถ้าข้อความนี้หลุดเข้า FRD/production copy = ความเสี่ยงเชิงกฎหมายและภาพลักษณ์ |
| **ตำแหน่ง** | `candDetail()` consentBanner + banner หัวฟอร์ม `candFormDrawer` (2 จุด) |
| **วิธีแก้** | เปลี่ยนเป็น "เก็บข้อมูลตามระยะเวลาที่ประกาศในนโยบายความเป็นส่วนตัว (ตั้งค่าที่ Policy Center)" · เพิ่ม field แสดงวันครบกำหนดเก็บ (retention_until) แบบ display-only + comment ว่าระยะเก็บอ่านจาก Policy Center config — ไม่ hardcode |

**เกณฑ์ตรวจรับ:**
- ไม่เหลือข้อความ "ไม่มีวันหมดอายุ" ในไฟล์ (grep = 0)
- drawer ผู้สมัครแสดงระยะเก็บ/วันครบกำหนดแบบ display-only พร้อม comment แหล่งที่มา config
- บันทึกประเด็น retention เข้า BRD §PDPA และ OQ list (ดูข้อ 4)

### FIX-04 · [MINOR] ปุ่มย้อนกลับบนการ์ดบอร์ดเห็นเป็นกล่องว่าง
- **อาการ:** ปุ่ม arrow-left (btn-secondary ขนาดเล็ก) บนการ์ด Kanban มองเห็นเป็นกล่องขาวเปล่า เหมือนปุ่มพัง
- **วิธีแก้:** เพิ่ม contrast ไอคอน หรือใส่ border ให้ชัด · disabled state ต้องต่างจาก enabled ชัดเจน
- **เกณฑ์ตรวจรับ:** ปุ่มย้อนกลับมองเห็นไอคอนชัดทั้ง enabled/disabled ที่ zoom 100%

### FIX-05 · [MINOR] Validation ใช้ toast อย่างเดียว — ทับปุ่มยืนยัน ไม่ชี้ field และค้างข้าม context
- **อาการ:** submit ฟอร์มว่าง → toast "กรุณากรอกข้อมูลให้ครบถ้วน" ลอยทับปุ่มยืนยันสร้างพอดี ไม่ไฮไลต์ field ที่ขาด และ toast ค้างแสดงเมื่อเปิด drawer อื่นต่อ
- **วิธีแก้:** ใช้ `validateField()/clearFieldError()` ที่มีอยู่แล้วทำ field-level error (ขอบแดง + ข้อความใต้ field + focus ตัวแรกที่ผิด) · ย้าย toast ไม่ให้ทับ footer หรือลด duration
- **เกณฑ์ตรวจรับ:** submit ฟอร์มว่าง → field ที่ขาดถูกไฮไลต์และ focus · toast ไม่บังปุ่ม action

### FIX-06 · [MINOR] `setCandTab` รับค่า tab ที่ไม่รู้จักแล้ว fallback เงียบไปแท็บประวัติ
- **อาการ:** เรียกด้วย id นอกชุด detail/assess/offer/history → เนื้อหาแสดงเป็นประวัติ โดย tab header ไม่ active ตัวไหน
- **วิธีแก้:** validate id ใน `setCandTab`: ไม่อยู่ในชุด → default `'detail'` (pattern เดียวกับ RC.tab ของ route หลักที่ทำถูกแล้ว)
- **เกณฑ์ตรวจรับ:** ค่า tab แปลกปลอม → แสดงแท็บรายละเอียดพร้อม header active ถูกตัว

### FIX-07 · [MINOR] ไม่มี loading state ตอน submit (Iron Rule #44)
- **อาการ:** ปุ่มยืนยันสร้าง/ส่งอนุมัติ ไม่มี spinner (loader-2) — `RC.busy` มีในโค้ดแล้วแต่ไม่สะท้อนบน UI
- **วิธีแก้:** ตอน `RC.busy=true` → ปุ่มแสดงไอคอน loader-2 หมุน + disabled จนจบ (mock delay สั้น ๆ ได้) เพื่อให้ dev copy pattern ถูก
- **เกณฑ์ตรวจรับ:** audit.sh ไม่เหลือ WARN Rule #44

---

## 3. WARN จาก audit (แก้ตามสะดวก · ไม่บล็อก)

- Rule #21 — ไอคอนบางจุดไม่มี class w-/h- (ss-caret, empty-icon ฯลฯ) — ส่วนใหญ่คุมด้วย CSS อยู่แล้ว ตรวจซ้ำเฉพาะจุดที่ขนาดเพี้ยน
- Rule #40 — เซลล์ตารางมี sub-line (.uc-email รหัสใต้ชื่อ) — pattern นี้ทีมใช้ทั่วระบบ ถ้าจะคงไว้ให้บันทึกเป็น accepted deviation
- Token — font-size hardcode บางจุดใน sidebar (ควรใช้ --fs-*) — เก็บตอน sync BASE-KIT รอบถัดไป

---

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-15 | Inbound handoff: hire → สร้าง Employee + เปิด On/Offboard จริง — ตอนนี้เป็น soft-linkage ยิง event อย่างเดียว (จงใจ · comment ไว้ในโค้ดแล้ว) ต้องออกแบบฝั่งรับ | Strike | FRD §Integration |
| OQ-16 (ใหม่) | PDPA retention ผู้สมัคร: ระยะเก็บกี่เดือน/ปี · ครบกำหนดแล้ว ลบหรือ anonymize · Talent Pool ต่ออายุ consent อย่างไร — เสนอเป็น config ที่ Policy Center (ห้าม hardcode ตามหลัก HR-1) | Strike / พี่เบิร์ด | FRD §PDPA + Policy Center |
| หมายเหตุ | Manpower hook (F124) เป็น display-only ไม่บังคับ — ตรงกับสถานะ F124 ที่ยังไม่เข้า dev · คง note ในฟอร์มไว้ถูกแล้ว | — | — |

---

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] `node --check` ทุก script block ผ่าน
- [ ] `audit.sh` → FAIL=0 และ WARN Rule #44 หายไป
- [ ] Playwright: pageerror=0 ทั้ง 4 แท็บ + รัน 3 เคสตาม Acceptance ของ FIX-01/02 ซ้ำ
- [ ] `grep "ไม่มีวันหมดอายุ"` = 0 (FIX-03)
- [ ] ผ่านแล้ว → อัพเดต `FEATURE_REGISTRY.md` (F127 · vibe แก้รอบ 2) + แจ้งพี่เบิร์ดอัพ Google Sheet + ส่งเข้า Phase B (FRD/TC)

---
*เอกสารนี้สร้างจากการตรวจไฟล์จริง (audit v9 + Playwright walkthrough ทุก flow) · 2 ก.ย. 2569*
