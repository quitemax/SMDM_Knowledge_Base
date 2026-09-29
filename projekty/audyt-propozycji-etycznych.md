# Audyt pakietu dokumentów etycznych (projekty robocze)

> Ocena siedmiu projektów roboczych z katalogu [`projekty/`](.) w
> kontekście obowiązującego statutu i regulaminów SM „Doły-Marysińska"
> (patrz baza w tym repozytorium). To analiza merytoryczna i strukturalna
> — **nie zastępuje weryfikacji przez radcę prawnego**, o którą proszą
> same dokumenty.

## Status poprawek (po drugiej turze)

Punkty **1.1, 1.2, 1.3** oraz uwaga o „skrojeniu pod jedną osobę"
(sekcja wstępna + dok. 01 § 6) zostały **wprowadzone bezpośrednio do
plików w [`projekty/md/`](md/)**, które od teraz różnią się od
oryginalnych `.docx`:
- **1.1 (tryb przyjęcia)** — dok. 01 § 15 zawiera teraz konkretną
  propozycję (Walne Zgromadzenie dla całości, z wariantem alternatywnym);
  dok. 02, 03, 04, 05, 06, 07 dostały wskazanie propozycji trybu
  (uchwała RN na podstawie § 49 ust. 1 pkt 21 Statutu).
- **1.2 (ustawa o sygnalistach)** — dok. 03 uzupełniony o realne
  wymogi ustawy z 14.06.2024 r. (Dz. U. 2024 poz. 928): próg 50
  zatrudnionych (art. 23), potwierdzenie przyjęcia w 7 dni i informacja
  zwrotna w 3 miesiące (art. 25 ust. 1 pkt 5 i 7), zgłoszenie ustne na
  żądanie w ciągu 14 dni (art. 26 ust. 6), prawo do zgłoszenia
  zewnętrznego do RPO niezależnie od trybu wewnętrznego (art. 30 ust.
  1–2). Ustawa nie jest jeszcze skonwertowana do `przepisy-prawne/` —
  wskazane w dokumencie jako zadanie do zrobienia osobno.
- **1.3 (regulamin zakupowy)** — dok. 06 dostał jawną klauzulę
  podporządkowania istniejącemu regulaminowi wyboru wykonawców
  (progi, tryby, Komisja Przetargowa rozstrzyga tamten dokument).
- **Obiektywność (dot. dok. 01 § 6)** — przepisano tak, by dotyczył
  jednolicie każdej dziedziny wiedzy specjalistycznej w Radzie
  (budownictwo, finanse, prawo, IT, zarządzanie nieruchomościami), nie
  tylko IT — usunięto wrażenie regulacji pod jedną, konkretną sytuację.

**Nadal otwarte** (świadomie nie ruszane w tej turze — patrz reszta
tego dokumentu): 1.4, 1.5, oraz wszystkie uwagi szczegółowe do
poszczególnych dokumentów w sekcji 2.

## Status poprawek (trzecia tura — świeży przegląd Kodeksu)

Przy ponownym, niezależnym przeczytaniu dok. 01 (bez opierania się na
poprzedniej ocenie) znalazłem cztery dodatkowe, konkretne problemy —
wszystkie już poprawione w [`md/01_...md`](md/01_Kodeks_odpowiedzialnego_sprawowania_mandatu.md):

1. **§ 4 ust. 3 zakładał nieistniejący mechanizm.** Kodeks odsyła do
   „zdania odrębnego na zasadach określonych w regulaminie organu" —
   sprawdziłem oba regulaminy: **Regulamin Zarządu** rzeczywiście
   przewiduje zdanie odrębne w protokole, ale **Regulamin Rady
   Nadzorczej — wcale**. Dla Rady ten przepis Kodeksu odsyłał donikąd.
   Oznaczone wprost, z rekomendacją uzupełnienia Regulaminu RN.
2. **§ 4 ust. 4 „sabotowanie" nie miało definicji.** Niezdefiniowany,
   emocjonalnie nacechowany termin w dokumencie mającym *zapobiegać*
   konfliktom to ryzyko — może sam stać się przedmiotem sporu o to, co
   nim jest. Zastąpione konkretnym katalogiem zachowań.
3. **§ 13 był całkowicie abstrakcyjny w kwestii konsekwencji.** Nie
   wskazywał żadnego realnego środka. Doprecyzowano: odwołanie z
   Zarządu przez RN (Statut § 55 ust. 2) i odwołanie z Rady przez WZ
   (Statut § 48) to already-existing, konkretne środki — nazwane wprost,
   razem z uwagą, że nie ma dziś żadnej sankcji „pośredniej" między
   brakiem reakcji a pełnym odwołaniem.
4. **Brak zasady nieretroakcji.** Dokument w kilku miejscach wyraźnie
   nawiązuje do niedawnych wydarzeń (patrz uwaga o „skrojeniu pod jedną
   osobę" wyżej) — bez jawnej zasady, że Kodeks ocenia zachowania od
   dnia wejścia w życie, mógłby być odczytany jako próba wstecznego
   rozliczenia. Dodano wprost w § 15.

Dodatkowo: § 8 dostał odesłanie do
[`../struktura-organizacyjna/ochrona-danych-osobowych.md`](../struktura-organizacyjna/ochrona-danych-osobowych.md).

**Pozostałych 6 dokumentów nie przeglądałem ponownie w tej turze** —
jeśli chcesz, mogę zrobić to samo świeże spojrzenie na każdy z nich.

## Status: ustawa o ochronie sygnalistów — teraz w pełni wdrożona do bazy

**Zaktualizowane.** Ustawa (Dz.U. 2024 poz. 928) przeszła pełny proces
konwersji identyczny jak pozostałe ~40 aktów: PDF i HTML pobrane z
`api.sejm.gov.pl`, skonwertowane skryptami `html_to_md.py` +
`toc_and_links.py` do
[`przepisy-prawne/md/ustawa-o-ochronie-sygnalistow.md`](../przepisy-prawne/md/ustawa-o-ochronie-sygnalistow.md)
(spis treści + kotwice + linkowanie wewnętrznych odniesień), wpisana do
`przepisy-prawne/README.md` (kategoria 11, nowa) i
`zrodla/przepisy-prawne-zewnetrzne.md`. Wszystkie cytaty w dok. 03
zamienione na prawdziwe linki do konkretnych artykułów.

Pełny tekst ujawnił dwa dodatkowe wymogi, których doraźna weryfikacja
nie złapała — oba już dopisane do dok. 03:
- **Konsultacje przed ustanowieniem procedury** — ustawa wymaga
  konsultacji ze związkiem zawodowym (5–10 dni) przed ustaleniem
  procedury, a ta wchodzi w życie dopiero 7 dni po ogłoszeniu (art. 24
  ust. 3–5). To dotyczy więc też Związku Zawodowego „Budowlani" i
  powinno wejść do trybu przyjęcia w § 15 Kodeksu, nie tylko do tego
  dokumentu.
- **Dokładna zawartość rejestru zgłoszeń** i okres przechowywania
  danych (3 lata po zakończeniu sprawy) — art. 29.

## Co zostało ocenione

1. `01_Kodeks_odpowiedzialnego_sprawowania_mandatu`
2. `02_Polityka_konfliktu_interesow`
3. `03_Procedura_zglaszania_nieprawidlowosci`
4. `04_Procedura_skarg_i_wnioskow`
5. `05_Standard_podejmowania_i_dokumentowania_decyzji`
6. `06_Standard_zakupow_i_zarzadzania_dostawcami`
7. `07_Standard_IT_danych_i_technologii`

Wersje Markdown — [`projekty/md/`](md/).

---

## 1. Ocena ogólna (dotyczy całego pakietu)

**Jakość drafterska jest wysoka.** Spójna struktura, konsekwentne
odsyłacze między dokumentami (np. Standard zakupów → Polityka konfliktu
interesów; Kodeks → Standard decyzji), realistyczny, niekazuistyczny
język. Dokumenty poprawnie **nie tworzą nowych kompetencji** (Kodeks
§ 1 ust. 2, Preambuła: „Kodeks nie zmienia kompetencji organów i nie
tworzy nowych uprawnień") — to ważne zabezpieczenie przed zarzutem
działania *ultra vires* wobec statutu.

Widać też wyraźnie, że pakiet powstał jako **odpowiedź na konkretny,
niedawny kryzys zarządczy** SMDM (spór o obsadę Zarządu, rola
technicznego eksperta w Radzie, spór o dostęp do systemów IT, zmiana
statutu z 29.06.2026 r. dot. składu Zarządu 2–3 osoby). To nie jest
zarzut — dobre regulacje często powstają jako reakcja na realny
incydent — ale trzeba mieć świadomość, że tak mocno „skrojony pod
sytuację" dokument może być odebrany przez pozostałych interesariuszy
(np. inną frakcję w Radzie) jako próba usankcjonowania jednej strony
sporu, nie jako neutralna reforma. Warto to zaadresować wprost przy
prezentowaniu pakietu — np. wskazać, że przegląd jest reakcją na
doświadczenia całej kadencji, a nie na jedno zdarzenie.

### 1.1. Brak mechanizmu przyjęcia — realne ryzyko prawne

Żaden z 7 dokumentów nie rozstrzyga, **który organ go przyjmuje**.
Kodeks (§ 15 ust. 1) świadomie to odkłada („po weryfikacji prawnej") —
to dobrze, że jest to nazwane wprost, ale bez odpowiedzi te dokumenty
zawisną. Z analizy statutu:

- [Statut § 49 ust. 1 pkt 21](../zrodla/md/statut.md#par-49) daje
  Radzie Nadzorczej prawo uchwalania „regulaminów nie zastrzeżonych do
  kompetencji innych organów" — to najbardziej prawdopodobna podstawa
  dla dokumentów 2–7 (polityki wykonawcze, nie dotyczą WZ).
- **Problem z samym Kodeksem** (dok. 1): reguluje też zachowanie
  członków Rady Nadzorczej, a [statut § 36 pkt 16](../zrodla/md/statut.md#par-36)
  zastrzega uchwalanie **regulaminu Rady Nadzorczej** dla Walnego
  Zgromadzenia. Jeśli Kodeks ma wiązać Radę na równi z jej regulaminem
  (np. § 3 „rozdział kompetencji Rady i Zarządu", § 10 „relacje z
  pracownikami" — to materia typowo regulaminowa), przyjęcie go samą
  uchwałą RN może być **podatne na zarzut obejścia kompetencji WZ**.
  Bezpieczniejsze warianty: (a) Kodeks przyjmuje WZ razem ze zmianą
  Regulaminu Rady Nadzorczej, albo (b) Kodeks jest formalnie
  „samoograniczeniem" przyjętym przez RN i Zarząd każde dla siebie,
  wyraźnie podporządkowanym istniejącym regulaminom (a nie odwrotnie).
  To pytanie do radcy prawnego, ale warto je zadać wprost, nie zostawiać
  cichcem.
- Nie ma też wzmianki, że dawny **„Kodeks Etyki Organów Spółdzielni"**
  (o którym mowa w adnotacji dok. 1: „projekt powstał przez przebudowę
  pierwotnego Kodeksu Etyki Organów Spółdzielni") jest w tej bazie
  wiedzy nieobecny — nie mogłem zweryfikować, czy nowy dokument
  faktycznie zastępuje stary w całości, czy zostawia luki. Jeśli stary
  Kodeks był formalnie uchwalony (przez RN albo WZ), **jego uchylenie
  wymaga tego samego trybu**, którym został przyjęty — to też do
  ustalenia przed przyjęciem nowego pakietu.

### 1.2. Luka w podstawie prawnej: ustawa o ochronie sygnalistów

**To najpoważniejsza luka merytoryczna całego pakietu.** Dokument 3
(„Procedura zgłaszania nieprawidłowości") to w praktyce wewnętrzny
kanał zgłaszania naruszeń — a Polska ma od 2024 r. **ustawę o ochronie
osób zgłaszających naruszenia prawa** (wdrażającą dyrektywę UE
2019/1937), która dla podmiotów zatrudniających **co najmniej 50
pracowników** nakłada konkretne, obowiązkowe wymogi: m.in. terminy na
potwierdzenie przyjęcia zgłoszenia (7 dni) i przekazanie informacji
zwrotnej (do 3 miesięcy), obowiązek umożliwienia zgłoszenia ustnego na
żądanie, zakaz działań odwetowych z konkretnym katalogiem sankcji, oraz
równoległe **zewnętrzne** kanały zgłaszania (do Rzecznika Praw
Obywatelskich / właściwych organów) niezależne od kanału wewnętrznego.

**Ta ustawa nie jest jeszcze w bazie źródeł prawnych tego repozytorium
— sprawdziłem, nie ma jej wcale.** Dokument 3 w obecnej formie (§ 2:
„zgłoszenia w dobrej wierze są chronione przed odwetem") odtwarza
*ducha* tej ustawy własnymi słowami, ale nie spełnia z pewnością jej
formalnych wymogów proceduralnych (numeracja zgłoszeń jest, terminy
proceduralne — nie ma). **Zanim ten dokument zostanie przyjęty, trzeba
ustalić: (a) czy SMDM przekracza próg 50 zatrudnionych (jeśli tak, ta
ustawa obowiązuje niezależnie od tego, czy Spółdzielnia przyjmie
własną procedurę), i (b) dostosować § 3–7 do jej konkretnych wymogów
proceduralnych.** To jest coś, co mogę dociągnąć w tej bazie wiedzy
(pobrać i przeanalizować tę ustawę), jeśli chcesz — dotąd nie było
powodu jej pobierać, bo żaden istniejący regulamin SMDM jej nie
przywoływał.

### 1.3. Rozjazd z już istniejącym, uchwalonym regulaminem zakupowym

Dokument 6 („Standard zakupów i zarządzania dostawcami") opisuje
zasady zakupowe (uczciwa konkurencja, kryteria przed oceną ofert,
koszt cyklu życia, ujawnianie konfliktu interesów) **nie odwołując się
ani razu** do już obowiązującego, uchwalonego przez Radę Nadzorczą
[regulaminu wyboru wykonawców robót, dostaw i usług](../zrodla/md/regulamin-wyboru-wykonawcow-robot-dostaw-i-uslug.md)
(uchwała nr 62/R/26) — patrz opis w
[`administracja-techniczna/procedura-przetargowa.md`](../administracja-techniczna/procedura-przetargowa.md).
Ten regulamin ma już konkretne, wiążące progi (5 000 zł / 50 000 zł),
tryby (przetarg / zapytanie o cenę / wolna ręka) i role (Komisja
Przetargowa, Dział Techniczny, Zarząd). Dokument 6 operuje na wyższym
poziomie ogólności („uczciwa konkurencja, gdy charakter zakupu na to
pozwala") i **nigdzie nie precyzuje relacji do tego regulaminu** — w
razie sprzeczności (np. co „całkowity koszt cyklu życia" oznacza dla
zamówienia poniżej progu zapytania o cenę) nie wiadomo, który dokument
ma pierwszeństwo. Rekomendacja: dodać jawne zdanie w § 1, że Standard
**uzupełnia** (nie zastępuje) istniejący regulamin zakupowy, i
wskazać wprost, że progi kwotowe i tryby pozostają regulowane tamtym
dokumentem.

### 1.4. Niejasna granica między dok. 3 i dok. 4

„Procedura zgłaszania nieprawidłowości" (dok. 3, dot. naruszeń prawa/
Kodeksu przez organy) i „Procedura skarg i wniosków" (dok. 4, dot.
skarg członków na działanie Spółdzielni) mają wspólny obszar: co jeśli
skarga członka (tryb dok. 4) w istocie zarzuca konkretnemu członkowi
Rady/Zarządu naruszenie (tryb dok. 3)? Żaden z dokumentów nie mówi, kto
i na jakim etapie decyduje, którym trybem sprawa idzie dalej. Warto
dodać jedno zdanie w obu dokumentach wskazujące punkt przekierowania
(np. „jeśli skarga wskazuje możliwe naruszenie przez członka organu,
osoba przyjmująca kieruje sprawę do trybu z Procedury zgłaszania
nieprawidłowości").

### 1.5. Otwarte pola [●] — priorytetyzacja

Wszystkie dokumenty poprawnie oznaczają miejsca wymagające decyzji
jako `[●]`, zamiast zgadywać — to dobra praktyka. Najważniejsze do
rozstrzygnięcia przed przyjęciem (bo są strukturalnie trudne, nie tylko
kosmetyczne):

- **Dok. 3 § 3 ust. 3**: kanał zgłoszeń, gdy zarzut dotyczy **całego**
  Zarządu lub **całej** Rady jednocześnie — statutowo jedynym organem
  „nad" obydwoma jest Walne Zgromadzenie. Dokument nie proponuje
  żadnego rozwiązania (np. niezależny prawnik zewnętrzny, komisja
  rewizyjna związku rewizyjnego przy najbliższej lustracji) — to realna
  luka, nie tylko brakująca liczba.
- **Dok. 2 § 3 ust. 3**: kto prowadzi rejestr oświadczeń o konflikcie
  interesów — naturalnie PM (ds. organizacyjno-samorządowych, już
  prowadzi rejestr uchwał/członków), ale trzeba to wskazać wprost i
  dopisać do zakresu obowiązków tego stanowiska.
- **Dok. 4 § 3 ust. 5**: termin odpowiedzi na skargę — statut
  ([§ 26](../zrodla/md/statut.md#par-26)) już ustanawia **1 miesiąc**
  na rozpatrzenie wniosków członków skierowanych do Zarządu — ten
  termin powinien się z tym pokrywać, nie zostać ustalony od nowa
  niezależnie.

## 2. Uwagi do poszczególnych dokumentów

### 01 — Kodeks odpowiedzialnego sprawowania mandatu

- **Mocna strona**: § 3 („Rada pyta «czy/dlaczego/jakie ryzyka», Zarząd
  odpowiada za «jak»") i § 6 (ekspertyza w Radzie bez przejmowania roli
  wykonawczej) trafnie i precyzyjnie oddają granicę nadzór/zarząd, którą
  już wyznacza statut (§ 49 vs. § 54), i przekładają ją na praktyczne
  reguły, których w statucie nie ma. To realna wartość dodana.
- **Ryzyko**: § 6 i załącznik (tabela „dobre/złe działanie") są bardzo
  szczegółowo dopasowane do scenariusza „ekspert techniczny w Radzie
  vs. dostęp do systemów IT" — czytelnik spoza tego kontekstu może nie
  rozumieć, skąd ta szczegółowość, a przy sporze dokument może być
  odczytany jako napisany pod konkretną osobę/sytuację. Rozważ krótkie
  zdanie wprowadzające kontekst (np. „doświadczenia poprzednich
  kadencji pokazały potrzebę doprecyzowania roli eksperckiej w Radzie"),
  żeby nie wyglądało na regulację *ad hominem*.
- **Do sprawdzenia**: § 4 ust. 4 („po prawidłowym podjęciu decyzji
  członek nie powinien podejmować działań mających na celu jej
  sabotowanie") — to rozsądna zasada kolegialności, ale zestawiona z
  niedawną historią Spółdzielni (upubliczniony spór o obsadę Zarządu)
  może wymagać doprecyzowania, gdzie kończy się „sabotaż" a zaczyna
  legalne wykonywanie uprawnień mniejszości (np. zaskarżenie uchwały do
  sądu — to wprost dopuszczone w zdaniu drugim, dobrze, że jest
  zastrzeżone).
- **Do sprawdzenia**: § 13 (naruszenia Kodeksu) słusznie nie wymyśla
  nowych sankcji — ale zestawiony z moim wcześniejszym ustaleniem, że
  **statutowa podstawa ogólnego „wykluczenia" członka (§ 18–24 statutu)
  jest dziś skreślona** (patrz
  [`czynsze-ksiegowosc/procedura-windykacyjna.md#wykluczenie`](../czynsze-ksiegowosc/procedura-windykacyjna.md#wykluczenie)),
  jedyną realną konsekwencją naruszenia Kodeksu przez członka Rady jest
  **odwołanie z Rady przez WZ** (co innego niż „wykluczenie ze
  Spółdzielni"). Warto to rozróżnienie nazwać wprost w § 13, żeby nikt
  nie oczekiwał sankcji, której statut dziś nie przewiduje.

### 02 — Polityka konfliktu interesów

- Solidny, kompletny dokument — typologia konfliktu (rzeczywisty/
  potencjalny/postrzegany) jest precyzyjna i przydatna praktycznie.
- **Luka**: § 5 ust. 2 („drobne materiały promocyjne... próg wartości
  [●]") — brak nawet orientacyjnej wartości czyni ten przepis
  martwym do czasu uchwały. Warto zaproponować punkt odniesienia (np.
  wartości z Kodeksu cywilnego dot. zwyczajowych podarunków, albo po
  prostu kwotę ustaloną uchwałą RN razem z przyjęciem dokumentu, nie
  później).
- **Do doprecyzowania**: § 4 ust. 4 („w razie wątpliwości o wyłączeniu
  decyduje właściwy organ bez udziału zainteresowanego") — nie mówi, co
  się dzieje przy remisie głosów po wyłączeniu zainteresowanego
  (realne przy nieparzystym normalnie składzie Rady, który przy
  wyłączeniu jednej osoby może stać się parzysty).

### 03 — Procedura zgłaszania nieprawidłowości

- Zobacz **1.2 wyżej** — to najpoważniejszy punkt całego audytu:
  brak odniesienia do ustawy o ochronie sygnalistów.
- § 4 ust. 3 i § 5 ust. 2 (zabezpieczenie dowodów przed kontaktem z
  osobą, której dotyczy zgłoszenie; możliwość nieinformowania jej z
  góry) są dobrze przemyślane proceduralnie — to nie jest amatorski
  dokument.
- **Luka**: brak jakiegokolwiek terminu — ani na wstępną ocenę (§ 4), ani
  na zakończenie postępowania wyjaśniającego (§ 5–6). Sama ustawa o
  sygnalistach narzuca tu konkretne terminy (patrz 1.2) — nawet bez
  niej, dokument bez żadnego terminu jest trudny do wyegzekwowania.

### 04 — Procedura skarg i wniosków

- Krótki, praktyczny, dobrze domyka temat „uporczywego/agresywnego
  skarżącego" (§ 5) — realny problem operacyjny, rzadko regulowany.
- **Luka**: § 3 ust. 5 zostawia termin odpowiedzi jako `[●]`, mimo że
  — jak wyżej (1.5) — statut już określa **1 miesiąc** dla wniosków do
  Zarządu (§ 26). To nie „do ustalenia od zera", tylko do zgrania z
  istniejącym przepisem.
- **Do doprecyzowania**: § 4 ust. 3 („skargi dotyczące całego organu
  wymagają wskazania niezależnego trybu [●]") — ten sam problem
  strukturalny co w dok. 3 § 3 ust. 3 (patrz 1.5) — oba dokumenty
  powinny mieć **spójną** odpowiedź na to samo pytanie („co gdy zarzut
  dotyczy całej Rady/całego Zarządu"), a nie dwie osobne, potencjalnie
  rozbieżne.

### 05 — Standard podejmowania i dokumentowania decyzji

- Dobry, uniwersalny szkielet („karta decyzji") — realnie użyteczny
  jako narzędzie, nie tylko deklaracja.
- **Uwaga**: § 2 („kiedy stosować") jest celowo szeroki i nieostry
  („istotne inwestycje... decyzje o znaczącym wpływie na członków") —
  to typowe dla tego typu standardu, ale oznacza, że w praktyce
  Zarząd/Rada same będą musiały wypracować próg „istotności". Warto
  rozważyć chociaż przykładowy próg kwotowy powiązany z już istniejącymi
  progami z regulaminu zakupowego (5 000/50 000 zł) — inaczej „Karta
  decyzji" może być pomijana jako zbyt pracochłonna dla spraw średniej
  wagi.
- Brak odniesienia do tego, **kto przechowuje** karty decyzji i jak
  długo — przy pozostałych dokumentach SMDM archiwizacja jest zwykle
  precyzyjnie określona (np. protokoły WZ — 10 lat, statut § 37 ust. 6).
  Warto dodać analogiczny przepis.

### 06 — Standard zakupów i zarządzania dostawcami

- Zobacz **1.3 wyżej** — główny problem to brak jawnego podporządkowania
  istniejącemu regulaminowi zakupowemu.
- § 6 (vendor lock-in) i § 5 ust. 2 (przegląd istotnych aneksów) to
  dojrzałe, rzadko spotykane w regulaminach spółdzielczych zapisy —
  bezpośrednio odpowiadają na ryzyko opisane też w
  [`administracja-techniczna/procedura-przetargowa.md`](../administracja-techniczna/procedura-przetargowa.md)
  (regulamin zakupowy obejmuje też dostawy/usługi IT, ale nikt nie jest
  formalnie wyznaczony jako właściciel tych zakupów — patrz
  `it-systemy/`). Ten dokument częściowo wypełnia tę lukę merytorycznie,
  ale nie organizacyjnie (nadal nie mówi, **kto** to robi).

### 07 — Standard IT, danych i technologii

- Bardzo mocno powiązany z dok. 1 § 6 (ekspertyza w Radzie) — razem
  tworzą spójną politykę „nadzór bez przejmowania operacji", co jest
  wartościowe i rzadkie w regulaminach spółdzielni mieszkaniowych.
- § 7 (sztuczna inteligencja) jest zaskakująco konkretny jak na dokument
  spółdzielni mieszkaniowej — to dobrze (temat realny, np. przy
  korespondencji z mieszkańcami czy analizie dokumentów), ale wymaga
  wskazania, kto ocenia „zatwierdzone usługi AI" (§ 7 ust. 1) — bez
  tego przepis jest niewykonalny (nikt nie wie, co jest „zatwierdzone").
- **Uwaga strukturalna**: ten dokument w praktyce ustanawia zasady IT
  governance, ale — jak zaznaczono w jego własnym nagłówku — „nie
  zastępuje instrukcji bezpieczeństwa, polityk ochrony danych ani
  procedur administratora systemów", których **w tej bazie wiedzy
  praktycznie nie ma** (`it-systemy/` to w większości DO UZUPEŁNIENIA —
  patrz [`it-systemy/README.md`](../it-systemy/README.md)). Standard
  wysokiego poziomu bez żadnych dokumentów wykonawczych pod spodem
  ryzykuje pozostaniem deklaracją.
- Dobrze koresponduje z już opisanym w tej bazie obowiązkiem RODO —
  patrz [`struktura-organizacyjna/ochrona-danych-osobowych.md`](../struktura-organizacyjna/ochrona-danych-osobowych.md)
  (w tym otwarte pytanie o obowiązek wyznaczenia IOD przy monitoringu
  wizyjnym — § 6 tego Standardu mógłby się do tego wprost odwołać).

## 3. Lista priorytetowa przed przyjęciem

1. **Sprawdzić próg zatrudnienia i dostosować dok. 3 do ustawy o
   ochronie sygnalistów** (1.2) — jedyny punkt z realnym ryzykiem
   niezgodności z bezwzględnie obowiązującym prawem.
2. **Ustalić tryb przyjęcia**, w szczególności dla Kodeksu wobec
   Regulaminu Rady Nadzorczej (1.1).
3. **Zharmonizować odpowiedź na „co gdy zarzut dotyczy całego organu"**
   między dok. 3 i dok. 4 (1.5, 2.4).
4. **Dopisać jawną relację dok. 6 do istniejącego regulaminu
   zakupowego** (1.3).
5. Rozstrzygnąć pozostałe `[●]` — większość to proste decyzje uchwałą,
   ale powyższe cztery są strukturalne i wymagają przemyślenia, nie
   tylko wypełnienia liczby.

---

**Metodologia**: ocena na podstawie treści 7 plików `.docx`
przekonwertowanych do Markdown ([`projekty/md/`](md/)) oraz
porównania z obowiązującym statutem i regulaminami SMDM już
udokumentowanymi w tym repozytorium. Nie konsultowano radcy prawnego —
to zastrzeżenie, o które proszą same dokumenty, pozostaje aktualne.
