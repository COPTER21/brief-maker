# Security Policy — 75 Controls Reference

Source: 14 international standards mapped to 75 specific controls.
ใช้เป็น **preset checklist** ให้ user เลือกใน Pillar 3 (Guardrails) ของ BRD

---

## 1. COSO — Internal Control & SoD

_การควบคุมภายในและแยกหน้าที่_

**Control ID Range:** S01-01 ถึง S01-07

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S01-01 | **DoA Limit** | กำหนดเพดานงบประมาณตามลำดับขั้น |
| S01-02 | **Maker-Checker Workflow** | บังคับผู้สร้างและผู้อนุมัติต้องไม่ใช่คนเดียวกัน |
| S01-03 | **Temporary Delegation** | มอบหมายสิทธิ์ชั่วคราวพร้อมวันหมดอายุ |
| S01-04 | **SoD Conflict Matrix** | ตารางบล็อกสิทธิ์ทับซ้อน (เช่น ห้ามจัดซื้อ+จ่ายเงิน) |
| S01-05 | **3-Way Matching** | ระบบกระทบยอด PO/GR/Invoice อัตโนมัติ |
| S01-06 | **Tolerance Limits** | การตั้งค่าความคลาดเคลื่อนที่ระบบยอมรับได้ |
| S01-07 | **Immutable Master Data Log** | บันทึก Before/After ห้ามลบเด็ดขาด |

## 2. ISO/IEC 27001 — Information Security

_ความมั่นคงปลอดภัยสารสนเทศ_

**Control ID Range:** S02-01 ถึง S02-07

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S02-01 | **Password Policy** | อายุรหัสผ่าน, ความซับซ้อน, ห้ามใช้ซ้ำ |
| S02-02 | **MFA Enforcer** | บังคับยืนยันตัวตนสองชั้นสำหรับธุรกรรมความเสี่ยงสูง |
| S02-03 | **Session Management** | เตะออกเมื่อ Idle, ป้องกันล็อกอินซ้อน |
| S02-04 | **Data Masking/Obfuscation** | เซนเซอร์ข้อมูล PII หรือ BOM บนหน้าจอ |
| S02-05 | **Data Classification Tags** | บังคับติด Tag ระดับความลับก่อน Export |
| S02-06 | **Export Limits** | จำกัดจำนวนแถวการโหลดข้อมูลต่อวัน |
| S02-07 | **Geolocation Block** | จำกัดให้เข้าถึงโมดูลสำคัญได้เฉพาะในเครือข่าย |

## 3. NIST CSF 2.0 — Cyber Resilience & SOC

_การเฝ้าระวังและการตอบสนอง_

**Control ID Range:** S03-01 ถึง S03-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S03-01 | **SCRM Access Control** | ควบคุมสิทธิ์แบบ Read-only สำหรับ Vendor |
| S03-02 | **Policy Versioning** | เก็บประวัติการแก้ Policy และปุ่ม Rollback |
| S03-03 | **Zero Trust Access** | ตรวจสอบบริบท (IP, Device) ก่อนให้เข้าโมดูลสำคัญ |
| S03-04 | **Anomaly Detection** | แจ้งเตือนล็อกอินข้ามพื้นที่ (Impossible Travel) |
| S03-05 | **Emergency Kill Switch** | ปุ่มฉุกเฉินเตะ User ทั้งหมดและปิด API ทันที |
| S03-06 | **Automated Restore Trigger** | ดึง Backup ล่าสุดกลับมาอัตโนมัติเมื่อโดนโจมตี |

## 4. COBIT 2019 — IT Governance & Value

_ธรรมาภิบาลและความคุ้มค่า_

**Control ID Range:** S04-01 ถึง S04-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S04-01 | **IT Investment Gate** | บังคับแนบ Business Case/ROI ก่อนขออนุมัติ |
| S04-02 | **Benefit Tracking** | แจ้งเตือน PM ให้ประเมินผลลัพธ์หลัง Go-live 6 เดือน |
| S04-03 | **Resource & Capacity Limits** | จำกัด Token AI หรือโควตาการประมวลผล |
| S04-04 | **CAB & UAT Enforcement** | บังคับแนบหลักฐานเทสต์ก่อนเอาขึ้น Production |
| S04-05 | **Standard Master Data Mapping** | บังคับรูปแบบการตั้งชื่อ (Naming Convention) |
| S04-06 | **SLA & Escalation Rules** | ตั้งเวลาแจ้งเตือนผู้บริหารหากระบบค้างนาน |

## 5. CIS Controls v8 — System Hardening

_การตั้งค่าระบบพื้นฐานให้รัดกุม_

**Control ID Range:** S05-01 ถึง S05-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S05-01 | **Dormant Account Disablement** | ปิดบัญชีที่ไม่ได้ล็อกอินเกินกำหนด (เช่น 45 วัน) |
| S05-02 | **Force Password Change** | บังคับเปลี่ยนรหัสผ่านเมื่อเข้าใช้ครั้งแรก |
| S05-03 | **Secure Protocol Blocker** | บังคับใช้ TLS 1.2+ ขึ้นไปเท่านั้น |
| S05-04 | **Automated Data Purge** | สคริปต์ลบไฟล์ชั่วคราวเมื่อหมดอายุการใช้งาน |
| S05-05 | **NTP Validation** | ซิงค์เวลาเซิร์ฟเวอร์ทั้งหมดให้ตรงกันระดับมิลลิวินาที |
| S05-06 | **IG Profile Auto-Scaler** | ปุ่มปรับระดับความเข้มงวด (IG1, IG2, IG3) อัตโนมัติ |

## 6. NIST SP 800-53 — Advanced Access & Audit

_การเข้าถึงและบันทึกระดับสูง_

**Control ID Range:** S06-01 ถึง S06-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S06-01 | **ABAC (Attribute-Based Access)** | ให้สิทธิ์โดยดูจาก บทบาท+สถานที่+เวลา |
| S06-02 | **Force Disconnect** | ตัด Session ทันทีเมื่อสิทธิ์ของพนักงานถูกเปลี่ยน |
| S06-03 | **Standardized Audit Content** | บังคับ Log ต้องมี (Who, What, When, Where, Result) |
| S06-04 | **Audit Failure Alert** | แจ้งเตือนเมื่อพื้นที่เก็บ Log ใกล้เต็ม |
| S06-05 | **Payload Encryption** | เข้ารหัสข้อมูลระดับ Field สำหรับข้อมูลอ่อนไหว |
| S06-06 | **Input Sanitization** | กรองอักขระพิเศษทุกช่องกรอกข้อมูลป้องกัน Injection |

## 7. ISO/IEC 27701 — Privacy & PDPA/GDPR

_การคุ้มครองข้อมูลส่วนบุคคล_

**Control ID Range:** S07-01 ถึง S07-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S07-01 | **Granular Consent** | แยกประเภทความยินยอม (บังคับ/เลือกได้) |
| S07-02 | **Consent Withdrawal** | แจ้งเตือนทุกโมดูลให้หยุดประมวลผลเมื่อมีการถอนความยินยอม |
| S07-03 | **Automated Data Portability** | ปุ่มดาวน์โหลดข้อมูลส่วนตัวสำหรับ User |
| S07-04 | **Anonymization (Right to be Forgotten)** | สคริปต์แปลงชื่อเป็นนามแฝงเมื่อร้องขอ |
| S07-05 | **Dynamic Data Purging** | ลบข้อมูลพนักงานเก่าอัตโนมัติเมื่อครบกำหนด (เช่น 10 ปี) |
| S07-06 | **PII Tagging & Masking** | แปะป้ายฟิลด์ข้อมูลส่วนบุคคลเพื่อควบคุมพิเศษ |

## 8. NIST Privacy Framework — Privacy Engineering

_วิศวกรรมความเป็นส่วนตัว_

**Control ID Range:** S08-01 ถึง S08-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S08-01 | **PII Data Flow Tracker** | ตรวจจับว่าข้อมูลส่วนบุคคลถูกส่งไป API ไหนบ้าง |
| S08-02 | **Automated PII Discovery** | สแกนหาข้อมูล PII ที่แอบซ่อนอยู่ใน Text box ทั่วไป |
| S08-03 | **Dynamic Pseudonymization** | ทำข้อมูลแฝงแบบ Real-time ก่อนส่งให้ AI วิเคราะห์ |
| S08-04 | **Data Perturbation** | บวกตัวเลขสุ่มเข้าไปในสถิติเพื่อป้องกันการระบุตัวตน |
| S08-05 | **Processing Transparency Log** | บันทึกว่า AI ตัวไหนใช้ข้อมูลอะไรไปตัดสินใจ |
| S08-06 | **Automated DPIA Trigger** | บังคับทำประเมินความเสี่ยงเมื่อเปิดใช้ฟีเจอร์ใหม่ |

## 9. IEC 62443 — IT/OT Network Security

_ความปลอดภัยรอยต่อโรงงาน_

**Control ID Range:** S09-01 ถึง S09-05

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S09-01 | **DMZ Enforcer** | บังคับให้ ERP ดึงข้อมูลผ่าน Historian Server ตรงกลางเท่านั้น |
| S09-02 | **API Conduit Whitelisting** | อนุญาตเฉพาะโปรโตคอลฝั่ง OT (เช่น MQTT, OPC UA) |
| S09-03 | **Strict Read-Only** | ล็อกระดับระบบ ห้ามส่งคำสั่งควบคุม(Write)กลับไปที่เครื่องจักร |
| S09-04 | **SL-Based Authentication** | บังคับ MFA เฉพาะหน้าจอที่ดูข้อมูลระดับ High-Impact |
| S09-05 | **IT/OT Severance Switch** | ปุ่มตัดขาด API ระหว่างออฟฟิศกับโรงงานกรณีฉุกเฉิน |

## 10. NIST SP 800-82 — OT Operations Controls

_การควบคุมปฏิบัติการหน้างาน_

**Control ID Range:** S10-01 ถึง S10-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S10-01 | **Purdue Level Routing** | บล็อกการยิง API ข้ามเลเยอร์ไปหาเครื่องจักรโดยตรง |
| S10-02 | **Data Polling Rate Limiter** | จำกัดความถี่ในการดึงข้อมูลไม่ให้เครื่องจักรโหลดหนัก |
| S10-03 | **OT-Safe Lockout** | ยกเว้นการล็อกบัญชีเมื่อใส่รหัสผิดสำหรับคอมพิวเตอร์หน้างาน (Safety) |
| S10-04 | **Workstation Binding** | เปิดฟีเจอร์บางอย่างได้จากคอมในห้อง Control Room เท่านั้น |
| S10-05 | **JIT Vendor Tunneling** | เปิดให้ Vendor รีโมทเข้ามาได้เฉพาะช่วงเวลาที่อนุมัติ |
| S10-06 | **Maintenance Window Scheduler** | ระงับการอัปเดตระบบในช่วงที่สายพานเดินเครื่อง |

## 11. SOC 2 (Type I & II) — Continuous Evidence

_การรวบรวมหลักฐานอัตโนมัติ_

**Control ID Range:** S11-01 ถึง S11-05

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S11-01 | **UAR Scheduler** | ระบบสร้างตั๋วให้หัวหน้าแผนกทบทวนสิทธิ์ลูกน้องทุก 90 วัน |
| S11-02 | **Ticket Enforcement** | บังคับใส่เลข Ticket ทุกครั้งที่มีการสร้าง/ลบ User |
| S11-03 | **Automated Restore Test** | ทดสอบสคริปต์กู้คืนฐานข้อมูลประจำเดือนอัตโนมัติ |
| S11-04 | **Batch Reconciliation** | กระทบยอดข้อมูลรับ-ส่ง และแจ้งเตือนเมื่อตกหล่น |
| S11-05 | **Continuous Evidence Export** | ถ่ายรูปตั้งค่าและแพ็กไฟล์ Log ส่งเข้า Audit Vault รายสัปดาห์ |

## 12. ISO 22301 — Business Continuity

_ความต่อเนื่องทางธุรกิจ_

**Control ID Range:** S12-01 ถึง S12-06

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S12-01 | **Module Tiering (RTO/RPO)** | จัดลำดับความถี่ในการแบ็คอัป (โมดูลสำคัญสุด แบ็คอัปถี่สุด) |
| S12-02 | **Auto-Read-Only Fallback** | ตัดเข้าโหมดอ่านอย่างเดียวเพื่อให้หน้างานเปิดดูข้อมูลต่อได้ |
| S12-03 | **Auto-Failover Trigger** | สลับ Traffic ไปไซต์สำรองทันทีเมื่อระบบหลักล่ม |
| S12-04 | **BCP Mode (Break-Glass)** | ปุ่มปลดล็อก SoD ชั่วคราวให้ทำงานข้ามขั้นตอนได้ยามฉุกเฉิน |
| S12-05 | **Offline Sync Queue** | อนุญาตให้บันทึกข้อมูลลงเครื่อง Local แล้วซิงค์ทีหลังเมื่อเน็ตมา |
| S12-06 | **Emergency Broadcast** | ยิง SMS/Line สั่งการพนักงานทุกโรงงานพร้อมกัน |

## 13. NIST AI RMF — AI Safety & Limits

_ความปลอดภัยของระบบ AI_

**Control ID Range:** S13-01 ถึง S13-03

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S13-01 | **Output Sanitization** | บังคับให้มนุษย์กดยืนยัน (Human-in-the-loop) ถ้ายอด AI แกว่งเกินเกณฑ์ |
| S13-02 | **Prompt Injection Protection** | สกัดกั้นคำสั่งที่พยายามหลอกให้ AI ล้วงข้อมูล |
| S13-03 | **Agent Execution Limits** | ตั้งเวลา Timeout ตัดการทำงาน AI หากประมวลผลนานเกินไป |

## 14. OWASP API Security — Gateway Protection

_การป้องกันจุดเชื่อมต่อ API_

**Control ID Range:** S14-01 ถึง S14-03

| Control ID | ชื่อ Control | คำอธิบาย |
|---|---|---|
| S14-01 | **Rate Limiting & Throttling** | จำกัดจำนวน Request ต่อนาที ป้องกันระบบพัง |
| S14-02 | **Payload Schema Validation** | ตรวจสอบโครงสร้างข้อมูลที่ส่งมา หากผิดฟอร์มให้เตะทิ้ง |
| S14-03 | **JWT Lifecycle** | ตั้งเวลาหมดอายุของ Token การเชื่อมต่อให้สั้นที่สุดและรีเฟรชอัตโนมัติ |


---

**Total Controls:** 78
