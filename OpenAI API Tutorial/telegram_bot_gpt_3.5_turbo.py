from openai import OpenAI 

model = "gpt-3.5-turbo"
client = OpenAI(api_key="your_openai_api_key")

def askai(user_input):
  response = client.chat.completions.create(model=model,messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": user_input}])  
  output = response.choices[0].message.content  
  return output

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):  
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):  
  await context.bot.send_message(chat_id=update.effective_chat.id, text=askai(update.message.text))

if __name__ == '__main__':  
  application = ApplicationBuilder().token('telegram_bot_token').build()      
  
  start_handler = CommandHandler('start', start)  
  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)      
  application.add_handler(start_handler)  
  application.add_handler(echo_handler)

  application.run_polling()