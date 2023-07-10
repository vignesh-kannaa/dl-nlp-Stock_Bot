from flask import Flask, request, render_template,jsonify
from src.db_connection import StockDB
from src.stocksApi import StockAPI
import src.helper as helper

application = Flask(__name__)
app = application

customerId = 101 #tesing with customerId

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fulfillment', methods=['POST'])
def fulfilmentRequest():
    payload = request.json
    intent = payload['queryResult']['intent']['displayName']
    res = ''
    print('intent: ', intent)
    intent_functions = {
        'current.price': getCurrentPrice,
        'portfolio.overview': getPortfolio,
        'transaction.history': getTransactionHistory,
        'portfolio.performance': getPortfolioPerformance,
    }

    if intent in intent_functions:
        res = intent_functions[intent](payload)
    else:
        res = 'Invalid intent'

    # return jsonify(content={"fulfillmentText": res})
    response = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [res]
                }
            }
        ]
    }
    return jsonify(response)


def getCurrentPrice(payload):
    parameters = payload['queryResult']['parameters']
    stockCompany = parameters['stock-company']
    number = parameters['number']
    if stockCompany is None:
        return 'Please provide the company'
    else:
        stockAPI = StockAPI()
        for company in stockCompany:
            data = stockAPI.stockById(company)
            currentPrice = data["financialData"]["currentPrice"]["raw"]
            if number:
                result = f"{number} stocks in {company} - {number * currentPrice} "+'\n'
            else:
                result = f"{company} - {currentPrice}  "
    return result


def getPortfolio(payload):
    db = StockDB()
    transactions = db.stockListById(customerId)
    dbData = helper.calculateStocksByTransactionType(transactions)
    result = ''
    for company, count in dbData.items():
        result += f"{count} shares in {company} " +'\n'
    print(result)
    return result


def getTransactionHistory(payload):
    db = StockDB()
    data = db.transactionHitory()
    result = 'Stock Transactions:\n'
    for row in data:
        company, symbol, quantity, action, timestamp, price = row
        result += company+' - '+action+'\n' + \
            'Quantity: '+str(quantity)+'\n' +\
            'Price: '+str(price)+'\n' +\
            'Date: '+timestamp.strftime('%Y-%m-%d %H:%M:%S')+'\n' + '---'+'\n'

    print(result)
    return result


def getPortfolioPerformance(payload):
    db = StockDB()
    data = db.transactionHitory()
    transHist = []
    for row in data:
        company, symbol, quantity, action, timestamp, price = row
        transHist.append({
            'Company': company,
            'Symbol': symbol,
            'Quantity': quantity,
            'Action': action,
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Price': str(price)
        })
    currentMarket = []
    stockAPI = StockAPI()
    unique_companies = set()
    for entry in transHist:
        if entry["Action"] == "Buy":
            unique_companies.add(entry["Symbol"])

    for symbol in unique_companies:
        data = stockAPI.stockById(symbol)
        currentPrice = data["financialData"]["currentPrice"]["raw"]
        currentMarket.append({
            'Company': symbol,
            'Price': currentPrice
        })
    result = helper.calcualteGainLoss(transHist, currentMarket)
    print(result)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0")

    # uvicorn main:app --reload
    # ngrok http 8000
