---
name: kickoff
description: เปิดงานฟีเจอร์ใน Codex และควบคุม CUBE workflow 12 ขั้นตั้งแต่สำรวจแผนกลาง/แพ็กบรีฟ ให้ผู้ใช้เลือก declaration ไปจนถึง HTML, QC, E2E, BRD, FRD, test cases, UAT และปิดงาน ใช้เมื่อผู้ใช้พิมพ์ `$kickoff <feature>`, “kickoff feature”, “เริ่มฟีเจอร์”, หรือขอทำ feature ตาม workflow กลางของ workspace นี้
---

# Feature Workflow Kickoff

เปิดงานจากข้อมูลจริงของ workspace แล้วหยุดที่ approval gate แรก ห้ามเริ่มสร้าง artifact ก่อนผู้ใช้เคาะ

## เริ่มต้น

1. อ่าน `../../workflow.paths.md` และ resolve ทุกบทบาทเป็น path จริง
2. อ่าน `references/kickoff-checklist.md` ให้ครบ
3. ใช้ชื่อ feature จากคำสั่งเป็นคำใบ้เท่านั้น
4. สำรวจ `BRIEF_ROOT` และ `OUTPUT_ROOT` แล้วให้ผู้ใช้ยืนยันโฟลเดอร์แพ็กบรีฟ แม้พบตัวเลือกเดียว
5. อ่านทุกไฟล์ใน `CENTRAL_PLAN`; สำหรับ HTML ให้อ่าน markup จริง
6. อ่านทุกไฟล์ในแพ็กบรีฟที่ยืนยัน และตรวจของเดิมใน `OUTPUT_ROOT`
7. รายงานสิ่งที่โหลด, path แพ็กบรีฟ, dependency, wave/edge, งานเดิม และทุกจุดที่ต้องเคาะ
8. ยื่นรายการ declaration แบบเป็นกลางตาม reference ให้ผู้ใช้เลือก 0–3 ตัวหรือพักคำตอบไว้ด้วย `?`
9. หยุดรออนุมัติ ห้ามเริ่ม step 1 เอง

## หลังผู้ใช้อนุมัติ

ทำตามหัวข้อ “Codex feature workflow” ใน `AGENTS.md` โดยไหล `1→5`, หยุดให้ผู้ใช้ตรวจและทวน declaration หนึ่งบรรทัด แล้วไหล `6→12` รัน declaration ที่เลือกหลัง step 7 และหยุดรอคำสั่ง commit

## กฎเครื่องมือ

- ใช้ `.tools/python.cmd` กับ Python ทุกคำสั่งของ CUBE skills
- ใช้ `.tools/playwright.cmd` สำหรับติดตั้งหรือตรวจ Playwright
- ใช้ `.tools/bash.cmd` สำหรับ shell-based skill checks บน Windows
- ห้ามแก้ไฟล์ใน `.agents/skills` ระหว่างทำ feature
- ห้าม commit, push, ลบ หรือแก้ feature อื่นโดยไม่มีคำสั่งชัดเจน
