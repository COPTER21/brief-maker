# NTF_BRIEF — F-HR-PAYROLL · Payroll (เงินเดือน)

> ออกโดย `ntf-declaration` · **Lane Mode** · S1.8 · 2026-08-30
> Input: `briefs/W4/F-HR-PAYROLL/PREBRIEF.md` §5 (transition) · §2 (S-XX) · §12 (**authoritative**) · `STANDARD_GAP.md` G-04
> **ประกาศ event ธุรกิจเท่านั้น — ไม่ implement** · การส่งจริงเป็นของ **ENG-NOTIFY** · **ห้ามประกาศซ้ำ `doa_pending` / `doa_result`** (DOA engine ยิงเอง)

## §1 Identity

| | |
|---|---|
| feature | `F-HR-PAYROLL` — Payroll · เงินเดือน |
| จำนวน event ที่ประกาศ | **7** (`E1`…`E7`) |
| ช่องทางตั้งต้น | **in-app + email** (ตาม ENG-NOTIFY default) `[ASSUMED]` |
| ⭐ กติกาความลับ | **การแจ้งเตือนทุกตัวส่งเป็น "ลิงก์เข้าระบบ" ไม่แนบไฟล์และไม่ใส่จำนวนเงินในเนื้อข้อความ** (`[ASSUMED A-4]` · RESTRICTED สูงสุดในโมดูล) |
| event ที่ถึง **พนักงานรายคน** | `E4` (สลิปพร้อม) และ `E7` (รอบถูกกลับรายการ) — สองตัวนี้เท่านั้น |

## §2 Declared Events (7 ตัว)

> trigger point อ้าง **PREBRIEF §5 (state machine)** · **§4 (BR)** · **§2 (S-XX)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่)

| # | event_id | trigger point (PREBRIEF) | ผู้รับ | เนื้อหา (ห้ามมีจำนวนเงิน) |
|---|---|---|---|---|
| **E1** | `payroll.inputs_not_settled` | §2 **S-07 · S-08 · S-09** — หลัง T-02 ดึงข้อมูลแล้วพบธง "ยอดยังไม่นิ่ง" ของต้นทางใดต้นทางหนึ่ง (FN-15) | **HR Payroll Officer** ของรอบ · (`[AI-DRAFT]` ผู้ดูแลของ feature ต้นทางนั้น) | รอบไหน · ต้นทางไหน · ติดกี่คน/กี่วัน/กี่ใบ · **ลิงก์ไปหน้าต้นทาง** |
| **E2** ⭐ | `payroll.blocked_missing_legal_config` | §2 **S-22 · S-23 · S-24** — หลัง T-03 คำนวณแล้วยังมีบรรทัด `ยังคำนวณไม่ได้` (FN-36 · **BR-15**) | **HR Payroll Officer** · **ผู้ดูแล HR Configuration** · Comp Admin | รอบไหน · **กลุ่มค่าที่ยังไม่มี (ประกันสังคม / ภาษี / กองทุนสำรองฯ / ฐานการแปลง / นโยบายหัก / เกณฑ์ทบทวน)** · จำนวนบรรทัดและจำนวนคนที่ติด · **ลิงก์ไปหน้า HR Configuration** — ⭐ **event นี้คือเสียงของกลไก fail-closed · ทำให้ปัญหาค่าที่หายไปไม่เงียบ** |
| **E3** | `payroll.run_closed` | §5 **T-11** รอบเข้า "ปิดรอบแล้ว" (S-38 · FN-54) | **HR Payroll Officer** · Comp Admin · **Finance** · ผู้อนุมัติทุกขั้นของรอบนั้น | รอบไหน · งวดไหน · จำนวนคน · **วันจ่าย** · ลิงก์ไปหน้ารอบ |
| **E4** ⭐ | `payroll.payslip_available` | §5 **P-02** — สลิปถูกเผยแพร่หลัง T-11 (S-38 · S-42 · FN-67) | ⭐ **พนักงานเจ้าของสลิป รายคน** | "สลิปเงินเดือนงวด &lt;งวด&gt; ของคุณพร้อมให้ดูแล้ว" + **ลิงก์เข้าระบบ** — ⛔ **ไม่แนบไฟล์ ไม่มีตัวเลขใด ๆ ในอีเมล** (RESTRICTED · BR-37) |
| **E5** | `payroll.bank_file_ready` | §2 **S-40** — ออกไฟล์โอนธนาคารสำเร็จ (FN-69) | **Finance** · HR Payroll Officer | รอบไหน · ธนาคารไหน · จำนวนรายการ · **จำนวนคนที่ต้องจ่ายด้วยวิธีอื่น (ไม่มีเลขบัญชี)** · ลิงก์ดาวน์โหลด (การดาวน์โหลดถูกบันทึกเป็น SecC) |
| **E6** `[AI-DRAFT]` | `payroll.pay_date_approaching` | `STANDARD_GAP.md` **G-04** — ใกล้ถึงวันจ่ายของงวดแต่รอบยังไม่ถึงสถานะ "ปิดรอบแล้ว" | **HR Payroll Officer** · ผู้จัดการฝ่ายบุคคล | งวดไหน · วันจ่ายเมื่อไร · รอบอยู่สถานะอะไร · **เหลืออีกกี่วัน** — เหตุผล: การจ่ายค่าจ้างตามกำหนดเป็นข้อผูกพันตามกฎหมายแรงงาน · **จำนวนวันล่วงหน้าเป็นค่าที่ตั้งได้ `[AI-DRAFT]` (ยังไม่ขอเป็นคีย์ใหม่ — รวมกับ `period_rule` ที่มีอยู่)** |
| **E7** | `payroll.run_reversed` | §2 **S-47** — รอบกลับรายการถูกปิด (FN-61) | **HR Payroll Officer** · Comp Admin · Finance · ผู้อนุมัติของรอบต้นฉบับ · ⭐ **พนักงานที่ได้รับผลกระทบรายคน** | รอบต้นฉบับไหนถูกกลับรายการ · โดยรอบไหน · เพราะอะไร · ลิงก์ — ⛔ **ไม่มีจำนวนเงิน** |

### §2.1 เหตุผลรายตัว (ทำไมประกาศ ทำไมไม่ซ้ำใคร)

- **E1 · E2 เป็นการแจ้งเตือน "งานติด" ไม่ใช่ "งานเสร็จ"** — ตระกูลเดียวกับที่ Shift & Roster แจ้งตารางที่ยังไม่เผยแพร่ · **E2 มีค่าที่สุดในใบนี้** เพราะกลไก fail-closed จะเงียบมากถ้าไม่มีใครถูกบอกว่ารอบเดินต่อไม่ได้เพราะค่าที่ HR Configuration ยังไม่ประกาศ
- **E4 เป็น event เดียวในโมดูล HR ที่ยิงถึงพนักงานทุกคนพร้อมกัน** — จึงต้องเป็น **ลิงก์ล้วน ไม่มีตัวเลข ไม่มีไฟล์แนบ** · ถ้าแนบ PDF ในอีเมล เอกสาร RESTRICTED จะออกไปอยู่นอกขอบเขตที่ Policy Center คุมได้ทันที
- **E7 ยิงถึงพนักงานด้วย** เพราะเงินที่เคยแจ้งว่าจ่ายแล้วถูกกลับรายการเป็นเรื่องที่เจ้าตัวต้องรู้ — **แต่ไม่บอกจำนวน** ให้เข้าไปดูสลิปของรอบใหม่เอง
- **ไม่มี event "รอบถูกสร้าง" หรือ "คำนวณเสร็จ"** — ผู้จัดทำเป็นคนกดเองและอยู่หน้าจอนั้นอยู่แล้ว · การแจ้งสิ่งที่ตัวเองเพิ่งกดคือเสียงรบกวน

## §3 Event ที่ **ไม่ประกาศ** (และเหตุผล) — ห้ามเงียบ

| event ที่อาจนึกถึง | ประกาศ? | เหตุผล |
|---|---|---|
| `doa_pending` (มีงานรออนุมัติ) | ❌ **ห้าม** | **DOA Engine ยิงเองอัตโนมัติ** เมื่อ `GET /doa/resolve` สร้างงาน — ประกาศซ้ำ = แจ้งสองครั้ง |
| `doa_result` (อนุมัติ/ไม่อนุมัติ) | ❌ **ห้าม** | เหตุผลเดียวกัน — ครอบ **T-08 · T-09** ทั้งคู่ (S-33 · S-35) |
| `hrconfig.*` (ค่าตามกฎหมายมีผลแล้ว) | ❌ ไม่ใช่ของเรา | **HR Configuration เป็นเจ้าของ** — เราเป็นผู้ฟัง ไม่ใช่ผู้ประกาศ |
| `attendance.*` · `leave.*` · `ot.*` · `salstruct.*` · `ofb_case_*` | ❌ ไม่ใช่ของเรา | ต้นทางประกาศแล้วทั้งหมด — เราฟังเพื่อขึ้นธง (S-36) และเพื่อเข้าคิวรอบปรับปรุง (S-21) |
| "รอบถูกยกเลิก" (T-12) | ⬜ **ไม่ประกาศ** | เกิดก่อนอนุมัติเสมอ · ยังไม่มีใครนอกทีมจัดทำรู้ว่ารอบนี้มีอยู่ — ไม่มีผู้รับที่ต้องรู้ |
| "รายการบัญชีพร้อมส่ง" (S-41) | ⬜ **ไม่ประกาศรอบนี้** | **Accounting GL ยังไม่มีในระบบ** — ไม่มีผู้รับ · เมื่อ Module Linkage เปิด ให้เพิ่ม `payroll.gl_payload_ready` (บันทึกไว้ที่ `OQ-PAY-08`) |
| "สลิปของรอบปรับปรุงพร้อม" | ⬜ **ใช้ `E4` ตัวเดิม** | สลิปของรอบปรับปรุงก็คือสลิป — ไม่ตั้ง event ใหม่ให้ผู้รับต้องเรียนรู้สองแบบ |

## §4 Payload Contract

**ทุก event มี field ร่วม:**
`event_id` · `occurred_at` · `company_id` · `run_no` · `run_type` · `period_code` · `actor_id` · `link` (deep link เข้าหน้าในระบบ)

**field เฉพาะ:**

| event | field เพิ่ม |
|---|---|
| E1 | `source_feature` · `flag_type` (`unconfirmed_days` · `pending_exception_days` · `open_request_count` · `unconfirmed_hours` · `pending_docs`) · `affected_count` · `source_link` |
| E2 ⭐ | `missing_config_groups[]` (`sso` · `pit` · `pf` · `payroll_basis` · `payroll_deduction` · `payroll_review`) · `uncomputable_line_count` · `uncomputable_employee_count` · `oq_ref` (`OQ-STD-PAY1…PAY6`) |
| E3 | `employee_count` · `pay_date` · `closed_by` — ⛔ **ไม่มี `net_total`** |
| E4 | `employee_id` · `payslip_no` · `pay_date` — ⛔ **ไม่มีจำนวนเงินใด ๆ · ไม่มีไฟล์แนบ** |
| E5 | `bank_code` · `record_count` · `excluded_count` |
| E6 | `pay_date` · `days_remaining` · `run_status` |
| E7 | `reversed_run_no` (รอบต้นฉบับ) · `reversal_run_no` (รอบใหม่) · `reason` · `affected_employee_id` (เมื่อส่งรายคน) — ⛔ **ไม่มีจำนวนเงิน** |

> ⭐ **กติกาเหล็กของ payload ใบนี้:** **ไม่มี event ใดพก `amount` · `net_total` · `gross_total` · `base_amount` หรือเลขบัญชีธนาคาร** — ข้อมูลค่าจ้างเป็น RESTRICTED และ payload ของ NOTIFY เดินทางผ่านช่องทางที่มีขอบเขตสิทธิ์คนละชุด (in-app · email · LINE) · **ผู้รับต้องกดลิงก์เข้ามาดูในระบบซึ่ง Policy Center คุมอยู่** · ข้อนี้เป็นหลักการเดียวกับที่ `CSQ_BRIEF §4` ใช้กับ event ของ 7C

## §5 เพิ่มเข้า Event Catalog (F-NOTIFY `EVENT_GROUPS`) `[DEFAULT — รอยืนยัน]`

| group | events |
|---|---|
| `hr.payroll.operation` | `payroll.inputs_not_settled` · `payroll.blocked_missing_legal_config` · `payroll.pay_date_approaching` |
| `hr.payroll.closing` | `payroll.run_closed` · `payroll.bank_file_ready` · `payroll.run_reversed` |
| `hr.payroll.employee` ⭐ | `payroll.payslip_available` — **กลุ่มที่พนักงานทุกคนเป็นผู้รับ · ต้องมี preference ให้ปิด email ได้แต่ปิด in-app ไม่ได้** `[AI-DRAFT]` |

## §6 Dev wiring note

1. ทุก event ยิง **หลังจากธุรกรรมสำเร็จเท่านั้น** — `E3`/`E4` ยิงหลัง T-11 commit ครบ (เลขสลิป + PDF + สำเนา + ตรึง snapshot) · ถ้าส่วนใดล้ม **ไม่ยิงเลย**
2. `E4` เป็น **fan-out รายคน** — รอบ 500 คน = 500 การแจ้งเตือน · ต้องส่งเป็น batch ที่ ENG-NOTIFY ไม่ใช่ loop ยิงทีละใบ `[AI-DRAFT]`
3. `E2` ต้อง **ไม่ยิงซ้ำทุกครั้งที่กดคำนวณ** — ยิงเมื่อ **ชุดกลุ่มค่าที่หายเปลี่ยนไป** เท่านั้น (dedupe ตาม `missing_config_groups[]` + `run_no`)
4. `E6` เป็น scheduled check ไม่ใช่ transition — ผูกกับ `pay_date` ของ `period_rule`
5. **ห้ามผูก `E4` กับอีเมลที่มีไฟล์แนบ** — ตรวจข้อนี้ใน QA

## §7 Open Questions

| # | คำถาม | เจ้าภาพ | ระหว่างรอ |
|---|---|---|---|
| `OQ-NTF-P1` | `E1` ควรแจ้งผู้ดูแลของ feature ต้นทางด้วยหรือแจ้งแค่ผู้จัดทำรอบ | Strike | แจ้งแค่ผู้จัดทำรอบ `[DEFAULT]` (กันเสียงรบกวนข้ามทีม) |
| `OQ-NTF-P2` | พนักงานปิดการแจ้งเตือน `E4` ได้หรือไม่ | Strike / Policy | ปิด email ได้ · ปิด in-app ไม่ได้ `[AI-DRAFT]` |
| `OQ-NTF-P3` | `E6` เตือนล่วงหน้ากี่วัน และเตือนซ้ำหรือไม่ | Strike | 3 วัน ครั้งเดียว `[ASSUMED]` |
| `OQ-NTF-P4` | เมื่อ Accounting GL พร้อม ต้องเพิ่ม `payroll.gl_payload_ready` หรือให้ปลายทาง poll | Architect | ไม่ประกาศรอบนี้ (§3) |

## Quality Gate (self-check)

| G | เกณฑ์ | ผล |
|---|---|---|
| G1 | ทุก event มี trigger ที่อ้าง PREBRIEF/GAP ได้จริง | ✅ E1…E7 |
| G2 | ไม่ประกาศซ้ำ `doa_pending` / `doa_result` | ✅ §3 |
| G3 | ไม่ประกาศ event ที่เป็นของ feature อื่น | ✅ §3 (ต้นทาง 6 ที่ + hrconfig) |
| G4 | ระบุผู้รับต่อ event | ✅ |
| G5 | event ที่ไม่ประกาศ มีเหตุผลเขียนไว้ | ✅ §3 (7 แถว) |
| G6 | ⭐ **payload ไม่มีจำนวนเงินและไม่มีไฟล์แนบ** | ✅ §4 · §6 ข้อ 5 |
