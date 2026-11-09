# Logic & Business Review Guide — F-TMP-002 Exit Interview

วันที่จัดทำ: 9 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: `context/F-TMP-002_DevPack/03_FRD/FRD_F-TMP-002_Pack/`  
วัตถุประสงค์: ตรวจระบบ production หลังผ่าน functional/UI test แล้ว โดยเน้น logic, business rule, permission, state/data integrity และผลกระทบข้ามระบบ

> เอกสารนี้เป็นแผนตรวจ ไม่ใช่ผลรับรอง ระบบจะถือว่าผ่านได้ต่อเมื่อผู้ตรวจรันเคสจริงและมีหลักฐานของแต่ละข้อ

## 1. ข้อสรุปสำหรับผู้ตรวจ

- ใช้ FRD เป็น acceptance oracle หลัก โดยเฉพาะ `05_RULES`, `03_LOGIC`, `02_API`, `04_DB`, `06_TESTS` และ `07_LOCKED_DECISIONS`
- ไม่ต้องใช้เวลาตรวจ pixel/layout ซ้ำ ยกเว้น UI ทำให้กฎธุรกิจผิด ใช้งานไม่ได้ หรือซ่อน action/ข้อมูลผิดสิทธิ์
- อย่าทดสอบเฉพาะ happy path ต้องตรวจ deny case, conditional validation, การเปลี่ยนสถานะ, การกดซ้ำ/เปิดหลายหน้าต่าง, snapshot, CSV/PDF และ side effect
- test pack เดิมมี 58 test cases แต่ `QA_AUDIT_F-TMP-002.md` ระบุ UAT ฉบับคน 39 เคสและ `[NO-BROWSER]`; ไฟล์เหล่านั้นเป็น test design ไม่ใช่หลักฐานว่าระบบ production ผ่าน

## 2. ประเด็นที่ต้องให้ PM/BA ยืนยันก่อนลงนามรับรอง

เอกสาร FRD ระบุว่ามีมติ `AI-DEFAULT` 11 ข้อ และ `OQ-01` ยังให้ลูกค้ายืนยันก่อน UAT แต่ระบบขึ้น production แล้ว จึงต้องขอคำยืนยันว่า production baseline ยอมรับเรื่องต่อไปนี้จริง:

1. ไม่มีขั้นอนุมัติ/รับทราบ ส่งแล้วจบที่ `submitted`
2. ไม่เปลี่ยนสถานะพนักงานและไม่ส่งข้อมูลไป Offboarding หรือระบบอื่น
3. ผู้ใช้แก้อายุตัว/อายุงานที่ระบบคำนวณได้เอง
4. HR สร้างแทนได้ และ informant เห็น/ยกเลิกได้แต่แก้ร่างหรือส่งไม่ได้
5. ผู้บังคับบัญชาไม่มีสิทธิ์เห็น แม้เป็นหัวหน้าของผู้ให้ข้อมูล
6. เลข EXI ออกตั้งแต่บันทึกร่างครั้งแรก
7. แนบไฟล์และ export CSV เป็น scope production
8. ปัจจัยลาออกเลือกได้สูงสุดตามแบบ 21 ข้อ ไม่ได้จำกัดแค่ 3 อันดับ

ถ้า PM/BA ไม่ยืนยันข้อใด ห้ามสรุปว่าเป็น bug ทันที ให้ลงเป็น “source/business decision conflict” และพักการรับรองส่วนนั้น

## 3. Test data และ persona ที่ต้องเตรียม

| ชุด | ต้องมี |
|---|---|
| E-A Owner | พนักงานทั่วไป มี birth date, hire date, ข้อมูล org ครบ |
| E-B Informant | พนักงานที่ HR จะสร้างแบบแทน |
| E-C Manager | ผู้บังคับบัญชาของ E-A/E-B แต่ไม่มี role HR |
| E-D Other | พนักงานอื่นที่ไม่เกี่ยวข้อง |
| H-A HR | มี `role-mgr-hr` และสร้างแทนได้ |
| T-2 | tenant/company อื่น สำหรับทดสอบ data isolation |
| Data missing | พนักงานไม่มี birth date และพนักงานไม่มี contract end date |
| Config | EXI active 1 รอบ และ inactive 1 รอบ (ถ้าทีมระบบจัดให้ได้) |

ใช้ข้อมูลทดสอบเท่านั้น ห้ามกรอกความเห็น Exit Interview จริงของพนักงาน production เพราะคำตอบเป็น Confidential/PII

## 4. ลำดับรันทดสอบแนะนำ

### P0 — ความลับและสิทธิ์ (ต้องผ่านทั้งหมด)

| ID | วิธีทดสอบ | Expected ตาม FRD | หลักฐาน |
|---|---|---|---|
| SEC-01 | E-A สร้างร่าง แล้ว login E-C ผู้บังคับบัญชา ค้นหา/กรองรายการ | ไม่เห็นใบ | ภาพรายการ |
| SEC-02 | E-C เปิด URL/ID ใบของ E-A โดยตรง | 404/ไม่พบ ไม่เปิดเผยว่ามีเอกสาร | ภาพ + network response |
| SEC-03 | E-D เปิด URL ร่าง/ส่งแล้วของ E-A | 404/ไม่พบ | ภาพ + response |
| SEC-04 | H-A สร้างแทน E-B แล้ว login E-B | เห็นใบ แต่ไม่มีแก้ไข/ส่ง; ยกเลิกได้ถ้า baseline ยืนยัน | ภาพ action |
| SEC-05 | E-A เปิดใบที่ H-A สร้างแทน E-B | ไม่เห็น/404 | response |
| SEC-06 | E-D เรียก cancel/update/submit ของใบ E-A โดยตรง | 403 หรือ 404 ตาม contract; ข้อมูลไม่เปลี่ยน | response + สถานะเดิม |
| SEC-07 | E-A export CSV | ได้เฉพาะใบที่ E-A มีสิทธิ์เห็น | CSV + เทียบรายการ |
| SEC-08 | E-C export CSV | ไม่มีใบของลูกน้อง | CSV |
| SEC-09 | H-A export CSV | เห็นทุกใบภายใน tenant ที่ได้รับสิทธิ์เท่านั้น | CSV |
| SEC-10 | ใช้ session/header tenant T-2 เปิด ID tenant แรก | ต้องไม่พบข้อมูลและไม่ดาวน์โหลด PDF/ไฟล์แนบได้ | response |
| SEC-11 | ใช้ URL ไฟล์แนบของคนอื่นโดยตรง | ดาวน์โหลดไม่ได้ | response |

เกณฑ์: ข้อ SEC ใดรั่วข้อมูลคำตอบ/ไฟล์/PDF ให้จัด Critical และหยุดรับรองทันที

### P0 — State transition และการล็อกข้อมูล

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| STA-01 | สร้างใหม่และบันทึกครั้งแรก | ได้เลข EXI 1 เลข, status `draft`, owner เป็นผู้สร้าง |
| STA-02 | แก้ร่างและบันทึกหลายครั้ง | เลขเดิม ไม่สร้างใบซ้ำ version เพิ่มอย่างถูกต้อง |
| STA-03 | ส่งร่างครบข้อมูลใน config 0 ขั้น | `draft → submitted`, มี `submitted_at`, ไม่มี pending/approved |
| STA-04 | หลังส่ง ลอง edit ผ่าน UI และ API | ไม่มีปุ่มแก้; API ปฏิเสธ; ค่าเดิมไม่เปลี่ยน |
| STA-05 | เจ้าของยกเลิกร่างโดยไม่ใส่เหตุผล | บล็อก “กรุณาระบุเหตุผล” |
| STA-06 | เจ้าของยกเลิกร่างพร้อมเหตุผล | `draft → cancelled`, เก็บเหตุผลและ audit |
| STA-07 | HR หรือ informant ยกเลิกใบ submitted ตามสิทธิ์ | `submitted → cancelled`, เก็บเหตุผล, แจ้งเตือนตามกฎ |
| STA-08 | ใบ cancelled ลองแก้/ส่ง/ยกเลิกซ้ำ | ทุก action ถูกปฏิเสธ ไม่มี state ย้อนกลับ |
| STA-09 | double-click ปุ่มบันทึก/ส่ง/ยกเลิก หรือยิง request ซ้ำ | มีใบเดียว, transition เดียว, event ไม่ซ้ำ |
| STA-10 | เปิดร่างเดียวกัน 2 browser แก้คนละค่าแล้วบันทึกตามลำดับ | request เก่าถูก 409 `STALE_VERSION`; ไม่ทับค่าล่าสุด |
| STA-11 | submit พร้อมกัน 2 browser | ส่งสำเร็จครั้งเดียว เลข/สถานะ/event ไม่ซ้ำ |

### P0 — Conditional validation และการคำนวณ

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| VAL-01 | HR สร้างแทนแต่ไม่เลือกผู้ให้ข้อมูล | บล็อก “กรุณาเลือกผู้ให้ข้อมูล” |
| VAL-02 | เลือกลาออกแต่ไม่ใส่ resign date | บล็อก |
| VAL-03 | resign date ก่อน hire date | บล็อกทั้ง UI และ server |
| VAL-04 | เปลี่ยนจากลาออกเป็นครบสัญญาหลังกรอก resign date | resign date ต้องถูก clear/ไม่ถูกบันทึก |
| VAL-05 | ครบสัญญาแต่ไม่เลือกเหตุผลข้อ 5 | บล็อก |
| VAL-06 | เหตุผลข้อ 5 = อื่น ๆ แต่ไม่กรอก | บล็อก |
| VAL-07 | เปลี่ยนจากเหตุผล “อื่น ๆ” เป็นตัวเลือกอื่น | ข้อความ other เก่าไม่ควรติดไปในข้อมูล/PDF |
| VAL-08 | ตอบ rating 25/26 แล้วส่ง | บล็อก ระบุเหลือ 1 ข้อ และชี้ตำแหน่งถูก |
| VAL-09 | ดัด request rating เป็น 0, 6, null, key ขาด/เกิน | server ตอบ 422; ไม่บันทึกค่าผิด |
| VAL-10 | ไม่เลือกปัจจัยลาออก | บล็อก |
| VAL-11 | เลือก other แต่ไม่กรอกข้อความ | บล็อก |
| VAL-12 | ดัด request ให้ rank ซ้ำ/ขาดช่วง/reason ซ้ำ | server ตอบ 422/constraint; transaction ไม่ค้างครึ่งเดียว |
| VAL-13 | เลือก 21 ปัจจัย แล้วเอาข้อกลางออก/เลื่อนอันดับ | rank ต้องกลับเป็น 1..N ไม่ซ้ำและคงหลัง reload |
| VAL-14 | พนักงานมี birth/hire date; เปลี่ยน resign date ข้ามวันเกิด/ครบรอบงาน | ปีเต็มถูกต้อง ไม่มี off-by-one |
| VAL-15 | พนักงานไม่มี birth date | age ว่างและกรอกเองได้ตามกฎ |
| VAL-16 | contract end ไม่มี contract_end_date upstream | ใช้วันที่วันนี้ตาม FRD และปรับได้ |
| VAL-17 | ปรับ age เป็น 14/81 และ service_months -1/12 ผ่าน UI/API | บล็อกตามช่วง 15–80 และ 0–11 |
| VAL-18 | เปิด `calc_manual`, กรอกค่าเอง, เปลี่ยนวันที่ลาออก, save/reload | ค่า manual ไม่ถูกคำนวณทับ |
| VAL-19 | ปิดโหมด manual/สั่งคำนวณใหม่ | กลับเป็นค่าที่คำนวณจาก ref date |

### P1 — Snapshot และความถูกต้องของข้อมูลระยะยาว

| ID | วิธีทดสอบ | Expected / จุดตัดสิน |
|---|---|---|
| DAT-01 | สร้างร่าง แล้วแก้ชื่อ/ตำแหน่ง/ฝ่ายใน Employee/Org | ใบเดิมใช้ snapshot ตอนออกเลข ไม่เปลี่ยนตาม master |
| DAT-02 | สร้างกรณีครบสัญญา แล้วเปลี่ยน contract_end_date upstream ก่อนเปิด/ส่ง | ต้องยืนยันกับ BA: ค่า ref date ควร snapshot; หากผลคำนวณเปลี่ยนเองถือเป็นความเสี่ยงข้อมูลย้อนหลัง |
| DAT-03 | HR สร้างแทน | owner = HR, employee/informant = พนักงาน, audit ระบุสร้างแทนอย่างตรวจสอบได้ |
| DAT-04 | บันทึก improvements 0, 1, 6, 12 แถว | UI/API/reload/PDF เก็บครบ ลำดับไม่สลับ ไม่ตัดข้อความ |
| DAT-05 | ใส่ภาษาไทย, emoji, newline, เครื่องหมาย quote/comma ในข้อความ | save/reload/PDF/CSV ไม่เพี้ยนและไม่ทำให้โครงสร้างเสีย |
| DAT-06 | ตรวจ audit หลัง create/edit/submit/cancel | append-only, actor/time/action ถูก, ประวัติเก่าไม่หาย |
| DAT-07 | ลอง refresh/back/เปิดหลาย tab ระหว่าง wizard | ไม่สร้าง draft ซ้ำหรือผูกไฟล์แนบผิดใบ |

### P1 — Numbering และ configuration

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| NUM-01 | ผู้ใช้ 2 คนบันทึกครั้งแรกพร้อมกัน | เลขไม่ซ้ำและเป็นรูปแบบจาก F-DOCCFG |
| NUM-02 | สร้างร่างแล้วยกเลิก แล้วสร้างใหม่ | เลขเดิมไม่ถูกนำกลับมาใช้ |
| NUM-03 | ปิด doc type EXI แล้วเข้ารายการ/เรียก create API | ปุ่มสร้าง disabled และ API 409 `DOC_TYPE_INACTIVE` |
| NUM-04 | ปิด EXI หลังเปิด wizard แต่ก่อน save | save ถูกปฏิเสธอย่างปลอดภัย ไม่มีใบครึ่งเดียว |
| NUM-05 | ตรวจปี พ.ศ./ค.ศ. ช่วงวันสิ้นปีตาม policy ของเลขเอกสาร | reset/format ถูกตาม F-DOCCFG ไม่เดาเลขเอง |

### P1 — Notification และ side effect

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| EVT-01 | ส่งใบ 1 ครั้ง | `exi_submitted` ถึง role-mgr-hr 1 ครั้ง และไม่ใส่คำตอบลับในข้อความ |
| EVT-02 | refresh/retry submit หลังสำเร็จ | ไม่ส่ง notification ซ้ำ |
| EVT-03 | ยกเลิกจาก draft | ไม่ยิง `exi_cancelled` ตาม FN-07 |
| EVT-04 | ยกเลิกจาก submitted | ยิง `exi_cancelled` ถึง HR + ผู้สร้าง 1 ครั้ง |
| EVT-05 | สร้าง/ส่ง/ยกเลิก | ไม่เปลี่ยน Employee status และไม่สร้าง offboarding/downstream record |

### P1 — CSV, PDF และ attachment

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| OUT-01 | PDF draft/submitted/cancelled | เลขและค่าตรง DB, ไม่มี `{{ }}`, สถานะ/ลายเซ็นตรงจริง |
| OUT-02 | PDF กรณีลาออกและครบสัญญา | checkbox และเหตุผลอยู่ช่องถูก ไม่แสดง field ของ branch อื่น |
| OUT-03 | PDF 21 ปัจจัย + 12 improvements | ไม่ตกหล่น ไม่ตัดแถว และอ่านได้ทุกหน้า |
| OUT-04 | export ใบที่เลือกปัจจัย 4–21 อันดับ | ต้องไม่สูญข้อมูล; ถ้า CSV มีเพียงอันดับ 1–3 ให้เปิด decision กับ BA |
| OUT-05 | CSV ภาษาไทย/quote/comma/newline/ค่าขึ้นต้น `=`, `+`, `-`, `@` | encoding ถูกและป้องกัน spreadsheet formula injection ตามมาตรฐานองค์กร |
| OUT-06 | filter แล้ว export | แถวใน CSV ตรง filter และสิทธิ์ ไม่ใช่ export ทั้งหมดโดยพลการ |
| OUT-07 | แนบไฟล์ PDF/Word/Excel/รูป ≤20 MB | upload, reload, download ถูกใบและถูกสิทธิ์ |
| OUT-08 | ไฟล์ชนิดห้าม/เกิน 20 MB/ชื่อซ้ำ | บล็อกหรือจัดการตาม policy; ไม่มีไฟล์ orphan |
| OUT-09 | ยกเลิกใบที่มีไฟล์แนบ | สิทธิ์ดาวน์โหลดหลังยกเลิกตรง policy และไม่รั่ว public URL |

### P2 — รายการและความทนทาน

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| LST-01 | search เลข/ชื่อ/รหัส/แผนก | ผลถูกและไม่เห็นข้อมูลนอกสิทธิ์ |
| LST-02 | filter status/sep type/division ผสมกัน | AND/Reset ถูกต้อง |
| LST-03 | pagination 25, เปลี่ยนหน้า, sort | ไม่ซ้ำ/ไม่หายเมื่อข้อมูลมากกว่า 25 |
| LST-04 | API ล้มตอน save/submit/cancel | แสดง error, state ไม่เปลี่ยน, retry ได้ |
| LST-05 | network ช้าหรือขาดหลังผู้ใช้กด submit | เมื่อกลับมา ต้องรู้ผลสุดท้ายแน่นอนและไม่สร้าง event ซ้ำ |

## 5. จุดขัดกัน/ช่องว่างใน FRD ที่ควรเปิดกับ PM/BA

1. **CSV อาจสูญปัจจัยอันดับ 4–21** — BR-04/DEC-05 ให้เลือกได้ 21 ปัจจัย แต่ AC-08 ระบุ CSV เฉพาะอันดับ 1–3 ต้องตกลง data contract ให้ชัด
2. **Contract end date ไม่มี snapshot ใน DB** — logic ใช้ `Employee.contract_end_date` เป็น ref date แต่ตารางไม่มีคอลัมน์ snapshot; ข้อมูล master เปลี่ยนอาจทำให้อายุงานย้อนหลังเปลี่ยน
3. **Approval/pending ปรากฏใน logic แต่ out of scope** — DB status มีแค่ draft/submitted/cancelled ขณะที่ FN-05..07 และ test K01–K03 กล่าวถึง pending/DOA; รอบ production ปัจจุบันควรยืนยันว่าเป็น dormant code ไม่ใช่ behavior ที่ต้องรับรอง
4. **AI-DEFAULT ยังไม่เห็นหลักฐานอนุมัติใน context** — ต้องมี production decision record จาก PM/BA โดยเฉพาะ visibility, cancel authority, no approval และ no downstream
5. **การแก้ค่าคำนวณด้วยมือ** — FRD อนุญาต แต่ต้องตกลงว่าจะเก็บเหตุผล/ค่าเดิมใน audit หรือไม่ เพราะมีผลต่อความน่าเชื่อถือของข้อมูล HR
6. **Cancellation ของ informant ที่ HR สร้างแทน** — permission matrix อนุญาตให้ยกเลิกแต่ห้ามแก้/ส่ง ต้องให้ BA ยืนยันว่าเจตนาถูกต้อง
7. **CSV เป็นข้อมูล Confidential** — FRD กล่าวถึงสิทธิ์ แต่ไม่ได้ระบุ audit การ export, masking, retention หรือ formula injection ให้ใช้ security standard กลางและบันทึกข้อจำกัด

## 6. วิธีบันทึกผลต่อเคส

แต่ละเคสให้ลงข้อมูลขั้นต่ำ:

- Result: Pass / Fail / Blocked / Not run
- เวลาและ environment/build
- persona + test data ID (ไม่ใส่ PII จริง)
- ขั้นตอนสั้น ๆ ที่ทำซ้ำได้
- Expected อ้าง FRD เช่น `05_RULES BR-06`, `03_LOGIC FN-10`
- Actual ที่เห็นจริง รวม status/ข้อความ/ค่าก่อน-หลัง
- screenshot หรือ video และ network response สำหรับ permission/API
- bug severity: Critical = รั่วข้อมูล/ข้ามสิทธิ์/ข้อมูลหาย, High = สถานะ/เลข/PDF/CSV/notification ผิด, Medium = ผิด spec แต่มีทางเลี่ยง, Low = ข้อความ/หน้าตา

## 7. เกณฑ์จบรอบ review

- SEC, STA, VAL ระดับ P0 ผ่าน 100%
- ไม่มี Critical/High ค้าง
- ทุก BR-01..BR-14 มีอย่างน้อย 1 ผลทดสอบจริง และ deny case ที่เกี่ยวข้อง
- state transition และ notification พิสูจน์ว่าไม่เกิดซ้ำ
- PDF/CSV เทียบกับค่าที่บันทึกจริงอย่างน้อยกรณีลาออก, ครบสัญญา, long data
- PM/BA ตอบข้อ conflict ในหัวข้อ 5 และยืนยัน AI-DEFAULT ที่ production ใช้
- ระบุชัดว่าอะไรไม่ได้ทดสอบ เช่น tenant isolation, config inactive หรือ notification backend; ห้ามนับเป็น Pass

เมื่อรันเสร็จ ให้นำผลจริงมาสร้าง Feature Check Report แยก Logic/UI/UX/Bug โดยห้ามเติม Pass ให้เคสที่ไม่มีหลักฐาน
