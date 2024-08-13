import numpy as np
from scipy.stats import norm
from typing import Literal, Dict

class AdvancedDerivativesPricing:
    """
    A class for pricing various derivative instruments including barrier options, futures, and CFDs.

    This class implements advanced pricing models for financial derivatives, with a focus on
    barrier options. It also provides methods for calculating option Greeks, futures prices,
    and CFD (Contract for Difference) prices.
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        """
        Initialize the AdvancedDerivativesPricing object with market parameters.

        Args:
            S (float): Current price of the underlying asset.
            K (float): Strike price of the option.
            T (float): Time to maturity in years.
            r (float): Risk-free interest rate (annualized).
            sigma (float): Volatility of the underlying asset (annualized).
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _d1(self, S: float, K: float, T: float, r: float, sigma: float) -> float:
        """
        Calculate the d1 parameter used in the Black-Scholes formula.

        Args:
            S (float): Current price of the underlying asset.
            K (float): Strike price of the option.
            T (float): Time to maturity in years.
            r (float): Risk-free interest rate (annualized).
            sigma (float): Volatility of the underlying asset (annualized).

        Returns:
            float: The calculated d1 value.
        """
        return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    def _d2(self, d1: float, sigma: float, T: float) -> float:
        """
        Calculate the d2 parameter used in the Black-Scholes formula.

        Args:
            d1 (float): The d1 parameter.
            sigma (float): Volatility of the underlying asset (annualized).
            T (float): Time to maturity in years.

        Returns:
            float: The calculated d2 value.
        """
        return d1 - sigma * np.sqrt(T)

    def price_barrier_option(self, option_type: Literal['call', 'put'], 
                             barrier_type: Literal['up-and-in', 'up-and-out', 'down-and-in', 'down-and-out'], 
                             barrier: float) -> float:
        """
        Price a barrier option using the analytical formula.

        This method implements the pricing model for various types of barrier options,
        including up-and-in, up-and-out, down-and-in, and down-and-out for both call and put options.

        Args:
            option_type (Literal['call', 'put']): The type of option.
            barrier_type (Literal['up-and-in', 'up-and-out', 'down-and-in', 'down-and-out']): The type of barrier.
            barrier (float): The barrier price level.

        Returns:
            float: The calculated price of the barrier option.

        Raises:
            ValueError: If any of the required parameters are None or if an invalid option type is provided.
        """
        if None in (self.S, self.K, self.T, self.r, self.sigma, barrier):
            raise ValueError("All parameters must be non-None")
        
        # Calculate Black-Scholes parameters
        d1 = self._d1(self.S, self.K, self.T, self.r, self.sigma)
        d2 = self._d2(d1, self.sigma, self.T)
        
        # Calculate additional parameters for barrier options
        lambda_ = (self.r - 0.5 * self.sigma**2) / self.sigma**2
        y = np.log(barrier**2 / (self.S * self.K)) / (self.sigma * np.sqrt(self.T)) + lambda_ * self.sigma * np.sqrt(self.T)
        x1 = np.log(self.S / barrier) / (self.sigma * np.sqrt(self.T)) + lambda_ * self.sigma * np.sqrt(self.T)
        y1 = np.log(barrier / self.S) / (self.sigma * np.sqrt(self.T)) + lambda_ * self.sigma * np.sqrt(self.T)

        # Price calculation based on option type and barrier type
        if option_type == 'call':
            if barrier_type == 'down-and-out':
                if self.S <= barrier:
                    return 0
                return (self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2) - 
                        self.S * (barrier / self.S)**(2 * lambda_) * (norm.cdf(-x1) - norm.cdf(-y)))
            elif barrier_type == 'up-and-out':
                if self.S >= barrier:
                    return 0
                return (self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2) - 
                        self.S * (barrier / self.S)**(2 * lambda_) * (norm.cdf(y) - norm.cdf(x1)))
            elif barrier_type == 'down-and-in':
                if self.S <= barrier:
                    return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
                return self.S * (barrier / self.S)**(2 * lambda_) * norm.cdf(-x1)
            elif barrier_type == 'up-and-in':
                if self.S >= barrier:
                    return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
                return self.S * (barrier / self.S)**(2 * lambda_) * norm.cdf(y)
        elif option_type == 'put':
            if barrier_type == 'down-and-out':
                if self.S <= barrier:
                    return 0
                return (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1) + 
                        self.S * (barrier / self.S)**(2 * lambda_) * (norm.cdf(-y) - norm.cdf(-x1)))
            elif barrier_type == 'up-and-out':
                if self.S >= barrier:
                    return 0
                return (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1) + 
                        self.S * (barrier / self.S)**(2 * lambda_) * (norm.cdf(x1) - norm.cdf(y)))
            elif barrier_type == 'down-and-in':
                if self.S <= barrier:
                    return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
                return self.S * (barrier / self.S)**(2 * lambda_) * norm.cdf(-y)
            elif barrier_type == 'up-and-in':
                if self.S >= barrier:
                    return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
                return self.S * (barrier / self.S)**(2 * lambda_) * norm.cdf(x1)
        else:
            raise ValueError(f"Invalid option type: {option_type}")

    def calculate_greeks(self, option_type: Literal['call', 'put'], 
                         barrier_type: Literal['up-and-in', 'up-and-out', 'down-and-in', 'down-and-out'], 
                         barrier: float) -> Dict[str, float]:
        """
        Calculate the Greeks (Delta, Gamma, Vega, Theta, Rho) for a barrier option.

        This method uses finite difference approximations to estimate the option Greeks.

        Args:
            option_type (Literal['call', 'put']): The type of option.
            barrier_type (Literal['up-and-in', 'up-and-out', 'down-and-in', 'down-and-out']): The type of barrier.
            barrier (float): The barrier price level.

        Returns:
            Dict[str, float]: A dictionary containing the calculated Greeks (Delta, Gamma, Vega, Theta, Rho).

        Raises:
            ValueError: If any of the required parameters are None.
        """
        if None in (self.S, self.K, self.T, self.r, self.sigma, barrier):
            raise ValueError("All parameters must be non-None")
        
        eps = 1e-5
        price = self.price_barrier_option(option_type, barrier_type, barrier)
        
        # Calculate Delta
        S_up = self.S + eps
        price_up = AdvancedDerivativesPricing(S_up, self.K, self.T, self.r, self.sigma).price_barrier_option(option_type, barrier_type, barrier)
        delta = (price_up - price) / eps

        # Calculate Gamma
        S_down = self.S - eps
        price_down = AdvancedDerivativesPricing(S_down, self.K, self.T, self.r, self.sigma).price_barrier_option(option_type, barrier_type, barrier)
        gamma = (price_up - 2*price + price_down) / (eps**2)

        # Calculate Vega
        sigma_up = self.sigma + eps
        price_sigma_up = AdvancedDerivativesPricing(self.S, self.K, self.T, self.r, sigma_up).price_barrier_option(option_type, barrier_type, barrier)
        vega = (price_sigma_up - price) / eps

        # Calculate Theta
        T_down = max(self.T - eps/365, eps)  # Ensure T doesn't become negative
        price_T_down = AdvancedDerivativesPricing(self.S, self.K, T_down, self.r, self.sigma).price_barrier_option(option_type, barrier_type, barrier)
        theta = (price_T_down - price) / (eps/365)

        # Calculate Rho
        r_up = self.r + eps
        price_r_up = AdvancedDerivativesPricing(self.S, self.K, self.T, r_up, self.sigma).price_barrier_option(option_type, barrier_type, barrier)
        rho = (price_r_up - price) / eps

        return {
            'Delta': delta,
            'Gamma': gamma,
            'Vega': vega,
            'Theta': theta,
            'Rho': rho
        }

    def price_futures(self, storage_cost: float = 0, convenience_yield: float = 0) -> float:
        """
        Calculate the theoretical price of a futures contract.

        This method uses the cost-of-carry model to price futures contracts.

        Args:
            storage_cost (float, optional): Annual storage cost as a fraction of the spot price. Defaults to 0.
            convenience_yield (float, optional): Annual convenience yield as a fraction of the spot price. Defaults to 0.

        Returns:
            float: The calculated futures price.

        Raises:
            ValueError: If any of the required parameters are None.
        """
        if None in (self.S, self.T, self.r):
            raise ValueError("S, T, and r must be non-None")
        net_cost = storage_cost - convenience_yield
        futures_price = self.S * np.exp((self.r + net_cost) * self.T)
        return futures_price

    def price_cfd(self, position: Literal['long', 'short'], financing_rate: float, holding_period: float) -> float:
        """
        Calculate the price (cost or profit) of a Contract for Difference (CFD).

        This method calculates the theoretical price of a CFD based on the position,
        financing rate, and holding period.

        Args:
            position (Literal['long', 'short']): The position taken in the CFD.
            financing_rate (float): Daily financing rate as a fraction of the spot price.
            holding_period (float): Number of days the CFD is held.

        Returns:
            float: The calculated CFD price (positive for profit, negative for loss).

        Raises:
            ValueError: If any of the required parameters are None or if an invalid position is provided.
        """
        if None in (self.S, self.r):
            raise ValueError("S and r must be non-None")
        daily_price_change = self.S * (np.exp(self.r * (holding_period / 365)) - 1)
        financing_cost = self.S * financing_rate * holding_period / 365

        if position == 'long':
            return daily_price_change - financing_cost
        elif position == 'short':
            return -daily_price_change - financing_cost
        else:
            raise ValueError("Invalid position type")