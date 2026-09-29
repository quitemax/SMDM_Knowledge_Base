import sys
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn


def iter_block_items(parent):
    """Yield paragraphs and tables in document order."""
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)


def heading_level(paragraph):
    style_name = (paragraph.style.name or "") if paragraph.style else ""
    style_name = style_name.lower()
    if style_name.startswith("heading "):
        try:
            return int(style_name.split(" ")[1])
        except (ValueError, IndexError):
            return 1
    if style_name in ("title",):
        return 1
    return None


def is_list_paragraph(paragraph):
    pPr = paragraph._p.pPr
    if pPr is None:
        return False, None
    numPr = pPr.find(qn('w:numPr'))
    if numPr is None:
        return False, None
    ilvl_el = numPr.find(qn('w:ilvl'))
    ilvl = int(ilvl_el.get(qn('w:val'))) if ilvl_el is not None else 0
    return True, ilvl


def runs_to_md(paragraph):
    parts = []
    for run in paragraph.runs:
        text = run.text
        if not text:
            continue
        if run.bold and run.italic:
            text = f"***{text}***"
        elif run.bold:
            text = f"**{text}**"
        elif run.italic:
            text = f"*{text}*"
        parts.append(text)
    return "".join(parts) if parts else paragraph.text


def table_to_md(table):
    lines = []
    rows = table.rows
    if not rows:
        return ""
    header = [c.text.strip().replace("\n", " ") for c in rows[0].cells]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in rows[1:]:
        cells = [c.text.strip().replace("\n", " ") for c in row.cells]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def convert(path, out_path):
    doc = Document(path)
    md_lines = []
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if not text:
                md_lines.append("")
                continue
            level = heading_level(block)
            is_list, ilvl = is_list_paragraph(block)
            content = runs_to_md(block)
            if level:
                md_lines.append("#" * min(level, 6) + " " + content.strip())
                md_lines.append("")
            elif is_list:
                indent = "  " * (ilvl or 0)
                md_lines.append(f"{indent}- {content.strip()}")
            else:
                md_lines.append(content)
                md_lines.append("")
        else:  # Table
            md_lines.append(table_to_md(block))
            md_lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Converted: {path} -> {out_path} ({len(md_lines)} lines)")


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    convert(src, dst)
