# INDEX — FRD F-TMP-002 แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview)

| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW.md | scope · roles · dependencies · security · OQ · coverage |
| 01_UI.md | layout decisions · P-01..P-03 · journey · empty/error |
| 02_API.md | API-01..12 · contract · cross-module |
| 03_LOGIC.md | FN-01..FN-10 · engines · trace |
| 04_DB.md | exit_interview · reason · improvement · audit |
| 05_RULES.md | BR-01..14 · state · permission · VR-01..09 · EC-01..10 |
| 06_TESTS.md | AC-01..13 · deny TC-D01..08 · DoD · microcopy |
| 07_LOCKED_DECISIONS.md | §7.0 DEC-01..17 · LD-01..04 |
| _SECTION_N.md | ผล frd_lint |
| declarations/ | EXI.doccfg.yaml · DOCCFG_BRIEF · EXI.ntf.yaml · NTF_BRIEF · EXI.mdoc.yaml · MDOC_BRIEF (ไม่มี DOA_BRIEF — DEC-03) |

## Cross-Reference
- BRD §2.4 → 07 §7.0 · BRD §8 BR → 05 §5.1 · BRD §9 EC → 05 §5.5 · BRD §6 US → 06 §6.1
## R8 Verification
- ทุก API ผูก FN (02 §2.4) · ทุก FN ผูก API (03 §3.3) · ทุก AC ผูก FN (06 §6.8) ✓
## Stats
- API 12 · FN 10 · BR 14 · VR 9 · EC 10 · AC 13 · deny 8 · DEC 17
