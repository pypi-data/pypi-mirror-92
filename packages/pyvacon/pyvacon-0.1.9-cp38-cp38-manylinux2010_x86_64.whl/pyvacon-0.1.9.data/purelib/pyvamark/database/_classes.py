import pyvamark.pyvamark_swig as _swig
from pyvamark._converter import _add_converter

DatabaseSettings = _add_converter(_swig.DatabaseSettings)
PgConnector = _add_converter(_swig.PgConnector)
DatabaseInterface = _add_converter(_swig.DatabaseInterface)
SpotDatabaseInterface = _add_converter(_swig.SpotDatabaseInterface)
SpotRedisInterface = _add_converter(_swig.SpotRedisInterface)
