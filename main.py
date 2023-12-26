import telebot
from poll import governor
from message_builder import Message_builder
bot = telebot.TeleBot("[TELEGRAM BOT TOKEN]", parse_mode='Markdown') # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['stats'])
def send_stats(message):
	name = message.from_user.first_name
	print (f'Stats asked by {name}')
	text = Message_builder()
	print (text)
	bot.reply_to(message, text)
	print ("Stats provided ✅")


@bot.message_handler(commands=['prop'])
def send_stats(message):
	name = message.from_user.first_name
	content = message.text
	result = content.replace("/prop ","")

	try:
		int(result)
		flag = True
	except:
		bot.reply_to(message,"Enter /prop + [proposal id]")
		flag = False

	if flag ==  True: 
		data = governor(result)
		bot.reply_to(message,data)

	#sending stickers after some specific proposals are shown. Just for fun.
	if result =="329": 
		bot.send_sticker(message.chat.id, sticker="CAACAgQAAxkBAAEocV1liV7aQPm5hZiuucuec5uElajwqQACTg8AAqbxcR4yrsxLTFkHvjME")

	if result =="16": 
		bot.send_sticker(message.chat.id, sticker= "CAACAgIAAxkBAAEocWFliV8pMY1C6CH4XkHwGhTIOUOCIAAClw0AAm-K8EtwIBpzwV7QdDME")

bot.infinity_polling()
