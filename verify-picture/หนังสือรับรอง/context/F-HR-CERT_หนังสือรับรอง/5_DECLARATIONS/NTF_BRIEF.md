# NTF_BRIEF — F-HR-CERT · Employment / Salary Certificate (หนังสือรับรอง)

> ออกโดย `ntf-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-30
> Input: `briefs/W3/F-HR-CERT/PREBRIEF.md` v1.0 **§12 (authoritative)** + §5 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `ntf ✓` = detect §12 `need` = `CONTEXT_PACK/HR.md` แถวหนังสือรับรอง → ✓ **"ออกแล้ว/พร้อมรับ"**)
> **ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature** · ⭐ **DOA events (`doa_pending` · `doa_result` · `doa_escalate`) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้ ประกาศซ้ำ = BLOCK**
> หมายเหตุ: **event catalog ปัจจุบันของ F-NOTIFY (`f-notify.html` → `EVENT_GROUPS`) ไม่มีในเวิร์กสเปซนี้** → ต้อง **Sync Read ก่อน register เพื่อกันชื่อชน/ความหมายซ้อน** · ค่า channel default ติด `[ASSUMED]` ตาม ENG-NOTIFY default (in-app + email)

## §1 Event ธุรกิจที่ feature นี้ประกาศ (7 event)

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `cert_requested` | §5 **T-02** `ร่าง → รออนุมัติ` (S-08 · FN-23) | **ผู้อนุมัติในสายที่ resolve ได้** + HR ที่ดูแลทะเบียน · (ถ้ายื่นแทน) **พนักงานเจ้าของหนังสือ** ด้วย | คำขอหนังสือรับรอง **{cert_doc_no}** ของ {employee_name} ({cert_type_label} · {language_label}) รอการอนุมัติ | in-app | ✓ |
| `cert_approved` | §5 **T-05** `รออนุมัติ → อนุมัติแล้ว` (S-09 · FN-60) | **ผู้ขอ** + **ผู้ยื่นแทน** (ถ้ามี) + HR ผู้ออกหนังสือ | คำขอ **{cert_doc_no}** ได้รับอนุมัติแล้ว — อยู่ระหว่างจัดทำหนังสือ | in-app + email `[ASSUMED]` | ✓ |
| `cert_rejected` | §5 **T-03** `รออนุมัติ → ไม่อนุมัติ` (S-10 · FN-31 · FN-60) | **ผู้ขอ** + ผู้ยื่นแทน | คำขอ **{cert_doc_no}** ไม่ได้รับอนุมัติ — เหตุผล: {reject_reason} | in-app + email `[ASSUMED]` | ✗ **บังคับ** |
| **`cert_issued`** ⭐ | §5 **T-06** `อนุมัติแล้ว → ออกแล้ว` (S-12 · FN-59) — **หลัง render PDF และเก็บสำเนาสำเร็จแล้วเท่านั้น** | **ผู้ขอ** + ผู้ยื่นแทน | หนังสือรับรอง **{cert_doc_no}** ออกแล้ว ({cert_type_label} · {language_label}) ลงวันที่ {issue_date} | in-app + email `[ASSUMED]` | ✗ **บังคับ** |
| **`cert_ready_for_pickup`** ⭐ | §5 **T-06** เมื่อ `delivery_method = รับที่ HR` (S-12 · S-13 · FN-59) | **ผู้ขอ** | หนังสือรับรอง **{cert_doc_no}** พร้อมให้รับที่ฝ่ายบุคคล ({issue_place}) | in-app + email `[ASSUMED]` | ✓ |
| `cert_revoked` | §5 **T-08** `ออกแล้ว/ส่งมอบแล้ว → เพิกถอนแล้ว` (S-14 · FN-67) | **ผู้ขอ** + ผู้ยื่นแทน + HR ผู้ดูแลทะเบียน | หนังสือรับรอง **{cert_doc_no}** ถูกเพิกถอน — เหตุผล: {revoke_reason} · กรุณาอย่าใช้ฉบับดังกล่าวต่อไป | in-app + email `[ASSUMED]` | ✗ **บังคับ** |
| `cert_pending_issue_overdue` | §5 **T-10** (นาฬิกา) ใบ "อนุมัติแล้ว" ค้างเกิน **3 วันทำการ** `[AI-DRAFT]` (S-16 · FN-62 · `OQ-CT-10`) | **HR ผู้ออกหนังสือ** (ไม่ส่งถึงพนักงาน) | คำขอ **{cert_doc_no}** อนุมัติแล้วแต่ยังไม่ได้ออกหนังสือ ({days_pending} วันทำการ) | in-app | ✓ |

**event ที่พิจารณาแล้ว "ไม่ประกาศ" (เขียนไว้ไม่ให้ตกหล่นเงียบ):**

| ไม่ประกาศ | เหตุผล |
|---|---|
| `doa_pending` · `doa_result` · `doa_escalate` | ⭐ **DOA engine ยิงเอง** — ประกาศซ้ำ = BLOCK (Iron rule ของ skill) · `cert_approved`/`cert_rejected` ในใบนี้เป็น **event ธุรกิจของเอกสาร** (ผู้รับคือผู้ขอ/พนักงาน) คนละตัวกับ `doa_result` (ผู้รับคือคนในสายอนุมัติ) — ⚠️ ตอน Sync Read กับ F-NOTIFY ต้องตรวจว่าไม่ทับซ้อนจนพนักงานได้ 2 ใบเรื่องเดียวกัน (**`OQ-NTF-CT-A`**) |
| `cert_delivered` (ดาวน์โหลด/รับของแล้ว) | **ไม่ต้องแจ้งใคร** — ผู้ที่ดาวน์โหลดคือผู้รับเอง · การบันทึกร่องรอยเป็นเรื่องของ audit + ท่อ SecC (`CSQ_BRIEF §2`) ไม่ใช่การแจ้งเตือน |
| `cert_superseded` (ถูกแทนที่) | ผู้ขอได้รับ **`cert_issued` ของฉบับใหม่** อยู่แล้ว ซึ่งมีข้อความอ้างว่าแทนฉบับใด — เพิ่มอีก event = แจ้งซ้ำเรื่องเดียวกัน `[ASSUMED]` |
| `cert_upstream_changed` (ข้อมูลต้นทางเปลี่ยนหลังออก · S-28) | ⭐ **เป็นธงบนทะเบียนให้ HR เห็น ไม่ใช่การแจ้งเตือนพนักงาน** — แจ้งพนักงานว่า "ข้อมูลหลังบ้านเปลี่ยน" ทั้งที่หนังสือยังใช้ได้ จะสร้างความสับสนโดยไม่จำเป็น · ถ้า HR ตัดสินใจเพิกถอน พนักงานจะได้ `cert_revoked` (**`OQ-NTF-CT-B`**) |
| แจ้งเตือนหนังสือ "ใกล้หมดอายุ" | **ไม่มีนโยบายอายุใช้งานในระบบรอบนี้** — คีย์ `cert_policy` ยังไม่เผยแพร่จาก HR Configuration (**`OQ-STD-CT3`**) · **ห้ามเดาจำนวนวันแล้วตั้งตัวเตือน** |
| แจ้งเตือนถึง **บุคคลที่สาม** (ธนาคาร/สถานทูต) | **"ไม่รองรับ"** (S-40 · `OQ-STD-CT7`) — ระบบไม่ส่งอะไรออกนอกองค์กรเอง |

## §2 กติกาการยิง (Dev wiring note)

- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref: cert_id, vars: {...} })` **ที่ transition ตาม trigger เท่านั้น** — **ห้ามเช็ค preference/ช่องทางเองใน feature**
- ⭐ **`cert_issued` และ `cert_ready_for_pickup` ยิง "หลัง" render PDF + `ENG-DOC-STORE.store()` สำเร็จเท่านั้น** — ยิงก่อนแล้ว render ล้ม = พนักงานได้ข่าวที่ไม่จริง (แพทเทิร์นเดียวกับ `F-HR-MOVE` "ยิงหลังการเรียกปลายทางสำเร็จ")
- ทุก event มี `ref` = `cert_id` (soft reference) + `{cert_doc_no}` ในข้อความ (**ตัวหนาที่เลขเอกสารเสมอ**)
- ⭐ **ห้ามใส่จำนวนเงินหรืออัตราค่าจ้างลงใน `vars` หรือข้อความแจ้งเตือนเด็ดขาด** — แจ้งเตือนวิ่งไปหลายช่องทาง (in-app · email · LINE) และ **ไม่มีชั้น masking ของตัวเอง** · ใช้ได้แค่ `{cert_type_label}` ("รับรองเงินเดือน") ซึ่งเป็น **ชื่อประเภท ไม่ใช่ตัวเลข** (`SS-5` · PREBRIEF BR-10 · **`CSQ_BRIEF §2`**)
- `{employee_name}` ปรากฏได้เฉพาะใน event ที่ส่งถึง **HR/ผู้อนุมัติ** (`cert_requested` · `cert_pending_issue_overdue`) — event ที่ส่งถึงผู้ขอไม่ต้องมี เพราะผู้ขอรู้อยู่แล้วว่าเป็นของตัวเอง
- ข้อความ template อยู่ในใบประกาศนี้ **ไม่ฝังใน code ของ feature**

## §3 เพิ่มเข้า Event Catalog (F-NOTIFY `EVENT_GROUPS`)

- กลุ่ม **"เอกสารธุรกรรม"** (`doc_status` เดิม) — `cert_requested` · `cert_approved` · `cert_rejected` · `cert_issued` · `cert_revoked` **ใช้กลุ่มเดิม ไม่เพิ่มกลุ่มใหม่** (ตระกูลเดียวกับ `lv_*` · `ot_*` · `move_*`)
- กลุ่ม **"เตือนงานค้าง"** — `cert_pending_issue_overdue` (ถ้ากลุ่มนี้ยังไม่มี ให้ใช้กลุ่มเอกสารธุรกรรมไปก่อน `[ASSUMED]`)
- `cert_ready_for_pickup` เป็น **event เฉพาะของ HR ที่ยังไม่มีใน catalog** → ⚠️ **Sync Read `f-notify.html` ก่อน register** เผื่อมี event ความหมายซ้อนอยู่แล้ว

## §4 Open Questions

| id | คำถาม | default | ใครตอบ |
|---|---|---|---|
| **`OQ-NTF-CT-A`** | `cert_approved` / `cert_rejected` ทับซ้อนกับ `doa_result` ที่ engine ยิงเองหรือไม่ (ผู้ขออาจได้ 2 ใบ) | **ประกาศไว้** เพราะผู้รับต่างกลุ่มกัน (ผู้ขอ vs คนในสาย) · ถ้า Sync Read แล้วพบว่าทับ → **ตัดของเราออก ใช้ของ engine** | Chin (ENG-NOTIFY) |
| **`OQ-NTF-CT-B`** | ต้องแจ้งพนักงานไหมเมื่อข้อมูลต้นทางเปลี่ยนหลังหนังสือออกไปแล้ว (S-28) | **ไม่แจ้ง** — เป็นธงให้ HR ตัดสินใจก่อน | Strike / BA |
| **`OQ-NTF-CT-C`** | ช่องทาง email สำหรับ **อดีตพนักงาน** (S-43) ใช้อีเมลส่วนตัวที่บันทึกไว้ได้หรือไม่ (บัญชีบริษัทถูก revoke แล้วโดย On/Offboard) | **ใช้อีเมลที่บันทึกไว้ใน Employee Master ได้** `[ASSUMED]` · ถ้าไม่มี → บังคับช่องทาง "รับที่ HR" | Strike / DPO |
| **`OQ-NTF-CT-D`** | จำนวนวันของ `cert_pending_issue_overdue` | **3 วันทำการ** `[AI-DRAFT]` (`OQ-CT-10`) — **ไม่ใช่ค่ากฎหมาย จึงตั้ง default ได้** แต่ควรย้ายไป `cert_policy` เมื่อ HR Configuration เผยแพร่ | BA |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| N1 | ไม่ประกาศ `doa_*` ซ้ำ | ✅ ประกาศชัดเจนว่าไม่ประกาศ + ตั้ง `OQ-NTF-CT-A` กันทับซ้อน |
| N2 | ทุก event มี `ref` | ✅ `cert_id` ทุกตัว |
| N3 | ทุก event มี trigger ที่ผูก transition จริง | ✅ T-02 · T-03 · T-05 · T-06 · T-08 · T-10 |
| N4 | ไม่ระบุ "ส่ง email/LINE" ใน logic ของ feature | ✅ channel เป็น default ที่ user preference ทับได้ |
| N5 | ข้อความ template อยู่ในใบนี้ ไม่ฝังในโค้ด | ✅ |
| N6 | ⭐ ไม่มีข้อมูล RESTRICTED ในข้อความ/`vars` | ✅ **ห้ามใส่ตัวเลขค่าจ้าง** ระบุเป็นข้อห้ามใน §2 |
| N7 | event ที่ตัดออกมีเหตุผลเขียนไว้ | ✅ 6 รายการใน §1 |

**Verdict: PASS** — 7 event ธุรกิจ พร้อม wire เข้า ENG-NOTIFY (Sync Read `f-notify.html` ก่อน register)
