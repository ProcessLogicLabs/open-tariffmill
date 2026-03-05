# TariffMill Auto-Update System

## Overview

TariffMill now features an intelligent auto-update system that checks for new releases on GitHub and allows users to install updates with minimal disruption.

## Features

### 1. Automatic Update Checking
- **Startup Checks**: Automatically checks for updates 2 seconds after launch (configurable)
- **Background Operation**: Runs in a separate thread to avoid blocking the UI
- **Smart Versioning**: Compares semantic versions (e.g., 0.97.57 vs 0.97.56)
- **GitHub Integration**: Uses GitHub Releases API to fetch latest version info

### 2. Silent Installation (New!)
- **One-Click Updates**: Users can download and install updates with a single click
- **Silent Mode**: Updates install automatically in the background without installer prompts
- **Interactive Mode**: Traditional installer with options (optional)
- **User Preference**: Configurable in Settings → Updates tab

### 3. User Controls
Located in **Settings → Updates**:

- ✅ **Check for updates when application starts** (default: ON)
  - When enabled, checks GitHub for new releases on startup
  - No personal data sent - only API version check

- ✅ **Install updates silently (recommended)** (default: ON)
  - When enabled, updates install automatically without showing installer dialogs
  - User data and settings are always preserved
  - Uncheck to see installer options during updates

## How It Works

### Update Check Flow
```
1. Application starts
2. After 2 seconds, background thread checks GitHub API
3. If new version found:
   - Show notification dialog with release notes
   - User chooses: Download & Install, View on GitHub, or Remind Me Later
4. If "Download & Install" clicked:
   - Download installer to temp directory with progress bar
   - Ask user to confirm installation
   - Install silently or interactively based on user preference
   - Close application and run installer
```

### Silent Installation

When silent mode is enabled:
- Installer runs with Inno Setup flags: `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS`
- No installer windows or prompts shown
- Application closes automatically
- Update installs in background
- User data preserved (database, templates, settings)
- Application can be relaunched after installation completes

### Interactive Installation

When silent mode is disabled:
- Traditional Inno Setup installer window shown
- User can choose installation directory
- User can choose desktop shortcut options
- Standard installation progress shown

## User Settings

### Enabling/Disabling Updates

1. Open **Settings** (Help → Preferences or Ctrl+,)
2. Go to **Updates** tab
3. Configure preferences:
   - **Check for updates when application starts**: ON/OFF
   - **Install updates silently (recommended)**: ON/OFF

### Manual Update Check

Users can manually check for updates:
- **Help** → **Check for Updates**
- Shows current version vs latest version
- Same download and install process

## Technical Details

### Files Modified
- `Tariffmill/tariffmill.py`:
  - Enhanced `_download_and_install_update()` method with silent install support
  - Added `silent_updates` user preference
  - Modified update dialog to respect user preferences

### Dependencies
- Uses standard library: `urllib.request`, `subprocess`, `tempfile`
- No additional packages required
- GitHub API (public, no authentication needed)

### Version Comparison
- Parses semantic version strings (e.g., "v0.97.57")
- Compares major.minor.patch as tuples
- Handles versions with or without 'v' prefix

### Download Process
- Downloads to system temp directory
- Shows progress bar (MB downloaded / total MB)
- Cancellable mid-download
- Verifies download completion before installation

### Installation Flags
Silent installation uses these Inno Setup command-line parameters:
- `/VERYSILENT`: No windows or message boxes shown
- `/SUPPRESSMSGBOXES`: Suppress message boxes
- `/NORESTART`: Don't restart computer after installation
- `/CLOSEAPPLICATIONS`: Automatically close running instances

## Benefits

### For Users
- **Effortless Updates**: One-click update process
- **No Interruption**: Silent mode requires no user interaction
- **Always Current**: Automatic checks ensure latest features and fixes
- **User Control**: Can disable or customize update behavior
- **Data Safety**: Settings and data always preserved

### For Developers
- **Reduced Support**: Users automatically get bug fixes
- **Better Adoption**: New features reach users faster
- **Telemetry-Free**: No tracking or analytics required
- **Simple Distribution**: Just publish GitHub release

## Troubleshooting

### Updates Not Checking
- Verify internet connection
- Check Settings → Updates → "Check for updates when application starts" is enabled
- Firewall may be blocking GitHub API (api.github.com)

### Silent Install Not Working
- Requires Windows platform
- Installer must be Inno Setup-based (.exe with Setup in name)
- User must have write permissions to installation directory

### Manual Installation
If automatic update fails:
1. Visit https://github.com/ProcessLogicLabs/TariffMill/releases
2. Download latest `TariffMill_Setup_X.X.X.exe`
3. Run installer manually
4. Data and settings will be preserved

## Future Enhancements

Potential improvements for future releases:
- [ ] Delta/patch updates (download only changed files)
- [ ] Scheduled updates (install at specific time)
- [ ] Rollback capability
- [ ] Update notifications in system tray
- [ ] Bandwidth throttling for downloads
- [ ] Offline update packages

## Security

- Updates only downloaded from official GitHub repository
- HTTPS used for all downloads
- No code execution during download (only after user confirmation)
- Installer signed by Process Logic Labs (when code signing certificate obtained)
- User data never transmitted during update process

## Changelog

### v0.97.57 (Current Release)
- ✨ Added silent update installation support
- ✨ Added user preference for silent vs interactive updates
- ✨ Enhanced update dialog with better messaging
- 🔧 Improved installer download progress display
- 📝 Added comprehensive update settings documentation

---

**Last Updated**: January 21, 2026
**TariffMill Version**: 0.97.57+
