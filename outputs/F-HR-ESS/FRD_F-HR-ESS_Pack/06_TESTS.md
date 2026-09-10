# 06_TESTS — F-HR-ESS · ESS Portal (พนักงานทำเอง)

> **Audience:** QA
> **Purpose:** Acceptance per FN + DoD + Cross-Module (deep-link/consume) cases
> **🚨 Expected text (v6.1):** ยึด **ข้อความจริงบนจอ (verbatim)** จาก `outputs/F-HR-ESS/ess.html` เป็นอันดับแรก (fallback microcopy กลาง v9). QA เช็คด้วยตา — anchor ด้วยข้อความ + tab/route จริง.

---

## §6.1 Acceptance Tests (FN 15/15)

| AT | FN | Given | When | Then (expected · verbatim) |
|---|---|---|---|---|
| **AT-01** | FN-01 | login เข้า ESS (self = สมชาย ใจดี) | เปิด tab "หน้าหลัก" | เห็น self-banner "**คุณกำลังดูข้อมูลของตนเอง**" + 5 การ์ด: "สลิปล่าสุด" · "โควตาลาคงเหลือ" · "OT เดือนนี้" · "ใบเบิกค้าง" · "แจ้งเตือน" + launcher "**ต้องการยื่นคำขอใช่ไหม?**" + ปุ่ม "ยื่นคำขอ" |
| **AT-02** | FN-02 | อยู่ tab "เงินเดือน & เวลา" | แตะแถวสลิป (หรือการ์ด "สลิปล่าสุด") | drawer เปิด 2 sub-tab "**รายละเอียด**" / "**สะสมทั้งปี (YTD)**"; เห็น "ยอดสุทธิ" + note "สลิปฉบับ PDF ออกจากระบบเงินเดือน (ต้นทาง) — ESS แสดงผลอ่านอย่างเดียว เห็นเฉพาะสลิปของตนเองแบบ all-or-nothing"; footer มี "อ่านอย่างเดียว · แก้ไขไม่ได้ในพอร์ทัล" + "ปิด" (ไม่มีปุ่มบันทึก/แก้) |
| **AT-03** | FN-03 | tab "เงินเดือน & เวลา" | อ่าน section "วันลา & โควตา" + กด "**ยื่นลา**" | เห็น quota bars + ประวัติลา (read); กด "ยื่นลา" → navigate-out (prototype: toast '**กำลังนำทางไปหน้า "การลา"**'); ไม่มีฟอร์มลาในพอร์ทัล |
| **AT-04** | FN-04 | tab "เงินเดือน & เวลา" | ดู "OT & เวลาทำงาน" + "ตารางกะของฉัน" | เห็น OT summary + scans table + ตารางกะสัปดาห์นี้ (วันที่/กะ) **read-only · ไม่มีปุ่มแก้กะ** |
| **AT-05** | FN-05 | tab "เอกสาร & สิทธิ์" | ดู "ใบเบิกค่าใช้จ่าย" + กด "**ยื่นเบิก**" | เห็นใบเบิกของฉัน (read); กด → toast '**กำลังนำทางไปหน้า "เบิกค่าใช้จ่าย"**' |
| **AT-06** | FN-06 | tab "เอกสาร & สิทธิ์" | ดู "หนังสือรับรอง / เอกสาร" + กด "**ขอหนังสือ**" | เห็นเอกสารที่ออก (read); กด → toast '**กำลังนำทางไปหน้า "หนังสือรับรอง"**' |
| **AT-07** | FN-07 | tab "เอกสาร & สิทธิ์" | ดู "สวัสดิการ & อบรม" | เห็นคงเหลือสวัสดิการ (bars) + ประวัติอบรม + ใบรับรอง (read-only · ไม่มีปุ่มแก้) |
| **AT-08** | FN-08 | tab "เอกสาร & สิทธิ์" | ดู "ข้อมูลส่วนตัว / โปรไฟล์" + กด "**ขอแก้ข้อมูล**" | เลขบัตร ปชช. แสดง masked + "ปิดบัง"; ข้อความ "การแก้ไขข้อมูลต้องยื่นผ่านหน้าฟีเจอร์เจ้าของเพื่อขออนุมัติ — ESS แก้ไขข้อมูลเองไม่ได้"; กด → toast '**กำลังนำทางไปหน้า "แก้ไขข้อมูลพนักงาน (ขออนุมัติ)"**' |
| **AT-09** | FN-09 | tab "แจ้งเตือน" | เปิดแท็บ | เห็น feed "แจ้งเตือนของฉัน" (consume ENG-NOTIFY) + search "ค้นหาการแจ้งเตือน" + filter "ทั้งหมด"/"ยังไม่อ่าน" |
| **AT-10** | FN-10 | อยู่ ESS | (demo) กด "ทดสอบเข้าถึงข้อมูลพนักงานอื่น" / ส่ง employee_id คนอื่น | modal "**เข้าถึงถูกปฏิเสธ**" + "403" + "คุณ (สมชาย ใจดี) ไม่มีสิทธิ์เข้าถึงข้อมูลของพนักงานคนอื่น ระบบปิดบังและไม่แสดงข้อมูลนอกขอบเขตของคุณ" + ปุ่ม "เข้าใจแล้ว"; **backend คืน 403 ไม่ leak field** (OQ-ESS-05) |
| **AT-11** | FN-11 | surface owner ยัง ba-done | เปิด section ที่ soft ref | เห็น chip "**[ASSUMED contract]**" (demo) / display-only · หน้าไม่พัง (BR-07) |
| **AT-12** | FN-90 | tab "แจ้งเตือน" | พิมพ์คำค้นที่ไม่ตรง / กรอง | empty state "**ไม่พบการแจ้งเตือน**" + "ลองล้างคำค้นหรือตัวกรอง" (ไม่ใช่ error) |
| **AT-13** | FN-92 | เปิดบนมือถือ (≤760/1080) | ย่อจอ | layout usable (seg-tabs/tables/drawer responsive) · ไม่ล้น (BR-05) |
| **AT-14** | FN-93 | เปิด drawer โปรไฟล์ | เลื่อนดู "ประวัติการเข้าถึงข้อมูลของฉัน" | เห็น audit rows (append-only) + "บันทึกการเข้าถึงถูกเพิ่มอัตโนมัติ (แก้/ลบไม่ได้)" |
| **AT-15** | FN-94 | self viewer | ทุกหน้า | self-banner ปรากฏ · RESTRICTED masked · ไม่มีข้อมูลนอกขอบเขต self แสดง (BR-06) |

---

## §6.2 Negative / Guard Tests

| AT | สถานการณ์ | Expected |
|---|---|---|
| NEG-01 | ไม่มีปุ่ม create/save/edit/delete ที่ใดในพอร์ทัล | ✅ drawer footer มีแค่ "ปิด" (+ "ยื่นคำขอ" navigate ใน profile) — **display-only** (LK-1) |
| NEG-02 | ยื่นคำขอ = navigate เท่านั้น | ✅ ไม่มี form/submit/POST ใน ESS — deep-link ออก (LK-2/BR-03) |
| NEG-03 | payslip partial | ✅ all-or-nothing — เต็มใบหรือ 403 (BR-02/VR-5) |
| NEG-04 | reveal RESTRICTED โดยไม่ใช่ self | ✅ backend block (self-guard · VR-2/VR-3) |
| NEG-05 | ESS ยิง notification event | ✅ **ไม่ยิง** — consume only (LK-6) |

---

## §6.3 Cross-Module Tests (Value Stream R12 · §6.9)

| XT | Downstream | Given | When | Then |
|---|---|---|---|---|
| **XT-01** | deep-link (5 routes) | action-picker "ยื่นคำขอ" | เลือกแต่ละประเภท | navigate ไป route [ASSUMED]: leave→`#/leave/new` · ot→`#/ot/new` · expense→`#/expense/new` · profile→`#/profile/edit-request` · cert→`#/cert/new` — **verify route จริงกับ owner ก่อน sign-off (OQ-ESS-02)** |
| **XT-02** | deep-link fallback | route ยังไม่พร้อม | กดยื่น | graceful notice + คงหน้า ESS (ไม่ค้าง · OQ-ESS-03 `[AI-DEFAULT]`) |
| **XT-03** | ENG-NOTIFY consume | มี notification ใหม่ที่ owner | เปิด tab แจ้งเตือน | feed แสดง (read) · ESS ไม่สร้าง/แก้ event (LK-6) |
| **XT-04** | ENG-CSQ SecC | เปิดข้อมูล self / เข้าถึงคนอื่น | view / denied | emit self-access event เข้า SecC pipe — **event id [ASSUMED · OQ-ESS-01]**, verify กับ ENG-CSQ owner ก่อน sign-off |
| **XT-05** | surface degrade | owner down/timeout | เปิด dashboard | per-card "โหลดไม่ได้" ไม่ล้มทั้งหน้า (OQ-ESS-04) |

---

## §6.4 Definition of Done (DoD)

- [ ] FN 15/15 มี AT ครอบ (AT-01..15) · ผ่านทั้งหมด
- [ ] Negative NEG-01..05 ผ่าน (display-only / navigate-only / all-or-nothing / self-guard / consume-only)
- [ ] Cross-module XT-01..05 ผ่าน — **XT-01 (routes) + XT-04 (CSQ event id) มีสถานะ [ASSUMED] จนกว่า OQ-ESS-02/01 ยืนยัน**
- [ ] self-access enforce ที่ **backend** (id param → 403 ไม่ leak) — OQ-ESS-05
- [ ] RESTRICTED masking + all-or-nothing payslip
- [ ] audit append-only (แก้/ลบไม่ได้) · reveal logged
- [ ] responsive มือถือ
- [ ] ไม่มี write path ใดใน ESS (ยืนยันด้วย NEG-01/02/05)
- [ ] microcopy ตรงจอ (verbatim) · CI Warm Light (Sync Read · ไม่ hardcode)

> **Blocking ก่อน dev sign-off:** OQ-ESS-01 (CSQ event id) · OQ-ESS-02 (deep-link routes) · OQ-ESS-05 (backend self-enforce) — ดู 00_OVERVIEW §0.8.
