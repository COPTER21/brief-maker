# AI Test Cases · F-WH-QHOLD กักคุณภาพ

> FULL AI 100% · 2026-09-14 · frozen HTML and FRD 00–08 · browser/production integration NOT-CHECKED. `system` cases ต้อง simulate backend/mock และไม่คิดเป็น manual HTML pass.

## Run protocol
Reset/continue each fixture exactly as Setup; perform every action then record actual and evidence. For DEMO approval, inspect badge and treat it as incoming mock decision only. Never claim actual DOA/GRN/sale/transfer/NC/CSQ result.

## Coverage ledger
| Source | Case IDs |
|---|---|
| S-01 | TC-001, TC-020, TC-021 |
| S-02 | TC-002, TC-003, TC-026, TC-034 |
| S-03 | TC-003, TC-004, TC-005 |
| S-04 | TC-004, TC-005, TC-006 |
| S-05 | TC-006, TC-007, TC-008, TC-009, TC-010, TC-012, TC-013, TC-014, TC-015 |
| S-06 | TC-016, TC-017, TC-036 |
| S-07 | TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-019, TC-022, TC-023, TC-024 |
| S-08 | TC-013, TC-014, TC-015, TC-026, TC-027, TC-028, TC-045 |
| S-09 | TC-016, TC-017, TC-018, TC-035 |
| S-10 | TC-023, TC-024, TC-025, TC-030, TC-043 |
| BR-01 | TC-001, TC-019, TC-020, TC-021, TC-022, TC-040 |
| BR-02 | TC-001, TC-016, TC-017, TC-018, TC-037, TC-038, TC-039 |
| BR-03 | TC-001, TC-002, TC-023, TC-024, TC-025, TC-043 |
| BR-04 | TC-002, TC-003, TC-005, TC-006, TC-026, TC-027, TC-029, TC-044 |
| BR-05 | TC-001, TC-004, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-036 |
| BR-06 | TC-001, TC-003, TC-004, TC-006, TC-012, TC-013, TC-014, TC-015 |
| BR-07 | TC-002, TC-005, TC-032, TC-033, TC-034, TC-035, TC-036, TC-038, TC-045 |
| BR-08 | TC-020, TC-024, TC-039, TC-040, TC-041, TC-042, TC-043 |
| FN-01 | TC-001, TC-025, TC-027, TC-028, TC-030, TC-031, TC-037 |
| FN-02 | TC-001, TC-019, TC-020, TC-021, TC-022, TC-040 |
| FN-03 | TC-001, TC-016, TC-017, TC-018, TC-039 |
| FN-04 | TC-001, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-029 |
| FN-05 | TC-002, TC-003, TC-034, TC-038 |
| FN-06 | TC-004, TC-013, TC-014, TC-015, TC-036 |
| FN-07 | TC-005, TC-006, TC-013, TC-014, TC-015, TC-045 |
| FN-08 | TC-032, TC-033, TC-034, TC-035, TC-036, TC-045 |
| FN-09 | TC-002, TC-020, TC-026, TC-027, TC-028, TC-041, TC-042, TC-044 |
| FN-10 | TC-023, TC-024, TC-025, TC-043 |
| US-01 | TC-001 |
| US-02 | TC-002, TC-003 |
| US-03 | TC-004, TC-005 |
| US-04 | TC-006 |
| US-05 | TC-007, TC-008, TC-009, TC-010, TC-012, TC-013, TC-014, TC-015 |
| US-06 | TC-016, TC-017 |
| US-07 | TC-023, TC-024 |
| US-08 | TC-026, TC-027, TC-028 |
| LOCK-01 | TC-031 |
| LOCK-02 | TC-018 |
| LOCK-03 | TC-001, TC-023 |
| LOCK-04 | TC-026, TC-044 |
| LOCK-05 | TC-019, TC-038, TC-040 |
| LOCK-06 | TC-029 |
| LOCK-07 | TC-031 |
| LOCK-08 | TC-032 |

## Cases

### TC-001 — กักบางส่วนทำให้ pending block ATP
- Route: `#/records` · Group: hold · Trace: S-01 US-01 BR-01 BR-02 BR-03 BR-05 BR-06 FN-01 FN-02 FN-03 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิดแท็บ รายการกัก | `#/records` | เห็นแถว SL-001 และ ATP90 | ☐ |
| 2 | คลิก เพิ่มการกัก แล้วเลือก SL-001 | สินค้า ITEM-101 / LOT-001 | drawer แสดง On-hand100 / จองขาย10 / ATP90 / กักได้90 | ☐ |
| 3 | กรอก จำนวน / ที่มา / เหตุผล | 30 / พบปัญหาภายหลัง / QC pending | แสดงจำนวน30และเหตุผล | ☐ |
| 4 | เลือกผู้อนุมัติสองช่อง | PERSON-01 ผู้ตรวจคุณภาพ และ PERSON-03 หัวหน้าคลัง | เห็นชื่อ ตำแหน่ง แผนก และ DEMO | ☐ |
| 5 | คลิก ส่งคำขอ | — | toast ส่งคำขอรออนุมัติแล้ว; สถานะรออนุมัติ, รอกัก30, กักมีผล0, ATP60, On-hand100 | ☐ |

### TC-002 — อนุมัติกักโดยจำลอง DOA
- Route: `#/history` · Group: decision · Trace: S-02 US-02 BR-03 BR-04 BR-07 FN-05 FN-09
- Setup: ต่อจาก TC-001; QH-001 requested, pendingHeld30, ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิดแท็บ รออนุมัติ | `#/history` | เห็น QH-001 จำนวน30 | ☐ |
| 2 | คลิกคำขอ QH-001 | — | drawer แสดงผู้อนุมัติสองคนและ DEMO | ☐ |
| 3 | คลิก จำลองอนุมัติ | — | toast ผลอนุมัติจำลอง; กลับรายการกัก activeHeld30,pendingHeld0,ATP60,onHand100 | ☐ |

### TC-003 — ไม่อนุมัติกักคืน ATP
- Route: `#/history` · Group: decision · Trace: S-03 US-02 BR-04 BR-06 FN-05
- Setup: รีเซ็ต baseline แล้วทำ TC-001 เท่านั้น

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด รออนุมัติ และคลิก QH-001 | — | เห็น requested และ ATP60 | ☐ |
| 2 | คลิก จำลองไม่อนุมัติ | — | คำขอ rejected, pendingHeld0,activeHeld0,ATP90,onHand100; event เพิ่มหนึ่ง | ☐ |

### TC-004 — ขอปล่อย12 ไม่เพิ่ม ATP ก่อนอนุมัติ
- Route: `#/records` · Group: release · Trace: S-04 US-03 BR-05 BR-06 FN-06
- Setup: รีเซ็ต baseline; ทำ TC-001→TC-002; activeHeld30,ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด รายการกัก แล้วคลิก SL-001 | — | เห็น กักมีผล30, ปล่อยได้30, ATP60 | ☐ |
| 2 | คลิก ขอปล่อยกัก | — | drawer แสดง จำนวน และผู้อนุมัติ | ☐ |
| 3 | กรอกจำนวน/เหตุผล/ที่มา | 12 / ตรวจผ่าน / พบปัญหาภายหลัง | จำนวน12 | ☐ |
| 4 | เลือก PERSON-01 และ PERSON-03 แล้วคลิก ส่งคำขอ | — | requested release12; pendingRelease12, releasable18,activeHeld30,ATP60 | ☐ |

### TC-005 — อนุมัติปล่อย12 เพิ่ม ATP ครั้งเดียว
- Route: `#/history` · Group: release · Trace: S-04 US-03 BR-04 BR-07 FN-07
- Setup: ต่อจาก TC-004; activeHeld30,pendingRelease12,ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด รออนุมัติ แล้วคลิกคำขอปล่อย | — | เห็นจำนวน12และ DEMO | ☐ |
| 2 | คลิก จำลองอนุมัติ | — | activeHeld18,pendingRelease0,ATP72,onHand100; event release.approved เพิ่มหนึ่ง | ☐ |

### TC-006 — ปฏิเสธปล่อยคง held เดิม
- Route: `#/history` · Group: release · Trace: S-05 US-04 BR-04 BR-06 FN-07
- Setup: รีเซ็ต; ทำ TC-001→TC-002→TC-004

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิดคำขอปล่อย12ใน รออนุมัติ | — | requested | ☐ |
| 2 | คลิก จำลองไม่อนุมัติ | — | activeHeld30,pendingRelease0,releasable30,ATP60 | ☐ |

### TC-007 — ปฏิเสธกักจำนวน 91
- Route: `#/records` · Group: validation · Trace: S-07 US-05 BR-05 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001/คนครบ | — | drawer เปิดและมี ATP90 | ☐ |
| 2 | กรอก จำนวนแล้วส่งคำขอ | 91 | จำนวนกักเกินยอดที่กักได้; ไม่มีคำขอใหม่,ATP90,onHand100 | ☐ |

### TC-008 — ปฏิเสธกักจำนวน 0
- Route: `#/records` · Group: validation · Trace: S-07 US-05 BR-05 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001/คนครบ | — | drawer เปิดและมี ATP90 | ☐ |
| 2 | กรอก จำนวนแล้วส่งคำขอ | 0 | จำนวนต้องมากกว่า 0; ไม่มีคำขอใหม่,ATP90,onHand100 | ☐ |

### TC-009 — ปฏิเสธกักจำนวน -1
- Route: `#/records` · Group: validation · Trace: S-07 US-05 BR-05 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001/คนครบ | — | drawer เปิดและมี ATP90 | ☐ |
| 2 | กรอก จำนวนแล้วส่งคำขอ | -1 | จำนวนต้องมากกว่า 0; ไม่มีคำขอใหม่,ATP90,onHand100 | ☐ |

### TC-010 — ปฏิเสธกักจำนวน 1.5
- Route: `#/records` · Group: validation · Trace: S-07 US-05 BR-05 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001/คนครบ | — | drawer เปิดและมี ATP90 | ☐ |
| 2 | กรอก จำนวนแล้วส่งคำขอ | 1.5 | จำนวนต้องมากกว่า 0 และตรงหน่วยนับ; ไม่มีคำขอใหม่,ATP90,onHand100 | ☐ |

### TC-011 — จำนวนว่างต้องไม่แปลงเป็น0
- Route: `#/records` · Group: validation · Trace: S-07 BR-05 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001/คนครบ | — | drawer เปิด | ☐ |
| 2 | ปล่อยช่องจำนวนว่างแล้วคลิก ส่งคำขอ | ว่าง | เห็น error จำนวน; ไม่มี request/event เพิ่ม | ☐ |

### TC-012 — กักได้90 และกักเพิ่ม1ถูกปฏิเสธ
- Route: `#/records` · Group: validation · Trace: S-07 US-05 BR-05 BR-06 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ส่งคำขอกัก90พร้อมคนครบ | 90 | pendingHeld90,ATP0 | ☐ |
| 2 | เปิดคำขอกักใหม่และกรอก1 | 1 | จำนวนกักเกินยอดที่กักได้; ไม่มีคำขอที่สอง | ☐ |

### TC-013 — ขอบเขตปล่อย 31
- Route: `#/records` · Group: validation · Trace: S-08 US-05 BR-05 BR-06 FN-06 FN-07
- Setup: รีเซ็ต; ทำ TC-001→TC-002 activeHeld30 ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | คลิก SL-001 แล้ว ขอปล่อยกัก | — | ปล่อยได้30 | ☐ |
| 2 | กรอกจำนวน/เหตุผล/เลือกคนครบแล้วส่ง | 31 | จำนวนปล่อยเกินยอดที่ปล่อยได้ | ☐ |

### TC-014 — ขอบเขตปล่อย 0
- Route: `#/records` · Group: validation · Trace: S-08 US-05 BR-05 BR-06 FN-06 FN-07
- Setup: รีเซ็ต; ทำ TC-001→TC-002 activeHeld30 ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | คลิก SL-001 แล้ว ขอปล่อยกัก | — | ปล่อยได้30 | ☐ |
| 2 | กรอกจำนวน/เหตุผล/เลือกคนครบแล้วส่ง | 0 | จำนวนต้องมากกว่า 0 | ☐ |

### TC-015 — ขอบเขตปล่อย 30
- Route: `#/records` · Group: validation · Trace: S-08 US-05 BR-05 BR-06 FN-06 FN-07
- Setup: รีเซ็ต; ทำ TC-001→TC-002 activeHeld30 ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | คลิก SL-001 แล้ว ขอปล่อยกัก | — | ปล่อยได้30 | ☐ |
| 2 | กรอกจำนวน/เหตุผล/เลือกคนครบแล้วส่ง | 30 | requested release30 ยัง ATP60; อนุมัติแล้ว activeHeld0,ATP90 | ☐ |

### TC-016 — ขาดผู้อนุมัติช่องที่สอง
- Route: `#/records` · Group: doa · Trace: S-09 US-06 BR-02 FN-03
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001 จำนวน30 เหตุผลครบ | — | มีช่องผู้ตรวจคุณภาพ/ผู้รับรองคลัง | ☐ |
| 2 | เลือก PERSON-01 ช่องแรก แล้วคลิกส่ง | ช่องสองว่าง | เห็น เลือกคนให้ครบทุกช่องอนุมัติ; ATP90 ไม่มีคำขอ | ☐ |

### TC-017 — ผู้ไม่อยู่ในรายชื่อเลือกไม่ได้
- Route: `#/records` · Group: doa · Trace: S-09 US-06 BR-02 FN-03
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิดเพิ่มการกัก เลือก SL-001 จำนวน30 | — | เห็น picker | ☐ |
| 2 | ค้น PERSON-04 ในช่องผู้ตรวจคุณภาพ | PERSON-04 | ไม่พบตัวเลือก PERSON-04 ในช่องนั้น; ไม่สามารถส่งด้วยผู้ไม่เข้าเกณฑ์ | ☐ |

### TC-018 — ชื่อจริง/ตำแหน่ง/แผนกและ DEMO
- Route: `#/records` · Group: doa · Trace: S-09 BR-02 LOCK-02 FN-03
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001 จำนวน30 | — | ช่องผู้อนุมัติปรากฏ | ☐ |
| 2 | เปิด picker ทั้งสอง | — | แต่ละตัวเลือกแสดง initials avatar, ชื่อ, ตำแหน่ง, แผนก; badge DEMO | ☐ |
| 3 | เลือก PERSON-01 และ PERSON-03 | — | ช่องแสดงชื่อและตำแหน่ง; ไม่มี role-ID เป็นตัวเลือก | ☐ |

### TC-019 — GRN QC ต้องมีอ้างอิง
- Route: `#/records` · Group: source · Trace: S-07 BR-01 FN-02
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001 จำนวน10 และคนครบ | — | drawer เปิด | ☐ |
| 2 | เลือกที่มา ตรวจรับ GRN QC เว้นอ้างอิง | — | ระบุอ้างอิง GRN QC; ไม่มีคำขอ | ☐ |

### TC-020 — GRN QC mock ref ถูก snapshot
- Route: `#/history` · Group: source · Trace: S-01 BR-01 BR-08 FN-02 FN-09
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ส่งกัก10 ที่มา ตรวจรับ GRN QC | GRN-2609-014 + เหตุผล + คนครบ | requested; ไม่มีการรับสินค้าใหม่ | ☐ |
| 2 | เปิด รออนุมัติ คลิกคำขอ | — | เห็นอ้างอิง GRN-2609-014; onHand ไม่เปลี่ยน | ☐ |

### TC-021 — พบปัญหาภายหลังไม่ต้อง GRN ref
- Route: `#/records` · Group: source · Trace: S-01 BR-01 FN-02
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก SL-001 จำนวน10 | ที่มา พบปัญหาภายหลัง; อ้างอิงว่าง | drawer ยอมให้ว่าง | ☐ |
| 2 | กรอกเหตุผล/คนครบ แล้วส่ง | — | requested; sourceRef null,ATP80 | ☐ |

### TC-022 — เหตุผลว่างถูกปฏิเสธ
- Route: `#/records` · Group: source · Trace: S-07 BR-01 FN-02
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิดเพิ่มการกัก SL-001 จำนวน10 คนครบ | เหตุผลว่าง | drawer เปิด | ☐ |
| 2 | คลิก ส่งคำขอ | — | ระบุเหตุผล; ไม่มีคำขอหรือ ATP change | ☐ |

### TC-023 — held30 ATP60 ปฏิเสธ outbound61
- Route: `#/records` · Group: availability · Trace: S-10 US-07 BR-03 FN-10
- Setup: รีเซ็ต; ทำ TC-001→TC-002; activeHeld30 ATP60

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด SL-001 drawer | — | เห็น ATP พร้อมใช้60 | ☐ |
| 2 | กรอก ตรวจจำนวนขาย/ย้ายที่ใช้ได้ แล้วคลิก ตรวจจำนวน | 61 | จำนวนนี้ใช้ไม่ได้ · พร้อมใช้ 60 · ยังไม่มีการขายหรือย้ายจริง | ☐ |

### TC-024 — outbound60 ผ่านการตรวจแต่ไม่ขายจริง
- Route: `#/records` · Group: availability · Trace: S-10 US-07 BR-03 BR-08 FN-10
- Setup: รีเซ็ต; ทำ TC-001→TC-002

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด SL-001 drawer แล้วกรอกตรวจจำนวน | 60 | จำนวนนี้พร้อมใช้ · พร้อมใช้ 60 · ยังไม่มีการขายหรือย้ายจริง | ☐ |
| 2 | ดู On-hand/กัก/ATP อีกครั้ง | — | 100/30/60 เท่าเดิม | ☐ |

### TC-025 — อีกล็อตไม่ถูกกักตาม SL-001
- Route: `#/records` · Group: availability · Trace: S-10 BR-03 FN-01 FN-10
- Setup: รีเซ็ต; ทำ TC-001→TC-002

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | ค้น SL-002 ในรายการกัก | SL-002 | เห็นแถวอีก slice | ☐ |
| 2 | คลิก SL-002 | — | activeHeld0,pendingHeld0; ATP คำนวณจาก SL-002 เอง ไม่รับ30จาก SL-001 | ☐ |

### TC-026 — ประวัติ append-only หลังคำขอและผล
- Route: `#/settings` · Group: history · Trace: S-02 US-08 BR-04 FN-09
- Setup: รีเซ็ต; ทำ TC-001→TC-002

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิดแท็บ ประวัติ | `#/settings` | เห็น hold.requested และ hold.approved ผูก QH-001 | ☐ |
| 2 | คลิกแต่ละเหตุการณ์ | — | เห็น actor/time/source/qty; ไม่มีปุ่มแก้ไขหรือลบ | ☐ |

### TC-027 — ค้นหาเหตุการณ์ตามคำขอ
- Route: `#/settings` · Group: history · Trace: US-08 BR-04 FN-01 FN-09
- Setup: รีเซ็ต; ทำ TC-001→TC-002

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด ประวัติ แล้วกรอกค้นหา | QH-001 | เห็นเฉพาะเหตุการณ์ QH-001 | ☐ |
| 2 | กรอกค้นหา | ZZ-NO-REQUEST | empty state; footer จำนวนตรงแถวที่เห็น | ☐ |

### TC-028 — กรองสถานะรออนุมัติ
- Route: `#/history` · Group: list · Trace: US-08 FN-01 FN-09
- Setup: รีเซ็ต; ทำ TC-001

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด รออนุมัติ | — | เห็น QH-001 | ☐ |
| 2 | กรองสถานะ รออนุมัติ | — | ทุกแถวที่เห็นเป็นรออนุมัติ; footer ตรงจำนวน | ☐ |

### TC-029 — ยกเลิก drawer ไม่เปลี่ยน ATP
- Route: `#/records` · Group: list · Trace: LOCK-06 BR-04 FN-04
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด เพิ่มการกัก เลือก SL-001 กรอก30 | — | drawer แสดงค่า | ☐ |
| 2 | คลิก ยกเลิก | — | drawer ปิด; ATP90, ไม่มี request/event ใหม่ | ☐ |

### TC-030 — สถิติตารางคำนวณจาก slice
- Route: `#/records` · Group: list · Trace: S-10 FN-01
- Setup: รีเซ็ต; ทำ TC-001→TC-002

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด รายการกัก | — | stat ตำแหน่งสินค้า=จำนวน slice, กักมีผลรวม30, รอกักรวม0 | ☐ |
| 2 | ตรวจ ATP พร้อมใช้ | — | เท่าผลรวม ATP ของทุก slice จากข้อมูล ไม่ใช่ค่าประมาณ | ☐ |

### TC-031 — แท็บอยู่ใต้หัวและ action ขวาบน
- Route: `#/records` · Group: list · Trace: LOCK-01 LOCK-07 FN-01
- Setup: รีเซ็ต fixture SL-001: onHand100, จองขาย10, กักมีผล0, รอกัก0, ATP90; maker Warehouse WH-01

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เปิด รายการกัก | — | tab row ใต้ page-head; เพิ่มการกักที่ action ขวาบน | ☐ |
| 2 | เปิด รออนุมัติ/ประวัติ | — | tab row คงตำแหน่ง ไม่มี hint/banner | ☐ |

### TC-032 — same request key same body replay (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: BR-07 FN-08
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | key K1 body hold30 | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง API-03 ซ้ำ | key K1 body hold30 | คืน requestId เดิม, projection/event ครั้งเดียว | ☐ |

### TC-033 — same key different body conflict (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: BR-07 FN-08
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | key K1 body hold31 | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง API-03 ซ้ำต่าง qty | key K1 body hold31 | IDEMPOTENCY_CONFLICT; no second reservation | ☐ |

### TC-034 — same DOA event replay (ต้อง simulate)
- Route: `#/history` · Group: system · Trace: S-02 BR-07 FN-05 FN-08
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | approve QH-001 | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง API-04 sourceEventId E1 ซ้ำ | approve QH-001 | held30/ATP60 เท่าเดิม; applied event เดียว | ☐ |

### TC-035 — decision after rejected blocked (ต้อง simulate)
- Route: `#/history` · Group: system · Trace: S-09 BR-07 FN-08
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | QH-001 rejected | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง API-04 approve หลัง reject | QH-001 rejected | INVALID_TRANSITION; ATP90 ไม่เปลี่ยน | ☐ |

### TC-036 — concurrent release stale version (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: S-06 BR-05 BR-07 FN-06 FN-08
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | release20 vs release15 held30 same version | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง API-03 สอง writer | release20 vs release15 held30 same version | รายแรก pending20; รายสอง VERSION_CONFLICT หรือ OVER_RELEASE; releasable10 | ☐ |

### TC-037 — cross-tenant slice denied (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: BR-02 FN-01
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | slice SL-X | มี baseline ที่ระบุ | ☐ |
| 2 | อ่าน/เขียน API-01/03 tenant อื่น | slice SL-X | 403 ACCESS_DENIED, no disclosure/mutation | ☐ |

### TC-038 — maker cannot decide via UI/API (ต้อง simulate)
- Route: `#/history` · Group: system · Trace: BR-02 BR-07 FN-05
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | approve own request | มี baseline ที่ระบุ | ☐ |
| 2 | เรียก API-04 จาก maker client | approve own request | 403; adapter-only external signed event | ☐ |

### TC-039 — DOA policy unavailable no request (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: BR-02 BR-08 FN-03
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | hold30 | มี baseline ที่ระบุ | ☐ |
| 2 | จำลอง API-02 unavailable | hold30 | 503/retryable; no request/projection/false approval | ☐ |

### TC-040 — GRN mock only (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: BR-01 BR-08 FN-02
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | hold30 | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง hold with GRN-2609-014 ref | hold30 | request source snapshot only; W3 GRN count/onHand unchanged | ☐ |

### TC-041 — NC/NTF candidate only (ต้อง simulate)
- Route: `#/settings` · Group: system · Trace: BR-08 FN-09
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | inventory.quarantine_changed | มี baseline ที่ระบุ | ☐ |
| 2 | capture outbox after approved hold | inventory.quarantine_changed | envelope once; no delivery/recipient/channel claim | ☐ |

### TC-042 — CSQ draft only (ต้อง simulate)
- Route: `#/settings` · Group: system · Trace: BR-08 FN-09
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | inventory.quarantine_changed | มี baseline ที่ระบุ | ☐ |
| 2 | capture candidate after approved hold | inventory.quarantine_changed | facts once; no 7C stamp or registry | ☐ |

### TC-043 — availability consumer no transaction (ต้อง simulate)
- Route: `#/records` · Group: system · Trace: S-10 BR-03 BR-08 FN-10
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | sell61 held30 ATP60 | มี baseline ที่ระบุ | ☐ |
| 2 | เรียก API-07 แล้วตรวจ downstream | sell61 held30 ATP60 | denied; sale/transfer records and movement unchanged | ☐ |

### TC-044 — held request immutable and ledger unchanged (ต้อง simulate)
- Route: `#/settings` · Group: system · Trace: BR-04 FN-09
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | movement baseline snapshot | มี baseline ที่ระบุ | ☐ |
| 2 | compare DB before/after hold+decision | movement baseline snapshot | movement rows byte-for-byte unchanged; qh_event append only | ☐ |

### TC-045 — release replay no ATP inflation (ต้อง simulate)
- Route: `#/history` · Group: system · Trace: S-08 BR-07 FN-07 FN-08
- Setup: role=integration/backend tester; ต้อง simulate API/DOA/Inventory fixture; ห้ามนับว่า HTML ผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|:---:|
| 1 | เตรียม backend/mock fixture | held30→0 | มี baseline ที่ระบุ | ☐ |
| 2 | ส่ง approve release30 E2 ซ้ำ | held30→0 | ATP90 ทั้งสองครั้ง, ไม่ใช่120; event ครั้งเดียว | ☐ |

## Result report
`{"feature_id":"F-WH-QHOLD","results":[{"id":"TC-001","status":"pass|fail|blocked","evidence":""}],"summary":{"total":45}}`

Coverage: 44/44 source IDs; 45 cases, 14 backend/mock-only. No browser execution claimed.
