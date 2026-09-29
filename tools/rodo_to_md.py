# -*- coding: utf-8 -*-
"""Convert the EUR-Lex 'OJ' HTML schema (eli-container/eli-subdivision,
oj-ti-art, oj-normal, 2-col label tables for recitals/litery) into the same
flat Markdown convention used for the ISAP acts in this knowledge base."""
import re
import sys
from bs4 import BeautifulSoup, NavigableString

REPL = {
    "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
    "ó": "o", "ś": "s", "ź": "z", "ż": "z",
}


def slugify(text: str) -> str:
    text = text.lower()
    for a, b in REPL.items():
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


class Converter:
    def __init__(self):
        self.footnotes = []  # (num, text) in document order

    def clean_inline(self, tag):
        clone = BeautifulSoup(str(tag), "html.parser")
        for a in clone.find_all("a"):
            a.replace_with(a.get_text())
        for b in clone.find_all(["b", "strong"]):
            b.replace_with(f"**{b.get_text()}**")
        for i in clone.find_all("i"):
            i.replace_with(f"*{i.get_text()}*")
        return norm_space(clone.get_text(" ", strip=True))

    def table_rows(self, table):
        """Flatten a 2-col label/text table into (label, text) pairs. Handles
        the case where a content cell itself contains nested 2-col tables
        (e.g. a numbered point whose text ends in a lettered sub-list) by
        emitting the cell's own paragraph text first, then recursing into
        any nested tables as additional, separate rows."""
        tbody = table.find("tbody", recursive=False) or table
        rows = []
        for tr in tbody.find_all("tr", recursive=False):
            cells = tr.find_all("td", recursive=False)
            if len(cells) < 2:
                continue
            label = norm_space(cells[0].get_text(" ", strip=True))
            content_cell = cells[1]
            texts = [
                self.clean_inline(p)
                for p in content_cell.find_all("p", recursive=False)
            ]
            own_text = " ".join(t for t in texts if t)
            if label or own_text:
                rows.append((label, own_text))
            for nested in content_cell.find_all("table", recursive=False):
                rows.extend(self.table_rows(nested))
        return rows

    def process_block(self, node, out):
        """Process a generic container's direct children: p.oj-normal lines,
        2-col label tables, or nested divs (recurse)."""
        for child in node.find_all(recursive=False):
            if child.name == "p" and "oj-normal" in (child.get("class") or []):
                text = self.clean_inline(child)
                if text:
                    out.append(text)
            elif child.name == "table":
                for label, text in self.table_rows(child):
                    out.append(f"{label} {text}".strip())
            elif child.name == "div":
                self.process_block(child, out)

    def process_article(self, div, out):
        title_p = div.find("p", class_="oj-ti-art", recursive=False)
        label = norm_space(title_p.get_text(" ", strip=True)) if title_p else ""
        title_div = div.find("div", class_="eli-title", recursive=False)
        name_p = title_div.find("p", class_="oj-sti-art") if title_div else None
        name = norm_space(name_p.get_text(" ", strip=True)) if name_p else ""
        aid = slugify(label)
        heading = f"{label}. {name}" if name else label
        out.append(f'\n\n<a id="{aid}"></a>\n### {heading}\n')
        body = []
        for child in div.find_all(recursive=False):
            if child is title_p or child is title_div:
                continue
            if child.name == "p" and "oj-normal" in (child.get("class") or []):
                text = self.clean_inline(child)
                if text:
                    body.append(text)
            elif child.name == "table":
                for label2, text2 in self.table_rows(child):
                    body.append(f"{label2} {text2}".strip())
            elif child.name == "div":
                self.process_block(child, body)
        out.append("\n\n".join(body))

    def process_section_like(self, div, level, out):
        p1 = div.find(["p"], class_="oj-ti-section-1", recursive=False)
        label = norm_space(p1.get_text(" ", strip=True)) if p1 else ""
        title_div = div.find("div", class_="eli-title", recursive=False)
        name_p = title_div.find("p", class_="oj-ti-section-2") if title_div else None
        name = norm_space(name_p.get_text(" ", strip=True)) if name_p else ""
        aid = slugify(label)
        heading = f"{label}. {name}" if name else label
        out.append(f'\n\n<a id="{aid}"></a>\n{"#" * level} {heading}\n')
        for child in div.find_all("div", recursive=False):
            if child is title_div:
                continue
            classes = child.get("class") or []
            cid = child.get("id", "")
            if "eli-subdivision" in classes and cid.startswith("art_"):
                self.process_article(child, out)
            elif re.search(r"\.sct_\d+$", cid) or cid.startswith("sct_"):
                self.process_section_like(child, level + 1, out)

    def process_preamble(self, pbl, out):
        motywy_started = False
        for child in pbl.find_all(recursive=False):
            cid = child.get("id", "")
            if child.name == "p" and "oj-normal" in (child.get("class") or []):
                text = self.clean_inline(child)
                if text:
                    out.append(text)
            elif child.name == "div" and cid.startswith("cit_"):
                p = child.find("p", class_="oj-normal")
                if p:
                    text = self.clean_inline(p)
                    if text:
                        out.append(text)
            elif child.name == "div" and cid.startswith("rct_"):
                if not motywy_started:
                    out.append('\n\n<a id="motywy"></a>\n### Motywy\n')
                    motywy_started = True
                table = child.find("table")
                if table:
                    for label, text in self.table_rows(table):
                        out.append(f"{label} {text}".strip())

    def process_final(self, fnp, out):
        final_div = fnp.find("div", class_="oj-final")
        if not final_div:
            return
        out.append('\n\n<a id="klauzula-koncowa"></a>\n### Klauzula końcowa\n')
        for child in final_div.find_all(recursive=False):
            if child.name == "p" and "oj-normal" in (child.get("class") or []):
                text = self.clean_inline(child)
                if text:
                    out.append(text)
            elif child.name == "div" and "oj-signatory" in (child.get("class") or []):
                lines = [
                    self.clean_inline(p)
                    for p in child.find_all("p", class_="oj-signatory")
                ]
                out.append(" / ".join(x for x in lines if x))

    def collect_footnotes(self, soup):
        notes = soup.find_all("p", class_="oj-note")
        for p in notes:
            anchor = p.find("a", id=re.compile(r"^ntr\d+"))
            if not anchor:
                continue
            num_m = re.match(r"ntr(\d+)", anchor.get("id", ""))
            num = num_m.group(1) if num_m else "?"
            clone = BeautifulSoup(str(p), "html.parser")
            a2 = clone.find("a", id=re.compile(r"^ntr\d+"))
            if a2:
                a2.decompose()
            text = self.clean_inline(clone)
            self.footnotes.append((num, text))

    def convert(self, html_path, title_override=None):
        with open(html_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        main_title = soup.find("div", class_="eli-main-title")
        title_lines = [
            self.clean_inline(p) for p in main_title.find_all("p", class_="oj-doc-ti")
        ] if main_title else []

        out = []
        if title_lines:
            h1 = " ".join(title_lines[:2]) if len(title_lines) > 1 else title_lines[0]
            out.append(f"# {h1}\n")
            if len(title_lines) > 2:
                out.append("\n\n".join(title_lines[2:]))

        pbl = soup.find("div", class_="eli-subdivision", id=re.compile(r"^pbl_"))
        if pbl:
            out.append('\n\n<a id="preambula"></a>\n## Preambuła\n')
            self.process_preamble(pbl, out)

        enc = soup.find("div", class_="eli-subdivision", id=re.compile(r"^enc_"))
        if enc:
            for chapter in enc.find_all("div", recursive=False):
                cid = chapter.get("id", "")
                if cid.startswith("cpt_"):
                    self.process_section_like(chapter, 3, out)

        fnp = soup.find("div", class_="eli-subdivision", id=re.compile(r"^fnp_"))
        if fnp:
            self.process_final(fnp, out)

        self.collect_footnotes(soup)

        body_text = "\n\n".join(x for x in out if x)
        body_text = re.sub(r"\n{3,}", "\n\n", body_text)

        if self.footnotes:
            fn_lines = ["\n\n## Przypisy\n"]
            for num, text in self.footnotes:
                fn_lines.append(f"\n({num}) {text}")
            body_text += "\n" + "\n".join(fn_lines)

        return body_text.strip() + "\n"


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    override = sys.argv[3] if len(sys.argv) > 3 else None
    conv = Converter()
    md = conv.convert(src, title_override=override)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"OK: {src} -> {dst} ({len(md)} chars, {len(conv.footnotes)} footnotes)")
