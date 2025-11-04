# openfrescopy/opensees/__init__.py
"""
# ****************************************************************** #
#    OpenFRESCO - Open Framework                                     #
#                 for Experimental Setup and Control                 #
#                                                                    #
#                                                                    #
# Copyright (c) 2006, The Regents of the University of California    #
# All Rights Reserved.                                               #
#                                                                    #
# Commercial use of this program without express permission of the   #
# University of California, Berkeley, is strictly prohibited. See    #
# file 'COPYRIGHT_UCB' in main directory for information on usage    #
# and redistribution, and for a DISCLAIMER OF ALL WARRANTIES.        #
#                                                                    #
# Developed by:                                                      #
#   Andreas Schellenberg (andreas.schellenberg@gmx.net)              #
#   Yoshikazu Takahashi (yos@catfish.dpri.kyoto-u.ac.jp)             #
#   Gregory L. Fenves (fenves@berkeley.edu)                          #
#   Stephen A. Mahin (mahin@berkeley.edu)                            #
#                                                                    #
# ****************************************************************** #

This module extends the original OpenSeesPy API (opensees.pyd) with hybrid
simulation capabilities by loading the OpenFrescoPy package (openfrescopy.dll).
This allows users to use both standard OpenSees functionality and OpenFrescoPy
hybrid simulation commands within the same OpenSees session.

Usage:
    Instead of importing the original OpenSeesPy API, import this module:
        import openfrescopy.opensees as ops
    
    Regular OpenSees functionality is available:
        ops.model('-basic', '-ndm', 2, '-ndf', 3)
    
    OpenFrescoPy hybrid simulation commands are also available:
        ops.expElement("twoNodeLink", 1, 1, 3, "-dir", 2, "-site", 1,
                      "-initStif", 2.8)
"""

# IMPORTANT: Set up DLL search path BEFORE importing any extensions
import os
import sys
from pathlib import Path

# Get the package root directory and subpackage directories
package_dir = Path(__file__).parent.parent.resolve()
opensees_dir = Path(__file__).parent.resolve()  # This subpackage directory
openfresco_dir = package_dir / "openfresco"  # Where shared DLLs are located

# Use Windows AddDllDirectory for DLL loading (Python 3.8+)
# This MUST be done before importing the .pyd extension
# DLLs are in openfresco subpackage where they're shared
os.add_dll_directory(str(openfresco_dir))
os.add_dll_directory(str(opensees_dir))

# Also add to PATH for loadPackage() which uses native Windows DLL loading
# loadPackage() looks for OpenFrescoPy.dll and may not respect os.add_dll_directory
openfresco_dir_str = str(openfresco_dir)
current_path = os.environ.get('PATH', '')
if openfresco_dir_str not in current_path:
    os.environ['PATH'] = openfresco_dir_str + os.pathsep + current_path

# Add opensees directory to sys.path so Python can find opensees.pyd
# opensees.pyd is a top-level module, so we need to add its directory to sys.path
if str(opensees_dir) not in sys.path:
    sys.path.insert(0, str(opensees_dir))

# Now try to import the OpenSeesPy API module (opensees.pyd)
# DLL path is already set up above
try:
    import opensees as _ops
except Exception as e:
    _import_error = e
    _ops = None

# Load the OpenFrescoPy package (OpenFrescoPy.dll) into the OpenSeesPy API
# This extends opensees.pyd with OpenFrescoPy hybrid simulation capabilities
# Note: loadPackage expects "OpenFrescoPy" (capitalized) as the package name
if _ops is not None:
    try:
        _ops.loadPackage('OpenFrescoPy')
    except Exception as e:
        # If loadPackage fails, log but don't fail the import
        _package_load_error = e
    
    # Expose all public attributes from the OpenSeesPy API (including
    # OpenFrescoPy functions). This allows users to import directly from the
    # module instead of accessing _ops. 
    # Example: 
    #   import openfrescopy.opensees as ops;
    #   ops.model(...); 
    #   ops.expElement(...)
    # Iterate through all attributes in the opensees module
    for _name in dir(_ops):
        # Only expose public attributes (those not starting with underscore)
        if not _name.startswith('_'):
            # Add each public attribute to this module's global namespace
            globals()[_name] = getattr(_ops, _name)

