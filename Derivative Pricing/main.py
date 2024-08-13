import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    """
    Main entry point for the Advanced Derivatives Pricing application.

    This script initializes the PyQt5 application, creates the main window,
    and starts the event loop.
    """
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop and exit when it's done
    sys.exit(app.exec_())