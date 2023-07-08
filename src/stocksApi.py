import requests


class StockAPI:
    def __init__(self):
        self.headers = {
            "X-RapidAPI-Key": "c8c1fc7d27mshbd2bc611ad076c3p1679c1jsn049bf7c78ddd",
            "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com",
        }

    def stockById(self, symbol):
        result = ""
        url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbol}/financial-data"
        response = requests.get(url, headers=self.headers)
        if "error" in response.text:
            result = 'Error in API: '+ response.text
        else:
              result = response.json()
        return result
