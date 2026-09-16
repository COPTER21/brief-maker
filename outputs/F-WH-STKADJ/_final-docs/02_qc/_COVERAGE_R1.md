# Coverage Report — Round 1 (HTML vs Contract) · F-WH-STKADJ Stock Adjustment

> Gate: **qc-coverage-checker** รอบ 1 (RE-GATE · final · regen on final bytes) · 2026-09-16
> Contract: `PREBRIEF_F-WH-STKADJ.md` + `FUNCTION_CHECKLIST_F-WH-STKADJ.md` (**55 FN**) · chip `dec:[doa,ntf,csq,doccfg,pdfdoc]`
> Artifact: `outputs/F-WH-STKADJ/F-WH-STKADJ.html` (1160 บรรทัด · 167.4K)
> Prior run: **BLOCK** — เหตุผลเดียว = **BR-26** (แหล่งที่มา `จากใบนับ` บังคับเลือก `ref_count_doc`) อยู่ใน contract แต่ยังไม่ enforce ใน HTML
> UI fixes รอบนี้ (verified · ไม่แตะ FN/business logic): (1) scroll-lock trap-stack balance `_trapStack` push/pop (L314,327,331-333) · (2) combobox z-index `--z-combopop:75` (L34) ผูก `.combo-pop,.menu-fixed` (L188) → popup ลอยเหนือ modal (`--z-modal:70`)

## ⭐ VERDICT: **PASS**

- **FN coverage: 55/55** — ทุก FN มี hook จริงใน HTML (route + selector + handler เดินได้) · FN-52 **hooked เต็ม**
- **BR-26 = FIXED & ENFORCED** — บล็อกจริงทั้ง 2 จุด (`wizardNext` step-1 L898 + `submitForApproval` L916) → prior BLOCK **RESOLVED**
- **BR-01..BR-27 ครอบครบ · S-01..S-26 ครอบครบ**
- **Declaration: 5/5 ตรง chip — ไม่มี DIVERGENCE**
- **Pattern Q surfaces ครบ** (list + wizard 5 + view 4 tabs + เอกสารแนบ landing + B2 v2)
- **Scope creep = 0** — negatives (FN-32/35/36/45..49) ยังยืน · FN-35 negative holds

> หมายเหตุ parser: `prebrief_checklist.py` ตัด glyph `★` ใน `| FN-52 ★ |` ทิ้ง (parse ได้ 54 FN + scenarios_without_fn=['S-26'] เป็น **false hole**) — ยืนยัน 55 FN ด้วย `grep -oE 'FN-[0-9]+' | sort -u` = 55 (FN-01..FN-52 + FN-90/91/92 · เลขไม่ต่อเนื่องแต่นับ unique ได้ 55). S-26 ↔ FN-52 map จริงในโค้ด. ค่า `RS-99` เป็นรหัสเหตุผล ไม่ใช่ scenario — S จริง S-01..S-26 เท่านั้น.

---

## 1. BR-26 — จุดที่เคยเป็น BLOCK · ยืนยันการ enforce (grep + อ่านโค้ด · final bytes)

| จุด enforce | บรรทัด | หลักฐาน (verbatim) | ผล |
|---|---|---|---|
| `wizardNext` step-1 | 898 | `if(d.source==='count'&&!d.ref_count_doc){ markErr('f-source',true); bad=true; } if(bad) return showToast(...'เลือกใบนับต้นเรื่อง (F084/F086) ก่อน (BR-26)'...)` | บล็อกไปขั้นถัดไป + markErr กรอบแดงที่ `f-source` (id จริง L790) + toast อ้าง BR-26 ✓ |
| `submitForApproval` | 916 | `if(d.source==='count'&&!d.ref_count_doc){ createWizard.step=1; renderCreateDrawer(); return showToast('เลือกใบนับต้นเรื่อง (F084/F086) ก่อน (BR-26)','warning'); }` | กระโดดกลับ step 1 + บล็อกส่ง ✓ |
| `buildDoc` sanitize | 909 | `ref_count_doc:d.source==='count'?d.ref_count_doc:null` | `ปรับตรง` ล้าง ref (ไม่บังคับ) ✓ |
| `setAdjSource` | 800 | `if(v!=='count') d.ref_count_doc=null;` | สลับกลับ `ปรับตรง` เคลียร์ ref ✓ |

**สรุป BR-26:** enforce แล้วจริง**ทั้ง 2 guard** (ปุ่ม "ถัดไป" และ "ส่งอนุมัติ") · `markErr` ชี้ id `f-source` ที่มีจริง (L790) → กรอบแดง inline ขึ้นถูกต้อง (WARN เดิม `f-countdoc` **หายแล้ว** · grep `f-countdoc`=0) · e2e พิสูจน์ 58/58 cases. **Prior BLOCK RESOLVED.**

---

## 2. FN Coverage Matrix (55/55) — HTML evidence

| FN | ความสามารถ | HTML evidence (route/selector/handler) | ผล |
|---|---|---|---|
| FN-01 | ปรับยอดกักกัน → picker เหลือ QA-* | line-bin filter `at.binTypes.includes(b.type)` (L946) · adjType→binTypes | ✓ |
| FN-02 | ตัดจำหน่ายของเสีย → picker เหลือ DM-* | เดียวกัน L946 · adjType `damage`→bin `damage` | ✓ |
| FN-03 | bin ล็อก/โซนปิด = disabled + เหตุ | bin combo locked disabled + reason (L946-951) | ✓ |
| FN-04 | ยอดระบบ auto + ผลต่าง + (ชิปเขียว) | line compute + `diffChip` · sysQty snapshot (L843) | ✓ |
| FN-05 | ผลต่าง − (ชิปแดง) | `diffChip` สี danger (L843) | ✓ |
| FN-06 | มูลค่า = ผลต่าง × ต้นทุน | `lineDiff`×cost (L533,843) | ✓ |
| FN-07 | สลับโหมดกรอก แปลงกลับไปมา | `gridMode` correct/delta · `lineDiff` (L741,904) | ✓ |
| FN-08 | totals Σ\|มูลค่า\| vs สุทธิ แยกชัด | `abs`/`net` totals + summary (L1033) | ✓ |
| FN-09 | เปลี่ยนคลังมีบรรทัด → confirm ล้าง | field-help + confirm-clear on wh change (L786) | ✓ |
| FN-10 | คู่ (bin,สินค้า) ซ้ำ → เตือน | dup-pair guard toast BR-01 (L902) | ✓ |
| FN-11 | ผลต่าง = 0 → บล็อก | `lineDiff===0` guard (L901) BR-02 | ✓ |
| FN-12 | ปรับลดติดลบ → บล็อก + คงเหลือจริง | `sysQty+diff<0` guard (L901) BR-03 | ✓ |
| FN-13 | ต้นทุน mock มีป้าย FWD-WIRE valuation | `FWD-WIRE: valuation engine` (L812,1034) · footer "มูลค่าอ้างอิงจาก Item Master (mock)" (L693) อ่านอย่างเดียว | ✓ |
| FN-14 | ขั้นอนุมัติแสดง Σ\|มูลค่า\| + ชั้น | step4 `abs`/DOA tiers (L1033,1075) | ✓ |
| FN-15 | มูลค่าต่ำ → ชั้นเดียว | DOA tier(abs) จุดตัด mock | ✓ |
| FN-16 | มูลค่าสูง → หลายชั้น เรียงลำดับ | slots numbered 1→N (L1075) | ✓ |
| FN-17 | ทุก slot ต้องคนจริง — ว่าง = ส่งไม่ได้ | `_slotErr` + `slots.some(!assignee)` (L916) BR-10 | ✓ |
| FN-18 | บรรทัดไม่มีเหตุผล → ส่งไม่ได้ + ชี้ | `if(!l.reason) return showToast(...BR-06)` (L904) | ✓ |
| FN-19 | บันทึกร่าง ไม่กระทบสต๊อก ไม่มีเลขจริง | draft code:null · `(ร่าง — ยังไม่ออกเลขที่)` `displayCode` | ✓ |
| FN-20 | ส่งอนุมัติ → ออก ADJ-YYYY-NNNN | เลขออกตอนส่ง (L570 ENG-DOC-NUM/DOCCFG · L881/1077 microcopy) | ✓ |
| FN-21 | อนุมัติต่อ slot → ครบ = อนุมัติแล้ว | `openApprove`/chain next-or-last (L1053-1055) | ✓ |
| FN-22 | ตีกลับ + เหตุผลบังคับ → ร่าง | `openReject`→reason (L1055) BR-11 | ✓ |
| FN-23 | "ผ่านรายการ" เฉพาะ อนุมัติแล้ว | ปุ่ม post เฉพาะ `st==='approved'` (L730,1000) BR-08 | ✓ |
| FN-24 | ยกเลิกเฉพาะ ร่าง/รออนุมัติ · **อนุมัติแล้ว ไม่มีปุ่มยกเลิก** | row-acts draft/pending only · `openCancel` guard `!['draft','pending'].includes(status)` (L730,1110) · FIX-02 | ✓ |
| FN-25 | posted ไม่มียกเลิก มีแต่ กลับรายการ | posted → กลับรายการ เท่านั้น (L731 area) | ✓ |
| FN-26 | list กรองครบ 6 สถานะ | status select 6 ค่า (L680) | ✓ |
| FN-27 | ยอดเปลี่ยน → เตือน 2 ยอดก่อน post | recheck modal 2 ยอด (L1127-1128) + `doPost(id,useLatest)` (L1137) BR-15 | ✓ |
| FN-28 | tab ลายเซ็น การ์ดผู้อนุมัติจริง | sign timeline `empChip` avatar+ชื่อ+ตำแหน่ง (L1053) | ✓ |
| FN-29 | tab ประวัติ movement + คู่ reversal 2 ทาง | movement table + linkDoc ผูกคู่ 2 ทาง (L1060) BR-16/18 | ✓ |
| FN-30 | หลัง post ป้าย รอลงบัญชี + FWD-WIRE JE · ไม่มีปุ่มลงบัญชีจริง | `je:'รอลงบัญชี'` pill + `FWD-WIRE: JE posting` (L1033,1060) BR-19 | ✓ |
| FN-31 | สินค้า archive → ใบเดิมยังแสดง ไม่พัง | soft-ref `ITEM_BY` fallback text (BR-22) | ✓ |
| FN-32 | ค้น in-transit TR-* → ไม่เจอเลย | filter `b.type!=='in-transit'` (L946) + TR-* empty msg (L965) BR-13 | ✓ (neg) |
| FN-33 | แนบไฟล์ → โผล่ landing เอกสารแนบ | attach handler + landing attach section (L847 step3) | ✓ |
| FN-34 | tab PDF A4 ครบ + พิมพ์ได้ | tab `pdf` A4 preview + print | ✓ |
| FN-35 | ทั้งระบบไม่มี ใบนับ/นับรอบ/cycle count/count sheet (หน้า/ปุ่ม/คำ UI) | ไม่มี screen/ปุ่มนับ · "cycle count" อยู่แค่ JS comment อ้าง contract F086 (L457 · ไม่ render) · preflight note (L1156) | ✓ (neg) |
| FN-36 | ไม่มี bin ปลายทาง + microcopy ชี้ Transfer | ไม่มีช่อง bin ปลายทาง · ค้น "ย้าย"→Transfer microcopy BR-05 | ✓ (neg) |
| FN-37 | dropdown เหตุผลกรองตามทิศ | `line-reason-*` filter by dir (L942) + BR-07 guard (L904) | ✓ |
| FN-38 | ทุกวันที่ ปี ค.ศ. ไม่มี พ.ศ. | `fmtDate`/`fmtDateTime` ค.ศ. · Buddhist-year=0 (L1157) | ✓ |
| FN-39 | audit append-only ทุก event | `d.audit.push` ทุก action (L1110,1137 ฯลฯ) history tab (L1059) | ✓ |
| FN-40 | เหตุผล "อื่น ๆ" → บังคับคำอธิบายเพิ่ม | `RS-99` needNote:true (L428) · `r.needNote&&!reasonNote` guard (L904) BR-06 | ✓ |
| FN-41 | เหตุผลรวมหัวใบ → เติมบรรทัดว่าง แก้รายบรรทัดได้ | header-reason fill-empty (L847) | ✓ |
| FN-42 | ไม่มี role ID ลอย ๆ แทนคน | slot=คนจริง `empChip` · microcopy "ห้ามใช้ role ID" (L1075) BR-10 [STD] | ✓ (neg) |
| FN-43 | ใบผสม สุทธิ≈0 ยังอนุมัติตามค่าสัมบูรณ์ | DOA base = `abs` (Σ\|มูลค่า\|) (L1033) BR-09 | ✓ |
| FN-44 | กลับรายการซ้ำไม่ได้ | reversal `isReversal`/`reversalOf` · ปุ่มหายหลัง revers (L512,701,1030) BR-18 | ✓ |
| FN-45 | ไม่มีปุ่มลบ/แก้ movement | movement table label "append-only · ไม่มีปุ่มลบ/แก้" (L1060) BR-16 | ✓ (neg) |
| FN-46 | quarantine ปรับได้แต่ย้ายออก storage ไม่ได้ | binTypes filter คุมประเภท (L946) · ไม่มีช่องปลายทาง BR-12 | ✓ (neg) |
| FN-47 | ไม่มีช่องกรอกเลขเอง / ตั้งเลขรัน | เลขจาก ENG-DOC-NUM/DOCCFG (L570) · ไม่มี input เลข OB-8 | ✓ (neg) |
| FN-48 | ไม่มีช่อง threshold/% เตือน | ไม่มี input threshold (อยู่ NC rules) BR-20 | ✓ (neg) |
| FN-49 | ไม่มีคอลัมน์ VAT/ส่วนลด | grid "no VAT col" (L176) · VAT identities tax-inert compat shim เท่านั้น (L434-443) · removed (L1156) | ✓ (neg) |
| FN-50 | sidebar Warehouse ตาม module map | Iron #104 one-feature-one-menu (L1156) · sidebar map (L605) | ✓ |
| FN-51 | ตัดจำหน่ายของเสีย ยังไม่แนบ → ส่งไม่ได้ | needAttach && !attachments guard (L905) BR-23 | ✓ |
| **FN-52 ★** | แหล่งที่มา จากใบนับ → บังคับ ref_count_doc · view โชว์ ใบนับต้นเรื่อง trace · ปรับตรง ไม่บังคับ · ไม่เปิดหน้าใบนับ | source segmented `f-source`/`setAdjSource` (L790,800) · combo `wiz-countdoc` (L974) · **BR-26 guards L898 + L916** · view ref row display-only "แสดงผล ไม่เปิดหน้าใบนับ" (L1032) · seed d3 source:count+ref_count_doc (L471) | ✓ **FULLY HOOKED** |
| FN-90 | ค้นหา/filter list + empty state | search (L677) + filters + empty state | ✓ |
| FN-91 | ยกเลิก/กลับรายการ ผ่าน confirm · ไม่มี hard delete | `reasonModal` ทุก destructive · append-only | ✓ |
| FN-92 | field validate ก่อนบันทึก + กัน double-submit | `wizardNext` validate + double-submit guard | ✓ |

---

## 3. Scenario Coverage (S-01..S-26)

ทุก S เดินจากทางเข้าจนจบผลลัพธ์ทางธุรกิจได้ใน UI. Highlights:
- **S-04/S-05** (exception): บล็อก inline ที่ step 2 (L901) · **S-13** slot ว่าง = บล็อก (L916)
- **S-08** ตีกลับ→ร่าง (L1055) · **S-09** ยกเลิกเฉพาะ ร่าง/รออนุมัติ (FIX-02 · L1110)
- **S-10** reversal คู่ movement + ผูกคู่ 2 ทาง (L512,1030,1060)
- **S-15** ตรวจยอดซ้ำก่อน post 2 ยอด (L1127) · **S-17** post → movement + FWD-WIRE JE (L1137)
- **S-18** quarantine ปรับได้ย้ายไม่ได้ · **S-19** damage ตัดจำหน่าย + บังคับแนบ (L905)
- **S-20** in-transit ไม่โผล่ (neg · L946) · **S-23** 1 ใบ 1 คลัง · **S-24/S-25** neg (no count / no move)
- **S-26 ★** จากใบนับ ref trace display-only (FN-52 · BR-26) — **ครอบครบ**

---

## 4. Business Rules (BR-01..BR-27) — ครบ

ทุก BR มี hook ใน HTML. จุดตรวจสำคัญ:
- **BR-26** = enforce 2 จุด (ดู §1 · L898 + L916) ✓ · **BR-27** = ยกเลิกเฉพาะ ร่าง/รออนุมัติ (FIX-02 · L730,1110) ✓
- BR-08 (no shortcut post) L730/1000 · BR-09 (Σ\|มูลค่า\| base) L1033 · BR-10 (คนจริง) L916/1075 · BR-15 (recheck) L1127 · BR-16/17/18 (append-only reversal) L1060 · BR-19 (JE mock) L1033/1060 · BR-23 (บังคับแนบ) L905

---

## 5. Declaration Coverage (Phase 0b) — 5/5 ตรง chip · ไม่มี DIVERGENCE

chip = `dec:[doa, ntf, csq, doccfg, pdfdoc]` · parser detect = doa/ntf/csq/doccfg (pdfdoc = print tab ไม่ใช่ declaration-signal)

| ท่อ | เข้าเงื่อนไข | Brief | HTML signal | ผล |
|---|---|---|---|---|
| DOA | ✅ (ส่งอนุมัติ/pending) | `5_DECLARATIONS/DOA_BRIEF_F-WH-STKADJ.md` | slot picker คนจริง · `FWD-WIRE: DOA engine` · "ห้ามใช้ role ID" · ไม่ hardcode chain (L1054,1075) | ✓ |
| NTF | ✅ (ส่งอนุมัติ/post/reversal) | `NTF_BRIEF_F-WH-STKADJ.md` | comment `NTF_BRIEF_F082` map event · `doa_pending` ไม่ประกาศซ้ำ (L1077,1083,1095,1109,1117,1134) | ✓ |
| CSQ | ✅ (มูลค่า/บัญชี) | `CSQ_BRIEF_F-WH-STKADJ.md` | `บันทึกเข้า 7C (CSQ_BRIEF_F082)` VC หลัก · OC/DC ไม่ประกาศซ้ำ (L1120,1133,1137) | ✓ |
| DOCCFG | ✅ (เลขรัน ADJ-YYYY-NNNN) | `DOCCFG_BRIEF_F-WH-STKADJ.md` | เลขจาก ENG-DOC-NUM ตาม DOCCFG (L570) · ไม่ hardcode รูปแบบเลข | ✓ |
| pdfdoc | ✅ (เอกสาร A4) | `print-spec-adj.md` | tab PDF A4 + ช่องเซ็นตาม DOA + print | ✓ |

**ผล: chip = detect → ไม่มี DIVERGENCE.**

---

## 6. Pattern Q Surface Coverage (Phase 0c) — ครบ

| Surface | Evidence | ผล |
|---|---|---|
| List | KPI แถบบน (L671) · filter (คลัง/สถานะ 6/ประเภท/วันที่/ผู้จัดทำ · L680) · `docPill` 6 สถานะ · เอกสารแนบ landing | ✓ |
| Wizard 5 steps | step1 ข้อมูล+แหล่งที่มา (L790) · step2 B2 v2 grid · step3 เหตุผล+หลักฐาน (L847) · step4 DOA slot (L1075) · step5 review/submit (L881) | ✓ |
| View 4 tabs | รายละเอียด · PDF · ลายเซ็น · ประวัติ | ✓ |
| PDF | A4 preview + ช่องเซ็นตาม DOA + พิมพ์ | ✓ |
| Modals | reason modals ทุก transition (ตีกลับ/ยกเลิก/กลับรายการ) + post recheck (L1110,1127) | ✓ |

---

## 7. Scope Creep = 0

Negatives ยังยืนครบ: FN-32 (in-transit), FN-35 (no cycle count screen/word ใน UI), FN-36 (no bin ปลายทาง), FN-45 (no movement delete), FN-46 (quarantine no move-out), FN-47/48/49 (no doc-num/threshold/VAT input).

> **นัยสำคัญ FN-52 vs FN-35:** การอ้าง "ใบนับต้นเรื่อง" (display-only ref, `ref_count_doc`, ไม่เปิดหน้าใบนับ) เป็นของที่ **BA re-gate อนุญาตโดยเจตนา** (S-26/FN-52/FIX-04) — ไม่ใช่ scope creep และไม่ขัด FN-35 ซึ่งห้าม *ฟังก์ชัน/หน้าจอ/ปุ่มนับสต๊อก* (count sheet/blind count/นับรอบ). ทั้งสองอยู่ร่วมกันได้ตามสัญญา. คำ "cycle count" ที่เจอใน HTML อยู่ใน JS comment อ้าง contract F086 (L457) — ไม่ render.

---

## 8. Gap List

| ลำดับ | Gap | ระดับ | ที่ต้องแก้ |
|---|---|---|---|
| (none) | — ไม่มี blocking gap — | — | — |
| G-w1 | Preflight HTML comment (L1154) เขียน "FN wired: 54/54" — stale (นับก่อนรวม FN-52) · comment z-scale (L1155) ยังไม่กล่าว `--z-combopop:75` | **WARN cosmetic** | อัปเดต comment เป็น 55/55 + note combopop ตอนแตะ HTML รอบหน้า (ถ้าแตะ .html ต้องวน step 3·4·5 ตาม C3.2) — comment ไม่ render ไม่ใช่ gate |

> เดิม WARN `markErr('f-countdoc')` (id ไม่มีจริง) — **RESOLVED** ในไบต์ปัจจุบัน: L898 ใช้ `markErr('f-source')` ที่ตรงกับ id จริง (L790) · `f-countdoc` grep = 0. เหลือเพียง comment count ที่ยัง stale — cosmetic ล้วน **ไม่กระทบ verdict PASS**.

---

## 9. Diff กับรอบก่อน (ที่ BLOCK)

| รายการ | รอบก่อน | รอบนี้ (final bytes) |
|---|---|---|
| BR-26 enforce | ❌ ไม่มีใน HTML (= BLOCK) | ✅ enforce 2 guard (L898 + L916) |
| FN-52 | บางส่วน (ยังไม่บังคับเลือก) | ✅ FULLY HOOKED |
| `markErr` target | `f-countdoc` (id ไม่มีจริง · WARN) | ✅ `f-source` (id จริง · WARN cleared) |
| UI: scroll-lock / combobox z | — | ✅ trap-stack balanced (L314-333) · `--z-combopop:75` เหนือ modal (L34,188) |
| Verdict | **BLOCK** | **PASS** |

**Prior BLOCK RESOLVED. พร้อมไปต่อ (e2e สดแล้ว 55/55 FN · 58/58 cases) แล้ว pack ส่ง dev.**
