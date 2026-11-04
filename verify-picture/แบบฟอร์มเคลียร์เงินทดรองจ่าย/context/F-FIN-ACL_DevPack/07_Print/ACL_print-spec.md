# PRINT SPEC — ใบเคลียร์เงินทดรองจ่าย (ACL) · Replica FM-FIN-02
> โหมด Replica · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json`
> ⚠️ ใช้ block ใหม่ **R9 ตารางกรอบ (.form-grid)** — ไม่มีใน thai-doc v2 · CSS อยู่ที่ `base_form_patch.css` (เสนอเข้าสกิล v2.1) — dev ใช้ไฟล์นี้แทน replica.css

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| เลขที่ | doc.no | ENG-DOC-NUM | ACL-2569-0013 |
| วันที่ | doc_date | doc.created_at | วัน เดือนเต็ม พ.ศ. |
| ชื่อผู้ขอเคลียร์ฯ / ตำแหน่ง / ฝ่าย/แผนก | employee.name/position/dept | Employee (F-EMP-001) · OrgUnit (F-ORG-001) snapshot ตอนออกเลข | text |
| อ้างอิงเลขที่ใบเบิกฯ | advance_ref | ผู้ใช้กรอก (DEC-01) | text |
| ลำดับ / รายละเอียด / จำนวนเงิน | lines[].no/description/amount | ผู้ใช้กรอก · เติมแถวว่างถึง 10 | `#,##0.00` |
| รวมค่าใช้จ่าย | total_expense | Σ lines.amount | `#,##0.00` |
| หัก จำนวนเงินที่เบิกฯ | advance_amount | ผู้ใช้กรอก | `#,##0.00` |
| จำนวนเงินที่เหลือส่งคืน · TOTAL | refund_amount · total_amount | advance − total (ติดลบได้ แสดง "-") | `#,##0.00` |
| ตัวอักษร | total_amount_text | baht_text(total) · ติดลบ = "ลบ…" | ไทย |
| วันที่ 5 ของเดือนถัดไป | policy.clear_due_day | ExpensePolicy.advance_clear_due_day | ตัวเลข |
| ชื่อบัญชี/ธนาคาร/เลขที่บัญชี | refund_account.* | Company.bank_accounts[purpose=advance_refund] | text |
| ช่องลงชื่อ (dynamic) | sign_rows[].signs[] | ผู้ขอ + 1 ต่อขั้นใน DOA (จำนวนตามที่ตั้ง · ไม่ fix) · แถวละ ≤4 เฉลี่ยเท่ากัน · คำตัดสินตาม role (print_config.decision_words.by_role) | ข้อความ "ส่ง/พิจารณาในระบบ วันที่ เวลา" |

## 5. สถานะที่ render (ทุกไฟล์ 1 หน้า · parity IDENTICAL 4/4)
draft · approved (เหลือคืน 149.50) · rejected (ขั้น 1 ไม่อนุมัติ) · long-14rows-overspent (14 แถว · dense · เหลือคืน −2,389.75) · approved-6steps (DOA 6 ขั้น → 7 ช่อง 2 แถว 4+3 · 1 หน้า) — parity 5/5
- กรณีสุดขั้ว 14 แถว + DOA 6 ขั้น = 2 หน้า โดยบล็อกลงชื่อทั้งก้อนขึ้นหน้า 2 (`.signs-block` ไม่ตัดกลาง) ตาม form-replica §5

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ FM-FIN-02.xlsx (Rev.00 : 01/07/2569) · compare region 0:0.72 = **0.66 PASS** (ทั้งหน้า 0.35 — เพราะตั้งใจย้าย)
- ตั้งใจต่าง: (1) ช่องลงชื่อย้ายลงล่างสุด (DEC-07) — ต้นฉบับอยู่ก่อนหมายเหตุ (2) "ผ่าย" → "ฝ่าย" (DEC-06) (3) TOTAL มีค่า + ตัวอักษรตรงยอด (DEC-12) (4) footer ระบบซ้าย (5) ลำดับเติมอัตโนมัติ
- profile: form_fs 9pt · title 16pt · logo 11mm · title_gap 6px · grid_gap 8px
