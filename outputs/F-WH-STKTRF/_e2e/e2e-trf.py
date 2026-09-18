#!/usr/bin/env python3
"""F-WH-STKTRF feature E2E — WF step 5.

Uses the shared uikit timing/runtime harness. Every checklist FN is mapped to a
rendered or state-transition assertion; FN-40 is a rendered negative case.
"""
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import Suite, ready, after, settle  # noqa: E402

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "F-WH-STKTRF.html").resolve()
BASE = HTML.as_uri()
SHOTS = HTML.parent / "_shots"
SHOTS.mkdir(exist_ok=True)
suite = Suite("F-WH-STKTRF · Stock Transfer")


def ev(pg, js, arg=None):
    return pg.evaluate(js) if arg is None else pg.evaluate(js, arg)


def open_(pg):
    ready(pg, BASE, timeout=9000)
    pg.wait_for_function("()=>document.getElementById('page-content')&&document.getElementById('page-content').innerHTML.length>0", timeout=9000)


def text(pg, sel="body"):
    return ev(pg, "s=>(document.querySelector(s)||{}).innerText||''", sel)


def toast(pg):
    return text(pg, "#toast")


def open_create(pg, step=1):
    after(pg, "()=>openCreateDrawer(null)")
    pg.wait_for_function("()=>window.createWizard&&document.getElementById('create-drawer-content')", timeout=4000)
    if step != 1:
        after(pg, f"()=>{{createWizard.step={step};renderCreateDrawer();}}")


def open_view(pg, doc_id, tab="detail"):
    after(pg, f"()=>openViewDrawer('{doc_id}')")
    pg.wait_for_function("()=>document.getElementById('view-drawer-content')", timeout=4000)
    after(pg, f"()=>{{viewState.tab='{tab}';renderViewDrawer();}}")


def c_list(pg):
    open_(pg)
    body = text(pg)
    for needle in ["ของที่อยู่ระหว่างทาง", "ใบรออนุมัติ", "ค้างระหว่างทาง", "รอฉันรับ", "อยู่ระหว่างทาง", "เอกสารแนบ"]:
        assert needle in body, f"landing ขาด {needle}"
    assert ev(pg, "()=>document.querySelectorAll('.stat').length") == 4
    assert ev(pg, "()=>document.querySelectorAll('.filter-bar input,.filter-bar select').length") >= 5
    headers = text(pg, ".landing-table thead")
    assert "ผู้จัดทำ" in headers and "เหตุผลย้าย" in headers, headers
    assert ev(pg, "()=>{const w=document.querySelector('.table-wrap');return w.scrollWidth>w.clientWidth}"), "landing table has no internal x-scroll range"
    assert ev(pg, "()=>{const w=document.querySelector('.table-wrap');w.scrollLeft=w.scrollWidth;return w.scrollLeft>0}"), "landing table cannot scroll horizontally"
    assert ev(pg, "()=>getComputedStyle(document.querySelector('.landing-table .cell-truncate')).textOverflow") == "clip", "landing cell still truncates with ellipsis"
    assert ev(pg, "()=>document.body.scrollWidth<=window.innerWidth"), "table pushes horizontal overflow to body"
    pg.screenshot(path=str(SHOTS / "landing_table_scrolled_right.png"), full_page=True)
    after(pg, "()=>{listState.q='ปาริชาต แก้วมณี';renderTableOnly();}")
    assert ev(pg, "()=>visibleDocs().length") > 0
    assert ev(pg, "()=>visibleDocs().every(d=>d.createdBy.includes('ปาริชาต แก้วมณี'))")
    after(pg, "()=>{listState.q='';listState.more=true;render();}")
    assert ev(pg, "()=>document.querySelector('.filter-more-panel')!==null")
    assert "เหตุผลย้าย" in text(pg, ".filter-more-panel")
    assert "ผู้จัดทำ" not in text(pg, ".filter-more-panel")
    pg.screenshot(path=str(SHOTS / "landing_filter_expanded.png"), full_page=True)
    after(pg, "()=>{listState.q='ไม่มีใบนี้แน่นอน';renderTableOnly();}")
    assert "ไม่พบรายการที่ค้นหา" in text(pg, ".list-card")
    assert ev(pg, "()=>document.querySelector('.empty .btn')!==null")
    return "KPI 4 · symmetric filters · creator search · creator/reason columns · attachments · empty state"


def c_upload(pg):
    open_(pg); open_create(pg, 4)
    picker = pg.locator("#trf-upload")
    assert picker.count() == 1
    picker.set_input_files({"name": "branch-request.pdf", "mimeType": "application/pdf", "buffer": b"%PDF-1.4\n% test"})
    assert "branch-request.pdf" in text(pg, "#create-drawer-content")
    assert ev(pg, "()=>createWizard.data.attachments.some(f=>f.name==='branch-request.pdf')")
    assert "แนบไฟล์แล้ว 1 ไฟล์" in toast(pg)
    pg.screenshot(path=str(SHOTS / "wizard_upload_file.png"), full_page=True)
    after(pg, "()=>handleUploadFiles([{name:'malware.exe',size:1200}])")
    assert "รองรับเฉพาะ PDF, JPG และ PNG" in toast(pg)
    assert not ev(pg, "()=>createWizard.data.attachments.some(f=>f.name==='malware.exe')")
    return "real file input · accepted file rendered · unsupported extension rejected"


def c_wizard_modes(pg):
    open_(pg); open_create(pg, 2)
    after(pg, "()=>{createWizard.data.whFrom='WH-BKK-01';createWizard.data.whTo='WH-BKK-01';createWizard.data.mode=docMode(createWizard.data.whFrom,createWizard.data.whTo);renderCreateDrawer();}")
    t = text(pg, "#create-drawer-content")
    assert "ภายในคลัง — ย้ายจบในจังหวะเดียว" in t, t[:500]
    assert ev(pg, "()=>[...document.querySelectorAll('#create-drawer-content input')].some(x=>x.value==='(ร่าง — ออกเลขอัตโนมัติเมื่อส่งอนุมัติ)')"), "draft automatic-number label missing"
    after(pg, "()=>{createWizard.data.whTo='WH-CNX-01';createWizard.data.mode=docMode(createWizard.data.whFrom,createWizard.data.whTo);renderCreateDrawer();}")
    t = text(pg, "#create-drawer-content")
    assert "ข้ามคลัง/สาขา — ต้องมีขั้นยืนยันรับที่ปลายทาง" in t and "TR-BKK-CNX" in t, t[:700]
    assert "คลังต้นทาง" in t and "คลังปลายทาง" in t, t[:700]
    return "wizard picker · derive 2 modes · transit read-only · draft has no number"


def c_line_rules(pg):
    open_(pg); open_create(pg, 3)
    after(pg, "()=>{const l=mkLine({binFrom:'A-01-02-C',item_code:'STA-PEN-001',item_name:'ปากกาลูกลื่น น้ำเงิน 0.5 มม.',unit:'ด้าม',qty:2000,unit_price:6.5,binTo:'A-01-02-C'});createWizard.data.whFrom='WH-BKK-01';createWizard.data.whTo='WH-BKK-01';createWizard.data.mode='intra';createWizard.data.lines=[l];renderCreateDrawer();}")
    t = text(pg, "#create-drawer-content")
    assert "ยอดคงเหลือต้นทาง 1,180" in t, t[:900]
    assert "bin ต้นทางและปลายทางต้องต่างกัน" in t, t[:900]
    assert "มูลค่ารวมที่ย้าย" in t and "13,000.00" in t, t[-700:]
    headers = text(pg, ".line-tbl thead")
    for forbidden in ["ราคาขาย", "Lot", "Serial"]:
        assert forbidden not in headers
    pg.screenshot(path=str(SHOTS / "wizard_line_editor_aligned.png"), full_page=True)
    after(pg, "()=>{createWizard.data.lines[0].binTo='A-01-01-A';renderCreateDrawer();wizardNext();}")
    assert "เกินยอดคงเหลือ" in toast(pg), toast(pg)
    after(pg, "()=>{createWizard.data.lines[0].qty=0;renderCreateDrawer();wizardNext();}")
    assert "มากกว่า 0" in toast(pg)
    return "over/on-zero/same-bin rendered blocks · totals · no sales/lot/serial columns"


def c_location_contract(pg):
    open_(pg); open_create(pg, 3)
    out = ev(pg, """()=>{const l=createBlankLine();createWizard.data.lines=[l];createWizard.data.whFrom='WH-BKK-01';createWizard.data.whTo='WH-BKK-01';
      const src=comboItems('binFrom-'+l.id,'');l.binFrom='QA-01';const dst=comboItems('binTo-'+l.id,'');
      return {src:src,dst:dst,tr:comboItems('binFrom-'+l.id,'TR-'),dm:comboItems('binFrom-'+l.id,'DM-'),st:comboItems('binFrom-'+l.id,'ST-')};}""")
    locked = [x for x in out["src"] if x["val"] == "B-03-02-B"]
    assert locked and locked[0]["dis"] and "ล็อก" in locked[0]["s"]
    assert out["dst"] and all(ev(pg, "c=>BIN_BY[c].type", x["val"]) == "quarantine" for x in out["dst"])
    assert out["tr"] == [] and out["dm"] == [] and out["st"] == []
    t = text(pg, "#create-drawer-content")
    assert "ใบปรับยอดสต๊อก" in t and "Putaway" not in t  # staging is filtered before selection
    return "locked disabled+reason · quarantine→quarantine · damage/staging/transit excluded"


def c_fn40_negative(pg):
    open_(pg); open_create(pg, 2)
    after(pg, """()=>{WAREHOUSES.push({code:'WH-NO-TR',name:'คลังไม่มีจุดพัก',addr:'—'});WH_BY['WH-NO-TR']=WAREHOUSES[WAREHOUSES.length-1];
      createWizard.data.whFrom='WH-BKK-01';createWizard.data.whTo='WH-NO-TR';createWizard.data.mode='inter';createWizard.data.docDate=TODAY;createWizard.data.reason='TR-01';renderCreateDrawer();wizardNext();}""")
    assert createWizard_step(pg) == 2
    assert "ยังไม่มีจุดพักระหว่างทาง" in toast(pg)
    assert "ติดต่อผู้ดูแลผังตำแหน่ง" in toast(pg)
    assert "สร้าง bin" not in text(pg, "#create-drawer-content")
    return "FN-40 rendered negative: missing pair blocks and directs admin configuration"


def createWizard_step(pg):
    return ev(pg, "()=>createWizard.step")


def c_internal_flow(pg):
    open_(pg)
    after(pg, "()=>{const d=findDoc('d2');d.status='approved';d.lines[0].qty=10;d.lines[0].binFrom='A-01-01-A';d.lines[0].item_code='STA-PPR-A4';window.__nativeDialogPolicy='accept';doShip('d2');}")
    assert ev(pg, "()=>findDoc('d2').status") == "moved"
    assert ev(pg, "()=>findDoc('d2').lines[0].received") == 10
    assert any("FWD-WIRE: JE posting" in a.get("note", "") for a in ev(pg, "()=>findDoc('d2').audit"))
    open_view(pg, "d2", "history")
    assert "ย้ายภายในคลังสำเร็จ" in text(pg, "#view-drawer-content")
    return "one-step internal move · recheck source · append-only JE marker"


def c_inter_transit(pg):
    open_(pg); open_view(pg, "d6", "detail")
    assert "ของที่ยังอยู่ระหว่างทาง" in text(pg, "#view-drawer-content"), text(pg, "#view-drawer-content")[:1000]
    after(pg, "()=>{viewState.tab='transit';renderViewDrawer();}")
    t = text(pg, "#view-drawer-content")
    assert "ค้างระหว่างทาง" in t, t[:1000]
    assert ev(pg, "()=>![...document.querySelectorAll('#view-drawer-content button')].some(b=>b.innerText.trim()==='ยกเลิก')"), "post-move cancel button still rendered"
    assert ev(pg, "()=>inTransitQty(findDoc('d6'))") > 0, "no transit quantity"
    assert ev(pg, "()=>findDoc('d6').status") == "in_transit", "wrong transit status"
    return "cross-warehouse leg 1 stays transit · visible remaining · cancel gone"


def c_receive_and_diff(pg):
    open_(pg)
    after(pg, "()=>openReceiveModal('d3')")
    assert "เฉพาะเจ้าหน้าที่ของคลังปลายทาง" in toast(pg), toast(pg)
    after(pg, "()=>{ME.wh='WH-CNX-01';ME.name='ณัฐริกา คำแสน';openReceiveModal('d3');}")
    after(pg, "()=>{receiveState.rows[0].take=Math.max(0,receiveState.rows[0].rem-1);renderReceiveModal();}")
    t = text(pg, "#receive-modal")
    for n in ["รับครั้งนี้", "คงค้างระหว่างทาง", "รอรับเพิ่ม", "ของหาย/เสียหายระหว่างทาง", "ตีกลับคืนต้นทาง"]:
        assert n in t, f"receive modal missing {n}: {t[:900]}"
    after(pg, "()=>{receiveState.rows[0].take=receiveState.rows[0].rem+1;renderReceiveModal();confirmReceive();}")
    assert "รับเกินจำนวนที่ส่งออกไม่ได้" in toast(pg) and "ใบปรับยอดสต๊อก" in toast(pg)
    after(pg, "()=>{receiveState.rows[0].take=1;receiveState.rows[0].diffAction='wait';confirmReceive();}")
    assert ev(pg, "()=>findDoc('d3').status") == "partial", ev(pg, "()=>findDoc('d3').status")
    assert ev(pg, "()=>inTransitQty(findDoc('d3'))") >= 0, "negative transit"
    assert ev(pg, "()=>findDoc('d1').status==='closed'&&inTransitQty(findDoc('d1'))===0"), "full receipt seed not closed"
    return "destination-only receive · 3 difference choices · over-receipt blocked · partial remains open"


def c_shortage_seed(pg):
    open_(pg); open_view(pg, "d4", "transit")
    t = text(pg, "#view-drawer-content")
    assert "ส่วนต่าง" in t and "ปิดใบพร้อมส่วนต่าง" in text(pg, "#view-drawer-content")
    assert ev(pg, "()=>writtenOffAmount(findDoc('d4'))") > 0
    assert ev(pg, "()=>inTransitQty(findDoc('d4'))") == 0
    assert ev(pg, "()=>findDoc('d5').status") == "returned"
    assert ev(pg, "()=>findDoc('d5').lines.every(l=>lineRemaining(l)===0)")
    assert ev(pg, "()=>DOCS.some(d=>isAging(d))")
    return "write-off closes transit · return closes remaining · invariant/aging seed proven"


def c_fix01_receive_guard(pg):
    open_(pg)
    open_view(pg, "d3")
    tip = pg.locator(".disabled-tip.receive-tip")
    assert tip.count() == 1, f"receive tooltip wrapper count={tip.count()}"
    tip.hover()
    settle(pg)
    tip_text = pg.locator(".receive-tip .disabled-tip-msg").text_content() or ""
    assert "ยืนยันรับได้เฉพาะเจ้าหน้าที่ของคลังปลายทาง (คลังเชียงใหม่)" in tip_text, f"tooltip text={tip_text!r}"
    tip_visibility = ev(pg, "()=>getComputedStyle(document.querySelector('.receive-tip .disabled-tip-msg')).visibility")
    assert tip_visibility == "visible", f"tooltip visibility={tip_visibility}"
    pg.screenshot(path=str(SHOTS / "receive_disabled_tooltip.png"), full_page=True)
    before = ev(pg, "()=>findDoc('d1').lines[0].received")
    after(pg, "()=>{const s=findDoc('d1'),l=s.lines[0];receiveState={id:s.id,rows:[{id:l.id,ref:l,qty:l.qty,rem:99,take:5,binActual:l.binActual||l.binTo,diffAction:'wait',diffReason:'',diffNote:''}]};confirmReceive();}")
    assert "ใบนี้ไม่อยู่ในสถานะรอรับ" in toast(pg)
    assert ev(pg, "()=>findDoc('d1').lines[0].received") == before
    after(pg, "()=>{const s=findDoc('d3'),l=s.lines[0],rem=lineRemaining(l);receiveState={id:s.id,rows:[{id:l.id,ref:l,qty:l.qty,rem:999,take:rem+5,binActual:l.binActual||l.binTo,diffAction:'wait',diffReason:'',diffNote:''}]};confirmReceive();}")
    assert "รับเกินจำนวนที่ส่งออกไม่ได้" in toast(pg)
    assert ev(pg, "()=>receiveState.rows[0].take===lineRemaining(findDoc('d3').lines[0])")
    return "FIX-01 closed receive blocked · remaining re-derived · injected take clamped · disabled reason tooltip visible"


def c_fix02_reverse_doa(pg):
    open_(pg)
    after(pg, "()=>openReverseModal('d12')")
    assert "กลับรายการได้เฉพาะใบที่ของขยับแล้ว" in toast(pg)
    assert ev(pg, "()=>document.querySelector('.modal-overlay')===null")
    after(pg, "()=>openReverseModal('d6')")
    assert "ตีกลับคืนต้นทาง" in toast(pg)
    after(pg, "()=>openReverseModal('d2')")
    after(pg, "()=>{document.getElementById('md-reason').value='ทดสอบใบกลับรายการ';document.getElementById('md-ok').click();}")
    rev_id = ev(pg, "()=>DOCS[0].id")
    assert ev(pg, "id=>findDoc(id).status", rev_id) == "pending_approval"
    assert ev(pg, "id=>findDoc(id).approval_chain.every(x=>x.status==='pending'&&!x.assignee&&!x.by&&!x.at)", rev_id)
    assert ev(pg, "id=>findDoc(id).lines.every(x=>!x.received&&!x.binActual)", rev_id)
    assert ev(pg, "()=>findDoc('d2').status") == "moved"
    after(pg, "()=>{modalState.slots.forEach(st=>{const e=EMPLOYEES.find(x=>st.roles.includes(x.role)&&x.name!==findDoc(modalState.id).submittedBy);st.assignee=e.name;});confirmSubmit();}")
    rev_state = ev(pg, "id=>({doc:findDoc(id),modal:modalState,toast:(document.getElementById('toast')||{}).innerText||''})", rev_id)
    assert ev(pg, "id=>findDoc(id).approval_chain.every(x=>x.assignee&&x.status==='pending')", rev_id), rev_state
    while ev(pg, "id=>!!currentStep(findDoc(id))", rev_id):
        assignee = ev(pg, "id=>currentStep(findDoc(id)).assignee", rev_id)
        role = ev(pg, "id=>currentStep(findDoc(id)).roles[0]", rev_id)
        ev(pg, "a=>{ME.name=a.name;ME.role=a.role;confirmApprove(a.id);}", {"id": rev_id, "name": assignee, "role": role}); settle(pg)
    assert ev(pg, "id=>findDoc(id).status", rev_id) == "approved"
    ev(pg, "id=>{window.__nativeDialogPolicy='accept';doShip(id);}", rev_id); settle(pg)
    assert ev(pg, "id=>findDoc(id).status", rev_id) == "moved"
    assert ev(pg, "()=>findDoc('d2').status") == "reversed"
    return "FIX-02 pending/in-transit reverse blocked · moved reversal follows DOA then ships"


def c_fix03_shortage_approval(pg):
    open_(pg)
    after(pg, "()=>{const s=findDoc('d3'),l=s.lines[0];l.pendingWriteOff=lineRemaining(l);l.diffReason='DF-01';s.status='partial';openShortageModal(s.id);modalState.evidence=[{name:'proof.pdf',size:'10 KB'}];modalState.slots.forEach(st=>{const e=EMPLOYEES.find(x=>st.roles.includes(x.role)&&x.name!==s.shippedBy);st.assignee=e.name;});confirmShortage();}")
    assert ev(pg, "()=>findDoc('d3').shortage_status") == "pending"
    assert ev(pg, "()=>findDoc('d3').status") == "partial"
    assert ev(pg, "()=>findDoc('d3').shortage_chain.every(x=>x.status==='pending'&&!x.by&&!x.at)")
    assert ev(pg, "()=>findDoc('d3').lines.every(x=>!x.writtenOff)")
    while ev(pg, "()=>!!currentShortageStep(findDoc('d3'))"):
        assignee = ev(pg, "()=>currentShortageStep(findDoc('d3')).assignee")
        role = ev(pg, "()=>currentShortageStep(findDoc('d3')).roles[0]")
        ev(pg, "a=>{ME.name=a.name;ME.role=a.role;confirmShortageApprove('d3');}", {"name": assignee, "role": role}); settle(pg)
    assert ev(pg, "()=>findDoc('d3').shortage_status") == "approved"
    assert ev(pg, "()=>findDoc('d3').status") == "closed_diff"
    assert ev(pg, "()=>findDoc('d3').shortage_chain.every(x=>x.status==='approved'&&x.by&&x.at)")
    return "FIX-03 shortage stays pending until each real assignee approves · then closed_diff"


def c_fix04_05_08_anchors_and_demo(pg):
    source = HTML.read_text(encoding="utf-8")
    assert source.count("CSQ:") >= 3
    assert source.count("NTF:") >= 3
    assert "ENG-DOC-NUM.next()" in source and "ENG-DOC-STORE" in source
    open_(pg)
    ev(pg, "()=>{const st=document.createElement('style');st.textContent='.demo-only{display:none!important}';document.head.appendChild(st);}")
    open_create(pg, 2)
    assert "ENG-DOC-NUM" not in text(pg, "#create-drawer-content")
    assert "FWD-WIRE" not in text(pg, "#create-drawer-content")
    after(pg, "()=>{createWizard.step=3;renderCreateDrawer();}")
    assert "FWD-WIRE" not in text(pg, "#create-drawer-content")
    open_view(pg, "d4", "detail")
    assert "FWD-WIRE" not in text(pg, "#view-drawer-content")
    after(pg, "()=>{viewState.tab='history';renderViewDrawer();}")
    assert "FWD-WIRE" not in text(pg, "#view-drawer-content")
    assert ev(pg, "()=>[...document.querySelectorAll('.demo-only')].every(x=>getComputedStyle(x).display==='none')")
    assert ev(pg, "()=>document.getElementById('view-drawer').getBoundingClientRect().right<=innerWidth")
    return "FIX-04/05 anchors complete · FIX-08 production-hide leaves clean stable UI"


def c_fix06_busy(pg):
    open_(pg)
    after(pg, "()=>{Object.assign(ME,{code:'EMP-1058',name:'ปาริชาต แก้วมณี',initials:'ปช',role:'wh_officer',dept:'คลังกลางบางนา',wh:'WH-BKK-01'});openSubmitModal('d8');modalState.slots[0].assignee='ธนกฤต ศรีวิชัย';confirmSubmit();}")
    assert ev(pg, "()=>findDoc('d8').status") == "pending_approval"
    ev(pg, "()=>Object.assign(ME,{code:'EMP-1042',name:'ธนกฤต ศรีวิชัย',initials:'ธก',role:'wh_supervisor',dept:'คลังสินค้า',wh:'WH-BKK-01'})")
    open_view(pg, "d8", "sign")
    assert "อนุมัติ" in text(pg, "#view-drawer-content")
    after(pg, "()=>confirmApprove('d8')")
    assert ev(pg, "()=>findDoc('d8').status") == "approved"
    after(pg, "()=>{renderViewDrawer();openShipModal('d8');}")
    ship_modal = text(pg, ".modal-overlay")
    assert "ยืนยันส่งออกจากต้นทาง" in ship_modal and "TRF-2026-0008" in ship_modal
    assert ev(pg, "()=>document.querySelector('#btn-confirm-ship')!==null")
    pg.screenshot(path=str(SHOTS / "ship_confirm_modal.png"), full_page=True)
    out = ev(pg, """()=>{const s=findDoc('d8');window.__nativeDialogPolicy='accept';
      const before=s.audit.length;doShip('d8');doShip('d8');return {status:s.status,before:before,after:s.audit.length,busy:state._busy};}""")
    assert out["status"] == "in_transit" and out["after"] == out["before"] + 1 and out["busy"]
    assert "กำลังดำเนินการ" in toast(pg)
    return "separated submitter/approver flow · CUBE confirm modal · double ship guarded · single audit mutation"


def c_approval(pg):
    open_(pg); open_view(pg, "d12", "sign")
    t = text(pg, "#view-drawer-content")
    assert "อนุมัติการย้าย" in t, t[:1200]
    assert "มูลค่า" in t and "ข้ามคลัง/สาขา" in text(pg, "#view-drawer-content"), t[:1200]
    assert ev(pg, "()=>document.querySelectorAll('.emp-chip').length") >= 1, "no person chip"
    after(pg, "()=>{const d=findDoc('d12');d.submittedBy='ปาริชาต แก้วมณี';d.approval_chain.filter(x=>x.status==='pending').forEach(x=>x.assignee=ME.name);openRejectModal('d12');}")
    assert "เหตุผล" in text(pg, ".modal-overlay"), text(pg, ".modal-overlay")
    after(pg, "()=>{document.getElementById('md-reason').value='ข้อมูลไม่ครบ';document.getElementById('md-ok').click();}")
    assert ev(pg, "()=>findDoc('d12').status") == "draft", ev(pg, "()=>findDoc('d12').status")
    assert ev(pg, "()=>findDoc('d12').code") == "TRF-2026-0012", "document number changed"
    return "real-person approval · 2 decision groups · reject reason returns draft keeping number"


def c_lifecycle(pg):
    open_(pg); open_view(pg, "d1")
    assert ev(pg, "()=>[...document.querySelectorAll('#view-drawer-content button')].some(b=>b.innerText.includes('กลับรายการ'))"), "closed record missing reverse button"
    open_view(pg, "d10")
    assert not ev(pg, "()=>[...document.querySelectorAll('#view-drawer-content button')].some(b=>b.innerText.includes('กลับรายการ'))"), "reversed record still has reverse button"
    open_view(pg, "d3")
    assert not ev(pg, "()=>[...document.querySelectorAll('#view-drawer-content button')].some(b=>b.innerText.trim()==='ยกเลิก')"), "post-move record has cancel button"
    open_view(pg, "d9", "history")
    assert "ยกเลิก" in text(pg, "#view-drawer-content"), "cancelled history missing event"
    assert ev(pg, "()=>document.querySelectorAll('#view-drawer-content .tl button').length") == 0, "history has mutable actions"
    return "cancel pre-move only · reverse once · no delete · immutable history"


def c_scope_and_softref(pg):
    open_(pg)
    visible = text(pg)
    for forbidden in ["ค่าขนส่ง", "เลข tracking", "pick list", "สร้าง bin", "แก้ผัง"]:
        assert forbidden not in visible
    assert "ยอดที่ถูกต้อง" not in visible and "จำนวนที่ปรับ" not in visible
    open_view(pg, "d1")
    assert "2569" not in text(pg, "#view-drawer-content")
    assert "2026" in text(pg, "#view-drawer-content")
    after(pg, "()=>{findDoc('d1').whFromNameSnapshot='คลังเดิมที่ยกเลิก';renderViewDrawer();}")
    assert ev(pg, "()=>findDoc('d1')!==null")
    return "scope guards · CE dates only · soft-reference record remains renderable"


def c_pdf_and_general(pg):
    open_(pg); open_view(pg, "d1", "pdf")
    t = text(pg, "#view-drawer-content")
    for n in ["TRF-2026-0001", "คลังกลางบางนา", "คลังเชียงใหม่", "มูลค่ารวมที่ย้าย", "ผู้รับปลายทาง"]:
        assert n in t, f"PDF missing {n}: {t[:1200]}"
    assert ev(pg, "()=>document.querySelectorAll('#view-drawer-content .tab').length") >= 5, "view tabs missing"
    assert ev(pg, "()=>document.querySelectorAll('svg.lucide').length") > 20, "icons not rendered"
    return "A4 preview route/lines/totals/signatures · Pattern Q tabs · Lucide rendered"


CASES = [
    ("LIST", c_list, ["FN-43","FN-51","FN-52","FN-53","FN-90","FN-96"]),
    ("WIZARD", c_wizard_modes, ["FN-01","FN-02","FN-03","FN-04","FN-05","FN-10","FN-11"]),
    ("LINES", c_line_rules, ["FN-06","FN-07","FN-08","FN-12","FN-44"]),
    ("UPLOAD", c_upload, ["FN-53"]),
    ("LOC", c_location_contract, ["FN-15","FN-16","FN-17","FN-18","FN-19"]),
    ("NEG40", c_fn40_negative, ["FN-40"]),
    ("INTRA", c_internal_flow, ["FN-13","FN-29","FN-37"]),
    ("TRANSIT", c_inter_transit, ["FN-14","FN-20","FN-21","FN-33","FN-45"]),
    ("RECEIVE", c_receive_and_diff, ["FN-22","FN-23","FN-24","FN-28","FN-46"]),
    ("DIFF", c_shortage_seed, ["FN-25","FN-26","FN-27","FN-41"]),
    ("FIX01", c_fix01_receive_guard, []),
    ("FIX02", c_fix02_reverse_doa, []),
    ("FIX03", c_fix03_shortage_approval, []),
    ("ANCHORS", c_fix04_05_08_anchors_and_demo, []),
    ("BUSY", c_fix06_busy, []),
    ("DOA", c_approval, ["FN-30","FN-31","FN-42","FN-47"]),
    ("LIFE", c_lifecycle, ["FN-32","FN-34","FN-35","FN-36","FN-48","FN-91","FN-93","FN-94"]),
    ("SCOPE", c_scope_and_softref, ["FN-09","FN-38","FN-39","FN-49","FN-50","FN-92","FN-95"]),
    ("PDF", c_pdf_and_general, ["FN-54"]),
]

ALL_FN = sorted({x for _,_,xs in CASES for x in xs})


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        suite.watch(page)
        covered = {}
        for tid, fn, fns in CASES:
            suite.check(tid, fn.__name__, lambda fn=fn: fn(page))
            passed = suite.results[-1][2] == "PASS"
            for code in fns:
                covered[code] = covered.get(code, False) or passed
        browser.close()
    passed_cases = suite.report(exit_on_fail=False)
    passed_fn = [x for x in ALL_FN if covered.get(x)]
    failed_fn = [x for x in ALL_FN if not covered.get(x)]
    if failed_fn:
        print("FN ไม่ผ่าน:", ", ".join(failed_fn))
    print(f"FN ครอบ {len(passed_fn)}/{len(ALL_FN)} · เคสรวม {len(CASES)} · ผ่าน {passed_cases}/{len(CASES)}")
    sys.exit(0 if passed_cases == len(CASES) and len(passed_fn) == len(ALL_FN) and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
