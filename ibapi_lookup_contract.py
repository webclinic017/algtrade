from ibapi.client import *
from ibapi.wrapper import *
import time
import pandas as pd
import threading

class TestApp(EClient, EWrapper):
  def __init__(self):
    EClient.__init__(self, self)
    self.orderId = 0
    self.contractDetails_df = pd.DataFrame(columns=["reqId", "symbol", "secType",  "conId", "exchange", "currency"])  
  
  def nextValidId(self, orderId):
    self.orderId = orderId
  
  def nextId(self):
    self.orderId += 1
    return self.orderId
   
  def error(self, reqId, errorCode, errorString, advancedOrderReject):
    print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, orderReject: {advancedOrderReject}")

  def contractDetails(self, reqId, contractDetails):
    attrs = vars(contractDetails)
    print("\n".join(f"{name}: {value}" for name,value in attrs.items()))
    self.contractDetails_df.loc[len(self.contractDetails_df)] = [reqId, contractDetails.contract.symbol, contractDetails.contract.secType, contractDetails.contract.conId, contractDetails.contract.exchange, contractDetails.contract.currency]  
    print(contractDetails.contract)

  def contractDetailsEnd(self, reqId):
    print("End of contract details")
    print(self.contractDetails_df)
    self.disconnect()
  
  def symbolSamples(self, reqId: int, contractDescriptions: ListOfContractDescription):
    print("Symbol Samples. Request Id: ", reqId)
    for contractDescription in contractDescriptions:
      derivSecTypes = ""
      for derivSecType in contractDescription.derivativeSecTypes:
        derivSecTypes += " "
        derivSecTypes += derivSecType
        print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
          "currency:%s, derivativeSecTypes:%s, description:%s, issuerId:%s" % (
          contractDescription.contract.conId,
          contractDescription.contract.symbol,
          contractDescription.contract.secType,
          contractDescription.contract.primaryExchange,
          contractDescription.contract.currency, derivSecTypes,
          contractDescription.contract.description,
          contractDescription.contract.issuerId))


  def securityDefinitionOptionParameter(self, reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
  
    print(f"Option chain exchange: {exchange} trading class: {tradingClass}, expirations: {expirations}, strikes: {strikes}")

app = TestApp()
app.connect("127.0.0.1", 7497, 0)
threading.Thread(target=app.run).start()
time.sleep(1)

mycontract = Contract()
# Stock
# mycontract.symbol = "AAPL"
# mycontract.secType = "STK"
# mycontract.currency = "USD"
# mycontract.exchange = "SMART"
# mycontract.primaryExchange = "NASDAQ"

# Future
#mycontract.symbol = "ES"
#mycontract.secType = "FUT"
#mycontract.currency = "USD"
#mycontract.exchange = "CME"
#mycontract.lastTradeDateOrContractMonth = 202503

# Option
mycontract.symbol = "IBM"
mycontract.secType = "OPT"
underConId = 8314
mycontract.currency = "USD"
mycontract.exchange = "SMART"
mycontract.lastTradeDateOrContractMonth = 20250221
#mycontract.right = "P"
#mycontract.tradingClass = "SPXW"
#mycontract.strike = 6100

app.reqContractDetails(app.nextId(), mycontract)
#print(f"Contract details: {app.contractDetails_df}")

#app.disconnect()