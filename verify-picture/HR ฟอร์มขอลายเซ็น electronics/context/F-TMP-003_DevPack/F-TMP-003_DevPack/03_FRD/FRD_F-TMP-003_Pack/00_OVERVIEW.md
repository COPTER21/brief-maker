# 00_OVERVIEW — F-TMP-003 คำขอมีและใช้ลายเซ็นดิจิทัล (DSR)

> frd-generator-v6 · Input Mode 0 (PREBRIEF v2 + FORM_SPEC + DECISIONS.lock) · Standard profile
> **โหมดไม่เฝ้า** — มติทุกข้อเป็น `[AI-DEFAULT]` รอลูกค้ายืนยันในใบลงนามก่อน UAT

| | |
|---|---|
| Feature | F-TMP-003 (รหัสชั่วคราว) |
| REQ | REQ-TMP-003 (รหัสชั่วคราว) |
| Module / Area | HR |
| doc_type | `DSR` (F-DOCCFG) |
| แบบพิมพ์ | FM-HRM-23 · Rev. 00 : 01/07/2569 (โหมด Replica) |
| archetype | Q-form (ใบขอ · ไม่มีรายการสินค้า · ไม่มีเอกสารต้นทาง) |
| BRD | `BRD_F-TMP-003.md` (APPROVED) |

## 1. ขอบเขตของ FRD ฉบับนี้
ครอบคลุมหน้าจอ ทะเบียน / สร้าง-แก้ร่าง / ดูรายละเอียด + แบบพิมพ์ PDF + สายอนุมัติ 1 ขั้น (dynamic)
**ไม่ครอบคลุม:** การออก/เพิกถอนใบรับรอง CA กับผู้ให้บริการภายนอก · การแก้ชื่อ-นามสกุลในทะเบียนพนักงาน (เป็นของ F-EMP-001) · การแจ้งเตือนวันหมดอายุใบรับรอง (ดู BRD §3.2)

## 2. ไฟล์ในชุด
| ไฟล์ | เนื้อหา |
|---|---|
| `00_OVERVIEW.md` | ภาพรวม · ของที่ต้องมีก่อนเริ่ม |
| `01_UI.md` | หน้าจอ · ช่อง · สถานะปุ่ม |
| `02_API.md` | endpoint + payload |
| `03_LOGIC.md` | FN-01…FN-12 (state machine · กฎตามกรณี · hook ของ engine) |
| `04_DB.md` | ตาราง · คอลัมน์ · index |
| `05_RULES.md` | business rule · validation · การอนุมัติ (DOA) |
| `06_TESTS.md` | เคสทดสอบ รวมเคสปฏิเสธสิทธิ์ |
| `07_LOCKED_DECISIONS.md` | มติที่ล็อกไว้ (DEC-01…DEC-17) |

## 3. ของที่ต้องมีก่อนเริ่มพัฒนา
| # | ของ | สถานะ |
|---|---|---|
| 1 | doc_type `DSR` ถูกสร้างและเปิดใช้ที่ **F-DOCCFG** | ยังไม่ทำ — ดู `DOCCFG_BRIEF_F-TMP-003.md` |
| 2 | DOA entry `DOA-DSR-01` ตั้งที่ DOA กลาง (F-DLG-001) | ยังไม่ทำ — ดู `DOA_BRIEF_F-TMP-003.md` · `wire_status: pending` |
| 3 | แบบเอกสารขึ้นทะเบียนที่ F185 | ยังไม่ทำ — ดู `MDOC_BRIEF_DSR.md` |
| 4 | event `dsr_cancelled` · `dsr_name_change_requested` ขึ้นที่ ENG-NOTIFY | ยังไม่ทำ — ดู `NTF_BRIEF_F-TMP-003.md` |
| 5 | role ของ "เจ้าหน้าที่ผู้ดูแลลายเซ็นดิจิทัล" ยืนยันกับ DOA กลาง (ตอนนี้ใช้ `role-mgr-hr` แทน) | **ค้าง** — BRD §15 OQ-01 |
| 6 | ทะเบียนพนักงานต้องมีชื่อ-นามสกุลภาษาอังกฤษครบ (ใช้ออกใบรับรอง CA) | **ค้าง** — BRD §15 OQ-02 |

## 4. ต้นแบบหน้าจอ
`feature.html` (html-generator-v9.3 · archetype Q-form · audit FAIL 0)
แบบพิมพ์: `print/form.tpl.html` + `print/print_config.json` + `print/DSR_data-contract.md` (thai-doc-pdf-generator v2.1 โหมด Replica)
