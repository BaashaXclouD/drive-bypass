from bot.helper.telegram_helper.message_utils import sendMessage
from bot import AUTHORIZED_CHATS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands


def authorize(update,context):
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    msg = ''
    with open('authorized_chats.txt', 'a') as file:
        if len(message_) == 2:
            chat_id = int(message_[1])
            if chat_id not in AUTHORIZED_CHATS:
                file.write(f'{chat_id}\n')
                AUTHORIZED_CHATS.add(chat_id)
                msg = '𝐂𝐡𝐚𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
            else:
                msg = 'User already authorized'
        elif reply_message is None:
            # Trying to authorize a chat
            chat_id = update.effective_chat.id
            if chat_id not in AUTHORIZED_CHATS:
                file.write(f'{chat_id}\n')
                AUTHORIZED_CHATS.add(chat_id)
                msg = '𝐂𝐡𝐚𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
            else:
                msg = '𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐜𝐡𝐚𝐭'
        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id not in AUTHORIZED_CHATS:
                file.write(f'{user_id}\n')
                AUTHORIZED_CHATS.add(user_id)
                msg = '𝐏𝐞𝐫𝐬𝐨𝐧 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭!'
            else:
                msg = '𝐏𝐞𝐫𝐬𝐨𝐧 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
        sendMessage(msg, context.bot, update)



def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        chat_id = int(message_[1])
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            msg = '𝐂𝐡𝐚𝐭 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
        else:
            msg = '𝐔𝐬𝐞𝐫 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
    elif reply_message is None:
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            msg = '𝐂𝐡𝐚𝐭 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
        else:
            msg = '𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐜𝐡𝐚𝐭'
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(user_id)
            msg = '𝐏𝐞𝐫𝐬𝐨𝐧 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭!'
        else:
            msg = '𝐏𝐞𝐫𝐬𝐨𝐧 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐮𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝!'
    with open('authorized_chats.txt', 'a') as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)



def sendAuthChats(update,context):
    users = ''.join(f"{user}\n" for user in AUTHORIZED_CHATS)
    users = users if users != '' else "None"
    sendMessage(f'Authorized Chats are : \n<code>{users}</code>\n', context.bot, update)


send_auth_handler = CommandHandler(command=BotCommands.AuthorizedUsersCommand, callback=sendAuthChats,
                                    filters=CustomFilters.owner_filter, run_async=True)
authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter, run_async=True)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter, run_async=True)

dispatcher.add_handler(send_auth_handler)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)
