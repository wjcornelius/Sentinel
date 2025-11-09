# Sentinel Corporation - Oracle Cloud Migration Guide

**Date**: November 3, 2025
**Purpose**: Migrate SC from crash-prone Windows laptop to Oracle Cloud Free Tier VM
**Target**: Zero monthly cost, 24/7 uptime, automated execution at 6:30 AM Pacific

---

## IMPORTANT: Your Local Backup

**Your laptop Sentinel folder STAYS INTACT.**

This migration is a **COPY**, not a **MOVE**:
- Local: `C:\Users\wjcor\OneDrive\Desktop\Sentinel` (backup, development, testing)
- Cloud: `/home/ubuntu/Sentinel` (production, automated daily runs)

You can develop locally, test on your laptop, then sync changes to cloud when ready.

---

## Migration Overview

### What We're Building

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR LAPTOP (Windows)                                      │
│  ┌──────────────────────────────────────────────┐          │
│  │  C:\Users\wjcor\OneDrive\Desktop\Sentinel   │          │
│  │  - Development environment (backup)          │          │
│  │  - Testing changes                           │          │
│  │  - VS Code with Claude Code                  │          │
│  └──────────────────────────────────────────────┘          │
│                        │                                    │
│                        │ VS Code Remote SSH                 │
│                        ▼                                    │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ (Internet)
                         │
┌─────────────────────────▼───────────────────────────────────┐
│  ORACLE CLOUD (Linux Ubuntu VM)                             │
│  ┌──────────────────────────────────────────────┐          │
│  │  /home/ubuntu/Sentinel                       │          │
│  │  - Production environment                    │          │
│  │  - Automated daily runs (cron)               │          │
│  │  - Always-on, never crashes                  │          │
│  │  - FREE FOREVER (no monthly cost)            │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  Cron Job: 6:30 AM Pacific → Run SC → Email results        │
└─────────────────────────────────────────────────────────────┘
```

### Timeline

| Phase | Duration | Your Effort | Description |
|-------|----------|-------------|-------------|
| **Phase 1** | 2-4 hours | Active setup | Oracle account, VM creation, SSH access |
| **Phase 2** | 1-2 hours | Copy/paste commands | SC migration, Python setup, testing |
| **Phase 3** | 30-60 min | Configuration | Cron automation, email notifications |
| **Total** | 4-7 hours | Over 2-3 days | One-time setup, then hands-off forever |

### What You'll Learn

**Minimal Linux Commands** (DOS equivalents):
- `ls` = `dir` (list files)
- `cd` = `cd` (change directory)
- `pwd` = `cd` (show current directory)
- `cp` = `copy` (copy file)
- `rm` = `del` (delete file)
- `nano` = `edit` (text editor)

**That's it.** Everything else is copy/paste commands I provide.

### Tools You'll Install

1. **PuTTY** (Windows SSH client) - for initial VM setup
2. **VS Code Remote SSH extension** - for development (makes cloud feel local)

---

## Phase Breakdown

### Phase 1: Oracle Cloud Setup (2-4 hours over 2 days)

**Goal**: Create free Oracle Cloud account with Ubuntu VM, establish SSH access

**What happens**:
1. Sign up for Oracle Cloud (free, no credit card required)
2. Wait for account approval (1-24 hours)
3. Create Ubuntu 22.04 VM (ARM, free tier)
4. Configure network (allow SSH access)
5. Download SSH private key
6. Connect via PuTTY to test

**Output**: Working Ubuntu VM you can SSH into

**Gotchas**:
- Oracle account approval can take up to 24 hours (usually 1-2 hours)
- ARM architecture (not x86) - Python works fine, just different CPU
- Need to save SSH private key (lose it = lose access)

---

### Phase 2: SC Migration (1-2 hours)

**Goal**: Copy SC to cloud VM, install dependencies, run first test

**What happens**:
1. Install VS Code Remote SSH extension
2. Connect to Oracle VM via VS Code
3. Copy Sentinel folder to cloud (drag/drop in VS Code)
4. Install Python 3, pip, virtualenv
5. Install SC dependencies (alpaca-py, openai, yfinance, etc.)
6. Set up API keys as environment variables (secure)
7. Create SQLite database
8. Run SC manually to test

**Output**: SC runs successfully on cloud VM

**Gotchas**:
- Need to recreate `.env` file with API keys (don't copy from laptop - security)
- Database starts fresh (or copy existing sentinel.db if you want history)
- First run might take longer (downloading data)

---

### Phase 3: Automation Setup (30-60 min)

**Goal**: Schedule SC to run daily at 6:30 AM Pacific, email you results

**What happens**:
1. Create bash script wrapper for SC
2. Set up cron job (Linux task scheduler)
3. Configure email notifications (optional but recommended)
4. Test cron job runs correctly
5. Set timezone to Pacific

**Output**: SC runs automatically every market day at 6:30 AM, you get email when done

**Gotchas**:
- Cron uses 24-hour time (6:30 AM = 06:30)
- Need to account for Pacific timezone
- Email setup optional (can check logs instead)

---

## Cost Breakdown

### Oracle Cloud Free Tier (What You Get Forever)

| Resource | Free Tier Limit | SC Usage | Headroom |
|----------|-----------------|----------|----------|
| **Compute (VMs)** | 4 ARM cores | 2 cores | 2x buffer |
| **RAM** | 24 GB total | 2-4 GB | 6x buffer |
| **Storage** | 200 GB | ~5 GB | 40x buffer |
| **Network** | 10 TB/month | ~1 GB/month | 10,000x buffer |
| **Monthly cost** | **$0** | **$0** | **FREE** |

### If You Accidentally Exceed Free Tier

Oracle won't charge you without explicit opt-in to paid tier. They'll just throttle or suspend resources. **You cannot get surprise bills.**

Compare to Google Cloud:
- Google: $300 credit expires after 90 days, then charges kick in
- Oracle: Free tier never expires, no credit card games

---

## Prerequisites

### What You Need Before Starting

- [ ] Stable internet connection (initial setup only)
- [ ] Email address (for Oracle account)
- [ ] Phone number (for Oracle verification)
- [ ] Your Alpaca API keys (paper trading)
- [ ] Your OpenAI API key (GPT-5)
- [ ] Your Perplexity API key (news)
- [ ] 4-7 hours spread over 2-3 days

### What You DON'T Need

- ❌ Credit card (Oracle free tier doesn't require it)
- ❌ Linux experience (I'll provide exact commands)
- ❌ Advanced networking knowledge (I'll configure everything)
- ❌ Money (entire process is free)

---

## Backup Strategy

### Local Laptop (Development)

**Purpose**: Testing, development, backup

**When to use**:
- Developing new features
- Testing changes before deploying to cloud
- Debugging issues
- Learning/experimentation

**Sync method**: Manual copy/paste or `scp` command (I'll show you)

### Cloud VM (Production)

**Purpose**: Automated daily trading, always-on reliability

**When to use**:
- Daily automated market runs
- Production trading
- Historical data storage
- Hands-off operation

**Backup method**: Oracle snapshots (free tier includes backups)

### Workflow Example

```
1. Develop new feature on laptop (local Sentinel folder)
2. Test locally (python main_script.py)
3. When satisfied, sync changes to cloud VM
4. Cloud VM uses new feature for next automated run
5. Local copy remains as backup/development environment
```

---

## What Could Go Wrong (and How We'll Fix It)

### Issue 1: Oracle Account Approval Delayed

**Symptom**: Waiting more than 24 hours for account approval
**Fix**: Contact Oracle support, use Google Cloud trial as backup plan
**Likelihood**: Low (usually approved in 1-2 hours)

### Issue 2: SSH Connection Failed

**Symptom**: Can't connect via PuTTY or VS Code
**Fix**: Check firewall rules, verify SSH key, test from Oracle console
**Likelihood**: Medium (common first-time setup issue, easy to fix)

### Issue 3: SC Fails to Run on Cloud

**Symptom**: Python errors, missing dependencies
**Fix**: Install missing packages, check Python version, verify API keys
**Likelihood**: Medium (expected during initial setup, we'll troubleshoot together)

### Issue 4: Cron Job Doesn't Run

**Symptom**: 6:30 AM comes, no SC execution
**Fix**: Check cron syntax, verify timezone, check logs
**Likelihood**: Medium (cron can be tricky first time, we'll test thoroughly)

### Issue 5: Run Out of Free Tier Resources

**Symptom**: Oracle warns about resource usage
**Fix**: Optimize SC (unlikely needed), reduce logging, clean old data
**Likelihood**: Very Low (SC uses <5% of free tier limits)

---

## Success Criteria

You'll know migration succeeded when:

✅ You can connect to Oracle VM via VS Code Remote
✅ SC runs successfully on cloud VM (manual test)
✅ Cron job executes at 6:30 AM Pacific automatically
✅ You receive email/notification when run completes
✅ You can edit files in VS Code and changes apply to cloud
✅ Your laptop can be off and SC still runs
✅ No monthly bills, no surprise charges

---

## Post-Migration Benefits

### What You Gain

1. **No More 6:30 AM Alarms**
   - SC runs automatically
   - Email tells you when done
   - Sleep in, check results over coffee

2. **No More Crash Anxiety**
   - Cloud VM never crashes
   - SC completes every run
   - No lost work, no corruption

3. **Professional Infrastructure**
   - Real trading systems run on servers
   - 24/7 uptime
   - Scalable for future features

4. **Development Freedom**
   - Use laptop for testing (can crash, doesn't matter)
   - Production runs independently
   - Best of both worlds

5. **Future Options**
   - Add webhooks (Alpaca calls your cloud VM)
   - Build web dashboard (monitor from phone)
   - Run multiple strategies in parallel
   - Scale to live trading when ready

---

## Ready to Begin?

Next document: **PHASE_1_ORACLE_SETUP.md** (detailed step-by-step instructions)

Let's get you off that crashing laptop and onto stable, free cloud infrastructure.

---

*Sentinel Corporation - Created with Claude Code*
*Migration Guide v1.0 - November 3, 2025*
