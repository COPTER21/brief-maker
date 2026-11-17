# INDEX — FRD F-TMP-001 ใบตรวจเช็คถังดับเพลิง
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error + events |
| 03_LOGIC | BE — FN-01..09 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..12 · TC-D01..06 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..13 ห้ามตัดสินขัด |
| declarations/ | NTF · DOCCFG · MDOC ฉบับจริง (ไม่มี DOA — DEC-03) |

## Cross-Reference
Page→API: P-01→API-01/08 · P-02→API-03/09 · P-03→API-02/04/05/06/07
API→Logic: 03 §3.3 · Logic→AC: 06 §6.1

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 3 · API 9 · FN 9 · BR 13 · VR 6 · EC 8 · AC 12 · deny 6
