# E2E Render-Gate Report — Bank Master (F-BNK) · `f-bank.html`
- วันที่: 2026-08-11 · Runner: Playwright (chromium headless) · viewport 1440×900 (+ 1440×560 สำหรับ scroll test)
- ไฟล์: `outputs/04_Bank-Master/01_HTML/f-bank.html`
- Script: `scratchpad/e2e_bank.py` · Screenshots: `_e2e_shots/` (16 ไฟล์) · **Console errors: 0**
- โฟกัส: 3 business rules ที่ "ตัดสินแล้วต้อง hold" + latent base-kit bugs (คลิกจริง ไม่เชื่อ static read)

## Verdict: 🟢 PASS — ทุก business rule และ latent-bug check ผ่าน

| # | รายการทดสอบ | คาดหวัง | ผลจริง (E2E) | ผล |
|---|---|---|---|---|
| BR1 | **IR-BNK-01 partial lock** — edit KBANK-01 (used=620) | ล็อก ธนาคาร + เลขบัญชี, ฟิลด์อื่นแก้ได้ | `bank.disabled=true`, `acct_no.disabled=true`, `acct_name.disabled=false`, `acct_type.disabled=false`, lock-tag ×2 | ✅ |
| BR1b | edit KTB-01 (used=0) | ไม่ล็อก | `bank.disabled=false`, `acct_no.disabled=false`, lock-tag=0 | ✅ |
| BR1c | edit SCB-01 (used=340) | ล็อกด้วย (used>0) | `bank.disabled=true` | ✅ |
| BR2 | **GL picker filter (F-PG BR-06)** — create ใหม่ | เห็นเฉพาะ active (KBANK); **ไม่เห็น SCB (draft)** | options = [`— ยังไม่ผูกกลุ่ม —`, `KBANK — ธนาคารกสิกรไทย`] · has SCB = **false** | ✅ |
| BR2b | edit SCB-01 (bound to draft group) | เห็น `SCB (ร่าง)` เพื่อกัน binding หลุด | options มี `SCB — ธนาคารไทยพาณิชย์ (ร่าง)` · selected value = `SCB` | ✅ |
| L1 | **Drawer re-render jump (#29)** — scroll drawer 325px → toggle checkbox | ไม่เด้งกลับบน | scroll before=325 → after toggle=325 → after 2nd toggle=325 (OK-NO-JUMP) | ✅ |
| L2 | **In-drawer dropdown z-index** — เปิด "เปลี่ยนสถานะ" ใน view drawer | เมนูอยู่เหนือ drawer body | `elementFromPoint` ที่ตำแหน่งเมนู = `pill is-active` (ตัวเมนูเอง อยู่บนสุด) | ✅ |
| L3 | **Modal z-index** — เปิด bulk-delete modal | modal อยู่เหนือทุกอย่าง | `elementFromPoint` กลาง modal = `MODAL-ON-TOP` | ✅ |
| L4 | **Overlay clipping (#95)** | dropdown ไม่โดน clip | GL/bank/type/status ทั้งหมดเป็น native `<select>` (browser layer เอง) — ไม่มี custom dropdown ใน scroll container → ไม่มีเคส clip | ✅ (n/a by design) |

## Interaction coverage (คลิกจริงครบ)
| Flow | ผล |
|---|---|
| List render | 8 แถว, KPI stat row (8/6/1/1), sticky thead — screenshot `01_list.png` ✅ |
| Create drawer | เปิด/ปิดได้, GL picker ไม่มี SCB, ปุ่ม primary label = `บันทึกบัญชีธนาคาร` (⚠️ ควรเป็น `ยืนยันสร้าง` — UX-03) `02_create_drawer.png` |
| Edit drawer (locked) | lock-tag แสดงบน ธนาคาร+เลขบัญชี, ฟิลด์ disable `03_edit_used_locked.png` ✅ |
| Edit drawer (SCB draft-bound) | GL picker แสดง `SCB (ร่าง)` selected `04_edit_scb_glpicker.png` ✅ |
| View drawer + tabs | summary chips + tab ภาพรวม/ประวัติ สลับได้ `07/09` ✅ |
| Status dropdown (in-drawer) | เปิดเหนือ body, เลือกได้ `08_view_statusmenu.png` ✅ |
| Bulk select → delete modal | เลือก 2 (1 used>0), modal บอก "ลบ 1 รายการ" ข้ามตัวที่มีเอกสาร `10/11` ✅ (used>0 guard ทำงาน) |
| Search | `SCB` → 1 แถว `12_search.png` ✅ |
| Filter status=ร่าง | → 1 แถว ✅ |
| Sort code desc | แถวแรก = `BAY-01` (เรียงถูก) ✅ |
| Empty state (filter no-match) | คำค้น `ZZZZZZ` → empty block แสดง `13_empty_filter.png` ✅ |
| Toggle status | setStatus KTB-01 → `inactive` สำเร็จ + toast ✅ |
| Import modal | pick → preview 6 แถว (มีแถวผิด/ซ้ำ highlight) `14/15` ✅ |

## หมายเหตุ
- **Latent bug L1** ทดสอบซ้ำด้วย viewport เตี้ย (560px) เพื่อบังคับให้ drawer body overflow จริง (325px) — ยืนยันไม่มีการเด้ง. สาเหตุเชิงกล: checkbox ในฟอร์มเป็น native `<input>` ที่ไม่เรียก `render()`/`innerHTML` rebuild จึงไม่มีทางเด้งอยู่แล้ว + มี `_keepScroll()` เป็น safety net
- ไม่พบ console error หรือ pageerror ตลอด flow ทั้งหมด
- Screenshot ทั้ง 16 ใบเก็บที่ `_e2e_shots/` — ทุกข้อสรุปในตารางอ้างได้จากไฟล์ภาพ + ค่า DOM ที่ query จริง
