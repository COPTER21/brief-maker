# CHANGELOG — html-generator v9.1 (2026-09-16)

จาก vibe จริงของ **Tenant Master (F-TM-01)** และ **Plan & Package (F-TM-02)** — ปัญหาที่ user เจอ: ฟอร์ม "โล่ง ๆ ห่าง ๆ" · list ซ้อนบรรทัด · checkbox label เละ · placeholder เข้มเกิน · tooltip ล้นขอบ · dropdown ค้างเปิด · z-index kit ไม่ได้ประกาศ

## เพิ่ม
| สิ่งที่เพิ่ม | ที่อยู่ |
|---|---|
| **Iron Rule #104 Compact Form Spacing + Placeholder + Checkbox Label** (แทน #43 การจองพื้นที่ error) | `knowledge/iron-rules.md` Group 22 |
| **Iron Rule #105 Lean Cell — 1 เซลล์ = 1 บรรทัด** (ขยาย #103A) | `knowledge/iron-rules.md` Group 22 |
| token `--c-placeholder: #B4B6BC` + `::placeholder` rule | `templates/file-skeleton.template.html` `:root` |
| **Z-Index Registry** `--z-content/sticky/shell/dropdown/backdrop/drawer/modal/toast` ประกาศใน `:root` + `.modal-backdrop/#drawer/#toast` ผูก var | skeleton (defect: v9.0 อ้าง var ที่ไม่มี) |
| `label.chk` + `.chk input[type=checkbox]` · `.table td.nw` · `.info-tip.is-below` · `.drawer .info-tip::after{left:0}` | skeleton CSS |
| `ssPick` blur input ก่อน `onSelect` | skeleton JS (search-select) |

## เปลี่ยน (BREAKING — ค่า kit)
- `.form-section` margin-top 28 → **16** · `.field` margin-bottom 16 → **12** · `.field-label` margin-bottom 6 → **4**
- `.field-error` จาก `visibility:hidden` (จอง 15px) → **`display:none`** โผล่เฉพาะ `.field.is-invalid` / `.is-show`
- `.ph > div:first-child` flex `1 1 auto` → **`1 1 0`**

## ผลกับไฟล์เดิม (gen จาก v9.0)
- แนะนำเพิ่ม z-index registry ใน feature-css ของไฟล์เก่า (ไม่งั้น overlay พึ่ง DOM order)
- ฟอร์มเก่าจะแน่นขึ้นเองเมื่อ re-gen · ตรวจ list ว่าไม่มี user-cell 2 บรรทัด (#105)
