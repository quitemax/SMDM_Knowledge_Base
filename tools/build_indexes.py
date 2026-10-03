# -*- coding: utf-8 -*-
"""Generuje spisy dokumentów z front matter (jedno źródło prawdy).

- zrodla/spis-dokumentow.md      — tabele między znacznikami
                                   <!-- build_indexes:zrodla --> ... <!-- /build_indexes:zrodla -->
- przepisy-prawne/README.md      — tabele aktów między znacznikami
                                   <!-- build_indexes:przepisy:N --> ... <!-- /build_indexes:przepisy:N -->
                                   (N = numer kategorii z pola category, np. "5. Energia, ...")

Wszystko poza znacznikami (wstępy, opisy, uwagi) pozostaje ręczne.
Kategoria (pole category) i kolejność w kategorii (pole order) pochodzą z front matter.

Użycie:
    python tools/build_indexes.py           # zapisuje zmiany
    python tools/build_indexes.py --check   # nic nie zapisuje; kod 1, gdy spisy są nieaktualne
"""
import datetime
import difflib
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Wiersze bez własnego pliku md (np. załącznik skanowany osobno) — wstawiane po wskazanym dokumencie.
ZRODLA_EXTRA_ROWS = {
    "regulamin-stalych-komisji-rady-nadzorczej": (
        "| Regulamin stałych komisji Rady Nadzorczej — Załącznik nr 2 (uzupełnienie brakującej strony) "
        "| [pdf](pdf/regulamin-stalych-komisji-rady-nadzorczej-zalacznik-2.pdf) "
        "| (treść wklejona do [md powyżej](md/regulamin-stalych-komisji-rady-nadzorczej.md#zalacznik-2)) "
        "| Zakres działania Komisji Gospodarki Zasobami Mieszkaniowymi (GZM) — brakująca strona 7 głównego regulaminu. |"
    ),
}
# Zdanie wstępne pod nagłówkiem wybranej kategorii.
ZRODLA_SECTION_INTRO = {
    "Uchwały Rady Nadzorczej": (
        "Osobne uchwały RN (nie regulaminy same w sobie) — katalog "
        "[`pdf/uchwaly-rady-nadzorczej/`](pdf/uchwaly-rady-nadzorczej/) i "
        "[`md/uchwaly-rady-nadzorczej/`](md/uchwaly-rady-nadzorczej/)."
    ),
}


def read_front_matter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        raise SystemExit(f"{path}: brak front matter (uruchom najpierw tools/validate_front_matter.py)")
    end = text.index("\n---", 3)
    data = yaml.safe_load(text[3:end])
    return data


def esc(s):
    return str(s).replace("|", "\\|")


def load(scope_glob):
    docs = []
    for f in sorted(glob.glob(os.path.join(ROOT, scope_glob), recursive=True)):
        d = read_front_matter(f)
        d["_path"] = f
        d["_name"] = os.path.basename(f)[:-3]
        docs.append(d)
    return docs


def zrodla_block(docs):
    base = os.path.join(ROOT, "zrodla")
    cats = {}
    for d in docs:
        cats.setdefault(d.get("category", "Inne"), []).append(d)
    ordered = sorted(cats.items(), key=lambda kv: min(x.get("order", 9999) for x in kv[1]))
    out = []
    for cat, items in ordered:
        out.append(f"## {cat}")
        out.append("")
        if cat in ZRODLA_SECTION_INTRO:
            out.append(ZRODLA_SECTION_INTRO[cat])
            out.append("")
        out.append("| Dokument | PDF | Markdown | Opis |")
        out.append("|---|---|---|---|")
        for d in sorted(items, key=lambda x: (x.get("order", 9999), x["_name"])):
            title = d["title"]
            if d.get("status") == "nieaktualny" and "nieaktualny" not in title:
                title = title[:-1] + ", nieaktualny)" if title.endswith(")") else title + " (nieaktualny)"
            pdf = os.path.normpath(os.path.join(os.path.dirname(d["_path"]), d["pdf"]))
            pdf_rel = os.path.relpath(pdf, base).replace(os.sep, "/")
            md_rel = os.path.relpath(d["_path"], base).replace(os.sep, "/")
            out.append(f"| {esc(title)} | [pdf]({pdf_rel}) | [md]({md_rel}) | {esc(d.get('summary', ''))} |")
            if d["_name"] in ZRODLA_EXTRA_ROWS:
                out.append(ZRODLA_EXTRA_ROWS[d["_name"]])
        out.append("")
    return "\n".join(out).rstrip("\n")


def fmt_date(v):
    if isinstance(v, str):
        v = datetime.date.fromisoformat(v)
    return v.strftime("%d.%m.%Y")


def przepisy_tables(docs):
    by = {}
    for d in docs:
        m = re.match(r"(\d+)\. ", d.get("category", ""))
        if not m:
            raise SystemExit(f"{d['_path']}: brak pola category w formacie \"N. Nazwa\"")
        by.setdefault(m.group(1), []).append(d)
    tables = {}
    for n, items in by.items():
        use_date = n == "1"
        src = "Źródło" if n == "9" else "Źródło (Dz.U.)"
        lines = [f"| Plik | {src} | {'Stan prawny na dzień' if use_date else 'Uwagi'} |", "|---|---|---|"]
        for d in sorted(items, key=lambda x: x.get("order", 9999)):
            pub = re.sub(r"^Dz\.U\. ", "", d["publisher"])
            if use_date:
                third = fmt_date(d["legal_state_date"]) if d.get("legal_state_date") else d.get("summary", "—")
            else:
                third = d.get("summary", "")
            lines.append(f"| `{d['_name']}.pdf` | {esc(pub)} | {esc(third)} |")
        tables[n] = "\n".join(lines)
    return tables


def replace_block(text, start, end, content, path):
    pat = re.compile(re.escape(start) + r"\n.*?\n" + re.escape(end), re.S)
    if not pat.search(text):
        raise SystemExit(f"{path}: brak znaczników {start} ... {end}")
    return pat.sub(lambda m: f"{start}\n{content}\n{end}", text, count=1)


def main():
    check = "--check" in sys.argv
    changed = []

    # --- zrodla ---
    path = os.path.join(ROOT, "zrodla", "spis-dokumentow.md")
    docs = load("zrodla/md/**/*.md")
    old = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in old else "\n"
    new = replace_block(old.replace("\r\n", "\n"), "<!-- build_indexes:zrodla -->",
                        "<!-- /build_indexes:zrodla -->", zrodla_block(docs), path).replace("\n", nl)
    if new != old:
        changed.append(path)
        if not check:
            open(path, "w", encoding="utf-8", newline="").write(new)

    # --- przepisy ---
    path = os.path.join(ROOT, "przepisy-prawne", "README.md")
    docs = load("przepisy-prawne/md/*.md")
    old = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in old else "\n"
    new = old.replace("\r\n", "\n")
    for n, table in przepisy_tables(docs).items():
        new = replace_block(new, f"<!-- build_indexes:przepisy:{n} -->",
                            f"<!-- /build_indexes:przepisy:{n} -->", table, path)
    new = new.replace("\n", nl)
    if new != old:
        changed.append(path)
        if not check:
            open(path, "w", encoding="utf-8", newline="").write(new)

    rel = [os.path.relpath(p, ROOT).replace(os.sep, "/") for p in changed]
    if check:
        if rel:
            print("Nieaktualne spisy (uruchom tools/build_indexes.py): " + ", ".join(rel))
            return 1
        print("Spisy aktualne.")
        return 0
    print("Zaktualizowano: " + (", ".join(rel) if rel else "nic do zmiany"))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
