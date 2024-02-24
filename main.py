import asyncio
import sqlite3
import getVp

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message 
from config import TOKEN

import kb
# sfasfsfasfdas
a = 0
bot = Bot(TOKEN)
dp = Dispatcher()   

@dp.message(Command('start'))
async def start(message : Message):
    await message.answer(f"Привет {message.from_user.first_name}, чтобы задать вопрос Сергею Андреевичу напиши в чат /napisat_vopros.\n\nВот пример /napisat_vopros Как ваши дела?", reply_markup=kb.main_kb)


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Возникли какие-то вопросы на пиши @feedback666_bot')


@dp.message(Command('napisat_vopros'))
async def vopros(message: Message, command: CommandObject | None=None ): 
    msg = command.args

    if not msg == None:
        db = sqlite3.connect('main.db')

        c = db.cursor()

        # c.execute("""CREATE TABLE vp (
        #           username text,
        #           vp text,
        #           otvet text
        # )""")

        c.execute(f"INSERT INTO vp VALUES ('{message.chat.id}', '{message.from_user.username}', '{msg}', 'None')")

        db.commit()
        db.close()
        
        # await message.answer("вопрос отправлен")
        await message.answer(getVp.postVp(msg))
    else:
        await message.answer("Вы не написали вопрос\nВот пример команды /napisat_vopros Как ваши дела?")
    await getVp.zapis_otveta()


@dp.message(F.text == "Мои вопросы")
async def myVp(message: Message):
    db = sqlite3.connect('main.db')
    c = db.cursor()

    id = message.chat.id
    c.execute("SELECT EXISTS(SELECT * FROM vp WHERE id = ?);", (id,))
    exists = c.fetchone()[0]

    if exists == 1:
        c.execute("SELECT vp, otvet FROM vp WHERE id = ?;", (id,))
        res = c.fetchall()    
        for i in res:
            vp_None = 'Ответа ещё нету' if i[1] == 'None' else i[1]
            await message.answer(f'Вопрос: {i[0]}\n\nОтвет: {vp_None}')

        db.close()
    else:
        await message.answer('Ты еще не задал вопросов!')


@dp.message(F.text == 'Лента вопросов')
async def lenta_vp(message: Message):
    vpp = await getVp.get_vp()
    otvv = await getVp.get_otvet()

    for question, answer in zip(vpp, otvv):
        await message.answer(f'Вопрос:\n{question}\n\nОтвет:\n{answer}')
    

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
        
