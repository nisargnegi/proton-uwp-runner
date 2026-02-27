# UWP Runner for SteamOS

A tool to run Universal Windows Platform (UWP) applications, including the Xbox App, on SteamOS by leveraging the native Proton compatibility layer.

## Overview
This tool allows you to:
1.  **Extract** `.appx` or `.msix` packages (standard UWP format).
2.  **Parse** the `AppxManifest.xml` to identify the executable.
3.  **Generate** a launch script that runs the application using Steam's Proton environment.

## Usage

### Prerequisites
- SteamOS (or a Linux distribution with Steam installed).
- Proton installed via Steam (Proton Experimental or 8.0+ recommended).

### Installation
Clone this repository and run the setup script (coming soon).

### Commands
- `python3 uwp_tool.py scan` - Scans for installed Proton versions.
- `python3 uwp_tool.py install <path_to_appx>` - Installs a UWP app.
- `python3 uwp_tool.py list` - Lists installed UWP apps.
- `python3 uwp_tool.py run <app_name>` - Runs an installed app.

## Disclaimer
Running UWP apps, especially those with heavy DRM like Xbox Game Pass games, is experimental. This tool provides the *mechanism* to run them, but cannot guarantee that all games or services will function correctly due to Wine/Proton limitations with Windows Services.
