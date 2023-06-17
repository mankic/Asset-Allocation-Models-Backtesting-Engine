# 📎 객체 지향적 자산 배분 모델 백테스트 엔진 구현
## About
포트폴리오 자산군의 과거 주가 데이터를 입력받아 주어진 자산 배분 모델 내에서 백테스트를 진행하고 성과를 볼 수 있도록 함.

<details>
  <summary><h2>Structure</h2></summary>
  <img width="50%" height="50%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/1e8d7adc-1013-426a-a5ec-9fc4aae2d111"></img>  
  </br>
</details>  

<details>
  <summary><h2>Environment</h2></summary>  
  
  * Python 3.9.16  
  
  * Numpy 1.24.3  
  
  * Pandas 1.5.3  
  
  * Matplotlib 3.7.1  
  
  * Scipy 1.10.1  
  
  * QuantStats 0.0.59
  </br>
</details>  

<details>
  <summary><h2>자산 배분 모형 목록</h2></summary>  
  
  <h3>1. 자산간 가중치 할당 모델</h3>  
  
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

  <h3>2. 포트폴리오 가중치 할당 모델</h3>  
  
  * 변동성 타겟팅 (Volatility Targeting)  
    > $W_p = \frac{\sigma_t}{\sigma_p}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL203C9-L216C27)
</br>  

  * CVaR 타겟팅 (CVaR Targeting)
    > $W_p = \frac{CVaR_t}{CVaR_p}$  
    > [코드링크](https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/blob/2cbd39796f2281bfc8c75dd2ea8341fe2bc80e43/asset_allocation_models_backtesting.py#LL218C8-L236C27)
</br>  
</details>  

<details>
  <summary><h2>거래 제약 조건</h2></summary>  

  * long-only  
  
  * 공매도 및 레버리지 불가  
  
  * (각 자산들의 가중치 합) = (포트폴리오 전체 가중치)  
  
  * 수익률에서 배당금은 계산하지 않음
  
  * 거래비용은 재투자를 가정한 복리수익률 수식을 사용함
    > $cost_{i,t} = abs(w_{i,t} - \frac{w_{i,t-1} (1+r_{i,t})}{\sum w_{i,t-1} (1+r_{i,t})}) * tc$  
  
  </br>
</details>  

<details>
  <summary><h2>백테스트 예시 및 결과</h2></summary>  
  <h3>1. 사용 데이터</h3>  
  
  * 출처 :  
    Yahoo Finance  
  
  * 구성 종목 :  
    |ETF|Sector|  
    |:---:|:---:|  
    |XLB|S&P500 원자재 기업 구성|  
    |XLE|S&P500 에너지 기업 구성|  
    |XLF|S&P500 대형 금융, 투자 기업 구성|  
    |XLI|S&P500 산업재 기업 구성|  
    |XLK|S&P500 대형 기술 기업 구성|  
    |XLP|S&P500 대형 필수 소비재 기업 구성|  
    |XLU|S&P500 유틸리티 기업 구성|  
    |XLV|S&P500 대형 헬스 케어 기업 구성|  
    |XLY|S&P500 임의 소비재 기업 구성|  
  
  * 기간 :  
    2013-06-01 ~ 2023-06-16  
    
  <h3>2. 선택 모델</h3>  
  
  * 자산 배분 :  
    Risk-Parity Model  
  
  * 포트폴리오 배분 :  
    Volatility Targeting Model  
    
  <h3>3. 코드 예시</h3>  
  
```python
# 포트폴리오 객체 생성
etf_portfolio = AssetAllocationBacktest(df)

  
# 백테스트 실행, 결과 저장
rp_vt_model = etf_df.run(cs_model='RP', ts_model='VT', cost=0.0005)

  
# 백테스팅 결과 시각화
etf_portfolio.performance_analytics(*rp_vt_model, qs_report=True)
```  
  
  <h3>4. 결과 시각화</h3>  
  <p>
    <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/4937a43c-6988-47ba-9828-c055c04a30d8"></img>  
    <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/4036a937-c78b-4ab7-b7ce-18499b1c6f00"></img>  
    <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/e8d28fdf-55f2-4743-a459-8c4aa8982fb1"></img>  
  </p>
  
  <h3>5. QuantStats 결과</h3>  
  <p>
  <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/c4cfabdf-d572-4873-a3ec-01217bccfe77"></img>  
  <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/8d8acf7a-a2c9-4e73-8ceb-ed97e5ef6fcb"></img>  
  <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/01d9e0ed-ccb9-43c4-b949-f32e1efdd0b6"></img>  
  <img width="40%" height="40%" src="https://github.com/mankic/Asset-Allocation-Models-Backtesting-Engine/assets/104434422/2cb10b31-aaa6-4451-9c1d-bcf0c3f6b5c4"></img>  
  </p>
</details>  
