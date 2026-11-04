# DOCCFG_BRIEF — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ · v1.1 (5 ต.ค. 2569)
> Auto-register ลง **Document Configuration (F003 / F-DOCCFG — master กลางของแบบเอกสาร)** ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register (มติ 2026-08-11)
> เลขทุกใบจาก ENG-DOC-NUM เท่านั้น · สำเนาทุกใบจาก ENG-DOC-STORE เท่านั้น · การตั้งค่าพิมพ์/ลายเซ็น/เวอร์ชัน/เปิดใช้ อ่านจาก F-DOCCFG เท่านั้น — ห้าม hardcode
> ที่มา: FRD_F-HR-OSW_Pack (03_LOGIC FN-05/09/11/13 · 05_RULES BR-OSW-14/15/17/18) · `print/OSW_print-spec.md` · DOA_BRIEF v1.0
> v1.1: ปรับตามโครงใหม่ — F-DOCCFG เป็น master กลาง (เลขรัน + ตั้งค่าพิมพ์ + เวอร์ชัน/เปิดใช้ + ประกาศ) · F185 เหลือแค่คำขอเอกสารใหม่ · โลโก้/หัวกระดาษมาจาก Organization + snapshot ตอนออกเลข · ช่องลายเซ็นตาม config รายช่อง
> ⚠ ยังไม่ได้ Sync Read registry ปัจจุบันของ F-DOCCFG (ไม่มีไฟล์ `f-doccfg.html` ในแชทนี้) → เช็ค code ชนก่อน register (OQ-1)

## doc_type ที่ประกาศ
| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| OSW | แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ | HR | `{PREFIX}-{YYYY}-{run:4}` | รายปี | global | ✗ | ✗ | ✓ |

- **ชนกับ registry เดิม:** ไม่พบเอกสารความหมายซ้อนในชุดที่รู้ (ใบลา LV · ใบขอทำงานล่วงเวลา OT · ใบเบิกค่าใช้จ่าย EXP = คนละเรื่อง) — ต้องยืนยันกับ registry จริง (OQ-1)
- No-gap ✗: เอกสารภายใน ไม่ใช่เอกสารภาษี/บัญชี → ออกเลขตอนร่างได้
- Snapshot อนุมัติ+เซ็น ✓: เก็บ PDF ฉบับผ่านอนุญาตครบเป็นหลักฐาน · ส่งออกภายนอก ✗ (ไม่มีการส่งให้บุคคลภายนอก)
- เวอร์ชัน/เปิดใช้: register เป็น **v1 สถานะ ready (รอเปิดใช้งาน)** · ลูกค้าเปิดใช้ + ตั้งวันมีผลเองที่ F-DOCCFG · ประกาศเปิดใช้ (announcement) default ปิด

## จุดออกเลข (ENG-DOC-NUM)
| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| บันทึกครั้งแรก (สร้าง → `draft`) | 03 FN-05 createOswDraft · 05 BR-OSW-14 · 07 LD-02 | ก่อนออกเลขตรวจ **สถานะเปิดใช้ของ doc_type OSW ที่ F-DOCCFG** (ไม่เปิด = BR_DOCTYPE_INACTIVE · BR-OSW-15) · เลข immutable ไม่คืนแม้ยกเลิก |

## จุดเก็บสำเนา (ENG-DOC-STORE)
| Event | เมื่อไหร่ | อ้าง FRD |
|---|---|---|
| approved_final | ขั้นสุดท้ายของ `approval_chain` อนุญาต → `approved` | 03 FN-09 → FN-13 storeApprovedPdf · 05 BR-OSW-18 · 06 AC-18 |
หมายเหตุ: ยกเลิกหลังอนุญาต → สำเนาคงอยู่ · อัปเดต metadata สถานะ = cancelled (FN-10 · 06 XT-04)

## การตั้งค่าพิมพ์ (print settings) — ค่าเริ่มต้นตอน register
| รายการ | ค่าเริ่มต้น | แก้ได้ที่ F-DOCCFG | ใช้ใน FRD |
|---|---|---|---|
| แบบพิมพ์ | 1 แบบ · `osw_body.tpl.html` (thai-doc-pdf-generator · FORM REPLICA) | ✅ (เวอร์ชันแบบพิมพ์ใหม่ = เวอร์ชัน doc_type ใหม่) | FN-11/12 |
| รหัสควบคุมแบบฟอร์มลูกค้า | `FM-HRM-02` · `Rev. 00 : 01/07/2569` | ✅ | data `doc.form_code` · `doc.revision` |
| หัวกระดาษ / โลโก้ | ดึงจาก **Organization (ข้อมูลบริษัท)** — ไม่เก็บใน doc_type · **snapshot ลงเอกสารตอนออกเลข** | ✅ (เลือกบริษัท/สาขาตาม Organization) | FN-05 `header_snapshot` → data `company.*` |
| ขั้นต่ำบรรทัดรายการ | 5 (ตามกระดาษเดิม) | ✅ | config `min_rows` (prototype `PDF_MIN_ROWS`) |
| ขนาดกระดาษ | A4 แนวตั้ง | ❌ (กติกา thai-doc) | — |

### ช่องลายเซ็น (sign boxes) — ตาม config รายช่อง
แบบพิมพ์ **ไม่ fix จำนวนช่อง** — FN-11 สร้าง `signs[]` จาก config ด้านล่าง + `approval_chain` (DOA snapshot) แล้วเรียงแถวล่างแบบ thai-doc B6
| # | box | source | label เริ่มต้น | แสดง | หมายเหตุ |
|---|---|---|---|---|---|
| 1 | requester | ผู้ขอ (`employee_*` + `submitted_at`) | พนักงาน | ชื่อ · ตำแหน่ง · วันที่ "ส่งในระบบ …" | ร่าง = เส้นวันที่ว่าง |
| 2..N | doa_step:* | 1 ช่องต่อขั้นใน `approval_chain` | role label ของขั้น (เช่น ผู้บังคับบัญชา) | ☑ อนุญาต / ☑ ไม่อนุญาต · ชื่อ · ตำแหน่ง · วันที่ "พิจารณาในระบบ …" | DOA เพิ่ม/ลดขั้น = ช่องเพิ่ม/ลดเอง (DEC-03) |
- admin เปลี่ยน label / ซ่อนวันที่ / สลับลำดับได้ที่ F-DOCCFG · ไม่ใช้ลายมือชื่อภาพ (DEC-09)

## Dev wiring note
- `osw.osw_no = ENG-DOC-NUM.next('OSW', company_ctx)` ที่ FN-05 — ห้าม format เอง ห้าม +1 เอง
- ก่อนออกเลข: `DOCCFG.status('OSW', company_ctx)` = active (แทนการเช็คที่ F185 เดิม)
- ตอนออกเลข: เก็บ `header_snapshot` (ชื่อบริษัท · โลโก้ ref · ที่อยู่) จาก Organization ลงเอกสาร — PDF ทุกครั้งใช้ snapshot นี้ ไม่ดึงสด
- render PDF: อ่าน `print_config` (template ref · form_code · revision · min_rows · sign_boxes) จาก F-DOCCFG → FN-11 → FN-12
- ผ่านขั้นสุดท้าย: `ENG-DOC-STORE.store(pdf, 'OSW', osw_id, 'approved_final')` — engine เช็ค flag เอง
- ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine/API ของ F-DOCCFG เท่านั้น

## ผลต่อ FRD (sync แล้วใน pack v1.0.1)
| ไฟล์ | เปลี่ยน |
|---|---|
| 00 §0.5 · 02 API-12 / §2.X · 03 FN-02 / §3.4 · 05 BR-OSW-15 · 06 AC-16 / XT-05 / DoD · UI Brief §10 | เช็คเปิดใช้: F185 API-23 → **F-DOCCFG status** · เปิดใช้งานทำที่ F-DOCCFG |
| 03 FN-05 · 04 §4.2 | เพิ่ม `header_snapshot` (jsonb) ตอนออกเลข |
| 03 FN-11 · print-spec §2 | `company.*` จาก header_snapshot · `signs[]` ตาม `sign_boxes` config · `min_rows` จาก config |

## Open Questions
| # | คำถาม | ใครตอบ |
|---|---|---|
| OQ-1 | code `OSW` ชนกับ registry F-DOCCFG หรือไม่ | ทีม 2B (Sync Read `f-doccfg.html` ก่อน deploy) |
