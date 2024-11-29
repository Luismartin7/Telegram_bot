import requests
from bs4 import BeautifulSoup
import telebot
import time
import threading

# Inicializa el bot con tu token
bot = telebot.TeleBot('7736364510:AAEvNU3pI0N3lAg2EL1-d1coUHlg625lDso')

# URL de la página web que quieres monitorear
url = 'https://www.wolorent.com/pisos-en-venta'

# Variable para almacenar el contenido anterior
previous_content = ''

# ID del chat al que se enviarán las notificaciones
chat_id = '-4746128668'


def check_for_updates():
    """Monitorea la página web para detectar cambios."""
    global previous_content
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Obtén el contenido HTML completo
            current_content = response.text.strip()

            # Compara el contenido actual con el anterior
            if current_content != previous_content:
                if previous_content != '':
                    bot.send_message(chat_id=chat_id,
                                     text='¡PISO NUEVO EN WOLORENT!')
                previous_content = current_content

            time.sleep(
                30)  # Esperar 30 segundos antes de la siguiente comprobación

        except Exception as e:
            print(f"Error durante la comprobación: {e}")
            time.sleep(60)  # Esperar un minuto antes de reintentar


# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "¡Hola! Estoy monitoreando la página web para ti, Luchito de mi corason."
    )


def start_bot():
    """Inicia el bot y el monitoreo en paralelo."""
    # Inicia el monitoreo en un hilo separado
    monitoring_thread = threading.Thread(target=check_for_updates, daemon=True)
    monitoring_thread.start()

    # Inicia el bot
    bot.polling(none_stop=True, interval=0, timeout=20)


if __name__ == '__main__':
    start_bot()
