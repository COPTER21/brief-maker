#!/usr/bin/env python3
"""
md_to_docx.py — แปลง BRD .md → .docx แบบ professional

For brd-generator-full skill

Features:
  - Thai font (Sarabun)
  - Cover page (CUBE NATIVE branding)
  - Navy/Primary Blue table headers (CUBE NATIVE CI)
  - Page numbers (footer)
  - Header branding
  - Section grouping (1-15 BRD core, 16-18 Philosophy embed)

Usage:
    python md_to_docx.py input.md output.docx [feature_name]

Examples:
    python md_to_docx.py BRD_quotation.md BRD_quotation.docx "สร้างใบเสนอราคา"

Requirements:
    - pandoc (system package)
    - python-docx (pip install python-docx)

Auto-installs python-docx if missing.
"""

import sys
import os
import subprocess
from pathlib import Path


# ============================================================
# Auto-install dependencies
# ============================================================

def ensure_dependencies():
    """ตรวจและติดตั้ง dependencies ถ้าจำเป็น"""
    # Check pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ pandoc not found. Please install:")
        print("   Ubuntu/Debian: sudo apt install pandoc")
        print("   macOS: brew install pandoc")
        sys.exit(1)

    # Check python-docx
    try:
        import docx  # noqa: F401
    except ImportError:
        print("⚠ python-docx not found. Installing...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "python-docx",
             "--quiet", "--break-system-packages"],
            check=False
        )
        try:
            import docx  # noqa: F401
            print("✓ python-docx installed")
        except ImportError:
            print("❌ Failed to install python-docx. Run manually:")
            print("   pip install python-docx --break-system-packages")
            sys.exit(1)


ensure_dependencies()

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement


# ============================================================
# Configuration
# ============================================================

THAI_FONT = "Sarabun"            # หรือ "TH Sarabun New" / "Noto Sans Thai"
ENG_FONT = "Sarabun"
HEADING_COLOR = "1F3864"          # Navy blue สำหรับ heading
PILLAR_COLOR_BG = "DEEBF7"        # ฟ้าอ่อน background
PILLAR_COLOR_TEXT = "1F3864"      # Navy text
TABLE_HEADER_BG = "B02049"        # Crimson 2BSimple
TABLE_HEADER_TEXT = "FFFFFF"
TABLE_BORDER_COLOR = "BFBFBF"
ACCENT_COLOR = "B02049"            # 2BSimple Crimson


# ============================================================
# Step 1: pandoc convert
# ============================================================

def pandoc_convert(md_path: str, docx_path: str):
    """ใช้ pandoc แปลง .md → .docx (basic structure)"""
    cmd = [
        "pandoc",
        md_path,
        "-o", docx_path,
        "--from=markdown+pipe_tables+raw_html",
        "--to=docx",
        "--standalone",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed: {result.stderr}")
    print(f"✓ pandoc convert ok: {docx_path}")


# ============================================================
# Step 2: post-process with python-docx
# ============================================================

def set_cell_background(cell, color_hex: str):
    """กำหนดสีพื้นหลัง cell (CLEAR shading ไม่ใช่ SOLID)"""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def set_cell_borders(cell, color_hex: str = TABLE_BORDER_COLOR, sz: int = 4):
    """กำหนด border ทั้ง 4 ด้าน"""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        b = OxmlElement(f'w:{edge}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), str(sz))
        b.set(qn('w:color'), color_hex)
        tc_borders.append(b)
    tc_pr.append(tc_borders)


def set_run_font(run, font_name: str = THAI_FONT, size: float = None,
                 bold: bool = None, color_hex: str = None):
    """กำหนด font + size + bold + color บน run"""
    run.font.name = font_name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if color_hex is not None:
        run.font.color.rgb = RGBColor.from_string(color_hex)


def apply_default_font(doc):
    """ใส่ Thai font ให้ทุก run + ปรับขนาด"""
    for para in doc.paragraphs:
        for run in para.runs:
            set_run_font(run, THAI_FONT, size=11)
        # heading sizes
        if para.style.name.startswith('Heading 1'):
            for run in para.runs:
                set_run_font(run, THAI_FONT, size=20, bold=True, color_hex=HEADING_COLOR)
        elif para.style.name.startswith('Heading 2'):
            for run in para.runs:
                set_run_font(run, THAI_FONT, size=16, bold=True, color_hex=HEADING_COLOR)
        elif para.style.name.startswith('Heading 3'):
            for run in para.runs:
                set_run_font(run, THAI_FONT, size=13, bold=True, color_hex=ACCENT_COLOR)
        elif para.style.name.startswith('Heading 4'):
            for run in para.runs:
                set_run_font(run, THAI_FONT, size=12, bold=True)

    # tables
    for table in doc.tables:
        for row_idx, row in enumerate(table.rows):
            for cell in row.cells:
                set_cell_borders(cell)
                for para in cell.paragraphs:
                    for run in para.runs:
                        set_run_font(run, THAI_FONT, size=10)
                # header row → crimson bg + white text + bold
                if row_idx == 0:
                    set_cell_background(cell, TABLE_HEADER_BG)
                    for para in cell.paragraphs:
                        for run in para.runs:
                            set_run_font(run, THAI_FONT, size=10, bold=True,
                                         color_hex=TABLE_HEADER_TEXT)


def add_page_numbers(doc):
    """เพิ่ม page number ใน footer"""
    section = doc.sections[0]
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # PAGE field
    run = p.add_run()
    set_run_font(run, THAI_FONT, size=9, color_hex="595959")

    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    run._element.append(fldChar1)
    run._element.append(instrText)
    run._element.append(fldChar2)


def add_header_branding(doc, feature_name: str):
    """เพิ่ม header brand"""
    section = doc.sections[0]
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(f"REQUIREMENT PHILOSOPHY · {feature_name.upper()}")
    set_run_font(run, THAI_FONT, size=8, color_hex="7F7F7F", bold=False)


def add_cover_page(doc, feature_name: str, metadata: dict):
    """เพิ่ม cover page หน้าแรก
    Strategy: build cover_items in display order (top → bottom)
    then reverse-insert before first paragraph
    """
    first_para = doc.paragraphs[0]

    # Build cover content (top → bottom in final document)
    cover_items = []
    cover_items.append(("blank", None))
    cover_items.append(("blank", None))
    cover_items.append(("blank", None))
    cover_items.append(("brand", "2BSimple Co., Ltd."))
    cover_items.append(("blank", None))
    cover_items.append(("doctype", "REQUIREMENT PHILOSOPHY"))
    cover_items.append(("separator", "─────────────────────────"))
    cover_items.append(("blank", None))
    cover_items.append(("feature", feature_name))
    cover_items.append(("blank", None))
    cover_items.append(("blank", None))
    cover_items.append(("blank", None))
    # metadata in given order
    for label, value in metadata.items():
        cover_items.append(("meta", (label, value)))
    cover_items.append(("blank", None))
    cover_items.append(("pagebreak", None))

    # Insert each item.
    # `first_para.insert_paragraph_before(...)` inserts AT the position of first_para
    # and pushes first_para down by 1.
    # If we iterate cover_items in display order [A, B, C], each new item appears
    # immediately above first_para, so ordering becomes A, B, C in document order.
    for kind, val in cover_items:
        new_p = first_para.insert_paragraph_before("")
        new_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if kind == "blank":
            continue
        elif kind == "brand":
            r = new_p.add_run(val)
            set_run_font(r, THAI_FONT, size=11, color_hex=ACCENT_COLOR, bold=True)
        elif kind == "doctype":
            r = new_p.add_run(val)
            set_run_font(r, THAI_FONT, size=28, bold=True, color_hex=HEADING_COLOR)
        elif kind == "separator":
            r = new_p.add_run(val)
            set_run_font(r, THAI_FONT, size=12, color_hex=ACCENT_COLOR)
        elif kind == "feature":
            r = new_p.add_run(val)
            set_run_font(r, THAI_FONT, size=22, bold=True, color_hex="000000")
        elif kind == "meta":
            label, value = val
            r_label = new_p.add_run(f"{label}: ")
            set_run_font(r_label, THAI_FONT, size=11, bold=True, color_hex="595959")
            r_value = new_p.add_run(value)
            set_run_font(r_value, THAI_FONT, size=11, color_hex="000000")
        elif kind == "pagebreak":
            r = new_p.add_run()
            r.add_break(WD_BREAK.PAGE)


def add_pillar_dividers(doc):
    """เพิ่ม visual divider ก่อน Pillar headings (Pillar 1, Pillar 2, ...)"""
    pillar_keywords = ["Pillar 1:", "Pillar 2:", "Pillar 3:", "Pillar 4:", "Pillar 5:"]
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading 1'):
            text = para.text
            if any(k in text for k in pillar_keywords):
                # change formatting to highlight pillar
                for run in para.runs:
                    set_run_font(run, THAI_FONT, size=22, bold=True, color_hex=ACCENT_COLOR)


# ============================================================
# Main
# ============================================================

def convert(md_path: str, docx_path: str, feature_name: str = "Untitled",
            metadata: dict = None):
    if metadata is None:
        metadata = {
            "Module": "—",
            "Owner": "—",
            "Version": "1.0",
            "Date": "—",
        }

    # 1. pandoc convert
    pandoc_convert(md_path, docx_path)

    # 2. post-process
    doc = Document(docx_path)

    # margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # apply default font
    apply_default_font(doc)

    # cover page
    add_cover_page(doc, feature_name, metadata)

    # header + footer
    add_header_branding(doc, feature_name)
    add_page_numbers(doc)

    # pillar dividers (color)
    add_pillar_dividers(doc)

    # save
    doc.save(docx_path)
    print(f"✓ post-process done: {docx_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: md_to_docx.py input.md output.docx [feature_name]")
        sys.exit(1)
    md = sys.argv[1]
    docx = sys.argv[2]
    feat = sys.argv[3] if len(sys.argv) > 3 else "Untitled Feature"
    convert(md, docx, feat)
