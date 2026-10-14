# BRD — F-AGM-011 Cane Receiving (การรับอ้อย/ออกใบรับอ้อย)

> Constraint mode (จาก invariants.md 🔒 · base + Enhancement v2) · Module เกษตรกรรม (AGM)/หน้างานโรงงาน · WKN · สถานะ: APPROVED

## §1 Business Context
การออก **ใบรับอ้อย (Receiving Note, CRN)** ที่โรงงาน — ดึง **ผลการเท (dump result)** จากโรงงานมาผูกกับคันรถที่ Check-in แล้ว (F-AGM-010) ออกใบ + PDF/QR พร้อม side effects (CBM → awaiting_payment, ปลดเลขเหรียญชั่ง). Receiving เป็น **single source of truth** ของน้ำหนักอ้อยสุทธิ + ประเภทอ้อย ที่ Cane Payment ใช้ต่อ. เอกสารนี้รวม **Enhancement v2** (Dump Result v2 & Sync All) เป็น truth ล่าสุด.

## §2 Problem / Opportunity
ของเดิม: dump คืนแค่ {ccs, net_weight}, query ด้วย date+coin, ต้องกดออกใบทีละคัน. Enhancement: dump ชุดเต็ม (ประเภทอ้อย/เวลาเข้า-ออก/น้ำหนักรวม-รถเบา-สุทธิ · **ไม่มี CCS** ย้ายไป Payment), query ด้วย checkin_datetime+coin+quota_id, + **Sync All** (ดึง+ออกใบอัตโนมัติเป็นชุด ลดภาระคิวเยอะ). Refactor → CUBE Warm Light + governance.

## §3 Goals & Scope
### §3.4 Locked Decisions (LOCK — จาก invariants)
| LOCK | Decision |
|---|---|
| LOCK-01 | คงพฤติกรรม AS-BUILT (enhanced) 100% + Enhancement v2 เป็น truth |
| LOCK-02 | **Dump v2**: ดึงผลการเทด้วย checkin_datetime+weigh_coin+quota_id → ประเภทอ้อย+เวลาเข้า/ออก+น้ำหนักรวม/รถเบา/สุทธิ (**ไม่มี CCS**) (BR-01) |
| LOCK-03 | Auto สำเร็จ → lock read-only · fail → manual (net 2-dec + เหตุผล) (BR-02) |
| LOCK-04 | net = gross − tare (หรือ manual) (BR-03) |
| LOCK-05 | **ออกใบรับอ้อย → side effects**: CRN + Issued + CBM awaiting_payment + ปลดเหรียญชั่ง + PDF A4+QR (BR-04) |
| LOCK-06 | POST /cane-receivings idempotent (ไม่สร้างซ้ำ) (BR-05) |
| LOCK-07 | **Sync All**: ดึง+ออกใบอัตโนมัติเป็นชุด (date range) → result modal (success/failed) (BR-06) |
| LOCK-08 | Sync All บังคับเลือกวันที่ + ไม่รันซ้อน (BR-07) |
| LOCK-09 | **Receiving = SoT for Payment**: ส่ง net_weight_kg + cane_type_code (CCS ที่ Payment) (BR-08) |
| LOCK-10 | **Void → rollback** CBM awaiting_dump_result + block payment · reason ≥5 (BR-09) · void ไม่ได้ถ้าจ่ายแล้ว (BR-10) |
| LOCK-11 | ดึงผลการเทใช้ได้เฉพาะรายการยังไม่ออกใบ (BR-11) |

### Out of Scope
CCS (ทำที่ Payment) · แก้ flow Check-in · กติกา CBM/Debt/Payment อื่น · scale hardware · factory API จริง.

## §4 Entities & State
- **ReceivingItem** (CHK-#### → CRN-YYYY-#####): Draft(รอผลเท)/Issued(เทแล้ว)/Void(ยกเลิก) + dump v2 fields
- **DumpResult v2**: caneType + timeIn/out + gross/tare/net + source auto/manual
State machine → invariants §4.

## §5 Key Business Rules
BR-01..12 (invariants §3). สำคัญ: dump v2 no-CCS (BR-01), auto-lock/manual (BR-02), issue side effects (BR-04), Sync All bulk (BR-06), Receiving=SoT (BR-08), void rollback (BR-09), void-blocked-if-paid (BR-10).

## §6 Functional Requirements (สรุป → FRD)
1. **US-01 Receiving List** — 3 แท็บ (รอผลเท/เทแล้ว/ยกเลิก) · filter สถานะ/ประเภทอ้อย/entryType/date · search coin · Export CSV · stats
2. **US-02 Issue Receiving** — checkin snapshot + ดึงผลการเท (Auto) v2 · manual fallback · ออกใบ (side effects)
3. **US-03 Sync All** — ดึง+ออกใบอัตโนมัติเป็นชุด (date range) · result modal
4. **US-04 Detail** — ดูข้อมูล + ผลการเท (read-only)
5. **US-05 PDF/Print** — A4 + QR viewer/print
6. **US-06 Void** — reason≥5 → rollback CBM + block payment
7. **US-07 QR scan / Search** — เช็คอินด้วย QR / ค้นเลขเหรียญชั่ง
8. **US-08 Cross-module** — feed Payment (net+cane_type) · CBM sync · free coin

## §7 Non-Functional
list p95<3s · issue<2s · Sync All async (batch) idempotent · dump snapshot audit · PDF ไทย A4+QR · RBAC (Staff/Supervisor/Admin/Viewer) · optimistic (etag).

## §18 Stats (list dashboard)
4 การ์ด: รอผลเท (Draft) · ออกใบวันนี้ (Issued) · ยกเลิก (Void) · น้ำหนักอ้อยรวมวันนี้ (Σ net).

## §Cross-Module Map
```
Check-In (F-AGM-010) ──checked-in──▶ Receiving (Draft "รอผลเท")
Factory dump API ──dump v2──▶ Receiving (caneType + weights)
Receiving (F-AGM-011) ──issue──▶ CBM(F-AGM-007) awaiting_payment + free Weigh Coin + PDF/QR
Receiving ──net_weight + cane_type (SoT)──▶ Cane Payment
Receiving ──void──▶ CBM awaiting_dump_result
```
