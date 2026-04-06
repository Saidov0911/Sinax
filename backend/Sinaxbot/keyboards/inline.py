from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_application_kb(app_id: int) -> InlineKeyboardMarkup:
    """Yangi zayavka uchun - faqat 'Men olaman' tugmasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📞 Men olaman",
            callback_data=f"take:{app_id}"
        )]
    ])


def taken_application_kb(app_id: int, taker_name: str) -> InlineKeyboardMarkup:
    """Kimdir olgandan keyin - Tasdiqlandi / Bekor qilindi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlandi",
                callback_data=f"confirm:{app_id}"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilindi",
                callback_data=f"cancel:{app_id}"
            ),
        ]
    ])


def list_kb() -> InlineKeyboardMarkup:
    """List komandasi uchun"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Gaplashilmaganlar", callback_data="list:new")],
        [InlineKeyboardButton(text="✅ Tasdiqlananlar", callback_data="list:confirmed")],
        [InlineKeyboardButton(text="❌ Bekor qilinganlar", callback_data="list:cancelled")],
    ])