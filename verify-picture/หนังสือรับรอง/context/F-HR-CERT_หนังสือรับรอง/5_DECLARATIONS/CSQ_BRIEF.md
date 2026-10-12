# CSQ_BRIEF — F-HR-CERT · Employment / Salary Certificate (หนังสือรับรอง)

> ออกโดย `csq-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-30
> Input: `briefs/W3/F-HR-CERT/PREBRIEF.md` v1.0 **§12 (authoritative)** + §5 state machine + §4 BR + §13 patch · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `csq ✓` = detect §12 = ตาราง `CONTEXT_PACK/HR.md` แถวหนังสือรับรอง → **✓ SecC**)
> หมายเหตุ: `references/csq-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (7 ท่อ · `kind` 3 ค่า · Envelope · Iron Rule · Quality Gate G1–G9) + `cube-4.0-current-state.md §3` + `feature-catalog-master.md §0` · ค่าที่เสนอเองติด `[DEFAULT — รอยืนยัน]`
> **feature ประกาศเท่านั้น — ห้ามคำนวณผลรายท่อ ห้ามตีมูลค่าเอง** · **ห้ามเก็บ column ผลรายท่อในตารางของ feature**

## §1 Identity

| | |
|---|---|
| profile_id | `CSQ-HRCERT` *(ตัวเลขลำดับจริงให้ Engine กำหนดตอน register)* `[DEFAULT — รอยืนยัน]` |
| feature_code | `F-HR-CERT` |
| feature name | Employment / Salary Certificate · หนังสือรับรอง |
| module | HR |
| กลุ่ม backfill | **B ล้วน** — *SecC on sensitive data disclosure* · ⭐ **ต่างจากพี่น้อง HR ทุกตัวตรงที่ feature นี้ไม่ได้ "เปลี่ยน" อะไรเลย** — มันแค่ **หยิบข้อมูลอ่อนไหวมาทำเป็นเอกสารแล้วส่งออกนอกองค์กร** |
| archetype | Q-document |
| version | 1.0 (2026-08-30) |
| ท่อที่ประกาศ | ⭐ **SecC เท่านั้น** — ไม่มี EC · FC · AC · DC (เหตุผลครบใน **§3**) |

## §2 Declared Events

> trigger point อ้าง **PREBRIEF §5 (state machine)** · **§4 (BR)** · **§2 (S-XX)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่)

| # | event_id | trigger point (PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|---|
| **E1** ⭐⭐ | `cert.issued` | §5 **T-06** `อนุมัติแล้ว → ออกแล้ว` (S-12 · **BR-03 · BR-23** · FN-35) — **หลัง render PDF + `ENG-DOC-STORE.store()` สำเร็จเท่านั้น** | **SecC** | ⭐ **จุดที่ข้อมูลบุคคลถูกตรึงเป็นเอกสารที่จะออกนอกองค์กร** — ข้อมูลตัวตน + ประวัติการจ้าง (**+ อัตราค่าจ้าง เมื่อ `has_salary_figure = true`**) ถูกรวมเป็นชิ้นเดียวพร้อมตราบริษัท · ตรงนิยาม "เปิดดู/เปิดเผยข้อมูลที่ปกปิด" ของท่อ SecC | `employee_id` · `cert_doc_no` · `company_id` · `cert_type` · **`has_salary_figure`** · `language` · `purpose_code` · `recipient_name` · `issue_date` · `issue_place` · `issued_by` · `requested_by` · **`on_behalf`** · **`consent_ack`** · `approval_action_id` · `approved_by` · `template_version_id` · `copies` · `delivery_method` · `employment_state` · `source_version_ids` (ก้อน `salary` · `movement` · `onboard` · `hr_config`) — ⛔ **ไม่มี `base_amount` และไม่มีตัวเลขเงินใด ๆ** |
| **E2** ⭐ | `cert.delivered_external` | §5 **T-07** `ออกแล้ว → ส่งมอบแล้ว` และ **T-12** ทุกครั้งที่ดาวน์โหลดซ้ำ (S-13 · S-33 · **BR-26** · FN-58) | **SecC** | ⭐ **จุดที่เอกสารออกจากมือองค์กรจริง** — E1 คือ "ทำเสร็จ" · E2 คือ "ออกไปแล้ว" · **แยกกันเพราะความเสี่ยงต่างกัน และดาวน์โหลดซ้ำได้หลายครั้งขณะที่ออกได้ครั้งเดียว** | `cert_doc_no` · `employee_id` · `company_id` · `has_salary_figure` · `delivery_method` · `delivered_to` (พนักงาน/ผู้ยื่นแทน) · `download_seq` (ครั้งที่) · `actor_id` · `delivered_at` — ⛔ **ไม่มีตัวเลขเงิน · ไม่มีอีเมลบุคคลที่สาม** (ระบบไม่ส่งออกนอกองค์กรเอง · S-40) |
| **E3** ⭐ | `cert.restricted_viewed` | §2 **S-33** · **BR-26** · FN-77 — มีการ **เปิดดูหรือดาวน์โหลดไฟล์ rendition ที่มีตัวเลขค่าจ้าง** (`salary_th` / `salary_en`) | **SecC** | การเปิดดูข้อมูลที่ปกติปกปิด · ⭐ **ไม่ซ้ำกับพี่น้อง 2 ตัวที่ประกาศไปแล้ว** — `salcomp.viewed_restricted` (`CSQ-HRSAL`) = เปิดดูที่ **หน้าจอโครงเงินเดือน** · `move.restricted_viewed` (`CSQ-HRMOVE`) = เปิดดูที่ **เอกสารคำสั่ง** · **ตัวนี้ = เปิดดู "เอกสารที่ออกไปข้างนอกแล้ว"** — คนละ surface คนละบริบทความเสี่ยง | `viewer_id` · `cert_doc_no` · `employee_id` · `company_id` · `view_surface` (`document` \| `pdf_salary`) · `rendition` · `viewed_at` — ⛔ **ไม่มีตัวเลขที่ถูกเปิดดู** |
| **E4** ⭐ | `cert.issue_blocked_masked` | §2 **S-22** · **BR-10** · FN-39 — ผู้ออกไม่มีสิทธิ์ RESTRICTED แต่พยายามออกหนังสือประเภทเงินเดือน (`masked = true`) | **SecC** | ⭐ **สัญญาณเชิงกำกับดูแลที่มีค่าที่สุดของ feature นี้** — ไม่ใช่ error แต่คือ **การพยายามเข้าถึงข้อมูลค่าจ้างของผู้ที่ไม่มีสิทธิ์** ที่ระบบปฏิเสธไว้ · ตระกูลเดียวกับ `salcomp.viewed_restricted` ที่ Salary Structure เปิดไว้ให้ใช้เชิงกำกับดูแล (`OQ-CSQ-01` ของ `CSQ-HRSAL`) | `actor_id` · `cert_doc_no` · `employee_id` · `company_id` · `cert_type` · `blocked_reason` (`MASKED` \| `NO_RATE_AT_DATE`) · `attempted_at` — ⛔ **ไม่มีตัวเลข** |
| **E5** | `cert.revoked` | §5 **T-08** `ออกแล้ว/ส่งมอบแล้ว → เพิกถอนแล้ว` (S-14 · **BR-22** · FN-67) | **SecC** | ⭐ **ความเสี่ยงที่ยังค้างอยู่ข้างนอก** — เอกสารถูกประกาศว่าใช้ไม่ได้ **แต่ฉบับจริงยังอยู่ในมือบุคคลภายนอก** · เป็นข้อมูลที่ฝ่ายกำกับต้องเห็น · **ห้ามลบ/แก้ event เดิม** — ส่ง **`reversal_of`** ชี้ E1 (BR-CSQ-04) | field ของ E1 (ยกเว้นที่ไม่จำเป็น) + **`reversal_of`** (ชี้ E1) · `revoke_reason` · `revoked_by` · `revoked_at` · `was_delivered` (bool) |

### §2.1 เหตุผลรายท่อ (ทำไม SecC และทำไมไม่ใช่ท่ออื่น)

**ทำไม SecC เป็นแกน:** ท่อ SecC ตามนิยามใน SKILL §Trigger Rule คือ *"แก้ข้อมูลอ่อนไหว / **เปิดดูข้อมูลที่ปกปิด** / เปลี่ยนสิทธิ์-นโยบาย"* — feature นี้ไม่ได้แก้อะไรและไม่ได้เปลี่ยนสิทธิ์ใคร **แต่มันคือกลไก "เปิดเผยข้อมูลที่ปกปิด" ที่ตั้งใจและเป็นทางการที่สุดในทั้งระบบ** ข้อมูล **PII + ค่าจ้าง (RESTRICTED)** ถูกพิมพ์ลงกระดาษที่มีตราบริษัท แล้วส่งไปอยู่ในมือธนาคาร/สถานทูต/นายจ้างใหม่ — **ถ้าท่อ SecC ไม่เห็นเส้นทางนี้ ระบบกำกับดูแลจะมองไม่เห็นช่องทางที่ข้อมูลค่าจ้างออกนอกองค์กรมากที่สุด**

**ทำไมแยก 5 event ไม่ใช่ event เดียว:** เพราะเป็น **5 ความเสี่ยงคนละแบบ** — สร้างเอกสาร (E1) · ส่งออกไป (E2) · เปิดดูตัวเลข (E3) · **พยายามเข้าถึงแล้วถูกปฏิเสธ (E4)** · เอกสารที่ออกไปแล้วใช้ไม่ได้แต่ยังอยู่ข้างนอก (E5) · การยุบรวมจะทำให้ **E4 หายไปทั้งตัว** ซึ่งเป็นสัญญาณเดียวที่บอกว่ามีคนพยายามเข้าถึงข้อมูลที่ไม่มีสิทธิ์

**การยื่นแทน (S-35) ไม่แยกเป็น event:** เป็น **ธง `on_behalf` + `consent_ack` บน E1/E2** — เพราะมันไม่ใช่เหตุการณ์ต่างหาก แต่เป็น **คุณสมบัติของการเปิดเผยครั้งนั้น** (ใครเป็นคนทำให้ข้อมูลออกไป และมีร่องรอยความยินยอมหรือไม่) · แยกเป็น event = **นับการเปิดเผยครั้งเดียวเป็นสองครั้ง**

**⛔ ไม่มีตัวเลขเงินในทุก payload (BR-CSQ-03):** ค่าจ้างเป็น **RESTRICTED** และ **Salary Structure เป็นเจ้าของชั้น masking** (`SS-5`) — ส่งตัวเลขเข้า Engine = **สร้างช่องทางอ้อมที่ `SS-5` ห้ามไว้ตรง ๆ** · สิ่งที่ส่งคือ **ธง `has_salary_figure`** (ข้อมูลนี้มีค่าจ้างอยู่ด้วยหรือไม่) ไม่ใช่ค่าจ้างเอง — **Engine ประเมินความอ่อนไหวจากธงได้โดยไม่ต้องรู้ตัวเลข**

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — ห้ามเงียบ

| ท่อ | ประกาศ? | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ **ห้าม** | มาจาก Operation Process (`sow.*`) อัตโนมัติ — feature นี้ **ไม่สร้างงาน OP เลยรอบนี้** (PREBRIEF §9 "รอบนี้ไม่ผูก") · ประกาศซ้ำ = **register reject 422** |
| **DC ระดับเอกสาร** (Decision) | ❌ **ห้าม** | **DOA engine เป็นเจ้าของ** — การอนุมัติ/ไม่อนุมัติคำขอหนังสือ **เป็นการเซ็นอนุมัติเอกสารล้วน ๆ ไม่ใช่ terminal decision แบบ Continue/Adjust/Hold/Stop** · ประกาศซ้ำ = **422** |
| **SC** | ❌ **ห้ามทุกกรณี** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) |
| **EC** (Economic) | ⬜ **ไม่เกี่ยว** | ⭐ **feature นี้ไม่ใช้ทรัพยากรที่ตีเป็นเงินได้ และไม่เปลี่ยนการจัดสรรกำลังคนเลย** — การออกหนังสือ 1 ฉบับไม่ทำให้ต้นทุนแรงงานของใครขยับ · หน่วยนับของ EC ในตระกูล HR ถูกจองไว้หมดแล้วโดย `CSQ-HRATT` (ชั่วโมงในกะ) · `CSQ-HROT` (ชั่วโมงนอกกะ) · `CSQ-HRLV` (วันลา) · `CSQ-HRMOVE` (หัว/FTE ที่เปลี่ยนหน่วยรับต้นทุน) — **ถ้าใบนี้ยิง EC จะเป็นการนับซ้ำโดยไม่มีหน่วยนับของตัวเอง** |
| **FC** (Financial) | ⬜ **ไม่เกี่ยว** | ⭐ **ไม่มีเงินไหลและไม่มีภาระผูกพันเกิดขึ้นจากใบนี้** — ตัวเลขค่าจ้างบนหนังสือเป็น **ข้อมูลที่ถูกรับรอง ไม่ใช่ยอดที่ถูกอนุมัติหรือผูกพัน** · การรับรองว่า "คนนี้ได้เงินเดือนเท่านี้" **ไม่ทำให้องค์กรผูกพันเพิ่มแม้แต่บาทเดียว** (ต่างจาก `CSQ-HRMOVE` E1 ที่การอนุมัติสร้างภาระผูกพันจริง) |
| **AC** (Accounting) | ⬜ **ไม่เกี่ยว** | ไม่สร้างรายการทางบัญชีใด ๆ — ไม่ตั้งหนี้ ไม่ตัดหนี้ ไม่ลงบัญชี · Payroll (⏳W4) เป็นผู้ลงบัญชีค่าจ้าง |
| **DC ที่ไม่ใช่การอนุมัติเอกสาร** | ⬜ **ไม่มี** | พิจารณาแล้ว: **การเพิกถอน (S-14)** และ **การออกใหม่แทน (S-15)** ไม่ใช่ terminal decision ของกระบวนการธุรกิจ แต่เป็น **การแก้ไขความผิดพลาดของเอกสาร** → ไม่เข้านิยาม DC · (ผลด้านความปลอดภัยของทั้งสองถูกจับด้วย **E5** ในท่อ SecC แล้ว) |

## §4 Payload Contract

| field | ชนิด | มาจาก entity | Classification / การ mask |
|---|---|---|---|
| `employee_id` · `company_id` | uuid | `employment_certificate` | **PII** — ส่ง id ไม่ส่งชื่อ (Engine join เองด้วยสิทธิ์ของตัวเอง) `[DEFAULT — รอยืนยัน]` |
| `cert_doc_no` | text | `employment_certificate` | Internal — เป็นกุญแจอ้างกลับ |
| `cert_type` · `language` · `purpose_code` | enum | `employment_certificate` | Internal |
| **`has_salary_figure`** | bool | `employment_certificate` (computed) | ⭐ **ธงแทนตัวเลข** — Engine ประเมินความอ่อนไหวจากธงนี้ |
| `recipient_name` | text | `employment_certificate` | **Confidential** — ชื่อหน่วยงานปลายทาง (บอกว่าข้อมูลไปที่ไหน · จำเป็นต่อการกำกับดูแล) |
| `on_behalf` · `consent_ack` | bool | `employment_certificate` | Internal — ใครทำให้ข้อมูลออกไป + มีร่องรอยความยินยอมไหม |
| `issued_by` · `requested_by` · `approved_by` · `viewer_id` · `actor_id` | uuid | `employment_certificate` / access log | **PII** — id เท่านั้น |
| `source_version_ids` | object | `employment_certificate` | Internal — ก้อนเวอร์ชัน 4 ต้นทาง (`SS-2` · `MV-3` · `OB-2` · `C-2`) ให้อธิบายย้อนหลังได้ |
| `download_seq` · `rendition` · `view_surface` | int · enum | access log | Internal |
| `blocked_reason` | enum | (runtime) | Internal — `MASKED` / `NO_RATE_AT_DATE` |
| **`base_amount` และตัวเลขเงินทุกชนิด** | — | — | ⛔ **ห้ามส่งเด็ดขาด** (BR-CSQ-03 · `SS-5`) |
| `idempotency_key` | text | envelope | `F-HR-CERT:{cert_doc_no}:{event}:{seq}` — unique ต่อ (feature, ref, action) (BR-CSQ-02) |

## §5 Register Checklist (ก่อน deploy จะ register สำเร็จ)

- [ ] ⭐ ตรวจว่า **ไม่มี event ใดประกาศ `oc` · `dc` · `sc`** — ทั้ง 5 event ประกาศ **`secc` ตัวเดียว** (ถ้าหลุด = **422**)
- [ ] Sync Read profile registry ของ F-CSQ-01 เพื่อกัน `event_id` ชน — โดยเฉพาะ **`cert.restricted_viewed` กับ `salcomp.viewed_restricted` และ `move.restricted_viewed`** (คนละ surface · ต้องไม่ถูกยุบรวม)
- [ ] ยืนยันว่า Engine รับ **`source_version_ids` เป็น object ที่มีคีย์ `null` ได้** — `hr_config.cert_policy` **เป็น `null` เสมอในรอบนี้** เพราะ HR Configuration ยังไม่เผยแพร่คีย์ (**`OQ-STD-CT3`**) · **คู่ขนานกับ `employment_term = null` ของ `F-HR-ONBOARD` (`OQ-STD-OB3`) และ `shift_rule = null` ของ `F-HR-ROSTER`**
- [ ] ยืนยันว่า Engine ยอมรับ event ที่เป็น **"การพยายามเข้าถึงที่ถูกปฏิเสธ" (E4)** ซึ่งไม่มี state transition รองรับ (**`OQ-CSQ-CT-A`**)
- [ ] map ทุกแถว §2 เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริงตอน S5 แล้ว **append ในไฟล์นี้**
- [ ] ตรวจโค้ด: ไม่มี column `is_secc_triggered` หรือคล้ายกันในตารางของ feature · ไม่มี `const PIPES_HIT = [...]` ใน HTML

## §6 Open Questions

| id | คำถาม | default | ใครตอบ |
|---|---|---|---|
| **`OQ-CSQ-CT-A`** | Engine รับ event ที่เป็น "การพยายามเข้าถึงที่ถูกปฏิเสธ" (E4) ได้ไหม (ไม่มี state transition รองรับ) | **ประกาศไว้** — ถ้า Engine ไม่รับ ให้ลงเป็น audit log ของ Policy Center แทน **แต่ห้ามตัดทิ้งเงียบ** | Architect (ENG-CSQ) |
| **`OQ-CSQ-CT-B`** | `recipient_name` (ชื่อหน่วยงานปลายทาง) ควรอยู่ใน payload ไหม — เป็นข้อมูล Confidential | **ส่ง** — เพราะ "ข้อมูลไปที่ไหน" คือหัวใจของการกำกับดูแลการเปิดเผยข้อมูล | DPO / Strike |
| **`OQ-CSQ-CT-C`** | E2 ยิงทุกครั้งที่ดาวน์โหลดซ้ำ หรือยิงครั้งแรกครั้งเดียว | **ทุกครั้ง** (มี `download_seq`) — การดาวน์โหลดซ้ำหลายครั้งเป็นสัญญาณที่มีความหมาย | Architect (ENG-CSQ) |
| **`OQ-CSQ-CT-D`** | ต้องยิง SecC เมื่อออกหนังสือประเภท **ไม่มีตัวเลขค่าจ้าง** ด้วยหรือไม่ | **ยิง** (E1 ยิงทุกใบ · แยกด้วยธง `has_salary_figure`) — เพราะ **PII + ประวัติการจ้างก็เป็นข้อมูลที่ออกนอกองค์กร** ไม่ใช่แค่ค่าจ้าง | DPO |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ไม่มี event ประกาศ `oc` | ✅ |
| G2 | ไม่มี event ประกาศ `dc` เพราะการอนุมัติ | ✅ ระบุเหตุผลใน §3 |
| G3 | ไม่มี event ประกาศ `sc` | ✅ |
| G4 | ทุก event มี trigger point อ้างได้จริง | ✅ T-06 · T-07/T-12 · S-33 · S-22 · T-08 |
| G5 | ทุก payload field มีจริงใน entity | ✅ ผูกกับ `PREBRIEF §3.1` ทุก field · **ข้อผูกพัน**: ยืนยันซ้ำกับ `04_DB` ตอน S5 |
| G6 | event ที่ยิง EC ระบุ `kind` ครบ | ✅ **N/A — ไม่มี event ที่ยิง EC** |
| G7 | EC จากเวลา/แรงงานที่ยังไม่มี Rate Card ระบุ `basis: declared` | ✅ **N/A** · แต่หลักการเดียวกันถูกใช้: **ส่งธงไม่ส่งตัวเลข** |
| G8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ `profile_id` · การส่ง id แทนชื่อ |
| G9 | `event_id` ไม่ชนความหมายกับ catalog เดิม | ⚠️ **ต้อง Sync Read** — โดยเฉพาะตระกูล `*_restricted_viewed` (ระบุใน §5) |

**Verdict: PASS** — 5 event · **ท่อ SecC ท่อเดียว** · ไม่แตะท่อต้องห้ามทั้งสาม
