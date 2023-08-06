# -*- coding: utf-8 -*-

import hashlib
import hmac
import time
from urllib import parse

import requests


class API:

    def __init__(self, api_key=None, api_secret=None):
        self.url = "https://api.bitflyer.com"
        self.api_key = api_key
        self.api_secret = api_secret

    def markets(self):
        """Market List - マーケットの一覧"""
        return self.public_get(path="/v1/getmarkets")

    def board(self, params={"product_code": "BTC_JPY"}):
        """Order Book - 板情報

        Parameters:
            product_code: Specifies a product_code or alias, as obtained from the Market List.
        """
        return self.public_get(path="/v1/getboard", params=params)

    def ticker(self, params={"product_code": "BTC_JPY"}):
        """Ticker - Ticker

        Parameters:
            product_code: Specifies a product_code or alias, as obtained from the Market List.
        """
        return self.public_get(path="/v1/getticker", params=params)

    def executions(self, params={"product_code": "BTC_JPY"}):
        """Execution History - 約定履歴

        Parameters:
            product_code: Specifies a product_code or alias, as obtained from the Market List.
            count: Specifies the number of results. If this is omitted, the value will be 100.
            before: Obtains data having an id lower than the value specified for this parameter.
            after: Obtains data having an id higher than the value specified for this parameter.
        """
        return self.public_get(path="/v1/getexecutions", params=params)

    def boardstate(self):
        """Orderbook status - 板の状態

        Parameters:
            product_code: Specifies a product_code or alias, as obtained from the Market List.
        """
        return self.public_get(path="/v1/getboardstate")

    def health(self):
        """Exchange status - 取引所の状態

        Parameters:
            product_code: Specifies a product_code or alias, as obtained from the Market List.
        """
        return self.public_get(path="/v1/gethealth")

    def chats(self):
        """Chat - チャット

        Parameter:
            from_date: This accesses a list of any new messages after this date. Defaults to the previous 5 days if left blank.
        """
        return self.public_get(path="/v1/getchats")

    def getpermissions(self):
        """Get API Key Permissions - API キーの権限を取得"""
        return self.private_get("/v1/me/getpermissions")

    def getbalance(self):
        """Get Account Asset Balance - 資産残高を取得"""
        return self.private_get("/v1/me/getbalance")

    def getcollateral(self):
        """Get Margin Status - 証拠金の状態を取得"""
        return self.private_get("/v1/me/getcollateral")

    def getcollateralaccounts(self):
        """Obtain the details of your margin deposits for each currency - 通貨別の証拠金の数量を取得"""
        return self.private_get("/v1/me/getcollateralaccounts")

    def getaddresses(self):
        """Get Crypto Assets Deposit Addresses - 預入用アドレス取得"""
        return self.private_get("/v1/me/getaddresses")

    def getcoinins(self, **kwargs):
        """Get Crypto Assets Deposit History - 仮想通貨預入履歴"""
        return self.private_get("/v1/me/getcoinins", **kwargs)

    def getcoinouts(self, **kwargs):
        """Get Crypto Assets Transaction History - 仮想通貨送付履歴"""
        return self.private_get("/v1/me/getcoinouts", **kwargs)

    def getbankaccounts(self):
        """Get Summary of Bank Accounts - 銀行口座一覧取得"""
        return self.private_get("/v1/me/getbankaccounts")

    def getdeposits(self, **kwargs):
        """Get Cash Deposits - 入金履歴"""
        return self.private_get("/v1/me/getdeposits", **kwargs)

    def withdraw(self, **kwargs):
        """Withdrawing Funds - 出金"""
        return self.post("/v1/me/withdraw", **kwargs)

    def getwithdrawals(self):
        """Get Deposit Cancellation History - 出金履歴"""
        return self.private_get("/v1/me/getwithdrawals")

    def sendchildorder(self, **kwargs):
        """Send a New Order - 新規注文を出す"""
        return self.post("/v1/me/sendchildorder", **kwargs)

    def cancelchildorder(self, **kwargs):
        """Cancel Order - 注文をキャンセルする"""
        return self.post("/v1/me/cancelchildorder", **kwargs)

    def sendparentorder(self, **kwargs):
        """Submit New Parent Order (Special order) - 新規の親注文を出す（特殊注文）"""
        return self.post("/v1/me/sendparentorder", **kwargs)

    def cancelparentorder(self, **kwargs):
        """Cancel parent order - 親注文をキャンセルする"""
        return self.post("/v1/me/cancelparentorder", **kwargs)

    def cancelallchildorders(self, **kwargs):
        """Cancel All Orders - すべての注文をキャンセルする"""
        return self.post("/v1/me/cancelallchildorders", **kwargs)

    def getchildorders(self, **kwargs):
        """List Orders - 注文の一覧を取得"""
        return self.private_get("/v1/me/getchildorders", **kwargs)

    def getparentorders(self, **kwargs):
        """List Parent Orders - 親注文の一覧を取得"""
        return self.private_get("/v1/me/getparentorders", **kwargs)

    def getparentorder(self, **kwargs):
        """Get Parent Order Details - 親注文の詳細を取得"""
        return self.private_get("/v1/me/getparentorder", **kwargs)

    def getexecutions(self, **kwargs):
        """List Executions - 約定の一覧を取得"""
        return self.private_get("/v1/me/getexecutions", **kwargs)

    def getbalancehistory(self, **kwargs):
        """List Balance History - 残高履歴を取得"""
        return self.private_get("/v1/me/getbalancehistory", **kwargs)

    def getpositions(self, **kwargs):
        """Get Open Interest Summary - 建玉の一覧を取得"""
        return self.private_get("/v1/me/getpositions", **kwargs)

    def getcollateralhistory(self, **kwargs):
        """Get Margin Change History - 証拠金の変動履歴を取得"""
        return self.private_get("/v1/me/getcollateralhistory", **kwargs)

    def gettradingcommission(self, params={"product_code": "BTC_JPY"}):
        """Get Trading Commission - 取引手数料を取得"""
        return self.private_get("/v1/me/gettradingcommission", params)

    def public_get(self, path, params=None):
        response = requests.get(self.url + path, params=params)
        
        return API.process_response(response)

    def private_get(self, path, params=None):
        url = self.url + path
        if params:
            path += "?" + parse.urlencode(params)
        header = self.get_header("GET", path)

        try:
            with requests.session() as s:
                s.headers.update(header)
                response = s.get(url, params=params)
        except requests.RequestException as e:
            raise e
        
        return API.process_response(response)

    def post(self, path, **kwargs):
        url = self.url + path
        data = str(kwargs)
        header = self.get_header("POST", path, data)

        try:
            with requests.Session() as s:
                s.headers.update(header)
                response = s.post(url, data=data)
        except requests.RequestException as e:
            raise e

        return API.process_response(response)

    def get_header(self, method, path, data=None):
        timestamp = API.get_nonce()
        text = timestamp + method + path
        if data:
            text += data
        sign = self.get_sign(text)

        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-SIGN": sign,
            "Content-Type": "application/json",
        }

    def get_sign(self, text):
        return hmac.new(
            self.api_secret.encode("utf-8"), text.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    @staticmethod
    def get_nonce():
        return str(int(time.time() * 1000000))

    @staticmethod
    def process_response(response):
        result = {"status_code": response.status_code}
        if len(response.content) > 0:
            result["content"] = response.json()

        return result
