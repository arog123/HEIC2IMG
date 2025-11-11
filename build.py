"""
Build script for HEIC to JPG/PNG Converter
Creates standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
import platform

def clean_build_dirs():
    """Remove old build directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/ directory...")
            shutil.rmtree(dir_name)
    
    # Remove spec file if exists
    if os.path.exists('heic_converter.spec'):
        os.remove('heic_converter.spec')
    
    print("Build directories cleaned.\n")

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("PyInstaller not found!")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding executable...\n")
    
    # Determine the platform
    system = platform.system()
    print(f"Building for: {system}\n")
    
    # Base PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=HEIC_Converter',
        '--windowed',  # No console window
        '--onefile',   # Single executable file
        '--clean',     # Clean PyInstaller cache
    ]
    
    # Add icon if it exists (you can create one)
    if os.path.exists('icon.ico'):
        cmd.append('--icon=icon.ico')
    
    # Hidden imports for dependencies
    hidden_imports = [
        'PIL._tkinter_finder',
        'pillow_heif',
        'tkinterdnd2',
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # Add data files if needed
    # cmd.extend(['--add-data', 'data_folder;data_folder'])  # Windows
    # cmd.extend(['--add-data', 'data_folder:data_folder'])  # Linux/Mac
    
    # Add the main script
    cmd.append('app.py')
    
    # Execute PyInstaller
    try:
        print(f"Running command: {' '.join(cmd)}\n")
        subprocess.check_call(cmd)
        print("\n" + "="*70)
        print("Build completed successfully!")
        print("="*70)
        
        # Show output location
        if system == "Windows":
            exe_name = "HEIC_Converter.exe"
        else:
            exe_name = "HEIC_Converter"
        
        output_path = os.path.join('dist', exe_name)
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
            print(f"\nExecutable created: {output_path}")
            print(f"File size: {file_size:.2f} MB")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        return False

def create_spec_file():
    """Create a custom .spec file for more control (optional)"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',
        'pillow_heif',
        'tkinterdnd2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HEIC_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""
    
    with open('heic_converter.spec', 'w') as f:
        f.write(spec_content)
    
    print("Custom .spec file created: heic_converter.spec")
    print("You can now build using: pyinstaller heic_converter.spec\n")

def main():
    """Main build process"""
    print("="*70)
    print("HEIC to JPG/PNG Converter - Build Script")
    print("="*70)
    print()
    
    # Check if main script exists
    if not os.path.exists('app.py'):
        print("Error: app.py not found in current directory!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Verify dependencies are installed
    print("Checking dependencies...")
    try:
        import PIL
        import pillow_heif
        import tkinterdnd2
        print("All dependencies found.\n")
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install all requirements first: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        print("Failed to install PyInstaller")
        sys.exit(1)
    
    print()
    
    # Ask user for build options
    print("Build Options:")
    print("1. Quick build (recommended)")
    print("2. Clean build (removes old build files first)")
    print("3. Create custom .spec file only")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        build_executable()
    elif choice == '2':
        clean_build_dirs()
        build_executable()
    elif choice == '3':
        create_spec_file()
    elif choice == '4':
        print("Build cancelled.")
        sys.exit(0)
    else:
        print("Invalid option. Please run again.")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("Build process completed!")
    print("="*70)
    print("\nNext steps:")
    print("1. Test the executable in the 'dist' folder")
    print("2. Distribute the executable to users")
    print("3. Consider code signing for production releases")

if __name__ == '__main__':
    main()