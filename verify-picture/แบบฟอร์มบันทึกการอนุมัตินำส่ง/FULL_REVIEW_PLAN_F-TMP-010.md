# Full Review Plan — F-TMP-010 แบบฟอร์มบันทึกการอนุมัตินำส่ง

วันที่จัดทำแผน: 26 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: FRD-F-TMP-010 v1.0 (`00_OVERVIEW` ถึง `07_LOCKED_DECISIONS`)  
วัตถุประสงค์: ตรวจเก็บตก Logic, Permission, State, Data integrity และ Integration บน Production โดยไม่ตรวจ layout ซ้ำ

> เอกสารนี้เป็นแผนตรวจ ไม่ใช่ใบรับรองผล Pass/Fail ผู้ตรวจต้องบันทึกผลและหลักฐานจากระบบจริงก่อนสรุปผล

## 1. ข้อสรุปจากการอ่านแพ็ก

- ใช้ FRD เป็น expected result หลักตามคำสั่ง PM/BA ได้ โดยเรียงน้ำหนักเป็น `07_LOCKED_DECISIONS` → `05_RULES` → `03_LOGIC` → `02_API/04_DB` → `06_TESTS` → Test Case เดิม
- Test Case เดิมมี 42 เคส แต่ UAT ฉบับคนเหลือ 37 เคส และตัด 5 เคสที่ต้องตรวจเชิงเทคนิค/หลังบ้านออก
- แพ็กมีคำเตือนว่าไม่มีผล `e2e_standard` จาก browser จริง จึงยังถือไม่ได้ว่า flow เชื่อมต่อครบเพียงเพราะ smoke test 58/58 และ tester เดิมผ่าน
- จุดเสี่ยงสูงสุดของ feature นี้ไม่ใช่ layout แต่คือสายอนุมัติ, สิทธิ์, การส่งกลับแล้วส่งใหม่, การกดซ้ำ/ข้อมูลชนกัน, PDF final, audit และการไม่ยิง event ที่ห้ามยิง
- FRD ระบุว่า Ready หลัง OQ-03/04/06/09 ปิด แต่หน้า Open Questions ยังแสดงรายการเดิม ต้องยืนยันค่า Production จริง ได้แก่ role/module ของ DOA, admin role id, doc type/feature taxonomy และ DOA engine ที่รองรับผลพิจารณา 5 แบบ
- มติ 11 ข้อเป็น `AI-DEFAULT` ในเอกสารต้นทาง หาก Production ทำตาม FRD ให้ตรวจตามนั้น แต่เรื่องเชิงนโยบายควรให้ BA/Owner รับทราบ โดยเฉพาะ “ไม่อนุมัติแล้วกลับร่าง”, “ออกเลขตั้งแต่บันทึกครั้งแรก” และ “ไม่ส่งต่อระบบอื่นหลังอนุมัติ”

## 2. กติกาการตัดสินผล

1. ถ้าระบบต่างจาก FRD ให้ลงเป็น finding ก่อน ห้ามตีความเองว่า FRD เก่าหรือระบบถูกกว่า
2. ถ้ามีหลักฐานว่า BA อนุมัติ behavior ใหม่หลัง FRD ให้แนบหลักฐานและลงเป็น `Spec conflict` ไม่ใช่ Bug ทันที
3. ทุกเคสต้องเก็บอย่างน้อย: เลขเอกสาร, ผู้ใช้/role, เวลา, input สำคัญ, ผลบนจอ และภาพ/Network response เมื่อผิดปกติ
4. เคสที่เกี่ยวกับ permission ต้องทดสอบทั้ง “ไม่มีปุ่มบน UI” และ “เรียก action/route ตรงแล้วถูกปฏิเสธ” เพราะซ่อนปุ่มอย่างเดียวไม่ใช่ security
5. ห้ามทดสอบข้อมูลจริงที่อ่อนไหว ใช้รายการทดสอบที่ระบุชัดและยกเลิก/ปิดงานได้

## 3. ชุดผู้ใช้และข้อมูลที่ต้องเตรียม

| ชุด | ผู้ใช้ |
|---|---|
| Maker | เจ้าของเอกสาร 2 คน เพื่อทดสอบข้ามเจ้าของ |
| Checker | ผู้ตรวจสอบขั้น 1 |
| Middle approver | รองกรรมการผู้จัดการ/ขั้นกลาง |
| Final approver | กรรมการผู้จัดการ/ผู้มีอำนาจ |
| Admin | admin ฝ่ายบริหารการลงทุนที่ Production ใช้จริง |
| Outsider | ผู้ใช้คนละฝ่ายและไม่อยู่ในสายอนุมัติ |

เตรียมเอกสารทดสอบอย่างน้อย 8 ใบ: ระดับ 2 ขั้น, ระดับ 3 ขั้น, ส่งกลับด้วย “ให้แก้ไข”, ส่งกลับด้วย “ไม่อนุมัติ”, อนุมัติแบบมีเงื่อนไขหลายขั้น, ยกเลิกระหว่าง pending, ข้อความยาว/ไฟล์แนบ และเคส concurrency สอง session

## 4. P0 — ต้องตรวจครบก่อนกล้ารับรอง Logic

| ID | Scenario | วิธีเล่น flow | Expected ตาม FRD | หลักฐาน |
|---|---|---|---|---|
| P0-01 | Happy path 2 ขั้น | Maker สร้างระดับรองกรรมการฯ → ส่ง → ขั้น 1 อนุมัติ → ขั้น 2 อนุมัติ | `draft → pending1 → pending2 → approved`; เลขเดิมตลอด; PDF แถวผลอย่างน้อย 3 โดยแถว 3 เป็น “—” | timeline + PDF |
| P0-02 | Happy path 3 ขั้น | สร้างระดับกรรมการผู้จัดการ → อนุมัติครบ 3 ขั้น | ต้องเดินทีละขั้น ห้ามข้าม; ขั้นสุดท้ายแล้วจึง approved | timeline ทุก role |
| P0-03 | ลำดับอนุมัติ | ให้ขั้น 2/3 พยายามกดก่อนขั้นปัจจุบัน | ไม่มีปุ่ม และ action ตรงได้ 403 `NOT_CURRENT_APPROVER`; สถานะไม่เปลี่ยน | UI + response |
| P0-04 | รับทราบ | ลอง `ack` ที่ขั้น 1, ขั้นกลาง และขั้นสุดท้าย | ใช้ได้เฉพาะขั้นกลาง; ขั้น 1/สุดท้ายไม่มีตัวเลือกและ API ได้ 422 `ACK_NOT_ALLOWED` | 3 roles |
| P0-05 | อนุมัติแบบมีเงื่อนไข | ขั้นหนึ่งกดโดยไม่ใส่ข้อสั่งการ แล้วใส่และยืนยัน | ครั้งแรกถูก block; เมื่อครบทุกขั้น สถานะ approved + ผลรวม “อนุมัติแบบมีเงื่อนไข”; แสดงเงื่อนไขทุกขั้น | detail + PDF |
| P0-06 | ให้แก้ไข | ขั้นปัจจุบันส่งกลับแบบ `revise` โดยลองเว้นคำสั่งก่อน | เว้นไม่ได้; สำเร็จแล้วกลับ `draft`, เลขเดิม, owner เห็นเหตุผล, คนในสายเดิมไม่เห็นร่าง | owner/old approver |
| P0-07 | ไม่อนุมัติ | ทำเหมือน P0-06 ด้วย `reject` | กลับ `draft` ไม่ใช่จบใบ; เลขเดิม; audit ระบุ “ไม่อนุมัติ (ขั้น n)” | detail/history |
| P0-08 | ส่งใหม่หลังถูกส่งกลับ | หลัง P0-06/07 แก้ข้อมูลและส่งใหม่ | resolve DOA ใหม่, chain เก่าย้าย audit, returned fields ถูกล้างจากสถานะใช้งาน, เลขเดิม | before/after chain |
| P0-09 | DOA freeze | ส่งใบให้ pending แล้วเปลี่ยนค่า DOA กลาง | ใบเดิมใช้ snapshot เดิม; ใบใหม่/ใบที่ส่งใหม่จึงใช้ DOA ใหม่ | chain comparison |
| P0-10 | ห้ามอนุมัติตัวเอง | ให้ DOA resolve ขั้นหนึ่งเป็น Maker หรือพยายามเลือก Maker | slot ต้องว่าง/เลือกไม่ได้; submit ตรงได้ 422 `SELF_APPROVAL` | modal + response |
| P0-11 | สิทธิ์มองเห็น | ทดสอบ owner อื่น, approver, admin, outsider ใน draft/pending/approved | draft เห็นเฉพาะ owner+admin; หลังส่งเฉพาะ owner/admin/คนใน chain; คนนอกได้ 404 ไม่เปิดเผยว่ามีเอกสาร | list + direct URL |
| P0-12 | Lock หลังอนุมัติ | พยายามแก้, ส่งซ้ำ, พิจารณาซ้ำ, ยกเลิกใบ approved | ทำไม่ได้ทุกช่องทาง; ข้อมูล/PDF final ไม่เปลี่ยน | UI + response |
| P0-13 | กดซ้ำ/เครือข่ายช้า | double-click submit/decide/cancel และ replay `Idempotency-Key` เดิม | เกิดผลครั้งเดียว, ไม่สร้าง chain/audit/event ซ้ำ, ไม่ออกเลขซ้ำ | network + history |
| P0-14 | ข้อมูลชนกันสอง session | เปิด version เดียวกัน 2 หน้าต่าง แล้วให้ทั้งคู่แก้/ตัดสิน | คนหลังได้ 409 `STALE`; สถานะและ audit สะท้อนเฉพาะรายการที่ชนะ | 2 sessions |
| P0-15 | Tenant/คนนอกองค์กร | ใช้ผู้ใช้คนละ tenant หรือ token ที่ไม่เกี่ยวข้องเปิด id ตรง | ไม่พบข้อมูล/404; list, detail, CSV และ attachment ไม่รั่ว | response/export |
| P0-16 | Audit integrity | ไล่สร้าง→แก้→ส่ง→ตัดสิน→ส่งกลับ→ส่งใหม่→อนุมัติ | ประวัติเรียงเวลา, actor/action/before-after ถูก, append-only, ไม่มีขั้นหายหรือถูกเขียนทับ | history/API/DB evidence |
| P0-17 | PDF final + Document Store | อนุมัติสุดท้ายแล้วดาวน์โหลด/เปิดใหม่หลายครั้ง | PDF FM-IVM-08 2 หน้า, ข้อมูลตรงจอ/chain, ชื่อ/ตำแหน่ง/วันที่ไทยถูก, final ถูกเก็บหนึ่งฉบับใน `approved_final` | PDF + storage evidence |
| P0-18 | Integration event | ตรวจ log/event หลัง cancel pending และ conditional approved | ยิงเฉพาะ `ivmh_cancelled` และ `ivmh_conditional_approved` ตามผู้รับ; DOA event ไม่ซ้ำ; ต้องไม่ยิง `ivmh.approved` | event/log evidence |

## 5. P1 — ตรวจความครบทางธุรกิจและข้อมูล

| ID | สิ่งที่ตรวจ | Expected สำคัญ |
|---|---|---|
| P1-01 | Validation ช่องบังคับทั้ง 5 + authority level | แต่ละช่องมี error ถูกจุด; `proposed_conditions` ไม่บังคับ |
| P1-02 | เปลี่ยนระดับ 2 ↔ 3 ตอน draft | preview/table/จำนวน slot เปลี่ยนก่อน freeze; ไม่มีข้อมูล chain เก่าค้าง |
| P1-03 | ผู้พิจารณาทุก slot | ต้องเลือกครบทุกขั้นและเป็นคนที่มีสิทธิ์; ห้าม Maker |
| P1-04 | Cancel draft/pending | เฉพาะ owner/admin; เหตุผลบังคับ; pending/waiting เป็น skipped; pending แจ้ง current approver |
| P1-05 | Cancel โดย outsider/approver | ไม่มีปุ่มและ action ตรงได้ 403; approved/cancelled ได้ 409 |
| P1-06 | เลขเอกสาร | ออกตอนบันทึกครั้งแรก, prefix IVMH, unique ต่อ tenant, เลขไม่เปลี่ยนเมื่อแก้/ส่งกลับ/ส่งใหม่; gap อนุญาต |
| P1-07 | doc type ปิดใช้ | สร้างไม่ได้และได้ 409 `DOC_TYPE_INACTIVE`; ห้าม fallback ออกเลขเอง |
| P1-08 | Attachments | รับ pdf/doc/xls/รูปไม่เกิน 20MB; ปฏิเสธชนิด/ขนาดผิด; คนไม่มีสิทธิ์เปิด/ลบไม่ได้; ref type = IVMH |
| P1-09 | List/filter/search/pagination | ตัวเลข badge, mine-to-act, filter ระดับ/สถานะ, search, pagination 25 และ sort ไม่ตกหล่น/ซ้ำ |
| P1-10 | CSV | ใช้ filter และ permission ชุดเดียวกับหน้าจอ; ไม่ส่งออกใบที่มองไม่เห็น; ภาษาไทย/อักขระพิเศษไม่เพี้ยน |
| P1-11 | Header snapshot | เปลี่ยนชื่อ/โลโก้องค์กรหลังออกเลขแล้ว ใบเดิมยังใช้ snapshot เดิม; ใบใหม่ใช้ค่าใหม่ |
| P1-12 | Maker/approver snapshot | เปลี่ยนชื่อ/ตำแหน่งพนักงานภายหลังแล้วเอกสาร final ยังคงข้อมูล ณ เวลาที่กำหนดใน FRD |
| P1-13 | PDF ข้อความยาว | ข้อความหลายบรรทัดและอักขระไทยยาวยังคง 2 หน้า ไม่ทับ/หาย; ขึ้นบรรทัดด้วย “ · ” ตาม contract |
| P1-14 | DOA 6 ขั้น | ผลพิจารณา 6 แถว, ลงชื่อ Maker+6 = 7 แถว, dense layout และไม่ตัดบล็อกลงชื่อกลางหน้า |
| P1-15 | Form identity | ทุกจุดใช้ FM-IVM-08 และ revision จาก DOCCFG ไม่ใช้ INV-FM-08; ประวัติท้ายแบบเป็น form revision ไม่ใช่ช่องกรอกต่อใบ |
| P1-16 | Confidential data | direct URL, CSV, PDF, attachment และ error response ไม่เผย project/subject/ชื่อผู้พิจารณาแก่ผู้ไม่มีสิทธิ์ |

## 6. Flow ที่แนะนำให้เล่นจริงแบบคุ้มเวลา

### Flow A — 2 ขั้น อนุมัติปกติ

ครอบคลุม P0-01, P0-03, P0-11, P0-12, P0-17, P1-06, P1-15 โดยสลับ login ทุก role และเก็บเลขเอกสารเดียวตลอด flow

### Flow B — 3 ขั้น + รับทราบ + มีเงื่อนไข

ขั้น 1 อนุมัติ → ขั้น 2 รับทราบ → ขั้น 3 ลองรับทราบให้ fail แล้วอนุมัติแบบมีเงื่อนไข ครอบคลุม P0-02/04/05/18 และตรวจผู้รับ notification

### Flow C — ส่งกลับ แก้ และส่งใหม่

ส่งกลับด้วย `revise` หนึ่งรอบ จากนั้นเปลี่ยน DOA/ระดับก่อนส่งใหม่ และอีกรอบใช้ `reject` ครอบคลุม P0-06/07/08/09/16 ซึ่งเป็น flow ที่แพ็กเดิมยังพิสูจน์ไม่ลึกพอ

### Flow D — Attack/negative

เปิด direct URL ด้วย outsider, เรียก action ของขั้นอื่น, เลือกตัวเอง, double click, stale สองหน้าต่าง, export CSV และเปิด attachment ข้ามสิทธิ์ ครอบคลุม P0-10/13/14/15 และ P1-16

### Flow E — เอกสารและ integration

ใช้ข้อความยาว + ไฟล์แนบ + DOA 6 ขั้น + doc type ปิดใช้ แล้วตรวจ PDF/Document Store/Event log ครอบคลุมเคสที่ UAT ฉบับคนตัดออก

## 7. ช่องว่างที่ Test Case เดิมยังไม่พอ

- ไม่มีเคสชัดเจนสำหรับ idempotency แม้ API บังคับ `Idempotency-Key` ทุก POST
- ไม่มีเคส stale/concurrent update แม้ FRD ระบุ 409 `STALE`
- ไม่มีเคส multi-tenant RLS และ attachment/CSV data leakage
- ไม่มีเคสส่งใหม่หลัง `revise/reject` เพื่อตรวจ re-resolve, clear chain และ audit เดิม
- ไม่มีเคสแก้ DOA ระหว่าง pending เพื่อพิสูจน์ snapshot freeze
- ไม่มีเคสตรวจ recipient/dedup ของ notification และการไม่ยิง `ivmh.approved` แบบมีหลักฐาน
- ไม่มีเคสตรวจ `approved_final` ใน Document Store และ immutability ของ final PDF
- เคส admin, DOA 6 ขั้น และ doc type inactive ถูกตัดออกจาก UAT ฉบับคน ทั้งที่เป็น business-critical configuration
- ไม่มีผล browser e2e มาตรฐานแนบในแพ็ก จึงควรรัน flow จริงด้วยผู้ใช้จริง ไม่อ้าง smoke test แทน

## 8. ประเด็นที่ควรถาม PM/BA/Owner ก่อนปิดผล

1. Production ใช้ admin role id อะไร และใครถูกจัด role นี้จริง
2. role ขั้น 2 และขั้น 3 ที่ FRD เขียน `role-gm` เหมือนกัน resolve เป็นคน/ตำแหน่งใดใน Production
3. ยืนยันนโยบายว่า “ไม่อนุมัติ” ต้องกลับร่างเลขเดิม ไม่ใช่ปิดใบ
4. ยืนยันว่าหลัง approved รอบนี้ต้องไม่เปลี่ยนระบบอื่นและไม่ยิง `ivmh.approved`
5. ยืนยัน retention และสิทธิ์เข้าถึง PDF/attachment ของข้อมูลการลงทุน
6. ใครเป็นเจ้าของการติดตามเงื่อนไขหลัง “อนุมัติแบบมีเงื่อนไข” เพราะ FRD ระบุว่าอยู่นอก scope

คำถามเหล่านี้ไม่ควรหยุดการทดสอบ behavior ตาม FRD แต่ต้องปิดก่อนลงชื่อรับรองเชิงธุรกิจ

## 9. วิธีจัดระดับ Finding

| Severity | ตัวอย่างใน feature นี้ |
|---|---|
| Critical | ข้ามขั้น/อนุมัติแทนกันได้, Maker อนุมัติเอง, ข้อมูลข้าม tenant, audit ถูกแก้/หาย |
| High | สถานะผิด, เลข/PDF final ผิด, ส่งกลับแล้วข้อมูลเสีย, event ผิดผู้รับ/ยิงสิ่งที่ห้ามยิง, duplicate action |
| Medium | validation/permission บางช่องผิดแต่มีทางเลี่ยง, CSV/filter ผิด, notification ขาดแต่ flow หลักยังจบ |
| Low | ข้อความ, format วันที่, label หรือความเรียบร้อยที่ไม่เปลี่ยนผลธุรกิจ |

## 10. แบบบันทึกผลต่อเคส

```text
Case ID:
วันที่/เวลา:
Environment/Build:
User + Role:
เลขเอกสาร:
Precondition:
Steps ที่ทำจริง:
Expected (อ้าง FRD BR/FN/VR/EC):
Actual:
Result: Pass / Fail / Blocked / Not Run
Evidence: screenshot / video / network / event log / PDF
Bug ID + Severity (ถ้ามี):
หมายเหตุ/ข้อมูลที่ต้อง cleanup:
```

## 11. เกณฑ์ปิด Full Review

- P0 ผ่านครบ 18 เคส หรือมีหลักฐาน Blocked/Out of scope ที่ PM/BA รับทราบเป็นลายลักษณ์อักษร
- P1 ผ่าน หรือ finding ถูกจัดระดับและมี owner/กำหนดแก้
- ไม่มี Critical/High ค้าง
- ทุก status transition มีอย่างน้อยหนึ่งหลักฐานจากระบบจริง
- มีหลักฐาน permission ทั้ง UI และ server-side deny
- PDF approved final, notification, audit และ CSV ถูกตรวจ ไม่ใช่ดูเฉพาะหน้าจอ
- ประเด็น configuration/OQ ในข้อ 8 มีคำตอบก่อนลงชื่อรับรอง

