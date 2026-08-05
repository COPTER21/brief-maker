# Example — F-91 (SOW Template)

ตัวอย่างจริงครบชุดของฟีเจอร์ F-91 "งานย่อย (SOW Template)".

| ไฟล์ | คืออะไร |
|---|---|
| `cases.json` | เนื้อหาแบบทดสอบ (6 groups, 18 cases, ชุดข้อมูล A–G) — Claude เขียนจาก BRD+FRD+HTML |
| `shot-spec.json` | สเปกถ่ายภาพ 16 จุด — Claude เขียนจากการอ่าน HTML prototype |
| `shots_b64.json` | ภาพไฮไลต์สำเร็จรูป (ผลลัพธ์ของ `capture.py`) — รวมไว้ให้ลอง build ได้เลยโดยไม่ต้องมี prototype |

## ลอง build (ไม่ต้องมี prototype — ใช้ shots สำเร็จรูป)
```bash
cd qa-friendly-html-generator
python scripts/build.py \
  --cases examples/F-91/cases.json \
  --shots examples/F-91/shots_b64.json \
  --out   testcase-F-91.html
# เปิด testcase-F-91.html ในเบราว์เซอร์
```

## ลองถ่ายภาพใหม่เอง (ต้องมี prototype `opproc-sow.html`)
```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   # ถ้าจำเป็นใน env นี้
python scripts/capture.py \
  --pack ./path/to/pack \
  --spec examples/F-91/shot-spec.json \
  --out  /tmp/shots.json
python scripts/build.py --cases examples/F-91/cases.json --shots /tmp/shots.json --out testcase-F-91.html
```
