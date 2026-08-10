# Pattern I — Signature Card List

> **Use for:** Signature tab inside Pattern G (PO-style drawer) — show all required signers + their status.
> **Examples:** Document approval chain, multi-step sign-off, audit trail.
> **Source:** v25 (signature card list).

---

## 🎯 When to Use

✅ Documents requiring multiple signatures/approvals (PO, Contract, Invoice approval)
✅ Sequential or parallel sign-off workflows
✅ Audit trail with signer + timestamp + role

❌ Single approver (just show "Approved by X at Y" in detail tab)
❌ Comments/notes (use Notes tab in Pattern C)

---

## 🏗️ Structure

```
Signatures Tab Body
  ├─ Summary row (X / Y signed)
  └─ .sig-list
      ├─ .sig-card (per signer)
      │   ├─ Icon (40×40 circle)
      │   ├─ Name + Role + Department
      │   ├─ Status pill
      │   └─ Date signed (if signed)
      ├─ .sig-card (next signer)
      ├─ ...
```

---

## 📋 HTML Skeleton

```html
function renderSignatureList(doc) {
  const signed = doc.signatures.filter(s => s.status === 'signed').length;
  const total = doc.signatures.length;
  
  return `
    <!-- Summary -->
    <div class="drawer-section">
      <div style="padding: 14px 16px; background: var(--c-bg-off); border-radius: 8px; 
                  display: flex; align-items: center; gap: 12px;">
        <div style="width: 40px; height: 40px; border-radius: 50%; 
                    background: ${signed === total ? '#E4F4EB' : '#E6F0FF'}; 
                    color: ${signed === total ? 'var(--c-success)' : 'var(--c-primary)'}; 
                    display: inline-flex; align-items: center; justify-content: center;">
          <i data-lucide="${signed === total ? 'check-circle-2' : 'clock'}" class="w-5 h-5"></i>
        </div>
        <div style="flex: 1;">
          <div style="font-weight: 600; font-size: 14px;">
            ${signed === total ? 'ลงนามครบแล้ว' : `รอลงนาม (${signed} / ${total})`}
          </div>
          <div style="font-size: 12px; color: var(--c-mute);">
            ${signed === total 
              ? 'เอกสารพร้อมใช้งาน' 
              : `เหลืออีก ${total - signed} ท่านต้องลงนาม`}
          </div>
        </div>
      </div>
    </div>

    <!-- Signer cards -->
    <div class="drawer-section" style="margin-bottom: 0;">
      <h3 class="drawer-section-title">รายชื่อผู้ลงนาม</h3>
      <div class="sig-list">
        ${doc.signatures.map((s, idx) => `
          <div class="sig-card ${s.status === 'signed' ? 'is-signed' : s.status === 'rejected' ? 'is-rejected' : 'is-pending'}">

            <!-- Signer icon (40px) -->
            <div class="sig-card-icon">
              ${s.status === 'signed' 
                ? '<i data-lucide="check" class="w-4 h-4"></i>' 
                : s.status === 'rejected'
                ? '<i data-lucide="x" class="w-4 h-4"></i>'
                : `<span style="font-weight: 600;">${idx + 1}</span>`}
            </div>

            <!-- Signer info -->
            <div class="sig-card-info">
              <div class="sig-card-role">${s.role}</div>
              <div class="sig-card-name">${s.name || '— ยังไม่ระบุ —'}</div>
              ${s.department ? `<div class="sig-card-dept">${s.department}</div>` : ''}
            </div>

            <!-- Status + date -->
            <div class="sig-card-status">
              <span class="pill pill-${s.status === 'signed' ? 'converted' : s.status === 'rejected' ? 'danger' : 'registered'}">
                <span class="dot is-${s.status === 'signed' ? 'converted' : s.status === 'rejected' ? 'suspended' : 'active'}"></span>
                ${s.status === 'signed' ? 'ลงนามแล้ว' : s.status === 'rejected' ? 'ปฏิเสธ' : 'รอลงนาม'}
              </span>
              ${s.signedAt ? `
                <div style="font-size: 11px; color: var(--c-mute-2); margin-top: 4px; text-align: right;">
                  ${formatDateTime(s.signedAt)}
                </div>
              ` : ''}
            </div>

          </div>
        `).join('')}
      </div>
    </div>
  `;
}
```

---

## 🎨 Signature Card CSS

```css
.sig-list { display: flex; flex-direction: column; gap: 8px; }
.sig-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border: 1px solid var(--c-line-2);
  border-radius: 10px;
  background: #fff;
  transition: all 120ms;
}
.sig-card.is-signed {
  border-color: rgba(16,185,129,0.20);
  background: rgba(16,185,129,0.02);
}
.sig-card.is-rejected {
  border-color: rgba(220,38,38,0.20);
  background: rgba(220,38,38,0.02);
}
.sig-card.is-pending {
  border-color: var(--c-line-2);
}
.sig-card-icon {
  width: 40px; height: 40px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 13px;
  color: var(--c-mute-2);
  background: var(--c-line-3);
  border: 1.5px solid var(--c-line-2);
}
.sig-card.is-signed .sig-card-icon {
  background: var(--c-success);
  color: #fff;
  border-color: var(--c-success);
}
.sig-card.is-rejected .sig-card-icon {
  background: var(--c-danger);
  color: #fff;
  border-color: var(--c-danger);
}
.sig-card-info { flex: 1; min-width: 0; }
.sig-card-role {
  font-size: 10.5px;
  color: var(--c-mute-2);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.sig-card-name {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--c-ink);
  margin-top: 3px;
}
.sig-card-dept {
  font-size: 11.5px;
  color: var(--c-mute-2);
  margin-top: 2px;
}
.sig-card-status { 
  text-align: right; 
  flex-shrink: 0;
}
```

---

## 🔧 Required JS Helpers

```javascript
// Data shape for signatures
// doc.signatures = [
//   {
//     id: 'sig-1',
//     role: 'ผู้ขอ',                          // role label (uppercase in card)
//     name: 'สมชาย ใจดี',                     // signer's name (or null if not yet assigned)
//     department: 'จัดซื้อ',                  // optional
//     status: 'signed' | 'pending' | 'rejected',
//     signedAt: '2026-05-18T10:30:00',       // ISO timestamp (null if not signed)
//     reason: '...'                          // for rejections
//   },
//   ...
// ]

// Approve/sign action
function signDocument(docId, sigId) {
  const doc = state.records.find(d => d.id === docId);
  if (!doc) return;
  const sig = doc.signatures.find(s => s.id === sigId);
  if (!sig) return;
  sig.status = 'signed';
  sig.signedAt = new Date().toISOString();
  sig.name = sig.name || 'You';
  render();
  showToast('ลงนามสำเร็จ', 'success');
}

function rejectDocument(docId, sigId, reason) {
  const doc = state.records.find(d => d.id === docId);
  if (!doc) return;
  const sig = doc.signatures.find(s => s.id === sigId);
  if (!sig) return;
  sig.status = 'rejected';
  sig.signedAt = new Date().toISOString();
  sig.reason = reason;
  doc.status = 'rejected';
  render();
  showToast('ปฏิเสธเอกสารแล้ว', 'warning');
}
```

---

## 🎯 Multi-state Variants

### Variant A: Sequential (One at a time)

When workflow is **sequential** (signer N can only sign after signer N-1):

```javascript
${doc.signatures.map((s, idx) => {
  const canSign = idx === 0 || doc.signatures[idx - 1].status === 'signed';
  return `
    <div class="sig-card is-${s.status} ${!canSign && s.status === 'pending' ? 'is-blocked' : ''}">
      ${!canSign && s.status === 'pending' 
        ? '<div style="font-size: 11px; color: var(--c-mute);">รอลำดับก่อนหน้า</div>' 
        : ''}
      <!-- ... rest of card ... -->
    </div>
  `;
}).join('')}
```

Add CSS:
```css
.sig-card.is-blocked { opacity: 0.55; background: var(--c-line-3); }
```

### Variant B: Parallel (Any order)

All `pending` signers can sign at any time — no ordering. Default behavior.

### Variant C: Quorum (e.g. 2 of 3)

```javascript
const quorumNeeded = 2;
const signed = doc.signatures.filter(s => s.status === 'signed').length;
const quorumMet = signed >= quorumNeeded;

// Summary message:
${quorumMet 
  ? 'ลงนามครบตามจำนวนที่กำหนด' 
  : `ต้องการเพิ่มอีก ${quorumNeeded - signed} ลายเซ็น (จากทั้งหมด ${doc.signatures.length})`}
```

---

## 🛡️ Iron Rules to Enforce

- **#21** Icons in cards have `w-4 h-4` ✓
- **#23** No color emoji ✓
- **Pre-populated signer name** when available (don't default to "User" or "—")
- **Status pill + dot** for consistency with rest of UI
- **Uppercase role** for prominent label (e.g., "ผู้ขอ", "ผู้อนุมัติ", "กรรมการ")

---

## ⚠️ Common Mistakes

1. **❌** Showing "User 1, User 2, ..." instead of actual names (pre-populate when known)
2. **❌** No visual difference between signed/pending/rejected cards (use border + bg subtly)
3. **❌** Date displayed without timezone consideration (use `formatDateTime` helper)
4. **❌** Status pill style doesn't match other UI (use existing `.pill` variants)
5. **❌** Card icon doesn't change with status (signed: check icon, rejected: x icon, pending: number)
6. **❌** Rejection reason hidden (show in card body for transparency)
7. **❌** No summary count at top — user has to count manually
8. **❌** Sequential workflow doesn't disable blocked cards (looks like all can sign)
