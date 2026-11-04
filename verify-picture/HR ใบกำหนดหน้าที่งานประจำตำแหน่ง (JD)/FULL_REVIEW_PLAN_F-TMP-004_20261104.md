# Full Review Plan — F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD)

วันที่จัดทำแผน: 4 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: FRD Pack v1.0 (`00_OVERVIEW` ถึง `07_LOCKED_DECISIONS`)  
เอกสารช่วยตรวจช่องว่าง: AI Test Cases 54 เคส, QA Audit, DOA/DOCCFG/NTF Brief  
สถานะเอกสารนี้: **แผนตรวจ — ยังไม่ใช่ผลรับรองผ่าน/ไม่ผ่าน**

## 1. ข้อสรุปสำหรับผู้ตรวจ

งานรอบนี้ไม่ควรเสียเวลา recheck layout ทุกจุด เพราะได้รับการยืนยันว่า UI ปรับแล้ว แต่ต้องตรวจว่า “ข้อมูลและสถานะเดินถูกคน ถูกลำดับ และไม่เสียเมื่อเกิดเหตุผิดปกติ” โดยให้น้ำหนักตามนี้:

1. **P0 — สิทธิ์และการอนุมัติ:** คนที่ไม่เกี่ยวต้องมองไม่เห็น/ทำรายการไม่ได้, ผู้จัดทำอนุมัติเองไม่ได้, อนุมัติได้เฉพาะขั้นปัจจุบัน
2. **P0 — วงจรชีวิตเอกสาร:** draft → pending → approved → acknowledged/superseded และ reject/cancel ต้องไปสถานะถูกต้องโดยไม่เปลี่ยนเลขเดิมผิดกฎ
3. **P0 — ฉบับใช้งานเดียวต่อตำแหน่ง:** อนุมัติฉบับใหม่แล้วฉบับเดิมต้องถูกแทนที่แบบ atomic และไม่เหลือ active สองฉบับ
4. **P1 — ข้อมูล snapshot และ PDF:** การเปลี่ยน Position/Organization ภายหลังต้องไม่ย้อนเปลี่ยนเอกสารเก่า; PDF ต้องตรงข้อมูลและสายอนุมัติจริง
5. **P1 — การเชื่อมระบบ:** เลขเอกสาร, DOA, notification, attachment และ CSV ต้องทำงานจริง ไม่ใช่เพียงหน้าจอแสดงเหมือนสำเร็จ
6. **P1 — ความทนทาน:** double-click, refresh, เปิดสองแท็บ, stale version, network retry ต้องไม่สร้างเลข/การตัดสิน/notification ซ้ำ

## 2. เงื่อนไขก่อนเริ่มและหลักฐานที่ต้องขอ

หากข้อใดหาไม่ได้ ให้ลงผลเป็น `ไม่สามารถตรวจ` พร้อมเหตุผล ห้ามตีความเป็นผ่าน

- [ ] ระบุ environment/build ที่ตรวจ และยืนยันว่าเป็น build เดียวกับ Production ปัจจุบัน
- [ ] มีบัญชีทดสอบอย่างน้อย 5 persona: Owner, Current Approver, Future/Other Approver, HR (`role-mgr-hr`), Incumbent และควรมี Outsider อีก 1 คน
- [ ] มีตำแหน่งทดสอบอย่างน้อย 3 แบบ: มีหัวหน้าปกติ, ไม่มี `reports_to`, และมี JD ฉบับใช้งานอยู่แล้ว
- [ ] ทราบค่า DOA จริงใน Production ว่ามีกี่ขั้น/role ใด และ `role-line-manager` resolve ได้จริง
- [ ] เปิดดู Audit/History, Notification Center, PDF, CSV และ attachment ได้
- [ ] มีวิธีตรวจเลขเอกสารและสถานะฉบับเก่า หรือมีผู้ดูแลช่วย query/log ให้
- [ ] เตรียมไฟล์แนบที่อนุญาต, ไฟล์ชนิดต้องห้าม และไฟล์เกินขนาดตาม policy กลาง
- [ ] ใช้ข้อมูลทดสอบที่ไม่ใช่ข้อมูลส่วนบุคคลจริง หรือได้รับอนุญาตแล้ว

## 3. จุดเอกสารที่ต้องยืนยันกับ PM/BA ก่อนลงนาม

DevPack ที่ได้รับมีประเด็นค้างดังนี้ แม้ระบบจะขึ้น Production แล้วก็ตาม จึงต้องถามว่าถูกปิดด้วยมติ/เอกสารฉบับใด:

| จุดค้างใน source | ความเสี่ยง | คำถามที่ต้องได้คำตอบ |
|---|---|---|
| DEC-01..12 เป็น `AI-DEFAULT` และระบุว่ารอลูกค้ายืนยัน | ระบบอาจทำงานตรง FRD แต่ไม่ตรงธุรกิจจริง | ลูกค้า/Process Owner ยืนยัน 12 มตินี้แล้วหรือไม่ อยู่ในเอกสารใด |
| DOA Brief ระบุ `wire_status: pending` และ role ค่าเริ่มยังรอยืนยัน | ส่งแล้วอาจวิ่งผิดคน หรือ hardcode | Production ใช้ DOA entry ใด จำนวนกี่ขั้น และ owner ของ config คือใคร |
| OQ-03 ระบุเพียง “ตัวชี้วัด” | ความหมาย/รูปแบบ KPI ไม่ชัด | KPI เป็นข้อความอิสระจริงหรือมีมาตรฐาน/validation เพิ่ม |
| OQ-05 รหัส feature/REQ จริงและชื่ออังกฤษใน Position master ยังไม่ปิด | trace/log/config อาจอ้างรหัสชั่วคราว | Production ใช้ feature id/doc type ใด และชื่ออังกฤษมาจาก master หรือผู้ใช้กรอก |
| QA Audit เป็น `[NO-BROWSER]` และตัด cross-module notification/บาง PDF ออกจากเอกสารคน | หลักฐานชุดนี้ไม่ยืนยัน integration จริง | มีผล E2E/Production smoke test ของ notification, PDF หลายขั้น และ browser จริงหรือไม่ |

## 4. Test data ที่ควรสร้าง

| ชุด | ใช้ทดสอบ | ข้อมูลสำคัญ |
|---|---|---|
| D1 Normal | happy path | ตำแหน่งมีหัวหน้า, ลูกน้อง 2 ตำแหน่ง รวม 3 คน, เนื้อหาครบ |
| D2 Top position | edge master | ตำแหน่งไม่มี `reports_to`; ผู้ใช้ต้องกรอก reports_to/หัวหน้าเอง |
| D3 Existing active | supersede | ตำแหน่งเดียวกันมี approved หรือ acknowledged อยู่แล้ว |
| D4 Long content | PDF/data | ข้อความไทย/อังกฤษยาว, ขึ้นบรรทัดใหม่, 12 แถวลูกน้อง |
| D5 Invalid | validation | จำนวน 0, ติดลบ, ทศนิยม, ตัวอักษร, มีจำนวนแต่ไม่มีตำแหน่ง, ไม่มี KPI |
| D6 Multi-step DOA | approval | DOA อย่างน้อย 2 ขั้น; ถ้าทำได้ใช้ 6 ขั้นเพื่อตรวจช่องลงนาม PDF |
| D7 Concurrency | race/retry | ผู้ใช้สอง session/สองแท็บเปิดเอกสาร version เดียวกัน |

## 5. ลำดับการเล่น Full Flow

### Flow A — สร้างร่างและตรวจ snapshot (P0/P1)

- [ ] A01 เลือกตำแหน่ง D1: ชื่อไทย/แผนก/ฝ่ายมาจาก master และแผนก/ฝ่ายแก้ไม่ได้; reports_to กับหัวหน้าแถวแรกเติมถูกคน
- [ ] A02 เปลี่ยน `reports_to`: เปลี่ยนได้เฉพาะใน JD และกลับไปดู Position master แล้วต้องไม่ถูกแก้ตาม
- [ ] A03 กรอกเฉพาะตำแหน่งแล้วบันทึกร่าง: ต้องบันทึกได้แม้ข้อมูลก่อนส่งยังไม่ครบ เพราะ draft ตรวจเฉพาะ `position_id`
- [ ] A04 บันทึกครั้งแรก: ได้เลข JD ทันทีเพียงเลขเดียว รูปแบบตรง config และ refresh แล้วเลขไม่เปลี่ยน
- [ ] A05 กดบันทึกซ้ำ/ดับเบิลคลิก/รีเฟรชช่วงกำลังบันทึก: ต้องไม่เกิดเอกสารหรือเลขซ้ำ
- [ ] A06 แก้ร่าง: owner แก้ได้; ผู้ใช้อื่นและ HR ที่ไม่ได้เป็นเจ้าของแก้ไม่ได้
- [ ] A07 เปลี่ยนชื่อแผนก/ฝ่าย/ชื่อบริษัท/โลโก้ใน master หลังออกเลข (ใช้ข้อมูลทดสอบและประสาน admin): เอกสารเดิมและ PDF ต้องใช้ snapshot เดิม; เอกสารใหม่ใช้ค่าปัจจุบัน

### Flow B — Validation และ calculation (P0)

- [ ] B01 เว้น `position_name_en`, `reports_to`, job purpose, responsibility, specification, KPI ทีละช่องแล้วลองส่ง: ต้องบล็อกตรงช่องและข้อความตรง FRD
- [ ] B02 ไม่กรอก `other_qualifications`: ต้องส่งได้
- [ ] B03 ไม่มีหัวหน้าเลย: ต้องบล็อก “ต้องมีผู้บังคับบัญชาโดยตรงอย่างน้อย 1 แถว”
- [ ] B04 หัวหน้าแถวแรกต่างจาก reports_to: ต้องเตือนแต่ยังส่งได้ ไม่ใช่บล็อก
- [ ] B05 headcount = 0/ติดลบ/ทศนิยม/ตัวอักษร: ต้องไม่ผ่าน server validation แม้หลบ client validation ได้
- [ ] B06 มี headcount แต่ไม่มีตำแหน่ง: ต้องบล็อก; มีตำแหน่งต้องกำหนดจำนวนเต็มอย่างน้อย 1
- [ ] B07 ลูกน้อง 2 แถวจำนวน 1+2: summary ต้องเป็น `2 ตำแหน่ง · 3 คน` ทั้งหน้า detail, CSV (ถ้ามีคอลัมน์) และ PDF
- [ ] B08 ไม่มีลูกน้อง: summary ต้องเป็น `ไม่มี`
- [ ] B09 ข้อความหลายบรรทัด/อักขระพิเศษ/ไทย-อังกฤษ: บันทึกและ PDF ต้องไม่ตัด, ไม่กลายเป็น HTML/script และกลับมาแก้แล้วข้อมูลเท่าเดิม
- [ ] B10 ตำแหน่ง D2 ไม่มี reports_to: ระบบต้องให้กรอก reports_to และหัวหน้าเองจนส่งได้ตาม EC-01

### Flow C — ส่งอนุมัติและ freeze สาย (P0)

- [ ] C01 เปิด DOA preview: จำนวนขั้น/role/ค่าเริ่มต้นตรง config Production ไม่ใช่ค่าที่ hardcode ใน feature
- [ ] C02 กรณี resolve line manager ไม่ได้: slot ต้องว่างและบังคับเลือกผู้อนุมัติ
- [ ] C03 ผู้จัดทำต้องไม่อยู่ในรายชื่อผู้อนุมัติ และถ้าฝืนเรียก API ต้องถูกปฏิเสธ
- [ ] C04 ส่งโดยไม่เลือก assignee ครบทุกขั้น: ต้องบล็อก; เลือกครบแล้วจึงเป็น pending
- [ ] C05 หลังส่ง: เนื้อหาและ attachment ที่ FRD ไม่อนุญาตให้แก้ต้องถูกล็อกทั้ง UI และ API
- [ ] C06 หลังส่งแล้วเปลี่ยน DOA config: ใบเดิมต้องใช้ approval chain snapshot เดิม; ใบใหม่ใช้ config ใหม่
- [ ] C07 ส่งซ้ำ/double-click/network retry: ต้องมี transition และ notification `doa_pending` ชุดเดียว
- [ ] C08 ตรวจ My Approval/รายการของ current approver: เห็นใบและทำรายการได้; future approver ยังตัดสินไม่ได้

### Flow D — Approve / Reject / Resubmit (P0)

- [ ] D01 owner กดอนุมัติใบตัวเอง: UI ไม่มีสิทธิ์และ API ตอบปฏิเสธ
- [ ] D02 ผู้อนุมัติที่ไม่ใช่ขั้นปัจจุบันกดอนุมัติ/ไม่อนุมัติ: ต้องถูกปฏิเสธ
- [ ] D03 current approver อนุมัติขั้นแรก: ใบยัง pending, ขั้นถัดไปเป็น current, ประวัติขั้นแรกไม่เปลี่ยนย้อนหลัง
- [ ] D04 ผู้อนุมัติสอง session กดตัดสินเอกสารเดียวกันพร้อมกัน: ต้องสำเร็จเพียงครั้งเดียว อีกครั้งได้ conflict/สถานะล่าสุด ไม่บันทึกซ้ำ
- [ ] D05 ไม่อนุมัติโดยไม่ใส่เหตุผล: ต้องบล็อก; ใส่เหตุผลแล้วกลับ draft และใช้เลขเดิม
- [ ] D06 หลัง reject: owner เห็นเหตุผล/ประวัติเดิม แก้ได้ และส่งใหม่แล้วระบบ resolve/freeze chain ชุดใหม่
- [ ] D07 อนุมัติขั้นสุดท้าย: status approved, approved_by/เวลา/ประวัติถูกต้อง และมี approved PDF snapshot
- [ ] D08 เปิดสองแท็บแล้วแท็บหนึ่งแก้/ส่งก่อน: อีกแท็บต้องได้ `STALE_VERSION` หรือบังคับ reload ไม่เขียนทับข้อมูลใหม่

### Flow E — Incumbent และ acknowledgement (P0/P1)

- [ ] E01 ก่อน approved ผู้ดำรงตำแหน่งเปิดด้วย URL ตรง: ต้อง 404 และไม่รั่วชื่อ/ข้อมูลเอกสาร
- [ ] E02 เฉพาะ HR ระบุ/เปลี่ยน incumbent ใน approved ได้; role อื่นต้องถูกปฏิเสธ
- [ ] E03 ระบุ incumbent แล้ว: คนที่ระบุเห็นใบและได้ `jd_ack_requested` เพียงหนึ่งครั้ง
- [ ] E04 คนอื่นกดรับทราบ: ต้อง 403 `NOT_INCUMBENT`
- [ ] E05 incumbent กดรับทราบ: approved → acknowledged, เวลารับทราบและ PDF ถูกต้อง, `jd_acknowledged` ส่งถึง owner และ HR
- [ ] E06 กดรับทราบซ้ำ/สองแท็บ: ต้องไม่สร้าง audit หรือ notification ซ้ำ
- [ ] E07 owner เป็น incumbent คนเดียวกัน: หลัง approved รับทราบได้ แต่ยังต้องไม่สามารถอนุมัติใบตัวเอง

### Flow F — Supersede ฉบับเดิม (P0 สูงสุด)

- [ ] F01 ใช้ D3 สร้างฉบับใหม่: ต้องมีคำเตือนว่ามีฉบับใช้งานอยู่ แต่ยังสร้าง/ส่งได้ตาม FRD
- [ ] F02 ก่อนฉบับใหม่อนุมัติสุดท้าย: ฉบับเดิมยังเป็น active และผู้ใช้ยังอ้างอิงได้
- [ ] F03 เมื่อฉบับใหม่ approved: ฉบับเดิมเปลี่ยนเป็น superseded, มี `superseded_by`, ฉบับใหม่เป็น active เพียงฉบับเดียว
- [ ] F04 ถ้าฉบับเดิมเป็น acknowledged: ต้องถูก supersede ได้และประวัติการรับทราบเดิมยังอยู่
- [ ] F05 สองใบของตำแหน่งเดียวกันถูกอนุมัติขั้นสุดท้ายพร้อมกัน: ต้องเหลือ active เพียงหนึ่งฉบับและไม่เกิด 500/ข้อมูลครึ่งทาง
- [ ] F06 `jd_superseded` ต้องออกหนึ่งครั้งต่อใบเดิมและระบุเลขฉบับใหม่ถูกต้อง
- [ ] F07 ผู้ดำรงตำแหน่งยังดูฉบับ superseded ของตนได้ แต่ต้องแยกชัดว่าไม่ใช่ฉบับใช้งาน

### Flow G — Cancel (P0/P1)

- [ ] G01 owner ยกเลิก draft/pending ได้เมื่อใส่เหตุผล; ไม่ใส่ต้องบล็อก
- [ ] G02 HR ยกเลิก draft/pending ของผู้อื่นได้; approver/incumbent/outsider ทำไม่ได้
- [ ] G03 approved/acknowledged/superseded/cancelled ต้องยกเลิกซ้ำไม่ได้
- [ ] G04 ยกเลิกจาก pending: current approval step เป็น skipped, ส่ง `jd_cancelled` ถึง current approver และ owner เพียงครั้งเดียว
- [ ] G05 ยกเลิกจาก draft: ไม่ควรยิง event ที่ FRD กำหนดเฉพาะ pending
- [ ] G06 cancel แข่งกับ approve คนละ session: ต้องจบสถานะเดียวแบบ atomic ไม่ใช่ทั้ง approved และ cancelled

### Flow H — Permission, tenant และข้อมูลรั่ว (P0 สูงสุด)

- [ ] H01 Owner เห็น draft ของตน แต่ approver/คนอื่นไม่เห็นก่อนส่ง
- [ ] H02 หลังส่ง approver ใน chain เห็นใบ; approver ที่ไม่อยู่ chain และ outsider ไม่เห็น
- [ ] H03 HR เห็นทุกใบใน tenant แต่ห้ามข้าม tenant
- [ ] H04 incumbent เห็นเฉพาะ approved/acknowledged/superseded ที่ระบุตน ไม่เห็น pending/draft
- [ ] H05 ทดสอบ URL/API id ที่ไม่มีสิทธิ์: ต้อง 404 ไม่ใช่ 403 เพื่อไม่เปิดเผยว่าเอกสารมีอยู่
- [ ] H06 CSV ของแต่ละ persona ต้องมีเฉพาะแถวที่ persona นั้นเห็น และต้องไม่ export PII/คอลัมน์เกิน FRD
- [ ] H07 ค้นหา/filter/count/badge ต้องคำนวณหลัง permission filter ไม่รั่วจำนวนเอกสารที่มองไม่เห็น
- [ ] H08 attachment และ PDF URL โดยตรงต้องใช้ permission เดียวกับเอกสาร ไม่ใช่รู้ URL แล้วเปิดได้
- [ ] H09 เปลี่ยน `X-Tenant`/tenant context ด้วย request ที่ไม่ได้รับสิทธิ์: ต้องไม่อ่านหรือเขียนข้าม tenant

### Flow I — PDF, CSV, attachment และ audit (P1)

- [ ] I01 PDF ทุกสถานะมีเลข JD และไม่มี placeholder เช่น `{{...}}`; draft มีคำว่า “ร่าง”
- [ ] I02 PDF approved/acknowledged แสดงผู้จัดทำ + ช่องต่อ DOA ทุกขั้น + incumbent; ข้อความเป็น “ส่ง/พิจารณา/รับทราบในระบบ” พร้อมวันเวลา ไม่ใช้ภาพลายเซ็น
- [ ] I03 D4 มีลูกน้อง 12 แถวและข้อความยาว: แสดงครบ, ลำดับไม่สลับ, ช่องลงนามไม่ถูกตัดกลางหน้า
- [ ] I04 D6 หลายขั้น: จำนวนช่องลงนามเพิ่มตาม chain จริง ไม่ fix 1 ขั้น; 6 ขั้นควรจัดรวม requester/incumbent เป็น 8 ช่อง 2 แถว
- [ ] I05 approved final PDF ที่เก็บไว้ต้องไม่เปลี่ยนเมื่อข้อมูล/ชื่อพนักงาน/master เปลี่ยนภายหลัง
- [ ] I06 CSV เคารพ search/filter/sort/permission, encoding ภาษาไทยเปิดได้, ไม่มี formula injection จากค่าที่ขึ้นต้น `=`, `+`, `-`, `@`
- [ ] I07 แนบ/ลบไฟล์ตามสิทธิ์และสถานะ; ไฟล์ต้องห้าม/เกินขนาดถูกปฏิเสธ; URL ดาวน์โหลดไม่เปิดสาธารณะ
- [ ] I08 Audit เป็น append-only และมี actor/เวลา/note ครบสำหรับ create, edit, submit, approve, reject, cancel, set incumbent, acknowledge, supersede
- [ ] I09 เวลาในหน้าจอ/PDF/audit ใช้ timezone เดียวกันและเรียงลำดับเหตุการณ์ถูกต้อง

### Flow J — Failure recovery / production behavior (P1)

- [ ] J01 ปิด doc type JD: ปุ่มสร้าง disabled และ API ตอบ `DOC_TYPE_INACTIVE`; เปิดกลับแล้วสร้างได้
- [ ] J02 DOA/Notification/Document Store ช้าหรือ error: ผู้ใช้เห็นผลจริง ไม่แสดง success ก่อน transaction หลักสำเร็จ
- [ ] J03 ถ้า notification ส่งไม่สำเร็จ เอกสารต้องไม่ค้างครึ่งสถานะ และมี retry/หลักฐานให้ตามได้โดยไม่ยิงซ้ำ
- [ ] J04 ถ้าเก็บ approved PDF ไม่สำเร็จ ต้องทราบว่าระบบ rollback approval หรือมี recovery queue ตามมาตรฐานใด
- [ ] J05 กด back/refresh/session timeout กลาง wizard: ข้อมูลที่บันทึกแล้วไม่หาย และข้อมูลที่ยังไม่บันทึกต้องมีคำเตือน
- [ ] J06 เปิดรายการจำนวนมาก: pagination/sort/filter ให้ผลคงที่ ไม่มีรายการซ้ำหรือหายระหว่างเปลี่ยนหน้า

## 6. เคส Business Sense ที่ FRD ยังไม่ตอบชัด — อย่าตัดสินเอง

รายการเหล่านี้ให้เปิด OQ/ถาม PM-BA-Owner ก่อนจัดเป็น Bug เพราะ FRD ยังไม่กำหนดคำตอบครบ:

1. ถ้า HR เปลี่ยน incumbent หลังคนเดิมรับทราบแล้ว ระบบควรกลับ approved, คง acknowledged, หรือสร้างคำขอรับทราบใหม่อย่างไร
2. การแก้/ลบ attachment หลัง submit, approved, acknowledged และ superseded อนุญาตถึงสถานะใด
3. ถ้า employee/approver ถูก deactivate ระหว่าง pending ใคร reassign และ audit อย่างไร
4. ถ้า Position ถูกปิดใช้งานหรือย้าย Org ระหว่าง draft/pending จะส่ง/อนุมัติต่อได้หรือไม่
5. approved final PDF เป็น record ที่แก้ไม่ได้หรือ regenerate ทุกครั้ง; ถ้า template เปลี่ยน เอกสารเก่าควรหน้าตาเดิมหรือใหม่
6. การเปลี่ยน incumbent ควรแจ้งคนเดิมหรือไม่ และต้อง revoke สิทธิ์เห็นฉบับใด
7. การค้นหา/CSV ต้องรองรับข้อมูลขนาดเท่าใด และมี limit/async export หรือไม่
8. เหตุผล reject/cancel และเนื้อหา JD มีข้อจำกัดความยาว/อักขระหรือไม่
9. “ฉบับใช้งานเดียว” ถ้ามีการ import/migration ข้อมูลเก่าที่ซ้ำ ระบบจัดการอย่างไร
10. retention ของ JD, PDF, attachment, audit และข้อมูล PII หลังพนักงานพ้นสภาพเป็นอย่างไร

## 7. เกณฑ์จัดระดับสิ่งที่พบ

| ระดับ | ตัวอย่างในฟีเจอร์นี้ |
|---|---|
| Critical | ข้าม tenant/สิทธิ์, owner อนุมัติเอง, ข้ามลำดับ DOA, active JD สองฉบับ, ข้อมูลหาย/แก้ย้อนหลัง |
| High | สถานะหรือเลขเอกสารผิด, reject/cancel/supersede ผิด, PDF approved ผิดข้อมูล, notification บังคับไม่ถึงผู้รับ |
| Medium | validation ผิดแต่มี workaround, audit ไม่ครบ, CSV/filter ไม่ตรง, retry ทำข้อมูลซ้ำที่แก้ได้ |
| Low | ข้อความ/ตำแหน่ง/spacing ซึ่งไม่กระทบ logic และการตัดสินใจ |

## 8. วิธีบันทึกผลต่อหนึ่งเคส

บันทึกให้ทำซ้ำได้ ไม่เขียนเพียง “ไม่ผ่าน”:

```text
Case: F05
Environment / Build:
Persona:
Document no / Position:
Precondition:
Steps:
Expected (อ้าง FRD/BR/AC):
Actual ที่เห็นจริง:
Evidence: screenshot/video/network/audit/notification/PDF
Result: Pass / Fail / Note / Not tested
Severity (ถ้า Fail):
Cleanup ที่ทำแล้ว:
```

## 9. เกณฑ์จบ Full Review

- ต้องทำ P0 ครบทุกเคส; P0 ที่ `ไม่สามารถตรวจ` ต้องมี owner และเหตุผล ไม่ถือว่าผ่าน
- P1 ที่เกี่ยวกับ integration ต้องมีหลักฐานอย่างน้อยหนึ่งชิ้นจากระบบปลายทาง เช่น notification ที่ได้รับจริง, PDF ที่ดาวน์โหลดจริง, audit หรือ log
- ห้ามรับรองผ่านถ้ายังมี Critical, มี P0 fail, หรือยังไม่ยืนยัน DOA/AI-DEFAULT ที่ Production ใช้จริง
- เมื่อทดสอบเสร็จ ให้นำผลจริงไปทำ Feature Check Report; รายการที่ไม่ได้ทดสอบต้องคงเป็น `na` ห้ามเติม pass จาก FRD หรือคำบอกเล่า

## 10. ชุด Smoke Test แบบสั้น ถ้ามีเวลาเพียง 60–90 นาที

ทำตามลำดับ: A01 → A03 → A04 → B01 → B05 → C01 → C03 → C05 → D02 → D05 → D07 → E01 → E03 → E05 → F03 → F05 → G06 → H05 → H06 → I02 → I05 → J01

ถ้า smoke ชุดนี้ผ่านจึงค่อยขยายไป Full Flow ทั้งหมด; ถ้าพบ Critical ให้หยุดเก็บหลักฐานและแจ้ง PM/BA/Dev ทันที ไม่ควรสร้างข้อมูล Production ต่อโดยไม่จำเป็น
