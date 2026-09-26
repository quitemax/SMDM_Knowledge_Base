# Baza wiedzy SM „Doły-Marysińska”

Repozytorium służy jako baza wiedzy o strukturze organizacyjnej i procesach
Spółdzielni Mieszkaniowej „Doły-Marysińska” w Łodzi. Ma odpowiadać na
pytania typu: kto za co odpowiada, jak przebiega dany proces, do kogo się
zwrócić, co zrobić w danej sytuacji — zarówno dla pracowników, jak i (część
treści) dla mieszkańców.

Na razie w formie plików Markdown w tym repozytorium — jeśli z czasem
okaże się to niewystarczające (wygoda edycji, wyszukiwanie, prawa dostępu),
można rozważyć migrację do dedykowanego narzędzia (np. BookStack).

## Struktura

- [`struktura-organizacyjna/`](struktura-organizacyjna/) — kto jest kim,
  komu podlega, jakie stanowiska istnieją, mapa zastępowalności, podział
  terenowy.
- [`zarzad/`](zarzad/) — procesy zarządcze, decyzje, uchwały, sprawy
  statutowe.
- [`administracja-techniczna/`](administracja-techniczna/) — procesy
  związane z budynkami, przeglądami, zgłoszeniami, przetargami.
- [`czynsze-ksiegowosc/`](czynsze-ksiegowosc/) — procesy finansowe:
  czynsze, fundusz remontowy, windykacja, faktury.
- [`kadry/`](kadry/) — procesy pracownicze: onboarding, offboarding,
  wynagrodzenia.
- [`it-systemy/`](it-systemy/) — dokumentacja techniczna systemów
  używanych w spółdzielni.
- [`procedury-mieszkancow/`](procedury-mieszkancow/) — czego mieszkaniec
  może się spodziewać, jak zgłasza sprawy (do wykorzystania też przy
  komunikacji zewnętrznej).
- [`zrodla/`](zrodla/) — oryginalne regulaminy i statut (PDF) oraz ich
  wersje przekonwertowane na Markdown, na podstawie których zbudowano
  powyższe foldery; pełna lista z opisami w
  [`zrodla/spis-dokumentow.md`](zrodla/spis-dokumentow.md). Zobacz też
  [`zrodla/przepisy-prawne-zewnetrzne.md`](zrodla/przepisy-prawne-zewnetrzne.md)
  — listę zewnętrznych ustaw i rozporządzeń wyznaczających ramy działalności
  Spółdzielni.
- [`przepisy-prawne/`](przepisy-prawne/) — pełne teksty (PDF, docelowo też
  Markdown) tych zewnętrznych aktów prawnych; patrz
  [`przepisy-prawne/README.md`](przepisy-prawne/README.md) po publikatory,
  stan prawny na dzień pobrania i interwały sprawdzania aktualizacji.

## Jak dokumentować proces

Każdy opisany proces powinien używać jednego, wspólnego szablonu — patrz
[`szablon-procesu.md`](szablon-procesu.md). Jednolity format sprawia, że
każdy proces jest tak samo łatwy do znalezienia i zrozumienia, niezależnie
od tego, kto go spisywał.

## Status wypełnienia (2026-09-25)

Pierwsza wersja tej bazy została zbudowana na podstawie rzeczywistych
regulaminów i statutu spółdzielni (patrz źródła w każdym pliku). Część
sekcji — zwłaszcza procesy czysto operacyjne, których nie opisuje żaden
regulamin (np. dokładny przebieg zgłoszenia awarii, onboarding pracownika,
mapa zastępowalności, podział terenowy między administracjami) — jest
oznaczona jako **DO UZUPEŁNIENIA**. Te fragmenty wymagają wiedzy osób
faktycznie prowadzących dany proces — nie zostały zgadnięte, żeby baza
wiedzy nie zawierała nieprawdziwych informacji.

## Dokumentacja projektu

- [`docs/historia.md`](docs/historia.md) — jak i po co powstał ten projekt.
- [`AGENTS.md`](AGENTS.md) — zasady pracy z tym repozytorium dla agentów AI.

## Zasada poufności

Ta baza wiedzy zawiera treść regulaminów i statutu — dokumentów uznanych
za dostępne publicznie (np. udostępnianych członkom spółdzielni). Opisy
stanowisk w [`struktura-organizacyjna/stanowiska-i-zakresy-obowiazkow.md`](struktura-organizacyjna/stanowiska-i-zakresy-obowiazkow.md)
są celowo napisane jako opis ROLI, nie CV konkretnej osoby — bez nazwisk,
inicjałów, wynagrodzeń czy dat konkretnych umów o pracę.
