# INDEX — FRD F-TMP-009 แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง (IVMG)
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error |
| 03_LOGIC | BE — FN-01..13 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..16 · TC-D01..08 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..21 ห้ามตัดสินขัด |
| declarations/ | DOA · NTF · DOCCFG · MDOC ฉบับจริง |

## Cross-Reference
Page→API: P-01→API-01/10 · P-02→API-03/04/11 · P-03→API-02/05..09/13 · P-04→API-11/12
API→Logic: 02 §2.1 · Logic→AC: 06 §6.8

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 4 · modal 6 · API 13 · FN 13 · BR 18 · VR 12 · EC 18 · AC 16 · deny 8
