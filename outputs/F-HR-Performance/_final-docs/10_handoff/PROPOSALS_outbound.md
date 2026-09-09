# PROPOSALS_outbound — F131 Performance / ประเมินผลงาน (F-HR-PERF)

> ปิดงาน WF-01 Phase B · 2026-09-09 · ข้อเสนอ/คำถามที่ต้องส่งออกไปยัง feature อื่น · BA/PM · Architect
> feature นี้ **ประกาศ** ปลายทางเท่านั้น (display-only / event / hook) — ไม่ hardcode สายอนุมัติ/เลข/ท่อ

## 1. Soft-refs — feature/engine ปลายทางที่ยังไม่มีตัวจริงใน workspace
| ปลายทาง | Performance ใช้ทำอะไร | สถานะ | ต้องเคาะ/wire อะไร |
|---|---|---|---|
| **HR Configuration #107** (appraisal_cycle) | อ่านรอบ/แบบฟอร์มประเมิน (ไม่สร้างเอง) | ยังไม่มี output/ | payload contract `configCycles` (API-05) · ใครเป็นเจ้าของ #107 |
| **F-HR-MOVE (Movement)** | ส่ง event ปรับตำแหน่ง/เงินเดือน (ไม่ CRUD) | ยังไม่มี | รับ event `perf.result.movement_requested` — payload frozen ที่ FRD 02_API |
| **F134 Succession Planning** | ส่งผลผู้มีศักยภาพ (display-only) | ba-done (ยังไม่ทำ Phase B) | รับ event `perf.result.succession_candidate` · F134 dep = "Performance W2" |
| **Training (F-HR-TRAIN)** | ส่ง gap → อบรม (hook) | ✅ มี outputs/F-HR-TRAIN | รับ event `perf.result.training_requested` — ยืนยัน contract ฝั่งรับ |
| **Employee Master** | อ่านชื่อ/ตำแหน่ง/แผนก + snapshot ณ รอบ (BR-10) | ยังไม่มี | source ของ dept (ใช้กับ scope หัวหน้า) |
| **ENG-DOA / ENG-NOTIFY / ENG-CSQ** | สอบทาน · แจ้งเตือน · 7C | engine กลาง | ดู declaration briefs (DOA/NTF/CSQ_BRIEF) |

## 2. OQ ค้าง — ต้องเคาะก่อน/ระหว่าง dev (ยกจาก FRD register · ไม่เดา)
| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| **OQ-PERF-05** | **CL-0013 สาย DOA ผู้บริหาร** — role-id จริงของผู้สอบทาน 2 ขั้น (แขวนตั้งแต่ 31 ส.ค.) | BA → ตั้งที่ Policy Center (DOA กลาง) | DOA_BRIEF slot ทั้ง 2 เว้น role-id ไว้ |
| **OQ-PERF-06** | **CSQ EC valuation** — มูลค่าเชิงเศรษฐกิจของผลประเมินคิดยังไง | Architect | CSQ_BRIEF · §Integration |
| **OQ-PERF-07** | payload contract ปลายทางที่ยังไม่มีตัวจริง (ข้อ 1) | PM | Integration |
| **OQ-PERF-08** | 360 feedback / competency / continuous check-in — wave ไหน | Strike | scope future |
| **OQ-PERF-09** | concurrent edit lock (2 คนแก้พร้อมกัน) — 409 policy | Strike/Architect | 03_LOGIC |
| **OQ-PERF-10** | Restricted Resources wire (masking ระดับ backend) | Architect | 04_DB/SEC |
| **OQ-PERF-11** | **mock-data**: หัวหน้า persona = ฝ่ายผลิต แต่คนขั้น mgr (อรทัย A3) = ฝ่ายบัญชี → เทส manager-review ผ่าน UI ในแผนกตนไม่ได้ (ตอนนี้เทสด้วย HR) · ควรเพิ่ม mock คนขั้น mgr ในฝ่ายผลิต | Strike/dev | demo coherence |
| **OQ-PERF-12** *(ใหม่จาก declaration)* | **re-open (แก้ผลหลังเผยแพร่) ควรมี event แจ้งเตือนพนักงานไหม** — FRD ยังไม่นิยาม event นี้ (NTF ใช้ re-publish ซ้ำ `perf.result.published`) | BA | NTF_BRIEF |

## 3. Cross-feature proposals
- **→ F134 Succession**: Performance เป็น producer ของ succession candidate (decision ผ่าน/top performer) — F134 ตอนทำ Phase B ควรรับ event นี้เป็น input
- **→ F-HR-TRAIN**: gap→Training hook เป็นทางเดียว (Performance ส่ง · Training รับ) — ยืนยันชื่อ/schema event ฝั่งรับให้ตรง
- **→ Payroll/Movement**: ผล→ปรับเงินเดือน/ตำแหน่ง เป็น event ไม่ใช่ CRUD ในหน้านี้ (LK-2)

## 4. Declarations รอบนี้
**doa + ntf + csq** (มติผู้ใช้ · แผนกลางมีแค่ doa+csq → เพิ่ม ntf ตาม PREBRIEF §12) · DOCCFG/PDFDOC = NOT_NEEDED (ไม่มีเลขรัน/เอกสารคนถือ)
- ไฟล์: `DOA_BRIEF_F-HR-Performance.md` · `NTF_BRIEF_F-HR-Performance.md` · `CSQ_BRIEF_F-HR-Performance.md`

## 5. สิทธิ์ = authority config (มติ PM/BA)
"ใครทำอะไรได้" ไม่ hardcode เป็นกฎธุรกิจในจอ — ประกาศผ่าน /doa แล้ว config ที่ DOA กลาง + dev wire (prototype คงพฤติกรรม demo ไว้เป็นตัวอย่าง) · scope การเห็น: staff=SELF · mgr=DEPT(ตน) · HR=ALL
