# openfrescopy/__init__.py
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

OpenFresco is an environment-independent software framework that connects
finite element models with control and data acquisition systems in
laboratories to facilitate hybrid simulation of structural and geotechnical
systems.

OpenFrescoPy is a Python wrapper for the OpenFresco API that can be used as
a standalone module with any finite element code. For OpenSees-specific
integration, see the opensees submodule which extends opensees.pyd with
openfrescopy.dll functionality.

Usage:
    import openfrescopy as opf
"""

# Import from the openfresco submodule, which contains the compiled
# OpenFrescoPy.pyd and DLLs. The submodule handles its own DLL path setup.
try:
    from . import openfresco as _openfresco_module
    _core = _openfresco_module
except Exception as e:
    # Store error for debugging if needed, but don't fail the package import
    _import_error = e
    _core = None

# If the core module was successfully imported, expose its public API.
# This allows users to import directly from the package instead of the
# internal module. Example: from openfrescopy import function_name
if _core is not None:
    # Get the set of names already in this module's namespace (to avoid
    # exposing imports like Path, os, sys, etc.)
    _existing_names = set(globals().keys())
    
    # Iterate through all attributes in the core module
    for _name in dir(_core):
        # Only expose public attributes (those not starting with underscore)
        # and exclude names that are already in this module's namespace
        if (not _name.startswith('_') and 
            _name not in _existing_names):
            # Add each public attribute to this module's global namespace
            globals()[_name] = getattr(_core, _name)