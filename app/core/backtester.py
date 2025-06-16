"""
Backtesting engine for running trading strategies and tracking results.
"""

from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    """A single trade (entry/exit) in the backtest."""
    entry_date: datetime
    entry_price: float
    position_size: float  # Number of shares/contracts
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    position_type: str = 'long'  # 'long' or 'short'
    status: str = 'open'  # 'open' or 'closed'
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None

class Backtester:
    """
    Runs a backtest for a given set of signals and price data.
    Handles position management, equity curve, and trade logging.
    """
    def __init__(
        self,
        data: pd.DataFrame,
        signals: List[str],
        initial_capital: float = 100000.0,
        position_size: float = 1.0,
        commission: float = 0.001
    ):
        self.data = data
        self.signals = signals
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.commission = commission
        self.current_capital = initial_capital
        self.current_position = None
        self.trades: List[Trade] = []
        self.equity_curve = pd.Series(index=data.index, dtype=float)
        self.equity_curve.iloc[0] = initial_capital

    def run(self) -> pd.DataFrame:
        """
        Main backtest loop. Steps through the data, processes signals, and updates equity.
        Returns the equity curve as a DataFrame.
        """
        for i in range(1, len(self.data)):
            current_date = self.data.index[i]
            current_price = self.data['Close'].iloc[i]
            current_signal = self.signals[i]
            # Carry forward previous equity by default
            self.equity_curve.iloc[i] = self.equity_curve.iloc[i-1]
            # If we have an open position, update its value
            if self.current_position is not None:
                if self.current_position.position_type == 'long':
                    position_value = self.current_position.position_size * current_price
                else:
                    position_value = self.current_position.position_size * (2 * self.current_position.entry_price - current_price)
                # Check for exit
                if current_signal == 'sell' and self.current_position.position_type == 'long':
                    self._close_position(current_date, current_price)
                elif current_signal == 'buy' and self.current_position.position_type == 'short':
                    self._close_position(current_date, current_price)
                self.equity_curve.iloc[i] = self.current_capital + position_value
            # If no open position, check for entry
            if current_signal == 'buy' and self.current_position is None:
                self._open_position(current_date, current_price, 'long')
            elif current_signal == 'sell' and self.current_position is None:
                self._open_position(current_date, current_price, 'short')
        # Close any open position at the end
        if self.current_position is not None:
            self._close_position(self.data.index[-1], self.data['Close'].iloc[-1])
        return pd.DataFrame({'Equity Curve': self.equity_curve})

    def _open_position(self, date: datetime, price: float, position_type: str):
        # Open a new position (long or short)
        position_size = (self.current_capital * self.position_size) / price
        commission_amount = position_size * price * self.commission
        self.current_position = Trade(
            entry_date=date,
            entry_price=price,
            position_size=position_size,
            position_type=position_type
        )
        self.current_capital -= commission_amount

    def _close_position(self, date: datetime, price: float):
        # Close the current position and log the trade
        if self.current_position is None:
            return
        commission_amount = self.current_position.position_size * price * self.commission
        if self.current_position.position_type == 'long':
            pnl = (price - self.current_position.entry_price) * self.current_position.position_size
        else:
            pnl = (self.current_position.entry_price - price) * self.current_position.position_size
        pnl_pct = (pnl / (self.current_position.entry_price * self.current_position.position_size)) * 100
        self.current_position.exit_date = date
        self.current_position.exit_price = price
        self.current_position.status = 'closed'
        self.current_position.pnl = pnl
        self.current_position.pnl_pct = pnl_pct
        self.current_capital += pnl - commission_amount
        self.trades.append(self.current_position)
        self.current_position = None

    def get_trade_log(self) -> pd.DataFrame:
        """
        Returns a DataFrame of all trades (entry/exit, PnL, etc).
        """
        if not self.trades:
            return pd.DataFrame()
        trade_data = []
        for trade in self.trades:
            trade_data.append({
                'Entry Date': trade.entry_date,
                'Entry Price': trade.entry_price,
                'Position Size': trade.position_size,
                'Exit Date': trade.exit_date,
                'Exit Price': trade.exit_price,
                'Position Type': trade.position_type,
                'PnL': trade.pnl,
                'PnL %': trade.pnl_pct,
                'Status': trade.status
            })
        return pd.DataFrame(trade_data)

    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Returns a dictionary of summary performance metrics for the backtest.
        """
        if not self.trades:
            return {}
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        losing_trades = len([t for t in self.trades if t.pnl < 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        avg_win = np.mean([t.pnl for t in self.trades if t.pnl > 0]) if winning_trades > 0 else 0
        avg_loss = np.mean([t.pnl for t in self.trades if t.pnl < 0]) if losing_trades > 0 else 0
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        return {
            'Total Trades': total_trades,
            'Win Rate': win_rate * 100,
            'Average Win': avg_win,
            'Average Loss': avg_loss,
            'Profit Factor': profit_factor,
            'Total Return': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
        }
# TODO: Add support for partial fills and slippage in the future 