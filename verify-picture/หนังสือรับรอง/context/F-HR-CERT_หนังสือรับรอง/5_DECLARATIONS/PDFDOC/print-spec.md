# PRINT SPEC — หนังสือรับรอง (Employment / Salary Certificate)

> ออกโดย `thai-doc-pdf-generator` · **Lane Mode** · S1.8 · 2026-08-30 · `F-HR-CERT`
> Input: `briefs/W3/F-HR-CERT/PREBRIEF.md` §3.1 (header) · §3.2 (ก้อนข้อเท็จจริงที่ตรึง) · §6 (view tab PDF) · §13 (`[STD]` patch) + `5_DECLARATIONS/DOCCFG_BRIEF.md` (doc_type `CERT` · เลขรัน `CERT-YYYY-NNNN`) + `DOA_BRIEF.md` §3 (ผู้ลงนาม)
> **เอกสารนี้เป็นของแนบ FRD** — `html-generator-v9` ใช้ `template.html` / `template_en.html` ไฟล์เดียวกันใน **view tab "PDF"** (Pattern Q · `.a4`)

## 1. สรุป

| | |
|---|---|
| ชื่อเอกสาร | **หนังสือรับรอง** · Certificate of Employment / Salary Certificate |
| doc_type | **`CERT`** · เลขรัน **`CERT-YYYY-NNNN`** (`ENG-DOC-NUM.next('CERT', company_ctx)` — **ห้าม format เอง**) |
| ขนาด | **A4 แนวตั้ง** · **1 หน้า** (`595.276 × 841.89 pts` — ยืนยันด้วย `pdfinfo` ทั้งสองไฟล์) |
| ฟอนต์ | **Sarabun ฝัง base64 ในไฟล์** (self-contained · เปิด/พิมพ์ได้ทุกเครื่อง · ใช้ชุดเดียวทั้งไทยและอังกฤษ) |
| CI | CUBE NATIVE ผ่าน `assets/base.css` — **ห้ามเขียน hex สีใน body · ห้ามแก้ base.css รายเอกสาร** |
| โครง body | `HEADER → META → PARTIES(2) → LETTER(ข้อความรับรอง) → NOTES` + `.doc-bottom`: `SIGNS(2 ช่อง) → FOOTER` |
| ⭐ **Renderer** | **เครื่องนี้ติดตั้ง Chromium ไม่ได้ (CDN ถูกบล็อกโดย egress allowlist)** → **render ด้วย WeasyPrint 69.0 แทน `scripts/render_pdf.py`** — เหมือนที่ `F-HR-LEAVE` · `F-HR-OT` · `F-HR-MOVE` ทำในเวฟก่อน · ผลลัพธ์ผ่าน **A4 1 หน้าทั้งสองภาษา** ตรวจด้วยสายตาแล้ว (ภาพที่ `briefs/W3/F-HR-CERT/_lane/QC/shots/`) |
| ช่องลายเซ็น | ⭐ **2 ช่อง: (1) ผู้มีอำนาจลงนาม (2) ที่ว่างสำหรับตราบริษัท** — **ไม่ใช่ e-signature** (`OQ-STD-CT1` · PREBRIEF FN-54 · FN-55) |
| ⭐ ชั้นความลับ | **ย่อหน้าอัตราค่าจ้างเป็น RESTRICTED** → เอกสารมี **4 rendition** (§5) |
| ไฟล์ที่ส่งมอบ | `template.html` (ไทย) · `template_en.html` (อังกฤษ) · `sample.pdf` (ไทย + ค่าจ้าง) · `sample_en.pdf` (อังกฤษ ไม่มีค่าจ้าง) · `print-spec.md` (ไฟล์นี้) |

## 2. ⭐ Rendition Matrix — 4 หน้าตาที่เป็นไปได้ (ข้อสำคัญที่สุดของเอกสารใบนี้)

| rendition | ภาษา | มีตัวเลขค่าจ้าง? | template ที่ใช้ | ย่อหน้า `[data-rendition="salary"]` | ตัวอย่างที่แนบมา | เกิดเมื่อ |
|---|---|---|---|---|---|---|
| **R1 `salary_th`** | ไทย | ✅ มี | `template.html` | **คงไว้** | ⭐ **`sample.pdf`** | `cert_type = salary` · `language = th` · ผู้ออก**มีสิทธิ์** RESTRICTED |
| **R2 `employment_th`** | ไทย | ❌ ไม่มี | `template.html` | **ตัดทั้งย่อหน้า** | (ตัดย่อหน้าออกจาก R1) | `cert_type = employment` / `service_letter` · `language = th` |
| **R3 `salary_en`** | อังกฤษ | ✅ มี | `template_en.html` | **คงไว้** | (คงย่อหน้าใน `template_en.html`) | `cert_type = salary` · `language = en` · ผู้ออก**มีสิทธิ์** RESTRICTED |
| **R4 `employment_en`** | อังกฤษ | ❌ ไม่มี | `template_en.html` | **ตัดทั้งย่อหน้า** | ⭐ **`sample_en.pdf`** | `cert_type = employment` / `service_letter` · `language = en` |

**กติกาการเลือก rendition (ตายตัว ไม่ใช่ดุลพินิจ):**
```
language  = cert_type.language            → เลือกไฟล์ template   (th → template.html · en → template_en.html)
has_salary_figure = (cert_type == salary) → เลือกว่าคงหรือตัดย่อหน้า [data-rendition="salary"]
```

⭐ **สามข้อห้ามที่ผิดแล้วเอกสารเสียหายทันที:**
1. **ห้ามพิมพ์ย่อหน้าค่าจ้างแบบเว้นว่าง / ขีด / ศูนย์ / `••••`** — เมื่อ `masked = true` ระบบต้อง **ปฏิเสธการออกหนังสือ** ไม่ใช่ออกให้แบบไม่มีตัวเลข (PREBRIEF **BR-10** · FN-39 · FN-40 · `SS-5`) · **ไม่มี rendition "มีหัวข้อค่าจ้างแต่ไม่มีตัวเลข"**
2. **ห้ามสลับภาษาโดยการแทนคำในไฟล์เดียว** — ภาษาเป็น **มิติของ template** (ตามแบบ locale variant ของ SAP SF) เพราะโครงประโยครับรองต่างกันทั้งย่อหน้า ไม่ใช่แค่คำศัพท์
3. **ห้ามพิมพ์ตัวเลขค่าจ้างลงในย่อหน้าอื่นหรือใน footer** — ตัวเลขปรากฏได้ที่เดียวคือย่อหน้า `[data-rendition="salary"]` เพื่อให้การตัดย่อหน้าเดียวทำให้เอกสารปลอดตัวเลขทั้งฉบับ

## 3. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | field ต้นทาง (PREBRIEF §3.1/§3.2) | หมายเหตุ |
|---|---|---|
| หัวกระดาษ: ชื่อ/ที่อยู่/โทร/เลขผู้เสียภาษี | **placeholder 2BSimple มาตรฐาน** | ⚠️ **แทนด้วยข้อมูลบริษัทจริงตอน bind** (§6) |
| `เลขที่` / `Ref.` | `cert_doc_no` | **ออกที่ `T-02` (กดส่ง) · immutable · ไม่ reuse** (BR-01) |
| `ลงวันที่` / `Date` | **`issue_date`** | ⭐ **ค่าที่สำคัญที่สุด — เป็นวันที่ที่ใช้ `resolve` ทุกต้นทาง** (BR-09) · ไทยใช้ พ.ศ. · อังกฤษใช้ ค.ศ. |
| `ออก ณ` / `Issued at` | `issue_place` | **[STD] G-03** — มาจากสาขา/สำนักงานที่ออก (Organization) **ไม่ใช่ช่องพิมพ์อิสระ** |
| `รหัสตรวจ` / `Verify` | `verification_code` | ใช้ค้นย้อนกลับในทะเบียน (S-36 · FN-48) · **ไม่ใช่เลขรันของ DOCCFG** |
| `ต้นฉบับ` / `ORIGINAL` | คงที่ | ทุกชุดที่พิมพ์ตาม `copies` ใช้ข้อความเดียวกันและ**เลขเดียวกัน** (FN-56) |
| กล่อง `ผู้ได้รับการรับรอง` | `employee_name_snapshot` / `employee_name_en_snapshot` · รหัสพนักงาน · ตำแหน่ง · หน่วยงาน · สาขา · ประเภทการจ้าง | ⭐ ตำแหน่ง/หน่วยงานมาจาก **`movement/assignment/resolve(as_of = issue_date)`** — **ห้ามใช้ `scheduled[]`** (**BR-14** · `MV-2` · FN-38) · ภาษาอังกฤษต้องมี `employee_name_en_snapshot` ไม่งั้น **บล็อก** (FN-10) |
| กล่อง `เรียน / ออกให้เพื่อยื่นต่อ` | `recipient_name` · `purpose_code` + `purpose_note` · `requested_by` / `on_behalf` | ระบุชัดว่ายื่นด้วยตนเองหรือ HR ยื่นแทน |
| ย่อหน้า 1 (สถานะการเป็นพนักงาน) | `employment_state` + ตำแหน่ง + ประเภทการจ้าง | ⭐ **ข้อความเปลี่ยนตาม `employment_state`** (§4) — **BR-16 · BR-17 · `OB-4`** |
| ย่อหน้า 2 (ระยะเวลา) | `start_date` · `last_working_day` · อายุงาน (computed) | ⭐ `start_date` มาจาก **`onboard/employment-window/resolve`** — **ไม่มีค่า = บล็อก ห้ามพิมพ์เอง** (**BR-18** · FN-42) |
| ⭐ ย่อหน้า 3 (ค่าจ้าง) | `base_amount` + `currency` + จำนวนเงินตัวอักษร | ⭐ **RESTRICTED** — จาก **`salary-structure/resolve(date = issue_date)`** · `masked`/`null` = **ปฏิเสธการออก** (§2 · **BR-10 · BR-12**) · ตัวอักษรจาก `scripts/baht_text.py` (ไทย) · **ปิดบังพร้อมตัวเลขเสมอ** (BR-11 · FN-52) |
| ย่อหน้า 4 (ขอบเขตการรับรอง) | ข้อความคงที่ | **ข้อความบังคับ ห้ามตัด** — เป็นสิ่งที่ทำให้ "ณ วันที่ออก" มีผลทางเอกสาร |
| `ออกให้ ณ วันที่` / `Issued on` | `issue_date` | ซ้ำกับ META โดยตั้งใจ (แบบหนังสือรับรองไทย) |
| `หมายเหตุ` ข้อ 1–3 | ข้อความคงที่ + `issuer_contact` | ⭐ **ข้อ 1 (ขอบเขต ณ วันที่ออก) และข้อ 2 (ช่องทางตรวจสอบ) เป็นข้อความบังคับ ห้ามตัด** · ข้อ 2 ใช้ `issuer_contact` **[STD] G-04** |
| ช่องลงนาม 1 | **`approved_by`** จาก `approval_chain` ขั้นสุดท้าย + ตำแหน่ง | ⭐ **ชื่อผู้ลงนาม = ผู้อนุมัติขั้นสุดท้ายที่เซ็นจริง ไม่ใช่ค่าคงที่** (`DOA_BRIEF §4`) |
| ช่องลงนาม 2 | — | **ที่ว่างสำหรับประทับตราบริษัท** · **ห้ามมีภาพตราจริง ห้ามมีลายเซ็นสแกน** (`OQ-STD-CT1` · FN-55) |
| footer | ข้อความระบบ + `cert_doc_no` + เลขหน้า | — |

## 4. ข้อความรับรองที่เปลี่ยนตาม `employment_state` (ตายตัว — ห้ามให้คนพิมพ์เอง)

| `employment_state` | ย่อหน้า 1–2 (ไทย) | อังกฤษ | อ้าง |
|---|---|---|---|
| `active` | "…และ **ปัจจุบันยังคงปฏิบัติงานอยู่กับบริษัทฯ** รวมระยะเวลาการปฏิบัติงาน X ปี Y เดือน นับถึงวันที่ออกหนังสือฉบับนี้" | "…and **remains employed by the Company as at the date of this certificate**…" | BR-16 · **`sample.pdf` / `sample_en.pdf` ใช้กรณีนี้** |
| `leaving` | "…**และมีกำหนดสิ้นสุดการปฏิบัติงานในวันที่ {last_working_day}**" | "…**and is scheduled to complete employment on {last_working_day}**" | BR-16 · `OQ-CT-13` `[AI-DRAFT]` |
| `left` | "…**เคยปฏิบัติงานกับบริษัทฯ ระหว่างวันที่ {start_date} ถึงวันที่ {last_working_day}**" (ใบผ่านงาน · **สิทธิตาม ป.พ.พ. ม.585**) | "…**was employed by the Company from {start_date} to {last_working_day}**" | BR-16 · **BR-27** · S-43 |
| `not_started` | — | — | ⛔ **บล็อก ออกหนังสือไม่ได้** (FN-45) |

⭐ **ข้อห้ามตามกฎหมาย (`[STD]` G-02 · BR-28):** เอกสารนี้พิมพ์ได้เฉพาะ **ระยะเวลาที่ทำงาน · ลักษณะงาน/ตำแหน่ง · (ค่าจ้าง เมื่อเป็น rendition ค่าจ้าง)** — **ห้ามมีเหตุผลการพ้นสภาพ · โทษทางวินัย · ผลประเมิน · หมายเหตุอิสระของผู้ออก อยู่ในทุก block ของ template** · โครง template นี้ **ไม่มีช่องว่างให้ใส่ข้อความอิสระเลย** ซึ่งเป็นวิธีบังคับกฎข้อนี้ (FN-95 · FN-96)

## 5. กติกาการพิมพ์และการเก็บสำเนา

- **A4 แนวตั้ง 1 หน้าเสมอ** — ถ้าข้อมูลยาวเกิน (ชื่อหน่วยงานยาว · ประวัติตำแหน่งหลายบรรทัด) ให้ **ย่อในกล่อง PARTIES ก่อน** ห้ามขยายเป็น 2 หน้าโดยไม่ตั้งใจ
- **พิมพ์หลายชุดตาม `copies`** — ทุกชุด **เลขที่เดียวกัน เนื้อหาเดียวกัน** (FN-56) · **ไม่มีคำว่า "สำเนา" ในรอบนี้** (ทุกชุดเป็นต้นฉบับที่ลงนามจริง) `[ASSUMED]`
- **เก็บสำเนาผ่าน `ENG-DOC-STORE.store()`** ที่ `T-06` (`issued`) และ `T-07` (`sent_external`) — ⭐ **เก็บเฉพาะ rendition ที่ออกไปจริง 1 ไฟล์ต่อ 1 ใบ** ไม่ใช่เก็บทั้ง 4 แบบ (`DOCCFG_BRIEF §3`)
- **ACL ของไฟล์ rendition ที่มีตัวเลขค่าจ้างแยกจากสิทธิ์การเห็นทะเบียน** (FN-74) · ทุกครั้งที่เปิด/ดาวน์โหลด = **event `cert.restricted_viewed` ท่อ SecC** (`CSQ_BRIEF §2 E3`)
- **หลัง "ออกแล้ว" เนื้อหาห้ามเปลี่ยนตลอดไป** — การ re-render จาก snapshot ต้องได้ไฟล์ที่เหมือนเดิมทุกประการ (**BR-23** · FN-36)

## 6. Placeholder ที่ต้องแทนตอน bind (สรุปให้ dev)

| placeholder ในตัวอย่าง | แทนด้วย |
|---|---|
| บริษัท ทูบีซิมเปิล จำกัด / 2BSimple Company Limited + ที่อยู่ + โทร + อีเมล + เลขผู้เสียภาษี | **ข้อมูลบริษัทจริงจาก Organization** (ตามบริษัทของพนักงาน · `company_id`) |
| โลโก้ `.doc-logo--ph` (ตัวย่อ "2B") | `<img class="doc-logo" src="data:image/png;base64,…">` โลโก้จริง |
| ชื่อพนักงาน · รหัส · ตำแหน่ง · หน่วยงาน · วันเริ่มงาน · อายุงาน | จาก snapshot ที่ตรึงตอน `T-06` (ทั้งหมด) |
| `68,500.00 บาท` / `THB 92,000.00` + จำนวนเงินตัวอักษร | จาก `salary-structure/resolve` **เฉพาะ rendition ค่าจ้าง** |
| `CERT-2569-00042` / `CERT-2026-00043` | `cert_doc_no` จาก `ENG-DOC-NUM` |
| `7K2M-9QX4` / `4T8P-2WD6` | `verification_code` |
| ชื่อ/ตำแหน่งผู้ลงนาม | `approval_chain` ขั้นสุดท้าย |
| ธนาคารกรุงไทย… / Royal Thai Embassy, Tokyo | `recipient_name` + `purpose_*` |

> **ปีบนเอกสาร:** ไทยใช้ **พ.ศ.** (2569) · อังกฤษใช้ **ค.ศ.** (2026) — ตัวอย่างสองไฟล์จึงมีปีต่างกันโดยตั้งใจ **แต่เป็นวันเดียวกัน (30 ส.ค.)** · เลขที่เอกสารบนตัวอย่างจึงต่างกันด้วย (`CERT-2569-…` vs `CERT-2026-…`) — ⚠️ **ตอน bind จริงต้องเลือกฐานปีของเลขรันให้เป็นแบบเดียวทั้งระบบ** ตามที่ F-DOCCFG กำหนด (**`OQ-DOCCFG-CT-01`**) · **ห้ามให้เลขรันขึ้นกับภาษาของหนังสือเด็ดขาด**

## 7. คำสั่งที่ใช้สร้างไฟล์ชุดนี้ (ทำซ้ำได้)

```bash
SK=.claude/skills/thai-doc-pdf-generator
python3 $SK/scripts/build_html.py body_th.html --title "หนังสือรับรอง — CERT-2569-00042" -o PDFDOC/template.html
python3 $SK/scripts/build_html.py body_en.html --title "Certificate of Employment — CERT-2026-00043" -o PDFDOC/template_en.html
# Chromium ใช้ไม่ได้บนเครื่องนี้ → ใช้ WeasyPrint แทน scripts/render_pdf.py
python3 -c "from weasyprint import HTML; HTML(filename='PDFDOC/template.html').write_pdf('PDFDOC/sample.pdf')"
python3 -c "from weasyprint import HTML; HTML(filename='<en_nosalary>.html').write_pdf('PDFDOC/sample_en.pdf')"
pdfinfo PDFDOC/sample.pdf     # → Pages: 1 · 595.276 x 841.89 pts (A4)
pdfinfo PDFDOC/sample_en.pdf  # → Pages: 1 · 595.276 x 841.89 pts (A4)
```
