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


def is_successful_transaction(T):
    if T and "resultingTrades" in T and float(T["resultingTrades"][0]["amount"]) > 0:
        return True
        
    return False


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
        result = P.buy('USDT_BTC', rate, amount)
        if is_successful_transaction(result):
            body = "Bought " + str(amount) + " BTC at " + "$" + str(rate) + ".\n"
            alert.send_email_alert("Trade Alert", body)
    elif (last_close > last_upper_band):
        btc_balance = float(P.get_balances()['BTC'])
        order_book = P.get_order_book('USDT_BTC')
        rate = float(order_book['bids'][5][0])
        print(btc_balance)
        result = P.sell('USDT_BTC', rate, btc_balance)
        if is_successful_transaction(result):
            body = "Sold " + str(btc_balance) + " BTC at " + "$" + str(rate)
            alert.send_email_alert("Trade Alert", "Sold BTC")
    
    print("Ran trade script at " + alert.get_pacific_time())

if __name__ == "__main__":
    analyze_and_trade()
