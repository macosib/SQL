import sqlalchemy
import pandas

class SQL:

    def __init__(self, user_db, password_db, name_db):
        self.user_db = user_db
        self.password_db = password_db
        self.name_db = name_db
        self.engine = sqlalchemy.create_engine(f'postgresql://{user_db}:{password_db}@localhost:5432/{name_db}')
        self.connection = self.engine.connect()


def main():
    sql = SQL('oleg', 'test_password', 'Homework')

    def select_homework_4():

        first = sql.connection.execute(
            f"""SELECT album_name AS название,
            publication_year AS год_выхода_альбома
            FROM albums
            WHERE publication_year = 2018;""").fetchall()

        second = sql.connection.execute(
                f"""SELECT	track_name AS название_трека,
                    duration AS длительность_трека
                    FROM	tracks
                    ORDER BY	duration DESC
                    LIMIT 1;""").fetchall()

        third = sql.connection.execute(
                f"""SELECT	track_name AS название,
                    duration AS продолжительность
                    FROM	tracks
                    WHERE	duration >= 210000;""").fetchmany(20)
        fourth = sql.connection.execute(
            f"""SELECT	collection_name AS название
                FROM	collection
                WHERE	publication_year BETWEEN 2018 AND 2020;""").fetchmany(20)
        fifth = sql.connection.execute(
            f"""SELECT	singer_name AS имя_исполнителя
                FROM	artists_list
                WHERE	singer_name NOT LIKE '%% %%';""").fetchall()

        sixth = sql.connection.execute(
            f"""SELECT	track_name AS название
                FROM	tracks
                WHERE	track_name ILIKE '%%мой%%'	or track_name ILIKE '%%my%%';""").fetchall()

        print(pandas.DataFrame(first))
        print()
        print(pandas.DataFrame(second))
        print()
        print(pandas.DataFrame(third))
        print()
        print(pandas.DataFrame(fourth))
        print()
        print(pandas.DataFrame(fifth))
        print()
        print(pandas.DataFrame(sixth))
 
    select_homework_4()

main()