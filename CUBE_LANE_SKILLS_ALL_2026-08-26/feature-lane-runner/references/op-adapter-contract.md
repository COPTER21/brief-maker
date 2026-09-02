# OP Adapter Contract

> **เป้าหมาย:** lane ไม่ต้องรู้จัก CUBE API เลย รู้แค่ 3 operation นี้
> พอ endpoint จริงมา → เขียน adapter ตัวเดียว lane ไม่ต้องแก้แม้แต่บรรทัดเดียว

---

## 1. Operations (มีแค่ 3 ตัว)

### `pull_brief(cl_code, feature_id) → BriefPack`
ดึงของจาก SOP1 ที่ลูกค้าเซ็นแล้ว

```json
{
  "cl_code": "CL-0003",
  "feature_id": "F-PUR-003",
  "sop1_status": "completed",
  "attachments": [
    { "sow": "SOP1/SOW2", "filename": "NF-SO-2026-0031_purchase-config_Sign-off.docx", "path": "..." },
    { "sow": "SOP1/SOW2", "filename": "prototype_ref.html", "path": "..." }
  ]
}
```

**Precondition:** `sop1_status = completed` — ยังไม่เซ็น = **ห้ามเริ่ม lane** (Hard Stop #2)

---

### `attach(sow_ref, files[]) → AttachResult`
แขวนไฟล์เข้า SOW

```json
{ "sow_ref": "CL-0003/SOP2/SOW1", "files": ["01_HTML/F-PUR-003.html", "_UX_CHECK_REPORT.md"] }
```

**ต้องเป็น idempotent** — ยิงซ้ำด้วย filename เดิมต้อง **replace ไม่ใช่ append**
(เลนวน fix loop ได้หลายรอบ ถ้า append จะได้ไฟล์ซ้ำ 4 เวอร์ชันปนกัน dev หยิบผิดแน่)

---

### `set_status(sow_ref, status, note?) → void`
เปลี่ยนสถานะ SOW

| lane state | OP status |
|---|---|
| step เริ่มทำ | `กำลังทำ` |
| step ผ่าน gate | `เสร็จแล้ว` |
| blocked | `ติดปัญหา` + note = สรุป `_BLOCKED.md` |

**ห้าม set `เสร็จแล้ว` ถ้า gate ของ step นั้นไม่ PASS/WARN** — กฎเหล็ก
(สถานะใน OP คือสิ่งที่คนอื่นใช้ตัดสินใจว่าจะหยิบงานต่อ — โกหกตรงนี้ทำให้ SOP3 เริ่มงานบนของพัง)

---

## 2. `_OP_MANIFEST.json` (ตัวกลาง)

lane เขียนไฟล์นี้เสมอ **ไม่ว่า API จะพร้อมหรือไม่**

```json
{
  "cl_code": "CL-0003",
  "feature_id": "F-PUR-003",
  "generated_at": "2026-07-24T14:22:00+07:00",
  "lane_verdict": "PASS",
  "entries": [
    {
      "sow_ref": "CL-0003/SOP2/SOW1",
      "sow_name": "จัดทำ HTML",
      "status": "เสร็จแล้ว",
      "files": ["01_HTML/F-PUR-003.html", "_UX_CHECK_REPORT.md", "_COVERAGE_R1.md"],
      "synced_at": null
    },
    {
      "sow_ref": "CL-0003/SOP2/SOW4",
      "sow_name": "Final Development Document",
      "status": "เสร็จแล้ว",
      "files": ["F-PUR-003_DevPack.zip", "_OUTPUT_CHECK_REPORT.md"],
      "synced_at": null
    }
  ]
}
```

`synced_at = null` → ยังไม่ push · มีค่า → push แล้ว (ใช้ resume ได้)

---

## 3. Modes

| Mode | เมื่อไหร่ | พฤติกรรม |
|---|---|---|
| `dry-run` | **ตอนนี้ — endpoint ยังไม่กำหนด** | เขียน manifest แล้วจบ · log "pending sync" · lane นับว่า**สำเร็จ** |
| `live` | มี endpoint + token | ยิงจริง · เขียน `synced_at` · retry 3 ครั้ง backoff |

**dry-run ต้องไม่นับเป็น fail** — ไม่งั้นเลนจะ blocked ทุกตัวเพราะเรื่องที่ไม่เกี่ยวกับคุณภาพงาน

---

## 4. ข้อมูลที่ต้องได้จากฝั่ง CUBE ก่อนเปิด `live`

เอาไปถาม/กำหนดตอนคุย API:

1. **Auth** — token แบบไหน, scope อะไร, หมดอายุยังไง
2. **SOW addressing** — `sow_ref` ใช้อะไรเป็น key จริง? (`CL-0003/SOP2/SOW1` หรือ internal id?)
   → ถ้าเป็น internal id ต้องมี `resolve(cl_code, sop_seq, sow_seq) → id` เพิ่มเป็น operation ที่ 4
3. **Upload** — multipart หรือ pre-signed URL · ขนาดสูงสุด (DevPack.zip อาจ 5–20 MB)
4. **Replace semantics** — แขวนชื่อไฟล์ซ้ำแล้วระบบทำอะไร (ต้องการ replace)
5. **Status enum** — ค่าจริงในระบบคืออะไร (`รอคิว` / `กำลังทำ` / `เสร็จแล้ว` / `ติดปัญหา`?)
6. **ผู้รับผิดชอบ** — ต้อง assign ให้ AI/bot user มั้ย หรือแขวนใต้ชื่อคนได้
7. **Idempotency** — มี request key มั้ย กัน double-attach ตอน retry

> ข้อ 2 กับ 5 เป็นตัวที่ทำให้ adapter เขียนไม่ได้ถ้าไม่รู้ — ที่เหลือเดา default ได้
