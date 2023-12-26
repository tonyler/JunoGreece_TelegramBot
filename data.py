import requests

class Juno: 
    def __init__(self) -> None:
        self.price = get_price()
        self.cs = get_current_supply()
        self.mc = float(self.cs) * float(self.price) 
        self.inflation = get_inflation()
        self.apr = get_apr()

api = "https://api-juno-ia.cosmosia.notional.ventures"

def get_price() -> float:
    return requests.get('https://api-osmosis.imperator.co/tokens/v2/juno', timeout=30).json()[0]['price']

def get_inflation() -> float:
    res = requests.get(url=api+'/cosmos/mint/v1beta1/inflation',timeout=30).json()
    return float(res['inflation'])

def get_bonded_tokens() -> int:
    res = requests.get(url=api+'/cosmos/staking/v1beta1/pool',timeout=30).json()
    return int(res['pool']['bonded_tokens'])

def get_current_supply() -> int:
    res = requests.get(url=api+'/cosmos/bank/v1beta1/supply/by_denom?denom=ujuno', timeout=30).json()
    return float(res['amount']['amount'])/1000000

def get_apr() -> float:
    epoch_tokens = (119941194-get_current_supply())
    bonded_tokens = get_bonded_tokens()/1000000
    apr = (epoch_tokens/bonded_tokens)*100
    return (apr)
    
 

