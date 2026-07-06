import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

## Token va Admin ID
TOKEN = "8215613212:AAEmwln_zfLBYazuYbzynqC0Fqg_uTQvr_k"
ADMIN_ID = 7575052801

# Logging sozlamalari
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Bot va Dispatcher ob'ektlarini yaratish
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

## Shikoyat holati uchun FSM
class ComplaintState(StatesGroup):
    waiting_for_text = State()

## /start komandasi uchun handler
@dp.message(CommandStart())
async def start_command(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🛍 Mahsulotlar"))
    builder.add(types.KeyboardButton(text="ℹ️ Biz haqimizda"))
    builder.add(types.KeyboardButton(text="📞 Aloqa"))
    builder.add(types.KeyboardButton(text="📝 Shikoyatlar")) # Admin panel o'rniga
    builder.adjust(2)

    await message.answer(
        f"Xush kelibsiz, {message.from_user.full_name}! Botimizga start berdingiz.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

## "📞 Aloqa" tugmasi uchun handler
@dp.message(F.text == "📞 Aloqa")
async def contact_handler(message: types.Message):
    await message.answer(
        "<b>📞 Admin bilan bog'lanish:</b>\n\n"
        "👤 Ism: Boxoviddin\n"
        "🆔 Familiya: Zuxriddinov\n"
        "📞 Telefon: <code>+998886577553</code>\n\n"
        "Ushbu raqam orqali biz bilan bog'lanishingiz mumkin.",
        parse_mode="HTML"
    )

## "ℹ️ Biz haqimizda" tugmasi uchun handler
@dp.message(F.text == "ℹ️ Biz haqimizda")
async def about_us_handler(message: types.Message):
    await message.answer(
        "<b>🌟 Biz haqimizda batafsil ma'lumot!</b>\n\n"
        "Biz mijozlarimizga eng yuqori sifatli mahsulotlarni taqdim etishga intilamiz. "
        "Har bir mahsulotimiz sinchkovlik bilan tanlab olingan bo'lib, o'zining mustahkamligi va dizayni bilan ajralib turadi.\n\n"
        "✅ <b>Sifat kafolati:</b> Mahsulotlarimiz eng yaxshi materiallardan tayyorlangan.\n"
        "✅ <b>Xizmat ko'rsatish:</b> Har bir mijoz uchun individual yondashuv.\n"
        "✅ <b>Qulaylik:</b> Hamyonbop narxlar va tezkor yetkazib berish.\n\n"
        "Biz bilan hamkorlik qilish siz uchun eng to'g'ri tanlovdir! 🚀",
        parse_mode="HTML"
    )

## "📝 Shikoyatlar" tugmasi uchun handler
@dp.message(F.text == "📝 Shikoyatlar")
async def complaint_start(message: types.Message, state: FSMContext):
    await state.set_state(ComplaintState.waiting_for_text)
    await message.answer("Iltimos, shikoyat yoki taklifingizni yozib yuboring, biz buni adminga yetkazamiz:")

## Shikoyat matnini qabul qilish va adminga yuborish
@dp.message(ComplaintState.waiting_for_text)
async def process_complaint(message: types.Message, state: FSMContext):
    # Adminga yuborish
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 <b>Yangi shikoyat/taklif!</b>\n\n"
             f"Foydalanuvchi: {message.from_user.full_name}\n"
             f"ID: <code>{message.from_user.id}</code>\n\n"
             f"Matn: <i>{message.text}</i>"
    )
    
    # Foydalanuvchiga tasdiq xabari
    await message.answer("✅ Shikoyatingiz adminga yuborildi. Rahmat!")
    
    # Holatni tozalash
    await state.clear()

## Botni ishga tushirish funksiyasi
async def main():
    print("\n======================================")
    print("Bot muvaffaqiyatli ishga tushdi...")
    print("Telegram'ga o'tib botni tekshiring!")
    print("======================================\n")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
