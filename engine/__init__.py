from Bot import Bot
token = "825926327:AAEfWbjOM1Y6peBa-tLrXqMEZ69LxYW6Xgo"

def main():
    """Функция работы бота."""
    bot = Bot(token)
    while True:
        bot.work()

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
