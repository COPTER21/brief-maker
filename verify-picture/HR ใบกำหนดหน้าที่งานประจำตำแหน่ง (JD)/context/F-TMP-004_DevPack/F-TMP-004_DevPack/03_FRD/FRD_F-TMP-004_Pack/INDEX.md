# INDEX — FRD F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)

| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW.md | scope · roles · dependencies · security · OQ · coverage |
| 01_UI.md | layout decisions · P-01..P-03 · journey · empty/error |
| 02_API.md | API-01..14 · contract · cross-module |
| 03_LOGIC.md | FN-01..FN-12 · engines · trace |
| 04_DB.md | job_description · superior · subordinate · audit |
| 05_RULES.md | BR-01..16 · state · permission · VR-01..09 · EC-01..10 |
| 06_TESTS.md | AC-01..15 · deny TC-D01..09 · DoD · microcopy |
| 07_LOCKED_DECISIONS.md | §7.0 DEC-01..17 · LD-01..05 |
| _SECTION_N.md | ผล frd_lint |
| declarations/ | JD.doa.yaml · DOA_BRIEF · JD.doccfg.yaml · DOCCFG_BRIEF · JD.ntf.yaml · NTF_BRIEF · JD.mdoc.yaml · MDOC_BRIEF |

## Cross-Reference
- BRD §2.4 → 07 §7.0 · BRD §8 BR → 05 §5.1 · BRD §9 EC → 05 §5.5 · BRD §6 US → 06 §6.1
## R8 Verification
- ทุก API ผูก FN (02 §2.4) · ทุก FN ผูก API (03 §3.3) · ทุก AC ผูก FN (06 §6.8) ✓
## Stats
- API 14 · FN 12 · BR 16 · VR 9 · EC 10 · AC 15 · deny 9 · DEC 17
