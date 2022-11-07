from pydoc import cli
import discord
from discord.ext import commands
from openpyxl import load_workbook

'''fn = 'List_of_santas.xlsx'
wb = load_workbook(fn)
ws = wb['data']
ws['A5'] = 'hello word'
wb.save(fn)
wb.close'''
PREFIX = '!'
fn = 'List_of_santas.xlsx' #xl файл для записи участников и реквестов
bot = commands.Bot( command_prefix = PREFIX, help_command=None, intents=discord.Intents.all())
bot.remove_command('help')

#words
hello_words = ['sup', 'hi', 'hellow', 'привет', 'сап', 'драсте', 'приветствую']
answer_words = ['как дел', 'как дела', 'который час', 'какой сейчас год', 'ты кто', 'кто ты']
@bot.event

#сообщение о готовности
async def on_ready():
    print()
    print("We have logged in as {0.user} ".format(bot)) 
    await bot.change_presence( status=discord.Status.online, activity=discord.Game('секретного санту'))

#функция записи реквеста в файл
async def add_req(message, req):
    wb = load_workbook(fn)
    ws = wb['data']
    ws.append([message.author.name + '#' + message.author.discriminator, req.content])
    wb.save(fn)
    wb.close
    print('успешная запиь в файл')




@bot.command( pass_context = True)
@commands.has_permissions(administrator = True)
async def clear( ctx, amount : int):
    await ctx.channel.purge( limit = amount )

#hello
@bot.command( pass_context = True)
async def hello( ctx, amount = 1 ):
    author = ctx.message.author
    await ctx.channel.purge( limit = amount )
    await ctx.send(f'привет, {author.mention} ' )



#herp

@bot.command( pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'навигация по командам')
    emb.add_field(name = '{}clear'.format(PREFIX), value = 'очистка чата')
    emb.add_field(name = '{}ban'.format(PREFIX), value = 'ban')
    emb.add_field(name = '{}kick'.format(PREFIX), value = 'kick')
    emb.add_field(name = '{}help'.format(PREFIX), value = 'помогай')

    await ctx.send (embed = emb)



#send direct message to author
@bot.command()
async def send_a(ctx):
    await ctx.author.send('hellow')

#send direct message to another
@bot.command()
async def send_to(ctx, member: discord.Member):
    await member.send(f'{member.name}, *текст подтянутый из таблицы в качестве рекветса*')


'''@bot.event
async def on_message(message):
    await bot.process_commands(message)
    msg = message.content.lower()

    if msg in hello_words:
        await message.channel.send('привет дружественная форма жизни')
    if msg in answer_words:
        await message.channel.send('не твоё дело, человечек')'''
#получение данных в директе от участника
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    msg = message.content.lower()

    if  not message.guild and msg in hello_words:
        await message.channel.send(f'привет котик, {message.author}')


    if  not message.guild and msg in answer_words:
        await message.channel.send('не твоё дело, человечек')
    if  not message.guild and msg == 'help':
        emb = discord.Embed(title = 'навигация по командам')
        emb.add_field(name = '{}clear'.format(PREFIX), value = 'очистка чата')
        emb.add_field(name = '{}ban'.format(PREFIX), value = 'ban')
        emb.add_field(name = '{}kick'.format(PREFIX), value = 'kick')
        emb.add_field(name = '{}help'.format(PREFIX), value = 'помогай')
        await message.channel.send (embed = emb)
    if  not message.guild and msg == 'участвовать':
        channel = message.channel
        await channel.send('диктуй свой реквест')
        req = await bot.wait_for('message')
        add_req(message, req)
        await message.channel.send('Это всё?')
            

'''@bot.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send(f'Hello {msg.author}!')'''




@bot.event
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

bot.run(token)
