# PROPOSALS_outbound — F-HR-TRAIN (อบรม · F133)

> ประเด็นที่ **feature นี้ตัดสินเองไม่ได้** — ต้องส่งกลับเจ้าของ feature/มติปลายทาง หรือ BA/SEC/Finance เคาะก่อน dev wire
> ปิดงาน 2026-09-03 · ผ่าน 12 step + BA review (7 FIX) + manual test (4 bug) + re-gate เขียว

---

## A. ข้อเสนอส่งออกไป feature/เจ้าของอื่น (outbound)

| # | ถึง | เรื่อง | สถานะปัจจุบันในงานนี้ | ต้องการ |
|---|---|---|---|---|
| **OB-NTF-01** | F-NOTIFY (F004) | ทะเบียน event กลางไม่มีกลุ่ม HR/ฝึกอบรม · 3 event `train_session_opened` / `train_enroll_confirmed` / `train_result` ยังไม่ลงทะเบียน | ประกาศใน `NTF_BRIEF_F-HR-TRAIN.md` เป็น feature-proposed (ชื่อ consistent ทุกที่) ยังไม่ hardcode | เพิ่มกลุ่ม "ฝึกอบรม (HR)" + ยืนยัน exact event_id ก่อน dev wire |
| **OB-DOA-01** | เจ้าของ DOA master / พี่เบิร์ด | `references/doa-contract.md` **หายจาก skill install** → verify role-id ปลายทางไม่ได้ · **drift:** HTML ใช้ `role-hr-dev-head` · brief/FRD ใช้ `role-hr-ld-head` (ตำแหน่งเดียวกัน) | role-id ติด `[DEFAULT—รอยืนยัน]` ทั้ง 2 ขั้น · HTML ใช้ `doaResolve()` runtime ไม่ hardcode (G7 ผ่าน) | ยืนยัน role-id จริง 2 ขั้น + เคลียร์ drift · **CL-0013 (สายผู้บริหาร) แขวน** — เพิ่ม slot 3 ไหม |
| **OB-RATE-01** | Rate Card (F060 · ยังไม่ dev) | ต้นทุน/มูลค่าอบรม (EC) + ต้นทุนต่อหัว ต้องดึงอัตรากลางจาก Rate Card | จอทำ **display-only** (badge "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม") · ต้นทุนต่อหัว = งบ/ผู้ผ่าน (จากงบที่กรอก) · ไม่ hardcode ตัวเลข Rate Card | wire ค่าจริงตอน F060 พร้อม (Phase 2) |
| **OB-EC-01** | Expense Claim (F101) / Finance | **reverse EC เมื่อยกเลิกลงทะเบียนหลังส่ง Expense แล้ว** (กระทบเงิน) | FRD ตั้ง conservative default = **ไม่ auto-reverse** | BA/Finance ยืนยันนโยบาย reverse |

---

## B. OQ ภายใน — BA/SEC เคาะ (ไม่บล็อก prototype · บล็อกการตั้งค่า/dev บางส่วน)

| OQ | ประเด็น | ค่าปัจจุบัน (default) | ผู้เคาะ |
|---|---|---|---|
| **OQ-01** | FN-10 framing: จอทำ "แนะนำผู้เรียนที่มี gap" vs checklist "แนะนำหลักสูตร" | คงจอปัจจุบัน (hook เนื้อในครบ · qc นับครอบ) | BA |
| **OQ-05** | RBAC: หัวหน้า "สร้างได้+อนุมัติ" หรือ "อนุมัติอย่างเดียว" | prototype = non-viewer สร้างได้ (ตาม recruit precedent) · viewer อ่าน+mask | SEC/BA |
| **OQ-UX-01** | ศัพท์ระบบบนจอ (`hook`/`EC`/`CSQ`/`[OB]`/`display-only`) — ตัดออกสำหรับ end-user ไหม | คงไว้ (prototype scaffolding · `jargon_leak=0`) | BA |
| **OQ-UX-02** | แถวชื่อหลักสูตรไทยยาว wrap 2 บรรทัด (สูง ~82px) — clamp หรือปล่อย | ปล่อย (โครงถูกตาม #103) | BA |
| **OQ-ERR** | 3 error code (`ERR_NOT_AUTHENTICATED` 401 · `ERR_NOT_FOUND` 404 · `BR_NO_PENDING_STEP` 422) = backend guard ไม่มีทางเข้าที่ UI | ตรวจไม่ได้ที่ prototype · dev enforce | dev/backend |

---

## C. Design System Pending (BASE-KIT — ส่งเจ้าของ design system)
บันทึกใน `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` = **DSP-02** (focus-trap × combobox-on-focus · disabled-button tooltip) + uikit helpers ที่เพิ่มรอบนี้ (C3.8)

---

## D. บันทึกที่ทำแล้ว (ไม่ต้องเคาะ — เพื่อ trace)
- **แก้ตาม BA review order 7 FIX ครบ** (FIX-01 บันทึกผลเฉพาะรอบปิด · 02 function guards · 03 เช็คชื่อ+ประเมิน 1-5 · 04 ประวัติ+ชม.สะสม · 05 ต้นทุนต่อหัว · 06 icon modal · 07 combobox portal)
- **manual test เจอ 4 bug จริง แก้ครบ** (BUG-01 การ์ดอนุมัติซ้อน · BUG-02 combobox หลักสูตรค้าง · BUG-03 tooltip ปุ่ม disabled · BUG-04 dropdown เด้งเอง) — ตัววัดหลุดทั้งหมด → เพิ่ม 4 uikit helper (append-only) กันหลุดใน feature อื่น
- **declaration รอบนี้ = doa + ntf + csq** (doccfg/pdfdoc = NOT-NEEDED · cert soft ref)
- 2 seed edge (TC-C06 ไม่มีหลักสูตร draft · TC-H03 ไม่มีผู้เรียนประวัติว่าง) = tester mark N/A ถ้าเข้าไม่ถึง
