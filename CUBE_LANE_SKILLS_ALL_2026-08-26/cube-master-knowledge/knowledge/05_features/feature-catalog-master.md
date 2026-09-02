---
file_id: KB-05-01
title: CUBE Master Feature Catalog
version: 2.2.0
last_updated: 2026-08-25
status: active
source: |
  CUBE_6BOOKS_ROLLUP_REPORT.html (24 ส.ค. 2026) tab ② A "Feature เดิมที่มี — 7C Wave Plan · 136 features"
  + CUBE_7C_COVERAGE_FLOW.html ④ Wave Plan (สถานะ/chip/wave — v1, dependency v2 รอ rebuild)
  + baseline platform ที่ทำแล้วแต่ไม่อยู่ในแผง (มติ user 2026-08-25)
note: |
  ★ v2.0 = rebase ทั้งฉบับ — ยึดรายการ 136 (+4 backbone/CS) ของแผง 7C เป็น catalog เดียว
  ไม่รวม feature ใหม่ 201 ตัวจาก 6 เล่ม (roadmap แยก — ยังไม่ lock ไม่ใช่ product)
---

# CUBE Master Feature Catalog (v2.0 — rebased 2026-08-25)

## Quick Reference (TL;DR)

- **ระบบเดียว Core ERP** (core.2bsimple.com) — 12 module areas · **140 features ในแผง 7C** (136 + backbone 4) · เสร็จ **54** (ทั้งหมดเป็น build จริง ยกเว้น Consequence Engine = BA เสร็จส่ง dev) · ค้าง **86** ใน W1–W9
- **Baseline platform ที่มีแล้ว (ไม่ต้องออกแบบใหม่ — ทุก feature ใหม่ต้องเรียกใช้ ไม่ทำเอง):** ดู §0
- ของเดิมนอกแผง (Cubic Registry · Agent/Skill Library · QA Feature Tester · CRM · Asset · Organization · IT Ticket) ดู §2
- 6 เล่ม C-Level (201 feature ใหม่) = roadmap input เท่านั้น — ไม่อยู่ใน catalog นี้ (ถ้าจะเก็บ → ไฟล์แยก `08_roadmap/`)
- สถานะ dev สด → tracking sheet ผ่าน `cube-master-tracking-generator` · สถานะ BA ต่อ feature → `FEATURE_REGISTRY.md`

---

## §0 Baseline Platform — มีแล้ว ใช้เป็นฐานของทุก feature (ห้าม re-implement)

| ฐาน | สิ่งที่มีแล้ว | feature ใหม่ต้องทำแค่ | skill/contract |
|---|---|---|---|
| **Operation Process** (module แยก) | Template CL/SOP/SOW · OP Configuration (type/sub-type · SLA · frequency · assignment) · งานทั้งหมด/งานเกี่ยวข้อง/งานของฉัน · Operation Cockpit (Gantt) · runtime F-95A/B/C · Work Projects (nested folder/ACL) · Template Cluster · parallel start | ประกาศงานเป็น SOW / ผูก event `sow.*` (OC มาอัตโนมัติ) | `op-pipeline-html-generator` · workflow_graph |
| **Action Plan + Team Plan** | แผนงานประจำวันของฉัน (ปฏิทิน/วัน/Gantt/build pool DnD/capacity/AI plan) · แผนงานของทีม (คน×7วัน · แก้ในฐานะหัวหน้า) | ส่งงานเข้า pool ผ่าน OP — ไม่สร้าง planner ใหม่ | html-generator-v9 Pattern P |
| **DOA Engine** (Policy Center) | สายอนุมัติกลาง threshold/delegate/expiry/SoD · `GET /doa/resolve` · slot picker เลือก "คน" ในตำแหน่ง (avatar+position+name — มติ 2026-08-17) · doa_pending/doa_result → NOTIFY อัตโนมัติ | ออก `DOA_BRIEF` ประกาศ action/วงเงิน — **ห้าม hardcode chain** | `doa-declaration` |
| **Document Configuration** (F-DOCCFG) | Document Type Master กลาง: เลขรัน `ENG-DOC-NUM.next()` + snapshot/สำเนา `ENG-DOC-STORE.store()` | ออก `DOCCFG_BRIEF` ประกาศ doc_type — ห้าม hardcode รูปแบบเลข | `doccfg-declaration` |
| **Notification System** (ENG-NOTIFY) | Cubic registry/rule/template · logs · Core bell/inbox/preference · in-app/email/LINE | ออก `NTF_BRIEF` ประกาศ event ธุรกิจ (ไม่ประกาศซ้ำ doa_*) | `ntf-declaration` |
| **Roles & Permissions · Employee · User Mgmt** | Roles/Permission matrix · Employee Master · User account/session · Password Policy · MFA · Session Mgmt · Data Masking (Policy Center 6/8) | อ้าง role id จาก Policy — ไม่ทำ permission ในตัว · ทุก field คน = Employee Master combobox | Policy Center |
| **7C Consequence Engine** (ENG-CSQ · F-CSQ-01) | event log + profile registry + evaluator · 7 ท่อ OC/SecC/EC/AC/FC/DC/SC (OC จาก OP · DC-doc จาก DOA · SC สงวน) — BA เสร็จ ส่ง dev 23 ส.ค. | ออก `CSQ_BRIEF` เฉพาะท่อ EC/SecC/AC/FC/DC-decision — ท่อต้องห้าม = 422 | `csq-declaration` |
| **Knowledge Center · Agent (Chat Bubble/Binding) · CS Onboarding Tracker** | มีแล้ว (General 14/14) | — | — |
| **Cubic** (แยก site) | Platform/Module/Feature/AIR/Engine/API Registry · Sandbox · Onboarding | ลง engine candidate ผ่าน Architect | — |

**กติกาเหล็กที่ทุก feature ต้องเคารพ:** DOA iron rule (`GET /doa/resolve`) · soft reference LD-4C-02 (master = picker assist, nullable, no cascade) · audit append-only ไม่มี hard delete · legal/config parameter ใช้ `effective_date` (HR-1) · engine-in-feature (engine เกิดใน feature → ลง CUBIC เป็น candidate) · Module Linkage (เชื่อม/ไม่เชื่อม + manual override)

---

## §1 Catalog — แผง 7C Wave Plan (140 = 136 + backbone/CS) · เสร็จ 54 / ค้าง 86

สถานะจาก Wave Plan 22–24 ส.ค. 2026 · Declarations = chip บนแผง (⚖ doa · 🔔 ntf · ◆ csq) + doccfg เมื่อเป็นเอกสาร + **pdfdoc** = ต้องรัน `thai-doc-pdf-generator` (template.html + sample.pdf + print-spec แนบ FRD) เมื่อ feature ออกเอกสาร/แบบฟอร์มทางการ · Archetype = แบบประกอบ html-generator-v9 ที่ต้องใช้ (Q = Transaction Document · P = Planner · J = Dashboard · master = A+B+C)

### Operation Process — CL/SOP/SOW · งาน · Cockpit · Action/Team Plan · Configuration — เสร็จ 8/8
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Template CL/SOP/SOW · แม่แบบกระบวนการ | ✅ เสร็จ | — | — | console/OP |  |
| Operation Process Configuration · ตั้งค่า OP — Type/Sub-type · SLA · frequency · assignment rule | ✅ เสร็จ | — | — | master/config |  |
| งานทั้งหมด · Operation Process | ✅ เสร็จ | — | — | console/OP |  |
| งานเกี่ยวข้อง · Operation Process | ✅ เสร็จ | — | — | console/OP |  |
| งานของฉัน · Operation Process | ✅ เสร็จ | — | — | console/OP |  |
| Team Plan · แผนงานทีม | ✅ เสร็จ | — | — | P-planner |  |
| Operation Cockpit (Gantt) · ภาพรวมงาน | ✅ เสร็จ | — | — | J-dashboard |  |
| Action Plan · แผนปฏิบัติการ | ✅ เสร็จ | — | — | P-planner |  |

### General — ส่วนกลาง — เสร็จ 5/5
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Document Configuration · เลขรัน + snapshot policy | ✅ เสร็จ | — | — | master |  |
| Notification System · แจ้งเตือนกลาง | ✅ เสร็จ | — | — | master |  |
| Knowledge Center · คลังความรู้ | ✅ เสร็จ | — | — | master |  |
| AI Chat Bubble · ผู้ช่วย AI | ✅ เสร็จ | — | — | master |  |
| Agent Binding · ผูก agent | ✅ เสร็จ | — | — | master |  |

### Sales — O2C — เสร็จ 10/11
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Customer Segment · เซกเมนต์ลูกค้า | ✅ เสร็จ | — | — | master |  |
| Customer · ลูกค้า | ✅ เสร็จ | — | — | master |  |
| Prospect · ลีด | ✅ เสร็จ | — | — | master |  |
| Credit Limit · วงเงินเครดิต | ✅ เสร็จ | — | — | master |  |
| Sales Team / Salesperson · ทีมขาย | ✅ เสร็จ | — | — | master |  |
| Sales Price List · บัญชีราคา | ✅ เสร็จ | — | — | master |  |
| Trade Agreement · ข้อตกลงการค้า | ✅ เสร็จ | — | — | master |  |
| Promotion · โปรโมชัน | ✅ เสร็จ | — | — | master |  |
| Quotation · ใบเสนอราคา | ✅ เสร็จ | — | doccfg pdfdoc | Q-document |  |
| Sales Order · คำสั่งขาย | ✅ เสร็จ | — | doccfg pdfdoc | Q-document |  |
| Sales Return · รับคืนของ | ⏳ ค้าง | W4 | doa ntf csq doccfg pdfdoc | Q-document |  |

### Marketing — เสร็จ 0/10
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Consent PDPA · opt-in/out ลูกค้า | ⏳ ค้าง | W1 | csq | master |  |
| Campaign · แคมเปญ · ใช้งบ | ⏳ ค้าง | W2 | doa ntf csq | master |  |
| Event Management · จัดงาน/บูธ | ⏳ ค้าง | W2 | ntf csq | master |  |
| Campaign ROI · ผลตอบแทนแคมเปญ (มุม EC) | ⏳ ค้าง | W3 | csq | J-dashboard |  |
| Content / Asset Library · คลังชิ้นงาน | ⏳ ค้าง | W8 | — | master |  |
| Email / Communication · สื่อสารลูกค้า | ⏳ ค้าง | W9 | ntf csq | master |  |
| Segmentation ขั้นสูง · แบ่งกลุ่มลึก | ⏳ ค้าง | W9 | csq | master |  |
| Lead Scoring · คะแนนลีด | ⏳ ค้าง | W9 | csq | master |  |
| Social Media · จัดการโซเชียล | ⏳ ค้าง | W9 | csq | master |  |
| UTM / Tracking · track ที่มาลูกค้า | ⏳ ค้าง | W9 | csq | master |  |

### Purchase — P2P — เสร็จ 1/5
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Vendor Master · ผู้ขาย | ✅ เสร็จ | — | — | master |  |
| PR ใบขอซื้อ · ขอซื้อ + อนุมัติ | ⏳ ค้าง | W2 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Compare Vendors · เทียบราคาผู้ขาย | ⏳ ค้าง | W2 | csq | master |  |
| PO ใบสั่งซื้อ · สั่งซื้อ · commitment | ⏳ ค้าง | W3 | doa ntf csq doccfg pdfdoc | Q-document |  |
| RTV คืนผู้ขาย · คืนของไม่ผ่าน | ⏳ ค้าง | W3 | doa ntf csq doccfg pdfdoc | Q-document |  |

### Warehouse — เสร็จ 6/16
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Warehouse &amp; Bin · คลัง/ตำแหน่ง | ✅ เสร็จ | — | — | master |  |
| Inventory (ATP) · ยอดคงคลัง | ✅ เสร็จ | — | — | master |  |
| Item Category · หมวดสินค้า | ✅ เสร็จ | — | — | master |  |
| Picking · จัดหยิบ | ✅ เสร็จ | — | doccfg pdfdoc | Q-document |  |
| Packing · แพ็ก | ✅ เสร็จ | — | doccfg pdfdoc | Q-document |  |
| Delivery Note · ส่งของ | ✅ เสร็จ | — | doccfg pdfdoc | Q-document |  |
| GRN รับของ · รับของ · GR/IR | ⏳ ค้าง | W3 | ntf csq doccfg pdfdoc | Q-document |  |
| Putaway · เก็บเข้า location | ⏳ ค้าง | W3 | csq | master |  |
| Stock Adjustment · ปรับยอด + อนุมัติ | ⏳ ค้าง | W3 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Stock Transfer · ย้ายคลัง/สาขา | ⏳ ค้าง | W3 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Stocktake · ตรวจนับใหญ่ | ⏳ ค้าง | W4 | doa csq | master |  |
| Reorder Point · จุดสั่งเติม | ⏳ ค้าง | W4 | ntf csq | master |  |
| Cycle Count + ABC · นับหมุนเวียน | ⏳ ค้าง | W4 | csq | master |  |
| Lot/Serial + Expiry · traceability | ⏳ ค้าง | W4 | csq | master |  |
| Quality Hold · กักของรอตรวจ | ⏳ ค้าง | W4 | doa ntf csq | master |  |
| Barcode / Mobile Scan · ช่องทาง capture | ⏳ ค้าง | W4 | — | master |  |

### OFM — Operation Factory Management — เสร็จ 8/8
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| ผังโรงงาน · layout โรงงาน | ✅ เสร็จ | — | — | master |  |
| ทะเบียนเครื่องจักร · machine registry | ✅ เสร็จ | — | — | master |  |
| ทะเบียนอะไหล่ · spare parts | ✅ เสร็จ | — | — | master |  |
| Location Permission · สิทธิ์พื้นที่ | ✅ เสร็จ | — | — | master |  |
| Operating Log · บันทึกเดินเครื่อง | ✅ เสร็จ | — | — | master |  |
| Work Order · ใบสั่งงานซ่อม/ผลิต | ✅ เสร็จ | — | doccfg pdfdoc | Q-document |  |
| Plant Health Dashboard · สุขภาพโรงงาน | ✅ เสร็จ | — | — | P-planner |  |
| Code Catalogs · รหัสมาตรฐาน OFM | ✅ เสร็จ | — | — | master |  |

### HR — เสร็จ 1/17
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Employee Master · พนักงาน | ✅ เสร็จ | — | — | master |  |
| ESS Portal · พนักงานทำเอง | ⏳ ค้าง | W1 | ntf csq | master |  |
| Salary Structure · โครงเงินเดือน | ⏳ ค้าง | W1 | csq | master |  |
| หนังสือรับรอง · เอกสารข้อมูลส่วนบุคคล | ⏳ ค้าง | W1 | doa ntf csq doccfg pdfdoc | Q-document |  |
| On/Offboard · เปิด-ปิดสิทธิ์ (revoke ตอนออก) | ⏳ ค้าง | W2 | doa ntf csq | master |  |
| Payroll · เงินเดือน (RESTRICTED) | ⏳ ค้าง | W2 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Expense Claim · เบิกค่าใช้จ่าย | ⏳ ค้าง | W5 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Welfare · สวัสดิการ | ⏳ ค้าง | W5 | doa csq | master |  |
| Manpower Planning · งบอัตรากำลัง | ⏳ ค้าง | W8 | doa csq | P-planner |  |
| Recruit / Candidate Pool · สรรหา | ⏳ ค้าง | W8 | doa ntf csq | master |  |
| Attendance · เวลาเข้างาน | ⏳ ค้าง | W8 | csq | master |  |
| OT / Shift · โอที/กะ | ⏳ ค้าง | W8 | doa ntf csq doccfg | Q-document |  |
| Leave · การลา | ⏳ ค้าง | W8 | doa ntf csq doccfg | Q-document |  |
| Performance · ประเมินผลงาน | ⏳ ค้าง | W8 | doa csq | master |  |
| Training &amp; Development · อบรม (เคส EC ไม่มี AC) | ⏳ ค้าง | W9 | doa csq | master |  |
| Succession Planning · ตัวตายตัวแทน | ⏳ ค้าง | W9 | csq | P-planner |  |
| Shift &amp; Roster · จัดกะ/เวร | ⏳ ค้าง | W9 | ntf csq | P-planner |  |

### Budget — เสร็จ 1/10
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Cost Center · ศูนย์ต้นทุน | ✅ เสร็จ | — | — | master |  |
| Fiscal Year · ปีงบประมาณ | ⏳ ค้าง | W6 | — | master |  |
| Budget Account · ผังบัญชีงบ | ⏳ ค้าง | W6 | csq | master |  |
| Budget Config · ตั้งค่างบ | ⏳ ค้าง | W7 | — | master |  |
| Budget Preparation · ตั้งงบ + อนุมัติ | ⏳ ค้าง | W7 | doa ntf csq | master |  |
| Department Budget · งบรายแผนก | ⏳ ค้าง | W7 | csq | master |  |
| Budget Control · ตรวจงบตอนสร้างเอกสาร | ⏳ ค้าง | W7 | csq | master |  |
| Budget Transfer · โอนงบ | ⏳ ค้าง | W7 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Budget Revision · เพิ่ม/ลดงบกลางปี | ⏳ ค้าง | W7 | doa ntf csq | master |  |
| Budget vs Actual · เทียบงบ-ใช้จริง | ⏳ ค้าง | W7 | — | master |  |

### Accounting — เสร็จ 3/18
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Chart of Accounts · ผังบัญชี | ✅ เสร็จ | — | — | master |  |
| GL Posting Group · กลุ่มลงบัญชี | ✅ เสร็จ | — | — | master |  |
| Tax Code · รหัสภาษี | ✅ เสร็จ | — | — | master |  |
| Fixed Asset / ค่าเสื่อม · ทะเบียนสินทรัพย์ + Post ค่าเสื่อม | ⏳ ค้าง | W2 | doa csq | master |  |
| Landed Cost · ต้นทุนแฝงนำเข้า | ⏳ ค้าง | W2 | csq | master |  |
| Inventory Valuation / Costing · FIFO/Avg — cost basis | ⏳ ค้าง | W2 | csq | master |  |
| Currency &amp; Exchange Rate · สกุลเงิน/อัตราแลกเปลี่ยน | ⏳ ค้าง | W4 | csq | master |  |
| Journal Entry · สมุดรายวัน | ⏳ ค้าง | W4 | doa csq doccfg pdfdoc | Q-document |  |
| AR Invoice · แจ้งหนี้ขาย | ⏳ ค้าง | W5 | ntf csq doccfg pdfdoc | Q-document |  |
| AP Invoice · ตั้งหนี้ซื้อ (3-way) | ⏳ ค้าง | W5 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Credit Note · ลดหนี้ลูกค้า | ⏳ ค้าง | W5 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Debit Note · ลดหนี้ผู้ขาย | ⏳ ค้าง | W5 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Bank Reconciliation · กระทบยอดธนาคาร | ⏳ ค้าง | W5 | csq | master |  |
| Recurring JE · รายการซ้ำอัตโนมัติ | ⏳ ค้าง | W5 | csq | master |  |
| Accrual ตั้งค้าง · เกณฑ์คงค้าง | ⏳ ค้าง | W5 | csq | master |  |
| Period-End Closing · ปิดงวด + lock | ⏳ ค้าง | W6 | doa ntf csq | master |  |
| VAT Report ภ.พ.30 · ภาษีขาย-ซื้อ | ⏳ ค้าง | W6 | csq pdfdoc | J-dashboard |  |
| WHT Report ภ.ง.ด.3/53 · หัก ณ ที่จ่าย | ⏳ ค้าง | W6 | csq pdfdoc | J-dashboard |  |

### Finance — เสร็จ 3/12
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Payment Terms · เงื่อนไขชำระ | ✅ เสร็จ | — | — | master |  |
| Bank Master · ธนาคาร | ✅ เสร็จ | — | — | master |  |
| Payment Method · วิธีชำระ | ✅ เสร็จ | — | — | master |  |
| Petty Cash · เงินสดย่อย | ⏳ ค้าง | W4 | doa ntf csq | master |  |
| Advance เงินทดรอง · จ่ายก่อน-เคลียร์หลัง | ⏳ ค้าง | W5 | doa ntf csq | master |  |
| Receipt Voucher · รับเงิน · ล้าง AR | ⏳ ค้าง | W6 | ntf csq doccfg pdfdoc | Q-document |  |
| Payment Voucher · จ่ายเงิน · ล้าง AP | ⏳ ค้าง | W6 | doa ntf csq doccfg pdfdoc | Q-document |  |
| Cheque / PDC · เช็ครับ-จ่ายล่วงหน้า | ⏳ ค้าง | W6 | ntf csq | master |  |
| WHT Cert 50 ทวิ · หนังสือรับรองหักภาษี | ⏳ ค้าง | W6 | csq pdfdoc | master |  |
| Cash Flow · กระแสเงินสด | ⏳ ค้าง | W7 | csq | master |  |
| Collections ติดตามหนี้ · งานทวงถาม · DSO | ⏳ ค้าง | W7 | ntf csq | master |  |
| Cash Forecast · พยากรณ์เงินสด | ⏳ ค้าง | W8 | csq | master |  |

### Policy Center — เสร็จ 6/8
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| DOA · สายอนุมัติกลาง | ✅ เสร็จ | — | — | master |  |
| Roles &amp; Permissions · บทบาท-สิทธิ์ | ✅ เสร็จ | — | — | master |  |
| Password Policy · นโยบายรหัสผ่าน | ✅ เสร็จ | — | — | master |  |
| MFA · ยืนยันตัวหลายชั้น | ✅ เสร็จ | — | — | master |  |
| Session Management · จัดการ session | ✅ เสร็จ | — | — | master |  |
| Data Masking · ปกปิดข้อมูล | ✅ เสร็จ | — | — | master |  |
| Audit Trail · audit กลาง — ใช้ event log ของ Engine ร่วม | ⏳ ค้าง | W1 | — | master |  |
| Data Classification · ชั้นความลับข้อมูล | ⏳ ค้าง | W1 | — | master |  |

### 7C Engine (backbone + config) — เสร็จ 1/4
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| Consequence Engine · event log + profile config + evaluator (รวม 1 feature · ENG-CSQ) | 🟢 BA เสร็จ ส่ง dev | W1 | — | master/config | Architect register ENG-CSQ-01/02 · dev สร้าง table |
| Rate Card · อัตราค่าแรง/เครื่อง (enabler EC) | ⏳ ค้าง | W1 | csq | master/config |  |
| Allocation Driver · ตัวกระจายต้นทุน (enabler EC) | ⏳ ค้าง | W1 | csq | master/config |  |
| Terminal Decision Record · Continue/Adjust/Hold/Stop/Complete | ⏳ ค้าง | W3 | csq | master |  |

### Report — 7C Consequence (7 หน้า) — เสร็จ 0/7
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| หน้า Operation Consequence · read model ท่อ OC | ⏳ ค้าง | W1 | — | master |  |
| หน้า Security Consequence · read model ท่อ SecC | ⏳ ค้าง | W2 | — | master |  |
| หน้า Economic Consequence · read model ท่อ EC | ⏳ ค้าง | W3 | — | master |  |
| หน้า Decision Consequence · read model ท่อ DC | ⏳ ค้าง | W3 | — | master |  |
| หน้า Accounting Consequence · read model ท่อ AC | ⏳ ค้าง | W6 | — | master |  |
| หน้า Financial Consequence · งบ P&amp;L/BS/CF + Ratio | ⏳ ค้าง | W8 | — | master |  |
| Business Central · convergence ทุกท่อ | ⏳ ค้าง | W8 | — | master |  |

### Customer Success — เสร็จ 1/1
| Feature | สถานะ | Wave | Declarations | Archetype (v9) | Dep |
|---|---|---|---|---|---|
| CS Onboarding Tracker · ติดตาม onboarding | ✅ เสร็จ | — | — | master |  |

> ⚠ ต้อง reconcile กับ FEATURE_REGISTRY.md: แผงนับ HR เสร็จ 1/17 แต่ registry บันทึก F-HR-01/02/03/04/11 done (5) · OFM แผงนับ 8/8 แต่ registry บอก F-OFM-14 Code Catalogs กำลังทำ — ยึด registry สำหรับ "BA เสร็จ" และยึดแผง/tracking sheet สำหรับ "build เสร็จ" (คนละความหมาย)

---

## §2 ของเดิมนอกแผง (มีอยู่จริง · นับเป็นฐาน Y/P ตอนเทียบ 6 เล่ม)

| กลุ่ม | feature | หมายเหตุ |
|---|---|---|
| Cubic | Platform / Module / Feature / AIR / Engine / API Registry · Notification registry · Sandbox · Onboarding | แยก site cubic4 |
| Agent | Agent/Skill Library · Agent Binding · Chat Bubble · Launcher | ใน Core |
| QA | Feature Tester (F-QA-001 · CSV parser ENG-QA-CSV-PARSER-001) · Ticket | ใน Core |
| Operation อื่น | CRM · Asset · Organization · IT Ticket · Customer Success | ใน Core |
| Knowledge (+CMS) | Hub · Login/Register/Profile · Article/Pillar/Author/Scraping CMS | แยก site |

---

## §3 Roadmap นอก catalog (อ้างอิงเท่านั้น)

CUBE_6BOOKS_ROLLUP_REPORT (24 ส.ค. 2026): feature ใหม่ 201 ตัวจาก 6 เล่ม C-Level (CHRO 55 · CCO 28 · CPO 26 · Data&AI 26 · EXS 28 · GRC 36 + shared engine 2) — ข้อเสนอ #1 คือจบ W1–W9 ก่อน (P→Y ก้อนใหญ่สุด) · #2 Decision–Action–Evidence Ledger Engine ต่อยอด TDR+OP — **ยังไม่ lock ไม่ใส่ใน catalog จนกว่า Strike เลือกก้อน**

---

## Change Log

- **2.2.0** (2026-08-25): เพิ่ม declaration `pdfdoc` (thai-doc-pdf-generator) 29 features
- **2.1.0** (2026-08-25): แยก module **Operation Process** ออกจาก General (CL/SOP/SOW · งานทั้งหมด/เกี่ยวข้อง/ของฉัน · Cockpit · Action/Team Plan) + เพิ่ม **Operation Process Configuration** · ตัด Type/Sub-type Master (= ส่วนหนึ่งของ CL/SOP/SOW)
- **2.0.0** (2026-08-25): Rebase ทั้งฉบับตามแผง 7C (136+4) + §0 Baseline Platform (OP/Action-Team Plan/DOA/DOCCFG/NOTIFY/Roles-Employee-User/ENG-CSQ) + §2 ของเดิมนอกแผง + §3 roadmap pointer — แทน v1.0 (Cubic-era draft 2026-05-27, ~131 features แยก 7 domain)
- **1.0.0** (2026-05-27): Initial draft — seeded from CUBE 4.0 Master Bible §3 + P2P backlog
