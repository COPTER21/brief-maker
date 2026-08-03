import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "testcases-vendor-price-list.md"
OUT = Path(__file__).resolve().parent / "cases.json"

GROUP_IDS = {
    "A": "g-a", "B": "g-b", "C": "g-c", "D": "g-d",
    "E": "g-e", "F": "g-f", "G": "g-g", "H": "g-h",
}

ROLE_MAP = {
    "procurement_officer": "เจ้าหน้าที่จัดซื้อ",
    "procurement_manager": "ผู้จัดการฝ่ายจัดซื้อ",
    "procurement_director": "ผู้อำนวยการฝ่ายจัดซื้อ",
    "finance_viewer": "ผู้ใช้งานฝ่ายการเงินที่ดูข้อมูลได้",
    "admin": "ผู้ดูแลระบบ",
    "other authenticated": "ผู้ใช้งานทั่วไปที่เข้าสู่ระบบแล้ว",
    "downstream service": "ส่วนงานที่นำราคาไปใช้ต่อ",
    "two authorized sessions": "ผู้อนุมัติสองคนที่เปิดรายการเดียวกัน",
    "DS-ROLE each": "บัญชีทดสอบทุกระดับสิทธิ์",
}

ROUTE_NAMES = {
    "#/vendor-price-list": "รายการราคาคู่ค้า",
    "#/vendor-price-list/batch": "กรอกหลายรายการ",
    "#/vendor-price-list/compare": "เปรียบเทียบราคา",
    "#/vendor-price-list/vendor/{vendorId}": "รายการราคาของคู่ค้าที่เลือก",
}

TECH_REPLACEMENTS = [
    (r"DS-UI", "ชุดข้อมูลหน้าต้นแบบ"),
    (r"DS-MASTER", "ชุดข้อมูลหลัก"),
    (r"DS-PRICE", "ชุดรายการราคา"),
    (r"DS-FX", "ชุดอัตราแลกเปลี่ยน"),
    (r"DS-XT", "ชุดข้อมูลเชื่อมโยง"),
    (r"DS-CONC", "ชุดข้อมูลหลายผู้ใช้"),
    (r"DS-ROLE", "ชุดบัญชีผู้ใช้ทดสอบ"),
    (r"\bAPI(?:-\d+)?\b", "ระบบเบื้องหลัง"),
    (r"\bDB\b", "ฐานข้อมูล"),
    (r"\bRLS\b", "การจำกัดสิทธิ์ข้อมูล"),
    (r"\bETag\b", "ข้อมูลรุ่นเดียวกัน"),
    (r"\bWORM\b", "ประวัติที่แก้ย้อนหลังไม่ได้"),
    (r"\bidempotenc(?:y|e)\b", "การส่งคำขอซ้ำโดยไม่สร้างรายการซ้ำ"),
    (r"\boptimistic concurrency\b", "การป้องกันข้อมูลชนกันเมื่อหลายคนทำพร้อมกัน"),
    (r"\bpayload\b", "ข้อมูลที่ระบบรับส่ง"),
    (r"\bfixtures?", "ข้อมูลทดสอบ"),
    (r"\bharness\b", "เครื่องมือทดสอบของทีมระบบ"),
    (r"\binject\b", "เตรียมสภาพทดสอบ"),
    (r"\bserver\b", "ระบบ"),
    (r"\brecords?\b", "รายการ"),
    (r"\bHeader\b", "รายการราคาหลัก"),
    (r"\bversion\b", "ฉบับราคา"),
    (r"\bactive\b", "ใช้งาน"),
    (r"\bpending(?:_approval)?\b", "รออนุมัติ"),
    (r"\bdraft\b", "ร่าง"),
    (r"\binactive\b", "ปิดใช้งาน"),
    (r"\bexternal ID\b", "รหัสอ้างอิงจากไฟล์"),
    (r"\bDOA\b", "สายอนุมัติตามวงเงิน"),
    (r"\bFX\b", "อัตราแลกเปลี่ยน"),
    (r"\bContract\b", "สัญญาที่อนุมัติแล้ว"),
    (r"\brole\b", "สิทธิ์ผู้ใช้"),
    (r"\bmask(?:ed|ing)?\b", "ปกปิดค่า"),
    (r"\btrace\b", "รายละเอียดการคำนวณ"),
    (r"\bbusiness clock\b", "เวลาจำลองของระบบ"),
    (r"\btier boundary\b", "ขอบช่วงปริมาณ"),
    (r"\boverlap\b", "ช่วงซ้อนกัน"),
    (r"\bmaster\b", "ข้อมูลหลัก"),
    (r"\brequest\b", "คำขอ"),
    (r"\bbody\b", "เนื้อหาคำขอ"),
    (r"\btenants?", "องค์กร"),
    (r"\bcompanies?", "บริษัท"),
    (r"\bsnapshot\b", "ข้อมูลที่บันทึก ณ เวลานั้น"),
    (r"\bcommit\b", "บันทึกข้อมูล"),
    (r"\bstale\b", "ล้าสมัย"),
    (r"\bmutation\b", "การเปลี่ยนข้อมูล"),
    (r"\bexplicit\b", "ที่ระบุชัดเจน"),
    (r"\bpolicy\b", "นโยบาย"),
    (r"\bconfig\b", "การตั้งค่า"),
    (r"\bretry\b", "ลองส่งซ้ำ"),
    (r"\bthreshold\b", "เกณฑ์"),
    (r"\bbaseline\b", "ค่าเริ่มต้น"),
    (r"\bcurrent\b", "ปัจจุบัน"),
    (r"\bsuccess\b", "สำเร็จ"),
    (r"\baction\b", "คำสั่ง"),
    (r"\bsummary\b", "สรุป"),
    (r"\bpreview\b", "ผลตรวจสอบก่อนนำเข้า"),
    (r"\broute\b", "หน้า"),
    (r"\bresolve\b", "เลือกใช้ราคา"),
    (r"\btier\b", "ช่วงปริมาณ"),
    (r"\binput\b", "ข้อมูลที่กรอก"),
    (r"\bsimulate\b", "ทดสอบด้วยเครื่องมือระบบ"),
    (r"\baudit\b", "ประวัติการตรวจสอบ"),
    (r"\blanded\b", "ต้นทุนรวมก่อนภาษี"),
    (r"\bchange\b", "การเปลี่ยนแปลง"),
    (r"\bapproval\b", "การอนุมัติ"),
    (r"\bstatus\b", "สถานะ"),
    (r"\bmaker\b", "ผู้สร้างรายการ"),
    (r"\bdate\b", "วันที่"),
    (r"\bdiscount\b", "ส่วนลด"),
    (r"\bfreight\b", "ค่าขนส่ง"),
    (r"\bsubmit\b", "ส่งข้อมูล"),
    (r"\bfallback\b", "ทางเลือกสำรอง"),
    (r"\bconfirm\b", "ยืนยัน"),
    (r"\bfocus\b", "จุดเลือกบนจอ"),
    (r"\bvalid\b", "ถูกต้อง"),
    (r"\binvalid\b", "ไม่ถูกต้อง"),
    (r"\bsession\b", "หน้าต่างผู้ใช้"),
    (r"\bdownstream\b", "ส่วนงานที่นำข้อมูลไปใช้ต่อ"),
    (r"\bservice\b", "ส่วนงานระบบ"),
    (r"\bidentity\b", "ข้อมูลระบุตัวรายการ"),
    (r"\bexternal\b", "จากภายนอก"),
    (r"\bprice\b", "ราคา"),
    (r"\bcurrency\b", "สกุลเงิน"),
    (r"\bproduct\b", "สินค้า"),
    (r"\bvendor\b", "คู่ค้า"),
    (r"\btwo\b", "สอง"),
    (r"\bblocks?", "ปิดกั้น"),
    (r"\bblocked\b", "ไม่พร้อมใช้งาน"),
    (r"\bcompare\b", "เปรียบเทียบราคา"),
    (r"\blist\b", "รายการ"),
    (r"\brows?\b", "แถว"),
    (r"\bstep\b", "ขั้น"),
    (r"\brefresh\b", "โหลดหน้าใหม่"),
    (r"\bview\b", "ดูข้อมูล"),
    (r"\belevated\b", "ต้องตรวจสอบเพิ่มเติม"),
    (r"\bstandard\b", "ขั้นตอนปกติ"),
    (r"\boutcome\b", "สรุปผล"),
    (r"\bconflict\b", "ข้อมูลขัดแย้ง"),
    (r"\bpill\b", "ป้ายสถานะ"),
    (r"\bformula\b", "สูตรคำนวณ"),
    (r"\bdropdown\b", "ช่องเลือกรายการ"),
    (r"\bmodal\b", "หน้าต่างยืนยัน"),
    (r"\bdrawer\b", "แผงด้านข้าง"),
    (r"\bbatch\b", "การกรอกหลายรายการ"),
    (r"\bprice_per\b", "ราคาต่อจำนวน"),
    (r"\bdirector\b", "ผู้อำนวยการ"),
    (r"\bcandidate(?:s)?\b", "ตัวเลือกราคา"),
    (r"\bescape\b", "Esc"),
    (r"\berror\b", "ข้อผิดพลาด"),
    (r"\bmanual\b", "กรอกเอง"),
    (r"\bex-tax\b", "ก่อนภาษี"),
    (r"\bstate\b", "สถานะ"),
    (r"\bconfidential\b", "ข้อมูลภายในบริษัท"),
    (r"\bdisabled\b", "กดไม่ได้"),
    (r"\bsearch\b", "ค้นหา"),
    (r"\bmissing\b", "ไม่มีข้อมูล"),
    (r"\bobsolete\b", "เลิกใช้งาน"),
    (r"\bempty\b", "ว่าง"),
    (r"\btransaction\b", "เอกสารรายการ"),
    (r"\bapproved\b", "อนุมัติแล้ว"),
    (r"\bscenario\b", "กรณีทดสอบ"),
    (r"\bcreate\b", "สร้าง"),
    (r"\bpurchasable\b", "สั่งซื้อได้"),
    (r"\brecheck\b", "ตรวจซ้ำ"),
    (r"\bbuild\b", "ชุดงานที่ส่งทดสอบ"),
    (r"\bboundary\b", "ค่าขอบเขต"),
    (r"\bfeature\b", "ความสามารถนี้"),
    (r"\bclient\b", "หน้าจอผู้ใช้"),
    (r"\bfield\b", "ช่องข้อมูล"),
    (r"\brequired\b", "จำเป็นต้องกรอก"),
    (r"\badmin\b", "ผู้ดูแลระบบ"),
    (r"\brate\b", "อัตรา"),
    (r"\bcode\b", "รหัส"),
    (r"\bscope\b", "ขอบเขตข้อมูล"),
    (r"\boverride\b", "ราคาที่ผู้มีสิทธิ์กำหนดเอง"),
    (r"\bmatrix\b", "ตารางสิทธิ์"),
    (r"\bschema\b", "รูปแบบคอลัมน์"),
    (r"\bprocurement_manager\b", "ผู้จัดการฝ่ายจัดซื้อ"),
    (r"\bprocurement_officer\b", "เจ้าหน้าที่จัดซื้อ"),
    (r"\bprocurement_director\b", "ผู้อำนวยการฝ่ายจัดซื้อ"),
    (r"\bfinance_viewer\b", "ผู้ใช้งานฝ่ายการเงินที่ดูข้อมูลได้"),
    (r"\bother authenticated\b", "ผู้ใช้งานทั่วไปที่เข้าสู่ระบบแล้ว"),
    (r"\bsame\b", "เดียวกัน"),
    (r"\bsource authority\b", "แหล่งอ้างอิงหลัก"),
    (r"\bbuy-side\b", "ราคาซื้อ"),
    (r"\bcanonical\b", "หลักที่ใช้งานจริง"),
    (r"\bfeature ID\b", "รหัสความสามารถ"),
    (r"\blegacy alias\b", "รหัสเดิม"),
    (r"\blegacy\b", "เดิม"),
    (r"\bowner\b", "ผู้ดูแลข้อมูล"),
    (r"\bpack\b", "เอกสารชุด"),
    (r"\bunknown\b", "ที่ไม่มีอยู่"),
    (r"\bnative controls?\b", "ปุ่มและช่องข้อมูลมาตรฐาน"),
    (r"\bnon-native controls?\b", "ส่วนที่กดได้บนหน้าจอ"),
    (r"\bcontrols?\b", "ปุ่มหรือช่องข้อมูล"),
    (r"\bsetup\b", "ข้อมูลก่อนเริ่ม"),
    (r"\bidentical\b", "เหมือนกัน"),
    (r"\bsite\b", "สาขา"),
    (r"\babsolute\b", "ค่าสัมบูรณ์"),
    (r"\bnormal\b", "ขั้นตอนปกติ"),
    (r"\boverdue\b", "เกินกำหนด"),
    (r"\bescalate\b", "ส่งต่อให้ผู้รับผิดชอบระดับถัดไป"),
    (r"\bcentral\b", "ส่วนกลาง"),
    (r"\bcounts?\b", "จำนวน"),
    (r"\bmatching existing drafts\b", "ตรงกับรายการร่างที่มีอยู่"),
    (r"\batomic accepted-set\b", "บันทึกเฉพาะชุดที่ผ่านทั้งหมดโดยไม่ขาดบางแถว"),
    (r"\batomic\b", "ครบทั้งชุดโดยไม่ขาดบางส่วน"),
    (r"\baccepted-set\b", "ชุดรายการที่ผ่านการตรวจ"),
    (r"\bsafe\b", "การทำซ้ำอย่างปลอดภัย"),
    (r"\bcontent\b", "เนื้อหา"),
    (r"\btext\b", "ข้อความ"),
    (r"\bexecute\b", "ทำงานเป็นคำสั่ง"),
    (r"\bunavailable\b", "ไม่มีให้ใช้งาน"),
    (r"\bfail(?:ure)?\b", "ไม่สำเร็จ"),
    (r"\bexplicitly\b", "อย่างชัดเจน"),
    (r"\binputs?\b", "ข้อมูลที่ใช้"),
    (r"\bvalidation\b", "การตรวจความถูกต้อง"),
    (r"\bedit\b", "แก้ไข"),
    (r"\bapprove\b", "อนุมัติ"),
    (r"\bSoD\b", "ผู้สร้างต้องไม่ใช่ผู้อนุมัติ"),
    (r"\bapplication logs?\b", "บันทึกการทำงานของระบบ"),
    (r"\bnetwork\b", "ข้อมูลที่ส่งผ่านหน้าจอ"),
    (r"\banalytics event\b", "ข้อมูลสถิติการใช้งาน"),
    (r"\bprojection\b", "การแสดงเฉพาะข้อมูลที่มีสิทธิ์"),
    (r"\bgranted\b", "ได้รับอนุญาต"),
    (r"\bhistorical\b", "ที่เก็บเป็นประวัติ"),
    (r"\breadable\b", "อ่านได้"),
    (r"\bevent/cache update\b", "ระบบรับรู้การเปลี่ยนแปลงทันที"),
    (r"\bevent\b", "เหตุการณ์ที่ระบบแจ้งต่อ"),
    (r"\bcache\b", "ข้อมูลชั่วคราว"),
    (r"\bupdate\b", "ปรับปรุง"),
    (r"\bknown\b", "ที่กำหนดไว้ล่วงหน้า"),
    (r"\braw\b", "ค่าจริง"),
    (r"\bleak\b", "รั่วไหล"),
    (r"\bevidence\b", "ข้อมูลประกอบ"),
    (r"\blower-priority\b", "ลำดับรอง"),
    (r"\bapplicable\b", "ใช้ได้ตามเงื่อนไข"),
    (r"\bclone\b", "สร้างรายการใหม่จากรายการเดิม"),
    (r"\bUI\b", "หน้าจอ"),
    (r"\bexisting\b", "ที่มีอยู่"),
    (r"\bone\b", "หนึ่ง"),
    (r"\bnew\b", "ใหม่"),
    (r"\bentry\b", "รายการ"),
    (r"\bsource currency\b", "สกุลเงินต้นทาง"),
    (r"\bpreload\b", "เลือกไว้ล่วงหน้า"),
    (r"\bmetadata\b", "ข้อมูลกำกับชุดงาน"),
    (r"\bsource\b", "แหล่งอ้างอิง"),
    (r"\bold\b", "เดิม"),
    (r"\btests?\b", "แบบทดสอบ"),
    (r"\breference\b", "ข้อมูลอ้างอิง"),
    (r"\bselection\b", "รายการที่เลือก"),
    (r"\brule\b", "กติกา"),
    (r"\bdependent\b", "เปลี่ยนตามข้อมูลที่เลือก"),
    (r"\bmultiple\b", "หลายค่า"),
    (r"made by another user", "สร้างโดยผู้ใช้อื่น"),
    (r"made by (?:current|ปัจจุบัน) user", "สร้างโดยผู้ใช้ปัจจุบัน"),
    (r"\bform\b", "แบบฟอร์ม"),
    (r"\breactivation\b", "การเปิดใช้งานกลับ"),
    (r"\breversible\b", "ย้อนกลับได้"),
    (r"\brevalidate\b", "ตรวจความพร้อมซ้ำ"),
    (r"\badd/remove\b", "เพิ่มและลบแถว"),
    (r"\bpartial\b", "บางส่วน"),
    (r"\bmock\b", "ข้อมูลจำลอง"),
    (r"\bimplementation\b", "ระบบที่พัฒนาจริง"),
    (r"\bnote\b", "ข้อความอธิบาย"),
    (r"\bencoding\b", "รูปแบบตัวอักษรของไฟล์"),
    (r"\bexpiry\b", "หมดอายุ"),
    (r"\bfresh\b", "เป็นปัจจุบัน"),
    (r"\beligible\b", "ที่ผ่านเงื่อนไข"),
    (r"\bvendors?\b", "คู่ค้า"),
    (r"\bascending\b", "จากต่ำไปสูง"),
    (r"\bambiguity\b", "คำตอบกำกวม"),
    (r"\beditor\b", "หน้าจอแก้ไข"),
    (r"\bno result\b", "ไม่พบผลลัพธ์"),
    (r"\bcalculation\b", "การคำนวณ"),
    (r"\banswer\b", "คำตอบ"),
    (r"\bfirst\b", "คนแรก"),
    (r"\bwins\b", "ทำสำเร็จ"),
    (r"\bsecond\b", "คนที่สอง"),
    (r"\bkey\b", "รหัสคำขอ"),
    (r"\bdifferent\b", "ต่างกัน"),
    (r"\bresult\b", "ผลลัพธ์"),
    (r"\bpermission\b", "สิทธิ์การใช้งาน"),
    (r"\brevoke\b", "ยกเลิกสิทธิ์"),
    (r"\bexport\b", "ส่งออกข้อมูล"),
    (r"\bprint\b", "พิมพ์"),
    (r"\blog\b", "บันทึกการทำงาน"),
    (r"\banalytics\b", "ข้อมูลสถิติ"),
    (r"\bchannel\b", "ช่องทาง"),
    (r"\bcorrelation ID\b", "รหัสติดตามการทำงาน"),
    (r"\brun\b", "รอบทดสอบ"),
    (r"\blive\b", "ล่าสุด"),
    (r"\bhistory\b", "ประวัติ"),
    (r"\bdown\b", "ขัดข้อง"),
    (r"\brecalculate\b", "คำนวณใหม่"),
    (r"\bprice_version_id\b", "รหัสฉบับราคา"),
    (r"\bLOCK-VPL-\d+\b", "ข้อตกลงขอบเขตงาน"),
    (r"\bsource precedence\b", "ลำดับการเลือกแหล่งราคา"),
    (r"\bFRD\b", "เอกสารข้อกำหนด"),
    (r"\blayout\b", "การจัดวาง"),
    (r"\bchecklist\b", "รายการตรวจ"),
    (r"\bonly\b", "เฉพาะ"),
    (r"\bout-of-date\b", "พ้นช่วงวันที่"),
    (r"\bexcluded\b", "ตัวเลือกที่ถูกตัดออก"),
    (r"\benabled\b", "กดได้"),
    (r"\balign\b", "อยู่ในแนวเดียวกัน"),
    (r"\btoast\b", "ข้อความแจ้งเตือน"),
    (r"\bprototype\b", "หน้าต้นแบบ"),
    (r"\bstill\b", "ยังคง"),
    (r"\bblank\b", "ว่าง"),
    (r"\bhighlight\b", "เน้นให้เห็น"),
    (r"\breason\b", "เหตุผล"),
    (r"\bvalues\b", "ค่า"),
    (r"\bhelper\b", "ข้อความอธิบาย"),
    (r"\balternative\b", "ค่าอื่นที่ใช้ได้"),
    (r"\bloading\b", "กำลังทำงาน"),
    (r"\bselect\b", "เลือก"),
    (r"\bresolved\b", "เลือกใช้ราคาแล้ว"),
    (r"\bthen later changed\b", "แล้วเปลี่ยนภายหลัง"),
    (r"\bconcurrent\b", "ทำพร้อมกัน"),
    (r"\bline\b", "รายการย่อย"),
]


def clean_inline(value: str) -> str:
    protected = {}
    def protect(match):
        key = f"__KEEP{len(protected)}__"
        protected[key] = match.group(0)
        return key
    value = re.sub(r"[A-Za-z0-9_+@.-]+\.csv", protect, value)
    for literal in ["F-VENDOR", "Product Master", "Purchase UOM", "Batch Entry", "Import Vendor Price List"]:
        if literal in value:
            key = f"__KEEP{len(protected)}__"
            protected[key] = literal
            value = value.replace(literal, key)
    value = value.replace("`", "").replace("⚠", "")
    value = re.sub(r"\((?:ต้อง simulate|ต้องตรวจ[^)]*|BR_[A-Z0-9_]+|ERR_[A-Z0-9_]+|NO_[A-Z0-9_]+)[^)]*\)", "", value)
    value = re.sub(r"\b(?:ERR|BR|NO)_[A-Z0-9_]+\b", "ข้อความแจ้งเตือนตามกรณี", value)
    value = re.sub(r"#/[A-Za-z0-9_{}:/.-]+", "หน้าที่ระบุ", value)
    for pattern, replacement in TECH_REPLACEMENTS:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    value = value.replace("HTML", "หน้าต้นแบบ").replace("UUID", "รหัสภายใน")
    cleanup = {
        "non-ปุ่มและช่องข้อมูลมาตรฐาน": "ส่วนที่กดได้บนหน้าจอ",
        "non-ใช้งาน": "ไม่อยู่ในสถานะใช้งาน",
        "non-สั่งซื้อได้": "สั่งซื้อไม่ได้",
        "company": "บริษัท",
        "source precedence": "ลำดับการเลือกแหล่งราคา",
        "แหล่งที่มา precedence": "ลำดับการเลือกแหล่งราคา",
        "แหล่งที่มา สกุลเงิน": "สกุลเงินต้นทาง",
        "ต้อง ทดสอบด้วยเครื่องมือระบบ": "ขั้นนี้ให้ทีมระบบตรวจยืนยัน",
        "ไม่พบใน หน้าต้นแบบ": "หน้าต้นแบบยังไม่แสดงผลนี้",
        "test-เครื่องมือทดสอบของทีมระบบ": "เครื่องมือทดสอบของทีมระบบ",
        "lower-priority": "ลำดับรอง",
        "Product ข้อมูลหลัก": "Product Master",
        "purchase ข้อมูลหลัก": "Purchase UOM",
        "UI": "หน้าจอ",
    }
    for old, new in cleanup.items():
        value = value.replace(old, new)
    value = re.sub(r"\s+", " ", value).strip(" ·;")
    for key, literal in protected.items():
        value = value.replace(key, literal)
    return value


def page_name(route: str) -> str:
    raw = route.replace("`", "").strip()
    if raw in ROUTE_NAMES:
        return ROUTE_NAMES[raw]
    if "vendor/:vendorId" in raw or "/vendor/" in raw:
        return "รายการราคาของคู่ค้าที่เลือก"
    if "batch" in raw:
        return "กรอกหลายรายการ"
    if "compare" in raw:
        return "เปรียบเทียบราคา"
    if "API" in raw or "N/A" in raw:
        return "ผลตรวจที่ทีมระบบเตรียมไว้"
    return "รายการราคาคู่ค้า"


def translate_action(action: str) -> str:
    raw = action.replace("`", "").strip()
    verb, _, detail = raw.partition(" ")
    if verb == "OPEN" and "#/" in detail:
        return "เปิดหน้า “{}” ตามชื่อที่เห็นในเมนู".format(page_name(detail))
    detail = clean_inline(detail)
    if verb == "OPEN":
        if "ระบบเบื้องหลัง" in detail or "เครื่องมือทดสอบ" in detail or "scenario" in detail.lower():
            return "ดูผลทดสอบที่ทีมระบบเตรียมไว้สำหรับกรณี “{}”".format(detail)
        if "ใช้งาน" in detail and "รายการ" in detail:
            return "ที่หน้ารายการ คลิกแถวที่มีป้ายสถานะ “ใช้งาน” หนึ่งครั้ง"
        if "รออนุมัติ" in detail:
            return "ที่หน้ารายการ คลิกแถวที่มีป้ายสถานะ “รออนุมัติ” หนึ่งครั้ง"
        if "ร่าง" in detail and "รายการ" in detail:
            return "ที่หน้ารายการ คลิกแถวที่มีป้ายสถานะ “ร่าง” หนึ่งครั้ง"
        if "สร้างรายการราคา" in detail or "drawer" in detail:
            return "มองหาปุ่ม “สร้างรายการราคา” ที่ด้านบนขวา แล้วคลิกหนึ่งครั้ง"
        return "เปิดหน้า “{}” ตามชื่อที่เห็นในเมนู".format(detail or "รายการราคาคู่ค้า")
    if verb == "CLICK":
        return "มองหาปุ่มหรือรายการที่เขียนว่า “{}” แล้วคลิกหนึ่งครั้ง".format(detail)
    if verb == "TYPE":
        if "→" in detail:
            value, field = [x.strip() for x in detail.split("→", 1)]
            return "คลิกช่อง “{}” แล้วพิมพ์ {}".format(field, value)
        return "กรอกข้อมูลตามที่ระบุในส่วน “{}” ให้ครบ".format(detail)
    if verb == "SELECT":
        return "คลิกช่องเลือกที่เกี่ยวข้อง แล้วเลือก “{}” จากรายการที่ระบบแสดง".format(detail)
    if verb == "UPLOAD":
        return "ที่ส่วนเลือกไฟล์ คลิกปุ่ม “เลือกไฟล์” แล้วเลือกไฟล์ชื่อ “{}” ที่ผู้ดูแลเตรียมไว้".format(detail)
    if verb == "PRESS":
        return "กดปุ่ม {} ที่แป้นพิมพ์หนึ่งครั้ง".format(detail)
    if verb == "WAIT":
        return "รอจนกระทั่ง {}".format(detail)
    if verb == "VERIFY":
        return "สังเกตและตรวจดู {}".format(detail)
    if verb == "TOGGLE":
        return "คลิกสวิตช์หรือช่องทำเครื่องหมาย “{}” หนึ่งครั้ง".format(detail)
    return clean_inline(raw)


def translate_expected(value: str, is_sys: bool) -> str:
    text = clean_inline(value)
    text = text.replace("toast", "ข้อความแจ้งเตือน").replace("modal", "หน้าต่างยืนยัน")
    text = text.replace("drawer", "แผงด้านข้าง").replace("route", "หน้าที่เปิดอยู่")
    text = text.replace("count", "จำนวนรายการ").replace("baseline", "ค่าที่จดไว้ก่อนเริ่ม")
    text = text.replace("commit", "บันทึกข้อมูล").replace("conflict", "ข้อมูลขัดแย้ง")
    text = text.replace("source", "แหล่งที่มา").replace("scope", "ขอบเขตข้อมูล")
    if is_sys and "ทีมระบบ" not in text:
        text += " (ขั้นนี้ให้ทีมระบบตรวจยืนยัน)"
    return text


def translate_input(value: str) -> str:
    value = clean_inline(value)
    return "—" if not value or value == "—" else value


def priority(meta: str) -> str:
    return "high" if "· P0 ·" in meta else "med" if "· P1 ·" in meta else "low"


def data_key(case_id: str) -> str | None:
    if case_id.startswith("TC-IMP-"):
        return "FILES"
    if case_id in {"TC-APR-06", "TC-APR-07", "TC-APR-08"}:
        return "E"
    if case_id.startswith("TC-CMP-"):
        return "C"
    if case_id in {"TC-CRT-03", "TC-CRT-04", "TC-CRT-05"}:
        return "B"
    if case_id.startswith("TC-CRT-") or case_id.startswith("TC-BAT-"):
        return "A"
    return None


def region_key(group_letter: str, action: str, expected: str, is_sys: bool) -> str:
    if is_sys:
        return ""
    text = action + " " + expected
    if "Import" in text or "นำเข้า" in text or group_letter == "E":
        return "import_modal"
    if group_letter == "D":
        return "batch_page"
    if group_letter == "F":
        return "compare_page"
    if "อนุมัติราคาฉบับนี้หรือไม่" in text:
        return "approve_modal"
    if "ปฏิเสธราคาฉบับนี้หรือไม่" in text:
        return "reject_modal"
    if "ปิดใช้งานรายการราคา" in text:
        return "deactivate_modal"
    if "เปิดใช้งานรายการราคา" in text:
        return "activate_modal"
    if "ถัดไป" in text or any(k in text for k in ["ราคาตั้ง", "เหตุผล", "เริ่มใช้", "สรุปก่อนส่ง"]):
        return "create_step2"
    if any(k in text for k in ["สร้างรายการราคา", "Purchase UOM", "ค้นหารหัสหรือชื่อคู่ค้า", "ค้นหารหัสหรือชื่อสินค้า"]):
        return "create_step1"
    if "คู่ค้าที่เลือก" in text or "แยกตามคู่ค้า" in text:
        return "vendor_page"
    if group_letter == "C":
        return "view_drawer"
    if group_letter == "A":
        return "list_page"
    return ""


text = SOURCE.read_text(encoding="utf-8")
lines = text.splitlines()
groups = []
group_letter = None
case_blocks = []
current = None

for line in lines:
    m = re.match(r"^### กลุ่ม ([A-H]) — (.+)$", line)
    if m:
        group_letter = m.group(1)
        groups.append({"id": GROUP_IDS[group_letter], "name": clean_inline(m.group(2))})
        continue
    m = re.match(r"^#### (TC-[A-Z]+-\d+) — (.+)$", line)
    if m:
        if current:
            case_blocks.append(current)
        current = {"id": m.group(1), "title": m.group(2), "group": group_letter, "lines": []}
        continue
    if current:
        if line.startswith("## ") or line.startswith("### กลุ่ม "):
            case_blocks.append(current)
            current = None
        else:
            current["lines"].append(line)
if current:
    case_blocks.append(current)

cases = []
for block in case_blocks:
    body = "\n".join(block["lines"])
    meta = re.search(r"^- Group/Priority/Trace: (.+)$", body, re.M)
    actor = re.search(r"^- Actor: (.+)$", body, re.M)
    setup = re.search(r"^- Setup: (.+)$", body, re.M)
    start = re.search(r"^- Start route: (.+)$", body, re.M)
    passed = re.search(r"^- Pass criteria: (.+)$", body, re.M)
    is_sys = any(x in body for x in ["ต้อง simulate", "⚠", "inject="]) or "downstream service" in body

    who_raw = actor.group(1).replace("`", "") if actor else "ผู้ทดสอบ"
    who = ROLE_MAP.get(who_raw, clean_inline(who_raw))
    setup_raw = setup.group(1).replace("`", "") if setup else ""
    seed_match = re.search(r"seed=([^·]+)", setup_raw)
    files_match = re.search(r"files=([^·]+)", setup_raw)
    pre_parts = ["เข้าสู่ระบบด้วยบัญชี{}".format(who)]
    if seed_match:
        pre_parts.append("มีข้อมูลทดสอบ: {}".format(clean_inline(seed_match.group(1))))
    if files_match and files_match.group(1).strip() != "—":
        pre_parts.append("เตรียมไฟล์: {}".format(clean_inline(files_match.group(1))))
    pre_parts.append("เริ่มที่หน้า “{}”".format(page_name(start.group(1) if start else "")))
    if is_sys:
        pre_parts.append("กรณีนี้ให้ทีมระบบเตรียมสภาพทดสอบพิเศษและแจ้งผล")

    steps = []
    for line in block["lines"]:
        if not re.match(r"^\| \d+ \|", line):
            continue
        cols = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cols) != 5:
            raise ValueError(f"Unexpected step table row: {line}")
        _, action, inp, expected, _ = cols
        steps.append([
            translate_action(action),
            translate_input(inp),
            translate_expected(expected, is_sys),
            region_key(block["group"], action, expected, is_sys),
        ])

    pass_text = clean_inline(passed.group(1) if passed else "ทำทุกขั้นได้และเห็นผลตรงตามที่ระบุ")
    why = "ตรวจให้แน่ใจว่า{}".format(pass_text)
    if is_sys:
        why += " กรณีนี้ต้องใช้เครื่องมือของทีมระบบ จึงข้ามในรอบทดสอบของผู้ใช้"
    case = {
        "id": block["id"],
        "grp": GROUP_IDS[block["group"]],
        "pri": priority(meta.group(1) if meta else ""),
        "title": clean_inline(block["title"]),
        "why": why,
        "who": who,
        "pre": " ก่อนเริ่ม: ".join([pre_parts[0], " · ".join(pre_parts[1:])]),
        "data": data_key(block["id"]),
        "pass": pass_text,
        "steps": steps,
    }
    if is_sys:
        case["sys"] = True
    cases.append(case)

data = {
    "A": {"rows": [
        ["คู่ค้า", "V-TH-MN-00001 · บริษัท สตีลโปร จำกัด"],
        ["สินค้า", "PM-4001 · กล่องลูกฟูก 5 ชั้น 60x40x40"],
        ["Purchase UOM", "BOX"], ["สกุลเงิน", "THB"],
        ["ราคาตั้ง / ราคาต่อจำนวน", "295.00 / 1"],
        ["ส่วนลด / ค่าขนส่ง", "0 / 0.50"],
        ["เริ่มใช้ / สิ้นสุด", "15 ส.ค. 2569 / เว้นว่าง"],
        ["เหตุผล", "ปรับราคาตามใบเสนอราคาล่าสุด"],
    ]},
    "B": {"rows": [
        ["คู่ค้าที่ยังใช้ไม่ได้", "V-TH-TR-00002, V-TH-TR-00003, V-TH-TR-00005, V-TH-TR-00006"],
        ["สินค้าที่ซื้อไม่ได้", "FG-1010 · เก้าอี้สำนักงาน ergonomic"],
        ["หน่วยซื้อที่ไม่ตรง", "KG สำหรับสินค้า PM-4001"],
    ]},
    "C": {"rows": [
        ["สินค้า", "RM-2001 · ไม้สักแปรรูป เกรด A"],
        ["ปริมาณ", "1,000 KG"], ["วันที่", "20 ส.ค. 2569"],
        ["สกุลเงินเป้าหมาย", "THB"],
    ]},
    "D": {"rows": [
        ["ราคาที่ไม่ถูกต้อง", "0 และ -0.01"],
        ["ส่วนลดที่ต้องลอง", "-0.01, 0, 100, 100.01"],
        ["ช่วงวันที่ผิด", "10 ส.ค. 2569 ถึง 9 ส.ค. 2569"],
    ]},
    "E": {"rows": [
        ["ราคาปัจจุบันต่อหน่วย", "100.00"],
        ["ต่ำกว่าเกณฑ์", "109.99 (+9.99%)"],
        ["เท่ากับเกณฑ์", "110.00 (+10.00%)"],
        ["สูงกว่าเกณฑ์", "110.01 (+10.01%)"],
    ]},
    "FILES": {"rows": [
        ["ไฟล์ผ่าน 4 แถว", "vpl-valid-4-rows.csv"],
        ["ไฟล์ข้อมูลไม่ตรง", "vpl-unmatched-master.csv"],
        ["ไฟล์รหัสซ้ำ", "vpl-duplicate-external-id.csv"],
        ["ไฟล์หัวคอลัมน์ผิด", "vpl-invalid-header.csv"],
        ["ไฟล์รูปแบบตัวอักษรผิด", "vpl-invalid-encoding.csv"],
        ["ไฟล์ข้อความคล้ายสูตร", "vpl-formula-like-cell.csv"],
    ]},
}

payload = {
    "meta": {
        "feature_id": "F-VENDOR-PRICELIST-001",
        "title": "แบบทดสอบรายการราคาคู่ค้า",
        "crumb": "จัดซื้อ",
        "code": "F-VENDOR-PRICELIST-001 · เวอร์ชัน 1.0",
        "footer": "F-VENDOR-PRICELIST-001 · 2BSimple · ผลบันทึกในเครื่องนี้อัตโนมัติ",
        "report_sub": "รายการราคาคู่ค้า · รหัสฟีเจอร์ F-VENDOR-PRICELIST-001",
    },
    "groups": groups,
    "data": data,
    "cases": cases,
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({
    "out": str(OUT),
    "groups": len(groups),
    "cases": len(cases),
    "steps": sum(len(c["steps"]) for c in cases),
    "sys_cases": sum(1 for c in cases if c.get("sys")),
}, ensure_ascii=False))
