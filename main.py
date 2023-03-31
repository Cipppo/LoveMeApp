from telegram.ext import * 
import telegram

'''

0 - aspetta il comando start 
1 - chiede se si vuole info o se si vuole mandare un messaggio 
2 - chiede a che numero si vuole mandare il messaggio
'''


phase = 1

def retrieveToken(filename):
    token = open(filename, 'r').read()
    return token

def write_to_channel(update, context, text):
    # Prendi il testo del messaggio inviato dopo il comando /scrivi

    # Invia il messaggio di testo nel canale "iGenLoveMeParty"
    context.bot.send_message(chat_id="@LovifyChannel", text=text)




def handle_text(update, context):
    global phase0Message, notintMessage, toNumber, fromNumber, fromAcceptedMessage, toAcceptedMessage, messageSentMessage, phase, message
    text = update.message.text
    if(phase == 1):
        context.bot.send_message(chat_id = update.effective_chat.id, text=phase0Message)
    elif(phase == 2):
        if(not text.isnumeric()):
            context.bot.send_message(chat_id = update.effective_chat.id, text=notintMessage)
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text=toAcceptedMessage)
            toNumber = int(text)
            phase = 3
    elif(phase == 3):
        if(not text.isnumeric()):
            context.bot.send_message(chat_id = update.effective_chat.id, text=notintMessage)
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text=fromAcceptedMessage)
            fromNumber = int(text)
            phase = 4
    elif(phase == 4):
        message = text
        context.bot.send_message(chat_id = update.effective_chat.id, text=messageSentMessage)
        text = "il numero {} ha scritto al numero {} il messaggio -> {}".format(fromNumber, toNumber, message)
        write_to_channel(update, context, text)
        phase = 1
        toNumber = 0
        fromNumber = 0

def start(update, context):
    global phase, initMessage
    phase = 1
    context.bot.send_message(chat_id=update.effective_chat.id, text=initMessage)

def asktoNumber(update, context):
    global phase2Message, phase
    phase = 2
    print("Entrato")
    context.bot.send_message(chat_id=update.effective_chat.id, text=phase2Message)

def annullaInvio(update, context):
    global phase, fromNumber, toNumber
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hai annullatto l'invio del messaggio !")
    fromNumber = 0
    toNumber = 0
    phase = 1


toNumber = 0
fromNumber = 0
message = ""

token = retrieveToken("token.txt")
initMessage = open('initMessage.txt', 'r').read()
phase0Message = open('phase0message.txt', 'r').read()
phase2Message = open("phase2Message.txt", 'r').read()
notintMessage = open("notintmessage.txt", 'r').read()
fromAcceptedMessage = open("fromAcceptedMessage.txt", 'r').read()
toAcceptedMessage = open("toAcceptedMessage.txt", "r").read()
messageSentMessage = open("messageSent.txt", "r").read()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

#dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("inviaunmessaggio", asktoNumber))
dispatcher.add_handler(CommandHandler("annulla", annullaInvio))

dispatcher.add_handler(MessageHandler(Filters.text, handle_text))





print("Startin the bot")
updater.start_polling(1.0)
