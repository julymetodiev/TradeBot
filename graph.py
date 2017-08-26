import pandas as pd
import matplotlib.pyplot as plt
#import alert
import config
import quant
from apiwrapper import PoloniexWrapper


def analyze_poloniex_chart_data(data, window_size=30, std_dev=2, sell_threshold=10):
    df = pd.DataFrame(data)
    rolling_mean, upper_band, lower_band = quant.bollinger_bands(df['close'], window_size, std_dev)
    
    last_lower_band = lower_band[lower_band.size-1]
    last_close = df['close'][df['close'].size-1]
    
    bb = pd.DataFrame(
        {
            'rolling_mean': rolling_mean,
            'upper_band': upper_band,
            'lower_band': lower_band,
            'close': df['close']
        }
    )
    bb.plot()
    plt.show()


if __name__ == '__main__':
    '''best_profit = 0
    best_settings = (None, None, None)
    
    for period in [300]:                         #period
        for ws in [20]:            # window size
            for sd in [2]:                       # standard deviation
                for st in [24]:  # sell threshold
                    data = poloniex.get_poloniex_chart_data(period=period)
                    profit = analyze_poloniex_chart_data(data, window_size=ws, std_dev=sd, sell_threshold=st)
                    if profit > best_profit:
                        best_profit = profit
                        best_settings = (period, ws, sd, st)
                    print(best_profit, best_settings)'''
    p = PoloniexWrapper(config.POLONIEX_API_KEY, config.POLONIEX_API_SECRET)
    data = p.get_chart_data('USDT_BTC', period=300, days=100)
    analyze_poloniex_chart_data(data, window_size=55, std_dev=2, sell_threshold=360)
