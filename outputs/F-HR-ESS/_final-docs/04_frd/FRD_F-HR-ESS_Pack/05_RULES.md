# 05_RULES — F-HR-ESS · ESS Portal (พนักงานทำเอง)

> **Audience:** BE dev + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Error Catalog + Data Classification / Security enforcement
> **Scope reminder:** display-only aggregator — rule ส่วนใหญ่เป็น **Prevent** (ห้ามทำ) + **self-access/masking**. ไม่มี rule เชิงเงิน/คำนวณ/สถานะของตัวเอง.

---

## §5.1 Business Rules (จาก BRD §9)

| BR | กฎ | ประเภท | Tag | Enforce ที่ |
|---|---|---|---|---|
| **BR-01** | ห้าม CRUD surface feature อื่น (display-only) | Prevent | FIXED | สถาปัตยกรรม — ไม่มี mutation endpoint (02_API) |
| **BR-02** | สลิปอ่าน PS-1 · **self เท่านั้น · all-or-nothing** | Prevent | FIXED | API-02 · FN-02 (backend) |
| **BR-03** | ยื่นคำขอ = **navigate** ไปหน้าเจ้าของ (ไม่ทำ form เอง) | Trigger | FIXED | FN-08 deep-link (client) · §2.4 |
| **BR-04** | dashboard = สรุป read จากหลาย surface | — | CONFIGURABLE 🤖 | FN-01 · การ์ดที่โชว์ = config-driven (Admin Panel Phase 2) |
| **BR-05** | responsive (พนักงานใช้มือถือ) | — | FIXED | 01_UI §1.5 |
| **BR-06** | **self-access เท่านั้น** · เข้าถึงคนอื่น = 403 (SecC) | Prevent/Error | FIXED | FN-04 (backend) · §5.7 |
| **BR-07** | surface ba-done = **[ASSUMED contract] soft ref** | Warning | WARNING | FN-03 degrade + chip (FN-11) · resolve เมื่อ owner done |
| **BR-08** | audit(อ่าน) **append-only** · masking ตาม self | — | FIXED | FN-05/FN-07 · T_ess_access_audit |

### §5.2 Flexibility Summary
- **FIXED:** BR-01/02/03/05/06/08 — สัญญาสถาปัตยกรรม portal display-only + SecC (เปลี่ยนไม่ได้โดยไม่เปลี่ยน archetype · = Scope Lock 00 §0.11).
- **CONFIGURABLE 🤖:** BR-04 (รายการการ์ด/surface ที่ dashboard รวม) — Admin Panel, config-driven.
- **WARNING:** BR-07 — รอ owner ba-done เพื่อเปลี่ยน [ASSUMED] เป็น contract จริง.
- ไม่มี rule DYNAMIC/Engine ที่ AI เดา.

---

## §5.3 Permission Matrix

| Role | ดูข้อมูลตัวเอง | ยื่นคำขอ (navigate) | ดูข้อมูลคนอื่น | CRUD ใน ESS | อนุมัติ |
|---|:--:|:--:|:--:|:--:|:--:|
| พนักงาน (self) | ✅ ทุก surface (masking ตาม self) | ✅ (navigate-out) | ❌ **403** | ❌ (ไม่มี) | ❌ (ไม่มีในพอร์ทัล) |
| System (ESS) | serve read (self-scope) | route ออก | ปิดบัง/403 | — | — |

> ไม่มี admin/manager ในรอบนี้ (NS-4). Manager self-service = NICE ไม่รองรับ.

---

## §5.4 Validation Rules

| VR | กฎ | Response |
|---|---|---|
| **VR-1** | route deep-link ปลายทางไม่ยืนยัน → แสดง [ASSUMED] chip · **ไม่ hardcode contract** (OQ-ESS-02) | chip + fallback graceful (OQ-ESS-03) |
| **VR-2** | ข้อมูล RESTRICTED (national_id/bank) → **masking ตาม self**; reveal เฉพาะ self → log | masked default · reveal_restricted audit |
| **VR-3** | เข้าถึง employee_id ≠ self (ผ่าน param/URL) → **403** ที่ backend · **ไม่ leak field ใด** | 403 modal (FN-10) · CSQ access_denied |
| **VR-4** | search/filter notif ไม่พบ → empty state (ไม่ใช่ error) | "ไม่พบการแจ้งเตือน" (FN-90) |
| **VR-5** | payslip = all-or-nothing → ห้าม partial projection | เต็มใบ หรือ 403 (BR-02) |

---

## §5.5 Edge Cases

### §10.1 Confirmed (☑ จาก BRD §10.1 / HTML)
| EC | สถานการณ์ | พฤติกรรม |
|---|---|---|
| EC-01 | เข้าถึงข้อมูลคนอื่น | 403 + ปิดบัง (modal `accessDenied`) — FN-10/94 |
| EC-02 | surface ba-done | display-only + [ASSUMED] chip — FN-11/BR-07 |
| EC-03 | ยื่นคำขอ | deep-link navigate-out (ไม่มี form ในพอร์ทัล) — BR-03 |
| EC-04 | ค้น/กรอง feed ไม่พบ | empty "ไม่พบการแจ้งเตือน / ลองล้างคำค้นหรือตัวกรอง" — FN-90 |
| EC-05 | mobile | responsive — FN-92 |
| EC-06 | payslip บางส่วน | all-or-nothing (เห็นทั้งใบ/ไม่เห็น) — BR-02 |

### §10.2 AI Probes (☐ conservative default · `[AI-DEFAULT]` · รอ BA)
| EC | สถานการณ์ | `[AI-DEFAULT]` | OQ |
|---|---|---|---|
| EC-07 | deep-link route เปลี่ยน/ยังไม่พร้อม | graceful notice/toast + คงหน้าเดิม (ไม่ค้าง) | OQ-ESS-03 |
| EC-08 | surface ต้นทาง down/timeout | per-card/surface degrade "โหลดไม่ได้" ไม่ล้มทั้งหน้า | OQ-ESS-04 |
| EC-09 | session หมดอายุกลาง drawer RESTRICTED | re-auth ก่อนอ่าน RESTRICTED | OQ-ESS-06 |
| EC-10 | employee_id ผ่าน param ตรงๆ | enforce self ที่ **server** (401/403) ไม่ใช่แค่ UI | OQ-ESS-05 |
| EC-11 | สลิป PDF ต้นทางยังไม่ออก | ปุ่มดาวน์โหลด disabled + เหตุผล | OQ (owner Payroll) |

---

## §5.6 Error Catalog

| Code | HTTP | เมื่อไหร่ | ข้อความผู้ใช้ (verbatim จอ) |
|---|---|---|---|
| ERR-403-SELF | 403 | เข้าถึงข้อมูลพนักงานคนอื่น (FN-10) | "เข้าถึงถูกปฏิเสธ" / "พนักงานเห็นได้เฉพาะข้อมูลของตนเอง" / "คุณ (<ชื่อ>) ไม่มีสิทธิ์เข้าถึงข้อมูลของพนักงานคนอื่น ระบบปิดบังและไม่แสดงข้อมูลนอกขอบเขตของคุณ" |
| ERR-404 | 404 | record ไม่มี (สลิป/surface) | (มาตรฐาน) |
| ERR-DEGRADED | 502/soft | surface/owner down | per-card "โหลดไม่ได้" (EC-08 · ไม่ throw ทั้งหน้า) |
| ERR-LINK-NA | soft | deep-link route ยังไม่พร้อม | graceful notice (EC-07) — ไม่โชว์ route/contract ดิบ |

> **Prototype note:** deep-link สำเร็จ = `showToast('กำลังนำทางไปหน้า "<label>"', 'info')` (stub · prod = navigate จริง · ไม่โชว์ route/contract ใน toast).

---

## §5.7 Security & Data Classification (D-CLASS · R10 · Bible P6)

**Preset:** P6 · HR / PII Sensitive (15 controls). **Domains:** D2 (Auth) · D7 (PII) · D9 (Audit) · D17 (Multi-tenant) · D-SelfAccess (SecC).

**Controls (จาก BRD §16):**
- ✓Must: **self-access enforcement ที่ server** (ไม่ใช่แค่ UI) · เข้าถึงคนอื่น = 403 (BR-06/FN-04/FN-10 · OQ-ESS-05)
- ✓Must: **masking personal/salary (RESTRICTED)** ตาม self (FN-05/VR-2)
- ✓Must: **audit อ่าน (append-only)** · แก้/ลบไม่ได้ (FN-07/BR-08)
- ✓Must: **ESS ไม่มี write path** → ลด attack surface (display-only by design · LK-1)
- ○Optional: re-auth ก่อนเปิด RESTRICTED (session · EC-09/OQ-ESS-06)

**D-CLASS enforcement:** ดู 04_DB §4.5. Restricted = national_id/bank/payslip money → mask+self ที่ backend. Default = Internal (ไม่มี Public).

### ⚠️ CSQ SecC self-access — **[ASSUMED · OQ-ESS-01]** (ห้าม invent event id)
> **conflict ที่ต้อง reconcile ก่อน dev wire:**
> - `CSQ_BRIEF_F059` (source of truth ประกาศ) → **`ess.self_access`** (พนักงานเปิดดูข้อมูลตัวเอง · ท่อ **SecC**)
> - `ess.html` anchors (comment ในโค้ด) → **`ess.restricted_view`** (เปิดดู RESTRICTED · L2534) + **`ess.access_denied`** (403 · L2657)
>
> **ต้องให้ PM/BA + ENG-CSQ owner ยืนยัน event id ปลายทางจริง** (1 ชื่อ หรือ 2–3 ชื่อ mapping กัน) ก่อน dev ผูก. **FRD ไม่ตัดสิน/ไม่ invent** — flag ทั้ง 03_LOGIC (FN-04/FN-07 emit) + 04_DB (`csq_event`) เป็น [ASSUMED]. ห้าม ESS ประกาศ OC/DC ซ้ำ (CSQ_BRIEF §ไม่ประกาศ) — ประกาศเฉพาะ self-access ของ portal.

### Declarations (NOTE only — **ไม่ generate ใน pack นี้**)
> ต่อคำสั่ง operator: FRD Pack เท่านั้น · **ไม่เรียก `*-declaration` skill · ไม่สร้าง DOA_/DOCCFG_/NTF_ brief**. บันทึกสถานะไว้เพื่อ traceability:
> - **ntf = need** (consume ENG-NOTIFY feed · FN-09 · ESS emits no events) — run แยกโดย operator ถ้าต้องการ
> - **csq = need** (SecC self-access · CSQ_BRIEF_F059 มีอยู่แล้ว · OQ-ESS-01 = event id)
> - **doa = no · doccfg = no · pdfdoc = no**
