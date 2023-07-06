"""
  ____                   _ _               __     ____   
 |  _ \            /\   | (_)             / /    / /\ \  
 | |_) |_   _     /  \  | |_  ___  _   _ / /    / /  \ \ 
 |  _ <| | | |   / /\ \ | | |/ _ \| | | < <    / /    > >
 | |_) | |_| |  / ____ \| | | (_) | |_| |\ \  / /    / / 
 |____/ \__, | /_/    \_\_|_|\___/ \__,_| \_\/_/    /_/  
         __/ |                                           
        |___/                                            

  _______                  _       _               _______   _      _           _    __      ____ 
 |__   __|                | |     | |             |__   __| | |    | |         | |   \ \    / /_ |
    | |_ __ __ _ _ __  ___| | __ _| |_ ___  _ __     | | ___| | ___| |__   ___ | |_   \ \  / / | |
    | | '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|    | |/ _ \ |/ _ \ '_ \ / _ \| __|   \ \/ /  | |
    | | | | (_| | | | \__ \ | (_| | || (_) | |       | |  __/ |  __/ |_) | (_) | |_     \  /   | |
    |_|_|  \__,_|_| |_|___/_|\__,_|\__\___/|_|       |_|\___|_|\___|_.__/ \___/ \__|     \/    |_|
                                                                                                  
                                                                                                  
"""
import os
import requests
import telebot
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer le jeton d'API Telegram à partir de la variable d'environnement
telegram_api_token = os.getenv('TELEGRAM_API_TOKEN')

# Créer un objet TeleBot avec le jeton d'API Telegram
bot = telebot.TeleBot(telegram_api_token)

# Fonction de traduction
def traduire_texte(texte, de, a):
    body = {
        "de": de,
        "a": a,
        "text": texte
    }

    # Envoyer la requête à l'API de traduction
    response = requests.post('https://codingtranslator.onrender.com/api', json=body)

    if response.status_code == 200:
        # Récupérer la réponse de l'API de traduction
        reponse = response.json()['reponse']
        return reponse
    else:
        return 'Une erreur s\'est produite lors de la traduction.'

# Commande /start
@bot.message_handler(commands=['start'])
def afficher_message_bienvenue(message):
    message_bienvenue = '''
    🌟 Bienvenue ! Je suis votre *traducteur Anglais Francais* 🌍

    Voici les principales commandes que je propose :

    🇺🇸 `/fr hello this is a test` - Traduire le texte en anglais vers francais.
    🇫🇷 `/en salut je suis un test` - Traduire le texte en francais vers anglais.

    *Vous pouvez compter sur moi pour des traductions rapides et précises. 🚀*

    Le code source de ce bot est open source et peut être consulté sur ce dépôt Git :
    [Lien vers le code source](https://github.com/codingtuto/TG-TRANSLATOR-BOT/)

    👉 Alors, prêt à traduire ? Envoyez-moi un message et choisissez la langue !

    '''

    bot.reply_to(message, message_bienvenue, parse_mode='Markdown')
# Commande /fr
@bot.message_handler(commands=['fr'])
def traduire_fr(message):
    texte = message.text.replace('/fr', '').strip()
    if texte:
        reponse = traduire_texte(texte, 'en', 'fr')
        bot.reply_to(message, reponse)
    else:
        bot.reply_to(message, 'Veuillez spécifier le texte à traduire après la commande /fr.')

# Commande /en
@bot.message_handler(commands=['en'])
def traduire_en(message):
    texte = message.text.replace('/en', '').strip()
    if texte:
        reponse = traduire_texte(texte, 'fr', 'en')
        bot.reply_to(message, reponse)
    else:
        bot.reply_to(message, 'Veuillez spécifier le texte à traduire après la commande /en.')

# Répondre aux autres messages
@bot.message_handler(func=lambda message: True)
def repondre_autre(message):
    bot.reply_to(message, 'Veuillez utiliser la commande /fr ou /en pour traduire le texte.')

# Lancer le bot
bot.polling()
