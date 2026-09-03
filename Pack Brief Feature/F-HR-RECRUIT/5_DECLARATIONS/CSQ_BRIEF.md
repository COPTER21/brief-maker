# CSQ_BRIEF — F-HR-RECRUIT · สรรหา
## 1. Identity: F-HR-RECRUIT · ENG-CSQ
## 2. Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| recruit.candidate_stored | เพิ่ม/แก้ผู้สมัคร (S-03·BR-02·BR-06) | **SecC** | เก็บ/เข้าถึงข้อมูลผู้สมัคร (PDPA) | ref:candidate_id · consent_pdpa · retention_until · action(view/store) |
| recruit.hired | offer accepted→hired (S-10) | **EC** | ต้นทุนสรรหา (ถ้าตี่มูลค่า · [AI-DRAFT] basis: declared) | ref:req_id · cost_declared · currency=THB |
## 3. ไม่ประกาศ: OC(OP) · DC-เอกสาร+doa_*(DOA) · AC/FC(ไม่ลงบัญชี/ไม่กระทบเงินสด) · SC(สงวน)
## 5. Register: [ ] SecC PDPA event · [ ] ไม่ซ้ำ OC/DC/SC → กัน 422
