# OpenFrescoPy

Python wrapper for the OpenFresco API - an environment-independent software
framework that connects finite element models with control and data acquisition
systems in laboratories to facilitate hybrid simulation of structural and
geotechnical systems.

## Installation

Install from source:

```bash
pip install .
```

Or for development mode:

```bash
pip install -e .
```

## Usage

### Standalone Module

OpenFrescoPy can be used as a standalone module with any finite element code:

```python
import openfrescopy as opf

# Use OpenFrescoPy functions directly
# (function names depend on the API exposed by _openfrescopy.pyd)
```

### OpenSees Integration

For OpenSees-specific integration, use the `opensees` submodule which extends
`opensees.pyd` with `openfrescopy.dll` functionality:

```python
import openfrescopy.opensees as ops

# Regular OpenSees functionality
ops.model('-basic', '-ndm', 2, '-ndf', 3)

# OpenFrescoPy hybrid simulation commands
ops.expElement("twoNodeLink", 1, 1, 3, "-dir", 2, "-site", 1,
               "-initStif", 2.8)
```

The DLL path is automatically configured when importing
`openfrescopy.opensees`, so no manual PATH setup is required.

## Requirements

- Python 3.10, 3.11, 3.12, 3.13, or 3.14 (compiled extensions are version-specific)
- Windows (compiled extensions are Windows-specific)
- OpenSeesPy (for OpenSees integration)

**Note:** The package automatically detects your Python version and loads the appropriate compiled binaries. Ensure you have binaries compiled for your Python version (see `BUILD_GUIDE.md` for build instructions).

## Examples

See the `examples/` directory for working examples, including:
- `OneBayFrame/OpenSees/OneBayFrame_Local.py` - Local hybrid simulation example

### Running the Example

After installation, run the example:

```bash
cd examples/OneBayFrame/OpenSees
python OneBayFrame_Local.py
```

This will generate output files (Node_Dsp.out, Node_Vel.out, etc.) in the example directory.

### Testing the Installation

Verify the installation works:

```python
# Test standalone module
import openfrescopy as opf
print("Has expElement:", hasattr(opf, 'expElement'))

# Test OpenSees integration
import openfrescopy.opensees as ops
print("Has model:", hasattr(ops, 'model'))
print("Has expElement:", hasattr(ops, 'expElement'))
```

## License

Copyright (c) 2006, The Regents of the University of California.
All Rights Reserved.

Commercial use of this program without express permission of the University of
California, Berkeley, is strictly prohibited. See file 'COPYRIGHT_UCB' in main
directory for information on usage and redistribution, and for a DISCLAIMER OF
ALL WARRANTIES.

## Authors

- Andreas Schellenberg (andreas.schellenberg@gmx.net)
- Yoshikazu Takahashi (yos@catfish.dpri.kyoto-u.ac.jp)
- Gregory L. Fenves (fenves@berkeley.edu)
- Stephen A. Mahin (mahin@berkeley.edu)

## Links

- OpenFresco: https://github.com/aschellenberg74/OpenFresco

