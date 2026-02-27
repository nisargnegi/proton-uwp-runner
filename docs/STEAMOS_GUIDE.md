# How to Run UWP Apps on SteamOS

This guide explains how to use the `uwp_tool.py` to attempt running UWP apps (including the Xbox App) on your Steam Deck or SteamOS device.

## Prerequisites

1.  **Switch to Desktop Mode:** Hold the Power button > Switch to Desktop.
2.  **Enable Developer Mode (Optional but Recommended):** In Settings > System > Developer Mode, ensure this is enabled.
3.  **Install Python:** SteamOS usually comes with Python, but verify by running `python3 --version` in Konsole.

## Step 1: Obtain the .appx / .msix Bundle

You need the `.appx` or `.msix` file of the application you want to run.
- For free/opensource UWP apps: Download directly from GitHub releases or the developer's site.
- For Xbox App / Game Pass: You may need to use a tool or site (like `store.rg-adguard.net`) to grab the `.appx` link directly from the Microsoft Store, or extract it from a Windows PC.

## Step 2: Extract and Install

Open Konsole (terminal) in the directory where you cloned this repository.

Run:
```bash
python3 uwp_tool.py install /path/to/your_app.appx
```

This will:
- Extract the package to `~/.local/share/uwp_runner/apps/`.
- Parse the manifest to find the main executable.
- Create a launch script using your installed Proton version.

## Step 3: Run the App

Run:
```bash
python3 uwp_tool.py run <app_name>
```

Or, execute the generated script directly (usually located in `~/.local/share/uwp_runner/launchers/`).

## Step 4: Adding to Steam (Optional)

1.  Open Steam in Desktop Mode.
2.  Games > "Add a Non-Steam Game to My Library..."
3.  Browse and select the generated launcher script (you might need to select "All Files" to see `.sh` files).
4.  Return to Gaming Mode and launch it from your Library.

## Troubleshooting

- **"File not found"**: Ensure the path to the `.appx` file is correct and absolute.
- **"Proton not found"**: Make sure you have installed a version of Proton (e.g., Proton 8.0 or Experimental) via Steam.
- **App crashes immediately**: This is common for complex UWP apps. Check the terminal output for Wine/Proton errors.
