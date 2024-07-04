import os

from qgis import processing
from qgis.core import (QgsVectorLayer, QgsProcessing, QgsRasterLayer, QgsProject, QgsRasterBandStats,
                       QgsColorRampShader, QgsSingleBandPseudoColorRenderer, QgsStyle)


def nadajStylWarstwie(warstwa: QgsVectorLayer, nazwaStylu: str):
    """Ustawienie stylu warstwie wektorowej z pliku."""
    uri = os.path.join(os.path.dirname(__file__), 'style', f'{nazwaStylu}.qml')
    warstwa.loadNamedStyle(uri)
    warstwa.triggerRepaint()

def nadajStylRastrowi(raster: QgsRasterLayer):
    """Ustawienie stylu dla warstwy wektorowej"""
    renderer = QgsSingleBandPseudoColorRenderer(raster.dataProvider(), 1)
    statystykiRastra = raster.dataProvider().bandStatistics(1, QgsRasterBandStats.All)

    renderer.setClassificationMax(statystykiRastra.maximumValue)
    renderer.setClassificationMin(statystykiRastra.minimumValue)

    domyslnyStyl = QgsStyle().defaultStyle()
    domyslnaPaletaBarw = domyslnyStyl.colorRampNames()
    wybranaPaletaBarw = domyslnyStyl.colorRamp(domyslnaPaletaBarw[25])
    wybranaPaletaBarw.invert()

    renderer.createShader(wybranaPaletaBarw, QgsColorRampShader.Interpolated, QgsColorRampShader.Continuous, 5)
    raster.setRenderer(renderer)

def interpolacja(warstwa: QgsVectorLayer, nazwaWskaznika: str) -> QgsRasterLayer:
    """Interpolacja danych dla wskazanego wskaźnika"""
    extent = warstwa.extent()
    xmin, xmanx, ymin, ymax = extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum()
    index = warstwa.fields().indexFromName(nazwaWskaznika)
    interpolation_input = f"{warstwa.source()}::~::0::~::{index}::~::0"

    rasterUrl = processing.run("qgis:tininterpolation",
                                  {'INTERPOLATION_DATA': interpolation_input,
                                   'EXTENT': f"{xmin},{xmanx},{ymin},{ymax} [EPSG:4326]",
                                   'METHOD': 0, 'PIXEL_SIZE': 0.1, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
                                   'TRIANGULATION': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    warstwa = QgsRasterLayer(rasterUrl, "Interpolacja")
    QgsProject.instance().addMapLayer(warstwa)
    return warstwa
