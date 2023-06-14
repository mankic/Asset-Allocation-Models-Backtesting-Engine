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
        
    def transaction_cost(self, weights_df, rets_df, cost=0.0005):
        """
        Transaction costs are calculated using the compound rate of return method, assuming reinvestment.
        
        :param weights_df: Weights dataframe of portfolio.
        :param rets_df: Returns dataframe of portfolio.
        :param cost: Transaction cost per unit.
        :return: Transaction cost dataframe.
        """
        prev_weights_df = (weights_df.shift().fillna(0) * (1 + rets_df.iloc[self.period - 1:, :])) \
        .div((weights_df.shift().fillna(0) * (1 + rets_df.iloc[self.period - 1:, :])).sum(axis=1), axis=0)
        
        cost_df = abs(weights_df - prev_weights_df) * cost
        cost_df.fillna(0, inplace=True)
        
        return cost_df
    
    def run(self, cs_model, ts_model, cost):
        """
        Execute portfolio backtesting.
        :param cs_model: Choose the asset allocation model you want.
        :param ts_model: Choose the portfolio weights model you want.
        :param cost: Transaction cost you have to pay.
        :return: [port_weights, port_asset_rets, port_rets]
        """
        backtest_dict = {}
        rets = self.rets
        
        # Execute the selected asset allocation model.
        for i, index in enumerate(rets.index[self.period - 1:]):
            if cs_model == 'EW':
                backtest_dict[index] = self.CrossSectional().ew(self.er[i])
            elif cs_model == 'MSR':
                backtest_dict[index] = self.CrossSectional().msr(self.er[i], self.cov[i])
            elif cs_model == 'GMV':
                backtest_dict[index] = self.CrossSectional().gmv(self.cov[i])
            elif cs_model == 'MDP':
                backtest_dict[index] = self.CrossSectional().mdp(self.vol[i], self.cov[i])
            elif cs_model == 'RP':
                backtest_dict[index] = self.CrossSectional().rp(self.cov[i])
            elif cs_model == 'EMV':
                backtest_dict[index] = self.CrossSectional().emv(self.vol[i])
        
        cs_weights = pd.DataFrame(list(backtest_dict.values()), index=backtest_dict.keys(), columns=rets.columns)
        cs_weights.fillna(0, inplace=True)
        
        cs_rets = cs_weights.shift() * rets.iloc[self.period - 1:, :]
        cs_port_rets = cs_rets.sum(axis=1)
        
        # Execute the selected portfolio weight model.
        if ts_model == 'VT':
            ts_weights = (self.PortRiskFreeWeights().vt(cs_port_rets, self.period))
        elif ts_model == 'CVT':
            ts_weights = (self.PortRiskFreeWeights().cvt(cs_port_rets, self.period))
        elif ts_model == None:
            ts_weights = 1
        
        # Portfolio investment weights
        port_weights = cs_weight.multiply(ts_weights, axis=0)
        
        # Transaction cost
        cost = self.transaction_cost(port_weights, rets)
        
        # Portfolio Returns
        port_asset_rets = port_weights.shift() * rets - cost
        port_rets = port_asset_rets.sum(axis=1)
        port_rets.index = pd.to_datetime(port_rets.index).strftime("%Y-%m-%d")
        
        return port_weights, port_asset_rets, port_rets


