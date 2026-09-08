# คำสั่งแก้ไข welfare.html (F102 Welfare — สวัสดิการ)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: welfare.html · มาตรฐาน html-generator-v9 (CI Warm Light · vanilla JS · single-file · BASE-KIT v6.4)
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**: benefit versioning (validateBenefit/submitBenefit — BR-03 overlap check), eligibility engine, DOA modal slot picker + confirmDoa, masking FN-94 (canSeeValue/canSeePerson/canSeeDependent), CSQ EC stamps, doReject (advance เฉพาะขั้น current — ถูกแล้ว), Esc chain, overlay portal, empty states, validateRequest ฝั่ง submit

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 doApprove precondition guard — CRITICAL
ตำแหน่ง: `function doApprove(id)`
สิ่งที่ผิด: อนุมัติ record สถานะใดก็ได้ (พิสูจน์: rejected → approved)
แก้เป็น: guard ต้น function — ถ้า `!r || r.status!=='pending'` ให้ toast warning "อนุมัติได้เฉพาะคำขอสถานะรออนุมัติ" แล้ว return ไม่แตะ state
ตรวจรับ: เรียกกับ rejected/cancelled/draft/approved → status ไม่เปลี่ยน · pending อนุมัติได้ปกติ

### 2. FIX-03 DOA advance ทีละขั้น — CRITICAL
ตำแหน่ง: `doApprove` (ทำต่อจากข้อ 1 ใน function เดียวกัน)
สิ่งที่ผิด: `forEach(a=>a.status='approved')` — คลิกเดียวจบทุกขั้น ขั้น 2 ได้ approved ทั้งที่ at:null
แก้เป็น: หา approval ขั้น `status==='current'` → set `status:'approved'` + `at:` วันที่วันนี้ (ISO) · ถ้ายังมีขั้นถัดไป → ขั้นถัดไปเป็น `current` และ `r.status` คงเป็น `pending` (toast "อนุมัติขั้น N แล้ว · ส่งต่อขั้นถัดไป") · ถ้าเป็นขั้นสุดท้าย → `r.status='approved'; r.pay='pending'` + toast EC เดิม — EC stamp/ตัดคงเหลือเกิดครั้งเดียวตอนขั้นสุดท้ายเท่านั้น
ตรวจรับ: คำขอ 2 ขั้น: คลิกแรก → ขั้น1 approved มี at, ขั้น2 current, คำขอยัง pending · คลิกสอง → approved จริง · ทุกขั้น approved มี at

### 3. FIX-02 re-check เพดาน/eligibility ตอนอนุมัติ — CRITICAL
ตำแหน่ง: `doApprove` (ก่อนเปลี่ยน status เป็น approved ขั้นสุดท้าย) + `function remaining`
สิ่งที่ผิด: อนุมัติเกินโควตาได้ (used 48,000 / quota 30,000) · อนุมัติคำขอของ benefit ที่ archived ได้ · `remaining()` clamp `Math.max(0,…)` ซ่อนติดลบ
แก้เป็น: ก่อน finalize ขั้นสุดท้าย เรียก `eligibility(emp,ben,r.useDate)` — ไม่ผ่าน → block พร้อมเหตุผล · คำนวณ `remaining` สด ถ้า `want > remaining` → block "คงเหลือไม่พอ ณ วันอนุมัติ" · `remaining()` เอา `Math.max(0,…)` ออก (คืนค่าจริง) แล้วให้จุด display เดิม format เป็น 0/badge เองโดยไม่เปลี่ยนหน้าตา
ตรวจรับ: pending 2 ใบรวมเกินโควตา → ใบสองถูก block · benefit archived → อนุมัติไม่ได้ · logic เห็นค่าติดลบได้ display ไม่พัง

### 4. FIX-04 persona guard ทั้ง UI และ function — CRITICAL
ตำแหน่ง: `drawerRequestView` (ส่วนสร้าง `acts`) · `doApprove/doReject/doCancelRequest/doArchiveBenefit/submitBenefit`
สิ่งที่ผิด: role employee เห็น+กดปุ่มอนุมัติได้ และเรียก function ตรงผ่าน (pending→approved)
แก้เป็น: เพิ่ม `function canApprove(){ return state.role==='admin'||state.role==='manager'; }` (โมเดลเดียวกับ FN-94) — (a) render ปุ่มอนุมัติ/ไม่อนุมัติเฉพาะ `canApprove()` · ปุ่มยกเลิกเฉพาะ admin หรือเจ้าของคำขอ (b) guard ต้นทุก mutation ข้างต้น: ไม่ผ่าน → toast "สิทธิ์ไม่พอ" return
ตรวจรับ: role employee ไม่เห็นปุ่ม + เรียก function ตรงแล้ว state ไม่เปลี่ยน · admin/manager ปกติ

### 5. FIX-05 doCancelRequest guard สถานะ — CRITICAL
ตำแหน่ง: `function doCancelRequest(id)`
สิ่งที่ผิด: ยกเลิกคำขอ approved+pay:'sent' ได้ ยอดใช้สิทธิ์หาย 12,000→0 เงียบ ๆ ขัด microcopy "ก่อนอนุมัติ — ไม่กระทบคงเหลือ"
แก้เป็น: guard `if(!r || !['draft','pending'].includes(r.status))` → toast "ยกเลิกได้เฉพาะร่าง/รออนุมัติ" return — ห้ามเพิ่ม flow reversal เอง (แขวน OQ-WEL-01)
ตรวจรับ: approved/rejected/revoked ยกเลิกไม่ได้ · draft/pending ยกเลิกได้เดิม

### 6. FIX-06 archive benefit เตือนคำขอค้าง — HIGH
ตำแหน่ง: `doArchiveBenefit` + confirm modal ของ archive
สิ่งที่ผิด: archive ทั้งที่มี pending อ้างอยู่ โดยไม่เตือน
แก้เป็น: นับ `REQUESTS.filter(r=>r.benefitId===id && ['draft','pending'].includes(r.status)).length` — ถ้า >0 แสดงใน confirm modal "มีคำขอรอดำเนินการ N ใบที่อ้างสวัสดิการนี้" ก่อนยืนยัน + guard role ตามข้อ 4
ตรวจรับ: archive ที่มีค้าง → confirm ระบุจำนวน · ไม่มีค้าง → เดิม

### 7. FIX-07 surface จ่ายประจำเข้ารอบเงินเดือน — HIGH
ตำแหน่ง: แท็บคงเหลือรายคน (`renderBalance`)
สิ่งที่ผิด: PVD unit percent มีแค่แถวขีด — ไม่มีที่สมัคร/กำหนด % และไม่มีรายการจ่ายประจำที่ส่งเข้ารอบเงินเดือน (c[4] ของ F102)
แก้เป็น: เพิ่ม section "จ่ายประจำผ่านเงินเดือน" ใต้ตารางสิทธิ์: รายการ benefit unit percent ของกลุ่มพนักงานคนนั้น + ค่า % ที่สมัคร (mock, แก้ได้ผ่าน drawer เล็กหรือ inline) + สถานะ "ส่งเข้ารอบเงินเดือนถัดไป" + note ชัดเจนว่า runtime จริงอยู่ฝั่ง Payroll (F065) อ่านค่าจากที่นี่ — display-only hook ห้าม mock หน้าจอ Payroll
ตรวจรับ: EMP กลุ่ม g-full เห็น PVD พร้อม % และสถานะส่งเข้ารอบ · ไม่มีหน้าจอ payroll เกิดใหม่

### 8. MINOR รวบ (ทำท้ายสุด)
- FIX-08: combobox ประเภทคน (reqEmp, balEmp, doaSlot*) เติม avatar initials (สไตล์ `.pav` ที่มีอยู่) หน้า option ให้ครบ anatomy #102 (avatar → ชื่อ → ตำแหน่ง·แผนก) — ห้ามแตะกลไก portal/keyboard เดิม
- FIX-09: แก้ mock `EMPLOYEES[].joinDate` จาก พ.ศ. เป็น ค.ศ. (เช่น 2564-05-01 → 2021-05-01) ทุกคน — หน้าคงเหลือรายคนต้องไม่แสดงปี 31xx

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT block (Rule #69) · ห้ามเปลี่ยน CI token
- ห้ามลบ comment TODO/OQ/FN ที่มีอยู่ (ยกเว้นจุดที่สั่งแก้)
- ห้ามแตะ: benefit versioning, doReject, confirmDoa, masking, EC stamps, Esc chain, overlay portal

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0 (WARN kit residuals คงได้)
3. Playwright: pageerror=0 + เคสต่อไปนี้ผ่านครบ:
   - doApprove กับ record rejected/cancelled/draft/approved → status ไม่เปลี่ยน
   - คำขอ 2 ขั้น: คลิกแรกยัง pending (ขั้น2 current) · คลิกสองถึง approved · ทุกขั้นมี at
   - pending 2 ใบรวมเกินโควตา → ใบสองถูก block · usedByPerson ≤ quota
   - archive benefit แล้วอนุมัติคำขอค้างไม่ได้ · archive มี confirm ระบุจำนวนคำขอค้าง
   - role employee: ไม่เห็นปุ่มอนุมัติ + เรียก mutation ตรงไม่ผ่าน
   - doCancelRequest กับ approved → ไม่เปลี่ยน · draft/pending → ยกเลิกได้
แนบผลรัน 3 ข้อนี้กลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict เดิม BLOCK)
