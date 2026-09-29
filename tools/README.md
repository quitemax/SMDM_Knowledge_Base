# tools/

Skrypty Python napisane w toku budowy tej bazy wiedzy — głównie do
konwersji źródeł (PDF/HTML/DOCX) na Markdown w konwencji używanej w tym
repozytorium, oraz odwrotnie. Żaden z nich nie jest uruchamiany
automatycznie — to narzędzia jednorazowego/doraźnego użycia,
uruchamiane ręcznie przy okazji dodawania nowego dokumentu źródłowego.

**Wspólne zależności** (Python 3, `pip install <pakiet>`):
`pymupdf` (import jako `fitz`), `beautifulsoup4` (`bs4`), `python-docx`
(`docx`, dla dwóch skryptów docx). Żaden skrypt nie wymaga Pandoc ani
LibreOffice.

## Konwersja przepisów prawnych (`przepisy-prawne/`)

### `pdf_to_md.py`

Konwertuje eksport PDF aktu prawnego (ISAP/api.sejm.gov.pl, gdy akt
nie ma dostępnego HTML) na Markdown w tej samej płaskiej konwencji co
reszta bazy (nagłówki Dział/Rozdział/Art./§, kotwice `<a id="...">`,
przypisy zebrane na końcu). Nie używa żadnego modelu AI — parsowanie
oparte wyłącznie na PyMuPDF (pozycje słów na stronie) i regułach
strukturalnych.

```
python pdf_to_md.py <źródło.pdf> <cel.md> [tytuł_zastępczy]
```

**To najbardziej dopracowany skrypt w tym zestawie** — obsługuje
dziesiątki wariantów źle zeskanowanych/złamanych PDF-ów (łamanie
czcionki w starych skanach, układ dwuszpaltowy, obwieszczenia
opakowujące tekst jednolity, przypisy zlepione z numerami punktów,
numerację z sufiksem „prim" w indeksie górnym itd.). **Pełna,
udokumentowana lista napotkanych problemów i sposobów ich obsługi jest
w [`../przepisy-prawne/README.md`](../przepisy-prawne/README.md)** —
przeczytaj tę listę przed modyfikacją skryptu, większość przypadków
brzegowych jest tam już opisana wraz z plikiem, który ją ujawnił.

### `html_to_md.py`

To samo, ale dla aktów z dostępnym tekstem HTML na ISAP
(`api.sejm.gov.pl/eli/acts/DU/{rok}/{pozycja}/text.html`) —
preferowane źródło, gdy dostępne, bo HTML ma już strukturę
(`unit_dzial`, `unit_arti`, `unit_para`, ...), więc parsowanie jest
prostsze i pewniejsze niż z PDF-u. Też bez udziału modelu AI.

```
python html_to_md.py <źródło.html> <cel.md> [tytuł_zastępczy]
```

### `rodo_to_md.py`

Wariant `html_to_md.py` dla RODO — EUR-Lex (Dziennik Urzędowy UE) ma
inny schemat HTML niż ISAP (`eli-container`/`eli-subdivision`,
`oj-ti-art`, `oj-normal`, dwukolumnowe tabele motywów/liter), więc
wymaga osobnego parsera. Używany tylko dla `rodo-rozporzadzenie-2016-679`
— jeśli kiedyś dojdzie inny akt prawa UE, prawdopodobnie da się
ponownie użyć tego skryptu.

```
python rodo_to_md.py <źródło.html> <cel.md> [tytuł_zastępczy]
```

### `toc_and_links.py`

Uruchamiany **po** jednym z powyższych — dopisuje do już
przekonwertowanego pliku `## Spis treści` (linkowany do
Działów/Rozdziałów/Art./§/Załączników) oraz zamienia odniesienia w
treści („art. 5 ust. 2", „§ 3", „rozdziału II") na linki do właściwego
nagłówka — **tylko** gdy odniesienie dotyczy tego samego aktu (nigdy
innej ustawy/rozporządzenia — to i tak zostaje zwykłym tekstem, bo nie
ma tu jego treści) i tylko gdy cel istnieje w pliku (zero martwych
linków).

```
python toc_and_links.py <plik.md> [cel.md]
```

Bez drugiego argumentu nadpisuje plik wejściowy. **Nie jest
bezpieczny do ponownego uruchomienia na już przetworzonym pliku** —
uruchomiony drugi raz na pliku, który już ma spis treści i linki,
tworzy zdublowany, zagnieżdżony spis treści. Przy poprawkach już
przetworzonego pliku najpierw usuń ręcznie sekcję „Spis treści" i
zamień linki `[tekst](#kotwica)` z powrotem na zwykły tekst, dopiero
potem uruchom ponownie. Pełna metodologia regresji (jak bezpiecznie
zmieniać ten skrypt bez psucia już zatwierdzonych 40 plików) — patrz
`przepisy-prawne/README.md`, sekcja o batch 4+.

### `crop.py`

Pomocniczy, do weryfikacji wzrokowej fragmentu strony PDF, gdy tekst
jest nieczytelny/wątpliwy w wyniku konwersji — renderuje wskazany
fragment strony jako obraz PNG do samodzielnego obejrzenia (przez
narzędzie do odczytu obrazów), zamiast całej strony.

```
python crop.py <plik.pdf> <nr_strony_od_1> <x0> <y0> <x1> <y1> [dpi] <wyjście.png>
```

`x0 y0 x1 y1` to współrzędne w ułamkach szerokości/wysokości strony
(0–1), nie w punktach — np. `0 0.1 1 0.3` to górny pasek strony.

## Konwersja dokumentów Word (`projekty/`)

Powstały przy okazji audytu pakietu propozycji dokumentów etycznych —
zamiany `.docx` ↔ `.md` w obie strony, tak żeby treść dało się
edytować/analizować jako Markdown, a potem odtworzyć jako realny
dokument Word.

### `docx_to_md.py`

Czyta plik `.docx` (przez `python-docx`) i zapisuje jego treść jako
Markdown: style „Heading N" → `#`/`##`, pogrubienie/kursywa w runach →
`**...**`/`*...*`, akapity z numeracją Worda (`numPr`) → `- ` (bez
zagnieżdżania), tabele → tabele Markdown.

```
python docx_to_md.py <źródło.docx> <cel.md>
```

Nie obsługuje obrazów, nagłówków/stopek dokumentu ani komentarzy —
tylko główny tekst. Sprawdzone na 7 dokumentach z prostym
formatowaniem (nagłówki, pogrubienia, jedna tabela) — nie testowane na
bardziej złożonych układach.

### `md_to_docx.py`

Odwrotność — czyta plik `.md` (w konwencji używanej w tym
repozytorium: `**Tytuł**` w pierwszej linii jako tytuł dokumentu,
`## § N. ...` jako nagłówki, `**pogrubienie**`/`*kursywa*`/
` ``kod`` ` w tekście, tabele `| a | b |`) i zapisuje jako `.docx`
przez `python-docx`.

```
python md_to_docx.py <źródło.md> <cel.docx>
```

**Znane ograniczenia** (nie było potrzeby ich obsługiwać przy
dotychczasowym użyciu, ale warto wiedzieć przed ponownym użyciem):
- Rozpoznaje tylko **jeden** markdown-owy nagłówek `#`/`##` na
  poziomy 1/2 — głębsze poziomy (`###` i niżej) nie są obsługiwane.
- Listy punktowane `- ` (prawdziwe markdown-owe bullet listy) **nie są
  obsługiwane** — w źródłowych dokumentach nie występowały (numeracja
  „1.", „2." była wpisana jako zwykły tekst akapitu, nie jako lista
  Worda), więc nie było potrzeby ich parsować. Dodanie obsługi przed
  ponownym użyciem na pliku z prawdziwymi listami markdown.
- Łączy kolejne niepuste linie w jeden akapit (tak jak w źródłowych
  plikach `.md` w tym repo, gdzie długie akapity są ręcznie zawijane
  bez pustej linii między fragmentami) — plik z inną konwencją
  zawijania linii wymaga sprawdzenia tego zachowania.
- Weryfikacja jakości konwersji: brak w tym środowisku LibreOffice/
  Pandoc do wyrenderowania podglądu, więc sprawdzanie odbywa się przez
  odczytanie wygenerowanego `.docx` z powrotem przez `python-docx` i
  porównanie tekstu/stylów/pogrubień akapit po akapicie — patrz commit
  historii `projekty/` dla przykładu tego procesu.

## Gdzie te skrypty faktycznie mieszkają

Te pliki to **kopie robocze** — oryginały (i historia ich powstawania,
w tym wszystkie naprawione błędy) żyją w scratchpadach poprzednich
sesji, nie w tym repozytorium przed tym commitem. Ten katalog to
pierwszy raz, gdy trafiają do kontroli wersji — od teraz zmiany w nich
powinny być commitowane tutaj, nie w scratchpadzie.
