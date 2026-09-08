# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
HR — F102 Welfare (สวัสดิการ) · welfare.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F102 Welfare (สวัสดิการ) · mod HR · arch master · dec: doa + csq |
| ไฟล์ที่ตรวจ | welfare.html (3,152 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-08 · BA gate (html-review-fix-order) |
| ขอบเขต | Re-gate ก่อนเข้า Phase B (FRD/TC) — เทียบ spec F102 ใน Cube_Feature_List + governance + interaction จริง |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK ทุก block · audit **FAIL=0** WARN=4 (kit residuals) · Playwright **pageerror=0** ทุก route/drawer/modal |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 5 · HIGH 2 · MINOR 2 → แก้แล้วส่ง re-gate เต็มรอบ |

## 1. สรุปผลตรวจ (Executive Summary)

โครงหน้าจอทำถูกตามมาตรฐานเกือบทั้งหมด: 4 แท็บ (ทะเบียน/คำขอ/คงเหลือรายคน/รายงาน) ครบตาม archetype master · benefit versioning ทำถูกตาม state machine (แก้ active = ออกเวอร์ชันใหม่ + ปิด effTo เวอร์ชันเดิมวันก่อนวันมีผล + กันช่วงมีผลทับกัน) · eligibility engine ครอบ leaver / กลุ่มไม่มีสิทธิ์ / ช่วงมีผล · DOA ทำตามมติ 2026-08-17 (slot picker เลือก "คน" ตามตำแหน่งที่ resolve จาก DOA กลาง + แสดง avatar+ตำแหน่ง+ชื่อใน timeline) · CSQ hook ประทับมูลค่าเข้า 7C EC ครบทุกจุด (stat/drawer/audit) · masking FN-94 ตาม role ทำงานฝั่ง display · empty submit ถูก block ด้วย field error · double submit สร้าง record เดียว · Esc chain ปิดตามลำดับ modal→drawer ถูกต้อง

ประเด็นที่ต้อง **BLOCK**: mutation ฝั่งอนุมัติ/ยกเลิก **ไม่มี guard เลยแม้แต่ชั้นเดียว** — พิสูจน์ด้วยการรันจริงว่า (1) อนุมัติคำขอที่ถูกปฏิเสธ/ยกเลิกไปแล้วได้ (2) คลิกอนุมัติครั้งเดียวข้ามสายอนุมัติ 2 ขั้นจบทันที (3) อนุมัติเกินเพดานได้ (ใช้ไป 48,000 จากโควตา 30,000 โดยหน้าจอโชว์คงเหลือ 0) (4) persona พนักงานเห็นและกดปุ่มอนุมัติได้ทั้งที่ข้อมูลถูก mask (5) ยกเลิกคำขอที่อนุมัติ+ส่งจ่ายแล้วได้ ทำยอดใช้สิทธิ์หายเงียบ ๆ — ทั้งหมดคือ logic hole ระดับ data integrity ที่ถ้าปล่อยเข้า FRD ทีม Phase B จะเขียน spec ตาม HTML ที่ผิด

### 1.1 ความครบถ้วนเทียบ Spec F102

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| กำหนดชุดสวัสดิการ×กลุ่มพนักงาน + เพดาน | ✅ | registry CRUD + groups multi-select + quota/unit (money/times/percent) + versioning + ช่วงมีผล (screenshot tab_registry) |
| ยอดสิทธิ์คงเหลือรายคน real-time | ✅ | แท็บคงเหลือรายคน: โควตา/ใช้ไป/คงเหลือ/progress ต่อประเภท + ผู้ติดตาม (screenshot balance_emp2) |
| ผูกการเบิกเข้าเพดานอัตโนมัติ | ⚠️ บางส่วน | เช็คตอน submit (validateRequest → "เกินคงเหลือ") แต่**ไม่ re-check ตอนอนุมัติ** + pending ไม่จองสิทธิ์ → overdraft ได้จริง (FIX-02, หลักฐาน B3) |
| สวัสดิการจ่ายประจำเข้ารอบเงินเดือน | ⚠️ บางส่วน | มีแค่ pill สถานะจ่าย (รอจ่าย/ส่งจ่ายแล้ว) + บรรทัด audit "เชื่อม Payroll" — ไม่มี surface จ่ายประจำ (เช่น สมัคร PVD % ต่อคน / รายการที่จะส่งเข้ารอบ) (FIX-07 + OQ-WEL-02) |
| dec: doa | ✅ hook | modal DOA slot picker (GET /doa/resolve · freeze หลังส่ง) + timeline ราย ขั้น — ตรงมติ 2026-08-17 · แต่ chain ถูก collapse ตอนอนุมัติ (FIX-03) |
| dec: csq | ✅ hook | EC stamp: stat "บันทึกเข้า 7C · EC", drawer chip, audit line — ไม่ประกาศท่อ OC/DC ซ้ำ ✓ |
| dep: F065 Payroll (data) / F101 Expense Claim (ctl) | ✅ display-only | pay status เป็น display + note "ระบบ (เชื่อม Payroll)" — ไม่ mock หน้าจอ feature อื่น ✓ |
| PDPA / masking (FN-94 · BR-08) | ⚠️ | masking display ถูกต้องทุกชั้น (ผู้ยื่น/มูลค่า/ผู้ติดตาม) แต่ persona ที่ถูก mask ยังกด mutation ได้ (FIX-04) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] doApprove ไม่มี precondition guard — อนุมัติ record สถานะปลายทางได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | เรียกอนุมัติคำขอที่ rejected/cancelled/draft ได้ สถานะกระโดดกลับเป็น approved |
| หลักฐาน | Bypass B1: `REQ-2569-0025` before `status:'rejected'` → เรียก `doApprove()` → after `{status:'approved', pay:'pending'}` |
| ผลกระทบ | terminal state ไม่ terminal จริง — คำขอที่ถูกปฏิเสธกลับมาตัดสิทธิ์+เข้าคิวจ่ายได้ |
| ตำแหน่ง | `function doApprove(id)` |
| วิธีแก้ | เพิ่ม guard ต้น function: `if(!r || r.status!=='pending') return showToast('อนุมัติได้เฉพาะคำขอสถานะรออนุมัติ','warning')` — pattern เดียวกับ precondition guard ขั้นเงิน (review-dimensions §2) |

เกณฑ์ตรวจรับ: (1) เรียก `doApprove` กับ record สถานะ rejected/cancelled/draft/approved → status ไม่เปลี่ยน + toast เตือน (2) record pending อนุมัติได้ปกติ

### FIX-02 · [CRITICAL] ไม่ re-check เพดาน/eligibility ณ ตอนอนุมัติ — อนุมัติเกินโควตาได้จริง

| ช่อง | รายละเอียด |
|---|---|
| อาการ | สอง pending ที่ต่างผ่านเช็คตอน submit ถูกอนุมัติทั้งคู่ → ยอดใช้เกินโควตา และ `remaining()` ใช้ `Math.max(0,…)` ซ่อนค่าติดลบ |
| หลักฐาน | Bypass B3: quota 30,000 · used ก่อน 12,000 · rem 18,000 → สร้าง pending 2 ใบ ใบละ 18,000 → อนุมัติทั้งคู่สำเร็จ → `usedAfter:48,000 · remainingShown:0` · Bypass B8: archive benefit แล้วยังอนุมัติคำขอค้างของ benefit นั้นได้ |
| ผลกระทบ | เพดานต่อปี (หัวใจของ F102 ตาม c[3]) ถูกทะลุโดยไม่มีสัญญาณเตือน — data + เงินเพี้ยน |
| ตำแหน่ง | `doApprove` · `remaining` · `usedByPerson` |
| วิธีแก้ | ใน `doApprove` (หลังผ่าน FIX-01): เรียก `eligibility()` + คำนวณคงเหลือใหม่ ถ้า want > remaining → block พร้อมเหตุผล "คงเหลือไม่พอ ณ วันอนุมัติ" · `remaining()` เลิก clamp 0 — คืนค่าจริง แล้วให้ชั้น display เป็นคน format (โชว์ 0 พร้อม badge "เต็มโควตา" ได้ แต่ logic ต้องเห็นติดลบ) · หมายเหตุ FRD: pending ควรจองสิทธิ์ (soft-reserve) — ใส่เป็น rule ใน 05_RULES |

เกณฑ์ตรวจรับ: (1) เคส B3 ซ้ำ → ใบที่สองถูก block ยอดใช้ ≤ โควตาเสมอ (2) benefit ที่ archived → อนุมัติคำขอค้างไม่ได้ (3) `remaining()` ไม่ clamp ค่าติดลบใน logic

### FIX-03 · [CRITICAL] DOA chain collapse — คลิกเดียวอนุมัติแทนทุกขั้น

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `doApprove` ทำ `(r.approvals||[]).forEach(a=>a.status='approved')` — ขั้นที่ยังเป็น current/pending ถูกปั๊ม approved หมดในคลิกเดียว |
| หลักฐาน | Bypass B2: `REQ-2569-0023` chain before `[{1:approved},{2:current}]` → `doApprove` ครั้งเดียว → `[{1:approved},{2:approved, at:null}]` — ขั้น 2 อนุมัติโดยไม่มีผู้กระทำ/เวลา |
| ผลกระทบ | สายอนุมัติ 2 ขั้นจาก DOA กลาย เป็นพิธีกรรม — ขัด DOA pattern (F019) และ transition guard (F147) ตรง ๆ |
| ตำแหน่ง | `doApprove` |
| วิธีแก้ | อนุมัติ = advance ทีละขั้น: หา `a=approvals.find(x=>x.status==='current')` → set approved + `at` วันนี้ → ถ้ามีขั้นถัดไป set เป็น current แล้ว **status คงเป็น pending** · เมื่อขั้นสุดท้าย approved ค่อยเปลี่ยน `r.status='approved'` + pay='pending' + EC stamp — reject ก็ทำเฉพาะขั้น current (โค้ดเดิมของ doReject ถูกแล้ว ใช้เป็นแบบ) |

เกณฑ์ตรวจรับ: (1) คำขอ 2 ขั้น กดอนุมัติครั้งแรก → ขั้น 1 approved มี at · ขั้น 2 current · คำขอยัง pending (2) กดครั้งที่สอง → approved จริง + ตัดคงเหลือ + EC stamp ทำครั้งเดียว (3) ทุกขั้นที่ approved มี at และ person

### FIX-04 · [CRITICAL] Permission หลุด — persona พนักงานอนุมัติ/ยกเลิกได้ทั้งปุ่มและ function

| ช่อง | รายละเอียด |
|---|---|
| อาการ | สลับ role เป็น employee: ข้อมูลถูก mask (••••• / RESTRICTED) แต่ปุ่ม อนุมัติ/ไม่อนุมัติ/ยกเลิกคำขอ ยังโชว์และกดได้ · เรียก `doApprove` ตรงก็ผ่าน |
| หลักฐาน | Screenshot persona_employee_req_view (ปุ่มอนุมัติสีแดงมุมขวาบน พร้อมข้อมูล mask) · Bypass B4: `role:'employee'` → `doApprove(REQ-2569-0023)` → `pending→approved` |
| ผลกระทบ | consent/permission gate มีแค่ครึ่งเดียว (display) — ขัดหลัก "กันทั้ง UI และ function" |
| ตำแหน่ง | `drawerRequestView` (บรรทัดสร้าง `acts`) · `doApprove/doReject/doCancelRequest/doArchiveBenefit/submitBenefit` |
| วิธีแก้ | เพิ่ม helper `canApprove()` (= role admin/manager ตามโมเดล persona เดิม FN-94) — (a) UI: render ปุ่มอนุมัติ/ไม่อนุมัติเฉพาะ canApprove · ปุ่มยกเลิกเฉพาะเจ้าของคำขอ/admin (b) function: guard ต้นทุก mutation `if(!canApprove()) return showToast('สิทธิ์ไม่พอ','warning')` — mirror ของ sec.can() ฝั่งจริง |

เกณฑ์ตรวจรับ: (1) role employee: ปุ่มอนุมัติ/ไม่อนุมัติไม่ render (2) เรียก `doApprove/doReject/doCancelRequest` ตรงใน role employee → state ไม่เปลี่ยน (3) role admin/manager ทำงานปกติ

### FIX-05 · [CRITICAL] ยกเลิกคำขอที่อนุมัติ/จ่ายแล้วได้ — ยอดใช้สิทธิ์หายเงียบ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `doCancelRequest` set cancelled โดยไม่ดูสถานะ — คำขอ approved + pay:'sent' ถูกยกเลิกได้ ยอดใช้สิทธิ์ที่นับจาก approved หายทันที ขณะที่ microcopy ยืนยันว่า "ยกเลิก…ก่อนอนุมัติ — ไม่กระทบคงเหลือ" |
| หลักฐาน | Bypass B5: `REQ-2569-0012` before `{status:'approved', pay:'sent', used:12,000}` → `doCancelRequest` → after `{status:'cancelled', used:0}` |
| ผลกระทบ | ยอดที่จ่ายเงินจริงไปแล้วหายจากบัญชีสิทธิ์ — คงเหลือพองกลับโดยไม่มีเอกสารกลับรายการ/audit (ขัด append-only) |
| ตำแหน่ง | `doCancelRequest` (+ ปุ่ม cancel render ถูกแล้ว เฉพาะ draft/pending — รูอยู่ที่ function) |
| วิธีแก้ | guard: `if(!r || !['draft','pending'].includes(r.status)) return showToast('ยกเลิกได้เฉพาะร่าง/รออนุมัติ','warning')` — การเรียกคืนสิทธิ์หลังอนุมัติเป็นคนละ flow (ดู OQ-WEL-01) |

เกณฑ์ตรวจรับ: (1) เคส B5 ซ้ำ → status คงเดิม used ไม่เปลี่ยน + toast (2) draft/pending ยกเลิกได้ปกติ + audit line ถูกต้อง

### FIX-06 · [HIGH] Archive benefit ที่ยังมีคำขอ pending อ้างอยู่ — เงียบ ไม่เตือน

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `doArchiveBenefit` เก็บถาวรทันทีแม้มี pending อ้าง benefit นั้น — คำขอค้างกลายเป็นอ้าง benefit ที่ไม่มีผล |
| หลักฐาน | Bypass B8: B-CHECKUP `active→archived` สำเร็จขณะ REQ-2569-0023 (pending) ยังอ้างอยู่ ไม่มี warning |
| ผลกระทบ | คำขอค้างค้างเติ่ง/ถูกอนุมัติบนสิทธิ์ที่ปิดแล้ว (ประกอบ FIX-02) |
| ตำแหน่ง | `doArchiveBenefit` + `modalConfirm` archive |
| วิธีแก้ | ก่อน archive นับ pending ที่อ้าง benefitId — ถ้ามี แสดงใน confirm modal ("มีคำขอรออนุมัติ N ใบ — ต้องจัดการก่อน/จะถูกระงับ") · ขั้นต่ำ: เตือน + require ยืนยัน · guard role ตาม FIX-04 |

เกณฑ์ตรวจรับ: archive benefit ที่มี pending → confirm ระบุจำนวนคำขอค้าง · archive ที่ไม่มีค้าง → เดิม

### FIX-07 · [HIGH] c[4] จ่ายประจำเข้ารอบเงินเดือน — ไม่มี surface

| ช่อง | รายละเอียด |
|---|---|
| อาการ | สวัสดิการชนิด percent (กองทุนสำรองเลี้ยงชีพ) โชว์ "สมัคร %" แต่ไม่มีที่สมัคร/กำหนด % ต่อคน และไม่มีรายการ "จ่ายประจำที่จะส่งเข้ารอบเงินเดือน" — pay hook มีเฉพาะคำขอรายครั้ง |
| หลักฐาน | grep: 'sent' ปรากฏเฉพาะ mock · แถว PVD ในคงเหลือรายคน = ขีด — ทั้งแถว (screenshot balance_emp2) |
| ผลกระทบ | capability ข้อ 4 ของ F102 และ contract F102→F065 (data: สวัสดิการที่จ่ายผ่านเงินเดือน) ไม่มีหลักฐานบนหน้าจอ → FRD จะเขียน integration ไม่ได้ |
| ตำแหน่ง | แท็บคงเหลือรายคน / drawer benefit-view |
| วิธีแก้ | เพิ่ม display-only hook ขั้นต่ำ: (a) section "จ่ายประจำผ่านเงินเดือน" ต่อคน — สมัคร/แก้ % PVD (mock) + สถานะส่งเข้ารอบ (b) note ชี้ว่า runtime จริงอยู่ฝั่ง F065 อ่านจาก F102 — ห้าม mock หน้าจอ Payroll · ถ้า Strike เคาะตัด scope รอบนี้ → ยุบ FIX นี้เป็น OQ-WEL-02 ปิดพร้อมบันทึกใน 0_DIRECTION |

เกณฑ์ตรวจรับ: มี surface สมัคร/แสดงรายการจ่ายประจำต่อคน + ระบุชัดว่าเป็น hook ไป F065 (หรือมีมติ OQ-WEL-02 ตัด scope เป็นลายลักษณ์อักษร)

### FIX-08 · [MINOR] Combobox คน ไม่ตรง anatomy #102 (ไม่มี avatar/icon ใน option)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | list ของ combobox พนักงานผู้ยื่น และ DOA slot picker แสดง ชื่อ→ตำแหน่ง·แผนก ถูก แต่ไม่มี avatar/`user` icon นำหน้า ตามที่ #102 ล็อก (คน = avatar → ชื่อ → ตำแหน่ง·แผนก) |
| หลักฐาน | Screenshot combo_open · modal_doa_combo |
| ผลกระทบ | ไม่ consistent กับ combobox คนใน lane เดียวกัน (golden features) |
| ตำแหน่ง | `ssRenderList` / config `initSearchSelect` ของ reqEmp, balEmp, doaSlot* |
| วิธีแก้ | เติม avatar initials (แบบเดียวกับ `.pav` ที่ใช้ใน doa-picked) หน้า option ทุกตัวของ combobox ประเภทคน — overlay portal เดิมดีอยู่แล้ว ห้ามแตะ |

เกณฑ์ตรวจรับ: ทุก combobox คนมี avatar+ชื่อ+ตำแหน่ง·แผนก ครบ 3 ส่วน ลำดับตาม #102

### FIX-09 · [MINOR] joinDate mock เป็น พ.ศ. ใน ISO field → แสดง "เข้างาน 1 พ.ค. 3107"

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `EMPLOYEES.joinDate:'2564-05-01'` (พ.ศ.) แต่ `fmtDate` บวก 543 อีกรอบ → หน้าคงเหลือรายคนแสดงปี 3107 |
| หลักฐาน | Screenshot balance_emp2 บรรทัดหัวการ์ดพนักงาน |
| ผลกระทบ | mock ไม่น่าเชื่อถือ + เสี่ยงทีม Phase B ลอก convention ผิด |
| ตำแหน่ง | `EMPLOYEES[]` joinDate ทุกคน |
| วิธีแก้ | แก้ mock เป็น ค.ศ. (2021-05-01 ฯลฯ) ให้ convention เดียวกับ field วันที่อื่นทั้งไฟล์ |

เกณฑ์ตรวจรับ: ทุกวันที่บนจอเป็น พ.ศ. ช่วง 25xx ไม่มี 31xx

## 3. WARN จาก audit (แก้ตามสะดวก · ไม่บล็อก)

- Rule #21 icon ไม่มี w-/h- 5 จุด — ส่วนใหญ่ CSS-sized (ss-caret/empty-icon/lead-icon) ตามที่ไฟล์ note ไว้เอง
- Rule #40 `.uc-email` CSS ตกค้างจาก kit (ไม่ถูกใช้) — ลบได้
- hardcoded font-size ใน base-kit residual
- Rule #103/#40 cell pill "ใช้สิทธิ์ได้/ไม่ใช้สิทธิ์" — ternary pill เดียวต่อเซลล์ (false-positive)

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ (ส่วน FRD) |
|---|---|---|---|
| OQ-WEL-01 | เรียกคืนสิทธิ์หลังอนุมัติ/จ่ายแล้ว ต้องมี flow reversal ไหม (เอกสารกลับรายการ + คืนคงเหลือ + EC reverse stamp) หรือ approved = final ตลอดปีสิทธิ์ | Strike | 03_LOGIC state machine §5 · 05_RULES |
| OQ-WEL-02 | scope "จ่ายประจำเข้ารอบเงินเดือน" (PVD % ฯลฯ) — ทำ surface ฝั่ง F102 รอบนี้ หรือยกไป F065 ทั้งก้อน (ผูกกับ FIX-07) | Strike + พี่เบิร์ด | §Integration F065 · Coverage Manifest |
| OQ-WEL-03 | pending ควร soft-reserve สิทธิ์ไหม (จองคงเหลือตั้งแต่ยื่น) หรือเช็คซ้ำเฉพาะตอนอนุมัติ (FIX-02 ทำแบบหลังเป็นขั้นต่ำ) | Strike | 05_RULES กติกาคงเหลือ |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ทุก script block ผ่าน
- [ ] audit.sh FAIL=0 (WARN kit residuals คงได้)
- [ ] Playwright pageerror=0 ทุก route/drawer/modal
- [ ] รันเคส Acceptance ของ FIX-01..05 (CRITICAL) และ FIX-06..07 (HIGH) ซ้ำทั้งชุด — โดยเฉพาะ B1/B2/B3/B4/B5/B8
- [ ] ส่งไฟล์กลับ re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (BA status F102) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → เข้า Phase B (FRD/TC)
