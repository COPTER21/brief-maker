# Pattern H — A4 Paper / PDF Preview

> **Use for:** Document PDF preview tab inside view drawer (Pattern G).
> **Layout:** A4-aspect paper (720px max-width, ~900px min-height) with navy table header.
> **Source:** v25 (PDF preview implementation).

---

## 🎯 When to Use

✅ Inside Pattern G drawer (PDF preview tab)
✅ Print-ready document layout (PO, SO, Invoice, Receipt, Quotation)
✅ Standalone print preview page

❌ List of records (use Pattern A)
❌ Editable form (use Pattern B)
❌ Quick summary (use drawer-fields in Pattern C/G Detail tab)

---

## 🏗️ Structure

```
.a4-wrap (drawer-body background, padding around paper)
  └─ .a4-paper (white card, 720px max-width, A4 aspect ratio)
      ├─ .a4-header (logo + doc title)
      ├─ .a4-meta (doc number + date + reference)
      ├─ .a4-parties (from + to columns)
      ├─ .a4-lines (item table with navy header)
      ├─ .a4-totals (subtotal + tax + grand total)
      ├─ .a4-notes (terms, remarks)
      ├─ .a4-signatures (signer slots)
      └─ .a4-footer (company info, page X of Y)
```

---

## 📋 HTML Skeleton

```html
<div class="a4-wrap">
  <div class="a4-paper" id="a4-${doc.id}">

    <!-- HEADER: Logo + Title -->
    <div class="a4-header">
      <div class="a4-logo">
        <div class="a4-logo-mark">
          <i data-lucide="box" class="w-5 h-5"></i>
        </div>
        <div>
          <div class="a4-company-name">บริษัท เคสตัวอย่าง จำกัด</div>
          <div class="a4-company-meta">เลขผู้เสียภาษี 0123456789012</div>
        </div>
      </div>
      <div class="a4-title-block">
        <div class="a4-doc-type">${doc.docTypeLabel}</div>
        <div class="a4-doc-no">${doc.docNo}</div>
      </div>
    </div>

    <!-- META: doc info -->
    <div class="a4-meta">
      <div>
        <div class="a4-meta-lbl">วันที่</div>
        <div class="a4-meta-val">${formatDate(doc.docDate)}</div>
      </div>
      <div>
        <div class="a4-meta-lbl">ครบกำหนด</div>
        <div class="a4-meta-val">${formatDate(doc.dueDate)}</div>
      </div>
      <div>
        <div class="a4-meta-lbl">เงื่อนไขชำระ</div>
        <div class="a4-meta-val">${doc.paymentTerms || '—'}</div>
      </div>
      <div>
        <div class="a4-meta-lbl">อ้างอิง</div>
        <div class="a4-meta-val">${doc.reference || '—'}</div>
      </div>
    </div>

    <!-- PARTIES: From / To -->
    <div class="a4-parties">
      <div class="a4-party-block">
        <div class="a4-party-lbl">${doc.docType === 'PO' ? 'ผู้ซื้อ' : 'ผู้ขาย'}</div>
        <div class="a4-party-name">บริษัท เคสตัวอย่าง จำกัด</div>
        <div class="a4-party-detail">
          123/45 ถนนสุขุมวิท แขวงคลองเตย<br>
          เขตคลองเตย กรุงเทพมหานคร 10110<br>
          โทร 02-123-4567
        </div>
      </div>
      <div class="a4-party-block">
        <div class="a4-party-lbl">${doc.docType === 'PO' ? 'ผู้ขาย' : 'ลูกค้า'}</div>
        <div class="a4-party-name">${doc.partyName}</div>
        <div class="a4-party-detail">
          ${doc.partyAddress}<br>
          เลขผู้เสียภาษี ${doc.partyTaxId}
        </div>
      </div>
    </div>

    <!-- LINES TABLE -->
    <table class="a4-lines">
      <thead>
        <tr>
          <th style="width: 36px; text-align: center;">#</th>
          <th>รายการ</th>
          <th style="width: 60px; text-align: right;">จำนวน</th>
          <th style="width: 56px;">หน่วย</th>
          <th style="width: 90px; text-align: right;">ราคา/หน่วย</th>
          <th style="width: 96px; text-align: right;">รวม</th>
        </tr>
      </thead>
      <tbody>
        ${doc.lines.map((l, i) => `
          <tr>
            <td style="text-align: center;">${i + 1}</td>
            <td>
              <div style="font-weight: 600;">${l.name}</div>
              ${l.code ? `<div style="font-size: 10.5px; color: var(--c-mute-2); margin-top: 2px;">${l.code}</div>` : ''}
            </td>
            <td style="text-align: right;">${l.qty}</td>
            <td>${l.unit || ''}</td>
            <td style="text-align: right;">${l.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td style="text-align: right; font-weight: 600;">${l.total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>

    <!-- TOTALS -->
    <div class="a4-totals-wrap">
      <div class="a4-totals">
        <div class="a4-totals-row">
          <span>ยอดรวม</span>
          <span>${doc.subtotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
        </div>
        <div class="a4-totals-row">
          <span>ภาษีมูลค่าเพิ่ม 7%</span>
          <span>${doc.tax.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
        </div>
        <div class="a4-totals-row is-grand">
          <span>ยอดสุทธิ (บาท)</span>
          <span>${doc.grandTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
        </div>
      </div>
    </div>

    <!-- NOTES -->
    ${doc.notes ? `
      <div class="a4-notes">
        <div class="a4-notes-lbl">หมายเหตุ</div>
        <div class="a4-notes-body">${doc.notes}</div>
      </div>
    ` : ''}

    <!-- SIGNATURES -->
    <div class="a4-signatures">
      ${(doc.signatures || []).map(s => `
        <div class="a4-sig-block">
          <div class="a4-sig-line"></div>
          <div class="a4-sig-name">(${s.name || '________________________'})</div>
          <div class="a4-sig-role">${s.role}</div>
          <div class="a4-sig-date">วันที่ ${s.signedAt ? formatDate(s.signedAt) : '_____________'}</div>
        </div>
      `).join('')}
    </div>

    <!-- FOOTER -->
    <div class="a4-footer">
      <div>เอกสารนี้พิมพ์โดยระบบ CUBE NATIVE</div>
      <div>หน้า 1 / 1</div>
    </div>

  </div>
</div>
```

---

## 🎨 A4 Paper CSS (add to file-skeleton or pattern file)

```css
.a4-wrap {
  background: var(--c-bg-off);
  padding: 24px;
  min-height: 100%;
  display: flex;
  justify-content: center;
}
.a4-paper {
  background: #fff;
  width: 100%;
  max-width: 720px;
  min-height: 900px;
  padding: 40px 44px;
  border: 1px solid var(--c-line-2);
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(17,17,17,0.08);
  font-size: 12px;
  line-height: 1.55;
  color: var(--c-ink);
}
.a4-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--c-navy);
  margin-bottom: 16px;
}
.a4-logo { display: flex; align-items: center; gap: 12px; }
.a4-logo-mark {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, var(--c-primary), var(--c-teal));
  border-radius: 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.a4-company-name { font-size: 14px; font-weight: 700; color: var(--c-navy); }
.a4-company-meta { font-size: 11px; color: var(--c-mute-2); margin-top: 2px; }
.a4-title-block { text-align: right; }
.a4-doc-type {
  font-size: 18px;
  font-weight: 700;
  color: var(--c-navy);
  letter-spacing: 0.05em;
}
.a4-doc-no {
  font-size: 13px;
  color: var(--c-mute);
  margin-top: 4px;
  letter-spacing: 0.02em;
}
.a4-meta {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px 24px;
  padding: 12px 0;
  border-bottom: 1px solid var(--c-line-2);
  margin-bottom: 16px;
}
.a4-meta-lbl { font-size: 10.5px; color: var(--c-mute-2); text-transform: uppercase; letter-spacing: 0.06em; }
.a4-meta-val { font-size: 12.5px; color: var(--c-ink); font-weight: 600; margin-top: 3px; }
.a4-parties {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 18px;
}
.a4-party-block {
  padding: 12px 14px;
  background: var(--c-bg-off);
  border-radius: 6px;
  border-left: 3px solid var(--c-primary);
}
.a4-party-lbl { font-size: 10.5px; color: var(--c-mute-2); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.a4-party-name { font-size: 13px; font-weight: 700; color: var(--c-ink); }
.a4-party-detail { font-size: 11.5px; color: var(--c-mute); margin-top: 4px; }

.a4-lines {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 14px;
  font-size: 11.5px;
}
.a4-lines thead { background: var(--c-navy); color: #fff; }
.a4-lines th {
  padding: 9px 10px;
  text-align: left;
  font-weight: 600;
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.a4-lines td {
  padding: 10px;
  border-bottom: 1px solid var(--c-line-2);
  vertical-align: top;
}
.a4-lines tbody tr:last-child td { border-bottom: 0; }

.a4-totals-wrap { display: flex; justify-content: flex-end; margin-bottom: 18px; }
.a4-totals { min-width: 280px; }
.a4-totals-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 12px;
  font-size: 12px;
  color: var(--c-mute);
}
.a4-totals-row.is-grand {
  background: var(--c-navy);
  color: #fff;
  font-weight: 700;
  font-size: 13px;
  padding: 10px 12px;
  margin-top: 4px;
  border-radius: 4px;
}

.a4-notes {
  padding: 12px 14px;
  background: #FEF9C3;
  border-left: 3px solid var(--c-warning);
  border-radius: 4px;
  margin-bottom: 18px;
}
.a4-notes-lbl { font-size: 10.5px; color: #B8690B; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; }
.a4-notes-body { font-size: 11.5px; color: #78350F; margin-top: 4px; }

.a4-signatures {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 24px;
  padding: 28px 0 16px;
}
.a4-sig-block { text-align: center; font-size: 11px; }
.a4-sig-line { border-top: 1px dashed var(--c-mute-3); height: 0; margin-bottom: 6px; }
.a4-sig-name { color: var(--c-ink); font-weight: 500; }
.a4-sig-role { color: var(--c-mute-2); margin-top: 2px; font-size: 10.5px; }
.a4-sig-date { color: var(--c-mute-2); margin-top: 6px; font-size: 10.5px; }

.a4-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 14px;
  margin-top: 24px;
  border-top: 1px solid var(--c-line-2);
  font-size: 10.5px;
  color: var(--c-mute-2);
}
```

---

## 🛡️ Iron Rules to Enforce

- **#21** All `<i data-lucide>` have `w-{N} h-{N}` ✓
- **#23** No color emoji — printed docs need professional look ✓
- **Compact font sizing (11.5-13px)** to fit A4 layout ✓
- **Navy table header** for company branding ✓
- **Decimal formatting** with `toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })` ✓

---

## ⚠️ Common Mistakes

1. **❌** Using `font-size: 14px` (too big — A4 paper should use 11-13px to fit content)
2. **❌** No fixed `max-width: 720px` (A4 paper looks wrong if too wide in browser)
3. **❌** Table header without navy bg (looks like regular table — needs distinctive paper look)
4. **❌** Decimal places inconsistent (always 2 decimals for amounts)
5. **❌** Signature blocks with placeholder `__________` not converting to actual line (use border-top: 1px dashed)
6. **❌** Footer without page number (always include "หน้า 1 / 1" even for single-page docs)
7. **❌** Notes section without left border accent (looks plain — add yellow left border for emphasis)
8. **❌** Party blocks without left border accent (use 3px navy/primary left border)

---

## 🎯 Print-Ready Optimization

```css
@media print {
  body { background: #fff; }
  .sidebar, .shell-bar, .drawer-tabs, .drawer-footer { display: none !important; }
  .drawer { 
    position: static !important;
    width: 100% !important;
    box-shadow: none !important;
    transform: none !important;
  }
  .a4-paper {
    box-shadow: none !important;
    border: 0 !important;
    max-width: 100% !important;
    padding: 0 !important;
  }
}
```
