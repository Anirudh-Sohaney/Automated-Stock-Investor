#simulation program
#simulates investing pattern for every 5 minutes

import prediction_model
import data
import math

stocks = {}
balance = int(input("enter starting balance : "))
data_ = data.pres
for time in data.sim_data[list(data.sim_data.keys())[0]]:
    print(time)
    preds = {}
    for company in data_:
        data_[company][time] = data.sim_data[company][time]
        preds[company] = list(prediction_model.predict_stock_movement(data_[company]))
    percents = prediction_model.calculate_investment_percent(preds)
    if stocks != {}:
        earned = 0
        dels = []
        for stock in stocks:
            if stock in percents:
                print(f"holding {stock}")
            else:
                price = data_[stock][time][1]
                sell = price * stocks[stock]
                earned += sell
                print(f"sold | {stock} | ${price} | {stocks[stock]} | {sell}")
                dels.append(stock)
        for del_ in dels:
            del stocks[del_]
        balance += earned
    if percents != {}:
        spent = 0
        for stock in percents:
            price = data_[stock][time][1]
            purchase_stocks = math.floor((percents[stock] * balance) / price)
            amount = purchase_stocks * price
            if amount != 0:
                if stock in stocks: stocks[stock] += purchase_stocks
                else: stocks[stock] = purchase_stocks
                spent += amount
                print(f"purchased | {stock} | ${price} | {purchase_stocks} | ${purchase_stocks*price} | {stocks[stock]}")
        balance -= spent
    print(f"End balance : ${balance}")

print(f"final balance : ${balance}")
