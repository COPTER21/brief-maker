# NTF_BRIEF — F-HR-RECRUIT · สรรหา
| Event ID | Trigger | ผู้รับ | ข้อความ | Channel | ปิดได้ |
|---|---|---|---|---|---|
| recruit_interview_scheduled | นัดสัมภาษณ์ (S-07) | ผู้สัมภาษณ์ + ผู้สมัคร | นัดสัมภาษณ์ตำแหน่ง **{position}** วันที่ {date} | in-app+email | ✗ |
| recruit_stage_changed | เลื่อน stage (S-06) | HR สรรหา + hiring manager | ผู้สมัคร **{candidate}** → {stage} | in-app | ✓ |
| recruit_offer_sent | offer approved→sent (S-09) | ผู้สมัคร | คุณได้รับข้อเสนอจ้างตำแหน่ง **{position}** | in-app+email | ✗ |
| recruit_offer_result | accepted/declined (S-10/S-11) | HR + hiring manager | ผู้สมัคร **{candidate}** {ตอบรับ/ปฏิเสธ} ข้อเสนอ | in-app | ✗ |
## Dev: ENG-NOTIFY.emit · doa_* มาอัตโนมัติ
