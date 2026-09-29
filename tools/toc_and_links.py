# -*- coding: utf-8 -*-
"""Add a linked table of contents and self-referencing cross-reference links
to an already-converted przepisy-prawne/md/*.md file.

Design (per user's explicit choices, 2026-09-27):
- Links point to the containing Art./§ (or Rozdział/Dział/Załącznik) heading,
  not to individual ustęp/pkt/lit — those have no anchor of their own.
- A citation is only turned into a link when its target heading actually
  exists in this document; otherwise it's left as plain text (no dead links).
- HTML-sourced files already carry `<a id="...">` anchors (dzial-N, rozdzial-N,
  oddzial-N, art-N, par-N) from html_to_md.py; PDF-sourced files have none, so
  this script adds matching ones using the same prefix convention.
"""
import re
import sys
import unicodedata

HEADING_RE = re.compile(r'^(#{1,4})\s+(.*)$')
ANCHOR_TAG_RE = re.compile(r'^<a id="([^"]+)"></a>$')

# unit_type -> (anchor prefix, nesting rank; lower nests higher/outer)
# The number is captured as [^\s.]+, NOT \S+ — \S+ would greedily swallow a
# directly-following period too (e.g. "1." in "Rozdział 1. Przepisy ogólne"),
# leaving nothing for the separate optional \.? to match and producing a
# num like "1." (period included) instead of "1".
UNIT_PATTERNS = [
    (re.compile(r'^Księga\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'ksiega', 0),
    (re.compile(r'^Część\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'czesc', 1),
    (re.compile(r'^Tytuł\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'tytul', 2),
    (re.compile(r'^Dział\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'dzial', 3),
    (re.compile(r'^Rozdział\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'rozdzial', 4),
    (re.compile(r'^Oddział\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'oddzial', 5),
    # RODO (EU regulation, converted from EUR-Lex HTML, different
    # terminology than ISAP-sourced Polish acts): "Sekcja" for a Rozdział's
    # subdivision instead of "Oddział", and the unabbreviated "Artykuł N"
    # instead of "Art. N" — but its own body text still cites articles the
    # usual abbreviated way ("art. 5"), so REF_RE needs no change, only the
    # heading-side recognition.
    (re.compile(r'^Sekcja\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'oddzial', 5),
    (re.compile(r'^Art\.\s+([^\s.]+)\.?\s*(.*)$'), 'art', 6),
    (re.compile(r'^Artykuł\s+([^\s.]+)\.?\s*(.*)$', re.IGNORECASE), 'art', 6),
    (re.compile(r'^§\s+([^\s.]+)\.?\s*(.*)$'), 'par', 6),
    (re.compile(r'^Załącznik\s+nr\s+(\d+)\.?\s*(.*)$', re.IGNORECASE), 'zalacznik', 0),
]
# a numberless or custom-titled annex heading ("Załącznik - Sposób...",
# "Załączniki") — still a real structural section worth a TOC entry, just
# with no number of its own to match in-body "załącznik nr N" citations
# against.
ZALACZNIK_BARE_RE = re.compile(r'^Załączni\w*\b', re.IGNORECASE)


def strip_brackets(num):
    """"9d[1]" -> "9d1" (canonical key used for both anchors and citations,
    regardless of whether the source wrote the prim suffix as a literal
    bracket or PDFtoMD normalized a glued superscript into one)."""
    return num.replace('[', '').replace(']', '')


def slugify_gfm(text):
    """Approximate GitHub's heading-anchor algorithm: lowercase, strip
    punctuation (keep letters incl. Polish diacritics, digits, spaces,
    hyphens), spaces -> hyphens."""
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch.isalnum() or ch in (' ', '-', '_'):
            out.append(ch)
    text = ''.join(out)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-') or 'sekcja'


class Heading:
    def __init__(self, line_idx, level, text, anchor, utype, num, rank, has_explicit_anchor):
        self.line_idx = line_idx
        self.level = level
        self.text = text
        self.anchor = anchor
        self.orig_anchor = anchor  # before dedupe_anchors may rename it
        self.utype = utype
        self.num = num  # canonical (brackets stripped), or None
        self.rank = rank
        self.has_explicit_anchor = has_explicit_anchor


def classify(text):
    """Return (utype, num, rank, display_num) or None if not a recognized
    structural unit (e.g. 'Treść ustawy', 'Przypisy', a footnote heading)."""
    for rx, utype, rank in UNIT_PATTERNS:
        m = rx.match(text)
        if m:
            num = m.group(1)
            return utype, strip_brackets(num), rank, num
    if ZALACZNIK_BARE_RE.match(text):
        return 'zalacznik', None, 0, None
    return None


def parse_headings(lines):
    headings = []
    for i, line in enumerate(lines):
        if i == 0:
            continue  # the document's own H1 title — not a structural unit
        m = HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()
        anchor = None
        has_explicit = False
        if i > 0:
            am = ANCHOR_TAG_RE.match(lines[i - 1].strip())
            if am:
                anchor = am.group(1)
                has_explicit = True
        if anchor is None:
            anchor = slugify_gfm(text)
        info = classify(text)
        utype, num, rank = ('other', None, 0)
        if info:
            utype, num, rank, _display_num = info
        headings.append(Heading(i, level, text, anchor, utype, num, rank, has_explicit))
    return headings


def dedupe_anchors(headings):
    """GFM appends -1, -2... to a repeated slug; mirror that for computed
    (non-explicit) anchors so our own TOC links match what a renderer without
    the existing <a id> tags would actually produce.

    Explicit <a id> tags are USUALLY trusted as unique, since the converter
    that wrote them normally already made them so — except rodo-rozporzadzenie-2016-679,
    converted by a one-off script outside the ISAP-oriented html_to_md.py
    pipeline (see przepisy-prawne/README.md), whose "sekcja-N" anchors reset
    per Rozdział and so collide across it (four separate "Sekcja 1", one per
    chapter that has sections, all anchored "sekcja-1") — a genuine
    pre-existing formatting defect, not something this script introduces:
    without fixing it, a TOC link to the second/third/fourth "Sekcja 1"
    would jump to the first one instead. So explicit anchors are deduped
    too, same as computed ones; process() then rewrites the actual <a id>
    line wherever this changes one (see fix_duplicate_explicit_anchors)."""
    seen = {}
    for h in headings:
        base = h.anchor
        n = seen.get(base, 0)
        if n:
            h.anchor = f"{base}-{n}"
        seen[base] = n + 1


def build_toc(headings):
    """Nested link list; a heading's TOC depth = number of still-open
    ancestors with a strictly lower rank (see UNIT_PATTERNS)."""
    out = ["<a id=\"spis-tresci\"></a>", "## Spis treści", ""]
    stack = []  # list of rank, in nesting order
    for h in headings:
        if h.utype == 'other':
            continue  # 'Treść ustawy', 'Przypisy', etc. — not worth a TOC row
        while stack and stack[-1] >= h.rank:
            stack.pop()
        indent = "  " * len(stack)
        out.append(f"{indent}- [{h.text}](#{h.anchor})")
        stack.append(h.rank)
    return out


ANCHOR_PREFIX = {
    'ksiega': 'ksiega', 'czesc': 'czesc', 'tytul': 'tytul', 'dzial': 'dzial',
    'rozdzial': 'rozdzial', 'oddzial': 'oddzial', 'art': 'art', 'par': 'par',
    'zalacznik': 'zalacznik',
}


def compute_anchors(headings):
    """Assign each heading's FINAL anchor value before any line is touched,
    then dedupe. Order matters: PDF-sourced headings get the prefix-num
    convention here (e.g. "rozdzial-1"), and Rozdział/Oddział numbering
    often restarts inside each Dział, so two different Działy each have
    their own "Rozdział 1" — deduping has to see these prefix-num values,
    not the pre-assignment placeholder, or collisions slip through."""
    for h in headings:
        if h.has_explicit_anchor or h.utype == 'other':
            continue
        if h.utype in ANCHOR_PREFIX and h.num:
            h.anchor = f"{ANCHOR_PREFIX[h.utype]}-{h.num.lower()}"
    dedupe_anchors(headings)


def apply_anchors(lines, headings):
    """PDF-sourced files have no <a id> tags at all — insert one before every
    heading that doesn't already have one. Also rewrites any EXISTING <a id>
    line that compute_anchors/dedupe_anchors renamed (see dedupe_anchors's
    docstring — rodo-rozporzadzenie-2016-679's "Sekcja" anchors collide
    across chapters in the source itself). Must run after compute_anchors so
    every h.anchor already holds its final, deduped value."""
    inserts = []  # (line_idx, text_to_insert_before)
    for h in headings:
        if h.has_explicit_anchor:
            if h.anchor != h.orig_anchor:
                lines[h.line_idx - 1] = f'<a id="{h.anchor}"></a>'
            continue
        if h.utype == 'other':
            continue
        inserts.append((h.line_idx, f'<a id="{h.anchor}"></a>'))
    for line_idx, text in sorted(inserts, key=lambda x: -x[0]):
        lines.insert(line_idx, text)
    return lines


# --- cross-reference linking -------------------------------------------------

# Whether a citation is self-referencing (link it) or points at a different
# act entirely (don't — there's no target here) hinges on what follows it,
# within the same clause. Polish legal drafting names an external act either
# by its enactment date ("ustawy z dnia 15 lutego 1992 r." — the act-type
# noun and "z dnia" can be several words apart, e.g. "rozporządzenia Prezesa
# Rady Ministrów z dnia...") or, for codes, by name alone ("Kodeksu
# cywilnego", no date). A bare "tej ustawy"/"niniejszego rozporządzenia" is
# the explicit self-reference marker and always wins even if some other
# act's name appears later in the same sentence.
#
# A single lookahead/lookbehind around each citation isn't enough: a
# newly-inserted provision commonly names one specific external act once
# ("...ustawy z dnia 11 stycznia 2018 r. o elektromobilności...") and then
# cites several of ITS articles afterward with bare "art. N" or even "tej
# ustawy" — all still meaning that other act, not the containing document,
# even many words / a full clause later. So instead of only checking the
# text immediately around one citation, the whole paragraph is scanned
# left to right for context-switch markers, and each citation is resolved
# against whichever marker last fired before it:
#   - a dated act citation, a named code/directive/treaty, or a
#     "wymienionej ustawy"/"odnośniku N" footnote cross-reference switches
#     into "foreign" context (no target here, never link);
#   - "tej ustawy"/"niniejszego rozporządzenia" switches back to "self"
#     ONLY when read as introducing a genuine self-reference, i.e. it's
#     kept as a foreign-context marker's own referent when one is already
#     active (see CONTEXT_MARK_RE: matching foreign takes priority when
#     both would match at the same spot, which can't happen here since the
#     two alternatives are mutually exclusive phrasings anyway).
# Before any marker, a paragraph starts in "self" context, since bare
# "art. N ust. M" with no named source at all is the normal way Polish
# legal text cites its own provisions.
CONTEXT_MARK_RE = re.compile(
    r'(?P<foreign>'
    # \w* to catch every Polish case ending ("w ustawie z dnia...", "tej
    # ustawy", "ustawą z dnia...", "rozporządzeniu z dnia..."), not just
    # nominative/genitive — a legal-text false positive from some unrelated
    # "ustaw-"/"rozporządzeni-" word followed by "z dnia" within 60 chars
    # is vanishingly unlikely.
    r'(?:ustaw\w*|rozporządzeni\w*)\b[^.;:]{0,60}?\bz\s+dnia\b'
    # an act can also be named without a date, by short/colloquial title —
    # "ustawy o własności lokali", "ustawie o partnerstwie publiczno-
    # prywatnym" (dative/locative, common after "w"/"o"), "rozporządzenia w
    # sprawie ..." — once introduced by date earlier, a later mention often
    # drops the date and cites just the short title. \w* (not [ya]) so every
    # case ending matches, same reasoning as the "z dnia" alternative above —
    # found missing via ustawa-o-podatku-dochodowym-od-osob-prawnych-cit,
    # where "ustawie o partnerstwie publiczno-prywatnym" (locative) fell
    # through the old [ya]-only class and left "art. 14 ... tej ustawy"
    # wrongly self-linked.
    r'|ustaw\w*\s+o\s+\w+'
    # "ustawy – Prawo budowlane": kept narrowly to [ya] (nominative/genitive
    # only), NOT broadened to \w* like the alternative above — a broader
    # \w* here also matches "ustawą" (instrumental, e.g. "niniejszą ustawą –
    # jednak..."), where the dash is ordinary punctuation pausing the
    # sentence, not introducing a short title, and (with the whole regex's
    # re.IGNORECASE) even matched a plain lowercase word after the dash —
    # found via ustawa-o-dozorze-technicznym-nowelizacja-2026-252.
    r'|ustaw[ya]\s*[-–]\s*[A-ZĄĆĘŁŃÓŚŹŻ]'
    r'|rozporządzeni\w*\s+w\s+sprawie\b'
    # EU acts are commonly cited by year/number instead of a Polish "z dnia"
    # date — "rozporządzenia 2016/679" (RODO/GDPR), "rozporządzenia (UE)
    # 2016/679" — never this document itself. Pre-2015 EU acts reverse the
    # order, number then year — "rozporządzenia (UE) nr 182/2011" — so both
    # orders must match.
    r'|rozporządzeni\w*\s*(?:\([A-ZĄĆĘŁŃÓŚŹŻ]+\)\s*)?(?:nr\s*)?(?:\d{4}/\d+|\d+/\d{4})\b'
    r'|Kodeks\w*\b'
    r'|dyrektyw[ya]?\w*\b'
    r'|Traktat\w*\b'
    r'|[Kk]onstytucj\w*\b'
    # a footnote's own boilerplate ("ustawy, o której mowa w odnośniku 3")
    # always points at whatever act that OTHER footnote cites by date —
    # never this document itself, even though no date appears right here.
    r'|odnośniku\s*\d+\b'
    r'|wymienion[ea][a-ząćęłńóśźż]*\s+(?:ustaw\w*|rozporządzeni\w*|dyrektyw\w*)\b'
    r')'
    r'|(?P<self>\b(?:tej|tego|niniejszej|niniejszego)\s+(?:ustawy|rozporządzenia)\b)',
    re.IGNORECASE,
)


# "art. N tej ustawy" / "§ N tego rozporządzenia" — here "tej"/"tego" is a
# demonstrative naming whichever act art./§ N belongs to (backward-looking:
# whatever act, self or foreign, was already established at that citation's
# own position), NOT a fresh announcement that the paragraph is now "back to
# self". Found via ustawa-prawo-budowlane: "...ustawy z dnia 18 listopada
# 2020 r. o doręczeniach elektronicznych, [...], o którym mowa w art. 40
# tej ustawy, albo [...] o której mowa w art. 2 pkt 7 tej ustawy" — the
# first "art. 40 tej ustawy" correctly stayed foreign (its own backward
# state was already foreign), but unconditionally treating that "tej
# ustawy" as a switch-to-self then wrongly flipped the SECOND, later
# citation ("art. 2 pkt 7") to self, even though the whole sentence is
# still about the foreign doręczenia-elektroniczne act throughout. A
# standalone "tej ustawy"/"niniejszego rozporządzenia" (not glued to a
# citation) is left as a real switch, since that phrasing is a genuine
# paragraph-level statement, not a per-citation qualifier.
CITATION_TAIL_RE = re.compile(
    r'(?:art\.|§)\s*[0-9]+[a-z]*(?:\s*(?:ust\.|pkt|lit\.)\s*[0-9]+[a-z]*\.?)*\s*$',
    re.IGNORECASE,
)
ATTACHED_SELF_FORWARD_RE = re.compile(
    r'^(?:\s*(?:ust\.|pkt|lit\.)\s*[0-9]+[a-z]*\.?)*\s*(?:tej|tego|niniejszej|niniejszego)\s+(?:ustawy|rozporządzenia)\b',
    re.IGNORECASE,
)


# CONTEXT_MARK_RE's "Kodeks\w*\b" alternative is unconditionally foreign —
# fine for every act EXCEPT a document that is itself a Kodeks (currently
# only kodeks-cywilny and kodeks-pracy), which routinely refers to ITSELF
# as bare "kodeksu"/"w kodeksie" or "Kodeksu pracy", with no self-marker
# ("tej/tego/niniejszej/niniejszego ustawy/rozporządzenia" never covers
# "Kodeks"). Found via kodeks-pracy: "...ze zmianami przewidzianymi w art.
# 195 i 196" right after a self-referential "przepisy kodeksu" stayed
# unlinked, even though #art-195/#art-196 exist in the very same document.
# Distinguishing self from foreign here needs a whitelist of the actual
# Polish code names, since the word right after "kodeksu" is often a verb
# ("kodeksu stosuje się") rather than a genuine other-code qualifier — only
# a real qualifier from this list makes the mention foreign; anything else
# (including nothing at all) is this document referring to itself.
KODEKS_QUALIFIER_RE = re.compile(
    r'^(cywiln\w*|karn\w*|post[eę]powania\s+\w+|handlow\w*|sp[oó]łek\s+handlowych|'
    r'celn\w*|wykrocze[nń]\w*|morsk\w*|rodzinn\w*|wyborcz\w*|prac\w*)',
    re.IGNORECASE,
)


def own_kodeks_name(text):
    """If this document IS a Kodeks (its own short title, e.g. "Kodeks
    pracy" on the line right after the H1), return the qualifier stem
    ("prac") so context_switches can recognize self-references to it;
    otherwise None (ordinary ustawa/rozporządzenie, unaffected)."""
    for line in text.split('\n', 6)[1:6]:
        m = re.match(r'^Kodeks\s+(\w+)', line.strip(), re.IGNORECASE)
        if m:
            qm = KODEKS_QUALIFIER_RE.match(m.group(1))
            if qm:
                return qm.group(1)[:4].lower()
    return None


def _is_real_foreign_match(m, text, own_kodeks):
    """Is a CONTEXT_MARK_RE 'foreign' match genuinely foreign? Only ever
    False for the "Kodeks\\w*\\b" alternative, and only when this document
    is itself that same Kodeks — see own_kodeks_name()/KODEKS_QUALIFIER_RE
    above. Shared by context_switches (backward state) and
    is_foreign_context's forward-clause scan, so both directions treat a
    self-referential "kodeksu"/"Kodeksu pracy" the same way."""
    if not own_kodeks or m.group(0)[:6].lower() != 'kodeks':
        return True
    qm = KODEKS_QUALIFIER_RE.match(text[m.end():].lstrip())
    qualifier = qm.group(1)[:4].lower() if qm else None
    return qualifier is not None and qualifier != own_kodeks


def context_switches(text, own_kodeks=None):
    """[(pos, is_foreign, is_attached), ...] in document order, one entry
    per marker. `is_attached` (only meaningful when not is_foreign) marks a
    self-marker glued to a citation — see CITATION_TAIL_RE above."""
    switches = []
    for m in CONTEXT_MARK_RE.finditer(text):
        is_foreign = m.group('foreign') is not None and _is_real_foreign_match(m, text, own_kodeks)
        is_attached = not is_foreign and bool(CITATION_TAIL_RE.search(text[:m.start()]))
        switches.append((m.start(), is_foreign, is_attached))
    return switches


def is_foreign_at(switches, pos, ignore_attached_self=False):
    """`ignore_attached_self`: set when evaluating a citation that is itself
    glued to "tej ustawy" — an earlier glued self-flip from a DIFFERENT such
    citation must not count for it (see CITATION_TAIL_RE docstring above);
    a later bare citation always sees every switch normally."""
    context = False  # self, until a marker before `pos` says otherwise
    for spos, is_foreign, is_attached in switches:
        if spos > pos:
            break
        if ignore_attached_self and is_attached:
            continue
        context = is_foreign
    return context


def is_foreign_context(text, switches, start, end, ignore_attached_self=False, own_kodeks=None):
    """Combines the backward-looking paragraph state (is_foreign_at) with a
    forward check within the same clause: Polish syntax often puts the act's
    name right AFTER the citation ("art. 2 pkt 27 ustawy z dnia 11 stycznia
    2018 r. o elektromobilności...") — before any state-machine marker has
    had a chance to fire — so that also has to be checked directly, scoped
    to the current clause (stopping at the next ./;/: ) so a foreign act
    named later in an unrelated part of a long sentence doesn't leak
    backward onto an earlier, genuinely self-referencing citation."""
    if is_foreign_at(switches, start, ignore_attached_self):
        return True
    clause = forward_clause(text, end)
    return any(
        m.group('foreign') is not None and _is_real_foreign_match(m, clause, own_kodeks)
        for m in CONTEXT_MARK_RE.finditer(clause)
    )


def forward_clause(text, end, cap=200):
    """Text from `end` up to the next ';' (or `cap` chars, whichever comes
    first) — NOT up to the next '.': Polish legal text is full of
    abbreviation periods ("pkt 2 lit. a ustawy z dnia...", "art. 1 ust. 2",
    "2022 r.") that would otherwise cut the window off right before the
    "z dnia" that makes a citation foreign. ';' reliably separates
    enumeration items without that risk. A too-wide window can occasionally
    bleed into unrelated later text in a long sentence, which risks
    under-linking (a missed self-reference) rather than over-linking (a
    wrong one) — the safer failure mode."""
    stop = text.find(';', end, end + cap)
    return text[end:stop if stop != -1 else end + cap]


# Some phrases name a *different* act only indirectly, by pointing at where
# in THIS document that other act is identified: "ustawy zmienianej/
# uchylanej w art. N" (the act this document amends or repeals, identified
# by which of its own articles does the amending/repealing) or
# "rozporządzenia, o którym mowa w § N" (an act named earlier, in this
# document's own § N — e.g. rozporzadzenie-bhp-roboty-budowlane's own § 33
# names a *different* regulation by date, so "załącznika nr 3 do
# rozporządzenia, o którym mowa w § 33" means that other regulation's own
# annex, not this document's). The art./§ number *inside* such a phrase is
# genuinely self-referencing (it really is this document's own unit,
# that's the whole point of identifying the other act *through* it) — only
# text *elsewhere* in the same clause, citing the OTHER act's own
# numbering, is foreign. A persisting CONTEXT_MARK_RE switch can't express
# "foreign here, self right there for this one number", so these are
# checked per-citation instead, in the forward clause window, with the
# referenced kind+number exempted.
# Kept to a short lookahead (much shorter than FOREIGN_LOOKAHEAD_CHARS):
# unlike a dated citation, which can legitimately sit a "pkt 2 lit. a" away,
# these exempting phrases attach directly to the noun phrase they qualify
# ("§ 30 załącznika nr 3 do rozporządzenia, o którym mowa w § 33" — ~20
# chars) — a match found only much further out is more likely a *different*
# clause's own reference (seen in practice: "art. 38 ust. 1, jego funkcje
# sprawuje ... powołany w trybie ustawy, o której mowa w art. 69 ust. 1" —
# the "ustawy" there belongs to "w trybie ustawy", an unrelated later
# clause, ~85 chars from "art. 38", and must NOT suppress it).
EXEMPTING_LOOKAHEAD_CHARS = 60
EXEMPTING_RE = re.compile(
    r'ustaw\w*\s+(?:zmienian\w*|zmienion\w*|uchylan\w*|uchylon\w*|wymienian\w*|wymienion\w*)\s+w\s+(art\.)\s*([0-9]+[a-z]*)'
    r'|(?:ustaw[ya]|rozporządzeni[ae]),?\s+o\s+któr(?:ej|ym)\s+mowa\s+w\s+(art\.|§)\s*([0-9]+[a-z]*)'
    # "ustawy wymienionej w ust. N pkt M" / "rozporządzenia wymienionego w
    # pkt N" (found in ustawa-o-podatku-dochodowym-od-osob-prawnych-cit and
    # ustawa-prawo-energetyczne respectively): unlike the two alternatives
    # above, this points at "ust."/"pkt" — a sub-unit with no anchor of its
    # own, so there's no number here to exempt back to self, only a foreign
    # act to establish. Capturing "ust."/"pkt" as ref_kw is enough: since
    # REF_RE (in link_references) only ever matches "art."/"§" as own_kw,
    # 'art' in 'ust.'/'pkt' is always False, so same_kw below is always
    # False and any art./§ citation earlier in the clause is correctly
    # ruled foreign, with no special-casing needed.
    r'|(?:ustaw\w*|rozporządzeni\w*)\s+wymienion\w*\s+w\s+(ust\.|pkt)\s*([0-9]+[a-z]*)',
    re.IGNORECASE,
)


def is_foreign_via_exempting_phrase(forward_text, own_kw, own_num):
    m = EXEMPTING_RE.search(forward_text)
    if not m:
        return False
    if m.group(1):
        ref_kw, ref_num = m.group(1), m.group(2)
    elif m.group(3):
        ref_kw, ref_num = m.group(3), m.group(4)
    else:
        ref_kw, ref_num = m.group(5), m.group(6)
    same_kw = ('art' in ref_kw.lower()) == ('art' in own_kw.lower())
    return not (same_kw and strip_brackets(ref_num) == strip_brackets(own_num))


REF_RE = re.compile(
    # \b only makes sense before a word character ("art."); § is already a
    # non-word symbol, so putting \b in front of the whole alternation would
    # silently never match it (no word/non-word transition between a space
    # and "§").
    #
    # The bracket alternative goes FIRST (same reasoning as pdf_to_md.py's
    # NUM): `(?:[a-z]+[0-9]*)*` can match zero repetitions and trivially
    # "succeeds" without ever trying the bracket, so a citation like
    # "art. 2[1]" would only capture "2", stranding "[1]" as unlinked text
    # right after the link — nothing here forces the backtrack that saves
    # headings elsewhere.
    #
    # The bracket itself can carry a trailing letter too ("art. 27[3a]",
    # Kodeks pracy/ustawa-o-spoldzielniach-mieszkaniowych convention for a
    # further-subdivided inserted article) alongside the plain-digit form
    # ("art. 24[1]") — without [a-z]* here, "art. 27[3a]" only linked the
    # "art. 27" part, leaving "[3a]" stranded right after the link.
    r'(\bart\.|\bArt\.|§)\s*([0-9]+(?:\[[0-9]+[a-z]*\]|(?:[a-z]+[0-9]*)*)?)'
)
REF_UNIT_RE = re.compile(
    r'\b(Rozdziału|rozdziału|Rozdział|rozdział|Działu|działu|Dział|dział)\s+'
    r'([IVXLC0-9]+(?:\[[0-9]+[a-z]*\])?)'
)
REF_ZAL_RE = re.compile(
    r'\bzałącznik(?:u|iem|a|ów)?\s+nr\s*([0-9]+)', re.IGNORECASE
)


def link_references(text, art_index, par_index, dzial_index, rozdzial_index, zal_index, own_kodeks=None):
    """Replace bare self-references to art./§/rozdział/dział/załącznik with a
    markdown link to the matching heading, only when a heading with that
    exact number exists in this document and the citation isn't clearly
    pointing at a different act (see context_switches/is_foreign_at).

    All three patterns are matched against the ORIGINAL text and resolved
    into a single list of (start, end, replacement) edits before anything
    is substituted — never three sequential .sub() passes each mutating the
    string the next one reads. An exempting phrase like "ustawy uchylanej w
    art. 175" must still be visible as plain text when a *later* pattern
    (e.g. REF_UNIT_RE, for an earlier "rozdziału 6" in the same clause)
    looks forward past it; if an earlier pass had already turned it into
    "[art. 175](#art-175)", the forward regex would no longer recognize it
    and the exemption check would silently stop firing.

    `own_kodeks`: see own_kodeks_name() — non-None only when this document
    is itself a Kodeks."""
    switches = context_switches(text, own_kodeks)
    edits = []  # (start, end, replacement)

    for m in REF_RE.finditer(text):
        kw, num = m.group(1), m.group(2)
        canon = strip_brackets(num)
        index = par_index if kw == '§' else art_index
        anchor = index.get(canon)
        if not anchor:
            continue
        attached = bool(ATTACHED_SELF_FORWARD_RE.match(text[m.end():]))
        if is_foreign_context(text, switches, m.start(), m.end(), ignore_attached_self=attached, own_kodeks=own_kodeks):
            continue
        if is_foreign_via_exempting_phrase(forward_clause(text, m.end(), cap=EXEMPTING_LOOKAHEAD_CHARS), kw, num):
            continue
        edits.append((m.start(), m.end(), f'[{kw} {num}](#{anchor})'))

    for m in REF_UNIT_RE.finditer(text):
        kw, num = m.group(1), m.group(2)
        is_dzial = kw.lower().startswith('dział') or kw.lower().startswith('działu')
        index = dzial_index if is_dzial else rozdzial_index
        key = num.upper() if re.match(r'^[IVXLC]+$', num, re.IGNORECASE) else num
        anchor = index.get(key) or index.get(strip_brackets(key))
        if not anchor:
            continue
        attached = bool(ATTACHED_SELF_FORWARD_RE.match(text[m.end():]))
        if is_foreign_context(text, switches, m.start(), m.end(), ignore_attached_self=attached, own_kodeks=own_kodeks):
            continue
        # a Rozdział/Dział number is never what an exempting phrase itself
        # identifies (that's always an art./§), so any match at all here
        # means foreign — no exemption to check, unlike REF_RE above.
        if EXEMPTING_RE.search(forward_clause(text, m.end(), cap=EXEMPTING_LOOKAHEAD_CHARS)):
            continue
        edits.append((m.start(), m.end(), f'[{kw} {num}](#{anchor})'))

    for m in REF_ZAL_RE.finditer(text):
        num = m.group(1)
        anchor = zal_index.get(num)
        if not anchor:
            continue
        attached = bool(ATTACHED_SELF_FORWARD_RE.match(text[m.end():]))
        if is_foreign_context(text, switches, m.start(), m.end(), ignore_attached_self=attached, own_kodeks=own_kodeks):
            continue
        # a załącznik number is never what an exempting phrase itself
        # identifies either — see REF_UNIT_RE above.
        if EXEMPTING_RE.search(forward_clause(text, m.end(), cap=EXEMPTING_LOOKAHEAD_CHARS)):
            continue
        start, end = m.span(1)
        replacement = m.group(0)[: start - m.start()] + f'[{num}](#{anchor})' + m.group(0)[end - m.start():]
        edits.append((m.start(), m.end(), replacement))

    edits.sort(key=lambda e: e[0])
    out = []
    pos = 0
    for start, end, replacement in edits:
        if start < pos:
            continue  # overlapping match (shouldn't happen; keep the earlier edit)
        out.append(text[pos:start])
        out.append(replacement)
        pos = end
    out.append(text[pos:])
    return ''.join(out)


def process(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    headings = parse_headings(lines)
    compute_anchors(headings)
    lines = apply_anchors(lines, headings)
    # re-parse: line indices shifted by inserted anchors, and this also
    # re-reads each explicit <a id> straight from the (possibly rewritten) line
    headings = parse_headings(lines)

    art_index, par_index, dzial_index, rozdzial_index, zal_index = {}, {}, {}, {}, {}
    for h in headings:
        if h.utype == 'art' and h.num:
            art_index.setdefault(h.num, h.anchor)
        elif h.utype == 'par' and h.num:
            par_index.setdefault(h.num, h.anchor)
        elif h.utype == 'dzial' and h.num:
            dzial_index.setdefault(h.num, h.anchor)
        elif h.utype == 'rozdzial' and h.num:
            rozdzial_index.setdefault(h.num, h.anchor)
        elif h.utype == 'zalacznik' and h.num:
            zal_index.setdefault(h.num, h.anchor)

    toc = build_toc(headings)
    own_kodeks = own_kodeks_name(text)

    heading_line_idx = {h.line_idx for h in headings}
    anchor_line_idx = set()
    for i, line in enumerate(lines):
        if ANCHOR_TAG_RE.match(line.strip()):
            anchor_line_idx.add(i)

    out_lines = []
    toc_inserted = False
    for i, line in enumerate(lines):
        if not toc_inserted and i > 0 and (i in heading_line_idx or i in anchor_line_idx):
            # insert right before the first heading/anchor after the title block,
            # but never before line 0 (the H1) — only once
            out_lines.extend(toc)
            out_lines.append("")
            toc_inserted = True
        if i in heading_line_idx or i in anchor_line_idx:
            out_lines.append(line)
            continue
        out_lines.append(
            link_references(line, art_index, par_index, dzial_index, rozdzial_index, zal_index, own_kodeks)
        )
    if not toc_inserted:
        out_lines.extend(toc)

    return '\n'.join(out_lines)


if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    result = process(src)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"OK: {src} -> {dst}")
