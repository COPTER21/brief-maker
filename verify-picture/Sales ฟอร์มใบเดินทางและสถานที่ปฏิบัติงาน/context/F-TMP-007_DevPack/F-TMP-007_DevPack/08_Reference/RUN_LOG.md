# RUN_LOG — F-TMP-007 ฟอร์มใบเดินทางและสถานที่ปฏิบัติงาน (REQ-TMP-007)
> บันทึกอัตโนมัติจาก `doc_master.py mark` + หมายเหตุที่ต้องจำ (มติที่เปลี่ยน · ข้อยกเว้น · เหตุผลของ WARN)

## ขั้น 1 — อ่านฟอร์ม + PREBRIEF v2
- ต้นฉบับ `.xlsx` 1 ชีท (Sheet1) · A4 แนวนอน · มีเพียงชีทเดียว ตรวจครบแล้ว
- แปลงภาพด้วย `_system/tools/to_image.py` (LibreOffice → PDF → pypdfium2) ได้ `SAMPLE.pdf` + `page-1.png` + `content.html`
  - ภาพแสดงอักษรไทยเป็นกล่อง (ฟอนต์ไทยไม่ครบใน LibreOffice) → **ถ้อยคำยึด content.html + การอ่านเซลล์ด้วย openpyxl** · ภาพใช้ดูโครงตาราง/ตำแหน่งเท่านั้น
- ชื่อจากหัวฟอร์ม (A2) = "ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade" → `dm.sh rename J007` แล้ว
- Doc No. อยู่ใน footer ของชีท: `Doc.No.FM-SAL-13 / Rev.00: 01/07/2569`
- ตาราง 21 คอลัมน์ · แถวรายการ 27 แถว (row 9–35) · แถวรวมยอด row 36 · บล็อกสรุป row 37–40 · ลายเซ็น 2 ช่อง (row 39–40) · เอกสารแนบ 3 บรรทัด
- `form_spec_check`: 45 ช่อง (ระบบ 2 · กรอก 27 · คำนวณ 14 · auto 2) · แถวซ้ำ 2 กลุ่ม · สูตร 14 · ลายเซ็น 2 · anomalies 5 · **ERROR 0**
- [บั๊กเครื่องมือ 1] `impact_summary.py` regex ไม่รับ `REQ-TMP-007` → รันบนสำเนาที่แทนเป็น `REQ-2569-0007` แล้วแทนกลับ + rename ไฟล์
- [บั๊กเครื่องมือ 2] ป้องกัน K2: `orig/content.html` → `orig/content.src.txt` ตั้งแต่จบขั้น 1
- 2026-10-07 15:34 · ขั้น 1 → done

## ขั้น 2 — gate 10 หมวด (unattended)
- ตอบเองตาม `4_knowledge/governance/unattended-policy.md` ทุกหมวด · บรรทัดแรกของ decisions.yaml ระบุ AI-DEFAULT
- G1: ใบนี้เป็นบันทึกเดินทาง + ขอเบิกค่าใช้จ่าย ไม่เปลี่ยน config ไม่ post ต่อ (การตั้งหนี้/จ่ายเงินอยู่นอกใบนี้ รอลูกค้ายืนยัน)
- G2: กระดาษมีช่องลงชื่อ 2 ช่อง (ซ้าย=ผู้จัดทำ ขวา=ผู้อนุมัติ) → DOA dynamic ค่าเริ่ม 1 ขั้น `role-line-manager`
- G3: ไม่มีค่าคงที่พิมพ์บนกระดาษ · แก้สูตรที่ผิด/ขาดในต้นฉบับ 3 จุด (รวมคอลัมน์ค่าที่พัก · รวมรายแถว · บวกค่าโทรศัพท์)
- G4: 27 แถว (วันทำงาน) + 3 แถว (เอกสารแนบ) ไม่จำกัดจำนวน
- G5 1:1 · G6 แถวล่างต่อขั้น DOA · G7 กลับร่าง · G8 เจ้าของ/ผู้อนุมัติหลังส่ง/admin · G9 first_save รหัส TWP · G10 แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗
- [บั๊กเครื่องมือ 7] `decisions_lock.py` ออก DEC-05/DEC-06 (G4) ให้ทุกกลุ่มซ้ำโดยอัตโนมัติ — ปล่อยตามปกติ
- ผล: 17 มติ · AI-DEFAULT 12 · สถานะ "พร้อมเริ่มทำ"
- 2026-10-07 15:35 · ขั้น 2 → done

## ขั้น 3 — ร่าง declaration (doa · ntf)
- `doa_tool.py init` → `TWP.doa.yaml` · 1 set · 1 ขั้น · dynamic · on_reject back_to_draft
- [บั๊กเครื่องมือ 8] init เขียน `platform: core` เสมอ → แก้มือเป็น `cube_core` ตาม Module Registry (sales → cube_core)
- ป้ายขั้น DOA: init ดึงจาก `signatures[].role_on_paper` ได้ "ช่องลงชื่อขวา (ไม่มีคำกำกับบนกระดาษ)" → แก้เป็น "ผู้อนุมัติ" (กระดาษไม่มีคำกำกับ บันทึกเป็น anomaly แล้ว)
- `doa_tool.py brief` → **PASS** (BLOCK 0)
- `ntf_tool.py suggest` ได้ 2 event · ตัด `twp_over_limit_approved` (review: true) เพราะกฎ G3 ของใบนี้เป็นคำเตือนบนหน้าจอ ไม่มี role ผู้รับที่ยืนยันได้
- `ntf_tool.py brief` → **PASS** (BLOCK 0) · เหลือ 1 event `twp_cancelled`
- doccfg + mdoc ทำที่ขั้น 4 (ต้องใช้ print_config)
- 2026-10-07 15:36 · ขั้น 3 → done

## ขั้น 4 — แบบพิมพ์ Replica
- บล็อก R9 ตารางกรอบ 21 คอลัมน์ (กระดาษเป็นตารางเส้นทึบ) · หัวตาราง 2 ชั้น · 27 แถวขั้นต่ำ
- `print/` : form.tpl.html · profile.json · print_config.json · make_data.py · data 5 สถานะ (draft · approved · rejected · long-34rows · approved-doa6steps)
- `parity_check.py` → **IDENTICAL 5/5** (ไม่มีคำเตือน)
- `render_doc.py` ทุกสถานะ → ไม่มี `{{}}` หลง · `build_html.py` → `TWP_template.html` + `out/<state>.html` (ฝังฟอนต์ mode=replica)
- [NO-BROWSER] ข้าม `render_states.py` (จึงไม่มี `_states_sheet.png` และยังไม่ยืนยันจำนวนหน้า)
- [NO-BROWSER] ข้าม `compare_original.py` (ไม่มี `compare_side.png`)
- [บั๊กเครื่องมือ 11] `base.css` ล็อก `@page size:A4 portrait` → ต้นฉบับแนวนอนทำเป็นแนวตั้ง + ย่อ token ใน profile · บันทึกความต่างใน `print/TWP_print-spec.md` §7 ข้อ 1
- `doccfg_tool.py init/brief --registry` → **PASS** (รหัส TWP ไม่ชนกับ ACL · MEM · VAN · TRV · DSR · CMP · LOA)
- `mdoc_tool.py validate/brief` → WARN (G04 taxonomy_def_id ยังไม่มี · G09 doa pending) — เป็น WARN ปกติของ feature ใหม่ ไม่บล็อก
- `doa_tool.py validate --print-config` → **PASS** (INFO: role-line-manager เป็น relative role ต้องยืนยันกับ DOA กลาง)
- 2026-10-07 15:43 · ขั้น 4 → done

## ขั้น 5 — HTML Q-form + gate
- ประกอบ `feature.html` (235 KB) จาก archetype canonical `html-generator-v9/references/form-archetype/_SOURCE_form-request-reference.html` ด้วย `_build/assemble_twp.py`
  - prefix (base-kit + CSS + body) จาก archetype · domain JS = `_build/twp_domain.js` · `TWP_TPL` = `print/form.tpl.html` (ไฟล์เดียวกับฝั่ง server)
  - [บั๊กเครื่องมือ 3] ใช้ `bedateHTML()` แทน `<input type="date">` (Rule #114) — สมอกตรวจซ้ำแล้วไม่มี `type="date"` ในไฟล์
  - [บั๊กเครื่องมือ 4] คัด domain JS โดยตัด 3 บรรทัด marker `PDF_CSS` ของ archetype ออก (assemble ฉีดใหม่) → ไม่เกิด `Identifier 'PDF_CSS' has already been declared`
- `audit.sh` → **FAIL 0 · WARN 4** (WARN ทั้งหมดตกทอดจาก base-kit ของ archetype: Rule #21 ไอคอนใน base-kit · Rule #40 `.uc-email` · token font-size · Rule #100F ขั้น "เอกสารแนบ" ซึ่ง DEC-12 ให้เก็บไว้)
- [NO-BROWSER] ข้าม `e2e_standard.py` · `prune_css.py` (ต้องรัน e2e ซ้ำหลัง prune) · `render-check.py`
  - แทนด้วย `reports/nodom_smoke.js` (node + vm + stub DOM) → `reports/nodom_smoke_report.txt` = **ALL CHECKS OK**
  - ครอบคลุม: docPrintData + tplRender ครบ 11 record ไม่มี `{{}}`/`undefined` · แบบพิมพ์เติมแถวครบ 27 · DOA 6 ขั้น → 7 ช่อง 2 แถว (4+3) · กฎการมองเห็น DEC-10 ไม่รั่ว · DEC-09 ส่งกลับ = ร่างเลขเดิม · DEC-12 ไม่มีปุ่มทำซ้ำ · Rule #114 · ยอดรวมทุกแถว · รวมรายแถว/รวมทั้งสิ้น/คงเหลือ · เอกสารที่แนบ 3 บรรทัด
- มี `<meta cube-archetype>` และ `window.__QA__` ครบ
- 2026-10-07 15:59 · ขั้น 5 → done
- 2026-10-07 15:59 · ขั้น 6 → skip · unattended — ให้คนดูจาก _BATCH_REPORT

## ขั้น 7 — BRD → FRD → declaration ฉบับจริง
- `BRD_F-TMP-007.md` 19 หัวข้อ (รวม §3.4 Scope Lock ชั่วคราวผูก DEC ทุกข้อ · §14 ใบสั่ง 10 ข้อ · §15 Open Questions Q1–Q10 · §19 AI Review) → **APPROVED (มีเงื่อนไข)**
- `FRD_F-TMP-007_Pack/` 8 ไฟล์ (00…07) · FN-01…FN-14 · BR-TWP-01…12 · VR-01…10 · T-01…T-74
- `frd_lint.py` → **Section N: BLOCK 0 · WARN 0 · PASS 11** (N1 DEC ครบ 17 · N2 ช่องครบ · N4 deny 9 จุด + เคสร่างคนอื่น · N5 header_snapshot + FN-06 · N6 approval_chain/doa_ref · N7 event ถูกอ้าง · N8)
  - [บั๊กเครื่องมือ 6] ระวังไม่เขียน microcopy สองคำติดกันด้วย `/` ใน 06_TESTS และไม่อ้างฟังก์ชันที่ตัดออก — รอบนี้ไม่พบปัญหา
  - [บั๊กเครื่องมือ 9] N3 ไม่ทำงานเพราะฟอร์มนี้ไม่มี `constants` บนกระดาษ → ไม่มี false positive
  - [บั๊กเครื่องมือ 10] K6/N1 "อ้างมติไม่ครบ" ป้องกันไว้แล้วด้วยตารางผูกมติใน BRD §3.4
- ใส่ frd_ref ตามที่ lint พิมพ์: doccfg `numbering` = `03_LOGIC FN-06` · `snapshot_points` = `03_LOGIC FN-13` · ntf `twp_cancelled` = `03_LOGIC FN-11`
- `doccfg_tool.py brief --final --registry` → **PASS** · `ntf_tool.py brief --final` → **PASS**
- 2026-10-07 16:12 · ขั้น 7 → done

## ขั้น 8 — UI Brief → test case AI → UAT
- `extract_anchors.py` → `reports/inventory.json` (css var 47 · z-index 22 · route 5 · toast 10 · ปุ่ม 21 · microcopy 257 · function 197 · marker 7)
- `UI_BRIEF_F-TMP-007.md` (AS-BUILT · §0–§13) → `brief_check.py` = **PASS · FAIL 0 · WARN 0** (B1–B8 ผ่านครบ · CSS var 47/47 · microcopy 60/60)
- `testcases-F-TMP-007.md` 38 เคส · 175 step (CRT 14 · DOA 10 · PERM 4 · PDF 6 · LIST 4) → `tc_lint.py` **ERROR 0**
- [NO-BROWSER] `verify_anchors.py` รันได้แบบ source อย่างเดียว (ไม่มี browser จึงไม่ไล่ DOM) → **MISSING 0** · DOM 0 · SOURCE 38
- `cases.json` (เอกสารแบบทดสอบสำหรับคน) 38 เคส · `QA_AUDIT_F-TMP-007.md` → `lite_audit.py --stamp` = **หายเงียบ 0** · drop ledger 0
- [NO-BROWSER] ข้าม `capture.py` (ภาพหน้าจอ) และ build UAT HTML — บันทึกไว้ใน QA_AUDIT §สิ่งที่ยังทำไม่ได้
- 2026-10-07 16:21 · ขั้น 8 → done

## ขั้น 9 — ตรวจรวม + แพ็ก DevPack
- `manifest_scan.py` → 40 artifact · ซ้ำ 0 (บั๊กเครื่องมือ 2 ป้องกันสำเร็จ: `orig/content.src.txt` ไม่ชนกับ `feature.html`)
- `consistency_check.py` รอบแรก: READY · BLOCK 0 · WARN 2 → แก้ 2 จุดแล้วรันซ้ำ
  1. K4 microcopy "รวมค่าใช้จ่ายที่เบิก" ไม่พบ เพราะหัวตารางใน prototype ตัดบรรทัดด้วย `<br>` → รวมเป็นบรรทัดเดียวในหน้าจอ (แบบพิมพ์ยังคงหัว 2 ชั้นตามกระดาษ)
  2. K4 microcopy "คงเหลือติดลบ — ต้องคืนเงินให้บริษัท" ใน FRD 06 T-11 ไม่ตรงข้อความจริงบนจอ → แก้ข้อความใน FRD ให้ตรงกับที่ prototype แสดง
- รันซ้ำ: **READY · BLOCK 0 · WARN 1 · PASS 10** — WARN เดียวคือ `ไม่มี report e2e_standard` ซึ่งเป็นผลของโหมด NO-BROWSER
- 2026-10-07 16:22 · ขั้น 9 → done
