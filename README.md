# Trading Strategy Simulator

A professional-grade, modular trading strategy backtesting platform built with Python and Streamlit. Features advanced performance analytics, real-time visualization, and a clean, extensible architecture designed for quantitative analysis and strategy development.

## 🚀 Features

### Core Functionality
- **Modular Strategy Framework**: Plug-and-play strategy system (SMA Crossover, RSI, MACD, Bollinger Bands)
- **Advanced Performance Metrics**: Comprehensive risk-adjusted returns analysis including Sharpe, Sortino, Calmar ratios
- **Real-time Visualization**: Interactive charts with trade markers and equity curve analysis
- **Professional UI/UX**: Clean Streamlit interface with tooltips, error handling, and responsive design

### Technical Capabilities
- **Position Management**: Sophisticated order execution with commission modeling
- **Trade Logging**: Detailed trade history with duration tracking and CSV export
- **Data Integration**: Yahoo Finance API integration with robust error handling
- **Extensible Architecture**: Easy addition of new strategies and metrics

## 🏗️ Architecture

```
app/
├── main.py              # Streamlit UI and application orchestration
├── data/
│   └── market_data.py   # Data fetching and validation
├── core/
│   └── backtester.py    # Backtesting engine with position management
├── strategies/
│   └── strategy_factory.py  # Strategy implementations and factory pattern
└── metrics/
    └── performance.py   # Performance calculation utilities
```

### Design Patterns
- **Factory Pattern**: Strategy instantiation and management
- **Abstract Base Classes**: Consistent strategy interface
- **Data Classes**: Clean trade and position representation
- **Modular Design**: Separation of concerns for maintainability

## 📊 Performance Metrics

- **Total Return**: Absolute performance measurement
- **Sharpe Ratio**: Risk-adjusted returns (annualized)
- **Sortino Ratio**: Downside risk-adjusted returns
- **Calmar Ratio**: CAGR to maximum drawdown ratio
- **Maximum Drawdown**: Largest peak-to-trough decline
- **CAGR**: Compound Annual Growth Rate
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit to gross loss ratio

## 🎯 Implemented Strategies

### SMA Crossover
- **Logic**: Buy when short MA crosses above long MA, sell on reverse
- **Parameters**: Configurable short/long window periods
- **Use Case**: Trend following in trending markets

### RSI Strategy
- **Logic**: Buy on oversold conditions, sell on overbought
- **Parameters**: RSI period, overbought/oversold thresholds
- **Use Case**: Mean reversion in range-bound markets

### MACD Strategy
- **Logic**: Buy on MACD/signal line crossover
- **Parameters**: Fast/slow EMA periods, signal line period
- **Use Case**: Momentum and trend confirmation

### Bollinger Bands
- **Logic**: Buy below lower band, sell above upper band
- **Parameters**: Window period, standard deviation multiplier
- **Use Case**: Volatility-based mean reversion

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/AaronM1812/trading-simulator.git
cd trading-simulator

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app/main.py
```

## 📈 Usage

1. **Select Parameters**: Choose ticker, date range, and strategy
2. **Configure Strategy**: Adjust strategy-specific parameters
3. **Run Simulation**: Execute backtest with real-time results
4. **Analyze Results**: Review performance metrics and trade log
5. **Export Data**: Download trade log for further analysis

## 🧪 Testing

```bash
# Run the test suite
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

## 🔧 Technical Stack

- **Backend**: Python 3.8+
- **Web Framework**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly
- **Data Source**: Yahoo Finance API
- **Testing**: pytest

## 🚧 Future Enhancements

### Phase 2 Roadmap
- **Portfolio Management**: Multi-asset support and correlation analysis
- **Advanced Strategies**: Mean reversion, momentum, and statistical arbitrage
- **Risk Management**: Position sizing, stop-loss, and portfolio optimization
- **Performance Optimization**: C++ backend for high-frequency simulation
- **Real-time Data**: Live market data integration
- **Machine Learning**: ML-based signal generation and optimization

### Advanced Features
- **Parameter Optimization**: Genetic algorithms and grid search
- **Walk-Forward Analysis**: Out-of-sample testing framework
- **Monte Carlo Simulation**: Risk analysis and scenario modeling
- **API Integration**: Real-time trading platform connectivity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the MIT License.

---

**Built by Aaron Malhi**

*For questions, feedback, or collaboration opportunities, feel free to reach out!*
