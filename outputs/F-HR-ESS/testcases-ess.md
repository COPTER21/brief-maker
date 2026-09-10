# AI Test Cases — F-HR-ESS · ESS Portal (พนักงานทำเอง)

Test case ละเอียดสำหรับ **AI agent (browser-use / vision)** รันบนหน้าจอจริงแล้วรายงานผลกลับ.
Feature นี้เป็น **portal(aggregate) · display-only + deep-link** — นิยามด้วย "สิ่งที่ห้ามทำ": **ไม่มี form/create/save/edit/delete ที่ใดในพอร์ทัล**, ทุกปุ่ม "ยื่น/ขอ" = **navigate ออก** ไปหน้า owner feature, เห็นได้เฉพาะข้อมูลของ **ตนเอง** (self-access · SecC). เคสจึงเน้น **VERIFY (สิ่งที่แสดง)** + **negative (ยืนยันว่าไม่มีของที่ห้ามมี)** + **permission (403 / masking)**.

> **Anchor source (v1.2):** microcopy verbatim จาก `outputs/F-HR-ESS/ess.html` (source of truth) → 01_UI → microcopy กลาง v9. ทุกข้อความในเคสคัดตรงจากจอ.
> **DEMO-ONLY note:** element `.demo-only` (persona strip · ปุ่ม "ทดสอบเข้าถึงข้อมูลพนักงานอื่น" · chip `[ASSUMED contract]` / `อ่านอย่างเดียว`) เป็น demo/dev — **prod build strips ทิ้ง**. เคสที่ใช้ trigger สาธิต (เช่น 403) mark ไว้ว่าเป็น demo; expected เชิงสิทธิ์จริงยังต้องเทสที่ backend (ดู TC-SEC02).
> **Internal nav = tab state** (`goTab`: home/pay/docs/notify) — ไม่ใช่ hash route ของ ESS เอง. **hash route เดียวที่ ESS สร้าง = deep-link OUT** (ของ owner feature · `[ASSUMED] · OQ-ESS-02`). Start ของทุกเคส = เปิดพอร์ทัล ESS แล้วสลับแท็บด้วยปุ่ม seg.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-HR-ESS (F059 · Cube_Feature_List) |
| Feature Name | ESS Portal — พนักงานทำเอง (Employee Self-Service) |
| Archetype | portal(aggregate) · display-only + deep-link (ไม่มี CRUD/mutation/เอกสาร/เลขรัน/อนุมัติของตัวเอง) |
| FRD Version | 1.0 (2026-09-10) · STANDARD (7 files) |
| App entry | เมนูซ้าย **"ESS ของฉัน"** (1 feature = 1 เมนู) · หน้าเดียว 4 seg-tabs (default = "หน้าหลัก") |
| Internal nav | tab state (home/pay/docs/notify) — ไม่มี hash route ภายใน |
| Deep-link OUT (hash) | `#/leave/new` · `#/ot/new` · `#/expense/new` · `#/profile/edit-request` · `#/cert/new` — **[ASSUMED] · OQ-ESS-02** (prototype = toast, prod = navigate จริง) |
| Persona (self) | สมชาย ใจดี · EMP-00123 · เจ้าหน้าที่การตลาด · ฝ่ายการตลาด · สำนักงานใหญ่ |
| ที่มา | FRD Pack `FRD_F-HR-ESS_Pack/` (06_TESTS · 05_RULES · 01_UI · 00_OVERVIEW) + `BRD_ess.md` + `ess.html` |
| จำนวนเคส | 40 (happy 21 · negative 7 · edge 4 · error 2 · permission 6) |

---

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| A · หน้าหลัก (dashboard · FN-01) | TC-H01..H05 | สูง |
| B · สลิปเงินเดือน (FN-02) | TC-P01..P04 | สูง |
| C · วันลา/โควตา + ยื่นลา (FN-03) | TC-L01..L03 | สูง |
| D · OT/เวลา/สแกน + ตารางกะ (FN-04) | TC-D01..D02 | สูง |
| E · เอกสาร & สิทธิ์ (FN-05/06/07/08) | TC-E01..E08 | สูง |
| F · แจ้งเตือน + ค้นหา/กรอง (FN-09/FN-90) | TC-N01..N06 | กลาง |
| G · self-access / masking (FN-10/FN-94/FN-93) | TC-SEC01..SEC05 | สูง |
| H · overlay/deep-link/responsive/degrade (FN-11/FN-92 · XT) | TC-X01..X07 | กลาง |

---

## Coverage Ledger

### FN (06_TESTS §6.1 · FUNCTION_CHECKLIST QA lane · 15/15)
| FN | AT | cases |
|---|---|---|
| FN-01 หน้ารวมของฉัน (5 การ์ด read + launcher) | AT-01 | TC-H01, TC-H02, TC-H03 |
| FN-02 สลิป + ประวัติ + YTD (self · all-or-nothing) | AT-02 | TC-P01, TC-P02, TC-P03, TC-P04 |
| FN-03 วันลา/โควตา (read) + "ยื่นลา" navigate-out | AT-03 | TC-L01, TC-L02, TC-L03 |
| FN-04 OT/เวลา/สแกน + ตารางกะ (read-only) | AT-04 | TC-D01, TC-D02 |
| FN-05 ใบเบิก (read) + "ยื่นเบิก" navigate-out | AT-05 | TC-E01, TC-E02 |
| FN-06 หนังสือรับรอง (read) + "ขอหนังสือ" navigate-out | AT-06 | TC-E03, TC-E04 |
| FN-07 สวัสดิการ/อบรม/ใบรับรอง (read) | AT-07 | TC-E05 |
| FN-08 โปรไฟล์ (read · masked) + "ขอแก้ข้อมูล" navigate-out | AT-08 | TC-E06, TC-E07, TC-E08 |
| FN-09 แจ้งเตือนของฉัน (consume ENG-NOTIFY feed) | AT-09 | TC-N01, TC-N05 |
| FN-10 เข้าถึงคนอื่น → 403 (self-access SecC) | AT-10 | TC-SEC01, TC-SEC02 |
| FN-11 surface ba-done → display-only + [ASSUMED] chip | AT-11 | TC-X05 |
| FN-90 ค้นหา/กรอง notif + empty state | AT-12 | TC-N02, TC-N03, TC-N04, TC-N06 |
| FN-92 responsive (มือถือ) | AT-13 | TC-X03 |
| FN-93 audit การเข้าถึงข้อมูลตัวเอง (append-only) | AT-14 | TC-E08, TC-SEC05 |
| FN-94 ปิดบัง/ไม่แสดงข้อมูลนอกขอบเขต self | AT-15 | TC-SEC03, TC-SEC04, TC-H04 |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-01 ห้าม CRUD surface อื่น (display-only) | TC-P03, TC-D02, TC-E05, TC-SEC03 (verify no create/save/edit/delete) |
| BR-02 สลิป self เท่านั้น · all-or-nothing | TC-P01, TC-P04, TC-SEC03 |
| BR-03 ยื่นคำขอ = navigate (ไม่ทำ form) | TC-L03, TC-E02, TC-E04, TC-E07, TC-X01, TC-X02 |
| BR-04 dashboard = สรุป read หลาย surface | TC-H01 |
| BR-05 responsive | TC-X03 |
| BR-06 self-access เท่านั้น · คนอื่น=403 | TC-SEC01, TC-SEC02, TC-SEC03 |
| BR-07 surface ba-done = [ASSUMED contract] soft ref | TC-X05 |
| BR-08 audit อ่าน append-only · masking ตาม self | TC-E08, TC-SEC04, TC-SEC05 |

### Validation Rules (05_RULES §5.4)
| VR | cases |
|---|---|
| VR-1 deep-link route ไม่ยืนยัน → [ASSUMED] chip + fallback | TC-X05, TC-X02 |
| VR-2 RESTRICTED masking ตาม self · reveal → log | TC-E08, TC-SEC04 |
| VR-3 employee_id ≠ self → 403 backend · ไม่ leak field | TC-SEC01, TC-SEC02 |
| VR-4 search/filter notif ไม่พบ → empty (ไม่ใช่ error) | TC-N03, TC-N06 |
| VR-5 payslip all-or-nothing · ห้าม partial | TC-P01, TC-P04 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 เข้าถึงคนอื่น → 403 + ปิดบัง | TC-SEC01 |
| EC-02 surface ba-done → [ASSUMED] chip | TC-X05 |
| EC-03 ยื่นคำขอ → deep-link navigate-out | TC-X01 |
| EC-04 ค้น/กรอง feed ไม่พบ → empty | TC-N03 |
| EC-05 mobile responsive | TC-X03 |
| EC-06 payslip บางส่วน → all-or-nothing | TC-P04 |
| EC-07 deep-link route ยังไม่พร้อม → graceful notice `[AI-DEFAULT]` | TC-X02 (ต้อง simulate) |
| EC-08 surface down/timeout → per-card degrade `[AI-DEFAULT]` | TC-X06 (ต้อง simulate) |
| EC-09 session หมดกลาง drawer RESTRICTED → re-auth `[AI-DEFAULT]` | — ข้าม (○Optional P6 · OQ-ESS-06 · หลังบ้าน/ไม่มีผล UI คงที่) |
| EC-10 employee_id ผ่าน param → enforce self ที่ server | TC-SEC02 (ต้อง simulate) |
| EC-11 สลิป PDF ต้นทางยังไม่ออก → ปุ่มดาวน์โหลด disabled | — ข้าม (prototype ไม่มีปุ่มดาวน์โหลด PDF · OQ owner Payroll) |

### Error Catalog (05_RULES §5.6)
| Code | cases |
|---|---|
| ERR-403-SELF (403) | TC-SEC01, TC-SEC02 |
| ERR-404 (404 record ไม่มี) | — ข้าม (มาตรฐาน · prototype ไม่มี state ให้ trigger 404 ที่ UI) |
| ERR-DEGRADED (502/soft · per-card "โหลดไม่ได้") | TC-X06 (ต้อง simulate) |
| ERR-LINK-NA (soft · deep-link route ยังไม่พร้อม) | TC-X02 (ต้อง simulate) |

### Permission Matrix (05_RULES §5.3)
| cell | cases |
|---|---|
| พนักงาน(self) ดูข้อมูลตัวเอง = ✅ allow | TC-H01, TC-P01, TC-E06, TC-N01 |
| พนักงาน(self) ยื่นคำขอ (navigate-out) = ✅ allow | TC-X01 |
| พนักงาน(self) ดูข้อมูลคนอื่น = ❌ 403 | TC-SEC01, TC-SEC02 |
| พนักงาน(self) CRUD ใน ESS = ❌ (ไม่มี) | TC-P03, TC-D02, TC-E05 (verify ไม่มีปุ่ม) |
| พนักงาน(self) อนุมัติ = ❌ (ไม่มีในพอร์ทัล) | TC-X04 |

### Negative / Guard (06_TESTS §6.2)
| NEG | cases |
|---|---|
| NEG-01 ไม่มี create/save/edit/delete · footer มีแค่ "ปิด" | TC-P03, TC-E08 |
| NEG-02 ยื่นคำขอ = navigate เท่านั้น (ไม่มี form/submit ใน ESS) | TC-L03, TC-X01, TC-X04 |
| NEG-03 payslip all-or-nothing (เต็มใบ/403) | TC-P04 |
| NEG-04 reveal RESTRICTED โดยไม่ใช่ self → block | TC-SEC02 (ต้อง simulate) |
| NEG-05 ESS ไม่ยิง notification event (consume only) | TC-X04 (ต้อง simulate · verify by absence) |

### Cross-Module (06_TESTS §6.3 · XT)
| XT | Downstream | cases |
|---|---|---|
| XT-01 deep-link 5 routes (leave/ot/expense/profile/cert) | owner features | TC-X01 (+ TC-L03/E02/E04/E07 section buttons) |
| XT-02 deep-link fallback (route ยังไม่พร้อม) | — | TC-X02 (ต้อง simulate) |
| XT-03 ENG-NOTIFY consume (feed) | F-NOTIFY | TC-N01 |
| XT-04 ENG-CSQ SecC self-access event `[ASSUMED · OQ-ESS-01]` | ENG-CSQ | TC-SEC05 (ต้อง simulate · event id [ASSUMED]) |
| XT-05 surface degrade (owner down) | owner | TC-X06 (ต้อง simulate) |

### Scope Lock (00_OVERVIEW §0.11 · LK-1..6 · ต้องมีเคส verify)
| LOCK | cases verify |
|---|---|
| LK-1 display-only · ห้าม CRUD feature อื่น | TC-P03, TC-D02, TC-E05, TC-SEC03 |
| LK-2 ยื่นคำขอ = navigate ไป owner (ไม่ทำ form) | TC-L03, TC-X01 |
| LK-3 สลิปจาก PS-1 · self · all-or-nothing | TC-P01, TC-P04 |
| LK-4 self-access เท่านั้น · คนอื่น=403 | TC-SEC01, TC-SEC02 |
| LK-5 surface ba-done = [ASSUMED contract] | TC-X05 |
| LK-6 CSQ=SecC + NTF=อ่าน feed · ไม่มี doa/doccfg/pdf · audit append-only | TC-N01, TC-E08, TC-X04 |

### Cross-cutting / States
| item | cases |
|---|---|
| self-banner (self-scope ทุกหน้า) | TC-H04, TC-SEC03 |
| empty state (feed) | TC-N03 |
| filtered-empty (unread + no match) | TC-N06 |
| overlay: modal-over-drawer + Esc chain (DSP-01) | TC-X07 |
| [ASSUMED]/read-only chip (demo) | TC-X05 |

> **Out of Scope (Scope Lock Exclusions · ห้ามสร้างเคส · NS-1..6):** สร้าง/แก้/ลบข้อมูล feature อื่น · ทำฟอร์มยื่นในพอร์ทัล · ออกสลิป/หนังสือ/PDF เอง · Manager self-service/อนุมัติในพอร์ทัล · config เมนู/สิทธิ์เอง · ออกเอกสาร/เลขรัน/สายอนุมัติ. เคสที่ "ยืนยันว่าไม่มี" ของพวกนี้ = negative (TC-P03/D02/E05/X04) ไม่ใช่การทดสอบ feature.

---

## Data Sets

> ทั้งหมดเป็น seed ของ persona **self = สมชาย ใจดี · EMP-00123** (mock ในพอร์ทัล). Agent ไม่ต้องกรอกข้อมูล — feature นี้ read-only. ค่าด้านล่างใช้เป็น "ค่าที่คาดเห็นบนจอ" (expected).

### DS-EMP (โปรไฟล์ self)
| ฟิลด์ | ค่า |
|---|---|
| ชื่อ-นามสกุล | สมชาย ใจดี |
| รหัสพนักงาน | EMP-00123 |
| ตำแหน่ง | เจ้าหน้าที่การตลาด |
| แผนก / สาขา | ฝ่ายการตลาด · สำนักงานใหญ่ |
| อีเมล | somchai.j@cube.co.th |
| โทรศัพท์ | 08X-XXX-4567 |
| วันเริ่มงาน | 1 มี.ค. 2562 |
| เลขบัตร ปชช. (masked) | X-XXXX-XXXXX-56-7 |
| เลขบัตร ปชช. (reveal) | 1-2345-67890-56-7 |
| บัญชีธนาคาร (masked) | ธนาคารกสิกรไทย ••••••3456 |
| บัญชีธนาคาร (reveal) | ธนาคารกสิกรไทย 123-4-53456-7 |

### DS-DASH (ค่าสรุป dashboard ที่คาด)
| การ์ด | ค่า | sub |
|---|---|---|
| สลิปล่าสุด | ฿38,250.00 | กรกฎาคม 2568 |
| โควตาลาคงเหลือ | 38 วัน | รวมทุกประเภท |
| OT เดือนนี้ | 12 ชม. | กรกฎาคม 2568 |
| ใบเบิกค้าง | 1 ใบ | รออนุมัติ |
| แจ้งเตือน | 2 รายการ | ยังไม่อ่าน (badge = 2) |

### DS-PAY (สลิปล่าสุด PS-2568-07)
| ฟิลด์ | ค่า |
|---|---|
| รอบเดือน | กรกฎาคม 2568 · จ่าย 31 ก.ค. 2568 |
| รายได้รวม / รายการหัก / ยอดสุทธิ | ฿45,000.00 / ฿6,750.00 / ฿38,250.00 |
| สถานะ | จ่ายแล้ว |
| YTD (สะสมทั้งปี) | รายได้ ฿315,000.00 · ภาษี ฿18,900.00 · ประกันสังคม ฿5,250.00 · สุทธิ ฿267,750.00 |

### DS-NOTIF (คำค้นทดสอบ)
| ชุด | ค่า | ผล |
|---|---|---|
| ค้นเจอ | `สลิป` | เจอ N-104 "สลิปเงินเดือนเดือนกรกฎาคมออกแล้ว" |
| ค้นไม่เจอ | `zzzไม่มีจริง` | empty state |
| unread filter | (ปุ่ม "ยังไม่อ่าน") | เหลือ 2 รายการ (N-104, N-103) |

### DS-DEEPLINK (label ที่คาดใน toast · verbatim)
| key | ปุ่ม | toast label |
|---|---|---|
| leave | "ยื่นลา" / "ขอลา" | การลา |
| ot | "ขอทำงานล่วงเวลา (OT)" | ขอทำงานล่วงเวลา |
| expense | "ยื่นเบิก" / "ขอเบิกค่าใช้จ่าย" | เบิกค่าใช้จ่าย |
| profile | "ขอแก้ข้อมูล" / "ขอแก้ข้อมูลส่วนตัว" | แก้ไขข้อมูลพนักงาน (ขออนุมัติ) |
| cert | "ขอหนังสือ" / "ขอหนังสือรับรอง" | หนังสือรับรอง |

### ไฟล์ทดสอบ (Files)
- ไม่มี — feature อ่านอย่างเดียว ไม่มีการอัปโหลด/นำเข้าไฟล์.

---

## Test Cases

## Group A — หน้าหลัก (dashboard · FN-01)

### TC-H01 — หน้ารวมของฉัน แสดง banner + launcher + 5 การ์ดสรุป (happy)
- group: หน้าหลัก · ความสำคัญ: สูง · trace: FN-01 / AT-01 / BR-04 / permission(self allow)
- actor (role): พนักงาน (self = สมชาย ใจดี)
- Setup: role=employee(self · EMP-00123) · seed=พอร์ทัลโหลด seed persona ครบ (สลิป/ลา/OT/เบิก/แจ้งเตือน) · files=—
- Start: OPEN พอร์ทัล ESS (เมนูซ้าย "ESS ของฉัน") — default tab = "หน้าหลัก"
- ผ่านเมื่อ: เห็น self-banner + launcher + การ์ดครบ 5 ใบตรง DS-DASH

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN พอร์ทัล ESS | — | หัวข้อ **ESS ของฉัน** + chip **พนักงานทำเอง** + คำโปรย "ดูข้อมูลของคุณจากทุกระบบไว้ที่เดียว — สลิป · ลา · OT · เบิก · หนังสือรับรอง · สวัสดิการ · อบรม · แจ้งเตือน" | ☐ |
| 2 | VERIFY self-banner | — | แถบ "**คุณกำลังดูข้อมูลของตนเอง (สมชาย ใจดี · EMP-00123) — ข้อมูลส่วนตัว/เงินเดือนแสดงเฉพาะของคุณเท่านั้น**" (ไอคอนโล่) | ☐ |
| 3 | VERIFY launcher card | — | หัวข้อ "**ต้องการยื่นคำขอใช่ไหม?**" + ข้อความ "เลือกประเภทคำขอ แล้วระบบจะพาไปยังหน้าฟีเจอร์เจ้าของเพื่อกรอกและส่ง (ESS ไม่รับคำขอเอง)" + ปุ่ม primary "**ยื่นคำขอ**" | ☐ |
| 4 | VERIFY การ์ด "สลิปล่าสุด" | — | ค่า **฿38,250.00** · sub **กรกฎาคม 2568** | ☐ |
| 5 | VERIFY การ์ด "โควตาลาคงเหลือ" | — | ค่า **38 วัน** · sub **รวมทุกประเภท** | ☐ |
| 6 | VERIFY การ์ด "OT เดือนนี้" | — | ค่า **12 ชม.** · sub **กรกฎาคม 2568** | ☐ |
| 7 | VERIFY การ์ด "ใบเบิกค้าง" | — | ค่า **1 ใบ** · sub **รออนุมัติ** | ☐ |
| 8 | VERIFY การ์ด "แจ้งเตือน" | — | ค่า **2 รายการ** · sub **ยังไม่อ่าน** · มี badge เลข **2** | ☐ |
| 9 | VERIFY seg-tabs | — | เห็น 4 แท็บ: **หน้าหลัก** (active) · **เงินเดือน & เวลา** · **เอกสาร & สิทธิ์** · **แจ้งเตือน** | ☐ |
| 10 | VERIFY section "ทางลัดของฉัน" | — | เห็นหัวข้อ "ทางลัดของฉัน" + "แตะการ์ดด้านบนเพื่อดูรายละเอียด (อ่านอย่างเดียว)" + chip "อ่านอย่างเดียว" + แถว พนักงาน = สมชาย ใจดี · เจ้าหน้าที่การตลาด | ☐ |

### TC-H02 — การ์ด dashboard นำทางถูกปลายทาง (happy)
- group: หน้าหลัก · ความสำคัญ: สูง · trace: FN-01 / AT-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS · tab "หน้าหลัก"
- ผ่านเมื่อ: แต่ละการ์ดพาไป view/tab ที่ถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "สลิปล่าสุด" | — | drawer เปิด หัวข้อสลิป **กรกฎาคม 2568** (drawer สลิป · ดู TC-P01) | ☐ |
| 2 | PRESS Esc | — | drawer ปิด กลับหน้าหลัก | ☐ |
| 3 | CLICK การ์ด "โควตาลาคงเหลือ" | — | สลับไปแท็บ **เงินเดือน & เวลา** (เห็น section "วันลา & โควตา") | ☐ |
| 4 | CLICK แท็บ "หน้าหลัก" | — | กลับ dashboard | ☐ |
| 5 | CLICK การ์ด "OT เดือนนี้" | — | สลับไปแท็บ **เงินเดือน & เวลา** (เห็น section "OT & เวลาทำงาน") | ☐ |
| 6 | CLICK แท็บ "หน้าหลัก" → CLICK การ์ด "ใบเบิกค้าง" | — | สลับไปแท็บ **เอกสาร & สิทธิ์** (เห็น "ใบเบิกค่าใช้จ่าย") | ☐ |
| 7 | CLICK แท็บ "หน้าหลัก" → CLICK การ์ด "แจ้งเตือน" | — | สลับไปแท็บ **แจ้งเตือน** (เห็น feed) | ☐ |

### TC-H03 — เปิดโปรไฟล์จากทางลัด (happy)
- group: หน้าหลัก · ความสำคัญ: กลาง · trace: FN-01 / FN-08 / AT-08
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS · tab "หน้าหลัก" · section "ทางลัดของฉัน"
- ผ่านเมื่อ: ปุ่ม "ดูโปรไฟล์ของฉัน" เปิด drawer โปรไฟล์ของ self

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ดูโปรไฟล์ของฉัน" (ในทางลัดของฉัน) | — | drawer เปิด eyebrow "**โปรไฟล์ของฉัน**" + chip "อ่านอย่างเดียว" · title **สมชาย ใจดี** · sub เจ้าหน้าที่การตลาด · ฝ่ายการตลาด | ☐ |
| 2 | VERIFY footer ของ drawer | — | มี "อ่านอย่างเดียว · แก้ไขไม่ได้ในพอร์ทัล" + ปุ่ม "ปิด" + ปุ่ม "ยื่นคำขอ" (ไม่มีปุ่มบันทึก/แก้ไข) | ☐ |
| 3 | PRESS Esc | — | drawer ปิด | ☐ |

### TC-H04 — self-banner ยืนยัน self-scope ทุกหน้า (permission · FN-94)
- group: หน้าหลัก · ความสำคัญ: สูง · trace: FN-94 / AT-15 / BR-06
- actor (role): พนักงาน (self)
- Setup: role=employee(self · EMP-00123) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS
- ผ่านเมื่อ: banner แสดงชื่อ+รหัสของ self เท่านั้น · ไม่มีชื่อ/รหัสพนักงานคนอื่นปรากฏ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY self-banner | — | ระบุ **สมชาย ใจดี · EMP-00123** (ตรง persona) — ไม่มี id/ชื่ออื่น | ☐ |
| 2 | CLICK แท็บ "เงินเดือน & เวลา" → VERIFY banner | — | banner ยังคงเป็น self เดิม (ไม่เปลี่ยนตาม tab) | ☐ |
| 3 | CLICK แท็บ "เอกสาร & สิทธิ์" → VERIFY | — | ทุกข้อมูล (สลิป/ลา/เบิก/โปรไฟล์) เป็นของ EMP-00123 · ไม่มีตัวเลือกสลับดูพนักงานอื่น (ไม่มี dropdown/ค้นหาพนักงาน) | ☐ |

### TC-H05 — เปิด action-picker จากปุ่ม "ยื่นคำขอ" ที่หัวหน้า (happy)
- group: หน้าหลัก · ความสำคัญ: กลาง · trace: FN-01 / BR-03 / M-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS · tab "หน้าหลัก"
- ผ่านเมื่อ: ปุ่ม "ยื่นคำขอ" (header) เปิด modal action-picker

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ยื่นคำขอ" (มุมขวาบน header) | — | modal เปิด หัวข้อ "**ยื่นคำขอ**" + "เลือกประเภทคำขอ — ระบบจะพาไปยังหน้าฟีเจอร์เจ้าของเพื่อกรอกและส่ง" | ☐ |
| 2 | VERIFY รายการใน modal | — | 5 แถว: ขอลา · ขอทำงานล่วงเวลา (OT) · ขอเบิกค่าใช้จ่าย · ขอแก้ข้อมูลส่วนตัว · ขอหนังสือรับรอง | ☐ |
| 3 | VERIFY note ท้าย modal | — | "ESS ไม่รับหรือบันทึกคำขอเอง — ทุกการยื่นทำที่หน้าฟีเจอร์เจ้าของ (deep-link) ตามมติ OQ-HR-04" | ☐ |
| 4 | CLICK ปุ่ม "ปิด" | — | modal ปิด กลับหน้าหลัก | ☐ |

---

## Group B — สลิปเงินเดือน (FN-02)

### TC-P01 — เปิดสลิป 2 sub-tab · อ่านอย่างเดียว (happy)
- group: สลิป · ความสำคัญ: สูง · trace: FN-02 / AT-02 / BR-02 / VR-5 / LK-3 / permission(self allow)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=สลิป PS-2568-07..05 (self) · files=—
- Start: OPEN พอร์ทัล ESS · CLICK แท็บ "เงินเดือน & เวลา"
- ผ่านเมื่อ: drawer สลิปเปิด 2 sub-tab · เห็นยอดสุทธิ · note all-or-nothing · footer มีแค่ "ปิด"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "สลิปเงินเดือน" | — | หัวข้อ "สลิปเงินเดือน" · sub "เฉพาะของตนเอง" · chip "[ASSUMED contract]" + "อ่านอย่างเดียว" · ตารางหัว: รอบเดือน/วันที่จ่าย/ยอดสุทธิ/สถานะ | ☐ |
| 2 | CLICK แถวสลิป "กรกฎาคม 2568 · PS-2568-07" | — | drawer เปิด · eyebrow "สลิปเงินเดือน" + chip "อ่านอย่างเดียว" · title **กรกฎาคม 2568** · sub "PS-2568-07 · จ่าย 31 ก.ค. 2568" | ☐ |
| 3 | VERIFY sub-tabs | — | เห็น 2 แท็บ "**รายละเอียด**" (active) / "**สะสมทั้งปี (YTD)**" | ☐ |
| 4 | VERIFY def ในแท็บรายละเอียด | — | รอบเดือน กรกฎาคม 2568 · รายได้รวม ฿45,000.00 · รายการหัก ฿6,750.00 · **ยอดสุทธิ ฿38,250.00** · สถานะ จ่ายแล้ว | ☐ |
| 5 | VERIFY note all-or-nothing | — | "**สลิปฉบับ PDF ออกจากระบบเงินเดือน (ต้นทาง) — ESS แสดงผลอ่านอย่างเดียว เห็นเฉพาะสลิปของตนเองแบบ all-or-nothing**" | ☐ |
| 6 | VERIFY footer drawer | — | "อ่านอย่างเดียว · แก้ไขไม่ได้ในพอร์ทัล" + ปุ่ม "ปิด" เท่านั้น (ไม่มีบันทึก/แก้/ดาวน์โหลดแก้) | ☐ |

### TC-P02 — สลิป sub-tab สะสมทั้งปี (YTD) (happy)
- group: สลิป · ความสำคัญ: กลาง · trace: FN-02 / AT-02
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=YTD ของ self · files=—
- Start: เปิด drawer สลิป PS-2568-07 (ต่อจาก TC-P01)
- ผ่านเมื่อ: แท็บ YTD แสดงยอดสะสมตรง DS-PAY

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวสลิป "PS-2568-07" | — | drawer เปิด (แท็บ "รายละเอียด" active) | ☐ |
| 2 | CLICK sub-tab "สะสมทั้งปี (YTD)" | — | เนื้อหาเปลี่ยนเป็น YTD · แท็บ YTD active | ☐ |
| 3 | VERIFY def YTD | — | รายได้สะสม ฿315,000.00 · ภาษีสะสม ฿18,900.00 · ประกันสังคมสะสม ฿5,250.00 · **สุทธิสะสม ฿267,750.00** | ☐ |
| 4 | CLICK sub-tab "รายละเอียด" | — | กลับหน้ารายละเอียด (ค่ายังเป็น ฿38,250.00) — สลับ tab ไม่รีเซ็ต drawer | ☐ |

### TC-P03 — ไม่มีปุ่มสร้าง/บันทึก/แก้ในพอร์ทัลทั้งหน้า (negative · NEG-01/BR-01/LK-1)
- group: สลิป · ความสำคัญ: สูง · trace: NEG-01 / BR-01 / LK-1 / permission(no CRUD)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS
- ผ่านเมื่อ: ไม่พบปุ่ม create/save/edit/delete ที่ใดในพอร์ทัล — มีแค่ "ยื่นคำขอ" (navigate) / "ปิด"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มทั้งหน้าหลัก | — | ปุ่มที่ actionได้มีเพียง "ยื่นคำขอ" (เปิด picker) + การ์ด (นำทาง) — **ไม่มี** "เพิ่ม/สร้าง/บันทึก/แก้ไข/ลบ" | ☐ |
| 2 | CLICK แท็บ "เงินเดือน & เวลา" → VERIFY | — | ปุ่มมีแค่ "ยื่นลา" (navigate) — ไม่มีปุ่มแก้สลิป/แก้กะ/บันทึก | ☐ |
| 3 | CLICK แถวสลิป → VERIFY drawer footer | — | footer = "ปิด" อย่างเดียว (ไม่มี save/submit) · มี ro-strip "อ่านอย่างเดียว · แก้ไขไม่ได้ในพอร์ทัล" | ☐ |
| 4 | VERIFY ทั้ง drawer สลิป | — | ไม่มี input/textarea/checkbox ที่แก้ค่าได้ — เป็นข้อความอ่านล้วน | ☐ |

### TC-P04 — payslip all-or-nothing (ไม่มี partial) (negative/edge · NEG-03/EC-06)
- group: สลิป · ความสำคัญ: สูง · trace: NEG-03 / EC-06 / BR-02 / VR-5
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=สลิป self ทุกใบมีครบทุกฟิลด์ · files=—
- Start: OPEN พอร์ทัล ESS · แท็บ "เงินเดือน & เวลา"
- ผ่านเมื่อ: สลิปแต่ละใบแสดงเต็ม (gross/deduct/net/status ครบ) — ไม่มีการซ่อนบางฟิลด์แบบ partial projection

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตารางสลิป | — | 3 แถว (PS-2568-07/06/05) ทุกแถวมี ยอดสุทธิ + สถานะ "จ่ายแล้ว" ครบ (ไม่มีแถวที่ค่าเป็นว่าง/ปิดบางส่วน) | ☐ |
| 2 | CLICK แถว "PS-2568-06 · มิถุนายน 2568" | — | drawer แสดงครบ: รายได้รวม ฿45,000.00 · รายการหัก ฿6,750.00 · ยอดสุทธิ ฿38,250.00 (เต็มใบ) | ☐ |
| 3 | VERIFY | — | ไม่มีฟิลด์ที่แสดง "•••"/ถูกตัดบางส่วนในสลิป (สลิป = เต็มใบหรือไม่เห็นเลย · ไม่มีสถานะกลาง) | ☐ |

---

## Group C — วันลา / โควตา + ยื่นลา (FN-03)

### TC-L01 — วันลา & โควตา (read) (happy)
- group: ลา · ความสำคัญ: สูง · trace: FN-03 / AT-03
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=โควตาลา (พักร้อน 4/10 · ป่วย 2/30 · กิจ 1/5) + ประวัติลา 3 รายการ · files=—
- Start: OPEN พอร์ทัล ESS · CLICK แท็บ "เงินเดือน & เวลา"
- ผ่านเมื่อ: เห็น quota bars + ประวัติลา read

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "วันลา & โควตา" | — | หัวข้อ + sub "อ่านจากระบบการลา" + chip "[ASSUMED contract]" + ปุ่ม "ยื่นลา" | ☐ |
| 2 | VERIFY quota bars | — | ลาพักร้อน คงเหลือ **6** / 10 วัน · ลาป่วย คงเหลือ **28** / 30 วัน · ลากิจ คงเหลือ **4** / 5 วัน | ☐ |
| 3 | VERIFY ตารางประวัติลา | — | หัว ประเภท/ช่วงวันลา/จำนวน/สถานะ · แถว LV-2568-014 (ลาพักร้อน · อนุมัติแล้ว) · LV-2568-021 (ลากิจ · รออนุมัติ) | ☐ |

### TC-L02 — เปิดรายละเอียดการลา (read drawer) (happy)
- group: ลา · ความสำคัญ: กลาง · trace: FN-03 / AT-03
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=LV-2568-014 · files=—
- Start: แท็บ "เงินเดือน & เวลา" · section "วันลา & โควตา"
- ผ่านเมื่อ: drawer รายละเอียดลาเปิด read-only + footer "ปิด"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวประวัติลา "LV-2568-014 · ลาพักร้อน" | — | drawer เปิด eyebrow "รายละเอียดการลา" + chip อ่านอย่างเดียว · title ลาพักร้อน · sub LV-2568-014 | ☐ |
| 2 | VERIFY def | — | ประเภท ลาพักร้อน · ช่วงวันลา 12–13 มิ.ย. 2568 · จำนวน 2 วัน · สถานะ อนุมัติแล้ว | ☐ |
| 3 | VERIFY note ต้นทาง | — | "อ่านจากระบบการลา (ต้นทาง) — หากต้องการยื่นลาใหม่ ใช้ปุ่ม "ยื่นลา" เพื่อไปยังหน้าการลา" | ☐ |
| 4 | VERIFY footer | — | ปุ่ม "ปิด" เท่านั้น (ไม่มีแก้/ยกเลิกลา) | ☐ |

### TC-L03 — "ยื่นลา" = navigate-out (ไม่มี form ใน ESS) (negative · NEG-02/BR-03/LK-2/XT-01)
- group: ลา · ความสำคัญ: สูง · trace: FN-03 / BR-03 / NEG-02 / LK-2 / XT-01(leave)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: แท็บ "เงินเดือน & เวลา" · section "วันลา & โควตา"
- ผ่านเมื่อ: กด "ยื่นลา" → toast นำทาง (prototype) · **ไม่มีฟอร์มลาเปิดในพอร์ทัล**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ยื่นลา" | — | ไม่มี drawer/modal ฟอร์มกรอกลาเปิดขึ้น | ☐ |
| 2 | WAIT จน toast ปรากฏ (≤3.2s) | — | toast info: **กำลังนำทางไปหน้า "การลา"** (prototype stub · prod = navigate `#/leave/new` [ASSUMED]) | ☐ |
| 3 | VERIFY หลัง toast | — | ยังอยู่หน้า ESS (แท็บเดิม) · ไม่มี field ให้กรอก/ปุ่มส่งคำขอในพอร์ทัล | ☐ |

---

## Group D — OT / เวลา / สแกน + ตารางกะ (FN-04)

### TC-D01 — OT & เวลาทำงาน + สแกน (read) (happy)
- group: OT/เวลา · ความสำคัญ: สูง · trace: FN-04 / AT-04 / BR-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=OT ก.ค. 2568 (12 ชม. · อนุมัติ 8 · รอ 4) + scans 3 แถว · files=—
- Start: OPEN พอร์ทัล ESS · CLICK แท็บ "เงินเดือน & เวลา"
- ผ่านเมื่อ: เห็น OT summary + ตารางสแกน read-only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "OT & เวลาทำงาน" | — | หัวข้อ + sub "กรกฎาคม 2568" + chip "[ASSUMED contract]" + "อ่านอย่างเดียว" | ☐ |
| 2 | VERIFY OT summary | — | "OT รวมเดือนนี้ = **12 ชั่วโมง (อนุมัติ 8 · รออนุมัติ 4)**" | ☐ |
| 3 | VERIFY ตารางสแกน | — | หัว วันที่/เข้า/ออก/หมายเหตุ · แถว 25 ก.ค. (08:52/18:10/ปกติ) · 24 ก.ค. (08:47/20:30/OT 2 ชม.) · 23 ก.ค. (09:05/18:02/เข้าสาย 5 นาที) | ☐ |
| 4 | VERIFY | — | ไม่มีปุ่มขอ OT/แก้เวลาในหน้านี้ (ขอ OT อยู่ใน action-picker เท่านั้น) | ☐ |

### TC-D02 — ตารางกะของฉัน 7 วัน · read-only ไม่มีปุ่มแก้กะ (happy/negative · AT-04/BR-01/LK-1)
- group: OT/เวลา · ความสำคัญ: สูง · trace: FN-04 / AT-04 / BR-01 / LK-1
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=ตารางกะสัปดาห์นี้ 7 แถว (จ.21–อา.27 ก.ค. 2568) · files=—
- Start: แท็บ "เงินเดือน & เวลา" · เลื่อนลงถึง section "ตารางกะของฉัน"
- ผ่านเมื่อ: เห็นตารางกะ 7 วัน · ไม่มีปุ่ม/ช่องแก้กะใด ๆ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "ตารางกะของฉัน" | — | หัวข้อ + sub "สัปดาห์นี้" + chip "[ASSUMED contract]" + "อ่านอย่างเดียว" · ตารางหัว วันที่/กะ | ☐ |
| 2 | VERIFY จำนวนแถว | — | **7 แถว** (จ.21 · อ.22 · พ.23 · พฤ.24 · ศ.25 · ส.26 · อา.27 ก.ค. 2568) | ☐ |
| 3 | VERIFY เนื้อกะ | — | จ.21–พ.23 = "เช้า 08:00–17:00" · พฤ.24 = "บ่าย 13:00–22:00" · ศ.25 = "เช้า 08:00–17:00" · ส.26/อา.27 = "หยุด" | ☐ |
| 4 | VERIFY การกระทำบนตารางกะ | — | ไม่มีปุ่ม "แก้กะ"/"สลับกะ"/dropdown แก้กะ · แถวคลิกไม่เปิดฟอร์มแก้ (read-only ล้วน) | ☐ |

---

## Group E — เอกสาร & สิทธิ์ (FN-05/06/07/08)

### TC-E01 — ใบเบิกค่าใช้จ่าย (read) (happy)
- group: เอกสาร · ความสำคัญ: สูง · trace: FN-05 / AT-05
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=ใบเบิก EX-2568-031 (รออนุมัติ) · EX-2568-028 (อนุมัติแล้ว) · files=—
- Start: OPEN พอร์ทัล ESS · CLICK แท็บ "เอกสาร & สิทธิ์"
- ผ่านเมื่อ: เห็นตารางใบเบิก + เปิด drawer รายละเอียด read

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "ใบเบิกค่าใช้จ่าย" | — | หัวข้อ + sub "ของฉัน" + chip "[ASSUMED contract]" + ปุ่ม "ยื่นเบิก" · ตารางหัว เรื่อง/วันที่/จำนวนเงิน/สถานะ | ☐ |
| 2 | VERIFY แถว | — | EX-2568-031 "ค่าเดินทางพบลูกค้า" ฿1,250.00 รออนุมัติ · EX-2568-028 "ค่ารับรองลูกค้า" ฿3,400.00 อนุมัติแล้ว | ☐ |
| 3 | CLICK แถว "EX-2568-031" | — | drawer เปิด "รายละเอียดใบเบิก" · จำนวนเงิน ฿1,250.00 · note "อ่านจากระบบเบิกค่าใช้จ่าย (ต้นทาง) — ยื่นเบิกใหม่ที่หน้าเบิกค่าใช้จ่าย" · footer "ปิด" | ☐ |

### TC-E02 — "ยื่นเบิก" = navigate-out (negative · NEG-02/BR-03/XT-01)
- group: เอกสาร · ความสำคัญ: สูง · trace: FN-05 / BR-03 / NEG-02 / XT-01(expense)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "ใบเบิกค่าใช้จ่าย"
- ผ่านเมื่อ: กด "ยื่นเบิก" → toast นำทาง · ไม่มีฟอร์มเบิกในพอร์ทัล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ยื่นเบิก" | — | ไม่มีฟอร์มเบิกเปิดในพอร์ทัล | ☐ |
| 2 | WAIT จน toast ปรากฏ | — | toast: **กำลังนำทางไปหน้า "เบิกค่าใช้จ่าย"** (prod = `#/expense/new` [ASSUMED]) | ☐ |
| 3 | VERIFY | — | ยังอยู่หน้า ESS · ไม่มี field/submit ในพอร์ทัล | ☐ |

### TC-E03 — หนังสือรับรอง / เอกสาร (read) (happy)
- group: เอกสาร · ความสำคัญ: กลาง · trace: FN-06 / AT-06 / BR-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=CERT-2568-004 (หนังสือรับรองการทำงาน) · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "หนังสือรับรอง / เอกสาร"
- ผ่านเมื่อ: เห็นเอกสารที่ออก + เปิด drawer read

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "หนังสือรับรอง / เอกสาร" | — | sub "ออกจากฝ่ายบุคคล" + chip [ASSUMED] + ปุ่ม "ขอหนังสือ" · ตารางหัว เอกสาร/วันที่ออก/ผู้ออก/สถานะ | ☐ |
| 2 | VERIFY แถว | — | CERT-2568-004 "หนังสือรับรองการทำงาน" · 2 ก.ค. 2568 · ฝ่ายบุคคล · ออกแล้ว | ☐ |
| 3 | CLICK แถว CERT-2568-004 | — | drawer "หนังสือรับรอง" · note "ไฟล์ PDF ออกจากฝ่ายบุคคล (ต้นทาง) — ESS แสดงผลอ่านอย่างเดียว" · footer "ปิด" | ☐ |

### TC-E04 — "ขอหนังสือ" = navigate-out (negative · NEG-02/BR-03/XT-01)
- group: เอกสาร · ความสำคัญ: กลาง · trace: FN-06 / BR-03 / NEG-02 / XT-01(cert)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "หนังสือรับรอง / เอกสาร"
- ผ่านเมื่อ: กด "ขอหนังสือ" → toast นำทาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ขอหนังสือ" | — | ไม่มีฟอร์มขอหนังสือเปิดในพอร์ทัล | ☐ |
| 2 | WAIT จน toast ปรากฏ | — | toast: **กำลังนำทางไปหน้า "หนังสือรับรอง"** (prod = `#/cert/new` [ASSUMED]) | ☐ |

### TC-E05 — สวัสดิการ & อบรม (read) (happy · BR-01/LK-1)
- group: เอกสาร · ความสำคัญ: กลาง · trace: FN-07 / AT-07 / BR-01 / LK-1
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=welfare (OPD 7000/15000 · ประกันกลุ่ม · PVD) + training TR-2568-012 · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "สวัสดิการ & อบรม"
- ผ่านเมื่อ: เห็นคงเหลือสวัสดิการ (bars) + ประวัติอบรม read · ไม่มีปุ่มแก้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "สวัสดิการ & อบรม" | — | sub "คงเหลือและประวัติของฉัน" + chip [ASSUMED] + "อ่านอย่างเดียว" | ☐ |
| 2 | VERIFY balances | — | "ค่ารักษาพยาบาล (OPD)" มี bar + **฿8,000 / ฿15,000** · "ประกันสุขภาพกลุ่ม" = "คุ้มครอง · วงเงิน 500,000 บาท" · "กองทุนสำรองเลี้ยงชีพ" = "สะสม 3% · สมทบ 3%" | ☐ |
| 3 | VERIFY ตารางอบรม | — | หัว หลักสูตรอบรม/วันที่/ชั่วโมง/ใบรับรอง/สถานะ · แถว TR-2568-012 "อบรมความปลอดภัยข้อมูล (Data Security)" · 6 ชม. · มีใบรับรอง · ผ่าน | ☐ |
| 4 | CLICK แถว TR-2568-012 | — | drawer "ประวัติอบรม" อ่านอย่างเดียว · footer "ปิด" (ไม่มีปุ่มแก้/ลงทะเบียน) | ☐ |

### TC-E06 — ข้อมูลส่วนตัว / โปรไฟล์ · เลขบัตรปิดบัง (happy · FN-08/VR-2)
- group: เอกสาร · ความสำคัญ: สูง · trace: FN-08 / AT-08 / VR-2 / permission(self allow)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=โปรไฟล์ EMP-00123 (RESTRICTED masked) · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "ข้อมูลส่วนตัว / โปรไฟล์"
- ผ่านเมื่อ: เลขบัตร ปชช. masked + note แก้ไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "ข้อมูลส่วนตัว / โปรไฟล์" | — | sub "อ่านจากทะเบียนพนักงาน" + chip [ASSUMED] + ปุ่ม "ดูโปรไฟล์" + "ขอแก้ข้อมูล" | ☐ |
| 2 | VERIFY def | — | ชื่อ-นามสกุล สมชาย ใจดี · ตำแหน่ง เจ้าหน้าที่การตลาด · อีเมล somchai.j@cube.co.th | ☐ |
| 3 | VERIFY เลขบัตร ปชช. | — | แสดง **X-XXXX-XXXXX-56-7** + chip "ปิดบัง" (ไอคอนกุญแจ) — ไม่โชว์เลขเต็ม | ☐ |
| 4 | VERIFY note | — | "การแก้ไขข้อมูลต้องยื่นผ่านหน้าฟีเจอร์เจ้าของเพื่อขออนุมัติ — ESS แก้ไขข้อมูลเองไม่ได้" | ☐ |

### TC-E07 — "ขอแก้ข้อมูล" = navigate-out (negative · NEG-02/BR-03/XT-01)
- group: เอกสาร · ความสำคัญ: สูง · trace: FN-08 / BR-03 / NEG-02 / XT-01(profile)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "ข้อมูลส่วนตัว / โปรไฟล์"
- ผ่านเมื่อ: กด "ขอแก้ข้อมูล" → toast นำทาง · ไม่มีฟอร์มแก้ในพอร์ทัล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ขอแก้ข้อมูล" | — | ไม่มีฟอร์มแก้โปรไฟล์เปิดในพอร์ทัล | ☐ |
| 2 | WAIT จน toast ปรากฏ | — | toast: **กำลังนำทางไปหน้า "แก้ไขข้อมูลพนักงาน (ขออนุมัติ)"** (prod = `#/profile/edit-request` [ASSUMED]) | ☐ |

### TC-E08 — โปรไฟล์ drawer: reveal RESTRICTED + audit append-only (happy/permission · FN-08/FN-93/VR-2/BR-08/NEG-01)
- group: เอกสาร · ความสำคัญ: สูง · trace: FN-08 / FN-93 / AT-14 / VR-2 / BR-08 / NEG-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=โปรไฟล์ self + accessAudit 3 แถว · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · CLICK ปุ่ม "ดูโปรไฟล์" (หรือทางลัด "ดูโปรไฟล์ของฉัน")
- ผ่านเมื่อ: reveal/ซ่อน เลขบัตร+บัญชี ทำได้ (self) · เห็น audit rows + note append-only · footer ไม่มี save

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ดูโปรไฟล์" | — | drawer เปิด · section "ข้อมูลทั่วไป" (รหัสพนักงาน EMP-00123 · วันเริ่มงาน 1 มี.ค. 2562 · โทรศัพท์ 08X-XXX-4567) | ☐ |
| 2 | VERIFY section RESTRICTED | — | หัวข้อ "**ข้อมูลจำกัดสิทธิ์ (RESTRICTED · ปิดบังตามตนเอง)**" · เลขบัตร ปชช. = **X-XXXX-XXXXX-56-7** + ปุ่ม "แสดง" · บัญชีธนาคาร = ธนาคารกสิกรไทย ••••••3456 | ☐ |
| 3 | CLICK ปุ่ม "แสดง" (ท้ายเลขบัตร) | — | เลขบัตรเปลี่ยนเป็นเต็ม **1-2345-67890-56-7** · บัญชีเปลี่ยนเป็น **123-4-53456-7** · ปุ่มเปลี่ยนข้อความเป็น "ซ่อน" | ☐ |
| 4 | CLICK ปุ่ม "ซ่อน" | — | กลับเป็น masked (X-XXXX-XXXXX-56-7 / ••••••3456) | ☐ |
| 5 | VERIFY section audit | — | "**ประวัติการเข้าถึงข้อมูลของฉัน (append-only)**" มีแถว เช่น "25 ก.ค. 2568 09:12 · เปิดดูสลิป PS-2568-07 (ของตนเอง)" + note "**บันทึกการเข้าถึงถูกเพิ่มอัตโนมัติ (แก้/ลบไม่ได้)**" | ☐ |
| 6 | VERIFY audit ไม่มีปุ่มแก้/ลบ | — | แต่ละ audit row ไม่มีปุ่มลบ/แก้ (append-only) · footer มี "ปิด" + "ยื่นคำขอ" (ไม่มี save) | ☐ |

---

## Group F — แจ้งเตือน + ค้นหา/กรอง (FN-09 / FN-90)

### TC-N01 — feed แจ้งเตือนของฉัน (consume) (happy · XT-03/LK-6)
- group: แจ้งเตือน · ความสำคัญ: กลาง · trace: FN-09 / AT-09 / XT-03 / LK-6
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=notifications 4 แถว (N-104..101 · unread=N-104,N-103) จาก ENG-NOTIFY · files=—
- Start: OPEN พอร์ทัล ESS · CLICK แท็บ "แจ้งเตือน"
- ผ่านเมื่อ: feed แสดง read + มี search + filter ทั้งหมด/ยังไม่อ่าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section "แจ้งเตือนของฉัน" | — | sub "การแจ้งเตือนล่าสุดของฉัน" + chip [ASSUMED]/"อ่านอย่างเดียว" | ☐ |
| 2 | VERIFY controls | — | ช่องค้นหา placeholder "**ค้นหาการแจ้งเตือน**" + ปุ่ม "**ทั้งหมด**" (active) + "**ยังไม่อ่าน**" | ☐ |
| 3 | VERIFY feed | — | เห็น 4 แถว เช่น "สลิปเงินเดือนเดือนกรกฎาคมออกแล้ว" · "คำขอลาพักร้อนได้รับการอนุมัติ" · แถว unread มีจุดสถานะ | ☐ |
| 4 | VERIFY | — | ไม่มีปุ่ม "ทำเครื่องหมายอ่านแล้ว"/mark-read ที่เขียนกลับ (ESS consume/display เท่านั้น · ESS ไม่ยิง event) | ☐ |

### TC-N02 — ค้นหาแจ้งเตือน เจอ (happy · FN-90)
- group: แจ้งเตือน · ความสำคัญ: กลาง · trace: FN-90 / AT-12
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=notifications 4 แถว · files=—
- Start: แท็บ "แจ้งเตือน"
- ผ่านเมื่อ: พิมพ์คำค้นที่ตรง → เหลือเฉพาะแถวที่ match

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง "ค้นหาการแจ้งเตือน" | DS-NOTIF: `สลิป` | feed กรองเหลือแถวที่มีคำว่า "สลิป" — เห็น "สลิปเงินเดือนเดือนกรกฎาคมออกแล้ว" | ☐ |
| 2 | VERIFY | — | แถวที่ไม่เกี่ยว (เช่น "แจ้งเตือนอบรมประจำปี") หายไปจาก feed | ☐ |

### TC-N03 — ค้นหาไม่พบ → empty state (edge · FN-90/VR-4/EC-04)
- group: แจ้งเตือน · ความสำคัญ: กลาง · trace: FN-90 / AT-12 / VR-4 / EC-04
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=notifications 4 แถว · files=—
- Start: แท็บ "แจ้งเตือน"
- ผ่านเมื่อ: คำค้นไม่ตรง → empty state (ไม่ใช่ error)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง "ค้นหาการแจ้งเตือน" | DS-NOTIF: `zzzไม่มีจริง` | feed ว่าง | ☐ |
| 2 | VERIFY empty state | — | แสดง "**ไม่พบการแจ้งเตือน**" + "**ลองล้างคำค้นหรือตัวกรอง**" (ไอคอน bell-off) — ไม่ใช่ข้อความ error สีแดง/หน้าพัง | ☐ |
| 3 | Clear คำค้น (ลบข้อความในช่อง) | (ว่าง) | feed กลับมาแสดง 4 แถวเดิม | ☐ |

### TC-N04 — filter ยังไม่อ่าน / ทั้งหมด (happy · FN-90)
- group: แจ้งเตือน · ความสำคัญ: กลาง · trace: FN-90 / AT-09
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=notifications (unread=2: N-104,N-103) · files=—
- Start: แท็บ "แจ้งเตือน"
- ผ่านเมื่อ: ปุ่ม "ยังไม่อ่าน" กรองเหลือ unread · "ทั้งหมด" คืนทั้งหมด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึกจำนวนแถว "ทั้งหมด" | — | จด: feed แสดง 4 แถว (อ้างใน step ถัดไป) | ☐ |
| 2 | CLICK ปุ่ม "ยังไม่อ่าน" | — | ปุ่มกลาย active · feed เหลือ **2 แถว** (N-104 "สลิป…", N-103 "คำขอลาพักร้อน…") — น้อยกว่าที่จดใน step 1 | ☐ |
| 3 | CLICK ปุ่ม "ทั้งหมด" | — | feed กลับเป็น 4 แถว = เท่าที่จดใน step 1 | ☐ |

### TC-N05 — เปิดรายละเอียดแจ้งเตือน (read drawer) (happy)
- group: แจ้งเตือน · ความสำคัญ: ต่ำ · trace: FN-09 / AT-09
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=N-104 · files=—
- Start: แท็บ "แจ้งเตือน"
- ผ่านเมื่อ: คลิกแถว → drawer อ่านอย่างเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "สลิปเงินเดือนเดือนกรกฎาคมออกแล้ว" | — | drawer เปิด eyebrow "แจ้งเตือน" · title = หัวข้อแจ้งเตือน · เนื้อ "ดูสลิป PS-2568-07 ได้ที่แท็บเงินเดือน & เวลา" | ☐ |
| 2 | VERIFY footer | — | ปุ่ม "ปิด" เท่านั้น (read-only) | ☐ |

### TC-N06 — filtered-empty (unread + คำค้นไม่ตรง) (edge · VR-4)
- group: แจ้งเตือน · ความสำคัญ: ต่ำ · trace: FN-90 / VR-4 / EC-04
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=notifications · files=—
- Start: แท็บ "แจ้งเตือน"
- ผ่านเมื่อ: กรอง unread + พิมพ์คำที่ unread ไม่มี → empty state

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ยังไม่อ่าน" | — | feed เหลือ 2 แถว unread | ☐ |
| 2 | TYPE → ช่อง "ค้นหาการแจ้งเตือน" | `อบรม` | "แจ้งเตือนอบรมประจำปี" เป็น read (unread=false) จึงไม่อยู่ในชุด unread → feed ว่าง | ☐ |
| 3 | VERIFY empty state | — | "ไม่พบการแจ้งเตือน" + "ลองล้างคำค้นหรือตัวกรอง" | ☐ |

---

## Group G — self-access / masking / audit (FN-10 / FN-94 / FN-93)

### TC-SEC01 — เข้าถึงข้อมูลพนักงานอื่น → 403 modal (permission/error · FN-10/EC-01/ERR-403-SELF/VR-3)
- group: security · ความสำคัญ: สูง · trace: FN-10 / AT-10 / EC-01 / VR-3 / BR-06 / LK-4 / ERR-403-SELF
- actor (role): พนักงาน (self)
- Setup: role=employee(self · สมชาย ใจดี) · seed=persona · files=— · **หมายเหตุ:** ปุ่ม trigger เป็น `.demo-only` (prod strips) — เคสนี้ทดสอบพฤติกรรม guard บนจอ demo
- Start: OPEN พอร์ทัล ESS · tab "หน้าหลัก" (persona/demo strip แสดง)
- ผ่านเมื่อ: กดปุ่มสาธิต → modal 403 พร้อมข้อความปิดบัง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY demo strip (demo-only) | — | เห็น "ตัวอย่าง (persona)" + "สจ สมชาย ใจดี · พนักงาน" + ปุ่ม "**ทดสอบเข้าถึงข้อมูลพนักงานอื่น**" | ☐ |
| 2 | CLICK ปุ่ม "ทดสอบเข้าถึงข้อมูลพนักงานอื่น" | — | modal เปิด หัวข้อ "**เข้าถึงถูกปฏิเสธ**" + subtitle "**พนักงานเห็นได้เฉพาะข้อมูลของตนเอง**" | ☐ |
| 3 | VERIFY เนื้อ modal | — | เลข "**403**" ตัวใหญ่ + "**คุณ (สมชาย ใจดี) ไม่มีสิทธิ์เข้าถึงข้อมูลของพนักงานคนอื่น ระบบปิดบังและไม่แสดงข้อมูลนอกขอบเขตของคุณ**" | ☐ |
| 4 | VERIFY | — | ไม่มีข้อมูลของพนักงานคนอื่นแสดงเบื้องหลัง/ใน 403 (ไม่ leak field) | ☐ |
| 5 | CLICK ปุ่ม "เข้าใจแล้ว" | — | modal ปิด กลับหน้าเดิม | ☐ |

### TC-SEC02 — enforce self-access ที่ backend (employee_id ผ่าน param → 403) (permission/error · EC-10/OQ-ESS-05/NEG-04) (ต้อง simulate)
- group: security · ความสำคัญ: สูง · trace: FN-10 / EC-10 / VR-3 / NEG-04 / OQ-ESS-05
- actor (role): พนักงาน (self · A) พยายามเข้าถึงข้อมูลพนักงาน B
- Setup: role=employee(self=A · เช่น EMP-00123) · seed=พนักงาน B (id อื่น เช่น EMP-00999) มีอยู่จริงในระบบ · files=— · **ต้อง simulate:** ยิง request read (API GET) โดยแนบ employee_id ของ B ผ่าน URL/param (ไม่มีปุ่มบนจอ — ทดสอบระดับ backend/DevTools)
- Start: (backend) เรียก endpoint aggregate read ด้วย employee_id = B
- ผ่านเมื่อ: server คืน 401/403 · ไม่ leak field ใดของ B (spec `[AI-DEFAULT]` = server-side guard ทุก read)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (simulate) ยิง GET read แนบ employee_id=B | id พนักงาน B | ตอบกลับ HTTP **403 (หรือ 401)** — ไม่ใช่ 200 พร้อมข้อมูล B | ☐ |
| 2 | VERIFY payload ที่ตอบกลับ | — | ไม่มี field ข้อมูลของ B รั่วออกมา (ไม่มีชื่อ/สลิป/เลขบัตรของ B) | ☐ |
| 3 | VERIFY (ถ้ามี UI) | — | ถ้ามีการ redirect/แสดงผลบน UI ต้องเป็น 403 ปิดบัง ไม่แสดงข้อมูล B | ☐ |

> ⚠ ถ้า prototype ไม่มี backend จริง ให้ mark **BLOCKED (ต้อง simulate)** — เป็นข้อ **blocking OQ-ESS-05** ก่อน dev sign-off (enforce ต้องอยู่ที่ server ไม่ใช่แค่ UI demo TC-SEC01).

### TC-SEC03 — ไม่มีข้อมูลนอกขอบเขต self แสดงที่ใด (permission · FN-94/AT-15/BR-06)
- group: security · ความสำคัญ: สูง · trace: FN-94 / AT-15 / BR-06 / LK-4 / BR-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self · EMP-00123) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS · เดินทุกแท็บ
- ผ่านเมื่อ: ทุก surface แสดงเฉพาะข้อมูลของ EMP-00123 · ไม่มีทางเลือกดูพนักงานอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทุกแท็บ (home/pay/docs/notify) | — | ชื่อ/รหัส/สลิป/ลา/เบิก/โปรไฟล์ = ของ สมชาย ใจดี · EMP-00123 ทั้งหมด | ☐ |
| 2 | VERIFY | — | ไม่มี dropdown/ช่องค้นหา "เลือกพนักงาน" · ไม่มีเมนู "ทีมของฉาน"/"ลูกน้อง" (Manager self-service = NS-4 นอกขอบเขต) | ☐ |
| 3 | VERIFY | — | ไม่มีปุ่มอนุมัติ/ตีกลับคำขอ (ESS ไม่มี approval — approver = owner feature) | ☐ |

### TC-SEC04 — masking default (RESTRICTED ปิดบังตั้งต้น) (permission · VR-2/BR-08)
- group: security · ความสำคัญ: สูง · trace: FN-08 / VR-2 / BR-08
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=โปรไฟล์ RESTRICTED · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · section "ข้อมูลส่วนตัว / โปรไฟล์"
- ผ่านเมื่อ: ค่า RESTRICTED เริ่มต้น = masked (ต้องกด "แสดง" ก่อนจึงเห็นเต็ม)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เลขบัตรในหน้า docs | — | ตั้งต้น masked "X-XXXX-XXXXX-56-7" + chip "ปิดบัง" (ไม่ reveal อัตโนมัติ) | ☐ |
| 2 | CLICK "ดูโปรไฟล์" → VERIFY ค่าเริ่มต้นใน drawer | — | เลขบัตร/บัญชี เริ่มต้น masked ทุกครั้งที่เปิด drawer (reveal ไม่ค้างข้ามการเปิดใหม่) | ☐ |

### TC-SEC05 — self-access event เข้า SecC pipe (CSQ) (cross-module · XT-04/FN-93) (ต้อง simulate · [ASSUMED])
- group: security · ความสำคัญ: กลาง · trace: XT-04 / FN-93 / BR-08 / OQ-ESS-01
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=ENG-CSQ SecC pipe รับ event · files=— · **ต้อง simulate:** ตรวจ event ที่ ESS emit เมื่อเปิดดูข้อมูล RESTRICTED/ถูก denied — **event id [ASSUMED · OQ-ESS-01]** (CSQ_BRIEF ประกาศ `ess.self_access` · HTML anchor `ess.restricted_view` / `ess.access_denied`) — ต้อง reconcile กับ ENG-CSQ owner ก่อน sign-off
- Start: เปิด drawer โปรไฟล์ (reveal RESTRICTED) และ trigger 403
- ผ่านเมื่อ: มี self-access event ยิงเข้า SecC (สังเกตจาก audit row / log ฝั่ง SecC เท่าที่ตรวจได้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "ดูโปรไฟล์" → CLICK "แสดง" (reveal เลขบัตร) | — | (simulate) มี event self-access/restricted_view เข้า SecC pipe · เพิ่ม access-audit row (append-only) | ☐ |
| 2 | VERIFY audit row เพิ่ม | — | ประวัติการเข้าถึงมีรายการเปิดข้อมูลของตนเองเพิ่ม (append-only · แก้/ลบไม่ได้) | ☐ |
| 3 | VERIFY (simulate) event id | — | event id ตรงกับที่ ENG-CSQ owner ยืนยัน — **ยังเป็น [ASSUMED] จนกว่า OQ-ESS-01 ปิด** (mark PENDING ถ้ายังไม่ยืนยัน) | ☐ |

> ⚠ event id ปลายทางยังไม่ยืนยัน (OQ-ESS-01) → mark **BLOCKED/PENDING** ถ้า reconcile ยังไม่เสร็จ. ห้ามถือว่า fail = โค้ดผิด — เป็น open contract.

---

## Group H — overlay / deep-link / responsive / degrade / [ASSUMED] (FN-11 / FN-92 / XT)

### TC-X01 — action-picker เดิน 5 deep-link (navigate-out) ครบ (happy/negative · XT-01/BR-03/NEG-02)
- group: overlay/deep-link · ความสำคัญ: สูง · trace: XT-01 / BR-03 / NEG-02 / LK-2 / permission(self navigate allow)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: OPEN พอร์ทัล ESS · CLICK ปุ่ม "ยื่นคำขอ" (เปิด M-01)
- ผ่านเมื่อ: แต่ละแถวใน picker → toast นำทางตรง label · ไม่มี form ในพอร์ทัล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ยื่นคำขอ" | — | modal action-picker เปิด (5 แถว) | ☐ |
| 2 | CLICK แถว "ขอลา" | — | modal ปิด + WAIT toast "**กำลังนำทางไปหน้า "การลา"**" | ☐ |
| 3 | CLICK "ยื่นคำขอ" → CLICK "ขอทำงานล่วงเวลา (OT)" | — | toast "**กำลังนำทางไปหน้า "ขอทำงานล่วงเวลา"**" (prod = `#/ot/new` [ASSUMED]) | ☐ |
| 4 | CLICK "ยื่นคำขอ" → CLICK "ขอเบิกค่าใช้จ่าย" | — | toast "**กำลังนำทางไปหน้า "เบิกค่าใช้จ่าย"**" | ☐ |
| 5 | CLICK "ยื่นคำขอ" → CLICK "ขอแก้ข้อมูลส่วนตัว" | — | toast "**กำลังนำทางไปหน้า "แก้ไขข้อมูลพนักงาน (ขออนุมัติ)"**" | ☐ |
| 6 | CLICK "ยื่นคำขอ" → CLICK "ขอหนังสือรับรอง" | — | toast "**กำลังนำทางไปหน้า "หนังสือรับรอง"**" | ☐ |
| 7 | VERIFY | — | ทุกครั้ง modal ปิดแล้ว navigate (toast) — **ไม่มี form/submit เปิดในพอร์ทัลเลย** | ☐ |

### TC-X02 — deep-link fallback เมื่อ route ปลายทางยังไม่พร้อม (edge/error · XT-02/EC-07/ERR-LINK-NA/VR-1) (ต้อง simulate)
- group: overlay/deep-link · ความสำคัญ: กลาง · trace: XT-02 / EC-07 / ERR-LINK-NA / VR-1 / OQ-ESS-03 `[AI-DEFAULT]`
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=route ปลายทาง (เช่น leave) config = "ยังไม่พร้อม/ไม่ resolve" · files=— · **ต้อง simulate:** ทำให้ resolveDeepLink คืน route ที่ไม่พร้อม
- Start: กด deep-link ที่ route ยังไม่พร้อม
- ผ่านเมื่อ: แสดง graceful notice + คงหน้า ESS (ไม่ค้าง · ไม่โชว์ route/contract ดิบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK deep-link (route ยังไม่พร้อม · simulate) | — | แสดง graceful notice/toast (ไม่ throw · ไม่หน้าขาว) | ☐ |
| 2 | VERIFY | — | ยังอยู่หน้า ESS (ไม่ค้าง/ไม่ redirect ผิด) · ข้อความไม่โชว์ route/contract ดิบ (`[AI-DEFAULT]` ปลอดภัย) | ☐ |

> `[AI-DEFAULT]` (OQ-ESS-03): เกณฑ์ "graceful ไม่ค้าง" ตัดสินโดย AI conservative default — fail อาจแปลว่า default ต้องปรับ ไม่ใช่โค้ดผิด.

### TC-X03 — responsive มือถือ (edge · FN-92/AT-13/BR-05)
- group: ทั่วไป · ความสำคัญ: กลาง · trace: FN-92 / AT-13 / BR-05 / EC-05
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=— · viewport มือถือ (กว้าง ≤760px)
- Start: OPEN พอร์ทัล ESS ที่ความกว้างมือถือ
- ผ่านเมื่อ: layout usable · ไม่ล้นแนวนอน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN พอร์ทัล ESS (viewport 390px) | — | sidebar ยุบ/off-canvas · เนื้อหาเต็มความกว้าง · ไม่มี horizontal scroll ของทั้งหน้า | ☐ |
| 2 | VERIFY seg-tabs + ตาราง | — | seg-tabs 4 อันยังกดสลับได้ · ตาราง (สลิป/กะ/เบิก) อ่านได้ (ตารางเลื่อนแนวนอนภายในกล่องของตัวเองได้) | ☐ |
| 3 | CLICK แถวสลิป → VERIFY drawer | — | drawer เปิดเต็มความกว้างจอมือถือ (min(680px,100vw)) · footer "ปิด" กดได้ | ☐ |

### TC-X04 — ไม่มีการยิง notification event / ไม่มี write path (negative · NEG-05/LK-6) (ต้อง simulate)
- group: ทั่วไป · ความสำคัญ: กลาง · trace: NEG-05 / LK-6 / BR-01 / permission(no approve)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=— · **ต้อง simulate:** ดัก network (DevTools) ขณะใช้พอร์ทัล
- Start: OPEN พอร์ทัล ESS · เดินทุกแท็บ + เปิด drawer + กด deep-link
- ผ่านเมื่อ: ไม่มี POST/PUT/PATCH/DELETE ออกจาก ESS · ไม่มี event ยิงเข้า ENG-NOTIFY (consume only)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (simulate) network ขณะเปิดแท็บ/drawer | — | request มีแต่ **GET** (aggregate read) — ไม่มี mutation POST/PUT/DELETE | ☐ |
| 2 | VERIFY (simulate) ตอนกด deep-link | — | ESS ไม่ยิง event สร้างคำขอ/notification — เป็นแค่ navigate (toast prototype) | ☐ |
| 3 | VERIFY | — | ไม่มีปุ่ม mark-read ที่เขียนกลับ ENG-NOTIFY · feed = consume/display เท่านั้น | ☐ |

> ถ้าไม่มี backend/network จริงใน prototype → mark **BLOCKED (ต้อง simulate)** แต่ยืนยันเชิงโครงสร้างได้ว่า UI ไม่มีปุ่ม write ใด (verify by absence).

### TC-X05 — surface ba-done = display-only + [ASSUMED contract] chip (edge · FN-11/AT-11/BR-07/LK-5) (demo)
- group: ทั่วไป · ความสำคัญ: กลาง · trace: FN-11 / AT-11 / BR-07 / VR-1 / LK-5
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=— · **หมายเหตุ:** chip [ASSUMED] เป็น `.demo-only` (prod strips) — เคสตรวจว่า soft-ref surface ไม่ทำหน้าพัง
- Start: OPEN พอร์ทัล ESS · แท็บ "เงินเดือน & เวลา" / "เอกสาร & สิทธิ์"
- ผ่านเมื่อ: section ของ owner ที่ยัง ba-done แสดง display-only + chip [ASSUMED] · หน้าไม่พัง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY chip บน section soft-ref | — | section (สลิป/ลา/OT/กะ/เบิก/cert/สวัสดิการ/โปรไฟล์) มี chip "**[ASSUMED contract]**" (demo) | ☐ |
| 2 | VERIFY | — | section ยังแสดงข้อมูล read ได้ตามปกติ (display-only) · หน้าไม่ error/ไม่พัง แม้ contract ยังไม่ยืนยัน (BR-07 degrade) | ☐ |

### TC-X06 — surface ต้นทาง down/timeout → per-card degrade (edge/error · XT-05/EC-08/ERR-DEGRADED) (ต้อง simulate)
- group: ทั่วไป · ความสำคัญ: กลาง · trace: XT-05 / EC-08 / ERR-DEGRADED / OQ-ESS-04 `[AI-DEFAULT]`
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=owner surface หนึ่ง (เช่น payroll) down/timeout · files=— · **ต้อง simulate:** ทำให้ read ของ surface หนึ่ง fail
- Start: OPEN พอร์ทัล ESS ขณะ surface หนึ่ง down
- ผ่านเมื่อ: card/section นั้นแสดง "โหลดไม่ได้" · surface อื่นยังทำงาน · หน้าไม่ล้มทั้งหน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN พอร์ทัล ESS (surface payroll down · simulate) | — | การ์ด/section สลิปแสดงสถานะ degrade "**โหลดไม่ได้**" (ต่อ card) | ☐ |
| 2 | VERIFY surface อื่น | — | โควตาลา/OT/แจ้งเตือน ยังโหลดและแสดงปกติ (ไม่ throw ทั้งหน้า · try/catch ต่อ surface) | ☐ |

### TC-X07 — Esc chain: modal ทับ drawer ปิด modal ก่อน (overlay · DSP-01)
- group: overlay · ความสำคัญ: กลาง · trace: 01_UI §1.6 / DSP-01 / M-01 · (เพิ่มเติม — overlay layering)
- actor (role): พนักงาน (self)
- Setup: role=employee(self) · seed=persona · files=—
- Start: แท็บ "เอกสาร & สิทธิ์" · เปิด drawer โปรไฟล์ ("ดูโปรไฟล์")
- ผ่านเมื่อ: action-picker เปิดทับ drawer ได้ · Esc ปิด modal ก่อน (drawer ยังเปิด) · Esc อีกครั้งปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "ดูโปรไฟล์" | — | drawer โปรไฟล์เปิด (footer มีปุ่ม "ยื่นคำขอ") | ☐ |
| 2 | CLICK ปุ่ม "ยื่นคำขอ" (ใน footer drawer) | — | modal action-picker เปิด **ทับ** drawer (modal อยู่เหนือ drawer · layering ถูก · DSP-01) | ☐ |
| 3 | PRESS Esc | — | **modal ปิดก่อน** — drawer โปรไฟล์ยังเปิดอยู่ (ปิดทีละชั้นบนสุด) | ☐ |
| 4 | PRESS Esc | — | คราวนี้ drawer โปรไฟล์ปิด กลับหน้า "เอกสาร & สิทธิ์" | ☐ |
| 5 | (ทางเลือก) เปิด picker ใน drawer อีกครั้ง → CLICK แถวใดแถวหนึ่ง | — | modal + drawer ปิดทั้งคู่ + toast นำทาง (deepLink ปิด overlay ทั้งสอง) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. **Login เป็น self persona** = สมชาย ใจดี · EMP-00123 (ทุกเคส role=employee/self). Feature นี้ไม่มี role อื่น (ไม่มี admin/manager · NS-4).
2. เปิดพอร์ทัลจากเมนูซ้าย **"ESS ของฉัน"**. Internal nav = **ปุ่ม seg-tab** (หน้าหลัก/เงินเดือน & เวลา/เอกสาร & สิทธิ์/แจ้งเตือน) — ไม่ใช่ URL hash.
3. รันเคสตามกลุ่ม A→H. ทุกเคส **refresh-safe** (เริ่มจาก Start ของตัวเอง — เปิดพอร์ทัลใหม่/สลับแท็บ ไม่พึ่ง state ค้าง).
4. **Anchor ด้วยข้อความบนจอ** (verbatim ในตาราง) — อย่าเดา. ปุ่ม/หัวข้อ/toast ตรงตามที่ระบุ.
5. เคสที่มี **(ต้อง simulate)** = ต้องมี backend/network/inject เงื่อนไข (TC-SEC02/SEC05/X02/X04/X06). ถ้า prototype ทำไม่ได้ → mark `blocked` + note เหตุผล (ห้ามรายงาน pass ลอย ๆ).
6. **DEMO-ONLY:** ปุ่มทดสอบ 403 + chip [ASSUMED]/อ่านอย่างเดียว เป็น demo (prod strips). เคสที่พึ่ง element เหล่านี้ (TC-SEC01/X05) mark demo — พฤติกรรมสิทธิ์จริงยืนยันที่ TC-SEC02 (backend).
7. Toast มีเวลาแสดง ~3.2s — ใช้ `WAIT` ก่อน VERIFY.
8. กรอกผลลง `Result Report (schema)` ท้ายไฟล์ · `evidence` = สิ่งที่เห็นจริงตอน fail/blocked.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FN (FUNCTION_CHECKLIST · QA lane) | 15 / 15 |
| Acceptance Tests (06_TESTS §6.1 AT) | 15 / 15 |
| Business rules (05_RULES §5.1 BR) | 8 / 8 |
| Validation rules (VR) | 5 / 5 |
| Edge cases (EC) | 9 / 11 (ข้าม 2 พร้อมเหตุผล) |
| Error codes | 3 / 4 (ข้าม ERR-404 พร้อมเหตุผล) |
| Permission cells | 5 / 5 |
| Negative / Guard (NEG) | 5 / 5 |
| Scope Lock (LK) | 6 / 6 |
| Cross-cutting / states | ครบ (banner · empty · filtered-empty · overlay Esc chain) |

- **Cross-Module (XT): 5 / 5** (XT-02/04/05 = ต้อง simulate · XT-04 event id [ASSUMED · OQ-ESS-01])
- **Scope Lock (LK): 6 / 6** — ทุก LOCK มีเคส verify
- **FN cross-check: ✅ 15/15** (FN-01..11 + FN-90/92/93/94)
- **Manifest cross-check (FRD §0.12): ✅ 15/15** — ทุกแถว FN ใน Coverage Manifest มีคู่ใน Ledger; Scenarios S-01..11 mapped ผ่าน FN rows; Rules BR-01..08 ครบ

### ข้าม (พร้อมเหตุผล)
- **EC-09** (session หมดกลาง drawer RESTRICTED → re-auth) — ○Optional (P6) · OQ-ESS-06 · หลังบ้าน/ไม่มีผล UI คงที่ให้ agent สังเกต → ข้าม (Phase 2 optional)
- **EC-11** (สลิป PDF ต้นทางยังไม่ออก → ปุ่มดาวน์โหลด disabled) — prototype ไม่มีปุ่มดาวน์โหลด PDF (สลิปอ่านในพอร์ทัลเท่านั้น) · OQ owner Payroll → ข้าม (ไม่มี element ให้ทดสอบในรอบนี้)
- **ERR-404** (record ไม่มี) — มาตรฐาน · prototype seed คงที่ ไม่มี state ให้ trigger 404 บน UI → ข้าม (ต้อง simulate ถ้า backend จริง)
- **Out of Scope (NS-1..6 · Scope Lock Exclusions)** — ไม่สร้างเคส "ทดสอบ": สร้าง/แก้/ลบ feature อื่น · ฟอร์มยื่นในพอร์ทัล · ออกสลิป/PDF เอง · Manager self-service/อนุมัติ · config เมนู/สิทธิ์ · เลขรัน/สายอนุมัติ. ครอบด้วย negative (verify-by-absence) ที่ TC-P03/D02/E05/SEC03/X04 แทน.

### หมายเหตุ blocking (ก่อน dev sign-off · 06_TESTS §6.4 DoD)
- **OQ-ESS-01** (CSQ event id) → TC-SEC05 ยัง [ASSUMED]/PENDING
- **OQ-ESS-02** (5 deep-link routes) → TC-X01/L03/E02/E04/E07 toast ถูก แต่ route ปลายทาง [ASSUMED]
- **OQ-ESS-05** (backend self-enforce) → TC-SEC02 ต้อง simulate · เป็น blocking PII

---

## Result Report (schema)

```json
{
  "feature_id": "F-HR-ESS",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-H01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-H02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-H03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-H04", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-H05", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-P01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-P02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-P03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-P04", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-L02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-L03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-D01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-D02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E04", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E05", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E06", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E07", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-E08", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-N01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-N02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-N03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-N04", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-N05", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-N06", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-SEC01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-SEC02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "(ต้อง simulate · blocking OQ-ESS-05)" },
    { "id": "TC-SEC03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-SEC04", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-SEC05", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "(ต้อง simulate · event id [ASSUMED] OQ-ESS-01)" },
    { "id": "TC-X01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-X02", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "(ต้อง simulate · [AI-DEFAULT] OQ-ESS-03)" },
    { "id": "TC-X03", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" },
    { "id": "TC-X04", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "(ต้อง simulate network)" },
    { "id": "TC-X05", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "(demo-only chip)" },
    { "id": "TC-X06", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "(ต้อง simulate · [AI-DEFAULT] OQ-ESS-04)" },
    { "id": "TC-X07", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 40, "pass": 0, "fail": 0, "blocked": 0 }
}
```
