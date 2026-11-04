# INDEX — FRD F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่

## 📂 Pack Contents
| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW | control · scope · roles · deps · classification · OQ · Coverage Manifest |
| 01_UI | Layout Decision Log · 3 หน้า + 5 modal · ข้อความจริง |
| 02_API | API-01..13 · cross-module contract |
| 03_LOGIC | FN-01..16 · F-OSW-ENG-01 · trace |
| 04_DB | 4 ตาราง · classification · PII |
| 05_RULES | BR-OSW-01..20 · state machine · VR · EC-01..24 · errors · security |
| 06_TESTS | AC-01..22 · XT-01..05 · DoD · verbatim text |
| 07_LOCKED_DECISIONS | DEC-01..10 · LD-01..07 · CD-01..04 |
| declarations/ | DOA_BRIEF · DOCCFG_BRIEF · MDOC_BRIEF_OSW + payload · DECISIONS |
| print/ | template · render_osw.py · samples · print-spec · base_form_patch.css |

## 🔍 Quick Nav by Question
- **FE dev:** 01_UI §1.0–1.2 → HTML `offsite-work-request.html` → 06 §6.10
- **BE dev (endpoint ใหม่):** 02 §2.1 → 03 §3.3 → 05 §5.2/5.4 → 04 §4.2
- **DBA:** 04 §4.2/4.3/4.6
- **QA:** 06 §6.1/6.9/6.10 → 05 §5.5
- **PM:** 00 §0.8 · 07 §7.3
- **Architect:** 03 §3.2 F-OSW-ENG-01 (CUBIC candidate) · 07 AT

## 🔗 Cross-Reference Tables
### Page → API
| Page | APIs |
|---|---|
| P-01 | API-01 · API-11 · API-10 (⋮ พิมพ์) · API-09 (⋮ ยกเลิก) |
| P-02 | API-12 · API-03 · API-04 · Document Center |
| P-03 | API-02 · API-10 · API-05/06 (M-01) · API-07 (M-02) · API-08 (M-03) · API-09 (M-04) |

### API → Logic → DB
| API | Logic | Tables |
|---|---|---|
| 01/02 | FN-01 | request · line (read) |
| 03 | FN-02/03/04/05/15 + ENG-DOC-NUM | request · line · attachment · audit |
| 04 | FN-03/04/06/15 | request · line · attachment · audit |
| 05 | FN-07 + DOA | — |
| 06 | FN-03/08/15 + DOA | request · audit |
| 07/08/13 | FN-09/13/15/16 + DOA · DOC-STORE · ENG-01 | request · audit |
| 09 | FN-10/15 + DOA · NOTIFY · DOC-STORE | request · audit |
| 10 | FN-01/11/12 + ENG-01 | request · line (read) |
| 11 | FN-01/14/15 | request · audit |
| 12 | FN-02 | — |

### Engine ↔ Feature
| Engine | Features |
|---|---|
| F-OSW-ENG-01 doc-print-template-render (NEW) | F-HR-OSW · candidate: แบบฟอร์มลูกค้าอื่นผ่าน thai-doc |
| DOA · ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY | existing |

## 🚨 R8 Verification Matrix
mutation APIs 03/04/06/07/08/09/13 → ทุกตัวมี Function ✅ · FN-01..16 ไม่มี orphan ✅ · ENG-01 ถูกเรียกผ่าน FN-12 ✅

## 📊 Pack Statistics
Pages 3 + modals 5 · APIs 13 (mutation 7) · Functions 16 · Engines 1 new + 4 existing · Tables 4 · BR 20 · VR 15 · EC 24 · AC 22 + XT 5 · OQ 10 (ปิดก่อน dev: 3)

## 🎯 Reading Order Recommendation
### First-time reader
00 → 07 §7.0 → 01 §1.0
### Onboarding new dev
00 → 01 + HTML → 02 → 03 → 04 → 05
### Architect review
00 §0.5/0.7 → 03 §3.2 → 07 §7.1/7.4

## Coverage Manifest Pointer
→ 00_OVERVIEW §0.12 (S-01..13 · R01..R20 · E01..E22 · §12.1)
