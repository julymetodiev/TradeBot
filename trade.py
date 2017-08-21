import pandas
from apiwrapper import PoloniexWrapper
import alert
import quant


def analyze_and_trade(period=300, window_size=55, std_dev=2, sell_threshold=360):
    P = PoloniexWrapper()
    chart_data = P.get_chart_data('BTC', period=period)
    df = pandas.DataFrame(chart_data)
    rolling_mean, upper_band, lower_band = quant.bollinger_bands(df['close'], window_size, std_dev)
    
    last_lower_band = lower_band[lower_band.size-1]
    last_upper_band = upper_band[upper_band.size-1]
    last_close = df['close'][df['close'].size-1]
    
    if (last_close < last_lower_band):
        usdt_balance = float(p.get_balances()['USDT'])
        order_book = p.get_order_book('USDT_BTC')
        rate = float(order_book['asks'][5][0])
        amount = (usdt_balance / rate)
        print(p.buy('USDT_BTC', rate, amount))
        alert.send_email_alert("Trade Alert", "Bought BTC")
    elif (last_close > last_upper_band):
        btc_balance = float(p.get_balances()['BTC'])
        order_book = p.get_order_book('USDT_BTC')
        rate = float(order_book['bids'][5][0])
        print(p.sell('USDT_BTC', rate, btc_balance))
        alert.send_email_alert("Trade Alert", "Sold BTC")
    
    
