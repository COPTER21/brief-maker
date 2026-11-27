# Full Review Guide — F-TMP-004 แบบฟอร์มตารางติดตามงานและแผนฐาน

วันที่จัดทำ: 27 พฤศจิกายน 2569  
สถานะเอกสาร: แผนตรวจและ desk review จาก FRD — **ยังไม่ใช่ผล Pass/Fail จากระบบจริง**

## 1. คำตอบสั้นสำหรับผู้ตรวจ

รอบนี้ไม่ควรตรวจ layout ซ้ำเป็นหลัก และไม่ควรใช้คำว่า “ลองกดดูแล้วใช้งานได้” เป็นผลสรุป ให้ยึด FRD เป็น baseline แล้วพิสูจน์ 6 เรื่อง:

1. กฎคำนวณและ validation ถูกต้อง
2. สถานะเอกสารเดินได้เฉพาะเส้นทางที่อนุญาต
3. สิทธิ์และลำดับอนุมัติไม่ถูกข้าม
4. ข้อมูล, PDF, CSV, ประวัติ และ notification สอดคล้องกัน
5. การกดซ้ำ, เปิดพร้อมกันหลายคน และระบบเชื่อมต่อล้ม ไม่ทำข้อมูลซ้ำหรือสถานะเพี้ยน
6. สิ่งที่ระบบทำตรงกับเจตนาธุรกิจ ไม่ใช่แค่ตรงหน้าจอ

ฟีเจอร์นี้ตาม FRD เป็น **การจัดทำและอนุมัติแผนฐาน** มากกว่าระบบติดตามงานต่อเนื่อง เพราะใบที่อนุมัติแล้วถูกล็อก และ “อัปเดตความคืบหน้าหลังอนุมัติ” อยู่นอก scope (§0.3, DEC-01, OQ-07)

## 2. Source of truth และเกณฑ์ตัดสิน

ใช้เอกสารตามลำดับนี้:

1. `FRD/05_RULES` — BR, state machine, permission, validation, edge case
2. `FRD/03_LOGIC` — สูตรและพฤติกรรมของแต่ละ function
3. `FRD/06_TESTS` — acceptance criteria และ deny cases
4. `FRD/02_API` และ `04_DB` — concurrency, idempotency, audit, RLS, server-side computation
5. `FRD/07_LOCKED_DECISIONS` — มติที่ล็อกไว้
6. HTML/UI brief ใช้อ้างข้อความและตำแหน่งบนจอ ไม่ใช้เปลี่ยนกฎธุรกิจ

การตัดสิน:

- ระบบไม่ตรง FRD ที่ชัดเจน = defect
- ระบบตรง FRD แต่ดูไม่ตอบโจทย์งานจริง = business gap / change request ไม่ใช่ defect
- FRD ขัดกันหรือระบุไม่พอ = clarification ห้ามเดาผลที่ควรเป็น
- สิ่งที่ยังไม่ได้ทำจริง = Not tested ห้ามนับเป็น Pass

## 3. ข้อควรระวังเมื่อระบบขึ้น Production แล้ว

- ขอใช้ UAT ที่ build/config เท่ากับ Production หรือ test tenant ใน Production
- ถ้าจำเป็นต้องตรวจบน Production จริง ให้ใช้ข้อมูลสมมติที่ระบุชัด, บัญชีทดสอบ, เลขเอกสารที่ตกลงกับ PM/BA และช่วงเวลาที่ไม่รบกวนงานจริง
- ห้ามทดสอบยกเลิก, อนุมัติ, notification, ปิด doc type, เปลี่ยน DOA หรือยิงซ้ำบนข้อมูลธุรกิจจริงโดยไม่มีผู้มีอำนาจอนุญาต
- เก็บ build/version, tenant, config DOA, doc type, บัญชี/role และเวลาทดสอบทุกครั้ง เพราะผลขึ้นกับ config เหล่านี้

## 4. ข้อมูลและบัญชีที่ต้องเตรียม

### Personas

- Owner A — ผู้จัดทำใบ
- Owner B — เจ้าของใบคนอื่น
- Approver 1 — ผู้ตรวจสอบขั้นปัจจุบัน
- Approver 2 — ผู้อนุมัติขั้นถัดไป
- Approver Other — อยู่ในสายแต่ยังไม่ถึงขั้น
- Outsider — ไม่ใช่เจ้าของและไม่อยู่ในสาย
- Investment Admin — admin ของฝ่ายตาม role จริง
- ผู้รับผิดชอบหมุดหมาย/งานที่ map เป็น user ได้อย่างน้อย 1 คน และข้อความที่ map ไม่ได้ 1 ค่า

### Config และข้อมูล

- DOA แบบ 1, 2 และ 6 ขั้น หรืออย่างน้อย 2 ขั้นพร้อมหลักฐานว่า dynamic จริง
- doc type `IVMB` สถานะ active; การปิดใช้ให้ทดสอบใน UAT เท่านั้น
- ไฟล์เล็กชนิด pdf/doc/xls/image, ไฟล์ชนิดไม่รองรับ, ไฟล์เกิน 20 MB
- ใบ draft, pending ขั้น 1, pending ขั้น 2, returned draft, approved, cancelled
- ข้อมูลแถวขั้นต่ำ, 8/18 แถว, มากกว่า 8/18 แถว และข้อความยาว/ภาษาไทย

## 5. ลำดับรันที่แนะนำ

### Gate A — Smoke และความพร้อม

- [ ] ยืนยัน build/config/tenant และบัญชีทุก role
- [ ] เปิดรายการและรายละเอียดได้ ไม่มี error ที่ขัดขวาง
- [ ] doc type IVMB active และเลขเอกสารออกจาก service จริง
- [ ] ยืนยันว่าจะตรวจ notification, PDF store, audit และ API evidence จากที่ใด

ถ้า Gate A ไม่พร้อม ให้หยุดและบันทึก Not tested แทนการเดา

### Gate B — P0 End-to-end เส้นหลัก

#### R01 สร้างร่างขั้นต่ำและออกเลข

- Owner A สร้างชื่อโครงการ + หมุดหมาย 1 แถว + งาน 1 แถวที่มีช่องบังคับครบ
- คาด: บันทึกได้เลข `IVMB-YYYY-NNNN`, status=draft, เลขไม่เปลี่ยนเมื่อแก้และบันทึกซ้ำ
- ตรวจต่อ: maker/header snapshot, audit create, ไม่มีเลข/ใบซ้ำเมื่อ double-click
- อ้าง: AC-01, BR-07, BR-10, FN-04

#### R02 Validation ช่องบังคับ

- ลองขาด project name, milestone/owner/baseline date, task/owner/due date ทีละชนิด
- คาด: บล็อก, ชี้แถวถูก, ข้อความตรง VR-01..03, ไม่สร้างข้อมูลครึ่งใบ
- อ้าง: AC-02, VR-01..03

#### R03 สูตรความคลาดเคลื่อน

- baseline 08/09, revised 11/09 → `+3` และเตือนแต่ไปต่อได้
- revised ก่อน baseline → ค่าลบและไม่เตือน
- revised ว่าง → แสดงว่าง/— ไม่ใช่ 0
- เพิ่มกรณีข้ามเดือน, ข้ามปี และ leap day เพื่อยืนยันว่าเป็น calendar-day difference
- อ้าง: AC-03, BR-01/02, EC-01/02

#### R04 Progress และ warning

- ลอง -1, 0, 0.5, 100, 100.01, 150 และค่าที่ไม่ใช่ตัวเลข
- คาด: 0–100 รวมทศนิยมผ่าน; นอกช่วง/ไม่ใช่ตัวเลขถูกบล็อก
- status=แล้วเสร็จ + 80% ต้องเตือนแต่ส่งได้
- อ้าง: AC-04/05, BR-03/04, EC-03/04

#### R05 last_updated

- บันทึกแถวใหม่ → มีวันที่ระบบ
- แก้เฉพาะแถว 2 → เปลี่ยนวันที่เฉพาะแถว 2
- บันทึกโดยไม่แก้แถวนั้น → วันที่เดิมต้องไม่เปลี่ยน
- ผู้ใช้แก้ค่าเองไม่ได้ และ server ต้องไม่รับค่าที่ client ส่งมา
- อ้าง: AC-06, BR-05, FN-02

#### R06 ส่งอนุมัติและ freeze สาย

- ส่งใบด้วย DOA 2 ขั้น; ตรวจ default assignee และจำนวน slot
- Owner ต้องเลือกตัวเองไม่ได้และทุกขั้นต้องมีคน
- หลังส่ง แก้ DOA กลาง แล้วเปิดใบเดิม
- คาด: ใบเดิมใช้ approval chain snapshot เดิม; status=pending ขั้น 1
- อ้าง: AC-07, BR-08, EC-06/07

#### R07 อนุมัติตามลำดับจนจบ

- Approver 2 พยายามอนุมัติก่อน → ต้องไม่มีปุ่มและ API ต้อง 403
- Approver 1 อนุมัติ → ขั้น 2 pending, ใบยังไม่ approved
- Approver 2 อนุมัติ → approved, ล็อกแก้ไข, approved_by/at ถูกต้อง
- ตรวจ PDF `approved_final` ถูกเก็บ และ event `ivmb_baseline_approved` ยิงครั้งเดียว
- อ้าง: AC-08, FN-06/09/10, TC-D03

#### R08 ส่งกลับและส่งใหม่

- ขั้น 1 ส่งกลับโดยไม่ใส่เหตุผล → บล็อก
- ใส่เหตุผล → กลับ draft, เลขเดิม, เห็นเหตุผลและ audit ขั้นที่ส่งกลับ
- เปลี่ยน DOA แล้วส่งใหม่ → resolve สายใหม่; chain เดิมยังอยู่ใน audit แต่ไม่ถูกใช้ต่อ
- อ้าง: AC-09, BR-09, FN-07

#### R09 ยกเลิก

- Owner ยกเลิก draft และ pending โดยเหตุผลบังคับ
- Admin ยกเลิก draft/pending ของคนอื่นตาม role จริง
- Outsider ต้องทำไม่ได้; approved/cancelled ต้องยกเลิกซ้ำไม่ได้
- pending→cancelled: ขั้นค้างเป็น skipped และ `ivmb_cancelled` ส่งถึงผู้พิจารณาปัจจุบันครั้งเดียว
- อ้าง: AC-11, FN-08/10, TC-D04

#### R10 Permission และข้อมูลรั่ว

- Owner B / Approver / Outsider ต้องไม่เห็น draft ของ Owner A ใน list, search, CSV และ direct URL
- ผู้ไม่มีสิทธิ์เปิด ID ตรง ๆ ต้องได้ 404 ไม่ใช่ 403
- Admin เห็นทุกใบ แต่แก้ draft ของคนอื่นไม่ได้
- ผู้ในสายเห็นหลังส่ง แต่ตัดสินได้เฉพาะ current step
- ทำซ้ำทั้ง UI และ direct API เพราะซ่อนปุ่มอย่างเดียวไม่พอ
- อ้าง: BR-11, §5.3, TC-D01..06, RLS

#### R11 PDF และ immutability

- ทุกสถานะ render ได้, รหัส `FM-IVM-02`, วันที่ พ.ศ., หน้า/ลายเซ็น/คำตัดสินตรง role
- 8 milestones + 18 tasks และ 12 milestones + 18 tasks: ไม่ตัดข้อความ/แถว/บล็อกลงชื่อ
- approved PDF ต้องตรงค่าที่อนุมัติ และยังเหมือนเดิมหลังแก้ชื่อพนักงาน, Organization, DOA หรือ revision config
- จำนวน sign rows = maker + จำนวนขั้นจาก snapshot ไม่ใช่ค่าปัจจุบัน
- อ้าง: AC-10/13, BR-12/13/15, FN-09

#### R12 ความสอดคล้องข้าม output

- เลือกใบเดียวเปรียบค่าระหว่าง detail, list summary, PDF, CSV, audit และ database/API response
- จำนวนแถว, ค่า variance, average progress, status, ผู้จัดทำ, เลข, วันเวลา ต้องไม่ขัดกัน
- CSV ต้องใช้ filter และสิทธิ์เดียวกับรายการ; ภาษาไทยเปิดได้ถูกต้อง
- อ้าง: AC-12, FN-11

### Gate C — Reliability / Integration ที่ test case เดิมยังไม่พิสูจน์พอ

#### R13 Idempotency และการกดซ้ำ

- double-click สร้าง, ส่ง, อนุมัติ, ส่งกลับ, ยกเลิก
- replay request ด้วย Idempotency-Key เดิม
- คาด: 1 ผลลัพธ์, 1 transition, 1 audit ที่มีผล, 1 event, ไม่สร้างใบ/เลข/PDF ซ้ำ
- อ้าง: API §2.3

#### R14 Optimistic locking

- เปิด draft เดียวกันสองแท็บ; แท็บ A บันทึก แล้วแท็บ B บันทึก version เก่า
- เปิด pending ก่อนอีกคนตัดสิน แล้วส่ง decision จากข้อมูลเก่า
- คาด: 409 STALE, ไม่ overwrite, ไม่เปลี่ยนสถานะซ้ำ, UI บอกให้ refresh อย่างเข้าใจได้
- อ้าง: EC-09, API §2.3

#### R15 Failure recovery

- จำลอง DOA resolve ล้ม, Document Number ล้ม, upload ล้ม, PDF/store ล้ม, notification ล้ม
- ตรวจว่า transaction ไม่ค้างครึ่งทางและ retry ไม่สร้างซ้ำ
- จุดต้องตกลงกับทีม: หาก final approval สำเร็จแต่ PDF store หรือ notification ล้ม จะ rollback approval หรือ queue retry

#### R16 Attachment

- อัปโหลด/ลบชนิดที่รองรับ, ชนิดไม่รองรับ, เกิน 20 MB, ชื่อไทย/ชื่อซ้ำ
- ผู้ไม่มีสิทธิ์ต้องเปิด/ลบ attachment ไม่ได้ แม้รู้ URL/ID
- หลังส่ง/approved/cancelled การเพิ่มหรือลบต้องเป็นไปตาม policy ที่ตกลง; FRD ยังไม่ระบุชัด
- อ้าง: FN-03, API-11

#### R17 Audit และหลักฐาน

- ทุก write มี actor/time/action/before/after ที่ถูกต้อง
- create/edit/submit/approve/reject/resubmit/cancel/attachment ต้อง trace ได้
- ประวัติเป็น append-only; ผู้ใช้ทั่วไปแก้หรือลบไม่ได้
- เหตุผลส่งกลับ/ยกเลิกต้องตรงกับที่แสดงบนจอ
- อ้าง: API §2.3, DB §4.2

#### R18 Multi-tenant / confidentiality

- ใช้ ID จาก tenant อื่นกับ list/detail/PDF/CSV/attachment/API write
- คาด: ไม่พบข้อมูลและเปลี่ยนข้อมูลไม่ได้ทุกช่องทาง
- log/export/notification ต้องไม่ปน tenant
- อ้าง: RLS, Data Classification

#### R19 Notification recipients

- pending→cancelled แจ้ง current approver เท่านั้น
- approved แจ้งผู้รับผิดชอบที่ map เป็น user ได้; ข้อความ free text ที่ map ไม่ได้ต้องไม่ทำ approval ล้ม
- DOA notification ต้องไม่ถูกยิงซ้ำโดย feature
- `ivmb.approved` ต้องไม่ยิงตาม DEC-02
- อ้าง: FN-10, XT-01/03

#### R20 Numbering และ snapshot

- สร้างหลายใบพร้อมกัน → เลขไม่ซ้ำ
- ยกเลิก/ล้มหลังขอเลข → gap ยอมรับได้ตาม `no-gap ✗`
- เปลี่ยนชื่อ/ตำแหน่ง maker หรือชื่อ/โลโก้บริษัทภายหลัง → เอกสารเดิมใช้ snapshot เดิม
- doc type inactive: สร้างไม่ได้ แต่ใบเดิมต้องยังดูได้ตาม policy
- อ้าง: BR-10, FN-04, EC-10

## 6. จุดเสี่ยง/คำถามที่ควรยกกับ PM/BA ก่อนเซ็นรับรอง

### Q1 — จุดประสงค์ธุรกิจของ “ติดตามงาน”

FRD ล็อกใบหลังอนุมัติและไม่ให้อัปเดตความคืบหน้าหลังอนุมัติ ถ้าผู้ใช้คาดว่าจะใช้ใบนี้ติดตามงานจริงหลังอนุมัติ ฟีเจอร์จะไม่ตอบโจทย์ แม้ทำตรง FRD ต้องให้ PM/BA ยืนยันว่าเป็น baseline approval เท่านั้น หรือเปิด change request แยก

### Q2 — PDF “ไม่จำกัดแถว” แต่ “2 หน้าเท่ากัน”

BR-13 ระบุทั้งแถวไม่จำกัดและ PDF 2 หน้า ซึ่งอาจเป็นไปไม่ได้เมื่อข้อมูลมากมาก ต้องกำหนดเพดาน, อนุญาตเพิ่มหน้า, หรือตัดข้อมูลอย่างไร ห้ามยอมรับการหายของข้อมูลเพื่อรักษา 2 หน้า

### Q3 — Progress ว่างและค่าเฉลี่ย

DB อนุญาต `progress_pct` เป็น null แต่ FRD ไม่บอกชัดว่าค่าเฉลี่ยไม่นับ null, นับเป็น 0 หรือบังคับกรอก จึงต้องขอสูตรจาก BA ก่อนตัดสิน defect

### Q4 — ผู้รับผิดชอบเป็น free text แต่ต้องส่ง notification

FRD บอกว่า owner ในแถวเป็นข้อความ และ event approved ส่งให้รายการที่ map เป็น user ได้ ต้องระบุกติกา mapping, ชื่อซ้ำ, หน่วยงาน, คนลาออก และกรณี map ไม่ได้

### Q5 — สิทธิ์ admin ยังคลุมเครือในเอกสาร

Overview ยังเขียนว่า admin role id เป็น OQ-04 แม้สถานะเอกสารบอกว่า OQ สำคัญปิดแล้ว ต้องยืนยัน role production ที่แท้จริงและพิสูจน์ว่าไม่มี role กว้างเกินฝ่ายบริหารการลงทุน

### Q6 — Attachment หลังเปลี่ยนสถานะ

FRD บอกชนิด/ขนาดและ API แต่ไม่บอกชัดว่า draft, pending, approved, cancelled ใครเพิ่ม/ลบ/ดาวน์โหลดได้บ้าง ต้องล็อก policy ก่อน sign-off

### Q7 — การอนุมัติกับ PDF/store/notification ล้มกลางทาง

FRD ไม่ระบุ transaction/retry policy ชัด ควรตกลง expected outcome เพื่อป้องกัน “สถานะ approved แต่ไม่มี final PDF” หรือ notification ซ้ำ

### Q8 — เอกสารมีร่องรอยความไม่สด

Overview ยังมี OQ-03/04/06 และ README ระบุ NO-BROWSER/no e2e report แต่ระบบจริงขึ้น Production แล้ว ให้ขอ FRD revision/build mapping ที่ใช้พัฒนาจริง หาก implementation เปลี่ยนหลัง v1.0 ต้องอัปเดต baseline ก่อนเซ็น

## 7. ชุดขั้นต่ำถ้าเวลามีน้อย

ถ้ามีเวลาเพียงครึ่งวัน ให้รัน R01–R12 โดยให้ความสำคัญ R06–R11 สูงสุด และเก็บ R13/R14 อย่างละหนึ่งเคส ถ้ามีเวลา 1–2 วัน ให้รันครบ R01–R20 พร้อม API/log evidence

ห้ามตัดออก:

- สูตรและ validation
- full approval + reject/resubmit
- permission deny ผ่าน direct URL/API
- approved lock + PDF final
- double-click/idempotency
- stale/concurrent update
- audit และ notification อย่างน้อยหนึ่งเส้นทาง

## 8. วิธีบันทึกผลต่อ scenario

| Field | ต้องบันทึก |
|---|---|
| Scenario | Rxx + ชื่อย่อย |
| FRD trace | AC/BR/FN/TC/EC ที่อ้าง |
| Actor/config | role, DOA, doc type, tenant |
| Test data | doc no และค่าหลัก หลีกเลี่ยงข้อมูลจริง |
| Expected | ค่าหรือสถานะที่ตรวจได้ |
| Actual | สิ่งที่เห็นจริง |
| Result | Pass / Fail / Blocked / Not tested |
| Evidence | screenshot + request/response หรือ log/audit id เมื่อเกี่ยวข้อง |
| Defect | severity + reproduce steps + expected/actual |

Severity แนะนำ:

- Critical — ข้ามสิทธิ์/ข้ามอนุมัติ, ข้อมูลหาย/รั่วข้าม tenant, approved ผิดคน
- High — สูตร/สถานะ/PDF/เลข/notification สำคัญผิด, เอกสารซ้ำ, approved ไม่มี final PDF
- Medium — ผิด FRD แต่มีทางเลี่ยง, audit/CSV/filter/attachment policy ผิด
- Low — ข้อความ/ตำแหน่ง/ความสวยงามที่ไม่กระทบ logic

## 9. เงื่อนไข sign-off

เซ็นรับรองได้เมื่อ:

- AC-01..14 และ TC-D01..06 มีผลจริง ไม่ใช่เพียงอ้าง test รอบเก่า
- P0 ไม่มี Fail/Blocked
- Critical/High = 0 หรือมี risk acceptance ที่ระบุเจ้าของและวันแก้
- Q1–Q8 มีคำตอบหรือถูกบันทึกเป็น accepted gap/change request
- ระบุสิ่งที่ไม่ได้ตรวจอย่างตรงไปตรงมา
- มีหลักฐาน backend สำหรับ permission, audit, event, PDF store, idempotency และ stale อย่างน้อยตาม scenario ข้างต้น

