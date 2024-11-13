import logging

import nest_asyncio
import ollama
from telegram import Update
from telegram.ext import ContextTypes

nest_asyncio.apply()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_ids = {}
context_memory = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет, {update.effective_user.first_name}! Чем могу помочь?')


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        "🤖 *Llama3 Бот* 🤖\n\n"
        "Этот бот создан на базе мощной нейросети llama3, которая поможет вам находить ответы на сложные вопросы, "
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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_ids:
        user_ids[user_id] = {'last_message': None, 'preferences': {}}
        context_memory[user_id] = []

    message_text = update.message.text
    context_messages = context_memory[user_id]

    context_messages.append({'role': 'user', 'content': message_text})
    context_memory[user_id] = context_messages[-8:]

    try:
        response = ollama.chat(model='llama3', messages=context_memory[user_id])
        await update.message.reply_text(response['message']['content'])
    except Exception as e:
        logging.error(f"Error while getting response from ollama: {e}")
        await update.message.reply_text('Произошла ошибка, попробуйте позже.')
