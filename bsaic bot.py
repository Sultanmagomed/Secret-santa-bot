from pydoc import cli
import discord
from discord.ext import commands
import datetime

PREFIX = '!'
client = commands.Bot( command_prefix = PREFIX, help_command=None, intents=discord.Intents.all())
client.remove_command('help')

#words
hello_words = ['sup', 'hi', 'hellow', 'привет', 'сап', 'драсте', 'приветствую']
answer_words = ['как дел', 'как дела', 'который час', 'какой сейчас год', 'ты кто', 'кто ты']
@client.event

async def on_ready():
    print('bot connected')
    await client.change_presence( status=discord.Status.online, activity=discord.Game('секретного санту'))


@client.command( pass_context = True)
@commands.has_permissions(administrator = True)
async def clear( ctx, amount : int):
    await ctx.channel.purge( limit = amount )

#hello
@client.command( pass_context = True)
async def hello( ctx, amount = 1 ):
    author = ctx.message.author
    await ctx.channel.purge( limit = amount )
    await ctx.send(f'привет, {author.mention} ' )

#kick

@client.command( pass_context = True)
@commands.has_permissions(administrator = True)
async def kick (ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge ( limit = 1)
    await member.kick (reason = reason)
    await ctx.send (f'kick user {member.mention}')

#ban

@client.command( pass_context = True)
@commands.has_permissions(administrator = True)
async def ban (ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge ( limit = 1)
    await member.ban (reason = reason)
    await ctx.send (f'ban user {member.mention}')

#herp

@client.command( pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'навигация по командам')
    emb.add_field(name = '{}clear'.format(PREFIX), value = 'очистка чата')
    emb.add_field(name = '{}ban'.format(PREFIX), value = 'ban')
    emb.add_field(name = '{}kick'.format(PREFIX), value = 'kick')
    emb.add_field(name = '{}help'.format(PREFIX), value = 'помогай')

    await ctx.send (embed = emb)

#time

@client.command( pass_context = True)
@commands.has_permissions(administrator = True)
async def time(ctx):
    emb = discord.Embed(title = 'сайт времени', color = discord.Color.dark_purple(), url = 'https://www.timeserver.ru/cities/kz/taldykorgan')
    emb.set_author( name = client.user.name, icon_url=client.user.avatar) #client.user.avatar
    emb.set_footer( text = ctx.author.name, icon_url=ctx.author.avatar)
    emb.set_image (url = 'https://tenshi.spb.ru/tenshi_logo_italic_little.gif')
    emb.set_thumbnail (url = 'https://habrastorage.org/r/w60/webt/61/50/55/615055c2a5164708798330.png')
        
    now_date = datetime.datetime.now()
    emb.add_field(name = 'датавремя', value = 'time:{}'.format(now_date) )
    await ctx.author.send(embed = emb)

#send direct message to author
@client.command()
async def send_a(ctx):
    await ctx.author.send('hellow')

#send direct message to another
@client.command()
async def send_to(ctx, member: discord.Member):
    await member.send(f'{member.name}, *текст подтянутый из таблицы в качестве рекветса*')
#unban
@client.command( pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit = 1)
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban (user)
        await ctx.send (f'unbanned user {member.mention}')
        return

@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()

    if msg in hello_words:
        await message.channel.send('привет котик')
    if msg in answer_words:
        await message.channel.send('не твоё дело, человечек')

@client.event
async def on_command_error (ctx, error):
    pass
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author}, сколько сообщений удалить?')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author}, недостаточно прав')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author}, нет такой комманды')
#connect


with open('token.txt') as file:
    token = file.readline()

client.run(token)
