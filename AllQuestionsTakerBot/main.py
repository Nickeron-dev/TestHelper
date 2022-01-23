import telegram.ext

with open('../token_all_questions.txt') as token_file:
    TOKEN = token_file.read()

token_file.close()

with open('../all_questions.txt') as questions_file:
    list_questions = questions_file.read()

questions_file.close()


def start(update, context):
    update.message.reply_text("Hello! Welcome to all questions)))")


def current_message(update, context):
    message = update.message.text
    with open('../all_questions.txt', "a") as current_questions_file:
        current_questions_file.write(message + "\n")

    current_questions_file.close()


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, current_message))

updater.start_polling()
updater.idle()

