import psycopg2
from psycopg2 import sql, Error
from DBscheme import DB_SCHEMA_SCRIPT

def setup_database(DB_HOST,DB_USER,DB_PORT,DB_PASSWORD,DB_NAME):
    try:
        # Подключаемся к стандартной БД postgres для создания новой БД
        conn = psycopg2.connect(
            dbname="postgres",  # стандартная БД для подключения
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True

        cursor = conn.cursor()

        # Проверяем существование БД
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
            .format(sql.Literal(DB_NAME))
        )

        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {}")
                .format(sql.Identifier(DB_NAME))
            )
            print(f"БД '{DB_NAME}' создана!")
        else:
            print(f"БД '{DB_NAME}' уже существует.")

        # Подключаемся к новой БД для создания схемы
        conn.close()
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(DB_SCHEMA_SCRIPT)
        conn.commit()
        print("Схема базы данных успешно создана")

    except Error as e:
        print("Ошибка PostgreSQL:", e)
    finally:
        if conn:
            conn.close()


