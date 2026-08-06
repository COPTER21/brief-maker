# AI_DEFAULTS · F-BNK Bank Master
> ค่าที่ AI ตั้งเอง (ไม่มีในใบเซ็น/PREBRIEF ไม่ชี้ชัด) — **หัวหน้าต้องรีวิว** · propagate ทุกเอกสารในสาย (BRD/FRD/TC/QA) ด้วย tag `[AI-DEFAULT]`

| ID | ประเด็น | ค่า default ที่ตั้งไว้ | ที่มา / เหตุผล | ต้องยืนยันโดย |
|---|---|---|---|---|
| OQ-1 | ใคร (tier ไหน) เปิดดูเลขบัญชีเต็มได้ (`canRevealFull`) | mock: ผู้ใช้ปัจจุบันมีสิทธิ์ reveal (`currentUser.canRevealFull=true`) · reveal ทุกครั้ง log audit | seed _SEED_NOTES — รอ Strike/Policy กำหนด tier จริง | Strike / Policy |
| OQ-2 | รองรับสกุลเงินอื่นเมื่อไหร่ | ล็อก **THB เท่านั้น** เฟสนี้ (field `currency` มีใน schema แล้ว → เปิด multi-currency ภายหลังไม่ต้องแก้ schema) | seed — โยง multi-currency roadmap | Strike |
| S-04 | รูปแบบเลขบัญชี | ตรวจ **ตัวเลข 10-15 หลัก** รวม ๆ (ไม่มีตาราง format ต่อธนาคาร) | PREBRIEF S-04 [AI-DRAFT] จงใจเลื่อน | หัวหน้า |
| S-05 | SWIFT ธนาคารต่างประเทศ | 8 หรือ 11 ตัว alnum (`^[A-Z0-9]{8}$|^[A-Z0-9]{11}$`) | PREBRIEF S-05 [AI-DRAFT] | หัวหน้า |
| ADD-1 | PromptPay / e-payment ID บนบัญชีบริษัท | **ไม่ทำเฟสนี้** — แนะนำเพิ่มเป็น field เมื่อออกแบบ Payment/Receipt Voucher (format ผูก logic ปลายทาง) | recommended future — ไม่ประดิษฐ์ scope master | ตัดสินตอนทำ Payment Voucher |
| ADD-2 | per-account purpose tag (เช่น payroll-only) | **ไม่ทำ** | over-engineer สำหรับ master เฟสนี้ | — |

**Data classification (สำคัญต่อ FRD R10 + permission TC):** เลขบัญชีธนาคาร = ข้อมูลอ่อนไหว → default masking 4 ตัวท้าย · reveal-on-permission + audit log ทุกครั้ง · ต้องมีชุด **negative/permission test cases** (ผู้ไม่มีสิทธิ์ reveal ไม่ได้ + เห็นแต่ masked).
