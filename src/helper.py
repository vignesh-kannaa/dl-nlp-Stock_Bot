def calculateStocksByTransactionType(transactions):
    stock_count = {}
    print(type(transactions))
    for company, quantity, transactionType in transactions:
        
        if company not in stock_count:
            stock_count[company] = 0

        if transactionType == 'Buy':
            stock_count[company] += quantity
        elif transactionType == 'Sell':
            stock_count[company] -= quantity

    return stock_count


def calcualteGainLoss(transHistory, currentMarket):
    gain_loss = {}
    for transaction in transHistory:
        if transaction["Action"] == "Buy":
            symbol = transaction["Symbol"]
            quantity = transaction["Quantity"]
            buy_price = float(transaction["Price"])

            current_value = next(
                (cv["Price"] for cv in currentMarket if cv["Company"] == symbol), None)

            if current_value is not None:
                current_value = float(current_value)
                gain_loss[symbol] = (current_value - buy_price) * quantity
                percentage = (current_value - buy_price) / buy_price * 100
                gain_loss[symbol] = (gain_loss[symbol], percentage)

    return gain_loss
