# AGENTS.md

Wskazówki dla agentów AI pracujących w tym repozytorium.

## Co to za projekt

Baza wiedzy o strukturze organizacyjnej i procesach Spółdzielni
Mieszkaniowej „Doły-Marysińska" w Łodzi — patrz [README.md](README.md).
To pliki Markdown, nie kod — większość pracy tutaj to pisanie i
redagowanie treści, nie programowanie.

## Zasady pracy z treścią

- **Każdy opisany fakt musi mieć źródło.** Jeśli proces albo zasada
  wynika z regulaminu/statutu, dodaj cytat paragrafu (patrz istniejące
  pliki w `manual/zarzad/`, `manual/czynsze-ksiegowosc/` itd. jako wzór). Nie zgaduj i
  nie wymyślaj procedur.
- **Brak informacji = `DO UZUPEŁNIENIA`, nie wymyślanie.** Jeśli żaden
  regulamin nie opisuje danego procesu operacyjnego, oznacz to wprost
  zamiast wypełniać treścią, która brzmi wiarygodnie, ale nie jest
  prawdziwa.
- **Nowy opisany proces = wspólny szablon.** Patrz
  [`manual/szablon-procesu.md`](manual/szablon-procesu.md).
- **Dane osobowe.** Opisy stanowisk to opis ROLI, nie CV konkretnej
  osoby — bez nazwisk, inicjałów, wynagrodzeń, dat konkretnych umów.
  Pliki dotyczące zakresów obowiązków i umów konkretnych, nazwanych osób
  są celowo pomijane w tym repo (patrz [`zrodla/README.md`](zrodla/README.md)).

## Praca ze źródłami (`zrodla/`)

- `zrodla/pdf/` — oryginalne skany/eksporty PDF, traktuj jako źródło
  ostateczne przy sporach interpretacyjnych.
- `zrodla/md/` — wersje po konwersji OCR na Markdown. **Mogą zawierać
  błędy odczytu** (literówki, źle rozpoznane znaki, pogubione
  formatowanie list/paragrafów). Przy poprawianiu pliku w `zrodla/md/`
  zawsze porównuj z odpowiadającym PDF-em w `zrodla/pdf/` i popraw treść
  tak, żeby wiernie odzwierciedlała oryginał — nie parafrazuj, nie
  zmieniaj sensu.
- Jeśli podczas poprawek natrafisz na fragment nieczytelny nawet w PDF,
  zaznacz to w tekście (np. `[nieczytelne]`) zamiast zgadywać.

## Praca z przepisami prawa (`przepisy-prawne/`)

- **Nowy akt prawny, na który się powołujesz — zaciągnij go, nie cytuj
  z pamięci.** Jeśli w toku pracy trzeba przywołać ustawę/rozporządzenie,
  którego jeszcze nie ma w `przepisy-prawne/`, pobierz jego oficjalny
  tekst jako PDF (i HTML, jeśli dostępny na ISAP/api.sejm.gov.pl — wtedy
  preferowane jako źródło konwersji) do `przepisy-prawne/pdf/` (i
  `przepisy-prawne/html/`), przekonwertuj do `przepisy-prawne/md/`
  narzędziami z [`tools/`](tools/README.md) (`pdf_to_md.py` /
  `html_to_md.py` + `toc_and_links.py`), i dopisz wpis w
  `przepisy-prawne/README.md` oraz `zrodla/przepisy-prawne-zewnetrzne.md`.
  Cytowanie konkretnych artykułów bez tej konwersji (np. tylko na
  podstawie doraźnego sprawdzenia) jest tymczasowo dopuszczalne przy
  szybkiej weryfikacji faktu, ale przed użyciem tego cytatu w
  jakimkolwiek dokumencie, który ma być podstawą decyzji, akt powinien
  przejść pełną konwersję jak reszta.

## Metadane dokumentów

Repozytorium jest importowane przez coopOS — format opisuje
[`docs/kontrakt-importu.md`](docs/kontrakt-importu.md).

- Każdy nowy lub zmieniony plik `.md` w `manual/`, `zrodla/md/` i
  `przepisy-prawne/md/` musi mieć poprawny front matter; plik bez niego
  nie jest publikowany.
- Przed commitem uruchom `python tools/validate_front_matter.py`
  (i `python tools/build_indexes.py`, jeśli zmieniłeś metadane w
  `zrodla/md/` lub `przepisy-prawne/md/` — spisy są generowane).
- Nowy akt prawny wymaga `publisher` i `legal_state_date` (tego drugiego
  nie zgaduj — pomiń, jeśli źródło go nie podaje).
- Nie zmieniaj nazwy opublikowanego pliku md bez potrzeby: nazwa to adres
  dokumentu na stronie. Zastąpiony dokument oznacz `status: nieaktualny`
  i `superseded_by` (nie usuwaj go).
- Wątpliwość co do `audience` = węższa grupa.

## Styl

- Pisz po polsku, w stylu istniejących plików (rzeczowo, bez ozdobników).
- Nie dodawaj dokumentów/plików, o które nikt nie prosił.
