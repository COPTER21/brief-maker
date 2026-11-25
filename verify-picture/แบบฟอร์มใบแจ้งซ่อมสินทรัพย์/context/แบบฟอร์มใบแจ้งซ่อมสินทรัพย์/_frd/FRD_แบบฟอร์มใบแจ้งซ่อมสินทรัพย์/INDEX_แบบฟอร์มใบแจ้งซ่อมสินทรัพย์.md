# INDEX — FRD F-TMP-001 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error + events |
| 03_LOGIC | BE — FN-01..10 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission/notify |
| 06_TESTS | QA — AC-01..13 · TC-D01..07 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..16 ห้ามตัดสินขัด |
| _SECTION_N | ผล frd_lint (Phase 3.6) |
| declarations/ | DOA · NTF · DOCCFG · MDOC ฉบับจริง |

## Cross-Reference
Page→API: P-01→API-01/10 · P-02→API-03/04/11 · P-03→API-02/05..09
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 5 · API 11 · FN 10 · BR 13 (+DOA 5) · VR 5 · EC 9 · AC 13 · deny 7
