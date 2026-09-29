import re
import sys
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

INLINE_RE = re.compile(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*|`.+?`)")


def add_inline_runs(paragraph, text):
    """Parse **bold**, *italic*, ***bold italic***, `code` within a line."""
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            paragraph.add_run(text[pos:m.start()])
        token = m.group(0)
        if token.startswith("***") and token.endswith("***"):
            r = paragraph.add_run(token[3:-3])
            r.bold = True
            r.italic = True
        elif token.startswith("**") and token.endswith("**"):
            r = paragraph.add_run(token[2:-2])
            r.bold = True
        elif token.startswith("`") and token.endswith("`"):
            r = paragraph.add_run(token[1:-1])
            r.font.name = "Consolas"
        elif token.startswith("*") and token.endswith("*"):
            r = paragraph.add_run(token[1:-1])
            r.italic = True
        else:
            paragraph.add_run(token)
        pos = m.end()
    if pos < len(text):
        paragraph.add_run(text[pos:])


def is_table_line(line):
    return line.strip().startswith("|")


def parse_table_block(lines, start):
    rows = []
    i = start
    while i < len(lines) and is_table_line(lines[i]):
        row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        rows.append(row)
        i += 1
    # drop the separator row (---|---)
    if len(rows) > 1 and all(re.match(r"^:?-+:?$", c) for c in rows[1]):
        del rows[1]
    return rows, i


def convert(src_path, dst_path, title=None):
    with open(src_path, "r", encoding="utf-8") as f:
        raw = f.read()
    lines = raw.split("\n")

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    i = 0
    first_bold_line_used = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "":
            i += 1
            continue

        # Table block
        if is_table_line(stripped):
            rows, i = parse_table_block(lines, i)
            if rows:
                ncols = len(rows[0])
                table = doc.add_table(rows=0, cols=ncols)
                table.style = "Table Grid"
                for r_idx, row in enumerate(rows):
                    cells = table.add_row().cells
                    for c_idx in range(ncols):
                        text = row[c_idx] if c_idx < len(row) else ""
                        p = cells[c_idx].paragraphs[0]
                        add_inline_runs(p, text)
                        if r_idx == 0:
                            for run in p.runs:
                                run.bold = True
            continue

        # Heading level 2: "## ..."
        if stripped.startswith("## "):
            text = stripped[3:].strip()
            h = doc.add_heading(level=2)
            add_inline_runs(h, text)
            i += 1
            continue

        # Heading level 1: "# ..."
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            h = doc.add_heading(level=1)
            add_inline_runs(h, text)
            i += 1
            continue

        # Bold-only line used as document title (first non-empty line, **Title**)
        if not first_bold_line_used and re.fullmatch(r"\*\*[^*].*[^*]\*\*", stripped):
            text = stripped[2:-2]
            h = doc.add_heading(level=0)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline_runs(h, text)
            first_bold_line_used = True
            i += 1
            continue

        # Italic-only subtitle line right after title, e.g. *Spółdzielnia ...*
        if re.fullmatch(r"\*[^*].*[^*]\*", stripped):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline_runs(p, stripped)
            i += 1
            continue

        # Regular paragraph (may span to blank line, but our source already
        # has one logical line per paragraph in most cases; join wrapped
        # lines that belong to the same paragraph only if no blank line
        # separates them AND the next line doesn't start a new block)
        para_lines = [line]
        j = i + 1
        while j < len(lines) and lines[j].strip() != "" and not is_table_line(lines[j]) \
                and not lines[j].lstrip().startswith("#") \
                and not re.fullmatch(r"\*\*[^*].*[^*]\*\*", lines[j].strip()):
            para_lines.append(lines[j])
            j += 1
        text = " ".join(l.strip() for l in para_lines)
        p = doc.add_paragraph()
        add_inline_runs(p, text)
        i = j

    doc.save(dst_path)
    print(f"OK: {src_path} -> {dst_path}")


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    convert(src, dst)
