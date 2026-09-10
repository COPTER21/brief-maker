# PRINT-SPEC — ใบเบิกค่าใช้จ่าย (EXP) · แนบ FRD
> A4 แนวตั้ง · Sarabun ฝัง base64 · Dev เอา EXP_template.html ไป bind data

## Field map (placeholder → source)
| placeholder | source | หมายเหตุ |
|---|---|---|
| เลขที่ EXP-YYYY-NNNN | ENG-DOC-NUM.next('EXP') | ออกตอนอนุมัติ (doccfg · reset รายปี พ.ศ. · no-gap) |
| วันที่ | header.doc_date | พ.ศ. |
| ผู้เบิก/รหัส/ตำแหน่ง/แผนก | Employee(snapshot) + Movement assignment ณ วันเบิก | soft ref |
| ศูนย์ต้นทุน | Movement assignment.cost_center (snapshot) | null = เว้น |
| ช่องทางจ่าย | header.pay_method | ผ่านเงินเดือน/โอนตรง [A-EXP-01] |
| ตาราง items (วันที่·หมวด·รายละเอียด·จำนวนเงิน) | lines[] | หมวดจาก HR Config เพดานหมวด |
| รวมเป็นเงิน / VAT 7% / รวมทั้งสิ้น | totals() | single source · VAT calcLineVat |
| ตัวอักษร | baht_text(grand_total) | scripts/baht_text.py |
| ลายเซ็น ผู้เบิก/ผู้อนุมัติ(DOA)/การเงิน | DOA chain (snapshot) | ผู้อนุมัติตามที่ resolve |

## กติกาพิมพ์
- A4 · margin ~15mm · ตารางเส้นบาง · เลข/เงิน tabular · วันที่ พ.ศ. ทั้งใบ
- สำเนา (ENG-DOC-STORE) เก็บตอน approved_final (doccfg snapshot flag)
- จำนวนเงิน = RESTRICTED — สำเนาที่เก็บผ่าน Policy Center

## หมายเหตุ
- template นี้เป็น **ตัวอย่าง 1 ใบ** — Dev bind ค่าจริงต่อใบ · เป็นทั้งไฟล์ต้นฉบับ PDF และ tab "PDF Preview" (a4) ใน HTML prototype (ใช้โครงเดียวกัน)
