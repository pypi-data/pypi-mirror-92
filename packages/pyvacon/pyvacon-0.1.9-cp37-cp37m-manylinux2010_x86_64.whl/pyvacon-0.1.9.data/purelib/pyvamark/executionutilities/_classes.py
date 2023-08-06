import pyvamark.pyvamark_swig as _swig
from pyvamark._converter import _add_converter

ExecutionParameter = _add_converter(_swig.ExecutionParameter)
InterfaceParameter = _add_converter(_swig.InterfaceParameter)
PythonWorkerParameter = _add_converter(_swig.PythonWorkerParameter)
