# 06_TESTS — F-LOCATION-MASTER-001 · Warehouse & Bin

> Audience: QA. Acceptance per story + edge + cross-module + DoD. **Expected text = verbatim จาก HTML** (source of truth); fallback microcopy กลาง v7.

---

## §6.1 Acceptance Tests (per BRD §7 story)

| ID | Story | Steps | Expected (verbatim) |
|---|---|---|---|
| AT-01 | S-01 create WH + branch | สร้างคลัง กรอก code/name/branch/geo | สาขาว่าง→บันทึกไม่ได้, toast "กรุณาเลือกสาขา"; code ซ้ำ→"รหัสซ้ำในระบบ"; สำเร็จ→"สร้างคลัง \"{code}\" สำเร็จ" |
| AT-02 | S-02 zone temp | เปิด temp_controlled ไม่กรอก min/max | "กรุณากรอกช่วงอุณหภูมิ"; min>max→"อุณหภูมิต่ำสุดต้องไม่เกินสูงสุด" |
| AT-03 | S-03 allows_direct | เลือก area allows_direct=false เป็น parent ตำแหน่ง | inline-warn "พื้นที่ {code} ตั้งค่า allows_direct = false — วางตำแหน่งตรงไม่ได้…" + link "เพิ่มชั้นวางในพื้นที่นี้ก่อน"; edit ปิด allows_direct ที่มี direct loc → "ปิด allows_direct ไม่ได้ — ยังมีตำแหน่งวางตรงอยู่ {n} รายการ" |
| AT-04 | S-04 location XOR + cap | สร้างตำแหน่ง เลือก parent, cap_val=0 | "ความจุต้องมากกว่า 0"; parent rack XOR area (radio-card เลือกได้ทีละ 1); code ซ้ำ→"รหัสซ้ำภายใน parent เดียวกัน" |
| AT-05 | S-05 bulk generate | template + preview + submit | preview "จะสร้างทั้งหมด: {N} ชั้นวาง × {M} = total"; collision→"ไม่สามารถสร้างได้ — ตรวจแม่แบบ/รหัสชน"; สำเร็จ→"สร้าง {N} ชั้นวาง × {M} ตำแหน่งสำเร็จ (atomic)" |
| AT-06 | S-06 archive node | archive node ที่มีลูก active / ไม่มี | มีลูก→danger "จัดเก็บ{lbl}ไม่ได้" + "จัดเก็บไม่ได้ — ยังมีรายการลูกใช้งานอยู่ {n} รายการ"; ไม่มี→confirm→"จัดเก็บ{lbl}แล้ว" (status=จัดเก็บแล้ว, ไม่ลบถาวร) |
| AT-07 | S-07 decommission | decommission location stock≠0 / =0 | stock≠0→danger "ปลดระวางไม่ได้" + "ต้องย้ายสต็อกออกก่อน…(BR-010)"; =0→"ปลดระวางตำแหน่งแล้ว" (decommissioned soft) |
| AT-08 | S-08 status change | block ไม่ระบุเหตุผล / activate ไม่มี barcode | block ว่าง→"ระบุเหตุผลที่บล็อก"; สำเร็จ→"บล็อกตำแหน่งแล้ว"; activate no barcode→"ต้องเพิ่มบาร์โค้ดก่อนถึงจะเปิดใช้งานตำแหน่งได้" |
| AT-09 | S-09 Operator view-only | login Operator | ปุ่มสร้าง/bulk disabled + tooltip "บทบาทนี้ไม่มีสิทธิ์สร้าง (ดูอย่างเดียว)"; ไม่มีปุ่ม archive/decommission |
| AT-10 | S-10 switch view keep sel | เลือก node ใน Tree → สลับ List | selection คงอยู่ (shared state.sel); view switcher สลับ List/Hierarchy |

## §6.2 Location create — barcode gate
- Create location ไม่มี barcode (loc_require_barcode ON) → toast "สร้างตำแหน่ง \"{code}\" สำเร็จ (ปิดใช้ — ต้องเพิ่มบาร์โค้ดก่อนเปิดใช้งาน)", status=inactive. เพิ่ม barcode → activate ได้.

## §6.3 Edit
- แก้ node/location สำเร็จ → "บันทึกการแก้ไขแล้ว".

## §6.4 Reparent gate
- ย้าย location ที่ hasStock → "ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)" (BR-012); stock=0 → ย้ายได้, full_path/path recompute.

## §6.5 Edge case tests
EC-01..EC-13 (☑, §5.4) each: assert block + verbatim message. EC-14..EC-18 (☐ `[AI-DEFAULT]`): test as documented default, mark pending BA confirm.

## §6.6 Permission matrix tests
For each role × action (create/edit/status/archive/decommission) assert allow/deny per §0.8. Deny → button disabled + tooltip (UI) / 403 `FORBIDDEN_ROLE` (API). SoD: Supervisor/Controller archive/decommission denied.

## §6.7 Status machine tests
Assert allowed transitions (§5.2); illegal transition rejected. decommissioned = terminal. Node active→archived only when no active children.

## §6.9 Cross-Module Test Cases (R12 — BRD §12.1)
| ID | Case | Expected |
|---|---|---|
| XT-01 | decommission location → downstream | emit `location.decommissioned`; Inventory ต้องไม่มี orphan stock (gate stock=0 ก่อน) |
| XT-02 | reparent location → path change | emit `location.reparented {old_path,new_path}`; downstream ที่ cache path re-read (EC-18) |
| XT-03 | block/frozen location | emit status event; Picking/Put Away gate หยิบ/วางไม่ได้ |
| XT-04 | full_path contract | export `location_id + full_path` = "WH code › zone name › area name › rack name › location code" — **no branch** (D15) |

## §6.10 Definition of Done
- [ ] AT-01..AT-10 pass · [ ] EC-01..EC-13 pass · [ ] permission matrix pass · [ ] status machine pass · [ ] XT-01..XT-04 pass
- [ ] All mutations write WORM audit; no hard delete anywhere (verify no DELETE) — GC#7/D11
- [ ] Uniqueness enforced at DB (concurrent test EC-15) · [ ] bulk atomic rollback (EC-06)
- [ ] full_path format correct (no branch, D15) · [ ] SLA: List/Tree ≤2s, bulk ≤5s/~500, action ≤1s (§17.1)
- [ ] `[AI-DEFAULT]` items (EC-14/15/17, OQ-4/5/7) flagged for BA confirm before Phase 2
