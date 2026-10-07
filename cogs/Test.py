import discord, random
from discord.ext import commands

class test(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("TestCog is loaded")
    
        
    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("Success!")
        
    @commands.command(name="ruleta")
    async def pick_random(self, ctx, *members: discord.Member):
        if not members:
            await ctx.send("Introdu cel puțin o persoană.")
        else:
            random_member = random.choice(members)
            await ctx.send(random_member.mention)
        
async def setup(bot):
    await bot.add_cog(test(bot))