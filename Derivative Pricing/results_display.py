from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt

class ResultsDisplay(QWidget):
    """
    A widget for displaying the results of derivative pricing calculations.

    This widget shows the barrier option price, Greeks, futures price, and CFD price.
    It provides methods to update the display with new results and clear previous results.
    """

    def __init__(self):
        """Initialize the ResultsDisplay widget with labels for each result type."""
        super().__init__()
        self.layout = QVBoxLayout()
        
        # Label for displaying the barrier option price
        self.price_label = QLabel()
        self.layout.addWidget(self.price_label)

        # Grid layout for displaying the Greeks
        self.greeks_layout = QGridLayout()
        self.layout.addLayout(self.greeks_layout)

        # Labels for futures and CFD prices
        self.futures_price_label = QLabel()
        self.layout.addWidget(self.futures_price_label)

        self.cfd_price_label = QLabel()
        self.layout.addWidget(self.cfd_price_label)

        self.setLayout(self.layout)

    def clear_results(self):
        """
        Clear all previous results from the display.

        This method removes all text from the price labels and
        clears the grid layout used for displaying Greeks.
        """
        # Clear text from all labels
        self.price_label.clear()
        self.futures_price_label.clear()
        self.cfd_price_label.clear()
        
        # Remove all items from the greeks_layout
        while self.greeks_layout.count():
            item = self.greeks_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_results(self, price: float, greeks: dict, futures_price: float, cfd_price: float):
        """
        Update the display with new calculation results.

        This method clears previous results and then populates the display
        with the newly calculated values for the barrier option price,
        Greeks, futures price, and CFD price.

        Args:
            price (float): The calculated barrier option price.
            greeks (dict): A dictionary containing the calculated Greeks.
            futures_price (float): The calculated futures price.
            cfd_price (float): The calculated CFD price.
        """
        # Clear previous results before updating
        self.clear_results()
        
        # Update barrier option price
        self.price_label.setText(f"Barrier Option Price: {price:.4f}")
        
        # Display Greeks in a grid layout
        for i, (greek, value) in enumerate(greeks.items()):
            # Add Greek name (right-aligned) and its value
            self.greeks_layout.addWidget(QLabel(f"{greek}:", alignment=Qt.AlignRight), i, 0)
            self.greeks_layout.addWidget(QLabel(f"{value:.6f}"), i, 1)

        # Update futures and CFD prices
        self.futures_price_label.setText(f"Futures Price: {futures_price:.4f}")
        self.cfd_price_label.setText(f"CFD Price: {cfd_price:.4f}")