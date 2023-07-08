import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()

# config = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'database': os.getenv('DB_DATABASE'),
#     'raise_on_warnings': True
# }


class StockDB:
    def __init__(self,):
        self.config = {
            'user': 'root',
            'password': 'password@321',
            'host': 'localhost',
            'database': 'stockbot',
            'raise_on_warnings': True
        }
        self.cnx = None

    def openConnection(self):
        self.cnx = mysql.connector.connect(**self.config)

    def closeConnection(self):
        if self.cnx is not None:
            self.cnx.close()
            self.cnx = None

    # def stockPriceByName(self, symbol):
    #     self.openConnection()
    #     cursor = self.cnx.cursor()
    #     query = "SELECT price FROM stockinfo where stockSymbol = %s"
    #     cursor.execute(query, (symbol))
    #     data = cursor.fetchall()
    #     cursor.close()
    #     self.closeConnection()
    #     return data

    def stockListById(self, customerId):
        self.openConnection()
        cursor = self.cnx.cursor()
        query = "SELECT company, quantity, transactionType from stockinfo where customerId = %s"
        cursor.execute(query, [customerId])
        data = cursor.fetchall()
        cursor.close()
        self.closeConnection()
        return data

    def transactionHitory(self,):
        self.openConnection()
        cursor = self.cnx.cursor()
        query = "SELECT company, stockSymbol, quantity, transactionType, transactionDate, price from stockinfo"
        cursor.execute(query,)
        data = cursor.fetchall()
        cursor.close()
        self.closeConnection()
        return data
