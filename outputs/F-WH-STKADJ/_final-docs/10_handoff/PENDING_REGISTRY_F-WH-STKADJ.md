# PENDING_REGISTRY — รายการของ F-WH-STKADJ (extract)

> ทะเบียนกลางอยู่ที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` — ไฟล์นี้คัดเฉพาะ 2 รายการที่พบใน feature นี้ (2026-09-16)
> ทั้งคู่ = C3.8 (แก้สำเนา feature + เพิ่ม uikit check + prove-by-revert แล้ว) · **รอเจ้าของ design system แก้ที่ BASE-KIT ต้นทาง**

| ID | ประเภท | รายละเอียด | แก้ + ตัววัด |
|---|---|---|---|
| **DSP-05** | BASE-KIT z-scale gap (popover-in-modal) | z-scale เดิมไม่มีชั้นเหนือ modal สำหรับ popover ที่เปิดในกล่อง modal → `.combo-pop`/`.menu-fixed` ใช้ `--z-portal`(60) < modal(70) → dropdown เลือกผู้อนุมัติในกล่อง "ส่งอนุมัติ" จมใต้ modal กดไม่ได้ · ผู้ใช้เจอเอง (UAT รอบ 3) · สายพันธุ์เดียวกับ DSP-01 แต่ขาดชั้น **เหนือ** modal | เพิ่ม `--z-combopop:75` (dropdown40 < drawer50 < portal60 < modal70 < **combopop75** < toast80) + `.combo-pop,.menu-fixed{z-index:var(--z-combopop)}` · uikit `assert_pop_above_modal` · prove-by-revert (ย้อน z→60 = FAIL) · e2e `DEF-SUBMIT-MODAL` |
| **DSP-06** | BASE-KIT trap-stack leak (navigate-between-overlays) | เปิด overlay ใหม่ก่อนปิดตัวเดิม (กลับรายการ → navigate ไป view ใบใหม่ก่อน `closeModal` + `openViewDrawer` ไม่ release trap เดิม) → `_trapStack` ไม่สมดุล → `body.is-overlay-open` ค้าง → scroll ล็อกทั้งจอหลังปิด · ผู้ใช้เจอเอง (UAT รอบ 3) | `openViewDrawer` เรียก `releaseFocus()` ถ้ามี view เดิมเปิด + สลับลำดับ reverse callback (`closeModal()` ก่อน `doReverse()`) · uikit `assert_no_scroll_lock_leak` · prove-by-revert · e2e `c_rev_doa` |

**ข้อเสนอ (รอเจ้าของ design system):**
- DSP-05 → เพิ่มชั้น z มาตรฐานสำหรับ popover-in-modal ที่ BASE-KIT ต้นทาง
- DSP-06 → ทำ trap-stack ให้ idempotent เมื่อ navigate ระหว่าง overlay (release trap เดิมอัตโนมัติก่อน push ใหม่)
