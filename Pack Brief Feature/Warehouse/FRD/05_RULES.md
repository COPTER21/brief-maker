# 05_RULES — F-LOCATION-MASTER-001 (v2)

## §5.1 Business Rules
| ID | Rule | Tag |
|---|---|---|
| BR-001 | Flexible parent: location rack XOR area (CHECK + FN-13) | FIXED |
| BR-002 | allows_direct gate (parent=area → area.allows_direct=true) | FIXED |
| BR-003 | Node code unique within parent (WH global / Zone-in-WH / Area-in-Zone / Rack-in-Area / Loc-in-parent) | FIXED |
| BR-004 | Location type = fixed enum 10 core (9 + PACK); type drives default flow | FIXED |
| BR-005 | Referential-safe delete: node ที่มีลูกลบไม่ได้ | FIXED |
| BR-006 | Zone temp_controlled=true → temp_min/max required, min≤max | FIXED |
| BR-007 | ปิด area.allows_direct ไม่ได้ถ้ายังมี direct location | FIXED |
| BR-008 | Warehouse address ดึงจาก Geo Master; postcode auto จาก subdistrict | FIXED |
| BR-009 | Capacity value > 0 | FIXED |
| BR-010 | Empty before deactivate/decommission (stock=0) | FIXED |
| BR-011 | Bulk-gen atomic + preview (no partial commit) | FIXED |
| BR-012 | Re-parent requires source empty / migrate | FIXED |
| BR-013 | Auto-full at max capacity | FIXED |
| BR-014 | Location ต้องมี barcode ก่อน activate | CONFIGURABLE (`loc_require_barcode`) |
| BR-015 | type → default behavior template (PACK=work loc not pickable …) | CONFIGURABLE (Phase 3, FN-23) |
| BR-S02 | Capacity check on putaway (≤ max) | CONFIGURABLE |
| BR-S03 | Item-type compatibility | CONFIGURABLE |
| BR-S04 | Temperature within zone range | CONFIGURABLE |
| BR-S06 | FEFO for expiry items | CONFIGURABLE |

## §5.2 Validation
- **Node pre-create/update:** code unique within parent; parent FK active; zone temp range ถ้า temp_controlled; area allows_direct flag.
- **Node pre-delete:** no children (zones/areas/racks/locations).
- **Location pre-create:** parent_type set; matching FK (XOR); area.allows_direct ถ้า parent=area; type∈10; capacity>0; coords within rack grid (ถ้า rack).
- **Location pre-activate:** barcode (ถ้า BR-014 on) + capacity + flags + rotation set.
- **Location pre-transaction:** status=active; capacity not exceeded; item-type allowed.
- **Warehouse address:** subdistrict เลือกแล้ว → postcode auto; province→district→subdistrict cascade integrity.

## §5.3 State Machine
**Nodes (WH/Zone/Area/Rack):** `active ⇄ inactive`; `active → (deleted ถ้าไม่มีลูก)`.
**Location (7 states):**
```
active → inactive | blocked(+reason) | maintenance | full(auto) | frozen | decommissioned
blocked → active ; frozen → active ; full → active(auto)
deactivate/decommission require stock=0 ; decommissioned = terminal (soft, keep history)
```

## §5.4 Edge Cases
| ID | Case | Behavior |
|---|---|---|
| EC-01 | location parent both rack+area | reject (CHECK / FN-13) |
| EC-02 | location no parent | reject |
| EC-03 | parent=area not allows_direct | reject + suggest add rack |
| EC-04 | putaway to full | block + alternative |
| EC-05 | deactivate/decommission with stock | block + migrate |
| EC-06 | bulk-gen code collision | atomic rollback |
| EC-07 | decommission with history | soft-keep (no hard delete) |
| EC-08 | capacity_value ≤ 0 | validation error |
| EC-09 | Operator attempts create/edit | 403 (view only) |
| EC-10 | delete WH/Zone/Area/Rack ที่มีลูก | block (BR-005) |
| EC-11 | zone temp_controlled แต่ไม่กรอกช่วง | reject (BR-006) |
| EC-12 | code ซ้ำใน parent (ทุกระดับ) | 409 |
| EC-13 | Supervisor attempts delete | 403 (delete = Manager/Admin) |
| EC-14 | ปิด area.allows_direct ทั้งที่มี direct loc | block (BR-007) |
| EC-15 | bulk-gen grid = 0 (rows/cols/levels=0) | block (preview total=0) |
| EC-16 | reparent ข้าม parent → code ชนใน parent ใหม่ | reject (re-check uniqueness) |
| EC-17 | เลือก province แล้วเปลี่ยน → district/subdistrict/postcode reset | UI cascade |

## §5.5 Error Catalog
| Code | HTTP | Message |
|---|---|---|
| INVALID_PARENT | 422 | parent ต้องเป็น rack หรือ area อย่างใดอย่างหนึ่ง |
| AREA_NOT_DIRECT | 422 | area นี้ไม่อนุญาตวาง location ตรง (allows_direct=false) |
| CODE_DUPLICATE | 409 | รหัสซ้ำภายใน parent |
| HAS_CHILDREN | 422 | ลบไม่ได้ — ยังมีรายการลูกอยู่ |
| HAS_DIRECT_LOCATIONS | 422 | ปิด allows_direct ไม่ได้ — ยังมี location ตรงอยู่ |
| TEMP_RANGE_REQUIRED | 422 | กรุณากรอกช่วงอุณหภูมิ |
| CAPACITY_INVALID | 422 | ความจุต้องมากกว่า 0 |
| NOT_EMPTY | 422 | ต้องย้ายสต็อกออกก่อน |
| INVALID_TRANSITION | 422 | เปลี่ยนสถานะไม่ได้ |
| BLOCK_REASON_REQUIRED | 422 | ระบุเหตุผลที่บล็อก |
| CODE_COLLISION | 409 | bulk-gen รหัสชน |
| INVALID_TEMPLATE | 422 | template ไม่ถูกต้อง |
| SOURCE_NOT_EMPTY | 422 | re-parent ต้องย้ายสต็อกก่อน |
| FORBIDDEN | 403 | ไม่มีสิทธิ์ |

## §5.7 Data Classification (D-CLASS)
- **Public:** geo reference (province/district/subdistrict/postcode) — read-only.
- **Internal (default, all owned):** node/location/address — RBAC by role; WORM audit.
- **Confidential/Restricted:** none.
- **Enforcement:** API RBAC (§02) · UI action visibility by role (§4.2 BRD) · Audit WORM ทุก mutation. No Policy Center Restricted registration.
