# Gate Policy v2.1

## Verdict → action
| Verdict | action |
|---|---|
| PASS | next |
| WARN | append `_LANE_LOG.md` → next · ถ้า cosmetic ลอง auto-fix 1 ครั้งก่อนไปต่อ |
| BLOCK | fix loop (ตาราง) · ฉีด report รอบก่อนเข้า fixer · รัน gate ซ้ำ · นับ `retries[stage]` ใน `_LANE_STATE.json` |

## Retry matrix
| Gate | fixer | rerun from | cap |
|---|---|---|---|
| S0.5 baseline | feature-review-standard baseline (ค้นเพิ่ม 1 รอบ) | S0.5 | 1 (ตกแล้วต่อด้วย WARN) |
| S1 prebrief gate | `feature-prebrief` + gap list (`prebrief_checklist.py` output) | S1 | 2 |
| S3a audit | patch script (python/str_replace · ห้าม regen ทั้งไฟล์) | S3a | 3 |
| S3b qc-ux (incl. render) | `qc-ux-html-checker` fix mode (surgical ตาม fix list) | S3a | 3 |
| S3c coverage R1 | `html-generator-v9` patch เฉพาะ FN/hook/surface ที่ report ชี้ | S3a | 2 |
| S4 BRD | `brd-generator-full` + AI Review รอบก่อน | S4 | 2 |
| S5 FRD | `frd-generator-v6` + Verification Report รอบก่อน | S5 | 2 |
| S6.5 coverage R2 / R15 | FRD (rule หาย) หรือ TC (FN ไม่มีเคส / R15 ไม่ตรง → regen testset จาก QA HTML) | S5 หรือ S6 | 2 |

- cap รวมต่อ feature **10** รอบ · `same_issue_count ≥ 2` → หยุดวนทันที
- ครบ cap → `_BLOCKED.md` (issues ที่เหลือ · รอบที่ลอง · ไฟล์ล่าสุด) · state `blocked` · **ไป feature ถัดไป** · S9 sync เป็น "ติดปัญหา" ห้ามแขวน DevPack

## Hard Stop (ห้าม auto-fix — `_BLOCKED.md` ตั้งแต่รอบแรก)
1. artifact ขัด LOCK/มติ ใน LANE_BRIEF (scope drift)
2. brief ไม่มี LOCK/OQ ref เลย
3. OQ business-critical (เงิน/กฎหมาย/สิทธิ์/ท่อ 7C) ไม่มีคำตอบใน scope note
4. governance invariant: hardcoded approval chain · hard delete · legal param ไม่มี effective_date · CSQ ประกาศ OC/DC-doc/SC
5. S1.8 ท่อที่ need แต่ declaration skill gen ไม่ได้

## Default table (ไม่ถาม)
| ไม่ชัด | default | tag |
|---|---|---|
| shell | ERP (sidebar 232/244 rail) | — |
| archetype ไม่ชัด | master (A+B+C) | `[ASSUMED]` ใน brief |
| DOA วงเงิน | ไม่มีวงเงิน · สายเดียว · ตามตำแหน่ง | `[ASSUMED]` ใน DOA_BRIEF |
| NTF ช่องทาง | in-app + email (ตาม ENG-NOTIFY default) | `[ASSUMED]` |
| CSQ ท่อ | ตาม signal ใน §12 เท่านั้น · ไม่แน่ใจ = ไม่ประกาศ + OQ | `[ASSUMED]` |
| PDF DOC บริษัท/ภาษี | placeholder 2BSimple มาตรฐาน | — |
| OQ อื่น | ตาม `html-generator-v9/references/gap-detection.md` | `[ASSUMED]` PREBRIEF/BRD §OQ |
ทุก `[ASSUMED]` ขึ้น REVIEW_SHEET ให้ Strike/BA เคาะ
