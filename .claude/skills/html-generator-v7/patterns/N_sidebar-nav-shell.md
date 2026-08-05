# Pattern N — Sidebar Navigation Shell (3-Level Accordion + Icon Rail + Slide Panel)

> **ใช้เมื่อ:** ระบบมีเมนู ≥ 2 ระดับ (Module › Group › Feature) หรือ user สั่ง "เมนูแบบ Core Shell",
> "sidebar 3 ระดับ", "เมนูย่อได้", "icon rail", "เมนูแบบ design system"
> **Reference (source of truth — copy structure/JS verbatim):** `references/sidebar-shell/core-shell-ultimate.html`
> **CI:** v2.0 Warm Light — sidebar/panel flat Charcoal `#111111`, active = Red `#FF3B30`, ไอคอนโมดูลที่มี active = Orange Light `#FFB763`
> **ที่มา:** UI_REVISION_BRIEF core-shell-sidebar (2026-07-09) — ผ่าน Playwright DOM assertions 35 เคส + audit.sh FAIL=0 แล้ว

---

## 1. โครงเมนู (Menu Model) — สูงสุด 3 ระดับ ห้ามเพิ่มระดับที่ 4

```
Module (L1)  ─── data-module      ← toggle เท่านั้น ไม่ navigate
 ├─ Feature (L2) ─── data-feature ← navigate #/{id}
 └─ Group (L2)  ─── data-group    ← toggle เท่านั้น ไม่ navigate
     └─ Feature (L3) ─── data-feature
```

| Node | Element | คลิกแล้ว |
|---|---|---|
| Module / Group | `<button aria-expanded>` | **toggle เท่านั้น — ห้าม navigate** |
| Feature | `<a data-feature>` | navigate → `#/{feature_id}` |

> ⛔ **กติกาเหล็ก:** หัวโมดูล/หัวกลุ่มคลิกแล้วห้ามเปลี่ยนหน้า — ถ้าทั้งกางทั้ง navigate ผู้ใช้จะหลุดหน้าโดยไม่ตั้งใจทุกครั้งที่แค่อยากเปิดดู

### MENU data shape (mock ใน prototype / `/api/menu` ใน production)

```jsonc
[
  { "id": "opproc", "label": "Operation Process", "icon": "git-branch",
    "children": [
      { "id": "op-all", "label": "งานทั้งหมด", "icon": "layers" },
      { "id": "op-manage", "label": "จัดการ", "icon": "folder-cog", "group": true,
        "children": [ { "id": "op-cl", "label": "CL Template", "icon": "workflow" } ] }
    ] }
]
```
- `group: true` = กลุ่ม (toggle) · ไม่มี = feature (navigate)
- Permission filtering ทำที่ backend — frontend วาดเฉพาะที่ได้รับมา (กลุ่ม/โมดูลที่ children ว่าง = ไม่ส่งมา)

---

## 2. สองโหมด (Modes)

| | โหมดกางเต็ม (default) | โหมดไอคอน |
|---|---|---|
| Width | `244px` (`--sidebar-w`) | `58px` (`--rail-w`) |
| Trigger | — | `body.icon-mode` |
| เนื้อหา | ครบ 3 ระดับ (accordion) | ไอคอนโมดูล → คลิกเปิด slide panel แสดง L2+L3 |
| Transition | `width 260ms var(--ease)` — `.main` ต้อง transition margin-left ด้วย duration เดียวกัน |

- **ค่าเริ่มต้น = กางเต็มเสมอ** (NN/g: การซ่อน nav หลังไอคอนทำให้ทำงานช้าลง — การย่อเป็นสิทธิ์ผู้ใช้ ห้ามตั้ง default)
- สลับด้วยปุ่ม toggle ท้ายแถว brand (ไอคอน `panel-left-close` ↔ `panel-left-open`, 30px) **หรือ** `Ctrl/⌘+B`
- ไอคอน→กาง: auto-กางโมดูล+กลุ่มของหน้าปัจจุบัน · กาง→ไอคอน: ปิด panel ที่ค้าง

## 3. Visual Hierarchy — แยกชั้นด้วย "ความลึก" ไม่ใช่สี

| ระดับ | Class | ทรีตเมนต์ (CI ใหม่) |
|---|---|---|
| Caption | `.sb-cap` | `10px/700` uppercase tracking `.1em` สี `#85878D` |
| L1 Module หัว | `.mod-h` | `13px/500` · กางอยู่ → `.mod[data-open=true]` พื้น `rgba(0,0,0,.20)` (inset well) · chevron หมุน `-90deg` เมื่อพับ |
| L1 มี active ข้างใน | `.mod.has-active` | ไอคอนโมดูล = `--c-teal-light` (**Orange Light `#FFB763`**) |
| L2 Feature | `.item` | `12.5px` · **active = พื้น `--c-primary` (Red `#FF3B30`) + ขีดขาวซ้าย 3px + shadow** |
| L2 Group หัว | `.grp-h` | `12px/600` · กางอยู่ → พื้น `rgba(0,0,0,.16)` (จมลึกกว่าโมดูลอีกชั้น) |
| L3 Sub-feature | `.sub` ใน `.subs` | เยื้อง `margin-left:20px` + เส้นรางแนวตั้ง `border-left: 1px solid var(--rail)` + ขีดสั้น `::before` ต่อรายการ |

```css
--rail: rgba(255,255,255,.12);
.subs { margin-left: 20px; padding-left: 10px; border-left: 1px solid var(--rail); }
.sub::before { content:''; position:absolute; left:-10px; top:50%; width:6px; height:1px; background: var(--rail); }
```

> **สี Red `#FF3B30` สงวนไว้ให้สถานะ active เพียงอย่างเดียว** — ห้ามใช้บอกลำดับชั้น
> (ถ้าใช้ทั้งสองอย่าง ผู้ใช้แยกไม่ออกว่าแดงแปลว่า "อยู่ตรงนี้" หรือ "ระดับนี้")

## 4. Slide Panel (เฉพาะโหมดไอคอน)

| | ค่า |
|---|---|
| ตำแหน่ง/ขนาด | `position:fixed; top:0; bottom:0; left:58px; width:216px` |
| Background | `#111111` (charcoal เดียวกับ sidebar — **ห้ามใช้การ์ดขาว** จะตัดอารมณ์ chrome) |
| Shadow | `12px 0 32px rgba(17,17,17,.34)` |
| เข้า/ออก | `transform: translateX(-102%)→0` + opacity `260ms` |
| **z-index** | scrim `30` < panel `34` < **sidebar `35`** ← ต้องเรียงแบบนี้ ไม่งั้นกดไอคอนเดิมซ้ำเพื่อปิดไม่ได้ (บั๊กที่เจอจริง) |
| โครง | `slide-head` (kicker "MODULE" + ชื่อ) → `slide-nav` (ใช้ `.item/.grp/.sub` ชุดเดียวกับโหมดกาง) → `slide-hint` → `slide-foot` |

## 5. Behavior Contracts

**โหมดกาง:** คลิกหัวโมดูล/กลุ่ม = toggle (กางหลายโมดูลพร้อมกันได้) · คลิก feature = navigate · **โมดูล/กลุ่มที่มี active อยู่ข้างในต้องพับได้ ห้ามเด้งกลับ**

> ⚠️ จุดพลาดอันดับ 1: ถ้า `render()` เรียก auto-expand ทุกครั้ง ผู้ใช้จะพับไม่ลง —
> `revealActive()` เรียกได้ **แค่ 3 จังหวะ**: โหลดครั้งแรก · เปลี่ยน route · สลับโหมดกลับมากาง

**โหมดไอคอน:** คลิกไอคอน = เปิด panel (stagger fade-in `delay index×24ms`) · คลิกไอคอน**เดิม**ซ้ำ = ปิด (รวมโมดูล active) · คลิกไอคอนอื่น = สลับ · คลิก scrim = ปิด · `Esc` = ปิด + **คืน focus ที่ไอคอนเดิม** · `↑↓` เลื่อน cursor (วนรอบ) · `Enter` เปิด · hover/focus ไอคอน = tooltip หลัง **240ms**

**Animation:** `.anim` ใส่ให้ `slide-nav` **เฉพาะตอนเปิด panel/สลับโมดูล** — กาง/พับกลุ่มใน panel **ห้าม re-animate รายการอื่น** + คง `scrollTop` · บังคับมี `prefers-reduced-motion: reduce → duration 1ms`

## 6. Accessibility Contract (บังคับ)

- หัวโมดูล/กลุ่ม = `<button aria-expanded>` (ไม่ใช่ div onclick) · toggle โหมด = `aria-pressed`
- ไอคอนโมดูล (โหมดไอคอน) = `aria-haspopup="menu"` + `aria-label` + `title`
- panel = `role="menu"`, รายการ = `role="menuitem" tabindex="-1"`
- เปิด panel ด้วย**คลิก** ไม่ใช่ hover (WCAG 3.2.1) · Esc ปิดได้ (1.4.13) · คืน focus (2.4.3)
- `:focus-visible { outline: 2px solid var(--c-primary); outline-offset: 2px; }` (2.4.7)

## 7. Tokens เพิ่มของ pattern นี้ (นอกเหนือจาก ci-tokens กลาง)

```css
--sidebar-w: 244px;  --rail-w: 58px;
--nav-l1: 13px;  --nav-l2: 12.5px;  --nav-l3: 12px;  --nav-cap: 10px;
--ease: cubic-bezier(.4, 0, .2, 1);
--rail: rgba(255,255,255,.12);
```
> Pattern N ใช้ `--sidebar-w: 244px` (กว้างกว่า shell พื้นฐาน 232px เพราะรองรับ 3 ระดับ) — เมื่อใช้ pattern นี้ให้ยึด 244px ทั้งไฟล์

## 8. ⌘K Command Palette (มีใน reference — ใช้เมื่อระบบไม่มี global search เดิม)

ค้นข้ามทุกโมดูลถึง L3 พร้อมแสดง path (Module › Group › Feature) · เปิด `Ctrl/⌘+K` · ถ้าระบบมี global search อยู่แล้ว **อย่าซ้อน** — ตัดส่วนนี้ออก

## 9. Generation Checklist

- [ ] Copy โครง HTML/CSS/JS จาก `references/sidebar-shell/core-shell-ultimate.html` — แก้เฉพาะ `MENU` array + branding text
- [ ] หัวโมดูล/กลุ่มไม่ navigate · feature navigate + hash routing refresh-safe · deep-link แล้วเมนูกางถึง active เอง
- [ ] Active พับได้ · `revealActive()` 3 จังหวะเท่านั้น
- [ ] z-index: scrim 30 / panel 34 / sidebar 35
- [ ] `.anim` เฉพาะตอนเปิด panel · `prefers-reduced-motion` มีผล
- [ ] a11y ครบตาม §6 · tooltip 240ms
- [ ] Scrollbar ตาม Iron Rule #49 (บาง 5px ขาวโปร่งบนพื้นเข้ม — ห้าม default)
- [ ] ไม่มี `localStorage` · ไม่มีสีนอก token · Lucide ตาม Rule #25
