"""Reusable rendered-UI auditor for CUBE HTML prototypes.

This module deliberately contains only cross-feature checks.  A feature audit
imports :class:`Audit` and supplies two walkers: ``walk_layout`` and
``walk_behavior``.  The implementation follows ``check_ui_prompt.md`` and is
intended to be extended centrally when a new class of defect is discovered.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Iterable

from playwright.sync_api import Browser, Page, sync_playwright


@dataclass
class Finding:
    category: str
    severity: str
    message: str
    browser: str
    width: int
    scene: str
    selector: str = ""
    measured: Any = None
    expected: Any = None
    source: str = "rendered"
    occurrences: list[dict[str, Any]] | None = None


class Audit:
    """Central UI auditor shared by every feature walk script."""

    DEFAULT_WIDTHS = (1280, 1440, 1920, 2560)
    HEIGHT = 900

    def __init__(
        self,
        target: str | Path,
        output_dir: str | Path,
        *,
        widths: Iterable[int] = DEFAULT_WIDTHS,
        browsers: Iterable[str] = ("chromium",),
        deterministic_screenshots: bool = True,
    ) -> None:
        self.target = Path(target).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.shot_root = self.output_dir / "ui-audit-shots"
        self.shot_root.mkdir(parents=True, exist_ok=True)
        self.widths = tuple(widths)
        self.browsers = tuple(browsers)
        self.deterministic_screenshots = deterministic_screenshots
        self.findings: list[Finding] = []
        self.checks: list[dict[str, Any]] = []
        self.runtime: list[dict[str, Any]] = []
        self.scans: list[dict[str, Any]] = []
        self.screenshot_pairs: list[dict[str, Any]] = []
        self.notes: list[str] = []
        self._browser_name = ""
        self._width = 0
        self._capture_pass = 1
        self._shot_index: dict[tuple[str, int, str, int], Path] = {}
        self.started_at = ""
        self.finished_at = ""

    # ---------- public helpers used by feature walkers ----------

    def open(self, page: Page, *, hash_route: str = "") -> None:
        url = self.target.as_uri()
        if hash_route:
            url += hash_route if hash_route.startswith("#") else "#" + hash_route
        page.goto(url, wait_until="load")
        page.wait_for_function("document.readyState === 'complete'")
        page.add_style_tag(
            content="""
            *,*::before,*::after {
              animation-duration: 0s !important;
              animation-delay: 0s !important;
              transition-duration: 0s !important;
              transition-delay: 0s !important;
              caret-color: transparent !important;
            }
            """
        )

    def check(
        self,
        condition: bool,
        label: str,
        *,
        category: str = "Behavior",
        measured: Any = None,
        expected: Any = True,
        severity: str = "ERROR",
        scene: str = "behavior",
        selector: str = "",
    ) -> bool:
        passed = bool(condition)
        self.checks.append(
            {
                "category": category,
                "label": label,
                "passed": passed,
                "browser": self._browser_name,
                "width": self._width,
                "scene": scene,
                "measured": measured,
                "expected": expected,
            }
        )
        if not passed:
            self.findings.append(
                Finding(
                    category=category,
                    severity=severity,
                    message=label,
                    browser=self._browser_name,
                    width=self._width,
                    scene=scene,
                    selector=selector,
                    measured=measured,
                    expected=expected,
                )
            )
        return passed

    def scan(self, page: Page, tag: str) -> dict[str, Any]:
        """Measure one fully rendered scene and save a deterministic screenshot."""
        page.wait_for_function("document.fonts ? document.fonts.status !== 'loading' : true")
        data = page.evaluate(_DOM_AUDIT_JS)
        scene = self._slug(tag)
        record = {
            "browser": self._browser_name,
            "width": self._width,
            "scene": scene,
            "pass": self._capture_pass,
            "measurements": data.get("measurements", {}),
        }
        self.scans.append(record)

        for item in data.get("findings", []):
            self.findings.append(
                Finding(
                    category=item.get("category", "Layout"),
                    severity=item.get("severity", "ERROR"),
                    message=item.get("message", "UI finding"),
                    browser=self._browser_name,
                    width=self._width,
                    scene=scene,
                    selector=item.get("selector", ""),
                    measured=item.get("measured"),
                    expected=item.get("expected"),
                    source=item.get("source", "rendered"),
                )
            )

        shot_dir = self.shot_root / f"pass-{self._capture_pass}"
        shot_dir.mkdir(parents=True, exist_ok=True)
        shot = shot_dir / f"{self._browser_name}-{self._width}-{scene}.png"
        page.screenshot(path=str(shot), full_page=True, animations="disabled")
        self._shot_index[(self._browser_name, self._width, scene, self._capture_pass)] = shot
        return data

    # ---------- orchestration ----------

    def run(
        self,
        walk_layout: Callable[["Audit", Page, str], None],
        walk_behavior: Callable[["Audit", Page], None],
    ) -> dict[str, Any]:
        self.started_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        with sync_playwright() as pw:
            for browser_name in self.browsers:
                browser_type = getattr(pw, browser_name)
                browser: Browser = browser_type.launch(headless=True)
                try:
                    passes = (1, 2) if self.deterministic_screenshots else (1,)
                    for pass_no in passes:
                        self._capture_pass = pass_no
                        for width in self.widths:
                            self._browser_name = browser_name
                            self._width = width
                            page = browser.new_page(viewport={"width": width, "height": self.HEIGHT})
                            self._watch_runtime(page, phase=f"layout-pass-{pass_no}")
                            try:
                                walk_layout(self, page, f"{browser_name}-{width}")
                            except Exception as exc:  # keep the report even when one scene fails
                                self._record_exception("Layout", "layout walker failed", exc, "walker")
                            finally:
                                page.close()

                    self._compare_screenshots(browser_name)

                    self._capture_pass = 1
                    self._width = 1440
                    page = browser.new_page(viewport={"width": 1440, "height": self.HEIGHT})
                    self._watch_runtime(page, phase="behavior")
                    try:
                        walk_behavior(self, page)
                    except Exception as exc:
                        self._record_exception("Behavior", "behavior walker failed", exc, "behavior")
                    finally:
                        page.close()
                finally:
                    browser.close()

        self.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        report = self._build_report()
        self._write_report(report)
        return report

    # ---------- reporting and runtime ----------

    def _watch_runtime(self, page: Page, *, phase: str) -> None:
        def on_console(msg) -> None:
            if msg.type not in {"error", "warning"}:
                return
            text = msg.text
            # Browser emits a URL-less generic line for failed external resources;
            # requestfailed below carries the URL and is the authoritative record.
            if text == "Failed to load resource: net::ERR_NETWORK_ACCESS_DENIED":
                return
            self.runtime.append(
                {
                    "kind": f"console-{msg.type}",
                    "external": False,
                    "message": text,
                    "browser": self._browser_name,
                    "width": self._width,
                    "phase": phase,
                }
            )

        def on_page_error(exc) -> None:
            self.runtime.append(
                {
                    "kind": "pageerror",
                    "external": False,
                    "message": str(exc),
                    "browser": self._browser_name,
                    "width": self._width,
                    "phase": phase,
                }
            )

        def on_request_failed(req) -> None:
            external = not req.url.startswith(("file:", "data:", "blob:"))
            failure = req.failure
            self.runtime.append(
                {
                    "kind": "requestfailed",
                    "external": external,
                    "message": f"{req.url} — {failure}",
                    "browser": self._browser_name,
                    "width": self._width,
                    "phase": phase,
                }
            )

        page.on("console", on_console)
        page.on("pageerror", on_page_error)
        page.on("requestfailed", on_request_failed)

    def _record_exception(self, category: str, label: str, exc: Exception, scene: str) -> None:
        self.findings.append(
            Finding(
                category=category,
                severity="ERROR",
                message=f"{label}: {type(exc).__name__}: {exc}",
                browser=self._browser_name,
                width=self._width,
                scene=scene,
                source="runner",
            )
        )

    def _compare_screenshots(self, browser_name: str) -> None:
        keys = sorted(
            (b, w, scene)
            for (b, w, scene, pass_no) in self._shot_index
            if b == browser_name and pass_no == 1
        )
        for b, width, scene in keys:
            first = self._shot_index.get((b, width, scene, 1))
            second = self._shot_index.get((b, width, scene, 2))
            if not first or not second:
                self.findings.append(
                    Finding(
                        category="Visual stability",
                        severity="ERROR",
                        message="ไม่มีภาพคู่สำหรับตรวจความนิ่ง",
                        browser=b,
                        width=width,
                        scene=scene,
                        measured=str(first or second or "missing"),
                        expected="pass-1 and pass-2",
                        source="screenshot",
                    )
                )
                continue
            hash1 = self._sha256(first)
            hash2 = self._sha256(second)
            same = hash1 == hash2
            pair = {
                "browser": b,
                "width": width,
                "scene": scene,
                "identical": same,
                "sha256_pass_1": hash1,
                "sha256_pass_2": hash2,
                "bytes_pass_1": first.stat().st_size,
                "bytes_pass_2": second.stat().st_size,
            }
            self.screenshot_pairs.append(pair)
            if not same:
                self.findings.append(
                    Finding(
                        category="Visual stability",
                        severity="ERROR",
                        message="ภาพสอง pass ไม่เหมือนกันทุกไบต์",
                        browser=b,
                        width=width,
                        scene=scene,
                        measured=pair,
                        expected="identical SHA-256",
                        source="screenshot",
                    )
                )

    def _build_report(self) -> dict[str, Any]:
        external_requests = [
            r for r in self.runtime if r["external"] and r["kind"] == "requestfailed"
        ]
        # Correlate library fallback warnings with the failed external request
        # URLs.  The URL evidence, not the console message alone, determines
        # that these are environmental rather than application runtime errors.
        if any(
            any(host in r["message"] for host in ("unpkg.com", "jsdelivr.net", "cdnjs.cloudflare.com"))
            for r in external_requests
        ):
            for item in self.runtime:
                if item["kind"].startswith("console-") and item["message"].startswith("[Lucide] All CDNs failed"):
                    item["external"] = True
                    item["correlated_to"] = "failed external CDN request URLs"

        internal_runtime = [r for r in self.runtime if not r["external"]]
        external_runtime = [r for r in self.runtime if r["external"]]
        if internal_runtime:
            for item in internal_runtime:
                self.findings.append(
                    Finding(
                        category="Runtime",
                        severity="ERROR",
                        message=item["message"],
                        browser=item["browser"],
                        width=item["width"],
                        scene=item["phase"],
                        source=item["kind"],
                    )
                )

        # The same source defect can appear at many viewports/passes.  Keep all
        # measurements in scans, but deduplicate the actionable finding list.
        unique: dict[tuple[Any, ...], Finding] = {}
        for finding in self.findings:
            key = (
                finding.category,
                finding.severity,
                finding.message,
                finding.selector,
                finding.source,
                json.dumps(finding.expected, ensure_ascii=False, sort_keys=True, default=str),
            )
            occurrence = {
                "browser": finding.browser,
                "width": finding.width,
                "scene": finding.scene,
                "measured": finding.measured,
            }
            if key in unique:
                unique[key].occurrences.append(occurrence)
            else:
                finding.occurrences = [occurrence]
                unique[key] = finding
        self.findings = list(unique.values())
        errors = sum(1 for f in self.findings if f.severity == "ERROR")
        warnings = sum(1 for f in self.findings if f.severity == "WARN")
        passed_checks = sum(1 for c in self.checks if c["passed"])
        report = {
            "target": str(self.target),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "browsers": list(self.browsers),
            "viewports": [{"width": w, "height": self.HEIGHT} for w in self.widths],
            "status": "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
            "summary": {
                "errors": errors,
                "warnings": warnings,
                "checks_passed": passed_checks,
                "checks_total": len(self.checks),
                "internal_runtime_events": len(internal_runtime),
                "external_runtime_events": len(external_runtime),
                "screenshot_pairs": len(self.screenshot_pairs),
                "stable_screenshot_pairs": sum(1 for p in self.screenshot_pairs if p["identical"]),
            },
            "findings": [asdict(f) for f in self.findings],
            "checks": self.checks,
            "scans": self.scans,
            "runtime": self.runtime,
            "screenshot_pairs": self.screenshot_pairs,
            "manual_review_required": [
                "ความสวยงามและจังหวะการจัดวางโดยรวม",
                "ลำดับงานและ microcopy เข้าใจง่ายสำหรับผู้ใช้จริงหรือไม่",
                "ประสบการณ์ screen reader เชิงความหมาย",
                "native browser tooltip ซึ่ง Playwright วัดกล่องภายในไม่ได้",
            ],
            "notes": self.notes,
        }
        return report

    def _write_report(self, report: dict[str, Any]) -> None:
        json_path = self.output_dir / "UI_AUDIT_RESULT.json"
        md_path = self.output_dir / "UI_AUDIT_REPORT.md"
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        lines = [
            "# UI Audit Report",
            "",
            f"- Target: `{report['target']}`",
            f"- Status: **{report['status']}**",
            f"- Viewports: {', '.join(str(v['width']) for v in report['viewports'])}",
            f"- Browsers: {', '.join(report['browsers'])}",
            f"- Errors: {report['summary']['errors']}",
            f"- Warnings: {report['summary']['warnings']}",
            f"- Behavior checks: {report['summary']['checks_passed']}/{report['summary']['checks_total']}",
            f"- Stable screenshot pairs: {report['summary']['stable_screenshot_pairs']}/{report['summary']['screenshot_pairs']}",
            f"- Internal runtime events: {report['summary']['internal_runtime_events']}",
            f"- External runtime events: {report['summary']['external_runtime_events']}",
            "",
            "## Findings",
            "",
        ]
        if report["findings"]:
            for index, item in enumerate(report["findings"], 1):
                lines.extend(
                    [
                        f"### {index}. [{item['severity']}] {item['category']} — {item['message']}",
                        "",
                        f"- Scene: `{item['scene']}` · {item['browser']} {item['width']}px",
                        f"- Selector: `{item['selector'] or '-'}`",
                        f"- Measured: `{json.dumps(item['measured'], ensure_ascii=False, default=str)}`",
                        f"- Expected: `{json.dumps(item['expected'], ensure_ascii=False, default=str)}`",
                        "",
                    ]
                )
        else:
            lines.extend(["ไม่พบ finding จากตัวตรวจอัตโนมัติ", ""])
        lines.extend(["## Manual review still required", ""])
        lines.extend(f"- {item}" for item in report["manual_review_required"])
        lines.append("")
        md_path.write_text("\n".join(lines), encoding="utf-8")

    @staticmethod
    def _slug(value: str) -> str:
        value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-")
        return value[:100] or "scene"

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


# Executed in the browser so every geometry result is based on rendered pixels,
# not assumptions from source code.  Results are intentionally capped per check;
# more than ~30 similar findings usually indicates a detector problem.
_DOM_AUDIT_JS = r"""
() => {
  const findings = [];
  const LIMIT = 30;
  const px = n => Math.round(n * 100) / 100;
  const visible = el => {
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity) !== 0 && r.width > 0 && r.height > 0;
  };
  const selector = el => {
    if (!el) return '';
    if (el.id) return '#' + CSS.escape(el.id);
    const parts = [];
    let node = el;
    while (node && node !== document.body && parts.length < 4) {
      let part = node.tagName.toLowerCase();
      if (node.classList.length) part += '.' + [...node.classList].slice(0, 2).map(CSS.escape).join('.');
      if (node.parentElement) {
        const peers = [...node.parentElement.children].filter(x => x.tagName === node.tagName);
        if (peers.length > 1) part += `:nth-of-type(${peers.indexOf(node) + 1})`;
      }
      parts.unshift(part); node = node.parentElement;
    }
    return parts.join(' > ');
  };
  const add = (category, severity, message, el, measured, expected, source='rendered') => {
    if (findings.length >= LIMIT) return;
    findings.push({category, severity, message, selector: selector(el), measured, expected, source});
  };
  const rect = el => {
    const r = el.getBoundingClientRect();
    return {left:px(r.left), top:px(r.top), right:px(r.right), bottom:px(r.bottom), width:px(r.width), height:px(r.height)};
  };

  // CSS source checks: undefined variables and classes used without definitions.
  let cssText = '';
  for (const sheet of [...document.styleSheets]) {
    try { cssText += [...sheet.cssRules].map(r => r.cssText).join('\n') + '\n'; } catch (_) {}
  }
  const declaredVars = new Set([...cssText.matchAll(/(--[\w-]+)\s*:/g)].map(m => m[1]));
  const usedVars = new Set([...cssText.matchAll(/var\(\s*(--[\w-]+)/g)].map(m => m[1]));
  const missingVars = [...usedVars].filter(v => !declaredVars.has(v)).sort();
  if (missingVars.length) add('Layout', 'ERROR', 'CSS variable ถูกเรียกใช้แต่ไม่ได้ประกาศ', document.documentElement, missingVars, [] ,'source-css');

  const definedClasses = new Set([...cssText.matchAll(/\.(-?[_a-zA-Z]+(?:\\.|[_a-zA-Z0-9-])*)/g)].map(m => m[1].replace(/\\(.)/g,'$1')));
  const ignoredClasses = new Set(['lucide', 'is-open', 'is-active', 'is-on', 'is-danger', 'is-warning', 'is-info', 'is-vat', 'is-wht', 'standard']);
  const usedClasses = new Map();
  for (const el of document.querySelectorAll('[class]')) for (const c of el.classList) usedClasses.set(c, (usedClasses.get(c)||0)+1);
  const undefinedClasses = [...usedClasses].filter(([c]) => !definedClasses.has(c) && !ignoredClasses.has(c) && !c.startsWith('lucide-')).map(([name,count]) => ({name,count})).sort((a,b)=>a.name.localeCompare(b.name));
  if (undefinedClasses.length) add('Layout', 'WARN', 'markup ใช้ class ที่ไม่มีนิยาม CSS', document.body, undefinedClasses.slice(0,20), [], 'source-css');

  // Page-level horizontal overflow.
  const pageOverflow = Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth;
  if (pageOverflow > 2) add('Responsive', 'ERROR', 'หน้าเกิด horizontal scroll ที่ไม่ตั้งใจ', document.documentElement, {overflowPx:px(pageOverflow), scrollWidth:document.documentElement.scrollWidth, viewport:innerWidth}, {overflowPx:0});

  const all = [...document.querySelectorAll('body *')].filter(visible);

  // Clipping by non-scrollable ancestors.
  for (const el of all) {
    if (findings.length >= LIMIT) break;
    if (getComputedStyle(el).position === 'fixed') continue;
    const er = el.getBoundingClientRect();
    let parent = el.parentElement;
    while (parent && parent !== document.body) {
      const ps = getComputedStyle(parent), pr = parent.getBoundingClientRect();
      const clipsX = ['hidden','clip'].includes(ps.overflowX);
      const clipsY = ['hidden','clip'].includes(ps.overflowY);
      const dx = clipsX ? Math.max(0, pr.left-er.left, er.right-pr.right) : 0;
      const dy = clipsY ? Math.max(0, pr.top-er.top, er.bottom-pr.bottom) : 0;
      if (dx > 2 || dy > 2) {
        add('Layout','ERROR','element ถูก overflow ของกล่องแม่ตัด',el,{clippedX:px(dx),clippedY:px(dy),element:rect(el),parent:rect(parent),parentOverflow:`${ps.overflowX}/${ps.overflowY}`},{clippedX:0,clippedY:0});
        break;
      }
      parent = parent.parentElement;
    }
  }

  // Text overflow when the content is not intentionally scrollable.
  for (const el of all) {
    if (findings.length >= LIMIT) break;
    const s = getComputedStyle(el);
    if (!el.textContent.trim() || ['inline','contents'].includes(s.display)) continue;
    if (['auto','scroll'].includes(s.overflowX)) continue;
    const overflow = el.scrollWidth - el.clientWidth;
    if (overflow > 3 && ['hidden','clip'].includes(s.overflowX)) {
      add('Layout','ERROR','ข้อความล้นกล่องและถูกตัด',el,{overflowPx:px(overflow),clientWidth:el.clientWidth,scrollWidth:el.scrollWidth},{overflowPx:0});
    }
  }

  // CSS dimensions/margins that cannot affect inline elements.
  for (const el of all) {
    const s = getComputedStyle(el);
    if (s.display !== 'inline') continue;
    const hasIneffective = (s.width !== 'auto') || (s.height !== 'auto') || parseFloat(s.marginTop) || parseFloat(s.marginBottom);
    if (hasIneffective) add('Layout','WARN','CSS width/height/vertical margin ไม่มีผลเพราะ element เป็น inline',el,{width:s.width,height:s.height,marginTop:s.marginTop,marginBottom:s.marginBottom},'display:inline-block/flex/block');
  }

  // Table descendants must stay inside their own cell.
  for (const td of document.querySelectorAll('td,th')) {
    if (!visible(td)) continue;
    const tr = td.getBoundingClientRect();
    for (const child of td.querySelectorAll('*')) {
      if (!visible(child) || getComputedStyle(child).position === 'fixed') continue;
      const cr = child.getBoundingClientRect();
      const overflow = Math.max(0, tr.left-cr.left, cr.right-tr.right);
      if (overflow > 2) { add('Layout','ERROR','เนื้อหาในเซลล์ล้นไปยังคอลัมน์ข้างเคียง',child,{overflowPx:px(overflow),cell:rect(td),child:rect(child)},{overflowPx:0}); break; }
    }
  }

  // Controls sharing a visual row: same-cell top alignment; cross-cell center alignment.
  for (const row of document.querySelectorAll('tr')) {
    if (!visible(row) || row.querySelector('[colspan]')) continue;
    const controls = [...row.querySelectorAll('button,input,select,textarea,[role=button]')].filter(visible).filter(el => !el.classList.contains('btn-sm'));
    const byCell = new Map();
    for (const el of controls) { const cell = el.closest('td,th'); if (!cell) continue; if (!byCell.has(cell)) byCell.set(cell,[]); byCell.get(cell).push(el); }
    const representatives = [...byCell.values()].map(v=>v[0]);
    if (representatives.length > 1) {
      const centers = representatives.map(el => { const r=el.getBoundingClientRect(); return r.top+r.height/2; });
      const delta = Math.max(...centers)-Math.min(...centers);
      if (delta > 3) add('Layout','WARN','control คนละเซลล์มีกึ่งกลางแนวตั้งไม่ตรงกัน',row,{centerDeltaPx:px(delta),centers:centers.map(px)},{centerDeltaPx:'<=3'});
    }
    for (const group of byCell.values()) if (group.length > 1) {
      const tops = group.map(el=>el.getBoundingClientRect().top), delta=Math.max(...tops)-Math.min(...tops);
      if (delta > 3) add('Layout','WARN','control ในเซลล์เดียวกันขอบบนไม่ตรงกัน',group[0],{topDeltaPx:px(delta)},{topDeltaPx:'<=3'});
    }
  }

  // Interactive controls in common flex/grid rows should have consistent height.
  for (const host of document.querySelectorAll('.toolbar,.filter-bar,.filters,.form-row,.ph-actions,.drawer-footer,.modal-footer')) {
    if (!visible(host)) continue;
    const controls = [...host.querySelectorAll(':scope > button,:scope > input,:scope > select,:scope > .btn,:scope > .field')].filter(visible).filter(el=>!el.classList.contains('btn-sm'));
    if (controls.length < 2) continue;
    const heights=controls.map(el=>el.getBoundingClientRect().height), delta=Math.max(...heights)-Math.min(...heights);
    if (delta > 3) add('Layout','WARN','ปุ่ม/input ในแถวเดียวกันสูงไม่เท่ากัน',host,{heightDeltaPx:px(delta),heights:heights.map(px)},{heightDeltaPx:'<=3'});
  }

  const sampleOcclusion = (overlay, category, message) => {
    const r=overlay.getBoundingClientRect(), inset=Math.min(18,r.width/5,r.height/5);
    const points=[[r.left+inset,r.top+inset],[r.left+r.width/2,r.top+inset],[r.right-inset,r.top+inset],[r.left+inset,r.top+r.height/2],[r.right-inset,r.top+r.height/2],[r.left+inset,r.bottom-inset],[r.left+r.width/2,r.bottom-inset],[r.right-inset,r.bottom-inset]];
    const leaks=[];
    for (const [x,y] of points) { const hit=document.elementFromPoint(x,y); if (hit && !overlay.contains(hit)) leaks.push({x:px(x),y:px(y),hit:selector(hit)}); }
    if (leaks.length) add(category,'ERROR',message,overlay,{leakCount:leaks.length,points:leaks},{leakCount:0});
  };
  const overlayLayer = el => {
    let node=el;
    while(node && node!==document.documentElement){
      const z=getComputedStyle(node).zIndex;
      if(z!=='auto' && Number.isFinite(Number(z))) return Number(z);
      node=node.parentElement;
    }
    return 0;
  };
  const visibleOverlays=[...document.querySelectorAll('.drawer.is-open,.modal-backdrop.is-open .modal,[role=dialog]')].filter(visible);
  const topOverlayLayer=visibleOverlays.length ? Math.max(...visibleOverlays.map(overlayLayer)) : 0;
  // A lower drawer being covered by a confirmation modal is intentional.  Only
  // the topmost active overlay must own all sampled points.
  for (const overlay of visibleOverlays.filter(el=>overlayLayer(el)===topOverlayLayer)) sampleOcclusion(overlay,'Layout','element ภายนอกวาดทับ overlay ที่เปิดอยู่');
  for (const menu of document.querySelectorAll('.ss-list:not(.hidden),[role=listbox],.dropdown-menu.is-open')) if (visible(menu)) sampleOcclusion(menu,'Layout','element ภายนอกวาดทับ dropdown ที่เปิดอยู่');

  // Drawer/modal close action placement.
  for (const header of document.querySelectorAll('.drawer-header,.modal-header')) {
    if (!visible(header)) continue;
    const close=[...header.querySelectorAll('button')].find(b=>/^(ปิด|close)$/i.test(((b.getAttribute('aria-label')||b.title||'').trim())));
    if (!close) { add('Accessibility','ERROR','หัว drawer/modal ไม่มีปุ่มปิดที่ระบุชื่อได้',header,null,'close button'); continue; }
    const hr=header.getBoundingClientRect(), cr=close.getBoundingClientRect();
    const controls=[...header.querySelectorAll('button')].filter(visible), rightmost=Math.max(...controls.map(b=>b.getBoundingClientRect().right));
    const title=header.querySelector('h1,h2,h3,.drawer-title,.modal-title');
    const rowDelta=title ? Math.abs((title.getBoundingClientRect().top+title.getBoundingClientRect().height/2)-(cr.top+cr.height/2)) : 0;
    if (rightmost-cr.right>2 || rowDelta>12) add('Layout','ERROR','ปุ่มปิดไม่อยู่ขวาสุดในแถวเดียวกับหัวข้อ',close,{rightGapToRightmost:px(rightmost-cr.right),centerDeltaPx:px(rowDelta),headerRightGap:px(hr.right-cr.right)},{rightGapToRightmost:0,centerDeltaPx:'<=12'});
  }

  // Keyboard reachability.  Backdrops and propagation-only wrappers are excluded.
  const clickables=[...document.querySelectorAll('button,a[href],input,select,textarea,[role=button],[onclick]')].filter(visible);
  for (const el of clickables) {
    if (el.matches('.drawer-backdrop,.modal-backdrop') || /stopPropagation\s*\(\s*\)/.test(el.getAttribute('onclick')||'')) continue;
    const intrinsically=/^(BUTTON|A|INPUT|SELECT|TEXTAREA)$/.test(el.tagName) || el.getAttribute('role')==='button' || el.tabIndex>=0;
    if (intrinsically) continue;
    const own=(el.getAttribute('onclick')||'').match(/([\w$]+)\s*\(/)?.[1];
    const equivalent=[...el.querySelectorAll('button,a[href],input,select,textarea,[role=button],[tabindex]')].some(child=>{
      const fn=(child.getAttribute('onclick')||'').match(/([\w$]+)\s*\(/)?.[1]; return own && fn===own;
    });
    if (!equivalent) add('Accessibility','ERROR','element ที่คลิกได้ไม่สามารถโฟกัสด้วยคีย์บอร์ด',el,{tag:el.tagName,tabIndex:el.tabIndex,handler:own||null},'focusable or equivalent focusable control');
  }

  // Basic accessible names.
  for (const el of clickables.filter(el=>/^(BUTTON|A)$/.test(el.tagName) || el.getAttribute('role')==='button')) {
    const name=(el.getAttribute('aria-label')||el.title||el.textContent||'').trim();
    if (!name) add('Accessibility','ERROR','interactive control ไม่มี accessible name',el,null,'non-empty accessible name');
  }

  // WCAG contrast for visible leaf text.  Gradients and transparent foregrounds are skipped.
  const parseColor = value => {
    let m=value.match(/rgba?\(([^)]+)\)/);
    if(m){const p=m[1].split(',').map(Number);return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};}
    m=value.match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)/);
    if(m)return {r:Number(m[1])*255,g:Number(m[2])*255,b:Number(m[3])*255,a:m[4]?Number(m[4]):1};
    return null;
  };
  const lum = c => { const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}; return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b); };
  const background = el => { let n=el; while(n&&n!==document.documentElement){const s=getComputedStyle(n);if(s.backgroundImage!=='none')return null;const c=parseColor(s.backgroundColor);if(c&&c.a>=.98)return c;n=n.parentElement;}return {r:255,g:255,b:255,a:1}; };
  let contrastFailures=0;
  for (const el of all) {
    if (contrastFailures>=12) break;
    if ([...el.children].some(visible) || !el.textContent.trim()) continue;
    const s=getComputedStyle(el), fg=parseColor(s.color), bg=background(el); if(!fg||!bg||fg.a<.98)continue;
    const l1=lum(fg),l2=lum(bg),ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
    const size=parseFloat(s.fontSize), bold=parseInt(s.fontWeight)>=700, large=size>=24||(size>=18.66&&bold), required=large?3:4.5;
    if(ratio+0.01<required){contrastFailures++;add('Accessibility','ERROR','text contrast ต่ำกว่า WCAG AA',el,{ratio:px(ratio),fontSizePx:px(size),fontWeight:s.fontWeight,foreground:s.color,background:`rgb(${bg.r}, ${bg.g}, ${bg.b})`},{ratio:`>=${required}`});}
  }

  const focusRulePresent=/:focus-visible/.test(cssText);
  if (!focusRulePresent) add('Accessibility','ERROR','CSS ไม่มี focus-visible treatment',document.documentElement,false,true,'source-css');

  return {
    findings,
    measurements: {
      viewport:{width:innerWidth,height:innerHeight},
      document:{scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight},
      visibleElements:all.length,
      clickableElements:clickables.length,
      undefinedCssVariables:missingVars.length,
      undefinedClasses:undefinedClasses.length,
      contrastFailures,
      findingCount:findings.length,
      findingLimitReached:findings.length>=LIMIT,
      focusVisibleRulePresent:focusRulePresent
    }
  };
}
"""
