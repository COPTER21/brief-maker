# NTF_BRIEF — F-HR-RECRUIT (F127) · สรรหา / Recruit

> ยิงผ่าน **ENG-NOTIFY** (F-NOTIFY Notification Center) เท่านั้น — feature **ประกาศ event** อย่างเดียว
> ห้าม hardcode ช่องทาง (in-app/email/LINE) หรือเงื่อนไข preference ใน logic ของ feature
> **DOA events มาอัตโนมัติ ไม่อยู่ในใบนี้** (ดู §DOA ด้านล่าง)
> Sync Read event catalog: `Related context/f-notify/f-notify.html → EVENT_GROUPS` (ตรวจแล้ว ไม่มีชื่อชน)

---

## §1 Business Events ของ feature (ต้องประกาศ)

| Event ID | Trigger (อ้าง FRD §) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `recruit_interview_scheduled` | `scheduleInterview` — INSERT interview + snapshot ผู้สัมภาษณ์ (03_LOGIC §3.1 FN-13 · API-15) · pipeline applied→screening→interview (05_RULES §5.2 Candidate) | ผู้สัมภาษณ์ (interviewer snapshot) + ผู้สมัคร (candidate) | นัดสัมภาษณ์ผู้สมัคร **{candidate}** ตำแหน่ง **{position}** วันที่ {scheduled_at}{ · สถานที่ {location}} | in-app+email | ✗ บังคับ |
| `recruit_stage_changed` | `moveCandidateStage` — UPDATE stage + audit (03_LOGIC §3.1 FN-12 · API-14) · transition pipeline (05_RULES §5.2 Candidate) | HR สรรหา (recruiter) + hiring manager | ผู้สมัคร **{candidate}** ตำแหน่ง **{position}** → สถานะ **{stage}** | in-app | ✓ |
| `recruit_offer_sent` | `sendOffer` — offer approved→sent (03_LOGIC §3.1 FN-18a · API-20) · Offer approved→sent (05_RULES §5.2 Offer · BR-04) | ผู้สมัคร (candidate) | คุณได้รับข้อเสนอจ้างงาน **{offer_ref}** ตำแหน่ง **{position}** — โปรดตอบรับ/ปฏิเสธ | in-app+email | ✗ บังคับ |
| `recruit_offer_result` | `respondOffer` — UPDATE offer accepted/declined (03_LOGIC §3.1 FN-18 · API-21) · Offer sent→accepted/declined (05_RULES §5.2 Offer) | HR สรรหา (recruiter) + hiring manager | ผู้สมัคร **{candidate}** ตำแหน่ง **{position}** **{ตอบรับ/ปฏิเสธ}** ข้อเสนอ **{offer_ref}** | in-app | ✗ บังคับ |

**ref (soft-reference) ต่อ event:**
- `recruit_interview_scheduled` · `recruit_stage_changed` · `recruit_offer_result` → `ref = candidate_id`
- `recruit_offer_sent` → `ref = candidate_id` (ผูก offer ผ่าน candidate · offer เป็น sub-entity)
- vars ในข้อความ = `{candidate}` (mask ตาม role · BR-06/FN-23), `{position}`, `{stage}`, `{scheduled_at}`, `{location}` (optional), `{offer_ref}`

> **หมายเหตุ masking (D7/BR-06):** `{candidate}` ในข้อความต้องผ่าน `maskCandidatePII` ตาม role ผู้รับก่อนแสดง — recruiter unmask · manager/viewer mask. ตัว emit ส่ง `candidate_id` ให้ ENG-NOTIFY render ตาม ACL ผู้รับ (feature ไม่ตัดสิน mask เอง)

---

## §2 DOA events — มาอัตโนมัติ **ห้ามประกาศซ้ำ** (Iron rule)

feature นี้มีอนุมัติ 2 สาย ที่วิ่งผ่าน DOA engine (Policy Center · `resolveDoaChain` FN-26):
- **อนุมัติเปิดอัตรา (req):** `submitRequisitionApproval` (FN-03) → `approveApprovalStep` (FN-04) — 03_LOGIC §3.1 · 05_RULES §5.2 Requisition (BR-01)
- **อนุมัติข้อเสนอ (offer):** `submitOfferApproval` (FN-16) → `approveApprovalStep(offer)` (FN-17=FN-04) — 05_RULES §5.2 Offer (BR-04)

→ `doa_pending` / `doa_result` / `doa_escalate` **DOA engine เป็นเจ้าของ ยิงเองอัตโนมัติ**
**ประกาศซ้ำในใบนี้ = BLOCK** จึง **ตัดออก** ทั้ง 3 ตัว (มีอยู่แล้วในกลุ่ม "การอนุมัติ (DOA)" ของ EVENT_GROUPS)

---

## §3 เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

ตรวจ collision กับ catalog ปัจจุบันแล้ว — **ไม่มีชื่อชน / ไม่มีความหมายซ้อนกับ event เดิม**:

| Event เดิมที่พิจารณา reuse | ผล |
|---|---|
| `doc_status` (เอกสารธุรกรรม: SO/GRN/INV) | **ไม่ reuse** — คนละ domain (candidate pipeline HR ≠ transaction document) · ผู้รับ/ข้อความคนละชุด |
| `mention` (comment/มอบหมาย) | **ไม่ reuse** — recruit event ผูก state transition ไม่ใช่ mention |
| `doa_*` | **ไม่ประกาศ** — DOA engine เจ้าของ (§2) |

**เพิ่มกลุ่มใหม่ใน EVENT_GROUPS** (dev เพิ่มตอน register F-NOTIFY):

```js
{ g: 'สรรหา (Recruit)', rows: [
  { id: 'recruit_interview_scheduled', name: 'นัดสัมภาษณ์ผู้สมัคร',      sub: 'มีการนัดสัมภาษณ์ที่คุณเกี่ยวข้อง', lockApp: true },   // ปิดไม่ได้
  { id: 'recruit_stage_changed',       name: 'ผู้สมัครเลื่อนสถานะ',       sub: 'candidate เลื่อนขั้นใน pipeline' },                    // ปิดได้
  { id: 'recruit_offer_sent',          name: 'ส่งข้อเสนอจ้างงานถึงผู้สมัคร', sub: 'offer ถูกส่งให้ผู้สมัคร', lockApp: true },            // ปิดไม่ได้
  { id: 'recruit_offer_result',        name: 'ผลตอบรับข้อเสนอ',           sub: 'ผู้สมัครตอบรับ / ปฏิเสธข้อเสนอ', lockApp: true },       // ปิดไม่ได้
]},
```

- `lockApp: true` = event บังคับ ปิดไม่ได้ (ตรงคอลัมน์ "ปิดได้ = ✗") — `recruit_stage_changed` เท่านั้นที่ปิดได้
- default email (PREFS): เปิด email สำหรับ event สำคัญที่ส่งถึงบุคคลภายนอก/ผู้สมัคร → `recruit_interview_scheduled`, `recruit_offer_sent` (สอด: catalog ตั้ง email=true เฉพาะ doa/system เดิม — dev เพิ่ม 2 id นี้เข้า allow-list email default)

---

## §4 Dev wiring note

- **จุดเรียก:** `ENG-NOTIFY.emit(event_id, { ref, vars })` ที่ transition ตาม trigger — **feature ห้ามเช็ค preference/channel เอง** (ENG-NOTIFY อ่าน PREFS ต่อ user × channel เอง)

| Function (03_LOGIC §3.1) | บรรทัด emit |
|---|---|
| `scheduleInterview` (FN-13) | `ENG-NOTIFY.emit('recruit_interview_scheduled', { ref: candidate_id, vars: { candidate, position, scheduled_at, location } })` |
| `moveCandidateStage` (FN-12) | `ENG-NOTIFY.emit('recruit_stage_changed', { ref: candidate_id, vars: { candidate, position, stage } })` |
| `sendOffer` (FN-18a) | `ENG-NOTIFY.emit('recruit_offer_sent', { ref: candidate_id, vars: { candidate, position, offer_ref } })` |
| `respondOffer` (FN-18) | `ENG-NOTIFY.emit('recruit_offer_result', { ref: candidate_id, vars: { candidate, position, offer_ref, decision } })` |

- **emit หลัง commit transition สำเร็จ** (side-effect ต่อจาก UPDATE/INSERT + appendAudit) — ยิง notify **ไม่บล็อก** business transition
- **NTF ล้มเหลว → queue/retry ที่ ENG-NOTIFY** (05_RULES §5.5 EC-10 · OQ-D4) — feature ไม่ try/catch เพื่อ rollback business
- **แยกจาก handoff event:** `recruit.candidate.hired` (FN-19 hireCandidate · BR-05 · LOCK-OB1) = **outbound integration contract ไป On/Offboard** (fire-and-forget) **ไม่ใช่ notification** — ไม่ประกาศในใบนี้ (อยู่ 02_API outbound event · OQ-15 ฝั่งรับยังไม่ออกแบบ)

---

## §5 Iron rule self-check

- [x] ไม่ประกาศ `doa_pending`/`doa_result`/`doa_escalate` ซ้ำ — ตัดออกชัดเจน (§2)
- [x] ไม่ระบุ "ส่ง email/LINE" ใน logic feature — channel = user preference + config กลาง (§4)
- [x] ข้อความ template อยู่ในใบประกาศ ไม่ฝัง code feature (§1)
- [x] ทุก event มี `ref` (candidate_id) — soft-reference ครบ 4/4 (§1)
- [x] ทุก event ผูก trigger = state transition จริง อ้าง 03_LOGIC §3.1 + 05_RULES §5.2 (ไม่ fabricate §)
- [x] naming snake_case `recruit_<event>` · ตรวจ collision catalog แล้ว ไม่ชน
