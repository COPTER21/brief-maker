# 07_LOCKED — F-WH-LOT

## §7.0 Scope lock
LOCK-W4-LOT from internal W4 pack/RIF §16.3/BRD §3.4: console/master only; no Pattern Q; no GRN/Transfer/QHold/NC/Picking implementation; read-only mocks and soft hooks only. HTML freezes after S3.

## Locked defaults and owner
| Decision | Value | Source | Owner |
|---|---|---|---|
| OQ-LOT-01 | FEFO for expiry-enabled item; non-expiry receipt order | W4 §3 [ASSUMED] | Warehouse Product Owner |
| Master soft refs | picker snapshot, not hard FK | LD-4C-02 | Central Architecture |
| Append-only movement | no edit/delete | Golden 4 | Warehouse Architecture |
| NC threshold | central NC rules | W4 §2 | NC owner |
| Declaration chip | csq only, NTF detection divergent | Feature list | Registry owner |

## Further [ASSUMED] resolutions before production
Serial qty=1, FEFO tie-break, effective date/old-policy treatment, tenant date comparison, W3-LITE movement/availability payload, Security classification of actor id. Named owners in 00_OVERVIEW §0.8. Until resolved, these are explicit defaults for specification and mock behavior, not secretly approved external contracts.
