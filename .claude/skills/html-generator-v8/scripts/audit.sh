#!/usr/bin/env bash
# audit.sh — Self-audit lint สำหรับ HTML ที่ html-generator-v6 สร้าง
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
echo "-------------------------------------------"
printf 'สรุป: FAIL=%s · WARN=%s\n' "$fail" "$warn"
echo "หมายเหตุ: Thai-rhythm/empty/sticky/ปุ่มเบี้ยว = visual → render จริง: python3 scripts/render-check.py <file>"
[ "$fail" -gt 0 ] && exit 1 || exit 0
