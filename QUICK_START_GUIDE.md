# Sentinel Corporation - Quick Start Guide

---

## 🚀 **How to Run SC**

### **Option 1: Desktop Launcher** (Recommended)
```
Double-click: Run_Sentinel.bat on your desktop
```

### **Option 2: Command Line**
```bash
cd "C:\Users\wjcor\OneDrive\Desktop\Sentinel"
python __sentinel_control_panel.py
```

---

## 📋 **Main Menu Options**

### **When Market is CLOSED** (Offline Mode):
1. **Generate Portfolio Plan** - Run SC analysis, get proposed trades
2. **View Saved Portfolio Plan** - Preview what SC wants to trade
3. **Approve Plan for Execution** - Lock in plan for Monday
4. **Reject Plan** - Delete and start over
5. **View Current Positions** - See what's in Alpaca
6. **View Account Summary** - Cash, buying power, portfolio value

### **When Market is OPEN** (Online Mode):
1. **Execute Approved Trading Plan** - Submit orders to Alpaca
2. (All the offline options still available)

---

## ✅ **Tonight's Workflow** (Friday Evening)

```
1. Run SC
2. Generate Portfolio Plan
   → SC shows: 3 BUY orders (MSFT, AAPL, GOOGL)
3. View Saved Portfolio Plan
   → Preview the orders
4. Don't like it? → Reject and regenerate
5. Like it? → Approve Plan for Execution
6. Exit SC
```

**Result**: You now have an APPROVED plan ready for Monday!

---

## 🎯 **Monday Morning Workflow** (If You Want to Execute)

```
1. Run SC at 9:30 AM
   → Mode shows: ONLINE (market open, no trades today)
2. Select: Execute Approved Trading Plan
3. Review orders one more time
4. Confirm: y
5. SC submits to Alpaca
   → Shows Order IDs for each trade
6. SC auto-switches to OFFLINE (already traded today)
7. Continue development safely
```

---

## 🔧 **Configuration** (`config.py`)

### **Current Settings**:
```python
ALPACA_PAPER_TRADING_ENABLED = True   # Connected to Alpaca
FORCE_OFFLINE_MODE = False            # Auto-detect mode
SKIP_RESEARCH_BY_DEFAULT = True       # Require approval for AI costs
```

### **To Switch to Simulation Mode**:
```python
ALPACA_PAPER_TRADING_ENABLED = False  # Use database instead of Alpaca
```

---

## 📊 **Your Alpaca Account**

**Account**: Sentinel Virtual Corp 1
**ID**: PA3UIGKEUGYP
**Starting Balance**: $100,000
**Buying Power**: $200,000 (2x margin)
**Current Positions**: 0 (clean slate)

---

## 🧪 **Test Commands**

### **Test Data Source**:
```bash
python Utils/data_source.py
```

### **Test Mode Manager**:
```bash
python Utils/mode_manager.py
```

### **Test Full Workflow**:
```bash
python test_full_workflow.py
```

### **Test Workflow Orchestrator**:
```bash
python workflow_orchestrator.py
```

---

## 📁 **Important Files**

**Trading Plans**:
- `proposed_trades_2025-11-01.json` - Today's approved plan

**Configuration**:
- `config.py` - All settings (API keys, mode control)

**Main Programs**:
- `__sentinel_control_panel.py` - User interface
- `workflow_orchestrator.py` - Coordinates departments
- `Run_Sentinel.bat` - Desktop launcher

**Utilities**:
- `Utils/data_source.py` - Reads from Alpaca or database
- `Utils/mode_manager.py` - Online/offline detection
- `Utils/alpaca_client.py` - Alpaca API wrapper

**Departments**:
- `Departments/Research/` - Stock screening & analysis
- `Departments/Risk/` - Position sizing & risk calculation
- `Departments/Portfolio/` - Constraint filtering & decision making

---

## ⚠️ **Important Notes**

### **Safety Features**:
- ✅ Can't trade when market is closed
- ✅ Can't trade if already traded today
- ✅ Must approve plan before execution
- ✅ Final confirmation before orders
- ✅ Auto-offline after trading

### **Current Limitations**:
- ⚠️ Department stubs (using mock data for now)
- ⚠️ Simple position sizing (10% per position)
- ⚠️ No real research yet (GPT-4/Perplexity disabled to save costs)

**These are intentional!** Proper testing infrastructure before enabling expensive AI calls.

---

## 🎯 **What to Do Next**

### **Tonight** (Friday):
1. ✅ Generate and approve a plan (DONE - you have one ready!)
2. ✅ Review the plan file: `proposed_trades_2025-11-01.json`
3. ✅ Check Alpaca dashboard to confirm $100K balance

### **Monday Morning** (Optional):
1. Run SC at 9:30 AM
2. Execute approved plan
3. Watch orders fill in Alpaca
4. Verify positions created

### **Next Development**:
1. Wire real Research Department (replace mock data)
2. Wire real Risk Department (replace simple sizing)
3. Wire real Portfolio Department (replace constraint stubs)
4. Test with real analysis pipeline

---

## 💡 **Pro Tips**

1. **Iterative Plan Generation**: You can regenerate plans as many times as you want until you approve one. Approval is the "lock".

2. **Safe Development**: After trading, SC auto-switches to OFFLINE. You can run it all day without risk of duplicate orders.

3. **Mode Override**: Use "Force OFFLINE Mode" if you want to guarantee no trading while testing.

4. **Check Alpaca Dashboard**: Always verify in Alpaca's web interface what SC sees.

5. **Review Plans Carefully**: Even though it's paper trading, treat it like real money for practice.

---

## 📞 **Quick Reference**

**Mode Detection**:
- ONLINE = Market open + No trades today
- OFFLINE = Market closed OR Already traded OR Manual override

**Plan Status**:
- PENDING_APPROVAL = Just generated, not approved yet
- APPROVED = Ready for execution Monday
- EXECUTED = Orders submitted to Alpaca

**File Locations**:
- Project: `C:\Users\wjcor\OneDrive\Desktop\Sentinel\`
- Launcher: `C:\Users\wjcor\OneDrive\Desktop\Run_Sentinel.bat`
- Plans: `proposed_trades_YYYY-MM-DD.json`

---

*Quick Start Guide - Sentinel Corporation*
*Updated: November 1, 2025*
