import discord, random
from discord.ext import commands

class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    # Check the author's top role to prevent them from managing higher roles, except for the server owner.
    @staticmethod
    def hierarchy_check(ctx: commands.Context, role: discord.Role) -> bool:
        return ctx.author.top_role > role or ctx.author == ctx.guild.owner
    
    # Check the bot's top role to prevent it from managing higher roles.
    @staticmethod
    def bot_hierarchy_check(ctx: commands.Context, role: discord.Role) -> bool:
        return ctx.guild.me.top_role > role
        
    @commands.command(name="addrole")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, role: discord.Role, member: discord.Member):
        
        if member.get_role(role.id):
            await ctx.send(f"<@{member.id}> already has the {role.name} role.")
            return
        
        if not self.hierarchy_check(ctx, role):
            await ctx.send("You can't add a role higher than your highest role.")
            return
            
        if not self.bot_hierarchy_check(ctx, role):
            await ctx.send("I can't add a role higher than my highest role.")
            return
        
        try:
            await member.add_roles(role)
        except discord.Forbidden: # The bot may not have permission to manage roles.
            await ctx.send("Something went wrong. I may not have permission to manage roles.")
        else:
            await ctx.send(f"Successfully added the {role.name} role to {member.display_name}.")
            
    @commands.command(name="removerole")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, role: discord.Role, member: discord.Member):
        
        if member.get_role(role.id) is None:
            await ctx.send(f"{member.display_name} does not have the {role.name} role.")
            return
    
        if not self.hierarchy_check(ctx, role):
            await ctx.send("You can't remove a role higher than your highest role.")
            return
            
        if not self.bot_hierarchy_check(ctx, role):
            await ctx.send("I can't remove a role higher than my highest role.")
            return
        
        try:
            await member.remove_roles(role)
        except discord.Forbidden: # The bot may not have permission to manage roles.
            await ctx.send("Something went wrong. I may not have permission to manage roles.")
        else:
            await ctx.send(f"Successfully removed the {role.name} role from {member.display_name}.")
            
    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def editrole(self, ctx):
        pass
    
    @editrole.command(name="name")
    async def edit_role_name(self, ctx, role: discord.Role, name: str):
        
        if not self.hierarchy_check(ctx, role):
            await ctx.send("You can't edit a role higher than your highest role.")
            return
            
        if not self.bot_hierarchy_check(ctx, role):
            await ctx.send("I can't edit a role higher than my highest role.")
            return
        
        old_name = role.name
        try:
            await role.edit(name=name)
        except discord.Forbidden:
            await ctx.send("Something went wrong. I may not have permission to manage roles.")
        else:
            await ctx.send(f"Successfully changed the role name from {old_name} to {name}.")
            
    @editrole.command(name="color")
    async def edit_role_name(self, ctx, role: discord.Role, color: discord.Colour):
        
        if not self.hierarchy_check(ctx, role):
            await ctx.send("You can't edit a role higher than your highest role.")
            return
            
        if not self.bot_hierarchy_check(ctx, role):
            await ctx.send("I can't edit a role higher than my highest role.")
            return
        
        old_color = role.color
        try:
            await role.edit(color=color)
        except discord.Forbidden:
            await ctx.send("Something went wrong. I may not have permission to manage roles.")
        else:
            await ctx.send(f"Successfully changed the role color from {old_color} to {color}.")

        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin is loaded")
    
        
async def setup(bot):
    await bot.add_cog(Admin(bot))