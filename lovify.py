from telegram.ext import * 
import telegram
import mysql.connector
from mysql.connector import Error
from threading import Thread
from time import sleep




'''

0 - aspetta il comando start 
1 - chiede se si vuole info o se si vuole mandare un messaggio 
2 - chiede a che numero si vuole mandare il messaggio
'''


def start_mysql_connection():
    try:
        connection = mysql.connector.connect(host="localhost", 
                                            database="lovify",
                                            user="root",
                                            password="root")
        if(connection.is_connected()):
            print("LOG ====> Connected to MYSQL Server!")
        return connection
    except Error as e:
        print("Error occured while connecting")
        print(e)
    
db = start_mysql_connection()
tot = 0

message_delay = 2



phase = 1

def retrieveToken(filename):
    token = open(filename, 'r').read()
    return token

def write_to_channel(update, context, text):
    # Prendi il testo del messaggio inviato dopo il comando /scrivi

    # Invia il messaggio di testo nel canale "iGenLoveMeParty"
    context.bot.send_message(chat_id="@LovifyChannel", text=text)




def handle_text(update, context):
    global phase0Message, notintMessage, toNumber, fromNumber, fromAcceptedMessage, toAcceptedMessage, messageSentMessage, phase, message, msg_queue, nicknames_queue
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
        if(filter(message) == False):
            warn = "⛔ Hai usato una parola non ammessa, per favore riscrivi il messaggio ! ⛔"
            context.bot.send_message(chat_id = update.effective_chat.id, text=warn)
        else:
#             context.bot.send_message(chat_id = update.effective_chat.id, text=messageSentMessage)
#             text = '''
#             NUOVO MESSAGGIO  💌
# Indirizzato al numero: {}
# {}
#             '''.format(toNumber, message)
#             write_to_channel(update, context, text)
            fromNumber = update.message.from_user.first_name
            saveMessage(toNumber, fromNumber, message)
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
    context.bot.send_message(chat_id=update.effective_chat.id, text=phase2Message)

def annullaInvio(update, context):
    global phase, fromNumber, toNumber
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hai annullatto l'invio del messaggio !")
    fromNumber = 0
    toNumber = 0
    phase = 1

def saveMessage(receiver, sender, message):
    global db

    cursor = db.cursor()
    query = "INSERT INTO messaggi (receiver, sender, textSent, msgRead) VALUES (%s, %s, %s, %s)"
    record = (receiver, sender, message, 0)
    cursor.execute(query, record)
    db.commit()
    print("LOG ====> Successfully Inserted!")

def filter(phrase): 
    global forbiddenWords
    found = 0
    phrase = phrase.replace("\n", "").lower()
    for i in forbiddenWords:
        if(i.replace("\n", "").replace(" ", "") in phrase):
            found = 1

    if found == 1: 
        return False
    else:
        return True

def getFirstNonRead():
    global db

    cursor = db.cursor()
    query = "SELECT * FROM messaggi WHERE msgRead=0 LIMIT 1"
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def readFirstNonRead(id):
    global db

    cursor = db.cursor()
    query = "UPDATE messaggi SET msgRead=1 WHERE id=%s"
    record = (id,)
    cursor.execute(query, record)
    db.commit()
    

def startVisualizer():
    global message_delay
    while(True):
        firstNonRead = getFirstNonRead()
        if(firstNonRead != []):
            firstNonRead = firstNonRead[0]
            print(firstNonRead)
            nonReadid = firstNonRead[0]
            nonReadReceiver = firstNonRead[1]
            nonReadText = firstNonRead[2]
            print("il numero {} riceve {}".format(nonReadReceiver, nonReadText))
            readFirstNonRead(nonReadid)
        sleep(message_delay)



toNumber = 0
fromNumber = 0
message = ""



token = retrieveToken("token.txt")
initMessage = open('messages/initMessage.txt', 'r').read()
phase0Message = open('messages/phase0message.txt', 'r').read()
phase2Message = open("messages/phase2Message.txt", 'r').read()
notintMessage = open("messages/notintmessage.txt", 'r').read()
fromAcceptedMessage = open("messages/fromAcceptedMessage.txt", 'r').read()
toAcceptedMessage = open("messages/toAcceptedMessage.txt", "r").read()
messageSentMessage = open("messages/messageSent.txt", "r").read()
forbiddenWords = open("messages/filter.txt", 'r').readlines()



updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

#dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("inviaunmessaggio", asktoNumber))
dispatcher.add_handler(CommandHandler("annulla", annullaInvio))

dispatcher.add_handler(MessageHandler(Filters.text, handle_text))





print("LOG ====> Startin the bot")
updater.start_polling(1.0)

visualizerThread = Thread(target=startVisualizer).start()
