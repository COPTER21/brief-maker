# F-HR-OSW DevPack — แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ (Off-site Work Request)

> Core Cube › HR · ลูกค้า Credence (แบบฟอร์ม FM-HRM-02 Rev.00) · จัดทำ 5 ต.ค. 2569
> ชุดส่ง dev = **Prototype (หน้าจอจริง) + FRD Pack (ระบบ) + UI Brief (แผนที่โค้ด)** · ที่เหลือเป็นเอกสารประกอบ

## อ่านอะไรก่อน
| คุณคือ | อ่านตามลำดับ |
|---|---|
| ทุกคน | `03_FRD/…/00_OVERVIEW.md` → `07_LOCKED_DECISIONS.md` (มติที่ห้ามเปลี่ยน) → เปิด `01_Prototype` เล่นจริง |
| FE | `01_Prototype/offsite-work-request.html` → `04_UI_Brief` → FRD `01_UI.md` |
| BE | FRD `02_API` → `03_LOGIC` → `04_DB` → `05_RULES` → `05_Governance` (DOA / DOCCFG / MDOC) → `07_Print` |
| QA | `06_Test/testcase-F-HR-OSW.html` (UAT ฉบับคน) · `06_Test/testcases-F-HR-OSW.md` (AI agent) · FRD `06_TESTS.md` |
| PM / Owner | `02_BRD` · FRD `00_OVERVIEW §0.8` (คำถามค้าง) |

## โฟลเดอร์
| โฟลเดอร์ | มีอะไร |
|---|---|
| `01_Prototype` | HTML single-file · หน้าจอจริงทั้งหมด (รายการ · สร้าง 3 ขั้น · รายละเอียด 4 แท็บ · 5 modal) |
| `02_BRD` | BRD v1.0 (.md + .docx) — APPROVED มีเงื่อนไข |
| `03_FRD` | FRD Pack v1.0.1 แบบ FULL (00–07 + INDEX) |
| `04_UI_Brief` | UI Brief AS-BUILT — tokens · z-index · route · overlay · state · microcopy · mock → API |
| `05_Governance` | DOA_BRIEF v1.1 · DOCCFG_BRIEF v1.1 · MDOC_BRIEF + payload · มติ DA (DECISIONS) |
| `06_Test` | test case สำหรับ AI agent · ชุดเทส UAT ฉบับคน (HTML) · QA audit |
| `07_Print` | แบบพิมพ์ FM-HRM-02 (template + ตัว render + ข้อมูลตัวอย่าง + PDF ตัวอย่าง + print-spec + CSS patch ของ thai-doc) |
| `08_Reference` | แบบฟอร์มต้นฉบับลูกค้า · PREBRIEF จาก CMS (REQ-2569-0011) + ฉบับทำใหม่ (REQ-2569-0000) · สรุปผลกระทบ |

## งาน backend โดยสรุป
- **API 13 ตัว** (`/api/v1/osw` …) · **Function 16 ตัว** · **4 ตาราง** (`T_osw_request` · `T_osw_line` · `T_osw_attachment` · `T_osw_audit`)
- **ใช้ของกลางที่มีอยู่ ไม่สร้างใหม่:** DOA engine (สายอนุมัติ N ขั้น เรียงขั้น) · ENG-DOC-NUM (เลขที่) · ENG-DOC-STORE (เก็บ PDF ตอนอนุญาตครบ) · ENG-NOTIFY · F-DOCCFG (สถานะเปิดใช้ + ตั้งค่าพิมพ์) · Organization (หัวกระดาษ) · ExpensePolicy (อัตราเบี้ยเลี้ยง)
- **Engine ใหม่ 1 ตัว:** `doc-print-template-render` (logic-less template → PDF) — ใช้ซ้ำกับแบบฟอร์มลูกค้าตัวอื่นได้ · ตัวอ้างอิงอยู่ที่ `07_Print/render_osw.py`

## จุดที่ต้องระวัง
1. **ห้าม hardcode:** อัตรา 150 บาท · เวลา 08:30–17:30 · รูปแบบเลข OSW · ผู้อนุมัติ · จำนวนช่องลายเซ็น — ทั้งหมดมาจาก config / engine
2. **สายอนุมัติ = DOA กลาง (dynamic · ไม่มีวงเงิน)** — feature เก็บ snapshot ตอนส่ง · ไม่อนุญาต = จบใบ (ทำซ้ำเป็นใบใหม่)
3. **สถานะเปิดใช้งานและตั้งค่าพิมพ์อยู่ที่ F-DOCCFG** (ไม่ใช่ F185 แล้ว) · หัวกระดาษเก็บติดเอกสารตอนออกเลข · ช่องลายเซ็น = ผู้ขอ + 1 ช่องต่อขั้น DOA
4. **PDF ใช้ template ไฟล์เดียวกับ prototype** — ผลจาก `render_osw.py` ตรงกับ prototype ทุก byte (ตรวจแล้ว)
5. **ของที่มีเฉพาะ prototype — ไม่ต้องทำ:** ตัวสลับผู้ใช้ในเมนูชื่อ · `S.sim` จำลอง API ล้ม · ปุ่มดาวน์โหลดใน prototype ใช้หน้าต่างพิมพ์แทนไฟล์จริง
6. ค่าสถานะใน prototype `pending` = FRD `pending_approval` (label "รออนุญาต" เหมือนกัน)
7. `audit.sh` ของ html-generator ขึ้น FAIL 9 ข้อเรื่องตัวแก้รายการสินค้า — เอกสารนี้ไม่มีรายการสินค้า (FRD 07 CD-03)

## ต้องปิดก่อน
| ก่อนอะไร | รายการ | ใคร |
|---|---|---|
| ส่ง dev | ใบ Sign-off ลูกค้ายืนยันมติ 10 ข้อ + ของจากโครงมาตรฐาน (เอกสารแนบ · ทำซ้ำ · ส่งออก CSV) | BA → ลูกค้า |
| BE เริ่ม | เจ้าของ ExpensePolicy.per_diem + หน้าตั้งค่าอัตรา | พี่เบิร์ด |
| ตั้งค่า DOA | ยืนยัน `role-line-manager` ใช้ได้ที่ DOA กลาง · ตั้ง entry `osw` | DOA owner |
| deploy | เช็ครหัส `OSW` ไม่ชน registry F-DOCCFG · register DOCCFG + MDOC (สถานะรอเปิดใช้) | ทีม 2B |
| deploy | อัป `07_Print/base_form_patch.css` เข้าสกิล thai-doc-pdf-generator กลาง | ทีมสกิล |
| ไม่บล็อก | SLA การพิจารณา (OQ-04) · ทำ NTF_BRIEF (`osw_cancelled`) · รัน qc-ux / qc-coverage อย่างเป็นทางการ | BA |

## สถานะการตรวจ prototype
E2E 64/64 · PDF/DOA 13/13 · smoke ทุกหน้าจอไม่มี error · self_audit PASS · แก้รอบล่าสุด: ผู้บังคับบัญชาไม่เห็นใบร่างของลูกน้อง (BR-OSW-19)

## md5
| ไฟล์ | md5 (8 ตัวแรก) |
|---|---|
| `01_Prototype/offsite-work-request.html` | `c4c8a371` |
| `02_BRD/BRD_F-HR-OSW.docx` | `4e3fc838` |
| `02_BRD/BRD_F-HR-OSW.md` | `8d44b8cf` |
| `03_FRD/FRD_F-HR-OSW_Pack/00_OVERVIEW.md` | `450acf8e` |
| `03_FRD/FRD_F-HR-OSW_Pack/01_UI.md` | `02d48c1c` |
| `03_FRD/FRD_F-HR-OSW_Pack/02_API.md` | `30410423` |
| `03_FRD/FRD_F-HR-OSW_Pack/03_LOGIC.md` | `07271def` |
| `03_FRD/FRD_F-HR-OSW_Pack/04_DB.md` | `d05afd49` |
| `03_FRD/FRD_F-HR-OSW_Pack/05_RULES.md` | `663d63be` |
| `03_FRD/FRD_F-HR-OSW_Pack/06_TESTS.md` | `264d5c20` |
| `03_FRD/FRD_F-HR-OSW_Pack/07_LOCKED_DECISIONS.md` | `8193c3e8` |
| `03_FRD/FRD_F-HR-OSW_Pack/INDEX.md` | `adc2ea6b` |
| `04_UI_Brief/UI_BRIEF_F-HR-OSW.md` | `caba09a3` |
| `05_Governance/DECISIONS_F-HR-OSW_2026-10-05.md` | `36bf812f` |
| `05_Governance/DOA_BRIEF_F-HR-OSW.md` | `289fc5ee` |
| `05_Governance/DOCCFG_BRIEF_F-HR-OSW.md` | `413f994e` |
| `05_Governance/MDOC_BRIEF_OSW.md` | `d7c255d3` |
| `05_Governance/OSW.mdoc.yaml` | `2800a048` |
| `06_Test/QA_AUDIT_F-HR-OSW.md` | `3c8ffc41` |
| `06_Test/testcase-F-HR-OSW.html` | `240182dd` |
| `06_Test/testcases-F-HR-OSW.md` | `351a3009` |
| `07_Print/OSW_print-spec.md` | `8482d122` |
| `07_Print/OSW_sample_approved.pdf` | `cb25df3a` |
| `07_Print/OSW_sample_draft.pdf` | `7d50a8c9` |
| `07_Print/OSW_template.html` | `3d891d74` |
| `07_Print/base_form_patch.css` | `15ae357a` |
| `07_Print/compare_FM-HRM-02_vs_OSW.png` | `0732b4d0` |
| `07_Print/osw_body.tpl.html` | `3f9206f0` |
| `07_Print/render_osw.py` | `5a995d09` |
| `07_Print/sample_approved.data.json` | `3d7ed30f` |
| `07_Print/sample_draft.data.json` | `c34a5ef7` |
| `08_Reference/FM-HRM-02_original_Rev00.pdf` | `23ef25f2` |
| `08_Reference/IMPACT_SUMMARY_REQ-2569-0000.html` | `25535e1a` |
| `08_Reference/PREBRIEF_REQ-2569-0000.md` | `d9e91d47` |
| `08_Reference/PREBRIEF_REQ-2569-0011.md` | `08b45787` |
