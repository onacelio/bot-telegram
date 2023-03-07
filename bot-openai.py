import telebot
import openai

openai.api_key = "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"
chave_api_telegram = "6106311624:AAGH_MRyPVA6y2yNcRLu3-mn4pXyjCXF-HY"

bot = telebot.TeleBot(chave_api_telegram)

@bot.message_handler(commands=["pergunta"])
def responder_pergunta(message):
    pergunta = message.text.replace("/pergunta", "").strip()

    if not pergunta:
        bot.reply_to(message, "Por favor faça uma pergunta!")
        return 

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=pergunta,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    bot.reply_to(message, response.choices[0].text)

@bot.message_handler(commands=["mandarOi"])
def mandarOi(message):
    bot.send_message(message.chat.id, "Olá, sou um bot de teste!")

def verificar(message):
    return True

@bot.message_handler(func=verificar)
def responder(message):
    text = """
            /mandarOi Mande um oi
        /pergunta Faça uma pergunta
    """

    bot.reply_to(message, text)

bot.polling()