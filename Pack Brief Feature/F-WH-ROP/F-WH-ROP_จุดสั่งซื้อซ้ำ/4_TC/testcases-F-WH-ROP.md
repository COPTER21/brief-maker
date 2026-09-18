# AI Test Cases — F-WH-ROP จุดสั่งซื้อซ้ำ

ทดสอบจาก FRD/BRD และข้อความใน frozen HTML; backend/mock cases ระบุ `(ต้อง simulate)` และไม่อ้างว่าเบราว์เซอร์หรือ integration ผ่านแล้ว.

## Meta
| Field | Value |
|---|---|
| Feature ID | F-WH-ROP |
| Version | 1.0 · 2026-09-14 |
| App entry | Warehouse → Reorder Point |
| Routes | `#/records`, `#/history`, `#/settings` |
| Source | BRD APPROVED AI, FRD 00–08, frozen HTML hash |
| Count | 60 cases; local browser run NOT-CHECKED |

## Coverage
| Group | Cases |
|---|---:|
| policy | 20 |
| suggestion | 12 |
| mock | 13 |
| history | 1 |
| list | 4 |
| system | 10 |

## Coverage Ledger
| Item | Cases |
|---|---|
| AT-01 | TC-001 |
| AT-02 | TC-002 |
| AT-03 | TC-003 |
| AT-04 | TC-004 |
| AT-05 | TC-005 |
| AT-06 | TC-006 |
| AT-07 | TC-007 |
| AT-08 | TC-008 |
| AT-09 | TC-009 |
| AT-10 | TC-010 |
| AT-11 | TC-011 |
| AT-12 | TC-012 |
| AT-13 | TC-013 |
| AT-14 | TC-014 |
| AT-15 | TC-015 |
| AT-16 | TC-016 |
| AT-17 | TC-017 |
| AT-18 | TC-018 |
| S-01 | TC-001, TC-036 |
| S-02 | TC-003, TC-004 |
| S-03 | TC-005 |
| S-04 | TC-006 |
| S-05 | TC-007, TC-031 |
| S-06 | TC-008 |
| S-07 | TC-010, TC-032 |
| S-08 | TC-018, TC-033 |
| S-09 | TC-009 |
| S-10 | TC-012 |
| S-11 | TC-013, TC-014 |
| S-12 | TC-015 |
| S-13 | TC-011, TC-040 |
| BR-01 | TC-001, TC-008, TC-010, TC-032, TC-036, TC-037, TC-039 |
| BR-02 | TC-001 |
| BR-03 | TC-002, TC-003 |
| BR-04 | TC-005, TC-006, TC-007, TC-028, TC-031, TC-032 |
| BR-05 | TC-009, TC-017, TC-029, TC-030 |
| BR-06 | TC-015, TC-044, TC-045, TC-046, TC-060 |
| BR-07 | TC-012, TC-041, TC-042 |
| BR-08 | TC-011, TC-013, TC-016, TC-039, TC-040, TC-043, TC-047 |
| R-01 | TC-001, TC-008, TC-010, TC-012, TC-032, TC-036, TC-037, TC-039, TC-041, TC-053 |
| R-02 | TC-001, TC-013 |
| R-03 | TC-002, TC-003, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, TC-025 |
| R-04 | TC-005, TC-006, TC-007, TC-028, TC-031, TC-032 |
| R-05 | TC-009, TC-017, TC-029, TC-030, TC-034, TC-035 |
| R-06 | TC-015, TC-044, TC-045, TC-046, TC-060 |
| R-07 | TC-012, TC-041, TC-042 |
| R-08 | TC-011, TC-013, TC-016, TC-039, TC-040, TC-043, TC-047 |
| LOCK-01 | TC-018, TC-026, TC-050, TC-058 |
| LOCK-02 | TC-027 |
| LOCK-03 | TC-044, TC-054 |
| LOCK-04 | TC-017, TC-047 |
| LOCK-05 | TC-047, TC-053 |
| LOCK-06 | TC-038, TC-058 |
| WF-FN-01 | TC-018, TC-048, TC-049, TC-050 |
| WF-FN-02 | TC-001, TC-003, TC-010, TC-039 |
| WF-FN-03 | TC-008, TC-010, TC-033 |
| WF-FN-04 | TC-005, TC-006, TC-007, TC-009 |
| WF-FN-05 | TC-005, TC-007, TC-033 |
| WF-FN-06 | TC-015, TC-044, TC-046 |
| WF-FN-07 | TC-012, TC-013, TC-014, TC-041 |
| WF-FN-08 | TC-011, TC-040, TC-047 |
| REQUIRED | TC-019, TC-020, TC-021 |
| BAD_REFERENCE | TC-024, TC-025 |
| POLICY_BOUNDS | TC-003, TC-022, TC-023 |
| BAD_EFFECTIVE_DATE | TC-004 |
| VERSION_CONFLICT | TC-051 |
| SNAPSHOT_UNAVAILABLE | TC-034 |
| SNAPSHOT_STALE | TC-035 |
| NO_POSITIVE_SUGGESTION | TC-042 |
| MOCK_UNAVAILABLE | TC-014, TC-043 |
| IDEMPOTENCY_CONFLICT | TC-052 |
| NC_RULE_MISSING | TC-045 |
| ACCESS_DENIED | TC-058 |
| NO_POLICY | TC-033 |
| XT-PR-01 | TC-012, TC-041, TC-053 |
| XT-PR-02 | TC-013 |
| XT-NC-01 | TC-015, TC-044, TC-054 |
| XT-NC-02 | TC-016, TC-046, TC-060 |
| XT-INV-01 | TC-017 |
| FN-09 | TC-048, TC-049 |
| CSQ | TC-059 |
| NTF | TC-060 |

## Data Sets
| Set | Fields | Values |
|---|---|---|
| A | policy | ITEM-101/WH-01 min10 max30 safety5, snapshot onHand20 held12 asOf 2026-09-14 |
| B | equality | ITEM-103/WH-01 available10 min10 max30 |
| C | below | ITEM-104/WH-01 available9 min10 max30 |
| D | above | ITEM-101/WH-02 available35 min25 max60 |
| E | missing | ITEM-116 no policy |
| Files | — | no upload cases |

## Test Cases

### Group: policy

### TC-001 — บันทึกนโยบายแยกคู่สินค้าและคลัง
- group: policy · ความสำคัญ: สูง · trace: AT-01 S-01 BR-01 BR-02 R-01 R-02 WF-FN-02
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มีแถว ITEM-116/WH-01 รุ่นแรกและข้อความ **บันทึกนโยบายแล้ว**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **เพิ่มนโยบาย** | — | drawer แสดงช่อง สินค้า, คลัง, ขั้นต่ำ, สูงสุด, Stock ปลอดภัย, วันที่เริ่มใช้ | ☐ |
| 3 | SELECT สินค้า **ITEM-116** และคลัง **WH-01** จากเมนูค้นหา | ITEM-116 / WH-01 | ช่องแสดงรหัสที่เลือกจริง | ☐ |
| 4 | TYPE ช่อง **ขั้นต่ำ**, **สูงสุด**, **Stock ปลอดภัย** | 10 / 30 / 5 | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | CLICK ปุ่ม **บันทึก** | — | มีแถว ITEM-116/WH-01 รุ่นแรกและข้อความ **บันทึกนโยบายแล้ว** | ☐ |

### TC-002 — ขอบเขตค่าเท่ากันยอมรับ
- group: policy · ความสำคัญ: สูง · trace: AT-02 BR-03 R-03
- actor (role): maker
- Setup: role=maker · seed=เปิด drawer นโยบาย ITEM-115 WH-01 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: min10 max10 safety10
- ผ่านเมื่อ: drawer ปิดและมี policy version ใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | min10 max10 safety10 | drawer ปิดและมี policy version ใหม่ | ☐ |

### TC-003 — ปฏิเสธ safety เกิน min
- group: policy · ความสำคัญ: สูง · trace: AT-03 S-02 BR-03 POLICY_BOUNDS WF-FN-02
- actor (role): maker
- Setup: role=maker · seed=drawer คู่ ITEM-115 WH-01 กรอกค่าแล้ว · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: min10 max20 safety11
- ผ่านเมื่อ: เห็นข้อความ **ต้องเป็น 0 ≤ safety ≤ min ≤ max** และ drawer ไม่ปิด

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | min10 max20 safety11 | เห็นข้อความ **ต้องเป็น 0 ≤ safety ≤ min ≤ max** และ drawer ไม่ปิด | ☐ |

### TC-004 — ปฏิเสธวันที่ไม่ถูกต้อง
- group: policy · ความสำคัญ: สูง · trace: AT-04 S-02 BAD_EFFECTIVE_DATE
- actor (role): maker
- Setup: role=maker · seed=drawer คู่ ITEM-115 WH-01 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: วันที่ 2026-99-99
- ผ่านเมื่อ: เห็นข้อความ **กรอกวันที่เริ่มใช้** หรือช่อง date ไม่รับค่า; ไม่มี version ใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | วันที่ 2026-99-99 | เห็นข้อความ **กรอกวันที่เริ่มใช้** หรือช่อง date ไม่รับค่า; ไม่มี version ใหม่ | ☐ |

### TC-008 — คลังเดียวกันต้องใช้นโยบายของตัวเอง
- group: policy · ความสำคัญ: สูง · trace: AT-08 S-06 BR-01 WF-FN-03
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: คู่ WH-02
- ผ่านเมื่อ: แสดงขั้นต่ำ 25 และสูงสุด 60 ต่างจาก WH-01 ที่ขั้นต่ำ 10/สูงสุด30

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-02** | คู่ WH-02 | แสดงขั้นต่ำ 25 และสูงสุด 60 ต่างจาก WH-01 ที่ขั้นต่ำ 10/สูงสุด30 | ☐ |

### TC-010 — นโยบายอนาคตยังไม่แทนตัวปัจจุบัน
- group: policy · ความสำคัญ: สูง · trace: AT-10 S-07 BR-01 [ASSUMED] WF-FN-02 WF-FN-03
- actor (role): maker
- Setup: role=maker · seed=policy ITEM-101 WH-01 รุ่น1 มีผล · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ITEM-101/WH-01 ยังใช้รุ่นที่มีผลวันที่ 2026-09-14

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN แท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นแถว ITEM-101/WH-01 รุ่นปัจจุบัน | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-01** | — | drawer แสดงรุ่น/เริ่มใช้ปัจจุบัน | ☐ |
| 3 | CLICK ปุ่ม **แก้ไขนโยบาย** | — | drawer มีช่องค่าของนโยบาย | ☐ |
| 4 | TYPE ช่อง **วันที่เริ่มใช้** | 2026-10-01 | ช่องแสดง 2026-10-01 | ☐ |
| 5 | TYPE ช่อง **สูงสุด** | 40 | ช่องแสดง 40 | ☐ |
| 6 | CLICK ปุ่ม **บันทึก** | — | toast **บันทึกนโยบายแล้ว** และรุ่นใหม่ **รอมีผล** | ☐ |
| 7 | OPEN แท็บ **คำแนะนำเติม** ที่ `#/history` | — | ITEM-101/WH-01 ยังใช้รุ่นที่มีผลวันที่ 2026-09-14 | ☐ |

### TC-011 — การบันทึกเพิ่มเหตุการณ์
- group: policy · ความสำคัญ: สูง · trace: AT-11 S-13 BR-08 WF-FN-08
- actor (role): auditor
- Setup: role=auditor · seed=รัน TC-001 ก่อน · files=—
- Start: OPEN `#/settings`
- ชุดข้อมูล: บันทึก policy หนึ่งครั้งใน TC-001
- ผ่านเมื่อ: มี event ใหม่อ้าง policy รุ่นที่บันทึกและเวลา

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **ประวัติ** ที่ `#/settings` | — | เห็นหัวข้อ **ประวัติ** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY แถวเหตุการณ์ **policy.saved** | บันทึก policy หนึ่งครั้งใน TC-001 | มี event ใหม่อ้าง policy รุ่นที่บันทึกและเวลา | ☐ |

### TC-019 — ช่องขั้นต่ำว่างต้องปฏิเสธ
- group: policy · ความสำคัญ: สูง · trace: REQUIRED R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย ITEM-116 WH-02 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ขั้นต่ำว่าง สูงสุด30 safety5
- ผ่านเมื่อ: เห็น **กรอกตัวเลขให้ครบ** และไม่มีแถวใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | ขั้นต่ำว่าง สูงสุด30 safety5 | เห็น **กรอกตัวเลขให้ครบ** และไม่มีแถวใหม่ | ☐ |

### TC-020 — ช่องสูงสุดว่างต้องปฏิเสธ
- group: policy · ความสำคัญ: สูง · trace: REQUIRED R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย ITEM-116 WH-02 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: min10 สูงสุดว่าง safety5
- ผ่านเมื่อ: เห็น **กรอกตัวเลขให้ครบ** และ drawer ไม่ปิด

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | min10 สูงสุดว่าง safety5 | เห็น **กรอกตัวเลขให้ครบ** และ drawer ไม่ปิด | ☐ |

### TC-021 — ช่อง safety ว่างต้องปฏิเสธ
- group: policy · ความสำคัญ: สูง · trace: REQUIRED R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย ITEM-116 WH-02 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: min10 max30 safetyว่าง
- ผ่านเมื่อ: เห็น **กรอกตัวเลขให้ครบ**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | min10 max30 safetyว่าง | เห็น **กรอกตัวเลขให้ครบ** | ☐ |

### TC-022 — ค่าติดลบปฏิเสธ
- group: policy · ความสำคัญ: สูง · trace: POLICY_BOUNDS R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย ITEM-116 WH-02 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: min -1 max30 safety0
- ผ่านเมื่อ: เห็น **ต้องเป็น 0 ≤ safety ≤ min ≤ max**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | min -1 max30 safety0 | เห็น **ต้องเป็น 0 ≤ safety ≤ min ≤ max** | ☐ |

### TC-023 — min เกิน max ปฏิเสธ
- group: policy · ความสำคัญ: สูง · trace: POLICY_BOUNDS R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย ITEM-116 WH-02 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: min31 max30 safety5
- ผ่านเมื่อ: เห็น error ขอบเขตและไม่มี policy version เพิ่ม

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | min31 max30 safety5 | เห็น error ขอบเขตและไม่มี policy version เพิ่ม | ☐ |

### TC-024 — รหัสสินค้าไม่อยู่ master
- group: policy · ความสำคัญ: สูง · trace: BAD_REFERENCE R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ITEM-999 / WH-01
- ผ่านเมื่อ: เห็น **เลือกสินค้าและคลังจากรายการ**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | ITEM-999 / WH-01 | เห็น **เลือกสินค้าและคลังจากรายการ** | ☐ |

### TC-025 — รหัสคลังไม่อยู่ master
- group: policy · ความสำคัญ: สูง · trace: BAD_REFERENCE R-03
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบาย · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ITEM-101 / WH-99
- ผ่านเมื่อ: เห็น **เลือกสินค้าและคลังจากรายการ**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | ITEM-101 / WH-99 | เห็น **เลือกสินค้าและคลังจากรายการ** | ☐ |

### TC-026 — searchable picker กรองสินค้า
- group: policy · ความสำคัญ: สูง · trace: UI master picker LOCK-01
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบายเปิด · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ITEM-103
- ผ่านเมื่อ: เมนูตัวเลือกแสดง ITEM-103 และเลือกได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | TYPE ช่อง **สินค้า** | ITEM-103 | เมนูตัวเลือกแสดง ITEM-103 และเลือกได้ | ☐ |

### TC-027 — searchable picker กรองคลัง
- group: policy · ความสำคัญ: สูง · trace: UI master picker LOCK-02
- actor (role): maker
- Setup: role=maker · seed=drawer เพิ่มนโยบายเปิด · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: WH-02
- ผ่านเมื่อ: เมนูตัวเลือกแสดง WH-02 และเลือกได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | TYPE ช่อง **คลัง** | WH-02 | เมนูตัวเลือกแสดง WH-02 และเลือกได้ | ☐ |

### TC-036 — future date แสดงรอมีผล
- group: policy · ความสำคัญ: สูง · trace: S-01 BR-01
- actor (role): reviewer
- Setup: role=reviewer · seed=รัน TC-010 ก่อน; policy future 2026-10-01 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: effective 2026-10-01
- ผ่านเมื่อ: สถานะ **รอมีผล** แทนมีผล

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวนโยบายวันอนาคต | effective 2026-10-01 | สถานะ **รอมีผล** แทนมีผล | ☐ |

### TC-037 — effective today แสดงมีผล
- group: policy · ความสำคัญ: สูง · trace: BR-01
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: effective วันนี้หรือก่อน
- ผ่านเมื่อ: สถานะ **มีผล**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวนโยบายปัจจุบัน | effective วันนี้หรือก่อน | สถานะ **มีผล** | ☐ |

### TC-038 — cancel drawer ไม่เพิ่ม version
- group: policy · ความสำคัญ: สูง · trace: LOCK-06 UI cancel
- actor (role): maker
- Setup: role=maker · seed=เปิด drawer เพิ่มนโยบาย; จดจำนวน policy ก่อน · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ค่าใน drawer ที่ยังไม่บันทึก
- ผ่านเมื่อ: drawer ปิด; จำนวน/แถว policy เท่าฐานที่จดไว้

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY ตัวเลขสรุป **นโยบาย** ก่อนเปิด drawer | — | จดจำนวนฐานไว้ | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก** | ค่าใน drawer ที่ยังไม่บันทึก | drawer ปิด; จำนวน/แถว policy เท่าฐานที่จดไว้ | ☐ |

### TC-039 — แก้นโยบายเพิ่ม version ไม่ overwrite
- group: policy · ความสำคัญ: สูง · trace: BR-01 BR-08 WF-FN-02
- actor (role): maker
- Setup: role=maker · seed=policy ITEM-101 WH-01 รุ่น1 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มีรุ่นใหม่และ event; รุ่นเก่ายังคงใน audit

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN แท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นแถว ITEM-101/WH-01 | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-01** | — | drawer แสดงรุ่นปัจจุบัน | ☐ |
| 3 | CLICK ปุ่ม **แก้ไขนโยบาย** | — | drawer edit เปิด | ☐ |
| 4 | TYPE ช่อง **ขั้นต่ำ** และ **สูงสุด** | 12 และ 34 | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | CLICK ปุ่ม **บันทึก** | — | มีรุ่นใหม่และ event; รุ่นเก่ายังคงใน audit | ☐ |

### Group: suggestion

### TC-005 — เท่าขั้นต่ำแนะนำถึงสูงสุด
- group: suggestion · ความสำคัญ: สูง · trace: AT-05 S-03 BR-04 R-04 [ASSUMED] WF-FN-04 WF-FN-05
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: fixture available10 min10 max30
- ผ่านเมื่อ: drawer แสดงพร้อมใช้ 10, ขั้นต่ำ/สูงสุด 10/30, จำนวนแนะนำ 20

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-103 / WH-01** | fixture available10 min10 max30 | drawer แสดงพร้อมใช้ 10, ขั้นต่ำ/สูงสุด 10/30, จำนวนแนะนำ 20 | ☐ |

### TC-006 — ต่ำกว่าขั้นต่ำแนะนำ 21
- group: suggestion · ความสำคัญ: สูง · trace: AT-06 S-04 BR-04 [ASSUMED] WF-FN-04
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: fixture available9 min10 max30
- ผ่านเมื่อ: drawer แสดงจำนวนแนะนำ 21

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-104 / WH-01** | fixture available9 min10 max30 | drawer แสดงจำนวนแนะนำ 21 | ☐ |

### TC-007 — สูงกว่าขั้นต่ำไม่มี PR
- group: suggestion · ความสำคัญ: สูง · trace: AT-07 S-05 BR-04 WF-FN-04 WF-FN-05
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: fixture available35 min25
- ผ่านเมื่อ: แสดงจำนวนแนะนำ 0 และไม่มีปุ่ม **แนะนำเปิด PR**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-02** | fixture available35 min25 | แสดงจำนวนแนะนำ 0 และไม่มีปุ่ม **แนะนำเปิด PR** | ☐ |

### TC-009 — หักสินค้ากักออกจากพร้อมใช้
- group: suggestion · ความสำคัญ: สูง · trace: AT-09 S-09 BR-05 [ASSUMED] WF-FN-04
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: onHand20 held12
- ผ่านเมื่อ: แสดง On-hand/กัก 20/12, พร้อมใช้ 8, จำนวนแนะนำ 22

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-01** | onHand20 held12 | แสดง On-hand/กัก 20/12, พร้อมใช้ 8, จำนวนแนะนำ 22 | ☐ |

### TC-028 — available=0 ยังแนะนำถึง max (ต้อง simulate)
- group: suggestion · ความสำคัญ: สูง · trace: BR-04 boundary [ASSUMED]
- actor (role): reviewer
- Setup: role=reviewer · seed=fixture snapshot pair available0 (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: inject onHand0 held0 min10 max30
- ผ่านเมื่อ: เห็นพร้อมใช้0 และจำนวนแนะนำ30

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวคู่ที่ snapshot available0 | inject onHand0 held0 min10 max30 | เห็นพร้อมใช้0 และจำนวนแนะนำ30 | ☐ |

### TC-029 — held เท่ากับ onHand (ต้อง simulate)
- group: suggestion · ความสำคัญ: สูง · trace: BR-05 boundary [ASSUMED]
- actor (role): reviewer
- Setup: role=reviewer · seed=fixture held=onHand (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: inject onHand20 held20
- ผ่านเมื่อ: เห็นพร้อมใช้0 และคำแนะนำตาม max

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวคู่ที่ held=onHand | inject onHand20 held20 | เห็นพร้อมใช้0 และคำแนะนำตาม max | ☐ |

### TC-030 — held เกิน onHand ไม่ติดลบ (ต้อง simulate)
- group: suggestion · ความสำคัญ: สูง · trace: BR-05 edge OQ-ROP-07
- actor (role): reviewer
- Setup: role=reviewer · seed=fixture held>onHand (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: inject onHand10 held12
- ผ่านเมื่อ: พร้อมใช้แสดง0 ไม่ติดลบ; production flags data quality

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวคู่ผิดปกติ | inject onHand10 held12 | พร้อมใช้แสดง0 ไม่ติดลบ; production flags data quality | ☐ |

### TC-031 — ค่า available เหนือ min หนึ่งหน่วย (ต้อง simulate)
- group: suggestion · ความสำคัญ: สูง · trace: S-05 BR-04
- actor (role): reviewer
- Setup: role=reviewer · seed=fixture available11/min10 (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: inject onHand11 held0
- ผ่านเมื่อ: จำนวนแนะนำ0 และไม่มีปุ่ม PR

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวคู่ที่ available11/min10 | inject onHand11 held0 | จำนวนแนะนำ0 และไม่มีปุ่ม PR | ☐ |

### TC-032 — recompute จากค่า config ที่เปลี่ยน
- group: suggestion · ความสำคัญ: สูง · trace: S-07 BR-01 BR-04
- actor (role): reviewer
- Setup: role=reviewer · seed=policy ITEM-101 WH-01 รุ่นใหม่ effective วันนี้ · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: policy min/max รุ่นใหม่ที่มีผล
- ผ่านเมื่อ: คำแนะนำในแถวตรงกับนโยบายรุ่นที่มีผล ไม่ใช่รุ่นเดิม

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **คำนวณใหม่** | policy min/max รุ่นใหม่ที่มีผล | คำแนะนำในแถวตรงกับนโยบายรุ่นที่มีผล ไม่ใช่รุ่นเดิม | ☐ |

### TC-033 — คู่ไม่มีนโยบายแสดงสถานะชัด
- group: suggestion · ความสำคัญ: สูง · trace: S-08 NO_POLICY WF-FN-03 WF-FN-05
- actor (role): reviewer
- Setup: role=reviewer · seed=ITEM-116 ยังไม่มี policy · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ITEM-116 / WH-01
- ผ่านเมื่อ: เห็น **ยังไม่มีนโยบาย** และไม่มีจำนวนแนะนำ

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | SELECT สินค้า **ITEM-116** และคลัง **WH-01** จากเมนู | ITEM-116 / WH-01 | ช่องแสดงคู่ที่เลือกจริง | ☐ |
| 3 | CLICK ปุ่ม **ตรวจนโยบาย** | ITEM-116 / WH-01 | เห็น **ยังไม่มีนโยบาย** และไม่มีจำนวนแนะนำ | ☐ |

### TC-034 — snapshot หายต้องไม่เติมศูนย์ (ต้อง simulate)
- group: suggestion · ความสำคัญ: สูง · trace: SNAPSHOT_UNAVAILABLE R-05
- actor (role): reviewer
- Setup: role=reviewer · seed=remove fixture snapshot for pair (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: คู่มี policy แต่ snapshot หาย
- ผ่านเมื่อ: เห็น **ไม่มีข้อมูลคงเหลือ** ไม่ใช่คำแนะนำ0

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **ตรวจนโยบาย** | คู่มี policy แต่ snapshot หาย | เห็น **ไม่มีข้อมูลคงเหลือ** ไม่ใช่คำแนะนำ0 | ☐ |

### TC-035 — snapshot stale ไม่ออกคำแนะนำบวก (ต้อง simulate)
- group: suggestion · ความสำคัญ: สูง · trace: SNAPSHOT_STALE R-05 OQ-ROP-04
- actor (role): reviewer
- Setup: role=reviewer · seed=backend stale snapshot (ต้อง simulate; local HTML ไม่มี freshness guard) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: snapshot เก่ากว่า owner SLA
- ผ่านเมื่อ: production returns SNAPSHOT_STALE; no positive advice

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **คำนวณใหม่** | snapshot เก่ากว่า owner SLA | production returns SNAPSHOT_STALE; no positive advice | ☐ |

### Group: mock

### TC-012 — คำแนะนำ PR เป็น mock payload
- group: mock · ความสำคัญ: สูง · trace: AT-12 S-10 BR-07 XT-PR-01 WF-FN-07
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ITEM-101 WH-01 qty22
- ผ่านเมื่อ: เห็น **PR-MOCK-** กับ ITEM-101/WH-01/22; ไม่มีข้อความว่าสร้าง PR จริง

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-01** | — | drawer แสดงข้อมูลคำแนะนำและปุ่มที่ตรงกับคู่ | ☐ |
| 3 | CLICK ปุ่ม **แนะนำเปิด PR** | ITEM-101 WH-01 qty22 | เห็น **PR-MOCK-** กับ ITEM-101/WH-01/22; ไม่มีข้อความว่าสร้าง PR จริง | ☐ |

### TC-013 — กด PR ซ้ำไม่เพิ่มคำขอ
- group: mock · ความสำคัญ: สูง · trace: AT-13 S-11 BR-08 XT-PR-02 WF-FN-07
- actor (role): maker
- Setup: role=maker · seed=เปิด suggestion ITEM-101 WH-01 และกด PR แล้วครั้งหนึ่ง · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: คู่และ snapshot เดิม
- ผ่านเมื่อ: เห็น **คำขอเดิม** และ mockRef เดิม

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **แนะนำเปิด PR** อีกครั้ง | คู่และ snapshot เดิม | เห็น **คำขอเดิม** และ mockRef เดิม | ☐ |

### TC-014 — ปลายทาง PR ไม่พร้อม (ต้อง simulate)
- group: mock · ความสำคัญ: สูง · trace: AT-14 S-11 MOCK_UNAVAILABLE WF-FN-07
- actor (role): maker
- Setup: role=maker · seed=fixture ITEM-103 WH-01 · inject mock adapter unavailable (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: inject ropPrAvailable=false
- ผ่านเมื่อ: เห็น **ปลายทาง PR ยังไม่พร้อม**; ไม่มี ack ใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **แนะนำเปิด PR** | inject ropPrAvailable=false | เห็น **ปลายทาง PR ยังไม่พร้อม**; ไม่มี ack ใหม่ | ☐ |

### TC-015 — NC candidate เหนือ ROP min
- group: mock · ความสำคัญ: สูง · trace: AT-15 S-12 BR-06 XT-NC-01 WF-FN-06
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ITEM-101 WH-02 above min
- ผ่านเมื่อ: เห็น **ส่งตัวเลือกให้กฎ NC** และข้อความ **ไม่ใช่ผลการแจ้งเตือน**; ไม่มีข้อความส่งสำเร็จ

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-02** | — | drawer แสดงข้อมูลคำแนะนำและปุ่มที่ตรงกับคู่ | ☐ |
| 3 | CLICK ปุ่ม **ส่งตัวเลือกให้กฎ NC** | ITEM-101 WH-02 above min | เห็น **ส่งตัวเลือกให้กฎ NC** และข้อความ **ไม่ใช่ผลการแจ้งเตือน**; ไม่มีข้อความส่งสำเร็จ | ☐ |

### TC-016 — NC candidate ซ้ำ
- group: mock · ความสำคัญ: สูง · trace: AT-16 BR-08 XT-NC-02
- actor (role): maker
- Setup: role=maker · seed=กด NC candidate คู่ ITEM-101 WH-02 แล้วหนึ่งครั้ง · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: snapshot/ruleRef เดิม
- ผ่านเมื่อ: เห็น **รายการนี้ส่งแล้ว** และไม่เพิ่ม candidate ซ้ำ

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **ส่งตัวเลือกให้กฎ NC** อีกครั้ง | snapshot/ruleRef เดิม | เห็น **รายการนี้ส่งแล้ว** และไม่เพิ่ม candidate ซ้ำ | ☐ |

### TC-017 — การแนะนำไม่แก้ stock
- group: mock · ความสำคัญ: สูง · trace: AT-17 BR-05 LOCK-04 XT-INV-01
- actor (role): reviewer
- Setup: role=reviewer · seed=ITEM-101 WH-01 onHand20 held12; ทำ TC-012/15 แล้ว · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: baseline 20/12 ในขั้นต้น
- ผ่านเมื่อ: ยังเห็น 20/12 และพร้อมใช้8 เท่าฐานที่จดไว้

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-01** ก่อน action | — | จดฐาน On-hand/กัก=20/12 และพร้อมใช้=8 | ☐ |
| 3 | CLICK ปุ่ม **แนะนำเปิด PR** | — | เห็น mockRef เท่านั้น | ☐ |
| 4 | VERIFY ช่อง **On-hand / กัก** หลังส่ง PR/NC | baseline 20/12 ในขั้นต้น | ยังเห็น 20/12 และพร้อมใช้8 เท่าฐานที่จดไว้ | ☐ |

### TC-041 — PR payload แยก item/warehouse
- group: mock · ความสำคัญ: สูง · trace: XT-PR-01 BR-07 WF-FN-07
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ITEM-103 WH-01 qty20
- ผ่านเมื่อ: ack แสดง ITEM-103 / WH-01 / 20; ไม่ใช่คู่ ITEM-101

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-103 / WH-01** | — | drawer แสดงข้อมูลคำแนะนำและปุ่มที่ตรงกับคู่ | ☐ |
| 3 | CLICK ปุ่ม **แนะนำเปิด PR** | ITEM-103 WH-01 qty20 | ack แสดง ITEM-103 / WH-01 / 20; ไม่ใช่คู่ ITEM-101 | ☐ |

### TC-042 — PR qty0 ปิด action
- group: mock · ความสำคัญ: สูง · trace: NO_POSITIVE_SUGGESTION BR-07
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ITEM-101 WH-02
- ผ่านเมื่อ: ไม่มีปุ่ม **แนะนำเปิด PR** ใน drawer

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถวที่แนะนำ0 | ITEM-101 WH-02 | ไม่มีปุ่ม **แนะนำเปิด PR** ใน drawer | ☐ |

### TC-043 — PR unavailable ไม่สร้าง event (ต้อง simulate)
- group: mock · ความสำคัญ: สูง · trace: MOCK_UNAVAILABLE BR-08
- actor (role): auditor
- Setup: role=auditor · seed=บันทึกจำนวน pr.mock ก่อน TC-014 · files=—
- Start: OPEN `#/settings`
- ชุดข้อมูล: run TC-014
- ผ่านเมื่อ: จำนวนเหตุการณ์ pr.mock เท่าฐานก่อน inject; ไม่มี ack ใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **ประวัติ** ที่ `#/settings` | — | เห็นหัวข้อ **ประวัติ** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY จำนวนแถวเหตุการณ์ **pr.mock** ก่อนจำลองปลายทางล่ม | — | จดจำนวนฐานไว้ | ☐ |
| 3 | VERIFY เหตุการณ์ **pr.mock** หลัง unavailable | run TC-014 | จำนวนเหตุการณ์ pr.mock เท่าฐานก่อน inject; ไม่มี ack ใหม่ | ☐ |

### TC-044 — NC ไม่ใช่แจ้งเตือนจริง
- group: mock · ความสำคัญ: สูง · trace: LOCK-03 BR-06 XT-NC-01 WF-FN-06
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ruleRef NC-ROP-BASE
- ผ่านเมื่อ: แสดงคำว่า **ไม่ใช่ผลการแจ้งเตือน**; ไม่มี recipient/channel/delivered

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **ITEM-101 / WH-01** | — | drawer แสดงข้อมูลคำแนะนำและปุ่มที่ตรงกับคู่ | ☐ |
| 3 | CLICK ปุ่ม **ส่งตัวเลือกให้กฎ NC** | ruleRef NC-ROP-BASE | แสดงคำว่า **ไม่ใช่ผลการแจ้งเตือน**; ไม่มี recipient/channel/delivered | ☐ |

### TC-045 — ไม่มี NC rule ไม่ส่ง candidate (ต้อง simulate)
- group: mock · ความสำคัญ: สูง · trace: NC_RULE_MISSING BR-06
- actor (role): maker
- Setup: role=maker · seed=policy ncRuleRef ว่าง (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: policy ncRuleRef ว่าง
- ผ่านเมื่อ: ไม่มีปุ่ม NC หรือเห็น error **ไม่มีกฎแจ้งเตือนที่ผูกไว้**

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK ปุ่ม **ส่งตัวเลือกให้กฎ NC** | policy ncRuleRef ว่าง | ไม่มีปุ่ม NC หรือเห็น error **ไม่มีกฎแจ้งเตือนที่ผูกไว้** | ☐ |

### TC-046 — NC candidate มี stock facts ไม่ใช่ threshold (ต้อง simulate)
- group: mock · ความสำคัญ: สูง · trace: XT-NC-02 BR-06 WF-FN-06
- actor (role): integration_tester
- Setup: role=integration_tester · seed=mock adapter capture payload (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: ITEM-101 WH-01 onHand20 held12 available8
- ผ่านเมื่อ: payload มีคู่/กฎ/พร้อมใช้/asOf และไม่มี channel/recipient

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY mock envelope จาก NC candidate | ITEM-101 WH-01 onHand20 held12 available8 | payload มีคู่/กฎ/พร้อมใช้/asOf และไม่มี channel/recipient | ☐ |

### TC-047 — history append-only หลัง PR/NC
- group: mock · ความสำคัญ: สูง · trace: LOCK-04 LOCK-05 BR-08 WF-FN-08
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/settings`
- ชุดข้อมูล: หลัง TC-012 และ TC-015
- ผ่านเมื่อ: เห็นสอง event แยกอ้างอิง; ไม่มีปุ่มลบหรือแก้ไข

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **ประวัติ** ที่ `#/settings` | — | เห็นหัวข้อ **ประวัติ** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY แถว **pr.mock** และ **nc.candidate** | หลัง TC-012 และ TC-015 | เห็นสอง event แยกอ้างอิง; ไม่มีปุ่มลบหรือแก้ไข | ☐ |

### Group: history

### TC-040 — ประวัตินโยบายแสดงรุ่นและวันที่
- group: history · ความสำคัญ: กลาง · trace: S-13 BR-08 WF-FN-08
- actor (role): auditor
- Setup: role=auditor · seed=รัน TC-039 ก่อน; มี policy.saved event · files=—
- Start: OPEN `#/settings`
- ชุดข้อมูล: event จาก TC-039
- ผ่านเมื่อ: drawer แสดง **รุ่น/เริ่มใช้** และอ้างอิง policy เดิม

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **ประวัติ** ที่ `#/settings` | — | เห็นหัวข้อ **ประวัติ** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | CLICK แถว **policy.saved** | event จาก TC-039 | drawer แสดง **รุ่น/เริ่มใช้** และอ้างอิง policy เดิม | ☐ |

### Group: list

### TC-018 — รายการนโยบายและคู่ที่ยังไม่ตั้ง
- group: list · ความสำคัญ: กลาง · trace: AT-18 S-08 LOCK-01 WF-FN-01
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: fixture 30 configured; ITEM-116 ไม่มี
- ผ่านเมื่อ: มีรายการตาม policy จริง; ไม่สร้างนโยบาย ITEM-116 เอง

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY แถวและตัวเลข **นโยบาย** | fixture 30 configured; ITEM-116 ไม่มี | มีรายการตาม policy จริง; ไม่สร้างนโยบาย ITEM-116 เอง | ☐ |

### TC-048 — ค้นหาด้วยรหัสสินค้า
- group: list · ความสำคัญ: กลาง · trace: FN-09 UI search WF-FN-01
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ITEM-101
- ผ่านเมื่อ: แถวที่เห็นมี ITEM-101 และจำนวนใน footer สอดคล้องกับแถว

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | TYPE ช่อง **ค้นหา** | ITEM-101 | แถวที่เห็นมี ITEM-101 และจำนวนใน footer สอดคล้องกับแถว | ☐ |

### TC-049 — กรองสถานะนโยบาย
- group: list · ความสำคัญ: กลาง · trace: FN-09 UI filter WF-FN-01
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: มีผล
- ผ่านเมื่อ: ทุกแถวที่เห็นแสดง **มีผล**; footer นับตามผลกรอง

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | SELECT ตัวกรอง **สถานะ** | มีผล | ทุกแถวที่เห็นแสดง **มีผล**; footer นับตามผลกรอง | ☐ |

### TC-050 — ค้นหาไม่พบแสดง empty state
- group: list · ความสำคัญ: กลาง · trace: LOCK-01 UI empty WF-FN-01
- actor (role): warehouse_policy_maker
- Setup: role=warehouse_policy_maker · seed=ROP demo fixture asOf 2026-09-14 · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: ZZ-NO-ITEM
- ผ่านเมื่อ: เห็น **ไม่พบรายการที่ตรงกับตัวกรอง** และไม่มีแถว

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | TYPE ช่อง **ค้นหา** | ZZ-NO-ITEM | เห็น **ไม่พบรายการที่ตรงกับตัวกรอง** และไม่มีแถว | ☐ |

### Group: system

### TC-051 — version conflict server rejects stale write (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: VERSION_CONFLICT API-02
- actor (role): backend_tester
- Setup: role=backend_tester · seed=two writers same policy, API harness (ต้อง simulate) · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: stale version
- ผ่านเมื่อ: VERSION_CONFLICT, prior row/event unchanged

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY API response after stale expectedVersion | stale version | VERSION_CONFLICT, prior row/event unchanged | ☐ |

### TC-052 — same idempotency key different body rejected (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: IDEMPOTENCY_CONFLICT API-04
- actor (role): backend_tester
- Setup: role=backend_tester · seed=accepted mock PR key, API harness (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: same key, different qty
- ผ่านเมื่อ: IDEMPOTENCY_CONFLICT; no second mock event

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY API-04 conflict response | same key, different qty | IDEMPOTENCY_CONFLICT; no second mock event | ☐ |

### TC-053 — PR contract does not create W2 PR (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: XT-PR-01 LOCK-05
- actor (role): integration_tester
- Setup: role=integration_tester · seed=W2-PUR-LITE PR count baseline, mock contract harness (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: valid PR payload
- ผ่านเมื่อ: mock ack only; W2-PUR-LITE PR count unchanged from baseline

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY จำนวน PR ของ W2-PUR-LITE ก่อนส่ง mock | — | จดจำนวนฐานจาก contract harness | ☐ |
| 3 | VERIFY mock adapter records | valid PR payload | mock ack only; W2-PUR-LITE PR count unchanged from baseline | ☐ |

### TC-054 — NC candidate does not deliver (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: XT-NC-01 LOCK-03
- actor (role): integration_tester
- Setup: role=integration_tester · seed=NC delivery count baseline, mock harness (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: valid NC envelope
- ผ่านเมื่อ: candidate ack only; notification delivery count unchanged from baseline

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY จำนวนการส่งแจ้งเตือนก่อน NC candidate | — | จดจำนวนฐานจาก contract harness | ☐ |
| 3 | VERIFY mock NC adapter records | valid NC envelope | candidate ack only; notification delivery count unchanged from baseline | ☐ |

### TC-055 — maker scoped policy write allowed (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: permission Maker allow
- actor (role): backend_tester
- Setup: role=backend_tester · seed=maker assigned WH-01, API harness (ต้อง simulate) · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: authorized tenant/warehouse
- ผ่านเมื่อ: new version accepted and auditable

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY API-02 response | authorized tenant/warehouse | new version accepted and auditable | ☐ |

### TC-056 — reviewer policy write denied (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: permission Reviewer deny
- actor (role): backend_tester
- Setup: role=backend_tester · seed=reviewer no write grant, API harness (ต้อง simulate) · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: reviewer tries write
- ผ่านเมื่อ: ACCESS_DENIED, policy/event unchanged

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY รุ่นและจำนวน event ของ policy ก่อน write | — | จดค่าฐานจาก API harness | ☐ |
| 3 | VERIFY API-02 response | reviewer tries write | ACCESS_DENIED, policy/event unchanged | ☐ |

### TC-057 — auditor read allowed but write denied (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: permission Auditor read/deny
- actor (role): backend_tester
- Setup: role=backend_tester · seed=auditor scoped account, API harness (ต้อง simulate) · files=—
- Start: OPEN `#/settings`
- ชุดข้อมูล: auditor credentials
- ผ่านเมื่อ: history scoped read succeeds, policy write ACCESS_DENIED

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **ประวัติ** ที่ `#/settings` | — | เห็นหัวข้อ **ประวัติ** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY API-06 then API-02 | auditor credentials | history scoped read succeeds, policy write ACCESS_DENIED | ☐ |

### TC-058 — cross-tenant access denied and scope locked (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: ACCESS_DENIED LOCK-01 LOCK-06
- actor (role): backend_tester
- Setup: role=backend_tester · seed=two tenants, API harness (ต้อง simulate) · files=—
- Start: OPEN `#/records`
- ชุดข้อมูล: other tenant policy ref
- ผ่านเมื่อ: ACCESS_DENIED and no disclosure/write; console/no wizard scope unchanged

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **นโยบายเติมสินค้า** ที่ `#/records` | — | เห็นหัวข้อ **นโยบายเติมสินค้า** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY API-01/02 cross-tenant response | other tenant policy ref | ACCESS_DENIED and no disclosure/write; console/no wizard scope unchanged | ☐ |

### TC-059 — CSQ declaration is producer contract only (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: CSQ BR-CSQ-01–05
- actor (role): integration_tester
- Setup: role=integration_tester · seed=CSQ owner contract harness (ต้อง simulate) · files=—
- Start: OPEN `#/settings`
- ชุดข้อมูล: policy.changed event candidate
- ผ่านเมื่อ: envelope may be captured after commit; no 7C tube stamp/registration claimed

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **ประวัติ** ที่ `#/settings` | — | เห็นหัวข้อ **ประวัติ** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY local declaration and backend outbox | policy.changed event candidate | envelope may be captured after commit; no 7C tube stamp/registration claimed | ☐ |

### TC-060 — NTF declaration is candidate only (ต้อง simulate)
- group: system · ความสำคัญ: กลาง · trace: NTF BR-06 XT-NC-02
- actor (role): integration_tester
- Setup: role=integration_tester · seed=NC owner contract harness (ต้อง simulate) · files=—
- Start: OPEN `#/history`
- ชุดข้อมูล: reorder candidate
- ผ่านเมื่อ: envelope shape/replay only; no actual alert/delivery

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | OPEN เปิดแท็บ **คำแนะนำเติม** ที่ `#/history` | — | เห็นหัวข้อ **คำแนะนำเติม** และตารางหรือสถานะว่างตามข้อมูลที่มี | ☐ |
| 2 | VERIFY NC/NTF producer envelope | reorder candidate | envelope shape/replay only; no actual alert/delivery | ☐ |

## วิธีที่ agent รัน (Run protocol)
เปิด route ใน Setup; ทำแต่ละ step ตามลำดับ; บันทึกค่าฐานก่อนเทียบ delta; ทำ sys cases เฉพาะเมื่อมี backend/mock harness. หากไม่มี harness ให้ blocked พร้อมเหตุผล ไม่ให้ pass สมมติ. ไม่ทดสอบ live PR/NC/CSQ/stock posting.

## Coverage Audit
| Category | covered / total |
|---|---:|
| Source items | 82 / 82 |
| FRD AT | 18 / 18 |
| PREBRIEF S | 13 / 13 |
| BRD BR | 8 / 8 |
| FRD R | 8 / 8 |
| Error catalog | 13 / 13 |
| Scope Lock | 6 / 6 |
| XT | 5 / 5 |
| Cases | 60 / 60 |

Manifest cross-check: ✅ all 8 US, 13 S, 8 BR rows mapped via ledger/cases. OOS excluded: actual W2 PR creation, NC delivery, CSQ registration/stamps, stock/movement mutation. Backend-only cases are retained as sys/ต้อง simulate, never shown as locally passed.

## Result Report (schema)
```json
{"feature_id":"F-WH-ROP","run_at":"<ISO>","results":[{"id":"TC-001","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}],"summary":{"total":60,"pass":0,"fail":0,"blocked":0}}
```
