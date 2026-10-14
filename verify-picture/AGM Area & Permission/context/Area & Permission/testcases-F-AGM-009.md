# AI Test Cases — F-AGM-009 Area & Permission Management (พื้นที่และการกำหนดสิทธิ์)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `area-permission-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ FRD 06_TESTS §6.10 microcopy + 05_RULES + สแกน prototype แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side **RBAC 403** · **optimistic 409 stale / idempotent dup** · **แก้ไขพื้นที่จริง** (editArea = stub toast) · **assign/unassign code จริง** (EMPTY↔OCCUPIED ไม่มีปุ่มใน prototype) · **before/after snapshot diff** · **real ERP HR / Geo master** · **area scope → Farmer/Quota จริง** · **ไฟล์ CSV จริง**) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

> ⚠ **หมายเหตุ demo role:** prototype fix `CURRENT_ROLE = 'System Admin'` → `canWrite = true` เสมอ · ปุ่ม write ทุกตัว + แท็บ **Roles** แสดงครบ · เคส RBAC ฝั่ง read-only (Area Head/Officer/Audit-QA) จึงเป็น `(ต้อง simulate)` เพราะสลับ role ไม่ได้บน prototype

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-009 (AGM/AREA — พื้นที่และการกำหนดสิทธิ์) |
| App entry | เปิดไฟล์ `area-permission-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/areas` (Areas list — default) · `#/areas/:area_id` (Area detail drawer 4 แท็บ, refresh-safe) · `#/roles` (Roles view — เห็นเฉพาะ System Admin/Director) |
| Top tabs (page-level) | **Areas** · **Roles** (Roles ซ่อนถ้าไม่ใช่ SA/Director) |
| Overlays (ไม่ผูก route) | create-area drawer · add-head modal · add-director modal · create-code modal · confirm modal |
| ที่มา | FRD_F-AGM-009_Pack (06_TESTS AC-01..27 + XT-01..05 · 05_RULES BR-AP-01..11 / VR-01..06 / EC-01..13) |
| จำนวนเคส | 52 เคส / 10 groups |
| Signature ⭐⭐⭐ | **org-geography + RBAC** (ไม่ใช่ ledger/booking): Area (geography) → ExtensionCode / AreaHead / Director + Audit append-only |
| หัวใจ 1 — Deactivate guard | Active area ที่ codes_count > 0 → ปิดใช้งานไม่ได้ `ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้` |
| หัวใจ 2 — Geography cascade | จังหวัด → อำเภอ (disabled จน province) → ตำบล (disabled จน district) → รหัสไปรษณีย์ auto-fill |
| หัวใจ 3 — RBAC write-gate | `canWrite = ['System Admin','Director']` → ปุ่ม write + Roles tab ซ่อนถ้าไม่ใช่ (prototype = SA เสมอ) |
| หัวใจ 4 — ERP active-only guard | เพิ่ม head/director ได้เฉพาะ ErpEmployee `active` · E07 (inactive) → `พนักงานไม่active` |
| หัวใจ 5 — Audit append-only | ทุก mutation (area/head/code) → push AuditEntry ใหม่ (ไม่แก้ของเดิม) |
| หมายเหตุ mock | prototype in-memory: refresh (F5) = reset seed 5 พื้นที่ + 7 codes + 3 heads + 1 director + 7 ERP employees + 4 audit — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม |
| Cross-module ⭐ | read ERP HR (add head/director) · read Geo master (cascade) · **area_id → scope Farmer/Quota (F-AGM-001/002)** = `(ต้อง simulate)` ที่ SIT |

**Seed ตั้งต้น (หลัง refresh — 5 พื้นที่ AR-0001..0005):**

| เลขพื้นที่ | ชื่อพื้นที่ | จังหวัด | สถานะ | #Heads | #Codes | version |
|---|---|---|---|---|---|---|
| AR-0001 | พื้นที่ภาคกลาง | กรุงเทพมหานคร | เปิดใช้งาน (Active) | 2 | 3 | v4 |
| AR-0002 | พื้นที่ภาคเหนือ | เชียงใหม่ | เปิดใช้งาน | 1 | 2 | v2 |
| AR-0003 | พื้นที่ภาคเหนือตอนบน | เชียงราย | ปิดใช้งาน (Inactive) | 0 | 0 | v1 |
| AR-0004 | พื้นที่ภาคกลางตะวันตก | กรุงเทพมหานคร | เปิดใช้งาน | 0 | 2 | v2 |
| AR-0005 | พื้นที่เชียงใหม่รอบนอก | เชียงใหม่ | เปิดใช้งาน | 0 | 0 | v1 |

- **Stat cards:** พื้นที่ทั้งหมด = **5** · เปิดใช้งาน = **4** · Extension Codes รวม = **7** · Area Heads รวม = **3**

**Seed Extension Codes (7 codes · 4 หลัก):**

| display_code | พื้นที่ | สถานะ | มอบหมายให้ | หมายเหตุ |
|---|---|---|---|---|
| 0101 | AR-0001 | ใช้งานอยู่ (OCCUPIED) | สมชาย ใจกล้า (E01) | โค้ดหลักโซนเหนือ |
| 0102 | AR-0001 | ใช้งานอยู่ | บุญมี ทองดี (E02) | โซนใต้ |
| 0103 | AR-0001 | ว่าง (EMPTY) | — | สำรอง |
| 0201 | AR-0002 | ใช้งานอยู่ | ประเสริฐ สุขใจ (E03) | — |
| 0202 | AR-0002 | ว่าง | — | รอมอบหมาย |
| 0401 | AR-0004 | ใช้งานอยู่ | วิไล งามตา (E04) | โซนสีลม |
| 0402 | AR-0004 | ว่าง | — | — |

> OCCUPIED = **4** (0101/0102/0201/0401) · EMPTY = **3** (0103/0202/0402)

**Seed Area Heads (global = 3) + Directors (1):**

| ประเภท | พนักงาน | รหัส | พื้นที่ |
|---|---|---|---|
| Head | สมชาย ใจกล้า | E01 | AR-0001 |
| Head | วิภา แก้วมณี | E05 | AR-0001 |
| Head | ประเสริฐ สุขใจ | E03 | AR-0002 |
| Director | ดำรง ผู้นำชัย | E06 | (global · ผู้อำนวยการ) |

**Seed ERP employees (7 — สำหรับค้น head/director):**

| รหัส | ชื่อ-สกุล | email | สถานะ |
|---|---|---|---|
| E01 | สมชาย ใจกล้า | somchai@wkn.co.th | active |
| E02 | บุญมี ทองดี | boonmee@wkn.co.th | active |
| E03 | ประเสริฐ สุขใจ | prasert@wkn.co.th | active |
| E04 | วิไล งามตา | wilai@wkn.co.th | active |
| E05 | วิภา แก้วมณี | wipha@wkn.co.th | active |
| E06 | ดำรง ผู้นำชัย | damrong@wkn.co.th | active (ผู้อำนวยการ · Director) |
| **E07** | **สมหญิง ลาพัก** | somying@wkn.co.th | **inactive** (ทดสอบ active-only guard) |

**Seed Geography master (cascade):**

| จังหวัด | อำเภอ/เขต | ตำบล/แขวง (postal) |
|---|---|---|
| กรุงเทพมหานคร (P1) | เขตพระนคร / เขตดุสิต / เขตบางรัก | เช่น สีลม (10500) · พระบรมมหาราชวัง (10200) |
| เชียงใหม่ (P2) | เมืองเชียงใหม่ / สันทราย / แม่ริม | เช่น หนองหาร (50290) · ศรีภูมิ (50200) |
| เชียงราย (P3) | เมืองเชียงราย / แม่สาย / เชียงของ | เช่น แม่สาย (57130) · เวียง (57000) |

**Seed Audit (บน AR-0001 — 4 แถว · append-only · เรียงใหม่→เก่า):**

| id | action badge | actor | details |
|---|---|---|---|
| AU-0004 | แก้ไขพื้นที่ | สมพร วงศ์ทะเบียน | ปรับปรุงข้อมูลที่อยู่พื้นที่ |
| AU-0003 | สร้างโค้ด | สมพร วงศ์ทะเบียน | สร้าง Extension Code: 0101 |
| AU-0002 | เพิ่มหัวหน้า | สมพร วงศ์ทะเบียน | เพิ่มหัวหน้าพื้นที่: สมชาย ใจกล้า |
| AU-0001 | สร้างพื้นที่ | สมพร วงศ์ทะเบียน | สร้างพื้นที่: พื้นที่ภาคกลาง |

**VERBATIM microcopy (Expected anchors — copy เป๊ะจาก prototype):**
- top tabs: `Areas` · `Roles` · detail tabs: `ภาพรวม` · `Area Heads` · `Extension Codes` · `Audit` · roles sub-tabs: `Directors` · `Area Heads` · `Extension Officers`
- ปุ่ม list: `Export CSV` · `สร้างพื้นที่` · `ล้างตัวกรอง` · `ยกเลิกการเลือก` · `Export ที่เลือก`
- ปุ่ม detail: `แก้ไข` · `Export` · `ปิด` · row-actions `เปิด`(eye)/`แก้ไข`(pencil)/toggle(power)
- ปุ่ม tab: `เพิ่มหัวหน้าพื้นที่` · `Create Code` · `เพิ่ม Director` · `เพิ่ม` · `ยืนยัน` · `ยกเลิก` · `ลบหัวหน้าพื้นที่` · `ลบ Director`
- area status pill: `เปิดใช้งาน` (Active · เขียว) · `ปิดใช้งาน` (Inactive · muted)
- code status pill: `ว่าง` (EMPTY) · `ใช้งานอยู่` (OCCUPIED)
- list columns: ☑ · **ชื่อพื้นที่ · จังหวัด · Heads · Codes · สถานะ · การกระทำ**
- filter list: search placeholder `ค้นหา ชื่อพื้นที่ / รหัส` · province `ทุกจังหวัด`/`กรุงเทพมหานคร`/`เชียงใหม่`/`เชียงราย` · status `ทุกสถานะ`/`เปิดใช้งาน`/`ปิดใช้งาน`
- toast success: `เปลี่ยนสถานะสำเร็จ` · `สร้างพื้นที่สำเร็จ` · `เพิ่มหัวหน้าพื้นที่สำเร็จ` · `ลบหัวหน้าพื้นที่สำเร็จ` · `สร้างโค้ดสำเร็จ` · `เพิ่ม Director สำเร็จ` · `ลบ Director สำเร็จ` · `กำลังเตรียมไฟล์ CSV`
- guard/validation (verbatim): `ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้` (desc `กรุณาย้ายหรือลบโค้ดที่ใช้งานอยู่ก่อน`) · `รูปแบบหมายเลขโค้ดไม่ถูกต้อง` (desc `กรอกตัวเลข 4 หลัก เช่น 0123`) · `กรุณาเลือกพื้นที่` · `กรุณาเลือกพนักงาน` · `พนักงานไม่active` (desc `ไม่สามารถเพิ่มพนักงานที่ไม่ได้ใช้งานเป็นหัวหน้าพื้นที่`) · `กรุณากรอกชื่อพื้นที่` · `กรุณาเลือกจังหวัด` · `กรุณาเลือกอำเภอ` · `กรุณาเลือกตำบล`
- dup guard: `หมายเลขโค้ดนี้มีอยู่แล้วในพื้นที่` · `พนักงานคนนี้เป็นหัวหน้าพื้นที่นี้อยู่แล้ว` · `พนักงานคนนี้เป็น Director อยู่แล้ว`
- geography help: `กรุณาเลือกจังหวัดก่อน` (district disabled) · `กรุณาเลือกอำเภอก่อน` (subdistrict disabled) · postal placeholder `เติมอัตโนมัติจากตำบล`
- confirm: `ยืนยันลบหัวหน้าพื้นที่?` · `ยืนยันลบ Director?`
- empty: `ยังไม่มีพื้นที่` (no-data) / `ไม่พบรายการที่ค้นหา` (filter) · `ยังไม่มีหัวหน้าพื้นที่` · `ยังไม่มี Extension Codes ในพื้นที่นี้` · `ยังไม่มีประวัติการเปลี่ยนแปลง` · `ยังไม่มี Director` · `ไม่พบ Extension Codes`
- footer/pagination: `แสดง X-Y จาก Z รายการ` · bulk `เลือกแล้ว N รายการ`
- stub/simulate: `เปิดฟอร์มแก้ไขพื้นที่ (ตัวอย่าง)` (editArea stub) · server `ไม่มีสิทธิ์ดำเนินการ` (403) · `ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช` (409 stale) · `รายการซ้ำ (idempotent)` (409 dup)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| A — Areas list / search / filter / stats / CSV / bulk | TC-A01..A07 (7) | สูงสุด |
| B — Area create + geography cascade | TC-B01..B06 (6) | สูงสุด |
| C — Area detail 4 tabs + toggle guard ⭐ | TC-C01..C06 (6) | สูงสุด |
| D — Area Heads add / remove (ERP active guard) | TC-D01..D06 (6) | สูงสุด |
| E — Extension Codes create / validation | TC-E01..E06 (6) | สูงสุด |
| F — Roles Directors (add / remove) | TC-F01..F05 (5) | สูง |
| G — Roles Area Heads + Extension Officers | TC-G01..G04 (4) | สูง |
| H — Audit timeline (append-only) | TC-H01..H03 (3) | กลาง |
| I — RBAC (write-gate + Roles tab) | TC-I01..I03 (3) | สูง |
| J — Cross-module XT-01..05 + simulate | TC-J01..J06 (6) | สูงสุด |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | list + 4 stats (พื้นที่ทั้งหมด/เปิดใช้งาน/Extension Codes/Area Heads) | TC-A01 |
| AC-02 | ค้นหา (ชื่อ/รหัส) · กรอง จังหวัด + สถานะ | TC-A02, TC-A03 |
| AC-03 | คอลัมน์ครบ (☑/ชื่อพื้นที่ link/จังหวัด/Heads/Codes/สถานะ pill/⋯) | TC-A01, TC-A06 |
| AC-04 | Export CSV → "กำลังเตรียมไฟล์ CSV" | TC-A05 |
| AC-05 | bulk select "เลือกแล้ว N รายการ" · pagination "แสดง X-Y จาก Z รายการ" | TC-A05 |
| AC-06 | empty → "ยังไม่มีพื้นที่" / "ไม่พบรายการที่ค้นหา" | TC-A04 |
| AC-07 | geography cascade: จังหวัด→อำเภอ→ตำบล→postal auto-fill | TC-B01, TC-B02, TC-B06 |
| AC-08 | สร้างสำเร็จ → เปิด detail ของพื้นที่ใหม่ | TC-B05 |
| AC-09 | 4 แท็บ (Overview/Area Heads/Extension Codes/Audit) + header | TC-C01 |
| AC-10 | Overview: ข้อมูลพื้นที่ครบ + สรุป (Heads/Codes/เวอร์ชัน) | TC-C02 |
| AC-11 | toggle Active→Inactive, codes>0 → guard | TC-C03, TC-C06 |
| AC-12 | toggle Inactive→Active → "เปลี่ยนสถานะสำเร็จ" | TC-C05 |
| AC-13 | เพิ่มหัวหน้า: ค้น ERP → เลือก → "เพิ่มหัวหน้าพื้นที่สำเร็จ" | TC-D01 |
| AC-14 | ไม่เลือกพนักงาน → "กรุณาเลือกพนักงาน" | TC-D02 |
| AC-15 | employee inactive → "พนักงานไม่active" | TC-D03 |
| AC-16 | ลบหัวหน้า → confirm → "ลบหัวหน้าพื้นที่สำเร็จ" | TC-D04 |
| AC-17 | สร้างโค้ด: พื้นที่ Active + 4 หลัก → "สร้างโค้ดสำเร็จ" | TC-E02 |
| AC-18 | ไม่เลือกพื้นที่ → "กรุณาเลือกพื้นที่" | TC-E03 |
| AC-19 | โค้ดไม่ใช่ 4 หลัก → "รูปแบบหมายเลขโค้ดไม่ถูกต้อง" | TC-E04 |
| AC-20 | codes tab: EMPTY(ว่าง)/OCCUPIED(ใช้งานอยู่) + assigned + note | TC-E01 |
| AC-21 | Roles tab แสดงเฉพาะ SA/Director | TC-F01, TC-I01 |
| AC-22 | Directors: เพิ่ม → "เพิ่ม Director สำเร็จ" · ลบ → "ลบ Director สำเร็จ" | TC-F02, TC-F04 |
| AC-23 | Extension Officers: cross-area + filter (พื้นที่/สถานะ) | TC-G02, TC-G03, TC-G04 |
| AC-24 | Area Heads (global): รายการ head ทุกพื้นที่ | TC-F01, TC-G01 |
| AC-25 | Audit timeline: action badge + actor + timestamp + details | TC-H01 |
| AC-26 | SA/Director: เห็นปุ่ม write + Roles tab | TC-I01 |
| AC-27 | Area Head/Officer/Audit-QA: read-only (write ซ่อน · Roles ซ่อน) | TC-I02 (ต้อง simulate) |

### Cross-Module / Event (06_TESTS §6.9) ⭐
| XT | Scenario | Source | cases |
|---|---|---|---|
| XT-01 | เพิ่มหัวหน้า/director → snapshot ชื่อ/email (active) | ERP HR (read) | TC-D01, TC-F02, TC-J01 |
| XT-02 | geography cascade อำเภอ/ตำบล/postal ตรงลำดับ | Geo master (read) | TC-B01, TC-B02, TC-J02 |
| XT-03 | area_id → scope เกษตรกร/โควตา (idempotent) | → Farmer/Quota (F-AGM-001/002) | TC-J03 (ต้อง simulate) |
| XT-04 | RBAC enforce: write = 403 ถ้าไม่ใช่ SA/Director | session role (server) | TC-I03, TC-J04 (ต้อง simulate) |
| XT-05 | audit append-only + before/after ทุก mutation | AuditEntry append | TC-H02, TC-J05 |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-AP-01 Deactivate guard (codes>0 ปิดไม่ได้) | TC-C03, TC-C06, TC-C04 |
| BR-AP-02 Geography cascade + postal auto-fill | TC-B01, TC-B02 |
| BR-AP-03 Extension Code ผูก Active area เท่านั้น | TC-E05 |
| BR-AP-04 Code EMPTY↔OCCUPIED (assign/unassign) | TC-E01, TC-J06 (ต้อง simulate) |
| BR-AP-05 Extension Officer = code assignment | TC-G02 |
| BR-AP-06 head/director active-only | TC-D03, TC-F03 |
| BR-AP-07 RBAC write-gate + Roles tab ซ่อน | TC-I01, TC-I02 |
| BR-AP-08 Optimistic (version) + idempotency key | TC-J06 (ต้อง simulate) |
| BR-AP-09 Audit before/after ทุก action | TC-H01, TC-H02, TC-J05 |
| BR-AP-10 People จาก ERP (ค้น ชื่อ/รหัส/email) ไม่สร้างคนใหม่ | TC-D01, TC-F02 |
| BR-AP-11 display_code 4 หลัก · postal 5 หลัก · email format | TC-E04, TC-B02 |

### Validation (05_RULES §5.4)
| VR | Message | cases |
|---|---|---|
| VR-01 | "รูปแบบหมายเลขโค้ดไม่ถูกต้อง" (4 digits) | TC-E04 |
| VR-02 | postal 5 หลัก (auto-fill; inline) | TC-B02 |
| VR-03 | email format (inline · จาก ERP snapshot) | TC-J06 (ต้อง simulate) |
| VR-04 | "กรุณาเลือกพื้นที่" (area required) | TC-E03 |
| VR-05 | "กรุณาเลือกพนักงาน" (employee required) | TC-D02, TC-F02 |
| VR-06 | "พนักงานไม่active" (employee active) | TC-D03, TC-F03 |

### Edge Cases (05_RULES §5.5)
| EC | Case | cases |
|---|---|---|
| EC-01 | toggle Active→Inactive, codes>0 → block | TC-C03, TC-C06 |
| EC-02 | toggle Inactive→Active → สำเร็จ | TC-C05 |
| EC-03 | create code, area Inactive → ไม่อยู่ใน dropdown | TC-E05 |
| EC-04 | create code ไม่ใช่ 4 หลัก → VR-01 block | TC-E04 |
| EC-05 | add head, employee inactive → VR-06 block | TC-D03 |
| EC-06 | add head/director ซ้ำ → idempotent (no dup) | TC-D06, TC-F02 |
| EC-07 | non-SA/Director เปิดหน้า → Roles tab + write ซ่อน | TC-I02 (ต้อง simulate) |
| EC-08 | geography cascade enable ทีละชั้น | TC-B01 |
| EC-09 | remove head/director → confirm → "ลบ...สำเร็จ" | TC-D04, TC-F04 |
| EC-10 | assign code EMPTY → OCCUPIED | TC-J06 (ต้อง simulate) |
| EC-11 | unassign code OCCUPIED → EMPTY | TC-J06 (ต้อง simulate) |
| EC-12 | optimistic stale → 409 CONFLICT_UPDATE_STALE | TC-J06 (ต้อง simulate) |
| EC-13 | idempotent dup → 409/no-op | TC-J06 (ต้อง simulate) |

### Error Catalog (05_RULES §5.6 — UI-observable)
| error | cases |
|---|---|
| VALIDATION_FAILED (code/area/employee/geo/name) | TC-E03, TC-E04, TC-D02, TC-D03, TC-B03, TC-B04 |
| AREA_HAS_ACTIVE_CODES(409) "ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" | TC-C03, TC-C06 |
| EMPLOYEE_INACTIVE(400) "พนักงานไม่active" | TC-D03, TC-F03 |
| FORBIDDEN(403) "ไม่มีสิทธิ์ดำเนินการ" | TC-I03, TC-J04 (simulate) |
| CONFLICT_UPDATE_STALE(409) "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช" | TC-J06 (simulate) |
| CONFLICT(409) "รายการซ้ำ (idempotent)" | TC-J06 (simulate) |

### State Machine (05_RULES §5.2)
| entity | ข้อยืนยัน (ย่อ) | cases |
|---|---|---|
| Area | Active ⇄ Inactive (Active→Inactive block ถ้า codes>0) | TC-C03, TC-C04, TC-C05, TC-C06 |
| ExtensionCode | EMPTY → (assign) → OCCUPIED → (unassign) → EMPTY | TC-E01, TC-J06 (simulate) |

### Permission (05_RULES §5.3)
| cell | cases |
|---|---|
| System Admin/Director (read+write · Roles tab ✅) — prototype user | TC-I01, TC-D01, TC-E02, TC-F02 |
| Area Head/Officer/Audit-QA (read · Roles ❌ · write ❌) — RBAC จริง | TC-I02, TC-I03, TC-J04 (simulate) |

**Manifest cross-check (FRD §0.12):** AC 27/27 (AC-01..27) · XT-01..05 5/5 · BR-AP-01..11 11/11 · VR-01..06 6/6 · EC-01..13 13/13 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — พื้นที่ใหม่ถูกต้อง (happy — create-area drawer)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ชื่อพื้นที่ | พื้นที่ทดสอบใหม่ |
| จังหวัด | เชียงราย |
| อำเภอ/เขต | แม่สาย |
| ตำบล/แขวง | แม่สาย |
| รหัสไปรษณีย์ | *(auto-fill)* 57130 |
| ที่อยู่ | 1 หมู่ 1 |
| คำอธิบาย | สร้างจาก test case |

### ชุด B — ค่าผิด (create-area negative)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | ชื่อพื้นที่ | *(เว้นว่าง)* | กรุณากรอกชื่อพื้นที่ |
| B2 | จังหวัด | *(เว้นว่าง · มีชื่อแล้ว)* | กรุณาเลือกจังหวัด |
| B3 | อำเภอ | *(เว้นว่าง · มีจังหวัดแล้ว)* | กรุณาเลือกอำเภอ |
| B4 | ตำบล | *(เว้นว่าง · มีอำเภอแล้ว)* | กรุณาเลือกตำบล |

### ชุด C — Extension Code (create-code modal)
| กรณี | พื้นที่ | โค้ด | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| C1 (happy) | AR-0005 (Active) | 0501 | สร้างโค้ดสำเร็จ |
| C2 | *(ไม่เลือก)* | 0101 | กรุณาเลือกพื้นที่ |
| C3 | AR-0001 | 12 (ไม่ครบ 4 หลัก) | รูปแบบหมายเลขโค้ดไม่ถูกต้อง |
| C4 (dup) | AR-0001 | 0101 (ซ้ำ) | หมายเลขโค้ดนี้มีอยู่แล้วในพื้นที่ |

### ชุด D — ERP employee (add head / director)
| กรณี | พนักงานที่ค้น | คาดหวัง |
|---|---|---|
| D1 (happy head) | วิไล / E04 (active) | เพิ่มหัวหน้าพื้นที่สำเร็จ |
| D2 (inactive) | สมหญิง / E07 (inactive) | พนักงานไม่active |
| D3 (dup head) | สมชาย / E01 (เป็น head AR-0001 อยู่แล้ว) | พนักงานคนนี้เป็นหัวหน้าพื้นที่นี้อยู่แล้ว |
| D4 (director) | บุญมี / E02 (active) | เพิ่ม Director สำเร็จ |

---

## Test Cases

## Group A — Areas list / search / filter / stats / CSV / bulk (US-01)

### TC-A01 — เปิดหน้า list + 4 stats + คอลัมน์ (happy — AC-01/03)
- group: A · ความสำคัญ: สูงสุด · trace: AC-01, AC-03 / UI loaded
- Setup: seed=default 5 พื้นที่ (refresh) · files=—
- Start: OPEN `#/areas`
- ผ่านเมื่อ: top tabs + stat cards + คอลัมน์แสดงตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/areas` | — | top tabs **Areas** (active) · **Roles** · หัวข้อ **พื้นที่ (Areas)** + count **5 รายการ** · sub "จัดการพื้นที่ปฏิบัติการ, สถานะ และหัวหน้าพื้นที่" | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **พื้นที่ทั้งหมด 5** · **เปิดใช้งาน 4** · **Extension Codes รวม 7** · **Area Heads รวม 3** | ☐ |
| 3 | VERIFY หัวคอลัมน์ตาราง | — | เรียง: ☑ · **ชื่อพื้นที่ · จังหวัด · Heads · Codes · สถานะ · การกระทำ** | ☐ |
| 4 | VERIFY แถว AR-0001 | — | ชื่อพื้นที่ **พื้นที่ภาคกลาง** (sub รหัส AR-0001) · จังหวัด **กรุงเทพมหานคร** · Heads **2** · Codes **3** · สถานะ **เปิดใช้งาน** | ☐ |
| 5 | VERIFY แถว AR-0003 (Inactive · 0/0) | — | จังหวัด **เชียงราย** · Heads **0** · Codes **0** · สถานะ **ปิดใช้งาน** (pill muted) | ☐ |
| 6 | VERIFY ปุ่ม page header + footer | — | ปุ่ม **Export CSV** · **สร้างพื้นที่** (primary) · footer **แสดง 1-5 จาก 5 รายการ** | ☐ |

### TC-A02 — ค้นหา ชื่อ / รหัส (happy — AC-02)
- group: A · ความสำคัญ: สูง · trace: AC-02 / search
- Setup: seed=default · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ภาคเหนือ" → ช่องค้นหา (placeholder **ค้นหา ชื่อพื้นที่ / รหัส**) | ชื่อ | เหลือ 2 แถว: AR-0002 (พื้นที่ภาคเหนือ) + AR-0003 (พื้นที่ภาคเหนือตอนบน) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** → TYPE "AR-0004" | รหัส | เหลือ 1 แถว AR-0004 (พื้นที่ภาคกลางตะวันตก) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** | — | กลับ 5 รายการ | ☐ |

### TC-A03 — filter จังหวัด + สถานะ (AC-02)
- group: A · ความสำคัญ: สูง · trace: AC-02 / province + status filter
- Setup: seed=default · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown จังหวัด = **เชียงใหม่** | — | เหลือ 2 แถว AR-0002 + AR-0005 | ☐ |
| 2 | CLICK **ล้างตัวกรอง** → SELECT สถานะ = **ปิดใช้งาน** | — | เหลือ 1 แถว AR-0003 (สถานะ **ปิดใช้งาน**) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** → SELECT สถานะ = **เปิดใช้งาน** | — | เหลือ 4 แถว (AR-0001/0002/0004/0005) · ไม่รวม AR-0003 | ☐ |

### TC-A04 — empty states (AC-06)
- group: A · ความสำคัญ: สูง · trace: AC-06 / empty (filter vs no-data)
- Setup: seed=default · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีพื้นที่นี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK **ล้างตัวกรอง** | — | กลับ 5 รายการ | ☐ |
| 3 | VERIFY (no-data variant): SELECT จังหวัด=เชียงราย + สถานะ=เปิดใช้งาน | — | empty state **ไม่พบรายการที่ค้นหา** (AR-0003 เชียงราย เป็น Inactive) | ☐ |

> หมายเหตุ: empty **ยังไม่มีพื้นที่** + ปุ่ม **สร้างพื้นที่ใหม่** โชว์เฉพาะกรณีระบบไม่มีพื้นที่เลย (all.length===0) — prototype seed มี 5 เสมอ จึงเป็นเคส `(ต้อง simulate)` ที่ระบบเปล่า

### TC-A05 — Export CSV + bulk select + pagination (AC-04/05) (บางส่วน ต้อง simulate)
- group: A · ความสำคัญ: กลาง · trace: AC-04, AC-05 · **prototype: toast จำลอง · ไฟล์จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Export CSV** → WAIT | — | toast **กำลังเตรียมไฟล์ CSV** | ☐ |
| 2 | CLICK checkbox หัวตาราง (เลือกทั้งหมด) | — | แถบ bulk **เลือกแล้ว 5 รายการ** + ปุ่ม **Export ที่เลือก** + **ยกเลิกการเลือก** | ☐ |
| 3 | CLICK **ยกเลิกการเลือก** | — | แถบ bulk หาย · ไม่มีแถวถูกเลือก | ☐ |
| 4 | VERIFY pagination footer | — | **แสดง 1-5 จาก 5 รายการ** (pageSize 25 · หน้าเดียว) | ☐ |
| 5 | VERIFY (ระบบจริง — SIT): ไฟล์ CSV จริง | — | ไฟล์ CSV ดาวน์โหลด · คอลัมน์ตรงตาราง | ☐ (ต้อง simulate) |

### TC-A06 — row-actions (เปิด/แก้ไข/toggle) + edit stub (AC-03)
- group: A · ความสำคัญ: กลาง · trace: AC-03 · **prototype: แก้ไข = stub toast · ฟอร์มแก้จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY row-actions แถว AR-0001 | — | มีปุ่ม **เปิด** (eye) · **แก้ไข** (pencil) · toggle (power) ครบ (canWrite=SA) | ☐ |
| 2 | CLICK ปุ่ม **แก้ไข** (pencil) บน AR-0001 | — | toast **เปิดฟอร์มแก้ไขพื้นที่ (ตัวอย่าง)** (stub) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): ฟอร์มแก้ไขพื้นที่จริง | — | เปิดฟอร์มแก้ + optimistic version + audit before/after | ☐ (ต้อง simulate) |

### TC-A07 — เปิด detail จากแถว + refresh-safe route (AC-03)
- group: A · ความสำคัญ: กลาง · trace: AC-03 / route `#/areas/:id`
- Setup: seed=default · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว AR-0002 (หรือปุ่ม เปิด eye) | — | drawer เปิด · URL = **#/areas/AR-0002** · eyebrow **พื้นที่ · AR-0002** | ☐ |
| 2 | F5 (refresh) ที่ URL #/areas/AR-0002 | — | drawer AR-0002 เปิดใหม่อัตโนมัติ (refresh-safe) | ☐ |
| 3 | CLICK ปุ่ม **ปิด** (footer) | — | drawer ปิด · กลับ `#/areas` (list 5 รายการ) | ☐ |

---

## Group B — Area create + geography cascade (US-02)

### TC-B01 — geography cascade: disabled ทีละชั้น (happy — AC-07 / EC-08 / XT-02) ★
- group: B · ความสำคัญ: สูงสุด · trace: AC-07 / EC-08 / XT-02 / BR-AP-02
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**
- ผ่านเมื่อ: cascade enable ทีละชั้น ตามลำดับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างพื้นที่** | — | drawer เปิด · eyebrow **สร้างพื้นที่** · title **สร้างพื้นที่ปฏิบัติการ** · sub "พื้นที่ใหม่เริ่มต้นที่สถานะ “เปิดใช้งาน”" | ☐ |
| 2 | VERIFY สถานะเริ่มต้นของ cascade | — | **อำเภอ/เขต** disabled · help **กรุณาเลือกจังหวัดก่อน** · **ตำบล/แขวง** disabled · help **กรุณาเลือกอำเภอก่อน** · **รหัสไปรษณีย์** readonly · placeholder **เติมอัตโนมัติจากตำบล** | ☐ |
| 3 | SELECT จังหวัด = **เชียงใหม่** | — | อำเภอ enabled · help เปลี่ยนเป็น **เลือกอำเภอในจังหวัดที่เลือก** · dropdown อำเภอ = เมืองเชียงใหม่ / สันทราย / แม่ริม | ☐ |
| 4 | SELECT อำเภอ = **สันทราย** | — | ตำบล enabled · dropdown ตำบล = หนองหาร / สันทรายน้อย | ☐ |

### TC-B02 — cascade เต็ม → postal auto-fill (AC-07 / VR-02 / BR-AP-11) ★
- group: B · ความสำคัญ: สูงสุด · trace: AC-07 / VR-02 / BR-AP-11 / postal 5 หลัก
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT จังหวัด **เชียงใหม่** → อำเภอ **สันทราย** → ตำบล **หนองหาร** | — | ช่อง **รหัสไปรษณีย์** auto-fill = **50290** (5 หลัก · readonly) | ☐ |
| 2 | VERIFY: เปลี่ยนตำบล = **สันทรายน้อย** | SELECT ตำบล สันทรายน้อย | postal auto เปลี่ยนเป็น **50210** | ☐ |

### TC-B03 — สร้างไม่มีชื่อ → block (negative — VR / AC-08)
- group: B · ความสำคัญ: สูง · trace: AC-08 / validation name
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้น **ชื่อพื้นที่** ว่าง → CLICK **สร้างพื้นที่** (footer) | B1 | warning **กรุณากรอกชื่อพื้นที่** · ไม่สร้าง | ☐ |

### TC-B04 — สร้างไม่ครบ geography → block ทีละชั้น (negative — AC-08)
- group: B · ความสำคัญ: สูง · trace: AC-08 / validation geo sequence
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**
- ชุดข้อมูล: B2/B3/B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ชื่อพื้นที่ "พื้นที่ทดสอบ" · เว้นจังหวัด → CLICK **สร้างพื้นที่** | B2 | warning **กรุณาเลือกจังหวัด** | ☐ |
| 2 | SELECT จังหวัด เชียงราย (ยังไม่เลือกอำเภอ) → CLICK **สร้างพื้นที่** | B3 | warning **กรุณาเลือกอำเภอ** | ☐ |
| 3 | SELECT อำเภอ แม่สาย (ยังไม่เลือกตำบล) → CLICK **สร้างพื้นที่** | B4 | warning **กรุณาเลือกตำบล** | ☐ |

### TC-B05 — สร้างพื้นที่สำเร็จ → detail (happy — AC-08) ★
- group: B · ความสำคัญ: สูงสุด · trace: AC-08 / navigate + list count
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**
- ชุดข้อมูล: A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอกชุด A: ชื่อ "พื้นที่ทดสอบใหม่" · จังหวัด เชียงราย · อำเภอ แม่สาย · ตำบล แม่สาย (postal auto 57130) → CLICK **สร้างพื้นที่** → WAIT | A | drawer ปิด + toast **สร้างพื้นที่สำเร็จ** · navigate ไป detail พื้นที่ใหม่ **AR-0006** (สถานะ **เปิดใช้งาน**) | ☐ |
| 2 | กลับ list → VERIFY count | — | **6 รายการ** · stat **พื้นที่ทั้งหมด 6** · **เปิดใช้งาน 5** · แถวใหม่ AR-0006 อยู่บนสุด | ☐ |

### TC-B06 — cascade reset เมื่อเปลี่ยนจังหวัด (AC-07 / EC-08)
- group: B · ความสำคัญ: สูง · trace: AC-07 / cascade dependency reset
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT จังหวัด เชียงใหม่ → อำเภอ สันทราย → ตำบล หนองหาร (postal 50290) | — | cascade เต็ม · postal 50290 | ☐ |
| 2 | เปลี่ยน SELECT จังหวัด = **กรุงเทพมหานคร** | — | อำเภอ + ตำบล ถูกล้าง (reset) · postal ว่าง (placeholder **เติมอัตโนมัติจากตำบล**) · dropdown อำเภอ = เขตพระนคร / เขตดุสิต / เขตบางรัก | ☐ |

---

## Group C — Area detail 4 tabs + toggle guard (US-03) ⭐

### TC-C01 — Detail header + 4 tabs (AC-09)
- group: C · ความสำคัญ: สูงสุด · trace: AC-09 / drawer 4 tabs
- Setup: seed=default · files=—
- Start: OPEN `#/areas/AR-0001`
- ผ่านเมื่อ: header + 4 แท็บ ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/areas/AR-0001` | — | drawer เปิด · eyebrow **พื้นที่ · AR-0001** · title **พื้นที่ภาคกลาง** + status pill **เปิดใช้งาน** · sub "กรุงเทพมหานคร · เขตพระนคร · อัปเดต: ..." | ☐ |
| 2 | VERIFY แถบแท็บ | — | 4 แท็บ: **ภาพรวม · Area Heads (2) · Extension Codes (3) · Audit** | ☐ |
| 3 | VERIFY ปุ่ม header | — | ปุ่ม **แก้ไข** · **ปิดใช้งาน** (toggle) · **Export** · ปุ่มปิด (x) | ☐ |

### TC-C02 — แท็บ ภาพรวม: ข้อมูลพื้นที่ + สรุป (AC-10)
- group: C · ความสำคัญ: สูงสุด · trace: AC-10 / overview grid + summary
- Setup: seed=default · files=—
- Start: OPEN `#/areas/AR-0001` (แท็บ ภาพรวม default)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section **ข้อมูลพื้นที่** | — | grid: ชื่อพื้นที่ **พื้นที่ภาคกลาง** · จังหวัด **กรุงเทพมหานคร** · อำเภอ/เขต **เขตพระนคร** · ตำบล/แขวง **พระบรมมหาราชวัง** · รหัสไปรษณีย์ **10200** · สถานะ **เปิดใช้งาน** | ☐ |
| 2 | VERIFY section **สรุป** | — | **Area Heads 2 คน** · **Extension Codes 3 โค้ด** · **เวอร์ชัน v4** | ☐ |

### TC-C03 — toggle guard: Active + codes>0 → block (negative — AC-11 / EC-01 / BR-AP-01) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-11 / EC-01 / BR-AP-01 (AREA_HAS_ACTIVE_CODES)
- Setup: seed=default (AR-0001 · 3 codes · Active) · files=—
- Start: OPEN `#/areas`
- ผ่านเมื่อ: block + status ยังเป็น เปิดใช้งาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม toggle (power) บนแถว AR-0001 → WAIT | — | toast **ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้** (desc **กรุณาย้ายหรือลบโค้ดที่ใช้งานอยู่ก่อน**) | ☐ |
| 2 | VERIFY สถานะ AR-0001 | — | สถานะยังเป็น **เปิดใช้งาน** (ไม่เปลี่ยน) · stat **เปิดใช้งาน 4** ไม่ลด | ☐ |
| 3 | VERIFY: AR-0004 (2 codes) ก็ block เช่นกัน | CLICK toggle บน AR-0004 | toast **ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้** · AR-0004 ยัง **เปิดใช้งาน** | ☐ |

### TC-C04 — toggle: Active + codes=0 → success (AC-11 boundary / BR-AP-01)
- group: C · ความสำคัญ: สูง · trace: AC-11 boundary / codes=0 allowed
- Setup: seed=default (AR-0005 · 0 codes · Active) · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม toggle (power) บนแถว AR-0005 → WAIT | — | toast **เปลี่ยนสถานะสำเร็จ** (0 codes → ไม่ติด guard) | ☐ |
| 2 | VERIFY สถานะ AR-0005 | — | สถานะเปลี่ยนเป็น **ปิดใช้งาน** · stat **เปิดใช้งาน 3** | ☐ |

### TC-C05 — toggle: Inactive → Active → success (AC-12 / EC-02)
- group: C · ความสำคัญ: สูงสุด · trace: AC-12 / EC-02
- Setup: seed=default (AR-0003 · Inactive) · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม toggle (power) บนแถว AR-0003 → WAIT | — | toast **เปลี่ยนสถานะสำเร็จ** (Inactive→Active ok เสมอ) | ☐ |
| 2 | VERIFY สถานะ AR-0003 | — | สถานะเปลี่ยนเป็น **เปิดใช้งาน** · stat **เปิดใช้งาน 5** | ☐ |

### TC-C06 — toggle guard จากปุ่มใน detail drawer (AC-11 / EC-01)
- group: C · ความสำคัญ: สูง · trace: AC-11 / EC-01 · guard จาก header drawer
- Setup: seed=default (AR-0004 · 2 codes · Active) · files=—
- Start: OPEN `#/areas/AR-0004`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม header | — | ปุ่ม toggle แสดงข้อความ **ปิดใช้งาน** (เพราะสถานะ Active) | ☐ |
| 2 | CLICK ปุ่ม **ปิดใช้งาน** (header drawer) → WAIT | — | toast **ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้** · status pill ยัง **เปิดใช้งาน** | ☐ |

---

## Group D — Area Heads add / remove (US-04)

### TC-D01 — เพิ่มหัวหน้าพื้นที่สำเร็จ (happy — AC-13 / XT-01) ★
- group: D · ความสำคัญ: สูงสุด · trace: AC-13 / XT-01 / BR-AP-10 (ERP snapshot)
- Setup: seed=default (AR-0004 · 0 heads) · files=—
- Start: OPEN `#/areas/AR-0004` → CLICK แท็บ **Area Heads**
- ชุดข้อมูล: D1
- ผ่านเมื่อ: ค้น ERP → เลือก active → เพิ่ม → success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **Area Heads (0)** → VERIFY empty | — | empty state **ยังไม่มีหัวหน้าพื้นที่** + ปุ่ม **เพิ่มหัวหน้าพื้นที่** | ☐ |
| 2 | CLICK **เพิ่มหัวหน้าพื้นที่** | — | modal **เพิ่มหัวหน้าพื้นที่** · ช่องค้น ERP placeholder **พิมพ์เพื่อค้นหาพนักงาน** · ปุ่ม **เพิ่ม** disabled | ☐ |
| 3 | TYPE "วิไล" → เลือกผล **วิไล งามตา · E04** (option แสดง tag **active**) | D1 | preview **พนักงานที่เลือก** = วิไล งามตา · E04 · ปุ่ม **เพิ่ม** enabled | ☐ |
| 4 | CLICK **เพิ่ม** → WAIT | — | modal ปิด + toast **เพิ่มหัวหน้าพื้นที่สำเร็จ** | ☐ |
| 5 | VERIFY แท็บ Area Heads + list | — | table มีแถว วิไล งามตา (E04 · wilai@wkn.co.th) · badge แท็บ **Area Heads (1)** · stat list **Area Heads รวม 4** | ☐ |

### TC-D02 — ไม่เลือกพนักงาน → block (negative — AC-14 / VR-05)
- group: D · ความสำคัญ: สูง · trace: AC-14 / VR-05
- Setup: seed=default · files=—
- Start: OPEN `#/areas/AR-0004` → แท็บ **Area Heads** → CLICK **เพิ่มหัวหน้าพื้นที่**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไม่เลือกพนักงาน → VERIFY ปุ่ม **เพิ่ม** | — | ปุ่ม **เพิ่ม** ยัง disabled (require selection) · preview **ยังไม่ได้เลือกพนักงาน** | ☐ |
| 2 | (ยิง submitAddHead ตรง ๆ โดยไม่เลือก) | — | block + warning **กรุณาเลือกพนักงาน** | ☐ |

### TC-D03 — เลือกพนักงาน inactive (E07) → block (negative — AC-15 / VR-06 / EC-05) ★
- group: D · ความสำคัญ: สูงสุด · trace: AC-15 / VR-06 / EC-05 / BR-AP-06
- Setup: seed=default (E07 สมหญิง ลาพัก inactive) · files=—
- Start: OPEN `#/areas/AR-0004` → แท็บ **Area Heads** → CLICK **เพิ่มหัวหน้าพื้นที่**
- ชุดข้อมูล: D2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "สมหญิง" → VERIFY option | D2 | option **สมหญิง ลาพัก · E07** แสดง tag **inactive** | ☐ |
| 2 | เลือก **สมหญิง ลาพัก** → CLICK **เพิ่ม** → WAIT | D2 | block + toast **พนักงานไม่active** (desc **ไม่สามารถเพิ่มพนักงานที่ไม่ได้ใช้งานเป็นหัวหน้าพื้นที่**) · ไม่เพิ่ม | ☐ |

### TC-D04 — ลบหัวหน้าพื้นที่ → confirm → success (AC-16 / EC-09)
- group: D · ความสำคัญ: สูง · trace: AC-16 / EC-09
- Setup: seed=default (AR-0001 · 2 heads: E01, E05) · files=—
- Start: OPEN `#/areas/AR-0001` → CLICK แท็บ **Area Heads**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บ Area Heads (2) | — | 2 แถว: สมชาย ใจกล้า (E01) · วิภา แก้วมณี (E05) · คอลัมน์ ชื่อ-สกุล / Email / มอบหมายเมื่อ / ลบ | ☐ |
| 2 | CLICK ปุ่ม ลบ (trash) บนแถว **วิภา แก้วมณี** | — | confirm modal **ยืนยันลบหัวหน้าพื้นที่?** · ปุ่ม **ลบหัวหน้าพื้นที่** (danger) + **ยกเลิก** | ☐ |
| 3 | CLICK **ลบหัวหน้าพื้นที่** → WAIT | — | modal ปิด + toast **ลบหัวหน้าพื้นที่สำเร็จ** · แท็บ **Area Heads (1)** · เหลือ สมชาย ใจกล้า | ☐ |

### TC-D05 — empty heads state (AC-09)
- group: D · ความสำคัญ: กลาง · trace: AC-09 / empty heads · AR-0003
- Setup: seed=default (AR-0003 · 0 heads) · files=—
- Start: OPEN `#/areas/AR-0003` → CLICK แท็บ **Area Heads**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **Area Heads (0)** | — | empty state **ยังไม่มีหัวหน้าพื้นที่** (desc "พื้นที่นี้ยังไม่มีการมอบหมายหัวหน้าพื้นที่") | ☐ |

### TC-D06 — เพิ่มหัวหน้าซ้ำ → idempotent guard (EC-06)
- group: D · ความสำคัญ: กลาง · trace: EC-06 / dup guard (no dup)
- Setup: seed=default (AR-0001 · E01 เป็น head อยู่แล้ว) · files=—
- Start: OPEN `#/areas/AR-0001` → แท็บ **Area Heads** → CLICK **เพิ่มหัวหน้าพื้นที่**
- ชุดข้อมูล: D3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "สมชาย" → เลือก **สมชาย ใจกล้า · E01** → CLICK **เพิ่ม** → WAIT | D3 | toast **พนักงานคนนี้เป็นหัวหน้าพื้นที่นี้อยู่แล้ว** (idempotent · ไม่เพิ่มซ้ำ) | ☐ |
| 2 | VERIFY แท็บ Area Heads | — | ยัง **2 แถว** (E01, E05 · ไม่เพิ่มซ้ำ) | ☐ |

---

## Group E — Extension Codes create / validation (US-05)

### TC-E01 — codes tab: EMPTY/OCCUPIED + assigned + note (AC-20)
- group: E · ความสำคัญ: สูง · trace: AC-20 / BR-AP-04 (state display)
- Setup: seed=default (AR-0001 · 3 codes) · files=—
- Start: OPEN `#/areas/AR-0001` → CLICK แท็บ **Extension Codes**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **Extension Codes (3)** | — | table · หัวคอลัมน์ **หมายเลขโค้ด · สถานะ · มอบหมายให้ · หมายเหตุ** + ปุ่ม **Create Code** | ☐ |
| 2 | VERIFY แถว 0101 / 0102 (OCCUPIED) | — | 0101 pill **ใช้งานอยู่** · มอบหมายให้ **สมชาย ใจกล้า** · หมายเหตุ "โค้ดหลักโซนเหนือ" · 0102 pill **ใช้งานอยู่** · บุญมี ทองดี | ☐ |
| 3 | VERIFY แถว 0103 (EMPTY) | — | pill **ว่าง** · มอบหมายให้ **—** · หมายเหตุ "สำรอง" | ☐ |

### TC-E02 — สร้าง Extension Code สำเร็จ (happy — AC-17) ★
- group: E · ความสำคัญ: สูงสุด · trace: AC-17 / BR-AP-03 / BR-AP-09 (audit)
- Setup: seed=default (AR-0005 · Active · 0 codes) · files=—
- Start: OPEN `#/areas/AR-0005` → แท็บ **Extension Codes** → CLICK **Create Code**
- ชุดข้อมูล: C1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Create Code** | — | modal **สร้าง Extension Code** · sub "เลือกได้เฉพาะพื้นที่ที่เปิดใช้งาน · หมายเลขโค้ด 4 หลัก" · dropdown default = พื้นที่ปัจจุบัน · โค้ด placeholder **เช่น 0123** | ☐ |
| 2 | TYPE หมายเลขโค้ด **0501** → CLICK **สร้างโค้ด** → WAIT | C1 | modal ปิด + toast **สร้างโค้ดสำเร็จ** | ☐ |
| 3 | VERIFY แท็บ Extension Codes | — | แถวใหม่ **0501** · สถานะ **ว่าง** (EMPTY · assigned null) · แท็บ **Extension Codes (1)** | ☐ |

### TC-E03 — ไม่เลือกพื้นที่ → block (negative — AC-18 / VR-04)
- group: E · ความสำคัญ: สูง · trace: AC-18 / VR-04
- Setup: seed=default · files=—
- Start: OPEN `#/roles` → sub-tab **Extension Officers** → CLICK **Create Code**
- ชุดข้อมูล: C2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (เปิดจาก Roles → area dropdown ค่าเริ่ม **— เลือกพื้นที่ —**) TYPE โค้ด 0101 · เว้นพื้นที่ → CLICK **สร้างโค้ด** | C2 | warning **กรุณาเลือกพื้นที่** · ไม่สร้าง | ☐ |

### TC-E04 — โค้ดไม่ใช่ 4 หลัก → block (negative — AC-19 / VR-01 / EC-04 / BR-AP-11)
- group: E · ความสำคัญ: สูง · trace: AC-19 / VR-01 / EC-04 / BR-AP-11
- Setup: seed=default · files=—
- Start: OPEN `#/areas/AR-0001` → แท็บ **Extension Codes** → CLICK **Create Code**
- ชุดข้อมูล: C3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกพื้นที่ AR-0001 · TYPE โค้ด **12** (2 หลัก) → CLICK **สร้างโค้ด** | C3 | toast **รูปแบบหมายเลขโค้ดไม่ถูกต้อง** (desc **กรอกตัวเลข 4 หลัก เช่น 0123**) · ไม่สร้าง | ☐ |

### TC-E05 — dropdown แสดงเฉพาะพื้นที่ Active (EC-03 / BR-AP-03)
- group: E · ความสำคัญ: สูง · trace: EC-03 / BR-AP-03 (Active-only dropdown)
- Setup: seed=default (AR-0003 = Inactive) · files=—
- Start: OPEN `#/roles` → sub-tab **Extension Officers** → CLICK **Create Code**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด dropdown **เลือกพื้นที่** | — | ตัวเลือก = 4 พื้นที่ Active (AR-0001/0002/0004/0005) · **AR-0003 (Inactive) ไม่อยู่ในรายการ** | ☐ |

### TC-E06 — สร้างโค้ดซ้ำในพื้นที่ → block (negative — EC-06 concept)
- group: E · ความสำคัญ: กลาง · trace: dup code guard
- Setup: seed=default (AR-0001 มีโค้ด 0101 แล้ว) · files=—
- Start: OPEN `#/areas/AR-0001` → แท็บ **Extension Codes** → CLICK **Create Code**
- ชุดข้อมูล: C4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกพื้นที่ AR-0001 · TYPE โค้ด **0101** (ซ้ำ) → CLICK **สร้างโค้ด** | C4 | warning **หมายเลขโค้ดนี้มีอยู่แล้วในพื้นที่** · ไม่สร้าง | ☐ |

---

## Group F — Roles Directors (US-06)

### TC-F01 — Roles tab + 3 sub-tabs + Directors table (AC-21/24)
- group: F · ความสำคัญ: สูง · trace: AC-21, AC-24 / roles page
- Setup: seed=default (role=System Admin) · files=—
- Start: OPEN `#/areas` → CLICK top tab **Roles**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK top tab **Roles** | — | URL **#/roles** · หัวข้อ **บทบาท (Roles)** · sub "จัดการบทบาทระดับโลก: Directors, Area Heads และ Extension Officers" | ☐ |
| 2 | VERIFY sub-tabs | — | **Directors (1)** · **Area Heads (3)** · **Extension Officers (4)** | ☐ |
| 3 | VERIFY Directors table (default) | — | 1 แถว: ดำรง ผู้นำชัย (E06 · damrong@wkn.co.th · บริหาร/ผู้อำนวยการ) · คอลัมน์ รหัสพนักงาน/ชื่อ-สกุล/Email/แผนก-ตำแหน่ง/มอบหมายเมื่อ/ลบ | ☐ |

### TC-F02 — เพิ่ม Director สำเร็จ (happy — AC-22 / XT-01 / VR-05)
- group: F · ความสำคัญ: สูง · trace: AC-22 / XT-01 / VR-05 / BR-AP-10
- Setup: seed=default · files=—
- Start: OPEN `#/roles` → sub-tab **Directors** → CLICK **เพิ่ม Director**
- ชุดข้อมูล: D4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่ม Director** | — | modal **เพิ่ม Director** · ช่องค้น ERP · ปุ่ม **เพิ่ม** disabled (VR-05 — ต้องเลือกก่อน) | ☐ |
| 2 | TYPE "บุญมี" → เลือก **บุญมี ทองดี · E02** (active) → CLICK **เพิ่ม** → WAIT | D4 | modal ปิด + toast **เพิ่ม Director สำเร็จ** | ☐ |
| 3 | VERIFY Directors table | — | 2 แถว (ดำรง ผู้นำชัย + บุญมี ทองดี) · sub-tab **Directors (2)** | ☐ |

### TC-F03 — เพิ่ม Director inactive → block (negative — VR-06 / BR-AP-06)
- group: F · ความสำคัญ: สูง · trace: VR-06 / BR-AP-06 (active-only)
- Setup: seed=default (E07 inactive) · files=—
- Start: OPEN `#/roles` → sub-tab **Directors** → CLICK **เพิ่ม Director**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "สมหญิง" → เลือก **สมหญิง ลาพัก · E07** (inactive) → CLICK **เพิ่ม** → WAIT | — | block + toast **พนักงานไม่active** (desc "ไม่สามารถมอบหมายพนักงานที่ไม่ได้ใช้งานเป็น Director") | ☐ |

### TC-F04 — ลบ Director → confirm → success (AC-22 / EC-09)
- group: F · ความสำคัญ: สูง · trace: AC-22 / EC-09
- Setup: seed=default (Director: E06) · files=—
- Start: OPEN `#/roles` → sub-tab **Directors**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม ลบ (trash) บนแถว **ดำรง ผู้นำชัย** | — | confirm modal **ยืนยันลบ Director?** · ปุ่ม **ลบ Director** (danger) + **ยกเลิก** | ☐ |
| 2 | CLICK **ลบ Director** → WAIT | — | modal ปิด + toast **ลบ Director สำเร็จ** · Directors table ว่าง → empty **ยังไม่มี Director** · sub-tab **Directors (0)** | ☐ |

### TC-F05 — ค้นหา Director ในตาราง (AC-22)
- group: F · ความสำคัญ: กลาง · trace: AC-22 / directors search filter
- Setup: seed=default · files=—
- Start: OPEN `#/roles` → sub-tab **Directors**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ดำรง" → ช่อง **ค้นหา Director (ชื่อ / รหัส / email)** | — | เหลือแถว ดำรง ผู้นำชัย | ☐ |
| 2 | ล้าง → TYPE "ไม่มีคนนี้" | — | Directors table ว่าง (ไม่ตรงคำค้น) | ☐ |

---

## Group G — Roles Area Heads + Extension Officers (US-06)

### TC-G01 — Roles Area Heads (global) ครบทุกพื้นที่ (AC-24)
- group: G · ความสำคัญ: สูง · trace: AC-24 / global heads list
- Setup: seed=default (heads global = 3) · files=—
- Start: OPEN `#/roles` → CLICK sub-tab **Area Heads**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK sub-tab **Area Heads (3)** | — | table · คอลัมน์ **ชื่อ-สกุล · Email · พื้นที่ · มอบหมายเมื่อ** · 3 แถว | ☐ |
| 2 | VERIFY แถว | — | สมชาย ใจกล้า (E01 · พื้นที่ภาคกลาง AR-0001) · วิภา แก้วมณี (E05 · AR-0001) · ประเสริฐ สุขใจ (E03 · พื้นที่ภาคเหนือ AR-0002) | ☐ |

### TC-G02 — Extension Officers: filter พื้นที่ (AC-23 / BR-AP-05)
- group: G · ความสำคัญ: สูง · trace: AC-23 / BR-AP-05 (officer = code assignment)
- Setup: seed=default (7 codes) · files=—
- Start: OPEN `#/roles` → CLICK sub-tab **Extension Officers**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK sub-tab **Extension Officers (4)** | — | table · คอลัมน์ **หมายเลขโค้ด · พื้นที่ · มอบหมายให้ · สถานะ · เปิด** · 7 แถว (cross-area) | ☐ |
| 2 | SELECT filter พื้นที่ = **พื้นที่ภาคกลาง** (AR-0001) | — | เหลือ 3 แถว: 0101 (สมชาย ใจกล้า · ใช้งานอยู่) · 0102 (บุญมี ทองดี · ใช้งานอยู่) · 0103 (— · ว่าง) | ☐ |
| 3 | SELECT filter พื้นที่ = **ทุกพื้นที่** | — | กลับ 7 แถว | ☐ |

### TC-G03 — Extension Officers: filter สถานะ EMPTY/OCCUPIED (AC-23)
- group: G · ความสำคัญ: สูง · trace: AC-23 / status filter
- Setup: seed=default · files=—
- Start: OPEN `#/roles` → sub-tab **Extension Officers**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT filter สถานะ = **ใช้งานอยู่ (OCCUPIED)** | — | เหลือ 4 แถว (0101/0102/0201/0401) · ทุกแถว pill **ใช้งานอยู่** | ☐ |
| 2 | SELECT filter สถานะ = **ว่าง (EMPTY)** | — | เหลือ 3 แถว (0103/0202/0402) · ทุกแถว pill **ว่าง** · มอบหมายให้ **—** | ☐ |

### TC-G04 — Extension Officers: filter ว่างเปล่า (AC-23 / empty)
- group: G · ความสำคัญ: กลาง · trace: AC-23 / empty filter
- Setup: seed=default (AR-0005 · 0 codes) · files=—
- Start: OPEN `#/roles` → sub-tab **Extension Officers**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT filter พื้นที่ = **พื้นที่เชียงใหม่รอบนอก** (AR-0005 · ไม่มีโค้ด) | — | table ว่าง + empty state **ไม่พบ Extension Codes** (desc "ลองปรับตัวกรองพื้นที่หรือสถานะ") | ☐ |

---

## Group H — Audit timeline (append-only) (US-07)

### TC-H01 — Audit timeline seed (AC-25 / BR-AP-09)
- group: H · ความสำคัญ: กลาง · trace: AC-25 / BR-AP-09 / timeline
- Setup: seed=default (AR-0001 · 4 audit) · files=—
- Start: OPEN `#/areas/AR-0001` → CLICK แท็บ **Audit**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **Audit** | — | timeline 4 รายการ (เรียงใหม่→เก่า) · แต่ละรายการมี action badge + actor **สมพร วงศ์ทะเบียน** + timestamp + details | ☐ |
| 2 | VERIFY รายการบนสุด/ล่างสุด | — | บนสุด badge **แก้ไขพื้นที่** ("ปรับปรุงข้อมูลที่อยู่พื้นที่") · ล่างสุด badge **สร้างพื้นที่** ("สร้างพื้นที่: พื้นที่ภาคกลาง") | ☐ |
| 3 | VERIFY badge อื่น | — | มี badge **สร้างโค้ด** ("สร้าง Extension Code: 0101") · **เพิ่มหัวหน้า** ("เพิ่มหัวหน้าพื้นที่: สมชาย ใจกล้า") | ☐ |

### TC-H02 — Audit append หลังเพิ่มหัวหน้า (XT-05 / BR-AP-09)
- group: H · ความสำคัญ: กลาง · trace: XT-05 / audit append (ไม่แก้ของเดิม)
- Setup: seed=default (AR-0004 · 0 heads · audit ว่าง) · files=—
- Start: OPEN `#/areas/AR-0004` → แท็บ **Audit**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **Audit** | — | empty state **ยังไม่มีประวัติการเปลี่ยนแปลง** (AR-0004 ยังไม่มี audit) | ☐ |
| 2 | แท็บ **Area Heads** → **เพิ่มหัวหน้าพื้นที่** → เลือก วิไล งามตา (E04) → **เพิ่ม** → กลับแท็บ **Audit** | — | มีรายการใหม่ badge **เพิ่มหัวหน้า** · actor **สมพร วงศ์ทะเบียน** · details "เพิ่มหัวหน้าพื้นที่: วิไล งามตา" (append entry ใหม่) | ☐ |

### TC-H03 — Audit before/after snapshot (BR-AP-09) (ต้อง simulate)
- group: H · ความสำคัญ: กลาง · trace: BR-AP-09 / XT-05 · **prototype: details string เท่านั้น · snapshot diff จริง = SIT**
- Setup: **simulate — ระบบจริง** · files=—
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): mutation ใด ๆ → AuditEntry เก็บ before/after JSON | — | append-only entry มี before/after snapshot ครบ · ของเดิมไม่ถูกแก้ (prototype เก็บแค่ details string) | ☐ (ต้อง simulate) |

---

## Group I — RBAC (write-gate + Roles tab) (US-08)

### TC-I01 — System Admin เห็นปุ่ม write + Roles tab (AC-26 / BR-AP-07)
- group: I · ความสำคัญ: สูง · trace: AC-26 / BR-AP-07 · demo role = System Admin
- Setup: seed=default (CURRENT_ROLE=System Admin · canWrite=true) · files=—
- Start: OPEN `#/areas`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY top tabs + list buttons | — | top tab **Roles** แสดง · ปุ่ม **สร้างพื้นที่** + row-actions **แก้ไข**/toggle แสดงครบ | ☐ |
| 2 | OPEN detail AR-0001 → VERIFY header + tabs | — | ปุ่ม **แก้ไข** · **ปิดใช้งาน** แสดง · แท็บ Area Heads มีปุ่ม **เพิ่มหัวหน้าพื้นที่** · Extension Codes มีปุ่ม **Create Code** | ☐ |
| 3 | VERIFY user chip (มุมขวาบน) | — | แสดง **สมพร วงศ์ทะเบียน** · role **ผู้ดูแลระบบ (System Admin) · WKN** | ☐ |

### TC-I02 — Non-SA/Director: read-only (Roles tab + write ซ่อน) (AC-27 / EC-07 / BR-AP-07) (ต้อง simulate)
- group: I · ความสำคัญ: สูง · trace: AC-27 / EC-07 / BR-AP-07 · **prototype fix role=SA · สลับ role ไม่ได้ — SIT**
- Setup: **simulate — ระบบจริง:** role = Area Head / Extension Officer / Audit-QA (canWrite=false)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): เปิดหน้าด้วย role ที่ไม่ใช่ SA/Director | — | top tab **Roles** ซ่อน · ปุ่ม **สร้างพื้นที่**/แก้ไข/toggle/เพิ่มหัวหน้า/Create Code ซ่อนทั้งหมด (read-only) | ☐ (ต้อง simulate) |
| 2 | VERIFY (ระบบจริง): navigate `#/roles` ตรง ๆ ด้วย role read-only | — | redirect กลับ `#/areas` (guard ป้องกันเข้า roles) | ☐ (ต้อง simulate) |

### TC-I03 — RBAC server 403 บน write (XT-04 / §5.3) (ต้อง simulate)
- group: I · ความสำคัญ: สูง · trace: XT-04 / §5.3 · **prototype: guard ฝั่ง client เท่านั้น — 403 จริง = SIT**
- Setup: **simulate — ระบบจริง:** POST create/toggle/head ด้วย role ไม่มีสิทธิ์
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): user ไม่มีสิทธิ์ ยิง mutation | — | HTTP 403 **ไม่มีสิทธิ์ดำเนินการ** (server-enforced · ไม่พึ่งการซ่อนปุ่มฝั่ง client) | ☐ (ต้อง simulate) |

---

## Group J — Cross-module / event XT-01..05 + simulate (06_TESTS §6.9) ⭐

### TC-J01 — XT-01: ERP snapshot (add head/director active) ★
- group: J · ความสำคัญ: สูงสุด · trace: XT-01 / BR-AP-06/10
- Setup: seed=default · files=—
- Start: OPEN `#/areas/AR-0004` → แท็บ **Area Heads** → CLICK **เพิ่มหัวหน้าพื้นที่**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "prasert" (email/รหัส) → VERIFY ค้นได้ทั้ง ชื่อ/รหัส/email | — | option **ประเสริฐ สุขใจ · E03 · prasert@wkn.co.th** (ค้นด้วย email match) | ☐ |
| 2 | เลือก **ประเสริฐ สุขใจ** → **เพิ่ม** → WAIT | — | toast **เพิ่มหัวหน้าพื้นที่สำเร็จ** · แถวใหม่ snapshot ชื่อ = ประเสริฐ สุขใจ + email = prasert@wkn.co.th (ตรงต้นทาง ERP) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): ERP HR read-only | — | ERP verified · GET only · ไม่สร้างพนักงานใหม่ (BR-AP-10) | ☐ (ต้อง simulate) |

### TC-J02 — XT-02: geography master cascade ตรงลำดับ
- group: J · ความสำคัญ: สูง · trace: XT-02 / BR-AP-02
- Setup: seed=default · files=—
- Start: OPEN `#/areas` → CLICK **สร้างพื้นที่**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT จังหวัด **กรุงเทพมหานคร** → อำเภอ **เขตบางรัก** → ตำบล **สีลม** | — | อำเภอ/ตำบล กรองตามลำดับ · postal auto **10500** (ตรง master) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): Geo master read | — | อำเภอ/ตำบล/postal จาก Geo master จริง (prototype = fixed 3 จังหวัด mock) | ☐ (ต้อง simulate) |

### TC-J03 — XT-03: area_id → scope Farmer/Quota (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-03 · **prototype: no Farmer/Quota link — SIT**
- Setup: **simulate — ระบบจริง:** area_id ใช้ scope เกษตรกร/โควตา
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): F-AGM-001/002 อ่าน area_id เพื่อ scope | — | เกษตรกร/โควตา ผูก area_id (idempotent) · เปลี่ยนพื้นที่ = re-scope ตาม | ☐ (ต้อง simulate) |

### TC-J04 — XT-04: RBAC enforce 403 (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-04 / §5.3 · **prototype single-role SA — SIT**
- Setup: **simulate — ระบบจริง:** write ด้วย role ไม่ใช่ SA/Director
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): write (create/edit/toggle/roles) = 403 ถ้าไม่ใช่ SA/Director | — | 403 **ไม่มีสิทธิ์ดำเนินการ** · server-enforced (ไม่พึ่งซ่อนปุ่ม) | ☐ (ต้อง simulate) |

### TC-J05 — XT-05: audit append-only ทุก mutation
- group: J · ความสำคัญ: สูง · trace: XT-05 / BR-AP-09
- Setup: seed=default · files=—
- Start: OPEN `#/areas/AR-0005` → toggle → แท็บ **Audit**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (AR-0005 · 0 codes) CLICK toggle (power) ในแถว/header → กลับ detail แท็บ **Audit** | — | มีรายการ audit ใหม่ badge **แก้ไขพื้นที่** ("ปิดใช้งานพื้นที่") · ของเดิมไม่ถูกลบ/แก้ (append-only) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): before/after snapshot | — | AuditEntry เก็บ before/after JSON ครบ (prototype = details string) | ☐ (ต้อง simulate) |

### TC-J06 — optimistic 409 / idempotent dup / assign-unassign stub (EC-10..13 / VR-03) (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: EC-10, EC-11, EC-12, EC-13, VR-03 · **prototype single-session · ไม่มี assign UI — SIT**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): assign code (EMPTY→OCCUPIED) / unassign (OCCUPIED→EMPTY) | — | code เปลี่ยนสถานะผ่าน assign/unassign (EC-10/11 · prototype ไม่มีปุ่ม assign) | ☐ (ต้อง simulate) |
| 2 | VERIFY (ระบบจริง): 2 sessions — B commit ด้วย version เก่า | — | 409 **ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช** (EC-12) | ☐ (ต้อง simulate) |
| 3 | VERIFY (ระบบจริง): POST mutation ซ้ำ idempotency-key เดิม | — | 409 **รายการซ้ำ (idempotent)** / no-op (EC-13) | ☐ (ต้อง simulate) |
| 4 | VERIFY (ระบบจริง): email format จาก ERP snapshot | — | email ผ่าน format validation (VR-03 · inline · prototype ใช้ email จาก ERP) | ☐ (ต้อง simulate) |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `area-permission-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock in-memory, refresh = reset seed 5 พื้นที่ + 7 codes + 3 heads + 1 director + 7 ERP employees + 4 audit (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/VERIFY/WAIT)
4. `WAIT` = รอ ≤3s จน Expected ปรากฏ (toast มุมขวาล่าง · action ~0.5s · toast แสดง ~3.2-4.2s)
5. **Deactivate guard:** พื้นที่ Active ที่มี codes > 0 → กด toggle จะได้ `ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้` · status ไม่เปลี่ยน · เฉพาะ codes=0 หรือ Inactive→Active จึงได้ `เปลี่ยนสถานะสำเร็จ`
6. **Geography cascade:** อำเภอ disabled จนเลือกจังหวัด · ตำบล disabled จนเลือกอำเภอ · postal auto-fill จากตำบล · เปลี่ยนจังหวัด = reset ชั้นล่างทั้งหมด
7. **ERP active guard:** เพิ่ม head/director ได้เฉพาะ employee `active` · E07 (สมหญิง ลาพัก) = inactive → `พนักงานไม่active`
8. **RBAC:** demo fix role=System Admin → ปุ่ม write + Roles tab แสดงครบ · เคส read-only + 403 = `(ต้อง simulate)`
9. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
10. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 27 / 27 (AC-01..27 · AC-27 = simulate) |
| Cross-Module / Event (XT-01..05) | 5 / 5 (XT-03/04 = simulate) |
| Business rules (BR-AP-01..11) | 11 / 11 |
| Validation (VR-01..06) | 6 / 6 (VR-03 = simulate) |
| Edge cases (EC-01..13) | 13 / 13 (EC-07/10/11/12/13 = simulate) |
| Error catalog (UI-observable) | ครบ · guard/validation บน prototype · 403/409 = simulate |
| Permission cells | SA allow ครบ · read-only/Manager = simulate |
| org-geography + RBAC + Audit append-only | ครบทุกชั้น (Area/Code/Head/Director/Audit) |

- **Manifest cross-check (FRD §0.12): ✅ 27 AC + 5 XT + 11 BR + 6 VR + 13 EC — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT
- TC-A04 no-data variant (ระบบไม่มีพื้นที่เลย — seed มี 5 เสมอ)
- TC-A05 step 5 (ไฟล์ CSV จริง — server-side)
- TC-A06 step 3 (ฟอร์มแก้ไขพื้นที่จริง — editArea = stub)
- TC-H03 (audit before/after snapshot diff จริง)
- TC-I02 (non-SA/Director read-only — role fix ที่ SA)
- TC-I03 / TC-J04 (RBAC 403 server-enforced)
- TC-J03 (area scope → Farmer/Quota จริง)
- TC-J05 step 2 (before/after snapshot)
- TC-J06 (assign/unassign code · optimistic 409 stale · idempotent dup · email format VR-03)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-009",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-A01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 52, "pass": 0, "fail": 0, "blocked": 0 }
}
```
