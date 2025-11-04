# OpenFrescoPy

Python wrapper for the OpenFresco API - an environment-independent software
framework that connects finite element models with control and data acquisition
systems in laboratories to facilitate hybrid simulation of structural and
geotechnical systems.

## Installation

### Requirements

- Python 3.10, 3.11, 3.12, 3.13, or 3.14 (64-bit)
- Windows (64-bit)
- pip (usually comes with Python)

### Installing from Wheel

Wheels are available in the `dist/` folder for Python 3.10-3.14. Install the appropriate wheel for your Python version:

1. **Find the wheel file** matching your Python version:
   - `dist/openfrescopy-0.1.0-cp310-cp310-win_amd64.whl` (Python 3.10)
   - `dist/openfrescopy-0.1.0-cp311-cp311-win_amd64.whl` (Python 3.11)
   - `dist/openfrescopy-0.1.0-cp312-cp312-win_amd64.whl` (Python 3.12)
   - `dist/openfrescopy-0.1.0-cp313-cp313-win_amd64.whl` (Python 3.13)
   - `dist/openfrescopy-0.1.0-cp314-cp314-win_amd64.whl` (Python 3.14)

2. **Install using pip:**
   ```bash
   pip install dist/openfrescopy-0.1.0-cp31x-cp31x-win_amd64.whl
   ```
   (Replace `x` with your Python minor version, e.g., `cp311` for Python 3.11)

3. **Verify installation:**
   ```bash
   python -c "import openfrescopy; print('Installation successful!')"
   ```

For information about building from source or understanding the build process, see `BUILD_GUIDE.md`.

## Usage

### Standalone Module

OpenFrescoPy can be used as a standalone module with any finite element code:

```python
import openfrescopy as opf

# Use OpenFrescoPy functions directly
# (function names depend on the API exposed by OpenFrescoPy.pyd)
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

**Note:** Use the wheel matching your Python version when installing. The package includes pre-built binaries for all supported Python versions.

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

Copyright © 2006. The Regents of the University of California (Regents).  
Copyright © 2006, Yoshikazu Takahashi, Kyoto University.

This software is licensed for educational, research, and not-for-profit purposes under
the UC Berkeley license. For commercial licensing opportunities, contact The Office of
Technology Licensing, UC Berkeley, 2150 Shattuck Avenue, Suite 510, Berkeley, CA 94720-1620,
(510) 643-7201.

Portions of this software are also subject to the BSD license from Kyoto University.
See [LICENSE](LICENSE) for full terms and conditions.

## Authors

- Andreas Schellenberg (andreas.schellenberg@gmx.net)
- Yoshikazu Takahashi (yos@catfish.dpri.kyoto-u.ac.jp)
- Gregory L. Fenves (fenves@berkeley.edu)
- Stephen A. Mahin (mahin@berkeley.edu)

## Links

- OpenFresco: https://github.com/aschellenberg74/OpenFresco

