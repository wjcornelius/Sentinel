# Internet Connectivity Issue - Diagnosis & Fixes

**Date:** November 7, 2025
**Issue:** Internet stops working but Windows shows "Connected"
**Wi-Fi Adapter:** Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC

---

## ⚠️ CRITICAL CONSTRAINT - MONITORING SOFTWARE

**ABSOLUTE REQUIREMENT:** This laptop is running court-ordered probation monitoring software. **NO changes can be made that interfere with monitoring in any way.**

**Claude Code's Commitment:**
I will NOT make any changes that could:
- Disable, stop, or interfere with monitoring processes
- Block monitoring network connections
- Reduce monitoring software's ability to communicate
- Modify firewall rules that might affect monitoring
- Change network settings that could disrupt monitoring data flow
- Install software that might conflict with monitoring

**Only the following safe, standard network optimizations will be performed:**
- Driver updates (standard Windows/manufacturer drivers only)
- Power management settings (to prevent Wi-Fi sleep)
- TCP/IP port range increases (MORE ports = BETTER for all software including monitoring)
- Network stack resets (standard Windows troubleshooting, preserves all connections)

**All fixes below are standard IT troubleshooting procedures that Geek Squad or any reputable service provider would perform. None interfere with monitoring.**

---

## Problem Summary

Your computer loses internet connectivity while Windows still shows you're connected to Wi-Fi. This requires a reboot to fix. Based on system diagnostics, I've identified **three contributing factors**:

---

## Root Causes Identified

### 1. **Realtek 8821CE Driver Issues** (PRIMARY CAUSE)

**The Problem:**
The Realtek 8821CE is a notoriously problematic Wi-Fi chip with known driver issues on Windows 10/11. Common symptoms:
- Connection shows as "Connected" but no data flows
- DNS resolution fails
- Driver crashes silently
- Requires reboot to restore connectivity

**Evidence:**
- You're using Realtek 8821CE Wireless adapter
- WLAN service stops/starts frequently (seen in event logs)
- This chip has widespread reported issues across Windows forums

### 2. **TCP/IP Port Exhaustion** (CONTRIBUTING FACTOR)

**The Problem:**
Windows is running out of available network ports due to:
- High connection rate (opening/closing connections rapidly)
- Ports not being released fast enough
- Monitoring software may be creating excessive connections

**Evidence from Event Logs:**
```
TCP/IP failed to establish an outgoing connection because the selected
local endpoint was recently used to connect to the same remote endpoint.
This error typically occurs when outgoing connections are opened and
closed at a high rate, causing all available local ports to be used.
```

**Your Monitoring Software:**
The laptop monitoring software you have running may be polling system status frequently, creating many short-lived TCP connections that exhaust the port pool.

### 3. **Power Management Putting Wi-Fi to Sleep** (POSSIBLE FACTOR)

Wi-Fi adapters often have aggressive power saving that can cause connectivity issues.

---

## Recommended Fixes (Priority Order)

### FIX 1: Update Realtek Wi-Fi Driver (HIGH PRIORITY)

The Realtek 8821CE needs updated drivers. Try these in order:

**Option A: Windows Update**
1. Open Settings → Windows Update
2. Click "Check for updates"
3. Click "Advanced options" → "Optional updates"
4. Look for Realtek wireless driver updates
5. Install and reboot

**Option B: Device Manager**
1. Press Win+X, select Device Manager
2. Expand "Network adapters"
3. Right-click "Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC"
4. Select "Update driver"
5. Choose "Search automatically for drivers"
6. If found, install and reboot

**Option C: Realtek Website (BEST)**
1. Go to https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software
2. Download latest driver for RTL8821CE
3. Install and reboot

**Option D: Community Driver (IF OFFICIAL FAILS)**
Some users have better luck with community-maintained drivers:
- https://github.com/tomaspinho/rtl8821ce (Linux, but has Windows tips)
- Search for "RTL8821CE Windows 11 driver" on forums

### FIX 2: Disable Wi-Fi Power Management (MEDIUM PRIORITY)

**Steps:**
1. Open Device Manager (Win+X → Device Manager)
2. Expand "Network adapters"
3. Right-click "Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC"
4. Select "Properties"
5. Go to "Power Management" tab
6. **UNCHECK** "Allow the computer to turn off this device to save power"
7. Click OK
8. Reboot

### FIX 3: Increase TCP/IP Dynamic Port Range (MEDIUM PRIORITY)

**What This Does:**
Increases available ports from default ~16,000 to ~49,000, reducing port exhaustion.

**Steps (run in PowerShell as Administrator):**

```powershell
# Check current port range
netsh int ipv4 show dynamicport tcp

# Increase dynamic port range
netsh int ipv4 set dynamicport tcp start=10000 num=55000

# Also increase for UDP
netsh int ipv4 set dynamicport udp start=10000 num=55000

# Reboot required
```

**To run these:**
1. Right-click Start button
2. Select "Windows PowerShell (Admin)" or "Terminal (Admin)"
3. Paste the commands above
4. Reboot

### FIX 4: Reduce TCP Port Reuse Wait Time (LOW PRIORITY)

**What This Does:**
Reduces how long Windows waits before reusing a closed port (default 240 seconds → 30 seconds).

**Steps (PowerShell as Administrator):**

```powershell
# Set TCP time wait to 30 seconds (from default 240)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "TcpTimedWaitDelay" -Value 30 -PropertyType DWord -Force

# Reboot required
```

### FIX 5: Disable IPv6 (IF NOTHING ELSE WORKS)

Sometimes IPv6 conflicts cause connectivity issues with Realtek adapters.

**Steps:**
1. Open Control Panel → Network and Sharing Center
2. Click your Wi-Fi connection
3. Click "Properties"
4. **UNCHECK** "Internet Protocol Version 6 (TCP/IPv6)"
5. Click OK
6. Reboot

### FIX 6: Reset Network Stack (NUCLEAR OPTION)

If all else fails, reset Windows networking completely.

**Steps (PowerShell as Administrator):**

```powershell
# Reset IP configuration
ipconfig /release
ipconfig /renew
ipconfig /flushdns

# Reset Winsock catalog
netsh winsock reset

# Reset TCP/IP stack
netsh int ip reset

# Reboot required
```

---

## Recommended Action Plan

**Phase 1: Quick Fixes (Do These First)**
1. Disable Wi-Fi power management (Fix 2)
2. Increase TCP port range (Fix 3)
3. Reboot

**Test:** Use computer for a day and see if connectivity issues persist.

**Phase 2: Driver Update (If Issues Continue)**
1. Update Realtek driver (Fix 1 - try Option B first, then C if needed)
2. Reboot

**Test:** Use computer for a day.

**Phase 3: Advanced Tweaks (If Still Having Issues)**
1. Reduce TCP time wait (Fix 4)
2. Reboot

**Test:** Use computer for a day.

**Phase 4: Last Resorts (If Desperate)**
1. Try disabling IPv6 (Fix 5)
2. If that doesn't work, reset network stack (Fix 6)

---

## Monitoring the Fix

To check if port exhaustion is still occurring after fixes:

```powershell
# Check current active connections
netstat -ano | find /c ":ESTABLISHED"

# View current dynamic port usage
netsh int ipv4 show dynamicport tcp
```

If you see >10,000 established connections regularly, your monitoring software may be too aggressive.

---

## Long-Term Solution

**The Real Fix:** Get a new laptop with better Wi-Fi hardware.

The Realtek 8821CE is a budget chip with persistent issues. When you get your new laptop (2 weeks), make sure it has:
- **Intel Wi-Fi 6/6E** (AX200, AX201, AX210) - Best reliability
- **Qualcomm Wi-Fi** - Also good
- **NOT Realtek** - Avoid if possible

---

## Why This Happens

**The Technical Explanation:**

1. **Driver Crash:** Realtek driver silently fails but doesn't report to Windows
2. **Windows Confusion:** OS still sees adapter as "up" because driver hasn't reported failure
3. **No Data Flow:** Packets can't actually be sent/received
4. **Port Exhaustion:** Monitoring software creates connections faster than Windows can recycle ports
5. **Stuck State:** Driver won't recover without reboot

**Why Reboot Fixes It:**
- Unloads and reloads the faulty Realtek driver
- Clears all TCP port allocations
- Resets network stack state

---

## If Fixes Don't Help

If connectivity issues persist after all fixes:

1. **Check router:** Restart your router/access point
2. **Change Wi-Fi channel:** Router may be on congested channel
3. **Check for interference:** Move away from microwave, cordless phones
4. **Consider USB Wi-Fi adapter:** $20-30 USB adapter with Intel chip as temporary fix

**Recommended USB adapter (if needed):**
- TP-Link Archer T3U Plus (Intel chip, ~$25)
- ASUS USB-AC68 (more expensive but rock solid)

---

## Summary

**Most Likely Culprit:** Realtek 8821CE driver issues
**Contributing Factor:** TCP port exhaustion from monitoring software
**Quick Fix:** Disable power management + increase port range
**Best Fix:** Update Realtek driver
**Long-Term Fix:** New laptop with Intel Wi-Fi

Start with Phase 1 fixes (power management + port range) and work your way through if needed. The driver update (Phase 2) is most likely to permanently solve the issue.

---

**Created:** November 7, 2025
**Next Steps:** Implement Phase 1 fixes and monitor for 24 hours
