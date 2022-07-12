import my_spotify_library
import save_data_file
import sqlalchemy
import random



class SQL:

    def __init__(self, user_db, password_db, name_db):
        self.user_db = user_db
        self.password_db = password_db
        self.name_db = name_db
        self.engine = sqlalchemy.create_engine(f'postgresql://{user_db}:{password_db}@localhost:5432/{name_db}')
        self.connection = self.engine.connect()


def main():
    sql = SQL('oleg', 'test_password', 'Homework')
    # data = save_data_file.data # Выбрать, если нет аккаунта в spotify
    data = my_spotify_library.main() # Выбрать, если есть аккаунт в spotify
    my_collection_name = ['Mix collection', 'Silver collection', 'Gold collection',
                          'Bronze collection', 'Platinum collection', 'Super Top collection',
                          'The Best collection', 'New collection']

    def insert_genres():
        result = []
        for value in data:
            result.extend(value['artist_genres'])
        result = list(set(result))
        for item in result:
            sql.connection.execute(f"""
            INSERT INTO genre_of_music(genre_name)
            VALUES('{item}');
            """)

    def insert_artist():
        result = []
        for value in data:
            result.append(value['artist_name'])
        result = list(set(result))
        for item in result:
            sql.connection.execute(f"""
            INSERT INTO artists_list(singer_name, alias) 
            VALUES('{item}', 'No data');
            """)

    def insert_albums():
        result_list = [(value['name_album'], int(value['release_date'][:4])) for value in data]
        for item in result_list:
            sql.connection.execute(f"""
            INSERT INTO albums(album_name, publication_year) 
            VALUES('{item[0].rstrip("'")}', {item[1]});
            """)

    def insert_genres_and_artist():
        result = set()
        for album in data:
            for genre in album['artist_genres']:
                result.add((album['artist_name'], genre))
        for item in result:
            sql.connection.execute(f"""
            INSERT INTO genres_and_artist(artist_id, genre_id)
            VALUES({
            sql.connection.execute(f'''
                SELECT id
                FROM artists_list
                WHERE singer_name = '{item[0]}';
                ''').fetchone()[0]},
                    {
            sql.connection.execute(f'''
                SELECT id
                FROM genre_of_music
                WHERE genre_name = '{item[1]}';
                ''').fetchone()[0]});
            """)

    def insert_albums_and_artists():
        result = []
        for album in data:
            result.append((album['name_album'], album['artist_name']))
        result = list(set(result))
        for item in result:
            sql.connection.execute(f"""
            INSERT INTO albums_and_artists(album_id, artist_id)
            VALUES({
            sql.connection.execute(f'''
                SELECT id
                FROM albums
                WHERE album_name = '{item[0]}';
                ''').fetchone()[0]},
                    {
            sql.connection.execute(f'''
                SELECT id
                FROM artists_list
                WHERE singer_name = '{item[1]}';
                ''').fetchone()[0]});
            """)

    def insert_tracks():
        result = []
        for value in data:
            for track in value['album_tracks']:
                result.append((value['name_album'],
                               track['track_name'],
                               int(track['duration'])))
        result = list(set(result))
        for item in result:
            sql.connection.execute(f"""
            INSERT INTO tracks(album_id, track_name, duration)
            VALUES ({sql.connection.execute(f"SELECT id FROM albums WHERE album_name = '{item[0]}';").fetchone()[0]},
            '{item[1]}', {item[2]}) ;""")

    def insert_collection():
        collections_list = my_collection_name.copy()
        result = []
        while len(collections_list) != 0:
            name_collection = collections_list.pop(random.choice(range(0, len(collections_list))))
            result.append((name_collection, random.randint(2020, 2022)))
        for item in result:
            sql.connection.execute(f"""
              INSERT INTO collection(collection_name, publication_year)
              VALUES ('{item[0]}', {item[1]}) ;""")

    def insert_track_list():
        tracks_list = []
        for value in data:
            for track in value['album_tracks']:
                tracks_list.append(track['track_name'])
        count_tracks = len(tracks_list) // len(my_collection_name)
        collections_list = my_collection_name.copy()
        result = []
        while len(tracks_list) != 0 and len(collections_list) != 0:
            name_collection = collections_list.pop(random.choice(range(0, len(collections_list))))
            if count_tracks < len(tracks_list):
                for item in range(count_tracks + 1):
                    result.append((name_collection, tracks_list.pop(random.choice(range(0, len(tracks_list))))))
            else:
                for item in range(len(tracks_list)):
                    result.append((name_collection, tracks_list.pop(random.choice(range(0, len(tracks_list))))))
        for item in result:
            sql.connection.execute(f"""
              INSERT INTO track_list(collection_id, track_id)
              VALUES (
              {sql.connection.execute(f"SELECT id FROM collection WHERE collection_name = '{item[0]}';").fetchone()[0]},
              {sql.connection.execute(f"SELECT id FROM tracks WHERE track_name = '{item[1]}';").fetchone()[0]}
              ) ;""")

    insert_genres()
    insert_artist()
    insert_albums()
    insert_genres_and_artist()
    insert_albums_and_artists()
    insert_tracks()
    insert_collection()
    insert_track_list()


if __name__ == '__main__':
    main()
