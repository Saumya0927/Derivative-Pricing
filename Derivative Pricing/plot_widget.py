from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class PlotWidget(QWidget):
    """
    A widget for plotting option payoffs.

    This widget embeds a matplotlib figure in a PyQt widget, allowing
    for dynamic plotting of option payoffs within the GUI.
    """

    def __init__(self):
        """Initialize the PlotWidget with a matplotlib figure and canvas."""
        super().__init__()
        layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_payoff(self, pricer, option_type, barrier_type, barrier):
        """
        Plot the payoff of a barrier option.

        This method calculates and plots the option prices for a range of
        underlying asset prices, showing the payoff structure of the option.

        Args:
            pricer (AdvancedDerivativesPricing): The pricing object.
            option_type (str): The type of option ('call' or 'put').
            barrier_type (str): The type of barrier option.
            barrier (float): The barrier price.
        """
        self.ax.clear()
        # Generate a range of stock prices centered around the strike price
        stock_prices = np.linspace(pricer.K * 0.5, pricer.K * 1.5, 100)
        option_prices = []
        
        # Calculate option prices for each stock price
        for S in stock_prices:
            pricer.S = S
            option_prices.append(pricer.price_barrier_option(option_type, barrier_type, barrier))
        
        # Plot the option prices
        self.ax.plot(stock_prices, option_prices, label='Option Price')
        self.ax.axvline(x=pricer.K, color='r', linestyle='--', label='Strike Price')
        self.ax.axvline(x=barrier, color='g', linestyle='--', label='Barrier')
        self.ax.set_xlabel('Stock Price')
        self.ax.set_ylabel('Option Price')
        self.ax.set_title(f'{option_type.capitalize()} {barrier_type} Barrier Option Payoff')
        self.ax.legend()
        self.ax.grid(True)
        
        # Redraw the canvas
        self.canvas.draw()