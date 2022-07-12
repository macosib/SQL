CREATE TABLE IF NOT EXISTS genre_of_music (
id SERIAL PRIMARY KEY,
genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS collection (
id SERIAL PRIMARY KEY,
collection_name  VARCHAR(100) NOT NULL UNIQUE,
publication_year INTEGER NOT NULL,
CHECK(publication_year > 1900 AND publication_year < 2023)
);

CREATE TABLE IF NOT EXISTS albums (
id SERIAL PRIMARY KEY,
album_name VARCHAR(100) NOT NULL,
publication_year INTEGER NOT NULL,
CHECK(publication_year > 1900 AND publication_year < 2023)
);

CREATE TABLE IF NOT EXISTS tracks (
id SERIAL PRIMARY KEY,
album_id INTEGER,
track_name VARCHAR(100) NOT NULL,
duration INTEGER NOT NULL,
FOREIGN KEY (album_id)  REFERENCES albums (id)
);

CREATE TABLE IF NOT EXISTS artists_list (
id SERIAL PRIMARY KEY,
singer_name VARCHAR(100) NOT NULL, 
alias VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS track_list (
collection_id INTEGER NOT NULL,
track_id INTEGER NOT NULL,
PRIMARY KEY (collection_id, track_id),
FOREIGN KEY (collection_id)  REFERENCES collection (id),
FOREIGN KEY (track_id)  REFERENCES tracks (id)
);

CREATE TABLE IF NOT EXISTS genres_and_artist (
artist_id INTEGER NOT NULL,
genre_id INTEGER NOT NULL,
PRIMARY KEY (artist_id, genre_id),
FOREIGN KEY (artist_id)  REFERENCES artists_list (id),
FOREIGN KEY (genre_id)  REFERENCES genre_of_music (id)
);

CREATE TABLE IF NOT EXISTS albums_and_artists (
album_id INTEGER NOT NULL,
artist_id INTEGER NOT NULL,
PRIMARY KEY (album_id, artist_id),
FOREIGN KEY (album_id)  REFERENCES albums (id),
FOREIGN KEY (artist_id)  REFERENCES artists_list (id)
);


