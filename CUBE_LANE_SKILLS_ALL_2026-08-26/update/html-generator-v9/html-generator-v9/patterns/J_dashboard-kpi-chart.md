# Pattern J — Dashboard (KPI + Chart)

> ใช้กับ: WF-06 Dashboard Suggestion/production, หน้า monitoring, executive view
> Anchor: design-system.html `#/dashboard` (KPI Heavy / Chart Heavy / Mixed Compact) + `#/kpi` + `#/chart`
> **Chart = inline SVG vanilla เท่านั้น** — ห้ามเพิ่ม Chart.js/D3/CDN ใหม่ (skill นี้ self-contained)

---

## เลือก Variant

| Variant | ใช้เมื่อ | โครง |
|---|---|---|
| **J1 KPI Heavy** | เน้นตัวเลขสรุป | stats row (4-6 cards) → ตาราง/รายการล่าสุด |
| **J2 Chart Heavy** | เน้นแนวโน้ม | stats row (3-4) → chart grid 2 คอลัมน์ → ตาราง |
| **J3 Mixed Compact** | executive รวมทุกอย่าง | stats → chart 1 ใหญ่ + side list → ตารางสรุป |

## โครงหน้า (ทุก variant)

```html
<div class="ph">
  <div class="ph-title-row"><h1 class="ph-title">Dashboard [ชื่อ]</h1></div>
  <p class="ph-sub">[คำอธิบาย]</p>
  <div class="ph-actions">
    <!-- filter ช่วงเวลา = ขวาสุดของ ph-actions (dashboard ไม่มีปุ่มสร้าง) -->
    <div class="seg-control"><!-- 7 วัน | 30 วัน | ไตรมาส | ปี --></div>
    <button class="btn btn-secondary"><i data-lucide="download" class="w-4 h-4"></i><span>Export CSV</span></button>
  </div>
</div>
<div class="stats"><!-- stat cards ตาม catalog #6 --></div>
<div class="dash-grid"><!-- chart cards --></div>
<div class="card"><!-- ตารางรายการล่าสุด (Pattern A แบบย่อ — ไม่มี filter bar, ≤6 cols, 5-10 แถว + ลิงก์ "ดูทั้งหมด") --></div>
```

```css
.dash-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(380px,1fr)); gap: var(--sp-lg); margin-bottom: var(--sp-lg); }
.chart-card { /* = .card + padding var(--sp-lg) */ }
.chart-head { display:flex; align-items:center; justify-content:space-between; margin-bottom: var(--sp-md); }
.chart-title { font-size: var(--fs-h3); font-weight:600; color: var(--c-ink); }
```

## Chart มาตรฐาน (SVG vanilla — helper แนะนำ)

รองรับ 4 ชนิด: **bar / line / area / donut** — เขียนเป็น JS function คืน SVG string:

```js
function gridLinesSVG(w,h,max){   // เส้น grid แนวนอน 4 เส้น + label แกน Y
  return [0,0.25,0.5,0.75,1].map(t=>{
    const y = h-32 - t*(h-56);
    return `<line x1="40" y1="${y}" x2="${w-8}" y2="${y}" stroke="var(--c-line-3)" stroke-width="1"></line>
            <text x="34" y="${y+4}" text-anchor="end" font-size="10" fill="var(--c-mute-3)">${fmtNumber(Math.round(max*t))}</text>`;
  }).join('');
}
function barChartSVG(data, {w=560,h=220,color='var(--c-primary)'}={}){
  const max = Math.max(...data.map(d=>d.v)) || 1;
  const bw = (w-40)/data.length;
  const bars = data.map((d,i)=>{
    const bh = Math.round((d.v/max)*(h-56));
    return `<g>
      <rect x="${40+i*bw+bw*0.18}" y="${h-32-bh}" width="${bw*0.64}" height="${bh}" rx="4" fill="${color}" opacity="0.9"></rect>
      <text x="${40+i*bw+bw/2}" y="${h-12}" text-anchor="middle" font-size="11" fill="var(--c-mute-2)">${d.label}</text>
    </g>`;}).join('');
  return `<svg viewBox="0 0 ${w} ${h}" style="width:100%;height:auto">${gridLinesSVG(w,h,max)}${bars}</svg>`;
}
```

กติกา chart:
- สีซีรีส์: series 1 = `--c-primary`, series 2 = `--c-teal`, series 3 = `--c-warning` — ห้ามสีอื่น
- Grid line = `--c-line-3`, แกน label = `--fs-cap` สี `--c-mute-2`
- ตัวเลขบน tooltip/label ใช้ `fmtNumber` + `.num`
- Donut: ใช้ stroke-dasharray บน circle, ค่ากลาง = ตัวเลขรวม (`--fs-kpi`)
- ทุก chart มี empty state (Rule #39) เมื่อ data ว่าง
- Legend: จุดสี 8px + label `--fs-meta` ใต้ chart-head ขวา

## Verification เฉพาะ pattern นี้
- [ ] จำนวน stat cards ≤6 (Rule #8)
- [ ] chart ใช้ SVG inline — grep ไม่เจอ CDN chart lib
- [ ] สีซีรีส์ตามลำดับ primary→teal→warning
- [ ] seg-control เปลี่ยนช่วงเวลาแล้ว chart+stats อัพเดตจริง (mock)
- [ ] ตารางล่างสุดกดแถวเปิด view ได้ (Rule #41)
