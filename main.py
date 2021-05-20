from typing import ValuesView
import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import keep_alive

from discord.user import User

intents = discord.Intents().all()
client = commands.Bot(command_prefix = "pip!", intents=intents)
bot_name = "Pypurpose"

# Prepare the Statuses for Cycling!
status = cycle([
  'Friend my Creator!',
  'with you 👀',
  'pip!help | Join the Support Server!',
  'Coded by Yoshiboi18303',
  'Made using Python',
  'pip!mute | Start making your server safer with my Moderation Commands!',
  'Follow my people on Twitter | pip!updates'
])

@tasks.loop(seconds = 10)
async def status_swap():
  await client.change_presence(activity=discord.Game(next(status)))

  # Start The bot, then Print something in the Console
@client.event
async def on_ready():
  print(f"{bot_name} is ready!")
  status_swap.start()
  # ^ Start Cycling through the Statuses!


@client.event
async def on_member_join(member):
  welcomeEmbed = discord.Embed(title = f"Welcome {member.name}!", description = f"Hello {member.mention}, welcome to Pypurpose | Support!", color = discord.Colour.green())

  await client.get_channel(844566581845033000).send(embed = welcomeEmbed)

@client.event
async def on_member_remove(member):
  goodbyeEmbed = discord.Embed(title = f"Goodbye {member.name}!", description = f"Big oof, {member.name} left Pypurpose | Support... hope you come back!", color = discord.Colour.red())

  await client.get_channel(844566727828045895).send(embed = goodbyeEmbed)

@client.command(aliases=['8ball','8b'])
async def eightball(ctx, *, question):
  responses = [
    'Outlook good.',
    'Yes - Definitely.',
    'Yes.',
    'Reply Hazy, try again.',
    'Ask Again Later',
    'Cannot Predict Now.',
    'I have no idea, but you should friend Yoshiboi18303#4045 on Discord!',
    'Hi',
    'Try again.',
    'Ok',
    'What',
    'Good Question',
    'Don’t count on it',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Very doubtful',
    'Better not tell you now',
    'Concentrate and ask again.',
    'It is certain',
    'It is decidedly so',
    'Without a doubt',
    'You may rely on it',
    'As I see it, yes',
    'Most Likely',
    'Signs point to yes'
  ]
  await ctx.send(f":8ball: Question: {question}\n:8ball: 8-ball says: {random.choice(responses)}")

@client.command(aliases=['boot'])
async def kick(ctx, member:discord.Member, *, reason=None):
  if(not ctx.author.guild_permissions.kick_members):
    await ctx.send('You require the `Kick Members` permission to run this command!')
  return
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} has been kicked for reason {reason}!')

@client.command(aliases=['hammer'])
async def ban(ctx, member:discord.Member, *, reason=None):
  if(not ctx.author.guild_permissions.ban_members):
    await ctx.send('You require the `Ban Members` permission to run this command!')
  return
  await member.ban(reason=reason)
  await ctx.send(f'{member.mention} has been banned for reason {reason}!')

@client.command(aliases=['unb','forgive'])
async def unban(ctx, *, member):
  if(not ctx.author.guild_permissions.ban_members):
    await ctx.send('You require the `Ban Members` permission to run this command!')
  return
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if(user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"I've unbanned {user.mention} from {ctx.guild}!")
      return

@client.command(aliases=['purge'])
async def clear(ctx, amount=10):
  if(not ctx.author.guild_permissions.manage_messages):
    await ctx.send('You require the `Manage Messages` permission to run this command!')
    return
  if amount > 100:
      await ctx.send("Sorry, the Discord Limit puts me to a Max of 100 Messages that can be Deleted from a channel!")
  else:
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages from {ctx.channel}!')

@client.command()
async def mute(ctx, member : discord.Member, *, reason=None):
  if(not ctx.author.guild_permissions.manage_messages):
    await ctx.send('You require the ``Manage Messages`` permission to run this command!')
    return

  guild = ctx.guild
  muteRole = discord.utils.get(guild.roles, name="Muted")

  await ctx.send("I see you don't have a Muted role here, let me fix that.")

  if not muteRole:
      muteRole = await guild.create_role(name="Muted")

      for channel in guild.channels:
        await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
      await member.add_roles(muteRole, reason=reason)
      await ctx.send(f"{member.mention} has been Muted!")
      await member.send(f"You have been muted in **{guild.name}** | Reason: **{reason}**!")

@client.command(aliases=['server','si'])
async def serverinfo(ctx):
  role_count = len(ctx.guild.roles)
  bot_count = [bot.mention for bot in ctx.guild.members if bot.bot]
  region = ctx.guild.region
  server_name = ctx.guild.name

  siEmbed = discord.Embed(timestamp = ctx.message.created_at, title=f"{ctx.guild.name} Information!", color = ctx.author.color)
  siEmbed.add_field(name='Server Name', value = server_name, inline=True)
  siEmbed.add_field(name='Server Region', value = region, inline=True)
  siEmbed.add_field(name='Verification Level', value = str(ctx.guild.verification_level), inline=True)
  siEmbed.add_field(name='Highest Role', value = ctx.guild.roles[-2], inline=True)
  siEmbed.add_field(name=f'Roles in {ctx.guild.name}', value = str(role_count), inline=True)
  siEmbed.add_field(name='Member Count', value = ctx.guild.member_count, inline=True)
  siEmbed.add_field(name='Bot Count', value = ', '.join(bot_count), inline=True)

  await ctx.send(embed = siEmbed)

@client.command(aliases=['twitter'])
async def updates(ctx):
  await ctx.send(f"Hello {ctx.author.mention}! Follow my Creator here! <https://twitter.com/Yoshiboi_Dev>")

@client.command(aliases=['opfp'])
async def oldprofilepic(ctx):
  await ctx.send("https://cdn.discordapp.com/avatars/844288136544780298/e74701289c1abb3f45fb6e2c1ae83eb5.png?size=2048")


@eightball.error
async def eightball_error(ctx, error):
   if isinstance(error, commands.MissingRequiredArgument):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Question.```\n`Logging to Console...`")
     print(f"An error was Encountered in guild: {ctx.guild}! Error was: {error}")

@ban.error
async def ban_error(ctx, error):
   if isinstance(error, commands.MissingRequiredArgument):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Member.```\n`Logging to Console...`")
     print(f"An error was Encountered in guild: {ctx.guild}! Error was: {error}")
   elif isinstance(error, commands.MemberNotFound):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Valid Member.```\n`Logging to Console...`")
     print(f"An error was Encountered in guild: {ctx.guild}! Error was: {error}")

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Member.```\n`Logging to Console...`")
     print(f"An error was Encountered in {ctx.guild}! Error was: {error}")
  elif isinstance(error, commands.MemberNotFound):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Valid Member.```\n`Logging to Console...`")
     print(f"An error was Encountered in guild: {ctx.guild}! Error was: {error}")

@mute.error
async def mute_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Member.```")
     print(f"An error was Encountered in {ctx.guild}! Error was: {error}")
  elif isinstance(error, commands.MemberNotFound):
     await ctx.send(f"Whoopsies! We ran into an Error, the error was: ```{error}```\nHow to fix this: ```Please include a Valid Member.```\n`Logging to Console...`")
     print(f"An error was Encountered in guild: {ctx.guild}! Error was: {error}")

keep_alive.keep_alive()
client.run(BOT_TOKEN_HERE)
