# -*- coding: utf-8 -*-
"""Waliduje front matter (metadane) i względne odnośniki w plikach md.

Sprawdzane katalogi: manual/, zrodla/md/ (z podkatalogami), przepisy-prawne/md/.
Specyfikacja formatu: docs/kontrakt-importu.md.

Kod wyjścia: 0 = brak błędów, 1 = są błędy (lista z numerami linii).
Ostrzeżenia nie zmieniają kodu wyjścia; ich listę wypisuje opcja -v.

Użycie (z dowolnego katalogu):
    python tools/validate_front_matter.py [-v]
"""
import datetime
import os
import re
import sys
from urllib.parse import unquote

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCOPES = {
    "manual": {"kinds": {"manual"}, "needs_pdf": False},
    "zrodla/md": {"kinds": {"statut", "regulamin", "uchwala"}, "needs_pdf": True},
    "przepisy-prawne/md": {"kinds": {"akt-prawny"}, "needs_pdf": True},
}
STATUSES = {"obowiazujacy", "nieaktualny", "uchylony", "projekt"}
AUDIENCES = {"public", "resident", "member", "membership", "technical", "finance",
             "hr", "management", "supervisory", "admin"}
KNOWN_KEYS = {"title", "kind", "status", "audience", "summary", "pdf", "superseded_by",
              "publisher", "legal_state_date", "source_url", "effective_from", "resolution",
              "section", "order", "incomplete",
              # pola pomocnicze używane przez tools/build_indexes.py
              "category"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ID_RE = re.compile(r'<a\s+(?:id|name)="([^"]+)"')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")

errors = []
warnings = []


def err(path, line, msg):
    errors.append((path, line, msg))


def warn(path, line, msg):
    warnings.append((path, line, msg))


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def split_front_matter(text):
    """Zwraca (dict|None, błąd|None, liczba linii front matter, treść)."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != "---":
        return None, "brak front matter (plik musi zaczynać się od ---)", 0, text
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r") == "---":
            raw = "\n".join(lines[1:i])
            try:
                data = yaml.safe_load(raw)
            except yaml.YAMLError as e:
                return None, f"niepoprawny YAML: {str(e).splitlines()[0]}", i + 1, ""
            if not isinstance(data, dict):
                return None, "front matter nie jest słownikiem", i + 1, ""
            return data, None, i + 1, "\n".join(lines[i + 1:])
    return None, "front matter nie jest zamknięty (brak końcowego ---)", 0, text


def github_slug(heading):
    s = re.sub(r"<[^>]+>", "", heading).strip().lower()
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    return s.replace(" ", "-")


_anchor_cache = {}


def anchors_of(path):
    if path in _anchor_cache:
        return _anchor_cache[path]
    found = set()
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        text = ""
    in_code = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        found.update(ID_RE.findall(line))
        m = HEADING_RE.match(line)
        if m:
            found.add(github_slug(m.group(2)))
    _anchor_cache[path] = found
    return found


def check_date(path, key, value):
    if isinstance(value, datetime.date):
        return
    if isinstance(value, str) and DATE_RE.match(value):
        try:
            datetime.date.fromisoformat(value)
            return
        except ValueError:
            pass
    err(path, 1, f"pole {key}: oczekiwano daty RRRR-MM-DD, jest {value!r}")


def check_meta(path, scope, data, all_names):
    cfg = SCOPES[scope]
    for key in ("title", "kind", "status", "audience"):
        if data.get(key) in (None, "", []):
            err(path, 1, f"brak wymaganego pola: {key}")
    for key in data:
        if key not in KNOWN_KEYS:
            warn(path, 1, f"nieznane pole: {key}")
    title = data.get("title")
    if title is not None and not isinstance(title, str):
        err(path, 1, "pole title musi być tekstem")
    kind = data.get("kind")
    if kind is not None and kind not in cfg["kinds"]:
        err(path, 1, f"kind={kind!r} niedozwolone w {scope}/ (dozwolone: {', '.join(sorted(cfg['kinds']))})")
    status = data.get("status")
    if status is not None and status not in STATUSES:
        err(path, 1, f"status={status!r} niedozwolony (dozwolone: {', '.join(sorted(STATUSES))})")
    aud = data.get("audience")
    if aud is not None:
        if not isinstance(aud, list) or not all(isinstance(a, str) for a in aud):
            err(path, 1, "audience musi być listą, np. [public]")
        else:
            bad = [a for a in aud if a not in AUDIENCES]
            if bad:
                err(path, 1, f"audience: niedozwolone wartości {bad}")
            if "public" in aud and len(aud) > 1:
                err(path, 1, "audience: public nie łączy się z innymi wartościami")
            if len(set(aud)) != len(aud):
                err(path, 1, "audience: powtórzone wartości")
    if "summary" in data and not isinstance(data["summary"], str):
        err(path, 1, "pole summary musi być tekstem")
    elif not data.get("summary"):
        warn(path, 1, "brak pola summary (zalecane)")

    # pdf
    pdf = data.get("pdf")
    if cfg["needs_pdf"] and not pdf:
        err(path, 1, "brak wymaganego pola: pdf")
    if pdf:
        target = os.path.normpath(os.path.join(os.path.dirname(path), str(pdf)))
        if not os.path.isfile(target):
            err(path, 1, f"pdf: plik nie istnieje: {pdf}")
        elif not target.lower().endswith(".pdf"):
            err(path, 1, f"pdf: to nie jest plik .pdf: {pdf}")

    # superseded_by
    sup = data.get("superseded_by")
    if status == "nieaktualny" and not sup:
        err(path, 1, "status nieaktualny wymaga pola superseded_by")
    if sup:
        if str(sup).endswith(".md"):
            err(path, 1, "superseded_by: podaj nazwę bez rozszerzenia .md")
        elif str(sup) not in all_names:
            err(path, 1, f"superseded_by: nie ma dokumentu o nazwie {sup!r}")

    # daty i pola dodatkowe
    for key in ("effective_from", "legal_state_date"):
        if data.get(key) is not None:
            check_date(path, key, data[key])
    if data.get("resolution") is not None and not isinstance(data["resolution"], str):
        err(path, 1, "resolution musi być tekstem (np. \"338/2024\")")
    if kind == "akt-prawny":
        if not data.get("publisher"):
            err(path, 1, "akt-prawny wymaga pola publisher")
        if data.get("legal_state_date") is None and status == "obowiazujacy":
            warn(path, 1, "akt-prawny bez legal_state_date")
    if scope == "manual":
        section = data.get("section")
        want = os.path.relpath(path, os.path.join(ROOT, "manual")).replace(os.sep, "/").split("/")[0]
        if section is not None and section != want and "/" in os.path.relpath(path, os.path.join(ROOT, "manual")).replace(os.sep, "/"):
            err(path, 1, f"section={section!r} nie zgadza się z katalogiem {want!r}")
        if "incomplete" in data and not isinstance(data["incomplete"], bool):
            err(path, 1, "incomplete musi być true/false")
        if "order" in data and not isinstance(data["order"], int):
            err(path, 1, "order musi być liczbą całkowitą")
    if "incomplete" in data and data["incomplete"] is True and scope != "manual":
        warn(path, 1, "incomplete ma sens tylko w manual/")


def check_body(path, body, offset):
    """Nagłówek # oraz odnośniki względne."""
    lines = body.split("\n")
    in_code = False
    h1 = []
    for i, line in enumerate(lines):
        n = offset + i + 1
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^# \S", line):
            h1.append(n)
        for m in LINK_RE.finditer(line):
            check_link(path, n, m.group(1))
    if not h1:
        err(path, offset + 1, "brak nagłówka # (tytuł dokumentu)")
    else:
        first_content = next((offset + i + 1 for i, l in enumerate(lines) if l.strip()), None)
        if h1[0] != first_content:
            # dopuszczamy wyłącznie puste linie przed nagłówkiem
            err(path, first_content or offset + 1, "plik (po front matter) musi zaczynać się od nagłówka #")
        if len(h1) > 1:
            err(path, h1[1], f"więcej niż jeden nagłówek # (pierwszy w linii {h1[0]})")


def check_link(path, line, target):
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):  # http:, https:, mailto:
        return
    base, _, frag = target.partition("#")
    if base:
        dest = os.path.normpath(os.path.join(os.path.dirname(path), unquote(base)))
        if not os.path.exists(dest):
            err(path, line, f"martwy odnośnik: {target}")
            return
    else:
        dest = path
    if frag:
        if os.path.isdir(dest) or not dest.endswith(".md"):
            return
        if unquote(frag) not in anchors_of(dest):
            err(path, line, f"brak kotwicy #{frag} w {rel(dest)}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    files = []
    for scope in SCOPES:
        base = os.path.join(ROOT, *scope.split("/"))
        for dirpath, _, names in os.walk(base):
            for n in sorted(names):
                if n.endswith(".md"):
                    files.append((scope, os.path.join(dirpath, n)))
    files.sort(key=lambda x: x[1])

    # unikalność nazw (adres dokumentu) w zrodla/md i przepisy-prawne/md
    seen = {}
    names_by_scope = {s: set() for s in SCOPES}
    for scope, path in files:
        name = os.path.basename(path)[:-3]
        names_by_scope[scope].add(name)
        if scope in ("zrodla/md", "przepisy-prawne/md"):
            if name in seen:
                err(path, 1, f"nazwa pliku nie jest unikalna (jest też {rel(seen[name])})")
            seen[name] = path
    all_doc_names = names_by_scope["zrodla/md"] | names_by_scope["przepisy-prawne/md"]

    for scope, path in files:
        text = open(path, encoding="utf-8").read()
        data, problem, fm_lines, body = split_front_matter(text)
        if problem:
            err(path, 1, problem)
            continue
        check_meta(path, scope, data, all_doc_names)
        check_body(path, body, fm_lines)

    if "-v" in sys.argv or "--verbose" in sys.argv:
        for p, l, m in sorted(warnings):
            print(f"OSTRZEŻENIE {rel(p)}:{l}: {m}")
    for p, l, m in sorted(errors):
        print(f"BŁĄD {rel(p)}:{l}: {m}")
    print(f"Sprawdzono {len(files)} plików md: {len(errors)} błędów, {len(warnings)} ostrzeżeń.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
