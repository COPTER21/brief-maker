from pathlib import Path


root = Path(__file__).resolve().parents[3]
src = root / "Pack Brief Feature" / "Pick" / "FUNCTION_CHECKLIST_F-WH-PICK_Picking.md"
dst = Path(__file__).resolve().parents[1] / src.name
lines = src.read_text(encoding="utf-8").splitlines()
out = []
for line in lines:
    if line.startswith("> จาก PREBRIEF"):
        out.append(line)
        out.append("> WF ตรวจรอบ 1 วันที่ 18 ส.ค. 2569 · ยึด Scope Lock ที่ผู้ใช้ยืนยันเหนือ checklist เดิม")
        continue
    if line.startswith("| FN-"):
        cells = line.split("|")
        cells[4] = " ✓ "
        line = "|".join(cells)
        if cells[1].strip() == "FN-17":
            cells[2] = " เลือกตำแหน่งเอง (manual): เฉพาะคลังเดียวกันและผ่าน hard eligibility เช่นเดียวกับ auto; ข้ามลำดับ priority ได้ แต่ห้าม HOLD/DAMAGED/RECEIVING/TRANSIT/VIRTUAL/PACK/STAGING, blocked/frozen/inactive · จอง + audit · แสดงคลังอื่นเป็นข้อมูลขอโอน "
            line = "|".join(cells)
        elif cells[1].strip() == "FN-24":
            cells[2] = " Negative contract: Pick รับ source จาก SO เท่านั้น; งานโอน/เติม/RTV/ผลิตไม่ส่ง trigger หรือเอกสารเข้าคิว Pick ใน scope นี้ "
            cells[3] = " Scope Lock #11 "
            line = "|".join(cells)
    out.append(line)
dst.write_text("\n".join(out) + "\n", encoding="utf-8")
print(dst)
