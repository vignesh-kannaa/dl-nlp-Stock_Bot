from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates

from fastapi import Request
from fastapi.responses import JSONResponse
from src.db_connection import StockDB
from src.stocksApi import StockAPI
import src.helper as helper
import json

application = FastAPI()
app = application
templates = Jinja2Templates(directory="templates")

customerId = 101


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/fulfillment")
async def fulfilmentRequest(request: Request):
    payload = await request.json()
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

    return JSONResponse(content={"fulfillmentText": res})


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
                result = f"{number} stocks in {company} - {number * currentPrice} ; "
            else:
                result = f"{company} - {currentPrice} ; "
    return result


def getPortfolio(payload):
    db = StockDB()
    transactions = db.stockListById(customerId)
    dbData = helper.calculateStocksByTransactionType(transactions)
    result = ''
    for company, count in dbData.items():
        result += f"{count} shares in {company} ;"
    print(result)
    return result


def getTransactionHistory(payload):
    db = StockDB()
    data = db.transactionHitory()
    table_data = []
    for row in data:
        company, symbol, quantity, action, timestamp, price = row
        table_data.append({
            'Company': company,
            'Symbol': symbol,
            'Quantity': quantity,
            'Action': action,
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Price': str(price)
        })
    # converting to string
    result = json.dumps(table_data)
    print(result)
    return result


def getPortfolioPerformance(payload):
    transHist = getTransactionHistory('')
    transHist = eval(transHist)
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
    result = json.dumps(result)
    print(result)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")

    # uvicorn main:app --reload
    # ngrok http 8000
