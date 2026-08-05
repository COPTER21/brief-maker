# Pattern G — PO-style View Drawer (Wide, with PDF Preview)

> **⭐ MERGED INTO THE v2 VIEW-DRAWER STANDARD (`pr.html`).** Document-centric view drawers
> (PO / SO / Invoice / Receipt / Quotation / PR) are now produced by **Pattern C — View Drawer
> with Tabs**, which is locked 100% to the reference. The PR reference *is* the canonical
> PO-style wide drawer (mono doc-no header, status-conditional actions, Detail / PDF / Signatures tabs).
>
> **Do this:** Follow **Pattern C** verbatim. Use the same files:
> - `references/drawer-standard/_SOURCE_pr-reference.html`
> - `references/drawer-standard/drawer.css.html`
> - `references/drawer-standard/view-drawer.js.txt`
> - `references/drawer-standard/shared-helpers.js.txt`

---

## 🎯 When to Use (vs Pattern C)

There is no longer a separate width/markup for "PO-style". Every document view uses the **same
wide v2 shell**:

- Shell: `#overlay-root → .overlay-wrap → .backdrop + .drawer-panel.drawer-enter` (wide **920px**;
  add `.standard` only for narrow 680px non-document records).
- Header: eyebrow + `<h2 class="tbl-mono" style="color:var(--c-primary)">${doc_no}</h2>` + `renderPill(status)` + `requester · dept` sub.
- Action contract (status-conditional) + `1px×22px` divider + `พิมพ์ / ดาวน์โหลด / ปิด` `.top-icon-btn`.
- Tabs: `รายละเอียด` · `PDF Preview` · `ลายเซ็น`.

→ **See Pattern C** for the exact header markup, tab functions, the A4 PDF sheet (Tab 2),
the signature chain (Tab 3), and open/close JS.

---

## 🧩 Document-type adaptation cheat-sheet

When the document is **not** a PR, change only the labels/fields — keep the shell, tabs, and CSS:

| Doc | Eyebrow | Doc-no field | Party sub-line | Extra detail section |
|---|---|---|---|---|
| PO | ใบสั่งซื้อ (Purchase Order) | `po_no` | vendor · dept | vendor terms, expected delivery |
| SO | ใบสั่งขาย (Sales Order) | `so_no` | customer · channel | ship-to, payment terms |
| Invoice | ใบแจ้งหนี้ (Invoice) | `inv_no` | customer · due date | aging, paid/outstanding |
| Receipt | ใบเสร็จรับเงิน (Receipt) | `rcpt_no` | payer · method | reference doc |
| Quotation | ใบเสนอราคา (Quotation) | `qt_no` | customer · valid-until | validity, lead time |

Status-action contract maps 1:1 (draft→submit, pending→approve/reject/return, approved→create-next).
PDF sheet header (company block, tax id, table, signatures) stays identical — swap the doc title only.

---

## 🛡️ Iron Rules

Identical to **Pattern C**. Do not reintroduce the legacy 680px `.drawer` markup for documents —
the standard document width is now 920px via `.drawer-panel`.
