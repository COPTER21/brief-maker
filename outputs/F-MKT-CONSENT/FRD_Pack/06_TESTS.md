# 06_TESTS — F-MKT-CONSENT ความยินยอม PDPA

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + FN-40 Negative Locks + Cross-Module + DoD
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + `consent-pdpa.html` (e2e ผ่าน 32/32 · FN 20/20)
> **🚨 Expected text:** ยึด **ข้อความจริงบนจอ (verbatim)** จาก HTML ก่อน แล้ว fallback microcopy กลาง — ห้ามแต่งคำเอง (§6.10)

---

## §6.1 Acceptance Criteria (AC per FN — 20 FN บวก)

### AT-01 (FN-01): สร้างวัตถุประสงค์ + upload v1
**Given** role=dpo **When** สร้าง purpose (name + ≥1 channel + life 1–120 + แนบเอกสาร) **Then** 201 + `versions:[{v:1}]` + toast "สร้างวัตถุประสงค์ PUR-0x แล้ว"
**Negative:** ไม่แนบเอกสาร → 422 BR_DOCUMENT_REQUIRED + toast "ต้องแนบเอกสาร PDPA"

### AT-02 (FN-02): อัปโหลดเวอร์ชันใหม่
**Given** purpose มี consent v1 **When** อัปโหลดเอกสารใหม่ **Then** current_ver=2 + toast "ออกเอกสาร v2 แล้ว · N รายการต้องขอใหม่" + CSQ `policy.version_published`

### AT-03 (FN-03): ตาราง purpose + สถิติ
**When** GET /consent/purposes **Then** แสดง ยินยอม/ถอน/หมดอายุ/%ครอบคลุม ต่อ purpose

### AT-04 (FN-04 · EC-07): ปิด purpose
**When** ปิด purpose **Then** status=closed + toast "ปิดวัตถุประสงค์ PUR-0x แล้ว" **And** สร้างคำขอใหม่ไม่ได้ (BR_PURPOSE_CLOSED) **And** consent เดิมยังอยู่ (BR-17)

### AT-05 (FN-05): สร้างคำขอ single-screen
**When** สร้างคำขอ (subject + purposes + channel) **Then** 201 + link + QR + toast "สร้างคำขอ REQ-xxxx พร้อมลิงก์และ QR แล้ว" **And** ไม่มี stepper/wizard (LOCK-07)

### AT-06 (FN-06): ส่งทางอีเมล
**When** ส่งคำขอทางอีเมล **Then** status=pending + toast "บันทึกการส่งทางอีเมล (จำลอง...)" — ไม่ส่งจริง

### AT-07 (FN-07 · BR-18): ส่งซ้ำช่องทางอื่น
**When** ส่งซ้ำทาง LINE **Then** send record ครั้งที่ 2 ในคำขอเดิม **And** ไม่สร้างคำขอใหม่

### AT-08 (FN-08): คัดลอกลิงก์ / QR
**When** คัดลอกลิงก์ **Then** toast "คัดลอกลิงก์แล้ว" · ดาวน์โหลด QR → toast "ดาวน์โหลด QR ของ ... แล้ว (บันทึกการนำลิงก์ออก)"

### AT-09 (FN-09): ดาวน์โหลดเอกสารของคำขอ
**Then** เอกสารเวอร์ชันปัจจุบันของแต่ละ purpose

### AT-10 (FN-10): เซ็นผ่าน recipient view + evidence 5
**Given** recipient view เปิด **When** อ่านเอกสาร → verify → ยินยอม → ส่ง **Then** toast "บันทึกคำตอบแล้ว · ยินยอม N · ปฏิเสธ M (เก็บหลักฐานครบ 5 อย่าง)" + registry row granted + evidence 5 ฟิลด์ครบ
**Negative:** ไม่ verify → toast "กรุณายืนยันตัวตนก่อนส่งคำตอบ" (BR_IDENTITY_NOT_VERIFIED)

### AT-11 (FN-11 · EC-06): ยินยอมบางวัตถุประสงค์
**Given** คำขอ 3 purpose **When** ยินยอม 2 ปฏิเสธ 1 **Then** registry บันทึกแยกรายข้อ (2 granted + 1 declined) — ไม่ใช่ทั้งก้อน

### AT-12 (FN-12): ดูหลักฐาน 1 รายการ
**Then** เห็นครบ 5: answeredAt · requestChannel · idMethod · policyVersion · ipDevice

### AT-13 (FN-13): ทะเบียน + กรองทุกมิติ
**When** กรอง search/status/channel/purpose **Then** ตาราง triple ถูกกรองถูกต้อง

### AT-14 (FN-14): Customer 360
**When** เลือกลูกค้า **Then** เห็นทุก consent ของคนนั้นในที่เดียว

### AT-15 (FN-15 · BR-09/10): ถอนแทนลูกค้า
**When** ถอน (เหตุผล + ช่องทาง) **Then** status=withdrawn ทันที + toast "ถอนความยินยอมแล้ว — มีผลทันที..." **And** ไม่มีขั้นอนุมัติ (LOCK-04)
- **AT-15b (EC-02):** ถอนแล้ว resolve triple เดิม → allowed:false ทันที
- **AT-15c (EC-08):** CSQ `consent.withdrawn` มี reversal_of=grant_event_id (ไม่ลบผลเดิม)
**Negative:** ไม่กรอกเหตุผล → toast "กรอกเหตุผล" · ไม่เลือกช่องทาง → toast "เลือกช่องทางที่ลูกค้าแจ้งมา"

### AT-16 (FN-16 · BR-12): รายการใกล้หมดอายุ ≤30 วัน
**Then** แสดงรายการ daysLeft 0–30 เรียงวันหมด · เตือนไม่บล็อก · กดต่ออายุได้

### AT-17 (FN-17 · BR-13): ต่ออายุ
**When** ต่ออายุจาก near-expiry **Then** สร้างคำขอใหม่อ้างเดิม (ref_old) + CSQ `consent.renew_requested` **And** ไม่แก้ expires_at เดิม

### AT-18 (FN-18 · BR-16): ประวัติ 1 รายการ
**Then** timeline append-only เรียงเวลา + เหตุผลทุกครั้ง (ขอ→ยินยอม→ถอน→ขอใหม่)

### AT-19 (FN-19): resolve simulator
**When** subject+purpose+channel=granted **Then** 200 + `allowed:true, status:"granted"` + reason + ตัวอย่าง JSON
- **AT-19b:** withdrawn → allowed:false reason "ถอนความยินยอมแล้ว..."
- **AT-19c (EC-03):** stale → allowed:false reason "ยินยอมไว้กับนโยบายเวอร์ชัน 1 แต่เวอร์ชันปัจจุบันคือ 2..."
- **Negative:** ไม่ครบ 3 ช่อง → toast "เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสอบ"

### AT-20 (FN-20 · EC-01): never_asked
**When** resolve triple ที่ไม่เคยมี record **Then** 200 + `allowed:false, status:"never_asked", found:false` + reason "ยังไม่เคยขอความยินยอมสำหรับคู่นี้ — ค่าเริ่มต้นคือส่งไม่ได้" — **ไม่ใช่ 404 · ไม่ใช่ declined**
- **AT-20b (EC-05):** pending เกิน 30 วัน → resolve reason "...การไม่ตอบไม่ใช่การยินยอม" (lapsed≠declined)

### AT-ID (EC-04): idempotency — double-submit → 1 record (Idempotency-Key)
### AT-VER-lock (EC-11): 2 dpo ออกเวอร์ชันพร้อมกัน → 409 ERR_STALE_DATA

---

## §6.2 FN-40 Negative Lock Tests (ต้องไม่มี — render จริงแล้ว assert absent · e2e ผ่าน 10/10)

| ID | ต้องไม่มี | LOCK | วิธีตรวจ |
|---|---|---|---|
| NEG-40.1 | cookie consent บนเว็บ | LOCK-05 | render + grep — absent |
| NEG-40.2 | สายอนุมัติก่อนส่งคำขอ (ปุ่ม/สถานะ approve) | LOCK-04 | render สายส่ง — ไม่มีขั้นอนุมัติ |
| NEG-40.3 | ส่งอีเมล/LINE จริง | — | toast จำลองเท่านั้น ("...จำลอง...") |
| NEG-40.4 | คำนวณมูลค่า / คอลัมน์เก็บผลรายท่อ | LOCK-CSQ-04/05 | render + grep — ไม่มี amount/pipe column |
| NEG-40.5 | การ์ดผล 7 ท่อ CSQ บนจอ | LOCK-CSQ-06 | render — ไม่มี pipe-card |
| NEG-40.6 | ประกาศท่อ OC/DC/SC | LOCK-CSQ-01/02/03 | FN-19 declare-only · CSQ_BRIEF ไม่มี OC/DC/SC |
| NEG-40.7 | ธง opt-out เดียวต่อคน | — | โมเดล triple (partial-unique) |
| NEG-40.8 | "ไม่ตอบ" = "ไม่ยินยอม" | — | render — lapsed≠declined (AT-20b) |
| NEG-40.9 | บล็อกการส่งเอง | — | resolve read-only (API-20 ไม่ mutate) |
| NEG-40.10 | wizard สร้างคำขอ (stepper 5 ขั้น) | LOCK-07 | render reqCreate — single-screen (AT-05) |

---

## §6.3 Test Data Setup
- 3 tenants (isolated) · subjects CUS-1001..1008 (external ref) · purposes PUR-01..04 (04 = closed)
- consents CNS-5001..5009 (mix: granted/withdrawn/declined/near-expiry/expired/stale v1<v2)
- roles: qa_officer / qa_dpo / qa_auditor (read)

## §6.4 Definition of Done
### Code
- [ ] ทุก AT-01..20 + FN-40 negatives implement + unit/integration/e2e pass
- [ ] resolve contract (BR-20) มี contract test (schema lock) — 200 เสมอ
- [ ] CSQ declare-only: idempotency_key unique + reversal_of ถอน + **ไม่มี OC/DC/SC**
- [ ] Code review + no critical/high security finding · logic coverage ≥80%
### QA
- [ ] P0/P1 pass · no P0/P1 bug · security D-domains verified (D7 PII mask)
### Deployment
- [ ] Migration staging pass · **BR-22 register `/consent/*` Backend Enforcement Gate (F143) + 4-step review เสร็จ (hard dependency, OQ-04)**
- [ ] baseline ตัวชี้วัด §2.3 เก็บก่อน launch (OQ-06)

## §6.5 WebSocket Events
N/A — feature นี้ไม่มี realtime/WS event (ntf ไม่เลือก · การส่งเป็น mock toast)

## §6.6 Performance Benchmarks
| Endpoint | P95 | หมายเหตุ |
|---|---|---|
| POST /consent/resolve | < X ms (กำหนดที่ load test) | call ก่อนส่งทุก message — capacity รองรับ campaign burst (BRD §17.5) |
| GET /consent/registry | < 500ms | filter indexed |

## §6.7 Test Environment Notes
- ENG-01/02 TEST mode (deterministic) · recipient token = staging link · CSQ 7C = mock sink (ตรวจ envelope shape)

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AT-01 | API-02 | FN-01 | — |
| AT-02 | API-04 | FN-02, FN-17 | — |
| AT-05 | API-07 | FN-05 | — |
| AT-10/11 | API-13 | FN-09, FN-10, FN-11 | — |
| AT-15 | API-17 | FN-13, FN-19 | — |
| AT-17 | API-19 | FN-14, FN-05 | — |
| AT-19/20 | API-20 | FN-20 | ENG-01, ENG-02 |
| AT-13/14/16 | API-14/16/18 | FN-11, FN-18 | ENG-02 |
> ทุก FN-01..20 + ENG-01/02 ถูก trace ≥1 AC ✅

## §6.9 Cross-Module Test Cases (BRD §12.1 Downstream)
| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | campaign เรียก resolve ก่อนส่ง (granted) | แคมเปญ | allowed:true → ส่งได้ |
| XT-02 | campaign เรียก resolve (never_asked/withdrawn/expired) | แคมเปญ | allowed:false + reason → ไม่ส่ง (default-deny) |
| XT-03 | ถอน → caller cache invalidation ≤5 นาที | caller | resolve ตอบ false ทันที (BR-21, OQ-02) |
| XT-04 | ทุก state change → CSQ envelope ถูกต้อง (idempotency_key/reversal_of) | 7C Engine | envelope shape ตรง · **ไม่มี OC/DC/SC** |
| XT-05 | register `/consent/*` Backend Enforcement Gate | F143 | 4-step review pass ก่อน go-live (OQ-04) |

## §6.10 Microcopy-Aware Expected Text
> ยึด verbatim จาก HTML (toast/label ที่ list ใน AC ด้านบน) — ai-testcase-md-generator (step 9) ต้อง match จอ 1:1
> ตัวอย่าง verbatim: "สร้างวัตถุประสงค์ PUR-0x แล้ว" · "ต้องแนบเอกสาร PDPA" · "กรุณายืนยันตัวตนก่อนส่งคำตอบ" · "ถอนความยินยอมแล้ว — มีผลทันที..." · "ยังไม่เคยขอความยินยอมสำหรับคู่นี้ — ค่าเริ่มต้นคือส่งไม่ได้"
