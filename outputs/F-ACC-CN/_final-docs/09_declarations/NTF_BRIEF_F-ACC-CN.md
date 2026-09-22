# NTF_BRIEF — F-ACC-CN / F096 ใบลดหนี้ลูกค้า (Credit Note)

> ยิงผ่าน **ENG-NOTIFY** (F-NOTIFY) เท่านั้น — feature **ประกาศ** event · ห้าม hardcode ช่องทาง/เงื่อนไขแจ้งเตือนในตัว feature
> **DOA events (`doa_pending` / `doa_result` / `doa_escalate`) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้ และห้ามประกาศซ้ำ** (submit/approve = สายอนุมัติของ ENG-DOA จาก DOA_BRIEF_F-ACC-CN)
> Source of truth: FRD_Pack/03_LOGIC (FN-09/10/11 · §3.3 trace) + 05_RULES (§5.2 state machine) · align กับ HTML `onFinalApprove` (FIX-05)

## §1 Identity
- feature: **F-ACC-CN / F096** · module: Accounting / AR · chip 🔔 Notify = ✓ (detect ✓)
- event source แยก 2 ทาง: **(1) DOA engine** → doa_pending/doa_result (ไม่ประกาศ) · **(2) event ธุรกิจของ feature เอง** → ประกาศในตารางด้านล่าง

## §2 Declared Events (feature-owned)

| Event ID | (ชื่อลัด) | Trigger (อ้าง FRD) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|---|---|
| `ar_cn_approved_applied` | **cn.issued** | pending_approval → approved **ครบสาย** (ออกเลข CN) — 03_LOGIC FN-11 step 7 · 05_RULES BR-09 · §5.2 | ผู้สร้าง (เจ้าหน้าที่ลูกหนี้ owner) + **ทีมลูกหนี้/AR** + พนักงานขายที่อ้าง | ใบลดหนี้ **{cn_no}** อนุมัติแล้ว — ลดหนี้ {inv_no} ฿{grand} · ภาษีขายที่ลด ฿{net_vat} · คงค้างใหม่ ฿{outstanding} | in-app | ✓ |
| `ar_cn_sent` | **cn.sent** | approved → sent (ส่งใบให้ลูกค้า / sent→resend ไม่เปลี่ยน state) — 03_LOGIC FN-10 · §5.2 | ผู้ติดต่อลูกค้า (external) + ผู้ส่ง (in-app echo) | ส่งใบลดหนี้ **{cn_no}** อ้างใบกำกับ {inv_no} ยอด ฿{grand} ให้ {customer} (แนบ PDF) | **ตาม preference ลูกค้า / config กลาง** (ไม่ hardcode) | ✗ (transactional) |
| `ar_cn_cancelled` | cn.cancelled | draft/pending_approval → cancelled — 03_LOGIC FN-09 · §5.2 (คืนยอด held) | ผู้สร้าง (+ ผู้อนุมัติที่ค้างในสาย ถ้ายกเลิกตอน pending) | ใบลดหนี้ **{cn_no ‖ ร่าง}** ถูกยกเลิก: {reason} | in-app | ✓ |

> **cn.issued / cn.sent = 2 event หลักที่โจทย์ระบุ** · `ar_cn_cancelled` เพิ่มตามที่ FN-09 emit จริงใน FRD (state transition จริง) — ไม่ใช่การเดา

## §3 Events ที่ **ไม่** ประกาศ (มาจากที่อื่น — ประกาศซ้ำ = ชนกับ engine เจ้าของ)
| Event | เจ้าของ | เหตุผล |
|---|---|---|
| `doa_pending` | **ENG-DOA** | ยิงอัตโนมัติตอน submit (FN-06 emit ผ่าน DOA engine — 03_LOGIC หมายเหตุ "ไม่ยิงเอง") |
| `doa_result` (approved/rejected step) | **ENG-DOA** | ผลรายขั้นของสายอนุมัติ = DOA engine · feature ยิงแค่ **business outcome** `ar_cn_approved_applied` ตอนครบสายเท่านั้น |
| `doa_escalate` | **ENG-DOA** | เลื่อนขั้น/เตือน SLA = DOA engine |

## §4 Payload Contract (ref + ตัวแปรในข้อความ — field มีจริงใน 04_DB)
- `ar_cn_approved_applied`: `cn_id`, `cn_no`, `inv_no` (ref_invoice), `customer` (customer_code/name — mask PII บุคคลธรรมดา), `grand`, `net_vat`, `outstanding` (คงค้างใหม่)
- `ar_cn_sent`: `cn_id`, `cn_no`, `inv_no`, `customer`, `grand`, `pdf_ref` (ENG-DOC-STORE)
- `ar_cn_cancelled`: `cn_id`, `cn_no ‖ 'ร่าง'`, `reason`, `actor`
- ทุก event มี `ref` (soft-reference → credit_note) — ไม่มี system broadcast

## §5 เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
- กลุ่ม **"เอกสารธุรกรรม"** → ใช้ doc_status pattern เดิม (approved/sent/cancelled) — ไม่ต้องเพิ่มกลุ่มใหม่
- `ar_cn_sent` เป็น outbound-to-customer → ผูก channel resolver ของ F-NOTIFY (email/LINE ตาม customer preference) · **feature ไม่เลือกช่องทางเอง**

## §6 Dev wiring note
- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref, vars })` ที่ transition จริง — **ห้ามเช็ค channel/preference เองใน feature**
  - `ar_cn_approved_applied` → FN-11 `issueCreditNote` (หลังออกเลข · API-06 final approve)
  - `ar_cn_sent` → FN-10 `sendToCustomer` (API-09)
  - `ar_cn_cancelled` → FN-09 `cancelCreditNote` (API-08)
- ห้ามระบุ "ส่ง email/LINE" ใน logic feature · ข้อความ template อยู่ในใบนี้ ไม่ฝังใน code

## §7 Open Questions
- ไม่มี OQ เฉพาะของ NTF · ผู้รับ "ทีมลูกหนี้/AR group" อ้างอิงกลุ่มใน F-NOTIFY — ถ้ายังไม่มี group นี้ → BA/Notification Center ตั้ง (ผูก role officer-ar) **[ASSUMED — รอยืนยัน group id]**
