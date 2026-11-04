# 00_OVERVIEW — F-TMP-001 แบบฟอร์มขอใช้รถตู้ (VAN)

> frd-generator-v6 · Input Mode 0 (PREBRIEF v2 + FORM_SPEC + DECISIONS.lock) · Standard profile
> **โหมดไม่เฝ้า** — มติทุกข้อเป็น `[AI-DEFAULT]` รอลูกค้ายืนยันในใบลงนามก่อน UAT

| | |
|---|---|
| Feature | F-TMP-001 (รหัสชั่วคราว) |
| REQ | REQ-TMP-001 (รหัสชั่วคราว) |
| Module / Area | HR |
| doc_type | `VAN` (F-DOCCFG) |
| แบบพิมพ์ | FM-HRM-22 · Rev. 00 : 01/07/2569 (โหมด Replica) |
| archetype | Q-form (ใบขอ · ไม่มีรายการสินค้า · ไม่มีเอกสารต้นทาง) |
| BRD | `BRD_F-TMP-001.md` (APPROVED 28/28) |

## 1. ขอบเขตของ FRD ฉบับนี้
ครอบคลุมหน้าจอ ทะเบียน / สร้าง-แก้ร่าง / ดูรายละเอียด + แบบพิมพ์ PDF + สายอนุมัติ 2 ขั้น (dynamic)
**ไม่ครอบคลุม:** ตารางการใช้รถ · มอบหมายคนขับ · เชื่อมเวลาทำงาน/เบิกจ่าย (ดู BRD §3.2)

## 2. ไฟล์ในชุด
| ไฟล์ | เนื้อหา |
|---|---|
| `00_OVERVIEW.md` | ภาพรวม · ของที่ต้องมีก่อนเริ่ม |
| `01_UI.md` | หน้าจอ · ช่อง · สถานะปุ่ม |
| `02_API.md` | endpoint + payload |
| `03_LOGIC.md` | FN-01…FN-12 (state machine · การคำนวณ · hook ของ engine) |
| `04_DB.md` | ตาราง · คอลัมน์ · index |
| `05_RULES.md` | business rule · validation · การอนุมัติ (DOA) |
| `06_TESTS.md` | เคสทดสอบ รวมเคสปฏิเสธสิทธิ์ |
| `07_LOCKED_DECISIONS.md` | มติที่ล็อกไว้ (DEC-01…DEC-14) |

## 3. ของที่ต้องมีก่อนเริ่มพัฒนา
| # | ของ | สถานะ |
|---|---|---|
| 1 | doc_type `VAN` ถูกสร้างและเปิดใช้ที่ **F-DOCCFG** | ยังไม่ทำ — ดู `DOCCFG_BRIEF_F-TMP-001.md` |
| 2 | DOA entry `DOA-VAN-01` ตั้งที่ DOA กลาง (F-DLG-001) | ยังไม่ทำ — ดู `DOA_BRIEF_F-TMP-001.md` · `wire_status: pending` |
| 3 | แบบเอกสารขึ้นทะเบียนที่ F185 | ยังไม่ทำ — ดู `MDOC_BRIEF_VAN.md` |
| 4 | event `van_cancelled` ขึ้นที่ ENG-NOTIFY | ยังไม่ทำ — ดู `NTF_BRIEF_F-TMP-001.md` |
| 5 | `role-line-manager` ยืนยันกับ DOA กลาง | **ค้าง** — BRD §15 OQ-01 |

## 4. ต้นแบบหน้าจอ
`feature.html` (html-generator-v9 · archetype Q-form · audit FAIL 0)
แบบพิมพ์: `print/form.tpl.html` + `print/print_config.json` + `print/VAN_data-contract.md` (thai-doc-pdf-generator v2.1 โหมด Replica)
