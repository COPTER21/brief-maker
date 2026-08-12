# 06_TESTS — F-ORG-001 Organization Management

> Acceptance per FR + DoD. ใช้คู่ frd-qa-generator-v2 (สร้าง SCN/TC/DATA/CSV).

## §6.1 Acceptance (Given-When-Then)
| ID | Scenario | Expected |
|---|---|---|
| AC-01 | Given list สาขา, When คลิกแถว, Then เปิด P-06 detail สาขานั้น | route #/branch/:id |
| AC-02 | Given drawer create division, When เว้น name_th, Then error | "กรุณาระบุชื่อ (ไทย)" |
| AC-03 | Given dept create, When เลือกสายงาน, Then บันทึก + นับใน division | deptCount +1 |
| AC-04 | Given dept create, When เว้นสายงาน, Then ขึ้นตรงบริษัท (chart ใต้ Company) | EC-04 |
| AC-05 | Given position, When เลือกสายงานไม่เลือกแผนก, Then list แสดง tag "สายงาน" | BR-04/EC-05 |
| AC-06 | Given parent dropdown, When แก้ dept ตัวเอง, Then ตัวเอง+ลูกหลานไม่อยู่ในตัวเลือก | BR-06 |
| AC-07 | Given ลบ division มีแผนก, When ยืนยัน, Then แผนก/ตำแหน่งสังกัด → null | BR-07/EC-01 |
| AC-08 | Given ลบ dept มีลูก, When ยืนยัน, Then ลูกเลื่อนขึ้น parent | BR-08/EC-02 |
| AC-09 | Given chart มี cycle, When render, Then ไม่ loop + node ครบ | EC-03 |
| AC-10 | Given CSV import Replace, When validate, Then แสดง pass/fail + error รายแถว ก่อน apply | BR-10 |
| AC-11 | Given CSV row ref code ไม่มี, When validate, Then row นั้น fail (ข้าม) ไม่ทำทั้งไฟล์ fail | EC-06 |
| AC-12 | Given Export→แก้→Import Replace, When apply, Then ข้อมูลตรง (round-trip) | BR-10 |
| AC-13 | Given CSV Merge code ซ้ำ, When apply, Then update (id เดิมคงอยู่) | BR-10 |
| AC-14 | Given role ไม่ผ่าน, When ดู position, Then salary band ซ่อน/`***` | §5.7 Restricted |
| AC-15 | Given export โดย role ไม่ผ่าน, Then คอลัมน์ Confidential/Restricted ถูกตัด | §4.6.5 |
| AC-16 | Given Company Edit, When อัปโหลดโลโก้ PNG ≤2MB, Then preview เปลี่ยนทันที + บันทึกแล้ว hero แสดงโลโก้ | BR-14/API-13 |
| AC-17 | Given อัปโหลดไฟล์ผิดชนิด/ใหญ่เกิน 2MB, Then ERR_LOGO_TYPE/ERR_LOGO_SIZE + ไม่บันทึก | EC-11 |
| AC-18 | Given มีโลโก้, When กดลบ, Then hero กลับเป็นไอคอนเริ่มต้น (ไม่กระทบเอกสารที่ออกแล้ว) | BR-14/API-14/EC-12 |

## §6.2 Definition of Done
- [ ] 5 entity CRUD + toggle + delete+cascade ทำงานครบ
- [ ] chart 2 แบบ coverage 100% (cycle-safe) — ตรง prototype QC
- [ ] CSV export(BOM)+import(Replace/Merge+validate) ครบ div/dept/pos
- [ ] landing detail ทุก entity + row-click + stopPropagation
- [ ] ทุก mutation เขียน Immutable audit (S01-07)
- [ ] Data Classification enforce (Restricted salary, Confidential PII)
- [ ] RLS multi-tenant + optimistic lock (version)
- [ ] Pre-DOA fields พร้อม wire DOA
- [ ] Iron Rules html-generator-v3 ผ่าน (verified prototype)
