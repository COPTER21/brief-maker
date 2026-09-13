# Pending Registry — เฉพาะที่ ความยินยอม PDPA (F-MKT-CONSENT) ลงไว้

> คัดจากทะเบียนกลาง `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` (ต้นฉบับที่เจ้าของ design system ต้องแก้)

| ID | ประเภท | รายละเอียดย่อ | สถานะ |
|---|---|---|---|
| MG-01 | uikit meter-gap (combobox) | ตัวตรวจ DSP-02 (`assert_combobox_closes_after_select` / `modal_autoopens_comboboxes`) hardwired กับ BASE-KIT `ss-*` เท่านั้น → ตรวจ combobox ที่ feature เขียนเอง (`.combo` / `cx_*`) ไม่ได้ · feature นี้จึงเขียน e2e คุ้ม DSP-02 ด้วย feature anchors เอง | รอเจ้าของ design system generalize check ให้รับ selector อื่นนอก `ss-*` |

DSP-01..04 (z-index/combobox/click-delegation ของ BASE-KIT) ได้ pre-wire ป้องกันในต้นแบบนี้แล้ว — ดูทะเบียนกลางสำหรับรายการที่ยังรอแก้ต้นทาง
