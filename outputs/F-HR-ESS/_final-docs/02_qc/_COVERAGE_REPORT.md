# Coverage Report — F-HR-ESS (F059 · ESS Portal พนักงานทำเอง) — รอบ 1: HTML

- วันที่: 2026-09-10 · **RE-RUN** หลัง BA re-gate fix order (C3.2 retrace หลังแตะ .html)
- Contract authority: `PREBRIEF.md` + `FUNCTION_CHECKLIST.html` (FN-01..11 + FN-90/92/93/94 = **15 FN**) + `HANDOFF.md` / `STANDARD_BASELINE.md` (MUST 11) + BA `REVIEW_FIX_ORDER_F059_ESS.md §1.1` (c[] list)
- Artifact ที่ตรวจ: `outputs/F-HR-ESS/ess.html` (surgically edited: FIX-01..04 · display-only เท่านั้น)
- Declarations: `5_DECLARATIONS/` → NTF_BRIEF.md ✓ · CSQ_BRIEF.md ✓ · NOT_NEEDED.md (doa/doccfg/pdfdoc) ✓
- Archetype: portal(aggregate) display-only + deep-link — **ไม่ใช่ Pattern Q** (ไม่มี list/wizard/view/pdf surface ของตัวเอง) → Phase 0c ข้าม

## Verdict: 🟢 PASS
สรุป: ครอบ **15/15 FN** · DECL 4/4 (2 need + 2 N/A) · **3 BA gap ปิดครบ (cert / shift / csq-anchor)** · gap block 0 · gap warn 0 · scope creep 0 · NOT-CHECKED 0 · DIVERGENCE 0

## ✅ ยืนยัน 3 BA gap (จาก REVIEW_FIX_ORDER §1.1) — ปิดแล้วทั้งหมด

| BA gap (c[]) | ก่อน | หลัง FIX | Evidence |
|---|---|---|---|
| **c[1]** ยื่นลา/OT/เบิก/**ขอหนังสือ** จากที่เดียว | ⚠️ 3/4 (ขอหนังสือหาย) | ✅ **5/5** deep-link | `LINKS.cert:{route:'#/cert/new'}` (L2225-2230) · launcher actionPicker 5 แถว: `apRow('calendar-plus'..'leave')` / `'clock'..'ot'` / `'receipt'..'expense'` / `'user-pen'..'profile'` / `apRow('award','ขอหนังสือรับรอง',..'cert')` (L2648-2652) · ปุ่ม "ขอหนังสือ" `onclick="deepLink('cert')"` หัว section FN-06 (L2417) |
| **c[4]** ตารางกะ + ประวัติลงเวลา | ⚠️ ครึ่งเดียว (มีแต่ประวัติสแกน) | ✅ ครบ (shift table + scan history) | `DATA.shifts` 7 วัน (L2185) · section "ตารางกะของฉัน · สัปดาห์นี้" ใน renderPay `sec('calendar-clock',...)` + table วัน/กะ (L2390-2393) · ประวัติสแกนเดิมคง (FN-04 L2378) · marked `CH_ASSUMED+CH_RO` (read-only · Time W2) |
| **dec csq** DIVERGENCE (chip◆csq ≠ detect) | ❌ grep CSQ=0 | ✅ 2 anchor → chip=detect | `CSQ: ess.access_denied → ท่อ SecC` ที่ modal accessDenied (L2657) · `CSQ: ess.restricted_view → ท่อ SecC` ที่ payslip render (L2534) · ทั้งคู่ระบุ `CSQ_BRIEF_F059` + `ห้ามประกาศ OC/DC ซ้ำ` · grep `ท่อ OC`/`ท่อ DC` = 0 (ไม่ประกาศท่อสงวน) |

## Coverage Matrix (ทุก item — รอบ 1 ตรวจคอลัมน์ HTML)

| Item | ประเภท | HTML | Evidence |
|---|---|---|---|
| FN-01 หน้ารวมของฉัน (dashboard cards + launcher) | FN | ✓ | `renderHome` (L2307) · quick cards launcher (L1416) · summary หลาย surface |
| FN-02 สลิป + ประวัติ + YTD (อ่าน PS-1 self) | FN | ✓ | `renderPay` FN-02 payslip (L2347) · openView('payslip') · all-or-nothing comment |
| FN-03 วันลา/โควตา + ปุ่ม "ยื่นลา" navigate | FN | ✓ | FN-03 leave read + deep-link (L2359) · `deepLink('leave')` |
| FN-04 OT/เวลา/สแกน **+ ตารางกะ** | FN | ✓ | FN-04 OT/scan (L2378) **+ ตารางกะของฉัน** (L2390-2393) — c[4] ครบ (FIX-02) |
| FN-05 ใบเบิก + ปุ่ม "ยื่นเบิก" navigate | FN | ✓ | FN-05 expense read + deep-link (L2404) · `deepLink('expense')` |
| FN-06 หนังสือรับรอง **+ ปุ่ม "ขอหนังสือ"** | FN | ✓ | FN-06 cert read (L2415) + deep-link 'ขอหนังสือ' (L2417) — c[1] เส้นที่ 5 (FIX-01) |
| FN-07 สวัสดิการ/คงเหลือ · อบรม/ใบรับรอง | FN | ✓ | FN-07 welfare + training (L2425) · DATA.certs/welfare/training render |
| FN-08 โปรไฟล์ + "ขอแก้ข้อมูล" ขออนุมัติ | FN | ✓ | FN-08 profile read + link (L2445) · `deepLink('profile')` #/profile/edit-request |
| FN-09 แจ้งเตือนของฉัน (feed) | FN | ✓ | `renderNotify` (L2462) · feed consume "ศูนย์แจ้งเตือน (ENG-NOTIFY)" (L2481) |
| FN-10 เห็นเฉพาะของตัวเอง — คนอื่น=403 (SecC) | FN | ✓ | self-access banner (L1374) · modal accessDenied 403 (L2656-2663) · CSQ anchor |
| FN-11 surface ba-done → display-only + [ASSUMED] | FN | ✓ | CH_ASSUMED chip (L1399/2160) · soft-ref stub (L2243) |
| FN-90 ค้นหา/filter + empty state | FN | ✓ | search input `oninput` (L2487) · `emptyStateHTML('bell-off','ไม่พบการแจ้งเตือน')` (L2471) · ss combobox emptyText (L1845) |
| FN-92 responsive มือถือ | FN | ✓ | responsive CSS FN-92/BR-05 (L1535) · media queries |
| FN-93 audit การเข้าถึง (append-only) | FN | ✓ | audit log FN-93 append-only (L1530) |
| FN-94 ปิดบังข้อมูลนอกขอบเขต | FN | ✓ | self-access banner FN-10/FN-94 (L1374) · masking mock EMP เดียว · 403 guard |
| S-01..S-11 (PREBRIEF scenarios) | scenario | ✓ | map 1:1 กับ FN-01..11 (Coverage §11) — เดินได้ครบ happy/alt/exception ใน tab home/pay/docs/notify + accessDenied |
| DECL-NTF (consume feed) | decl | ✓ | chip ✓need → `NTF_BRIEF.md` ✓ + anchor ENG-NOTIFY consume (L2481) · ESS ไม่ยิง event เอง (display-only) |
| DECL-CSQ (SecC self-access) | decl | ✓ | chip ✓need → `CSQ_BRIEF.md` (event ess.self_access · ท่อ SecC) ✓ + 2 HTML anchor (L2534/2657) · **DIVERGENCE ปิด** (FIX-03) |
| DECL-DOA | decl | N/A | portal อ่านอย่างเดียว · ไม่มี action อนุมัติ/slot picker · NOT_NEEDED.md — ยืนยัน grep mutation/approval = 0 |
| DECL-DOCCFG | decl | N/A | ไม่ออกเอกสาร/เลขรันเอง · NOT_NEEDED.md — ไม่มี running-number pattern ในไฟล์ |
| Scope guard: ไม่ CRUD feature อื่น (OQ-HR-04) | guard | ✓ | grep `<form`/`onsubmit`/`.submit(`/`do*`/`save*`/`create*`/`update*`/`delete*` = **0 match** · deepLink = navigate-out stub (showToast) เท่านั้น (L2674-2681) |

## 🟢 Display-only lock (OQ-HR-04) — ยืนยันคงอยู่
- **ไม่มี mutation function** ใด ๆ: grep `function do[A-Z]/save/create/update/delete` = 0 · ไม่มี `<form>` · ไม่มี `onsubmit` · ไม่มี `.submit()`
- ทุก "ยื่น"/"ขอ" = **deep-link OUT เท่านั้น** — `deepLink(key)` (L2675) แค่ `showToast('กำลังนำทางไปหน้า...')` แล้วปิด modal/drawer · ไม่มีการรับ/บันทึกคำขอในพอร์ทัล
- modal actionPicker note ย้ำ "ESS ไม่รับหรือบันทึกคำขอเอง ... ตามมติ OQ-HR-04" (L2653)
- FIX-04 (cosmetic): องค์ประกอบสาธิตติด class `.demo-only` + `/* DEMO-ONLY */` comment (CSS L1394-1397 · CH_ASSUMED/CH_RO L2243-2244 · demo-strip L2285) — prod strip ได้ · ไม่กระทบ scope/FN

## 🔴 Gaps: — (ไม่มี)
## 🟡 Warnings / Scope Creep: — (ไม่มี)
- ตารางกะ (FIX-02) และ cert deep-link (FIX-01) = BA สั่งเพื่อปิด c[4]/c[1] โดยตรง · ทั้งคู่ display-only ([ASSUMED] soft-ref) → **in-scope ไม่ใช่ creep**
## ⬜ NOT-CHECKED: — (รอบ 1 HTML ตรวจครบทุก item)

## 📌 หมายเหตุ OQ ที่ยกไปรอบ FRD (ไม่กระทบ verdict รอบนี้)
- **OQ-ESS-01**: event_id CSQ จริง (anchor ใช้ `ess.access_denied`/`ess.restricted_view` · CSQ_BRIEF ประกาศ `ess.self_access`) — ท่อ SecC ตรงกัน · ชื่อ event ปลายทางรอ Strike+Architect เคาะก่อนเขียน FRD §CSQ
- **OQ-ESS-02**: route deep-link ทั้ง 5 เส้น (#/leave/new · #/ot/new · #/expense/new · #/profile/edit-request · #/cert/new) ยัง [ASSUMED contract] — ยืนยัน route จริงกับ feature เจ้าของก่อน FRD §Integration

## Diff จากรอบก่อน (BA re-gate BLOCK → รอบนี้)
- **ปิดแล้ว**: FIX-01 (c[1] cert เส้นที่ 5) · FIX-02 (c[4] ตารางกะ) · FIX-03 (dec csq anchor → DIVERGENCE หาย)
- **ค้าง**: — (ไม่มี block/warn ค้าง)
- **ใหม่**: — (ไม่มี gap/creep ใหม่จากการแตะ .html)
