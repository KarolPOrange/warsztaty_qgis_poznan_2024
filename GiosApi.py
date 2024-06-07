from __future__ import annotations

import pandas as pd
import requests
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsProject, QgsField, QgsFeature, QgsGeometry, QgsPointXY


class GiosApi:
    """Interfejs API portalu "Jakość Powietrza" GIOŚ."""

    HEADERS = {'Accept-Encoding': 'gzip, deflate', }
    PARAMS = {'size': 500, }
    URLS = {
        'stacje': r'https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll',
        'stanowiskaPomiarowe': r'https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/',
        'wskazniki': r'https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/'
    }

    def __init__(self, session: requests.session):
        self.session = session

    @classmethod
    def pobierzStacjePomiarowe(cls) -> dict:
        """Pobierz wszystkie stacje pomiarowe."""
        response = requests.get(cls.URLS['stacje'], headers=cls.HEADERS, params=cls.PARAMS)
        return response.json()

    def _pobierzIdStanowiskaPom(self, idStacji: int, nazwaWskaznika: str) -> str | None:
        """Pobierz identyfikator stanowiska dla danego wskaźnika, w wybranej stacji pomiarowej."""
        URL = f"{self.URLS['stanowiskaPomiarowe']}{idStacji}"

        response = self.session.get(URL, headers=self.HEADERS, params=self.PARAMS)
        wskazniki = response.json()["Lista stanowisk pomiarowych dla podanej stacji"]
        stanowisko_pomiarowe = next(
            filter(lambda wskaznik: wskaznik['Wskaźnik - kod'] == nazwaWskaznika, wskazniki), None
        )

        return stanowisko_pomiarowe['Identyfikator stanowiska'] if stanowisko_pomiarowe else None

    def _pobierzDaneDlaWskaznika(self, idStacji: int, nazwaWskaznika: str) -> int | None:
        """Pobierz wartości danego wskaźnika, w wybranej stacji pomiarowej."""
        idStanowiskaPom = self._pobierzIdStanowiskaPom(idStacji, nazwaWskaznika)

        if not idStanowiskaPom:
            return None

        URL = f"{self.URLS['wskazniki']}{idStanowiskaPom}"
        response = self.session.get(URL, headers=self.HEADERS, params=self.PARAMS)
        wartoscWskaznika = response.json().get("Lista danych pomiarowych", None)
        wartoscWskaznika = float(sum(d['Wartość'] if d['Wartość'] else 0 for d in wartoscWskaznika)) / len(
            wartoscWskaznika) if wartoscWskaznika else None

        return int(wartoscWskaznika) if wartoscWskaznika else None

    def _aktualizaujDanePomiarowe(self, stacje: pd.DataFrame, nazwaWskaznika: str):
        """Aktualizuj dane stacji pomiarowych o wartości danego wskaźnika."""
        for stacja in stacje.itertuples(name='Stacja'):
            stacje.loc[stacja.Index, nazwaWskaznika] = self._pobierzDaneDlaWskaznika(stacja.id_stacji, nazwaWskaznika)

    def _zapisDoWarstwy(self, stacje: pd.DataFrame) -> QgsVectorLayer:
        """Konwertuj dane z pd.DataFrame do postaci warstwy wektorowej QGiS."""
        warstwa = QgsVectorLayer('Point?crs=EPSG:4326', "Stacje", "memory")
        warstwa_pr = warstwa.dataProvider()
        warstwa.startEditing()

        kolumny = [QgsField(nazwa_kolumny, QVariant.String) for nazwa_kolumny in stacje.columns[:-1]]
        kolumny.append(QgsField(stacje.columns[-1], QVariant.Double))
        warstwa_pr.addAttributes(kolumny)
        warstwa.updateFields()

        for stacja in stacje.itertuples():
            nowyObiekt = QgsFeature()
            nowyObiekt.setAttributes([str(dane) for dane in stacja[1:]])
            nowyObiekt.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(stacja.long), float(stacja.lat))))
            warstwa.addFeature(nowyObiekt)
        warstwa.commitChanges()
        return warstwa

    def pobierzWarstwe(self, nazwaWskaznika: str) -> QgsVectorLayer:
        """Pobierz dane o wartości danego wskaźnika powietrza dla stacji pomiaorych w Polsce."""
        if not nazwaWskaznika:
            return QgsVectorLayer()
        stacje = pd.json_normalize(self.pobierzStacjePomiarowe()['Lista stacji pomiarowych'])
        stacje.rename(columns={'Identyfikator stacji': 'id_stacji',
                               'Kod stacji': 'kod_stacji',
                               'Nazwa stacji': 'nazwa_stacji',
                               'WGS84 φ N': 'lat',
                               'WGS84 λ E': 'long',
                               'Identyfikator miasta': 'id_miasta',
                               'Nazwa miasta': 'nazwa_miasta',
                               'Gmina': 'gmi',
                               'Powiat': 'pow',
                               'Województwo': 'woj',
                               'Ulica': 'ul'}, inplace=True)

        self._aktualizaujDanePomiarowe(stacje, nazwaWskaznika)
        stacje.dropna(subset=[nazwaWskaznika], inplace=True)
        return self._zapisDoWarstwy(stacje)


if __name__ == '__main__':
    with requests.Session() as session:
        giosApi = GiosApi(session)
        warstwa = giosApi.pobierzWarstwe('PM10')
        QgsProject.instance().addMapLayer(warstwa)
