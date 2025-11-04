# Build Guide for OpenFrescoPy

## File Structure

```
openfrescopy/
├── __init__.py                    # Package root
├── _version_utils.py              # Version detection utilities (for dev mode)
├── setup.py                       # Build script with dummy Extension modules
├── pyproject.toml                 # Package metadata and configuration
│
├── openfresco/                    # Module wrapper (Python code)
│   └── __init__.py                # Loads OpenFrescoPy.pyd and DLLs
│
├── opensees/                      # Module wrapper (Python code)
│   └── __init__.py                # Loads opensees.pyd and DLLs
│
├── prebuilt/                      # Pre-built binaries (build artifacts)
│   ├── py310/                     # Pre-built binaries for Python 3.10
│   │   ├── openfresco/
│   │   │   ├── OpenFrescoPy.pyd  # ← Place your compiled .pyd here
│   │   │   └── *.dll              # ← Place all required DLLs here
│   │   └── opensees/
│   │       └── opensees.pyd       # ← Place your compiled .pyd here
│   │
│   ├── py311/                     # Pre-built binaries for Python 3.11
│   │   ├── openfresco/
│   │   │   ├── OpenFrescoPy.pyd  # ← Currently has files
│   │   │   └── *.dll
│   │   └── opensees/
│   │       └── opensees.pyd
│   │
│   ├── py312/                     # Pre-built binaries for Python 3.12
│   ├── py313/                     # Pre-built binaries for Python 3.13
│   └── py314/                     # Pre-built binaries for Python 3.14
```

## Build Process Overview

### Step 1: Compile .pyd Files with Visual Studio

For each Python version you want to support:

1. **Configure Visual Studio project** for the target Python version:
   - Set include directory: `C:\Python3XX\include`
   - Set library directory: `C:\Python3XX\libs`
   - Link against: `python3XX.lib` (e.g., `python311.lib`)
   - Set output extension: `.pyd` (not `.dll`)
   - Set output directory: `prebuilt/pyXXX/openfresco/` or `prebuilt/pyXXX/opensees/`

2. **Build OpenFrescoPy.pyd**:
   - Output: `prebuilt/py311/openfresco/OpenFrescoPy.pyd`
   - Copy all required DLLs to: `prebuilt/py311/openfresco/`
   - Ensure DLLs are compatible with this Python version

3. **Build opensees.pyd**:
   - Output: `prebuilt/py311/opensees/opensees.pyd`
   - **Important**: Must be compiled for the same Python version as OpenFrescoPy.pyd

4. **Repeat for each Python version** (3.10, 3.11, 3.12, 3.13, 3.14)

### Step 2: Build Wheel for Each Python Version

After placing binaries in the appropriate `prebuilt/pyXXX/` directories:

```bash
# Activate Python 3.1x conda environment
conda activate py31x  # or whatever your environment is named
python -m pip install build
python -m build --wheel
```

This will:
- Detect you're using Python 3.1x from the active environment
- Copy files from `py31x/` to the build directory
- Create wheel: `dist/openfrescopy-0.1.0-cp31x-cp31x-win_amd64.whl`

For instance, for Python 3.12:
```bash
conda activate py312
python -m pip install build
python -m build --wheel
conda deactivate
```

The resulting wheel will be tagged for Python 3.12:

- Package structure in wheel:
    ```
    openfrescopy/
    ├── openfresco/
    │   ├── __init__.py
    │   ├── OpenFrescoPy.pyd
    │   └── *.dll
    └── opensees/
        ├── __init__.py
        └── opensees.pyd
    ```
- Wheel filename: `openfrescopy-0.1.0-cp312-cp312-win_amd64.whl`

### Step 4: Installation

Users install the appropriate wheel:

```bash
pip install openfrescopy-0.1.0-cp312-cp312-win_amd64.whl
```

Python automatically selects the correct wheel based on:
- Python version (cp312)
- Platform (win_amd64)

## Important Notes

1. **Version Consistency**: All binaries in a `prebuilt/pyXXX/` directory must be compiled for the same Python version
2. **DLL Location**: DLLs go in `prebuilt/pyXXX/openfresco/` (shared by both modules)
3. **Wheel Tags**: Each wheel is built for ONE Python version (you get separate wheels for 3.10, 3.11, etc.)
4. **DLL Path Setup**: `os.add_dll_directory()` is called BEFORE importing extensions in both `__init__.py` files
5. **Always activate the conda environment** for the Python version you're building for. The `setup.py` script will detect the active Python version and copy from the corresponding `prebuilt/pyXXX/` directory.

