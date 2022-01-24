# import telegram.ext
#
# with open('../token_main.txt') as token_file:
#     TOKEN = token_file.read()
#
# token_file.close()
#
# with open('../all_questions.txt') as questions_file:
#     list_questions = questions_file.read()
#
# questions_file.close()
#
#
# def start(update, context):
#     update.message.reply_text("Hello! Welcome)))")
#
#
# def help(update, context):
#     update.message.reply_text("Help!!!")
# def start_test(update, context):
#     global list_questions
#     previous_message = ""
#     update.message.reply_text("As soon as any questions will appear, you will see them")
#     while True:
#         with open('../all_questions.txt') as updated_questions_file:
#             updated_list = updated_questions_file.read()
#         updated_questions_file.close()
#         if list_questions != updated_list:
#             update.message.reply_text("Updated list: ")
#             update.message.reply_text(updated_list)
#             list_questions = updated_list
#
#
# updater = telegram.ext.Updater(TOKEN, use_context=True)
# disp = updater.dispatcher
#
# disp.add_handler(telegram.ext.CommandHandler("start", start))
# disp.add_handler(telegram.ext.CommandHandler("help", help))
# disp.add_handler(telegram.ext.CommandHandler("start_test", start_test))
#
# updater.start_polling()
# updater.idle()

import requests

with open('../token_main.txt') as token_file:
    TOKEN = token_file.read()

token_file.close()

with open('../all_questions.txt') as questions_file:
    list_questions = questions_file.read()

questions_file.close()

bot_chatID = -668820576
while True:
    with open('../all_questions.txt') as updated_questions_file:
        updated_list = updated_questions_file.read()
    updated_questions_file.close()
    if list_questions != updated_list:
        send_text_1 = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID.__str__() + '&parse_mode=Markdown&text=' + 'Updated:'
        send_text_2 = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID.__str__() + '&parse_mode=Markdown&text=' + updated_list
        requests.get(send_text_1)
        requests.get(send_text_2)
        list_questions = updated_list
