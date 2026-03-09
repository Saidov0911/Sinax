from aiogram import Router, F
from aiogram.types import CallbackQuery
import asyncpg
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from keyboards.inline import taken_application_kb, new_application_kb

router = Router()


async def get_db():
    return await asyncpg.connect(
        host=DB_HOST, port=int(DB_PORT),
        database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


@router.callback_query(F.data.startswith("take:"))
async def take_application(callback: CallbackQuery):
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

    await callback.message.edit_text(
        callback.message.text +
        f"\n\n📞 <b>{taker_name}</b> telefon qilmoqda...",
        reply_markup=taken_application_kb(app_id, taker_name),
        parse_mode='HTML'
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm:"))
async def confirm_application(callback: CallbackQuery):
    app_id = int(callback.data.split(":")[1])

    conn = await get_db()
    try:
        await conn.execute(
            'UPDATE applications_application SET status = $1 WHERE id = $2',
            'confirmed', app_id
        )
    finally:
        await conn.close()

    await callback.message.edit_text(
        callback.message.text.split("\n\n📞")[0] +
        "\n\n✅ <b>Tasdiqlandi</b>",
        reply_markup=None,
        parse_mode='HTML'
    )
    await callback.answer("Tasdiqlandi!")


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_application(callback: CallbackQuery):
    app_id = int(callback.data.split(":")[1])

    conn = await get_db()
    try:
        await conn.execute(
            'UPDATE applications_application SET status = $1 WHERE id = $2',
            'cancelled', app_id
        )
    finally:
        await conn.close()

    await callback.message.edit_text(
        callback.message.text.split("\n\n📞")[0] +
        "\n\n❌ <b>Bekor qilindi</b>",
        reply_markup=None,
        parse_mode='HTML'
    )
    await callback.answer("Bekor qilindi!")