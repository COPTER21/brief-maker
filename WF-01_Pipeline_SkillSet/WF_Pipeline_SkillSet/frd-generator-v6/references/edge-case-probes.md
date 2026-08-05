# Edge Case Probes — frd-generator-v6

> **Purpose:** Proactive blind-spot detection — ถาม user คำถาม edge case ที่ BA มักลืม
> **Used by:** Phase 2.5 (Edge Case Probing) — กลายเป็น Edge Cases ใน 05_RULES.md
> **Heritage:** Preserved from v2.8 → v4 → v5

---

## 🎯 Trigger Matrix

ดู feature pattern → activate probe ที่ตรงกัน

| Feature Pattern | Activate Probe |
|---|---|
| approve / sign / multi-step approval | **PR-1** Concurrency, **PR-3** Permission Mid-flight |
| real-time / WebSocket / multi-user same data | **PR-2** Stale Data |
| submit / create / mutation transaction | **PR-4** Network Failure, **PR-7** Idempotency |
| bulk / import / batch upload | **PR-5** Bulk/Atomic |
| draft / wizard / multi-step form | **PR-6** Draft/Resume |
| cancel / reverse / void | **PR-8** Compensation |
| financial / inventory / counter | **PR-9** Race Condition |

---

## 🔍 Probe Details

### PR-1: Concurrency (สำหรับ approve/sign)

**คำถาม:**
> "ถ้า manager 2 คนกด approve พร้อมกันใน 1 record → จะเกิดอะไร?"
> A) คนแรกได้ — คนสองโดน 409 Conflict
> B) ทั้งคู่ approve แล้ว double-record audit log
> C) อื่น ๆ

**Impact ใน FRD:**
- 02_API: เพิ่ม optimistic locking (version field)
- 03_LOGIC: function ต้อง check current state ก่อน update
- 05_RULES: ERR_ALREADY_APPROVED
- 06_TESTS: TC ทดสอบ concurrent approve

---

### PR-2: Stale Data (real-time/WebSocket)

**คำถาม:**
> "User A แก้ field X อยู่, User B อ่านหน้านี้ทิ้งไว้ 10 นาที, A กด save → B เห็นข้อมูลเก่า, B กด edit field Y → จะ overwrite ของ A ไหม?"

**Impact:**
- 02_API: เพิ่ม `updated_at` ใน response + check `if-match` header
- 05_RULES: ERR_STALE_DATA / conflict resolution policy
- 06_TESTS: TC stale write

---

### PR-3: Permission Mid-flight

**คำถาม:**
> "User เริ่ม edit หน้านี้ตอนเป็น manager, ระหว่างเปิดหน้าโดน demote เป็น staff, แล้วกด save → จะอนุญาตไหม?"

**Impact:**
- 02_API: re-check role ตอน mutation (ไม่ใช่แค่ตอน GET)
- 05_RULES: ERR_PERMISSION_REVOKED
- 03_LOGIC: function check role context

---

### PR-4: Network Failure (mid-transaction)

**คำถาม:**
> "User กด submit, server รับ request แล้ว, แต่ network ขาดก่อน response กลับ → user จะ retry → จะเกิด double-submit ไหม?"

**Impact:**
- 02_API: เพิ่ม idempotency key
- 05_RULES: idempotency policy (24hr cache)
- 06_TESTS: TC retry safety

---

### PR-5: Bulk/Atomic (import 1000 rows)

**คำถาม:**
> "User upload CSV 1000 rows, row 500 มี error → จะ:"
> A) Reject ทั้งไฟล์ (atomic)
> B) Insert 499 rows ก่อน error
> C) Insert ทั้งหมดที่ valid + report invalid

**Impact:**
- 02_API: transaction boundary policy
- 05_RULES: bulk error handling
- 06_TESTS: partial-failure scenarios

---

### PR-6: Draft/Resume (wizard form)

**คำถาม:**
> "User กรอก wizard ถึง step 3 จาก 5, ปิด browser, กลับมา 1 ชม.หลัง → ข้อมูลยังอยู่ไหม? ที่ไหน? expire เมื่อไหร่?"

**Impact:**
- 02_API: draft endpoints (auto-save)
- 04_DB: draft table หรือ status='draft'
- 05_RULES: draft expiry policy (24hr/7d)
- 03_LOGIC: cleanupExpiredDrafts function

---

### PR-7: Idempotency (mutation)

**คำถาม:**
> "User double-click submit (race condition) → จะ:"
> A) สร้าง 2 records
> B) สร้าง 1 record + 1 error
> C) สร้าง 1 record + 1 silent success (idempotent)

**Impact:**
- 02_API: idempotency-key header pattern
- 03_LOGIC: function check existing key
- 05_RULES: ERR_DUPLICATE_KEY policy

---

### PR-8: Compensation (cancel/reverse)

**คำถาม:**
> "Payment สำเร็จแล้ว ผู้ใช้กด cancel → จะ:"
> A) Refund อัตโนมัติ
> B) Refund manual (admin)
> C) ไม่ refund (final sale)

**Impact:**
- 02_API: cancel endpoint behavior
- 03_LOGIC: compensation function (refund Engine)
- 05_RULES: cancellation policy
- 06_TESTS: TC cancel after success

---

### PR-9: Race Condition (financial/inventory)

**คำถาม:**
> "Stock = 1 ชิ้น, customer A + B กด buy พร้อมกัน → ใครได้?"
> A) คนแรกที่ DB commit (DB lock)
> B) คนแรกที่ click + 200ms grace
> C) Reserve mechanism (Adjust inventory before payment)

**Impact:**
- 04_DB: row-level lock หรือ inventory_reservation table
- 03_LOGIC: reserveStock function (atomic)
- 05_RULES: ERR_OUT_OF_STOCK + reservation expiry
- 06_TESTS: TC race buy

---

## 📋 Probe Workflow

### Phase 2.5 — How to run

1. **Detect feature patterns** — อ่าน Brief/BRD หา keyword
2. **Activate matching probes** — list ที่จะถาม
3. **Show plan to user:**
   ```
   ผม activated PR-1 (Concurrency), PR-7 (Idempotency), PR-9 (Race) ตาม feature pattern
   - ตอบไม่ทุกข้อก็ได้ ที่ skip จะ mark ใน 00_OVERVIEW Out of Scope
   - ขอเริ่มถามเลยไหม?
   ```
4. **Ask one-by-one** — รับคำตอบ
5. **Integrate answers:**
   - Concurrency rules → 03_LOGIC + 05_RULES
   - Idempotency → 02_API contract
   - Compensation → 03_LOGIC §3.2 (if engine) หรือ §3.1
   - Race → 04_DB + 03_LOGIC
6. **Mark skipped** → 00_OVERVIEW §Open Questions

---

## 🚨 ห้ามทำ

- **ห้าม activate ทุก probe ทุก feature** — เลือกตาม trigger pattern เท่านั้น
- **Interactive mode: ห้ามแต่งคำตอบ probe เอง** — ต้องถาม user
- **Lane Mode (one-shot): ห้ามถาม** — ตอบตามลำดับ BRD §10 → NODE_BRIEF/GOLDEN_RULES → conservative default + tag `[AI-DEFAULT]` + Open Question (ดู SKILL.md Phase 2.5)
- **ห้าม skip Phase 2.5 ใน FULL variant** — Critical features ต้องผ่าน probing
- **LEAN variant** อาจ skip ถ้าไม่มี mutation — แต่ถ้ามี PR-7 mandatory

---

## 📊 Coverage Matrix (Self-Check)

ก่อน Phase 4 deliver — ถาม:

| Variant | Min probes activated |
|---|---|
| LEAN (read-only) | 0 — but PR-7 ถ้ามี mutation |
| LEAN (with mutation) | PR-7 minimum |
| STANDARD | 2+ based on triggers |
| FULL | 3+ based on triggers |

ถ้า activate < min → review Brief/BRD ว่าครอบคลุมจริงไหม
