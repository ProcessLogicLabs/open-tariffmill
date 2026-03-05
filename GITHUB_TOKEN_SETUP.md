# TariffMill GitHub Token Setup Guide

## Overview

This guide explains how to set up the GitHub Personal Access Token for TariffMill authentication. This enables all domain users to automatically fetch the user list from GitHub, ensuring consistent access to the Admin Panel across all workstations.

## Why This Is Needed

TariffMill loads `auth_users.json` from GitHub to manage user authentication. Without the token:
- New domain users see an empty user list in the Admin Panel
- The "Restricted Access" warning appears even for admin users
- Each user would need their own local copy of the auth file

With the token properly configured:
- ✅ All users automatically get the latest user list from GitHub
- ✅ User updates are instant across all workstations
- ✅ Works consistently for all domain users

---

## Step 1: Generate GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens/new?scopes=repo

2. Configure the token:
   - **Note**: `TariffMill Auth File Access`
   - **Expiration**: Choose `No expiration` or `1 year`
   - **Scope**: Ensure `repo` (Full control of private repositories) is **checked**
     - This is required to access the private `ProcessLogicLabs/TariffMill` repository

3. Click **Generate token**

4. **CRITICAL**: Copy the token immediately (it starts with `ghp_`)
   - ⚠️ You won't be able to see it again after leaving this page!
   - Save it temporarily in a secure location

---

## Step 2: Set System-Wide Environment Variable

**Important**: This must be set as a **System** variable (not User variable) so all domain users can access it.

### On Windows Server or Deployment Machine:

1. Press `Win + X` → Select **System**

2. Click **Advanced system settings** (on the right side panel)

3. Click the **Environment Variables...** button

4. In the **System variables** section (bottom half, NOT User variables):
   - Click **New...**
   - Variable name: `TARIFFMILL_GITHUB_TOKEN`
   - Variable value: `ghp_your_actual_token_here` (paste the token you copied)
   - Click **OK**

5. Click **OK** on all dialogs to save

### Screenshot of Correct Location:
```
┌─────────────────────────────────────┐
│  User variables for [Username]     │  ← NOT here
│  [...]                              │
├─────────────────────────────────────┤
│  System variables                   │  ← SET HERE
│  ┌─────────────────────────────┐   │
│  │ TARIFFMILL_GITHUB_TOKEN     │   │
│  │ ghp_xxxxxxxxxxxxxxxxxxxx    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## Step 3: Restart and Test

1. **Restart any running TariffMill instances**
   - Environment variables only load when the application starts
   - If the app is running, close it completely and reopen

2. **Open TariffMill**

3. **Press `Ctrl+Shift+A`** to open the Admin Panel

4. **Check User Management tab**
   - Should now show all users from GitHub
   - No "Restricted Access" warning

---

## Step 4: Verify in Logs

Check the application log to confirm the token is working:

**Log Location:**
```
C:\Users\[USERNAME]\AppData\Local\TariffMill\tariffmill.log
```

**Look for these messages:**

✅ **Success:**
```
Successfully fetched remote user list
```

❌ **Failure (invalid token):**
```
GitHub authentication failed - check AUTH_GITHUB_TOKEN
```

❌ **Failure (repo not found):**
```
Auth config file not found in GitHub repo
```

---

## Troubleshooting

### Token Not Working?

1. **Verify token scope:**
   - Go to: https://github.com/settings/tokens
   - Find your token
   - Ensure `repo` scope is checked (not just `repo:status`)

2. **Check repository access:**
   - Verify the `ProcessLogicLabs/TariffMill` repository exists
   - Verify it contains `auth_users.json` file
   - Ensure your GitHub account has access to the repository

3. **Test environment variable:**
   - Open Command Prompt
   - Run: `echo %TARIFFMILL_GITHUB_TOKEN%`
   - Should display your token (not empty or "not defined")

4. **Restart computer:**
   - Sometimes system variables need a full computer restart to propagate
   - After restart, test again

### Still Not Working?

1. **Check token hasn't expired:**
   - Go to: https://github.com/settings/tokens
   - Verify token status (active, not expired)
   - Regenerate if needed

2. **Check network connectivity:**
   - Ensure workstation can reach `api.github.com`
   - Check firewall rules
   - Test with: `ping api.github.com`

3. **Check logs for detailed errors:**
   - Open `tariffmill.log`
   - Search for "auth" or "GitHub"
   - Look for specific error messages

---

## Alternative: Fallback to Local File

If you cannot use the GitHub token (network restrictions, security policy, etc.), you can use the fallback method:

1. Copy `auth_users.json` to the installation directory:
   ```
   C:\Program Files\TariffMill\auth_users.json
   ```

2. This file will be shared across all users

3. **Note**: You must manually update this file when users change

---

## Security Notes

- The GitHub token is stored as a system environment variable
- It's accessible to all users on the machine (by design, for shared access)
- The token only has `repo` scope (read-only access to TariffMill repository)
- Recommended: Use a service account or bot account for the token (not a personal account)
- Set expiration to 1 year and calendar reminder to rotate the token

---

## Summary

✅ **What you did:**
- Generated GitHub Personal Access Token
- Set `TARIFFMILL_GITHUB_TOKEN` as system-wide environment variable
- Restarted TariffMill

✅ **What happens now:**
- All domain users can access the admin panel user list
- User changes sync automatically from GitHub
- No more "Restricted Access" issues for authenticated admins

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the log file for specific errors
3. Verify all steps were completed correctly
4. Contact: admin@processlogiclabs.com

---

**Last Updated:** 2026-02-09
**Version:** 1.0
