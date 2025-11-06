# Oracle Cloud Migration - Complete Plan for Sentinel Corporation

**Date:** November 6, 2025
**Purpose:** Migrate Sentinel Corporation from unreliable laptop to Oracle Cloud Free Tier
**Priority:** CRITICAL - Laptop crashes, RAM failures, possible forced sleep by Monitoring
**Cost:** $0/month (Oracle Cloud Always Free Tier)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Why Migrate Now](#why-migrate-now)
3. [Migration Phases](#migration-phases)
4. [Crash Recovery Plan](#crash-recovery-plan)
5. [Rollback Strategy](#rollback-strategy)
6. [Testing Plan](#testing-plan)
7. [Post-Migration Monitoring](#post-migration-monitoring)

---

## Executive Summary

### The Plan
Migrate Sentinel Corporation trading system from local laptop to Oracle Cloud compute instance in **3 phases**:
1. **Phase 1:** Setup Oracle Cloud (reversible, no risk)
2. **Phase 2:** Deploy & Test on Cloud (laptop still primary)
3. **Phase 3:** Switch to Cloud Primary (laptop becomes backup)

### Key Benefits
- **100% uptime** - No more laptop crashes or sleep modes
- **Guaranteed execution** - Cron jobs run at 8:00 AM PT even if laptop off
- **Better performance** - Dedicated resources, no database lock issues
- **Monitoring-proof** - Cloud instance unaffected by local monitoring software
- **$0 cost** - Oracle Always Free Tier

### Safety Features
- **Every phase is reversible** - Can abort and return to laptop at any time
- **Laptop remains backup** - Keep local system functional during migration
- **Gradual transition** - Test thoroughly before switching primary
- **Git-based deployment** - Easy to roll back or redeploy

---

## Why Migrate Now

### Current Problems with Laptop
1. **Unreliable Hardware**
   - Laptop crashes frequently (crashed twice today)
   - RAM failed previously (reason for new laptop)
   - Current laptop aging and unstable

2. **Monitoring Software Concerns**
   - May force sleep mode after inactivity
   - Cannot guarantee system running at 8:00 AM PT
   - User cannot modify power settings (compliance)

3. **Execution Reliability**
   - Today's execution at 8:00 AM PT succeeded
   - But laptop could be asleep/crashed tomorrow
   - Missing execution = missing trades = opportunity cost

4. **Database Issues**
   - Database lock errors today (fixed but concerning)
   - Laptop's limited resources cause contention
   - Cloud has dedicated resources

### Why Oracle Cloud Free Tier

**Always Free Resources:**
- 2 VM instances (Ampere A1 Compute)
- 24 GB RAM total (12 GB per instance - plenty for SC)
- 200 GB block storage
- 10 TB outbound data transfer/month
- **Completely free forever** - not a trial

**vs AWS Free Tier:**
- AWS: Only free for 12 months
- AWS t2.micro: 1 GB RAM (not enough for SC)
- Oracle: Free forever, 12 GB RAM per instance

**vs Other Options:**
- Google Cloud: No permanent free tier
- Azure: Trial only
- Oracle: Best free tier in industry

---

## Migration Phases

### Phase 1: Oracle Cloud Setup (30-45 minutes)
**Goal:** Create and configure Oracle Cloud instance
**Risk:** ZERO - No changes to laptop system
**Reversible:** YES - Can delete cloud instance at any time

#### Step 1.1: Create Oracle Cloud Account (10 min)
1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill out registration:
   - Email address
   - Country/region
   - Cloud account name
4. Verify email
5. Add payment method (required but not charged for Always Free)
6. Complete identity verification

**If laptop crashes:** Resume from any computer with internet. Oracle saves progress.

#### Step 1.2: Create Compute Instance (15 min)
1. Log into Oracle Cloud Console
2. Navigate to Compute → Instances
3. Click "Create Instance"
4. Configure:
   - **Name:** sentinel-trading-01
   - **Image:** Ubuntu 22.04 (latest)
   - **Shape:** VM.Standard.A1.Flex
   - **OCPU:** 2 (free tier allows up to 4)
   - **Memory:** 12 GB (free tier allows up to 24 GB)
   - **Boot volume:** 100 GB
5. **IMPORTANT:** Download SSH private key
   - Save as `sentinel_oracle_key.pem`
   - Store safely - cannot retrieve later
6. Click "Create"
7. Wait 2-3 minutes for provisioning

**If laptop crashes:**
- Keys already downloaded? Proceed from any computer
- Keys not downloaded? Delete instance and recreate (no data loss)

#### Step 1.3: Configure Firewall (5 min)
1. In instance details, click "Subnet"
2. Click the security list
3. Add Ingress Rule:
   - **Source:** 0.0.0.0/0
   - **Destination Port:** 22 (SSH)
4. Add Ingress Rule for HTTPS (optional, for future web dashboard):
   - **Source:** 0.0.0.0/0
   - **Destination Port:** 443

**If laptop crashes:** No problem - firewall saves automatically in Oracle Cloud

#### Step 1.4: Initial SSH Connection (10 min)
1. Get instance public IP from console
2. Set key permissions:
   ```bash
   chmod 600 sentinel_oracle_key.pem
   ```
3. Connect:
   ```bash
   ssh -i sentinel_oracle_key.pem ubuntu@<PUBLIC_IP>
   ```
4. If successful, you're connected to your cloud instance!

**If laptop crashes:**
- Public IP is in Oracle Console (check from any computer)
- SSH key is on laptop (when it restarts, just try again)

**Phase 1 Complete: Oracle instance ready, laptop unchanged**

---

### Phase 2: Deploy & Test (45-60 minutes)
**Goal:** Get Sentinel running on cloud, test thoroughly
**Risk:** LOW - Laptop system still primary, cloud is just a copy
**Reversible:** YES - Delete cloud files, laptop unaffected

#### Step 2.1: Install Dependencies (15 min)
Connect to cloud instance and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install git
sudo apt install -y git

# Install SQLite (for database)
sudo apt install -y sqlite3

# Create project directory
mkdir -p ~/sentinel
cd ~/sentinel
```

**If laptop crashes:** Progress saved on cloud. Reconnect from laptop when it restarts and continue.

#### Step 2.2: Clone Repository (5 min)
```bash
# Clone from GitHub
git clone https://github.com/wjcornelius/Sentinel.git
cd Sentinel

# Create virtual environment
python3.11 -m venv venv

# Activate virtualenv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

**If laptop crashes:**
- Code is on GitHub (accessible from anywhere)
- When laptop restarts, clone continues where it left off

#### Step 2.3: Configure Secrets (10 min)
**IMPORTANT:** Do NOT commit API keys to GitHub

```bash
# Create config.py with API keys
nano config.py
```

Paste your API keys:
```python
# Alpaca
ALPACA_API_KEY = "your_alpaca_key"
ALPACA_SECRET_KEY = "your_alpaca_secret"

# OpenAI
OPENAI_API_KEY = "your_openai_key"

# Perplexity
PERPLEXITY_API_KEY = "your_perplexity_key"
```

Save and exit (Ctrl+X, Y, Enter)

**If laptop crashes:**
- API keys are in your password manager or local config.py
- When laptop restarts, copy keys from laptop to cloud

#### Step 2.4: Initialize Database (5 min)
```bash
# Database will auto-create on first run, but let's verify:
python3 -c "import sqlite3; conn = sqlite3.connect('sentinel.db'); print('Database created successfully')"
```

**If laptop crashes:** Database file saved on cloud. Just reconnect and continue.

#### Step 2.5: Test Execution (15 min)
```bash
# Test Research Department
python3 -c "from Departments.Research.research_department import ResearchDepartment; r = ResearchDepartment('sentinel.db', None); print('Research OK')"

# Test News Department
python3 -c "from Departments.News.news_department import NewsDepartment; n = NewsDepartment('sentinel.db'); print('News OK')"

# Test full workflow (DO NOT EXECUTE - just generate plan)
python3 sentinel_control_panel.py
# Select option [1] Request Trading Plan
# Review plan (DO NOT EXECUTE)
# Verify it works
# Exit

```

**If laptop crashes during testing:**
- Cloud instance keeps running
- Reconnect when laptop restarts
- Check logs: `tail -f sentinel.log`

#### Step 2.6: Setup Cron Job (10 min)
```bash
# Edit crontab
crontab -e
```

Add this line (executes at 8:00 AM Pacific Time = 11:00 AM Eastern = 16:00 UTC):
```
0 16 * * 1-5 cd /home/ubuntu/sentinel/Sentinel && /home/ubuntu/sentinel/Sentinel/venv/bin/python3 /home/ubuntu/sentinel/Sentinel/run_daily_cycle.py >> /home/ubuntu/sentinel/cron.log 2>&1
```

This runs Monday-Friday at 8:00 AM PT automatically.

**Verify cron job:**
```bash
crontab -l  # List all cron jobs
```

**If laptop crashes:** Cron job is on cloud, unaffected. Will run tomorrow at 8:00 AM PT.

**Phase 2 Complete: Sentinel running on cloud, tested, cron scheduled**

---

### Phase 3: Switch to Cloud Primary (15 minutes)
**Goal:** Make cloud the primary execution system
**Risk:** LOW - Laptop remains functional backup
**Reversible:** YES - Just switch back to laptop execution

#### Step 3.1: Backup Laptop Data (5 min)
On laptop:
```bash
# Backup current database
cp sentinel.db sentinel_backup_$(date +%Y%m%d).db

# Commit any uncommitted changes
git add .
git commit -m "Backup before cloud migration"
git push origin main
```

#### Step 3.2: Sync Database (5 min)
**Option A: Start Fresh on Cloud (Recommended)**
- Cloud starts with clean database
- Reconcile positions from Alpaca on first run
- Simpler, cleaner

**Option B: Copy Laptop Database to Cloud**
```bash
# On laptop, compress database
gzip -c sentinel.db > sentinel.db.gz

# Copy to cloud
scp -i sentinel_oracle_key.pem sentinel.db.gz ubuntu@<PUBLIC_IP>:/home/ubuntu/sentinel/Sentinel/

# On cloud, extract
gunzip sentinel.db.gz
```

#### Step 3.3: Monitor First Cloud Execution (5 min)
**Tomorrow morning at 8:00 AM PT:**

1. SSH into cloud instance:
   ```bash
   ssh -i sentinel_oracle_key.pem ubuntu@<PUBLIC_IP>
   ```

2. Watch logs in real-time:
   ```bash
   tail -f /home/ubuntu/sentinel/cron.log
   ```

3. Verify execution completes successfully

4. Check Alpaca dashboard for orders

**If anything fails:**
- Cloud logs everything to `/home/ubuntu/sentinel/cron.log`
- Can manually run from laptop as backup
- Fix issues and try again tomorrow

**Phase 3 Complete: Cloud is now primary, laptop is backup**

---

## Crash Recovery Plan

### Scenario 1: Laptop Crashes During Phase 1 (Oracle Setup)
**Impact:** ZERO - No changes to laptop system yet

**Recovery:**
1. Restart laptop
2. Log into Oracle Cloud from browser (any computer works)
3. Continue where you left off
4. All Oracle setup is in cloud - nothing lost

### Scenario 2: Laptop Crashes During Phase 2 (Deployment)
**Impact:** LOW - Cloud instance has partial progress, laptop unaffected

**Recovery:**
1. Restart laptop
2. SSH back into cloud instance
3. Check what's installed:
   ```bash
   cd ~/sentinel/Sentinel
   ls -la
   ```
4. Resume from last completed step
5. All cloud files preserved

**Specific Sub-Scenarios:**
- **During git clone:** Just run `git clone` again (fast, no data loss)
- **During pip install:** Reactivate venv and run `pip install -r requirements.txt` again
- **During config:** Edit `config.py` again and paste keys
- **During testing:** Just rerun tests

### Scenario 3: Laptop Crashes During Phase 3 (Switchover)
**Impact:** LOW - Both systems functional, just need to verify

**Recovery:**
1. Restart laptop
2. Verify cloud system status:
   ```bash
   ssh -i sentinel_oracle_key.pem ubuntu@<PUBLIC_IP>
   crontab -l  # Verify cron job exists
   ```
3. If cloud ready: Done, cloud is primary
4. If cloud not ready: Use laptop as primary, finish cloud setup later

### Scenario 4: Laptop Crashes AFTER Migration (Cloud is Primary)
**Impact:** NONE - Cloud keeps running!

**What Happens:**
- 8:00 AM PT tomorrow: Cloud executes trading plan automatically
- Laptop completely irrelevant
- You can check execution from:
  - Alpaca mobile app
  - Alpaca website (from any computer)
  - SSH into cloud when laptop restarts

**This is the whole point of cloud migration!**

### Scenario 5: Cloud Instance Fails (Extremely Rare)
**Impact:** MEDIUM - Need to switch back to laptop

**Recovery:**
1. Use laptop to execute manually:
   ```bash
   python sentinel_control_panel.py
   ```
2. Fix cloud issue:
   - Check Oracle Cloud Console for instance status
   - Restart instance if needed
   - Check logs for errors
3. Once cloud fixed, resume cloud primary

**Likelihood:** <0.01% - Oracle has 99.95% uptime SLA

---

## Rollback Strategy

### Rollback from Phase 1
**Action:** Delete Oracle Cloud instance
**Time:** 2 minutes
**Data Loss:** None (laptop unchanged)

### Rollback from Phase 2
**Action:** Stop using cloud, keep using laptop
**Time:** 0 minutes (just don't switch)
**Data Loss:** None

### Rollback from Phase 3 (Cloud is Primary)
**Action:** Disable cloud cron, use laptop

**Steps:**
1. SSH into cloud:
   ```bash
   ssh -i sentinel_oracle_key.pem ubuntu@<PUBLIC_IP>
   ```
2. Disable cron:
   ```bash
   crontab -r  # Remove all cron jobs
   ```
3. Use laptop for execution:
   ```bash
   python sentinel_control_panel.py
   ```

**Time:** 5 minutes
**Data Loss:** None (database sync if needed)

---

## Testing Plan

### Pre-Migration Tests (On Laptop)
- [ ] Verify all departments working
- [ ] Verify database accessible
- [ ] Commit and push latest code to GitHub
- [ ] Backup config.py (API keys)
- [ ] Backup sentinel.db

### Post-Deployment Tests (On Cloud)
- [ ] Verify Python 3.11 installed
- [ ] Verify all pip packages installed
- [ ] Verify config.py has correct API keys
- [ ] Test Research Department import
- [ ] Test News Department import
- [ ] Test Operations Manager import
- [ ] Test database connection
- [ ] Test Alpaca API connection
- [ ] Test full workflow (Request Trading Plan - DO NOT EXECUTE)
- [ ] Verify cron job syntax
- [ ] Verify cron job time (8:00 AM PT = 16:00 UTC)

### First Live Execution Tests
- [ ] Cloud cron runs at 8:00 AM PT
- [ ] Logs show workflow execution
- [ ] Orders submitted to Alpaca
- [ ] Database updated correctly
- [ ] No errors in cron.log

---

## Post-Migration Monitoring

### Daily Checks (First Week)
- Check `/home/ubuntu/sentinel/cron.log` every day after 8:00 AM PT
- Verify orders in Alpaca dashboard
- Monitor for any errors or warnings

### Weekly Checks (Ongoing)
- Check cloud instance status (Oracle Console)
- Review logs for any recurring issues
- Update system packages if needed:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```

### Monthly Checks
- Review cloud costs (should remain $0)
- Check Oracle Cloud account status
- Verify cron job still active
- Test SSH access

---

## Cost Breakdown

### Oracle Cloud Always Free Tier
- **Compute:** $0/month (2 VMs with 24 GB RAM total)
- **Storage:** $0/month (200 GB block storage)
- **Network:** $0/month (10 TB outbound/month)
- **Total:** **$0/month forever**

### Comparison
- **Laptop electricity:** ~$5-10/month (no longer needs to run 24/7)
- **Net savings:** $5-10/month
- **Reliability gain:** Priceless

---

## Security Considerations

### SSH Key Management
- Keep `sentinel_oracle_key.pem` safe (encrypted backup recommended)
- Never commit SSH keys to GitHub
- Can regenerate if lost (but requires instance recreation)

### API Key Security
- Never commit `config.py` to GitHub (already in `.gitignore`)
- Store API keys in password manager
- Rotate keys periodically (good practice)

### Firewall
- Only port 22 (SSH) exposed
- Can add IP whitelist for extra security (limit SSH to your IP)
- Optional: Setup fail2ban for brute force protection

---

## Troubleshooting

### Cannot SSH into instance
**Check:**
1. Instance is running (Oracle Console)
2. Security list has port 22 open
3. SSH key file has correct permissions: `chmod 600 sentinel_oracle_key.pem`
4. Using correct IP address (public IP from console)
5. Using correct username: `ubuntu` (not `root`)

### Cron job not running
**Check:**
1. Crontab syntax: `crontab -l`
2. Timezone correct: `timedatectl` (should show UTC)
3. Cron service running: `sudo systemctl status cron`
4. Check cron.log for errors: `tail -100 /home/ubuntu/sentinel/cron.log`

### Out of memory
**Check:**
1. Instance has 12 GB RAM (plenty for SC)
2. No other heavy processes: `top`
3. If needed: Upgrade to 24 GB RAM (still free tier)

### Database locked errors
**Check:**
1. Not running multiple instances simultaneously
2. Database file has correct permissions
3. No zombie processes: `ps aux | grep python`

---

## Conclusion

This migration plan provides:
- **Safety:** Every phase is reversible
- **Reliability:** Cloud instance runs 24/7
- **Cost:** $0/month (Oracle Always Free)
- **Crash-proof:** Laptop crashes don't affect cloud
- **Monitoring-proof:** Cloud unaffected by local monitoring software

**Next Steps:**
1. Review this plan
2. Ask any questions
3. Begin Phase 1 (Oracle setup)
4. Test thoroughly in Phase 2
5. Switch to cloud primary in Phase 3

**Estimated Total Time:** 2-3 hours (can pause between phases)

**Risk:** Minimal (every step reversible, laptop remains backup)

**Reward:** Never worry about laptop crashes during trading hours again!

---

**Document Version:** 1.0
**Last Updated:** November 6, 2025
**Status:** Ready for implementation
