import discord
import requests
import json
from discord.ext import commands

class Coin_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dogecoin'])
    async def doge(ctx):
        b_api = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=DOGEUSDT')
        b_data = b_api.json()
        symbol = b_data['symbol']
        price_change = b_data['priceChange']
        WeightedAvg = b_data['weightedAvgPrice']
        prevClose = b_data['prevClosePrice']
        lastprice = b_data['lastPrice']
        lastbid = b_data['bidPrice']
        open_p = b_data['openPrice']
        high = b_data['highPrice']
        low = b_data['lowPrice']
        volume = b_data['volume']
        embed=discord.Embed(title="Dogecoin 24h ticker", description="Dogecoin values from Binance")
        embed.add_field(name="DOGE_USDT", value=f"```\nSymbol: {symbol}\n\nPrices\n\n   Weighted avg: ${WeightedAvg:.8}\n   Previous Close: ${prevClose:.8}\n   Last: ${lastprice:.8}\n   Open: ${open_p:.8}\n   High: ${high:.8}\n   Low: ${low:.8}\n\nVolume: {volume}\n```", inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['bitcoin'])
    async def btc(ctx):
        b_api = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT')
        b_data = b_api.json()
        symbol = b_data['symbol']
        price_change = b_data['priceChange']
        WeightedAvg = b_data['weightedAvgPrice']
        prevClose = b_data['prevClosePrice']
        lastprice = b_data['lastPrice']
        lastbid = b_data['bidPrice']
        open_p = b_data['openPrice']
        high = b_data['highPrice']
        low = b_data['lowPrice']
        volume = b_data['volume']
        embed=discord.Embed(title="Bitcoin 24h ticker", description="Bitcoin values from Binance")
        embed.add_field(name="BTC_USDT", value=f"```\nSymbol: {symbol}\n\nPrices\n\n   Weighted avg: ${WeightedAvg:.8}\n   Previous Close: ${prevClose:.8}\n   Last: ${lastprice:.8}\n   Open: ${open_p:.8}\n   High: ${high:.8}\n   Low: ${low:.8}\n\nVolume: {volume}\n```", inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Coin_commands(bot))