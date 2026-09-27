# Przepisy prawne (źródła zewnętrzne)

Pełne teksty zewnętrznych aktów prawnych wymienionych w
[`zrodla/przepisy-prawne-zewnetrzne.md`](../zrodla/przepisy-prawne-zewnetrzne.md) — w odróżnieniu
od `zrodla/`, to nie są dokumenty Spółdzielni, tylko powszechnie obowiązujące prawo, które
wyznacza ramy jej działalności.

- `pdf/` — oryginalne pliki PDF pobrane z oficjalnych źródeł (głównie
  `api.sejm.gov.pl`/ISAP — Internetowy System Aktów Prawnych Kancelarii Sejmu; RODO z
  mirrora PIBR, jako zapasowe źródło na wypadek, gdyby EUR-Lex zablokował pobieranie).
- `html/` — dla aktów, które mają dostępny tekst w HTML (ISAP `text.html` lub, dla RODO,
  EUR-Lex), surowy HTML pobrany bezpośrednio (bez pośrednictwa modeli AI) — źródło
  pośrednie dla konwersji do `md/`.
- `md/` — wersje przekonwertowane na Markdown. 16 z 35 aktów przekonwertowano z HTML
  (patrz tabele niżej, kolumna „MD”); pozostałe wymagają konwersji z PDF (do zrobienia).

### Stan konwersji do Markdown

16 aktów miało dostępny tekst HTML u źródła i zostało przekonwertowanych bezpośrednio
(konwersja własnym skryptem, nie przez model AI — unika ryzyka parafrazy/skrótów treści
prawnej). Jedno ograniczenie znane: w
`rozporzadzenie-warunki-techniczne-budynkow-i-usytuowanie-2002-UCHYLONE.md` część tabel
(źle zagnieżdżone w źródłowym HTML) nie została odwzorowana — plik ma o tym adnotację i
w razie potrzeby trzeba sprawdzić PDF.

Pozostałe 19 aktów nie ma dostępnego HTML u źródła (sam PDF) — ich konwersja do
Markdown jeszcze się nie odbyła.

Zasada pobierania: dla każdego aktu szukano najnowszego **obowiązującego tekstu
jednolitego** (obwieszczenie Marszałka Sejmu / właściwego ministra ogłaszające jednolity
tekst) na dzień 26-27.09.2026. Jeśli po tekście jednolitym istniała już nowelizacja,
której jeszcze nie ujednolicono urzędowo, pobrano dodatkowo tę nowelizację jako osobny
plik (nazwa z sufiksem `-nowelizacja-RRRR-NNN`) — do ręcznego uwzględnienia przy
konwersji na Markdown.

## Stan na 26-27.09.2026

### 1. Ustrój spółdzielni

| Plik | Źródło (Dz.U.) | Stan prawny na dzień |
|---|---|---|
| `ustawa-prawo-spoldzielcze.pdf` | 2026 poz. 521 | 23.03.2026 |
| `ustawa-o-spoldzielniach-mieszkaniowych.pdf` | 2026 poz. 889 | 10.06.2026 |
| `ustawa-o-wlasnosci-lokali.pdf` | 2026 poz. 232 | — (tekst jednolity z 20.02.2026) |

### 2. Proces budowlany i utrzymanie budynku

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `ustawa-prawo-budowlane.pdf` | 2026 poz. 524 | tekst jednolity, stan na 19.03.2026 |
| `ustawa-prawo-budowlane-nowelizacja-2025-1847.pdf` | 2025 poz. 1847 | nowelizacja z 4.12.2025, wchodzi etapami (część przepisów dopiero 20.09.2026 i 1.04.2027) — **nie jest jeszcze w pełni wliczona** do tekstu jednolitego powyżej |
| `rozporzadzenie-warunki-techniczne-uzytkowania-budynkow-mieszkalnych-1999-UCHYLONE.pdf` | 1999 nr 74 poz. 836 | **UCHYLONE 21.09.2026.** Zastępujące rozporządzenie jeszcze nie zostało opublikowane (trwa proces legislacyjny w MRiT) — 18-miesięczny okres przejściowy pozwala nadal stosować te przepisy |
| `rozporzadzenie-warunki-techniczne-budynkow-i-usytuowanie-2002-UCHYLONE.pdf` | tekst jedn. 2022 poz. 1225 (akt macierzysty 2002 nr 75 poz. 690) | **UCHYLONE 20.09.2026**, ten sam powód co wyżej — zastępujące rozporządzenie ma objąć oba akty naraz |
| `rozporzadzenie-ksiazka-obiektu-budowlanego-c-kob.pdf` | 2022 poz. 2778 | obowiązujący |
| `rozporzadzenie-dziennik-budowy-edb.pdf` | 2023 poz. 45 | obowiązujący |

**⚠️ Do zrobienia priorytetowo:** sprawdzić, czy nowe rozporządzenie zastępujące warunki
techniczne (1999 + 2002) zostało już opublikowane — patrz sekcja „Interwały sprawdzania”
niżej.

### 3. BHP przy robotach budowlanych

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `rozporzadzenie-bhp-roboty-budowlane.pdf` | 2003 nr 47 poz. 401 | brak formalnego tekstu jednolitego — pobrano tekst oryginalny |
| `rozporzadzenie-ogolne-przepisy-bhp.pdf` | 2003 nr 169 poz. 1650 | tekst jednolity, obowiązujący |
| `rozporzadzenie-plan-bioz.pdf` | 2003 nr 120 poz. 1126 | obowiązujący |

### 4. Ochrona przeciwpożarowa

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `ustawa-o-ochronie-przeciwpozarowej.pdf` | 2025 poz. 188 | tekst jednolity; nowelizacja DU 2026/815 (ustawa o zarządzaniu kryzysowym) jeszcze nie wliczona |
| `rozporzadzenie-ochrona-przeciwpozarowa-budynkow.pdf` | 2023 poz. 822 | tekst jednolity |
| `rozporzadzenie-ochrona-przeciwpozarowa-budynkow-nowelizacja-2024-1716.pdf` | 2024 poz. 1716 | nowelizacja z 21.11.2024, jeszcze nie wliczona do tekstu jednolitego powyżej |

Przewody kominowe i CEEB nie mają odrębnego aktu — podstawa to Prawo budowlane (kat. 2)
i ustawa o CEEB (kat. 5).

### 5. Energia, ciepło, termomodernizacja

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `ustawa-o-charakterystyce-energetycznej-budynkow.pdf` | 2024 poz. 101 | tekst jednolity |
| `ustawa-o-wspieraniu-termomodernizacji-i-remontow-oraz-ceeb.pdf` | 2026 poz. 920 | tekst jednolity, stan na 25.06.2026. **Ta ustawa dostaje nowy tekst jednolity wyjątkowo często** (styczeń 2022, październik 2024, wrzesień 2025, lipiec 2026) |
| `rozporzadzenie-audyt-energetyczny.pdf` | 2009 nr 43 poz. 346 | tekst oryginalny (brak tekstu jednolitego) |
| `rozporzadzenie-audyt-energetyczny-nowelizacja-2022-2816.pdf` | 2022 poz. 2816 | najnowsza nowelizacja wzorów kart audytu |
| `ustawa-prawo-energetyczne.pdf` | 2026 poz. 43 | tekst jednolity, stan na dzień ogłoszenia 5.12.2025 |
| `rozporzadzenie-podzielniki-kosztow-ogrzewania.pdf` | 2021 poz. 2273 | obowiązujący |

### 6. Media, odpady, woda

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `ustawa-o-utrzymaniu-czystosci-i-porzadku-w-gminach.pdf` | 2025 poz. 733 | tekst jednolity |
| `ustawa-o-zbiorowym-zaopatrzeniu-w-wode-i-odprowadzaniu-sciekow.pdf` | 2024 poz. 757 | tekst jednolity |
| `ustawa-o-zbiorowym-zaopatrzeniu-w-wode-nowelizacja-2026-605.pdf` | 2026 poz. 605 | duża nowelizacja (wdrożenie dyrektywy UE 2020/2184), weszła w życie 21.05.2026, jeszcze nie wliczona do tekstu jednolitego powyżej |
| `ustawa-prawo-o-miarach.pdf` | 2022 poz. 2063 | tekst jednolity |
| `rozporzadzenie-kontrola-metrologiczna-przyrzadow-pomiarowych.pdf` | 2026 poz. 551 | tekst jednolity (dot. terminów legalizacji wodomierzy — 5 lat, załącznik nr 5) |

### 7. Dźwigi i urządzenia techniczne

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `ustawa-o-dozorze-technicznym.pdf` | 2024 poz. 1194 | tekst jednolity |
| `ustawa-o-dozorze-technicznym-nowelizacja-2026-252.pdf` | 2026 poz. 252 | nowelizacja z 23.01.2026, jeszcze nie wliczona |
| `rozporzadzenie-dozor-techniczny-dzwigi-utb.pdf` | 2018 poz. 2176 | tekst oryginalny (urządzenia transportu bliskiego, w tym dźwigi osobowe) |

### 8. Finanse, rachunkowość, umowy

| Plik | Źródło (Dz.U.) | Uwagi |
|---|---|---|
| `ustawa-o-rachunkowosci.pdf` | 2026 poz. 522 | tekst jednolity |
| `ustawa-o-podatku-dochodowym-od-osob-prawnych-cit.pdf` | 2026 poz. 554 | tekst jednolity, stan na 18.03.2026 |
| `ustawa-prawo-zamowien-publicznych.pdf` | 2026 poz. 793 | tekst jednolity, stan na 25.05.2026 |
| `kodeks-cywilny.pdf` | 2026 poz. 795 | tekst jednolity, stan na 19.05.2026 (całość kodeksu — dla Spółdzielni istotne zwłaszcza art. 647 i nast. o umowie o roboty budowlane, rękojmia, gwarancja) |

### 9. Dane osobowe i sprawy lokatorskie

| Plik | Źródło | Uwagi |
|---|---|---|
| `rodo-rozporzadzenie-2016-679.pdf` | Dz.Urz. UE L 119/1 z 4.5.2016 | rozporządzenie unijne, stosowane wprost, nie ma polskiego tekstu jednolitego do aktualizacji; PDF z mirrora PIBR (zapasowo — EUR-Lex bywa niedostępny, blokada anty-botowa), ale MD przekonwertowano z HTML pobranego bezpośrednio z EUR-Lex |
| `ustawa-o-ochronie-danych-osobowych.pdf` | 2019 poz. 1781 | tekst jednolity z 2019 r.; nowelizacje DU 2026/252 i DU 2026/548 jeszcze nie wliczone |
| `ustawa-o-ochronie-praw-lokatorow.pdf` | 2023 poz. 725 | tekst jednolity |

## Interwały sprawdzania aktualizacji

Nie ma jednego uniwersalnego okresu — zależy od tego, jak często dany akt jest
nowelizowany i jak krytyczny jest dla bieżącej działalności Spółdzielni:

- **Pilne, sprawdzać co miesiąc do wyjaśnienia:** nowe rozporządzenie zastępujące
  warunki techniczne użytkowania budynków (uchylone 1999/2002, kat. 2) — na dzień
  pobrania wciąż nieopublikowane.
- **Co 6 miesięcy** (akty często i istotnie nowelizowane, bezpośrednio wpływające na
  bieżące decyzje Zarządu/Rady Nadzorczej): Prawo spółdzielcze, ustawa o spółdzielniach
  mieszkaniowych, Prawo budowlane, ustawa o wspieraniu termomodernizacji i remontów
  oraz o CEEB (dostaje nowy tekst jednolity średnio raz na 9-12 miesięcy), ustawy
  podatkowe (CIT, rachunkowość) i Prawo zamówień publicznych (zwłaszcza na przełomie
  roku kalendarzowego, gdy zmieniają się progi kwotowe).
- **Raz w roku:** pozostałe ustawy i rozporządzenia z listy (BHP, ochrona
  przeciwpożarowa, dozór techniczny, media/woda/odpady, Kodeks cywilny, RODO/ochrona
  danych osobowych, ochrona praw lokatorów) — chyba że pojawi się konkretny sygnał
  (np. wiadomość o nowelizacji), wtedy sprawdzić od razu.
- **Rozporządzenia bez formalnego tekstu jednolitego** (BHP przy robotach budowlanych
  z 2003 r., audyt energetyczny z 2009 r., dozór dla dźwigów z 2018 r.) — Kancelaria
  Sejmu nie republikuje ich w całości po każdej zmianie, więc trzeba samodzielnie
  sprawdzić listę nowelizacji na stronie ISAP/api.sejm.gov.pl przy każdym przeglądzie,
  nie tylko szukać nowego obwieszczenia.

Przy każdym sprawdzeniu najszybciej zweryfikować status przez
`https://api.sejm.gov.pl/eli/acts/DU/{rok}/{pozycja}` (pole `status`/`inForce` oraz
`nowelizacje po tekście jednolitym`) dla Dz.U. wskazanego w tabelach wyżej.
