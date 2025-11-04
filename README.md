# Options strategy visualizer

An interactive web tool to explore, analyze, and visualize European option strategies (calls & puts) using PnL graphs.

Whether you're a trader, finance student, or hobbyist, this application helps you understand the profit/loss (PnL) potential and risk exposure of various option strategies at maturity. All calculations are powered by the Black-Scholes model, ensuring theoretical accuracy.

## Key Features
- Interactive PnL Graphs: Visualize profit/loss as a function of the underlying asset price at maturity.
- Portfolio Greeks: Track Delta, Gamma, Vega, Theta, and Rho to understand risk sensitivities.
- Black-Scholes Calculations: Accurate pricing and Greeks for European calls and puts.
- Customizable Strategies: Adjust strike prices, volatility, interest rates, and time to maturity.
- User-Friendly Interface: Intuitive design for quick strategy testing and analysis.

## Example Strategies
- Straddle: Buy a call and put at the same strike price.
- Strangle: Buy a call and put at different strike prices.
- Butterfly Spread: Combine calls/puts to create a limited-risk, limited-reward strategy.

## Testing
- **Framework**: pytest
- **Location**: Tests/
- **Run tests**:
  - pytest -v
  - pytest Tests/test_module.py

## Getting started

#### Prerequisites

- Python 3.8+ installed on your system.
- Pip (Python package manager) for dependency installation.

#### Installation steps
- Clone the repository (or download the project files): **git clone https://github.com/bellije/OptionStrategyVisualizer.git**
- Navigate to the project directory: **cd OptionStrategyVisualizer**
- Install dependencies: **pip install -r requirements.txt**
- Launch the application: **python ./main.py**
- Open the app: The application will automatically open in your default browser at http://127.0.0.1:8050/.
