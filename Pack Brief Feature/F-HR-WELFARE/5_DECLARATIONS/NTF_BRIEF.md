# NTF_BRIEF — F-HR-WELFARE · สวัสดิการ
> ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode ช่องทาง · DOA events (doa_pending/doa_result) มาอัตโนมัติ ไม่อยู่ในใบนี้

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| welfare_request_submitted | คำขอ: draft→submitted (S-07 · §5) | HR Welfare Admin | มีคำขอใช้สิทธิ์สวัสดิการ **{request_no}** จาก {employee} รออนุมัติ | in-app | ✓ |
| welfare_request_result | pending→approved/rejected (S-07/S-11 · §5) | ผู้ยื่น | คำขอ **{request_no}** ของคุณ {ผล: อนุมัติ/ไม่อนุมัติ} | in-app+email | ✗ บังคับ |
| welfare_quota_near_limit | ยอดใช้สะสม ≥ 80% โควตา (BR-02) | เจ้าของสิทธิ์ | สิทธิ์ **{benefit_type}** ใกล้เต็มโควตา (เหลือ {คงเหลือ}) | in-app | ✓ |
| welfare_eligibility_ended | leaver signal → revoke (S-13 · BR-06) | ผู้ยื่น + HR | สิทธิ์สวัสดิการของ {employee} สิ้นสุดตามวันพ้นสภาพ **{last_day}** | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
- กลุ่มใหม่ "สวัสดิการ (welfare_*)" — 4 event ข้างบน (ยังไม่มีในกลุ่มเดิม)
## Dev wiring note
- ENG-NOTIFY.emit(event_id, {ref: request_no/employee_id, vars}) ที่ transition ตาม trigger — ห้ามเช็ค channel preference เอง (config กลาง)
