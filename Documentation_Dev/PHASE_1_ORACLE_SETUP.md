# Phase 1: Oracle Cloud Account & VM Setup

**Estimated Time**: 2-4 hours (mostly waiting for account approval)
**Active Work**: ~30 minutes
**Prerequisites**: Email, phone number, internet connection

---

## Overview

By the end of Phase 1, you will have:
- ✅ Oracle Cloud free tier account (approved)
- ✅ Ubuntu 22.04 VM running (ARM architecture)
- ✅ SSH access configured
- ✅ Ability to connect via PuTTY from Windows

---

## Step 1: Create Oracle Cloud Account

### 1.1 Navigate to Oracle Cloud Free Tier

**Action**: Open web browser, go to:
```
https://www.oracle.com/cloud/free/
```

**What you'll see**: Oracle Cloud Free Tier landing page

**Click**: "Start for free" button (usually top-right or center)

---

### 1.2 Fill Out Account Information

**Form fields** (fill out completely):

| Field | What to Enter | Notes |
|-------|---------------|-------|
| **Email** | Your primary email | You'll receive verification here |
| **Country/Territory** | United States | Affects data center location |
| **First Name** | Your first name | |
| **Last Name** | Your last name | |
| **Company** | "Sentinel Corporation" or leave blank | Optional |

**Click**: "Verify my email"

---

### 1.3 Email Verification

**Check your email** (within 1-2 minutes):
- From: Oracle Cloud
- Subject: "Verify your email address"
- **Click** the verification link

**Browser will open**: Continue signup process

---

### 1.4 Complete Account Details

**More fields** (second page):

| Field | What to Enter | Notes |
|-------|---------------|-------|
| **Password** | Strong password (save it!) | Min 12 chars, uppercase, number, special |
| **Cloud Account Name** | `sentinel-corp` or your choice | Lowercase, no spaces (becomes part of URL) |
| **Home Region** | `US West (Phoenix)` or `US West (San Jose)` | **CANNOT CHANGE LATER** - choose Phoenix if unsure |
| **Phone Number** | Your mobile | For SMS verification |

**IMPORTANT - Home Region**:
- Phoenix = closer to California (lower latency)
- San Jose = even closer but sometimes higher demand
- **Pick Phoenix** if you're not sure

**Click**: "Continue"

---

### 1.5 Phone Verification

**Wait for SMS code** (30 seconds to 2 minutes):
- Oracle sends 6-digit code to your phone
- Enter code in verification box
- **Click**: "Verify code"

---

### 1.6 Payment Method (Skip This!)

**You'll see**: "Add payment verification method"

**IMPORTANT**: Oracle free tier does NOT require credit card
- Look for text that says: "Skip for now" or "Continue without payment method"
- **Click that option**

**If forced to enter card**:
- Oracle will NOT charge unless you manually upgrade to paid tier
- They verify identity, not charge you
- Set up billing alerts at $0.01 if paranoid

---

### 1.7 Account Approval Wait

**What happens now**:
1. Oracle reviews your account (fraud prevention)
2. You receive email: "Your account is being provisioned"
3. **Wait time**: 1-24 hours (usually 1-2 hours)

**During wait time**:
- Check email every hour
- When approved: "Your Oracle Cloud account is ready"
- **Click**: "Sign in to Oracle Cloud"

**If > 24 hours**: Contact Oracle support (rare, but happens)

---

## Step 2: Create Ubuntu VM Instance

### 2.1 Sign In to Oracle Cloud Console

**Navigate to**:
```
https://cloud.oracle.com/
```

**Sign in with**:
- Cloud Account Name: `sentinel-corp` (or whatever you chose)
- Username: Your email
- Password: Your password

**You'll see**: Oracle Cloud Console dashboard

---

### 2.2 Navigate to Compute Instances

**Dashboard navigation**:
1. Look for menu icon (☰) in top-left
2. **Click**: "Compute" → "Instances"
3. **Or search**: Type "instances" in search box

**You'll see**: "Instances" page (currently empty)

---

### 2.3 Create VM Instance

**Click**: "Create Instance" button (big blue button)

**Form appears**: "Create Compute Instance"

---

### 2.4 Instance Configuration

#### Basic Information

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `sentinel-vm` | Descriptive name for your VM |
| **Compartment** | Leave default (root) | Organization unit (ignore for now) |

#### Placement

| Field | Value | Notes |
|-------|-------|-------|
| **Availability Domain** | Leave default | Auto-selected based on region |
| **Fault Domain** | Leave default | Don't change |

#### Image and Shape (IMPORTANT!)

**Click**: "Change Image" button

**Select**:
- **Image**: Ubuntu 22.04 (or latest Ubuntu)
- **Image build**: Latest available
- **Click**: "Select Image"

**Click**: "Change Shape" button

**CRITICAL - Select ARM Shape (Free Tier)**:

1. **Click**: "Ampere" tab (not Intel/AMD)
2. **Select**: `VM.Standard.A1.Flex`
3. **Configure**:
   - **Number of OCPUs**: 2 (or up to 4 if available)
   - **Memory (GB)**: 12 GB (or up to 24 GB if available)

**Why ARM?**:
- Free tier includes: 4 ARM cores + 24 GB RAM forever
- Free tier Intel: Only 2 cores + 1 GB RAM (not enough for SC)
- Python works great on ARM (no issues)

**Click**: "Select Shape"

#### Networking

**Keep defaults**:
- ✅ "Create new virtual cloud network"
- ✅ "Assign a public IPv4 address"
- ✅ "Create new subnet"

**These auto-configure** networking for SSH access

#### Add SSH Keys (CRITICAL - DON'T LOSE THIS!)

**Two options**:

**Option A: Generate SSH Key Pair (RECOMMENDED)**
1. **Click**: "Generate a key pair for me"
2. **Click**: "Save Private Key" → Downloads `ssh-key-YYYY-MM-DD.key`
3. **Click**: "Save Public Key" → Downloads `ssh-key-YYYY-MM-DD.key.pub`
4. **SAVE BOTH FILES** in safe location:
   - Example: `C:\Users\wjcor\Documents\Oracle_SSH_Keys\`
   - **IF YOU LOSE THESE, YOU CANNOT ACCESS YOUR VM**

**Option B: Upload Your Own** (skip unless you have existing SSH keys)

#### Boot Volume

**Keep defaults**:
- Boot volume size: 50 GB (plenty for SC)
- ✅ "Use in-transit encryption"

---

### 2.5 Create the Instance

**Review everything**:
- Name: `sentinel-vm`
- Image: Ubuntu 22.04
- Shape: VM.Standard.A1.Flex (ARM, 2 cores, 12 GB RAM)
- SSH keys: Downloaded and saved
- Public IP: Yes

**Click**: "Create" button (bottom of page)

**Wait**: 1-2 minutes while VM provisions

**Status changes**:
- Provisioning (orange icon)
- Running (green icon)

---

### 2.6 Note Your VM's Public IP

**When status = Running**:

**Find in the instance details**:
- **Public IP Address**: `XXX.XXX.XXX.XXX`
- **COPY THIS** - you'll need it for SSH

**Example**:
```
Public IP: 129.158.45.123
```

---

## Step 3: Configure Network Security

### 3.1 Why This Matters

Oracle VMs have firewall rules (security lists) that BLOCK all incoming connections by default (including SSH). We need to allow SSH (port 22).

---

### 3.2 Open SSH Port

**From instance details page**:
1. Scroll down to **"Primary VNIC"** section
2. **Click**: The subnet link (blue text, looks like `subnet-YYYYMMDD-HHMM`)

**You'll see**: Subnet details page

**Navigate to Security List**:
1. Look for **"Security Lists"** in left menu
2. **Click**: "Default Security List for vcn-YYYYMMDD-HHMM" (or similar)

**You'll see**: List of Ingress Rules (incoming connections)

---

### 3.3 Add SSH Ingress Rule

**Check existing rules**:
- Look for rule with **Destination Port: 22**
- If it exists: You're done! (Skip to Step 4)
- If NOT exists: Continue below

**Click**: "Add Ingress Rules" button

**Fill out form**:

| Field | Value | Notes |
|-------|-------|-------|
| **Source Type** | CIDR | Standard IP range format |
| **Source CIDR** | `0.0.0.0/0` | Allow from anywhere (your laptop's IP changes) |
| **IP Protocol** | TCP | SSH uses TCP |
| **Destination Port Range** | `22` | SSH port |
| **Description** | "SSH access" | Optional but helpful |

**Click**: "Add Ingress Rules"

**Result**: SSH port 22 now open to internet (secured by SSH key auth)

---

## Step 4: Install PuTTY (Windows SSH Client)

### 4.1 Download PuTTY

**Navigate to**:
```
https://www.putty.org/
```

**Click**: "Download PuTTY" → Latest Windows installer (64-bit)

**File downloads**: `putty-64bit-X.XX-installer.msi`

---

### 4.2 Install PuTTY

**Run installer**:
1. Double-click downloaded `.msi` file
2. Click "Next" through installer
3. Keep all defaults
4. Click "Install"
5. Click "Finish"

**Installed programs**:
- PuTTY (SSH client)
- PuTTYgen (key converter - we'll use this!)

---

### 4.3 Convert SSH Key to PuTTY Format

**Why**: Oracle gives you OpenSSH key (`.key` file), but PuTTY needs PPK format

**Open PuTTYgen**:
1. Start Menu → PuTTY → PuTTYgen
2. Window opens: "PuTTY Key Generator"

**Load Oracle's key**:
1. **Click**: "Load" button
2. **Change file type** dropdown (bottom-right): "All Files (*.*)"
3. **Navigate to** where you saved SSH key: `C:\Users\wjcor\Documents\Oracle_SSH_Keys\`
4. **Select**: `ssh-key-YYYY-MM-DD.key` (no .pub)
5. **Click**: "Open"

**You'll see**: "Successfully imported foreign key..."
- Click "OK"

**Save as PPK**:
1. **Click**: "Save private key"
2. Warning: "Save without passphrase?" → Click "Yes"
3. **Save as**: `oracle-sentinel-vm.ppk` (same folder as original key)
4. **Close PuTTYgen**

---

### 4.4 Connect to VM via PuTTY

**Open PuTTY**:
1. Start Menu → PuTTY → PuTTY
2. Window opens: "PuTTY Configuration"

**Session settings**:

| Field | Value | Notes |
|-------|-------|-------|
| **Host Name** | `ubuntu@XXX.XXX.XXX.XXX` | Replace XXX with your VM's public IP |
| **Port** | `22` | Default SSH port |
| **Connection type** | SSH | Should be selected by default |

**Example**:
```
Host Name: ubuntu@129.158.45.123
```

**Configure SSH key**:
1. Left sidebar: **Click**: "Connection" → "SSH" → "Auth" → "Credentials"
2. **"Private key file for authentication"**: Click "Browse"
3. **Navigate to**: `C:\Users\wjcor\Documents\Oracle_SSH_Keys\oracle-sentinel-vm.ppk`
4. **Select** the `.ppk` file
5. **Click**: "Open"

**Save this session** (so you don't have to re-enter every time):
1. Left sidebar: **Click**: "Session" (back to top)
2. **"Saved Sessions"**: Type `Sentinel-Oracle-VM`
3. **Click**: "Save"
4. **Click**: "Open" (to connect)

---

### 4.5 First Connection

**Security Alert**:
- First time connecting: "PuTTY Security Alert" appears
- Message: "The host key is not cached..."
- **This is normal**
- **Click**: "Accept"

**Terminal window opens**:

```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-1045-oracle aarch64)

ubuntu@sentinel-vm:~$
```

**YOU'RE IN!** ✅

---

## Step 5: Initial VM Setup

### 5.1 Update System Packages

**Copy/paste these commands** (one at a time):

```bash
sudo apt update
```

**What this does**: Updates package list (like "apt-get update" in old Ubuntu)

**You'll see**: Lots of text scrolling (package updates downloading)

**When done**: Prompt returns: `ubuntu@sentinel-vm:~$`

---

```bash
sudo apt upgrade -y
```

**What this does**: Upgrades all installed packages to latest versions
**`-y` flag**: Auto-answers "yes" to prompts (no interaction needed)

**You'll see**: More text, possibly "XX packages upgraded"

**Wait time**: 2-5 minutes (first time)

**When done**: Prompt returns

---

### 5.2 Install Basic Tools

```bash
sudo apt install -y python3 python3-pip python3-venv git nano curl
```

**What this installs**:
- `python3`: Python 3 (for SC)
- `python3-pip`: Package manager (install alpaca-py, etc.)
- `python3-venv`: Virtual environments (isolation)
- `git`: Version control (pull from GitHub)
- `nano`: Text editor (like Notepad for terminal)
- `curl`: Download tool (testing APIs)

**Wait time**: 1-2 minutes

**When done**: Prompt returns

---

### 5.3 Verify Python Installation

```bash
python3 --version
```

**Expected output**:
```
Python 3.10.12
```

(Or similar - anything 3.9+ is fine)

---

```bash
pip3 --version
```

**Expected output**:
```
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
```

---

### 5.4 Set Timezone to Pacific

**Why**: Cron jobs run based on server time. We need 6:30 AM **Pacific**, not UTC.

```bash
sudo timedatectl set-timezone America/Los_Angeles
```

**Verify**:
```bash
date
```

**Expected output** (example):
```
Sun Nov  3 11:45:32 AM PST 2025
```

Should show **PST** or **PDT** (Pacific time), not UTC.

---

### 5.5 Check Available Resources

**See your VM specs**:

```bash
lscpu | grep -E "Architecture|CPU\(s\)|Model name"
```

**Expected output**:
```
Architecture:            aarch64
CPU(s):                  2
Model name:              Neoverse-N1
```

**Check memory**:

```bash
free -h
```

**Expected output**:
```
              total        used        free      shared  buff/cache   available
Mem:           11Gi       450Mi        10Gi       1.0Mi       500Mi        10Gi
Swap:            0B          0B          0B
```

**You should see**: ~11-12 GB total RAM (plenty for SC)

---

### 5.6 Check Disk Space

```bash
df -h /
```

**Expected output**:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        48G  2.1G   46G   5% /
```

**You should see**: ~46-48 GB available (plenty for SC)

---

## Step 6: Test Connection Stability

### 6.1 Leave Terminal Open

**Keep PuTTY window open** for 5 minutes
- Do nothing, just watch
- Verify connection doesn't drop

**If connection drops**:
- Firewall issue (check ingress rules)
- Network issue (try again)

**If stable for 5 minutes**: ✅ Connection is good

---

### 6.2 Close and Reconnect

**Close PuTTY** (type `exit` or just close window)

**Re-open PuTTY**:
1. Open PuTTY
2. **Double-click**: "Sentinel-Oracle-VM" in saved sessions
3. Should connect immediately without prompts

**If successful**: ✅ Saved session works

---

## Phase 1 Complete! ✅

### What You've Accomplished

✅ Oracle Cloud account created and approved
✅ Ubuntu 22.04 VM running (ARM, 2 cores, 12 GB RAM)
✅ SSH access configured (PuTTY)
✅ System packages updated
✅ Python 3, pip, git installed
✅ Timezone set to Pacific
✅ Connection stable and saved

### What's Next

**Phase 2**: Install VS Code Remote SSH extension, copy Sentinel to cloud, install dependencies

**Estimated time**: 1-2 hours

---

## Troubleshooting

### Can't Connect via PuTTY

**Error**: "Connection refused" or "Connection timed out"

**Fixes**:
1. Verify public IP is correct (check Oracle console)
2. Verify ingress rule for port 22 exists (Step 3.3)
3. Verify using correct SSH key (`.ppk` file)
4. Verify username is `ubuntu` (not `root` or your name)
5. Wait 5 minutes (VM might still be provisioning)

---

### Oracle Account Not Approved

**Symptom**: Waiting > 24 hours

**Fixes**:
1. Check spam folder for approval email
2. Log in to cloud.oracle.com → check account status
3. Contact Oracle support: https://www.oracle.com/cloud/support/
4. Provide: Account name, email, approximate signup time

---

### VM Creation Failed

**Error**: "Out of capacity" or "Shape not available"

**Fixes**:
1. Try different Availability Domain (edit instance, change AD)
2. Try lower resources (1 OCPU, 6 GB RAM still plenty for SC)
3. Try different region (US West San Jose instead of Phoenix)
4. Wait 24 hours and retry (capacity fluctuates)

---

### SSH Key Lost

**Symptom**: Deleted `.key` or `.ppk` file

**Fixes**:
1. **If VM still accessible**: Create new SSH key pair, add to VM
2. **If VM not accessible**: Terminate VM, create new one (data lost)
3. **Prevention**: Back up SSH keys to USB drive, cloud storage

---

## Next Steps

**When ready for Phase 2**:
1. Read `PHASE_2_SC_MIGRATION.md`
2. Install VS Code Remote SSH extension
3. Copy Sentinel to cloud VM
4. Install Python dependencies
5. Run first test of SC on cloud

**Questions before proceeding?** Ask now - Phase 1 is the foundation. Better to clarify now than troubleshoot later.

---

*Phase 1 Complete - Ready for Migration*
*Sentinel Corporation - Oracle Cloud Setup Guide*
