# Kontrakt importu (coopOS) — format metadanych i konwencje

Opis formatu, na którym polega aplikacja coopOS importująca to repozytorium.
Walidacja: [`tools/validate_front_matter.py`](../tools/validate_front_matter.py);
generowanie spisów: [`tools/build_indexes.py`](../tools/build_indexes.py)
(patrz [`tools/README.md`](../tools/README.md)).

## Po co to jest

coopOS co jakiś czas (cron) pobiera to repozytorium i publikuje jego treść na stronie:

- `zrodla/` — statut i regulaminy → strona „Dokumenty” (HTML z md + PDF do pobrania),
- `przepisy-prawne/` — akty prawne → strona „Dokumenty / Przepisy prawa” (HTML z md + PDF),
- `wzory/` — wzory wniosków i oświadczeń do pobrania (`kind: wzor`; PDF + md),
- `manual/` — baza wiedzy → strony treści (publiczny „Poradnik mieszkańca” i wewnętrzna „Baza wiedzy”).

Importer nie zgaduje: **plik bez poprawnych metadanych nie jest publikowany** (to celowe — brak
wpisu = brak publikacji, żeby wewnętrzna treść nie wyciekła przez przeoczenie).

## 1. Metadane (front matter) w każdym pliku md

Każdy plik `.md` w `manual/`, `zrodla/md/` (z podkatalogami) i `przepisy-prawne/md/` zaczyna się blokiem YAML:

```yaml
---
title: "Statut Spółdzielni Mieszkaniowej „Doły-Marysińska” w Łodzi"
kind: statut            # statut | regulamin | uchwala | akt-prawny | manual
status: obowiazujacy    # patrz niżej
audience: [public]      # kto może to zobaczyć, patrz niżej
summary: "Podstawowy akt prawny: cel i przedmiot działalności, członkostwo, organy, tytuły prawne do lokali."
---
```

Wartości tekstowe (zwłaszcza zawierające dwukropek, cudzysłowy „…” lub polskie znaki) zapisujemy
w cudzysłowie prostym `"`.

### Pola wspólne

| Pole | Wymagane | Znaczenie |
|---|---|---|
| `title` | tak | Tytuł wyświetlany na stronie i na listach. To on jest kanoniczny: pierwszy nagłówek `#` w treści może się różnić (np. „Ustawa z dnia 26 czerwca 1974 r.” albo „kadry/”), importer usuwa go z treści i pokazuje `title`. |
| `kind` | tak | Rodzaj dokumentu; steruje tym, w którym dziale strony się pojawi. W `zrodla/md/`: `statut`, `regulamin`, `uchwala`; w `przepisy-prawne/md/`: `akt-prawny`; w `wzory/md/`: `wzor`; w `manual/`: `manual`. |
| `status` | tak | `obowiazujacy` (aktualny), `nieaktualny` (zastąpiony, tylko historia), `uchylony` (akt uchylony), `projekt` (w opracowaniu, nie publikować). |
| `audience` | tak | Lista odbiorców, patrz niżej. |
| `summary` | zalecane | Jedno–dwa zdania na listę dokumentów (zastępuje kolumnę „Opis” ze spisu dokumentów). |
| `pdf` | dla `zrodla/` i `przepisy-prawne/` | Ścieżka względna do PDF, np. `../pdf/statut.pdf`. |
| `superseded_by` | gdy `status: nieaktualny` | Nazwa pliku (bez `.md`) dokumentu, który go zastąpił. |

### Pola dodatkowe dla aktów prawnych (`kind: akt-prawny`)

| Pole | Znaczenie |
|---|---|
| `publisher` | Publikator, np. `Dz.U. 2026 poz. 521` (wymagane). |
| `legal_state_date` | Stan prawny na dzień, `RRRR-MM-DD`; pokazujemy go czytelnikowi. Pomijamy, gdy żadne źródło w repozytorium go nie podaje. |
| `source_url` | Adres oficjalnego tekstu (ISAP / EUR-Lex). |

### Pola dodatkowe dla regulaminów i statutu

| Pole | Znaczenie |
|---|---|
| `effective_from` | Data wejścia w życie `RRRR-MM-DD` (jeśli znana). |
| `resolution` | Numer uchwały przyjmującej, np. `338/2024` (jeśli znany). |

### Pola dodatkowe dla `manual/`

| Pole | Znaczenie |
|---|---|
| `section` | Dział, np. `kadry`, `procedury-mieszkancow` (domyślnie nazwa katalogu). |
| `order` | Liczba do sortowania w obrębie działu (domyślnie alfabetycznie po tytule). |
| `incomplete` | `true`, jeśli plik zawiera fragmenty „DO UZUPEŁNIENIA”; strona pokaże baner „Treść w opracowaniu”. |

Plik `README.md` w katalogu działu jest stroną główną tego działu (jego `title` to nazwa działu).

### Pola pomocnicze dla spisów (`zrodla/md/`, `przepisy-prawne/md/`)

| Pole | Znaczenie |
|---|---|
| `category` | Nazwa grupy w spisie dokumentów (`zrodla/spis-dokumentow.md`) lub w tabelach `przepisy-prawne/README.md` (format „N. Nazwa”). Używa go wyłącznie `tools/build_indexes.py`. |
| `order` | Kolejność dokumentu w spisie. Używa go wyłącznie `tools/build_indexes.py`. |

## 2. Odbiorcy (`audience`)

Dozwolone wartości (lista, można kilka):

| Wartość | Kto widzi |
|---|---|
| `public` | każdy, także niezalogowany |
| `resident` | zalogowani mieszkańcy |
| `member` | zalogowani członkowie spółdzielni |
| `membership` | pracownicy działu członkowsko-mieszkaniowego |
| `technical` | pracownicy działu technicznego |
| `finance` | pracownicy działu finansowego |
| `hr` | pracownicy działu kadr (HR) |
| `management` | zarząd |
| `supervisory` | rada nadzorcza |
| `admin` | wyłącznie administratorzy systemu (np. dostępy do systemów IT) |

coopOS mapuje te wartości na uprawnienia (to jego sprawa, nie tego repozytorium). Reguły:

- `public` nie łączymy z innymi wartościami.
- Wątpliwość = węższa grupa. Lepiej, żeby ktoś poprosił o dostęp, niż żeby treść wewnętrzna była publiczna.
- Domyślni odbiorcy dla katalogów `manual/` (każdy plik może to nadpisać swoim `audience`):

| Katalog | Domyślne `audience` |
|---|---|
| `procedury-mieszkancow/` | `[public]` |
| `struktura-organizacyjna/` | `[membership, technical, finance, hr, management, supervisory]`; plik `organy-spoldzielni.md` → `[public]` |
| `zarzad/` | `[management, supervisory]` |
| `rada-nadzorcza/` | `[supervisory, management]` |
| `administracja-techniczna/` | `[technical, management]` |
| `czynsze-ksiegowosc/` | `[finance, membership, management]` |
| `kadry/` | `[hr, management]` |
| `it-systemy/` | `[admin]` |

- `zrodla/md/` (statut, regulaminy), `przepisy-prawne/md/` → `[public]` (jawne), z wyjątkiem
  ewentualnych dokumentów, które trzeba ograniczyć (wtedy wpisz węższą grupę). Uchwały
  Rady Nadzorczej (`kind: uchwala`) → `[member, management, supervisory]`.

## 3. Konwencje treści

1. **Jeden nagłówek `#`** na początku pliku (importer go usuwa z treści, tytuł bierze z `title`). Dalej tylko `##` i niżej.
2. **Spis treści** nie jest potrzebny: importer generuje go sam z nagłówków. Ręcznie napisany blok
   `## Spis treści` z listą odnośników importer usunie z wyniku. Można go zostawić dla czytelności w GitHubie.
3. **Kotwice** `<a id="par-55"></a>` zostają — linki do paragrafów (`/dokumenty/statut#par-55`)
   mają być stabilne. Nie zmieniaj istniejących identyfikatorów bez wyraźnej potrzeby.
4. **Odnośniki między plikami** zapisuj jako względne ścieżki do plików `.md`, np.
   `[regulamin](../../zrodla/md/regulamin-porzadku-domowego-2025.md#par-3)`. Importer przepisze je na
   adresy strony. Odnośnik do pliku, który jest niepubliczny dla czytelnika, pokaże się jako zwykły tekst.
5. **Odnośniki do PDF** — względne ścieżki do plików w `pdf/`; importer zamieni je na linki do pobrania.
6. **Tabele** w składni GFM są obsługiwane. Złożone tabele w obrazach (skany) zostają obrazami.
7. **Aktualizacje** zapisuj jako cytat na początku pliku, jak w statucie
   (`> **Aktualizacja 2026-06-29**: …`) — importer pokaże go jako wyróżnioną uwagę.
8. **Dane osobowe** — opis ról, nie osób.

## 3a. Jak importer interpretuje metadane

| Co | Reguła |
|---|---|
| Adres dokumentu (`zrodla/`, `przepisy-prawne/`) | nazwa pliku md bez `.md`, np. `statut` → `/dokumenty/statut` |
| Adres strony (`manual/`) | ścieżka względem `manual/` z `/` zamienionym na `-`, bez `.md`, np. `kadry/onboarding-pracownika.md` → `/strona/kadry-onboarding-pracownika`; `kadry/README.md` → `kadry` |
| `status: obowiazujacy` | opublikowany (aktualny) |
| `status: nieaktualny` lub `uchylony` | archiwum (widoczny z etykietą „nieaktualny” i linkiem do `superseded_by`) |
| `status: projekt` | nie publikowany (szkic) |
| `kind: uchwala` | **pomijany na tym etapie** (uchwały i sprawozdania dla zalogowanych członków to osobny etap); metadane są uzupełnione, ale importer ich jeszcze nie opublikuje |
| `kind: manual` | strona treści (`manual/`), nie dokument do pobrania |
| plik bez front matter lub z błędnym | **nie jest publikowany**, importer zgłasza błąd w logu |
| zmiana treści pliku | importer porównuje hash i aktualizuje tylko to, co się zmieniło; ręczne edycje w coopOS są nadpisywane, dopóki ktoś nie odłączy dokumentu od źródła |

## 4. Nazwy plików

- Nazwa pliku md = identyfikator dokumentu (slug) w adresie strony, np. `statut.md` → `/dokumenty/statut`.
  Używaj małych liter, cyfr i myślników. **Nie zmieniaj nazwy opublikowanego dokumentu** bez
  `superseded_by`, bo zmieni się jego adres.
- Nazwy dłuższe niż ok. 100 znaków skracaj (limit 260 znaków ścieżki w Windows uniemożliwia klonowanie repozytorium).
- Plik md i PDF tego samego dokumentu mają tę samą nazwę bazową.
- Nazwy plików md w `zrodla/md/` i `przepisy-prawne/md/` są unikalne (to adres dokumentu).

## 5. Czego repozytorium NIE zawiera

- **Wypełnionych formularzy** (dane osobowe). Puste wzory wniosków i oświadczeń są w `wzory/`
  (`kind: wzor`; pole `source_url` wskazuje pierwotny plik na stronie Spółdzielni).
- Danych osobowych, haseł, kluczy.

## 6. Walidacja

`python tools/validate_front_matter.py` (uruchamiane też w GitHub Actions przy każdym pushu i pull requeście) sprawdza:
obecność wymaganych pól, dozwolone wartości `kind`/`status`/`audience`, nagłówek `#` na początku treści,
istnienie pliku `pdf`, to, że `superseded_by` wskazuje istniejący dokument, unikalność nazw plików md oraz
to, że wszystkie względne odnośniki w md (wraz z kotwicami `#...`) prowadzą do istniejących plików i kotwic.
