# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import norm
from scipy.optimize import minimize

import quantstats as qs
import yfinance as yf


# -

class AssetAllocationBacktesting:
    """
    A class for backtesting asset allocation model and present portfolio performance.
    
    :param price_df: Historical price dataframe.
    :param period: Period for annualization.
    """
    
    def __init__(self, price_df, period=252):
        
        self.period = period
        
        # Returns data
        self.rets = price_df.pct_change().dropna()
        
        # Expected returns
        self.er = np.array(self.rets * self.period)
        
        # Volatility
        self.vol = np.array(self.rets.rolling(self.period).std() * np.sqrt(self.period))
        
        # Covarience Matrix
        cov = self.rets.rolling(self.period).cov() * self.period
        self.cov = cov.values.reshape(int(cov.shape[0]/cov.shape[1]), cov.shape[1], cov.shape[1])
        
        # Transaction Cost
        self.cost = 0.0005
        
        
    class CrossSectional:
        """
        A class of horizontal distribution models that distributes weights among assets.
        """
        
        def ew(self, er):
            """
            All assets are equally weights.
            
            :param er: Each asset's expected returns.
            :return: weights vector
            """
            noa = er.shape[0]  # number of asset
            weights = np.ones_like(er) * (1/noa)
            
            return weights
        
        def msr(self, er, cov):
            """
            Find the weights that maximizes the Sharpe ratio of the portfolio.
            
            :param er: Each asset's expected returns.
            :param cov: Covariance matrix between assets.
            :return: weights vector
            """
            noa = er.shape[0]
            init_guess = np.repeat(1/noa, noa)          
            bounds=((0.0, 1.0), ) * noa
            weights_sum_to_1 = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            
            def neg_sharpe(weights, er, cov):
                r = weights.T @ er
                vol = np.sqrt(weights.T @ cov @ weights)
                return - r / vol
            
            weights = minimize(neg_sharpe,
                              init_guess,
                              args=(er, cov),
                              method='SLSQP',
                              constraints=(weights_sum_to_1,),
                              bounds=bounds)
            
            return weights.x
        
        def gmv(self, cov):
            """
            Find the weights that minimizes the volatility of the portfolio.
            
            :param cov: Covariance matrix between assets.
            :return: weights vector
            """
            noa = cov.shape[0]
            init_guess = np.repeat(1/noa, noa)          
            bounds=((0.0, 1.0), ) * noa
            weights_sum_to_1 = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            
            def port_vol(weights, cov):
                vol = np.sqrt(weights.T @ cov @ weights)
                return vol
            
            weights = minimize(port_vol,
                              init_guess,
                              args=(cov),
                              method='SLSQP',
                              constraints=(weights_sum_to_1,),
                              bounds=bounds)
            
            return weights.x
        
        def mdp(self, vol, cov):
            """
            Find the weights that maximizes the diversification ratio of the portfolio.
            
            :param vol: Each asset's volatility.
            :param cov: Covariance matrix between assets.
            :return: weights vector
            """
            noa = vol.shape[0]
            init_guess = np.repeat(1/noa, noa)          
            bounds=((0.0, 1.0), ) * noa
            weights_sum_to_1 = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            
            def neg_div_ratio(weights, vol, cov):
                weighted_vol = weights.T @ vol
                port_vol = np.sqrt(weights.T @ cov @ weights)
                return - weighted_vol / port_vol
            
            weights = minimize(neg_div_ratio,
                              init_guess,
                              args=(vol, cov),
                              method='SLSQP',
                              constraints=(weights_sum_to_1,),
                              bounds=bounds)
            
            return weights.x
        
        def rp(self, cov):
            """
            Find the weights that equalizes the risk contribution of each asset.
            
            :param cov: Covariance matrix between assets.
            :return: weights vector
            """
            noa = cov.shape[0]
            init_guess = np.repeat(1/noa, noa)
            target_risk = np.repeat(1/noa, noa)
            bounds=((0.0, 1.0), ) * noa
            weights_sum_to_1 = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            
            def min_risk_contribs(weights, target_risk, cov):
                port_var = weights.T @ cov @ weights
                marginal_contribs = cov @ weights
                risk_contribs = np.multiply(marginal_contribs, weights.T) / port_var
                w_contribs = ((risk_contribs - target_risk) ** 2).sum()
                return w_contribs
            
            weights = minimize(min_risk_contribs,
                              init_guess,
                              args=(target_risk, cov),
                              method='SLSQP',
                              constraints=(weights_sum_to_1,),
                              bounds=bounds)
            
            return weights.x
        
        def emv(self, vol):
            """
            Assuming that the correlation coefficient between assets is 0, 
            calculate the weights that equalizes the risk contribution of each asset.
            
            :param vol: Each asset's volatility.
            :return: weights vector
            """
            inv_vol = 1 / vol
            weights = inv_vol / inv_vol.sum()
            
            return weights
        
        
    class PortRiskFreeWeights:
        """
        Dynamically balances between portfolio and risk-free assets to manage overall portfolio risk.
        """
        
        def vt(self, port_rets, period, vol_target=0.1):
            """
            Calculates the weight of a portfolio inversely proportional to the current volatility of the portfolio.
            
            :param port_rets: Returns of the portfolio.
            :param period: Period for annualization.
            :param vol_target: Target volatility of the portfolio.
            :return: Portfolio weights
            """
            vol = port_rets.rolling(period).std() * np.sqrt(period)
            weights = (vol_target / vol).replace([np.inf, -np.inf], 0).shift().fillna(0)
            weights[weights > 1] = 1
            
            return weigths
        
        def cvt(self, port_rets, period, delta=0.01, cvar_target=0.05):
            """
            Calculates the weight of a portfolio inversely proportional to the current CVaR of the portfolio.
            
            :param port_rets: Returns of the portfolio.
            :param period: Period for annualization.
            :param delta: Probability of loss in the portfolio return distribution.
            :param cvar_target: Target CVaR of the portfolio.
            :return: Portfolio weights
            """
            def calculate_CVaR(rets, delta=0.01):
                VaR = rets.quatile(delta)
                return rets[rets <= VaR].mean()
            
            rolling_CVaR = - port_rets.rolling(period).apply(calculate_CVaR, args=(delta)).fillna(0)
            weights = (cvar_target / rolling_CVaR).replace([np.inf, -np.inf], 0).shift().fillna(0)
            weights[weights > 1] = 1
            
            return weights


