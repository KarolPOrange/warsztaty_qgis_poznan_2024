# Warsztaty QGiS "API z API" - Poznań 2024
## Założenia warsztatu
Praktyczne warsztaty podczas, których uczestnicy poznają metody pobierania i wizualizacji danych przestrzennych, udostępnionych
za pomocą zewnętrznego API. W ramach szkolenia zostanie stworzona od podstaw wtyczka QGiSowa, która będzie korzystać z 
ogólnodostępnych danych o jakości powietrza, udostępnionych przez Główny Inspektorat Ochrony Środowiska.
Wynikiem warsztatów zostanie w pełni funkcjonalna wtyczka, stworzona z wykorzystaniem takich technologii, jak Python, pyqgis oraz pyQt.

## Konfiguracja Środowiska
W ramach warsztatów będziemy korzystać z zintegrowanego środowiska programistycznego (IDE) PyCharm.
PyCharm jest wiodącym IDE wykorzystywanym przy dewelopmencie kodu w języku Python.
PyCharm w wersji darmowej daje możliwość prostej integracji ze środowiskiem python-a stworzonego na potrzeby QGiSa.
Dzięki integracji będziemy mieli dostęp dokumentacji bibliotek dostępnych z poziomu konsoli QGiSa.
Konfiguracja PyCharma z QGiSem następuję w następujących krokach.
1. Pobranie PyCharma (wersja Community) z oficjalnej strony: https://www.jetbrains.com/pycharm/download
2. Dodanie nowego interpreter Python w PyCharmie

![wybieranieSciezka_0](https://github.com/KarolPOrange/warsztaty_qgis_poznan_2024/assets/149786515/623604dd-5534-4d48-8394-586cdc630570)

3. Wybranie wirtualnego środowiska QGiSowego

![zrzut](https://github.com/KarolPOrange/warsztaty_qgis_poznan_2024/assets/61205666/110b415a-8ffc-451a-b3ca-73996b0408a7)

4. Po stworzniu nowego środowiska trzeba chwile poczekać na skofigurowanie się PyCharma

## Korzystanie z Interfejsu programistycznego aplikacji (API)
### Czym jest API ?
API, czyli interfejs programowania aplikacji (ang. application programming interface) to zestaw reguł umożliwiających 
przesyłanie danych między aplikacjami. Wiele serwisów sieciowych oferuje publiczne API, pozwalające każdemu na wysyłanie
i odbieranie zawartości z danego serwisu. API dostępne przez Internet przy użyciu adresów URL zaczynających się od http://
to inaczej API sieciowe. Pobieranie oraz publikowanie informacji w sieci wymaga wysłania żądania do API.
[Link do artykułu](https://support.apple.com/pl-pl/guide/shortcuts-mac/apd2e30c9d45/mac#:~:text=API%2C%20czyli%20interfejs%20programowania%20aplikacji,odbieranie%20zawarto%C5%9Bci%20z%20danego%20serwisu.)

![rest-api](https://github.com/KarolPOrange/warsztaty_qgis_poznan_2024/assets/61205666/f4b53c22-02eb-47f9-be19-8c787d011db9)


### Jakie dane oferuje Główny Inspektorat Ochrony Środowiska (GIOŚ) ?
GIOŚ umożliwia dostęp do danych dotyczących jakości powietrza w Polsce, wytwarzanych w ramach Państwowego Monitoringu 
Środowiska i gromadzonych w bazie EKOINFONET - JPOAT.

W skład danych udostępnionych przez GIOŚ wchodzą międzyinnymi:
- aktualne wskazania indeksu jakości powietrza
- lista stacji i stanowisk pomiarowych
- statystyki roczne
- archiwalne dane pomiarowe

Dane udostępniane są w formacie JSON, dzięki czemu mogą być w łatwy sposób parsowane przez struktury danych dostępne w Pythonie.
Dokumentację wraz z przykładami wykorzystania zapytań API można znaleźć pod [tym linkiem](https://powietrze.gios.gov.pl/pjp/content/api).

Przykład odpowiedzi API:

![przykład odpowiedzi](https://github.com/KarolPOrange/warsztaty_qgis_poznan_2024/assets/61205666/9eee7605-eb5e-4ea7-8441-022c732da466)

## Interfejs użytkownika z pyQt
Interfejs użytkownika zbudowany jest w QGiSie za pomocą freamworku Qt.
Framework Qt zawiera kompleksowy zestaw wysoce intuicyjnych i modułowych klas bibliotek C++.
Qt tworzy bardzo czytelny, łatwy w utrzymaniu i nadający się do ponownego użycia kod, 
charakteryzujący się wysoką wydajnością w czasie wykonywania i niewielkimi rozmiarami, ponadto jest wieloplatformowy.
Dodatkowo Qt jest wyposażony w interfejsy API, które upraszczają tworzenie aplikacji oraz pozwala na tworzenie GUI w 
innych językach programownia.

Na warsztatach skorzystamy właśnie z API Python-owego (nazwane pyQt - [dokumentacja](https://doc.qt.io/qtforpython-6/). 
Pozwoli nam to w szybki sposób zbudowanie interfejsu naszej wtyczki oraz podłączenie pod dane elementy GUI naszych funkcjonalności.

pyQt pozwala tworzyć GUI w dwojaki sposób:
- z poziomu kodu

![kodQt](https://github.com/KarolPOrange/warsztaty_qgis_poznan_2024/assets/61205666/49c45522-d670-42ba-a032-f50511a63224)

- za pomocą dedykowanego narzędzia (Qt Designer)

![qtDesigner](https://github.com/KarolPOrange/warsztaty_qgis_poznan_2024/assets/61205666/8e8c9f67-11b6-4a2a-bc1e-8ef945f02070)

