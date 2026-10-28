# DECISIONS.lock — REQ-TMP-005

> สถานะ: **พร้อมเริ่มทำ** · ใช้แทน Scope Lock ชั่วคราวจนมีใบเซ็นลูกค้า (BRD §3.4 · FRD 07 §7.0) · ห้ามสกิลปลายน้ำตัดสินขัดกับไฟล์นี้
> **โหมดไม่เฝ้า (doc-master-batch)** — AI ตัดสินทุกหมวดตาม ERP standard → ติด AI-DEFAULT ทั้งหมด (รวม G1) · ต้องให้ลูกค้ายืนยันในใบเซ็นก่อน UAT
> `AI-DEFAULT` = ใช้ค่าเสนอเพราะไม่ได้ตอบ — ทุกสกิลต้องติดป้ายนี้ต่อในเอกสารที่อ้าง

| ID | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | ค่าคงที่อ่านจาก config: "1 ต้องพัฒนา (ยังไม่สามารถปฏิบัติได้ตามมาตรฐาน)" → CompetencyLevelConfig.levels[1].description, "2 พอใช้ (ปฏิบัติได้บางส่วน แต่ยังไม่สม่ำเสมอ)" → CompetencyLevelConfig.levels[2].description, "3 ทำได้ดี (ปฏิบัติได้ตามมาตรฐานของตำแหน่ง)" → CompetencyLevelConfig.levels[3].description, "4 เชี่ยวชาญ (ทำได้ดีมาก และสามารถถ่ายทอดให้ผู้อื่นได้)" → CompetencyLevelConfig.levels[4].description · คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | สมรรถนะหลัก (Core Competency): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 5 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G4 | สมรรถนะเฉพาะสายงาน (Functional Competency): ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-07 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-08 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-09 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-10 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-11 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส CMP | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-12 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
