# LANE_BRIEF — {FEATURE_ID}

> ใบสั่งเข้าเลน 1 feature — คู่กับ Central Plan ทั้งก้อนเสมอ (plan = ความรู้, brief = เจตนา)
> สั้นที่สุดเท่าที่สั่งงานได้ — ความเฉพาะทาง business อยู่ใน plan แล้ว ไม่ต้องลอกมา

| | |
|---|---|
| **Feature** | `F-XXX` (ต้องมีใน workflow_graph.json — ไม่มี = Hard Stop) |
| **Wave** | ตาม BUILD_ORDER (เช็ค dependency `data`/`config` เสร็จแล้วจริง) |
| **ประเภทงาน** | new / ENH ต่อของ existing (ระบุ artifact เดิม) |

## Scope รอบนี้
- ทำ: {capability ที่เอา — อ้าง summary/edges ใน plan ได้เลย}
- ไม่ทำรอบนี้: {สิ่งที่ตัดออกทั้งที่ plan มี — สำคัญมาก กัน agent ทำเผื่อ}

## LOCK (ศักดิ์เท่าใบเซ็น)
- {LD-xx / AC-xx / OQ-Gxx ที่เกี่ยว — หรืออ้างใบเซ็น NF-SO ถ้าเป็นงานลูกค้า}

## หมายเหตุ (ถ้ามี)
- {ข้อจำกัด/ความต้องการพิเศษที่ไม่อยู่ใน plan}
