# CSQ_BRIEF — F131 Performance / ประเมินผลงาน (F-HR-PERF)

> **ยิงผ่าน ENG-CSQ (7C · compliance-sensitive-queue) เท่านั้น — feature "ประกาศท่อ" เท่านั้น ห้าม hardcode**
> ประกาศ **SecC (masking) + DC (decision)** เท่านั้น — ❌ **ห้าม** OC / DC-doc / SC / AC / FC (สงวนของ engine · LK-6)
> Source of truth: FRD Pack (03_LOGIC §3.2 ENG-CSQ · 02_API §API-12 · §2.X · 05_RULES BR-08/BR-13/§5.7 D-CLASS/§5.8 · 07_LOCKED LK-4/LK-6/LD-03)
> รันหลัง step 7 (FRD) · WF-01 declaration (manual — ไม่มี csq-declaration skill) · 2026-09-09

---

## 1. Identity

| Field | Value |
|---|---|
| feature_id | F131 · F-HR-PERF · module HR |
| engine | ENG-CSQ (`compliance-sensitive-queue` · 7C) · **EXISTING** (shared) |
| classification สูงสุดที่แตะ | **RESTRICTED (SecC)** — score/decision/gap/notes (00_OVERVIEW §0.7.1 · Preset P6) |
| ท่อที่ประกาศ | **SecC + DC** เท่านั้น (LK-6) |

---

## 2. Declared 7C Pipes

| pipe | ท่อ (7C) | ขอบเขตในฟีเจอร์ | เงื่อนไข |
|:--:|---|---|---|
| **SecC** | Security-sensitive Content (ผลประเมิน/คะแนน RESTRICTED · masking) | เข้าถึง/เก็บผลประเมินรายคน (score/decision/gap/notes) — ข้อมูลลับต่อบุคคล · masking + row-scope ตาม role (SELF/DEPT/ALL) | ทุกครั้งที่ผลถูกเผยแพร่/เก็บเข้า 7C (FN-17 applyScopeAndMask · BR-08/BR-11) |
| **DC** | Decision Control (decision ผ่าน/ไม่ผ่าน/ทบทวน) | **terminal decision** ของการสอบทาน — **ไม่ใช่การเซ็นอนุมัติเอกสาร** (นั่นเป็น DOA) | บันทึก ณ ขั้นสุดท้ายของ calibration (FN-07 last stage · BR-13) |

> **DC ที่ประกาศ = decision เชิงผล (ผ่าน/ไม่ผ่าน/ทบทวน)** ไม่ใช่ DC-เอกสาร (doc signature) ที่ ENG-DOA เจ้าของ.

---

## 3. Declared Event

| event_id | trigger (state transition · อ้าง FRD) | ท่อ | payload |
|---|---|:--:|---|
| `perf.result.published` | **per-person publish** — `recordCalibrationStage` ขั้นสุดท้าย → appraisal.status `calibration→published` (03_LOGIC FN-07 · API-12 isLast) · **รวม re-publish (ยิงซ้ำ per-person)** | **SecC + DC** | `{ appraisal_id, employee_ref, classification: 'SecC', decision: 'DC' }` (ENG-CSQ input schema · 03_LOGIC §3.2) |

- **Trigger = per-person publish** (OQ-PERF-02 **RESOLVED** · LD-03) — ยิง 1 ครั้งต่อผลรายคนที่เผยแพร่ · re-open → re-publish → **ยิงซ้ำ per-person** (02_API §2.X).
- จุดเรียกเดียวกับ ENG-NOTIFY `perf.result.published` (API-12 isLast) แต่ **คนละ engine / คนละท่อ** — CSQ = 7C compliance queue · NOTIFY = user notification.
- audit: mutation เขียน "บันทึกผลประเมินเข้า 7C" (append-only · BR-09/FN-16).

---

## 4. ไม่ประกาศ (สงวน / เจ้าของอื่น)

| ท่อ | เหตุผล |
|---|---|
| **OC** (Operational Control / OP) | ไม่อยู่ในขอบเขต feature (LK-6) |
| **DC-doc + doa_*** | เป็นการเซ็นอนุมัติเอกสาร → **ENG-DOA** เจ้าของ (ดู DOA_BRIEF) — ห้ามประกาศซ้ำ |
| **AC / FC** | ไม่ลงบัญชี / ไม่มีเงินสด (perf ไม่มีธุรกรรมการเงิน — ปรับเงินเดือนเป็น event ให้ Movement · LK-2) |
| **SC** | สงวนของ engine |

---

## 5. Wire Checklist (`wire_status: pending → wired`)

- [ ] dev wire: emit `perf.result.published` (SecC/DC) ที่ API-12 isLast (per-person publish + re-publish)
- [ ] ยืนยัน payload = `{ appraisal_id, employee_ref, classification:'SecC', decision:'DC' }`
- [ ] ยืนยัน masking/scope (FN-17) บังคับที่ payload (ไม่ใช่แค่ UI hide · AT-01) ก่อนเข้าคิว 7C
- [ ] ผูก RESTRICTED fields กับ Restricted Resources registry (Policy Center) — **OQ-PERF-10 OPEN** (04_DB §4.6.6)

---

## 6. Open Questions

| OQ | คำถาม | Owner | สถานะ |
|---|---|---|---|
| **OQ-PERF-06** | **CSQ EC valuation** — มูลค่า EC ของ `perf.result.published` คิดยังไง + ท่อ 7C detail | **Architect** | 🔴 **OPEN — leave as OQ** (trigger locked · valuation deferred · LD-03) |
| OQ-PERF-10 | Restricted fields wire กับ Restricted Resources registry (Policy Center) | Security/Policy Center | OPEN (04_DB §4.6.6) |

> **ไม่ block FRD** — event ยิงถูกจุดแล้ว (per-person publish) · EC valuation เป็นรายละเอียดปลายทางที่ Architect เคาะ (00_OVERVIEW §0.8 · 07_LOCKED §7.5).

---

## 7. NOT-NEEDED (ท่อ declaration อื่นในตระกูล)

- **DOCCFG:** NOT-NEEDED — ไม่มีเลขรันเอกสาร (archetype master+cycle · ไม่ใช่ Pattern Q · LD-08)
- **PDFDOC (thai-doc-pdf):** NOT-NEEDED — ไม่มีเอกสารคนถือ/พิมพ์ A4/ลายเซ็น (LD-08)
