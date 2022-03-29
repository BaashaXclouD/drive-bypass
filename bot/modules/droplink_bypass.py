import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from bot.helper.telegram_helper.message_utils import *
from bot import AUTHORIZED_CHATS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands


# droplink url


# ==============================================
    
def droplink_bypass(update,context):
  try:
    url = update.message.text.split(' ',maxsplit=1)[1]
    LOGGER.info(f"Drop link : {url}")
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'
    sendMessage(final_url, context.bot, update, button)

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()
    sendMessage(res, context.bot, update, button)

  except IndexError:
    sendMessage("𝐒𝐞𝐧𝐝 𝐃𝐫𝐨𝐩 𝐋𝐢𝐧𝐤 𝐰𝐢𝐭𝐡 𝐂𝐨𝐦𝐦𝐞𝐧𝐝", context.bot, update)

# ==============================================

drop_handler = CommandHandler(BotCommands.DropCommand, droplink_bypass,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(drop_handler)
