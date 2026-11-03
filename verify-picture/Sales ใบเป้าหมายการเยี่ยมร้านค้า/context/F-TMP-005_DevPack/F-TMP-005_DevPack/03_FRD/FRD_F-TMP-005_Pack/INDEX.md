# INDEX — FRD F-TMP-005 ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade

| ไฟล์ | เนื้อหา |
|---|---|
| 00_OVERVIEW.md | scope · roles · dependencies · security · OQ · coverage |
| 01_UI.md | layout decisions · P-01..P-03 · journey · empty/error |
| 02_API.md | API-01..12 · contract · cross-module |
| 03_LOGIC.md | FN-01..FN-10 · engines · trace |
| 04_DB.md | visit_target · visit_target_day · visit_target_store · audit |
| 05_RULES.md | BR-01..15 · state · permission · VR-01..10 · EC-01..10 |
| 06_TESTS.md | AC-01..14 · deny TC-D01..08 · DoD · microcopy |
| 07_LOCKED_DECISIONS.md | §7.0 DEC-01..18 · LD-01..05 |
| _SECTION_N.md | ผล frd_lint |
| declarations/ | SVT.doa.yaml · DOA_BRIEF · SVT.doccfg.yaml · DOCCFG_BRIEF · SVT.ntf.yaml · NTF_BRIEF · SVT.mdoc.yaml · MDOC_BRIEF |

## Cross-Reference
- BRD §2.4 → 07 §7.0 · BRD §8 BR → 05 §5.1 · BRD §9 EC → 05 §5.5 · BRD §6 US → 06 §6.1
## R8 Verification
- ทุก API ผูก FN (02 §2.4) · ทุก FN ผูก API (03 §3.3) · ทุก AC ผูก FN (06 §6.8) ✓
## Stats
- API 12 · FN 10 · BR 15 · VR 10 · EC 10 · AC 14 · deny 8 · DEC 18
