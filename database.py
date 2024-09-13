from typing import Tuple, Union

import pymysql


class DatabaseHandler:
    __conn: pymysql.Connection = None
    if __conn is None:
        __conn = pymysql.connect(host="localhost", user="root", password="root", database="wt_cp")

    @staticmethod
    def register_user(name: str, email: str, password: str) -> int:
        with DatabaseHandler.__conn.cursor() as curr:
            curr.execute("SELECT email FROM users WHERE email=%s", (email,))
            if curr.fetchone():
                return 0

        with DatabaseHandler.__conn.cursor() as curr:
            curr.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password),
            )

            DatabaseHandler.__conn.commit()
            return curr.lastrowid

    @staticmethod
    def get_user(email: str) -> Union[Tuple[int, str, str, str], None]:
        with DatabaseHandler.__conn.cursor() as curr:
            curr.execute(
                "SELECT id, name, email, password FROM users WHERE email=%s",
                (email,),
            )
            user = curr.fetchone()

        return user

    @staticmethod
    def add_contact(user_id: int, name: str, email: str, message: str):
        with DatabaseHandler.__conn.cursor() as curr:
            curr.execute(
                "INSERT INTO contacts (user_id, name, email, message) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, message),
            )
            DatabaseHandler.__conn.commit()
