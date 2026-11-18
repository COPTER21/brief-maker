# INDEX — FRD F-TMP-009 แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 00_OVERVIEW | ทุกคน — scope · roles · deps · OQ · Coverage Manifest |
| 01_UI | FE — จอ (source of truth = feature.html) |
| 02_API | BE — endpoint + error |
| 03_LOGIC | BE — FN-01..11 |
| 04_DB | DBA |
| 05_RULES | BE/QA — BR/VR/EC/state/permission |
| 06_TESTS | QA — AC-01..14 · TC-D01..07 |
| 07_LOCKED_DECISIONS | ทุกคน — DEC-01..14 ห้ามตัดสินขัด |
| declarations/ | DOA · NTF · DOCCFG · MDOC ฉบับจริง |

## Cross-Reference
Page→API: P-01→API-01/12 · P-02→API-03/04/13 · P-03→API-02/05..11
API→Logic: 03 §3.3 · Logic→AC: 06 §6.4

## R8 Verification
ทุก API มี FN · ทุก FN มี API · ทุก AC มี FN ✓

## Stats
หน้า 3 · modal 7 · API 13 · FN 11 · BR 12 · VR 9 · EC 8 · AC 14 · deny 7
