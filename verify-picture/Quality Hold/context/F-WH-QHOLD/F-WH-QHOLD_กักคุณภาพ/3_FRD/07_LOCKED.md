# Locked decisions and open questions
LOCK-01 console/master, no wizard; LOCK-02 DOA actual people; LOCK-03 held excluded ATP; LOCK-04 append-only; LOCK-05 external mock limits; LOCK-06 data-derived list; LOCK-07 UI rules 67.1/104/105/106; LOCK-08 HTML freeze post S3. Sources BRD §3.4, Scope Lock.

| OQ | Default and status | Owner |
|---|---|---|
| OQ-QH-01 | held onHand, not ATP `[ASSUMED]` | Warehouse Product Owner + Inventory owner |
| OQ-QH-02 | pending hold blocks ATP immediately `[ASSUMED]` | Warehouse Product Owner |
| OQ-QH-03 | pending release reserves held, no ATP free `[ASSUMED]` | Warehouse Product Owner |
| OQ-QH-04 | DOA policy slots/eligible person and event key mock `[ASSUMED contract]` | DOA owner |
| OQ-QH-05 | EA integer demo precision and UoM production `[ASSUMED]` | Item/Inventory owner |
| OQ-QH-06 | GRN/NC/CSQ external payload/ref `[ASSUMED contract]` | GRN/NC/CSQ owners |
| OQ-QH-07 | maker/approver SoD and effective policy `[ASSUMED]` | DOA/Security owner |

Changes to defaults require owner decision in production backlog; frozen HTML changes require S3a–c plus html-to-frd-sync.
