import numpy as np


def bollinger_bands(prices, window_size, std_dev):
    rolling_mean = prices.rolling(window=window_size).mean()
    rolling_std  = prices.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*std_dev)
    lower_band = rolling_mean - (rolling_std*std_dev)
    return rolling_mean, upper_band, lower_band
    

def calculate_profit(prices, upper_band, lower_band, window_size=30, sell_threshold=10):
    profit = 0
    buy = []
    trade_counter = 0
    
    for i in range(len(prices)):
        if np.isnan(upper_band[i]):
            continue
        
        if prices[i] < lower_band[i]:
            #print("buy")
            trade_counter += 1
            buy.append((i, prices[i]))
        elif prices[i] > upper_band[i]:
            #print("sell")
            trade_counter += 1
            for _ in range(len(buy)):
                profit += prices[i] - buy.pop()[1]
                
        while len(buy) > 0 and i - buy[0][0] > sell_threshold:
            profit += prices[i] - buy.pop(0)[1]
    #print("Trade counter: ", trade_counter)
    return profit
    

def calculate_average_window(prices, upper_band, lower_band):
    L = None
    lengths = []
    
    for i in range(len(prices)):
        if np.isnan(upper_band[i]):
            continue
        
        if prices[i] < lower_band[i]:
            if L is None:
                L = i
        elif prices[i] > upper_band[i]:
            if L is not None:
                lengths.append(i-L)
                L = None
    print(lengths)
    x = 0
    for l in lengths:
        x += l
    x = x/len(lengths)
    return x