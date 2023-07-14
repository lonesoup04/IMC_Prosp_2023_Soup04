# IMC_Prosp_2023_Soup04
The algorithm trading bot for IMC Prosperity 2023, 

**Final Ranking: 60th over 7000+ teams**

# Team: Soup04

Pu Su (LinkedIn: https://www.linkedin.com/in/pu-s-16b3b9219/)

# Thoughts

In this game, it's better to think about whether you want to be a maker or a taker in the market: your strategy and the market nature will decide your profits
<br>
**Round 1**<br>

In the first round, there are two categories that can be traded: **pearls** and **bananas**

**for pearls**, the price doesn't change much, fluctuates around 10000

so it's easy to think that we can give a buy order at 9999 and a sell order at 10001, with max sizes we can trade (20)

however, by doing the EDA about the spread of the order book, we can find that the spread sometimes will be 4-6

thus, to get that money, we can have 2 types of execution strategy

keep bid less than and ask over 10000, when there is a buy order over 10000, trade with it, and vice versa; but when there is not, place order at bid+1 / ask-1


<br>**for bananas**, its price fluctuates more, but our max position is still 20, and the banana's price is not a big number (little profit for the taker)

thus, just think how we can get a fair price for banana

as I did the EDA, I found that the bid volume and ask volume have an impact on the t+1 price

thus, I used VWAP to define the fair price and make the market

however, in the first round, since I wrote sell order when I should buy and buy order when I should sell for pearls, my algo profit was negative, and my rank was saved by my manual part, ending with 924<br>

**Round 2**<br>

new products were introduced to us: **Coconuts** and **Pina Coladas**

by doing the correlation analysis, I found that they are highly correlated and can do the pair-trading, be the taker (position is large and the price is high)

8 Pinas = 15 Coconuts (arbitrage both)

to get both products' mid-prices, rescale Pina's mid-price to Coconuts price range, take the average as acceptable_price, and get the edge (= acceptable_price - Coconuts' mid-price)

by analyzing the edge's range (max about +-30, but most frequently shake around 15-20), I set the standard to 15

so the percentage needed for Coconuts is edge/15, and to **hedge** the risk, the percentage needed for Pina is -edge/15

after this round, my rank jumped to 465<br>

<br>**Round 3**<br>

new round, **Mayberries** and **Diving Gear** were involved

for Mayberries, the obvious pattern is that their price will raise before noon and drop after that

so just get the full position before noon and short after that

however, we can improve the strategy by making the market long before or after that time, as the spread of Mayberries reaches 4-6

so I set a certain period for the maker strategy and a certain period for the taker strategy<br>

for Diving Gear(DG), there is other data for Dolphin (which has a high correlation with DG price)

but after doing EDA, I found there is no chance for pair trading

however, by just looking through graphs, I found if there is a huge drop or rise in Dolphin numbers in one tick, DG price will drop or rise slowly

then, by plotting the actual change, I decided to set (+/-5) as a signal, others are just noise

rank -> 111<br>

<br>**Round 4**<br>
New products: Picnic basket (PB) and its three original product DIP, Baguette(B), Ukulele(U)

they have info that PB = 4 DIP + 2B + U (said by rules)

but I got edge = PB - (4 DIP + 2B + U), the edge max around 300

to use -edge/edge_max to get PB percentage, and edge/edge_max as other percentages

But in the end, the lambda problem happened on IMC's server, my DG strategy was based on creating a global variable as the sign, but it was all cleared in the lambda problem, so my rank just jumped to 77<br>

<br>**Round 5**<br>
what's new: we can get some trader's trading information! that means we can totally do mirror trading!

by analyzing their win rate, I found trader "**Oliva**" has a nearly 100% win rate

Oliva trade banana, Ukulele, and Mayberries

but my strategy for bananas and Mayberries has more profits, so I set Ukulele's strategy to mimic Oliva's strategy

rank -> 60<br>

<br>**After all**<br>
This is my first time participating in the algorithm trading competition, though challenging, I found it really fun to discover the pattern behind each product through data analysis

my final was coming at that time, so I didn't have much time for other analysis, and still busy after the break, so sharing these after 4 months

Anyway, hope these thoughts are helpful to you
