# HTML freeze edit sync

Pre-document correction: strict calendar-date validation was added after first S3c freeze and before BRD/FRD authoring. S3a v9 audit rerun FAIL=0/WARN=2; S3b isolated domain assertions rerun 18/18; S3c official renderer retried twice with Playwright unavailable. The new freeze hash is in HTML_FREEZE_SHA256.txt. No FRD existed at edit time, so html-to-frd-sync has no FRD target; the corrected behavior is now the source for first FRD authoring.
