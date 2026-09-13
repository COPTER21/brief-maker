# Pattern F — Configurable Modifier (Toggle + Sub-Config Card)

> ⚠️ ถ้าใช้ใน context ของ **line editor** (PR/PO/QT/SO/เอกสารธุรกรรม) → **B2 เป็นเจ้าของ contract**
> ให้ตาม `B2_document-line-editor.md` แทนไฟล์นี้ — ไฟล์นี้ใช้กับ context อื่น (settings, master detail ฯลฯ)

> **Use for:** Settings/forms where a feature toggle reveals additional config when enabled.
> **Examples:** Withholding Tax toggle → reveals WHT rate config, Discount toggle → reveals discount amount/percent.
> **Source:** v25 lines 1674-1780 (refactored).

---

## 🎯 When to Use

✅ Boolean feature toggle that, when ON, requires more configuration
✅ Optional behaviors with parameters (apply discount, enable WHT, send notification)
✅ Settings page with nested options

❌ Always-required input (just use a field directly)
❌ Mutually exclusive options (use radio buttons or select)
❌ More than 5-6 sub-fields when enabled (move to separate page/drawer)

---

## 🏗️ Structure

```
.config-row (wrapper)
  ├─ .config-row-header (label + toggle)
  │   ├─ Label (with optional help icon)
  │   └─ .toggle (clickable wrapper)
  │       └─ .toggle-track > .toggle-thumb
  └─ .config-row-body (sub-config card, only when toggle ON)
      └─ form fields
```

---

## 📋 HTML Skeleton

```html
<!-- Withholding Tax Toggle Example -->
<div class="config-row" style="border: 1px solid var(--c-line-2); border-radius: 10px; 
                                background: #fff; margin-bottom: 12px; overflow: hidden;">

  <!-- HEADER (always visible) -->
  <div class="config-row-header" 
       style="padding: 14px 18px; display: flex; justify-content: space-between; 
              align-items: center; gap: 12px; cursor: pointer; user-select: none;"
       onclick="toggleConfig('wht'); render();">
    <div style="flex: 1;">
      <div style="font-size: 14px; font-weight: 600; color: var(--c-ink); display: flex; align-items: center; gap: 8px;">
        <span>หัก ณ ที่จ่าย (Withholding Tax)</span>
        <i data-lucide="info" class="w-3.5 h-3.5" style="color: var(--c-mute-2);" 
           title="ระบบจะคำนวณภาษีหัก ณ ที่จ่ายและบันทึกเป็นเอกสารแยก"></i>
      </div>
      <div style="font-size: 12px; color: var(--c-mute); margin-top: 3px;">
        ${state.config.wht.enabled ? `กำหนด ${state.config.wht.rate}% สำหรับ ${state.config.wht.category || 'ทุกประเภท'}` : 'ปิดอยู่ — ไม่มีการหัก ณ ที่จ่าย'}
      </div>
    </div>

    <!-- Toggle (full row clickable) — Iron Rule #20 -->
    <div class="toggle" style="flex-shrink: 0;">
      <div class="toggle-track ${state.config.wht.enabled ? 'is-on' : ''}">
        <div class="toggle-thumb"></div>
      </div>
    </div>
  </div>

  <!-- BODY (only visible when toggle ON) -->
  ${state.config.wht.enabled ? `
    <div class="config-row-body" 
         style="padding: 16px 18px; background: var(--c-bg-off); 
                border-top: 1px solid var(--c-line-2);">
      
      <div class="field-row">
        <div class="field">
          <label class="field-label">อัตรา (%) <span class="req">*</span></label>
          <select class="select field-input" onchange="state.config.wht.rate = this.value; render();">
            <option value="1" ${state.config.wht.rate === '1' ? 'selected' : ''}>1%</option>
            <option value="3" ${state.config.wht.rate === '3' ? 'selected' : ''}>3%</option>
            <option value="5" ${state.config.wht.rate === '5' ? 'selected' : ''}>5%</option>
            <option value="10" ${state.config.wht.rate === '10' ? 'selected' : ''}>10%</option>
          </select>
        </div>

        <div class="field">
          <label class="field-label">ประเภท</label>
          <select class="select field-input" onchange="state.config.wht.category = this.value; render();">
            <option value="">— ทุกประเภท —</option>
            <option value="service">บริการ</option>
            <option value="rental">ค่าเช่า</option>
            <option value="commission">ค่านายหน้า</option>
          </select>
        </div>
      </div>

      <div class="field" style="margin-bottom: 0;">
        <label class="field-label">หมายเหตุ</label>
        <input class="input field-input" type="text" placeholder="เช่น ใบหัก ณ ที่จ่าย ม.40(2)">
      </div>
    </div>
  ` : ''}
</div>
```

---

## 🎨 Toggle CSS (add to file-skeleton if not present)

```css
.toggle { cursor: pointer; user-select: none; }
.toggle-track {
  width: 38px; height: 22px;
  background: var(--c-line);
  border-radius: 999px;
  position: relative;
  transition: background 180ms;
}
.toggle-track.is-on { background: var(--c-primary); }
.toggle-thumb {
  position: absolute;
  top: 2px; left: 2px;
  width: 18px; height: 18px;
  background: #fff;
  border-radius: 50%;
  transition: transform 180ms cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}
.toggle-track.is-on .toggle-thumb { transform: translateX(16px); }
```

---

## 🔧 Required JS Helpers

```javascript
// State extension
// state.config = {
//   wht: { enabled: false, rate: '3', category: '' },
//   discount: { enabled: false, type: 'percent', value: 0 },
//   notify: { enabled: true, channel: 'email' },
//   ...
// }

function toggleConfig(key) {
  if (!state.config[key]) state.config[key] = { enabled: false };
  state.config[key].enabled = !state.config[key].enabled;
}
```

---

## 🎯 Multi-Modifier Example (Discount + WHT + Notify)

```html
<div class="card">
  <div style="padding: 18px;">
    <h3 class="drawer-section-title">ตัวเลือกเพิ่มเติม</h3>
    
    ${renderConfigRow('discount', 'ส่วนลด', 'apply discount on this transaction', renderDiscountConfig())}
    ${renderConfigRow('wht', 'หัก ณ ที่จ่าย', 'Withholding tax', renderWhtConfig())}
    ${renderConfigRow('notify', 'แจ้งเตือนลูกค้า', 'Send email/SMS notification', renderNotifyConfig())}
  </div>
</div>
```

---

## 🛡️ Iron Rules to Enforce

- **#17** Responsive form grid (`.field-row` with auto-fit) ✓
- **#18** Form field structure (label / input / help / error) ✓
- **#19** Hide number input spinner ✓
- **#20** Toggle pattern: `<div onclick>` + transform translateX (NOT `<label><input>`) ✓
- **#21** All `<i data-lucide>` have `w-{N} h-{N}` ✓
- **#23** No color emoji ✓

---

## ⚠️ Common Mistakes

1. **❌** Using `<input type="checkbox">` for toggle — causes browser inconsistencies (Iron Rule #20)
2. **❌** Toggle thumb not animating when toggled — must use `transform: translateX()`, not `left` change
3. **❌** Sub-config visible even when toggle OFF — use conditional render `${state.config.X.enabled ? ... : ''}`
4. **❌** Validation passing when required sub-field empty AND toggle ON — must validate sub-fields conditionally
5. **❌** Only the toggle is clickable (small target) — make the **whole header row** clickable
6. **❌** Sub-config body has same bg as header (no visual separation) — use `var(--c-bg-off)` + border-top
7. **❌** Toggle without label or with unclear label — always include description text
8. **❌** Multiple modifier rows without spacing — add `margin-bottom: 12px` between rows

---

## 🎯 Variants

### Variant A: Compact (one-line per modifier)

For settings page with many simple toggles:

```html
<div style="padding: 12px 18px; border-bottom: 1px solid var(--c-line-2); 
            display: flex; justify-content: space-between; align-items: center;"
     onclick="toggleConfig('notify'); render();">
  <div>
    <div style="font-size: 13.5px; font-weight: 500;">แจ้งเตือน Email</div>
    <div style="font-size: 12px; color: var(--c-mute);">ส่งสรุปทุกวัน 09:00</div>
  </div>
  <div class="toggle">
    <div class="toggle-track ${state.config.notify.enabled ? 'is-on' : ''}">
      <div class="toggle-thumb"></div>
    </div>
  </div>
</div>
```

### Variant B: Card-style (heavy config with multiple fields)

Already shown above — used for WHT, Discount, etc.

### Variant C: Inline (single sub-field)

```html
<div style="display: flex; align-items: center; gap: 12px;">
  <div class="toggle" onclick="toggleConfig('discount'); render();">
    <div class="toggle-track ${state.config.discount.enabled ? 'is-on' : ''}">
      <div class="toggle-thumb"></div>
    </div>
  </div>
  <span>ส่วนลด</span>
  ${state.config.discount.enabled ? `
    <input class="input" type="number" style="width: 100px;" placeholder="%">
    <span>%</span>
  ` : ''}
</div>
```
