# BRD Types — 4 ประเภท + Section Coverage Matrix

ใช้สำหรับ brd-generator-full ในการเลือก Section ที่ต้อง cover ตามประเภท BRD

---

## 1. New Feature

**คำนิยาม:** Feature ใหม่ทั้งหมด ไม่เคยมีในระบบ
**ขนาด:** เต็มทุก Section (1-18 + Appendix)

**Section Coverage:**
- ✅ Section 1-15 ครบ
- ✅ Section 16-18 (Philosophy embed)
- ✅ Screen List
- ✅ AI Review: C01-C19 + PE01-PE05

**ข้อสำคัญ:**
- ทุก step ใน Section 5 ต้องมี COSO
- ทุก rule ที่มีตัวเลข/เงื่อนไข ต้องติด Tag
- ต้องเลือก Security Preset
- ต้องมี SLA + KPI + Threshold

---

## 2. Enhancement

**คำนิยาม:** ปรับ/เพิ่มใน feature ที่มีอยู่แล้ว
**ขนาด:** เต็ม + เพิ่ม "ของเก่า vs ของใหม่" + Regression Scope

**Section Coverage:**
- ✅ Section 1-18 (เหมือน New Feature)
- ✅ Section 11 เน้น: ตาราง "ของเก่า vs ของใหม่"
- ✅ Section 11.2 Regression Scope (บังคับ)
- ✅ Section 14.5 Regression Scope ใน Dev Summary
- ✅ AI Review: C01-C19 + CE01-CE03 + PE01-PE05

**ข้อสำคัญ:**
- ทุก Section ที่เปลี่ยน ต้องเขียน "ของเก่า" คู่กับ "ของใหม่"
- Business Rules: ตรวจว่า Rule ที่เคย FIXED ต้องเปลี่ยนเป็น CONFIGURABLE/DYNAMIC หรือไม่
- Data Entity: ใช้ตาราง Action (ADD/MODIFY/REMOVE/NO CHANGE)
- Edge Cases: เน้น "ของเก่าพังเพราะของใหม่"

---

## 3. Bug Fix

**คำนิยาม:** แก้ข้อผิดพลาดของ feature ที่มีอยู่แล้ว
**ขนาด:** สั้น

**Section Coverage:**
- ✅ Section 1 (Document Info)
- ✅ Expected vs Actual Behavior
- ✅ Reproduce Steps
- ✅ Impact Analysis (สั้น)
- ✅ Root Cause (ถ้าทราบ)
- ✅ Proposed Fix
- ✅ Regression Test ที่ต้องเพิ่ม
- ✅ Dev Summary (สั้น)
- ❌ ข้าม Section 5, 6, 9, 10, 16-18 (ไม่ต้อง)
- ✅ AI Review: CB01-CB03

**ข้อสำคัญ:**
- ห้ามไม่มี Reproduce Steps (ถ้าไม่มี → STOP ขอ user)
- ตรวจว่า Bug อาจเกิดซ้ำใน Module อื่นที่ใช้ Logic เดียวกันหรือไม่
- ไม่ต้อง Generate Edge Cases ใหม่ (Bug = Edge Case ที่เกิดแล้ว)

---

## 4. Config / Chore

**คำนิยาม:** เปลี่ยน config/setting หรือ technical chore
**ขนาด:** สั้นสุด

**Section Coverage:**
- ✅ Section 1 (Document Info)
- ✅ ค่าเก่า → ค่าใหม่
- ✅ เหตุผล
- ✅ Impact Analysis (สั้นมาก)
- ✅ ผู้อนุมัติ
- ❌ ข้าม Section 5-18 (ไม่ต้อง)
- ✅ AI Review: CC01-CC04

**ข้อสำคัญ:**
- ระบุว่า Config อยู่ที่ไหน (Config File / Admin Panel / DB) เพื่อบอก Dev
- ตรวจว่ามีผลย้อนหลังกับเอกสารเก่าหรือไม่
- ⚠️ ถ้า Config นี้กระทบวงกว้าง → แนะนำให้ user ยกระดับเป็น Enhancement (สร้าง Admin Panel)

---

## Section Coverage Matrix (Quick Reference)

| Section | New Feature | Enhancement | Bug Fix | Config |
|---|:---:|:---:|:---:|:---:|
| 1. Document Info | ✅ | ✅ | ✅ | ✅ |
| 2. Business Context | ✅ | ✅ | ⚡ สั้น | ⚡ สั้น |
| 3. Scope | ✅ | ✅ | ❌ | ❌ |
| 4. User Roles | ✅ | ⚡ ถ้าเปลี่ยน | ❌ | ❌ |
| 5. User Journey + COSO | ✅ | ⚡ ถ้าเปลี่ยน | ❌ | ❌ |
| 6. Data Entity | ✅ | ⚡ ADD/MODIFY | ❌ | ❌ |
| 7. User Stories | ✅ | ⚡ Story ใหม่ | ❌ | ❌ |
| 8. Status & Lifecycle | ✅ | ⚡ ถ้าเปลี่ยน | ❌ | ❌ |
| 9. Business Rules + Tags | ✅ | ✅ | ❌ | ❌ |
| 9.5 ระดับความยืดหยุ่น | ✅ | ✅ | ❌ | ❌ |
| 10. Edge Cases | ✅ | ✅ | ❌ | ❌ |
| 11. Impact / Regression | ❌ | ✅ | ⚡ Impact only | ⚡ Impact only |
| 12. System Context & Cross-Module Impact (12.1 Value Stream ⭐) | ✅ | ✅ | ❌ | ❌ |
| 12.3 Existing System | ✅ | ✅ | ❌ | ⚡ ระบุที่ตั้ง |
| 13. Delivery Phases | ✅ | ✅ | ❌ | ❌ |
| 14. Dev Summary "ใบสั่ง" | ✅ | ✅ + 14.5 | ⚡ สั้น | ⚡ สั้นสุด |
| 15. Open Questions | ✅ | ✅ | ⚡ ถ้ามี | ⚡ ถ้ามี |
| 16. Security & Compliance | ✅ | ✅ | ❌ | ❌ |
| 17. Health Check | ✅ | ✅ | ❌ | ❌ |
| 18. Monitoring | ✅ | ✅ | ❌ | ❌ |
| Screen List | ✅ | ⚡ ถ้าเปลี่ยน | ❌ | ❌ |

Legend: ✅ บังคับ | ⚡ ใส่เฉพาะที่เกี่ยวข้อง | ❌ ไม่ต้อง
