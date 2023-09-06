import sqlite3, logging, os


class SqliteWork:
    def __init__(self):
        if os.path.isfile('todo.db') is False:
            logging.info('[SQLITE_WORK] создаём todo.db')
            self.conn = SqliteWork.create_db(os.listdir('schemas'))

        else: self.conn = sqlite3.connect('todo.db')


    def add_work(self, chat_id: int, text: str):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO works (chat_id, content) values ({chat_id},\'{text}\')')
        self.conn.commit()

    def get_works(self, chat_id: int):
        cursor = self.conn.cursor()
        cursor.execute(f'select * from works where chat_id = {chat_id}')
        res = cursor.fetchall()

        return res

    def add_expire_to_work(self, chat_id: int, work_id: int, time: str):
        if not self.check_work_exist(chat_id,work_id): return False

        cursor = self.conn.cursor()
        cursor.execute(f'update works set expires = \'{time}\' where post_id = {work_id}')
        self.conn.commit()

        return True

    def check_work_exist(self, chat_id: int, work_id: int):
        cursor = self.conn.cursor()
        cursor.execute(f'select * from works where chat_id = {chat_id} and post_id = {work_id}')
        res = cursor.fetchone()
        return not (res is None)

    def delete_work(self, chat_id: int, work_id: int):
        cursor = self.conn.cursor()
        cursor.execute(f'delete from works where chat_id = {chat_id} and post_id = {work_id}')
        self.conn.commit()

    def finish_work(self, chat_id: int,work_id: int):
        cursor = self.conn.cursor()
        cursor.execute(f'update works set finished = 1 where chat_id = {chat_id} and post_id = {work_id}')
        self.conn.commit()


    @staticmethod
    def create_db(schema_files: list[str]):
        con = sqlite3.connect('todo.db')
        cur = con.cursor()
        for file in schema_files:
            with open(f'schemas/{file}') as f:
                cur.execute(f.read())
                con.commit()

        return con