#!/usr/bin/env python3
"""render-check.py — เปิด HTML ด้วย headless browser แล้ว screenshot เพื่อ verify visual จริง
(Thai vertical rhythm, empty state, sticky header, ปุ่มไม่เบี้ยว) — บทเรียน: อ่าน CSS แล้วเดาไม่พอ.

ใช้: python3 scripts/render-check.py output.html [--font /path/NotoSansThai.ttf] [--out shot.png]

ต้องมี playwright + chromium (pip install playwright && playwright install chromium).
ถ้าไม่มี font ไทยในเครื่อง ให้โหลด NotoSansThai มาติดตั้งก่อน (ดู README ของ skill) —
เพราะปัญหา baseline ไทยลอยสูง "เห็นเฉพาะตอนฟอนต์ไทยโหลด".
"""
import sys, argparse, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--out', default='/tmp/render-check.png')
    ap.add_argument('--width', type=int, default=1280)
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--wait', type=int, default=1200)
    ap.add_argument('--full', action='store_true', default=True)
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright ไม่ได้ติดตั้ง — pip install playwright && playwright install chromium")
        sys.exit(2)
    uri = pathlib.Path(a.html).resolve().as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': a.width, 'height': a.height}, device_scale_factor=2)
        pg.goto(uri); pg.wait_for_timeout(a.wait)
        pg.screenshot(path=a.out, full_page=a.full)
        b.close()
    print("screenshot →", a.out)
    print("ตรวจด้วยตา: ปุ่ม/pill/เซลล์ ข้อความไทยอยู่กึ่งกลางไหม · empty state มี icon+action ไหม · sticky header ค้างไหม")

if __name__ == '__main__':
    main()
