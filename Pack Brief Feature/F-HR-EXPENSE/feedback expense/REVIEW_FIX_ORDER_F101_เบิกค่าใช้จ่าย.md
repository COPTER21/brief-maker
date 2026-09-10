# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
HR — F101 Expense Claim (เบิกค่าใช้จ่าย) · expense.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F101 Expense Claim (เบิกค่าใช้จ่าย) · mod HR · arch **Q-document** · dec: doa + ntf + csq + doccfg + pdfdoc |
| ไฟล์ที่ตรวจ | expense.html (2,402 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-09 · BA gate (html-review-fix-order) |
| ขอบเขต | Re-gate ก่อนเข้า Phase B (FRD/TC) — เทียบ spec F101 + governance + interaction จริง |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 7 block · audit **FAIL=0** WARN=4 (kit residuals + #99 segmented) · Playwright **pageerror=0** |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 6 · HIGH 2 · MINOR 2 → แก้แล้วส่ง re-gate เต็มรอบ |

## 1. สรุปผลตรวจ (Executive Summary)

ไฟล์นี้ engineering ดีกว่าสองตัวก่อนหน้าใน batch เดียวกันชัดเจน: Pattern Q ครบ (list + wizard + view 4 แท็บ รายละเอียด/PDF Preview/ลายเซ็น·อนุมัติ/ประวัติ + เอกสารแนบใน landing) · B2 line editor + VAT engine canonical · DOA ฝั่ง submit ทำถูกตามมติ 2026-08-17 — resolve ช่วงวงเงินจาก DOA กลาง (BR-04/LK-1) + **slot ไม่ prefill** ผู้ใช้ต้องเลือกคนจริง ปุ่ม disabled จนครบ (UX-06) · reject บังคับเหตุผล · over-cap = เตือน+เหตุผลตามมติ A-EXP-05 · `_busy` กัน double-submit ทุก action · unsupportedNote ประกาศ scope-cut เป็นลายลักษณ์อักษรในไฟล์ (จ่ายจริง/mileage/travel pre-approval/cash advance/multi-currency/OCR)

ประเด็นที่ต้อง **BLOCK** กระจุกที่ครึ่งหลังของ flow: (1) doApprove อนุมัติใบที่ถูกตีกลับได้ + ออกเลข (2) chain 3 ขั้น (ผอ. ยัง pending) คลิกเดียว approved หมด (3) **masking กลับด้าน** — ผู้อนุมัติ DOA เห็นจำนวนเงินเป็น ฿••••• ทุกบรรทัดแต่ต้องกดอนุมัติตามวงเงิน ขณะที่ผู้เบิก/ธุรการเห็นเงินทุกใบและเห็นปุ่มอนุมัติเอง (self-approve — toxic pair ตาม SoD) (4) เอกสารที่อนุมัติแล้ว reopen กลับเป็นร่าง เลขที่ออกแล้วหาย (5) ใบที่**จ่ายแล้ว**ถูกยกเลิกได้ (6) เลขรันแบบ count-based **ออกเลขซ้ำได้จริง** (EXP-2569-005 สองใบ) และไม่มีร่องรอย ENG-DOC-NUM/DOCCFG ทั้งที่ chip doccfg ประกาศ

### 1.1 ความครบถ้วนเทียบ Spec F101

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| ยื่นเบิก + แนบหลักฐาน (มือถือได้) | ✅ | wizard หลายขั้น + B2 line editor + แนบใบเสร็จ + receiptRequired ตามหมวด (HR Config #107) |
| ตรวจงบ (F117) + เพดานสิทธิ์สวัสดิการ | ❌ | มีเฉพาะเพดานหมวดจาก HR Config — hook ตรวจงบ F117 = 0 · hook เพดานสวัสดิการ (F102 ctl, ba-done) = 0 (FIX-07) |
| อนุมัติตามวงเงิน DOA | ⚠️ | resolve ช่วงวงเงิน + slot ไม่ prefill ✓ แต่ approve collapse ทุกขั้น (FIX-02) + ผู้อนุมัติถูก mask เงิน (FIX-03) |
| จ่ายคืนผ่าน PV/petty cash + สถานะจ่ายแล้ว | ⚠️ | payHook display-only ✓ ("ส่งจ่ายผ่านเงินเดือน รอบ ก.ย." / "โอนแล้ว") — petty cash ไม่มี · การจ่ายจริงถูกตัด scope ใน unsupportedNote (OQ-EXP-01) |
| เคลียร์เงินทดรอง หักลบอัตโนมัติ | ❌ | ประกาศ "ไม่รองรับรอบนี้ (ตัดสินแล้ว)" ในไฟล์ — ขัด c[] ของ Feature List (OQ-EXP-01) |
| dec: doa | ⚠️ | submit ถูกต้องครบ · approve ผิด (FIX-01/02) |
| dec: ntf | ⚠️ | มีแต่ข้อความ toast "แจ้งผู้อนุมัติ/ผู้เบิก" — ไม่มี anchor/comment NTF ให้ decl_rule จับ (FIX-08) |
| dec: csq | ✅ hook | modal+toast "ยิง 7C (FC/EC)" — ท่อที่อ้างรอเทียบ CSQ_BRIEF (OQ-EXP-02) |
| dec: doccfg | ❌ | เลขรัน gen เองแบบ count-based ในตัว feature · ENG-DOC-NUM/DOCCFG = 0 · เลขซ้ำได้จริง (FIX-06) |
| dec: pdfdoc | ✅ | แท็บ PDF Preview (a4Doc) ตามฟอร์ม |
| Pattern Q archetype | ✅ | list + wizard + view 4 แท็บ + เอกสารแนบใน landing ครบ |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] doApprove ไม่มี precondition guard — อนุมัติใบที่ถูกตีกลับได้ + ออกเลข

| ช่อง | รายละเอียด |
|---|---|
| อาการ | เรียกอนุมัติเอกสารสถานะ rejected/cancelled/draft ได้ทันที พร้อมออกเลขเอกสาร |
| หลักฐาน | Bypass E1: d5 `status:'rejected'` → `doApprove()` → `{status:'approved', code:'EXP-2569-005'}` |
| ผลกระทบ | terminal ไม่ terminal จริง — ใบที่ตีกลับกลับมาออกเลข+เข้าคิวจ่ายได้ |
| ตำแหน่ง | `function doApprove(id)` |
| วิธีแก้ | guard ต้น function: `d.status!=='pending_approval'` → toast + return |

เกณฑ์ตรวจรับ: doApprove กับ rejected/cancelled/draft/approved/paid → ไม่เปลี่ยน · pending_approval → เดินต่อได้

### FIX-02 · [CRITICAL] DOA chain collapse — 3 ขั้น คลิกเดียว approved หมด

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `d.chain.forEach(s=>s.status='approved')` — ขั้นที่ยัง pending ถูกปั๊ม approved ในคลิกเดียว |
| หลักฐาน | Bypass E2: d4 chain `[หัวหน้า:approved, ผจก.:approved, ผอ.:pending]` → doApprove ครั้งเดียว → `['approved','approved','approved']` + เอกสาร approved |
| ผลกระทบ | สายอนุมัติตามวงเงิน (หัวใจ c[3]) กลายเป็นพิธีกรรม — ยอด 50,000+ ที่ต้องถึง ผอ. จบที่คลิกแรก |
| ตำแหน่ง | `doApprove` |
| วิธีแก้ | advance ทีละขั้น: หา step แรกที่ยัง pending → approved + at · ยังมีขั้นถัดไป → เอกสารคง pending_approval · ขั้นสุดท้ายค่อย approved + ออกเลข + PDF + 7C + payHook (side-effect ทั้งชุดครั้งเดียวตอนจบ chain) |

เกณฑ์ตรวจรับ: ใบ chain 3 ขั้น: คลิก 1–2 เอกสารยัง pending_approval ขั้นถัดไปเป็นคิว · คลิก 3 → approved + เลขออกครั้งเดียว · ทุกขั้นมี at

### FIX-03 · [CRITICAL] Masking กลับด้าน + role guard หลุด — ผู้อนุมัติมองไม่เห็นเงิน / ผู้เบิกอนุมัติเองได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | role ผู้อนุมัติ (DOA) ตั้ง `mask:true` → เปิดใบรออนุมัติเห็นเงินทุกบรรทัด/ยอดรวมเป็น "฿ •••••" แต่มีปุ่มอนุมัติ · role ผู้เบิก/ธุรการ (`mask:false`) เห็นเงินทุกใบของทุกคน และเห็นปุ่มอนุมัติ/ไม่อนุมัติ (ปุ่ม render ตามสถานะอย่างเดียว) · function ไม่ guard role |
| หลักฐาน | Screenshot role_mgr_view_pending (เงิน ••••• + ปุ่มอนุมัติมุมล่าง) · evaluate: ผู้เบิก hasApproveBtn=true |
| ผลกระทบ | (a) อนุมัติตามวงเงินโดยมองไม่เห็นวงเงิน = เป็นไปไม่ได้เชิงธุรกิจ (b) ผู้สร้างใบอนุมัติเองได้ = toxic pair ตรงตาม SoD (F145) |
| ตำแหน่ง | `EXP.roles` (flag mask) · จุด render ปุ่มใน `dwView` foot · `doApprove/doReject` |
| วิธีแก้ | สลับทิศ masking: ผู้อนุมัติเห็นเงินเต็ม · ผู้เบิก/ธุรการเห็นเฉพาะใบของตน (หรือ mask ใบคนอื่น — scope แขวน OQ-EXP-03) · ปุ่มอนุมัติ/ไม่อนุมัติ render เฉพาะ role ผู้อนุมัติ + guard ต้น doApprove/doReject (mirror sec.can()) |

เกณฑ์ตรวจรับ: role ผู้อนุมัติเห็นจำนวนเงินเต็มบนใบรออนุมัติ · role ผู้เบิกไม่เห็นปุ่มอนุมัติ + เรียก doApprove ตรงไม่ผ่าน

### FIX-04 · [CRITICAL] doReopen บนใบอนุมัติแล้ว — เอกสารออกเลขแล้วกลับเป็นร่าง เลขหาย

| ช่อง | รายละเอียด |
|---|---|
| อาการ | doReopen ไม่เช็คสถานะ — เรียกกับใบ approved ได้ สถานะกลับ draft และ code ถูกทับเป็น "(ร่าง)" |
| หลักฐาน | Bypass E4: d2 `{approved, code:'EXP-2569-0001'}` → doReopen → `{draft, code:'(ร่าง)'}` |
| ผลกระทบ | เอกสารทางการที่ออกเลขแล้วหายจากทะเบียน — ขัด Q-document rule "แก้หลังอนุมัติ = revision ใหม่ + re-approve" และขัด doccfg (เลขออกแล้วห้ามหาย) |
| ตำแหน่ง | `doReopen` (ปุ่ม render ถูกแล้ว — เฉพาะ rejected · รูอยู่ที่ function) |
| วิธีแก้ | guard: เฉพาะ `status==='rejected'` เท่านั้น — แก้ใบ approved เป็นคนละ flow (revision) ไม่ทำในรอบนี้ |

เกณฑ์ตรวจรับ: doReopen กับ approved/paid/pending/draft → ไม่เปลี่ยน · rejected → draft ได้ตามเดิม

### FIX-05 · [CRITICAL] doCancel บนใบที่จ่ายแล้ว

| ช่อง | รายละเอียด |
|---|---|
| อาการ | doCancel ไม่เช็คสถานะ — ใบ paid ถูกยกเลิกได้ |
| หลักฐาน | Bypass E5: d6 `{status:'paid'}` → doCancel → `cancelled` |
| ผลกระทบ | ใบที่เงินออกไปแล้ว (โอนแล้ว 2569-08-28) หายจากสถานะจ่าย — data การเงินเพี้ยน |
| ตำแหน่ง | `doCancel` (ปุ่ม render เฉพาะ draft — รูอยู่ที่ function) |
| วิธีแก้ | guard: เฉพาะ `['draft'].includes(d.status)` (pending ให้ใช้เส้นทางตีกลับ/ถอนตามที่ Strike เคาะ) — toast + return สถานะอื่น |

เกณฑ์ตรวจรับ: paid/approved/rejected/pending → ยกเลิกไม่ได้ · draft → ได้ตามเดิม

### FIX-06 · [CRITICAL] เลขรันซ้ำ + ไม่มี hook ENG-DOC-NUM (dec doccfg)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | เลขเอกสาร gen ในตัว feature: `'EXP-2569-00'+(3+count(approved))` — (a) count-based: ใบที่หลุดจากสถานะ approved ทำเลขถัดไปซ้ำ (b) format ผิด (005 ไม่ pad 4 หลัก) (c) ไม่มีร่องรอย ENG-DOC-NUM/DOCCFG ทั้งไฟล์ทั้งที่ chip doccfg ประกาศ |
| หลักฐาน | Bypass E6: อนุมัติ t1 ได้ `EXP-2569-005` → reopen t1 → อนุมัติ t2 ได้ `EXP-2569-005` **ซ้ำกันจริง** · grep ENG-DOC-NUM=0, doccfg=0 |
| ผลกระทบ | เลขเอกสารทางการซ้ำ = ผิดหลัก F003 (concurrent-safe, ห้าม feature รันเลขเอง) — Phase B จะลอก pattern ผิด |
| ตำแหน่ง | `doApprove` (บรรทัด gen code) |
| วิธีแก้ | mock ให้ถูกหลัก: ตัวนับ global เดินหน้าอย่างเดียว (ไม่อิง count สถานะ) + pad 4 หลัก + comment `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type ที่ประกาศใน DOCCFG_BRIEF_F101 — ห้าม feature รันเลขเอง -->` + สำเนา PDF ผ่าน ENG-DOC-STORE (comment) |

เกณฑ์ตรวจรับ: เคส E6 ซ้ำ → เลขไม่ซ้ำ ไม่ reuse · format EXP-YYYY-NNNN 4 หลักเสมอ · มี comment hook ENG-DOC-NUM/DOCCFG

### FIX-07 · [HIGH] c[2] hooks หาย — ตรวจงบ F117 และเพดานสิทธิ์สวัสดิการ (F102 ctl)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | ระบบตรวจเฉพาะ "เพดานหมวด" จาก HR Config — ไม่มี hook ตรวจงบ (F117) และไม่มี hook เพดานสิทธิ์สวัสดิการ ทั้งที่ c[2] ระบุทั้งคู่ และ contract F102→F101 (ctl) lock แล้ว (F102 ba-done) |
| หลักฐาน | grep F117=0 · budget=0 · สวัสดิการปรากฏเฉพาะเมนู sidebar |
| ผลกระทบ | contract ctl กับ F102 ไม่มีหลักฐานบนหน้าจอ → FRD เขียน integration ไม่ได้ |
| ตำแหน่ง | wizard ขั้นสรุป/ตรวจ + `dwView` |
| วิธีแก้ | display-only hook 2 จุด: (a) กล่อง "ตรวจงบ (Budget Control F117 — W7)" สถานะ mock + note ยังไม่ dev (b) บรรทัดเบิกหมวดสวัสดิการ → โชว์สิทธิ์คงเหลือจาก F102 (mock) + เตือนเกินสิทธิ์ — ไม่ mock หน้าจอ feature อื่น |

เกณฑ์ตรวจรับ: หน้าสรุปก่อนส่งเห็น hook ตรวจงบ + เพดานสวัสดิการพร้อม note ที่มา · ไม่มีหน้าจอ F117/F102 เกิดใหม่

### FIX-08 · [HIGH] dec ntf ไม่มี anchor — มีแต่ข้อความ toast

| ช่อง | รายละเอียด |
|---|---|
| อาการ | chip ntf ประกาศ แต่ในไฟล์ไม่มี `ntf(`/comment NTF event ใด ๆ — มีเพียงข้อความ toast "แจ้งผู้อนุมัติ/แจ้งผู้เบิก" |
| หลักฐาน | grep ntf(=0 · NTF=0 |
| ผลกระทบ | decl_rule (S1.8) เทียบ chip vs detect จะ DIVERGENCE |
| ตำแหน่ง | doSubmit / doApprove / doReject |
| วิธีแก้ | เพิ่ม comment hook ต่อจุด: `<!-- NTF: exp.submitted → ผู้อนุมัติขั้นแรก · exp.approved/exp.rejected → ผู้เบิก · doa_pending/doa_result มาจาก DOA engine ห้ามประกาศซ้ำ (NTF_BRIEF_F101) -->` |

เกณฑ์ตรวจรับ: ทุก transition ที่แจ้งเตือนมี NTF anchor · ไม่ประกาศ doa_* ซ้ำ

### FIX-09 · [MINOR] ปุ่มปิด drawer icon ไม่ render (กล่องเปล่า)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `<i data-lucide>` ในปุ่มปิด drawer ไม่ถูกแปลงเป็น svg — บั๊กเดียวกับ F131 |
| หลักฐาน | Screenshot role_mgr_view_pending มุมขวาบน |
| วิธีแก้ | เรียก `renderIcons()` หลังเติม drawer innerHTML |

เกณฑ์ตรวจรับ: เปิด drawer แล้วปุ่มปิดมี svg เสมอ

### FIX-10 · [MINOR] microcopy อ้างท่อ 7C แบบ fix ("FC/EC")

| ช่อง | รายละเอียด |
|---|---|
| อาการ | modal/toast ระบุ "ยิง 7C (FC/EC)" hardcode ชื่อท่อ — ท่อจริงต้องมาจาก CSQ_BRIEF (และ DC มาจาก DOA engine อัตโนมัติ ห้ามอ้างเอง) |
| หลักฐาน | modal approve + toast doApprove |
| วิธีแก้ | เปลี่ยนเป็น "บันทึกเข้า 7C ตาม CSQ_BRIEF_F101" — ท่อจริงรอเคาะ OQ-EXP-02 |

เกณฑ์ตรวจรับ: ไม่มีชื่อท่อ hardcode ใน microcopy

## 3. WARN จาก audit (แก้ตามสะดวก · ไม่บล็อก)

- Rule #21 icon ไม่มี w-/h- 3 จุด (CSS-sized kit)
- Rule #40 `.uc-email` CSS ตกค้าง (ไม่ถูกใช้)
- hardcoded font-size base-kit residual
- Rule #99 ส่วนลดท้ายบิล segmented ฿/% — ตรวจแล้วมี endbill.mode ใน mock (audit จับ pattern ไม่เจอ) — ยืนยันด้วยตาใน wizard ก่อนปิด WARN

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ (ส่วน FRD) |
|---|---|---|---|
| OQ-EXP-01 | unsupportedNote ตัด scope "เคลียร์เงินทดรอง (c[5])" + "การจ่ายจริง/petty cash (c[4])" — ขัด c[] ใน Feature List: ยืนยันมติ (อ้าง 0_DIRECTION ถ้ามี) + อัพเดต Feature List/Coverage Manifest หรือสั่งเพิ่มกลับ | Strike | Coverage Manifest · §Integration F103/F109/F091 |
| OQ-EXP-02 | ท่อ 7C ของใบเบิก — ไฟล์อ้าง FC/EC แต่การอนุมัติค่าใช้จ่ายควรแตะ AC (ลงบัญชี) ด้วยหรือไม่ · DC มาจาก DOA อัตโนมัติ | Strike + Architect | CSQ_BRIEF_F101 |
| OQ-EXP-03 | scope การเห็นของ ผู้เบิก/ธุรการ — ปัจจุบันเห็นใบ+ยอดเงินของทุกคน ควรเป็น SELF/DEPT? | Strike | SEC_BRIEF scope_type |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ทุก script block ผ่าน
- [ ] audit.sh FAIL=0
- [ ] Playwright pageerror=0 ทุก route/drawer/modal
- [ ] รันเคส Acceptance ของ FIX-01..06 (CRITICAL) และ FIX-07..08 (HIGH) ซ้ำ — โดยเฉพาะ E1/E2/E4/E5/E6 + masking ผู้อนุมัติ
- [ ] ส่งไฟล์กลับ re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (BA status F101) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → เข้า Phase B (FRD/TC)
