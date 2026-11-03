# Full Review Plan — บันทึกภายใน (F-TMP-002)

วันที่จัดทำแผน: 3 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: FRD Pack v1.0 ลงวันที่ 7 ตุลาคม 2569  
สถานะเอกสารนี้: **แผนตรวจ — ทุกเคสยังไม่ทดสอบ**

> เอกสารนี้ไม่ใช่ใบรับรองผลและไม่ถือว่าเคสใดผ่าน จนกว่าผู้ตรวจจะทดสอบบนระบบจริงและบันทึก Actual Result + Evidence

## 1. ข้อสรุปสำหรับผู้ตรวจ

อย่าตรวจเฉพาะ happy path ว่า “สร้าง → ส่ง → อนุมัติได้” เพราะความเสี่ยงหลักของฟีเจอร์นี้อยู่ที่:

1. คนที่ไม่มีสิทธิ์มองเห็นหรือแก้เอกสารได้หรือไม่
2. เลขที่เอกสารถูกออกซ้ำ เปลี่ยน หรือออกใหม่หลังถูกตีกลับหรือไม่
3. สายอนุมัติอ่านจาก DOA ตอนส่งและ freeze จริงหรือไม่
4. ผู้อนุมัติผิดลำดับ ผู้จัดทำอนุมัติเอง หรือกดซ้ำได้หรือไม่
5. การตีกลับ/แก้ส่งใหม่/ยกเลิก เปลี่ยนสถานะและรักษาประวัติถูกต้องหรือไม่
6. CSV, ไฟล์แนบ, PDF และ direct URL เคารพสิทธิ์เดียวกับหน้าจอหรือไม่
7. Audit trail และ notification บอกคน เหตุผล และเวลาถูกต้องหรือไม่

ควรใช้ FRD เป็น expected result หลัก แต่ต้องเปิดประเด็นกับ PM/BA เมื่อ FRD ขัดกันหรือยังเป็นค่าชั่วคราว ห้ามเลือก behavior ให้ระบบเอง

## 2. ประเด็นที่ต้องเคลียร์กับ PM/BA ก่อน sign-off

| ID | ประเด็น | หลักฐานในชุดเอกสาร | สิ่งที่ต้องได้คำตอบ |
|---|---|---|---|
| OQ-01 | Scope lock ยังเป็น AI-DEFAULT และรอลูกค้ายืนยัน | FRD `00_OVERVIEW` §คำถามค้าง, `07_LOCKED_DECISIONS` | มติ DEC-01 ถึง DEC-11 ถูกยืนยันแล้วจริงหรือไม่ และหลักฐานอยู่ที่ใด |
| OQ-02 | รหัส `F-TMP-002` / `REQ-TMP-002` ยังระบุว่าเป็นรหัสชั่วคราว | FRD `00_OVERVIEW` Document Control | production ใช้รหัส feature/document type จริงชื่อใด |
| OQ-03 | การไม่อนุมัติขัดกันในรายละเอียด | `05_RULES` ระบุ reject → draft แต่ `03_LOGIC` ระบุ rejected แล้ว owner ต้อง reopen | หลังผู้พิจารณากดไม่อนุมัติ ต้องเป็น `draft` ทันที หรือ `rejected` จนผู้จัดทำกด “แก้แล้วส่งใหม่” |
| OQ-04 | role ฝ่ายกฎหมายไม่มีใน contract เดิม จึงใช้ `role-compliance` ชั่วคราว | FRD `00_OVERVIEW` §คำถามค้าง, `07_LOCKED_DECISIONS` §7.1 | production ต้อง resolve ผู้พิจารณาจาก role ใด และรายชื่อใครบ้าง |
| OQ-05 | ขอบเขต admin ยังตีความได้หลายแบบ | FRD ระบุ “admin role ของหน่วยงานเจ้าของเอกสาร — เห็นทุกใบ” | เห็นทุกใบในหน่วยงาน, บริษัท หรือทุกบริษัท และยกเลิกข้ามหน่วยงานได้หรือไม่ |
| OQ-06 | approve พร้อมข้อคิดเห็น แต่ FRD ไม่บอกชัดว่าข้อคิดเห็นบังคับหรือไม่ | `03_LOGIC` MEM-FN-04 เทียบ MEM-FN-05 | กดอนุมัติโดยไม่ใส่ข้อคิดเห็นได้หรือไม่ |
| OQ-07 | notification ที่ตรวจจาก UI ได้ไม่ครบ | cancel ต้องยิง `mem_cancelled`; DOA engine ยิง `doa_pending`/`doa_result` | ผู้รับ ช่องทาง เนื้อหา และกรณี retry/ส่งซ้ำที่ถูกต้องคืออะไร |

หาก OQ-01, OQ-03, OQ-04 หรือ OQ-05 ยังไม่มีคำตอบ ให้รายงานผลเป็น **ติดเงื่อนไข/รอคำยืนยัน** ไม่ควรรับรอง production แบบสมบูรณ์

## 3. ข้อควรระวังเมื่อทดสอบ production

- อย่าเปลี่ยน DOA, ปิด `doc_type.MEM`, inject error หรือยิง API ข้ามสิทธิ์บน production โดยไม่มี change approval และช่วงเวลาทดสอบที่ตกลงไว้
- ถ้ามี UAT/staging ที่ config เหมือน production ให้ทดสอบ destructive, concurrency และ failure cases ที่นั่น
- หากจำเป็นต้องสร้างข้อมูลบน production ให้ใช้หัวเรื่อง `[TEST-REVIEW-YYYYMMDD]`, ข้อมูลสมมติ, เก็บเลขเอกสารทุกใบ และยกเลิกตามกระบวนการที่ได้รับอนุญาต ห้ามลบ audit trail
- การสร้างร่างจะใช้เลขเอกสารจริงตาม FRD จึงต้องให้ PM/BA ยอมรับ gap ของเลขรันก่อนเริ่ม
- อย่าแนบข้อมูลพนักงาน/ลูกค้าจริง ใช้ไฟล์สมมติที่ไม่มีข้อมูลส่วนบุคคล
- ใช้ Network/DevTools หรือ API client เฉพาะเมื่อได้รับสิทธิ์ ห้ามแก้ payload ของ production โดยพลการ

## 4. ชุดผู้ใช้และข้อมูลที่ต้องเตรียม

| รหัส | ผู้ใช้ | ใช้พิสูจน์ |
|---|---|---|
| U1 | ผู้จัดทำ A | owner, create/edit/submit/reopen/cancel |
| U2 | ผู้พิจารณาขั้น 1 | current approver |
| U3 | ผู้พิจารณาขั้น 2 | future approver/ลำดับการอนุมัติ |
| U4 | พนักงานนอกสาย | data leakage และ direct URL |
| U5 | ผู้ดูแลทะเบียนเอกสาร | admin visibility/cancel scope |
| U6 (ถ้ามี) | ผู้จัดทำ B ต่างหน่วยงาน/บริษัท | tenant/department isolation |

ไฟล์ทดสอบขั้นต่ำ: PDF เล็ก, DOCX, XLSX, JPG/PNG, `.exe`, ไฟล์ 20 MB พอดี, ไฟล์มากกว่า 20 MB เล็กน้อย, ไฟล์เปลี่ยนนามสกุลปลอม และไฟล์ชื่อไทย/ชื่อยาว

## 5. ลำดับทดสอบที่แนะนำ

### รอบ A — Smoke และกฎข้อมูลหลัก

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-01 | U1 สร้างโดยกรอก เรียน/เรื่อง/เนื้อหา แล้วบันทึกร่าง | ได้เลขรูปแบบ production ของ MEM, สถานะร่าง, วันที่วันนี้ | screenshot + doc no | ☐ ยังไม่ทดสอบ |
| RV-02 | ทดสอบเว้นแต่ละ required field ทีละช่อง รวมค่าเป็น space ล้วน | บันทึก/ข้ามขั้นไม่ได้และชี้ช่องที่ขาด | screenshot ทุก field | ☐ ยังไม่ทดสอบ |
| RV-03 | ดับเบิลคลิกบันทึก หรือกดซ้ำระหว่าง spinner | สร้างเพียง 1 record และ 1 doc no | video/network | ☐ ยังไม่ทดสอบ |
| RV-04 | U1 แก้ร่างของตนเองหลายครั้ง | แก้ได้เฉพาะ เรียน/เรื่อง/เนื้อหา/ไฟล์แนบ; doc no ไม่เปลี่ยน | before/after + history | ☐ ยังไม่ทดสอบ |
| RV-05 | เปลี่ยนชื่อ/แผนก U1 หรือข้อมูลบริษัทหลังสร้าง (ทำใน UAT) แล้วเปิดใบเดิม | `from` และ header ของใบเดิมคงค่า snapshot ตอนสร้าง | before/after | ☐ ยังไม่ทดสอบ |
| RV-06 | สร้างใกล้รอยต่อวัน/เขตเวลาไทย (ทำใน UAT) | `doc_date` เป็นวันที่ธุรกิจที่ตกลง ไม่เลื่อนวันจาก UTC | screenshot + server time | ☐ ยังไม่ทดสอบ |

### รอบ B — ส่งอนุมัติและ DOA

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-07 | U1 ส่งร่าง โดยเลือก approver ครบทุกขั้น | สถานะ pending; ขั้นแรก pending; ขั้นถัดไป waiting; มี submitted_at | timeline + network | ☐ ยังไม่ทดสอบ |
| RV-08 | ล้างผู้พิจารณาอย่างน้อย 1 ขั้นแล้วกดส่ง | ส่งไม่ได้และบอกขั้นที่ยังไม่ครบ | screenshot | ☐ ยังไม่ทดสอบ |
| RV-09 | พยายามเลือก U1 เป็น approver; ถ้ามีสิทธิ์ API ให้ตรวจ server-side ด้วย | ไม่มีชื่อให้เลือกและ server ตอบ `SELF_APPROVAL_DENIED` | screenshot/response | ☐ ยังไม่ทดสอบ |
| RV-10 | ตั้ง DOA 2 ขั้นใน UAT ส่งใบ แล้วเปลี่ยน DOA เป็นอีกแบบ | ใบที่ส่งแล้วคง chain เดิม; ใบใหม่ใช้ chain ใหม่ | 2 timelines + config evidence | ☐ ยังไม่ทดสอบ |
| RV-11 | ตั้ง DOA 6 ขั้นใน UAT | modal/timeline มี 6 ขั้นและ PDF มี 6 ช่องลงชื่อแบบ 3+3 | screenshot + PDF | ☐ ยังไม่ทดสอบ |
| RV-12 | ตรวจ notification หลัง submit | U2 ได้ `doa_pending` เพียงครั้งเดียว ผู้ที่ไม่เกี่ยวข้องไม่ได้รับ | notification evidence | ☐ ยังไม่ทดสอบ |

### รอบ C — อนุมัติ, ลำดับ, race condition

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-13 | U2 อนุมัติขั้น 1 พร้อมข้อคิดเห็น | ขั้น 1 approved, ขั้น 2 pending, document ยัง pending, note/เวลา/ผู้อนุมัติถูกต้อง | timeline + PDF preview | ☐ ยังไม่ทดสอบ |
| RV-14 | U3 พยายามอนุมัติก่อนถึงขั้นของตน | ไม่มีปุ่ม; direct call ถูกปฏิเสธ `NOT_CURRENT_APPROVER` | screenshot/response | ☐ ยังไม่ทดสอบ |
| RV-15 | U2/U3 อนุมัติครบทุกขั้น | document เป็น approved; ไม่มี field ธุรกิจอื่นถูกเปลี่ยนและไม่ส่งข้อมูลระบบอื่น | before/after + integration log | ☐ ยังไม่ทดสอบ |
| RV-16 | เปิดใบเดียวกันสอง session แล้วกดอนุมัติ/ไม่อนุมัติใกล้กัน | สำเร็จเพียง action แรก; อีก session ได้ stale state; ไม่มี audit/notification ซ้ำ | video + audit | ☐ ยังไม่ทดสอบ |
| RV-17 | ดับเบิลคลิกปุ่มอนุมัติ | ไม่เกิด approve ซ้ำ, ไม่ข้ามขั้น, ไม่ยิง notification ซ้ำ | network + timeline | ☐ ยังไม่ทดสอบ |
| RV-18 | ทดสอบ approve ไม่กรอกข้อคิดเห็นตามคำตอบ OQ-06 | behavior ตรงมติ PM/BA | screenshot | ☐ ยังไม่ทดสอบ |

### รอบ D — ไม่อนุมัติ, แก้ส่งใหม่, ยกเลิก

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-19 | U2 กดไม่อนุมัติโดยไม่ใส่เหตุผล | ทำรายการไม่ได้และแจ้งให้ระบุเหตุผล | screenshot | ☐ ยังไม่ทดสอบ |
| RV-20 | U2 ไม่อนุมัติพร้อมเหตุผล | สถานะและปุ่มต่อไปตรงคำตอบ OQ-03; ขั้นถัดไป skipped; เก็บเหตุผล/actor/time | timeline + history | ☐ ยังไม่ทดสอบ |
| RV-21 | U1 แก้ใบที่ถูกตีกลับและส่งใหม่ | กลับเป็นร่าง/ส่งใหม่ได้, **doc no เดิม**, audit รอบเก่าไม่หาย, chain resolve ใหม่ | before/after | ☐ ยังไม่ทดสอบ |
| RV-22 | U1 ยกเลิกร่างพร้อมเหตุผล | cancelled; แก้/ส่งต่อไม่ได้; audit มีเหตุผล | screenshot + history | ☐ ยังไม่ทดสอบ |
| RV-23 | U1 ยกเลิก pending พร้อมเหตุผล | cancelled; pending step เป็น skipped; current approver ได้ `mem_cancelled` ครั้งเดียว | status + notification | ☐ ยังไม่ทดสอบ |
| RV-24 | U1/U5 พยายามยกเลิก approved, rejected, cancelled และ U4 พยายามยกเลิกใบคนอื่น | ถูกปฏิเสธทุกกรณีที่ FRD ไม่อนุญาต; สถานะไม่เปลี่ยน | response + status | ☐ ยังไม่ทดสอบ |
| RV-25 | U5 ยกเลิก draft/pending ภายในขอบเขต admin ที่ BA ยืนยัน | ยกเลิกได้เฉพาะ scope ที่ได้รับอนุญาตและต้องมีเหตุผล | screenshot + history | ☐ ยังไม่ทดสอบ |

### รอบ E — สิทธิ์และการรั่วไหลของข้อมูล (P0)

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-26 | ก่อน submit ให้ U2/U4 ค้นในรายการและเปิด direct URL ของร่าง U1 | ไม่พบในรายการ; direct URL ตอบ NOT_FOUND โดยไม่เปิดเผยว่ามี record | screenshot/response | ☐ ยังไม่ทดสอบ |
| RV-27 | หลัง submit ให้ U2, U3, U4 ตรวจรายการ/direct URL | ผู้ที่อยู่ใน approval chain เห็น; U4 ไม่เห็น | screenshots 3 users | ☐ ยังไม่ทดสอบ |
| RV-28 | U4/U2/U5 พยายามแก้ร่าง U1 ด้วย UI และ direct API ตามสิทธิ์ | เฉพาะ owner ของ draft แก้ได้; คนอื่นได้ `NOT_OWNER`/deny | response | ☐ ยังไม่ทดสอบ |
| RV-29 | ทดสอบรายการ, detail, PDF, attachment URL และ CSV ด้วย U4 | ทุกช่องทางบังคับ visibility rule เดียวกัน ไม่มี data leak | responses | ☐ ยังไม่ทดสอบ |
| RV-30 | U5 และ U6 ตรวจขอบเขตหน่วยงาน/บริษัท | admin เห็นเฉพาะขอบเขตที่ BA ยืนยัน; ไม่มีข้าม tenant | screenshots | ☐ ยังไม่ทดสอบ |
| RV-31 | หลัง reject แล้ว reopen เป็น draft ให้ผู้อนุมัติเดิมเปิด URL | behavior ตรง visibility rule ที่ตกลง; ถ้า chain reset และเป็น draft ควรไม่เห็น | response | ☐ ยังไม่ทดสอบ |

### รอบ F — ไฟล์แนบ, CSV และรายการ

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-32 | แนบ PDF/DOCX/XLSX/JPG/PNG ที่ถูกต้องและลบไฟล์ | แนบ/เปิด/ดาวน์โหลด/ลบได้ตามสถานะและสิทธิ์; record อื่นไม่กระทบ | screenshot + download | ☐ ยังไม่ทดสอบ |
| RV-33 | แนบ `.exe`, ไฟล์ปลอมนามสกุล, 20 MB พอดี, >20 MB และหลายไฟล์ผสม | รับเฉพาะชนิดที่อนุญาตและ ≤20 MB; ปฏิเสธเฉพาะไฟล์เสีย | evidence ทุก boundary | ☐ ยังไม่ทดสอบ |
| RV-34 | U4 เปิด attachment URL โดยรู้ URL; owner ลองแก้ไฟล์เมื่อ pending/approved | U4 ถูกปฏิเสธ; mutation หลัง draft เป็นไปตามสิทธิ์เดียวกับเอกสาร | response | ☐ ยังไม่ทดสอบ |
| RV-35 | ค้นหาเลขที่/ผู้จัดทำ/เรียน/เรื่อง, กรองสถานะ/หน่วยงาน, sort, pagination | ผลและจำนวนสอดคล้องทุกครั้ง; reset filter ถูกต้อง | screenshots | ☐ ยังไม่ทดสอบ |
| RV-36 | export CSV หลังใช้ filter ด้วย U1/U2/U4/U5 | มีเฉพาะ rows ที่หน้าจอและผู้ใช้นั้นเห็น; filter ตรง; UTF-8 BOM อ่านไทยได้ | CSV + row count | ☐ ยังไม่ทดสอบ |
| RV-37 | เปิด CSV ตรวจสูตรอันตรายจากค่าที่ขึ้นต้น `=`, `+`, `-`, `@` (UAT) | ไม่ทำให้ spreadsheet execute สูตรจากข้อมูลผู้ใช้ | CSV evidence | ☐ ยังไม่ทดสอบ |

### รอบ G — PDF, snapshot, audit และความทนทาน

| ID | วิธีทดสอบ | Expected จาก FRD | หลักฐานที่เก็บ | ผล |
|---|---|---|---|---|
| RV-38 | ตรวจ PDF ของ draft/approved/rejected/cancelled | สถานะ, checkbox, เหตุผล, note และลายเซ็นตรง record; ไม่มีช่องผู้จัดทำเพิ่ม | PDFs | ☐ ยังไม่ทดสอบ |
| RV-39 | ใส่เนื้อหาไทยยาว หลายย่อหน้า/อักขระพิเศษและ DOA หลายขั้น | ไม่ตัดข้อความ/ช่องลงชื่อกลางหน้า; อ่านได้ครบ | PDF ทุกหน้า | ☐ ยังไม่ทดสอบ |
| RV-40 | เทียบ `doc_date` กับ `legal_opinion_date` | เป็นคนละค่าและสะท้อนเวลาสร้างกับเวลาพิจารณาจริง | PDF + timeline | ☐ ยังไม่ทดสอบ |
| RV-41 | หลัง approved เปลี่ยนข้อมูล master/ชื่อ approver (UAT) แล้วเปิด final PDF | approved final copy คงข้อมูล ณ เวลาที่อนุมัติ ไม่ drift ตาม master | before/after PDF | ☐ ยังไม่ทดสอบ |
| RV-42 | ไล่ History ตั้งแต่ create → edit → submit → approve/reject/reopen/cancel | append-only, เรียงเวลา, actor/action/reason ครบ, ไม่มีรายการหายหรือซ้ำ | full history | ☐ ยังไม่ทดสอบ |
| RV-43 | จำลอง server fail/upload fail ใน UAT | แจ้งล้มเหลว, ไม่สร้าง record/doc no/audit ซ้ำ, retry ได้อย่างปลอดภัย | video + logs | ☐ ยังไม่ทดสอบ |
| RV-44 | logout/session หมดอายุระหว่างกรอกหรือก่อน action สำคัญ | ไม่บันทึกด้วย user ผิด, ไม่ค้างสถานะกึ่งสำเร็จ, กลับมาแล้วเห็นข้อมูลที่ commit จริง | video | ☐ ยังไม่ทดสอบ |

## 6. เกณฑ์ตัดสิน

- **ไม่ผ่าน:** พบข้ามสิทธิ์/ข้อมูลรั่ว, อนุมัติผิดคนหรือผิดลำดับ, เลขซ้ำ/เลขเปลี่ยน, ข้อมูลหรือ audit สูญหาย, state ผิดจนธุรกิจทำงานต่อไม่ได้
- **ผ่านแบบมีเงื่อนไข:** พบ logic fail 1–2 ข้อ หรือมี High bug ที่มีแผนแก้และต้อง retest; หรือ OQ สำคัญยังไม่มีหลักฐานยืนยัน
- **ผ่าน:** P0 ทั้งหมดผ่าน, เคส FRD สำคัญมีหลักฐาน, ไม่มี Critical/High ค้าง และ PM/BA ยืนยัน OQ ที่กระทบ behavior แล้ว

Severity ที่แนะนำ:

- Critical — ข้ามสิทธิ์/ข้าม tenant, อนุมัติแทนกัน, audit ถูกแก้หรือลบ, ข้อมูลหาย
- High — เลขซ้ำ/เลขเปลี่ยน, สถานะผิด, approver ผิด, CSV/PDF/notification ส่งข้อมูลผิดคน
- Medium — ผิด FRD แต่มีทางเลี่ยง, history ไม่ครบ, filter/export บางกรณีผิด
- Low — ข้อความ/ตำแหน่ง/รูปแบบที่ไม่กระทบ logic

## 7. รูปแบบจด Bug ให้ทำซ้ำได้

```text
BUG-ID:
หัวข้อ:
Severity:
Environment / build / เวลา:
User/Role:
Precondition (doc no/status/DOA):
Steps:
1.
2.
Expected ตาม FRD:
Actual ที่เห็น:
Evidence (ภาพ/วิดีโอ/network/log):
Record ID / Doc No:
ความถี่: ทุกครั้ง / บางครั้ง (__/__)
ผลกระทบทางธุรกิจ:
```

## 8. หลักฐานขั้นต่ำก่อนปิดงาน

- ตารางผล RV-01 ถึง RV-44 พร้อม Pass/Fail/Blocked/NA และเหตุผลของ NA
- เลขเอกสารทดสอบและผู้ใช้ที่ใช้ทุก flow
- ภาพหรือวิดีโอของ state transition สำคัญ
- หลักฐาน direct URL/API สำหรับ permission cases ไม่ใช่ดูแค่ว่าปุ่มหาย
- CSV จริงและ PDF จริงอย่างน้อย draft, approved, rejected/cancelled
- History/Audit เต็ม flow อย่างน้อย 1 ใบ
- หลักฐาน notification ของ submit, result และ cancel pending
- คำตอบ PM/BA ของ OQ-01 ถึง OQ-07
- Bug list และผล retest แยกรอบอย่างชัดเจน

เมื่อมีผลจริงครบ จึงนำผลไปสร้าง Feature Check Report โดยห้ามเติม Pass ให้เคสที่ไม่ได้ทดสอบ
