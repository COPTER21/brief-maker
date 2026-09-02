# Lane Log — {FEATURE_ID}

CL: {CL_CODE} · เริ่ม: {STARTED_AT} · adapter mode: {MODE}

---

## Timeline

| เวลา | Step | Skill | Verdict | รอบ | หมายเหตุ |
|---|---|---|---|---|---|
| | S0 | requirement-intake-formatter | | 1 | |
| | S1 | html-generator-v6 | — | 1 | |
| | S2 | qc-ux-html-checker | | 1 | |

---

## Fix Rounds

### {STEP} รอบ {N}
- **issue ที่แก้:** {id + ตำแหน่ง}
- **skill:** {skill}
- **ผล:** fixed {n} / remaining {n} / new {n}
- **remaining ที่ซ้ำจากรอบก่อน:** {list — ถ้าซ้ำ 2 รอบ ต้อง escalate}

---

## Defaults ที่ตัดสินใจแทน user

| Step | ประเด็น | ค่าที่ใช้ | อ้างอิง |
|---|---|---|---|
| | | | gate-policy §6 |

> ตารางนี้คือสิ่งที่ต้องอ่านก่อนอย่างอื่นตอน review — เป็นจุดที่ AI เดาแทนคน

---

## สรุป

- verdict รวม: {PASS/WARN/BLOCKED}
- fix rounds ทั้งหมด: {n}/8
- DevPack: {path หรือ "ไม่ได้สร้าง (blocked)"}
- OP sync: {synced / pending}
