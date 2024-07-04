"""
QGIS plugin: Api z Api
"""
def classFactory(iface):
    from .Plugin import Plugin
    return Plugin(iface)
