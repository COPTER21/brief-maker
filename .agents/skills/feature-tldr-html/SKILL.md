---
name: feature-tldr-html
description: >
  สร้าง "หน้าปกสรุปฟีเจอร์" (Feature TL;DR / ELI5) เป็น HTML ไฟล์เดียว ที่ dev/tester/ลูกค้า/BA
  เปิดปุ๊บอ่าน 2 นาทีเข้าใจว่าฟีเจอร์นี้ทำอะไรได้ · ทำอะไรไม่ได้ · ขอบเขตแค่ไหน · ใครใช้ ·
  มีกี่หน้าจอ · กฎอะไรห้ามพลาด · เชื่อมกับ module ไหน — ภาษาระดับเด็ก 5 ขวบ ไม่มีศัพท์ระบบ
  ไม่มี field/API/SQL. แปลจาก FRD Pack (source of truth) + HTML เป็นภาษาคน.
  ★ ต่างจาก dev-brief-generator (spec 15 นาที เชิงลึก) — ตัวนี้คือหน้าปกแปะหัว pack ให้คนอ่าน
  ก่อนกดเข้า FRD จริง. ใช้เมื่อ user พูดถึง "สรุปฟีเจอร์อ่านง่าย", "หน้าปกสรุปฟีเจอร์",
  "feature summary", "feature TL;DR", "eli5 feature", "สรุปให้ dev/tester อ่านง่ายๆ",
  "ฟีเจอร์นี้ทำอะไรได้บ้าง", "summary doc อ่านง่าย", "ทำหน้าเดียวอ่านจบ", "สรุปขอบเขตฟีเจอร์",
  "feature-tldr-html", "one-pager ฟีเจอร์", "ภาษาเด็ก 5 ขวบ". ใช้ทุกครั้งที่มี FRD Pack (+HTML)
  แล้วต้องการหน้าสรุปภาษาคนสำหรับคนที่ไม่อยากอ่าน FRD เต็ม แม้ไม่เรียกชื่อ skill ตรงๆ.
  Input: FRD Pack (required) + HTML (แนะนำ). Output: 1 ไฟล์ .html เปิด browser ทันที.
---

# Feature TL;DR HTML Generator — "หน้าปกสรุปฟีเจอร์"

สร้าง **HTML ไฟล์เดียว** ที่ dev/tester เปิดแล้วอ่าน **2 นาทีเข้าใจทั้งฟีเจอร์** ก่อนกดเข้า FRD จริง

> **หลักการเดียวที่ต้องจำ:** เขียนให้ **เด็ก 5 ขวบ** อ่านรู้เรื่อง
> — ไม่มีศัพท์ระบบ (field / API / endpoint / RLS / enum / FK / query / state machine)
> — ไม่มีตาราง DB / ไม่มีโค้ด / ไม่มี route path ดิบ
> — เล่าเป็น "ทำอะไรได้" ไม่ใช่ "ระบบทำงานยังไง"

**Document Chain:** `frd-generator-v6` (FRD Pack) + `html-generator-v8` (HTML) → **`feature-tldr-html`** (หน้าปกสรุป) → แปะหัว pack ส่ง dev/tester

---

## Input

| ไฟล์ | จำเป็น | ใช้ทำอะไร |
|---|---|---|
| **FRD Pack** (`FRD_F-XX_Pack/` — 00_OVERVIEW, 01_UI, 05_RULES, 06_TESTS, ...) | **required** | source of truth — ดึงเนื้อหาทั้งหมดจากที่นี่ |
| **HTML prototype** (`<feature>.html`) | แนะนำ | ยืนยันหน้าจอ/ปุ่ม/action จริง (กัน FRD กับ HTML drift) |

**ถ้ามี FRD Pack ในมือ → เริ่มทำทันที ไม่ต้องถาม.**
ถ้าไม่มี FRD Pack เลย → บอก user ว่าต้องมี FRD Pack ก่อน (ใช้ `frd-generator-v6`).
ถ้ามีแค่ HTML ไม่มี FRD → ทำได้แบบ degraded (สกัดจากหน้าจอ) แต่เตือนว่า "ทำไม่ได้/กฎ" อาจไม่ครบ.

---

## Output

**1 ไฟล์:** `FEATURE_TLDR_[feature_id].html` — self-contained (inline CSS, ไม่มี CDN, เปิด browser ได้เลย)
- CI CUBE **Warm Light** (Ivory/Charcoal/Red/Orange, Satoshi + Noto Sans Thai)
- Print-friendly A4 (Ctrl+P ออกมาเป็น 1-2 หน้าสวย)
- ความยาวเป้าหมาย: **1 หน้าจอ scroll สั้นๆ** — ถ้ายาวเกิน 2 หน้าจอ = แปลว่ายังไม่ย่อพอ

---

## ขั้นตอน (ทำตามลำดับ)

### Step 1 — อ่าน Input ให้ครบ

อ่าน **ทุกไฟล์ใน FRD Pack** + HTML (ถ้ามี). อย่าอ่านแค่ 00_OVERVIEW แล้วเดา.
สร้าง mental model ของฟีเจอร์ก่อนเขียน — feature นี้แก้ปัญหาอะไรให้ใคร.

ดึง `feature_id` + `feature_name` + `module` จาก **00_OVERVIEW §0 (CUBE ERP Library Path)** → ใช้ตั้งชื่อไฟล์ + หัวเอกสาร.

### Step 2 — สกัดเนื้อหา 8 บล็อก (อ่าน `references/extraction-map.md`)

แต่ละบล็อกในหน้าปาก มาจาก section ไหนของ FRD — **map ไว้ครบใน `references/extraction-map.md` เปิดอ่านก่อนสกัด**. สรุปสั้น:

| บล็อกในหน้าปก | ดึงจาก |
|---|---|
| ① ฟีเจอร์นี้คืออะไร (1 ประโยค + 2-3 บรรทัด) | 00_OVERVIEW — Purpose / Scope |
| ② ✅ ทำอะไรได้ | 00_OVERVIEW scope-in + 01_UI (ปุ่ม/action) + 06_TESTS (AT ที่ผ่าน) |
| ③ ❌ ทำอะไรไม่ได้ / นอกขอบเขต | 00_OVERVIEW **Out of Scope** + 05_RULES (ข้อห้าม/lock) |
| ④ ใครใช้ + ใช้ตอนไหน | 00_OVERVIEW **Roles** + Journey/trigger จาก 01_UI |
| ⑤ มีกี่หน้าจอ แต่ละหน้าทำอะไร | 01_UI — Pages (แปลง route เป็นชื่อหน้าภาษาคน) |
| ⑥ กฎสำคัญห้ามพลาด | 05_RULES — เลือก **เฉพาะกฎที่ tester/dev พลาดแล้วเจ๊ง** แปลเป็นภาษาคน |
| ⑦ เชื่อมกับ module ไหน | 02_API cross-module + 00_OVERVIEW Downstream/Value Stream |
| ⑧ ต้องมีคนอนุมัติไหม + ข้อมูลอ่อนไหวแค่ไหน | DOA placeholder (05_RULES) + 00_OVERVIEW §0.7.1 Data Classification |

> บล็อก ⑦ ⑧ เป็น optional — ถ้าฟีเจอร์ไม่มี (ไม่เชื่อม module อื่น / ไม่มีอนุมัติ / ข้อมูลไม่อ่อนไหว) → **ตัดทิ้งทั้งบล็อก** อย่าใส่ "N/A" ให้รก.

### Step 3 — แปลเป็นภาษาเด็ก 5 ขวบ (อ่าน `references/eli5-rules.md`)

**นี่คือหัวใจของ skill.** เปิด `references/eli5-rules.md` — มีกฎการเขียน + ตารางแปลศัพท์ (glossary) ระบบ→ภาษาคน + ตัวอย่าง before/after. ห้ามข้าม.

หลักสั้นๆ:
- ประโยคสั้น 1 ใจความ · ใช้คำที่แม่ค้าตลาดเข้าใจ
- "ระบบจะ validate ว่า absolute_timeout > idle_timeout" → **"ตั้งเวลาเด้งออกยาวสุด ต้องมากกว่าเวลานั่งเฉยๆ"**
- ทุกข้อ "ทำได้" ขึ้นต้นด้วยกริยาที่คนกดปุ่มทำจริง (เพิ่ม/แก้/ค้นหา/พิมพ์ออก/ส่งอนุมัติ)
- เลี่ยงคำพวก "จัดการ (manage)", "ดำเนินการ (process)", "ระบบรองรับ" — คลุมเครือ บอกให้ชัดว่าทำอะไร

### Step 4 — Build HTML จาก template

1. อ่าน template `assets/tldr-template.html` — มี CI Warm Light + โครง 8 บล็อก + print CSS ครบแล้ว
2. เติมเนื้อหาลง placeholder (`{{...}}`) — **อย่าแก้ CSS / โครงสี** (ล็อกไว้แล้ว)
3. บล็อกไหนไม่มีข้อมูล → ลบทั้ง section ออก (ดู comment `<!-- OPTIONAL -->` ใน template)
4. เขียนไฟล์ที่ `/home/claude/FEATURE_TLDR_[feature_id].html`

### Step 5 — ตรวจก่อนส่ง (Gate)

รัน `scripts/check.sh <file.html>` — ตรวจ:
- ไม่มีศัพท์ต้องห้าม (API, endpoint, RLS, enum, FK, SQL, `SELECT`, `route`, `/api/`) หลุดเข้ามาในเนื้อหาที่คนอ่าน
- ไม่มี `{{placeholder}}` ค้าง
- HTML เปิดได้ (มี `<html>`, `</html>`, `#overlay`ไม่จำเป็น — static)
- ไม่มี CDN link (ต้อง self-contained)

ถ้า FAIL → แก้จนผ่าน. แล้ว `cp` ไป `/mnt/user-data/outputs/` → `present_files`.

---

## กฎเหล็ก (ห้ามพลาด)

1. **ห้ามมีศัพท์ระบบในเนื้อหาที่คนอ่าน** — field / column / API / endpoint / RLS / enum / FK / query / SQL / route path / state machine / payload. (ชื่อฟีเจอร์ code เช่น F-SEC-14 ใส่ได้เป็น reference เล็กๆ)
2. **source of truth = FRD Pack** — ห้ามแต่งความสามารถที่ FRD ไม่มี. ถ้า HTML กับ FRD ขัดกัน → เชื่อ FRD แต่ note ไว้ (ดู §Drift ใน extraction-map).
3. **ย่อจริง** — ถ้าเกิน 2 หน้าจอ scroll = ยังไม่ผ่าน. ตัดกฎที่ไม่สำคัญออก เหลือเฉพาะที่พลาดแล้วเจ๊ง.
4. **บล็อกว่าง = ตัดทิ้ง** ไม่ใส่ "N/A" / "ไม่มี" ให้รก.
5. **CI ล็อก** — Warm Light เท่านั้น ห้ามแก้สี/ฟอนต์ใน template.
6. **ส่งไฟล์** — เขียน `/home/claude` → `cp` `/mnt/user-data/outputs/` → `present_files`.

---

## หลังทำเสร็จ

หน้าปกนี้ **ไม่ต้องอัพเดต FEATURE_REGISTRY** (เป็น derived doc ไม่ใช่ artifact หลัก).
แนะนำ user: แปะไฟล์นี้เป็นหน้าแรกของ pack ตอนส่ง dev/tester หรือวางคู่ FRD ใน share drive.

---

## Reference files

- `references/extraction-map.md` — FRD section ไหน → บล็อกไหน + วิธี handle drift (เปิดที่ Step 2)
- `references/eli5-rules.md` — กฎเขียนภาษาคน + glossary แปลศัพท์ + ตัวอย่าง before/after (เปิดที่ Step 3)
- `assets/tldr-template.html` — HTML template CI Warm Light พร้อม placeholder (ใช้ที่ Step 4)
- `scripts/check.sh` — gate ตรวจศัพท์ต้องห้าม + placeholder ค้าง (รันที่ Step 5)
