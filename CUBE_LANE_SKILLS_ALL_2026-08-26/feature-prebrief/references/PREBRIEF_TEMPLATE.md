# PREBRIEF Template v2 — 12 sections

ไฟล์: `PREBRIEF_[F-code]_[Name].md` · ที่มาต่อข้อ: **[แผน] / [มติ] / [AI-DRAFT]** (+[STD])
ตัวอย่างในนี้ใช้ GRN (Goods Receipt) เพราะครบทุกความยาก — feature ง่ายกว่าตัด section ที่ N/A ได้แต่ต้องเขียนว่า N/A เพราะอะไร

```markdown
# PREBRIEF · [Feature EN] — [ชื่อไทย]
> Module · Wave · จาก PB_[code] + Central Plan v[x.y] · วันที่
> เอกสารนี้คือ source of truth เชิง business ของ feature — [AI-DRAFT] รอเคาะผ่าน wireframe review

## 0. Obligations — พันธะจากต้นทาง (ทุกแถวต้องถูกอ้างกลับ)
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | เส้นเข้า: PO → GRN (รับตามใบสั่งซื้อ) [doc] | Central Plan §3 | §2, S-01..S-04 |
| OB-2 | เส้นออก: GRN → Inventory (stock ขยับ) [post] | Central Plan §3 | S-01, §9 |
| OB-3 | เส้นออก: GRN → AP Invoice (3-way match) | Central Plan §4 | §9 |
| OB-4 | สถานะเอกสารกลางตาม DocHeader contract | Contract Slice | §5 |
| OB-5 | หมายเหตุแผน: "หนักสุด 12 rules" | Central Plan | §4 ครบ 12 |

## 1. สรุป + ผู้ใช้ + สิทธิ์
- ทำอะไร 2-3 ประโยค [แผน]
- | Role | เห็นอะไร | ทำอะไรได้ |

## 2. Scenarios — ทุกกรณีที่เกิดได้ (derive จาก D1-D6)
> บันทึกการ derive: D1→S-01..03 · D2→S-05,S-07 · D3→S-04 · D4→S-06 · D5→ผลใน S-01 · D6[STD]→S-08
| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ scenario นี้ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | รับครบตาม PO | ทุก line รับ = ค้างรับ | qty รับครั้งนี้/line | stock+ · PO→"รับครบ" · GR/IR ตั้ง |
| S-02 | Alt | รับบางส่วน | บาง line รับ < ค้างรับ | qty บางส่วน | PO→"รับบางส่วน" ค้างรับเหลือถูกต้อง |
| S-03 | Alt/Exception | รับเกิน | รับ > ค้างรับ | tolerance % (config) | ≤tol รับได้+เตือน · >tol บล็อก [AI-DRAFT][STD] — OQ ถ้ายังไม่มีมติ |
| S-04 | Exception | QC ไม่ผ่าน (ทั้งใบ/บาง line) | ของถึงแต่ไม่รับเข้า stock | **เหตุผล reject · จำนวน reject/line · disposition (คืน/รอตรวจซ้ำ/ทำลาย) · ผู้ตรวจ** | line reject ไม่เข้า stock · เปิดทาง RTV |
| S-05 | Exception | ยกเลิก GRN | ก่อน/หลัง post ต่างกัน | เหตุผลยกเลิก | หลัง post = reversal stock [AI-DRAFT][STD] |
| S-06 | Exception | PO ต้นทางถูกยกเลิก/แก้ระหว่างรับ | เปิด GRN ไม่ได้/เตือน | — | บล็อก + ชี้ไป PO |
| S-07 | Alt | บันทึกร่างค้างไว้ | ยังไม่ post | — | ไม่กระทบ stock |
| S-08 | ไม่รองรับ | รับโดยไม่มี PO | — | — | **ไม่รองรับใน phase นี้ [มติ/OQ]** — เขียนชัด ห้ามเงียบ |

## 3. Data — full data dict
### 3.1 Header
| Field | ชนิด | บังคับ | Default | ที่มา | Validation | ที่มาข้อ |
(เลขที่ auto · อ้าง PO (combobox master→soft ref) · วันที่รับ · ผู้รับ · คลัง/bin · หมายเหตุ)
### 3.2 Lines (grid ตาม B2 v7)
| Field | ชนิด | ... |
(สินค้า[จาก PO line] · **qty สั่ง · รับแล้วสะสม · รับครั้งนี้ · คงเหลือ(computed)** · UoM ·
 ผล QC/line · จำนวน reject · เหตุผล · disposition · bin ปลายทาง)
### 3.3 Computed / แสดงอย่างเดียว
(คงเหลือ = สั่ง − รับสะสม − รับครั้งนี้ · สถานะรวมใบ derive จาก lines)
### 3.4 Config ที่ feature นี้อ่าน
(tolerance รับเกิน · เปิด/ปิด QC step — ชี้ว่า config อยู่ feature ไหน + mock ยังไง)

## 4. Business Rules
| BR | กติกา | พฤติกรรมเมื่อชน | scenario ที่เกี่ยว | ที่มา |
| BR-01 | รับครั้งนี้ ≤ คงเหลือ+tolerance | เกิน tol = บล็อก+บอกเหตุ | S-03 | [AI-DRAFT][STD] |
| BR-02 | line ที่ QC reject ไม่เข้า stock | แยกยอดชัด | S-04 | [แผน] |
(ครบตามพันธะ — GRN ตัวอย่างต้องได้ ~12 ตาม note แผน)

## 5. State Machine
ร่าง → รอตรวจ(ถ้าเปิด QC) → รับเข้าแล้ว(posted) → ยกเลิก(reversal)
| จาก | ไป | ใครกด | เงื่อนไข | scenario |
(ทุก transition ผูก scenario · DOA ถ้ามี = placeholder ตามกติกากลาง)

## 6. Actions ต่อหน้า
| หน้า | action | enable เมื่อ | ทำอะไร | toast/ผล |

## 7. Data behaviour
เลขรัน · soft reference (LD-4C-02) · soft archive · audit append-only · ผูก Document Center แนบไฟล์

## 8. Mock Data Spec — ชุดข้อมูลที่ prove ทุก scenario ได้
| ชุด | รายการ | prove scenario ไหน |
| PO-1001 ค้างรับเต็ม 3 lines | รับครบ | S-01 |
| PO-1002 รับไปแล้วบางส่วน | รับเพิ่ม/ค้างเหลือ | S-02 |
| PO-1003 มี line ใกล้เกิน tol | รับเกิน | S-03 |
| PO-1004 ตั้ง QC บังคับ | reject flow | S-04 |
(ห้าม lorem — ชื่อสินค้า/ตัวเลขต้องหน้าตาเหมือนธุรกิจจริง · landing/KPI คำนวณจากชุดนี้แล้วสมเหตุผล)

## 9. Edges + Hotspot + ผลปลายทาง
| ทิศ | คู่ | จุดใน UI | เกิดอะไรที่ปลายทาง (wireframe ต้อง demo แม้ mock) |
(เช่น post S-01 แล้ว → หน้า PO mock แสดงสถานะ "รับครบ")

## 10. OQ + [AI-DRAFT] register → pin
| # | ประเด็น | เจ้าภาพ | pin ที่ |

## 11. Coverage Matrix (ledger — gate อยู่ที่นี่)
| S | BR ที่ใช้ | transition | หน้าจอ/ปุ่ม | FN ใน checklist |
|---|---|---|---|---|
| S-01 | BR-.. | ร่าง→posted | GRN drawer + ปุ่ม post | FN-01,FN-02 |
เงื่อนไขผ่าน: ทุก BR โผล่ ≥1 แถว · ทุก transition โผล่ ≥1 แถว · ทุก S มี UI + FN · ทุก OB ถูกอ้าง
```


## §12 สัญญาณประกาศ (Declaration signals — ให้ S1.8 อ่าน · lane mode บังคับ)
| ท่อ | สัญญาณใน PREBRIEF (อ้าง S-XX/FN-XX) | chip จาก brief | สรุป |
|---|---|---|---|
| DOA | {S-xx: ส่งอนุมัติ/อนุมัติ/ไม่อนุมัติ · มีวงเงิน? } | {✓/—} | need / no / DIVERGENCE |
| NTF | {transition ที่ใครต้องรู้ — ไม่นับ doa_pending/doa_result} | {✓/—} | |
| CSQ | {ผล ต้นทุน/PDPA/บัญชี/งบ/decision → ท่อ EC/SecC/AC/FC/DC} | {✓/—} | |
| DOCCFG | {doc_type · เลขรัน · สำเนา} | {✓/—} | |
| PDF DOC | {เอกสาร/แบบฟอร์มที่ต้องพิมพ์/ส่ง — thai-doc-pdf-generator} | {✓/—} | |
DIVERGENCE: {— หรือรายการ chip≠detect พร้อมเหตุ}
