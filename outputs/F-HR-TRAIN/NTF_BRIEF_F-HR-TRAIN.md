# NTF_BRIEF — F-HR-TRAIN · Training (อบรม)
> ยิงผ่าน **ENG-NOTIFY.emit(event_id, {ref, vars})** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature
> DOA events (doa_pending / doa_result / doa_escalate) มาจาก DOA engine อัตโนมัติ — **ไม่อยู่ในใบนี้**
> CSQ event `train.enrolled_paid` (EC) เป็น cross-module emit ไม่ใช่ notification — อยู่ที่ CSQ_BRIEF ไม่ใช่ใบนี้

## Event ประกาศ (3 ตัว)

| Event ID | Trigger (อ้าง FRD) | ผู้รับ | Payload (ref + vars) | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|---|
| `train_session_opened` | Session `draft → open` — FN-06 `openSession` (03_LOGIC §3.1) · API-11 · 05_RULES §state "+ NTF opened" | พนักงานกลุ่มเป้าหมายของหลักสูตร (target audience) | `ref = session_id` · `{course, session}` | หลักสูตร **{course}** (รอบ {session}) เปิดรับสมัครแล้ว | in-app | ✓ |
| `train_enroll_confirmed` | Enrollment `→ confirmed` — 2 ทาง: ฟรี (FN-08 · LOCK-01) **หรือ** DOA อนุมัติครบ (FN-10 `approveEnrollmentStep`, 03_LOGIC §3.1) | ผู้เรียน (เจ้าของ enrollment) | `ref = enrollment_id` · `{course, date}` | ยืนยันเข้าอบรม **{course}** วันที่ {date} | in-app + email | ✗ บังคับ |
| `train_result` | Enrollment `confirmed → passed/failed` — FN-14 `recordResult` (03_LOGIC §3.1) · API-20 · guard closed+attended+result | ผู้เรียน (เจ้าของ enrollment) | `ref = enrollment_id` · `{course, result}` | ผลอบรม **{course}**: {ผ่าน/ไม่ผ่าน} | in-app | ✓ |

**Cross-check กับหน้าจอจริง (อบรม.html):** ทั้ง 3 event ยิงจริงบนจอ — `sessionOpen()` (L2886) → session_opened · `approveEnrollmentStep` เมื่ออนุมัติครบ (L2773) + free-path (L2823) → enroll_confirmed · บันทึก/ประกาศผล (L2797) → result · **L2946 `ntf('ส่งอนุมัติลงทะเบียน DOA')` = doa_pending ของ DOA engine → ตัดออก ไม่ประกาศซ้ำ**

## ตัดออกจากใบนี้ (โดยเจตนา)
| ตัด | เหตุผล |
|---|---|
| `doa_pending` (ส่งเข้าอนุมัติ · FN-09) · `doa_result` · `doa_escalate` | DOA engine (F-DLG-001) เป็นเจ้าของ — ประกาศซ้ำ = BLOCK |
| `train.enrolled_paid` (FN-10 EC · 05_RULES §D8) | CSQ/EC emit ข้ามโมดูล ไม่ใช่ notification ปลายทาง — อยู่ที่ CSQ_BRIEF |

## ⚠️ เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS) — ต้องยืนยันก่อน dev wire
Sync Read `f-notify.html` → `EVENT_GROUPS` ปัจจุบันมีเฉพาะสาย Sales/DOA:
`doa_pending · doa_result · doa_escalate · doc_status · doc_attach · mention · system`
— **ไม่มีกลุ่ม HR/ฝึกอบรม และไม่มี event `train_*` ในทะเบียนกลาง**

3 event ข้างต้นเป็น **feature-proposed + locked ระดับ FRD** (ชื่อตรงกันทุกที่: 03_LOGIC / 05_RULES / NTF_BRIEF ต้นทาง / HTML) แต่ **ยังไม่ถูกลงทะเบียนในทะเบียนกลาง F-NOTIFY** จึงต้องเพิ่มเป็นกลุ่มใหม่ตอน deploy:

```
กลุ่มใหม่ (เสนอ): "ฝึกอบรม (HR)"
  train_session_opened  — เปิดรับสมัครรอบอบรม            (default: app on)
  train_enroll_confirmed — ยืนยันเข้าอบรม               (default: app+email, lock=on บังคับ)
  train_result          — ผลอบรม (ผ่าน/ไม่ผ่าน)          (default: app on)
```

> **OQ-NTF-01 (ยก BA เคาะ · [รอยืนยัน]):** exact event_id string + การเพิ่มกลุ่ม "ฝึกอบรม (HR)" ต้องยืนยันกับเจ้าของ F-NOTIFY ก่อน dev wire — ไม่พบ HR training master ในทะเบียนกลาง (Sales-only) จึงยืนยันรหัสปลายทางจากทะเบียนไม่ได้ **ห้ามเดา/ตั้งระบบจริงจนกว่าจะเคาะ**

## Dev wiring note
- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref, vars })` ที่ transition ตาม trigger — **ห้าม feature เช็ค preference/channel เอง** (user preference + config กลางที่ F-NOTIFY จัดการ)
- `train_session_opened` → ใน FN-06 หลัง `status='open'` (03_LOGIC L50)
- `train_enroll_confirmed` → ใน FN-08 free-path **และ** FN-10 เมื่อ approval_done=true (ยิงครั้งเดียวต่อ enrollment)
- `train_result` → ใน FN-14 หลัง set result (03_LOGIC L118)
- email เป็น default ของ `train_enroll_confirmed` เท่านั้น (event สำคัญ/ยืนยันการเข้าร่วม) — ที่เหลือ in-app; ผู้ใช้ override ได้ที่ศูนย์ตั้งค่า F-NOTIFY

## Quality Gate (Iron rules ของ skill)
- [x] ไม่ประกาศ doa_pending/result/escalate ซ้ำ (ตัดออกชัดเจน)
- [x] ไม่ระบุ "ส่ง email/LINE" ใน logic feature — channel เป็น default ระดับใบประกาศ + user preference กลาง
- [x] ข้อความ template อยู่ในใบประกาศ ไม่ฝังใน code feature
- [x] ทุก event มี ref (session_id / enrollment_id) — ครบ 3/3
