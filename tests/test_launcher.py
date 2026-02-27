import unittest
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from launcher import LauncherGenerator

class TestLauncherGenerator(unittest.TestCase):
    def setUp(self):
        self.app_name = 'Test App'
        self.exe_path = '/path/to/app.exe'
        self.compat_path = '/home/user/.local/share/uwp_runner/compatdata/test_app'
        self.proton_path = '/home/user/.steam/steam/steamapps/common/Proton 8.0'
        self.generator = LauncherGenerator(self.app_name, self.exe_path, self.compat_path, self.proton_path)

    def tearDown(self):
        if os.path.exists(self.generator.launcher_dir):
            shutil.rmtree(self.generator.launcher_dir)

    def test_generate_script(self):
        path = self.generator.generate_script()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.access(path, os.X_OK))

        with open(path, 'r') as f:
            content = f.read()
            self.assertIn(f'STEAM_COMPAT_DATA_PATH="{self.compat_path}"', content)
            self.assertIn(f'"{self.proton_path}/proton" run "{self.exe_path}"', content)

if __name__ == '__main__':
    unittest.main()
