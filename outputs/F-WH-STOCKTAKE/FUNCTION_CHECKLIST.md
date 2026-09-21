# FUNCTION_CHECKLIST — F-WH-STOCKTAKE

อัปเดต WF จาก HTML/Coverage R1/E2E และ QA จาก AI Test Cases/Coverage R2 เมื่อ 2026-09-20

| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|:---:|:---:|:---:|
| FN-01 | เลือกคลัง/โซน/ตำแหน่งแบบค้นหาและกำหนดพื้นที่รอบนับใหญ่ | S05,S09/BR01 | ✓ `#/create` | — | ✓ TC-ST-01–03 |
| FN-02 | แสดงรายการ Item/Location แบบ soft-reference | S05/BR01 | ✓ `#/sheets` | — | ✓ TC-ST-06 |
| FN-03 | ล็อก movement เฉพาะพื้นที่และกันรอบซ้อน | S05,S09,S12/BR01 | ✓ `scopesOverlap()` | — | ✓ TC-ST-04–05 |
| FN-04 | เก็บ snapshot ยอด ณ lock time แบบไม่แก้ย้อนหลัง | S01,S05,S13/BR02 | ✓ `freezeRound()` | — | ✓ TC-ST-04,26 |
| FN-05 | สร้างใบนับและมอบหมายคนจริง | S05/BR03 | ✓ assign modal | — | ✓ TC-ST-06–07,09 |
| FN-06 | ผู้ตรวจไม่เห็นยอดระบบ/ผลต่าง; supervisor reveal ตามสิทธิ์ | S01,S05/BR03 | ✓ `canSeeSystem()` | — | ✓ TC-ST-08–09,22 |
| FN-07 | บันทึกผลนับศูนย์ได้ แต่กันค่าติดลบและช่องว่าง | S01,S04/BR03 | ✓ validation | — | ✓ TC-ST-10 |
| FN-08 | คำนวณผลต่างหลังส่งและใช้ threshold config effective date | S02,S03,S08/BR04 | ✓ `submitCount()` | — | ✓ TC-ST-11,13–14 |
| FN-09 | บังคับนับซ้ำโดยคนอิสระเมื่อเกิน threshold | S07/BR04 | ✓ recount flow | — | ✓ TC-ST-11–13 |
| FN-10 | ส่ง DOA slot คนจริง อนุมัติ/ปฏิเสธมีเหตุผลและ audit | S05,S06/BR05 | ✓ approval flow | — | ✓ TC-ST-14–18 |
| FN-11 | ส่งผลต่างไป Stock Adjustment draft แล้วปลดล็อก ไม่ปรับยอดเอง | S10,S11/BR06 | ✓ `handoff()` | — | ✓ TC-ST-19–20,25 |
| FN-12 | แยก boundary Stocktake รอบใหญ่จาก Cycle Count ABC | S05/BR01 | ✓ rendered scope | — | ✓ TC-ST-21 |

หลักฐานรวม: `_COVERAGE_REPORT.md` · `_e2e/RESULT.md` · `testcases-F-WH-STOCKTAKE.md`
