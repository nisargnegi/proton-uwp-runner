import xml.etree.ElementTree as ET
import os

class ManifestParser:
    def __init__(self, manifest_path):
        """
        Initializes the ManifestParser with the path to the AppxManifest.xml file.
        """
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
        self.manifest_path = manifest_path
        self.tree = ET.parse(manifest_path)
        self.root = self.tree.getroot()
        # Define namespaces commonly used in AppxManifests
        self.namespaces = {
            'win10': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10',
            'uap': 'http://schemas.microsoft.com/appx/manifest/uap/windows10',
            'mp': 'http://schemas.microsoft.com/appx/2014/phone/manifest',
            'default': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10' # Fallback default
        }

    def get_identity(self):
        """
        Extracts the Identity Name and Publisher from the manifest.
        Returns a dictionary: {'Name': '...', 'Publisher': '...'}
        """
        identity = self.root.find('win10:Identity', self.namespaces)
        if identity is None:
            # Fallback for simpler manifests without explicit win10 namespace on root
             identity = self.root.find('{http://schemas.microsoft.com/appx/manifest/foundation/windows10}Identity')

        if identity is not None:
            return {
                'Name': identity.get('Name'),
                'Publisher': identity.get('Publisher'),
                'Version': identity.get('Version')
            }
        return None

    def get_executable(self):
        """
        Finds the executable path defined in the <Application> tag.
        Returns the executable filename/path.
        """
        applications = self.root.find('win10:Applications', self.namespaces)
        if applications is None:
             applications = self.root.find('{http://schemas.microsoft.com/appx/manifest/foundation/windows10}Applications')

        if applications is not None:
            # Assumes single application package for now, or takes the first one
            app = applications.find('win10:Application', self.namespaces)
            if app is None:
                app = applications.find('{http://schemas.microsoft.com/appx/manifest/foundation/windows10}Application')

            if app is not None:
                exe_path = app.get('Executable')
                if exe_path:
                    # Windows paths use backslashes, convert to forward slashes for Linux
                    return exe_path.replace('\\', '/')

        return None

    def get_display_name(self):
         """
         Tries to get the display name from VisualElements or Properties.
         """
         # Try Properties first
         props = self.root.find('win10:Properties', self.namespaces)
         if props:
             display_name = props.find('win10:DisplayName', self.namespaces)
             if display_name is not None:
                 return display_name.text

         # Try Application VisualElements
         applications = self.root.find('win10:Applications', self.namespaces)
         if applications:
             app = applications.find('win10:Application', self.namespaces)
             if app:
                 visuals = app.find('uap:VisualElements', self.namespaces)
                 if visuals:
                     return visuals.get('DisplayName')
         return "Unknown App"
