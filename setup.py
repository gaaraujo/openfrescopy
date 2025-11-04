"""
Setup script for openfrescopy package with dummy Extension modules for proper wheel tags.

This setup uses dummy Extension modules to ensure wheels get correct Python version
and platform tags (cp3XX, win_amd64, etc.) even though the actual .pyd files are
compiled with Visual Studio outside of setuptools.

The build process:
1. Detects the current Python version
2. Copies pre-built .pyd files from pyXXX/ directories to their target subpackages
3. Copies shared DLLs to the appropriate location
4. Creates dummy Extension modules to trigger proper wheel tagging
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
import sys
import shutil
from pathlib import Path


class ExcludeSetupPy(build_py):
    """Custom build_py that excludes setup.py from the package."""
    
    def copy_file(self, src, dst, preserve_mode=True, preserve_times=True, link=None, level=1):
        """Override copy_file to skip copying setup.py."""
        if src.endswith('setup.py') or 'setup.py' in src:
            self.announce(f"Skipping {src} (build-time file)", level=2)
            return dst, False
        return super().copy_file(src, dst, preserve_mode, preserve_times, link, level)


class CopyPrebuiltExtension(build_ext):
    """Custom build_ext that copies pre-built .pyd files instead of compiling."""
    
    def build_extensions(self):
        """Copy pre-built extensions from prebuilt/pyXXX directories."""
        # Get Python version (e.g., 311 for Python 3.11)
        py_version = f"{sys.version_info.major}{sys.version_info.minor:02d}"
        source_version_dir = Path("prebuilt") / f"py{py_version}"
        
        if not source_version_dir.exists():
            print(f"Warning: Source directory {source_version_dir} not found. "
                  f"Skipping extension copy for Python {sys.version_info.major}.{sys.version_info.minor}")
            return
        
        # Determine build directory
        build_lib = Path(self.build_lib)
        
        # Get extension suffix for expected filename (e.g., .cp311-win_amd64.pyd)
        ext_suffix = self.get_ext_filename("")
        
        # Copy OpenFrescoPy.pyd to subpackage and extension build location
        openfresco_source = source_version_dir / "openfresco" / "OpenFrescoPy.pyd"
        openfresco_target_dir = build_lib / "openfrescopy" / "openfresco"
        openfresco_target = openfresco_target_dir / "OpenFrescoPy.pyd"
        openfresco_ext_target = build_lib / f"OpenFrescoPy{ext_suffix}"
        
        if openfresco_source.exists():
            openfresco_target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(openfresco_source, openfresco_target)
            shutil.copy2(openfresco_source, openfresco_ext_target)
            print(f"Copied {openfresco_source.name} -> subpackage and extension location")
        else:
            print(f"Warning: {openfresco_source} not found")
        
        # Copy opensees.pyd to subpackage and extension build location
        opensees_source = source_version_dir / "opensees" / "opensees.pyd"
        opensees_target_dir = build_lib / "openfrescopy" / "opensees"
        opensees_target = opensees_target_dir / "opensees.pyd"
        opensees_ext_target = build_lib / f"opensees{ext_suffix}"
        
        if opensees_source.exists():
            opensees_target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(opensees_source, opensees_target)
            shutil.copy2(opensees_source, opensees_ext_target)
            print(f"Copied {opensees_source.name} -> subpackage and extension location")
        else:
            print(f"Warning: {opensees_source} not found")
        
        # Copy shared DLLs to openfresco subpackage
        openfresco_dll_dir = source_version_dir / "openfresco"
        if openfresco_dll_dir.exists() and openfresco_target_dir.exists():
            for dll_file in openfresco_dll_dir.glob("*.dll"):
                shutil.copy2(dll_file, openfresco_target_dir / dll_file.name)
            print(f"Copied {len(list(openfresco_dll_dir.glob('*.dll')))} DLL file(s)")


# Dummy Extension modules to trigger proper wheel tags
# These won't actually be compiled - we copy pre-built .pyd files instead
# The names match the .pyd module names (OpenFrescoPy and opensees are top-level modules)
ext_modules = [
    Extension(
        "OpenFrescoPy",
        sources=[],  # Empty - we'll copy pre-built .pyd
        language="c++",
    ),
    Extension(
        "opensees",
        sources=[],  # Empty - we'll copy pre-built .pyd
        language="c++",
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={
        "build_ext": CopyPrebuiltExtension,
        "build_py": ExcludeSetupPy,
    },
)
