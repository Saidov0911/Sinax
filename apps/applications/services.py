import json
import requests
from django.conf import settings


def send_telegram_notification(application) -> bool:
    token = settings.BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
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
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps(reply_markup),
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False