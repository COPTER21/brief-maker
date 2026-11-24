# INDEX — FRD F-TMP-004 แบบฟอร์มแผนโครงการ
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error |
| 03_LOGIC | BE — FN-01..11 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..18 · TC-D01..09 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..18 ห้ามตัดสินขัด |
| declarations/ | DOA · NTF · DOCCFG · MDOC ฉบับจริง |

## Cross-Reference
Page→API: P-01→API-01/11 · P-02→API-03/04/12/13 · P-03→API-02/05..10
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN (ยกเว้น API-12/13 = Document Center/HR/Organization) · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 6 · API 13 · FN 11 · BR 17 (+DOA 5) · VR 9 · EC 11 · AC 18 · deny 9
