from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QDoubleValidator

class ParameterInput(QWidget):
    """
    A widget for inputting parameters for derivative pricing.

    This widget provides a form layout with input fields for various
    parameters used in derivative pricing calculations, including
    stock price, strike price, volatility, and other relevant factors.
    """

    def __init__(self):
        """Initialize the ParameterInput widget with all necessary input fields."""
        super().__init__()
        layout = QFormLayout()

        # Create input fields
        self.S = QLineEdit()
        self.K = QLineEdit()
        self.T = QLineEdit()
        self.r = QLineEdit()
        self.sigma = QLineEdit()
        self.barrier = QLineEdit()
        self.storage_cost = QLineEdit()
        self.convenience_yield = QLineEdit()
        self.financing_rate = QLineEdit()
        self.holding_period = QLineEdit()
        
        # Set validators for numeric input to ensure valid data entry
        for widget in [self.S, self.K, self.T, self.r, self.sigma, self.barrier, 
                       self.storage_cost, self.convenience_yield, self.financing_rate, self.holding_period]:
            widget.setValidator(QDoubleValidator())

        # Add input fields to the layout with descriptive labels
        layout.addRow("Spot Price (S):", self.S)
        layout.addRow("Strike Price (K):", self.K)
        layout.addRow("Time to Maturity (T):", self.T)
        layout.addRow("Risk-free Rate (r):", self.r)
        layout.addRow("Volatility (σ):", self.sigma)
        layout.addRow("Barrier:", self.barrier)
        layout.addRow("Storage Cost:", self.storage_cost)
        layout.addRow("Convenience Yield:", self.convenience_yield)
        layout.addRow("Financing Rate:", self.financing_rate)
        layout.addRow("Holding Period (days):", self.holding_period)

        # Create and add dropdown menus for categorical inputs
        self.option_type = QComboBox()
        self.option_type.addItems(['call', 'put'])
        layout.addRow("Option Type:", self.option_type)

        self.barrier_type = QComboBox()
        self.barrier_type.addItems(['up-and-in', 'up-and-out', 'down-and-in', 'down-and-out'])
        layout.addRow("Barrier Type:", self.barrier_type)

        self.cfd_position = QComboBox()
        self.cfd_position.addItems(['long', 'short'])
        layout.addRow("CFD Position:", self.cfd_position)

        # Add calculate button to trigger pricing calculations
        self.calculate_button = QPushButton("Calculate")
        layout.addRow(self.calculate_button)

        self.setLayout(layout)