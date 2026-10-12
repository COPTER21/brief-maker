# 03_LOGIC — F-HR-CERT · หนังสือรับรอง

> Audience: **Backend (ตรรกะ)** · ⭐ **อ่าน §3.0 ทั้งส่วนก่อนเขียนโค้ดใด ๆ ที่แตะ `issue_date` หรือการอ่านต้นทาง**
> Convention: Function = `camelCase` · Engine = `kebab-case` · ⭐ **feature ไม่เรียก Engine ตรง — ต้องผ่าน API เสมอ** (CUBIC 3-layer)

---

# §3.0 กลไกหลักของฟีเจอร์ (อ่านก่อนทุกอย่าง)

## §3.0.1 ⭐⭐ `buildSnap()` — จุดตรึงข้อเท็จจริงที่ T-06

> **นี่คือสิ่งเดียวที่ทำให้ฟีเจอร์นี้เชื่อถือได้** · ทุกบรรทัดในหัวข้อนี้เป็น invariant ไม่ใช่ข้อเสนอแนะ

### (ก) สัญญาของฟังก์ชัน

```
F-20  buildSnap(input) → SnapResult

input  = { employee_id, company_id, as_of, cert_type, language,
           show_position_history, template_id }
         ⭐ as_of = issue_date เสมอ — ไม่มี default เป็น "วันนี้" ที่ระดับฟังก์ชัน
            ผู้เรียก (F-26) เป็นคนตั้ง issue_date แล้วส่งลงมา

output = { ok: true,  snapshot: {...}, warnings: [...] }
       | { ok: false, blocker: { code, message, link }, warnings: [...] }
```

⭐ **ฟังก์ชันนี้ไม่เขียนฐานข้อมูลเลย** — มันคืนก้อนข้อมูล ผู้เรียกเป็นคนตัดสินใจว่าจะ INSERT หรือไม่

### (ข) ⭐ ทั้งสี่ต้นทางถูก resolve ด้วย `as_of = issue_date` ค่าเดียวกัน

| ลำดับ | ต้นทาง | เรียกด้วย | เอาอะไรมา | เอามาไว้ที่ไหนบน snapshot |
|---|---|---|---|---|
| 1 | **On/Offboard** (X-API-04) | `as_of = issue_date` | `start_date` · `last_working_day` · `employment_state` · `case_ref` · `config_version_ids` | `snap_start_date` · `snap_last_working_day` · `snap_employment_state` · `source_version_ids.onboard` |
| 2 | **Employee Movement — assignment** (X-API-02) | `as_of = issue_date` · `include=source,scheduled` | ⭐ **ตำแหน่ง · หน่วยงาน · สาขา · ระดับ · ประเภทการจ้าง จาก `assignment` เท่านั้น** · `source_movement_doc_no` · `movement_state` | `snap_position` · `snap_department` · `snap_branch` · `snap_grade` · `snap_employment_type` · `source_version_ids.movement` |
| 3 | **Employee Movement — history** (X-API-03) | `as_of = issue_date` | ⭐ **กลุ่ม `effective[]` เท่านั้น** | `snap_position_history` (เมื่อ `show_position_history = true`) |
| 4 | **Salary Structure** (X-API-01) | `date = issue_date` · **เฉพาะเมื่อ `cert_type = salary`** | `base_amount` · `currency` · `masked` · `version_id.band` | `snap_base_amount` · `snap_currency` · `snap_amount_text` · `source_version_ids.salary` |
| 5 | **HR Configuration** (X-API-05) | `date = issue_date` · `group = cert_policy` | ค่านโยบาย + `version_id` — ⭐ **รอบนี้ได้ค่าว่างเสมอ** | `source_version_ids.hr_config` (= `null`) |
| 6 | **Employee Master / Organization** | (อ่านตรง) | ชื่อ TH/EN · รหัสพนักงาน · ตำแหน่งตั้งต้น (เมื่อ `movement_state = baseline`) · `issue_place` · `issuer_contact` | `snap_employee_name_*` · `snap_issue_place` · `snap_issuer_contact` |

⭐ **ข้อบังคับสามข้อของขั้นนี้:**
1. **ค่า `as_of` ตัวเดียวกันถูกส่งไปทั้ง 5 call** — ห้ามให้ call ไหนใช้ "วันนี้" (`CI-1` · BR-09 · **IA-01**)
2. **ทั้ง 5 call ต้องสำเร็จครบ** — ตัวใดล้ม → คืน `502 ERR_UPSTREAM_UNAVAILABLE` พร้อมระบุต้นทาง · ⭐ **ไม่ตรึงอะไรเลย ไม่มี snapshot ครึ่งใบ** (PR-4)
3. **ห้าม cache ข้ามวัน** ทุกต้นทาง (`SS-3` · `MV-5` · `OB-3` · `C-3`) — cache ได้ภายในวันเดียว · ล้างเมื่อได้ event ตาม `02_API §2.6`

### (ค) ⭐⭐ ตำแหน่งมาจาก `assignment/resolve` เท่านั้น — และ `scheduled[]` ไปไม่ถึง snapshot

```
สิ่งที่ resolve คืนมา:
   assignment { position, department, branch, grade, employment_type, source_movement_doc_no }
   scheduled[] [ { movement_doc_no, effective_date, attribute_family[], has_pay_change }, … ]
                ↑ ⭐ ก้อนนี้เข้าโปรแกรมได้ แต่ไปได้แค่ F-18 เท่านั้น

F-20 buildSnap()          ← รับเฉพาะ assignment  (type: Assignment)
F-18 detectScheduledWarning() ← รับเฉพาะ scheduled[] (type: ScheduledItem[])
```

- ⭐ **บังคับด้วย type ที่แยกกัน ไม่ใช่ด้วยวินัยของคนเขียน** — `buildSnap()` **ไม่มี parameter ที่รับ `ScheduledItem[]` เลย** จึงไม่มีทางที่ค่าที่รอมีผลจะไหลเข้า snapshot ได้แม้เขียนโค้ดผิด
- `F-18` คืน `warnings[]` เท่านั้น — คำเตือนขึ้นบนหน้าจอ ("มีคำสั่งที่จะมีผล DD/MM — หนังสือฉบับนี้ยังไม่รวมรายการนั้น") และ **ถูกบันทึกลง `snap_scheduled_warning` เพื่ออธิบายย้อนหลัง ไม่ใช่เพื่อพิมพ์**
- ⭐ **ไม่มี code path ใดที่แปลง `ScheduledItem` เป็นค่าที่พิมพ์ได้** · ⭐ **ไม่มี endpoint · ไม่มีปุ่ม · ไม่มี flag ใดที่ทำให้ `scheduled[]` ถูกใช้เป็นค่าปัจจุบัน** (`MV-2` · BR-14 · FN-18 · **IA-08**)
- **ถ้า `assignment: null` (`NO_MOVEMENT_FOR_EMPLOYEE`)** → ⭐ **ห้ามตีความว่าไม่มีตำแหน่ง** → ใช้ค่าตั้งต้นจาก Employee Master พร้อมบันทึก `movement_state = baseline` ลง snapshot (FN-46)

### (ง) ⭐ ประวัติพิมพ์เฉพาะ `effective[]`

- `history/resolve` คืนสองกลุ่มแยกกัน — `effective[]` (มีผลแล้ว) กับ `scheduled[]` (รอมีผล)
- ⭐ **`buildSnap()` อ่านเฉพาะ `effective[]`** · กลุ่ม `scheduled[]` ของ history **ถูกทิ้งทันทีที่ระดับ mapper** — ไม่มีทางรวมเข้าเส้นเดียวกัน (FN-20)
- ⭐ **แถวตระกูล `pay` ในประวัติคืนค่าที่ปิดบังเสมอจากต้นทาง** (`MV-4`) — และฟีเจอร์นี้ **ไม่พิมพ์แถวตระกูลนั้นลงหนังสือเลย** เพราะหนังสือรับรองพิมพ์ได้แค่ **ตำแหน่ง/หน่วยงาน/ช่วงเวลา** (BR-28)

### (จ) ⭐ `version_id` ทั้งสี่ก้อนถูกเก็บบนเอกสาร

```
source_version_ids = {
  salary   : <uuid | null>,        ← version_id.band จาก Salary Structure (null เมื่อไม่ใช่ประเภทเงินเดือน)
  movement : <movement_doc_no | null>,  ← source_movement_doc_no (null เมื่อ movement_state = baseline)
  onboard  : { case_ref, config_version_ids: { holiday_calendar, period_rule, employment_term: null } },
  hr_config: <uuid | null>         ← ⭐ null เสมอในรอบนี้ (cert_policy ยังไม่เผยแพร่)
}
```

- ⭐ **ห้ามคัดลอกตัวเลขไปเก็บถาวรโดยไม่มี `version_id` คู่กัน** — สิ่งที่เก็บคือ **snapshot ของเอกสาร ไม่ใช่ตารางอัตราเงา** (BR-13 · `SS-2` · **IA-02**)
- ⭐ **ก้อนที่เป็น `null` ต้องรับได้ทุกที่** — `hr_config` เป็น `null` เสมอ · `employment_term` เป็น `null` เสมอ (คู่ขนานกับ `F-HR-ONBOARD` `OQ-STD-OB3` และ `F-HR-ROSTER` `shift_rule`)

### (ฉ) ⭐⭐ หลัง "ออกแล้ว" เนื้อหาห้ามเปลี่ยนตลอดไป (BR-23)

| ก่อน `issued` | ตั้งแต่ `issued` |
|---|---|
| ทุกครั้งที่เปิดดู = **อ่านสดจากต้นทาง** (`F-17 previewFacts`) | ⭐ **แสดงจาก snapshot เท่านั้น — ไม่อ่านต้นทางอีกเลย** |
| ค่าที่เห็นเปลี่ยนได้ตามข้อมูลจริง | ⭐ **ค่าที่เห็นเหมือนเดิมทุกตัวอักษรตลอดกาล** |
| ยังไม่มีไฟล์ | `F-23 renderDocument()` รับ **snapshot** เป็น input ไม่ใช่ `employee_id` |

- ⭐ **`renderDocument()` ไม่มี parameter ที่ทำให้มันไปอ่านต้นทางได้** — signature รับ `(snapshot, rendition, template_version_id)` เท่านั้น
- ⭐ **การ re-render จาก snapshot เดิมต้องได้ไฟล์ที่เหมือนเดิมทุกประการ** (byte-for-byte เมื่อ template version เดิม) — ทดสอบที่ **IA-02** · CP-12
- ตาราง `T_certificate_snapshot` ⭐ **INSERT ครั้งเดียว ไม่มี UPDATE ไม่มี DELETE** — บังคับด้วย trigger ที่ระดับฐานข้อมูล (`04_DB §4.7`)

### (ช) ⭐ ต้นทางเปลี่ยนหลังออกหนังสือ → ติดธง แล้วจบ

```
event จากต้นทาง (ofb_case_cancelled · move_cancelled_before_effective ·
                 move_superseded · move_voided_employee_left)
        │
        ▼
F-32 applyUpstreamChangedFlag(event)
        ├─ หาใบที่ "ออกไปแล้ว" (issued / delivered) ซึ่ง source_version_ids อ้างถึงสิ่งที่เปลี่ยน
        ├─ set upstream_changed_flag = true + เขียน upstream_changed_detail (อะไรเปลี่ยน · เมื่อไร · จากต้นทางไหน)
        ├─ เขียนแถวใน T_certificate_history
        └─ จบ
             ⭐ ไม่แก้ snapshot          ⭐ ไม่ re-render ไฟล์
             ⭐ ไม่เปลี่ยนสถานะใบ         ⭐ ไม่ยิงแจ้งเตือนถึงพนักงาน (OQ-NTF-CT-B)
             ⭐ ไม่เพิกถอนให้เอง          → HR เป็นผู้ตัดสินใจ (FN-72 · BR-19 · IA-11)
```

**เหตุผล:** เอกสารอยู่ในมือธนาคาร/สถานทูตแล้ว · การที่ระบบ "แก้ให้เอง" จะทำให้ **ไฟล์ในระบบไม่ตรงกับไฟล์ที่คนนอกถืออยู่** ซึ่งแย่กว่าการปล่อยให้ต่างกันโดยรู้ตัว · ธงมีไว้ให้ HR ตัดสินใจว่าจะ **เพิกถอน** หรือ **ออกใหม่แทน** หรือ **ไม่ทำอะไร** (บางกรณีหนังสือยังถูกต้องอยู่)

## §3.0.2 ⭐ การเลือกสายอนุมัติ — สองรูปสาย และเหตุผลที่ตัวเลขเงินต้องไม่อยู่ในกติกา

```
F-04 computeHasSalaryFigure(cert_type) → bool
        has_salary_figure = (cert_type == "salary")
        ⭐ ฟังก์ชันตายตัว · ไม่มี input จากผู้ใช้ · ผู้ใช้ตั้งเองไม่ได้

F-05 pickAction(cert_type, purpose) → action_id
        ⭐ signature ไม่มี argument ที่เป็นจำนวนเงิน ไม่มีเปอร์เซ็นต์ ไม่มี grade
        employment / service_letter → "cert_approve_employment"
        salary                       → "cert_approve_salary"
        (resubmit / reissue ใช้ matrix ของสองตัวข้างบนตามค่า has_salary_figure ณ เวลาที่ resolve)

F-06 resolveApprovalChain(action_id, employee_id, company_id) → Step[]
        → GET /doa/resolve   ⭐ ไม่มี query parameter ที่เป็นเงินเลย
        คืน 1 step (role-mgr-hr) หรือ 2 step (role-mgr-hr → role-comp-admin)
```

| รูปสาย | เกิดเมื่อ | ขั้นที่ 1 | ขั้นที่ 2 |
|---|---|---|---|
| **1 ขั้น** | `has_salary_figure = false` | `role-mgr-hr` | — |
| **2 ขั้น** ⭐ | `has_salary_figure = true` | `role-mgr-hr` | ⭐ `role-comp-admin` — **ผู้ดูแลข้อมูลค่าจ้าง (ต้องมีสิทธิ์ RESTRICTED)** |

### ⭐ ทำไมนี่เป็น invariant (`CI-6` · IA-04)

ถ้าเอา **จำนวนเงินเดือนของพนักงาน** ไปเป็นขอบของ matrix ("เกิน X ต้องเพิ่มขั้น") จะเสียสองชั้น
1. **ตัวเลขที่มี `effective_date` ถูกคัดลอกไปฝังในทะเบียน DOA** — วันที่ Salary Structure ประกาศกระบอกใหม่ matrix จะเงียบ ๆ ผิดทันที (ผิด `P-8` · `P-8′`)
2. ⭐⭐ **"เงินเดือนของคนคนหนึ่ง" รั่วออกมาเป็นความยาวของสายอนุมัติ** — ใครที่เห็นว่าใบนี้ผ่านกี่ขั้นจะอนุมานช่วงเงินเดือนได้ทันที **โดยไม่ต้องเห็นตัวเลขเลย** · สิ่งที่รั่วไม่ใช่ข้อมูล แต่เป็น **รูปร่างของกระบวนการ** ซึ่งผ่านชั้น masking ทุกชั้นไปได้ — เป็น "ทางอ้อม" ที่ **`SS-5` ห้ามไว้ตรง ๆ**

**วิธีตรวจตอน dev:** `grep` หา `amount` ในไฟล์ที่เรียก DOA → **ต้องไม่พบค่าจริง** · ตรวจ signature ของ `F-05` → **ต้องมีแค่สอง argument ที่เป็น enum** (`DOA_BRIEF §6`)

**อื่น ๆ ของสาย:**
- `F-07 freezeApprovalChain` — สาย resolve ตอนกดส่งแล้ว **แช่แข็ง** · แก้ทะเบียน DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว (BR-07)
- `F-12 assertSoD` — ⭐ **ใบนี้เสี่ยงกว่าใบพี่น้อง เพราะผู้ยื่นมักเป็น HR เอง** · ถ้าสายที่ resolve ได้มีแต่ตัวผู้ยื่น → **บล็อก + ให้เลือกคนอื่นที่มีสิทธิ์เดียวกัน** `[DEFAULT — รอยืนยัน]` (`OQ-DOA-CT-A`)
- **จำนวน slot บนหน้าจอ = จำนวน step ที่ resolve ได้จริง** — ⭐ **ห้ามวาดตายตัว** (BR-05)
- ⭐ **slot ขั้นที่ 2 กรองเฉพาะผู้มีสิทธิ์ RESTRICTED ตั้งแต่ตอนเลือก** — ไม่ใช่ปล่อยผ่านแล้วไปตายตอนกดออก
- ⭐ **"การออกหนังสือ" (T-06) ไม่ใช่ action ของ DOA** — อำนาจอยู่ที่การอนุมัติคำขอไปแล้ว · ทำเป็น action = อนุมัติซ้ำสองชั้นในเรื่องเดียวกัน

## §3.0.3 ⭐⭐ ค่าจ้างที่ถูกปิดบัง ⇒ ปฏิเสธการออก (ไม่ใช่เว้นช่อง)

```
F-21 assertIssuable(snap) → ok | Blocker

ด่านที่ 1 ⭐ masked
    if cert_type == "salary" and snap.masked == true:
        → F-39 emitSecurityEvent("cert.issue_blocked_masked",
                                 { actor_id, cert_doc_no, employee_id, company_id,
                                   cert_type, blocked_reason: "MASKED", attempted_at })
        → return Blocker(ERR_SALARY_MASKED,
              "ต้องมีสิทธิ์เข้าถึงข้อมูลค่าจ้างจึงจะออกหนังสือประเภทนี้ได้",
              link = ส่งต่อผู้มีสิทธิ์)
        ⭐ ไม่ตรึงอะไร · ไม่สร้างไฟล์ · ไม่เปลี่ยนสถานะ

ด่านที่ 2   rate = null / NO_RATE_AT_DATE  → ERR_NO_RATE_AT_DATE + ลิงก์ "จัดการที่ โครงเงินเดือน"
            ⭐ ห้ามใช้อัตราของวันใกล้เคียงแทน (BR-12)
            → ยิง cert.issue_blocked_masked ด้วย blocked_reason = "NO_RATE_AT_DATE"
ด่านที่ 3   window = null / NO_CASE_FOR_EMPLOYEE → ERR_NO_EMPLOYMENT_WINDOW + ลิงก์ "ปรับปรุงที่ เข้าออกงาน"
            ⭐ ห้ามตีความว่าไม่ใช่พนักงาน · ⭐ ไม่มีทางลัดให้พิมพ์วันเริ่มงานเอง (BR-18)
ด่านที่ 4   employment_state == "not_started"     → ERR_NOT_STARTED
            ⭐ employment_state == "left" ไม่ใช่ด่าน — ผ่านได้เสมอ (BR-27 · §3.0.6)
ด่านที่ 5   language == "en" and !snap_employee_name_en → ERR_NO_EN_NAME + ลิงก์ Employee Master
            ⭐ ระบบไม่ทับศัพท์ชื่อให้เอง
ด่านที่ 6   template ที่เลือกไม่ active แล้ว        → ERR_TEMPLATE_INACTIVE
```

### ⭐ ทำไม "ไม่ออก" ถึงเป็นผลลัพธ์ที่ถูกต้อง ไม่ใช่ความล้มเหลว

- **เอกสารที่มีหัวข้อค่าจ้างแต่เว้นตัวเลขไว้ แย่กว่าไม่ออกเลย** — ปลายทางจะตีความเองว่า "เงินเดือนเป็นศูนย์" หรือ "บริษัทปกปิด" ซึ่งทั้งคู่ทำร้ายพนักงาน
- **การเว้นช่องคือทางอ้อม** — ถ้าออกหนังสือได้โดยไม่มีตัวเลข คนที่ไม่มีสิทธิ์จะ "ออกไปก่อนแล้วให้คนอื่นเติม" ซึ่งเป็นการหลบชั้น masking
- ⭐ **`ENG-02 document-rendition-selector` ไม่มีค่าที่ห้า** — รับ `(language, has_salary_figure, masked)` แล้วคืน 1 ใน 4 rendition **หรือคืน `REFUSE`** · **ไม่มี rendition แบบ "มีหัวข้อค่าจ้างแต่ไม่มีตัวเลข"** ให้เลือกได้เลย (`PRINT_SPEC §P.2`)
- **จำนวนเงินตัวอักษรสืบทอดการปิดบัง** — `snap_amount_text` คำนวณจาก `snap_base_amount` เท่านั้น · ปิดบังตัวเลข = ไม่มีตัวอักษรด้วย (BR-11 · FN-52)
- **`cert.issue_blocked_masked` ไม่ใช่ error log** — เป็น ⭐ **สัญญาณเชิงกำกับดูแลที่มีค่าที่สุดของฟีเจอร์นี้** เพราะมันคือ "มีคนพยายามทำให้ข้อมูลค่าจ้างออกนอกองค์กรโดยไม่มีสิทธิ์ แล้วระบบปฏิเสธไว้" (`CSQ_BRIEF §2 E4` · KPI-05 · TH-05)

## §3.0.4 ⭐ ออกใหม่แทน กับ เพิกถอน = **แทนที่ ไม่ใช่ลบ**

### (ก) เพิกถอน (T-08 · `F-29`)

```
F-29 revokeCertificate(cert_id, revoke_reason, actor)
  1. ตรวจสถานะ ∈ { issued, delivered }              → ไม่ใช่ = 409
  2. บังคับ revoke_reason (ว่าง = 422 ERR_REASON_REQUIRED)
  3. set status = revoked · revoked_by · revoked_at · revoke_reason
     ⭐ ไม่แตะ T_certificate_snapshot เลยแม้แต่คอลัมน์เดียว
     ⭐ ไม่ลบไฟล์ — pdf_file_ref เดิมยังเปิดได้ตามปกติ
  4. F-24 storeDocumentCopy(pdf, 'revoked')          ← เพิ่มสำเนาใหม่ ไม่ทับของเดิม
  5. เขียน history · F-38 ยิง cert_revoked ("กรุณาอย่าใช้ฉบับดังกล่าวต่อไป")
  6. F-39 ยิง cert.revoked (SecC E5) พร้อม reversal_of ชี้ event cert.issued เดิม
     ⭐ ห้ามลบหรือแก้ event เดิมที่ยิงไปแล้ว (BR-CSQ-04)
```

⭐ **ทำไมไฟล์ยังอยู่:** เพราะ **ฉบับจริงอยู่ในมือบุคคลภายนอกแล้ว** · การลบไฟล์ในระบบไม่ได้ทำให้ฉบับข้างนอกหายไป แต่ทำให้องค์กร **พิสูจน์ไม่ได้ว่าฉบับที่ออกไปหน้าตาอย่างไร** เมื่อถูกโต้แย้งภายหลัง

### (ข) ออกใหม่แทน (T-09 · `F-30` + `F-31`)

```
F-30 reissueCertificate(old_cert_id, reason, new_attrs)      ← ที่ API-16
  1. ตรวจใบเดิม ∈ { issued, delivered, revoked }
  2. สร้าง "ใบใหม่" เป็น draft ที่ supersedes = <เลขเดิม>
     ⭐ ใบเดิมยังไม่เปลี่ยนสถานะ ณ จุดนี้
  3. ผู้ใช้เดินตัวช่วยต่อ → API-06 submit → เลขใหม่ → เดินสายอนุมัติใหม่ทั้งสาย (OQ-CT-09)

F-31 markSuperseded(old_cert_id, new_cert_doc_no)            ← ถูกเรียกจาก F-26 เท่านั้น
  เรียกเมื่อ "ใบใหม่ออกสำเร็จแล้ว" (หลังขั้นที่ 9 ของ §3.0.1) :
  1. set old.status = superseded · old.superseded_by = <เลขใหม่>
     ⭐ ไม่แตะ snapshot ของใบเดิม · ⭐ ไม่ลบไฟล์เดิม
  2. F-24 storeDocumentCopy(old_pdf, 'superseded')
  3. เขียน history ทั้งสองใบให้ชี้หากัน
```

⭐ **ลำดับที่ห้ามสลับ:** `F-31` ถูกเรียกจาก `F-26` (ตอนใบใหม่ออกสำเร็จ) **ไม่ใช่จาก `F-30`** (ตอนสร้างร่าง)
> เหตุผล: ถ้าเปลี่ยนใบเดิมเป็น `superseded` ตั้งแต่ตอนสร้างร่าง แล้วใบใหม่ถูกปฏิเสธ **พนักงานจะไม่มีเอกสารที่ใช้ได้เลยทั้งที่ไม่ควรเป็นแบบนั้น**

### (ค) สิ่งที่ไม่มีในระบบทั้งสองทาง

| ไม่มี | เพราะ |
|---|---|
| ปุ่มลบใบที่ออกแล้ว | BR-22 · ⭐ บังคับที่ระดับฐานข้อมูลด้วย (`04_DB §4.7`) ไม่ใช่แค่ซ่อนปุ่ม |
| ปุ่มแก้เนื้อหาใบที่ออกแล้ว | BR-23 · `renderDocument()` ไม่มีทางรับค่าที่คนแก้ |
| การ "แก้ไขเล็กน้อย" ของใบที่ออกแล้ว | ⭐ ทางเดียวคือออกใหม่แทน — ไม่มีทางกลาง |
| ใบที่มีทั้ง `revoked_at` และ `superseded_by` | CHECK constraint กันไว้ (CA-04 · `04_DB §4.7`) |

## §3.0.5 ⭐ เส้นทางของอดีตพนักงาน (S-43 · BR-27) — สิทธิตามกฎหมาย

```
ป.พ.พ. มาตรา 585 : "เมื่อการจ้างงานสุดสิ้นลงแล้ว ลูกจ้างชอบที่จะได้รับใบสำคัญ
                    แสดงว่าลูกจ้างนั้นได้ทำงานมานานเท่าไร และงานที่ทำนั้นเป็นงานอย่างไร"
พ.ร.บ.คุ้มครองแรงงาน 2541 มาตรา 14 (แนวปฏิบัติเดียวกัน)
```

**ผลที่ตามมาในระบบ (สามข้อ):**

| # | ข้อบังคับ | รูปธรรม |
|---|---|---|
| 1 ⭐ | **`employment_state = left` ไม่ใช่เหตุให้บล็อกไม่ว่ากรณีใด** | `F-21 assertIssuable` **ไม่มีด่านที่ตรวจ `left`** — สิ่งที่บล็อกได้มีแค่ `not_started` (ด่าน 4) กับข้อมูลต้นทางไม่พอ (ด่าน 2 · 3) |
| 2 | **ต้องมีทางเข้าที่ใช้ได้จริง** | `API-25` รองรับ `include_left=true` · ตัวช่วยขั้น 1 มีตัวกรอง "รวมพนักงานที่พ้นสภาพ" สำหรับ HR (FN-93) |
| 3 | **ต้องมีช่องทางรับที่ใช้ได้จริง** | `VR-09` — ตัวเลือก "ดาวน์โหลดเอง" ถูกซ่อน (ไม่มีบัญชีผู้ใช้แล้ว) · เหลือ "รับที่ HR" กับ "อีเมลที่บันทึกไว้" · ไม่มีอีเมล → บังคับ "รับที่ HR" (`OQ-NTF-CT-C` · FN-94) |

**ข้อความบนหนังสือ** — `F-36 buildEmploymentStatement(employment_state, dates)` เลือกสำนวนตายตัว:

| `employment_state` | สำนวน (ไทย) | อายุงานนับถึง |
|---|---|---|
| `active` | "…ปัจจุบันยังคงปฏิบัติงานอยู่กับบริษัทฯ" | `issue_date` |
| `leaving` | "…และมีกำหนดสิ้นสุดการปฏิบัติงานในวันที่ {last_working_day}" | `issue_date` |
| `left` | ⭐ "…**เคยปฏิบัติงานกับบริษัทฯ ระหว่างวันที่ {start_date} ถึงวันที่ {last_working_day}**" | ⭐ **`last_working_day`** (ไม่ใช่วันที่ออกหนังสือ) |
| `not_started` | — | ⛔ บล็อก |

⭐ **`last_working_day = null` ไม่แปลว่า "ทำงานตลอดไป"** — ตัวตัดสินคือ `employment_state` เท่านั้น (`OB-4` · BR-17 · **IA-10**)

## §3.0.6 ⭐⭐ กฎ "ไม่มีข้อความอันเป็นที่เสียหาย" (S-44 · BR-28) — บังคับด้วยโครงสร้าง

> **กฎข้อนี้ไม่ได้ถูกบังคับด้วย validation** — เพราะ validation ที่ตรวจ "ข้อความเชิงลบ" เป็นไปไม่ได้ในทางปฏิบัติ
> **มันถูกบังคับด้วยการที่ไม่มีที่ให้ข้อความนั้นอยู่ตั้งแต่ต้น** — สี่ชั้นซ้อนกัน

| ชั้น | มาตรการ | ตรวจที่ |
|---|---|---|
| **ชั้นที่ 1 — สัญญาต้นทาง** | ⭐ **On/Offboard ไม่เผยแพร่ `termination_reason` · `is_immediate_exit`** ตั้งแต่ระดับ API (`F-HR-ONBOARD §0.13.1`) → ฟีเจอร์นี้ **ไม่มีทางรู้เหตุผลการพ้นสภาพเลย** แม้จะอยากรู้ | `00_OVERVIEW §0.13.1` |
| **ชั้นที่ 2 — schema** | ⭐ **ไม่มีคอลัมน์ใดใน `T_certificate_snapshot` ที่เก็บข้อความอิสระซึ่งถูก render ลงเอกสาร** — ทุกคอลัมน์ที่ render ได้เป็นค่าที่มาจาก `resolve()` ทั้งหมด | `04_DB §4.3` · `§4.7` · `F-44` |
| **ชั้นที่ 3 — แม่แบบ** | ⭐ **โครง template ไม่มี block ที่รับข้อความอิสระเลย** — ทุก placeholder ผูกกับ field ที่มาจาก snapshot (`PRINT_SPEC §P.3`) | `PRINT_SPEC §P.4` |
| **ชั้นที่ 4 — หน้าจอ** | ⭐ **ไม่มีช่องกรอกอิสระในทุกขั้นของตัวช่วยและในมุมมองใบ** (`01_UI §1.5` ข้อ 18) | AT-95 · **IA-14** |

**`F-44 assertNoFreeTextOnDocument()`** — ฟังก์ชันตรวจเชิงโครงสร้างที่รันตอน build/test:
```
สำหรับทุก placeholder ในแม่แบบทั้งสองไฟล์:
    ต้อง map ไป field ของ T_certificate_snapshot หรือค่าคงที่ของแม่แบบ
    ⭐ ถ้าเจอ placeholder ที่ map ไปคอลัมน์ที่ผู้ใช้พิมพ์ได้ → build fail
```

⭐ **`purpose_note` (ช่องระบุเมื่อเลือกจุดประสงค์ "อื่น ๆ") ไม่ถูก render ลงเอกสารในฐานะหมายเหตุอิสระ** — ใช้จัดหมวดของคำขอกับแสดงในทะเบียนเท่านั้น
⭐ **`recipient_name` ถูกพิมพ์ในฐานะ "เรียน …" ซึ่งเป็นคำขึ้นต้นมาตรฐาน ไม่ใช่หมายเหตุ** — และเป็นค่าที่ผู้ขอเป็นคนระบุเองว่าจะยื่นที่ไหน ไม่ใช่ข้อความที่ผู้ออกเขียนถึงตัวลูกจ้าง

**สิ่งที่หนังสือพิมพ์ได้ (รายการปิด — เพิ่มไม่ได้โดยไม่แก้ FRD):**
ระยะเวลาที่ทำงาน · ลักษณะงาน/ตำแหน่ง/หน่วยงาน/สาขา/ประเภทการจ้าง · อายุงาน · (ค่าจ้าง เมื่อเป็น rendition ค่าจ้าง) · ข้อความคงที่ของแม่แบบ (ขอบเขตการรับรอง · ช่องทางตรวจสอบ) · ข้อมูลบริษัท · เลขที่ · วันที่ · สถานที่ออก · รหัสตรวจสอบ · ชื่อ/ตำแหน่งผู้ลงนาม

## §3.0.7 ⭐ นโยบายที่ต้นทางยังไม่เผยแพร่ (S-30)

```
X-API-05  GET /hr-config/resolve?date=<issue_date>&company_id=&group=cert_policy
   → 404 / กลุ่มไม่มี / ไม่มีเวอร์ชัน active
   ⭐ ปฏิบัติเหมือน "ค่าว่าง" ไม่ใช่ error (PR-8)
        hr_config_values      = {}
        source_version_ids.hr_config = null
        warnings += CERT_POLICY_NOT_PUBLISHED
   ⭐ ไม่บล็อกการออกหนังสือ
   ⭐ ห้ามใส่ค่า default ที่เดาเอง — UI แสดง "ยังไม่ได้ตั้งค่า"
```

⭐ **นี่คือคีย์ที่ขาดตัวที่ 6 ของ module HR** ต่อจาก `legal_minimum` · `ot_cap.*` · `shift_rule.*` · `employment_term.*` (ยกไปแล้ว 2 รอบ) → **`OQ-STD-CT3`** · ควรเคาะรวมเป็นการเปลี่ยนแปลงเดียวของ HR Configuration

---

# §3.1 Function Inventory (44 ตัว)

> Convention: `camelCase` · ⭐ **ทุกฟังก์ชันที่รับวันที่ ต้องรับเป็น parameter — ห้ามอ่าน "วันนี้" ข้างใน**

## §3.1.1 กลุ่มคำขอ (F-01…F-11)

| # | Function | Input → Output | ทำอะไร | กฎที่ผูก |
|---|---|---|---|---|
| **F-01** | `createDraft(payload, actor)` | → `{cert_id, row_version}` | สร้างร่าง · ⭐ **ไม่ออกเลข ไม่เรียกต้นทางเลย** · รองรับ `employee_state = left` (BR-27) | BR-01 · BR-27 |
| **F-02** | `updateDraft(cert_id, patch, row_version)` | → `{row_version}` | แก้ร่าง · ⭐ ปฏิเสธถ้าใบมีเลขแล้ว | BR-22 |
| **F-03** | `deleteDraft(cert_id)` | → `void` | ⭐ **ลบได้เฉพาะร่างที่ยังไม่มีเลข** · เขียน history ก่อนลบ | BR-22 · VR-15 |
| **F-04** | `computeHasSalaryFigure(cert_type)` | → `bool` | ⭐ **ฟังก์ชันตายตัว** `cert_type == "salary"` · ผู้ใช้ตั้งเองไม่ได้ | BR-06 |
| **F-05** ⭐ | `pickAction(cert_type, purpose)` | → `action_id` | ⭐ **signature ไม่มี argument ที่เป็นจำนวนเงิน** | BR-06 · **IA-04** |
| **F-06** | `resolveApprovalChain(action_id, employee_id, company_id)` | → `Step[]` | เรียก DOA engine · ⭐ **ไม่ส่งค่าเงิน** | BR-04 |
| **F-07** | `freezeApprovalChain(cert_id, steps, slots)` | → `void` | เขียน `T_certificate_approval_trace` · แช่แข็ง | BR-07 |
| **F-08** | `issueDocNo(company_ctx)` | → `cert_doc_no` | ⭐ `ENG-DOC-NUM.next('CERT')` · **ห้ามฟอร์แมตเอง ห้าม +1 เอง** | BR-01 · BR-02 |
| **F-09** | `validateSubmit(cert)` | → `Violation[]` | ช่องบังคับครบ · ภาษา EN มีชื่อ EN | VR-01…VR-09 |
| **F-10** | `checkConsentTrace(cert)` | → `ok \| Violation` | ⭐ ยื่นแทน + ประเภทเงินเดือน → บังคับร่องรอยความยินยอม | BR-25 · VR-13 |
| **F-11** | `checkDuplicatePending(employee_id, cert_type, language)` | → `Cert[]` | หาใบซ้ำที่ยังรออนุมัติ | VR-14 |

## §3.1.2 กลุ่มสายอนุมัติ (F-12…F-16)

| # | Function | ทำอะไร | กฎ |
|---|---|---|---|
| **F-12** ⭐ | `assertSoD(cert, steps, actor)` | ⭐ ผู้ขอ/ผู้ยื่นแทนเซ็นใบตัวเองไม่ได้ · สายที่มีแต่ผู้ยื่น = บล็อก | BR-08 · **IA-05** |
| **F-13** | `submitCertificate(cert_id, slots, actor)` | **orchestrator ของ T-02** — ลำดับ 10 ขั้นใน `02_API §2.2 API-06` | BR-01 · BR-04…BR-08 |
| **F-14** | `approveStep(cert_id, step_seq, actor, comment)` | อนุมัติขั้นปัจจุบัน · บันทึก **ผู้เซ็นจริง** ต่างจากผู้ถูกกำหนดได้ · ขั้นสุดท้าย → T-05 | BR-07 · FN-33 |
| **F-15** | `rejectCertificate(cert_id, reason, actor)` | ⭐ เหตุผลบังคับ · ใบสิ้นสุด · **เลขไม่ reuse** | BR-01 · VR-25 |
| **F-16** | `cancelCertificate(cert_id, reason, actor)` | ผู้ขอ/ผู้ยื่นแทนยกเลิกก่อนอนุมัติครบ | BR-07 · VR-28 |

## §3.1.3 ⭐ กลุ่มจุดตรึงข้อเท็จจริง (F-17…F-26) — หัวใจของฟีเจอร์

| # | Function | Input → Output | ทำอะไร | กฎ |
|---|---|---|---|---|
| **F-17** | `previewFacts(cert, as_of)` | → `{facts, warnings[], blockers[]}` | ⭐ **อ่านสด ไม่ตรึง ไม่เขียนฐาน** · ใช้ที่ขั้น 3 · ⭐ **ไม่แสดงตัวเลขค่าจ้าง** | BR-09 · FN-15 |
| **F-18** ⭐ | `detectScheduledWarning(scheduled: ScheduledItem[])` | → `Warning[]` | ⭐ **รับ `ScheduledItem[]` เท่านั้น · คืนคำเตือนเท่านั้น · ไม่มีทางคืนค่าที่พิมพ์ได้** | BR-14 · **IA-08** |
| **F-19** | `detectFactsChangedSinceSubmit(cert, facts_now)` | → `Diff[]` | เทียบค่าวันยื่นกับวันออก → ให้ผู้ออกยืนยันก่อน | BR-09 · VR-22 |
| **F-20** ⭐⭐ | `buildSnap(input)` | → `SnapResult` | ⭐ **§3.0.1 ทั้งหัวข้อ** · ⭐ **ไม่มี parameter ที่รับ `ScheduledItem[]`** · ⭐ **ไม่เขียนฐาน** | CI-1…CI-3 · **IA-01 · IA-02 · IA-08 · IA-09** |
| **F-21** ⭐ | `assertIssuable(snap)` | → `ok \| Blocker` | ⭐ **ด่าน 6 ตัวใน §3.0.3** · ⭐ **ไม่มีด่านที่ตรวจ `left`** | BR-10 · BR-12 · BR-16 · BR-18 · BR-27 · **IA-07 · IA-13** |
| **F-22** ⭐ | `selectRendition(language, has_salary_figure, masked)` | → `rendition \| REFUSE` | ⭐ **คืน 1 ใน 4 หรือ REFUSE — ไม่มีค่าที่ห้า** | `PRINT_SPEC §P.2` · **IA-07** |
| **F-23** | `renderDocument(snapshot, rendition, template_version_id)` | → `pdf` | ⭐ **signature ไม่มีทางไปอ่านต้นทางได้** · re-render จาก snapshot เดิม = ไฟล์เดิม | BR-23 · **IA-02** |
| **F-24** | `storeDocumentCopy(pdf, cert_id, store_event)` | → `file_ref` | ⭐ **idempotent ต่อ `(cert_id, event)`** · **เพิ่มสำเนา ไม่ทับ ไม่ลบ** | BR-03 · BR-22 |
| **F-25** | `generateVerificationCode(cert_id)` | → `code` | สุ่ม · ตรวจไม่ซ้ำก่อนบันทึก · **ไม่ใช่เลขรัน** | FN-48 · DI-05 |
| **F-26** ⭐⭐ | `issueCertificate(cert_id, issue_date, template_id, acks, actor)` | → `IssueResult` | **orchestrator ของ T-06** — ลำดับ 10 ขั้นใน `02_API §2.2 API-11` · ⭐ **เรียก `F-31` เมื่อใบนี้ `supersedes` ใบอื่น** | CI-1…CI-9 |

## §3.1.4 กลุ่มส่งมอบ · เพิกถอน · แทนที่ (F-27…F-33)

| # | Function | ทำอะไร | กฎ |
|---|---|---|---|
| **F-27** | `recordDelivery(cert_id, method, actor)` | T-07 · บันทึกช่องทาง + เวลา + ครั้งที่ · `store('sent_external')` | BR-26 · FN-58 |
| **F-28** ⭐ | `recordAccess(cert_id, actor, access_type, rendition)` | T-12 · เขียน `T_certificate_access_log` · ⭐ **ตรวจ ACL ที่ตัวไฟล์ทุกครั้ง** · ถ้าไฟล์มีตัวเลข → เรียก `F-39` | BR-26 · FN-74 · FN-77 |
| **F-29** | `revokeCertificate(cert_id, reason, actor)` | T-08 · **§3.0.4(ก)** | BR-22 · **IA-12** |
| **F-30** | `reissueCertificate(old_cert_id, reason, attrs)` | สร้างใบใหม่เป็นร่างที่ `supersedes` · ⭐ **ยังไม่เปลี่ยนใบเดิม** | BR-22 |
| **F-31** ⭐ | `markSuperseded(old_cert_id, new_doc_no)` | ⭐ **ถูกเรียกจาก `F-26` เท่านั้น** (เมื่อใบใหม่ออกสำเร็จ) · **§3.0.4(ข)** | BR-22 · BR-23 |
| **F-32** ⭐ | `applyUpstreamChangedFlag(event)` | T-11 · **§3.0.1(ช)** — ⭐ **ติดธงเท่านั้น** | BR-19 · BR-23 · **IA-11** |
| **F-33** | `ackUpstreamChangedFlag(cert_id, actor, note)` | HR รับทราบธง · ⭐ **ประวัติยังคงอยู่ ไม่ลบ** | BR-19 · BR-22 |

## §3.1.5 กลุ่มทะเบียน · การอ่าน · การเผยแพร่ (F-34…F-37 · F-42…F-44)

| # | Function | ทำอะไร | กฎ |
|---|---|---|---|
| **F-34** | `searchRegister(filters)` | ค้น 6 ทาง · เรียกใช้ `ENG-04` เพื่อคลี่สายการแทนที่ | FN-63 · FN-64 |
| **F-35** | `verifyByCode(code)` | ค้นด้วยรหัสตรวจสอบ → ต้องได้ใบเดียวเสมอ | FN-48 · KPI-06 |
| **F-36** ⭐ | `buildEmploymentStatement(employment_state, start_date, last_working_day, language)` | ⭐ **เลือกสำนวนตายตัวจากตาราง §3.0.5** · ⭐ **ไม่มีทางรับข้อความจากคน** | BR-16 · BR-17 · BR-28 · **IA-10** |
| **F-37** | `computeServiceLength(start_date, end_date)` | อายุงาน ปี–เดือน · ⭐ `end_date = last_working_day` เมื่อ `left` · `issue_date` เมื่ออื่น ๆ | FN-19 |
| **F-42** | `listCertificates(scope, filters, actor)` | รายการตามขอบเขตสิทธิ์ (พนักงานเห็นของตัวเอง · HR เห็นทั้งบริษัท) | FN-73 |
| **F-43** | `buildRegisterReadModel(filters)` | ⭐ **สร้างมุมมองที่เผยแพร่ตาม §0.13.2** — **ไม่ใส่จำนวนเงิน · ไม่ใส่ข้อความอิสระ · ไม่ใส่สายอนุมัติ** | §0.13.2 |
| **F-44** ⭐ | `assertNoFreeTextOnDocument()` | ⭐ **ตรวจเชิงโครงสร้างตอน build/test** — placeholder ทุกตัวต้อง map ไป field ของ snapshot หรือค่าคงที่ | BR-28 · **IA-14** |

## §3.1.6 กลุ่มเหตุการณ์ · งานเบื้องหลัง (F-38…F-41)

| # | Function | ทำอะไร | กฎ |
|---|---|---|---|
| **F-38** | `emitBusinessNotification(event_id, cert, vars)` | ยิง 7 NTF event · ⭐ **ห้ามใส่จำนวนเงินใน `vars`** · ⭐ **`cert_issued` ยิงหลัง `store()` สำเร็จเท่านั้น** | `05_RULES §5.9.1` |
| **F-39** | `emitSecurityEvent(event_id, payload)` | ยิง 5 SecC event · ⭐ **payload ไม่มีจำนวนเงิน — ส่งธง `has_salary_figure` แทน** | `05_RULES §5.9.2` · BR-26 |
| **F-40** | `registerWhereUsed()` | ลงทะเบียนกับต้นทาง 4 ตัว (bootstrap) · ⭐ **ไม่ใช่การเขียนข้อมูลของต้นทาง** | `SS-7` · `MV-6` · `OB-6` · `C-6` |
| **F-41** | `escalatePendingIssue(now)` | นาฬิกา T-10 — ใบ `approved` ค้างเกิน 3 วันทำการ → ยิง `cert_pending_issue_overdue` · ⭐ **ไม่ออกหนังสือให้เอง ไม่เปลี่ยนสถานะ** · idempotent (PR-7) | FN-62 · `OQ-CT-10` |

---

# §3.2 Engine Inventory (8 ตัว · **ใหม่ 4**)

> Iron Rules (CUBIC 3-layer): ⭐ **Engine ไม่รู้จัก HTTP** · **input/output เป็น object ล้วน** · **ค่านโยบายเป็น input เสมอ ไม่อยู่ข้างใน** · **feature เรียก Engine ผ่าน API ไม่เรียกตรง**

| # | Engine | สถานะ | Signature (แนวคิด) | ทำไมควรเป็น Engine |
|---|---|---|---|---|
| **ENG-01** ⭐⭐ | `certificate-fact-freeze-engine` | **candidate (NEW)** | `freeze({ facts_by_source, as_of, cert_type, language, policy }) → { snapshot, version_ids } \| { blocker }` | ⭐ **ตรรกะ "ยืนยันความจริง ณ วันหนึ่งแล้วตรึงไว้" ใช้ซ้ำได้กับทุกเอกสารที่ต้องรับรองข้อเท็จจริง** (ใบผ่านงาน · หนังสือรับรอง · เอกสารสำหรับหน่วยงานราชการ · ในอนาคตคือหนังสือรับรองของ Payroll) · ⭐ **ค่านโยบายเป็น input (`policy`) ไม่อยู่ข้างใน** |
| **ENG-02** ⭐⭐ | `document-rendition-selector` | **candidate (NEW)** | `select({ language, has_sensitive_figure, masked }) → rendition \| REFUSE` | ⭐ **กติกา "ไม่มี rendition ที่เว้นช่องข้อมูลอ่อนไหว" ควรอยู่ที่เดียว ไม่กระจายตามหน้าจอ** · ใช้ซ้ำได้กับ `F-HR-MOVE` (2 rendition `full`/`masked`) โดยเป็น superset |
| **ENG-03** ⭐ | `cert-action-selector` | **candidate (NEW)** | `pick({ cert_type }) → action_id` | ⭐ **ตระกูลเดียวกับ `movement-action-selector` ของ F-HR-MOVE** · ⭐ **signature ไม่มี field ที่รับจำนวนเงินหรือเปอร์เซ็นต์** — เป็นรูปแบบที่ควรทำให้เป็นมาตรฐานของทั้ง ERP |
| **ENG-04** | `supersede-chain-engine` | **candidate (NEW)** | `resolveChain({ doc_no }) → { chain: [doc_no…], head, tail }` | คลี่สายการแทนที่หลายทอด (A→B→C) · ⭐ **ใช้ร่วมกับ `movement-supersede-engine`** ที่ F-HR-MOVE เสนอไว้ — ควรพิจารณายุบเป็นตัวเดียว |
| **ENG-05** | `salary-structure-resolve-client` | existing | `resolve({ employee_id, date, company_id }) → RateSnapshot` | Reuse จาก F-HR-MOVE |
| **ENG-06** | `hr-config-resolve-client` | existing | `resolve({ date, company_id, group }) → ConfigValues` | Reuse — ⭐ **ต้องรองรับกรณี "ไม่มีกลุ่ม" เป็นค่าว่าง ไม่ใช่ error** |
| **ENG-07** | `document-render-engine` | existing | `render({ template_html, data }) → pdf` | Reuse — honor `@page` + ฟอนต์ฝังในไฟล์ |
| **ENG-08** | `doa-resolve-client` | existing | `resolve({ action_id, employee_id, company_id }) → Step[]` | Reuse — ⭐ **ไม่มี parameter ที่เป็นเงิน** |

> ⭐ **Engine ใหม่ทั้ง 4 ตัวไม่มีค่านโยบายอยู่ข้างใน** — `ENG-01` รับ `policy` เป็น input · `ENG-02` รับ 3 ธง · `ENG-03` รับ enum · `ENG-04` รับเลขที่เอกสาร
> ⭐ **`ENG-03` เป็นตัวที่ตรวจง่ายที่สุดว่าละเมิด LOCK-BAND หรือยัง** — ถ้าวันหนึ่ง signature มี field ที่เป็นตัวเลข นั่นคือสัญญาณว่าใครกำลังจะเอาเงินมาเป็นเกณฑ์แบ่งสาย

---

# §3.3 Function → API / Rule Trace

| Function | เรียกจาก | ผูกกับกฎ | ทดสอบที่ |
|---|---|---|---|
| F-01 · F-02 · F-03 | API-03 · API-04 · API-05 · API-16 | BR-01 · BR-22 · BR-27 | AT-01 · AT-14 · AT-65 · AT-93 |
| F-04 · F-05 | API-03 · API-04 · API-06 · API-07 | BR-06 | AT-05 · AT-28 · AT-29 · **IA-04** |
| F-06 · F-07 · F-12 | API-06 · API-07 | BR-04 · BR-05 · BR-07 · BR-08 | AT-26 · AT-27 · AT-30 · **IA-03 · IA-05** |
| F-08 | API-06 | BR-01 · BR-02 | AT-23 · AT-24 · AT-25 · **IA-06** |
| F-09 · F-10 · F-11 | API-06 · API-24 | VR-01…VR-14 · BR-25 | AT-09 · AT-12 · AT-13 |
| F-13 | API-06 | BR-01 · BR-04…BR-08 | AT-23 · AT-27 · AT-30 |
| F-14 · F-15 · F-16 | API-08 · API-09 · API-10 | BR-07 · VR-25 · VR-27 · VR-28 | AT-31 · AT-32 · AT-33 |
| F-17 · F-18 · F-19 | API-12 | BR-09 · BR-14 · VR-21 · VR-22 | AT-15 · AT-17 · **IA-08** |
| **F-20** | API-11 | **CI-1…CI-3** · BR-09 · BR-13 · BR-14 · BR-15 | AT-35 · AT-37 · AT-38 · AT-46 · **IA-01 · IA-02 · IA-08 · IA-09** |
| **F-21** | API-11 | BR-10 · BR-12 · BR-16 · BR-18 · **BR-27** | AT-39 · AT-41 · AT-42 · AT-45 · AT-93 · **IA-07 · IA-13** |
| F-22 · F-23 · ENG-02 · ENG-07 | API-11 · API-13 | BR-10 · BR-11 · BR-23 · BR-24 | AT-40 · AT-49 · AT-50 · AT-52 · **IA-07** |
| F-24 · F-25 | API-11 · API-14 · API-15 | BR-03 · BR-22 | AT-48 · AT-58 |
| **F-26** | API-11 | **CI-1…CI-9** | AT-35 · AT-36 · **IA-01 · IA-02 · IA-07** |
| F-27 · F-28 | API-13 · API-14 | BR-26 | AT-57 · AT-58 · AT-74 · AT-77 |
| F-29 · F-30 · F-31 · ENG-04 | API-15 · API-16 · API-11 | BR-22 · BR-23 | AT-67 · AT-68 · AT-69 · **IA-12** |
| F-32 · F-33 | (event listener) · API-28 | BR-19 · BR-23 | AT-71 · AT-72 · **IA-11** |
| F-34 · F-35 · F-42 · F-43 | API-19 · API-20 · API-01 · API-29 | BR-22 · §0.13.2 | AT-63 · AT-64 · AT-73 · AT-85 |
| **F-36 · F-37** | API-11 · API-12 · API-13 | BR-16 · BR-17 · **BR-28** | AT-19 · AT-21 · AT-43 · AT-44 · AT-96 · **IA-10** |
| F-38 · F-39 | (ทุกจุดที่มี event) | `05_RULES §5.9` | AT-59 · AT-60 · AT-77 |
| F-40 · F-41 | (bootstrap) · (นาฬิกา) | — | AT-62 · AT-86 |
| **F-44** | (build/test) | **BR-28** | AT-95 · **IA-14** |

**ตรวจ R8:** ทุก Function ถูก trace ✅ **44/44** · ทุก Engine ถูก trace ✅ **8/8** · ไม่มี orphan ✅ · ไม่มี `createX`/`updateX`/สูตรคำนวณ ซ่อนใน `02_API` ✅
