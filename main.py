import ccxt
import config

binance=ccxt.binance({
        'apiKey': config.apiKey,
        'secret': config.secret,  
        'options': {
        'defaultType': 'future',
    },
    })

def marketorder(symbol,side,lev,stopLossPrice,takeProfitPrice,cost):
        symbol=symbol[:-2]

        orderbook = binance.fetch_order_book(symbol)
        if side=="sell":
            price=orderbook['asks'][0][0]
            amount = cost/price
        else:
            price=orderbook['bids'][0][0]
            amount = cost/price
        
        binance.fapiprivate_post_leverage({'symbol': symbol,'leverage': lev,})
        binance.create_order(symbol, 'market', side, amount,price)
        inverted_side = 'sell' if side == 'buy' else 'buy'
        stopLossParams = {'stopPrice': stopLossPrice}
        binance.create_order(symbol, 'STOP_MARKET', inverted_side, amount, price, stopLossParams)
        takeProfitParams = {'stopPrice': takeProfitPrice}
        binance.create_order(symbol, 'TAKE_PROFIT_MARKET', inverted_side, amount, price, takeProfitParams)

def tradebinance(request):
    data = request.get_json()
    passphrase = data['passphrase']
    ticker = data['ticker']
    side = data['side']
    leverage = data['leverage']
    stoploss = data['stoploss']
    takeprofit = data['takeprofit']
    cost = data['cost']

    if 'passphrase' not in data or passphrase!=config.tradingview_pass:
        binance.cancel_all_orders(binance.market(ticker)['id'])
        return "Canceled_All_order"
    else:
        marketorder(ticker,side,leverage,stoploss,takeprofit,cost)
        return "Cool"
