# INDEX — FRD F-TMP-002 บันทึกภายใน

| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW.md | Document control · scope · roles · dependencies · คำถามค้าง |
| 01_UI.md | 4 route · หน้ารายการ · wizard 3 ขั้น · view 4 แท็บ · modal · microcopy |
| 02_API.md | API-01…API-12 + รหัสผลลัพธ์ |
| 03_LOGIC.md | MEM-FN-01…MEM-FN-10 + engine ที่เรียก + trace |
| 04_DB.md | `memo` · `memo_attachment` · `memo_audit` |
| 05_RULES.md | BR-MEM-01…11 · VR-01…04 · EC-01…11 |
| 06_TESTS.md | AC · NG · PM (สิทธิ์) · ER · PR (แบบพิมพ์) · DoD |
| 07_LOCKED_DECISIONS.md | DEC-01…DEC-15 + convention deviations |

## Function Trace
| Function | API | DB | Rule | Test |
|---|---|---|---|---|
| MEM-FN-01 createMemoDraft | API-03 | `memo.doc_no` `header_snapshot` | BR-MEM-01/02 | AC-01 · NG-01 · NG-06 |
| MEM-FN-02 updateMemoDraft | API-04 | `memo` | BR-MEM-03 | PM-05 |
| MEM-FN-03 submitMemo | API-05 | `approval_chain` `doa_ref` | BR-MEM-07/08 | AC-02 · AC-08 · PM-07 |
| MEM-FN-04 approveMemoStep | API-06 | `approval_chain` `legal_opinion` | BR-MEM-10 | AC-03 · PM-06 · ER-01 |
| MEM-FN-05 rejectMemo | API-07 | `approval_chain` | BR-MEM-04 | AC-05 · NG-02 |
| MEM-FN-06 cancelMemo | API-08 | `cancel_reason` | BR-MEM-05 | AC-06 · NG-03 · EC-09 |
| MEM-FN-07 listMemo/getMemo | API-01/02/11 | index | BR-MEM-06 | PM-01…PM-04 · AC-07 |
| MEM-FN-08 reopenRejectedMemo | API-09 | `status` | BR-MEM-04 | AC-05 |
| MEM-FN-09 renderMemoPdf | API-10 | `header_snapshot` `approval_chain` | VR-01…03 | PR-01…PR-07 |
| MEM-FN-10 attachMemoFile | API-12 | `memo_attachment` | BR-MEM-09 | NG-04 · ER-04 |

## Quick Nav
- route ของ prototype: `#/memo` · `#/memo/create` · `#/memo/edit/:id` · `#/memo/view/:id`
- แบบพิมพ์: `print/form.tpl.html` · `print/profile.json` · `print/print_config.json` · `print/MEM_print-spec.md`
- ใบประกาศ: `DOCCFG_BRIEF_F-TMP-002.md` · `DOA_BRIEF_F-TMP-002.md` · `NTF_BRIEF_F-TMP-002.md` · `MDOC_BRIEF_MEM.md`
