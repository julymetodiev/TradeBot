# TradeBot

TradeBot is an automated cryptocurrency trader built with Python. It includes scripts for interacting with currency exchanges, analyzing price data using popular TA methods (e.g. Bollinger Bands), sending email alerts, and more.

At the moment, TradeBot is designed to support [Poloniex](https://poloniex.com/). However, it is fairly trivial to add support for other exchanges. The API wrapper is decoupled from the rest of the library, allowing exchange APIs to be easily interchanged.


## How to set up automated trading

(TradeBot requires Python 3.6.1 in order to run)


Create a virtual environment.
```
$ virtualenv -p python venv
$ source venv/bin/activate
```

Install the required dependencies.
```
$ pip install -r requirements.txt
```

Create a config file using the example config. Fill in the necessary info.
```
$ cp config_EXAMPLE.py config.py
$ vi config.py
```

Create a cron job that will run every five minutes.
```
$ crontab -e

# Add the following line
*/5 * * * * /home/ubuntu/TradeBot/venv/bin/python /home/ubuntu/TradeBot/trade.py
```

Finally, add your email address to the email_list.txt. You can add multiple emails if you wish. If you are using an Amazon EC2 instance, you need to [set up Amazon SES](https://aws.amazon.com/getting-started/tutorials/send-an-email/) and verify each email address.



## How it works

Currently, TradeBot uses [Bollinger Bands](https://en.wikipedia.org/wiki/Bollinger_Bands) to analyze price data. When the price drops below the lower band, a 'buy' transaction is issued. When the price rises above the upper band, a 'sell' transaction is issued.

Using this simple strategy, I've been able to generate an average of 1.5% profit per trade. Of course, your results may vary i.e. I am not responsible for any loss of money.

