import pandas
import telebot
import random

chave_api_telegram = "CHAVE DO BOT TELEGRAM"

bot = telebot.TeleBot(chave_api_telegram)

try:
    data = pandas.read_csv('data.csv')
except FileNotFoundError:
    data = pandas.DataFrame(columns=['pergunta', 'resposta'])

def salvar_pergunta_resposta(pergunta, resposta):
    global data
    data = data.append({"pergunta": pergunta, "resposta": resposta}, ignore_index=True)
    data.to_csv("data.csv", index=False)

@bot.message_handler(commands=["adicionar"])
def adicionar_pergunta(message):
    bot.send_message(message.chat.id, "Qual é a pergunta?")
    bot.register_next_step_handler(message, aguardar_pergunta)

def aguardar_pergunta(message):
    pergunta = message.text
    bot.send_message(message.chat.id, "Qual é a resposta?")
    bot.register_next_step_handler(message, lambda m: aguardar_resposta(m, pergunta))

def aguardar_resposta(message, pergunta):
    resposta = message.text
    salvar_pergunta_resposta(pergunta, resposta)
    bot.send_message(message.chat.id, "OBRIGADO, graças a você aprendi algo novo!")

@bot.message_handler(commands=["pergunta"])
def responderPergunta(message):
    user_pergunta = message.text.replace("/pergunta", "").strip()
    resposta = None
    error = "Desculpe, eu não sei a respota para essa pergunta"

    linha = data.loc[data["pergunta"] == user_pergunta]

    if not linha.empty:
        resposta = linha.iloc[0]["resposta"]

    if resposta is not None:
        bot.reply_to(message, resposta)
    else:
        bot.reply_to(message, error)

@bot.message_handler(commands=["rolarDado"])
def dado_de_seis(message):
    dados = [6, 8, 10, 12, 20, 100]
    dado = random.randint(0, len(dados) - 1)

    valor_dado = random.randint(1, dados[dado])

    text = f"""
    O dado girado foi 1d{dados[dado]}
    O valor do dado foi: {valor_dado}

    Rolar outro dado: /rolarDado
    """

    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def mensagem(message):
    text = """
    Olá! Como posso ajudar:

    /pergunta Faça uma pergunta ao bot
    /adicionar Adicione uma pergunta e resposta no banco de dados do bot
    /rolarDado Role qualquer tipo de dado (1d6, 1d8, 1d20, etc)
    """

    bot.reply_to(message, text)

bot.polling()