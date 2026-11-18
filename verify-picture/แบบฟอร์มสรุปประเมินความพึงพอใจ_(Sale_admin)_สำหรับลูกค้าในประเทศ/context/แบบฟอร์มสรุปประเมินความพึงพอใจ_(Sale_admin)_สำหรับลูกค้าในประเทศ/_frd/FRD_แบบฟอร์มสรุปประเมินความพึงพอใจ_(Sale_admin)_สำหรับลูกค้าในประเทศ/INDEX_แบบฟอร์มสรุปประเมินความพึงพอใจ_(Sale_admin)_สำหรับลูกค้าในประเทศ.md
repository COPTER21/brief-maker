# INDEX — FRD F-TMP-005 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (SDS)
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error + ฟิลด์อนุมัติ (DOA) |
| 03_LOGIC | BE — FN-01..09 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..14 · TC-D01..06 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..16 ห้ามตัดสินขัด |
| declarations/ | DOA · NTF · DOCCFG · MDOC ฉบับจริง |

## Cross-Reference
Page→API: P-01→API-01/10 · P-02→API-03/04/05/11 · P-03→API-02/06..09
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 5 · API 11 · FN 9 · BR 14 · VR 7 · EC 12 · AC 14 · deny 6
