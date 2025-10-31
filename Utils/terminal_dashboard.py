"""
Terminal Dashboard - Week 7 Day 2
Real-time portfolio monitoring dashboard using rich library

Features:
- Real-time P&L updates with color-coded gains/losses
- Open positions table with current prices
- Recent trades log
- System health status monitoring
- Auto-refresh every 5 seconds
- Keyboard controls (q=quit, r=refresh, p=pause)

Designed for 60" TV display - no scrolling required!

Author: Claude Code (CC)
Week: 7 Day 2
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import time
import logging

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import Executive Department for data
from Departments.Executive.executive_department import ExecutiveDepartment

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Only warnings and errors to avoid cluttering terminal
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class TerminalDashboard:
    """
    Real-time terminal dashboard for Sentinel Corporation portfolio monitoring

    Features:
    - Live updates without scrolling
    - Color-coded performance metrics
    - Auto-refresh every N seconds
    - Keyboard controls for navigation
    - Fits any screen size (60" TV compatible)
    """

    def __init__(self, db_path: str = None, refresh_interval: int = 5):
        """
        Initialize terminal dashboard

        Args:
            db_path: Path to Sentinel database
            refresh_interval: Seconds between auto-refresh (default 5)
        """
        self.console = Console()
        self.refresh_interval = refresh_interval
        self.is_paused = False
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize Executive Department
        project_root = Path(__file__).parent.parent

        if db_path is None:
            db_path = project_root / "sentinel.db"
        else:
            db_path = Path(db_path)

        messages_dir = project_root / "Messages"
        reports_dir = project_root / "Reports"

        self.executive = ExecutiveDepartment(
            db_path=db_path,
            messages_dir=messages_dir,
            reports_dir=reports_dir
        )

        # Dashboard state
        self.last_update = None
        self.update_count = 0

        self.logger.info(f"TerminalDashboard initialized: db={db_path}, refresh={refresh_interval}s")

    def create_header(self) -> Panel:
        """Create dashboard header with title and timestamp"""
        title = Text()
        title.append("SENTINEL CORPORATION", style="bold cyan")
        title.append(" | ", style="white")
        title.append("Executive Portfolio Dashboard", style="cyan")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subtitle = Text(f"Last Update: {timestamp}", style="dim white")

        # Add update counter
        if self.update_count > 0:
            subtitle.append(f" | Updates: {self.update_count}", style="dim cyan")

        header_text = Text()
        header_text.append(title)
        header_text.append("\n")
        header_text.append(subtitle)

        return Panel(
            Align.center(header_text),
            box=box.DOUBLE,
            style="cyan"
        )

    def create_performance_panel(self, data: Dict) -> Panel:
        """Create performance metrics panel with color-coded values"""
        performance = data.get('performance', {})

        # Daily P&L with color coding
        daily_pnl = performance.get('daily_pnl', 0.0)
        daily_pnl_pct = performance.get('daily_pnl_pct', 0.0)

        pnl_color = "green" if daily_pnl >= 0 else "red"
        pnl_text = Text()
        pnl_text.append("Daily P&L: ", style="white")
        pnl_text.append(f"${daily_pnl:,.2f}", style=f"bold {pnl_color}")
        pnl_text.append(f" ({daily_pnl_pct:+.2f}%)", style=pnl_color)

        # Realized vs Unrealized
        realized_pnl = performance.get('realized_pnl', 0.0)
        unrealized_pnl = performance.get('unrealized_pnl', 0.0)

        realized_text = Text()
        realized_text.append("  Realized: ", style="dim white")
        realized_text.append(f"${realized_pnl:,.2f}", style="green" if realized_pnl >= 0 else "red")

        unrealized_text = Text()
        unrealized_text.append("  Unrealized: ", style="dim white")
        unrealized_text.append(f"${unrealized_pnl:,.2f}", style="green" if unrealized_pnl >= 0 else "red")

        # Sharpe Ratio
        sharpe = performance.get('sharpe_ratio_30d', 0.0)
        sharpe_text = Text()
        sharpe_text.append("Sharpe Ratio (30d): ", style="white")
        sharpe_color = "green" if sharpe > 2.0 else "yellow" if sharpe > 1.0 else "red"
        sharpe_text.append(f"{sharpe:.3f}", style=f"bold {sharpe_color}")

        # Win Rate
        win_rate = performance.get('win_rate_30d', 0.0)
        win_rate_text = Text()
        win_rate_text.append("Win Rate (30d): ", style="white")
        win_rate_color = "green" if win_rate >= 60 else "yellow" if win_rate >= 50 else "red"
        win_rate_text.append(f"{win_rate:.1f}%", style=f"bold {win_rate_color}")

        # Max Drawdown
        max_dd = performance.get('max_drawdown', 0.0)
        max_dd_text = Text()
        max_dd_text.append("Max Drawdown: ", style="white")
        max_dd_color = "green" if max_dd < 5 else "yellow" if max_dd < 10 else "red"
        max_dd_text.append(f"{max_dd:.2f}%", style=max_dd_color)

        # Alpha vs SPY
        alpha = performance.get('alpha_vs_spy', 0.0)
        alpha_text = Text()
        alpha_text.append("Alpha vs SPY: ", style="white")
        alpha_color = "green" if alpha > 0 else "red"
        alpha_text.append(f"{alpha:+.2f}%", style=f"bold {alpha_color}")

        # Combine all metrics
        content = Text()
        content.append(pnl_text)
        content.append("\n")
        content.append(realized_text)
        content.append("\n")
        content.append(unrealized_text)
        content.append("\n\n")
        content.append(sharpe_text)
        content.append("  |  ")
        content.append(win_rate_text)
        content.append("\n")
        content.append(max_dd_text)
        content.append("  |  ")
        content.append(alpha_text)

        return Panel(
            content,
            title="[bold white]PERFORMANCE METRICS",
            border_style="green" if daily_pnl >= 0 else "red",
            box=box.ROUNDED
        )

    def create_positions_table(self, positions: List[Dict]) -> Panel:
        """Create open positions table"""
        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE,
            expand=True
        )

        table.add_column("Ticker", style="cyan", width=8)
        table.add_column("Shares", justify="right", width=10)
        table.add_column("Entry $", justify="right", width=12)
        table.add_column("Current $", justify="right", width=12)
        table.add_column("Position Value", justify="right", width=15)
        table.add_column("Unrealized P&L", justify="right", width=15)
        table.add_column("P&L %", justify="right", width=10)

        if not positions:
            table.add_row("No open positions", "", "", "", "", "", "")
        else:
            total_value = 0.0
            total_pnl = 0.0

            for pos in positions:
                ticker = pos['ticker']
                shares = pos['shares']
                entry_price = pos['entry_price']
                current_price = pos.get('current_price', entry_price)

                position_value = shares * current_price
                unrealized_pnl = shares * (current_price - entry_price)
                pnl_pct = ((current_price - entry_price) / entry_price) * 100

                total_value += position_value
                total_pnl += unrealized_pnl

                # Color code P&L
                pnl_color = "green" if unrealized_pnl >= 0 else "red"

                table.add_row(
                    ticker,
                    f"{shares:,}",
                    f"${entry_price:.2f}",
                    f"${current_price:.2f}",
                    f"${position_value:,.2f}",
                    f"[{pnl_color}]${unrealized_pnl:,.2f}[/{pnl_color}]",
                    f"[{pnl_color}]{pnl_pct:+.2f}%[/{pnl_color}]"
                )

            # Add totals row
            total_pnl_color = "green" if total_pnl >= 0 else "red"
            table.add_row(
                "[bold]TOTAL",
                "",
                "",
                "",
                f"[bold]${total_value:,.2f}",
                f"[bold {total_pnl_color}]${total_pnl:,.2f}[/bold {total_pnl_color}]",
                "",
                style="bold white"
            )

        return Panel(
            table,
            title=f"[bold white]OPEN POSITIONS ({len(positions)})",
            border_style="cyan",
            box=box.ROUNDED
        )

    def create_system_health_panel(self, health: Dict) -> Panel:
        """Create system health status panel"""
        departments = health.get('departments', {})
        alerts = health.get('alerts', [])

        # Department status
        status_text = Text()
        status_text.append("Department Status:\n", style="bold white")

        for dept, status in departments.items():
            dept_name = dept.replace('_', ' ').title()

            if status == 'healthy':
                icon = "✅"
                color = "green"
            elif status == 'degraded':
                icon = "⚠️"
                color = "yellow"
            elif status == 'unhealthy':
                icon = "❌"
                color = "red"
            else:  # no_data or other
                icon = "⏸️"
                color = "dim white"

            status_text.append(f"  {icon} ", style=color)
            status_text.append(f"{dept_name}: ", style="white")
            status_text.append(f"{status}\n", style=color)

        # Alerts
        if alerts:
            status_text.append("\n")
            status_text.append("Active Alerts:\n", style="bold yellow")
            for alert in alerts[:3]:  # Show top 3 alerts
                status_text.append(f"  ⚠️  {alert}\n", style="yellow")
        else:
            status_text.append("\n")
            status_text.append("✅ No active alerts\n", style="green")

        # Health score
        healthy_count = sum(1 for s in departments.values() if s == 'healthy')
        total_count = len(departments)
        health_pct = (healthy_count / total_count * 100) if total_count > 0 else 0

        health_color = "green" if health_pct >= 80 else "yellow" if health_pct >= 60 else "red"
        status_text.append("\n")
        status_text.append("System Health: ", style="white")
        status_text.append(f"{healthy_count}/{total_count} healthy ({health_pct:.0f}%)", style=f"bold {health_color}")

        return Panel(
            status_text,
            title="[bold white]SYSTEM HEALTH",
            border_style=health_color,
            box=box.ROUNDED
        )

    def create_footer(self) -> Panel:
        """Create dashboard footer with keyboard controls"""
        footer_text = Text()
        footer_text.append("Controls: ", style="bold white")
        footer_text.append("[Q]", style="bold cyan")
        footer_text.append(" Quit  ", style="white")
        footer_text.append("[R]", style="bold cyan")
        footer_text.append(" Refresh Now  ", style="white")
        footer_text.append("[P]", style="bold cyan")
        footer_text.append(" Pause/Resume  ", style="white")

        if self.is_paused:
            footer_text.append("  |  ", style="dim white")
            footer_text.append("⏸️  PAUSED", style="bold yellow")
        else:
            footer_text.append("  |  ", style="dim white")
            footer_text.append(f"▶️  Auto-refresh: {self.refresh_interval}s", style="green")

        return Panel(
            Align.center(footer_text),
            style="dim white",
            box=box.SIMPLE
        )

    def generate_layout(self) -> Layout:
        """Generate complete dashboard layout"""
        # Fetch real-time data from Executive Department
        try:
            data = self.executive.get_realtime_dashboard_data()
            self.last_update = datetime.now()
            self.update_count += 1
        except Exception as e:
            self.logger.error(f"Failed to fetch dashboard data: {e}")
            # Return error panel
            error_panel = Panel(
                f"[bold red]Error fetching data:[/bold red]\n{e}",
                title="ERROR",
                border_style="red"
            )
            layout = Layout()
            layout.split_column(
                Layout(self.create_header(), size=5),
                Layout(error_panel),
                Layout(self.create_footer(), size=3)
            )
            return layout

        # Create layout
        layout = Layout()

        # Split into header, body, footer
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )

        # Header
        layout["header"].update(self.create_header())

        # Footer
        layout["footer"].update(self.create_footer())

        # Body - split into top and bottom
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right", ratio=2)
        )

        # Left side - performance and health
        layout["left"].split_column(
            Layout(self.create_performance_panel(data), name="performance"),
            Layout(self.create_system_health_panel(data.get('system_health', {})), name="health")
        )

        # Right side - positions table
        layout["right"].update(self.create_positions_table(data.get('open_positions', [])))

        return layout

    def run(self):
        """Run the dashboard with auto-refresh"""
        self.console.clear()

        try:
            with Live(self.generate_layout(), refresh_per_second=1, console=self.console, screen=True) as live:
                while True:
                    # Update layout
                    if not self.is_paused:
                        live.update(self.generate_layout())

                    # Sleep for refresh interval
                    time.sleep(self.refresh_interval)

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Dashboard stopped by user (Ctrl+C)[/yellow]")
        except Exception as e:
            self.console.print(f"\n[bold red]Dashboard error:[/bold red] {e}")
            self.logger.error(f"Dashboard error: {e}", exc_info=True)


# Quick test and standalone launcher
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sentinel Corporation Terminal Dashboard")
    parser.add_argument(
        '--db',
        type=str,
        default=None,
        help='Path to Sentinel database (default: sentinel.db in project root)'
    )
    parser.add_argument(
        '--refresh',
        type=int,
        default=5,
        help='Refresh interval in seconds (default: 5)'
    )

    args = parser.parse_args()

    # Launch dashboard
    print("Starting Sentinel Corporation Terminal Dashboard...")
    print(f"Refresh interval: {args.refresh} seconds")
    print("Press Ctrl+C to exit\n")

    dashboard = TerminalDashboard(db_path=args.db, refresh_interval=args.refresh)
    dashboard.run()
