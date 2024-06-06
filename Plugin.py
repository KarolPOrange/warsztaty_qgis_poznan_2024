
import os

from qgis.PyQt.QtGui import QIcon, QAction


class Akcja:
    ikona = QIcon(os.path.join(os.path.dirname(__file__), 'icons', 'api.svg'))
    nazwa = "Indeks Jakości Powietrza"
    opis = "Wtyczka pobierająca za pomocą API i wizualizująca dane o jakości powietrza"


class IndeksJakosciPowietrzaWtyczka:

    def __init__(self, iface):
        self.pasekNarzedzi = None
        self.iface = iface
        self.akcja = None
        self.oknoWtyczki = None

    def initGui(self):
        self.akcja = QAction(Akcja.ikona, Akcja.nazwa, self.iface.mainWindow())
        self.pasekNarzedzi = self.iface.addToolBar("Nasze Wtyczki")
        self.pasekNarzedzi.addAction(self.akcja)
        self.akcja.triggered.connect(self.run)

    def unload(self):
        """Rozładowje wtyczkę. Rozłącza sygnały, zamyka okna należące do wtyczki, usuwa ikonę."""
        self.akcja.triggered.disconnect(self.run)

    def run(self):
        """Otwiera/zamyka okno"""
        print("RUN")
