# Laptop Transfer Guide - Complete Migration Plan

**Created:** November 8, 2025
**Purpose:** Transfer Sentinel and development environment to new laptop
**Method:** USB drive + OneDrive sync
**Constraint:** Both laptops must have monitoring software installed

---

## Overview

This guide provides step-by-step instructions for transferring your complete development environment from your current laptop to a new one, ensuring nothing is lost and everything works correctly.

**Timeline:** 1-2 hours total transfer time
**Required:** 16GB USB drive, both laptops with monitoring installed

---

## PHASE 1: PREPARATION (Current Laptop - Do This Now)

### 1A. Run Inventory Script

Run the automated inventory script (created below) to document:
- All installed applications
- Python packages
- VS Code extensions
- Sentinel configuration
- Database files
- Git configuration

**Command:**
```bash
python Laptop_Transfer_Inventory.py
```

**Output:** Creates `Transfer_Inventory_Report.txt` with everything documented

### 1B. Create Backup Package

Run the backup script (created below) to copy critical files to USB:

**Command:**
```bash
python Create_Transfer_Package.py
```

**What This Does:**
- Backs up sentinel.db database
- Exports config.py (with API keys)
- Copies all Python requirements
- Exports VS Code settings
- Creates application list
- Packages everything into `Sentinel_Transfer_Package/`

### 1C. Manual Verification Checklist

Before leaving current laptop, verify these are backed up:

- [ ] Sentinel folder (check OneDrive sync status)
- [ ] sentinel.db database file
- [ ] config.py with API keys (CRITICAL!)
- [ ] Browser bookmarks (export to HTML)
- [ ] Git credentials (username/email)
- [ ] Any documents outside OneDrive

---

## PHASE 2: EXECUTION (New Laptop - With Monitoring Installed)

### 2A. Initial Setup (Before File Transfer)

**On New Laptop:**

1. Sign into Windows with same Microsoft account
2. Sign into OneDrive (this will start syncing Sentinel)
3. Install Python 3.12 from python.org
4. Install Git from git-scm.com
5. Install VS Code from code.visualstudio.com

**IMPORTANT:** Let OneDrive fully sync before proceeding. Check:
- Bottom-right OneDrive icon shows green checkmark
- `C:\Users\wjcor\OneDrive\Desktop\Sentinel` folder exists

### 2B. Restore from USB

1. **Insert USB drive** into new laptop

2. **Copy Transfer Package:**
   ```
   USB:\Sentinel_Transfer_Package\
       → C:\Users\wjcor\OneDrive\Desktop\Sentinel_Backup\
   ```

3. **Restore Database:**
   ```
   Copy sentinel.db from backup to:
   C:\Users\wjcor\OneDrive\Desktop\Sentinel\sentinel.db
   ```

4. **Restore Config:**
   ```
   Copy config.py from backup to:
   C:\Users\wjcor\OneDrive\Desktop\Sentinel\config.py
   ```

5. **Verify API Keys:**
   - Open config.py in Notepad
   - Confirm APCA_API_KEY_ID and APCA_API_SECRET_KEY are present
   - DO NOT share these with anyone

### 2C. Python Environment Setup

**Open Command Prompt in Sentinel folder:**

```bash
cd C:\Users\wjcor\OneDrive\Desktop\Sentinel

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install packages from USB backup
pip install -r Sentinel_Transfer_Package\requirements.txt
```

**This installs all Python packages you need.**

### 2D. VS Code Setup

1. **Open VS Code**
2. **Install Extensions:**
   - Press Ctrl+Shift+X (Extensions panel)
   - Search and install:
     - Python (Microsoft)
     - Pylance (Microsoft)
     - Claude Code (Anthropic)
     - GitLens (optional but recommended)

3. **Open Sentinel Folder:**
   - File → Open Folder
   - Select `C:\Users\wjcor\OneDrive\Desktop\Sentinel`

4. **Select Python Interpreter:**
   - Ctrl+Shift+P → "Python: Select Interpreter"
   - Choose `.\venv\Scripts\python.exe`

5. **Configure Claude Code:**
   - Follow extension prompts to sign in
   - Verify it connects to Anthropic API

### 2E. Git Configuration

**In VS Code Terminal (or Command Prompt):**

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Test Git connection to GitHub
git status
```

**If you need to re-authenticate GitHub:**
- Git will prompt when you try to push
- Use Personal Access Token (not password)

---

## PHASE 3: VERIFICATION

### 3A. Test Sentinel

**Run this verification script:**

```bash
python test_new_laptop_setup.py
```

**What This Tests:**
- Database connection works
- Alpaca API keys valid
- All departments can import
- Trading connection active
- Mode Manager operational

### 3B. Manual Tests

**Test each component:**

1. **Control Panel:**
   ```bash
   python sentinel_control_panel.py
   ```
   - Should launch without errors
   - Try viewing dashboard (option 4)

2. **Database Integrity:**
   ```bash
   python test_database_consolidation.py
   ```
   - Verify all 24 tables present
   - Check row counts match old laptop

3. **Trading Connection:**
   ```bash
   python test_price_api_fix.py
   ```
   - Should fetch real-time prices
   - Confirms Alpaca connection works

### 3C. Final Checklist

- [ ] Sentinel Control Panel launches
- [ ] Dashboard shows correct portfolio ($98.5K equity)
- [ ] Can view 22 current positions
- [ ] Python virtual environment activated
- [ ] Git shows correct branch (main)
- [ ] VS Code recognizes Python interpreter
- [ ] Claude Code extension working
- [ ] Alpaca API connection successful

---

## TROUBLESHOOTING

### Problem: OneDrive Not Syncing

**Solution:**
- Check OneDrive is signed in (system tray icon)
- Right-click OneDrive → Settings → Account → Choose folders
- Ensure Desktop is checked

### Problem: Python Packages Won't Install

**Solution:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Then retry requirements
pip install -r requirements.txt
```

### Problem: Alpaca Connection Fails

**Solution:**
- Verify config.py has correct API keys
- Check keys at: alpaca.markets (Account → API Keys)
- Confirm using PAPER trading keys (not live)

### Problem: Database Missing Tables

**Solution:**
```bash
# Run migration script
python migrate_databases.py

# Verify tables
python analyze_databases.py
```

### Problem: Git Authentication Fails

**Solution:**
- Use Personal Access Token (not password)
- GitHub Settings → Developer Settings → Personal Access Tokens
- Generate new token with 'repo' scope

---

## DATA THAT DOES NOT TRANSFER

These will need manual recreation:

1. **Pinned Taskbar Items** - Re-pin manually
2. **Desktop Shortcuts** - Recreate as needed
3. **Browser Data** - Sign into Chrome/Edge to sync
4. **Scheduled Tasks** - None currently, but note for future
5. **Environment Variables** - None needed for Sentinel

---

## MONITORING SOFTWARE NOTES

**Safe Activities (Monitoring Will See But Is Expected):**
- Copying files from USB to laptop
- Installing Python, Git, VS Code
- Downloading packages from PyPI (pip install)
- Syncing files via OneDrive
- Connecting to GitHub
- Connecting to Alpaca API

**All of these are legitimate development activities.**

**Your PO confirmed:**
- Monitoring installed on new laptop FIRST
- Then data transfer is permitted
- Old laptop disposed after confirmation

---

## POST-TRANSFER CLEANUP (Old Laptop)

**After Verifying New Laptop Works:**

1. **Verify Everything Transferred:**
   - Compare file counts
   - Test Sentinel on new laptop thoroughly
   - Run at least 1 trading cycle successfully

2. **Notify PO:**
   - Confirm new laptop operational
   - Schedule old laptop disposal
   - Get disposal confirmation requirements

3. **Wipe Old Laptop (After PO Approval):**
   - Settings → Update & Security → Recovery
   - "Reset this PC" → "Remove everything"
   - DO NOT do this until PO confirms disposal plan

---

## ESTIMATED TIMELINE

**Preparation (Current Laptop):** 30 minutes
- Run inventory script: 5 min
- Create backup package: 10 min
- Manual verification: 15 min

**New Laptop Setup:** 60-90 minutes
- Initial installs: 30 min
- Python environment: 15 min
- VS Code configuration: 15 min
- File restoration: 10 min
- Verification: 20 min

**Total:** ~2 hours from start to fully operational new laptop

---

## SUPPORT

**If You Get Stuck:**
- Read error messages carefully
- Check troubleshooting section above
- Use Claude Code in VS Code for help
- All scripts include error messages to guide you

**Critical Files Locations:**
- Database: `C:\Users\wjcor\OneDrive\Desktop\Sentinel\sentinel.db`
- Config: `C:\Users\wjcor\OneDrive\Desktop\Sentinel\config.py`
- Backup: USB drive or `Sentinel_Backup\` folder

---

**Document Version:** 1.0
**Last Updated:** November 8, 2025
**Status:** Ready for use when new laptop arrives
