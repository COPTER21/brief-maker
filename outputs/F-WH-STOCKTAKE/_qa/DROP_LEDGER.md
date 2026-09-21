# UAT Lite Drop Ledger — F-WH-STOCKTAKE

ต้นทาง: `testcases-F-WH-STOCKTAKE.md` จำนวน 27 เคส · เก็บใน UAT Lite 11 เคส

| เคสที่ไม่ใส่ใน UAT | เหตุผล |
|---|---|
| TC-ST-04–07,09,13,15–16,18,20–22 | กฎถูกครอบใน quick flow/negative case ที่รวมขั้นใกล้เคียงแล้ว; เก็บรายละเอียดเต็มใน AI Test Cases |
| TC-ST-23 optimistic concurrency | ต้องใช้ 2 session และ backend revision จริง |
| TC-ST-24 idempotency | ต้องตรวจ request key/side effect ที่ integration layer |
| TC-ST-25 F082 failure | ต้อง stub ปลายทาง F082 |
| TC-ST-26 movement cut-off | ต้องควบคุม transaction time และ inventory service |
| TC-ST-27 production config/demo absence | ต้องตรวจ production build และ DOA config จริง |

ไม่มีเคสใดถูกลบทิ้งจาก coverage; เคสที่ตัดยังอยู่ใน AI Test Cases และ Coverage รอบ 2
