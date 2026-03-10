from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import asyncpg
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from keyboards.inline import list_kb

router = Router()

STATUS_LABELS = {
    'new': '🆕 Gaplashilmagan',
    'confirmed': '✅ Tasdiqlangan',
    'cancelled': '❌ Bekor qilingan',
}


async def get_db():
    return await asyncpg.connect(
        host=DB_HOST, port=int(DB_PORT),
        database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


@router.message(Command("list"))
async def cmd_list(message: Message):
    await message.answer(
        "📋 <b>Zayavkalar ro'yxati</b>\nQaysi ro'yxatni ko'rmoqchisiz?",
        reply_markup=list_kb(),
        parse_mode='HTML'
    )

@router.message(Command("myid"))
async def cmd_myid(message: Message):
    await message.answer(
        f"Sizning Telegram ID'ingiz: <code>{message.from_user.id}</code>",
        parse_mode='HTML'
    )


@router.callback_query(F.data.startswith("list:"))
async def show_list(callback: CallbackQuery):
    status = callback.data.split(":")[1]

    conn = await get_db()
    try:
        rows = await conn.fetch(
            '''SELECT id, name, phone, service_type, taken_by
               FROM applications_application
               WHERE status = $1
               ORDER BY created_at DESC
               LIMIT 20''',
            status
        )
    finally:
        await conn.close()

    if not rows:
        await callback.message.edit_text(
            f"{STATUS_LABELS[status]}\n\nHozircha zayavka yo'q.",
            reply_markup=list_kb(),
            parse_mode='HTML'
        )
        await callback.answer()
        return

    text = f"{STATUS_LABELS[status]}\n\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. 👤 {row['name']} | 📞 {row['phone']} | 🛠 {row['service_type']}"
        if row['taken_by']:
            text += f" | 📞 {row['taken_by']}"
        text += "\n"

    await callback.message.edit_text(
        text,
        reply_markup=list_kb(),
        parse_mode='HTML'
    )
    await callback.answer()