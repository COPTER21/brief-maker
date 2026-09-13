# Pattern K — Informative Report (Screen + Print)

> ใช้กับ: WF-04 Informative Report Suggestion/production — รายงานที่ผู้ใช้เปิดดู + สั่งพิมพ์/PDF ได้
> Anchor: design-system.html `#/table-rpt` (Standard / Grouped / Pivot) + `#/mixed` (Exec/Ops) + Pattern H (A4)
> ต่างจาก Pattern A (list view): report = อ่าน/พิมพ์ ไม่มี CRUD — ไม่มีปุ่มสร้าง, ไม่มี row action, ไม่มี checkbox

---

## เลือก Variant

| Variant | ใช้เมื่อ |
|---|---|
| **K1 Standard Table** | รายงานแถวเรียบ (รายการขาย, สต๊อกคงเหลือ) |
| **K2 Grouped** | จัดกลุ่ม + subtotal ต่อกลุ่ม (ยอดขายรายลูกค้า/เดือน) |
| **K3 Summary + Detail** | บล็อกสรุปบน (ตัวเลขรวม) + ตารางรายละเอียดล่าง |

## โครงหน้า

```html
<div class="ph">
  <div class="ph-title-row"><h1 class="ph-title">[ชื่อรายงาน]</h1></div>
  <p class="ph-sub">ข้อมูล ณ [fmtDateTime] · เงื่อนไข: [สรุป filter ที่เลือก]</p>
  <div class="ph-actions">
    <button class="btn btn-secondary"><i data-lucide="download" class="w-4 h-4"></i><span>Export CSV</span></button>
    <button class="btn btn-secondary" onclick="window.print()"><i data-lucide="printer" class="w-4 h-4"></i><span>พิมพ์</span></button>
  </div>
</div>
<div class="card">
  <div class="filter-bar"><!-- เงื่อนไขรายงาน: ช่วงวันที่ (จำเป็น) + มิติหลัก + ปุ่ม "แสดงรายงาน" btn-primary ขวาสุดของ filter bar (ข้อยกเว้น Rule 46.1 — report ไม่มีปุ่มสร้าง, ปุ่ม run อยู่กับเงื่อนไข) --></div>
  <div class="table-scroll is-sticky"><table class="rpt">…</table></div>
  <div class="table-footer"><!-- รวมทั้งสิ้น + จำนวนรายการ --></div>
</div>
```

## กติกาตารางรายงาน

- คอลัมน์ตัวเลข = `.num` + `col-num` ชิดขวา, ใช้ `fmtNumber/fmtMoney` (Rule #43)
- **แถวรวม (grand total):** `tfoot` bg `--c-bg-off`, ตัวหนา, เส้นบน 2px `--c-line`
- **K2 กลุ่ม:** แถวหัวกลุ่ม bg `--c-line-3` ตัวหนา + แถว subtotal ท้ายกลุ่ม (`รวม [ชื่อกลุ่ม]` ชิดขวา)
- คอลัมน์เกิน 8 ได้ (ข้อยกเว้น Rule #16 — report อ่านแนวนอน) แต่ต้องอยู่ใน `.table-scroll`
- ไม่มีข้อมูล → empty state "ไม่พบข้อมูลตามเงื่อนไข ลองปรับช่วงวันที่" (Rule #39)

## Print CSS (บังคับ)

```css
@media print {
  .sidebar, .shell-bar, .filter-bar, .ph-actions, .table-footer .pager { display:none !important; }
  .content { margin-left:0 !important; padding:0 !important; }
  body { min-width:0 !important; background:#fff; }
  .card { border:none; box-shadow:none; }
  .rpt th { background:#F1EEEA !important; -webkit-print-color-adjust:exact; }
  .rpt tr { break-inside: avoid; }
  .print-header { display:block !important; }  /* หัวกระดาษ: โลโก้+ชื่อรายงาน+เงื่อนไข+วันที่พิมพ์ */
}
.print-header { display:none; }
```

- หัวกระดาษพิมพ์ (`.print-header`): ชื่อบริษัท + ชื่อรายงาน + เงื่อนไข + "พิมพ์เมื่อ [fmtDateTime]"
- รายงานทางการ A4 (มีลายเซ็น/แบบฟอร์ม) → ใช้ Pattern H แทน

## Verification เฉพาะ pattern นี้
- [ ] ไม่มีปุ่มสร้าง / checkbox / row action ใด ๆ
- [ ] ตัวเลขทุกคอลัมน์ชิดขวา `.num` + format กลาง
- [ ] แถวรวม/subtotal ครบตาม variant
- [ ] `window.print()` แล้ว sidebar/shell/filter หาย + หัวกระดาษโผล่ (render-check ด้วย media print ถ้าทำได้)
- [ ] ph-sub แสดง "ข้อมูล ณ + เงื่อนไข" เสมอ
