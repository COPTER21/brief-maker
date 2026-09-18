# 07_LOCKED_DECISIONS — F-WH-STKTRF

## 7.0 Imported immutable scope locks

| ID | Locked decision |
|---|---|
| LK-1 | Q-document full archetype with B2 v2 line editor |
| LK-2 | Transfer between warehouses/branches is in scope |
| LK-3 | Cross-warehouse always passes through in-transit; shipment is not receipt |
| LK-4 | Destination confirmation closes cross-warehouse transfer |
| LK-5 | DOA picker selects real people; role IDs and hardcoded chains are forbidden |
| LK-6 | Numbering/document storage use DOCCFG and printable document contract |
| LK-7 | JE is mock/pending only; actual posting is future W5 |
| LK-8 | Inventory movement is append-only; correction uses reversal |
| LK-9 | Location model is inherited from Putaway and must not be redefined |
| LK-10 | Stock adjustment and stock count are outside this feature |
| LK-11 | Gregorian year, CUBE Warm Light, and registered warehouse navigation |

## 7.1 Implementation decisions

- One transfer contains one source/destination warehouse pair.
- Client never selects the transit location directly.
- Reversal is a new approval-controlled transfer; no movement exists before execution.
- Shortage remains partial until all shortage approvers finish.
- Native browser confirm is not permitted for transaction actions.

## 7.2 Open decisions

BRD OQ-TRF-01..08 remain visible and use their interim values. A decision that conflicts with LK-1..11 requires an approved BRD revision before code changes.

