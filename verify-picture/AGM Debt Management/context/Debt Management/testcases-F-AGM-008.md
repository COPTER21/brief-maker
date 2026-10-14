# AI Test Cases — F-AGM-008 Debt Management (จัดการหนี้ลูกหนี้)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `debt-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ FRD 06_TESTS §6.10 microcopy + 05_RULES + สแกน prototype แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side optimistic lock 409 · **DOA approval workflow จริง (PENDING_APPROVAL 202)** · accrual/ดอกเบี้ยงวดจริง · manual allocation editor · **feed outstanding → CBM/Contract จริง** · PDF Statement/CSV จริง · adjustment reverse append จริง) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

> ⚠ **หมายเหตุ microcopy (prototype ปัจจุบัน ≠ FRD anchor ตรง ๆ 3 จุด — Expected ยึด "ข้อความบนจอจริง"):**
> ส่งออก CSV → `จำลองส่งออกไฟล์ CSV (5 รายการ)` (FRD anchor "เริ่มส่งออกรายงานแล้ว") · รายงาน Aging → `จำลองสร้างรายงาน Aging Summary` (FRD anchor "กำลังสร้างรายงานอายุหนี้...") · ค้นโควตาไม่พบ → `ไม่พบโควตาที่ค้นหา` (FRD anchor "ไม่พบโควตา") · "พบข้อมูลโควตา" ไม่เป็น toast — แสดงเป็น section **ข้อมูลลูกหนี้** + auto-fill ชื่อ/เบอร์แทน

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-008 (AGM/DEBT — จัดการหนี้ลูกหนี้) |
| App entry | เปิดไฟล์ `debt-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/debtors` (list — default) · `#/debtors/:debtor_id` (list + Detail drawer 5 แท็บ, refresh-safe) |
| Overlays (ไม่ผูก route) | create-debtor drawer · create-obligation drawer · manual-payment modal · write-off modal |
| ที่มา | FRD_F-AGM-008_Pack (06_TESTS AC-01..36 + XT-01..05 · 05_RULES BR-DEBT-01..11 / VR-01..15 / EC-01..13) |
| จำนวนเคส | 54 เคส / 10 groups |
| Signature ⭐⭐⭐ | **3-entity ledger** (ไม่ใช่ state-machine): Debtor → Obligation (N) → Ledger (double-entry, append-only) |
| หัวใจ 1 — Payment allocation waterfall | จัดสรรตาม **priority ↑** · ในแต่ละภาระ **ดอกเบี้ย → ค่าปรับ → ต้นทุน** · validate-then-save (ต้องกด `ตรวจสอบการจัดสรร` ก่อน) |
| หัวใจ 2 — Write-off DOA | คงเหลือ > **100,000** → warning `จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ` · ≤ 100,000 → ปกติ |
| หัวใจ 3 — Contract lock | ภาระจากสัญญา (source=contract 🔒) → แก้ไม่ได้ `รายการจากสัญญาแก้ไขไม่ได้` |
| หัวใจ 4 — Debtor idempotent | 1 ลูกหนี้ : 1 โควตา · ค้นโควตาที่มีลูกหนี้แล้ว → `มีลูกหนี้อยู่แล้ว` + navigate detail |
| หัวใจ 5 — Ledger double-entry | เดบิต/เครดิต/คงเหลือ · kind badge (ตั้งหนี้/ดอกเบี้ย/ค่าปรับ/ชำระ/ปรับปรุง/ตัดหนี้สูญ/ย้อนรายการ) · append-only |
| หมายเหตุ mock | prototype in-memory: refresh (F5) = reset seed 5 ลูกหนี้ + 8 ภาระ + 6 โควตา — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม |
| Cross-module ⭐ | read Quota (F-AGM-002 verified) · read Contract (F-AGM-005 contract_id 🔒) · **feed outstanding → CBM (F-AGM-007) / Contract** = `(ต้อง simulate)` ที่ SIT |

**Seed ตั้งต้น (หลัง refresh — 5 ลูกหนี้ DEB-2568-0001..0005):**

| เลขลูกหนี้ | โควตา · เกษตรกร | ยอดคงค้าง | ภาระ# | Aging | สถานะ | labels |
|---|---|---|---|---|---|---|
| DEB-2568-0001 | QUO-2568-0001 · สมชาย ไร่ทอง | 125,000.00 ฿ | 3 | 31-60 | ใช้งาน | คิว1, ฤดูแล้ง2568 |
| DEB-2568-0002 | QUO-2568-0002 · บุญมี ทุ่งกว้าง | 85,000.00 ฿ | 2 | 0-30 | ใช้งาน | คิว2 |
| DEB-2568-0003 | QUO-2568-0003 · ประเสริฐ ใจดี | 0.00 ฿ | 0 | — | ปิด | — |
| DEB-2568-0004 | QUO-2568-0004 · วิไล สวนอ้อย | 245,000.00 ฿ | 5 | 90+ | ใช้งาน | ค้างชำระ, คิว3 |
| DEB-2568-0005 | QUO-2568-0006 · จันทร์ ศรีสุข | 156,000.00 ฿ | 4 | 61-90 | ใช้งาน | คิว4 |

- **Stat cards:** ลูกหนี้ทั้งหมด = **5** · ยอดคงค้างรวม = **611,000.00 ฿** · เกินกำหนด (Aging 90+) = **1** (DEB-0004) · ตัดหนี้สูญ = **0**

**Seed ภาระหนี้ (8 obligations OBL-2568-0001..0008 — ต้นทุน/ดอกเบี้ย/ค่าปรับ/คงเหลือ):**

| ID | ลูกหนี้ | แหล่งที่มา | ประเภท | ต้นทุน | ดอกเบี้ยสะสม | ค่าปรับ | คงเหลือ | ลำดับ |
|---|---|---|---|---|---|---|---|---|
| OBL-2568-0001 | DEB-0001 | สัญญา 🔒 (CNT-2568-0011) | ปุ๋ย | 70,000 | 1,500 | 0 | 71,500 | 1 |
| OBL-2568-0002 | DEB-0001 | แมนนวล | เครื่องจักร | 55,000 | 1,500 | 0 | 56,500 | 2 |
| OBL-2568-0003 | DEB-0001 | ปรับปรุง (ลดต้นเงิน · ref OBL-2568-0001 / LED-2568-0004) | อื่นๆ · ปรับลดต้นเงินตามข้อตกลงประนอมหนี้ | -5,000 | 0 | 0 | -3,000 | 3 |
| OBL-2568-0004 | DEB-0002 | สัญญา 🔒 (CNT-2568-0021) | พันธุ์อ้อย | 45,000 | 300 | 0 | 45,300 | 1 |
| OBL-2568-0005 | DEB-0002 | แมนนวล | ยาปราบ | 39,500 | 200 | 0 | 39,700 | 2 |
| OBL-2568-0006 | DEB-0004 | สัญญา 🔒 (CNT-2568-0041) | ปุ๋ย | 138,000 | 5,000 | 2,000 | 145,000 | 1 |
| OBL-2568-0007 | DEB-0004 | แมนนวล | เงินส่งเสริม | 95,000 | — | — | 100,000 | 2 |
| OBL-2568-0008 | DEB-0005 | แมนนวล | เครื่องจักร | 154,000 | — | — | 156,000 | 1 |

> ⚠ **allocation signature:** DEB-0001 คงค้าง = Σ obligation = 71,500 + 56,500 + (-3,000) = **125,000** · DEB-0002 = 45,300 + 39,700 = **85,000**

**Seed บัญชีสมุด (ledger) บน DEB-2568-0001 — 4 แถว double-entry (append-only):**

| ID | ประเภท (kind) | เดบิต | เครดิต | คงเหลือ |
|---|---|---|---|---|
| LED-2568-0001 | ตั้งหนี้ | 70,000 | - | 70,000 |
| LED-2568-0002 | ดอกเบี้ย | 1,500 | - | 71,500 |
| LED-2568-0003 | ตั้งหนี้ | 55,000 | - | 126,500 |
| LED-2568-0004 | ชำระ | - | 8,000 | 118,500 |

**Seed โควตา (6 รายการ — จาก `QUOTAS` const, READ-ONLY · quota search):**

| เลขโควตา | เกษตรกร | เบอร์ | มีลูกหนี้แล้ว? |
|---|---|---|---|
| QUO-2568-0001 | สมชาย ไร่ทอง | 0812345678 | ✅ DEB-2568-0001 |
| QUO-2568-0002 | บุญมี ทุ่งกว้าง | 0898765432 | ✅ DEB-2568-0002 |
| QUO-2568-0003 | ประเสริฐ ใจดี | 0861112222 | ✅ DEB-2568-0003 |
| QUO-2568-0004 | วิไล สวนอ้อย | 0873334444 | ✅ DEB-2568-0004 |
| QUO-2568-0005 | มานพ นำทาง | 0865556666 | **❌ ยังไม่มีลูกหนี้** |
| QUO-2568-0006 | จันทร์ ศรีสุข | 0887778888 | ✅ DEB-2568-0005 |

> quota search placeholder = **พิมพ์เลขโควตา หรือ ชื่อเกษตรกร** · ค้นด้วยเลขโควตา/ชื่อเกษตรกร แล้วกดปุ่ม **ค้นหา** · ค้นว่าง → `กรุณากรอกรหัสโควตา` · ไม่พบ → `ไม่พบโควตาที่ค้นหา`

**VERBATIM microcopy (Expected anchors — copy เป๊ะจาก prototype):**
- ปุ่ม list: `ส่งออก CSV` · `รายงาน Aging` · `สร้างลูกหนี้` · `ล้างตัวกรอง` · `ยกเลิกการเลือก`
- ปุ่ม detail: `บันทึกการชำระ` · `สร้างภาระหนี้` · `ส่งออก Statement` · `ปิด` · row-actions `ดู` / `แก้ไข` / `ตัดหนี้`
- Tabs: `ภาพรวม` · `ภาระหนี้` · `บัญชีสมุด` · `เอกสาร` · `การตั้งค่า`
- Status pill: `ใช้งาน` · `ระงับ` · `ปิด` · `ตัดหนี้สูญ` · `ย้อนรายการ`
- Aging pill/filter: `0-30 วัน` · `31-60 วัน` · `61-90 วัน` · `90+ วัน` · filter `ทุกสถานะ` / `ทุกช่วง Aging`
- Source badge: `สัญญา` 🔒 · `แมนนวล` · `ปรับปรุง`
- Ledger kind badge: `ตั้งหนี้` · `ดอกเบี้ย` · `ค่าปรับ` · `ชำระ` · `ปรับปรุง` · `ตัดหนี้สูญ` · `ย้อนรายการ`
- Payment: `บันทึกการชำระเงิน` · วิธี `เงินสด`/`โอนเงิน`/`หักกลบ` · `ตรวจสอบการจัดสรร` · allocation types `ดอกเบี้ย`/`ค่าปรับ`/`ต้นทุน` · `รวมจัดสรร`
- Write-off: `ตัดหนี้สูญ` · `ยืนยันตัดหนี้`
- Toasts (success/info): `สร้างลูกหนี้สำเร็จ` · `บันทึกภาระหนี้สำเร็จ` · `ตรวจสอบการจัดสรรเรียบร้อย` · `บันทึกการชำระเรียบร้อย` · `ตัดหนี้เรียบร้อย` · `สร้างเอกสารเรียบร้อย` · `มีลูกหนี้อยู่แล้ว` · `จำลองส่งออกไฟล์ CSV (5 รายการ)` · `จำลองสร้างรายงาน Aging Summary`
- Errors (verbatim): `กรุณากรอกรหัสโควตา` · `ไม่พบโควตาที่ค้นหา` · `กรุณากรอกชื่อเกษตรกร` · `จำนวนต้นทุนต้องมากกว่า 0` · `กรุณากรอกรายละเอียดประเภทอื่นๆ` · `กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น "จากสัญญา"` · `กรุณาเลือกชนิดการปรับปรุง` · `การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี)` · `วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย` · `วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด` · `กรุณากรอกจำนวนเงินที่ถูกต้อง` · `กรุณาตรวจสอบการจัดสรรก่อน` · `กรุณากรอกเลขอ้างอิง` · `กรุณายืนยันการตัดหนี้` · `กรุณากรอกเหตุผลการตัดหนี้` · inline `จำนวนเกินยอดคงเหลือ` · `จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ` · `รายการจากสัญญาแก้ไขไม่ได้`
- Empty: list ว่าง (ไม่มีลูกหนี้) → `ไม่พบลูกหนี้` + `สร้างลูกหนี้ใหม่` · filter ว่าง → `ไม่พบรายการที่ค้นหา` + `ล้างตัวกรอง` · ภาระหนี้ว่าง → `ยังไม่มีภาระหนี้` · เอกสาร → `ยังไม่มีเอกสาร`
- Server (simulate): `ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช` (409 stale) · `รายการซ้ำ (idempotent)` (409 dup) · `ไม่มีสิทธิ์ดำเนินการ` (403) · `รายการจากสัญญาแก้ไขไม่ได้` (423 LOCKED)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L — List / search / filter / stats / CSV·Aging | TC-L01..L06 (6) | สูงสุด |
| D — Debtor create (idempotent + quota search) | TC-D01..D05 (5) | สูงสุด |
| T — Debtor detail 5 tabs (header/quick stats/tabs/settings) | TC-T01..T06 (6) | สูง |
| O — Obligation create (source gating + type + dates) | TC-O01..O08 (8) | สูงสุด |
| P — Manual payment (waterfall · validate-then-save) ⭐ | TC-P01..P07 (7) | สูงสุด |
| M — Write-off (DOA 100k gate) ⭐ | TC-M01..M06 (6) | สูงสุด |
| G — Ledger / double-entry / export Statement | TC-G01..G04 (4) | สูง |
| K — Contract-lock & adjustment (append-only) | TC-K01..K03 (3) | สูง |
| N — Aging & negative outstanding | TC-N01..N03 (3) | กลาง |
| X — Cross-module / event XT-01..05 + simulate | TC-X01..X06 (6) | สูงสุด |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | list + 4 stats (ลูกหนี้ทั้งหมด/ยอดคงค้างรวม/เกินกำหนด/ตัดหนี้สูญ) | TC-L01 |
| AC-02 | ค้นหา (โควตา/ชื่อ/เลขลูกหนี้) · กรอง สถานะ + Aging | TC-L02, TC-L03, TC-L04 |
| AC-03 | คอลัมน์ครบ + ยอดติดลบ = แดง | TC-L01, TC-N03 |
| AC-04 | ส่งออก CSV + รายงาน Aging | TC-L06 |
| AC-05 | empty filter → "ไม่พบลูกหนี้" (no data) / "ไม่พบรายการที่ค้นหา" | TC-L05 |
| AC-06 | ค้นโควตาว่าง → "กรุณากรอกรหัสโควตา" | TC-D02 |
| AC-07 | ค้นโควตาที่มีลูกหนี้ → "มีลูกหนี้อยู่แล้ว" + navigate (BR-01) | TC-D01, TC-X01 |
| AC-08 | ค้นโควตาใหม่ → preview + auto-fill ชื่อ/เบอร์ | TC-D03 |
| AC-09 | สร้างไม่มีชื่อ → "กรุณากรอกชื่อเกษตรกร" | TC-D04 |
| AC-10 | สร้างสำเร็จ → "สร้างลูกหนี้สำเร็จ" → detail | TC-D05 |
| AC-11 | header (ชื่อ+id+status) + quick stats 4 | TC-T01 |
| AC-12 | 5 แท็บ (ภาพรวม/ภาระหนี้ N/บัญชีสมุด N/เอกสาร/การตั้งค่า) | TC-T01 |
| AC-13 | แท็บภาระหนี้: table + source badge + ปุ่ม ดู/แก้ไข/ตัดหนี้ | TC-T02 |
| AC-14 | แท็บบัญชีสมุด: double-entry + kind badge + ส่งออก Statement | TC-T03, TC-G01 |
| AC-15 | แท็บการตั้งค่า (ดอก 5.00 / ค่าปรับ 2.00 / simple_daily_365 / % ของยอดสุทธิ) | TC-T06 |
| AC-16 | source=สัญญา ไม่ใส่ contract_id → VR-03 | TC-O03 |
| AC-17 | source=ปรับปรุง ไม่เลือกชนิด → VR-04 | TC-O04 |
| AC-18 | source=ปรับปรุง ไม่อ้างอิง → VR-05 | TC-O05 |
| AC-19 | type=อื่นๆ ไม่ใส่ desc → VR-02 | TC-O02 |
| AC-20 | ต้นทุน ≤ 0 → "จำนวนต้นทุนต้องมากกว่า 0" | TC-O01 |
| AC-21 | disbursement > start_interest → VR-06 | TC-O06 |
| AC-22 | start_interest > maturity → VR-07 | TC-O07 |
| AC-23 | บันทึกสำเร็จ → "บันทึกภาระหนี้สำเร็จ" | TC-O08 |
| AC-24 | จำนวน ≤ 0 → "กรุณากรอกจำนวนเงินที่ถูกต้อง" | TC-P02 |
| AC-25 | ตรวจสอบการจัดสรร → preview + "ตรวจสอบการจัดสรรเรียบร้อย" | TC-P01, TC-P03 |
| AC-26 | waterfall ถูกต้อง (ดอกเบี้ย→ค่าปรับ→ต้นทุน · เรียง priority) | TC-P03 |
| AC-27 | จัดสรรไม่หมด → "เหลือ: X" (overpay) | TC-P06 |
| AC-28 | save ไม่ validate → "กรุณาตรวจสอบการจัดสรรก่อน" | TC-P04 |
| AC-29 | save ไม่มีเลขอ้างอิง → "กรุณากรอกเลขอ้างอิง" | TC-P05 |
| AC-30 | save สำเร็จ → "บันทึกการชำระเรียบร้อย" + ledger(payment) | TC-P01, TC-P07 |
| AC-31 | ไม่ติ๊ก confirm → "กรุณายืนยันการตัดหนี้" | TC-M02 |
| AC-32 | ไม่ใส่เหตุผล → "กรุณากรอกเหตุผลการตัดหนี้" | TC-M03 |
| AC-33 | amount > คงเหลือ → inline "จำนวนเกินยอดคงเหลือ" | TC-M04 |
| AC-34 | amount > 100,000 → "จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ" (DOA) | TC-M05 |
| AC-35 | ตัดสำเร็จ (≤DOA) → "ตัดหนี้เรียบร้อย" + status→ตัดหนี้สูญ | TC-M01, TC-M06 |
| AC-36 | export statement → "สร้างเอกสารเรียบร้อย" | TC-G02 |

### Cross-Module / Event (06_TESTS §6.9) ⭐
| XT | Scenario | Source | cases |
|---|---|---|---|
| XT-01 | สร้างลูกหนี้ → snapshot farmer/quota verified | Quota (read) | TC-X01, TC-D05 |
| XT-02 | obligation source=contract → contract_id + 🔒 · แก้ไม่ได้ (423) | Contract (read) | TC-X02, TC-K01 |
| XT-03 | outstanding อ่านโดย CBM = Σ obligation | → CBM (F-AGM-007) | TC-X03, TC-G03 |
| XT-04 | write-off > DOA → PENDING_APPROVAL (idempotent) | Manager approval | TC-X04 (ต้อง simulate) |
| XT-05 | adjustment reverse → ledger reverse + status reversed (append-only) | append ledger | TC-X05 (ต้อง simulate), TC-K03 |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-DEBT-01 Debtor idempotent per quota (1:1) | TC-D01, TC-X01 |
| BR-DEBT-02 Payment waterfall (priority↑ → ดอกเบี้ย → ค่าปรับ → ต้นเงิน) | TC-P03, TC-P01, TC-P06 |
| BR-DEBT-03 Payment validate-then-save | TC-P01, TC-P04 |
| BR-DEBT-04 Write-off DOA > 100,000 → อนุมัติผู้จัดการ | TC-M05, TC-X04 |
| BR-DEBT-05 Write-off + reason + confirm บังคับ · irreversible | TC-M02, TC-M03 |
| BR-DEBT-06 Contract-sourced = 🔒 locked (immutable) | TC-K01, TC-X02, TC-T02 |
| BR-DEBT-07 Adjustment อ้างอิงรายการเดิม + type · principal ติดลบได้ | TC-O05, TC-K03, TC-N03 |
| BR-DEBT-08 Ledger double-entry append-only | TC-G01, TC-G04 |
| BR-DEBT-09 Aging 0-30/31-60/61-90/90+ (สี) | TC-N01, TC-N02 |
| BR-DEBT-10 outstanding = ledger of record → CBM/Contract read | TC-G03, TC-X03 |
| BR-DEBT-11 Obligation source gating (contract/adjustment/other) | TC-O03, TC-O04, TC-O05, TC-O02 |

### Validation (05_RULES §5.4)
| VR | Message | cases |
|---|---|---|
| VR-01 | "จำนวนต้นทุนต้องมากกว่า 0" | TC-O01 |
| VR-02 | "กรุณากรอกรายละเอียดประเภทอื่นๆ" | TC-O02 |
| VR-03 | "กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น \"จากสัญญา\"" | TC-O03 |
| VR-04 | "กรุณาเลือกชนิดการปรับปรุง" | TC-O04 |
| VR-05 | "การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี)" | TC-O05 |
| VR-06 | "วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย" | TC-O06 |
| VR-07 | "วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด" | TC-O07 |
| VR-08 | "กรุณากรอกจำนวนเงินที่ถูกต้อง" | TC-P02 |
| VR-09 | "กรุณาตรวจสอบการจัดสรรก่อน" | TC-P04 |
| VR-10 | "กรุณากรอกเลขอ้างอิง" | TC-P05 |
| VR-11 | "กรุณายืนยันการตัดหนี้" | TC-M02 |
| VR-12 | "กรุณากรอกเหตุผลการตัดหนี้" | TC-M03 |
| VR-13 | inline "จำนวนเกินยอดคงเหลือ" | TC-M04 |
| VR-14 | "กรุณากรอกรหัสโควตา" | TC-D02 |
| VR-15 | "กรุณากรอกชื่อเกษตรกร" | TC-D04 |

### Edge Cases (05_RULES §5.5)
| EC | Case | cases |
|---|---|---|
| EC-01 | create debtor ซ้ำโควตา → "มีลูกหนี้อยู่แล้ว" → navigate | TC-D01, TC-X01 |
| EC-02 | payment > total outstanding → "เหลือ: X" | TC-P06 |
| EC-03 | payment ไม่กด validate → block | TC-P04 |
| EC-04 | write-off > 100k → banner DOA → PENDING_APPROVAL | TC-M05, TC-X04 |
| EC-05 | write-off amount > outstanding → inline error | TC-M04 |
| EC-06 | edit contract-sourced obligation → 423 LOCKED | TC-K01, TC-X02 |
| EC-07 | adjustment ไม่อ้างอิง → VR-05 | TC-O05 |
| EC-08 | adjustment reduce_principal → principal ติดลบ · reverse → reversed | TC-K03, TC-N03 |
| EC-09 | dates ผิดลำดับ → VR-06/07 | TC-O06, TC-O07 |
| EC-10 | ledger แก้/ลบ → ไม่ได้ (append-only) → reverse entry | TC-G04 |
| EC-11 | outstanding ติดลบ → สีแดง (credit balance) | TC-N03 |
| EC-12 | optimistic stale → 409 CONFLICT_UPDATE_STALE | TC-X06 (ต้อง simulate) |
| EC-13 | idempotent dup payment → 409/no-op | TC-X06 (ต้อง simulate) |

### Error Catalog (05_RULES §5.6 — UI-observable)
| error | cases |
|---|---|
| VALIDATION_FAILED (ต้นทุน/desc/สัญญา/ปรับปรุง/dates/จำนวน/อ้างอิง) | TC-O01..O07, TC-P02, TC-P04, TC-P05, TC-M02..M04, TC-D02, TC-D04 |
| PENDING_APPROVAL(202) "ต้องการอนุมัติจากผู้จัดการ" | TC-M05, TC-X04 (simulate) |
| LOCKED(423) "รายการจากสัญญาแก้ไขไม่ได้" | TC-K01, TC-X02 |
| CONFLICT_UPDATE_STALE(409) "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช" | TC-X06 (simulate) |
| CONFLICT(409) "รายการซ้ำ (idempotent)" | TC-X06 (simulate) |
| FORBIDDEN(403) "ไม่มีสิทธิ์ดำเนินการ" | TC-X06 (simulate) |

### State Machine (05_RULES §5.2)
| entity | ข้อยืนยัน (ย่อ) | cases |
|---|---|---|
| Debtor | active ⇄ suspended → closed(outstanding=0) → written_off | TC-L01 (DEB-0003 ปิด · 0.00) |
| Obligation | active ⇄ suspended → closed(ชำระครบ) → written_off / reversed | TC-M06, TC-K03 |
| Ledger | append-only (immutable) | TC-G01, TC-G04 |

### Permission (05_RULES §5.3)
| cell | cases |
|---|---|
| Debt.Officer (CRUD + payment + write-off ≤DOA) — prototype user เดียวกดได้ทุก action | TC-D05, TC-P07, TC-M01, TC-O08 |
| Debt.Manager (approve >DOA + adjustment/reverse) — RBAC/DOA จริง | TC-X04 (simulate) |
| Contract (write contract-obligation 🔒) · CBM/Contract (read outstanding) | TC-X02, TC-X03 (simulate) |

**Manifest cross-check (FRD §0.12):** AC 36/36 (AC-01..36) · XT-01..05 5/5 · BR-DEBT-01..11 11/11 · VR-01..15 15/15 · EC-01..13 13/13 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — ภาระหนี้แมนนวลถูกต้อง (happy — สร้างบน DEB-2568-0001)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| แหล่งที่มา (source) | **แมนนวล** |
| ประเภทภาระหนี้ (type) | เครื่องจักร |
| จำนวนต้นทุน (บาท) | 40,000 |
| วันที่เบิก | 2568-01-10 |
| วันเริ่มคิดดอกเบี้ย | 2568-01-15 |
| วันครบกำหนด | 2568-06-30 |
| ลำดับ (priority) | 4 |
| อัตราดอกเบี้ย (% ต่อปี) | 5.00 |
| อัตราค่าปรับ (% ต่อปี) | 2.00 |

### ชุด B — ค่าผิดสำหรับ negative (obligation create)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | จำนวนต้นทุน | `0` (source=แมนนวล) | จำนวนต้นทุนต้องมากกว่า 0 |
| B2 | ประเภท=อื่นๆ · รายละเอียด | *(เว้นว่าง)* | กรุณากรอกรายละเอียดประเภทอื่นๆ |
| B3 | แหล่งที่มา=จากสัญญา · รหัสสัญญา | *(เว้นว่าง)* | กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น "จากสัญญา" |
| B4 | แหล่งที่มา=ปรับปรุง · ชนิดการปรับปรุง | *(เว้นว่าง)* | กรุณาเลือกชนิดการปรับปรุง |
| B5 | แหล่งที่มา=ปรับปรุง · อ้างอิง | *(เว้นว่าง ทั้ง obl+ledger)* | การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี) |
| B6 | วันที่เบิก / วันเริ่มดอกเบี้ย | เบิก `2568-02-01` · ดอกเบี้ย `2568-01-15` | วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย |
| B7 | วันเริ่มดอกเบี้ย / วันครบกำหนด | ดอกเบี้ย `2568-07-01` · ครบ `2568-06-30` | วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด |

### ชุด C — Payment allocation (DEB-2568-0001 · จ่าย 30,000)
| ป้าย | ค่า | allocation คาดหวัง |
|---|---|---|
| จำนวนเงิน (บาท) | 30,000 | OBL-2568-0001 → **ดอกเบี้ย 1,500.00 ฿** + **ต้นทุน 28,500.00 ฿** = **รวมจัดสรร 30,000.00 ฿** · เหลือ 0 |
| เลขอ้างอิง | RCPT-30001 | (บังคับก่อน save) |

---

## Test Cases

## Group L — List / search / filter / stats / CSV·Aging (P-01)

### TC-L01 — เปิดหน้า list + 4 stats + คอลัมน์ (happy — AC-01/03)
- group: L · ความสำคัญ: สูงสุด · trace: AC-01, AC-03 / UI loaded
- Setup: seed=default 5 ลูกหนี้ (refresh) · files=—
- Start: OPEN `#/debtors`
- ผ่านเมื่อ: list + stat cards + คอลัมน์แสดงตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/debtors` | — | หัวข้อ **จัดการหนี้ลูกหนี้** + sub "ทะเบียนลูกหนี้ตามโควตา..." · footer **แสดง 5 จาก 5 รายการ** | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **ลูกหนี้ทั้งหมด 5** · **ยอดคงค้างรวม 611,000.00 ฿** · **เกินกำหนด 1** (Aging 90+ วัน) · **ตัดหนี้สูญ 0** | ☐ |
| 3 | VERIFY หัวคอลัมน์ตาราง | — | เรียง: ☑ · **เลขลูกหนี้ · โควตา · ชื่อเกษตรกร · ยอดคงค้าง · ภาระ · Aging · สถานะ · อัปเดตล่าสุด · การกระทำ** | ☐ |
| 4 | VERIFY แถว DEB-2568-0001 | — | โควตา QUO-2568-0001 · สมชาย ไร่ทอง · ยอดคงค้าง **125,000.00** · ภาระ **3** · Aging **31-60 วัน** · สถานะ **ใช้งาน** | ☐ |
| 5 | VERIFY แถว DEB-2568-0003 (ปิด · 0.00) | — | ยอดคงค้าง **0.00** · ภาระ **0** · Aging **—** · สถานะ **ปิด** | ☐ |
| 6 | VERIFY ปุ่ม page header | — | ปุ่ม **ส่งออก CSV** · **รายงาน Aging** · **สร้างลูกหนี้** (primary ขวาบน) | ☐ |

### TC-L02 — ค้นหา โควตา / ชื่อ / เลขลูกหนี้ (happy — AC-02)
- group: L · ความสำคัญ: สูง · trace: AC-02 / search debounce
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "QUO-2568-0004" → ช่องค้นหา (placeholder **ค้นหา โควตา / ชื่อ / เลขลูกหนี้**) | โควตา | เหลือ 1 แถว DEB-2568-0004 (วิไล สวนอ้อย) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** → TYPE "จันทร์" | ชื่อ | เหลือ 1 แถว DEB-2568-0005 (จันทร์ ศรีสุข · QUO-2568-0006) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** → TYPE "DEB-2568-0002" | เลขลูกหนี้ | เหลือ 1 แถว DEB-2568-0002 (บุญมี ทุ่งกว้าง) | ☐ |

### TC-L03 — filter สถานะ (AC-02)
- group: L · ความสำคัญ: สูง · trace: AC-02 / status filter (5 ค่า)
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **ใช้งาน** | — | เหลือ 4 แถว (DEB-0001/0002/0004/0005) · ไม่รวม DEB-0003 (ปิด) | ☐ |
| 2 | SELECT สถานะ = **ปิด** | — | เหลือ 1 แถว DEB-2568-0003 (สถานะ **ปิด**) | ☐ |
| 3 | SELECT สถานะ = **ตัดหนี้สูญ** | — | ตารางว่าง + empty state **ไม่พบรายการที่ค้นหา** (seed ไม่มี written_off) | ☐ |

### TC-L04 — filter Aging (AC-02 / BR-DEBT-09)
- group: L · ความสำคัญ: สูง · trace: AC-02 / aging filter (5 ค่า)
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown Aging = **90+ วัน** | — | เหลือ 1 แถว DEB-2568-0004 (Aging **90+ วัน** · pill สีแดง) | ☐ |
| 2 | SELECT Aging = **61-90 วัน** | — | เหลือ 1 แถว DEB-2568-0005 (Aging **61-90 วัน**) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** | — | กลับ 5 รายการ · dropdown กลับ **ทุกช่วง Aging** | ☐ |

### TC-L05 — empty states (AC-05)
- group: L · ความสำคัญ: สูง · trace: AC-05 / empty (no-data vs filter)
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีลูกหนี้รายนี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK **ล้างตัวกรอง** | — | กลับ 5 รายการ | ☐ |
| 3 | VERIFY (no-data variant): SELECT สถานะ=ตัดหนี้สูญ + Aging=90+ | — | empty state **ไม่พบรายการที่ค้นหา** (filter empty · ไม่ใช่ "ไม่พบลูกหนี้" เพราะมี record ในระบบ) | ☐ |

> หมายเหตุ: empty **ไม่พบลูกหนี้** + ปุ่ม **สร้างลูกหนี้ใหม่** จะโชว์เฉพาะกรณีระบบไม่มีลูกหนี้เลย (all.length===0) — prototype seed มี 5 เสมอ จึงเป็นเคส `(ต้อง simulate)` ที่ระบบเปล่า

### TC-L06 — ส่งออก CSV + รายงาน Aging (AC-04) (บางส่วน ต้อง simulate)
- group: L · ความสำคัญ: กลาง · trace: AC-04 · **prototype: toast จำลอง · ไฟล์จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** → WAIT | — | toast **จำลองส่งออกไฟล์ CSV (5 รายการ)** | ☐ |
| 2 | CLICK ปุ่ม **รายงาน Aging** → WAIT | — | toast **จำลองสร้างรายงาน Aging Summary** | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): ไฟล์ CSV / รายงาน Aging จริง | — | ไฟล์ดาวน์โหลดจริง คอลัมน์ตรงตาราง | ☐ (ต้อง simulate) |

---

## Group D — Debtor create (idempotent + quota search) (OV-01)

### TC-D01 — ค้นโควตาที่มีลูกหนี้แล้ว → "มีลูกหนี้อยู่แล้ว" + navigate (happy — AC-07 / EC-01) ★
- group: D · ความสำคัญ: สูงสุด · trace: AC-07 / BR-DEBT-01 / EC-01 / XT-01
- Setup: seed=default · files=—
- Start: OPEN `#/debtors` → CLICK **สร้างลูกหนี้**
- ผ่านเมื่อ: idempotent — เด้งไป detail เดิม ไม่สร้างซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างลูกหนี้** | — | drawer **สร้างลูกหนี้จากโควตา** เปิด · ช่องค้นหาโควตา placeholder **พิมพ์เลขโควตา หรือ ชื่อเกษตรกร** | ☐ |
| 2 | TYPE "QUO-2568-0001" → CLICK ปุ่ม **ค้นหา** → WAIT | — | toast **มีลูกหนี้อยู่แล้ว** · drawer ปิด · navigate ไป **#/debtors/DEB-2568-0001** (detail เปิด) | ☐ |
| 3 | VERIFY count list | — | ยัง **5 รายการ** (ไม่สร้างลูกหนี้ซ้ำ · 1:1 quota) | ☐ |

### TC-D02 — ค้นโควตาว่าง → "กรุณากรอกรหัสโควตา" (negative — AC-06 / VR-14)
- group: D · ความสำคัญ: สูง · trace: AC-06 / VR-14
- Setup: seed=default · files=—
- Start: OPEN `#/debtors` → CLICK **สร้างลูกหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้นช่องค้นหาโควตาว่าง → CLICK ปุ่ม **ค้นหา** | — | toast/warning **กรุณากรอกรหัสโควตา** · ไม่แสดง preview | ☐ |

### TC-D03 — ค้นโควตาใหม่ (ยังไม่มีลูกหนี้) → preview + auto-fill (happy — AC-08)
- group: D · ความสำคัญ: สูง · trace: AC-08 / quota search verified
- Setup: seed=default · files=—
- Start: OPEN `#/debtors` → CLICK **สร้างลูกหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "QUO-2568-0005" → CLICK **ค้นหา** → WAIT | — | ปรากฏ section **ข้อมูลลูกหนี้** · ช่อง **ชื่อเกษตรกร** auto-fill = **มานพ นำทาง** · **เบอร์** = **0865556666** | ☐ |
| 2 | VERIFY: ค้นด้วยชื่อได้ | ล้าง → TYPE "มานพ" → CLICK **ค้นหา** | เจอ QUO-2568-0005 เช่นเดียวกัน (ค้นด้วยชื่อเกษตรกร) | ☐ |
| 3 | VERIFY: ค้นไม่พบ | ล้าง → TYPE "QUO-9999" → CLICK **ค้นหา** | toast **ไม่พบโควตาที่ค้นหา** · ไม่แสดง preview | ☐ |

### TC-D04 — สร้างไม่มีชื่อ → "กรุณากรอกชื่อเกษตรกร" (negative — AC-09 / VR-15)
- group: D · ความสำคัญ: สูง · trace: AC-09 / VR-15
- Setup: seed=default · files=—
- Start: OPEN `#/debtors` → CLICK **สร้างลูกหนี้** → ค้น QUO-2568-0005

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ลบค่าในช่อง **ชื่อเกษตรกร** ให้ว่าง → CLICK **สร้างลูกหนี้** | — | block + toast **กรุณากรอกชื่อเกษตรกร** · field ติด is-invalid · ไม่สร้าง | ☐ |

### TC-D05 — สร้างลูกหนี้สำเร็จ → detail (happy — AC-10 / XT-01) ★
- group: D · ความสำคัญ: สูงสุด · trace: AC-10 / XT-01 / BR-DEBT-01
- Setup: seed=default · files=—
- Start: OPEN `#/debtors` → CLICK **สร้างลูกหนี้** → ค้น QUO-2568-0005

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ค้น **QUO-2568-0005** → auto-fill มานพ นำทาง · 0865556666 | — | section ข้อมูลลูกหนี้แสดงค่าครบ | ☐ |
| 2 | CLICK ปุ่ม **สร้างลูกหนี้** → WAIT | — | drawer ปิด + toast **สร้างลูกหนี้สำเร็จ** · navigate ไป detail ลูกหนี้ใหม่ **DEB-2568-0006** (สถานะ ใช้งาน · ยอดคงค้าง 0.00) | ☐ |
| 3 | กลับ list → VERIFY | — | count = **6 รายการ** · การ์ดลูกหนี้ทั้งหมด = 6 · แถวใหม่ผูก QUO-2568-0005 | ☐ |

---

## Group T — Debtor detail 5 tabs (P-02)

### TC-T01 — Detail header + quick stats + 5 tabs (AC-11/12)
- group: T · ความสำคัญ: สูง · trace: AC-11, AC-12 / drawer 5 tabs
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001`
- ผ่านเมื่อ: header + quick stats 4 + 5 แท็บ ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/debtors/DEB-2568-0001` | — | drawer เปิด · eyebrow **ลูกหนี้ · DEB-2568-0001** · title **สมชาย ไร่ทอง** + status pill **ใช้งาน** · sub **โควตา: QUO-2568-0001 · 0812345678** | ☐ |
| 2 | VERIFY quick stats (4) | — | **ยอดคงค้างรวม 125,000.00** · **จำนวนภาระหนี้ 3** · **Aging 31-60 วัน** · **อัปเดตล่าสุด** (วันเวลา) | ☐ |
| 3 | VERIFY แถบแท็บ | — | 5 แท็บ: **ภาพรวม · ภาระหนี้ (3) · บัญชีสมุด (4) · เอกสาร · การตั้งค่า** · ปุ่ม header **บันทึกการชำระ** + **สร้างภาระหนี้** | ☐ |
| 4 | VERIFY แท็บ ภาพรวม (default) | — | section **ข้อมูลติดต่อ** (ชื่อ/โควตา/เบอร์/ป้ายกำกับ คิว1, ฤดูแล้ง2568) + section **สถิติ** (คงค้าง/ภาระ/Aging/สถานะ) | ☐ |

### TC-T02 — แท็บ ภาระหนี้: table + source badge + actions (AC-13 / BR-DEBT-06)
- group: T · ความสำคัญ: สูง · trace: AC-13 / source badge (สัญญา🔒/แมนนวล/ปรับปรุง)
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK แท็บ **ภาระหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ภาระหนี้** | — | table 3 แถว · หัวคอลัมน์ ID · แหล่งที่มา · ประเภท · ต้นทุน · ดอกเบี้ยสะสม · ค่าปรับ · คงเหลือ · ลำดับ · สถานะ · วันครบกำหนด · การกระทำ | ☐ |
| 2 | VERIFY แถว OBL-2568-0001 | — | badge **สัญญา** + ไอคอน 🔒 · sub CNT-2568-0011 · ต้นทุน 70,000.00 · คงเหลือ 71,500.00 · ลำดับ 1 | ☐ |
| 3 | VERIFY แถว OBL-2568-0002 / OBL-2568-0003 | — | OBL-0002 badge **แมนนวล** · OBL-0003 badge **ปรับปรุง** (คงเหลือ **-3,000.00** สีแดง) | ☐ |
| 4 | VERIFY row-actions ต่อแถว | — | ปุ่ม **ดู** (eye) · **แก้ไข** (pencil) · **ตัดหนี้** (scissors) ครบ (OBL ที่ยังไม่ตัดหนี้สูญ) | ☐ |

### TC-T03 — แท็บ บัญชีสมุด: double-entry + kind badge (AC-14 / BR-DEBT-08)
- group: T · ความสำคัญ: สูง · trace: AC-14 / double-entry
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK แท็บ **บัญชีสมุด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **บัญชีสมุด (4)** | — | หัวคอลัมน์ ID · วันที่ · ประเภท · **เดบิต · เครดิต · คงเหลือ** · หมายเหตุ · ปุ่ม **ส่งออก Statement** (ขวาบน) | ☐ |
| 2 | VERIFY แถว LED-2568-0001 / LED-2568-0002 | — | LED-0001 kind **ตั้งหนี้** เดบิต 70,000.00 คงเหลือ 70,000.00 · LED-0002 kind **ดอกเบี้ย** เดบิต 1,500.00 คงเหลือ 71,500.00 | ☐ |
| 3 | VERIFY แถว LED-2568-0004 (ชำระ) | — | kind **ชำระ** · เดบิต **-** · เครดิต **8,000.00** · คงเหลือ 118,500.00 | ☐ |

### TC-T04 — แท็บ เอกสาร (empty) (AC-12)
- group: T · ความสำคัญ: กลาง · trace: AC-12 / documents placeholder
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK แท็บ **เอกสาร**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **เอกสาร** | — | empty state **ยังไม่มีเอกสาร** + ปุ่ม **อัปโหลดเอกสาร** | ☐ |

### TC-T05 — ภาระหนี้ว่าง (empty) + ปิด drawer (AC-12)
- group: T · ความสำคัญ: กลาง · trace: AC-12 / empty obligations · DEB-0003 (0 ภาระ)
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0003` → CLICK แท็บ **ภาระหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY quick stats DEB-2568-0003 | — | ยอดคงค้างรวม **0.00** · จำนวนภาระหนี้ **0** · สถานะ **ปิด** | ☐ |
| 2 | CLICK แท็บ **ภาระหนี้ (0)** | — | empty state **ยังไม่มีภาระหนี้** + ปุ่ม **สร้างภาระหนี้** | ☐ |
| 3 | CLICK ปุ่ม **ปิด** (footer) | — | drawer ปิด · กลับ `#/debtors` (list 5 รายการ) | ☐ |

### TC-T06 — แท็บ การตั้งค่า (ค่าเริ่มต้น) (AC-15)
- group: T · ความสำคัญ: สูง · trace: AC-15 / settings defaults
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK แท็บ **การตั้งค่า**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **การตั้งค่า** | — | section **ค่าเริ่มต้น** · **อัตราดอกเบี้ย (ต่อปี) 5.00%** · **อัตราค่าปรับ (ต่อปี) 2.00%** · **วิธีคำนวณ simple_daily_365** · **กติกาการหักหนี้ % ของยอดสุทธิ** | ☐ |

---

## Group O — Obligation create (source gating + type + dates) (OV-02)

### TC-O01 — ต้นทุน ≤ 0 → block (negative — AC-20 / VR-01)
- group: O · ความสำคัญ: สูง · trace: AC-20 / VR-01
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกแหล่งที่มา **แมนนวล** · ประเภท เครื่องจักร · จำนวนต้นทุน **0** → CLICK **บันทึกภาระหนี้** | B1 | toast/warning **จำนวนต้นทุนต้องมากกว่า 0** · ไม่บันทึก | ☐ |

### TC-O02 — ประเภท=อื่นๆ ไม่ใส่รายละเอียด → block (negative — AC-19 / VR-02)
- group: O · ความสำคัญ: สูง · trace: AC-19 / VR-02
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | แหล่งที่มา แมนนวล · จำนวนต้นทุน 10,000 · ประเภท **อื่นๆ** · เว้นรายละเอียดว่าง → CLICK **บันทึกภาระหนี้** | B2 | warning **กรุณากรอกรายละเอียดประเภทอื่นๆ** · ไม่บันทึก | ☐ |

### TC-O03 — source=สัญญา ไม่ใส่ contract_id → block (negative — AC-16 / VR-03)
- group: O · ความสำคัญ: สูงสุด · trace: AC-16 / VR-03 / BR-DEBT-11
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | แหล่งที่มา **จากสัญญา** · จำนวนต้นทุน 20,000 · ประเภท ปุ๋ย · เว้น **รหัสสัญญา** ว่าง → CLICK **บันทึกภาระหนี้** | B3 | warning **กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น "จากสัญญา"** · ไม่บันทึก | ☐ |

### TC-O04 — source=ปรับปรุง ไม่เลือกชนิด → block (negative — AC-17 / VR-04)
- group: O · ความสำคัญ: สูง · trace: AC-17 / VR-04 / BR-DEBT-11
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | แหล่งที่มา **ปรับปรุง** · จำนวนต้นทุน -2,000 · เว้น **ชนิดการปรับปรุง** ว่าง → CLICK **บันทึกภาระหนี้** | B4 | warning **กรุณาเลือกชนิดการปรับปรุง** · ไม่บันทึก | ☐ |

### TC-O05 — source=ปรับปรุง ไม่อ้างอิงรายการเดิม → block (negative — AC-18 / VR-05 / EC-07)
- group: O · ความสำคัญ: สูง · trace: AC-18 / VR-05 / EC-07 / BR-DEBT-07
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | แหล่งที่มา **ปรับปรุง** · เลือกชนิดการปรับปรุง · จำนวนต้นทุน -2,000 · เว้น **อ้างอิงภาระหนี้เดิม + รายการสมุดบัญชี** ว่างทั้งคู่ → CLICK **บันทึกภาระหนี้** | B5 | warning **การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี)** · ไม่บันทึก | ☐ |

### TC-O06 — วันที่เบิก > วันเริ่มคิดดอกเบี้ย → block (negative — AC-21 / VR-06 / EC-09)
- group: O · ความสำคัญ: สูง · trace: AC-21 / VR-06 / EC-09
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | แหล่งที่มา แมนนวล · ประเภท เครื่องจักร · ต้นทุน 30,000 · **วันที่เบิก 2568-02-01** · **วันเริ่มคิดดอกเบี้ย 2568-01-15** → CLICK **บันทึกภาระหนี้** | B6 | warning **วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย** · ไม่บันทึก | ☐ |

### TC-O07 — วันเริ่มคิดดอกเบี้ย > วันครบกำหนด → block (negative — AC-22 / VR-07 / EC-09)
- group: O · ความสำคัญ: สูง · trace: AC-22 / VR-07 / EC-09
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: B7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | แหล่งที่มา แมนนวล · ต้นทุน 30,000 · วันที่เบิก 2568-01-10 · **วันเริ่มคิดดอกเบี้ย 2568-07-01** · **วันครบกำหนด 2568-06-30** → CLICK **บันทึกภาระหนี้** | B7 | warning **วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด** · ไม่บันทึก | ☐ |

### TC-O08 — สร้างภาระหนี้แมนนวลสำเร็จ (happy — AC-23) ★
- group: O · ความสำคัญ: สูงสุด · trace: AC-23 / BR-DEBT-08 (ledger charge)
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **สร้างภาระหนี้**
- ชุดข้อมูล: A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอกชุด A: แหล่งที่มา แมนนวล · ประเภท เครื่องจักร · ต้นทุน 40,000 · เบิก 2568-01-10 · ดอกเบี้ย 2568-01-15 · ครบ 2568-06-30 · ลำดับ 4 → CLICK **บันทึกภาระหนี้** → WAIT | A | drawer ปิด + toast **บันทึกภาระหนี้สำเร็จ** | ☐ |
| 2 | VERIFY แท็บ ภาระหนี้ + quick stats | — | ภาระใหม่ **OBL-2568-0009** badge **แมนนวล** · คงเหลือ 40,000.00 · จำนวนภาระหนี้ = **4** · ยอดคงค้างรวม = **165,000.00** | ☐ |
| 3 | VERIFY แท็บ บัญชีสมุด | — | มีแถว ledger ใหม่ kind **ตั้งหนี้** เดบิต 40,000.00 (double-entry append) | ☐ |

---

## Group P — Manual payment (waterfall · validate-then-save) (OV-03) ⭐

### TC-P01 — บันทึกการชำระ waterfall สำเร็จ (happy — AC-25/30) ★
- group: P · ความสำคัญ: สูงสุด · trace: AC-25, AC-30 / BR-DEBT-02/03
- Setup: seed=default (DEB-0001 คงค้าง 125,000) · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **บันทึกการชำระ**
- ชุดข้อมูล: C
- ผ่านเมื่อ: validate → allocation ถูกต้อง → save สำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกการชำระ** | — | modal **บันทึกการชำระเงิน** · sub "สมชาย ไร่ทอง · คงค้าง 125,000.00" · ปุ่ม **บันทึกการชำระ** disabled | ☐ |
| 2 | TYPE จำนวนเงิน **30,000** · วิธี เงินสด | C | (ยังไม่แสดง allocation จนกด ตรวจสอบ) | ☐ |
| 3 | CLICK ปุ่ม **ตรวจสอบการจัดสรร** → WAIT | — | toast **ตรวจสอบการจัดสรรเรียบร้อย** · ตาราง allocation: OBL-2568-0001 **ดอกเบี้ย 1,500.00** + **ต้นทุน 28,500.00** · **รวมจัดสรร 30,000.00** | ☐ |
| 4 | TYPE เลขอ้างอิง **RCPT-30001** → ปุ่ม บันทึกการชำระ เปิด → CLICK **บันทึกการชำระ** → WAIT | C | modal ปิด + toast **บันทึกการชำระเรียบร้อย** | ☐ |
| 5 | VERIFY แท็บ บัญชีสมุด + quick stats | — | มีแถว ledger kind **ชำระ** เครดิต 30,000.00 · ยอดคงค้างรวม DEB-0001 ลดเหลือ **95,000.00** | ☐ |

### TC-P02 — จำนวน ≤ 0 → block (negative — AC-24 / VR-08)
- group: P · ความสำคัญ: สูง · trace: AC-24 / VR-08
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **บันทึกการชำระ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE จำนวนเงิน **0** → CLICK **ตรวจสอบการจัดสรร** | — | warning **กรุณากรอกจำนวนเงินที่ถูกต้อง** · ไม่แสดง allocation | ☐ |

### TC-P03 — waterfall ตาม priority + ดอกเบี้ย→ค่าปรับ→ต้นทุน (AC-26 / BR-DEBT-02)
- group: P · ความสำคัญ: สูงสุด · trace: AC-26 / BR-DEBT-02 / allocation signature
- Setup: seed=default (DEB-0004 · OBL-0006 มีดอกเบี้ย 5,000 + ค่าปรับ 2,000) · files=—
- Start: OPEN `#/debtors/DEB-2568-0004` → CLICK **บันทึกการชำระ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE จำนวนเงิน **10,000** → CLICK **ตรวจสอบการจัดสรร** → WAIT | — | allocation OBL-2568-0006 (priority 1): **ดอกเบี้ย 5,000.00** → **ค่าปรับ 2,000.00** → **ต้นทุน 3,000.00** · รวมจัดสรร **10,000.00** (ยืนยันลำดับ ดอกเบี้ย ก่อน ค่าปรับ ก่อน ต้นทุน) | ☐ |
| 2 | VERIFY: ไม่จัดสรรข้าม priority | — | OBL-2568-0007 (priority 2) **ยังไม่ถูกจัดสรร** (10,000 หมดที่ OBL-0006 ก่อน) | ☐ |

### TC-P04 — save ไม่กด ตรวจสอบ → block (negative — AC-28 / VR-09 / EC-03)
- group: P · ความสำคัญ: สูง · trace: AC-28 / VR-09 / EC-03 / BR-DEBT-03
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **บันทึกการชำระ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE จำนวนเงิน 30,000 + เลขอ้างอิง RCPT-1 (ยังไม่กด ตรวจสอบการจัดสรร) | — | ปุ่ม **บันทึกการชำระ** ยัง disabled (ต้อง validated ก่อน) | ☐ |
| 2 | (ยิง submitPayment ตรง ๆ ผ่าน guard โดยยังไม่ validate) | — | block + warning **กรุณาตรวจสอบการจัดสรรก่อน** | ☐ |

### TC-P05 — save ไม่มีเลขอ้างอิง → block (negative — AC-29 / VR-10)
- group: P · ความสำคัญ: สูง · trace: AC-29 / VR-10
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → CLICK **บันทึกการชำระ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE จำนวนเงิน 30,000 → CLICK **ตรวจสอบการจัดสรร** (validated) → เว้นเลขอ้างอิงว่าง | — | ปุ่ม **บันทึกการชำระ** ยัง disabled (require reference) | ☐ |
| 2 | (ยิง submitPayment ตรง ๆ โดยไม่มีเลขอ้างอิง) | — | block + warning **กรุณากรอกเลขอ้างอิง** | ☐ |

### TC-P06 — จ่ายเกินยอด → "เหลือ: X" (overpay — AC-27 / EC-02)
- group: P · ความสำคัญ: สูง · trace: AC-27 / EC-02
- Setup: seed=default (DEB-0002 คงค้างรวม 85,000) · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → CLICK **บันทึกการชำระ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE จำนวนเงิน **90,000** → CLICK **ตรวจสอบการจัดสรร** → WAIT | — | allocation จัดสรรจนหมด: OBL-0004 (ดอกเบี้ย 300 + ต้นทุน 45,000) + OBL-0005 (ดอกเบี้ย 200 + ต้นทุน 39,500) · **รวมจัดสรร 85,000.00** · แถบเตือน **เหลือ: 5,000.00 (เกินยอดคงค้าง — ส่วนที่เหลือไม่ถูกจัดสรร)** | ☐ |

### TC-P07 — วิธีชำระ + ledger note (AC-30)
- group: P · ความสำคัญ: กลาง · trace: AC-30 / วิธี เงินสด/โอนเงิน/หักกลบ
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → CLICK **บันทึกการชำระ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกวิธีชำระ **โอนเงิน** · จำนวน 10,000 → CLICK **ตรวจสอบการจัดสรร** → เลขอ้างอิง SLIP-01 → CLICK **บันทึกการชำระ** → WAIT | — | toast **บันทึกการชำระเรียบร้อย** | ☐ |
| 2 | VERIFY แท็บ บัญชีสมุด แถวใหม่ | — | kind **ชำระ** · หมายเหตุมีคำว่า **โอนเงิน · อ้างอิง SLIP-01** · เครดิต 10,000.00 (double-entry) | ☐ |

---

## Group M — Write-off (DOA 100k gate) (OV-04) ⭐

### TC-M01 — ตัดหนี้ปกติ (≤DOA) สำเร็จ (happy — AC-35) ★
- group: M · ความสำคัญ: สูงสุด · trace: AC-35 / BR-DEBT-04 (≤100k) / BR-DEBT-05
- Setup: seed=default (OBL-2568-0004 คงเหลือ 45,300 ≤ 100,000) · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → แท็บ **ภาระหนี้** → row OBL-2568-0004 CLICK **ตัดหนี้**
- ผ่านเมื่อ: ≤DOA → ไม่มี warning · ตัดสำเร็จ · status→ตัดหนี้สูญ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตัดหนี้** บน OBL-2568-0004 | — | modal **ตัดหนี้สูญ** · alert irreversible · ยอดคงเหลือ **45,300.00** · จำนวนที่ตัด default 45,300 | ☐ |
| 2 | TYPE เหตุผล "หนี้สูญตามมติคณะกรรมการ" → ติ๊ก **confirm** checkbox → CLICK **ยืนยันตัดหนี้** → WAIT | — | modal ปิด + toast **ตัดหนี้เรียบร้อย** (ไม่มี warning DOA เพราะ 45,300 ≤ 100,000) | ☐ |
| 3 | VERIFY แท็บ ภาระหนี้ | — | OBL-2568-0004 สถานะ pill = **ตัดหนี้สูญ** · ไม่มีปุ่ม ตัดหนี้ แถวนั้นแล้ว | ☐ |

### TC-M02 — ไม่ติ๊ก confirm → block (negative — AC-31 / VR-11)
- group: M · ความสำคัญ: สูง · trace: AC-31 / VR-11 / BR-DEBT-05
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → แท็บ ภาระหนี้ → OBL-2568-0005 CLICK **ตัดหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE เหตุผล "ทดสอบ" · **ไม่ติ๊ก confirm** | — | ปุ่ม **ยืนยันตัดหนี้** ยัง disabled | ☐ |
| 2 | (ยิง submitWriteoff ตรง ๆ โดยไม่ติ๊ก confirm) | — | block + warning **กรุณายืนยันการตัดหนี้** | ☐ |

### TC-M03 — ไม่ใส่เหตุผล → block (negative — AC-32 / VR-12)
- group: M · ความสำคัญ: สูง · trace: AC-32 / VR-12 / BR-DEBT-05
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → แท็บ ภาระหนี้ → OBL-2568-0005 CLICK **ตัดหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ติ๊ก **confirm** · **เว้นเหตุผลว่าง** | — | ปุ่ม **ยืนยันตัดหนี้** ยัง disabled (require reason) | ☐ |
| 2 | (ยิง submitWriteoff ตรง ๆ โดยเหตุผลว่าง) | — | block + warning **กรุณากรอกเหตุผลการตัดหนี้** | ☐ |

### TC-M04 — จำนวนเกินยอดคงเหลือ → inline error (negative — AC-33 / VR-13 / EC-05)
- group: M · ความสำคัญ: สูง · trace: AC-33 / VR-13 / EC-05
- Setup: seed=default (OBL-2568-0005 คงเหลือ 39,700) · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → แท็บ ภาระหนี้ → OBL-2568-0005 CLICK **ตัดหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE จำนวนที่ตัด **50,000** (> คงเหลือ 39,700) | — | inline error ใต้ช่อง **จำนวนเกินยอดคงเหลือ** (สีแดง) | ☐ |
| 2 | VERIFY ปุ่ม ยืนยันตัดหนี้ | — | ปุ่ม disabled / ไม่สามารถตัดได้ขณะเกินยอด | ☐ |

### TC-M05 — จำนวน > 100,000 → DOA warning (AC-34 / BR-DEBT-04 / EC-04)
- group: M · ความสำคัญ: สูงสุด · trace: AC-34 / EC-04 · **prototype: warning แสดง แต่ยังตัดได้ · PENDING_APPROVAL จริง = SIT**
- Setup: seed=default (OBL-2568-0006 คงเหลือ 145,000 > 100,000) · files=—
- Start: OPEN `#/debtors/DEB-2568-0004` → แท็บ ภาระหนี้ → OBL-2568-0006 CLICK **ตัดหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal | — | ยอดคงเหลือ **145,000.00** · จำนวนที่ตัด default 145,000 | ☐ |
| 2 | ติ๊ก confirm + เหตุผล "หนี้สูญเกิน DOA" → CLICK **ยืนยันตัดหนี้** → WAIT | — | warning **จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ** (DOA · > 100,000) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): PENDING_APPROVAL(202) | — | ระบบจริง → เข้าคิวรออนุมัติผู้จัดการ (ยังไม่ตัดจริง) · prototype = ตัดต่อได้เลย (mock) | ☐ (ต้อง simulate) |

### TC-M06 — write-off → ledger(write_off) + status (AC-35 / BR-DEBT-08)
- group: M · ความสำคัญ: สูง · trace: AC-35 / ledger append · obligation → written_off
- Setup: seed=default (OBL-2568-0005 คงเหลือ 39,700 ≤ DOA) · files=—
- Start: OPEN `#/debtors/DEB-2568-0002` → แท็บ ภาระหนี้ → OBL-2568-0005 CLICK **ตัดหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ติ๊ก confirm + เหตุผล "ตัดหนี้ตามมติ" · จำนวน 39,700 → CLICK **ยืนยันตัดหนี้** → WAIT | — | toast **ตัดหนี้เรียบร้อย** · OBL-2568-0005 สถานะ **ตัดหนี้สูญ** | ☐ |
| 2 | VERIFY แท็บ บัญชีสมุด | — | มีแถว ledger kind **ตัดหนี้สูญ** เครดิต 39,700.00 (double-entry append) · ยอดคงค้างรวม DEB-0002 ลดลง | ☐ |

---

## Group G — Ledger / double-entry / export Statement (OV-05)

### TC-G01 — ledger double-entry 4 แถว seed (AC-14 / BR-DEBT-08)
- group: G · ความสำคัญ: สูง · trace: AC-14 / BR-DEBT-08 / balance_after
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **บัญชีสมุด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 4 แถว ledger seed | — | LED-0001 ตั้งหนี้ dr70,000 bal70,000 · LED-0002 ดอกเบี้ย dr1,500 bal71,500 · LED-0003 ตั้งหนี้ dr55,000 bal126,500 · LED-0004 ชำระ cr8,000 bal118,500 | ☐ |
| 2 | VERIFY kind badge | — | badge ต่างสี: ตั้งหนี้ (outline) · ดอกเบี้ย (info) · ชำระ (success) | ☐ |

### TC-G02 — ส่งออก Statement → "สร้างเอกสารเรียบร้อย" (AC-36) (บางส่วน ต้อง simulate)
- group: G · ความสำคัญ: สูง · trace: AC-36 · **prototype: toast จำลอง · PDF จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **บัญชีสมุด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก Statement** → WAIT | — | toast **สร้างเอกสารเรียบร้อย** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): PDF Statement ไทย | — | เอกสาร PDF ภาษาไทยจริงถูกสร้าง (prototype = mock toast) | ☐ (ต้อง simulate) |

### TC-G03 — outstanding = Σ obligation (ledger of record) (XT-03 / BR-DEBT-10)
- group: G · ความสำคัญ: สูง · trace: XT-03 / BR-DEBT-10 / outstanding invariant
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **ภาระหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | คำนวณ Σ คงเหลือของภาระ | — | 71,500 + 56,500 + (-3,000) = **125,000.00** | ☐ |
| 2 | VERIFY quick stats ยอดคงค้างรวม | — | **125,000.00** (ตรงกับ Σ obligation · outstanding = ledger of record) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): CBM (F-AGM-007) อ่าน outstanding | — | debtor_outstanding ที่ CBM = 125,000.00 (feed จริง = SIT) | ☐ (ต้อง simulate) |

### TC-G04 — ledger append-only (แก้/ลบไม่ได้) (EC-10 / BR-DEBT-08)
- group: G · ความสำคัญ: กลาง · trace: EC-10 / BR-DEBT-08 / immutable
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **บัญชีสมุด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY: ตาราง ledger ไม่มีปุ่ม แก้ไข/ลบ ต่อแถว | — | ไม่มี row-action แก้/ลบ ในแท็บบัญชีสมุด (append-only · immutable) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): แก้ไข ledger → ปฏิเสธ · ต้องออก reverse entry | — | ระบบจริงไม่ยอม UPDATE/DELETE · การแก้ = append reverse (kind ย้อนรายการ) | ☐ (ต้อง simulate) |

---

## Group K — Contract-lock & adjustment (OV-06)

### TC-K01 — แก้ไขภาระจากสัญญา → "รายการจากสัญญาแก้ไขไม่ได้" (negative — EC-06 / XT-02 / BR-DEBT-06)
- group: K · ความสำคัญ: สูง · trace: EC-06 / XT-02 / BR-DEBT-06 (423 LOCKED)
- Setup: seed=default (OBL-2568-0001 source=สัญญา 🔒) · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **ภาระหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **แก้ไข** (pencil) บน OBL-2568-0001 (badge สัญญา 🔒) | — | toast/warning **รายการจากสัญญาแก้ไขไม่ได้** · ไม่เปิดฟอร์มแก้ | ☐ |
| 2 | VERIFY: แก้ไขภาระแมนนวลได้ | CLICK **แก้ไข** บน OBL-2568-0002 (แมนนวล) | เปิด flow แก้ (prototype toast **เปิดฟอร์มแก้ไขภาระหนี้ (ตัวอย่าง)**) — ไม่ถูก lock | ☐ |

### TC-K02 — ดูภาระ (read-only view) จากสัญญา (AC-13 / BR-DEBT-06)
- group: K · ความสำคัญ: กลาง · trace: AC-13 / obligation view modal
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **ภาระหนี้** → OBL-2568-0001 CLICK **ดู**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ดู** (eye) บน OBL-2568-0001 | — | modal read-only แสดง คงเหลือ 71,500.00 · รหัสสัญญา CNT-2568-0011 · อัตราดอกเบี้ย 5.00% · วันที่เบิก/วันเริ่มดอกเบี้ย/วันครบกำหนด | ☐ |

### TC-K03 — adjustment (ปรับปรุง) อ้างอิงรายการเดิม · principal ติดลบ (EC-08 / BR-DEBT-07 / XT-05)
- group: K · ความสำคัญ: สูง · trace: EC-08 / BR-DEBT-07 / XT-05 · **reverse จริง append-only = SIT**
- Setup: seed=default (OBL-2568-0003 ปรับปรุง · principal -5,000 · ref OBL-0001/LED-0004) · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **ภาระหนี้** → OBL-2568-0003 CLICK **ดู**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY OBL-2568-0003 | — | badge **ปรับปรุง** · ประเภท "อื่นๆ · ปรับลดต้นเงินตามข้อตกลงประนอมหนี้" · ต้นทุน **-5,000.00** · คงเหลือ **-3,000.00** (แดง) · อ้างอิงภาระหนี้ OBL-2568-0001 | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): adjustment reverse | — | reverse → append ledger kind **ย้อนรายการ** + obligation status **ย้อนรายการ** (append-only · ไม่แก้ของเดิม) | ☐ (ต้อง simulate) |

---

## Group N — Aging & negative outstanding (OV-07)

### TC-N01 — Aging pill สี ตาม bucket (BR-DEBT-09)
- group: N · ความสำคัญ: กลาง · trace: BR-DEBT-09 / aging pill 4 สี
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Aging pill รายแถว | — | DEB-0001 **31-60 วัน** (เหลือง) · DEB-0002 **0-30 วัน** (เขียว) · DEB-0004 **90+ วัน** (แดง) · DEB-0005 **61-90 วัน** (ส้ม) · DEB-0003 **—** (muted) | ☐ |

### TC-N02 — filter Aging 90+ → เกินกำหนด (AC-02 / BR-DEBT-09)
- group: N · ความสำคัญ: กลาง · trace: AC-02 / เกินกำหนด = aging 90+
- Setup: seed=default · files=—
- Start: OPEN `#/debtors`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT Aging = **90+ วัน** | — | เหลือ 1 แถว DEB-2568-0004 · ตรงกับ stat card **เกินกำหนด 1** | ☐ |

### TC-N03 — ยอดคงค้างติดลบ = แดง (AC-03 / EC-11 / EC-08)
- group: N · ความสำคัญ: กลาง · trace: AC-03 / EC-11 / negative red
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **ภาระหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY OBL-2568-0003 คอลัมน์ ต้นทุน + คงเหลือ | — | ต้นทุน **-5,000.00** และ คงเหลือ **-3,000.00** แสดง **สีแดง** (credit balance · principal ติดลบจาก adjustment) | ☐ |

---

## Group X — Cross-module / event XT-01..05 + simulate (06_TESTS §6.9) ⭐

### TC-X01 — สร้างลูกหนี้ → snapshot farmer/quota (XT-01) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-07/10 / BR-DEBT-01
- Setup: seed=default · files=—
- Start: OPEN `#/debtors` → CLICK **สร้างลูกหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ค้น **QUO-2568-0005** → auto-fill มานพ นำทาง · 0865556666 → CLICK **สร้างลูกหนี้** → WAIT | — | toast **สร้างลูกหนี้สำเร็จ** · detail snapshot ผูกโควตา QUO-2568-0005 · ชื่อ = มานพ นำทาง (ตรงต้นทาง Quota) | ☐ |
| 2 | VERIFY: idempotent — ค้น QUO-2568-0001 (มีลูกหนี้) | ค้นซ้ำ | toast **มีลูกหนี้อยู่แล้ว** + navigate detail เดิม (ไม่สร้างซ้ำ) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): Quota read-only | — | Quota (F-AGM-002) verified · GET only · ไม่มี write-back | ☐ (ต้อง simulate) |

### TC-X02 — obligation source=contract → contract_id + 🔒 locked (XT-02)
- group: X · ความสำคัญ: สูง · trace: XT-02 / EC-06 / BR-DEBT-06 (423)
- Setup: seed=default (OBL-2568-0001 contract 🔒) · files=—
- Start: OPEN `#/debtors/DEB-2568-0001` → แท็บ **ภาระหนี้**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY OBL-2568-0001 | — | badge **สัญญา** 🔒 · contract_id **CNT-2568-0011** แสดง (จาก Contract F-AGM-005) | ☐ |
| 2 | CLICK **แก้ไข** | — | **รายการจากสัญญาแก้ไขไม่ได้** (423 LOCKED) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): write contract-obligation | — | เฉพาะ Contract role เขียนได้ · ที่ Debt = immutable | ☐ (ต้อง simulate) |

### TC-X03 — outstanding อ่านโดย CBM = Σ obligation (XT-03)
- group: X · ความสำคัญ: สูงสุด · trace: XT-03 / BR-DEBT-10 · **feed จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/debtors/DEB-2568-0004`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY DEB-2568-0004 ยอดคงค้างรวม | — | **245,000.00** = Σ obligation (OBL-0006 145,000 + OBL-0007 100,000) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): CBM (F-AGM-007) อ่าน debtor_outstanding | — | ยอดที่ CBM = 245,000.00 ตรงกับ Debt (ledger of record) | ☐ (ต้อง simulate) |

### TC-X04 — write-off > DOA → PENDING_APPROVAL (idempotent) (XT-04 / EC-04) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-04 / EC-04 / BR-DEBT-04 · **prototype: warning แสดง แต่ยังตัดได้ (ไม่มี real approval queue) — SIT**
- Setup: **simulate — ระบบจริง:** write-off OBL-2568-0006 (145,000 > 100,000)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): submit write-off > DOA | — | HTTP 202 **ต้องการอนุมัติจากผู้จัดการ** · เข้าคิว PENDING_APPROVAL · ยังไม่ตัดจริงจน Manager approve (idempotent) | ☐ (ต้อง simulate) |

### TC-X05 — adjustment reverse → ledger reverse append-only (XT-05 / EC-08) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-05 / EC-08 / BR-DEBT-07/08 · **prototype: reverse workflow จริง = SIT**
- Setup: **simulate — ระบบจริง:** reverse OBL-2568-0003 (adjustment)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): reverse adjustment | — | append ledger kind **ย้อนรายการ** (ไม่แก้/ลบของเดิม) · obligation status → **ย้อนรายการ** · outstanding ปรับตาม (append-only) | ☐ (ต้อง simulate) |

### TC-X06 — optimistic stale / idempotent dup / RBAC (EC-12/13 · §5.3) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: EC-12, EC-13, §5.3 · **prototype single-session/user เดียว — SIT**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): 2 sessions — B commit ด้วย row_version เก่า | — | 409 **ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช** (EC-12) | ☐ (ต้อง simulate) |
| 2 | VERIFY (ระบบจริง): POST payment ซ้ำ idempotency-key เดิม | — | 409 **รายการซ้ำ (idempotent)** / no-op (EC-13) | ☐ (ต้อง simulate) |
| 3 | VERIFY (ระบบจริง): user ไม่มีสิทธิ์ (RBAC/DOA) | — | 403 **ไม่มีสิทธิ์ดำเนินการ** · ปุ่มถูกซ่อน (Debt.Officer vs Manager) | ☐ (ต้อง simulate) |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `debt-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock in-memory, refresh = reset seed 5 ลูกหนี้ + 8 ภาระ + 6 โควตา (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/VERIFY/WAIT)
4. `WAIT` = รอ ≤3s จน Expected ปรากฏ (toast มุมขวาล่าง · action ~0.5s · toast แสดง ~3.6-4.2s)
5. **Payment waterfall:** ต้องกด `ตรวจสอบการจัดสรร` ก่อน (validate-then-save) · ปุ่มบันทึกเปิดเมื่อ validated + มีเลขอ้างอิง · จัดสรร priority↑ → ในภาระ ดอกเบี้ย→ค่าปรับ→ต้นทุน
6. **Write-off DOA:** คงเหลือ > 100,000 → warning `จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ` · prototype ยังตัดได้ (mock) · PENDING_APPROVAL จริง = SIT
7. **Ledger:** append-only — ไม่มีปุ่มแก้/ลบ · การแก้ = reverse entry
8. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
9. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 36 / 36 (AC-01..36) |
| Cross-Module / Event (XT-01..05) | 5 / 5 (XT-04/05 = simulate) |
| Business rules (BR-DEBT-01..11) | 11 / 11 |
| Validation (VR-01..15) | 15 / 15 |
| Edge cases (EC-01..13) | 13 / 13 (EC-12/13 = simulate) |
| Error catalog (UI-observable) | ครบ · 202/423 บน prototype · 409/403 = simulate |
| Permission cells | Debt.Officer allow ครบ · Manager/Contract/CBM = simulate |
| 3-entity ledger (Debtor/Obligation/Ledger) | ครบทุกชั้น + double-entry + append-only |

- **Manifest cross-check (FRD §0.12): ✅ 36 AC + 5 XT + 11 BR + 15 VR + 13 EC — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT
- TC-L06 step 3 (ไฟล์ CSV/Aging จริง — server-side)
- TC-G02 step 2 (PDF Statement จริง — server-side)
- TC-G03 step 3 / TC-X03 (feed outstanding → CBM จริง)
- TC-G04 step 2 (ledger UPDATE/DELETE ปฏิเสธ จริง)
- TC-K03 step 2 / TC-X05 (adjustment reverse append-only จริง)
- TC-M05 step 3 / TC-X04 (DOA PENDING_APPROVAL 202 จริง)
- TC-X01 step 3 / TC-X02 step 3 (Quota/Contract read-only · no write-back)
- TC-X06 (optimistic 409 stale · idempotent dup 409 · RBAC 403 — single session/user)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-008",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 54, "pass": 0, "fail": 0, "blocked": 0 }
}
```
