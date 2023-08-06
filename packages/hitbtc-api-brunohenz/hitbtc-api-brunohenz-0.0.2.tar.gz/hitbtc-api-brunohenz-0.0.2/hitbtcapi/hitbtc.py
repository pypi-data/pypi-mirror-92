from hitbtcClient import HitBtcClient


class HitBtc:
    def __init__(self, apikey, apisecret):
        self.client = HitBtcClient(apikey, apisecret)

    # Currencies
    # Get all currencies from hitbtc
    def get_currencies(self):
        return self.client.api_get_query('public/currency')

    # Order book
    def get_orderbook(self, symbol):
        return self.client.api_get_query('public/orderbook/' + symbol)

    # Orders
    # Get the user's orders
    def get_orders(self):
        return self.client.api_get_query('order')

    # Create a new order
    def create_order(self, orderdata):
        return self.client.api_post_query('order', orderdata)

    # Trades
    # Get the user's trading history
    def get_trades_history(self, symbol):
        paramdata = '?symbol=' + symbol
        return self.client.api_get_query('history/order' + paramdata)
