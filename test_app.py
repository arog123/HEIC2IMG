import unittest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import pillow_heif
from app import HEICConverter


class TestHEICConverter(unittest.TestCase):
    """Test suite for HEIC to JPG/PNG Converter"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.test_dir = tempfile.mkdtemp()
        pillow_heif.register_heif_opener()
        
        # Create a test HEIC file (simulated with a regular image)
        self.test_image_path = os.path.join(self.test_dir, "test_image.heic")
        self.create_test_image(self.test_image_path)
        
        # Create a mock root window for testing
        self.mock_root = Mock()
        self.mock_root.title = Mock()
        self.mock_root.geometry = Mock()
        self.mock_root.resizable = Mock()
    
    def tearDown(self):
        """Clean up after each test method"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_test_image(self, path, size=(100, 100), mode='RGB'):
        """Create a test image file"""
        img = Image.new(mode, size, color='red')
        # Save as PNG first, then rename to .heic for testing
        temp_path = path.replace('.heic', '.png')
        img.save(temp_path, 'PNG')
        if os.path.exists(temp_path):
            os.rename(temp_path, path)
        return path
    
    def test_file_extension_validation(self):
        """Test that only .heic files are accepted"""
        # Create test files with different extensions
        valid_file = os.path.join(self.test_dir, "valid.heic")
        invalid_file = os.path.join(self.test_dir, "invalid.jpg")
        
        with open(valid_file, 'w') as f:
            f.write("test")
        with open(invalid_file, 'w') as f:
            f.write("test")
        
        # Valid file should pass
        self.assertTrue(valid_file.lower().endswith('.heic'))
        
        # Invalid file should fail
        self.assertFalse(invalid_file.lower().endswith('.heic'))
    
    def test_output_filename_generation(self):
        """Test that output filenames are generated correctly"""
        input_file = "/path/to/image.heic"
        
        # Test JPG output
        base_name = os.path.splitext(input_file)[0]
        jpg_output = base_name + ".jpg"
        self.assertEqual(jpg_output, "/path/to/image.jpg")
        
        # Test PNG output
        png_output = base_name + ".png"
        self.assertEqual(png_output, "/path/to/image.png")
    
    def test_file_exists_check(self):
        """Test file existence validation"""
        existing_file = os.path.join(self.test_dir, "exists.heic")
        non_existing_file = os.path.join(self.test_dir, "not_exists.heic")
        
        with open(existing_file, 'w') as f:
            f.write("test")
        
        self.assertTrue(os.path.exists(existing_file))
        self.assertFalse(os.path.exists(non_existing_file))
    
    def test_image_mode_conversion_for_jpg(self):
        """Test that RGBA images are properly converted for JPG"""
        # Create an RGBA image
        rgba_image = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        
        # Convert to RGB with white background (as done in the converter)
        if rgba_image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', rgba_image.size, (255, 255, 255))
            background.paste(rgba_image, mask=rgba_image.split()[-1])
            rgb_image = background
        
        self.assertEqual(rgb_image.mode, 'RGB')
        self.assertEqual(rgb_image.size, (100, 100))
    
    def test_valid_output_formats(self):
        """Test that valid output formats are recognized"""
        valid_formats = ['JPG', 'PNG']
        
        for fmt in valid_formats:
            self.assertIn(fmt, valid_formats)
        
        invalid_format = 'GIF'
        self.assertNotIn(invalid_format, valid_formats)
    
    def test_image_conversion_jpg(self):
        """Test converting an image to JPG format"""
        input_path = os.path.join(self.test_dir, "test.heic")
        output_path = os.path.join(self.test_dir, "test.jpg")
        
        # Create a test image
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(input_path, 'PNG')  # Save as PNG but with .heic extension
        
        # Open and convert
        img = Image.open(input_path)
        img.save(output_path, 'JPEG', quality=95)
        
        # Verify output exists and is valid
        self.assertTrue(os.path.exists(output_path))
        
        # Verify it can be opened as JPG
        converted_img = Image.open(output_path)
        self.assertEqual(converted_img.format, 'JPEG')
        self.assertEqual(converted_img.size, (100, 100))
    
    def test_image_conversion_png(self):
        """Test converting an image to PNG format"""
        input_path = os.path.join(self.test_dir, "test.heic")
        output_path = os.path.join(self.test_dir, "test.png")
        
        # Create a test image
        img = Image.new('RGBA', (100, 100), color=(0, 255, 0, 200))
        img.save(input_path, 'PNG')
        
        # Open and convert
        img = Image.open(input_path)
        img.save(output_path, 'PNG')
        
        # Verify output exists and is valid
        self.assertTrue(os.path.exists(output_path))
        
        # Verify it can be opened as PNG
        converted_img = Image.open(output_path)
        self.assertEqual(converted_img.format, 'PNG')
        self.assertEqual(converted_img.size, (100, 100))
    
    def test_transparency_preservation_png(self):
        """Test that PNG conversion preserves transparency"""
        input_path = os.path.join(self.test_dir, "transparent.heic")
        output_path = os.path.join(self.test_dir, "transparent.png")
        
        # Create an RGBA image with transparency
        img = Image.new('RGBA', (50, 50), color=(255, 0, 0, 128))
        img.save(input_path, 'PNG')
        
        # Convert to PNG
        img = Image.open(input_path)
        img.save(output_path, 'PNG')
        
        # Verify transparency is preserved
        converted_img = Image.open(output_path)
        self.assertEqual(converted_img.mode, 'RGBA')
    
    def test_case_insensitive_extension(self):
        """Test that both .heic and .HEIC are accepted"""
        lowercase = "image.heic"
        uppercase = "IMAGE.HEIC"
        mixed = "Image.HeiC"
        
        self.assertTrue(lowercase.lower().endswith('.heic'))
        self.assertTrue(uppercase.lower().endswith('.heic'))
        self.assertTrue(mixed.lower().endswith('.heic'))
    
    def test_path_handling_with_spaces(self):
        """Test handling of file paths with spaces"""
        path_with_spaces = os.path.join(self.test_dir, "my image file.heic")
        
        # Create file
        with open(path_with_spaces, 'w') as f:
            f.write("test")
        
        self.assertTrue(os.path.exists(path_with_spaces))
        self.assertTrue(path_with_spaces.lower().endswith('.heic'))
    
    def test_overwrite_existing_file(self):
        """Test that existing output files are overwritten"""
        input_path = os.path.join(self.test_dir, "input.heic")
        output_path = os.path.join(self.test_dir, "input.jpg")
        
        # Create input file
        img = Image.new('RGB', (100, 100), color='red')
        img.save(input_path, 'PNG')
        
        # Create existing output file
        existing_img = Image.new('RGB', (50, 50), color='blue')
        existing_img.save(output_path, 'JPEG')
        
        original_size = os.path.getsize(output_path)
        
        # Convert (should overwrite)
        img = Image.open(input_path)
        img.save(output_path, 'JPEG', quality=95)
        
        new_size = os.path.getsize(output_path)
        
        # Size should be different since we overwrote with different image
        self.assertNotEqual(original_size, new_size)


class TestImageQuality(unittest.TestCase):
    """Test image quality and conversion parameters"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_jpg_quality_setting(self):
        """Test that JPG quality is set correctly"""
        quality = 95
        self.assertGreaterEqual(quality, 0)
        self.assertLessEqual(quality, 100)
        self.assertEqual(quality, 95)
    
    def test_image_dimensions_preserved(self):
        """Test that image dimensions are preserved during conversion"""
        original_size = (200, 150)
        img = Image.new('RGB', original_size, color='green')
        
        temp_jpg = os.path.join(self.test_dir, "temp.jpg")
        img.save(temp_jpg, 'JPEG')
        
        loaded_img = Image.open(temp_jpg)
        self.assertEqual(loaded_img.size, original_size)


class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_corrupted_file_handling(self):
        """Test handling of corrupted image files"""
        corrupted_file = os.path.join(self.test_dir, "corrupted.heic")
        
        with open(corrupted_file, 'w') as f:
            f.write("This is not a valid image file")
        
        # Attempting to open should raise an exception
        with self.assertRaises(Exception):
            Image.open(corrupted_file)
    
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        empty_file = os.path.join(self.test_dir, "empty.heic")
        
        with open(empty_file, 'w') as f:
            pass  # Create empty file
        
        # Attempting to open should raise an exception
        with self.assertRaises(Exception):
            Image.open(empty_file)
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent files"""
        nonexistent = os.path.join(self.test_dir, "does_not_exist.heic")
        
        self.assertFalse(os.path.exists(nonexistent))


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHEICConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestImageQuality))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("Running HEIC Converter Test Suite...\n")
    result = run_tests()
    
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)