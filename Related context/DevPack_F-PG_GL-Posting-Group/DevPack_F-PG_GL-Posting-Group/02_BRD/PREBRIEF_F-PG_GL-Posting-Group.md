# PREBRIEF · GL Posting Group — กลุ่มการบันทึกบัญชีแยกประเภท
> Sales lane · F-0.19 · Finance Foundation · จาก HTML as-built (recheck + CI rebrand v8 — 2026-08-09) + FRD pack เดิม (v5.1 — **stale**)
> Reverse Mode: HTML คือของจริง · [AI-DRAFT] รอเคาะ · รหัสเดิม: F-GL-POSTING-001
> **บทบาท**: "สมุดแปลเอกสารธุรกิจ → เลขบัญชี" — mapping layer ตั้งครั้งเดียว เอกสารทุกใบไม่ต้องเลือกบัญชีเอง · **ไม่ post เอง** (GL engine เป็นผู้ post)

## 0. Obligations — พันธะจากต้นทาง
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | **Rules สืบทอดจาก pack (FIXED ห้ามฝืน)**: R01 บัญชีที่เลือก = COA leaf (postable) เท่านั้น · R02 ตรงประเภท COA (AP=หนี้สิน · AR/สินค้า/ธนาคาร/ภาษีซื้อ=สินทรัพย์ · ภาษีขาย=หนี้สิน · sales=รายได้ · COGS/purchase=ค่าใช้จ่าย) · R03 code unique · R04 combination (bus×prod) unique · **R05 kind ล็อกหลังสร้าง** · R06 soft-delete only · R07 เปลี่ยน kind ก่อนบันทึก → ล้าง account fields | FRD 05_RULES | §2, §4 |
| OB-2 | **Contract จาก Item Master (VD-PDM-15)**: Item เก็บ soft-ref `กลุ่มบัญชีสินค้า` (6 ค่า: FINISHED/RAWMAT/PACKAGING/SERVICE/TRADE/EXPENSE) + `กลุ่มภาษี` (VAT7/VAT0/NONVAT) — **feature นี้ต้อง serve**: `GET /gl/posting-groups?type=product` + `GET /gl/vat-groups` · as-built แกน prod ของ matrix ยังเป็น GOODS/SERVICE (คนละชุด) → **OQ-PG-04 รอเคาะก่อนแก้** | PREBRIEF F-PDM OB-2 | §9, §10 |
| OB-3 | **Contract จาก Tax Code (OB-2 ของ 0.16)**: "GL Posting Setup map รหัสภาษี → บัญชี GL" — as-built ยังไม่มี (VAT acct ผูกที่ vendor/customer group = ทุก tax code ลงบัญชีเดียว) → **OQ-PG-01** เสนอ tab 3 "VAT Posting Setup" (มาตรฐาน BC) — ไม่เพิ่มเองก่อนเคาะ | Registry §5 | §9, §10 |
| OB-4 | Upstream: **COA (F-COA-001)** ป้อน dropdown บัญชีทุกช่อง — as-built hardcode 16 บัญชี (mock) · จริง sync เฉพาะ leaf + postable + **สถานะใช้งาน** (BR-07 ของ COA) + filter ประเภทตาม R02 | pack §0.4 + COA prebrief | §3, §7 |
| OB-5 | DOA: ไม่มีสายอนุมัติ — placeholder 4 fields = null · NOTIF ไม่ emit | Ledger | §3.3 |
| OB-6 | Pattern เลน (VD-PDM): สถานะ 3 ค่าอิสระ **ทั้ง 2 tab** · bulk ต่อ tab · ไม่มีลบเดี่ยว · ตัด hint/field-help · import + export CSV **per-tab** component มาตรฐานเลน (upload-box → preview → done · merge-only) | มติเลน | §2, §6 |
| OB-7 | v8 + CI Warm Light (rebrand จาก Navy v3.9): #96 full-height + sticky thead · #97 responsive 768 · #29 scroll preservation · Esc chain | มติ v8 | §6 |
| OB-8 | **IR-PG-01** [AI-DRAFT พี่น้อง IR-TAX/IR-COA]: `used>0` (มี journal post ผ่าน mapping แล้ว) → ล็อก **รหัสกลุ่ม** (tab 1) / **combination bus×prod** (tab 2) — แก้ได้ ชื่อ/บัญชี/สถานะ · kind ล็อกหลังสร้างเสมอ (R05 — ไม่ต้องรอ used) | มติ 2026-08-09 | §2 S-04, BR-05 |

## 1. สรุป + ผู้ใช้ + โครง 2 tab
| Tab | ทำอะไร | 1 แถว = |
|---|---|---|
| **1 · Specific Posting Groups** | จับ entity → บัญชี control: **เจ้าหนี้** (AP + ภาษีซื้อ) · **สินค้าคงคลัง** (Inventory + Interim GR/IR) · **ธนาคาร** (เงินฝาก) · **ลูกหนี้** (AR + ภาษีขาย) | 1 กลุ่ม (code + kind + ชุดบัญชีตาม kind) |
| **2 · General Posting Setup** | เมทริกซ์ กลุ่มธุรกิจ × กลุ่มสินค้า → บัญชีรายได้ (Sales) / บัญชีซื้อ (Purchase) / ต้นทุน (COGS) | 1 combination |
ผู้ใช้: ฝ่ายบัญชี/Finance Lead ตั้งค่า · เอกสารซื้อ-ขายทุก module ใช้ทางอ้อมผ่าน GL engine

## 2. Scenarios (derive: D1→S-05 · D2→S-06 · D3→S-04 · D4→OB-4 (COA upstream — dropdown เฉพาะใช้งาน) · D5→§9 (GL resolve เฉพาะใช้งาน) · D6[STD]→S-07..S-09)
| S | ประเภท | ชื่อ | เกิดอะไร | ข้อมูลที่ต้องมี | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | สร้าง Posting Group (tab 1) | เลือกประเภท 4 kind → ชุดช่องบัญชีเปลี่ยนตาม (R07: เปลี่ยน kind ก่อนบันทึก → ล้างช่องบัญชี) · บัญชีเลือกจาก dropdown COA (filter ประเภทตาม R02) | code\* ชื่อ\* บัญชีหลักตาม kind\* | Vendor/Customer/Item/Bank master เลือกกลุ่มนี้ได้ (เฉพาะใช้งาน) |
| S-02 | Happy | สร้าง Setup (tab 2) | เลือก กลุ่มธุรกิจ × กลุ่มสินค้า + บัญชี 3 ช่อง (sales/purchase/COGS) | ครบ 5 ช่อง\* · combination ไม่ซ้ำ (R04) | GL post ขาย-ซื้อของ combination นี้ลงบัญชีชุดนี้ |
| S-03 | Alt | แก้ไข | แก้ชื่อ/บัญชี/สถานะได้เสมอ · **kind แก้ไม่ได้หลังสร้าง (R05)** | — | เอกสารใหม่ใช้บัญชีชุดใหม่ทันที (posting เก่าไม่ย้อน) |
| S-04 | Alt | แก้ตัวที่มี posting แล้ว | **IR-PG-01**: `used>0` → รหัสกลุ่ม/combination ล็อก (ฝืน → block + toast) · บัญชียังแก้ได้ (เจตนา: เปลี่ยนบัญชีปลายทางไปข้างหน้า) | — | soft-ref ที่ entity/เอกสารเก่าไม่หลุด |
| S-05 | Exception | ข้อมูลผิด | code ว่าง/ซ้ำ (R03) · ชื่อว่าง · บัญชีหลักว่าง · combination ซ้ำ (R04) | — | บล็อกชี้ช่อง + toast |
| S-06 | Alt | เปลี่ยนสถานะอิสระ (เมนู view / bulk 3 ค่า — ทั้ง 2 tab) | ทุกทิศ ไม่มีอนุมัติ | — | ไม่ "ใช้งาน" → entity ใหม่เลือกไม่ได้ / GL resolve ไม่เจอ (เอกสารใหม่ของ combination นั้น error ที่ GL — ตั้งใจ) |
| S-07 | Exception | bulk ลบ | confirm บอกยอดข้าม — `used>0` ไม่ลบ (R06 soft-delete → ใช้เปลี่ยนสถานะแทน) | เลือก ≥1 | — |
| S-08 | Happy | นำเข้า CSV per-tab (**merge-only เพิ่มอย่างเดียว**) | จอแรก: upload-box + ปุ่ม template ต่อ tab เท่านั้น · per-row validate: REQUIRED / BAD_KIND / CODE_DUPLICATE (ทะเบียน+ในไฟล์) / combination ซ้ำ (R04) / **บัญชีต้องมีใน COA (R01)** / BAD_STATUS · status ไทย ว่าง=ร่าง | tab 1: code,kind,name_th,name_en,account_1,account_2,status · tab 2: bus,prod,sales_acct,purchase_acct,cogs_acct,status | ทะเบียนเดิมไม่ถูกแตะ |
| S-09 | Happy | ส่งออก CSV per-tab | ตาม filter · คอลัมน์เดียวกับ template (roundtrip) · สถานะไทย · BOM | — | `postgrp_groups_export_…` / `postgrp_setup_export_…` |
| S-10 | **ไม่รองรับ** (ตัดสินแล้ว) | ① โหมดนำเข้า Replace/merge-overwrite (ตัดออก — ตอบ R08 CONFIGURABLE: ไม่มีทางล้าง/ทับ mapping ขณะระบบเดินอยู่) ② เปลี่ยน kind หลังสร้าง (R05) ③ ลบเดี่ยว / ลบตัวมี posting ④ **VAT Posting Setup ต่อรหัสภาษี — ยังไม่ทำ รอ OQ-PG-01** ⑤ UI จัดการค่ากลุ่มธุรกิจ/กลุ่มสินค้า (R09 DYNAMIC — รอ OQ-PG-04) ⑥ post บัญชีจริง (GL engine ทำ — นอก scope) ⑦ สายอนุมัติ | | | |

## 3. Data — full data dict
### 3.1 Tab 1 · Specific Posting Group
| Field | บังคับ | กติกา | ล็อกเมื่อ |
|---|---|---|---|
| code | ✅ | unique (R03) · uppercase ตอนนำเข้า | 🔒 used>0 (IR-PG-01) |
| ประเภท (kind 4 ค่า: เจ้าหนี้/สินค้าคงคลัง/ธนาคาร/ลูกหนี้) | ✅ | เปลี่ยนก่อนบันทึก → ล้างช่องบัญชี (R07) | 🔒 หลังสร้างเสมอ (R05) |
| ชื่อ (TH) / ชื่อ (EN) | TH ✅ | — | แก้ได้ |
| ชุดบัญชีตาม kind — เจ้าหนี้: AP\* + ภาษีซื้อ · สินค้า: Inventory\* + Interim · ธนาคาร: เงินฝาก\* · ลูกหนี้: AR\* + ภาษีขาย | หลัก ✅ | dropdown จาก COA — leaf+postable+ใช้งาน + ตรงประเภท (R01/R02) | แก้ได้ (เจตนา S-04) |
| สถานะ (3 ค่า) | — | อิสระ | แก้ได้ |
### 3.2 Tab 2 · General Posting Setup
| Field | บังคับ | กติกา |
|---|---|---|
| กลุ่มธุรกิจ (bus) × กลุ่มสินค้า (prod) | ✅ | combination unique (R04) · 🔒 used>0 · ค่ากลุ่ม as-built: DOMESTIC/FOREIGN × GOODS/SERVICE — **ชุด prod รอเคาะให้ตรง Item (OQ-PG-04)** |
| บัญชีรายได้ / บัญชีซื้อ / บัญชีต้นทุน | ✅ ทั้ง 3 | COA — รายได้/ค่าใช้จ่าย (R02) |
| สถานะ (3 ค่า) | — | อิสระ |
### 3.3 ระบบ: `used` (จำนวน journal ที่ post ผ่าน mapping — mock · จริง sync GL → OQ-PG-03) · created/updated · DOA placeholder 4 fields = null (OB-5)

## 4. Business Rules
| BR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01 | บัญชีทุกช่อง = COA leaf/postable/ใช้งาน + ตรงประเภท — validate ทั้งฟอร์มและไฟล์นำเข้า | S-01, S-08 | R01+R02 |
| BR-02 | code unique (tab 1) · combination bus×prod unique (tab 2) | S-05 | R03+R04 |
| BR-03 | kind ล็อกหลังสร้าง · เปลี่ยน kind ก่อนบันทึก → ล้างช่องบัญชี | S-01, S-03 | R05+R07 |
| BR-04 | ลบไม่ได้เมื่อ `used>0` — bulk ข้ามพร้อมแจ้ง (soft-delete → เปลี่ยนสถานะแทน) | S-07 | R06 |
| BR-05 | **IR-PG-01**: used>0 ล็อกรหัส/combination — แก้ได้ ชื่อ/บัญชี/สถานะ | S-04 | [AI-DRAFT] |
| BR-06 | สถานะ 3 ค่าอิสระ ทั้ง 2 tab · GL resolve + entity picker ใช้เฉพาะ "ใช้งาน" | S-06 | มติเลน |
| BR-07 | นำเข้า merge-only เพิ่มอย่างเดียว per-tab · status ว่าง=ร่าง | S-08 | มติ 2026-08-09 |
| BR-08 | feature นี้ไม่ post — GL engine resolve ตอนเอกสาร post: (คู่ค้า→specific group) + (bus×prod→setup) → journal lines ลง COA | — | §0.2 pack |

## 5. State Machine — 3 สถานะอิสระ (ร่าง ⇄ ใช้งาน ⇄ ไม่ใช้งาน ทุกทิศ) ทั้ง 2 tab — เมนู view / bulk / ฟอร์ม / ไฟล์นำเข้า

## 6. Actions ต่อหน้า
| หน้า | Action |
|---|---|
| หน้าเดียว 2 tab | tabbar สลับ (เคลียร์ selection + filter สถานะเมื่อสลับ) · ต่อ tab: stat 4 ใบกดกรอง · ค้นหา + filter (tab 1: ประเภทกลุ่ม sdd + สถานะ · tab 2: ค้น bus/prod + สถานะ) · checkbox + bulk (3 สถานะ + ลบ) · ส่งออก/นำเข้า CSV · เพิ่ม · แถว: แก้ไข · #96 sticky thead · **#29 scroll ไม่เด้ง** |
| Drawer form ×2 | tab 1: kind picker (ล็อกตอน edit) + ชุดบัญชีตาม kind (sdd ค้นบัญชี) · tab 2: bus/prod + บัญชี 3 ช่อง · สถานะ · validate ครบ |
| Drawer view ×2 | ชุดบัญชีที่ผูก + เมนูเปลี่ยนสถานะ 3 ค่า + แก้ไข · Esc chain |
| Modal | นำเข้า 3 จังหวะมาตรฐานเลน · confirm ลบ bulk (บอกยอดข้าม) |

## 7. Data behaviour
soft reference สองชั้น: ① entity (Vendor/Customer/Item/Bank) เก็บ **code กลุ่ม** ② กลุ่มเก็บ **รหัสบัญชี COA** — GL resolve สดตอน post (แก้บัญชีในกลุ่ม = เอกสารใหม่ใช้ทันที ของเก่าไม่ย้อน) · COA dropdown mock 16 บัญชี → จริง sync API (OQ-PG-02) · `used` mock → journal count (OQ-PG-03)

## 8. Mock Data Spec
Tab 1 — 7 กลุ่มครอบ 4 kind × 3 สถานะ: LOCAL (vendor · used 82 — prove ล็อก+guard) · FOREIGN · FINISHED · KBANK (used 203) · DOMESTIC-C · SCB (ร่าง) · SCRAP (ไม่ใช้งาน used 6) · Tab 2 — 3 ชุด: DOMESTIC×GOODS (used 340) · DOMESTIC×SERVICE · FOREIGN×GOODS (ร่าง) — **FOREIGN×SERVICE เว้นว่างให้ template นำเข้า** · template ต่อ tab: ผ่านบางแถว + ซ้ำทะเบียน + BAD_STATUS + บัญชีไม่มีใน COA

## 9. Edges + ผลปลายทาง
| ทิศ | คู่ | ผ่านอะไร |
|---|---|---|
| เข้า | ← **COA (F-COA-001)** | dropdown บัญชีทุกช่อง (leaf+postable+ใช้งาน · R01/R02) — OQ-PG-02 |
| เข้า | ← **Item Master (F-PDM)** | Item เลือก "กลุ่มบัญชีสินค้า"+"กลุ่มภาษี" ผ่าน `GET /gl/posting-groups?type=product` + `/gl/vat-groups` (contract ประกาศแล้ว — ชุดค่ารอ sync OQ-PG-04) |
| เข้า | ← Customer / Vendor / Bank master (อนาคต) | เลือก specific group + กลุ่มธุรกิจ — master ยังไม่ทำ (edge ประกาศ) |
| ออก | → **GL / Journal engine** | resolve บัญชีตอนเอกสาร post (AP/AR Inv, GRN, Payment) — feature นี้ไม่ post เอง (BR-08) |
| ออก | → Tax Code (0.16) | **gap**: mapping รหัสภาษี→บัญชี ยังไม่มี — OQ-PG-01 (เสนอ tab VAT Posting Setup) |
| — | DOA / NOTIF | ไม่มี (OB-5) |

## 10. OQ + [AI-DRAFT] register
| # | ประเด็น | เจ้าภาพ | สถานะ |
|---|---|---|---|
| OQ-PG-01 | **Tax mapping gap** (contract Tax OB-2 + Item vat_prod_group ชี้ตรงกัน 2 ทาง) — เลือก A: field ที่ Tax master / **B: tab 3 "VAT Posting Setup" (แนะนำ — มาตรฐาน BC)** / C: คงเดิม | Strike | pin |
| OQ-PG-02 | COA dropdown hardcode 16 บัญชี — จริง sync F-COA เฉพาะ leaf+postable+ใช้งาน + filter ประเภท R02 | FRD | pin |
| OQ-PG-03 | `used` mock — จริง = journal count ที่ post ผ่าน mapping · ยืนยัน IR-PG-01 [AI-DRAFT] | Strike | pin |
| OQ-PG-04 | **Group values ไม่ sync**: แกน prod ของ matrix (GOODS/SERVICE) ≠ ชุดที่ Item เลือก (6 ค่า FINISHED/RAWMAT/…) — เคาะ: ใช้ชุด Item เป็นหลัก + UI จัดการค่ากลุ่ม (R09 DYNAMIC) + business group ฝั่ง Customer/Vendor (master ยังไม่ทำ) | Strike | pin |
| OQ-PG-05 | FRD pack v5.1 **stale** — regen จาก HTML + เพิ่ม API contract 2 endpoint ของ Item | BA | เปิด |

## 11. Coverage Matrix
| S | BR | transition | UI | FN |
|---|---|---|---|---|
| S-01, S-02 | BR-01,02,03 | สร้าง→3 ค่า | form ×2 + kind picker | FN-01..FN-06 |
| S-03, S-04 | BR-03,05 | amend | kind lock + IR-PG-01 guard | FN-07..FN-09 |
| S-05 | BR-01,02 | — | validate | FN-10, FN-11 |
| S-06 | BR-06 | ทุกทิศ | เมนู view + bulk ×2 tab | FN-12..FN-14 |
| S-07 | BR-04 | ลบ | bulk + confirm ข้าม | FN-15 |
| S-08 | BR-01,07 | นำเข้า | modal 3 จังหวะ per-tab | FN-16..FN-19 |
| S-09 | — | — | export per-tab | FN-20 |
| S-10 | — | — | (ตรวจว่าไม่มี) | FN-40 |
ผ่าน: BR ครบ ✓ · state ครบ ✓ · S↔UI↔FN ครบ ✓ · OB-1..8 อ้างครบ ✓ · R01..R07 ไม่ถูกฝืน · R08 ตอบด้วยตัด Replace · R09 แขวน OQ-PG-04 ✓
