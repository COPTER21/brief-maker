# 06_TESTS — F-WH-LOT

## Acceptance ledger (route and visible text anchors)
| ID | Given | When | Then / observable assertion | Route |
|---|---|---|---|---|
| AT-01 | ITEM-101/102 policies | change ITEM-101 mode and save “บันทึกการตั้งค่า” | ITEM-101 changes only; history event appended; movement snapshot unchanged | #/settings |
| AT-02 | ITEM-101 expiry enabled | save create with blank `#f3` | “กรอกวันหมดอายุ”; row/event counts unchanged | drawer on #/records |
| AT-03 | ITEM-103 expiry disabled | save with blank expiry | “บันทึกแล้ว”; null expiry; no movement added | drawer on #/records |
| AT-04 | ITEM-102 serial SN-102 exists | create SN-102 again | “ซีเรียลนี้ถูกใช้แล้ว”; no duplicate row/event | drawer |
| AT-05 | Oct01, Oct15, expired Sep01, fully held Nov01 fixture | click “แนะนำล็อต” for ITEM-101 | Oct01 then Oct15; excluded others; lotRows/movement snapshots unchanged | #/settings |
| AT-06 | ITEM-103 expiry disabled | click “แนะนำล็อต” | earliest receivedAt first; valuation method unchanged | #/settings |
| AT-07 | LOT-2609-011 and 012 refs | select each trace lot | 011 has GRN-2609-014/Transfer-2609-009, 012 GRN-2609-016; selected detail previous/next correct | #/history |
| AT-08 | seven fixture lots | search, filter, sort, cancel drawer | visible table/count order correct; cancel no create | #/records |
| AT-09 | NC rules external | click “เปิดกฎแจ้งเตือน” | hook acknowledgement; no local threshold/channel stored | #/settings |
| AT-10 | valid lot-mode (nonserial) identity submitted | replay same input/key | local “รายการนี้ส่งแล้ว” before a second create; production same key returns prior result and one event | drawer |
| AT-11 | no matching rows | search unmatched text | “ไม่พบรายการที่ตรงกับตัวกรอง” | #/records |
| AT-12 | any open drawer | press Esc | drawer/backdrop close, no write | drawer |

## §6.9 Cross-module mock contract tests
| ID | Boundary | Only assert | Must not assert |
|---|---|---|---|
| XT-01 | W3-LITE GRN/Transfer movement | request/read shape, selected lot ref, missing-source empty/unavailable, no local movement mutation | actual GRN posting/Transfer reversal |
| XT-02 | NC expiry | event candidate/ref envelope and soft hook, no local threshold | notification channel/delivery |
| XT-03 | Picking | ordered candidate payload and unchanged availability; consumer revalidation contract | reservation/issue posted |
| XT-04 | CSQ | `master.changed` envelope/idempotency shape; engine mock ack | 7C result or registry connected |

## DoD and limits
AT/XT trace to BRD stories/rules via 00_OVERVIEW §0.12. Browser visual interactions are not claimed tested in S3c. Unit domain tests 8/8 cover conditional date, serial, FEFO/FIFO, trace fixture, isolation and immutability. Server uniqueness, permission and cross-lane integration require implementation tests later.
