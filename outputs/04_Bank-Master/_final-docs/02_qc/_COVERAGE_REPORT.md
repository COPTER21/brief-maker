# Coverage Report — F-BNK Bank Master (Reverse Mode · รอบ 1: HTML vs Contract)

- วันที่ 2026-08-11 · feature F-0.21 Bank Master · **Reverse Mode**: HTML = source of truth, ต้องครอบ PREBRIEF (OB/BR/S) + FUNCTION_CHECKLIST
- Artifact ที่ตรวจ: `outputs/04_Bank-Master/01_HTML/f-bank.html` (1061 บรรทัด, single-file SPA)
- Contract sources: `PREBRIEF_F-BNK_Bank-Master.md` (OB-1..7, BR-01..07, S-01..10, OQ-BNK-01..05) · `FUNCTION_CHECKLIST_F-BNK_Bank-Master.md` (FN-01..25, FN-90, FN-40)
- Checklist size: fields 11 · actions 10 · statuses 3 · IR/guard rules 4 · scope-guard (ห้ามมี) 8

> หมายเหตุขอบเขต: skill นี้ตรวจ **ความครบเชิง business scope** เท่านั้น — iron rules / CI / UX polish เป็นงาน `qc-ux-html-checker` (ไม่ตัดสินที่นี่). ไม่มี FRD Pack + testcases แนบ → รอบ 2 (FRD+TC) = NOT-CHECKED ทั้งหมด (feature ยังไม่ gen FRD ต่อ OQ-BNK-05).

## Verdict: 🟢 PASS — COMPLETE

สรุป: ครอบ **36/36** contract item · gap block 0 · gap warn 0 · over-build 0 · out-of-scope leak 0 · NOT-CHECKED = รอบ 2 (FRD/TC ยังไม่มีไฟล์)

---

## Coverage Matrix — Fields (11)

| Field | ประเภท | HTML | Evidence |
|---|---|---|---|
| code (auto ได้) | field | ✓ | `#fld-code` L631-635 · `autoCode()` L768 `{bank}-{run}` · uppercase + dup check L737-739 |
| ธนาคาร (9 ค่า) | field | ✓ | `BANKS[]` L365-375 (9 ค่า) · `#in-bank` L636-639 |
| ชื่อบัญชี | field | ✓ | `#fld-acct-name` L645-649 · required validate L735 |
| เลขที่บัญชี | field | ✓ | `#fld-acct-no` L640-644 · 10–12 หลัก + ตัดขีด L740-741 |
| ประเภทบัญชี (3 ค่า) | field | ✓ | `ACCT_TYPES[]` L377-381 · `#in-acct-type` L654-657 |
| สาขา | field | ✓ | `#in-branch` L650-653 |
| พร้อมเพย์ | field | ✓ | `#fld-promptpay` L658-662 · validate ว่าง/10/13 L744-745 |
| GL Posting Group (soft-ref kind=bank) | field | ✓ | `BANK_POSTING_GROUPS[]` L385-388 · `#in-posting-group` L665-671 · comment kind=bank + generic F-PG-API-01 L383-384 |
| side รับ/จ่าย/รับ+จ่าย | field | ✓ | `use_receive`/`use_pay` chk L681-688 · `useText()` L396 |
| pre-select ★ (default) | field | ✓ | `default_receive`/`default_pay` L689-696 · radio-unset L754-755 · ตาราง ★รับ/★จ่าย L490 |
| สถานะ (3 ค่า อิสระ) | field | ✓ | `#in-status` L697-704 · `statusLabel()` L393 |

## Coverage Matrix — Actions (10)

| Action | HTML | Evidence |
|---|---|---|
| create | ✓ | `openCreate()` L714 · `saveBank('create')` L717 · toast L764 |
| edit | ✓ | `openEdit()` L715 · row pencil L498 · view header L832 |
| view | ✓ | `openView()` L771 · row click L488 · summary chips + 3 sections L788-820 |
| delete (confirm modal) | ✓ | bulk delete `openBulkDelete()` L983 → confirm modal L987-996 → `confirmBulkDelete()` L998 · **ไม่มีลบเดี่ยว = by design** (FN-40) |
| CSV import | ✓ | `bulkImport()` L897 · 3 จังหวะ pick→preview→done L935-962 · merge-only |
| CSV export | ✓ | `exportCSV()` L1006-1014 · ตาม filter · BOM · `bank_export_YYYY-MM-DD.csv` |
| search | ✓ | `onSearch()` L578 · ค้น รหัส/ธนาคาร/สาขา/เลขบัญชี/ชื่อ L428 |
| filter (bank + status) | ✓ | `onFilter()` L579 · bank select L552 · status select L553-558 · stat quickFilter L580 |
| sort | ✓ | `sortBy()` L586 · sortable th L483-486 |
| pagination | ✓ | `renderPager()` L566 · pageSize 8 L403 · `goToPage()` L587 |

## Coverage Matrix — Statuses + Rules/Guards (7)

| Item | ประเภท | HTML | Evidence |
|---|---|---|---|
| active / inactive / draft | status | ✓ | `statusLabel()` L393 · pills `.is-active/.is-inactive/.is-draft` L169-171 |
| BR-03 ★ radio 1/ฝั่ง + DEFAULT_GUARD (active+ฝั่งเปิด) | rule | ✓ | guard toast L747-748 · radio unset others L754-755 |
| BR-03 side-effect: หลุด active → ★ หลุด | rule | ✓ | `setStatus()` L972 · `bulkSetStatus()` L980 (`if(st!=='active') default_*=false`) |
| **IR-BNK-01** used>0 ล็อก ธนาคาร+เลขบัญชี (partial) | rule (block) | ✓ | `locked` L609 · disabled L638,642 · lock-tag L610 · **logic guard** L758 (`if(!locked) set bank/acct`) · field อื่นแก้ได้ |
| **IR-BNK-01** delete blocked เมื่อ used>0 | rule (block) | ✓ | นับ used L985 · modal เตือนข้าม L991 · `confirmBulkDelete` skip used>0 L1001 |
| BR-04 GL picker = active-only + คงตัว draft ที่ผูกอยู่ | rule | ✓ | `pgOpts` L614 `filter(status==='active' \|\| code===r.posting_group)` — SCB(draft) โผล่ก็ต่อเมื่อ record ผูกไว้เดิม |
| BR-04 view เตือน "ยังไม่ผูก — GL post ไม่ได้" | rule | ✓ | view GL section L810 · chip "ยังไม่ผูก" L793 |

## Coverage Matrix — Scope Guard (ต้อง **ไม่มี** — 8)

| ห้ามมี (FN-40 / S-10 / OB) | ผล | Evidence |
|---|---|---|
| Payment Method integration (OQ-BNK-01 = ตัด) | ✓ ไม่มี | ไม่มี hook/field/endpoint ไป PM · sidebar "วิธีชำระเงิน" = `is-disabled` shell chrome เท่านั้น L308 |
| DOA / สายอนุมัติ (placeholder only) | ✓ ไม่มี | `approver_role/approved_by/approved_at/approval_chain=null` L412+ · ไม่มี UI อนุมัติ · comment DOA-ENGINE placeholder L410 |
| dedicated Bank-Master GL endpoint | ✓ ไม่มี | comment ยืนยัน generic `F-PG-API-01` `GET /api/v1/gl/posting-groups?kind=bank&status=active` L383 |
| ยอดคงเหลือ / opening balance | ✓ ไม่มี | grep opening/balance/ยอดคงเหลือ = 0 hit |
| สกุลเงินอื่น / SWIFT / IBAN | ✓ ไม่มี | THB disabled L674 · grep swift/iban = 0 hit |
| จำนวน used บนจอ | ✓ ไม่มี | `used` ปรากฏเฉพาะ logic (lock/guard/delete-skip count) — ไม่แสดงเลข used รายบัญชีบน list/view |
| ลบเดี่ยว / Replace-import / posting_group·promptpay ในไฟล์นำเข้า | ✓ ไม่มี | row action มีแค่ pencil L497-499 · import ไม่มี mode selector L935-940 · template 8 คอลัมน์ไม่มี pg/promptpay L887 |
| ★ หลายตัวต่อฝั่ง / ผู้มีอำนาจเซ็น·วงเงิน / hint text | ✓ ไม่มี | ★ radio unset L754-755 · ไม่มี field วงเงิน/ผู้เซ็น · create form ไม่มี `.hint` ใต้ช่อง |

## Coverage Matrix — Function Checklist (FN-01..25, FN-90) spot-map

ทุก FN มี evidence — ไม่มี ✗ · highlights:
FN-01 3 sections L628/665/678 · FN-02 auto code L768 · FN-05 THB disabled L674 · FN-06 DOA null+used=0 L763 · FN-07..09 ★/guard/side-effect L747-755,972,980 · FN-10/11 IR lock UI+logic L610,758 · FN-12/13 validate L735-746 · FN-14 status menu current disabled L836 · FN-15 bulk bar + select-all thead L502-511 · FN-16 stat/filter/search/sort/pager ร่วม · FN-18..21 import 3 จังหวะ + IN_FILE_DUPLICATE L902-906 + สรุปข้าม+สาเหตุ L955-962 · FN-22 export roundtrip · FN-23 title mask + 4 chips L828,789 · FN-24 GL warn L810 · FN-25 #96/#29/#97/Esc chain L91-92,442,95-102,1048-1054 · FN-90 delete ผ่าน confirm เสมอ L987.

---

## 🔴 Gaps
ไม่มี — block/warn rule และ contract field/action ครอบครบทุกข้อในรอบ 1 (HTML).

## 🟡 Warnings / Scope Creep
ไม่มี scope creep เชิง business. พบเฉพาะ **copy-paste chrome leftover** (cosmetic — เป็นงาน qc-ux ไม่กระทบ coverage verdict):
- Notif menu ยังเป็นข้อความจาก template เดิม ("มีรหัสภาษีใหม่…", "ลิตร ถูกหยุดใช้งาน") L333-334
- Sidebar/breadcrumb `navTo('units')` ยังใช้ route `units` จาก template Unit Master L307,327
> ทั้งสองไม่ใช่ field/action/flow ของ Bank Master — ไม่นับเป็น over-build. แจ้งให้ qc-ux เก็บ.

## ⬜ NOT-CHECKED (รอบ 2 — FRD + Test cases)
- Golden rules ↔ FRD 05_RULES · edges ↔ FRD API/LOGIC · block rule/exception path ↔ TC — **ยังตรวจไม่ได้**: feature ยังไม่มี FRD Pack + testcases (OQ-BNK-05 = พร้อม gen FRD แต่ยังไม่ได้ gen). รันรอบ 2 หลัง frd-generator-v6 + ai-testcase-md-generator เสร็จ.

## 💡 เสนอเข้า contract
ไม่มี — PREBRIEF + FUNCTION_CHECKLIST ครอบเพียงพอ, ไม่พบ standard flow ที่ contract ขาด.
