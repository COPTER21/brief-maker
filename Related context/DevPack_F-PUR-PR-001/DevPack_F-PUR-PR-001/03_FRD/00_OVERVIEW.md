# 00_OVERVIEW — F-PUR-PR · PR ใบขอซื้อ

## §0.1 Document Control

| หัวข้อ | ค่า |
|---|---|
| Feature | **F-PUR-PR** · PR ใบขอซื้อ (Purchase Requisition) · registry fid **F072** |
| Module | Purchase (จัดซื้อ) · CUBE 4.0 Core ERP |
| Archetype (registry `arch`) | **Q-document** — Pattern Q + B2 v2 line editor |
| Declarations (registry `dec`) | `doa` ⚖ · `ntf` 🔔 · `csq` ◆ · `doccfg` · `pdfdoc` 📄 — **ครบ 5 ชิป** |
| Wave / automation | W2 · `auto: lite` → **WF-01 Mode B** (Phase A มาจาก BA lane · เลนนี้ทำ Phase B) |
| **Pack Variant** | **FULL** (9 files + INDEX) |
| เหตุผล variant | fallback จาก BRD: pages=3 (+6 overlay), **states=5** (≥4 → FULL), approval=**Yes**, money=**Yes** (VAT 3 โหมด · ส่วนลด 2 ชั้น · WHT) |
| Upstream | `02_BRD/BRD_F-PUR-PR.md` **APPROVED** (C01–C23 · 23/23) · `01_HTML/F-PUR-PR.html` ผ่าน re-gate ขั้น 7R |
| Sync Read | `html-generator-v9` — SKILL.md · `knowledge/iron-rules.md` · `patterns/Q_transaction-document-archetype.md` |
| วันที่ | 2026-09-13 · **ปี ค.ศ. ทุกจุด** (LOCK-YEAR) |
| สถานะ | Phase B — FRD Pack |

> **HTML-first (R14):** HTML คือ source of truth ของหน้าจอ · FRD **สกัด+ตรวจ+บันทึก** ไม่แต่ง spec สวนจอ
> อยากเปลี่ยนอะไรบนจอ → Open Question เท่านั้น

## §0.2 Scope

### In Scope
I1 หน้ารายการ + ค้นหา/กรอง + แถบเอกสารแนบรวม · I2 wizard 5 ขั้น · I3 B2 v2 line editor ·
I4 เอกสารแนบ · I5 ส่งอนุมัติผ่าน DOA slot picker (คนจริง) · I6 หน้าดูเอกสาร 4 แท็บ ·
I7 อนุมัติ/ไม่อนุมัติ/เรียกคืน/ยกเลิก/ทำสำเนา · I8 ตรวจงบ **จำลอง** (เตือนอย่างเดียว)

### Out of Scope
O1 ควบคุมงบจริง (F117 · W7) · O2 เทียบราคาผู้ขาย (F073) · O3 ใบสั่งซื้อ/รับของ/ตั้งหนี้/จ่ายเงิน (W3/W5/W6) ·
O4 ทยอยออก PO จาก PR ใบเดียว · O5 ตั้งค่าสายอนุมัติ (F019) · O6 ตั้งค่าเลขเอกสาร (F-DOCCFG) · O7 เลือกช่องทางแจ้งเตือน (F-NOTIFY)

## §0.3 Roles

ผู้ขอซื้อ · หัวหน้าหน่วยงาน · ผู้จัดการฝ่ายจัดซื้อ · ผู้บริหารการเงิน · เจ้าหน้าที่จัดซื้อ (ดูอย่างเดียว) · ผู้ตรวจสอบ (ดูอย่างเดียว)
Permission matrix เต็ม: BRD §4.2 · **กติกาแกน: ผู้ขอเซ็นอนุมัติใบของตัวเองไม่ได้ (BR-03 · แบ่งแยกหน้าที่)**

## §0.4 Dependencies

| Dependency | สถานะ | วิธีจัดการ |
|---|---|---|
| ทะเบียนผู้ขาย F007 · สินค้า F009/F010 · ศูนย์ต้นทุน F012 · หน่วยนับ | เสร็จแล้ว | **soft-reference** — ตัวเลือกเท่านั้น ไม่ผูกคีย์ ไม่ตรวจความมีอยู่ ว่างได้ (LOCK-SR) |
| ทะเบียน DOA F019 | เสร็จแล้ว | อ่านตอนส่งอนุมัติ · feature ประกาศ + แสดงตัวเลือกคน |
| `ENG-DOC-NUM` / `ENG-DOC-STORE` | กลาง | เรียกผ่านบริการกลาง **ห้ามสร้างเลขเอง** |
| `ENG-NOTIFY` | กลาง | ประกาศเหตุการณ์ **ห้ามเลือกช่องทางเอง** |
| `ENG-CSQ` (7C) | กลาง | ประกาศ 2 event (EC) |
| **F117 Budget Control (W7)** | **ยังไม่มี** | **จำลอง + `TODO: budget-control hook`** — ห้าม implement ห้ามรอ (LOCK-FW) |

## §0.5 Security Preset

**Internal-Sensitive** — เอกสารภายในที่มีข้อมูลเชิงพาณิชย์ (ราคา · ผู้ขาย · งบ) · ไม่มีข้อมูลส่วนบุคคลอ่อนไหว
Security Bible triggers ที่ยิง: **financial-document** · **approval-workflow** · **file-upload** · **audit-trail**

## §0.7.1 Data Classification Summary

| ระดับสูงสุดที่ฟีเจอร์แตะ | **Confidential** |
|---|---|

- **Confidential:** `unit_price_est` · `subtotal` · `grand_total` · `budget_check_result` · `vendor_suggest` (ข้อมูลเชิงพาณิชย์ — ราคาประมาณและผู้ขายที่แนะนำเปิดเผยกลยุทธ์จัดซื้อ)
- **Internal:** ฟิลด์ที่เหลือเกือบทั้งหมด (เลขที่ · วันที่ · สถานะ · เหตุผล · ประวัติ)
- **PII flag:** `requester_id/name` · `approver_name/position` = **ชื่อ/ตำแหน่งพนักงานภายใน** (PII ระดับต่ำ ไม่ใช่ sensitive PDPA)
- **Restricted:** **ไม่มี** → ไม่ต้อง wire Restricted Resources registry
- รายละเอียดครบ: `04_DB §4.6`

## §0.10 ★ ใบประกาศ — ออกครบ 5 ใบตามชิป

registry F072 ประกาศ `dec: doa, ntf, csq, doccfg, pdfdoc` · **ออกครบทั้ง 5 ใบ ไม่มีใบใดตกหล่น**

| ชิป | ใบประกาศใน `03_FRD/` | ที่มา |
|---|---|---|
| ⚖ `doa` | `DOA_BRIEF_F-PUR-PR-001.md` | รับจาก `5_DECLARATIONS/` (BA lane) |
| 🔔 `ntf` | `NTF_BRIEF_F-PUR-PR-001.md` | รับจาก `5_DECLARATIONS/` |
| ◆ `csq` | `CSQ_BRIEF_F-PUR-PR-001.md` | รับจาก `5_DECLARATIONS/` — **repo นี้ไม่มี `csq-declaration` skill** จึงรับจากต้นน้ำอย่างเดียว |
| `doccfg` | `DOCCFG_BRIEF_F-PUR-PR-001.md` | รับจาก `5_DECLARATIONS/` |
| 📄 `pdfdoc` | `PRINT_SPEC_F-PUR-PR-001.md` | รับจาก `5_DECLARATIONS/` — **repo นี้ไม่มี pdfdoc spec generator** |

> **ไม่มีใบไหนที่ "ชิปมีแต่ไม่ออก"** — ไม่ต้องเขียนเหตุผลการตกหล่น
> `csq-declaration` และ `pdfdoc` generator ยังไม่มีใน repo นี้ (ช่องว่างของ toolchain — 80 และ 28 ฟีเจอร์ตามลำดับ) แต่ไม่กระทบ pack นี้เพราะ BA lane ส่งใบมาให้แล้ว

## §0.11 Scope Lock

FULL variant → Scope Lock อยู่ที่ **`07_LOCKED_DECISIONS.md §7.0`** (LOCK-Q · LOCK-B2 · LOCK-DOA · LOCK-DECL · LOCK-FW · LOCK-SR · LOCK-YEAR + HANDOFF §3 ทั้ง 10 ข้อ)

## §0.12 ★ Coverage Manifest (R13)

ทุก Story / Rule / Edge จาก BRD ต้องมีแถว — ไม่มีที่ลง = Open Question

### Stories (BRD §7)
| BRD Ref | Requirement | อยู่ที่ |
|---|---|---|
| S-01 AC-01 | กรอกไม่ครบ → ไปขั้นถัดไปไม่ได้ | `01_UI` P-02/S2 · `03_LOGIC` FN-04 · `05_RULES` V-01 · `06_TESTS` AT-01 |
| S-01 AC-02 | วันที่ต้องการใช้ < วันที่เอกสาร → บล็อก | `05_RULES` V-02 · `06_TESTS` AT-02 |
| S-01 AC-03 | ต้องมี ≥1 รายการครบ | `03_LOGIC` FN-05 · `05_RULES` V-03 · `06_TESTS` AT-03 |
| S-01 AC-04 | ออกเลขที่ตอนส่งอนุมัติ | `02_API` API-05 · `03_LOGIC` FN-08 · `05_RULES` BR-05 · `06_TESTS` AT-04 |
| S-01 AC-05 | slot picker แสดงรูป+ชื่อ+ตำแหน่ง · เลือกไม่ครบ → ปุ่มปิด | `01_UI` P-04 · `05_RULES` BR-02/V-08 · `06_TESTS` AT-05 |
| S-02 AC-06 | ไม่อยู่ในขั้นปัจจุบัน → ไม่เห็นปุ่มอนุมัติ | `03_LOGIC` FN-11 · `05_RULES` BR-03 · `06_TESTS` AT-06 |
| S-02 AC-07 | ไม่อนุมัติต้องใส่เหตุผล ≥3 ตัวอักษร | `05_RULES` V-07 · `06_TESTS` AT-07 |
| S-02 AC-08 | อนุมัติครบ → APPROVED + ประวัติครบ | `03_LOGIC` FN-09 · `06_TESTS` AT-08 |
| S-03 AC-09 | ระหว่างรออนุมัติ ปุ่มแก้ไขไม่ปรากฏ | `01_UI` P-03 · `05_RULES` BR-04 · `06_TESTS` AT-09 |
| S-03 AC-10 | เรียกคืน → ร่าง · ลายเซ็น void แต่ยังเห็นในประวัติ | `03_LOGIC` FN-10 · `05_RULES` EC-03 · `06_TESTS` AT-10 |
| S-04 AC-11 | งบไม่พอ → เตือน แต่ส่งได้ | `03_LOGIC` FN-07 · `05_RULES` BR-07 · `06_TESTS` AT-11 |
| S-04 AC-12 | ไม่เลือกศูนย์ต้นทุน → ข้ามตรวจงบ | `05_RULES` EC-02 · `06_TESTS` AT-12 |
| S-05 AC-13 | คัดลอกใบ — ไม่คัดลอกเลขที่/ลายเซ็น/ประวัติ/แนบ | `03_LOGIC` FN-12 · `06_TESTS` AT-13 |
| S-05 AC-14 | ใบไม่อนุมัติมีปุ่มทำสำเนา | `01_UI` P-03 · `06_TESTS` AT-14 |

### Business Rules (BRD §9.1)
| BRD Ref | อยู่ที่ |
|---|---|
| BR-01..BR-12 | `05_RULES §5.1` ครบทั้ง 12 ข้อ · test: `06_TESTS` AT-04/05/06/09/11 + BR-trace §6.8 |

### Validation (BRD §9.2)
| BRD Ref | อยู่ที่ |
|---|---|
| V-01..V-09 | `05_RULES §5.2` ครบ 9 ข้อ · test AT-01/02/03/07/15/16/17 |

### Edge Cases (BRD §10)
| BRD Ref | อยู่ที่ |
|---|---|
| EC-01..EC-07 (☑ ยืนยันแล้ว) | `05_RULES §5.3` ครบ 7 ข้อ · test AT-12/15/16/18/19 |
| CL-01 CL-02 CA-01 EM-01 ST-01 (☐ รอเคาะ) | `05_RULES §5.3.2` + **Open Questions §0.13** — CL-01/CL-02 มีในระบบแล้ว · CA-01 = `[AI-DEFAULT]` · EM-01/ST-01 เจ้าของคือ DOA/NOTIFY |

### Cross-module (BRD §12.1)
| ปลายทาง | อยู่ที่ |
|---|---|
| F073 เทียบราคาผู้ขาย | `02_API §2.9` XT-01 · `06_TESTS §6.9` XT-01 |
| W3 ใบสั่งซื้อ | `02_API §2.9` XT-02 · `06_TESTS §6.9` XT-02 |
| W7 ควบคุมงบ | `03_LOGIC` FN-07 (mock) · `07_LOCKED` LD-05 · `06_TESTS §6.9` XT-03 |
| 7C ประทับผล | `02_API §2.9` XT-04 · `06_TESTS §6.9` XT-04 |

**ผล: ทุก requirement มีที่ลง — ไม่มีแถวที่ "อยู่ที่" ว่าง**

### ★ §0.12.1 Function Checklist coverage — `FUNCTION_CHECKLIST` FN-01..FN-24

> ⚠️ **ระวังชนกันของรหัส:** `FN-xx` ใน **FUNCTION_CHECKLIST** = *ฟังก์ชันของฟีเจอร์ (ระดับธุรกิจ)*
> ส่วน `F-PUR-PR-FN-xx` ใน **`03_LOGIC.md`** = *ฟังก์ชันของชั้น logic (ระดับโค้ด)* — **คนละชุดรหัสกัน**
> ตารางนี้ map ชุดแรก (FN-01..FN-24 ของ checklist) เข้ากับที่อยู่ใน pack

| FN (checklist) | ฟังก์ชัน | อยู่ที่ | test |
|---|---|---|---|
| FN-01 | List PR + คอลัมน์ครบ | `01_UI §1.1` · `03_LOGIC` F-PUR-PR-FN-01 | AT-37 · AI-01 |
| FN-02 | ค้นหา + filter | `01_UI §1.1` · `03_LOGIC` F-PUR-PR-FN-01 | AI-02..AI-04 |
| FN-03 | แถบเอกสารแนบใน landing | `01_UI §1.1` | AI-07 |
| FN-04 | empty / loading / error state | `01_UI §1.1` | AT-37 · AI-05 · AI-06 |
| FN-05 | เปิด wizard 5 ขั้น | `01_UI §1.2` | AT-38 · AI-08 |
| FN-06 | Step header + validate วันที่ | `03_LOGIC` F-PUR-PR-FN-04 · `05_RULES` V-01/V-02 | AT-01 · AT-02 |
| FN-07 | Cost center picker (soft-ref) | `04_DB §4.2` · `05_RULES` EC-02 | AT-12 · AI-12 |
| FN-08 | B2 v2 line editor grid | `01_UI §1.3` | AI-18 |
| FN-09 | Item combobox + free-text | `01_UI §1.3` · `05_RULES` EC-01 | AT-19 · AI-16 · AI-17 |
| FN-10 | ส่วนลดรายบรรทัด | `03_LOGIC` ENG-PR-CALC | AT-28 · AI-22 |
| FN-11 | VAT segmented 3 โหมด | `03_LOGIC` ENG-PR-CALC | AT-29 · AI-20 |
| FN-12 | Totals ครบตามลำดับ | `01_UI §1.3` · `03_LOGIC` ENG-PR-CALC | AI-21 |
| FN-13 | เพิ่ม/ลบแถว + กันแถวว่าง | `03_LOGIC` F-PUR-PR-FN-05 · `05_RULES` V-04/V-05 | AT-15 · AT-16 |
| FN-14 | ผู้ขายแนะนำ (soft-ref) | `04_DB` `t_pr_vendor_suggest` · `05_RULES` BR-12 | AT-27 · AI-45 |
| FN-15 | แนบไฟล์ + validate | `02_API` API-11 · `03_LOGIC` F-PUR-PR-FN-15 | AT-17 · AI-25 |
| FN-16 | Step 5 สรุป read-only | `01_UI §1.2` | AI-26 |
| FN-17 | แถบตรวจงบ mock + TODO | `03_LOGIC` F-PUR-PR-FN-07 · `05_RULES` BR-07 · `07_LOCKED` LD-05 | AT-11 · AI-31 |
| FN-18 | DOA slot picker คนจริง | `01_UI §1.5` · `03_LOGIC` ENG-DOA-RESOLVE | AT-05 · AI-29 |
| FN-19 | บันทึกร่าง / ส่งอนุมัติ | `02_API` API-03/API-05 | AT-04 · AI-30 |
| FN-20 | View tab รายละเอียด + ปุ่มตามสถานะ | `01_UI §1.4` · `03_LOGIC` F-PUR-PR-FN-11 | AT-06 · AI-38 |
| FN-21 | View tab PDF (A4) | `01_UI §1.4` · `PRINT_SPEC_*` | AI-34 |
| FN-22 | View tab ลายเซ็น | `01_UI §1.4` | AT-08 · AI-35 |
| FN-23 | View tab ประวัติ append-only | `01_UI §1.4` · `05_RULES` BR-11 | AT-26 · AI-36 |
| FN-24 | อนุมัติ/ไม่อนุมัติ/เรียกคืน/ยกเลิก/คัดลอก | `02_API` API-06..API-10 | AT-07/10/13/18 · AI-40..AI-43 |

**ครบ 24/24**

### ★ §0.12.2 Scenario coverage — `PREBRIEF §5` SC-01..SC-15

| SC | สถานการณ์ | อยู่ที่ | test |
|---|---|---|---|
| SC-01 | Happy path — สร้าง → ส่ง → อนุมัติครบ | `05_RULES §5.4` · `06_TESTS §6.1` | AT-04 · AT-08 |
| SC-02 | บันทึกร่างแล้วกลับมาแก้ | `02_API` API-03/API-04 | AT-34 · AI-22 |
| SC-03 | Line เป็น free-text นอกทะเบียน | `05_RULES` EC-01 | AT-19 |
| SC-04 | ไม่อนุมัติ + เหตุผล | `05_RULES` V-07 · `02_API` API-07 | AT-07 |
| SC-05 | เรียกคืนระหว่างรออนุมัติ | `05_RULES` EC-03 · `03_LOGIC` F-PUR-PR-FN-10 | AT-10 |
| **SC-06** | ยอดเกินวงเงิน slot ที่เลือก | **`07_LOCKED` LD-10 + OQ-07** — ระบบ resolve ชั้นจากยอดอัตโนมัติ สภาวะนี้จึงเกิดไม่ได้ | AT-21 |
| SC-07 | ตรวจงบไม่ผ่าน (mock) | `05_RULES` BR-07 · EC-07 | AT-11 |
| SC-08 | แก้ไขหลังส่งอนุมัติ | `05_RULES` BR-04 | AT-09 |
| SC-09 | ยกเลิกใบที่อนุมัติแล้ว | `05_RULES` EC-04 · `02_API` API-09 | AT-18 |
| SC-10 | ไม่มีสิทธิ์อนุมัติแต่เปิดใบ | `05_RULES` BR-03 · EC-06 · `03_LOGIC` F-PUR-PR-FN-11 | AT-06 |
| SC-11 | แนบไฟล์เกินขนาด/ผิดชนิด | `05_RULES` V-06 · EC-05 | AT-17 |
| SC-12 | คัดลอกใบเดิม | `03_LOGIC` F-PUR-PR-FN-12 | AT-13 |
| SC-13 | รายการว่างแล้วส่งอนุมัติ | `05_RULES` V-03 | AT-03 |
| SC-14 | วันที่ต้องการใช้ < วันที่เอกสาร | `05_RULES` V-02 | AT-02 |
| SC-15 | List ไม่มีข้อมูล / โหลดพัง | `01_UI §1.1` states | AT-37 |

**ครบ 15/15** — โดย **SC-06 เป็นข้อเดียวที่ระบบทำคนละแบบกับถ้อยคำใน PREBRIEF** (ดู LD-10 · OQ-07)

## §0.13 Open Questions

### ยกมาจาก HANDOFF §5 (เจ้าของต้องตอบ — ห้ามเงียบ)
| OQ | เรื่อง | ค่าที่ใช้ไปก่อน | เจ้าของ |
|---|---|---|---|
| OQ-01 | ตัวเลขวงเงินอนุมัติ 3 ระดับ | 50,000 / 500,000 บาท `[ASSUMED]` | ผู้บริหารจัดซื้อ · **พี่เบิร์ด** |
| OQ-02 | แยกสายอนุมัติรายหน่วยงานไหม | ชุดเดียวทุกหน่วยงาน `[ASSUMED]` | เจ้าของกระบวนการจัดซื้อ |
| OQ-03 | ยกเลิกใบที่อนุมัติแล้วต้องอนุมัติซ้ำไหม | ไม่ต้อง (เหตุผล + ยืนยัน) `[ASSUMED]` | เจ้าของกระบวนการจัดซื้อ |
| OQ-04 | เมื่อ W7 พร้อม เปลี่ยน "เตือน" เป็น "บล็อก" ไหม | เตือนอย่างเดียว | เจ้าของ W7 + การเงิน |
| OQ-05 | หลายบริษัท/หลายสกุลเงินในเฟสถัดไป | หนึ่งบริษัท THB `[ASSUMED]` | สถาปนิกระบบ |
| OQ-06 | ผู้อนุมัติไม่อยู่ → ส่งต่อให้ใคร | ยังไม่มี | เจ้าของทะเบียน DOA |
| A-01 | รูปแบบผลตรวจงบ `{ok, remaining, budget_code}` | `[ASSUMED contract]` | เจ้าของ W7 |
| A-02 | เอกสารแนบ PDF/JPG/PNG/XLSX ≤10MB | `[ASSUMED]` | เจ้าของกระบวนการ |

### ★ เปิดใหม่ในเลนนี้ (Phase B)
| OQ | เรื่อง | เหตุผล | เจ้าของ |
|---|---|---|---|
| **OQ-07** | **ถ้อยคำ SC-06 ใน PREBRIEF ไม่ตรงกับพฤติกรรมจริง** — PREBRIEF เขียนว่า *"ยอดสุทธิเกินวงเงิน slot ที่เลือก → เตือนที่ step 5"* แต่ระบบใช้ `resolveDoa(amount)` **เลือกชั้นอนุมัติจากยอดให้อัตโนมัติ** → สภาวะ "เกินวงเงินของ slot ที่เลือก" เกิดขึ้นไม่ได้เชิงโครงสร้าง จึงไม่มีข้อความเตือนใด ๆ (`grep 'เกินวงเงิน'` = 0) · **ผลเชิงธุรกิจถูก** แต่ถ้อยคำ brief ต้องแก้ | ตรวจพบที่ขั้น 7R coverage · ดู `01_HTML/_COVERAGE_REPORT.md` W1 · ตราไว้ที่ `07_LOCKED` LD-09 | BA |
| **OQ-08** | **wizard step 3 เคยใช้ชื่อ `รายการที่ขอซื้อ` ขัด iron rule #100** — แก้กลับเป็น `รายการสินค้า` ในเลนนี้แล้ว · ถ้าทีมยืนยันว่าอยากได้ถ้อยคำที่ครอบ "บริการ/สินทรัพย์" ด้วย ต้องขอแก้ **iron rule #100 ระดับระบบ** ไม่ใช่แก้เฉพาะฟีเจอร์นี้ | `pr_type` = goods\|service\|asset · ตารางอ่านอย่างเดียวใช้หัวว่า `สินค้า / บริการ` | BA + เจ้าของ Pattern Q |
| **OQ-09** | **ปุ่มสาธิต 2 ปุ่มต้องถอดก่อน production** — `ทดสอบสถานะโหลดผิดพลาด` · `ทดสอบไฟล์ไม่ผ่านเงื่อนไข` · รอบนี้ **เก็บไว้** เพราะ QA ต้องใช้เข้าสถานะผิดพลาด (TC ของ SC-11/SC-15) | HANDOFF §4 · ตัดสินใจที่ขั้น 7R ข้อ 5 | ทีม dev ก่อน deploy |

### Probe defaults ที่ใช้ (Lane Mode · `[AI-DEFAULT]`)
| Probe | คำถาม | default ที่ใช้ | tag |
|---|---|---|---|
| PR-1 | ผู้อนุมัติ 2 คนกดพร้อมกันในขั้นเดียวกัน | **optimistic lock → 409 `PR_SLOT_ALREADY_DECIDED`** คนแรกชนะ | `05_RULES` CA-01 `[AI-DEFAULT]` |
| PR-7 | ส่งอนุมัติซ้ำจากการกดรัว/เน็ตช้า | **idempotency key required** ที่ `POST /purchase-requisitions/:id/submit` | `02_API` API-05 `[AI-DEFAULT]` |
| PR-9 | แก้ใบพร้อมกัน 2 หน้าต่าง | **version check → 409 `PR_VERSION_CONFLICT`** | `02_API` API-03 `[AI-DEFAULT]` |

> `[AI-DEFAULT]` = เลนนี้ตัดสินแทนเพราะ BRD ไม่ได้ระบุ — **ต้องให้ BA ยืนยันตอน review** ไม่ใช่ข้อสรุปสุดท้าย
