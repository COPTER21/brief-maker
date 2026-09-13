#!/usr/bin/env bash
# audit.sh — Self-audit lint สำหรับ HTML ที่ html-generator-v9 สร้าง (v6+ compatible)
# ใช้: bash scripts/audit.sh path/to/output.html
set -u
F="${1:-}"
if [ -z "$F" ] || [ ! -f "$F" ]; then echo "usage: bash scripts/audit.sh <file.html>"; exit 2; fi
fail=0; warn=0
hitprint(){ printf '%s\n' "$1" | sed 's/^/        /'; }
flag(){ # flag LEVEL "msg" "egrep_pattern" ["grep -v exclude"]
  local lvl="$1" msg="$2" pat="$3" excl="${4:-}" hits
  if [ -n "$excl" ]; then hits=$(grep -nE "$pat" "$F" 2>/dev/null | grep -vE "$excl" | head -5)
  else hits=$(grep -nE "$pat" "$F" 2>/dev/null | head -5); fi
  if [ -n "$hits" ]; then
    if [ "$lvl" = "FAIL" ]; then fail=$((fail+1)); printf '❌ FAIL  %s\n' "$msg"; else warn=$((warn+1)); printf '⚠️  WARN  %s\n' "$msg"; fi
    hitprint "$hits"
  fi
}
echo "=== Iron Rules audit: $F ==="
flag FAIL "Rule #36 — '.btn{ line-height:1 }' ตัดสระไทย → ใช้ padding-top:2px" '\.btn\s*\{[^}]*line-height:\s*1\b'
flag WARN "Rule #36 — overflow:hidden บน .btn เอง (ตัดสระไทย; ใช้ .btn-truncate .lbl)" '\.btn\s*\{[^}]*overflow:\s*hidden'
flag WARN "Rule #41 — data-lucide=\"eye\" (กดแถวเปิด view แทน)" 'data-lucide="eye"'
hits=$(grep -nE '<i data-lucide=' "$F" 2>/dev/null | grep -vE '\bw-[0-9]' | head -5)
if [ -n "$hits" ]; then warn=$((warn+1)); printf '⚠️  WARN  Rule #21 — <i data-lucide> ไม่มี class w-{N}/h-{N}\n'; hitprint "$hits"; fi
flag FAIL "Rule #30 — .content มี max-width (ต้อง fluid)" '\.content\s*\{[^}]*max-width'
flag WARN "Rule #40 — เซลล์ตารางมี sub-line ซ้อน (.uc-email) → แยกคอลัมน์" 'uc-email'
nopt=$(grep -oE '<option' "$F" | wc -l | tr -d ' '); nsel=$(grep -oE '<select' "$F" | wc -l | tr -d ' ')
if [ "${nsel:-0}" -gt 0 ] && [ "${nopt:-0}" -gt 0 ]; then avg=$(( nopt / nsel ))
  if [ "$avg" -gt 8 ]; then warn=$((warn+1)); printf '⚠️  WARN  Rule #34 — เฉลี่ย ~%s options/select (>8) → พิจารณา search-select\n' "$avg"; fi; fi
flag FAIL "Rule #24 — console.log ใน production" 'console\.log'
flag FAIL "Rule #24 — TODO comment" 'TODO'
flag FAIL "No-storage — localStorage/sessionStorage" '(localStorage|sessionStorage)'
flag FAIL "Rule #25 — เรียก lucide.createIcons() ตรง ๆ (ใช้ renderIcons())" 'lucide\.createIcons\(\)' 'window\.lucide\.createIcons'
grep -q 'scrollbar-gutter' "$F" || { warn=$((warn+1)); printf '⚠️  WARN  Rule #35 — ไม่พบ scrollbar-gutter:stable\n'; }
grep -q '::-webkit-scrollbar' "$F" || { fail=$((fail+1)); printf '❌ FAIL  Rule #49 — ไม่พบ custom scrollbar (::-webkit-scrollbar) — ห้ามใช้ default scrollbar\n'; }
grep -q 'scrollbar-width' "$F" || { warn=$((warn+1)); printf '⚠️  WARN  Rule #49 — ไม่พบ scrollbar-width: thin (Firefox)\n'; }
if grep -q '<table' "$F" && ! grep -qE 'empty|emptyState' "$F"; then warn=$((warn+1)); printf '⚠️  WARN  Rule #39 — มีตารางแต่ไม่พบ empty state\n'; fi
grep -q '#111111' "$F" || { warn=$((warn+1)); printf '⚠️  WARN  Rule #1 — ไม่พบ Charcoal #111111\n'; }
grep -q 'Noto Sans Thai' "$F" || { warn=$((warn+1)); printf '⚠️  WARN  Rule #2 — ไม่พบ Noto Sans Thai\n'; }
# ===== v3.13 Design Consistency checks =====
flag FAIL "Rule #11 — drawer 540px (legacy — ต้อง 920/.standard 680)" 'width:\s*540px'
flag FAIL "Rule #27 — class sb-section/sb-section-title (BANNED legacy)" 'sb-section'
flag WARN "Token — hardcoded font-size ที่ไม่ใช่ var (ควรใช้ --fs-*)" 'font-size:\s*1[0-9]px'
dupfmt=$(grep -cE 'function (fmtMoney|fmtDate|fmtDateTime|fmtNumber|emptyStateHTML|searchSelectHTML|validateField)' "$F")
if [ "${dupfmt:-0}" -gt 7 ]; then warn=$((warn+1)); printf '⚠️  WARN  Helper กลางถูก define ซ้ำ (%s) — ใช้จาก skeleton เท่านั้น\n' "$dupfmt"; fi
flag WARN "Rule #46 — ปุ่ม + (สร้าง) นอก .ph-actions? ตรวจตำแหน่งปุ่มสร้างด้วยตา" 'filter-bar[^>]*>[^<]*<button class="btn btn-primary"'
flag FAIL "Rule #48 — carousel ใน landing (ห้าม)" 'carousel'
if grep -q 'stepper' "$F" && ! grep -q 'step-dot' "$F"; then warn=$((warn+1)); printf '⚠️  WARN  Rule #47 — มี stepper แต่ไม่ใช้ component กลาง (.step-dot)\n'; fi
if grep -qE 'onclick="submit' "$F" && ! grep -q 'loader-2' "$F"; then warn=$((warn+1)); printf '⚠️  WARN  Rule #44 — มี submit แต่ไม่พบ loading state (loader-2)\n'; fi
# ---- v9: Document Archetype (Rules #98–#101) — ทริกเกอร์เมื่อไฟล์เป็นเอกสารธุรกรรม ----
if grep -qE 'vat_mode|renderSignTab|line-tbl' "$F"; then
  echo "--- doc_archetype (Pattern Q / B2 v2) ---"
  need(){ if ! grep -qE "$2" "$F"; then fail=$((fail+1)); printf '❌ FAIL  %s\n' "$1"; fi; }
  needw(){ if ! grep -qE "$2" "$F"; then warn=$((warn+1)); printf '⚠️  WARN  %s\n' "$1"; fi; }
  need "Rule #99 — line editor ต้องใช้ table.line-tbl (grid contract v2)" 'class="tbl line-tbl"'
  need "Rule #99 — ไม่พบ calcLineVat (VAT engine กลาง)" 'function calcLineVat'
  need "Rule #99 — ไม่พบ migrateLine" 'function migrateLine'
  need "Rule #99 — ไม่พบ totals() (single source of totals)" 'function totals\('
  need "Rule #99 — ไม่พบ taxBadgeV (tax pill)" 'function taxBadgeV'
  need "Rule #99 — ไม่พบ renderLineSummary" 'function renderLineSummary'
  need "Rule #99 — แถวขยายต้องใช้ selector line-expand-panel-anchor" 'line-expand-panel-anchor'
  need "Rule #99 — VAT segmented ต้องมี 3 โหมด none/add/included" "\['included', 'รวมแล้ว \(NET\)'\]"
  needw "Rule #99 — ส่วนลดท้ายบิล segmented ฿/% (endbill.mode)" "endbill\.mode"
  need "Rule #100 — wizard step ชื่อล็อก 'ตรวจสอบและยืนยัน'" 'ตรวจสอบและยืนยัน'
  need "Rule #100 — wizard step ชื่อล็อก 'เอกสารแนบ'" "'เอกสารแนบ'"
  need "Rule #100 — wizard step ชื่อล็อก 'รายการสินค้า' (ตัดได้เฉพาะเอกสารไม่มี line items — ถ้าตัด ให้ log)" "'รายการสินค้า'"
  need "Rule #100 — ทุก step ต้องเปิดด้วย STEPH()" 'STEPH\('
  need "Rule #100 — .upload-zone ใน step เอกสารแนบ" 'upload-zone'
  need "Rule #101 — view tab 'รายละเอียด' (detail)" "tabBtn\('detail'"
  need "Rule #101 — view tab 'PDF Preview' (pdf)" "tabBtn\('pdf'"
  need "Rule #101 — view tab 'ลายเซ็น / อนุมัติ' (sign)" "tabBtn\('sign'"
  need "Rule #101 — view tab 'ประวัติ' (history)" "tabBtn\('history'"
  need "Rule #101 — เอกสารแนบต้องเป็น section ใน tab รายละเอียด (SEC('paperclip', 'เอกสารแนบ…'))" "SEC\('paperclip', \`เอกสารแนบ"
  flag FAIL "Rule #101 — ห้ามมี tab เอกสารแนบแยก" "tabBtn\('(attach|files|attachments)'"
  need "Rule #98 — list ต้องมีคอลัมน์ลายเซ็น (renderSignProgress)" 'function renderSignProgress'
  need "Rule #98 — docPill (สถานะเอกสาร)" 'function docPill'
  need "Rule #98 — PDF .a4 + ช่องเซ็น" "class=\"a4\""
  need "Rule #98 — DOA slot picker (.slot-row) ใน submit modal" 'slot-row'
  need "Rule #98 — drawer create ต้องเป็น .drawer-panel.wide (1290)" 'drawer-panel wide|drawer-panel\.wide'
  flag FAIL "Rule #98 — hardcoded approval chain (ห้าม) — ต้อง resolve จาก DOA" "approval_chain\s*:\s*\[\s*\{\s*roles\s*:\s*\[\s*'[A-Za-z_]+'\s*\]\s*,\s*assignee\s*:\s*'[^']+'"  "MOCK|mock|seed|SOS\b"
fi
# ---- v9: Rule #102/#103 combobox anatomy + lean list ----
selbig=$(python3 - "$F" <<'PY' 2>/dev/null
import re,sys
s=open(sys.argv[1],encoding='utf-8').read()
n=0
for m in re.finditer(r'<select[^>]*>(.*?)</select>',s,re.S):
    if m.group(1).count('<option')>7: n+=1
print(n)
PY
)
if [ "${selbig:-0}" -gt 0 ]; then warn=$((warn+1)); printf '⚠️  WARN  Rule #102 — <select> มี >7 options (%s ตัว) → ควรเป็น search combobox\n' "$selbig"; fi
flag WARN "Rule #102 — option คน มี icon แต่ไม่มีบรรทัดตำแหน่ง (ต้อง ชื่อ→ตำแหน่ง·แผนก)" 'data-lucide="user"[^<]*<[^>]*>[^<]*</(span|div)></button>'
flag WARN "Rule #103/#40 — cell มี pill ≥2 ตัว (ซ้อนข้อมูลคนละตัวในคอลัมน์เดียว → แยกคอลัมน์)" '<td[^>]*>[^<]*(<span class="pill[^>]*>[^<]*</span>[^<]*){2,}</td>'
# ---- v9: Rule #104 one feature · one menu ----
dupnav=$(python3 - "$F" <<'PY' 2>/dev/null
import re,sys,collections
s=open(sys.argv[1],encoding='utf-8').read()
m=re.search(r'<(aside|nav)[^>]*(sidebar|nav)[^>]*>(.*?)</\1>',s,re.S|re.I)
seg=m.group(3) if m else s
hrefs=re.findall(r'href="#/([A-Za-z0-9_-]+)',seg)+re.findall(r'(?:navigate|go|route|nav)\(\\?[\'"]/?([A-Za-z0-9_-]+)',seg)+re.findall(r'data-route="/?([A-Za-z0-9_-]+)',seg)
c=collections.Counter(hrefs)
print(sum(1 for k,v in c.items() if v>1))
PY
)
if [ "${dupnav:-0}" -gt 0 ]; then warn=$((warn+1)); printf '⚠️  WARN  Rule #104 — sidebar มีหลายเมนูใต้ route เดียวกัน (%s กลุ่ม) → feature เดียว = เมนูเดียว ส่วนย่อยเป็น tabs ในหน้า\n' "$dupnav"; fi
# ---- v9: Rule #105 demo/persona control in page header · #40.1 row geometry (static hints) ----
flag FAIL "Rule #105 — persona/demo switch อยู่ใน page header (.ph-right/.ph-actions) → ย้ายไป .demo-strip" 'class="ph-(right|actions)"[^>]*>(?:(?!</div>).)*?(persona|demo|role-switch|\(ปิดบัง\)|\(เปิดเผย\))'
flag WARN "Rule #40.1 — cell คนใช้ avatar แบบ block (ไม่มี .tbl-person / inline-flex) → แถวจะสูงซ้อน" '<td[^>]*>\s*<div[^>]*class="[^"]*avatar[^"]*"[^>]*>[^<]*</div>\s*<div'
echo "-------------------------------------------"
printf 'สรุป: FAIL=%s · WARN=%s\n' "$fail" "$warn"
echo "หมายเหตุ: Thai-rhythm/empty/sticky/ปุ่มเบี้ยว = visual → render จริง: python3 scripts/render-check.py <file>"
[ "$fail" -gt 0 ] && exit 1 || exit 0
