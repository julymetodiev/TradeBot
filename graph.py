import pandas as pd
import matplotlib.pyplot as plt
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
    p = PoloniexWrapper(config.POLONIEX_API_KEY, config.POLONIEX_API_SECRET)
    data = p.get_chart_data('USDT_BTC', period=300, days=100)
    analyze_poloniex_chart_data(data, window_size=55, std_dev=2, sell_threshold=360)
