import asyncio

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from commands import handle_message, start, about
from settings import bot_settings


async def main() -> None:
    application = ApplicationBuilder().token(bot_settings.FATHER_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
