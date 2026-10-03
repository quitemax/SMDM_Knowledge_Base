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

Treść opisowa (struktura, procesy, procedury) znajduje się w katalogu
`manual/`; poza nim są źródła, przepisy prawne, narzędzia, projekty i
dokumentacja projektu.

- [`manual/struktura-organizacyjna/`](manual/struktura-organizacyjna/README.md) — kto
  jest kim, komu podlega, jakie stanowiska istnieją, mapa
  zastępowalności, podział terenowy.
- [`manual/zarzad/`](manual/zarzad/README.md) — procesy zarządcze, decyzje, uchwały,
  sprawy statutowe.
- [`manual/rada-nadzorcza/`](manual/rada-nadzorcza/README.md) — zasady działania Rady
  Nadzorczej, podejmowanie uchwał, wybór członków Zarządu, stałe komisje
  Rady.
- [`manual/administracja-techniczna/`](manual/administracja-techniczna/README.md) —
  procesy związane z budynkami, przeglądami, zgłoszeniami, przetargami.
- [`manual/czynsze-ksiegowosc/`](manual/czynsze-ksiegowosc/README.md) — procesy
  finansowe: czynsze, fundusz remontowy, windykacja, faktury.
- [`manual/kadry/`](manual/kadry/README.md) — procesy pracownicze: onboarding,
  offboarding, wynagrodzenia.
- [`manual/it-systemy/`](manual/it-systemy/README.md) — dokumentacja techniczna
  systemów używanych w spółdzielni.
- [`manual/procedury-mieszkancow/`](manual/procedury-mieszkancow/README.md) — czego
  mieszkaniec może się spodziewać, jak zgłasza sprawy (do wykorzystania
  też przy komunikacji zewnętrznej).
- [`zrodla/`](zrodla/) — oryginalne regulaminy i statut (PDF) oraz ich
  wersje przekonwertowane na Markdown, na podstawie których zbudowano
  powyższe foldery; pełna lista z opisami w
  [`zrodla/spis-dokumentow.md`](zrodla/spis-dokumentow.md). Zobacz też
  [`zrodla/przepisy-prawne-zewnetrzne.md`](zrodla/przepisy-prawne-zewnetrzne.md)
  — listę zewnętrznych ustaw i rozporządzeń wyznaczających ramy działalności
  Spółdzielni.
- [`wzory/`](wzory/README.md) — wzory wniosków i oświadczeń do pobrania ze
  strony Spółdzielni (PDF oraz wersje Markdown).
- [`przepisy-prawne/`](przepisy-prawne/) — pełne teksty (PDF, docelowo też
  Markdown) tych zewnętrznych aktów prawnych; patrz
  [`przepisy-prawne/README.md`](przepisy-prawne/README.md) po publikatory,
  stan prawny na dzień pobrania i interwały sprawdzania aktualizacji.

## Import przez coopOS

To repozytorium jest cyklicznie importowane przez aplikację coopOS i
publikowane na stronie spółdzielni (statut, regulaminy i przepisy jako
dokumenty, `manual/` jako baza wiedzy). **Pliki md bez poprawnego front
matter nie są publikowane.** Format metadanych, odbiorców (`audience`) i
konwencje treści opisuje [`docs/kontrakt-importu.md`](docs/kontrakt-importu.md);
poprawność sprawdza `python tools/validate_front_matter.py`.

## Jak dokumentować proces

Każdy opisany proces powinien używać jednego, wspólnego szablonu — patrz
[`manual/szablon-procesu.md`](manual/szablon-procesu.md). Jednolity format sprawia, że
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
- [`docs/kontrakt-importu.md`](docs/kontrakt-importu.md) — format metadanych
  i konwencje wymagane przez import do coopOS.
- [`AGENTS.md`](AGENTS.md) — zasady pracy z tym repozytorium dla agentów AI.

## Zasada poufności

Ta baza wiedzy zawiera treść regulaminów i statutu — dokumentów uznanych
za dostępne publicznie (np. udostępnianych członkom spółdzielni). Opisy
stanowisk w [`struktura-organizacyjna/stanowiska-i-zakresy-obowiazkow.md`](manual/struktura-organizacyjna/stanowiska-i-zakresy-obowiazkow.md)
są celowo napisane jako opis ROLI, nie CV konkretnej osoby — bez nazwisk,
inicjałów, wynagrodzeń czy dat konkretnych umów o pracę.
