# Derivation Playbook — แตก 1 element → หลายเคส

ใช้คู่กับ Iron Rule R5. เดิน "ทุกแถวใน Coverage Ledger" ผ่านเมนูด้านล่าง ตามชนิดของมัน แล้วจะได้
เคสครบโดยไม่ต้องนึกเอง. ตารางขวาคือ "เคสที่ต้องมี" (อย่างน้อย).

---

## 1) ฟิลด์ input (validation schema)
ต่อฟิลด์ ให้ดู constraint แล้วออกเคสตามที่ฟิลด์นั้นมี:
| constraint | เคสที่ต้องมี |
|---|---|
| required | กรอกถูก (ผ่าน) · เว้นว่าง → error required |
| format/regex | ตรง format (ผ่าน) · ผิด format → error (เช่น tax_id 13 หลัก / email RFC) |
| length/range | ค่ากลาง (ผ่าน) · ต่ำกว่า min · เกิน max (boundary ทั้งสองฝั่ง) |
| enum | ค่าที่ valid (ผ่าน) · ค่านอก enum → error |
| FK (อยู่ใน master) | code ที่มีจริง (ผ่าน) · code ที่ไม่มี → INVALID_FK_CODE |
| unique | ค่าใหม่ (ผ่าน) · ค่าซ้ำ → duplicate (block หรือ warn ตาม tag) |
| encrypt/mask (PII) | แสดงค่า masked ถูกต้อง · ไม่เก็บ plaintext (ถ้าตรวจได้บน UI) |
> type-conditional: ถ้า required ขึ้นกับ type (company vs individual) ต้องมีเคสของ **ทั้งสอง type**.

## 2) Permission matrix (role × field/action)
กวาดทุก cell: ต่อ (role, สิ่งที่ทำ) ออก **คู่** เคส — allowed = ทำได้ + เห็นผล; denied = ถูกปฏิเสธ
+ เห็น error/ปุ่มหาย/ฟิลด์ read-only. อย่างน้อยต้องครอบ: ทุก role ที่ "ทำได้" 1 เคส + ทุก role ที่
"ถูกห้าม" 1 เคส ต่อ action/section สำคัญ (create/edit-field/bulk/archive/view-sensitive/export).

## 3) CRUD lifecycle (ต่อ entity)
create (happy ครบ field) → view (เห็นค่าที่บันทึก) → edit (แก้ + diff) → archive → (restore ถ้ามี).
แต่ละขั้นเป็นเคสแยก. create happy ต้องมี step ต่อ section (Identity/Contact/Address/Bank/Financial).

## 4) List / table
- search: เจอ · ไม่เจอ (empty state) · อักขระพิเศษ/ภาษาไทย
- filter: **ทุกค่า** ของแต่ละ dropdown (เช่น status: active/vip/suspended/archived/all) + reset
- sort: ทุกคอลัมน์ที่ sort ได้ × 2 ทิศ
- pagination: ไปหน้าถัดไป/สุดท้าย · ellipsis (เมื่อหน้ามาก) · กลับหน้า 1 เมื่อ filter เปลี่ยน
- states: loading skeleton · empty (ไม่มีข้อมูลเลย) · filtered-empty (filter แล้วว่าง) · error+retry

## 5) Multi-card 1:N (address / bank)
add card · delete card · กฎ "มี primary ได้ตัวเดียว" (toggle ใบ 2 → ใบ 1 หลุด primary) ·
ลบ primary → ตัวถัดไปถูกตั้ง primary อัตโนมัติ · min-count (เช่น company ต้องมี ≥1 address → เว้น = error).

## 6) Cascade dropdown
เลือกครบถูกต้อง (ผ่าน) · parent-child ไม่ตรง → CASCADE_VIOLATION · เปลี่ยน parent → child เคลียร์ ·
auto-fill (postal) + override ได้.

## 7) CSV import
template download (มี sample) · ไฟล์ valid → preview → commit → toast · แต่ละ error แยกเคส:
missing required headers · file too large · row limit exceeded · bad format · per-row validation fail
(แสดงใน error list) · duplicate-in-file (warn) · placeholder row ถูก skip.

## 8) Bulk actions
tick ทีละแถว · master checkbox = select all หน้านี้ · indeterminate (เลือกบางส่วน) · selection ค้าง
ข้ามหน้า · bulk archive (+ already-archived → skipped) · bulk export · clear selection.

## 9) Cross-module / atomic flow
happy (convert สำเร็จ → ปลายทาง sync) · rollback (ขั้นใดล้ม → ทั้งคู่ไม่เปลี่ยน) · กันซ้ำ
(already-converted ไม่โผล่) · callback onSuccess vs onCancel · ปลายทาง down → fallback toast ·
locked contract (signature ห้ามเปลี่ยน).

## 10) Security / PII
แสดง masked ถูก format · view-sensitive ที่มีสิทธิ์ → เห็นค่า + audit log entry · ไม่มีสิทธิ์ → 403/ปุ่มหาย ·
encryption-at-rest (ถ้าตรวจได้) · RLS cross-tenant (tenant อื่นมองไม่เห็น → 404/ว่าง).

## 11) State machine
ทุก transition **ถูกต้อง** = 1 เคส · ทุก transition **ต้องห้าม** = 1 เคส (เห็น error) ·
transition ที่ต้องมี note → เว้น note = ถูกบล็อก.

## 12) UX / interaction
dirty-check: แก้แล้วปิด → confirm; ไม่แก้แล้วปิด → ปิดเลย · 3 ทางปิด (ESC/backdrop/X) · Ctrl/Cmd+S =
save · focus/scroll preservation · toast หายเองตามเวลา/คลิกปิด.

## 13) Edge cases (EC list)
ต่อ EC ที่ **สังเกตได้บน UI** = 1 เคส (เช่น timeout retain form, long address, postal override,
selection ข้ามหน้า, decryption failed → masked+แจ้ง). EC ที่เป็น Phase 2/หลังบ้านล้วน → ใส่ Ledger
ทำเครื่องหมายข้าม + เหตุผล.

---

## ปริมาณที่คาดหวัง
- pack เล็ก (1 หน้า ไม่กี่ rule) → ~10-20 เคส
- pack FULL (หลาย FR + 40+ rules + EC + permission matrix) → **คาดหวัง 50-100+ เคส** —
  อย่าหยุดที่ happy path ไม่กี่เคส. ถ้าได้น้อยกว่านี้มาก แปลว่ายังไล่ Ledger ไม่ครบ.
- จัดเคสเป็น group ตามหน้า/journey เพื่อให้อ่าน/รันเป็นชุดได้.

---

## 14) Archetype นอกเหนือ CRUD (dashboard / console / report)
playbook ข้อ 1-13 เน้นฟอร์ม+ลิสต์. ถ้า feature เป็นชนิดอื่น ใช้แนวนี้เพิ่ม:

**Dashboard / Report (display-heavy):**
- ทุก widget/การ์ด/กราฟ = 1 เคส VERIFY ค่าตรงกับ data ที่คาด (ตัวเลข/แกน/legend)
- ทุก filter/ช่วงเวลา (date range, drill-down) = เคสเปลี่ยนค่าแล้ว widget อัปเดตถูก
- empty / loading / error ของแต่ละ widget
- export/print ของรายงาน (ถ้ามี) + ตรงกับ filter
- สิทธิ์: role ไหนเห็น widget ไหน (allow/deny)

**Console (display + action ในหน้าเดียว — kanban/workload/agent console):**
- ทุก action บน item (assign, move, approve, reject, ...) = allow + deny ตามสถานะ/สิทธิ์
- state change ของ item แล้ว UI ขยับถูก (เช่นการ์ดย้ายคอลัมน์)
- bulk/drag (ถ้ามี) + optimistic UI + rollback เมื่อ fail
- realtime/refresh (ถ้ามี) — mark สังเกต/รอ (WAIT)

**Wizard / multi-step:**
- เดินครบทุก step (happy) + กันข้าม step ที่ยังไม่ valid + ปุ่ม back คงค่า + ออกกลางคัน
- validation ต่อ step + step สุดท้าย submit atomic

> หลักเดียวกัน: ทุก "สิ่งที่แสดง" = VERIFY 1 เคส; ทุก "สิ่งที่กดได้" = allow + deny; ทุก "สถานะ" = ถูก + ผิด.
> แล้วลง Ledger เหมือนเดิม (FR/rule/EC/error/permission/state).

## Cross-Module (XT — v6)
จาก 06_TESTS §6.9 + 02_API §2.X:
- **forward:** ทำ action ต้นทาง → VERIFY ผลฝั่งปลายทาง (หรือ event/toast ถ้า prototype ไม่มีหน้า downstream)
- **compensating:** แก้/ยกเลิกกลางทาง → VERIFY ปลายทางถูก release/rollback (ใช้ R17 capture baseline ก่อนเสมอ —
  เช่น จด budget commitment ก่อนยกเลิก PR)
- **Setup:** seed ทั้งสองฝั่ง + role ที่เห็นทั้งคู่; ทำไม่ได้ → `(ต้อง simulate)`
