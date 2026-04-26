import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

SERVICES = [
    ("🤖 Бот-визитка", "Рассказывает о вас или бизнесе, показывает услуги, принимает заявки.\n💰 от $30"),
    ("🛒 Бот для магазина", "Каталог товаров, корзина, оформление заказа прямо в Telegram.\n💰 от $80"),
    ("📅 Бот-запись", "Клиенты записываются на услуги, вы получаете уведомления.\n💰 от $60"),
    ("🔔 Бот-рассылка", "Отправляет сообщения всем подписчикам по расписанию или вручную.\n💰 от $50"),
    ("⚙️ Бот под задачу", "Любая логика — парсинг, интеграция с API, автоматизация.\n💰 от $70"),
]


def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Услуги", callback_data="services")],
        [InlineKeyboardButton("💼 Примеры работ", callback_data="portfolio")],
        [InlineKeyboardButton("📞 Связаться", callback_data="contact")],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Назад", callback_data="back")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Привет! Я помогу вам заказать Telegram-бота.\n\n"
        "Разрабатываю ботов под любые задачи — от простых визиток "
        "до сложных систем с базой данных и оплатой.\n\n"
        "Выберите раздел:"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard())


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        lines = ["*Доступные услуги:*\n"]
        for name, desc in SERVICES:
            lines.append(f"*{name}*\n{desc}\n")
        text = "\n".join(lines)
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif query.data == "portfolio":
        text = (
            "*Примеры работ:*\n\n"
            "🔹 Бот-визитка для фрилансера — кнопки, услуги, контакты\n"
            "🔹 Бот для онлайн-магазина — каталог + корзина\n"
            "🔹 Бот-рассылка для Telegram-канала\n\n"
            "📌 Хотите увидеть демо — напишите мне, пришлю ссылку."
        )
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif query.data == "contact":
        text = (
            "*Связаться со мной:*\n\n"
            "✉️ Telegram: @MavletGerrey\n\n"
            "Напишите — отвечу в течение нескольких часов и обсудим ваш проект."
        )
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif query.data == "back":
        text = (
            "👋 Привет! Я помогу вам заказать Telegram-бота.\n\n"
            "Разрабатываю ботов под любые задачи — от простых визиток "
            "до сложных систем с базой данных и оплатой.\n\n"
            "Выберите раздел:"
        )
        await query.edit_message_text(text, reply_markup=main_keyboard())


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()


if __name__ == "__main__":
    main()
