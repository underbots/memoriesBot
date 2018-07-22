from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler , Filters
import time as t
import csv

from _configure import TOKEN
from git_update import git_update



########################### global variables#################################
# fUNTION NECESITIES
WRITING , W1 = range(2) #
FILE = 'memories.md'
DIR = 'media/'
UDF = 'user_data.csv' # user data file, name

# Messages
HELP = """Hello, here you can store your more relevant (at least for you) memories, any kind of feelings.
The instructions are:        
   /start basic bot initialization
   /help shows this beautiful message
   /hi to start writing your memories 
   /done to close your memories 
   /git to upload your result
"""

START = """Oh dear, I look forward to hearing from you :) ESTO ES CREEPY PERO BUENO

Please tell me whatever you want, I am an open book"""

END_W = """Reading you has been a pleasure!"""
#########################  basic calls#########################

def setup (bot , update ):
   """
   Create or upload de user informatión a redstribute to his count
   user_data.csv;  structure: id, first name , username  
"""
   user_id = update.message.from_user.id
   first_name = update.message.from_user.first_name
   user_name = update.message.from_user.username

   with open(UDF, 'a', newline='') as csvfile: # cambio w por a
    fieldnames = ['id', 'first name' , 'username' ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'id': user_id, 'first name': first_name , 'username': user_name})

    writer.close()

   print (f""" Usuario {user_name} detectado:
Hola , {first_name}, espero no haberte asustado, su id es {user_id}""")
   
def help_ms(bot , update):
   """ string -> void
"""
   update.message.reply_text(HELP)

def start( bot , update ):
    """Show a message that mean that you have started
"""
    #file management # AÑADIR CONTROL DE LA FECHA
    global DATA
    global modified
    with open(FILE , 'r') as original:
       DATA = original.read()
    original.close()

    modified = open( FILE , 'w')
    modified.write(f'\n# {t.strftime("%A")} {t.strftime("%d")}  {t.strftime("%M")} {t.strftime("%y")} a las {t.strftime("%H:%M:%S")} \n ' ) # Imprimo la fecha t.strftime('%y-%m-%d_%a_%H_%M_%S')

    
    update.message.reply_text(START)
    
    return WRITING

def write1(bot , update):
    """ repeat the message you have write
"""
    file_text = update.message.text
    update.message.reply_text( f' OMG ')
    modified.write(file_text + '\n')
    
    return WRITING

def write(bot , update):
    """ repeat the message you have write
"""
    file_text = update.message.text
    update.message.reply_text( f' Ok ')
    modified.write(file_text + '\n')
    return W1

    
def photo (bot , update):
   """ manage photos"""
   
   photo = update.message.photo[-1]
   # Preguntar por el nombre de la foto y modificar (interactive_tools.py)
   name = t.strftime('%y-%m-%d_%a_%H_%M_%S')
   path =  DIR+ name
   #gestión de carpetas
   
   file_id = photo.file_id
   file_down = bot.get_file(file_id)
   file_down.download(path)

   modified.write(f'![{name}](/{path})\n')
   update.message.reply_text( f'Su fotillo {name} ha sido descargada en la carpeta {DIR} ')
   
   return W1
 
def my_finish (bot , update):
   """end conversation
"""
   #file managemet
   modified.write(DATA)
   modified.close()

   update.message.reply_text( END_W)
   
   return ConversationHandler.END

def git ( bot , update ):
   """ update to git """
   git_update( f"Diario del día {t.strftime('%y-%m-%d_%a_%H_%M_%S')}" )
 
######################## main #####################################
def  main():
   
   updater = Updater(TOKEN) 
   
   # my calls 
   updater.dispatcher.add_handler(CommandHandler("start", setup ))
   updater.dispatcher.add_handler(CommandHandler('help', help_ms))
   updater.dispatcher.add_handler(CommandHandler('git', git ))
   
   conv_handler = ConversationHandler(
      entry_points=[ CommandHandler('hi', start) ],
      # both states has the same options, but for design reason the need to coexist :)
      states={ 
         WRITING: [ MessageHandler( Filters.text , write) , MessageHandler( Filters.photo , photo) ], # add inside Fiters.phto, video, audio...
         W1:[ MessageHandler( Filters.text , write1)  , MessageHandler( Filters.photo , photo)]
      
        },

        fallbacks=[ CommandHandler('done', my_finish) , CommandHandler('help', help_ms),CommandHandler("start", help_ms) ]
   )

   # AÑADIR MODO UPDATE PARA SUBIR ACTUALIZACIÓN A GIT (estaría guay que te enviara un enlace, para así poder verlo desde la página wed)
   updater.dispatcher.add_handler(conv_handler)
   # basic coniguration
   updater.start_polling()
   updater.idle()

if __name__ == '__main__':
   main()

 
