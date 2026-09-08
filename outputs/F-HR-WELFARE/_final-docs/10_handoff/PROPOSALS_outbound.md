# PROPOSALS_outbound — F-HR-WELFARE (F102 Welfare · สวัสดิการ)
> ข้อเสนอ/คำถามที่ส่งออกไปยัง BA / แผนกลาง / feature อื่น — ปิดงาน WF-01 2026-09-08
> (ในไฟล์นี้ = ของที่ **ต้องมีคนนอก feature เคาะ** ก่อน dev เอาไปตั้งค่า/สร้างจริง)

## 1. แผนกลาง (Cube_Feature_List) — chip ไม่ตรง
| id | เรื่อง | ปัจจุบัน | เสนอ | owner |
|---|---|---|---|---|
| PR-01 | F102 dec chip ขาด **ntf** | plan `dec=["doa","csq"]` | เพิ่ม `ntf` (STANDARD_BASELINE cap.12 MUST + PREBRIEF §12 + มีเนื้อแจ้งเตือน 5 event จริง) · user ยืนยันใช้ ntf ตั้งแต่ kickoff | PM/BA |

## 2. DOA (F-DLG-001 · สายอนุมัติกลาง)
| id | เรื่อง | สถานะ | owner |
|---|---|---|---|
| OQ-DOA-01 🔴 | **role id จริง 2 ตัว** ของสาย (หัวหน้าสายงาน / HR สวัสดิการ) | brief ใช้ placeholder `role-hr-line-manager` / `role-hr-welfare-admin` `[DEFAULT — รอยืนยัน]` — ไม่มี DOA master ให้ verify → **blocker ตอน dev wire** | BA / พี่เบิร์ด |
| A-WEL-03 / CL-0013 | ผู้บริหารต้องเซ็นสวัสดิการบางประเภทมั้ย (แขวน 31 ส.ค.) | research ตัดสิน: **ไม่มี exec-path** (welfare ไม่ผูกวงเงินแบบ capex) · 2 ขั้น หัวหน้า→HR ไม่มีวงเงิน | พี่เบิร์ด ยืนยัน |
| OQ-DOA-03 | approver ในสายลาออกกลางคัน (สาย freeze แล้ว) | ยังไม่กำหนด | BA |

## 3. Payroll / Expense (F065 / F101) — hook จ่าย
| id | เรื่อง | สถานะ | owner |
|---|---|---|---|
| A-WEL-02 / OQ-03 🔴 | **สัญญา hook สถานะจ่าย** (Welfare อ่าน · Payroll/Expense จ่าย) + **payroll clawback** ตอนกลับรายการ | HTML/FRD ทำ display-only `[ASSUMED contract]` — ต้องนิยาม field/endpoint จริงกับ F065/F101 | Strike + ทีม Payroll |
| OQ-WEL-02 | จ่ายประจำ (กองทุนสำรองฯ %) ทำ enroll ที่ F102 หรือยกไป F065 ทั้งก้อน | research ตัดสิน: **enroll ที่ F102 (display-only) · หักจริง F065** — ขอ F065 ยืนยันรับ contract | Strike + พี่เบิร์ด |

## 4. Reversal / คงเหลือ (นโยบายเชิงลึก — เข้า FRD Phase B)
| id | เรื่อง | สถานะ | owner |
|---|---|---|---|
| OQ-WEL-01 | **กลับรายการหลังอนุมัติ/จ่าย** | research ตัดสิน + **ทำแล้ว (minimal)**: append-only · คืนสิทธิ์ · EC reverse · clawback flag · admin-only · reason บังคับ — ต้องยืนยัน "นโยบายกลับรายการเต็ม" (เช่น มีเอกสารกลับรายการทางบัญชีมั้ย) | Strike |
| OQ-WEL-03 / OQ-04 | pending จองสิทธิ์ (soft-reserve) vs เช็คตอนอนุมัติ + **atomic re-check** กันแข่งอนุมัติพร้อมกัน | research ตัดสิน: **เช็คตอนอนุมัติ** + โชว์ exposure (`[AI-DEFAULT]` · atomic เป็นเรื่อง backend) | Strike / Dev |

## 5. Backend enforcement + soft-ref ที่ verify ไม่ได้ในรอบนี้
| id | เรื่อง | owner |
|---|---|---|
| OQ-05 🔴 | permission ต้อง enforce **ฝั่ง backend** ด้วย (HTML กันแค่ UI+client guard) `[AI-DEFAULT]` | Dev / Security |
| REF-01 | contract จริงของ **On/Offboard** (`employment-window/resolve?include=signal` · joiner/leaver) — plan=done แต่ไม่มี output/`HR_DONE_CONTRACTS/` ให้ diff | BA หา source |
| REF-02 | **HR Configuration #107** (company_scope · ปฏิทิน/ปีสิทธิ์) — อ่านอย่างเดียว ต้องมี contract | BA |
| A-WEL-01/04/05 | benefit master เป็นของ Welfare · ผู้ติดตามเก็บใน Welfare · open-enrolment/life-event `[AI-DRAFT]` | Strike ยืนยัน |

## 6. Design System (ส่งเจ้าของ BASE-KIT) — อยู่ที่ `_SHARED/DESIGN_SYSTEM_PENDING.md`
- **DSP-01** modal z-index (จมใต้ drawer) — **เกิดซ้ำใน F102** แก้สำเนาแล้ว · รอแก้ต้นทาง
- **DSP-02** combobox focus/auto-open — **เกิดซ้ำใน F102** แก้สำเนาแล้ว · รอแก้ต้นทาง
- (person-cell name/meta ชนบรรทัด = CSS ระดับ feature ไม่ใช่ skeleton → ไม่ลง DSP · เพิ่ม uikit check `person_cell_line_collision` กันทุก feature แล้ว)

---
**declaration รอบนี้:** doa + ntf + csq (csq = EC เท่านั้น + reverse) · doccfg/pdfdoc = NOT-NEEDED
**สรุป:** ไม่มี OQ ที่บล็อก WF-01 pipeline (ทุก gate เขียว) · แต่ 🔴 4 ตัว (OQ-DOA-01 · A-WEL-02/OQ-03 · OQ-05) เป็น **blocker ตอน dev เอาไป wire/ตั้งค่าจริง** — ต้องเคาะก่อน build
