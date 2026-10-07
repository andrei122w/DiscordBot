import discord
import os
from discord.ext import commands

class AutoMod(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        channel_id = os.getenv("REACTION_LOG_CHANNEL_ID")
        try:
            self.reaction_log_channel_id = int(channel_id) if channel_id else None
        except ValueError as error:
            raise ValueError("REACTION_LOG_CHANNEL_ID must be a numeric channel ID.") from error
    

    @staticmethod
    async def message_filter(message : discord.Message):
        word_list = message.content.split()
        
        # Check each word.
        for word in word_list:
            if word.lower() == "test":
                await message.delete()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("AutoMod is loaded")
        
    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        
        # Prevent the bot from responding to itself.
        if message.author == self.bot.user:
            return
        
        # Ignore commands.
        if message.content.startswith(self.bot.command_prefix):  
            return
        
        await self.message_filter(message)
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.message_filter(after)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.reaction_log_channel_id is None:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        
        bot_channel = self.bot.get_channel(self.reaction_log_channel_id)
        if bot_channel is None:
            bot_channel = await self.bot.fetch_channel(self.reaction_log_channel_id)

        if bot_channel:
            await bot_channel.send(f"<@{user.id}> reacted to the message '{message.content}' in channel <#{channel.id}>", silent = True)
        
        print(f"{user} reacted to the message {message.content} in channel {channel.name}")
        
                
async def setup(bot):
    await bot.add_cog(AutoMod(bot))