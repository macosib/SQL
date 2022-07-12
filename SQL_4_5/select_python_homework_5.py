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

    def select_homework_5():
        first = sql.connection.execute(
            f"""SELECT COUNT(*), genre_id, genre_of_music.genre_name  FROM genres_and_artist
INNER JOIN genre_of_music on genres_and_artist.genre_id = genre_of_music.id
GROUP BY genre_id, genre_of_music.genre_name
ORDER BY genre_id;""").fetchall()

        first1 = sql.connection.execute(
            f"""SELECT COUNT(genres_and_artist.artist_id) AS Количество, genre_id AS Жанр FROM genres_and_artist
GROUP BY genre_id
ORDER BY genre_id;""").fetchall()

        second = sql.connection.execute(
            f"""SELECT COUNT(*) Количество_треков FROM tracks
WHERE album_id IN (SELECT id FROM albums WHERE publication_year BETWEEN 2019 AND 2020);""").fetchall()

        third = sql.connection.execute(
            f"""SELECT albums.album_name AS Имя_альбома,
album_id AS Альбом_ID, 
ROUND(AVG(tracks.duration)) AS Средняя_продолжительность_треков FROM albums
INNER JOIN tracks ON tracks.album_id = albums.id
GROUP BY Имя_альбома, Альбом_ID
ORDER BY Имя_альбома;""").fetchmany(20)
        fourth = sql.connection.execute(
            f"""SELECT artists_list.id, artists_list.singer_name FROM artists_list
WHERE artists_list.id NOT IN (SELECT artists_list.id FROM artists_list
JOIN albums_and_artists ON artists_list.id = albums_and_artists.artist_id
JOIN albums on albums_and_artists.album_id = albums.id
WHERE albums.publication_year = 2020)
ORDER BY artists_list.id;""").fetchmany(20)
        fifth = sql.connection.execute(
            f"""SELECT DISTINCT collection_name, singer_name  FROM collection
INNER JOIN track_list ON collection.id = track_list.collection_id
INNER JOIN tracks ON  track_list.track_id = tracks.id 
INNER JOIN albums ON tracks.album_id = albums.id 
INNER JOIN albums_and_artists ON albums_and_artists.album_id = albums.id 
INNER JOIN artists_list ON artists_list.id = albums_and_artists.artist_id
WHERE singer_name = 'Basta'
ORDER BY singer_name;""").fetchall()

        sixth = sql.connection.execute(
            f"""SELECT album_name, artist_id  FROM albums
JOIN albums_and_artists ON albums.id = albums_and_artists.album_id
WHERE artist_id IN (SELECT artist_id FROM genres_and_artist
GROUP BY artist_id
HAVING COUNT(*) > 1);""").fetchall()

        seventh = sql.connection.execute(
            f"""SELECT track_name, track_list.track_id  FROM tracks
LEFT JOIN track_list ON tracks.id =  track_list.track_id 
WHERE track_list.collection_id  IS NULL;""").fetchall()

        eighth = sql.connection.execute(
            f"""SELECT singer_name Имя_артиста, t.track_name Имя_трека, t.duration Длительность FROM artists_list al
JOIN albums_and_artists aa ON al.id = aa.artist_id 
JOIN albums a ON a.id = aa.album_id 
JOIN tracks t ON a.id = t.album_id
WHERE t.duration = (SELECT MIN(duration) FROM tracks);""").fetchall()

        ninth = sql.connection.execute(
            f"""SELECT album_name FROM albums a
WHERE a.id IN (SELECT album_id FROM (SELECT album_id, COUNT(*) AS Количество FROM tracks GROUP BY album_id) AS res
WHERE Количество = (SELECT Количество FROM (SELECT album_id, COUNT(*) AS Количество FROM tracks GROUP BY album_id) AS res2
ORDER BY res2.Количество LIMIT 1));""").fetchall()


        print(pandas.DataFrame(first))
        print()
        print(pandas.DataFrame(first1))
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
        print()
        print(pandas.DataFrame(seventh))
        print()
        print(pandas.DataFrame(eighth))
        print()
        print(pandas.DataFrame(ninth))

    select_homework_5()


main()
