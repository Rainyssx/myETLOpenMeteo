import psycopg2
from psycopg2 import sql, Error
from  DBscheme import DB_SCHEMA_SCRIPT

# Данные из Docker-контейнера
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "user"  # как в вашем `docker run`
DB_PASSWORD = "password"  # как в вашем `docker run`
NEW_DB_NAME = "db_for_openMeteo"  # название новой БД

try:
    # Подключаемся к БД "postgres" (она есть по умолчанию)
    conn = psycopg2.connect(
        dbname=NEW_DB_NAME,  # стандартная БД
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True  # чтобы CREATE DATABASE сработал

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}")
        .format(sql.Literal(NEW_DB_NAME))
    )

    if not cursor.fetchone():
    # Создаём БД, если её не
    # т
        cursor.execute(
            sql.SQL("CREATE DATABASE {}")
            .format(sql.Identifier(NEW_DB_NAME)))
        print(f"БД '{NEW_DB_NAME}' создана!")
    else:
        print(f"БД '{NEW_DB_NAME}' уже существует.")

    cursor.execute(DB_SCHEMA_SCRIPT)
    print(f"Вся база создана")


except Error as e:
    print("Ошибка PostgreSQL:", e)



