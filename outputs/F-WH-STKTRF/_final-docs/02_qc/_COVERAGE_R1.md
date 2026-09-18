# Coverage Report — F-WH-STKTRF (รอบ 1: HTML)

- วันที่: 2026-09-16 · node: `F083 Stock Transfer` · wave: W3 · archetype: Q-document
- Source of truth ตามผู้ใช้: `Pack Brief Feature/F-WH-STKTRF_Stock Transfer` + ทุกไฟล์ใน `Cube_Feature_List`
- Artifacts ที่ตรวจ: `F-WH-STKTRF.html` · PREBRIEF · Function Checklist · Cube Feature List
- Contract: FN 61 · edges ธุรกิจ 3 · engine hooks 4 · scope guard 13 กลุ่ม

## Verdict: 🟢 PASS

สรุป: **FN 61/61 · edges 7/7 · scope creep 0 · BLOCK 0 · WARN 0**  
Runtime proof (PM/BA re-gate 2026-09-17): **E2E 19/19 · console error 0** · `FN-40` ผ่านแบบ rendered negative case · FIX-01–FIX-06/FIX-08 ผ่านครบ (receive guard, reversal DOA, shortage approval chain, anchors, busy lock, demo-only)

## Dependency / edge matrix

| Item | ประเภท | HTML | Evidence |
|---|---|:---:|---|
| F008 → F083 คลังต้นทาง/ปลายทาง + location | edge in / data | ✓ | Warehouse/bin master + picker `comboItems()`; locked/quarantine/damage/staging/in-transit guards |
| F083 → F009 ย้ายยอดระหว่างคลัง/สาขา | edge out / post | ✓ | `doShip()` · `confirmReceive()` · `confirmShortage()` + movement/audit timeline |
| F083 → F070 ต้นทุนเคลื่อนตามการย้าย | edge out / post | ✓ | `calcLineVat()`/`totals()` ใช้ต้นทุนอ้างอิงและแสดง `FWD-WIRE: JE posting` โดยไม่มีปุ่ม post จริง |
| F019 / DOA → F083 | engine / approval | ✓ | `resolveDoa()` · real-person slot · sign tab แยก 2 decision points |
| F003 / DOCCFG → F083 | engine / document | ✓ | ออกเลขตอนส่งอนุมัติ · draft ไม่มีเลข · `ENG-DOC-NUM` forward wire |
| F083 → F004 / Notification | engine / event | ✓ | audit/transition มี notification forward wire; ไม่ hardcode channel |
| F083 → F054 / CSQ | engine / event | ✓ | transition และ movement append-only เป็นจุด emit; ไม่มี UI carbon logic เพิ่มเอง |

## FN coverage matrix

| Item | HTML | Evidence / rendered proof |
|---|:---:|---|
| FN-01 | ✓ | wizard 5 ขั้นเปิดได้; warehouse picker ใน step 2 |
| FN-02 | ✓ | route chip “ภายในคลัง — ย้ายจบในจังหวะเดียว” derive จากคลังเท่ากัน |
| FN-03 | ✓ | route chip “ข้ามคลัง/สาขา — ต้องมีขั้นยืนยันรับที่ปลายทาง” |
| FN-04 | ✓ | warehouse อยู่หัวใบเท่านั้น; line editor มีเฉพาะ bin |
| FN-05 | ✓ | `TR-BKK-CNX` แสดงแบบ read-only จาก `transitBinFor()` |
| FN-06 | ✓ | step 3 block จำนวนเกิน on-hand พร้อมเพดาน |
| FN-07 | ✓ | step 3 block qty ≤ 0 |
| FN-08 | ✓ | same-bin warning + block ก่อนผ่าน step |
| FN-09 | ✓ | `changeWarehouse()` ใช้ native confirm ก่อนล้าง lines และแจ้งเปลี่ยน mode |
| FN-10 | ✓ | draft แสดง “(ร่าง — ยังไม่ออกเลขที่)” |
| FN-11 | ✓ | `nextCode()` ถูกเรียกเมื่อ confirm submit; รูปแบบ `TRF-YYYY-NNNN` |
| FN-12 | ✓ | `renderLineSummary()` แสดงจำนวนบรรทัด/จำนวนรวม/มูลค่ารวม |
| FN-13 | ✓ | `doShip()` intra ปิดเป็น `moved` ในครั้งเดียว; E2E INTRA |
| FN-14 | ✓ | inter เปลี่ยนเป็น `in_transit`; ปลายทางยังไม่ขยับ |
| FN-15 | ✓ | locked bin ยังพบใน picker แต่ disabled พร้อม lock reason |
| FN-16 | ✓ | source quarantine จำกัด destination quarantine |
| FN-17 | ✓ | damage ถูกตัดออกจาก source/destination picker |
| FN-18 | ✓ | staging ถูกตัดออก; note ชี้ flow ที่ถูกต้องใน contract |
| FN-19 | ✓ | ค้น `TR-*` ใน picker ได้ empty list |
| FN-20 | ✓ | detail note + transit tab แสดงคงค้างและ route 2 ขา |
| FN-21 | ✓ | source warehouse ถูก block; destination warehouse เปิด receive ได้ |
| FN-22 | ✓ | seed `d1` รับครบ: `closed`, in-transit = 0 |
| FN-23 | ✓ | partial receive + wait คงสถานะ `partial` และรับต่อได้ |
| FN-24 | ✓ | modal แสดง 3 ทาง: wait / write-off / return |
| FN-25 | ✓ | shortage modal บังคับ reason + evidence + DOA slots + real person |
| FN-26 | ✓ | `d4` closed_diff, write-off amount > 0, transit = 0 |
| FN-27 | ✓ | `d5` returned กลับ bin เดิมและไม่เข้า shortage DOA |
| FN-28 | ✓ | over-receive block พร้อมชี้ Stock Adjustment |
| FN-29 | ✓ | `doShip()` recheck on-hand ก่อน movement |
| FN-30 | ✓ | submit modal person combobox มี avatar/ชื่อ/ตำแหน่ง; slot ว่าง submit ไม่ได้ |
| FN-31 | ✓ | reject reason required; กลับ draft และคงเลขเดิม |
| FN-32 | ✓ | cancel เฉพาะ draft/pending/approved + reason modal; record ไม่ถูกลบ |
| FN-33 | ✓ | หลังส่งออกไม่มีปุ่ม cancel; เหลือ return/reversal |
| FN-34 | ✓ | reversal สร้าง movement ทิศตรงข้ามและผูกใบคู่ |
| FN-35 | ✓ | reversed record ไม่มีปุ่ม reverse ซ้ำ |
| FN-36 | ✓ | หลัง submit view read-only; ไม่มีปุ่มลบ movement |
| FN-37 | ✓ | history แสดง `FWD-WIRE: JE posting`; ไม่มีปุ่ม post จริง |
| FN-38 | ✓ | ไม่มี field ปรับยอด; note ชี้ Stock Adjustment |
| FN-39 | ✓ | ไม่มีหน้าจอ count sheet/cycle count/blind count |
| FN-40 | ✓ | **rendered negative:** คู่คลัง `WH-NO-TR` ถูก block และ toast ชี้ผู้ดูแลผัง |
| FN-41 | ✓ | `isAging()` อ่าน `CFG.transitAgingDays`; badge แสดงตาม NC rule config |
| FN-42 | ✓ | review/sign แสดงมูลค่า+mode ที่ส่ง DOA; feature ไม่ให้แก้ tier |
| FN-43 | ✓ | KPI 4 ใบคลิก filter ได้และค่าคำนวณจาก DOCS |
| FN-44 | ✓ | line grid ไม่มี sales price/Lot/Serial; scan placeholder อยู่ |
| FN-45 | ✓ | detail/transit/receive surfaces แสดงคงค้างก่อนรับ |
| FN-46 | ✓ | transit tab แสดง invariant; seed diff/return ลงท้าย transit = 0 |
| FN-47 | ✓ | sign tab แยก approval การย้ายและ shortage chain |
| FN-48 | ✓ | history timeline append-only แสดง route/movement/reversal |
| FN-49 | ✓ | ไม่มี create/edit location/bin affordance |
| FN-50 | ✓ | ไม่มี freight/carrier/tracking/pick-list field |
| FN-51 | ✓ | tabs “รอฉันรับ” และ “อยู่ระหว่างทาง” ทำงานจริง |
| FN-52 | ✓ | filter grid: search (รวมผู้จัดทำ) + from/to + mode + status + date range + reason; ตารางแสดงผู้จัดทำและเหตุผลย้ายให้ตรวจผลได้ |
| FN-53 | ✓ | landing มี “เอกสารแนบล่าสุด” + filter ตามใบ; wizard step 4 ใช้ file input/drag-and-drop จริงและ reject ชนิดไฟล์นอก PDF/JPG/PNG |
| FN-54 | ✓ | PDF preview มี number/route/mode/lines/totals/DOA/ผู้รับปลายทาง |
| FN-90 | ✓ | search/filter ทำงาน + actionable empty state |
| FN-91 | ✓ | destructive actions ใช้ confirm/reason modal และ danger action |
| FN-92 | ✓ | soft-ref snapshot semantics; record ยัง render แม้ master ref เปลี่ยน |
| FN-93 | ✓ | validation ทุก step + submit button disabled ระหว่าง action/timer guard |
| FN-94 | ✓ | create/edit/submit/approve/reject/ship/receive/diff/return/reverse append audit |
| FN-95 | ✓ | UI/PDF ใช้ปี ค.ศ.; E2E ไม่พบ `2569` ใน view |
| FN-96 | ✓ | CUBE Warm Light · Satoshi/Noto Thai · Lucide/local SVG fallback · Warehouse sidebar |

## Scope guard

ไม่พบ UI สำหรับ Stock Adjustment, cycle count, location configuration, manual in-transit selection, post JE จริง, Lot/Serial, RF/pick wave, carrier/tracking, intercompany pricing หรือ destination QC. เส้นทางที่ต้องพึ่ง feature อื่นใช้ข้อความชี้ทาง/forward wire ตาม pack โดยไม่แก้ feature อื่น

## Fresh-gate fixes

1. จัด landing filter เป็น grid ที่สมมาตร; รวมผู้จัดทำไว้ใน search และเพิ่มคอลัมน์ผู้จัดทำ/เหตุผลย้าย
2. จัด line editor ด้วย fixed colgroup ให้หัวตารางและ control ตรงแนว
3. เปลี่ยน wizard step 4 เป็น upload file จริง พร้อม drag-and-drop และ validation ชนิดไฟล์
4. คง attachment landing + filter ตามใบตาม FN-53 และเพิ่ม local SVG icon fallback

ไม่มี unresolved coverage gap ในรอบ 1
