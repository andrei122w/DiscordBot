import discord, os
from discord.ext import commands

class Manager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Manager is loaded")
        
    # Unload cogs.
    @commands.command(name="unload")
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        message = await ctx.send("Unloading...")
        await message.delete()
        
        try:
            await self.bot.unload_extension(f"cogs.{cog.capitalize()}")
            await ctx.send(f"{cog} has been unloaded.")
        except commands.ExtensionNotLoaded:  # The extension is already unloaded.
            await ctx.send(f"{cog} is not loaded.")
        except commands.ExtensionNotFound:   # The extension was not found.
            await ctx.send(f"Error: {cog} was not found.")
        except Exception as e:
            await ctx.send(f"Error: unloading {cog}, {e}")
            
    # Load cogs.
    @commands.command(name="load")
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        message = await ctx.send("Loading...")
        await message.delete()
        
        try:
            await self.bot.load_extension(f"cogs.{cog.capitalize()}")
            await ctx.send(f"{cog} has been loaded.")
        except commands.ExtensionAlreadyLoaded: # The extension is already loaded.
            await ctx.send(f"{cog} is already loaded.")
        except commands.ExtensionNotFound:  # The extension was not found.
            await ctx.send(f"Error: {cog} was not found.")
        except Exception as e:
            await ctx.send(f"Error loading {cog}: {e}")
            
     # Reload cogs.
    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        message = await ctx.send("Reloading...")
        await message.delete()
        
        try:
            await self.bot.reload_extension(f"cogs.{cog.capitalize()}")
            await ctx.send(f"{cog} has been reloaded.")
        except commands.ExtensionNotLoaded: # The extension must be loaded before it can be reloaded.
            await ctx.send(f"{cog} is not loaded.")
        except commands.ExtensionNotFound:  # The extension was not found.
            await ctx.send(f"Error: {cog} was not found.")
        except Exception as e:
            await ctx.send(f"Error reloading {cog}: {e}")
            
    @commands.command(name="loadedcogs")
    @commands.is_owner()
    async def loaded_cogs(self, ctx):
        cogs = list(ctx.bot.cogs.keys())
        
        if cogs is None:
            owner = await ctx.bot.fetch_user(ctx.bot.owner_id)
            await ctx.send(f"Ce ai făcut de s-a stricat tot? {owner.mention}")
        else:
            await ctx.reply(f"Available cogs: {', '.join(cogs)}")
            
    @commands.command(name="allcogs")
    @commands.is_owner()
    async def all_cogs(self, ctx):  
        cogs = [] 
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cogs.append(filename)
        await ctx.send(cogs)
            
    @commands.command(name="stop")
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send("Shutting down.")
        await ctx.bot.close()
        
        
async def setup(bot):
    await bot.add_cog(Manager(bot))