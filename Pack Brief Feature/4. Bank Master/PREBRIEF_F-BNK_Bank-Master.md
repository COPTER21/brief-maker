# PREBRIEF · Bank Master — บัญชีธนาคาร
> Sales lane · F-0.21 · Finance Foundation · **gen ใหม่ 2026-08-09 (ไม่มี base/FRD เดิม)** — skeleton จาก f-paymethod (สืบมติ r2 ทั้งชุด) · review logic + fix ผ่าน
> Reverse Mode: HTML คือของจริง · [AI-DRAFT] รอเคาะ
> **บทบาท**: ทะเบียนบัญชีธนาคารที่บริษัทถือ (เงินฝากจริง รายบัญชี) — ใช้ร่วมฝั่งรับ (Receipt) และจ่าย (PV) · ปิด chain Finance Foundation: COA → Posting Group → **Bank Master** → Payment Method

## 0. Obligations — พันธะจากต้นทาง
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | Pattern เลน (VD-PDM): สถานะ 3 ค่าอิสระ + statusMenu + stat 4 ใบ + bulk (used>0 ข้าม) + ไม่มีลบเดี่ยว + import 3 จังหวะ merge-only + export roundtrip + DOA null | มติเลน | §2, §6 |
| OB-2 | v8 + มติ r2 (สืบจาก PM): **ไม่มี used บนจอ** (guard ใน logic) · view = summary chips 4 ใบ + sections · icon generic · #29 `_keepScroll` · #96/#97 · Esc chain | มติ r2 | §6 |
| OB-3 | **Soft-ref → GL Posting Group (0.19 kind=bank)**: บัญชี GL เงินฝาก resolve ผ่านกลุ่ม — **ไม่เก็บเลข COA ตรง** (มาตรฐาน BC Bank Posting Group) · mock 2 กลุ่ม (KBANK/SCB) · จริง `GET /gl/posting-groups?type=bank&status=active` — mock cross-file: SCB ใน 0.19 ยังเป็นร่าง (note ในโค้ดแล้ว) | 0.19 + BC | §3, §7, OQ-BNK-02 |
| OB-4 | เอกสารผู้เรียก (Receipt/PV) ยังไม่ทำ — edge ประกาศรอ: เลือกบัญชีเฉพาะ "ใช้งาน" + ฝั่งตรง · ★ pre-select · snapshot ตอนบันทึก | มติ gen | §9, OQ-BNK-04 |
| OB-5 | THB เท่านั้น (LD THB-only ของเลน) — สกุลเงินแสดง disabled · multi-currency นอก scope | LD เลน | §3 |
| OB-6 | DOA: ไม่มีสายอนุมัติ — placeholder 4 fields = null · NOTIF ไม่ emit | Ledger | §3 |
| OB-7 | **มติ review (2026-08-09)**: fix นำเข้าเช็คซ้ำกันเองในไฟล์ (IN_FILE_DUPLICATE — รหัส+เลขบัญชี) เพิ่มจาก validate ปกติ | review | S-08 |

## 1. สรุป + ผู้ใช้
ทะเบียนบัญชีธนาคารบริษัท (รายบัญชีจริง: ธนาคาร×สาขา×เลขบัญชี) · ผู้ตั้งค่า: ฝ่ายบัญชี/Finance · ผู้ใช้ทางอ้อม: ผู้บันทึก Receipt/PV
**ธนาคาร 9 ค่า**: กสิกรไทย · ไทยพาณิชย์ · กรุงเทพ · กรุงไทย · ทีเอ็มบีธนชาต · กรุงศรีฯ · ออมสิน · ยูโอบี · อื่น ๆ

## 2. Scenarios
| S | ประเภท | ชื่อ | เกิดอะไร | ข้อมูลที่ต้องมี | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | เพิ่มบัญชีธนาคาร | ฟอร์ม 3 sections: ข้อมูลบัญชี (code auto ตามธนาคารถ้าเว้น เช่น KBANK-03) → GL (เลือกกลุ่ม Bank Posting Group + THB disabled) → การใช้งาน (ฝั่ง + ★ + สถานะ) | ธนาคาร\* เลขบัญชี\* (10–12 หลัก ใส่ขีดได้ · unique ทั้งทะเบียน) ชื่อบัญชี\* ฝั่ง ≥1\* | Receipt/PV เลือกได้ (ใช้งาน+ฝั่งตรง) |
| S-02 | Happy | ผูกกลุ่มบัญชี GL | เลือกจากกลุ่ม kind=bank ของ 0.19 (สถานะใช้งาน) — ไม่ผูก = บันทึกได้แต่ view เตือน "GL post ไม่ได้จนกว่าจะผูกกลุ่ม" | — | GL resolve บัญชีเงินฝากผ่านกลุ่ม |
| S-03 | Happy | ตั้ง ★บัญชีรับหลัก/จ่ายหลัก | 1 บัญชีต่อฝั่งทั้งระบบ (ตัวเดียวเป็นทั้งคู่ได้) · ตั้งใหม่ตัวเก่าหลุด (radio) · DEFAULT_GUARD: ต้อง active + ฝั่งเปิด · **สถานะหลุดจาก active → ★ หลุดตาม** | — | เอกสาร pre-select ให้ · "ฝั่ง = สิทธิ์ใช้ · ★ = ตัว default" |
| S-04 | Alt | แก้บัญชีที่มีเอกสารผ่านแล้ว | **IR-BNK-01 [AI-DRAFT]**: used>0 → ล็อก **ธนาคาร + เลขที่บัญชี** (UI disabled + lock-tag + logic guard — เปลี่ยนเลข = เปิดบัญชีใหม่แทน) · แก้ได้: ชื่อบัญชี/สาขา/ประเภท/พร้อมเพย์/กลุ่ม GL/ฝั่ง/★/สถานะ | — | เอกสารเก่า (snapshot) ไม่หลุด |
| S-05 | Exception | ข้อมูลผิด | เลขบัญชีนอก 10–12 หลัก (ACCT_INVALID) · เลขซ้ำทะเบียน (ACCT_DUPLICATE — เทียบแบบตัดขีด) · code ซ้ำ · ชื่อบัญชีว่าง · พร้อมเพย์ไม่ใช่ 10/13 หลัก · ไม่เลือกฝั่ง | — | บล็อกชี้ช่อง + toast |
| S-06 | Alt | เปลี่ยนสถานะอิสระ (เมนู view / bulk 3 ค่า) | ทุกทิศ ไม่มีอนุมัติ · side effect: หลุด active → ★ หลุด | — | ไม่ใช้งาน (เช่นปิดบัญชี) → เอกสารใหม่เลือกไม่ได้ |
| S-07 | Exception | bulk ลบ | confirm บอกยอดข้าม — used>0 (มีเอกสารผ่านบัญชี) ไม่ลบ | เลือก ≥1 | — |
| S-08 | Happy | นำเข้า CSV (merge-only) | 3 จังหวะ · validate: REQUIRED / BAD_BANK / ACCT_INVALID / **ACCT_DUPLICATE** / BAD_TYPE / BAD_USE / BAD_STATUS / CODE_DUPLICATE / **IN_FILE_DUPLICATE (รหัส+เลขบัญชีซ้ำกันเองในไฟล์ — fix review)** · ธนาคาร/ประเภท/ฝั่ง/สถานะภาษาไทย (ว่าง=ออมทรัพย์/ทั้งสอง/ร่าง) · ไม่มี posting_group ในไฟล์ (ผูกทีหลังในจอ) | code,bank,branch,account_no,account_name,account_type,use_in,status | ทะเบียนเดิมไม่ถูกแตะ |
| S-09 | Happy | ส่งออก CSV | ตาม filter · คอลัมน์เดียวกับ template (roundtrip — ไม่มี promptpay/posting_group ตาม template) · BOM · `bank_export_YYYY-MM-DD.csv` | — | — |
| S-10 | **ไม่รองรับ** (ตัดสินแล้ว) | ① ยอดคงเหลือ/opening balance (เรื่อง GL/Reconciliation ไม่ใช่ master) ② multi-currency (THB-only OB-5) ③ SWIFT/IBAN ④ ผู้มีอำนาจเซ็น/วงเงิน (เรื่อง DOA/Policy) ⑤ used บนจอ (มติ r2) ⑥ โหมดนำเข้า Replace ⑦ ลบเดี่ยว ⑧ ★ หลายตัวต่อฝั่ง ⑨ posting_group/promptpay ในไฟล์นำเข้า | | | |

## 3. Data — full data dict
| Field | บังคับ | กติกา | ล็อกเมื่อ |
|---|---|---|---|
| code | auto ได้ | unique · เว้นว่าง = `{ธนาคาร}-{เลขรัน}` · uppercase | แก้ได้ |
| ธนาคาร (9 ค่า) | ✅ | — | 🔒 used>0 (IR-BNK-01) |
| เลขที่บัญชี | ✅ | 10–12 หลัก (ขีดได้) · unique ทั้งทะเบียน (เทียบตัดขีด) | 🔒 used>0 |
| ชื่อบัญชี | ✅ | — | แก้ได้ |
| สาขา / ประเภทบัญชี (ออมทรัพย์/กระแสรายวัน/ฝากประจำ) | — | — | แก้ได้ |
| พร้อมเพย์ผูกบัญชี | — | ว่าง หรือ 10 หลัก (เบอร์) / 13 หลัก (เลขภาษี) | แก้ได้ |
| กลุ่มบัญชี GL (posting_group) | — (แต่ GL post ไม่ได้ถ้าไม่ผูก) | soft-ref → 0.19 kind=bank สถานะใช้งาน | แก้ได้ |
| สกุลเงิน | — | THB คงที่ (disabled) | — |
| use_receive / use_pay | ≥1 ✅ | สิทธิ์ใช้ต่อฝั่ง | แก้ได้ |
| default_receive / default_pay (★) | — | 1 ตัวต่อฝั่งทั้งระบบ · ต้อง active+ฝั่งเปิด · หลุดตามสถานะ | แก้ได้ |
| สถานะ (3 ค่า) | — | อิสระทุกทิศ | — |
| ระบบ | | `used` (count เอกสารผ่านบัญชี — logic เท่านั้น ไม่โชว์) · created/updated · DOA null 4 fields | |

## 4. Business Rules
| BR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01 | เลขบัญชี 10–12 หลัก unique ทั้งทะเบียน (เทียบตัดขีด) — validate ฟอร์ม + ไฟล์ (รวมซ้ำกันเองในไฟล์) | S-05, S-08 | มาตรฐาน + fix review |
| BR-02 | **IR-BNK-01 [AI-DRAFT]**: used>0 ล็อกธนาคาร+เลขบัญชี — แก้ได้ที่เหลือ · ลบไม่ได้ (bulk ข้าม) | S-04, S-07 | OQ-BNK-03 |
| BR-03 | ฝั่ง ≥1 · ★ 1 ตัว/ฝั่ง radio · DEFAULT_GUARD (active+ฝั่งเปิด) · หลุด active → ★ หลุดตาม | S-03, S-06 | pattern PM |
| BR-04 | บัญชี GL resolve ผ่าน Bank Posting Group เท่านั้น — master นี้ไม่เก็บเลข COA · ไม่ผูกกลุ่ม = GL post ไม่ได้ (view เตือน) | S-02 | OB-3 (BC standard) |
| BR-05 | เอกสารเลือกได้เฉพาะ "ใช้งาน" + ฝั่งตรง · ★ pre-select · snapshot ตอนบันทึก | S-01 | OB-4 |
| BR-06 | พร้อมเพย์: ว่าง / 10 / 13 หลักเท่านั้น | S-05 | มาตรฐานไทย |
| BR-07 | นำเข้า merge-only · ค่าไทยในไฟล์ · ว่าง=ออมทรัพย์/ทั้งสอง/ร่าง | S-08 | มติเลน |

## 5. State Machine — 3 สถานะอิสระทุกทิศ + side effect: หลุดจาก active → ★ ทั้ง 2 ฝั่งหลุดตาม (เมนู view / bulk / ฟอร์ม / ไฟล์นำเข้า)

## 6. Actions ต่อหน้า
| หน้า | Action |
|---|---|
| List | stat 4 ใบกดกรอง · ค้นหา (รหัส/ธนาคาร/สาขา/เลขบัญชี) + filter ธนาคาร + สถานะ · sort · pager (8/หน้า) · bulk (3 สถานะ + ลบ) · ส่งออก/นำเข้า · เพิ่ม · แถว: ★รับ/★จ่าย + กลุ่ม GL + แก้ไข · #96 sticky thead · #29 |
| Drawer form | 3 sections: ข้อมูลบัญชี → GL (กลุ่ม + THB disabled) → การใช้งาน · IR lock (disabled + lock-tag เมื่อ used>0) · validate ครบ + DEFAULT_GUARD toast |
| Drawer view | header: ชื่อธนาคาร + เลขบัญชี mask (xxx-x-xx…) · summary chips 4 ใบ (ธนาคาร/เลขบัญชี/ฝั่ง/กลุ่ม GL) · 3 sections: ข้อมูลบัญชี → บัญชีแยกประเภท GL (เตือนถ้ายังไม่ผูก) → การใช้งานในเอกสาร (ฝั่ง+★) · tab ภาพรวม/ประวัติ · เมนูเปลี่ยนสถานะ · Esc chain |
| Modal | นำเข้า 3 จังหวะ · confirm ลบ bulk (บอกยอดข้าม) |

## 7. Data behaviour
soft-ref สองชั้น + snapshot: ① เอกสาร (Receipt/PV) เก็บ code บัญชี + สำเนาค่าตอนบันทึก ② บัญชีเก็บ code กลุ่ม → กลุ่มเก็บเลขบัญชี COA (0.19) — GL resolve สดตอน post · BANK_POSTING_GROUPS mock 2 ค่า → sync จริง filter active (OQ-BNK-02 — mock cross-file: SCB ใน 0.19 ยังร่าง note ในโค้ด) · `used` mock → count จริง

## 8. Mock Data Spec
8 บัญชีครอบ 6 ธนาคาร × 3 สถานะ: KBANK-01 (★รับ · used 620 · ผูก KBANK · พร้อมเพย์เลขภาษี) · SCB-01 (★จ่าย · used 340 · current) · BBL-01 · KTB-01 (used 0 — ลบได้) · KBANK-02 (สำรอง) · BAY-01 (พร้อมเพย์เบอร์) · TTB-01 (ร่าง) · GSB-01 (ไม่ใช้งาน — ปิดบัญชีแล้ว used 15) · BULK_SAMPLE 6 แถว: ผ่าน 3 + KBANK-01 ซ้ำทะเบียน + BAD-01 (BAD_BANK) + UOB-01 ซ้ำในไฟล์ (IN_FILE_DUPLICATE)

## 9. Edges + ผลปลายทาง
| ทิศ | คู่ | ผ่านอะไร |
|---|---|---|
| เข้า | ← **GL Posting Group (0.19 kind=bank)** | dropdown กลุ่มบัญชี GL — `GET /gl/posting-groups?type=bank&status=active` (OQ-BNK-02) |
| ออก | → **Payment Method (0.20)** | รอเคาะ OQ-BNK-01: PM เปลี่ยน default_acct จาก COA ตรง → เลือกบัญชีจากทะเบียนนี้ (ปิด OQ-PM-02 · เงินสดยกเว้นใช้ COA เงินสดในมือ) |
| ออก | → **Receipt / PV** (ยังไม่ทำ) | เลือกบัญชี (ใช้งาน+ฝั่งตรง) · ★ pre-select · snapshot |
| ออก | → **GL engine** | post เงินเข้า/ออกบัญชีเงินฝากผ่านกลุ่ม 0.19 |
| ออก | → Bank Reconciliation (อนาคต) | เลขบัญชี unique + ธนาคาร match statement |
| — | DOA / NOTIF | ไม่มี (OB-6) |

## 10. OQ + [AI-DRAFT] register
| # | ประเด็น | เจ้าภาพ | สถานะ |
|---|---|---|---|
| OQ-BNK-01 | PM (0.20) ควรชี้บัญชีจากทะเบียนนี้แทน COA ตรง — ปิด OQ-PM-02 · เคาะแล้วแก้ PM 1 field | Strike | pin |
| OQ-BNK-02 | Bank Posting Groups mock 2 ค่า → sync จริง filter active · **บังคับผูกกลุ่มก่อนเปิดใช้มั้ย?** (ตอนนี้บันทึกได้แต่เตือน) · mock cross-file SCB=ร่างใน 0.19 | Strike | pin |
| OQ-BNK-03 | IR-BNK-01 [AI-DRAFT]: used>0 ล็อกธนาคาร+เลขบัญชี + used จริง = count เอกสารผ่านบัญชี | Strike | pin |
| OQ-BNK-04 | Receipt/PV ยังไม่ทำ — ยืนยัน flow เลือกบัญชี + snapshot + ★ pre-select | Strike | pin |
| OQ-BNK-05 | ยังไม่มี FRD (feature gen ใหม่) — gen ครั้งแรกหลัง OQ-BNK-01/02 เคาะ | BA | เปิด |

## 11. Coverage Matrix
| S | BR | transition | UI | FN |
|---|---|---|---|---|
| S-01, S-02 | BR-01,04,05 | สร้าง→3 ค่า | form 3 sections + auto code + GL เตือน | FN-01..FN-06 |
| S-03 | BR-03 | ★ radio + guard | ★ badge + DEFAULT_GUARD | FN-07..FN-09 |
| S-04 | BR-02 | amend | IR lock (disabled+tag+logic) | FN-10, FN-11 |
| S-05 | BR-01,06 | — | validate | FN-12, FN-13 |
| S-06 | BR-03 | ทุกทิศ + side effect | เมนู view + bulk | FN-14..FN-16 |
| S-07 | BR-02 | ลบ | bulk + confirm ข้าม | FN-17 |
| S-08 | BR-01,07 | นำเข้า | modal 3 จังหวะ + IN_FILE_DUPLICATE | FN-18..FN-21 |
| S-09 | — | — | export | FN-22 |
| S-10 | — | — | (ตรวจว่าไม่มี) | FN-40 |
ผ่าน: BR ครบ ✓ · state+side effect ครบ ✓ · S↔UI↔FN ครบ ✓ · OB-1..7 อ้างครบ ✓ · fix review สะท้อนใน S-08/BR-01 ✓
