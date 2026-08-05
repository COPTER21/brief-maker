# Tax Code HTML Coverage Map

| Scope / Rule | UI hook | Behavior |
|---|---|---|
| Preset VAT/WHT | VAT/WHT tabs และ 7 preset records | มี preset VAT7, VAT0, VAT-EX, WHT1/2/3/5 |
| Company scope | company context ใน shell | records และ GL lookup กรองด้วย `COMP-001` |
| Unique code | create/edit drawer | ตรวจซ้ำแบบ case-insensitive ภายในบริษัท |
| GL ก่อนเปิดใช้ | master combobox + validation | บันทึกร่างได้ แต่ activate ไม่ได้หาก GL ไม่ครบ |
| VAT model | family/kind/direction fields | standard/zero/exempt และ sale/purchase/both |
| WHT income category | searchable income type | ไม่ผูกแบบ ภ.ง.ด.; resolve downstream |
| Effective date | start/end fields + picker date | start ต้องมี, end ≥ start, picker ตรวจทั้งสองขอบ |
| Used-rate immutability | edit drawer ของ used record | rate disabled และมี action “สร้างรหัสแทน” |
| Replacement lineage | replacement flow + view drawer | `replacesTaxCodeId`, `replacedByTaxCodeId`, ปิดช่วงรหัสเดิม |
| No hard delete | row/view actions + confirmation | active → deactivate, draft → archive, ไม่มี delete mutation |
| Historical documents | picker snapshot panel | บันทึก tax id/code/name/rate/family/kind/direction/date |
| Audit | view drawer timeline | append-only event สำหรับ create/update/deactivate/archive/replacement |
| Permissions | action rendering + submit guards | create/update/activate/deactivate/audit แยกสิทธิ์ |
| Production route | hash initialization | `#/accounting/setup/tax-codes` |
| Empty/filter/sort | list toolbar/table | search, lifecycle filter, sortable columns, empty state/reset |

Preflight: `self_audit.py PASS`; `audit.sh FAIL=0`; browser route/create/picker/snapshot checks PASS.

