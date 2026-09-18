# S7.5 UI Brief source gate

PASS for source-anchored extraction: three routes mapped, four overlay types (drawer/backdrop/picker/toast), state matrix, z-index, Esc/outside-click, verbatim labels/messages, backend/FRD mapping and demo-only section. All claims point to `_lane_tools/build.py` and `_lane_tools/rop_inject.js` authored source from the frozen build; generated HTML was not reread in the feature. Actual visual typography/layout and button interaction remain WARN because Playwright was unavailable. No new UI requirement silently introduced; one proposal is separated in §13.
