# S3a UX gate — Stocktake · v9

Verdict **WARN**, BLOCK 0 pending browser interaction. `audit.sh` FAIL=0/WARN=2 (literal font-size token and missing submit loader); Node syntax PASS. `self_audit.py` true spacing/hex/z/extra inline findings fixed. Remaining raw FAIL comes from exactly three inline widths required by verbatim #106 toolbar block and `.tabs/.tab` required by #104 (older scanner calls custom tabs); no v9 contradiction is introduced by the UI. #67.1 no hint/info banner; #104 tab row directly below `.ph` before stats/filter; #105 `data-demo="persona-switch"` + visible DEMO badge; #106 `.toolbar > .search-box` and 200/180px selects, reset in same flex row.

WARN UX-01 `#/sheets`/`#/variance` submit buttons are synchronous mock; add disabled/loading during real wiring. WARN UX-02 fixed font tokens have a few literal display sizes; UI owner polishes during vibe. Browser full state transition and 1024 render are S3c evidence, not assumed here.
