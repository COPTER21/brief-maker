# AI Test Cases · F-WH-CYCLE นับตามรอบ

> FULL AI100 · frozen HTML + FRD · 47 cases from one source. Browser/production NOT-CHECKED; `system` cases require API/mock harness and are not manual HTML passes.

## Run protocol
Reset/continue each Setup exactly; inspect DEMO badge when role switch used; record actual result/evidence. Mock assertions stop at payload/ack/unchanged stock, never real W3 posting or CSQ result.

## Coverage ledger
| Source | Case IDs |
|---|---|
| S-01 | TC-001 |
| S-02 | TC-004, TC-005, TC-030 |
| S-03 | TC-031, TC-032 |
| S-04 | TC-002, TC-003, TC-006, TC-011, TC-031, TC-047 |
| S-05 | TC-007, TC-008, TC-009, TC-010, TC-011, TC-042, TC-047 |
| S-06 | TC-012, TC-013, TC-014, TC-015, TC-026, TC-033, TC-046 |
| S-07 | TC-017, TC-039 |
| S-08 | TC-016, TC-018, TC-019, TC-038, TC-040 |
| S-09 | TC-020, TC-021, TC-037 |
| S-10 | TC-022, TC-034, TC-041 |
| US-01 | TC-001 |
| US-02 | TC-004, TC-030 |
| US-03 | TC-032 |
| US-04 | TC-002, TC-011, TC-047 |
| US-05 | TC-008, TC-009, TC-010 |
| US-06 | TC-012, TC-014, TC-033 |
| US-07 | TC-017 |
| US-08 | TC-016, TC-018 |
| US-09 | TC-020, TC-021 |
| US-10 | TC-022 |
| BR-01 | TC-001, TC-002, TC-003, TC-004, TC-005, TC-030, TC-031, TC-032 |
| BR-02 | TC-002, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-042, TC-047 |
| BR-03 | TC-012, TC-014, TC-020, TC-026, TC-033, TC-034, TC-043, TC-046 |
| BR-04 | TC-013, TC-014, TC-015, TC-022, TC-041 |
| BR-05 | TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-037 |
| BR-06 | TC-016, TC-017, TC-018, TC-021, TC-022, TC-038, TC-039, TC-040, TC-044 |
| BR-07 | TC-027, TC-034, TC-035, TC-036, TC-037, TC-040, TC-043 |
| BR-08 | TC-045 |
| FN-01 | TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-047 |
| FN-02 | TC-001, TC-002, TC-004, TC-005, TC-030, TC-031, TC-032, TC-047 |
| FN-03 | TC-008, TC-009, TC-010, TC-011, TC-022, TC-028, TC-041, TC-042, TC-047 |
| FN-04 | TC-012, TC-014, TC-020, TC-026, TC-033, TC-043, TC-046 |
| FN-05 | TC-013, TC-014, TC-015, TC-016, TC-020, TC-021, TC-022, TC-034, TC-035, TC-041 |
| FN-06 | TC-014, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-037, TC-043 |
| FN-07 | TC-016, TC-017, TC-018, TC-021, TC-022, TC-038, TC-039, TC-040, TC-044 |
| FN-08 | TC-005, TC-011, TC-020, TC-021, TC-027, TC-028, TC-035, TC-036, TC-037, TC-040, TC-042, TC-045, TC-047 |
| FN-09 | TC-001, TC-008, TC-023, TC-024, TC-025, TC-026, TC-029 |
| LOCK-01 | TC-023, TC-024, TC-025, TC-028, TC-029 |
| LOCK-02 | TC-001 |
| LOCK-03 | TC-008, TC-012 |
| LOCK-04 | TC-012, TC-029 |
| LOCK-05 | TC-017, TC-020 |
| LOCK-06 | TC-044 |
| LOCK-07 | TC-027 |
| LOCK-08 | TC-045 |
| LOCK-09 | TC-030 |

## Cases

### TC-001 — ค่าเริ่มต้น ABC มูลค่า AABC
- Route: `#/records` · group: abc · trace: S-01 US-01 BR-01 FN-01 FN-02 FN-09 LOCK-02
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด จัดชั้น ABC | `#/records` | แถวเรียง ITEM-101/102/103/104, คะแนน40/30/20/10, คลาส A/A/B/C | ☐ |
| 2 | ตรวจสัดส่วนจริง | — | 40%,30%,20%,10%; ไม่มีคะแนนความถี่ปนค่าเริ่มต้น | ☐ |

### TC-002 — ปรับสัดส่วน 40/40/20 ทำให้ class เปลี่ยน
- Route: `#/records` · group: abc · trace: S-04 US-04 BR-01 BR-02 FN-01 FN-02
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | คลิก แก้เกณฑ์ ABC | — | drawer แสดง basis, effective date, A/B/C, cadence | ☐ |
| 2 | กรอก A/B/C และบันทึก | 40/40/20 | toast บันทึกเกณฑ์ ABC แล้ว; คลาส A/B/B/C และ policy version ใหม่ | ☐ |

### TC-003 — สัดส่วนรวม105 ถูกปฏิเสธ
- Route: `#/records` · group: abc · trace: S-04 BR-01 FN-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แก้เกณฑ์ ABC | — | drawer เปิด | ☐ |
| 2 | กรอก A/B/C แล้วบันทึก | 70/25/10 | เห็น สัดส่วน A/B/C ต้องรวม 100; version และคลาสเดิมไม่เปลี่ยน | ☐ |

### TC-004 — โหมดคะแนนมูลค่า×ความถี่
- Route: `#/records` · group: abc · trace: S-02 US-02 BR-01 FN-01 FN-02
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แก้เกณฑ์ ABC | — | basis มูลค่าเริ่มต้น | ☐ |
| 2 | เลือก มูลค่า × ความถี่ แล้วบันทึก | A70/B20/C10 | คะแนน ITEM-101/102/103/104 เป็น160/90/40/10, ไม่เรียกคะแนนว่าเงิน; policy version ใหม่ | ☐ |

### TC-005 — เปลี่ยนกลับ basis มูลค่า
- Route: `#/records` · group: abc · trace: S-02 BR-01 BR-02 FN-01 FN-02 FN-08
- Setup: ต่อจาก TC-004

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แก้เกณฑ์ ABC แล้วเลือก มูลค่า | — | basis มูลค่า | ☐ |
| 2 | บันทึก | — | คะแนนกลับ40/30/20/10, คลาส A/A/B/C; version ก่อนยังอยู่ audit | ☐ |

### TC-006 — วันที่เริ่มใช้ไม่ถูกต้อง
- Route: `#/records` · group: abc · trace: S-04 BR-02 FN-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แก้เกณฑ์ ABC | — | มีช่องวันที่ | ☐ |
| 2 | ลบวันที่และบันทึก | วันที่ว่าง | เห็น วันที่เริ่มใช้ไม่ถูกต้อง; ไม่เพิ่ม version | ☐ |

### TC-007 — รอบนับต้องเป็นบวก
- Route: `#/records` · group: abc · trace: S-05 BR-02 FN-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แก้เกณฑ์ ABC | — | รอบ A/B/C 1/3/6 | ☐ |
| 2 | กรอก รอบ A=0 แล้วบันทึก | 0/3/6 | เห็น ช่วงเวลาและรอบนับต้องมากกว่า 0; policy เดิมคงอยู่ | ☐ |

### TC-008 — สร้างแผน A จาก Jan31
- Route: `#/history` · group: plan · trace: S-05 US-05 BR-02 FN-03 FN-09
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แผนนับและงานนับ กด สร้างแผนนับ | — | drawer มีสินค้า/คลัง/ผู้ตรวจนับ/วันที่ล่าสุด | ☐ |
| 2 | ค้นหาและเลือก ITEM-101 | ITEM-101 WH-01; counter ปรียา; ล่าสุด2026-01-31 | picker แสดงรหัสและชื่อสินค้า | ☐ |
| 3 | คลิก สร้างแผน | — | แถวใหม่ class A due2026-02-28 ผู้ตรวจนับ PERSON-COUNT-01; captured expected ไม่แสดงต่อ counter | ☐ |

### TC-009 — สร้างแผน B จาก Jan31
- Route: `#/history` · group: plan · trace: S-05 US-05 BR-02 FN-03
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด สร้างแผนนับ | — | drawer เปิด | ☐ |
| 2 | เลือก ITEM-103 และวันที่ล่าสุด | 2026-01-31 | สินค้า ITEM-103 class B | ☐ |
| 3 | คลิก สร้างแผน | — | แถว due2026-04-30 | ☐ |

### TC-010 — สร้างแผน C จาก Jan31
- Route: `#/history` · group: plan · trace: S-05 US-05 BR-02 FN-03
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด สร้างแผนนับ | — | drawer เปิด | ☐ |
| 2 | เลือก ITEM-104 และวันที่ล่าสุด | 2026-01-31 | สินค้า ITEM-104 class C | ☐ |
| 3 | คลิก สร้างแผน | — | แถว due2026-07-31 | ☐ |

### TC-011 — เปลี่ยนนโยบายไม่แก้ due ของแผนเก่า
- Route: `#/history` · group: plan · trace: S-05 US-04 BR-02 FN-03 FN-08
- Setup: รัน TC-008 ก่อน จด due2026-02-28

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด จัดชั้น ABC แก้ A/B/C | 40/40/20 | version ใหม่ | ☐ |
| 2 | กลับ แผนนับและงานนับ ดูแผนจาก TC-008 | — | policy snapshot/version และ due2026-02-28 เดิม | ☐ |

### TC-012 — ผู้ตรวจนับไม่เห็น expected ก่อนนับ
- Route: `#/history` · group: blind · trace: S-06 US-06 BR-03 FN-04 LOCK-04
- Setup: รีเซ็ต fixture; role DEMO ผู้ตรวจนับ; CC-001 expected100 stored fixture

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แผนนับและงานนับ คลิก CC-001 | — | เห็นสินค้า/ล็อต/ตำแหน่ง/หน่วย/กำหนด/สถานะ | ☐ |
| 2 | ตรวจ drawer และตาราง | — | ไม่เห็น expected100, มูลค่า, ผลต่าง; DEMO badge แยกจาก user | ☐ |

### TC-013 — จำนวนว่างส่งไม่ได้
- Route: `#/history` · group: blind · trace: S-06 BR-04 FN-05
- Setup: role DEMO ผู้ตรวจนับ; CC-001 assigned

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | คลิก CC-001 แล้ว บันทึกผลนับ | — | ช่องจำนวนว่าง | ☐ |
| 2 | คลิก ส่งผลนับ | ว่าง | เห็น กรอกจำนวนที่นับได้; ยัง assigned, ไม่มี attempt | ☐ |

### TC-014 — นับศูนย์ถูกต้องและ reviewer เห็นผลต่าง
- Route: `#/history` · group: blind · trace: S-06 US-06 BR-03 BR-04 FN-04 FN-05 FN-06
- Setup: role DEMO ผู้ตรวจนับ; CC-001 expected100

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด CC-001 บันทึกผลนับ | 0 | ช่องแสดง0 | ☐ |
| 2 | คลิก ส่งผลนับ | — | status รอตรวจ; counter ยังไม่เห็น expected/variance | ☐ |
| 3 | สลับ DEMO ผู้ตรวจทาน เปิด ตรวจทานและประวัติ คลิก CC-001 | — | เห็น expected100, counted0, delta−100 | ☐ |

### TC-015 — นับติดลบถูกปฏิเสธ
- Route: `#/history` · group: blind · trace: S-06 BR-04 FN-05
- Setup: role DEMO ผู้ตรวจนับ; CC-001 assigned

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด CC-001 บันทึกผลนับ | −1 | ช่องจำนวน | ☐ |
| 2 | คลิก ส่งผลนับ | −1 | เห็น กรอกจำนวนที่นับได้; ไม่มี attempt | ☐ |

### TC-016 — ส่งผลนับอย่างเดียวยังไม่มี StockAdj
- Route: `#/settings` · group: review · trace: S-08 US-08 BR-05 BR-06 FN-05 FN-06 FN-07
- Setup: role DEMO ผู้ตรวจนับ; CC-001 expected100

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | นับ104 แล้วส่งผล | 104 | status รอตรวจ | ☐ |
| 2 | สลับ DEMO ผู้ตรวจทาน เปิด ตรวจทานและประวัติ | — | เห็น delta+4 แต่ไม่มีปุ่ม ส่งผลต่าง ก่อนรับรอง | ☐ |

### TC-017 — นับตรง100 รับรองแล้วไม่ส่งปรับยอด
- Route: `#/settings` · group: review · trace: S-07 US-07 BR-05 BR-06 FN-06 FN-07
- Setup: รีเซ็ต; CC-001 expected100

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ผู้ตรวจนับส่ง100 | 100 | status รอตรวจ | ☐ |
| 2 | สลับ DEMO ผู้ตรวจทาน เปิด CC-001 ตรวจทาน | — | expected100,counted100,delta0 | ☐ |
| 3 | กรอกเหตุผลแล้วคลิก รับรองผล | ตรงตามจริง | status ตรวจแล้ว; ไม่มีปุ่ม ส่งผลต่าง (mock); onHand fixture100 | ☐ |

### TC-018 — รับรองผลต่าง+4 แล้วส่ง mock หนึ่งครั้ง
- Route: `#/settings` · group: review · trace: S-08 US-08 BR-05 BR-06 FN-06 FN-07
- Setup: รีเซ็ต; CC-001 expected100

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ผู้ตรวจนับส่ง104 | 104 | รอตรวจ | ☐ |
| 2 | ผู้ตรวจทานเปิด ตรวจทาน กรอกเหตุผลและรับรอง | ตรวจแล้ว | status ตรวจแล้ว, delta+4 | ☐ |
| 3 | เปิด CC-001 และคลิก ส่งผลต่าง (mock) | — | toast ส่งคำขอปรับยอดจำลอง SA-MOCK-001; onHand100/movement unchanged | ☐ |

### TC-019 — รับรองไม่มีเหตุผลถูกปฏิเสธ
- Route: `#/settings` · group: review · trace: S-08 BR-05 FN-06
- Setup: รีเซ็ต; ผู้ตรวจนับส่ง104, reviewer DEMO

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด CC-001 คลิก ตรวจทาน | — | เห็น expected/count/delta | ☐ |
| 2 | เว้นเหตุผลแล้วคลิก รับรองผล | ว่าง | เห็น ระบุเหตุผลการรับรอง; status รอตรวจ | ☐ |

### TC-020 — ขอนับใหม่เปิดฟอร์มว่าง
- Route: `#/settings` · group: recount · trace: S-09 US-09 BR-03 BR-05 FN-04 FN-05 FN-06 FN-08
- Setup: รีเซ็ต; ผู้ตรวจนับส่ง97, reviewer DEMO

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด CC-001 คลิก ตรวจทาน | expected100,counted97,delta−3 | เห็นผลต่าง | ☐ |
| 2 | คลิก ขอนับใหม่ | — | status นับใหม่; attempt97 ล็อก | ☐ |
| 3 | สลับ DEMO ผู้ตรวจนับ เปิด CC-001 บันทึกผลนับ | — | ช่องจำนวนว่าง, ไม่เห็น expected100/variance/97 | ☐ |

### TC-021 — นับใหม่99 ใช้ delta ล่าสุด−1
- Route: `#/settings` · group: recount · trace: S-09 US-09 BR-05 BR-06 FN-05 FN-06 FN-07 FN-08
- Setup: ต่อจาก TC-020 recount requested

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ผู้ตรวจนับกรอก99 และส่ง | 99 | status รอตรวจ attempt รุ่น2 | ☐ |
| 2 | ผู้ตรวจทานเปิด ตรวจทานและประวัติ คลิก CC-001 | — | expected100,counted99,delta−1 | ☐ |
| 3 | กรอกเหตุผล รับรอง แล้วส่งผลต่าง mock | นับใหม่แล้ว | payload mock counted99/delta−1 ไม่ใช้97/−3; onHand100 | ☐ |

### TC-022 — นับ3box snapshot12 เป็น36/base +12
- Route: `#/settings` · group: uom · trace: S-10 US-10 BR-04 BR-06 FN-03 FN-05 FN-07
- Setup: รีเซ็ต; CC-002 expectedBase24, factorSnapshot12pcs/box

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ผู้ตรวจนับเปิด CC-002 และส่ง3 | 3 box | status รอตรวจ | ☐ |
| 2 | ผู้ตรวจทานเปิด CC-002 | — | expectedBase24,countedBase36,delta+12 | ☐ |
| 3 | รับรองพร้อมเหตุผลแล้วส่ง mock | ตรวจแล้ว | payload expected24,counted36,delta+12; ไม่ปรับยอดจริง | ☐ |

### TC-023 — ค้นหารหัสงานนับ
- Route: `#/history` · group: list · trace: FN-09 LOCK-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แผนนับและงานนับ | — | เห็น CC-001/002 | ☐ |
| 2 | กรอกค้นหา | CC-001 | เห็นเฉพาะ CC-001; footer แสดง1จาก2 | ☐ |

### TC-024 — กรองสถานะรอนับ
- Route: `#/history` · group: list · trace: FN-09 LOCK-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด แผนนับและงานนับ | — | มีแถวรอนับ | ☐ |
| 2 | เลือกตัวกรองสถานะ รอนับ | — | แถวที่เห็นเป็นรอนับและ footer ตรงจำนวน | ☐ |

### TC-025 — ล้างตัวกรองคืนรายการ
- Route: `#/history` · group: list · trace: FN-09 LOCK-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ค้น CC-001 และเลือกสถานะรอนับ | — | ผลแคบลง | ☐ |
| 2 | คลิก ล้างตัวกรอง | — | เห็นรายการเต็มและ footer ตรงทั้งหมด | ☐ |

### TC-026 — ส่งออกผู้ตรวจนับไม่รั่ว expected
- Route: `#/settings` · group: list · trace: S-06 BR-03 FN-04 FN-09
- Setup: role DEMO ผู้ตรวจนับ; CC-001 มี attempt

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด ตรวจทานและประวัติ | — | ช่องผลนับ/ผลต่างเป็น — | ☐ |
| 2 | คลิก ส่งออก | — | CSV ไม่มี expected100, value หรือ variance; หากยังไม่มี browser ให้ blocked ไม่ใช่ pass | ☐ |

### TC-027 — event audit append-only
- Route: `#/settings` · group: list · trace: BR-07 FN-08 LOCK-07
- Setup: รัน TC-018 ก่อน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด ตรวจทานและประวัติ คลิก CC-001 | — | สถานะส่งผลต่างแล้ว | ☐ |
| 2 | ตรวจรายการเหตุการณ์ | — | มี count.submitted/count.reviewed/stockadj.mock_ack ตามเวลา; ไม่มีปุ่มแก้/ลบ | ☐ |

### TC-028 — ยกเลิกแผนไม่เพิ่ม session
- Route: `#/history` · group: list · trace: FN-03 FN-08 LOCK-01
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด สร้างแผนนับ แล้วกรอกสินค้า | ITEM-101 | drawer มีค่า | ☐ |
| 2 | คลิก ยกเลิก | — | drawer ปิด; จำนวนแผนและ event เท่าฐาน | ☐ |

### TC-029 — แท็บใต้ page-head และ DEMO แยกผู้ใช้
- Route: `#/records` · group: list · trace: LOCK-01 LOCK-04 FN-09
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด จัดชั้น ABC | — | tab row ใต้ page-head, action ขวาบน | ☐ |
| 2 | สลับ DEMO ผู้ตรวจนับ/ผู้ตรวจทาน | — | badge DEMO ส้มติด selector; ไม่มี hint/banner; ไม่อ้างว่าเป็นสิทธิ์จริง | ☐ |

### TC-030 — default and weighted fixture ranking (ต้อง simulate)
- Route: `#/records` · group: system · trace: S-02 US-02 BR-01 FN-02
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | X100×1 Y50×4 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | X100×1 Y50×4 | default X first; weighted Y score200 first, separate policy snapshots | ☐ |

### TC-031 — zero score all C and negative rejected (ต้อง simulate)
- Route: `#/records` · group: system · trace: S-03 S-04 BR-01 FN-02
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | two zero items, then value−1 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | two zero items, then value−1 | all C without NaN; negative policy snapshot rejected | ☐ |

### TC-032 — stable tie overshoot (ต้อง simulate)
- Route: `#/records` · group: system · trace: S-03 US-03 BR-01 FN-02
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | codes01–04 scores30/30/20/20 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | codes01–04 scores30/30/20/20 | A,A,A,B actual A80/B20/C0; refresh stable | ☐ |

### TC-033 — counter API projection redacted (ต้อง simulate)
- Route: `#/history` · group: system · trace: S-06 US-06 BR-03 FN-04
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | GET API-04 counter before/after/recount/export | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | GET API-04 counter before/after/recount/export | JSON/CSV/errors lack expected/value/variance, reviewer after submit has them | ☐ |

### TC-034 — unassigned counter denied (ต้อง simulate)
- Route: `#/history` · group: system · trace: S-10 BR-03 BR-07 FN-05
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | PERSON-X POST attempt CC-001 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | PERSON-X POST attempt CC-001 | 403, no attempt/event; owner counter allowed | ☐ |

### TC-035 — same submit key replay once (ต้อง simulate)
- Route: `#/history` · group: system · trace: BR-07 FN-05 FN-08
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | POST attempt count100 keyK1 twice | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | POST attempt count100 keyK1 twice | one immutable attempt/ref and event | ☐ |

### TC-036 — same key different count conflict (ต้อง simulate)
- Route: `#/history` · group: system · trace: BR-07 FN-08
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | keyK1 count100 then101 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | keyK1 count100 then101 | IDEMPOTENCY_CONFLICT; no second attempt | ☐ |

### TC-037 — old attempt review rejected after recount (ต้อง simulate)
- Route: `#/settings` · group: system · trace: S-09 BR-05 BR-07 FN-06 FN-08
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | attempt97 old, then new99, accept old | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | attempt97 old, then new99, accept old | STALE_ATTEMPT; new99 remains pending | ☐ |

### TC-038 — mock dispatch before review rejected (ต้อง simulate)
- Route: `#/settings` · group: system · trace: S-08 BR-06 FN-07
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | submitted104 no review | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | submitted104 no review | PRE_REVIEW_DISPATCH; W3 mock count unchanged | ☐ |

### TC-039 — zero delta no mock (ต้อง simulate)
- Route: `#/settings` · group: system · trace: S-07 BR-06 FN-07
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | reviewed100 vs100 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | reviewed100 vs100 | ZERO_DELTA; W3 mock count0 | ☐ |

### TC-040 — mock retry one ref unchanged stock (ต้อง simulate)
- Route: `#/settings` · group: system · trace: S-08 BR-06 BR-07 FN-07 FN-08
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | reviewed104 keyD1 twice | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | reviewed104 keyD1 twice | one SA-MOCK ref; onHand/movement byte-equal baseline | ☐ |

### TC-041 — UoM mapping change does not rewrite snapshot (ต้อง simulate)
- Route: `#/settings` · group: system · trace: S-10 BR-04 FN-03 FN-05
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | CC-002 3box factor12 then source factor10 | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | CC-002 3box factor12 then source factor10 | countedBase36/delta+12 immutable | ☐ |

### TC-042 — policy version does not reschedule old plan (ต้อง simulate)
- Route: `#/history` · group: system · trace: S-05 BR-02 FN-03 FN-08
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | Jan31 plan dueFeb28 then new policy | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | Jan31 plan dueFeb28 then new policy | old policySnapshot/due unchanged | ☐ |

### TC-043 — cross-tenant RLS and reviewer authorization (ต้อง simulate)
- Route: `#/settings` · group: system · trace: BR-03 BR-07 FN-04 FN-06
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | tenant other; counter tries review | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | tenant other; counter tries review | 403 no disclosure/mutation | ☐ |

### TC-044 — W3 StockAdj mock boundary (ต้อง simulate)
- Route: `#/settings` · group: system · trace: BR-06 LOCK-06 FN-07
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | reviewed nonzero payload | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | reviewed nonzero payload | ack/ref only; no actual adjustment approval/posting or stock mutation | ☐ |

### TC-045 — CSQ draft only (ต้อง simulate)
- Route: `#/settings` · group: system · trace: BR-08 LOCK-08 FN-08
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | count.reviewed candidate | baseline/actor/version พร้อม | ☐ |
| 2 | เรียกสัญญาที่ระบุ | count.reviewed candidate | envelope draft; no 7C registration/stamp | ☐ |

### TC-046 — counter บังคับ reviewer view หรือ ABC value ไม่ผ่าน (ต้อง simulate)
- Route: `#/settings` · group: system · trace: S-06 BR-03 FN-04
- Setup: role=backend/integration tester; ต้อง simulate API/mocks; HTML-only ไม่ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม counter assigned CC-001 | GET API-04 ?view=reviewer และ API-03 value/export | counter token | ☐ |
| 2 | เรียก view/endpoint ข้ามสิทธิ์ | counter token | 403 หรือ projection ปิด expected/value/variance ทุก response/CSV/error; DEMO switch ไม่เปลี่ยนสิทธิ์ | ☐ |

### TC-047 — future policy ใช้ตามวันที่แผน ไม่เปลี่ยนย้อนหลัง
- Route: `#/history` · group: plan · trace: S-04 S-05 US-04 BR-02 FN-01 FN-02 FN-03 FN-08
- Setup: รีเซ็ต fixture ABC: ITEM-101/102/103/104 มูลค่า40/30/20/10 ความถี่4/3/2/1; policy basis=value,A70/B20/C10; ผู้ตรวจนับ PERSON-COUNT-01; W3 mock only

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด จัดชั้น ABC ตั้งนโยบายใหม่เริ่ม 2026-10-01 | A40/B40/C20 | version ใหม่รอมีผล; current Sep14 class ยัง A/A/B/C | ☐ |
| 2 | สร้างแผน ITEM-102 วันที่สร้าง2026-09-20 ล่าสุด Jan31 | — | policy ABC-01,class A,due2026-02-28 | ☐ |
| 3 | สร้างแผน ITEM-102 วันที่สร้าง2026-10-02 ล่าสุด Jan31 | — | policy ABC-02,class B,due2026-04-30; แผน Sep20 ไม่เปลี่ยน | ☐ |

## Result schema
`{"feature_id":"F-WH-CYCLE","results":[{"id":"TC-001","status":"pass|fail|blocked","evidence":""}],"summary":{"total":47}}`

Coverage: 46/46 source IDs, 47 cases, 17 system/mock only. No browser execution claimed.
