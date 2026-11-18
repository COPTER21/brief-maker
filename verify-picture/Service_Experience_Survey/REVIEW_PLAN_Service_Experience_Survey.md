# Full Logic Review Plan — Service Experience Survey (F-TMP-006 / FM-SAL-22)

> เป้าหมาย: ตรวจระบบ Production ที่ผ่าน UAT และปรับ layout แล้ว โดยเน้น business logic, state, permission, data integrity, integration และ output ไม่ใช่การ review ความสวยงามซ้ำ

## 1. ข้อสรุปก่อนเริ่ม

- ใช้ FRD เป็น acceptance baseline หลัก ตามคำสั่ง PM/BA
- ถ้าระบบไม่ตรงกฎที่ FRD ระบุชัดและไม่มีมติใหม่ ให้จัดเป็น `Spec defect`
- ถ้า FRD ขัดกันเอง เป็น AI-DEFAULT หรือยังมี OQ ให้จัดเป็น `Business gap / ต้องยืนยัน` ห้ามสรุปเป็น bug โดยไม่มีคำตอบจาก PM/BA
- ถ้าระบบตรง FRD แต่เสี่ยงต่อข้อมูล สิทธิ์ หรือการปฏิบัติงาน ให้จัดเป็น `Operational risk / ข้อเสนอแนะ`
- UI layout ถือว่าผ่านแล้ว ตรวจ UI เฉพาะสิ่งที่บอกผลของ logic เช่น ปุ่มตามสิทธิ์ สถานะ validation ข้อมูลที่แสดง และข้อความ error

## 2. จุดเสี่ยงใน FRD ที่ต้องเคลียร์กับ PM/BA

| ID | ประเด็น | สิ่งที่เอกสารเขียน | ความเสี่ยง / คำถามที่ต้องยืนยัน |
|---|---|---|---|
| GAP-01 | มติธุรกิจยังเป็น AI-DEFAULT | `07_LOCKED_DECISIONS` ระบุ DEC-01..10 เป็น AI-DEFAULT และต้องยืนยันก่อน UAT | มีใบยืนยันจริงหรือไม่ และมติ Production ตรงกับรายการนี้หรือไม่ |
| GAP-02 | สถานะ OQ ขัดกัน | Overview บอก Ready หลัง OQ-02/04/07 ปิด แต่ §0.6 ยังเรียก OQ-01..08 ว่า Open Questions | ขอ final decision/version ที่ Production ใช้จริง |
| GAP-03 | รหัสยังเป็นรหัสชั่วคราว | Feature ID = `F-TMP-006`; OQ-07 ถามรหัสจริง/function code | Production ใช้รหัสใดใน config, audit, monitoring และ support |
| GAP-04 | ปีในเลขเอกสาร | API/AC ใช้ `SEA-YYYY-NNNN`; test data ใช้ `SEA-2569-xxxx`; OQ-08 ยังถาม ค.ศ./พ.ศ. | เลขจริงต้องใช้ปีแบบใด และ reset เมื่อใด |
| GAP-05 | ความหมาย “วันที่บันทึก” | BR-03/DEC-12 ให้ใช้ `created_at`; DB มี `recorded_at` แยก | ร่างสร้างวันที่ 1 แต่บันทึกผลวันที่ 5 ในรายการควรแสดงวันที่ใด |
| GAP-06 | แบบประเมินซ้ำ | EC-03 บอกไม่บล็อก แต่ OQ-06 ยังไม่ตัดสิน | ลูกค้าคนเดิม เดือนเดียวกันสร้างหลายใบได้จริงหรือไม่; รายงานสรุปจะนับอย่างไร |
| GAP-07 | สิทธิ์การเห็นใบ | DEC-08 เป็น AI-DEFAULT: เจ้าของเห็นของตน; manager เห็นทั้งหมด; Sales Admin คนอื่นเห็นไม่ได้ทุกสถานะ | หลัง recorded แล้วควรแชร์ในทีมได้หรือยังคงปิดตลอด |
| GAP-08 | Contact Person | OQ-05 ยังถามว่าจะเลือกจาก master หรือพิมพ์เอง | Production ใช้แบบใด และต้องเก็บ snapshot/รหัส contact หรือไม่ |
| GAP-09 | เกณฑ์คะแนนต่ำ | เอกสารระบุอ่าน config ค่าเริ่ม 2; OQ-03 ยังถามเกณฑ์ | ค่า Production ปัจจุบันเท่าใด ใครเปลี่ยนได้ และมี effective date หรือไม่ |
| GAP-10 | Customer snapshot ตอนแก้ร่าง | snapshot ถูกสร้างตอนออกเลขครั้งแรก แต่ PUT อนุญาตเปลี่ยน `customer_id` | ถ้าเปลี่ยนลูกค้าหลังสร้างร่าง ชื่อ snapshot ต้องเปลี่ยนตามหรือห้ามเปลี่ยนลูกค้า |
| GAP-11 | คะแนนบางส่วนในร่าง | API อนุญาต scores บางส่วน แต่ DB อธิบาย score “10 แถวต่อใบเมื่อครบ” | คะแนนบางส่วนเก็บเป็นแถวจริงหรือเก็บที่อื่น และเปิดร่างกลับมาต้องไม่หาย |
| GAP-12 | ไฟล์แนบ | อยู่ใน scope แต่ไม่มี rule เรื่องชนิดไฟล์ ขนาด ลบหลัง recorded/cancelled และสิทธิ์ดาวน์โหลด | ขอ policy ที่ใช้จริงก่อนตัดสินผล |

## 3. เงื่อนไขก่อนเทส Production

- ใช้บัญชีทดสอบอย่างน้อย 3 บัญชี: Owner A, Sales Admin B, Manager (`role-mgr-sales`)
- ถ้าทำได้ ใช้คนละ tenant อีก 1 บัญชีเพื่อทดสอบ tenant isolation
- ใช้ลูกค้าทดสอบ ไม่ใช้ชื่อบุคคลจริงใน Contact Person หรือไฟล์แนบ
- ขอค่าปัจจุบันของ doc type `SEA`, รูปแบบเลข, low-score threshold และ notification recipient
- เตรียมสิทธิ์ดู Notification Center, audit/history, CSV และ PDF
- ตกลง prefix ของข้อมูลทดสอบ เช่น `[REVIEW-20261118]` และยกเลิกข้อมูลทดสอบหลังจบ ห้ามลบ audit
- เก็บ evidence ทุกเคส: เวลา, account/role, doc no, input, expected, actual, screenshot หรือ response/correlation ID
- ก่อนทดสอบ negative ที่อาจส่ง notification ให้แจ้งผู้รับ และใช้ข้อมูลที่ระบุชัดว่าเป็น test

## 4. ชุดข้อมูลทดสอบขั้นต่ำ

| Data | ค่า |
|---|---|
| D1 Happy | เดือนปัจจุบัน, ลูกค้าทดสอบ A, Contact `TEST OWNER A`, คะแนน 3–5 ครบ 10 ข้อ |
| D2 Partial | ตอบเฉพาะ q1=4, q2=5 แล้วเก็บร่าง |
| D3 Low boundary | ชุดหนึ่งมีคะแนนเท่ากับ threshold และอีกชุด threshold+1 |
| D4 Invalid text | Contact ว่าง, space ล้วน, 120 ตัว, 121 ตัว, Unicode ไทย/จีน/ญี่ปุ่น |
| D5 Long feedback | feedback หลายบรรทัดและยาวเกิน 5 บรรทัด PDF |
| D6 Duplicate | ลูกค้าและเดือนเดียวกับ D1 |
| D7 Snapshot | ลูกค้าทดสอบที่สามารถเปลี่ยนชื่อใน Customer master ได้ |
| D8 Formula-like CSV | ข้อความขึ้นต้น `=`, `+`, `-`, `@` โดยใช้ข้อมูลทดสอบที่ปลอดภัย |

## 5. ลำดับการทดสอบที่แนะนำ

### Phase A — P0: Flow หลักและข้อมูลไม่เสีย

| ID | วิธีทดสอบ | Expected ตาม FRD | Result / Evidence |
|---|---|---|---|
| A01 | Owner A สร้าง D1 และบันทึกเป็นร่าง | ได้สถานะ draft; ได้เลข SEA ตอน save ครั้งแรก; ข้อมูลครบตามที่กรอก | ☐ |
| A02 | ปิดแล้วเปิดร่าง A01 ใหม่ | เดือน ลูกค้า Contact คะแนน feedback และไฟล์แนบคงเดิม | ☐ |
| A03 | แก้ร่าง A01 แล้ว save ซ้ำหลายครั้ง | doc no เดิม; version เพิ่ม; ไม่เกิดเอกสารซ้ำ | ☐ |
| A04 | เติมคะแนนครบ 10 แล้ว record | draft → recorded; recorded_at ถูกตั้ง; audit มี action; ไม่มี approval step | ☐ |
| A05 | เปิด recorded แล้วลองแก้ผ่าน UI และ direct route/API ถ้าทำได้ | ไม่มีปุ่มแก้; server ปฏิเสธ `NOT_DRAFT`; ข้อมูลเดิมไม่เปลี่ยน | ☐ |
| A06 | Owner สร้าง D2 ตอบไม่ครบแล้วพยายาม record | ปฏิเสธ; แจ้งจำนวน/ข้อที่ขาด; ยังเป็น draft; คะแนนเดิมไม่หาย | ☐ |
| A07 | Owner ยกเลิก draft พร้อมเหตุผล | draft → cancelled; เก็บ reason/actor/time; แก้และ record ต่อไม่ได้ | ☐ |
| A08 | Owner ยกเลิก recorded พร้อมเหตุผล | recorded → cancelled; คะแนนและประวัติเดิมยังอยู่; แก้ไม่ได้ | ☐ |

### Phase B — Validation และ boundary

| ID | วิธีทดสอบ | Expected ตาม FRD | Result / Evidence |
|---|---|---|---|
| B01 | เปิดสร้างใหม่ | Month default = เดือนปัจจุบัน และไม่มีช่องวันที่กรอกเอง | ☐ |
| B02 | ไม่เลือก Month / Customer / Contact ทีละช่องและหลายช่องพร้อมกัน | บล็อกตาม VR-01..03; ไม่สร้างข้อมูลครึ่งใบโดยไม่ตั้งใจ | ☐ |
| B03 | Contact เป็น space ล้วน | trim แล้วถือว่าว่าง; แสดง “กรุณากรอกชื่อผู้ติดต่อ” | ☐ |
| B04 | Contact 120 และ 121 ตัวอักษร | 120 ผ่าน; 121 ต้องถูกปฏิเสธอย่างชัดเจน ไม่ truncate เงียบ | ☐ |
| B05 | ส่ง score 0, 6, ทศนิยม, string และ q_key นอก q1..q10 ผ่าน API ถ้ามีสิทธิ์ | ปฏิเสธ 422; DB ไม่เปลี่ยน | ☐ |
| B06 | คลิกคะแนนข้อเดิมจาก 1 เป็น 5 | มีเพียงค่าเดียวต่อข้อ; summary เปลี่ยนทันที; ไม่มีค่าซ้ำ | ☐ |
| B07 | record เมื่อขาด 1 ข้อ และเมื่อครบพอดี 10 ข้อ | ขาด 1 บล็อก; ครบ 10 ผ่าน | ☐ |
| B08 | Feedback ว่าง, หลายบรรทัด, Unicode และยาวมาก | เก็บ/อ่านคืนครบตามข้อจำกัดจริง; ไม่ทำให้ record/PDF พัง | ☐ |
| B09 | กดยกเลิกโดยไม่ใส่เหตุผลและใส่ space ล้วน | ปฏิเสธ `REASON_REQUIRED`; สถานะไม่เปลี่ยน | ☐ |
| B10 | สร้าง D6 ซ้ำลูกค้า+เดือน | ตาม FRD ปัจจุบัน “ไม่บล็อก”; บันทึกเป็น business gap หาก PM/BA ต้องการกันซ้ำ | ☐ |

### Phase C — คะแนนต่ำ การคำนวณ และ notification

| ID | วิธีทดสอบ | Expected ตาม FRD | Result / Evidence |
|---|---|---|---|
| C01 | ยืนยันค่า low threshold ของ Production จาก config | ค่าเดียวกับที่ใช้คำนวณและอธิบายได้; ไม่สมมติว่าเป็น 2 | ☐ |
| C02 | Record ชุดที่คะแนนต่ำสุด = threshold+1 | low_count=0; ไม่ยิง `sea_low_score_recorded` | ☐ |
| C03 | Record ชุดที่มี 1 ข้อ = threshold | low_count=1; แสดง low-score state/banner; manager ได้แจ้ง 1 ครั้ง | ☐ |
| C04 | Record หลายข้อที่ ≤ threshold | low_count ตรงจำนวนจริง; notification variables doc/customer/count/month ถูกต้อง | ☐ |
| C05 | คำนวณ average รวมและรายกลุ่มด้วยชุดคะแนนที่หารไม่ลงตัว | ค่าเฉลี่ยและ rounding ตรงกันในหน้ารายการ/รายละเอียด/CSV | ☐ |
| C06 | ตรวจ PDF ของใบ C03/C04 | PDF ไม่มี average และ low_count เพราะ BR-10 ระบุเป็นค่าแสดงผลเท่านั้น | ☐ |
| C07 | refresh/retry request record เดิมด้วย Idempotency-Key เดิม | ไม่ record ซ้ำ ไม่ยิง notification ซ้ำ ไม่สร้าง audit ซ้ำ | ☐ |
| C08 | Owner ยกเลิกใบเอง เทียบกับ Manager ยกเลิก | Owner ยกเลิก: ไม่ส่ง sea_cancelled ให้ตนเอง; Manager ยกเลิก: Owner ได้แจ้งพร้อม actor/reason | ☐ |

### Phase D — Permission, privacy และ tenant isolation

| ID | วิธีทดสอบ | Expected ตาม FRD | Result / Evidence |
|---|---|---|---|
| D01 | Owner A ดู list/search/count/export | เห็นเฉพาะใบของตนทุกสถานะ; count และ CSV นับเฉพาะชุดที่เห็น | ☐ |
| D02 | Sales Admin B ใช้ URL/ID ของ draft, recorded, cancelled ของ A | ทุก GET ตอบเสมือนหาไม่พบ (`404 NOT_FOUND`); Contact/ไฟล์/PDF ไม่รั่ว | ☐ |
| D03 | Sales Admin B พยายาม edit/record/cancel ใบ A ผ่าน API | ปฏิเสธ; สถานะ version audit notification ไม่เปลี่ยน | ☐ |
| D04 | Manager เปิดใบของ A | เห็นได้ทุกสถานะตาม DEC-08 รวม PDF/ไฟล์/ประวัติ | ☐ |
| D05 | Manager พยายาม edit หรือ record แทน A | ทำไม่ได้; record ตอบ `403 NOT_OWNER`; UI ไม่มี action ที่ชวนให้เข้าใจผิด | ☐ |
| D06 | Manager ยกเลิก draft และ recorded ของ A | ทำได้เมื่อมีเหตุผล; Owner ได้ notification | ☐ |
| D07 | ทดสอบ account ไม่มี role ที่เกี่ยวข้อง | เข้า feature/action ไม่ได้ และไม่เห็นข้อมูลผ่าน API/export/PDF | ☐ |
| D08 | ถ้ามี test tenant B ให้ลองเดา ID/doc no จาก tenant A | ต้องไม่พบทุก endpoint รวม attachment/PDF/export; ไม่มี count leakage | ☐ |
| D09 | ตรวจ access/application log สำหรับการเปิดใบ | ต้องไม่มีค่า Contact Person หรือข้อมูลส่วนบุคคลถูก log ตาม FRD | ☐ |
| D10 | ตรวจ session หมดอายุระหว่าง save/record | ไม่บันทึกแบบไม่รู้ตัว; กลับเข้าแล้วเห็นสถานะจริง; ไม่ duplicate | ☐ |

### Phase E — Customer snapshot, master และ document number

| ID | วิธีทดสอบ | Expected / จุดตัดสิน | Result / Evidence |
|---|---|---|---|
| E01 | สร้างใบแล้วเปลี่ยนชื่อลูกค้าใน master | ใบเดิม/PDF/CSV คง `customer_name_snapshot` ตาม BR-09 | ☐ |
| E02 | ใน draft เปลี่ยน customer_id หลังเคย save แล้ว | ต้องขอคำตอบ GAP-10; ตรวจว่า customer_id กับ snapshot ไม่ขัดกัน | ☐ |
| E03 | เปิด Customer ที่ไม่ใช่ต่างประเทศผ่าน UI/API | ต้องสอดคล้อง OQ-04 และ policy Production; บันทึกผลเป็น gap ถ้า FRD ยังไม่ตัดสิน | ☐ |
| E04 | Save พร้อมกันหลายใบ | doc no ไม่ซ้ำภายใน tenant; format/reset ตรง config; no-gap ไม่ได้บังคับ | ☐ |
| E05 | retry create ด้วย Idempotency-Key เดิม | ได้เอกสารเดิม ไม่ออกเลข/สร้างใบใหม่ | ☐ |
| E06 | ปิด doc type SEA แล้วลองสร้าง จากนั้นเปิดกลับ | ปุ่ม disabled/ข้อความตรง; API 409 `DOC_TYPE_INACTIVE`; ใบเดิมยังอ่านได้ | ☐ |
| E07 | เทียบ header/company/logo/form code/revision ก่อนและหลังแก้ config | ใบเดิมคง snapshot; ใบใหม่ใช้ config ใหม่ตามเวลาที่ออกเลข | ☐ |

### Phase F — List, filter, CSV, attachment และ PDF

| ID | วิธีทดสอบ | Expected ตาม FRD | Result / Evidence |
|---|---|---|---|
| F01 | เทียบ tab count กับแถวจริงในแต่ละสถานะและแต่ละ role | count เป็นของ visible set และเปลี่ยนทันทีหลัง transition | ☐ |
| F02 | ค้นด้วย doc no/customer/contact/recorder และกรอง month/recorder/status ร่วมกัน | ผลเป็น intersection ที่ถูกต้อง; reset คืนครบ; pagination ไม่ทำข้อมูลหาย/ซ้ำ | ☐ |
| F03 | Export CSV หลังใส่ filter | มีเฉพาะผลตาม filter+permission และคอลัมน์ตาม AC-10 | ☐ |
| F04 | เปิด CSV ด้วย Excel/UTF-8 โดยมีไทย/จีน/ญี่ปุ่น/ขึ้นบรรทัดใหม่/จุลภาค | ตัวอักษรและคอลัมน์ไม่แตก; ไม่มี mojibake | ☐ |
| F05 | ใช้ D8 ใน field ที่ export | ค่าไม่ถูก Excel ประมวลเป็นสูตรที่เป็นอันตราย; ถ้ายังไม่กำหนดให้รายงาน security risk | ☐ |
| F06 | แนบไฟล์ปกติ แล้วเปิดใหม่/ดาวน์โหลดด้วย Owner/Manager/คนไม่มีสิทธิ์ | Owner/Manager ตาม policy ดาวน์โหลดได้; ผู้ไม่มีสิทธิ์ไม่ได้; ชื่อ/ชนิด/ขนาดถูกต้อง | ☐ |
| F07 | ลองชนิด/ขนาดไฟล์ผิด ลบไฟล์ใน draft/recorded/cancelled | เทียบกับ policy จริง; ถ้าไม่มี policy ให้รายงาน GAP-12 ไม่เดา expected | ☐ |
| F08 | PDF draft/recorded/cancelled | 1 หน้า ภาษาอังกฤษ คะแนน ✓ ตรงข้อ; DRAFT/CANCELLED ถูกสถานะ | ☐ |
| F09 | PDF D5 และ Unicode Contact/Company | ยัง 1 หน้า; ไม่ตัดข้อความสำคัญ; glyph ไม่เป็นสี่เหลี่ยม | ☐ |
| F10 | เทียบ PDF preview กับไฟล์ download/server render | เนื้อหา เลข สถานะ คะแนน feedback header/footer ตรงกัน | ☐ |

### Phase G — Concurrency, audit และความทนทาน

| ID | วิธีทดสอบ | Expected ตาม FRD | Result / Evidence |
|---|---|---|---|
| G01 | เปิด draft เดียวกัน 2 tab; save tab แรก แล้ว save tab เก่า | tab เก่าได้ 409 `STALE_VERSION`; ไม่ overwrite; UI ชวน refresh | ☐ |
| G02 | กด save/record/cancel รัวหรือ network retry | action เกิดครั้งเดียว; doc no/status/audit/notification ไม่ซ้ำ | ☐ |
| G03 | ตรวจ audit ตั้งแต่ create→edit→record→cancel | ลำดับ actor/time/action/note ครบ; append-only; ไม่มีแก้/ลบย้อนหลัง | ☐ |
| G04 | จำลอง error ของ notification หลัง record สำเร็จ | ต้องรู้ transaction/outbox policy: สถานะกับ event ไม่หลุดกันและ retry ไม่ซ้ำ | ☐ |
| G05 | จำลอง PDF/attachment service ล่ม | core record ไม่เสีย; error ชัด; retry ได้; ไม่มีเอกสาร/ไฟล์ครึ่งชุด | ☐ |
| G06 | ตรวจว่า feature ไม่แก้ master และไม่ส่ง event downstream อื่น | ตรง BR-13/DEC-01/02; notification ที่ประกาศไว้เป็นข้อยกเว้นตาม FRD | ☐ |

## 6. เกณฑ์จัดระดับสิ่งที่พบ

| ระดับ | ตัวอย่าง |
|---|---|
| Critical | ข้าม tenant/role, เห็น Contact Person ของคนอื่น, ข้อมูลหาย, audit ถูกแก้ได้ |
| High | คะแนน/สถานะ/doc no ผิด, record ไม่ครบได้, duplicate action, notification สำคัญผิดผู้รับ, PDF/CSV ผิดข้อมูลธุรกิจ |
| Medium | filter/count/audit บางส่วนผิด, validation มีทางเลี่ยง, snapshot/config ไม่ตรงแต่มีทางแก้ชั่วคราว |
| Low | ข้อความหรือ functional feedback เล็กน้อยที่ไม่ทำให้ผลธุรกิจผิด |
| Business gap | FRD/OQ/AI-DEFAULT ไม่ชัดหรือขัดกัน ต้องให้ PM/BA ตัดสิน ไม่ใช่ bug โดยอัตโนมัติ |

## 7. รูปแบบบันทึก defect ที่ควรใช้

```text
ID / Severity / Classification:
FRD reference:
Environment + build + time:
Actor / role / tenant:
Precondition + test data:
Steps:
Expected:
Actual:
Business impact:
Evidence (screenshot/video/request ID/doc no):
Reproducibility:
```

## 8. Exit criteria สำหรับสรุปว่า review ครบ

- P0 ทั้งหมดผ่าน หรือมี defect พร้อม owner/กำหนดแก้
- ทดสอบครบ 3 role และ direct URL/API deny cases ไม่ใช่ดูแค่ปุ่มซ่อน
- ทดสอบครบทุก transition: create→draft→edit→record→cancel และ invalid transition
- ทดสอบ boundary low-score, notification, idempotency และ concurrency
- CSV/PDF/attachment ถูกทั้งข้อมูล สิทธิ์ และ Unicode
- GAP-01..12 ได้คำตอบหรือบันทึกเป็น accepted risk โดย PM/BA
- ทุกข้อที่สรุปว่า Pass มี evidence; ข้อที่ไม่ได้ทดสอบระบุ `Not tested` ห้ามตีความเป็น Pass

## 9. แหล่งอ้างอิงที่ใช้

- `_frd/FRD_Service_Experience_Survey/00_OVERVIEW_Service_Experience_Survey.md`
- `_frd/FRD_Service_Experience_Survey/02_API_Service_Experience_Survey.md`
- `_frd/FRD_Service_Experience_Survey/03_LOGIC_Service_Experience_Survey.md`
- `_frd/FRD_Service_Experience_Survey/04_DB_Service_Experience_Survey.md`
- `_frd/FRD_Service_Experience_Survey/05_RULES_Service_Experience_Survey.md`
- `_frd/FRD_Service_Experience_Survey/06_TESTS_Service_Experience_Survey.md`
- `_frd/FRD_Service_Experience_Survey/07_LOCKED_DECISIONS_Service_Experience_Survey.md`
- `_tc/TC_Service_Experience_Survey.md`
- `_tc/QA_AUDIT_Service_Experience_Survey.md`
- `_reference/RUN_LOG_Service_Experience_Survey.md`

