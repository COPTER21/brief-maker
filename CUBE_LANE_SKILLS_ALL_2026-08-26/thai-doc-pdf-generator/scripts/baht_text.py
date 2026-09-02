#!/usr/bin/env python3
"""
baht_text.py — convert a number to Thai baht text (จำนวนเงินเป็นตัวอักษร).

Follows the standard Thai convention used on invoices/receipts:
- "...บาทถ้วน" when no satang
- satang rendered as "...สตางค์"
- correct "เอ็ด" / "ยี่" handling

CLI:   python baht_text.py 1234567.50   -> หนึ่งล้านสองแสน...บาทห้าสิบสตางค์
Import: from baht_text import baht_text;  baht_text(1234.00)
"""
import sys
from decimal import Decimal, ROUND_HALF_UP

_DIGITS = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
_PLACES = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]


def _read_int(num_str: str) -> str:
    """Read an integer string (no commas) as Thai words."""
    num_str = num_str.lstrip("0") or "0"
    if num_str == "0":
        return "ศูนย์"
    # handle millions recursively (Thai groups by 6 digits with 'ล้าน')
    if len(num_str) > 6:
        head, tail = num_str[:-6], num_str[-6:]
        return _read_int(head) + "ล้าน" + (_read_int(tail) if tail.lstrip("0") else "")
    words = ""
    n = len(num_str)
    for i, ch in enumerate(num_str):
        d = int(ch)
        place = n - i - 1
        if d == 0:
            continue
        if place == 1 and d == 1:          # สิบ
            words += "สิบ"
        elif place == 1 and d == 2:        # ยี่สิบ
            words += "ยี่สิบ"
        elif place == 0 and d == 1 and n > 1:  # ...เอ็ด
            words += "เอ็ด"
        else:
            words += _DIGITS[d] + _PLACES[place]
    return words


def baht_text(amount) -> str:
    amt = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    neg = amt < 0
    amt = abs(amt)
    baht = int(amt)
    satang = int((amt - baht) * 100)
    out = ""
    if baht == 0 and satang == 0:
        return "ศูนย์บาทถ้วน"
    if baht > 0:
        out += _read_int(str(baht)) + "บาท"
    if satang > 0:
        if baht == 0:
            out += ""
        out += _read_int(str(satang)) + "สตางค์"
    else:
        out += "ถ้วน"
    return ("ลบ" if neg else "") + out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python baht_text.py <amount>")
        sys.exit(1)
    print(baht_text(sys.argv[1]))
