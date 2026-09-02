---
file_id: KB-03-TEMPLATE
title: VS Bible Template
version: 1.0.0
last_updated: 2026-05-27
status: template
---

# [VS Name] — Full Bible Template

> **How to use**: Copy this file to `[vs-id]-bible.md`, fill in each section, then add entry in INDEX.md

## Quick Reference (TL;DR)

- **VS**: [Name]
- **Trigger**: [event ที่เปิด VS]
- **Outcome**: [จุดจบที่วัดได้]
- **VCs**: [list]
- **Invariants**: [rules ที่ทุก VC ต้องปฏิบัติ]

---

## §1. VC Catalog

| VC | name | trigger event | decision criteria | key feature |
|---|---|---|---|---|
| VC1 | ... | ... | ... | ... |

---

## §2. Path Catalog (per VC)

ใส่ table ของแต่ละ VC ว่ามี path อะไรบ้าง + outcome state

---

## §3. Anchors / Invariants

Rules ที่ cross ทุก VC

---

## §4. Edge Cases (Business-Level)

ไม่ใช่ system edge — แต่เป็น business event ที่ระบบต้องรับมือ

---

## §5. Locked Decisions

ตัดสินไปแล้ว ห้ามเปลี่ยนโดยไม่ review ร่วม

---

## §6. Feature Catalog (VS-specific)

| feature_id | name | status (done/wip/backlog) |
|---|---|---|

---

## §7. Glossary (VS-specific terms)

---

## Change Log

- **1.0.0** (YYYY-MM-DD): Initial draft
