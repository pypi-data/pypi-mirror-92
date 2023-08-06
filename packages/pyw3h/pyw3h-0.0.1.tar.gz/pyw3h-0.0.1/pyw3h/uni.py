import pandas as pd
from dotenv import load_dotenv
import json
from tqdm import trange
from datetime import datetime
from web3 import Web3
import time
import requests
import os


class Uniswap:
    load_dotenv()
    WEB3_PROVIDER = os.getenv( "WEB3_HTTP_URI" )

    def __init__(self):
        self.w3 = Web3( Web3.HTTPProvider( self.WEB3_PROVIDER ) )
        self.factory = Web3.toChecksumAddress( "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f" )

    def get_pair_prices(self, pair, block=None, step=None):

        pair = Web3.toChecksumAddress( pair )

        with open( "UniPair.json", "r" ) as f:
            abi = f.read()
        pair_contract = self.w3.eth.contract( abi=abi, address=pair )

        with open( "ERC20.json", "r" ) as f:
            abi = f.read()

        token0_contract = self.w3.eth.contract( abi=abi, address=pair_contract.functions.token0().call() )
        token1_contract = self.w3.eth.contract( abi=abi, address=pair_contract.functions.token1().call() )

        token0_decimals = int( token0_contract.functions.decimals().call() )
        token1_decimals = int( token1_contract.functions.decimals().call() )

        if not block:
            reserves = pair_contract.functions.getReserves().call()
            reserve0 = int( reserves[0] ) / 10 ** token0_decimals
            reserve1 = int( reserves[1] ) / 10 ** token1_decimals
            return reserve1 / reserve0
        else:
            prices_list = []
            max_block = self.w3.eth.blockNumber
            min_block = max_block - block
            for i in trange( min_block, max_block, step ):
                if i > max_block:
                    break

                b = min( i, max_block )
                reserves = pair_contract.functions.getReserves().call( block_identifier=b )
                reserve0 = int( reserves[0] ) / 10 ** token0_decimals
                reserve1 = int( reserves[1] ) / 10 ** token1_decimals
                date = datetime.utcfromtimestamp( float( reserves[2] ) )
                price = reserve1 / reserve0
                prices_list.append( {"date": date, "price": price} )

            df = pd.DataFrame( prices_list )
            return df

    def get_pair(self, token0, token1):
        with open( "UniFactory.json", "r" ) as f:
            abi = json.load( f )

        factory_contract = self.w3.eth.contract( abi=abi, address=self.factory )
        token0 = Web3.toChecksumAddress( token0 )
        token1 = Web3.toChecksumAddress( token1 )
        pair = factory_contract.functions.getPair( token0, token1 ).call()
        return Web3.toChecksumAddress( pair )

    @staticmethod
    def token_info(data, decimals=False):
        """
        :param decimals:
        :param data: either symbol (dont'care for upper/lowercase, or address (checks for starting with 0x and decides)
        :return: list of [symbol or address, decimals]
        """
        url = "https://tokens.coingecko.com/uniswap/all.json"
        r = None

        while True:
            try:
                r = requests.get( url ).json()
            except requests.exceptions.Timeout:
                time.sleep( 5 )
                continue
            except requests.exceptions.TooManyRedirects as e:
                print( f"URL cannot be reached. {e}" )
                break
            except requests.exceptions.RequestException as e:
                raise SystemExit( e )
            else:
                break

        r = pd.DataFrame( r["tokens"] )

        if data.startswith( "0x" ):
            ret = r.loc[r["address"] == data, ["symbol", "decimals"]]
            ret.reset_index( drop=True, inplace=True )
            return ret.loc[0].symbol if decimals is False else ret.loc[0].decimals

        else:
            data = str( data ).upper()
            ret = r.loc[r["symbol"] == data, ["address", "decimals"]]
            ret.reset_index( drop=True, inplace=True )
            return ret.loc[0].address if decimals is False else ret.loc[0].decimals


if __name__ == '__main__':
    while True:
        choice = int( input( '1: Symbol/Address -> Address/Symbol, 2: Token0/Token1 --> Pair, 3: Pair --> Price, '
                             '0: Exit ' ) )
        if choice == 1:
            u = Uniswap()
            data = str( input( 'Symbol/Address? ' ) )
            print(u.token_info(data))
        elif choice == 2:
            u = Uniswap()
            token0 = str(input('Token 0: ')).lower()
            token1 = str(input('Token 1: ')).lower()
            print(u.get_pair(token0, token1))
        elif choice == 3:
            u = Uniswap()
            pair = str(input('Pair: '))
            print(u.get_pair_prices(pair))
        elif choice == 0:
            break
