# QA_AUDIT — F-TMP-002 (qa-friendly-html-generator v3.1 · Lite)

- ต้นทาง: testcases-F-TMP-002.md · MD: **64 เคส**
- เอกสารคน (Lite): **23 เคส** · drop ledger 41 เคส
- ภาพหน้าจอ: ไม่มี — [NO-BROWSER] ข้าม capture.py (regionKey ว่างทุก step)

## Drop ledger
| TC | เหตุผล |
|---|---|
| TC-L02 | ซ้ำกับ TC-L01 |
| TC-L03 | ผูกเลขที่ตัวอย่าง (R16) — ค้นหา/รีเซ็ตครอบด้วย TC-L05 |
| TC-L04 | permutation ของ TC-L05 |
| TC-L06 | permutation ของ TC-L05 |
| TC-L07 | ตรวจโดย AI (testcases MD) |
| TC-L08 | ต้องมีข้อมูลเกินหน้า — ตรวจโดย AI (testcases MD) |
| TC-L10 | ครอบด้วย TC-C05 |
| TC-C02 | ยุบรวมกับ TC-S01 |
| TC-C03 | พฤติกรรม focus — ตรวจโดย AI (testcases MD) |
| TC-C08 | ตรวจโดย AI (testcases MD) |
| TC-V03 | ยุบรวมใน TC-V02 step 3 |
| TC-V04 | permutation ของ TC-V02 |
| TC-V05 | ตรวจโดย AI (testcases MD) |
| TC-V07 | ตรวจโดย AI (testcases MD) |
| TC-K01 | ค่าจาก seed (R16) — คำนวณตรวจใน TC-C01/C04 |
| TC-K02 | ค่าจาก seed (R16) |
| TC-K03 | ค่าจาก seed (R16) |
| TC-K04 | ค่าจาก seed (R16) — ครอบด้วย TC-C04 |
| TC-K05 | ค่าจาก seed (R16) |
| TC-K06 | ตรวจโดย AI (testcases MD) |
| TC-U01 | ตรวจโดย AI (testcases MD) |
| TC-U02 | ยุบรวมใน TC-C01 step 4 |
| TC-S02 | ยุบรวมใน TC-S01 step 2 |
| TC-S04 | simulate สายหลายขั้น — ตรวจโดย AI (testcases MD) |
| TC-S05 | จำลอง API ล้ม — ตรวจโดย AI (testcases MD) |
| TC-S06 | จำลองข้อมูลชนกัน — ตรวจโดย AI (testcases MD) |
| TC-A04 | ทางเลือกของ TC-A01 — ตรวจโดย AI (testcases MD) |
| TC-A05 | แจ้งเตือนปลายทาง (simulate) — ตรวจโดย AI (testcases MD) |
| TC-X02 | permutation ของ TC-X01 |
| TC-X03 | ครอบด้วย TC-P05 + TC-X01 |
| TC-X04 | ตรวจโดย AI (testcases MD) |
| TC-P02 | ต้องพิมพ์ที่อยู่หน้าเว็บ — ตรวจโดย AI (testcases MD) |
| TC-P04 | ตรวจโดย AI (testcases MD) |
| TC-P06 | ต้องสลับผู้ใช้เขตอื่น — ตรวจโดย AI (testcases MD) |
| TC-D03 | ยุบรวมใน TC-D01 step 3 |
| TC-D04 | simulate สาย 6 ขั้น — ตรวจโดย AI (testcases MD) |
| TC-E01 | simulate ปิดแบบเอกสาร — ตรวจโดย AI (testcases MD) |
| TC-E02 | ครอบด้วย TC-C06 |
| TC-E03 | พฤติกรรมเมาส์ — ตรวจโดย AI (testcases MD) |
| TC-E04 | ผลหลังบ้าน — ตรวจโดย AI (testcases MD) |
| TC-E05 | ยังไม่มีกฎ (OQ-06) — ตรวจโดย AI (testcases MD) |

## Merge note
- TC-C02 → TC-S01 · TC-U02 → TC-C01 · TC-S02 → TC-S01 · TC-V03 → TC-V02 · TC-D03 → TC-D01
