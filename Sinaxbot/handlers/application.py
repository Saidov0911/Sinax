from aiogram import Router, F
from aiogram.types import CallbackQuery
import asyncpg
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from keyboards.inline import taken_application_kb

router = Router()


async def get_db():
    return await asyncpg.connect(
        host=DB_HOST, port=int(DB_PORT),
        database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


async def is_allowed(telegram_id: int) -> bool:
    conn = await get_db()
    try:
        row = await conn.fetchrow(
            '''SELECT id FROM applications_alloweduser
               WHERE telegram_id = $1 AND is_active = true''',
            telegram_id
        )
        return row is not None
    finally:
        await conn.close()


async def edit_all_messages(bot, app_id: int, new_text: str, reply_markup=None):
    """Barcha foydalanuvchilardagi xabarni tahrirlash"""
    conn = await get_db()
    try:
        messages = await conn.fetch(
            '''SELECT chat_id, message_id
               FROM applications_applicationmessage
               WHERE application_id = $1''',
            app_id
        )
    finally:
        await conn.close()

    for msg in messages:
        try:
            await bot.edit_message_text(
                chat_id=msg['chat_id'],
                message_id=msg['message_id'],
                text=new_text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        except Exception:
            pass


@router.callback_query(F.data.startswith("take:"))
async def take_application(callback: CallbackQuery):
    if not await is_allowed(callback.from_user.id):
        await callback.answer("Sizga ruxsat yo'q!", show_alert=True)
        return

    app_id = int(callback.data.split(":")[1])
    taker_name = callback.from_user.full_name

    conn = await get_db()
    try:
        app = await conn.fetchrow(
            'SELECT * FROM applications_application WHERE id = $1', app_id
        )

        if app['status'] != 'new':
            await callback.answer("Bu zayavkani allaqachon boshqasi olgan!", show_alert=True)
            return

        await conn.execute(
            '''UPDATE applications_application
               SET status = $1, taken_by = $2
               WHERE id = $3''',
            'in_progress', taker_name, app_id
        )
    finally:
        await conn.close()

    new_text = (
        f"📋 <b>Ariza #{app_id}</b>\n\n"
        f"👤 <b>Ism:</b> {app['name']}\n"
        f"📞 <b>Telefon:</b> {app['phone']}\n"
        f"🛠 <b>Xizmat:</b> {app['service_type']}\n\n"
        f"📞 <b>{taker_name}</b> telefon qilmoqda..."
    )

    await edit_all_messages(
        callback.bot, app_id, new_text,
        reply_markup=taken_application_kb(app_id, taker_name)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm:"))
async def confirm_application(callback: CallbackQuery):
    if not await is_allowed(callback.from_user.id):
        await callback.answer("Sizga ruxsat yo'q!", show_alert=True)
        return

    app_id = int(callback.data.split(":")[1])

    conn = await get_db()
    try:
        app = await conn.fetchrow(
            'SELECT * FROM applications_application WHERE id = $1', app_id
        )

        # Faqat olgan ishchi tasdiqlashi mumkin
        if app['taken_by'] != callback.from_user.full_name:
            await callback.answer(
                f"Bu zayavkani faqat {app['taken_by']} tasdiqlashi mumkin!",
                show_alert=True
            )
            return

        await conn.execute(
            'UPDATE applications_application SET status = $1 WHERE id = $2',
            'confirmed', app_id
        )
    finally:
        await conn.close()


    new_text = (
        f"📋 <b>Ariza #{app_id}</b>\n\n"
        f"👤 <b>Ism:</b> {app['name']}\n"
        f"📞 <b>Telefon:</b> {app['phone']}\n"
        f"🛠 <b>Xizmat:</b> {app['service_type']}\n\n"
        f"✅ <b>Tasdiqlandi</b>"
    )

    await edit_all_messages(callback.bot, app_id, new_text)
    await callback.answer("Tasdiqlandi!")


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_application(callback: CallbackQuery):
    if not await is_allowed(callback.from_user.id):
        await callback.answer("Sizga ruxsat yo'q!", show_alert=True)
        return

    app_id = int(callback.data.split(":")[1])

    conn = await get_db()
    try:
        app = await conn.fetchrow(
            'SELECT * FROM applications_application WHERE id = $1', app_id
        )

        # Faqat olgan ishchi bekor qilishi mumkin
        if app['taken_by'] != callback.from_user.full_name:
            await callback.answer(
                f"Bu zayavkani faqat {app['taken_by']} bekor qilishi mumkin!",
                show_alert=True
            )
            return

        await conn.execute(
            'UPDATE applications_application SET status = $1 WHERE id = $2',
            'cancelled', app_id
        )
    finally:
        await conn.close()

    new_text = (
        f"📋 <b>Ariza #{app_id}</b>\n\n"
        f"👤 <b>Ism:</b> {app['name']}\n"
        f"📞 <b>Telefon:</b> {app['phone']}\n"
        f"🛠 <b>Xizmat:</b> {app['service_type']}\n\n"
        f"❌ <b>Bekor qilindi</b>"
    )

    await edit_all_messages(callback.bot, app_id, new_text)
    await callback.answer("Bekor qilindi!")