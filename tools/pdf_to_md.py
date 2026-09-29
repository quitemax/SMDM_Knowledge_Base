# -*- coding: utf-8 -*-
"""Convert ISAP-style Sejm PDF exports (no HTML available) into the same
flat Markdown convention used elsewhere in this knowledge base.

Strategy: PyMuPDF's own line/paragraph segmentation is unreliable on these
PDFs (fully-justified old documents emit one 'line' per word in some
producers), so we re-cluster words into visual lines by y0, strip the
repeating ISAP header/footer, then reflow lines into paragraphs using
structural markers (Rozdzial/Dzial/Art./section-para) and blank-line gaps.
"""
import re
import sys

import fitz

# Some old (~2000-2005) Sejm/Dziennik-Ustaw PDFs embed a custom-subset font
# whose ToUnicode CMap is broken: certain Polish diacritic glyphs decode to
# unrelated symbol/Latin characters that never legitimately occur in Polish
# legal text, so this substitution is safe to apply unconditionally.
MOJIBAKE_FIX = str.maketrans({
    "∏": "ł", "Ê": "ś", "ƒ": "ń", "à": "ą",
    "ç": "ć", "ê": "ź", "˝": "ż", "Ñ": "Ą",
    "¸": "Ł", "Â": "Ś", "˚": "Ż", "´": "ę",
})


def fix_mojibake(text: str) -> str:
    return text.translate(MOJIBAKE_FIX).replace("﻿", "")


HEADER_RE = re.compile(
    r"^\W{0,2}Kancelaria Sejmu\b.*$"
    r"|^Dziennik Ustaw Nr \d+ . \d+ . Poz\. \d+( i \d+)?$"
    r"|^Dziennik Ustaw . \d+ . Poz\. \d+( i \d+)?$"
    r"|^Dziennik Urz[eę]dowy\b.*$"
)
FOOTER_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# A unit number can carry a letter suffix ("24a") or a "prim" suffix marking
# a provision inserted after an already-lettered one (ust./art. 24¹) — some
# acts write this out as a literal bracket in the source text ("24[1]"),
# but others set a true (smaller-font) superscript digit, which PyMuPDF's
# own word-grouping glues straight onto the preceding word with no
# separator at all ("9h" + superscript "1" -> word text "9h1"). A letter
# suffix is never itself followed by a bare digit in genuine Polish legal
# numbering, so a trailing digit after one always means this glued
# superscript, and can be matched unconditionally, no font-size check
# needed. The digit is re-bracketed at render time (see bracket_prim) for
# a single consistent on-page convention regardless of which way the
# source wrote it.
#
# The bracket alternative is tried FIRST, not second: `(?:[a-z]+\d*)*` can
# match zero repetitions (empty), which trivially "succeeds" without ever
# looking at a following "[N]" — fine when whatever follows NUM in the
# caller's own pattern is a REQUIRED literal that then fails and forces
# backtracking into the other alternative (this is what saves the Art./§
# heading match, which requires a literal "." right after NUM), but
# heading_and_title()'s own pattern has only an OPTIONAL "\.?" there, so
# nothing forces that backtrack — NUM silently stops at the bare number and
# "[1]" leaks into the heading's title text instead (seen on
# ustawa-o-spoldzielniach-mieszkaniowych's inserted "Rozdział 1[1]"
# chapters, rendered as "Rozdział 1. [1] Prawa członków..." instead of
# "Rozdział 1[1]. Prawa członków..."). Trying the bracket first removes the
# dependency on that lucky backtrack.
# The bracketed prim suffix can itself carry a trailing letter ("Art.
# 18[3a]", Kodeks pracy's own literal source notation for "art. 18(3a)" —
# the third article inserted after art. 18, further split into lettered
# sub-articles a, b, c...) alongside the plain-digit form ("art. 24[1]")
# already seen elsewhere — without the optional [a-z]* here, the required
# literal "." right after NUM in "^Art\.\s*{NUM}\." never matches (there's
# still an unconsumed "a]" before it), so the whole Art. heading fails to
# be recognized as a paragraph boundary at all, and the WHOLE following
# article's text gets merged into whatever preceded it.
NUM = r"\d+(?:\[\d+[a-z]*\]|(?:[a-z]+\d*)*)?"
# Rozdział/Oddział are numbered with arabic digits in most acts but with
# Roman numerals throughout in others (e.g. Kodeks cywilny) — accept both.
# A Roman-numbered chapter can also carry a lettered suffix for an inserted
# chapter, same idea as arabic "24a" ("Rozdział IIa", "Rozdział IIb" — and
# even upper-case "Rozdział IIC" in Kodeks pracy, apparently a small-caps
# rendering quirk rather than a deliberate case distinction) — without the
# letter allowed here, paragraph-splitting doesn't recognize these as a
# heading boundary at all, so the WHOLE following chapter's text gets
# merged into one blob and then swallowed as this heading's own title.
UNIT_NUM = rf"(?:{NUM}|[IVXLC]+[a-zA-Z]*)"

ORDINAL_WORD = (
    r"pierwsz\w*|drug\w*|trzeci\w*|czwart\w*|pi[aą]t\w*|sz[oó]st\w*|"
    r"si[oó]dm\w*|[oó]sm\w*|dziewi[aą]t\w*|dziesi[aą]t\w*|"
    # 11th-15th, needed for Kodeks pracy's word-ordinal Działy
    # ("DZIAŁ JEDENASTY" ... "DZIAŁ PIĘTNASTY"), including the
    # prim-suffixed "DZIAŁ CZTERNASTYA".
    r"jedenast\w*|dwunast\w*|trzynast\w*|czternast\w*|pi[eę]tnast\w*"
)

MARKER_RES = [
    re.compile(rf"^Ksi[eę]ga\s+(?:{ORDINAL_WORD})\b", re.IGNORECASE),
    re.compile(r"^Cz[eę][śs][ćc]\s+[IVXLC]+", re.IGNORECASE),
    re.compile(r"^Tytu[łl]\s+[IVXLC]+", re.IGNORECASE),
    # Dział is usually numbered with Roman numerals, but Kodeks pracy spells
    # it out as an ordinal word instead ("DZIAŁ PIERWSZY", "DZIAŁ DRUGI") —
    # same ORDINAL_WORD alternation already used for Księga.
    re.compile(rf"^Dzia[łl]\s+(?:[IVXLC]+|{ORDINAL_WORD})\b", re.IGNORECASE),
    re.compile(rf"^Rozdzia[łl]\s+{UNIT_NUM}\b", re.IGNORECASE),
    re.compile(rf"^Oddzia[łl]\s+{UNIT_NUM}\b", re.IGNORECASE),
    # No re.IGNORECASE here: lowercase "załącznik nr N do ustawy" is a very
    # common mid-sentence citation (this act refers to its own annexes
    # constantly) that would otherwise false-trigger a paragraph break —
    # unlike Część/Tytuł/Dział, a genuine annex heading is always
    # capitalized, so requiring exact case is the safe default.
    re.compile(r"^Za[łl]ącznik(?:i)?\s+(?:nr\s+\d+|do\s)"),
    re.compile(rf"^Art\.\s*{NUM}\."),
    re.compile(rf"^§\s*{NUM}\."),
    re.compile(rf"^{NUM}\)(?:\d+\))?\s"),  # optional glued footnote ref, e.g. "2)2) tekst"
    re.compile(rf"^{NUM}\.(?:\d+\))?\s"),  # optional glued footnote ref, e.g. "5.8) tekst"
    re.compile(r"^[a-z]\)\s"),
]


def is_marker_start(text: str) -> bool:
    return any(r.match(text) for r in MARKER_RES)


def detect_column_split(words, page_width):
    """Return the x-coordinate of a two-column gutter.

    Finding a candidate: the page's pooled word x0-start distribution
    usually has a wide empty band at the gutter, since (almost) no word
    starts inside it. This can occasionally happen by pure chance on a
    single-column, fully-justified page too, so it's only a candidate.

    Validating it: replay the row-level L/R split this candidate would
    produce (same rule extract_page_lines uses — both sides present with
    a gap under 10pt gets merged as one full-width row). On a genuine
    two-column page, real body text essentially never straddles the
    gutter, so almost no row should hit that merge case. On a
    single-column page, a false-candidate x tends to sit where ordinary
    ~2-4pt word spacing routinely straddles it, so many rows would.
    Reject the candidate if that happens often."""
    if len(words) < 20:
        return None
    xs = sorted(w[0] for w in words)
    best = None
    for a, b in zip(xs, xs[1:]):
        gap = b - a
        mid = (a + b) / 2
        if page_width * 0.35 < mid < page_width * 0.65 and gap > 14:
            if best is None or gap > best[0]:
                best = (gap, mid)
    if not best:
        return None
    split_x = best[1]
    n_left = sum(1 for x in xs if x < split_x)
    n_right = len(xs) - n_left
    if n_left < len(xs) * 0.2 or n_right < len(xs) * 0.2:
        return None

    both_sides = 0
    false_merge = 0
    for ws in cluster_rows(words):
        left = [w for w in ws if (w[0] + w[2]) / 2 < split_x]
        right = [w for w in ws if (w[0] + w[2]) / 2 >= split_x]
        if left and right:
            both_sides += 1
            if right[0][0] - left[-1][2] < 10:
                false_merge += 1
    if both_sides >= 5 and false_merge / both_sides > 0.3:
        return None
    return split_x


ANNEX_PAGE_RE = re.compile(
    r"^Za[łl]ącznik\s+(nr\s+\d+\b|do\s+(?!obwieszczenia\b))", re.MULTILINE
)


def first_annex_page(doc):
    """Page index (0-based) of the first annex/attachment caption, if any.
    Annexes are often tables (coefficient schedules, card templates) whose
    own column boundaries have nothing to do with the main enacting text's
    layout, but a small cluster of such pages can still pass
    detect_column_split's per-page check (real, wide gaps between genuine
    table cells, not word-wrap noise) and then outvote 90+ pages of plain
    single-column prose that show no signal at all — as happened with a
    single 3-page coefficient table at the tail of `ustawa-prawo-budowlane`
    (95 pages, one annex), which detect_doc_column_split mistook for a
    document-wide two-column gutter and used to scramble every other page.
    So the main text's layout is decided only from pages before the first
    annex."""
    for i, page in enumerate(doc):
        if ANNEX_PAGE_RE.search(page.get_text()):
            return i
    return None


def detect_doc_column_split(doc):
    """A document's layout doesn't change mid-way, but a single page's
    signal can be too weak to trust (e.g. a title page with looser
    spacing) — so decide the split once from whichever pages show strong
    evidence, then apply it to every page, including weak/ambiguous ones.
    A flat minimum count (rather than a fraction of all pages) avoids
    missing a genuinely two-column document that also has many
    table/form pages with no column signal of their own (e.g. an
    audit-report rozporządzenie with attached card templates)."""
    annex_at = first_annex_page(doc)
    candidates = []
    for i, page in enumerate(doc):
        if annex_at is not None and i >= annex_at:
            break
        words = page.get_text("words")
        split_x = detect_column_split(words, page.rect.width)
        if split_x is not None:
            candidates.append(split_x)
    if len(candidates) < 3:
        return None
    # A genuine layout puts the gutter at the same x on every page; stray
    # per-page false positives (each page's own row-spacing coincidence)
    # land at scattered, inconsistent x's instead. Require the largest
    # tightly-clustered group, not just any 3 candidates overall.
    candidates.sort()
    best_group = []
    for i in range(len(candidates)):
        j = i
        while j + 1 < len(candidates) and candidates[j + 1] - candidates[i] <= 15:
            j += 1
        if j - i + 1 > len(best_group):
            best_group = candidates[i:j + 1]
    if len(best_group) < 3:
        return None
    return best_group[len(best_group) // 2]


def cluster_rows(words, tol=1.5):
    """Group words into visual lines by y0. A plain round(y0) bucket is not
    safe: two words on the same physical line can land a fraction of a
    point apart (e.g. one run includes a bracketed superscript that shifts
    its reported baseline slightly) and round to different integers,
    silently splitting one line into two. A tolerance-based sweep avoids
    that boundary case."""
    ws_sorted = sorted(words, key=lambda w: w[1])
    clusters = []
    current = []
    ref_y = None
    for w in ws_sorted:
        if current and w[1] - ref_y > tol:
            clusters.append(current)
            current = []
            ref_y = None
        current.append(w)
        ref_y = w[1] if ref_y is None else min(ref_y, w[1])
    if current:
        clusters.append(current)
    return clusters


def extract_page_lines(page, doc_split_x=None, footnote_cutoff=None):
    words = page.get_text("words")
    if footnote_cutoff is not None:
        words = [w for w in words if w[1] < footnote_cutoff]
    words = [
        (w[0], w[1], w[2], w[3], fix_mojibake(w[4]), *w[5:]) for w in words
    ]
    words = [w for w in words if w[4]]  # drop words left empty (e.g. a lone BOM)
    if not words:
        return []

    split_x = doc_split_x

    rows = []  # (y0, side, text) side in ('L','R','F')
    for ws in cluster_rows(words):
        ws = sorted(ws, key=lambda w: w[0])
        y0 = min(w[1] for w in ws)
        if split_x is None:
            text = " ".join(w[4] for w in ws)
            rows.append((y0, "F", text, ws[0][0]))
            continue
        full_text = " ".join(w[4] for w in ws)
        if HEADER_RE.match(full_text) or FOOTER_DATE_RE.match(full_text):
            # A running header/footer can span the full page width with a
            # wide internal gap (e.g. a centered page number vs. a
            # right-aligned "Poz. N") that happens to straddle the column
            # split point — check the whole line before splitting it,
            # or it reads as two-column body text on each side of the gap.
            continue
        left = [w for w in ws if (w[0] + w[2]) / 2 < split_x]
        right = [w for w in ws if (w[0] + w[2]) / 2 >= split_x]
        if left and right:
            gap = right[0][0] - left[-1][2]
            if gap >= 10:
                rows.append((y0, "L", " ".join(w[4] for w in left), left[0][0]))
                rows.append((y0, "R", " ".join(w[4] for w in right), right[0][0]))
            else:
                allw = left + right
                rows.append((y0, "F", " ".join(w[4] for w in allw), allw[0][0]))
        elif left:
            rows.append((y0, "L", " ".join(w[4] for w in left), left[0][0]))
        elif right:
            rows.append((y0, "R", " ".join(w[4] for w in right), right[0][0]))

    rows = [r for r in rows if not HEADER_RE.match(r[2]) and not FOOTER_DATE_RE.match(r[2])]

    if split_x is None:
        rows.sort(key=lambda r: r[0])
        return [(y, x, t) for (y, side, t, x) in rows]

    top_full = sorted((r for r in rows if r[1] == "F" and r[0] < 100), key=lambda r: r[0])
    mid_full = sorted((r for r in rows if r[1] == "F" and 100 <= r[0] < 700), key=lambda r: r[0])
    bottom_full = sorted((r for r in rows if r[1] == "F" and r[0] >= 700), key=lambda r: r[0])
    left_rows = sorted((r for r in rows if r[1] == "L"), key=lambda r: r[0])
    right_rows = sorted((r for r in rows if r[1] == "R"), key=lambda r: r[0])
    ordered = top_full + left_rows + mid_full + right_rows + bottom_full
    return [(y, x, t) for (y, side, t, x) in ordered]


def reflow(lines):
    """Merge a page's visual lines into paragraphs. A new paragraph starts
    at a structural marker, at a large vertical gap, or after a line that
    ends a sentence AND the next line is indented like a new list item."""
    paragraphs = []
    cur = []
    prev_y = None
    for y0, x0, text in lines:
        gap = (y0 - prev_y) if prev_y is not None else 0
        new_para = False
        if not cur:
            new_para = True
        elif is_marker_start(text):
            new_para = True
        elif gap > 20:
            new_para = True
        if new_para and cur:
            paragraphs.append(" ".join(cur))
            cur = []
        if cur and cur[-1].endswith("-") and not cur[-1].endswith("--"):
            cur[-1] = cur[-1][:-1] + text
        else:
            cur.append(text)
        prev_y = y0
    if cur:
        paragraphs.append(" ".join(cur))
    return paragraphs


STRUCTURAL_MARKER_RES = MARKER_RES[:7]  # Księga..Załącznik, not Art./§/list items


def split_glued_headings(paragraphs):
    """A structural heading (Księga/Część/Tytuł/Dział/Rozdział/Oddział) can
    end up glued to the tail of the previous paragraph when reflow() didn't
    see a strong break there (e.g. the previous unit's last sentence ends
    right where a new Księga starts on the same visual line). Re-split any
    paragraph where such a marker appears after its start."""
    out = []
    for p in paragraphs:
        earliest = None
        for rx in STRUCTURAL_MARKER_RES:
            m = rx.search(p)
            if m and m.start() > 0 and (earliest is None or m.start() < earliest):
                earliest = m.start()
        if earliest:
            out.append(p[:earliest].rstrip())
            out.append(p[earliest:])
        else:
            out.append(p)
    return out


def norm_space(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    return text.strip()


LOWER_WORDS = {
    "i", "w", "z", "do", "na", "dla", "oraz", "o", "u", "ze", "we", "a",
    "pod", "nad", "przy", "po", "od", "ku", "za", "the", "of",
}


def smart_title_case(text: str) -> str:
    words = text.split(" ")
    out = []
    for idx, w in enumerate(words):
        core = w.lower()
        if idx > 0 and core in LOWER_WORDS:
            out.append(core)
        else:
            out.append(core[:1].upper() + core[1:] if core else w)
    return " ".join(out)


def heading_and_title(p, next_p):
    """Match a Część/Tytuł/Dział/Rozdział/Oddział heading paragraph; if it
    has no title text of its own, consume the next paragraph as the title
    (common layout where the number and its name are on separate
    lines/paragraphs). Some older codes (Prawo spółdzielcze) render these
    in ALL CAPS, so matching is case-insensitive; the label itself is
    normalized to title case for a consistent heading style.
    Returns (level, heading_text, consumed_next) or None."""
    sentence = lambda s: s[:1].upper() + s[1:].lower()
    # Roman-numeral labels are always upper ("III"); arabic ones ("3a") are
    # left as-is so a lowercase letter suffix doesn't get forced to upper.
    roman_or_asis = lambda s: s.upper() if re.match(r"^[IVXLC]+$", s, re.IGNORECASE) else s
    # A "Załącznik nr N" caption can carry a glued footnote-marker bracket
    # right after its number ("Załącznik nr 1[19)]", from a later-added
    # annex) — peel it off before matching below, or the generic "(.*)"
    # rest-capture swallows it as if it were the title text, which then
    # blocks the next-paragraph-as-title consumption for every such annex.
    zal_footnote = None
    m_zal_fn = re.match(r"^(Za[łl]ącznik\s+nr\s+\d+)(\[\d+\)\])(.*)$", p)
    if m_zal_fn:
        zal_footnote = m_zal_fn.group(2)
        p = m_zal_fn.group(1) + m_zal_fn.group(3)
    for rx, level, num_case in (
        (re.compile(rf"^(Ksi[eę]ga\s+(?:{ORDINAL_WORD}))\b\.?\s*(.*)", re.IGNORECASE), 2, sentence),
        (re.compile(r"^(Cz[eę][śs][ćc]\s+[IVXLC]+)\b\.?\s*(.*)", re.IGNORECASE), 2, str.upper),
        (re.compile(r"^(Tytu[łl]\s+[IVXLC]+)\b\.?\s*(.*)", re.IGNORECASE), 2, str.upper),
        (re.compile(rf"^(Dzia[łl]\s+(?:[IVXLC]+|{ORDINAL_WORD}))\b\.?\s*(.*)", re.IGNORECASE), 3, str.upper),
        # No \b here (unlike the other unit patterns): UNIT_NUM can end in a
        # literal "]" for a prim-suffixed chapter ("Rozdział 1[1]"), and \b
        # can never match between two non-word characters — a "]" directly
        # followed by a space or newline has no word/non-word transition
        # for \b to sit on, so it forced the engine to backtrack UNIT_NUM
        # down to just "1", leaking "[1]" into the title text instead
        # ("Rozdział 1. [1] Prawa członków..." instead of the correct
        # "Rozdział 1[1]. Prawa członków...").
        (re.compile(rf"^(Rozdzia[łl]\s+{UNIT_NUM})\.?\s*(.*)", re.IGNORECASE), 3, roman_or_asis),
        (re.compile(rf"^(Oddzia[łl]\s+{UNIT_NUM})\.?\s*(.*)", re.IGNORECASE), 4, roman_or_asis),
        (re.compile(r"^(Za[łl]ącznik\s+nr\s+\d+)\b\.?\s*(.*)"), 2, lambda s: s),
    ):
        m = rx.match(p)
        if not m:
            continue
        word, num = m.group(1).rsplit(" ", 1)
        rest = m.group(2)
        heading_footnote = None
        # A footnote marker glued right after a letter-suffixed unit number
        # ("Rozdział 6b46) Sprawozdanie...", i.e. "Rozdział 6b" + footnote
        # "46)") reads as if its digits were part of the number, because
        # NUM's letter-suffix branch also swallows trailing digits (needed
        # elsewhere for a genuine glued prim-suffix like "8d1") — the tell
        # is that the "rest" captured after the number then starts with a
        # bare ")", which a real title never does. Recovered by peeling the
        # trailing digits back off `num` and re-bracketing them as a
        # footnote marker, mirroring split_heading_footnote's Art./§
        # handling of the same glue.
        if rest.lstrip().startswith(")"):
            fn_m = re.search(r"(\d+)$", num)
            if fn_m:
                heading_footnote = f"[{fn_m.group(1)})]"
                num = num[: fn_m.start()]
                rest = rest.lstrip()[1:]
        label = f"{word[:1].upper()}{word[1:].lower()} {num_case(num)}"
        if heading_footnote:
            label += f" {heading_footnote}"
        title = rest.strip()
        consumed = False
        if not title and next_p and not is_marker_start(next_p) and len(next_p) < 220:
            title = next_p.strip()
            consumed = True
        if title and title.isupper():
            # section/chapter titles use Polish sentence case, unlike a
            # document's own act-type title line (see smart_title_case)
            title = title[:1] + title[1:].lower()
        if zal_footnote:
            heading = f"{label}. {zal_footnote}"
            if title:
                heading += f" {title}"
        else:
            heading = f"{label}. {title}".strip(". ").replace(". .", ".")
        return level, heading, consumed
    return None


HEADING_FOOTNOTE_RE = re.compile(rf"^(\d+\))\s+((?:{NUM}|§\s*{NUM})\.\s.*)$")

PRIM_SUFFIX_RE = re.compile(r"^(.*\d[a-z]+)(\d+)$")


def bracket_prim(label):
    """Render a NUM unit's glued prim-suffix digit (see NUM's definition)
    in the same bracket form used when the source already writes it out
    literally, e.g. "Art. 9h1" -> "Art. 9h[1]" — one consistent on-page
    convention regardless of which way a given act's typesetting did it.
    Already-bracketed labels ("Art. 5[1]") end in "]", not a bare digit,
    so they pass through unchanged."""
    m = PRIM_SUFFIX_RE.match(label)
    return f"{m.group(1)}[{m.group(2)}]" if m else label


def split_heading_footnote(label, rest):
    """An Art./§ heading whose whole unit was added/changed by a later
    amendment carries a footnote marker glued right after the number, e.g.
    'Art. 12b.5) 1. Kary pieniężne...' — move that marker into the heading
    itself instead of leaving it to read like a stray list item."""
    label = bracket_prim(label)
    m = HEADING_FOOTNOTE_RE.match(rest)
    if m:
        return f"{label}. [{m.group(1)}]", m.group(2)
    return f"{label}.", rest


PARAGRAF_SUBART_RE = re.compile(rf"^Art\.\s*{NUM}\.\s*§")


def paragraf_is_subart(paragraphs):
    """Some codes (Prawo spółdzielcze, Kodeks cywilny) number an article's
    own sub-paragraphs as '§ 1.', '§ 2.' instead of plain '1.', '2.' —
    unlike a rozporządzenie, where '§ N.' IS the top-level unit. Detected
    once per document from any 'Art. N. § 1. ...' paragraph, since that
    combination only happens under the sub-Art convention."""
    return any(PARAGRAF_SUBART_RE.match(p) for p in paragraphs)


def paragraphs_to_md(paragraphs, subart_paragraf=False):
    out = []
    i = 0
    n = len(paragraphs)
    while i < n:
        p = norm_space(paragraphs[i])
        if not p:
            i += 1
            continue
        # A footnote marker glued right after a list/ustęp marker
        # ("2)2) tekst", "5.8) tekst") — bracket it so it doesn't read as
        # a doubled point number.
        p = re.sub(rf"^({NUM}\))(\d+\))(\s)", r"\1[\2]\3", p)
        p = re.sub(rf"^({NUM}\.)(\d+\))(\s)", r"\1[\2]\3", p)
        # Same glue, but on a "Załącznik nr N" caption: the annex number
        # itself has no natural terminator before a run-on footnote digit
        # ("Załącznik nr 119)" = annex 1 + footnote 19), so this assumes a
        # single-digit annex number when a trailing "...)" follows directly
        # — true of every such case seen so far, but not guaranteed for a
        # document with 10+ annexes sharing this exact glue.
        p = re.sub(r"^(Za[łl]ącznik\s+nr\s+\d)(\d+\))(\s|$)", r"\1[\2]\3", p)
        # A plain ustęp/list marker's own glued prim-suffix digit (see NUM) —
        # e.g. an ustęp inserted after ust. 8d gets numbered "8d1." rather
        # than a whole new Art., so it never reaches split_heading_footnote
        # (which only brackets this for an Art./§ heading's own label).
        p = re.sub(r"^(\d+[a-z]+)(\d+)([.)])", r"\1[\2]\3", p)
        next_p = norm_space(paragraphs[i + 1]) if i + 1 < n else None
        hd = heading_and_title(p, next_p)
        m_par = None if subart_paragraf else re.match(rf"^(§\s*{NUM})\.\s*(.*)", p)
        m_art = re.match(rf"^(Art\.\s*{NUM})\.\s*(.*)", p)
        if hd:
            level, heading, consumed = hd
            out.append(f'\n\n{"#" * level} {heading}\n')
            i += 2 if consumed else 1
            continue
        elif m_par:
            label, rest = split_heading_footnote(m_par.group(1), m_par.group(2))
            out.append(f'\n\n### {label}\n\n{rest}')
        elif m_art:
            label, rest = split_heading_footnote(m_art.group(1), m_art.group(2))
            out.append(f'\n\n### {label}\n\n{rest}')
        else:
            out.append(p)
        i += 1
    return "\n\n".join(out)


ZALACZNIK_OBWIESZCZENIA_RE = re.compile(r"Za[łl]ącznik do obwieszczenia\b", re.IGNORECASE)


COVER_PAGE_LINE_RES = [
    re.compile(r"^Dziennik Ustaw$", re.IGNORECASE),
    re.compile(r"^RZECZYPOSPOLITEJ POLSKIEJ$", re.IGNORECASE),
    re.compile(r"^Warszawa, dnia .+ r\.$", re.IGNORECASE),
    re.compile(r"^Poz\. \d+$"),
]


def skip_cover_page(paragraphs):
    """Modern (~2020s) Dziennik Ustaw PDF exports open with a full cover
    page ('Dziennik Ustaw' / 'RZECZYPOSPOLITEJ POLSKIEJ' / publication date
    / 'Poz. N'), each as its own paragraph, before the act's own title."""
    idx = 0
    while idx < len(paragraphs) and any(
        rx.match(paragraphs[idx]) for rx in COVER_PAGE_LINE_RES
    ):
        idx += 1
    return paragraphs[idx:]


def skip_obwieszczenie_preamble(paragraphs):
    """When the PDF is an 'obwieszczenie ws. ogłoszenia jednolitego tekstu'
    wrapping the real act, its own procedural preamble precedes the
    'Załącznik do obwieszczenia ...' line and the real act's own title —
    drop everything up to and including that Załącznik caption. Depending
    on where reflow() happened to see a strong-enough break, the signing
    minister's name can end up glued to the front of that same paragraph,
    or the real act's own 'USTAWA/ROZPORZĄDZENIE ...' title glued to its
    back — so search, don't just match, and keep any such title found
    trailing in the same paragraph instead of discarding it with the rest."""
    for i, p in enumerate(paragraphs):
        m = ZALACZNIK_OBWIESZCZENIA_RE.search(p)
        if not m:
            continue
        tail = p[m.end():]
        title_m = re.search(r"(ROZPORZ[ĄA]DZENIE|USTAWA|OBWIESZCZENIE|UCHWA[ŁL]A)\b", tail)
        rest = [tail[title_m.start():]] if title_m else []
        return rest + paragraphs[i + 1:]
    return paragraphs


def build_title(paragraphs):
    """Detect the ISAP header block: Dz.U. citation, ALL-CAPS act type,
    'z dnia ...' date line, and 'w sprawie ...'/subject line. Returns
    (title_md, remaining_paragraphs)."""
    idx = 0
    citation = None
    if idx < len(paragraphs) and re.match(r"^Dz\.\s*U\.", paragraphs[idx]):
        citation = norm_space(paragraphs[idx])
        idx += 1
    type_line = None
    date_line = None
    combined = re.match(
        r"^(ROZPORZ[ĄA]DZENIE|USTAWA|OBWIESZCZENIE|UCHWA[ŁL]A)\s+(z dnia\b.+)$",
        paragraphs[idx] if idx < len(paragraphs) else "",
    )
    if combined:
        type_line = combined.group(1)
        date_line = combined.group(2)
        idx += 1
    else:
        if idx < len(paragraphs) and paragraphs[idx].isupper():
            type_line = norm_space(paragraphs[idx])
            idx += 1
        if idx < len(paragraphs) and re.match(r"^z dnia\b", paragraphs[idx], re.IGNORECASE):
            date_line = norm_space(paragraphs[idx])
            idx += 1
    subject_line = None
    if idx < len(paragraphs) and not is_marker_start(paragraphs[idx]):
        subject_line = norm_space(paragraphs[idx])
        idx += 1
    h1 = " ".join(
        x for x in (smart_title_case(type_line) if type_line else None, date_line) if x
    )
    body_top = "\n\n".join(x for x in (subject_line,) if x)
    title_md = f"# {h1}\n\n{body_top}\n" if h1 else ""
    return title_md, paragraphs[idx:]


MARKER_ONLY_RE = re.compile(r"^\d+\)$")


def dominant_font_size(doc):
    from collections import Counter
    sizes = Counter()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    sizes[round(span["size"], 1)] += len(span["text"])
    return sizes.most_common(1)[0][0] if sizes else 10.0


def page_footnote_spans(page, body_size):
    """Spans on this page that belong to the footnote-definition block at
    the bottom: smaller than body text, in an unbroken run all the way to
    the last line of the page (a fixed height-fraction cutoff is too
    fragile — a footnote with a long nested list can start well over
    halfway up an otherwise short page)."""
    spans = []
    for block in page.get_text("dict")["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                spans.append(span)
    spans.sort(key=lambda s: (round(s["bbox"][1]), s["bbox"][0]))
    footnote_spans = []
    for span in reversed(spans):
        if not span["text"].strip():
            continue
        if span["size"] < body_size - 0.5:
            footnote_spans.append(span)
        else:
            break
    footnote_spans.reverse()
    return footnote_spans


def footnote_cutoffs(doc, body_size):
    """Per-page y0 above which words are real body text — used to keep
    footnote-definition text (already collected separately) out of the
    main paragraph flow, since the word-level extraction has no font-size
    information of its own to tell the two apart."""
    cutoffs = {}
    for i, page in enumerate(doc):
        spans = page_footnote_spans(page, body_size)
        if spans:
            cutoffs[i] = min(s["bbox"][1] for s in spans) - 1
    return cutoffs


def extract_footnotes(doc):
    """ISAP 'tekst jednolity' pages carry footnote definitions at the page
    bottom in a smaller font than the body text, each starting with a tiny
    superscript 'N)' marker — distinct from the same 'N)' marker appearing
    inline (also small) at its point of reference higher up the page.

    A footnote's own running text can itself contain a short enumeration
    item ("1) ...; 2) ...; 3) ...") when it lists several amended directives
    or similar, and that item's number can land in its own text span whose
    full text is just "3)" — textually indistinguishable from a genuine
    marker by MARKER_ONLY_RE alone. Telling them apart needs font size: the
    real superscript marker is set noticeably smaller than the footnote's
    own body text (both already smaller than the main body, which is why
    both passed page_footnote_spans' cutoff in the first place). Rather
    than a fixed size ratio, the marker size is taken as the smallest size
    actually seen in the footnote region, document-wide — robust as long
    as that relation holds, and it always has so far."""
    body_size = dominant_font_size(doc)
    all_spans = [
        span
        for page in doc
        for span in page_footnote_spans(page, body_size)
        if span["text"].strip()
    ]
    marker_size = min((s["size"] for s in all_spans), default=None)
    footnotes = []
    current = None
    for span in all_spans:
        text = span["text"]
        is_marker = (
            MARKER_ONLY_RE.match(text.strip())
            and marker_size is not None
            and span["size"] <= marker_size + 0.5
        )
        if is_marker:
            if current:
                footnotes.append(current)
            current = [text.strip(), ""]
        elif current:
            text = fix_mojibake(text)
            if current[1].rstrip().endswith("-") and not current[1].rstrip().endswith("--"):
                current[1] = current[1].rstrip()[:-1] + text.lstrip()
            else:
                current[1] += text
    if current:
        footnotes.append(current)
    footnotes = [(m, norm_space(t)) for m, t in footnotes if norm_space(t)]
    # An obwieszczenie's own cover page and the Załącznik it wraps each
    # restart footnote numbering from 1 — since only the Załącznik's body
    # survives skip_obwieszczenie_preamble, keep each marker's LAST
    # occurrence (the wrapper's copy always comes first in page order).
    by_marker = {}
    order = []
    for m, t in footnotes:
        if m not in by_marker:
            order.append(m)
        by_marker[m] = t
    return [(m, by_marker[m]) for m in order]


ACT_TITLE_RE = re.compile(r"^(ROZPORZ[ĄA]DZENIE|USTAWA|OBWIESZCZENIE|UCHWA[ŁL]A)\b")


def trim_to_single_act(paragraphs):
    """ISAP's per-act PDF export is a page-range cut from the Dziennik
    Ustaw issue, so a short act sharing its first/last page with a
    neighbouring act pulls in that neighbour's tail/head text too. Detect
    every ALL-CAPS act-title paragraph; if there's more than one, keep only
    the stretch starting at the first (our act) and ending right before the
    second (the next act bleeding in)."""
    markers = [i for i, p in enumerate(paragraphs) if p.isupper() and ACT_TITLE_RE.match(p)]
    if len(markers) < 2:
        return paragraphs
    return paragraphs[markers[0]:markers[1]]


def convert(pdf_path, title_override=None, skip_pages=0):
    doc = fitz.open(pdf_path)
    doc_split_x = detect_doc_column_split(doc)
    body_size = dominant_font_size(doc)
    cutoffs = footnote_cutoffs(doc, body_size)
    all_lines = []
    for i, page in enumerate(doc):
        if i < skip_pages:
            continue
        all_lines.extend(extract_page_lines(page, doc_split_x, cutoffs.get(i)))
    paragraphs = reflow(all_lines)
    paragraphs = split_glued_headings(paragraphs)
    # Strip the obwieszczenie's own cover page and procedural preamble
    # BEFORE trimming to a single act: its title is itself an ALL-CAPS
    # act-type paragraph, so if trim ran first it could mistake the
    # preamble for "our act" and the real Załącznik-wrapped act for a
    # bleeding-in neighbour, keeping the wrapper and discarding the act.
    paragraphs = skip_cover_page(paragraphs)
    paragraphs = skip_obwieszczenie_preamble(paragraphs)
    paragraphs = trim_to_single_act(paragraphs)
    if title_override:
        title_md = f"# {title_override}\n"
    else:
        title_md, paragraphs = build_title(paragraphs)
    body = paragraphs_to_md(paragraphs, subart_paragraf=paragraf_is_subart(paragraphs))
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    footnotes = extract_footnotes(doc)
    if footnotes:
        fn_lines = ["\n\n## Przypisy\n"]
        for marker, text in footnotes:
            fn_lines.append(f"\n[{marker}] {text}")
        body += "\n" + "\n".join(fn_lines)

    return title_md + "\n" + body


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    title_override = sys.argv[3] if len(sys.argv) > 3 else None
    md = convert(src, title_override=title_override)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"OK: {src} -> {dst} ({len(md)} chars)")
