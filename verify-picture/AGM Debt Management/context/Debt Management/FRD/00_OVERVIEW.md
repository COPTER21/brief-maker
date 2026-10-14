# 00_OVERVIEW — F-AGM-008 Debt Management

## §0.1 Identity
| | |
|---|---|
| Feature ID | F-AGM-008 |
| ชื่อ | จัดการหนี้ลูกหนี้ (Debt Management) |
| Module | เกษตรกรรม (AGM) · WKN |
| Pack | FRD_F-AGM-008_Pack (7 ไฟล์ STANDARD) |
| Reverse | RIF v2 + invariants.md 🔒 (T3 code-only) |
| BRD | BRD_F-AGM-008 APPROVED (LOCK-01..11) |

## §0.2 Purpose
Financial ledger of record ของหนี้ลูกหนี้เกษตรกร (ผูกโควตา) — obligation + interest/penalty + payment allocation + write-off + adjustment + double-entry ledger. Outstanding อ่านโดย CBM/Contract.

## §0.3 Scope
In: Debtor (list/create/detail 5 tabs) · Obligation (create/list/write-off) · Payment (allocation waterfall) · Write-off (DOA) · Ledger (double-entry + export) · Adjustment. Out: payment-run engine, accrual job, real docs, manual allocation.

## §0.4 Entities
Debtor `DEB-YYYY-####` (1:1 quota) · Obligation `OBL-YYYY-####` (N) · LedgerEntry `LED-YYYY-####` (append-only). → 04_DB.

## §0.5 Actors / RBAC
Debt.Officer (CRUD + payment + write-off ≤DOA) · Debt.Manager (approve >DOA + adjustment/reverse) · Contract (write contract-obligation 🔒) · CBM/Contract (read outstanding). → 05_RULES §5.3.

## §0.6 Cross-Module
read Quota (F-AGM-002 verified) · read Contract (F-AGM-005 contract_id 🔒) · **feed outstanding** → CBM (F-AGM-007 debtor_outstanding) + Contract deduction.

## §0.11 Scope Lock (← BRD §3.4)
LOCK-01..11. สำคัญ: allocation waterfall (03), DOA 100k (05), contract-lock (04/05), ledger double-entry (04), outstanding cross-module (02/03).

## §0.7 Pages (→ 01_UI)
P-01 Debtor List · P-02 Debtor Detail (5 tabs) · OV create-debtor · OV create-obligation · OV manual-payment · OV write-off.

## §0.8 Open Questions
OQ-01 DOA value · OQ-02 manual allocation · OQ-03 accrual job · OQ-04 suspend/close action (invariants §8).
