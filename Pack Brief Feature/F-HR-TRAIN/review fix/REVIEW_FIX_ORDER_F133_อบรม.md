# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
**CUBE 4.0 · HR Module — F133 อบรม (Training & Development) · `อบรม.html`**

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F133 อบรม (W8 · master · เคส EC ไม่มี AC) |
| ไฟล์ที่ตรวจ | `อบรม.html` (หลัง vibe) |
| วันที่ตรวจ | 2 ก.ย. 2569 · ผู้ตรวจ: BA (skill: html-review-fix-order) |
| เครื่องมือ | audit.sh v9 · node --check · Playwright (walkthrough + bypass catalog) |
| ผล Quality Gate | node OK · audit **FAIL=0** (WARN=3 base-kit inherited) · **pageerror=0** ทั้ง 4 แท็บ |
| **Verdict** | **BLOCK** — CRITICAL 1 (บันทึกผลก่อนจบอบรม) + HIGH 4 · แก้แล้วส่ง re-gate เต็มรอบก่อนเข้า FRD |

---

## 1. สรุปผลตรวจ (Executive Summary)

งานคุณภาพดีขึ้นชัดเจนจากรอบ F127 — บทเรียนถูกนำมาใช้ครบ: `viewerRO()` guard ทุก mutation, tab id แปลกปลอม fallback ปลอดภัย, validation ระดับ field (`markInvalidFields`), ไม่ติด WARN #44, และมี section **"ขอบเขตที่ไม่รองรับ — ตัดสินแล้ว"** ประกาศ 5 ข้อชัดเจน (Expense hook-only, gap อ่านจาก Performance, ไม่ทำ eLearning, ใบรับรอง soft ref, หมวดอ่านจาก HR Config) · Guard ธุรกิจหลายจุดถูกต้อง: กันลงทะเบียนซ้ำ/เกิน capacity, ใบรับรองออกได้เฉพาะผู้ผ่าน, terminal state กันย้อน, DOA เฉพาะหลักสูตรมีค่าใช้จ่าย, Rate Card (F060) เป็น display-only พร้อม note ตรงมาตรฐาน dependency

แต่พบ 1 ช่องโหว่ CRITICAL ที่กดถึงได้จาก UI ปกติ (บันทึกผลผ่าน/ไม่ผ่านได้ทั้งที่รอบยัง "เปิดรับสมัคร" — การอบรมยังไม่เกิด) และ capability ตาม spec หายไป 2 ข้อโดย**ไม่ได้ประกาศตัด scope** (เช็คชื่อ+ประเมินหลังอบรม, ประวัติอบรมรายคน+ชั่วโมงสะสม) รวมถึง function-layer guard ที่หลุด 3 จุด — ต้องแก้ก่อนเข้า FRD

### 1.1 ความครบถ้วนเทียบ Spec F133

| Capability ตามแผน | ผล | หมายเหตุ |
|---|---|---|
| แผนหลักสูตร + รอบอบรม + ที่นั่ง | ✅ ผ่าน | Course Catalog + Session + capacity bar + กันลงเกิน/ซ้ำ |
| เสนอ/อนุมัติผู้เข้าอบรม | ✅ ผ่าน | enroll จาก gap (F131 hook) หรือเลือกเอง · DOA เมื่อมีค่าใช้จ่าย · approve/reject + เหตุผล |
| เช็คชื่อ + ประเมินหลังอบรม | ❌ ไม่ผ่าน | ไม่มีเช็คชื่อ (attendance) และไม่มีแบบประเมินหลังอบรม — มีแค่บันทึกผลผ่าน/ไม่ผ่าน · **ไม่อยู่ใน oos** → FIX-03 |
| ประวัติอบรมรายคน + ชั่วโมงสะสม | ❌ ไม่ผ่าน | ไม่มี view รายคน/ชั่วโมงสะสมเลย · **ไม่อยู่ใน oos** → FIX-04 |
| ต้นทุนต่อหัว/หลักสูตรมุม EC | ⚠️ บางส่วน | EC ref card display-only รอ Rate Card (ถูกต้อง) แต่มุม "ต้นทุนต่อหัว" จากงบที่มีอยู่ยังไม่มี → FIX-05 |
| Governance: DOA · CSQ(EC) · dependency F131/F060 | ✅ ผ่าน | DOA avatar+ตำแหน่ง+ชื่อคน ตาม lock · EC ไม่ post บัญชี (OB-1) · hooks display-only + note ตรง |

---

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] บันทึกผล (ผ่าน/ไม่ผ่าน) ได้ทั้งที่รอบอบรมยัง "เปิดรับสมัคร" — การอบรมยังไม่เกิดขึ้น

| | |
|---|---|
| **อาการ** | ผู้เรียนสถานะ "ยืนยันลงทะเบียน" มีปุ่ม **บันทึกผล** โผล่ทั้งในแท็บ ผล/ใบรับรอง และแท็บผู้เรียนใน drawer ตั้งแต่รอบยังสถานะ `open` — กดบันทึก "ผ่าน" ได้ทันที |
| **หลักฐาน** | Playwright: enroll (confirmed) ในรอบ SES-2569-001 (status=`open`, อบรม 15 ต.ค.) → `submitResult('pass')` สำเร็จ → status=`passed` · รายงาน completion rate นับผลนี้ทันที |
| **ผลกระทบ** | ผลอบรม/ใบรับรอง/completion rate เกิดก่อนการอบรมจริง — ข้อมูลรายงานเชื่อไม่ได้ และ dev จะ implement ตาม |
| **ตำแหน่ง** | `openResultModal()` (guard แค่ `e.status==='confirmed'`) + จุด render ปุ่มบันทึกผลใน result tab และ learner tab |
| **วิธีแก้** | เพิ่มเงื่อนไข: บันทึกผลได้เฉพาะเมื่อรอบ `status==='closed'` (ปิดรอบ = จบการอบรม ตาม microcopy เดิม) — `openResultModal` toast แจ้ง "บันทึกผลได้หลังปิดรอบอบรม" ถ้ายังไม่ปิด · ปุ่มบันทึกผลใน UI แสดงเป็น disabled + tooltip เหตุผลขณะรอบยังไม่ปิด |

**เกณฑ์ตรวจรับ:**
- รอบ `open`: ปุ่มบันทึกผล disabled พร้อมเหตุผล และเรียก `submitResult` ตรงก็ถูกบล็อก (status ไม่เปลี่ยน)
- ปิดรอบแล้ว: บันทึกผลได้ตามเดิม flow ครบ (audit + NTF)
- completion rate นับเฉพาะผลจากรอบที่ปิดแล้ว

### FIX-02 · [HIGH] Mutation guard อยู่แค่ชั้น UI — function หลุด 3 จุด

| | |
|---|---|
| **อาการ/หลักฐาน** | (a) `enrollApprove/enrollReject` ไม่เช็ค `canApprove` — persona เจ้าหน้าที่ (canApprove=false) เรียกตรง อนุมัติครบ 2 ขั้น → `confirmed` ได้จริง (b) `sendExpense` ไม่เช็คสถานะ/กันซ้ำ — ส่งได้ตอน `pending_doa` (ยังไม่ผ่านอนุมัติ) และส่งซ้ำได้ (c) `submitSession` ไม่เช็คสถานะหลักสูตร — สร้างรอบให้หลักสูตร `closed` ได้ ขัด microcopy ตัวเอง ("ปิดหลักสูตร — ไม่เปิดรอบใหม่ได้") |
| **หมายเหตุ** | UI ทำถูกแล้วทุกจุด (ปุ่มซ่อน/กรองตามเงื่อนไข) — ปัญหาคือชั้น function ไม่ guard ซ้ำ ตาม pattern บั๊ก "gate กันแค่ชั้น UI" |
| **ตำแหน่ง** | `enrollApprove()` · `enrollReject()` · `sendExpense()` · `submitSession()` |
| **วิธีแก้** | เพิ่ม guard ต้น function: (a) `if(!PERSONAS[TC.persona].canApprove){showToast('เฉพาะผู้อนุมัติ','warning');return;}` (b) `if(e.status!=='confirmed'&&e.status!=='passed'||e.expenseSent)return+toast` (c) `if(courseOf/getCourse(draft.courseId).status!=='published')return+toast` |

**เกณฑ์ตรวจรับ:** เรียกทั้ง 4 function ตรงด้วยเงื่อนไขผิด → ถูกบล็อกด้วย toast, state ไม่เปลี่ยน · เส้นทาง UI ปกติทำงานเหมือนเดิม

### FIX-03 · [HIGH] Capability "เช็คชื่อ + ประเมินหลังอบรม" หายทั้งก้อน และไม่ได้ประกาศตัด scope

| | |
|---|---|
| **อาการ** | ไม่มีเช็คชื่อเข้าอบรม (attendance) และไม่มีแบบประเมินหลังอบรมใด ๆ (grep เช็คชื่อ/attendance/ประเมินหลังอบรม = 0) — มีเพียงบันทึกผลผ่าน/ไม่ผ่าน · section oos ที่ประกาศตัด scope ไว้ 5 ข้อ **ไม่มีข้อนี้** |
| **ผลกระทบ** | spec `c[]` ระบุเป็น capability หลัก — ถ้าเข้า FRD โดยไม่มี dev จะไม่ build และไม่มีมติรองรับ |
| **วิธีแก้** | เพิ่มใน learner tab (หลังปิดรอบ): (1) เช็คชื่อรายคน — toggle เข้า/ขาด ต่อผู้เรียน + คนขาดบันทึกผลไม่ได้ (2) ประเมินหลังอบรม — modal ให้คะแนน 1-5 + comment ต่อผู้เรียนหรือระดับรอบ (mock ระดับ FN พอ) · **ทางเลือก:** ถ้าทีมยืนยันตัด scope → ต้องเพิ่มเข้า oos + เปิด OQ ให้ Strike เคาะ (ห้ามหายเงียบ) |

**เกณฑ์ตรวจรับ:** flow เช็คชื่อ→บันทึกผล ต่อเนื่องถูกลำดับ (ขาด=บันทึกผลไม่ได้) + ผลประเมินหลังอบรมเก็บและแสดงได้ — หรือ oos + OQ ครบถ้าตัด

### FIX-04 · [HIGH] Capability "ประวัติอบรมรายคน + ชั่วโมงสะสม" หายทั้งก้อน และไม่ได้ประกาศตัด scope

| | |
|---|---|
| **อาการ** | ไม่มี view ประวัติการอบรมต่อพนักงาน และไม่มีชั่วโมงสะสมที่ไหนเลย (grep = 0) · ไม่อยู่ใน oos |
| **วิธีแก้** | เพิ่มจุดเข้าถึง: คลิกชื่อผู้เรียน (result tab / learner tab) → drawer/section "ประวัติอบรมของ [ชื่อ]" — รายการทุก enrollment (หลักสูตร รอบ ผล ใบรับรอง) + ชั่วโมงสะสมรวม (คำนวณจาก duration ชม. ของหลักสูตรที่สถานะผ่าน) — mock จาก DB.enrolls ที่มีอยู่ ไม่ต้องเพิ่ม data ใหม่ |

**เกณฑ์ตรวจรับ:** เปิดประวัติจากชื่อคนได้ · ชั่วโมงสะสม = ผลรวม ชม. เฉพาะรายการผ่าน · คนไม่มีประวัติเห็น empty state

### FIX-05 · [HIGH] มุม "ต้นทุนต่อหัว/หลักสูตร" ยังไม่มี (ทำได้เลยโดยไม่ต้องรอ Rate Card)

| | |
|---|---|
| **อาการ** | EC ref card อ้าง Rate Card display-only ถูกต้องแล้ว แต่ spec ต้องการ "ต้นทุนต่อหัว/หลักสูตรมุม EC" ซึ่งคำนวณจากงบ (budget) ที่มีในระบบได้ — ปัจจุบันไม่มีที่ไหนแสดง |
| **วิธีแก้** | เพิ่มการ์ดในแท็บรายงาน: ต่อหลักสูตรมีค่าใช้จ่าย แสดง งบ · ผู้ผ่าน · **ต้นทุนต่อหัว = งบ/ผู้ผ่าน** + note "อัตรากลางจริงจะอ่านจาก Rate Card เมื่อพร้อม (ไม่ hardcode)" — สอดคล้อง EC ไม่ post บัญชี |

**เกณฑ์ตรวจรับ:** การ์ดต้นทุนต่อหัวแสดงถูกต่อหลักสูตร · หลักสูตรฟรี/ยังไม่มีผู้ผ่านแสดง "—" ไม่หารศูนย์

### FIX-06 · [MINOR] Icon ใน modal ไม่แสดง (กล่องว่าง)

- **อาการ:** modal ลงทะเบียนผู้เรียน — icon header และ avatar ในการ์ดแนะนำจาก gap เป็นกล่องชมพูว่าง · ปุ่ม icon เล็กข้าง "บันทึกผล" ใน learner tab เป็นกล่องขาวว่าง (ขณะที่ avatar ในตาราง/drawer อื่นแสดงปกติ)
- **วิธีแก้:** ให้ `renderIcons()` ครอบ modal container ทุกครั้งหลัง `tcOpenModal()` render + ตรวจ initials/contrast ของ avatar ใน modal · ปุ่ม icon เล็กเพิ่ม contrast ทุก state
- **เกณฑ์ตรวจรับ:** ไม่มีกล่อง icon/avatar ว่างในทุก modal + ปุ่ม icon มองเห็นชัดที่ zoom 100%

### FIX-07 · [MINOR] Combobox เลือกผู้เรียนใน modal — list โดนขอบ modal ตัด + option ไม่มี avatar

- **อาการ:** เปิด dropdown ค้นหาพนักงานใน modal ลงทะเบียน → list โผล่ได้รายการเดียวแล้วถูกขอบ/footer ของ modal บัง (clip) · รายการมีชื่อ+ตำแหน่งแต่ไม่มี avatar
- **วิธีแก้:** overlay ของ combobox ใน modal ต้อง portal/ยกระดับ z ไม่โดน clip ตามหลัก Overlay Portal (#95) · option เพิ่ม avatar initials ให้ครบ anatomy combobox คน (#102) ให้เหมือนการ์ด gap ด้านบน
- **เกณฑ์ตรวจรับ:** list แสดงอย่างน้อย 4-5 รายการเต็มไม่โดนตัด scroll ได้ · ทุก option มี avatar+ชื่อ+ตำแหน่ง

---

## 3. WARN จาก audit (ไม่บล็อก)

WARN=3 เป็น base-kit inherited ทั้งหมด (#21 icon-class มี CSS sizing · #40 sub-line user-cell meta · token font-size sidebar) — ไฟล์ประกาศไว้ใน GATE note ของตัวเองแล้ว ตรงกับ accepted deviation ของทีม · เก็บตอน sync BASE-KIT

---

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-17 (ใหม่ · เฉพาะกรณีทีมเลือกตัด scope FIX-03/04) | ยืนยันตัด "เช็คชื่อ+ประเมินหลังอบรม" และ/หรือ "ประวัติ+ชั่วโมงสะสม" ออกจาก F133 รอบนี้หรือไม่ — ถ้าตัด ต้องเข้า oos อย่างเป็นทางการ | Strike | Scope F133 + FRD §Coverage |
| หมายเหตุ | Rate Card (F060) ยังไม่ dev — EC ref เป็น display-only ถูกต้องแล้ว ไม่ต้องเคาะเพิ่ม · ใบรับรอง soft ref [ASSUMED] มีมติแล้วใน oos | — | — |

---

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] `node --check` ทุก script block ผ่าน
- [ ] `audit.sh` → FAIL=0
- [ ] Playwright: pageerror=0 ทั้ง 4 แท็บ + เคส Acceptance ของ FIX-01/02 ผ่านครบ (บันทึกผลก่อนปิดรอบถูกบล็อก · 4 function guard ทำงาน)
- [ ] Coverage: FIX-03/04/05 มีของจริง หรือ oos+OQ-17 ครบ
- [ ] ผ่านแล้ว → อัพเดต `FEATURE_REGISTRY.md` (F133 · vibe รอบ 2) + แจ้งพี่เบิร์ดอัพ Google Sheet → เข้า Phase B (FRD/TC)

---
*ตรวจด้วย skill html-review-fix-order — audit v9 + Playwright walkthrough + bypass catalog (B1-B8) · 2 ก.ย. 2569*
