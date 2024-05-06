import discord
from discord.ext import commands, tasks

import requests
from datetime import datetime

class watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watcher.start()
        self.message:discord.Message = None
    
    @tasks.loop(minutes=15)
    async def watcher(self):
        status = await self.bot.get_channel(1237023011975200768).fetch_message(1237029840377610314)
        count = await self.bot.get_channel(1237023011975200768).fetch_message(1237029925429706773)
        response = requests.get("https://earthquickly.com/discord/status_1.json")
        data = response.json()
        size = data['status']['size']
        embed = discord.Embed(title="EarthQuicklyの導入サーバー数", description=f"{size}サーバー\n更新:{discord.utils.format_dt(datetime.now())}", color=discord.Color.light_gray(), timestamp=datetime.now())
        await status.edit(embed=embed)
        if size[-2:] == '00':
            await count.edit(content=f":tada:祝！{size}サーバー！:tada:")
        else:
            return
    

    @commands.Cog.listener()
    async def on_presence_update(self, before, after: discord.Member):
        if after.id == '935855687400054814':
            if after.status.offline:
                embed = discord.Embed(title="ダウン通知", description="Earthquickly Botがダウンしてしまいました！", color=discord.Color.red())
                self.message = await self.bot.get_channel(1236680579454603285).send(embed=embed)
            else:
                if self.message:
                    embed = discord.Embed(title="アップ通知", description="Earthquickly Botが復活しました！", color=discord.Color.green())
                    self.message.edit(embed=embed)
                    self.message = None
                else:
                    return

async def setup(bot: commands.Bot):
    await bot.add_cog(watcher(bot))