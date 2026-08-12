#!/usr/bin/env bash
# gate: จับศัพท์ระบบหลุด + placeholder ค้าง + CDN ต้องห้าม
# usage: bash scripts/check.sh <file.html>
here="$(cd "$(dirname "$0")" && pwd)"
python3 "$here/check.py" "$@"
