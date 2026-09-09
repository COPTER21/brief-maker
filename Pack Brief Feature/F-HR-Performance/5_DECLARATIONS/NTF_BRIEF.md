# NTF_BRIEF — F-HR-PERF
| Event ID | Trigger | ผู้รับ | ข้อความ | Channel | ปิดได้ |
|---|---|---|---|---|---|
| perf_cycle_opened | รอบเปิดกรอก (S-01) | พนักงาน+หัวหน้าในรอบ | รอบประเมิน **{cycle}** เปิดให้กรอกแล้ว | in-app+email | ✓ |
| perf_overdue | เกินกำหนดกรอก (S-08) | ผู้ที่ยังไม่กรอก | แบบประเมิน **{cycle}** ครบกำหนด {date} | in-app+email | ✗ |
| perf_result_published | สอบทานเสร็จ→เผยแพร่ (S-05) | พนักงานเจ้าของ | ผลประเมินรอบ **{cycle}** เผยแพร่แล้ว | in-app | ✗ |
## Dev: ENG-NOTIFY.emit · doa_* อัตโนมัติ
