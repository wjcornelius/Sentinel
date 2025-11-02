"""
Mode Manager Module
===================
Manages online/offline mode for Sentinel Corporation.

Logic:
- Default: ONLINE (live trading mode)
- Auto-offline: Market closed OR already traded today
- Manual override: Can force offline when auto-detection says online
- Config-driven: FORCE_OFFLINE_MODE in config.py

Future-proof: Supports multiple Alpaca accounts via config.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from Utils.market_status import MarketStatus
from Utils.alpaca_client import AlpacaClient


class ModeManager:
    """
    Manages Sentinel Corporation's operating mode (online/offline).
    """

    MODE_ONLINE = 'ONLINE'
    MODE_OFFLINE = 'OFFLINE'

    def __init__(self, alpaca_client=None):
        """
        Initialize Mode Manager.

        Args:
            alpaca_client: AlpacaClient instance (optional, will create if needed)
        """
        self.alpaca_client = alpaca_client
        self.market_status = None

        # Initialize market status checker (needs Alpaca client)
        if self.alpaca_client:
            self.market_status = MarketStatus(self.alpaca_client)

        self._current_mode = None
        self._mode_reason = None
        self._manual_override = None

    def determine_mode(self):
        """
        Determine what mode SC should be in based on all factors.

        Priority (highest to lowest):
        1. Manual override (FORCE_OFFLINE_MODE in config)
        2. Market status (closed, already traded, etc.)
        3. Default (ONLINE)

        Returns:
            tuple: (mode, reason)
                mode: 'ONLINE' or 'OFFLINE'
                reason: Human-readable explanation
        """
        # Priority 1: Check for manual override in config
        if hasattr(config, 'FORCE_OFFLINE_MODE') and config.FORCE_OFFLINE_MODE:
            return (self.MODE_OFFLINE, "Manual override: FORCE_OFFLINE_MODE = True in config")

        # Priority 2: Check if Alpaca is disabled (pure simulation mode)
        if hasattr(config, 'ALPACA_PAPER_TRADING_ENABLED'):
            if not config.ALPACA_PAPER_TRADING_ENABLED:
                return (self.MODE_OFFLINE, "Alpaca disabled: ALPACA_PAPER_TRADING_ENABLED = False")
        elif hasattr(config, 'LIVE_TRADING'):
            # Backward compatibility with old LIVE_TRADING flag
            if not config.LIVE_TRADING:
                return (self.MODE_OFFLINE, "Simulation mode: LIVE_TRADING = False")

        # Priority 3: Check market status (if Alpaca is connected)
        if self.market_status:
            should_be_online, reason = self.market_status.should_be_online()

            if should_be_online:
                return (self.MODE_ONLINE, "Market is open and no trades submitted today")
            else:
                return (self.MODE_OFFLINE, reason)

        # Priority 4: Default to OFFLINE if no Alpaca client (safety)
        if not self.alpaca_client:
            return (self.MODE_OFFLINE, "No Alpaca client connected (safety default)")

        # Priority 5: Default to ONLINE (should rarely reach here)
        return (self.MODE_ONLINE, "Default mode (no restrictions detected)")

    def get_current_mode(self):
        """
        Get current operating mode.

        Returns:
            str: 'ONLINE' or 'OFFLINE'
        """
        if self._current_mode is None:
            self._current_mode, self._mode_reason = self.determine_mode()

        return self._current_mode

    def get_mode_reason(self):
        """
        Get reason for current mode.

        Returns:
            str: Human-readable explanation
        """
        if self._mode_reason is None:
            self._current_mode, self._mode_reason = self.determine_mode()

        return self._mode_reason

    def is_online(self):
        """
        Check if currently in online mode.

        Returns:
            bool: True if online
        """
        return self.get_current_mode() == self.MODE_ONLINE

    def is_offline(self):
        """
        Check if currently in offline mode.

        Returns:
            bool: True if offline
        """
        return self.get_current_mode() == self.MODE_OFFLINE

    def force_offline(self):
        """
        Manually force offline mode.
        """
        self._current_mode = self.MODE_OFFLINE
        self._mode_reason = "Manual override: Forced offline by user"
        self._manual_override = self.MODE_OFFLINE

    def force_online(self):
        """
        Manually force online mode (use with caution!).
        Will still check if market is open and no trades today.

        Returns:
            tuple: (success: bool, message: str)
        """
        # Safety check: Make sure market is open
        if self.market_status:
            if not self.market_status.is_market_open_now():
                return (False, "Cannot force online: Market is closed")

            if self.market_status.already_traded_today():
                return (False, "Cannot force online: Already traded today")

        # OK to force online
        self._current_mode = self.MODE_ONLINE
        self._mode_reason = "Manual override: Forced online by user"
        self._manual_override = self.MODE_ONLINE

        return (True, "Forced online mode activated")

    def clear_override(self):
        """
        Clear manual override and return to auto-detection.
        """
        self._manual_override = None
        self._current_mode = None
        self._mode_reason = None

        # Re-determine mode
        return self.determine_mode()

    def get_mode_summary(self):
        """
        Get comprehensive mode information for display.

        Returns:
            dict: Mode information
        """
        current_mode = self.get_current_mode()
        reason = self.get_mode_reason()

        summary = {
            'mode': current_mode,
            'is_online': self.is_online(),
            'is_offline': self.is_offline(),
            'reason': reason,
            'manual_override': self._manual_override is not None,
            'override_mode': self._manual_override,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Add market status if available
        if self.market_status:
            market_summary = self.market_status.get_status_summary()
            summary['market_status'] = market_summary

        # Add Alpaca connection status
        if self.alpaca_client:
            conn_info = self.alpaca_client.get_connection_info()
            summary['alpaca_connected'] = conn_info['connected']
            summary['alpaca_paper'] = conn_info['paper_trading']
        else:
            summary['alpaca_connected'] = False
            summary['alpaca_paper'] = None

        return summary

    def can_submit_orders(self):
        """
        Check if orders can be submitted in current mode.

        Returns:
            tuple: (can_submit: bool, reason: str)
        """
        if not self.is_online():
            return (False, "Cannot submit orders: System is in OFFLINE mode")

        if not self.alpaca_client:
            return (False, "Cannot submit orders: No Alpaca client connected")

        if not self.alpaca_client.is_connected():
            return (False, "Cannot submit orders: Alpaca not connected")

        # Check if paper trading is enabled
        if hasattr(config, 'ALPACA_PAPER_TRADING_ENABLED'):
            if not config.ALPACA_PAPER_TRADING_ENABLED:
                return (False, "Cannot submit orders: ALPACA_PAPER_TRADING_ENABLED = False")

        return (True, "Ready to submit orders")

    def get_available_actions(self):
        """
        Get list of available actions in current mode.

        Returns:
            dict: Available actions with descriptions
        """
        actions = {}

        # Always available
        actions['view_dashboard'] = "View live dashboard"
        actions['view_positions'] = "View current positions (from Alpaca)"
        actions['view_account'] = "View account info (from Alpaca)"
        actions['run_analysis'] = "Run research/analysis (educational mode)"

        # Mode-specific actions
        if self.is_online():
            actions['submit_orders'] = "Submit orders to Alpaca"
            actions['force_offline'] = "Force offline mode (manual override)"
        else:
            # In offline mode, check if can force online
            if self.market_status:
                if self.market_status.is_market_open_now() and not self.market_status.already_traded_today():
                    actions['force_online'] = "Force online mode (manual override)"

        actions['clear_override'] = "Clear manual override (return to auto-detection)"

        return actions


# Convenience function
def create_mode_manager(alpaca_client=None):
    """
    Create a mode manager.

    Args:
        alpaca_client: AlpacaClient instance (optional)

    Returns:
        ModeManager instance
    """
    return ModeManager(alpaca_client=alpaca_client)


if __name__ == "__main__":
    # Test the mode manager
    print("=" * 80)
    print("MODE MANAGER MODULE TEST")
    print("=" * 80)
    print()

    try:
        # Create Alpaca client first
        from Utils.alpaca_client import create_alpaca_client

        print("Connecting to Alpaca...")
        alpaca = create_alpaca_client()

        if not alpaca.is_connected():
            print("✗ Not connected to Alpaca. Check API keys in config.py")
            print()
            print("Testing without Alpaca (limited functionality)...")
            alpaca = None

        # Create mode manager
        mm = create_mode_manager(alpaca_client=alpaca)

        # Get mode summary
        summary = mm.get_mode_summary()

        print("Current Mode Information:")
        print(f"  Mode:              {summary['mode']}")
        print(f"  Is Online:         {summary['is_online']}")
        print(f"  Is Offline:        {summary['is_offline']}")
        print(f"  Reason:            {summary['reason']}")
        print(f"  Manual Override:   {summary['manual_override']}")
        print(f"  Alpaca Connected:  {summary['alpaca_connected']}")
        print(f"  Alpaca Paper:      {summary['alpaca_paper']}")
        print()

        if 'market_status' in summary:
            ms = summary['market_status']
            print("Market Status:")
            print(f"  Current Time (ET): {ms['current_time_et']}")
            print(f"  Is Market Day:     {ms['is_market_day']}")
            print(f"  Is Market Open:    {ms['is_market_open_now']}")
            print(f"  Already Traded:    {ms['already_traded_today']}")
            print()

        # Check if can submit orders
        can_submit, submit_reason = mm.can_submit_orders()
        print(f"Can Submit Orders: {can_submit}")
        print(f"  Reason: {submit_reason}")
        print()

        # Show available actions
        actions = mm.get_available_actions()
        print("Available Actions:")
        for action, description in actions.items():
            print(f"  - {action}: {description}")
        print()

        # Test manual override
        print("Testing manual override...")
        mm.force_offline()
        print(f"  After force_offline(): Mode = {mm.get_current_mode()}")

        success, msg = mm.force_online()
        print(f"  After force_online(): {msg}")
        print(f"  Mode = {mm.get_current_mode()}")

        mm.clear_override()
        print(f"  After clear_override(): Mode = {mm.get_current_mode()}")
        print()

        print("=" * 80)
        print("[SUCCESS] Mode Manager test completed successfully")
        print("=" * 80)

    except Exception as e:
        print()
        print("=" * 80)
        print(f"[ERROR] Error: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
