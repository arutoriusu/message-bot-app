from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from bot.models import Message, User


request = Request(
            con_pool_size=8,
            connect_timeout=0.5,
            read_timeout=1.0,
        )
bot = Bot(
    request=request,
    token=settings.TOKEN,
)


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e
    
    return inner


@log_errors
def send_message_to_users(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    date = update.message.date

    user, _ = User.objects.get_or_create(
        pk=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    message = Message(
        user=user,
        text=text,
        date_for_send=date,
    )
    message.save()

    last_dog = text.rindex('@')
    result = text[last_dog:].index(' ')+last_dog
    only_users_list = text[:result]
    only_text = text[result:]
    list_of_users = only_users_list.split(' ')

    for u in list_of_users:
        u = u.replace('@', '')
        find_user_id = User.objects.filter(name=u)
        if find_user_id:
            bot.send_message(find_user_id.first().pk, text)

    reply_text = "Сообщение{} было отправлено людям: {}\n".format(only_text, only_users_list)
    update.message.reply_text(
        text = reply_text,
    )


@log_errors
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    date = update.message.date

    user, _ = User.objects.get_or_create(
        pk=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    update.message.reply_text(
        "Привет! Я бот, который отправляет сообщение указанным людям. Также они должны быть зарегистрированы у бота.\n\n"
        "Для указания людей, которым хочешь отправить сообщение, укажи их короткие адреса через пробел.\n\n"
        "Например: @ewq @qwe Привет ребята\n\n"
        "Для просмотра зарегистрированных пользователей используй команду /listusers")

    
@log_errors
def list_users(update: Update, context: CallbackContext):
    reply_text = "Список зарегистрированных пользователей:\n"
    all_users = User.objects.all()
    for user in all_users:
        reply_text += "@" + user.name + "\n"
    update.message.reply_text(reply_text)


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        
        updater = Updater(
            bot=bot,
            use_context=True,
        )


        start_handler = CommandHandler('start', start)
        updater.dispatcher.add_handler(start_handler)

        listusers_handler = CommandHandler('listusers', list_users)
        updater.dispatcher.add_handler(listusers_handler)

        message_handler = MessageHandler(Filters.text, send_message_to_users)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
