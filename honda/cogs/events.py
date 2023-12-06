import discord, datetime, asyncio, aiosqlite, traceback, logging
from discord.ext import commands, tasks
from backend.classes import Colors, Emojis

def seconds_to_dhms(time):
    seconds_to_minute   = 60
    seconds_to_hour     = 60 * seconds_to_minute
    seconds_to_day      = 24 * seconds_to_hour

    days    =   time // seconds_to_day
    time    %=  seconds_to_day

    hours   =   time // seconds_to_hour
    time    %=  seconds_to_hour

    minutes =   time // seconds_to_minute
    time    %=  seconds_to_minute

    seconds = time
    return ("%d days, %d hours, %d minutes, %d seconds" % (days, hours, minutes, seconds))

async def noperms(self, ctx, permission):
    e = discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: you are missing permission `{permission}`")
    await sendmsg(self, ctx, None, e, None, None, None)

def blacklist(): 
        async def predicate(ctx): 
            if ctx.guild is None:
             return False
            async with ctx.bot.db.cursor() as cursor:
                await cursor.execute("SELECT * FROM nodata WHERE user = {}".format(ctx.author.id))
                check = await cursor.fetchone()
                if check is not None: 
                   await ctx.reply#(embed=discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} you are blacklisted, join in viliecore to find more about it. https://viliebot.com/"), mention_author=False)
                return check is None
        return commands.check(predicate)   
        
async def sendmsgg(self, ctx, content, embed, view, file, allowed_mentions, delete_after): 
    if ctx.guild is None: return
    try:
       await ctx.reply(content=content, embed=embed, view=view, file=file, allowed_mentions=allowed_mentions, mention_author=False, delete_after=delete_after)
    except:
        await ctx.send(content=content, embed=embed, view=view, file=file, allowed_mentions=allowed_mentions, delete_after=delete_after) 
        
async def sendmsg(self, ctx, content, embed, view, file, allowed_mentions): 
    if ctx.guild is None: return
    try:
       await ctx.reply(content=content, embed=embed, view=view, file=file, allowed_mentions=allowed_mentions, mention_author=True)
    except:
        await ctx.send(content=content, embed=embed, view=view, file=file, allowed_mentions=allowed_mentions) 

async def commandhelp(self, ctx, cmd):
    prefixes = []
    for l in set(p for p in await self.bot.command_prefix(self.bot, ctx.message)):
      prefixes.append(l)
    try:
       command = self.bot.get_command(cmd)
       if command.usage is None:
        usage = ""
       else:
        usage = command.usage 

       embed = discord.Embed(color=0x2B2D31, title=command, description=command.help)
       embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
       embed.add_field(name="category", value=command.description)
       if command.brief:
        embed.add_field(name="commands", value=command.brief, inline=False)
       embed.add_field(name="usage", value=f"```{prefixes[0]}{cmd} {usage}```", inline=False)
       embed.add_field(name="aliases", value=', '.join(map(str, command.aliases)) or "none")
       embed.set_footer(text="honda", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
       await ctx.reply(embed=embed, mention_author=False)
    except:
       await ctx.reply(f"command `{cmd}` not found", mention_author=False)


class Events(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot 
        self.blacklisted = [1103187356934230037, 976975317468061746, 1108686885494202511, 1112981008166428742, 797458672225091594, 1093247033164431471, 1009935254414438541]

    #@commands.Cog.listener()
    #async def on_ready(self): 
    #  online = "<:on:1072888106296037417>"
     # log = self.bot.get_channel(1097943648060051536)
      #embed = discord.Embed(color=0x2B2D31, description=f"{online} **{self.bot.user.name}** is back up! serving `{len(self.bot.guilds)}` gulids with about `{len(set(self.bot.get_all_members()))}` users at `{round(self.bot.latency * 1000)}ms`", timestamp=datetime.datetime.now())
      #await log.send(embed=embed)
        
    @commands.Cog.listener('on_guild_join')
    async def joinmsg(self, guild: discord.Guild):
        channel = self.bot.get_channel(1178067765035270224)
        channel1 = guild.text_channels[0]
        invite = await channel1.create_invite(unique=True)
        edm = discord.Embed(color=0x2f3136, description="i have left your server because it has less than 1 members", timestamp=datetime.datetime.now())
        edm.set_footer(text="honda", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        embed = discord.Embed(color=0x2f3136, description=f"joined **{guild.name}** (`{guild.id}`) owned by {guild.owner} ({guild.member_count})", timestamp=datetime.datetime.now())
        embed.set_footer(text="?", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        msg = await channel.send(embed=embed, content=f"inv: {invite}")
        #await msg.add_reaction("<:check:1126571720816468129>")
        if guild.member_count < 1:
          for member in guild.members:
            if member.id == guild.owner_id:
             dm_channel = await member.create_dm()
             await dm_channel.send(embed=edm)
             await guild.leave()

    @commands.Cog.listener('on_guild_join')
    async def hii_events(self, guild: discord.Guild):
        e = discord.Embed(title=f"joined cute server called {guild.name}", description=" ", color=Colors.default)
        e.add_field(name=" ",value="Hey I'm verified bot with 100+ commands, autopost features, vanity, music and trusted by 300+ servers. Elevate your Discord experience now! <:sparkles:1130845524522704918>\n\nMy prefixes are **/slash** or **@mention**\nIf you need help or additional help join our **support server** and open ticket in <#1178067746181894249> <:earlysupporter:1152567924662468619>", inline=False) 
        e.add_field(name=" ",value="<:fire:1129806609099530300> **vanity set /hondabot", inline=False)
        e.add_field(name=" ", value="<:warning:1126572583442206820> **please read our** [tos](https://www.termsfeed.com/live/a388c8ac-e21f-49b9-b1d6-7e8aa660cf53) **and** [privacy policy](https://www.privacypolicygenerator.info/live.php?token=yzAy72GYmCK91hjTi2ePqX9iPn1t3wBE) **carefully!**")
        button1 = discord.ui.Button(label="vote", style=discord.ButtonStyle.url, url="https://top.gg/bot/")
        button2 = discord.ui.Button(label="support", style=discord.ButtonStyle.url, url="https://discord.gg/hondabot")
        button3 = discord.ui.Button(label="invite", style=discord.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1090979901483528242&permissions=8&scope=bot")
        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        if guild.owner_id in self.blacklisted:
            await guild.leave()
        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    return await channel.send(embed=e, view=view, allowed_mentions=discord.AllowedMentions(users=True), content=f"hey <@{guild.owner.id}> <:heart:1130845539852877834>")
                await asyncio.sleep(10)
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        return await channel.send(embed=e, view=view, allowed_mentions=discord.AllowedMentions(users=True), content=f"hey <@{guild.owner.id}> if you're enjoying honda, please consider leaving a review on Top.gg!\nhttps://top.gg/bot/1094942437820076083#reviews\nIf you need help setting the bot please join our support server https://discord.gg/U6yhf64DET >> <#1125077059404845126>")

                       

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
      gays = self.bot.get_channel(1178067763823136969) 
      embed1 = discord.Embed(color=0x2f3136, description=f"<:repeatbutton:1129817608770818068> **loading informations**")
      embed = discord.Embed(color=0x2f3136, description=f"{ctx.author} (`{ctx.author.id}`) - {ctx.guild} (`{ctx.guild.id}`) - `{ctx.command}`", timestamp=datetime.datetime.now())
      embed.set_footer(text="honda", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
      msg = await gays.send(embed=embed)
      #await msg.add_reaction("1??") #<a:w_w:1103337013656174652>
      #await asyncio.sleep(1.5)
      #await msg.edit(embed=embed) 
            
    @commands.Cog.listener('on_guild_remove')
    async def leavemsg(self, guild: discord.Guild):
      channel4321 = self.bot.get_channel(1178067765035270224) 
      embed = discord.Embed(color=0x2B2D31, description=f"left **{guild.name}** (`{guild.id}`) owned by {guild.owner} ({guild.member_count})")
      embed.set_footer(text="?", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
      await channel4321.send(embed=embed) 

    @commands.Cog.listener('on_guild_remove')
    async def leave_event_use(self, guild: discord.Guild):
      await self.bot.db.execute(f"DELETE FROM prefixes WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM female WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM male WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM anime WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM banner WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM random WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM fgifs WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM mgifs WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM agifs WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM automeme WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM match WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM autocar WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM guns WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM faceless WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM autobody WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM autoshoes WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM jewellry WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM aesthetic WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM cartoon WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM drill WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM hellokitty WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM money WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM smoking WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM animals WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM soft WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM quote WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM couplesgif WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM couplespfp WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM kpop WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM edgy WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM besties WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM core WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM autonsfw WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM welcome WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM restore WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM goodbye WHERE guild = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM joindm WHERE guild = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM voicemaster WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM pingonjoin WHERE guild_id = {guild.id}")
      await self.bot.db.execute(f"DELETE FROM imageonly WHERE guild = {guild.id}")
      await self.bot.db.commit()
      channel = self.bot.get_channel(1178067740968374303)
      msg = await channel.send(f"i left {guild.name} ({guild.id}) owned by {guild.owner} membercount is {guild.member_count} ppl and the database has been cleared")
      await msg.add_reaction("<:check:1126571720816468129>")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild: return
        if message.author.bot: return 	
        if message.content == f"<@{self.bot.user.id}>":           
            prefixes = []
            for l in set(p for p in await self.bot.command_prefix(self.bot, message)):
             prefixes.append(l)
            await message.reply(content="hai :3 " + "\nprefix:" + " ".join(f"`{g}`" for g in prefixes))      
        async with self.bot.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM seen WHERE guild_id = {} AND user_id = {}".format(message.guild.id, message.author.id))
          check = await cursor.fetchone()
          if check is None: 
            await cursor.execute("INSERT INTO seen VALUES (?,?,?)", (message.guild.id, message.author.id, int(datetime.datetime.now().timestamp())))
            await self.bot.db.commit()
          elif check is not None: 
           try: 
            ts = int(datetime.datetime.now().timestamp())
            sql = ("UPDATE seen SET time = ? WHERE guild_id = ? AND user_id = ?")
            val = (ts, message.guild.id, message.author.id)
            await cursor.execute(sql, val)
            await self.bot.db.commit()  
           except Exception as e: print(e)  
          
    @commands.Cog.listener()
    async def on_message_edit(self, before, after): 
        await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error): 
        if isinstance(error,commands.errors.CommandNotFound): return
        elif isinstance(error, commands.errors.CheckFailure) : return
        else:
            try:
                await ctx.reply(embed=discord.Embed(color=Colors.yellow, description=f"{Emojis.warning} {ctx.author.mention}: {error}"),mention_author=True)
            except: 
                pass
 

    @commands.Cog.listener('on_guild_join')
    async def join_gg_shit(self, guild: discord.Guild):
        owo = self.bot.get_channel(1130527580924153966)
        channel = guild.text_channels[0]
        invite = await channel.create_invite(unique=True)
        edm = discord.Embed(color=0x2f3136, description=f"Congratulations! **{guild.name}** has more than **120** members **({guild.member_count})** and it has been featured in our support server in the channel <#117806774618189424>")
        edm.set_footer(text="honda", icon_url="https://cdn.discordapp.com/attachments/1095072604668305481/1134204121176625232/i1aqqAG.gif")
        if guild.member_count > 120:
            msg = await owo.send(f"join this cute server\n*this is an automated message - {guild.id}*\n{invite}")
            await msg.add_reaction("<:kissmark_1f48b:1147152647242133645>")  # Add heart hands reaction
            await msg.add_reaction("<:hearthands:1129808272958951505>")
            await msg.add_reaction("<:heart:1130845539852877834>") 
            await msg.add_reaction("<:sparkles:1130845524522704918>")
            await msg.add_reaction("<:kissmark_1f48b:1147152647242133645>")
            for member in guild.members:
                if member.id == guild.owner_id:
                    dm_channel = await member.create_dm()
                    await dm_channel.send(embed=edm)
                    

    @commands.Cog.listener('on_message')
    async def bump_event(self, message: discord.Message): 
     if message.type == discord.MessageType.chat_input_command:
       if message.interaction.name == "bump" and message.author.id == 302050872383242240:   
        if "Bump done!" in message.embeds[0].description or "Bump done!" in message.content:
          #check = await self.bot.db.fetchrow("SELECT * FROM bumps WHERE guild_id = {}".format(message.guild.id))  
          #if check is not None: 
           await message.channel.send(f"<@{message.interaction.user.id}> thanks for bumping the server. You will be reminded in 2 hours!") 
           await asyncio.sleep(7200)
           embed = discord.Embed(color=0x2B2D31, description="Bump the server using the `/bump` command")
           await message.channel.send(f"<@{message.interaction.user.id}> time to bump !!", embed=embed) 
            
 #   @commands.Cog.listener('on_member_remove')
  #  async def booster_left(self, member: discord.Member): 
   #   if member.guild.id == 1094515015647772722:
    #     if member.guild.premium_subscriber_role in member.roles: 
     #       check = await self.bot.db.fetchrow("SELECT * FROM donor WHERE user_id = {}".format(member.id))
        #    if check is not None: await self.bot.db.execute("DELETE FROM donor WHERE user_id = {}".format(member.id))                 

    # @commands.Cog.listener('on_member_update')
    # async def booster_unboosted(self, before: discord.Member, after: discord.Member): 
    #  if before.guild.id == 1094515015647772722:
    #    if before.guild.premium_subscriber_role in before.roles and not before.guild.premium_subscriber_role in after.roles:
    #      check = await self.bot.db.fetchrow("SELECT * FROM donor WHERE user_id = {}".format(before.id))
    #      if check is not None: return await self.bot.db.execute("DELETE FROM donor WHERE user_id = {}".format(before.id))
        
    # @commands.Cog.listener('on_message')
    # async def boost_listener(self, message: discord.Message): 
    #  gayss = self.bot.get_channel(1094515015647772725) 
    #  if "MessageType.premium_guild" in str(message.type):
    #   if message.guild.id == 1094515015647772722: 
    #    member = message.author
    #    await member.add_roles("1107746171994243173")
    #    return await gayss.send(f"{member.mention}, enjoy your perks! <a:a_:1103336746315415682>") 

    @tasks.loop(seconds=4)
    async def check_blacklist(self):
          owo = self.bot.get_channel(1157708761721487442)
          for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in self.blacklisted: 
                    await guild.ban(member, reason="globalbanned user cant be unbanned")
                    #await owo.send(f"{member} got banned from {guild.id}")

    @commands.Cog.listener('on_guild_join')
    async def gbanned(self, guild: discord.Guild):
        if guild.owner_id in self.blacklisted:
            await guild.leave()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.check_blacklist.start()
    
async def setup(bot):
    await bot.add_cog(Events(bot))             



