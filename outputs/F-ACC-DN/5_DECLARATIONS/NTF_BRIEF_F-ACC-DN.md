# NTF_BRIEF — F-ACC-DN / F097 ใบลดหนี้ผู้ขาย (Debit Note)

> ยิงผ่าน **ENG-NOTIFY** (F-NOTIFY) เท่านั้น — feature **ประกาศ** event · ห้าม hardcode ช่องทาง/เงื่อนไขแจ้งเตือนในตัว feature
> **DOA events (`doa_pending` / `doa_result` / `doa_escalate`) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้ และห้ามประกาศซ้ำ** (submit/approve = สายอนุมัติของ ENG-DOA จาก DOA_BRIEF_F-ACC-DN)
> Source of truth: FRD_Pack/03_LOGIC (FN-15/16/12 · §3.3 trace) + 05_RULES (§5.2 state machine) · align กับ HTML `onFinalApprove` / `openSendDN`
> **Mirror ของ F-ACC-CN** ฝั่ง AR → re-domain เป็น AP/ผู้ขาย/ภาษีซื้อ

## §1 Identity
- feature: **F-ACC-DN / F097** · module: Accounting / AP · chip 🔔 Notify = ✓ (detect ✓ 3 events)
- event source แยก 2 ทาง: **(1) DOA engine** → doa_pending/doa_result (ไม่ประกาศ) · **(2) event ธุรกิจของ feature เอง** → ประกาศในตารางด้านล่าง

## §2 Declared Events (feature-owned)

| Event ID | (ชื่อลัด) | Trigger (อ้าง FRD) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|---|---|
| `ap_dn_approved_applied` | **dn.issued** | pending_approval → approved **ครบสาย** (ออกเลข DN) — 03_LOGIC FN-12 · 05_RULES BR-09 · §5.2 | ผู้สร้าง (เจ้าหน้าที่เจ้าหนี้/AP owner) + **ทีมเจ้าหนี้/AP** + ผู้จัดการจัดซื้อที่อ้าง | ใบลดหนี้ **{dn_no}** อนุมัติแล้ว — ลดหนี้ {api_no} ฿{grand} · ภาษีซื้อที่ลด ฿{net_vat} · คงค้างจ่ายใหม่ ฿{outstanding} · เครดิตคงเหลือ ฿{vendor_credit} | in-app | ✓ |
| `ap_dn_sent` | **dn.sent** | approved → sent (ส่งใบให้ผู้ขาย / sent→resend ไม่เปลี่ยน state) — 03_LOGIC FN-16 · §5.2 | ผู้ติดต่อผู้ขาย (external) + ผู้ส่ง (in-app echo) | ส่งใบลดหนี้ **{dn_no}** อ้างใบกำกับ {vendor_invoice_no} ยอด ฿{grand} ให้ {vendor} (แนบ PDF) | **ตาม preference ผู้ขาย / config กลาง** (ไม่ hardcode) | ✗ (transactional) |
| `ap_dn_cancelled` | dn.cancelled | draft/pending_approval → cancelled — 03_LOGIC FN-15 · §5.2 (คืนยอด held) | ผู้สร้าง (+ ผู้อนุมัติที่ค้างในสาย ถ้ายกเลิกตอน pending) | ใบลดหนี้ **{dn_no ‖ ร่าง}** ถูกยกเลิก: {reason} | in-app | ✓ |

> **dn.issued / dn.sent = 2 event หลักที่โจทย์ระบุ** · `ap_dn_cancelled` เพิ่มตามที่ FN-15 emit จริงใน FRD (state transition จริง) — ไม่ใช่การเดา
> **หมายเหตุ vendor credit (FN-20):** ข้อความ `dn.issued` เพิ่มตัวแปร `{vendor_credit}` (เครดิตคงเหลือกับผู้ขาย = ส่วนเกินหนี้ค้าง) — 0 เมื่อไม่มีส่วนเกิน

## §3 Events ที่ **ไม่** ประกาศ (มาจากที่อื่น — ประกาศซ้ำ = ชนกับ engine เจ้าของ)
| Event | เจ้าของ | เหตุผล |
|---|---|---|
| `doa_pending` | **ENG-DOA** | ยิงอัตโนมัติตอน submit (FN-11 emit ผ่าน DOA engine) |
| `doa_result` (approved/rejected step) | **ENG-DOA** | ผลรายขั้นของสายอนุมัติ = DOA engine · feature ยิงแค่ **business outcome** `ap_dn_approved_applied` ตอนครบสายเท่านั้น |
| `doa_escalate` | **ENG-DOA** | เลื่อนขั้น/เตือน SLA = DOA engine |

## §4 Payload Contract (ref + ตัวแปรในข้อความ — field มีจริงใน 04_DB)
- `ap_dn_approved_applied`: `dn_id`, `dn_no`, `api_no` (ref_ap_invoice), `vendor` (vendor_code/name — mask PII บุคคลธรรมดา), `grand`, `net_vat` (ภาษีซื้อที่ลด), `outstanding` (คงค้างจ่ายใหม่), `vendor_credit` (เครดิตคงเหลือ)
- `ap_dn_sent`: `dn_id`, `dn_no`, `api_no`, `vendor_invoice_no`, `vendor`, `grand`, `pdf_ref` (ENG-DOC-STORE)
- `ap_dn_cancelled`: `dn_id`, `dn_no ‖ 'ร่าง'`, `reason`, `actor`
- ทุก event มี `ref` (soft-reference → debit_note) — ไม่มี system broadcast

## §5 เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
- กลุ่ม **"เอกสารธุรกรรม"** → ใช้ doc_status pattern เดิม (approved/sent/cancelled) — ไม่ต้องเพิ่มกลุ่มใหม่
- `ap_dn_sent` เป็น outbound-to-vendor → ผูก channel resolver ของ F-NOTIFY (email/LINE ตาม vendor preference) · **feature ไม่เลือกช่องทางเอง**

## §6 Dev wiring note
- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref, vars })` ที่ transition จริง — **ห้ามเช็ค channel/preference เองใน feature**
  - `ap_dn_approved_applied` → FN-12 `issueDebitNote` (หลังออกเลข · API-06 final approve)
  - `ap_dn_sent` → FN-16 `sendToVendor` (API-09)
  - `ap_dn_cancelled` → FN-15 `cancelDebitNote` (API-08)
- ห้ามระบุ "ส่ง email/LINE" ใน logic feature · ข้อความ template อยู่ในใบนี้ ไม่ฝังใน code

## §7 Open Questions
- ไม่มี OQ เฉพาะของ NTF · ผู้รับ "ทีมเจ้าหนี้/AP group" อ้างอิงกลุ่มใน F-NOTIFY — ถ้ายังไม่มี group นี้ → BA/Notification Center ตั้ง (ผูก role officer-ap) **[ASSUMED — รอยืนยัน group id]**
