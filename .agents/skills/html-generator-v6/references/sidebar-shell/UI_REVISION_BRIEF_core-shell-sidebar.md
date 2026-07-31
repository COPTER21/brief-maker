> ⚠️ **หมายเหตุ v4.2:** เอกสารนี้คือ brief ต้นฉบับ (เขียนสมัย CI เก่า CUBE NATIVE) เก็บไว้เป็น design rationale
> สีที่อ้างในเอกสาร (`#0B1D3A`, `#0B5CFF`, `#00A88E`, `#5EEAD4`, Inter) ถูกแทนที่ด้วย CI ใหม่แล้วใน
> `core-shell-ultimate.html` (ไฟล์ข้างกัน) และ `patterns/N_sidebar-nav-shell.md` — **เวลา generate ให้ยึด Pattern N + reference HTML เท่านั้น**
> Mapping: Navy→Charcoal `#111111` · Blue active→Red `#FF3B30` · Teal-light→Orange Light `#FFB763` · Inter→Satoshi

# UI Revision Brief — Core Shell Sidebar (เมนูฝั่งซ้าย)

> เอกสารคู่ HTML สำหรับส่ง Dev ใช้ implement เมนูซ้ายของ Core Cube ในระบบเดิม
> ไฟล์อ้างอิง: `core-shell-ultimate.html`
> อ้างอิงมาตรฐาน: `html-generator-v6` (CI CUBE NATIVE)
> สร้างเมื่อ: 9 กรกฎาคม 2569

---

## 1. สรุปภาพรวม (Executive Summary)

**Scope:** Sidebar navigation ของ Core Cube เท่านั้น — **ไม่รวมเนื้อหาหน้า feature**
**Type:** Refactor (ปรับโครงเมนูเดิม ไม่ใช่ feature ใหม่)
**Effort (rough):** S — 2-4 วัน (ถ้า extract เป็น shared component ตัวเดียว)
**Stack ใน reference:** HTML + vanilla JS + CSS ล้วน (ไม่มี Tailwind/CDN นอกจาก Google Fonts + Lucide)

เมนูเดิมมี 3 ระดับ แต่ **แยกชั้นไม่ออก** เพราะทั้ง L2 และ L3 ใช้พื้นหลังโทนใกล้กัน ผู้ใช้อ่านไม่ออกว่าอะไรเป็นลูกของอะไร

Shell นี้แก้ที่โครง ไม่ใช่ที่สี — **ยังคง 3 ระดับเท่าเดิม** (Module › Group › Feature) แต่แยกชั้นด้วย *ความลึกของพื้นผิว* (inset well + เส้นราง + ระยะเยื้อง) และสงวนสีน้ำเงิน `#0B5CFF` ไว้ให้ **สถานะ active อย่างเดียว** ห้ามใช้บอกลำดับชั้น

เพิ่ม **2 โหมด** ที่สลับกันได้:
- **โหมดกางเต็ม (244px)** — เห็นครบ 3 ระดับในแถบเดียว (accordion)
- **โหมดไอคอน (58px)** — เหลือไอคอนโมดูล กดแล้วมี panel navy สไลด์ออกมาแสดง L2+L3

**ไฟล์ที่ส่งมาด้วย**
- `core-shell-ultimate.html` — reference เปิดใน browser เล่นได้เลย (พื้นที่ตรงกลางเป็น placeholder เขียนว่า "Feature Section" — จงใจ เพราะอยู่นอก scope)
- `UI_REVISION_BRIEF_core-shell-sidebar.md` — เอกสารนี้

**สิ่งที่ Dev ต้องทำ**
1. Extract sidebar + slide panel + command palette เป็น shared component ตัวเดียว (`<AppSidebar />`) ใช้ร่วมทุกหน้าของ Core
2. เปลี่ยน `MENU` array (hardcode ใน reference) → ดึงจาก `GET /api/menu` ต่อ tenant
3. Wire `data-module` / `data-group` / `data-feature` เข้ากับ permission gating ของ Policy Center
4. เก็บ "โหมดเมนูล่าสุด" ลง user preference ฝั่ง server (ดู §9 OQ-01)

---

## 2. โครงเมนู (Menu Model)

3 ระดับ — nesting ลึกสุดที่รองรับคือระดับนี้ ห้ามเพิ่มระดับที่ 4

```
Module (L1)  ─── data-module
 ├─ Feature (L2)                     ─── data-feature   ← ลูกตรง ไม่มีกลุ่ม
 └─ Group (L2)  ─── data-group                          ← เช่น "จัดการ"
     └─ Feature (L3)  ─── data-feature
```

**ข้อมูลจริงใน reference:** 16 โมดูล · 4 กลุ่ม · 44 feature

| Node | เป็น | คลิกแล้ว |
|---|---|---|
| Module | `<button aria-expanded>` | toggle เท่านั้น — **ไม่ navigate** |
| Group | `<button aria-expanded>` | toggle เท่านั้น — **ไม่ navigate** |
| Feature | `<a data-feature>` | navigate → `#/{feature_id}` |

> **กติกาสำคัญ:** หัวโมดูลและหัวกลุ่มห้าม navigate เด็ดขาด ถ้าคลิกแล้วทั้งกางและเปลี่ยนหน้า ผู้ใช้จะเปลี่ยนหน้าโดยไม่ตั้งใจทุกครั้งที่แค่อยากดูว่าข้างในมีอะไร

### Shape ที่ API ต้องคืน

```jsonc
[
  {
    "id": "opproc",                    // → data-module
    "label": "Operation Process",
    "icon": "git-branch",              // ชื่อไอคอน Lucide
    "children": [
      { "id": "op-all", "label": "งานทั้งหมด", "icon": "layers" },
      {
        "id": "op-manage",             // → data-group
        "label": "จัดการ",
        "icon": "folder-cog",
        "group": true,                 // ★ flag บอกว่าเป็นกลุ่ม ไม่ใช่ feature
        "children": [
          { "id": "op-cl", "label": "CL Template", "icon": "workflow" }
        ]
      }
    ]
  }
]
```

- `group: true` คือตัวแยกว่า node นี้เป็นกลุ่ม (มี `children`) หรือเป็น feature (ไปหน้าได้)
- ถ้า tenant ไม่มีสิทธิ์ feature ใด → **ไม่ส่ง node นั้นมา** (กรองที่ backend ไม่ใช่ซ่อนที่ frontend)
- ถ้ากลุ่มไหนถูกกรองจน `children` ว่าง → ไม่ส่งกลุ่มนั้น
- ถ้าโมดูลไหน `children` ว่าง → ไม่ส่งโมดูลนั้น

---

## 3. Design Decisions

| # | เรื่อง | ทำอะไร | เหตุผล | กระทบ Logic? |
|---|---|---|---|---|
| 1 | แยกชั้น L1/L2/L3 | ใช้ inset well + เส้นราง + ระยะเยื้อง | สีไม่พอ — ตาแยก "ความลึก" ได้ดีกว่าแยก "เฉด" ที่ใกล้กัน | ❌ |
| 2 | สีน้ำเงิน `#0B5CFF` | สงวนให้ **active เท่านั้น** | ถ้าใช้บอกลำดับชั้นด้วย ผู้ใช้จะแยกไม่ออกว่าน้ำเงินแปลว่า "อยู่ตรงนี้" หรือ "ระดับนี้" | ❌ |
| 3 | โหมดไอคอน | ต้องกด toggle เอง · **ค่าเริ่มต้นคือกางเต็ม** | NN/g วัดได้ว่าการซ่อน nav หลังไอคอนทำให้เวลาทำงานนานขึ้นและคนใช้เมนูน้อยลง → การย่อต้องเป็นสิทธิ์ผู้ใช้ ห้ามตั้งเป็นค่าเริ่มต้น | ❌ |
| 4 | ไอคอนล้วน (ไม่มี label) | มี tooltip หน่วง 240ms + `aria-label` + `title` | 16 โมดูล มีชื่อนามธรรม (Atlas, Master Data) — แยกด้วยไอคอนอย่างเดียวไม่ไหว ต้องมีตัวช่วย | ❌ |
| 5 | slide panel สีเดียวกับ sidebar | `#0B1D3A` ไม่ใช่การ์ดขาว | การ์ดขาวลอยตัดอารมณ์ chrome ทั้งแถบ · panel เข้มทำให้อ่านเป็นส่วนขยายของ rail | ❌ |
| 6 | เปิด panel = คลิก ไม่ใช่ hover | + ปิดด้วย Esc / คลิกที่ว่าง | WCAG 1.4.13 (Content on Hover or Focus) + 3.2.1 (On Focus) — content ที่โผล่ต้อง dismissible และไม่โผล่เองตอน hover | ❌ |
| 7 | ปุ่ม toggle | ไอคอน 30px ท้ายแถว brand | ไม่กินแถวของตัวเอง คืนพื้นที่ให้เมนู 52px | ❌ |
| 8 | ⌘K command palette | ค้นข้ามทุกโมดูล ถึงระดับ L3 | SAP Fiori: search คือทางเข้าเมนูที่คนใช้บ่อยที่สุด · จำเป็นมากขึ้นเมื่อผู้ใช้ย่อ rail | ✅ ต้อง index ทุก feature |
| 9 | anim เฉพาะตอนเปิด panel | กางกลุ่มไม่รีอนิเมตรายการอื่น | รายการที่ไม่เกี่ยวขยับ = ตาเสียโฟกัส | ❌ |
| 10 | active node ต้องพับได้ | ไม่บังคับกางค้าง | ผู้ใช้ต้องปิดสิ่งที่ตัวเองไม่อยากเห็นได้เสมอ แม้กำลังอยู่ในนั้น | ❌ |

---

## 4. Component Spec

### 4.1 Sidebar (`<aside class="sidebar">`)

| | โหมดกาง | โหมดไอคอน |
|---|---|---|
| Width | `244px` (`--sidebar-w`) | `58px` (`--rail-w`) |
| Trigger | — | `body.icon-mode` |
| Transition | `width 260ms cubic-bezier(.4,0,.2,1)` | เดียวกัน |
| z-index | `35` | `35` |

> **z-index 35 สำคัญ** — ต้องสูงกว่า scrim (`30`) ไม่งั้นกดไอคอนเดิมซ้ำเพื่อปิด panel ไม่ได้ (scrim บัง) นี่คือบั๊กที่เจอตอนเทสต์

`.main` ต้อง `margin-left` ตามความกว้าง sidebar และ transition ด้วย duration เท่ากัน

### 4.2 แถว Brand (`.sb-brand`)

- โหมดกาง: `[โลโก้ 34px] [Cube 4.0 · Core / CUBE ERP] ────── [toggle 30px]` (toggle `margin-left:auto`)
- โหมดไอคอน: `flex-direction: column` → โลโก้บน / toggle ล่าง จัดกลาง
- ไอคอน toggle สลับ `panel-left-close` ↔ `panel-left-open`
- `title` + tooltip เปลี่ยนข้อความ: "ย่อเป็นไอคอน (Ctrl+B)" ↔ "กางเมนูเต็ม (Ctrl+B)"

### 4.3 ระดับ L1 — Module (`.mod` / `.mod-h`)

| | ค่า |
|---|---|
| กางอยู่ | `.mod[data-open="true"]` → `background: rgba(0,0,0,.20)` + `margin-bottom: 7px` |
| font | `13px` / `500` (active → `600` + `#fff`) |
| chevron | `chevron-down` · หมุน `-90deg` เมื่อพับ · transition `200ms` |
| มี active อยู่ข้างใน | `.mod.has-active` → ไอคอนเป็น `--c-teal-light` |

### 4.4 ระดับ L2 — Feature / Group

**Feature (`.item`)** — `12.5px` · active = พื้น `#0B5CFF` + ขีดขาวซ้าย 3px + shadow
**Group (`.grp` / `.grp-h`)** — `12px` / `600` · กางอยู่ → `background: rgba(0,0,0,.16)` (จมลึกกว่าโมดูลอีกชั้น)

### 4.5 ระดับ L3 — Sub-feature (`.sub`)

```css
.subs { margin-left: 20px; padding-left: 10px; border-left: 1px solid rgba(255,255,255,.12); }
.sub::before { content:''; position:absolute; left:-10px; top:50%; width:6px; height:1px; background: rgba(255,255,255,.12); }
```

เยื้อง + เส้นรางแนวตั้ง + ขีดสั้นแตกออกมาต่อรายการ — นี่คือสิ่งที่ทำให้ L3 อ่านออกว่าเป็นลูกของกลุ่ม ไม่ใช่พี่น้องของ L2

### 4.6 Slide Panel (`.slide`) — เฉพาะโหมดไอคอน

| | ค่า |
|---|---|
| ตำแหน่ง | `position: fixed; top:0; bottom:0; left: 58px` |
| Width | `216px` |
| Background | `#0B1D3A` (`--c-navy`) — โทนเดียวกับ sidebar |
| Shadow | `12px 0 32px rgba(11,29,58,.34)` |
| เข้า/ออก | `transform: translateX(-102%) → 0` + `opacity` · `260ms` |
| z-index | `34` (ใต้ sidebar `35`, เหนือ scrim `30`) |
| โครง | `slide-head` (kicker "MODULE" + ชื่อโมดูล) → `slide-nav` (L2 + L3) → `slide-hint` → `slide-foot` |

ข้างใน panel ใช้ class `.item` / `.grp` / `.sub` **ชุดเดียวกับโหมดกาง** — ไม่ต้องเขียน style ซ้ำ

---

## 5. Behavior Contracts

### 5.1 โหมดกางเต็ม

| การกระทำ | ผลลัพธ์ |
|---|---|
| คลิกหัวโมดูล | กาง/พับโมดูลนั้น (กางพร้อมกันหลายโมดูลได้) |
| คลิกหัวกลุ่ม | กาง/พับกลุ่มนั้น |
| คลิก feature | navigate `#/{id}` |
| คลิกหัวโมดูล/กลุ่ม **ที่มี active อยู่ข้างใน** | **ต้องพับได้** — ห้ามเด้งกลับ |

> **จุดที่พลาดง่ายที่สุด:** ถ้า `render()` เรียก "กางโมดูลของหน้าปัจจุบัน" ทุกครั้ง ผู้ใช้จะพับไม่ลง
> การกางอัตโนมัติต้องเรียก **เฉพาะ 3 จังหวะนี้เท่านั้น**: โหลดครั้งแรก · เปลี่ยน route · สลับโหมดกลับมากาง
> (ใน reference คือฟังก์ชัน `revealActive()`)

### 5.2 โหมดไอคอน

| การกระทำ | ผลลัพธ์ |
|---|---|
| คลิกไอคอนโมดูล | slide panel เปิดที่โมดูลนั้น (พร้อม stagger anim) |
| คลิกไอคอน**เดิมซ้ำ** | ปิด panel — **รวมถึงโมดูลที่กำลัง active อยู่** |
| คลิกไอคอน**อื่น**ขณะเปิด | สลับ panel ไปโมดูลนั้น |
| คลิกหัวกลุ่มใน panel | กาง/พับกลุ่ม — **ห้าม re-animate รายการอื่น** |
| คลิก feature | navigate + ปิด panel |
| คลิกที่ว่าง (scrim) | ปิด panel |
| `Esc` | ปิด panel + **คืนโฟกัสกลับที่ไอคอนโมดูลเดิม** |
| `↑` / `↓` | เลื่อน cursor ระหว่าง L2+L3 (วนรอบ) |
| `Enter` | เปิด feature ที่ cursor อยู่ |
| hover / focus ไอคอน | tooltip ชื่อโมดูล หลัง **240ms** (ไม่ใช่ทันที) |

### 5.3 สลับโหมด

- ปุ่ม toggle ในแถว brand **หรือ** `Ctrl/⌘ + B`
- ไอคอน → กาง: กางโมดูล + กลุ่มของหน้าปัจจุบันให้อัตโนมัติ (ไม่ให้ผู้ใช้หลงทาง)
- กาง → ไอคอน: ปิด panel ที่ค้างอยู่ (ถ้ามี)

### 5.4 Animation

| จังหวะ | ทำ | ไม่ทำ |
|---|---|---|
| เปิด/สลับ panel | รายการ fade-in ทีละแถว `animation-delay: index × 24ms` | — |
| กาง/พับกลุ่มใน panel | ไม่มี anim เลย · คง `scrollTop` ของ panel ไว้ | ห้าม re-render แบบใส่ delay ใหม่ |
| `↑` `↓` | ไม่ re-render | — |

Implement: ใส่ class `.anim` ให้ `slide-nav` **เฉพาะตอนเปิดโมดูลใหม่** — CSS ผูก `@keyframes` ไว้กับ `.anim` เท่านั้น

### 5.5 prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) { * { transition-duration: 1ms !important; animation-duration: 1ms !important; } }
```
บังคับมี — ผู้ใช้ที่ตั้งค่านี้มักมีอาการเวียนศีรษะจากการเคลื่อนไหวบนจอ

---

## 6. CSS Tokens

ห้ามแก้ ห้าม hardcode สีนอกรายการนี้

```css
--c-navy: #0B1D3A;         /* sidebar + slide panel */
--c-navy-2: #14284A;       /* gradient กลาง sidebar */
--c-primary: #0B5CFF;      /* active เท่านั้น */
--c-teal: #00A88E;
--c-teal-light: #5EEAD4;   /* ไอคอนของโมดูลที่มี active */

--sidebar-w: 244px;  --rail-w: 58px;  --shell-h: 52px;
--nav-l1: 13px;  --nav-l2: 12.5px;  --nav-l3: 12px;  --nav-cap: 10px;
--ease: cubic-bezier(.4, 0, .2, 1);
--rail: rgba(255,255,255,.12);   /* เส้นรางของ L3 */
```

- Font: `Noto Sans Thai` + `Inter` (Google Fonts เท่านั้น)
- Icon: Lucide `0.469.0` — reference โหลดจาก CDN สามชั้น (unpkg → jsdelivr → cdnjs) **ใน production ให้ bundle เข้าไปเลย ห้ามพึ่ง CDN**

---

## 7. Hook สำหรับระบบอื่น

ทุก node พก data attribute ไว้แล้ว — ไม่ต้องแก้ markup เพื่อต่อระบบเหล่านี้

| Attribute | ใครใช้ | ใช้ทำอะไร |
|---|---|---|
| `data-module` | Cubic — Menu Management | เปิด/ปิดโมดูลต่อ tenant |
| `data-group` | Cubic | เปิด/ปิดกลุ่ม |
| `data-feature` | Policy Center | permission gating รายฟีเจอร์ + audit ว่าใครเข้าเมนูไหน |

**หมายเหตุ:** การซ่อนเมนูตาม permission ต้องทำที่ **backend (`/api/menu`)** ไม่ใช่ `display:none` ที่ frontend — ไม่งั้น URL ยังเข้าตรงได้อยู่ดี frontend เพียงแค่ไม่วาดสิ่งที่ไม่ได้รับมา

---

## 8. Accessibility Contract

| ข้อ | มาตรฐาน | ทำอะไร |
|---|---|---|
| หัวโมดูล/หัวกลุ่ม | — | `<button aria-expanded="true\|false">` — ไม่ใช่ `<div onclick>` |
| ไอคอนโมดูล (โหมดไอคอน) | — | เพิ่ม `aria-haspopup="menu"` + `aria-label` + `title` |
| slide panel | — | `role="menu"` · รายการข้างใน `role="menuitem" tabindex="-1"` |
| เปิดด้วยคลิก ไม่ใช่ hover | WCAG 3.2.1 | ห้ามเปิด panel ตอน hover |
| ปิดได้ + ไม่หายเอง | WCAG 1.4.13 | Esc ปิด · tooltip ค้างจนกว่าจะเลื่อนเมาส์ออก |
| คืนโฟกัส | WCAG 2.4.3 | Esc → focus กลับที่ปุ่มที่เปิด |
| Focus ring | WCAG 2.4.7 | `:focus-visible { outline: 2px solid #0B5CFF; outline-offset: 2px; }` |
| toggle state | — | ปุ่ม toggle มี `aria-pressed` |

---

## 9. Open Questions

| # | คำถาม | ทางเลือก | รอใคร |
|---|---|---|---|
| **OQ-01** | เก็บโหมดเมนูล่าสุดของผู้ใช้ยังไง | reference ห้ามใช้ `localStorage` → ควรเป็น user preference ฝั่ง server (`GET/PUT /api/me/prefs`) เพราะผู้ใช้เปลี่ยนเครื่องแล้วต้องได้เหมือนเดิม | Strike |
| **OQ-02** | จำ "โมดูลที่กางอยู่" ข้าม session ด้วยไหม | (ก) ไม่จำ กางเฉพาะโมดูลของหน้าปัจจุบัน · (ข) จำทั้ง set — แนะนำ (ก) เพราะง่ายและไม่มีเมนูยาวคาหน้าจอ | Strike |
| **OQ-03** | ⌘K อยู่ใน scope ของงานนี้ไหม | reference มีให้ครบแล้ว แต่ถ้าระบบเดิมมี global search อยู่แล้ว → ใช้ตัวเดิม อย่าซ้อนกัน | Bird |
| **OQ-04** | โมดูลที่มี feature เกิน ~8 ตัว | accordion จะยาวมาก — พิจารณาแตกเป็นกลุ่ม หรือย้าย feature ท้าย ๆ ไปเป็นแท็บในหน้า | BA |
| **OQ-05** | pattern นี้ยังไม่มีใน `html-generator-v6` (A–M) | flyout + icon-toggle ควร register เป็น **pattern N** ก่อนใช้ทั่วระบบ | Chin |

---

## 10. Out of Scope

- ❌ **เนื้อหาหน้า feature** — พื้นที่ตรงกลางใน reference เป็น placeholder เขียนว่า "Feature Section" จงใจ
- ❌ Topbar / breadcrumb / user chip — มีใน reference เพื่อให้เห็นบริบท แต่ไม่ใช่ deliverable ของงานนี้
- ❌ Responsive / mobile drawer — reference ตั้ง `min-width: 1180px` · เมนูบนจอเล็กต้องออกแบบแยก
- ❌ Multi-tenant menu editor (ฝั่ง Cubic) — งานคนละใบ
- ❌ Backend `/api/menu` — brief นี้ระบุแค่ shape ที่ frontend ต้องการ

---

## ผลการตรวจ (Verification)

รันบน reference ก่อนส่ง — ผ่านครบ

- `node --check` ผ่าน · `audit.sh` → **FAIL = 0**
- Playwright DOM assertions **35 เคส ผ่านทั้งหมด**
  โครง 3 ระดับ · พับ active node ได้ทั้งโมดูลและกลุ่ม · โหมดไอคอน 58px + panel `#0B1D3A` ที่ `left:58px` · กดไอคอนเดิมซ้ำปิดได้แม้เป็นโมดูล active · กางกลุ่มไม่รีอนิเมต (opacity คงที่ `1`) · `↑↓` `Enter` `Esc` + คืนโฟกัส · `aria-haspopup` · ⌘K ค้นถึง L3 พร้อม path · `Ctrl+B` · refresh-safe · deep-link `#/pol-class` กางโมดูล+กลุ่มให้เอง · `data-module` 16 / `data-group` 4 / `data-feature` 44 · `prefers-reduced-motion` มีผลจริง
- บั๊กที่เจอระหว่างทางและแก้แล้ว: **scrim `z-30` คลุมทับ sidebar `z-20`** ทำให้กดไอคอนเดิมซ้ำเพื่อปิด panel ไม่ได้ → ยก sidebar เป็น `z-35`

---

## Checklist ส่งงาน

- [ ] Extract เป็น shared component ตัวเดียว ใช้ทุกหน้าของ Core
- [ ] `MENU` มาจาก `/api/menu` ไม่ใช่ hardcode
- [ ] หัวโมดูล/หัวกลุ่ม **ไม่ navigate**
- [ ] `revealActive()` เรียกแค่ 3 จังหวะ (โหลด / เปลี่ยน route / สลับกลับมากาง)
- [ ] sidebar `z-index` สูงกว่า scrim
- [ ] `.anim` ใส่เฉพาะตอนเปิด panel
- [ ] Lucide bundle เข้า build ไม่พึ่ง CDN
- [ ] ไม่มี `localStorage` · ไม่มี `console.log` · ไม่มีสีนอก token
- [ ] `prefers-reduced-motion` ทำงาน
- [ ] เคลียร์ OQ-01 กับ Strike ก่อน merge
