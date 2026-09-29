# AI Test Cases — F-WH-LOT Lot/Serial + Expiry

## Meta
| Key | Value |
|---|---|
| Feature ID | F-WH-LOT |
| Version | 1.0 / 2026-09-14 |
| App entry | F-WH-LOT.html |
| Routes | #/records, #/history, #/settings + drawer |
| Cases | 59 · Mirror UAT |
| Source | FRD v6 00–08, BRD v1, HTML after S3 freeze |

## Coverage
- รายการและทางเข้า: 10 cases
- สร้างล็อตและซีเรียล: 16 cases
- นโยบายรายสินค้า: 8 cases
- FEFO และความพร้อมใช้: 9 cases
- ติดตามการเคลื่อนไหว: 6 cases
- ขอบเขตและสิทธิ์: 10 cases

## Coverage Ledger
### FRD acceptance
| item | cases / status |
|---|---|
| AT-01 | TC-026, TC-027, TC-028, TC-029, TC-030, TC-031, TC-032 |
| AT-02 | TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-019 |
| AT-03 | TC-017 |
| AT-04 | TC-018, TC-020, TC-021, TC-022 |
| AT-05 | TC-034, TC-035, TC-036, TC-037, TC-038, TC-040, TC-041, TC-042 |
| AT-06 | TC-039 |
| AT-07 | TC-007, TC-043, TC-044, TC-045, TC-046, TC-047 |
| AT-08 | TC-001, TC-002, TC-004, TC-005, TC-006, TC-008, TC-009, TC-010, TC-023 |
| AT-09 | TC-033 |
| AT-10 | TC-025, TC-058 |
| AT-11 | TC-002, TC-003 |
| AT-12 | TC-023, TC-024 |
### Business rules
| item | cases / status |
|---|---|
| BR-01 | TC-013, TC-018, TC-019, TC-027, TC-028, TC-054, TC-057, TC-059 |
| BR-02 | TC-015, TC-017, TC-029 |
| BR-03 | TC-021, TC-022 |
| BR-04 | TC-005, TC-035, TC-036, TC-037, TC-038, TC-042 |
| BR-05 | TC-034, TC-039, TC-040 |
| BR-06 | TC-041, TC-051 |
| BR-07 | TC-043, TC-044, TC-045, TC-048, TC-049, TC-056 |
| BR-08 | TC-001, TC-016, TC-031, TC-032, TC-048, TC-053, TC-055 |
| BR-09 | TC-033, TC-052 |
### Edge cases
| item | cases / status |
|---|---|
| EC-01 | TC-035, TC-036 |
| EC-02 | TC-003, TC-046, TC-050 |
| EC-03 | TC-021 |
### Errors
| item | cases / status |
|---|---|
| ITEM_NOT_FOUND | TC-012 |
| TRACKING_DISABLED | TC-059 |
| EXPIRY_REQUIRED | TC-015 |
| SERIAL_REQUIRED | TC-020 |
| SERIAL_DUPLICATE | TC-021 |
| LOT_REQUIRED | TC-014 |
| INVALID_POLICY | TC-030 |
| VERSION_CONFLICT | TC-057 |
| FORBIDDEN | TC-054, TC-055, TC-056 |
| SOURCE_UNAVAILABLE | TC-050 |
| NO_ELIGIBLE_LOTS | TC-042 |
| IDEMPOTENCY_CONFLICT | TC-025, TC-058 |
### Permission cells
| item | cases / status |
|---|---|
| P_OPERATOR_CREATE_ALLOW | TC-016 |
| P_OPERATOR_CONFIG_DENY | TC-054 |
| P_CONFIG_POLICY_ALLOW | TC-028 |
| P_AUDITOR_TRACE_ALLOW | TC-043 |
| P_AUDITOR_CREATE_DENY | TC-055 |
### Cross-module
| item | cases / status |
|---|---|
| XT-01 | TC-043, TC-049, TC-050 |
| XT-02 | TC-033, TC-052 |
| XT-03 | TC-051 |
| XT-04 | TC-053 |
### Scope lock
| item | cases / status |
|---|---|
| LOCK-W4-LOT | TC-023, TC-041, TC-048 |

## Data Sets
| Set | Field | Value |
|---|---|---|
| A | item | ITEM-101 · ข้าวหอม; tracking lot; expiry on |
| A | lot/expiry | NEW-101 / 2026-12-01 |
| B | item | ITEM-102 · นม UHT; tracking serial; expiry on |
| B | serial | SN-102 duplicate / SN-999 unique |
| C | item | ITEM-103 · อะไหล่; tracking lot; expiry off |
| D | FEFO | Oct01, Oct15, expired Sep01, held Nov01; onHand/held per fixture |
| E | trace | 011→GRN-2609-014/Transfer-2609-009; 012→GRN-2609-016 |

## Test Cases
### รายการและทางเข้า
#### TC-001 — เปิดรายการล็อต
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08 BR-08
- actor (role): role=operator
- Setup: role=operator; seed=7 identity fixtures
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็นคอลัมน์ รหัสล็อต สินค้า ซีเรียล วันหมดอายุ สถานะ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | VERIFY ตารางใต้หัวข้อ Lot/Serial + Expiry | — | เห็นคอลัมน์ รหัสล็อต สินค้า ซีเรียล วันหมดอายุ สถานะ | ☐ |

#### TC-002 — ค้นหารหัสล็อตที่มี
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08 AT-11
- actor (role): role=operator
- Setup: role=operator; seed=LOT-2609-011
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: แสดงจำนวนที่ตรงกับข้อมูลจริง
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | TYPE ช่อง “ค้นหาชื่อ / รหัสสินค้า / รหัสเก่า…” | LOT-2609-011 | เหลือแถวที่มีรหัสนี้ | ☐ |
| 3 | VERIFY ตัวเลขท้ายตาราง | — | แสดงจำนวนที่ตรงกับข้อมูลจริง | ☐ |

#### TC-003 — ค้นหาที่ไม่มีผล
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-11 EC-02
- actor (role): role=operator
- Setup: role=operator; seed=fixture เดิม
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “ไม่พบรายการที่ตรงกับตัวกรอง”
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | TYPE ช่องค้นหา | ZZ-NO-LOT | เห็น “ไม่พบรายการที่ตรงกับตัวกรอง” | ☐ |

#### TC-004 — ล้างตัวกรอง
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08
- actor (role): role=operator
- Setup: role=operator; seed=ค้นหา ZZ-NO-LOT อยู่
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ช่องค้นหาว่างและแถวกลับตามข้อมูลจริง
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “ล้างตัวกรอง” | — | ช่องค้นหาว่างและแถวกลับตามข้อมูลจริง | ☐ |

#### TC-005 — กรองสถานะกักอยู่
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08 BR-04
- actor (role): role=operator
- Setup: role=operator; seed=มี LOT-2609-023 held
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เฉพาะล็อตสถานะกักอยู่ปรากฏ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | SELECT ตัวกรองสถานะ | กักอยู่ | เฉพาะล็อตสถานะกักอยู่ปรากฏ | ☐ |

#### TC-006 — เรียงตามรหัสล็อต
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08
- actor (role): role=operator
- Setup: role=operator; seed=หลาย lot
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ลำดับกลับด้าน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK หัวคอลัมน์ “รหัสล็อต” | — | แถวเรียงตามรหัส | ☐ |
| 3 | CLICK หัวคอลัมน์ “รหัสล็อต” | — | ลำดับกลับด้าน | ☐ |

#### TC-007 — เปิด drawer จากแถว
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-07 P-04
- actor (role): role=operator
- Setup: role=operator; seed=LOT-2609-011
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: drawer รายละเอียดแสดงรหัสล็อตที่เลือก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK แถว LOT-2609-011 | — | drawer รายละเอียดแสดงรหัสล็อตที่เลือก | ☐ |

#### TC-008 — สลับ tab รายการและ trace
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08 P-01 P-02
- actor (role): role=operator
- Setup: role=operator
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: route #/records และตารางปรากฏ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK tab “ติดตามการเคลื่อนไหว” | — | route #/history และตัวเลือกล็อตปรากฏ | ☐ |
| 3 | CLICK tab “ล็อตและซีเรียล” | — | route #/records และตารางปรากฏ | ☐ |

#### TC-009 — โหลด route ตรง
- group: รายการและทางเข้า · ความสำคัญ: สูง · trace: AT-08 P-02
- actor (role): role=auditor
- Setup: role=auditor
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: route และหน้าถูกคงหลัง refresh
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | VERIFY tab “ติดตามการเคลื่อนไหว” | — | route และหน้าถูกคงหลัง refresh | ☐ |

#### TC-010 — ส่งออกรายการ
- group: รายการและทางเข้า · ความสำคัญ: กลาง · trace: AT-08
- actor (role): role=operator
- Setup: role=operator
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ดาวน์โหลด CSV ที่มีหัวคอลัมน์ตามรายการ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “ส่งออก” | — | ดาวน์โหลด CSV ที่มีหัวคอลัมน์ตามรายการ | ☐ |

### สร้างล็อตและซีเรียล
#### TC-011 — เปิดฟอร์มสร้าง
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 P-04
- actor (role): role=operator
- Setup: role=operator; permission create
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: drawer “สร้างล็อตหรือซีเรียล” เปิด และ focus ไปช่องสินค้า
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “สร้างรายการ” | — | drawer “สร้างล็อตหรือซีเรียล” เปิด และ focus ไปช่องสินค้า | ☐ |

#### TC-012 — บังคับเลือกสินค้า
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 ITEM_NOT_FOUND
- actor (role): role=operator
- Setup: role=operator; open create drawer
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: แสดง “เลือกสินค้าจากรายการ”; ไม่เพิ่มแถว
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” โดยไม่เลือกสินค้า | — | แสดง “เลือกสินค้าจากรายการ”; ไม่เพิ่มแถว | ☐ |

#### TC-013 — ค้นหาสินค้าใน picker
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 BR-01
- actor (role): role=operator
- Setup: role=operator; open create drawer
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ช่องสินค้าแสดง ITEM-101 และช่อง expiry ปรากฏ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | TYPE ช่อง “ค้นหาสินค้า” | ITEM-101 | option แสดงรหัสสินค้า ชื่อ และคลัง | ☐ |
| 3 | CLICK option ITEM-101 · ข้าวหอม | — | ช่องสินค้าแสดง ITEM-101 และช่อง expiry ปรากฏ | ☐ |

#### TC-014 — บังคับรหัสล็อต
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 LOT_REQUIRED
- actor (role): role=operator
- Setup: role=operator; create drawer selected ITEM-101 with expiry date
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: แสดง “กรอกรหัสล็อต”; ไม่เพิ่มแถว
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” โดยปล่อยรหัสล็อตว่าง | — | แสดง “กรอกรหัสล็อต”; ไม่เพิ่มแถว | ☐ |

#### TC-015 — บังคับ expiry เฉพาะสินค้าเปิด
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 BR-02 EXPIRY_REQUIRED
- actor (role): role=operator
- Setup: role=operator; selected ITEM-101; lot NEW-101; expiry blank
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: แสดง “กรอกวันหมดอายุ”; ไม่มีแถวใหม่
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” | — | แสดง “กรอกวันหมดอายุ”; ไม่มีแถวใหม่ | ☐ |

#### TC-016 — สร้างล็อตพร้อม expiry
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 BR-08 P_OPERATOR_CREATE_ALLOW
- actor (role): role=operator
- Setup: role=operator; selected ITEM-101; lot NEW-101; expiry 2026-12-01
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: มี NEW-101 หนึ่งแถว; movement เดิมไม่เปลี่ยน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” | — | ปุ่มแสดง “กำลังบันทึก…” แล้ว toast “บันทึกแล้ว” | ☐ |
| 3 | VERIFY ตาราง | — | มี NEW-101 หนึ่งแถว; movement เดิมไม่เปลี่ยน | ☐ |

#### TC-017 — ไม่บังคับ expiry สำหรับ ITEM-103
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-03 BR-02
- actor (role): role=operator
- Setup: role=operator; selected ITEM-103; lot NEW-103; expiry blank
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: บันทึกได้และวันหมดอายุแสดงว่าง/—
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” | — | บันทึกได้และวันหมดอายุแสดงว่าง/— | ☐ |

#### TC-018 — ITEM-102 เปิดช่องซีเรียล
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-04 BR-01
- actor (role): role=operator
- Setup: role=operator; open create drawer
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ช่อง “ซีเรียล” และ “วันหมดอายุ” ปรากฏ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK option ITEM-102 · นม UHT | — | ช่อง “ซีเรียล” และ “วันหมดอายุ” ปรากฏ | ☐ |

#### TC-019 — ITEM-101 ซ่อนช่องซีเรียล
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-02 BR-01
- actor (role): role=operator
- Setup: role=operator; open create drawer
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ช่องซีเรียลไม่ปรากฏ แต่วันหมดอายุปรากฏ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK option ITEM-101 · ข้าวหอม | — | ช่องซีเรียลไม่ปรากฏ แต่วันหมดอายุปรากฏ | ☐ |

#### TC-020 — บังคับซีเรียล
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-04 SERIAL_REQUIRED
- actor (role): role=operator
- Setup: role=operator; selected ITEM-102; lot NEW-S; expiry 2026-12-01; serial blank
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: แสดง “กรอกซีเรียล”; ไม่เพิ่มแถว
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” | — | แสดง “กรอกซีเรียล”; ไม่เพิ่มแถว | ☐ |

#### TC-021 — ปฏิเสธซีเรียลซ้ำใน item
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-04 BR-03 SERIAL_DUPLICATE EC-03
- actor (role): role=operator
- Setup: role=operator; selected ITEM-102; lot NEW-S; serial SN-102; expiry valid
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: แสดง “ซีเรียลนี้ถูกใช้แล้ว”; ไม่มีแถวใหม่
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” | — | แสดง “ซีเรียลนี้ถูกใช้แล้ว”; ไม่มีแถวใหม่ | ☐ |

#### TC-022 — สร้างซีเรียลไม่ซ้ำ
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-04 BR-03
- actor (role): role=operator
- Setup: role=operator; selected ITEM-102; lot NEW-S2; serial SN-999; expiry valid
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: “บันทึกแล้ว”; แถวใหม่มี SN-999
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” | — | “บันทึกแล้ว”; แถวใหม่มี SN-999 | ☐ |

#### TC-023 — ยกเลิกฟอร์ม
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-08 LOCK-W4-LOT AT-12
- actor (role): role=operator
- Setup: role=operator; open create drawer and enter NEW-CANCEL
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: drawer ปิด; ไม่เพิ่มรายการหรือประวัติ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “ยกเลิก” | — | drawer ปิด; ไม่เพิ่มรายการหรือประวัติ | ☐ |

#### TC-024 — Esc ปิดฟอร์ม
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-12
- actor (role): role=operator
- Setup: role=operator; open create drawer
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: drawer และ backdrop ปิด; ไม่มีการบันทึก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | PRESS Escape | — | drawer และ backdrop ปิด; ไม่มีการบันทึก | ☐ |

#### TC-025 — ป้องกันส่งซ้ำ local
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: AT-10 IDEMPOTENCY_CONFLICT
- actor (role): role=operator
- Setup: role=operator; save nonserial ITEM-103 NEW-REPLAY once; same form payload/key again
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “รายการนี้ส่งแล้ว”; มี identity/event ครั้งเดียว
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” ซ้ำ | — | เห็น “รายการนี้ส่งแล้ว”; มี identity/event ครั้งเดียว | ☐ |

#### TC-059 — ปฏิเสธสร้างเมื่อ item ปิด tracking
- group: สร้างล็อตและซีเรียล · ความสำคัญ: สูง · trace: BR-01 TRACKING_DISABLED
- actor (role): role=config owner
- Setup: role=config owner; ITEM-101 policy set to ไม่ติดตาม and expiry off; open create drawer
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “สินค้านี้ไม่ได้เปิดติดตามล็อตหรือซีเรียล”; ไม่เพิ่ม identity
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK option ITEM-101 · ข้าวหอม | — | item ถูกเลือก | ☐ |
| 3 | CLICK “บันทึก” | — | เห็น “สินค้านี้ไม่ได้เปิดติดตามล็อตหรือซีเรียล”; ไม่เพิ่ม identity | ☐ |

### นโยบายรายสินค้า
#### TC-026 — เปิดตั้งค่ารายสินค้า
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 P-03
- actor (role): role=config owner
- Setup: role=config owner
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็นสินค้า รูปแบบติดตาม และบังคับวันหมดอายุ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | VERIFY หัวข้อ “ตั้งค่ารายสินค้า” | — | เห็นสินค้า รูปแบบติดตาม และบังคับวันหมดอายุ | ☐ |

#### TC-027 — ค้นหา ITEM-102 ใน settings
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 BR-01
- actor (role): role=config owner
- Setup: role=config owner
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: รูปแบบติดตามเป็นซีเรียลและวันหมดอายุเปิด
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | TYPE ช่องสินค้า | ITEM-102 | option ITEM-102 · นม UHT ปรากฏ | ☐ |
| 3 | CLICK option ITEM-102 | — | รูปแบบติดตามเป็นซีเรียลและวันหมดอายุเปิด | ☐ |

#### TC-028 — เปลี่ยนโหมด ITEM-101
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 BR-01 P_CONFIG_POLICY_ALLOW
- actor (role): role=config owner
- Setup: role=config owner; selected ITEM-101
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: toast “บันทึกการตั้งค่าแล้ว”; event เพิ่ม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | SELECT “รูปแบบติดตาม” | ซีเรียล | select แสดงซีเรียล | ☐ |
| 3 | CLICK “บันทึกการตั้งค่า” | — | toast “บันทึกการตั้งค่าแล้ว”; event เพิ่ม | ☐ |

#### TC-029 — ปิด expiry ราย item
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 BR-02
- actor (role): role=config owner
- Setup: role=config owner; selected ITEM-101
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ITEM-101 ต่อไปไม่บังคับวันที่; ITEM-102 ไม่เปลี่ยน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | TOGGLE “บังคับวันหมดอายุ” | ปิด | checkbox ไม่ถูกเลือก | ☐ |
| 3 | CLICK “บันทึกการตั้งค่า” | — | ITEM-101 ต่อไปไม่บังคับวันที่; ITEM-102 ไม่เปลี่ยน | ☐ |

#### TC-030 — reject mode none + expiry
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 INVALID_POLICY
- actor (role): role=config owner
- Setup: role=config owner; selected ITEM-101
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “เปิดวันหมดอายุต้องติดตามล็อตหรือซีเรียล”; policy ไม่เปลี่ยน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | SELECT “รูปแบบติดตาม” | ไม่ติดตาม | select แสดงไม่ติดตาม | ☐ |
| 3 | TOGGLE “บังคับวันหมดอายุ” | เปิด | checkbox ถูกเลือก | ☐ |
| 4 | CLICK “บันทึกการตั้งค่า” | — | เห็น “เปิดวันหมดอายุต้องติดตามล็อตหรือซีเรียล”; policy ไม่เปลี่ยน | ☐ |

#### TC-031 — policy isolate ITEM-101/102
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 BR-08
- actor (role): role=config owner
- Setup: role=config owner; ITEM-101 and 102 seeded
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ITEM-102 ยังเป็นซีเรียล+expiry ตามเดิม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK บันทึก ITEM-101 tracking change | — | ITEM-101 เปลี่ยน | ☐ |
| 3 | CLICK option ITEM-102 | — | ITEM-102 ยังเป็นซีเรียล+expiry ตามเดิม | ☐ |

#### TC-032 — policy audit append (system/mock)
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-01 BR-08
- actor (role): role=auditor
- Setup: role=auditor; config owner saved policy
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: event ใหม่เพิ่ม; movement ก่อนหน้าไม่เปลี่ยน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | VERIFY ประวัติการตั้งค่า | — | event ใหม่เพิ่ม; movement ก่อนหน้าไม่เปลี่ยน | ☐ |

#### TC-033 — เปิดกฎแจ้งเตือน
- group: นโยบายรายสินค้า · ความสำคัญ: สูง · trace: AT-09 BR-09 XT-02
- actor (role): role=config owner
- Setup: role=config owner
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “กฎแจ้งเตือนเปิดในระบบกลาง”; ไม่มี threshold ในหน้านี้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “เปิดกฎแจ้งเตือน” | — | เห็น “กฎแจ้งเตือนเปิดในระบบกลาง”; ไม่มี threshold ในหน้านี้ | ☐ |

### FEFO และความพร้อมใช้
#### TC-034 — เรียง FEFO ตาม expiry
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-05
- actor (role): role=operator
- Setup: role=operator; ITEM-101 expiry enabled; fixture Oct01/Oct15
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: Oct01 อยู่ก่อน Oct15 ในตารางคำแนะนำ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | Oct01 อยู่ก่อน Oct15 ในตารางคำแนะนำ | ☐ |

#### TC-035 — ตัดล็อตหมดอายุ
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-04 EC-01
- actor (role): role=operator
- Setup: role=operator; ITEM-101; fixture expired Sep01
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ล็อตหมดอายุไม่อยู่ในคำแนะนำ แต่ยังอยู่รายการ/trace
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | ล็อตหมดอายุไม่อยู่ในคำแนะนำ แต่ยังอยู่รายการ/trace | ☐ |

#### TC-036 — ตัดล็อต held เต็มจำนวน
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-04 EC-01
- actor (role): role=operator
- Setup: role=operator; ITEM-101; fixture held=onHand Nov01
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ล็อตกักเต็มจำนวนไม่ปรากฏในคำแนะนำ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | ล็อตกักเต็มจำนวนไม่ปรากฏในคำแนะนำ | ☐ |

#### TC-037 — คำนวณพร้อมใช้เป็น onHand-held (system/mock)
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-04
- actor (role): role=operator
- Setup: role=operator; ITEM-101 with partial hold snapshot
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: คอลัมน์พร้อมใช้เท่าคงเหลือลบจำนวนกัก ตาม snapshot
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | คอลัมน์พร้อมใช้เท่าคงเหลือลบจำนวนกัก ตาม snapshot | ☐ |

#### TC-038 — zero available excluded (system/mock)
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-04
- actor (role): role=operator
- Setup: role=operator; upstream snapshot onHand=0
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: zero-available lot ไม่ปรากฏ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | zero-available lot ไม่ปรากฏ | ☐ |

#### TC-039 — FIFO สำหรับ item ไม่เปิด expiry
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-06 BR-05
- actor (role): role=operator
- Setup: role=operator; ITEM-103 expiry off
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ล็อตรับก่อนอยู่ก่อนตาม receivedAt
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK option ITEM-103 | — | ตั้งค่าแสดงไม่บังคับ expiry | ☐ |
| 3 | CLICK “แนะนำล็อต” | — | ล็อตรับก่อนอยู่ก่อนตาม receivedAt | ☐ |

#### TC-040 — tie-break เสถียร (system/mock)
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-05
- actor (role): role=operator
- Setup: role=operator; two lots same expiry/receivedAt [ASSUMED fixture]
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เรียง lot id เสถียรตามข้อกำหนด; ไม่มีการสลับสุ่ม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | เรียง lot id เสถียรตามข้อกำหนด; ไม่มีการสลับสุ่ม | ☐ |

#### TC-041 — แนะนำไม่เปลี่ยน stock
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-06 LOCK-W4-LOT
- actor (role): role=operator
- Setup: role=operator; capture onHand/held snapshot ก่อน
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: onHand/held และ movement hash ไม่เปลี่ยน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | แสดงคำแนะนำ | ☐ |
| 3 | VERIFY ยอดเดิม | — | onHand/held และ movement hash ไม่เปลี่ยน | ☐ |

#### TC-042 — ไม่มีล็อตพร้อมใช้ (system/mock)
- group: FEFO และความพร้อมใช้ · ความสำคัญ: สูง · trace: AT-05 BR-04 NO_ELIGIBLE_LOTS
- actor (role): role=operator
- Setup: role=operator; item/warehouse with all lots expired or held
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “ไม่มีล็อตที่พร้อมใช้”; ไม่มี reservation
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “แนะนำล็อต” | — | เห็น “ไม่มีล็อตที่พร้อมใช้”; ไม่มี reservation | ☐ |

### ติดตามการเคลื่อนไหว
#### TC-043 — trace LOT-2609-011
- group: ติดตามการเคลื่อนไหว · ความสำคัญ: สูง · trace: AT-07 BR-07 XT-01 P_AUDITOR_TRACE_ALLOW
- actor (role): role=auditor
- Setup: role=auditor
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ตารางมี GRN-2609-014 และ Transfer-2609-009
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | SELECT ล็อต | LOT-2609-011 | ตารางมี GRN-2609-014 และ Transfer-2609-009 | ☐ |

#### TC-044 — trace LOT-2609-012
- group: ติดตามการเคลื่อนไหว · ความสำคัญ: สูง · trace: AT-07 BR-07
- actor (role): role=auditor
- Setup: role=auditor
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ตารางมี GRN-2609-016 และไม่มี ref ของ 011
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | SELECT ล็อต | LOT-2609-012 | ตารางมี GRN-2609-016 และไม่มี ref ของ 011 | ☐ |

#### TC-045 — เปิด predecessor/successor
- group: ติดตามการเคลื่อนไหว · ความสำคัญ: สูง · trace: AT-07 BR-07
- actor (role): role=auditor
- Setup: role=auditor; selected LOT-2609-011
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: รายละเอียดแสดงก่อนหน้า M-001
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | CLICK แถว M-001 | — | รายละเอียดแสดงถัดไป M-002 | ☐ |
| 3 | CLICK แถว M-002 | — | รายละเอียดแสดงก่อนหน้า M-001 | ☐ |

#### TC-046 — lot ไม่มี movement
- group: ติดตามการเคลื่อนไหว · ความสำคัญ: สูง · trace: AT-07 EC-02
- actor (role): role=auditor
- Setup: role=auditor; new master identity without movement
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: เห็น “ยังไม่มีการเคลื่อนไหวของล็อตนี้”
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | SELECT ล็อตใหม่ | — | เห็น “ยังไม่มีการเคลื่อนไหวของล็อตนี้” | ☐ |

#### TC-047 — view drawer trace เฉพาะล็อต
- group: ติดตามการเคลื่อนไหว · ความสำคัญ: สูง · trace: AT-07
- actor (role): role=auditor
- Setup: role=auditor; LOT-2609-012
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: drawer แสดง availability และ movement ของ 012 เท่านั้น
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK แถว LOT-2609-012 | — | drawer แสดง availability และ movement ของ 012 เท่านั้น | ☐ |

#### TC-048 — movement read-only
- group: ติดตามการเคลื่อนไหว · ความสำคัญ: สูง · trace: BR-07 BR-08 LOCK-W4-LOT
- actor (role): role=auditor
- Setup: role=auditor
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: ไม่มีแก้ไข/ลบ/โพสต์ stock
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | VERIFY ตาราง movement | — | ไม่มีแก้ไข/ลบ/โพสต์ stock | ☐ |

### ขอบเขตและสิทธิ์
#### TC-049 — W3 movement payload mock (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: XT-01 BR-07
- actor (role): role=integration tester
- Setup: role=integration tester; W3 mock seed LOT-2609-011
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: movement id, lot id, qty, at, from/to, predecessor shape ตรง FRD; no posting
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | VERIFY source ref ใน fixture | — | movement id, lot id, qty, at, from/to, predecessor shape ตรง FRD; no posting | ☐ |

#### TC-050 — W3 source unavailable (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: XT-01 EC-02 SOURCE_UNAVAILABLE
- actor (role): role=integration tester
- Setup: role=integration tester; W3 mock unavailable
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: empty/source-unavailable; no invented GRN ref
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | VERIFY trace response | — | empty/source-unavailable; no invented GRN ref | ☐ |

#### TC-051 — Picking receives candidate read payload (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: XT-03 BR-06
- actor (role): role=integration tester
- Setup: role=integration tester; Picking mock consumer
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: candidate lot and available qty passed, no reservation/issue
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | VERIFY ranked payload | — | candidate lot and available qty passed, no reservation/issue | ☐ |

#### TC-052 — NC expiry envelope mock (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: XT-02 BR-09
- actor (role): role=integration tester
- Setup: role=integration tester; NC mock
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: tenant/item/lot/expiry/ref/idempotency shape; no channel delivery assertion
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | VERIFY expiry candidate envelope | — | tenant/item/lot/expiry/ref/idempotency shape; no channel delivery assertion | ☐ |

#### TC-053 — CSQ policy event mock (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: XT-04 BR-08
- actor (role): role=integration tester
- Setup: role=integration tester; CSQ mock
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: payload shape and idempotency, no 7C stamp assertion
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | VERIFY master.changed envelope | — | payload shape and idempotency, no 7C stamp assertion | ☐ |

#### TC-054 — server denies unauthorized config (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: FORBIDDEN BR-01 P_OPERATOR_CONFIG_DENY
- actor (role): role=operator lacking config permission
- Setup: role=operator lacking config permission; production API simulated
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: server rejects FORBIDDEN and policy unchanged; prototype alone cannot prove
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “บันทึกการตั้งค่า” | — | server rejects FORBIDDEN and policy unchanged; prototype alone cannot prove | ☐ |

#### TC-055 — server denies auditor identity create (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: FORBIDDEN BR-08 P_AUDITOR_CREATE_DENY
- actor (role): role=auditor lacking create permission
- Setup: role=auditor lacking create permission; production API simulated
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: server rejects FORBIDDEN and identity/audit unchanged; prototype alone cannot prove
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | CLICK “บันทึก” ใน drawer | — | server rejects FORBIDDEN and identity/audit unchanged; prototype alone cannot prove | ☐ |

#### TC-056 — tenant isolation of trace (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: FORBIDDEN BR-07
- actor (role): role=auditor tenant B
- Setup: role=auditor tenant B; tenant A lot id simulated
- Start: OPEN `#/history`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: cross-tenant ref denied; prototype fixture alone cannot prove
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/history | — | หน้า ติดตามการเคลื่อนไหว ปรากฏ | ☐ |
| 2 | VERIFY trace request | — | cross-tenant ref denied; prototype fixture alone cannot prove | ☐ |

#### TC-057 — version conflict policy (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: VERSION_CONFLICT BR-01
- actor (role): role=config owner
- Setup: role=config owner; concurrent version simulated
- Start: OPEN `#/settings`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: VERSION_CONFLICT and old policy preserved; requires API integration
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/settings | — | หน้า ตั้งค่ารายสินค้า ปรากฏ | ☐ |
| 2 | CLICK “บันทึกการตั้งค่า” | — | VERSION_CONFLICT and old policy preserved; requires API integration | ☐ |

#### TC-058 — same idempotency key production (system/mock)
- group: ขอบเขตและสิทธิ์ · ความสำคัญ: สูง · trace: AT-10 IDEMPOTENCY_CONFLICT
- actor (role): role=integration tester
- Setup: role=integration tester; POST same key/payload twice
- Start: OPEN `#/records`
- ชุดข้อมูล: A/B/C/D/E ตามเคส
- ผ่านเมื่อ: same identity ref twice and exactly one audit event; requires API integration
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN #/records | — | หน้า ล็อตและซีเรียล ปรากฏ | ☐ |
| 2 | VERIFY API responses | — | same identity ref twice and exactly one audit event; requires API integration | ☐ |

## วิธีที่ agent รัน (Run protocol)
เปิด route ตาม Start; เตรียม fixture ตาม Setup; ทดสอบ action ทีละแถว; บันทึกหลักฐานเฉพาะที่เห็นจริง. เคส system/mock ต้อง simulate ตาม FRD และไม่อ้างว่า prototype พิสูจน์ integration. Browser render NOT-CHECKED ใน lane; QA ต้องรันจริงก่อน visual acceptance.

## Coverage Audit
| หมวด | mapped / total |
|---|---|
| FRD acceptance | 12 / 12 |
| Business rules | 9 / 9 |
| Edge cases | 3 / 3 |
| Errors | 12 / 12 |
| Permission cells | 5 / 5 |
| Cross-module | 4 / 4 |
| Scope lock | 1 / 1 |
- Manifest cross-check: 10/10 stories, 9/9 rules, 3/3 edge classes referenced in FRD; production-only errors below remain deliberately simulated or out of HTML scope.
- ข้าม: errors with no visible HTML surface require production API integration, specifically . No downstream posting/delivery or 7C outcome is tested.

## Result Report (schema)
```json
{"feature_id":"F-WH-LOT","run_at":"<ISO datetime>","results":[{"id":"TC-001","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}],"summary":{"total":59,"pass":0,"fail":0,"blocked":0}}
```
