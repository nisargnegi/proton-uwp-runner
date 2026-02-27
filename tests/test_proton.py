import unittest
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from proton_manager import ProtonManager

class TestProtonManager(unittest.TestCase):
    def setUp(self):
        # Create a mock Proton directory structure
        self.mock_steam_dir = os.path.expanduser('~/.local/share/Steam/steamapps/common')
        os.makedirs(os.path.join(self.mock_steam_dir, 'Proton 7.0'), exist_ok=True)
        os.makedirs(os.path.join(self.mock_steam_dir, 'Proton 8.0'), exist_ok=True)
        # Create dummy proton executable files
        with open(os.path.join(self.mock_steam_dir, 'Proton 7.0', 'proton'), 'w') as f:
            f.write('#!/bin/bash\necho "Proton 7.0"')
        with open(os.path.join(self.mock_steam_dir, 'Proton 8.0', 'proton'), 'w') as f:
            f.write('#!/bin/bash\necho "Proton 8.0"')

        self.manager = ProtonManager()

    def tearDown(self):
        # Clean up mock directories
        shutil.rmtree(os.path.join(self.mock_steam_dir, 'Proton 7.0'))
        shutil.rmtree(os.path.join(self.mock_steam_dir, 'Proton 8.0'))

        # Clean up compatdata
        compat_path = os.path.expanduser('~/.local/share/uwp_runner/compatdata')
        if os.path.exists(compat_path):
            shutil.rmtree(compat_path)

    def test_scan_for_proton(self):
        self.manager.scan_for_proton()
        self.assertTrue(len(self.manager.proton_versions) >= 2)

    def test_get_latest_proton(self):
        latest = self.manager.get_latest_proton()
        # Should pick Proton 8.0 because of reverse sort
        self.assertIn('Proton 8.0', latest)

    def test_create_compat_data(self):
        app_id = 'test_app_123'
        path = self.manager.create_compat_data(app_id)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'pfx')))

if __name__ == '__main__':
    unittest.main()
