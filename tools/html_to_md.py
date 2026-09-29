# -*- coding: utf-8 -*-
"""Convert ISAP/api.sejm.gov.pl 'text.html' legal-act pages into the Markdown
convention used in this knowledge base (anchors + flat 1./1)/a) prefixes,
no nested markdown lists, footnotes collected at the bottom)."""
import re
import sys
from bs4 import BeautifulSoup

HEADING_LEVEL = {"unit_dzial": 2, "unit_bran": 2, "unit_chpt": 3, "unit_oddz": 4}
ANCHOR_PREFIX = {
    "unit_dzial": "dzial",
    "unit_bran": "dzial",
    "unit_chpt": "rozdzial",
    "unit_oddz": "oddzial",
    "unit_arti": "art",
    "unit_para": "par",
}
ARTICLE_LIKE = {"unit_arti", "unit_para"}
LIST_LIKE = {"unit_pass", "unit_pint", "unit_lett", "unit_tir", "unit_ppkt", "unit_none"}


def slugify(text: str) -> str:
    text = text.lower()
    repl = {
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ź": "z", "ż": "z",
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "sekcja"


def norm_space(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    return text.strip()


def anchor_id(div, fallback_counter):
    data_id = div.get("data-id")
    utype = next((c for c in div.get("class", []) if c.startswith("unit_")), None)
    prefix = ANCHOR_PREFIX.get(utype)
    if data_id and prefix:
        num = data_id.split("_", 1)[-1]
        return f"{prefix}-{num}"
    fallback_counter[0] += 1
    return f"sec-{fallback_counter[0]}"


class Converter:
    def __init__(self):
        self.footnotes = []  # list of (marker, text)
        self.fallback_counter = [0]
        self.tables_rendered = 0

    def strip_footnotes(self, tag):
        for gloss in tag.find_all("a", class_=re.compile("gloss-link")):
            marker_tag = gloss.find("sup")
            marker = marker_tag.get_text(strip=True) if marker_tag else "*"
            tooltip = gloss.find(class_="tooltip-text")
            note = norm_space(tooltip.get_text(" ", strip=True)) if tooltip else ""
            if note:
                self.footnotes.append((marker, note))
                gloss.replace_with(f"[{marker}]")
            else:
                gloss.replace_with("")
        return tag

    def clean_inline(self, tag):
        tag = BeautifulSoup(str(tag), "html.parser")
        self.strip_footnotes(tag)
        for a in tag.find_all("a"):
            a.replace_with(a.get_text())
        for b in tag.find_all(["b", "strong"]):
            b.replace_with(f"**{b.get_text()}**")
        text = tag.get_text(" ", strip=True)
        return norm_space(text)

    def table_to_md(self, table):
        rows = []
        for tr in table.find_all("tr"):
            cells = [norm_space(td.get_text(" ", strip=True)) for td in tr.find_all(["td", "th"])]
            if any(c for c in cells):
                rows.append(cells)
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        keep = [i for i in range(width) if any(r[i] for r in rows)]
        if not keep:
            return ""
        rows = [[r[i] for i in keep] for r in rows]
        width = len(keep)
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
        for r in rows[1:]:
            lines.append("| " + " | ".join(r) + " |")
        self.tables_rendered += 1
        return "\n".join(lines)

    def get_label(self, h3):
        if not h3:
            return ""
        h3_copy = BeautifulSoup(str(h3), "html.parser")
        for span in h3_copy.find_all(class_="pro-title-unit"):
            span.decompose()
        self.strip_footnotes(h3_copy)
        return norm_space(h3_copy.get_text(" ", strip=True))

    def get_title(self, h3):
        if not h3:
            return ""
        span = h3.find(class_="pro-title-unit")
        return norm_space(span.get_text(" ", strip=True)) if span else ""

    def render_cite_box(self, cite_box):
        """A 'cite-box' wraps a provision quoted inline after '...w brzmieniu:'
        when a list item (unit_pint/unit_lett/etc.) inserts or replaces text —
        opening quote mark, the quoted unit itself (which can be a whole
        multi-ustęp article, not just a single line), closing quote mark,
        trailing punctuation. The quoted unit renders through the normal
        process_children path (so a multi-ustęp quoted article still gets one
        markdown paragraph per ustęp, consistent with how this corpus renders
        ustępy everywhere else); only the quote marks and trailing punctuation
        are glued directly onto its first/last line."""
        opn = cite_box.find("div", class_="qmark-opn")
        body = cite_box.find("div", class_="cite-body")
        cls = cite_box.find("div", class_="qmark-cls")
        trailer = cite_box.find("div", class_="trailer")
        opn_text = opn.get_text(strip=True) if opn else ""
        cls_text = cls.get_text(strip=True) if cls else ""
        trailer_text = trailer.get_text(strip=True) if trailer else ""
        inner_out = []
        if body:
            self.process_children(body, inner_out)
        rendered = "\n".join(inner_out).strip()
        if not rendered:
            return ""
        # A whole quoted article/paragraph (not just a bare list item) renders
        # as its own anchor + heading line — glue the opening quote onto the
        # heading text itself, not onto the anchor tag that precedes it, or
        # it ends up as a dangling quote mark on its own line above the
        # heading instead of visibly opening the quoted unit's own number.
        heading_m = re.match(r'^(<a id="[^"]+"></a>\n#{2,4} )(.*)$', rendered, re.MULTILINE)
        if heading_m:
            rendered = rendered[: heading_m.end(1)] + opn_text + heading_m.group(2) + rendered[heading_m.end():]
            return f"{rendered}{cls_text}{trailer_text}"
        return f"{opn_text}{rendered}{cls_text}{trailer_text}"

    def process_children(self, container, out):
        for child in container.find_all(recursive=False):
            if child.name == "table":
                md = self.table_to_md(child)
                if md:
                    out.append("\n" + md + "\n")
            elif child.name == "div" and child.get("data-template") == "xText":
                text = self.clean_inline(child)
                if text:
                    out.append("\n" + text)
            elif child.name == "div" and "cite-box" in (child.get("class") or []):
                text = self.render_cite_box(child)
                if text:
                    out.append("\n" + text)
            elif child.name == "div" and any(
                c.startswith("unit_") for c in (child.get("class") or [])
            ):
                self.process_unit(child, out)
            elif child.name == "div":
                # unwrap generic wrapper divs (e.g. class="block")
                self.process_children(child, out)

    def _emit_list_children(self, children, out, label, state):
        """Shared by the LIST_LIKE branch of process_unit: emit a flat run of
        a list item's own children (xText / table / cite-box / a nested
        unit), gluing the item's own label onto the first piece of content
        and prefixing every later piece with its own paragraph break — same
        rule for a piece reached by unwrapping a generic wrapper div (this
        is what a plain 'unit_pint' loop used to skip entirely, silently
        dropping the whole quoted provision inside a 'cite-box' when it
        wasn't a direct child)."""
        for child in children:
            if child.name == "div" and child.get("data-template") == "xText":
                t = self.clean_inline(child)
                if not t:
                    continue
                if not state[0]:
                    out.append(f"\n{label} {t}" if label else f"\n{t}")
                    state[0] = True
                else:
                    out.append(f"\n{t}")
            elif child.name == "table":
                md = self.table_to_md(child)
                if md:
                    out.append("\n" + md + "\n")
            elif child.name == "div" and "cite-box" in (child.get("class") or []):
                t = self.render_cite_box(child)
                if not t:
                    continue
                if not state[0]:
                    out.append(f"\n{label} {t}" if label else f"\n{t}")
                    state[0] = True
                else:
                    out.append(f"\n{t}")
            elif child.name == "div" and any(
                c.startswith("unit_") for c in (child.get("class") or [])
            ):
                if not state[0] and label:
                    out.append(f"\n{label}")
                    state[0] = True
                self.process_unit(child, out)
            elif child.name == "div":
                # unwrap a generic wrapper div (e.g. one other than cite-box)
                self._emit_list_children(child.find_all(recursive=False), out, label, state)

    def process_unit(self, div, out):
        classes = div.get("class", [])
        utype = next((c for c in classes if c.startswith("unit_")), None)
        h3 = div.find("h3", recursive=False)
        inner = div.find("div", class_="unit-inner", recursive=False)
        label = self.get_label(h3)
        title = self.get_title(h3)
        aid = anchor_id(div, self.fallback_counter)

        if utype in HEADING_LEVEL:
            level = HEADING_LEVEL[utype]
            heading = f"{label}. {title}" if title else label
            out.append(f'\n\n<a id="{aid}"></a>\n{"#" * level} {heading}\n')
            if inner:
                self.process_children(inner, out)
        elif utype in ARTICLE_LIKE:
            out.append(f'\n\n<a id="{aid}"></a>\n### {label}\n')
            if inner:
                self.process_children(inner, out)
        elif utype in LIST_LIKE:
            children = inner.find_all(recursive=False) if inner else []
            state = [False]  # first_emitted, boxed so the recursive helper can update it
            self._emit_list_children(children, out, label, state)
            if not state[0] and label:
                out.append(f"\n{label}")
        else:
            if inner:
                self.process_children(inner, out)
            else:
                self.process_children(div, out)

    def convert(self, html_path, title_override=None):
        with open(html_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        source_table_count = len(soup.find_all("table"))

        h1 = soup.find("h1")
        head_type = h1.find(class_="head-type") if h1 else None
        head_date = h1.find(class_="head-date") if h1 else None
        head_title = h1.find(class_="head-title") if h1 else None
        is_obwieszczenie = bool(
            head_type and "obwieszczenie" in head_type.get_text().lower()
        )
        if title_override and is_obwieszczenie:
            title_line = title_override
            title_full = ""
        else:
            title_line = " ".join(
                norm_space(x.get_text(" ", strip=True))
                for x in (head_type, head_date)
                if x
            )
            title_full = self.clean_inline(head_title) if head_title else ""

        out = []
        out.append(f"# {title_line}\n\n{title_full}\n" if title_full else f"# {title_line}\n")

        parts = soup.find("div", class_="parts")
        if parts:
            for section in parts.find_all("section", recursive=False):
                part_div = section.find("div", class_="part")
                part_title = ""
                if part_div:
                    h2 = part_div.find("h2", class_="part")
                    if h2:
                        part_title = norm_space(h2.get_text(" ", strip=True))
                lowered = part_title.lower()
                if lowered.startswith("treść obwieszczenia") or lowered.startswith(
                    "tresc obwieszczenia"
                ):
                    continue  # pure procedural wrapper, no informational value
                is_main_body = bool(
                    re.match(r"^za[lł]ącznik\s*-\s*tekst jednolit", part_title, re.IGNORECASE)
                ) or not part_title
                container = part_div if part_div else section
                if not is_main_body and part_title:
                    out.append(
                        f'\n\n<a id="{slugify(part_title)}"></a>\n## {part_title}\n'
                    )
                self.process_children(container, out)
        else:
            body = soup.find("body")
            if body:
                self.process_children(body, out)

        body_text = "\n".join(out)
        body_text = re.sub(r"\n{3,}", "\n\n", body_text)

        if source_table_count > self.tables_rendered:
            missing = source_table_count - self.tables_rendered
            warning = (
                f"\n\n> **Uwaga:** źródłowy HTML zawiera {source_table_count} tabel, "
                f"z których {missing} nie zostało odwzorowanych w tej wersji "
                "(prawdopodobnie zagnieżdżone tabele lub tabele oznaczone w źródle jako "
                "„patrz oryginał”) — sprawdź odpowiadający plik PDF.\n"
            )
            body_text += warning

        if self.footnotes:
            seen = set()
            fn_lines = ["\n\n## Przypisy\n"]
            for marker, note in self.footnotes:
                key = (marker, note)
                if key in seen:
                    continue
                seen.add(key)
                fn_lines.append(f"\n{marker} {note}")
            body_text += "\n" + "\n".join(fn_lines)

        return body_text.strip() + "\n"


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    override = sys.argv[3] if len(sys.argv) > 3 else None
    conv = Converter()
    md = conv.convert(src, title_override=override)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"OK: {src} -> {dst} ({len(md)} chars, {len(conv.footnotes)} footnote refs)")
