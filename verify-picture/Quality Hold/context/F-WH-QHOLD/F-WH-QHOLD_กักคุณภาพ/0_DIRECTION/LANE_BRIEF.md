# LANE_BRIEF · F-WH-QHOLD · Quality Hold / กักคุณภาพ

> W4B FULL · 2026-09-14 · AI 100% no-vibe · console/master, no Pattern Q

## Intent
Hold or release identified stock slice by Item/Warehouse/location/lot for GRN QC mock or later issue, through configured DOA real-person slots. Held quantity stays onHand but is excluded from ATP and transferable quantity; stock/movement ledger remains unchanged. Hold/release decisions produce append-only quarantine events. NC/NTF and CSQ are declaration producer contracts only. GRN QC W3-LITE is mock `[ASSUMED contract]` and no GRN or transfer/sale is implemented. Chips from FEATURE_LIST: `doa,ntf,csq`.

## Dependency and owner boundary
Existing Warehouse & Bin F008 and Inventory ATP F009 are upstream reads; Lot/Serial F087 is W4A done and supplies lot soft refs; GRN F079 W3-LITE pending is mock source. Item master/UoM row is not explicit in FEATURE_LIST_ALL; use existing master picker and record source gap, not a new master implementation. DOA engine supplies slot definitions/eligible people and external decisions; no fixed manager chain. NC decides recipients/channel. No Stock Adjustment or JE posting in QHold.

## Default decisions to carry
OQ-QH-01/W4 §3: held onHand but not ATP `[ASSUMED]`. Pending hold quarantine timing is unspecified in source: safest local default pending hold blocks ATP immediately `[ASSUMED]`, Warehouse Product Owner owns confirmation. Pending release does not free ATP until approved. Approval person slots and decisions are external mock; no auto-approve. Detailed arithmetic and acceptance in PREBRIEF/FRD/TC.
