# INDEX — FRD F-TMP-003 แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน

| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW.md | scope · roles · dependencies · security · OQ · coverage |
| 01_UI.md | layout decisions · P-01..P-03 · ช่องตามกระดาษ · journey · empty/error |
| 02_API.md | API-01..12 · contract · DOA · cross-module |
| 03_LOGIC.md | FN-01..FN-09 · engines · trace |
| 04_DB.md | visitor_access_request · approval_chain · audit |
| 05_RULES.md | BR-01..12 · BR-DOA-01..05 · state · permission · VR-01..08 · EC-01..11 |
| 06_TESTS.md | AC-01..14 · deny TC-D01..08 · DoD · microcopy |
| 07_LOCKED_DECISIONS.md | §7.0 DEC-01..15 · LD-01..04 |
| _SECTION_N.md | ผล frd_lint |
| declarations/ | VAR.doa.yaml · DOA_BRIEF · VAR.doccfg.yaml · DOCCFG_BRIEF · VAR.ntf.yaml · NTF_BRIEF · VAR.mdoc.yaml · MDOC_BRIEF |

## Cross-Reference
- BRD §2.4 → 07 §7.0 · BRD §8 BR → 05 §5.1 · BRD §9 EC → 05 §5.5 · BRD §6 US → 06 §6.1
## R8 Verification
- ทุก API ผูก FN (02 §2.4) · ทุก FN ผูก API (03 §3.3) · ทุก AC ผูก FN (06 §6.8) ✓
## Stats
- API 12 · FN 9 · BR 12 (+ BR-DOA 5) · VR 8 · EC 11 · AC 14 · deny 8 · DEC 15
