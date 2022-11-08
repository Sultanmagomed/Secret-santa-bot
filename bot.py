from pydoc import cli
import discord
from discord.ext import commands
from openpyxl import load_workbook

PREFIX = '!' #префикс для всяких комманд, которые не используются
fn = 'List_of_santas.xlsx' #xl файл для записи участников и реквестов
bot = commands.Bot( command_prefix = PREFIX, help_command=None, intents=discord.Intents.all())
bot.remove_command('help')

#словари
hello_words = ['sup', 'hi', 'hellow', 'привет', 'сап', 'драсте', 'приветствую']
answer_words = ['как дел', 'как дела', 'который час', 'какой сейчас год', 'ты кто', 'кто ты']
paricipant_word = ['участвовать', 'хочу участвовать', 'быть сантой', 'хочу быть сантой', 'запишите', 'запиши', 'запишите меня', 'запиши меня']
adding_words = ['добавить', 'дополнить', 'добавь', 'дополни', 'дополнение', 'ps', 'add', 'add request', 'ещё', 'ещё кое-что', 'ещё кое что', 'ещё коечто',]
yes_words = ['да', 'lf', 'ja', 'yes', 'es', 'угу']
no_words = ['нет', 'не', 'ytn', 'no', 'нит']

#сообщение о готовности и указание статуса бота
@bot.event
async def on_ready():
    print()
    print("Успешно залогинились как {0.user} ".format(bot)) 
    await bot.change_presence( status=discord.Status.online, activity=discord.Game('секретного санту'))

#функция записи реквеста в файл
async def add_req(message, req):
    wb = load_workbook(fn)
    ws = wb['data']
    ws.append([message.author.name + '#' + message.author.discriminator, req.content, str(await checknget_url(req))])
    wb.save(fn)
    wb.close
    print('успешная запиь в файл')
#функция дополнения реквеста
async def expand_req(req, str_number):
    wb = load_workbook(fn)
    ws = wb['data']
    if req.attachments and str(req.content) != '':
        print('вот что в сообщении, смотри ' + str(req.content))
        ws['B'+ str(str_number)] = str(wb.active.cell(row=str_number, column=2).value) + '. Дополнение: ' + req.content
    else:
        print('ничего нет в сообщении, не дополняю смотри ' + str(req.content))
    if wb.active.cell(row=str_number, column=3).value == None:
        ws['C'+ str(str_number)] = str(await checknget_url(req))
    else:
        ws['C'+ str(str_number)] =str(wb.active.cell(row=str_number, column=3).value) + str(await checknget_url(req))
    wb.save(fn)
    wb.close
    print('успешная запиь в файл')
#функция проверки участника на повторное участие
async def check_participy(message):
    wb = load_workbook(fn)
    requestor = message.author.name + '#' + message.author.discriminator
    for i in range(1,100):
        value=wb.active.cell(row=i, column=1).value
        if value == requestor:
            print (requestor + 'участвует уже, строка №' + str(i))
            return i
    print (requestor + 'не участвовал ещё')
    return False
#функция получения url вложенных картинок
async def checknget_url(message):
    if  not message.guild and message.attachments:
        files = []
        for attachment in message.attachments:
            try:
                if attachment.content_type.startswith("image/"):
                    files.append(attachment.url)
            except:
                continue
        if files:
            return files
        

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


#получение данных в директе от участника
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    msg = message.content.lower()
    #приветсвие
    if  not message.guild and msg in hello_words:
        await message.channel.send(f'привет котик, {message.author}')
    #ответ на ненужный вопрос
    if  not message.guild and msg in answer_words:
        await message.channel.send('не твоё дело, человечек')
    #herp
    if  not message.guild and msg == 'help':
        emb = discord.Embed(title = 'навигация по командам')
        emb.add_field(name = '{}clear'.format(PREFIX), value = 'очистка чата')
        emb.add_field(name = '{}ban'.format(PREFIX), value = 'ban')
        emb.add_field(name = '{}kick'.format(PREFIX), value = 'kick')
        emb.add_field(name = '{}help'.format(PREFIX), value = 'помогай')
        await message.channel.send (embed = emb)




        

#проверка на участие и дополнение реквеста
    if  not message.guild and msg in paricipant_word:
        channel = message.channel
        if await check_participy(message) != False:
            print ('уже участвует')
            await channel.send('ты уже участвуешь, Хочешь что-то добавить?')
            answer = await bot.wait_for('message')
            if answer.content.lower() in yes_words:
                print('да получено')
                await channel.send('диктуй своё дополнение')
                expreq = await bot.wait_for('message') 
                await expand_req(expreq, await check_participy(message))
                await message.channel.send('Это всё дополнение?')
            print('да пропущено')
            return
        else: 
            print ('не участвует')
        await channel.send('диктуй свой реквест')
        req = await bot.wait_for('message')
        await add_req(message, req)
        await message.channel.send('Это всё?')
#Прямое дополнение реквеста с проверкой на участие (надо сделать отдельную функцию принятия реквеста и отдельную дополнения)
    if  not message.guild and msg in adding_words:
        channel = message.channel
        if await check_participy(message) == False:
            print ('ещё не участвует')
            await channel.send('ты ещё не участвуешь, Хочешь участвовать?')
            answer = await bot.wait_for('message')
            if answer.content in yes_words:
                print('да получено')
                await channel.send('диктуй свой реквест')
                req = await bot.wait_for('message')
                await add_req(message, req)
                await message.channel.send('Это всё?')
            print('да пропущено')
            return
        else: 
            print ('участвует')
            await channel.send('диктуй своё дополнение')
            expreq = await bot.wait_for('message') 
            await expand_req(expreq, await check_participy(message))
            await message.channel.send('Это всё дополнение?')

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


with open('token.txt') as file: #Чтение файла из токена
    token = file.readline()

bot.run(token)