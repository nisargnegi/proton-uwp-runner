import zipfile
import os
import shutil

class Extractor:
    def __init__(self, package_path, install_dir):
        """
        Initializes the Extractor with the package path and the target installation directory.
        """
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Package file not found: {package_path}")
        self.package_path = package_path
        self.install_dir = install_dir

    def extract(self):
        """
        Extracts the contents of the package to the installation directory.
        Returns the path to the extracted directory.
        """
        if not os.path.exists(self.install_dir):
            os.makedirs(self.install_dir)

        try:
            with zipfile.ZipFile(self.package_path, 'r') as zip_ref:
                zip_ref.extractall(self.install_dir)
            return self.install_dir
        except zipfile.BadZipFile:
            print(f"Error: {self.package_path} is not a valid zip file.")
            return None

    def cleanup(self):
        """
        Removes the extracted directory (useful for failed installations).
        """
        if os.path.exists(self.install_dir):
            shutil.rmtree(self.install_dir)
