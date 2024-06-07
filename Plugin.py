"""
QGIS Plugin: Api z Api
"""
import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.gui import QgisInterface
from qgis.utils import iface

from .ApiWindow import ApiWindow


class ActionRun:
    name = "Uruchom wtyczkę Api z Api"
    icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "api.svg"))
    parent = iface.mainWindow()


class Plugin:
    """Wtyczka Api z Api.

    :param iface: instancja interfejsu QGIS
    """

    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self.actionRun = None

    def initGui(self):
        """Inicjalizacjia interfejsu wtyczki.

        QGIS najpierw ładuje kolejno wtyczki, uruchamia swoje GUI a na końcu woła kolejno initGui wszystkich wtyczek.
        """
        self.actionRun = QAction(
            ActionRun.icon,
            ActionRun.name,
            ActionRun.parent
        )
        self.actionRun.triggered.connect(self.run)  # uruchamiaj 'run' na kliknięcie ikony z wtyczką
        iface.pluginToolBar().addAction(self.actionRun)  # dodaj akcję do paska narzędzi
        iface.pluginMenu().addAction(self.actionRun)  # dodaj akcję do menu QGIS


    def unload(self):
        """Rozładuj wtyczkę."""
        iface.pluginToolBar().removeAction(self.actionRun)  # usuń akcję z paska narzędzi
        iface.pluginMenu().removeAction(self.actionRun)  # usuń akcję z menu QGIS


    def run(self):
        """Uruchom okno wtyczki."""
        window = ApiWindow()  # utworzenie obiektu klasy ApiWindow, tworzone nowe okno, stare nie jest zapamiętane
        window.show()  # pokaż okno
