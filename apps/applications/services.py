import json
import requests
from django.conf import settings
from .models import AllowedUser, ApplicationMessage


def send_telegram_notification(application) -> bool:
    token = settings.BOT_TOKEN
    group_chat_id = settings.TELEGRAM_GROUP_ID

    if not token:
        return False

    text = (
        f"📋 <b>Yangi ariza!</b>\n\n"
        f"👤 <b>Ism:</b> {application.name}\n"
        f"📞 <b>Telefon:</b> {application.phone}\n"
        f"🛠 <b>Xizmat:</b> {application.get_service_type_display()}"
    )

    reply_markup = {
        'inline_keyboard': [[
            {'text': '📞 Men olaman', 'callback_data': f'take:{application.id}'}
        ]]
    }

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # 1. Guruhga yuborish
    if group_chat_id:
        msg = _send_message(url, group_chat_id, text, reply_markup)
        if msg:
            ApplicationMessage.objects.create(
                application=application,
                chat_id=group_chat_id,
                message_id=msg['message_id']
            )

    # 2. Har bir ruxsatli ishchiga yuborish
    allowed_users = AllowedUser.objects.filter(is_active=True)
    for user in allowed_users:
        msg = _send_message(url, user.telegram_id, text, reply_markup)
        if msg:
            ApplicationMessage.objects.create(
                application=application,
                chat_id=user.telegram_id,
                message_id=msg['message_id']
            )

    return True


def _send_message(url, chat_id, text, reply_markup):
    try:
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'reply_markup': json.dumps(reply_markup),
        }
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get('result')
    except requests.RequestException:
        pass
    return None


def edit_all_messages(token, application, new_text, reply_markup=None):
    """Barcha foydalanuvchilardagi xabarni tahrirlash"""
    messages = ApplicationMessage.objects.filter(application=application)
    url = f"https://api.telegram.org/bot{token}/editMessageText"

    for msg in messages:
        try:
            payload = {
                'chat_id': msg.chat_id,
                'message_id': msg.message_id,
                'text': new_text,
                'parse_mode': 'HTML',
            }
            if reply_markup:
                payload['reply_markup'] = json.dumps(reply_markup)
            else:
                payload['reply_markup'] = json.dumps({'inline_keyboard': []})
            requests.post(url, data=payload, timeout=5)
        except requests.RequestException:
            pass