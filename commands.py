import logging
import nest_asyncio
import ollama
from telegram import Update, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, CallbackQuery
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from settings import bot_settings

nest_asyncio.apply()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

user_ids = {}
context_memory = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=f'Привет, *{update.effective_user.first_name}*! '
             f'Чем могу вам помочь?',
        parse_mode="Markdown"
    )
    logging.log(level=logging.INFO, msg="/start message sent")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        "🤖 *Ollama Бот* 🤖\n\n"
        "Этот бот создан на базе мощных нейросетей на выбор, которые помогут вам находить ответы на сложные вопросы, "
        "обсуждать разнообразные темы, генерировать идеи и тексты, а также просто вести интересные беседы!\n\n"
        "*Что бот умеет?*\n"
        "- Отвечает на любые вопросы\n"
        "- Помогает решать задачи и обрабатывать данные\n"
        "- Проводит анализ текстов и генерирует текст по запросу\n"
        "- Поддерживает продуктивный диалог\n\n"
        "*Как использовать?*\n"
        "Просто напишите сообщение, и бот постарается предоставить вам наилучший ответ, исходя из своих возможностей."
    )
    photo = open("./res/ollama.png", "rb")
    await update.message.reply_photo(photo=photo)
    await update.message.reply_text(text=about_text, parse_mode="Markdown")
    logging.log(level=logging.INFO, msg="/about message sent")


async def github(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=f"Вы можете найти мой репозиторий на GitHub по следующей ссылке: {bot_settings.GITHUB_URL}"
    )
    logging.log(level=logging.INFO, msg="/github message sent")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id

        if user_id not in user_ids:
            user_ids[user_id] = {'last_message': None, 'preferences': {}}
            context_memory[user_id] = []

        message_text = update.message.text
        context_messages = context_memory[user_id]

        context_messages.append({'role': 'user', 'content': message_text})
        context_memory[user_id] = context_messages[-8:]
        logging.log(level=logging.INFO, msg="Added user's message to context")

        await update.message.chat.send_action(ChatAction.TYPING)

        response = ollama.chat(model="llama3.2-vision", messages=context_memory[user_id])
        bot_reply = response['message']['content']
        logging.log(level=logging.INFO, msg="Bot in process of response")

        context_messages.append({'role': 'assistant', 'content': bot_reply})
        context_memory[user_id] = context_messages[-8:]
        logging.log(level=logging.INFO, msg="Added bot's message to context")

        await update.message.reply_text(bot_reply)
        logging.log(level=logging.INFO, msg="Bot send response")

    except Exception as e:
        logging.error(f"Error while handling message: {e}")
        await update.message.reply_text('Произошла ошибка. Попробуйте еще раз.')
