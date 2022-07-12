SELECT
	album_name AS название,
	publication_year AS год_выхода_альбома
FROM
	albums
WHERE
	publication_year = 2018;

SELECT
	track_name AS название_трека,
	duration AS длительность_трека
FROM
	tracks
ORDER BY
	duration DESC
LIMIT 1;

SELECT	track_name AS название,
	duration AS продолжительность
FROM	tracks
WHERE	duration >= 210000;

SELECT	collection_name AS название
FROM	collection
WHERE	publication_year BETWEEN 2018 AND 2020;

SELECT	singer_name AS имя_исполнителя
FROM	artists_list
WHERE	singer_name NOT LIKE '% %';

SELECT	track_name AS название
FROM	tracks
WHERE	track_name ILIKE '%мой%'	or track_name ILIKE '%my%';
