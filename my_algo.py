from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import math
import pandas as pd


class Trader:
    def __init__(self):
        self.DS_last = 0
        self.DS_cur = 0
        self.indicator = 0 #set 0 not trade, 1 buy, -1 sell
        self.ukll = 0
        self.ukll_check = 0
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                positions = state.position[product] if product in state.position else 0
                position_limit = 20
                position_ratio = positions/position_limit
                rest_position_bid = (1-position_ratio)*position_limit
                rest_position_ask = (-1-position_ratio)*position_limit
                acceptable_price = 10000 + (-1/10)*positions
                # If statement checks if there are any SELL orders in the PEARLS market


                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                # if best_ask < acceptable_price:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order

                if best_ask <= acceptable_price:
                    if -best_ask_volume > rest_position_bid:
                        # print("BUY", str(rest_position_bid) + "x", best_ask)
                        orders.append(Order(product, best_ask, rest_position_bid))
                    else:
                        # print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                elif (best_ask-1) >= acceptable_price:
                    if best_ask_volume < rest_position_ask:
                        # print("SELL", str(-rest_position_ask) + "x", (best_ask-1))
                        orders.append(Order(product, (best_ask-1), rest_position_ask))
                    else:
                        # print("SELL", str(-best_ask_volume) + "x", (best_ask-1))
                        orders.append(Order(product, (best_ask-1), best_ask_volume))
                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium

                if best_bid >= acceptable_price:
                    if -best_bid_volume < rest_position_ask:
                        # print("SELL", str(-rest_position_ask) + "x", best_bid)
                        orders.append(Order(product, best_bid, rest_position_ask))
                    else:
                        # print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                elif (best_bid+1) <= acceptable_price:
                    if best_bid_volume > rest_position_bid:
                        # print("BUY", str(rest_position_bid) + "x", (best_bid+1))
                        orders.append(Order(product, (best_bid+1), rest_position_bid))
                    else:
                        # print("BUY", str(best_bid_volume) + "x", (best_bid+1))
                        orders.append(Order(product, (best_bid+1), best_bid_volume))
                # Add all the above the orders to the result dict
                result[product] = orders

            if product == 'BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]

                w_ask_p_t = 0
                w_ask_v_t = abs(sum(order_depth.sell_orders.values()))
                w_bid_p_t = 0
                w_bid_v_t = abs(sum(order_depth.buy_orders.values()))
                for i in order_depth.sell_orders.keys():
                    w_ask_p_t += (i*abs(order_depth.sell_orders[i])) #positive
                    # w_ask_v_t += abs(order_depth.sell_orders[i])
                w_ask_p = w_ask_p_t/w_ask_v_t
                for i in order_depth.buy_orders.keys():
                    w_bid_p_t += (i*order_depth.buy_orders[i])
                    # w_bid_v_t += order_depth.buy_orders[i]
                w_bid_p = w_bid_p_t/w_bid_v_t

                positions = state.position[product] if product in state.position else 0
                position_limit = 20
                position_ratio = positions/position_limit
                rest_position_bid = int((1-position_ratio)*position_limit)
                rest_position_ask = int((-1-position_ratio)*position_limit)

                acceptable_price = (w_ask_p+w_bid_p)/2 +(-1/10)*positions


                if best_ask <= acceptable_price:
                    if -best_ask_volume > rest_position_bid:
                        # print("BUY", str(rest_position_bid) + "x", best_ask)
                        orders.append(Order(product, best_ask, rest_position_bid))
                    else:
                        # print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                elif (best_ask-1) >= acceptable_price:
                    if best_ask_volume < rest_position_ask:
                        # print("SELL", str(-rest_position_ask) + "x", (best_ask-1))
                        orders.append(Order(product, (best_ask-1), rest_position_ask))
                    else:
                        # print("SELL", str(-best_ask_volume) + "x", (best_ask-1))
                        orders.append(Order(product, (best_ask-1), best_ask_volume))

                if best_bid >= acceptable_price:
                    if -best_bid_volume < rest_position_ask:
                        # print("SELL", str(-rest_position_ask) + "x", best_bid)
                        orders.append(Order(product, best_bid, rest_position_ask))
                    else:
                        # print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                elif (best_bid+1) <= acceptable_price:
                    if best_bid_volume > rest_position_bid:
                        # print("BUY", str(rest_position_bid) + "x", (best_bid+1))
                        orders.append(Order(product, (best_bid+1), rest_position_bid))
                    else:
                        # print("BUY", str(best_bid_volume) + "x", (best_bid+1))
                        orders.append(Order(product, (best_bid+1), best_bid_volume))
                result[product] = orders

            if product == 'COCONUTS':
                order_depth: OrderDepth = state.order_depths[product]
                order_depth_p: OrderDepth = state.order_depths['PINA_COLADAS']
                orders: list[Order] = []
                orders_p: list[Order] = []

                positions = state.position[product] if product in state.position else 0
                positions_p = state.position['PINA_COLADAS'] if 'PINA_COLADAS' in state.position else 0

                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                mid_price = (best_ask+best_bid)/2

                best_ask_p = min(order_depth_p.sell_orders.keys())
                best_bid_p = max(order_depth_p.buy_orders.keys())
                mid_price_p = (best_ask_p+best_bid_p)/2

                acceptable_price = (mid_price+(mid_price_p*8/15))/2
                edge = acceptable_price - mid_price
                percent_c_plan = edge/15
                percent_p_plan = -percent_c_plan

                limit_position = 600
                limit_position_p = 300
                percentage_C = positions/limit_position
                percentage_P = positions_p/limit_position_p

                if percent_c_plan < percentage_C:
                    if abs(percent_c_plan) > 1:
                        percent_c_plan = -1
                    need_percentage = percent_c_plan-percentage_C #negative percentage needed
                    need_volumn = math.floor(limit_position*need_percentage) #is negative

                    # if abs(edge) <= 15:
                    # print("SELL", str(-need_volumn) + "x", (best_ask-1))
                    orders.append(Order(product, (best_ask-1), need_volumn))
                    # else:
                    #     print("SELL", str(-need_volumn) + "x", best_bid)
                    #     orders.append(Order(product, best_bid, need_volumn))

                elif percent_c_plan > percentage_C:
                    if abs(percent_c_plan) > 1:
                        percent_c_plan = 1
                    need_percentage = percent_c_plan-percentage_C #positive percentage needed
                    need_volumn = math.floor(limit_position*need_percentage) #is positive
                    #
                    # if abs(edge) <= 15:
                    # print("BUY", str(need_volumn) + "x", (best_bid+1))
                    orders.append(Order(product, (best_bid+1), need_volumn))
                    # else:
                    #     print("BUY", str(need_volumn) + "x", best_ask)
                    #     orders.append(Order(product, best_ask, need_volumn))

                if percent_p_plan < percentage_P:
                    if abs(percent_p_plan) > 1:
                        percent_c_plan = -1
                    need_percentage = percent_p_plan-percentage_P #negative percentage needed
                    need_volumn = math.floor(limit_position_p*need_percentage) #is negative
                    #
                    # if abs(edge) <= 15:
                    # print("SELL", str(-need_volumn) + "x", (best_ask_p-1))
                    orders_p.append(Order('PINA_COLADAS', (best_ask_p-1), need_volumn))
                    # else:
                    #     print("SELL", str(-need_volumn) + "x", best_bid_p)
                    #     orders_p.append(Order('PINA_COLADAS', best_bid_p, need_volumn))

                elif percent_p_plan > percentage_P:
                    if abs(percent_p_plan) > 1:
                        percent_c_plan = 1
                    need_percentage = percent_p_plan-percentage_P #positive percentage needed
                    need_volumn = math.floor(limit_position_p*need_percentage) #is positive

                    # if abs(edge) <= 15:
                    # print("BUY", str(need_volumn) + "x", (best_bid_p+1))
                    orders_p.append(Order('PINA_COLADAS', (best_bid_p+1), need_volumn))
                    # else:
                    #     print("BUY", str(need_volumn) + "x", best_ask_p)
                    #     orders_p.append(Order('PINA_COLADAS', best_ask_p, need_volumn))

                result[product] = orders
                result['PINA_COLADAS'] = orders_p

            if product == 'BERRIES':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                time = state.timestamp

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]

                mid_price = (best_ask + best_bid)/2
                # df_berry = pd.DataFrame({'time':[]},'mid_price':[])
                # berry_timecount = 0

                w_ask_p_t = 0
                w_ask_v_t = abs(sum(order_depth.sell_orders.values()))
                w_bid_p_t = 0
                w_bid_v_t = abs(sum(order_depth.buy_orders.values()))
                for i in order_depth.sell_orders.keys():
                    w_ask_p_t += (i*abs(order_depth.sell_orders[i])) #positive
                w_ask_p = w_ask_p_t/w_ask_v_t
                for i in order_depth.buy_orders.keys():
                    w_bid_p_t += (i*order_depth.buy_orders[i])
                w_bid_p = w_bid_p_t/w_bid_v_t

                positions = state.position[product] if product in state.position else 0
                position_limit = 250
                position_ratio = positions/position_limit
                rest_position_bid = (1-position_ratio)*position_limit
                rest_position_ask = (-1-position_ratio)*position_limit
                acceptable_price = (w_ask_p+w_bid_p)/2 +(-1/position_limit)*positions

                if time < 250000 or time > 750000:
                    if best_ask <= acceptable_price:
                        if -best_ask_volume > rest_position_bid:
                            # print("BUY", str(rest_position_bid) + "x", best_ask)
                            orders.append(Order(product, best_ask, rest_position_bid))
                        else:
                            # print("BUY", str(-best_ask_volume) + "x", best_ask)
                            orders.append(Order(product, best_ask, -best_ask_volume))
                    elif (best_ask-1) >= acceptable_price:
                        if best_ask_volume < rest_position_ask:
                            # print("SELL", str(-rest_position_ask) + "x", (best_ask-1))
                            orders.append(Order(product, (best_ask-1), rest_position_ask))
                        else:
                            # print("SELL", str(-best_ask_volume) + "x", (best_ask-1))
                            orders.append(Order(product, (best_ask-1), best_ask_volume))
                    if best_bid >= acceptable_price:
                        if -best_bid_volume < rest_position_ask:
                            # print("SELL", str(-rest_position_ask) + "x", best_bid)
                            orders.append(Order(product, best_bid, rest_position_ask))
                        else:
                            # print("SELL", str(best_bid_volume) + "x", best_bid)
                            orders.append(Order(product, best_bid, -best_bid_volume))
                    elif (best_bid+1) <= acceptable_price:
                        if best_bid_volume > rest_position_bid:
                            # print("BUY", str(rest_position_bid) + "x", (best_bid+1))
                            orders.append(Order(product, (best_bid+1), rest_position_bid))
                        else:
                            # print("BUY", str(best_bid_volume) + "x", (best_bid+1))
                            orders.append(Order(product, (best_bid+1), best_bid_volume))
                elif time > 250000 and time < 500000:
                    if positions < position_limit:
                        if -best_ask_volume > rest_position_bid:
                        # print("BUY", str(rest_position_bid) + "x", best_ask)
                            orders.append(Order(product, best_ask, rest_position_bid))
                        else:
                            # print("BUY", str(-best_ask_volume) + "x", best_ask)
                            orders.append(Order(product, best_ask, -best_ask_volume))

                elif time > 500000 and time < 750000:
                    if positions > -position_limit:
                        if -best_bid_volume < rest_position_ask:
                            # print("SELL", str(-rest_position_ask) + "x", best_bid)
                            orders.append(Order(product, best_bid, rest_position_ask))
                        else:
                            # print("SELL", str(best_bid_volume) + "x", best_bid)
                            orders.append(Order(product, best_bid, -best_bid_volume))

                result[product] = orders

            if product == 'DIVING_GEAR':
                # time = state.timestamp
                self.DS_last = self.DS_cur
                # print(self.DS_last)
                self.DS_cur = state.observations['DOLPHIN_SIGHTINGS']
                # print(self.DS_cur)
                if abs(self.DS_cur - self.DS_last) > 50: #not possible, and exclude lambda problem:
                    dif = 0
                else:
                    dif = self.DS_cur - self.DS_last
                # print(dif)

                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                positions = state.position[product] if product in state.position else 0

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]

                limit_position = 50
                position_ratio = positions/position_limit
                rest_position_bid = (1-position_ratio)*position_limit
                rest_position_ask = (-1-position_ratio)*position_limit
                # self.indicator = 0 set 0 not trade, 1 buy, -1 sell
                #trade
                if dif >= 5:
                    self.indicator = 1
                elif dif <= -5:
                    self.indicator = -1

                if self.indicator == 1: #buy, dophin grow fast
                    if positions < position_limit:
                        if -best_ask_volume > rest_position_bid:
                            # print("BUY", str(rest_position_bid) + "x", best_ask)
                            orders.append(Order(product, best_ask, rest_position_bid))
                        else:
                            # print("BUY", str(-best_ask_volume) + "x", best_ask)
                            orders.append(Order(product, best_ask, -best_ask_volume))
                elif self.indicator == -1: #sell, dophin drop fast
                    if positions > -position_limit:
                        if -best_bid_volume < rest_position_ask:
                            # print("SELL", str(-rest_position_ask) + "x", best_bid)
                            orders.append(Order(product, best_bid, rest_position_ask))
                        else:
                            # print("SELL", str(best_bid_volume) + "x", best_bid)
                            orders.append(Order(product, best_bid, -best_bid_volume))

                result[product] = orders

            if product == 'PICNIC_BASKET':
                order_depth: OrderDepth = state.order_depths[product]
                order_depth_u: OrderDepth = state.order_depths['UKULELE']
                order_depth_b: OrderDepth = state.order_depths['BAGUETTE']
                order_depth_d: OrderDepth = state.order_depths['DIP']

                orders: list[Order] = []
                orders_u: list[Order] = []
                orders_b: list[Order] = []
                orders_d: list[Order] = []

                positions = state.position[product] if product in state.position else 0
                positions_u = state.position['UKULELE'] if 'UKULELE' in state.position else 0
                positions_b = state.position['BAGUETTE'] if 'BAGUETTE' in state.position else 0
                positions_d = state.position['DIP'] if 'DIP' in state.position else 0

                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                mid_price = (best_ask+best_bid)/2

                best_ask_u = min(order_depth_u.sell_orders.keys())
                best_bid_u = max(order_depth_u.buy_orders.keys())
                mid_price_u = (best_ask_u+best_bid_u)/2

                best_ask_b = min(order_depth_b.sell_orders.keys())
                best_bid_b = max(order_depth_b.buy_orders.keys())
                mid_price_b = (best_ask_b+best_bid_b)/2

                best_ask_d = min(order_depth_d.sell_orders.keys())
                best_bid_d = max(order_depth_d.buy_orders.keys())
                mid_price_d = (best_ask_d+best_bid_d)/2

                edge = mid_price - mid_price_u - 2*mid_price_b - 4*mid_price_d - 400 #high - sell, low - buy
                edge_max = 300
                percent_pb_plan = -edge/edge_max
                percent_res_plan = -percent_pb_plan

                limit_position = 70
                limit_position_u = 70
                limit_position_b = 150 #150
                limit_position_d = 300 #300

                percentage_pb = positions/limit_position
                percentage_u = positions_u/limit_position_u
                percentage_b = positions_b/limit_position_b
                percentage_d = positions_d/limit_position_d
                """the PICNIC_BASKET"""
                if percent_pb_plan < percentage_pb:
                    if abs(percent_pb_plan) > 1:
                        percent_pb_plan = -1
                    need_percentage = percent_pb_plan-percentage_pb #negative percentage needed
                    need_volumn = math.floor(limit_position*need_percentage) #is negative

                    # if abs(edge) <= 250:
                    #     print("SELL", str(-need_volumn) + "x", (best_ask-1))
                    #     orders.append(Order(product, (best_ask-1), need_volumn))
                    # else:
                    # print("SELL", str(-need_volumn) + "x", best_ask-1)
                    orders.append(Order(product, best_ask-1, need_volumn))

                elif percent_pb_plan > percentage_pb:
                    if abs(percent_pb_plan) > 1:
                        percent_pb_plan = 1
                    need_percentage = percent_pb_plan-percentage_pb #positive percentage needed
                    need_volumn = math.floor(limit_position*need_percentage) #is positive
                    #
                    # if abs(edge) <= 15:
                    # print("BUY", str(need_volumn) + "x", (best_bid+1))
                    orders.append(Order(product, (best_bid+1), need_volumn))
                    # else:
                    #     print("BUY", str(need_volumn) + "x", best_ask)
                    #     orders.append(Order(product, best_ask, need_volumn))
                result[product] = orders
                """now UKULELE"""
                market_trades_u = state.market_trades['UKULELE'] if 'UKULELE' in state.market_trades else []
                for i in market_trades_u:
                    if i.buyer == 'Olivia':
                        self.ukll = 1
                        self.ukll_check += 1
                    elif i.seller == 'Olivia':
                        self.ukll = -1
                        self.ukll_check += 1

                if percentage_u > 0.95 or percentage_u < -0.95:
                    if self.ukll_check >= 2 or self.ukll_check == 0:
                        self.ukll = 0

                if self.ukll == 1:
                    if percentage_u < 1:
                        need_percentage = 1-percentage_u
                        need_volumn = math.floor(limit_position_u*need_percentage)
                        orders_u.append(Order('UKULELE', best_bid+1, need_volumn))
                elif self.ukll == -1:
                    if percentage_u > -1:
                        need_percentage = -1-percentage_u # negative
                        need_volumn = math.floor(limit_position_u*need_percentage) #negative
                        orders_u.append(Order('UKULELE', best_ask-1, need_volumn))
                elif self.ukll == 0:
                    if percent_res_plan < percentage_u:
                        if abs(percent_res_plan) > 1:
                            percent_res_plan = -1
                        need_percentage = percent_res_plan-percentage_u #negative percentage needed
                        need_volumn = math.floor(limit_position_u*need_percentage) #is negative
                        # print("SELL", str(-need_volumn) + "x", best_ask-1)
                        orders_u.append(Order('UKULELE', best_ask-1, need_volumn))

                    elif percent_res_plan > percentage_u:
                        if abs(percent_res_plan) > 1:
                            percent_res_plan = 1
                        need_percentage = percent_res_plan-percentage_u #positive percentage needed
                        need_volumn = math.floor(limit_position_u*need_percentage) #is positive
                        # print("BUY", str(need_volumn) + "x", (best_bid+1))
                        orders_u.append(Order('UKULELE', (best_bid+1), need_volumn))
                result['UKULELE'] = orders_u

                """now BAGUETTE"""
                if percent_res_plan < percentage_b:
                    if abs(percent_res_plan) > 1:
                        percent_res_plan = -1
                    need_percentage = percent_res_plan-percentage_b #negative percentage needed
                    need_volumn = math.floor(limit_position_b*need_percentage) #is negative
                    # print("SELL", str(-need_volumn) + "x", best_ask-1)
                    orders_b.append(Order('BAGUETTE', best_ask-1, need_volumn))

                elif percent_res_plan > percentage_b:
                    if abs(percent_res_plan) > 1:
                        percent_res_plan = 1
                    need_percentage = percent_res_plan-percentage_b #positive percentage needed
                    need_volumn = math.floor(limit_position_b*need_percentage) #is positive
                    # print("BUY", str(need_volumn) + "x", (best_bid+1))
                    orders_b.append(Order('BAGUETTE', (best_bid+1), need_volumn))
                result['BAGUETTE'] = orders_b

                """now DIP"""
                if percent_res_plan < percentage_d:
                    if abs(percent_res_plan) > 1:
                        percent_res_plan = -1
                    need_percentage = percent_res_plan-percentage_d #negative percentage needed
                    need_volumn = math.floor(limit_position_d*need_percentage) #is negative
                    # print("SELL", str(-need_volumn) + "x", best_ask-1)
                    orders_d.append(Order('DIP', best_ask-1, need_volumn))

                elif percent_res_plan > percentage_d:
                    if abs(percent_res_plan) > 1:
                        percent_res_plan = 1
                    need_percentage = percent_res_plan-percentage_d #positive percentage needed
                    need_volumn = math.floor(limit_position_d*need_percentage) #is positive
                    # print("BUY", str(need_volumn) + "x", (best_bid+1))
                    orders_d.append(Order('DIP', (best_bid+1), need_volumn))
                result['DIP'] = orders_d
                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result
