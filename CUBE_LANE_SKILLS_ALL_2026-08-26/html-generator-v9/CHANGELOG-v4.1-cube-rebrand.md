# CHANGELOG v4.1 — CUBE CI Rebrand (2026-07-09)

เปลี่ยน CI จากธีม **CUBE NATIVE (Navy/Blue/Teal, Inter)** เป็น **CUBE Design System (Warm Light, Satoshi)**
ตาม design system ใหม่ที่ทีมส่งมา (`CUBE-design/tokens/*.css` + brand guide)

## หลักการ
- **ชื่อ CSS var คงเดิมทั้งหมด** (`--c-navy`, `--c-primary`, `--c-teal`, ...) เพื่อไม่กระทบ 48 Iron Rules,
  patterns A-M, drawer standard v2, JS, และ audit.sh — เปลี่ยนเฉพาะ**ค่า**
- ความหมายใหม่ของ var: `--c-navy` = **Charcoal** · `--c-primary` = **Red (action/priority)` ·
  `--c-teal` = **Orange (connection)**

## Brand Core mapping

| Var | เดิม (NATIVE) | ใหม่ (CUBE) | หมายเหตุ |
|---|---|---|---|
| `--c-navy` | `#0B1D3A` Navy | `#111111` Charcoal | headings, sidebar (flat) |
| `--c-navy-2` | `#14284A` | `#111111` | sidebar ไม่ใช่ gradient แล้ว — flat charcoal |
| `--c-primary` | `#0B5CFF` Blue | `#FF3B30` Red | CTA, links, focus ring, active menu |
| `--c-primary-hover` | `#0847CC` | `#E62E24` | |
| `--c-teal` | `#00A88E` Teal | `#FF9A1F` Orange | secondary accent = connection |
| `--c-teal-light` | `#5EEAD4` | `#FFB763` | |

## Neutrals (slate → warm)

| Var | เดิม | ใหม่ |
|---|---|---|
| `--c-ink` | `#0F172A` | `#111111` |
| body text | `#1E293B` | `#2A2B2F` |
| `--c-mute` | `#475569` | `#54565C` |
| `--c-mute-2` | `#64748B` | `#73757B` |
| `--c-mute-3` | `#94A3B8` | `#9A9CA2` |
| `--c-line` | `#CBD5E1` | `#DEDAD4` |
| `--c-line-2` | `#E2E8F0` | `#E9E5E0` |
| `--c-line-3` | `#F1F5F9` | `#F1EEEA` |
| `--c-bg-off` | `#F6F8FB` | `#FAF8F5` (Ivory) |

## Semantic + Pills

| | เดิม | ใหม่ |
|---|---|---|
| `--c-success` | `#10B981` | `#1F9D55` |
| `--c-warning` | `#D97706` | `#E8870F` |
| `--c-danger` | `#DC2626` | `#E62E24` |
| Info pill | `#DBEAFE`/`#1E40AF` | `#E6F0FF`/`#1A5FCC` |
| Success pill | `#D1FAE5`/`#065F46` | `#E4F4EB`/`#157A41` |
| Warning pill | `#FEF3C7`/`#92400E` | `#FFF1DD`/`#B8690B` |
| Inactive pill | `#F1F5F9`/`#64748B` | `#F1EEEA`/`#73757B` |
| Danger pill | `#FEE2E2`/`#DC2626` | `#FFE9E7`/`#E62E24` |

## Typography
- Font stack: `'Noto Sans Thai', 'Inter'` → **`'Satoshi', 'Noto Sans Thai'`**
- Loading: Noto Sans Thai คงจาก Google Fonts + **Satoshi จาก Fontshare CDN**
  `https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700,900&display=swap`

## Derived
- rgba navy `rgba(11,29,58,x)` → `rgba(17,17,17,x)` (backdrop, shadows)
- Logo gradient `135deg Blue→Teal` → `135deg Red→Orange` (ตรง two-dot signature ของแบรนด์)
- Sidebar gradient 3-stop navy → flat `#111111`
- audit.sh Rule #1: เช็ค `#111111` (Charcoal) แทน `#0B1D3A`

## ไฟล์ที่แก้ (22 ไฟล์)
SKILL.md · README.md · knowledge/{ci-tokens,erp-design-guide,iron-rules}.md ·
patterns/{B,C,D,H,I,K,L,M} · references/{design-system.html,conflict-resolution.md} ·
references/drawer-standard/* (4 ไฟล์) · scripts/audit.sh · templates/* (2 ไฟล์)

## ยังไม่เปลี่ยน (นอก scope "สี/CI" — รอเคาะ)
- Geometry: sidebar `232px` (design ใหม่ = 248px), shell-h `52px` (ใหม่ = topbar 60px)
- Radius scale: `--r-md 8px / --r-lg 12px` (design ใหม่ = 10px control / 14px card / 20px panel)
- Shadow-cell signature (`-3px 4px 0 rgba(17,17,17,0.10)`) ยังไม่ได้เพิ่มเป็น token
- Sentence case + microcopy voice ตาม brand guide ใหม่ (กระทบ knowledge/microcopy.md)
