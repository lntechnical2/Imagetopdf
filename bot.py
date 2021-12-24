import os
from PIL import Image
from pyrogram import Client,filters 
from pyrogram.types import (InlineKeyboardButton,  InlineKeyboardMarkup)

from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

TOKEN = os.environ.get("TOKEN", "5038294950:AAEyM5XCPiU3jXcHdUe5EqMzEPidI70y9x8")

API_ID = int(os.environ.get("API_ID", 17360277))

API_HASH = os.environ.get("API_HASH", "6ddf1de91bd98748f61cabb3b71d2d15")
app = Client(
        "pdf",
        bot_token=TOKEN,api_hash=API_HASH,
            api_id=API_ID
    )


LIST = {}

@app.on_message(filters.command(['start']))
async def start(client, message):
 await message.reply_text(text =f"""- Welcome Dear, 
- In Bot Convert Images To PDF ✅
- Send Images To Be Converted To PDF""",reply_to_message_id = message.message_id 
 )



@app.on_message(filters.private & filters.photo)
async def pdf(client,message):
 
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.photo.file_id)
 ms = await message.reply_text("Converting to PDF 🔁......")
 file = await client.download_media(file_id)
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])}Successful Created PDF If You Want Add More Image Send Me One By One.\n\n **في حالة الانتهاء ، انقر هنا 👉 /convert** ")
 

@app.on_message(filters.command(['convert']))
async def done(client,message):
 images = LIST.get(message.from_user.id)

 if isinstance(images, list):
  del LIST[message.from_user.id]
 if not images:
  await message.reply_text( "No image !!")
  return

 path = f"{message.from_user.id}" + ".pdf"
 images[0].save(path, save_all = True, append_images = images[1:])
 
 await client.send_document(message.from_user.id, open(path, "rb"), caption = "تفضل ملف PDF !!\n**PDF Created By : @GaN2OO1**")
 os.remove(path)
 
 
 
 
app.run()
