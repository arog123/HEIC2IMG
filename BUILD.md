# Building the HEIC Converter

This guide explains how to build the HEIC to JPG/PNG Converter into a standalone executable.

## Prerequisites

- Python 3.7 or higher installed
- All project dependencies installed (`pip install -r requirements.txt`)
- PyInstaller will be automatically installed by the build script if not present

## Quick Build

The easiest way to build the application:

```bash
python build.py
```

Then select option 1 for a quick build.

## Build Options

### Option 1: Using the Build Script (Recommended)

Run the interactive build script:

```bash
python build.py
```

**Available options:**
1. **Quick build** - Build immediately without cleaning
2. **Clean build** - Remove old build files first, then build
3. **Create custom .spec file** - Generate a .spec file for advanced customization
4. **Exit** - Cancel the build

### Option 2: Manual PyInstaller Command

If you prefer to build manually:

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Basic build
pyinstaller --name=HEIC_Converter --windowed --onefile app.py

# With hidden imports (recommended)
pyinstaller --name=HEIC_Converter --windowed --onefile \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=pillow_heif \
  --hidden-import=tkinterdnd2 \
  app.py
```

### Option 3: Using Custom .spec File

For more control over the build:

1. Generate the .spec file:
   ```bash
   python build.py
   # Select option 3
   ```

2. Edit `heic_converter.spec` as needed

3. Build using the spec file:
   ```bash
   pyinstaller heic_converter.spec
   ```

## Build Output

After building, you'll find:

- **dist/** folder containing the executable
  - Windows: `HEIC_Converter.exe`
  - macOS: `HEIC_Converter.app` or `HEIC_Converter`
  - Linux: `HEIC_Converter`

- **build/** folder containing build files (can be deleted)

## Platform-Specific Notes

### Windows

- The executable will be created as `HEIC_Converter.exe`
- No console window will appear (windowed mode)
- File size: ~30-50 MB (varies with dependencies)
- You can add an icon by placing `icon.ico` in the project root

### macOS

- The executable will be created as `HEIC_Converter` or `HEIC_Converter.app`
- May need to allow the app in Security & Privacy settings
- Code signing recommended for distribution

### Linux

- The executable will be created as `HEIC_Converter`
- May need to make it executable: `chmod +x dist/HEIC_Converter`
- Should work on most modern Linux distributions

## Adding an Icon

To add a custom icon to your executable:

1. Create or download an icon file:
   - Windows: `icon.ico` (ICO format)
   - macOS: `icon.icns` (ICNS format)
   - Linux: `icon.png` (PNG format)

2. Place it in the project root directory

3. The build script will automatically include it

## Troubleshooting

### "Module not found" errors

Add the missing module to hidden imports:
```bash
pyinstaller --hidden-import=missing_module_name app.py
```

### Executable is too large

Try these options:
- Use `--onefile` for a single executable (slower startup)
- Use `--onedir` for faster startup but multiple files
- Exclude unnecessary packages: `--exclude-module=module_name`

### Runtime errors in built executable

1. Test with console mode first: Remove `--windowed` flag
2. Check for missing data files or dependencies
3. Review the build output for warnings

### UPX Errors

If you see UPX-related errors, disable UPX compression:
```bash
pyinstaller --noupx app.py
```

## Advanced Customization

### Custom .spec File Options

Edit `heic_converter.spec` to customize:

- **datas**: Include additional files
  ```python
  datas=[('icon.png', '.')],
  ```

- **binaries**: Include binary files
  ```python
  binaries=[('lib/mylib.so', 'lib')],
  ```

- **excludes**: Exclude modules to reduce size
  ```python
  excludes=['matplotlib', 'numpy'],
  ```

- **upx**: Enable/disable UPX compression
  ```python
  upx=True,  # or False
  ```

### One Directory vs One File

**One File** (`--onefile`):
- Pros: Single executable, easy distribution
- Cons: Slower startup, larger file

**One Directory** (`--onedir`):
- Pros: Faster startup
- Cons: Multiple files to distribute

## Code Signing (Production)

### Windows
```bash
signtool sign /f certificate.pfx /p password HEIC_Converter.exe
```

### macOS
```bash
codesign --deep --force --verify --verbose --sign "Developer ID" HEIC_Converter.app
```

## Distribution

After building:

1. Test the executable thoroughly on the target platform
2. Create an installer (optional):
   - Windows: Use NSIS or Inno Setup
   - macOS: Create DMG file
   - Linux: Create .deb or .rpm package

3. Consider these distribution methods:
   - Direct download from website/GitHub releases
   - App stores (Microsoft Store, Mac App Store)
   - Package managers (Homebrew, Chocolatey)

## Clean Up

To remove build files:

```bash
# Manual cleanup
rm -rf build dist *.spec

# Or use the build script with option 2
python build.py
# Select option 2
```

## Testing the Executable

Before distribution:

1. Test on a clean system without Python installed
2. Test all features:
   - File browsing
   - Drag and drop
   - JPG conversion
   - PNG conversion
   - Error handling
3. Test with various HEIC file types
4. Check for missing dependencies

## CI/CD Integration

For automated builds, you can integrate with CI/CD:

### GitHub Actions Example

```yaml
name: Build Executable

on: [push]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    - name: Build executable
      run: python build.py
```

## Support

If you encounter issues during the build process:

1. Check the [PyInstaller documentation](https://pyinstaller.org/)
2. Review build warnings and errors carefully
3. Open an issue on the project repository with:
   - Your OS and Python version
   - Complete error message
   - Build command used

---

**Happy Building!** 🚀