import json
from numpy import poly
from web3 import Web3
import requests

#TEST API KEY
polygon_test_api = '48Q8C2GH74Y9KVJG1ETJAUZ2KND5K63ZED'
polygon_base_url = 'https://api.polygonscan.com/api'

polygon_node_url = 'https://rpc-mainnet.maticvigil.com/v1/4ac5fc1eea43fd27f0e7e3e0aada1cd6d7ca7c95'
web3 = Web3(Web3.HTTPProvider(polygon_node_url))
quickswap_factory_abi_file = open('Quickswap/FactoryABI.json')
quickswap_factory_abi = json.load(quickswap_factory_abi_file)
quickswap_factory_address = '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'

def getPairCount_UniswapV2Fork(address, abi):
    quickswap_factory_contract = web3.eth.contract(address=address, abi=abi)

    pair_count = quickswap_factory_contract.functions.allPairsLength().call()

    return pair_count

def getPairAddress_UniswapV2Fork(address, abi, id):
    quickswap_factory_contract = web3.eth.contract(address=address, abi=abi)

    pair_address = quickswap_factory_contract.functions.allPairs(id).call()

    return pair_address

def getContractABI(address, key, url):

    res = requests.get(url + '?module=contract&action=getabi&address=' + address + '&apikey=' + key)
    response = res.json()

    if 'Contract source code not verified' in response['result']:
        print('Contract source code not verified')
        return 'Contract source code not verified'
    else:
        return response['result']

def getPairInfo_UniswapV2Fork(address, abi):
    pair_contract = web3.eth.contract(address=address, abi=abi)

    token0 = pair_contract.functions.token0().call()
    token1 = pair_contract.functions.token1().call()
    
    return token0, token1

def getTokenInfo(address, url, key):
    abi = getContractABI(address, polygon_test_api, polygon_base_url)
    if abi == 'Contract source code not verified':
        return
    token_contract = web3.eth.contract(address=address, abi=abi)

    try:
        token_symbol = token_contract.functions.symbol().call()
    except:
        token_symbol = getTokenInfoByTransactions(address, url, key)

    print(token_symbol)

def getTokenInfoByTransactions(address, url, key):
    res = requests.get(url + '?module=account&action=tokentx&contractaddress=' + address + '&page=1&offset=1&startblock=0&endblock=99999999&sort=asc'+'&apikey=' + key)
    response = res.json()
    
    token_symbol = response['result'][0]['tokenSymbol']

    print(token_symbol)
    return token_symbol

    #https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174&address=0x6813ad11cca98e15ff181a257a3c2855d1eee69e&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken

    
    
if __name__ == "__main__":
    # pair_count = getPairCount_UniswapV2Fork(quickswap_factory_address,quickswap_factory_abi)
    
    for i in range(30, 32):
        address = getPairAddress_UniswapV2Fork(quickswap_factory_address, quickswap_factory_abi, i)
        print(address)
        abi = getContractABI(address, polygon_test_api, polygon_base_url)
        token0, token1 = getPairInfo_UniswapV2Fork(address, abi)

        print("Token0: " + token0)
        print("Token1: " + token1)

        getTokenInfo('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', polygon_base_url, polygon_test_api)








# # Prices

# ETH_AMOUNT = web3.toWei('1', 'Ether')
# daiAmount = exchange_contract.functions.getEthToTokenInputPrice(ETH_AMOUNT).call()
# print(daiAmount)
# bid_price = web3.toWei(daiAmount, 'Ether')
# daiAmount = exchange_contract.functions.getTokenToEthOutputPrice(ETH_AMOUNT).call()
# offer_price = web3.toWei(daiAmount, 'Ether')

# x = bid_price / 1000000000000000000

# print(x, offer_price)

# import json
# from web3 import Web3

# #this program queries for all of the uniswap pair addresses and their token supply

# infura_url = 'https://mainnet.infura.io/v3/89840781559f4078b6c06710f83ba796'
# web3 = Web3(Web3.HTTPProvider(infura_url))

# # uniswap_Factory
# factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
# factory_address = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
# factory_contract = web3.eth.contract(address=factory_address, abi=factory_abi)


# #returns a count of all the trading pairs on uniswap
# allPairsLength = exchange_contract.functions.allPairsLength().call()
# print(allPairsLength)

# abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

# contract = web3.eth.contract(address='0x12EDE161c702D1494612d19f05992f43aa6A26FB', abi=abi)
# symbol = contract.functions.token0().call()
# supply = contract.functions.totalSupply().call()
# print('0x12EDE161c702D1494612d19f05992f43aa6A26FB', supply, symbol)

# get the uniswap pair address for pricing
# for i in range(1, allPairsLength):
#     allPairs_address = factory_contract.functions.allPairs(i).call()
#     print(allPairs_address)
    # contract = web3.eth.contract(address=allPairs_address, abi=pairs_abi)
    # symbol = contract.functions.name().call()
    # supply = contract.functions.totalSupply().call()
    # print(allPairs_address, supply)