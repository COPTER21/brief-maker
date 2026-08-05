# UI Audit Report

- Target: `C:\Users\Admin\Desktop\Work\brief-maker\outputs\10_Tax-Code\01_HTML\TaxCode.html`
- Status: **FAIL**
- Viewports: 1280, 1440, 1920, 2560
- Browsers: chromium
- Errors: 4
- Warnings: 0
- Behavior checks: 17/17
- Stable screenshot pairs: 27/28
- Internal runtime events: 0
- External runtime events: 66

## Findings

### 1. [ERROR] Accessibility — text contrast ต่ำกว่า WCAG AA

- Scene: `chromium-1280-01-vat-list` · chromium 1280px
- Selector: `div.sb-module:nth-of-type(2) > div.sb-features > a.sb-item.is-active:nth-of-type(1) > span`
- Measured: `{"ratio": 3.55, "fontSizePx": 13, "fontWeight": "600", "foreground": "rgb(255, 255, 255)", "background": "rgb(255, 59, 48)"}`
- Expected: `{"ratio": ">=4.5"}`

### 2. [ERROR] Accessibility — text contrast ต่ำกว่า WCAG AA

- Scene: `chromium-1280-01-vat-list` · chromium 1280px
- Selector: `div.ph:nth-of-type(1) > div.ph-actions:nth-of-type(2) > button.btn.btn-primary:nth-of-type(2) > span`
- Measured: `{"ratio": 1.06, "fontSizePx": 13, "fontWeight": "500", "foreground": "rgb(255, 255, 255)", "background": "rgb(250, 248, 245)"}`
- Expected: `{"ratio": ">=4.5"}`

### 3. [ERROR] Accessibility — text contrast ต่ำกว่า WCAG AA

- Scene: `chromium-1280-06-create-vat` · chromium 1280px
- Selector: `div.dw-footer:nth-of-type(3) > div.dw-footer-right > button.btn.btn-primary:nth-of-type(2) > span`
- Measured: `{"ratio": 1.06, "fontSizePx": 13, "fontWeight": "500", "foreground": "rgb(255, 255, 255)", "background": "rgb(250, 248, 245)"}`
- Expected: `{"ratio": ">=4.5"}`

### 4. [ERROR] Visual stability — ภาพสอง pass ไม่เหมือนกันทุกไบต์

- Scene: `chromium-1280-01-vat-list` · chromium 1280px
- Selector: `-`
- Measured: `{"browser": "chromium", "width": 1280, "scene": "chromium-1280-01-vat-list", "identical": false, "sha256_pass_1": "dc1029f06c4b8675095a08501872eeae907d69fafc397f04a1c6faba719a2c90", "sha256_pass_2": "b5572d2ab60bf81fb42f262a9e041f53007ab57bd7c5b5aa7acfb82a84aeab81", "bytes_pass_1": 74312, "bytes_pass_2": 74315}`
- Expected: `"identical SHA-256"`

## Manual review still required

- ความสวยงามและจังหวะการจัดวางโดยรวม
- ลำดับงานและ microcopy เข้าใจง่ายสำหรับผู้ใช้จริงหรือไม่
- ประสบการณ์ screen reader เชิงความหมาย
- native browser tooltip ซึ่ง Playwright วัดกล่องภายในไม่ได้
