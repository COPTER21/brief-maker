# COVERAGE CHECK — ROUND 1 · F-WH-DN Delivery Note

**Verdict: PASS** · FN ครบ **34/34** · business edges ครบ **7/7** · scope creep **0**  
ตรวจจาก HTML จริงเทียบ PREBRIEF, Function Checklist, Central Plan และ locked artifacts ของ Picking/Packing ไม่ใช้ข้อความ pass ที่ฝังใน seed เป็นหลักฐาน

## 1. Function coverage

| FN | UI / function evidence ใน `f-wh-delivery-note.html` | ผล |
|---|---|---:|
| FN-01 | `dnJobs`, `queueRows`, queue table | ✓ |
| FN-02 | `openPackModal` แสดงกล่อง/สินค้า | ✓ |
| FN-03 | multi-select key = source type + customer + ship-to; checkbox lock และ confirm guard | ✓ |
| FN-04 | `openCreateConfirm`, `paintCreateConfirm`; cancel ไม่ mutate | ✓ |
| FN-05 | confirm fields: assignee/carrier/vehicle/tracking/date/slot + overload/late warning | ✓ |
| FN-06 | `shipTab` แบ่ง recipient, schedule/owner และ carrier | ✓ |
| FN-07 | `assigneeCombo`, `cbOpen`, `cbKey`, workload badge | ✓ |
| FN-08 | `markReady`, `markErr`, toast validation | ✓ |
| FN-09 | carrier/vehicle/driver selectors พร้อม capacity metadata | ✓ |
| FN-10 | 3PL tracking/drop point; `dispatch` block tracking ว่าง | ✓ |
| FN-11 | pickup จาก `refInfo` → carrier `PICKUP`; ไม่บังคับรถ/คนขับ | ✓ |
| FN-12 | `openDispatchModal` สรุป + GI warning + ปุ่มพิมพ์ | ✓ |
| FN-13 | `dispatch` → `postGoodsIssue`, movement `issue`, SO issued/reserved, audit/notify note | ✓ |
| FN-14 | `TRACK_STAGES`, `nextTrackStage`, tracking timeline/action | ✓ |
| FN-15 | `openPodModal`, `paintPod`, `paintPodFoot`, required recipient | ✓ |
| FN-16 | `mockSign`, `mockPhoto`, remove controls, max 4 photos | ✓ |
| FN-17 | `confirmPod` partial → `return_in`, accepted/rejected and SO counters | ✓ |
| FN-18 | delivered/partial header action “ส่งต่อวางบิล” | ✓ |
| FN-19 | `openFailModal`, 6 reasons, attempt log, no reverse GI | ✓ |
| FN-20 | attempts/history + `reschedule`; `DNCFG.maxAttempts=3` warning | ✓ |
| FN-21 | `openReturnAllModal` → reverse GI, returned, pack queue, RTN audit | ✓ |
| FN-22 | `askBackorder`, `decideBackorder` (backorder/close short) | ✓ |
| FN-23 | `openCancelModal`; conditional reverse GI + pack/SO sync | ✓ |
| FN-24 | `syncSoStatus` และ Document Flow ต่อ SO ใน `shipTab` | ✓ |
| FN-25 | `itemsTab` รายการรวม + lot/expiry/location/boxes/result | ✓ |
| FN-26 | `shipTab` edit เฉพาะ draft; `backToDraft` เฉพาะ ready action | ✓ |
| FN-27 | `docTab` A4 preview/check-result/4 conditions/4 signatures + `06_PRINT` deliverables | ✓ |
| FN-28 | completed Transfer → PACK-2026-0460 → TR-2026-0012 queue; `refInfo` แสดง WH-01→WH-02 และไม่มี SO sync | ✓ |
| FN-90 | `dnStepper` 4 ขั้น + success/current/error state | ✓ |
| FN-91 | `dnRows`, filters, mine, carrier, late, attempts, POD, `exportCSV` | ✓ |
| FN-92 | 4 tabs, state actions, document Escape chain | ✓ |
| FN-93 | `canManage`, `canDrive`, persona switch และ terminal-state action lock | ✓ |
| FN-94 | `pushAuditD` prepend-only และทุก transition เรียก audit | ✓ |
| FN-95 | ภาพ 1440/1000 ผ่าน; responsive rules เดิมและ table overflow local | ✓ |

คอลัมน์ `WF` ใน `FUNCTION_CHECKLIST_F-WH-DN_DeliveryNote.md` ถูกอัปเดตเป็น ☑ ครบ 34 รายการ; คอลัมน์ DEV/QA ยังไม่แตะ

## 2. Business edge coverage

| Edge / contract | UI hook | Source alignment | ผล |
|---|---|---|---:|
| Picking → Packing → DN | คิวรับเฉพาะ packed และ bind `dnRef` | Central Plan `Picking → Packing → DN`; locked Picking/Packing | ✓ |
| DN → Inventory | dispatch Goods Issue + reverse/return movements | Central Plan inventory movement contract | ✓ |
| DN → SO | issued/shipped/returned + status flow | PREBRIEF BR-08/11/14 | ✓ |
| DN → AR Invoice | action หลัง delivered/partial | Central Plan “bill from delivery” | ✓ |
| DN → Sales Return / RTN | partial/rejected/return-all hooks | Central Plan + PREBRIEF S-11/S-14 | ✓ |
| Stock Transfer → DN | referenced transfer queue and print/ref display | User-confirmed scope 20 Aug 2569 | ✓ |
| Document Config | UI แสดงเลข prospective; print spec ห้าม hardcode production running | PREBRIEF + declaration selection | ✓ |

## 3. Confirmed decisions reflected

1. รวมหลาย Packing/SO ได้เมื่อ **ประเภทต้นทาง + ลูกค้า + ที่อยู่จัดส่งเดียวกัน**; direct hash navigation ที่ข้ามกฎถูก guard ซ้ำใน confirm
2. Stock Transfer เป็นเส้นทางใช้งานจริงใน prototype ไม่ใช่ข้อความ placeholder
3. Manual creation แยกปุ่ม/ฟอร์ม/flag จาก reference creation และมี status controller ที่เลือกได้ทุกสถานะ พร้อมเหตุผลและ audit
4. Manual status ไม่ทำ Goods Issue หรือ sync SO/Transfer อัตโนมัติ เพื่อไม่สร้าง side effect จากเอกสารที่ไม่มี reference; ข้อจำกัดนี้แสดงใน UI ชัดเจน

## 4. Scope and dependency notes

- ไม่แก้ไฟล์ต้นฉบับใต้ `Pack Brief Feature\Delivery Note`
- ไม่แก้ Picking, Packing, Stock Transfer หรือ shared BASE-KIT
- การทำ production contract ฝั่ง Stock Transfer เป็น downstream proposal สำหรับ Step 12; รอบนี้ไม่มี unresolved conflict เพราะ UI/behavior ของ DN ใช้ reference แบบ soft-ref และไม่แก้ feature อื่น
- Out of scope ตาม PREBRIEF ยังคงเดิม: route optimization, split vehicle, mobile e-POD/GPS, 3PL API จริง, auto freight และ auto Credit Note

## 5. Evidence files

- `02_QC/step1-render.png`
- `02_QC/ux-shots/route_list.png`
- `02_QC/ux-shots/route_list__overlay_tbody tr.png`
- `02_QC/dn-a4-preview.png`
- `_UX_CHECK_REPORT.md`

**Round-1 gate:** ผ่านสำหรับไป Step 5 E2E

### Freshness recheck · manual-test feedback

หลังแก้ icon visibility, source-controlled customer hint, reload drawer และ manual failed-attempt counter: `WF 34/34`, regression anchors `4/4`, E2E `16/16`, console errors `0`.

### PM/BA refinement · transport assignment

FN-09 ขยายให้ confirm/draft ใช้ search dropdown, ผู้รับผิดชอบจำกัดเฉพาะพนักงานบริษัท, และส่วนขนส่งกรอกรถ/คนขนส่งภายนอกเองได้ ผล fresh recheck: PMBA anchors `6/6`, E2E `17/17`, console errors `0`.
