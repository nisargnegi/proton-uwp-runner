import os
import glob
import shutil

class ProtonManager:
    def __init__(self):
        """
        Initializes the ProtonManager.
        """
        self.proton_paths = [
            os.path.expanduser('~/.steam/steam/steamapps/common/Proton*'),
            os.path.expanduser('~/.local/share/Steam/steamapps/common/Proton*')
        ]
        self.proton_versions = []
        self.scan_for_proton()

    def scan_for_proton(self):
        """
        Scans for installed Proton versions in standard Steam locations.
        Populates self.proton_versions with the paths to valid Proton installations.
        """
        self.proton_versions = [] # Reset before scanning
        for path_pattern in self.proton_paths:
            found = glob.glob(path_pattern)
            for path in found:
                # Check if it actually looks like a Proton dir (has a 'proton' script)
                if os.path.exists(os.path.join(path, 'proton')):
                     self.proton_versions.append(path)

        # Simple sort, puts 'Proton 8.0' before 'Proton 7.0' etc.
        # This is a heuristic, not a perfect semantic version sort.
        self.proton_versions.sort(reverse=True)

    def get_latest_proton(self):
        """
        Returns the path to the latest found Proton version.
        Returns None if no Proton versions are found.
        """
        if not self.proton_versions:
            return None
        return self.proton_versions[0]

    def create_compat_data(self, app_id):
        """
        Creates a compatdata directory structure for a new app.
        app_id: A unique identifier for the app (e.g., package name).
        Returns the path to the compatdata directory.
        """
        compat_path = os.path.expanduser(f'~/.local/share/uwp_runner/compatdata/{app_id}')
        pfx_path = os.path.join(compat_path, 'pfx')

        if not os.path.exists(pfx_path):
            os.makedirs(pfx_path)

        return compat_path
