# INDEX — FRD Pack F-PUR-PR · PR ใบขอซื้อ

**Variant:** FULL (9 files + INDEX) · **Mode:** WF-01 Mode B (HTML-first) · 2026-09-13

## Quick Nav

| ไฟล์ | สำหรับใคร | เนื้อหา |
|---|---|---|
| [`00_OVERVIEW.md`](00_OVERVIEW.md) | ทุกคน | Document Control · Scope · Roles · Dependencies · **§0.12 Coverage Manifest** · **§0.13 Open Questions** |
| [`01_UI.md`](01_UI.md) | **FE dev** | **§1.0 Layout Decision Log** · 3 หน้า + 3 overlay · B2 v2 grid · microcopy verbatim |
| [`02_API.md`](02_API.md) | **BE dev (HTTP)** | API-01..API-12 · **§2.9 Cross-Module Contract** · **§2.10 Error Catalog** (16 code) |
| [`03_LOGIC.md`](03_LOGIC.md) | **BE dev (logic)** | FN-01..FN-16 · ENG-PR-CALC · ENG-DOA-RESOLVE · **§3.3 R8 Trace Table** |
| [`04_DB.md`](04_DB.md) | **DBA / BE dev** | 6 tables · **Data Classification ทุก column** · indexes |
| [`05_RULES.md`](05_RULES.md) | **BE dev + QA** | BR-01..12 · V-01..09 · EC-01..07 + CL/CA · C-01..08 · **§5.7 D-CLASS** |
| [`06_TESTS.md`](06_TESTS.md) | **QA** | AT-01..AT-40 · **§6.8 Traceability Matrix** · **§6.9 Cross-Module Tests** · DoD |
| [`07_LOCKED_DECISIONS.md`](07_LOCKED_DECISIONS.md) | **ทุกคน** | **§7.0 Scope Lock + HANDOFF §3 ครบ 10 ข้อ** · LD-01..LD-13 · Convention Deviations |

### ใบประกาศตามชิป (`dec: doa · ntf · csq · doccfg · pdfdoc`)
| ไฟล์ | ชิป | ใช้ทำอะไร |
|---|---|---|
| [`DOA_BRIEF_F-PUR-PR-001.md`](DOA_BRIEF_F-PUR-PR-001.md) | ⚖ `doa` | matrix ที่ต้องไปตั้งที่ทะเบียน DOA กลาง + field contract |
| [`NTF_BRIEF_F-PUR-PR-001.md`](NTF_BRIEF_F-PUR-PR-001.md) | 🔔 `ntf` | 7 event ที่ต้อง wire เข้า `ENG-NOTIFY` |
| [`CSQ_BRIEF_F-PUR-PR-001.md`](CSQ_BRIEF_F-PUR-PR-001.md) | ◆ `csq` | 2 event เข้าท่อ 7C (EC) + ท่อที่จงใจไม่ประกาศ |
| [`DOCCFG_BRIEF_F-PUR-PR-001.md`](DOCCFG_BRIEF_F-PUR-PR-001.md) | `doccfg` | จด `doc_type = PR` · จุดออกเลข · จุดเก็บสำเนา |
| [`PRINT_SPEC_F-PUR-PR-001.md`](PRINT_SPEC_F-PUR-PR-001.md) | 📄 `pdfdoc` | แบบพิมพ์ A4 · ปี ค.ศ. · ช่องลายเซ็นแปรตามสายจริง |
| [`HTML_UI_BRIEF_F-PUR-PR-001.md`](HTML_UI_BRIEF_F-PUR-PR-001.md) | — | anatomy ระดับ selector สำหรับ FE (สกัดจาก HTML 1:1) |

---

## Cross-Reference — UI → API → Logic → DB

| UI action (route) | API | Functions | Engines | Tables |
|---|---|---|---|---|
| เปิดหน้ารายการ (`#/list`) | API-01 | FN-01, FN-16 | — | `t_pr_header` · `t_pr_approval_slot` |
| เปิดเอกสาร (`#/view/:id`) | API-02 | FN-02, FN-11, FN-07, FN-16 | — | ทุกตาราง |
| บันทึกร่างใหม่ (`#/create`) | API-03 | FN-03, FN-04, FN-05 | ENG-PR-CALC | `t_pr_header` `t_pr_line` `t_pr_vendor_suggest` `t_pr_history` |
| แก้ร่าง (`#/edit/:id`) | API-04 | FN-06, FN-04, FN-05 | ENG-PR-CALC | `t_pr_header` `t_pr_line` `t_pr_history` |
| **ส่งอนุมัติ** (modal) | API-05 | FN-08, FN-05, FN-07 | ENG-PR-CALC · ENG-DOA-RESOLVE · ENG-DOC-NUM · ENG-NOTIFY | + `t_pr_approval_slot` |
| อนุมัติ | API-06 | FN-09, FN-11 | ENG-NOTIFY · ENG-CSQ · ENG-DOC-STORE | `t_pr_approval_slot` `t_pr_header` `t_pr_history` |
| ไม่อนุมัติ | API-07 | FN-13, FN-11 | ENG-NOTIFY | เหมือนบน |
| เรียกคืน | API-08 | FN-10 | ENG-NOTIFY | เหมือนบน |
| ยกเลิก | API-09 | FN-14 | ENG-NOTIFY · ENG-CSQ | เหมือนบน |
| ทำสำเนา | API-10 | FN-12, FN-03 | ENG-PR-CALC | สร้างใบใหม่ |
| แนบ/ลบไฟล์ | API-11 / API-12 | FN-15 | ENG-NOTIFY | `t_pr_attachment` |

## Function Trace (R8)

**mutation API 10/10 มี Function/Engine** ✅ · **Function 16/16 ถูกเรียก** ✅ · **Engine 2/2 ถูกเรียก** ✅ · **ไม่มี orphan** ✅
ตารางเต็ม: [`03_LOGIC.md §3.3`](03_LOGIC.md)

## State Machine

```
draft ──ส่งอนุมัติ──► pending_approval ──อนุมัติครบทุกขั้น──► approved ──ยกเลิก(+เหตุผล)──► cancelled
  │                        │                                      │
  │                        ├──ไม่อนุมัติ(+เหตุผล)──► rejected      └──(hook)──► เทียบราคา / ใบสั่งซื้อ
  │                        └──เรียกคืน(slot→void)──► draft
  └──ยกเลิก──► cancelled
```
รายละเอียด + ผลข้างเคียงต่อ transition: [`05_RULES.md §5.4`](05_RULES.md)

## ★ สิ่งที่ต้องอ่านก่อนเริ่ม dev

1. **[`07_LOCKED_DECISIONS.md §7.0`](07_LOCKED_DECISIONS.md)** — LOCK 7 ข้อจาก BRD + HANDOFF §3 ครบ 10 ข้อ · **แตะข้อไหน = กลับไปหา BA**
2. **[`00_OVERVIEW.md §0.13`](00_OVERVIEW.md)** — OQ 9 ข้อ + `[AI-DEFAULT]` 3 ข้อที่รอ BA ยืนยัน
3. **[`01_HTML/F-PUR-PR.html`](../01_HTML/F-PUR-PR.html)** — **source of truth ของหน้าจอ** · FRD ไม่สวนจอ (R14)
4. **ยอดเงินทุกตัวคำนวณฝั่งเซิร์ฟเวอร์** — ห้ามเชื่อค่าจาก client ([`03_LOGIC`](03_LOGIC.md) ENG-PR-CALC)
5. **3 อย่างที่ห้ามทำเอง:** ออกเลขเอกสาร (`ENG-DOC-NUM`) · เลือกช่องทางแจ้งเตือน (`ENG-NOTIFY`) · ตัดสินสายอนุมัติ (`ENG-DOA-RESOLVE`)
6. **ปุ่มสาธิต 2 ปุ่มต้องถอดก่อน production** — LD-11 · OQ-09
