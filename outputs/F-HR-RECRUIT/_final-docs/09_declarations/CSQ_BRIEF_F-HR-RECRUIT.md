# CSQ_BRIEF — F-HR-RECRUIT · สรรหา  *(carried)*

> ⚠️ **หมายเหตุการ carry:** WF-01 **ไม่มี skill `csq-declaration`** (มีแค่ `doa` · `doccfg` · `ntf`)
> ใบนี้จึง **ยกมาจากแพ็กบรีฟ Phase A** (`Pack Brief Feature/F-HR-RECRUIT/5_DECLARATIONS/CSQ_BRIEF.md`) **verbatim**
> เพื่อให้ dev/BA เห็น event ที่ต้องประกาศเข้า ENG-CSQ ต่อไป — **ไม่ได้ผ่าน generator/quality-gate ของ skill**
> ต้องให้ BA ทวนก่อนใช้จริง (ต่างจาก DOA/NTF ที่ผ่าน companion skill แล้ว)

---

## 1. Identity: F-HR-RECRUIT · ENG-CSQ
## 2. Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| recruit.candidate_stored | เพิ่ม/แก้ผู้สมัคร (S-03·BR-02·BR-06) | **SecC** | เก็บ/เข้าถึงข้อมูลผู้สมัคร (PDPA) | ref:candidate_id · consent_pdpa · retention_until · action(view/store) |
| recruit.hired | offer accepted→hired (S-10) | **EC** | ต้นทุนสรรหา (ถ้าตีมูลค่า · [AI-DRAFT] basis: declared) | ref:req_id · cost_declared · currency=THB |
## 3. ไม่ประกาศ: OC(OP) · DC-เอกสาร+doa_*(DOA) · AC/FC(ไม่ลงบัญชี/ไม่กระทบเงินสด) · SC(สงวน)
## 5. Register: [ ] SecC PDPA event · [ ] ไม่ซ้ำ OC/DC/SC → กัน 422

---

**OQ ที่พัวพัน:** `recruit.candidate_stored.retention_until` ผูกกับ **OQ-16** (PDPA retention — ระยะเก็บ/ลบ/anonymize อ่านจาก Policy Center · FIX-03 กลับมติ "ไม่มี expire") — ยังรอเคาะ
