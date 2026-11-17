# INDEX — FRD F-TMP-008 สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (MTS)
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error + field DOA (null) |
| 03_LOGIC | BE — FN-01..09 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..13 · TC-D01..06 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..20 ห้ามตัดสินขัด |
| declarations/ | NTF · DOCCFG · MDOC ฉบับจริง (ไม่มี DOA — DEC-03) |

## Cross-Reference
Page→API: P-01→API-01/08 · P-02→API-03/04/09 · P-03→API-02/05/06/07
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 3 · API 9 · FN 9 · BR 12 · VR 6 · EC 11 · AC 13 · deny 6
