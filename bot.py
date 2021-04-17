from telebot import TeleBot, types
from io import BytesIO
from PIL import Image
import os, re

TOKEN =os.environ.get("BOT_TOKEN",None)
bot = TeleBot(TOKEN)

list_image = {}

@bot.message_handler(commands = ["start"])
def start(message):
 name = re.sub(r"[*_`]", "", message.from_user.first_name)
 msg = f"""
Hi* _{name}_!* iam image to pdf bot 

_i can convert image to pdf_


*This bot created by @nicebroadmin*
  """

 markup = types.InlineKeyboardMarkup()
 markup.add(types.InlineKeyboardButton("Get updates ", url = "https://t.me/lntechnical"))
 bot.send_message(message.from_user.id, msg, reply_markup = markup, parse_mode = "Markdown")

@bot.message_handler(content_types = ["photo"])
def add_photo(message):
 if not isinstance(list_image.get(message.from_user.id), list):
  bot.reply_to(message, """ 
  I can't 😔  convert your iamge to pdf you  need to \nclick here 👉   /pdf
   """)
  return

 if len(list_image[message.from_user.id]) >= 20:
  bot.reply_to(message, "Maximal 20 images :(")
  return

 file = bot.get_file(message.photo[1].file_id)
 downloaded_file = bot.download_file(file.file_path)
 image = Image.open(BytesIO(downloaded_file))

 list_image[message.from_user.id].append(image)
 bot.reply_to(message, f"""{len(list_image[message.from_user.id])} image Successful created PDF if you want add image send me more image
 If done click here 👉 /convert  """)

@bot.message_handler(commands = ["pdf"])
def pdf(message):
 bot.send_message(message.from_user.id, """Send me image one by one 
I making list  don't confuse me 😂 """)

 if not isinstance(list_image.get(message.from_user.id), list):
  list_image[message.from_user.id] = []

@bot.message_handler(commands = ["convert"])
def done(message):
 images = list_image.get(message.from_user.id)

 if isinstance(images, list):
  del list_image[message.from_user.id]

 if not images:   
  bot.send_message(message.from_user.id, "Send me image only 😒  !!")
  return

 path = str(message.from_user.id) + ".pdf"
 images[0].save(path, save_all = True, append_images = images[1:])
 bot.send_document(message.from_user.id, open(path, "rb"), caption = "It is your pdf\n Tankyou for using \nJoin us @lntechnical  !!")
 os.remove(path)

bot.polling(none_stop = True)
