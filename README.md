# Advanced Derivatives Pricing Application

## Overview

This Advanced Derivatives Pricing Application is a powerful, user-friendly tool designed for financial analysts, traders, and students to price and analyze various derivative instruments. Built with Python and PyQt5, it offers a graphical interface for pricing barrier options, calculating Greeks, and estimating prices for futures and CFDs (Contracts for Difference).


## Features

- **Barrier Option Pricing**: Supports various types including up-and-in, up-and-out, down-and-in, and down-and-out for both call and put options.
- **Greeks Calculation**: Computes Delta, Gamma, Vega, Theta, and Rho for barrier options.
- **Futures Pricing**: Estimates futures prices considering storage costs and convenience yields.
- **CFD Pricing**: Calculates CFD prices for both long and short positions.
- **Interactive Plotting**: Visualizes option payoffs dynamically.
- **User-Friendly Interface**: Easy-to-use GUI for inputting parameters and displaying results.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/advanced-derivatives-pricing.git
   ```

2. Navigate to the project directory:
   ```
   cd advanced-derivatives-pricing
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application by executing:

```
python main.py
```

1. Enter the required parameters in the input fields.
2. Select the option type, barrier type, and CFD position from the dropdown menus.
3. Click the "Calculate" button to compute prices and Greeks.
4. View the results in the display area and the plotted payoff graph.

## Project Structure

```
Derivative-Pricing/
│
├── main.py
├── main_window.py
├── advanced_derivatives_pricing.py
├── parameter_input.py
├── results_display.py
├── plot_widget.py
├── requirements.txt
└── README.md
```

- `main.py`: Entry point of the application.
- `main_window.py`: Defines the main application window.
- `advanced_derivatives_pricing.py`: Core pricing logic for derivatives.
- `parameter_input.py`: Widget for user input of pricing parameters.
- `results_display.py`: Widget for displaying calculation results.
- `plot_widget.py`: Widget for plotting option payoffs.

## Dependencies

- Python 3.7+
- PyQt5
- NumPy
- SciPy
- Matplotlib
