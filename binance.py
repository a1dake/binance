import random
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import unittest

api_key = 'your_api_key'
api_secret = 'your_secret_key'

client = Client(api_key, api_secret)

def create_orders(order_data):
    volume = order_data['volume']
    number = order_data['number']
    amountDif = order_data['amountDif']
    side = order_data['side']
    priceMin = order_data['priceMin']
    priceMax = order_data['priceMax']

    orders = []
    volume_per_order = volume / number

    for i in range(number):
        volume_range = (volume_per_order - amountDif, volume_per_order + amountDif)
        volume_order = random.uniform(*volume_range)

        price_order = random.uniform(priceMin, priceMax)

        try:
            result = client.create_order(
                symbol='BTCUSDT',
                side=side,
                type='LIMIT',
                quantity=volume_order / price_order,
                price=price_order)

            orders.append(result)

        except BinanceAPIException as e:
            print(f"API error: {e}")

        except BinanceOrderException as e:
            print(f"Order error: {e}")

        except Exception as e:
            print(f"Unknown error: {e}")

    return orders

class TestCreateOrders(unittest.TestCase):
    def test_create_orders(self):
        order_data = {
            "volume": 10000.0,
            "number": 5,
            "amountDif": 50.0,
            "side": "SELL",
            "priceMin": 200.0,
            "priceMax": 300.0
        }

        orders = create_orders(order_data)
        self.assertEqual(len(orders), order_data['number'], "Number of orders created is incorrect")