import unittest
import os
import shutil
import zipfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from extractor import Extractor

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.test_zip = 'tests/test_package.appx'
        self.extract_dir = 'tests/extracted_app'

        # Create a dummy zip file
        with zipfile.ZipFile(self.test_zip, 'w') as zip_ref:
            zip_ref.writestr('test_file.txt', 'This is a test file inside the package.')
            zip_ref.writestr('AppxManifest.xml', '<Package></Package>')

    def tearDown(self):
        if os.path.exists(self.test_zip):
            os.remove(self.test_zip)
        if os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir)

    def test_extract(self):
        extractor = Extractor(self.test_zip, self.extract_dir)
        result = extractor.extract()

        self.assertEqual(result, self.extract_dir)
        self.assertTrue(os.path.exists(os.path.join(self.extract_dir, 'test_file.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.extract_dir, 'AppxManifest.xml')))

    def test_cleanup(self):
        extractor = Extractor(self.test_zip, self.extract_dir)
        extractor.extract()
        self.assertTrue(os.path.exists(self.extract_dir))

        extractor.cleanup()
        self.assertFalse(os.path.exists(self.extract_dir))

if __name__ == '__main__':
    unittest.main()
