# INDEX — FRD F-TMP-008 หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล

| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW.md | ขอบเขต · role · dependency · security · coverage manifest |
| 01_UI.md | Layout Decision Log · หน้าจอ · journey · empty/error |
| 02_API.md | endpoint · contract · trace ไป logic |
| 03_LOGIC.md | Functions FN-01..FN-10 + engines ที่เรียกใช้ |
| 04_DB.md | ตาราง · field dictionary · data classification · retention |
| 05_RULES.md | business rules · state machine · permission · validation · error · notification |
| 06_TESTS.md | acceptance · deny cases · test data · DoD |
| 07_LOCKED_DECISIONS.md | §7.0 = DECISIONS.lock (DEC-01..DEC-15) · LD · deviation · OQ |

## Cross-Reference
- BRD: `BRD_F-TMP-008.md` (APPROVED · AI-DEFAULT)
- HTML: `feature.html` (Pattern Q2 · audit FAIL 0 · stub DOM smoke 39/39)
- แบบพิมพ์: `print/form.tpl.html` + `print/PDC_print-spec.md` + `print/PDC_data-contract.md`
- Declaration: `DOCCFG_BRIEF_F-TMP-008.md` · `NTF_BRIEF_F-TMP-008.md` · `MDOC_BRIEF_PDC.md` · `DOA_BRIEF_F-TMP-008.md` (ประกาศ 0 ขั้น · dynamic)

## R8 Verification
ทุก mutation API ใน 02_API มี FN ปลายทางใน 03_LOGIC (ดู §2.4 / §3.3)

## Stats
9 ไฟล์ · variant STANDARD · FN 10 ตัว · ตาราง 4 + attachment · เคสทดสอบ 24
