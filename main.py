from aiogram import Bot, types, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from sqlite_work import SqliteWork
import asyncio, logging, os, sqlite_work


class TodoBot:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.sqlite = SqliteWork()
        self.bot = Bot(token=os.environ['TODOBOT_TG_TOKEN'])
        self.dp = Dispatcher()
        #self.dp.message.register(self.start, CommandStart())
        self.dp.message.register(self.add_work, Command("add_work"))
        self.dp.message.register(self.get_works, Command("works"))
        self.dp.message.register(self.add_expire_to_work, Command("expire_work"))
        self.dp.message.register(self.delete_work, Command('delete_work'))
        self.dp.message.register(self.finish_work, Command('finish_work'))

    async def add_work(self, message: Message):
        chat_id: int = message.chat.id
        text: str = ' '.join(message.text.split()[1:])
        self.sqlite.add_work(chat_id, text)

        await message.reply('Задача добавлена.')

    async def get_works(self, message: Message):
        chat_id: int = message.chat.id

        works = self.sqlite.get_works(chat_id)
        for work in works:
            reply_text = f"""
                ID: {work[0]},\nОписание: {work[2]},\nЗаканчивается: {work[3]},\nЗавершена: {bool(work[4])}
            """
            await message.bot.send_message(chat_id,reply_text)

    async def add_expire_to_work(self, message: Message):
        chat_id: int = message.chat.id
        text: list[str] = message.text.split()
        work_id: int = int(text[1])
        time: str = text[2]

        result = self.sqlite.add_expire_to_work(chat_id,work_id,time)
        if result is False:
            await message.reply('Такой записи нет для вашего чата, или её просто не существует')
            return
        await message.reply(f'Установлен срок {time}')

    async def delete_work(self, message: Message):
        chat_id: int = message.chat.id
        work_id: int = int(message.text.split()[1])

        is_exist: bool = self.sqlite.check_work_exist(chat_id,work_id)
        if not is_exist:
            await message.reply('Такой записи нет для вашего чата, или её просто не существует')
            return

        self.sqlite.delete_work(chat_id,work_id)

        await message.reply(f'Запись {work_id} была успешно удалена')

    async def finish_work(self, message: Message):
        chat_id: int = message.chat.id
        text: list[str] = message.text.split()
        work_id: int = int(text[1])

        is_exist: bool = self.sqlite.check_work_exist(chat_id,work_id)
        if not is_exist:
            await message.reply('Такой записи нет для вашего чата, или её просто не существует')
            return

        self.sqlite.finish_work(chat_id,work_id)

        await message.reply(f'Запись {work_id} была помечена как завершённая')

if __name__ in "__main__":
    bot: TodoBot = TodoBot()
    asyncio.run(bot.dp.start_polling(bot.bot))