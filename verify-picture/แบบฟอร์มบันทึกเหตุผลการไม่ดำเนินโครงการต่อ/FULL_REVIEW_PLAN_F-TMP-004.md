# Full Review Playbook — F-TMP-004 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ

วันที่จัดทำแผน: 24 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: FRD v1.0 (`00_OVERVIEW` ถึง `07_LOCKED_DECISIONS`)  
วัตถุประสงค์: ตรวจเก็บตกด้าน business logic และการทำงานของระบบที่ขึ้น Production แล้ว โดยไม่รับรอง UI layout ซ้ำ

## 1. ข้อสรุปก่อนเริ่ม

ใช่ — ให้ใช้ FRD เป็นฐานหลักตามคำสั่ง PM/BA แต่ไม่ควรใช้ FRD เป็นหลักฐานว่าระบบ “ผ่านแล้ว” ในตัวเอง ต้องพิสูจน์ 4 ชั้นต่อไปนี้กับระบบจริง:

1. กฎใน FRD ทำงานจริงทั้งกรณีผ่านและกรณีถูกปฏิเสธ
2. state, permission, audit และข้อมูลหลังบ้านเปลี่ยนอย่างถูกต้อง
3. integration ที่ FRD อ้างถึงทำงานจริงและไม่ทำซ้ำ
4. กฎที่ FRD ระบุเป็น AI-DEFAULT หรือ Open Question ได้รับการยืนยันจาก BA/Owner แล้ว

สิ่งที่มีใน context ยังไม่ใช่หลักฐาน Production acceptance:

- Test case 30 เคสระบุชัดว่ารันกับ prototype `feature.html`
- `00_อ่านก่อน.md` ระบุ NO-BROWSER และยังไม่ได้ render PDF/e2e/ภาพ UAT รอบเต็ม
- QA Audit ตัดเคสหลังบ้านบางรายการออกจากเอกสารคน
- Coverage ที่เขียนว่าครบคือ coverage ของข้อกำหนด ไม่ใช่ผลทดสอบระบบ Production

ดังนั้นบทบาทของผู้ review รอบนี้ควรเน้นจุดที่ prototype พิสูจน์ไม่ได้: server validation, สิทธิ์จริง, state transition, audit, concurrency, idempotency, tenant isolation, notification, Document Store, config snapshot และผลกระทบข้ามระบบ

## 2. ข้อที่ต้องถาม PM/BA ก่อนลงนาม

ถ้าคำตอบยังไม่ชัด ให้บันทึกเป็น “Blocked/Business decision pending” ไม่ใช่ Pass หรือ Bug ของ Dev

| ประเด็น | เหตุผลที่ต้องยืนยัน | เอกสารอ้างอิง |
|---|---|---|
| ลูกค้า/Owner ยืนยัน AI-DEFAULT 11 ข้อแล้วหรือยัง | FRD ระบุว่าต้องยืนยันก่อน UAT แต่ไฟล์ยังแสดง OQ-02 | Overview §0.8, Locked Decisions §7.0 |
| Production ใช้ role ใดแทนผู้อนุมัติระดับรองกรรมการ/กรรมการ | `role-gm` ถูกระบุว่าเป็นค่าชั่วคราว | OQ-03, LD-05 |
| ProjectClosure config มี owner และค่าจริงที่อนุมัติแล้วหรือยัง | เหตุผล 8 ข้อและสถานะปิดโครงการมาจาก config ไม่ควร hardcode | OQ-04, BR-01, BR-06 |
| รหัสเอกสาร PCL ผ่านการ register และไม่ชน feature อื่นหรือยัง | เอกสารระบุ OQ-06 ก่อน register | OQ-06, FN-03 |
| เอกสารนี้ต้องผูก/ปิดโครงการต้นทาง FM-BDM-01/03 หรือไม่ | ปัจจุบัน FRD ระบุว่าไม่ผูกและไม่ปิดโครงการต้นทาง | OQ-05, BR-14 |
| Notification ต้องยิงจริงหรือ “ประกาศไว้แต่ไม่ยิง” | DEC-02 เขียนว่าไม่ยิง แต่ FN-09, API cross-module และ NTF declaration สั่งให้ยิง 2 event | DEC-02 เทียบ FN-09 / API §2.X |

ข้อสุดท้ายเป็น source conflict ที่ต้องให้ BA/Architect ตัดสินก่อนใช้ผล notification เป็นเกณฑ์ Pass/Fail

## 3. ขอบเขตที่ปลอดภัยบน Production

- ใช้ tenant/company ทดสอบ, project name ที่ค้นและลบเชิงธุรกิจได้ง่าย เช่น `[REVIEW-241169]-...`, และบัญชีทดสอบที่อนุมัติแล้ว
- ห้ามเปลี่ยน DOA กลาง, ปิด doc type PCL, แก้ ProjectClosure config หรือทดสอบข้าม tenant ในข้อมูลจริงโดยไม่มีผู้ดูแลระบบร่วมด้วย
- ห้ามยกเลิก/อนุมัติเอกสารจริงของผู้ใช้งานเพื่อทดสอบ
- เคสที่ต้องแก้ config, จำลอง concurrent request, ตรวจ event/store/database หรือยิง API โดยตรง ให้ทำใน UAT/test tenant หรือให้ Dev/DBA รันพร้อมหลักฐาน
- หาก Production ไม่มี test tenant ให้ตรวจ Production แบบ read-only และทำ mutation tests ใน UAT build เดียวกันก่อน

## 4. Test personas และข้อมูลขั้นต่ำ

ต้องมีผู้ใช้แยกจริงอย่างน้อย 6 persona ห้ามใช้ account เดียวสลับ role เพราะจะพิสูจน์ segregation of duties ไม่ได้

| Persona | ใช้พิสูจน์ |
|---|---|
| Maker A | สร้าง/แก้/ส่ง/ยกเลิกเอกสารของตน |
| Maker B | มองไม่เห็นและแก้เอกสารร่างของ Maker A ไม่ได้ |
| Approver Step 1 | เห็นหลังส่งและตัดสินได้เฉพาะขั้นปัจจุบัน |
| Approver Step 2 | เห็นเอกสารแต่ตัดสินก่อนคิวไม่ได้ |
| BDM Admin | เห็นทุกใบและยกเลิกได้ แต่แก้/อนุมัติแทนไม่ได้ |
| Outsider หรือผู้ใช้อีก tenant | มองไม่เห็นทั้ง list, detail, PDF และ attachment |

สร้างเอกสารทดสอบอย่างน้อย 5 ใบ:

- D1: happy path สถานะ “ปิดโครงการแล้ว”
- D2: สถานะ “ติดตามเงื่อนไขในอนาคต” สำหรับ notification
- D3: reject ที่ขั้น 1 แล้วแก้และส่งใหม่
- D4: reject ที่ขั้น 2 แล้วแก้และส่งใหม่
- D5: cancel ระหว่าง pending

ทุกใบควรเลือกเหตุผลอย่างน้อย 2 แถว และมีข้อความเฉพาะที่ตามรอยได้ใน detail/evidence/impact/revisit condition

## 5. ลำดับทดสอบแนะนำ

### Phase A — Smoke และกฎข้อมูล (P0)

| ID | วิธีทดสอบ | Expected ที่ต้องเห็น |
|---|---|---|
| A01 | เปิดรายการด้วย Maker A, Maker B, Admin | แต่ละคนเห็นตาม BR-13; ร่างของ A ไม่รั่วถึง B |
| A02 | สร้างฟอร์มใหม่ | เหตุผลครบตาม config, ค่าเริ่ม “ไม่ใช่”, owner เริ่มเป็นผู้จัดทำ, วันที่เริ่มเป็นวันนี้ |
| A03 | กดถัดไป/บันทึกโดยเว้น required และกรอก whitespace | server ต้องไม่รับ; ข้อความ VR-01/02/04 แสดงตรงจุด |
| A04 | ไม่เลือก “ใช่” สักเหตุผล | บล็อกด้วย VR-02 ทั้ง UI และ API |
| A05 | เลือกเหตุผลปกติและ “เหตุผลอื่น” เป็นใช่แต่ไม่กรอกรายละเอียด | บล็อกทุกแถวที่เลือกใช่; เหตุผลอื่นมีข้อความเฉพาะ |
| A06 | กรอก detail/evidence/impact/revisit แล้วเปลี่ยน ใช่→ไม่ใช่ | ช่องถูก disable และล้างจริง; refresh แล้วข้อมูลไม่กลับ; PDF ไม่มีข้อความเก่า |
| A07 | เลือก follow โดยไม่กรอก future_followup | บล็อก; เปลี่ยนเป็นสถานะอื่นแล้วค่าที่ไม่ควรใช้ต้องไม่สร้างผลแจ้งเตือนผิด |
| A08 | เลือกวันที่พรุ่งนี้, วันนี้ และวันสิ้นปี พ.ศ. | อนาคตถูกบล็อก; วันนี้ผ่าน; ค่าเก็บ/แสดงไม่เลื่อนวันเพราะ timezone |
| A09 | บันทึกครั้งแรกและกดซ้ำ/ดับเบิลคลิก | ได้เอกสารเดียว เลข PCL เดียว ไม่ข้ามหรือซ้ำเพราะ request ซ้ำ |
| A10 | เปิดเอกสารร่างอีกครั้ง | ทุกค่าตรงหลัง refresh; selected_count เท่าจำนวนแถวใช่; reason_name เป็น snapshot |

### Phase B — วงจรอนุมัติครบเส้น (P0)

| ID | วิธีทดสอบ | Expected ที่ต้องเห็น |
|---|---|---|
| B01 | Maker A ส่ง D1 | ส่งได้เฉพาะ draft; chain มาจาก DOA จริง; ทุก slot มี assignee; ไม่มี Maker A ในผู้พิจารณา |
| B02 | Approver Step 2 พยายามตัดสินก่อน Step 1 ทั้งจาก UI และ direct API | ไม่มีปุ่มและ API ตอบ 403 `NOT_CURRENT_APPROVER`; state/audit ไม่เปลี่ยน |
| B03 | Step 1 approve แล้ว Step 2 approve | transition `draft → pending(1) → pending(2) → approved`; เวลา/คน/คำตัดสินทุกขั้นถูกต้อง |
| B04 | หลัง approved พยายามแก้, ส่งซ้ำ, cancel และ decide ซ้ำ | ถูกบล็อก; เอกสารและ audit ไม่เปลี่ยน |
| B05 | Step 1 reject โดยไม่ใส่เหตุผล แล้วใส่เหตุผล | ไม่มีเหตุผลต้องถูกบล็อก; เมื่อมีเหตุผลกลับ draft, เลขเดิม, returned fields และ audit ครบ |
| B06 | แก้ D3 แล้วส่งใหม่ | resolve DOA ใหม่; chain รอบเก่าอยู่ใน audit; chain ปัจจุบันไม่ปน; เลขเดิม |
| B07 | Step 1 approve แล้ว Step 2 reject | กลับ draftเหมือนกัน; บันทึกว่าใคร/ขั้นใด reject; ขั้นก่อนหน้าไม่หายจากประวัติ |
| B08 | เปลี่ยน DOA หลังส่งแต่ก่อน approve (เฉพาะ UAT) | ใบที่รอใช้ snapshot เดิม; ใบที่ส่งใหม่ใช้ DOA ใหม่ (EC-06) |
| B09 | DOA 1, 2 และ 6 ขั้น (เฉพาะ UAT) | จำนวนขั้นจริง dynamic; PDF มีแถวลงชื่อ 2, 3, 7 แถว; ไม่มีการ fix 2 ขั้น |

### Phase C — สิทธิ์และการป้องกันข้อมูล (P0)

ทดสอบทั้งปุ่มบน UI และ URL/API โดยตรง เพราะ “ไม่มีปุ่ม” ไม่ได้แปลว่า backend ปลอดภัย

| ID | วิธีทดสอบ | Expected ที่ต้องเห็น |
|---|---|---|
| C01 | Maker B เปิด id ของร่าง Maker A | 404 ไม่เปิดเผยว่ามีเอกสาร |
| C02 | Outsider เปิด pending/approved/cancelled, PDF และ attachment URL | 404/deny ทุกช่องทาง |
| C03 | Approver ที่อยู่ใน chain เปิด draft หลังถูก reject กลับร่าง | ต้องมองไม่เห็น draft ตาม LD-02/BR-13 |
| C04 | Admin เปิดทุกสถานะและพยายาม edit/approve | ดูและ cancel ได้ตามกฎ แต่ edit/approve แทนไม่ได้ |
| C05 | Maker A ปลอม assignee เป็นตนเองหรือส่ง user id นอกตัวเลือกทาง API | 422 `SELF_APPROVAL`/validation; chain ไม่ถูกสร้าง |
| C06 | ผู้ใช้ tenant อื่นเดา id/doc_no และค้นหา | ไม่เห็น list/detail/PDF/attachment; ห้ามข้อมูลข้าม tenant |
| C07 | ใส่ HTML/script และสูตร CSV เช่น `=1+1` ในข้อความ | หน้า/PDF ไม่ execute script; CSV ไม่เปิดช่อง formula injection |

### Phase D — Cancel, concurrency และ request ซ้ำ (P0/P1)

| ID | วิธีทดสอบ | Expected ที่ต้องเห็น |
|---|---|---|
| D01 | Owner cancel ตอน draft โดยไม่ใส่เหตุผล/แล้วใส่เหตุผล | ไม่ใส่ถูกบล็อก; ใส่แล้ว cancelled; แก้/ส่งต่อไม่ได้ |
| D02 | Owner cancel ตอน pending | cancelled; current pending step เป็น skipped; เหตุผลและ audit ครบ |
| D03 | Admin cancel ใบของคนอื่น; outsider cancel | Admin ผ่านตาม FRD; outsider 403 `NOT_OWNER` |
| D04 | cancel approved/cancelled ซ้ำ | 409 `NOT_CANCELLABLE`; state/audit ไม่เพิ่มผิด |
| D05 | เปิด draft สอง browser แก้คนละค่าแล้ว save ต่อกัน | request เก่าตอบ 409 `STALE`; ค่าของ request แรกไม่ถูกทับ |
| D06 | Step 1 กด approve พร้อมกันสอง session | มีเพียงครั้งเดียวที่สำเร็จ; อีกครั้ง 409; ไม่มี audit/event ซ้ำ |
| D07 | ส่ง POST เดิมด้วย Idempotency-Key เดิมและ key ใหม่ | key เดิมคืนผลเดิมโดยไม่ทำซ้ำ; key ใหม่ต้องยังติด state guard |

### Phase E — PDF, attachment, CSV และ integration (P0/P1)

| ID | วิธีทดสอบ | Expected ที่ต้องเห็น |
|---|---|---|
| E01 | เปิด PDF ของ draft, pending, approved, cancelled | ทุกสถานะ 2 หน้า; หน้า 1 เหตุผลครบ; หน้า 2 สรุป/ลงชื่อ/ประวัติ;เลข/สถานะ/ข้อมูลตรงฐานข้อมูล |
| E02 | ใช้ข้อความยาวครบ 8 เหตุผลและ DOA 6 ขั้น | ยัง 2 หน้า; ข้อความไม่หาย; block ลงชื่อไม่ถูกตัดกลาง; อ่านได้จริง |
| E03 | approve ขั้นสุดท้าย | PDF approved_final ถูกเก็บครั้งเดียวใน Document Store และเปิดย้อนหลังได้ |
| E04 | แก้ข้อมูล master เช่นชื่อพนักงาน/บริษัท/config หลังออกเลข (UAT) | เอกสารเก่ายังใช้ snapshot ที่กำหนด; เอกสารใหม่ใช้ค่าใหม่ |
| E05 | แนบไฟล์ชนิดถูก/ผิด, ชื่อไทย/ยาว, ไฟล์ว่าง/เกินขนาด | รับเฉพาะที่ policy อนุญาต; error ชัด; ไม่มีไฟล์ orphan; คนไม่มีสิทธิ์โหลดไม่ได้ |
| E06 | ลบ attachment ตอน draft และลองหลัง pending/approved | ทำได้เฉพาะสถานะ/สิทธิ์ที่ระบบกำหนด; audit/Document Center สอดคล้อง (หาก FRD ไม่กำหนด ให้เปิด OQ) |
| E07 | กรองหลายเงื่อนไขแล้ว export CSV | จำนวน/แถวตรงกับ list ที่กรอง; ภาษาไทย/วันที่/เลขเอกสารถูก; ไม่มีข้อมูลที่ผู้ใช้ไม่มีสิทธิ์ |
| E08 | ค้นหาด้วย doc_no, project name, ผู้จัดทำ และชื่อเหตุผล | ตรง FN-10 ทุก field; pagination/sort ไม่ทำแถวหายหรือซ้ำ |
| E09 | approve D2 ที่ closure_status=follow | ถ้าตกลงให้ยิง event: ผู้จัดทำได้รับ `pcl_followup_approved` ครั้งเดียวและ link ถูกใบ |
| E10 | cancel D5 ระหว่าง pending | ถ้าตกลงให้ยิง event: current approver ได้ `pcl_cancelled` ครั้งเดียว; draft→cancelled ไม่ส่งผิดคน |
| E11 | ตรวจ DOA notification | ระบบ feature ต้องไม่ยิง `doa_pending/doa_result` ซ้ำกับ DOA engine |
| E12 | ตรวจโครงการต้นทาง FM-BDM-01/03 ก่อนและหลัง approve | ต้องไม่ถูกปิด/แก้/ส่งต่อ ตาม scope ปัจจุบัน |

### Phase F — Config และความคงทนของข้อมูล (UAT/ร่วมกับ Dev/DBA)

| ID | วิธีทดสอบ | Expected ที่ต้องเห็น |
|---|---|---|
| F01 | ปิด doc type PCL แล้วสร้าง | 409 `DOC_TYPE_INACTIVE`; ไม่เกิดเลขหรือ partial record |
| F02 | เปลี่ยนชื่อ/ลำดับ reason config หลังสร้างเอกสาร | ใบเก่ารักษา reason_name snapshot; ใบใหม่อ่าน config ใหม่ตามกติกาที่ BA ยืนยัน |
| F03 | ส่ง reason_code/closure_status ที่ไม่มีใน config ทาง API | 422; ห้ามเก็บค่าปลอม |
| F04 | สร้างเลขพร้อมกันหลาย request | doc_no unique ต่อ tenant/company; ไม่มี duplicate หรือเลขถูก reuse |
| F05 | ตรวจ audit จาก DB/log | ทุก write มี actor/time/action/note; append-only;ไม่มี update/delete history |
| F06 | ลองแก้ payload ฝั่ง clientให้ selected=ไม่ใช่แต่มีข้อความ | server ล้าง detail/evidence/impact/revisit เสมอ |
| F07 | ตรวจ retention/backup ของ approved PDF และ attachment | สอดคล้อง policy เอกสาร; ไม่มี hard delete โดยไม่ตั้งใจ |

## 6. Business-sense review ที่ไม่ควรพลาด

นอกจากความตรง FRD ให้ถามว่าระบบช่วยธุรกิจปิดวงจรได้จริงหรือไม่:

- เอกสารนี้ระบุเพียงชื่อโครงการ แต่ไม่ผูกเลขโครงการต้นทาง จึงมีความเสี่ยงเลือก/พิมพ์ชื่อผิด, ชื่อซ้ำ และรายงานย้อนกลับไม่ได้ นี่เป็น gap ทางธุรกิจที่ FRD ตั้งใจ defer ไม่ใช่ bug แต่ควรให้ PM/BA รับทราบเป็นลายลักษณ์อักษร
- สถานะ “ติดตามเงื่อนไขในอนาคต” มีข้อความ future follow-up แต่ไม่มี due date, owner ของ follow-up หรือระบบเตือนเมื่อถึงเงื่อนไข จึงเป็นเพียงบันทึก ไม่ใช่กระบวนการติดตามจริง
- “รอจัดเก็บเอกสาร” ไม่มี workflow ว่าใครต้องจัดเก็บ, เมื่อไร และเปลี่ยนเป็น “ปิดโครงการแล้ว” อย่างไร อาจค้างถาวรได้
- ระบบอนุญาตให้ owner/admin ยกเลิกตอน pending แต่ต้องชัดว่าผู้อนุมัติทุกคนที่เกี่ยวข้องรับรู้การยกเลิกหรือเฉพาะ current approver
- CSV และการเห็นข้อมูลโดย admin เป็นจุดเสี่ยง PII/ข้อมูลเชิงกลยุทธ์ ควรตรวจ role scope, audit การ export และ policy การส่งต่อไฟล์
- การกลับ draft หลัง reject แล้ว resolve DOA ใหม่อาจทำให้ผู้อนุมัติเปลี่ยนคนระหว่างรอบ ต้องยืนยันว่าธุรกิจยอมรับและ audit เปรียบเทียบรอบได้
- PDF ที่เก็บเป็น approved_final ต้องพิสูจน์ว่า immutable และอ้าง revision/config ณ เวลานั้น ไม่ใช่ render ใหม่แล้วหน้าตา/ข้อความเปลี่ยนตาม master ปัจจุบัน

## 7. วิธีจดผลเพื่อออก Feature Check Report

อย่าติ๊กผ่านแบบรวมว่า “flow ผ่าน” ให้บันทึกหนึ่งแถวต่อกฎ/สถานการณ์:

| Case | Result | หลักฐานขั้นต่ำ |
|---|---|---|
| B03 | Pass/Fail/Blocked | doc_no, ผู้ใช้แต่ละขั้น, เวลา, screenshot status/audit, response ที่เกี่ยวข้อง |
| C02 | Pass/Fail/Blocked | actor, URL/API, HTTP status, หน้าจอที่เห็น |
| D06 | Pass/Fail/Blocked | 2 request timestamps, response ทั้งคู่, audit/event count |
| E03 | Pass/Fail/Blocked | doc_no, approved timestamp, Document Store reference/hash |

เมื่อพบปัญหา ให้เก็บ:

1. build/environment และเวลาเกิดเหตุ
2. persona/role/tenant
3. doc_no หรือ test record id
4. ขั้นตอนทำซ้ำแบบสั้น
5. Expected โดยอ้าง FRD ID
6. Actual ที่เห็นจริง
7. screenshot/clip และ response/log ถ้ามี
8. ตรวจซ้ำได้หรือไม่ และกระทบข้อมูลจริงหรือไม่

ห้ามสรุป Pass ให้สิ่งที่ไม่ได้ตรวจ ให้ใช้ `Not tested` หรือ `Blocked` โดยเฉพาะ backend/integration cases

## 8. เกณฑ์หยุดและแจ้งทันที

หยุดการทดสอบ mutation บน Production และแจ้ง PM/BA/Dev ทันทีถ้าพบข้อใดข้อหนึ่ง:

- ข้ามสิทธิ์, ข้ามลำดับอนุมัติ, self-approve หรือข้อมูลข้าม tenant
- เลขเอกสารซ้ำ, เอกสารซ้ำจากการกดซ้ำ, ข้อมูลหาย/ถูกทับ
- approved แล้วแก้หรือยกเลิกได้
- reject/cancel แล้ว state หรือ audit ไม่ตรง
- PDF approved_final ไม่ตรงข้อมูลที่อนุมัติหรือถูกเปลี่ยนย้อนหลัง
- event/notification ยิงซ้ำหรือผิดผู้รับจนเกิดการตัดสินใจผิด
- ระบบปิด/แก้โครงการต้นทางทั้งที่ FRD ระบุว่าไม่ทำ

## 9. Definition of Done สำหรับ review รอบนี้

ถือว่าการ review ครบเมื่อ:

- Phase A–E ทุกเคสมี Pass/Fail/Blocked พร้อมหลักฐาน
- Phase F มีผลจาก UAT/Dev/DBA หรือระบุชัดว่าไม่ได้ตรวจ
- Open Questions และ source conflict เรื่อง notification มีคำตอบจากผู้มีอำนาจ
- ทุก Fail ผูก bug ที่ทำซ้ำได้และมี severity ตามผลกระทบ
- ออกรายงาน Feature Check Report โดยไม่รับรอง UI/UX หรือ backend ส่วนที่ไม่ได้ตรวจ

