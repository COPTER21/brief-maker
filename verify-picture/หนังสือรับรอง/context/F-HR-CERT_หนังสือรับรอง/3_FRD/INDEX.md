# INDEX — FRD Pack · F-HR-CERT · Employment / Salary Certificate (หนังสือรับรอง)

**Variant: FULL (9 ไฟล์ + INDEX + PRINT_SPEC)** · สร้างโดย `frd-generator-v6` Lane Mode v2 · 2026-08-30
**Phase 3.5: ✅ PASSED (A–M)** — รายงานเต็มอยู่ท้ายไฟล์นี้

## 📂 Pack Contents

| ไฟล์ | Audience | เนื้อหาหลัก |
|---|---|---|
| `00_OVERVIEW.md` | ทุกคน | Document control · Scope + Phase 2.5 probing 8 ข้อ · Roles COSO · Dependencies · **§0.12 Coverage Manifest (97 FN)** · ⭐ **§0.13 Published Certificate Surface** (อ่านอะไรจากต้นทางทั้ง 4 · เผยแพร่อะไร · **ไม่เขียนกลับที่ใดเลย**) · ⭐ **§0.14 Point-in-Time Contract (`CI-1…CI-9`)** · §0.15 Soft Reference · **§0.16 Declaration Conformance** |
| `01_UI.md` | FE | **§1.0 Layout Decision Log** + ⭐ **§1.0.1 DIV-CT-01** · Page Inventory 4 หน้า · ตัวช่วย 5 ขั้น · มุมมองใบ 4 แท็บ · COSO touchpoints · ⭐ **§1.5 สิ่งที่ต้องไม่มี 18 ข้อ** |
| `02_API.md` | BE (HTTP) | 30 endpoint + **11 cross-module outbound** · contract ของ 6 ตัวที่มีสัญญาเฉพาะ · **§2.4 API → Logic Trace** · **§2.5 Cross-Module Contract** · §2.6 Inbound Event Listener |
| **`03_LOGIC.md`** ⭐ | BE (ตรรกะ) | ⭐⭐ **§3.0 กลไกหลัก 7 หัวข้อ (หัวใจของแพ็ก)** · **44 Function** · **8 Engine (ใหม่ 4)** · Trace |
| `04_DB.md` | DBA / BE | 6 ตาราง + 1 view · classification ครบทุกคอลัมน์ · ER · index · ⭐ **§4.7 append-only enforcement 10 ข้อ** · migration |
| `05_RULES.md` | BE + QA | BR-01…BR-28 พร้อมจุดบังคับใช้ · state machine 9 สถานะ/12 transition · permission · edge case 43 · **error catalog 26 code** · **§5.7 D-CLASS** · **§5.8 Functions Cut 10** · **§5.9 Declaration Rules** |
| `06_TESTS.md` | QA | **AT-01…AT-118** · ⭐⭐ **IA-01…IA-14 (ตกข้อใดข้อหนึ่ง = หยุดปล่อยรุ่น)** · **CM-01…CM-12** · test data 22 ชุด · DoD · **microcopy verbatim 28 ข้อความ** |
| `07_LOCKED_DECISIONS.md` | ทุกคน | ⭐ **§7.0 Scope Lock 16 ข้อ (IMMUTABLE)** · LD-CERT-01…14 · Convention deviation 4 · **OQ 33 ข้อ** · tradeoff 8 |
| **`PRINT_SPEC.md`** ⭐ | ทีมทำเอกสาร | field mapping ของหนังสือ · กติกาการพิมพ์ · ช่องลงนาม 2 ช่องคงที่ · ⭐⭐ **§P.2 rendition matrix เต็ม (ไทย/อังกฤษ × มี/ไม่มีเงินเดือน) + สามข้อห้าม** · §P.4 ข้อความตาม `employment_state` + ข้อห้ามตามกฎหมาย |
| `INDEX.md` | ทุกคน | ไฟล์นี้ |
| `UI_BRIEF_หนังสือรับรอง.md` | FE + BA | (สร้างที่ S7) สรุปหน้าจอ + **Drift Log** |

## 🔍 Quick Nav by Question

| คำถาม | ไปที่ |
|---|---|
| ⭐⭐ **ตอนกดออกหนังสือ ระบบทำอะไรบ้าง ลำดับไหน** | **`03_LOGIC §3.0.1`** · `02_API §2.2 API-11` |
| ⭐⭐ **ทำไมสายอนุมัติไม่ได้มาจากตัวเลขเงิน** | **`03_LOGIC §3.0.2`** · `00_OVERVIEW §0.14.1` |
| ⭐⭐ **ไม่มีสิทธิ์เห็นค่าจ้างแล้วเกิดอะไร** | **`03_LOGIC §3.0.3`** · `PRINT_SPEC §P.2.3` |
| ⭐ **เพิกถอนกับออกใหม่แทน ต่างกันตรงไหน ทำอะไรก่อนอะไร** | **`03_LOGIC §3.0.4`** |
| ⭐ **อดีตพนักงานขอหนังสือได้ไหม** | **`03_LOGIC §3.0.5`** · `06_TESTS IA-13` |
| ⭐⭐ **ทำไมไม่มีช่องหมายเหตุ** | **`03_LOGIC §3.0.6`** · `PRINT_SPEC §P.4.1` |
| **นโยบายที่ต้นทางยังไม่เผยแพร่ ทำยังไง** | **`03_LOGIC §3.0.7`** · `07_LOCKED OQ-STD-CT3` |
| **มีคำสั่งโยกย้ายที่รอมีผล จะเกิดอะไร** | `03_LOGIC §3.0.1(ค)` · `06_TESTS IA-08` |
| **ต้นทางเปลี่ยนหลังหนังสือออกไปแล้ว** | `03_LOGIC §3.0.1(ช)` · `06_TESTS IA-11` |
| **feature อื่นอ่านอะไรจากที่นี่ได้บ้าง** | **`00_OVERVIEW §0.13`** |
| **ฟีเจอร์นี้เขียนอะไรกลับไปที่ไหนบ้าง** | ⭐ **`00_OVERVIEW §0.13.5` — ไม่เขียนกลับที่ใดเลย** |
| **หน้าจอมีกี่หน้า route อะไร** | `01_UI §1.1` |
| **ทำไมไม่ใช้ตัวแก้ไขบรรทัดมาตรฐาน** | `01_UI §1.0.1` · `07_LOCKED CV-01` |
| **endpoint ไหนเรียก function อะไร** | `02_API §2.4` · `03_LOGIC §3.3` |
| **คอลัมน์ไหนเป็นข้อมูลชั้นความลับ** | `04_DB §4.2` · `§4.6` · `05_RULES §5.7` |
| **error code มีอะไรบ้าง** | `05_RULES §5.6` |
| **ทดสอบอะไรบ้างก่อนปล่อยรุ่น** | `06_TESTS §6.6` · ⭐ **`§6.3 IA`** |
| **อะไรที่ห้ามเปลี่ยน** | `07_LOCKED §7.0` |
| **อะไรยังไม่เคาะ** | `07_LOCKED §7.3` |
| ⭐ **หนังสือมีกี่หน้าตา ต่างกันตรงไหน เลือกยังไง** | **`PRINT_SPEC §P.2`** |

## 🔗 Cross-Reference Tables

### FN → ไฟล์
ตารางเต็ม **97 แถว** อยู่ที่ **`00_OVERVIEW §0.12.0`**

### BR → ไฟล์
ตารางเต็ม **28 แถว** อยู่ที่ **`00_OVERVIEW §0.12.2`** · จุดบังคับใช้จริงที่ `05_RULES §5.1` · ข้อความเต็มที่ `BRD §9.1`

### State → Transition → Event

| สถานะ | เข้าโดย | ออกโดย | event ที่ยิง |
|---|---|---|---|
| `draft` | T-01 | T-02 · T-04 · (ลบ) | — |
| `pending_approval` | T-02 | T-03 · T-04 · T-05 | **`cert_requested`** (NTF) · (DOA ยิง `doa_pending` เอง) |
| `rejected` | T-03 | — | **`cert_rejected`** (NTF · ปิดไม่ได้) · (DOA ยิง `doa_result` เอง) |
| `cancelled` | T-04 | — | — |
| `approved` | T-05 | T-06 | **`cert_approved`** (NTF) |
| **`issued`** ⭐ | T-06 | T-07 · T-08 · T-09 | **`cert_issued`** · (`cert_ready_for_pickup` เมื่อรับที่ HR) · ⭐ **`cert.issued` (SecC E1)** |
| `delivered` | T-07 | T-08 · T-09 | ⭐ **`cert.delivered_external` (SecC E2)** |
| `revoked` | T-08 | — | **`cert_revoked`** (NTF · ปิดไม่ได้) · ⭐ **`cert.revoked` (SecC E5 · `reversal_of` → E1)** |
| `superseded` | T-09 | — | — (ผู้ขอได้ `cert_issued` ของฉบับใหม่อยู่แล้ว) |
| *(นาฬิกา)* ใบค้างเกินกำหนด | — | — | **`cert_pending_issue_overdue`** (T-10 · ⭐ ไม่เปลี่ยนสถานะ) |
| *(event ต้นทาง)* หลังออกแล้ว | — | — | ⭐ **ไม่ยิงอะไร — ติดธง `upstream_changed_flag` เท่านั้น** (T-11) |
| *(เปิด/ดาวน์โหลดไฟล์ที่มีตัวเลข)* | — | — | ⭐ **`cert.restricted_viewed` (SecC E3)** (T-12) |
| *(ถูกปฏิเสธเพราะไม่มีสิทธิ์)* | — | — | ⭐ **`cert.issue_blocked_masked` (SecC E4)** — ⭐ **ไม่มี transition รองรับ เพราะไม่ใช่การเปลี่ยนสถานะ** |

### Engine → ผู้ใช้

| Engine | สถานะ | เรียกจาก |
|---|---|---|
| ⭐⭐ **`certificate-fact-freeze-engine`** (ENG-01) | **candidate NEW** | `F-20 buildSnap` · `API-11` |
| ⭐⭐ **`document-rendition-selector`** (ENG-02) | **candidate NEW** | `F-22 selectRendition` · `API-11` · `API-13` |
| ⭐ **`cert-action-selector`** (ENG-03) | **candidate NEW** | `F-05 pickAction` · `API-06` · `API-07` |
| **`supersede-chain-engine`** (ENG-04) | **candidate NEW** | `F-34 searchRegister` · `API-19` |
| `salary-structure-resolve-client` (ENG-05) | existing | `F-20` · `F-17` · `X-API-01` |
| `hr-config-resolve-client` (ENG-06) | existing | `F-20` · `F-17` · `X-API-05` |
| `document-render-engine` (ENG-07) | existing | `F-23` · `API-13` |
| `doa-resolve-client` (ENG-08) | existing | `F-06` · `X-API-06` |

## 🚨 R8 Verification Matrix

| เกณฑ์ | ผล |
|---|---|
| ทุก mutation API มี ≥1 Function/Engine | ✅ 16/16 |
| ทุก Function ใน `03_LOGIC §3.1` ถูก trace | ✅ 44/44 |
| ทุก Engine ใน `03_LOGIC §3.2` ถูก trace | ✅ 8/8 |
| ไม่มี orphan Function/Engine | ✅ |
| ไม่มี `createX`/`updateX`/สูตรคำนวณ ซ่อนใน `02_API` | ✅ |

## 📊 Pack Statistics

| มิติ | จำนวน |
|---|---:|
| ไฟล์ในแพ็ก | **11** (9 + INDEX + PRINT_SPEC) |
| หน้าจอ / route | 4 / 4 |
| API endpoint | 30 (+ 11 cross-module outbound) |
| Function | 44 |
| Engine | 8 (**ใหม่ 4**) |
| ตาราง DB / view | 6 / 1 |
| Business Rule | 28 |
| Validation Rule | 32 |
| Error code | 26 |
| Edge Case | 43 (☑ 22 · ☐ 21) |
| Acceptance Test | 118 |
| **Invariant Assertion** | **14** |
| Cross-module test | 12 |
| FN ที่ครอบ | **97 / 97** |
| Story ที่ครอบ | **97 / 97** |
| Scenario ที่ครอบ | **44 / 44** |
| Transition | **12 / 12** |
| Functions Cut (ไม่รองรับ) | **10 / 10** |
| Open Question | **33** (30 จาก BRD + `OQ-FRD-CT-01…03`) |
| `[ASSUMED]`/`[AI-DRAFT]` จาก HTML | 10 |
| `[AI-DEFAULT]` จาก Phase 2.5 | 8 |
| NTF event | **7** |
| CSQ event | **5** (⭐ ท่อ SecC ท่อเดียว) |
| DOA action / matrix | **4 / 2** (⭐ ไม่มีวงเงิน) |
| DOCCFG doc_type | 1 |
| **PDF rendition** | **4** ⭐ |

## 🎯 Reading Order Recommendation

1. `00_OVERVIEW §0.3` (ขอบเขต) → ⭐ **`§0.13`** (อ่านอะไร เผยแพร่อะไร **ไม่เขียนกลับที่ใด**) → ⭐ **`§0.14`** (invariant)
2. ⭐⭐ **`03_LOGIC §3.0` ทั้งส่วน** — **อ่านก่อนเขียนโค้ดใด ๆ ที่แตะ `issue_date` หรือการอ่านต้นทาง**
3. `01_UI §1.0` + `§1.0.1` (ทำไมไม่มีตัวแก้ไขบรรทัด) + `§1.5` (สิ่งที่ต้องไม่มี 18 ข้อ)
4. `04_DB` (โดยเฉพาะ **§4.7**) → `02_API` → `03_LOGIC §3.1–§3.3`
5. `05_RULES` (ทั้งไฟล์) → ⭐ **`06_TESTS §6.3 IA`** (สิ่งที่ห้ามพลาด)
6. `07_LOCKED §7.0` + `§7.3` (อะไรห้ามเปลี่ยน · อะไรยังไม่เคาะ)
7. ⭐ **`PRINT_SPEC §P.2`** (เมื่อถึงงานเอกสาร) — อ่านคู่กับ `03_LOGIC §3.0.3`

## Coverage Manifest Pointer ⭐
**`00_OVERVIEW §0.12`** — FN 97/97 · Story 97/97 · BR 28/28 · Scenario 44/44 · Edge 43/43 · Functions Cut 10/10 · **ไม่มีแถวที่ "อยู่ที่" ว่าง**

---

## 🔍 Phase 3.5 Verification Report — FRD F-HR-CERT

```
### A. Pack Completeness
- [x] Variant decision (FULL) match เกณฑ์ fallback จาก BRD ✅ (pages=4 · states=9 ≥ 4 · approval=Yes · money-sensitive=Yes)
- [x] All expected files generated (9 + INDEX) ✅
- [x] 03_LOGIC.md exists ✅
- [x] INDEX.md cross-references all files ✅
- [x] **PRINT_SPEC.md present** ✅ (ท่อ PDF present → บังคับ)
      — ⭐ **และครอบ rendition matrix เต็มทั้ง 4 ตัว (ไทย/อังกฤษ × มี/ไม่มีเงินเดือน) พร้อมกติกาการเลือกแบบตายตัว
        และประกาศชัดว่าไม่มี rendition ที่ห้า (masked = REFUSE)** ✅ (§P.2)

### B. Function/API Coverage
- [x] 30 endpoint มี contract ครบ (6 ตัวที่มีสัญญาเฉพาะเขียนเต็ม · ที่เหลืออยู่ในตาราง §2.1 + §2.4) ✅
- [x] ทุก mutation API ระบุ Idempotency + row_version ✅
- [x] ⭐ **API-11 (จุดตรึงข้อเท็จจริง) ระบุลำดับ 10 ขั้นที่ห้ามสลับ พร้อมพฤติกรรมเมื่อตกด่านทุกกรณี** ✅

### C. R8 Logic Traceability
- [x] ทุก mutation API มี ≥1 Function/Engine ✅ 16/16
- [x] ทุก Function ถูก trace ✅ 44/44
- [x] ทุก Engine ถูก trace ✅ 8/8
- [x] ไม่มี orphan ✅

### D. API ↔ DB Linkage
- [x] ทุก API ที่เขียนข้อมูล ชี้ตารางที่มีอยู่จริงใน 04_DB ✅
- [x] read model (API-29) map กับ V_certificate_register ✅
- [x] ⭐ **T_certificate_snapshot มี trigger บล็อก UPDATE/DELETE (D1) และ T_certificate มี trigger
      บล็อกการแก้คอลัมน์ที่ตรึงเมื่อ status ≥ issued (D3)** ✅
- [x] ⭐ **CHECK constraint กันใบที่มีทั้ง revoked_at และ superseded_by (D6)** ✅
- [x] ⭐ **CHECK constraint บังคับ has_salary_figure = (cert_type = 'salary') (D8)** ✅

### E. UI ↔ API Cross-reference
- [x] P-01 ตัวช่วย 5 ขั้น → API-03/04/07/12/24/06 ✅
- [x] P-01 มุมมองใบ 4 แท็บ → API-02 (รายละเอียด) · API-13 (เอกสาร) · API-02 (ลายเซ็น) · API-17/18 (ประวัติ) ✅
- [x] P-01 ปุ่มตามสถานะ → API-06/08/09/10/11/14/15/16 ✅
- [x] P-02 → API-27 ✅ · P-03 → API-19 · API-20 · API-28 · API-30 ✅ · P-04 → API-26 · API-13 ✅

### F. Engine Iron Rules (CUBIC 3-layer)
- [x] ไม่มี Engine อ้างอิงสิ่งที่เป็น HTTP ✅
- [x] input/output เป็น object ล้วน ✅
- [x] feature ไม่ข้าม API ไปเรียก Engine ตรง ✅
- [x] **Engine ใหม่ทั้ง 4 ตัวไม่มีค่านโยบายอยู่ข้างใน (ค่าเป็น input เสมอ)** ✅
- [x] ⭐⭐ **ENG-03 cert-action-selector ไม่มี field ใดใน signature ที่รับจำนวนเงินหรือเปอร์เซ็นต์** ✅
- [x] ⭐⭐ **ENG-02 document-rendition-selector ไม่มีค่าคืนที่ห้า — masked คืน REFUSE ไม่ใช่ rendition ที่เว้นช่อง** ✅

### G. Logic Placement Compliance
- [x] ไม่มี createX/updateX แอบใน 02_API ✅
- [x] ไม่มี pure calculation แอบใน 02_API ✅
- [x] logic ที่ควรอยู่ 03_LOGIC อยู่จริงทั้งหมด ✅
- [x] ⭐ **buildSnap() · assertIssuable() · selectRendition() อยู่ที่ 03_LOGIC ทั้งหมด ไม่มีชิ้นใดกระจายไปอยู่ที่ 02_API** ✅

### H. Security Bible Application
- [x] Preset P6 (Sensitive Data Disclosure) เลือกแล้ว + 15 controls + เพิ่มนอก preset 2 ตัว ✅ (BRD §16 · 05_RULES §5.7)
- [x] บันทึกเหตุผลที่ไม่เลือก P2/P4/P-MAX ✅ (BRD §16.1)
- [x] ⭐ **Restricted fields → flag ใน Open Questions (wire Restricted Resources)** ✅ OQ-CT-14 · A-2
- [x] ⭐ **สองมาตรการนอก preset มาจากข้อกฎหมายไทยโดยตรง (C-16 ไม่มีช่องกรอกอิสระ · C-17 ไม่ปฏิเสธสิทธิโดยโครงสร้าง)** ✅

### I. Convention Compliance
- [x] API path `/api/v1/certificate/*` ✅
- [x] field_key = snake_case ✅
- [x] Function = camelCase ✅
- [x] Engine = kebab-case ✅
- [x] Error code = UPPER_SNAKE ✅
- [x] Status = snake_case ✅

### J. Data Classification (R10)
- [x] ทุกคอลัมน์ใน 04_DB §4.2/§4.3 มี Classification ✅
- [x] ทุกคอลัมน์มี PII flag ✅
- [x] §4.6 ครบ 6 subsection (.1–.6) ✅
- [x] 00_OVERVIEW §0.7.1 ระบุระดับสูงสุด (**Restricted**) ✅
- [x] 05_RULES §5.7 มีส่วน D-CLASS ✅
- [x] ไม่มี default = Public ✅ (**ไม่มีคอลัมน์ Public เลย**)
- [x] ⭐ **มี Restricted → ระบุการ wire Restricted Resources ใน Open Questions แล้ว** ✅
- [x] ⭐ **ระบุชัดว่า masked = true → ไม่มีแถว snapshot เกิดขึ้นเลย (ไม่ใช่ "มีแถวแต่คอลัมน์เป็น null")** ✅

### K. Coverage Manifest (R13)
- [x] ทุก Story ใน BRD §7 (97) มีแถว ✅
- [x] ทุก Rule ใน BRD §9 (28) มีแถว ✅
- [x] ทุก Edge ☑ (22) มีแถว ✅ · ☐ (21) มีแถว ✅
- [x] **ทุก FN (97) มีแถวพร้อมคอลัมน์ UI/API/LOGIC/RULES/TESTS** ✅
- [x] **Functions Cut 10/10 อยู่ในแมนิเฟสต์** ✅
- [x] ไม่มีแถวที่ "อยู่ที่" ว่าง ✅

### L. Scope Lock + Value Stream (R11/R12)
- [x] Scope Lock 16 ข้อ import ครบจาก BRD §3.4 → 07_LOCKED §7.0 ✅
- [x] ไม่มี spec ใดในแพ็กขัด LOCK ✅
- [x] 02_API มี Cross-Module Contract ครบตาม BRD §12.1 ✅ (X-API-01…11 + inbound listener)
- [x] 06_TESTS มี cross-module case ≥1 ต่อ upstream/downstream ที่มี data ไหล ✅ (CM-01…CM-12)
- [x] ⭐ **§0.13.5 ระบุทั้งสองทิศทาง — consumer เขียนเข้ามาไม่ได้ และ feature นี้ก็ไม่เขียนกลับไปที่ใดเลย** ✅

### M. HTML Alignment (v6.1)
- [x] จำนวนหน้าใน 01_UI = จำนวน route ใน HTML **เป๊ะ (4 = 4)** ✅
      (`#/cert/list` · `#/cert/inbox` · `#/cert/register` · `#/cert/mine`)
- [x] ทุก route ใน 01_UI มีจริงใน HTML ✅
- [x] Pattern (observed) ตรงกับที่จอใช้จริง — spot-check 6 จุด:
      · ตัวช่วย 5 ขั้น ชื่อขั้นตรงกับ `01_UI §1.2` ✅ (ผู้ขอและประเภท › รายละเอียดคำขอ › ข้อมูลที่จะปรากฏบนหนังสือ › ผู้อนุมัติ › ตรวจสอบและยืนยัน)
      · มุมมองใบ 4 แท็บ (`detail` · `pdf` · `sign` · `history`) บน `.drawer-header.has-tabs` เส้นเดียว ✅
      · `.slot-row` จำนวน slot ผันตามสายจริง (1 หรือ 2) ✅
      · `.filter-row` แถวเดียว (52px ค่าเดียวทุกจุด) ✅
      · `class="a4"` หน้าเอกสาร A4 1 หน้า · ช่องลงนาม 1 ช่อง + ที่ว่างตราบริษัท ✅
      · เอกสารแนบเป็น section ในแท็บรายละเอียด ไม่ใช่แท็บที่ 5 ✅
- [x] ⭐⭐ **การเลือกสายอนุมัติบนจอเป็นฟังก์ชันของประเภทหนังสือ ไม่ใช่ของจำนวนเงิน** ✅
- [x] 06_TESTS expected text ตรง verbatim — spot-check ≥6 ข้อความ:
      · `ต้องมีสิทธิ์เข้าถึงข้อมูลค่าจ้างจึงจะออกหนังสือประเภทนี้ได้` ✅
      · `มีคำสั่งที่จะมีผล {date} — หนังสือฉบับนี้ยังไม่รวมรายการนั้น` ✅
      · `ยังไม่ได้ตั้งค่า` ✅
      · `หนังสือรับรอง {cert_doc_no} ถูกเพิกถอน — กรุณาอย่าใช้ฉบับดังกล่าวต่อไป` ✅
      · `ข้อมูลต้นทางเปลี่ยนหลังออกหนังสือ — เนื้อหาของหนังสือไม่ถูกแก้` ✅
      · `ไม่พบรายการตามเงื่อนไข` ✅
- [x] ไม่พบ HTML-STANDARD CONFLICT ✅
- [!] **บันทึก 2 ข้อเบี่ยงที่ต้องให้คนรับทราบ (ไม่ใช่ conflict ของ spec):**
      · **DIV-CT-01 (CV-01)** — ไม่ใช้ตัวแก้ไขบรรทัดมาตรฐาน (line editor B2 v2)
        เพราะฟีเจอร์นี้ไม่มีรายการที่คนพิมพ์ และช่องกรอกอิสระขัด **BR-28 (ป.พ.พ. ม.585)** โดยตรง
        → `01_UI §1.0.1` · `07_LOCKED CV-01` · Drift Log ที่ S7 · `_NOTIFY.md`
      · **CV-02 (เครื่องมือ)** — บล็อก `doc_archetype` ของ `audit.sh` ผูกกับชื่อคลาส/ฟังก์ชันของ line editor B2 v2
        ซึ่งเอกสารใบนี้ต้องไม่มี → **ตรวจ Pattern Q surface ด้วยมือแทน (COVERAGE_R1 §5 · 7/7 ✓)**
        วิธีเดียวกับ F-HR-LEAVE · F-HR-OT · F-HR-MOVE → `_NOTIFY.md` ให้ Architect พิจารณาปรับเครื่องมือ

### Declaration Conformance (Lane Mode v2)
- [x] NTF 7 = 7 ✅ · CSQ 5 = 5 (⭐ ท่อ SecC ท่อเดียว) ✅ · DOA 4 action / 2 matrix ✅ · DOCCFG 1 ✅ · PDFDOC 1 (⭐ 4 rendition) ✅
- [x] **ไม่มี event ใหม่ที่ FRD คิดขึ้นเอง** ✅
- [x] ⭐ **สองชุด event disjoint สนิท** ✅ (`cert_*` underscore = NTF vs `cert.*` dot = SecC — ไม่มีชื่อซ้ำแม้แต่ตัวเดียว)
- [x] **ไม่มีใบใดประกาศซ้ำ `doa_pending` / `doa_result` / `doa_escalate`** ✅
- [x] ⭐ **ไม่มีใบใดประกาศท่อ `oc` · `dc` ระดับเอกสาร · `sc`** ✅ (เหตุผลรายท่อครบที่ `CSQ_BRIEF §3` · `05_RULES §5.9.2`)

### Verdict
✅ **All checks passed (A–M + Declaration Conformance) → deliver Pack**
   หมายเหตุ 2 ข้อ (DIV-CT-01 · CV-02) เป็นข้อเบี่ยงที่บันทึกไว้ครบพร้อมเหตุผลและเส้นทางส่งต่อ — ไม่ใช่ข้อบกพร่องของแพ็ก
```
