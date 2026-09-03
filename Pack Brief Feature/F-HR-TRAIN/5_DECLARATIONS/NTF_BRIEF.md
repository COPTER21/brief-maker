# NTF_BRIEF — F-HR-TRAIN
| Event ID | Trigger | ผู้รับ | ข้อความ | Channel | ปิดได้ |
|---|---|---|---|---|---|
| train_session_opened | เปิดรับรอบอบรม (S-02) | กลุ่มเป้าหมาย | หลักสูตร **{course}** เปิดรับสมัคร | in-app | ✓ |
| train_enroll_confirmed | ยืนยันลงทะเบียน (S-04) | ผู้เรียน | ยืนยันเข้าอบรม **{course}** วันที่ {date} | in-app+email | ✗ |
| train_result | บันทึกผล (S-06) | ผู้เรียน | ผลอบรม **{course}**: {ผ่าน/ไม่ผ่าน} | in-app | ✓ |
## Dev: ENG-NOTIFY.emit · doa_* อัตโนมัติ
