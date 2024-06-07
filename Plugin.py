"""
QGIS Plugin: Api z Api
"""
import os

from qgis.PyQt.QtGui import QIcon, QAction
from qgis.gui import QgisInterface


class Akcja:
    ikona = QIcon(os.path.join(os.path.dirname(__file__), 'icons', 'api.svg'))
    nazwa = "Uruchom wtyczkę Api z Api"
    opis = "Wtyczka pobierająca za pomocą API i wizualizująca dane o jakości powietrza"


class Plugin:
    """Wtyczka Api z Api.

    :param iface: instancja interfejsu QGIS
    """

    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self.akcja = None

    def initGui(self):
        self.akcja = QAction(Akcja.ikona, Akcja.nazwa, self.iface.mainWindow())
        self.akcja.triggered.connect(self.run)  # uruchamiaj 'run' na kliknięcie ikony z wtyczką
        self.iface.pluginToolBar().addAction(self.akcja)  # dodaj akcję do paska narzędzi
        self.iface.pluginMenu().addAction(self.akcja)  # dodaj akcję do menu QGIS


    def unload(self):
        """Rozładowje wtyczkę. Rozłącza sygnały, zamyka okna należące do wtyczki, usuwa ikonę."""
        self.akcja.triggered.disconnect(self.run)  # rozłącz sygnał 'run'
        self.iface.pluginToolBar().removeAction(self.akcja)  # usuń akcję z paska narzędzi
        self.iface.pluginMenu().removeAction(self.akcja)  # usuń akcję z menu QGIS

    def run(self):
        """Otwiera/zamyka okno"""
        print("RUN")
