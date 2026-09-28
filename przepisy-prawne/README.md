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
- `md/` — wersje przekonwertowane na Markdown. Wszystkie akty są już przekonwertowane: 16
  z HTML (patrz tabele niżej, kolumna „MD”), pozostałe 20 z samego PDF (patrz niżej).

### Stan konwersji do Markdown

16 aktów miało dostępny tekst HTML u źródła i zostało przekonwertowanych bezpośrednio
(konwersja własnym skryptem `html_to_md.py`, nie przez model AI — unika ryzyka
parafrazy/skrótów treści prawnej), z wyjątkiem RODO — ten plik ma inną strukturę
źródłowego HTML (EUR-Lex, nie ISAP) i nie przechodzi przez ten skrypt; jeśli będzie
potrzebna jego weryfikacja, wymaga osobnego, ręcznego porównania z PDF/HTML, nie
ponownego uruchomienia `html_to_md.py`. Jedno ograniczenie znane: w
`rozporzadzenie-warunki-techniczne-budynkow-i-usytuowanie-2002-UCHYLONE.md` część tabel
(źle zagnieżdżone w źródłowym HTML) nie została odwzorowana — plik ma o tym adnotację i
w razie potrzeby trzeba sprawdzić PDF.

**Naprawiony błąd konwertera HTML (27.09.2026):** gdy punkt wyliczenia lub ustęp
(`unit_pint`/`unit_lett`/`unit_pass`/…) wprowadzał lub zastępował przepis cytowanym
tekstem po dwukropku „w brzmieniu:”, źródłowy HTML owija ten cytat w `<div
class="cite-box">` (znak cudzysłowu otwierającego, właściwa treść w `cite-body`, znak
zamykający, przecinek/średnik/kropka na końcu) — a pętla obsługująca punkty wyliczenia
nie miała żadnej obsługi dla generycznych divów-opakowań (w przeciwieństwie do głównej
ścieżki `process_children`), więc całą zacytowaną treść po prostu pomijała, łącznie z
przypadkami, gdy cytat sam w sobie był całym nowym, wielo-ustępowym artykułem. Naprawione
ogólnie (dodano obsługę `cite-box` z zachowaniem naturalnego podziału na akapity dla
cytowanej treści wieloustępowej). Przy ponownej konwersji wszystkich 16 plików HTML
(oprócz RODO) okazało się, że realna utrata treści dotyczyła tylko 2 plików —
`rozporzadzenie-ochrona-przeciwpozarowa-budynkow-nowelizacja-2024-1716.md` (całe brakujące
§ 28a z 4 ustępami plus dwa inne cytowane fragmenty) i `ustawa-o-ochronie-danych-osobowych.md`
(brakująca treść roty ślubowania Prezesa UODO) — w pozostałych aktach wystąpienia
`cite-box` leżały wyłącznie w pomijanej celowo „treści obwieszczenia” (procedural preamble
obwieszczenia ogłaszającego tekst jednolity), więc nie miały wpływu na treść merytoryczną.

Pozostałe 20 aktów nie ma dostępnego HTML u źródła (sam PDF) — konwersja z PDF
**zakończona** (20 z 20: `rozporzadzenie-warunki-techniczne-uzytkowania-budynkow-mieszkalnych-1999-UCHYLONE`,
`rozporzadzenie-bhp-roboty-budowlane`, `rozporzadzenie-plan-bioz`,
`ustawa-o-wlasnosci-lokali`, `ustawa-prawo-budowlane-nowelizacja-2025-1847`,
`ustawa-o-utrzymaniu-czystosci-i-porzadku-w-gminach`,
`ustawa-o-wspieraniu-termomodernizacji-i-remontow-oraz-ceeb`,
`ustawa-o-spoldzielniach-mieszkaniowych`, `ustawa-o-ochronie-przeciwpozarowej`,
`ustawa-prawo-spoldzielcze`, `ustawa-o-zbiorowym-zaopatrzeniu-w-wode-nowelizacja-2026-605`,
`kodeks-cywilny`, `rozporzadzenie-audyt-energetyczny`,
`rozporzadzenie-kontrola-metrologiczna-przyrzadow-pomiarowych`, `ustawa-o-rachunkowosci`,
`ustawa-prawo-budowlane`, `ustawa-o-dozorze-technicznym-nowelizacja-2026-252`,
`ustawa-prawo-zamowien-publicznych`, `ustawa-o-podatku-dochodowym-od-osob-prawnych-cit`,
`ustawa-prawo-energetyczne`),
przez własny skrypt (PyMuPDF + ręczne reguły), nie model AI. Napotkane problemy źródłowe i
jak skrypt sobie z nimi radzi:
- **łamanie czcionki** (tylko stare, ~2003 r. skany): część znaków diakrytycznych była
  zakodowana w PDF jako inne, niepowiązane symbole (np. „ł”→„∏”, „ń”→„ƒ”, „ś”→„Ê”) —
  wykryte i skorygowane automatycznie (bezpieczne, bo te symbole nigdy nie występują w
  polskim tekście prawnym). Nowsze akty (2020+) tego problemu nie mają.
- **układ dwuszpaltowy**: skrypt wykrywa układ kolumnowy per dokument i scala kolumny
  we właściwej kolejności.
- **pasek tytułowy w „rynnie” między kolumnami** (stare skany): na stronach otwierających
  akt tytuł bywa wydrukowany wąskim pasem dokładnie pomiędzy kolumnami, co myli
  automatyczne wykrywanie kolumn — w `rozporzadzenie-bhp-roboty-budowlane.md` i
  `rozporzadzenie-plan-bioz.md` fragment tytułu/klauzuli wprowadzającej trzeba było
  ręcznie zrekonstruować z surowego tekstu strony (zweryfikowane wobec PDF, nie zgadywane).
- **wycinek PDF obejmuje sąsiedni akt**: eksport ISAP dla krótkiego aktu bywa cięciem po
  stronach Dziennika Ustaw, więc ciągnie ze sobą końcówkę poprzedniego aktu i/lub
  początek następnego, który dzieli z nim stronę — skrypt wykrywa i przycina do
  właściwego aktu po tytule ustawy/rozporządzenia (zastosowane w `rozporzadzenie-plan-bioz`,
  gdzie oryginalny PDF zawierał fragmenty sąsiednich aktów: rozporządzenia o
  funkcjonariuszach ABW przed i rozporządzenia o wzorach wniosków budowlanych po).
- **obwieszczenie opakowujące tekst jednolity** (nowsze akty): skrypt wykrywa nagłówek
  strony tytułowej Dziennika Ustaw i proceduralny wstęp obwieszczenia Marszałka Sejmu i
  pomija je, zaczynając właściwą treść od „Załącznik do obwieszczenia…” (ten sam wzorzec
  co przy konwersji z HTML).
- **przypisy dolne** (tekst jednolity z historią nowelizacji): skrypt wykrywa blok
  przypisów na dole strony po mniejszej czcionce (a nie sztywnym progu wysokości strony,
  bo długi przypis z zagnieżdżoną listą może zaczynać się wysoko na stronie) i zbiera je
  w sekcję „## Przypisy” na końcu pliku, tak jak w plikach z HTML.
- **numeracja z sufiksem w nawiasie kwadratowym** („art. 24[1]”, „ust. 1[1]”): niektóre
  akty oznaczają wstawiony przepis nie literą („24a”) tylko taką notacją zamiast
  indeksu górnego („24¹”) — to autentyczny sposób zapisu w źródle (zweryfikowane wizualnie
  w PDF), skrypt rozpoznaje go jak zwykły sufiks jednostki, żeby poprawnie dzielić
  akapity i nagłówki.
- **precyzja grupowania linii**: dwa słowa na tej samej fizycznej linii mogą mieć
  nieznacznie różny raportowany y0 (np. gdy jeden fragment zawiera indeks w nawiasie
  kwadratowym) i przy grupowaniu przez proste zaokrąglenie trafić do różnych „wierszy” —
  skrypt grupuje słowa w linie z tolerancją, a nie sztywnym zaokrągleniem, co naprawiło
  kilka wcześniej niezauważonych przestawień słów (m.in. jednostki „m2”/„m3” w kilku już
  wcześniej skonwertowanych plikach — poprawione przy okazji).
- **wzory matematyczne w załącznikach**: formuła w PDF czasem nie odwzorowuje się jako
  sensowny tekst (np. `ustawa-o-wspieraniu-termomodernizacji...`, wzór na premię
  kompensacyjną) — w takim wypadku strona źródłowa jest renderowana jako obraz i wzór
  przepisywany ręcznie na tej podstawie, z adnotacją w pliku wskazującą, że tak powstał.
- **„§” jako jednostka wewnątrz artykułu, nie samodzielna jednostka**: w rozporządzeniach
  „§ N.” jest jednostką najwyższego poziomu (jak „Art.” w ustawach), ale niektóre starsze
  ustawy/kodeksy (Prawo spółdzielcze, Kodeks cywilny) numerują akapity wewnątrz artykułu
  jako „§ 1.”, „§ 2.” zamiast zwykłych liczb — skrypt wykrywa ten wzorzec (obecność
  „Art. N. § 1.” w dokumencie) i wtedy nie traktuje „§ N.” jako nagłówka.
- **wyższe jednostki podziału**: oprócz Rozdziału/Działu skrypt obsługuje też Część, Tytuł
  i Księgę (Kodeks cywilny: Księga > Tytuł > Dział > Rozdział), w tym zapis wielkimi
  literami („CZĘŚĆ I”, spotykany w Prawie spółdzielczym) i numerację słowną Księgi
  („Księga pierwsza” zamiast cyframi rzymskimi).
- **Rozdział/Oddział numerowane cyframi rzymskimi**: większość aktów używa cyfr arabskich
  („Rozdział 1”), ale Kodeks cywilny konsekwentnie używa rzymskich („Rozdział I”) —
  skrypt rozpoznaje oba warianty.
- **próg wykrywania układu dwuszpaltowego zbyt wysoki dla dokumentów z załącznikami
  tabelarycznymi**: dokument uznawany był za jednoszpaltowy, jeśli mniej niż ~30% stron
  wykazywało sygnał kolumn — zbyt agresywne dla aktu, którego większość stron to
  załączniki/tabele (np. `rozporzadzenie-audyt-energetyczny`, gdzie tylko 5 z 44 stron to
  właściwy, dwuszpaltowy tekst przepisów, reszta to wzory kart audytu). Próg obniżony do
  stałej liczby stron (3), niezależnie od długości dokumentu.
- **załączniki w formie obrazu (nieczytelne tabele)**: niektóre starsze rozporządzenia
  mają załączniki (wzory formularzy/kart) osadzone jako zeskanowana grafika, nie tekst —
  w takim wypadku plik ma adnotację, że dany załącznik nie został skonwertowany, i odsyła
  do PDF (zastosowane w `rozporzadzenie-audyt-energetyczny`, załączniki nr 1–4).
- **nagłówek strony rozbity przez wykrywanie kolumn**: nagłówek typu „Dziennik Ustaw – N
  – Poz. NNN” bywa jedną linią rozciągniętą na całą szerokość strony z szerokim odstępem
  wewnętrznym (np. wyśrodkowany numer strony vs. wyrównany do prawej „Poz.”) — jeśli ten
  odstęp trafiał akurat w punkt podziału kolumn, skrypt dzielił nagłówek na dwie części
  jak zwykły tekst dwuszpaltowy, więc nigdy nie pasował do wzorca nagłówka i przeciekał do
  treści. Naprawione: skrypt sprawdza wzorzec nagłówka na całej (niepodzielonej) linii,
  zanim w ogóle rozważy podział na kolumny.
- **fałszywe wykrycie układu dwuszpaltowego** (`rozporzadzenie-kontrola-metrologiczna-...`):
  dokument jest w całości jednoszpaltowy, ale zwykłe odstępy między wyrazami w
  wyjustowanym tekście przypadkiem utworzyły pozorną „szczelinę” w rozkładzie pozycji
  początków wyrazów blisko środka strony, co myliło wykrywanie kolumn. Naprawione:
  kandydat na szczelinę kolumn jest teraz dodatkowo weryfikowany przez sprawdzenie, czy
  przy tym podziale rzeczywiście niewiele linii miałoby tekst „przeskakujący” przez niego
  z małym odstępem (co dla prawdziwej kolumny prawie nigdy się nie zdarza, a dla zwykłego
  tekstu jednoszpaltowego — bardzo często).
- **obwieszczenie + wykrywanie „PDF obejmuje sąsiedni akt” w złej kolejności**: gdy
  wykrywanie sąsiedniego aktu (patrz wyżej) uruchamiało się przed pominięciem wstępu
  obwieszczenia, własny tytuł obwieszczenia i tytuł właściwego aktu w załączniku bywały
  mylnie potraktowane jako „dwa sąsiadujące akty”, co ucinało całą właściwą treść,
  zostawiając tylko proceduralny wstęp obwieszczenia. Kolejność kroków odwrócona: najpierw
  pominięcie strony tytułowej/wstępu obwieszczenia, dopiero potem wykrywanie sąsiedniego
  aktu.
- **zdublowane przypisy z tekstu jednolitego i strony obwieszczenia**: obwieszczenie i
  załącznik, który opakowuje, czasem numerują przypisy od nowa, więc ten sam numer (np.
  „1)”) mógł się pojawić dwa razy z niemal identyczną, ale nie identyczną treścią — skrypt
  teraz zachowuje tylko ostatnie (chronologicznie późniejsze, czyli należące do
  właściwego aktu) wystąpienie danego numeru przypisu.
- **numer przypisu zlepiony z numerem punktu/ustępu** (np. „2)2) tekst”, „5.8) tekst”):
  gdy nowelizacja dodaje przypis do istniejącego punktu listy, numer przypisu bywa
  wydrukowany bezpośrednio po numerze punktu bez odstępu, co czytało się jak
  zdublowany/błędny numer punktu — skrypt rozpoznaje ten wzorzec i nawiasuje numer
  przypisu (`2)[2)] tekst`), żeby było jasne, że to dwa różne numery.
- **`Załącznik nr N` jako nagłówek**: skrypt teraz rozpoznaje podpis załącznika jako
  osobny nagłówek (dopasowanie z rozróżnianiem wielkości liter, żeby nie łapać zwykłych,
  małą literą pisanych odwołań w zdaniu typu „określa załącznik nr 5 do ustawy”) i, jeśli
  następny akapit to krótki (<220 znaków), niebędący numerowaną pozycją tytuł, dołącza go
  do nagłówka. Ten sam numer bywa zlepiony z numerem przypisu („Załącznik nr 119)” = nr 1
  + przypis 19) — skrypt zakłada wtedy jednocyfrowy numer załącznika i nawiasuje przypis
  osobno (`Załącznik nr 1[19)]`), a tytuł z kolejnego akapitu nadal poprawnie dołącza.
- **fałszywe wykrycie układu dwuszpaltowego przez tabelę w załączniku** (`ustawa-prawo-budowlane`,
  95 stron, 1 załącznik-tabela na 3 ostatnich stronach): dokument jest w całości
  jednoszpaltowy, ale prawdziwa szczelina między kolumnami tabeli w załączniku przeszła
  walidację jako gdyby to była szczelina kolumn głównego tekstu, i cały dokument (92 strony
  zwykłej prozy) został błędnie podzielony na dwie kolumny, co poprzestawiało kolejność
  fragmentów zdań na każdej stronie. Naprawione: wykrywanie układu kolumnowego bierze pod
  uwagę tylko strony sprzed pierwszego napotkanego podpisu „Załącznik nr N”/„Załącznik do
  ustawy/rozporządzenia” (ale nie „Załącznik do obwieszczenia”, czyli własnego opakowania
  obwieszczenia — to nie jest treściowy załącznik aktu).
- **numer wyliczenia wewnątrz treści przypisu mylony z markerem nowego przypisu**
  (`ustawa-prawo-budowlane`, przypis 1): gdy przypis sam zawiera numerowane wyliczenie
  („[...]: 1) dyrektywy...; 2) częściowo...; 3) częściowo...”), pozycja takiego wyliczenia
  może trafić do własnego fragmentu tekstu, którego cała treść to tylko „3)” — nie do
  odróżnienia od prawdziwego, małego markera nowego przypisu przez samo dopasowanie wzorca,
  więc przypis 1 urywał się w połowie, a jego dalsza treść ginęła jako fałszywy „przypis 3)”
  (nadpisywany później przez prawdziwy przypis 3). Naprawione: marker przypisu rozpoznawany
  jest teraz też po rozmiarze czcionki (najmniejszy rozmiar występujący w obszarze przypisów
  w całym dokumencie), a nie tylko po treści.
- **konwencja „Art. N. § 1.” użyta tylko w jednym cytowanym przepisie wewnątrz ustawy
  nowelizującej** (`ustawa-o-dozorze-technicznym-nowelizacja-2026-252` — mimo nazwy pliku
  to obszerna nowelizacja wdrażająca dyrektywę NIS2, głównie zmieniająca ustawę o krajowym
  systemie cyberbezpieczeństwa; przepis dotyczący dozoru technicznego to tylko jeden art.
  wśród ok. 50): art. 6 tej ustawy wstawia do Ordynacji podatkowej nowy art. 299i, który —
  zgodnie z konwencją Ordynacji podatkowej — dzieli się na „§ 1.”, „§ 2.”, „§ 3.” zamiast
  zwykłych ustępów. Skrypt wykrywa tę konwencję tylko globalnie dla całego dokumentu (po
  wystąpieniu „Art. N. § 1.” na początku akapitu), a cytowany art. 299i zaczyna się w
  środku akapitu (po „w brzmieniu: „Art. 299i. § 1. ...”), więc nie został wykryty — „§ 2.”
  i „§ 3.” zostały błędnie potraktowane jako nagłówki najwyższego poziomu. Poprawione
  ręcznie (za wąski, jednorazowy przypadek na całe dotychczasowe 17 plików, żeby uzasadniać
  zmianę w skrypcie); do obserwacji, czy powtórzy się w kolejnych aktach.
- **załączniki w formie rozbudowanych tabel wielostronicowych** (`ustawa-o-dozorze-technicznym-nowelizacja-2026-252`,
  załączniki nr 1–3: klasyfikacja sektorów/podsektorów/rodzajów podmiotów z kolumnami progu
  wielkości „I II III”): podobnie jak przy `rozporzadzenie-kontrola-metrologiczna...`, tekst
  jest odzyskany, ale bez struktury tabeli — plik ma o tym adnotację i w razie potrzeby
  trzeba sprawdzić PDF.
- **przypis do pozycji wewnątrz innego przypisu, oznaczony cyfrą rzymską zamiast arabskiej**
  (`ustawa-prawo-zamowien-publicznych`, przypis 1): jedna z pozycji w wykazie
  dyrektyw/rozporządzeń wymienionych w przypisie 1 do tytułu ustawy ma własną, odrębną
  adnotację o późniejszej zmianie, oznaczoną „I)” zamiast zwykłej cyfry — żeby nie
  kolidować z arabską numeracją głównych przypisów (1–74). Skrypt rozpoznaje tylko markery
  cyfrowe (`\d+\)`), więc tekst „I) W brzmieniu ustalonym...” doczepił się do końca
  przypisu 1 zamiast być osobną pozycją. Poprawione ręcznie (pierwszy taki przypadek na 18
  plików); do obserwacji.
- **załącznik w formie rozbudowanej tabeli liczbowej** (`ustawa-o-podatku-dochodowym-od-osob-prawnych-cit`,
  załącznik nr 1: Wykaz rocznych stawek amortyzacyjnych, 6 stron, tabela Pozycja/Stawka
  %/Symbol KŚT/Nazwa środka trwałego): tekst jest odzyskany, ale bez struktury tabeli, a
  błędne przypisanie stawki % do symbolu KŚT miałoby realny skutek podatkowy — plik ma o
  tym adnotację i w razie potrzeby trzeba sprawdzić PDF. Pozostałe załączniki tej ustawy
  (listy podmiotów/krajów UE, wykaz usług) to listy nazw bez tego ryzyka, więc zostały bez
  adnotacji.
- **jednostka z literowym sufiksem, do której doklejono własny sufiks „prim” (wstawiona
  jednostka po już-literowej)** (`ustawa-prawo-energetyczne`, 48 wystąpień — najbardziej
  poszkodowany plik ze wszystkich): oprócz zwykłego sufiksu literowego („24a”) i sufiksu
  „prim” zapisanego wprost nawiasem kwadratowym w źródle („24[1]”, patrz wyżej), ta ustawa
  (wyjątkowo mocno nowelizowana) zawiera dużo jednostek z sufiksem prim doklejonym do
  jednostki, która już ma sufiks literowy — zapisanym w PDF jako prawdziwy, mniejszy
  indeks górny („Art. 9d¹”, „ust. 8d²”), a nie nawiasem. PyMuPDF grupuje słowa wyłącznie po
  położeniu, nie po foncie, więc taki indeks trafiał w jedno słowo z bazową jednostką bez
  żadnego separatora („9d1”, „8d2”) — wzorzec jednostki nigdy tego nie rozpoznawał jako
  początek jednostki/nagłówka, więc cała jednostka (czasem cały akapit) doklejała się do
  poprzedniej. Dotyczyło to całych serii wstawionych artykułów (np. Art. 9d¹, 9e¹, 9h¹–9h³)
  i ustępów (np. ust. 8d¹–8d¹⁶, 8g¹–8g⁸) — czyli sporej części przepisów o przyłączaniu
  mikroinstalacji OZE do sieci. Naprawione ogólnie: cyfra bezpośrednio po sufiksie literowym
  jest teraz zawsze rozpoznawana jako doklejony sufiks prim (bezpieczne, bo sufiks literowy
  w prawdziwej polskiej numeracji nigdy sam nie kończy się gołą cyfrą) i przy renderowaniu
  ujmowana w nawias kwadratowy dla jednego, spójnego zapisu niezależnie od tego, jak
  zrobił to dany akt („Art. 9d1” → „Art. 9d[1]”); obsłużone też zagnieżdżenie głębsze niż
  jeden poziom („ust. 8d2a” — kolejny sufiks literowy po cyfrze prim), choć tam sama cyfra
  zostaje bez nawiasu (nie wygląda jak literówka, bo kończy się literą, nie cyfrą). Pełna
  regresja na 19 wcześniej zatwierdzonych plikach nie wykazała żadnych zmian — ten wzorzec
  w ogóle w nich nie występował.

Wszystkie 20 aktów bez HTML u źródła zostały sprawdzone i przekonwertowane. Zbieranie
napotkanych problemów źródłowych (lista wyżej) można uznać za zamknięte dla obecnego
zestawu plików — nowy problem tego typu pojawi się dopiero przy kolejnym akcie dodanym do
tego katalogu.

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

## Spis treści i linkowane odniesienia (w toku)

Każdy plik w `md/` dostaje: (1) `## Spis treści` zaraz po tytule, linkujący do
Działów/Rozdziałów/Oddziałów/Art./§/Załączników w dokumencie, (2) w treści — bez
zmieniania samego brzmienia — odniesienia typu „art. 5 ust. 2”/„§ 3”/„rozdziału II”/
„załącznika nr 1” zamienione na link do właściwego nagłówka, **tylko gdy dotyczą tego
samego aktu** (nie do innej ustawy/rozporządzenia/Kodeksu/dyrektywy — te zostają zwykłym
tekstem, bo nie ma tu ich treści) **i tylko gdy cel istnieje w pliku** (żadnych martwych
linków). Link prowadzi do całego artykułu/paragrafu, nie do pojedynczego ustępu/punktu —
te nie mają własnych kotwic. Pliki z HTML mają już kotwice `<a id="...">` z
`html_to_md.py` (`dzial-N`, `rozdzial-N`, `oddzial-N`, `art-N`, `par-N`); pliki z PDF
dostają analogiczne kotwice dopisane tym samym skryptem wzbogacającym
(`toc_and_links.py`, w tym samym scratchpadzie co konwertery). Robione seriami po 3
pliki, z przerwą na przegląd.

Rozpoznawanie „obcego” aktu przy odniesieniu jak „art. 2” nie ogranicza się do sprawdzenia
tekstu bezpośrednio przed/po cytacie — skrypt skanuje cały akapit jako sekwencję
przełączników kontekstu („ustawy/rozporządzenia... z dnia...”, „Kodeksu...”, „wymienionej
ustawy”, „ustawy, o której mowa w odnośniku N” → kontekst obcy; „tej ustawy”/„niniejszego
rozporządzenia” → kontekst własny, *chyba że* wcześniej w tym samym akapicie nazwano już
inny akt, bo wtedy to zaimkowe odniesienie zwykle wraca do TEGO aktu, nie do
konwertowanego dokumentu — np. „ustawy z dnia 11 stycznia 2018 r. o
elektromobilności... w rozumieniu art. 2 pkt 3 tej ustawy” dalej mówi o ustawie o
elektromobilności). Dodatkowo sprawdzane jest też najbliższe otoczenie PO cytacie w tej
samej klauzuli — do najbliższego „;” (NIE „.”: polskie skróty prawne, „lit. a”, „pkt 2”,
„2022 r.”, obcinałyby okno tuż przed „z dnia”, które dopiero czyni cytat obcym), bo szyk
polski często stawia numer artykułu przed nazwą aktu („art. 2 pkt 27 ustawy z dnia...”),
zanim jakikolwiek wcześniejszy przełącznik kontekstu zdążyłby zadziałać. Akt bywa też
nazwany bez daty, samym (krótkim) tytułem — „ustawy o własności lokali”, „ustawy – Prawo
budowlane”, „rozporządzenia w sprawie...” — to również rozpoznawane jako kontekst obcy.
Osobny przypadek: „ustawy zmienianej w art. N” nazywa inny akt przez wskazanie, GDZIE w
tym dokumencie go nowelizuje — więc samo „art. N” w tej frazie zostaje linkiem do tego
dokumentu (to naprawdę jego artykuł), ale każde INNE odniesienie do numeracji przed tą
frazą w tej samej klauzuli („art. 5 ust. 14 ustawy zmienianej w art. 43” — art. 5 należy
tam do aktu nowelizowanego w art. 43, nie do tego dokumentu) jest traktowane jako obce.

Ta seria (batch 4) ujawniła też dwa oddzielne, wcześniejsze błędy w samym `pdf_to_md.py`
(nie w `toc_and_links.py`), obecne od dawna w już zatwierdzonych plikach — nagłówek
Rozdziału/Oddziału z sufiksem „prim” w nawiasie kwadratowym („Rozdział 1[1]”) albo z
doklejonym numerem przypisu bez nawiasu („Rozdział 6b46)”) nie był poprawnie rozpoznawany:
`\b` w `heading_and_title()` nie może dopasować się między dwoma znakami
nie-alfanumerycznymi (np. „]” i spacją), więc silnik nigdy nie cofał się do próby
dopasowania nawiasu, a dla doklejonego przypisu brakowało odpowiednika
`split_heading_footnote()`, który mają already Art./§. Efekt: taki nagłówek albo w ogóle
nie był rozpoznawany jako nagłówek (zwykły akapit), albo numer jednostki i numer przypisu
zlewały się w jedno. Naprawione ogólnie w `pdf_to_md.py` (kolejność alternatyw w `NUM`,
usunięcie zbędnego `\b`, dodanie analogicznego rozdzielania doklejonego przypisu) i
zastosowane retroaktywnie do `ustawa-o-spoldzielniach-mieszkaniowych` (3 nagłówki
Rozdziałów) i `ustawa-o-rachunkowosci` (2 nagłówki) — jedyne dwa dotychczas zatwierdzone
pliki, w których ten wzorzec się pojawia (sprawdzone na wszystkich 20). Ten sam błąd
kolejności alternatyw dotyczył też cytowań w treści (`art. 2[1]`, `rozdziału 2[1]`) w
`toc_and_links.py` — poprawiony tam samo.

Gotowe: `rozporzadzenie-audyt-energetyczny-nowelizacja-2022-2816`,
`rozporzadzenie-ochrona-przeciwpozarowa-budynkow-nowelizacja-2024-1716`,
`rozporzadzenie-podzielniki-kosztow-ogrzewania`, `rozporzadzenie-plan-bioz`,
`rozporzadzenie-dziennik-budowy-edb`, `rozporzadzenie-audyt-energetyczny`,
`rozporzadzenie-ksiazka-obiektu-budowlanego-c-kob`,
`ustawa-prawo-budowlane-nowelizacja-2025-1847`, `ustawa-o-wlasnosci-lokali`,
`rozporzadzenie-warunki-techniczne-uzytkowania-budynkow-mieszkalnych-1999-UCHYLONE`,
`ustawa-o-charakterystyce-energetycznej-budynkow`, `ustawa-o-spoldzielniach-mieszkaniowych`,
`ustawa-o-ochronie-praw-lokatorow`, `ustawa-o-zbiorowym-zaopatrzeniu-w-wode-i-odprowadzaniu-sciekow`,
`rozporzadzenie-ochrona-przeciwpozarowa-budynkow`,
`rozporzadzenie-kontrola-metrologiczna-przyrzadow-pomiarowych`,
`ustawa-o-dozorze-technicznym`, `ustawa-o-ochronie-przeciwpozarowej`, `ustawa-prawo-o-miarach`,
`rozporzadzenie-dozor-techniczny-dzwigi-utb`, `ustawa-o-ochronie-danych-osobowych`,
`ustawa-o-wspieraniu-termomodernizacji-i-remontow-oraz-ceeb`,
`ustawa-o-utrzymaniu-czystosci-i-porzadku-w-gminach`, `rozporzadzenie-bhp-roboty-budowlane`
(24 z 36).

Ta paczka (batch 6) wymusiła większą przebudowę `toc_and_links.py`, po tym jak audyt
znalazł dwa kolejne fałszywe trafienia obu wymagające tego samego mechanizmu: „ustawy
uchylanej w art. N” (jak „zmienianej”, ale dla aktu uchylanego) oraz „rozporządzenia, o
którym mowa w § N” — fraza wskazująca inny akt pośrednio, przez numer jednostki W TYM
dokumencie, gdzie jest on nazwany. W obu przypadkach numer WEWNĄTRZ frazy zostaje
własnym linkiem (to naprawdę jednostka tego dokumentu), a wszystko INNE w tej samej
klauzuli przed frazą jest obce — dokładnie ten sam problem co przy „zmienianej”, więc
zunifikowane w jedną funkcję (`is_foreign_via_exempting_phrase`). Przy okazji znalezione i
naprawione:
- literówka w dopasowaniu odmiany „który” (kod próbował „które” + opcjonalne „j”/„m”, ale
  „którym” to inny temat fleksyjny niż „której” — nie „które” + „m” — więc dopasowanie
  nigdy nie trafiało);
- błąd kolejności działań: `link_references` uruchamiał trzy kolejne `.sub()` (Art./§,
  Rozdział/Dział, Załącznik), z których każdy mutował tekst przed kolejnym — więc gdy
  wcześniejszy .sub() już zamienił frazę wyłączającą na link, kolejny .sub() nie widział
  już zwykłego tekstu, którego szukał. Przepisane na jedno przejście: wszystkie dopasowania
  zbierane względem ORYGINALNEGO tekstu, decyzje podjęte, dopiero potem złożone w jeden
  wynik;
- zbyt szerokie okno wyszukiwania frazy wyłączającej (odziedziczone po ogólnym sprawdzeniu
  „obcości”) potrafiło złapać frazę z zupełnie innej, niepowiązanej klauzuli dalej w
  zdaniu (np. „art. 38 ust. 1, jego funkcje sprawuje ... powołany w trybie ustawy, o
  której mowa w art. 69 ust. 1” — fraza przy „art. 69” fałszywie odbierała link
  poprawnemu, wcześniejszemu „art. 38”). Zawężone do 60 znaków (frazy wyłączające
  przylegają bezpośrednio do jednostki, której dotyczą, w odróżnieniu od cytowania z datą,
  które może być oddalone o „pkt X lit. Y”).
Zweryfikowane pełną regresją: wszystkie 19 wcześniej zatwierdzonych plików odtworzone
identycznie po rozpakowaniu istniejących linków i ponownym przepuszczeniu przez
naprawiony `link_references`.

Ta paczka (batch 5) dodała jeszcze jeden wzorzec obcego aktu do `toc_and_links.py`: akty UE
bywają cytowane numerem rok/pozycja zamiast polskiej daty — „rozporządzenia 2016/679”
(RODO), „rozporządzenia (UE) 2016/679” — znaleziony na `art. 15`/`art. 30 rozporządzenia
2016/679` w `ustawa-o-ochronie-przeciwpozarowej`, które bez tej reguły linkowały błędnie do
własnych Art. 15/30. Sprawdzone na wszystkich 14 wcześniej zatwierdzonych plikach — wzorzec
nigdzie indziej nie występuje.

Od tego miejsca (batch 7+) przetwarzanie idzie bez przerw seriami po 3, na wyraźną prośbę —
całość pozostałych plików robiona jest hurtowo, z tym samym rygorem audytu co dotychczas
(dry-run → sprawdzenie martwych linków/duplikatów kotwic → dwukierunkowy audyt fałszywych
trafień → pełna regresja na wszystkich wcześniej zatwierdzonych plikach → dopiero
zastosowanie), ale bez zatrzymywania się na przegląd po każdej trójce.

**RODO (`rodo-rozporzadzenie-2016-679`) wymagało dwóch realnych poprawek w
`toc_and_links.py`:**
- RODO używa innej terminologii niż akty ISAP: „Artykuł N” zamiast „Art. N”, „Sekcja N”
  zamiast „Oddział N” (ROZDZIAŁY numerowane rzymsko, wielką literą) — dodane do
  `UNIT_PATTERNS`. Treść odwołań w tekście nadal używa skróconego „art. N”, więc `REF_RE`
  nie wymagał zmiany.
- RODO ma już własne kotwice `<a id="sekcja-N">` (z jednorazowego skryptu konwertującego,
  poza pipeline'em `html_to_md.py` — inny prefiks niż zwykle, `artykul-N`/`rozdzial-N` rzymskie/
  `sekcja-N`, ale wewnętrznie spójny), lecz numeracja „Sekcja 1”–„Sekcja 5” zaczyna się od
  nowa w każdym Rozdziale, więc te same kotwice powtarzają się 2–4 razy w całym dokumencie —
  autentyczny błąd formatowania w źródle, nie coś wprowadzonego przez ten skrypt. Bez
  naprawy TOC linkowałby zawsze do PIERWSZEGO wystąpienia danej „Sekcji N”. `dedupe_anchors`
  deduplikuje teraz też kotwice jawne (`<a id>`), nie tylko obliczane — a nowa funkcja
  `apply_anchors` (dawniej `add_missing_anchors`) przy okazji nadpisuje istniejącą linię
  `<a id="stara-wartość">` na nową, zdeduplikowaną wartość, gdziekolwiek dedup ją zmienił.

**Odkryty przy okazji, głębszy błąd kolejności działań w `toc_and_links.py` (dotyczył
WSZYSTKICH plików z PDF, nie tylko RODO, ale ujawnił się dopiero na `ustawa-prawo-spoldzielcze`,
gdzie Rozdział 1/2/3... powtarza się w kilku różnych Działach):** `dedupe_anchors` był
wywoływany na wartościach `h.anchor` sprzed przydzielenia ostatecznej kotwicy w konwencji
prefiks-numer (`add_missing_anchors` nadpisywał `h.anchor` PO deduplikacji, więc każda
zmiana wprowadzona przez dedup i tak przepadała). Efekt: pliki z PDF, w których np. „Rozdział
1” pojawia się w kilku Działach, dostawały tę samą kotwicę `rozdzial-1` za każdym razem —
TOC i pierwsze wystąpienie w treści wskazywały poprawnie, ale wszystkie kolejne odnośniki do
„Rozdziału 1” (z innego Działu) i tak trafiały do pierwszego. Naprawione przez rozdzielenie
na dwa kroki: `compute_anchors` (przydziela ostateczną wartość kotwicy KAŻDEMU nagłówkowi,
potem dopiero deduplikuje) i `apply_anchors` (dopiero wtedy mutuje linie pliku — wstawia
brakujące `<a id>` i nadpisuje te, które dedup zmienił). Zweryfikowane pełną regresją na
wszystkich 25 wcześniej zatwierdzonych plikach (odtworzone identycznie) oraz ręcznie na
`ustawa-prawo-spoldzielcze` (kotwice `rozdzial-2`, `rozdzial-2-1` itd. — już bez duplikatów).

**Drugi błąd znaleziony w tej paczce:** wzorzec rozpoznający cytowanie aktu UE numerem
rok/pozycja (dodany w batch 5) zakładał tylko kolejność „rok/numer” (np. „2016/679”) — ale
starsze akty UE (sprzed 2015) numerują odwrotnie, numer/rok („rozporządzenia (UE) nr
182/2011”), co w RODO (art. 93) linkowało błędnie własne „art. 5”/„art. 8” do artykułów tego
samego numeru w RODO, mimo że w rzeczywistości odnoszą się do zupełnie innego aktu (komitologia,
nr 182/2011). Naprawione: wzorzec dopuszcza teraz obie kolejności cyfr.

Gotowe dodatkowo: `rodo-rozporzadzenie-2016-679`, `ustawa-prawo-spoldzielcze`,
`ustawa-o-zbiorowym-zaopatrzeniu-w-wode-nowelizacja-2026-605`,
`rozporzadzenie-ogolne-przepisy-bhp`, `ustawa-o-dozorze-technicznym-nowelizacja-2026-252`,
`rozporzadzenie-warunki-techniczne-budynkow-i-usytuowanie-2002-UCHYLONE` (30 z 36).
