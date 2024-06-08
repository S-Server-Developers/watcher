import discord
from discord.ext import commands, tasks

import requests
from datetime import datetime

class watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watcher.start()
        self.message:discord.Message = None
        self.monitoring = False
    
    @tasks.loop(minutes=15)
    async def watcher(self):
        status = await self.bot.get_channel(1237023011975200768).fetch_message(1237029840377610314)
        count = await self.bot.get_channel(1237023011975200768).fetch_message(1237029925429706773)
        response = requests.get("https://earthquickly.com/discord/status_1.json")
        data = response.json()
        size = data['status']['size']
        embed = discord.Embed(title="EarthQuicklyの導入サーバー数", description=f"{size}サーバー\n更新:{discord.utils.format_dt(datetime.now())}", color=discord.Color.light_gray(), timestamp=datetime.now())
        embed.set_footer(text="この情報は15分ごとに更新されます。")
        await status.edit(embed=embed)
        if size[-2:] == '00':
            await count.edit(content=f":tada:祝！{size}サーバー！:tada:")
        else:
            return
    

    @commands.Cog.listener()
    async def on_presence_update(self, before, after: discord.Member):
        member:discord.User = self.bot.get_user(935855687400054814)
        shizengakari:discord.User = self.bot.get_user(1134778801671376907)
        guild = self.bot.get_guild(1148956059000651806)
        if after.guild != guild:
            return
        if after.id == member.id or after.id == shizengakari.id:
            if after.status == discord.Status.offline:
                if self.message is None:
                    embed = discord.Embed(title="Watcher", color=discord.Color.red(), timestamp=datetime.now())
                    embed.add_field(name=f"<a:down:1238112292802134047>Down {after.display_name} ({discord.utils.format_dt(datetime.now(), style='R')})", value=f"{after.display_name}がダウンしてしまいました！", inline=False)
                    embed.set_footer(text="更新日時")
                    self.message = await self.bot.get_channel(1236680579454603285).send(embed=embed)
                    return
                else:
                    return
            elif after.status != discord.Status.offline and after.status != discord.Status.online:
                if self.message:
                    if not self.monitoring:
                        embed = self.message.embeds[0]
                        embed.add_field(name=f"<a:possible:1238112280600903710>Monitoring {after.display_name} ({discord.utils.format_dt(datetime.now(), style='R')})", value="いつもとステータスが違う気がするので、オンライン<:online:1238112276125454407>になるまで監視中です。", inline=False)
                        embed.color = discord.Color.orange()
                        await self.message.edit(embed=embed)
                        self.monitoring = True
                        return
                    else:
                        return
                else:
                    return
            elif before.status != discord.status.online and after.status == discord.Status.online:
                if self.message:
                    embed = self.message.embeds[0]
                    embed.add_field(name=f"<a:stable:1238112294781718680>Up ({discord.utils.format_dt(datetime.now(), style='R')})", value=f"{after.display_name}が復活しました！")
                    embed.timestamp = datetime.now()
                    embed.color = discord.Color.green()
                    await self.message.edit(embed=embed)
                    self.message = None
                    self.monitoring = False
                    return
                else:
                    return
    
    async def cog_unload(self):
        self.watcher.stop()


async def setup(bot: commands.Bot):
    await bot.add_cog(watcher(bot))