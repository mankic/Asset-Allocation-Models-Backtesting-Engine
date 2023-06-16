# 📎 객체 지향적 자산 배분 모델 백테스트 엔진 구현
## About
포트폴리오 자산군의 과거 주가 데이터(주간)를 입력받아 주어진 자산 배분 모델 내에서 백테스트를 진행하고 성과를 볼 수 있도록 함.

<details>
  <summary><h2>Structure</h2></summary>
  <img width="50%" height="50%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/1e8d7adc-1013-426a-a5ec-9fc4aae2d111"></img>  
</details>  

<details>
  <summary><h2>Environment</h2></summary>  
  
  * Python 3.9.16
  * Numpy 1.24.3
  * Pandas 1.5.3
  * Matplotlib 3.7.1
  * Scipy 1.10.1
  * QuantStats 0.0.59
  * yfinance 0.2.18
</details>  

<details>
  <summary><h2>자산 배분 모형 목록</h2></summary>  
  
  <h3>자산간 가중치 할당 모델</h3>  
  
  * 동일 가중 (Equal Weighted)
    > $w_i = \frac{1}{n}$  
    > [코드 링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL64C1-L74C27)
</br>  

  * 샤프 비율 최대화 (Max Sharpe Ratio)
    > $Maximize: SR_p = \frac{w^TR}{\sqrt{w^T\sum w}}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL76C9-L101C29)
</br>  

  * 글로벌 최소 분산 (Global Minimum Variance)
    > $Minimize: \sigma_p = \sqrt{w^T\sum w}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL103C9-L126C29)
</br>  

  * 최대 분산투자 포트폴리오 (Most Diversified Portfolio)
    > $Maximize: DR = \frac{w^T\sigma}{\sqrt{w^T\sum w}}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL128C9-L153C29)
</br>  

  * 리스크 패리티 (Risk Parity)
    > $Minimize:\sum\limits_{i=1}^N (w_i\frac{(\sum w)_i}{\sigma_p^2}-\frac{1}{N})^2$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL155C9-L182C29)
</br>  

  * 동등 한계 변동성 (Equal Marginal Volatility)  
    > $w_i = \frac{1/\sigma_i}{\sum\limits_{i=1}^N 1/\sigma_i}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL184C9-L195C27)
</br>  

  <h3>포트폴리오 가중치 할당 모델</h3>  
  
  * 변동성 타겟팅 (Volatility Targeting)  
    > $W_p = \frac{\sigma_t}{\sigma_p}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL203C9-L216C27)
</br>  

  * CVaR 타겟팅 (CVaR Targeting)
    > $W_p = \frac{CVaR_t}{CVaR_p}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL218C8-L236C27)
</br>  
</details>  

## 거래 제약 조건
## 과거 데이터 테스트
