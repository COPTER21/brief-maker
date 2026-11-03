# INDEX — FRD F-TMP-001 แบบประเมินความพึงพอใจลูกค้า
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error |
| 03_LOGIC | BE — FN-01..09 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..13 · TC-D01..05 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..13 ห้ามตัดสินขัด |
| declarations/ | DOCCFG · MDOC · NTF ฉบับจริง (ไม่มี DOA — DEC-03) |

## Cross-Reference
Page→API: P-01→API-01/08 · P-02→API-03/04/09/10 · P-03→API-02/05/06/07
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN (ยกเว้น API-10 ของ feature เจ้าของ Customer) · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 3 · API 10 · FN 9 · BR 12 · VR 6 · EC 8 · AC 13 · deny 5
