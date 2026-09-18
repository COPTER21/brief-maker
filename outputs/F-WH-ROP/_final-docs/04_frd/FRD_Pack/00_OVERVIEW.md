# 00 OVERVIEW · F-WH-ROP

## 0.1 Identity

- Feature: F085 / F-WH-ROP · Reorder Point
- Module/Wave: Warehouse · W4 FULL
- Routes: `#/records`, `#/history`, `#/settings`
- Source: BRD v2.0 + approved HTML + PM/BA decisions 2026-09-18

## 0.2 Purpose

Maintain versioned replenishment policy per Item×Warehouse, evaluate F009 ATP snapshots, notify low stock and create grouped F072 PR Drafts without auto-submit.

## 0.3 Scope Lock

In: policy, evaluation, three statuses, scheduler/movement/manual triggers, NTF, grouped PR Draft, append-only history. Out: hold calculation, stock mutation, PO, vendor selection, PR approval, 7C result UI, printable document.

## 0.4 Roles

`rop_policy_admin`, `rop_planner`, `rop_auditor`, scheduler service and movement subscriber. All production reads/writes require tenant and warehouse authorization.

## 0.5 Core Formula

`ROP=max(min_qty,safety_qty+adu*lead_time_days)`; trigger iff `ATP<ROP`; `raw=max(0,max_qty+safety_qty-ATP-on_order)`; `suggested_qty=ceil(raw/pack_size)*pack_size`.

## 0.6 Integrations

F009 provides ATP/ADU/On-Order/asOf. ENG-NOTIFY consumes `reorder_point.triggered`. F072 creates Draft with `origin_type=reorder_point`; F072 owns PR lifecycle and DOA submission.

## 0.7 Declarations

NTF enabled. CSQ emits only `master.changed` to SecC after sensitive policy commit. No DOA or DOCCFG declaration for F085.

## 0.8 Data Classification

Policy values and stock figures are Confidential business data. Actor references and audit metadata follow central classification; do not send raw person names in integration envelopes.
