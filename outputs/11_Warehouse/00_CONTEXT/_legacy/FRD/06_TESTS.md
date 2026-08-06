# 06_TESTS — F-LOCATION-MASTER-001 (v2)

## §6.1 Acceptance
| TC | Scenario | Expected |
|---|---|---|
| TC-01 | เปิด List view (root) | แสดง Warehouses, KPI 5 ระดับ, drill-path = "ทุก Warehouse" |
| TC-02 | คลิกแถว Warehouse | drill ลง → แสดง Zones ของ WH นั้น + drill-path อัปเดต |
| TC-03 | Drill ครบ → Rack | แสดง Locations + filter type/status |
| TC-04 | สลับ List ↔ Hierarchy view | context (node ที่เลือก) คงอยู่ |
| TC-05 | Hierarchy view เลือก node | ฝั่งขวาแสดง summary panel (ไม่ใช่ตาราง list) + child stat chips |
| TC-06 | คลิก child stat chip ใน summary | สลับไป List view ที่ node นั้น |
| TC-07 | Create Warehouse + เลือกจังหวัด | dropdown อำเภอเปิด + reset ค่าเดิม |
| TC-08 | เลือกตำบล | รหัสไปรษณีย์ auto-fill (read-only) |
| TC-09 | Create Zone temp_controlled ไม่กรอกช่วง | block (TEMP_RANGE_REQUIRED) |
| TC-10 | Create Area allows_direct=true | สำเร็จ + Area แสดง segmented Racks/Location ตรง |
| TC-11 | Create Location under Rack | parent=rack → rack lookup required, area ว่าง |
| TC-12 | Create Location under Area (allows_direct=false) | reject + แนะนำเพิ่ม rack |
| TC-13 | Create Location both parents | blocked (CHECK / FN-13) |
| TC-14 | type=PACK | pill ม่วง "Pack"; (Phase 3) default flags = work location |
| TC-15 | Duplicate code within parent (ทุกระดับ) | 409 CODE_DUPLICATE |
| TC-16 | Wizard step1 validation | Next ถูก block จนกรอกครบ |
| TC-17 | Delete WH/Zone/Area/Rack ที่มีลูก | blocked (HAS_CHILDREN) |
| TC-18 | ปิด area.allows_direct ทั้งที่มี direct loc | blocked (HAS_DIRECT_LOCATIONS) |
| TC-19 | Deactivate/Decommission location with stock | blocked + migrate |
| TC-20 | Bulk generate preview | แสดงจำนวน rack×location ก่อน generate |
| TC-21 | Bulk generate collision | atomic rollback + error |
| TC-22 | View location 3 tabs | ภาพรวม/ความจุ&flags/ประวัติ |
| TC-23 | View node | fields + full path + child counts + ปุ่มเจาะลง |
| TC-24 | Status pill colors | ตรงตาม state (7 location + active/inactive node) |
| TC-25 | Esc/backdrop/X | ปิด drawer/modal 3 ทาง |
| TC-26 | Operator role | ปุ่ม create/edit/delete ซ่อน (view only) |
| TC-27 | Supervisor role | สร้าง/แก้ได้ แต่ปุ่มลบซ่อน (delete = Manager/Admin) |

## §6.2 Definition of Done
CRUD ครบ 5 ระดับ; flexible-parent enforced (UI + FN-13 + CHECK); allows_direct gate + toggle guard; referential-safe delete; node code uniqueness within parent; zone temp validation; geo cascade + postcode auto; empty-before-deactivate; bulk-gen atomic+preview; location state machine; wizard validation; dual-view context-shared; PACK type + (Phase 3) type-default flags; RBAC + SoD (delete=Manager); HTML Iron Rules 31/31; refresh-safe routing; WORM audit ทุก mutation.

## §6.3 Edge/Negative
EC-01..EC-17 covered.
