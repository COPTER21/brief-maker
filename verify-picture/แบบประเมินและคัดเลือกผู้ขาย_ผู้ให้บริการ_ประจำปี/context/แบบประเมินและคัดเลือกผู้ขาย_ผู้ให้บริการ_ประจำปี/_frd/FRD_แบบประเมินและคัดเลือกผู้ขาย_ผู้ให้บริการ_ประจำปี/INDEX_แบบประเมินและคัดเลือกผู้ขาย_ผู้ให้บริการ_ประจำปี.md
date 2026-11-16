# INDEX — FRD F-TMP-004 แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error |
| 03_LOGIC | BE — FN-01..11 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission/notification |
| 06_TESTS | QA — AC-01..15 · TC-D01..07 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..17 ห้ามตัดสินขัด |
| declarations/ | DOA · NTF · DOCCFG · MDOC ฉบับจริง |

## Cross-Reference
Page→API: P-01→API-01/10 · P-02→API-03/04/11/12 · P-03→API-02/05..09
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 5 · API 12 · FN 11 · BR 15 (+BR-DOA 4) · VR 10 · EC 12 · AC 15 · deny 7
