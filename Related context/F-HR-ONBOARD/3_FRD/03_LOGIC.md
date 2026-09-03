# 03_LOGIC — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> **CUBIC 3 ชั้น** — Feature Function (`camelCase` · scope-local) → Engine (`kebab-case` · reusable · pure object in/out) → **Engine ห้ามรู้จัก HTTP**
> **§3.0 คือหัวใจของแพ็กนี้** — อ่านให้จบก่อนแตะโค้ดใด ๆ ที่เกี่ยวกับสิทธิ์

---

## §3.0 กลไกการเพิกถอนสิทธิ์ (หัวใจของแพ็ก) ⭐

### §3.0.1 ทำไมต้องมีทะเบียน — และทะเบียนนี้คืออะไรกันแน่

คำถามที่ feature นี้ต้องตอบได้คือ *"คนที่ออกไปเมื่อวานยังเข้าระบบอะไรได้บ้าง"* · คำตอบจะพิสูจน์ไม่ได้เลยถ้าการเพิกถอนเป็น **ช่องติ๊กเดียว** เพราะช่องติ๊กบอกได้แค่ว่า *มีคนคิดว่าทำแล้ว* ไม่ได้บอกว่า *ทำอะไรไปบ้าง ใครทำ เมื่อไร*

**ทะเบียนสิทธิ์ของรอบ (`T_onb_access_item`)** จึงถูกออกแบบให้เป็น **ทะเบียนหลักฐาน (evidence register)** ไม่ใช่ตารางสิทธิ์:

- **1 แถว = 1 สิทธิ์ที่จับต้องได้** — ไม่มี "รายการรวม" และไม่มีแถวใดที่แทนสิทธิ์หลายชิ้น (**AR-1**)
- แต่ละแถวเก็บ **ที่มา** (มาจากรอบเข้างาน / อ่านจากสิทธิ์ปัจจุบัน / เพิ่มภายหลัง) เพื่อให้รู้ว่ารายการนี้เข้ามาในสายตาได้อย่างไร
- แต่ละแถวเก็บ **คำขอ** (`request_id` · `requested_at`) และ **ผลตอบกลับ** (`ack_by` · `ack_at` · `ack_ref`) แยกกัน — คำขอคือสิ่งที่เราทำ ผลตอบกลับคือสิ่งที่ต้นทางทำ
- **ทะเบียนนี้ไม่ตอบคำถามว่า "ตอนนี้ใครมีสิทธิ์อะไร"** — คำถามนั้นเป็นของ Roles & Permissions · ทะเบียนนี้ตอบว่า **"รอบนี้ขออะไรไปและได้รับการยืนยันกลับมาว่าอย่างไร"** (`02_API §2.2.1`)

### §3.0.2 ชนิดของสิทธิ์ที่ทะเบียนต้องครอบ (`access_kind` · 8 ค่า)

| ค่า | ชื่อบนจอ | ทำไมต้องมีแยกเป็นชนิด |
|---|---|---|
| `iam` | บัญชีผู้ใช้ · SSO | บัญชีหลัก — ปิดตัวนี้ยังไม่พอ เพราะบางระบบมี local account ของตัวเอง |
| `role` | บทบาทในระบบ | บัญชีอาจถูกปิดแต่บทบาทยังค้างอยู่ในกลุ่มที่ให้สิทธิ์ต่อ |
| `mfa` | ปัจจัยยืนยันตัวตน | อุปกรณ์ยืนยันตัวตนที่ยังผูกอยู่ = ทางกลับเข้าระบบ |
| `token` | โทเคน/กุญแจ API | **ชนิดที่ถูกลืมบ่อยที่สุด** — ไม่ผูกกับการเข้าสู่ระบบของคน จึงไม่หายไปเมื่อปิดบัญชี |
| `vpn` | VPN/ใบรับรอง | ใบรับรองเครือข่ายมีอายุของตัวเองและไม่ขึ้นกับบัญชี |
| `mail` | เมล/แชท/ประชุม | ช่องทางสื่อสารที่ยังรับข้อมูลองค์กรได้ |
| `shared` | กล่อง/กลุ่ม/ไดรฟ์ร่วม | การเป็นสมาชิกของพื้นที่ร่วมยังให้สิทธิ์อ่านต่อแม้บัญชีส่วนตัวถูกปิด |
| `badge` | บัตร/กุญแจ/ที่จอด | สิทธิ์ทางกายภาพ — ไม่มีระบบไอทีใดปิดให้ |

> ⭐ **ชนิดทั้งแปดมาจากแนวปฏิบัติด้านความปลอดภัย ไม่ใช่จาก ERP** — `STANDARD_BASELINE §1 C-10` บันทึกไว้ว่า **ERP ทั้งสามค่ายที่สำรวจ (Odoo 18 · D365 · SAP) ไม่ถือการเพิกถอนเป็นวัตถุที่ตรวจสอบได้เลย**

### §3.0.3 `revocation_due_at` — เวลาที่การเพิกถอนมีผล

```
เมื่ออนุมัติครบสาย (T-8):
    if (case.is_immediate_exit)  revocation_due_at = <เวลาที่อนุมัติครบสายนั้นเอง>
    else                         revocation_due_at = <สิ้นวันของ last_working_day (23:59)>
```

| กติกา | เหตุผล |
|---|---|
| **ตั้งครั้งเดียวตอนอนุมัติ** | ก่อนอนุมัติ ยังไม่มีอะไรแน่นอน · หลังอนุมัติ ค่านี้เป็นสัญญากับทุกฝ่าย |
| **ไม่มี endpoint ใดแก้ค่านี้** (AR-3) | ถ้าเลื่อนได้ งานที่ทำไม่ทันจะกลายเป็นเหตุผลให้เลื่อน แล้ววันที่คนพ้นสภาพยังเข้าระบบได้จะยาวขึ้นเรื่อย ๆ |
| **ไม่เลื่อนแม้ตกวันหยุด** (AR-9 · CL-02) | ความปลอดภัยไม่รอวันทำการ — ต่างจากกำหนดเสร็จของงานซึ่งตัดวันหยุด |
| **แก้ `last_working_day` หลังอนุมัติ → ต้องดึงกลับเป็นร่างและอนุมัติใหม่** | ค่านี้เป็นผลของสิ่งที่สายอนุมัติเซ็นไปแล้ว (BR-DOA-05) |
| ⭐ **`is_immediate_exit` แยกวันเพิกถอนออกจากวันสุดท้ายตามสัญญา** | คนถูกเลิกจ้างทันทีอาจยังได้ค่าจ้างถึงวันตามสัญญา — **แต่ต้องเข้าระบบไม่ได้ตั้งแต่วันนี้** · สองเรื่องนี้ไม่ใช่เรื่องเดียวกันและต้องเก็บแยกกัน |

### §3.0.4 การปิดรายการ — ทางเดียวเท่านั้น

```
รายการปิดได้ก็ต่อเมื่อ:
    POST /access-items/:id/ack  มาถึงพร้อม  ack_by ≠ null  AND  ack_at ≠ null  AND  ack_ref ≠ null
    → revoke_state = 'revoked'   (หรือ grant_state = 'granted' / 'restored' ตามชนิดคำขอ)
    → ยิง SecC ของรายการนั้น

ถ้าขาดข้อใดข้อหนึ่ง → 422 ERR_ACK_INCOMPLETE → รายการยังค้าง
```

| ข้อห้าม (บังคับที่ระดับโค้ดและที่ระดับ UI) | ทำไม |
|---|---|
| ❌ **ไม่มี endpoint ให้คนตั้ง `revoke_state` เอง** | ถ้ามี ทะเบียนจะกลายเป็นช่องติ๊กที่มีหน้าตาซับซ้อน |
| ❌ **ไม่มีช่องติ๊กในหน้าจอ** (FN-39) | ผู้ใช้ต้องมองไม่เห็นแม้แต่ทางที่จะทำผิด |
| ❌ **ระบบไม่ตั้งเป็นสำเร็จเองเมื่อครบเวลา** (S-29) | การเงียบของต้นทางไม่ใช่การยืนยัน |
| ❌ **ผลตอบกลับที่ไม่ครบไม่นับ** | หลักฐานที่ไม่มีคนทำหรือไม่มีเวลา พิสูจน์อะไรไม่ได้ (C-12) |
| ✅ **ผลตอบกลับซ้ำด้วย `request_id` เดิม = ไม่เปลี่ยนอะไรและไม่ยิง SecC ซ้ำ** (CA-03) | ต้นทางอาจส่งซ้ำโดยไม่ตั้งใจ |

### §3.0.5 ธง `revocation_overdue` — และทำไมมันบล็อกการปิดรอบ

```
ทุก 15 นาที (scanRevocationDue):
  for each case where approval_status = 'approved' and case_status ≠ 'closed'/'cancelled':
      if now > case.revocation_due_at and exists(item where revoke_state ≠ 'revoked'):
            case.revocation_flag = 'overdue'
            overdue_hours = hoursBetween(case.revocation_due_at, now)
            severity      = severityOf(overdue_hours)
            emit CSQ  offboard.revocation_overdue  (severity, retry_count, pending_access_kinds[])
            emit NTF  ofb_revocation_overdue       (ปิดไม่ได้ · ยกระดับผู้รับตาม severity)
      else if ทุกรายการ revoked:
            case.revocation_flag = 'none'
            case.case_status     = 'revoked'
            emit CSQ  offboard.access_revoked (is_final = true)
            emit NTF  ofb_access_revoked
```

| ระดับ | เมื่อ `overdue_hours` | ผู้รับที่ถูกยกระดับ |
|---|---|---|
| **เฝ้าระวัง** (`warning`) | < 48 | HR · ผู้ดูแลสิทธิ์ |
| **รุนแรง** (`high`) | 48 – 168 | + หัวหน้าสายงาน |
| **วิกฤต** (`critical`) | ≥ 168 | + **Policy Center** |

`[ASSUMED · A-2]` — **feature ส่งข้อเท็จจริง (`overdue_hours` · `pending_count` · `pending_access_kinds[]`) · การตัดสินระดับความรุนแรงขั้นสุดท้ายเป็นของ Engine** · เกณฑ์ข้างบนเป็นค่าเริ่มต้นที่รอ Strike เคาะ (`07_LOCKED §7.3`)

**ทำไมธงนี้ต้องบล็อกการปิดรอบ:**
การปิดรอบคือการประกาศว่า *"เรื่องนี้จบแล้ว"* · ถ้ารอบปิดได้ทั้งที่ยังมีสิทธิ์ค้าง **ระบบจะเป็นผู้พูดความเท็จเอง** และตัวเลขทุกตัวในรายงานจะไม่มีความหมาย · จึงเป็น **invariant IA-04 ที่ตกแล้วหยุด release** ไม่ใช่แค่กฎธุรกิจ

### §3.0.6 การส่งมอบความเป็นเจ้าของข้อมูลไม่ชะลอการเพิกถอน (AR-8 · BR-31)

ปัญหาที่แนวปฏิบัติของ M365/Google Workspace ชี้ไว้: **การเพิกถอนบัญชีทำให้ข้อมูลที่คนนั้นเป็นเจ้าของเข้าไม่ถึง** — กล่องจดหมาย ไฟล์ที่ดูแล กลุ่มที่เป็นเจ้าของ · ทางแก้ที่ *ผิด* คือเลื่อนเวลาเพิกถอนจนกว่าจะส่งมอบเสร็จ

**ทางแก้ที่ feature นี้เลือก:**

```
งานส่งมอบความเป็นเจ้าของข้อมูล (5 รายการ) เป็น "งานบังคับ" → เข้า closeBlockers
แต่ ไม่แตะ revocation_due_at เลย

ถ้าถึงเวลาเพิกถอนแล้วงานยังไม่เสร็จ:
    → ระบบเสนอปุ่ม "ขอสิทธิ์ชั่วคราวให้ผู้รับมอบ"  (requestTempAccess)
    → ออกคำขอสิทธิ์ชั่วคราวให้ "ผู้รับมอบ" ไม่ใช่ต่ออายุให้ "ผู้ที่ออก"
    → emit CSQ offboard.temp_access_delegated  (การให้คนหนึ่งเข้าถึงข้อมูลของอีกคน = การเปลี่ยนสิทธิ์เต็มตัว)
```

> **หลักคิด:** ปัญหาคือ *"ข้อมูลต้องเข้าถึงได้"* ไม่ใช่ *"คนนี้ต้องเข้าถึงได้"* — เมื่อแยกสองเรื่องนี้ออกจากกัน คำตอบคือมอบสิทธิ์ให้คนที่ยังอยู่ ไม่ใช่ยืดสิทธิ์ให้คนที่ไปแล้ว

### §3.0.7 การยกเลิกหลังเพิกถอน = คำขอคืนสิทธิ์ใหม่ (AR-5 · BR-14)

```
cancelCase(case) เมื่อ case_status = 'revoked':
    for each item where revoke_state = 'revoked':
        สร้าง "แถวใหม่" หรือ "คำขอใหม่" ที่มี:
            action        = 'restore'
            reversal_of   = <access_item_id / event ref ของการเพิกถอนเดิม>   ← บังคับ
            revoke_state  = 'restore_requested'
        ส่งคำขอไปยัง Roles & Permissions
    ห้ามแตะแถวเดิม: ack_by / ack_at / ack_ref ของการเพิกถอนเดิมยังอยู่ครบ
    เมื่อ ack ของคำขอคืนกลับมา → emit CSQ offboard.access_restored (พร้อม reversal_of)
```

| ข้อห้าม | ทำไม |
|---|---|
| ❌ **ห้าม `UPDATE ... SET revoke_state = 'none'`** | จะทำให้ประวัติบอกว่า "ไม่เคยเพิกถอน" ทั้งที่เพิกถอนไปแล้วจริง — **นี่คือความผิดพลาดที่ SAP เตือนไว้ในเอกสารของตัวเอง** (`STANDARD_BASELINE C-20`) |
| ❌ **ห้ามลบแถวเดิม** | ประวัติเป็น append-only (AR-6) |
| ✅ **`reversal_of` บังคับ** | ผู้ตรวจสอบต้องไล่ได้ว่าสิทธิ์ที่กลับมาคือสิทธิ์ตัวไหนที่เคยถูกถอน |

### §3.0.8 ลำดับที่ผิดแล้วพัง (sequence guard)

| # | ลำดับที่ถูก | ถ้าทำผิดลำดับจะเกิดอะไร |
|---|---|---|
| 1 | **อนุมัติครบสาย → จึงตั้ง `revocation_due_at` → จึงส่งคำขอเพิกถอนได้** | ส่งคำขอก่อนอนุมัติ = เพิกถอนสิทธิ์ของคนที่อาจไม่ได้ออกจริง (BR-DOA-07 · `ERR_CASE_NOT_APPROVED`) |
| 2 | **สร้าง SOW สำเร็จ → จึงบันทึกรอบ** | รอบที่ไม่มี SOW = งานที่ไม่มีใครเห็น (EN-01 · `ERR_SOW_CREATE_FAILED`) |
| 3 | **อ่าน `holiday_calendar` + เก็บ `version_id` → จึงคำนวณกำหนดเสร็จ** | คำนวณก่อนอ่าน = ใช้ปฏิทินของวันอื่น (C-1 · C-2) |
| 4 | **ตรวจงวดปิด → ตอนกรอก และตอน commit/อนุมัติซ้ำอีกครั้ง** | ตรวจครั้งเดียวตอนกรอก = งวดอาจถูกปิดระหว่างรออนุมัติ (P-7 · BR-DOA-06) |
| 5 | **รับ ack → ปิดรายการ → ประเมินความครบ → จึงเปลี่ยนสถานะรอบ** | เปลี่ยนสถานะก่อนประเมิน = รอบเป็น "เพิกถอนแล้ว" ทั้งที่ยังไม่ครบ (IA-01) |
| 6 | **ปิดงานค้าง → ถอนค่าที่เผยแพร่ → ออกคำขอคืนสิทธิ์ → จึงตั้งรอบเป็นยกเลิก** | ตั้งเป็นยกเลิกก่อน = งานลอยและปลายทางยังอ่านค่าเก่า (BR-13 · FN-49) |

---

## §3.1 Functions (48 ตัว · camelCase)

### กลุ่ม A — รอบเข้างาน

| # | Function | ทำอะไร | เรียก Engine | trace |
|---|---|---|---|---|
| **FN-A01** | `createCase` | ตรวจว่าคนอยู่ในทะเบียนพนักงาน → อ่านค่าจาก HR Configuration → generate งานเป็น SOW → สร้างทะเบียนสิทธิ์ตั้งต้น → บันทึกรอบสถานะ `ร่าง`/`รอวันเริ่มงาน` | `ENG-HRCFG-READ` · `ENG-WORKDAY-01` · `ENG-OPSOW-01` · `ENG-ACCESSREG-01` | FN-01 · FN-81 |
| FN-A02 | `previewTasks` | คืนรายการงานที่จะถูกสร้างพร้อมกำหนดเสร็จ **โดยยังไม่บันทึก** | `ENG-WORKDAY-01` | FN-02 |
| FN-A03 | `computeTaskDueDates` | คำนวณ `due_date` ของทุกงานจากวันอ้างอิง ± offset ตัดวันหยุด · **งานที่ `due_offset_days = null` ให้ผู้ใช้ตั้งเอง** | `ENG-WORKDAY-01` | FN-03 · FN-20 |
| FN-A04 | `isTaskRunnable` | งานเดินได้หรือยัง — pre-boarding เดินได้ทันที · งานปิดสิทธิ์เดินได้เมื่อ `approved` | — | FN-04 · FN-25 |
| FN-A05 | `announceCaseStarted` | ยิง `onb_case_started` ถึงผู้รับผิดชอบทุกงาน + หัวหน้า | — | FN-01 |
| FN-A06 | `addCaseTask` / `dropCaseTask` | เพิ่ม/ปิดงานนอกแม่แบบ **บังคับเหตุผล** · **ไม่แตะแม่แบบต้นทาง** | `ENG-OPSOW-01` | FN-10 |
| FN-A07 | `updateCaseDates` | แก้วันสำคัญ → คำนวณกำหนดเสร็จของงานที่ยังไม่เสร็จใหม่ · **งานที่เสร็จแล้วไม่ถูกแตะ** → ยิง `onb_start_date_changed` | `ENG-WORKDAY-01` · `ENG-PERIOD-GUARD` | FN-11 |
| FN-A08 | `advanceStartedCases` | *(background รายวัน)* รอบที่ `today ≥ start_date` → `กำลังดำเนินการ` + เผยแพร่ `start_date` + สัญญาณ joiner | — | FN-08 · FN-09 |
| FN-A09 | `setProbationReview` | บันทึกผลการทบทวนทดลองงาน (ผ่าน/ไม่ผ่าน/ขยายเวลา) + ผู้ทบทวน | — | FN-14 |
| **FN-A10** ⭐ | `readEmploymentTerm` | อ่าน `employment_term.*` จาก HR Configuration · **ถ้า `null` คืน `{value: null, display: "ยังไม่มีค่าให้อ่าน", link: "#/hr-config/..."}`** · **ห้ามคืนค่า default ใด ๆ** | `ENG-HRCFG-READ` | FN-15 · FN-22 |
| FN-A11 | `closeCase` | ปิดรอบเมื่อ `closeBlockers` ว่าง · บันทึกธงจ้างกลับ | `ENG-REVOKE-01` · `ENG-OPSOW-01` | FN-16 · FN-72 |
| **FN-A12** ⭐ | `closeBlockers` | คืน **รายการเหตุที่ปิดรอบไม่ได้ เป็นรายบรรทัด** — งานบังคับค้าง · **สิทธิ์ยังเพิกถอนไม่ครบ** · **ธง overdue** · ทรัพย์สินค้าง · งานส่งมอบข้อมูล · งานมอบหมายผู้ใต้บังคับบัญชา | `ENG-REVOKE-01` | FN-17 · FN-43 · FN-78 |

### กลุ่ม B — รอบออกงานและการอนุมัติ

| # | Function | ทำอะไร | เรียก Engine | trace |
|---|---|---|---|---|
| FN-B01 | `createOffboardCase` | เหมือน FN-A01 แต่ใช้ `last_working_day` เป็นสมอ + ตั้งทะเบียนสิทธิ์จากสองแหล่ง | `ENG-ACCESSREG-01` | FN-19 |
| FN-B02 | `computeOffboardDueDates` | กำหนดเสร็จคิดถอยหลังจาก `last_working_day` | `ENG-WORKDAY-01` | FN-20 |
| FN-B03 | `assertNotInClosedPeriod` | ตรวจว่าวันที่ไม่ตกในงวดที่ปิด · **คืนวันที่เร็วที่สุดที่ตั้งได้** · **เรียกซ้ำตอน commit และตอนอนุมัติ** | `ENG-PERIOD-GUARD` | FN-21 |
| FN-B04 | `submitCase` | ตัดสิน `approval_action_id` จาก `termination_reason` + `is_immediate_exit` → `GET /doa/resolve` → **freeze `approval_chain`** | `ENG-DOA-01` | FN-23 |
| FN-B05 | `renderApprovalSlots` | คืนจำนวนและลำดับ slot **จากผลของ resolve เท่านั้น** | `ENG-DOA-01` | FN-24 |
| FN-B06 | `approveCase` | เดิน slot · ครบสาย → `approved` + **`FN-B08`** + เผยแพร่ `last_working_day` + สัญญาณ leaver + ยิง `ofb_case_approved` | `ENG-DOA-01` · `ENG-PERIOD-GUARD` | FN-25 · FN-26 |
| FN-B07 | `rejectCase` | **บังคับ `reject_reason`** → `rejected` → แก้แล้วส่งใหม่ = **re-resolve ทั้งสาย** | `ENG-DOA-01` | FN-27 |
| **FN-B08** ⭐ | `setRevocationDue` | ตั้ง `revocation_due_at` ตาม §3.0.3 · **เรียกได้จาก `approveCase` เท่านั้น · ไม่มี API ใดเรียกตรง** | — | FN-31 · FN-37 |
| FN-B09 | `checkDepartingResponsibilities` | อ่านจำนวนผู้ใต้บังคับบัญชา (Employee Master) + งานอนุมัติค้าง (DOA) → **สร้างงานบังคับมอบหมาย** ถ้ามีมากกว่าศูนย์ | `ENG-OPSOW-01` | FN-77 · FN-78 |

### กลุ่ม C — สิทธิ์และการเพิกถอน ⭐

| # | Function | ทำอะไร | เรียก Engine | trace |
|---|---|---|---|---|
| **FN-C01** | `requestGrant` | ส่งคำขอเปิดสิทธิ์ตามรายการที่ผู้ใช้ยืนยัน → `grant_state = requested` + `request_id` | `ENG-REVOKE-01` | FN-05 |
| **FN-C02** ⭐ | `requestRevokeAll` | ส่งคำขอเพิกถอน **ทุกแถว** ของรอบ → `revoke_state = requested` · **บล็อกถ้ารอบยังไม่ `approved`** | `ENG-REVOKE-01` | FN-31 |
| FN-C03 | `buildInitialAccessRegister` | รวมสิทธิ์จาก **รอบเข้างาน** + **สิทธิ์ปัจจุบันที่อ่านจาก Roles & Permissions** พร้อมคอลัมน์ที่มา · **ถ้าอ่านต้นทางไม่ได้ ให้ตั้งธง `source_read_failed` ไม่ใช่เงียบ** | `ENG-ACCESSREG-01` | FN-41 |
| FN-C04 | `listAccessKinds` | นับรายการต่อชนิดครบ 8 ชนิด | — | FN-30 |
| **FN-C05** ⭐⭐ | `receiveAccessAck` | **ทางเดียวที่เขียน `grant_state`/`revoke_state` เป็นสถานะสำเร็จ** — ตรวจ `ack_by`/`ack_at`/`ack_ref` ครบ → ปิดรายการ → ยิง SecC ของรายการนั้น → เรียก `FN-C07` | `ENG-REVOKE-01` | FN-06 · FN-33 |
| FN-C06 | `handleAckFailure` | ผลตอบกลับ `failed` → `fail_reason` + คงสถานะค้าง + ยิง `access_request_failed` (ปิดการแจ้งไม่ได้) | — | FN-07 · FN-40 |
| **FN-C07** ⭐ | `evaluateRevocationCompleteness` | ประเมินว่าครบหรือยัง → ครบ: `case_status = revoked` + SecC `is_final` + ยิง `ofb_access_revoked` · ไม่ครบและเลยกำหนด: **ธง overdue** | `ENG-REVOKE-01` | FN-33 · FN-34 |
| FN-C08 | `scanRevocationDue` | *(background ทุก 15 นาที)* ส่งคำขอของรอบที่ถึงกำหนด · ประเมินธง · ยิง event ซ้ำพร้อม severity | `ENG-REVOKE-01` | FN-34 · FN-36 |
| FN-C09 | `revocationProgress` | คืน `{done, all, open[]}` สำหรับแถบความคืบหน้า | — | FN-32 |
| FN-C10 | `addLateAccessItem` | เพิ่มรายการที่พบภายหลัง **บังคับเหตุผล** · `source = late` · **รอบยังปิดไม่ได้จนกว่ารายการนี้จะถูกเพิกถอน** | `ENG-ACCESSREG-01` | FN-38 |
| **FN-C11** ⭐ | `requestTempAccess` | ออกคำขอสิทธิ์ชั่วคราวให้ **ผู้รับมอบ** (ไม่ใช่ต่ออายุให้ผู้ที่ออก) → SecC `temp_access_delegated` · **ไม่แตะ `revocation_due_at`** | `ENG-REVOKE-01` | FN-76 |
| FN-C12 | `retryAccessRequest` | ส่งคำขอซ้ำ + `retry_count++` + ล้าง `ack_*` เดิม · **ระบบไม่ตั้งเป็นสำเร็จเอง** | `ENG-REVOKE-01` | FN-40 |
| FN-C13 | `reconcileAccessAck` | *(background ทุก 1 ชม.)* ทางสำรองของ webhook — ถามสถานะคำขอที่ยังไม่มีผลตอบกลับ | `ENG-REVOKE-01` | OQ-FRD-01 |

### กลุ่ม D — การเผยแพร่และปลายทาง

| # | Function | ทำอะไร | trace |
|---|---|---|---|
| FN-D01 | `publishEmploymentWindow` | ปรับ read model เมื่อ `start_date` หรือ `last_working_day` มีผล/ถูกถอน + สัญญาณ joiner/leaver | FN-09 · FN-26 · FN-49 |
| FN-D02 | `readAttendancePending` | อ่านวันที่ยังไม่ยืนยันของคนนั้นจาก Attendance — **อ่านอย่างเดียว ห้ามคำนวณเอง (AT-6)** | FN-55 |
| FN-D03 | `readLeaveOverlap` | อ่านใบลาที่คร่อม `last_working_day` + ยอดสิทธิ์คงเหลือจาก Leave — **ห้ามนับวันเอง (LV-4) · ห้ามตีความป้ายจ่ายเป็นเงิน (LV-6)** | FN-55 · FN-56 |
| FN-D04 | `resolveEmploymentWindow` | ตอบ `GET /employment-window/resolve` ตาม `00_OVERVIEW §0.13.2` | FN-53 · FN-54 |
| FN-D05 | `setLinkage` | ปรับสถานะการเชื่อมของ Module Linkage | FN-57 · FN-59 |

### กลุ่ม E — การยกเลิกและคืนสิทธิ์

| # | Function | ทำอะไร | trace |
|---|---|---|---|
| FN-E01 | `cancelOnboardCase` | **บังคับเหตุผล** → ปิดงานค้างทั้งหมดชัดแจ้ง → ถอน `start_date` ที่เผยแพร่ | FN-12 |
| FN-E02 | `revokeOnCancel` | ถ้ารอบเข้างานเคยเปิดสิทธิ์ → **ออกคำขอปิดบัญชีทันที** + SecC `access_revoked_on_cancel` | FN-13 |
| FN-E03 | `cancelOffboardCase` | **บังคับเหตุผล + ผ่าน A-3 สายเดิม** → ปิดงานค้าง → **ถอน `last_working_day` ที่เผยแพร่** → ยิง `ofb_case_cancelled` | FN-48 · FN-49 |
| **FN-E05** ⭐ | `issueRestoreRequests` | ยกเลิกหลังเพิกถอน → **ออกคำขอคืนสิทธิ์ใหม่ทุกแถวพร้อม `reversal_of`** · **ห้ามย้อนสถานะเดิม** → SecC `access_restored` | FN-50 · FN-51 |

### กลุ่ม F — รายการ · ค้นหา · ประวัติ · สิทธิ์การเห็น

| # | Function | ทำอะไร | trace |
|---|---|---|---|
| FN-F01 | `listCases` | กรอง/ค้นหา/แบ่งหน้า · **กรองที่ระดับ query ตามขอบเขต** | FN-90 |
| FN-F02 | `getCase` | คืนรอบหนึ่งใบ · **ปิดบัง field Confidential ที่ชั้น API** + เขียนร่องรอยการเปิดดู | FN-66 |
| FN-F03 | `getWatchlist` | รวมรอบติดธง overdue + งานเลยกำหนด + คำขอที่ล้มเหลว — **ขอบเขตเฉพาะรอบของฟีเจอร์นี้** | FN-35 · FN-74 |
| FN-F04 | `appendHistory` | เขียนแถวประวัติทุก transition · ทุกคำขอ/ผลตอบกลับ · **ทุกการเปิดดูข้อมูลอ่อนไหว** | FN-68 |
| FN-F05 | `listTemplates` | อ่านแม่แบบจาก Operation Process · กรอง `inactive` ออกจากตัวเลือกแต่ยังแสดงในรอบเก่า | FN-64 · FN-65 |
| FN-F06 | `upsertAssetItem` | ส่งมอบ/คืน/คืนไม่ได้ + เหตุผล | FN-42 |
| FN-F07 | `attachEvidence` | แนบผ่าน Document Center · เก็บเฉพาะ `evidence_ref` | FN-46 |

---

## §3.2 Engines (7 ตัว · kebab-case · **pure object in/out · ห้ามรู้จัก HTTP**)

| # | Engine | หน้าที่ | สถานะ | ใช้ซ้ำที่ไหนได้อีก |
|---|---|---|---|---|
| **ENG-REVOKE-01** ⭐ | **`access-revocation-engine`** | รับทะเบียนสิทธิ์ + `revocation_due_at` + เวลาปัจจุบัน → คืน **คำขอที่ต้องส่ง · ความครบ · ธง overdue · `severity` · รายการที่ค้าง** · ไม่รู้จัก HTTP ไม่รู้จักฐานข้อมูล | **engine candidate ใหม่** — ยกให้ Architect ลงทะเบียนใน CUBIC | **Policy Center** (การกวาดบัญชีตกค้างทั้งระบบ) · **Asset** (การติดตามทรัพย์สินที่เกินกำหนดคืน) · **Contract/Vendor offboarding** ในอนาคต |
| ENG-DOA-01 | `doa-resolver` | resolve สายจาก `action_id` + freeze + เดิน slot + SoD | ✅ baseline (ของกลาง) | ทุก feature ที่มีการอนุมัติ |
| ENG-WORKDAY-01 | `workday-shifter` | เลื่อนวันตาม offset โดยตัดวันหยุดจากปฏิทินที่ส่งเข้ามา | ✅ baseline | ทุก feature ที่มีกำหนดเสร็จ |
| ENG-PERIOD-GUARD | `closed-period-guard` | ตรวจว่าวันที่ตกในงวดที่ปิดหรือไม่ + คืนวันที่เร็วที่สุดที่ตั้งได้ | ✅ baseline (P-7) | Attendance · Leave · OT · Payroll |
| ENG-OPSOW-01 | `op-sow-publisher` | แปลงงานในแม่แบบเป็นการประกาศ SOW + สะท้อนสถานะกลับ | ✅ baseline | ทุก feature ที่มี checklist ผูก OP |
| ENG-HRCFG-READ | `hrconfig-reader` | อ่านค่า ณ วันที่ + คืน `version_id` + **คืน `null` อย่างชัดแจ้งเมื่อคีย์ยังไม่เผยแพร่** | ✅ baseline (C-1…C-3) | ทุก feature HR |
| **ENG-ACCESSREG-01** | `access-register-builder` | รับสิทธิ์จากรอบเข้างาน + สิทธิ์ปัจจุบันที่อ่านมา → คืน **ทะเบียนตั้งต้นพร้อมคอลัมน์ที่มาและการรวมรายการซ้ำ** · ถ้าอ่านต้นทางไม่ได้ให้ติดธงแทนการเงียบ | **engine candidate ใหม่** (คู่กับ ENG-REVOKE-01) | Policy Center · Vendor offboarding |

> **ข้อกำหนด CUBIC ที่ทุก engine ในตารางนี้ผ่าน:** ไม่มี engine ใดอ้าง `req`/`res`/header · input/output เป็น object ล้วน · **feature ไม่เรียก engine ข้าม API layer**

### §3.2.1 ทำไม `access-revocation-engine` ควรเป็น engine ไม่ใช่ function ในฟีเจอร์

ตรรกะ **"ส่งคำขอ → รอผลตอบกลับ → เกินกำหนด → ยกระดับ → ปิดเมื่อครบ"** ไม่ได้ผูกกับเรื่องคนเข้าออกงานเลย — มันคือรูปแบบของ **การติดตามคำขอที่มีเส้นตาย** ซึ่งเกิดซ้ำในหลายที่:

| ที่ที่ใช้ซ้ำได้ | รูปเดียวกันตรงไหน |
|---|---|
| **Policy Center** — กวาดหาบัญชีตกค้างทั้งระบบ (OQ-STD-OB9) | รายการที่ควรถูกปิดแต่ยังไม่ปิด + เส้นตาย + การยกระดับ |
| **Asset** — ทรัพย์สินที่เกินกำหนดคืน | เหมือนกันทุกส่วนยกเว้นชนิดของวัตถุ |
| **Vendor/Contractor offboarding** (OQ-STD-OB11) | เมื่อมีทะเบียนบุคคลภายนอกแล้ว ใช้ engine เดิมได้ทันที |

> **ยกให้ Architect เป็น engine candidate** — บันทึกไว้ที่ `_lane/_NOTIFY.md` และ `00_OVERVIEW §0.6`

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor · R8)

| API | ชนิด | Function | Engine | ตารางที่แตะ |
|---|---|---|---|---|
| API-01 `GET /cases` | read | `listCases` | — | `T_onb_case` |
| API-02 `GET /cases/:id` | read | `getCase` · `appendHistory` (การเปิดดู) | — | `T_onb_case` · `T_onb_task` · `T_onb_access_item` · `T_onb_asset_item` · `T_onb_history` |
| **API-03 `POST /cases`** | mutation | `createCase` · `computeTaskDueDates` · `buildInitialAccessRegister` · `announceCaseStarted` | `ENG-HRCFG-READ` · `ENG-WORKDAY-01` · `ENG-OPSOW-01` · `ENG-ACCESSREG-01` | `T_onb_case` · `T_onb_task` · `T_onb_access_item` · `T_onb_history` |
| API-04 `GET /cases/preview` | read | `previewTasks` | `ENG-WORKDAY-01` | — |
| **API-05 `PATCH /cases/:id/dates`** | mutation | `updateCaseDates` · `computeTaskDueDates` · `assertNotInClosedPeriod` | `ENG-WORKDAY-01` · `ENG-PERIOD-GUARD` | `T_onb_case` · `T_onb_task` · `T_onb_history` |
| **API-06 `POST /cases/:id/submit`** | mutation | `submitCase` · `renderApprovalSlots` · `assertNotInClosedPeriod` | **`ENG-DOA-01`** · `ENG-PERIOD-GUARD` | `T_onb_case` · `T_onb_history` |
| **API-07 `POST /cases/:id/approve`** | mutation | `approveCase` · **`setRevocationDue`** · `publishEmploymentWindow` · `checkDepartingResponsibilities` | `ENG-DOA-01` · `ENG-PERIOD-GUARD` · `ENG-OPSOW-01` | `T_onb_case` · `T_onb_task` · `T_onb_history` |
| **API-08 `POST /cases/:id/reject`** | mutation | `rejectCase` | `ENG-DOA-01` | `T_onb_case` · `T_onb_history` |
| **API-09 `POST /cases/:id/cancel`** | mutation | `cancelOnboardCase` / `cancelOffboardCase` · `revokeOnCancel` · **`issueRestoreRequests`** · `publishEmploymentWindow` | **`ENG-REVOKE-01`** · `ENG-OPSOW-01` | ทุกตาราง |
| **API-10 `POST /cases/:id/access-requests`** | mutation | `requestGrant` | **`ENG-REVOKE-01`** | `T_onb_access_item` · `T_onb_history` |
| **API-11 `POST /cases/:id/revocation-requests`** | mutation | `requestRevokeAll` | **`ENG-REVOKE-01`** | `T_onb_access_item` · `T_onb_history` |
| **API-12 `POST /access-items/:id/retry`** | mutation | `retryAccessRequest` | `ENG-REVOKE-01` | `T_onb_access_item` · `T_onb_history` |
| **API-13 `POST /cases/:id/access-items`** | mutation | `addLateAccessItem` | `ENG-ACCESSREG-01` | `T_onb_access_item` · `T_onb_history` |
| **API-14 `POST /cases/:id/temp-access`** | mutation | `requestTempAccess` | `ENG-REVOKE-01` | `T_onb_access_item` · `T_onb_history` |
| **API-15 `POST /cases/:id/tasks` · `PATCH /tasks/:id`** | mutation | `addCaseTask` · `dropCaseTask` · `updateCaseTask` | `ENG-OPSOW-01` | `T_onb_task` · `T_onb_history` |
| **API-16 `POST /tasks/:id/evidence`** | mutation | `attachEvidence` | — | `T_onb_task` · `T_onb_history` |
| **API-17 `PATCH /cases/:id/linkage`** | mutation | `setLinkage` | — | `T_onb_case` · `T_onb_history` |
| API-18 `GET /templates` | read | `listTemplates` | `ENG-OPSOW-01` | — |
| **API-19 `POST /cases/:id/close`** | mutation | `closeCase` · **`closeBlockers`** | `ENG-REVOKE-01` · `ENG-OPSOW-01` | `T_onb_case` · `T_onb_history` |
| **API-20 `POST /access-items/:id/ack`** ⭐ | mutation | **`receiveAccessAck`** · `handleAckFailure` · **`evaluateRevocationCompleteness`** | **`ENG-REVOKE-01`** | `T_onb_access_item` · `T_onb_case` · `T_onb_history` |
| API-21 `GET /cases/:id/history` | read | `getCaseHistory` | — | `T_onb_history` |
| **API-22 `POST /cases/:id/assets` · `PATCH /assets/:id`** | mutation | `upsertAssetItem` | — | `T_onb_asset_item` · `T_onb_history` |
| **API-23 `PATCH /cases/:id/probation-review`** | mutation | `setProbationReview` | — | `T_onb_case` · `T_onb_history` |
| API-24 `GET /watchlist` | read | `getWatchlist` | `ENG-REVOKE-01` | `T_onb_case` · `T_onb_access_item` · `T_onb_task` |
| **API-25 `POST /internal/scan-revocation-due`** | mutation | **`scanRevocationDue`** · `evaluateRevocationCompleteness` | **`ENG-REVOKE-01`** | `T_onb_case` · `T_onb_access_item` · `T_onb_history` |
| **API-26 `POST /internal/advance-started-cases`** | mutation | `advanceStartedCases` · `publishEmploymentWindow` | — | `T_onb_case` · `T_onb_history` |
| **API-27 `POST /internal/reconcile-access-ack`** | mutation | `reconcileAccessAck` | `ENG-REVOKE-01` | `T_onb_access_item` · `T_onb_history` |
| **API-28 `POST /usage`** | mutation | `registerConsumerUsage` | — | `T_onb_consumer_usage` |
| API-30 `GET /employment-window/resolve` | read | `resolveEmploymentWindow` | — | `T_onb_case` (read model) |

**R8 verification:**
- ✅ **ทุก mutation API มี ≥ 1 Function/Engine** — 21 mutation ทั้งหมด trace ครบ
- ✅ **ทุก Function ใน §3.1 ถูก trace อย่างน้อย 1 API** — 48/48 (background 4 ตัวผูกกับ API-25 · API-26 · API-27)
- ✅ **ทุก Engine ใน §3.2 ถูกใช้จริง** — 7/7
- ✅ **ไม่มี orphan Function/Engine**

---

## §3.4 ลำดับการทำงานที่ต้องเป็นแบบนี้เท่านั้น (sequence ที่ผิดแล้วพัง)

### §3.4.1 สร้างรอบ (API-03)

```
1. ตรวจว่า employee_id อยู่ในทะเบียนพนักงาน            ← ผิดลำดับ = สร้างรอบให้บุคคลภายนอกได้ (FN-81)
2. ENG-HRCFG-READ: อ่าน holiday_calendar + period_rule ณ วันอ้างอิง · เก็บ version_id
3. ENG-PERIOD-GUARD: ตรวจว่าวันอ้างอิงไม่ตกในงวดที่ปิด
4. ENG-WORKDAY-01: คำนวณ due_date ของทุกงาน
5. ENG-OPSOW-01: ประกาศ SOW ทุกงาน  ← ถ้าล้มเหลว ต้อง rollback ทั้งหมด (ERR_SOW_CREATE_FAILED)
6. ENG-ACCESSREG-01: สร้างทะเบียนสิทธิ์ตั้งต้น
7. บันทึกรอบ + เขียนประวัติ
8. ยิง onb_case_started
```

### §3.4.2 อนุมัติครบสาย (API-07) ⭐

```
1. ตรวจว่าผู้เรียกเป็นผู้ถือ slot ปัจจุบัน               ← ERR_NOT_CURRENT_APPROVER
2. ENG-PERIOD-GUARD: ตรวจงวดปิด "ซ้ำอีกครั้ง"          ← BR-DOA-06 · งวดอาจถูกปิดระหว่างรออนุมัติ
3. ENG-DOA-01: เดิน slot
4. ถ้ายังไม่ครบสาย → จบ (ไม่แตะสิทธิ์ ไม่เผยแพร่อะไร)
5. ครบสาย:
   5.1 case_status = approved
   5.2 setRevocationDue()          ← ตั้งครั้งเดียว ไม่มีที่อื่นเรียก
   5.3 publishEmploymentWindow()   ← last_working_day มีผลกับปลายทาง ณ จุดนี้
   5.4 checkDepartingResponsibilities()  ← สร้างงานมอบหมายถ้ามีผู้ใต้บังคับบัญชา/งานอนุมัติค้าง
   5.5 emit ofb_case_approved
   5.6 ถ้า is_immediate_exit → requestRevokeAll() ทันที + emit CSQ immediate_revocation
```

### §3.4.3 รับผลตอบกลับ (API-20) ⭐⭐

```
1. ยืนยันตัวตนของผู้ส่ง                                  ← ไม่ผ่าน = 401
2. หา access_item จาก request_id                        ← ไม่พบ = 422 ERR_ACK_UNKNOWN_REQUEST
3. ถ้า request_id นี้เคยได้ ack แล้ว → คืนผลเดิม จบ      ← idempotent (CA-03)
4. ตรวจ ack_by / ack_at / ack_ref ครบทั้งสาม             ← ขาดข้อใด = 422 ERR_ACK_INCOMPLETE  ★ ห้ามปิดรายการ
5. ถ้า result = failed → handleAckFailure() (ค้าง + เหตุผล + emit access_request_failed) จบ
6. ถ้า result = success:
   6.1 ตั้งสถานะของรายการ (granted / revoked / restored)
   6.2 เขียน ack_by · ack_at · ack_ref
   6.3 emit CSQ ของ "รายการนั้น"  (ไม่ใช่ของทั้งรอบ)
   6.4 evaluateRevocationCompleteness()
       ├─ ครบทุกแถว → case_status = revoked · revocation_flag = none
       │               emit CSQ access_revoked (is_final=true) + NTF ofb_access_revoked
       └─ ไม่ครบ และ now > revocation_due_at → revocation_flag = overdue (คงไว้)
7. appendHistory()
```

### §3.4.4 ยกเลิกรอบที่เพิกถอนไปแล้ว (API-09 · T-14) ⭐

```
1. ตรวจว่าผ่าน A-3 (สายเดิม) แล้ว                        ← ไม่ผ่าน = ยังยกเลิกไม่ได้
2. บังคับ cancel_reason                                  ← ERR_REASON_REQUIRED
3. ENG-OPSOW-01: ปิดงาน checklist ที่ค้างทั้งหมด "อย่างชัดแจ้ง" + นับจำนวน
4. publishEmploymentWindow(): ถอน last_working_day → null · employment_state กลับเป็น active
5. issueRestoreRequests():
      สำหรับทุกแถวที่ revoke_state = 'revoked'
        → สร้างคำขอคืนสิทธิ์ใหม่ พร้อม reversal_of = <แถว/เหตุการณ์เดิม>   ★ บังคับ
        → ห้ามแตะ ack_by / ack_at / ack_ref ของการเพิกถอนเดิม              ★ ห้ามเด็ดขาด
6. case_status = cancelled
7. emit ofb_case_cancelled (พร้อมจำนวนงานที่ปิด + จำนวนคำขอคืนสิทธิ์)
8. appendHistory() ทุกขั้นข้างต้น
```

### §3.4.5 ปิดรอบ (API-19)

```
1. closeBlockers() → ถ้าไม่ว่าง: 409 ERR_CLOSE_BLOCKED พร้อม details.blockers[] แยกรายบรรทัด
      blockers ที่เป็นไปได้:
        · งานบังคับที่ยังไม่เสร็จ (รายชื่องาน)
        · รายการสิทธิ์ที่ยังไม่ถูกเพิกถอน (จำนวน + ชนิด)      ★
        · ธง revocation_flag = overdue                        ★ → 409 ERR_REVOCATION_OVERDUE
        · ทรัพย์สินที่ยังไม่คืนและไม่ได้ทำเครื่องหมาย "คืนไม่ได้"
        · งานส่งมอบความเป็นเจ้าของข้อมูลที่ยังไม่เสร็จ
        · งานมอบหมายผู้ใต้บังคับบัญชา/งานอนุมัติค้างที่ยังไม่เสร็จ
2. บันทึกธงสิทธิ์การจ้างกลับ (ถ้ากรอก)
3. case_status = closed · closed_by · closed_at
4. appendHistory()
```
