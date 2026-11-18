# แผน Full Review — F-TMP-007 ใบสรุปประเมินความพึงพอใจลูกค้าต่างประเทศ

วันที่จัดทำ: 18 พฤศจิกายน 2569  
ขอบเขต: ตรวจ Logic และการทำงานหลังขึ้น Production โดยยึด FRD เป็น Acceptance Baseline  
ไม่รวม: การตัดสินความสวยงาม/layout ใหม่ เว้นแต่ UI ทำให้ทำงานผิดหรือเข้าใจผลลัพธ์ผิด

## 1. วิธีตัดสินผล

แยกสิ่งที่พบเป็น 4 ประเภท ห้ามปนกัน

| ประเภท | ใช้เมื่อ | การดำเนินการ |
|---|---|---|
| Bug | ระบบทำไม่ตรง FRD/ผลลัพธ์ผิด/ข้ามสิทธิ์/ข้อมูลผิด | เปิด defect พร้อมหลักฐาน |
| Spec conflict | FRD สองส่วนขัดกันหรือคาดหวังไม่ชัด | ถาม BA/PM ก่อนตัดสิน dev |
| Business risk | ระบบตรง FRD แต่เสี่ยงต่อธุรกิจ | เปิดข้อเสนอ/decision ไม่ลงเป็น bug |
| Not tested | ไม่มีข้อมูล บัญชี สิทธิ์ หรือหลักฐานฝั่ง backend | ระบุข้อจำกัด ห้ามลง Pass |

ระดับความรุนแรงแนะนำ:

- Critical: ข้าม tenant/ข้ามสิทธิ์, เจ้าของอนุมัติตัวเอง, ข้อมูลหายหรือแก้เอกสารอนุมัติแล้วได้
- High: คะแนน/ลูกค้า/สถานะ/เลขเอกสาร/PDF final/notification ผิด, เกิดเอกสารหรือการอนุมัติซ้ำ
- Medium: validation, audit, snapshot, filter/CSV หรือข้อความ error ผิด แต่มีทางเลี่ยง
- Low: ข้อความ/ตำแหน่งที่ไม่ทำให้ logic ผิด

## 2. ข้อควรทำก่อนทดสอบ Production

- ใช้ test tenant หรือชุดข้อมูลที่ PM/BA อนุมัติ ห้ามสร้าง/ยกเลิก/อนุมัติเอกสารลูกค้าจริงเพื่อทดสอบ
- เตรียมบัญชีอย่างน้อย 5 แบบ: owner A, owner B, approver ขั้นปัจจุบัน, approver ที่ยังไม่ถึงขั้น, role-mgr-sales และถ้าเป็นไปได้บัญชีอีก tenant
- ขอสิทธิ์ดูหลักฐาน backend เฉพาะที่จำเป็น: audit log, notification delivery, stored `approved_final`, document number log และ API response/status code
- จด build/version, tenant, เวลาเริ่มทดสอบ, เลขเอกสารทดสอบ และ test data ทุกชุด
- ใช้เดือนทดสอบที่มี SEA สถานะ recorded: 0 ราย, 1 ราย, มากกว่า 8 ราย, ลูกค้าซ้ำหลาย SEA และมีคะแนนต่ำ
- เตรียม SEA หนึ่งใบที่สามารถยกเลิกหลังถูกดึงเข้าร่างได้
- เตรียม DOA 1 ขั้นและหลายขั้น ถ้าแก้ Production ไม่ได้ ให้ทดสอบหลายขั้นใน UAT และลง Production เป็น Not tested

## 3. ลำดับตรวจที่แนะนำ

### Gate A — ยืนยัน Baseline ก่อนลงมือ

| ID | ตรวจ | ผ่านเมื่อ |
|---|---|---|
| A01 | ยืนยันว่า FRD version ที่ PM/BA ให้ยึดคือ v1.0 วันที่ 10 ต.ค. 2569 หรือมีฉบับใหม่กว่า | มี version/ลิงก์หรือคำยืนยันเป็นลายลักษณ์อักษร |
| A02 | ขอหลักฐาน sign-off ของมติ `AI-DEFAULT` 11 ข้อ | มีใบยืนยัน หรือ PM/BA รับทราบว่ายังเป็นความเสี่ยง |
| A03 | ยืนยันผลปิด OQ-02 ถึง OQ-07 | ได้คำตอบเรื่อง DOA role, PDF, การสร้างซ้ำเดือน, code SES/F-TMP-007 |
| A04 | เทียบ role จริงกับ FRD: Maker, Managing Director/role-ceo, role-mgr-sales | mapping ตรงระบบจริงและมี owner ชัดเจน |

ถ้า A01 ไม่ชัด ให้หยุดตัดสิน bug เพราะอาจเทียบผิด baseline; ยังสำรวจระบบและเก็บหลักฐานได้

### Gate B — Security, Permission, Tenant (P0)

| ID | วิธีทดสอบ | Expected ตาม FRD |
|---|---|---|
| B01 | owner A เปิดรายการและยิง URL/API ของ draft owner B | ไม่เห็นใน list; detail ตอบ 404 ไม่เปิดเผยว่ามีเอกสาร |
| B02 | approver เปิด draft ที่ยังไม่ส่ง | ไม่เห็นและ GET detail = 404 |
| B03 | owner พยายาม approve ใบตัวเอง ทั้งจาก UI และ API | ไม่มีปุ่ม; API 403 `NOT_CURRENT_APPROVER`/self approval ถูกบล็อก |
| B04 | approver แก้ draft, cancel ใบคนอื่น หรือส่งแทน owner | UI ไม่มี action; API 403 |
| B05 | approver คนที่ไม่ใช่ขั้นปัจจุบันกดตัดสิน | 403 `NOT_CURRENT_APPROVER`; สถานะไม่เปลี่ยน |
| B06 | role-mgr-sales เปิดทุกสถานะ | เห็นทุกใบใน tenant; cancel ได้เฉพาะ draft/pending; approve ไม่ได้ |
| B07 | คนทั่วไปเปิดใบ owner A และพยายาม cancel | 404 ตอนดูหรือ 403 `NOT_OWNER`; ไม่มีข้อมูลหลุดใน error |
| B08 | เปิด/ค้น/API ด้วยบัญชี tenant B โดยใช้ id/doc no ของ tenant A | ไม่เห็นข้อมูลทุกช่อง, attachment, PDF, CSV และ audit; ควรได้ 404 |
| B09 | ดาวน์โหลด PDF/attachment ด้วย URL เดิมหลัง logout หรือเปลี่ยน user | ต้องตรวจสิทธิ์ใหม่ ไม่ใช่ public/permanent URL ที่ข้ามสิทธิ์ |
| B10 | CSV ด้วย role ต่าง ๆ | ได้เฉพาะรายการที่ role นั้นมองเห็น และไม่มีข้อมูลข้าม tenant |

หยุด release/review และแจ้งทันทีถ้า B01–B10 พบการข้ามสิทธิ์หรือข้าม tenant

### Gate C — ข้อมูลต้นทาง SEA และการเลือกเดือน (P0/P1)

| ID | วิธีทดสอบ | Expected ตาม FRD |
|---|---|---|
| C01 | เลือกเดือนว่างแล้วกดดึง | แจ้งไม่มีลูกค้าเพิ่ม; ส่งไม่ได้เพราะต้องมีอย่างน้อย 1 ราย |
| C02 | เดือนมี SEA recorded 1 ราย | แสดงลูกค้า/เลข SEA/วันที่/คะแนน q1–q10 ตรงต้นทาง |
| C03 | มี SEA สถานะอื่น เช่น draft/cancelled | ไม่ถูกเสนอให้เลือกและไม่ถูกดึง |
| C04 | ลูกค้าหนึ่งรายมี SEA 2 ใบในเดือน | ใช้ใบ `survey_date` ล่าสุดและเตือนว่ามีหลายใบ |
| C05 | เดือนมีมากกว่า 8 ลูกค้า | ดึงสูงสุด 8 และแจ้งจำนวนที่เหลือ; เพิ่มคนที่ 9 ถูกบล็อก |
| C06 | เพิ่มลูกค้าคนเดิมซ้ำผ่าน UI และ API | UI ไม่เสนอซ้ำ; API 422; ไม่มีคอลัมน์ซ้ำ |
| C07 | เปลี่ยนเดือนหลังดึงลูกค้า | ล้างคอลัมน์เดิมและแจ้งชัดเจน |
| C08 | ตรวจหัวข้อ 10 ข้อ/3 กลุ่มและคะแนน | mapping q1–q10 ตรง config/กระดาษ; คะแนน read-only |
| C09 | คะแนน 1–2 หรือ weight ต่ำกว่า threshold config | ไฮไลต์เตือนแต่ไม่บล็อกการส่ง |
| C10 | ดัดแปลง request ส่งชื่อ/คะแนนปลอมจาก browser | server ต้องดึง snapshot จาก SEA เองและไม่เชื่อค่าจาก FE |
| C11 | ยกเลิก SEA หลังดึงเข้าร่าง | ร่างมี stale banner; submit ตอบ 422 `SOURCE_SURVEY_CANCELLED` จนลบคอลัมน์นั้น |
| C12 | เปลี่ยน SEA หลังใบถูกส่งแล้ว | ใบ pending/approved ใช้ snapshot เดิม ไม่เปลี่ยนตามต้นทาง |

ตรวจเพิ่มเชิง business: ถ้า SEA ล่าสุดวัดจาก `survey_date` เท่ากันสองใบ FRD ไม่กำหนด tie-breaker ให้ถาม BA; อย่าคาดเดาเอง

### Gate D — สร้าง/บันทึกร่าง/Validation/เลขเอกสาร

| ID | วิธีทดสอบ | Expected ตาม FRD |
|---|---|---|
| D01 | กดถัดไป/ส่งโดยไม่เลือกเดือนและลูกค้า | แจ้ง `กรุณาเลือกเดือน` และ `เพิ่มลูกค้า...อย่างน้อย 1 ราย` ในจุดที่ถูกต้อง |
| D02 | บันทึกร่างโดยยังไม่มี conclusion | บันทึกได้ตาม AC-01 |
| D03 | ส่งโดยไม่มี conclusion | ส่งไม่ได้; แจ้ง `กรุณาเขียนสรุปผลการประเมิน` |
| D04 | conclusion 1000/1001 ตัวอักษร | 1000 ผ่าน; 1001 ถูกบล็อกทั้ง UI/API |
| D05 | suggestion 1000/1001 ตัวอักษร | ตรวจตาม FN-01/UI แม้ VR table ระบุไม่ครบ; หากผลไม่ชัดให้เป็น spec conflict |
| D06 | บันทึกครั้งแรก | ได้เลข SES จาก Document Config เพียงครั้งเดียวและสถานะ draft |
| D07 | แก้และบันทึก draft ซ้ำ | เลขเดิม ไม่ออกเลขใหม่ |
| D08 | reject แล้วส่งใหม่ | เลขเดิม ไม่ออกเลขใหม่ |
| D09 | กด Save/Submit ซ้ำเร็ว ๆ หรือ retry request เดิมด้วย Idempotency-Key เดิม | เกิดรายการ/transition/notification เพียงครั้งเดียว |
| D10 | สองหน้าต่างแก้ version เดียวกัน | คนหลังได้ 409 `STALE_VERSION`; ไม่ทับข้อมูลเงียบ ๆ |
| D11 | ปิด doc type SES แล้วลองสร้าง | สร้างไม่ได้ 409 `DOC_TYPE_INACTIVE` |
| D12 | แนบไฟล์ชนิด/ขนาดถูกต้องและผิดกติกา | ไฟล์ดีเปิดได้และผูกใบถูกต้อง; ไฟล์อันตราย/เกินขนาดถูกปฏิเสธ; ไม่มีข้าม tenant |

หมายเหตุ: FRD ขัดกันเล็กน้อยเรื่อง `DOC_TYPE_INACTIVE` — §2.2 บอกทุก write แต่ FN-03/EC-10 เน้นตอนสร้าง ต้องให้ BA/DOCCFG owner ยืนยันว่าปิด doc type แล้วใบเดิมยัง approve/cancel ได้หรือไม่

### Gate E — State Machine และ DOA แบบ End-to-End (P0)

รันอย่างน้อย 4 เส้นทาง โดยใช้เอกสารคนละใบเพื่อไม่ปน state

#### E1 Happy path

1. Owner สร้าง draft และ submit
2. ตรวจสถานะ `draft → pending`
3. ตรวจ DOA resolve ตอน submit และผู้สรุปไม่เป็น approver
4. Approver ขั้นปัจจุบัน approve
5. ถ้ามีหลายขั้น สถานะยัง pending และส่งต่อเฉพาะขั้นถัดไป
6. ขั้นสุดท้าย approve → `approved`
7. ตรวจเอกสารถูก lock, แก้/cancel ไม่ได้, มี approved_by/approved_at และ audit ครบ

#### E2 Reject แล้วแก้ส่งใหม่

1. Approver reject โดยไม่กรอกเหตุผล → ต้องบล็อก
2. กรอกเหตุผล → `pending → draft`, เลขเดิม, owner เห็นเหตุผล
3. Owner แก้และส่งใหม่
4. ระบบ resolve DOA ใหม่ตามค่าปัจจุบัน; chain รอบเก่ายังอยู่ใน audit ไม่ถูกเขียนทับ

#### E3 Cancel

1. Owner cancel draft โดยไม่กรอกเหตุผล → บล็อก; กรอกแล้ว → cancelled
2. Owner cancel pending → cancelled, pending step เป็น skipped และผู้อนุมัติปัจจุบันได้รับ `ses_cancelled`
3. role-mgr-sales ทำซ้ำกับ draft/pending → ทำได้
4. approver/คนทั่วไป cancel → ทำไม่ได้
5. cancel approved/cancelled ซ้ำ → 409 `NOT_CANCELLABLE`

#### E4 DOA snapshot

1. ส่งใบด้วย chain A
2. เปลี่ยน DOA กลางเป็น chain B ระหว่าง pending
3. ใบเดิมต้องเดิน chain A ต่อ
4. ใบที่ reject กลับ draft แล้ว submit ใหม่ต้อง resolve เป็น chain B
5. DOA 6 ขั้นต้องทำงานครบทุกขั้นและ PDF มีช่องลงชื่อ 7 ช่อง (ผู้สรุป + 6 approver)

### Gate F — Notification, Audit และผลข้างเคียง

| ID | วิธีทดสอบ | Expected ตาม FRD |
|---|---|---|
| F01 | approve final ใบที่ไม่มีคะแนนต่ำ | ไม่ยิง `ses_low_score_approved` |
| F02 | approve final ใบที่มีคะแนนต่ำหลายช่อง | ยิง event เดียว พร้อม `low_count` และ `low_customers` ถูกต้อง ไป owner + role-mgr-sales |
| F03 | approve ขั้นกลาง | ยังไม่ยิง low-score final event |
| F04 | cancel จาก pending | ยิง `ses_cancelled` ไป approver ขั้นปัจจุบันครั้งเดียว |
| F05 | cancel จาก draft | ไม่ยิง pending-cancel notification ตาม FRD |
| F06 | approve final | `ses.approved` ต้องไม่ยิงในรอบนี้ แม้ประกาศ contract ไว้ |
| F07 | ทุก create/edit/submit/approve/reject/cancel | audit append-only มี actor/time/action/reason/version; user แก้หรือลบย้อนหลังไม่ได้ |
| F08 | retry/double-click | event/audit/state transition ไม่ซ้ำ |

อย่าตัดสิน F01–F08 จาก toast อย่างเดียว ต้องดู Notification Center/outbox/log หรือหลักฐานที่ทีมระบบยอมรับ

### Gate G — PDF, Approved Final และ CSV

| ID | วิธีทดสอบ | Expected ตาม FRD |
|---|---|---|
| G01 | เปิด PDF ของ draft/pending/approved/cancelled | สถานะ/เลข/เดือน/ข้อมูลตรง record และสิทธิ์ผู้เปิดถูกต้อง |
| G02 | เอกสาร 1, 4, 5 และ 8 ลูกค้า | ตารางเติมช่องว่างถูกต้อง รวม 8 คอลัมน์เป็น 2 ชุด × 4 |
| G03 | ตรวจหัวข้อ 10 ข้อ 3 กลุ่ม | ถ้อยคำไทย/mapping/คะแนนตรง snapshot ไม่มี `{{ }}` หลง |
| G04 | conclusion/suggestion ยาว 1000 | PDF ยัง 2 หน้า ไม่มีข้อความหายหรือทับลายเซ็น |
| G05 | DOA 1 และ 6 ขั้น | จำนวน/ลำดับช่องลงชื่อถูกต้อง; คำตัดสิน `รับทราบและอนุมัติ` |
| G06 | approve final | มีไฟล์ immutable ใน Document Store ชนิด `approved_final`; ดาวน์โหลดซ้ำได้และ hash/เนื้อหาไม่เปลี่ยน |
| G07 | เปลี่ยน config/logo/topic หลังอนุมัติ | approved PDF เดิมใช้ snapshot ไม่เปลี่ยนย้อนหลัง |
| G08 | CSV ตาม filter/status/month/search | 1 แถว = 1 ลูกค้า, จำนวนแถวและค่าตรงหน้ารายการ, UTF-8/ภาษาไทยเปิดได้ |
| G09 | CSV field ที่ขึ้นต้น `=`, `+`, `-`, `@` | ถูกป้องกัน spreadsheet formula injection |

### Gate H — รายการ ค้นหา กรอง และความถูกต้องข้ามหน้าจอ

| ID | วิธีทดสอบ | Expected |
|---|---|---|
| H01 | ค้นด้วยเลขเอกสาร ผู้สรุป เดือน ลูกค้า | ผลตรงจริง ไม่เห็นรายการนอกสิทธิ์ |
| H02 | กรองสถานะ/เดือนร่วมกันและ reset | count, rows, pagination ตรงกัน |
| H03 | หน้าเกิน 25 รายการและ sort | ไม่ซ้ำ/ไม่หายเมื่อเปลี่ยนหน้า; sort คงที่ |
| H04 | เทียบ list → detail → PDF → CSV | doc no, month, owner, customer count, low count, status ตรงกันทุกจุด |
| H05 | หลัง action สำเร็จหรือ fail แล้ว refresh/back/reopen | state จริงตรงกับข้อความบนจอ ไม่เกิด optimistic UI ค้าง |

## 4. เส้นทางที่ควร “เล่น” อย่างน้อยในรอบนี้

ถ้ามีเวลาจำกัด ให้รัน 10 ชุดนี้ตามลำดับ:

1. ข้ามสิทธิ์/ข้าม tenant ทั้ง detail, PDF, attachment, CSV
2. สร้างร่างจาก SEA recorded และตรวจคะแนน q1–q10 กับต้นทางทีละช่อง
3. เดือนว่าง, ลูกค้าซ้ำ, มากกว่า 8, หลาย SEA ใช้ใบล่าสุด
4. SEA ถูกยกเลิกหลังดึง แล้วลอง submit
5. Happy path draft → pending → approved พร้อม low-score notification และ approved_final
6. Reject → draft เลขเดิม → เปลี่ยน DOA → submit ใหม่
7. Cancel จาก pending พร้อม reason, skipped step และ notification
8. Double-click/retry + stale version สองหน้าต่าง
9. PDF 8 ลูกค้า + ข้อความ 1000 + DOA หลายขั้น
10. เทียบ list/detail/PDF/CSV/audit ให้ข้อมูลชุดเดียวกัน

## 5. ประเด็น Business Sense ที่ต้องยกให้ PM/BA ไม่ใช่ตัดสินเอง

1. **สร้างหลายใบในเดือนเดียวกันได้** — FRD EC-06 ระบุไม่บล็อกเพราะ OQ-06 ยังไม่ปิด เสี่ยงสรุปซ้ำ/แจ้งเตือนซ้ำ/ผู้บริหารอ่านคนละชุด ควรมี policy ว่าเตือน, block หรือ version
2. **11 มติเป็น AI-DEFAULT** — เช่น 8 ลูกค้าต่อใบ, ออกเลขตอนบันทึกร่าง, reject กลับ draft, admin เห็นทั้งหมด, approval 1 ขั้น ต้องมี sign-off จริง
3. **เลขเอกสารออกตั้งแต่ draft และ no-gap = false** — draft/cancel จะกินเลข เป็น expected ตาม FRD แต่ควรให้ฝ่ายเอกสารยืนยัน
4. **PDF เปลี่ยนจากต้นฉบับแนวนอน 1 หน้าเป็นแนวตั้ง 2 หน้า** — เป็น decision สำคัญต่อเอกสารควบคุม ไม่ควรถือว่าผ่านเพียงเพราะ layout สวย
5. **role-ceo เป็นชื่อชั่วคราว** — ต้องยืนยัน mapping กับ Managing Director จริง มิฉะนั้นอาจส่งผิดคนหรือค้างอนุมัติ
6. **อนุมัติแล้วไม่ส่งต่อระบบอื่น และ `ses.approved` ไม่ยิง** — downstream report อาจไม่รู้ว่ามีใบใหม่ ต้องยืนยันว่าเป็นเจตนาธุรกิจจริง
7. **คะแนนต่ำเป็นเพียงเตือน ไม่บล็อก** — ไม่มี corrective action/owner/SLA ใน feature นี้ ควรถามว่าธุรกิจยอมรับหรือมี process ภายนอก
8. **เลือก SEA ล่าสุดด้วย survey_date** — กรณีวันที่เท่ากันไม่มี tie-breaker ใน FRD ควรกำหนดให้ deterministic
9. **ปิด Document Type แล้วใบเดิมทำอะไรได้** — FRD มีถ้อยคำขัดกันระหว่าง “ทุก write” กับ “สร้างไม่ได้” ต้องตกลงก่อนตี bug
10. **Retention/การลบข้อมูลลูกค้าต่างประเทศ** — FRD ระบุ Confidential และ RLS แต่ไม่ระบุ retention, export logging หรือสิทธิ์ลบ/เก็บถาวร ควรให้ security/data owner รับทราบ

## 6. ช่องโหว่ของ Test Pack เดิมที่รอบนี้ควรเก็บให้ครบ

- QA audit เดิมระบุ `NO-BROWSER`; หลายเคสยังไม่เคยพิสูจน์ด้วย browser จริง
- UAT แบบคนตัดเคส DOA หลายขั้น, stale version และ Doc Config inactive ออก จึงต้องทดสอบเพิ่มใน UAT/API
- ไม่มี cross-tenant case ชัดเจน ทั้งที่ FRD ระบุ PostgreSQL RLS
- Idempotency-Key ถูกกำหนดใน API แต่ Acceptance Criteria ไม่ได้บังคับทดสอบ double-submit/retry
- Notification, Document Store และ audit ต้องตรวจหลักฐาน backend ไม่ใช่แค่ข้อความบน UI
- Suggestion 1000/1001 ตัวอักษรระบุใน logic/UI แต่ validation table ไม่ชัด
- CSV formula injection, attachment authorization และ direct download URL ไม่ได้ถูกระบุเป็น acceptance case

## 7. Template เก็บหลักฐานต่อเคส

| ช่อง | บันทึก |
|---|---|
| Case ID / FRD ref | เช่น E2 / BR-09 / FN-06 |
| Actor / tenant | user, role, tenant |
| Test data | doc no, month, SEA id, customer alias |
| Steps | ขั้นสั้น ๆ ทำซ้ำได้ |
| Expected | ข้อความ/สถานะ/ค่า/API code ที่วัดได้ |
| Actual | สิ่งที่เห็นจริง ห้ามเขียนเพียง “ไม่ผ่าน” |
| Evidence | screenshot/video + request/response + log เวลาเดียวกัน |
| Classification | Bug / Spec conflict / Business risk / Not tested |
| Severity | Critical/High/Medium/Low |

## 8. เกณฑ์ปิดรอบ Review

- P0 permission/tenant/state/SoD ผ่านครบ ไม่มี Critical/High ค้าง
- AC 14, BR 15, VR 7, EC 12 และ Deny 6 มีผล Pass/Fail/Not tested รายข้อ
- ทุก FN-01 ถึง FN-09 มีอย่างน้อยหนึ่ง positive และหนึ่ง negative/recovery path ที่เกี่ยวข้อง
- event, audit, approved_final และ snapshot มีหลักฐานฝั่งระบบ
- ข้อ Not tested ทุกข้อมีเหตุผล/เจ้าของ/แผนทดสอบต่อ
- Business risks และ spec conflicts ถูก PM/BA รับทราบ ไม่ถูกซ่อนเป็น “ผ่านตาม FRD”

