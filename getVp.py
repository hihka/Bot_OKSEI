import aiohttp
import user_agent
import asyncio
import sqlite3
from aiogram import Bot
from config import TOKEN

from bs4 import BeautifulSoup

bot = Bot(TOKEN)


async def postVp(vp):
    data = {'question': str(vp)}
    headers = {"User-Agent": user_agent.generate_user_agent()}
    async with aiohttp.ClientSession() as session:
        async with session.post('https://ask.oksei.ru/add_question.php', headers=headers, data=data, ssl=False) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
            text = soup.get_text()
            return text


async def fetch_html(url):
    headers = {"User-Agent": user_agent.generate_user_agent()}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            return await response.text()


async def zapis_otveta():
    while True:
        await asyncio.sleep(43200)
        html = await fetch_html('https://ask.oksei.ru/questions')

        soup = BeautifulSoup(html, 'html.parser')
        vopros = soup.find_all('div', class_='text-question')
        vpp = [vppp.text.strip() for vppp in vopros]

        otvet = soup.find_all('div', class_='text-answer')
        ress = [otv.text.strip() for otv in otvet]
        
        db = sqlite3.connect('main.db') 
        c = db.cursor()

        c.execute("SELECT rowid, vp, id, otvet FROM vp;")  
        rows = c.fetchall()

        for b in range(len(rows)):
            for i in vpp:

                if i in rows[b][1]:
                    if rows[b][3] == 'None':
                        c.execute("UPDATE vp SET otvet = ? WHERE vp = ?", (ress[vpp.index(i)], vpp[vpp.index(i)]))

                        await bot.send_message(chat_id=rows[0][2], text=f'Вопрос: {rows[b][1]}\nОтвет: {ress[vpp.index(i)]}')

        db.commit()
        db.close()
       

async def get_otvet():
    html = await fetch_html('https://ask.oksei.ru/questions')
    soup = BeautifulSoup(html, 'html.parser')
    otvet = soup.find_all('div', class_='text-answer')
    ress = [otv.text.strip() for otv in otvet]
    return ress

async def get_vp():
    html = await fetch_html('https://ask.oksei.ru/questions')
    soup = BeautifulSoup(html, 'html.parser')
    otvet = soup.find_all('div', class_='text-question')
    ress = [otv.text.strip() for otv in otvet]
    return ress


