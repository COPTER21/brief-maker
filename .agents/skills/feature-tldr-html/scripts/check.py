#!/usr/bin/env python3
# Gate สำหรับ Feature TL;DR HTML — จับศัพท์ระบบหลุด + placeholder ค้าง + CDN ต้องห้าม
# ตรวจ "เนื้อหาที่คนอ่าน" เท่านั้น (strip <style>, comments, <head> ก่อน)
import sys, re

# ศัพท์ระบบที่ห้ามหลุดเข้าเนื้อหาที่คนอ่าน (word-boundary, case-insensitive)
BANNED = [
    r"\bAPI\b", r"\bendpoint\b", r"\bendpoints\b", r"\bRLS\b", r"\benum\b",
    r"\bforeign key\b", r"\bFK\b", r"\bpayload\b", r"\bSELECT\b", r"\bINSERT\b",
    r"\bUPDATE\b", r"\bWHERE\b", r"/api/", r"\bidempotent\b", r"\bpagination\b",
    r"\bstate machine\b", r"\bCRUD\b", r"\bschema\b", r"\btenant_id\b",
    r"#/[a-z]",                       # route path ดิบ เช่น #/sessions
    r"\b[a-z_]+_(?:id|timeout|at|by)\b",   # snake_case field เช่น idle_timeout, approved_by
]
# CDN ที่อนุญาต (font เท่านั้น) — นอกจากนี้ = FAIL
ALLOWED_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "api.fontshare.com")

def strip_noise(html):
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S|re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)      # HTML comments
    html = re.sub(r"<head.*?</head>", " ", html, flags=re.S|re.I)  # font links/meta
    html = re.sub(r"<[^>]+>", " ", html)                     # tags → เหลือ text
    return html

def main():
    if len(sys.argv) < 2:
        print("usage: check.py <file.html>"); sys.exit(2)
    raw = open(sys.argv[1], encoding="utf-8").read()
    fails = []

    # 1) placeholder ค้าง
    left = re.findall(r"\{\{[A-Z_]+\}\}", raw)
    if left:
        fails.append(f"placeholder ค้าง: {sorted(set(left))}")

    # 2) CDN ต้องห้าม
    for url in re.findall(r'https?://([^/"\')\s]+)', raw):
        if url not in ALLOWED_HOSTS:
            fails.append(f"CDN ต้องห้าม (self-contained เท่านั้น ยกเว้น font): {url}")

    # 3) โครง HTML
    if "<html" not in raw.lower() or "</html>" not in raw.lower():
        fails.append("โครง HTML ไม่ครบ (<html>...</html>)")

    # 4) ศัพท์ระบบในเนื้อหา
    text = strip_noise(raw)
    for pat in BANNED:
        m = re.search(pat, text, flags=re.I)
        if m:
            snippet = text[max(0,m.start()-25):m.start()+30].strip().replace("\n"," ")
            fails.append(f"ศัพท์ระบบหลุดเข้าเนื้อหา: '{m.group()}'  …{snippet}…")

    if fails:
        print("❌ FAIL — แก้ก่อนส่ง:")
        for f in fails: print("   •", f)
        sys.exit(1)
    print("✅ PASS — ไม่มีศัพท์ระบบหลุด / placeholder ครบ / self-contained")
    sys.exit(0)

if __name__ == "__main__":
    main()
