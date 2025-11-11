# HEIC2IMG
A little python program to convert .heic files to jpeg or png

# HEIC to JPG/PNG Converter

A simple Python desktop application with a graphical user interface for converting HEIC (High Efficiency Image Container) files to JPG or PNG format.

<img width="497" height="426" alt="Screenshot 2025-11-11 at 22 07 32" src="https://github.com/user-attachments/assets/f5745593-7065-43ff-86ad-0734ee0f3973" />

## Features

- **Drag & Drop Support** - Simply drag HEIC files onto the application window
- **File Browser** - Browse and select HEIC files from your computer
- **Multiple Output Formats** - Convert to either JPG or PNG
- **File Type Verification** - Automatically validates that selected files are HEIC format
- **Transparent Image Handling** - Properly converts images with transparency to JPG (with white background) or PNG (preserving transparency)
- **User-Friendly Interface** - Clean and intuitive GUI built with tkinter
- **Same Directory Output** - Converted files are saved in the same location as the original

## Requirements

- Python 3.7 or higher
- See `requirements.txt` for Python package dependencies

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `pillow` - Image processing library
   - `pillow-heif` - HEIC file format support
   - `tkinterdnd2` - Drag and drop functionality

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Load a HEIC file** using either method:
   - Drag and drop a HEIC file onto the application window
   - Click the "Browse File" button to select a file

3. **Select output format:**
   - Choose between JPG or PNG (JPG is selected by default)

4. **Convert the file:**
   - Click the "Convert" button
   - The converted file will be saved in the same directory as the original file

5. **Success message:**
   - A popup will confirm successful conversion and show the output filename

## Output File Naming

Converted files are saved with the same name as the original file, but with the new extension:
- Original: `photo.heic`
- Converted to JPG: `photo.jpg`
- Converted to PNG: `photo.png`

## Supported Formats

**Input:**
- `.heic` / `.HEIC` files

**Output:**
- `.jpg` (JPEG format with 95% quality)
- `.png` (PNG format with full quality)

## Notes

- When converting to JPG, images with transparency will have a white background automatically added
- When converting to PNG, transparency is preserved
- The original HEIC file is not modified or deleted
- If a file with the output name already exists, it will be overwritten

## Troubleshooting

**"Invalid File" error:**
- Ensure the file has a `.heic` extension
- Check that the file is not corrupted

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're using Python 3.7 or higher

**Drag and drop not working:**
- Try using the Browse button instead
- Reinstall tkinterdnd2: `pip install --upgrade tkinterdnd2`

## License

See LICENSE file :).

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

- Built with [Pillow](https://python-pillow.org/) for image processing
- HEIC support provided by [pillow-heif](https://github.com/bigcat88/pillow_heif)
- Drag and drop functionality via [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)
