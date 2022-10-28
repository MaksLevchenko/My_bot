import json
import random
import re
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, Filters, MessageHandler, TypeHandler\
    , CommandHandler, BaseFilter

updater = Updater('Your_token')
dispatcher = updater.dispatcher

def echo(update, context):
    text = 'ECHO: ' + update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)

answer = ['Бесспорно', 'Никогда', 'Обязательно', 'Нет', 'Да', 'Конечно', 'Вы этого заслуживаете', 'Наверное',
          'Это случится завтра', 'Точно', 'Понятное дело', 'Точно не сейчас', 'Может быть',
          'Может быть, на следующей неделе?', 'Наверное', 'Наврятли', 'Это уже произошло!',
          'Скоро', 'Не бывать этому', 'Скорее всего да', 'Скорее всего нет']
def magic(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Привет, Мир! Я магический шар, и я знаю ответ на любой Ваш вопрос.',
        reply_markup=ask_reply_markup)

    name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Приветствую Вас, о повелитель {name}!',
        reply_markup=ask_reply_markup)

    context.bot.send_message(
            chat_id=update.effective_chat.id, text='Задайте мне вопрос, повелитель:',
            reply_markup=ask_reply_markup)

def magic_continue(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(random.choice(answer))
    update.message.reply_text(f'Есть ли у Вас ко мне ещё вопросы, о {name}? (Да, Нет): ')

def magic_2(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Задайте мне вопрос, повелитель:',
        reply_markup=ask_reply_markup)

def magic_end(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Возвращайтесь если возникнут вопросы, о {name}',
        reply_markup=ask_reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""
    Бот может здороваться на разных языках.
    Список поддерживаемых приветствий:
    - привет - русский
    - hello - английский
    - hola - испанский
    """)


def ru(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    update.message.reply_text(f'Привет {name}')


def en(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('hello')


def es(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('hola')


def not_supported(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Приветствие "{update.message.text}" не поддерживается.')


def get_greeting_filter(greeting: str) -> BaseFilter:
    return Filters.regex(re.compile(f'^{greeting}$', re.IGNORECASE)) & Filters.update.message

ask_reply_markup = ReplyKeyboardMarkup([['Подбросить монетку', 'Случайное число', 'Предсказания']], resize_keyboard=True)

def ask_what_to_do(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Что нужно сделать?', reply_markup=ask_reply_markup)

def get_coin_side():
    return 'Орёл' if random.randint(0,1) == 1 else 'Решка'

coin_inline_keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Подбросить ещё раз?',
                                                                          callback_data='flip_a_coin_again')]])

def flip_a_coin(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(get_coin_side(), reply_markup=coin_inline_keyboard_markup)

def flip_a_coin_again(update: Update, context: CallbackContext) -> None:
    text = f'{get_coin_side()}\nОтредактированно: {datetime.datetime.now().isoformat()}'
    update.callback_query.edit_message_text(text=text, reply_markup=coin_inline_keyboard_markup)

def get_random_number():
    return random.randint(0, 1000)

number_inline_keyboard_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Сгенерировать новое', callback_data='new_random_number')]])

def random_number(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(get_random_number(), reply_markup=number_inline_keyboard_markup)

def new_random_number(update: Update, context: CallbackContext) -> None:
    text = f'{get_random_number()}\nОтредактированно: {datetime.datetime.now().isoformat()}'
    update.callback_query.edit_message_text(text=text, reply_markup=number_inline_keyboard_markup)



def main() -> None:

    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(MessageHandler(get_greeting_filter('привет'), ru))
    updater.dispatcher.add_handler(MessageHandler(get_greeting_filter('hello'), en))
    updater.dispatcher.add_handler(MessageHandler(get_greeting_filter('hola'), es))
    updater.dispatcher.add_handler(CallbackQueryHandler(flip_a_coin_again, pattern='^flip_a_coin_again'))
    updater.dispatcher.add_handler(CallbackQueryHandler(new_random_number, pattern='^new_random_number'))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.update.message & Filters.text('Предсказания'), magic))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'[А-ЯЁёа-я .,]\?')), magic_continue))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Да'), magic_2))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Нет'), magic_end))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Случайное число'), random_number))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('Подбросить монетку'), flip_a_coin))
    updater.dispatcher.add_handler(TypeHandler(Update, ask_what_to_do))
    updater.dispatcher.add_handler(MessageHandler(Filters.update.message & Filters.text, not_supported))

    updater.start_polling()

    print('Started')

    updater.idle()


if __name__ == "__main__":
    main()