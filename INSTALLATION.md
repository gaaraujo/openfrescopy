# Installation Instructions for OpenFrescoPy

## Requirements

- **Python 3.10 to 3.14** (64-bit)
- **Windows** (64-bit)
- **pip** (usually comes with Python)

## Installation

### For Python 3.1x Users (replace x with the appropriate version)

1. **Download the wheel file from the `dist/` folder:**
   - `dist/openfrescopy-0.1.0-cp31x-cp31x-win_amd64.whl`

2. **Install using pip:**
   ```bash
   pip install dist/openfrescopy-0.1.0-cp31x-cp31x-win_amd64.whl
   ```

   Or if you prefer to specify the full path:
   ```bash
   pip install C:\path\to\dist\openfrescopy-0.1.0-cp31x-cp31x-win_amd64.whl
   ```

3. **Verify installation:**
   ```python
   python -c "import openfrescopy; print('Installation successful!')"
   ```

## Testing the Installation

```python
# Test standalone module
import openfrescopy as opf
print("Has expElement:", hasattr(opf, 'expElement'))

# Test OpenSees integration
import openfrescopy.opensees as ops
print("Has model:", hasattr(ops, 'model'))
print("Has expElement:", hasattr(ops, 'expElement'))
```

