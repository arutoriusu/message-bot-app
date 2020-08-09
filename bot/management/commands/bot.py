from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
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
def do_echo(update: Update, context: CallbackContext):
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


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
