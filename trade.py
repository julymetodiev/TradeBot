import pandas
from apiwrapper import PoloniexWrapper
import alert
import quant
import config


def test_simple_bollinger_strategy(period, window_size, std_dev, sell_threshold):
    P = PoloniexWrapper(config.POLONIEX_API_KEY, config.POLONIEX_API_SECRET)
    chart_data = P.get_chart_data('USDT_BTC', period=period)
    df = pandas.DataFrame(chart_data)
    rolling_mean, upper_band, lower_band = quant.bollinger_bands(df['close'], window_size, std_dev)
    print(len(upper_band))
    print(len(lower_band))
    print(len(df['close']))

    for i in range(lower_band.size):
        last_lower_band = lower_band[i]
        last_upper_band = upper_band[i]
        last_close = df['close'][i]

        if (last_close < last_lower_band):
            print("Bought BTC at " + str(i))
        elif (last_close > last_upper_band):
            print("Sold BTC at " + str(i))


def analyze_and_trade(period=300, window_size=55, std_dev=2, sell_threshold=360):
    P = PoloniexWrapper(config.POLONIEX_API_KEY, config.POLONIEX_API_SECRET)
    chart_data = P.get_chart_data('USDT_BTC', period=period)
    df = pandas.DataFrame(chart_data)
    rolling_mean, upper_band, lower_band = quant.bollinger_bands(df['close'], window_size, std_dev)
    
    last_lower_band = lower_band[lower_band.size-1]
    last_upper_band = upper_band[upper_band.size-1]
    last_close = df['close'][df['close'].size-1]
    
    if (last_close < last_lower_band):
        usdt_balance = float(P.get_balances()['USDT'])
        order_book = P.get_order_book('USDT_BTC')
        rate = float(order_book['asks'][5][0])
        amount = (usdt_balance / rate)
        print(P.buy('USDT_BTC', rate, amount))
        alert.send_email_alert("Trade Alert", "Bought BTC")
    elif (last_close > last_upper_band):
        btc_balance = float(P.get_balances()['BTC'])
        order_book = P.get_order_book('USDT_BTC')
        rate = float(order_book['bids'][5][0])
        print(P.sell('USDT_BTC', rate, btc_balance))
        alert.send_email_alert("Trade Alert", "Sold BTC")
    
    print("Ran trade script at " + alert.get_pacific_time())

if __name__ == "__main__":
    analyze_and_trade()
