# INDEX — FRD F-TMP-006 รายงานการเข้า-ออก ห้อง server
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error |
| 03_LOGIC | BE — FN-01..10 (FN-05 สงวน) |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..14 · TC-D01..08 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..14 ห้ามตัดสินขัด |
| declarations/ | NTF · DOCCFG · MDOC ฉบับจริง (ไม่มี DOA — DEC-03) |

## Cross-Reference
Page→API: P-01→API-01/09 · P-02→API-03/04/10 · P-03→API-02/05/06/07/08
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 4 · API 10 · FN 9 · BR 14 · VR 6 · EC 10 · AC 14 · deny 8
