import requests

potential_apis = ("https://juno-api.polkachu.com",
                    "https://api-juno-ia.cosmosia.notional.ventures",
                    "https://lcd-juno.itastakers.com",
                    "https://rest-juno.goldenratiostaking.net",
                    "https://juno-rest.publicnode.com")
class Juno: 
    def __init__(self) -> None:
        self.api, self.chain_is_live = get_api()
        if self.chain_is_live:
            self.price = get_price()
            self.cs = get_current_supply(self.api)
            self.mc = float(self.cs) * float(self.price) 
            self.inflation = get_inflation(self.api)
            self.bonded_tokens = get_bonded_tokens(self.api)
            self.apr = get_apr(self.cs,self.bonded_tokens)

def get_api(): 
    for api in potential_apis: 
        try:
            response = requests.get(api)
        except: 
            pass
        if response.status_code == 200: 
            print (f"API used: {api}")
            return api,True
    return "Ίσως να υπάρχει πρόβλημα με την αλυσίδα! 😳",False

def get_price() -> float:
    return requests.get('https://api-osmosis.imperator.co/tokens/v2/juno', timeout=30).json()[0]['price']

def get_inflation(api) -> float:
    res = requests.get(url=f'{api}/cosmos/mint/v1beta1/inflation',timeout=30).json()
    return float(res['inflation'])

def get_bonded_tokens(api) -> int:
    res = requests.get(url=f'{api}/cosmos/staking/v1beta1/pool',timeout=30).json()
    return int(res['pool']['bonded_tokens'])

def get_current_supply(api) -> int:
    res = requests.get(url= f"{api}/cosmos/bank/v1beta1/supply/by_denom?denom=ujuno", timeout=30).json()
    return float(res['amount']['amount'])/1000000

def get_apr(current_supply,bonded_tokens) -> float:
    epoch_tokens = (119941194-current_supply)
    bonded_tokens = bonded_tokens/1000000 
    apr = epoch_tokens/bonded_tokens
    return (apr)
    
 

