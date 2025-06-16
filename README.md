# Trading Bot Simulator

A professional-grade trading strategy backtesting and simulation platform built with Python. This project demonstrates both quantitative trading strategy implementation and software engineering best practices.

## 🚀 Features

- **Multiple Trading Strategies**
  - SMA Crossover
  - RSI Strategy
  - MACD Strategy
  - (More strategies can be easily added through the plugin system)

- **Comprehensive Backtesting**
  - Realistic trade execution
  - Commission handling
  - Position sizing
  - Long/Short support

- **Advanced Performance Metrics**
  - Total Return
  - Sharpe Ratio
  - Maximum Drawdown
  - CAGR
  - Calmar Ratio
  - Sortino Ratio
  - Win Rate
  - Profit Factor
  - Recovery Factor

- **Professional UI**
  - Interactive charts with Plotly
  - Trade log visualization
  - Performance metrics dashboard
  - CSV export functionality

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/trading-simulator.git
cd trading-simulator
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

1. Start the Streamlit app:
```bash
streamlit run app/main.py
```

2. In the web interface:
   - Select a stock ticker
   - Choose a date range
   - Select a trading strategy
   - Adjust strategy parameters
   - Click "Run Simulation"

3. View the results:
   - Price chart with trade signals
   - Equity curve
   - Performance metrics
   - Trade log

## 📊 Strategy Details

### SMA Crossover
- Uses two Simple Moving Averages
- Generates buy signal when short MA crosses above long MA
- Generates sell signal when short MA crosses below long MA

### RSI Strategy
- Uses Relative Strength Index
- Generates buy signal when RSI crosses below oversold threshold
- Generates sell signal when RSI crosses above overbought threshold

### MACD Strategy
- Uses Moving Average Convergence Divergence
- Generates buy signal when MACD line crosses above signal line
- Generates sell signal when MACD line crosses below signal line

## 🏗️ Project Structure

```
trading-simulator/
├── app/                      # Application source code
│   ├── main.py              # Streamlit app entry point
│   ├── strategies/          # Trading strategies
│   ├── core/               # Backtesting engine
│   ├── metrics/            # Performance metrics
│   ├── data/               # Market data handling
│   └── utils/              # Helper functions
├── tests/                   # Unit tests
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🛠️ Development

1. Code formatting:
```bash
black app/ tests/
```

2. Linting:
```bash
ruff check app/ tests/
```

3. Type checking:
```bash
mypy app/ tests/
```

## 📝 Adding New Strategies

1. Create a new strategy class in `app/strategies/`
2. Inherit from the `Strategy` base class
3. Implement the `generate_signals` method
4. Register the strategy in `STRATEGY_REGISTRY`

Example:
```python
from app.strategies.strategy_factory import Strategy

class MyStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame, **kwargs) -> list:
        # Implement your strategy logic here
        return signals
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Market data from [Yahoo Finance](https://finance.yahoo.com/)
- Charts powered by [Plotly](https://plotly.com/)
