# FRD Pack — F-TMP-010 หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว

| ไฟล์ | เนื้อหา |
|---|---|
| `00_OVERVIEW.md` | ขอบเขต · actor · ภาพรวมหน้าจอ · สิ่งที่ไม่ทำรอบนี้ |
| `01_UI.md` | หน้าจอ P-01..P-03 + modal · ช่องตามกระดาษ 1:1 · microcopy |
| `02_API.md` | endpoint · payload · event ที่ยิง |
| `03_LOGIC.md` | FN-01..FN-12 (ตรรกะต่อฟังก์ชัน · จุดออกเลข · จุดเก็บสำเนา · จุดยิง event) |
| `04_DB.md` | ตาราง · คอลัมน์ · index · header_snapshot · approval_chain / doa_ref |
| `05_RULES.md` | BR / VR / EC ทั้งหมด พร้อมผูกมติ DEC |
| `06_TESTS.md` | เคสทดสอบระดับ FRD (รวมเคสปฏิเสธสิทธิ์) |
| `07_LOCKED_DECISIONS.md` | §7.0 DECISIONS.lock (DEC-01..DEC-17) · §7.1 ผลต่อ FRD · §7.2 Carry-over Decisions |

- Variant: **STANDARD** · Input Mode 0 (PREBRIEF v2 + FORM_SPEC + DECISIONS.lock)
- แบบพิมพ์: `print/form.tpl.html` (Replica · FM-HRM-51 Rev. 00 : 01/07/2569) · รหัสเอกสาร **IMC**
- Prototype: `feature.html` (Pattern Q2 · audit FAIL 0 · stub DOM 50/50)
- โหมดไม่เฝ้า: มติทุกข้อเป็น **AI-DEFAULT** ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT
