# UI BRIEF — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ (AS-BUILT)

> ใช้คู่: **HTML `offsite-work-request.html` (source of truth)** + **FRD_F-HR-OSW_Pack** + บรีฟนี้ (design intent + แผนที่โค้ด)
> ทุกบรรทัดสกัดจาก HTML — anchor = selector / function / ข้อความจริง · ข้อเสนอที่ไม่ใช่ของจริงอยู่ §13 เท่านั้น

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `offsite-work-request.html` รอบ 4 (kit html-generator-v9.2 · ~230 KB · single-file SPA) |
| Gate ของ HTML | E2E 64/64 · PDF/DOA 13/13 · smoke 112 views pageerror 0 · self_audit PASS · audit.sh FAIL 9 = กฎ B2 line editor (ไม่ใช้กับเอกสารนี้ — FRD 07 CD-03) |
| FRD | `FRD_F-HR-OSW_Pack` v1.0 (FULL) — paired ✅ |
| Print | `print/osw_body.tpl.html` (เหมือน `OSW_TPL` ใน HTML) + `print/OSW_print-spec.md` |
| Drift | 0 business drift · 2 รายการ HTML-only ที่ไม่ใช่ของระบบจริง (§11) |
| วันที่ | 5 ต.ค. 2569 |

## §1 Design Tokens AS-BUILT
**CSS variables (`:root`)** — ใช้ตามนี้ ห้ามตั้งค่าใหม่
| กลุ่ม | ตัวแปร = ค่า |
|---|---|
| สีหลัก | `--c-navy` #111111 · `--c-primary` #FF3B30 · `--c-primary-hover` #E62E24 · `--c-teal` #FF9A1F · `--c-teal-light` #FFB763 · `--c-ink` #111111 |
| ตัวหนังสือรอง | `--c-mute` #54565C · `--c-mute-2` #73757B · `--c-mute-3` #9A9CA2 · `--c-placeholder` rgb(180,182,188) |
| เส้น/พื้น | `--c-line` #DEDAD4 · `--c-line-2` #E9E5E0 · `--c-line-3` #F1EEEA · `--c-bg-off` #FAF8F5 |
| สถานะ | `--c-success` #1F9D55 · `--c-warning` #E8870F · `--c-danger` #E62E24 |
| Shell | `--sidebar-w` 232px · `--shell-h` 52px |
| Type | `--fs-h1` 22 · `--fs-h2` 17 · `--fs-h3` 15 · `--fs-body` 14 · `--fs-sub` 13 · `--fs-meta` 12 · `--fs-cap` 11 · `--fs-kpi` 28 (px) |
| Spacing | `--sp-xs` 4 · `--sp-sm` 8 · `--sp-md` 12 · `--sp-lg` 20 · `--sp-xl` 28 (px) |
| Radius | `--r-xs` 4 · `--r-sm` 6 · `--r-md` 8 · `--r-lg` 12 · `--r-full` 999 (px) |
**Font:** `'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` (หัวหน้า `.ph-title` = Noto Sans Thai) · **PDF** ใช้ Sarabun (แยกโลก — อยู่ใน iframe)
**Icons:** Lucide 0.469.0 (loader multi-CDN · `renderIcons()`) · เมนู ⋮ render ไอคอนเฉพาะในเมนู (`data-rmic`) กันคลิกทะลุ

**z-index map (สูง → ต่ำ)**
| z | ตัวแปร | ใช้กับ |
|---|---|---|
| 80 | `--z-toast` | `#toast` |
| 70 | `--z-popover` | `.row-menu` (⋮) · `.ss-list.menu-fixed` (search-select ที่ portal ออกจาก drawer/modal) · `.menu-fixed` |
| 60 | `--z-modal` | `.modal-backdrop` (modal อยู่เหนือ drawer เสมอ) |
| 51 | `--z-drawer` | `#drawer` |
| 50 | `--z-backdrop` | `#drawerBackdrop` · `.ss-list` (ปกติ) |
| 30 | `--z-dropdown` | `.user-menu` · `.info-tip::after` |
| 10 | `--z-sticky` / `--z-shell` | `.shell-bar` · `.sidebar` · `thead th` sticky · `.wizard-footer` |
| 1–3 | literal | stepper circle/line · sticky thead ใน `.table-scroll` |

## §2 Route Map
| Route | หน้าที่ | เปิดด้วย | Refresh-safe |
|---|---|---|---|
| `#/offsite` | P-01 รายการ (default ของ feature) | `go('offsite')` หลังปิด drawer | ✅ |
| `#/offsite/view/:id` | P-03 รายละเอียด | `showDrawer({kind:'view'})` → `go('offsite/view/'+id)` | ✅ `applyRoute()` เปิด drawer เอง (ถ้าไม่มีสิทธิ์ดู = ไม่เปิด) |
| `#/offsite/create` | P-02 สร้าง | `startWizard()` | ✅ |
| `#/offsite/create/copy-:id` | P-02 ทำซ้ำ | `dupRec(id)` | ✅ |
| `#/offsite/edit/:id` | P-02 แก้ไขร่าง | `startWizard(id)` | ✅ (ไม่ใช่ร่างของตัวเอง → toast + ไม่เปิด) |
กลไก: `go(r)` เขียน hash (ข้ามเมื่อรันใน `about:` srcdoc) · `applyRoute()` ผูก `hashchange` + เรียกครั้งแรกใน `render()` (`S.booted`) · back ของเบราว์เซอร์ = ปิด/เปิด drawer ตาม route

## §3 Layout Shell
| ส่วน | Anchor | AS-BUILT |
|---|---|---|
| Sidebar | `.sidebar` · `.sb-module[data-module="hr"]` · `.sb-item[data-feature="offsite"]` | 232px · module "HR" (หุบได้ `toggleModule`) · feature "ขอออกนอกสถานที่" + `#sbBadge` (จำนวนรอฉันพิจารณา · ซ่อนเมื่อ 0) |
| Shell bar | `.shell-bar` | สูง 52 · breadcrumb `Core › HR › ขอออกนอกสถานที่` · กระดิ่ง (`#notifBtn`) · user chip (`#ucName` `#ucRole` `#ucAv`) |
| User menu | `#userMenu` | **prototype only:** "สลับผู้ใช้ (ตัวอย่างสายอนุมัติ)" (`#personaList` · `switchPersona`) · ระบบจริงเหลือแค่ ออกจากระบบ |
| Content | `#page-content` · `.page-fill` | กว้างเต็ม (ไม่มี max-width) · ตารางยืดถึงขอบล่าง |
| Responsive | `@media (max-width:1180px)` | การ์ดสรุป wizard ย้ายลงล่าง · fields-4 → 2 คอลัมน์ · 1024 ไม่มี h-scroll |

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
```
.page-fill
├ .ph  — h1 .ph-title + .ph-en "(Off-site Work Request)" · .ph-count "N รายการ · เปิดอยู่ M" · .ph-sub
│        .ph-actions: [ส่งออก CSV] exportCSV() → [สร้างคำขอ] #btnCreate startWizard()
├ .alert-row.is-danger (เฉพาะ DOC.active=false)
├ .stats — statCard('all'|'pending'|'mine') → setStat(k)   (.stat.is-click.is-on = กำลังกรอง)
└ .card.list-card
   ├ .filter-bar: .input-search #fq onQ() · ss 'fst' · ss 'fmode' · ss 'fdept' · .fb-spacer · [ล้างตัวกรอง] resetFilters()
   ├ .table-wrap > table.table — thead sortTh(col) · tbody tr.is-clickable rowClick(event,id)
   │     td: .code-strong เลขที่ | วันที่ขอ | ผู้ขอ | ช่วงที่ไป (title=ช่วง·วัน) | pill(MODE) | docPill | renderSignProgress | num r เบี้ยเลี้ยง | .row-actions-cell .ra-btn ⋮ openRowMenu(id,this)
   └ .table-foot pager() — ".num a – b จาก N" ซ้าย · .pagination ขวา
```
### P-02 สร้าง/แก้ไข (`renderWizard()` ใน `#drawer.drawer.wide`)
```
.dw-head  — .dw-eyebrow (file-plus "สร้างเอกสารใหม่" | pencil "แก้ไขเอกสาร") · h2.dw-title · .top-icon-btn ปิด
            .d-stepper > .stepper-item × 3 (active/done · done คลิก goStep(n))
.drawer-body.is-soft (ขั้น 1 พื้น off-white)
  ขั้น 1 wizMain(): .wz-split
    .wz-main — STEPH · (alert ทำซ้ำ)
      .wz-card ①  .wz-card-h(.wz-no "1" · "ไปเมื่อไหร่ ทำอะไร" · #oswDays)
                  .trips > tripCard(l,i,n) × N   ·  button.add-row addLine()
      .wz-card ②  .wz-card-h(.wz-no "2" · "ค้างคืนไหม")
                  .track-grid > .track-card × 2 setMode('day'|'overnight')  (.tc-ic · .tc-main · .tc-radio)
                  (overnight) .pd-line [#pdN #pdP #pdTotal · #nightsHelp] + .link-btn toggleNights()
                  (adjust) .pd-adjust > #fNights · #fPaid  (numStep → .num-step)
    aside.wz-sum sumCard(f) — ผู้ขอ / เรียน (empChip) · #sumRange #sumDays · ลักษณะ · .wz-sum-total #sumTotal · .wz-sum-foot
  ขั้น 2 wizAttach(): STEPH · .upload-zone (คลิก → #oswFile) · .file-row × N removeFile(i)
  ขั้น 3 wizReview(): STEPH · (.alert-row ย้อนหลัง) · .review-card × 4 (ข้อมูลคำขอ · วันที่ไปปฏิบัติงาน linesTable · ค่าเบี้ยเลี้ยง perDiemBlock · เอกสารแนบ)
.dw-footer — ซ้าย [ย้อนกลับ] wizBack() · ขวา [ยกเลิก] closeDrawer() → [ถัดไป] #btnNext wizNext() | [บันทึกแบบร่าง] #btnDraft saveDraft() + [บันทึกและส่งขออนุญาต] #btnSaveSubmit saveAndSubmit()
```
**tripCard** (`.trip` · `#ln-i`): `.trip-h` (`.trip-no` "วันที่ไป"/"ช่วงที่ N" · `.trip-days #ldays-i` · ลบ `removeLine(i)` เมื่อ N>1) · `.trip-dates` (`[name=ld-f-i]` · `.trip-to` "ถึง" · `[name=ld-t-i]` min=d_from) · `input.trip-why [name=lp-i]` · `.trip-time` (ซ่อน: "08:30 – 17:30 น." + `.link-btn showTime(id)` / แสดง: `[name=lt-f-i]` `[name=lt-t-i]`) · `.trip-err` (ข้อความแรกของช่วง)

### P-03 รายละเอียด (`renderViewDrawer()` ใน `#drawer` 920)
```
.dw-head — .doc-ident(.doc-ident-ic map-pin · .dw-eyebrow · .doc-ident-row: h2.dw-title.mono code + docPill + pill(MODE) · .dw-sub)
           .dw-actions: [ปุ่มตามสถานะ §8] · .drawer-header-divider · .top-icon-btn ทำซ้ำ dupRec · พิมพ์ genPdf(id,true) · ดาวน์โหลด PDF genPdf(id) · ปิด
.drawer-tabs — tabBtn('detail'|'pdf'|'sign'|'history') → setTab
.drawer-body — renderDetailTab | renderPdfTab | renderSignTab | renderHistoryTab
.dw-footer — .dw-foot-meta "แก้ไขล่าสุด … · by" (+ lock "อนุญาตแล้ว ล็อกแก้ไข") · [ปิด]
```
- **detail:** `viewBanner()` → SEC info "ข้อมูลเอกสาร" (.drawer-fields: เลขที่ · วันที่ขอ · สถานะ · เรียน) → SEC user "ผู้ขอ" → SEC calendar-range "รายการวันที่ปฏิบัติงาน (N)" + `.sec-meta` "รวม M วัน" + `linesTable` (.osw-view-lines) → SEC wallet `perDiemBlock` (.osw-pd 4 ช่อง / .is-off) → SEC paperclip "เอกสารแนบ (N ไฟล์ · Document Center)" → SEC database "ข้อมูลระบบ"
- **pdf:** `.pv-bar` (.pv-meta + .pv-actions) → `.a4 > .pdf-slot > iframe.pdf-frame[srcdoc=oswPdfDoc(r)]` · `onload=fitPdf` ปรับสูง ≥1123px ตามเนื้อหา
- **sign:** `.review-card` (.drawer-fields.fields-4: สายอนุมัติ .kbd "{doa_entry_ref} · N ขั้น" · สถานะ+ขั้น n/N · ผู้ส่ง empChip · ผลโดย) + `.sp-bar.is-wide` → SEC pen-tool `.timeline` (ส่งขออนุญาต → ขั้น 1..N + `.tl-acts` อนุญาต/ไม่อนุญาต inline เมื่อ canAct → ผลลัพธ์)
- **history:** SEC history "ประวัติ (append-only)" `.timeline` ใหม่→เก่า (`tl-dot.is-success|is-danger` ตาม tone)

## §5 Component Inventory
| Component | Anchor | States (AS-BUILT) | ขนาด/หมายเหตุ |
|---|---|---|---|
| Stat card | `.stat.is-click` `statCard()` | default · hover (border) · active `.is-on` · disabled — | grid auto-fit min 200 |
| Search-select | `searchSelectHTML(key)` + `initSearchSelect` (`fst` `fmode` `fdept` `slot{i}`) | default · focus → list · typing filter + `<mark>` · keyboard ↑↓ Enter Esc · clear X · empty "ไม่พบรายการ" · invalid (ผ่าน `.field.is-invalid`) | list portal เมื่ออยู่ใน drawer/modal (`menu-fixed`) |
| Sort header | `th.is-sortable` `sortTh()` | ↕ / ↑ / ↓ · `.is-sorted` | |
| Row menu ⋮ | `.row-menu` `.rm-item(.is-danger)` `openRowMenu()` | open / ปิดเมื่อคลิกนอก / scroll | fixed `--top/--left` · flip ขึ้นถ้าที่ล่างไม่พอ · min-width 180 |
| Doc pill | `docPill()` / `pill(DOC_ST)` | 5 ค่า §8 | |
| Mode pill | `pill(MODE)` | ไป-กลับ `.pill-info` · ค้างคืน `.pill-warning` | |
| Sign progress | `.sign-prog` `.sp-bar` `.sp-fill --p` | ร่าง = "—" · n/N · rejected = `.is-bad` แดงเต็ม | bar 46px |
| Trip card | `.trip` `tripCard()` | default · `.is-bad` (ขอบแดง + `.trip-err`) · input `.is-bad` · time hidden/shown | |
| Add row | `.add-row` | default dashed · hover แดง | สูง 40 |
| Track card | `.track-card(.is-on)` `.tc-radio` | default · hover · selected (ขอบ primary + radio เต็ม) | 2 คอลัมน์ |
| Per-diem line | `.pd-line(.is-warn)` | ปกติ · warn (พื้นส้ม) เมื่อคืนเกินช่วง/คืนที่ได้ > คืนที่ค้าง | ตัวเลข soft update ไม่ rebuild |
| Num stepper | `.num-step(.is-bad)` `.ns-btn` `stepNum()` `setNum()` | default · invalid · ค่า < 0 ไม่ได้ | สูง 40 · ปุ่ม 40 |
| Summary card | `aside.wz-sum` | sticky top · `.wz-sum-total.is-off` เมื่อไป-กลับ | 300px · ≤1180 static |
| Upload zone | `.upload-zone` + `#oswFile` | ว่าง "คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)" / มีไฟล์ "แนบไฟล์เพิ่ม" · error toast | |
| Slot row (DOA) | `.slot-row` `.slot-no` `.slot-role` `#fSlot{i}` | default (ค่าเริ่มจาก `resolveDoa`) · invalid "กรุณาเลือกผู้พิจารณา" | 1 แถวต่อขั้น |
| Reason chips | `.chip-row` `.chip(.is-on)` `setReasonPreset()` | default · selected | เติมข้อความลง textarea |
| Buttons | `.btn-primary/secondary/ghost/success/danger/link(.is-danger)` | default · hover · disabled (busy) · loading "กำลังบันทึก…" + `loader-2 .spin` | primary เดียวต่อ footer |
| Empty state | `emptyStateHTML()` | 2 แบบ (§9) | |
| Toast | `#toast` `showToast()` | info/success/warning/error | ขวาล่าง · 2.8s |

## §6 Overlay Registry
| Overlay | Anchor | ขนาด | เปิด | ปิด / Dismiss rules | z |
|---|---|---|---|---|---|
| Drawer สร้าง/แก้ไข | `#drawer.drawer.drawer-panel.wide` `renderWizard` | min(1290px,100vw) | `startWizard()` | ปุ่ม X · `ยกเลิก` · backdrop · Esc → **ถ้ากรอกค้าง (`S.dw.dirty`) เปิด M-05 แทน** · บันทึกสำเร็จ = ปิดแบบ force | 51 |
| Drawer รายละเอียด | `#drawer.drawer.drawer-panel` `renderViewDrawer` | min(920px,100vw) | `openView()` / route | X · `ปิด` · backdrop · Esc | 51 |
| Backdrop drawer | `#drawerBackdrop` | เต็มจอ | คู่ drawer | คลิก = `closeDrawer()` | 50 |
| M-01 ส่งขออนุญาต | `.modal.is-lg` kind=submit | 680 | `openSubmit()` (หลัง saveAndSubmit / ปุ่มส่ง) | `ยกเลิก` · backdrop · Esc · ไม่ปิดเองถ้า API ล้ม | 60 |
| M-02 อนุญาต | `.modal` kind=approve | 440 | `openApprove()` | `ยกเลิก` · Esc · **backdrop ไม่ปิดเมื่อพิมพ์ความเห็นแล้ว** | 60 |
| M-03 ไม่อนุญาต | `.modal` kind=reject | 440 | `openReject()` | `ยกเลิก` · Esc · **backdrop ไม่ปิดเมื่อมีเหตุผล** | 60 |
| M-04 ยกเลิกเอกสาร | `.modal` kind=cancel | 440 | `openCancel()` | `ไม่ยกเลิก` · Esc · **backdrop ไม่ปิดเมื่อมีเหตุผล** | 60 |
| M-05 ทิ้งข้อมูล | `.modal` kind=discard | 440 | `closeDrawer()` ขณะ dirty | `กลับไปกรอกต่อ` · `ทิ้งข้อมูล` → `closeDrawer(true)` | 60 |
| Row menu ⋮ | `.row-menu` ใน `#overlay-root` | ≥180 | `openRowMenu()` | คลิกนอก · scroll (capture) · เลือกเมนู | 70 |
| Search-select list | `.ss-list` | สูงสุด 280 | focus input | เลือก · Esc · คลิกนอก | 50/70 |
| User menu | `#userMenu.is-open` | — | `toggleUserMenu()` | คลิกนอก | 30 |
| PDF generator | `iframe.pdf-gen` ใน `#overlay-root` | 0×0 hidden | `genPdf()` | — (ค้างไว้ใช้ซ้ำ) | — |
| Toast | `#toast` | auto | `showToast()` | 2.8s auto | 80 |
Animation: drawer slide 280ms (`.is-open` translateX) · modal scale 0.96→1 200ms · backdrop opacity 200ms · `prefers-reduced-motion` ปิดแอนิเมชัน

## §7 Interaction Spec
- **Esc chain** (kit `keydown`): `state.modal.open` → `closeModal()` → else `state.drawer.open` → `closeDrawer()` (dirty → M-05) · search-select จัด Esc ของตัวเอง (`ssOnKey`)
- **Click-outside:** user menu (`document click`) · row menu (คลิกนอก `.row-menu`/`.row-actions-cell`) · search-select · modal backdrop → `modalBackdropClick()` (กันปิดเมื่อมีข้อความ)
- **Row click vs ⋮:** `rowClick(ev,id)` ข้ามเมื่อคลิกใน `.row-actions-cell`
- **Render preservation:** `render()` ห่อ `preserveRenderState/restoreRenderState` (scroll drawer + focus input) · ช่อง "เพื่อ" และตัวเลขคืน **soft update** (ไม่ rebuild — focus/caret คงอยู่) · วันที่/เวลาใช้ `onchange` แล้ว render
- **Auto behaviors:** เลือกวันที่ไป → ถึงวันที่ = วันเดียวกันถ้าว่างหรือก่อน · `ไปอีกช่วง` ยกเวลา+เพื่อ + focus `ld-f` ใหม่ (RAF) · ค้างคืน: `nAuto` → คืน = Σ(วัน−1) ทุกครั้งที่เปลี่ยนวันที่ จนผู้ใช้ปรับ · คืนที่ได้ตามคืนที่ค้างจนแยก
- **Busy:** ปุ่มบันทึก/ส่ง/อนุญาต disabled + "กำลังบันทึก…" ระหว่างทำงาน (`S.busy`) · กันกดซ้ำ
- **Toast หลังปิด:** drawer ปิดก่อน แล้ว toast (setTimeout 220–300ms)
- **Positioning:** row menu = fixed (`--top/--left`) จาก `getBoundingClientRect` · flip ขึ้นเมื่อด้านล่างไม่พอ · search-select ใน drawer/modal ใช้ portal (`menu-fixed`) กันจมใต้ overflow
- **PDF:** iframe srcdoc แยก CSS (thai-doc base + FORM REPLICA) จากหน้าหลัก · `fitPdf` วัดความสูง · `genPdf` = iframe ซ่อน → `document.fonts.ready` → `print()` · title = เลขที่ (ชื่อไฟล์เวลาบันทึกเป็น PDF)

## §8 State-Driven UI Matrix
| status (`DOC_ST`) | Label | Pill class | Header actions (P-03) | ⋮ menu | Banner |
|---|---|---|---|---|---|
| `draft` | ร่าง | `pill-muted` | เจ้าของ: `ยกเลิก`(link danger) · `แก้ไข` · `ส่งขออนุญาต`(primary) | ทำซ้ำ · แก้ไข · พิมพ์ · ยกเลิกเอกสาร | "ยังเป็นร่าง — ส่งขออนุญาตเมื่อข้อมูลครบ" |
| `pending` | รออนุญาต | `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: `ไม่อนุญาต`(link danger) · `อนุญาต`(success) · เจ้าของ/HR: `ยกเลิกเอกสาร` | ทำซ้ำ · พิมพ์ · (ยกเลิกเอกสาร) | "รอ {ชื่อ} พิจารณา" (+ " — คุณเป็นผู้พิจารณาคำขอนี้") |
| `approved` | อนุญาตแล้ว | `pill-success` | เจ้าของ/HR: `ยกเลิกเอกสาร` · footer lock | ทำซ้ำ · พิมพ์ · (ยกเลิกเอกสาร) | — |
| `rejected` | ไม่อนุญาต | `pill-danger` | — | ทำซ้ำ · พิมพ์ | "ไม่อนุญาต — {เหตุผล}" |
| `cancelled` | ยกเลิก | `pill-muted` | — | ทำซ้ำ · พิมพ์ | "ยกเลิกแล้ว — {เหตุผล}" |
Chain step status (`renderSignTab`): `approved` อนุญาต · `rejected` ไม่อนุญาต · `pending` รอพิจารณา · `waiting` ยังไม่ส่ง · `skipped` ข้าม
PDF ตามสถานะ: draft → footer "· ร่าง" + ช่องลายเซ็นวันที่ "วันที่ ........./........./........." · ตัดสินแล้ว → ☑ + "พิจารณาในระบบ วันที่ เวลา น."
**DB ↔ UI:** prototype ใช้ `pending` = FRD `pending_approval`

## §9 Microcopy (verbatim)
| หมวด | ข้อความ |
|---|---|
| หัวหน้า | "แบบขออนุญาตออกปฏิบัติงานนอกสถานที่" · "(Off-site Work Request)" · "ขออนุญาตผู้บังคับบัญชาก่อนออกไปปฏิบัติงานนอกสถานที่ · คำนวณเบี้ยเลี้ยงเมื่อค้างคืน" |
| stats | "คำขอทั้งหมด" / "ที่คุณเกี่ยวข้อง" · "รออนุญาต" / "รอผู้บังคับบัญชาพิจารณา" · "รอฉันพิจารณา" / "คลิกเพื่อดูรายการ" · "ไม่มีรายการค้าง" |
| filter | placeholder "ค้นหาเลขที่ / ผู้ขอ / เพื่อ" · "ทุกสถานะ" · "ทุกลักษณะ" · "ทุกฝ่าย" · "ล้างตัวกรอง" |
| คอลัมน์ | "เลขที่" · "วันที่ขอ" · "ผู้ขอ" · "ช่วงที่ไปปฏิบัติงาน" · "ลักษณะ" · "สถานะเอกสาร" · "ลายเซ็น" · "เบี้ยเลี้ยง (บาท)" |
| ⋮ | "ทำซ้ำ" · "แก้ไข" · "พิมพ์" · "ยกเลิกเอกสาร" |
| wizard | eyebrow "สร้างเอกสารใหม่" / "แก้ไขเอกสาร" · h2 "ขออนุญาตออกปฏิบัติงานนอกสถานที่" / "แก้ไขคำขอ {code}" · steps "ข้อมูลหลักคำขอ" "เอกสารแนบ" "ตรวจสอบและยืนยัน" |
| ขั้น 1 | hint "ใส่วันที่และเรื่องที่จะไป แล้วเลือกว่าค้างคืนไหม — ที่เหลือระบบคำนวณให้" · "ไปเมื่อไหร่ ทำอะไร" · "วันที่ไป" / "ช่วงที่ N" · "ถึง" · placeholder "ไปทำอะไร ที่ไหน — เช่น ตรวจงานติดตั้ง (โรงงานลูกค้า ขอนแก่น)" · "08:30 – 17:30 น." · "เปลี่ยนเวลา" · "น." · "ไปอีกช่วง" · "ค้างคืนไหม" · "ไป-กลับ" / "กลับภายในวัน" · "ค้างคืน" / "ได้ค่าเบี้ยเลี้ยง" · "ค้าง N คืน · ได้เบี้ยเลี้ยง P คืน × ฿150.00 = ฿X" · "ปรับจำนวนคืน" / "เสร็จ" · "คืนที่ค้าง" · "คืนที่ได้เบี้ยเลี้ยง" · "คืน" |
| hint คืน | "คิดจากวันที่ที่ใส่ให้อัตโนมัติ" · "ช่วงวันที่ค้างได้ N คืน" · "มากกว่าช่วงวันที่ (ค้างได้ N คืน) — ตรวจอีกครั้ง" · "ใส่วันที่ก่อน หรือปรับจำนวนคืน (อย่างน้อย 1 คืน)" · "คืนที่ได้เบี้ยเลี้ยงต้องไม่เกินคืนที่ค้าง" |
| error ในการ์ด | "เลือกวันที่และบอกว่าไปทำอะไร" · "เลือกวันที่ไป" · "บอกว่าไปทำอะไร ที่ไหน" · "วันที่กลับต้องไม่ก่อนวันที่ไป" · "ใส่เวลาให้ครบ" · "เวลาสิ้นสุดต้องหลังเวลาเริ่ม" · "วันที่ซ้อนกับช่วงที่ N" |
| สรุป | "สรุปคำขอ" · "ผู้ขอ" · "เรียน" · "ผู้บังคับบัญชา" · "ช่วงที่ไป" · "N ช่วง · M วัน" · "ยังไม่ได้เลือกวันที่" · "ลักษณะ" · "ค่าเบี้ยเลี้ยงรวม" · "ไม่มี" · "ผู้ขอและผู้บังคับบัญชาดึงจากระบบ" |
| ทำซ้ำ | "ทำซ้ำจาก {code} — ใส่วันที่ใหม่" |
| ขั้น 2 | "แนบเอกสารประกอบ (ถ้ามี)" · "เช่น หนังสือเชิญ กำหนดการ หรือใบมอบหมายงาน" · "คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)" / "แนบไฟล์เพิ่ม" · "PDF, Word, Excel หรือรูปภาพ ไม่เกิน 20 MB ต่อไฟล์" |
| ขั้น 3 | "ตรวจสอบและยืนยัน" · "ส่งแล้วแก้ไขไม่ได้ — ถ้าต้องเปลี่ยน ให้ยกเลิกแล้วทำซ้ำ" · "มี N ช่วงเป็นวันที่ผ่านมาแล้ว — ส่งเป็นคำขอย้อนหลัง" · "ข้อมูลคำขอ" · "วันที่ไปปฏิบัติงาน" · "ค่าเบี้ยเลี้ยง" · "เอกสารแนบ" · "ไม่มีเอกสารแนบ" |
| footer | "ย้อนกลับ" · "ยกเลิก" · "ถัดไป" · "บันทึกแบบร่าง" · "บันทึกและส่งขออนุญาต" · "กำลังบันทึก…" |
| view | "ข้อมูลเอกสาร" · "ผู้ขอ" · "รายการวันที่ปฏิบัติงาน (N)" · "รวม M วัน" · "ลักษณะการปฏิบัติงานและเบี้ยเลี้ยง" · "ไป-กลับ — ไม่มีค่าเบี้ยเลี้ยง" · "จำนวนคืนที่ค้าง" · "คืนที่ได้เบี้ยเลี้ยง" · "อัตราต่อคืน" · "เอกสารแนบ (N ไฟล์ · Document Center)" · "ข้อมูลระบบ" · "สร้างโดย" · "แก้ไขล่าสุด" · "อนุญาตแล้ว ล็อกแก้ไข" · "ปิด" |
| tabs | "รายละเอียด" · "PDF Preview" · "ลายเซ็น / อนุมัติ" · "ประวัติ" |
| pdf bar | "ตัวอย่าง PDF · A4 · แบบพิมพ์ FM-HRM-02 Rev. 00 · สร้างจากข้อมูลเอกสารนี้" · "ดาวน์โหลด PDF" · "พิมพ์" |
| sign tab | "สายอนุมัติ (DOA)" · "ขั้น n/N" · "ผู้ส่ง" · "ผลโดย" · "ลำดับการอนุมัติ" · "ส่งขออนุญาต" · "ยังไม่ส่ง" · "ขั้น N · {role}" · "ผลลัพธ์" · "อนุญาตให้ออกปฏิบัติงานนอกสถานที่" · "รอผล" · "ประวัติ (append-only)" |
| modal | "ส่งขออนุญาต?" · "ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร" · "เลือกผู้พิจารณา" · "อนุญาตให้ออกปฏิบัติงานนอกสถานที่?" · "ความเห็น" / placeholder "ไม่บังคับ" · "ไม่อนุญาตคำขอนี้?" · "ยกเลิกเอกสาร?" · "อนุญาตแล้ว — ยกเลิกแล้วใช้ต่อไม่ได้" · "เหตุผล" · placeholder "แจ้งผู้ขอว่าเพราะอะไร" / "เหตุผลที่ยกเลิก" · "กรุณาระบุเหตุผล" · "กรุณาเลือกผู้พิจารณา" · "ไม่ยกเลิก" · "ทิ้งข้อมูลที่กรอกไว้?" · "ข้อมูลในแบบฟอร์มนี้ยังไม่ได้บันทึก" · "กลับไปกรอกต่อ" · "ทิ้งข้อมูล" |
| chips | ไม่อนุญาต: "ไม่ใช่งานที่ได้รับมอบหมาย" · "ช่วงเวลาไม่เหมาะสม" · "ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม" — ยกเลิก: "งานเลื่อนหรือยกเลิก" · "เปลี่ยนผู้ไปปฏิบัติงาน" · "บันทึกผิด" |
| toast | "บันทึกร่างแล้ว · {code}" · "ส่งขออนุญาตแล้ว · {code}" · "อนุญาตแล้ว · {code}" · "ไม่อนุญาตแล้ว · {code}" · "ยกเลิกเอกสารแล้ว · {code}" · "กรุณากรอกข้อมูลให้ครบถ้วน" · "แก้ไขได้เฉพาะร่างของตัวเอง" · "แบบเอกสารนี้ยังไม่เปิดใช้งาน" · "ส่งออก N รายการ" · "กำลังเปิดหน้าต่างพิมพ์ · {code}" · "เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ · {code}" · "{ชื่อไฟล์} — ชนิดไฟล์ไม่รองรับ" · "{ชื่อไฟล์} — ไฟล์ใหญ่เกินกำหนด (สูงสุด 20 MB)" · "แนบไม่ได้ N ไฟล์ — ชนิดไฟล์ไม่รองรับหรือใหญ่เกิน 20 MB" · "แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง" · "ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง" · "ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่" · "คุณไม่มีสิทธิ์ทำรายการนี้" · "ไม่มีการแจ้งเตือนใหม่" · (prototype only) "สลับเป็น {ชื่อ}" |
| empty | "ยังไม่มีคำขอออกปฏิบัติงานนอกสถานที่" / "สร้างคำขอก่อนออกไปปฏิบัติงานนอกสถานที่ เพื่อให้ผู้บังคับบัญชาอนุญาต" / "สร้างคำขอ" · "ไม่พบรายการที่ค้นหา" / "ลองปรับคำค้นหรือล้างตัวกรอง" / "ล้างตัวกรอง" · เลือกผู้พิจารณาไม่พบ "ไม่พบรายการ" |
| lock | "แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างคำขอใหม่ไม่ได้" |
| audit act | "สร้างเอกสาร" · "แก้ไขร่าง" · "ส่งขออนุญาต" (note "ถึง {ชื่อ}") · "อนุญาต (ขั้น N)" · "อนุญาต" · "ไม่อนุญาต" · "ยกเลิกเอกสาร" |

## §10 Data Binding & BACKEND anchors
| Prototype (mock) | แทนด้วย (FRD) | หมายเหตุ |
|---|---|---|
| `EMP[]`, `empOf()`, `ME()` | API-12 form-context · F-EMP-001 / F-ORG-001 | ผู้ขอ/หัวหน้า |
| `POLICY.perDiem` (150) | API-12 `per_diem_rate` (ExpensePolicy) | ห้าม hardcode |
| `blankLine()` เวลา 08:30/17:30 | API-12 `default_time` | |
| `DOC.active` | API-12 `doc_type_active` (F-DOCCFG status) | |
| `RECS[]`, `listRows()`, `canSee()` | API-01 / API-02 (scope ฝั่ง server) | stats มาจาก API-01 `stats` |
| `persist()` (+ `SEQ` เลขรัน) | API-03 / API-04 (ENG-DOC-NUM) | |
| `validateMain()` | FN-03 (server) + ทำซ้ำฝั่ง client เพื่อ UX | ข้อความ §9 |
| `perDiem()` `maxNights()` `lineDays()` | FN-04 | |
| `MOCK_DOA_RESOLVED` / `resolveDoa()` (DOA-ENGINE-HOOK) | API-05 approval-preview | dynamic N ขั้น |
| `confirmSubmit()` | API-06 | |
| `confirmApprove()` / `confirmReason()` | API-07 / API-08 / API-09 | sequential |
| `oswPdfData()` + `tplRender(OSW_TPL)` | FN-11/12 · API-10 | template เดียวกัน · `DOC.form/rev` · `CO_LOGO` · `PDF_MIN_ROWS` → `print_config` + `header_snapshot` (DOCCFG_BRIEF v1.1) |
| `genPdf()` | API-10 `disposition=attachment` | ระบบจริงดาวน์โหลดไฟล์ |
| `exportCSV()` | API-11 | |
| `gateFiles()` + `pickFiles()` | Document Center upload + file_policy | |
| `commitRejected()` + `S.sim` | error mapping 409/403/5xx | prototype hook เท่านั้น |
| `switchPersona()` | — (ลบ) | prototype only |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/11 · BR-OSW-19 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/12 · BR-OSW-03..08 · VR-01..10 | `renderWizard()` `wizMain()` `tripCard()` |
| §4 P-03 | 01 P-03 · API-02/10 · BR-OSW-17 | `renderViewDrawer()` |
| §6 M-01 | 01 M-01 · API-05/06 · BR-OSW-09/11 | `renderModal` submit · `.slot-row` |
| §6 M-02/03 | 01 M-02/03 · API-07/08 · BR-OSW-10/12 | `confirmApprove` · `confirmReason` |
| §6 M-04 | 01 M-04 · API-09 · BR-OSW-12 | `openCancel` |
| §6 M-05 | 01 M-05 · EC-10 | discard |
| §8 | 05 §5.2 state machine | `DOC_ST` · `viewBanner` |
| §9 | 06 §6.10 · 05 §5.4 | strings |

**⚠️ Drift Log**
| # | ประเภท | รายการ | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only (prototype) | ตัวสลับผู้ใช้ `switchPersona` ใน user menu | ไม่สร้างในระบบจริง (FRD §0.3 Out of Scope) |
| D-02 | HTML-only (prototype) | `S.sim` จำลอง API ล้ม | ไม่สร้าง — ใช้ error จริง |
| D-03 | naming | prototype `pending` ↔ FRD `pending_approval` | ใช้ค่า FRD ใน API · label เหมือนกัน |
| D-04 | FRD-only | API-13 DOA callback · `osw_cancelled` event | ไม่มีบนจอ (backend) — ปกติ |
ไม่มี business drift

## §12 Diff จากเวอร์ชันก่อน
— ไม่ทำ (ไม่มี HTML เวอร์ชันก่อนแนบ) · สรุปรอบงานอยู่ใน PREFLIGHT ท้าย HTML

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่อง "เพื่อ" อาจเพิ่ม autocomplete จากใบเดิมของผู้ขอ (ไม่อยู่ในขอบเขตรอบนี้)
- `.pdf-slot` ระบบจริงใช้ `<embed>` PDF จาก API-10 แทน iframe HTML ได้ (หน้าตาเหมือนกันเพราะ template เดียวกัน)
