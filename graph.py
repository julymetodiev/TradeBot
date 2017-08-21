import pandas as pd
import matplotlib.pyplot as plt
import alert
import quant
import poloniex


def analyze_poloniex_chart_data(data, window_size=30, std_dev=2, sell_threshold=10):
    df = pd.DataFrame(data)
    rolling_mean, upper_band, lower_band = quant.bollinger_bands(df['close'], window_size, std_dev)
    
    last_lower_band = lower_band[lower_band.size-1]
    last_close = df['close'][df['close'].size-1]
    
    profit = quant.calculate_profit(df['close'], upper_band, lower_band, window_size, sell_threshold)
    return profit
    #avg = quant.calculate_average_window(df['close'], upper_band, lower_band)
    #print(avg)
    
    
    '''if (last_close < last_lower_band):
        alert.send_email_alert("Bollinger band alert! Price dropped below lower band!")
        print("Sent email alert")
    
    bb = pd.DataFrame(
        {
            'rolling_mean': rolling_mean,
            'upper_band': upper_band,
            'lower_band': lower_band,
            'close': df['close']
        }
    )
    bb.plot()
    plt.show()'''


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
                
    data = poloniex.get_poloniex_chart_data(period=300)
    profit = analyze_poloniex_chart_data(data, window_size=110, std_dev=2, sell_threshold=24)
    print(profit)
    
    
    
    
    
    
    
    
    