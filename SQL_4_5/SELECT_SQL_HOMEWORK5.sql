--1.   Количество исполнителей в каждом жанре
--1.1
SELECT COUNT(*), genre_id, genre_of_music.genre_name  FROM genres_and_artist
INNER JOIN genre_of_music on genres_and_artist.genre_id = genre_of_music.id
GROUP BY genre_id, genre_of_music.genre_name
ORDER BY genre_id;
--1.2
SELECT COUNT(genres_and_artist.artist_id) AS Количество, genre_id AS Жанр FROM genres_and_artist
GROUP BY genre_id
ORDER BY genre_id;

--2) количество треков, вошедших в альбомы 2019-2020 годов

SELECT COUNT(*) Количество_треков FROM tracks
WHERE album_id IN (SELECT id FROM albums WHERE publication_year BETWEEN 2019 AND 2020);


--3) Средняя продолжительность треков по каждому альбому

SELECT albums.album_name AS Имя_альбома,
album_id AS Альбом_ID, 
ROUND(AVG(tracks.duration)) AS Средняя_продолжительность_треков FROM albums
INNER JOIN tracks ON tracks.album_id = albums.id
GROUP BY Имя_альбома, Альбом_ID
ORDER BY Имя_альбома;


--4) все исполнители, которые не выпустили альбомы в 2020 году

SELECT artists_list.id, artists_list.singer_name FROM artists_list
WHERE artists_list.id NOT IN (SELECT artists_list.id FROM artists_list
JOIN albums_and_artists ON artists_list.id = albums_and_artists.artist_id
JOIN albums on albums_and_artists.album_id = albums.id
WHERE albums.publication_year = 2020)
ORDER BY artists_list.id;


--5) названия сборников, в которых присутствует конкретный исполнитель (Basta);

SELECT DISTINCT collection_name, singer_name  FROM collection
INNER JOIN track_list ON collection.id = track_list.collection_id
INNER JOIN tracks ON  track_list.track_id = tracks.id 
INNER JOIN albums ON tracks.album_id = albums.id 
INNER JOIN albums_and_artists ON albums_and_artists.album_id = albums.id 
INNER JOIN artists_list ON artists_list.id = albums_and_artists.artist_id
WHERE singer_name = 'Basta'
ORDER BY singer_name;

--6) название альбомов, в которых присутствуют исполнители более 1 жанра 
--(поставил значение больше для наглядности)

SELECT album_name, artist_id  FROM albums
JOIN albums_and_artists ON albums.id = albums_and_artists.album_id
WHERE artist_id IN (SELECT artist_id FROM genres_and_artist
GROUP BY artist_id
HAVING COUNT(*) > 1);

--7) наименование треков, которые не входят в сборники

SELECT track_name, track_list.track_id  FROM tracks
LEFT JOIN track_list ON tracks.id =  track_list.track_id 
WHERE track_list.collection_id  IS NULL;

--8) исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
SELECT singer_name Имя_артиста, t.track_name Имя_трека, t.duration Длительность FROM artists_list al
JOIN albums_and_artists aa ON al.id = aa.artist_id 
JOIN albums a ON a.id = aa.album_id 
JOIN tracks t ON a.id = t.album_id
WHERE t.duration = (SELECT MIN(duration) FROM tracks);

--9) название альбомов, содержащих наименьшее количество треков.

SELECT album_name FROM albums a
WHERE a.id IN (SELECT album_id FROM (SELECT album_id, COUNT(*) AS Количество FROM tracks GROUP BY album_id) AS res
WHERE Количество = (SELECT Количество FROM (SELECT album_id, COUNT(*) AS Количество FROM tracks GROUP BY album_id) AS res2
ORDER BY res2.Количество LIMIT 1));
