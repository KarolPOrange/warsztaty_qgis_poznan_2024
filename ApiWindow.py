import os
from typing import Any

import requests
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor, QBrush, QIcon
from qgis.PyQt.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QWidget
from qgis.core import QgsProject, QgsFeature, QgsVectorLayer
from qgis.utils import iface

from .GiosApi import GiosApi
from .utils import nadajStylWarstwie, interpolacja, nadajStylRastrowi

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ApiWindow.ui'))


class ApiWindow(QMainWindow, FORM_CLASS):
    """Okno umożliwiające wyświetlanie danych o jakości powietrza."""
    def __init__(self):
        super().__init__(iface.mainWindow())  # ustal parenta, w którym ma się wyświetlać okno
        self.setupUi(self)  # ustawienie UI
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), './icons', 'api.svg')))
        self.wgtCenterMenu.hide()
        self.stationsLayer = None
        self.indicatorName = None
        self.graphicsView.setCachingEnabled(True)


    def on_pbPM10_released(self):
        """Na odpuszczenie przycisku dodaj/usuń warstwy dotyczące wskaźnika PM10"""
        self._onIndicatorButtonReleased(self.pbPM10)

    def on_pbNO2_released(self):
        """Na odpuszczenie przycisku dodaj/usuń warstwy dotyczące wskaźnika NO2"""
        self._onIndicatorButtonReleased(self.pbNO2)

    def on_pbSO2_released(self):
        """Na odpuszczenie przycisku dodaj/usuń warstwy dotyczące wskaźnika SO2"""
        self._onIndicatorButtonReleased(self.pbSO2)

    def on_pbO3_released(self):
        """Na odpuszczenie przycisku dodaj/usuń warstwy dotyczące wskaźnika O3"""
        self._onIndicatorButtonReleased(self.pbO3)

    def on_pbDane_released(self):
        """Na odpuszczenie przycisku pokaż/ukryj dane dotyczące wskaźników"""
        if self.wgtCenterMenu.isHidden():
            self.wgtCenterMenu.show()  # pokaż zakładkę z tabelą z danymi
        else:
            self.wgtCenterMenu.hide()  # ukryj zakładkę z tabelą z danymi

        if not self.stationsLayer:
            return  # jeżeli nie ma warstwy, to nie generuj danych do tabeli

        self._aktualizujWierszeWTabeli()

    def on_pbInterpolacja_released(self):
        if self.stationsLayer:
            raster = interpolacja(self.stationsLayer, self._indicatorName())
            nadajStylRastrowi(raster)
            self.graphicsView.setLayers([])  # wyczyść warstwy
            self.graphicsView.setLayers([self.stationsLayer, raster, self._osmLayer()])  # dodaj warstwy do widoku
            self.graphicsView.show()

    def _aktualizujWierszeWTabeli(self):
        """Dodaje wypełnione wiersze w tabeli dla elementów z warstwy"""
        self.twDane.setRowCount(0)
        for feat in self.stationsLayer.getFeatures():
            self._addRow(feat)  # dodaj dane w tabeli


    def _uncheckButtons(self, parent: QWidget, buttonToSkip: QPushButton=None):
        """Odznacz QPushButtony należące do podanego prenta."""
        for button in parent.findChildren(QPushButton):
            if buttonToSkip and buttonToSkip.objectName() == button.objectName():
                continue
            button.setChecked(False)


    def _checkedButton(self, parent: QWidget) -> QPushButton:
        """Zwraca wciśnięty QPushButton ze wszystkich buttonów podanego parenta."""
        for button in parent.findChildren(QPushButton):
            if button.isChecked():
                return button


    def _indicatorName(self) -> str:
        """Zwróć nazwę wskaźnika"""
        if checked_button := self._checkedButton(self.frameTop):
            return checked_button.objectName().replace('pb', '')


    def _clearData(self):
        """Wyczyść scenę oraz tabelę danych."""
        self.graphicsView.setLayers([])  # wyczyść warstwy
        self.twDane.setRowCount(0)  # usuń wiersze
        self.stationsLayer = None
        QgsProject.instance().removeAllMapLayers()

    def _setStationLayer(self):
        """Ustaw warstwe z danymi o stacjach i wartościach wskaźników jakości powietrza."""
        with requests.Session() as session:
            giosApi = GiosApi(session)
            self.stationsLayer = giosApi.pobierzWarstwe(self._indicatorName())
            nadajStylWarstwie(self.stationsLayer, self._indicatorName())
            QgsProject.instance().addMapLayer(self.stationsLayer)

    def _osmLayer(self) -> QgsVectorLayer:
        """Zwraca warstwę OSM jeżeli została dodana do projektu.

        :return: warstwa osm jeżeli istnieje
        """
        lyrs_osm = QgsProject.instance().mapLayersByName("OSM Standard")
        return lyrs_osm[0] if lyrs_osm else None


    def _setGraphicView(self):
        """Ustaw widok."""
        self.graphicsView.setDestinationCrs(self.stationsLayer.crs())  # ustaw układ współrzędnych warstwy
        extent = self.stationsLayer.extent()
        self.graphicsView.setExtent(extent.buffered(extent.width() / 20))  # ustaw zakres wyśwetlania danych w oknie
        self.graphicsView.setDestinationCrs(QgsProject.instance().crs())  # ustawiam crs projektu
        self.graphicsView.setLayers([self.stationsLayer, self._osmLayer()])  # dodaj warstwy do widoku
        self.graphicsView.show()


    def _onIndicatorButtonReleased(self, button: QPushButton):
        """Na wciśnięcie przycisku wskaźnika wyświetl dane."""
        self._clearData()
        if not button.isChecked():
            return  # aktualnie zwalniany przycisk jest odklikiwany, więc nie pobieraj danych

        self._uncheckButtons(self.frameTop, buttonToSkip=button)  # odznacz pozostałe przyciski wskaźników
        self._setStationLayer()  # ustaw warstwę z danymi o stacjach
        self._setGraphicView()  # ustaw wizualizację
        self._aktualizujWierszeWTabeli()  # aktualizuj dane w tabeli


    def _tableItem(self, itemValue: Any) -> QTableWidgetItem:
        """Zwraca item dla komórki w tabeli.

        :param itemValue: wartość komórki w wierszy == wartość dla QTableWidgetItem
        :return: item komórki tabeli
        """
        if isinstance(itemValue, float) or isinstance(itemValue, int):
            item = QTableWidgetItem(0)  # dla wartości liczbowych
            item.setData(0, itemValue)
        else:
            item = QTableWidgetItem(itemValue)  # dla wartości tekstowych

        item.setBackground(QBrush(QColor(207, 217, 218)))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # włączenie selekcji pól, wyłączenie edytowalności
        return item


    def _addRow(self, feature: QgsFeature):
        """Dodaje wiersz z uzupełnionymi danymi dla feature'a.

        :param feature: feature z warstwy (QgsVectorLayer)
        """
        self.twDane.insertRow(self.twDane.rowCount())
        station = feature['nazwa_stacji'] or ''
        city = feature['nazwa_miasta'] or ''
        indicator = feature[f"{self._indicatorName()}"] or ''

        for ind, val in enumerate([station, city, indicator]):
            row_number = self.twDane.rowCount() - 1
            self.twDane.setItem(row_number, ind, self._tableItem(val))
