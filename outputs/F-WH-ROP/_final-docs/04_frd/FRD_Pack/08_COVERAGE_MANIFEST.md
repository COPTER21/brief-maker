# 08 COVERAGE MANIFEST · F-WH-ROP

| FN | BRD | UI | API/Logic | Rules | Tests | HTML anchor |
|---|---|---|---|---|---|---|
| FN-01 list/filter | §3,9 | P-01 | API-01/FN-01 | BR-01 | AT-01,02 | `renderTableOnly` |
| FN-02 save/validate | §6,7 | P-01 drawer | API-02/FN-02 | BR-02 | AT-03..07 | `ropSaveFromDrawer` |
| FN-03 active policy | §7 | P-01/P-02 | FN-03 | BR-01 | AT-01,02 | `ropPolicyActive` |
| FN-04 evaluate | §7 | P-02 drawer | API-03/FN-04 | BR-03..05 | AT-08..15 | `ropEvaluatePair` |
| FN-05 visible states | §9,10 | P-02 | API-03 | BR-06 | AT-16..18 | status pills/check card |
| FN-06 notification | §11,14 | P-02 toast | API-05/FN-06 | BR-08 | AT-22,23 | `ropNcCandidate` |
| FN-07 PR Draft | §3,5,11 | P-02/P-03 | API-06/FN-07 | BR-09,10 | AT-24..27 | `ropPreparePR` |
| FN-08 history | §8,9 | P-03 | API-07/FN-08 | BR-11 | AT-28 | `ropEventLabel/Detail` |
| DECL-NTF | §14 | toast only | API-05 | BR-08 | AT-22,23 | NTF envelope |
| DECL-CSQ | §14,15 | no 7C card | API-02/FN-02 | BR-CSQ-01..05 | AT-29..32 | ENG-CSQ contract comment |

Scope locks 10/10 mapped. FN 8/8 mapped. Negative cases include every validation branch and dependency failure. DOA/DOCCFG: N/A by LOCK-10.
