# RUN_LOG — F-TMP-008 FM-CCC-04 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม Corrective Action Request (CAR) (REQ-TMP-008)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)


## ขั้น 1 · หมายเหตุ
- ภาพฟอร์ม: to_image.py → LibreOffice → PDF → pypdfium2 (print area A1:AM66 · A4 portrait scale 45% · 2 หน้า — หน้า 2 เป็นเศษขอบคอลัมน์ AM ที่ล้นจาก scale ไม่ใช่เนื้อหาใหม่) · ภาพเห็นตัวไทย อ่านได้ · ถ้อยคำยึด content.html + openpyxl + drawing1.xml (กล่องข้อความ "ตรวจสอบโดย HOD ……… …/…/…" ที่ AJ41) + footer (Doc. No. : FM-CCC-04 · Rev.00 : 01/07/2569)
- form.title = "ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม" (หัวฟอร์ม H1 ส่วนภาษาไทย · ชื่อเต็มพร้อม "Corrective Action Request (CAR)" เก็บใน form.title_full) · ชื่อในคิวไม่เพี้ยน → ไม่ rename
- โครงฟอร์ม: หัว (P-CAR No. · DOC NAME · DOC NO. · หน่วยงาน · ผู้พบปัญหา · วันที่/เวลาที่พบ) · 1 หัวข้อปัญหา · 2 ดัชนี/เป้าหมาย · 3 ตารางอาการ 5 แถว + รวม คู่กับ 6.3 ประสิทธิผล (C) · ผู้เข้าร่วมประชุม 8 · 4 Why-Why (ทำไม 1/2/3 + สาเหตุรากเหง้า) แถบ "การจัดทำ"/"การตรวจสอบ" อย่างละชุด · 5 (D) 5.1/6.1 · 5.2/6.2 · 7 ป้องกัน (A) เฉพาะกรณี/ทั้งระบบ · 8 เอกสารที่ต้องแก้ · 9 ทบทวนความเสี่ยง · 10 ตรวจ 3 Doc · 11 ทบทวน · 12 อนุมัติ
- ลายเซ็น 11: จุดลงนามตรวจสอบ 7 (HOD · IC Mgr · 6.1 MD · 6.1 IC Mgr. · 10 IC Mgr · 11 MD · 11 IC Mgr.) = who=other · ข้อ 12 อนุมัติ 4 ช่อง (GM/AMD/ผู้จัดการฝ่าย · MD · IC · IC Mgr.) = approver
- ค่าคงที่ 1: "ภายใน 30 นาที" → CarConfig.analysis_start_minutes · สูตร 6 (% ต่อแถว + รวม ของข้อ 3 และ 6.3)
- form_spec_check: ERROR 0 · 87 ช่อง · 18 กลุ่มแถวซ้ำ · ฟอร์มเปล่า ไม่มีข้อมูลส่วนบุคคลจริง
- ไม่มี PREBRIEF CMS → PREBRIEF v2 จาก FORM_SPEC (--req REQ-TMP-008 --module Governance) · impact_summary · FEATURE_REGISTRY ไม่มี feature CAR/แก้ไขป้องกัน → feature ใหม่ (เสนอใน _BATCH_REPORT)
- orig/content.html → orig/out/content.html (กันชน artifact prototype · บทเรียน J001/J002)
- 2026-10-10 09:39 · ขั้น 1 → done · FORM_SPEC 87 ช่อง · 18 กลุ่ม · ลายเซ็น 11 · ERROR 0 · PREBRIEF v2

## ขั้น 2 · gate (unattended — AI-DEFAULT 28 มติ + VALID 7)
- G1: ฟอร์มไม่ระบุการเปลี่ยนค่า/ส่งต่อ → config_changes [] · post_to [] · DOC NAME/DOC NO./เอกสารที่ต้องแก้ (8)/3 Doc (10) = ผู้ใช้กรอกเลขอ้างอิงเอง
- G2: ข้อ 12 มีช่องอนุมัติ 4 ช่อง → dynamic 4 ขั้นตามลำดับกระดาษ role-line-manager (GM/AMD/ผู้จัดการฝ่าย) → role-md → role-ic-officer → role-ic-mgr · ไม่มีวงเงิน · role-md / role-ic-officer / role-ic-mgr ไม่มีใน doa-roles-contract → แจ้ง _BATCH_REPORT · จุดลงนามตรวจสอบ 7 จุด (HOD · IC Mgr · MD · IC Mgr.) = สิทธิ์ลงนามตรวจสอบตาม role ไม่ใช่ DOA
- G3: 30 นาที → CarConfig.analysis_start_minutes (เกิน = เตือน) · % คำนวณอัตโนมัติ · Σ > ทั้งหมด = เตือน · พบปัญหาในอนาคต/เกิดใหม่+เกิดซ้ำขัดกัน = บล็อก · ส่งตรวจสอบต้องครบขั้นต่ำ · ส่งอนุมัติต้องลงนามตรวจสอบครบ 7 · SoD
- G4: 16 กลุ่มแถวซ้ำ ไม่จำกัด · PDF ขั้นต่ำเท่ากระดาษ
- G5: 1:1 · แก้ '7.;' → '7.:' · คงป้าย 6.1 ซ้ำ
- G6: ลงนามตามตำแหน่งเดิมบนกระดาษ · ข้อ 12 = 1 ช่องต่อขั้น DOA · ข้อความในระบบ ไม่ใช้ภาพ
- G7: สถานะ ร่าง → รอตรวจสอบ (ผู้ตรวจ IC กรอกช่วง "การตรวจสอบ" + ลงนามตรวจสอบ) → รออนุมัติ (DOA 4 ขั้น) → อนุมัติแล้ว · ไม่อนุมัติ/ส่งกลับแก้ไข → ร่างเลขเดิม (ล้างจุดลงนามตรวจสอบ) · ยกเลิก owner+admin ใน ร่าง/รอตรวจสอบ/รออนุมัติ · เหตุผลบังคับ
- G8: เจ้าของ · ผู้ลงนามตรวจสอบหลังส่งตรวจสอบ · ผู้อนุมัติหลังส่งอนุมัติ · admin role IC (แผนกบริหารองค์กรและกำกับดูแล) เห็นทั้งหมด
- G9: ออกเลขตอนบันทึกครั้งแรก · รหัส CAR จากป้าย "P-CAR No." บนกระดาษ (ไม่ชน registry ACL/ITRS/SRC/DRITS/CRR/ITCR/SRAL · ไม่ชน DAR ของ J007)
- G10: แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- decisions_lock: 35 มติ พร้อมเริ่มทำ (exit 0) · dm.sh tag → AI-DEFAULT 28
- 2026-10-10 09:40 · ขั้น 2 → done · DECISIONS.lock พร้อมเริ่มทำ · 35 มติ · AI-DEFAULT 28 · DOA 4 ขั้น · code CAR

## ขั้น 3 · declaration ร่าง
- doa: init (agent ก่อน) module=policy · doa_type car · 4 ขั้นตามข้อ 12 role-line-manager → role-md → role-ic-officer → role-ic-mgr · on_reject แก้เป็น back_to_draft แล้ว · action submit_car from in_review (ขั้นตรวจสอบ IC อยู่ก่อน DOA) · validate WARN G1 (role-md/role-ic-officer/role-ic-mgr นอก contract) · BLOCK 0 · brief → DOA_BRIEF_F-TMP-008.md
- ntf: car_cancelled (รอตรวจสอบ/รออนุมัติ → ยกเลิก) · car_submitted_for_review (→ role-ic-officer) · car_review_returned (→ owner) · ตัด over_limit (เกณฑ์เป็นคำเตือนตอนกรอก) → PASS
- doccfg + mdoc ทำหลังขั้น 4
- 2026-10-10 12:12 · ขั้น 3 → done · doa WARN (role-md/ic-officer/ic-mgr นอก contract) BLOCK 0 · ntf PASS · doccfg/mdoc หลังขั้น 4

## ขั้น 4 · แบบพิมพ์ Replica (R9 ตารางกรอบ · R10 2 หน้า)
- ต้นฉบับ Excel แนวนอนหนาแน่น 1 หน้า (scale 45% → < 8pt) · 87 ช่อง · 18 กลุ่มแถวซ้ำ (~140 แถวว่าง) · ลงนาม 11 จุด → R10 ออกแบบ A4 แนวตั้ง 2 หน้า (Sarabun 8pt · lh 1.2 · ไม่บีบ < 8pt)
- form.tpl.html สร้างจาก .scratch/make_tpl.py: ตาราง 24 คอลัมน์เท่ากัน (ความกว้างด้วย colspan · ไม่มี style ใน body) · หัวบล็อกอยู่ใน <thead> (ซ้ำเมื่อข้ามหน้า) · .page-break ที่ .doc-page หน้า 2 · "มีต่อหน้าถัดไป" ท้ายหน้า 1 · หัวย่อหน้า 2 (ชื่อเอกสาร + P-CAR No.) · footer ทุกหน้า "หน้า n/2"
- จุดตัดหน้า: หน้า 1 = หัว · 1–3 · ผู้เข้าร่วมประชุม · 4 (การจัดทำ ทำไม1/2 · การตรวจสอบ ทำไม1/2 · การจัดทำ ทำไม3/รากเหง้า) · หน้า 2 = การตรวจสอบ ทำไม3/รากเหง้า · 5/6 · 7 · 8–11 · 12 บล็อกลงชื่อ DOA ทั้งก้อน
- ช่องลงชื่อข้อ 12 = sign_rows (build_signs()[1:] ตัดช่องผู้ขอ — กระดาษไม่มี · 1 ช่อง/ขั้น DOA แถวละ ≤4) · จุดลงนามตรวจสอบ 7 จุดเป็นช่องคงที่ตามตำแหน่งกระดาษ (rv.*) · ไม่ใช้ layout.dense (dense ของสกิลลดฟอนต์ลายเซ็นเป็น 7.2pt)
- profile.json · print_config.json (pages 2 · group_min_rows · review_points · sign_boxes doa_step:* · decision_words · config_reads CarConfig.analysis_start_minutes) · make_data.py → 5 สถานะ (draft · approved · rejected (MD ไม่อนุมัติ) · long-text (เต็มความจุกระดาษ + ข้อความยาว) · approved-doa6steps 6 ช่อง 3+3) · ข้อมูลสมมติทั้งหมด
- parity_check: IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด → print/out/*.html + CAR_template.html (.scratch/render_nobrowser.py)
- [NO-BROWSER] ข้าม render_pdf.py (ภายใน render_states.py) — render body + build_html ทีละสถานะแทน ได้ HTML ไม่มี PDF/PNG/_states_sheet.png
- [NO-BROWSER] ข้าม compare_original.py (ต้องใช้ approved.pdf) · layout เปลี่ยนตั้งใจ (แนวนอน 1 หน้า → แนวตั้ง 2 หน้า) อธิบายใน print-spec §7
- ตรวจเบื้องต้นนอกเครื่องงาน (stage HTML 5 สถานะไป Chromium ใน container ของ agent · ไม่เก็บไฟล์กลับ): 5/5 = 2 หน้า A4 · สูงสุดหน้า 2 สถานะ DOA 6 ขั้น 256/269 มม. · ตัวอักษรเนื้อฟอร์ม ≥ 8pt (ยกเว้น footer/"มีต่อหน้าถัดไป" ขนาดกลางของสกิล) · บล็อกลงชื่อไม่ตัด — ไม่ใช่ผลด่านทางการ ต้องรัน render_states --max-pages 2 บนเครื่องที่มี browser
- ข้อจำกัด → OQ: ข้อความยาวมาก/แถวเกินขั้นต่ำหลายกลุ่มพร้อมกันอาจเกิน 2 หน้า (หัวตารางซ้ำ · แถวไม่ตัด) — ลูกค้ายืนยันว่ารับหน้า 3 "ใบต่อ" ได้ไหม
- doccfg: CAR · module POLICY · ออกเลขตอนบันทึกครั้งแรก · pages 2 · --registry ไม่ชน (ACL ITRS SRC DRITS CRR ITCR SRAL · J007 DAR) → PASS · mdoc: WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้ · function_code F01 ชั่วคราว
- doa validate --print-config: G8/G9 ผ่าน · WARN G1 (role-md/role-ic-officer/role-ic-mgr นอก contract) · BLOCK 0
- 2026-10-10 12:30 · ขั้น 4 → done · 2 หน้า (R10) · parity 5/5 IDENTICAL · [NO-BROWSER] ไม่มี PDF/compare · doccfg PASS · mdoc WARN(G04,G09) · doa BLOCK 0

## ขั้น 5 · HTML Q-form (html-generator v9.4)
- เปิด GOLDEN_SKELETON.html + ui-standard-list-drawer.md U1–U28 เทียบก่อน build · ฐานโครง/BASE-KIT = canonical references/form-archetype (ผ่าน .build/build_feature.py เดียวกับ J005) · helper กลางของ Q-form (pager · modal shell · drawer · ไฟล์แนบ · commitRejected) ยกจาก app ของ J005 ด้วย .build/patch_app.py (//@keep) · ส่วน domain CAR เขียนใหม่ใน .build/p_*.js · โลโก้ตัวอย่างจาก xl/media ของต้นฉบับ (ระบบจริงอ่าน Organization)
- ช่องตามกระดาษ 1:1 (#106): ช่วง "การจัดทำ" (ผู้จัดทำ · wizard 3 ขั้น ข้อมูลหลักรายงาน › เอกสารแนบ › ตรวจสอบและยืนยัน) = หัว (DOC NAME/DOC NO./ผู้พบปัญหา/วันที่-เวลาที่พบ) · 1 · 2 · 3 (+6.3) ตารางคำนวณ % สด · ผู้เข้าร่วมประชุม · 4 ทำไม 1/2/3/รากเหง้า · 5.1/6.1 · 5.2/6.2 · 7 · 8 · 9 · ช่วง "การตรวจสอบ" + ข้อ 10 = drawer "บันทึกการตรวจสอบ" ของ IC (DEC-31) · หน่วยงาน = ระบบใส่ · 30 นาที = CAR_CONFIG (CarConfig)
- แถวซ้ำ ≤4 ช่อง = การ์ดต่อแถว (#107) · ตาราง 3 (8 ช่อง) = ตาราง (#104) · วันที่ทุกช่อง bedateHTML (#114) · ไม่จำกัดแถว (DEC-05…22)
- flow: ร่าง → ส่งตรวจสอบ (เลือกผู้ตรวจสอบ IC + slot DOA ต่อขั้น · freeze ตอนส่ง) → รอตรวจสอบ (IC บันทึกการตรวจสอบ · ลงนามตรวจสอบ 7 จุดตาม role: HOD=role-line-manager · IC Mgr=role-ic-mgr · MD=role-md · SoD ผู้จัดทำลงนามไม่ได้) → ส่งอนุมัติ (บล็อกถ้าลงนามไม่ครบ 7) → รออนุมัติ DOA 4 ขั้นเรียงลำดับ → อนุมัติแล้ว · ไม่อนุมัติ/ตีกลับ = ร่างเลขเดิม + ล้างจุดลงนามตรวจสอบ · ยกเลิก owner+admin (ร่าง/รอตรวจสอบ/รออนุมัติ) เหตุผลบังคับ
- กฎ DEC-04: พบปัญหาในอนาคต = บล็อก · เกิดใหม่↔เกิดซ้ำครั้งที่ = บล็อก · ขั้นต่ำก่อนส่งตรวจสอบ = บล็อก (แสดงรายการที่ขาด) · Σ > จำนวนทั้งหมด · ทำไมระดับถัดไปไม่มีผล "จริง" · กำหนดเสร็จก่อนวันที่พบ · บันทึกครั้งแรกช้ากว่า 30 นาที = เตือน
- audit.sh: FAIL 0 · WARN 3 (จาก BASE-KIT กลาง: comment lucide · .uc-email · font-size px ใน shell — เหมือน J005) → reports/audit.txt · prune_css ตัด 77 rule → audit ซ้ำ FAIL 0 · มี meta cube-archetype + window.__QA__ + DOA-ENGINE-HOOK
- [NO-BROWSER] ข้าม e2e_standard.py · ข้าม render-check.py บนเครื่องงาน
- ตรวจเบื้องต้นนอกเครื่องงาน (stage feature.html ไป Chromium ใน container ของ agent · lucide stub · ไม่เก็บไฟล์กลับ): e2e_standard 21/21 ก่อนและหลัง prune · flow test 26/26 (ส่งตรวจสอบ · IC บันทึกการตรวจสอบ · ลงนาม 7 จุดโดย HOD/IC Mgr/MD · ส่งอนุมัติบล็อกเมื่อลงนามไม่ครบ · อนุมัติ 4 ขั้น · ไม่อนุมัติกลับร่างเลขเดิม + ล้างลงนาม · IC ตีกลับ · admin ยกเลิก · พบปัญหาในอนาคตบล็อก · เกิดใหม่/เกิดซ้ำบล็อก · % สด + เตือนรวมเกิน · ออกเลข CAR ตอนบันทึกร่าง) · ไม่มี pageerror — ไม่ใช่ผลด่านทางการ
- parity แบบพิมพ์ใน prototype: printData จาก JS (6 ใบ ทุกสถานะ) → render_doc.py IDENTICAL 6/6 · key ของ printData = key ของ make_data.py (ไม่มีส่วนต่าง)
- U1–U28: U1✓ (ไม่มี stat cards · badge ใน sub ≤3) U2✓ U3✓ U4✓ U5✓ kebab ⋮ U6✓ U7✓ CSV ที่ head U8✓ 920/1290 U9✓ เหตุผลบังคับ U10✓ U11✓(kit) U12✓ U13✓ summary+timeline+emp-chip (จุดลงนามตรวจสอบ + ข้อ 12) U14✓ wizard 3 ขั้น U15✓ แก้ไข = wizard เดิม เฉพาะร่าง U16 – (ไม่มีลบ: ยกเลิก = soft + เหตุผล) U17✓ U18✓ U19✓ header sub 1 fact (วันที่พบปัญหา) U20✓ seg tabs ทั้งหมด/รอฉันดำเนินการ/รายงานของฉัน U21✓(kit) U22✓ U23✓ ตารางย่อยว่างมี empty panel U24✓ search-select portal U25✓ backdrop onmousedown U26–U28 – (ไม่มีหน้าตั้งค่า — CarConfig ตั้งที่ config กลาง)
- 2026-10-10 12:48 · ขั้น 5 → done · audit FAIL 0 · U1–U28 ✓ · [NO-BROWSER] e2e/render-check ข้าม (pre-check นอกเครื่อง e2e 21/21 · flow 26/26 · print parity 6/6)
- 2026-10-10 12:48 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 6 — ข้าม (unattended)
- ให้คนดูจาก _BATCH_REPORT · [NO-BROWSER] ยังไม่มี _states_sheet.png / screenshot หน้าจอหลัก (ต้อง render บนเครื่องที่มี browser)

## ขั้น 7 · BRD → FRD → declaration ฉบับจริง
- BRD_F-TMP-008.md/.docx (brd-generator-full v2.3 Prebrief Mode · Lane · md_to_docx.py) — §2.4 Scope Lock = DEC ครบ 35 ข้อตรงตัว · AI Review C01–C23 + PE01–PE05 → **APPROVED** (C16 ไม่มีรหัสใน registry = ยอมรับใน Prebrief Mode · ตัวชี้วัดไม่มีใน input → OQ-01)
- FRD_F-TMP-008_Pack (frd-generator-v6.2 Input Mode 0 · FULL variant: states=5 + approval) 00–07 + INDEX + declarations/ · 07 §7.0 = แถว DEC จาก DECISIONS.lock.md ตรงตัว (35)
- FRD บรรยายสาย DOA ตรงมติ DEC-03/DEC-32 (4 ขั้น role-line-manager → role-md → role-ic-officer → role-ic-mgr · resolve+freeze ตอนส่งตรวจสอบ · เริ่มพิจารณาเมื่อ IC ส่งอนุมัติจาก in_review ตรงกับ doa action from_state) · ไม่อนุมัติ/ตีกลับ → draft เลขเดิม + ล้างจุดลงนาม (DEC-25) · จุดลงนามตรวจสอบ 7 จุดแยกจาก DOA (บทเรียน K2/K7)
- frd_lint Section N: BLOCK 0 · WARN 1 (N3 false positive — เลข "30" ตรงกับข้อความ "DEC-30" ใน BR-08/EC-04 ไม่ใช่ค่าคงที่ 30 นาที · ค่าจริงอ่านจาก CarConfig.analysis_start_minutes) · PASS 13 → reports/_SECTION_N.md
- declaration --final: doccfg PASS (--registry · CAR ไม่ชน · frd_ref FN-02/FN-09) · ntf PASS (frd_ref FN-04/07/11 + FN-13) · doa WARN (role-md/role-ic-officer/role-ic-mgr นอก contract · --print-config) BLOCK 0 · mdoc WARN G04 (ไม่มี taxonomy_def_id) + G09 (doa pending) — อธิบายได้ → คัดลง FRD_F-TMP-008_Pack/declarations/
- OQ ใหม่: OQ-04 เชื่อมทะเบียนเอกสาร · OQ-05 เกิน 2 หน้า · OQ-06 ผู้กรอก 6.3
- 2026-10-10 12:54 · ขั้น 7 → done · BRD APPROVED · frd_lint BLOCK 0 (WARN N3 false positive) · declaration final BLOCK 0 (doa WARN role นอก contract · mdoc WARN G04/G09)

## ขั้น 8 · UI Brief → test case AI → UAT
- extract_anchors → reports/inventory.json (routes 7 · toast 19 · ปุ่ม 26) · UI_BRIEF_F-TMP-008.md (§0–§13 · CSS vars/z-index/microcopy สกัดจาก inventory ด้วย .build/gen_ui_brief.py) → brief_check: PASS · FAIL 0 · WARN 0 → reports/ui_brief_check.md
- testcases-F-TMP-008.md: 60 เคส / 196 step (L9 C5 V6 Q4 F2 D3 I2 G3 A6 K4 P6 X3 E4 T3) · tc_lint ERROR 0 · Coverage Ledger + Audit (S 15/15 · VR 8/8 · DEC 35/35 · XT 4/4 · ข้าม BR-13/EC-01/EC-06 พร้อมเหตุผล)
- [NO-BROWSER] ข้าม verify_anchors.py บนเครื่องงาน · ตรวจเบื้องต้นนอกเครื่องงาน (Chromium ใน container ของ agent · lucide stub): DOM 297 · SOURCE 89 · PATTERN 16 · DATA 45 · MISSING 0 (รอบแรก MISSING 2 = ข้อความที่ประกอบจากหลาย element → แก้ anchor แล้ว) — ไม่ใช่ผลด่านทางการ
- UAT (qa-friendly v3.1 Lite): cases.json 54 เคส · drop ledger 6 (คำสั่งหลังบ้าน/จำลอง/พิมพ์ที่อยู่ตรง) · lite_audit หายเงียบ 0 + stamp md5 · build testcase-F-TMP-008.html
- [NO-BROWSER] ข้าม capture.py → ไม่มีภาพหน้าจอ (regionKey ว่างทุก step · shots_b64.json = {})
- 2026-10-10 13:01 · ขั้น 8 → done · brief_check FAIL 0 · tc_lint ERROR 0 (60 เคส) · lite_audit หายเงียบ 0 · [NO-BROWSER] verify_anchors/capture ข้าม (pre-check anchors MISSING 0)
