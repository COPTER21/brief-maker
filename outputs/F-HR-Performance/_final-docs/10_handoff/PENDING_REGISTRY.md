# PENDING Registry — F131 Performance (สรุปเฉพาะ feature นี้)

> ทะเบียนกลางอยู่ที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` — ไฟล์นี้สรุปเฉพาะที่แตะ F131

## BASE-KIT bugs ที่เกิดซ้ำ (แก้สำเนา feature แล้ว · ต้นทางยังไม่แก้)
| รหัส | อาการ | สถานะใน F131 |
|---|---|---|
| DSP-01 | modal เปิดในลิ้นชักจมใต้ drawer (z-index) | ✅ แก้สำเนา (`.modal-backdrop` z=var(--z-portal)) · e2e DSP-01 คุม |
| DSP-02 | (a) combobox ไม่ปิดหลังเลือก · (b) modal เปิดแล้ว dropdown กางเอง | ✅ แก้สำเนา (guardOverlayAutoCombo) · e2e DSP-02a/02b คุม |

→ ทั้งคู่ยัง**รอเจ้าของ design system แก้ต้นทาง** BASE-KIT (จุดเดียวกันจะหลุดใน feature ถัดไปถ้าไม่แก้ต้นทาง)

## OQ ที่ยกออก (รายละเอียดเต็มใน `PROPOSALS_outbound.md`)
OQ-PERF-05 CL-0013 role-id · 06 CSQ EC valuation · 07 payload ปลายทาง · 08 360/competency · 09 concurrent-lock · 10 restricted-wire · 11 mock-data (หัวหน้าฝ่ายผลิตไม่มีคนขั้น mgr) · 12 re-open notify event
