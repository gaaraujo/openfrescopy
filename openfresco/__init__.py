# openfrescopy/openfresco/__init__.py
"""
OpenFrescoPy core module - compiled extension and DLLs.

This submodule contains the compiled OpenFrescoPy extension (OpenFrescoPy.pyd)
and its required DLL dependencies. The .pyd file is in this subpackage directory,
and DLLs are shared here for use by both openfresco and opensees modules.
Users typically import from the parent package (import openfrescopy), but this
submodule can also be imported directly as an alternative.
"""

# IMPORTANT: Set up DLL search path BEFORE importing any extensions
import os
import sys
from pathlib import Path

# Get the directory containing this __init__.py file (where .pyd and DLLs are located)
openfresco_dir = Path(__file__).parent.resolve()

# Use Windows AddDllDirectory for DLL loading (Python 3.8+)
# This MUST be done before importing the .pyd extension
os.add_dll_directory(str(openfresco_dir))

# Add this directory to sys.path so Python can find OpenFrescoPy.pyd
# This is necessary because OpenFrescoPy is a top-level module
if str(openfresco_dir) not in sys.path:
    sys.path.insert(0, str(openfresco_dir))

# Now try to import the core module (OpenFrescoPy.pyd)
# DLL path is already set up above
try:
    import OpenFrescoPy as _core
except Exception as e:
    _import_error = e
    _core = None

# If the core module was successfully imported, expose its public API
if _core is not None:
    _existing_names = set(globals().keys())
    
    for _name in dir(_core):
        if (not _name.startswith('_') and 
            _name not in _existing_names):
            globals()[_name] = getattr(_core, _name)

