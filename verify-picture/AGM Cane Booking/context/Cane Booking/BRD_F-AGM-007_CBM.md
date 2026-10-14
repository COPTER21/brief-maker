# BRD — F-AGM-007 Cane Booking Management (CBM) · จัดการจองรอบส่งอ้อย

| Field | Value |
|---|---|
| Feature ID | F-AGM-007 (เดิม ETCD) |
| Module | AGM · Site WKN |
| Status | **APPROVED** (Refactor + Enhancement Synthesis v1.1→v1.7 — constraint mode จาก invariants.md 🔒) |
| Type | Refactor (rename ETCD→CBM) + Enhancement (cumulative) |
| Upstream/Events | read Quota/Crop/Season · รับ event Receiving/Payment/Check-In · Debt Mgt |
| Author | brd-generator-full (SOW3.2) |

---

## §1 Executive Summary
ระบบจัดการการจองรอบส่งอ้อยของโรงงาน (เดิมชื่อ ETCD) ยกเครื่องเป็น **Cane Booking Management (CBM)** — จัดระเบียบสถานะการทำงานเป็น **3 แกนต่อเนื่องแบบห้ามข้ามขั้น (no-skip)**: การอนุมัติจอง → การตัด/ขนส่ง → การจ่ายเงิน · แสดงผลรวมเป็น **ไทม์ไลน์เดียว 10 ขั้น** พร้อมสถานะที่คำนวณ (derived: รอส่งอนุมัติตัด, อยู่ระหว่างจัดส่ง, รอผลการเท) · บางสถานะถูกควบคุมโดยระบบภายนอกเท่านั้น (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) · รองรับการหักหนี้เป็น % · และพิมพ์เอกสาร A4 (ใบสั่งตัด/ใบส่งอ้อย) พร้อม QR

## §2 Objectives & Metrics
| # | Objective | Metric |
|---|---|---|
| 2.1 | ลดสถานะข้ามขั้น | 0 การเปลี่ยนสถานะที่ผิดลำดับ (no-skip guard) |
| 2.2 | ป้องกันแก้สถานะระบบด้วยมือ | 100% ปฏิเสธ manual → ILLEGAL_STATE_TRANSITION |
| 2.3 | เอกสารพิมพ์ครบ | ใบสั่งตัด/ใบส่งอ้อย พิมพ์ได้ตาม gate + QR ทำงาน |
| 2.4 | ตรวจสอบย้อนหลัง | audit + event ครบทุก transition |
| 2.5 | idempotency | event ซ้ำ → no-op/409 (ไม่ซ้ำผล) 100% |

## §3 Scope

### §3.1 In Scope
CRUD booking · 3-axis state machine (no-skip) · combined 10-step timeline + derived display · phase "-" + filter "ยังไม่เริ่ม" · actions per RBAC + reason on reverse · system-controlled locks + simulated external events · debt deduction % · print 2 PDFs + per-row download + bulk ZIP · search/filter/sort/export

### §3.2 Out of Scope (Non-Goals v1.1)
เชื่อมลอจิกจริง 3 ฟีเจอร์อนาคต (รับอ้อย/ทำจ่าย/ใบเสร็จ) — เตรียมสถานะ+ปุ่ม/จำลอง event เท่านั้น · ไม่แก้ตรรกะนับความจุเลน/slot

### §3.4 Scope Lock (→ FRD 00_OVERVIEW)
| LOCK | ข้อความ |
|---|---|
| **LOCK-01** | 3-axis state model (approval/cut_transport/payment) · no-skip (Gate: B เมื่อ A=verified · C เมื่อ B closed) |
| **LOCK-02** | **ไม่มี `dispatched`** ในแกน B (v1.3) · ปิดแกน B ด้วย `cut_transport_closed_at` (receiving event) |
| **LOCK-03** | combined timeline **10 ขั้น**: รออนุมัติ→อนุมัติรอบจองแล้ว→รอส่งอนุมัติตัด→รออนุมัติตัด→รอตัด→รอจัดส่ง→อยู่ระหว่างจัดส่ง→รอผลการเท→รอทำจ่าย→เสร็จสิ้น |
| **LOCK-04** | derived states: รอส่งอนุมัติตัด (verified&cut=null) · อยู่ระหว่างจัดส่ง (dispatch_started) · รอผลการเท (checkin&!dump) |
| **LOCK-05** | **system-controlled (non-manual)**: รอผลการเท/รอทำจ่าย/เสร็จสิ้น — รับผ่าน event เท่านั้น + badge 🔒 |
| **LOCK-06** | phase display "-" เมื่อยังไม่เริ่ม + filter "ยังไม่เริ่ม" (derived, ไม่เก็บ DB) |
| **LOCK-07** | verified label = **"อนุมัติรอบจองแล้ว"** (v1.5) |
| **LOCK-08** | idempotent + optimistic lock (row_version) ทุก action/event · reverse ต้องมี reason + audit |
| **LOCK-09** | debt_deduction_percent 0-100 · offset จริงที่ Payment |
| **LOCK-10** | print ใบสั่งตัด (≥awaiting_cutting) · ใบส่งอ้อย (≥awaiting_dispatch) + QR → `/:id/view` · bulk ZIP |
| **LOCK-11** | completed → read-only (lock) |

## §4 Cross-Module & Events Contract ⭐ (→ FRD 02_API §2.X)
| Item | รายละเอียด |
|---|---|
| Read | Quota (farmer snapshot) · Crop · Season (open/closed) |
| Debt Mgt | `GET /api/debt/debtors?quota_id=` → outstanding (แสดง %) |
| **Event: check-in** | (ระบบ Check-In) → derived "รอผลการเท" |
| **Event: receiving-completed** | (ระบบรับอ้อย) → ปิดแกน B (closed_at) + payment=awaiting_payment ("รอทำจ่าย") |
| **Event: payment-completed** | (ระบบการเงิน) → payment=completed ("เสร็จสิ้น") |
| ทุก event | idempotent (event_id) · non-manual (guard) · prototype = ปุ่มจำลอง |

## §5 Personas & Permissions (→ invariants §4)
CBM.Approver/Admin (approve/reject/cancel, ขออนุมัติตัด) · Cut.Manager (อนุมัติตัด/จบการตัด/print CUT) · Dispatch.Manager (เริ่มจัดส่ง/print DLV) · Finance.Manager (via events) · ระบบภายนอก (system events)

## §6 Data Requirements
T_cbm_bookings (invariants §1) · T_cbm_history (audit+events) · read Quota/Crop/Season · Debt snapshot · doc numbers (CBM-CUT/CBM-DLV รันแยก)

## §7 Functional Stories
| US | Story |
|---|---|
| US-01 | สร้าง booking (quota/crop/season/รถ/เลน/เวลา + debt%) → waiting_for_verify |
| US-02 | อนุมัติ/ปฏิเสธ/ยกเลิก (+reason) จอง |
| US-03 | เดินแกน B: ขออนุมัติตัด→อนุมัติตัด→จบการตัด→เริ่มจัดส่ง (per RBAC, no-skip) |
| US-04 | จำลอง event ระบบ: check-in→รอผลการเท · receiving→รอทำจ่าย · payment→เสร็จสิ้น |
| US-05 | list 3-axis columns + derived "-" + combined progress + filter "ยังไม่เริ่ม" |
| US-06 | detail: timeline 10 ขั้น + 3-axis badges + sections + actions + system-lock badge |
| US-07 | print ใบสั่งตัด/ใบส่งอ้อย (gate) + QR · download per row + bulk ZIP |
| US-08 | debt % + outstanding snapshot |
| US-09 | manual void (+reason) revert 1 ขั้น · completed=lock |
| US-10 | search/filter/sort/export CSV (แสดง "-" ตามจอ) |

## §11 Non-Functional
list p95<3s · action<1s · event idempotent · PDF ไทยครบ + QR · optimistic lock · alias `/etcd/*` (deprecate)

## §12 Value Stream Impact
Farmer→Quota→Plot→Crop→Contract → **CBM (จองรอบส่งอ้อย)** → [รับอ้อย/ชั่ง→ทำจ่าย→ใบเสร็จ] · ETCD tab ใน Crop อ่าน booking

## §17 Open Questions → invariants §8 (OQ-CB1..CB4)

## §18 Dashboard Widgets
Booking ทั้งหมด · รออนุมัติ · กำลังตัด/ขนส่ง · รอผลการเท/รอทำจ่าย · เสร็จสิ้น
