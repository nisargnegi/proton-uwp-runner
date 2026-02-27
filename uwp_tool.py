import argparse
import sys
import os
import shutil
import zipfile
import stat

# Local imports
# Adjust path to include src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from manifest_parser import ManifestParser
from extractor import Extractor
from proton_manager import ProtonManager
from launcher import LauncherGenerator

INSTALL_BASE = os.path.expanduser('~/.local/share/uwp_runner/apps')
LAUNCHER_BASE = os.path.expanduser('~/.local/share/uwp_runner/launchers')

def ensure_dirs():
    if not os.path.exists(INSTALL_BASE):
        os.makedirs(INSTALL_BASE)
    if not os.path.exists(LAUNCHER_BASE):
        os.makedirs(LAUNCHER_BASE)

def scan_proton():
    pm = ProtonManager()
    print("Scanning for Proton installations...")
    if not pm.proton_versions:
        print("No Proton installations found! Ensure Steam and Proton are installed.")
        return

    for version in pm.proton_versions:
        print(f"Found: {version}")

    latest = pm.get_latest_proton()
    if latest:
        print(f"\nLatest detected: {latest}")

def install_app(appx_path):
    ensure_dirs()
    if not os.path.exists(appx_path):
        print(f"Error: File not found: {appx_path}")
        return

    # Basic check for .appxbundle
    if appx_path.lower().endswith('.appxbundle'):
        print("\n[WARNING] You provided an .appxbundle file.")
        print("This tool currently supports installing a single .appx architecture package.")
        print("Please extract the .appxbundle manually (it is a zip file) and find the .appx file")
        print("corresponding to your architecture (usually x64) inside it.")
        print("Then run this command again with that specific .appx file.")
        return

    print(f"Analyzing {appx_path}...")

    # Create a temporary extraction dir
    temp_dir = os.path.expanduser('~/.local/share/uwp_runner/temp_extract')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    print("Extracting package (this may take a while)...")
    extractor = Extractor(appx_path, temp_dir)
    extracted_path = extractor.extract()

    if not extracted_path:
        print("Extraction failed.")
        return

    # Parse Manifest
    manifest_path = os.path.join(extracted_path, 'AppxManifest.xml')
    if not os.path.exists(manifest_path):
        print("Error: AppxManifest.xml not found in package.")
        shutil.rmtree(temp_dir)
        return

    try:
        parser = ManifestParser(manifest_path)
        identity = parser.get_identity()
        exe_name = parser.get_executable()
        display_name = parser.get_display_name()
    except Exception as e:
        print(f"Error parsing manifest: {e}")
        shutil.rmtree(temp_dir)
        return

    if not identity or not exe_name:
        print("Error: Could not parse Identity or Executable from manifest.")
        shutil.rmtree(temp_dir)
        return

    app_id = identity.get('Name', 'UnknownApp')
    print(f"Detected App: {display_name} ({app_id})")
    print(f"Executable: {exe_name}")

    # Move to permanent location
    final_dir = os.path.join(INSTALL_BASE, app_id)
    if os.path.exists(final_dir):
        print(f"App {app_id} already installed. Overwriting...")
        shutil.rmtree(final_dir)

    print(f"Installing to {final_dir}...")
    shutil.move(extracted_path, final_dir)

    # Set up Proton Compat Data
    pm = ProtonManager()
    proton_path = pm.get_latest_proton()

    if not proton_path:
        print("Error: No Proton installation found. Cannot generate launcher.")
        return

    compat_path = pm.create_compat_data(app_id)
    print(f"Created compatdata at {compat_path}")

    # Generate Launcher
    exe_full_path = os.path.join(final_dir, exe_name)

    # Ensure exe is executable
    if os.path.exists(exe_full_path):
        st = os.stat(exe_full_path)
        os.chmod(exe_full_path, st.st_mode | stat.S_IEXEC)
    else:
        print(f"Warning: Executable {exe_name} not found in extracted files.")

    launcher = LauncherGenerator(display_name, exe_full_path, compat_path, proton_path)
    script_path = launcher.generate_script()

    print(f"\nSuccess! Installed {display_name}")
    print(f"Launcher created at: {script_path}")
    print(f"To run: python3 uwp_tool.py run \"{display_name}\"")

def list_apps():
    ensure_dirs()
    files = os.listdir(LAUNCHER_BASE)
    if not files:
        print("No apps installed.")
        return

    print("Installed Apps (Launchers):")
    for f in files:
        if f.endswith(".sh"):
            print(f" - {f.replace('.sh', '').replace('_', ' ')}")

def run_app(app_name):
    ensure_dirs()
    # Try exact match or match based on sanitized name
    safe_name = "".join(c for c in app_name if c.isalnum() or c in (' ', '.', '_', '-')).strip().replace(" ", "_")
    script_path = os.path.join(LAUNCHER_BASE, f"{safe_name}.sh")

    if not os.path.exists(script_path):
        # Try finding it loosely
        found_script = None
        for f in os.listdir(LAUNCHER_BASE):
            if app_name.lower() in f.lower():
                found_script = os.path.join(LAUNCHER_BASE, f)
                break

        if found_script:
            script_path = found_script
        else:
            print(f"Launcher for '{app_name}' not found.")
            return

    print(f"Launching {script_path}...")
    # Use os.system to execute the script
    os.system(f'"{script_path}"')

def main():
    parser = argparse.ArgumentParser(description="UWP Runner for SteamOS")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Scan command
    subparsers.add_parser('scan', help='Scan for Proton versions')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install a UWP .appx/.msix file')
    install_parser.add_argument('path', help='Path to the .appx file')

    # List command
    subparsers.add_parser('list', help='List installed apps')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run an installed app')
    run_parser.add_argument('name', help='Name of the app (as shown in list)')

    args = parser.parse_args()

    if args.command == 'scan':
        scan_proton()
    elif args.command == 'install':
        install_app(args.path)
    elif args.command == 'list':
        list_apps()
    elif args.command == 'run':
        run_app(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
