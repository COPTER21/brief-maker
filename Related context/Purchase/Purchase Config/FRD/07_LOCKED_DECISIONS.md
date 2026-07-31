# 07_LOCKED_DECISIONS — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration)

> ตัดสินใจที่ BRD/cheat sheet/stakeholder แล้ว — FRD ห้าม override

---

## §7.1 Locked Decisions (feature-level)

### LD-01: config-driven — ห้าม hardcode
PR/PO/Comparison อ่าน effective config (API-06) ไป gate flow · ไม่ฝัง rule ในโค้ด

### LD-02: payment types ดึงจาก Payment Term (Finance)
รายการมาจาก Payment Term master · Purchase Config เลือก**เปิดใช้** + ตั้งค่าเริ่มต้น (default/%/งวด/วัน) → **inherit ไป PO** (ปรับราย PO ได้ ตาม D08/D09)

### LD-03: ไม่มี cost_center/budget_account ใน PR mandatory
มากับ **ใบปลดอายัด (UNLK)** ที่ออกจากงบแผนก · บังคับอ้างใบปลดอายัด (release_require_unlock_ref) ตั้งที่ **Budget Config (#4)** ไม่ใช่ที่นี่

### LD-04: approval → DOA
ส่ง amount ให้ DOA engine ตัดสินสายอนุมัติ · Purchase Config ไม่ตั้ง tier (สอดคล้องกฎ CUBE ห้าม hardcode approval)

### LD-05: Direct Payment ไม่อยู่ที่นี่
Direct Payment (จ่ายตรง bypass PR/PO/GRN) **เปิดที่ AP Invoice** = Finance/Accounting Config

### LD-06: GRN/QC/Putaway/tolerance → Inventory Config
flow รับของไม่อยู่ Purchase Config

### LD-07: Numbering engine reusable + forward-only
ENG-DOCNUM-01 atomic (กันเลขซ้ำ) + reset cycle (last_reset_period กันซ้ำ) · config มีผล forward-only

### LD-08: Locked decisions D01–D15 = read-only (ไม่ทำเป็น config)
แสดงในการ์ด "กติกาที่ระบบกำหนดตายตัว" — D02 GRN trigger ตาม payment type, D03 partial เสมอ, D04 auto-close, D05 lock payment type, D06 3-way, D14 CN จาก vendor ฯลฯ

---

## §7.2 P2P Cheat Sheet Decisions อ้างอิง (D01–D15)
D01 payment term ที่ PO เท่านั้น · D02 GRN trigger ตาม type · D03 รับไม่ครบ=Partial · D04 auto-close PO · D05 เปลี่ยน type หลัง approve ไม่ได้ · D06 3-way บังคับ · D07 Close PO balance ที่ GRN · D08 Deposit inherit%+ปรับ PO · D09 Installment inherit+ปรับ%/due · D10 Partial GRN กำหนดยอด · D11 Credit overdue เตือนไม่ block · D12 Subcontract=full_postpay · D13 PV 2 types · D14 CN จาก vendor · D15 Installment≠Partial

## §7.3 ID Notes
- Functions PCFG-FN-01..10 · Engine ใหม่ ENG-DOCNUM-01 (reusable ทุกโมดูลที่ออกเลขเอกสาร) · external refs: Payment Term/Budget Config/DOA/Vendor Price List (read)

## §7.4 Governance Checkpoints
- ✅ **User Access ENC** — edit เฉพาะ Admin/Manager (FN-09); viewer read
- ✅ **DOA ENC** — (optional Q1) config change สำคัญผ่าน DOA · ไม่ hardcode
- **Data Classification** = Internal (ไม่มี Confidential/PII/Restricted)
