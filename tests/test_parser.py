import unittest
import os
import sys

# Add src to the path so we can import ManifestParser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from manifest_parser import ManifestParser

class TestManifestParser(unittest.TestCase):
    def setUp(self):
        self.sample_xml = 'tests/sample_manifest.xml'
        with open(self.sample_xml, 'w') as f:
            f.write("""<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10" xmlns:mp="http://schemas.microsoft.com/appx/2014/phone/manifest" xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10" IgnorableNamespaces="uap mp">
  <Identity Name="Microsoft.XboxApp" Publisher="CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US" Version="48.83.6001.0" ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>Xbox</DisplayName>
    <PublisherDisplayName>Microsoft Corporation</PublisherDisplayName>
    <Logo>Images\StoreLogo.png</Logo>
  </Properties>
  <Applications>
    <Application Id="App" Executable="bin\XboxApp.exe" EntryPoint="XboxApp.App">
      <uap:VisualElements DisplayName="Xbox" Description="Xbox App" BackgroundColor="transparent" Square150x150Logo="Images\Square150x150Logo.png" Square44x44Logo="Images\Square44x44Logo.png">
      </uap:VisualElements>
    </Application>
  </Applications>
</Package>""")

    def tearDown(self):
        if os.path.exists(self.sample_xml):
            os.remove(self.sample_xml)

    def test_get_identity(self):
        parser = ManifestParser(self.sample_xml)
        identity = parser.get_identity()
        self.assertEqual(identity['Name'], 'Microsoft.XboxApp')
        self.assertEqual(identity['Version'], '48.83.6001.0')

    def test_get_executable(self):
        parser = ManifestParser(self.sample_xml)
        exe = parser.get_executable()
        # Should now return forward slash path
        self.assertEqual(exe, 'bin/XboxApp.exe')

    def test_get_display_name(self):
        parser = ManifestParser(self.sample_xml)
        name = parser.get_display_name()
        self.assertEqual(name, 'Xbox')

if __name__ == '__main__':
    unittest.main()
