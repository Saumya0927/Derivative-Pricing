from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer
from advanced_derivatives_pricing import AdvancedDerivativesPricing
from parameter_input import ParameterInput
from results_display import ResultsDisplay
from plot_widget import PlotWidget
import traceback

class MainWindow(QMainWindow):
    """
    The main window of the Advanced Derivatives Pricing application.

    This class sets up the main UI layout, including the parameter input widget,
    results display, and plotting area. It also handles the calculation logic
    and error handling.
    """

    def __init__(self):
        """Initialize the main window and set up the UI components."""
        super().__init__()
        self.setWindowTitle("Advanced Derivatives Pricing")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Set up the left side of the UI with parameter input and results display
        left_layout = QVBoxLayout()
        self.parameter_input = ParameterInput()
        self.results_display = ResultsDisplay()
        left_layout.addWidget(self.parameter_input)
        left_layout.addWidget(self.results_display)

        # Set up the right side of the UI with the plotting widget
        self.plot_widget = PlotWidget()

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.plot_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect the calculate button to the calculation method
        self.parameter_input.calculate_button.clicked.connect(self.calculate_and_update)

    def calculate_and_update(self):
        """
        Perform calculations based on user input and update the display.

        This method retrieves input values, performs pricing calculations,
        and updates the results display and plot. It also handles input
        validation and error display.
        """
        try:
            # Helper function to safely convert input to float
            def safe_float(value, name):
                if not value:
                    raise ValueError(f"{name} cannot be empty")
                return float(value)

            # Retrieve and validate all input values
            S = safe_float(self.parameter_input.S.text(), "Spot Price")
            K = safe_float(self.parameter_input.K.text(), "Strike Price")
            T = safe_float(self.parameter_input.T.text(), "Time to Maturity")
            r = safe_float(self.parameter_input.r.text(), "Risk-free Rate")
            sigma = safe_float(self.parameter_input.sigma.text(), "Volatility")
            barrier = safe_float(self.parameter_input.barrier.text(), "Barrier")
            storage_cost = safe_float(self.parameter_input.storage_cost.text(), "Storage Cost")
            convenience_yield = safe_float(self.parameter_input.convenience_yield.text(), "Convenience Yield")
            financing_rate = safe_float(self.parameter_input.financing_rate.text(), "Financing Rate")
            holding_period = safe_float(self.parameter_input.holding_period.text(), "Holding Period")
            
            option_type = self.parameter_input.option_type.currentText()
            barrier_type = self.parameter_input.barrier_type.currentText()
            cfd_position = self.parameter_input.cfd_position.currentText()

            # Perform pricing calculations
            pricer = AdvancedDerivativesPricing(S, K, T, r, sigma)
            price = pricer.price_barrier_option(option_type, barrier_type, barrier)
            greeks = pricer.calculate_greeks(option_type, barrier_type, barrier)
            futures_price = pricer.price_futures(storage_cost, convenience_yield)
            cfd_price = pricer.price_cfd(cfd_position, financing_rate, holding_period)

            # Update results display
            self.results_display.update_results(price, greeks, futures_price, cfd_price)
            
            # Use QTimer to delay the plot update slightly, allowing the GUI to refresh
            QTimer.singleShot(100, lambda: self.plot_widget.plot_payoff(pricer, option_type, barrier_type, barrier))

        except ValueError as ve:
            # Handle input validation errors
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            # Handle unexpected errors
            error_message = f"An error occurred:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            QMessageBox.critical(self, "Error", error_message)
            print(error_message)  # Print to console for debugging