import telebot
from poll import governor
from message_builder import Message_builder
import os 
from dotenv import load_dotenv 
load_dotenv()
telegram_key = os.environ.get("TELEGRAM_KEY")
print (telegram_key)

bot = telebot.TeleBot(telegram_key, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def send_stats(message):

	text = Message_builder()
	bot.reply_to(message, text)
	name = message.from_user.first_name

	print (f'Stats asked by {name}')
	print ("Stats provided ✅")



@bot.message_handler(commands=['prop'])
def send_stats(message):
	name = message.from_user.first_name
	content = message.text
	#getting the proposal id given by the user
	result = content.replace("/prop ","")  
	#making sure it's /prop + proposal id. Ff it's not, the bot sends a message to the user
	try:     		 
		int(result) 
		proposal_id_given = True
	except:
		bot.reply_to(message,"Enter /prop + [proposal id]") #
		proposal_id_given = False

	if proposal_id_given: 
		data = governor(result)
		bot.reply_to(message,data)

	#sending stickers after some specific proposals are shown. Just for fun.
	if result =="329": 
		bot.send_sticker(message.chat.id, sticker="CAACAgQAAxkBAAEocV1liV7aQPm5hZiuucuec5uElajwqQACTg8AAqbxcR4yrsxLTFkHvjME")
	if result =="16": 
		bot.send_sticker(message.chat.id, sticker= "CAACAgIAAxkBAAEocWFliV8pMY1C6CH4XkHwGhTIOUOCIAAClw0AAm-K8EtwIBpzwV7QdDME")

bot.infinity_polling()
