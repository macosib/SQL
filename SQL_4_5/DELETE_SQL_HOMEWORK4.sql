SELECT * FROM genre_of_music;
SELECT * FROM artists_list;
SELECT * FROM tracks;
SELECT * FROM albums;
SELECT * FROM genres_and_artist;
SELECT * FROM albums_and_artists;
SELECT * FROM collection;
SELECT * FROM track_list;

DELETE FROM genres_and_artist;
DELETE FROM albums_and_artists;
DELETE FROM genre_of_music;
DELETE FROM artists_list;
DELETE FROM track_list;
DELETE FROM collection;
DELETE FROM tracks;
DELETE FROM albums;

ALTER SEQUENCE genre_of_music_id_seq RESTART WITH 1;
ALTER SEQUENCE artists_list_id_seq RESTART WITH 1;
ALTER SEQUENCE albums_id_seq RESTART WITH 1;
ALTER SEQUENCE tracks_id_seq RESTART WITH 1;
ALTER SEQUENCE collection_id_seq RESTART WITH 1;

