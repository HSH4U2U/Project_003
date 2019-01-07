import os, json
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured
import telegram
# import fbchat
# from fbchat import Client


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secret_file = os.path.join(BASE_DIR, './secrets.json')  # secrets.json 파일 위치를 명시
with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# 페메 보내기
# FB_ID = get_secret("FB_ID")
# FB_PW = get_secret("FB_PW")
# client = Client(FB_ID, FB_PW, max_tries=2)


# def send_fb_message(message, receiver_uid):
#     client.send(fbchat.models.Message(message), receiver_uid)


# email 보내기
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")


def send_email(title, message, receiver_list):
    send_mail(title, message, EMAIL_HOST_USER, receiver_list, fail_silently=False)


# telegram 보내기
TELEGRAM_TOKEN = get_secret("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_telegram(title, message, chat_id):
    text = str(title) + "\n" + str(message)
    bot.sendMessage(chat_id=chat_id, text=text)
