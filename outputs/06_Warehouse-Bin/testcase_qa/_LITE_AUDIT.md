# Lite Audit — F-LOCATION-MASTER-001

- Source: 62 cases / 178 steps
- Kept: 30 cases / 47 steps
- Mode: Lite

## Keep IDs

`TC-A01,A03,A05,A07,A09,B01,B02,B04,B05,B06,B08,C01,C04,C05,C07,C08,D01,D02,D06,D07,D08,E01,E03,E05,E06,F06,H02,I01,I02,I03`

## Drop ledger

- `TC-A02,A04,A06` · ตัด/ยุบ — navigation/filter permutations ซ้ำกับ A01/A03/A05
- `TC-A08` · ตัด — audit detail ซ้ำกับ I02 ซึ่งเป็น acceptance สำคัญกว่า
- `TC-B03,B07,B09` · ตัด — keyboard/dismiss/portal technical permutations; B08 เป็นตัวแทน Esc chain
- `TC-C02,C03,C06,C09,C10` · ตัด — parent valid ถูก C01, direct error C04; type permutation/back/re-parent simulate ไม่จำเป็นในรอบคน
- `TC-D03,D04,D05` · ตัด — Freeze/bulk reason ซ้ำกับ block; derived full ต้อง simulate
- `TC-E02,E04,E07` · ตัด — validation/status permutations ซ้ำกับ C05/E03/D01
- `TC-F01,F02,F03,F04,F05,F07` · ตัด — หลังบ้าน/สิทธิ์ข้าม tenant/concurrency/idempotency/corrupt graph ต้องรันโดยระบบ
- `TC-G01,G04,G05,G06` · ตัด — ต้อง simulate module ปลายทาง; `TC-G02,G03` ยุบเข้า C08/D06
- `TC-G02,G03` · ยุบ — behavior ซ้ำกับ `TC-C08`,`TC-D06`
- `TC-H01,H03` · ตัด/ยุบ — schema/doc inspection ไม่ใช่งานคน; exact copy ถูกใช้ในทุกเคสที่เก็บ

## Merge notes

- ยุบการนำทางต่อเนื่องของ A01, B01, C01 ให้เป็นขั้นภาษาคน แต่คงจุดตรวจสำคัญ
- Expected ที่อ้างจำนวน mock ถูกเปลี่ยนเป็น “เท่าข้อมูลจริง”; คง literal เฉพาะค่าที่ผู้ทดสอบกรอกเอง
- ค่า Branch/Geo อ้างแหล่ง Company/ข้อมูลพื้นที่ ไม่ถือค่าจาก prototype เป็นข้อมูลจริง
