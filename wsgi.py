from threading import Thread
import asyncio
import bot
import api


if __name__ == '__main__':
    Thread(target=api.runner).start()
    asyncio.run(bot.app.run_polling())
