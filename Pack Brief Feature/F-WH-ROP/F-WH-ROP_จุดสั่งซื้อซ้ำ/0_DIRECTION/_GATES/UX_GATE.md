# S3a — ROP UX and v9 gate

Verdict: WARN. v9 audit FAIL=0, WARN=2 (Lucide icon class in canonical toolbar, hardcoded token in v9 shell). self_audit reports inline_layout=3 from the exact canonical `.toolbar>.search-box` block required by Golden Rule #106, missing_ids=5 from parser scanning JS template/dynamic picker IDs, and custom_tabs=2 from the canonical page-head-adjacent tabs. These are lint heuristics, not observed runtime defects. No browser rendering is claimed.

Source inspection before freeze confirms policy, suggestion, and history tabs render distinct rows through the shared canonical toolbar; action buttons sit in page-head; no hint/banner; picker is a searchable combobox. All 17 isolated domain assertions pass in DOMAIN_TEST.json. Remaining visual and interaction evidence belongs to S3c/S6b and is not asserted here.
