import logging
import os
from telegram import Update, constants, Bot
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
    ConversationHandler,
)
from soldiers import SoldierRepository
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Environment variable TELEGRAM_BOT_TOKEN is not set")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

NAME, BIRTHDATE = range(2)

soldiers_repository = SoldierRepository()


async def send_message(chat_id: str, message: str):
    bot = Bot(TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)


async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        raise ValueError("effective_chat is None")

    starting_text = """
    Hello! I'm a bot for finding soldiers.\n\n
    You can control me by sending these commands:\n
    /add - add soldier for finding\n
    /remove - remove soldier
    /show - show all soldiers\n\n
    -----\n
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=starting_text
    )


async def _show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(context._user_id)
    soldiers = soldiers_repository.get_by_chat_id(update.effective_chat.id)
    soldiers_text = ""
    if update.effective_chat is None:
        raise ValueError("effective_chat is None")

    if not soldiers:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No soldiers found. Use /add to add a soldier.",
        )
        return
    for soldier in soldiers:
        soldiers_text += (
            f"Name: {soldier.name}, Birthdate: {soldier.birthdate}\n"
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=soldiers_text
    )


async def _add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        raise ValueError("effective_chat is None")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What is the <b>NAME</b> of a soldier your are looking for?",
        parse_mode=constants.ParseMode.HTML,
    )

    return NAME


async def _name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text
    context.user_data["name"] = name
    logger.info("Name: %s", name)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
        What is the <b>BIRTHDATE</b> of a soldier your are looking for? Write
        data in format YYYY-MM-DD ex: 1972-04-28
        """,
        parse_mode=constants.ParseMode.HTML,
    )

    return BIRTHDATE


async def _birthdate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    try:
        birthdate = update.message.text
        context.user_data["birthdate"] = birthdate
        await update.message.reply_text(
            "Thank you! I will find the soldier for you."
        )

        soldiers_repository.add(
            update.effective_chat.id,
            context.user_data["name"],
            context.user_data["birthdate"].strftime("%Y-%m-%d"),
        )
        logger.info("Soldier added")

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "Invalid birthdate format. Format YYYY-MM-DD ex: 1972-04-28"
        )
        return BIRTHDATE


async def _unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", _start)
    show_handler = CommandHandler("show", _show)
    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", _add)],
        states={
            NAME: [MessageHandler(filters.TEXT, _name)],
            BIRTHDATE: [MessageHandler(filters.TEXT, _birthdate)],
        },
        fallbacks=[],
    )

    unknown_handler = MessageHandler(filters.COMMAND, _unknown)
    application.add_handler(start_handler)
    application.add_handler(show_handler)
    application.add_handler(add_conv_handler)
    application.add_handler(unknown_handler)

    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
