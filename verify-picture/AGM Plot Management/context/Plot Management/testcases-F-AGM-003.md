# AI Test Cases — F-AGM-003 Plot Management (จัดการแปลงที่ดิน)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `plot-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ HTML + UI Brief §9 แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side / optimistic lock / concurrency / role / Farmer API จริง) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-003 (AGM/Plot — WKN) |
| App entry | เปิดไฟล์ `plot-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/plots` (list — default) · `#/plots/:plot_code` (view drawer, refresh-safe) |
| ที่มา | FRD_F-AGM-003_Pack (7 ไฟล์) · BRD APPROVED (LOCK-01..12) · HTML v1.0 (audit FAIL=0) · UI_BRIEF_F-AGM-003 |
| จำนวนเคส | 56 เคส / 10 groups |
| Scope Lock | LOCK-01..12 (00_OVERVIEW §0.11 ← BRD §3.4) — ทุกข้อมีเคส verify (ดู Ledger) |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า = ข้อมูล reset กลับ seed 8 แปลง + 5 โควตา — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh (F5) ก่อนเริ่ม |
| Cross-module ⭐ | **READ-ONLY** — Plot อ่าน Quota (search + farmer snapshot) ผ่าน `QUOTAS` const + `findQuotaByNo()` · store `quota_no` snapshot · **ไม่มี write-back ไป Quota** · **1 โควตา : N แปลง** (ต่างจาก Quota→Farmer 1:0..1) · Farmer/Quota feature จริง (ENG-EXT-Q01) ทดสอบตอน SIT |

**Seed ตั้งต้น (หลัง refresh — 8 แปลง PLT-2569-001..008):**
| เลขแปลง | โควตา | เกษตรกร | จังหวัด | พื้นที่(ไร่) | เลขที่เอกสาร | สถานะ | อายุ(วัน) |
|---|---|---|---|---|---|---|---|
| PLT-2569-001 | QT-2569-001 | สมหญิง รักดี | กาญจนบุรี | 12.50 | 12345 | **รอตรวจสอบ** | 12 (ค้าง) |
| PLT-2569-002 | QT-2569-001 | สมหญิง รักดี | กาญจนบุรี | 8.75 | 12346 | **รอตรวจสอบ** | 9 (ค้าง) |
| PLT-2569-003 | QT-2569-002 | สุรพล เก่งการไร่ | สุพรรณบุรี | 25.00 | 22001 | **รอตรวจสอบ** | 5 |
| PLT-2569-004 | QT-2569-003 | ทองดี พูลผล | ราชบุรี | 15.20 | 33005 | **รอตรวจสอบ** | 20 (ค้าง) |
| PLT-2569-005 | QT-2569-002 | สุรพล เก่งการไร่ | สุพรรณบุรี | 30.40 | 22050 | **ตรวจแล้ว** | 15 |
| PLT-2569-006 | QT-2569-004 | ประนอม ใจเพชร | ราชบุรี | 6.00 | 44010 | **ตรวจแล้ว** | 25 |
| PLT-2569-007 | QT-2569-005 | สมพงษ์ ทองแท้ | กาญจนบุรี | 18.90 | 55020 | **ไม่ผ่าน** | 8 |
| PLT-2569-008 | QT-2569-003 | ทองดี พูลผล | ราชบุรี | 9.30 | 33099 | **ไม่ผ่าน** | 30 |

สรุป: รอตรวจสอบ 4 (ค้างเกิน 7 วัน 3 รายการ) · ตรวจแล้ว 2 · ไม่ผ่าน 2 · แปลงทั้งหมด 8
- PLT-007 fail_reason = "เอกสารสิทธิ์ไม่ชัดเจน · ต้องแนบฉบับใหม่" · PLT-008 fail_reason = "พิกัดอยู่นอกเขตพื้นที่ที่ระบุในโควตา"
> ⚠ **1:N signature:** โควตา **QT-2569-001 ผูก 2 แปลงในseed** (PLT-001 + PLT-002) — พิสูจน์ 1 quota : N plots ได้ทันที · การผูกแปลงที่ 3 บน QT-2569-001 ต้องสำเร็จ (ไม่มี block แบบ Quota 1:0..1) → เคส X03

**Seed โควตา (5 รายการ — verified ทุกตัว, เลือกได้ทั้งหมด · จาก `QUOTAS` const, READ-ONLY):**
| เลขโควตา | เกษตรกร | เบอร์ | เลขบัตร (masked) | ที่อยู่ (จังหวัด/อำเภอ/ตำบล) | postal |
|---|---|---|---|---|---|
| QT-2569-001 | สมหญิง รักดี | 0823456789 | 3-XXXX-XXXX-XX-2 | กาญจนบุรี/ท่าม่วง/วังขนาย | 71110 |
| QT-2569-002 | สุรพล เก่งการไร่ | 0945678901 | 3-XXXX-XXXX-XX-4 | สุพรรณบุรี/สองพี่น้อง/สองพี่น้อง | 72110 |
| QT-2569-003 | ทองดี พูลผล | 0889012345 | 3-XXXX-XXXX-XX-8 | ราชบุรี/โพธาราม/โพธาราม | 70120 |
| QT-2569-004 | ประนอม ใจเพชร | 0833334444 | 4-XXXX-XXXX-XX-3 | ราชบุรี/บ้านโป่ง/ท่าผา | 70110 |
| QT-2569-005 | สมพงษ์ ทองแท้ | 0855556666 | 4-XXXX-XXXX-XX-5 | กาญจนบุรี/ท่ามะกา/ท่ามะกา | 71120 |
> โควตาทุกใบเลือกได้ (ไม่มี block "มีโควตาแล้ว") — **ทุก verified quota ผูกได้หลายแปลง** · dropdown option = `[QT] · [ชื่อ]` + sub `[เบอร์] · [เลขบัตร masked]`

**Users:** Field Officer = **สมพร วงศ์ทะเบียน** (`CURRENT_USER` — create/edit/delete/import) · Data Steward = **ธนพล ตรวจสอบ** (`STEWARD` — verify/bulk)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| P — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination | TC-P01..P07 (7) | สูง |
| C — สร้างแปลง + quota binding + validation | TC-C01..C12 (12) | สูง |
| I — CSV Import | TC-I01..I09 (9) | สูง |
| V — ตรวจสอบยืนยัน (เดี่ยว) | TC-V01..V05 (5) | สูง |
| B — Bulk verify | TC-B01..B03 (3) | สูง |
| E — แก้ไข + State machine | TC-E01..E04 (4) | สูง |
| D — ลบ (soft / hard) | TC-D01..D04 (4) | สูง |
| W — รายละเอียด / ประวัติ | TC-W01..W04 (4) | กลาง |
| **X — Cross-module quota binding ⭐ (READ-ONLY, 1:N)** | TC-X01..X05 (5) | **สูงสุด** |
| S — System / simulate (optimistic lock, concurrency, idempotency, SoD) | TC-S01..S04 (4) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1 ← BRD §7)
| item | cases |
|---|---|
| AC-01 ค้นหา+เลือก quota → farmer snapshot read-only + fields ปลดล็อก | TC-C01, TC-C02, TC-X01, TC-X02 |
| AC-02 create happy + toast "สร้างแปลงสำเร็จ — [เลขแปลง]" + Waiting for verify + audit create | TC-C01, TC-X02 |
| AC-02b quota ไม่พบ → "ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก" + block | TC-C03 |
| AC-03 ไม่แนบ Shapefile → "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)" | TC-C05 |
| AC-04 lat นอกช่วง / long นอกช่วง (verbatim) | TC-C06, TC-C07 |
| AC-05 area 0/ติดลบ → "พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0" | TC-C08 |
| AC-06 postal ≠ 5 หลัก | TC-C11 (auto), TC-I05, TC-I08 |
| AC-07 deed ซ้ำ → "เลขที่เอกสารสิทธิ์ซ้ำ" | TC-C09, TC-E04 |
| AC-08 cascade จังหวัด→อำเภอ→ตำบล + postal auto + reset | TC-C11 |
| AC-09 search (debounce 300ms) + filter status/province + ไม่พบ → "ไม่พบรายการที่ค้นหา" | TC-P02, TC-P03, TC-P04 |
| AC-10 sort plot_code/area/deed + export CSV เคารพ filter + pagination | TC-P05, TC-P06, TC-P07 |
| AC-11 edit + บันทึก → version++ · **status คงเดิม** (LOCK-07) + audit | TC-E01 |
| AC-12 stale (version เก่า) → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| AC-13 edit ระเบียน Verified → อนุญาต · status คงเดิม (OQ-P1) | TC-E02 |
| AC-14 CSV ดี → summary total/created/failed + ทุกแถว Waiting for verify | TC-I02, TC-I08 |
| AC-15 header ไม่ตรง → reject ทั้งไฟล์ + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]" | TC-I04 |
| AC-16 lat/long/postal นอกเกณฑ์ → error รายแถว + error report download | TC-I05, TC-I02 |
| AC-17 ไม่ใช่ .csv → "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" | TC-I03 |
| AC-18 waiting + Pass+Confirm → toast "ยืนยันเรียบร้อย" + pill เขียว + audit | TC-V01 |
| AC-19 Fail ไม่กรอกเหตุผล → "กรุณากรอกเหตุผล" (block) | TC-V02 |
| AC-20 Fail + reason → pill แดง + fail_reason แสดง detail + audit | TC-V03, TC-W04 |
| AC-21 Bulk: เลือกทั้งหมด = เฉพาะ waiting · Pass → ทุกรายการ Verified + audit count | TC-B01 |
| AC-22 Bulk Fail = เหตุผลเดียวทุกรายการ (บังคับ) | TC-B02 |
| AC-23 Bulk partial (บาง verified) → "สำเร็จ X ล้มเหลว Y" + retry | TC-B03 (ต้อง simulate ส่วน per-record) |
| AC-23b verified/failed → verify ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม) | TC-V05, TC-S02 (simulate) |
| AC-24 detail 3 tab + farmer snapshot card (ดูโควตา) + download shapefile/doc | TC-W01, TC-W04 |
| AC-25 tab ประวัติ = audit timeline create/edit/verify/delete + actor/time | TC-W02 |
| AC-25b deep-link plot ไม่มี/ถูกลบ → "ไม่พบข้อมูลแปลงที่เลือก" + กลับ list | TC-W03, TC-D04 |
| AC-26 Soft delete + reason → toast "ลบแปลงแล้ว" + ซ่อนจาก list + audit | TC-D01 |
| AC-27 Hard delete + reason → ลบถาวร + กลับ list + audit · idempotent | TC-D02, TC-D04 |
| AC-28 double-click ยืนยันสร้าง → 1 รายการ (disabled + idempotency) | TC-C12 |

### Cross-Module (06_TESTS §6.9) ⭐ READ-ONLY
| XT | Scenario | Upstream | Case |
|---|---|---|---|
| XT-01 | สร้างแปลง ผูก quota → quota_no set + farmer snapshot ตรง · **quota ไม่ถูกแก้** | Quota (read) | TC-X02, TC-X05 |
| XT-02 | quota search → autocomplete คืน verified quota + farmer snapshot read-only | Quota (read) | TC-X01 |
| XT-03 | 1 quota หลายแปลง → สร้าง plot ที่ 3 บน QT-2569-001 สำเร็จ (1:N ไม่ block) | Quota | TC-X03 |
| XT-04 | quota ถูกลบหลังผูก → plot คง quota_no snapshot + flag (ไม่ error, ไม่ cascade) | Quota | TC-X04 (ต้อง simulate) |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-AGP-01 quota binding บังคับก่อนกรอก + quota_id read-only | TC-C02, TC-C04, TC-X02 |
| BR-AGP-02 1 quota : N plots (ไม่จำกัด) | TC-X03 |
| BR-AGP-03 create/import → Waiting for verify เสมอ | TC-C01, TC-I08 |
| BR-AGP-04 verify Confirm · Pass→Verified · Fail→Verification failed + reason | TC-V01, TC-V02, TC-V03 |
| BR-AGP-05 Bulk Fail = เหตุผลเดียวทุกรายการ | TC-B02 |
| BR-AGP-06 edit ไม่เปลี่ยน status อัตโนมัติ | TC-E01, TC-E02, TC-E03 |
| BR-AGP-07 audit ทุก create/edit/verify/delete (actor/time/count) | TC-W02, TC-B01 |
| BR-AGP-08 soft + hard delete + reason | TC-D01, TC-D02, TC-D03 |
| BR-AGP-09 deed_number unique → duplicate reject | TC-C09, TC-E04, TC-I07 |
| BR-AGP-10 CSV partial success + error report | TC-I02 |
| BR-AGP-11 optimistic lock + idempotency ทุก mutation | TC-C12, TC-S01, TC-D04 |
| BR-AGP-12 lat/long เก็บ 6 ทศนิยม | TC-C01 (step verify), TC-W01 |
| BR-AGP-13 shapefile mandatory · document optional | TC-C05, TC-W04, TC-I09 |

### Validation (05_RULES §5.4 VR-01..12)
| VR | cases |
|---|---|
| VR-01 required×14 "กรุณา…" | TC-C10 |
| VR-02 latitude [-90,90] | TC-C06, TC-I05 |
| VR-03 longitude [-180,180] | TC-C07, TC-I05 |
| VR-04 postal 5 digits | TC-C11, TC-I05 |
| VR-05 area_rai > 0 | TC-C08, TC-I05 |
| VR-06 shapefile มี | TC-C05 |
| VR-07 deed_number unique (exclude self) | TC-C09, TC-E04 |
| VR-08 quota เลือกก่อน | TC-C04, TC-C02 |
| VR-09 fail_reason บังคับเมื่อ Fail | TC-V02, TC-V04, TC-B02 |
| VR-10 postal ↔ ตำบล match (auto) | TC-C11, TC-I08 |
| VR-11 address_line/deed_owner ≤255 (TC-463) | TC-S03 (ต้อง simulate) |
| VR-12 cascade reset (เปลี่ยนจังหวัด→เคลียร์อำเภอ/ตำบล/postal) | TC-C11 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 quota ไม่พบ → inline error, block | TC-C03 |
| EC-02 shapefile ไม่แนบ | TC-C05 |
| EC-03 lat/long นอกช่วง | TC-C06, TC-C07 |
| EC-04 area = 0 / ติดลบ | TC-C08 |
| EC-05 postal ≠ 5 หลัก | TC-C11, TC-I05 |
| EC-06 deed ซ้ำ (form/CSV/DB race) | TC-C09, TC-I07, TC-S03 |
| EC-07 verify fail ไม่ใส่เหตุผล | TC-V02, TC-B02 |
| EC-08 bulk เลือกทั้งหมด = เฉพาะ waiting | TC-B01 |
| EC-09 bulk partial (บาง verified แล้ว) | TC-B03 (ต้อง simulate) |
| EC-10 edit ระเบียน verified → อนุญาต, status คงเดิม (OQ-P1) | TC-E02 |
| EC-11 delete ระเบียน verified → อนุญาต + audit (OQ-P2) | TC-D03 |
| EC-12 stale edit (version เก่า) → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (ต้อง simulate) |
| EC-13 concurrent verify (status เปลี่ยนแล้ว) → 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (ต้อง simulate) |
| EC-14 CSV header ไม่ตรง → reject ทั้งไฟล์ + column error | TC-I04 |
| EC-15 CSV lat/long/postal นอกเกณฑ์ → error รายแถว | TC-I05 |
| EC-16 double-submit create → idempotency → 1 รายการ | TC-C12 |
| EC-17 deep-link plot ไม่มี/ถูกลบ → "ไม่พบข้อมูลแปลงที่เลือก" + กลับ list | TC-W03, TC-D04 |
| EC-18 quota ถูกลบหลังผูก → plot คง quota_no snapshot + flag | TC-X04 (ต้อง simulate — code path snapshot fallback) |

### Legacy carry-over (TC-446..501 → AS-BUILT anchors)
| Legacy TC | Scenario | Case |
|---|---|---|
| TC-446 create happy + shapefile | TC-C01 · TC-448 (case/space/unicode search) TC-P02 |
| TC-447 quota not found | TC-C03 · TC-449 area boundaries TC-C08 |
| TC-450 shapefile mandatory | TC-C05 · TC-452 double-submit TC-C12 |
| TC-455/456 detail / deep-link missing | TC-W01 / TC-W03 |
| TC-458/459 verify pass/fail reason | TC-V01 / TC-V03 · TC-460 edit keeps status TC-E01 |
| TC-462 edit-when-verified (pending-spec) | TC-E02 (allow, OQ-P1) |
| TC-463 large/unicode text | TC-S03 (ต้อง simulate — server len guard) |
| TC-465/466 soft/hard delete | TC-D01 / TC-D02 · TC-467 delete-when-verified (pending) TC-D03 (allow, OQ-P2) |
| TC-468 idempotent delete + refresh | TC-D04 |
| TC-470/471 bulk pass/fail shared reason | TC-B01 / TC-B02 · TC-472 partial TC-B03 |
| TC-473 selection across pagination | TC-P07 (single page — SIT multi-page) |
| TC-477/479 search multi + trim/unicode | TC-P02 · TC-480 sort persist TC-P05 |
| TC-481 pagination | TC-P06 · TC-482 export CSV (filter) TC-P07 |
| TC-485/501 duplicate deed policy (pending-spec) | TC-C09 / TC-S03 |
| TC-486 stale data conflict | TC-S01 (ต้อง simulate) · TC-489 concurrency verify TC-S02 |
| TC-488 server-side validation | TC-S04 (ต้อง simulate) · TC-490 SoD lock (pending) TC-S04 |
| TC-495..499 import wizard/preview/commit/partial | TC-I01/I02/I05/I08 · TC-500 audit all state TC-W02 |

### Error catalog (05_RULES §5.6 — ที่มีผลบน UI prototype)
| error | cases |
|---|---|
| ERR_QUOTA_NOT_FOUND "ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก" | TC-C03, TC-I06 |
| BR_DEED_DUPLICATE "เลขที่เอกสารสิทธิ์ซ้ำ" | TC-C09, TC-E04, TC-I07 |
| ERR_VALIDATION_FAILED (รายช่อง) | TC-C06..C10, TC-I05 |
| ERR_SHAPEFILE_REQUIRED "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)" | TC-C05 |
| BR_VERIFY_FAIL_NO_REASON "กรุณากรอกเหตุผล" | TC-V02, TC-B02 |
| (verify no result) "กรุณาเลือกผลการตรวจสอบ" | TC-V04 |
| ERR_CSV_INVALID "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" | TC-I03 |
| (CSV header) "ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ" + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]" | TC-I04 |
| (quota binding) "กรุณาค้นหาและเลือกโควตาก่อน" | TC-C04 |
| (submit incomplete) "กรุณากรอกข้อมูลให้ครบถ้วน" | TC-C10 |
| ERR_STALE_DATA(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" | TC-S01 (simulate) |
| BR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" | TC-S02 (simulate) |
| ERR_NOT_FOUND "ไม่พบข้อมูลแปลงที่เลือก" | TC-W03, TC-D04 |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases / สถานะ |
|---|---|
| Field Officer: create/edit/delete/import/export = allow | TC-C01, TC-E01, TC-D01, TC-I02 (prototype user=สมพร) |
| Admin/Steward: +verify/bulk = allow | TC-V01, TC-B01 (prototype verify actor=ธนพล ตรวจสอบ) |
| ปุ่มซ่อนตาม RBAC (Field Officer เห็น verify ไม่ได้) | — ข้าม (prototype ไม่มี role switching — ทดสอบระบบจริงผ่าน ENC; UI จริงต้องซ่อนปุ่มตาม §5.3) |
| SoD self-verify block (OQ-P7) | TC-S04 (ต้อง simulate) |

### Scope Lock (00_OVERVIEW §0.11 ← BRD §3.4)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | capability legacy 100% (CRUD/CSV/verify/bulk/delete/search/export) | ทั้ง suite — ตัวแทน: TC-C01, TC-I02, TC-V01, TC-B01, TC-E01, TC-D01, TC-W01, TC-P02 |
| LOCK-02 | 3-state machine + soft/hard delete | TC-V01, TC-V03, TC-D01, TC-V05 |
| LOCK-03 | **quota binding บังคับ (read-only)** ⭐ | TC-C02, TC-C04, TC-X01, TC-X02 |
| LOCK-04 | address 5-field + province cascade | TC-C11 |
| LOCK-05 | **shapefile mandatory** · document optional | TC-C05, TC-W04, TC-I09 |
| LOCK-06 | **1 quota : N plots** ⭐ | TC-X03 |
| LOCK-07 | edit ไม่เปลี่ยน status | TC-E01, TC-E02, TC-E03 |
| LOCK-08 | verify confirm + fail reason บังคับ | TC-V01, TC-V02 |
| LOCK-09 | bulk fail เหตุผลเดียว | TC-B02 |
| LOCK-10 | soft/hard delete + reason | TC-D01, TC-D02 |
| LOCK-11 | CSV partial success + Waiting for verify | TC-I02, TC-I08 |
| LOCK-12 | optimistic lock + idempotency + audit + deed unique | TC-C12, TC-S01, TC-W02, TC-C09 |

### UI States (§8 State-Driven Matrix)
| item | cases |
|---|---|
| loaded / filtered / filter-empty | TC-P01, TC-P02, TC-P04 |
| stats 4 การ์ด (ค้างเกิน 7 วัน 3 รายการ) | TC-P01 |
| pill 3 สถานะ (รอตรวจสอบ/ตรวจแล้ว/ไม่ผ่าน) | TC-P01, TC-P03 |
| checkbox waiting selectable / อื่น disabled | TC-B01 |
| farmer snapshot card (teal) + ดูโควตา / quota ถูกลบ snapshot fallback | TC-W01, TC-X04 |
| field gating (locked จนเลือก quota) ⭐ | TC-C02 |
| view actions ตามสถานะ (แก้ไข/ตรวจสอบ/ลบ) | TC-V05, TC-D03 |
| submitting state ("กำลังบันทึก…/กำลังดำเนินการ…/กำลังลบ…/กำลังนำเข้า…") | TC-C01, TC-V01, TC-D01, TC-I02 (step WAIT) |
| sort / pagination footer | TC-P05, TC-P06 |

**Manifest cross-check (FRD §0.12):** Stories 10/10 · Rules BR-AGP-01..13 13/13 · VR-01..12 12/12 · EC-01..18 18/18 · XT-01..04 4/4 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — แปลงถูกต้อง (happy — ผูก QT-2569-001, พิสูจน์ 1:N ที่แปลงที่ 3)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาเลขโควตา | เลือก **QT-2569-001 · สมหญิง รักดี** *(verified — farmer snapshot: กาญจนบุรี/ท่าม่วง/วังขนาย, 0823456789 · dropdown ดึงข้อมูลอัตโนมัติ)* |
| ประเภทกรรมสิทธิ์ | โฉนด |
| เลขที่เอกสารสิทธิ์ | 78901 *(unique — ไม่ซ้ำ seed)* |
| วันที่ออกเอกสาร | 2557-06-15 |
| ชื่อเจ้าของตามเอกสาร | สมหญิง รักดี |
| ที่อยู่ | 55 หมู่ 3 |
| จังหวัด / อำเภอ / ตำบล | กาญจนบุรี / ท่าม่วง / วังขนาย *(postal auto **71110**)* |
| ละติจูด / ลองจิจูด | 14.025000 / 99.515000 |
| พื้นที่ (ไร่) | 11.25 |
| ไฟล์ลักษณะแปลง (Shapefile) | คลิกโซนแนบ (จำลอง) — **บังคับ** |
| เอกสารสิทธิ์ | *(ข้าม — ไม่บังคับ)* |

### ชุด B — ค่าผิดสำหรับ negative (ต้องเลือกโควตา ชุด A ก่อน เพื่อปลดล็อกฟิลด์)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | ละติจูด | `95` | พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90 |
| B2 | ลองจิจูด | `200` | พิกัดลองจิจูดต้องอยู่ระหว่าง -180 ถึง 180 |
| B3 | พื้นที่ (ไร่) | `0` (หรือ `-5`) | พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0 |
| B4 | เลขที่เอกสารสิทธิ์ | `12345` (ซ้ำ PLT-001) | เลขที่เอกสารสิทธิ์ซ้ำ |
| B5 | ไฟล์ลักษณะแปลง | *(ไม่แนบ)* | กรุณาแนบไฟล์ลักษณะแปลง (Shapefile) |
| B6 | ค้นหาเลขโควตา | *(ไม่เลือกเลย → submit)* | กรุณาค้นหาและเลือกโควตาก่อน |
| B7 | ค้นหาเลขโควตา | พิมพ์ `QT-9999` | ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก |

### ไฟล์ทดสอบ (Files) — runner ต้องเตรียมก่อนรัน
> header **13 คอลัมน์** (จาก `CSV_COLS` ใน HTML): `quota_no,ownership_type,deed_number,deed_issue_date,deed_owner_name,address,province,district,subdistrict,latitude,longitude,area,shapefile_url`
> *(`shapefile_url` **บังคับ** — แถวที่ไม่มี = แถวเสีย · ไปรษณีย์ไม่มีในคอลัมน์ — ระบบเติมจากตำบลอัตโนมัติ · แม่แบบดาวน์โหลดได้ในModal = `plot_template.csv`)*

| ชื่อไฟล์ | เนื้อหา |
|---|---|
| `plot_ok.csv` | 3 แถวถูกทั้งหมด — quota QT-2569-001/002/003 · deed 80001/80002/80003 · lat/long/area ในเกณฑ์ · จังหวัด/อำเภอ/ตำบลตรง ADDRESS · **มี shapefile_url ทุกแถว** (เช่น `plot_80001.zip`) |
| `plot_mixed.csv` | 6 แถว: 4 ถูก (deed 80011..80014) + แถว 3 latitude `95` + แถว 5 area `0` · **มี shapefile_url ทุกแถว** |
| `plot_badquota.csv` | 2 แถว: แถวแรกถูก · แถวสอง quota_no `QT-9999` (ไม่มีในระบบ) · **มี shapefile_url ทุกแถว** |
| `plot_dupfile.csv` | 3 แถว: แถว 2 กับแถว 3 ใช้ deed_number เดียวกัน `80010` · **มี shapefile_url ทุกแถว** |
| `plot_dupdb.csv` | 2 แถว: แถวแรก deed_number `12345` (ซ้ำ seed) + แถวสอง `80020` ใหม่ · **มี shapefile_url ทุกแถว** |
| `plot_badaddr.csv` | 2 แถว: แถวแรก subdistrict `วังขนายย` (สะกดผิด ในท่าม่วง) · แถวสอง province `นครปฐม` (ไม่มีในระบบ) · **มี shapefile_url ทุกแถว** |
| `plot_noshape.csv` | 2 แถว: แถวแรกถูกครบ · **แถวสอง `shapefile_url` ว่าง** (ทดสอบ shapefile บังคับ) |
| `plot_badheader.csv` | header ขาดคอลัมน์ `area` (เหลือ 12 คอลัมน์จาก 13) + 1 แถวข้อมูลถูก |
| `plot_too_large.csv` | ไฟล์ .csv ขนาด > 5MB (gen แถวซ้ำจนเกิน) |
| `notes.xlsx` | ไฟล์ Excel ใด ๆ (ทดสอบ guard นามสกุลไฟล์) |

---

## Test Cases

## Group P — รายการ / ค้นหา / กรอง / เรียง / ส่งออก / pagination (P-01)

### TC-P01 — เปิดหน้า list + stats widgets (happy)
- group: P · ความสำคัญ: สูง · trace: 01_UI P-01 / UI state loaded / D-01 stats
- Setup: role=Field Officer (default) · seed=default 8 แปลง (refresh) · files=—
- Start: OPEN `#/plots`
- ผ่านเมื่อ: หน้า list + สถิติ 4 การ์ดแสดงเลขตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/plots` | — | หัวข้อ **จัดการแปลงที่ดิน** + count **8 รายการ** · sub "ทะเบียนแปลงชาวไร่ · ผูกกับโควตา · ตรวจสอบยืนยันและนำเข้า CSV" · breadcrumb "เกษตรกรรม › จัดการแปลงที่ดิน" · sidebar **จัดการแปลงที่ดิน** active | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **แปลงทั้งหมด 8** (sub "ไม่รวมที่ถูกลบ") · **รอตรวจสอบ 4** (meta ส้ม "ค้างเกิน 7 วัน 3 รายการ") · **ตรวจแล้ว 2** (sub "พร้อมทำสัญญา") · **ไม่ผ่าน 2** (sub "มีเหตุผลระบุ") | ☐ |
| 3 | VERIFY ปุ่มบน page header (ขวาบน) | — | เรียงซ้าย→ขวา: **Import CSV** · **ตรวจสอบที่เลือก (0)** (disabled) · **สร้างแปลง** (ปุ่มแดง ขวาสุด) | ☐ |
| 4 | VERIFY ตาราง | — | 9 คอลัมน์: ☐, เลขแปลง (mono แดง), เลขโควตา, ชื่อเกษตรกร, จังหวัด, พื้นที่ (ไร่), เลขที่เอกสาร, สถานะ, การดำเนินการ · pill 3 สี ครบ | ☐ |
| 5 | VERIFY footer ตาราง | — | ข้อความ **1 – 8 จาก 8 รายการ** | ☐ |

### TC-P02 — ค้นหา (debounce 300ms, 5 field) (happy — AC-09)
- group: P · ความสำคัญ: สูง · trace: AC-09 / US-09 / legacy TC-477/479
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`
- ผ่านเมื่อ: ค้นได้ เลขแปลง/โควตา/ชื่อ/เอกสาร/จังหวัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "PLT-2569-007" → ช่องค้นหา | เลขแปลง | รอ ~0.3s ตารางเหลือ 1 แถว: PLT-2569-007 สมพงษ์ ทองแท้ (pill แดง **ไม่ผ่าน**) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** แล้ว TYPE "QT-2569-001" | เลขโควตา | เหลือ 2 แถว (PLT-001, PLT-002 — ผูกโควตาเดียวกัน) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** แล้ว TYPE "สุรพล" | ชื่อเกษตรกร | เหลือ 2 แถว (PLT-003, PLT-005 สุรพล เก่งการไร่) | ☐ |
| 4 | CLICK **ล้างตัวกรอง** แล้ว TYPE "33099" | เลขที่เอกสาร | เหลือ 1 แถว PLT-2569-008 | ☐ |
| 5 | CLICK **ล้างตัวกรอง** แล้ว TYPE "ราชบุรี" | จังหวัด | เหลือ 3 แถว (PLT-004, PLT-006, PLT-008 จังหวัดราชบุรี) | ☐ |

### TC-P03 — กรองสถานะ + จังหวัด (happy — AC-09)
- group: P · ความสำคัญ: สูง · trace: AC-09 / filter status+province
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **รอตรวจสอบ** | — | เหลือ 4 แถว ทุกแถว pill เหลือง **รอตรวจสอบ** · footer "1 – 4 จาก 4 รายการ" | ☐ |
| 2 | SELECT dropdown สถานะ = **ตรวจแล้ว** | — | เหลือ 2 แถว (PLT-005, PLT-006) pill เขียว **ตรวจแล้ว** | ☐ |
| 3 | SELECT dropdown สถานะ = **ไม่ผ่าน** | — | เหลือ 2 แถว (PLT-007, PLT-008) pill แดง **ไม่ผ่าน** | ☐ |
| 4 | CLICK **ล้างตัวกรอง** → SELECT dropdown จังหวัด = **กาญจนบุรี** | — | เหลือ 3 แถว (PLT-001, PLT-002, PLT-007) | ☐ |
| 5 | SELECT สถานะ = **รอตรวจสอบ** (ค้างจังหวัดกาญจนบุรีไว้) | — | เหลือ 2 แถว (PLT-001, PLT-002) — filter ผสม status+province ทำงานร่วมกัน | ☐ |

### TC-P04 — ค้นหาไม่เจอ → empty state (edge — AC-09)
- group: P · ความสำคัญ: กลาง · trace: AC-09 filter-empty
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีแปลงนี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state: **ไม่พบรายการที่ค้นหา** + "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty state) | — | ตารางกลับมา 8 รายการ | ☐ |

### TC-P05 — Sort คอลัมน์ (AC-10)
- group: P · ความสำคัญ: ต่ำ · trace: AC-10 / sortBy plot_code/area_rai/deed_number / legacy TC-480
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **พื้นที่ (ไร่)** | — | แถวเรียงพื้นที่น้อย→มาก (6.00 บนสุด → 30.40 ล่าง) | ☐ |
| 2 | CLICK หัวคอลัมน์ **พื้นที่ (ไร่)** อีกครั้ง | — | เรียงกลับ มาก→น้อย (30.40 บนสุด) | ☐ |
| 3 | CLICK หัวคอลัมน์ **เลขแปลง** | — | เรียงตาม plot_code (PLT-2569-001 บนสุด) | ☐ |
| 4 | CLICK หัวคอลัมน์ **เลขที่เอกสาร** | — | เรียงตาม deed_number (localeCompare) | ☐ |

### TC-P06 — Pagination footer + row-click เปิด view (AC-10)
- group: P · ความสำคัญ: ต่ำ · trace: AC-10 / Rule #41 (row-click = view)
- Setup: role=Field Officer · seed=default (8 < 20/หน้า — หน้าเดียว) · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ pagination | — | ปุ่มหน้า **1** (active สีแดง) · ลูกศรซ้าย/ขวา disabled (หน้าเดียว) | ☐ |
| 2 | CLICK กลางแถว PLT-2569-003 (ไม่โดน checkbox/ไอคอน) | — | view drawer เปิด eyebrow "แปลงที่ดิน · QT-2569-002" + หัวข้อ **PLT-2569-003** + route เปลี่ยนเป็น `#/plots/PLT-2569-003` | ☐ |
| 3 | PRESS Esc | — | drawer ปิด + route กลับ `#/plots` | ☐ |

### TC-P07 — Export CSV เคารพ filter (AC-10) (executable)
- group: P · ความสำคัญ: กลาง · trace: AC-10 / API-14 / legacy TC-482/473 · **หมายเหตุ: prototype มีปุ่ม Export CSV บน page header แล้ว (`exportPlots()`) · selection across pagination ยังเป็น SIT (seed หน้าเดียว)**
- Setup: role=Field Officer · seed=default
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า header | — | มีปุ่ม **Export CSV** (ไอคอน download) บน header ถัดจาก Import CSV | ☐ |
| 2 | SELECT filter สถานะ = **ตรวจแล้ว** → CLICK **Export CSV** | — | ดาวน์โหลดไฟล์ `plots_export_YYYY-MM-DD.csv` มีเฉพาะแถวที่ตรง filter (สถานะ ตรวจแล้ว) · toast เขียว **ส่งออกข้อมูล N รายการสำเร็จ** | ☐ |
| 3 | CLICK **ล้างตัวกรอง** → CLICK **Export CSV** | — | ไฟล์ใหม่มีทุกแถวในรายการปัจจุบัน (เคารพ search/filter ที่เหลือ) | ☐ |
| 4 | (ระบบจริง — SIT): export ข้ามหน้า pagination หลายหน้า | — | ไฟล์รวมทุกแถวที่ตรง filter ทุกหน้า | ☐ |

---

## Group C — สร้างแปลง + quota binding + validation (OV-01)

### TC-C01 — สร้างแปลง happy (ผูก QT-2569-001) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-02 / BR-AGP-01/03 / LOCK-03/05 / VR-08
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`
- ชุดข้อมูล: A
- ผ่านเมื่อ: quota snapshot + toast สร้างสำเร็จ + แถวใหม่ Waiting for verify

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างแปลง** (แดง ขวาบน) | — | drawer เปิดจากขวา eyebrow **สร้างแปลงที่ดิน** + หัวข้อ **สร้างแปลง** · section แรก **ค้นหาโควตา (บังคับก่อนกรอกข้อมูล)** · แถบ lock "เลือกโควตาก่อนจึงจะกรอกข้อมูลแปลงได้" | ☐ |
| 2 | CLICK ช่อง **ค้นหาเลขโควตา (Quota No.)** → พิมพ์ "QT-2569-001" | — | dropdown แสดง **QT-2569-001 · สมหญิง รักดี** + sub "0823456789 · 3-XXXX-XXXX-XX-2" · help "เลือกโควตาที่ตรวจแล้ว · เลือกได้หลายแปลงต่อ 1 โควตา (1:N) · ระบบจะดึงข้อมูลเกษตรกรให้อัตโนมัติ" | ☐ |
| 3 | CLICK ตัวเลือก **QT-2569-001 · สมหญิง รักดี** | A | การ์ด teal **ผูกกับโควตา · QT-2569-001 · สมหญิง รักดี · 0823456789** + "เลขบัตร 3-XXXX-XXXX-XX-2" (read-only) + ปุ่ม **เปลี่ยนโควตา** · **ฟิลด์แปลงปลดล็อก** (opacity เต็ม) | ☐ |
| 4 | กรอกฟิลด์ครบ: ประเภทกรรมสิทธิ์ โฉนด · เลขที่เอกสาร 78901 · วันที่ 2557-06-15 · เจ้าของ สมหญิง รักดี · ที่อยู่ 55 หมู่ 3 | A | แสดงค่าครบทุกช่อง | ☐ |
| 5 | SELECT ที่อยู่แปลง: กาญจนบุรี → ท่าม่วง → วังขนาย | A | รหัสไปรษณีย์ เติม **71110** อัตโนมัติ (readonly) · help "ระบบกำหนดให้อัตโนมัติจากตำบล" | ☐ |
| 6 | TYPE ละติจูด 14.025000 · ลองจิจูด 99.515000 · พื้นที่ 11.25 | A | แสดงค่า (inputmode decimal) | ☐ |
| 7 | CLICK โซน **ไฟล์ลักษณะแปลง (Shapefile)** | — | toast info **จำลองแนบไฟล์ลักษณะแปลง (Shapefile .zip ≤50MB)** · โซนขึ้นชื่อไฟล์ + "คลิกเพื่อเปลี่ยน" | ☐ |
| 8 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (กดซ้ำไม่ได้) | ☐ |
| 9 | WAIT จน toast ปรากฏ (≤3s) | — | drawer ปิด + toast เขียว **สร้างแปลงสำเร็จ — PLT-2569-009** | ☐ |
| 10 | VERIFY ตาราง | — | แถวบนสุด = PLT-2569-009 สมหญิง รักดี · pill เหลือง **รอตรวจสอบ** · count = **9 รายการ** · การ์ดรอตรวจสอบ = 5 | ☐ |
| 11 | CLICK แถว PLT-2569-009 → Tab **ประวัติ** | — | มี 1 event **สร้างแปลง** โดย สมพร วงศ์ทะเบียน + note "ผูกกับโควตา QT-2569-001 · สมหญิง รักดี" | ☐ |

### TC-C02 — Field gating: ฟิลด์ล็อกจนกว่าเลือกโควตา ★ signature
- group: C · ความสำคัญ: สูงสุด · trace: AC-01 / BR-AGP-01 / LOCK-03 / VR-08
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY block ฟิลด์แปลง ก่อนเลือกโควตา | — | โซน `#plot-fields` จางลง (opacity ~0.55, pointer-events none) · แถบ info มีไอคอน lock "เลือกโควตาก่อนจึงจะกรอกข้อมูลแปลงได้" · ทุก input/select disabled | ☐ |
| 2 | พยายาม CLICK ช่อง **เลขที่เอกสารสิทธิ์** | — | กดไม่ได้ (fields locked) | ☐ |
| 3 | CLICK ค้นหาโควตา → เลือก **QT-2569-002 · สุรพล เก่งการไร่** | — | การ์ด teal ปรากฏ · **ฟิลด์ปลดล็อกทันที** (opacity เต็ม, พิมพ์ได้) · แถบ lock หาย | ☐ |
| 4 | CLICK ปุ่ม **เปลี่ยนโควตา** | — | กลับไปโหมดค้นหาโควตา · ฟิลด์ล็อกอีกครั้ง (เลือกใหม่ได้) | ☐ |

### TC-C03 — โควตาไม่พบ → inline error (negative — AC-02b / EC-01)
- group: C · ความสำคัญ: สูง · trace: AC-02b / EC-01 / ERR_QUOTA_NOT_FOUND / legacy TC-447
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง**
- ชุดข้อมูล: B7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ค้นหาโควตา → พิมพ์ "QT-9999" | B7 | dropdown แสดงข้อความว่าง **ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก** (emptyText) | ☐ |
| 2 | VERIFY ฟิลด์แปลง | — | ยัง **locked** (ไม่มีโควตาที่เลือก) — กรอกข้อมูลแปลงไม่ได้ | ☐ |
| 3 | ลบคำค้น พิมพ์ "สมพงษ์" (ชื่อในโควตา QT-2569-005) | — | dropdown พบ **QT-2569-005 · สมพงษ์ ทองแท้** (ค้นด้วยชื่อได้) | ☐ |

### TC-C04 — Submit ก่อนเลือกโควตา → block (negative — VR-08)
- group: C · ความสำคัญ: สูง · trace: BR-AGP-01 / VR-08 / "กรุณาค้นหาและเลือกโควตาก่อน"
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง**
- ชุดข้อมูล: B6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไม่เลือกโควตา → CLICK ปุ่ม **ยืนยันสร้าง** ทันที | B6 | ไม่บันทึก + toast เหลือง **กรุณาค้นหาและเลือกโควตาก่อน** — ไม่มีแปลงใหม่ | ☐ |
| 2 | VERIFY count ตาราง (หลังปิด) | — | ยัง 8 รายการ | ☐ |

### TC-C05 — ไม่แนบ Shapefile → block (negative — AC-03 / VR-06 / EC-02)
- group: C · ความสำคัญ: สูง · trace: AC-03 / VR-06 / ERR_SHAPEFILE_REQUIRED / LOCK-05 / legacy TC-450
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-003 → กรอกฟิลด์ครบ (**ยกเว้น Shapefile**)
- ชุดข้อมูล: A (ยกเว้น B5 — ไม่แนบไฟล์)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ไม่คลิกโซน Shapefile → CLICK **ยืนยันสร้าง** | B5 | ไม่บันทึก + ข้อความแดงใต้โซน Shapefile **กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | CLICK โซน **ไฟล์ลักษณะแปลง (Shapefile)** → CLICK **ยืนยันสร้าง** → WAIT | — | แนบแล้ว (กรอบเขียว) → บันทึกสำเร็จ toast **สร้างแปลงสำเร็จ — [เลขแปลง]** | ☐ |
| 3 | VERIFY โซน **เอกสารสิทธิ์ (ไม่บังคับ)** | — | เว้นว่างได้ ไม่ block (document optional) | ☐ |

### TC-C06 — ละติจูดนอกช่วง (negative — AC-04 / VR-02)
- group: C · ความสำคัญ: สูง · trace: AC-04 / VR-02 / EC-03
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "95" → ช่อง **ละติจูด** → CLICK **ยืนยันสร้าง** | B1 | ข้อความแดงใต้ช่อง **พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90** + กรอบช่องแดง | ☐ |
| 2 | แก้เป็น "14.025" | — | error หายเมื่อ validate ซ้ำ (ค่าในเกณฑ์) | ☐ |

### TC-C07 — ลองจิจูดนอกช่วง (negative — AC-04 / VR-03)
- group: C · ความสำคัญ: สูง · trace: AC-04 / VR-03 / EC-03
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001
- ชุดข้อมูล: B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "200" → ช่อง **ลองจิจูด** → CLICK **ยืนยันสร้าง** | B2 | ข้อความแดง **พิกัดลองจิจูดต้องอยู่ระหว่าง -180 ถึง 180** | ☐ |

### TC-C08 — พื้นที่ 0/ติดลบ (negative — AC-05 / VR-05)
- group: C · ความสำคัญ: สูง · trace: AC-05 / VR-05 / EC-04 / legacy TC-449
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "0" → ช่อง **พื้นที่ (ไร่)** → CLICK **ยืนยันสร้าง** | B3 | ข้อความแดง **พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0** | ☐ |
| 2 | TYPE "-5" ต่อ → CLICK **ยืนยันสร้าง** | — | error เดิมคงอยู่ (ติดลบ ≤ 0) | ☐ |

### TC-C09 — เลขที่เอกสารซ้ำ (negative — AC-07 / VR-07)
- group: C · ความสำคัญ: สูง · trace: AC-07 / VR-07 / BR_DEED_DUPLICATE / BR-AGP-09 / legacy TC-485
- Setup: role=Field Officer · seed=default (deed 12345 มีอยู่ที่ PLT-001) · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001
- ชุดข้อมูล: B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "12345" → ช่อง **เลขที่เอกสารสิทธิ์** แล้ว CLICK ช่องอื่น (blur) | B4 | ข้อความแดงใต้ช่อง **เลขที่เอกสารสิทธิ์ซ้ำ** + กรอบช่องแดง (checkDeed on-blur) | ☐ |
| 2 | กรอกช่องที่เหลือครบ → CLICK **ยืนยันสร้าง** | — | ไม่บันทึก + error ใต้ช่องเอกสารคงเดิม + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 3 | แก้เลขเอกสารเป็น "78901" → CLICK **ยืนยันสร้าง** → WAIT | — | บันทึกสำเร็จ toast **สร้างแปลงสำเร็จ — [เลขแปลง]** | ☐ |

### TC-C10 — required ครบชุด (negative — VR-01)
- group: C · ความสำคัญ: สูง · trace: VR-01 / ERR_VALIDATION_FAILED
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001 (ปลดล็อกฟิลด์) → **ไม่กรอกอะไรต่อ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** ทันที (ฟิลด์ว่าง) | — | ไม่บันทึก + error ครบ: **กรุณากรอกละติจูด / กรุณากรอกลองจิจูด / กรุณากรอกพื้นที่** + required อื่น "กรุณา…" + ข้อความ Shapefile **กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | VERIFY ช่อง **เอกสารสิทธิ์ (ไม่บังคับ)** | — | ไม่มี error (optional) | ☐ |

### TC-C11 — Address cascade + postal auto + reset (AC-08 / VR-04/10/12)
- group: C · ความสำคัญ: สูง · trace: AC-08 / VR-04, VR-10, VR-12 / LOCK-04 / cascade
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง **อำเภอ/ตำบล** ก่อนเลือกจังหวัด | — | อำเภอ disabled (placeholder/สีเทา, emptyText "เลือกจังหวัดก่อน") | ☐ |
| 2 | SELECT จังหวัด **ราชบุรี** → อำเภอ **บ้านโป่ง** → ตำบล **ท่าผา** | — | รหัสไปรษณีย์ เติม **70110** อัตโนมัติ (readonly, 5 หลัก) | ☐ |
| 3 | SELECT อำเภอใหม่ = **โพธาราม** | — | ตำบล + ไปรษณีย์ ถูกเคลียร์ (reset ลูกโซ่ · จังหวัดคงเดิม ราชบุรี) | ☐ |
| 4 | SELECT จังหวัดใหม่ = **สุพรรณบุรี** | — | อำเภอ/ตำบล/ไปรษณีย์ ถูกเคลียร์ทั้งหมด (cascade reset — VR-12) | ☐ |
| 5 | SELECT สุพรรณบุรี → สองพี่น้อง → ต้นตาล | — | ไปรษณีย์ = **72110** (auto) · ช่องไปรษณีย์แก้เองไม่ได้ (readonly — postal ผิด 5 หลักเป็นไปไม่ได้ทางฟอร์ม; ตรวจ 5-หลัก ที่ CSV แทน — TC-I05) | ☐ |

### TC-C12 — Double-click กันสร้างซ้ำ (edge — AC-28 / EC-16)
- group: C · ความสำคัญ: สูง · trace: AC-28 / EC-16 / BR-AGP-11 (idempotency) / legacy TC-452
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง** → เลือกโควตา QT-2569-001 → กรอกชุด A ครบ + แนบ Shapefile

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยันสร้าง** สองครั้งเร็วที่สุด (double-click) | — | คลิกแรกปุ่มกลายเป็น **กำลังบันทึก…** + disabled — คลิกที่สองไม่มีผล | ☐ |
| 2 | WAIT จน toast → VERIFY ตาราง | — | มีแปลงใหม่ **1 รายการเท่านั้น** (count = 9 รายการ, ไม่ใช่ 10) | ☐ |

---

## Group I — CSV Import (OV-05 — ทุกแถว Waiting for verify)

### TC-I01 — ดาวน์โหลดแม่แบบ + modal (13 คอลัมน์)
- group: I · ความสำคัญ: สูง · trace: US-03 / legacy TC-495 / 13 คอลัมน์
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Import CSV** | — | modal หัวข้อ **นำเข้าแปลงที่ดินจากไฟล์ CSV** + subtitle ".csv (UTF-8) ≤5MB · ทุกแถวสถานะ \"รอตรวจสอบ\" · โควตาต้องมีในระบบ · เลขที่เอกสารไม่ซ้ำ" | ☐ |
| 2 | VERIFY แถบดาวน์โหลด + คำแนะนำ | — | แถบ **ดาวน์โหลดแม่แบบ CSV** + ปุ่ม **ดาวน์โหลดแม่แบบ** · กล่องคำแนะนำ "header ตรงแม่แบบ 13 คอลัมน์ · UTF-8 · โควตาต้องเป็นเลขที่มีในระบบ · **shapefile_url บังคับ** · ละติจูด [-90,90] · ลองจิจูด [-180,180] · พื้นที่ > 0 · เลขที่เอกสารซ้ำ = แถวเสีย" | ☐ |
| 3 | CLICK **ดาวน์โหลดแม่แบบ** | — | ได้ไฟล์ `plot_template.csv` — header 13 คอลัมน์: quota_no,ownership_type,deed_number,deed_issue_date,deed_owner_name,address,province,district,subdistrict,latitude,longitude,area,shapefile_url + 2 แถวตัวอย่าง (UTF-8 BOM — ไทยไม่เพี้ยน) | ☐ |
| 4 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ยังไม่เลือกไฟล์) | ☐ |

### TC-I02 — Import แถวผสม → partial success + error report (happy — AC-14/16 / EC-15)
- group: I · ความสำคัญ: สูง · trace: AC-14, AC-16 / BR-AGP-10 / LOCK-11 · ทุกแถว Waiting for verify
- Setup: role=Field Officer · seed=default · files=`plot_mixed.csv` (6 แถว: 4 ดี 2 เสีย)
- Start: OPEN `#/plots` → CLICK **Import CSV**
- ผ่านเมื่อ: แถวดีสร้างครบ + แถวเสียรายงาน download ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD plot_mixed.csv | — | ชื่อไฟล์ + ขนาด (KB) แสดงข้างปุ่ม | ☐ |
| 2 | VERIFY สรุปผลตรวจ (preview — ก่อนเขียน) | — | 3 chip: **แถวทั้งหมด 6** · **ผ่าน 4** · **ไม่ผ่าน 2** | ☐ |
| 3 | VERIFY ตารางข้อผิดพลาด "รายละเอียดข้อผิดพลาด (แถวเสียจะถูกข้าม)" | — | 2 แถว: "แถว 3" latitude **พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90** · "แถว 5" area **พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0** | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันนำเข้า (4 แถว)** → WAIT | — | ปุ่มเป็น **กำลังนำเข้า…** → phase done: chip แถวทั้งหมด 6 / **สร้างสำเร็จ 4** / **ล้มเหลว 2** + toast **นำเข้าแปลง 4 รายการสำเร็จ — ข้าม 2 แถว** | ☐ |
| 5 | CLICK ปุ่ม **ดาวน์โหลดรายงาน** | — | ได้ไฟล์ `plot-upload-errors.csv` มี 2 แถว error | ☐ |
| 6 | CLICK **ปิด** → VERIFY ตาราง | — | แปลงใหม่ 4 แถวบนสุด ทุกแถว pill เหลือง **รอตรวจสอบ** · count = **12 รายการ** | ☐ |

### TC-I03 — File guard: นามสกุล + ขนาด (negative — AC-17)
- group: I · ความสำคัญ: สูง · trace: AC-17 / ERR_CSV_INVALID
- Setup: role=Field Officer · seed=default · files=`notes.xlsx`, `plot_too_large.csv`
- Start: OPEN `#/plots` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD notes.xlsx | — | toast แดง **ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV** — ไฟล์ไม่ถูกรับ | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD plot_too_large.csv | — | toast แดง **ขนาดไฟล์ต้องไม่เกิน 5MB** — ไฟล์ไม่ถูกรับ, ปุ่มยืนยันยัง disabled | ☐ |

### TC-I04 — Header ไม่ตรงแม่แบบ → reject ทั้งไฟล์ (edge — AC-15 / EC-14)
- group: I · ความสำคัญ: สูง · trace: AC-15 / EC-14 / LOCK-11
- Setup: role=Field Officer · seed=default · files=`plot_badheader.csv` (ขาดคอลัมน์ area)
- Start: OPEN `#/plots` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกไฟล์** → UPLOAD plot_badheader.csv | — | ไม่ขึ้น preview + ข้อความแดงใต้ช่องไฟล์ **คอลัมน์ไฟล์ไม่ตรงแม่แบบ: area** (หรือ "จำนวนคอลัมน์ไม่ถูกต้อง (12/13)") + toast แดง **ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ** | ☐ |
| 2 | VERIFY ตารางหลังปิด modal | — | ไม่มีแถวใดถูกสร้าง (count ยัง 8 รายการ) | ☐ |

### TC-I05 — lat/long/area/postal นอกเกณฑ์ รายแถว (edge — AC-16 / EC-15)
- group: I · ความสำคัญ: สูง · trace: AC-16 / VR-02/03/04/05 / legacy TC-497
- Setup: role=Field Officer · seed=default · files=`plot_badgeo.csv` (2 แถว: lat 100 / long 200)
- Start: OPEN `#/plots` → CLICK **Import CSV**
> gen `plot_badgeo.csv`: แถว 1 latitude=100 · แถว 2 longitude=200 (fields อื่นถูก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD plot_badgeo.csv | — | preview: ผ่าน 0 / ไม่ผ่าน 2 — "แถว 2" latitude **พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90** · "แถว 3" longitude **พิกัดลองจิจูดต้องอยู่ระหว่าง -180 ถึง 180** | ☐ |
| 2 | VERIFY ปุ่ม **ยืนยันนำเข้า** | — | disabled (ผ่าน 0 แถว) | ☐ |
| 3 | (แทน postal) UPLOAD plot_badaddr.csv → VERIFY | — | "ไม่พบตำบลในท่าม่วง" (สะกด "วังขนายย") · "ไม่พบจังหวัดในระบบ" (province "นครปฐม") — postal auto จากตำบล; ถ้าตำบลไม่ตรงจึงไม่มี postal 5 หลัก | ☐ |

### TC-I06 — โควตาไม่พบใน CSV (negative — ERR_QUOTA_NOT_FOUND)
- group: I · ความสำคัญ: กลาง · trace: AC-02b (CSV) / BR-AGP-01
- Setup: role=Field Officer · seed=default · files=`plot_badquota.csv` (แถว 2 quota QT-9999)
- Start: OPEN `#/plots` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD plot_badquota.csv | — | preview: ผ่าน 1 / ไม่ผ่าน 1 — "แถว 3" quota_no **ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก** | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (1 แถว)** → WAIT | — | สร้างเฉพาะแถวที่ผูกโควตาถูก · toast **นำเข้าแปลง 1 รายการสำเร็จ — ข้าม 1 แถว** | ☐ |

### TC-I07 — เลขที่เอกสารซ้ำ (ในไฟล์ + ในระบบ) (edge — BR-AGP-09 / EC-06)
- group: I · ความสำคัญ: กลาง · trace: VR-07 / BR_DEED_DUPLICATE
- Setup: role=Field Officer · seed=default · files=`plot_dupfile.csv`, `plot_dupdb.csv`
- Start: OPEN `#/plots` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD plot_dupfile.csv | — | preview: ผ่าน 2 / ไม่ผ่าน 1 — แถวหลังของคู่ซ้ำ error **เลขที่เอกสารสิทธิ์ซ้ำ (ภายในไฟล์ แถว N)** | ☐ |
| 2 | CLICK **เลือกไฟล์** → UPLOAD plot_dupdb.csv | — | preview ใหม่: ผ่าน 1 / ไม่ผ่าน 1 — แถว deed 12345 error **เลขที่เอกสารสิทธิ์ซ้ำ** (ซ้ำ seed PLT-001) | ☐ |

### TC-I08 — ไฟล์ถูกทั้งหมด + postal auto (happy — AC-14 / BR-AGP-03)
- group: I · ความสำคัญ: กลาง · trace: AC-14 / VR-10 (auto) / ทุกแถว Waiting for verify
- Setup: role=Field Officer · seed=default · files=`plot_ok.csv` (3 แถว ไม่มีคอลัมน์ postal)
- Start: OPEN `#/plots` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD plot_ok.csv | — | preview: ผ่าน 3 / ไม่ผ่าน 0 + แถบ **ทุกแถวผ่านการตรวจสอบ ไม่มีข้อผิดพลาด** | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (3 แถว)** → WAIT | — | phase done: สร้างสำเร็จ 3 + แถบ **นำเข้าสำเร็จทั้งหมด ไม่มีข้อผิดพลาด · ทุกแถวสถานะ "รอตรวจสอบ"** + toast เขียว **นำเข้าแปลง 3 รายการสำเร็จ** | ☐ |
| 3 | CLICK **ปิด** → CLICK แถวแปลงใหม่คนแรก | — | detail: ที่อยู่แปลง รหัสไปรษณีย์ เติมอัตโนมัติจากตำบล (5 หลัก) · pill **รอตรวจสอบ** · farmer snapshot = โควตาที่ผูก | ☐ |

### TC-I09 — แถวไม่มี shapefile_url → error (negative — AC-16b / LOCK-05 / G1)
- group: I · ความสำคัญ: สูง · trace: AC-16b / VR-06 / BR-AGP-13 / shapefile บังคับใน CSV
- Setup: role=Field Officer · seed=default · files=`plot_noshape.csv` (แถว 2 คอลัมน์ `shapefile_url` ว่าง)
- Start: OPEN `#/plots` → CLICK **Import CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD plot_noshape.csv | — | preview: ผ่าน 1 / ไม่ผ่าน 1 — "แถว 3" shapefile_url **กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)** (แถวเสีย จะถูกข้าม) | ☐ |
| 2 | CLICK **ยืนยันนำเข้า (1 แถว)** → WAIT | — | สร้างเฉพาะแถวที่มี shapefile_url · toast **นำเข้าแปลง 1 รายการสำเร็จ — ข้าม 1 แถว** · แถวที่สร้างมี shapefile ครบ (LOCK-05 ไม่ถูกละเมิด) | ☐ |

---

## Group V — ตรวจสอบยืนยัน เดี่ยว (OV-03)

### TC-V01 — Verify Pass เดี่ยว (happy — AC-18 / LOCK-08)
- group: V · ความสำคัญ: สูง · trace: AC-18 / US-05 / BR-AGP-04
- Setup: role=Data Steward (prototype: user เดียวกดได้) · seed=default (PLT-2569-003 waiting) · files=—
- Start: OPEN `#/plots/PLT-2569-003`
- ผ่านเมื่อ: pill เปลี่ยนเขียว + ประวัติ event ผ่าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer + ปุ่ม | — | หัวข้อ **PLT-2569-003** + pill เหลือง **รอตรวจสอบ** + ปุ่ม **แก้ไข / ตรวจสอบ / ลบ** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบ** | — | modal **ตรวจสอบแปลง** — subtitle "เลือกผลการตรวจสอบ · หากไม่ผ่านต้องระบุเหตุผล" + เลขแปลง + เกษตรกร + โควตา + เลขที่เอกสาร + radio 2 (ผ่าน/ไม่ผ่าน) | ☐ |
| 3 | CLICK ตัวเลือก **ผ่าน** | — | ตัวเลือกไฮไลต์เขียว · ไม่มีช่องเหตุผล (ไม่ต้องกรอกเมื่อผ่าน) | ☐ |
| 4 | CLICK ปุ่ม **ยืนยัน** | — | ปุ่มเป็น **กำลังดำเนินการ…** | ☐ |
| 5 | WAIT จน toast ปรากฏ | — | toast เขียว **ยืนยันเรียบร้อย** + pill ใน drawer/ตารางเปลี่ยนเป็นเขียว **ตรวจแล้ว** · การ์ดตรวจแล้ว = 3 | ☐ |
| 6 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ผ่าน** (จุดเขียว) โดย ธนพล ตรวจสอบ | ☐ |

### TC-V02 — Verify Fail ไม่กรอกเหตุผล → block (negative — AC-19 / VR-09 / EC-07)
- group: V · ความสำคัญ: สูงสุด · trace: AC-19 / BR-AGP-04 / BR_VERIFY_FAIL_NO_REASON / LOCK-08
- Setup: role=Data Steward · seed=default (PLT-2569-004 waiting) · files=—
- Start: OPEN `#/plots/PLT-2569-004` → CLICK **ตรวจสอบ**
- ผ่านเมื่อ: กด ไม่ผ่าน + เหตุผลว่าง → block (ต่างจาก reason ไม่บังคับใน delete)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวเลือก **ไม่ผ่าน** | — | ไฮไลต์แดง · ปรากฏช่อง **เหตุผลที่ไม่ผ่าน** มี * (บังคับ) placeholder "ระบุเหตุผลที่ไม่ผ่านการตรวจสอบ..." | ☐ |
| 2 | CLICK ปุ่ม **ยืนยัน** โดย **ไม่กรอกเหตุผล** | — | **block** + ข้อความแดงใต้ช่องเหตุผล **กรุณากรอกเหตุผล** + toast เหลืองข้อความเดียวกัน — ไม่เปลี่ยนสถานะ | ☐ |

### TC-V03 — Verify Fail พร้อมเหตุผล (happy — AC-20)
- group: V · ความสำคัญ: สูง · trace: AC-20 / LOCK-02 / legacy TC-459
- Setup: role=Data Steward · seed=default (PLT-2569-004 waiting) · files=—
- Start: OPEN `#/plots/PLT-2569-004` → CLICK **ตรวจสอบ** → CLICK **ไม่ผ่าน**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "เอกสารสิทธิ์ไม่ครบ ขอฉบับใหม่" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ทำเครื่องหมายไม่ผ่านแล้ว** + pill แดง **ไม่ผ่าน** | ☐ |
| 2 | VERIFY Tab **ข้อมูลทั่วไป** (ท้ายกลุ่ม) | — | กล่องแดง **เหตุผลที่ไม่ผ่าน: เอกสารสิทธิ์ไม่ครบ ขอฉบับใหม่** | ☐ |
| 3 | CLICK Tab **ประวัติ** | — | รายการบนสุด **ตรวจสอบ — ไม่ผ่าน** (จุดแดง) + note "เอกสารสิทธิ์ไม่ครบ ขอฉบับใหม่" โดย ธนพล ตรวจสอบ | ☐ |

### TC-V04 — ไม่เลือกผลตรวจสอบ (negative — VR-09)
- group: V · ความสำคัญ: กลาง · trace: VR-09 / "กรุณาเลือกผลการตรวจสอบ"
- Setup: role=Data Steward · seed=default (PLT-2569-002 waiting) · files=—
- Start: OPEN `#/plots/PLT-2569-002` → CLICK **ตรวจสอบ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยืนยัน** ทันที (ยังไม่เลือก radio) | — | ไม่ดำเนินการ + error ใต้ radio **กรุณาเลือกผลการตรวจสอบ** + toast เหลืองข้อความเดียวกัน | ☐ |

### TC-V05 — ปุ่มตรวจสอบซ่อนสำหรับ verified/failed (AC-23b)
- group: V · ความสำคัญ: กลาง · trace: AC-23b / BR-AGP-04 / §8 view actions
- Setup: role=Data Steward · seed=default · files=—
- Start: OPEN `#/plots/PLT-2569-005` (verified)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มบนหัว view drawer (PLT-005 ตรวจแล้ว) | — | มี **แก้ไข + ลบ** — **ไม่มีปุ่ม ตรวจสอบ** (verified) | ☐ |
| 2 | OPEN `#/plots/PLT-2569-007` (failed) → VERIFY ปุ่ม | — | เช่นเดียวกัน: มี แก้ไข + ลบ · ไม่มี ตรวจสอบ | ☐ |
| 3 | VERIFY ตาราง: checkbox แถว PLT-005/006/007/008 | — | checkbox จาง กดไม่ได้ (title "เลือกได้เฉพาะรายการรอตรวจสอบ") — verify ซ้ำผ่าน UI ไม่ได้ · ส่วน 409 server = TC-S02 (simulate) | ☐ |

---

## Group B — Bulk verify (OV-03)

### TC-B01 — Bulk เลือกทั้งหมด = เฉพาะ waiting + Pass (happy — AC-21 / EC-08)
- group: B · ความสำคัญ: สูง · trace: AC-21 / EC-08 / US-06 / BR-AGP-07 / legacy TC-470
- Setup: role=Data Steward · seed=default (waiting 4) · files=—
- Start: OPEN `#/plots`
- ผ่านเมื่อ: เลือกทั้งหมดติ๊กเฉพาะ waiting + summary

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY checkbox รายแถว | — | แถว **ตรวจแล้ว/ไม่ผ่าน** (PLT-005/006/007/008) checkbox จาง กดไม่ได้ · แถว **รอตรวจสอบ** (001..004) กดได้ | ☐ |
| 2 | CLICK checkbox หัวตาราง | — | ติ๊กเฉพาะ 4 แถว waiting · โผล่ bulk-bar "**เลือก 4 รายการ (รอตรวจสอบ)**" + ปุ่มหัวเปลี่ยนเป็น **ตรวจสอบที่เลือก (4)** (enabled) | ☐ |
| 3 | CLICK **ตรวจสอบที่เลือก (4)** | — | modal **ตรวจสอบแปลง (4 รายการ)** + list "รายการที่เลือก (4 รายการ)" แสดง เลขแปลง + ชื่อ + โควตา ครบ 4 + help "ใช้เหตุผลเดียวกันทุกรายการ (เมื่อเลือก \"ไม่ผ่าน\")" | ☐ |
| 4 | CLICK **ผ่าน** → CLICK ปุ่ม **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** | ☐ |
| 5 | VERIFY ตาราง + stats | — | ไม่มีแถว pill เหลืองเหลือ · การ์ด **รอตรวจสอบ 0** · **ตรวจแล้ว 6** · ปุ่มหัวกลับเป็น (0) disabled | ☐ |

### TC-B02 — Bulk Fail = เหตุผลเดียวทุกรายการ (AC-22 / LOCK-09 / VR-09)
- group: B · ความสำคัญ: สูง · trace: AC-22 / BR-AGP-05 / legacy TC-471
- Setup: role=Data Steward · seed=default (waiting 4) · files=—
- Start: OPEN `#/plots` → เลือกทั้งหมด (4 waiting) → CLICK **ตรวจสอบที่เลือก (4)**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่ผ่าน** โดยไม่กรอกเหตุผล → CLICK **ยืนยัน** | — | block + **กรุณากรอกเหตุผล** + note "ใช้เหตุผลเดียวกันนี้กับทุกรายการที่เลือก" | ☐ |
| 2 | TYPE "พิกัดไม่ตรงเอกสาร" → ช่องเหตุผล → CLICK **ยืนยัน** → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ 4 ล้มเหลว 0** · ทุกแถวที่เลือก pill แดง **ไม่ผ่าน** | ☐ |
| 3 | OPEN แปลงหนึ่งใน 4 → Tab ข้อมูลทั่วไป | — | กล่อง **เหตุผลที่ไม่ผ่าน: พิกัดไม่ตรงเอกสาร** (เหตุผลเดียวกันทุกใบ) | ☐ |

### TC-B03 — Bulk partial (บางรายการ verified ก่อน) (edge — AC-23 / EC-09) (ต้อง simulate)
- group: B · ความสำคัญ: สูง · trace: AC-23 / EC-09 / retry · **prototype single-session: การเลือกกรองเฉพาะ waiting อยู่แล้ว จึง สำเร็จ=ทั้งหมด; per-record conflict (คนที่สอง verify ก่อน) = SIT**
- Setup: role=Data Steward · seed=default
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) เลือก waiting ทั้งหมด → Pass → ยืนยัน → WAIT | — | toast **ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ N ล้มเหลว 0** (ทุกใบ waiting จริง) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): บางใบถูก verify โดยผู้อื่นก่อน submit | — | summary "สำเร็จ X ล้มเหลว Y" — ใบที่ status เปลี่ยนแล้วถูกนับ ล้มเหลว + list retry (per-record 409 BR_STATUS_CONFLICT) | ☐ |

---

## Group E — แก้ไข + State machine (OV-02 — LOCK-07)

### TC-E01 — แก้ไขแปลง waiting → status คงเดิม + version++ (happy — AC-11)
- group: E · ความสำคัญ: สูง · trace: AC-11 / US-07 / BR-AGP-06 / legacy TC-460
- Setup: role=Field Officer · seed=default (PLT-2569-003 waiting) · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ ท้ายแถว PLT-2569-003 | — | drawer **แก้ไขแปลง PLT-2569-003** · sub "สถานะ: รอตรวจสอบ · เวอร์ชัน 1" · แถบ info **โควตา QT-2569-002 · สุรพล เก่งการไร่ — แก้ไขการผูกไม่ได้ในหน้านี้** + แถบ warn **แก้ไขข้อมูลแล้วสถานะคงเดิม** · ทุกช่องมีค่าเดิม | ☐ |
| 2 | TYPE แก้ช่อง **พื้นที่ (ไร่)** เป็น "26.50" | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** + แถว PLT-003 ยัง pill เหลือง **รอตรวจสอบ** (ไม่เปลี่ยนสถานะ) + พื้นที่ในตาราง = 26.50 | ☐ |
| 4 | OPEN `#/plots/PLT-2569-003` → Tab **ประวัติ** | — | มี event **แก้ไขข้อมูล** เพิ่มบนสุด · footer "เวอร์ชัน 2" | ☐ |

### TC-E02 — แก้ไข Verified → **ยังคง ตรวจแล้ว** (AC-13 / EC-10 / OQ-P1) ★
- group: E · ความสำคัญ: สูงสุด · trace: AC-13 / EC-10 / BR-AGP-06 / legacy TC-462 (allow — pending-spec resolved OQ-P1)
- Setup: role=Field Officer · seed=default (PLT-2569-005 verified) · files=—
- Start: OPEN `#/plots/PLT-2569-005`
- ผ่านเมื่อ: แก้แล้วบันทึก → สถานะยัง **ตรวจแล้ว** (ไม่กลับ waiting อัตโนมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **แก้ไข** (verified มีปุ่มแก้ไข) | — | drawer แก้ไข · sub "สถานะ: ตรวจแล้ว · เวอร์ชัน N" · แถบ "แก้ไขข้อมูลแล้วสถานะคงเดิม" | ☐ |
| 2 | TYPE แก้ช่อง **ที่อยู่** → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** | ☐ |
| 3 | VERIFY แถว PLT-2569-005 ในตาราง | — | pill **ยังเป็นเขียว ตรวจแล้ว** (ไม่กลับ รอตรวจสอบ) · การ์ดตรวจแล้วยัง 2 | ☐ |

### TC-E03 — แก้ไข Failed → ยังคง ไม่ผ่าน + fail_reason คงอยู่
- group: E · ความสำคัญ: สูง · trace: AC-13 / BR-AGP-06 / §5.2
- Setup: role=Field Officer · seed=default (PLT-2569-007 failed, reason "เอกสารสิทธิ์ไม่ชัดเจน · ต้องแนบฉบับใหม่") · files=—
- Start: OPEN `#/plots/PLT-2569-007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Tab ข้อมูลทั่วไป | — | pill แดง **ไม่ผ่าน** + กล่อง **เหตุผลที่ไม่ผ่าน: เอกสารสิทธิ์ไม่ชัดเจน · ต้องแนบฉบับใหม่** | ☐ |
| 2 | CLICK **แก้ไข** → TYPE แก้ช่อง **ชื่อเจ้าของตามเอกสาร** → CLICK **บันทึกการแก้ไข** → WAIT | — | toast **บันทึกการแก้ไขแล้ว** · pill ยังแดง **ไม่ผ่าน** (ไม่กลับ waiting) | ☐ |
| 3 | OPEN `#/plots/PLT-2569-007` → Tab ข้อมูลทั่วไป | — | กล่อง **เหตุผลที่ไม่ผ่าน** ยังคงอยู่ (fail_reason ไม่ถูกเคลียร์) | ☐ |

### TC-E04 — แก้แล้วชนเลขเอกสารซ้ำ (negative — VR-07 exclude self)
- group: E · ความสำคัญ: กลาง · trace: VR-07 / BR_DEED_DUPLICATE / BR-AGP-09
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK ดินสอแถว PLT-2569-003

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกการแก้ไข** โดยไม่แก้อะไร | — | บันทึกสำเร็จ (เลขเอกสารเดิมของตัวเอง **ไม่**นับเป็นซ้ำ — exclude self) | ☐ |
| 2 | CLICK ดินสอแถว PLT-2569-003 อีกครั้ง → TYPE เลขที่เอกสารเป็น "12345" (ของ PLT-001) แล้ว blur → CLICK **บันทึกการแก้ไข** | — | ไม่บันทึก + error ใต้ช่องเอกสาร **เลขที่เอกสารสิทธิ์ซ้ำ** | ☐ |

---

## Group D — ลบ (soft / hard — OV-04 — LOCK-10)

### TC-D01 — Soft delete แปลง waiting (happy — AC-26)
- group: D · ความสำคัญ: สูง · trace: AC-26 / BR-AGP-08 / US-08 / legacy TC-465
- Setup: role=Field Officer · seed=default (PLT-2569-004 waiting) · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า การ์ด **แปลงทั้งหมด** และ **รอตรวจสอบ** | — | บันทึก: ทั้งหมด=8, รอตรวจสอบ=4 (อ้างใน step 5) | ☐ |
| 2 | CLICK ไอคอนถังขยะ ท้ายแถว PLT-2569-004 | — | modal แดง **ลบแปลง?** + subtitle `ต้องการลบ "PLT-2569-004 — ทองดี พูลผล" ใช่หรือไม่` + radio **ลบชั่วคราว (Soft)** (default) / **ลบถาวร (Hard)** + ช่อง **เหตุผล (ไม่บังคับ)** + note soft "รายการจะถูกซ่อน (soft delete) และบันทึกลงประวัติ" | ☐ |
| 3 | คง radio **ลบชั่วคราว** → CLICK ปุ่ม **ลบแปลง** (แดง) | — | ปุ่มเป็น **กำลังลบ…** | ☐ |
| 4 | WAIT จน toast ปรากฏ | — | toast **ลบแปลงแล้ว** + แถว PLT-2569-004 หายจากตาราง | ☐ |
| 5 | VERIFY stats | — | ทั้งหมด=7 · รอตรวจสอบ=3 — soft-deleted ไม่นับ | ☐ |
| 6 | OPEN `#/plots/PLT-2569-004` (route ตรง) | — | ไม่เปิด detail — toast **ไม่พบข้อมูลแปลงที่เลือก** + เด้งกลับ `#/plots` | ☐ |

### TC-D02 — Hard delete → ลบถาวร (AC-27)
- group: D · ความสำคัญ: สูง · trace: AC-27 / BR-AGP-08 / legacy TC-466
- Setup: role=Field Officer · seed=default (PLT-2569-002 waiting) · files=—
- Start: OPEN `#/plots` → CLICK ถังขยะ แถว PLT-2569-002

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK radio **ลบถาวร (Hard)** | — | note เปลี่ยนเป็นแดง **การลบถาวรไม่สามารถกู้คืนได้** | ☐ |
| 2 | TYPE "ข้อมูลผิด สร้างซ้ำ" → เหตุผล → CLICK **ลบแปลง** → WAIT | — | toast **ลบแปลงแล้ว** + แถว PLT-002 หาย · count = 7 รายการ | ☐ |
| 3 | OPEN `#/plots/PLT-2569-002` | — | toast **ไม่พบข้อมูลแปลงที่เลือก** + กลับ list (ลบถาวรออกจาก records) | ☐ |

### TC-D03 — ลบแปลง verified via view drawer (edge — EC-11 / OQ-P2)
- group: D · ความสำคัญ: กลาง · trace: EC-11 / BR-AGP-08 / legacy TC-467 (allow — pending-spec resolved OQ-P2) · **หมายเหตุ: ในตาราง แถว verified/failed ไม่มีไอคอนถังขยะ (เฉพาะ waiting); ปุ่มลบอยู่ใน view drawer**
- Setup: role=Field Officer · seed=default (PLT-2569-006 verified) · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **การดำเนินการ** แถว PLT-2569-006 (ตรวจแล้ว) ในตาราง | — | มีเฉพาะไอคอนดินสอ — **ไม่มีถังขยะ** (list ลบเฉพาะ waiting) | ☐ |
| 2 | CLICK แถว PLT-2569-006 → VERIFY ปุ่มหัว view drawer | — | มี **แก้ไข + ลบ** (view drawer อนุญาตลบทุกสถานะ — EC-11) | ☐ |
| 3 | CLICK ปุ่ม **ลบ** → CLICK **ลบแปลง** (soft) → WAIT | — | toast **ลบแปลงแล้ว** + drawer ปิด + แถว PLT-006 หาย · การ์ดตรวจแล้ว = 1 | ☐ |

### TC-D04 — Idempotent delete + deep-link หลังลบ (AC-27 / EC-17)
- group: D · ความสำคัญ: กลาง · trace: AC-27 / EC-17 / BR-AGP-11 / legacy TC-468
- Setup: role=Field Officer · seed=default (PLT-2569-001 waiting) · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ถังขยะ แถว PLT-2569-001 → CLICK **ลบแปลง** (soft) → WAIT | — | toast **ลบแปลงแล้ว** + แถวหาย | ☐ |
| 2 | PRESS F5 (refresh) | — | mock reset → seed กลับมา 8 แปลง (in-memory) — ยืนยันว่า refresh = reset (ทุกเคส independent) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): กดลบซ้ำ / refresh หลังลบ | — | DELETE idempotent — ไม่ duplicate audit, ไม่ error record ที่ลบไปแล้ว (BR-AGP-11) | ☐ |

---

## Group W — รายละเอียด / ประวัติ (P-02 — 3 tabs)

### TC-W01 — View detail 3 tabs + farmer snapshot card (AC-24 / BR-AGP-12)
- group: W · ความสำคัญ: สูง · trace: AC-24 / US-04 / cross-module farmer snapshot
- Setup: role=Field Officer · seed=default (PLT-2569-001 → QT-2569-001) · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว PLT-2569-001 | — | view drawer: eyebrow "แปลงที่ดิน · QT-2569-001" + หัวข้อ **PLT-2569-001** (mono) + pill เหลือง **รอตรวจสอบ** | ☐ |
| 2 | VERIFY farmer snapshot card (ใต้หัว) | — | การ์ด teal/ส้มอ่อน **ผูกกับโควตา · QT-2569-001 · สมหญิง รักดี · 0823456789** + ปุ่ม **ดูโควตา** | ☐ |
| 3 | VERIFY Tab **ข้อมูลทั่วไป** | — | 3 กลุ่ม: **ข้อมูลกรรมสิทธิ์** (ประเภท/เลขเอกสาร/วันที่/เจ้าของ) · **ที่อยู่แปลง** (ที่อยู่/จังหวัด/อำเภอ/ตำบล/รหัสไปรษณีย์) · **พิกัด & พื้นที่** (ละติจูด 14.023145 / ลองจิจูด 99.512088 · 6 ทศนิยม · พื้นที่ + ปุ่ม "เปิดแผนที่") | ☐ |
| 4 | CLICK ปุ่ม **ดูโควตา** | — | toast info **จำลองเปิดหน้าโควตา QT-2569-001** (prototype standalone — deep-link จริงตอน deploy รวม features · READ-ONLY) | ☐ |
| 5 | VERIFY footer drawer | — | "อัปเดตล่าสุด … · เวอร์ชัน N" + ปุ่ม **ปิด** | ☐ |

### TC-W02 — Timeline ประวัติครบทุก event (AC-25 / BR-AGP-07)
- group: W · ความสำคัญ: สูง · trace: AC-25 / audit append-only / legacy TC-500
- Setup: role=Field Officer · seed=default (PLT-2569-007 failed — create + verify_fail) · files=—
- Start: OPEN `#/plots/PLT-2569-007` → CLICK Tab **ประวัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY timeline | — | เรียงใหม่→เก่า: **ตรวจสอบ — ไม่ผ่าน** (จุดแดง + note "เอกสารสิทธิ์ไม่ชัดเจน · ต้องแนบฉบับใหม่" + โดย ธนพล ตรวจสอบ) → **สร้างแปลง** (โดย สมพร วงศ์ทะเบียน + note "ผูกกับโควตา QT-2569-005 · สมพงษ์ ทองแท้") — ทุกรายการมีวันเวลา | ☐ |

### TC-W03 — Deep-link refresh-safe + missing (AC-25b / EC-17)
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / refresh-safe / ERR_NOT_FOUND / legacy TC-456
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots/PLT-2569-005` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/plots/PLT-2569-005` | — | หน้า list โหลด + view drawer **PLT-2569-005** เปิดเองทันที | ☐ |
| 2 | PRESS F5 (refresh ทั้งหน้า) | — | กลับมาที่เดิม — drawer PLT-2569-005 ยังเปิด (refresh-safe) | ☐ |
| 3 | OPEN `#/plots/PLT-9999-999` (ไม่มีในระบบ) | — | toast แดง **ไม่พบข้อมูลแปลงที่เลือก** + เด้งกลับ `#/plots` (ไม่มี drawer) | ☐ |

### TC-W04 — Files tab + fail reason note (AC-24 / AC-20 / BR-AGP-13)
- group: W · ความสำคัญ: กลาง · trace: AC-24 / LOCK-05 · shapefile/document download
- Setup: role=Field Officer · seed=default (PLT-2569-008 failed) · files=—
- Start: OPEN `#/plots/PLT-2569-008`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK Tab **ไฟล์ที่อัปโหลด** | — | การ์ด **ไฟล์ลักษณะแปลง (Shapefile)** (มี link ดาวน์โหลด — seed มี shapefile) · **เอกสารสิทธิ์ — ไม่มีไฟล์** (document optional เว้นว่าง) | ☐ |
| 2 | CLICK link ไฟล์ Shapefile | — | toast info **จำลองดาวน์โหลด [ชื่อไฟล์]** | ☐ |
| 3 | CLICK Tab **ข้อมูลทั่วไป** → เลื่อนท้าย | — | กล่องแดง **เหตุผลที่ไม่ผ่าน: พิกัดอยู่นอกเขตพื้นที่ที่ระบุในโควตา** | ☐ |

---

## Group X — Cross-module quota binding ⭐ (06_TESTS §6.9 — READ-ONLY, 1:N)

> Plot อ่าน Quota ผ่าน `QUOTAS` const + `findQuotaByNo()` — **ไม่มี write-back ไป Quota** (ต่างจาก Quota→Farmer ที่ writeMemberQuotaStatus) · พิสูจน์ได้บนจอผ่าน (ก) farmer snapshot card (read-only) (ข) ผูกหลายแปลงต่อ 1 โควตาได้ (1:N) (ค) `QUOTAS` array ไม่ถูก mutate · การ reconcile ไป Quota/Farmer feature จริง = `(ต้อง simulate)` ที่ SIT

### TC-X01 — Quota search คืน verified quota + farmer snapshot read-only (XT-02)
- group: X · ความสำคัญ: สูงสุด · trace: XT-02 / AC-01 / BR-AGP-01 / LOCK-03
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ค้นหาโควตา → พิมพ์ "QT-2569" | — | dropdown แสดง **5 โควตา** (ทั้งหมด verified) — option = `[QT] · [ชื่อ]` + sub `[เบอร์] · [เลขบัตร masked]` | ☐ |
| 2 | CLICK **QT-2569-004 · ประนอม ใจเพชร** | — | การ์ด teal farmer snapshot: QT-2569-004 · ประนอม ใจเพชร · 0833334444 · เลขบัตร 4-XXXX-XXXX-XX-3 (masked, read-only) · ฟิลด์ปลดล็อก | ☐ |
| 3 | VERIFY การ์ด farmer | — | ข้อมูลเกษตรกร **แก้ไม่ได้** (แสดงอย่างเดียว) — ปุ่ม **เปลี่ยนโควตา** เท่านั้น | ☐ |

### TC-X02 — สร้างแปลงผูก quota → quota_no set · quota ไม่ถูกแก้ (XT-01 / XT-05) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-02 / BR-AGP-01 / §0.14 no write-back
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-004 · ประนอม ใจเพชร** → กรอกฟิลด์ครบ (deed 78905) + Shapefile → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างแปลงสำเร็จ — [เลขแปลง]** · แถวใหม่ แสดงเลขโควตา QT-2569-004, ชื่อ ประนอม ใจเพชร (snapshot จาก quota) | ☐ |
| 2 | CLICK แถวใหม่ → VERIFY farmer card | — | ผูกกับโควตา QT-2569-004 · ประนอม ใจเพชร · 0833334444 — ตรง quota ต้นทาง | ☐ |
| 3 | พิสูจน์ READ-ONLY: CLICK **สร้างแปลง** อีกครั้ง → ค้นหา → เลือก **QT-2569-004** | — | **เลือกได้ตามปกติ** (ไม่ขึ้น "มีโควตาแล้ว" — Quota ไม่ถูก mutate เป็น has_plot) — ต่างจาก Quota→Farmer 1:0..1 | ☐ |
| 4 | VERIFY (ระบบจริง — SIT) | — | เปิด Quota feature `#/quotas/QT-2569-004` → โควตา **ไม่มี field/สถานะที่เปลี่ยน** จากการผูกแปลง (read-only ENG-EXT-Q01) | ☐ |

### TC-X03 — 1 quota : N plots (ผูกแปลงที่ 3 บน QT-2569-001) (XT-03) ★ signature
- group: X · ความสำคัญ: สูงสุด · trace: XT-03 / BR-AGP-02 / LOCK-06
- Setup: role=Field Officer · seed=default (QT-2569-001 ผูก PLT-001 + PLT-002 อยู่แล้ว) · files=—
- Start: OPEN `#/plots` → CLICK **สร้างแปลง**
- ผ่านเมื่อ: ผูกแปลงที่ 3 บนโควตาเดิมได้ ไม่มี block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QT-2569-001 · สมหญิง รักดี** (มี 2 แปลงผูกอยู่แล้ว) | — | การ์ด farmer snapshot ปรากฏ **ไม่มี block "มีโควตาแล้ว"** (1:N — ต่างจาก Quota 1:0..1) | ☐ |
| 2 | กรอกฟิลด์ครบ (deed 78910) + Shapefile → CLICK **ยืนยันสร้าง** → WAIT | A | toast **สร้างแปลงสำเร็จ — [เลขแปลง]** | ☐ |
| 3 | CLICK **ล้างตัวกรอง** แล้ว TYPE "QT-2569-001" → ช่องค้นหา (list) | — | ตารางแสดง **3 แถว** ผูกโควตา QT-2569-001 (PLT-001, PLT-002, แปลงใหม่) — พิสูจน์ 1 quota : N plots | ☐ |

### TC-X04 — quota ถูกลบหลังผูก → snapshot fallback (XT-04 / EC-18) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-04 / EC-18 / §0.14 · **prototype: `QUOTAS` เป็น const ลบไม่ได้ — SIT case · code path มี fallback: ถ้า findQuotaByNo คืน null → การ์ดเทา "โควตา [x] ถูกลบหลังผูก — คงหมายเลขโควตาไว้ (snapshot)"**
- Setup: role=Field Officer · **simulate — ระบบจริง:** แปลง linked กับ quota ที่ถูกลบภายหลัง
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): เปิด detail แปลงที่ quota ถูกลบ | — | แทน farmer card teal → การ์ดเทา **โควตา [QT] ถูกลบหลังผูก — คงหมายเลขโควตาไว้ (snapshot)** (ไม่มีปุ่มดูโควตา) · plot ยังอยู่ ไม่ error ไม่ cascade delete | ☐ |
| 2 | VERIFY: quota_no snapshot | — | plot คงหมายเลขโควตาไว้ + flag anomaly (คู่ plot↔quota ไม่ตรง) — ไม่ปล่อยเงียบ | ☐ |

### TC-X05 — Assert ไม่มี write-back ไป Quota (READ-ONLY invariant)
- group: X · ความสำคัญ: สูง · trace: §0.14 / XT-01 / D-02 Drift
- Setup: role=Field Officer · seed=default · files=—
- Start: OPEN `#/plots`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้างแปลงผูก QT-2569-002 (ตามชุด A) → WAIT toast | — | สร้างสำเร็จ · **ไม่มี toast/history event ประเภท "อัปเดตสถานะโควตา"** (ต่างจาก Quota→Farmer ที่มี write-back) | ☐ |
| 2 | CLICK แปลงใหม่ → Tab **ประวัติ** | — | มีเฉพาะ event **สร้างแปลง** — ไม่มี cross-module write event (Plot อ่าน Quota อย่างเดียว) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT) | — | ตรวจ Quota record ก่อน/หลังผูกแปลง = **ไม่เปลี่ยน** (ENG-EXT-Q01 GET only, ไม่มี PATCH) | ☐ |

---

## Group S — System / simulate (optimistic lock · concurrency · SoD)

### TC-S01 — Optimistic lock stale edit → 409 (edge — AC-12 / EC-12) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-12 / EC-12 / VR-11 / ERR_STALE_DATA / BR-AGP-11 / legacy TC-486 · **prototype single-session ทำไม่ได้ (Drift D-03) — SIT case · idempotency double-click ตรวจแล้วใน TC-C12**
- Setup: **simulate — ระบบจริง:** 2 sessions — A แก้ record + save ก่อน, B ที่เปิดค้างไว้ save ทีหลังด้วย expected_version เก่า
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B กด **บันทึกการแก้ไข** หลัง A save ไปแล้ว | — | 409 + toast แดง **ข้อมูลล้าสมัย กรุณารีเฟรช** — ข้อมูลของ A ไม่ถูกทับ | ☐ |

### TC-S02 — Concurrent verify status changed → 409 (edge — AC-23b / EC-13) (ต้อง simulate)
- group: S · ความสำคัญ: สูง · trace: AC-23b / EC-13 / BR_STATUS_CONFLICT / legacy TC-489 · **prototype UI ซ่อนปุ่มตรวจสอบสำหรับ verified/failed (TC-V05) — ส่วน 409 server = SIT**
- Setup: **simulate — ระบบจริง:** A verify record ก่อน, B verify record เดิม (status เปลี่ยนแล้ว)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B POST verify กับ record ที่ A เพิ่ง verify | — | 409 + **สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช** — สถานะที่ A ตั้งไว้คงเดิม | ☐ |

### TC-S03 — Server-side validation + duplicate-deed race + len guard (TC-463/485/488/501) (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: VR-11 / EC-06 / BR-AGP-09 · **duplicate-deed policy = pending-spec (TC-501) · address_line/deed_owner ≤255 (TC-463) · UI passes → server reject (TC-488)**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): 2 request สร้างแปลง deed เดียวกันพร้อมกัน (race) | — | server unique constraint → 1 สำเร็จ, อีก 1 ได้ **เลขที่เอกสารสิทธิ์ซ้ำ** (policy ต้องเคาะ — TC-501 pending) | ☐ |
| 2 | VERIFY (ระบบจริง): กรอก address_line/deed_owner > 255 อักขระ | — | server reject "ความยาวเกิน" (VR-11) + inline error แม้ UI ปล่อยผ่าน (TC-488) | ☐ |

### TC-S04 — SoD: ผู้สร้างห้าม verify ตัวเอง / RBAC hide (TC-490) (ต้อง simulate)
- group: S · ความสำคัญ: กลาง · trace: §5.3 SoD (OQ-P7) / permission matrix / legacy TC-490 · **prototype ไม่มี role switching — Field Officer/Steward เป็น user เดียว — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง:** feature flag SoD + RBAC
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — RBAC): login เป็น Field Officer | — | ปุ่ม **ตรวจสอบ / ตรวจสอบที่เลือก** ถูกซ่อน (verify = Admin/Steward เท่านั้น) | ☐ |
| 2 | VERIFY (ระบบจริง — SoD flag ON): Steward verify แปลงที่ตนเองสร้าง | — | block 403 + ข้อความ SoD (ผู้สร้างไม่ควรตรวจสอบเอง) · flag OFF → ผ่านแต่ log anomaly | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `plot-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed 8 แปลง + 5 โควตา (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/UPLOAD/PRESS/WAIT/VERIFY)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast มุมขวาล่าง · create/verify/delete 0.6–0.7s · import 0.9s + toast 4.5s — อ่านทันทีที่โผล่)
5. **quota binding บังคับ:** ทุกเคสสร้าง/negative ที่ต้องกรอกฟิลด์แปลง ต้อง **เลือกโควตาก่อน** (ฟิลด์ล็อกจนกว่าเลือก) — ยกเว้นเคสที่ทดสอบ gating เอง (TC-C02/C03/C04)
6. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
7. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"
8. ไฟล์ทดสอบทั้งหมด (CSV/xlsx) ต้องอยู่ในโฟลเดอร์ที่ agent เข้าถึงได้ก่อนเริ่ม (ดู Data Sets → Files) · header CSV = 13 คอลัมน์ (มี shapefile_url บังคับ · ไม่มี postal — auto จากตำบล)
9. จบทุกเคส → กรอก Result Report ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 28 / 28 (AC-01..28 + AC-02b/AC-23b/AC-25b) |
| Cross-Module (XT-01..04) | 4 / 4 (XT-04 simulate) + X05 read-only assertion |
| Business rules (BR-AGP-01..13) | 13 / 13 |
| Validation (VR-01..12) | 12 / 12 |
| Edge cases (EC-01..18) | 18 / 18 (EC-09/12/13/18 simulate/SIT) |
| Error codes (UI-observable) | 13 / 13 (ERR_STALE_DATA / BR_STATUS_CONFLICT = simulate) |
| Permission cells | Field Officer / Steward allow ครบ · RBAC deny / SoD = TC-S04 (simulate) |
| Scope Lock (LOCK-01..12) | 12 / 12 — ทุก LOCK มีเคส verify |
| Legacy TC-446..501 (56 เคส) | mapped 100% (server-only/pending-spec → simulate group S) |

- **Manifest cross-check (FRD §0.12): ✅ 10 Stories + 13 Rules + 12 VR + 18 EC + 4 XT — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT (7 เคส)
- TC-P07 (export CSV — ไม่มี UI ใน prototype)
- TC-B03 (bulk partial per-record conflict)
- TC-X04 (quota ถูกลบหลังผูก — QUOTAS เป็น const)
- TC-S01 (optimistic lock 409 — single session)
- TC-S02 (concurrent verify 409)
- TC-S03 (server unique race + len guard + duplicate-deed policy pending)
- TC-S04 (SoD / RBAC — ไม่มี role switching)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-003",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-P01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 56, "pass": 0, "fail": 0, "blocked": 0 }
}
```
