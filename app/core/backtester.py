#libraries used for backtesting
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime

#dataclass to store the trade information
@dataclass
class Trade:
    #entry date, entry price, position size, exit date, exit price, position type, status, pnl and pnl percentage
    entry_date: datetime
    entry_price: float
    position_size: float
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    position_type: str = 'long'
    status: str = 'open'
    pnl: Optional[float] = None
    pnl_pct: Optional[float] = None

#class to run the backtest
class Backtester:

    #initializing the backtester
    def __init__(
        self,
        data: pd.DataFrame,
        signals: List[str],
        #initial capital
        initial_capital: float = 100000.0,
        #position size
        position_size: float = 1.0,
        #commission rate
        commission: float = 0.001
    ):
        #dataframe of the price data
        self.data = data
        #list of the signals
        self.signals = signals
        #initial capital
        self.initial_capital = initial_capital
        #position size
        self.position_size = position_size
        #commission rate
        self.commission = commission
        #current capital
        self.current_capital = initial_capital
        #current position
        self.current_position = None
        #list of trades
        self.trades: List[Trade] = []
        #equity curve
        self.equity_curve = pd.Series(index=data.index, dtype=float)
        #initial equity curve
        self.equity_curve.iloc[0] = initial_capital

    #function to run the backtest
    def run(self) -> pd.DataFrame:
        #loop through the data
        for i in range(1, len(self.data)):
            current_date = self.data.index[i]
            current_price = self.data['Close'].iloc[i]
            current_signal = self.signals[i]
            #carry forward previous equity by default
            self.equity_curve.iloc[i] = self.equity_curve.iloc[i-1]
            #if we have an open position, update its value
            if self.current_position is not None:
                #calculating the position value for a long position
                if self.current_position.position_type == 'long':
                    position_value = self.current_position.position_size * current_price
                else:
                    #calculating the position value for a short position
                    position_value = self.current_position.position_size * (2 * self.current_position.entry_price - current_price)
                #check for exit
                if current_signal == 'sell' and self.current_position.position_type == 'long':
                    self._close_position(current_date, current_price)
                elif current_signal == 'buy' and self.current_position.position_type == 'short':
                    self._close_position(current_date, current_price)
                #updating the equity curve for the current position, aka the total value of the portfolio
                self.equity_curve.iloc[i] = self.current_capital + position_value
            #if no open position, check for entry
            if current_signal == 'buy' and self.current_position is None:
                self._open_position(current_date, current_price, 'long')
            elif current_signal == 'sell' and self.current_position is None:
                self._open_position(current_date, current_price, 'short')
        #close any open position at the end
        if self.current_position is not None:
            self._close_position(self.data.index[-1], self.data['Close'].iloc[-1])
        #returning the equity curve as a dataframe
        return pd.DataFrame({'Equity Curve': self.equity_curve})

    #function to open a new position
    def _open_position(self, date: datetime, price: float, position_type: str):
        #open a new position (long or short)
        position_size = (self.current_capital * self.position_size) / price
        #commission amount
        commission_amount = position_size * price * self.commission
        #creating a new trade
        self.current_position = Trade(
            entry_date=date,
            entry_price=price,
            position_size=position_size,
            position_type=position_type
        )
        #subtracting the commission from the current capital
        self.current_capital -= commission_amount

    #function to close a position
    def _close_position(self, date: datetime, price: float):
        #close the current position and log the trade
        if self.current_position is None:
            return
        #commission amount
        commission_amount = self.current_position.position_size * price * self.commission
        #calculating the pnl
        if self.current_position.position_type == 'long':
            pnl = (price - self.current_position.entry_price) * self.current_position.position_size
        else:
            pnl = (self.current_position.entry_price - price) * self.current_position.position_size
        #calculating the pnl percentage
        pnl_pct = (pnl / (self.current_position.entry_price * self.current_position.position_size)) * 100
        #updating the current position
        self.current_position.exit_date = date
        self.current_position.exit_price = price
        self.current_position.status = 'closed'
        self.current_position.pnl = pnl
        self.current_position.pnl_pct = pnl_pct
        #updating the current capital
        self.current_capital += pnl - commission_amount
        #adding the trade to the list of trades
        self.trades.append(self.current_position)
        #resetting the current position
        self.current_position = None

    #function to get the trade log
    def get_trade_log(self) -> pd.DataFrame:
        #error handling if no trades are found
        if not self.trades:
            return pd.DataFrame()
        #list to store the trade data
        trade_data = []
        #loop through the trades
        for trade in self.trades:
            #adding the trade data to the list
            trade_data.append({
                'Entry Date': trade.entry_date,
                'Entry Price': trade.entry_price,
                'Position Size': trade.position_size,
                'Exit Date': trade.exit_date,
                'Exit Price': trade.exit_price,
                'Position Type': trade.position_type,
                'PnL': trade.pnl,
                'PnL %': trade.pnl_pct,
                'Status': trade.status,
                'Trade Duration': (trade.exit_date - trade.entry_date).days if trade.exit_date and trade.entry_date else None
            })
        return pd.DataFrame(trade_data)

    #function to get the performance metrics
    def get_performance_metrics(self) -> Dict[str, float]:
        #error handling if no trades are found
        if not self.trades:
            return {}
        #total number of trades
        total_trades = len(self.trades)
        #number of winning trades
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        #number of losing trades
        losing_trades = len([t for t in self.trades if t.pnl < 0])
        #win rate
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        #average win
        avg_win = np.mean([t.pnl for t in self.trades if t.pnl > 0]) if winning_trades > 0 else 0
        #average loss
        avg_loss = np.mean([t.pnl for t in self.trades if t.pnl < 0]) if losing_trades > 0 else 0
        #profit factor
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        #returning the performance metrics as a dictionary
        return {
            'Total Trades': total_trades,
            'Win Rate': win_rate * 100,
            'Average Win': avg_win,
            'Average Loss': avg_loss,
            'Profit Factor': profit_factor,
            'Total Return': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
        }