import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, date
from scipy.stats import norm
necessary_for_formula=["Strike Price","Time to Maturity(In Years)","Current Stock Price","Risk Free Interest Rate","Implied Volatility"]


i=1
while i==1:
    symbol=str(input("Please enter symbol: ")).upper()
    if len(symbol)>4:
        print("Invalid symbol, please try again")
    else:
        i==i+1
        print("This is your symbol",symbol)
        break
print("---------------------------------------------------------------------------------------------------------")
dat = yf.Ticker(symbol)

stockprice=dat.info['regularMarketPrice']

expiration = dat.options

expiration_array=pd.DataFrame(expiration)

print(expiration_array)
print("---------------------------------------------------------------------------------------------------------")
expiration_index = int(input("Pick a date using index number: "))
print("---------------------------------------------------------------------------------------------------------")
expdate = expiration_array.iloc[expiration_index, 0]

expdate = str(expdate)

while True:
    callorput=str(input("Call or Put Data? (C/P) ")).upper()
    if callorput=="C":
        chain = dat.option_chain(date=expdate).calls
        print("Calls:\n", chain.to_string())
        break
    if callorput == "P":
        chain = dat.option_chain(date=expdate).puts
        print("Puts:\n", chain.to_string())
        break
    else:
        print("Invalid input, try again")



chain_info = int(input("Pick a date using index number: "))

k =chain.iloc[chain_info, 2]
r=0.5 #change to get live data later
v=chain.iloc[chain_info, 10]
s=dat.info['regularMarketPrice']
current_date=date.today()
expiry_date = datetime.strptime(expdate, "%Y-%m-%d").date()
days_to_expiry = (expiry_date - current_date).days
t = days_to_expiry / 365
formulavalues=[k,t,s,r,v]
print("---------------------------------------------------------------------------------------------------------")
print("This is your chosen option:\n",chain.loc[chain_info])
print("---------------------------------------------------------------------------------------------------------")
for i in range(len(necessary_for_formula)) :
    print(necessary_for_formula[i],":",formulavalues[i])
print("---------------------------------------------------------------------------------------------------------")
d1= (np.log(s / k) + (r + 0.5 * v ** 2) * t) / (v * np.sqrt(t))
d2= d1 - v * np.sqrt(t)

if callorput=="C":
    price = s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
if callorput=="P":
    price = k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)


print(f"\nBlack-Scholes Price for", symbol ,",",k ,"strike expiring", expdate,":")
print(f" Option Price: ${price:.2f}")
